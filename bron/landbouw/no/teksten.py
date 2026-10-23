# Landspecifieke tekstblokken van de Noorse gids (NL / EN / NB). Stand 23 oktober 2026.
import re, unicodedata
def _slug(x):
    x = x.replace("æ", "ae").replace("ø", "oe").replace("Æ", "Ae").replace("Ø", "Oe")
    x = "".join(c for c in unicodedata.normalize("NFD", x) if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"\(.*?\)", "", x)).strip("-")
def L(naam): return f'<a href="#locatie/{_slug(naam)}">{naam}</a>'

# alleen fylker met locaties, van zuid naar noord
REGN = {"agder": ["Agder", "Agder", "Agder"],
        "buskerud": ["Buskerud", "Buskerud", "Buskerud"],
        "innlandet": ["Innlandet", "Innlandet", "Innlandet"],
        "trondelag": ["Trøndelag", "Trøndelag", "Trøndelag"],
        "troms": ["Troms", "Troms", "Troms"]}

DYR, BJO, LAN, TAN, POL, NOR = L("Dyreparken"), L("Bjørneparken"), L("Langedrag Naturpark"), L("Tangen Dyrepark"), L("Polar Park"), L("Park Nordica")

# losse vervangingen in het sjabloon (resten van Portugal in de Noorse vaste teksten)
NB_VERV = [("i Portugal", "i Norge"), ("I Portugal", "I Norge"), ("portugisiske dyreparker", "norske dyreparker")]
VAST = [
 (r'<p class="stamp">.*?</p>', '<p class="stamp"><span class="l-nl">Stand 23 oktober 2026</span><span class="l-en">Updated 23 October 2026</span><span class="l-nb">Oppdatert 23. oktober 2026</span></p>'),
 (r'<p class="lede">.*?</p>', '<p class="lede">'
  '<span class="l-nl">Waar in Noorwegen kun je tijgers, leeuwen, cheetahs, lynxen en andere wilde katten zien? Per soort en per park zie je hier welke katten er wonen, welke jongen er onlangs geboren zijn en wat er binnenkort verandert. En met welke route je alle soorten ziet.</span>'
  '<span class="l-en">Where in Norway can you see tigers, lions, cheetahs, lynxes and other wild cats? By species and by park, this guide shows which cats live where, which young were born recently and what is about to change. And which route lets you see every species.</span>'
  '<span class="l-nb">Hvor i Norge kan du se tigre, løver, geparder, gauper og andre ville kattedyr? Per art og per park viser guiden hvilke katter som bor hvor, hvilke unger som nylig er født og hva som snart endrer seg. Og hvilken rute som tar deg til alle artene.</span></p>'),
]

LOC_INTRO = ["Alle dierentuinen, dierenparken en wildparken in Noorwegen waar bezoekers wilde katten kunnen zien. Tik op een stip om te zien welke katten er wonen.",
             "All zoos, animal parks and wildlife parks in Norway where visitors can see wild cats. Tap a dot to see which cats live there.",
             "Alle dyrehager, dyreparker og viltparker i Norge der du kan se ville kattedyr. Trykk på en prikk for å se hvilke katter som bor der."]

