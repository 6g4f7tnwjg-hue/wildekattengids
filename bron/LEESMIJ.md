# Bron van de Wilde katachtigen-gids

Alles wordt uit deze map gebouwd. Pas nooit de gegenereerde bestanden in de hoofdmap aan
(`index.html`, `soort/`, `top10/`, `nederland/`, `belgie/`, `luxemburg/`, `duitsland/`, `frankrijk/`, `oostenrijk/`, `zwitserland/`, `verenigd-koninkrijk/`, `italie/`, `spanje/`, `ierland/`, `portugal/`, `denemarken/`, `sitemap.xml`): die worden bij elke bouw overschreven.

## Wat staat waar

| Bestand | Inhoud |
|---|---|
| `gidsen/nl.html`, `be.html`, `lu.html`, `de.html`, `fr.html`, `at.html`, `ch.html`, `uk.html`, `it.html`, `es.html`, `ie.html`, `pt.html`, `dk.html` | De landengidsen. Alle gegevens (soorten, waarnemingen `R`, locaties `LOCS`, jongen `YOUNG`) staan in het script van de gids; Alle landen zijn één pagina; Duitsland, Frankrijk, Oostenrijk, Zwitserland, het VK, Italië, Spanje, Ierland en Portugal hebben een filter per deelstaat of regio (`REGIO`, `REGN`; Spanje per autonome gemeenschap, Ierland per provincie, Portugal per NUTS-regio). Talen (regel: Nederlands, Engels en de landstaal of -talen): NL/EN (Nederland, VK, Ierland), NL/EN/FR (België, Frankrijk), NL/EN/DE (Duitsland, Oostenrijk), NL/EN/FR/DE (Luxemburg), NL/EN/DE/FR/IT (Zwitserland), NL/EN/IT (Italië), NL/EN/ES (Spanje), NL/EN/PT (Portugal), NL/EN/DA (Denemarken; taalcode `da`, landcode `dk`). Een gids met één derde taal gebruikt `T(nl,en,x)` en `l-x`-elementen; Zwitserland en Luxemburg gebruiken de taaltabel `LGS` (`T(nl,en,...)` in de volgorde van `LGS`, woordenlijsten per taal zoals `SPFR`, `R5IT`, `ITD`). Foto's staan erin als `@@IMGn@@`. |
| `start.html` | De startpagina. De gegevens in `const D` (kaartstippen, aantallen, recente geboortes) worden bij elke bouw opnieuw berekend uit de gidsen. Kaartvormen en de deelstaat-notitie blijven staan. Talen: Nederlands, Engels, Frans, Duits, Italiaans en Spaans (`T(nl,en,fr,de,it,es)` en `l-fr`/`l-de`/`l-it`/`l-es`-elementen). Onder de titel staat een regel met aantallen (landen · locaties · soorten), berekend uit `D`. Opbouw (16-10-2026, stijl van de Spottersgids): bovenbalk met zoeken, taal en menu; tabbladen Kaart · Landen · Soorten (`#kaart`, `#landen`, `#soorten`); de kaart filtert op land, soort, type en recente geboortes (rode stip); het menu opent de top 10 en de losse pagina’s `#geboren`, `#perpark`, `#typen` en `#over`. |
| `../img/` | Alle foto's; `n.webp` hoort bij `@@IMGn@@`. Nieuwe foto: volgend nummer toevoegen. |
| `artifact_kop.html`, `web_kop.html` | Vaste kopjes voor de Claude-pagina en de website. |
| `top10.json` | De top 10 om te bezoeken (blok op de startpagina en pagina `/top10/`, op de Claude-pagina `#top10`). `vast` staat in die volgorde bovenaan, met de uitleg in zeven talen (nl, en, fr, de, it, es, pt); is de lijst korter dan 10 of verdwijnt een park uit de gids, dan vult de bouw aan op score. Volgorde of uitleg veranderen: alleen dit bestand aanpassen. |
| `franse_namen.json`, `duitse_namen.json`, `italiaanse_namen.json`, `spaanse_namen.json` | Franse, Duitse, Italiaanse en Spaanse soortnamen voor de startgegevens. |
| `taalmenu.js` | Het taalmenu (wereldbol met de taalcode; de lijst toont de talen van de pagina in hun eigen naam). De bouw zet het in de startpagina en in elke gids. |
| `locatietypes.json` | De vaste lijst van locatietypes en labels. Elke locatie heeft in `LOCINFO` één `type` (de namen uit deze lijst) en `labels` (sleutels uit deze lijst). Dierentuin = lid van EAZA, NVD, VdZ, UIZA, AIZA of BIAZA; anders dierenpark. Types en labels hebben namen in zeven talen (nl, en, fr, de, it, es, pt) en uitleg per type (`uitleg_pt` voor de hoofdpagina); `locatietypes.js` kiest de taal met `LT_I`/`LT_TX`. |
| `locatietypes.js` | Filterknoppen, labels en types in de gidsen; de bouw zet dit achter het script van elke gids en deelstaat. |
| `huisstijl.py` | Huisstijl van de startpagina voor de gidsen op de website: bovenbalk, kleuren en letters, rustiger kop, tabbladen en Ko-fi-voet (CSS en script worden door de bouw in elke gids en losse pagina gezet). |
| `bouw.py`, `startdata.py`, `extract.js` | De bouw. Deelstaten en regio’s staan in `STATES` en `REGIOS` in `bouw.py` (samen `DEEL`). |

