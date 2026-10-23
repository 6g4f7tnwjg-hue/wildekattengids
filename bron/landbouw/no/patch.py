import os
# no_merged.json + vv1 + redactie -> no_final.json
import json, copy, re, unicodedata
D = os.path.dirname(os.path.abspath(__file__)) + "/"
M = json.load(open(D + "no_merged.json", encoding="utf8"))
V1 = json.load(open(D + "vv1_resultaat.json", encoding="utf8")) if os.path.exists(D + "vv1_resultaat.json") else {"locaties": [], "zonder_katten": []}
exec(open(D + "merge.py").read().split("L=[];Z=[]")[0])   # regio()
def norm(s): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode())

# Tangen staat dubbel (zo en op): de versie van zo houden
L = [copy.deepcopy(l) for l in M["locaties"] if not (l["_bron"] == "op" and l["naam"] == "Tangen Dyrepark")]
for v in V1["locaties"]:   # vv1 levert volledige records
    v = copy.deepcopy(v); old = [i for i, l in enumerate(L) if l["naam"] == v["naam"]]
    if old: L[old[0]] = v
    else: L.append(v)
for l in L:
    l["regio"] = regio(l.get("lon"), l.get("lat")); l.pop("fylke", None); l.pop("_bron", None)
def loc(n):
    l = [x for x in L if x["naam"] == n]; assert l, n; return l[0]

# ---- redactie: weergavenaam, plaats, type, labels (dierentuin = lid van EAZA of SDF)
E = {
 "Dyreparken i Kristiansand (Kristiansand Dyrepark)": ("Dyreparken", "Kristiansand", "Dierentuin", []),
 "Bjørneparken": ("Bjørneparken", "Flå", "Dierentuin", ["seizoen"]),
 "Langedrag Naturpark": ("Langedrag Naturpark", "Tunhovd (Nore og Uvdal)", "Wildpark", ["overnachten"]),
 "Tangen Dyrepark": ("Tangen Dyrepark", "Tangen (Stange)", "Dierenpark", ["seizoen"]),
 "Polar Park": ("Polar Park", "Bardu", "Wildpark", []),
 "Park Nordica": ("Park Nordica", "Trones (Namsskogan)", "Wildpark", []),
}
for old, (nm, pl, ty, lab) in E.items():
    l = loc(old); l["naam"], l["plaats"], l["type"], l["labels"] = nm, pl, ty, lab
assert len(L) == len(E), [l["naam"] for l in L]

LAB = {
 "Amoer": ("Amoer", "Amur"), "Amoer (P. p. orientalis)": ("Amoer (P. p. orientalis)", "Amur (P. p. orientalis)"),
 "Zuidelijk (A. j. jubatus)": ("Zuidelijk (A. j. jubatus)", "Southern (A. j. jubatus)"),
 "Zuidelijk (P. l. melanochaita)": ("Zuidelijk (P. l. melanochaita)", "Southern (P. l. melanochaita)"),
 "Noordelijk (P. l. leo)": ("Noordelijk (P. l. leo)", "Northern (P. l. leo)"),
 "Noordelijk (L. l. lynx)": ("Noordelijk (L. l. lynx)", "Northern (L. l. lynx)"),
 "Karpatisch (L. l. carpathicus)": ("Karpatisch (L. l. carpathicus)", "Carpathian (L. l. carpathicus)"),
 "onbekend": ("onbekend", "unknown"), "—": None,
}
# ondersoort alleen als de bron hem noemt: lynx (eigen keuze van de vervolgagent) en leeuw (herkomst Mufasa onbekend) terug naar onbekend
for l in L:
    for k in l["katten"]:
        if k["soort"] == "Euraziatische lynx" or (k["soort"] == "Leeuw" and l["naam"] == "Dyreparken"): k["ondersoort"] = "onbekend"
for l in L:
    for k in l["katten"]:
        o = k["ondersoort"]; o = o if isinstance(o, str) else o.get("nl")
        assert o in LAB, (l["naam"], k["soort"], o)
        v = LAB[o]
        if v is None or (o == "onbekend" and k["soort"] in ("Serval",)):
            k["ondersoort"] = "—"
        else:
            k["ondersoort"] = {"nl": v[0], "en": v[1]}
        if k["status"] != "w": k["twijfel"] = None
        elif not k.get("twijfel"): k["twijfel"] = {"nl": k["toelichting"]["nl"], "en": k["toelichting"]["en"]}
    for g in l.get("geboortes", []):
        b = g["geboren"]; ap = bool(re.search(r"[a-z(]", b)) or len(b.split(" ")[0].split("-")) < 3
        g["geboren"] = b.split(" ")[0]
        if ap: g["approx"] = True
M["locaties"] = L
Z = M["zonder_katten"] + V1["zonder_katten"]
seen = set(); ZZ = []
for z in Z:
    k = norm(z["naam"])[:12]
    if k in seen or any(norm(z["naam"])[:10] in norm(l["naam"]) or norm(l["naam"])[:10] in norm(z["naam"]) for l in L): continue
    seen.add(k); ZZ.append(z)
M["zonder_katten"] = ZZ
M["checked"] = "23-10-2026"
M["route"] = ["Dyreparken", "Bjørneparken", "Tangen Dyrepark"]
json.dump(M, open(D + "no_final.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
CONF = set("gybr")
for l in sorted(L, key=lambda l: l["regio"]):
    print(l["regio"], "|", l["naam"], "|", l["type"], "|", " ".join(f'{k["soort"]}:{k["status"]}:{json.dumps(k["ondersoort"],ensure_ascii=False)[:30]}' for k in l["katten"]), "|", [g["geboren"] for g in l.get("geboortes", [])])
print(len(L), "locaties;", len([l for l in L if any(k["status"] in CONF for k in l["katten"])]), "bevestigd;", len(ZZ), "zonder")
