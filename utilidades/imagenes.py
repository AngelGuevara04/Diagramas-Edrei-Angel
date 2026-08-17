from __future__ import annotations

import json
import html
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

try:
    from duckduckgo_search import DDGS
except Exception:  # pragma: no cover - depende del entorno local
    DDGS = None


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
)
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
NSFW_BLOCK_TERMS = {
    "porn",
    "porno",
    "xxx",
    "adult",
    "sex",
    "nude",
    "naked",
    "hentai",
    "onlyfans",
    "xvideos",
    "xnxx",
    "redtube",
    "youporn",
    "brazzers",
}


def sanitize_filename(label: str, fallback: str = "nodo") -> str:
    text = str(label or "").strip()
    if not text:
        return fallback
    text = re.sub(r'[\\/:*?"<>|]+', "-", text)
    text = re.sub(r"\s+", " ", text).strip(" .")
    return text or fallback


def _collect_labels(tree: Any) -> list[str]:
    labels: list[str] = []
    seen: set[str] = set()

    def add_label(value: Any) -> None:
        text = str(value).strip()
        if text and text not in seen:
            seen.add(text)
            labels.append(text)

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                add_label(key)
                walk(value)
            return
        if isinstance(node, (list, tuple, set)):
            for item in node:
                walk(item)
            return

    walk(tree)
    return labels


def _pick_extension(url: str, content_type: str | None) -> str:
    ctype = (content_type or "").lower()
    if "image/webp" in ctype:
        return ".webp"
    if "image/png" in ctype:
        return ".png"
    if "image/jpeg" in ctype or "image/jpg" in ctype:
        return ".jpg"

    parsed = urllib.parse.urlsplit(url)
    ext = Path(parsed.path).suffix.lower()
    return ext if ext in VALID_EXTENSIONS else ".jpg"


def _looks_like_image_bytes(data: bytes) -> bool:
    if not data or len(data) < 32:
        return False
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return True
    if data.startswith(b"\xff\xd8\xff"):
        return True
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return True
    return False


def is_valid_image_file(path: Path) -> bool:
    try:
        data = path.read_bytes()
    except OSError:
        return False
    return _looks_like_image_bytes(data)


def _search_candidates_bing(query: str) -> list[str]:
    clean_query = str(query or "").strip()
    if not clean_query:
        return []
    safe_query = (
        f"{clean_query} -porno -porn -xxx -adult -sex -nude -hentai -onlyfans"
    )
    url = "https://www.bing.com/images/search?" + urllib.parse.urlencode(
        {
            "q": safe_query,
            "form": "HDRSC2",
            "first": "1",
            "tsc": "ImageBasicHover",
            "adlt": "strict",
        }
    )
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=25) as response:
        html = response.read().decode("utf-8", errors="replace")

    candidates: list[str] = []

    patterns = [
        r'"murl":"(https?://[^"]+)"',
        r'murl&quot;:&quot;(https?://.+?)&quot;',
        r'"turl":"(https?://[^"]+)"',
        r'turl&quot;:&quot;(https?://.+?)&quot;',
        r'imgurl:&quot;(https?://.+?)&quot;',
    ]
    for pattern in patterns:
        for raw in re.findall(pattern, html):
            decoded = html_unescape_and_normalize_url(raw)
            if decoded and not _is_nsfw_candidate_url(decoded):
                candidates.append(decoded)

    # Deduplicate preserving order.
    out: list[str] = []
    seen: set[str] = set()
    for item in candidates:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def _is_nsfw_candidate_url(url: str) -> bool:
    raw = str(url or "").strip().lower()
    if not raw:
        return True
    try:
        split = urllib.parse.urlsplit(raw)
    except Exception:
        return True
    haystack = f"{split.netloc} {split.path} {split.query}"
    return any(term in haystack for term in NSFW_BLOCK_TERMS)


