# Voortgang

Bijgehouden door Claude. Nieuwste bovenaan.

## 18 oktober 2026 – Nieuwe opbouw op alle landen

Het ontwerp van /nederland/ staat nu op alle twaalf landpagina's (`LIVE` in `bron/test_ontwerp.py`). Nieuw voor landen met regio's: regioknoppen boven de soortrondjes op het kaartscherm; de lijsten "In beeld" en Locaties volgen het regio- en typefilter. Teksten in alle gidstalen. Gecontroleerd op 390 px in alle talen: geen fouten, geen horizontaal scrollen, aantallen kloppen (bevestigde soorten = getal bij "Alle katten"). De testpagina /nederland-test/ is weg.

## 18 oktober 2026 – Nieuwe opbouw live op /nederland/

Goedgekeurd: het testontwerp staat nu ook op /nederland/ (`test_ontwerp.maak_alles()`, lijst `LIVE`). De reserve blijft /nederland-oud/; /nederland-test/ blijft voorlopig staan voor de volgende landen. Volgende stappen (afgesproken): alle andere landen in dit ontwerp (met regiofilter op het kaartscherm en teksten in alle gidstalen), daarna de hoofdpagina en losse pagina's gelijktrekken en de IUCN-status op de soortpagina's vervangen door de geschatte aantallen in het wild, tot slot de Nederlandse gids nalopen (stand 28-9-2026).

## 18 oktober 2026 – Testpagina nieuwe opbouw (/nederland-test/)

Op verzoek een testpagina naast de live Nederlandse gids, om de landpagina's dichter bij de hoofdpagina te brengen (bron: `bron/test_ontwerp.py`, zie `bron/LEESMIJ.md`). /nederland/ en de andere pagina's zijn niet veranderd.
- Onderbalk Kaart · Soorten · Locaties · Meer (gelijk aan de hoofdpagina); Routeplanner, Actueel, In het kort, Kleur & hybriden, Favorieten, Hoofdtabel, Over en Rapporteer onder Meer.
- Startscherm = kaart: kop zoals de hoofdpagina (titel, ondertitel, regel met aantallen), soortrondjes met foto die de kaart filteren, typeknoppen onder de kaart, lijst “In beeld” (meeste soorten eerst). Zoeken klapt open via het vergrootglas. Geen tegels met illustraties en geen grote Rapporteer-balk.
- Soorten: fotokaartjes zoals op de hoofdpagina. Locaties: één lijst met locatiekaartjes (type-icoon, plaats, type, aantal soorten, korte beschrijving), met typefilter. “Geen katachtigen gevonden” en “Niet specifiek online te verifiëren” staan onder Over.
- “Aanwezig” wordt alleen in de hoofdtabel nog getoond; elders alleen afwijkingen (vertrek, gepland, rondleiding …).

## 17 oktober 2026 – Oostenrijk, Zwitserland, Frankrijk en VK: één pagina met regiofilter

Met `bron/samenvoegen.py` zijn de gidsen van Oostenrijk (22 locaties), Zwitserland (20), Frankrijk (67) en het VK (88) omgezet van een pagina per deelstaat/regio naar één pagina met een regiofilter, zoals Italië en Spanje. Alleen Duitsland (172) houdt pagina’s per deelstaat.
- Gegevens samengevoegd (`R`, `LOCS`, `LOCINFO`, `YOUNG`, vertaaltabellen); drie VK-locaties stonden in twee regio’s en tellen nu één keer (88 i.p.v. 91). Kaart: alle regio’s samen met een nieuwe projectie. Route met alle soorten opnieuw berekend (gretig).
- Teksten per regio (In het kort, aanbevelingen, gepland, kleur, uitleg, lijsten per locatie) staan onder elkaar met de regionaam als kop (`data-rg`); het regiofilter verbergt de andere regio’s overal op de pagina. Nieuwe algemene teksten (inleiding, locaties, jongen) in alle talen van de gids.
- Oude adressen (`#tirol/…`, `/oostenrijk/tirol/`, `/oostenrijk/tirol/locatie/…`) werken nog: de gids zet dan het filter op die regio; `bouw.py` maakt doorverwijzingen (`OUD_DEEL`).
- Bijwerken gaat nu zoals bij Italië: één gids `bron/gidsen/xx.html` met `REGIO`/`REGN`/`REGORDER`.

## 16 oktober 2026 – Gidsen in de huisstijl van de startpagina

