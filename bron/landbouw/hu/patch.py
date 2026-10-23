import os
# hu_merged.json + vv1 + redactie -> hu_final.json
import json, copy, re, unicodedata
D = os.path.dirname(os.path.abspath(__file__)) + "/"
M = json.load(open(D + "hu_merged.json", encoding="utf8"))
V1 = json.load(open(D + "vv1_resultaat.json", encoding="utf8")) if os.path.exists(D + "vv1_resultaat.json") else {"locaties": [], "zonder_katten": [], "lidmaatschap": {}}
exec(open(D + "merge.py").read().split("L=[];Z=[]")[0])   # regio()
def norm(s): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", s.lower().replace("ł", "l")).encode("ascii", "ignore").decode())

# dubbelingen: de vermeldingen van "op" staan ook bij de regio-agenten; die versies houden
L = [copy.deepcopy(l) for l in M["locaties"] if l["_bron"] != "op"]
for v in V1["locaties"]:   # vv1 levert volledige records
    v = copy.deepcopy(v); old = [i for i, l in enumerate(L) if l["naam"] == v["naam"]]
    if old: L[old[0]] = v
    else: L.append(v)
# locaties zonder (overgebleven) katten naar "zonder katten"
LEEG = [l for l in L if not l["katten"]]
L = [l for l in L if l["katten"]]
M["zonder_katten"] = M["zonder_katten"] + [{"naam": l["naam"], "plaats": l["plaats"], "reden": {"nl": "Geen katten meer bevestigd. " + (l.get("earlier") or {}).get("nl", ""), "en": "No cats confirmed any more. " + (l.get("earlier") or {}).get("en", "")}} for l in LEEG]
for l in L:
    l["regio"] = regio(l.get("lon"), l.get("lat")); l.pop("megye", None); l.pop("_bron", None)
    if l["naam"] in V1.get("lidmaatschap", {}): l["lidmaatschap"] = V1["lidmaatschap"][l["naam"]]
def loc(n):
    l = [x for x in L if x["naam"] == n]; assert l, n; return l[0]

# ---- redactie: weergavenaam, plaats, type, labels
# Dierentuin = lid van EAZA of MÁSZ (MÁASZ); opvang behoudt zijn eigen type; andere vergunde parken = Dierenpark
E = {
 "Fővárosi Állat- és Növénykert": ("Zoo Budapest", "Budapest (Városliget)", "Dierentuin", []),
 "Veresegyházi Medveotthon": ("Medveotthon Veresegyház", "Veresegyház", "Opvang of sanctuary", []),
 "Budakeszi Vadaspark": ("Budakeszi Vadaspark", "Budakeszi", "Dierentuin", []),
 "Szentendrei Kisállatkert": ("Szentendrei Kisállatkert", "Szentendre", "Dierenpark", []),
 "ZOO Szigetbecse": ("Zoo Szigetbecse", "Szigetbecse", "Dierenpark", []),
 "Richter Safari Park": ("Richter Safari Park", "Nagykőrös", "Dierenpark", []),
 "Nyíregyházi Állatpark (Sóstó Zoo)": ("Sóstó Zoo", "Nyíregyháza", "Dierentuin", []),
 "Debreceni Állat- és Növénykert (Zoo Debrecen)": ("Zoo Debrecen", "Debrecen", "Dierentuin", []),
 "Miskolci Állatkert": ("Zoo Miskolc", "Miskolc", "Dierentuin", []),
 "Gyöngyösi Állatkert": ("Zoo Gyöngyös", "Gyöngyös", "Dierenpark", []),
 "Jászberényi Állat- és Növénykert": ("Zoo Jászberény", "Jászberény", "Dierentuin", []),
 "Hortobágyi Vadaspark (Pusztaszafari)": ("Hortobágyi Vadaspark", "Hortobágy (Malomháza)", "Wildpark", ["rondleiding"]),
 "Szegedi Vadaspark": ("Szegedi Vadaspark", "Szeged", "Dierentuin", []),
 "Kittenberger Kálmán Növény- és Vadaspark (Veszprémi Állatkert)": ("Zoo Veszprém", "Veszprém", "Dierentuin", []),
 "Xantus János Állatkert": ("Zoo Győr", "Győr", "Dierentuin", []),
 "Pécsi Állatkert és Akvárium-Terrárium (PécsZoo)": ("Zoo Pécs", "Pécs", "Dierentuin", []),
 "Kecskeméti Vadaskert": ("Kecskeméti Vadaskert", "Kecskemét", "Dierentuin", []),
 "MaganZOO Állat- és Szabadidőpark": ("MaganZOO", "Felsőlajos", "Dierenpark", []),
 "Állatkert, Állatsimogató és Állatotthon a Csácsi-hegyen": ("Állatkert Csácsi-hegy", "Zalaegerszeg", "Dierenpark", []),
 "Mecske Zoo (voorheen RepZOOtic Animal Center)": ("Mecske Zoo", "Erdősmecske", "Opvang of sanctuary", []),
}
EXTRA = {}   # nieuwe locaties uit vv1: naam -> (weergavenaam, plaats, type, labels)
E.update(EXTRA)
for old, (nm, pl, ty, lab) in E.items():
    l = loc(old); l["naam"], l["plaats"], l["type"], l["labels"] = nm, pl, ty, lab
