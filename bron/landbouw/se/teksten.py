# Landspecifieke tekstblokken van de Zweedse gids (NL / EN / SV). Stand 22 oktober 2026.
import re, unicodedata
def _slug(x):
    x = "".join(c for c in unicodedata.normalize("NFD", x) if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"\(.*?\)", "", x)).strip("-")
def L(naam): return f'<a href="#locatie/{_slug(naam)}">{naam}</a>'

# alleen län met locaties, van zuid naar noord
REGN = {"skane": ["Skåne", "Skåne", "Skåne län"],
        "kalmar": ["Kalmar (Öland)", "Kalmar (Öland)", "Kalmar län"],
        "vastra-gotaland": ["Västra Götaland", "Västra Götaland", "Västra Götalands län"],
        "ostergotland": ["Östergötland", "Östergötland", "Östergötlands län"],
        "sodermanland": ["Södermanland", "Södermanland", "Södermanlands län"],
        "stockholm": ["Stockholm", "Stockholm", "Stockholms län"],
        "gavleborg": ["Gävleborg", "Gävleborg", "Gävleborgs län"],
        "vasternorrland": ["Västernorrland", "Västernorrland", "Västernorrlands län"],
        "vasterbotten": ["Västerbotten", "Västerbotten", "Västerbottens län"]}

PAR, NOR, KOL, SKA, YST = L("Parken Zoo"), L("Nordens Ark"), L("Kolmårdens Djurpark"), L("Skånes Djurpark"), L("Ystad Djurpark")
BOR, OLA, SKN, VIL, LYC, JUN = L("Borås Djurpark"), L("Ölands Djurpark"), L("Skansen"), L("Vildriket"), L("Lycksele Djurpark"), L("Junsele Djurpark")

# losse vervangingen in het sjabloon (resten van Portugal in de Zweedse vaste teksten)
SV_VERV = [("i Portugal", "i Sverige"), ("I Portugal", "I Sverige"), ("portugisiska djurparker", "svenska djurparker")]
VAST = [
 (r'<p class="stamp">.*?</p>', '<p class="stamp"><span class="l-nl">Stand 22 oktober 2026</span><span class="l-en">Updated 22 October 2026</span><span class="l-sv">Uppdaterad 22 oktober 2026</span></p>'),
 (r'<p class="lede">.*?</p>', '<p class="lede">'
  '<span class="l-nl">Waar in Zweden kun je tijgers, sneeuwluipaarden, lynxen, manoels en andere wilde katten zien? Per soort en per park zie je hier welke katten er wonen, welke jongen er onlangs geboren zijn en wat er binnenkort verandert. En met welke route je alle soorten ziet.</span>'
  '<span class="l-en">Where in Sweden can you see tigers, snow leopards, lynxes, Pallas’s cats and other wild cats? By species and by park, this guide shows which cats live where, which young were born recently and what is about to change. And which route lets you see every species.</span>'
  '<span class="l-sv">Var i Sverige kan du se tigrar, snöleoparder, lodjur, manuler och andra vilda kattdjur? Per art och per park visar guiden vilka katter som bor var, vilka ungar som nyss har fötts och vad som snart ändras. Och vilken rutt som tar dig till alla arter.</span></p>'),
]

LOC_INTRO = ["Alle dierentuinen en dierenparken in Zweden waar bezoekers wilde katten kunnen zien. Tik op een stip om te zien welke katten er wonen.",
             "All zoos and animal parks in Sweden where visitors can see wild cats. Tap a dot to see which cats live there.",
             "Alla djurparker i Sverige där du kan se vilda kattdjur. Tryck på en prick för att se vilka katter som bor där."]

