# Landspecifieke tekstblokken van de Hongaarse gids (NL / EN / HU). Stand 23 oktober 2026.
import re, unicodedata
def _slug(x):
    x = "".join(c for c in unicodedata.normalize("NFD", x) if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"\(.*?\)", "", x)).strip("-")
def L(naam): return f'<a href="#locatie/{_slug(naam)}">{naam}</a>'

# alleen megyék met locaties, ruwweg van west naar oost
REGN = {"gyor-moson-sopron": ["Győr-Moson-Sopron", "Győr-Moson-Sopron", "Győr-Moson-Sopron"],
        "zala": ["Zala", "Zala", "Zala"],
        "veszprem": ["Veszprém", "Veszprém", "Veszprém"],
        "baranya": ["Baranya", "Baranya", "Baranya"],
        "budapest": ["Boedapest", "Budapest", "Budapest"],
        "pest": ["Pest", "Pest", "Pest"],
        "bacs-kiskun": ["Bács-Kiskun", "Bács-Kiskun", "Bács-Kiskun"],
        "csongrad-csanad": ["Csongrád-Csanád", "Csongrád-Csanád", "Csongrád-Csanád"],
        "heves": ["Heves", "Heves", "Heves"],
        "jasz-nagykun-szolnok": ["Jász-Nagykun-Szolnok", "Jász-Nagykun-Szolnok", "Jász-Nagykun-Szolnok"],
        "borsod-abauj-zemplen": ["Borsod-Abaúj-Zemplén", "Borsod-Abaúj-Zemplén", "Borsod-Abaúj-Zemplén"],
        "hajdu-bihar": ["Hajdú-Bihar", "Hajdú-Bihar", "Hajdú-Bihar"],
        "szabolcs-szatmar-bereg": ["Szabolcs-Szatmár-Bereg", "Szabolcs-Szatmár-Bereg", "Szabolcs-Szatmár-Bereg"]}

SZE, BUD, SZT, GYO, SOS, MIS = L("Szegedi Vadaspark"), L("Zoo Budapest"), L("Szentendrei Kisállatkert"), L("Zoo Gyöngyös"), L("Sóstó Zoo"), L("Zoo Miskolc")
MAG, MED, MEC, KEC, GYR, PEC, CSA, RIC = L("MaganZOO"), L("Medveotthon Veresegyház"), L("Mecske Zoo"), L("Kecskeméti Vadaskert"), L("Zoo Győr"), L("Zoo Pécs"), L("Állatkert Csácsi-hegy"), L("Richter Safari Park")

# losse vervangingen in het sjabloon (resten van Portugal in de Hongaarse vaste teksten)
HU_VERV = [("Portugáliában", "Magyarországon"), ("portugál állatkertek", "magyar állatkertek")]
VAST = [
 (r'<p class="stamp">.*?</p>', '<p class="stamp"><span class="l-nl">Stand 23 oktober 2026</span><span class="l-en">Updated 23 October 2026</span><span class="l-hu">Frissítve: 2026. október 23.</span></p>'),
 (r'<p class="lede">.*?</p>', '<p class="lede">'
  '<span class="l-nl">Waar in Hongarije kun je tijgers, sneeuwluipaarden, nevelpanters, manoels en andere wilde katten zien? Per soort en per park zie je hier welke katten er wonen, welke jongen er onlangs geboren zijn en wat er binnenkort verandert. En met welke route je alle soorten ziet.</span>'
  '<span class="l-en">Where in Hungary can you see tigers, snow leopards, clouded leopards, Pallas’s cats and other wild cats? By species and by park, this guide shows which cats live where, which young were born recently and what is about to change. And which route lets you see every species.</span>'
  '<span class="l-hu">Hol láthatsz Magyarországon tigrist, hópárducot, ködfoltos párducot, manult és más vadmacskákat? Az útmutató fajonként és parkonként megmutatja, melyik macska hol él, milyen kölykök születtek nemrég, és mi változik hamarosan. És hogy melyik útvonalon láthatod az összes fajt.</span></p>'),
]

