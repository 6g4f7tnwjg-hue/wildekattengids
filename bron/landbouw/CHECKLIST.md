# Checklist: een nieuw land (vanaf november 2026)

**Eén land = één nieuw gesprek.** Begin met: “Lees `bron/OVERDRACHT.md` en `bron/landbouw/CHECKLIST.md`; we doen <land>.”
Kopieer deze lijst naar `bron/landbouw/<code>/STAPPEN.md` en vink af (`[x]`) en commit na elke stap. Zo kan een volgend gesprek precies verder waar dit stopte.
Details per stap: `bron/landbouw/LEESMIJ.md`. Voorbeeld: `bron/landbouw/ro/` (meest recent).

## 0. Afspraken
- [ ] Werktak `<land>-wip` vanaf `main`.
- [ ] Afbakening is vast (zoals CZ/PL/HU/RO): particulieren en circussen met kanttekening, status volgens toegang; **geen namen van particulieren**; locaties alleen uit politieberichten (zonder plaats of toegang) niet opnemen. Alleen voorleggen als het land iets bijzonders heeft.
- [ ] Talen: NL + EN + landstaal.

## 1. Onderzoek (zuinig)
- [ ] `OPDRACHT.md` kopiëren van het vorige land en aanpassen (land, datum, zoektermen, zoobond, afbakening).
- [ ] **Drie** onderzoeksagenten, **model `sonnet`**, elk eigen voorvoegsel; taken niet laten overlappen:
  1. `lst`: officiële lijst (vergunningen), zoobond, EAZA, **Zootierliste per soort** (alleen deze agent doet Zootierliste), wetgeving (particulieren, circussen).
  2. `aa`: eerste helft van het land (regio’s noemen), inclusief particulieren, opvang en circussen in die regio’s.
  3. `bb`: tweede helft, idem.
- [ ] `merge.py` → controleer tegen de officiële lijst en Zootierliste: welke vergunde parken ontbreken?
- [ ] **Vervolgagent alleen bij echte gaten** (ontbrekende vergunde parken, of veel `w` bij grote parken); ook `sonnet`. Eén ronde.
- [ ] Ruwe uitvoer committen.

## 2. Sjabloon en gedeelde lagen
- [ ] `tools/basis_omzetten.py` afleiden van het vorige land; `<taal>_todo.json` laten vertalen (agent, `sonnet`).
  - Let op: een `const`-string (zoals `TITLE_XX`) moet in `<taal>_vast.json` als JSON-string mét aanhalingstekens.
  - Let op: `replace('"hu"', …)` raakt ook `<p class="pl">` (CSS-klasse, geen taal); uitzonderen.
- [ ] `tools/gen_omzetten.py` → `gen.py`.
- [ ] Gedeelde lagen (één agent, voorbeeld: de commits van het vorige land): `test_ontwerp.py`, `nieuw_ontwerp.py` (`LANDEN`!), `huisstijl.py`, `jungle.py` (getalvormen, landnaam na getal), `locatietypes.js/json`, `taalmenu.js`, `bouw.py`, `startdata.py`, `start.html` (poly, lijsten in 7 talen, kaartkader).
- [ ] Kaart: `kaart_maken.py` (landen buiten NUTS, zoals Moldavië: Natural Earth).

## 3. Redactie (zelf, zwaar model)
- [ ] `patch.py`: dubbelingen, weergavenamen, type (dierentuin = EAZA/zoobond, of vergunning als er geen ledenlijst is), labels, ondersoort alleen met bron, geboortes binnen de groeigrens (Felinae 1 jaar, Pantherinae 2 jaar).
- [ ] **Privacy-scan**: geen persoonsnamen bij particulieren; geen beschuldigingen, alleen feiten (`grep` op eigenaar/owner/familie in `_final.json`).
- [ ] `zonder_katten`: ontdubbelen op volledige naam (niet op een voorvoegsel zoals “Grădina Zoologică”).
- [ ] `teksten.py` (getallen narekenen met een script, niet uit het hoofd).
- [ ] `gen.py` → ontbrekende vertalingen (agent, `sonnet`) → `gen.py` → “ontbreekt: 0”.

## 4. Controle (één keer, aan het eind)
- [ ] `python3 bron/controle/jscheck.py bron/gidsen/<code>.html` → 0 JS-fouten.
- [ ] `python3 bron/bouw.py` (±6 min); in het log: “testontwerp geschreven: <land>/index.html”.
- [ ] `bash bron/controle/servers.sh` (8101 = main, 8102 = werkmap).
- [ ] `python3 bron/controle/landtest.py <land> nl,en,<taal> "<2 locaties, 1 soort>" "<woorden van de vorige taal>"` → 0 afwijkingen. Bekijk minstens 3 schermafdrukken (`bron/controle/uit/shots/`): start, een locatie, een soort, in de landstaal.
- [ ] Ook op laptopbreedte (1366 px) één blik: kop, menubalk onderaan, pijltjes.
- [ ] `python3 bron/controle/vergelijk.py <land> <land>-oud` → alleen verwachte verschillen (tellingen, landenlijsten). Duitse soort-doorverwijzingen haperen soms: `--opnieuw`.
- [ ] Eén bouw na de laatste wijziging; daarna niets meer veranderen zonder opnieuw te testen.

## 5. Afronden
- [ ] Documentatie: `VOORTGANG.md`, `TWIJFELGEVALLEN.md`, `bron/OPEN.md`, `bron/LEESMIJ.md` (lessen), `bron/OVERDRACHT.md`.
- [ ] Commit en push `<land>-wip`; kort verslag aan de gebruiker met de link; vragen: “Mag ik <land> naar `main` zetten?”
- [ ] Na akkoord: `git push origin HEAD:main` (fast-forward); live-link geven.

## Onderhoud (apart gesprek, geen nieuw land)
Af en toe één gesprek dat alleen `bron/OPEN.md` afwerkt: open vragen aan de gebruiker, “nagaan”-lijsten per land (kort, met `sonnet`), WebKit/Safari-test, kaartfouten.