def tldr():
    nl = f'''<div class="l-nl">
<div class="prose">
  <ul>
    <li><strong>6 soorten bevestigd</strong> op 6 locaties: 2 dierentuinen (lid van EAZA of de Zweedse dierentuinvereniging SDF), 1 dierenpark en 3 wildparken met Noordse dieren.</li>
    <li><strong>{DYR}</strong> in Kristiansand heeft de meeste soorten: tijger, leeuw, cheetah en lynx. De Euraziatische lynx, de wilde kat van Noorwegen zelf, zie je in 5 parken, tot ver boven de poolcirkel ({POL}).</li>
    <li><strong>Maar op één plek te zien:</strong> de tijger, de leeuw en de cheetah ({DYR}), de Amoerluipaard ({BJO}) en de serval ({TAN}).</li>
    <li><strong>Jonge katten:</strong> vier cheetahs (augustus 2026) en leeuwenwelpen uit april 2026 en mei 2025 in {DYR}.</li>
    <li><strong>Bijzonder:</strong> in {LAN} kun je met een begeleider het lynxverblijf in en overnachten in een hut midden tussen de lynxen.</li>
    <li><strong>Geen particulieren en geen circussen:</strong> uitheemse wilde katten mogen in Noorwegen niet als huisdier worden gehouden en niet in een circus optreden. De serval van {TAN} is een in beslag genomen huisdier.</li>
  </ul>
  </div>
</div>'''
    en = f'''<div class="l-en">
<div class="prose">
  <ul>
    <li><strong>6 species confirmed</strong> at 6 locations: 2 zoos (members of EAZA or the Swedish zoo association SDF), 1 animal park and 3 wildlife parks with Nordic animals.</li>
    <li><strong>{DYR}</strong> in Kristiansand has the most species: tiger, lion, cheetah and lynx. The Eurasian lynx, Norway’s own wild cat, can be seen in 5 parks, up to far above the Arctic Circle ({POL}).</li>
    <li><strong>Only in one place:</strong> the tiger, the lion and the cheetah ({DYR}), the Amur leopard ({BJO}) and the serval ({TAN}).</li>
    <li><strong>Young cats:</strong> four cheetahs (August 2026) and lion cubs from April 2026 and May 2025 at {DYR}.</li>
    <li><strong>Special:</strong> at {LAN} you can enter the lynx enclosure with a guide and stay overnight in a cabin among the lynxes.</li>
    <li><strong>No private keepers and no circuses:</strong> in Norway exotic wild cats may not be kept as pets or shown in circuses. The serval at {TAN} is a confiscated pet.</li>
  </ul>
  </div>
</div>'''
    nb = f'''<div class="l-nb">
<div class="prose">
  <ul>
    <li><strong>6 arter bekreftet</strong> på 6 steder: 2 dyrehager (medlem av EAZA eller den svenske dyreparkforeningen SDF), 1 dyrepark og 3 viltparker med nordiske dyr.</li>
    <li><strong>{DYR}</strong> i Kristiansand har flest arter: tiger, løve, gepard og gaupe. Gaupa, Norges eget ville kattedyr, kan du se i 5 parker, helt opp til langt nord for polarsirkelen ({POL}).</li>
    <li><strong>Bare ett sted:</strong> tiger, løve og gepard ({DYR}), amurleopard ({BJO}) og serval ({TAN}).</li>
    <li><strong>Unger:</strong> fire geparder (august 2026) og løveunger fra april 2026 og mai 2025 i {DYR}.</li>
    <li><strong>Spesielt:</strong> på {LAN} kan du bli med inn i gaupeinnhegningen og overnatte i en hytte midt blant gaupene.</li>
    <li><strong>Ingen privatpersoner og ingen sirkus:</strong> i Norge er det forbudt å holde eksotiske ville kattedyr som kjæledyr eller vise dem i sirkus. Servalen på {TAN} er et beslaglagt kjæledyr.</li>
  </ul>
  </div>
</div>'''
    return nl + en + nb + "\n"

