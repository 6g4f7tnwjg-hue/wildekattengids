# Landspecifieke tekstblokken van de Tsjechische gids (NL / EN / CS). Stand 22 oktober 2026.
import re, unicodedata
def _slug(x):
    x = "".join(c for c in unicodedata.normalize("NFD", x) if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"\(.*?\)", "", x)).strip("-")
def L(naam): return f'<a href="#locatie/{_slug(naam)}">{naam}</a>'

REGN = {"karlovarsky": ["Karlsbad", "Karlovy Vary Region", "Karlovarský kraj"],
        "plzensky": ["Pilsen", "Plzeň Region", "Plzeňský kraj"],
        "ustecky": ["Ústí nad Labem", "Ústí nad Labem Region", "Ústecký kraj"],
        "stredocesky": ["Midden-Bohemen", "Central Bohemia", "Středočeský kraj"],
        "praha": ["Praag", "Prague", "Praha"],
        "jihocesky": ["Zuid-Bohemen", "South Bohemia", "Jihočeský kraj"],
        "liberecky": ["Liberec", "Liberec Region", "Liberecký kraj"],
        "kralovehradecky": ["Hradec Králové", "Hradec Králové Region", "Královéhradecký kraj"],
        "pardubicky": ["Pardubice", "Pardubice Region", "Pardubický kraj"],
        "vysocina": ["Vysočina", "Vysočina", "Kraj Vysočina"],
        "jihomoravsky": ["Zuid-Moravië", "South Moravia", "Jihomoravský kraj"],
        "olomoucky": ["Olomouc", "Olomouc Region", "Olomoucký kraj"],
        "zlinsky": ["Zlín", "Zlín Region", "Zlínský kraj"],
        "moravskoslezsky": ["Moravië-Silezië", "Moravian-Silesian Region", "Moravskoslezský kraj"],
        "circus": ["Reizende circussen", "Travelling circuses", "Kočovné cirkusy"]}

PRA, OST, OLO, PLZ, HLU, TAB = L("Zoo Praha"), L("Zoo Ostrava"), L("Zoo Olomouc"), L("Zoo Plzeň"), L("Zoo Hluboká"), L("Zoo Tábor")
OTH, LIB, DVK, HOD, ZLI, JIH = L("Othello Park"), L("Zoo Liberec"), L("Safari Park Dvůr Králové"), L("Zoo Hodonín"), L("Zoo Zlín"), L("Zoo Jihlava")
BRN, CHV, KAR, DOK, KLE, ZVO = L("Zoo Brno"), L("Kočkovité šelmy Chvojenec"), L("Rekreační park Karlštejn"), L("Zoopark Doksy (Doksyland)"), L("Particuliere houder Kletečná"), L("Zoopark Zvole")
RIN, RAB, DVO, PLA, CHL, UST = L("Ringelland"), L("Animal Park Rabina"), L("Zoo Dvorec"), L("Zoo Plasy"), L("Zoo Chleby"), L("Zoo Ústí nad Labem")
HRA, FAU, EXO, HUM, BOB, SIM = L("Zoo Na Hrádečku"), L("Faunapark Horní Lipová"), L("Exotika na ranči"), L("Cirkus Humberto"), L("Cirkus Bob Navarro King"), L("Cirkus Šimek")

# losse vervangingen in het sjabloon (regex -> tekst)
CS_VERV = [("v Portugalsku", "v Česku"), ("V Portugalsku", "V Česku"), ("portugalských", "českých"), ("portugalské", "české")]
VAST = [
 (r'<p class="stamp">.*?</p>', '<p class="stamp"><span class="l-nl">Stand 22 oktober 2026</span><span class="l-en">Updated 22 October 2026</span><span class="l-cs">Aktualizováno 22. října 2026</span></p>'),
 (r'<p class="lede">.*?</p>', '<p class="lede">'
  '<span class="l-nl">Waar in Tsjechië kun je leeuwen, tijgers, sneeuwluipaarden, manoels en andere wilde katten zien? Per soort en per park zie je hier welke katten er wonen, welke jongen er onlangs geboren zijn en wat er binnenkort verandert. En met welke route je alle soorten ziet.</span>'
  '<span class="l-en">Where in Czechia can you see lions, tigers, snow leopards, Pallas’s cats and other wild cats? By species and by park, this guide shows which cats live where, which young were born recently and what is about to change. And which route lets you see every species.</span>'
  '<span class="l-cs">Kde v Česku uvidíš lvy, tygry, irbisy, manuly a další divoké kočky? Podle druhů i podle parků ti průvodce ukáže, které kočky kde žijí, jaká mláďata se nedávno narodila a co se brzy změní. A jakou trasou uvidíš všechny druhy.</span></p>'),
]

LOC_INTRO = ["Alle dierentuinen, dierenparken, particuliere houders, opvangcentra en circussen in Tsjechië waar bezoekers wilde katten kunnen zien. Tik op een stip om te zien welke katten er wonen. Circussen staan niet op de kaart.",
             "All zoos, animal parks, private keepers, rescue centres and circuses in Czechia where visitors can see wild cats. Tap a dot to see which cats live there. Circuses are not on the map.",
             "Všechny zoologické zahrady, zooparky, soukromí chovatelé, záchranné stanice a cirkusy v Česku, kde můžeš vidět divoké kočky. Klepni na tečku a uvidíš, které kočky tam žijí. Cirkusy na mapě nejsou."]

