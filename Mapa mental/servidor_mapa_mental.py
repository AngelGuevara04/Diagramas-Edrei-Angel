"""
Servidor local para el editor de mapa mental.

Incluye:
- Servido de archivos estaticos del proyecto "Mapa mental".
- Endpoints de imagenes para buscar por etiqueta con Openverse/Wikimedia, Bing y DuckDuckGo.
"""

from __future__ import annotations

import argparse
import ast
import base64
import binascii
import json
import os
import random
import re
import sys
import threading
import time
import uuid
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib import parse as urlparse


PROJECT_ROOT = Path(__file__).resolve().parent
WORKSPACE_ROOT = PROJECT_ROOT.parent
MAX_BODY_BYTES = 12_000_000
VALID_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
DEFAULT_IMAGE_DIR = "ImagenesMapaMental"
DEFAULT_SUFFIX = ""
DEFAULT_PROVIDER = "openverse"
REVIEW_CANDIDATES_DIRNAME = "_review_candidates"
REVIEW_CANDIDATE_LIMIT = 8
DOWNLOAD_LOCK = threading.Lock()
JOBS_LOCK = threading.Lock()
JOBS: dict[str, dict[str, Any]] = {}
JOB_RETENTION_SECONDS = 1800
SUPPORTED_PROVIDERS = {"openverse", "bing", "ddg"}
PROVIDER_ENV_KEYS: dict[str, str] = {}
BING_PAUSE_EVERY = 6
BING_PAUSE_SECONDS = 1.2

if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

_IMAGE_HELPERS_ERROR: str | None = None
try:
    from utilidades.imagenes import (
        _collect_labels,
        buscar_candidatos_imagen,
        descargar_imagen_bing,
        descargar_imagen_ddg,
        descargar_imagen_desde_url,
        descargar_imagen_openverse,
        sanitize_filename,
    )
except Exception as exc:  # pragma: no cover - depende del entorno local
    _IMAGE_HELPERS_ERROR = str(exc)
    _collect_labels = None
    buscar_candidatos_imagen = None
    descargar_imagen_bing = None
    descargar_imagen_ddg = None
    descargar_imagen_desde_url = None
    descargar_imagen_openverse = None
    sanitize_filename = None


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def get_provider_api_key(provider: str) -> str:
    env_key = PROVIDER_ENV_KEYS.get(provider, "")
    if not env_key:
        return ""
    return str(os.getenv(env_key, "")).strip()


def provider_requires_key(provider: str) -> bool:
    return provider in PROVIDER_ENV_KEYS


def parse_python_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "si", "yes", "y"}:
            return True
        if lowered in {"0", "false", "no", "n"}:
            return False
    return default


