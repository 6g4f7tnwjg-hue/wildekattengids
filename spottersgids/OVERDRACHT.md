# Overdracht – Spottersgids voor wilde katten (Wild Cat Spotter's Guide)

Maker: J. Gelens. Stand: 16 oktober 2026. Alle 42 soorten hebben een soortpagina.

## Waar staat alles
- **Live (artifact, privé):** https://claude.ai/artifact/4Pmep6UwbY4aoyRyXXfRRX – altijd bijwerken op deze URL (publiceer `spottersgids/index.html`; vanuit een nieuwe chat eerst `read` met deze URL, dan publiceren met `url`).
- **Repo:** `yeetkitty/wildekattengids`, branch **`spottersgids-europa`**, map `spottersgids/` (losse site naast de bestaande dierentuingids; niets daarbuiten aangeraakt).
- **Bron van de soortgegevens:** artifact "De KATalogue" https://claude.ai/code/artifact/ba3edb6b-d786-4e68-906b-779c6b5cb3ea (42 soorten, foto's + credits, verspreidingskaarten, IUCN). Al uitgepakt naar `bron/katalogue.json`, `bron/land.txt` en `img/NN-i.jpg`.

## Opbouw van `spottersgids/`
| Pad | Wat |
|---|---|
| `bron/template.html` | De hele site (HTML/CSS/JS, één pagina met #-routes). `__DATA__` wordt bij het bouwen vervangen. Ko-fi-link: `KOFI_URL` (= https://ko-fi.com/katalogue). |
| `bron/build.py` | Bouwt `index.html`. `PAGES` = lijst met soortnummers die een pagina hebben (nu alle 42). Foto's worden als data-URI ingebakken (losse bestanden laden niet in de Claude-app). |
| `data/<nr>.json` | Onderzoek per soort: intro, plekken (score 1–5, seizoen, tijdstip, tocht, bronnen), tips, bedreigingen, status, bronnen – NL en EN. |
| `data/topspots.json` | Oorspronkelijke topspotlijst; telt nu alleen nog als "deze plek mag topspot zijn bij score 4". |
| `data/alias.json` | Samenvoegen van dezelfde plek onder verschillende id's. |
| `data/extra_cont.json` | Extra werelddelen bovenop de KATalogue (luipaard, Afr. wilde kat, moeraskat → ook Europa). |
| `data/text.json`, `data/europe.json` | Pagina's Verantwoord spotten, Katten in Europa, Paklijst, Over mij (NL/EN). |
| `TWIJFELS.md` | Alle twijfels en redactiekeuzes per soort en per ronde. |
| `index.html` | Gebouwde site (≈12,7 MB, grens artifact 16 MB). |

Bouwen: `cd spottersgids && python3 bron/build.py` → daarna publiceren en committen/pushen.
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
- Start: werelddeelfilter; tabs **Kaart · Topspots · Soorten**. Kaart met fotorij "kies een kat": per werelddeel alleen katten van dat werelddeel (kleur = met spotplek, grijs = leeft er, nog geen plek); kies je een kat, dan blijft de kaart in het werelddeel met leefgebied erachter. Sterren = topspots. Topspots: eerst 6, knop "Toon alle". Soorten: zoekveld.
- Soortpagina: samenvatting (beste plek/tijd/kans), snelmenu, inklapbare plekken (top 3 open), kaart met genummerde plekken + keuzelijst "Ook te zien op deze plekken", tips, status/bedreigingen, foto's met credits, bronnen.
- Menu: Soorten · Topspots · Katten in Europa · Meer (Verantwoord spotten, Paklijst, Over mij).

## Open punten / mogelijke vervolgstappen
- Wolkentijgerkat staat grijs in de fotorij bij Noord-Amerika (KATalogue rekent Costa Rica/Panama tot Noord-Amerika, de gids tot Midden-/Zuid-Amerika) – gebruiker nog niet gevraagd of dit gelijkgetrokken moet worden.
- Paginagrootte ≈12,7 MB: eventueel foto's verkleinen als de site op de telefoon traag laadt.
- Kaart van Azië is op mobiel vol (niet aangepast; niet gevraagd).
- Leeuw bij Ndutu staat niet meer op de kaart (leeuwenpagina neemt Ndutu niet op); Ndutu is topspot voor de cheetah.
- Iriomote (Bengaalse kat, ~100 dieren) staat erin met score 2 – gebruiker kan vragen om te schrappen.
- Artifact is privé; delen gaat via het deelmenu van de pagina.
- Er is (nog) geen pull request gemaakt; alleen gepusht naar de branch.
