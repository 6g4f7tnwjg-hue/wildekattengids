# Landspecifieke tekstblokken van de Deense gids (NL / EN / DA). Stand 22 oktober 2026.

REGN = {"nordjylland": ["Noord-Jutland", "North Jutland", "Nordjylland"],
        "midtjylland": ["Midden-Jutland", "Central Jutland", "Midtjylland"],
        "syddanmark": ["Zuid-Denemarken", "Southern Denmark", "Syddanmark"],
        "sjaelland": ["Seeland", "Zealand", "Sjælland"],
        "hovedstaden": ["Hoofdstadregio", "Capital Region", "Hovedstaden"]}

def L(href, naam): return f'<a href="#locatie/{href}">{naam}</a>'
KBH = L("zoo-koebenhavn", "Zoo København"); REE = L("ree-park", "Ree Park"); RAN = L("randers-regnskov", "Randers Regnskov")
KRO = L("krokodille-zoo", "Krokodille Zoo"); SKA = L("skaerup-zoo", "Skærup Zoo"); ODS = L("odsherred-zoo-rescue", "Odsherred Zoo Rescue")
GIV = L("givskud-zoo-zootopia", "Givskud Zoo – Zootopia"); BLA = L("blavand-zoo", "Blåvand Zoo"); AAL = L("aalborg-zoo", "Aalborg Zoo")
ODE = L("odense-zoo", "Odense Zoo"); KNU = L("knuthenborg-safaripark", "Knuthenborg Safaripark"); JYL = L("jyllands-park-zoo", "Jyllands Park Zoo")
MUN = L("munkholm-zoo", "Munkholm Zoo"); ZPS = L("zoopark-sydsjaelland", "Zoopark Sydsjælland"); HAN = L("hansenberg-zoo", "Hansenberg Zoo")
GLA = L("glad-zoo", "Glad Zoo"); PAN = L("pangea-park-falster", "Pangea Park Falster")

def sp3(nl, en, da): return [nl, en, da]
VAST = [
 (r'<p class="stamp">.*?</p>', '<p class="stamp"><span class="l-nl">Stand 22 oktober 2026</span><span class="l-en">Updated 22 October 2026</span><span class="l-da">Opdateret 22. oktober 2026</span></p>'),
 (r'<span class="l-da">i portugisiske dyreparker og zoologiske haver</span>', '<span class="l-da">i danske dyreparker og zoologiske haver</span>'),
 (r'<p class="lede">.*?</p>', '<p class="lede">'
  '<span class="l-nl">Waar in Denemarken kun je leeuwen, tijgers, jaguars, poema’s en andere wilde katten zien? Per soort en per park zie je hier welke katten er wonen, welke jongen er onlangs geboren zijn en wat er binnenkort verandert. En met welke route je alle soorten ziet.</span>'
  '<span class="l-en">Where in Denmark can you see lions, tigers, jaguars, pumas and other wild cats? By species and by park, this guide shows which cats live where, which young were born recently and what is about to change. And which route lets you see every species.</span>'
  '<span class="l-da">Hvor i Danmark kan du se løver, tigre, jaguarer, pumaer og andre vilde kattedyr? Art for art og park for park viser guiden, hvilke katte der bor hvor, hvilke unger der er født for nylig, og hvad der snart ændrer sig. Og hvilken rute du skal tage for at se alle arterne.</span></p>'),
]

LOC_INTRO = ["Alle dierentuinen, dierenparken, safariparken en opvangcentra in Denemarken waar bezoekers wilde katten kunnen zien. Tik op een stip om te zien welke katten er wonen.",
             "All zoos, animal parks, safari parks and rescue centres in Denmark where visitors can see wild cats. Tap a dot to see which cats live there.",
             "Alle zoologiske haver, dyreparker, safariparker og redningscentre i Danmark, hvor besøgende kan se vilde kattedyr. Tryk på en prik for at se, hvilke katte der bor der."]