def tldr():
    nl = f'''<div class="l-nl">
<div class="prose">
  <ul>
    <li><strong>11 soorten bevestigd</strong> op 11 locaties: 10 dierentuinen (lid van EAZA of de Zweedse dierentuinvereniging SDF) en 1 dierenpark.</li>
    <li><strong>{PAR}</strong> heeft 6 soorten, {NOR} 5 en {KOL} 4. De Euraziatische lynx, de wilde kat van Zweden zelf, zie je in 8 parken.</li>
    <li><strong>Maar op één plek te zien:</strong> de jaguar en de vissende kat ({PAR}), de manoel ({NOR}), de serval ({YST}) en de Europese wilde kat ({SKA}).</li>
    <li><strong>Jonge katten:</strong> vier Amoertijgers in {KOL} (juni 2026; twee oudere zussen uit het voorjaar van 2025) en drie Perzische luipaarden in {NOR} (mei 2026).</li>
    <li><strong>Seizoen:</strong> de meeste parken zijn alleen van het voorjaar tot de herfst open. Het hele jaar open zijn {SKN} en {VIL}; {JUN} en {LYC} vooral in de zomer.</li>
    <li><strong>Geen particulieren en geen circussen:</strong> in Zweden mogen wilde katten niet als huisdier worden gehouden en niet in een circus optreden. Orsa Rovdjurspark is sinds 2022 dicht.</li>
  </ul>
  </div>
</div>'''
    en = f'''<div class="l-en">
<div class="prose">
  <ul>
    <li><strong>11 species confirmed</strong> at 11 locations: 10 zoos (members of EAZA or the Swedish zoo association SDF) and 1 animal park.</li>
    <li><strong>{PAR}</strong> has 6 species, {NOR} 5 and {KOL} 4. The Eurasian lynx, Sweden’s own wild cat, can be seen in 8 parks.</li>
    <li><strong>Only in one place:</strong> the jaguar and the fishing cat ({PAR}), the Pallas’s cat ({NOR}), the serval ({YST}) and the European wildcat ({SKA}).</li>
    <li><strong>Young cats:</strong> four Amur tigers at {KOL} (June 2026; two older sisters from spring 2025) and three Persian leopards at {NOR} (May 2026).</li>
    <li><strong>Season:</strong> most parks are only open from spring to autumn. {SKN} and {VIL} are open all year; {JUN} and {LYC} mainly in summer.</li>
    <li><strong>No private keepers and no circuses:</strong> in Sweden wild cats may not be kept as pets or shown in circuses. Orsa Rovdjurspark has been closed since 2022.</li>
  </ul>
  </div>
</div>'''
    sv = f'''<div class="l-sv">
<div class="prose">
  <ul>
    <li><strong>11 arter bekräftade</strong> på 11 platser: 10 zoo (med i EAZA eller Svenska Djurparksföreningen) och 1 djurpark.</li>
    <li><strong>{PAR}</strong> har 6 arter, {NOR} 5 och {KOL} 4. Lodjuret, Sveriges eget vilda kattdjur, kan du se i 8 parker.</li>
    <li><strong>Bara på ett ställe:</strong> jaguar och fiskarkatt ({PAR}), manul ({NOR}), serval ({YST}) och vildkatt ({SKA}).</li>
    <li><strong>Ungar:</strong> fyra amurtigrar på {KOL} (juni 2026; två äldre systrar från våren 2025) och tre persiska leoparder på {NOR} (maj 2026).</li>
    <li><strong>Säsong:</strong> de flesta parker har bara öppet från vår till höst. {SKN} och {VIL} har öppet hela året; {JUN} och {LYC} främst på sommaren.</li>
    <li><strong>Inga privatpersoner och inga cirkusar:</strong> i Sverige får vilda kattdjur inte hållas som sällskapsdjur eller visas på cirkus. Orsa Rovdjurspark är stängd sedan 2022.</li>
  </ul>
  </div>
</div>'''
    return nl + en + sv + "\n"

