# Eenmalig: cz/gen.py -> se/gen.py
import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../..")
s=open('cz/gen.py').read()
R=[("bron/gidsen/cz.html uit cz_basis.html (Tsjechische vaste teksten) + cz_final.json","bron/gidsen/se.html uit se_basis.html (Zweedse vaste teksten) + se_final.json"),
('CS = json.load(open(D + "cs.json", encoding="utf8")) if __import__("os").path.exists(D + "cs.json") else {}','SV = json.load(open(D + "sv.json", encoding="utf8")) if __import__("os").path.exists(D + "sv.json") else {}'),
('"""Tsjechische tekst bij een nl/en-paar: uit cs.json (sleutel = Engelse tekst)."""','"""Zweedse tekst bij een nl/en-paar: uit sv.json (sleutel = Engelse tekst)."""'),
("if en in CS: return CS[en]","if en in SV: return SV[en]"),("if nl in CS: return CS[nl]","if nl in SV: return SV[nl]"),
('o.get("cs")','o.get("sv")'),('gidsen/cz.html"','gidsen/se.html"'),('"cz_basis.html"','"se_basis.html"'),('"cz_final.json"','"se_final.json"'),
('t["cs"]','t["sv"]'),
("LON0, LAT0, KX = 11.8, 51.25, 0.6455","LON0, LAT0, KX = 10.9, 69.1, 0.4668"),("PX(19.15, 0)","PX(24.25, 0)"),("PX(0, 48.35)","PX(0, 55.25)"),
('aria-label="Kaart van Tsjechië met','aria-label="Kaart van Zweden met'),
('f\'T("Kaart van Tsjechië met {len(LOCS_)} locaties met katachtigen","Map of Czechia with {len(LOCS_)} l\'','f\'T("Kaart van Zweden met {len(LOCS_)} locaties met katachtigen","Map of Sweden with {len(LOCS_)} l\''),
("r'(Map of Czechia with )","r'(Map of Sweden with )"),('f"Mapa Česka s {len(LOCS_)} místy s kočkovitými šelmami"','f"Karta över Sverige med {len(LOCS_)} platser med kattdjur"'),
("TX.CS_VERV","TX.SV_VERV"),
('"Bevestigd", "Confirmed", "Potvrzeno"','"Bevestigd", "Confirmed", "Bekräftade"'),('"Onzeker", "Uncertain", "Nejisté"','"Onzeker", "Uncertain", "Osäkra"'),
('"vermeldingen", "entries", "záznamů"','"vermeldingen", "entries", "uppgifter"'),
('f"V Česku k vidění nejsou ({len(niet)} druhů)"','f"Går inte att se i Sverige ({len(niet)} arter)"'),
('f"S kočkovitými šelmami ({len(LOCS_)} míst)"','f"Med kattdjur ({len(LOCS_)} platser)"'),
('"Žádné kočkovité šelmy nenalezeny"','"Inga kattdjur hittades"'),('"O oficiálním seznamu zoologických zahrad"','"Om den officiella listan över djurparker"'),
('f"Trasa s {len(pre)} parky"','f"Rutt med {len(pre)} parker"'),
('("cs", "-cs")','("sv", "-sv")'),
("\"(Tsjechië: één pagina met de veertien kraje)\"","\"(Zweden: één pagina met de län)\""),
('"in Tsjechische dierenlocaties"','"in Zweedse dierenlocaties"'),('"in Czech zoos and animal parks"','"in Swedish zoos and animal parks"'),
('"Waar te zien in Tsjechië"','"Waar te zien in Zweden"'),('"Where to see it in Czechia"','"Where to see it in Sweden"'),
('"Wilde katachtigen in Tsjechië"','"Wilde katachtigen in Zweden"'),('"Wild cats in Czechia"','"Wild cats in Sweden"'),
('niet te zien in Tsjechië."','niet te zien in Zweden."'),('not on view in Czechia."','not on view in Sweden."'),
('nu in Tsjechië te zien?"','nu in Zweden te zien?"'),('seen in Czechia right now?"','seen in Sweden right now?"'),
("<title>Wilde katachtigen in Tsjechische dierenlocaties","<title>Wilde katachtigen in Zweedse dierenlocaties"),
('"Wild cats in Czech zoos and animal parks — updated','"Wild cats in Swedish zoos and animal parks — updated'),
('f"Niet in Tsjechië te zien ({len(niet)} soorten)", f"Not on view in Czechia ({len(niet)} species)"','f"Niet in Zweden te zien ({len(niet)} soorten)", f"Not on view in Sweden ({len(niet)} species)"'),
]
for a,b in R:
    assert a in s,a; s=s.replace(a,b)
s=re.sub(r'\bCS\b','SV',s)
s=re.sub(r'(R[1567]|SP)CS\b',r'\1SV',s); s=s.replace('ROUTENOTE_CS','ROUTENOTE_SV')
s=s.replace('["nl", "en", "cs"]','["nl", "en", "sv"]')
s=s.replace('MISS, open(D + "da_ontbreekt.json"','MISS, open(D + "sv_ontbreekt.json"').replace("ontbreekt da:","ontbreekt sv:")
open('se/gen.py','w').write(s)
left=[l for l in s.split('\n') if re.search(r'Tsjech|Czech|Česk|[ěščřžůň]|"cs"|\bcs\b|CS',l)]
print('\n'.join(x[:160] for x in left))