def tldr():
    nl = f'''<div class="l-nl">
<div class="prose">
  <ul>
    <li><strong>15 soorten bevestigd</strong> op 15 locaties: 4 dierentuinen, 3 safariparken, 7 dierenparken en 1 opvangcentrum. Daarnaast twee locaties met alleen onzekere of niet vrij te bezoeken katten.</li>
    <li><strong>{REE}</strong> heeft de meeste soorten (5): leeuw, luipaard, cheetah, vissende kat en zandkat. De cheetah, de vissende kat en de zandkat zie je in Denemarken alleen hier.</li>
    <li><strong>Maar op één plek te zien:</strong> nevelpanter en poema in {KRO} (de enige poema’s van Denemarken), ocelot en rode lynx in {SKA}, margay in {RAN}.</li>
    <li><strong>Jonge katten:</strong> een Amoerpanter in {KBH} (september 2026), acht leeuwenwelpen in {GIV} (mei en juni 2026), twee zwarte jaguars in {RAN} (februari 2026), twee jonge Amoertijgers in {KBH} (juli 2025) en leeuwenwelpen uit 2025 in {REE}, {ODE} en {BLA} (witte leeuwen).</li>
    <li><strong>Veel parken zijn in de winter dicht</strong> of alleen in het weekend open, zoals {REE}, {ODS}, {JYL} en {SKA}. Kijk vóór je bezoek bij “Openingstijden”.</li>
    <li><strong>Geen circussen en geen particulieren:</strong> wilde katten in circussen zijn al sinds 1962 verboden en particulieren mogen geen roofdieren houden. Opvang voor in beslag genomen katten (servals, caracals) is er in {ODS}.</li>
  </ul>
  </div>
</div>'''
    en = f'''<div class="l-en">
<div class="prose">
  <ul>
    <li><strong>15 species confirmed</strong> at 15 locations: 4 zoos, 3 safari parks, 7 animal parks and 1 rescue centre. In addition, two locations with only uncertain cats or cats not freely open to visitors.</li>
    <li><strong>{REE}</strong> has the most species (5): lion, leopard, cheetah, fishing cat and sand cat. The cheetah, fishing cat and sand cat can only be seen here in Denmark.</li>
    <li><strong>Only in one place:</strong> clouded leopard and puma at {KRO} (Denmark’s only pumas), ocelot and bobcat at {SKA}, margay at {RAN}.</li>
    <li><strong>Young cats:</strong> an Amur leopard at {KBH} (September 2026), eight lion cubs at {GIV} (May and June 2026), two black jaguars at {RAN} (February 2026), two young Amur tigers at {KBH} (July 2025) and lion cubs from 2025 at {REE}, {ODE} and {BLA} (white lions).</li>
    <li><strong>Many parks close in winter</strong> or only open at weekends, such as {REE}, {ODS}, {JYL} and {SKA}. Check “Opening times” before you go.</li>
    <li><strong>No circuses and no private keepers:</strong> wild cats in circuses have been banned since 1962 and private individuals may not keep carnivores. Confiscated cats (servals, caracals) are cared for at {ODS}.</li>
  </ul>
  </div>
</div>'''
    da = f'''<div class="l-da">
<div class="prose">
  <ul>
    <li><strong>15 arter bekræftet</strong> på 15 steder: 4 zoologiske haver, 3 safariparker, 7 dyreparker og 1 redningscenter. Dertil to steder med kun usikre katte eller katte, der ikke frit kan ses af publikum.</li>
    <li><strong>{REE}</strong> har flest arter (5): løve, leopard, gepard, fiskekat og sandkat. Gepard, fiskekat og sandkat kan du kun se her i Danmark.</li>
    <li><strong>Kun ét sted:</strong> træleopard og puma i {KRO} (Danmarks eneste pumaer), ozelot og rødlos i {SKA}, margay i {RAN}.</li>
    <li><strong>Unger:</strong> en amurleopard i {KBH} (september 2026), otte løveunger i {GIV} (maj og juni 2026), to sorte jaguarer i {RAN} (februar 2026), to unge amurtigre i {KBH} (juli 2025) og løveunger fra 2025 i {REE}, {ODE} og {BLA} (hvide løver).</li>
    <li><strong>Mange parker er lukket om vinteren</strong> eller kun åbne i weekenden, f.eks. {REE}, {ODS}, {JYL} og {SKA}. Tjek “Åbningstider” før dit besøg.</li>
    <li><strong>Ingen cirkus og ingen private:</strong> vilde kattedyr i cirkus har været forbudt siden 1962, og private må ikke holde rovdyr. Konfiskerede katte (servaler, karakaler) får et hjem i {ODS}.</li>
  </ul>
  </div>
</div>'''
    return nl + en + da + "\n"

