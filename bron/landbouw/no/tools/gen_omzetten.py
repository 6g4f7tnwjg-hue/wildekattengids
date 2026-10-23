# Eenmalig: se/gen.py -> no/gen.py
import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../..")
s = open("se/gen.py").read()
R = [("bron/gidsen/se.html uit se_basis.html (Zweedse vaste teksten) + se_final.json", "bron/gidsen/no.html uit no_basis.html (Noorse vaste teksten) + no_final.json"),
 ('SV = json.load(open(D + "sv.json", encoding="utf8")) if __import__("os").path.exists(D + "sv.json") else {}', 'NB = json.load(open(D + "nb.json", encoding="utf8")) if __import__("os").path.exists(D + "nb.json") else {}'),
 ('"""Zweedse tekst bij een nl/en-paar: uit sv.json (sleutel = Engelse tekst)."""', '"""Noorse tekst bij een nl/en-paar: uit nb.json (sleutel = Engelse tekst)."""'),
 ("if en in SV: return SV[en]", "if en in NB: return NB[en]"), ("if nl in SV: return SV[nl]", "if nl in NB: return NB[nl]"),
 ('o.get("sv")', 'o.get("nb")'), ('gidsen/se.html"', 'gidsen/no.html"'), ('"se_basis.html"', '"no_basis.html"'), ('"se_final.json"', '"no_final.json"'),
 ('t["sv"]', 't["nb"]'),
 ("LON0, LAT0, KX = 10.9, 69.1, 0.4668", "LON0, LAT0, KX = 4.4, 71.3, 0.4289"), ("PX(24.25, 0)", "PX(31.3, 0)"), ("PX(0, 55.25)", "PX(0, 57.9)"),
 ('aria-label="Kaart van Zweden met', 'aria-label="Kaart van Noorwegen met'),
 ('"Kaart van Zweden met {len(LOCS_)} locaties met katachtigen","Map of Sweden with', '"Kaart van Noorwegen met {len(LOCS_)} locaties met katachtigen","Map of Norway with'),
 ("r'(Map of Sweden with )", "r'(Map of Norway with )"), ('f"Karta över Sverige med {len(LOCS_)} platser med kattdjur"', 'f"Kart over Norge med {len(LOCS_)} steder med kattedyr"'),
 ("TX.SV_VERV", "TX.NB_VERV"),
 ('"Bevestigd", "Confirmed", "Bekräftade"', '"Bevestigd", "Confirmed", "Bekreftet"'), ('"Onzeker", "Uncertain", "Osäkra"', '"Onzeker", "Uncertain", "Usikre"'),
 ('"vermeldingen", "entries", "uppgifter"', '"vermeldingen", "entries", "oppføringer"'),
 ('f"Går inte att se i Sverige ({len(niet)} arter)"', 'f"Kan ikke ses i Norge ({len(niet)} arter)"'),
 ('f"Med kattdjur ({len(LOCS_)} platser)"', 'f"Med kattedyr ({len(LOCS_)} steder)"'),
 ('"Inga kattdjur hittades"', '"Ingen kattedyr funnet"'), ('"Om den officiella listan över djurparker"', '"Om den offisielle listen over dyreparker"'),
 ('f"Rutt med {len(pre)} parker"', 'f"Rute med {len(pre)} parker"'),
 ('("sv", "-sv")', '("nb", "-nb")'),
 ('"(Zweden: één pagina met de län)"', '"(Noorwegen: één pagina met de fylker)"'),
 ('"in Zweedse dierenlocaties"', '"in Noorse dierenlocaties"'), ('"in Swedish zoos and animal parks"', '"in Norwegian zoos and animal parks"'),
 ('"Waar te zien in Zweden"', '"Waar te zien in Noorwegen"'), ('"Where to see it in Sweden"', '"Where to see it in Norway"'),
 ('"Wilde katachtigen in Zweden"', '"Wilde katachtigen in Noorwegen"'), ('"Wild cats in Sweden"', '"Wild cats in Norway"'),
 ('niet te zien in Zweden."', 'niet te zien in Noorwegen.'+'"'), ('not on view in Sweden."', 'not on view in Norway.'+'"'),
 ('nu in Zweden te zien?"', 'nu in Noorwegen te zien?"'), ('seen in Sweden right now?"', 'seen in Norway right now?"'),
 ("<title>Wilde katachtigen in Zweedse dierenlocaties — stand 22 oktober 2026", "<title>Wilde katachtigen in Noorse dierenlocaties — stand 23 oktober 2026"),
 ('"Wild cats in Swedish zoos and animal parks — updated 22 October 2026"', '"Wild cats in Norwegian zoos and animal parks — updated 23 October 2026"'),
 ('f"Niet in Zweden te zien ({len(niet)} soorten)", f"Not on view in Sweden ({len(niet)} species)"', 'f"Niet in Noorwegen te zien ({len(niet)} soorten)", f"Not on view in Norway ({len(niet)} species)"'),
]
for a, b in R:
    assert a in s, a; s = s.replace(a, b)
s = re.sub(r'\bSV\b', 'NB', s)
s = re.sub(r'(R[1567]|SP)SV\b', r'\1NB', s); s = s.replace('ROUTENOTE_SV', 'ROUTENOTE_NB')
s = s.replace('["nl", "en", "sv"]', '["nl", "en", "nb"]')
s = s.replace('MISS, open(D + "sv_ontbreekt.json"', 'MISS, open(D + "nb_ontbreekt.json"').replace("ontbreekt sv:", "ontbreekt nb:")
open("no/gen.py", "w").write(s)
left = [l for l in s.split("\n") if re.search(r'Zwed|Swed|Sverige|"sv"|\bsv\b|\bSV|[äö]', l)]
print("\n".join(x[:160] for x in left))