LOC_INTRO = ["Alle dierentuinen, dierenparken, opvangcentra en wildparken in Hongarije waar wilde katten wonen. Tik op een stip om te zien welke katten er wonen.",
             "All zoos, animal parks, rescue centres and wildlife parks in Hungary where wild cats live. Tap a dot to see which cats live there.",
             "Az összes magyarországi állatkert, állatpark, mentőközpont és vadaspark, ahol vadmacskák élnek. Koppints egy pontra, és megnézheted, milyen macskák élnek ott."]

def tldr():
    nl = f'''<div class="l-nl">
<div class="prose">
  <ul>
    <li><strong>16 soorten bevestigd</strong> op 20 locaties: 11 dierentuinen (lid van EAZA of de Hongaarse dierentuinvereniging MÁSZ), 6 andere vergunde dierenparken (waaronder particuliere parken), 2 opvangcentra en het wildpark van Hortobágy.</li>
    <li><strong>{SZE}</strong> heeft 10 soorten, {SOS} 9 en {MIS} en {GYO} elk 7.</li>
    <li><strong>Maar op één plek te zien:</strong> de nevelpanter ({SZE}), Geoffroy’s kat ({SOS}) en de manoel ({BUD}).</li>
    <li><strong>Jonge katten:</strong> Amoertijgers in {BUD} (2025), een manoel in {BUD} en drie servals in {SOS} (mei 2026), en bij {MAG} leeuwen, een tijger en een serval (2026).</li>
    <li><strong>Witte tijgers en witte leeuwen</strong> zie je vooral in {MAG}, {GYR}, {PEC} en {CSA}; zwarte panters in {KEC}.</li>
    <li><strong>Circussen:</strong> geen Hongaars circus heeft in 2025–2026 nog grote katten gevonden; vanaf 1 januari 2027 zijn alle wilde katten in circussen verboden. De leeuwen en tijgers van de circusfamilie Richter wonen sinds 2022 in {RIC}.</li>
  </ul>
  </div>
</div>'''
    en = f'''<div class="l-en">
<div class="prose">
  <ul>
    <li><strong>16 species confirmed</strong> at 20 locations: 11 zoos (members of EAZA or the Hungarian zoo association MÁSZ), 6 other licensed animal parks (including private parks), 2 rescue centres and the Hortobágy wildlife park.</li>
    <li><strong>{SZE}</strong> has 10 species, {SOS} 9 and {MIS} and {GYO} 7 each.</li>
    <li><strong>Only in one place:</strong> the clouded leopard ({SZE}), Geoffroy’s cat ({SOS}) and the Pallas’s cat ({BUD}).</li>
    <li><strong>Young cats:</strong> Amur tigers at {BUD} (2025), a Pallas’s cat at {BUD} and three servals at {SOS} (May 2026), and lions, a tiger and a serval at {MAG} (2026).</li>
    <li><strong>White tigers and white lions</strong> can be seen mainly at {MAG}, {GYR}, {PEC} and {CSA}; black panthers at {KEC}.</li>
    <li><strong>Circuses:</strong> no Hungarian circus was found with big cats in 2025–2026; from 1 January 2027 all wild cats are banned in circuses. The lions and tigers of the Richter circus family have lived at {RIC} since 2022.</li>
  </ul>
  </div>
</div>'''
    hu = f'''<div class="l-hu">
<div class="prose">
  <ul>
    <li><strong>16 megerősített faj</strong> 20 helyen: 11 állatkert (az EAZA vagy a Magyar Állatkertek Szövetsége tagja), 6 másik engedélyes állatpark (köztük magánparkok), 2 mentőközpont és a Hortobágyi Vadaspark.</li>
    <li>A legtöbb faj: {SZE} – 10, {SOS} – 9, {MIS} és {GYO} – 7-7.</li>
    <li><strong>Csak egy helyen látható:</strong> ködfoltos párduc ({SZE}), Geoffroy-macska ({SOS}) és manul ({BUD}).</li>
    <li><strong>Kölykök:</strong> amuri tigrisek – {BUD} (2025); manul – {BUD} és három szervál – {SOS} (2026. május); oroszlánok, egy tigris és egy szervál – {MAG} (2026).</li>
    <li><strong>Fehér tigrisek és fehér oroszlánok</strong> főleg itt: {MAG}, {GYR}, {PEC}, {CSA}; fekete párducok: {KEC}.</li>
    <li><strong>Cirkuszok:</strong> 2025–2026-ban egyetlen magyar cirkuszban sem találtunk nagymacskát; 2027. január 1-jétől minden vadmacska tilos a cirkuszokban. A Richter cirkuszcsalád oroszlánjai és tigrisei 2022 óta itt élnek: {RIC}.</li>
  </ul>
  </div>
</div>'''
    return nl + en + hu + "\n"

