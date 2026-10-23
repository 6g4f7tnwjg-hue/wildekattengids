# Landspecifieke tekstblokken van de Poolse gids (NL / EN / PL). Stand 23 oktober 2026.
import re, unicodedata
def _slug(x):
    x = x.replace("ł", "l").replace("Ł", "L")
    x = "".join(c for c in unicodedata.normalize("NFD", x) if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"\(.*?\)", "", x)).strip("-")
def L(naam): return f'<a href="#locatie/{_slug(naam)}">{naam}</a>'

# alleen woiwodschappen met locaties, ruwweg van noord naar zuid
REGN = {"pomorskie": ["Pommeren", "Pomerania", "Pomorskie"],
        "zachodniopomorskie": ["West-Pommeren", "West Pomerania", "Zachodniopomorskie"],
        "kujawsko-pomorskie": ["Koejavië-Pommeren", "Kuyavia-Pomerania", "Kujawsko-pomorskie"],
        "podlaskie": ["Podlachië", "Podlaskie", "Podlaskie"],
        "wielkopolskie": ["Groot-Polen", "Greater Poland", "Wielkopolskie"],
        "mazowieckie": ["Mazovië", "Masovia", "Mazowieckie"],
        "lodzkie": ["Łódź", "Łódź", "Łódzkie"],
        "dolnoslaskie": ["Neder-Silezië", "Lower Silesia", "Dolnośląskie"],
        "opolskie": ["Opole", "Opole", "Opolskie"],
        "swietokrzyskie": ["Święty Krzyż", "Holy Cross", "Świętokrzyskie"],
        "lubelskie": ["Lublin", "Lublin", "Lubelskie"],
        "slaskie": ["Silezië", "Silesia", "Śląskie"],
        "malopolskie": ["Klein-Polen", "Lesser Poland", "Małopolskie"]}

KRA, CHO, WRO, ROM, TOR = L("Zoo Kraków"), L("Śląski Ogród Zoologiczny"), L("Zoo Wrocław"), L("Zoo Romanówka"), L("Zoo Toruń")
OPO, WAR, LOD, PLO, GDA, BOR = L("Zoo Opole"), L("Zoo Warszawa"), L("Orientarium Zoo Łódź"), L("Zoo Płock"), L("Zoo Gdańsk"), L("Zoo Borysew")
POZ, LAC, CZC, LUB, BYD = L("Nowe Zoo Poznań"), L("Zoo Łączna"), L("Particuliere houder Czchów"), L("Zoo Lubin"), L("Zoo Bydgoszcz")

# losse vervangingen in het sjabloon (resten van Portugal in de Poolse vaste teksten)
PL_VERV = [("w Portugalii", "w Polsce"), ("W Portugalii", "W Polsce"), ("portugalskie ogrody zoologiczne", "polskie ogrody zoologiczne")]
VAST = [
 (r'<p class="stamp">.*?</p>', '<p class="stamp"><span class="l-nl">Stand 23 oktober 2026</span><span class="l-en">Updated 23 October 2026</span><span class="l-pl">Aktualizacja 23 października 2026</span></p>'),
 (r'<p class="lede">.*?</p>', '<p class="lede">'
  '<span class="l-nl">Waar in Polen kun je tijgers, sneeuwluipaarden, nevelpanters, manoels en andere wilde katten zien? Per soort en per park zie je hier welke katten er wonen, welke jongen er onlangs geboren zijn en wat er binnenkort verandert. En met welke route je alle soorten ziet.</span>'
  '<span class="l-en">Where in Poland can you see tigers, snow leopards, clouded leopards, Pallas’s cats and other wild cats? By species and by park, this guide shows which cats live where, which young were born recently and what is about to change. And which route lets you see every species.</span>'
  '<span class="l-pl">Gdzie w Polsce zobaczysz tygrysy, irbisy, pantery mgliste, manule i inne dzikie koty? Przewodnik pokazuje według gatunków i parków, które koty gdzie mieszkają, jakie młode niedawno się urodziły i co wkrótce się zmieni. I jaką trasą zobaczysz wszystkie gatunki.</span></p>'),
]

LOC_INTRO = ["Alle dierentuinen, dierenparken, particuliere houders en opvangcentra in Polen waar wilde katten wonen. Tik op een stip om te zien welke katten er wonen.",
             "All zoos, animal parks, private keepers and rescue centres in Poland where wild cats live. Tap a dot to see which cats live there.",
             "Wszystkie ogrody zoologiczne, parki zwierząt, prywatni hodowcy i ośrodki ratunkowe w Polsce, w których mieszkają dzikie koty. Kliknij kropkę, aby zobaczyć, jakie koty tam mieszkają."]

