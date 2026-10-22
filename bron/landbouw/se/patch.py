import os
# se_merged.json + vv1 + redactie -> se_final.json
import json, copy, re, unicodedata
D = os.path.dirname(os.path.abspath(__file__)) + "/"
M = json.load(open(D + "se_merged.json", encoding="utf8"))
V1 = json.load(open(D + "vv1_resultaat.json", encoding="utf8"))
exec(open(D + "merge.py").read().split("L=[];Z=[]")[0])   # regio()
def norm(s): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode())

# vv1 levert volledige records voor tien locaties; Ystad uit het onderzoek van Zuid-Zweden
L = [copy.deepcopy(v) for v in V1["locaties"]]
L += [copy.deepcopy(l) for l in M["locaties"] if l["naam"] == "Ystad Djurpark" and l["_bron"] == "sy"]
for l in L:
    l["regio"] = regio(l.get("lon"), l.get("lat")); l.pop("lan", None); l.pop("_bron", None)
def loc(n):
    l = [x for x in L if x["naam"] == n]; assert l, n; return l[0]

# ---- redactie per locatie: weergavenaam, plaats, type, labels
# Dierentuin = lid van EAZA of de Svenska Djurparksföreningen (SDF)
E = {
 "Kolmårdens Djurpark": ("Kolmårdens Djurpark", "Kolmården (Norrköping)", "Dierentuin", ["seizoen"]),
 "Parken Zoo": ("Parken Zoo", "Eskilstuna", "Dierentuin", ["seizoen"]),
 "Nordens Ark": ("Nordens Ark", "Hunnebostrand (Sotenäs)", "Dierentuin", ["seizoen"]),
 "Borås Djurpark": ("Borås Djurpark", "Borås", "Dierentuin", ["seizoen"]),
 "Skånes Djurpark": ("Skånes Djurpark", "Höör", "Dierentuin", ["seizoen"]),
 "Ystad Djurpark": ("Ystad Djurpark", "Skårby (Ystad)", "Dierentuin", ["seizoen"]),
 "Ölands Djur- och Nöjespark": ("Ölands Djurpark", "Färjestaden (Öland)", "Dierentuin", ["seizoen"]),
 "Skansen": ("Skansen", "Stockholm (Djurgården)", "Dierentuin", []),
 "Vildriket (voorheen Järvzoo)": ("Vildriket", "Järvsö (Ljusdal)", "Dierentuin", []),
 "Lycksele Djurpark": ("Lycksele Djurpark", "Lycksele", "Dierentuin", ["seizoen"]),
 "Junsele Djurpark": ("Junsele Djurpark", "Junsele (Sollefteå)", "Dierenpark", ["seizoen"]),
}
for old, (nm, pl, ty, lab) in E.items():
    l = loc(old); l["naam"], l["plaats"], l["type"], l["labels"] = nm, pl, ty, lab
assert len(L) == len(E)

# ---- ondersoort-labels in vaste vorm
LAB = {
 "Amoer": ("Amoer", "Amur"), "Sumatraans": ("Sumatraans", "Sumatran"),
 "onbekend, incl. witte tijger": ("onbekend, incl. witte tijger", "unknown, incl. white tiger"),
 "Aziatisch (P. l. leo, voorheen P. l. persica)": ("Aziatisch (P. l. leo, voorheen P. l. persica)", "Asiatic (P. l. leo, formerly P. l. persica)"),
 "Amoer (P. p. orientalis)": ("Amoer (P. p. orientalis)", "Amur (P. p. orientalis)"),
 "Perzisch": ("Perzisch", "Persian"),
 "Zuidelijk (A. j. jubatus)": ("Zuidelijk (A. j. jubatus)", "Southern (A. j. jubatus)"),
 "Karpatisch (L. l. carpathicus)": ("Karpatisch (L. l. carpathicus)", "Carpathian (L. l. carpathicus)"),
 "Noordelijk (L. l. lynx)": ("Noordelijk (L. l. lynx)", "Northern (L. l. lynx)"),
 "F. s. silvestris (fokdieren voor Schotland)": None,
 "onbekend": ("onbekend", "unknown"), "—": None,
}
for l in L:
    for k in l["katten"]:
        if k["soort"] == "Manoel (Pallas’ kat)": k["soort"] = "Manoel"
        o = k["ondersoort"]; o = o if isinstance(o, str) else o.get("nl")
        assert o in LAB, (l["naam"], k["soort"], o)
        v = LAB[o]
        if v is None or (o == "onbekend" and k["soort"] in ("Serval", "Jaguar", "Manoel", "Vissende kat", "Sneeuwluipaard", "Europese wilde kat")):
            k["ondersoort"] = "—"
        else:
            k["ondersoort"] = {"nl": v[0], "en": v[1]}
        if k["status"] != "w": k["twijfel"] = None
        elif not k.get("twijfel"): k["twijfel"] = {"nl": k["toelichting"]["nl"], "en": k["toelichting"]["en"]}
    for g in l.get("geboortes", []):
        b = g["geboren"]; ap = bool(re.search(r"[a-z(]", b)) or len(b.split(" ")[0].split("-")) < 3
        b = b.split(" ")[0]
        if b == "2025": b = "2025-04"   # Kolmården, Lava en Azka: voorjaar 2025
        g["geboren"] = b
        if ap: g["approx"] = True
M["locaties"] = L
# geen katten: alles samen (zonder dubbelingen en zonder locaties met katten)
Z = M["zonder_katten"] + V1["zonder_katten"]
seen = set(); ZZ = []
for z in Z:
    k = norm(z["naam"])[:12]
    if k in seen or any(norm(z["naam"])[:10] in norm(l["naam"]) or norm(l["naam"])[:10] in norm(z["naam"]) for l in L): continue
    seen.add(k); ZZ.append(z)
M["zonder_katten"] = ZZ
M["checked"] = "22-10-2026"
M["route"] = ["Parken Zoo", "Nordens Ark", "Skånes Djurpark", "Ystad Djurpark"]
json.dump(M, open(D + "se_final.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
CONF = set("gybr")
for l in sorted(L, key=lambda l: l["regio"]):
    print(l["regio"], "|", l["naam"], "|", l["type"], "|", " ".join(f'{k["soort"]}:{k["status"]}' for k in l["katten"]), "|", [g["geboren"] for g in l.get("geboortes", [])])
print(len(L), "locaties;", len([l for l in L if any(k["status"] in CONF for k in l["katten"])]), "bevestigd;", len(ZZ), "zonder")
for z in ZZ: print("  -", z["naam"], "|", z.get("plaats"))
