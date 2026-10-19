# Overdracht – Spottersgids voor wilde katten (Wild Cat Spotter's Guide)

Maker: J. Gelens. Stand: 16 oktober 2026. Alle 42 soorten hebben een soortpagina. De gids staat live op GitHub Pages.

## Waar staat alles
- **Live (openbaar): https://yeetkitty.github.io/wildekattengids/spottersgids/** – GitHub Pages publiceert de branch `main` van `yeetkitty/wildekattengids` direct (geen workflow; `.nojekyll` in de root). Live sinds 16-10-2026 via PR #1.
- **Repo:** `yeetkitty/wildekattengids`, map `spottersgids/`. Werkbranch: **`spottersgids-europa`** (na PR #1 opnieuw opgezet vanaf `main`). Niets buiten `spottersgids/` aanraken: de rest is de bestaande dierentuingids (https://yeetkitty.github.io/wildekattengids/, niet aanpassen).
- **Oud artifact (privé), niet meer bijwerken:** https://claude.ai/artifact/4Pmep6UwbY4aoyRyXXfRRX – staat op de versie van 16-10-2026 met de foto's ingebakken (12,7 MB). Gebruiker: "laat het oude artifact maar". Losse foto-bestanden laden niet in de Claude-app (twee keer geprobeerd), daarom is de gids verhuisd naar GitHub Pages. De huidige `index.html` werkt niet meer als artifact.
- **Bron van de soortgegevens:** artifact "De KATalogue" https://claude.ai/code/artifact/ba3edb6b-d786-4e68-906b-779c6b5cb3ea (42 soorten, foto's + credits, verspreidingskaarten, IUCN). Al uitgepakt naar `bron/katalogue.json`, `bron/land.txt` en `img/NN-i.jpg`.

## Werkwijze per wijziging
1. `git fetch origin main`; werk op `spottersgids-europa`. Is de vorige PR al samengevoegd, zet de branch dan eerst opnieuw op: `git checkout -B spottersgids-europa origin/main`.
2. Wijzig `bron/template.html`, `bron/build.py` of `data/*.json` – alleen wat gevraagd is.
3. Bouwen: `cd spottersgids && python3 bron/build.py` (de melding over Ndutu bij soort 1 is bekend en onschuldig).
4. Lokaal testen zoals Pages het serveert: `python3 -m http.server 8765` in de repo-root, dan `http://localhost:8765/spottersgids/` (Playwright met Chromium uit `/opt/pw-browsers` werkt; Python-pakket `playwright` eventueel eerst `pip install`). Telefoon testen met `is_mobile=True`.
5. Committen en pushen naar `spottersgids-europa` (afspraak: na elke wijziging).
6. Live zetten: **Claude zet het zelf live** (afspraak 16-10-2026, "gelijk live"): na testen pushen naar `spottersgids-europa` én naar `main` (`git push origin spottersgids-europa:main`, fast-forward). Geen pull request meer nodig. Daarna ±1 minuut tot de site bijgewerkt is.

## Opbouw van `spottersgids/`
| Pad | Wat |
|---|---|
| `bron/template.html` | De hele site (HTML/CSS/JS, één pagina met #-routes). `__DATA__` wordt bij het bouwen vervangen. Ko-fi-link: `KOFI_URL` (= https://ko-fi.com/katalogue). Begint met `<!doctype html>` + viewport-meta (nodig voor Pages). |
| `bron/build.py` | Bouwt `index.html`. `PAGES` = soortnummers met een pagina (alle 42). Foto's zijn losse bestanden: groot = `img/NN-i.jpg` (origineel, niet opnieuw gecomprimeerd), klein = `foto/NN-i-k.webp` (200 px, door de bouw gemaakt) voor fotorij, lijstjes en Katten in Europa. |
| `bron/borders.json` | Landsgrenzen + landnamen (NL/EN) voor de soortkaart, gemaakt met `bron/borders.mjs` (node; npm-pakketten world-atlas, topojson-client, i18n-iso-countries, d3-geo). Alleen opnieuw maken als dat nodig is. |
| `data/<nr>.json` | Onderzoek per soort: intro, plekken (score 1–5, seizoen, tijdstip, tocht, bronnen), tips, bedreigingen, status, bronnen – NL en EN. |
| `data/topspots.json` | Oorspronkelijke topspotlijst; telt alleen nog als "deze plek mag topspot zijn bij score 4". |
| `data/alias.json` | Samenvoegen van dezelfde plek onder verschillende id's. |
| `data/extra_cont.json` | Extra werelddelen bovenop de KATalogue (luipaard, Afr. wilde kat, moeraskat → ook Europa). |
| `data/text.json`, `data/europe.json` | Pagina's Verantwoord spotten, Katten in Europa, Paklijst, Over mij (NL/EN). |
| `TWIJFELS.md` | Alle twijfels en redactiekeuzes per soort en per ronde. |
| `index.html` | Gebouwde startpagina (klein omhulsel). Oude #-adressen (bijv. `#soort-27`) werken nog. |
| `data.js`, `app.js`, `style.css` | Gebouwd: gegevens, script en stijl uit de template, gedeeld door alle pagina's (met `?v=`-versie tegen oude cache). Niet met de hand wijzigen. |
| `<nl-naam>/index.html`, `en/<en-name>/index.html` | Gebouwd: losse soortpagina per taal (84 stuks) voor Google, met eigen titel, beschrijving, canonical/hreflang en voorgerenderde tekst. `<base href>` wijst naar de map spottersgids. |
| `sitemap.xml` | Gebouwd: start + 84 soortpagina's. |
| `img/`, `foto/` | Foto's (groot jpg, klein webp); horen in de repo, Pages serveert ze. |

Topspot-regel in de bouw: plek met score 5 op een soortpagina = topspot; score 4 alleen als hij in `topspots.json` voor die soort staat.

## Afspraken met de gebruiker (belangrijk)
- **Alleen aanpassen wat gevraagd wordt.** Bij onduidelijke wensen **doorvragen**; bij een keuze eerst een voorstel met advies geven ("Wat stel je voor" = opties + aanbeveling, nog niet bouwen).
- Na elke wijziging committen, pushen en direct live zetten (naar `main`).
- Na elke update de link sturen naar wat er veranderd is (bijv. https://yeetkitty.github.io/wildekattengids/spottersgids/wilde-kat/), of naar de startpagina als het de hele site raakt.
- Taal: Nederlands naar de gebruiker; site NL/EN. Gidsnamen uit de KATalogue (bijv. sneeuwpanter, Sundaluipaardkat, het luipaard). Let op het Duitse "stuft/stufte" in statusteksten → "deelt in"/"zette".
- Schrijfstijl: avontuurlijk, eerlijk, "je"; intro eindigt met "Kans: X – …".
- Kansscore eerlijk (5 bijna zeker … 1 alleen geluk/cameravallen).
- **Geen namen van reisorganisaties/lodges** in tekst of brontitels; geen hun sites als bron. Uitzondering (16-10-2026): reisverslagen van reisorganisaties die op mammalwatching.com staan mogen als bron blijven (naam alleen in de URL, niet in titel of tekst). Excursies wél concreet beschrijven ("excursies moeten er juist in").
- Plekken alleen op gebiedsniveau, markers op het midden van het gebied; geen holen/wissels/rustplekken.
- **Niet lokken:** voederplekken niet als aanbevolen plek (bij wolkentijgerkat twee geschrapt).
- Ontwerp: één lichte stijl (donker vond de gebruiker te donker). Kaart opent als eerste tabblad.
- De gids mag openbaar zijn en gevonden worden.

## Wat er gebouwd is (functies)
- Meldpagina `#melden` (en `#melden-<nr>` met soort vooraf gekozen), 16-10-2026, net als 'Rapporteer' in de dierentuingids: verstuurt via Web3Forms (zelfde sleutel `W3F_KEY` als de dierentuingids) naar de maker. Keuzes: kat gezien / plek ontbreekt / info klopt niet / iets anders, soort, plek (of andere plek), datum, opmerkingen (max. 500), samenvatting. Link in menu Meer, op Over mij en onderaan elke soortpagina. Testen met een nagebootste verzending (Playwright route), niet echt versturen.
- Losse soortpagina's (16-10-2026): NL op `/spottersgids/manoel/`, EN op `/spottersgids/en/pallas-cat/`. Links naar soorten gaan via `spHref()`; de taalknop op een soortpagina gaat naar de pagina in de andere taal. `window.SG_PAGE` in de pagina vertelt het script welke soort/taal.
- Telefoon (≤820 px): de balk met werelddelen en tabbladen verdwijnt bij omlaag scrollen en komt terug bij omhoog scrollen (16-10-2026).
- Start: werelddeelfilter; tabs **Kaart · Topspots · Soorten**. Fotorij "kies een kat": per werelddeel alleen katten van dat werelddeel (kleur = met spotplek, grijs = leeft er, nog geen plek); kies je een kat, dan blijft de kaart in het werelddeel met leefgebied erachter. Sterren = topspots.
- Startkaart (aangepast 16-10-2026): kleinere markers; de legenda is een filter op kans (standaard 3–5 aan, knop "Toon ook kans 1–2"); zoomen met +/−/hele kaart, knijpen, slepen als ingezoomd, ctrl+scroll en dubbelklik; daaronder een lijst "Plekken op de kaart / in beeld" (eerst 10, knop "Toon alle"; tik = plek kiezen). Bewegen herzien 17-10-2026: geen zijwaartse schuifbalk meer op de telefoon (wereldkaart = venster dat je met één vinger zijwaarts sleept, `BASEX`); ingezoomd sleep je vrij; updates per beeldje (`liveView`), na een gebaar geen herbouw maar `commitView`; uitloop na loslaten; afgebroken gebaar wordt netjes afgesloten. Verticaal vegen scrolt de pagina zolang je niet bent ingezoomd. Code: `homeData`, `drawHomeMap`, `bindGestures`, `drawMapList` in de template.
- Topspots: eerst 6, knop "Toon alle". Soorten: zoekveld.
- Topspotkaartjes met plekfoto (17-10-2026): `data/spotfoto.json` (id → src, cr, url, title), bron `img/spot-<id>.jpg` (max 1280 px), de bouw maakt `foto/spot-<id>.webp` (800 px). Plekfoto groot, rond soortfotootje (max. 3) linksonder, credit rechtsonder. Gevonden via Openverse (Flickr/Wikimedia, alleen CC BY, CC BY-SA, CC0). Deramakot en Steppe van Oost-Mongolië: geen vrije foto van de plek zelf, daarom een sfeerfoto (regenwoud Sabah, steppe Noord-Mongolië) met `note_nl`/`note_en` → 'Sfeerfoto (…)' vóór de credit (op verzoek gebruiker 17-10-2026).
- Soortpagina (overzichtelijker gemaakt 17-10-2026): alle foto's bovenaan als veegstrook met puntjes (`#hstrip`, `.hdots`; geen fotosectie onderaan meer), samenvatting (beste plek/tijd), snelmenu (blijft staan, licht op bij het onderdeel waar je bent: `bindJumpSpy`), eerst de kaart met genummerde plekken + keuzelijst "Ook te zien op deze plekken" (tik op nummer = plek opent), dan de plekken ingeklapt, alleen de top 3 zichtbaar + knop "Toon alle n plekken" (`showAllSpots`, ook bij tik op een kaartmarker) (rij: nummer, plek, land, kort seizoen via `shortSeason`, kans), uitgeklapt seizoen/tijdstip/tocht als regels met icoon (`factsHtml`/`FICO`, ook in het paneel van de startkaart), daaronder ingeklapte koppen (`.fold`, op verzoek 17-10-2026): Spottips (n), Status en bedreigingen (met IUCN-label in de kop), Bronnen (n); een knop in het snelmenu of een bronnummer klapt het onderdeel open. Kaart en Plekken blijven open.
- Menu (gelijkgetrokken met de Bezoekersgids 17-10-2026): Soorten · Topspots · Katten in Europa (op de telefoon met iconen) · Meer (Verantwoord spotten, Paklijst, Melden, Over deze gids, Bezoekersgids-link, Ko-fi). Taalknop = wereldbol (zelfde `bron/taalmenu.js` als de Bezoekersgids, door `build.py` achter `app.js` gezet); menuknop donker als hij open is; `body{margin:0}` zodat kop en menu de volle breedte hebben. Zoekknop in de kop (17-10-2026, zoals de Bezoekersgids): zoekt in katten (NL/EN/Latijn) en plekken (naam, gebied, land); kat → soortpagina, plek → startkaart met die plek gekozen (`goSpot`; vanaf een losse soortpagina via `sessionStorage` 'sg-spot'). In de Bezoekersgids staat 'Over deze gids' nu ook onder Meer (`bron/start.html`, `bron/huisstijl.py`).

## Open punten / mogelijke vervolgstappen
- Dierentuinfoto's (17-10-2026): `data/fotos.json` overschrijft per soort de fotolijst uit `bron/katalogue.json` (die blijft ongewijzigd). Weg: sneeuwpanter 1, nevelpanter 2–4, colocolo 1, vissende kat 2–4, platkopkat 2, Chinese bergkat 1, zwartvoetkat 1–2. Nieuw uit het wild (iNaturalist): `img/06-5.jpg` (nevelpanter, hoofdfoto), `img/33-5.jpg` (vissende kat). Borneose baaikat 1 en tilcayo 1 blijven met 'in gevangenschap' (`captive: true`), want er is geen goede foto uit het wild. Twijfelgevallen bewust laten staan: Sundaluipaardkat 2, savannetijgerkat 4, jaguarundi 2, wolkentijgerkat 1/2/4.
- Verbeterlijst uit de review van 16-10-2026: gedaan. Op 16-10: IUCN-status gecontroleerd (jaguarundi NT 2026, Aziatische goudkat VU, kodkod LC 2025 kloppen; goudkat: beoordeling 2023, gepubliceerd 2025 – tekst aangepast 17-10-2026), kansuitleg in legenda startkaart, 'Tijger kans 5' in kaartlijst, kans uit samenvattingsvak (2 vakken), bronnummers gesorteerd, Ko-fi in voettekst, icoon (`icon.svg`, `icon-180.png`) en deelvoorbeeld (og-tags; soortpagina's met eigen foto). Ook gedaan: reisverslagen als uitzondering toegestaan, soortkaart met landsgrenzen en -namen, tilcayo 'de nieuwste kattensoort ter wereld', kaarten op telefoon groter (wereld 960 px breed, overige kaarten vierkant).
- Gekoppeld met de dierentuingids (16-10-2026, met toestemming buiten `spottersgids/`): groen blok + voettekstlink in `bron/start.html` (NL → spottersgids/, andere talen → spottersgids/?lang=en), en `bron/bouw.py` neemt `spottersgids/sitemap.xml` op in de hoofd-sitemap. De spottersgids leest `?lang=nl|en`. Na een spottersgids-bouw met nieuwe pagina's moet de hoofdsite opnieuw gebouwd worden (`python3 bron/bouw.py`, ±9 min) om de hoofd-sitemap bij te werken.
- Kat met alleen plekken met kans 1–2 (bijv. caracal): bij het kiezen van die kat zet de startkaart kans 1–2 vanzelf aan (17-10-2026, gebruiker: ja). Ze blijven daarna aan tot je ze uitzet.
- OVERDRACHT.md/TWIJFELS.md openbaar: gebruiker vindt het niet erg (17-10-2026), laten staan.
- Testbranch `spottersgids-fotos-los` (proef losse foto's in het artifact) kan weg; verwijderen werd in de sessie geblokkeerd. Gebruiker kan hem zelf op GitHub verwijderen.
- Wolkentijgerkat: op 16-10-2026 bij Noord-Amerika weggehaald (`REMOVE_CONT` in `build.py`); staat alleen nog bij Midden- & Zuid-Amerika.
- Leeuw bij Ndutu toegevoegd (17-10-2026, gebruiker: toevoegen): plek 4 op de leeuwenpagina, kans 5, dec–mrt, bron TBY Tanzania 2013 (paartjes leeuwen + mannetje bij het Ndutumeer, ondanks droog jaar). Topspotkaartje Ndutu: Leeuw · Cheetah. Bouwwaarschuwing over Ndutu is daarmee weg.
- Testbranch: gebruiker verwijdert hem later zelf.
- Iriomote (Bengaalse kat, ~100 dieren, score 2): uitgelegd (verkeer is hoofdbedreiging, tekst zegt stapvoets rijden); gebruiker 17-10-2026: laten staan.
- Klein lay-outpuntje gezien (niet gevraagd): op brede schermen loopt "Kans 3 · redelijke kans" in het samenvattingsvak van de soortpagina iets buiten het vak.

## Safari-stijl (live sinds 19-10-2026)
- Gebruiker wilde de Spottersgids "meer als de Bezoekersgids": zelfde opbouw, maar bruin (Safari). Goedgekeurd en live op de hele gids: onderbalk **Kaart · Soorten · Topspots · Meer** (vervangt de tabbladen en de schuivende werelddeelbalk), donkere kop per scherm (166 px, golfrand, acacia met zon, sporen), titel in Anton met wereldbol-embleem (lange titels worden kleiner: `fitSk`), onderregel en goudgele regel met aantallen; "Kies een werelddeel" (op Kaart, Soorten en Topspots, één gedeelde keuze) en "Kies een kat" met pootjes; Soorten als fotoraster in twee inklapbare groepen (Pantherinae nrs. 1–7 / Felinae, op naam); Topspots met dezelfde kaartjes; Meer als lijst met ronde iconen (zelfde onderdelen als het menu ☰); soort- en tekstpagina's met dezelfde kop en een zwevende terugknop (`.fab`); voet met de luipaard op de tak (CSS/JS uit `../bron/jungle.py`, door `build.py` toegevoegd). Info, kansen, kaartfuncties, losse soortadressen en NL/EN bleven gelijk.
- Kleuren en plaatjes: `:root` in `bron/template.html` (zand `--bg`, koffiebruin `--dark`, okergeel `--sun`); acacia, gras, sporen, golf en pootjes maakt `build.py` en zet ze als `--i-…`-variabelen. "Bijgewerkt …" = datum van de laatste commit in `data/` of `bron/katalogue.json` (`__UPDATED__`).
- Proefversies: kopieer de template naar `bron/template-test.html` en bouw met `python3 bron/build.py --test` → alleen `test/` (noindex, soortpagina's via `#soort-<nr>` binnen de testpagina). De testmap na gebruik weer weghalen.
