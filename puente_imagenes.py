import sys
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

# Import search functions from local utilidades
try:
    from utilidades.imagenes import _search_candidates_ddg, _search_candidates_bing
except ImportError:
    print("Error: No se pudo importar utilidades.imagenes.")
    print("Asegurate de estar ejecutando este script desde la carpeta raiz del proyecto.")
    sys.exit(1)

class PuenteHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlsplit(self.path)
        if parsed.path == "/api/search":
            query = urllib.parse.parse_qs(parsed.query).get("q", [""])[0]
            provider = urllib.parse.parse_qs(parsed.query).get("provider", ["ddg"])[0]
            
            try:
                if provider == "bing":
                    results = _search_candidates_bing(query)
                else:
                    results = _search_candidates_ddg(query)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": True, "results": results}).encode())
                print(f"[{provider.upper()}] Busqueda: '{query}' -> {len(results)} resultados")
            except Exception as e:
                self.send_response(500)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode())
                print(f"[{provider.upper()}] Error en '{query}': {e}")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Desactivar el log por defecto para no saturar la consola
        pass

if __name__ == "__main__":
    port = 8765
    try:
        server = HTTPServer(("localhost", port), PuenteHandler)
        print("=========================================================")
        print("                 PUENTE LOCAL ACTIVO                     ")
        print("=========================================================")
        print(f"[*] Escuchando en http://localhost:{port}")
        print("[*] Manten esta ventana negra ABIERTA mientras usas el")
        print("    editor de mapas mentales en tu navegador (Render).")
        print("[*] Usa 'Ctrl + C' para cerrar este puente.")
        print("=========================================================\n")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nPuente Local cerrado.")
    except Exception as e:
        print(f"\nError al iniciar el Puente Local: {e}")
