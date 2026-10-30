import os
# ro_merged.json + vv1 + redactie -> ro_final.json
import json, copy, re, unicodedata
D = os.path.dirname(os.path.abspath(__file__)) + "/"
M = json.load(open(D + "ro_merged.json", encoding="utf8"))
V1 = json.load(open(D + "vv1_resultaat.json", encoding="utf8")) if os.path.exists(D + "vv1_resultaat.json") else {"locaties": [], "zonder_katten": [], "lidmaatschap": {}}
exec(open(D + "merge.py").read().split("L=[];Z=[]")[0])   # regio()
def norm(s): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", s.lower().replace("ł", "l")).encode("ascii", "ignore").decode())

# dubbelingen: de vermeldingen van "op" staan ook bij de regio-agenten; die versies houden
L = [copy.deepcopy(l) for l in M["locaties"] if l["_bron"] != "op" and not l["_bron"].startswith("vv")]
for v in V1["locaties"]:   # vv1 levert volledige records
    v = copy.deepcopy(v); old = [i for i, l in enumerate(L) if l["naam"] == v["naam"]]
    if old: L[old[0]] = v
    else: L.append(v)
# locaties zonder (overgebleven) katten naar "zonder katten"
LEEG = [l for l in L if not l["katten"]]
L = [l for l in L if l["katten"]]
M["zonder_katten"] = M["zonder_katten"] + [{"naam": l["naam"], "plaats": l["plaats"], "reden": {"nl": "Geen katten meer bevestigd. " + (l.get("earlier") or {}).get("nl", ""), "en": "No cats confirmed any more. " + (l.get("earlier") or {}).get("en", "")}} for l in LEEG]
for l in L:
    l["regio"] = regio(l.get("lon"), l.get("lat")); l.pop("judet", None); l.pop("_bron", None)
    if l["naam"] in V1.get("lidmaatschap", {}): l["lidmaatschap"] = V1["lidmaatschap"][l["naam"]]
def loc(n):
    l = [x for x in L if x["naam"] == n]; assert l, n; return l[0]

# ---- redactie: weergavenaam, plaats, type, labels
# Dierentuin = vergunning op de ANMAP-lijst (14-11-2025; FGZAR heeft geen openbare ledenlijst); Bârlad (vergunning in aanvraag) = Dierenpark;
# particulieren zonder vergunning = Particuliere houder
E = {
 "Grădina Zoologică București (Zoo Băneasa)": ("Zoo București (Băneasa)", "București", "Dierentuin", []),
 "Grădina Zoologică Ploiești (Zoo Bucov)": ("Zoo Ploiești (Bucov)", "Bucov (Ploiești)", "Dierentuin", []),
 "Grădina Zoologică Pitești (Pădurea Trivale)": ("Zoo Pitești (Trivale)", "Pitești", "Dierentuin", []),
 "Grădina Zoologică Craiova (Parcul Nicolae Romanescu)": ("Zoo Craiova", "Craiova", "Dierentuin", []),
 "Grădina Zoologică Călărași (Complexul de Agrement Dumbrava)": ("Zoo Călărași", "Călărași", "Dierentuin", []),
 "Grădina Zoologică Târgoviște (Parcul Chindia)": ("Zoo Târgoviște", "Târgoviște", "Dierentuin", []),
 "Grădina Zoologică Râmnicu Vâlcea (Ostroveni)": ("Zoo Râmnicu Vâlcea", "Râmnicu Vâlcea", "Dierentuin", []),
 "Grădina Zoologică Brașov (Zoo Brașov)": ("Zoo Brașov", "Brașov", "Dierentuin", []),
 "Grădina Zoologică Târgu Mureș": ("Zoo Târgu Mureș", "Târgu Mureș", "Dierentuin", []),
 "Grădina Zoologică Sibiu": ("Zoo Sibiu", "Sibiu", "Dierentuin", []),
 "Grădina Zoologică Oradea": ("Zoo Oradea", "Oradea", "Dierentuin", []),
 "Grădina Zoologică „Prof. Ioan Crișan” Reșița": ("Zoo Reșița", "Reșița", "Dierentuin", []),
 "Parcul de Agrement „Moara de Vânt” (Zoo Parc Cluj)": ("Zooparc Moara de Vânt", "Sălicea (bij Cluj-Napoca)", "Dierentuin", []),
 "Liska Park": ("Liska Park", "Valea Târnei (Șinteu)", "Particuliere houder", []),
 "Ținutul Cailor": ("Ținutul Cailor", "Felcheriu (Oșorhei)", "Particuliere houder", []),
 "Grădina Zoologică Bârlad": ("Zoo Bârlad", "Bârlad", "Dierenpark", []),
 "Grădina Zoologică Brăila": ("Zoo Brăila", "Brăila", "Dierentuin", []),
 "Grădina Zoologică Galați (Pădurea Gârboavele)": ("Zoo Galați (Gârboavele)", "Tulucești (bij Galați)", "Dierentuin", []),
 "Parcul Zoologic Rădăuți": ("Zoo Rădăuți", "Rădăuți", "Dierentuin", []),
 "Arca lui Noe": ("Arca lui Noe", "Zaharești (Stroiești)", "Particuliere houder", []),
}
EXTRA = {}
E.update(EXTRA)
for old, (nm, pl, ty, lab) in E.items():
    l = loc(old); l["naam"], l["plaats"], l["type"], l["labels"] = nm, pl, ty, lab
