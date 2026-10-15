# Bron van de Wilde katachtigen-gids

Alles wordt uit deze map gebouwd. Pas nooit de gegenereerde bestanden in de hoofdmap aan
(`index.html`, `soort/`, `top10/`, `nederland/`, `belgie/`, `luxemburg/`, `duitsland/`, `frankrijk/`, `oostenrijk/`, `zwitserland/`, `verenigd-koninkrijk/`, `italie/`, `spanje/`, `ierland/`, `sitemap.xml`): die worden bij elke bouw overschreven.

## Wat staat waar

| Bestand | Inhoud |
|---|---|
| `gidsen/nl.html`, `be.html`, `lu.html`, `de.html`, `fr.html`, `at.html`, `ch.html`, `uk.html`, `it.html`, `es.html`, `ie.html` | De landengidsen. Alle gegevens (soorten, waarnemingen `R`, locaties `LOCS`, jongen `YOUNG`) staan in het script van de gids; Duitsland, Frankrijk, Oostenrijk, Zwitserland en het VK hebben één blok per deelstaat of regio, Italië, Spanje en Ierland zijn één pagina met een filter per regio (`REGIO`, `REGN`; Spanje per autonome gemeenschap, Ierland per provincie). Talen (regel: Nederlands, Engels en de landstaal of -talen): NL/EN (Nederland, VK, Ierland), NL/EN/FR (België, Frankrijk), NL/EN/DE (Duitsland, Oostenrijk), NL/EN/FR/DE (Luxemburg), NL/EN/DE/FR/IT (Zwitserland), NL/EN/IT (Italië), NL/EN/ES (Spanje). Een gids met één derde taal gebruikt `T(nl,en,x)` en `l-x`-elementen; Zwitserland en Luxemburg gebruiken de taaltabel `LGS` (`T(nl,en,...)` in de volgorde van `LGS`, woordenlijsten per taal zoals `SPFR`, `R5IT`, `ITD`). Foto's staan erin als `@@IMGn@@`. |
| `start.html` | De startpagina. De gegevens in `const D` (kaartstippen, aantallen, recente geboortes) worden bij elke bouw opnieuw berekend uit de gidsen. Kaartvormen en de deelstaat-notitie blijven staan. Talen: Nederlands, Engels, Frans, Duits, Italiaans en Spaans (`T(nl,en,fr,de,it,es)` en `l-fr`/`l-de`/`l-it`/`l-es`-elementen). Onder de titel staat een regel met aantallen (landen · locaties · soorten), berekend uit `D`. |
| `../img/` | Alle foto's; `n.webp` hoort bij `@@IMGn@@`. Nieuwe foto: volgend nummer toevoegen. |
| `artifact_kop.html`, `web_kop.html` | Vaste kopjes voor de Claude-pagina en de website. |
| `top10.json` | De top 10 om te bezoeken (blok op de startpagina en pagina `/top10/`, op de Claude-pagina `#top10`). `vast` staat in die volgorde bovenaan, met de uitleg in zes talen (nl, en, fr, de, it, es); is de lijst korter dan 10 of verdwijnt een park uit de gids, dan vult de bouw aan op score. Volgorde of uitleg veranderen: alleen dit bestand aanpassen. |
| `franse_namen.json`, `duitse_namen.json`, `italiaanse_namen.json`, `spaanse_namen.json` | Franse, Duitse, Italiaanse en Spaanse soortnamen voor de startgegevens. |
| `taalmenu.js` | Het taalmenu (wereldbol met de taalcode; de lijst toont de talen van de pagina in hun eigen naam). De bouw zet het in de startpagina en in elke gids. |
| `locatietypes.json` | De vaste lijst van locatietypes en labels. Elke locatie heeft in `LOCINFO` één `type` (de namen uit deze lijst) en `labels` (sleutels uit deze lijst). Dierentuin = lid van EAZA, NVD, VdZ, UIZA, AIZA of BIAZA; anders dierenpark. |
| `locatietypes.js` | Filterknoppen, labels en types in de gidsen; de bouw zet dit achter het script van elke gids en deelstaat. |
| `bouw.py`, `startdata.py`, `extract.js` | De bouw. Deelstaten en regio’s staan in `STATES` en `REGIOS` in `bouw.py` (samen `DEEL`). |

## Bijwerken

