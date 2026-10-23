#!/usr/bin/env python3
"""Bouwt de Wilde katachtigen-gids uit één bron.

Bron (map bron/):
  gidsen/nl.html, be.html, lu.html, de.html  – de landengidsen (foto's als @@IMGn@@)
  start.html                                  – de startpagina (de gegevens in "const D" worden hier opnieuw berekend)
  ../img/                                     – alle foto's (n.webp / n.jpg …), nummer = n in @@IMGn@@
  artifact_kop.html, web_kop.html             – vaste kopjes voor de Claude-pagina en de website
  franse_namen.json, duitse_namen.json        – Franse en Duitse soortnamen voor de startgegevens

Uitvoer:
  _claude/claude.html  – één bestand voor de Claude-pagina (publiceren via Artifact)
  de website in de hoofdmap van de repository: index.html, nederland/, belgie/, luxemburg/, duitsland/,
  losse soort- en locatiepagina's, sitemap.xml, robots.txt

Gebruik:  python3 bron/bouw.py            (alles)
          python3 bron/bouw.py --geen-web  (alleen de Claude-pagina)
Vereist: node, Python met playwright (voor de losse pagina's).
"""
import base64, datetime, html as H, json, os, re, shutil, subprocess, sys, tempfile, threading, functools
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

BRON = os.path.dirname(os.path.abspath(__file__)) + "/"
ROOT = os.path.dirname(BRON.rstrip("/")) + "/"
sys.path.insert(0, BRON)
from startdata import bereken, slug, soorten, _young
import huisstijl

BASE = "/wildekattengids/"
SITE = "https://yeetkitty.github.io" + BASE
F = {"nl": "nederland", "be": "belgie", "lu": "luxemburg", "de": "duitsland", "fr": "frankrijk", "at": "oostenrijk", "ch": "zwitserland", "uk": "verenigd-koninkrijk", "it": "italie", "es": "spanje", "ie": "ierland", "pt": "portugal", "dk": "denemarken", "cz": "tsjechie", "se": "zweden", "no": "noorwegen", "fi": "finland", "pl": "polen", "hu": "hongarije"}
LAND = {"nl": "Nederland", "be": "België", "lu": "Luxemburg", "de": "Duitsland", "fr": "Frankrijk", "at": "Oostenrijk", "ch": "Zwitserland", "uk": "Verenigd Koninkrijk", "it": "Italië", "es": "Spanje", "ie": "Ierland", "pt": "Portugal", "dk": "Denemarken", "cz": "Tsjechië", "se": "Zweden", "no": "Noorwegen", "fi": "Finland", "pl": "Polen", "hu": "Hongarije"}
STATES = {"bayern": "Bayern", "nedersaksen": "Nedersaksen", "nrw": "Noordrijn-Westfalen", "saksen": "Saksen", "berlijn": "Berlijn", "hamburg": "Hamburg", "bremen": "Bremen", "saarland": "Saarland", "sleeswijk-holstein": "Sleeswijk-Holstein", "hessen": "Hessen", "brandenburg": "Brandenburg", "mecklenburg-voor-pommeren": "Mecklenburg-Voor-Pommeren", "rijnland-palts": "Rijnland-Palts", "thueringen": "Thüringen", "saksen-anhalt": "Saksen-Anhalt", "baden-wuerttemberg": "Baden-Württemberg"}
REGIOS = {"auvergne-rhone-alpes": "Auvergne-Rhône-Alpes", "bourgogne-franche-comte": "Bourgogne-Franche-Comté", "bretagne": "Bretagne", "centre-val-de-loire": "Centre-Val de Loire", "corsica": "Corsica", "grand-est": "Grand Est", "hauts-de-france": "Hauts-de-France", "ile-de-france": "Île-de-France", "normandie": "Normandië", "nouvelle-aquitaine": "Nouvelle-Aquitaine", "occitanie": "Occitanie", "pays-de-la-loire": "Pays de la Loire", "provence-alpes-cote-dazur": "Provence-Alpes-Côte d’Azur"}
# landen met één blok per deelstaat of regio (alleen de blokken die in de gids staan tellen)
AT_ST = {"wien": "Wenen", "niederoesterreich": "Neder-Oostenrijk", "burgenland": "Burgenland", "oberoesterreich": "Opper-Oostenrijk", "salzburg": "Salzburg", "steiermark": "Stiermarken", "kaernten": "Karinthië", "tirol": "Tirol", "vorarlberg": "Vorarlberg"}
CH_RG = {"genfermeergebied": "Genèvemeerregio", "mittelland": "Mittelland", "noordwest-zwitserland": "Noordwest-Zwitserland", "zuerich": "Zürich", "oost-zwitserland": "Oost-Zwitserland", "centraal-zwitserland": "Centraal-Zwitserland", "ticino": "Ticino"}
UK_RG = {"londen": "Londen", "zuidoost-engeland": "Zuidoost-Engeland", "zuidwest-engeland": "Zuidwest-Engeland", "oost-engeland": "Oost-Engeland", "oost-midlands": "East Midlands", "west-midlands": "West Midlands", "noordwest-engeland": "Noordwest-Engeland", "yorkshire": "Yorkshire en de Humber", "noordoost-engeland": "Noordoost-Engeland", "schotland": "Schotland", "wales": "Wales", "noord-ierland": "Noord-Ierland"}
DEEL = {}
# Frankrijk, Oostenrijk, Zwitserland en het VK zijn sinds 17-10-2026 één pagina met een regiofilter (bron/samenvoegen.py),
# Duitsland sinds 18-10-2026; de oude adressen per regio of deelstaat verwijzen door
OUD_DEEL = {"de": STATES, "fr": REGIOS, "at": AT_ST, "ch": CH_RG, "uk": UK_RG}
W3F_KEY = "9494e3c0-9342-4457-a5d6-b795793b9ce4"
MIME = {"webp": "image/webp", "jpg": "image/jpeg", "png": "image/png", "gif": "image/gif"}

def rd(p):
    return open(p, encoding="utf8").read()