def tldr():
    nl = f'''<div class="l-nl">
<div class="prose">
  <ul>
    <li><strong>23 soorten bevestigd</strong> op 37 locaties: 15 dierentuinen, 1 safaripark, 10 dierenparken, 8 particuliere houders (waarvan 3 circussen), 2 opvangcentra, en het lynxverblijf van Nationaal Park Šumava. Daarnaast zeven locaties met alleen onzekere of niet te bezoeken katten.</li>
    <li><strong>{PRA}, {OST} en {OLO}</strong> hebben elk 9 soorten, {PLZ} 8. Tsjechië heeft veel kleine katten: manoel, roestkat, jaguarundi, Geoffroy’s kat, margay, vissende kat, zandkat en twee soorten luipaardkatten.</li>
    <li><strong>Maar op één plek te zien:</strong> de ocelot, in het particuliere {OTH}.</li>
    <li><strong>Jonge katten:</strong> zes cheetahs in {OLO} en vijf in {PRA} (2026), Sri Lanka-luipaarden in {OST} (oktober 2026), Amoerpanters in {OLO}, leeuwen in {HOD}, servals in {DVK} en Amoertijgers in {HLU}.</li>
    <li><strong>Particulieren en circussen:</strong> in Tsjechië mogen particulieren grote katten houden (fokken is sinds 2022 verboden) en circussen mogen wilde katten tonen. Deze gids noemt ze met hun status; sommige zijn niet of alleen met een rondleiding te bezoeken.</li>
    <li><strong>Witte tijgers en witte leeuwen</strong> zie je vooral bij particuliere houders; in de erkende dierentuinen leeft nog één witte tijgerin ({LIB}).</li>
  </ul>
  </div>
</div>'''
    en = f'''<div class="l-en">
<div class="prose">
  <ul>
    <li><strong>23 species confirmed</strong> at 37 locations: 15 zoos, 1 safari park, 10 animal parks, 8 private keepers (3 of them circuses), 2 rescue centres and the lynx enclosure of Šumava National Park. In addition, seven locations with only uncertain cats or cats that cannot be visited.</li>
    <li><strong>{PRA}, {OST} and {OLO}</strong> each have 9 species, {PLZ} 8. Czechia has many small cats: Pallas’s cat, rusty-spotted cat, jaguarundi, Geoffroy’s cat, margay, fishing cat, sand cat and two species of leopard cat.</li>
    <li><strong>Only in one place:</strong> the ocelot, at the privately run {OTH}.</li>
    <li><strong>Young cats:</strong> six cheetahs at {OLO} and five at {PRA} (2026), Sri Lankan leopards at {OST} (October 2026), Amur leopards at {OLO}, lions at {HOD}, servals at {DVK} and Amur tigers at {HLU}.</li>
    <li><strong>Private keepers and circuses:</strong> in Czechia private individuals may keep big cats (breeding has been banned since 2022) and circuses may show wild cats. This guide lists them with their status; some cannot be visited or only on a guided tour.</li>
    <li><strong>White tigers and white lions</strong> are mainly kept by private keepers; the licensed zoos still have one white tigress ({LIB}).</li>
  </ul>
  </div>
</div>'''
    cs = f'''<div class="l-cs">
<div class="prose">
  <ul>
    <li><strong>23 potvrzených druhů</strong> na 37 místech: 15 zoologických zahrad, 1 safari park, 10 zooparků, 8 soukromých chovatelů (z toho 3 cirkusy), 2 záchranné stanice a rysí výběh Národního parku Šumava. K tomu sedm míst jen s nejistými kočkami nebo s kočkami, které se nedají navštívit.</li>
    <li><strong>{PRA}, {OST} a {OLO}</strong> mají po 9 druzích, {PLZ} 8. Česko má hodně malých koček: manula, kočku cejlonskou, jaguarundi, kočku slaništní, margaye, kočku rybářskou, kočku pouštní a dva druhy kočky bengálské.</li>
    <li><strong>Jen na jednom místě:</strong> ocelot, v soukromém {OTH}.</li>
    <li><strong>Mláďata:</strong> šest gepardů v {OLO} a pět v {PRA} (2026), levharti cejlonští v {OST} (říjen 2026), levharti mandžuští v {OLO}, lvi v {HOD}, servalové v {DVK} a tygři ussurijští v {HLU}.</li>
    <li><strong>Soukromí chovatelé a cirkusy:</strong> v Česku smějí soukromníci chovat velké kočky (rozmnožování je od roku 2022 zakázané) a cirkusy smějí ukazovat divoké kočky. Průvodce je uvádí i s jejich stavem; některé se nedají navštívit, nebo jen s průvodcem.</li>
    <li><strong>Bílé tygry a bílé lvy</strong> uvidíš hlavně u soukromých chovatelů; licencované zoo mají už jen jednu bílou tygřici ({LIB}).</li>
  </ul>
  </div>
</div>'''
    return nl + en + cs + "\n"

