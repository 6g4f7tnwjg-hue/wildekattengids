# Maakt kaart.json (MAIN, ISLANDS, BUUR, LINES) voor een landgids uit GISCO NUTS 2024 (1:3 miljoen).
# Gebruik: python3 kaart_maken.py <map> <LANDCODE> <NUTS-niveau regio's 2|3> <lon0> <lat0> <lon1> <lat1> <buren,komma's> [eps]
# Voorbeeld Tsjechië: python3 kaart_maken.py cz CZ 3 11.8 48.35 19.15 51.25 DE,PL,SK,AT
# De geojson-bestanden worden in <map>/kaart/ gedownload als ze er nog niet zijn (niet committen: groot).
# Vereist shapely (pip install shapely). De projectie in gen.py: LON0=lon0, LAT0=lat1, KX=cos(midden-breedte).
import json, math, os, sys, urllib.request
from shapely.geometry import shape, box
from shapely.ops import unary_union, linemerge
d, cc, niv = sys.argv[1], sys.argv[2], sys.argv[3]
lon0, lat0, lon1, lat1 = map(float, sys.argv[4:8])
buren = sys.argv[8].split(",") if len(sys.argv) > 8 and sys.argv[8] else []
eps = float(sys.argv[9]) if len(sys.argv) > 9 else 0.006
K = os.path.join(os.path.dirname(os.path.abspath(__file__)), d, "kaart")
os.makedirs(K, exist_ok=True)
def nuts(n):
    p = os.path.join(K, f"nuts{n}.geojson")
    if not os.path.exists(p):
        urllib.request.urlretrieve(f"https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_03M_2024_4326_LEVL_{n}.geojson", p)
    return json.load(open(p))
n0 = {f["properties"]["NUTS_ID"]: shape(f["geometry"]) for f in nuts(0)["features"]}
land = n0[cc]
fr = box(lon0, lat0, lon1, lat1)
def rings(g): return [g] if g.geom_type == "Polygon" else list(g.geoms)
def pts(p): return [[round(x, 2), round(y, 2)] for x, y in p.exterior.coords]
ps = sorted(rings(land.simplify(eps)), key=lambda p: -p.area)
MAIN = pts(ps[0]); ISL = [pts(p) for p in ps[1:] if p.area > 0.003]
BUUR = []
for b in buren:
    g = n0[b].intersection(fr).simplify(eps)
    if g.is_empty: continue
    BUUR += [pts(p) for p in rings(g) if p.area > 0.002]
R = [shape(f["geometry"]) for f in nuts(int(niv))["features"]
     if f["properties"]["NUTS_ID"].startswith(cc) and len(f["properties"]["NUTS_ID"]) == 2 + int(niv)]
inner = unary_union([r.boundary for r in R]).difference(land.boundary.buffer(0.004))
inner = linemerge(inner) if inner.geom_type != "LineString" else inner
inner = inner.simplify(eps)
LINES = [[[round(x, 2), round(y, 2)] for x, y in g.coords] for g in (inner.geoms if hasattr(inner, "geoms") else [inner]) if g.length > 0.02]
json.dump({"MAIN": MAIN, "ISLANDS": ISL, "BUUR": BUUR, "LINES": LINES}, open(os.path.join(K, "kaart.json"), "w"))
KX = math.cos(math.radians((lat0 + lat1) / 2))
print(f"kaart.json: MAIN {len(MAIN)} punten, {len(ISL)} eilanden, {len(BUUR)} buren, {len(LINES)} grenslijnen; in gen.py: LON0={lon0}, LAT0={lat1}, KX={KX:.4f}, W=PX({lon1},0), H=PX(0,{lat0})")
