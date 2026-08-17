import urllib.request
import urllib.parse

url = "https://corsproxy.io/?" + urllib.parse.quote("https://duckduckgo.com/i.js?q=Tierra&o=json")
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req) as response:
        print("Response:", response.status)
        print(response.read()[:200])
except Exception as e:
    print("Error:", e)