GEEN = [
 [("Erkende dierentuin, geen katachtigen", "Licensed zoo, no cats", "Licencovaná zoo bez kočkovitých šelem"),
  "Krokodýlí ZOO Protivín, Krokodýlí a želví ZOO Praha, Papouščí zoologická zahrada Bošovice, ZOO Mořský svět (Praha), Zoopark Nehvizdy, Zoo Park Vyškov (alleen een huiskat van het ras bengaal)",
  ["Krokodýlí ZOO Protivín, Krokodýlí a želví ZOO Praha, Papouščí zoologická zahrada Bošovice, ZOO Mořský svět (Prague), Zoopark Nehvizdy, Zoo Park Vyškov (only a domestic Bengal cat)",
   "Krokodýlí ZOO Protivín, Krokodýlí a želví ZOO Praha, Papouščí zoologická zahrada Bošovice, ZOO Mořský svět (Praha), Zoopark Nehvizdy, Zoo Park Vyškov (jen domácí kočka plemene bengálská)"]],
 [("Vroeger katachtigen, nu niet meer", "Cats in the past, not any more", "Dříve kočkovité šelmy, už ne"),
  "Tropic Hukvaldy (poema tot 2023), Zoopark Holčovice (leeuw alleen opgezet), Minizoo Svatá Kateřina (Chotěvice; tijgers alleen in oude bronnen), Zoopark Bašť (particulier, niet open)",
  ["Tropic Hukvaldy (puma until 2023), Zoopark Holčovice (lion only stuffed), Minizoo Svatá Kateřina (Chotěvice; tigers only in old sources), Zoopark Bašť (private, not open)",
   "Tropic Hukvaldy (puma do roku 2023), Zoopark Holčovice (lev jen vycpaný), Minizoo Svatá Kateřina (Chotěvice; tygři jen ve starých zdrojích), Zoopark Bašť (soukromý, nepřístupný)"]],
 [("Gesloten", "Closed", "Zavřeno"),
  "Minizoo Vendryně (gesloten door de milieu-inspectie), SEKO Zoopark (Louny; verbouwing)",
  ["Minizoo Vendryně (closed by the environmental inspectorate), SEKO Zoopark (Louny; rebuilding)",
   "Minizoo Vendryně (zavřena inspekcí životního prostředí), SEKO Zoopark (Louny; přestavba)"]],
 [("Circussen zonder katten", "Circuses without cats", "Cirkusy bez kočkovitých šelem"),
  "Cirkus Aleš (laatste tijgers in januari 2025 naar FELIDA, Nederland), Cirkus Jo-Joo, Národní cirkus Original Berousek (treedt niet meer op), Cirkus Sultán (gestopt in 2020)",
  ["Cirkus Aleš (last tigers went to FELIDA, the Netherlands, in January 2025), Cirkus Jo-Joo, Národní cirkus Original Berousek (no longer performs), Cirkus Sultán (stopped in 2020)",
   "Cirkus Aleš (poslední tygři odešli v lednu 2025 do FELIDA v Nizozemsku), Cirkus Jo-Joo, Národní cirkus Original Berousek (už nevystupuje), Cirkus Sultán (skončil v roce 2020)"]],
 [("Opvangcentra en natuurcentra zonder katten", "Rescue and nature centres without cats", "Záchranné stanice a přírodní centra bez koček"),
  "Záchranná stanice hl. m. Prahy (Jinonice), Stanice pro handicapovaná zvířata NP Šumava (Vimperk), Návštěvnické centrum Srní (alleen wolven), Kašperské Hory (informatiecentrum)",
  ["Záchranná stanice hl. m. Prahy (Jinonice), Stanice pro handicapovaná zvířata NP Šumava (Vimperk), Návštěvnické centrum Srní (wolves only), Kašperské Hory (information centre)",
   "Záchranná stanice hl. m. Prahy (Jinonice), Stanice pro handicapovaná zvířata NP Šumava (Vimperk), Návštěvnické centrum Srní (jen vlci), Kašperské Hory (informační středisko)"]],
 [("Andere dierenparken, minizoo’s en kinderboerderijen zonder katachtigen", "Other animal parks, mini zoos and farm parks without cats", "Další zooparky, minizoo a statky bez kočkovitých šelem"),
  "Zoopark Zelčín, Zookoutek Kunratice, Zookoutek Kamýk, Divoká zahrada Hostivař, Farmapark Muchomůrka (Soběhrdy), Zoopark Jeleni Homole (Drhovy), Akva-Tera Plzeň, Safari resort Hluboká u Borovan, Zookoutek Feferské rybníčky (Prachatice), Lesopark Amerika (Františkovy Lázně), Minizoo Diana en Minizoo Stará Role (Karlovy Vary), Malevilská zoo, Minizoo.cz (Kostomlaty pod Řípem), Zámecký zvěřinec Častolovice, Farma Wenet (Broumov), Fajnpark Chlumec nad Cidlinou, Babiččin dvoreček (Doudleby nad Orlicí), Zookoutek Zobal (Police nad Metují), Biopark Teplice, Zoopark Tuchořice, Zoopark Radonice, Zahrada Harta (Vysoké Mýto), Teracentrum Dolní Čermná, Areál dravců a sov Sychrov, Zámecké medvědárium Náchod, Podzámecká zahrada Kroměříž, Fauna park Valašské Meziříčí, Zookoutek DDM Třebíč, Zookoutek Zahrady Vysočiny (Žďár nad Sázavou), Horečky ranč (Lichnov), Minizoo Kružberk, Vodní miniZOO Baška, Aqua Terra Štramberk, MiniZoo SVČ Opava, Papilonia Ostrava, Zoopark Rapotín, Staroveská Myslivna",
  None],
]
def geen(i):
    out = ""
    for row in GEEN:
        k, t, tr = row
        if i and tr: t = tr[i - 1]
        out += f"    <li><b>{k[i]}:</b> {t}</li>\n"
    return out