GEEN = [
 [("Officieel erkend, geen katachtigen", "Officially approved, no cats", "Officielt godkendt, ingen kattedyr"),
  "Brændesgårdshaven (Svaneke, Bornholm), Danmarks Fugle Zoo (Tommerup), Den Blå Planet (Kastrup), Fiskeri- og Søfartsmuseet (Esbjerg), Fjord&Bælt (Kerteminde), Jesperhus JungleZoo (Nykøbing Mors), Kattegatcentret (Grenaa), Legoland (Billund), NaturBornholm (Aakirkeby), Nordsøen Oceanarium (Hirtshals), Orøstrand (Orø), Skandinavisk Dyrepark (Kolind), Terrariet (Vissenbjerg), AQUA Akvarium & Dyrepark (Silkeborg)"],
 [("Vroeger katachtigen, nu niet meer", "Cats in the past, not any more", "Tidligere kattedyr, ikke længere"),
  "Nordisk Dyrepark (Hobro; vroeger serval, nu alleen huiskatten van het ras lykoi)"],
 [("Gesloten", "Closed", "Lukket"), "Hillerød Mini Zoo (Hillerød; door de gemeente gesloten)"],
 [("Andere dierenparken en kinderboerderijen zonder katachtigen", "Other animal parks and farm parks without cats", "Andre dyreparker og bondegårde uden kattedyr"),
  "Pangea Park Sjælland (Bjæverskov), Øens Dyr (Masnedø), Filskov Mini Zoo (Filskov), Minidyrehaven Ribelund (Ribe), Klokkerholm Dyrepark (Hjallerup), Farm Fun (Ålbæk), Nymarksminde (Vodskov), Fun-Park Hirtshals (Hirtshals), Hjortdal Dyrefarm (Fjerritslev), Family Farm Fun Park (Løkken), Klithusegården (Skallerup)"],
 [("Attractieparken zonder dieren", "Theme parks without animals", "Forlystelsesparker uden dyr"),
  "BonBon-Land (Holme-Olstrup), Djurs Sommerland (Nimtofte), Fårup Sommerland (Blokhus), Lalandia (Billund), Sommerland Sjælland (Nørre Asmindrup)"],
 [("Roofvogels, aquaria en natuurcentra", "Birds of prey, aquariums and nature centres", "Rovfugle, akvarier og naturcentre"),
  "Bornholms Rovfugleshow (Rønne), Bornholms Sommerfuglepark (Nexø), EagleWorld (Bindslev), Falkecenter Samsø, Lille Vildmosecentret (Dokkedal; vrij levende elanden), Naturama (Svendborg), Øresundsakvariet (Helsingør)"],
 [("Hertenparken (alleen vrij levende herten)", "Deer parks (free-living deer only)", "Dyrehaver (kun fritlevende hjorte)"),
  "Jægersborg Dyrehave (Klampenborg), Marselisborg Dyrehave (Aarhus), Haderslev Dyrehave, Dyrehaven i Nørreskoven (Esbjerg)"],
 [("Circussen", "Circuses", "Cirkus"), "Cirkus Arena, Cirkus Benneweis, Cirkus Dannebrog, Cirkus Trapez e.a.: geen wilde katten (verboden sinds 1962)"],
]
GEEN_VERT = {  # vertaling van de toevoegingen tussen haakjes
 "Nordisk Dyrepark (Hobro; vroeger serval, nu alleen huiskatten van het ras lykoi)": ["Nordisk Dyrepark (Hobro; formerly serval, now only domestic cats of the Lykoi breed)", "Nordisk Dyrepark (Hobro; tidligere serval, nu kun huskatte af racen lykoi)"],
 "Hillerød Mini Zoo (Hillerød; door de gemeente gesloten)": ["Hillerød Mini Zoo (Hillerød; closed by the municipality)", "Hillerød Mini Zoo (Hillerød; lukket af kommunen)"],
 "Cirkus Arena, Cirkus Benneweis, Cirkus Dannebrog, Cirkus Trapez e.a.: geen wilde katten (verboden sinds 1962)": ["Cirkus Arena, Cirkus Benneweis, Cirkus Dannebrog, Cirkus Trapez and others: no wild cats (banned since 1962)", "Cirkus Arena, Cirkus Benneweis, Cirkus Dannebrog, Cirkus Trapez m.fl.: ingen vilde kattedyr (forbudt siden 1962)"],
}
def geen(i):
    out = ""
    for (k, t) in GEEN:
        if i and t in GEEN_VERT: t = GEEN_VERT[t][i - 1]
        elif i: t = t.replace("Falkecenter Samsø", "Falkecenter Samsø").replace("vrij levende elanden", ["free-living elk", "fritlevende elge"][i - 1])
        out += f"    <li><b>{k[i]}:</b> {t}</li>\n"
    return out

OFFICIEEL = [
 """<p>In Denemarken heeft elke dierentuin een vergunning van de Fødevarestyrelsen (Deense voedsel- en warenautoriteit) nodig. Particulieren mogen geen roofdieren houden (bekendmaking nr. 1261 van 2015), met uitzondering van hond en kat; erkende dierentuinen zijn daarvan uitgezonderd.</p>
    <p>De Fødevarestyrelsen publiceert een lijst “Godkendte zoologiske anlæg” met 31 erkende dierentuinen (bijgewerkt oktober 2026). Formeel is dat de lijst voor de handel in dieren binnen de EU; kleinere dierenparken kunnen er dus op ontbreken (zo staat Nordisk Dyrepark er niet op).</p>
    <p>De lijst in deze gids is daarom opgebouwd uit die officiële lijst, de ledenlijsten van DAZA (de Deense dierentuinvereniging, 15 leden) en EAZA (12 Deense leden), Zootierliste (alle katachtigen, huidige en vroegere houders) en een zoektocht per regio. Alle 31 erkende dierentuinen zijn nagelopen.</p>
    <p>Of een park een dierentuin of een dierenpark heet, hangt in deze gids af van het lidmaatschap van EAZA of DAZA. Safariparken en opvangcentra houden hun eigen type.</p>
""",
 """<p>In Denmark every zoo needs a licence from the Danish Veterinary and Food Administration (Fødevarestyrelsen). Private individuals may not keep carnivores other than dogs and cats (executive order no. 1261 of 2015); approved zoos are exempt.</p>
    <p>The Fødevarestyrelsen publishes a list “Godkendte zoologiske anlæg” with 31 approved zoos (updated October 2026). Formally this is the list for trade in animals within the EU, so smaller animal parks may be missing from it (Nordisk Dyrepark, for example, is not on it).</p>
    <p>The list in this guide was therefore built from that official list, the member lists of DAZA (the Danish zoo association, 15 members) and EAZA (12 Danish members), Zootierliste (all cats, current and former holders) and a search region by region. All 31 approved zoos were checked.</p>
    <p>Whether a park is called a zoo or an animal park in this guide depends on membership of EAZA or DAZA. Safari parks and rescue centres keep their own type.</p>
""",
 """<p>I Danmark skal enhver zoologisk have have tilladelse fra Fødevarestyrelsen. Private må ikke holde rovdyr bortset fra hund og kat (bekendtgørelse nr. 1261 af 2015); godkendte zoologiske anlæg er undtaget.</p>
    <p>Fødevarestyrelsen offentliggør en liste over “Godkendte zoologiske anlæg” med 31 anlæg (opdateret oktober 2026). Formelt er det listen til handel med dyr inden for EU, så mindre dyreparker kan mangle på den (Nordisk Dyrepark står for eksempel ikke på den).</p>
    <p>Listen i denne guide er derfor bygget op af den officielle liste, medlemslisterne fra DAZA (Danske Zoologiske Haver og Akvarier, 15 medlemmer) og EAZA (12 danske medlemmer), Zootierliste (alle kattedyr, nuværende og tidligere holdere) og en søgning region for region. Alle 31 godkendte anlæg er gennemgået.</p>
    <p>Om en park kaldes zoologisk have eller dyrepark i denne guide, afhænger af medlemskab af EAZA eller DAZA. Safariparker og redningscentre beholder deres egen type.</p>
"""]