1. Pas de gids aan in `bron/gidsen/…`.
2. Bouw: `python3 bron/bouw.py` (vereist node en Python met playwright; duurt een paar minuten door de losse pagina's). In de Claude-cloudomgeving: `pip install playwright==1.56.0`, want die versie past bij de Chromium in `/opt/pw-browsers` (chromium-1194); de nieuwste Playwright zoekt een andere browser.
3. Controleer `git diff`, commit en push → de website (https://yeetkitty.github.io/wildekattengids/) is binnen een paar minuten bij.
4. Publiceer `_claude/claude.html` als update van de Claude-pagina
   (https://claude.ai/code/artifact/6d4b4553-65b1-4dc3-82b1-41c087dcc110), met als `files` de inhoud van
   `_claude/bestanden.json` (de foto's, `img/n.webp`). Alleen gewijzigde of nieuwe foto's hoeven mee; de rest blijft staan.

Alleen de Claude-pagina bouwen: `python3 bron/bouw.py --geen-web`.

## Verschillen tussen de twee versies (worden door de bouw toegevoegd)

- Website: elk land, elke deelstaat en elke regio heeft een eigen adres, met zoektitel, beschrijving en deelvoorbeeld; elke soort en locatie heeft een eigen, vaste pagina (momentopname van de gids); foto's als losse bestanden; sitemap.
- Website: elke soort heeft ook een pagina voor alle landen samen (`/soort/<naam>/`); in de Claude-pagina opent die binnen de startpagina (`#kat/<naam>`). De gegevens staan in `D.sp` (berekend door `startdata.soorten`).
- Website: het meldformulier verstuurt via Web3Forms naar de mail van de maker. De Claude-pagina gebruikt de reacties van Claude.
- Claude-pagina: één pagina; de landen worden binnen de pagina geopend.
- Claude-pagina: de foto's staan er niet in, maar worden als losse bestanden (`img/n.webp`, op volle kwaliteit) met de pagina meegepubliceerd. De pagina zelf mag maximaal 16 MB zijn; daar telt nu alleen tekst en gegevens mee (de bouw stopt boven 15,8 MB).
- Claude-pagina: de landgidsen staan gecomprimeerd (gzip) in de pagina en worden pas uitgepakt als je een land opent (DecompressionStream). Losse bestanden ernaast laden werkt niet: de Claude-omgeving blokkeert eigen scripts en het ophalen van bestanden. Zo blijft de pagina ruim onder 16 MB.

## Een taal of land toevoegen: lessen (oktober 2026)

- **Twee soorten vertaalde tekst.** Een gids heeft losse zinnen per taal (`<span class="l-xx">`) én hele tekstblokken per taal (`<div class="l-xx">`, bijv. “In het kort”, de uitleg en de bronnen). Wie een taal toevoegt, moet beide vertalen; anders blijven die secties in de nieuwe taal leeg. Geef de id’s in een gekopieerd blok de nieuwe taal (`werkwijze-fr` → `werkwijze-de`), anders staan ze dubbel.
- **Meer dan drie talen.** Een gids met één derde taal gebruikt `T(nl,en,x)`. Voor meer talen gebruikt de gids de taaltabel `LGS` (zoals Zwitserland en Luxemburg): `T(nl,en,...)` in de volgorde van `LGS`, woordenlijsten per taal (`SPFR`, `R5IT`, `ITD` enz.) en vakken van drie of meer teksten in de gegevens (`LOCINFO`, `TWX`, `YOUNG`). Volg dat model voor een nieuwe taal in een andere gids.
- **Vertalingen hergebruiken.** Vertalingen uit andere gidsen overnemen (op de Engelse tekst als sleutel) scheelt veel werk, maar bij korte woorden ging het mis: een bronnotitie in de Franse gids gaf “visit” in plaats van “visite”, en maandnamen stonden er in het Engels. Geef voorrang aan de woordenlijst (`FRD`, `DED` enz.) en vaste teksten boven bronnotities (`SRC_GL`), en controleer vertalingen die gelijk zijn aan het Engels.
- **Elke taal testen.** Open elke gids in elke taal op 375 px en kijk of er geen foutmeldingen zijn, of er niets breder is dan het scherm en of de secties gevuld zijn. Een taalwissel kan stil mislukken als de code een woordenlijst te vroeg leest.
- **Nieuw land met één pagina en regio’s** (zoals Italië): neem de Belgische gids als basis (één pagina met groepen per provincie) en voeg een regiofilter toe. Locaties zonder vaste plek (reizende circussen) krijgen geen coördinaten; de kaart van de gids en van de startpagina slaan ze over.
- **Startpagina en een nieuw land**: landcode in `F`/`LAND` (bouw.py) en in `C`, `ORDER`, `FLAG`, de kleuren (`--c-xx`, `--t-xx`), de kaartlijsten en de routeringsregels van `start.html`; een kaartvorm in `D[xx].poly`; en het kaartkader (`FULL`) groter maken als het land buiten het kader valt. Ook de landenlijsten in titels en beschrijvingen (in vijf talen) aanpassen.
- **Onderzoek met meerdere agenten.** Geef elke agent een eigen naamvoorvoegsel voor zijn bestanden; parallelle agenten overschreven elkaars bestanden met dezelfde naam. Agenten lopen tegen de grens van 200 zoekopdrachten aan: verdeel het land in kleinere regio’s en start een vervolgagent voor wat is blijven liggen.

## Spanje toevoegen: lessen (oktober 2026)

- **Een gids afleiden van een bestaande gids.** De Spaanse gids is gemaakt door de Italiaanse gids om te zetten met een script: eerst de taal (alle `l-it`-teksten, de taaltabellen `SPIT`→`SPES`, `ITD`→`ESD` enz., en het derde argument van `T()` naar het Spaans), daarna de gegevens (`R`, `LOCS`, `LOCINFO`, `REGIO`, `REGN`, `TWX`, `YOUNG` …) en tot slot de vaste tekstblokken (In het kort, lijsten, aanbevelingen, kleurvarianten, uitleg). Let op: hele tekstblokken (`<div class="l-xx">`) worden niet door een vertaaltabel geraakt en moeten allemaal opnieuw geschreven worden.
- **Franse resten in de Italiaanse gids**: het derde argument van `T()` bevatte op een paar plekken Frans. Controleer bij een nieuwe taal alle `T()`-aanroepen met drie of meer argumenten.
- **Zesde taal op de hoofdpagina**: alle 87 `T()`-aanroepen kregen een zesde argument, plus `l-es`-teksten, `C[land].es`, `STAT`, `kname` (soortnaam index 11), `MND.es` en de datumnotatie (“15 de octubre de 2026”). `startdata.py` levert de Spaanse soortnamen op index 7 (per locatie) en 11 (per soort).
- **Kaart zonder eilanden**: op verzoek staan de Balearen en de Canarische Eilanden niet op de kaarten; die locaties hebben geen coördinaten in `LOCS` (zoals reizende circussen) en staan wel in de lijst en het regiofilter. Kaartvorm en regiogrenzen komen uit Natural Earth (50m) en de grenzen van de comunidades (click_that_hood), vereenvoudigd.
- **Onderzoek**: zes regio-agenten plus vier vervolgagenten. Elke agent schreef een eigen bestand (`and_`, `cat_`, `val_`, `mad_`, `nrd_`, `can_`, `vv1_`–`vv4_`) in hetzelfde JSON-formaat; een samenvoegscript koppelde ze op naam en coördinaten. Daarna redactie en vertaling (NL/EN/ES) door twee agenten, met de Nederlandse tekst als sleutel van de vertaaltabellen.

## Ierland toevoegen: lessen (oktober 2026)

- **Een derde taal eruit halen.** De Ierse gids (NL/EN) is met een script afgeleid van de Spaanse: eerst alle `l-es`-elementen en `-es`-blokken weg (met een tellende verwijderfunctie, want blokken zijn genest), `LGS` naar `["nl","en"]` en de Spaanse tabellen (`SPES`, `ESD`, `R1ES` …) leeg. Daarna de gegevens (`R`, `LOCS`, `LOCINFO`, `REGIO`, `REGN`, `TWX`, `YOUNG` …) en de vaste tekstblokken. Het script en de gegevens staan niet in de repo; zie de werkwijze in `VOORTGANG.md`.
- **Een buurland op de kaart.** Noord-Ierland staat grijs op de kaart van de gids (`NI`, klasse `buur`), zodat de grens duidelijk is; het kaartkader (`viewBox`) moet dan ook Noord-Ierland omvatten. Op de startpagina hoort Noord-Ierland bij de vorm van het VK.
- **Lege provincie.** Een provincie zonder locaties met katten (Connacht) krijgt geen kop in de lijst en geen chip in het filter; zet de locaties zonder katten wel in “Geen katachtigen gevonden”.
- **Link naar een andere landgids.** Binnen een gids werkt een relatieve link naar een ander land niet in de Claude-pagina; gebruik de volledige website-URL met `target="_blank"`.
- **Kaartkader op de startpagina.** Bij een land verder naar het westen: `LON0` in `start.html` lager zetten en `FULL[2]` met hetzelfde aantal pixels vergroten (`(oud−nieuw)·K`, K = 0,623·60).
- **Welpennamen in `YOUNG.n`.** Zet in `n` alleen het aantal (“2 welpen”); namen en geslacht in `x`. De startpagina vertaalt `n` met vaste regels naar FR/DE/IT/ES, en een zin met namen wordt half vertaald.
- **Weinig locaties, veel “geen katten”.** In Ierland zijn er 7 locaties met katten en 73 zonder. De officiële lijst (2022) bestond vooral uit roofvogelcentra, open farms en aquaria; ook die zijn allemaal nagelopen en in de lijst gezet.