OFFICIEEL = [
 """<p>In Tsjechië heeft elke dierentuin een licentie nodig van het ministerie van Milieu (wet nr. 162/2003 over dierentuinen). De nieuwste gepubliceerde lijst (27 maart 2025) telt 29 dierentuinen met licentie; een lijst van 2026 is niet gevonden.</p>
    <p>Daarnaast mogen particulieren grote katten houden, met registratie (CITES), een bewijs van vakbekwaamheid en eisen aan het verblijf. Sinds 2022 is het fokken van grote katten buiten erkende dierentuinen verboden. Eind 2023 waren er ongeveer 118 geregistreerde tijgers, van wie zo’n 85 bij particulieren. Circussen mogen wilde katten nog tonen, maar sinds 2022 niet meer fokken en geen na 2022 geboren dieren africhten.</p>
    <p>De lijst in deze gids is opgebouwd uit de ministeriële lijst, de ledenlijsten van UCSZOO (15 Tsjechische leden) en EAZA (14 Tsjechische leden), Zootierliste (alle katachtigen, huidige en vroegere houders) en een zoektocht per kraj naar kleinere parken, particulieren, opvang en circussen. Alle 29 dierentuinen met licentie zijn nagelopen.</p>
    <p>Of een park een dierentuin of een dierenpark heet, hangt in deze gids af van het lidmaatschap van EAZA of UCSZOO. Particuliere houders zonder dierentuinlicentie heten “particuliere houder”.</p>
""",
 """<p>In Czechia every zoo needs a licence from the Ministry of the Environment (Act no. 162/2003 on zoos). The latest published list (27 March 2025) has 29 licensed zoos; no 2026 list was found.</p>
    <p>Private individuals may also keep big cats, with registration (CITES), a certificate of competence and housing requirements. Since 2022 breeding big cats outside licensed zoos has been banned. At the end of 2023 there were about 118 registered tigers, around 85 of them with private keepers. Circuses may still show wild cats, but since 2022 they may not breed them or train animals born after 2022.</p>
    <p>The list in this guide was built from the ministry list, the member lists of UCSZOO (15 Czech members) and EAZA (14 Czech members), Zootierliste (all cats, current and former holders) and a search region by region for smaller parks, private keepers, rescue centres and circuses. All 29 licensed zoos were checked.</p>
    <p>Whether a park is called a zoo or an animal park in this guide depends on membership of EAZA or UCSZOO. Private keepers without a zoo licence are called “private keeper”.</p>
""",
 """<p>V Česku potřebuje každá zoologická zahrada licenci Ministerstva životního prostředí (zákon č. 162/2003 Sb. o zoologických zahradách). Poslední zveřejněný seznam (27. března 2025) uvádí 29 licencovaných zoo; seznam pro rok 2026 se nenašel.</p>
    <p>Velké kočky smějí chovat i soukromníci, s registrací (CITES), osvědčením o odborné způsobilosti a požadavky na ubikace. Od roku 2022 je rozmnožování velkých koček mimo licencované zoo zakázané. Na konci roku 2023 bylo registrováno asi 118 tygrů, z toho zhruba 85 u soukromníků. Cirkusy smějí divoké kočky dál ukazovat, ale od roku 2022 je nesmějí rozmnožovat ani cvičit zvířata narozená po roce 2022.</p>
    <p>Seznam v tomto průvodci vychází ze seznamu ministerstva, členských seznamů UCSZOO (15 českých členů) a EAZA (14 českých členů), databáze Zootierliste (všechny kočkovité šelmy, současní i dřívější chovatelé) a z hledání kraj po kraji: menší parky, soukromí chovatelé, záchranné stanice a cirkusy. Prošli jsme všech 29 licencovaných zoo.</p>
    <p>Zda se park v tomto průvodci jmenuje zoologická zahrada, nebo zoopark, závisí na členství v EAZA nebo UCSZOO. Soukromí chovatelé bez licence zoo jsou označeni jako „soukromý chovatel“.</p>
"""]