GEEN = [
 [("Vergunde parken zonder katachtigen", "Licensed parks without cats", "Engedélyes parkok vadmacska nélkül"),
  "Tropicarium (Boedapest), Tisza-tavi Ökocentrum (Poroszló), Kimba Elefánt Park, Pusztaottlaka (nu een autosafaripark), Afrika Múzeum Balatonederics (leeuwen alleen opgezet), Körösvölgyi Állatpark (Szarvas), Bella Állatpark (Siófok), Zoo Kisfalud",
  ["Tropicarium (Budapest), Tisza-tavi Ökocentrum (Poroszló), Kimba Elefánt Park, Pusztaottlaka (now a drive-through safari park), Afrika Múzeum Balatonederics (lions only stuffed), Körösvölgyi Állatpark (Szarvas), Bella Állatpark (Siófok), Zoo Kisfalud",
   "Tropicarium (Budapest), Tisza-tavi Ökocentrum (Poroszló), Kimba Elefánt Park, Pusztaottlaka (ma autós szafaripark), Afrika Múzeum Balatonederics (oroszlán csak kitömve), Körösvölgyi Állatpark (Szarvas), Bella Állatpark (Siófok), Zoo Kisfalud"]],
 [("Circussen zonder katten", "Circuses without cats", "Cirkuszok vadmacska nélkül"),
  "Magyar Nemzeti Cirkusz, Richter Flórián Cirkusz (de dieren wonen in het Richter Safari Park), Eötvös Cirkusz (leeuwen en tijgers tot ten minste 2019; nu niet bevestigd)",
  ["Magyar Nemzeti Cirkusz, Richter Flórián Cirkusz (its animals live in the Richter Safari Park), Eötvös Cirkusz (lions and tigers until at least 2019; not confirmed now)",
   "Magyar Nemzeti Cirkusz, Richter Flórián Cirkusz (állatai a Richter Safari Parkban élnek), Eötvös Cirkusz (oroszlánok és tigrisek legalább 2019-ig; most nem megerősített)"]],
 [("Andere dierenparken, minizoo’s en kinderboerderijen zonder katachtigen", "Other animal parks, mini zoos and farm parks without cats", "Más állatparkok, minizoók és állatsimogatók vadmacska nélkül"),
  "Mini Zoo Komló (de ‘bengaalse kat’ is waarschijnlijk het huiskatras), Nagykanizsa Mini Zoo, MancsRanch (Pécs), Kenguru Park Tiszaderzs, Törökmezői Kis-Állatpark, RoBirtok, Előszállás, Pákozd en andere kleine parken",
  ["Mini Zoo Komló (the ‘Bengal cat’ is probably the domestic breed), Nagykanizsa Mini Zoo, MancsRanch (Pécs), Kenguru Park Tiszaderzs, Törökmezői Kis-Állatpark, RoBirtok, Előszállás, Pákozd and other small parks",
   "Mini Zoo Komló (a „bengáli macska” valószínűleg a házimacskafajta), Nagykanizsai Mini Zoo, MancsRanch (Pécs), Kenguru Park Tiszaderzs, Törökmezői Kis-Állatpark, RoBirtok, Előszállás, Pákozd és más kis parkok"]],
]
def geen(i):
    out = ""
    for row in GEEN:
        k, t, tr = row
        if i and tr: t = tr[i - 1]
        out += f"    <li><b>{k[i]}:</b> {t}</li>\n"
    return out

