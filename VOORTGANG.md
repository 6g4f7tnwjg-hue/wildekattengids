# Voortgang

Bijgehouden door Claude. Nieuwste bovenaan.

## 16 oktober 2026 – Nieuwe opbouw startpagina

De startpagina (`bron/start.html`) is opnieuw ingedeeld in de stijl van de Spottersgids (kleuren, letters Alegreya/Alegreya Sans/Barlow Condensed, knoppen). Mobiel is de pagina van ±16.400 px naar ±1.400 px gegaan.
- **Bovenbalk** (vast): pootje + naam, vergrootglas (zoekvak klapt open), taalmenu, menuknop.
- **Tabbladen** Kaart · Landen · Soorten; de pagina opent op Kaart.
- **Kaart**: landenknoppen om in te zoomen, soortcirkels met foto (kies een soort: alleen zijn locaties, onzeker als open stip), +/−/hele kaart, slepen en knijpen. Locaties met recente geboortes hebben een rode stip; de legenda heeft een knop “Recent geboren” (alleen die locaties) en een uitklapbaar filter op type. Het infovak toont de katten en de geboortes van de gekozen locatie.
- **Landen**: één kaart per land met aantallen, talen en de nieuwste geboorte. “Kies een land” en “Overzicht per land” zijn samengevoegd.
- **Menu**: Top 10, Recent geboren (nieuwe pagina met alle geboortes uit `D.sp`, filter per land), Parken op aantal soorten, Soorten locaties, Over deze gids; onder “Meer” de Spottersgids en Ko-fi. De dubbele blokken onderaan (Spottersgids, Ko-fi, landenlijst naast de kaart) zijn weg.
- De soortpagina’s (`/soort/…`) en `/top10/` gebruiken dezelfde kop en stijl.

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
