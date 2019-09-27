import re

fin = open("cube.wrl", "rt")
content = fin.read()

m = re.search("point\s+\[([^\]]+)", str)
points = re.split("[\s,]+",m.group(1).strip())
print("points = ", len(points))

m = re.search("coordIndex\s+\[([^\]]+)", str)
coords = re.split("[\s,]+",m.group(1).strip())
print("coords = ", len(coords))

fin.close()