OFFICIEEL = [
 """<p>In Hongarije heeft elke dierentuin een vergunning van de natuurbeschermingsdienst van de provincie nodig. Er is geen openbaar landelijk register. De beste lijst is een rondvraag bij alle provincies uit april 2025 (gepubliceerd juni 2025): 45 locaties met een dierentuinvergunning. Daarnaast heeft de voedselautoriteit NÉBIH een lijst van 13 erkende dierentuinen (oktober 2024).</p>
    <p>Leeuwen, tijgers, luipaarden, jaguars, sneeuwluipaarden, cheetahs en poema’s mogen alleen in dierentuinen worden gehouden (en tot eind 2026 in circussen). Kleinere katten zoals serval en caracal mogen particulieren met een vergunning houden. Vanaf 1 januari 2027 zijn alle wilde katten in circussen verboden; dieren die er al zijn mogen blijven, maar niet meer optreden of fokken.</p>
    <p>De lijst in deze gids is opgebouwd uit die lijsten, de ledenlijsten van EAZA (9 Hongaarse dierentuinen) en de Hongaarse dierentuinvereniging (MÁSZ, 13 leden), Zootierliste (alle katachtigen, huidige en vroegere houders) en een zoektocht per megye naar andere parken, opvang en circussen.</p>
    <p>Of een park in deze gids een dierentuin heet, hangt af van het lidmaatschap van EAZA of MÁSZ. Andere parken met een dierentuinvergunning heten dierenpark.</p>
""",
 """<p>In Hungary every zoo needs a permit from the county nature conservation authority. There is no public national register. The best list is a survey of all counties from April 2025 (published June 2025): 45 sites with a zoo licence. In addition, the food chain authority NÉBIH lists 13 approved zoos (October 2024).</p>
    <p>Lions, tigers, leopards, jaguars, snow leopards, cheetahs and pumas may only be kept in zoos (and in circuses until the end of 2026). Smaller cats such as servals and caracals may be kept privately with a permit. From 1 January 2027 all wild cats are banned in circuses; animals already there may stay but may no longer perform or breed.</p>
    <p>The list in this guide was built from those lists, the member lists of EAZA (9 Hungarian zoos) and the Hungarian zoo association (MÁSZ, 13 members), Zootierliste (all cats, current and former holders) and a search county by county for other parks, rescue centres and circuses.</p>
    <p>Whether a park is called a zoo in this guide depends on membership of EAZA or MÁSZ. Other parks with a zoo licence are called animal parks.</p>
""",
 """<p>Magyarországon minden állatkertnek a megyei természetvédelmi hatóság engedélyére van szüksége. Nyilvános országos nyilvántartás nincs. A legjobb lista egy 2025. áprilisi, minden megyére kiterjedő felmérés (megjelent 2025 júniusában): 45 hely állatkerti engedéllyel. Emellett a NÉBIH 13 elismert állatkertet tart nyilván (2024. október).</p>
    <p>Oroszlánt, tigrist, leopárdot, jaguárt, hópárducot, gepárdot és pumát csak állatkert tarthat (és 2026 végéig cirkusz). Kisebb macskákat, például szervált és karakált magánszemély is tarthat engedéllyel. 2027. január 1-jétől minden vadmacska tilos a cirkuszokban; a már ott élő állatok maradhatnak, de nem léphetnek fel és nem szaporodhatnak.</p>
    <p>Az útmutató listája ezekből a listákból, az EAZA (9 magyar állatkert) és a Magyar Állatkertek Szövetsége (13 tag) taglistáiból, a Zootierlistéből (minden macskaféle, jelenlegi és korábbi tartók) és megyénkénti keresésből áll (más parkok, mentőközpontok, cirkuszok).</p>
    <p>Az, hogy egy parkot állatkertnek nevezünk-e, az EAZA- vagy MÁSZ-tagságtól függ. A többi állatkerti engedéllyel rendelkező park állatpark.</p>
"""]