Nieuw bestand `bron/huisstijl.py`: de bouw zet in elke landengids, deelstaat- en regiopagina en in de losse soort- en locatiepagina’s (alleen op de website) dezelfde bovenbalk als de startpagina (pootje = terug naar de hoofdpagina, vergrootglas = zoeken op de hoofdpagina via `#zoek`, taalknop van de gids, menu), de kleuren en letters van de startpagina, een rustiger kop (kleine titelregel, foto 21:9), de inhoudsopgave als tabbladen die blijven staan (met het actieve tabblad gemarkeerd) en de Ko-fi-voet. “← Alle landen”, “Steun de gids” bovenaan en het losse Ko-fi-blok zijn verborgen. De gegevens, teksten en kaarten van de gidsen zijn niet veranderd. Het pootje draagt het oude id `naar-landen`, omdat het script van de gids daarnaar luistert.
- Kaarten in de gidsen: elke stip krijgt kleur en icoon van zijn type (zelfde als de startpagina; `window.__HST` uit `huisstijl.kaartdata`, het type uit `LOCINFO`), de typeknoppen boven de kaart (`locatietypes.js`) krijgen hetzelfde icoon, zee lichtblauw. Startpagina: bij een gekozen land zijn de stippen en namen van de andere landen weg en zijn die landen grijs.

## 16 oktober 2026 – Nieuwe opbouw startpagina

De startpagina (`bron/start.html`) is opnieuw ingedeeld in de stijl van de Spottersgids (kleuren, letters Alegreya/Alegreya Sans/Barlow Condensed, knoppen). Mobiel is de pagina van ±16.400 px naar ±1.400 px gegaan.
- **Bovenbalk** (vast): pootje + naam, vergrootglas (zoekvak klapt open), taalmenu, menuknop.
- **Tabbladen** Kaart · Landen · Soorten; de pagina opent op Kaart.
- **Kaart**: landenknoppen om in te zoomen, soortcirkels met foto (kies een soort: alleen zijn locaties, onzeker als open stip), +/−/hele kaart, slepen en knijpen. Locaties met recente geboortes hebben een rode stip; de legenda heeft een knop “Recent geboren” (alleen die locaties) en een uitklapbaar filter op type. Het infovak toont de katten en de geboortes van de gekozen locatie.
- **Landen**: één kaart per land met aantallen, talen en de nieuwste geboorte. “Kies een land” en “Overzicht per land” zijn samengevoegd.
- **Menu**: Top 10, Recent geboren (nieuwe pagina met alle geboortes uit `D.sp`, filter per land), Parken op aantal soorten, Soorten locaties, Over deze gids; onder “Meer” de Spottersgids en Ko-fi. De dubbele blokken onderaan (Spottersgids, Ko-fi, landenlijst naast de kaart) zijn weg.
- De soortpagina’s (`/soort/…`) en `/top10/` gebruiken dezelfde kop en stijl.
- Later dezelfde avond: elk type locatie een eigen kleur en icoon (`TCOL`, `GLY` in `start.html`, volgorde van `locatietypes.json`); locaties die op het scherm dicht bij elkaar liggen worden een rondje met een getal (tik = inzoomen, op dezelfde plek = lijst in het infovak); bij een gekozen land worden de andere landen lichter; geboortes aan/uit (rode rand, bij groepjes een rood stipje); legenda met de types klapt uit onder de kaart.
- Daarna: geboortes standaard uit; geen nieuwste geboorte meer op de landkaarten; kaart met lichtblauwe zee, grijze buurlanden (`NBR`, Natural Earth 1:50m via world-atlas, geprojecteerd en bijgesneden) en landnamen; groepjes olijfgroen met schaduw; “Soorten locaties” klapt per type open tot een lijst per land; Ko-fi onderaan elke pagina (voet van `start.html`); lijst “In beeld” onder de kaart (meeste soorten eerst, tik = kaart erheen).

## 16 oktober 2026 – Portugal

Nieuwe landpagina `portugal/` (bron: `bron/gidsen/pt.html`), in het Nederlands, Engels en Portugees (Europees Portugees). Eén pagina met een filter per regio (de NUTS-regio’s van 2024: Norte, Centro, Oeste en Taagvallei, Lissabon en Setúbal, Alentejo, Algarve, Azoren, Madeira; alleen regio’s met locaties krijgen een knop), plus kaart, routeplanner, recente geboortes, soortpagina’s, filters op type en labels en het meldformulier. Spanje staat grijs op de kaart.

