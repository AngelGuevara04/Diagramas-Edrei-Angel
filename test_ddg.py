from duckduckgo_search import DDGS

try:
    with DDGS() as ddgs:
        results = list(ddgs.images("Tierra y Marte El Sistema Solar", max_results=2))
        print("Results:", results)
except Exception as e:
    print("Error:", type(e), e)
