# Landspecifieke tekstblokken van de Roemeense gids (NL / EN / RO). Stand 30 oktober 2026.
import re, unicodedata
def _slug(x):
    x = "".join(c for c in unicodedata.normalize("NFD", x) if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"\(.*?\)", "", x)).strip("-")
def L(naam): return f'<a href="#locatie/{_slug(naam)}">{naam}</a>'

# alleen județe met locaties, ruwweg van west naar oost
REGN = {"bihor": ["Bihor", "Bihor", "Bihor"],
        "caras-severin": ["Caraș-Severin", "Caraș-Severin", "Caraș-Severin"],
        "cluj": ["Cluj", "Cluj", "Cluj"],
        "dolj": ["Dolj", "Dolj", "Dolj"],
        "sibiu": ["Sibiu", "Sibiu", "Sibiu"],
        "valcea": ["Vâlcea", "Vâlcea", "Vâlcea"],
        "mures": ["Mureș", "Mureș", "Mureș"],
        "arges": ["Argeș", "Argeș", "Argeș"],
        "dambovita": ["Dâmbovița", "Dâmbovița", "Dâmbovița"],
        "brasov": ["Brașov", "Brașov", "Brașov"],
        "suceava": ["Suceava", "Suceava", "Suceava"],
        "prahova": ["Prahova", "Prahova", "Prahova"],
        "bucuresti": ["Boekarest", "Bucharest", "București"],
        "calarasi": ["Călărași", "Călărași", "Călărași"],
        "vaslui": ["Vaslui", "Vaslui", "Vaslui"],
        "braila": ["Brăila", "Brăila", "Brăila"],
        "galati": ["Galați", "Galați", "Galați"]}

BUC, BRV, TGM, SIB, PLO = L("Zoo București (Băneasa)"), L("Zoo Brașov"), L("Zoo Târgu Mureș"), L("Zoo Sibiu"), L("Zoo Ploiești (Bucov)")
ORA, RES, LIS, TIN, CRA, BAR, GAL, ARC = L("Zoo Oradea"), L("Zoo Reșița"), L("Liska Park"), L("Ținutul Cailor"), L("Zoo Craiova"), L("Zoo Bârlad"), L("Zoo Galați (Gârboavele)"), L("Arca lui Noe")

# losse vervangingen in het sjabloon (resten van Portugal in de Roemeense vaste teksten)
RO_VERV = [("Portugalia", "România")]
VAST = [
 (r'<p class="stamp">.*?</p>', '<p class="stamp"><span class="l-nl">Stand 30 oktober 2026</span><span class="l-en">Updated 30 October 2026</span><span class="l-ro">Actualizat: 30 octombrie 2026</span></p>'),
 (r'<p class="lede">.*?</p>', '<p class="lede">'
  '<span class="l-nl">Waar in Roemenië kun je leeuwen, tijgers, jaguars, lynxen en andere wilde katten zien? Per soort en per park zie je hier welke katten er wonen, welke jongen er onlangs geboren zijn en wat er binnenkort verandert. En met welke route je alle soorten ziet.</span>'
  '<span class="l-en">Where in Romania can you see lions, tigers, jaguars, lynxes and other wild cats? By species and by park, this guide shows which cats live where, which young were born recently and what is about to change. And which route lets you see every species.</span>'
  '<span class="l-ro">Unde poți vedea în România lei, tigri, jaguari, râși și alte feline sălbatice? Ghidul îți arată, pe specii și pe parcuri, ce feline trăiesc și unde, ce pui s-au născut de curând și ce se schimbă în curând. Și pe ce traseu poți vedea toate speciile.</span></p>'),
]

LOC_INTRO = ["Alle dierentuinen, dierenparken en particuliere parken in Roemenië waar wilde katten wonen. Tik op een stip om te zien welke katten er wonen.",
             "All zoos, animal parks and private parks in Romania where wild cats live. Tap a dot to see which cats live there.",
             "Toate grădinile zoologice, parcurile zoologice și parcurile private din România în care trăiesc feline sălbatice. Atinge un punct ca să vezi ce feline trăiesc acolo."]

