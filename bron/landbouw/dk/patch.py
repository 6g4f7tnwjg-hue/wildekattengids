import os
# dk_merged.json + vv_resultaat.json + redactie -> dk_final.json
import json, copy
D = os.path.dirname(os.path.abspath(__file__)) + "/"
M = json.load(open(D + "dk_merged.json", encoding="utf8"))
V = json.load(open(D + "vv_resultaat.json", encoding="utf8"))
byname = {l["naam"]: l for l in M["locaties"]}
VMAP = {"HANSENBERG Zoo (Hansenberg Organia)": None, "Glad Zoo": None}

# ---- vervolgonderzoek verwerken: katten per soort vervangen, lege velden niet overschrijven
for v in V["locaties"]:
    if v["naam"] not in byname:
        v = copy.deepcopy(v); v["regio"] = "syddanmark"; M["locaties"].append(v); byname[v["naam"]] = v; continue
    l = byname[v["naam"]]
    for f in ("uren", "about", "earlier"):
        if (v.get(f) or {}).get("nl"):
            l[f] = v[f]
    ks = {k["soort"]: k for k in l["katten"]}
    for k in v["katten"]: ks[k["soort"]] = k
    l["katten"] = list(ks.values())
    if v.get("geboortes"):
        l["geboortes"] = v["geboortes"]
for z in list(M["zonder_katten"]):
    if z["naam"] in ("Glad Zoo",): M["zonder_katten"].remove(z)

# ---- redactie per locatie
E = {
 "Zoologisk Have København (ZOO København)": dict(naam="Zoo København", plaats="Frederiksberg (København)", type="Dierentuin", labels=[]),
 "Knuthenborg Safaripark": dict(plaats="Maribo (Lolland)", type="Safaripark", labels=["seizoen"]),
 "Odsherred Zoo Rescue": dict(plaats="Asnæs (Odsherred)", type="Opvang of sanctuary", labels=["seizoen"]),
 "Krokodille Zoo": dict(plaats="Eskilstrup (Falster)", type="Dierenpark", labels=["nietdagelijks"]),
 "Pangea Park Falster": dict(plaats="Nykøbing Falster", type="Dierenpark", labels=[]),
 "ZOOPARK Sydsjælland (ZOOPARK Næstved)": dict(naam="Zoopark Sydsjælland", plaats="Næstved", type="Dierenpark", labels=[], url="https://www.visitdenmark.dk/"),
 "Odense ZOO": dict(naam="Odense Zoo", plaats="Odense", type="Dierentuin", labels=[]),
 "GIVSKUD ZOO – ZOOTOPIA": dict(naam="Givskud Zoo – Zootopia", plaats="Givskud (Vejle)", type="Safaripark", labels=["seizoen"]),
 "Blåvand Zoo": dict(plaats="Blåvand (Varde)", type="Dierenpark", labels=[]),
 "Skærup Zoo": dict(plaats="Skærup (Børkop, Vejle)", type="Dierenpark", labels=["seizoen"]),
 "Ree Park": dict(plaats="Ebeltoft (Djursland)", type="Safaripark", labels=["seizoen"]),
 "Randers Regnskov": dict(plaats="Randers", type="Dierentuin", labels=[]),
 "Jyllands Park Zoo": dict(plaats="Haunstrup (Herning)", type="Dierenpark", labels=["seizoen"]),
 "Munkholm Zoo": dict(plaats="Balle (Djursland)", type="Dierenpark", labels=["seizoen"]),
 "Aalborg Zoo": dict(plaats="Aalborg", type="Dierentuin", labels=[]),
 "HANSENBERG Zoo (Hansenberg Organia)": dict(naam="Hansenberg Zoo", plaats="Kolding", type="Dierenpark", labels=["bezoekdagen"]),
 "Glad Zoo": dict(plaats="Lintrup (Vejen)", type="Dierenpark", labels=["seizoen"]),
}
for old, e in E.items():
    l = byname[old]
    for k, v in e.items(): l[k] = v

# ---- teksten die ontbraken of beter moeten
def setk(loc, soort, **kw):
    l = next(x for x in M["locaties"] if x["naam"] == loc)
    k = next(x for x in l["katten"] if x["soort"] == soort)
    k.update(kw)
def drop(loc, soort):
    l = next(x for x in M["locaties"] if x["naam"] == loc)
    l["katten"] = [k for k in l["katten"] if k["soort"] != soort]
def loc(n): return next(x for x in M["locaties"] if x["naam"] == n)