def parse_mind_map_text(mind_map_text: str) -> dict[str, Any]:
    try:
        parsed = ast.literal_eval(mind_map_text)
    except Exception as exc:
        raise ValueError(f"mapa_ejemplo invalido: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("mapa_ejemplo debe ser un dict.")
    return parsed


def collect_labels(mind_map: dict[str, Any]) -> list[str]:
    if _collect_labels is None:
        raise RuntimeError("No se pudieron cargar utilidades.imagenes.")
    labels = _collect_labels(mind_map)
    unique_labels: list[str] = []
    seen: set[str] = set()
    for label in labels:
        text = str(label).strip()
        if text and text not in seen:
            unique_labels.append(text)
            seen.add(text)
    return unique_labels


def resolve_image_dir(image_dir_text: str | None) -> tuple[Path, Path]:
    raw = str(image_dir_text or DEFAULT_IMAGE_DIR).replace("\\", "/").strip()
    if not raw:
        raw = DEFAULT_IMAGE_DIR
    if re.match(r"^[a-zA-Z]:/", raw) or raw.startswith("/"):
        raise ValueError("IMAGE_DIR debe ser relativo al proyecto (sin ruta absoluta).")

    parts = [p for p in raw.split("/") if p]
    if not parts:
        parts = [DEFAULT_IMAGE_DIR]
    if any(part in {".", ".."} for part in parts):
        raise ValueError("IMAGE_DIR no puede contener '.' o '..'.")

    relative_dir = Path(*parts)
    absolute_dir = PROJECT_ROOT / relative_dir
    return relative_dir, absolute_dir


def resolve_image_file(image_dir_text: str | None, file_name_text: str | None) -> tuple[Path, Path, str, Path]:
    relative_dir, output_dir = resolve_image_dir(image_dir_text)
    raw_name = str(file_name_text or "").replace("\\", "/").strip()
    safe_name = Path(raw_name).name
    if not safe_name:
        raise ValueError("file_name es requerido.")
    if safe_name in {".", ".."}:
        raise ValueError("file_name invalido.")
    ext = Path(safe_name).suffix.lower()
    if ext not in VALID_IMAGE_EXTENSIONS:
        raise ValueError(f"Extension no permitida: {ext or '(sin extension)'}")
    target_path = output_dir / safe_name
    return relative_dir, output_dir, safe_name, target_path


def find_existing_image(output_dir: Path, stem: str) -> Path | None:
    for ext in VALID_IMAGE_EXTENSIONS:
        candidate = output_dir / f"{stem}{ext}"
        if candidate.exists():
            return candidate
    for candidate in output_dir.glob(f"{stem}.*"):
        if candidate.suffix.lower() in VALID_IMAGE_EXTENSIONS:
            return candidate
    return None


def build_web_path(relative_dir: Path, file_name: str) -> str:
    parts = [*relative_dir.parts, file_name]
    encoded = [urlparse.quote(part) for part in parts]
    return "/" + "/".join(encoded)


def build_review_candidates_path(relative_dir: Path, stem: str, provider: str) -> tuple[Path, Path]:
    safe_stem = sanitize_filename(stem or "nodo") if sanitize_filename else "nodo"
    safe_provider = sanitize_filename(provider or "provider") if sanitize_filename else "provider"
    rel = relative_dir / REVIEW_CANDIDATES_DIRNAME / safe_stem / safe_provider
    return rel, PROJECT_ROOT / rel


def ensure_image_for_label(
    label: str,
    provider: str,
    provider_api_key: str,
    suffix: str,
    output_dir: Path,
    force_refresh: bool,
    download_missing: bool,
) -> tuple[str, Path | None, str]:
    if sanitize_filename is None:
        raise RuntimeError("No se pudieron cargar utilidades.imagenes.")

    downloader_map = {
        "openverse": descargar_imagen_openverse,
        "bing": descargar_imagen_bing,
        "ddg": descargar_imagen_ddg,
    }
    downloader = downloader_map.get(provider)
    if downloader is None:
        raise RuntimeError(f"Proveedor no soportado: {provider}")

    file_stem = sanitize_filename(label) or "nodo"
    query = f"{label} {suffix}".strip()
    existing = None if force_refresh else find_existing_image(output_dir, file_stem)
    if existing is not None:
        return "cache", existing, query
    if not download_missing:
        return "missing", None, query

    with DOWNLOAD_LOCK:
        if provider in {"bing", "openverse", "ddg"}:
            ok = bool(downloader(query, file_stem, str(output_dir)))
        else:
            ok = bool(downloader(query, file_stem, str(output_dir), provider_api_key))
    if not ok:
        return "failed", None, query

    downloaded = find_existing_image(output_dir, file_stem)
    if downloaded is None:
        return "failed", None, query
    return "downloaded", downloaded, query


def _public_job_snapshot(job: dict[str, Any]) -> dict[str, Any]:
    return {
        "job_id": job["job_id"],
        "status": job["status"],
        "done": job["done"],
        "canceled": job["canceled"],
        "error": job["error"],
        "created_at": job["created_at"],
        "updated_at": job["updated_at"],
        "image_dir": job["image_dir"],
        "provider": job["provider"],
        "suffix": job["suffix"],
        "force_refresh": job["force_refresh"],
        "download_missing": job["download_missing"],
        "total_labels": job["total_labels"],
        "completed_labels": job["completed_labels"],
        "total_images": len(job["images"]),
        "downloaded": job["downloaded"],
        "cached": job["cached"],
        "missing": len(job["missing_labels"]),
        "failed": len(job["failures"]),
        "images": list(job["images"]),
        "missing_labels": list(job["missing_labels"]),
        "failures": list(job["failures"]),
    }


def _cleanup_old_jobs() -> None:
    now = time.time()
    with JOBS_LOCK:
        stale_ids = [
            job_id
            for job_id, job in JOBS.items()
            if job.get("done") and (now - float(job.get("updated_at", now))) > JOB_RETENTION_SECONDS
        ]
        for job_id in stale_ids:
            JOBS.pop(job_id, None)


def _cooperative_sleep(seconds: float, cancel_event: threading.Event, slice_seconds: float = 0.2) -> None:
    remaining = max(0.0, float(seconds))
    while remaining > 0:
        if cancel_event.is_set():
            return
        step = min(slice_seconds, remaining)
        time.sleep(step)
        remaining -= step


def _create_job(
    labels: list[str],
    image_dir: str,
    provider: str,
    suffix: str,
    force_refresh: bool,
    download_missing: bool,
) -> str:
    _cleanup_old_jobs()
    job_id = uuid.uuid4().hex
    now = time.time()
    with JOBS_LOCK:
        JOBS[job_id] = {
            "job_id": job_id,
            "status": "running",
            "done": False,
            "canceled": False,
            "error": None,
            "created_at": now,
            "updated_at": now,
            "image_dir": image_dir,
            "provider": provider,
            "suffix": suffix,
            "force_refresh": force_refresh,
            "download_missing": download_missing,
            "labels": list(labels),
            "total_labels": len(labels),
            "completed_labels": 0,
            "downloaded": 0,
            "cached": 0,
            "images": [],
            "missing_labels": [],
            "failures": [],
            "cancel_event": threading.Event(),
        }
    return job_id


def _cancel_job(job_id: str) -> bool:
    with JOBS_LOCK:
        job = JOBS.get(job_id)
        if not job:
            return False
        if job["done"]:
            return True
        job["cancel_event"].set()
        job["status"] = "cancel_requested"
        job["updated_at"] = time.time()
        return True


def _run_image_job(
    job_id: str,
    labels: list[str],
    provider: str,
    provider_api_key: str,
    suffix: str,
    output_dir: Path,
    relative_dir: Path,
    force_refresh: bool,
    download_missing: bool,
) -> None:
    try:
        for label in labels:
            with JOBS_LOCK:
                job = JOBS.get(job_id)
                if not job:
                    return
                cancel_event = job["cancel_event"]

            if cancel_event.is_set():
                with JOBS_LOCK:
                    job = JOBS.get(job_id)
                    if job:
                        job["status"] = "canceled"
                        job["done"] = True
                        job["canceled"] = True
                        job["updated_at"] = time.time()
                return

            status, path, query = ensure_image_for_label(
                label=label,
                provider=provider,
                provider_api_key=provider_api_key,
                suffix=suffix,
                output_dir=output_dir,
                force_refresh=force_refresh,
                download_missing=download_missing,
            )

            with JOBS_LOCK:
                job = JOBS.get(job_id)
                if not job:
                    return

                if path is None:
                    if status == "missing":
                        job["missing_labels"].append({"label": label, "query": query})
                    else:
                        job["failures"].append({"label": label, "query": query})
                else:
                    if status == "downloaded":
                        job["downloaded"] += 1
                    elif status == "cache":
                        job["cached"] += 1

                    job["images"].append(
                        {
                            "label": label,
                            "query": query,
                            "status": status,
                            "file_name": path.name,
                            "web_path": build_web_path(relative_dir, path.name),
                        }
                    )

                job["completed_labels"] += 1
                job["updated_at"] = time.time()
                completed = int(job["completed_labels"])

            # Pausa ligera por lotes para reducir bloqueos/rate-limit de Bing.
            if (
                provider == "bing"
                and BING_PAUSE_EVERY > 0
                and completed > 0
                and completed % BING_PAUSE_EVERY == 0
            ):
                extra_jitter = random.uniform(0.0, 0.6)
                _cooperative_sleep(BING_PAUSE_SECONDS + extra_jitter, cancel_event)

        with JOBS_LOCK:
            job = JOBS.get(job_id)
            if not job:
                return
            if job["cancel_event"].is_set():
                job["status"] = "canceled"
                job["canceled"] = True
            else:
                job["status"] = "completed"
            job["done"] = True
            job["updated_at"] = time.time()
    except Exception as exc:
        with JOBS_LOCK:
            job = JOBS.get(job_id)
            if not job:
                return
            job["status"] = "error"
            job["error"] = str(exc)
            job["done"] = True
            job["updated_at"] = time.time()


class MindMapEditorHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stdout.write(f"[http] {self.address_string()} - {fmt % args}\n")

    def send_json(self, payload: dict[str, Any], status: int = 200) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _read_json_body(self) -> tuple[dict[str, Any] | None, str | None]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0:
            return None, "Body vacio."
        if length > MAX_BODY_BYTES:
            return None, "Body demasiado grande."

        try:
            raw_body = self.rfile.read(length).decode("utf-8", errors="replace")
            payload = json.loads(raw_body)
        except json.JSONDecodeError:
            return None, "JSON invalido en la solicitud."
        if not isinstance(payload, dict):
            return None, "JSON invalido: se esperaba un objeto."
        return payload, None

    def _parse_image_request(
        self,
        payload: dict[str, Any],
    ) -> tuple[dict[str, Any] | None, str | None]:
        mind_map_text = str(payload.get("mind_map_text", "")).strip()
        if not mind_map_text:
            return None, "mind_map_text no puede estar vacio."

        suffix = str(payload.get("suffix", DEFAULT_SUFFIX)).strip()
        provider = str(payload.get("provider", DEFAULT_PROVIDER)).strip().lower() or DEFAULT_PROVIDER
        if provider not in SUPPORTED_PROVIDERS:
            return None, f"provider no soportado. Opciones: {', '.join(sorted(SUPPORTED_PROVIDERS))}."
        force_refresh = parse_python_bool(payload.get("force_refresh"), default=False)
        download_missing = parse_python_bool(payload.get("download_missing"), default=True)
        max_labels_raw = payload.get("max_labels")
        max_labels = None
        if max_labels_raw not in (None, ""):
            try:
                max_labels = max(1, int(max_labels_raw))
            except Exception:
                return None, "max_labels debe ser numerico."

        try:
            mind_map = parse_mind_map_text(mind_map_text)
            labels = collect_labels(mind_map)
            if max_labels is not None:
                labels = labels[:max_labels]
            relative_dir, output_dir = resolve_image_dir(payload.get("image_dir"))
            output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            return None, str(exc)

        provider_api_key = get_provider_api_key(provider)
        if download_missing and provider_requires_key(provider) and not provider_api_key:
            env_name = PROVIDER_ENV_KEYS.get(provider, "API_KEY")
            return None, f"Falta API key para {provider}. Define {env_name} en .env o entorno."

        return {
            "labels": labels,
            "provider": provider,
            "provider_api_key": provider_api_key,
            "suffix": suffix,
            "force_refresh": force_refresh,
            "download_missing": download_missing,
            "relative_dir": relative_dir,
            "output_dir": output_dir,
        }, None

    def _build_sync_result(
        self,
        labels: list[str],
        provider: str,
        provider_api_key: str,
        suffix: str,
        force_refresh: bool,
        download_missing: bool,
        relative_dir: Path,
        output_dir: Path,
    ) -> dict[str, Any]:
        images: list[dict[str, Any]] = []
        failures: list[dict[str, Any]] = []
        missing: list[dict[str, Any]] = []
        downloaded = 0
        cached = 0

        for label in labels:
            status, path, query = ensure_image_for_label(
                label=label,
                provider=provider,
                provider_api_key=provider_api_key,
                suffix=suffix,
                output_dir=output_dir,
                force_refresh=force_refresh,
                download_missing=download_missing,
            )
            if path is None:
                if status == "missing":
                    missing.append({"label": label, "query": query})
                else:
                    failures.append({"label": label, "query": query})
                continue

            if status == "downloaded":
                downloaded += 1
            elif status == "cache":
                cached += 1

            images.append(
                {
                    "label": label,
                    "query": query,
                    "status": status,
                    "file_name": path.name,
                    "web_path": build_web_path(relative_dir, path.name),
                }
            )

        return {
            "ok": True,
            "image_dir": str(relative_dir).replace("\\", "/"),
            "provider": provider,
            "suffix": suffix,
            "force_refresh": force_refresh,
            "download_missing": download_missing,
            "total_labels": len(labels),
            "total_images": len(images),
            "downloaded": downloaded,
            "cached": cached,
            "missing": len(missing),
            "failed": len(failures),
            "images": images,
            "missing_labels": missing,
            "failures": failures,
        }

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Allow", "GET,POST,OPTIONS")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        split = urlparse.urlsplit(self.path)
        route = split.path
        if route == "/api/images/status":
            providers = {
                "openverse": {"configured": True, "env_key": None},
                "bing": {"configured": True, "env_key": None},
                "ddg": {"configured": descargar_imagen_ddg is not None, "env_key": None},
            }
            self.send_json(
                {
                    "ok": _IMAGE_HELPERS_ERROR is None,
                    "bing_ready": _IMAGE_HELPERS_ERROR is None,
                    "providers": providers,
                    "error": _IMAGE_HELPERS_ERROR,
                }
            )
            return
        if route == "/api/images/google-links":
            params = urlparse.parse_qs(split.query or "")
            mind_map_text = str((params.get("mind_map_text") or [""])[0]).strip()
            if not mind_map_text:
                self.send_json({"ok": False, "error": "mind_map_text es requerido."}, status=400)
                return
            try:
                mind_map = parse_mind_map_text(mind_map_text)
                labels = sorted(list(set(collect_labels(mind_map))))
                self.send_json({"ok": True, "labels": labels, "total": len(labels)})
            except Exception as exc:
                self.send_json({"ok": False, "error": str(exc)}, status=400)
            return
        if route in {"/api/images/search/status", "/api/images/bing/status"}:
            params = urlparse.parse_qs(split.query or "")
            job_id = str((params.get("job_id") or [""])[0]).strip()
            if not job_id:
                self.send_json({"ok": False, "error": "job_id es requerido."}, status=400)
                return
            with JOBS_LOCK:
                job = JOBS.get(job_id)
                snapshot = _public_job_snapshot(job) if job else None
            if snapshot is None:
                self.send_json({"ok": False, "error": "Job no encontrado."}, status=404)
                return
            self.send_json({"ok": True, **snapshot})
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        route = urlparse.urlsplit(self.path).path
        image_search_routes = {
            "/api/images/search",
            "/api/images/search/start",
            "/api/images/search/cancel",
            "/api/images/bing",
            "/api/images/bing/start",
            "/api/images/bing/cancel",
        }
        image_review_routes = {
            "/api/images/review/delete",
            "/api/images/review/write",
            "/api/images/review/candidates",
        }
        if route not in {
            *image_search_routes,
            *image_review_routes,
        }:
            self.send_json({"ok": False, "error": "Ruta no encontrada."}, status=404)
            return

        if _IMAGE_HELPERS_ERROR is not None and route in image_search_routes:
            self.send_json(
                {
                    "ok": False,
                    "error": (
                        "No se pudo cargar utilidades/imagenes.py. "
                        f"Detalle: {_IMAGE_HELPERS_ERROR}"
                    ),
                },
                status=503,
            )
            return

        payload, body_error = self._read_json_body()
        if body_error:
            status_code = 413 if "demasiado grande" in body_error else 400
            self.send_json({"ok": False, "error": body_error}, status=status_code)
            return

        assert payload is not None

        if route == "/api/images/review/delete":
            try:
                relative_dir, output_dir, safe_name, target_path = resolve_image_file(
                    payload.get("image_dir"),
                    payload.get("file_name"),
                )
                output_dir.mkdir(parents=True, exist_ok=True)
                deleted = False
                if target_path.exists():
                    target_path.unlink()
                    deleted = True
                self.send_json(
                    {
                        "ok": True,
                        "deleted": deleted,
                        "file_name": safe_name,
                        "image_dir": str(relative_dir).replace("\\", "/"),
                    }
                )
            except Exception as exc:
                self.send_json({"ok": False, "error": str(exc)}, status=400)
            return

        if route == "/api/images/review/write":
            try:
                relative_dir, output_dir, safe_name, target_path = resolve_image_file(
                    payload.get("image_dir"),
                    payload.get("file_name"),
                )
                output_dir.mkdir(parents=True, exist_ok=True)
                image_b64 = str(payload.get("image_base64", "")).strip()
                if not image_b64:
                    raise ValueError("image_base64 no puede estar vacio.")
                if image_b64.startswith("data:"):
                    comma_idx = image_b64.find(",")
                    if comma_idx <= 0:
                        raise ValueError("image_base64 invalido.")
                    image_b64 = image_b64[comma_idx + 1 :]
                try:
                    raw_bytes = base64.b64decode(image_b64, validate=True)
                except (ValueError, binascii.Error) as exc:
                    raise ValueError("image_base64 invalido.") from exc
                if not raw_bytes:
                    raise ValueError("image_base64 vacio tras decodificar.")
                target_path.write_bytes(raw_bytes)
                self.send_json(
                    {
                        "ok": True,
                        "file_name": safe_name,
                        "image_dir": str(relative_dir).replace("\\", "/"),
                        "web_path": build_web_path(relative_dir, safe_name),
                        "bytes_written": len(raw_bytes),
                    }
                )
            except Exception as exc:
                self.send_json({"ok": False, "error": str(exc)}, status=400)
            return

        if route == "/api/images/review/candidates":
            try:
                if buscar_candidatos_imagen is None or descargar_imagen_desde_url is None or sanitize_filename is None:
                    raise RuntimeError("No se pudieron cargar utilidades.imagenes para candidatos.")

                label = str(payload.get("label", "")).strip()
                if not label:
                    raise ValueError("label es requerido.")

                provider = str(payload.get("provider", DEFAULT_PROVIDER)).strip().lower() or DEFAULT_PROVIDER
                if provider not in SUPPORTED_PROVIDERS:
                    raise ValueError(f"provider no soportado. Opciones: {', '.join(sorted(SUPPORTED_PROVIDERS))}.")

                suffix = str(payload.get("suffix", DEFAULT_SUFFIX)).strip()
                max_results_raw = payload.get("max_results", REVIEW_CANDIDATE_LIMIT)
                try:
                    max_results = max(1, min(20, int(max_results_raw)))
                except Exception:
                    max_results = REVIEW_CANDIDATE_LIMIT

                force_refresh = parse_python_bool(payload.get("force_refresh"), default=False)
                relative_dir, output_dir = resolve_image_dir(payload.get("image_dir"))
                output_dir.mkdir(parents=True, exist_ok=True)

                stem = sanitize_filename(label) or "nodo"
                rel_candidates_dir, abs_candidates_dir = build_review_candidates_path(relative_dir, stem, provider)
                abs_candidates_dir.mkdir(parents=True, exist_ok=True)

                if force_refresh:
                    for old in abs_candidates_dir.glob("*"):
                        if old.is_file() and old.suffix.lower() in VALID_IMAGE_EXTENSIONS:
                            old.unlink()

                cached_files = sorted(
                    [
                        p
                        for p in abs_candidates_dir.glob("*")
                        if p.is_file() and p.suffix.lower() in VALID_IMAGE_EXTENSIONS
                    ],
                    key=lambda p: p.name.lower(),
                )

                query = f"{label} {suffix}".strip()
                query_fallback = str(label or "").strip()
                if len(cached_files) < max_results:
                    urls = buscar_candidatos_imagen(provider, query, max_results=max_results * 2)
                    if not urls and query_fallback and query_fallback.lower() != query.lower():
                        urls = buscar_candidatos_imagen(
                            provider,
                            query_fallback,
                            max_results=max_results * 2,
                        )
                        query = query_fallback
                    existing_names = {p.name.lower() for p in cached_files}
                    added = 0
                    for idx, url in enumerate(urls, start=1):
                        if len(cached_files) >= max_results:
                            break
                        file_name = descargar_imagen_desde_url(
                            url=url,
                            file_stem=f"{idx:02d}_{stem}",
                            output_dir=str(abs_candidates_dir),
                        )
                        if not file_name:
                            continue
                        lower_name = file_name.lower()
                        if lower_name in existing_names:
                            continue
                        existing_names.add(lower_name)
                        candidate_path = abs_candidates_dir / file_name
                        if candidate_path.exists():
                            cached_files.append(candidate_path)
                            added += 1
                    if added > 0:
                        cached_files = sorted(cached_files, key=lambda p: p.name.lower())

                files_payload = [
                    {
                        "file_name": p.name,
                        "web_path": build_web_path(rel_candidates_dir, p.name),
                    }
                    for p in cached_files[:max_results]
                ]
                self.send_json(
                    {
                        "ok": True,
                        "provider": provider,
                        "label": label,
                        "query": query,
                        "image_dir": str(relative_dir).replace("\\", "/"),
                        "cache_dir": str(rel_candidates_dir).replace("\\", "/"),
                        "total_candidates": len(files_payload),
                        "files": files_payload,
                    }
                )
            except Exception as exc:
                self.send_json({"ok": False, "error": str(exc)}, status=400)
            return

        if route in {"/api/images/search/cancel", "/api/images/bing/cancel"}:
            job_id = str(payload.get("job_id", "")).strip()
            if not job_id:
                self.send_json({"ok": False, "error": "job_id es requerido."}, status=400)
                return
            cancelled = _cancel_job(job_id)
            if not cancelled:
                self.send_json({"ok": False, "error": "Job no encontrado."}, status=404)
                return
            self.send_json({"ok": True, "job_id": job_id, "message": "Cancelacion solicitada."})
            return

        parsed_request, parse_error = self._parse_image_request(payload)
        if parse_error:
            self.send_json({"ok": False, "error": parse_error}, status=400)
            return

        assert parsed_request is not None
        labels = parsed_request["labels"]
        provider = parsed_request["provider"]
        provider_api_key = parsed_request["provider_api_key"]
        suffix = parsed_request["suffix"]
        force_refresh = parsed_request["force_refresh"]
        download_missing = parsed_request["download_missing"]
        relative_dir = parsed_request["relative_dir"]
        output_dir = parsed_request["output_dir"]

        if route in {"/api/images/search/start", "/api/images/bing/start"}:
            job_id = _create_job(
                labels=labels,
                image_dir=str(relative_dir).replace("\\", "/"),
                provider=provider,
                suffix=suffix,
                force_refresh=force_refresh,
                download_missing=download_missing,
            )
            worker = threading.Thread(
                target=_run_image_job,
                kwargs={
                    "job_id": job_id,
                    "labels": labels,
                    "provider": provider,
                    "provider_api_key": provider_api_key,
                    "suffix": suffix,
                    "output_dir": output_dir,
                    "relative_dir": relative_dir,
                    "force_refresh": force_refresh,
                    "download_missing": download_missing,
                },
                daemon=True,
            )
            worker.start()
            self.send_json(
                {
                    "ok": True,
                    "job_id": job_id,
                    "status": "running",
                    "image_dir": str(relative_dir).replace("\\", "/"),
                    "provider": provider,
                    "suffix": suffix,
                    "force_refresh": force_refresh,
                    "download_missing": download_missing,
                    "total_labels": len(labels),
                }
            )
            return

        result = self._build_sync_result(
            labels=labels,
            provider=provider,
            provider_api_key=provider_api_key,
            suffix=suffix,
            force_refresh=force_refresh,
            download_missing=download_missing,
            relative_dir=relative_dir,
            output_dir=output_dir,
        )
        self.send_json(result)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Servidor local del editor de mapa mental.")
    parser.add_argument("--host", default="127.0.0.1", help="Host de escucha (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Puerto (default: 8000)")
    return parser.parse_args()


def main() -> None:
    load_env_file(PROJECT_ROOT / ".env")
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), MindMapEditorHandler)
    print(f"Servidor iniciado en http://{args.host}:{args.port}/")
    print("Endpoint imagenes: POST /api/images/search (compat: /api/images/bing)")
    print("Jobs imagenes: POST /api/images/search/start | GET /api/images/search/status?job_id=... | POST /api/images/search/cancel")
    print("Revision imagenes: POST /api/images/review/write | POST /api/images/review/delete")
    print("Estado imagenes: GET /api/images/status")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