ADVIES = [
 f"""<ul class="prose">
    <li><strong>Alle 16 soorten in vijf parken:</strong>
      <ul>
        <li><strong>Szegedi Vadaspark</strong>: nevelpanter, sneeuwluipaard, jaguar, cheetah, poema, Europese wilde kat (en leeuw, tijger, luipaard, lynx)</li>
        <li><strong>Zoo Budapest</strong>: manoel (en leeuw, tijger, Perzisch luipaard)</li>
        <li><strong>Szentendrei Kisállatkert</strong> (bij Boedapest): rode lynx</li>
        <li><strong>Zoo Gyöngyös</strong>: caracal, moeraskat, serval (en tijger, leeuw, luipaard, poema)</li>
        <li><strong>Sóstó Zoo</strong> (Nyíregyháza): Geoffroy’s kat (en drie tijgerondersoorten, witte leeuwen, sneeuwluipaard, jaguar, cheetah, serval)</li>
      </ul>
    </li>
    <li><strong>Alternatieven:</strong> caracal en moeraskat ook in {MIS}; rode lynx, moeraskat en serval samen in {MEC} (Baranya).</li>
    <li><strong>Particuliere parken</strong> hebben vaak beperkte openingstijden; kijk vóór je bezoek op hun site.</li>
    <li><strong>Twijfel je over een dier?</strong> Bel of mail dan vóór je bezoek met het park.</li>
  </ul>
""",
 f"""<ul class="prose">
    <li><strong>All 16 species in five parks:</strong>
      <ul>
        <li><strong>Szegedi Vadaspark</strong>: clouded leopard, snow leopard, jaguar, cheetah, puma, European wildcat (and lion, tiger, leopard, lynx)</li>
        <li><strong>Zoo Budapest</strong>: Pallas’s cat (and lion, tiger, Persian leopard)</li>
        <li><strong>Szentendrei Kisállatkert</strong> (near Budapest): bobcat</li>
        <li><strong>Zoo Gyöngyös</strong>: caracal, jungle cat, serval (and tiger, lion, leopard, puma)</li>
        <li><strong>Sóstó Zoo</strong> (Nyíregyháza): Geoffroy’s cat (and three tiger subspecies, white lions, snow leopard, jaguar, cheetah, serval)</li>
      </ul>
    </li>
    <li><strong>Alternatives:</strong> caracal and jungle cat also at {MIS}; bobcat, jungle cat and serval together at {MEC} (Baranya).</li>
    <li><strong>Private parks</strong> often have limited opening times; check their website before you go.</li>
    <li><strong>Not sure about an animal?</strong> Call or email the park before your visit.</li>
  </ul>
""",
 f"""<ul class="prose">
    <li><strong>Mind a 16 faj öt parkban:</strong>
      <ul>
        <li><strong>Szegedi Vadaspark</strong>: ködfoltos párduc, hópárduc, jaguár, gepárd, puma, európai vadmacska (és oroszlán, tigris, leopárd, hiúz)</li>
        <li><strong>Fővárosi Állatkert</strong>: manul (és oroszlán, tigris, perzsa leopárd)</li>
        <li><strong>Szentendrei Kisállatkert</strong> (Budapest mellett): vörös hiúz</li>
        <li><strong>Gyöngyösi Állatkert</strong>: karakál, mocsári macska, szervál (és tigris, oroszlán, leopárd, puma)</li>
        <li><strong>Sóstó Zoo</strong> (Nyíregyháza): Geoffroy-macska (és három tigris-alfaj, fehér oroszlánok, hópárduc, jaguár, gepárd, szervál)</li>
      </ul>
    </li>
    <li><strong>Más lehetőség:</strong> karakál és mocsári macska itt is: {MIS}; vörös hiúz, mocsári macska és szervál együtt: {MEC} (Baranya).</li>
    <li><strong>A magánparkok</strong> gyakran rövidebb ideig vannak nyitva; nézd meg a honlapjukat, mielőtt elindulsz.</li>
    <li><strong>Bizonytalan vagy egy állatban?</strong> Látogatás előtt hívd fel vagy írj a parknak.</li>
  </ul>
"""]

GEPLAND = [
 f"""<ul class="prose">
    <li><strong>Circussen:</strong> vanaf 1 januari 2027 zijn alle wilde katten in Hongaarse circussen verboden.</li>
    <li><strong>{SOS}:</strong> de witte tijgers zijn er niet meer; de eigen site noemt ze nog.</li>
    <li><strong>{SZE}:</strong> sinds de zomer van 2026 woont er weer een tijger, na de dood van de Amoertijger Igor (maart 2026).</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Gepland</span> · <span class="st st-w"><i></i>Onzeker</span></p>
""",
 f"""<ul class="prose">
    <li><strong>Circuses:</strong> from 1 January 2027 all wild cats are banned in Hungarian circuses.</li>
    <li><strong>{SOS}:</strong> the white tigers are no longer there; the park’s own website still lists them.</li>
    <li><strong>{SZE}:</strong> since summer 2026 there is a tiger again, after the death of the Amur tiger Igor (March 2026).</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Planned</span> · <span class="st st-w"><i></i>Uncertain</span></p>
""",
 f"""<ul class="prose">
    <li><strong>Cirkuszok:</strong> 2027. január 1-jétől minden vadmacska tilos a magyar cirkuszokban.</li>
    <li><strong>{SOS}:</strong> a fehér tigrisek már nincsenek ott; a park honlapja még említi őket.</li>
    <li><strong>{SZE}:</strong> 2026 nyara óta újra van tigris, Igor amuri tigris halála (2026. március) után.</li>
  </ul>
  <p class="tlegend"><span class="st st-p"><i></i>Tervezett</span> · <span class="st st-w"><i></i>Bizonytalan</span></p>
"""]

