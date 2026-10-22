# Eenmalig: Zweden op de Europakaart van start.html (D.se.poly, kader, buurlanden Noorwegen/Finland)
import json, re, os
from shapely.geometry import shape, box
B = os.path.dirname(os.path.abspath(__file__)) + "/../../../"
n0 = {f["properties"]["NUTS_ID"]: shape(f["geometry"]) for f in json.load(open(B + "landbouw/se/kaart/nuts0.geojson"))["features"]}
def rings(g): return [g] if g.geom_type == "Polygon" else list(g.geoms)
se = sorted(rings(n0["SE"].simplify(0.03)), key=lambda p: -p.area)
poly = [[[round(x, 2), round(y, 2)] for x, y in p.exterior.coords] for p in se if p.area > 0.02]
print("se poly", len(poly), sum(map(len, poly)))
LAT_NEW = 69.4; DY = (LAT_NEW - 59.0) * 60
K = 0.623 * 60; S = 60; LON0 = -10.75
P = lambda lo, la: ((lo - LON0) * K + 10, (LAT_NEW - la) * S + 10)
W = round(P(25.6, 0)[0]); H = 1420 + round(DY)
fr = box(-11, 30, 25.7, 70.5)
nb = ""
for c in ["NO", "FI"]:
    for p in rings(n0[c].intersection(fr).simplify(0.03)):
        if p.area < 0.05: continue
        nb += "M" + "L".join(f"{P(x,y)[0]:.0f},{P(x,y)[1]:.0f}" for x, y in p.exterior.coords[:-1]) + "Z"
s = open(B + "start.html", encoding="utf8").read()
m = re.search(r"const D=(\{.*?\});\n", s); D = json.loads(m.group(1))
D["se"] = {"counts": [0, 0], "locs": [], "poly": poly, "water": [], "young": [], "lt": []}
s = s[:m.start(1)] + json.dumps(D, ensure_ascii=False, separators=(",", ":")) + s[m.end(1):]
# oude buurlanden (in de oude projectie) omlaag schuiven, nieuwe erbij
s = s.replace('let h=`<path class="nb" d="${NBR}"/>`;', 'let h=`<path class="nb" d="${NBR}" transform="translate(0,%d)"/><path class="nb" d="${NBR2}"/>`;' % round(DY), 1)
s = s.replace('let m=`<path class="nb" d="${NBR}"/>`;', 'let m=`<path class="nb" d="${NBR}" transform="translate(0,%d)"/><path class="nb" d="${NBR2}"/>`;' % round(DY), 1)
s = s.replace("/* plek van de landnaam: midden van de grootste vorm */", 'const NBR2="%s";\n/* plek van de landnaam: midden van de grootste vorm */' % nb, 1)
s = s.replace("const K=0.623*60, S=60, LON0=-10.75, LAT0=59.0;", "const K=0.623*60, S=60, LON0=-10.75, LAT0=%s;" % LAT_NEW, 1)
s = s.replace("const FULL=[0,0,1140,1420]", "const FULL=[0,0,%d,%d]" % (W, H), 1)
s = s.replace('<svg id="map" class="map" viewBox="0 0 1140 1420"', '<svg id="map" class="map" viewBox="0 0 %d %d"' % (W, H), 1)
open(B + "start.html", "w", encoding="utf8").write(s)
print("FULL", W, H, "DY", DY, "NBR2", len(nb))
