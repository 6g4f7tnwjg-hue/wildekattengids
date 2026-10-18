# Overdracht (18 oktober 2026, laat op de avond)

Lees eerst `bron/LEESMIJ.md` (opbouw, bouw en de telregel), `bron/OPEN.md` (open punten) en bovenaan `VOORTGANG.md` (laatste wijzigingen).

## Waar we staan
- De hele site heeft één opbouw, gelijk aan de hoofdpagina:
  - Landpagina's: onderbalk Kaart · Locaties · Soorten · Meer. Het kaartscherm heeft regioknoppen, soortrondjes, de kaart met typeknoppen en "In beeld".
  - Hoofdpagina, top 10 en `/soort/…`: onderbalk Kaart · Landen · Soorten · Meer.
- Gemaakt in `bron/test_ontwerp.py`, dat aan het eind van `bron/bouw.py` draait (na `nieuw_ontwerp.py`). Bron per land is `/<land>-oud/`, de gebouwde gids zonder app-laag.
- Deze sessie: de hele site intern gecontroleerd (tellingen, teksten, links, alle talen op 390 px) en alles verbeterd wat afweek:
  - **Telregel** (staat in `LEESMIJ.md`): een getal bij een soort of locatie telt alleen bevestigde vermeldingen (g, y, b, r); onzekere staan er apart achter ("10 soorten · 1 onzeker"). Filterknoppen met een gekozen soort en "In beeld" tellen wat kaart en lijst tonen.
  - De groep "Onzeker" in de routeplanner (`UNSURE`) wordt in elke gids uit `R` berekend.
  - Alle gidsen hebben nu 43 soorten (ook Duitsland, Frankrijk, Oostenrijk, Zwitserland en het VK).
  - Typeknoppen volgen de gekozen regio; de hoofdpagina meldt de 17 locaties die niet op de kaart staan.
  - Vaste teksten met getallen bijgewerkt (België, Italië, Spanje, Ierland, Portugal, VK-regio's).
  - "Lijkt op"-links naar soorten zonder pagina in dat land gaan naar de Europese soortpagina.

- Later op 18-10-2026:
  - Op het scherm Meer van de landpagina's is het blok "Bezoekersgids" weg (kop en links). Dat staat in `MEER_NIEUW` in `test_ontwerp.py`. De links staan nog in het ☰-menu.
  - Locatiefoto's in de Nederlandse gids: Eindhoven Zoo (tijger, Cro-Cop) en Hoenderdaell (leeuw, Ingredia), beide CC BY 4.0, `img/265.webp` en `img/266.webp`.

## Let op bij volgende wijzigingen
- Vaste teksten in de gidsen (In het kort, regioblokken) bevatten getallen die met de hand zijn geschreven. Verandert een locatie of status, pas die zinnen dan in alle talen mee aan.
- De controlescripts van deze sessie staan niet in de repo. Ze vergeleken:
  - `extract.js`-gegevens met de gebouwde pagina's (Playwright, alle landen en talen);
  - de getallen in de vaste teksten met de gegevens.

## Werkwijze
- Bijwerken:
  1. Bron aanpassen in `bron/`.
  2. `python3 bron/bouw.py` draaien (±5 min; Playwright 1.56.0 en node nodig).
  3. Controleren op 390 px, in alle talen.
  4. Committen en pushen naar `main`. GitHub Pages is daarna binnen een paar minuten bij.
- Nooit de gegenereerde mappen in de hoofdmap met de hand aanpassen.
- Bij wachten op de bouw niet `pgrep -f "bron/bouw.py"` in dezelfde opdracht gebruiken: dat vindt zichzelf.
- De gebruiker (J. Gelens) wil:
  - Antwoorden in het Nederlands, kort.
  - Bij "wat stel je voor" alleen een voorstel, nog geen werk.
  - Alleen wijzigen wat gevraagd is.
  - Na elke update de link naar wat veranderd is.
  - Bij "vraag door" eerst vragen stellen, met keuzeknoppen.

## Afgesproken voor later
- Locatiefoto's Nederland: nog geen foto voor BestZoo (luipaard, jaguar, serval), Faunapark Flakkee, Taman Indonesia en Stichting AAP. Er zijn Commons-mappen "BestZoo" en "AAP (wildlife sanctuary)". Zoeken lukte niet goed: Wikimedia (API, Wikidata en afbeeldingen) gaf vanuit de cloud vaak 429. De gewone zoekpagina en `?action=raw` van een bestandspagina werkten wel. De gebruiker zoekt zelf mee en stuurt links. Controleer of de foto echt in dat park is gemaakt (een voorgestelde "Lioness from Perth Zoo" voor BestZoo is afgewezen).
- Foto's van parken in de locatiekaartjes.
- Desktopweergave: Locaties in twee kolommen met de kaart ernaast.
- Aantallen in het wild: twijfelgevallen staan in `bron/OPEN.md` (rode lynx, Euraziatische lynx, vissende kat, marmerkat). Pas invullen na een besluit.
- Nagaan, nog niet veranderd (zie `bron/OPEN.md`):
  - mogelijk dubbele geboortes in Dortmund (leeuw) en Whipsnade (cheetah);
  - Exotic Pet Refuge staat bij Oost-Engeland, maar ligt in Lincolnshire;
  - vier datums "sept 2026" in de Nederlandse gids.
- Overige open punten staan in `bron/OPEN.md`: top 10 met Spanje/Portugal/Italië, landen nalopen, enzovoort.
