# Eenmalig: hu/gen.py -> ro/gen.py
import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../..")
s = open("hu/gen.py").read()
R = [("bron/gidsen/hu.html uit hu_basis.html (Hongaarse vaste teksten) + hu_final.json", "bron/gidsen/ro.html uit ro_basis.html (Roemeense vaste teksten) + ro_final.json"),
 ('HUT = json.load(open(D + "hu.json", encoding="utf8")) if __import__("os").path.exists(D + "hu.json") else {}', 'ROT = json.load(open(D + "ro.json", encoding="utf8")) if __import__("os").path.exists(D + "ro.json") else {}'),
 ('"""Hongaarse tekst bij een nl/en-paar: uit hu.json (sleutel = Engelse tekst)."""', '"""Roemeense tekst bij een nl/en-paar: uit ro.json (sleutel = Engelse tekst)."""'),
 ("if en in HUT: return HUT[en]", "if en in ROT: return ROT[en]"), ("if nl in HUT: return HUT[nl]", "if nl in ROT: return ROT[nl]"),
 ('o.get("hu")', 'o.get("ro")'), ('gidsen/hu.html"', 'gidsen/ro.html"'), ('"hu_basis.html"', '"ro_basis.html"'), ('"hu_final.json"', '"ro_final.json"'),
 ('t["hu"]', 't["ro"]'),
 ("LON0, LAT0, KX = 16.0, 48.65, 0.6801", "LON0, LAT0, KX = 20.1, 48.4, 0.6953"), ("PX(23.0, 0)", "PX(30.0, 0)"), ("PX(0, 45.65)", "PX(0, 43.5)"),
 ('aria-label="Kaart van Hongarije met', 'aria-label="Kaart van Roemenië met'),
 ('"Kaart van Hongarije met {len(LOCS_)} locaties met katachtigen","Map of Hungary with', '"Kaart van Roemenië met {len(LOCS_)} locaties met katachtigen","Map of Romania with'),
 ("r'(Map of Hungary with )", "r'(Map of Romania with )"), ('f"Magyarország térképe: {len(LOCS_)} hely vadmacskákkal"', 'f"Harta României: locații cu feline: {len(LOCS_)}"'),
 ("TX.HU_VERV", "TX.RO_VERV"),
 ('"Bevestigd", "Confirmed", "Megerősítve"', '"Bevestigd", "Confirmed", "Confirmat"'), ('"Onzeker", "Uncertain", "Bizonytalan"', '"Onzeker", "Uncertain", "Incert"'),
 ('"vermeldingen", "entries", "bejegyzés"', '"vermeldingen", "entries", "înregistrări"'),
 ('f"Magyarországon nem látható ({len(niet)} faj)"', 'f"Nu pot fi văzute în România (specii: {len(niet)})"'),
 ('f"Vadmacskákkal ({len(LOCS_)} hely)"', 'f"Cu feline (locații: {len(LOCS_)})"'),
 ('"Nem találtunk vadmacskát"', '"Nu am găsit feline"'), ('"A hivatalos állatkertlistáról"', '"Despre lista oficială a grădinilor zoologice"'),
 ('f"Útvonal {len(pre)} parkkal"', 'f"Traseu (parcuri: {len(pre)})"'),
 ('("hu", "-hu")', '("ro", "-ro")'),
 ('"(Hongarije: één pagina met de megyék)"', '"(Roemenië: één pagina met de județe)"'),
 ('"in Hongaarse dierenlocaties"', '"in Roemeense dierenlocaties"'), ('"in Hungarian zoos and animal parks"', '"in Romanian zoos and animal parks"'),
 ('"Waar te zien in Hongarije"', '"Waar te zien in Roemenië"'), ('"Where to see it in Hungary"', '"Where to see it in Romania"'),
 ('"Wilde katachtigen in Hongarije"', '"Wilde katachtigen in Roemenië"'), ('"Wild cats in Hungary"', '"Wild cats in Romania"'),
 ('niet te zien in Hongarije."', 'niet te zien in Roemenië."'), ('not on view in Hungary."', 'not on view in Romania."'),
 ('nu in Hongarije te zien?"', 'nu in Roemenië te zien?"'), ('seen in Hungary right now?"', 'seen in Romania right now?"'),
 ("<title>Wilde katachtigen in Hongaarse dierenlocaties — stand 23 oktober 2026", "<title>Wilde katachtigen in Roemeense dierenlocaties — stand 30 oktober 2026"),
 ('"Wild cats in Hungarian zoos and animal parks — updated 23 October 2026"', '"Wild cats in Romanian zoos and animal parks — updated 30 October 2026"'),
 ('f"Niet in Hongarije te zien ({len(niet)} soorten)", f"Not on view in Hungary ({len(niet)} species)"', 'f"Niet in Roemenië te zien ({len(niet)} soorten)", f"Not on view in Romania ({len(niet)} species)"'),
]
for a, b in R:
    assert a in s, a; s = s.replace(a, b)
s = re.sub(r'\bHUT\b', 'ROT', s)
s = re.sub(r'(R[1567]|SP)HU\b', r'\1RO', s); s = s.replace('ROUTENOTE_HU', 'ROUTENOTE_RO')
s = s.replace('["nl", "en", "hu"]', '["nl", "en", "ro"]')
s = s.replace('MISS, open(D + "hu_ontbreekt.json"', 'MISS, open(D + "ro_ontbreekt.json"').replace("ontbreekt hu:", "ontbreekt ro:")
open("ro/gen.py", "w").write(s)
left = [l for l in s.split("\n") if re.search(r'Hongar|Hungar|"hu"|\bhu\b|\bHU[A-Z_]|_HU\b|[őű]|Magyar', l)]
print("\n".join(x[:160] for x in left))
