# Onderzoek: wilde katachtigen in Noorse dierenlocaties (stand oktober 2026)

Doel: voor een gids "Wilde katachtigen in Noorse dierenlocaties" vastleggen welke wilde kattensoorten
(Felidae, NIET de huiskat, NIET huiskat-hybriden zoals Bengaal/Savannah) in welke Noorse dierentuinen,
dierenparken, wildparken, safariparken, attractieparken met dieren en opvangcentra te zien zijn.
Alleen Noorwegen (Norge), inclusief Svalbard. Vandaag is 22-10-2026. SDF = Svenska Djurparksföreningen (heeft ook Noorse leden, o.a. Bjørneparken).

## Lees eerst
- /root/.claude/skills/synced/361f9230-f0b2-4aeb-85a3-73b8ac64d42c_164ba32d-3c32-4381-b207-96ef713cb5fc/wilde-katachtigen-gids/references/valkuilen.md
- /root/.claude/skills/synced/361f9230-f0b2-4aeb-85a3-73b8ac64d42c_164ba32d-3c32-4381-b207-96ef713cb5fc/wilde-katachtigen-gids/references/taxonomie.md

## Bronnenvolgorde
1. Eigen website van het park (dyrene/våre dyr/dyreliste/kart/parkkart). Laadt een dierenlijst pas in de browser,
   render dan met Playwright (Python, `pip install playwright==1.56.0` indien nodig; Chromium staat in /opt/pw-browsers,
   NIET `playwright install` draaien). Probeer ook sitemap.xml en /wp-json/wp/v2/pages?search=...
2. Recent Noors nieuws (NRK, TV 2, VG, Dagbladet, Aftenposten, NTB, regionale kranten zoals Fædrelandsvennen), met datum. Zoek in het Noors:
   løve, tiger, leopard, jaguar, snøleopard, skyleopard (= nevelpanter), gepard, puma, gaupe (= Euraziatische lynx),
   rødgaupe (= rode lynx), serval, karakal, ozelot, leopardkatt (= Bengaalse kat), fiskekatt (= vissende kat), manul/pallaskatt,
   villkatt (= Europese wilde kat), sandkatt (= zandkat), unger/kattunger "ble født", "har fått unger". Let op: "bengalkatt" is vaak het huiskatras Bengaal — controleer.
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
- Recente geboortes: kleine katten jonger dan 1 jaar, grote katten (Pantherinae) jonger dan 2 jaar (dus geboren na 22-10-2024).
- Vrij levende wilde katten tellen niet mee (wel noemen in "about"). Huiskatten in het park: noemen in "about" als opvallend.
- Ook locaties ZONDER katten vastleggen (in "zonder_katten") met korte reden — zo kunnen we ze op de pagina noemen.
- Schrijf alle teksten in het Nederlands (nl) en Engels (en). Plaatsnamen met Noorse letters (Flå, Kristiansand, Tromsø). Kort, feitelijk, gewone taal. Geen andere diersoorten,
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
      "fylke": "Noorse naam van het fylke (indeling 2024), bijv. Agder",
      "lon": 8.15, "lat": 58.18,
      "type": "Dierentuin | Dierenpark | Wildpark | Safaripark | Attractiepark met dieren | Sanctuary | Opvangcentrum | Kinderboerderij | Anders",
      "lidmaatschap": ["EAZA", "SDF", ...],
      "url": "https://...",
      "uren": {"nl": "Openingstijden kort, met (eigen site, gezien DD-MM-2026)", "en": "..."},
      "about": {"nl": "1–3 zinnen", "en": "..."},
      "earlier": {"nl": "Katten die er eerder waren, met jaartal en bron", "en": "..."},
      "katten": [
        {"soort": "Tijger", "ondersoort": "Amoer", "status": "g",
         "toelichting": {"nl": "...", "en": "..."},
         "aantal": {"nl": "2 (kater X en poes Y)", "en": "2 (male X and female Y)"},
         "bron": "Eigen site soortpagina (gezien 22-10-2026); NRK 12-05-2026",
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
