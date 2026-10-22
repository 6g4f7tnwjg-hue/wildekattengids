import os
# cz_merged.json + vv1/vv2 + redactie -> cz_final.json
import json, copy, re, unicodedata
D = os.path.dirname(os.path.abspath(__file__)) + "/"
M = json.load(open(D + "cz_merged.json", encoding="utf8"))
V1 = json.load(open(D + "vv1_resultaat.json", encoding="utf8"))
V2 = json.load(open(D + "vv2_resultaat.json", encoding="utf8"))
exec(open(D + "merge.py").read().split("L=[];Z=[]")[0])   # regio()
def norm(s): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode())

L = M["locaties"]
# dubbelingen: Doksy en Ringelland (vv2 levert de volledige versie)
L = [l for l in L if not (l["_bron"] == "op" and l["naam"] in ("Doksyland – Zoopark Doksy", "Ringelland"))]
L = [l for l in L if l["naam"] not in ("Cirkus Šimek", "Cirkus Humberto (familie Navrátil)")]
byn = {norm(l["naam"]): l for l in L}
def find(n):
    k = norm(n)
    if k in byn: return byn[k]
    for kk, l in byn.items():
        if k[:10] in kk or kk[:10] in k: return l
    return None
# vv2: volledige records
for v in V2["locaties"]:
    v = copy.deepcopy(v); v["regio"] = regio(v.get("lon"), v.get("lat")); v.pop("kraj", None)
    old = find(v["naam"])
    if old and old in L:
        for f in ("uren", "about", "earlier", "url"):
            if not (v.get(f) or ({} if f != "url" else "")) and old.get(f): v[f] = old[f]
        L[L.index(old)] = v
    else:
        L.append(v)
    byn = {norm(l["naam"]): l for l in L}
# vv1: per soort
for v in V1["locaties"]:
    old = find(v["naam"])
    if old is None or (v.get("lon") and v.get("type")):
        v = copy.deepcopy(v); v["regio"] = regio(v.get("lon"), v.get("lat")); v.pop("kraj", None)
        if old: L[L.index(old)] = v
        else: L.append(v)
        byn = {norm(l["naam"]): l for l in L}; continue
    ks = old["katten"]
    for k in v["katten"]:
        sub = lambda x: x["ondersoort"] if isinstance(x["ondersoort"], str) else x["ondersoort"].get("nl")
        same = [x for x in ks if x["soort"] == k["soort"] and (sub(x) == sub(k) or len([y for y in ks if y["soort"] == k["soort"]]) == 1)]
        if same: ks[ks.index(same[0])] = k
        else: ks.append(k)
    if v.get("geboortes"): old["geboortes"] = (old.get("geboortes") or []) + [g for g in v["geboortes"] if g["soort"] not in [x["soort"] for x in old.get("geboortes", [])]]
def loc(n):
    l = find(n); assert l, n; return l
def drop(n, soort, sub=None):
    l = loc(n); l["katten"] = [k for k in l["katten"] if not (k["soort"] == soort and (sub is None or sub in json.dumps(k["ondersoort"], ensure_ascii=False)))]
def add_earlier(n, nl, en):
    l = loc(n); e = l.get("earlier") or {"nl": "", "en": ""}
    l["earlier"] = {"nl": (e.get("nl", "") + " " + nl).strip(), "en": (e.get("en", "") + " " + en).strip()}
drop("Zoo Brno", "Luipaard"); drop("Zoo Brno", "Vissende kat")
add_earlier("Zoo Brno", "Sri Lanka-luipaard en vissende kat: in 2025 vertrokken (jaarverslag 2025: 0 op 31-12-2025).", "Sri Lankan leopard and fishing cat: left in 2025 (annual report 2025: none on 31-12-2025).")
drop("Zoopark Olovnice", "Rode lynx"); drop("Zoopark Olovnice", "Euraziatische lynx")
add_earlier("Zoopark Olovnice", "Rode lynx (laatst gezien 05/2023) en Euraziatische lynx (Zootierliste).", "Bobcat (last seen 05/2023) and Eurasian lynx (Zootierliste).")
drop("Kočkovité šelmy Chvojenec", "Serval")
# Family Park Česká Skalice: alleen onzekere caracal (serval laatst 06/2024 -> eerder)
fp = loc("Family Park Česká Skalice")
fp.update({"naam": "Family Park Česká Skalice", "plaats": "Česká Skalice", "lon": 16.043, "lat": 50.395, "type": "Dierenpark", "url": "",
           "uren": {"nl": "Onbekend; geen eigen website gevonden (gezien 22-10-2026).", "en": "Unknown; no website of its own found (seen 22-10-2026)."},
           "about": {"nl": "Kleine familiedierentuin (vroeger Zoopark Česká Skalice). Het oude domein verwijst naar spam; nieuws uit 2025 noemt geen katten.", "en": "Small family zoo (formerly Zoopark Česká Skalice). The old domain redirects to spam; 2025 news mentions no cats."},
           "earlier": {"nl": "Serval: volgens Zootierliste sinds 2024 (bord gezien 06/2024); niets nieuwers gevonden.", "en": "Serval: according to Zootierliste since 2024 (sign seen 06/2024); nothing newer found."}})
