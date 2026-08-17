import sys
sys.path.insert(0, ".")
from utilidades.imagenes import _search_candidates_bing
try:
    results = _search_candidates_bing("Tierra y Marte El Sistema Solar")
    print("Bing Results:", len(results), results[:2])
except Exception as e:
    print("Error:", type(e), e)