GEEN = [
 [("Aquaria zonder katachtigen", "Aquariums without cats", "Akvarier uten kattedyr"),
  "Akvariet i Bergen en Atlanterhavsparken (Ålesund; beide EAZA), Polaria (Tromsø), Lofotakvariet, Sognefjord Akvarium, Drøbak Akvarium, Risør Akvarium, Saltstraumen Opplevelsessenter",
  ["Akvariet i Bergen and Atlanterhavsparken (Ålesund; both EAZA), Polaria (Tromsø), Lofotakvariet, Sognefjord Akvarium, Drøbak Akvarium, Risør Akvarium, Saltstraumen Opplevelsessenter",
   "Akvariet i Bergen og Atlanterhavsparken (Ålesund; begge EAZA), Polaria (Tromsø), Lofotakvariet, Sognefjord Akvarium, Drøbak Akvarium, Risør Akvarium, Saltstraumen Opplevelsessenter"]],
 [("Vroeger katachtigen", "Cats in the past", "Tidligere kattedyr"),
  "Haugaland Zoo (Karmøy; nevelpanter rond 2017–2018, nu een vogel- en familiepark)",
  ["Haugaland Zoo (Karmøy; clouded leopard around 2017–2018, now a bird and family park)",
   "Haugaland Zoo (Karmøy; skyleopard rundt 2017–2018, nå en fugle- og familiepark)"]],
 [("Circussen zonder katten", "Circuses without cats", "Sirkus uten kattedyr"),
  "Cirkus Arnardo, Cirkus Agora, Cirkus Merano; voor dieren in een circus is een vergunning van Mattilsynet nodig, die alleen voor gedomesticeerde soorten wordt gegeven",
  ["Cirkus Arnardo, Cirkus Agora, Cirkus Merano; animals in a circus need a permit from Mattilsynet, which is only given for domesticated species",
   "Cirkus Arnardo, Cirkus Agora, Cirkus Merano; dyr i sirkus krever tillatelse fra Mattilsynet, som bare gis for tamme arter"]],
 [("Andere dierenparken en attractieparken zonder katachtigen", "Other animal parks and amusement parks without cats", "Andre dyreparker og fornøyelsesparker uten kattedyr"),
  "Oslo Reptilpark, Den Lille Dyrehage (Gjerstad), Kongeparken (Ålgård), Haugaland Zoo, Foldvik Familiepark (alleen huiskatten), Barnas Dyrepark Lindesnes, Hunderfossen, Snilsberg, Lilleputthammer, Hjorteparken Mork",
  ["Oslo Reptilpark, Den Lille Dyrehage (Gjerstad), Kongeparken (Ålgård), Haugaland Zoo, Foldvik Familiepark (domestic cats only), Barnas Dyrepark Lindesnes, Hunderfossen, Snilsberg, Lilleputthammer, Hjorteparken Mork",
   "Oslo Reptilpark, Den Lille Dyrehage (Gjerstad), Kongeparken (Ålgård), Haugaland Zoo, Foldvik Familiepark (bare tamkatter), Barnas Dyrepark Lindesnes, Hunderfossen, Snilsberg, Lilleputthammer, Hjorteparken Mork"]],
]
def geen(i):
    out = ""
    for row in GEEN:
        k, t, tr = row
        if i and tr: t = tr[i - 1]
        out += f"    <li><b>{k[i]}:</b> {t}</li>\n"
    return out

