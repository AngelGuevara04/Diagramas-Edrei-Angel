"""
Servidor local para el editor de mapa conceptual.

Incluye:
- Servido de archivos estaticos del proyecto.
- Endpoint POST /api/ia/concept-map para aplicar cambios al concept_map usando Gemini.

Uso:
    python servidor_mapa_conceptual.py --port 8000

Variables de entorno:
- GEMINI_API_KEY (recomendada)
- GOOGLE_API_KEY (alternativa)

Tambien se puede cargar desde un archivo .env en esta misma carpeta.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from pprint import pformat
from typing import Any
from urllib import error as urlerror
from urllib import parse as urlparse
from urllib import request as urlrequest


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_MODEL = "gemini-2.5-flash-lite"
MAX_BODY_BYTES = 1_500_000


def load_env_file(env_path: Path) -> None:
    """Carga variables KEY=VALUE de .env sin dependencias externas."""
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


def get_api_key() -> str:
    load_env_file(PROJECT_ROOT / ".env")
    return (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "").strip()


def extract_first_json(text: str) -> Any:
    """Extrae el primer JSON valido desde un texto libre."""
    decoder = json.JSONDecoder()
    cleaned = text.strip()

    # Intenta JSON directo primero.
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Remueve fences markdown comunes.
    cleaned = cleaned.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Busca el primer objeto/array decodificable.
    for i, ch in enumerate(cleaned):
        if ch not in "{[":
            continue
        try:
            obj, _ = decoder.raw_decode(cleaned[i:])
            return obj
        except json.JSONDecodeError:
            continue
    raise ValueError("No se pudo extraer JSON de la respuesta del modelo.")


def collect_text_from_gemini_response(response_payload: dict[str, Any]) -> str:
    candidates = response_payload.get("candidates") or []
    if not candidates:
        raise ValueError("Gemini no devolvio candidatos.")
    first = candidates[0]
    content = first.get("content") or {}
    parts = content.get("parts") or []
    texts: list[str] = []
    for part in parts:
        if isinstance(part, dict) and isinstance(part.get("text"), str):
            texts.append(part["text"])
    if not texts:
        raise ValueError("Gemini no devolvio texto util en el primer candidato.")
    return "\n".join(texts).strip()


def call_gemini_for_concept_map(
    api_key: str,
    model: str,
    instruction: str,
    concept_map_text: str,
) -> tuple[list[Any], str]:
    """Llama a Gemini y devuelve (concept_map, texto_bruto)."""
    system_instruction = (
        "Eres un asistente experto en mapas conceptuales de Draw.io.\n"
        "Tu tarea es modificar un concept_map existente siguiendo la instruccion del usuario.\n"
        "Responde solo JSON valido y nada mas."
    )

    user_prompt = (
        "Aplica la instruccion al concept_map actual.\n"
        "Debes devolver un JSON con esta forma exacta:\n"
        "{\n"
        '  "concept_map": [ ... ]\n'
        "}\n\n"
        "Reglas:\n"
        "- Mantener estructura compatible con el generador: lista principal, grupos, subtitulos y ramas.\n"
        "- En ramas, cada entrada conceptual debe ser lista de dos posiciones [texto, conector] o [null, conector].\n"
        "- No uses markdown ni bloques de codigo.\n\n"
        f"Instruccion del usuario:\n{instruction}\n\n"
        f"concept_map actual:\n{concept_map_text}\n"
    )

    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{urlparse.quote(model, safe='-._')}:generateContent?key={urlparse.quote(api_key)}"
    )
    payload = {
        "system_instruction": {"parts": [{"text": system_instruction}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json",
        },
    }

    body = json.dumps(payload).encode("utf-8")
    req = urlrequest.Request(
        endpoint,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )

    try:
        with urlrequest.urlopen(req, timeout=60) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except urlerror.HTTPError as exc:
        detail = ""
        try:
            detail = exc.read().decode("utf-8", errors="replace")
        except Exception:
            detail = ""
        raise RuntimeError(f"Gemini HTTP {exc.code}: {detail or exc.reason}") from exc
    except urlerror.URLError as exc:
        raise RuntimeError(f"No se pudo conectar con Gemini: {exc.reason}") from exc

    data = json.loads(raw)
    text = collect_text_from_gemini_response(data)
    extracted = extract_first_json(text)

    if isinstance(extracted, list):
        concept_map = extracted
    elif isinstance(extracted, dict):
        concept_map = extracted.get("concept_map")
    else:
        concept_map = None

    if not isinstance(concept_map, list):
        raise ValueError("La respuesta de Gemini no incluyo 'concept_map' como lista.")

    return concept_map, text


def to_python_literal(value: Any) -> str:
    """Convierte estructuras Python en literal legible para el textarea."""
    return pformat(value, width=100, sort_dicts=False)


class MapEditorHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

    def log_message(self, fmt: str, *args: Any) -> None:
        # Conserva log simple, sin ruido excesivo.
        sys.stdout.write(f"[http] {self.address_string()} - {fmt % args}\n")

    def send_json(self, payload: dict[str, Any], status: int = 200) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Allow", "GET,POST,OPTIONS")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        route = urlparse.urlsplit(self.path).path
        if route == "/api/ia/status":
            key_present = bool(get_api_key())
            self.send_json(
                {
                    "ok": True,
                    "gemini_configured": key_present,
                    "message": (
                        "Gemini configurado."
                        if key_present
                        else "Falta GEMINI_API_KEY o GOOGLE_API_KEY."
                    ),
                }
            )
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        route = urlparse.urlsplit(self.path).path
        if route != "/api/ia/concept-map":
            self.send_json({"ok": False, "error": "Ruta no encontrada."}, status=404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0:
            self.send_json({"ok": False, "error": "Body vacio."}, status=400)
            return
        if length > MAX_BODY_BYTES:
            self.send_json({"ok": False, "error": "Body demasiado grande."}, status=413)
            return

        try:
            raw_body = self.rfile.read(length).decode("utf-8", errors="replace")
            payload = json.loads(raw_body)
        except json.JSONDecodeError:
            self.send_json({"ok": False, "error": "JSON invalido en la solicitud."}, status=400)
            return

        instruction = str(payload.get("instruction", "")).strip()
        concept_map_text = str(payload.get("concept_map_text", "")).strip()
        model = str(payload.get("model", "")).strip() or DEFAULT_MODEL

        if not instruction:
            self.send_json({"ok": False, "error": "La instruccion no puede estar vacia."}, status=400)
            return
        if not concept_map_text:
            self.send_json({"ok": False, "error": "concept_map_text no puede estar vacio."}, status=400)
            return

        api_key = get_api_key()
        if not api_key:
            self.send_json(
                {
                    "ok": False,
                    "error": (
                        "No se encontro GEMINI_API_KEY. Define la variable de entorno o crea "
                        "un archivo .env en 'Mapa conceptual'."
                    ),
                },
                status=503,
            )
            return

        try:
            concept_map, raw_text = call_gemini_for_concept_map(
                api_key=api_key,
                model=model,
                instruction=instruction,
                concept_map_text=concept_map_text,
            )
            concept_map_python = to_python_literal(concept_map)
        except Exception as exc:
            self.send_json({"ok": False, "error": str(exc)}, status=502)
            return

        self.send_json(
            {
                "ok": True,
                "model": model,
                "concept_map_python": concept_map_python,
                "raw_response_excerpt": raw_text[:600],
            }
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Servidor local del editor de mapa conceptual.")
    parser.add_argument("--host", default="127.0.0.1", help="Host de escucha (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Puerto (default: 8000)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), MapEditorHandler)
    print(f"Servidor iniciado en http://{args.host}:{args.port}/")
    print("Endpoint IA: POST /api/ia/concept-map")
    print("Estado IA: GET /api/ia/status")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