def wr(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf8").write(t)
def sub1(t, old, new, n=1):
    c = t.count(old)
    if c != n:
        sys.exit(f"bouw gestopt: {c}x gevonden (verwacht {n}x): {old[:100]!r}")
    return t.replace(old, new)
def js(o):
    return json.dumps(o, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\!--")
def esc(x):
    return H.escape(x, quote=True)

# ------------------------------------------------------------------ bron inlezen
G = {c: rd(BRON + f"gidsen/{c}.html") for c in F}
START = rd(BRON + "start.html")

# ------------------------------------------------------------------ locatietypes en labels in elke gids zetten
LTJ = json.load(open(BRON + "locatietypes.json", encoding="utf8"))
LT_JS = ("\n/* ---- locatietypes ---- */\nconst LT=" + js({"types": LTJ["types"], "labels": LTJ["labels"], "beperkt": LTJ["beperkt_toegankelijk"]})
         + ";\n" + rd(BRON + "locatietypes.js"))
LT_HOOK = 'window.addEventListener("hashchange",route);\nroute();'
def met_types(t):
    if '<script type="application/json" id="ds-' in t or 'id="dsmap"' in t:
        def fix(mm):
            d = json.loads(mm.group(2))
            d["js"] = sub1(d["js"], LT_HOOK, LT_HOOK + LT_JS.replace("</", "<\\/"))
            return mm.group(1) + json.dumps(d, ensure_ascii=False).replace("</", "<\\/") + mm.group(3)
        return re.sub(r'(<script type="application/json" id="ds-[a-z-]+">)(.*?)(</script>)', fix, t, flags=re.S)
    return sub1(t, LT_HOOK, LT_HOOK + LT_JS.replace("</", "<\\/"))
G = {c: met_types(t) for c, t in G.items()}
# taalmenu (wereldbol met de huidige taal) in de startpagina en elke gids: zie bron/taalmenu.js
TM_JS = "<script>\n" + rd(BRON + "taalmenu.js").replace("</", "<\\/") + "</script>\n"
def met_taalmenu(t):
    return sub1(t, "</body>", TM_JS + "</body>")
G = {c: met_taalmenu(t) for c, t in G.items()}
imgs = sorted((f for f in os.listdir(ROOT + "img") if re.match(r"^\d+\.\w+$", f)), key=lambda f: int(f.split(".")[0]))
assert [int(f.split(".")[0]) for f in imgs] == list(range(len(imgs))), "fotonummers moeten aaneengesloten zijn"

# ------------------------------------------------------------------ startgegevens opnieuw berekenen
DATA = {c: json.loads(subprocess.check_output(["node", BRON + "extract.js", BRON + f"gidsen/{c}.html"])) for c in F}
m = re.search(r"const D=(\{.*?\});\n", START)
D = json.loads(m.group(1))
fr = json.load(open(BRON + "franse_namen.json", encoding="utf8"))
de_namen = json.load(open(BRON + "duitse_namen.json", encoding="utf8"))
it_namen = json.load(open(BRON + "italiaanse_namen.json", encoding="utf8"))
es_namen = json.load(open(BRON + "spaanse_namen.json", encoding="utf8"))
pt_namen = json.load(open(BRON + "portugese_namen.json", encoding="utf8"))
today = datetime.date.today()
for c in F:
    D[c] = bereken(DATA[c], D[c], today, fr, c, de_namen, it_namen, es_namen, pt_namen)
for c in OUD_DEEL:
    D[c].pop("note", None)   # "alle 13 regio's" e.d. hoort niet meer bij één pagina
D["sp"] = soorten(DATA, fr, today, de_namen, it_namen, es_namen, pt_namen)
# kenmerken per soort voor de soortpagina (uit de Nederlandse gids) en de pagina in de Spottersgids
_nlg = DATA["nl"]["main"]; _bysci = {x[2]: x for x in _nlg["SPECIES"]}; _spen = _nlg.get("SPEN") or {}
_kata = json.load(open(ROOT + "spottersgids/bron/katalogue.json", encoding="utf8"))
D["feit"] = {}
for _s in D["sp"]:
    _r = _bysci.get(_s[4])
    if not _r: continue
    _k = next((k for k in _kata if k["la"] == _s[4]), None); _map = ""
    if _k:
        for _c in (slug(_k["nl"]), slug(_k["nl"].replace("’", "").replace("'", ""))):
            if os.path.exists(ROOT + "spottersgids/" + _c + "/index.html"): _map = _c; break
    D["feit"][_s[0]] = [_r[4], _r[5], _r[6], _r[9], ((_spen.get(_r[0]) or ["", "", ""]) + ["", ""])[2], _map]
D["lt"] = {"types": [{k: t[k] for k in ("nl", "en", "fr", "de", "it", "es", "pt", "uitleg", "uitleg_en", "uitleg_fr", "uitleg_de", "uitleg_it", "uitleg_es", "uitleg_pt")} for t in LTJ["types"]],
           "labels": [{k: l[k] for k in ("key", "nl", "en", "fr", "de", "it", "es", "pt", "icoon")} for l in LTJ["labels"]]}
# top 10 om te bezoeken (bron/top10.json): vaste plaatsen, aangevuld met de hoogste score
def top10(D):
    cfg = json.load(open(BRON + "top10.json", encoding="utf8"))
    CONFS = set("gybr"); landen = [c for c in F]
    nloc = {}
    for c in landen:
        for l in D[c]["locs"]:
            for x in {x[4] for x in l[5] if x[3] in CONFS}: nloc[x] = nloc.get(x, 0) + 1
    def score(c, i):
        l = D[c]["locs"][i]; lt = (D[c].get("lt") or [])[i] if i < len(D[c].get("lt") or []) else ["", []]
        conf = {x[4] for x in l[5] if x[3] in CONFS}; onz = [x for x in l[5] if x[3] not in CONFS]
        sc = len(conf) * 10 + sum(4 for x in conf if nloc[x] <= 3)
        sc += 3 * ("overnachten" in lt[1]) + 3 * (lt[0] == "Safaripark")
        sc -= 8 * bool(set(lt[1]) & {"rondleiding", "leden", "bezoekdagen"}) + 2 * len(onz)
        return sc
    out, per = [], {}
    def zoek(c, naam):
        return next((i for i, l in enumerate(D[c]["locs"]) if l[0] == naam), None)
    for v in cfg["vast"]:
        i = zoek(v["land"], v["naam"])
        if i is None:
            print("top 10: niet (meer) in de gids:", v["naam"]); continue
        out.append({"c": v["land"], "i": i, "uitleg": v.get("uitleg") or []}); per[v["land"]] = per.get(v["land"], 0) + 1
    kand = sorted(((score(c, i), c, i) for c in landen for i in range(len(D[c]["locs"]))), reverse=True)
    for sc, c, i in kand:
        if len(out) >= 10: break
        if D[c]["locs"][i][0] in cfg.get("uitsluiten", []) or any(o["c"] == c and o["i"] == i for o in out): continue
        if per.get(c, 0) >= cfg.get("max_per_land", 4): continue
        out.append({"c": c, "i": i, "uitleg": []}); per[c] = per.get(c, 0) + 1
    return out[:10]
D["top10"] = top10(D)
START = START[:m.start(1)] + json.dumps(D, ensure_ascii=False, separators=(",", ":")) + START[m.end(1):]
# datum "Bijgewerkt …" op de startpagina: de dag van de bouw
_MNL = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"]
_MFR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
_MDE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
_MIT = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]
_MES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
_MPT = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
_MEN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
START, _n = re.subn(r'<p class="stamp">.*?</p>',
    f'<p class="stamp"><span class="l-nl">Bijgewerkt {today.day} {_MNL[today.month-1]} {today.year}</span><span class="l-en">Updated {today.day} {_MEN[today.month-1]} {today.year}</span>'
    f'<span class="l-fr">Mis à jour le {today.day} {_MFR[today.month-1]} {today.year}</span><span class="l-de">Aktualisiert am {today.day}. {_MDE[today.month-1]} {today.year}</span>'
    f'<span class="l-it">Aggiornato al {today.day} {_MIT[today.month-1]} {today.year}</span><span class="l-es">Actualizado el {today.day} de {_MES[today.month-1]} de {today.year}</span>'
    f'<span class="l-pt">Atualizado a {today.day} de {_MPT[today.month-1]} de {today.year}</span></p>',
    START, count=1)
assert _n == 1, "datum op de startpagina niet gevonden"
wr(BRON + "start.html", START)
START = met_taalmenu(START)

# ------------------------------------------------------------------ Claude-pagina
# De foto's staan niet in de pagina zelf maar als losse bestanden ernaast (img/n.webp). Publiceren met
# Artifact: file_path _claude/claude.html en files = de inhoud van _claude/bestanden.json.
# Zo telt voor de 16 MB-grens alleen de tekst en de gegevens.
# Elke landgids staat gecomprimeerd (gzip, base64) in de pagina en wordt pas uitgepakt als je het land opent.
# Losse bestanden ernaast werken niet: de Claude-omgeving blokkeert eigen scripts én het ophalen van bestanden.
import gzip
IMG = ["img/" + f for f in imgs]
shutil.rmtree(ROOT + "_claude/g", ignore_errors=True)
GZ = {c: base64.b64encode(gzip.compress(t_.encode("utf-8"), 9)).decode("ascii") for c, t_ in G.items()}
wr(ROOT + "_claude/bestanden.json", json.dumps({"img/" + f: "img/" + f for f in imgs}, indent=0) + "\n")
k = START.index("<script>\n(function(){")
claude = (rd(BRON + "artifact_kop.html") + "<script>window.__IMG=" + json.dumps(IMG) + ";\nwindow.__G={};\nwindow.__GZ=" + json.dumps(GZ)
          + ";\nwindow.__START=" + js(START) + ";</script>\n" + START[k:])
wr(ROOT + "_claude/claude.html", claude)
print("Claude-pagina:", ROOT + "_claude/claude.html", round(len(claude.encode()) / 1e6, 1), "MB; gidsen gecomprimeerd:",
      ", ".join(f"{c} {round(len(v) / 1e6, 2)}" for c, v in GZ.items()), "MB")
assert len(claude.encode()) < 15.8e6, "Claude-pagina te groot (grens 16 MB)"
if "--geen-web" in sys.argv:
    sys.exit(0)

# ------------------------------------------------------------------ website: hulpjes
def opsomming(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " en " + xs[-1]
def kort(t, n=158):
    return t if len(t) <= n else t[:n - 1].rsplit(" ", 1)[0] + "…"
def plaats_kort(p):
    return re.sub(r"^([^()]*) \(([^()]*)\)$", r"\1, \2", p)
PATHS = [BASE + "img/" + f for f in imgs]
def fotos(t):
    return re.sub(r"@@IMG(\d+)@@", lambda mm: PATHS[int(mm.group(1))], t)
# bezoekersteller (GoatCounter, zonder cookies) – alleen op de website
GOATCOUNTER = '<script data-goatcounter="https://wildekattengids.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>\n'
def seo(title, desc, url, image=SITE + "voorbeeld.jpg", soort="website"):
    return (f'<meta name="description" content="{esc(desc)}">\n<meta name="author" content="J. Gelens">\n'
            f'<link rel="canonical" href="{url}">\n<meta property="og:type" content="{soort}">\n'
            f'<meta property="og:site_name" content="Wilde katachtigen-gids">\n<meta property="og:title" content="{esc(title)}">\n'
            f'<meta property="og:description" content="{esc(desc)}">\n<meta property="og:url" content="{url}">\n'
            f'<meta property="og:image" content="{image}">\n<meta property="og:locale" content="nl_NL">\n'
            + GOATCOUNTER +
            '<meta name="twitter:card" content="summary_large_image">\n')

# meldformulier via Web3Forms (alleen op de website; de Claude-pagina gebruikt reacties)
NOTE = {"nl": "Je melding gaat rechtstreeks naar de maker van de gids en is niet openbaar. Wil je een reactie, zet dan je e-mailadres bij Opmerkingen.",
        "en": "Your report goes straight to the guide’s author and is not public. If you would like a reply, add your email address under Comments.",
        "fr": "Votre signalement est envoyé directement à l’auteur du guide et n’est pas public. Si vous souhaitez une réponse, indiquez votre adresse e-mail dans les commentaires.",
        "de": "Deine Meldung geht direkt an den Macher des Leitfadens und ist nicht öffentlich. Wenn du eine Antwort möchtest, gib deine E-Mail-Adresse unter Anmerkungen an.",
        "it": "La tua segnalazione arriva direttamente all’autore della guida e non è pubblica. Se desideri una risposta, aggiungi il tuo indirizzo e-mail nelle osservazioni.",
        "es": "Tu aviso llega directamente al autor de la guía y no es público. Si quieres una respuesta, añade tu dirección de correo electrónico en las observaciones.",
        "pt": "O teu aviso vai diretamente para o autor do guia e não é público. Se quiseres uma resposta, acrescenta o teu endereço de e-mail nas observações.",
        "da": "Din melding går direkte til guidens forfatter og er ikke offentlig. Hvis du gerne vil have svar, så skriv din e-mailadresse under Bemærkninger.",
        "cs": "Tvoje hlášení jde přímo autorovi průvodce a není veřejné. Pokud chceš odpověď, napiš do poznámek svou e-mailovou adresu.",
        "sv": "Din rapport går direkt till guidens författare och är inte offentlig. Om du vill ha svar, skriv din e-postadress under Kommentarer.",
        "nb": "Meldingen din går rett til forfatteren av guiden og er ikke offentlig. Vil du ha svar, skriv e-postadressen din under Kommentarer.",
        "fi": "Ilmoituksesi menee suoraan oppaan tekijälle eikä ole julkinen. Jos haluat vastauksen, kirjoita sähköpostiosoitteesi kohtaan Huomautukset.",
        "pl": "Twoje zgłoszenie trafia bezpośrednio do autora przewodnika i nie jest publiczne. Jeśli chcesz odpowiedzi, wpisz swój adres e-mail w Uwagach.",
        "hu": "A bejelentésed közvetlenül az útmutató szerzőjéhez kerül, és nem nyilvános. Ha választ szeretnél, írd be az e-mail-címedet a Megjegyzések mezőbe."}
RPWEB0 = r'''async function rpWeb(d){
  const btn=rpEl("rp-go");btn.disabled=true;rpMsg(T("Bezig met versturen…","Sending…"@@SEND@@));
  const body={access_key:window.__W3F.key,subject:"Melding gids "+window.__W3F.land+": "+d.type+" – "+d.loc,from_name:"Wilde katachtigen-gids",
    Melding:rpEl("rp-sum").textContent.trim(),Soort_melding:d.type,Locatie:d.loc,Soort:d.soort,Datum_bezoek:d.datum||"-",Opmerkingen:d.opm||"-",
    Gids:window.__W3F.land,Pagina:location.href,Taal:(typeof LANG!=="undefined"?LANG:"nl"),botcheck:""};
  try{
    const r=await fetch("https://api.web3forms.com/submit",{method:"POST",headers:{"Content-Type":"application/json","Accept":"application/json"},body:JSON.stringify(body)});
    const j=await r.json().catch(()=>({}));
    if(!(r.ok&&j.success))throw new Error("mislukt");
    rpEl("rp-opm").value="";rpUpdate();
    rpMsg(T("Bedankt! Je melding is verstuurd.","Thank you! Your report has been sent."@@OK@@));
  }catch(e){
    rpMsg(T("Versturen is niet gelukt. Probeer het later opnieuw.","Sending failed. Please try again later."@@FOUT@@),true);
  }
  btn.disabled=false;
}
'''
RPTXT = {"SEND": {"fr": "Envoi en cours…", "de": "Wird gesendet…", "it": "Invio in corso…", "es": "Enviando…", "pt": "A enviar…", "da": "Sender…", "cs": "Odesílám…", "sv": "Skickar…", "nb": "Sender…", "fi": "Lähetetään…", "pl": "Wysyłanie…", "hu": "Küldés…"},
         "OK": {"fr": "Merci ! Votre signalement a été envoyé.", "de": "Danke! Deine Meldung wurde gesendet.", "it": "Grazie! La tua segnalazione è stata inviata.", "es": "¡Gracias! Tu aviso se ha enviado.", "pt": "Obrigado! O teu aviso foi enviado.", "da": "Tak! Din melding er sendt.", "cs": "Děkujeme! Tvoje hlášení bylo odesláno.", "sv": "Tack! Din rapport har skickats.", "nb": "Takk! Meldingen din er sendt.", "fi": "Kiitos! Ilmoituksesi on lähetetty.", "pl": "Dziękujemy! Twoje zgłoszenie zostało wysłane.", "hu": "Köszönjük! A bejelentésedet elküldtük."},
         "FOUT": {"fr": "L’envoi a échoué. Veuillez réessayer plus tard.", "de": "Senden fehlgeschlagen. Bitte versuche es später noch einmal.", "it": "Invio non riuscito. Riprova più tardi.", "es": "No se ha podido enviar. Inténtalo de nuevo más tarde.", "pt": "Não foi possível enviar. Tenta novamente mais tarde.", "da": "Afsendelsen mislykkedes. Prøv igen senere.", "cs": "Odeslání se nezdařilo. Zkus to prosím později.", "sv": "Det gick inte att skicka. Försök igen senare.", "nb": "Det gikk ikke å sende. Prøv igjen senere.", "fi": "Lähetys epäonnistui. Yritä myöhemmin uudelleen.", "pl": "Nie udało się wysłać. Spróbuj ponownie później.", "hu": "A küldés nem sikerült. Próbáld újra később."}}
# talen van elke gids na Nederlands en Engels, in de volgorde van T(nl,en,…) in die gids
GTAAL = {"nl": [], "be": ["fr"], "lu": ["fr", "de"], "de": ["de"], "fr": ["fr"], "at": ["de"], "ch": ["de", "fr", "it"], "uk": [], "it": ["it"], "es": ["es"], "ie": [], "pt": ["pt"], "dk": ["da"], "cz": ["cs"], "se": ["sv"], "no": ["nb"], "fi": ["fi"], "pl": ["pl"], "hu": ["hu"]}
def rpweb(c):
    t = RPWEB0
    for k, v in RPTXT.items():
        t = t.replace("@@" + k + "@@", "".join("," + json.dumps(v[l], ensure_ascii=False) for l in GTAAL[c]))
    return t
RPWEB = rpweb("be")
def meld_js(t, rp=RPWEB):
    t = sub1(t, "} else {COMMENTS=null;rpUit();} }", "} else if(window.__W3F){COMMENTS={};} else {COMMENTS=null;rpUit();} }")
    t = sub1(t, "  if(COMMENTS===undefined){", "  if(window.__W3F){rpUpdate();return rpWeb(d);}\n  if(COMMENTS===undefined){")
    return sub1(t, "function rpUit(){", rp + "function rpUit(){")
def meld_note(h):
    mm = re.search(r'(<p class="prose" style="font-size:14.5px;color:var\(--muted\)">)(<span class="l-nl">Na het klikken opent een reactievenster.*?)(</p>)', h, re.S)
    assert mm, "uitleg meldformulier niet gevonden"
    spans = re.findall(r'<span class="l-(\w\w)">', mm.group(2))
    return h[:mm.start(2)] + "".join(f'<span class="l-{l}">{NOTE[l]}</span>' for l in spans) + h[mm.end(2):]
def meld(doc, land, rp):
    i = doc.index("<meta charset"); j = doc.index(">", i) + 1
    doc = doc[:j] + f'\n<script>window.__W3F={{key:"{W3F_KEY}",land:"{land}"}};</script>\n' + doc[j:]
    if '<script type="application/json" id="ds-' in doc or 'id="dsmap"' in doc:
        def fix(mm):
            d = json.loads(mm.group(2))
            d["js"] = meld_js(d["js"], rp); d["html"] = meld_note(d["html"])
            return mm.group(1) + json.dumps(d, ensure_ascii=False).replace("</", "<\\/") + mm.group(3)
        doc = re.sub(r'(<script type="application/json" id="ds-[a-z-]+">)(.*?)(</script>)', fix, doc, flags=re.S)
        return doc
    return meld_note(meld_js(doc, rp))

# ------------------------------------------------------------------ website: landen- en deelstaatpagina's
for d in list(F.values()):
    shutil.rmtree(ROOT + d, ignore_errors=True)
CTRY = {
    "nl": ("Wilde katachtigen in Nederland – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Nederlandse dierentuinen, dierenparken en opvangcentra? Leeuw, tijger, luipaard, lynx, serval, manoel en meer, per park, met kaart, routeplanner en recente geboortes."),
    "be": ("Wilde katachtigen in België – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Belgische dierentuinen en dierenparken, van Pairi Daiza en Planckendael tot Pakawi? Per soort en per park, met kaart, routeplanner en recente geboortes."),
    "lu": ("Wilde katachtigen in Luxemburg – welke wilde katten zie je waar?",
           "Welke wilde katten zie je in Luxemburgse dierenparken? Met bezoekinformatie, kaart en soortpagina’s."),
    "fr": ("Wilde katachtigen in Frankrijk – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Franse dierentuinen, dierenparken en opvangcentra? Per regio, per soort en per park, met kaart, routeplanner en recente geboortes."),
    "at": ("Wilde katachtigen in Oostenrijk – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Oostenrijkse dierentuinen, Tierparks en Wildparks, van Schönbrunn tot de Alpenzoo? Per deelstaat, per soort en per park, met kaart, routeplanner en recente geboortes."),
    "ch": ("Wilde katachtigen in Zwitserland – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Zwitserse dierentuinen, Tierparks en Wildparks, van Zoo Zürich tot de Sikypark? Per regio, per soort en per park, met kaart, routeplanner en recente geboortes."),
    "uk": ("Wilde katachtigen in het Verenigd Koninkrijk – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Britse dierentuinen, safariparken en wildlife parks? Per regio, per soort en per park, met kaart, routeplanner en recente geboortes."),
    "it": ("Wilde katachtigen in Italië – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Italiaanse dierentuinen, dierenparken, safariparken, opvangcentra en circussen? Per regio, per soort en per park, met kaart, routeplanner en recente geboortes."),
    "es": ("Wilde katachtigen in Spanje – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Spaanse dierentuinen, dierenparken, safariparken en opvangcentra? Per regio, per soort en per park, met kaart, routeplanner en recente geboortes."),
    "ie": ("Wilde katachtigen in Ierland – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Ierse dierentuinen, wildlife parks en dierenparken, van Dublin Zoo tot Fota Wildlife Park? Per provincie, per soort en per park, met kaart, routeplanner en recente geboortes."),
    "pt": ("Wilde katachtigen in Portugal – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Portugese dierentuinen, dierenparken, safariparken en opvangcentra, van Zoo de Lisboa tot Badoca? Per regio, per soort en per park, met kaart, routeplanner en recente geboortes."),
    "dk": ("Wilde katachtigen in Denemarken – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Deense dierentuinen, dierenparken en safariparken, van Zoo København tot Ree Park en Knuthenborg? Per regio, per soort en per park, met kaart, routeplanner en recente geboortes."),
    "cz": ("Wilde katachtigen in Tsjechië – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Tsjechische dierentuinen, dierenparken, safariparken en opvangcentra, van Zoo Praha tot Safari Park Dvůr Králové? Per regio, per soort en per park, met kaart, routeplanner en recente geboortes."),
    "se": ("Wilde katachtigen in Zweden – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Zweedse dierentuinen en dierenparken, van Kolmården en Borås Djurpark tot Nordens Ark en Orsa Rovdjurspark? Per län, per soort en per park, met kaart, routeplanner en recente geboortes."),
    "no": ("Wilde katachtigen in Noorwegen – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Noorse dierentuinen en dierenparken, van Kristiansand Dyrepark tot Polar Park? Per fylke, per soort en per park, met kaart, routeplanner en recente geboortes."),
    "fi": ("Wilde katachtigen in Finland – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Finse dierentuinen en dierenparken, van Korkeasaari tot Ähtäri en Ranua? Per landschap, per soort en per park, met kaart, routeplanner en recente geboortes."),
    "pl": ("Wilde katachtigen in Polen – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Poolse dierentuinen, dierenparken, safariparken en opvangcentra, van Zoo Wrocław tot Zoo Warszawa? Per woiwodschap, per soort en per park, met kaart, routeplanner en recente geboortes."),
    "hu": ("Wilde katachtigen in Hongarije – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Hongaarse dierentuinen, dierenparken en opvangcentra, van de Budapest Zoo tot Nyíregyháza en Szeged? Per megye, per soort en per park, met kaart, routeplanner en recente geboortes."),
    "de": ("Wilde katachtigen in Duitsland – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Duitse dierentuinen, Tierparks en Wildparks? Per deelstaat, per soort en per park, met kaart, routeplanner en recente geboortes."),
}
# Duitse gids op de website: elke pagina krijgt alleen de gegevens van zijn eigen deelstaat (de Claude-pagina houdt alles in één bestand)
DSKR = {c: {st: [[r[0], "", r[2], r[3], r[4]] for r in DATA[c][st]["R"]] for st in DATA[c]} for c in DEEL}
def alleen_ds(doc, keep, c="de"):
    doc = re.sub(r'<script type="application/json" id="ds-([a-z-]+)">.*?</script>\n?',
                 lambda mm: mm.group(0) if mm.group(1) == keep else "", doc, flags=re.S)
    i = doc.index("<meta charset"); j = doc.index(">", i) + 1
    extra = f'\n<script>window.__DSBASE="{BASE}{F[c]}/";' + ("window.__DSKR=" + js(DSKR[c]) + ";" if keep is None else "") + "</script>"
    return doc[:j] + extra + doc[j:]
HOME_JS = 'if(window.__home){window.__home();}else{location.reload();}'
WEB = {}
DEEL_WEB = {}
for c, doc in G.items():
    doc = fotos(doc)
    doc = sub1(doc, HOME_JS, f'location.href="{BASE}";')
    doc = sub1(doc, '<a href="#" id="naar-landen">', f'<a href="{BASE}" id="naar-landen">')
    _li = {n: ((v.get("type") or [""])[0]) for part in DATA[c].values() for n, v in (part.get("LOCINFO") or {}).items()}
    _vl = re.search(r"\n  " + c + r":'(<svg[^']*)'", START).group(1).replace('class="flag"', "")
    _kd = huisstijl.kaartdata(LTJ["types"], _li, ["nl", "en"] + GTAAL[c])
    _kd["jong"] = sorted({e["loc"] for part in DATA[c].values() for _d, e in _young(part, lambda n: n, lambda n, en: en, today, None)})
    doc = huisstijl.toepassen(doc, ["nl", "en"] + GTAAL[c], BASE, _kd,
                              huisstijl.kopdata(c, ["nl", "en"] + GTAAL[c], _vl))   # bovenbalk, kleuren, letters, kop, tabbladen en Ko-fi van de startpagina
    t, d = CTRY[c]
    doc = re.sub(r"<title>[^<]*</title>", lambda mm: f"<title>{t}</title>\n" + seo(t, d, SITE + F[c] + "/"), doc, count=1)
    WEB[c] = doc   # zonder meldformulier-aanpassing (voor de stijl en momentopnames)
    if c in DEEL:
        DEEL_WEB[c] = meld(doc, LAND[c], rpweb(c))
        wr(ROOT + F[c] + "/index.html", alleen_ds(DEEL_WEB[c], None, c))
    else:
        wr(ROOT + F[c] + "/index.html", meld(doc, LAND[c], rpweb(c)))
DEELPAG = [(c, st, nm) for c in DEEL for st, nm in DEEL[c].items() if st in DATA[c]]
for c, st, nm in DEELPAG:
    o = DATA[c][st]
    cats = []
    for r in o["R"]:
        if r[0] not in cats:
            cats.append(r[0])
    t = f"Wilde katachtigen in {nm} – welke wilde katten in welke dierentuin?"
    d = f"Welke wilde katten zie je in {nm}? {len(o['LOCS'])} {'dierentuinen, Tierparks en Wildparks' if c in ('de', 'at', 'ch') else 'dierentuinen, safariparken en wildlife parks' if c == 'uk' else 'dierentuinen, dierenparken en opvangcentra'} met o.a. {', '.join(x.lower() for x in cats[:4])}. Met kaart, routeplanner en recente geboortes."
    url = SITE + F[c] + "/" + st + "/"
    doc = re.sub(r'<title>.*?</title>.*?<meta name="twitter:card"[^>]*>\n', "", DEEL_WEB[c], count=1, flags=re.S)
    # adres vastzetten op deze deelstaat; een link naar een andere deelstaat of naar de Duitse startpagina gaat naar die pagina
    force = ('<script>(function(){var h=decodeURIComponent(location.hash.slice(1)),s=h.split("/")[0],A=' + json.dumps(list(DEEL[c]))
             + ',B="' + BASE + F[c] + '/";if(s==="' + c + '"){location.replace(B+"#"+h);return;}if(s!=="' + st
             + '"&&A.indexOf(s)>=0){location.replace(B+s+"/#"+h);return;}if(!/^' + st + '(\\/|$)/.test(h)){try{history.replaceState(null,"","#'
             + st + '"+(h?"/"+h:""));}catch(e){}}})();</script>\n')
    head = f"<title>{t}</title>\n" + seo(f"Wilde katachtigen in {nm}", d, url) + force
    i = doc.index("<meta charset"); j = doc.index(">", i) + 1
    wr(ROOT + f"{F[c]}/{st}/index.html", alleen_ds(doc[:j] + "\n" + head + doc[j:], st, c))

# ------------------------------------------------------------------ website: startpagina
st = START
fmap = "{" + ",".join(f'{c}:"{BASE}{v}/"' for c, v in F.items()) + "}"
st = sub1(st, "window.openCountry=function(c,h){",
          f"window.__F={fmap};\n  window.openCountry=function(c,h){{location.replace(window.__F[c]+(h?\"#\"+h:\"\"));return;")
st = st.replace("${c}.html", "${window.__F[c]}").replace("${ZOOM}.html", "${window.__F[ZOOM]}")
TITLE = "Wilde katachtigen in de Benelux, Duitsland, Frankrijk, Oostenrijk, Zwitserland, Italië, Spanje, Portugal, Denemarken, Zweden, Noorwegen, Finland, Polen, Tsjechië, Hongarije, het Verenigd Koninkrijk en Ierland – waar zie je welke wilde kat?"
DESC = ("Gids van J. Gelens: welke wilde katten – leeuw, tijger, luipaard, lynx, serval, manoel en meer – je in dierentuinen, "
        "dierenparken en opvangcentra in Nederland, België, Luxemburg, Duitsland, Frankrijk, Oostenrijk, Zwitserland, Italië, Spanje, Portugal, Denemarken, Zweden, Noorwegen, Finland, Polen, Tsjechië, Hongarije, het Verenigd Koninkrijk en Ierland kunt zien. Met kaart, routeplanner en recente geboortes.")
st = sub1(st, "<title>Wilde katachtigen in de Benelux, Duitsland, Frankrijk, Oostenrijk, Zwitserland, Italië, Spanje, Portugal, Denemarken, Zweden, Noorwegen, Finland, Polen, Tsjechië, Hongarije, het Verenigd Koninkrijk en Ierland</title>",
          f"<title>{TITLE}</title>\n" + seo("Wilde katachtigen in de Benelux, Duitsland, Frankrijk, Oostenrijk, Zwitserland, Italië, Spanje, Portugal, Denemarken, Zweden, Noorwegen, Finland, Polen, Tsjechië, Hongarije, het Verenigd Koninkrijk en Ierland", DESC, SITE)
          + '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
          + f'<link rel="icon" href="{BASE}icon.svg" type="image/svg+xml">\n')
st = sub1(st, '<meta charset="utf-8">', '<meta charset="utf-8"><script>window.__KATBASE="' + BASE + 'soort/";window.__HOMEURL="' + BASE
          + '";window.__IMGP=' + json.dumps(PATHS) + ';</script>')
st = st.replace("<html>", '<html lang="nl">', 1)
wr(ROOT + "index.html", st)

# ------------------------------------------------------------------ website: één soortpagina voor alle landen (/soort/<naam>/)
shutil.rmtree(ROOT + "soort", ignore_errors=True)
CONFC = set("gybr")
KATS = []
for s in D["sp"]:
    al = {s[0]} | set(s[5])
    locs = [(c, l, x[3]) for c in F for l in D[c]["locs"] for x in l[5] if x[4] in al]
    if locs:
        KATS.append((s, locs))
def kat_page(s, locs, inhoud=""):
    conf = [(c, l) for c, l, x in locs if x in CONFC]
    landen = [LAND[c] for c in F if any(cc == c for cc, l in conf)]
    title = f"{s[1]} in Nederland, België, Luxemburg, Duitsland, Frankrijk, Oostenrijk, Zwitserland, Italië, Spanje, Portugal, Denemarken, Zweden, Noorwegen, Finland, Polen, Tsjechië, Hongarije, het Verenigd Koninkrijk en Ierland: waar zie je hem? – Wilde katachtigen-gids"
    if conf:
        desc = kort(f"Waar zie je een {s[1].lower() if s[1] != 'Geoffroy’s kat' else s[1]}? In {opsomming(landen)} op {len(conf)} {'locatie' if len(conf) == 1 else 'locaties'}: "
                    + ", ".join(l[0] for c, l in conf[:6]) + ". Met kaart en recente geboortes.")
    else:
        desc = kort(f"{s[1]} ({s[4]}): vermeldingen in dierentuinen en dierenparken in de Benelux, Duitsland, Frankrijk, Oostenrijk, Zwitserland, Italië, Spanje, Portugal, Denemarken, Zweden, Noorwegen, Finland, Polen, Tsjechië, Hongarije, het Verenigd Koninkrijk en Ierland, met kaart en recente geboortes.")
    url = SITE + "soort/" + s[0] + "/"
    img = SITE + PATHS[s[6]][len(BASE):] if s[6] is not None else SITE + "voorbeeld.jpg"
    doc = re.sub(r"<title>.*?</title>.*?<meta name=\"twitter:card\"[^>]*>\n", "", st, count=1, flags=re.S)
    doc = re.sub(r'<meta property="og:image:width"[^>]*>\n<meta property="og:image:height"[^>]*>\n', "", doc, count=1)
    head = (f"<title>{esc(title)}</title>\n" + seo(title.split(" – ")[0], desc, url, image=img, soort="article")
            + f'<script>window.__KAT="{s[0]}";document.documentElement.classList.add("katmode");</script>\n')
    i = doc.index("<meta charset"); j = doc.index(">", i) + 1
    doc = doc[:j] + "\n" + head + doc[j:]
    return sub1(doc, '<section id="katview"></section>', f'<section id="katview">{inhoud}</section>')
for s, locs in KATS:
    wr(ROOT + "soort/" + s[0] + "/index.html", kat_page(s, locs))
# top 10 om te bezoeken (/top10/)
def top_page():
    title = "Top 10 dierentuinen om wilde katten te zien – Benelux, Duitsland, Frankrijk, Oostenrijk, Zwitserland, Italië, Spanje, Portugal, Denemarken, Zweden, Noorwegen, Finland, Polen, Tsjechië, Hongarije, het Verenigd Koninkrijk en Ierland"
    namen = [D[t["c"]]["locs"][t["i"]][0] for t in D["top10"]]
    desc = kort("De tien parken waar je de meeste en de bijzonderste wilde katten ziet: " + ", ".join(namen) + ".")
    doc = re.sub(r"<title>.*?</title>.*?<meta name=\"twitter:card\"[^>]*>\n", "", st, count=1, flags=re.S)
    doc = re.sub(r'<meta property="og:image:width"[^>]*>\n<meta property="og:image:height"[^>]*>\n', "", doc, count=1)
    head = (f"<title>{esc(title)}</title>\n" + seo(title.split(" – ")[0], desc, SITE + "top10/", soort="article")
            + '<script>window.__TOP=1;document.documentElement.classList.add("katmode");</script>\n')
    i = doc.index("<meta charset"); j = doc.index(">", i) + 1
    return doc[:j] + "\n" + head + doc[j:]
wr(ROOT + "top10/index.html", top_page())

# ------------------------------------------------------------------ website: losse soort- en locatiepagina's

routes = []
for c in [c for c in F if c not in DEEL]:
    sp = {}
    for l in D[c]["locs"]:
        routes.append((c, None, "locatie", l[4], l[0], {"plaats": l[1], "katten": [s[0] for s in l[5]]}))
        for s in l[5]:
            sp.setdefault(s[4], {"naam": s[0], "locs": []})["locs"].append(f"{l[0]} ({l[1]})")
    routes += [(c, None, "soort", k2, v["naam"], {"locs": v["locs"]}) for k2, v in sp.items()]
for c_, stt, o in [(c, st, DATA[c][st]) for c in DEEL for st in DATA[c]]:
    sp = {}
    for l in o["LOCS"]:
        cats = []
        for r in o["R"]:
            if r[2] in l[4] and r[0] not in cats:
                cats.append(r[0])
                sp.setdefault(slug(r[0]), {"naam": r[0], "locs": []})["locs"].append(f"{l[0]} ({l[1]})")
        routes.append((c_, stt, "locatie", slug(l[0]), l[0], {"plaats": l[1], "katten": cats}))
    routes += [(c_, stt, "soort", k2, v["naam"], {"locs": v["locs"]}) for k2, v in sp.items()]

PART = {}
for c, f in F.items():
    doc = WEB[c]
    wr(ROOT + f + "/gids.css", "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", doc, re.S)))
    PART[c] = huisstijl.bovenbalk(["nl"], BASE, taal=False)
    PART[c + "_kofi"] = huisstijl.voet(["nl"])

