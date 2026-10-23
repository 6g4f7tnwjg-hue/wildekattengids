# Voortgang

Bijgehouden door Claude. Nieuwste bovenaan.

## 23 oktober 2026 – Noorwegen

Nieuwe landpagina `noorwegen/` (bron: `bron/gidsen/no.html`, gebouwd met `bron/landbouw/no/gen.py`), in het Nederlands, Engels en Noors (bokmål; taalcode `nb`, landcode `no`). Eén pagina met een filter per fylke (5 fylker met locaties), met kaart, routeplanner, recente geboortes, soortpagina’s, filters en het meldformulier. Zweden en Finland staan grijs op de kaart.

**Aantallen**
- **6 locaties**, alle met een bevestigde kat: 2 dierentuinen (Dyreparken, EAZA; Bjørneparken, SDF), 1 dierenpark (Tangen Dyrepark) en 3 wildparken met Noordse dieren (Langedrag, Polar Park, Park Nordica).
- **6 soorten bevestigd**: tijger, leeuw, luipaard (Amoerluipaard), cheetah, Euraziatische lynx, serval. De lynx in 5 parken.
- 10 vermeldingen in de hoofdtabel, geen onzekere.
- Route met alle soorten in drie parken: Dyreparken, Bjørneparken, Tangen Dyrepark.
- Recente geboortes in Dyreparken: 4 cheetahs (6-8-2026), 4 leeuwen (29-4-2026) en 5 leeuwen (19-5-2025, 4 in leven).
- 23 andere locaties zonder katten (aquaria, attractieparken, circussen); Haugaland Zoo had rond 2017–2018 een nevelpanter.

**Werkwijze**
- Er is geen officiële lijst: parken melden zich bij Mattilsynet en hebben voor elke wilde soort een vergunning nodig (FOR-2016-09-05-1035). Gebruikt: EAZA (3 Noorse leden), SDF (Bjørneparken) en Zootierliste.
- Particulieren mogen sinds 2017 geen uitheemse wilde katten houden (FOR-2017-05-11-597, ook hybriden F1–F4); in circussen alleen gedomesticeerde dieren.
- Vier onderzoeksagenten en één vervolgagent. Type: dierentuin bij lidmaatschap van EAZA of SDF; parken met alleen Noordse dieren in grote verblijven als wildpark.
- Ondersoort alleen als een bron hem noemt: lynx en leeuw (Dyreparken) staan op onbekend.
- De gids is met een script afgeleid van de Zweedse (`bron/landbouw/no/tools/basis_omzetten.py`), vaste teksten door een vertaalagent; Noorse datums als “23. oktober 2026”.

**Gedeelde bestanden**: taal `nb` en land `no` in alle gedeelde lagen; locatietypes in het Noors: dierentuin = “Dyrehage”, dierenpark = “Dyrepark”. Hoofdpagina: Noorwegen in alle lijsten; kaartkader naar 71,4° N en 31,7° O (Finnmark), Finland grijs. Nu 16 landen.

**Ook**: Tsjechische gids: Iberische lynx “Španělsko a Portugalsko” (was “Španělsko a Česko”).

**Gecontroleerd**: de Noorse pagina in NL/EN/NB op 390 px (Chromium): geen fouten, geen horizontaal scrollen, geen Zweedse of Portugese resten. Overige pagina’s vergeleken met de vorige versie.

## 23 oktober 2026 – Zweden

Nieuwe landpagina `zweden/` (bron: `bron/gidsen/se.html`, gebouwd met `bron/landbouw/se/gen.py`), in het Nederlands, Engels en Zweeds. Eén pagina met een filter per län (9 län met locaties), met kaart, routeplanner, recente geboortes, soortpagina’s, filters op type en labels en het meldformulier. Noorwegen, Finland en Denemarken staan grijs op de kaart.

