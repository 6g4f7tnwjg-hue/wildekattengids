# Landspecifieke tekstblokken van de Finse gids (NL / EN / FI). Stand 23 oktober 2026.
import re, unicodedata
def _slug(x):
    x = "".join(c for c in unicodedata.normalize("NFD", x) if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"\(.*?\)", "", x)).strip("-")
def L(naam): return f'<a href="#locatie/{_slug(naam)}">{naam}</a>'

# alleen landschappen met locaties, van zuid naar noord
REGN = {"uusimaa": ["Uusimaa", "Uusimaa", "Uusimaa"],
        "pohjois-karjala": ["Noord-Karelië", "North Karelia", "Pohjois-Karjala"],
        "etela-pohjanmaa": ["Zuid-Österbotten", "South Ostrobothnia", "Etelä-Pohjanmaa"],
        "pohjois-pohjanmaa": ["Noord-Österbotten", "North Ostrobothnia", "Pohjois-Pohjanmaa"],
        "lappi": ["Lapland", "Lapland", "Lappi"]}

KOR, AHT, RAN, KUU, KIT = L("Korkeasaari"), L("Ähtäri Zoo"), L("Ranua Wildlife Park"), L("Kuusamon Suurpetokeskus"), L("Kitee Zoo")

# losse vervangingen in het sjabloon (resten van Portugal in de Finse vaste teksten)
FI_VERV = [("Portugalissa", "Suomessa"), ("portugalilaiset eläintarhat", "suomalaiset eläintarhat")]
VAST = [
 (r'<p class="stamp">.*?</p>', '<p class="stamp"><span class="l-nl">Stand 23 oktober 2026</span><span class="l-en">Updated 23 October 2026</span><span class="l-fi">Päivitetty 23. lokakuuta 2026</span></p>'),
 (r'<p class="lede">.*?</p>', '<p class="lede">'
  '<span class="l-nl">Waar in Finland kun je tijgers, sneeuwluipaarden, manoels, lynxen en andere wilde katten zien? Per soort en per park zie je hier welke katten er wonen, welke jongen er onlangs geboren zijn en wat er binnenkort verandert.</span>'
  '<span class="l-en">Where in Finland can you see tigers, snow leopards, Pallas’s cats, lynxes and other wild cats? By species and by park, this guide shows which cats live where, which young were born recently and what is about to change.</span>'
  '<span class="l-fi">Missä Suomessa voit nähdä tiikereitä, lumileopardeja, manuleja, ilveksiä ja muita luonnonvaraisia kissaeläimiä? Opas kertoo lajeittain ja puistoittain, mitkä kissat asuvat missäkin, mitä poikasia on äskettäin syntynyt ja mikä on pian muuttumassa.</span></p>'),
]

LOC_INTRO = ["Alle dierentuinen, dierenparken en wildparken in Finland waar bezoekers wilde katten kunnen zien. Tik op een stip om te zien welke katten er wonen.",
             "All zoos, animal parks and wildlife parks in Finland where visitors can see wild cats. Tap a dot to see which cats live there.",
             "Kaikki Suomen eläintarhat, eläinpuistot ja villieläinpuistot, joissa voit nähdä luonnonvaraisia kissaeläimiä. Napauta pistettä, niin näet, mitä kissoja siellä asuu."]