**Aantallen**
- **7 locaties** met wilde katachtigen: 3 dierentuinen (Jardim Zoológico de Lisboa, Zoo Santo Inácio, Zoo de Lagos), 2 dierenparken (Zoo da Maia, Europaradise), 1 wildpark (Parque Biológico da Serra da Lousã) en 1 safaripark (Badoca). Europaradise heeft alleen een onzekere vermelding.
- **10 soorten bevestigd**: leeuw, tijger, luipaard, jaguar, nevelpanter, cheetah, Euraziatische lynx, Iberische lynx, rode lynx, serval. Ocelot (Lagos) alleen onzeker.
- 23 vermeldingen in de hoofdtabel, waarvan 3 onzeker (zie `TWIJFELGEVALLEN.md`).
- Route met alle soorten in twee parken: Jardim Zoológico de Lisboa en Zoo de Lagos.
- 1 recente geboorte: drie Perzische luipaarden in Lissabon (april 2026).
- 48 andere locaties onderzocht zonder katten (fokcentrum Iberische lynx, gepland, gesloten, opvang, aquaria, quintas pedagógicas e.d.); op de Azoren en Madeira geen wilde katten.

**Werkwijze**
- Basislijst uit Zootierliste (alle 202 katachtige taxa, “Aktuelle” en “Ehemalige”: 38 Portugese instellingen), de EAZA-ledenkaart (7 Portugese leden) en de AIZA-ledenlijst (7 Portugese leden).
- Officiële lijst: vergunningen geeft sinds 2012 de DGAV (niet het ICNF). De enige gepubliceerde lijst “Parques Zoológicos Licenciados” (24 parken) is van 28-04-2021: **verouderd**. Azoren en Madeira hebben eigen diensten.
- Zes onderzoeksagenten (Zootierliste en officiële lijsten, Norte, Centro, Lissabon + Alentejo, Algarve + eilanden, opvang/particulieren/circussen) en één vervolgagent voor de open punten. Eén JSON-formaat met eigen naamvoorvoegsels, samengevoegd met een script; regio’s bepaald uit de coördinaten (NUTS 2024).
- Type: dierentuin bij lidmaatschap van EAZA of AIZA; safariparken en wildparken houden hun eigen type.
- Circussen: wilde dieren verboden (Lei 20/2019, overgang tot eind 2025); de laatste circuskatten gingen naar AAP Primadomus (Spanje, 2022 en 2026). Particulieren mogen sinds 2018 geen wilde katten houden (Portaria 86/2018).
- De gids is met een script afgeleid van de Spaanse gids: Spaans → Portugees in de code (taaltabellen `SPPT`, `PTD`, `R1PT` …), de vaste teksten door een vertaalagent naar het Portugees vertaald, daarna gegevens en tekstblokken (NL/EN, Portugees via een vertaaltabel). Geen foto’s van parken gezocht.

**Hoofdpagina**: Portugal heeft een vlag, kleur (donkerblauw), tegel en kaartvorm (vasteland; het kaartkader was al groot genoeg), staat in “alle soorten”, “parken op aantal soorten”, het overzicht per land, het zoeken en de tellerregel. Landenlijsten in titels en beschrijvingen in zes talen bijgewerkt. Het taalmenu van de hoofdpagina blijft zes talen; Portugees staat in het taalmenu van de Portugese gids. `locatietypes.json`/`.js` en het meldformulier hebben nu ook Portugees.

**Gecontroleerd**: de Portugese pagina (NL/EN/PT) en de hoofdpagina (zes talen) op 375 px: geen fouten, geen horizontaal scrollen, geen Spaanse resten. Regiofilter, kaart, zoeken, locatie- en soortpagina’s, route, interne links en de Claude-pagina.

## 15 oktober 2026 – Ierland

Nieuwe landpagina `ierland/` (bron: `bron/gidsen/ie.html`), in het Nederlands en Engels (geen Iers, op verzoek). Eén pagina met een filter per provincie (Leinster, Munster, Ulster-deel; Connacht heeft geen locaties met katten), plus kaart, routeplanner, recente geboortes, soortpagina’s, filters op type en labels en het meldformulier. Noord-Ierland staat niet in deze gids: grijs op de kaart, met een verwijzing naar de VK-gids.

