"""
Servidor local para el editor de cuadro sinoptico.

Incluye:
- Servido de archivos estaticos del proyecto "Cuadro sinoptico".
"""

from __future__ import annotations

import argparse
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent


class SynopticEditorHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stdout.write(f"[http] {self.address_string()} - {fmt % args}\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Servidor local del editor de cuadro sinoptico.")
    parser.add_argument("--host", default="127.0.0.1", help="Host de escucha (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8003, help="Puerto (default: 8003)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), SynopticEditorHandler)
    print(f"Servidor iniciado en http://{args.host}:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