**Aantallen**
- **11 locaties**, alle met een bevestigde kat: 10 dierentuinen (lid van EAZA of de Svenska Djurparksföreningen: Kolmården, Parken Zoo, Nordens Ark, Borås, Skånes Djurpark, Ystad, Öland, Skansen, Vildriket, Lycksele) en 1 dierenpark (Junsele, alleen ’s zomers).
- **11 soorten bevestigd**: leeuw, tijger, luipaard, jaguar, sneeuwluipaard, cheetah, Euraziatische lynx, serval, vissende kat, manoel, Europese wilde kat. De lynx in 8 parken.
- 29 vermeldingen in de hoofdtabel, waarvan 2 onzeker (Nordens Ark: Amoerluipaard en wilde kat; zie `TWIJFELGEVALLEN.md`).
- Route met alle soorten in vier parken: Parken Zoo, Nordens Ark, Skånes Djurpark, Ystad Djurpark.
- Recente geboortes: 4 Amoertijgers in Kolmården (3-6-2026) en 2 in het voorjaar van 2025, 3 Perzische luipaarden in Nordens Ark (mei 2026).
- Ruim 40 andere locaties onderzocht zonder katten (o.a. Furuviksparken, Universeum, Slottsskogen, Tropikariet, elandenparken, circussen). Orsa Rovdjurspark (dicht sinds 2022) en Frösö Zoo (dicht sinds 2019) staan bij “Gesloten”.

**Werkwijze**
- Officiële lijst: er is geen openbare landelijke lijst van dierentuinvergunningen (länsstyrelse). Gebruikt: Jordbruksverket “godkända avgränsade anläggningar” (05-10-2026), SDF (13 Zweedse leden), EAZA (18 Zweedse dierentuinen/aquaria) en Zootierliste (62 Zweedse vermeldingen bij 17 instellingen).
- Afbakening: particulieren mogen in Zweden geen wilde katten houden (SJVFS 2019:15) en roofdieren zijn in circussen verboden (Djurskyddsförordning 2019:66); er waren dus geen particulieren of circussen op te nemen.
- Zes onderzoeksagenten (lijsten, vier gebieden, opvang/particulieren/circussen) en één vervolgagent (twijfelgevallen). Type: dierentuin bij lidmaatschap van EAZA of SDF.
- De gids is met een script afgeleid van de Tsjechische (`bron/landbouw/se/tools/basis_omzetten.py`: Tsjechisch → Zweeds in de code, vaste teksten door een vertaalagent), gegevens via een vertaaltabel (`sv.json`, `bron_vert.json`). Kaart uit GISCO NUTS 2024 (län = NUTS 3).

**Gedeelde bestanden**: taal `sv` en land `se` in alle gedeelde lagen (zoals bij Tsjechisch); locatietypes in het Zweeds: dierentuin = “Zoo”, dierenpark = “Djurpark”. `jungle.py`: “1 plats / N platser i Sverige”. Hoofdpagina: Zweden met vlag, kaartvorm en zoomknop in alle lijsten; kaartkader naar het noorden vergroot (tot 69,4° N), Noorwegen en Finland grijs; landenlijsten in titels en beschrijvingen bijgewerkt (nu 15 landen · 576 locaties · 30 soorten).

**Gecontroleerd**: de Zweedse pagina in NL/EN/SV op 390 px (Chromium): geen fouten, geen horizontaal scrollen, geen Tsjechische, Deense of Portugese resten. Alle andere landpagina’s (alle talen) tekst voor tekst gelijk aan de vorige versie; hoofdpagina, top 10 en de soortpagina’s verschillen alleen door Zweden. WebKit niet getest.

## 22 oktober 2026 – Tsjechië

Nieuwe landpagina `tsjechie/` (bron: `bron/gidsen/cz.html`), in het Nederlands, Engels en Tsjechisch. Eén pagina met een filter per kraj (13 kraje met locaties; Karlovarský kraj heeft er geen) plus een groep “Reizende circussen”, met kaart, routeplanner, recente geboortes, soortpagina’s, filters op type en labels en het meldformulier. Duitsland, Polen, Slowakije en Oostenrijk staan grijs op de kaart.