ADVIES = [
 f"""<ul class="prose">
    <li><strong>Alle 15 soorten in zes parken:</strong>
      <ul>
        <li><strong>Zoo København</strong> (Kopenhagen): tijger, luipaard, leeuw</li>
        <li><strong>Odsherred Zoo Rescue</strong> (Asnæs, Seeland): caracal, serval, Euraziatische lynx</li>
        <li><strong>Krokodille Zoo</strong> (Eskilstrup, Falster): nevelpanter, poema</li>
        <li><strong>Skærup Zoo</strong> (bij Vejle): jaguar, ocelot, rode lynx</li>
        <li><strong>Ree Park</strong> (Ebeltoft): cheetah, vissende kat, zandkat (en leeuw, luipaard)</li>
        <li><strong>Randers Regnskov</strong> (Randers): margay (en jaguar, Euraziatische lynx)</li>
      </ul>
    </li>
    <li><strong>Alternatieven:</strong> de caracal zie je ook in {JYL} (dan blijf je in Jutland), de tijger ook in {AAL}, {ODE} en {KNU}.</li>
    <li><strong>Let op de seizoenen:</strong> {REE} is in de winter alleen in de kerstweekenden open, {ODS} gaat pas met Pasen weer open en {SKA} sluit begin november. {KRO} is buiten de vakanties alleen van vrijdag tot en met zondag open. Plan een rondreis dus tussen april en oktober.</li>
    <li><strong>Openingstijden</strong> staan op de pagina van elk park.</li>
    <li><strong>Twijfel je over een dier?</strong> Bel of mail dan vóór je bezoek met het park. Alle onzekere vermeldingen staan onder “Over” bij “Twijfelgevallen”.</li>
  </ul>
""",
 f"""<ul class="prose">
    <li><strong>All 15 species in six parks:</strong>
      <ul>
        <li><strong>Zoo København</strong> (Copenhagen): tiger, leopard, lion</li>
        <li><strong>Odsherred Zoo Rescue</strong> (Asnæs, Zealand): caracal, serval, Eurasian lynx</li>
        <li><strong>Krokodille Zoo</strong> (Eskilstrup, Falster): clouded leopard, puma</li>
        <li><strong>Skærup Zoo</strong> (near Vejle): jaguar, ocelot, bobcat</li>
        <li><strong>Ree Park</strong> (Ebeltoft): cheetah, fishing cat, sand cat (and lion, leopard)</li>
        <li><strong>Randers Regnskov</strong> (Randers): margay (and jaguar, Eurasian lynx)</li>
      </ul>
    </li>
    <li><strong>Alternatives:</strong> the caracal can also be seen at {JYL} (so you stay in Jutland), the tiger also at {AAL}, {ODE} and {KNU}.</li>
    <li><strong>Mind the seasons:</strong> in winter {REE} only opens on the Christmas weekends, {ODS} does not reopen until Easter and {SKA} closes in early November. Outside the school holidays {KRO} is only open from Friday to Sunday. So plan a tour between April and October.</li>
    <li><strong>Opening times</strong> are on each park’s page.</li>
    <li><strong>Not sure about an animal?</strong> Call or email the park before your visit. All uncertain entries are listed under “About” in “Doubtful cases”.</li>
  </ul>
""",
 f"""<ul class="prose">
    <li><strong>Alle 15 arter i seks parker:</strong>
      <ul>
        <li><strong>Zoo København</strong> (København): tiger, leopard, løve</li>
        <li><strong>Odsherred Zoo Rescue</strong> (Asnæs, Sjælland): karakal, serval, europæisk los</li>
        <li><strong>Krokodille Zoo</strong> (Eskilstrup, Falster): træleopard, puma</li>
        <li><strong>Skærup Zoo</strong> (ved Vejle): jaguar, ozelot, rødlos</li>
        <li><strong>Ree Park</strong> (Ebeltoft): gepard, fiskekat, sandkat (samt løve, leopard)</li>
        <li><strong>Randers Regnskov</strong> (Randers): margay (samt jaguar, europæisk los)</li>
      </ul>
    </li>
    <li><strong>Alternativer:</strong> karakal kan også ses i {JYL} (så bliver du i Jylland), tiger også i {AAL}, {ODE} og {KNU}.</li>
    <li><strong>Hold øje med sæsonerne:</strong> {REE} har om vinteren kun åbent i juleweekenderne, {ODS} åbner først igen til påske, og {SKA} lukker i starten af november. Uden for ferierne har {KRO} kun åbent fredag til søndag. Planlæg derfor en rundtur mellem april og oktober.</li>
    <li><strong>Åbningstider</strong> står på siden for hver park.</li>
    <li><strong>I tvivl om et dyr?</strong> Ring eller skriv til parken før dit besøg. Alle usikre registreringer står under “Om” i “Tvivlstilfælde”.</li>
  </ul>
"""]

