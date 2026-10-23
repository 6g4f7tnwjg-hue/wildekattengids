# Eenmalig: Noorwegen op de Europakaart van start.html (D.no.poly, kader naar 71,4° N en 31,7° O, Finland grijs in NBR2)
import json, re, os
from shapely.geometry import shape, box
B = os.path.dirname(os.path.abspath(__file__)) + "/../../../"
n0 = {f["properties"]["NUTS_ID"]: shape(f["geometry"]) for f in json.load(open(B + "landbouw/no/kaart/nuts0.geojson"))["features"]}
def rings(g): return [g] if g.geom_type == "Polygon" else list(g.geoms)
no = n0["NO"].intersection(box(3, 57, 32, 71.5))   # zonder Svalbard en Jan Mayen
ps = sorted(rings(no.simplify(0.04)), key=lambda p: -p.area)
poly = [[[round(x, 2), round(y, 2)] for x, y in p.exterior.coords] for p in ps if p.area > 0.03]
print("no poly", len(poly), sum(map(len, poly)))
LAT_OUD, LAT_NEW = 69.4, 71.4; DY = (LAT_NEW - 59.0) * 60
K = 0.623 * 60; S = 60; LON0 = -10.75
P = lambda lo, la: ((lo - LON0) * K + 10, (LAT_NEW - la) * S + 10)
W = round(P(31.7, 0)[0]); H = 1420 + round(DY)
nb = ""
for p in rings(n0["FI"].intersection(box(-11, 30, 31.7, 71.5)).simplify(0.03)):
    if p.area < 0.05: continue
    nb += "M" + "L".join(f"{P(x,y)[0]:.0f},{P(x,y)[1]:.0f}" for x, y in p.exterior.coords[:-1]) + "Z"
s = open(B + "start.html", encoding="utf8").read()
m = re.search(r"const D=(\{.*?\});\n", s); D = json.loads(m.group(1))
D["no"] = {"counts": [0, 0], "locs": [], "poly": poly, "water": [], "young": [], "lt": []}
s = s[:m.start(1)] + json.dumps(D, ensure_ascii=False, separators=(",", ":")) + s[m.end(1):]
assert s.count('transform="translate(0,624)"') == 2
s = s.replace('transform="translate(0,624)"', 'transform="translate(0,%d)"' % round(DY))
s = re.sub(r'const NBR2="[^"]*";', 'const NBR2="%s";' % nb, s, count=1)
a = "LON0=-10.75, LAT0=%s;" % LAT_OUD; assert a in s; s = s.replace(a, "LON0=-10.75, LAT0=%s;" % LAT_NEW)
s, n1 = re.subn(r"const FULL=\[0,0,\d+,\d+\]", "const FULL=[0,0,%d,%d]" % (W, H), s)
s, n2 = re.subn(r'<svg id="map" class="map" viewBox="0 0 \d+ \d+"', '<svg id="map" class="map" viewBox="0 0 %d %d"' % (W, H), s)
assert n1 == n2 == 1
open(B + "start.html", "w", encoding="utf8").write(s)
print("FULL", W, H, "DY", DY)