def tldr():
    nl = f'''<div class="l-nl">
<div class="prose">
  <ul>
    <li><strong>9 soorten bevestigd</strong> op 16 locaties: 13 vergunde dierentuinen, de dierentuin van Bârlad (vergunning aangevraagd) en 2 particuliere parken. Bij 4 andere locaties is niets recent bevestigd.</li>
    <li><strong>Leeuw en tijger</strong> zie je bijna overal: elk in 14 parken. De andere soorten zijn zeldzaam.</li>
    <li><strong>{BUC}</strong> heeft 7 soorten, {BRV} en {TGM} elk 5.</li>
    <li><strong>Maar op één plek te zien:</strong> de serval ({BUC}), de caracal ({LIS}, particulier) en de sneeuwluipaard ({BRV}, sinds maart 2026 niet te zien).</li>
    <li><strong>Jonge katten:</strong> twee Amoertijgers in {ORA} (ca. april 2026) en twee leeuwen in {PLO} (maart 2025).</li>
    <li><strong>Witte tijgers</strong> in {CRA} en {TGM}; een <strong>zwarte panter</strong> in {BUC}.</li>
    <li><strong>Circussen:</strong> wilde dieren zijn in Roemeense circussen verboden sinds 2017.</li>
  </ul>
  </div>
</div>'''
    en = f'''<div class="l-en">
<div class="prose">
  <ul>
    <li><strong>9 species confirmed</strong> at 16 locations: 13 licensed zoos, the zoo of Bârlad (licence applied for) and 2 private parks. At 4 other locations nothing has been confirmed recently.</li>
    <li><strong>Lion and tiger</strong> can be seen almost everywhere: each in 14 parks. The other species are rare.</li>
    <li><strong>{BUC}</strong> has 7 species, {BRV} and {TGM} 5 each.</li>
    <li><strong>Only in one place:</strong> the serval ({BUC}), the caracal ({LIS}, private) and the snow leopard ({BRV}, not on view since March 2026).</li>
    <li><strong>Young cats:</strong> two Amur tigers at {ORA} (c. April 2026) and two lions at {PLO} (March 2025).</li>
    <li><strong>White tigers</strong> at {CRA} and {TGM}; a <strong>black panther</strong> at {BUC}.</li>
    <li><strong>Circuses:</strong> wild animals have been banned in Romanian circuses since 2017.</li>
  </ul>
  </div>
</div>'''
    ro = f'''<div class="l-ro">
<div class="prose">
  <ul>
    <li><strong>9 specii confirmate</strong> în 16 locații: 13 grădini zoologice autorizate, grădina zoologică din Bârlad (în curs de autorizare) și 2 parcuri private. În alte 4 locații nu s-a confirmat nimic recent.</li>
    <li><strong>Leul și tigrul</strong> se văd aproape peste tot: fiecare în 14 parcuri. Celelalte specii sunt rare.</li>
    <li><strong>{BUC}</strong> are 7 specii, {BRV} și {TGM} câte 5.</li>
    <li><strong>Într-un singur loc:</strong> servalul ({BUC}), caracalul ({LIS}, privat) și leopardul zăpezilor ({BRV}, nu poate fi văzut din martie 2026).</li>
    <li><strong>Pui:</strong> doi tigri de Amur la {ORA} (cca. aprilie 2026) și doi lei la {PLO} (martie 2025).</li>
    <li><strong>Tigri albi</strong> la {CRA} și {TGM}; o <strong>panteră neagră</strong> la {BUC}.</li>
    <li><strong>Circuri:</strong> animalele sălbatice sunt interzise în circurile din România din 2017.</li>
  </ul>
  </div>
</div>'''
    return nl + en + ro + "\n"