def _kv(lg, titel, sp, naar, locs):
    return f'<h3>{titel} <a class="kv-sp" href="#soort/{sp}">{naar}</a></h3>\n  <ul class="prose">\n' + "".join(f"    <li>{x}</li>\n" for x in locs) + "  </ul>\n"
KV = [
 (("Witte tijger", "naar de tijger"), ("White tiger", "to the tiger"), ("Fehér tigris", "a tigrishez"), "tijger", [MAG, GYR, PEC, CSA]),
 (("Witte leeuw", "naar de leeuw"), ("White lion", "to the lion"), ("Fehér oroszlán", "az oroszlánhoz"), "leeuw", [SOS, SZE, GYR, MAG]),
 (("Zwarte panter", "naar de luipaard"), ("Black panther", "to the leopard"), ("Fekete párduc", "a leopárdhoz"), "luipaard", [KEC]),
]
KVTXT = {"nl": f"Een witte tijger heeft een recessieve mutatie in het gen SLC45A2 en is geen albino; binnen het Europese fokprogramma worden ze niet meer gefokt. Witte leeuwen hebben leucisme, zwarte panters melanisme. De witte tijgers van {SOS} zijn er niet meer; volgens de site van {SZE} is ook een van de jaguars zwart (niet bevestigd).",
         "en": f"A white tiger has a recessive mutation in the SLC45A2 gene and is not an albino; they are no longer bred within the European breeding programme. White lions have leucism, black panthers melanism. The white tigers of {SOS} are gone; according to the {SZE} website one of the jaguars is black (not confirmed).",
         "hu": f"A fehér tigris az SLC45A2 gén recesszív mutációját hordozza, és nem albínó; az európai tenyészprogramban már nem tenyésztik. A fehér oroszlánok leucisztikusak, a fekete párducok melanisztikusak. A fehér tigrisek már nincsenek itt: {SOS}; {SZE} honlapja szerint az egyik jaguár fekete (nem megerősített)."}
HYB = {"nl": "Er zijn geen lijgers, tigons of andere hybriden van wilde katten gevonden. Zoo Szigetbecse houdt savannahkatten (kruisingen van serval en huiskat); die tellen in deze gids niet mee.",
       "en": "No ligers, tigons or other hybrids of wild cats were found. Zoo Szigetbecse keeps Savannah cats (crosses between serval and domestic cat); they do not count in this guide.",
       "hu": "Ligert, tigont vagy más vadmacska-hibridet nem találtunk. A Szigetbecsei Zoo savannah macskákat (szervál és házimacska keverékét) is tart; ezek nem számítanak bele az útmutatóba."}
def _kleur():
    out = ""
    for i, lg in enumerate(["nl", "en", "hu"]):
        out += f'<div class="l-{lg}">\n' + "".join(_kv(lg, k[i][0], k[3], k[i][1], k[4]) for k in KV) + f'  <p class="prose">{KVTXT[lg]}</p>\n</div>'
    out += '<h3 id="hybriden" style="font-size:22px;margin-top:30px"><span class="l-nl">Hybriden</span><span class="l-en">Hybrids</span><span class="l-hu">Hibridek</span></h3>\n'
    for lg in ["nl", "en", "hu"]:
        out += f'<div class="l-{lg}">\n<p class="prose">{HYB[lg]}</p>\n</div>'
    return out
KLEUR = _kleur()