**Aantallen**
- **7 locaties** met wilde katachtigen: 3 dierentuinen (Dublin Zoo, Fota Wildlife Park, Ardmore Open Farm; EAZA of BIAZA), 2 dierenparken (Secret Valley, Errigal View), 1 wildpark (Wild Ireland) en 1 attractiepark (Emerald Park). Ardmore en Errigal View hebben alleen onzekere vermeldingen.
- **6 soorten bevestigd**: leeuw (Aziatisch), tijger (Amoer en Sumatraans), luipaard (Amoer), cheetah, Euraziatische lynx en serval. Sneeuwluipaard (Dublin Zoo) alleen onzeker.
- 15 vermeldingen in de hoofdtabel, waarvan 4 onzeker (zie `TWIJFELGEVALLEN.md`).
- Route met alle soorten in drie parken: Emerald Park, Dublin Zoo en Secret Valley (Fota kan Dublin Zoo vervangen).
- 3 recente geboortes, allemaal in Fota: cheetah (november 2025), Sumatraanse tijger (juni 2026), Aziatische leeuw (juli 2026).
- 73 andere locaties onderzocht zonder katten (gesloten, circussen, opvang zonder katten, roofvogelcentra, open farms, aquaria).

**Werkwijze**
- Basislijst uit Zootierliste (alle katachtige taxa, “Aktuelle” en “Ehemalige”: 35 Ierse instellingen, 6 met katten), de EAZA-ledenkaart (5 Ierse leden) en de BIAZA-ledenlijst (5 Ierse leden).
- Officiële lijst: de NPWS publiceert geen lijst van vergunde dierentuinen (S.I. 440/2003). De nieuwste volledige lijst is een antwoord op Kamervragen van 8 september 2022 (55 geïnspecteerde dierentuinen, 51 open): **verouderd**. Alle namen daarop zijn nagelopen.
- Vijf onderzoeksagenten (Zootierliste en officiële lijsten, Leinster, Munster, Connacht + Cavan/Donegal/Monaghan, opvang/particulieren/circussen) en twee vervolgagenten (open punten per locatie; de NPWS-namen en een brede zoektocht naar gemiste locaties). Eén JSON-formaat, eigen naamvoorvoegsels, samengevoegd met een script. Per locatie de eigen website (waar nodig met Playwright), daarna Iers nieuws en sociale media; bij elke vermelding bron en datum.
- Type: dierentuin bij lidmaatschap van EAZA of BIAZA (BIAZA toegevoegd aan `locatietypes.json`); wildparken en attractieparken houden hun eigen type.
- Circussen: wilde dieren verboden sinds 1-1-2018 (S.I. 482/2017), ook tentoonstellen en winterkwartieren; geen circus met katten meer. Particulier houden van wilde dieren is in de Republiek niet geregeld (geen register); geen particuliere houder gevonden die bezoekers ontvangt.
- De gids is met een script afgeleid van de Spaanse gids (eerst het Spaans eruit, dan gegevens en vaste teksten). Geen foto’s van parken gezocht; de pagina gebruikt de bestaande soortfoto’s.

**Hoofdpagina**: Ierland heeft een vlag, kleur (groen), tegel en kaartvorm (Natural Earth; het kaartkader is naar het westen vergroot tot 10,75° W), staat in “alle soorten”, “parken op aantal soorten”, het overzicht per land, het zoeken en de tellerregel (nu 11 landen · 500 locaties · 29 soorten). Landenlijsten in titels en beschrijvingen in zes talen bijgewerkt. Top 10 niet veranderd: geen Iers park komt in de buurt (Fota en Emerald Park scoren 30, nummer 10 heeft 46).

**Gecontroleerd**: de Ierse pagina (NL/EN) en de hoofdpagina (zes talen) op 375 px: geen fouten, geen horizontaal scrollen. Provinciefilter (kaart, lijsten en hoofdtabel), kaart, zoeken, locatie- en soortpagina’s, route, interne links en de Claude-pagina.

## 15 oktober 2026 – Spanje

Nieuwe landpagina `spanje/` (bron: `bron/gidsen/es.html`), in het Nederlands, Engels en Spaans. Eén pagina met een filter per autonome gemeenschap (kaart, lijsten, keuzelijst en hoofdtabel), plus kaart, routeplanner, recente geboortes, soortpagina’s, filters op type en labels en het meldformulier.

