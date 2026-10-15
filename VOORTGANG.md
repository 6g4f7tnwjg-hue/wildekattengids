# Voortgang

Bijgehouden door Claude. Nieuwste bovenaan.

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
