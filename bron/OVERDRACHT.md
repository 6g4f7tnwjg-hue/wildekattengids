# Overdracht (18 oktober 2026, avond)

Lees eerst `bron/LEESMIJ.md` (opbouw en bouw), `bron/OPEN.md` (open punten) en bovenaan `VOORTGANG.md` (laatste wijzigingen).

## Waar we staan
- De hele site heeft één opbouw, gelijk aan de hoofdpagina:
  - Landpagina's: onderbalk Kaart · Locaties · Soorten · Meer. Het kaartscherm heeft regioknoppen, soortrondjes, de kaart met typeknoppen en "In beeld".
  - Hoofdpagina, top 10 en `/soort/…`: onderbalk Kaart · Landen · Soorten · Meer.
- Gemaakt in `bron/test_ontwerp.py`, dat aan het eind van `bron/bouw.py` draait (na `nieuw_ontwerp.py`). Bron per land is `/<land>-oud/`, de gebouwde gids zonder app-laag.
- Deze sessie toegevoegd:
  - Wat niet samengaat wordt grijs en schuift achteraan (land/regio ↔ soort), met een melding.
  - Zoekveld boven Locaties en Soorten.
  - Favorieten voor alle landen samen op de hoofdpagina (`#favorieten`, localStorage `nt-fav`).
  - Meer op de hoofdpagina is een eigen scherm (`#meer`).
  - Volgorde van Meer op de landpagina's: In het kort, Actueel, Kleur & hybriden, Routeplanner, Hoofdtabel, Over, Rapporteer.
  - Routeplanner "Al wel:".
  - Foto van een zwarte panter bij Kleur & hybriden.
  - Balearen op de kaarten; de Canarische Eilanden bewust niet, met een melding op de kaart.
  - De kaart zoomt in op een gekozen regio.
  - IUCN-status vervangen door "In het wild (geschat)", nu ook ingevuld voor Geoffroy's kat en zandkat.

## Werkwijze
- Bijwerken:
  1. Bron aanpassen in `bron/`.
  2. `python3 bron/bouw.py` draaien (±5 min; Playwright 1.56.0 en node nodig).
  3. Controleren op 390 px, in alle talen.
  4. Committen en pushen naar `main`. GitHub Pages is daarna binnen een paar minuten bij.
- Nooit de gegenereerde mappen in de hoofdmap met de hand aanpassen.
- De gebruiker (J. Gelens) wil:
  - Antwoorden in het Nederlands, kort.
  - Bij "wat stel je voor" alleen een voorstel, nog geen werk.
  - Alleen wijzigen wat gevraagd is.
  - Na elke update de link naar wat veranderd is.
  - Bij "vraag door" eerst vragen stellen, met keuzeknoppen.

## Afgesproken voor later
- Foto's van parken in de locatiekaartjes.
- Desktopweergave: Locaties in twee kolommen met de kaart ernaast.
- Aantallen in het wild: de twijfelgevallen staan in `bron/OPEN.md` (rode lynx, Euraziatische lynx, vissende kat, marmerkat). Pas invullen na een besluit.
- Overige open punten staan in `bron/OPEN.md`: top 10 met Spanje/Portugal/Italië, landen nalopen, enzovoort.