OFFICIEEL = [
 """<p>Noorwegen heeft geen openbare lijst van dierentuinen. Een dierenpark meldt zich bij Mattilsynet (voedsel- en dierenautoriteit) en heeft voor elke soort die geen huisdier is een vergunning nodig (forskrift om dyrevelferd ved fremvisning av dyr, 2016). Voor wilde katten is dus altijd een vergunning nodig; voor de lynx, een inheemse soort, ook van de milieudienst. De Raad voor dierethiek telde in 2021 dertien dierenparken.</p>
    <p>Particulieren mogen sinds 2017 geen uitheemse wilde zoogdieren houden, ook geen kruisingen met huiskatten tot en met de vierde generatie. In circussen mogen alleen gedomesticeerde dieren optreden. Wilde katten zie je in Noorwegen dus alleen in dierenparken.</p>
    <p>De lijst in deze gids is opgebouwd uit de ledenlijsten van EAZA (3 Noorse leden) en de Zweedse dierentuinvereniging SDF (1 Noors lid), Zootierliste (alle katachtigen, huidige en vroegere houders) en een zoektocht per fylke naar dierenparken, wildparken, aquaria, opvang en circussen.</p>
    <p>Of een park een dierentuin heet, hangt in deze gids af van het lidmaatschap van EAZA of SDF. Parken met alleen Noordse dieren in grote natuurlijke verblijven heten wildpark.</p>
""",
 """<p>Norway has no public list of zoos. An animal park registers with Mattilsynet (the Norwegian Food Safety Authority) and needs a permit for every species that is not a domestic animal (regulation on the welfare of animals on display, 2016). Wild cats therefore always need a permit; the lynx, a native species, also needs one from the environment agency. The Council for Animal Ethics counted thirteen animal parks in 2021.</p>
    <p>Since 2017 private individuals may not keep exotic wild mammals, nor crosses with domestic cats up to the fourth generation. Only domesticated animals may perform in circuses. So in Norway you can only see wild cats in animal parks.</p>
    <p>The list in this guide was built from the member lists of EAZA (3 Norwegian members) and the Swedish zoo association SDF (1 Norwegian member), Zootierliste (all cats, current and former holders) and a search county by county for animal parks, wildlife parks, aquariums, rescue centres and circuses.</p>
    <p>Whether a park is called a zoo in this guide depends on membership of EAZA or SDF. Parks with only Nordic animals in large natural enclosures are called wildlife parks.</p>
""",
 """<p>Norge har ingen offentlig liste over dyreparker. En dyrepark melder seg til Mattilsynet og trenger tillatelse for hver art som ikke er et husdyr (forskrift om dyrevelferd ved fremvisning av dyr, 2016). Ville kattedyr krever derfor alltid tillatelse; gaupa, som er en norsk art, også fra miljømyndighetene. Rådet for dyreetikk telte tretten dyreparker i 2021.</p>
    <p>Siden 2017 har privatpersoner ikke fått holde eksotiske ville pattedyr, heller ikke krysninger med tamkatt til og med fjerde generasjon. I sirkus kan bare tamme dyr opptre. Ville kattedyr kan du altså bare se i dyreparker.</p>
    <p>Listen i guiden bygger på medlemslistene til EAZA (3 norske medlemmer) og den svenske dyreparkforeningen SDF (1 norsk medlem), Zootierliste (alle kattedyr, nåværende og tidligere holdere) og et søk fylke for fylke etter dyreparker, viltparker, akvarier, redningssentre og sirkus.</p>
    <p>Om en park kalles dyrehage i guiden, avhenger av medlemskap i EAZA eller SDF. Parker med bare nordiske dyr i store, naturlige innhegninger kalles viltpark.</p>
"""]