def tldr():
    nl = f'''<div class="l-nl">
<div class="prose">
  <ul>
    <li><strong>21 soorten bevestigd</strong> op 28 locaties: 13 dierentuinen (lid van EAZA of de Poolse dierentuinvereniging RDPOZiA), 7 andere vergunde dierenparken, 5 particuliere minizoo’s, 1 opvang, 1 lynxcentrum en het wisentreservaat van Białowieża.</li>
    <li><strong>{KRA}</strong> heeft 11 soorten, {OPO} 10 en {ROM}, {WRO} en {CHO} elk 8.</li>
    <li><strong>Maar op één plek te zien:</strong> de nevelpanter ({WRO}), de rode lynx, de jaguarundi en de Amoer-luipaardkat ({ROM}) en de vissende kat ({TOR}).</li>
    <li><strong>Jonge katten:</strong> drie sneeuwluipaarden in {WAR} (juli 2026), leeuwen in {LOD} (juli 2026), Amoertijgers in {OPO} (2025) en {PLO} (2025), zandkatten in {GDA} en lynxen in {CHO} (2026).</li>
    <li><strong>Particulieren en circussen:</strong> sinds eind 2021 mogen particulieren en circussen geen grote katten, cheetahs of poema’s meer houden; dieren die er al waren mogen blijven. Servals en (met vergunning) lynxen en caracals zie je ook in particuliere minizoo’s. Circussen met katten zijn in 2025–2026 niet gevonden.</li>
    <li><strong>Witte leeuwen, witte tijgers en zwarte panters</strong> zie je in {BOR}.</li>
  </ul>
  </div>
</div>'''
    en = f'''<div class="l-en">
<div class="prose">
  <ul>
    <li><strong>21 species confirmed</strong> at 28 locations: 13 zoos (members of EAZA or the Polish zoo association RDPOZiA), 7 other licensed animal parks, 5 private mini zoos, 1 rescue centre, 1 lynx centre and the bison reserve of Białowieża.</li>
    <li><strong>{KRA}</strong> has 11 species, {OPO} 10 and {ROM}, {WRO} and {CHO} 8 each.</li>
    <li><strong>Only in one place:</strong> the clouded leopard ({WRO}), the bobcat, the jaguarundi and the Amur leopard cat ({ROM}) and the fishing cat ({TOR}).</li>
    <li><strong>Young cats:</strong> three snow leopards at {WAR} (July 2026), lions at {LOD} (July 2026), Amur tigers at {OPO} (2025) and {PLO} (2025), sand cats at {GDA} and lynxes at {CHO} (2026).</li>
    <li><strong>Private keepers and circuses:</strong> since late 2021 private keepers and circuses may no longer keep big cats, cheetahs or pumas; animals already there may stay. Servals and (with a permit) lynxes and caracals can also be seen in private mini zoos. No circuses with cats were found in 2025–2026.</li>
    <li><strong>White lions, white tigers and black panthers</strong> can be seen at {BOR}.</li>
  </ul>
  </div>
</div>'''
    pl = f'''<div class="l-pl">
<div class="prose">
  <ul>
    <li><strong>21 gatunków potwierdzonych</strong> w 28 miejscach: 13 ogrodów zoologicznych (członkowie EAZA lub RDPOZiA), 7 innych licencjonowanych parków zwierząt, 5 prywatnych minizoo, 1 ośrodek ratunkowy, 1 ośrodek rysi i rezerwat żubrów w Białowieży.</li>
    <li><strong>{KRA}</strong> ma 11 gatunków, {OPO} 10, a {ROM}, {WRO} i {CHO} po 8.</li>
    <li><strong>Tylko w jednym miejscu:</strong> pantera mglista ({WRO}), ryś rudy, jaguarundi i kot amurski ({ROM}) oraz kot rybołów ({TOR}).</li>
    <li><strong>Młode:</strong> trzy irbisy w {WAR} (lipiec 2026), lwy w {LOD} (lipiec 2026), tygrysy amurskie w {OPO} (2025) i {PLO} (2025), koty pustynne w {GDA} i rysie w {CHO} (2026).</li>
    <li><strong>Prywatni hodowcy i cyrki:</strong> od końca 2021 roku prywatne osoby i cyrki nie mogą już trzymać dużych kotów, gepardów ani pum; zwierzęta, które już tam były, mogą zostać. Serwale oraz (za zezwoleniem) rysie i karakale zobaczysz też w prywatnych minizoo. W latach 2025–2026 nie znaleziono cyrków z kotami.</li>
    <li><strong>Białe lwy, białe tygrysy i czarne pantery</strong> zobaczysz w {BOR}.</li>
  </ul>
  </div>
</div>'''
    return nl + en + pl + "\n"

