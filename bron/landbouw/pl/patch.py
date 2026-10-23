import os
# pl_merged.json + vv1 + redactie -> pl_final.json
import json, copy, re, unicodedata
D = os.path.dirname(os.path.abspath(__file__)) + "/"
M = json.load(open(D + "pl_merged.json", encoding="utf8"))
V1 = json.load(open(D + "vv1_resultaat.json", encoding="utf8")) if os.path.exists(D + "vv1_resultaat.json") else {"locaties": [], "zonder_katten": [], "lidmaatschap": {}}
exec(open(D + "merge.py").read().split("L=[];Z=[]")[0])   # regio()
def norm(s): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", s.lower().replace("ł", "l")).encode("ascii", "ignore").decode())

# dubbelingen (regio-agent en op): Czchów, Łączna en Żużela uit de regio houden; servalhouder zonder plaats en zonder toegang niet opnemen (privacy)
WEG = {("op", "Fun Animals (particuliere houder, Czchów)"), ("op", "ZOO Łączna"), ("op", "Mini Zoo Żużela"), ("zu", "Particuliere servalhouder in powiat niżański")}
L = [copy.deepcopy(l) for l in M["locaties"] if (l["_bron"], l["naam"]) not in WEG]
for v in V1["locaties"]:   # vv1 levert volledige records
    v = copy.deepcopy(v); old = [i for i, l in enumerate(L) if l["naam"] == v["naam"]]
    if old: L[old[0]] = v
    else: L.append(v)
for l in L:
    l["regio"] = regio(l.get("lon"), l.get("lat")); l.pop("woj", None); l.pop("_bron", None)
    if l["naam"] in V1.get("lidmaatschap", {}): l["lidmaatschap"] = V1["lidmaatschap"][l["naam"]]
def loc(n):
    l = [x for x in L if x["naam"] == n]; assert l, n; return l[0]

