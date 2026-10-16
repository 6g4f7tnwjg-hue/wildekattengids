# Overdracht – Spottersgids voor wilde katten (Wild Cat Spotter's Guide)

Maker: J. Gelens. Stand: 16 oktober 2026. Alle 42 soorten hebben een soortpagina.

## Waar staat alles
- **Live: GitHub Pages** https://yeetkitty.github.io/wildekattengids/spottersgids/ – openbaar sinds 16-10-2026 (PR #1 samengevoegd). Pages publiceert de branch `main` (map `spottersgids/`). Wijzigingen: werken op `spottersgids-europa` (vers vanaf `main`), daarna via een nieuwe pull request naar `main` (alleen als de gebruiker erom vraagt).
- **Oud: artifact (privé)** https://claude.ai/artifact/4Pmep6UwbY4aoyRyXXfRRX – staat nog op de versie met ingebakken foto's (12,7 MB). Losse foto's laden niet in de Claude-app (getest 16-10-2026). Gebruiker akkoord met een korte 'verhuisd naar …'-pagina; publiceren werd in de sessie geblokkeerd, wacht op bevestiging. De huidige `index.html` werkt NIET meer in het artifact.
- **Repo:** `yeetkitty/wildekattengids`, branch **`spottersgids-europa`**, map `spottersgids/` (losse site naast de bestaande dierentuingids; niets daarbuiten aangeraakt).
- **Bron van de soortgegevens:** artifact "De KATalogue" https://claude.ai/code/artifact/ba3edb6b-d786-4e68-906b-779c6b5cb3ea (42 soorten, foto's + credits, verspreidingskaarten, IUCN). Al uitgepakt naar `bron/katalogue.json`, `bron/land.txt` en `img/NN-i.jpg`.

## Opbouw van `spottersgids/`
| Pad | Wat |
|---|---|
| `bron/template.html` | De hele site (HTML/CSS/JS, één pagina met #-routes). `__DATA__` wordt bij het bouwen vervangen. Ko-fi-link: `KOFI_URL` (= https://ko-fi.com/katalogue). |
| `bron/build.py` | Bouwt `index.html`. `PAGES` = lijst met soortnummers die een pagina hebben (nu alle 42). Foto's zijn losse bestanden: groot = `img/NN-i.jpg` (origineel), klein = `foto/NN-i-k.webp` (200 px, door de bouw gemaakt) voor fotorij, lijstjes en Katten in Europa. |
| `data/<nr>.json` | Onderzoek per soort: intro, plekken (score 1–5, seizoen, tijdstip, tocht, bronnen), tips, bedreigingen, status, bronnen – NL en EN. |
| `data/topspots.json` | Oorspronkelijke topspotlijst; telt nu alleen nog als "deze plek mag topspot zijn bij score 4". |
| `data/alias.json` | Samenvoegen van dezelfde plek onder verschillende id's. |
| `data/extra_cont.json` | Extra werelddelen bovenop de KATalogue (luipaard, Afr. wilde kat, moeraskat → ook Europa). |
| `data/text.json`, `data/europe.json` | Pagina's Verantwoord spotten, Katten in Europa, Paklijst, Over mij (NL/EN). |
| `TWIJFELS.md` | Alle twijfels en redactiekeuzes per soort en per ronde. |
| `index.html` | Gebouwde site (≈0,9 MB; met foto's ≈1,2 MB per bezoek). |
| `img/`, `foto/` | Foto's (groot jpg, klein webp); moeten mee naar `main`. |

Bouwen: `cd spottersgids && python3 bron/build.py` → daarna committen/pushen (en via `main` live zetten). Lokaal testen: `python3 -m http.server` in de repo-root en `http://localhost:8000/spottersgids/` openen.
Topspot-regel in de bouw: plek met score 5 op een soortpagina = topspot; score 4 alleen als hij in `topspots.json` voor die soort staat.

## Afspraken met de gebruiker (belangrijk)
- Werkwijze per ronde; na elke ronde publiceren en **stoppen**. Bij latere wijzigingen **alleen aanpassen wat gevraagd wordt**. Bij onduidelijke wensen **doorvragen** (gebruiker vraagt daar expliciet om).
- Taal: Nederlands naar de gebruiker; site NL/EN. Gidsnamen uit de KATalogue (bijv. sneeuwpanter, Sundaluipaardkat, het luipaard). Let op het Duitse "stuft/stufte" in statusteksten → "deelt in"/"zette".
- Schrijfstijl: avontuurlijk, eerlijk, "je"; intro eindigt met "Kans: X – …".
- Kansscore eerlijk (5 bijna zeker … 1 alleen geluk/cameravallen).
- **Geen namen van reisorganisaties/lodges** in tekst of brontitels; geen hun sites als bron. Excursies wél concreet beschrijven ("excursies moeten er juist in").
- Plekken alleen op gebiedsniveau, markers op het midden van het gebied; geen holen/wissels/rustplekken.
- **Niet lokken:** voederplekken niet als aanbevolen plek (bij wolkentijgerkat twee geschrapt).
- Ontwerp: één lichte stijl (donker vond de gebruiker te donker). Kaart opent als eerste tabblad.

## Wat er gebouwd is (functies)
- Start: werelddeelfilter; tabs **Kaart · Topspots · Soorten**. Kaart met fotorij "kies een kat": per werelddeel alleen katten van dat werelddeel (kleur = met spotplek, grijs = leeft er, nog geen plek); kies je een kat, dan blijft de kaart in het werelddeel met leefgebied erachter. Sterren = topspots. Startkaart (16-10-2026): markers kleiner; legenda is een filter op kans (standaard 3–5 aan, knop "Toon ook kans 1–2"); zoomen met +/−/hele kaart, knijpen, slepen als ingezoomd, ctrl+scroll en dubbelklik; daaronder een lijst "Plekken op de kaart / in beeld" (eerst 10, knop "Toon alle"). Soortpagina-kaarten ongewijzigd. Topspots: eerst 6, knop "Toon alle". Soorten: zoekveld.
- Soortpagina: samenvatting (beste plek/tijd/kans), snelmenu, inklapbare plekken (top 3 open), kaart met genummerde plekken + keuzelijst "Ook te zien op deze plekken", tips, status/bedreigingen, foto's met credits, bronnen.
- Menu: Soorten · Topspots · Katten in Europa · Meer (Verantwoord spotten, Paklijst, Over mij).

## Open punten / mogelijke vervolgstappen
- Wolkentijgerkat staat grijs in de fotorij bij Noord-Amerika (KATalogue rekent Costa Rica/Panama tot Noord-Amerika, de gids tot Midden-/Zuid-Amerika) – gebruiker nog niet gevraagd of dit gelijkgetrokken moet worden.
- Openbaar maken is goedgekeurd; een link vanaf de bestaande site en opname in `sitemap.xml` komen later.
- Testbranch `spottersgids-fotos-los` (proef losse foto's in het artifact) kan weg; verwijderen werd in de sessie geblokkeerd.
- Kaart van Azië is op mobiel vol (niet aangepast; niet gevraagd).
- Leeuw bij Ndutu staat niet meer op de kaart (leeuwenpagina neemt Ndutu niet op); Ndutu is topspot voor de cheetah.
- Iriomote (Bengaalse kat, ~100 dieren) staat erin met score 2 – gebruiker kan vragen om te schrappen.
- Artifact is privé; delen gaat via het deelmenu van de pagina.
- Er is (nog) geen pull request gemaakt; alleen gepusht naar de branch.