**Aantallen**
- **43 locaties** met wilde katachtigen in 15 autonome gemeenschappen: 17 dierentuinen, 8 dierenparken, 5 safariparken, 3 wildparken, 8 opvangcentra, 1 attractiepark en 1 natuur- en fokcentrum (El Acebuche, alleen met parkgids). Daarvan 2 op de Balearen en 5 op de Canarische Eilanden (in de lijst en het regiofilter, niet op de kaart).
- **18 soorten bevestigd**: leeuw, tijger, luipaard, jaguar, nevelpanter, cheetah, poema, Euraziatische lynx, Iberische lynx, rode lynx, serval, caracal, ocelot, margay, Geoffroy’s kat, Bengaalse kat, Europese wilde kat, Afrikaanse wilde kat. Sneeuwluipaard en zandkat alleen onzeker.
- 124 vermeldingen in de hoofdtabel, waarvan 27 onzeker (zie `TWIJFELGEVALLEN.md`) en 6 alleen met rondleiding (AAP Primadomus, El Acebuche).
- Route met alle soorten in vijf parken (de enige combinatie): Safari Madrid, Zoo Koki, Terra Natura Benidorm, Oasys MiniHollywood en Selwo Aventura.
- 4 recente geboortes: margay (Terra Natura Benidorm, september 2026), jaguar (Loro Parque, februari 2026), leeuw (Cabárceno, juli 2026; Safari Madrid, februari 2025).
- 52 andere locaties onderzocht zonder katten (gesloten, niet te bezoeken, vroeger katten of geen katten).

**Werkwijze**
- Basislijst uit Zootierliste (alle 202 katachtige taxa, “Aktuelle” en “Ehemalige”: 56 Spaanse instellingen), de EAZA-ledenkaart en de AIZA-ledenlijst (45 Spaanse leden).
- Officiële registers per autonome gemeenschap gezocht: alleen Castilië en León publiceert het register (open data, 2023); de andere 18 gemeenschappen en steden hebben geen openbare lijst. De nationale inventaris (Ley 31/2003) is alleen in een versie van 2012 bekend.
- Zes onderzoeksagenten per regio en vier vervolgagenten voor wat door de zoeklimiet bleef liggen (o.a. circussen, particulieren en opvang landelijk). Per locatie de eigen website (waar nodig met Playwright), daarna Spaans nieuws en sociale media; bij elke vermelding bron en datum.
- Type: dierentuin bij lidmaatschap van EAZA of AIZA (AIZA toegevoegd aan `locatietypes.json`); safariparken, wildparken en opvangcentra houden hun eigen type.
- Circussen: verboden sinds 2023 (Ley 7/2023); geen circus of particuliere houder gevonden waar bezoekers nog katten zien. Iberische lynx: fokcentra niet te bezoeken, vrij levende lynxen tellen niet mee.
- Geen foto’s van parken gezocht; de pagina gebruikt de bestaande soortfoto’s.

**Hoofdpagina**: Spanje heeft een vlag, kleur, tegel en kaartvorm (alleen het vasteland; het kaartkader is iets groter gemaakt), staat in “alle soorten”, “parken op aantal soorten”, het overzicht per land, het zoeken en de tellerregel (nu 10 landen · 493 locaties · 29 soorten). De hoofdpagina heeft nu zes talen: Spaans erbij (ook soortnamen, locatietypes, top-10-uitleg, datum en meldformulier). De top 10 is niet veranderd (voorstel in `bron/OPEN.md`).

**Gecontroleerd**: de Spaanse pagina (NL/EN/ES) en de hoofdpagina (zes talen) op 375 px: geen fouten, geen horizontaal scrollen. Regiofilter, kaart, zoeken (tabel en hoofdpagina), locatie- en soortpagina’s, route, interne links en de Claude-pagina.

## 15 oktober 2026 – Italië

Nieuwe landpagina `italie/` (bron: `bron/gidsen/it.html`), in het Nederlands, Engels en Italiaans. Eén pagina met een filter per regio (kaart, lijsten, keuzelijst en hoofdtabel), plus kaart, routeplanner, recente geboortes, soortpagina’s, filters op type en labels en het meldformulier.