## Nieuw ontwerp landpagina's (oktober 2026)

`nieuw_ontwerp.py` draait aan het eind van `bouw.py` en zet op elke landpagina in `LANDEN` (alle landen) het app-ontwerp: startscherm met tellers, zoekbalk en tegels, elk onderdeel als eigen scherm, onderbalk. De gebouwde oude pagina wordt als reserve bewaard in `/<land>-oud/` (noindex). Teksten die het ontwerp zelf toevoegt staan in `TR` (NL/EN plus FR, DE, IT, ES, PT); al het andere komt uit de gids. Een regiolink (`/frankrijk/bretagne/`) opent meteen het scherm Locaties met het regiofilter aan. `maak_los()` zet daarna ook de losse park- en soortpagina's (`/<land>/locatie/…`, `/<land>/soort/…`) in dezelfde stijl: terugknop met titel bovenaan, onderbalk naar de gids van het land en een kaart "Bekijk in de gids" onderaan. `maak_start()` geeft de startpagina en de top 10 dezelfde kleuren en een onderbalk (Home · Landen · Soorten · Meer; Meer opent het menu). Duitsland is op 18-10-2026 met `samenvoegen.py de` één pagina met een deelstaatfilter geworden (zoals Frankrijk); de oude keuzepagina en deelstaatpagina's staan als momentopname in `/duitsland-oud/deelstaten/` en `/duitsland-oud/<deelstaat>/`.

## Ontwerp landpagina's: opbouw van de hoofdpagina (18-10-2026)