GEEN = [
 [("Dierentuinen en aquaria (EAZA of SDF) zonder katachtigen", "Zoos and aquariums (EAZA or SDF) without cats", "Djurparker och akvarier (EAZA eller SDF) utan kattdjur"),
  "Furuviksparken (Gävle), Universeum en Slottsskogens djurpark (Göteborg), Tropikariet (Helsingborg), Malmö Museer – Akvariet, Skansen-Akvariet (Stockholm), Tropicarium Kolmården, Myskoxcentrum (Härjedalen)",
  ["Furuviksparken (Gävle), Universeum and Slottsskogens djurpark (Gothenburg), Tropikariet (Helsingborg), Malmö Museer – Akvariet, Skansen-Akvariet (Stockholm), Tropicarium Kolmården, Myskoxcentrum (Härjedalen)",
   "Furuviksparken (Gävle), Universeum och Slottsskogens djurpark (Göteborg), Tropikariet (Helsingborg), Malmö Museer – Akvariet, Skansen-Akvariet (Stockholm), Tropicarium Kolmården, Myskoxcentrum (Härjedalen)"]],
 [("Gesloten", "Closed", "Stängda"),
  "Orsa Rovdjurspark (sinds november 2022; had Amoertijgers, Perzische luipaarden, sneeuwluipaarden en lynxen), Frösö Zoo (Östersund, sinds 2019; had tijgers en leeuwen), Blekinge Exotiska Värld (Karlshamn), Aquaria Vattenmuseum (Stockholm)",
  ["Orsa Rovdjurspark (since November 2022; had Amur tigers, Persian leopards, snow leopards and lynxes), Frösö Zoo (Östersund, since 2019; had tigers and lions), Blekinge Exotiska Värld (Karlshamn), Aquaria Vattenmuseum (Stockholm)",
   "Orsa Rovdjurspark (sedan november 2022; hade amurtigrar, persiska leoparder, snöleoparder och lodjur), Frösö Zoo (Östersund, sedan 2019; hade tigrar och lejon), Blekinge Exotiska Värld (Karlshamn), Aquaria Vattenmuseum (Stockholm)"]],
 [("Circussen zonder katten", "Circuses without cats", "Cirkusar utan kattdjur"),
  "Cirkus Brazil Jack, Cirkus Scott, Cirkus Saraffino, Cirkus Maximum (stopte in 2018); roofdieren zijn in Zweedse circussen verboden",
  ["Cirkus Brazil Jack, Cirkus Scott, Cirkus Saraffino, Cirkus Maximum (stopped in 2018); predators are banned in Swedish circuses",
   "Cirkus Brazil Jack, Cirkus Scott, Cirkus Saraffino, Cirkus Maximum (slutade 2018); rovdjur är förbjudna på svenska cirkusar"]],
 [("Wildparken en elandenparken zonder katachtigen", "Wildlife parks and moose parks without cats", "Viltparker och älgparker utan kattdjur"),
  "Eriksberg (Blekinge), Kosta Safaripark, Öster Malma viltpark (Nyköping), Avesta Visentpark, Moose Garden (Östersund), Wrågården (Falköping), Dalslands Moose Ranch, Gårdsjö älgpark, Värmlands Älgpark, Bisonfarmen i Gate (Hjo)",
  None],
 [("Andere dierenparken, tropenhuizen en kinderboerderijen zonder katachtigen", "Other animal parks, tropical houses and farm parks without cats", "Andra djurparker, tropikhus och 4H-gårdar utan kattdjur"),
  "Gotlands Djurpark (alleen huiskatten), Mössebergs djurpark (Falköping), Nolhaga (Alingsås), Tibro Mini-Zoo, Emaus lantgård (Uddevalla), Vårviks gård (Trollhättan), Lillskogen (Karlstad), 4H-gårdar in Karlstad en Stockholm, Kungsbyn Temapark (Västerås), Havets Hus (Lysekil), Fjärilshuset – Haga Ocean (Solna), Holmsunds Tropikhus, Tropikhuset Jönköping, Reptilcenter Malmö, High Chaparral, Fun City (Tvååker)",
  ["Gotlands Djurpark (domestic cats only), Mössebergs djurpark (Falköping), Nolhaga (Alingsås), Tibro Mini-Zoo, Emaus lantgård (Uddevalla), Vårviks gård (Trollhättan), Lillskogen (Karlstad), 4H farms in Karlstad and Stockholm, Kungsbyn Temapark (Västerås), Havets Hus (Lysekil), Fjärilshuset – Haga Ocean (Solna), Holmsunds Tropikhus, Tropikhuset Jönköping, Reptilcenter Malmö, High Chaparral, Fun City (Tvååker)",
   "Gotlands Djurpark (bara tamkatter), Mössebergs djurpark (Falköping), Nolhaga (Alingsås), Tibro Mini-Zoo, Emaus lantgård (Uddevalla), Vårviks gård (Trollhättan), Lillskogen (Karlstad), 4H-gårdar i Karlstad och Stockholm, Kungsbyn Temapark (Västerås), Havets Hus (Lysekil), Fjärilshuset – Haga Ocean (Solna), Holmsunds Tropikhus, Tropikhuset Jönköping, Reptilcenter Malmö, High Chaparral, Fun City (Tvååker)"]],
]
def geen(i):
    out = ""
    for row in GEEN:
        k, t, tr = row
        if i and tr: t = tr[i - 1]
        out += f"    <li><b>{k[i]}:</b> {t}</li>\n"
    return out

