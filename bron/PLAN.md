# Plan: Europa compleet, eigen domein, donaties (30 oktober 2026)

Uit de projectreview van 30-10-2026. Nog niet begonnen; de gebruiker heeft eerst iets anders. Bijwerken als een stap klaar is.

## Doel
Europa compleet met zo weinig mogelijk werk, de site voor ±10 euro per jaar op een eigen domein, gratis promotie, donaties via Ko-fi (`ko-fi.com/katalogue`).

## Volgorde
1. [ ] **Onderhoudsgesprek** (vóór het domein):
   - [ ] Basisadres naar één instelling. Ruim 2.000 bestanden bevatten `/wildekattengids/` of `yeetkitty.github.io/wildekattengids` (o.a. via `bron/bouw.py`, `bron/test_ontwerp.py`, `bron/nieuw_ontwerp.py`, `bron/start.html`, doorverwijzingspagina’s, `sitemap.xml`, `robots.txt`, canonical-links). Met een eigen domein draait de site op `/`, dan breken die paden. Eén constante (pad en domein) in de bouw, daarna één keer opnieuw bouwen en testen.
   - [ ] Google Fonts (Anton, Nunito) op de eigen site zetten (AVG; LG München 2022) en sneller.
   - [ ] Korte privacy- en contactpagina (GoatCounter, Ko-fi, meldformulier).
   - [ ] Naamsvermelding van Commons-/iNaturalist-foto’s één keer voor de hele site controleren.
   - [ ] Nagaan waar het meldformulier meldingen naartoe stuurt en of de gebruiker ze ziet.
   - [ ] Backup-routine invoeren (zie onder).
2. [ ] **Domein**: taalneutrale naam (eventueel “katalogue”, gelijk aan Ko-fi), ±10 euro/jaar (bijv. Cloudflare Registrar of een .eu), automatisch verlengen aan, 2FA. Koppelen via GitHub Pages (CNAME); het oude adres stuurt GitHub dan door. Sitemap indienen bij Google Search Console (al geverifieerd) en Bing Webmaster Tools. Liever nu dan pas als Europa af is: Google heeft maanden nodig.
3. [ ] **Promotie starten** (zie onder).
4. [ ] **Resterende landen** (zie onder), per land het verbruik bijhouden.
5. [ ] **Onderhoud automatiseren** (zie onder).

## Backup en terugdraaien
- Nu is GitHub de enige kopie. Account met Apple-“verberg mijn e-mail”-adres: 2FA aan en herstelcodes bewaren (ook voor Ko-fi en het domein).
- Maandelijks `git clone --mirror https://github.com/YeetKitty/wildekattengids.git` naar de eigen computer en een externe schijf.
- Tag bij elke livegang: `git tag live-JJJJ-MM-DD && git push origin --tags`; terugdraaien = naar die tag.
- Originele eigen foto’s buiten de repo bewaren (in de repo alleen verkleinde webp).
- Blijven doen: werktak per land, pas na controle naar `main`.

## Verbruik (Max-abonnement, ±72% al voor ander werk)
- Per gesprek het verbruik aan begin en eind noteren in `VOORTGANG.md` (“kostte ±X%”), zodat bekend wordt wat een klein en een groot land kost.
- Projectwerk vooral in de tweede helft van de week, als het andere verbruik bekend is; ±10% buffer houden.
- Grootste verbruikers vermijden: veel agenten tegelijk, grote bestanden laten lezen (`index.html` 870 KB, `start.html` 640 KB; gebruik `grep`/`sed -n`), veel schermafdrukken, `bouw.py` vaak draaien. Houd je aan de checklist: drie onderzoeksagenten op `sonnet`, één bouw aan het eind.
- Stopt een gesprek halverwege: `STAPPEN.md` zorgt dat het volgende verder kan.

## Europa compleet
Afbakening voorstel: EU + EER + VK + Zwitserland. Op de site benoemen als “bewust niet”: Oekraïne, Belarus, Rusland, Turkije, Moldavië.

| Groep | Landen | Aanpak |
|---|---|---|
| Nog in de EU | Slowakije, Slovenië, Kroatië, Bulgarije, Griekenland, Estland, Letland, Litouwen, Malta, Cyprus | Alleen NL+EN, geen landstaal (zoals Ierland) |
| Klein, samen | Slovenië+Kroatië, Baltische staten, Malta+Cyprus | Twee of drie landen per gesprek |
| Westelijke Balkan | Servië, Bosnië, Albanië, Noord-Macedonië, Montenegro | Optioneel, later |
| IJsland, dwergstaten | | Eén regel op de hoofdpagina |