**Aantallen**
- **41 locaties** met wilde katachtigen: 28 vaste locaties (11 dierentuinen, 6 dierenparken, 4 safariparken, 3 wildparken, 2 opvangcentra en 2 particuliere houders) en **13 reizende circussen** (zonder vaste plek op de kaart).
- **18 soorten bevestigd**: leeuw, tijger, luipaard, jaguar, sneeuwluipaard, nevelpanter, cheetah, poema, jaguarundi, Euraziatische lynx, serval, caracal, ocelot, Geoffroy’s kat, Bengaalse kat, vissende kat, manoel, Europese wilde kat.
- 135 vermeldingen in de hoofdtabel, waarvan 16 onzeker (zie `TWIJFELGEVALLEN.md`) en 11 alleen met rondleiding.
- Route met alle soorten in vier parken: La Torbiera, Parco Safari delle Langhe, Valcorba en Cappeller.

**Werkwijze**
- Basislijst uit Zootierliste (alle katachtigen, huidige en vroegere houdingen in Italië), aangevuld met de officiële lijst van vergunde dierentuinen (MASE, oktober 2025: 37 + 1 regionaal), de EAZA-ledenkaart, de UIZA-lijst (2022) en een landelijke zoektocht naar opvangcentra, particuliere houders en circussen.
- Per locatie de eigen website, daarna Italiaans nieuws en sociale media; bij elke vermelding bron en datum. Geboortes van de afgelopen 12 maanden (grote katten 2 jaar).
- Type: dierentuin alleen bij lidmaatschap van EAZA of UIZA (ook toegevoegd aan `locatietypes.json`).
- Geen foto’s van parken gezocht; de pagina gebruikt de bestaande soortfoto’s.

**Hoofdpagina**: Italië heeft een vlag, kleur en tegel, staat op de kaart (het kaartkader is groter gemaakt), in “alle soorten”, “parken op aantal soorten”, het overzicht per land en het zoeken; de tellerregel telt nu 9 landen. Italië doet mee in de berekening van de top 10, maar de top 10 is een vaste lijst van tien parken (zie `bron/OPEN.md`).

**Gecontroleerd**: de Italiaanse pagina en de hoofdpagina op 375 px in elke taal (geen fouten, geen horizontaal scrollen), regiofilter, kaart, zoeken, locatie- en soortpagina’s en interne links.

## 14 oktober 2026 – talen en kop van de hoofdpagina

**Talen (nieuwe regel: elke landpagina in Nederlands, Engels en de landstaal of -talen)**

| Land | Talen nu | Wat er veranderd is |
|---|---|---|
| Nederland | NL/EN | – |
| België | NL/EN/FR | – |
| Luxemburg | NL/EN/FR/DE | Duits toegevoegd (alle teksten, ook “In het kort”, uitleg en soortpagina’s) |
| Duitsland | NL/EN/DE | – |
| Frankrijk | NL/EN/FR | – |
| Oostenrijk | NL/EN/DE | had al geen Frans meer |
| Zwitserland | NL/EN/DE/FR/IT | Frans en Italiaans toegevoegd, in alle 7 regio’s |
| Verenigd Koninkrijk | NL/EN | Duits verwijderd |
| Hoofdpagina | NL/EN/FR/DE/IT | Italiaans toegevoegd (ook soortnamen, locatietypes en top 10) |

De inhoud zelf is niet veranderd; alleen vertaald. De gidsen met meer dan drie talen (Zwitserland, Luxemburg) gebruiken nu één taaltabel (`LGS`) in plaats van één vaste derde taal.

**Kop van de hoofdpagina**
- De rij taalknoppen is vervangen door één knop met een wereldbol en de taalcode (“🌐 NL”). Tikken opent een lijst met de talen in hun eigen naam. Op een landpagina staan alleen de talen van dat land. Code: `bron/taalmenu.js`, door de bouw in elke pagina gezet.
- Ondertitel: “Wilde katachtigen in Europa” (in elke taal), met daaronder een regel met aantallen (landen · locaties · soorten) die uit de data wordt berekend. Stand bij deze bouw: 8 landen · 409 locaties · 29 bevestigde soorten.
- Pootje, “Steun de gids” en de taalknop staan op één regel, ook op 375 px; de datum staat op een smal scherm op de regel eronder.

**Gecontroleerd:** elke landpagina en de hoofdpagina op 375 px in elke taal (geen fouten, geen horizontaal scrollen), taalwissel via het menu, zoeken, kaart en interne links.

**Opgemerkt, niet aangepast:** de Zürich-pagina noemt een park “de enige … in Oost-Zwitserland” (lijkt een fout in het origineel); de balk “Alle regio’s / Regio:” in de Zwitserse regio’s is in elke taal Nederlands (was al zo).
