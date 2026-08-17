import urllib.request
import re
url = "https://images.search.yahoo.com/search/images?p=Tierra+y+Marte+El+Sistema+Solar"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        urls = re.findall(r'imgurl=&quot;(https?://[^&]+)&quot;', html)
        print("Yahoo results:", len(urls), urls[:3])
except Exception as e:
    print("Error:", e)