GEPLAND = [
 f"""<ul class="prose">
    <li><strong>{AAL}:</strong> een nieuw, veel groter leeuwenverblijf was op 24–25 oktober 2026 leeg te bezichtigen; de Aziatische leeuwen verhuizen er daarna heen. De Sumatraanse tijgers krijgen dan het oude leeuwenverblijf.</li>
    <li><strong>{KBH}:</strong> het jonge Amoerpanter (geboren 23 september 2026) is naar verwachting vanaf eind november te zien. De savanne wordt van eind oktober tot half december 2026 opgeknapt.</li>
    <li><strong>{ODE}:</strong> het project “Fantastiske Asien” (aangekondigd juni 2026) maakt het tijgerverblijf groter.</li>
    <li><strong>{KNU}:</strong> een nieuw leeuwengebied van ongeveer 40.000 m² is in aanbouw.</li>
    <li><span class="st st-w"><i></i></span> <strong>{ZPS}:</strong> niet duidelijk of het park open is en of er nog tijgers en een lynx zijn; de bronnen uit 2026 spreken elkaar tegen.</li>
    <li><strong>Winterstop:</strong> {REE} (open op 5–6, 12–13 en 19–20 december), {ODS} (tot Pasen 2027), {JYL} (tot Palmzondag 2027), {SKA} (na 8 november), {MUN} (na 1 november). {HAN} is alleen op de open dag te bezoeken (23 januari 2027).</li>
  </ul>
  <p class="tlegend"><span class="st st-w"><i></i>Onzeker</span></p>
""",
 f"""<ul class="prose">
    <li><strong>{AAL}:</strong> a new, much larger lion house could be viewed empty on 24–25 October 2026; the Asiatic lions will move in afterwards. The Sumatran tigers will then get the old lion enclosure.</li>
    <li><strong>{KBH}:</strong> the young Amur leopard (born 23 September 2026) is expected to be on view from late November. The savannah is being renovated from late October to mid-December 2026.</li>
    <li><strong>{ODE}:</strong> the “Fantastiske Asien” project (announced June 2026) will enlarge the tiger enclosure.</li>
    <li><strong>{KNU}:</strong> a new lion area of about 40,000 m² is being built.</li>
    <li><span class="st st-w"><i></i></span> <strong>{ZPS}:</strong> unclear whether the park is open and whether it still has tigers and a lynx; the 2026 sources contradict each other.</li>
    <li><strong>Winter closure:</strong> {REE} (open on 5–6, 12–13 and 19–20 December), {ODS} (until Easter 2027), {JYL} (until Palm Sunday 2027), {SKA} (after 8 November), {MUN} (after 1 November). {HAN} can only be visited on its open day (23 January 2027).</li>
  </ul>
  <p class="tlegend"><span class="st st-w"><i></i>Uncertain</span></p>
""",
 f"""<ul class="prose">
    <li><strong>{AAL}:</strong> et nyt og meget større løveanlæg kunne ses tomt den 24.–25. oktober 2026; de asiatiske løver flytter ind bagefter. Sumatratigrene får derefter det gamle løveanlæg.</li>
    <li><strong>{KBH}:</strong> den unge amurleopard (født 23. september 2026) ventes at kunne ses fra slutningen af november. Savannen bliver renoveret fra slutningen af oktober til midten af december 2026.</li>
    <li><strong>{ODE}:</strong> projektet “Fantastiske Asien” (annonceret juni 2026) gør tigeranlægget større.</li>
    <li><strong>{KNU}:</strong> et nyt løveområde på omkring 40.000 m² er under opførelse.</li>
    <li><span class="st st-w"><i></i></span> <strong>{ZPS}:</strong> uklart, om parken er åben, og om der stadig er tigre og en los; kilderne fra 2026 modsiger hinanden.</li>
    <li><strong>Vinterlukning:</strong> {REE} (åbent 5.–6., 12.–13. og 19.–20. december), {ODS} (indtil påske 2027), {JYL} (indtil palmesøndag 2027), {SKA} (efter 8. november), {MUN} (efter 1. november). {HAN} kan kun besøges på sin åbent hus-dag (23. januar 2027).</li>
  </ul>
  <p class="tlegend"><span class="st st-w"><i></i>Usikker</span></p>
"""]