setk("Zoo København", "Leeuw", ondersoort={"nl": "Zuidelijk (P. l. melanochaita)", "en": "Southern (P. l. melanochaita)"},
     aantal={"nl": "onbekend", "en": "unknown"})
setk("Zoo København", "Tijger", aantal={"nl": "minstens 4 (paar en 2 jonge poezen uit 2025)", "en": "at least 4 (pair and 2 young females from 2025)"})
setk("Zoo København", "Luipaard", aantal={"nl": "onbekend (kater, poes en 1 jong uit 2026)", "en": "unknown (male, female and 1 cub from 2026)"})
setk("Knuthenborg Safaripark", "Leeuw", aantal={"nl": "9 (5 katers, 4 leeuwinnen)", "en": "9 (5 males, 4 lionesses)"})
setk("Givskud Zoo – Zootopia", "Leeuw", aantal={"nl": "minstens 8 volwassen en 8 welpen uit 2026", "en": "at least 8 adults and 8 cubs from 2026"})
setk("Skærup Zoo", "Ocelot", ondersoort="—")
setk("Blåvand Zoo", "Leeuw", ondersoort={"nl": "wit", "en": "white"}, aantal={"nl": "onbekend (paar en 4 welpen uit 2025)", "en": "unknown (pair and 4 cubs from 2025)"})
setk("Ree Park", "Luipaard", ondersoort={"nl": "Noord-Chinees (P. p. orientalis, voorheen P. p. japonensis)", "en": "North Chinese (P. p. orientalis, formerly P. p. japonensis)"},
     aantal={"nl": "2 (kater Suresh en poes ShanXi)", "en": "2 (male Suresh and female ShanXi)"})
setk("Ree Park", "Leeuw", aantal={"nl": "onbekend (o.a. leeuwin Elsa en 3 welpen uit 2025)", "en": "unknown (incl. lioness Elsa and 3 cubs from 2025)"})
setk("Randers Regnskov", "Jaguar", ondersoort="—", aantal={"nl": "onbekend (o.a. poes Chica, dochter Sibba en 2 welpen uit 2026)", "en": "unknown (incl. female Chica, daughter Sibba and 2 cubs from 2026)"})
setk("Randers Regnskov", "Margay", ondersoort="—")
setk("Odsherred Zoo Rescue", "Caracal", ondersoort="—")
setk("Krokodille Zoo", "Nevelpanter", ondersoort="—")
setk("Krokodille Zoo", "Poema", ondersoort="—")
setk("Jyllands Park Zoo", "Caracal", ondersoort="—"); setk("Jyllands Park Zoo", "Serval", ondersoort="—")
setk("Munkholm Zoo", "Serval", ondersoort="—",
     toelichting={"nl": "Twee servalverblijven op de parkkaart; de parkteksten noemen ‘eksotiske servaler’ en het café heet ‘Serval Grillen’. Een bezoeker schreef in juli 2026 over servaljongen; het park heeft dat niet bevestigd.",
                  "en": "Two serval enclosures on the park map; the park texts mention ‘exotic servals’ and the café is called ‘Serval Grillen’. A visitor wrote about serval kittens in July 2026; the park has not confirmed this."},
     bron="Eigen site ‘Kort over haven’ en parkkaart (gezien 22-10-2026); Trustpilot-review juli 2026")
loc("Munkholm Zoo")["geboortes"] = []
setk("Munkholm Zoo", "Euraziatische lynx", ondersoort={"nl": "onbekend (‘Altai-lynx’ volgens het park)", "en": "unknown (‘Altai lynx’ according to the park)"})
setk("Skærup Zoo", "Jaguar", aantal={"nl": "onbekend", "en": "unknown"})
setk("Glad Zoo", "Serval", aantal={"nl": "onbekend (minstens 1 poes)", "en": "unknown (at least 1 female)"})
setk("Zoopark Sydsjælland", "Tijger", ondersoort={"nl": "Bengaals, incl. witte tijger", "en": "Bengal, incl. white tiger"})
# ondersoort-labels in vaste vorm
LAB = {"Amoer": {"nl": "Amoer", "en": "Amur"}, "Sumatraans": {"nl": "Sumatraans", "en": "Sumatran"}, "onbekend": {"nl": "onbekend", "en": "unknown"},
       "Noordelijk (L. l. lynx)": {"nl": "Noordelijk (L. l. lynx)", "en": "Northern (L. l. lynx)"},
       "Aziatisch (P. l. leo, voorheen P. l. persica)": {"nl": "Aziatisch (P. l. leo, voorheen P. l. persica)", "en": "Asiatic (P. l. leo, formerly P. l. persica)"},
       "Amoer (P. p. orientalis)": {"nl": "Amoer (P. p. orientalis)", "en": "Amur (P. p. orientalis)"},
       "Arabisch (F. m. harrisoni)": {"nl": "Arabisch (F. m. harrisoni)", "en": "Arabian (F. m. harrisoni)"}, "—": "—"}