**Aantallen**
- **44 locaties**, waarvan **37 met een bevestigde kat**: 15 dierentuinen (EAZA/UCSZOO), 1 safaripark (Dvůr Králové), 10 dierenparken, 8 particuliere houders (waarvan 3 circussen), 2 opvangcentra en het lynxverblijf van NP Šumava (Kvilda). Zeven locaties hebben alleen onzekere of niet te bezoeken katten (o.a. Kletečná, Zoopark Zvole, Animal Park Rabina, Ringelland).
- **23 soorten bevestigd**: leeuw, tijger, luipaard, jaguar, sneeuwluipaard, cheetah, poema, jaguarundi, Euraziatische lynx, Canadese lynx, rode lynx, serval, caracal, ocelot, margay, Geoffroy’s kat, Bengaalse kat, Soendanese luipaardkat, vissende kat, roestkat, manoel, Europese wilde kat, zandkat. Afrikaanse wilde kat en moeraskat alleen onzeker (Jihlava, Nová Říše).
- 175 vermeldingen in de hoofdtabel (zie `TWIJFELGEVALLEN.md` voor de onzekere).
- Route met alle soorten in zes parken: Zoo Plzeň, Zoo Hluboká, Zoo Tábor, Othello Park, Zoo Olomouc, Zoo Ostrava (de ocelot alleen in het particuliere Othello Park).
- Veel recente geboortes, o.a. cheetahs in Olomouc (6) en Praag (5), Sri Lanka-luipaarden in Ostrava (oktober 2026), Amoerpanters in Olomouc, leeuwen in Hodonín, servals in Dvůr Králové, tijgers in Hluboká.
- Ruim 50 andere locaties onderzocht zonder katten (o.a. alle erkende dierentuinen zonder katten, minizoo’s, gesloten parken, circussen zonder katten).

**Werkwijze**
- Officiële lijst: ministerie van Milieu, dierentuinen met licentie (29, lijst van 27-03-2025). Daarnaast UCSZOO (15 Tsjechische leden), EAZA (14) en Zootierliste (463 Tsjechische vermeldingen).
- Zeven onderzoeksagenten (lijsten, vijf regio’s, opvang/particulieren/circussen) en twee vervolgagenten (dierentuinen; particulieren en circussen). Besluit gebruiker (22-10-2026): circussen opnemen zoals in Italië; particuliere parken opnemen met kanttekening en status volgens toegang.
- Type: dierentuin bij lidmaatschap van EAZA of UCSZOO; particuliere parken zonder dierentuinlicentie als “particuliere houder”.
- Taxonomie: de Palawan-luipaardkat als Soendanese luipaardkat (Kitchener 2017); de Noord-Chinese luipaard als “Noord-Chinees (P. p. orientalis, voorheen P. p. japonensis)”.
- De gids is met een script afgeleid van de Deense gids (Deens → Tsjechisch in de code, `SPCS`, `CSD` …), de vaste teksten door een vertaalagent vertaald, de gegevens via een vertaaltabel. Kaart uit GISCO NUTS 2024 (kraje = NUTS 3).

**Gedeelde bestanden**: taal `cs` en land `cz` in alle gedeelde lagen (zoals bij Deens). `jungle.py`: in de kop van een soortpagina in het Tsjechisch het juiste meervoud (místo/místa/míst) en “v Česku”. Hoofdpagina: kaartkader iets breder (FULL 1140) zodat Oost-Tsjechië erop past; Polen, Slowakije en Hongarije grijs.

**Gecontroleerd**: de Tsjechische pagina in NL/EN/CS op 390 px (Chromium): geen fouten, geen horizontaal scrollen, geen Deense of Portugese resten. Alle andere landpagina’s (ook Denemarken) tekst voor tekst gelijk aan de vorige versie; hoofdpagina, top 10 en soortpagina’s verschillen alleen door Tsjechië.

## 22 oktober 2026 – Denemarken

Nieuwe landpagina `denemarken/` (bron: `bron/gidsen/dk.html`), in het Nederlands, Engels en Deens. Eén pagina met een filter per regio (de vijf Deense regio’s: Nordjylland, Midtjylland, Syddanmark, Sjælland, Hovedstaden), plus kaart, routeplanner, recente geboortes, soortpagina’s, filters op type en labels en het meldformulier. Duitsland en Zweden staan grijs op de kaart.

