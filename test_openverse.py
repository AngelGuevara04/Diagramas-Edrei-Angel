import sys
sys.path.insert(0, ".")
from utilidades.imagenes import _search_candidates_openverse, _search_candidates_wikimedia
try:
    results = _search_candidates_openverse("Tierra y Marte El Sistema Solar")
    print("Openverse Results:", len(results), results[:2])
    results2 = _search_candidates_wikimedia("Tierra y Marte El Sistema Solar")
    print("Wikimedia Results:", len(results2), results2[:2])
except Exception as e:
    print("Error:", type(e), e)
