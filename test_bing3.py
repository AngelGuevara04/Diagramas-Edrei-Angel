import re
with open("bing.html", "r", encoding="utf-8") as f:
    html = f.read()
matches = re.findall(r'src="([^"]+)"', html)
matches2 = re.findall(r'src2="([^"]+)"', html)
print("src matches:", [m for m in matches if 'http' in m][:5])
print("src2 matches:", [m for m in matches2 if 'http' in m][:5])