def guide_url(c, st_, kind=None, s=None):
    h = (st_ + ("/" + kind + "/" + s if kind else "")) if st_ else (kind + "/" + s if kind else "")
    return BASE + F[c] + "/" + ("#" + h if h else "")
def static_url(c, st_, kind, s):
    return BASE + F[c] + "/" + (st_ + "/" if st_ else "") + kind + "/" + s + "/"
LANDSOORTEN = {c: {slug(r[0]) for r in DATA[c]["main"]["R"]} for c in F}   # soorten met een eigen pagina per land
def rewrite(frag, c, st_):
    def fix(mm):
        h = mm.group(1)
        r = re.match(r"#(?:([a-z-]+)/)?(soort|locatie)/([a-z0-9-]+)$", h)
        if r and ((st_ is None and r.group(1) is None) or (st_ and r.group(1) in (None, st_))):
            if r.group(2) == "soort" and not st_ and r.group(3) not in LANDSOORTEN[c]:
                # soort zonder pagina in dit land ("lijkt op"): naar de Europese soortpagina, anders de Spottersgids, anders de gids
                s = r.group(3)
                if os.path.exists(ROOT + "soort/" + s + "/index.html"): return f'href="{BASE}soort/{s}/"'
                if os.path.exists(ROOT + "spottersgids/" + s + "/index.html"): return f'href="{BASE}spottersgids/{s}/"'
                return f'href="{guide_url(c, None, "soort", s)}"'
            return f'href="{static_url(c, st_, r.group(2), r.group(3))}"'
        rest = h[1:]
        if st_ and not rest.startswith(st_):
            rest = st_ + ("/" + rest if rest else "")
        return f'href="{BASE}{F[c]}/{"#" + rest if rest else ""}"'
    return re.sub(r'href="(#[^"]*)"', fix, frag)