def tldr():
    nl = f'''<div class="l-nl">
<div class="prose">
  <ul>
    <li><strong>8 soorten bevestigd</strong> op 4 locaties: 3 dierentuinen (lid van EAZA) en 1 roofdierpark dat je alleen met een gids bezoekt. In {KIT} is de lynx onzeker.</li>
    <li><strong>{KOR}</strong> in Helsinki heeft ze alle acht: leeuw, tijger, Amoerluipaard, sneeuwluipaard, lynx, Amoer-luipaardkat, manoel en Europese wilde kat. Je ziet in Finland dus alle soorten in één park.</li>
    <li><strong>De Euraziatische lynx</strong>, de wilde kat van Finland zelf, woont in alle vier parken, tot in Lapland ({RAN}).</li>
    <li><strong>Jonge katten:</strong> twee Amoerluipaarden (juli 2026) en drie manoels (mei 2026) in {KOR}.</li>
    <li><strong>Seizoen:</strong> {KOR} en {RAN} zijn het hele jaar open; {AHT} na een faillissement in 2025 alleen in de schoolvakanties, {KIT} en {KUU} vooral in de zomer.</li>
    <li><strong>Geen particulieren en geen circussen:</strong> uitheemse roofdieren mogen in Finland sinds 2016 niet particulier worden gehouden, en in circussen mogen alleen gedomesticeerde dieren optreden.</li>
  </ul>
  </div>
</div>'''
    en = f'''<div class="l-en">
<div class="prose">
  <ul>
    <li><strong>8 species confirmed</strong> at 4 locations: 3 zoos (EAZA members) and 1 predator park you can only visit with a guide. The lynx at {KIT} is uncertain.</li>
    <li><strong>{KOR}</strong> in Helsinki has all eight: lion, tiger, Amur leopard, snow leopard, lynx, Amur leopard cat, Pallas’s cat and European wildcat. So in Finland you can see every species in one park.</li>
    <li><strong>The Eurasian lynx</strong>, Finland’s own wild cat, lives in all four parks, as far north as Lapland ({RAN}).</li>
    <li><strong>Young cats:</strong> two Amur leopards (July 2026) and three Pallas’s cats (May 2026) at {KOR}.</li>
    <li><strong>Season:</strong> {KOR} and {RAN} are open all year; {AHT} only in school holidays since a bankruptcy in 2025, {KIT} and {KUU} mainly in summer.</li>
    <li><strong>No private keepers and no circuses:</strong> since 2016 exotic predators may not be kept privately in Finland, and only domesticated animals may perform in circuses.</li>
  </ul>
  </div>
</div>'''
    fi = f'''<div class="l-fi">
<div class="prose">
  <ul>
    <li><strong>8 lajia varmistettu</strong> 4 paikassa: 3 eläintarhaa (EAZAn jäseniä) ja 1 suurpetokeskus, johon pääsee vain oppaan kanssa. Ilves on epävarma: {KIT}.</li>
    <li><strong>{KOR}</strong> Helsingissä on kaikki kahdeksan: leijona, tiikeri, amurinleopardi, lumileopardi, ilves, amurinleopardikissa, manuli ja villikissa. Suomessa näet siis kaikki lajit yhdessä puistossa.</li>
    <li><strong>Ilves</strong>, Suomen oma luonnonvarainen kissaeläin, asuu kaikissa neljässä puistossa, Lappia myöten ({RAN}).</li>
    <li><strong>Poikaset:</strong> kaksi amurinleopardia (heinäkuu 2026) ja kolme manulia (toukokuu 2026): {KOR}.</li>
    <li><strong>Kausi:</strong> {KOR} ja {RAN} ovat auki ympäri vuoden; {AHT} vuoden 2025 konkurssin jälkeen vain koulujen lomilla, {KIT} ja {KUU} lähinnä kesällä.</li>
    <li><strong>Ei yksityisiä eikä sirkuksia:</strong> vieraslajisia petoeläimiä ei Suomessa ole saanut pitää yksityisesti vuodesta 2016, ja sirkuksissa saa esiintyä vain kotieläimiä.</li>
  </ul>
  </div>
</div>'''
    return nl + en + fi + "\n"

