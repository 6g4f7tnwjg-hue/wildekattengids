# Open punten

Bijgehouden door Claude. Bijwerken als een punt is opgelost.

## Voor later (afgesproken)

- **Voedertijden en verzorgerspraatjes** toevoegen bij de top 10 (en eventueel in de gidsen).
- **Overzeese gebieden van Frankrijk** (bijv. Zoo de Guyane: jaguar, ocelot, margay): nog beslissen of ze erbij komen.
- **Foto's van Franse parken**: veel locaties hebben nog geen foto (Commons gaf een limiet). Een rustige extra ronde.
- **Maandelijkse controle**: een geplande taak die nieuws over geboortes, vertrek en aankomst zoekt en voorstellen doet.
- **Volgend land**: het Verenigd Koninkrijk staat erin (14-10-2026, NL/EN/DE). Keuze voor daarna volgt. Als de website sneller moet: de vaste JS van de deelstaatblokken één keer delen in plaats van per blok (scheelt ±4 MB).
- **VK nagaan**: Longleat (eigen site geblokkeerd; alles uit nieuws), Whipsnade (eigen site geblokkeerd), Amazon World (Isle of Wight: oude pagina noemt ocelot en Geoffroy’s kat), Green Dragon Eco Farm (alleen Zootierliste: lynx en wilde kat; niet opgenomen), Mole Hall en Galloway Wildlife Park (mogelijk dicht), Borth Wild Animal Kingdom (katten 2020–2021 weg). Een officiële landelijke lijst van vergunde dierentuinen is niet openbaar; de nieuwste volledige lijst is een FOI-antwoord van APHA uit 2018–2019.
- **Zwitserland in het Frans**: de gids is nu NL/EN/DE. Frans erbij kan met een tweede versie van elk regioblok (NL/EN/FR) die de pagina laadt bij de taalknop FR.
- **Oostenrijk/Zwitserland nagaan**: Tiger’s World (Judenau, NÖ) — alleen op een toeristische site, eigen site niet te openen, niet opgenomen; Luchsgehege Loipersdorf (ligging en publiek onbekend); Parc animalier de Prêles (BE) niet nagelopen; Bioparc Genève houdt ook hybride wilde katten en savannahkatten (niet meegeteld).
- **Fréjus (Var)**: dierentuin dicht sinds 30-8-2026; na eind november 2026 nagaan waar de katten zijn gebleven.
- **Kapotte links op de losse soortpagina’s (website)** (gezien 14-10-2026, bestond al vóór de taalwijziging): 586 links naar soortpagina’s binnen een deelstaat of regio die daar niet bestaan (bijv. `oostenrijk/steiermark/soort/manoel/`). Komt uit de “lijkt op”-verwijzingen op de momentopnames; in de interactieve gids werken ze wel.
- **Italië (15-10-2026)**:
  - **Top 10**: de lijst `vast` in `top10.json` telt tien parken, dus Italië staat er nu niet in. Beste Italiaanse kandidaat: Parco Faunistico La Torbiera (8 soorten, o.a. vissende kat, manoel, nevelpanter; score 80, nummer 10 heeft 86). Beslissen of er een park uit moet.
  - **UIZA**: geen actuele ledenlijst; gebruikt is de lijst van aangesloten parken op uiza.org (januari 2022). Napoli, Fasano, Ravenna en Pombia staan niet bij EAZA of UIZA en heten daarom dierenpark of safaripark.
  - **Ministeriële lijst** (MASE, oktober 2025): “BIN snc” (Trentino) niet thuisgebracht.
  - **Circussen**: 13 reizende circussen, momentopnames (dompteurs wisselen van circus). Het volledige verbod op wilde dieren in circussen is uitgesteld tot eind 2026: begin 2027 opnieuw nagaan.
  - **Nagaan**: Bioparco di Roma (site gaf 403; leeuw en luipaard nu onzeker, verblijf in verbouwing), Simba Little Wild Park (sloopbevel kooien augustus 2025), Le Cornelle (Amoertijger), Valcorba (Amoer-luipaardkat), Zoo delle Star (leeuw, luipaard), de Area faunistica della Lince in Civitella Alfedena (nieuwe lynx?).
  - **Foto's**: geen eigen foto's van Italiaanse parken (afspraak: geen foto's van dierentuinen zoeken).
- **Onderzoeksagenten**: in de opdracht zetten dat ze geen persoonlijke gegevens meesturen (ook niet als contact in een User-Agent).

- **Controle op gemiste parken in Frankrijk (13-10-2026)**: vergeleken met de officiële lijst (ICPE-rubriek 2140, Géorisques: 196 vergunde dierenparken), Zootierliste en Nature et Zoo; geen gemiste locaties met katten. Nog onduidelijk, mogelijk navragen bij de DDPP: een vergunning op naam van een particulier in Grignols (Gironde) en de vereniging Gaia in Allennes-les-Marais (Nord); van geen van beide is een site of bezoekinformatie gevonden.
- **Sigean**: Nature et Zoo noemt een serval (sinds 2023), de eigen site en het persdossier 2026 niet. Niet opgenomen.
- **Citadelle van Besançon**: in februari 2024 kwam er een in beslag genomen serval binnen (tijdelijke opvang?); niet op de eigen site. Niet opgenomen.

## Bronnen en valkuilen (geleerd bij Italië, oktober 2026)

**Bronnen Italië**
- **Ministeriële lijst:** “Elenco strutture licenziate” van het ministerie van Milieu (MASE, wet D.Lgs. 73/2005), via mase.gov.it/pagina/giardini-zoologici. Versie oktober 2025: 37 instellingen plus het regionaal erkende park van Introd; ook aquaria en vlindertuinen.
- **UIZA:** geen openbare ledenlijst; alleen de lijst van aangesloten parken op uiza.org/link-utili (januari 2022).
- **EAZA:** de ledenpagina geeft een 404; de ledenkaart haalt de gegevens uit `https://www.eaza.net/page-data/sq/d/2685603474.json`.
- **Zootierliste:** geen landpagina met alle instellingen; bouw de lijst per soort op, met de filters “Aktuelle” en “Ehemalige”.
- **Circussen:** de katten horen bij dompteurs en hun stallen (o.a. Montico, Vassallo, Martini, Berosini, Caroli, Nicolay) en wisselen vaak van circus. Beste bronnen: circusfans.eu (ook de rss-zoekfunctie) en PassioneCirco. Geen officieel register.
- **Sardinië:** de wilde kat daar (*Felis lybica sarda*) is een Afrikaanse wilde kat; opvangcentra (zoals Bonassai) laten ze weer vrij, er is er geen te bezoeken.

**Valkuilen**
- **Italiaanse namen:** *gattopardo africano* = serval, *lince del deserto* = caracal, *leopardo melanico* = zwarte panter, *gatto leopardo* = luipaardkat (niet de huiskat Bengal), *ghepardo* = cheetah, *gatto di Pallas* = manoel.
- **Oude soortpagina’s:** een soortpagina op de eigen site bewijst niet dat het dier er nog is (Le Cornelle: Amoertijger, Romeo overleden in 2024). Vergelijk met de parkkaart (Valcorba: luipaardkat niet meer op de kaart van 2026) en let op verwijderde pagina’s die een 404 geven (Cappeller: caracal).
- **Eén eigenaar, meerdere parken:** dieren verhuizen tussen parken van dezelfde eigenaar (groep De Rocchi: Pombia, Le Cornelle, Zoosafari Fasano, Safari Ravenna). Een “nieuwe” kat in het ene park is vaak een vertrokken kat uit het andere.
- **Dierentuin of dierenpark:** een park met EEP-dieren is niet automatisch lid van EAZA (Zoo di Napoli). Controleer het lidmaatschap altijd in de ledenlijst.

## Bewust niet in de gids (opnieuw bekijken als er iets verandert)

- **ROAAR (Trets)**: opvang van ex-circustijgers en -leeuwen; alleen bezoek voor peters (500 euro per jaar).
- **Caresse de tigre (Seine-Maritime)**: omstreden opvang; geen bezoekinformatie, geen nieuws na 2023.
- **Big Cats (Mézos, Landes)**: opening door de prefectuur geweigerd (2025).
- **Tonga Terre d'Accueil (Loire)** en **Sanctuaire Oural (Sancy)**: niet open voor publiek.
- **Zoo des 3 Vallées (Tarn)**: gesloten; katten in 2025–2026 weggehaald.

## Twijfelgevallen in de gidsen

Status w = onzeker (telt niet als bevestigd), p = gepland, y = tijdelijk niet zichtbaar, b = vertrek aangekondigd. Stand 14 oktober 2026.

Regel (voor alle landen, 14-10-2026): bevestigd alleen met een recente bron (2025–2026); onzeker alleen met een concrete aanwijzing van na 2024; is de laatste aanwijzing van vóór 2024 of is het dier aantoonbaar weg, dan naar “Eerder hier”; zonder betrouwbare bron geschrapt.

### Duitsland

**Nedersaksen**

- [p] Erlebnis-Zoo Hannover – vissende kat: komt bij de binturongs in de Dschungelpalast; nog niet aangekomen (stand 21-9-2026)
- [w] Tierpark Ströhen – cheetah: Staat nog op de peterschapslijst van de eigen site (okt. 2026); laatst gezien bij een bezoek in okt. 2024. Geen eigen bericht of bezoekersmelding uit 2025–2026 gevonden.
- [w] Tierpark Ströhen – serval: Staat nog op de peterschapslijst van de eigen site (okt. 2026); laatst gezien bij een bezoek in okt. 2024. Geen eigen bericht of bezoekersmelding uit 2025–2026 gevonden.
- [w] Wildpark Neuhaus – Europese wilde kat: Laatst gezien in 2020. Het park hield op 8-8-2025 een themadag ‘Katzen’ (‘Werdet zum Wildkatzenprofi’), maar noemt de wilde kat nergens als bewoner; geen recente waarneming.
- [w] Wildtierstation Sachsenhagen – Europese wilde kat: Opvangstation met wildekattenverblijf (2015): wilde katten worden opgevangen en uitgezet (vrouwtje uitgezet 16-4-2026). Of er nu een wilde kat zit en te zien is, is onbekend.
- [w] Wildtierstation Sachsenhagen – serval: Jan. 2025 één vrouwtje gezien; okt. 2025 twee in beslag genomen servals in quarantaine. Geen later bericht; opvangdieren worden vaak doorgeplaatst.
- [w] Artenschutzzentrum Grasleben – manoel: Manoel staat als nr. 19 op de plattegrond van april 2026, maar niet in de soortenlijst ‘Unsere Tiere’ (2026). Laatst gezien juli 2024; geen melding uit 2025–2026.
- [w] Tiergarten Ludwigslust – Euraziatische lynx: Lynx staat in de dierenlijst op de eigen pagina die voor seizoen 2026 is bijgewerkt (open 21-3 t/m 1-11-2026), maar de laatste gedateerde waarneming is van aug. 2022; parkplan uit 2021.
- [w] Tiergarten Ludwigslust – Europese wilde kat: Wilde kat staat in de dierenlijst op de eigen pagina die voor seizoen 2026 is bijgewerkt (open 21-3 t/m 1-11-2026), maar de laatste gedateerde waarneming is van aug. 2022; parkplan uit 2021.

**Noordrijn-Westfalen**

- [w] Tierpark Nadermann – luipaard: Op het parkplan 2026 staan twee zwarte ‘panters’ en in mei 2026 hing er een luipaardbord, maar er werd geen dier gezien. Laatste waarneming juli 2020. De zwarte ‘panters’ kunnen ook zwarte jaguars zijn.
- [w] Zoo Dortmund – Zuidelijke tijgerkat: In maart 2026 nog bebord, maar bij bezoeken in 2023, 2024, 2025 en maart 2026 niet gezien; laatste waarneming juli 2022 (toen 1,2).

**Saksen**

- [w] Zoo Leipzig – cheetah: Eigen site en zooplan noemen nog cheetah’s, maar volgens de Zootierliste ging in 2026 een vrouwtje uit Leipzig naar Zoo Saarbrücken. Eind 2025 was er nog maar één.
- [w] Tierpark Chemnitz – luipaard: Luipaardvrouwtje in 08/2025 nog gezien en de voedering staat nog op de site, maar op 18-9-2026 meldde het park ‘vorübergehend’ te stoppen met grote katten.
- [w] Zoo der Minis – caracal: Volgens de dierenlijst per 31-12-2024 nog een paar (1,1), maar bij een bezoek in 12/2024 niet gezien en niet in de peterschapslijst (mei 2024). Geen bericht uit 2025–2026.
- [w] Zoo der Minis – serval: Twee vrouwtjes volgens de dierenlijst per 31-12-2024, gezien in 12/2024 en vermeld in de peterschapslijst (mei 2024). Geen bericht of melding uit 2025–2026.

**Bayern**

- [w] Tiergarten Straubing – tijger: Sibirischer Tiger staat in het actuele dierenlexicon en op het parkplan, maar is na 09/2023 niet meer gezien: in juni 2026 een leeg verblijf met bord. Geen bericht van de dierentuin over de huidige tijgers.
- [p] Zoo Augsburg – sneeuwluipaard: verblijf in het nieuwe WB-Himalaya Land; opening uitgesteld naar 2027

**Rijnland-Palts**

- [p] Wildfreigehege Wildenburg – Euraziatische lynx: nieuw lynxverblijf in aanbouw

**Thüringen**

- [p] Tierpark Gotha – tijger: Mara en Tonga (Tanga), nakomelingen van Indira, wachten in opvang Primadomus (Spanje) op het nieuwe tijgerhuis.

**Saksen-Anhalt**

- [w] Tierpark Hexentanzplatz – Europese wilde kat: Bord stond er nog in 2-2025, maar de kat werd toen niet gezien; laatst gezien 10-2023. Niet op de eigen site; toeristische fiches (2026) noemen wel wilde katten.
- [w] Wildpark Christianental – Europese wilde kat: Site (2026) noemt wilde katten en er hangt een bord (5-2025), maar bij vijf bezoeken 2014–2025 nooit gezien.
- [w] Heimattierpark im Südpark – Europese wilde kat: Laatst gezien en bebord bij een bezoek in 11-2024; geen bron uit 2025–2026 gevonden en de stadssite noemt alleen lynxen.

**Baden-Württemberg**

- [w] Wildpark Bad Mergentheim – Europese wilde kat: Staat op de dierenlijst van het park, maar bezoekers van de Zootierliste zagen sinds 2022 nooit een wilde kat; geen recent eigen bericht.

**Berlijn**

- [w] Zoo Berlin – Zuidelijke tijgerkat: Er hangt nog een bord (4-2025, 6-2026) en het bestand eind 2024 was 1 kater, maar laatst gezien 7-2024.

### Frankrijk

**Hauts-de-France**

- [w] Parc Saint-Léger – Parc animalier – luipaard: Vroeger ‘Parc Les Grands Félins’ van de dompteurfamilie Bauer (in 2024 nog leeuwen, tijgers, cheeta’s, panters en poema’s aangeboden). Een gidsfiche (parcsetloisirs.fr, 2026) noemt panter, serval en lynx, maar de eigen plattegrond van 2026 noemt geen katten. Niet bevestigd dat er katten voor bezoekers te zien zijn. Niet nabellen (14-10-2026); opnieuw bekijken bij een nieuwe bron of als het park in april 2027 weer opengaat.
- [w] Parc Saint-Léger – Parc animalier – serval: Vroeger ‘Parc Les Grands Félins’ van de dompteurfamilie Bauer (in 2024 nog leeuwen, tijgers, cheeta’s, panters en poema’s aangeboden). Een gidsfiche (parcsetloisirs.fr, 2026) noemt panter, serval en lynx, maar de eigen plattegrond van 2026 noemt geen katten. Niet bevestigd dat er katten voor bezoekers te zien zijn. Niet nabellen (14-10-2026); opnieuw bekijken bij een nieuwe bron of als het park in april 2027 weer opengaat.
- [w] Parc Saint-Léger – Parc animalier – Euraziatische lynx: Vroeger ‘Parc Les Grands Félins’ van de dompteurfamilie Bauer (in 2024 nog leeuwen, tijgers, cheeta’s, panters en poema’s aangeboden). Een gidsfiche (parcsetloisirs.fr, 2026) noemt panter, serval en lynx, maar de eigen plattegrond van 2026 noemt geen katten. Niet bevestigd dat er katten voor bezoekers te zien zijn. Niet nabellen (14-10-2026); opnieuw bekijken bij een nieuwe bron of als het park in april 2027 weer opengaat.

**Auvergne-Rhône-Alpes**

- [w] Zoo de Lyon (Parc de la Tête d'Or) – manoel: Paar Banihal en Cota woont er volgens manulization.com (2026) en Zootierliste (1,1 in 2-2025), maar het verblijf is niet open voor publiek; geen eigen bericht van de zoo.

**Bretagne**

- [w] Les Terres de Nataé – nevelpanter: Op de eigen site en de Nature et Zoo-lijst (12-2025); in 6-2025 hing het bord, maar de nevelpanter werd niet gezien (laatst gezien 7-2022).
- [w] Les Terres de Nataé – serval: Op de eigen site en de Nature et Zoo-lijst (12-2025); in 6-2025 hing het bord, maar niet gezien. In 10-2021 nog maar één kater, laatst gezien 7-2022.

**Occitanie**

- [w] Parc Animalier de Pradinas (Parc animalier du Ségala) – Rode lynx: Er is een lynx (inspectie 2022, toeristische fiches), maar de soort is onzeker: het bord zegt 'Lynx rufus', de foto toont een Euraziatische lynx. Niet in Zootierliste.
- [y] Zoo de Montpellier (Parc zoologique Henri de Lunaret) – leeuw: zoo dicht 1-8-2026 tot 2e helft 2028; dieren blijven, sommige tijdelijk verplaatst
- [y] Zoo de Montpellier (Parc zoologique Henri de Lunaret) – cheetah: zoo dicht 1-8-2026 tot 2e helft 2028; dieren blijven, sommige tijdelijk verplaatst
- [y] EcoZonia – Terres de prédateurs – Zuidelijke tijgerkat: achter de schermen; bedoeld voor de nieuwe Andeszone

**Pays de la Loire**

- [w] Zoo de La Flèche – luipaard: Volgens een Facebookbericht van Zoo Hoyerswerda (28-4-2026) ging er een ♀ (geb. 2020) naar La Flèche, maar ze staat niet op de eigen site; of ze te zien is, is onbekend.

### Oostenrijk

**Opper-Oostenrijk**

- [w] Welser Tiergarten – Euraziatische lynx: Na de dood van Burli (aug. 2025) bleef alleen de zieke kat Fuchur over; niet bevestigd dat zij in okt. 2026 nog leeft. Dierenlijst noemt de lynx nog.

**Salzburg**

- [y] Zoo Salzburg (Hellbrunn) – Leeuw: nieuw paar in gewenning; leeuwenhuis nog dicht, nog niet te zien (sept. 2026)

**Stiermarken**

- [p] Tierpark Tragöß – Euraziatische lynx: site: 'Coming Soon'; volgens Facebook (via Zootierliste) sept. 2026 2 lynxen uit Wenen

**Karinthië**

- [w] Tierpark Rosegg – Euraziatische lynx: Geen dierenlijst op de eigen site; lynx alleen op foto's (2021) en in actuele toeristische beschrijvingen. Geen gedateerde bevestiging na 2024 gevonden.


### Zwitserland

**Mittelland**

- [w] Sikypark – Schweizer Tierrettungspark – Rode lynx: Alleen Zootierliste/Instagram 2025; niet op de eigen site of in de peterschapslijst.
- [w] Sikypark – Schweizer Tierrettungspark – Serval: Staat op de persoonlijkhedenpagina en volgens ZTL 2025 nog aanwezig, maar niet in de huidige peterschapslijst.

**Centraal-Zwitserland**

- [w] Toni's Zoo – Cheetah: Alleen een bezoekverslag 6/2025 en oudere toeristische teksten; geen bevestiging op de eigen site.
- [w] Toni's Zoo – Serval: Alleen Zootierliste-bezoekverslag 6/2025; geen eigen bron.
- [w] Toni's Zoo – Caracal: Alleen Zootierliste meldt een paar caracals sinds 2026; niet bevestigd.

### Verenigd Koninkrijk

**Zuidoost-Engeland**

- [w] Cotswold Wildlife Park – Nevelpanter: De FAQ (bijgewerkt juni 2026) en de toegankelijkheidspagina gebruiken 'by the Leopards' als oriëntatiepunt en Zootierliste noemt nevelpanters, maar de dierenlijst en het nieuws noemen ze niet.
- [w] Crocodiles of the World – Nevelpanter: De zoogdierpagina (bijgewerkt september 2026) noemt 'Clouded Leopard' alleen bij de adopties, niet in de tekst. Bij de inzamelactie voor nevelpanters in Nepal (2024) staat een foto 'Bao'. Zootierliste noemt de Indochinese nevelpanter.
- [b] Marwell Zoo – Tijger: alleen tijdelijk: Luca blijft ongeveer zes maanden terwijl zijn verblijf in The Big Cat Sanctuary (Kent) wordt verbouwd
- [b] The Big Cat Sanctuary – Aziatische goudkat: enige in het VK; vertrekt naar Tierpark Berlin (EEP)
- [w] Wingham Wildlife Park – Nevelpanter: Blog uit 2025 noemt de soort algemeen; geen recente bevestiging dat er nog nevelpanters te zien zijn.
- [w] Wingham Wildlife Park – Bengaalse kat: Alleen Zootierliste meldt een kater sinds 2024; niet op de eigen site gevonden.
- [w] Port Lympne Hotel & Reserve – Luipaard: Geen eigen soortpagina meer; alleen een bezoekverslag van feb. 2026 meldt nog één Amoerluipaard.
- [w] Hemsley Conservation Centre – Ocelot: Alleen genoemd als buurverblijf in een forumbericht van jan. 2026; geen eigen bron gevonden.

**Zuidwest-Engeland**

- [w] Exmoor Zoo – Vissende kat: Niet op de eigen site. Volgens Zootierliste in 2025 een paar uit de zoo van Colombo; forumpost noemde komst in najaar 2025. Niet bevestigd.
- [b] Combe Martin Wildlife & Dinosaur Park – Luipaard: ♂ Kazimir achter de schermen; vertrekt naar Zuid-Korea (fokprogramma)

**Oost-Engeland**

- [w] ZSL Whipsnade Zoo – Tijger: Alleen Wikipedia en Zootierliste melden komst van Crispin uit London Zoo in 2026; zoo-site was niet bereikbaar.
- [w] Hamerton Zoo Park – Luipaard: Volgens Zootierliste kwam in 2025 een zwart luipaardvrouwtje uit Lumigny (Frankrijk); niet in de sponsorlijst op de eigen site.
- [w] Jimmy's Farm & Wildlife Park – Jaguar: Alleen Zootierliste meldt een jaguar in bruikleen van Dartmoor Zoo (2026); niet op eigen site gevonden.

**West Midlands**

- [w] Hoo Zoo and Dinosaur World – Vissende kat: De pagina 'Fishing Cats' is in jan. 2026 opnieuw opgeslagen, maar heeft (anders dan de andere katten) geen tekst over het eigen dier en Zootierliste noemt geen vissende kat. Niet bevestigd.
- [w] Hoo Zoo and Dinosaur World – Bengaalse kat: Pagina 'Leopard Cat' in nov. 2025 bijgewerkt, maar alleen met algemene tekst; Zootierliste noemt geen bengaalse kat. Niet bevestigd.
- [w] Drayton Manor Zoo – Manoel: Volgens Zootierliste kwamen in 2026 twee vrouwtjes uit Port Lympne; niet op de dierenlijst van het park gevonden en geen nieuwsbericht.

**Yorkshire en de Humber**

- [w] Bridlington Animal Park – Caracal: Alleen Zootierliste (bezoek 10-2026, 'gesehen'); niet op de dierenlijst van het park. Op ZooChat is sprake van een lynx; mogelijk verwisseling.
- [y] Yorkshire Wildlife Park – Tijger: park na dodelijk incident (10-10-2026) gesloten; Altai wordt niet afgemaakt

**Schotland**

- [w] Calderglen Zoo – Europese wilde kat: Een reisgids (bijgewerkt juni 2025) noemt wilde katten; de eigen site noemt geen katten en er is geen recent bericht.

**Noord-Ierland**

- [y] Belfast Zoo – Cheetah: poes Mia tijdelijk in Fota Wildlife Park (EEP); terugkeer verwacht
