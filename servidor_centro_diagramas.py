"""
Servidor central para el menu principal de Diagramas.

Funciones:
- Sirve archivos estaticos de la raiz del proyecto.
- Hace proxy de APIs hacia:
  - /api/ia/*      -> servidor de mapa conceptual
  - /api/images/*  -> servidor de mapa mental
"""

from __future__ import annotations

import argparse
import sys
from http import HTTPStatus, client
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib import parse as urlparse


PROJECT_ROOT = Path(__file__).resolve().parent


class CentroDiagramasHandler(SimpleHTTPRequestHandler):
    concept_host = "127.0.0.1"
    concept_port = 8001
    mind_host = "127.0.0.1"
    mind_port = 8002

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stdout.write(f"[centro] {self.address_string()} - {fmt % args}\n")

    def _read_body(self) -> bytes:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0:
            return b""
        return self.rfile.read(length)

    def _pick_backend(self, route: str) -> tuple[str, int] | None:
        if route.startswith("/api/ia/"):
            return self.concept_host, self.concept_port
        if route.startswith("/api/images/"):
            return self.mind_host, self.mind_port
        return None

    def _proxy_request(self) -> bool:
        split = urlparse.urlsplit(self.path)
        route = split.path
        backend = self._pick_backend(route)
        if backend is None:
            return False

        host, port = backend
        body = self._read_body()
        target_path = route
        if split.query:
            target_path = f"{target_path}?{split.query}"

        headers = {}
        for key, value in self.headers.items():
            lowered = key.lower()
            if lowered in {"host", "connection"}:
                continue
            headers[key] = value
        headers["Host"] = f"{host}:{port}"

        conn = client.HTTPConnection(host, port, timeout=90)
        try:
            conn.request(self.command, target_path, body=body, headers=headers)
            upstream = conn.getresponse()
            payload = upstream.read()
        except Exception as exc:
            self.send_response(HTTPStatus.BAD_GATEWAY)
            msg = (
                f'{{"ok": false, "error": "No se pudo conectar al backend {host}:{port}: {exc}"}}'
            ).encode("utf-8", errors="replace")
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)
            return True
        finally:
            conn.close()

        self.send_response(upstream.status, upstream.reason)
        for key, value in upstream.getheaders():
            lowered = key.lower()
            if lowered in {"connection", "transfer-encoding", "keep-alive"}:
                continue
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)
        return True

    def do_OPTIONS(self) -> None:  # noqa: N802
        if self._proxy_request():
            return
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Allow", "GET,POST,OPTIONS")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        split = urlparse.urlsplit(self.path)
        if split.path == "/":
            self.path = "/index.html"
        if self._proxy_request():
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        if self._proxy_request():
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Ruta no encontrada.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Servidor central de Diagramas.")
    parser.add_argument("--host", default="127.0.0.1", help="Host de escucha del servidor central.")
    parser.add_argument("--port", type=int, default=8000, help="Puerto del servidor central.")
    parser.add_argument("--concept-host", default="127.0.0.1", help="Host del backend conceptual.")
    parser.add_argument("--concept-port", type=int, default=8001, help="Puerto del backend conceptual.")
    parser.add_argument("--mind-host", default="127.0.0.1", help="Host del backend mental.")
    parser.add_argument("--mind-port", type=int, default=8002, help="Puerto del backend mental.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    handler_cls = type(
        "ConfiguredCentroDiagramasHandler",
        (CentroDiagramasHandler,),
        {
            "concept_host": args.concept_host,
            "concept_port": args.concept_port,
            "mind_host": args.mind_host,
            "mind_port": args.mind_port,
        },
    )
    server = ThreadingHTTPServer((args.host, args.port), handler_cls)
    print(f"Servidor central en http://{args.host}:{args.port}/")
    print(
        "Proxy APIs -> "
        f"/api/ia/* => {args.concept_host}:{args.concept_port} | "
        f"/api/images/* => {args.mind_host}:{args.mind_port}"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor central detenido.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