def page(c, st_, kind, s, naam, extra, frag):
    plek = (DEEL[c][st_] + " (" + LAND[c] + ")") if st_ else LAND[c]
    if kind == "soort":
        title = f"{naam} in {plek}: in welke dierentuinen te zien? – Wilde katachtigen-gids"
        desc = kort(f"{naam} is in {plek} te zien bij {opsomming(extra['locs'])}. Met status, aantallen en bezoekinformatie per park.")
    else:
        cats = extra["katten"]
        title = f"{naam} ({plaats_kort(extra['plaats'])}): welke wilde katten zie je er? – Wilde katachtigen-gids"
        desc = kort((f"Bij {naam} in {extra['plaats']} zie je {opsomming([x if x == 'Geoffroy’s kat' else x.lower() for x in cats])}. " if cats
                     else f"{naam} in {extra['plaats']}. ") + "Met informatie over de katten, openingstijden en bezoek.")
    url = "https://yeetkitty.github.io" + static_url(c, st_, kind, s)
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
{seo(title.split(' – ')[0], desc, url, soort='article')}<link rel="preconnect" href="https://fonts.googleapis.com">
{huisstijl.FONTS}
<link rel="stylesheet" href="{BASE}{F[c]}/gids.css">
<style>.gidslink{{margin-top:14px}}.gidslink a{{display:inline-flex;align-items:center;gap:8px;font-family:"Alegreya Sans",system-ui,sans-serif;font-size:16px;font-weight:700;color:#F0EEE2;background:#1E2318;border:1px solid #1E2318;border-radius:999px;padding:8px 16px;text-decoration:none}}.gidslink a:hover{{background:#46552E;border-color:#46552E}}#info[hidden]{{display:block!important}}</style>
</head>
<body>
{PART[c]}
<div class="wrap gidslink"><a href="{guide_url(c, st_, kind, s)}">Open de interactieve gids van {esc(plek)} →</a></div>
<div class="wrap" id="info">
{rewrite(frag["html"], c, st_)}
</div>
{PART[c + '_kofi']}
{huisstijl.JS}</body>
</html>
"""

async def snapshots():
    from playwright.async_api import async_playwright
    tmp = tempfile.mkdtemp()
    os.symlink(ROOT.rstrip("/"), tmp + "/wildekattengids")
    srv = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(type("Q", (SimpleHTTPRequestHandler,), {"log_message": lambda *a: None}), directory=tmp))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    local = f"http://127.0.0.1:{srv.server_address[1]}{BASE}"
    res = {}
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page(locale="nl-NL", viewport={"width": 1100, "height": 900})
        cur = None
        for (c, st_, kind, s, naam, extra) in routes:
            h = (st_ + "/" if st_ else "") + kind + "/" + s
            if cur != (c, st_):
                await pg.goto(local + F[c] + "/#" + h)
                await pg.wait_for_timeout(1800 if c in DEEL else 900)
                cur = (c, st_)
            else:
                await pg.evaluate(f"location.hash={json.dumps('#' + h)}")
                await pg.wait_for_timeout(350)
            ok = await pg.evaluate("()=>{const i=document.getElementById('info');return !!(i&&!i.hidden&&i.querySelector('h1'))}")
            if not ok:
                print("niet gelukt:", c, st_, kind, s)
                continue
            res[(c, st_, kind, s)] = await pg.evaluate("""()=>{const i=document.getElementById('info').cloneNode(true);
                i.querySelectorAll('.langsw,[data-setlang]').forEach(e=>{(e.closest('.langsw')||e).remove();});
                i.querySelectorAll('script').forEach(e=>e.remove());
                return {html:i.innerHTML,h1:i.querySelector('h1').textContent.trim()};}""")
        for s, locs in KATS:
            await pg.goto(local + "soort/" + s[0] + "/")
            await pg.wait_for_timeout(300)
            h1 = await pg.evaluate("()=>{const e=document.querySelector('#katview h1');return e?e.textContent.trim():''}")
            if h1 != s[1]:
                sys.exit(f"bouw gestopt: soortpagina {s[0]} niet goed ({h1!r})")
            res[("kat", s[0])] = await pg.evaluate("()=>document.getElementById('katview').innerHTML")
        await br.close()
    srv.shutdown()
    shutil.rmtree(tmp)
    return res

import asyncio
res = asyncio.run(snapshots())
urls = [SITE, SITE + "top10/"] + [SITE + f + "/" for f in F.values()] + [SITE + F[c] + "/" + s + "/" for c, s, _ in DEELPAG]
for s, locs in KATS:
    wr(ROOT + "soort/" + s[0] + "/index.html", kat_page(s, locs, res[("kat", s[0])]))
    urls.append(SITE + "soort/" + s[0] + "/")
for r in routes:
    key = r[:4]
    if key not in res:
        continue
    fr_ = res[key]
    if r[4].lower() not in fr_["h1"].lower() and fr_["h1"].lower() not in r[4].lower():
        sys.exit(f"bouw gestopt: verkeerde pagina vastgelegd voor {key}: {fr_['h1']}")
    u = static_url(*key)
    wr(ROOT + u[len(BASE):] + "index.html", page(*r, fr_))
    urls.append("https://yeetkitty.github.io" + u)
# Spottersgids (eigen bouw in spottersgids/) meenemen in de hoofd-sitemap
if os.path.exists(ROOT + "spottersgids/sitemap.xml"):
    urls += [u for u in re.findall(r"<loc>([^<]+)</loc>", rd(ROOT + "spottersgids/sitemap.xml")) if u not in urls]
wr(ROOT + "sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
   + "".join(f"  <url><loc>{u}</loc><lastmod>{today.isoformat()}</lastmod></url>\n" for u in urls) + "</urlset>\n")
# oude adressen na hernoemen van soorten in de Duitse gids (okt 2026) → doorverwijzen
OUD = {"cheeta": "cheetah", "luipaardkat": "bengaalse-kat", "pampakat": "colocolo", "andeskat": "andesbergkat"}
for st_ in STATES:
    for o, n in OUD.items():
        doel = static_url("de", None, "soort", n)   # sinds 18-10-2026 één Duitslandpagina
        if os.path.exists(ROOT + doel[len(BASE):] + "index.html") and not os.path.exists(ROOT + "duitsland/" + st_ + "/soort/" + o + "/index.html"):
            wr(ROOT + "duitsland/" + st_ + "/soort/" + o + "/index.html",
               f'<!DOCTYPE html><html lang="nl"><head><meta charset="UTF-8"><title>Doorverwijzing</title><link rel="canonical" href="https://yeetkitty.github.io{doel}">'
               f'<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={doel}"></head><body><a href="{doel}">Ga verder</a></body></html>\n')
def doorverwijzing(pad, doel):
    wr(ROOT + pad + "index.html", f'<!DOCTYPE html><html lang="nl"><head><meta charset="UTF-8"><title>Doorverwijzing</title><link rel="canonical" href="https://yeetkitty.github.io{doel}">'
       f'<meta name="robots" content="noindex"><script>var h=location.hash.slice(1);location.replace("{doel}"+(h&&"{doel}".indexOf("#")>=0?"/"+h:""));</script>'
       f'<meta http-equiv="refresh" content="0; url={doel}"></head><body><a href="{doel}">Ga verder</a></body></html>\n')
for c, regs in OUD_DEEL.items():
    m0 = DATA[c]["main"]; rg = m0.get("REGIO") or {}
    for st_ in regs:
        doorverwijzing(F[c] + "/" + st_ + "/", BASE + F[c] + "/#" + st_)
    for l in D[c]["locs"]:
        st_ = rg.get(l[0])
        if st_:
            doorverwijzing(F[c] + "/" + st_ + "/locatie/" + l[4] + "/", static_url(c, None, "locatie", l[4]))
            for x in l[5]:
                if os.path.exists(ROOT + static_url(c, None, "soort", x[4])[len(BASE):] + "index.html") and not os.path.exists(ROOT + F[c] + "/" + st_ + "/soort/" + x[4] + "/index.html"):
                    doorverwijzing(F[c] + "/" + st_ + "/soort/" + x[4] + "/", static_url(c, None, "soort", x[4]))
wr(ROOT + "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
print("Website:", len(urls), "pagina's")

# nieuw ontwerp landpagina's (17-10-2026): zet het nieuwe ontwerp op /<land>/, oude pagina als reserve op /<land>-oud/ (zie bron/nieuw_ontwerp.py)
import nieuw_ontwerp; nieuw_ontwerp.maak(); nieuw_ontwerp.maak_los(); nieuw_ontwerp.maak_start()   # losse park- en soortpagina's ook in de nieuwe stijl (18-10-2026)

# ontwerp landpagina's (18-10-2026): opbouw van de hoofdpagina op alle landen (zie bron/test_ontwerp.py)
try:
    import test_ontwerp; test_ontwerp.maak_alles()
except Exception as e:
    print("testontwerp overgeslagen:", e)

# jungle-stijl (18-10-2026): vormgeving "Expeditie" als losse laag over alle pagina's, als allerlaatste stap (zie bron/jungle.py)
import jungle; jungle.maak()

# één hoofdkop per pagina (19-10-2026): op /soort/<naam>/ en /top10/ zitten de koppen van de startpagina verborgen in de pagina.
# Die worden h2, zodat de soortnaam (in #katview) de enige h1 is. Ze zijn op deze pagina's nooit zichtbaar (elke knop opent de startpagina).
def een_hoofdkop(pad):
    doc = rd(pad)
    stukken = re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<section id="katview">.*?</section>)', doc, flags=re.S)
    for i in range(0, len(stukken), 2):
        stukken[i] = re.sub(r"<(/?)h1\b", r"<\1h2", stukken[i])
    wr(pad, "".join(stukken))
for pad in [ROOT + "top10/index.html"] + [ROOT + "soort/" + d + "/index.html" for d in sorted(os.listdir(ROOT + "soort"))]:
    if os.path.exists(pad):
        een_hoofdkop(pad)