GEEN = [
 [("Vergunde dierentuinen en opvang zonder katachtigen", "Licensed zoos and rescue centres without cats", "Grădini zoologice și centre autorizate fără feline"),
  "Zoo Roman, Green Codru (Bihor), Dragoș Vodă (Vânători-Neamț) en Vama Buzăului (wisenten), de vivaria van Bacău en Oradea, de aquaria van Constanța, Galați, Ploiești, Tulcea en Drobeta-Turnu Severin, Libearty Zărnești en Bălan (beren)",
  ["Zoo Roman, Green Codru (Bihor), Dragoș Vodă (Vânători-Neamț) and Vama Buzăului (bison), the vivaria of Bacău and Oradea, the aquaria of Constanța, Galați, Ploiești, Tulcea and Drobeta-Turnu Severin, Libearty Zărnești and Bălan (bears)",
   "Zoo Roman, Green Codru (Bihor), Dragoș Vodă (Vânători-Neamț) și Vama Buzăului (zimbri), vivariile din Bacău și Oradea, acvariile din Constanța, Galați, Ploiești, Tulcea și Drobeta-Turnu Severin, Libearty Zărnești și Bălan (urși)"]],
 [("Gesloten dierentuinen", "Closed zoos", "Grădini zoologice închise"),
  "Timișoara (sinds 2020), Hunedoara (2025; de tijgers gingen naar Reșița), Turda (2021), Piatra Neamț (2021), Baia Mare, Onești, Buhuși, Slatina, Caracal en Târgu Jiu",
  ["Timișoara (since 2020), Hunedoara (2025; the tigers went to Reșița), Turda (2021), Piatra Neamț (2021), Baia Mare, Onești, Buhuși, Slatina, Caracal and Târgu Jiu",
   "Timișoara (din 2020), Hunedoara (2025; tigrii au ajuns la Reșița), Turda (2021), Piatra Neamț (2021), Baia Mare, Onești, Buhuși, Slatina, Caracal și Târgu Jiu"]],
 [("Circussen en rondreizende shows", "Circuses and travelling shows", "Circuri și spectacole itinerante"),
  "Circul Metropolitan București (Globus) heeft geen wilde dieren meer; de rondreizende show ‘Zoo Park’ heeft geen katten",
  ["Circul Metropolitan București (Globus) no longer has wild animals; the travelling show ‘Zoo Park’ has no cats",
   "Circul Metropolitan București (Globus) nu mai are animale sălbatice; spectacolul itinerant „Zoo Park” nu are feline"]],
 [("Minizoo’s en kinderboerderijen zonder katachtigen", "Mini zoos and farm parks without cats", "Mini-zoo-uri și ferme cu animale fără feline"),
  "ZooLand Arad, Zoolandia (Chimindia), Parcul Bejan (Deva), Arca Land (Sculeni), Hadâmbu (Mironeasa), Lelești, Zetea, Băile Bálványos, Dracula’s Reptiles (Brașov) en andere kleine parken. Chiajna (Ilfov) had rond 2014 leeuwen en tijgers; daarna niets bekend",
  ["ZooLand Arad, Zoolandia (Chimindia), Parcul Bejan (Deva), Arca Land (Sculeni), Hadâmbu (Mironeasa), Lelești, Zetea, Băile Bálványos, Dracula’s Reptiles (Brașov) and other small parks. Chiajna (Ilfov) had lions and tigers around 2014; nothing known since",
   "ZooLand Arad, Zoolandia (Chimindia), Parcul Bejan (Deva), Arca Land (Sculeni), Hadâmbu (Mironeasa), Lelești, Zetea, Băile Bálványos, Dracula’s Reptiles (Brașov) și alte parcuri mici. Chiajna (Ilfov) avea lei și tigri în jurul anului 2014; de atunci nu se mai știe nimic"]],
]
def geen(i):
    out = ""
    for row in GEEN:
        k, t, tr = row
        if i and tr: t = tr[i - 1]
        out += f"    <li><b>{k[i]}:</b> {t}</li>\n"
    return out

