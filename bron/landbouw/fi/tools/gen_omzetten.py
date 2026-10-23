# Eenmalig: no/gen.py -> fi/gen.py
import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../..")
s = open("no/gen.py").read()
R = [("bron/gidsen/no.html uit no_basis.html (Noorse vaste teksten) + no_final.json", "bron/gidsen/fi.html uit fi_basis.html (Finse vaste teksten) + fi_final.json"),
 ('NB = json.load(open(D + "nb.json", encoding="utf8")) if __import__("os").path.exists(D + "nb.json") else {}', 'FI = json.load(open(D + "fi.json", encoding="utf8")) if __import__("os").path.exists(D + "fi.json") else {}'),
 ('"""Noorse tekst bij een nl/en-paar: uit nb.json (sleutel = Engelse tekst)."""', '"""Finse tekst bij een nl/en-paar: uit fi.json (sleutel = Engelse tekst)."""'),
 ("if en in NB: return NB[en]", "if en in FI: return FI[en]"), ("if nl in NB: return NB[nl]", "if nl in FI: return FI[nl]"),
 ('o.get("nb")', 'o.get("fi")'), ('gidsen/no.html"', 'gidsen/fi.html"'), ('"no_basis.html"', '"fi_basis.html"'), ('"no_final.json"', '"fi_final.json"'),
 ('t["nb"]', 't["fi"]'),
 ("LON0, LAT0, KX = 4.4, 71.3, 0.4289", "LON0, LAT0, KX = 19.0, 70.15, 0.4246"), ("PX(31.3, 0)", "PX(31.7, 0)"), ("PX(0, 57.9)", "PX(0, 59.6)"),
 ('aria-label="Kaart van Noorwegen met', 'aria-label="Kaart van Finland met'),
 ('"Kaart van Noorwegen met {len(LOCS_)} locaties met katachtigen","Map of Norway with', '"Kaart van Finland met {len(LOCS_)} locaties met katachtigen","Map of Finland with'),
 ("r'(Map of Norway with )", "r'(Map of Finland with )"), ('f"Kart over Norge med {len(LOCS_)} steder med kattedyr"', 'f"Suomen kartta: {len(LOCS_)} paikkaa, joissa on kissaeläimiä"'),
 ("TX.NB_VERV", "TX.FI_VERV"),
 ('"Bevestigd", "Confirmed", "Bekreftet"', '"Bevestigd", "Confirmed", "Varmistettu"'), ('"Onzeker", "Uncertain", "Usikre"', '"Onzeker", "Uncertain", "Epävarma"'),
 ('"vermeldingen", "entries", "oppføringer"', '"vermeldingen", "entries", "merkintää"'),
 ('f"Kan ikke ses i Norge ({len(niet)} arter)"', 'f"Ei nähtävissä Suomessa ({len(niet)} lajia)"'),
 ('f"Med kattedyr ({len(LOCS_)} steder)"', 'f"Kissaeläimiä ({len(LOCS_)} paikkaa)"'),
 ('"Ingen kattedyr funnet"', '"Kissaeläimiä ei löytynyt"'), ('"Om den offisielle listen over dyreparker"', '"Virallisesta eläintarhaluettelosta"'),
 ('f"Rute med {len(pre)} parker"', 'f"Reitti: {len(pre)} puistoa"'),
 ('("nb", "-nb")', '("fi", "-fi")'),
 ('"(Noorwegen: één pagina met de fylker)"', '"(Finland: één pagina met de landschappen)"'),
 ('"in Noorse dierenlocaties"', '"in Finse dierenlocaties"'), ('"in Norwegian zoos and animal parks"', '"in Finnish zoos and animal parks"'),
 ('"Waar te zien in Noorwegen"', '"Waar te zien in Finland"'), ('"Where to see it in Norway"', '"Where to see it in Finland"'),
 ('"Wilde katachtigen in Noorwegen"', '"Wilde katachtigen in Finland"'), ('"Wild cats in Norway"', '"Wild cats in Finland"'),
 ('niet te zien in Noorwegen."', 'niet te zien in Finland."'), ('not on view in Norway."', 'not on view in Finland."'),
 ('nu in Noorwegen te zien?"', 'nu in Finland te zien?"'), ('seen in Norway right now?"', 'seen in Finland right now?"'),
 ("<title>Wilde katachtigen in Noorse dierenlocaties — stand 23 oktober 2026", "<title>Wilde katachtigen in Finse dierenlocaties — stand 23 oktober 2026"),
 ('"Wild cats in Norwegian zoos and animal parks — updated 23 October 2026"', '"Wild cats in Finnish zoos and animal parks — updated 23 October 2026"'),
 ('f"Niet in Noorwegen te zien ({len(niet)} soorten)", f"Not on view in Norway ({len(niet)} species)"', 'f"Niet in Finland te zien ({len(niet)} soorten)", f"Not on view in Finland ({len(niet)} species)"'),
]
for a, b in R:
    assert a in s, a; s = s.replace(a, b)
s = re.sub(r'\bNB\b', 'FI', s)
s = re.sub(r'(R[1567]|SP)NB\b', r'\1FI', s); s = s.replace('ROUTENOTE_NB', 'ROUTENOTE_FI')
s = s.replace('["nl", "en", "nb"]', '["nl", "en", "fi"]')
s = s.replace('MISS, open(D + "nb_ontbreekt.json"', 'MISS, open(D + "fi_ontbreekt.json"').replace("ontbreekt nb:", "ontbreekt fi:")
open("fi/gen.py", "w").write(s)
left = [l for l in s.split("\n") if re.search(r'Noorw|Norw|Norge|"nb"|\bnb\b|\bNB|[æø]|Usikk', l)]
print("\n".join(x[:160] for x in left))
