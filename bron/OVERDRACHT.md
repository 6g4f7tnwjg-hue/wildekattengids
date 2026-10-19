# Overdracht (19 oktober 2026, nacht)

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

## Jungle-stijl (18–19 oktober 2026)
- De hele site (743 pagina's, behalve `/spottersgids/`, `/<land>-oud/` en `/voorbeeld-jungle/`) heeft de jungle-stijl "Expeditie". Alles staat in **`bron/jungle.py`**, dat als allerlaatste stap van `bouw.py` draait. Het zet één blok `<!--jungle-->…<!--/jungle-->` (lettertypen, CSS en een paar kleine scripts) vóór `</body>`; de inhoud van de pagina's blijft ongewijzigd.
- Terugdraaien: `python3 bron/jungle.py --weg` en de regel onderaan `bouw.py` weghalen. Reservekopie van vóór de jungle-stijl: tak `backup-voor-jungle`.
- Controle na elke wijziging: pagina's zonder het jungle-blok moeten exact gelijk zijn aan de versie ervoor (vingerafdruk per pagina). Daarnaast een tik-test op 414 px (onderbalk, Meer-subpagina's, terugknop) én een "rust"-meting: na het tikken mogen er geen doorlopende DOM-wijzigingen zijn.
- Wat de stijl doet:
  - Kleuren: donker junglegroen `#143A22`, goudgeel `#F2C14E`, lichtgroene achtergrond met vage luipaardvlekken. Letters: Anton (koppen, hoofdletters) en Nunito (tekst).
  - Groene koppen met monsterablad en golfrand. Op de landpagina's zijn de koppen van Kaart, Locaties, Soorten, Meer en alle Meer-subpagina's (In het kort, Actueel, Kleur & hybriden, Routeplanner, Hoofdtabel, Over, Rapporteer) exact even hoog en gelijk opgebouwd: vlag + titel, lichte regel, goudgele regel (teksten in `KOP_JS`, per scherm vooraf klaargezet en met CSS `:has(#…​.nw-cur)` getoond, zodat er niets verspringt). Lange titels worden kleiner gemaakt in plaats van afgekapt.
  - Soort- en parkpagina's binnen een land (`#soort/…`, `#locatie/…` en de losse pagina's): één groene kop (`DETAIL_JS`), foto eronder, hartje rond op de foto. De losse pagina's krijgen vlag, landnaam en hartje via `window.__JGLOS` (`los_js()`, 19-10).
  - Zwevende gele terugknop linksonder (`.jg-terug`), alleen op Meer-subpagina's en detailpagina's; gaat terug naar Soorten/Locaties of klikt de bestaande terugknop.
  - Knoppen (landen, filters, typen, regio's) in stijl A "bladgroen" (19-10, vervangt het hout): `KNOP`/`KNOP_AAN`. Bolletjes voor de lijsten "Waar te zien" en "Katten hier".
  - Scherm Locaties (19-10): losse kaartjes met goudgele badge en soortrondjes (`kaartje()` in `test_ontwerp.py`); de lijst "In beeld" op het kaartscherm is ongewijzigd.
  - Voet als horizontale tak (19-10, `TAK_JS`/`TAK_CSS`): Ko-fi-tekst op de tak, luipaard ligt erop. Getekende luipaard (ronde groene ogen met wimpers, snorharen, knipperen, kop kantelt, staart zwiept; tik = opkijken). Tekening in `svg()`/`oog()` in `jungle.py`.
- **Les:** gebruik geen MutationObserver die op `class`-wijzigingen in `#main` reageert en dan zelf HTML schrijft. Dat gaf een oneindige lus en de site reageerde niet meer op tikken (19-10, direct teruggedraaid). Teksten nu vooraf bouwen en alleen met CSS wisselen.
- Bekend, niet door de stijl: op de kaart van Frankrijk, Duitsland en Spanje is de site zelf continu bezig (ook zonder jungle-laag). Tikken werkt, maar het kost mogelijk batterij. Nog niet uitgezocht.
- Testpagina's (noindex, niet gelinkt): `/voorbeeld-jungle/` (drie stijlvoorbeelden, `test/` per paginasoort, `ogen/`).

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
- Spottersgids later ook in de jungle-stijl (gebruiker: "kan later").
- Locatiefoto's Nederland: nog geen foto voor BestZoo (luipaard, jaguar, serval), Faunapark Flakkee, Taman Indonesia en Stichting AAP. Er zijn Commons-mappen "BestZoo" en "AAP (wildlife sanctuary)". Zoeken lukte niet goed: Wikimedia (API, Wikidata en afbeeldingen) gaf vanuit de cloud vaak 429. De gewone zoekpagina en `?action=raw` van een bestandspagina werkten wel. De gebruiker zoekt zelf mee en stuurt links. Controleer of de foto echt in dat park is gemaakt (een voorgestelde "Lioness from Perth Zoo" voor BestZoo is afgewezen).
- Foto's van parken in de locatiekaartjes.
- Desktopweergave: Locaties in twee kolommen met de kaart ernaast.
- Aantallen in het wild: twijfelgevallen staan in `bron/OPEN.md` (rode lynx, Euraziatische lynx, vissende kat, marmerkat). Pas invullen na een besluit.
- Nagaan, nog niet veranderd (zie `bron/OPEN.md`):
  - mogelijk dubbele geboortes in Dortmund (leeuw) en Whipsnade (cheetah);
  - Exotic Pet Refuge staat bij Oost-Engeland, maar ligt in Lincolnshire;
  - vier datums "sept 2026" in de Nederlandse gids.
- Overige open punten staan in `bron/OPEN.md`: top 10 met Spanje/Portugal/Italië, landen nalopen, enzovoort.
