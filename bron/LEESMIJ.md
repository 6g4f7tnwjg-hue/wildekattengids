# Bron van de Wilde katachtigen-gids

Alles wordt uit deze map gebouwd. Pas nooit de gegenereerde bestanden in de hoofdmap aan
(`index.html`, `soort/`, `top10/`, `nederland/`, `belgie/`, `luxemburg/`, `duitsland/`, `frankrijk/`, `sitemap.xml`): die worden bij elke bouw overschreven.

## Wat staat waar

| Bestand | Inhoud |
|---|---|
| `gidsen/nl.html`, `be.html`, `lu.html`, `de.html`, `fr.html` | De landengidsen. Alle gegevens (soorten, waarnemingen `R`, locaties `LOCS`, jongen `YOUNG`) staan in het script van de gids; de Duitse gids heeft één blok per deelstaat, de Franse één blok per regio (13 regio’s van Europees Frankrijk; Corsica heeft geen katten). Talen: Nederlands en Engels; België, Luxemburg en Frankrijk ook Frans, Duitsland ook Duits (`T(nl,en,de)` en `l-de`-elementen). Foto's staan erin als `@@IMGn@@`. |
| `start.html` | De startpagina. De gegevens in `const D` (kaartstippen, aantallen, recente geboortes) worden bij elke bouw opnieuw berekend uit de gidsen. Kaartvormen en de deelstaat-notitie blijven staan. Talen: Nederlands, Engels, Frans en Duits (`T(nl,en,fr,de)` en `l-fr`/`l-de`-elementen). |
| `../img/` | Alle foto's; `n.webp` hoort bij `@@IMGn@@`. Nieuwe foto: volgend nummer toevoegen. |
| `artifact_kop.html`, `web_kop.html` | Vaste kopjes voor de Claude-pagina en de website. |
| `top10.json` | De top 10 om te bezoeken (blok op de startpagina en pagina `/top10/`, op de Claude-pagina `#top10`). `vast` staat in die volgorde bovenaan, met de uitleg in vier talen; is de lijst korter dan 10 of verdwijnt een park uit de gids, dan vult de bouw aan op score. Volgorde of uitleg veranderen: alleen dit bestand aanpassen. |
| `franse_namen.json`, `duitse_namen.json` | Franse en Duitse soortnamen voor de startgegevens. |
| `locatietypes.json` | De vaste lijst van locatietypes en labels. Elke locatie heeft in `LOCINFO` één `type` (de namen uit deze lijst) en `labels` (sleutels uit deze lijst). Dierentuin = lid van EAZA, NVD of VdZ; anders dierenpark. |
| `locatietypes.js` | Filterknoppen, labels en types in de gidsen; de bouw zet dit achter het script van elke gids en deelstaat. |
| `bouw.py`, `startdata.py`, `extract.js` | De bouw. Deelstaten en regio’s staan in `STATES` en `REGIOS` in `bouw.py` (samen `DEEL`). |

## Bijwerken

1. Pas de gids aan in `bron/gidsen/…`.
2. Bouw: `python3 bron/bouw.py` (vereist node en Python met playwright; duurt een paar minuten door de losse pagina's).
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