GEEN = [
 [("Dierentuinen en aquaria zonder katachtigen", "Zoos and aquariums without cats", "Eläintarhat ja akvaariot ilman kissaeläimiä"),
  "Sea Life Helsinki, Tropicario (Helsinki), Maretarium (Kotka), Särkänniemi (Tampere; aquarium en kinderboerderij), Zoolandia (Lieto; alleen boerderijdieren), Lomamäen lemmikkipuisto (Inkoo)",
  ["Sea Life Helsinki, Tropicario (Helsinki), Maretarium (Kotka), Särkänniemi (Tampere; aquarium and farm), Zoolandia (Lieto; farm animals only), Lomamäen lemmikkipuisto (Inkoo)",
   "Sea Life Helsinki, Tropicario (Helsinki), Maretarium (Kotka), Särkänniemi (Tampere; akvaario ja kotieläinpiha), Zoolandia (Lieto; vain kotieläimiä), Lomamäen lemmikkipuisto (Inkoo)"]],
 [("Opvang van wilde dieren (niet open voor publiek)", "Wildlife rescue (not open to the public)", "Villieläinhoitolat (eivät avoinna yleisölle)"),
  "De wildopvang van Korkeasaari (twee weeslynxen 2024–2026, nu in Ähtäri en het Zweedse Vildriket), Nordic Wildlife Care (Mustasaari), Kankaanpään eläinsuojeluyhdistys (drie lynxwelpen in 2024)",
  ["Korkeasaari’s wildlife hospital (two orphaned lynxes 2024–2026, now at Ähtäri and Vildriket in Sweden), Nordic Wildlife Care (Mustasaari), Kankaanpään eläinsuojeluyhdistys (three lynx kittens in 2024)",
   "Korkeasaaren villieläinsairaala (kaksi orpoa ilvestä 2024–2026, nyt Ähtärissä ja Ruotsin Vildriketissä), Nordic Wildlife Care (Mustasaari), Kankaanpään eläinsuojeluyhdistys (kolme ilvesvauvaa 2024)"]],
 [("Circussen zonder katten", "Circuses without cats", "Sirkukset ilman kissaeläimiä"),
  "Sirkus Finlandia, Sirkus Florentina, Sirkus Magnum; in Finse circussen mogen alleen gedomesticeerde dieren optreden",
  ["Sirkus Finlandia, Sirkus Florentina, Sirkus Magnum; only domesticated animals may perform in Finnish circuses",
   "Sirkus Finlandia, Sirkus Florentina, Sirkus Magnum; suomalaisissa sirkuksissa saa esiintyä vain kotieläimiä"]],
 [("Andere dierenparken en kinderboerderijen zonder katachtigen", "Other animal parks and farm parks without cats", "Muut eläinpuistot ja kotieläinpihat ilman kissaeläimiä"),
  "Kuopion eläinpuisto (alleen huiskatten), Escurial (Liminka; gesloten), PikkuKili (Lieksa), Kuusamon visenttipuisto, Ålands Viltsafari, Heinolan lintutarha, Haltialan kotieläintila, Orimattilan kotieläinpuisto, Kissankulman eläinpiha en andere kinderboerderijen",
  ["Kuopion eläinpuisto (domestic cats only), Escurial (Liminka; closed), PikkuKili (Lieksa), Kuusamon visenttipuisto, Ålands Viltsafari, Heinolan lintutarha, Haltialan kotieläintila, Orimattilan kotieläinpuisto, Kissankulman eläinpiha and other farm parks",
   "Kuopion eläinpuisto (vain kotikissoja), Escurial (Liminka; suljettu), PikkuKili (Lieksa), Kuusamon visenttipuisto, Ålands Viltsafari, Heinolan lintutarha, Haltialan kotieläintila, Orimattilan kotieläinpuisto, Kissankulman eläinpiha ja muut kotieläinpihat"]],
]
def geen(i):
    out = ""
    for row in GEEN:
        k, t, tr = row
        if i and tr: t = tr[i - 1]
        out += f"    <li><b>{k[i]}:</b> {t}</li>\n"
    return out