ADVIES = [
 f"""<ul class="prose">
    <li><strong>Alle 6 soorten in drie parken:</strong>
      <ul>
        <li><strong>Dyreparken</strong> (Kristiansand): tijger, leeuw, cheetah, lynx</li>
        <li><strong>Bjørneparken</strong> (Flå, Hallingdal): Amoerluipaard (en lynx)</li>
        <li><strong>Tangen Dyrepark</strong> (Stange, bij Hamar): serval</li>
      </ul>
    </li>
    <li><strong>Alternatieven voor de lynx:</strong> {LAN} (ook in Hallingdal, met overnachting tussen de lynxen), {NOR} in Trøndelag en {POL} in Troms.</li>
    <li><strong>Plan in de zomer:</strong> Bjørneparken en Tangen Dyrepark zijn in de winter dicht. Openingstijden staan op de pagina van elk park.</li>
    <li><strong>Twijfel je over een dier?</strong> Bel of mail dan vóór je bezoek met het park.</li>
  </ul>
""",
 f"""<ul class="prose">
    <li><strong>All 6 species in three parks:</strong>
      <ul>
        <li><strong>Dyreparken</strong> (Kristiansand): tiger, lion, cheetah, lynx</li>
        <li><strong>Bjørneparken</strong> (Flå, Hallingdal): Amur leopard (and lynx)</li>
        <li><strong>Tangen Dyrepark</strong> (Stange, near Hamar): serval</li>
      </ul>
    </li>
    <li><strong>Alternatives for the lynx:</strong> {LAN} (also in Hallingdal, with a night among the lynxes), {NOR} in Trøndelag and {POL} in Troms.</li>
    <li><strong>Plan for summer:</strong> Bjørneparken and Tangen Dyrepark are closed in winter. Opening times are on each park’s page.</li>
    <li><strong>Not sure about an animal?</strong> Call or email the park before your visit.</li>
  </ul>
""",
 f"""<ul class="prose">
    <li><strong>Alle 6 artene i tre parker:</strong>
      <ul>
        <li><strong>Dyreparken</strong> (Kristiansand): tiger, løve, gepard, gaupe</li>
        <li><strong>Bjørneparken</strong> (Flå, Hallingdal): amurleopard (og gaupe)</li>
        <li><strong>Tangen Dyrepark</strong> (Stange, ved Hamar): serval</li>
      </ul>
    </li>
    <li><strong>Alternativer for gaupa:</strong> {LAN} (også i Hallingdal, med overnatting blant gaupene), {NOR} i Trøndelag og {POL} i Troms.</li>
    <li><strong>Planlegg for sommeren:</strong> Bjørneparken og Tangen Dyrepark er stengt om vinteren. Åpningstider står på hver parks side.</li>
    <li><strong>Usikker på et dyr?</strong> Ring eller send e-post til parken før besøket.</li>
  </ul>
"""]

GEPLAND = [
 f"""<ul class="prose">
    <li><strong>{BJO}:</strong> voor mei 2026 was de komst van een Amoerluipaardpoes (Mila, uit Pittsburgh) aangekondigd; niet bevestigd dat ze er is.</li>
    <li><strong>Seizoen voorbij:</strong> {BJO} gaat in april 2027 weer open, {TAN} in mei 2027.</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Gepland</span> · <span class="st st-w"><i></i>Onzeker</span></p>
""",
 f"""<ul class="prose">
    <li><strong>{BJO}:</strong> an Amur leopard female (Mila, from Pittsburgh) was announced for May 2026; not confirmed that she has arrived.</li>
    <li><strong>Season over:</strong> {BJO} reopens in April 2027, {TAN} in May 2027.</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Planned</span> · <span class="st st-w"><i></i>Uncertain</span></p>
""",
 f"""<ul class="prose">
    <li><strong>{BJO}:</strong> en amurleopardhunn (Mila, fra Pittsburgh) var varslet til mai 2026; ikke bekreftet at hun har kommet.</li>
    <li><strong>Sesongen er over:</strong> {BJO} åpner igjen i april 2027, {TAN} i mai 2027.</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Planlagt</span> · <span class="st st-w"><i></i>Usikkert</span></p>
"""]

KVTXT = {"nl": "Er zijn in Noorwegen geen witte tijgers, witte leeuwen of zwarte panters gevonden.",
         "en": "No white tigers, white lions or black panthers were found in Norway.",
         "nb": "Det ble ikke funnet hvite tigre, hvite løver eller svarte pantere i Norge."}
HYB = {"nl": "Er zijn geen lijgers, tigons of andere hybriden van wilde katten gevonden. Kruisingen van huiskatten en wilde katten (zoals savannah- en bengaalkatten) tot en met de vierde generatie mogen in Noorwegen niet particulier worden gehouden; ze tellen in deze gids niet mee.",
       "en": "No ligers, tigons or other hybrids of wild cats were found. Crosses between domestic cats and wild cats (such as Savannah and Bengal cats) up to the fourth generation may not be kept privately in Norway; they do not count in this guide.",
       "nb": "Det ble ikke funnet ligere, tigoner eller andre hybrider av ville kattedyr. Krysninger mellom tamkatt og ville kattedyr (som savannah- og bengalkatter) til og med fjerde generasjon kan ikke holdes privat i Norge; de teller ikke i guiden."}