fp["katten"] = [k for k in fp["katten"] if k["soort"] == "Caracal"]
fp["regio"] = regio(fp["lon"], fp["lat"])

# ---- redactie per locatie: weergavenaam, plaats, type, labels
E = {
 "Zoo Praha": ("Zoo Praha", "Praha (Troja)", "Dierentuin", []),
 "Zookoutek Malá Chuchle": ("Zookoutek Malá Chuchle", "Praha (Malá Chuchle)", "Opvang of sanctuary", []),
 "ZOO Chleby": ("Zoo Chleby", "Chleby (Nymburk)", "Dierentuin", []),
 "Zoopark Zájezd": ("Zoopark Zájezd", "Zájezd (Buštěhrad)", "Dierenpark", []),
 "Rekreační park Karlštejn (Zoopark Karlštejn)": ("Rekreační park Karlštejn", "Karlštejn", "Particuliere houder", ["seizoen"]),
 "Zoopark Olovnice": ("Zoopark Olovnice", "Olovnice (Mělník)", "Dierenpark", []),
 "Ringelland": ("Ringelland", "Habrkovice (Kutná Hora)", "Particuliere houder", []),
 "Statek U Merlina": ("Statek U Merlina", "Chyňava (Beroun)", "Dierenpark", []),
 "ParaZOO Vlašim (ČSOP Vlašim)": ("ParaZOO Vlašim", "Vlašim", "Opvang of sanctuary", []),
 "Zoologická a botanická zahrada města Plzně (Zoo Plzeň)": ("Zoo Plzeň", "Plzeň", "Dierentuin", []),
 "Jihočeská zoologická zahrada Hluboká nad Vltavou (Zoo Hluboká)": ("Zoo Hluboká", "Hluboká nad Vltavou", "Dierentuin", []),
 "Zoologická zahrada Tábor (ZOO Tábor)": ("Zoo Tábor", "Tábor (Větrovy)", "Dierenpark", []),
 "ZOO Dvorec": ("Zoo Dvorec", "Dvorec (Borovany)", "Dierenpark", []),
 "Zoo Na Hrádečku": ("Zoo Na Hrádečku", "Horní Pěna (Jindřichův Hradec)", "Dierentuin", []),
 "Zoo Plasy (ZOO & Fantasy Golf Plasy)": ("Zoo Plasy", "Plasy (Plzeň-sever)", "Dierenpark", []),
 "Návštěvnické centrum Kvilda (NP Šumava) – rysí výběh": ("Lynxverblijf Kvilda (NP Šumava)", "Kvilda", "Natuur- en fokcentrum", []),
 "Království lesa (Lipno)": ("Království lesa", "Lipno nad Vltavou", "Attractiepark met dieren", []),
 "Zoo Liberec": ("Zoo Liberec", "Liberec", "Dierentuin", []),
 "Zoologická zahrada Ústí nad Labem": ("Zoo Ústí nad Labem", "Ústí nad Labem", "Dierentuin", []),
 "Zoologická zahrada Děčín – Pastýřská stěna": ("Zoo Děčín", "Děčín", "Dierentuin", []),
 "Zoopark Chomutov": ("Zoopark Chomutov", "Chomutov", "Dierentuin", []),
 "Safari Park Dvůr Králové": ("Safari Park Dvůr Králové", "Dvůr Králové nad Labem", "Safaripark", []),
 "Zoopark Doksy (Doksyland)": ("Zoopark Doksy (Doksyland)", "Doksy (Česká Lípa)", "Particuliere houder", ["seizoen"]),
 "Kočkovité šelmy Chvojenec (Kočkovité šelmy z. ú.)": ("Kočkovité šelmy Chvojenec", "Chvojenec (Pardubice)", "Particuliere houder", ["rondleiding"]),
 "Zoopark Stěžery": ("Zoopark Stěžery", "Stěžery (Hradec Králové)", "Dierenpark", []),
 "Zoo Brno": ("Zoo Brno", "Brno (Bystrc)", "Dierentuin", []),
 "Zoo Hodonín": ("Zoo Hodonín", "Hodonín", "Dierentuin", []),
 "Zoo Zlín": ("Zoo Zlín", "Zlín (Lešná)", "Dierentuin", []),
 "Zoo Jihlava": ("Zoo Jihlava", "Jihlava", "Dierentuin", []),
 "Stanice Pavlov (záchranná stanice)": ("Stanice Pavlov", "Pavlov (Ledeč nad Sázavou)", "Opvang of sanctuary", []),
 "ZOO Sedlec (Faunapark Sedlec)": ("Zoo Sedlec", "Sedlec (Mikulov)", "Dierenpark", []),
 "Rodinný zookoutek Nová Říše": ("Zookoutek Nová Říše", "Vápovice (Nová Říše)", "Dierenpark", []),
 "Zoologická zahrada a botanický park Ostrava": ("Zoo Ostrava", "Ostrava", "Dierentuin", []),
 "Zoologická zahrada Olomouc – Svatý Kopeček": ("Zoo Olomouc", "Olomouc (Svatý Kopeček)", "Dierentuin", []),
 "ZOO Faunapark Horní Lipová": ("Faunapark Horní Lipová", "Lipová-lázně (Horní Lipová)", "Dierenpark", []),
 "Exotika na ranči Bítovany": ("Exotika na ranči", "Bítovany (Chrudim)", "Particuliere houder", []),
 "Zoopark Zvole": ("Zoopark Zvole", "Zvole (Praha-západ)", "Particuliere houder", []),
 "Particuliere houderij Kletečná (Váňa)": ("Particuliere houder Kletečná", "Kletečná (Humpolec)", "Particuliere houder", []),
 "Animal Park Rabina (voorheen Biopark Štít)": ("Animal Park Rabina", "Klamoš (Hradec Králové)", "Particuliere houder", []),
 "Othello Park": ("Othello Park", "Žáravice (Pardubice)", "Particuliere houder", ["nietdagelijks"]),
 "Family Park Česká Skalice": ("Family Park Česká Skalice", "Česká Skalice", "Dierenpark", []),
 "Cirkus Humberto": ("Cirkus Humberto", "–", "Particuliere houder", ["reistrond"]),
 "Cirkus Bob Navarro King (Cirkus KING)": ("Cirkus Bob Navarro King", "–", "Particuliere houder", ["reistrond"]),
 "Cirkus Šimek": ("Cirkus Šimek", "–", "Particuliere houder", ["reistrond"]),
}
for old, (nm, pl, ty, lab) in E.items():
    l = loc(old); l["naam"], l["plaats"], l["type"], l["labels"] = nm, pl, ty, lab