OFFICIEEL = [
 """<p>In Finland heeft elke dierentuin een vergunning nodig; sinds 2026 geeft de voedselautoriteit Ruokavirasto die af (daarvoor de regionale overheden). Er is geen openbare lijst van die vergunningen. Volgens Yle (juli 2025) zijn er twaalf vergunde dierentuinen; daarvan hebben er vijf wilde katten.</p>
    <p>Particulieren mogen sinds 2016 geen uitheemse roofdieren houden, ook geen kruisingen met huiskatten tot en met de vierde generatie. Sinds 2024 mogen in circussen alleen gedomesticeerde dieren optreden (dierenwelzijnswet 693/2023). Wilde katten zie je in Finland dus alleen in dierentuinen en dierenparken.</p>
    <p>De lijst in deze gids is opgebouwd uit dat overzicht, de ledenlijsten van EAZA en de Finse dierentuinvereniging (Suomen eläintarhayhdistys), Zootierliste (alle katachtigen, huidige en vroegere houders) en een zoektocht per landschap naar andere parken, opvang en circussen.</p>
    <p>Of een park een dierentuin heet, hangt in deze gids af van het lidmaatschap van EAZA.</p>
""",
 """<p>In Finland every zoo needs a permit; since 2026 these are issued by the Finnish Food Authority (Ruokavirasto), before that by the regional authorities. There is no public list of these permits. According to Yle (July 2025) there are twelve licensed zoos; five of them have wild cats.</p>
    <p>Since 2016 private individuals may not keep exotic predators, nor crosses with domestic cats up to the fourth generation. Since 2024 only domesticated animals may perform in circuses (Animal Welfare Act 693/2023). So in Finland you can only see wild cats in zoos and animal parks.</p>
    <p>The list in this guide was built from that overview, the member lists of EAZA and the Finnish zoo association (Suomen eläintarhayhdistys), Zootierliste (all cats, current and former holders) and a search region by region for other parks, rescue centres and circuses.</p>
    <p>Whether a park is called a zoo in this guide depends on EAZA membership.</p>
""",
 """<p>Suomessa jokainen eläintarha tarvitsee luvan; vuodesta 2026 sen myöntää Ruokavirasto (aiemmin aluehallintovirastot). Luvista ei ole julkista luetteloa. Ylen mukaan (heinäkuu 2025) luvallisia eläintarhoja on kaksitoista; niistä viidessä on luonnonvaraisia kissaeläimiä.</p>
    <p>Yksityiset eivät ole saaneet pitää vieraslajisia petoeläimiä vuodesta 2016, eivät myöskään kotikissan risteymiä neljänteen polveen asti. Vuodesta 2024 sirkuksissa on saanut esiintyä vain kotieläimiä (eläinten hyvinvointilaki 693/2023). Luonnonvaraisia kissaeläimiä näet Suomessa siis vain eläintarhoissa ja eläinpuistoissa.</p>
    <p>Oppaan luettelo perustuu tähän katsaukseen, EAZAn ja Suomen eläintarhayhdistyksen jäsenluetteloihin, Zootierlisteen (kaikki kissaeläimet, nykyiset ja entiset pitäjät) sekä maakunta kerrallaan tehtyyn hakuun muista puistoista, hoitoloista ja sirkuksista.</p>
    <p>Se, kutsutaanko puistoa oppaassa eläintarhaksi, riippuu EAZA-jäsenyydestä.</p>
"""]

ADVIES = [
 f"""<ul class="prose">
    <li><strong>Alle 8 soorten in één park:</strong> {KOR} (Helsinki), het hele jaar open. De manoelkater is meestal niet te zien; kom vroeg of bij het voeren.</li>
    <li><strong>De lynx</strong> zie je ook in {RAN} (Lapland, met ook de Amoer-luipaardkat), {AHT} en {KUU} (alleen met een gids); in {KIT} is hij onzeker.</li>
    <li><strong>{AHT}</strong> is alleen in de schoolvakanties open; kijk vóór je bezoek op de site.</li>
    <li><strong>Twijfel je over een dier?</strong> Bel of mail dan vóór je bezoek met het park.</li>
  </ul>
""",
 f"""<ul class="prose">
    <li><strong>All 8 species in one park:</strong> {KOR} (Helsinki), open all year. The male Pallas’s cat is usually out of sight; come early or at feeding time.</li>
    <li><strong>The lynx</strong> can also be seen at {RAN} (Lapland, also with the Amur leopard cat), {AHT} and {KUU} (guided visits only); at {KIT} it is uncertain.</li>
    <li><strong>{AHT}</strong> is only open in school holidays; check the website before you go.</li>
    <li><strong>Not sure about an animal?</strong> Call or email the park before your visit.</li>
  </ul>
""",
 f"""<ul class="prose">
    <li><strong>Kaikki 8 lajia yhdessä puistossa:</strong> {KOR} (Helsinki), auki ympäri vuoden. Manulikoiras on yleensä piilossa; tule aikaisin tai ruokinta-aikaan.</li>
    <li><strong>Ilveksen</strong> näet myös näissä: {RAN} (Lappi, myös amurinleopardikissa), {AHT} ja {KUU} (vain oppaan kanssa); epävarma: {KIT}.</li>
    <li><strong>{AHT}</strong> on auki vain koulujen lomilla; tarkista verkkosivulta ennen käyntiä.</li>
    <li><strong>Epävarma eläimestä?</strong> Soita tai lähetä sähköpostia puistoon ennen käyntiä.</li>
  </ul>
"""]