**Aantallen**
- **17 locaties**, waarvan **15 met een bevestigde kat**: 4 dierentuinen (Zoo København, Odense Zoo, Aalborg Zoo, Randers Regnskov; EAZA/DAZA), 3 safariparken (Knuthenborg, Givskud Zoo – Zootopia, Ree Park), 7 dierenparken (Krokodille Zoo, Pangea Park Falster, Blåvand Zoo, Skærup Zoo, Jyllands Park Zoo, Munkholm Zoo, Glad Zoo) en 1 opvangcentrum (Odsherred Zoo Rescue). Zoopark Sydsjælland heeft alleen onzekere vermeldingen; Hansenberg Zoo (schoolzoo in Kolding) is alleen op de open dag te bezoeken.
- **15 soorten bevestigd**: leeuw, tijger, luipaard, jaguar, nevelpanter, cheetah, poema, Euraziatische lynx, rode lynx, serval, caracal, ocelot, margay, vissende kat, zandkat.
- 41 vermeldingen in de hoofdtabel, waarvan 5 onzeker (zie `TWIJFELGEVALLEN.md`).
- Route met alle soorten in zes parken: Zoo København, Odsherred Zoo Rescue, Krokodille Zoo, Skærup Zoo, Ree Park, Randers Regnskov (alternatieven: Jyllands Park Zoo voor de caracal; Aalborg, Odense of Knuthenborg voor de tijger).
- Recente geboortes: Amoerpanter in Kopenhagen (23-09-2026), 8 leeuwenwelpen in Givskud (mei en juni 2026), 2 zwarte jaguars in Randers (februari 2026), leeuwenwelpen in Ree Park (oktober 2025), Odense (september 2025) en Blåvand (witte leeuwen, juli 2025), 2 Amoertijgers in Kopenhagen (juli 2025).
- Ruim 40 andere locaties onderzocht zonder katten (erkende aquaria en dierenparken, attractieparken, hertenparken, roofvogelcentra, circussen, gesloten).

**Werkwijze**
- Officiële lijst: Fødevarestyrelsen, “Godkendte zoologiske anlæg” (31 locaties, oktober 2026; formeel de lijst voor EU-handel, kleinere parken kunnen ontbreken). Daarnaast DAZA (15 leden), EAZA (12 Deense leden) en Zootierliste (alle ~200 kattenpagina’s, Aktuelle en Ehemalige: 91 Deense vermeldingen).
- Zes onderzoeksagenten (lijsten, vier regio’s, opvang/particulieren/circussen) en één vervolgagent voor de open punten (o.a. Glad Zoo: serval gevonden; Hansenberg: lynx; Skærup: lynx naar “Eerder hier”). Eén JSON-formaat, samengevoegd met een script; regio’s bepaald uit de coördinaten (NUTS 2024).
- Type: dierentuin bij lidmaatschap van EAZA of DAZA; safariparken en opvang houden hun eigen type.
- Circussen: wilde katten (menagerieën) verboden sinds 1962. Particulieren mogen geen roofdieren houden (BEK 1261/2015).
- De gids is met een script afgeleid van de Portugese gids: Portugees → Deens in de code (`SPDA`, `DAD`, `R1DA` …, `l-da`), de vaste teksten door een vertaalagent naar het Deens vertaald, daarna gegevens en tekstblokken (NL/EN, Deens via een vertaaltabel met de Engelse tekst als sleutel). Kaart uit GISCO NUTS 2024 (1:3 miljoen). Geen foto’s van parken gezocht.

**Gedeelde bestanden**: taal `da` (Deens) toegevoegd aan `taalmenu.js`, `locatietypes.json`/`.js`, `huisstijl.py`, `jungle.py`, `nieuw_ontwerp.py`, `test_ontwerp.py`, `bouw.py` (meldformulier) en `startdata.py`; land `dk` in alle landenlijsten. Adressen: æ → ae en ø → oe in `slug()` (`startdata.py`, `test_ontwerp.py` en de Deense gids; komt in geen andere gids voor, dus andere adressen veranderen niet).

**Hoofdpagina**: Denemarken heeft een vlag, kaartvorm en zoomknop, staat in “alle soorten”, “parken op aantal soorten”, het overzicht per land, het zoeken en de tellerregel (nu 13 landen · 521 locaties · 29 soorten). Zweden en Zuid-Noorwegen staan nu grijs op de Europakaart. Landenlijsten in titels en beschrijvingen (zeven talen) bijgewerkt. De hoofdpagina blijft zeven talen; Deens staat in het taalmenu van de Deense gids. De top 10 is niet veranderd.

**Gecontroleerd**: de Deense pagina in NL/EN/DA op 390 en 414 px (Chromium): geen fouten, geen horizontaal scrollen, geen Portugese of Nederlandse resten in het Deens, regiofilter, kaart, locatie- en soortpagina’s. Alle andere landpagina’s tekst voor tekst gelijk aan de vorige versie; hoofdpagina, top 10 en soortpagina’s verschillen alleen door Denemarken. WebKit niet getest (niet geïnstalleerd).