OFFICIEEL = [
 """<p>In Roemenië heeft elke dierentuin een milieuvergunning nodig van het milieuagentschap van het district. Het nationale agentschap ANMAP publiceert een overzicht: op 14 november 2025 waren er 30 vergunde dierentuinen en openbare aquaria, één dierentuin in aanvraag (Bârlad) en één tijdelijk gesloten (Timișoara), plus 6 opvangcentra.</p>
    <p>Particulieren mogen wilde dieren alleen houden met een vergunning van de veterinaire dienst van het district. Wilde dieren in circussen zijn verboden sinds 22 juli 2017 (wet 171/2017); sinds 2022 is overtreding strafbaar.</p>
    <p>De lijst in deze gids is opgebouwd uit het ANMAP-overzicht, de EAZA-ledenlijst (Brașov lid sinds september 2025; Sibiu en Târgu Mureș kandidaat), Zootierliste (alle katachtigen, huidige en vroegere houders) en een zoektocht per district naar andere parken, particulieren en circussen.</p>
    <p>De Roemeense dierentuinfederatie FGZAR heeft geen openbare ledenlijst. Daarom heet in deze gids elk park met een dierentuinvergunning van ANMAP een dierentuin. Particuliere parken zonder vergunning staan erin als particuliere houder, met een kanttekening.</p>
""",
 """<p>In Romania every zoo needs an environmental permit from the county environmental agency. The national agency ANMAP publishes an overview: on 14 November 2025 there were 30 licensed zoos and public aquaria, one zoo awaiting a licence (Bârlad) and one temporarily closed (Timișoara), plus 6 rescue centres.</p>
    <p>Private individuals may keep wild animals only with a permit from the county veterinary service. Wild animals in circuses have been banned since 22 July 2017 (Law 171/2017); since 2022 breaking the ban is a criminal offence.</p>
    <p>The list in this guide was built from the ANMAP overview, the EAZA member list (Brașov a member since September 2025; Sibiu and Târgu Mureș candidates), Zootierliste (all cats, current and former holders) and a search county by county for other parks, private keepers and circuses.</p>
    <p>The Romanian zoo federation FGZAR has no public member list. In this guide, every park with an ANMAP zoo licence is therefore called a zoo. Private parks without a licence are listed as private keepers, with a note.</p>
""",
 """<p>În România, fiecare grădină zoologică are nevoie de o autorizație de mediu de la agenția județeană pentru protecția mediului. Agenția națională ANMAP publică o situație: la 14 noiembrie 2025 existau 30 de grădini zoologice și acvarii publice autorizate, o grădină zoologică în curs de autorizare (Bârlad) și una închisă temporar (Timișoara), plus 6 centre de reabilitare.</p>
    <p>Persoanele private pot deține animale sălbatice numai cu autorizație de la direcția sanitar-veterinară județeană. Animalele sălbatice sunt interzise în circuri din 22 iulie 2017 (Legea 171/2017); din 2022, încălcarea interdicției este infracțiune.</p>
    <p>Lista din acest ghid se bazează pe situația ANMAP, pe lista membrilor EAZA (Brașov membru din septembrie 2025; Sibiu și Târgu Mureș candidate), pe Zootierliste (toate felinele, deținători actuali și foști) și pe o căutare pe județe după alte parcuri, deținători privați și circuri.</p>
    <p>Federația Grădinilor Zoologice și Acvariilor din România (FGZAR) nu are o listă publică a membrilor. De aceea, în acest ghid, orice parc cu autorizație de grădină zoologică de la ANMAP se numește grădină zoologică. Parcurile private fără autorizație apar ca deținători privați, cu o mențiune.</p>
"""]