OFFICIEEL = [
 """<p>In Zweden heeft elke dierentuin een vergunning van de länsstyrelse (provincie) nodig. Er is geen openbare landelijke lijst van die vergunningen. De lijst die er het dichtst bij komt, is die van Jordbruksverket met “godkända avgränsade anläggningar” (5 oktober 2026): 16 dierentuinen en aquaria plus 5 onderzoeksinstellingen. Kleinere parken met een vergunning, zoals Junsele Djurpark, staan er niet op.</p>
    <p>Particulieren mogen geen wilde katten houden, ook geen kruisingen met huiskatten (Jordbruksverket, SJVFS 2019:15). Roofdieren, behalve honden en huiskatten, zijn in circussen verboden (Djurskyddsförordning 2019:66). Wilde katten zie je in Zweden dus alleen in dierentuinen en dierenparken.</p>
    <p>De lijst in deze gids is opgebouwd uit de lijst van Jordbruksverket, de ledenlijsten van de Svenska Djurparksföreningen (SDF, 13 Zweedse leden) en EAZA (18 Zweedse dierentuinen en aquaria), Zootierliste (alle katachtigen, huidige en vroegere houders) en een zoektocht per län naar kleinere parken, opvang en circussen.</p>
    <p>Of een park een dierentuin of een dierenpark heet, hangt in deze gids af van het lidmaatschap van EAZA of SDF.</p>
""",
 """<p>In Sweden every zoo needs a permit from the county administrative board (länsstyrelse). There is no public national list of these permits. The closest is the Swedish Board of Agriculture (Jordbruksverket) list of “approved confined establishments” (5 October 2026): 16 zoos and aquariums plus 5 research institutions. Smaller parks with a permit, such as Junsele Djurpark, are not on it.</p>
    <p>Private individuals may not keep wild cats, nor crosses with domestic cats (Jordbruksverket, SJVFS 2019:15). Predators other than dogs and domestic cats are banned in circuses (Animal Welfare Ordinance 2019:66). So in Sweden you can only see wild cats in zoos and animal parks.</p>
    <p>The list in this guide was built from the Jordbruksverket list, the member lists of the Swedish Association of Zoological Parks and Aquaria (SDF, 13 Swedish members) and EAZA (18 Swedish zoos and aquariums), Zootierliste (all cats, current and former holders) and a search county by county for smaller parks, rescue centres and circuses.</p>
    <p>Whether a park is called a zoo or an animal park in this guide depends on membership of EAZA or SDF.</p>
""",
 """<p>I Sverige behöver varje djurpark tillstånd från länsstyrelsen. Det finns ingen offentlig nationell lista över dessa tillstånd. Närmast kommer Jordbruksverkets lista över godkända avgränsade anläggningar (5 oktober 2026): 16 djurparker och akvarier plus 5 forskningsinstitutioner. Mindre parker med tillstånd, som Junsele Djurpark, finns inte med.</p>
    <p>Privatpersoner får inte hålla vilda kattdjur, inte heller korsningar med tamkatt (Jordbruksverket, SJVFS 2019:15). Rovdjur, utom hundar och tamkatter, är förbjudna på cirkus (djurskyddsförordningen 2019:66). Vilda kattdjur kan du alltså bara se i djurparker.</p>
    <p>Listan i guiden bygger på Jordbruksverkets lista, medlemslistorna från Svenska Djurparksföreningen (SDF, 13 svenska medlemmar) och EAZA (18 svenska djurparker och akvarier), Zootierliste (alla kattdjur, nuvarande och tidigare hållare) och en sökning län för län efter mindre parker, djurräddning och cirkusar.</p>
    <p>Om en park kallas zoo eller djurpark i guiden beror på medlemskap i EAZA eller SDF.</p>
"""]