GEEN = [
 [("Vergunde dierentuinen zonder katachtigen", "Licensed zoos without cats", "Licencjonowane ogrody zoologiczne bez kotów"),
  "Akwarium Gdyńskie, Zoo Sosnowiec, Dolina Charlotty (Słupsk), Stare Zoo Poznań, Park Dzikich Zwierząt Kadzidłowo (lynx en wilde kat alleen tot 2020)",
  ["Akwarium Gdyńskie, Zoo Sosnowiec, Dolina Charlotty (Słupsk), Stare Zoo Poznań, Park Dzikich Zwierząt Kadzidłowo (lynx and wildcat only until 2020)",
   "Akwarium Gdyńskie, Zoo Sosnowiec, Dolina Charlotty (Słupsk), Stare Zoo Poznań, Park Dzikich Zwierząt Kadzidłowo (ryś i żbik tylko do 2020)"]],
 [("Gesloten of zonder katten meer", "Closed or no cats any more", "Zamknięte lub już bez kotów"),
  "Zoo Safari Świerkocin (dicht sinds 2017), Lemur Park Rumia en Zoo-Egzotyczne Kaszuby (lijken dicht), MiniZooPark Walim (serval niet meer bevestigd), Mazurskie Mini Zoo Kąp, MiniZoo Mantadia (Łódź) en Dobronianka (servals tot 2023)",
  ["Zoo Safari Świerkocin (closed since 2017), Lemur Park Rumia and Zoo-Egzotyczne Kaszuby (appear closed), MiniZooPark Walim (serval no longer confirmed), Mazurskie Mini Zoo Kąp, MiniZoo Mantadia (Łódź) and Dobronianka (servals until 2023)",
   "Zoo Safari Świerkocin (zamknięte od 2017), Lemur Park Rumia i Zoo-Egzotyczne Kaszuby (prawdopodobnie zamknięte), MiniZooPark Walim (serwal niepotwierdzony), Mazurskie Mini Zoo Kąp, MiniZoo Mantadia (Łódź) i Dobronianka (serwale do 2023)"]],
 [("Circussen zonder katten", "Circuses without cats", "Cyrki bez kotów"),
  "Cyrk Zalewski, Cyrk Korona, Cyrk Arlekin, Cyrk Arena; sinds december 2021 mogen circussen geen grote katten meer houden",
  ["Cyrk Zalewski, Cyrk Korona, Cyrk Arlekin, Cyrk Arena; since December 2021 circuses may no longer keep big cats",
   "Cyrk Zalewski, Cyrk Korona, Cyrk Arlekin, Cyrk Arena; od grudnia 2021 cyrki nie mogą trzymać dużych kotów"]],
 [("Andere parken, opvang en minizoo’s zonder katachtigen", "Other parks, rescue centres and mini zoos without cats", "Inne parki, ośrodki i minizoo bez kotów"),
  "Mini Zoo Śrem, Zwierzyniec Bałtowski, opvang Mysikrólik (Bielsko-Biała), Bieszczady-opvangpark Olchowiec (gestopt in 2026) en andere minizoo’s; zie de bronnen per woiwodschap",
  ["Mini Zoo Śrem, Zwierzyniec Bałtowski, Mysikrólik rescue centre (Bielsko-Biała), Olchowiec rescue park in the Bieszczady (closed in 2026) and other mini zoos",
   "Mini Zoo Śrem, Zwierzyniec Bałtowski, ośrodek Mysikrólik (Bielsko-Biała), ośrodek w Olchowcu w Bieszczadach (zamknięty w 2026) i inne minizoo"]],
]
def geen(i):
    out = ""
    for row in GEEN:
        k, t, tr = row
        if i and tr: t = tr[i - 1]
        out += f"    <li><b>{k[i]}:</b> {t}</li>\n"
    return out