for l in L:
    assert l["naam"] in [v[0] for v in E.values()], ("niet geredigeerd:", l["naam"])
    if l["plaats"] == "–": l["lon"] = l["lat"] = None; l["regio"] = "circus"

# ---- ondersoort-labels in vaste vorm
LAB = {
 "Amoer": ("Amoer", "Amur"), "Sumatraans": ("Sumatraans", "Sumatran"), "Bengaals": ("Bengaals", "Bengal"),
 "Bengaals, incl. witte tijger": ("Bengaals, incl. witte tijger", "Bengal, incl. white tiger"),
 "Maleis (P. t. jacksoni)": ("Maleis (P. t. jacksoni)", "Malayan (P. t. jacksoni)"),
 "onbekend (witte tijgers)": ("onbekend, incl. witte tijger", "unknown, incl. white tiger"),
 "onbekend (als 'tygr indický' aangeduid; incl. witte tijgers)": ("Bengaals (volgens de houder), incl. witte tijger", "Bengal (according to the keeper), incl. white tiger"),
 "Aziatisch (P. l. leo, voorheen P. l. persica)": ("Aziatisch (P. l. leo, voorheen P. l. persica)", "Asiatic (P. l. leo, formerly P. l. persica)"),
 "Noordelijk (P. l. leo)": ("Noordelijk (P. l. leo)", "Northern (P. l. leo)"),
 "Zuidelijk (P. l. melanochaita)": ("Zuidelijk (P. l. melanochaita)", "Southern (P. l. melanochaita)"),
 "Zuidelijk (P. l. melanochaita), incl. witte leeuw": ("Zuidelijk (P. l. melanochaita), incl. witte leeuw", "Southern (P. l. melanochaita), incl. white lion"),
 "Zuidelijk (P. l. melanochaita), wit": ("Zuidelijk (P. l. melanochaita), wit", "Southern (P. l. melanochaita), white"),
 "onbekend, incl. witte leeuw": ("onbekend, incl. witte leeuw", "unknown, incl. white lion"), "wit": ("wit", "white"),
 "Amoer (P. p. orientalis)": ("Amoer (P. p. orientalis)", "Amur (P. p. orientalis)"),
 "Noord-Chinees (P. p. japonensis)": ("Noord-Chinees (P. p. orientalis, voorheen P. p. japonensis)", "North Chinese (P. p. orientalis, formerly P. p. japonensis)"),
 "Perzisch": ("Perzisch", "Persian"), "Sri Lanka (P. p. kotiya)": ("Sri Lanka (P. p. kotiya)", "Sri Lankan (P. p. kotiya)"),
 "incl. zwarte panter": ("onbekend, incl. zwarte panter", "unknown, incl. black panther"),
 "onbekend, incl. zwarte panter": ("onbekend, incl. zwarte panter", "unknown, incl. black panther"),
 "Soedanees (A. j. soemmeringii)": ("Soedanees (A. j. soemmeringii)", "Sudan (A. j. soemmeringii)"),
 "Zuidelijk (A. j. jubatus)": ("Zuidelijk (A. j. jubatus)", "Southern (A. j. jubatus)"),
 "Karpatisch (L. l. carpathicus)": ("Karpatisch (L. l. carpathicus)", "Carpathian (L. l. carpathicus)"),
 "onbekend, incl. Karpatisch (L. l. carpathicus)": ("onbekend, incl. Karpatisch (L. l. carpathicus)", "unknown, incl. Carpathian (L. l. carpathicus)"),
 "Amoer (P. b. euptilura)": ("Amoer (P. b. euptilura)", "Amur (P. b. euptilura)"),
 "Sri Lanka (P. r. phillipsi)": ("Sri Lanka (P. r. phillipsi)", "Sri Lankan (P. r. phillipsi)"),
 "Gordons wilde kat (F. l. gordoni)": ("Gordons wilde kat (F. l. gordoni)", "Gordon’s wildcat (F. l. gordoni)"),
 "F. m. harrisoni": ("Arabisch (F. m. harrisoni)", "Arabian (F. m. harrisoni)"),
 "onbekend": ("onbekend", "unknown"), "—": None,
}
for l in L:
    for k in l["katten"]:
        if k["soort"] == "Manoel (Pallas’ kat)": k["soort"] = "Manoel"
        o = k["ondersoort"]; o = o if isinstance(o, str) else o.get("nl")
        if k["soort"] == "Bengaalse kat" and "Palawan" in o or k["soort"] == "Soendanese luipaardkat":
            k["soort"] = "Soendanese luipaardkat"; k["ondersoort"] = {"nl": "Palawan (P. j. sumatranus)", "en": "Palawan (P. j. sumatranus)"}; continue
        assert o in LAB, (l["naam"], k["soort"], o)
        v = LAB[o]
        if v is None or (o == "onbekend" and k["soort"] in ("Serval", "Caracal", "Poema", "Margay", "Moeraskat", "Jaguar", "Rode lynx", "Manoel", "Ocelot", "Jaguarundi", "Vissende kat", "Geoffroy’s kat", "Sneeuwluipaard", "Canadese lynx")):
            k["ondersoort"] = "—"
        else:
            k["ondersoort"] = {"nl": v[0], "en": v[1]}
        if k["status"] != "w": k["twijfel"] = None
        elif not k.get("twijfel"): k["twijfel"] = {"nl": k["toelichting"]["nl"], "en": k["toelichting"]["en"]}
    l.setdefault("labels", [])
    for g in l.get("geboortes", []):
        b = g["geboren"]; ap = bool(re.search(r"[a-z(]", b)) or len(b.split(" ")[0].split("-")) < 3
        b = b.split(" ")[0]
        if b == "2026": b = "2026-06"   # Jihlava caracal: vóór 20-07-2026
        if l["naam"] == "Zoo Olomouc" and g["soort"] == "Geoffroy’s kat": b = "2026-07"
        g["geboren"] = b
        if ap: g["approx"] = True
M["locaties"] = L
# geen katten: alles samen
Z = M["zonder_katten"] + V1["zonder_katten"] + V2["zonder_katten"]
seen = set(); ZZ = []
for z in Z:
    k = norm(z["naam"])[:12]
    if k in seen or any(norm(z["naam"])[:10] in norm(l["naam"]) for l in L): continue
    seen.add(k); ZZ.append(z)
M["zonder_katten"] = ZZ
M["checked"] = "22-10-2026"
M["route"] = ["Zoo Plzeň", "Zoo Hluboká", "Zoo Tábor", "Othello Park", "Zoo Olomouc", "Zoo Ostrava"]
json.dump(M, open(D + "cz_final.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
CONF = set("gybr")
for l in sorted(L, key=lambda l: l["regio"]):
    print(l["regio"], "|", l["naam"], "|", l["type"], "|", " ".join(f'{k["soort"]}:{k["status"]}' for k in l["katten"]), "|", [g["geboren"] for g in l.get("geboortes", [])])
print(len(L), "locaties;", len([l for l in L if any(k["status"] in CONF for k in l["katten"])]), "bevestigd;", len(ZZ), "zonder")