ADVIES = [
 f"""<ul class="prose">
    <li><strong>Alle 23 soorten in zes parken:</strong>
      <ul>
        <li><strong>Zoo Plzeň</strong>: sneeuwluipaard, Canadese lynx, rode lynx, Soendanese luipaardkat, cheetah (en leeuw, tijger, luipaard)</li>
        <li><strong>Zoo Hluboká</strong> (bij České Budějovice): zandkat, Europese wilde kat (en tijger, lynx)</li>
        <li><strong>Zoo Tábor</strong>: poema (en leeuw, tijger, lynx)</li>
        <li><strong>Othello Park</strong> (Žáravice, bij Pardubice): ocelot (en tijger, lynx, caracal)</li>
        <li><strong>Zoo Olomouc</strong>: jaguar, Bengaalse kat, serval (en leeuw, tijger, luipaard, cheetah, lynx, Geoffroy’s kat)</li>
        <li><strong>Zoo Ostrava</strong>: roestkat, vissende kat, manoel, jaguarundi, margay, caracal, Geoffroy’s kat (en leeuw, luipaard)</li>
      </ul>
    </li>
    <li><strong>Alternatieven:</strong> de poema zie je ook in {HRA} en {FAU}. Wie in Praag is: {PRA} heeft 9 soorten, waaronder manoel, jaguarundi en vissende kat.</li>
    <li><strong>{OTH}</strong> is een particulier park en alleen van woensdag tot en met zondag open; het is de enige plek met een ocelot.</li>
    <li><strong>Openingstijden</strong> staan op de pagina van elk park. Particuliere parken zijn vaak alleen in het seizoen open.</li>
    <li><strong>Twijfel je over een dier?</strong> Bel of mail dan vóór je bezoek met het park. Alle onzekere vermeldingen staan onder “Over” bij “Twijfelgevallen”.</li>
  </ul>
""",
 f"""<ul class="prose">
    <li><strong>All 23 species in six parks:</strong>
      <ul>
        <li><strong>Zoo Plzeň</strong>: snow leopard, Canada lynx, bobcat, Sunda leopard cat, cheetah (and lion, tiger, leopard)</li>
        <li><strong>Zoo Hluboká</strong> (near České Budějovice): sand cat, European wildcat (and tiger, lynx)</li>
        <li><strong>Zoo Tábor</strong>: puma (and lion, tiger, lynx)</li>
        <li><strong>Othello Park</strong> (Žáravice, near Pardubice): ocelot (and tiger, lynx, caracal)</li>
        <li><strong>Zoo Olomouc</strong>: jaguar, leopard cat, serval (and lion, tiger, leopard, cheetah, lynx, Geoffroy’s cat)</li>
        <li><strong>Zoo Ostrava</strong>: rusty-spotted cat, fishing cat, Pallas’s cat, jaguarundi, margay, caracal, Geoffroy’s cat (and lion, leopard)</li>
      </ul>
    </li>
    <li><strong>Alternatives:</strong> the puma can also be seen at {HRA} and {FAU}. If you are in Prague: {PRA} has 9 species, including Pallas’s cat, jaguarundi and fishing cat.</li>
    <li><strong>{OTH}</strong> is a private park, open only from Wednesday to Sunday; it is the only place with an ocelot.</li>
    <li><strong>Opening times</strong> are on each park’s page. Private parks are often only open in season.</li>
    <li><strong>Not sure about an animal?</strong> Call or email the park before your visit. All uncertain entries are listed under “About” in “Doubtful cases”.</li>
  </ul>
""",
 f"""<ul class="prose">
    <li><strong>Všech 23 druhů v šesti parcích:</strong>
      <ul>
        <li><strong>Zoo Plzeň</strong>: irbis, rys kanadský, rys červený, kočka sundská, gepard (a lev, tygr, levhart)</li>
        <li><strong>Zoo Hluboká</strong> (u Českých Budějovic): kočka pouštní, kočka divoká (a tygr, rys)</li>
        <li><strong>Zoo Tábor</strong>: puma (a lev, tygr, rys)</li>
        <li><strong>Othello Park</strong> (Žáravice u Pardubic): ocelot (a tygr, rys, karakal)</li>
        <li><strong>Zoo Olomouc</strong>: jaguár, kočka bengálská, serval (a lev, tygr, levhart, gepard, rys, kočka slaništní)</li>
        <li><strong>Zoo Ostrava</strong>: kočka cejlonská, kočka rybářská, manul, jaguarundi, margay, karakal, kočka slaništní (a lev, levhart)</li>
      </ul>
    </li>
    <li><strong>Alternativy:</strong> pumu uvidíš i v {HRA} a {FAU}. Kdo je v Praze: {PRA} má 9 druhů, mezi nimi manula, jaguarundi a kočku rybářskou.</li>
    <li><strong>{OTH}</strong> je soukromý park, otevřený jen od středy do neděle; je to jediné místo s ocelotem.</li>
    <li><strong>Otevírací doba</strong> je na stránce každého parku. Soukromé parky bývají otevřené jen v sezoně.</li>
    <li><strong>Nejsi si jistý/á zvířetem?</strong> Před návštěvou parku zavolej nebo napiš. Všechny nejisté záznamy najdeš v části „O průvodci“ u „Sporných případů“.</li>
  </ul>
"""]

GEPLAND = [
 f"""<ul class="prose">
    <li><span class="st st-p"><i></i></span> <strong>{LIB}:</strong> er komen Amoertijgers; het verblijf wordt sinds mei 2026 voorbereid (geen datum).</li>
    <li><strong>{OST}:</strong> het huis van de Indische katten is sinds 9 oktober 2026 tijdelijk dicht na de geboorte van twee Sri Lanka-luipaarden.</li>
    <li><strong>{TAB}:</strong> in het voorjaar van 2027 opent een opvangcentrum voor katten uit warme streken.</li>
    <li><strong>{PRA}:</strong> de Amoertijgerin Arila moet mogelijk tijdelijk weg vanwege een verbouwing.</li>
    <li><strong>Seizoen voorbij:</strong> {KAR} gaat pas in 2027 weer open, {DOK} sloot op 26 september 2026.</li>
    <li><span class="st st-w"><i></i></span> <strong>Niet te bezoeken of onzeker:</strong> {ZVO} (sinds augustus 2025 dicht), {RAB} (sinds najaar 2024 dicht), {KLE} (particulier, rechtszaak) en {RIN} (geen bronnen van na 2024).</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Gepland</span> · <span class="st st-w"><i></i>Onzeker</span></p>
""",
 f"""<ul class="prose">
    <li><span class="st st-p"><i></i></span> <strong>{LIB}:</strong> Amur tigers are coming; the enclosure has been in preparation since May 2026 (no date).</li>
    <li><strong>{OST}:</strong> the Indian cats house has been temporarily closed since 9 October 2026 after the birth of two Sri Lankan leopards.</li>
    <li><strong>{TAB}:</strong> a rescue centre for cats from warm climates opens in spring 2027.</li>
    <li><strong>{PRA}:</strong> the Amur tigress Arila may have to move temporarily because of building work.</li>
    <li><strong>Season over:</strong> {KAR} does not reopen until 2027, {DOK} closed on 26 September 2026.</li>
    <li><span class="st st-w"><i></i></span> <strong>Not open or uncertain:</strong> {ZVO} (closed since August 2025), {RAB} (closed since autumn 2024), {KLE} (private, court case) and {RIN} (no sources after 2024).</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Planned</span> · <span class="st st-w"><i></i>Uncertain</span></p>
""",
 f"""<ul class="prose">
    <li><span class="st st-p"><i></i></span> <strong>{LIB}:</strong> přijdou tygři ussurijští; výběh se připravuje od května 2026 (bez data).</li>
    <li><strong>{OST}:</strong> pavilon indických šelem je od 9. října 2026 dočasně zavřený po narození dvou levhartů cejlonských.</li>
    <li><strong>{TAB}:</strong> na jaře 2027 se otevře záchranné centrum pro kočky z teplých oblastí.</li>
    <li><strong>{PRA}:</strong> tygřice ussurijská Arila možná bude kvůli přestavbě dočasně jinde.</li>
    <li><strong>Sezona skončila:</strong> {KAR} se otevře až v roce 2027, {DOK} zavřel 26. září 2026.</li>
    <li><span class="st st-w"><i></i></span> <strong>Nepřístupné nebo nejisté:</strong> {ZVO} (zavřeno od srpna 2025), {RAB} (zavřeno od podzimu 2024), {KLE} (soukromý chov, soudní řízení) a {RIN} (žádné zdroje po roce 2024).</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Plánováno</span> · <span class="st st-w"><i></i>Nejisté</span></p>
"""]