## 19 oktober 2026 – VK-gids: types langs de BIAZA/EAZA-regel

Alle 88 VK-locaties vergeleken met de ledenlijst van BIAZA (biaza.org.uk/members/all, 127 leden) en EAZA (strapi.eaza.net/api/members en map.eaza.net). Van dierenpark naar dierentuin: Wingham Wildlife Park en Ponderosa Zoo (BIAZA-lid), Capel Manor Gardens en Fenn Bell Conservation Project (voorlopig BIAZA-lid). Alle andere "dierentuinen" zijn lid van BIAZA of EAZA (Cotswold, Howletts en Port Lympne alleen EAZA). Wildwood Escot onduidelijk (BIAZA-pagina van Wildwood Trust noemt alleen Kent), daarom ongewijzigd. Wildparken en opvangcentra vallen niet onder deze regel en zijn niet veranderd.

## 19 oktober 2026 – Aantallen in het wild aangevuld

Op verzoek ingevuld als ondergrens in `WILD` van alle gidsen: marmerkat "> 10.000" (IUCN 2016, volwassen dieren), vissende kat "3.200–7.500" (volwassen dieren, bron onzeker), rode lynx "> 2.350.000" (alleen VS, alle dieren; Roberts & Crimmins) en Euraziatische lynx "> 69.500" (optelling per regio, alle dieren, Azië onvolledig). De uitleg op de site noemt "volwassen dieren volgens de IUCN"; voor de twee lynxen klopt dat strikt genomen niet.

## 19 oktober 2026 – Portugees als zevende taal van de hoofdpagina

De hoofdpagina, top 10 en de soortpagina's (`/soort/…`) hebben nu ook Portugees (Europees Portugees), met knop PT in de taalkeuze. Aangepast: `start.html` (T() met 7e argument, vaste teksten `l-pt`, landnamen, maanden, statussen, IUCN, taalherkenning), `startdata.py` (soortnamen op index 8 in de locaties en 12 in `D.sp`, aantal jongen met eigen regels `_N_PT`), `bouw.py` (datum, locatietypes), `portugese_namen.json` (uit `SPPT` in de Portugese gids), `locatietypes.json` (`uitleg_pt`; de bestaande `pt`-namen ongewijzigd), `top10.json` (7e uitlegzin), `test_ontwerp.py` en `nieuw_ontwerp.py` (teksten van de Europa-laag, soortinfo uit `SPPT`). Gecontroleerd: alle schermen in PT (Chromium en WebKit, 414 px), en NL/EN/FR/DE/IT/ES tekst voor tekst gelijk aan de vorige versie; Portugal-gids ongewijzigd.

Besloten: geen Franse overzeese gebieden, Zwitserland niet in het Frans (staan in `OPEN.md` onder "Bewust niet").

## 19 oktober 2026 – Europa-onderbalk opent bovenaan

Op de hoofdpagina (en top 10) opent Kaart, Landen of Soorten in de onderbalk nu altijd bovenaan, ook als je eerst naar beneden had gescrold (`test_ontwerp.py`, klik op `#nw-sbar-start`). Getest in Chromium en WebKit op 414 px; geen doorlopende DOM-wijzigingen.

## 19 oktober 2026 – Top 10 bijgewerkt

Later: de landknoppen boven de top 10 zijn weg (`renderTop` in `start.html`). In de Portugese gids zegt de vaste tekst bij Lissabon nu acht soorten in plaats van negen (NL/EN/PT), gelijk aan de gegevens.

Op verzoek van de gebruiker (`bron/top10.json`, lijst `vast`). Nieuwe volgorde: Lumigny, Faunapark Flakkee, Le Domaine des Fauves, Pairi Daiza, Hoenderdaell / Stichting Leeuw, Jardim Zoológico de Lisboa, Safari Madrid, Felidae Barnim, Exmoor Zoo, La Torbiera. Eruit: ZooParc de Beauval, Zoo du Bassin d’Arcachon, Wilhelma, Zoo Leipzig en Safaripark Beekse Bergen. The Big Cat Sanctuary (VK, hoogste score buiten de lijst) bewust niet: te duur voor bezoekers. Uitlegzinnen voor de vijf nieuwe parken in zes talen. Alleen `top10` in de startgegevens is veranderd; top 10 gecontroleerd op 390 px in NL/EN/DE/ES.