ADVIES = [
 f"""<ul class="prose">
    <li><strong>Alle soorten in drie parken:</strong>
      <ul>
        <li><strong>Zoo București (Băneasa)</strong>: tijger (Amoer en Bengaals), leeuw, luipaard (zwarte panter), jaguar, poema, lynx en serval</li>
        <li><strong>Zoo Brașov</strong>: sneeuwluipaard (sinds maart 2026 niet te zien), Karpatische lynx, jaguar, leeuw en Amoertijger</li>
        <li><strong>Liska Park</strong> (Bihor): caracal (en tijger); particulier, opende zonder vergunning</li>
      </ul>
    </li>
    <li><strong>Alternatieven:</strong> {TGM} heeft poema, Noord-Chinese luipaard, lynx en witte tijgers; {SIB} en {PLO} hebben jaguars.</li>
    <li><strong>Particuliere parken</strong> hebben vaak geen vergunning en kunnen plotseling sluiten; kijk vóór je bezoek op hun site.</li>
    <li><strong>Twijfel je over een dier?</strong> Bel of mail dan vóór je bezoek met het park.</li>
  </ul>
""",
 f"""<ul class="prose">
    <li><strong>All species in three parks:</strong>
      <ul>
        <li><strong>Zoo București (Băneasa)</strong>: tiger (Amur and Bengal), lion, leopard (black panther), jaguar, puma, lynx and serval</li>
        <li><strong>Zoo Brașov</strong>: snow leopard (not on view since March 2026), Carpathian lynx, jaguar, lion and Amur tiger</li>
        <li><strong>Liska Park</strong> (Bihor): caracal (and tiger); private, opened without a licence</li>
      </ul>
    </li>
    <li><strong>Alternatives:</strong> {TGM} has puma, North Chinese leopard, lynx and white tigers; {SIB} and {PLO} have jaguars.</li>
    <li><strong>Private parks</strong> often have no licence and may close suddenly; check their website before you go.</li>
    <li><strong>Not sure about an animal?</strong> Call or email the park before your visit.</li>
  </ul>
""",
 f"""<ul class="prose">
    <li><strong>Toate speciile în trei parcuri:</strong>
      <ul>
        <li><strong>Zoo București (Băneasa)</strong>: tigru (de Amur și bengal), leu, leopard (panteră neagră), jaguar, pumă, râs și serval</li>
        <li><strong>Zoo Brașov</strong>: leopard al zăpezilor (nu poate fi văzut din martie 2026), râs carpatin, jaguar, leu și tigru de Amur</li>
        <li><strong>Liska Park</strong> (Bihor): caracal (și tigru); privat, deschis fără autorizație</li>
      </ul>
    </li>
    <li><strong>Alte variante:</strong> {TGM} are pumă, leopard nord-chinezesc, râs și tigri albi; {SIB} și {PLO} au jaguari.</li>
    <li><strong>Parcurile private</strong> adesea nu au autorizație și se pot închide brusc; verifică site-ul lor înainte de vizită.</li>
    <li><strong>Nu ești sigur de un animal?</strong> Sună sau scrie parcului înainte de vizită.</li>
  </ul>
"""]

GEPLAND = [
 f"""<ul class="prose">
    <li><strong>{GAL}:</strong> in augustus 2026 werden vier leeuwen en een jonge Amoertijger uit een illegale menagerie (Picior de Munte, Dâmbovița) hierheen gestuurd; hun aankomst is niet bevestigd.</li>
    <li><strong>{RES}:</strong> het deel met gevaarlijke dieren is vanaf begin oktober 2026 ongeveer twee maanden dicht voor rioleringswerk.</li>
    <li><strong>{ORA}:</strong> de stad wil de dierentuin verhuizen naar het Cihei-bos (besluit van 25-06-2026).</li>
    <li><strong>{BRV}:</strong> de sneeuwluipaarden zijn sinds 31-03-2026 ‘tijdelijk niet beschikbaar’; de reden is niet bekend.</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Gepland</span> · <span class="st st-w"><i></i>Onzeker</span></p>
""",
 f"""<ul class="prose">
    <li><strong>{GAL}:</strong> in August 2026 four lions and a young Amur tiger from an illegal menagerie (Picior de Munte, Dâmbovița) were sent here; their arrival has not been confirmed.</li>
    <li><strong>{RES}:</strong> the area with dangerous animals is closed for about two months from early October 2026 for sewer works.</li>
    <li><strong>{ORA}:</strong> the city wants to move the zoo to the Cihei forest (decision of 25-06-2026).</li>
    <li><strong>{BRV}:</strong> the snow leopards have been ‘temporarily unavailable’ since 31-03-2026; the reason is not known.</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Planned</span> · <span class="st st-w"><i></i>Uncertain</span></p>
""",
 f"""<ul class="prose">
    <li><strong>{GAL}:</strong> în august 2026, patru lei și un tigru de Amur tânăr dintr-o menajerie ilegală (Picior de Munte, Dâmbovița) au fost trimiși aici; sosirea lor nu este confirmată.</li>
    <li><strong>{RES}:</strong> zona cu animale periculoase este închisă aproximativ două luni de la începutul lui octombrie 2026, pentru lucrări la canalizare.</li>
    <li><strong>{ORA}:</strong> orașul vrea să mute grădina zoologică în pădurea Cihei (hotărârea din 25.06.2026).</li>
    <li><strong>{BRV}:</strong> leoparzii zăpezilor sunt „momentan indisponibili” din 31.03.2026; motivul nu se cunoaște.</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Planificat</span> · <span class="st st-w"><i></i>Incert</span></p>
"""]

