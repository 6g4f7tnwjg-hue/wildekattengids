# Onderzoek: wilde katachtigen in Roemeense dierenlocaties (stand oktober 2026)

Doel: voor een gids "Wilde katachtigen in Roemeense dierenlocaties" vastleggen welke wilde kattensoorten
(Felidae, NIET de huiskat, NIET huiskat-hybriden zoals Bengaal/Savannah) in welke Roemeense dierentuinen,
dierenparken, wildparken, safariparken, attractieparken met dieren en opvangcentra te zien zijn.
Alleen Roemenië (România). Vandaag is 30-10-2026. Roemeense dierentuinvereniging: Asociația Grădinilor Zoologice și Acvariilor din România (AGZAR). Dierentuinen hebben een vergunning (autorizație de funcționare) van het ministerie van Milieu; controleer of er een openbare lijst is.

## Lees eerst
- /root/.claude/skills/synced/361f9230-f0b2-4aeb-85a3-73b8ac64d42c_164ba32d-3c32-4381-b207-96ef713cb5fc/wilde-katachtigen-gids/references/valkuilen.md
- /root/.claude/skills/synced/361f9230-f0b2-4aeb-85a3-73b8ac64d42c_164ba32d-3c32-4381-b207-96ef713cb5fc/wilde-katachtigen-gids/references/taxonomie.md

## Bronnenvolgorde
1. Eigen website van het park (animale/animalele noastre/specii/hartă (ook Engelse versie van de site); Facebook-pagina van de stad/het park). Laadt een dierenlijst pas in de browser,
   render dan met Playwright (Python, `pip install playwright==1.56.0` indien nodig; Chromium staat in /opt/pw-browsers,
   NIET `playwright install` draaien). Probeer ook sitemap.xml en /wp-json/wp/v2/pages?search=...
2. Recent Roemeens nieuws (Digi24, Adevărul, Libertatea, HotNews, Agerpres, Ziarul Financiar, regionale media zoals Monitorul de Brașov, Tribuna, Ziarul de Iași, Gazeta de Sud, Știri de Cluj), met datum. Zoek in het Roemeens:
   leu/lei, leoaică, tigru (siberian/de Amur, sumatran, bengal, alb), leopard (de Amur, persan, negru = zwarte panter), jaguar, leopard al zăpezilor / irbis (= sneeuwluipaard),
   leopard încețoșat (= nevelpanter), ghepard, pumă, râs / râs eurasiatic (= Euraziatische lynx), râs roșu (= rode lynx), serval, caracal, ocelot, pisică sălbatică (= Europese wilde kat),
   pisica lui Pallas / manul, pisică de junglă (= moeraskat), pisică pescar (= vissende kat), pisică leopard (= Bengaalse kat; let op: kan ook het huiskatras zijn — controleer),
   pisică de nisip (= zandkat), "pui", "s-au născut", "naștere".
3. Zootierliste (zootierliste.de) en ZooChat: alleen aanvullend, nooit als enige bron voor "aanwezig".
4. Sociale media (posts van het park zelf) als laatste redmiddel.
Noteer bij elke vermelding de bron én de datum (ongedateerd = "ongedateerd").

## Regels
- Statuscodes: g = aanwezig (recente bron 2025–2026), y = tijdelijk niet zichtbaar, b = vertrek aangekondigd,
  p = gepland (alleen officiële aankondiging met diersoort), w = onzeker (concrete aanwijzing van na 2024 maar
  niet bevestigd; altijd met uitleg), r = alleen met rondleiding, n = niet open voor publiek.
  Laatste aanwijzing van vóór 2024 of aantoonbaar weg → bij "earlier" (Eerder hier), niet als vermelding.
- Aantallen: "onbekend" tenzij bevestigd. Namen van dieren als bekend.
- Soortnamen: gebruik EXACT deze Nederlandse sleutels: Leeuw, Tijger, Luipaard, Jaguar, Sneeuwluipaard, Nevelpanter,
  Cheetah, Poema, Jaguarundi, Euraziatische lynx, Canadese lynx, Iberische lynx, Rode lynx, Serval, Caracal,
  Aziatische goudkat, Marmerkat, Ocelot, Margay, Geoffroy’s kat, Bengaalse kat (= luipaardkat/amurkat,
  Prionailurus bengalensis), Vissende kat, Roestkat, Manoel (Pallas’ kat), Europese wilde kat, Afrikaanse wilde kat,
  Zandkat, Zwartvoetkat, Moeraskat (overige: zie taxonomie.md).
- Ondersoortlabels volgens taxonomie.md, bijv. "Amoer", "Bengaals", "Sumatraans", "Noordelijk (P. l. leo)",
  "Aziatisch (P. l. leo, voorheen P. l. persica)", "Zuidelijk (P. l. melanochaita)", "Amoer (P. p. orientalis)",
  "Noordelijk (L. l. lynx)", "Zuidelijk (A. j. jubatus)", anders "onbekend" of "—" als de soort geen ondersoort heeft.