ADVIES = [
 f"""<ul class="prose">
    <li><strong>Alle 11 soorten in vier parken:</strong>
      <ul>
        <li><strong>Parken Zoo</strong> (Eskilstuna): jaguar, vissende kat, leeuw, cheetah (en tijger, luipaard)</li>
        <li><strong>Nordens Ark</strong> (Hunnebostrand, ten noorden van Göteborg): manoel, sneeuwluipaard, lynx (en tijger, luipaard)</li>
        <li><strong>Skånes Djurpark</strong> (Höör): Europese wilde kat (en lynx)</li>
        <li><strong>Ystad Djurpark</strong>: serval</li>
      </ul>
    </li>
    <li><strong>Alternatieven:</strong> sneeuwluipaard en lynx zie je ook in {KOL}, de cheetah en de leeuw ook in {BOR}. Skånes Djurpark en Ystad liggen ongeveer een uur rijden uit elkaar.</li>
    <li><strong>Plan in de zomer:</strong> Parken Zoo is van november tot het voorjaar dicht, Ystad Djurpark van november tot mei. Openingstijden staan op de pagina van elk park.</li>
    <li><strong>Twijfel je over een dier?</strong> Bel of mail dan vóór je bezoek met het park. Alle onzekere vermeldingen staan onder “Over” bij “Twijfelgevallen”.</li>
  </ul>
""",
 f"""<ul class="prose">
    <li><strong>All 11 species in four parks:</strong>
      <ul>
        <li><strong>Parken Zoo</strong> (Eskilstuna): jaguar, fishing cat, lion, cheetah (and tiger, leopard)</li>
        <li><strong>Nordens Ark</strong> (Hunnebostrand, north of Gothenburg): Pallas’s cat, snow leopard, lynx (and tiger, leopard)</li>
        <li><strong>Skånes Djurpark</strong> (Höör): European wildcat (and lynx)</li>
        <li><strong>Ystad Djurpark</strong>: serval</li>
      </ul>
    </li>
    <li><strong>Alternatives:</strong> snow leopard and lynx can also be seen at {KOL}, cheetah and lion also at {BOR}. Skånes Djurpark and Ystad are about an hour’s drive apart.</li>
    <li><strong>Plan for summer:</strong> Parken Zoo is closed from November to spring, Ystad Djurpark from November to May. Opening times are on each park’s page.</li>
    <li><strong>Not sure about an animal?</strong> Call or email the park before your visit. All uncertain entries are listed under “About” in “Doubtful cases”.</li>
  </ul>
""",
 f"""<ul class="prose">
    <li><strong>Alla 11 arter i fyra parker:</strong>
      <ul>
        <li><strong>Parken Zoo</strong> (Eskilstuna): jaguar, fiskarkatt, lejon, gepard (och tiger, leopard)</li>
        <li><strong>Nordens Ark</strong> (Hunnebostrand, norr om Göteborg): manul, snöleopard, lodjur (och tiger, leopard)</li>
        <li><strong>Skånes Djurpark</strong> (Höör): vildkatt (och lodjur)</li>
        <li><strong>Ystad Djurpark</strong>: serval</li>
      </ul>
    </li>
    <li><strong>Alternativ:</strong> snöleopard och lodjur finns också på {KOL}, gepard och lejon också på {BOR}. Skånes Djurpark och Ystad ligger ungefär en timmes bilresa från varandra.</li>
    <li><strong>Planera för sommaren:</strong> Parken Zoo är stängt från november till våren, Ystad Djurpark från november till maj. Öppettider finns på varje parks sida.</li>
    <li><strong>Osäker på ett djur?</strong> Ring eller mejla parken före besöket. Alla osäkra uppgifter finns under ”Om” vid ”Osäkra fall”.</li>
  </ul>
"""]

GEPLAND = [
 f"""<ul class="prose">
    <li><strong>{PAR}:</strong> de zwarte jaguarkater Avatar is in september 2026 naar Artis (Amsterdam) verhuisd. Het park is van november tot het voorjaar dicht.</li>
    <li><strong>{NOR}:</strong> bij de Karpatische lynxkater (sinds april 2025) is een poes aangekondigd; nog niet bevestigd.</li>
    <li><strong>Seizoen voorbij:</strong> {OLA} is dicht tot 30 april 2027, {JUN} en {LYC} zijn alleen in de zomer (vrij) open.</li>
    <li><span class="st st-w"><i></i></span> <strong>Onzeker:</strong> de Amoerluipaard en de Europese wilde kat van {NOR} (zie Twijfelgevallen).</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Gepland</span> · <span class="st st-w"><i></i>Onzeker</span></p>
""",
 f"""<ul class="prose">
    <li><strong>{PAR}:</strong> the black male jaguar Avatar moved to Artis (Amsterdam) in September 2026. The park is closed from November to spring.</li>
    <li><strong>{NOR}:</strong> a female has been announced for the Carpathian lynx male (here since April 2025); not yet confirmed.</li>
    <li><strong>Season over:</strong> {OLA} is closed until 30 April 2027, {JUN} and {LYC} are only (fully) open in summer.</li>
    <li><span class="st st-w"><i></i></span> <strong>Uncertain:</strong> the Amur leopard and the European wildcat at {NOR} (see Doubtful cases).</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Planned</span> · <span class="st st-w"><i></i>Uncertain</span></p>
""",
 f"""<ul class="prose">
    <li><strong>{PAR}:</strong> den svarta jaguarhanen Avatar flyttade i september 2026 till Artis (Amsterdam). Parken är stängd från november till våren.</li>
    <li><strong>{NOR}:</strong> en hona har aviserats till den karpatiska lodjurshanen (här sedan april 2025); ännu inte bekräftat.</li>
    <li><strong>Säsongen är slut:</strong> {OLA} är stängt till 30 april 2027, {JUN} och {LYC} har bara (fullt) öppet på sommaren.</li>
    <li><span class="st st-w"><i></i></span> <strong>Osäkert:</strong> amurleoparden och vildkatten på {NOR} (se Osäkra fall).</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Planerat</span> · <span class="st st-w"><i></i>Osäkert</span></p>
"""]

