# Overdracht (30 oktober 2026) — voor een nieuw gesprek

**Werkwijze vanaf nu:** één land (of één onderhoudsklus) per gesprek. Volg **`bron/landbouw/CHECKLIST.md`** stap voor stap en vink af in `bron/landbouw/<code>/STAPPEN.md`. Onderzoeksagenten en vertaalagenten op het lichtere model (`sonnet`); redactie, teksten en controle zelf. Testscripts staan in `bron/controle/` (`servers.sh`, `landtest.py`, `jscheck.py`, `vergelijk.py`).

## Waar we staan
- **20 landen**, alles op `main` en live (https://yeetkitty.github.io/wildekattengids/). Laatste: Roemenië (30-10-2026), Hongarije, Polen, Finland, Noorwegen, Zweden (23-10-2026).
- Afspraak: kleine opmaakfixes na testen meteen naar `main`; nieuwe landen en inhoud eerst vragen.
- Antwoord in het Nederlands, kort; bij “wat stel je voor” alleen een voorstel; na elke update de link.

## Eerstvolgende
- De gebruiker kiest het volgende land, of een **onderhoudsgesprek** voor `bron/OPEN.md` (open: “1 locaties”-vraag, Zoo Jihlava, nagaan-lijsten per land, WebKit, grijze buurlanden oostelijk op de Europakaart).
- Nog niet gedaan: Slowakije, Slovenië/Kroatië, de Baltische staten, Bulgarije, Griekenland.

# Overdracht (23 oktober 2026, later) — voor een nieuwe chat

Lees eerst `bron/LEESMIJ.md` (opbouw, bouw, telregel en de lessen per land), **`bron/landbouw/LEESMIJ.md`** (zo maak je een nieuw land), `bron/OPEN.md` en bovenaan `VOORTGANG.md`. Gebruik de skill “wilde-katachtigen-gids”.

## Waar we staan
- **20 landen** in de gids (met **RO**, Roemenië, 30-10-2026, NL/EN/RO: 20 locaties, 16 bevestigd, 9 soorten; bron in `bron/landbouw/ro/`; met **HU**, Hongarije, 23-10-2026, NL/EN/HU: 20 locaties, 16 soorten; bron in `bron/landbouw/hu/`; met **PL**, Polen, 23-10-2026, NL/EN/PL: 30 locaties, 21 soorten; bron in `bron/landbouw/pl/`; met **FI**, Finland, 23-10-2026, NL/EN/FI: 5 locaties, 8 soorten; bron in `bron/landbouw/fi/`): NL, BE, LU, DE, FR, AT, CH, UK, IE, IT, ES, PT, DK, CZ, **SE** (Zweden, 23-10-2026, NL/EN/SV) en **NO** (Noorwegen, 23-10-2026, NL/EN/NB). Noorwegen: 6 locaties, 6 soorten; bron in `bron/landbouw/no/`.
- Zweden: 11 locaties, 11 soorten; bron in `bron/landbouw/se/` (`patch.py` → `se_final.json`, `teksten.py`, `gen.py`). De Europakaart is naar het noorden vergroot (tot 69,4° N).
- Open voor Zweden: zie `bron/OPEN.md` (Nordens Ark: Amoerluipaard en wilde kat; Öland: tijger).
- Tsjechische gids: Iberische lynx “Španělsko a Česko” rechtgezet (23-10-2026).
- **Afspraak (23-10-2026):** kleine opmaakfixes na testen meteen naar `main` pushen, zonder eerst te vragen. Nieuwe landen en inhoud: wel eerst vragen.
- Laptop (23-10-2026): menubalk ook op landpagina's onderaan; pijltjes, muiswiel en slepen bij schuifrijen (`SCHUIF_JS` in `bron/jungle.py`).
- Pushen naar `main` werd op 23-10-2026 door de automatische toestemmingscontrole geblokkeerd; vraag de gebruiker of het mag.

# Overdracht (22 oktober 2026, eind van de dag) — voor een nieuwe chat

Lees eerst `bron/LEESMIJ.md` (opbouw, bouw, telregel en de lessen per land), **`bron/landbouw/LEESMIJ.md`** (zo maak je een nieuw land, stap voor stap), `bron/OPEN.md` en bovenaan `VOORTGANG.md`. Gebruik de skill “wilde-katachtigen-gids”.

## Waar we staan
- **14 landen** in de gids: NL, BE, LU, DE, FR, AT, CH, UK, IE, IT, ES, PT, **DK** (22-10-2026, NL/EN/DA) en **CZ** (22-10-2026, NL/EN/CS). Hoofdpagina: 14 landen · 565 locaties · 29 soorten.
- Alles staat op `main` en is live (https://yeetkitty.github.io/wildekattengids/). De werktakken `denemarken-wip` en `tsjechie-wip` zijn volledig in `main` opgenomen en mogen weg.
- **Nieuw**: `bron/landbouw/` met de bouwscripts en gegevens van Denemarken en Tsjechië (`gen.py`, `patch.py`, `teksten.py`, `_final.json`, vertaaltabellen, kaart). `python3 bron/landbouw/<land>/gen.py` maakt `bron/gidsen/<land>.html` opnieuw (byte voor byte gelijk aan de huidige gids). `bron/landbouw/kaart_maken.py` maakt de kaart van een nieuw land.

## Volgend land
- De gebruiker wil verder met een volgend land; welk land is nog niet gekozen. Eerder voorgesteld: **Zweden** (± 30–40 locaties; Kolmården, Borås, Nordens Ark, Orsa, Parken Zoo, Skånes Djurpark; vergunningen via Jordbruksverket, Svenska Djurparksföreningen), Polen (groot, veel opvang), Slowakije of Hongarije (buren van Tsjechië, al grijs op de Europakaart), Noorwegen (klein). Vraag eerst welk land; bij “wat stel je voor” alleen een voorstel.
- Werkwijze: volg `bron/landbouw/LEESMIJ.md`; neem `bron/landbouw/cz/` als voorbeeld (meest recent, met particulieren en circussen). Talen: NL + EN + landstaal. Leg de afbakening vooraf voor (circussen, particulieren zonder vergunning). Besluit bij Tsjechië: circussen zoals in Italië; particulieren opnemen met kanttekening en status volgens toegang.
- Valt het land buiten het kaartkader van de hoofdpagina (`FULL` en de viewBox van `#map` in `start.html`, nu breedte 1140 ≈ 19,7° O; boven 59° N), vergroot dan het kader (lessen Ierland/Tsjechië in `bron/LEESMIJ.md`). Buurlanden grijs: `NBR` in `start.html`.

## Open punten (kort; details in `bron/OPEN.md`)
- **Zoo Jihlava** (CZ): eigen site was onbereikbaar; negen kleine katten staan op onzeker. Opnieuw nagaan, in `bron/landbouw/cz/cz_final.json` op “g” zetten, `gen.py` en `bouw.py` draaien, en de getallen in `cz/teksten.py` aanpassen als ze veranderen.
- **“1 locaties”**: in de kop van een soortpagina met één locatie staat in het Nederlands (en de andere talen behalve CS/DA) het meervoud (`jungle.py`, regel met `LW`). Aan de gebruiker gevraagd of dat rechtgezet moet worden; nog geen antwoord.
- **Claude-pagina** (`_claude/claude.html`) is gebouwd maar niet opnieuw gepubliceerd.
- **WebKit/Safari** niet getest voor DK en CZ (`python3 -m playwright install webkit`).
- Particulieren en circussen in CZ zijn momentopnames (Ringelland, Kletečná, Zvole, Rabina, circussen).

## Afspraken met de gebruiker (J. Gelens)
- Antwoorden in het Nederlands, kort. Bij “wat stel je voor” alleen een voorstel. Alleen wijzigen wat gevraagd is. Na elke update de link naar wat veranderd is.
- Tussenwerk committen op een werktak (de stop-hook vraagt om commit en push); pas naar `main` als alles gebouwd en gecontroleerd is.
- Gebruik geen `pgrep`/`pkill -f` met een patroon dat in je eigen opdracht staat (dat stopt je eigen shell); stop processen op PID.

# Overdracht (22 oktober 2026, avond)

## 22 oktober 2026: Tsjechië
- Nieuwe gids `/tsjechie/` (NL/EN/CS, bron `bron/gidsen/cz.html`), 44 locaties, 23 soorten, inclusief particuliere houders en circussen (besluit gebruiker). Zie `VOORTGANG.md`, `TWIJFELGEVALLEN.md` en `bron/OPEN.md` (Zoo Jihlava opnieuw nagaan).


## 22 oktober 2026: Denemarken
- Nieuwe gids `/denemarken/` (NL/EN/DA, bron `bron/gidsen/dk.html`), 17 locaties, 15 soorten; zie bovenaan `VOORTGANG.md`, `TWIJFELGEVALLEN.md` en `bron/OPEN.md`.
- Deens (`da`) staat nu in alle gedeelde lagen; land `dk`. Lessen in `bron/LEESMIJ.md` onder “Denemarken toevoegen”.
- Zweden en Zuid-Noorwegen grijs op de Europakaart (`NBR` in `start.html`).
- De Claude-pagina (`_claude/claude.html`) is gebouwd maar niet opnieuw gepubliceerd.

# Overdracht (19 oktober 2026, avond)

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
- Opgelost (19-10-2026): op kaarten met groepjes (o.a. Frankrijk, Duitsland, Spanje, Italië, VK) tekende de kaart elk beeldje opnieuw, doordat het groeperen zijn eigen wijzigingen als filterwijziging zag (`groepen()` in `huisstijl.py`, nu met `takeRecords()`).
- Testpagina's (noindex, niet gelinkt): `/voorbeeld-jungle/` (drie stijlvoorbeelden, `test/` per paginasoort, `ogen/`).

## Avond 19-10-2026
- **☰-menu's gelijk** (`huisstijl.py` voor de landen, `start.html` + `test_ontwerp.py` voor Europa). Het ☰-menu in een land is het menu van de hele Europa-gids; de onderbalk gaat over het land zelf.
  - Europa: Favorieten, Top 10, Recent geboren, Parken op aantal soorten, Soorten locaties; onder MEER: Over, Spottersgids, Ko-fi.
  - Landen: eerst Kaart (Europese kaart), Alle landen, Alle soorten, daarna hetzelfde blok. Favorieten (`fav` in `huisstijl.py`) wijst naar de Europese lijst `#favorieten`.
  - Recent geboren heeft overal een ster; de MEER-kop is overal klein en grijs (override in `jungle.py`); Ko-fi-tekst overal "Steun de gids op Ko-fi".
- **Safari en #meer**: losse schermen (#meer, #favorieten, #geboren, #perpark, #typen, #over) hebben dezelfde id als het adres, dus Safari sprong erheen en de kop viel onder de groene balk. Opgelost met `scroll-margin-top:100vh` op `section.page` en een vroeg script in `start.html` dat meteen `pagemode` zet (geen flits van de kaart). `bouw.py` zoekt `<script>\n(function(){` in `start.html`: zet nieuwe scripts in de kop altijd in een eigen `<script>`-blok.
- **Batterij**: zie "Opgelost" hierboven (kaart tekende elk beeldje opnieuw).
- **Kopjes boven de kaart** (met dubbele punt): Europa "Kies een land:" en "Kies een kat:"; landen "Kies een deelstaat:" / "Kies een regio:" / "Kies een provincie:" (in de gidsen zelf, `rg-lab`) en "Kies een kat:" (`test_ontwerp.py`). Nederland, België en Luxemburg hebben geen regioknoppen.
- **Gekozen soort**: overal één regel "Naam · N locaties · Soortpagina →" (Europa: `catnote` in `start.html`, zonder Latijnse naam en zonder "Alle katten tonen"; landen: `spinfo()` in `test_ontwerp.py`).
- **Top 10**: vlag vast links, lange plaatsnaam loopt ernaast door (`.toplist .plc`).
- Controle deze avond met Playwright (Chromium en WebKit) op 414 px; WebKit-browser: `python3 -m playwright install webkit`. Een echte iPhone kan afwijken; laat de gebruiker het nakijken.

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