# geen namen van particulieren
cs = loc("Állatkert Csácsi-hegy")
cs["about"] = {"nl": "Particulier dierenpark met kinderboerderij en opvang (sinds 2014) met ongeveer 140 dieren, ook afgedankte circusdieren. Na jarenlange procedures over de tijgers kreeg het in december 2024 een dierentuinvergunning en een groter tijgerverblijf.",
               "en": "Private animal park with petting zoo and animal home (since 2014), with about 140 animals including retired circus animals. After years of disputes over the tigers it received a zoo licence in December 2024 and an enlarged tiger enclosure."}
assert len(L) == len(E), sorted(set(l["naam"] for l in L) - {v[0] for v in E.values()})

LAB = {
 "Amoer": ("Amoer", "Amur"), "Sumatraans": ("Sumatraans", "Sumatran"), "Bengaals": ("Bengaals", "Bengal"),
 "Bengaals, incl. witte tijger": ("Bengaals, incl. witte tijger", "Bengal, incl. white tiger"),
 "Aziatisch (P. l. leo, voorheen P. l. persica)": ("Aziatisch (P. l. leo, voorheen P. l. persica)", "Asiatic (P. l. leo, formerly P. l. persica)"),
 "Zuidelijk (P. l. melanochaita)": ("Zuidelijk (P. l. melanochaita)", "Southern (P. l. melanochaita)"),
 "Zuidelijk (P. l. melanochaita), incl. witte leeuw": ("Zuidelijk (P. l. melanochaita), incl. witte leeuw", "Southern (P. l. melanochaita), incl. white lion"),
 "Amoer (P. p. orientalis)": ("Amoer (P. p. orientalis)", "Amur (P. p. orientalis)"),
 "Noord-Chinees (P. p. japonensis)": ("Noord-Chinees (P. p. orientalis, voorheen P. p. japonensis)", "North Chinese (P. p. orientalis, formerly P. p. japonensis)"),
 "Perzisch": ("Perzisch", "Persian"), "Sri Lanka (P. p. kotiya)": ("Sri Lanka (P. p. kotiya)", "Sri Lankan (P. p. kotiya)"),
 "Afrikaans (P. p. pardus), zwarte panter": ("Afrikaans (P. p. pardus), zwarte panter", "African (P. p. pardus), black panther"),
 "Afrikaans (P. p. pardus) volgens eigen site": ("Afrikaans (P. p. pardus)", "African (P. p. pardus)"),
 "zwarte panter": ("onbekend, zwarte panter", "unknown, black panther"),
 "Maleis (P. t. jacksoni)": ("Maleis (P. t. jacksoni)", "Malayan (P. t. jacksoni)"),
 "Maleis (P. t. tigris, voorheen P. t. jacksoni)": ("Maleis (P. t. tigris, voorheen P. t. jacksoni)", "Malayan (P. t. tigris, formerly P. t. jacksoni)"),
 "Noord-Chinees (P. p. orientalis, voorheen P. p. japonensis)": ("Noord-Chinees (P. p. orientalis, voorheen P. p. japonensis)", "North Chinese (P. p. orientalis, formerly P. p. japonensis)"),
 "Afrikaans (P. p. pardus)": ("Afrikaans (P. p. pardus)", "African (P. p. pardus)"),
 "Zuidelijk (P. l. melanochaita), wit": ("Zuidelijk (P. l. melanochaita), wit", "Southern (P. l. melanochaita), white"),
 "onbekend, incl. witte leeuw": ("onbekend, incl. witte leeuw", "unknown, incl. white lion"),
 "onbekend, incl. witte leeuw (‘fehér krugeri’)": ("onbekend, incl. witte leeuw", "unknown, incl. white lion"),
 "onbekend, incl. witte tijger": ("onbekend, incl. witte tijger", "unknown, incl. white tiger"),
 "onbekend, zwarte panter": ("onbekend, zwarte panter", "unknown, black panther"),
 "onbekend, incl. witte leeuw (Zuidelijk, P. l. melanochaita)": ("Zuidelijk (P. l. melanochaita), incl. witte leeuw", "Southern (P. l. melanochaita), incl. white lion"),
 "Zuidelijk (A. j. jubatus)": ("Zuidelijk (A. j. jubatus)", "Southern (A. j. jubatus)"),
 "Noordelijk (L. l. lynx)": ("Noordelijk (L. l. lynx)", "Northern (L. l. lynx)"),
 "Karpatisch (L. l. carpathicus)": ("Karpatisch (L. l. carpathicus)", "Carpathian (L. l. carpathicus)"),
 "Arabisch (F. m. harrisoni)": ("Arabisch (F. m. harrisoni)", "Arabian (F. m. harrisoni)"),
 "Mongools (O. m. manul)": None, "O. m. manul": None,
 "Sri Lanka (P. r. phillipsi)": ("Sri Lanka (P. r. phillipsi)", "Sri Lankan (P. r. phillipsi)"),
 "Amoer (P. b. euptilura)": ("Amoer (P. b. euptilura)", "Amur (P. b. euptilura)"),
 "onbekend": ("onbekend", "unknown"), "—": None,
}
KLEIN = ("Serval", "Caracal", "Poema", "Margay", "Jaguar", "Rode lynx", "Manoel", "Ocelot", "Jaguarundi", "Vissende kat", "Geoffroy’s kat", "Sneeuwluipaard", "Nevelpanter", "Roestkat", "Europese wilde kat", "Zandkat", "Bengaalse kat")
for l in L:
    for k in l["katten"]:
        if k["soort"] == "Manoel (Pallas’ kat)": k["soort"] = "Manoel"
        o = k["ondersoort"]; o = o if isinstance(o, str) else o.get("nl")
        assert o in LAB, (l["naam"], k["soort"], o)
        v = LAB[o]
        if v is None or (o == "onbekend" and k["soort"] in KLEIN):
            k["ondersoort"] = "—"
        else:
            k["ondersoort"] = {"nl": v[0], "en": v[1]}
        if k["status"] != "w": k["twijfel"] = None
        elif not k.get("twijfel"): k["twijfel"] = {"nl": k["toelichting"]["nl"], "en": k["toelichting"]["en"]}
    # geboortes zonder datum weg (MaganZOO: vier witte tijgerwelpen, "vóór maart 2025"); servaljong april 2026
    l["geboortes"] = [g for g in l.get("geboortes", []) if g["geboren"][:1].isdigit()]
    for g in l["geboortes"]:
        if l["naam"] == "MaganZOO" and g["soort"] == "Serval" and g["geboren"].startswith("2026 "): g["geboren"] = "2026-04"
    for g in l.get("geboortes", []):
        b = g["geboren"]; ap = bool(re.search(r"[a-z(]", b)) or len(b.split(" ")[0].split("-")) < 3
        g["geboren"] = b.split(" ")[0].split("/")[0]
        if ap: g["approx"] = True
    if l["plaats"] == "–": l["lon"] = l["lat"] = None; l["regio"] = "circus"
M["locaties"] = L
Z = M["zonder_katten"] + V1["zonder_katten"]
seen = set(); ZZ = []
for z in Z:
    k = norm(z["naam"])[:12]
    if k in seen or any(norm(z["naam"])[:10] in norm(l["naam"]) or norm(l["naam"])[:10] in norm(z["naam"]) for l in L): continue
    seen.add(k); ZZ.append(z)
M["zonder_katten"] = ZZ
M["checked"] = "23-10-2026"
M["route"] = ["Szegedi Vadaspark", "Zoo Budapest", "Szentendrei Kisállatkert", "Zoo Gyöngyös", "Sóstó Zoo"]
json.dump(M, open(D + "hu_final.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
CONF = set("gybr")
for l in sorted(L, key=lambda l: l["regio"]):
    print(l["regio"], "|", l["naam"], "|", l["type"], "|", " ".join(f'{k["soort"]}:{k["status"]}' for k in l["katten"]), "|", [g["geboren"] for g in l.get("geboortes", [])])
print(len(L), "locaties;", len([l for l in L if any(k["status"] in CONF for k in l["katten"])]), "bevestigd;", len(ZZ), "zonder")