def kv(nl, en, da, sp, locs, t):
    h = {"nl": f'<h3>{nl} <a class="kv-sp" href="#soort/{sp}">naar de {t[0]}</a></h3>', "en": f'<h3>{en} <a class="kv-sp" href="#soort/{sp}">to the {t[1]}</a></h3>', "da": f'<h3>{da} <a class="kv-sp" href="#soort/{sp}">til {t[2]}</a></h3>'}
    ul = "  <ul class=\"prose\">\n" + "".join(f"    <li>{x}</li>\n" for x in locs) + "  </ul>\n"
    return h, ul
KV = [("Witte leeuw", "White lion", "Hvid løve", "leeuw", [BLA], ("leeuw", "lion", "løven")),
      ("Zwarte jaguar", "Black jaguar", "Sort jaguar", "jaguar", [RAN, SKA], ("jaguar", "jaguar", "jaguaren"))]
KVTXT = {"nl": "Een witte leeuw heeft leucisme (geen albinisme): hij heeft wel gekleurde ogen. Bij de jaguar komt zwart (melanisme) door een dominant gen; in Randers zijn moeder Chica en haar welpen uit 2026 zwart, in Skærup de kater. Of er bij {ZPS} nog een witte tijger is, is onzeker.",
         "en": "A white lion has leucism (not albinism): its eyes are coloured. In jaguars, black colouring (melanism) is caused by a dominant gene; in Randers mother Chica and her 2026 cubs are black, in Skærup the male. Whether {ZPS} still has a white tiger is uncertain.",
         "da": "En hvid løve har leucisme (ikke albinisme): øjnene har farve. Hos jaguaren skyldes sort farve (melanisme) et dominant gen; i Randers er moren Chica og hendes unger fra 2026 sorte, i Skærup hannen. Om {ZPS} stadig har en hvid tiger, er usikkert."}
HYB = {"nl": "Er zijn geen lijgers, tigons of andere hybriden van wilde katten gevonden. Kruisingen van huiskatten met wilde katten (zoals savannah- of bengaalkatten) tellen in deze gids niet mee en zijn in de parken niet gevonden.",
       "en": "No ligers, tigons or other hybrids of wild cats were found. Crosses of domestic cats with wild cats (such as Savannah or Bengal cats) do not count in this guide, and none were found in the parks.",
       "da": "Der er ikke fundet ligere, tigoner eller andre hybrider af vilde kattedyr. Krydsninger mellem huskatte og vilde katte (som savannah- eller bengalkatte) tæller ikke med i denne guide og er ikke fundet i parkerne."}
def _kleur():
    out = ""
    for lg in ["nl", "en", "da"]:
        out += f'<div class="l-{lg}">\n'
        for nl, en, da, sp, locs, t in KV:
            h, ul = kv(nl, en, da, sp, locs, t); out += h[lg] + "\n" + ul
        out += f'  <p class="prose">{KVTXT[lg].replace("{ZPS}", ZPS)}</p>\n</div>'
    out += '<h3 id="hybriden" style="font-size:22px;margin-top:30px"><span class="l-nl">Hybriden</span><span class="l-en">Hybrids</span><span class="l-da">Hybrider</span></h3>\n'
    for lg in ["nl", "en", "da"]:
        out += f'<div class="l-{lg}">\n<p class="prose">{HYB[lg]}</p>\n</div>'
    return out
KLEUR = _kleur()