def _kv(lg, titel, sp, naar, locs):
    return f'<h3>{titel} <a class="kv-sp" href="#soort/{sp}">{naar}</a></h3>\n  <ul class="prose">\n' + "".join(f"    <li>{x}</li>\n" for x in locs) + "  </ul>\n"
KV = [
 (("Witte tijger", "naar de tijger"), ("White tiger", "to the tiger"), ("Vit tiger", "till tigern"), "tijger", [JUN]),
]
KVTXT = {"nl": f"Een witte tijger heeft een recessieve mutatie in het gen SLC45A2 en is geen albino; binnen het Europese fokprogramma worden ze niet meer gefokt. {JUN} heeft twee witte tijgers en een gewone; volgens het park de enige witte tijgers van Zweden. {PAR} had vroeger witte tijgers (tot 2010) en tot september 2026 de zwarte jaguar Avatar.",
         "en": f"A white tiger has a recessive mutation in the SLC45A2 gene and is not an albino; they are no longer bred within the European breeding programme. {JUN} has two white tigers and one orange tiger; according to the park, the only white tigers in Sweden. {PAR} used to have white tigers (until 2010) and, until September 2026, the black jaguar Avatar.",
         "sv": f"En vit tiger har en recessiv mutation i genen SLC45A2 och är ingen albino; inom det europeiska avelsprogrammet föds de inte längre upp. {JUN} har två vita tigrar och en vanlig; enligt parken de enda vita tigrarna i Sverige. {PAR} hade tidigare vita tigrar (till 2010) och fram till september 2026 den svarta jaguaren Avatar."}
HYB = {"nl": "Er zijn geen lijgers, tigons of andere hybriden van wilde katten gevonden. Kruisingen van huiskatten en wilde katten (zoals savannah- en bengaalkatten tot de vierde generatie) mogen in Zweden niet particulier worden gehouden; ze tellen in deze gids niet mee.",
       "en": "No ligers, tigons or other hybrids of wild cats were found. Crosses between domestic cats and wild cats (such as Savannah and Bengal cats up to the fourth generation) may not be kept privately in Sweden; they do not count in this guide.",
       "sv": "Inga ligrar, tigoner eller andra hybrider mellan vilda kattdjur hittades. Korsningar mellan tamkatt och vilda kattdjur (som savannah- och bengalkatter till och med fjärde generationen) får inte hållas privat i Sverige; de räknas inte i guiden."}
def _kleur():
    out = ""
    for i, lg in enumerate(["nl", "en", "sv"]):
        out += f'<div class="l-{lg}">\n' + "".join(_kv(lg, k[i][0], k[3], k[i][1], k[4]) for k in KV) + f'  <p class="prose">{KVTXT[lg]}</p>\n</div>'
    out += '<h3 id="hybriden" style="font-size:22px;margin-top:30px"><span class="l-nl">Hybriden</span><span class="l-en">Hybrids</span><span class="l-sv">Hybrider</span></h3>\n'
    for lg in ["nl", "en", "sv"]:
        out += f'<div class="l-{lg}">\n<p class="prose">{HYB[lg]}</p>\n</div>'
    return out
KLEUR = _kleur()