GEPLAND = [
 f"""<ul class="prose">
    <li><strong>{AHT}:</strong> na het faillissement van oktober 2025 alleen open in de schoolvakanties; de sneeuwluipaardpoes Juma is er niet meer.</li>
    <li><strong>{KUU}:</strong> de directie trad in 2026 af; de toekomst van het park is onzeker.</li>
    <li><strong>Seizoen voorbij:</strong> {KIT} sloot op 25 oktober 2026.</li>
    <li><span class="st st-w"><i></i></span> <strong>Onzeker:</strong> de lynx van {KIT} (geen eigen bron uit 2025–2026).</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Gepland</span> · <span class="st st-w"><i></i>Onzeker</span></p>
""",
 f"""<ul class="prose">
    <li><strong>{AHT}:</strong> since the bankruptcy of October 2025 only open in school holidays; the female snow leopard Juma is no longer there.</li>
    <li><strong>{KUU}:</strong> the management resigned in 2026; the park’s future is uncertain.</li>
    <li><strong>Season over:</strong> {KIT} closed on 25 October 2026.</li>
    <li><span class="st st-w"><i></i></span> <strong>Uncertain:</strong> the lynx at {KIT} (no own source from 2025–2026).</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Planned</span> · <span class="st st-w"><i></i>Uncertain</span></p>
""",
 f"""<ul class="prose">
    <li><strong>{AHT}:</strong> lokakuun 2025 konkurssin jälkeen auki vain koulujen lomilla; lumileopardinaaras Juma ei ole enää siellä.</li>
    <li><strong>{KUU}:</strong> johto erosi vuonna 2026; puiston tulevaisuus on epävarma.</li>
    <li><strong>Kausi on ohi:</strong> {KIT} sulkeutui 25. lokakuuta 2026.</li>
    <li><span class="st st-w"><i></i></span> <strong>Epävarma:</strong> ilves, {KIT} (ei omaa lähdettä vuosilta 2025–2026).</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Suunniteltu</span> · <span class="st st-w"><i></i>Epävarma</span></p>
"""]

KVTXT = {"nl": "Er zijn in Finland geen witte tijgers, witte leeuwen of zwarte panters gevonden.",
         "en": "No white tigers, white lions or black panthers were found in Finland.",
         "fi": "Suomesta ei löytynyt valkoisia tiikereitä, valkoisia leijonia eikä mustia panttereita."}
HYB = {"nl": "Er zijn geen lijgers, tigons of andere hybriden van wilde katten gevonden. Kruisingen van huiskatten en wilde katten (zoals savannahkatten) tot en met de vierde generatie mogen in Finland niet particulier worden gehouden; ze tellen in deze gids niet mee.",
       "en": "No ligers, tigons or other hybrids of wild cats were found. Crosses between domestic cats and wild cats (such as Savannah cats) up to the fourth generation may not be kept privately in Finland; they do not count in this guide.",
       "fi": "Ligereitä, tigoneita tai muita luonnonvaraisten kissaeläinten risteymiä ei löytynyt. Kotikissan ja villien kissaeläinten risteymiä (kuten savannahkissoja) ei Suomessa saa pitää yksityisesti neljänteen polveen asti; niitä ei lasketa oppaaseen."}
def _kleur():
    out = ""
    for lg in ["nl", "en", "fi"]:
        out += f'<div class="l-{lg}">\n  <p class="prose">{KVTXT[lg]}</p>\n</div>'
    out += '<h3 id="hybriden" style="font-size:22px;margin-top:30px"><span class="l-nl">Hybriden</span><span class="l-en">Hybrids</span><span class="l-fi">Risteymät</span></h3>\n'
    for lg in ["nl", "en", "fi"]:
        out += f'<div class="l-{lg}">\n<p class="prose">{HYB[lg]}</p>\n</div>'
    return out