def _search_candidates_openverse(query: str) -> list[str]:
    endpoint = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(
        {"q": query, "page_size": 12, "license_type": "all"}
    )
    req = urllib.request.Request(endpoint, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
    except Exception:
        return []

    results = payload.get("results") if isinstance(payload, dict) else []
    if not isinstance(results, list):
        return []

    out: list[str] = []
    for item in results:
        if not isinstance(item, dict):
            continue
        candidate = item.get("url") or ""
        normalized = html_unescape_and_normalize_url(candidate)
        if normalized:
            out.append(normalized)
    return out


def _search_candidates_wikimedia(query: str) -> list[str]:
    endpoint = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": f"{query} filetype:bitmap",
            "gsrnamespace": 6,
            "gsrlimit": 12,
            "prop": "imageinfo",
            "iiprop": "url|mime",
            "iiurlwidth": 900,
        }
    )
    req = urllib.request.Request(endpoint, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
    except Exception:
        return []

    pages = payload.get("query", {}).get("pages", {}) if isinstance(payload, dict) else {}
    if not isinstance(pages, dict):
        return []

    out: list[str] = []
    for page in pages.values():
        if not isinstance(page, dict):
            continue
        infos = page.get("imageinfo") or []
        if not isinstance(infos, list) or not infos:
            continue
        info = infos[0] if isinstance(infos[0], dict) else {}
        candidate = info.get("thumburl") or info.get("url") or ""
        normalized = html_unescape_and_normalize_url(candidate)
        if normalized:
            out.append(normalized)
    return out


def _search_candidates_ddg(query: str, max_results: int = 12) -> list[str]:
    if DDGS is None:
        return []
    out: list[str] = []
    try:
        with DDGS() as ddgs:
            for item in ddgs.images(str(query or "").strip(), max_results=max(1, int(max_results))):
                if not isinstance(item, dict):
                    continue
                candidate = item.get("image") or item.get("thumbnail") or ""
                normalized = html_unescape_and_normalize_url(candidate)
                if normalized:
                    out.append(normalized)
    except Exception:
        return []
    return out


def buscar_candidatos_imagen(provider: str, query: str, max_results: int = 12) -> list[str]:
    normalized_provider = str(provider or "").strip().lower()
    q = str(query or "").strip()
    limit = max(1, int(max_results))
    if not q:
        return []

    if normalized_provider == "openverse":
        out = _search_candidates_openverse(q)
        if not out:
            out = _search_candidates_wikimedia(q)
        return out[:limit]
    if normalized_provider == "bing":
        return _search_candidates_bing(q)[:limit]
    if normalized_provider == "ddg":
        return _search_candidates_ddg(q, max_results=limit)[:limit]
    return []


def descargar_imagen_desde_url(url: str, file_stem: str, output_dir: str, prefix: str = "") -> str | None:
    stem = sanitize_filename(file_stem)
    pre = sanitize_filename(prefix, fallback="") if prefix else ""
    if pre:
        stem = f"{pre}_{stem}"
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    target_base = folder / stem
    ok = _download_image(str(url or ""), target_base)
    if not ok:
        return None
    for ext in VALID_EXTENSIONS:
        candidate = folder / f"{stem}{ext}"
        if candidate.exists():
            return candidate.name
    for candidate in folder.glob(f"{stem}.*"):
        if candidate.suffix.lower() in VALID_EXTENSIONS:
            return candidate.name
    return None


def _search_candidates_unsplash(query: str, api_key: str) -> list[str]:
    endpoint = "https://api.unsplash.com/search/photos?" + urllib.parse.urlencode(
        {"query": query, "per_page": 12, "orientation": "squarish"}
    )
    req = urllib.request.Request(
        endpoint,
        headers={
            "User-Agent": USER_AGENT,
            "Authorization": f"Client-ID {api_key}",
            "Accept-Version": "v1",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
    except Exception:
        return []

    results = payload.get("results") if isinstance(payload, dict) else []
    if not isinstance(results, list):
        return []

    out: list[str] = []
    for item in results:
        if not isinstance(item, dict):
            continue
        urls = item.get("urls")
        if not isinstance(urls, dict):
            continue
        candidate = (
            urls.get("regular")
            or urls.get("small")
            or urls.get("full")
            or urls.get("raw")
            or ""
        )
        normalized = html_unescape_and_normalize_url(candidate)
        if normalized:
            out.append(normalized)
    return out


def _search_candidates_pexels(query: str, api_key: str) -> list[str]:
    endpoint = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode(
        {"query": query, "per_page": 12, "orientation": "square"}
    )
    req = urllib.request.Request(
        endpoint,
        headers={"User-Agent": USER_AGENT, "Authorization": api_key},
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
    except Exception:
        return []

    photos = payload.get("photos") if isinstance(payload, dict) else []
    if not isinstance(photos, list):
        return []

    out: list[str] = []
    for item in photos:
        if not isinstance(item, dict):
            continue
        src = item.get("src")
        if not isinstance(src, dict):
            continue
        candidate = (
            src.get("large2x")
            or src.get("large")
            or src.get("medium")
            or src.get("original")
            or ""
        )
        normalized = html_unescape_and_normalize_url(candidate)
        if normalized:
            out.append(normalized)
    return out


def _search_candidates_pixabay(query: str, api_key: str) -> list[str]:
    endpoint = "https://pixabay.com/api/?" + urllib.parse.urlencode(
        {
            "key": api_key,
            "q": query,
            "image_type": "photo",
            "safesearch": "true",
            "per_page": 12,
        }
    )
    req = urllib.request.Request(endpoint, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
    except Exception:
        return []

    hits = payload.get("hits") if isinstance(payload, dict) else []
    if not isinstance(hits, list):
        return []

    out: list[str] = []
    for item in hits:
        if not isinstance(item, dict):
            continue
        candidate = item.get("largeImageURL") or item.get("webformatURL") or item.get("previewURL") or ""
        normalized = html_unescape_and_normalize_url(candidate)
        if normalized:
            out.append(normalized)
    return out


def html_unescape_and_normalize_url(value: str) -> str:
    decoded = html.unescape(str(value or "")).strip().replace("\\/", "/")
    if decoded.startswith("http://") or decoded.startswith("https://"):
        return sanitize_url_for_request(decoded)
    return ""


def sanitize_url_for_request(url: str) -> str:
    raw = str(url or "").strip()
    if not raw:
        return ""

    # Elimina caracteres de control que rompen urllib.
    raw = "".join(ch for ch in raw if ch >= " " and ch != "\x7f")

    split = urllib.parse.urlsplit(raw)
    if split.scheme not in {"http", "https"} or not split.netloc:
        return ""

    path = urllib.parse.quote(split.path or "", safe="/:@-._~!$&'()*+,;=%")
    query = urllib.parse.quote(split.query or "", safe="=&:@-._~!$'()*+,;/%")
    fragment = urllib.parse.quote(split.fragment or "", safe=":@-._~!$&'()*+,;=/?%")
    return urllib.parse.urlunsplit((split.scheme, split.netloc, path, query, fragment))


def _download_image(url: str, output_file: Path) -> bool:
    normalized_url = sanitize_url_for_request(url)
    if not normalized_url:
        return False

    req = urllib.request.Request(
        normalized_url,
        headers={"User-Agent": USER_AGENT, "Referer": "https://www.bing.com/"},
    )
    try:
        with urllib.request.urlopen(req, timeout=35) as response:
            data = response.read()
            content_type = response.headers.get("Content-Type")
    except (urllib.error.URLError, TimeoutError, ValueError):
        return False

    if not str(content_type or "").lower().startswith("image/"):
        return False

    if not data or len(data) < 1024:
        return False
    if not _looks_like_image_bytes(data):
        return False

    ext = _pick_extension(normalized_url, content_type)
    target = output_file.with_suffix(ext)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return True


def descargar_imagen_bing(query: str, file_stem: str, output_dir: str) -> bool:
    stem = sanitize_filename(file_stem)
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)

    candidates = _search_candidates_bing(str(query or "").strip())
    if not candidates:
        return False

    target_base = folder / stem
    for url in candidates[:12]:
        if _download_image(url, target_base):
            return True
    return False


def descargar_imagen_openverse(query: str, file_stem: str, output_dir: str) -> bool:
    stem = sanitize_filename(file_stem)
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)

    candidates = _search_candidates_openverse(str(query or "").strip())
    if not candidates:
        candidates = _search_candidates_wikimedia(str(query or "").strip())
    if not candidates:
        return False

    target_base = folder / stem
    for url in candidates[:12]:
        if _download_image(url, target_base):
            return True
    return False


def descargar_imagen_ddg(query: str, file_stem: str, output_dir: str) -> bool:
    if DDGS is None:
        return False

    stem = sanitize_filename(file_stem)
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)

    candidates = _search_candidates_ddg(str(query or "").strip(), max_results=12)
    if not candidates:
        return False

    target_base = folder / stem
    for url in candidates[:12]:
        if _download_image(url, target_base):
            return True
    return False


def descargar_imagen_unsplash(query: str, file_stem: str, output_dir: str, api_key: str) -> bool:
    if not str(api_key or "").strip():
        return False

    stem = sanitize_filename(file_stem)
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)

    candidates = _search_candidates_unsplash(str(query or "").strip(), str(api_key).strip())
    if not candidates:
        return False

    target_base = folder / stem
    for url in candidates[:12]:
        if _download_image(url, target_base):
            return True
    return False


def descargar_imagen_pexels(query: str, file_stem: str, output_dir: str, api_key: str) -> bool:
    if not str(api_key or "").strip():
        return False

    stem = sanitize_filename(file_stem)
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)

    candidates = _search_candidates_pexels(str(query or "").strip(), str(api_key).strip())
    if not candidates:
        return False

    target_base = folder / stem
    for url in candidates[:12]:
        if _download_image(url, target_base):
            return True
    return False


def descargar_imagen_pixabay(query: str, file_stem: str, output_dir: str, api_key: str) -> bool:
    if not str(api_key or "").strip():
        return False

    stem = sanitize_filename(file_stem)
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)

    candidates = _search_candidates_pixabay(str(query or "").strip(), str(api_key).strip())
    if not candidates:
        return False

    target_base = folder / stem
    for url in candidates[:12]:
        if _download_image(url, target_base):
            return True
    return False