for l in M["locaties"]:
    for k in l["katten"]:
        if isinstance(k["ondersoort"], str):
            assert k["ondersoort"] in LAB, (l["naam"], k["soort"], k["ondersoort"])
            k["ondersoort"] = LAB[k["ondersoort"]]
        k.setdefault("twijfel", None)
        if k["status"] != "w": k["twijfel"] = None
# geboortes: datums in vaste vorm
G = {("Zoo København", "Tijger"): "2025-07-09", ("Odense Zoo", "Leeuw"): "2025-09", ("Blåvand Zoo", "Leeuw"): "2025-07"}
for l in M["locaties"]:
    for g in l.get("geboortes", []):
        if (l["naam"], g["soort"]) in G: g["geboren"] = G[(l["naam"], g["soort"])]; g["approx"] = True
        if g["geboren"].startswith("2026-06 "): g["geboren"] = "2026-06"; g["approx"] = True
        g["geboren"] = g["geboren"].split(" ")[0]
loc("Zoo København")["geboortes"] = [g for g in loc("Zoo København")["geboortes"] if g["soort"] == "Luipaard"] + \
    [g for g in V["locaties"] if g["naam"].startswith("Zoologisk")][0]["geboortes"]
for g in loc("Zoo København")["geboortes"]:
    if g["soort"] == "Tijger": g["geboren"] = "2025-07-09"; g["approx"] = True; g["n"] = {"nl": "4 welpen, 2 in leven", "en": "4 cubs, 2 alive"}
for g in loc("Givskud Zoo – Zootopia")["geboortes"]:
    if g["geboren"].startswith("2026-06"): g["geboren"] = "2026-06"; g["approx"] = True
for g in loc("Blåvand Zoo")["geboortes"]: g["n"] = {"nl": "4 welpen", "en": "4 cubs"}; g["x"] = {"nl": "Witte leeuwen: één kater en drie poezen, de eerste levensvatbare welpen na 16 jaar. Namen en ouders niet bekendgemaakt.", "en": "White lions: one male and three females, the first viable cubs in 16 years. Names and parents not announced."}
for g in loc("Zoo København")["geboortes"]:
    if g["soort"] == "Luipaard": g["sub"] = {"nl": "Amoerpanter", "en": "Amur leopard"}

# volgorde: per regio zoals op de kaart (wordt in gen.py gesorteerd)
for l in M["locaties"]:
    if l["naam"] == "Zoo København":
        t = json.dumps(l, ensure_ascii=False).replace("geboren in ZOO", "geboren in Zoo København").replace("in ZOO geboren", "in Zoo København geboren").replace("Moeder geboren in ZOO", "Moeder geboren in Zoo København")
        l.clear(); l.update(json.loads(t))
EARL = {
 "Zoo København": {"nl": "Caracal: gehouden tot 2024 (in het jaarverslag 2024 nog genoemd; volgens de stamboekgegevens op Zootierliste op 31-12-2024 geen meer). Poema’s: meerdere worpen tussen 1959 en 1978 (DR, 2023).",
                   "en": "Caracal: kept until 2024 (still mentioned in the 2024 annual report; according to studbook data on Zootierliste none left on 31-12-2024). Pumas: several litters between 1959 and 1978 (DR, 2023)."},
 "Odense Zoo": {"nl": "", "en": ""}, "Givskud Zoo – Zootopia": {"nl": "", "en": ""},
}
for n, e in EARL.items(): loc(n)["earlier"] = e
M["checked"] = "22-10-2026"
M["route"] = ["Ree Park", "Zoo København", "Randers Regnskov", "Krokodille Zoo", "Skærup Zoo", "Odsherred Zoo Rescue"]
json.dump(M, open(D + "dk_final.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
for l in M["locaties"]: print(l["regio"], l["naam"], [(k["soort"], k["status"]) for k in l["katten"]], [g["geboren"] for g in l.get("geboortes", [])])
