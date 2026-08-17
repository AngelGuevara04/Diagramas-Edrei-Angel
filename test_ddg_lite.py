import urllib.request
req = urllib.request.Request("https://lite.duckduckgo.com/lite/", data=b"q=Tierra+Marte", headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode('utf-8')[:200])
except Exception as e:
    print("Error:", e)