def _kv(lg, titel, sp, naar, locs):
    return f'<h3>{titel} <a class="kv-sp" href="#soort/{sp}">{naar}</a></h3>\n  <ul class="prose">\n' + "".join(f"    <li>{x}</li>\n" for x in locs) + "  </ul>\n"
KV = [
 (("Witte tijger", "naar de tijger"), ("White tiger", "to the tiger"), ("Tigru alb", "la tigru"), "tijger", [CRA, TGM]),
 (("Zwarte panter", "naar de luipaard"), ("Black panther", "to the leopard"), ("Panteră neagră", "la leopard"), "luipaard", [BUC]),
]
KVTXT = {"nl": f"Een witte tijger heeft een recessieve mutatie in het gen SLC45A2 en is geen albino; binnen het Europese fokprogramma worden ze niet meer gefokt. Zwarte panters hebben melanisme. Niet recent bevestigd: witte tijgers in {BAR} en {ARC} (gesloten), een witte leeuw in {BRV} (januari 2025, 21 jaar oud) en een witte leeuw in {ORA}.",
         "en": f"A white tiger has a recessive mutation in the SLC45A2 gene and is not an albino; they are no longer bred within the European breeding programme. Black panthers have melanism. Not confirmed recently: white tigers at {BAR} and {ARC} (closed), a white lion at {BRV} (January 2025, 21 years old) and a white lion at {ORA}.",
         "ro": f"Tigrul alb are o mutație recesivă în gena SLC45A2 și nu este albinos; în programul european de reproducere nu mai este crescut. Panterele negre au melanism. Neconfirmate recent: tigri albi la {BAR} și {ARC} (închis), un leu alb la {BRV} (ianuarie 2025, 21 de ani) și un leu alb la {ORA}."}
HYB = {"nl": f"In {ARC} werd in 2025 een liger geboren (kruising van leeuw en tijger), Goliath; hij stierf op 6 mei 2026 bij een brand. Verder zijn geen hybriden van wilde katten gevonden.",
       "en": f"A liger (a cross between lion and tiger), Goliath, was born at {ARC} in 2025; he died in a fire on 6 May 2026. No other hybrids of wild cats were found.",
       "ro": f"La {ARC} s-a născut în 2025 un ligru (încrucișare între leu și tigru), Goliath; a murit într-un incendiu pe 6 mai 2026. Alți hibrizi de feline sălbatice nu au fost găsiți."}
def _kleur():
    out = ""
    for i, lg in enumerate(["nl", "en", "ro"]):
        out += f'<div class="l-{lg}">\n' + "".join(_kv(lg, k[i][0], k[3], k[i][1], k[4]) for k in KV) + f'  <p class="prose">{KVTXT[lg]}</p>\n</div>'
    out += '<h3 id="hybriden" style="font-size:22px;margin-top:30px"><span class="l-nl">Hybriden</span><span class="l-en">Hybrids</span><span class="l-ro">Hibrizi</span></h3>\n'
    for lg in ["nl", "en", "ro"]:
        out += f'<div class="l-{lg}">\n<p class="prose">{HYB[lg]}</p>\n</div>'
    return out
KLEUR = _kleur()