OFFICIEEL = [
 """<p>In Polen heeft elke dierentuin een vergunning van de Generalny Dyrektor Ochrony Środowiska (GDOŚ, landelijke milieudienst) nodig. De lijst op de site van GDOŚ (ongedateerd, gezien op 23-10-2026) telt 25 dierentuinen; 20 daarvan hebben wilde katten.</p>
    <p>Grote katten, cheetahs, poema’s en jaguarundi’s staan op de lijst van gevaarlijke dieren (categorie I): particulieren mogen ze niet houden, en sinds 18 december 2021 geldt dat ook voor circussen. Dieren die toen al bij een circus of particulier waren, moesten worden gemeld en mogen blijven. Lynxen, caracals en goudkatten (categorie II) mogen alleen met een vergunning van de regionale milieudienst. De serval staat niet op de lijst; daarom zie je servals ook in kleine particuliere minizoo’s.</p>
    <p>De lijst in deze gids is opgebouwd uit de GDOŚ-lijst, de ledenlijsten van EAZA (12 Poolse dierentuinen) en RDPOZiA (18 leden), Zootierliste (alle katachtigen, huidige en vroegere houders) en een zoektocht per woiwodschap naar minizoo’s, particulieren, opvang en circussen.</p>
    <p>Of een park in deze gids een dierentuin heet, hangt af van het lidmaatschap van EAZA of RDPOZiA. Andere parken met een dierentuinvergunning heten dierenpark, minizoo’s zonder vergunning particuliere houder.</p>
""",
 """<p>In Poland every zoo needs a permit from the General Director for Environmental Protection (GDOŚ). The list on the GDOŚ website (undated, seen 23-10-2026) has 25 zoos; 20 of them keep wild cats.</p>
    <p>Big cats, cheetahs, pumas and jaguarundis are on the list of dangerous animals (category I): private individuals may not keep them, and since 18 December 2021 this also applies to circuses. Animals already kept by a circus or private keeper had to be registered and may stay. Lynxes, caracals and golden cats (category II) are only allowed with a permit from the regional environment directorate. The serval is not on the list, which is why servals can also be seen in small private mini zoos.</p>
    <p>The list in this guide was built from the GDOŚ list, the member lists of EAZA (12 Polish zoos) and RDPOZiA (18 members), Zootierliste (all cats, current and former holders) and a search voivodeship by voivodeship for mini zoos, private keepers, rescue centres and circuses.</p>
    <p>Whether a park is called a zoo in this guide depends on membership of EAZA or RDPOZiA. Other parks with a zoo licence are called animal parks, mini zoos without a licence private keepers.</p>
""",
 """<p>W Polsce każdy ogród zoologiczny potrzebuje zezwolenia Generalnego Dyrektora Ochrony Środowiska (GDOŚ). Wykaz na stronie GDOŚ (bez daty, sprawdzony 23-10-2026) obejmuje 25 ogrodów zoologicznych; w 20 z nich są dzikie koty.</p>
    <p>Duże koty, gepardy, pumy i jaguarundi znajdują się na liście gatunków niebezpiecznych (kategoria I): osoby prywatne nie mogą ich trzymać, a od 18 grudnia 2021 dotyczy to także cyrków. Zwierzęta, które już były w cyrku lub u prywatnej osoby, trzeba było zgłosić i mogą zostać. Rysie, karakale i złotki (kategoria II) są dozwolone tylko za zezwoleniem regionalnego dyrektora ochrony środowiska. Serwala nie ma na liście, dlatego serwale zobaczysz też w małych prywatnych minizoo.</p>
    <p>Lista w przewodniku powstała na podstawie wykazu GDOŚ, list członków EAZA (12 polskich ogrodów) i RDPOZiA (18 członków), bazy Zootierliste (wszystkie koty, obecni i dawni hodowcy) oraz wyszukiwania województwo po województwie: minizoo, prywatni hodowcy, ośrodki i cyrki.</p>
    <p>To, czy park nazywamy w przewodniku ogrodem zoologicznym, zależy od członkostwa w EAZA lub RDPOZiA. Inne parki z licencją ogrodu zoologicznego to parki zwierząt, a minizoo bez licencji to prywatni hodowcy.</p>
"""]