## 19 oktober 2026 – Voet als horizontale tak

Op alle pagina's met de jungle-stijl is de voet nu een getekende tak over de hele breedte: de luipaard ligt erop (buik precies op de bovenrand, poten en staart over de rand), rechts een takje met bladeren, en de Ko-fi-tekst, -knop en de regel "Samengesteld door J. Gelens" staan op de tak. De tak wordt in JS op de echte maat getekend (`TAK_JS`/`TAK_CSS` in `bron/jungle.py`), werkt voor `footer.hs-foot` (landpagina's, losse pagina's) en `footer.foot` (hoofdpagina, top 10, soortpagina's). Testpagina `/voorbeeld-jungle/tak/` weer weggehaald.

## 19 oktober 2026 – Knop "Naar boven" werkt weer

Op de schermen van de landpagina's (Kaart, Locaties, Soorten, Meer-subpagina's) scrolde "Naar boven" naar de onderkant van de oude gidskop, die in het nieuwe ontwerp verborgen is: de pagina sprong maar een paar pixels. Nu gaat hij altijd helemaal naar boven (klik-afvanger in `bron/test_ontwerp.py`). Getest in alle landen.

## 19 oktober 2026 – Kop startscherm landpagina's gelijk aan de andere koppen

De groene kop van het startscherm (Kaart) op de landpagina's was net anders dan die van Locaties, Soorten en Meer: 1 px lager, vlag 2 px lager, smallere letterafstand in de titel en een hogere golf. Nu exact gelijk (gemeten in alle landen op 390 en 414 px). CSS in `bron/jungle.py` onder de `.nt-kop`-regels.

## 19 oktober 2026 – Scherm Locaties als kaartjes, knoppen zonder hout

- Scherm Locaties op alle landpagina's: elke locatie een los kaartje met het aantal bevestigde soorten als goudgele badge rechtsboven ("1 onzeker" eronder als dat er is), het type-icoon bovenaan naast de naam en soortrondjes (foto's, bevestigd eerst, onzeker met stippelrand, maximaal 6 en dan "+n") in plaats van de afgekapte beschrijving. Volgorde ongewijzigd (meeste soorten eerst). Zoeken doorzoekt de beschrijving nog steeds. Code: `kaartje()` in `bron/test_ontwerp.py`, kleuren in `bron/jungle.py`.
- Knoppen (land, regio, type, filters) in stijl A "bladgroen": effen lichte knop met donkergroene rand, gekozen donkergroen met goudgele tekst (`KNOP`/`KNOP_AAN` in `bron/jungle.py`, vervangt `HOUT`).

## 19 oktober 2026 – Losse park- en soortpagina's net als de gids

De losse pagina's (`/<land>/locatie/…`, `/<land>/soort/…`) hebben nu dezelfde kop als in de gids: landvlag voor de titel, "N locaties in <land>" bij soorten en het hartje rond op de foto. Het hartje gebruikt dezelfde favorieten (`nt-fav`) als de gids. Vlaggen en landnamen komen uit `bron/start.html`; code in `bron/jungle.py` (`los_js()`, `hart()` in `DETAIL_JS`).

## 18 oktober 2026 – Foto's Eindhoven Zoo en Hoenderdaell

Locatiefoto's toegevoegd in de Nederlandse gids (`LOCPHOTOS`): Eindhoven Zoo (Siberische tijger, Cro-Cop, CC BY 4.0, `img/265.webp`) en Landgoed Hoenderdaell / Stichting Leeuw (leeuw, Ingredia, CC BY 4.0, `img/266.webp`). Nog zonder foto: Faunapark Flakkee, BestZoo, Taman Indonesia, Stichting AAP. De voorgestelde foto voor BestZoo ("Lioness from Perth Zoo") is niet gebruikt: die is in Perth gemaakt en BestZoo heeft geen leeuwen.

## 18 oktober 2026 – Meer op de landpagina's zonder blok Bezoekersgids

Op het scherm Meer van alle landpagina's zijn de kop "Bezoekersgids" en de links eronder (Alle landen, Alle soorten, Top 10, Over deze gids, Spottersgids) weggehaald (`MEER_NIEUW` in `bron/test_ontwerp.py`). Ze staan nog in het ☰-menu.