def _kleur():
    out = ""
    for lg in ["nl", "en", "nb"]:
        out += f'<div class="l-{lg}">\n  <p class="prose">{KVTXT[lg]}</p>\n</div>'
    out += '<h3 id="hybriden" style="font-size:22px;margin-top:30px"><span class="l-nl">Hybriden</span><span class="l-en">Hybrids</span><span class="l-nb">Hybrider</span></h3>\n'
    for lg in ["nl", "en", "nb"]:
        out += f'<div class="l-{lg}">\n<p class="prose">{HYB[lg]}</p>\n</div>'
    return out
KLEUR = _kleur()

UITLEG = {
 "werkwijze": {
  "nl": """<p class="prose">Voor alle Noorse dierentuinen, dierenparken, wildparken, aquaria, opvangcentra en circussen is nagegaan welke wilde katachtigen er te zien zijn. Omdat er geen officiële lijst is, komt de basislijst uit de ledenlijsten van EAZA en SDF en uit Zootierliste (alle katachtigen, huidige en vroegere houders); per fylke is daarna gezocht naar andere parken. Elke locatie is gecontroleerd op de eigen website, aangevuld met Noors nieuws. Bij elke vermelding staan de bron en de datum.</p>
  <p class="prose">Een kat telt mee als een bezoeker hem kan zien. Vrij levende lynxen tellen niet mee.</p>
  <p class="prose">De indeling in soorten volgt de standaard van de IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>""",
  "en": """<p class="prose">For all Norwegian zoos, animal parks, wildlife parks, aquariums, rescue centres and circuses, we checked which wild cats can be seen. As there is no official list, the base list comes from the member lists of EAZA and SDF and from Zootierliste (all cats, current and former holders); each county was then searched for other parks. Every location was checked on its own website, supplemented by Norwegian news. Each entry shows its source and date.</p>
  <p class="prose">A cat counts if a visitor can see it. Free-living lynxes do not count.</p>
  <p class="prose">Species follow the standard of the IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>""",
  "nb": """<p class="prose">For alle norske dyrehager, dyreparker, viltparker, akvarier, redningssentre og sirkus har vi sjekket hvilke ville kattedyr du kan se. Siden det ikke finnes noen offisiell liste, kommer grunnlisten fra medlemslistene til EAZA og SDF og fra Zootierliste (alle kattedyr, nåværende og tidligere holdere); deretter har vi søkt etter andre parker fylke for fylke. Hvert sted er sjekket på sin egen nettside, supplert med norske nyheter. Hver oppføring viser kilde og dato.</p>
  <p class="prose">En katt teller hvis en besøkende kan se den. Frittlevende gauper teller ikke.</p>
  <p class="prose">Inndelingen i arter følger standarden fra IUCN/SSC Cat Classification Task Force (Kitchener mfl., 2017, <i>Cat News</i> Special Issue 11).</p>"""},
 "namen": {
  "nl": """<ul class="prose">
    <li><strong>Gaupe</strong> is de Euraziatische lynx, <strong>gepard</strong> de cheetah, <strong>løve</strong> de leeuw en <strong>amurleopard</strong> de Amoerluipaard.</li>
    <li><strong>Dyrepark</strong> betekent dierenpark; Dyreparken in Kristiansand heet ook Kristiansand Dyrepark.</li>
  </ul>""",
  "en": """<ul class="prose">
    <li><strong>Gaupe</strong> is the Eurasian lynx, <strong>gepard</strong> the cheetah, <strong>løve</strong> the lion and <strong>amurleopard</strong> the Amur leopard.</li>
    <li><strong>Dyrepark</strong> means animal park; Dyreparken in Kristiansand is also called Kristiansand Dyrepark.</li>
  </ul>""",
  "nb": """<ul class="prose">
    <li>Guiden er skrevet på nederlandsk; de norske artsnavnene står på artssidene. <strong>Gaupe</strong> heter <i>Euraziatische lynx</i> på nederlandsk, <strong>gepard</strong> <i>cheetah</i> og <strong>amurleopard</strong> <i>Amoerluipaard</i>.</li>
    <li>Dyreparken i Kristiansand kalles også Kristiansand Dyrepark.</li>
  </ul>"""},
 "verdwenen": {
  "nl": f"""<p class="prose">Bij elk park staat onder “Eerder hier” welke katten er vroeger waren. Opvallend: de Amoertijger Altai, in 2022 in {DYR} geboren, ging in februari 2025 naar Yorkshire Wildlife Park; de serval Niño zat eerst tijdelijk in {DYR}. Haugaland Zoo had rond 2017–2018 een nevelpanter.</p>""",
  "en": f"""<p class="prose">Each park’s page lists under “Previously here” which cats it used to have. Notable: the Amur tiger Altai, born at {DYR} in 2022, moved to Yorkshire Wildlife Park in February 2025; the serval Niño first stayed temporarily at {DYR}. Haugaland Zoo had a clouded leopard around 2017–2018.</p>""",
  "nb": f"""<p class="prose">På hver parks side står det under «Tidligere her» hvilke katter som fantes der før. Verdt å nevne: amurtigeren Altai, født i {DYR} i 2022, flyttet i februar 2025 til Yorkshire Wildlife Park; servalen Niño bodde først midlertidig i {DYR}. Haugaland Zoo hadde en skyleopard rundt 2017–2018.</p>"""},
 "controle": {
  "nl": """<p class="prose"><strong>Lijsten en regels:</strong> de ledenlijsten van EAZA en SDF (oktober 2026), de regels van Mattilsynet voor dieren die worden getoond (FOR-2016-09-05-1035) en het verbod op het houden van uitheemse dieren (FOR-2017-05-11-597).</p>
  <p class="prose"><strong>Databanken:</strong> Zootierliste (alle katachtigen, huidige en vroegere houdingen), alleen aanvullend.</p>
  <p class="prose"><strong>Websites van de parken</strong>, met dierenlijsten, soortpagina’s, kalenders en nieuws.</p>
  <p class="prose"><strong>Nieuws:</strong> onder meer NRK, TV 2, Fædrelandsvennen en regionale kranten.</p>""",
  "en": """<p class="prose"><strong>Lists and rules:</strong> the member lists of EAZA and SDF (October 2026), Mattilsynet’s rules on animals on display (FOR-2016-09-05-1035) and the ban on keeping exotic animals (FOR-2017-05-11-597).</p>
  <p class="prose"><strong>Databases:</strong> Zootierliste (all cats, current and former holdings), used only as a supplement.</p>
  <p class="prose"><strong>Park websites</strong>, with animal lists, species pages, calendars and news.</p>
  <p class="prose"><strong>News:</strong> including NRK, TV 2, Fædrelandsvennen and regional newspapers.</p>""",
  "nb": """<p class="prose"><strong>Lister og regler:</strong> medlemslistene til EAZA og SDF (oktober 2026), Mattilsynets regler for fremvisning av dyr (FOR-2016-09-05-1035) og forbudet mot å holde eksotiske dyr (FOR-2017-05-11-597).</p>
  <p class="prose"><strong>Databaser:</strong> Zootierliste (alle kattedyr, nåværende og tidligere holdere), bare som supplement.</p>
  <p class="prose"><strong>Parkenes nettsider</strong> med dyrelister, artssider, kalendere og nyheter.</p>
  <p class="prose"><strong>Nyheter:</strong> blant annet NRK, TV 2, Fædrelandsvennen og regionale aviser.</p>"""},
}
