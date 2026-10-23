# Eenmalig: fi/gen.py -> pl/gen.py
import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../..")
s = open("fi/gen.py").read()
R = [("bron/gidsen/fi.html uit fi_basis.html (Finse vaste teksten) + fi_final.json", "bron/gidsen/pl.html uit pl_basis.html (Poolse vaste teksten) + pl_final.json"),
 ('FI = json.load(open(D + "fi.json", encoding="utf8")) if __import__("os").path.exists(D + "fi.json") else {}', 'PLT = json.load(open(D + "pl.json", encoding="utf8")) if __import__("os").path.exists(D + "pl.json") else {}'),
 ('"""Finse tekst bij een nl/en-paar: uit fi.json (sleutel = Engelse tekst)."""', '"""Poolse tekst bij een nl/en-paar: uit pl.json (sleutel = Engelse tekst)."""'),
 ("if en in FI: return FI[en]", "if en in PLT: return PLT[en]"), ("if nl in FI: return FI[nl]", "if nl in PLT: return PLT[nl]"),
 ('o.get("fi")', 'o.get("pl")'), ('gidsen/fi.html"', 'gidsen/pl.html"'), ('"fi_basis.html"', '"pl_basis.html"'), ('"fi_final.json"', '"pl_final.json"'),
 ('t["fi"]', 't["pl"]'),
 ('x = x.replace("æ", "ae").replace("ø", "oe")', 'x = x.replace("ł", "l").replace("Ł", "L").replace("æ", "ae").replace("ø", "oe")'),
 ("LON0, LAT0, KX = 19.0, 70.15, 0.4246", "LON0, LAT0, KX = 14.0, 55.0, 0.6163"), ("PX(31.7, 0)", "PX(24.25, 0)"), ("PX(0, 59.6)", "PX(0, 48.9)"),
 ('aria-label="Kaart van Finland met', 'aria-label="Kaart van Polen met'),
 ('"Kaart van Finland met {len(LOCS_)} locaties met katachtigen","Map of Finland with', '"Kaart van Polen met {len(LOCS_)} locaties met katachtigen","Map of Poland with'),
 ("r'(Map of Finland with )", "r'(Map of Poland with )"), ('f"Suomen kartta: {len(LOCS_)} paikkaa, joissa on kissaeläimiä"', 'f"Mapa Polski: miejsca z kotami: {len(LOCS_)}"'),
 ("TX.FI_VERV", "TX.PL_VERV"),
 ('"Bevestigd", "Confirmed", "Varmistettu"', '"Bevestigd", "Confirmed", "Potwierdzone"'), ('"Onzeker", "Uncertain", "Epävarma"', '"Onzeker", "Uncertain", "Niepewne"'),
 ('"vermeldingen", "entries", "merkintää"', '"vermeldingen", "entries", "wpisy"'),
 ('f"Ei nähtävissä Suomessa ({len(niet)} lajia)"', 'f"Niewidoczne w Polsce (gatunki: {len(niet)})"'),
 ('f"Kissaeläimiä ({len(LOCS_)} paikkaa)"', 'f"Z kotami (miejsca: {len(LOCS_)})"'),
 ('"Kissaeläimiä ei löytynyt"', '"Nie znaleziono kotów"'), ('"Virallisesta eläintarhaluettelosta"', '"O oficjalnej liście ogrodów zoologicznych"'),
 ('f"Reitti: {len(pre)} puistoa"', 'f"Trasa (parki: {len(pre)})"'),
 ('("fi", "-fi")', '("pl", "-pl")'),
 ('"(Finland: één pagina met de landschappen)"', '"(Polen: één pagina met de woiwodschappen)"'),
 ('"in Finse dierenlocaties"', '"in Poolse dierenlocaties"'), ('"in Finnish zoos and animal parks"', '"in Polish zoos and animal parks"'),
 ('"Waar te zien in Finland"', '"Waar te zien in Polen"'), ('"Where to see it in Finland"', '"Where to see it in Poland"'),
 ('"Wilde katachtigen in Finland"', '"Wilde katachtigen in Polen"'), ('"Wild cats in Finland"', '"Wild cats in Poland"'),
 ('niet te zien in Finland."', 'niet te zien in Polen."'), ('not on view in Finland."', 'not on view in Poland."'),
 ('nu in Finland te zien?"', 'nu in Polen te zien?"'), ('seen in Finland right now?"', 'seen in Poland right now?"'),
 ("<title>Wilde katachtigen in Finse dierenlocaties — stand 23 oktober 2026", "<title>Wilde katachtigen in Poolse dierenlocaties — stand 23 oktober 2026"),
 ('"Wild cats in Finnish zoos and animal parks — updated 23 October 2026"', '"Wild cats in Polish zoos and animal parks — updated 23 October 2026"'),
 ('f"Niet in Finland te zien ({len(niet)} soorten)", f"Not on view in Finland ({len(niet)} species)"', 'f"Niet in Polen te zien ({len(niet)} soorten)", f"Not on view in Poland ({len(niet)} species)"'),
]
for a, b in R:
    assert a in s, a; s = s.replace(a, b)
s = re.sub(r'\bFI\b', 'PLT', s)
s = re.sub(r'(R[1567]|SP)FI\b', r'\1PL', s); s = s.replace('ROUTENOTE_FI', 'ROUTENOTE_PL')
s = s.replace('["nl", "en", "fi"]', '["nl", "en", "pl"]')
s = s.replace('MISS, open(D + "fi_ontbreekt.json"', 'MISS, open(D + "pl_ontbreekt.json"').replace("ontbreekt fi:", "ontbreekt pl:")
open("pl/gen.py", "w").write(s)
left = [l for l in s.split("\n") if re.search(r'Finl|Finn|Suom|"fi"|\bfi\b|\bFI|[äö]', l)]
print("\n".join(x[:160] for x in left))