# ---- redactie: weergavenaam, plaats, type, labels
# Dierentuin = lid van EAZA of RDPOZiA; Dierenpark = wel op de GDOŚ-lijst (vergund), geen lid; Particuliere houder = minizoo zonder dierentuinvergunning
E = {
 "Gdański Ogród Zoologiczny (Zoo Gdańsk)": ("Zoo Gdańsk", "Gdańsk (Oliwa)", "Dierentuin", []),
 "Ogród Zoologiczny w Bydgoszczy (LPKiW Myślęcinek)": ("Zoo Bydgoszcz", "Bydgoszcz (Myślęcinek)", "Dierentuin", []),
 "Ogród Zoobotaniczny w Toruniu": ("Zoo Toruń", "Toruń", "Dierentuin", []),
 "Ogród Zoologiczny CANPOL": ("Zoo Canpol", "Sieroczyn (Człuchów)", "Dierenpark", ["gratis"]),
 "Akcent ZOO": ("Akcent Zoo", "Białystok", "Dierenpark", []),
 "Rezerwat Pokazowy Żubrów (Białowieski Park Narodowy)": ("Wisentreservaat Białowieża", "Białowieża", "Wildpark", []),
 "Lemur Park": ("Lemur Park", "Rumia", "Particuliere houder", []),
 "Park Edukacyjny Zoo-Egzotyczne Kaszuby": ("Zoo-Egzotyczne Kaszuby", "Tuchlino (Sierakowice)", "Particuliere houder", []),
 "ZOO Wrocław": ("Zoo Wrocław", "Wrocław", "Dierentuin", []),
 "Nowe Zoo (Ogród Zoologiczny w Poznaniu)": ("Nowe Zoo Poznań", "Poznań", "Dierentuin", []),
 "Ogród Zoologiczny w Opolu (Zoo Opole)": ("Zoo Opole", "Opole", "Dierentuin", []),
 "ZOO Łączna (ZOO Farma)": ("Zoo Łączna", "Łączna (Mieroszów)", "Dierenpark", []),
 "Mini Zoo Żużela": ("Mini Zoo Żużela", "Żużela (Krapkowice)", "Particuliere houder", []),
 "Ogród Zoologiczny w Nowym Tomyślu": ("Zoo Nowy Tomyśl", "Nowy Tomyśl", "Dierenpark", []),
 "Ogród Zoologiczny w Lubinie (ZOO Lubin)": ("Zoo Lubin", "Lubin", "Dierentuin", []),
 "Miejski Ogród Zoologiczny im. Antoniny i Jana Żabińskich w Warszawie (Zoo Warszawa)": ("Zoo Warszawa", "Warszawa", "Dierentuin", []),
 "Orientarium Zoo Łódź (Miejski Ogród Zoologiczny w Łodzi)": ("Orientarium Zoo Łódź", "Łódź", "Dierentuin", []),
 "Miejski Ogród Zoologiczny w Płocku (Zoo Płock)": ("Zoo Płock", "Płock", "Dierentuin", []),
 "Zoo Borysew (Zoo Safari Borysew)": ("Zoo Borysew", "Borysew (Poddębice)", "Dierenpark", []),
 "Ogród Zoologiczny im. Stefana Milera w Zamościu (Zoo Zamość)": ("Zoo Zamość", "Zamość", "Dierentuin", []),
 "Ogród Zoologiczny w Romanówce (Zoo Wojciechów)": ("Zoo Romanówka", "Romanówka (Wojciechów)", "Dierenpark", []),
 "Ogród Zoologiczny Leśne Zacisze": ("Zoo Leśne Zacisze", "Lisów (Morawica)", "Dierentuin", []),
 "Śląski Ogród Zoologiczny": ("Śląski Ogród Zoologiczny", "Chorzów", "Dierentuin", []),
 "Ogród Zoologiczny w Krakowie (Miejski Park i Ogród Zoologiczny)": ("Zoo Kraków", "Kraków", "Dierentuin", []),
 "Leśny Park Niespodzianek": ("Leśny Park Niespodzianek", "Ustroń", "Dierenpark", []),
 "Zwierzyniec Kopytkowo (Mini Zoo)": ("Zwierzyniec Kopytkowo", "Izdebnik (Lanckorona)", "Particuliere houder", []),
 "Particuliere houder Czchów": ("Particuliere houder Czchów", "Czchów", "Particuliere houder", []),
 "Dzika Zagroda w Jabłonowie (Zachodniopomorskie Towarzystwo Przyrodnicze)": ("Dzika Zagroda Jabłonowo", "Jabłonowo (Mirosławiec)", "Natuur- en fokcentrum", []),
 "Ośrodek Rehabilitacji Dzikich Zwierząt Klekusiowo": ("Klekusiowo", "Tomaszów Bolesławiecki", "Opvang of sanctuary", []),
 "Farma Goławice – Mini Zoo": ("Farma Goławice", "Goławice Drugie (Pomiechówek)", "Particuliere houder", ["rondleiding"]),
 "Hacjenda Alpaka – Mini ZOO Nowy Sącz": ("Hacjenda Alpaka", "Ubiad (Chełmiec)", "Particuliere houder", ["rondleiding"]),
 "Mini Zoo Zaczarnie": ("Mini Zoo Zaczarnie", "Zaczarnie (Lisia Góra)", "Particuliere houder", []),
 "MiniZooPark Walim": ("MiniZooPark Walim", "Walim (Stara Kornica)", "Particuliere houder", []),
}
for old, (nm, pl, ty, lab) in E.items():
    l = loc(old); l["naam"], l["plaats"], l["type"], l["labels"] = nm, pl, ty, lab
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
M["route"] = []
json.dump(M, open(D + "pl_final.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
CONF = set("gybr")
for l in sorted(L, key=lambda l: l["regio"]):
    print(l["regio"], "|", l["naam"], "|", l["type"], "|", " ".join(f'{k["soort"]}:{k["status"]}' for k in l["katten"]), "|", [g["geboren"] for g in l.get("geboortes", [])])
print(len(L), "locaties;", len([l for l in L if any(k["status"] in CONF for k in l["katten"])]), "bevestigd;", len(ZZ), "zonder")