- Vul een ondersoort ALLEEN in als een bron (eigen site, nieuws, Zootierliste/stamboek) hem noemt; anders "onbekend". Niet afleiden uit het land (een Roemeense lynx is niet automatisch "Karpatisch").
- Geen persoonlijke gegevens meesturen in verzoeken (ook niet in een User-Agent).
- Recente geboortes: kleine katten jonger dan 1 jaar, grote katten (Pantherinae) jonger dan 2 jaar (dus geboren na 22-10-2024).
- Vrij levende wilde katten tellen niet mee (wel noemen in "about"). Huiskatten in het park: noemen in "about" als opvallend.
- Ook locaties ZONDER katten vastleggen (in "zonder_katten") met korte reden — zo kunnen we ze op de pagina noemen.
- Schrijf alle teksten in het Nederlands (nl) en Engels (en). Plaatsnamen met Roemeense letters (Brașov, Târgu Mureș, Pitești, Iași; ș en ț met komma). Kort, feitelijk, gewone taal. Geen andere diersoorten,
  geen Rode Lijst-status, geen algemene bezoektips.
- Gebruik bij hulpscripts ALLEEN je eigen map (zie je opdracht); raak geen andere bestanden aan, ook niet de repo.
- Je hebt een beperkt aantal zoekopdrachten: werk de belangrijkste parken eerst grondig af.

## Uitvoer: één JSON-bestand (pad staat in je opdracht)
```json
{
  "locaties": [
    {
      "naam": "Officiële naam van het park",
      "plaats": "Plaats (gemeente)",
      "judet": "Roemeense naam van het județ of București, bijv. Brașov",
      "lon": 19.08, "lat": 47.52,
      "type": "Dierentuin | Dierenpark | Wildpark | Safaripark | Attractiepark met dieren | Sanctuary | Opvangcentrum | Kinderboerderij | Anders",
      "lidmaatschap": ["EAZA", "AGZAR", ...],
      "url": "https://...",
      "uren": {"nl": "Openingstijden kort, met (eigen site, gezien DD-MM-2026)", "en": "..."},
      "about": {"nl": "1–3 zinnen", "en": "..."},
      "earlier": {"nl": "Katten die er eerder waren, met jaartal en bron", "en": "..."},
      "katten": [
        {"soort": "Tijger", "ondersoort": "Amoer", "status": "g",
         "toelichting": {"nl": "...", "en": "..."},
         "aantal": {"nl": "2 (kater X en poes Y)", "en": "2 (male X and female Y)"},
         "bron": "Eigen site soortpagina (gezien 22-10-2026); Digi24 12-05-2026",
         "twijfel": {"nl": "alleen bij w: waarom onzeker", "en": "..."}}
      ],
      "geboortes": [
        {"soort": "Tijger", "geboren": "2026-05-03", "n": {"nl": "3 welpen", "en": "3 cubs"},
         "x": {"nl": "namen/geslacht/moeder/vader, sinds wanneer te zien", "en": "..."}, "bron": "... DD-MM-2026"}
      ],
      "kleur": "witte tijger / zwarte panter / ... of leeg"
    }
  ],
  "zonder_katten": [
    {"naam": "...", "plaats": "...", "reden": {"nl": "bijv. geen katachtigen op de dierenlijst (eigen site 22-10-2026)", "en": "..."}}
  ],
  "open_punten": ["vrije tekst: wat je niet kon bevestigen, tegenstrijdigheden"]
}
```
Coördinaten: van OpenStreetMap/Nominatim of de eigen site, 3 decimalen.
Lever aan het eind een korte samenvatting (max 15 regels): welke locaties met katten, welke twijfelgevallen.

## Afbakening Roemenië (zoals bij Tsjechië, Polen en Hongarije)
Particuliere houders (minizoo, parc privat, colecție privată) en circussen met wilde katten worden OPGENOMEN, met kanttekening. Type "Particuliere houder"; status volgens toegang (g als vrij te bezoeken, r als alleen met rondleiding/afspraak, n als niet open voor publiek). Geen namen van particuliere personen (wel namen van bedrijven/stichtingen). Locaties die alleen uit een politie- of inbeslagnamebericht bekend zijn, zonder plaats of toegang, niet opnemen (wel bij open_punten). Circussen zonder vaste plek: "plaats": "–", geen coördinaten (lon/lat null). Ga na of wilde dieren in Roemeense circussen verboden zijn (en sinds wanneer).
Veel Roemeense steden hebben een kleine gemeentelijke dierentuin (grădina zoologică, ook "minizoo" of "colț zoo" in een park); neem ze allemaal mee, ook als ze klein zijn.