def _kv(lg, titel, sp, naar, locs):
    return f'<h3>{titel} <a class="kv-sp" href="#soort/{sp}">{naar}</a></h3>\n  <ul class="prose">\n' + "".join(f"    <li>{x}</li>\n" for x in locs) + "  </ul>\n"
KV = [
 (("Witte tijger", "naar de tijger"), ("White tiger", "to the tiger"), ("Bílý tygr", "k tygrovi"), "tijger", [LIB, DVO, KAR, DOK, CHV]),
 (("Witte leeuw", "naar de leeuw"), ("White lion", "to the lion"), ("Bílý lev", "ke lvu"), "leeuw", [CHL, TAB, PLA, KAR, DOK, CHV]),
 (("Zwarte panter", "naar de luipaard"), ("Black panther", "to the leopard"), ("Černý panter", "k levhartovi"), "luipaard", [PLA, CHV]),
 (("Zwarte jaguar", "naar de jaguar"), ("Black jaguar", "to the jaguar"), ("Černý jaguár", "k jaguárovi"), "jaguar", [ZLI, OLO]),
]
KVTXT = {"nl": f"Een witte tijger heeft een recessieve mutatie in het gen SLC45A2 en is geen albino; binnen het Europese fokprogramma worden ze niet meer gefokt. De witte tijgerin Surya Bára in Liberec is de laatste in een Tsjechische dierentuin met licentie. Witte leeuwen hebben leucisme; zwarte panters en zwarte jaguars hebben melanisme. Ook {RIN} en {RAB} hadden witte tijgers en zwarte panters, maar zijn onzeker of dicht.",
         "en": f"A white tiger has a recessive mutation in the SLC45A2 gene and is not an albino; they are no longer bred within the European breeding programme. The white tigress Surya Bára in Liberec is the last one in a licensed Czech zoo. White lions have leucism; black panthers and black jaguars have melanism. {RIN} and {RAB} also had white tigers and black panthers, but are uncertain or closed.",
         "cs": f"Bílý tygr má recesivní mutaci genu SLC45A2 a není albín; v rámci evropského chovného programu se už nechovají. Bílá tygřice Surya Bára v Liberci je poslední v licencované české zoo. Bílí lvi mají leucismus; černí panteři a černí jaguáři mají melanismus. Bílé tygry a černé pantery měly i {RIN} a {RAB}, ty jsou ale nejisté nebo zavřené."}
HYB = {"nl": "Er zijn geen lijgers, tigons of andere hybriden van wilde katten met zekerheid gevonden. Zootierliste noemde vroeger tijgerhybriden bij Chvojenec; de eigen site noemt ze niet meer. In Zoo Plasy leeft een kruising van een serval en een huiskat; die telt in deze gids niet mee, net als savannah- en bengaalkatten.",
       "en": "No ligers, tigons or other hybrids of wild cats were found with certainty. Zootierliste formerly listed tiger hybrids at Chvojenec; its own site no longer mentions them. Zoo Plasy keeps a cross between a serval and a domestic cat; like Savannah and Bengal cats, it does not count in this guide.",
       "cs": "Ligři, tigoni ani jiní kříženci divokých koček se s jistotou nenašli. Zootierliste dříve uváděla křížence tygrů v Chvojenci; jejich vlastní web je už neuvádí. V Zoo Plasy žije kříženec servala a domácí kočky; stejně jako savannah a bengálské kočky se v tomto průvodci nepočítá."}
def _kleur():
    out = ""
    for i, lg in enumerate(["nl", "en", "cs"]):
        out += f'<div class="l-{lg}">\n' + "".join(_kv(lg, k[i][0], k[3], k[i][1], k[4]) for k in KV) + f'  <p class="prose">{KVTXT[lg]}</p>\n</div>'
    out += '<h3 id="hybriden" style="font-size:22px;margin-top:30px"><span class="l-nl">Hybriden</span><span class="l-en">Hybrids</span><span class="l-cs">Kříženci</span></h3>\n'
    for lg in ["nl", "en", "cs"]:
        out += f'<div class="l-{lg}">\n<p class="prose">{HYB[lg]}</p>\n</div>'
    return out
KLEUR = _kleur()