UITLEG = {
 "werkwijze": {
  "nl": """<p class="prose">Voor alle Hongaarse dierentuinen, dierenparken, particuliere parken, opvangcentra en circussen is nagegaan welke wilde katachtigen er te zien zijn. De basislijst komt uit de rondvraag bij de provincies (45 vergunde locaties, 2025), de NÉBIH-lijst, de ledenlijsten van EAZA en MÁSZ en Zootierliste (alle katachtigen, huidige en vroegere houders); per megye is daarna gezocht naar andere parken. Elke locatie is gecontroleerd op de eigen website, aangevuld met Hongaars nieuws. Bij elke vermelding staan de bron en de datum.</p>
  <p class="prose">Een kat telt mee als een bezoeker hem kan zien, ook als dat alleen met een rondleiding kan. Particuliere parken staan erin als ze een vergunning hebben en open zijn; namen van particulieren staan niet in de gids.</p>
  <p class="prose">De indeling in soorten volgt de standaard van de IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>""",
  "en": """<p class="prose">For all Hungarian zoos, animal parks, private parks, rescue centres and circuses, we checked which wild cats can be seen. The base list comes from the county survey (45 licensed sites, 2025), the NÉBIH list, the member lists of EAZA and MÁSZ and Zootierliste (all cats, current and former holders); each county was then searched for other parks. Every location was checked on its own website, supplemented by Hungarian news. Each entry shows its source and date.</p>
  <p class="prose">A cat counts if a visitor can see it, even if only on a guided tour. Private parks are included if they are licensed and open; names of private individuals are not given.</p>
  <p class="prose">Species follow the standard of the IUCN/SSC Cat Classification Task Force (Kitchener et al., 2017, <i>Cat News</i> Special Issue 11).</p>""",
  "hu": """<p class="prose">Minden magyar állatkertet, állatparkot, magánparkot, mentőközpontot és cirkuszt megvizsgáltunk, hogy milyen vadmacskák láthatók ott. Az alaplista a megyei felmérésből (45 engedélyes hely, 2025), a NÉBIH listájából, az EAZA és a MÁSZ taglistáiból és a Zootierlistéből (minden macskaféle, jelenlegi és korábbi tartók) áll; ezután megyénként kerestünk további parkokat. Minden helyet a saját honlapján és a magyar sajtóban ellenőriztünk. Minden bejegyzésnél ott a forrás és a dátum.</p>
  <p class="prose">Egy macska akkor számít, ha a látogató láthatja, akár csak vezetett túrán. A magánparkok akkor szerepelnek, ha engedélyük van és nyitva vannak; magánszemélyek nevét nem közöljük.</p>
  <p class="prose">A fajok felosztása az IUCN/SSC Cat Classification Task Force szabványát követi (Kitchener és mtsai, 2017, <i>Cat News</i> Special Issue 11).</p>"""},
 "namen": {
  "nl": """<ul class="prose">
    <li><strong>Hiúz</strong> is de Euraziatische lynx, <strong>vörös hiúz</strong> de rode lynx, <strong>hópárduc</strong> de sneeuwluipaard, <strong>ködfoltos párduc</strong> de nevelpanter, <strong>manul</strong> de manoel en <strong>mocsári macska</strong> de moeraskat.</li>
    <li><strong>Tijger:</strong> in Nyíregyháza leven drie ondersoorten naast elkaar: de Amoertijger, de Sumatraanse tijger en de Maleise tijger (sinds 2017 bij <i>P. t. tigris</i>).</li>
    <li><strong>Luipaard:</strong> de Noord-Chinese luipaard van Szeged en Debrecen hoort bij de Amoerpanter (<i>P. p. orientalis</i>).</li>
  </ul>""",
  "en": """<ul class="prose">
    <li><strong>Hiúz</strong> is the Eurasian lynx, <strong>vörös hiúz</strong> the bobcat, <strong>hópárduc</strong> the snow leopard, <strong>ködfoltos párduc</strong> the clouded leopard, <strong>manul</strong> the Pallas’s cat and <strong>mocsári macska</strong> the jungle cat.</li>
    <li><strong>Tiger:</strong> Nyíregyháza keeps three subspecies side by side: the Amur tiger, the Sumatran tiger and the Malayan tiger (since 2017 part of <i>P. t. tigris</i>).</li>
    <li><strong>Leopard:</strong> the North Chinese leopard of Szeged and Debrecen belongs to the Amur leopard (<i>P. p. orientalis</i>).</li>
  </ul>""",
  "hu": """<ul class="prose">
    <li>Az útmutató hollandul készült; a magyar fajnevek a fajok oldalain szerepelnek.</li>
    <li><strong>Tigris:</strong> Nyíregyházán három alfaj él egymás mellett: az amuri, a szumátrai és a maláj tigris (2017 óta a <i>P. t. tigris</i> része).</li>
    <li><strong>Leopárd:</strong> a szegedi és debreceni észak-kínai leopárd az amuri leopárdhoz (<i>P. p. orientalis</i>) tartozik.</li>
  </ul>"""},
 "verdwenen": {
  "nl": f"""<p class="prose">Bij elk park staat onder “Eerder hier” welke katten er vroeger waren. Opvallend: de witte tijgers van {SOS} (tot 2026), de Amoertijger Igor van {SZE} (ingeslapen maart 2026), de vissende kat en de Aziatische leeuwin van Jászberény, en de Palawan-luipaardkat van Debrecen. De in beslag genomen tijgerwelp Pablo ging via {BUD} naar {MED}.</p>""",
  "en": f"""<p class="prose">Each park’s page lists under “Previously here” which cats it used to have. Notable: the white tigers of {SOS} (until 2026), the Amur tiger Igor of {SZE} (put down March 2026), the fishing cat and the Asiatic lioness of Jászberény, and the Palawan leopard cat of Debrecen. The confiscated tiger cub Pablo went via {BUD} to {MED}.</p>""",
  "hu": f"""<p class="prose">Minden park oldalán az „Korábban itt” résznél szerepel, milyen macskák éltek ott. Említésre méltó: a fehér tigrisek ({SOS}, 2026-ig), Igor amuri tigris ({SZE}, elaltatták 2026 márciusában), a jászberényi halászmacska és ázsiai oroszlán, valamint a debreceni palawani leopárdmacska. A lefoglalt Pablo tigriskölyök a Fővárosi Állatkerten keresztül ide került: {MED}.</p>"""},
 "controle": {
  "nl": """<p class="prose"><strong>Lijsten en regels:</strong> de rondvraag bij de provincies (IrányAdó Magazin, 17-06-2025), de NÉBIH-lijst (17-10-2024), de ledenlijsten van EAZA (oktober 2026) en MÁSZ, het besluit over gevaarlijke dieren (85/2015 FM) en het circusverbod (124/2026 Korm.).</p>
  <p class="prose"><strong>Databanken:</strong> Zootierliste (alle katachtigen, huidige en vroegere houdingen), alleen aanvullend.</p>
  <p class="prose"><strong>Websites van de parken</strong>, met dierenlijsten, adoptiepagina’s, voederprogramma’s en nieuws.</p>
  <p class="prose"><strong>Nieuws:</strong> onder meer Index, Telex, HVG, Origo, Délmagyar, Haon en andere regionale portalen.</p>""",
  "en": """<p class="prose"><strong>Lists and rules:</strong> the county survey (IrányAdó Magazin, 17-06-2025), the NÉBIH list (17-10-2024), the member lists of EAZA (October 2026) and MÁSZ, the decree on dangerous animals (85/2015 FM) and the circus ban (124/2026 Korm.).</p>
  <p class="prose"><strong>Databases:</strong> Zootierliste (all cats, current and former holdings), used only as a supplement.</p>
  <p class="prose"><strong>Park websites</strong>, with animal lists, adoption pages, feeding programmes and news.</p>
  <p class="prose"><strong>News:</strong> including Index, Telex, HVG, Origo, Délmagyar, Haon and other regional portals.</p>""",
  "hu": """<p class="prose"><strong>Listák és szabályok:</strong> a megyei felmérés (IrányAdó Magazin, 2025. 06. 17.), a NÉBIH listája (2024. 10. 17.), az EAZA (2026. október) és a MÁSZ taglistái, a veszélyes állatokról szóló rendelet (85/2015 FM) és a cirkuszi tilalom (124/2026 Korm.).</p>
  <p class="prose"><strong>Adatbázisok:</strong> Zootierliste (minden macskaféle, jelenlegi és korábbi tartás), csak kiegészítésként.</p>
  <p class="prose"><strong>A parkok honlapjai</strong> állatlistákkal, örökbefogadási oldalakkal, etetési programokkal és hírekkel.</p>
  <p class="prose"><strong>Hírek:</strong> többek között Index, Telex, HVG, Origo, Délmagyar, Haon és más regionális portálok.</p>"""},
}