UITLEG = {
 "werkwijze": {
  "nl": """<p class="prose">Voor alle Roemeense dierentuinen, dierenparken, particuliere parken, opvangcentra en circussen is nagegaan welke wilde katachtigen er te zien zijn. De basislijst komt uit het ANMAP-overzicht van vergunde dierentuinen (14-11-2025), de EAZA-ledenlijst en Zootierliste (alle katachtigen, huidige en vroegere houders); per district is daarna gezocht naar andere parken. Elke locatie is gecontroleerd op de eigen website, aangevuld met Roemeens nieuws. Bij elke vermelding staan de bron en de datum.</p>
  <p class="prose">Een kat telt mee als een bezoeker hem kan zien. Veel Roemeense dierentuinen hebben geen actuele dierenlijst online; katten zonder bron uit 2025–2026 staan als onzeker. Particuliere parken staan erin, ook zonder vergunning, met een kanttekening; namen van particulieren staan niet in de gids.</p>
  <p class="prose">De indeling in soorten volgt de standaard van de IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>""",
  "en": """<p class="prose">For all Romanian zoos, animal parks, private parks, rescue centres and circuses, we checked which wild cats can be seen. The base list comes from the ANMAP overview of licensed zoos (14-11-2025), the EAZA member list and Zootierliste (all cats, current and former holders); each county was then searched for other parks. Every location was checked on its own website, supplemented by Romanian news. Each entry shows its source and date.</p>
  <p class="prose">A cat counts if a visitor can see it. Many Romanian zoos have no up-to-date animal list online; cats without a source from 2025–2026 are marked uncertain. Private parks are included, even without a licence, with a note; names of private individuals are not given.</p>
  <p class="prose">Species follow the standard of the IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>""",
  "ro": """<p class="prose">Pentru toate grădinile zoologice, parcurile zoologice, parcurile private, centrele de reabilitare și circurile din România am verificat ce feline sălbatice pot fi văzute. Lista de bază provine din situația ANMAP a grădinilor zoologice autorizate (14.11.2025), din lista membrilor EAZA și din Zootierliste (toate felinele, deținători actuali și foști); apoi am căutat alte parcuri în fiecare județ. Fiecare locație a fost verificată pe site-ul propriu și în presa română. La fiecare înregistrare apar sursa și data.</p>
  <p class="prose">O felină contează dacă un vizitator o poate vedea. Multe grădini zoologice din România nu au online o listă actualizată a animalelor; felinele fără sursă din 2025–2026 apar ca incerte. Parcurile private apar, chiar și fără autorizație, cu o mențiune; numele persoanelor private nu sunt publicate.</p>
  <p class="prose">Împărțirea pe specii urmează standardul IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>"""},
 "namen": {
  "nl": """<ul class="prose">
    <li><strong>Râs</strong> is de Euraziatische lynx (in Roemenië vaak ‘râs carpatin’, Karpatische lynx), <strong>leopard al zăpezilor</strong> de sneeuwluipaard, <strong>pumă</strong> de poema en <strong>pisică sălbatică</strong> de Europese wilde kat.</li>
    <li><strong>Tijger:</strong> ‘tigru siberian’ is de Amoertijger.</li>
    <li><strong>Luipaard:</strong> de Noord-Chinese luipaard van Târgu Mureș hoort bij de Amoerpanter (<i>P. p. orientalis</i>).</li>
  </ul>""",
  "en": """<ul class="prose">
    <li><strong>Râs</strong> is the Eurasian lynx (in Romania often ‘râs carpatin’, Carpathian lynx), <strong>leopard al zăpezilor</strong> the snow leopard, <strong>pumă</strong> the puma and <strong>pisică sălbatică</strong> the European wildcat.</li>
    <li><strong>Tiger:</strong> ‘tigru siberian’ is the Amur tiger.</li>
    <li><strong>Leopard:</strong> the North Chinese leopard of Târgu Mureș belongs to the Amur leopard (<i>P. p. orientalis</i>).</li>
  </ul>""",
  "ro": """<ul class="prose">
    <li>Ghidul a fost scris în neerlandeză; denumirile românești ale speciilor apar pe paginile speciilor.</li>
    <li><strong>Tigru:</strong> „tigrul siberian” este tigrul de Amur.</li>
    <li><strong>Leopard:</strong> leopardul nord-chinezesc de la Târgu Mureș aparține leopardului de Amur (<i>P. p. orientalis</i>).</li>
  </ul>"""},
 "verdwenen": {
  "nl": f"""<p class="prose">Bij elk park staat onder “Eerder hier” welke katten er vroeger waren. Opvallend: de jaguars van {CRA}, {BAR} en {GAL}, de luipaarden en wilde katten van {ORA}, de witte tijgers van {BRV} en {SIB} (laatst gemeld 2022) en de liger van {ARC}. De dierentuinen van Timișoara (2020) en Hunedoara (2025) sloten; de tijgers van Hunedoara wonen nu in {RES}.</p>""",
  "en": f"""<p class="prose">Each park’s page lists under “Previously here” which cats it used to have. Notable: the jaguars of {CRA}, {BAR} and {GAL}, the leopards and wildcats of {ORA}, the white tigers of {BRV} and {SIB} (last reported 2022) and the liger of {ARC}. The zoos of Timișoara (2020) and Hunedoara (2025) closed; the Hunedoara tigers now live at {RES}.</p>""",
  "ro": f"""<p class="prose">Pe pagina fiecărui parc, la „Anterior aici”, apar felinele care au trăit acolo. De remarcat: jaguarii de la {CRA}, {BAR} și {GAL}, leoparzii și pisicile sălbatice de la {ORA}, tigrii albi de la {BRV} și {SIB} (ultima mențiune în 2022) și ligrul de la {ARC}. Grădinile zoologice din Timișoara (2020) și Hunedoara (2025) s-au închis; tigrii din Hunedoara trăiesc acum la {RES}.</p>"""},
 "controle": {
  "nl": """<p class="prose"><strong>Lijsten en regels:</strong> het ANMAP-overzicht van dierentuinen, aquaria en opvangcentra (14-11-2025) en het jaarverslag 2025, de EAZA-ledenlijst (Agerpres 06-10-2025), wet 205/2004 (houden van wilde dieren), wet 171/2017 (circusverbod) en wet 138/2022.</p>
  <p class="prose"><strong>Databanken:</strong> Zootierliste (alle katachtigen, huidige en vroegere houdingen), alleen aanvullend.</p>
  <p class="prose"><strong>Websites van de parken</strong>, met dierenlijsten, soortpagina’s, adoptiepagina’s en nieuws.</p>
  <p class="prose"><strong>Nieuws:</strong> onder meer Agerpres, Digi24, Adevărul, G4Media, Radio Reșița, Monitorul de Suceava en andere regionale media.</p>""",
  "en": """<p class="prose"><strong>Lists and rules:</strong> the ANMAP overview of zoos, aquaria and rescue centres (14-11-2025) and the 2025 annual report, the EAZA member list (Agerpres 06-10-2025), Law 205/2004 (keeping wild animals), Law 171/2017 (circus ban) and Law 138/2022.</p>
  <p class="prose"><strong>Databases:</strong> Zootierliste (all cats, current and former holdings), used only as a supplement.</p>
  <p class="prose"><strong>Park websites</strong>, with animal lists, species pages, adoption pages and news.</p>
  <p class="prose"><strong>News:</strong> including Agerpres, Digi24, Adevărul, G4Media, Radio Reșița, Monitorul de Suceava and other regional media.</p>""",
  "ro": """<p class="prose"><strong>Liste și reguli:</strong> situația ANMAP a grădinilor zoologice, acvariilor și centrelor de reabilitare (14.11.2025) și raportul anual 2025, lista membrilor EAZA (Agerpres, 06.10.2025), Legea 205/2004 (deținerea animalelor sălbatice), Legea 171/2017 (interdicția din circuri) și Legea 138/2022.</p>
  <p class="prose"><strong>Baze de date:</strong> Zootierliste (toate felinele, deținători actuali și foști), doar ca sursă suplimentară.</p>
  <p class="prose"><strong>Site-urile parcurilor</strong>, cu liste de animale, pagini ale speciilor, pagini de adopție și știri.</p>
  <p class="prose"><strong>Știri:</strong> printre altele Agerpres, Digi24, Adevărul, G4Media, Radio Reșița, Monitorul de Suceava și alte publicații regionale.</p>"""},
}