ADVIES = [
 f"""<ul class="prose">
    <li><strong>Alle 21 soorten in vijf parken:</strong>
      <ul>
        <li><strong>Zoo Kraków</strong>: jaguar, ocelot, zandkat, Geoffroy’s kat, Noord-Chinese luipaard, manoel, serval (en tijger, leeuw, sneeuwluipaard, lynx)</li>
        <li><strong>Śląski Ogród Zoologiczny</strong> (Chorzów): cheetah (en poema, caracal, lynx)</li>
        <li><strong>Zoo Wrocław</strong>: nevelpanter, roestkat, Europese wilde kat (en Sumatraanse tijger, sneeuwluipaard, manoel)</li>
        <li><strong>Zoo Romanówka</strong> (bij Lublin): rode lynx, jaguarundi, Amoer-luipaardkat, poema, caracal</li>
        <li><strong>Zoo Toruń</strong>: vissende kat (en lynx)</li>
      </ul>
    </li>
    <li><strong>Alternatieven:</strong> {OPO} heeft 10 soorten, waaronder jaguar, ocelot, cheetah en serval. In Warschau: {WAR} met sneeuwluipaard, Amoerluipaard, cheetah en manoel. {CHO} en {KRA} liggen maar een uur rijden uit elkaar.</li>
    <li><strong>Particuliere minizoo’s</strong> zijn vaak alleen op afspraak of in het seizoen open; kijk vóór je bezoek op hun site.</li>
    <li><strong>Twijfel je over een dier?</strong> Bel of mail dan vóór je bezoek met het park. Alle onzekere vermeldingen staan onder “Over” bij “Twijfelgevallen”.</li>
  </ul>
""",
 f"""<ul class="prose">
    <li><strong>All 21 species in five parks:</strong>
      <ul>
        <li><strong>Zoo Kraków</strong>: jaguar, ocelot, sand cat, Geoffroy’s cat, North Chinese leopard, Pallas’s cat, serval (and tiger, lion, snow leopard, lynx)</li>
        <li><strong>Śląski Ogród Zoologiczny</strong> (Chorzów): cheetah (and puma, caracal, lynx)</li>
        <li><strong>Zoo Wrocław</strong>: clouded leopard, rusty-spotted cat, European wildcat (and Sumatran tiger, snow leopard, Pallas’s cat)</li>
        <li><strong>Zoo Romanówka</strong> (near Lublin): bobcat, jaguarundi, Amur leopard cat, puma, caracal</li>
        <li><strong>Zoo Toruń</strong>: fishing cat (and lynx)</li>
      </ul>
    </li>
    <li><strong>Alternatives:</strong> {OPO} has 10 species, including jaguar, ocelot, cheetah and serval. In Warsaw: {WAR} with snow leopard, Amur leopard, cheetah and Pallas’s cat. {CHO} and {KRA} are only an hour’s drive apart.</li>
    <li><strong>Private mini zoos</strong> are often only open by appointment or in season; check their website before you go.</li>
    <li><strong>Not sure about an animal?</strong> Call or email the park before your visit. All uncertain entries are listed under “About” in “Doubtful cases”.</li>
  </ul>
""",
 f"""<ul class="prose">
    <li><strong>Wszystkie 21 gatunków w pięciu parkach:</strong>
      <ul>
        <li><strong>Zoo Kraków</strong>: jaguar, ocelot, kot pustynny, kot Geoffroya, lampart północnochiński, manul, serwal (oraz tygrys, lew, irbis, ryś)</li>
        <li><strong>Śląski Ogród Zoologiczny</strong> (Chorzów): gepard (oraz puma, karakal, ryś)</li>
        <li><strong>Zoo Wrocław</strong>: pantera mglista, kot cejloński, żbik (oraz tygrys sumatrzański, irbis, manul)</li>
        <li><strong>Zoo Romanówka</strong> (koło Lublina): ryś rudy, jaguarundi, kot amurski, puma, karakal</li>
        <li><strong>Zoo Toruń</strong>: kot rybołów (oraz ryś)</li>
      </ul>
    </li>
    <li><strong>Alternatywy:</strong> {OPO} ma 10 gatunków, m.in. jaguara, ocelota, geparda i serwala. W Warszawie: {WAR} z irbisem, lampartem amurskim, gepardem i manulem. {CHO} i {KRA} dzieli tylko godzina jazdy.</li>
    <li><strong>Prywatne minizoo</strong> są często otwarte tylko po umówieniu się albo w sezonie; sprawdź ich stronę przed wizytą.</li>
    <li><strong>Nie masz pewności co do zwierzęcia?</strong> Zadzwoń albo napisz do parku przed wizytą. Wszystkie niepewne wpisy znajdziesz w części „O przewodniku” w „Przypadkach wątpliwych”.</li>
  </ul>
"""]

GEPLAND = [
 f"""<ul class="prose">
    <li><span class="st st-p"><i></i></span> <strong>{LUB}:</strong> er komt een lynxverblijf (aangekondigd voor 2026).</li>
    <li><strong>{LAC}:</strong> op 13 oktober 2026 nam justitie dieren in beslag; de Bengaalse tijger ging naar Nederland. Het park is dicht; de vergunning wordt mogelijk ingetrokken.</li>
    <li><strong>{BYD}:</strong> in het najaar van 2026 opent een nieuw lynxverblijf.</li>
    <li><span class="st st-w"><i></i></span> <strong>Niet te bezoeken:</strong> {CZC} (twee leeuwen en een tijger bij een particulier; rechtszaak loopt).</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Gepland</span> · <span class="st st-w"><i></i>Onzeker</span></p>
""",
 f"""<ul class="prose">
    <li><span class="st st-p"><i></i></span> <strong>{LUB}:</strong> a lynx enclosure is coming (announced for 2026).</li>
    <li><strong>{LAC}:</strong> on 13 October 2026 prosecutors seized animals; the Bengal tiger went to the Netherlands. The park is closed and may lose its licence.</li>
    <li><strong>{BYD}:</strong> a new lynx enclosure opens in autumn 2026.</li>
    <li><span class="st st-w"><i></i></span> <strong>Not open to visitors:</strong> {CZC} (two lions and a tiger with a private keeper; court case ongoing).</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Planned</span> · <span class="st st-w"><i></i>Uncertain</span></p>
""",
 f"""<ul class="prose">
    <li><span class="st st-p"><i></i></span> <strong>{LUB}:</strong> powstaje wybieg dla rysi (zapowiedziany na 2026).</li>
    <li><strong>{LAC}:</strong> 13 października 2026 prokuratura zabezpieczyła zwierzęta; tygrys bengalski trafił do Holandii. Park jest zamknięty i może stracić zezwolenie.</li>
    <li><strong>{BYD}:</strong> jesienią 2026 otwiera się nowy wybieg dla rysi.</li>
    <li><span class="st st-w"><i></i></span> <strong>Niedostępne dla zwiedzających:</strong> {CZC} (dwa lwy i tygrys u prywatnego hodowcy; trwa proces).</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Planowane</span> · <span class="st st-w"><i></i>Niepewne</span></p>
"""]