UITLEG = {
 "werkwijze": {
  "nl": """<p class="prose">Voor alle Deense dierentuinen, dierenparken, safariparken en opvangcentra is nagegaan welke wilde katachtigen er te zien zijn. De basislijst komt uit de lijst van erkende dierentuinen van de Fødevarestyrelsen (31 locaties, oktober 2026), de ledenlijsten van DAZA en EAZA en Zootierliste (alle katachtigen, huidige en vroegere houders); per regio is daarna gezocht naar kleinere dierenparken en opvang met katten. Elke locatie is gecontroleerd op de eigen website, aangevuld met Deens nieuws. Bij elke vermelding staan de bron en de datum.</p>
  <p class="prose">Een kat telt mee als een bezoeker hem kan zien, ook als dat maar op bepaalde dagen kan. Opvangcentra tellen dus ook mee. Wilde katten in circussen zijn in Denemarken al sinds 1962 verboden en particulieren mogen geen roofdieren houden (bekendmaking 1261/2015); er is geen circus of particuliere houder gevonden waar bezoekers katten kunnen zien.</p>
  <p class="prose">De indeling in soorten volgt de standaard van de IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>""",
  "en": """<p class="prose">For all Danish zoos, animal parks, safari parks and rescue centres, we checked which wild cats can be seen. The base list comes from the Fødevarestyrelsen list of approved zoos (31 locations, October 2026), the member lists of DAZA and EAZA, and Zootierliste (all cats, current and former holders); each region was then searched for smaller animal parks and rescue centres with cats. Every location was checked on its own website, supplemented by Danish news. Each entry gives the source and the date.</p>
  <p class="prose">A cat counts if a visitor can see it, even if only on certain days. Rescue centres therefore count as well. Wild cats in circuses have been banned in Denmark since 1962, and private individuals may not keep carnivores (executive order 1261/2015); no circus or private keeper was found where visitors can see cats.</p>
  <p class="prose">Species follow the standard of the IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>""",
  "da": """<p class="prose">For alle danske zoologiske haver, dyreparker, safariparker og redningscentre er det undersøgt, hvilke vilde kattedyr man kan se. Grundlisten stammer fra Fødevarestyrelsens liste over godkendte zoologiske anlæg (31 steder, oktober 2026), medlemslisterne fra DAZA og EAZA og Zootierliste (alle kattedyr, nuværende og tidligere holdere); derefter er der søgt region for region efter mindre dyreparker og redningscentre med katte. Hvert sted er kontrolleret på dets egen hjemmeside, suppleret med danske nyheder. Ved hver registrering står kilde og dato.</p>
  <p class="prose">En kat tæller med, hvis en besøgende kan se den, også selvom det kun er på bestemte dage. Redningscentre tæller derfor også med. Vilde kattedyr i cirkus har været forbudt i Danmark siden 1962, og private må ikke holde rovdyr (bekendtgørelse 1261/2015); der er ikke fundet noget cirkus eller nogen privat holder, hvor besøgende kan se katte.</p>
  <p class="prose">Inddelingen i arter følger standarden fra IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>"""},
 "namen": {
  "nl": """<ul class="prose">
    <li><strong>Los</strong> is de lynx: <strong>europæisk los</strong> de Euraziatische lynx, <strong>rødlos</strong> de rode lynx. <strong>Karakal</strong> is de caracal (vroeger ook “woestijnlynx”, maar geen echte lynx).</li>
    <li><strong>Gepard</strong> is de cheetah, <strong>træleopard</strong> de nevelpanter, <strong>fiskekat</strong> de vissende kat en <strong>ozelot</strong> de ocelot.</li>
    <li><strong>Sibirisk tiger</strong> is de Amoertijger; <strong>amurleopard</strong> (in Kopenhagen) de Amoerpanter. De <strong>nordkinesiske leopard</strong> van Ree Park hoort volgens de indeling van 2017 ook bij <i>P. p. orientalis</i>.</li>
    <li><strong>Leeuw:</strong> sinds 2017 zijn er twee ondersoorten: de noordelijke leeuw (<i>P. l. leo</i>), waartoe de Aziatische leeuw van Aalborg hoort, en de zuidelijke leeuw (<i>P. l. melanochaita</i>), waartoe de Angola-leeuwen horen. De witte leeuwen van Blåvand zijn van zuidelijke afkomst.</li>
    <li><strong>Vrij levende wilde katten</strong> vallen buiten dit overzicht. De Europese wilde kat is in Denemarken niet vastgesteld; in de herfst van 2025 wel in Sleeswijk-Holstein, net over de grens.</li>
  </ul>""",
  "en": """<ul class="prose">
    <li><strong>Los</strong> is the lynx: <strong>europæisk los</strong> the Eurasian lynx, <strong>rødlos</strong> the bobcat. <strong>Karakal</strong> is the caracal (sometimes called “desert lynx”, but not a true lynx).</li>
    <li><strong>Gepard</strong> is the cheetah, <strong>træleopard</strong> the clouded leopard, <strong>fiskekat</strong> the fishing cat and <strong>ozelot</strong> the ocelot.</li>
    <li><strong>Sibirisk tiger</strong> is the Amur tiger; <strong>amurleopard</strong> (in Copenhagen) the Amur leopard. According to the 2017 classification, Ree Park’s <strong>nordkinesisk leopard</strong> (North Chinese leopard) also belongs to <i>P. p. orientalis</i>.</li>
    <li><strong>Lion:</strong> since 2017 there are two subspecies: the northern lion (<i>P. l. leo</i>), which includes Aalborg’s Asiatic lions, and the southern lion (<i>P. l. melanochaita</i>), which includes the Angolan lions. Blåvand’s white lions are of southern origin.</li>
    <li><strong>Free-living wild cats</strong> are outside the scope of this guide. The European wildcat has not been recorded in Denmark; it was found in Schleswig-Holstein, just across the border, in autumn 2025.</li>
  </ul>""",
  "da": """<ul class="prose">
    <li><strong>Los:</strong> europæisk los er <i>Lynx lynx</i>, rødlos er <i>Lynx rufus</i>. <strong>Karakal</strong> kaldes også “ørkenlos”, men er ikke en rigtig los.</li>
    <li><strong>Træleopard</strong> er <i>Neofelis nebulosa</i> (på engelsk clouded leopard); <strong>fiskekat</strong> er <i>Prionailurus viverrinus</i>.</li>
    <li><strong>Sibirisk tiger</strong> er det samme som amurtiger. Ree Parks <strong>nordkinesiske leopard</strong> hører efter inddelingen fra 2017 også til <i>P. p. orientalis</i>, ligesom amurleoparden i København.</li>
    <li><strong>Løve:</strong> siden 2017 er der to underarter: den nordlige løve (<i>P. l. leo</i>), som Aalborgs asiatiske løver hører til, og den sydlige løve (<i>P. l. melanochaita</i>), som angolaløverne hører til. De hvide løver i Blåvand er af sydlig afstamning.</li>
    <li><strong>Fritlevende vilde katte</strong> er ikke med i denne oversigt. Europæisk vildkat er ikke påvist i Danmark; i efteråret 2025 blev den fundet i Slesvig-Holsten, lige syd for grænsen.</li>
  </ul>"""},
 "verdwenen": {
  "nl": """<p class="prose">Bij elk park staat onder “Eerder hier” welke katten er vroeger waren. Opvallend: de Sumatraanse tijgers van Ree Park (tot 2020), de Aziatische kater Aakash in Aalborg (ingeslapen in december 2025, nu opgezet te zien), de caracal van Zoo København (tot 2024), de Amoertijgers van het vroegere Guldborgsund Zoo (nu Pangea Park Falster) en de lynxen van Skærup Zoo en Glad Zoo (laatst gezien 2021–2022). Wilde katten verdwenen al in de jaren zestig uit de circussen.</p>""",
  "en": """<p class="prose">Each park’s page lists under “Previously here” which cats it used to have. Notable: Ree Park’s Sumatran tigers (until 2020), Aalborg’s Asiatic male Aakash (put down in December 2025, now on display stuffed), the caracal at Zoo København (until 2024), the Amur tigers of the former Guldborgsund Zoo (now Pangea Park Falster) and the lynxes at Skærup Zoo and Glad Zoo (last seen 2021–2022). Wild cats disappeared from circuses as early as the 1960s.</p>""",
  "da": """<p class="prose">Ved hver park står under “Tidligere her”, hvilke katte der var der før. Bemærkelsesværdigt: Ree Parks sumatratigre (indtil 2020), Aalborgs asiatiske han Aakash (aflivet i december 2025, nu udstoppet og udstillet), karakalen i Zoo København (indtil 2024), amurtigrene i det tidligere Guldborgsund Zoo (nu Pangea Park Falster) og lossene i Skærup Zoo og Glad Zoo (sidst set 2021–2022). Vilde kattedyr forsvandt allerede fra cirkus i 1960’erne.</p>"""},
 "controle": {
  "nl": """<p class="prose"><strong>Officiële lijsten:</strong> de lijst “Godkendte zoologiske anlæg” van de Fødevarestyrelsen (oktober 2026), de ledenlijsten van DAZA en EAZA (oktober 2026) en de Deense regels voor het houden van dieren (bekendmaking 1261/2015).</p>
  <p class="prose"><strong>Databanken:</strong> Zootierliste (alle katachtigen, huidige en vroegere houdingen), alleen aanvullend.</p>
  <p class="prose"><strong>Websites van de parken</strong>, met dierenlijsten, soortpagina’s, plattegronden, dagprogramma’s en nieuws.</p>
  <p class="prose"><strong>Nieuws:</strong> onder meer DR, TV 2 en de regionale zenders (TV2 Fyn, TV2 Nord, TV2 Østjylland, TV Syd, TV 2 Øst), Ritzau, JydskeVestkysten en lokale nieuwssites.</p>""",
  "en": """<p class="prose"><strong>Official lists:</strong> the Fødevarestyrelsen list “Godkendte zoologiske anlæg” (October 2026), the member lists of DAZA and EAZA (October 2026) and the Danish rules on keeping animals (executive order 1261/2015).</p>
  <p class="prose"><strong>Databases:</strong> Zootierliste (all cats, current and former holdings), used only as a supplement.</p>
  <p class="prose"><strong>Park websites</strong>, with animal lists, species pages, maps, daily programmes and news.</p>
  <p class="prose"><strong>News:</strong> including DR, TV 2 and the regional stations (TV2 Fyn, TV2 Nord, TV2 Østjylland, TV Syd, TV 2 Øst), Ritzau, JydskeVestkysten and local news sites.</p>""",
  "da": """<p class="prose"><strong>Officielle lister:</strong> Fødevarestyrelsens liste “Godkendte zoologiske anlæg” (oktober 2026), medlemslisterne fra DAZA og EAZA (oktober 2026) og de danske regler for dyrehold (bekendtgørelse 1261/2015).</p>
  <p class="prose"><strong>Databaser:</strong> Zootierliste (alle kattedyr, nuværende og tidligere hold), kun som supplement.</p>
  <p class="prose"><strong>Parkernes hjemmesider</strong> med dyrelister, artssider, kort, dagsprogrammer og nyheder.</p>
  <p class="prose"><strong>Nyheder:</strong> bl.a. DR, TV 2 og regionalstationerne (TV2 Fyn, TV2 Nord, TV2 Østjylland, TV Syd, TV 2 Øst), Ritzau, JydskeVestkysten og lokale nyhedssider.</p>"""},
}
