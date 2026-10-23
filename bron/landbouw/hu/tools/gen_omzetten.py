# Eenmalig: pl/gen.py -> hu/gen.py
import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../..")
s = open("pl/gen.py").read()
R = [("bron/gidsen/pl.html uit pl_basis.html (Poolse vaste teksten) + pl_final.json", "bron/gidsen/hu.html uit hu_basis.html (Hongaarse vaste teksten) + hu_final.json"),
 ('PLT = json.load(open(D + "pl.json", encoding="utf8")) if __import__("os").path.exists(D + "pl.json") else {}', 'HUT = json.load(open(D + "hu.json", encoding="utf8")) if __import__("os").path.exists(D + "hu.json") else {}'),
 ('"""Poolse tekst bij een nl/en-paar: uit pl.json (sleutel = Engelse tekst)."""', '"""Hongaarse tekst bij een nl/en-paar: uit hu.json (sleutel = Engelse tekst)."""'),
 ("if en in PLT: return PLT[en]", "if en in HUT: return HUT[en]"), ("if nl in PLT: return PLT[nl]", "if nl in HUT: return HUT[nl]"),
 ('o.get("pl")', 'o.get("hu")'), ('gidsen/pl.html"', 'gidsen/hu.html"'), ('"pl_basis.html"', '"hu_basis.html"'), ('"pl_final.json"', '"hu_final.json"'),
 ('t["pl"]', 't["hu"]'),
 ("LON0, LAT0, KX = 14.0, 55.0, 0.6163", "LON0, LAT0, KX = 16.0, 48.65, 0.6801"), ("PX(24.25, 0)", "PX(23.0, 0)"), ("PX(0, 48.9)", "PX(0, 45.65)"),
 ('aria-label="Kaart van Polen met', 'aria-label="Kaart van Hongarije met'),
 ('"Kaart van Polen met {len(LOCS_)} locaties met katachtigen","Map of Poland with', '"Kaart van Hongarije met {len(LOCS_)} locaties met katachtigen","Map of Hungary with'),
 ("r'(Map of Poland with )", "r'(Map of Hungary with )"), ('f"Mapa Polski: miejsca z kotami: {len(LOCS_)}"', 'f"Magyarország térképe: {len(LOCS_)} hely vadmacskákkal"'),
 ("TX.PL_VERV", "TX.HU_VERV"),
 ('"Bevestigd", "Confirmed", "Potwierdzone"', '"Bevestigd", "Confirmed", "Megerősítve"'), ('"Onzeker", "Uncertain", "Niepewne"', '"Onzeker", "Uncertain", "Bizonytalan"'),
 ('"vermeldingen", "entries", "wpisy"', '"vermeldingen", "entries", "bejegyzés"'),
 ('f"Niewidoczne w Polsce (gatunki: {len(niet)})"', 'f"Magyarországon nem látható ({len(niet)} faj)"'),
 ('f"Z kotami (miejsca: {len(LOCS_)})"', 'f"Vadmacskákkal ({len(LOCS_)} hely)"'),
 ('"Nie znaleziono kotów"', '"Nem találtunk vadmacskát"'), ('"O oficjalnej liście ogrodów zoologicznych"', '"A hivatalos állatkertlistáról"'),
 ('f"Trasa (parki: {len(pre)})"', 'f"Útvonal {len(pre)} parkkal"'),
 ('("pl", "-pl")', '("hu", "-hu")'),
 ('"(Polen: één pagina met de woiwodschappen)"', '"(Hongarije: één pagina met de megyék)"'),
 ('"in Poolse dierenlocaties"', '"in Hongaarse dierenlocaties"'), ('"in Polish zoos and animal parks"', '"in Hungarian zoos and animal parks"'),
 ('"Waar te zien in Polen"', '"Waar te zien in Hongarije"'), ('"Where to see it in Poland"', '"Where to see it in Hungary"'),
 ('"Wilde katachtigen in Polen"', '"Wilde katachtigen in Hongarije"'), ('"Wild cats in Poland"', '"Wild cats in Hungary"'),
 ('niet te zien in Polen."', 'niet te zien in Hongarije."'), ('not on view in Poland."', 'not on view in Hungary."'),
 ('nu in Polen te zien?"', 'nu in Hongarije te zien?"'), ('seen in Poland right now?"', 'seen in Hungary right now?"'),
 ("<title>Wilde katachtigen in Poolse dierenlocaties — stand 23 oktober 2026", "<title>Wilde katachtigen in Hongaarse dierenlocaties — stand 23 oktober 2026"),
 ('"Wild cats in Polish zoos and animal parks — updated 23 October 2026"', '"Wild cats in Hungarian zoos and animal parks — updated 23 October 2026"'),
 ('f"Niet in Polen te zien ({len(niet)} soorten)", f"Not on view in Poland ({len(niet)} species)"', 'f"Niet in Hongarije te zien ({len(niet)} soorten)", f"Not on view in Hungary ({len(niet)} species)"'),
]
for a, b in R:
    assert a in s, a; s = s.replace(a, b)
s = re.sub(r'\bPLT\b', 'HUT', s)
s = re.sub(r'(R[1567]|SP)PL\b', r'\1HU', s); s = s.replace('ROUTENOTE_PL', 'ROUTENOTE_HU')
s = s.replace('["nl", "en", "pl"]', '["nl", "en", "hu"]')
s = s.replace('MISS, open(D + "pl_ontbreekt.json"', 'MISS, open(D + "hu_ontbreekt.json"').replace("ontbreekt pl:", "ontbreekt hu:")
open("hu/gen.py", "w").write(s)
left = [l for l in s.split("\n") if re.search(r'Pol|Polsk|"pl"|\bpl\b|\bPL[A-Z]|[ąęśźżńć]', l)]
print("\n".join(x[:160] for x in left))
