# Landbouw: zo zijn Denemarken, Tsjechië, Zweden, Noorwegen, Finland, Polen en Hongarije gemaakt (en zo maak je het volgende land)

Per land een map (`dk/`, `cz/`, `se/`, `no/`, `fi/`, `pl/`) met alles waaruit de gids `bron/gidsen/<land>.html` gebouwd is. Na een wijziging in de gegevens: `python3 bron/landbouw/<land>/gen.py` (schrijft `bron/gidsen/<land>.html`) en daarna `python3 bron/bouw.py`.

## Bestanden per land

| Bestand | Wat |
|---|---|
| `OPDRACHT.md` | De opdracht voor de onderzoeksagenten (bronnenvolgorde, statussen, JSON-formaat). Kopiëren en aanpassen voor een nieuw land. |
| `*_resultaat.json` | Ruwe uitvoer van de onderzoeksagenten (per regio, lijsten, opvang, vervolg `vv*`). Alleen ter naslag. |
| `merge.py` | Voegt de regio-uitvoer samen tot `<land>_merged.json` en bepaalt de regio uit de coördinaten. CZ heeft `kaart/nuts3.geojson` nodig (niet in de repo, zie onder). |
| `patch.py` | Redactie: verwerkt de vervolgagenten, dubbelingen, weergavenamen, plaats, type, labels, vaste ondersoort-labels, geboortedatums → `<land>_final.json`. **Wijzig gegevens hier of in `_final.json`**. Let op: `patch.py` opnieuw draaien overschrijft `_final.json` (vanuit `_merged.json`, dat niet in de repo staat). Kleine updates dus direct in `_final.json` doen. |
| `<land>_final.json` | De gegevens van de gids (locaties, katten, geboortes, zonder katten, route). |
| `teksten.py` | Landspecifieke tekstblokken in NL/EN/derde taal: regio’s (`REGN`), kop/lede, In het kort, Geen katachtigen, officiële lijst, Aanbevelingen, Gepland, Kleurvarianten, Over (werkwijze, namen, verdwenen, bronnen). **Vaste getallen in deze teksten met de hand bijwerken.** |
| `<taal>.json` (`da.json`, `cs.json`) | Vertaaltabel van de gegevens: Engelse tekst → derde taal. Ontbrekende vertalingen schrijft `gen.py` naar `da_ontbreekt.json`. |
| `bron_vert.json` | Vertaling van de bronvermeldingen: Nederlands → [Engels, derde taal]. Ontbrekend → `bron_ontbreekt.json`. |
| `<land>_basis.html` | Het sjabloon: de gids met vaste teksten in de derde taal, maar zonder landgegevens. |
| `gen.py` | Bouwt de gids: sjabloon + `_final.json` + `teksten.py` + vertaaltabellen + `kaart/kaart.json`. |
| `kaart/kaart.json` | Kaart van de gids (`MAIN`, `ISLANDS`, `BUUR`, `LINES`), lengte/breedte; projectie staat in `gen.py` (`LON0`, `LAT0`, `KX`). |

## Een nieuw land (volgorde zoals bij Tsjechië, ±1 sessie)

1. **Voorstel en akkoord** van de gebruiker (land, talen: NL + EN + landstaal).
2. **Map** `bron/landbouw/<code>/`; `OPDRACHT.md` kopiëren en aanpassen (land, zoektermen in de landstaal, lidmaatschap van de landelijke zoobond).
3. **Onderzoek** met agenten, elk een eigen voorvoegsel en hulpmap: lijsten (officieel, zoobond, EAZA, Zootierliste per soort), 4–5 regio’s, opvang/particulieren/circussen. Daarna vervolgagenten voor gaten (vergelijk met de officiële lijst en Zootierliste) en zwakke vermeldingen. Afbakening die de gebruiker moet beslissen (circussen, particulieren zonder vergunning) vooraf voorleggen.
4. **Sjabloon**: neem `cz/cz_basis.html` (of `dk/dk_basis.html`; voor Zweden is dit gescript in `se/tools/basis_omzetten.py`, ook `html:not(.cs)` hernoemen), hernoem de taal in de code (`l-cs` → `l-xx`, `SPCS` → `SPXX`, `CSD` → `XXD`, `R1CS` …, `"cs"`, `html.cs`, ids `-cs`) met een script, en laat een vertaalagent de vaste teksten (niet de landblokken) naar de nieuwe taal vertalen.
5. **Gedeelde lagen**: een agent zet taal en land in `test_ontwerp.py`, `nieuw_ontwerp.py`, `huisstijl.py`, `jungle.py`, `locatietypes.js/json`, `taalmenu.js` (achteraan in elke talenlijst; zie de commits van Deens en Tsjechisch). Zelf: `bouw.py` (`F`, `LAND`, `NOTE`, `RPTXT`, `GTAAL`, `CTRY`, landenlijsten in titels), `startdata.py` (`GTAAL`), `start.html` (regex-landenlijsten, `C`, `ORDER`, `FLAG`, `LBL`, kaartlijsten, `D.<code>.poly`, landenlijsten in zeven talen, eventueel `FULL`/viewBox en buurlanden `NBR`).
6. **Kaart**: `python3 bron/landbouw/kaart_maken.py <map> <LANDCODE> <2|3> lon0 lat0 lon1 lat1 BUREN` (GISCO NUTS 2024, 1:3 miljoen; vereist `pip install shapely`). Het script print de waarden voor `LON0`, `LAT0`, `KX` en de randen in `gen.py`. Voor de regio van elke locatie: `merge.py` (punt-in-polygoon op dezelfde NUTS-bestanden).
7. **Gegevens**: `merge.py` → `patch.py` (redactie) → `gen.py` → ontbrekende vertalingen laten vertalen (`*_ontbreekt.json` → `<taal>.json`, `bron_vert.json`) → `gen.py` opnieuw.
8. **Bouwen en controleren**: `python3 bron/bouw.py`; andere landen tekst voor tekst vergelijken met de vorige versie (twee lokale servers, Playwright), de nieuwe pagina in alle talen op 390/414 px, scan op resten van de vorige taal.
9. **Documentatie**: `TWIJFELGEVALLEN.md`, `VOORTGANG.md`, `bron/OPEN.md`, `bron/LEESMIJ.md`, `bron/OVERDRACHT.md`; daarna committen en naar `main` pushen.
