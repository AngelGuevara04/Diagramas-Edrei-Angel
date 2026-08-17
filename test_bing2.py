import sys
import urllib.request
import urllib.parse
sys.path.insert(0, ".")
url = "https://www.bing.com/images/search?q=Tierra+y+Marte+El+Sistema+Solar&form=HDRSC2&first=1&tsc=ImageBasicHover&adlt=strict"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
with urllib.request.urlopen(req, timeout=25) as response:
    html = response.read().decode("utf-8", errors="replace")
print("HTML snippet:", html[5000:6000])
with open("bing.html", "w", encoding="utf-8") as f:
    f.write(html)