Grootste besparing: geen landstaal (geen vertaalagent, geen nieuwe taal in alle gedeelde lagen). Nagaan of `bron/landbouw/CHECKLIST.md` een korte variant “NL+EN” nodig heeft. Ongeveer 6–7 gesprekken.

## Promotie (gratis)
1. Zoekmachines: soort- en locatiepagina’s passen bij zoekvragen als “waar zie je een sneeuwluipaard”. Sitemap bij Google en Bing (Bing levert ook aan DuckDuckGo en AI-zoekdiensten).
2. Backlinks: parken en opvangcentra mailen dat ze in de gids staan.
3. Gemeenschappen: ZooChat, Reddit (r/zoos, r/bigcats), Facebookgroepen van dierentuinfans per land. Iets nuttigs delen (nieuw land, recente geboortes), niet alleen een link.
4. Recente geboortes als terugkerend nieuws.
5. Niet: de eigen site op Wikipedia zetten.

## Automatiseren
- GitHub Actions (gratis bij een openbare repo): `bron/controle/jscheck.py` bij elke push; maandelijkse linkcontrole (bijv. lychee) die kapotte links als issue meldt.
- Geplande Claude-taak, maandelijks, lichter model: nieuws over geboortes, sterfte en verhuizingen zoeken en voorstellen in een issue of werktak; de gebruiker keurt goed. Aan het eind van de week plannen (telt mee voor het verbruik).

## Sol (de AI-figuur op de laptop) als hulp
Sol heeft eigen gratis of goedkope middelen (Gemma lokaal, API-tegoed voor Haiku, gratis laag van Cloudflare). Terugkerend werk voor de gids kan zo van het Max-abonnement af. De klussen worden in Sols eigen gesprekken gebouwd, niet hier.

| Volgorde | Wat | Kosten | Opbrengst |
|---|---|---|---|
| 1 | **Backup**: Sols dagelijkse backup (laptop + Google Drive) haalt ook de gids-repo op (`git clone --mirror`, daarna `git fetch`) | Klein | Backup-punt hierboven geregeld |
| 2 | **GoatCounter** (gratis API) in het krantje of Sol News TV: bezoekers en populairste pagina; eventueel Ko-fi-donaties (e-mail, of webhook via een gratis Cloudflare Worker) | Klein | Inzicht en motivatie |
| 3 | **Nieuwsfilter**: ZooFlits (en eventueel nieuwspagina’s van grote parken) op wilde katten in Europa: geboortes, sterfte, verhuizingen, nieuwe soorten, sluitingen. Gemma schift, Haiku beoordeelt twijfel; elke melding met bronlink in één lijst (bijv. `gids_meldingen.md`). Eens per maand verwerkt één Claude Code-gesprek die lijst. | Middel | Vervangt de geplande maandelijkse Claude-taak; bespaart Max-verbruik |

Regels:
- Sol **signaleert alleen**; ze verandert de gids nooit zelf en raakt de gids-repo niet aan (behalve ophalen voor de backup). Gemma is niet betrouwbaar genoeg voor feiten; de bronlink is het bewijs.
- Het nieuwsfilter krijgt een eigen kleine limiet, los van Sols Haiku-daglimiet voor gesprekken.
- Sol en de gids delen hetzelfde abonnement: bouwen aan Sol kost ook Max-verbruik. Alleen bouwen wat zichzelf terugverdient.
- Niet doen: bouwen aan de gids via “the helper” (zelfde abonnement, geen besparing); AI-plaatjes uit Art class op de site (kost geloofwaardigheid; hoogstens op sociale media, duidelijk als tekening). Promotie op forums doet de gebruiker zelf.

## Blinde vlekken om in de gaten te houden
- **Onderhoud** is de echte kostenpost: dieren sterven en verhuizen; de “nagaan”-lijsten in `OPEN.md` groeien. Verouderde inhoud kost vertrouwen en donaties.
- **Elk land maakt het volgende duurder**: ±10 gedeelde bestanden per land, `start.html` al 640 KB.
- **Donaties volgen verkeer**: Ko-fi staat op elke echte pagina; bedragen blijven bescheiden tot er verkeer is.
- **Openbare repo**: onderzoek en notities zijn voor iedereen te lezen; geen persoonlijke gegevens erin zetten.