UITLEG = {
 "werkwijze": {
  "nl": """<p class="prose">Voor alle Zweedse dierentuinen, dierenparken, wildparken, tropenhuizen, opvangcentra en circussen is nagegaan welke wilde katachtigen er te zien zijn. De basislijst komt uit de lijst van Jordbruksverket (oktober 2026), de ledenlijsten van SDF en EAZA en Zootierliste (alle katachtigen, huidige en vroegere houders); per län is daarna gezocht naar kleinere parken. Elke locatie is gecontroleerd op de eigen website, aangevuld met Zweeds nieuws. Bij elke vermelding staan de bron en de datum.</p>
  <p class="prose">Een kat telt mee als een bezoeker hem kan zien. Vrij levende lynxen (bijvoorbeeld in de bossen rond Kolmården) tellen niet mee.</p>
  <p class="prose">De indeling in soorten volgt de standaard van de IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>""",
  "en": """<p class="prose">For all Swedish zoos, animal parks, wildlife parks, tropical houses, rescue centres and circuses, we checked which wild cats can be seen. The base list comes from the Jordbruksverket list (October 2026), the member lists of SDF and EAZA, and Zootierliste (all cats, current and former holders); each county was then searched for smaller parks. Every location was checked on its own website, supplemented by Swedish news. Each entry shows its source and date.</p>
  <p class="prose">A cat counts if a visitor can see it. Free-living lynxes (for example in the forests around Kolmården) do not count.</p>
  <p class="prose">Species follow the standard of the IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>""",
  "sv": """<p class="prose">För alla svenska djurparker, viltparker, tropikhus, djurräddningar och cirkusar har vi kontrollerat vilka vilda kattdjur du kan se. Grundlistan kommer från Jordbruksverkets lista (oktober 2026), medlemslistorna från SDF och EAZA och Zootierliste (alla kattdjur, nuvarande och tidigare hållare); sedan har vi sökt efter mindre parker län för län. Varje plats har kontrollerats på sin egen webbplats, kompletterat med svenska nyheter. Varje uppgift anger källa och datum.</p>
  <p class="prose">En katt räknas om en besökare kan se den. Frilevande lodjur (till exempel i skogarna runt Kolmården) räknas inte.</p>
  <p class="prose">Indelningen i arter följer standarden från IUCN/SSC Cat Classification Task Force (Kitchener m.fl., 2017, <i>Cat News</i> Special Issue 11).</p>"""},
 "namen": {
  "nl": """<ul class="prose">
    <li><strong>Lodjur</strong> of <strong>lo</strong> is de Euraziatische lynx, <strong>snöleopard</strong> de sneeuwluipaard, <strong>gepard</strong> de cheetah en <strong>manul</strong> de manoel (Pallas’ kat).</li>
    <li><strong>Fiskarkatt</strong> is de vissende kat, <strong>vildkatt</strong> de Europese wilde kat. De wilde katten van Nordens Ark worden gefokt voor uitzetting in Schotland.</li>
    <li><strong>Leeuw:</strong> sinds 2017 zijn er twee ondersoorten: de noordelijke leeuw (<i>P. l. leo</i>), waartoe de Aziatische leeuwen van Kolmården en Parken Zoo horen, en de zuidelijke leeuw (<i>P. l. melanochaita</i>).</li>
    <li><strong>Lynx:</strong> Kolmården, Skånes Djurpark, Skansen en Vildriket houden de noordelijke (Scandinavische) lynx (<i>L. l. lynx</i>), Borås en Nordens Ark de Karpatische lynx (<i>L. l. carpathicus</i>).</li>
  </ul>""",
  "en": """<ul class="prose">
    <li><strong>Lodjur</strong> or <strong>lo</strong> is the Eurasian lynx, <strong>snöleopard</strong> the snow leopard, <strong>gepard</strong> the cheetah and <strong>manul</strong> the Pallas’s cat.</li>
    <li><strong>Fiskarkatt</strong> is the fishing cat, <strong>vildkatt</strong> the European wildcat. Nordens Ark breeds its wildcats for release in Scotland.</li>
    <li><strong>Lion:</strong> since 2017 there are two subspecies: the northern lion (<i>P. l. leo</i>), which includes the Asiatic lions of Kolmården and Parken Zoo, and the southern lion (<i>P. l. melanochaita</i>).</li>
    <li><strong>Lynx:</strong> Kolmården, Skånes Djurpark, Skansen and Vildriket keep the northern (Scandinavian) lynx (<i>L. l. lynx</i>), Borås and Nordens Ark the Carpathian lynx (<i>L. l. carpathicus</i>).</li>
  </ul>""",
  "sv": """<ul class="prose">
    <li>Guiden är skriven på nederländska; artnamnen på svenska finns på artsidorna. <strong>Lodjur</strong> heter <i>Euraziatische lynx</i> på nederländska, <strong>snöleopard</strong> <i>sneeuwluipaard</i> och <strong>manul</strong> <i>manoel</i>.</li>
    <li>Vildkatterna på Nordens Ark föds upp för utplantering i Skottland.</li>
    <li><strong>Lejon:</strong> sedan 2017 finns det två underarter: det nordliga lejonet (<i>P. l. leo</i>), dit de asiatiska lejonen på Kolmården och Parken Zoo hör, och det sydliga lejonet (<i>P. l. melanochaita</i>).</li>
    <li><strong>Lodjur:</strong> Kolmården, Skånes Djurpark, Skansen och Vildriket har det nordliga (skandinaviska) lodjuret (<i>L. l. lynx</i>), Borås och Nordens Ark det karpatiska lodjuret (<i>L. l. carpathicus</i>).</li>
  </ul>"""},
 "verdwenen": {
  "nl": f"""<p class="prose">Bij elk park staat onder “Eerder hier” welke katten er vroeger waren. Opvallend: Orsa Rovdjurspark (Amoertijgers, Perzische luipaarden, sneeuwluipaarden; dicht sinds 2022) en Frösö Zoo (tijgers en leeuwen; dicht sinds 2019). In {PAR} verdwenen de nevelpanter en de zandkat (rond 2020) en de zwarte jaguar Avatar (2026). {BOR} heeft sinds 2022 geen tijgers meer, {OLA} geen leeuwen en {KOL} ruilde in 2024 zijn Afrikaanse leeuwen voor Aziatische.</p>""",
  "en": f"""<p class="prose">Each park’s page lists under “Previously here” which cats it used to have. Notable: Orsa Rovdjurspark (Amur tigers, Persian leopards, snow leopards; closed since 2022) and Frösö Zoo (tigers and lions; closed since 2019). {PAR} lost its clouded leopard and sand cat (around 2020) and the black jaguar Avatar (2026). {BOR} has had no tigers since 2022, {OLA} no longer has lions and {KOL} replaced its African lions with Asiatic lions in 2024.</p>""",
  "sv": f"""<p class="prose">På varje parks sida står under ”Tidigare här” vilka katter som fanns där förut. Värt att nämna: Orsa Rovdjurspark (amurtigrar, persiska leoparder, snöleoparder; stängd sedan 2022) och Frösö Zoo (tigrar och lejon; stängd sedan 2019). {PAR} förlorade sin molnleopard och sandkatt (runt 2020) och den svarta jaguaren Avatar (2026). {BOR} har inte haft tigrar sedan 2022, {OLA} har inga lejon längre och {KOL} bytte 2024 sina afrikanska lejon mot asiatiska.</p>"""},
 "controle": {
  "nl": """<p class="prose"><strong>Officiële lijsten:</strong> de lijst van Jordbruksverket met goedgekeurde instellingen (05-10-2026), de ledenlijsten van SDF (29-10-2025) en EAZA (oktober 2026), de regels voor dieren in circussen (Djurskyddsförordning 2019:66) en voor het houden van wilde dieren (SJVFS 2019:15).</p>
  <p class="prose"><strong>Databanken:</strong> Zootierliste (alle katachtigen, huidige en vroegere houdingen), alleen aanvullend.</p>
  <p class="prose"><strong>Websites van de parken</strong>, met dierenlijsten, soortpagina’s, parkkaarten, kalenders en nieuws.</p>
  <p class="prose"><strong>Nieuws:</strong> onder meer SVT, Sveriges Radio, NT, BT en regionale nieuwssites.</p>""",
  "en": """<p class="prose"><strong>Official lists:</strong> the Jordbruksverket list of approved establishments (05-10-2026), the member lists of SDF (29-10-2025) and EAZA (October 2026), the rules on animals in circuses (Animal Welfare Ordinance 2019:66) and on keeping wild animals (SJVFS 2019:15).</p>
  <p class="prose"><strong>Databases:</strong> Zootierliste (all cats, current and former holdings), used only as a supplement.</p>
  <p class="prose"><strong>Park websites</strong>, with animal lists, species pages, park maps, calendars and news.</p>
  <p class="prose"><strong>News:</strong> including SVT, Sveriges Radio, NT, BT and regional news sites.</p>""",
  "sv": """<p class="prose"><strong>Officiella listor:</strong> Jordbruksverkets lista över godkända anläggningar (05-10-2026), medlemslistorna från SDF (29-10-2025) och EAZA (oktober 2026), reglerna för djur på cirkus (djurskyddsförordningen 2019:66) och för att hålla vilda djur (SJVFS 2019:15).</p>
  <p class="prose"><strong>Databaser:</strong> Zootierliste (alla kattdjur, nuvarande och tidigare hållare), bara som komplement.</p>
  <p class="prose"><strong>Parkernas webbplatser</strong> med djurlistor, artsidor, parkkartor, kalendrar och nyheter.</p>
  <p class="prose"><strong>Nyheter:</strong> bland annat SVT, Sveriges Radio, NT, BT och regionala nyhetssajter.</p>"""},
}