def _kv(lg, titel, sp, naar, locs):
    return f'<h3>{titel} <a class="kv-sp" href="#soort/{sp}">{naar}</a></h3>\n  <ul class="prose">\n' + "".join(f"    <li>{x}</li>\n" for x in locs) + "  </ul>\n"
KV = [
 (("Witte tijger", "naar de tijger"), ("White tiger", "to the tiger"), ("Biały tygrys", "do tygrysa"), "tijger", [BOR]),
 (("Witte leeuw", "naar de leeuw"), ("White lion", "to the lion"), ("Biały lew", "do lwa"), "leeuw", [BOR]),
 (("Zwarte panter", "naar de luipaard"), ("Black panther", "to the leopard"), ("Czarna pantera", "do lamparta"), "luipaard", [BOR]),
]
KVTXT = {"nl": f"Een witte tijger heeft een recessieve mutatie in het gen SLC45A2 en is geen albino; binnen het Europese fokprogramma worden ze niet meer gefokt. Witte leeuwen hebben leucisme, zwarte panters melanisme. In {BOR} kregen de zwarte luipaarden in juli 2025 twee jongen. De witte leeuw Tabo van {ROM} stierf in maart 2026; {KRA} had in 2016–2017 zwarte jaguars.",
         "en": f"A white tiger has a recessive mutation in the SLC45A2 gene and is not an albino; they are no longer bred within the European breeding programme. White lions have leucism, black panthers melanism. At {BOR} the black leopards had two cubs in July 2025. The white lion Tabo at {ROM} died in March 2026; {KRA} had black jaguars in 2016–2017.",
         "pl": f"Biały tygrys ma recesywną mutację genu SLC45A2 i nie jest albinosem; w europejskim programie hodowlanym nie rozmnaża się ich już. Białe lwy mają leucyzm, czarne pantery melanizm. W {BOR} czarne lamparty miały w lipcu 2025 dwoje młodych. Biały lew Tabo z {ROM} padł w marcu 2026; {KRA} miał czarne jaguary w latach 2016–2017."}
HYB = {"nl": "Er zijn geen lijgers, tigons of andere hybriden van wilde katten gevonden. Savannah- en bengaalkatten (kruisingen met huiskatten) tellen in deze gids niet mee.",
       "en": "No ligers, tigons or other hybrids of wild cats were found. Savannah and Bengal cats (crosses with domestic cats) do not count in this guide.",
       "pl": "Nie znaleziono ligrów, tigonów ani innych mieszańców dzikich kotów. Koty savannah i bengalskie rasy domowej (krzyżówki z kotem domowym) nie są ujęte w przewodniku."}
def _kleur():
    out = ""
    for i, lg in enumerate(["nl", "en", "pl"]):
        out += f'<div class="l-{lg}">\n' + "".join(_kv(lg, k[i][0], k[3], k[i][1], k[4]) for k in KV) + f'  <p class="prose">{KVTXT[lg]}</p>\n</div>'
    out += '<h3 id="hybriden" style="font-size:22px;margin-top:30px"><span class="l-nl">Hybriden</span><span class="l-en">Hybrids</span><span class="l-pl">Mieszańce</span></h3>\n'
    for lg in ["nl", "en", "pl"]:
        out += f'<div class="l-{lg}">\n<p class="prose">{HYB[lg]}</p>\n</div>'
    return out
KLEUR = _kleur()