`test_ontwerp.py` draait aan het eind van `bouw.py` (na `nieuw_ontwerp.py`) en zet op elk land in `LIVE` (alle landen) de opbouw van de hoofdpagina, met `/<land>-oud/` als bron. Onderbalk Kaart · Soorten · Locaties · Meer; het startscherm is de kaart met regioknoppen (landen met regio's), soortrondjes (filteren de kaart; het getal bij "Alle katten" is het aantal bevestigde soorten, soorten zonder bevestigde vermelding hebben een stippelrand), typeknoppen onder de kaart en een lijst "In beeld"; Soorten als fotokaartjes; Locaties als één lijst met locatiekaartjes (filters regio en type); de hoofdtabel, de routeplanner en de rest onder Meer; "Geen katachtigen gevonden" en "Over de lijst" onder Over; "Aanwezig" alleen nog in de hoofdtabel. Nieuwe teksten in `TR` (NL/EN plus FR, DE, IT, ES, PT). Terugdraaien: `test_ontwerp.py` en de regels onderaan `bouw.py` weghalen en opnieuw bouwen.

Daarna (ook in `test_ontwerp.py`): `maak_los2()` geeft de losse park- en soortpagina's dezelfde onderbalk (Kaart · Soorten · Locaties · Meer) en verbergt "Aanwezig"; `maak_europa()` geeft de hoofdpagina, de top 10 en de soortpagina's `/soort/…` de onderbalk Kaart · Landen · Soorten · Meer (zonder de tabbladen erboven), een korte uitleg bij de kaart en altijd zichtbare typeknoppen; op de soortpagina's staat in plaats van de IUCN-status de geschatte aantallen in het wild (`WILD` uit de Nederlandse gids), heet het vak met het gebied "Verspreiding" en hebben de locaties bij "Waar te zien" een type-icoon.

## Jungle-stijl (18-10-2026)

`jungle.py` draait als allerlaatste stap van `bouw.py` en zet op alle pagina's (behalve `/<land>-oud/`, `/spottersgids/`, `/voorbeeld-jungle/` en doorverwijzingen) één blok `<!--jungle-->…<!--/jungle-->` voor `</body>`: lettertypen (Anton, Nunito) en CSS in de stijl "Expeditie" (donker junglegroen, bladeren, luipaardvlekken, golfrand, houten knoppen, goudgeel). Gegevens, teksten en indeling blijven ongewijzigd. Terugdraaien: `python3 bron/jungle.py --weg` en de regel onderaan `bouw.py` weghalen. Reservekopie van de site van vóór de jungle-stijl: tak `backup-voor-jungle`.

## Vindbaarheid (19-10-2026)

De titel van de startpagina staat in de `<head>` van `start.html` (stond eerst in de body, waardoor titel, beschrijving en deelplaatje van de startpagina buiten de kop vielen). De startpagina, de top 10 en de soortpagina's hebben een favicon (`/icon.svg`, pootje in junglekleuren; vast bestand in de hoofdmap). Na de jungle-stijl zet `een_hoofdkop()` onderaan `bouw.py` op `/soort/<naam>/` en `/top10/` de verborgen koppen van de startpagina om van h1 naar h2, zodat de soortnaam de enige h1 is. Die koppen zijn daar nooit zichtbaar (elke knop opent de startpagina), dus het beeld verandert niet.

## Telregel (18-10-2026)

Overal op de site telt een getal bij een soort of locatie alleen **bevestigde** vermeldingen (status g, y, b of r); onzekere (w, en ook p en n) staan er apart achter ("10 soorten · 1 onzeker"). Zo telt ook "N soorten bevestigd op M locaties": M = locaties met een bevestigde kat. Uitzondering: het getal bij een filterknop voor regio of land met een gekozen soort, en "In beeld", tellen wat de kaart en de lijst tonen (dus ook onzekere). De groep "Onzeker" in de routeplanner (`UNSURE`) wordt in elke gids uit `R` berekend; niet meer met de hand bijhouden.

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
- **Kaart zonder Canarische Eilanden**: op verzoek staan de Canarische Eilanden niet op de kaarten (te ver weg; de Balearen staan er sinds 18-10-2026 wel op, met hun eigen eilandvormen in `ISLANDS` van de Spaanse gids en in `D.es.poly` van de startpagina); die locaties hebben geen coördinaten in `LOCS` (zoals reizende circussen) en staan wel in de lijst en het regiofilter. Kaartvorm en regiogrenzen komen uit Natural Earth (50m) en de grenzen van de comunidades (click_that_hood), vereenvoudigd.
- **Onderzoek**: zes regio-agenten plus vier vervolgagenten. Elke agent schreef een eigen bestand (`and_`, `cat_`, `val_`, `mad_`, `nrd_`, `can_`, `vv1_`–`vv4_`) in hetzelfde JSON-formaat; een samenvoegscript koppelde ze op naam en coördinaten. Daarna redactie en vertaling (NL/EN/ES) door twee agenten, met de Nederlandse tekst als sleutel van de vertaaltabellen.

## Ierland toevoegen: lessen (oktober 2026)

- **Een derde taal eruit halen.** De Ierse gids (NL/EN) is met een script afgeleid van de Spaanse: eerst alle `l-es`-elementen en `-es`-blokken weg (met een tellende verwijderfunctie, want blokken zijn genest), `LGS` naar `["nl","en"]` en de Spaanse tabellen (`SPES`, `ESD`, `R1ES` …) leeg. Daarna de gegevens (`R`, `LOCS`, `LOCINFO`, `REGIO`, `REGN`, `TWX`, `YOUNG` …) en de vaste tekstblokken. Het script en de gegevens staan niet in de repo; zie de werkwijze in `VOORTGANG.md`.
- **Een buurland op de kaart.** Noord-Ierland staat grijs op de kaart van de gids (`NI`, klasse `buur`), zodat de grens duidelijk is; het kaartkader (`viewBox`) moet dan ook Noord-Ierland omvatten. Op de startpagina hoort Noord-Ierland bij de vorm van het VK.
- **Lege provincie.** Een provincie zonder locaties met katten (Connacht) krijgt geen kop in de lijst en geen chip in het filter; zet de locaties zonder katten wel in “Geen katachtigen gevonden”.
- **Link naar een andere landgids.** Binnen een gids werkt een relatieve link naar een ander land niet in de Claude-pagina; gebruik de volledige website-URL met `target="_blank"`.
- **Kaartkader op de startpagina.** Bij een land verder naar het westen: `LON0` in `start.html` lager zetten en `FULL[2]` met hetzelfde aantal pixels vergroten (`(oud−nieuw)·K`, K = 0,623·60).
- **Welpennamen in `YOUNG.n`.** Zet in `n` alleen het aantal (“2 welpen”); namen en geslacht in `x`. De startpagina vertaalt `n` met vaste regels naar FR/DE/IT/ES, en een zin met namen wordt half vertaald.
- **Weinig locaties, veel “geen katten”.** In Ierland zijn er 7 locaties met katten en 73 zonder. De officiële lijst (2022) bestond vooral uit roofvogelcentra, open farms en aquaria; ook die zijn allemaal nagelopen en in de lijst gezet.

## Portugal toevoegen: lessen (oktober 2026)

- **Een derde taal vervangen in plaats van weghalen.** De Portugese gids is afgeleid van de Spaanse: alle Spaanse namen in de code zijn hernoemd (`SPES`→`SPPT`, `ESD`→`PTD`, `R1ES`→`R1PT`, `LBL_ES`→`LBL_PT`, `MND_ES`→`MND_PT`, het `es`-blok in `XT` → `pt`, `l-es`→`l-pt`, `LGS`, de taalknop en de taalscriptjes in de kop) en daarna zijn de Spaanse teksten vervangen door Portugese. Let op drie plekken die een gewone vertaaltabel mist: het derde argument van `T()` als sjabloontekst met backticks (bijv. `` `Comprobado: ${inf.checked}…` ``), de blokken `statussen-es` en `onzeker-es` (hele tekstblokken met een eigen id) en de woordenlijst voor bronnen `SRC_GL` (bevat Spaans; leeg gemaakt omdat alle bronnen in `R7EN`/`R7PT` staan). Controleer de nieuwe taal altijd met een scan op woorden uit de oude taal.
- **Nieuwe taal in de gedeelde bestanden.** Een gidstaal die de hoofdpagina niet heeft, moet toch in `taalmenu.js` (naam van de taal), `locatietypes.json` (`pt` bij types en labels), `locatietypes.js` (`LT_I`, extra argument in `LT_TX` en bij elke aanroep) en `bouw.py` (`NOTE`, `RPTXT`, `GTAAL`) en `startdata.py` (`GTAAL`).
- **Vertalen via een tabel.** Gegevens en tekstblokken zijn in het Nederlands en Engels geschreven; het Portugees komt uit een vertaaltabel met de Engelse tekst als sleutel. Ontbrekende teksten worden verzameld en in één keer door een vertaalagent vertaald.
- **Regio’s uit coördinaten.** De NUTS-regio’s (2024) komen uit de GISCO-bestanden van Eurostat; de regio van elke locatie wordt uit de coördinaten bepaald. Spanje staat als grijs buurland op de kaart (`BUUR`).
- **Agenten en gedeelde mappen.** Een vertaalagent overschreef een script met dezelfde naam in de werkmap; geef agenten een eigen map voor hulpscripts en noem in de opdracht welke bestanden ze niet mogen aanraken.


## Denemarken toevoegen: lessen (oktober 2026)

- **Landcode ≠ taalcode.** Het land heet `dk`, de taal `da`. In `GTAAL` staat `"dk": ["da"]`; in de gids zijn alle taalnamen `da` (`l-da`, `SPDA`, `DAD`, `R1DA` …). De gedeelde lagen (`test_ontwerp.py`, `nieuw_ontwerp.py`, `huisstijl.py`, `jungle.py`, `locatietypes.*`, `taalmenu.js`) hebben `da` achteraan in hun talenlijsten, zodat bestaande indexen niet verschuiven. In `EU_CSS` (`test_ontwerp.py`) staat een regel die `.l-da` op de hoofdpagina verbergt, omdat `start.html` geen Deens heeft.
- **Deense letters in adressen.** `slug()` maakt van æ “ae” en van ø “oe” (å wordt “a” door NFD). Dat staat in `startdata.py`, `test_ontwerp.py` (`slug_py`) en de JS-`slug` van de Deense gids. Een nieuwe gids met æ/ø moet dezelfde regel in zijn eigen `slug` krijgen.
- **Regiofilter**: naast `REGIO` en `REGN` ook `REGORDER` (volgorde van de knoppen) aanpassen; anders verschijnt alleen “Alle regio’s”.
- **Officiële lijst**: de Fødevarestyrelsen-lijst (“Godkendte zoologiske anlæg”) is de lijst voor EU-handel. Kleine parken (Nordisk Dyrepark) staan er niet op: per regio zoeken blijft nodig.
- **Kleine parken verstoppen katten.** Glad Zoo noemde de serval niet op “Vores dyr”, wel in het dagprogramma (voedering) en in de persfoto’s. Kijk bij kleine parken ook naar dagprogramma, parkkaart en mediabibliotheek (WordPress).
- **Europakaart**: Zweden en Zuid-Noorwegen zijn aan `NBR` in `start.html` toegevoegd (GISCO NUTS 2024, geprojecteerd met `P`).
- Het bouwscript van de gids (afgeleid van de Portugese gids, gegevens als JSON, Deens via een vertaaltabel) staat niet in de repo.