UITLEG = {
 "werkwijze": {
  "nl": """<p class="prose">Voor alle Tsjechische dierentuinen, dierenparken, particuliere houders, opvangcentra en circussen is nagegaan welke wilde katachtigen er te zien zijn. De basislijst komt uit de lijst van dierentuinen met licentie van het ministerie van Milieu (29 dierentuinen, maart 2025), de ledenlijsten van UCSZOO en EAZA en Zootierliste (alle katachtigen, huidige en vroegere houders); per kraj is daarna gezocht naar kleinere parken, particulieren, opvang en circussen. Elke locatie is gecontroleerd op de eigen website en in de jaarverslagen, aangevuld met Tsjechisch nieuws. Bij elke vermelding staan de bron en de datum.</p>
  <p class="prose">Een kat telt mee als een bezoeker hem kan zien, ook als dat maar op bepaalde dagen of met een rondleiding kan. Particuliere houders en circussen staan erin met een kanttekening; locaties die niet te bezoeken zijn, staan erin met de status “niet open voor publiek” en tellen niet als bevestigd.</p>
  <p class="prose">De indeling in soorten volgt de standaard van de IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>""",
  "en": """<p class="prose">For all Czech zoos, animal parks, private keepers, rescue centres and circuses, we checked which wild cats can be seen. The base list comes from the Ministry of the Environment list of licensed zoos (29 zoos, March 2025), the member lists of UCSZOO and EAZA, and Zootierliste (all cats, current and former holders); each region was then searched for smaller parks, private keepers, rescue centres and circuses. Every location was checked on its own website and in annual reports, supplemented by Czech news. Each entry gives the source and the date.</p>
  <p class="prose">A cat counts if a visitor can see it, even if only on certain days or on a guided tour. Private keepers and circuses are included with a note; locations that cannot be visited are listed as “not open to the public” and do not count as confirmed.</p>
  <p class="prose">Species follow the standard of the IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>""",
  "cs": """<p class="prose">U všech českých zoologických zahrad, zooparků, soukromých chovatelů, záchranných stanic a cirkusů jsme zjišťovali, které divoké kočkovité šelmy tam můžeš vidět. Základní seznam vychází ze seznamu licencovaných zoo Ministerstva životního prostředí (29 zoo, březen 2025), z členských seznamů UCSZOO a EAZA a z databáze Zootierliste (všechny kočkovité šelmy, současní i dřívější chovatelé); potom jsme kraj po kraji hledali menší parky, soukromé chovatele, záchranné stanice a cirkusy. Každé místo jsme ověřili na jeho webu a ve výročních zprávách, doplněno českými zprávami. U každého záznamu je zdroj a datum.</p>
  <p class="prose">Kočka se počítá, pokud ji návštěvník může vidět, i když jen v některé dny nebo s průvodcem. Soukromí chovatelé a cirkusy jsou uvedeni s poznámkou; místa, která se nedají navštívit, mají stav „nepřístupné veřejnosti“ a nepočítají se jako potvrzená.</p>
  <p class="prose">Rozdělení na druhy se řídí standardem IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>"""},
 "namen": {
  "nl": """<ul class="prose">
    <li><strong>Levhart</strong> is de luipaard (<strong>levhart cejlonský</strong> de Sri Lanka-luipaard, <strong>levhart mandžuský</strong> de Amoerpanter), <strong>irbis</strong> de sneeuwluipaard en <strong>gepard</strong> de cheetah.</li>
    <li><strong>Rys ostrovid</strong> is de Euraziatische lynx (in Tsjechische dierentuinen vaak de Karpatische), <strong>rys červený</strong> de rode lynx en <strong>karakal</strong> de caracal.</li>
    <li><strong>Kočka bengálská</strong> is de (wilde) Bengaalse kat of luipaardkat, niet het huiskatras Bengaal. De Palawan-luipaardkat (Zoo Praha, Zoo Plzeň) hoort volgens de indeling van 2017 bij de Soendanese luipaardkat.</li>
    <li><strong>Kočka cejlonská</strong> is de roestkat, <strong>kočka slaništní</strong> Geoffroy’s kat, <strong>kočka rybářská</strong> de vissende kat en <strong>kočka pouštní</strong> de zandkat.</li>
    <li><strong>Leeuw:</strong> sinds 2017 zijn er twee ondersoorten: de noordelijke leeuw (<i>P. l. leo</i>), waartoe de Berberleeuwen en de Aziatische leeuwen horen, en de zuidelijke leeuw (<i>P. l. melanochaita</i>). De Noord-Chinese luipaard hoort bij de Amoerpanter (<i>P. p. orientalis</i>).</li>
    <li><strong>Vrij levende wilde katten</strong> vallen buiten dit overzicht: de Euraziatische lynx leeft wild in het Šumava-gebergte en de Europese wilde kat komt in Tsjechië weer voor.</li>
  </ul>""",
  "en": """<ul class="prose">
    <li><strong>Levhart</strong> is the leopard (<strong>levhart cejlonský</strong> the Sri Lankan leopard, <strong>levhart mandžuský</strong> the Amur leopard), <strong>irbis</strong> the snow leopard and <strong>gepard</strong> the cheetah.</li>
    <li><strong>Rys ostrovid</strong> is the Eurasian lynx (in Czech zoos often the Carpathian lynx), <strong>rys červený</strong> the bobcat and <strong>karakal</strong> the caracal.</li>
    <li><strong>Kočka bengálská</strong> is the (wild) leopard cat, not the Bengal domestic cat breed. According to the 2017 classification, the Palawan leopard cat (Zoo Praha, Zoo Plzeň) belongs to the Sunda leopard cat.</li>
    <li><strong>Kočka cejlonská</strong> is the rusty-spotted cat, <strong>kočka slaništní</strong> Geoffroy’s cat, <strong>kočka rybářská</strong> the fishing cat and <strong>kočka pouštní</strong> the sand cat.</li>
    <li><strong>Lion:</strong> since 2017 there are two subspecies: the northern lion (<i>P. l. leo</i>), which includes the Barbary and Asiatic lions, and the southern lion (<i>P. l. melanochaita</i>). The North Chinese leopard belongs to the Amur leopard (<i>P. p. orientalis</i>).</li>
    <li><strong>Free-living wild cats</strong> are outside the scope of this guide: the Eurasian lynx lives wild in the Šumava mountains, and the European wildcat is found in Czechia again.</li>
  </ul>""",
  "cs": """<ul class="prose">
    <li>Průvodce používá české názvy podle BioLibu; v nizozemské verzi jsou názvy nizozemské. Kočka bengálská je divoká kočka (<i>Prionailurus bengalensis</i>), ne plemeno domácí kočky.</li>
    <li>Kočka palawanská (Zoo Praha, Zoo Plzeň) patří podle rozdělení z roku 2017 ke kočce sundské (<i>P. javanensis</i>).</li>
    <li><strong>Lev:</strong> od roku 2017 se rozlišují dva poddruhy: lev severní (<i>P. l. leo</i>), kam patří lev berberský i lev indický, a lev jižní (<i>P. l. melanochaita</i>). Levhart severočínský patří k levhartu mandžuskému (<i>P. p. orientalis</i>).</li>
    <li><strong>Volně žijící kočky</strong> do přehledu nepatří: rys ostrovid žije volně na Šumavě a kočka divoká se v Česku znovu vyskytuje.</li>
  </ul>"""},
 "verdwenen": {
  "nl": f"""<p class="prose">Bij elk park staat onder “Eerder hier” welke katten er vroeger waren. Opvallend: de Sri Lanka-luipaard en de vissende katten van {BRN} (in 2025 vertrokken), de laatste Europese wilde kat van {OLO} (overleden juli 2025), de cheetah van Zoopark Zvole en de katten van circussen die gestopt zijn (Cirkus Aleš, Cirkus Sultán). In beslag genomen katten gingen vaak via {LIB} naar de opvang FELIDA in Nederland.</p>""",
  "en": f"""<p class="prose">Each park’s page lists under “Previously here” which cats it used to have. Notable: the Sri Lankan leopard and fishing cats of {BRN} (left in 2025), the last European wildcat at {OLO} (died July 2025), the cheetah of Zoopark Zvole and the cats of circuses that have stopped (Cirkus Aleš, Cirkus Sultán). Confiscated cats often went via {LIB} to the FELIDA rescue centre in the Netherlands.</p>""",
  "cs": f"""<p class="prose">U každého parku je v části „Dříve zde“ uvedeno, které kočky tam bývaly. Za zmínku stojí levhart cejlonský a kočky rybářské ze {BRN} (odešly v roce 2025), poslední kočka divoká v {OLO} (uhynula v červenci 2025), gepard ze Zooparku Zvole a kočky cirkusů, které skončily (Cirkus Aleš, Cirkus Sultán). Zabavené kočky často odcházely přes {LIB} do záchranného centra FELIDA v Nizozemsku.</p>"""},
 "controle": {
  "nl": """<p class="prose"><strong>Officiële lijsten:</strong> de lijst van dierentuinen met licentie van het ministerie van Milieu (27-03-2025), de ledenlijsten van UCSZOO en EAZA (oktober 2026) en de wet over dierentuinen (162/2003 Sb.).</p>
  <p class="prose"><strong>Databanken:</strong> Zootierliste (alle katachtigen, huidige en vroegere houdingen), alleen aanvullend.</p>
  <p class="prose"><strong>Websites en jaarverslagen van de parken</strong>, met dierenlijsten, soortpagina’s, plattegronden en nieuws.</p>
  <p class="prose"><strong>Nieuws:</strong> onder meer iROZHLAS (ČRo), ČT24, iDNES, Novinky, Deník en regionale nieuwssites.</p>""",
  "en": """<p class="prose"><strong>Official lists:</strong> the Ministry of the Environment list of licensed zoos (27-03-2025), the member lists of UCSZOO and EAZA (October 2026) and the Zoos Act (162/2003 Sb.).</p>
  <p class="prose"><strong>Databases:</strong> Zootierliste (all cats, current and former holdings), used only as a supplement.</p>
  <p class="prose"><strong>Park websites and annual reports</strong>, with animal lists, species pages, maps and news.</p>
  <p class="prose"><strong>News:</strong> including iROZHLAS (ČRo), ČT24, iDNES, Novinky, Deník and regional news sites.</p>""",
  "cs": """<p class="prose"><strong>Oficiální seznamy:</strong> seznam licencovaných zoo Ministerstva životního prostředí (27. 3. 2025), členské seznamy UCSZOO a EAZA (říjen 2026) a zákon o zoologických zahradách (162/2003 Sb.).</p>
  <p class="prose"><strong>Databáze:</strong> Zootierliste (všechny kočkovité šelmy, současné i dřívější chovy), jen jako doplněk.</p>
  <p class="prose"><strong>Weby a výroční zprávy parků</strong> s přehledy zvířat, stránkami druhů, plánky a novinkami.</p>
  <p class="prose"><strong>Zprávy:</strong> mimo jiné iROZHLAS (ČRo), ČT24, iDNES, Novinky, Deník a regionální zpravodajské weby.</p>"""},
}