UITLEG = {
 "werkwijze": {
  "nl": """<p class="prose">Voor alle Poolse dierentuinen, dierenparken, minizoo’s, particulieren, opvangcentra en circussen is nagegaan welke wilde katachtigen er te zien zijn. De basislijst komt uit de lijst van GDOŚ (25 dierentuinen), de ledenlijsten van EAZA en RDPOZiA en Zootierliste (alle katachtigen, huidige en vroegere houders); per woiwodschap is daarna gezocht naar kleinere parken, particulieren, opvang en circussen. Elke locatie is gecontroleerd op de eigen website, aangevuld met Pools nieuws. Bij elke vermelding staan de bron en de datum.</p>
  <p class="prose">Een kat telt mee als een bezoeker hem kan zien, ook als dat alleen op afspraak kan. Particulieren staan erin met een kanttekening; locaties die niet te bezoeken zijn, staan erin met de status “niet open voor publiek” en tellen niet als bevestigd. Namen van particuliere houders staan niet in de gids.</p>
  <p class="prose">De indeling in soorten volgt de standaard van de IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>""",
  "en": """<p class="prose">For all Polish zoos, animal parks, mini zoos, private keepers, rescue centres and circuses, we checked which wild cats can be seen. The base list comes from the GDOŚ list (25 zoos), the member lists of EAZA and RDPOZiA and Zootierliste (all cats, current and former holders); each voivodeship was then searched for smaller parks, private keepers, rescue centres and circuses. Every location was checked on its own website, supplemented by Polish news. Each entry shows its source and date.</p>
  <p class="prose">A cat counts if a visitor can see it, even if only by appointment. Private keepers are included with a note; locations that cannot be visited are listed as “not open to the public” and do not count as confirmed. Names of private keepers are not given.</p>
  <p class="prose">Species follow the standard of the IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>""",
  "pl": """<p class="prose">Sprawdziliśmy wszystkie polskie ogrody zoologiczne, parki zwierząt, minizoo, prywatnych hodowców, ośrodki i cyrki pod kątem tego, jakie dzikie koty można w nich zobaczyć. Podstawą jest wykaz GDOŚ (25 ogrodów), listy członków EAZA i RDPOZiA oraz Zootierliste (wszystkie koty, obecni i dawni hodowcy); potem szukaliśmy w każdym województwie mniejszych parków, prywatnych hodowców, ośrodków i cyrków. Każde miejsce sprawdziliśmy na jego stronie internetowej i w polskich mediach. Przy każdym wpisie podajemy źródło i datę.</p>
  <p class="prose">Kot jest liczony, jeśli zwiedzający może go zobaczyć, nawet tylko po umówieniu się. Prywatni hodowcy są ujęci z adnotacją; miejsca, których nie można odwiedzić, mają status „niedostępne dla zwiedzających” i nie liczą się jako potwierdzone. Nie podajemy nazwisk prywatnych hodowców.</p>
  <p class="prose">Podział na gatunki opiera się na standardzie IUCN/SSC Cat Classification Task Force (Kitchener i in., 2017, <i>Cat News</i> Special Issue 11).</p>"""},
 "namen": {
  "nl": """<ul class="prose">
    <li><strong>Ryś</strong> is de Euraziatische lynx, <strong>irbis</strong> de sneeuwluipaard, <strong>pantera mglista</strong> de nevelpanter, <strong>manul</strong> de manoel en <strong>żbik</strong> de Europese wilde kat.</li>
    <li><strong>Kot amurski</strong> is de Amoer-luipaardkat, een ondersoort van de Bengaalse kat (<i>Prionailurus bengalensis euptilura</i>), niet het huiskatras Bengaal. <strong>Kot cejloński</strong> is de roestkat, <strong>kot rybołów</strong> de vissende kat.</li>
    <li><strong>Leeuw:</strong> sinds 2017 zijn er twee ondersoorten: de noordelijke leeuw (<i>P. l. leo</i>), waartoe de Aziatische leeuwen van Łódź en Kraków horen, en de zuidelijke leeuw (<i>P. l. melanochaita</i>), waartoe de Angolese leeuwen horen. De Noord-Chinese luipaard hoort bij de Amoerpanter (<i>P. p. orientalis</i>).</li>
  </ul>""",
  "en": """<ul class="prose">
    <li><strong>Ryś</strong> is the Eurasian lynx, <strong>irbis</strong> the snow leopard, <strong>pantera mglista</strong> the clouded leopard, <strong>manul</strong> the Pallas’s cat and <strong>żbik</strong> the European wildcat.</li>
    <li><strong>Kot amurski</strong> is the Amur leopard cat, a subspecies of the leopard cat (<i>Prionailurus bengalensis euptilura</i>), not the domestic Bengal breed. <strong>Kot cejloński</strong> is the rusty-spotted cat, <strong>kot rybołów</strong> the fishing cat.</li>
    <li><strong>Lion:</strong> since 2017 there are two subspecies: the northern lion (<i>P. l. leo</i>), which includes the Asiatic lions of Łódź and Kraków, and the southern lion (<i>P. l. melanochaita</i>), which includes the Angolan lions. The North Chinese leopard belongs to the Amur leopard (<i>P. p. orientalis</i>).</li>
  </ul>""",
  "pl": """<ul class="prose">
    <li>Przewodnik jest napisany po niderlandzku; polskie nazwy gatunków są na stronach gatunków. <strong>Kot amurski</strong> to podgatunek kota bengalskiego (<i>Prionailurus bengalensis euptilura</i>), a nie rasa domowa bengal.</li>
    <li><strong>Lew:</strong> od 2017 roku wyróżnia się dwa podgatunki: lwa północnego (<i>P. l. leo</i>), do którego należą lwy azjatyckie z Łodzi i Krakowa, oraz lwa południowego (<i>P. l. melanochaita</i>), do którego należą lwy angolskie. Lampart północnochiński należy do lamparta amurskiego (<i>P. p. orientalis</i>).</li>
  </ul>"""},
 "verdwenen": {
  "nl": f"""<p class="prose">Bij elk park staat onder “Eerder hier” welke katten er vroeger waren. Opvallend: de Bengaalse tijger van {LAC} (in oktober 2026 in beslag genomen, nu in Nederland), de witte leeuw Tabo van {ROM} (overleden maart 2026), de serval van {CHO} (2025 naar Tsjechië) en de jaguarundi en wilde kat van {KRA}. Zoo Safari Świerkocin is sinds 2017 dicht.</p>""",
  "en": f"""<p class="prose">Each park’s page lists under “Previously here” which cats it used to have. Notable: the Bengal tiger of {LAC} (seized in October 2026, now in the Netherlands), the white lion Tabo of {ROM} (died March 2026), the serval of {CHO} (moved to Czechia in 2025) and the jaguarundi and wildcat of {KRA}. Zoo Safari Świerkocin has been closed since 2017.</p>""",
  "pl": f"""<p class="prose">Na stronie każdego parku w części „Wcześniej tutaj” podajemy, jakie koty tam były. Warto wspomnieć: tygrys bengalski z {LAC} (zabezpieczony w październiku 2026, obecnie w Holandii), biały lew Tabo z {ROM} (padł w marcu 2026), serwal z {CHO} (w 2025 trafił do Czech) oraz jaguarundi i żbik z {KRA}. Zoo Safari Świerkocin jest zamknięte od 2017 roku.</p>"""},
 "controle": {
  "nl": """<p class="prose"><strong>Officiële lijsten:</strong> de lijst van dierentuinen van GDOŚ (gezien 23-10-2026), de ledenlijsten van EAZA (oktober 2026) en RDPOZiA, de natuurbeschermingswet (art. 73, Dz.U. 2026 poz. 1315) en de lijst van gevaarlijke soorten (Dz.U. 2011 nr 173 poz. 1037).</p>
  <p class="prose"><strong>Databanken:</strong> Zootierliste (alle katachtigen, huidige en vroegere houdingen), alleen aanvullend.</p>
  <p class="prose"><strong>Websites van de parken</strong>, met dierenlijsten, soortpagina’s, parkkaarten en nieuws.</p>
  <p class="prose"><strong>Nieuws:</strong> onder meer TVN24, Onet, Gazeta Wyborcza, Radio Kraków, TVP3 en regionale kranten.</p>""",
  "en": """<p class="prose"><strong>Official lists:</strong> the GDOŚ list of zoos (seen 23-10-2026), the member lists of EAZA (October 2026) and RDPOZiA, the Nature Conservation Act (art. 73, Dz.U. 2026 item 1315) and the list of dangerous species (Dz.U. 2011 no. 173 item 1037).</p>
  <p class="prose"><strong>Databases:</strong> Zootierliste (all cats, current and former holdings), used only as a supplement.</p>
  <p class="prose"><strong>Park websites</strong>, with animal lists, species pages, park maps and news.</p>
  <p class="prose"><strong>News:</strong> including TVN24, Onet, Gazeta Wyborcza, Radio Kraków, TVP3 and regional newspapers.</p>""",
  "pl": """<p class="prose"><strong>Oficjalne wykazy:</strong> wykaz ogrodów zoologicznych GDOŚ (sprawdzony 23-10-2026), listy członków EAZA (październik 2026) i RDPOZiA, ustawa o ochronie przyrody (art. 73, Dz.U. 2026 poz. 1315) i lista gatunków niebezpiecznych (Dz.U. 2011 nr 173 poz. 1037).</p>
  <p class="prose"><strong>Bazy danych:</strong> Zootierliste (wszystkie koty, obecne i dawne hodowle), tylko jako uzupełnienie.</p>
  <p class="prose"><strong>Strony parków</strong> z listami zwierząt, stronami gatunków, mapami i aktualnościami.</p>
  <p class="prose"><strong>Media:</strong> m.in. TVN24, Onet, Gazeta Wyborcza, Radio Kraków, TVP3 i gazety regionalne.</p>"""},
}