KLEUR = _kleur()

UITLEG = {
 "werkwijze": {
  "nl": """<p class="prose">Voor alle Finse dierentuinen, dierenparken, aquaria, opvangcentra en circussen is nagegaan welke wilde katachtigen er te zien zijn. Omdat er geen openbare lijst is, komt de basislijst uit het overzicht van Yle (2025), de ledenlijsten van EAZA en de Finse dierentuinvereniging en Zootierliste; per landschap is daarna gezocht naar andere parken. Elke locatie is gecontroleerd op de eigen website, aangevuld met Fins nieuws. Bij elke vermelding staan de bron en de datum.</p>
  <p class="prose">Een kat telt mee als een bezoeker hem kan zien, ook als dat alleen met een gids kan. Vrij levende lynxen en dieren in de wildopvang tellen niet mee.</p>
  <p class="prose">De indeling in soorten volgt de standaard van de IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>""",
  "en": """<p class="prose">For all Finnish zoos, animal parks, aquariums, rescue centres and circuses, we checked which wild cats can be seen. As there is no public list, the base list comes from Yle’s overview (2025), the member lists of EAZA and the Finnish zoo association and Zootierliste; each region was then searched for other parks. Every location was checked on its own website, supplemented by Finnish news. Each entry shows its source and date.</p>
  <p class="prose">A cat counts if a visitor can see it, even if only with a guide. Free-living lynxes and animals in wildlife rescue do not count.</p>
  <p class="prose">Species follow the standard of the IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>""",
  "fi": """<p class="prose">Kävimme läpi kaikki Suomen eläintarhat, eläinpuistot, akvaariot, hoitolat ja sirkukset ja selvitimme, mitä luonnonvaraisia kissaeläimiä niissä voi nähdä. Koska julkista luetteloa ei ole, perusluettelo tulee Ylen katsauksesta (2025), EAZAn ja Suomen eläintarhayhdistyksen jäsenluetteloista ja Zootierlistestä; sen jälkeen etsimme muita puistoja maakunta kerrallaan. Jokainen paikka on tarkistettu sen omilta verkkosivuilta ja suomalaisista uutisista. Jokaisessa merkinnässä on lähde ja päivämäärä.</p>
  <p class="prose">Kissa lasketaan mukaan, jos kävijä voi nähdä sen, myös silloin kun se onnistuu vain oppaan kanssa. Vapaana elävät ilvekset ja hoitolan eläimet eivät ole mukana.</p>
  <p class="prose">Lajijako noudattaa IUCN/SSC Cat Classification Task Forcen standardia (Kitchener ym., 2017, <i>Cat News</i> Special Issue 11).</p>"""},
 "namen": {
  "nl": """<ul class="prose">
    <li><strong>Ilves</strong> is de Euraziatische lynx, <strong>lumileopardi</strong> de sneeuwluipaard, <strong>manuli</strong> de manoel en <strong>villikissa</strong> de Europese wilde kat.</li>
    <li><strong>Amurinleopardikissa</strong> is de Amoer-luipaardkat, een ondersoort van de Bengaalse kat (<i>Prionailurus bengalensis euptilura</i>), niet het huiskatras Bengaal.</li>
    <li><strong>Leeuw:</strong> de leeuwen van Korkeasaari zijn Aziatische leeuwen, sinds 2017 ingedeeld bij de noordelijke leeuw (<i>P. l. leo</i>).</li>
  </ul>""",
  "en": """<ul class="prose">
    <li><strong>Ilves</strong> is the Eurasian lynx, <strong>lumileopardi</strong> the snow leopard, <strong>manuli</strong> the Pallas’s cat and <strong>villikissa</strong> the European wildcat.</li>
    <li><strong>Amurinleopardikissa</strong> is the Amur leopard cat, a subspecies of the leopard cat (<i>Prionailurus bengalensis euptilura</i>), not the domestic Bengal breed.</li>
    <li><strong>Lion:</strong> the lions at Korkeasaari are Asiatic lions, since 2017 classified as the northern lion (<i>P. l. leo</i>).</li>
  </ul>""",
  "fi": """<ul class="prose">
    <li>Opas on kirjoitettu hollanniksi; suomenkieliset lajinimet näkyvät lajisivuilla. <strong>Ilves</strong> on hollanniksi <i>Euraziatische lynx</i>, <strong>lumileopardi</strong> <i>sneeuwluipaard</i> ja <strong>manuli</strong> <i>manoel</i>.</li>
    <li><strong>Amurinleopardikissa</strong> on leopardikissan alalaji (<i>Prionailurus bengalensis euptilura</i>), ei bengalinkissa-kotikissarotu.</li>
    <li><strong>Leijona:</strong> Korkeasaaren leijonat ovat aasianleijonia, jotka on vuodesta 2017 luettu pohjoiseen leijonaan (<i>P. l. leo</i>).</li>
  </ul>"""},
 "verdwenen": {
  "nl": f"""<p class="prose">Bij elk park staat onder “Eerder hier” welke katten er vroeger waren. Opvallend: de manoel van {RAN} (2013–2023) en de sneeuwluipaardkater Jamal van {AHT} (overleden 2023). De dierentuin van Suvenniemi (Kajaani) had vóór 1939 al lynx, cheetah en luipaard.</p>""",
  "en": f"""<p class="prose">Each park’s page lists under “Previously here” which cats it used to have. Notable: the Pallas’s cat at {RAN} (2013–2023) and the male snow leopard Jamal at {AHT} (died 2023). The old zoo of Suvenniemi (Kajaani) had lynx, cheetah and leopard before 1939.</p>""",
  "fi": f"""<p class="prose">Jokaisen puiston sivulla kerrotaan kohdassa ”Aiemmin täällä”, mitä kissoja siellä on ollut. Mainitsemisen arvoisia: manuli ({RAN}, 2013–2023) ja lumileopardiuros Jamal ({AHT}, kuoli 2023). Kajaanin Suvenniemen eläintarhassa oli jo ennen vuotta 1939 ilves, gepardi ja leopardi.</p>"""},
 "controle": {
  "nl": """<p class="prose"><strong>Lijsten en regels:</strong> het overzicht van Yle (09-07-2025), de ledenlijsten van EAZA (oktober 2026) en de Finse dierentuinvereniging, de dierenwelzijnswet 693/2023 en het verbod op het houden van uitheemse dieren (704/2019).</p>
  <p class="prose"><strong>Databanken:</strong> Zootierliste (alle katachtigen, huidige en vroegere houdingen), alleen aanvullend.</p>
  <p class="prose"><strong>Websites van de parken</strong>, met dierenlijsten, soortpagina’s, kalenders en nieuws.</p>
  <p class="prose"><strong>Nieuws:</strong> onder meer Yle, Helsingin Sanomat en regionale kranten.</p>""",
  "en": """<p class="prose"><strong>Lists and rules:</strong> Yle’s overview (09-07-2025), the member lists of EAZA (October 2026) and the Finnish zoo association, the Animal Welfare Act 693/2023 and the ban on keeping exotic animals (704/2019).</p>
  <p class="prose"><strong>Databases:</strong> Zootierliste (all cats, current and former holdings), used only as a supplement.</p>
  <p class="prose"><strong>Park websites</strong>, with animal lists, species pages, calendars and news.</p>
  <p class="prose"><strong>News:</strong> including Yle, Helsingin Sanomat and regional newspapers.</p>""",
  "fi": """<p class="prose"><strong>Luettelot ja säännöt:</strong> Ylen katsaus (09-07-2025), EAZAn (lokakuu 2026) ja Suomen eläintarhayhdistyksen jäsenluettelot, eläinten hyvinvointilaki 693/2023 sekä vieraslajien pitokielto (704/2019).</p>
  <p class="prose"><strong>Tietokannat:</strong> Zootierliste (kaikki kissaeläimet, nykyiset ja entiset pitopaikat), vain täydentävänä.</p>
  <p class="prose"><strong>Puistojen verkkosivut</strong> eläinluetteloineen, lajisivuineen, kalentereineen ja uutisineen.</p>
  <p class="prose"><strong>Uutiset:</strong> muun muassa Yle, Helsingin Sanomat ja alueelliset lehdet.</p>"""},
}
