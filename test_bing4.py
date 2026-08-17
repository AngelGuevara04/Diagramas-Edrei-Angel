with open("bing.html", "r", encoding="utf-8") as f:
    html = f.read()
import re
murls = re.findall(r'"murl"\s*:\s*"([^"]+)"', html)
print("murls:", murls[:5])