loc("Zoo București (Băneasa)")["regio"] = "bucuresti"   # ligt net over de NUTS-grens met Ilfov
loc("Arca lui Noe")["geboortes"] = []   # gesloten, niet geregistreerde welpen
an = loc("Arca lui Noe")   # feitelijk houden: geen beschuldigingen
an["about"] = {"nl": "Particuliere dierentuin met ongeveer 500 dieren, nooit vergund als dierentuin. Sinds september 2025 gesloten voor publiek, na bijtincidenten. Op 06-05-2026 stierf liger Goliath (geboren juni 2025) bij een brand.",
               "en": "Private zoo with about 500 animals, never licensed as a zoo. Closed to the public since September 2025, after biting incidents. Liger Goliath (born June 2025) died in a fire on 06-05-2026."}
for k in an["katten"]:
    if k["soort"] == "Tijger": k["toelichting"] = {"nl": "Particuliere houder; gesloten voor publiek. In 2025 waren er volgens een reportage tijgers, ook een witte tijger.", "en": "Private keeper; closed to the public. According to a 2025 report there were tigers, including a white tiger."}
    if k["soort"] == "Serval": k["toelichting"] = {"nl": "Particuliere houder; gesloten voor publiek. Volgens een reportage uit 2025 minstens twee servals.", "en": "Private keeper; closed to the public. According to a 2025 report at least two servals."}
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
    l["geboortes"] = [g for g in l.get("geboortes", []) if g["geboren"][:1].isdigit() and len(g["geboren"]) >= 7]
    for g in l.get("geboortes", []):
        b = g["geboren"]; ap = bool(re.search(r"[a-z(]", b)) or len(b.split(" ")[0].split("-")) < 3
        g["geboren"] = b.split(" ")[0].split("/")[0]
        if ap: g["approx"] = True
    if l["plaats"] == "–": l["lon"] = l["lat"] = None; l["regio"] = "circus"
M["locaties"] = L
Z = M["zonder_katten"] + V1["zonder_katten"]
DUBBEL = {"Zoo Park România (rondreizende dierenshow)", "Libearty Bear Sanctuary (Asociația Milioane de Prieteni)", "Menagerie International Wildlife Foundation (IWF)"}
seen = set(); ZZ = []
for z in Z:
    k = norm(z["naam"])
    if k in seen or z["naam"] in DUBBEL or any(k == norm(l["naam"]) for l in L): continue
    seen.add(k); ZZ.append(z)
M["zonder_katten"] = ZZ
M["checked"] = "30-10-2026"
M["route"] = ["Zoo București (Băneasa)", "Zoo Brașov", "Zoo Târgu Mureș"]
json.dump(M, open(D + "ro_final.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
CONF = set("gybr")
for l in sorted(L, key=lambda l: l["regio"]):
    print(l["regio"], "|", l["naam"], "|", l["type"], "|", " ".join(f'{k["soort"]}:{k["status"]}' for k in l["katten"]), "|", [g["geboren"] for g in l.get("geboortes", [])])
print(len(L), "locaties;", len([l for l in L if any(k["status"] in CONF for k in l["katten"])]), "bevestigd;", len(ZZ), "zonder")