## 18 oktober 2026 – Interne controle en tellingen gelijkgetrokken

Hele site intern nagelopen (tellingen, teksten, links, alle talen op 390 px). Verbeterd:
- Routeplanner: de groep "Onzeker" wordt nu berekend uit de gegevens (`UNSURE` in alle gidsen); hij stond verouderd in Duitsland, Frankrijk, Oostenrijk, Zwitserland en het VK. Lege kop "Onzeker" verdwijnt.
- Eén telregel: getallen bij een soort of locatie tellen alleen bevestigde vermeldingen (aanwezig, tijdelijk niet zichtbaar, vertrek aangekondigd, rondleiding); onzekere staan er apart achter ("10 soorten · 1 onzeker"). Geldt voor "Alle katten" met een regio (landpagina's) of land (hoofdpagina), de locatie- en soortkaartjes en de soortinfo op de landpagina's, de knoppen op de soortpagina's `/soort/…` en de losse locatiepagina's. Soorten die in een regio of land alleen onzeker zijn, krijgen daar een stippelrand.
- Typeknoppen op de landpagina's volgen de gekozen regio.
- Hoofdpagina: onder "In beeld" staat hoeveel locaties niet op de kaart staan (reizende circussen, Canarische Eilanden).
- Duitsland, Frankrijk, Oostenrijk, Zwitserland en het VK hebben nu ook 43 soorten (oostelijke tijgerkat, wolkentijgerkat, tilcayo) met de zin over de indeling; alle "niet te zien"-aantallen +3. Hoofdletters in de Duitse kopjes ("In Deutschland", "In Österreich", "In der Schweiz").
- Vaste teksten: België 29 soorten niet te zien; "bevestigd op N locaties" telt overal locaties met een bevestigde kat (België 13, Italië 38, Spanje 41, Ierland 5, Portugal 6, VK Zuidoost-Engeland 16, Oost-Engeland 17, East Midlands 6; lynx en wilde kat in die VK-regio's).
- Italiaanse gids: routeplanner-uitleg, voetregel en "soorten katachtigen" op de parkpagina's in het Italiaans. Franse gids: bronregels "maandoverzicht" vervangen.
- Losse soortpagina's per land: "lijkt op"-links naar soorten zonder pagina in dat land gaan naar de Europese soortpagina (of de Spottersgids, of de gids).
- Nagaan (niet veranderd): zie `bron/OPEN.md` (mogelijk dubbele geboortes, Exotic Pet Refuge).

## 18 oktober 2026 – Aantallen in het wild aangevuld

Ontbrekende schattingen (24 soorten) onderzocht; alleen betrouwbare IUCN-cijfers voor volwassen dieren ingevuld: Geoffroy’s kat ca. 528.000 en zandkat ca. 27.300 (in alle gidsen). Overige uitkomsten en twijfelgevallen in `bron/OPEN.md` en `bron/wild_onderzoek_2026-10.json`.

## 18 oktober 2026 – Inzoomen op een gekozen regio

Landpagina's: kies je een regio (deelstaat, provincie, comunidad …), dan zoomt de kaart in op de locaties van die regio; "Alle regio's" zet de kaart weer op heel het land. `huisstijl.py` geeft daarvoor `window.__HSZOOM(svg, viewBox|null)`; `regioZoom()` in `test_ontwerp.py`.

## 18 oktober 2026 – Balearen op de kaart, melding bij lege kaart

- De Balearen staan nu op de kaart van Spanje en op de Europakaart (eilandvormen uit Natural Earth 1:50m via world-atlas; coördinaten Natura Parc 39,610/2,837 en Safari Mallorca 39,582/3,361 uit OpenStreetMap). Kaartkader van de Spaanse gids iets breder (viewBox 442). De Canarische Eilanden blijven op verzoek van de kaart (te ver weg); de teksten daarover zijn aangepast (NL/EN/ES).
- Landpagina's: kies je een regio zonder stippen op de kaart (bijv. Canarische Eilanden), dan staat er op de kaart "… staat niet op de kaart. Bekijk de N locaties hieronder ↓" (tik = naar de lijst).
- Volledige bouw gedraaid (`bron/bouw.py`); de losse pagina's kregen daarbij ook de nieuwste CSS.

## 18 oktober 2026 – Routeplanner "Al wel" en foto zwarte panter

- Routeplanner: boven "Nog niet:" staat nu ook "Al wel:" met de soorten die je met je keuze al ziet (alle landen, alle talen).
- Kleur & hybriden: foto van een zwarte panter bovenaan (`img/nieuw/zwarte-panter.webp`; "Melanistic leopard at Tadoba.jpg", Atul.rewild, Wikimedia Commons, CC BY-SA 4.0, met naamsvermelding en link).

## 18 oktober 2026 – Scherm Meer op de hoofdpagina

Meer in de onderbalk van de hoofdpagina (ook vanaf top 10 en de soortpagina's) opent nu het scherm `#meer` in plaats van het menu: Favorieten, Top 10, Recent geboren, Parken op aantal soorten, Soorten locaties, Over deze gids en de Spottersgids (eigen taal), elk met icoon. Ko-fi staat alleen onderaan. Het ☰-menu blijft. Volgorde Meer op de landpagina's: In het kort, Actueel, Kleur & hybriden, Routeplanner, Hoofdtabel, Over, Rapporteer.

## 18 oktober 2026 – Zoekvelden en volgorde onderbalk

Zoekveld bovenaan Locaties (naam, plaats en beschrijving) en bovenaan Soorten (Nederlandse en Engelse naam), op alle landpagina's. Onderbalk nu Kaart · Locaties · Soorten · Meer (ook op de losse park- en soortpagina's).

## 18 oktober 2026 – Favorieten naar de hoofdpagina

Favorieten zijn één lijst voor alle landen (localStorage `nt-fav`, items met land; oude `nw-fav` wordt overgenomen, het land wordt opgezocht). Opslaan kan met het hartje bij parken en soorten in de landgidsen, in het infovak van de Europakaart en op de Europese soortpagina's. De lijst staat op de hoofdpagina: menu → Favorieten (`#favorieten`, per land gegroepeerd, parken eerst; een park opent de landgids, een soort de soortpagina van het land waar hij bewaard is, of de Europese soortpagina). Op de landpagina's staat Favorieten niet meer onder Meer.

## 18 oktober 2026 – Meer zonder dubbelingen

Op het scherm Meer van de landpagina's: Ko-fi niet meer in de lijst (staat onderaan), de Spottersgids alleen in de eigen taal, en kaart Europa, Recent geboren, Parken op aantal soorten en Soorten locaties weg (staan in het menu bovenaan). Over (`MEER_OUD`/`MEER_NIEUW` in `bron/test_ontwerp.py`).

## 18 oktober 2026 – Land/regio en soort: wat niet samengaat grijs

Hoofdpagina: kies je een land, dan worden de soortrondjes van katten die daar niet zitten grijs en schuiven achteraan (achter een streepje); "Alle katten" toont het aantal soorten in dat land. Kies je een soort, dan gebeurt hetzelfde met de landknoppen, en staat bij de andere landen het aantal locaties met die soort. Een grijze knop blijft aantikbaar: het andere filter gaat uit en er verschijnt kort een melding ("… niet te zien in …"). Op de landpagina's werkt het zo met regio's en soorten. Beschikbaarheid: elke vermelding telt (ook onzeker), net als op de kaart.

## 18 oktober 2026 – Hoofdpagina, soortpagina's en losse pagina's gelijkgetrokken

- Hoofdpagina en top 10: onderbalk Kaart · Landen · Soorten · Meer; de tabbladen Kaart/Landen/Soorten bovenaan zijn weg; het uitlegvak bij de kaart is één regel zolang er geen locatie gekozen is; de typeknoppen staan altijd onder de kaart (knop Legenda weg).
- Soortpagina's `/soort/…` (29): dezelfde onderbalk; IUCN-status vervangen door "In het wild (geschat)" (waarde uit `WILD`, anders "onbekend"); "In het wild" (gebied) heet nu "Verspreiding"; hoofdletter in de Spottersgids-link (bijv. "Zie de Afrikaanse wilde kat"); type-icoon bij de locaties onder "Waar te zien".
- Losse park- en soortpagina's per land (700): onderbalk Kaart · Soorten · Locaties · Meer, titel "Soorten" i.p.v. "Per kat", "Aanwezig" verborgen.
- Gecontroleerd: hoofdpagina, top 10, alle soortpagina's en een steekproef losse pagina's op 390 px; soortpagina in NL/EN/DE.

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
