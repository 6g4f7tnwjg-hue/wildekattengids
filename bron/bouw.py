#!/usr/bin/env python3
"""Bouwt de Wilde katachtigen-gids uit één bron.

Bron (map bron/):
  gidsen/nl.html, be.html, lu.html, de.html  – de landengidsen (foto's als @@IMGn@@)
  start.html                                  – de startpagina (de gegevens in "const D" worden hier opnieuw berekend)
  ../img/                                     – alle foto's (n.webp / n.jpg …), nummer = n in @@IMGn@@
  artifact_kop.html, web_kop.html             – vaste kopjes voor de Claude-pagina en de website
  franse_namen.json                           – Franse soortnamen voor de startgegevens

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
from startdata import bereken, slug, soorten

BASE = "/wildekattengids/"
SITE = "https://yeetkitty.github.io" + BASE
F = {"nl": "nederland", "be": "belgie", "lu": "luxemburg", "de": "duitsland"}
LAND = {"nl": "Nederland", "be": "België", "lu": "Luxemburg", "de": "Duitsland"}
STATES = {"bayern": "Bayern", "nedersaksen": "Nedersaksen", "nrw": "Noordrijn-Westfalen", "saksen": "Saksen", "berlijn": "Berlijn"}
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
    if '<script type="application/json" id="ds-' in t:
        def fix(mm):
            d = json.loads(mm.group(2))
            d["js"] = sub1(d["js"], LT_HOOK, LT_HOOK + LT_JS.replace("</", "<\\/"))
            return mm.group(1) + json.dumps(d, ensure_ascii=False).replace("</", "<\\/") + mm.group(3)
        return re.sub(r'(<script type="application/json" id="ds-[a-z-]+">)(.*?)(</script>)', fix, t, flags=re.S)
    return sub1(t, LT_HOOK, LT_HOOK + LT_JS.replace("</", "<\\/"))
G = {c: met_types(t) for c, t in G.items()}
imgs = sorted((f for f in os.listdir(ROOT + "img") if re.match(r"^\d+\.\w+$", f)), key=lambda f: int(f.split(".")[0]))
assert [int(f.split(".")[0]) for f in imgs] == list(range(len(imgs))), "fotonummers moeten aaneengesloten zijn"

# ------------------------------------------------------------------ startgegevens opnieuw berekenen
DATA = {c: json.loads(subprocess.check_output(["node", BRON + "extract.js", BRON + f"gidsen/{c}.html"])) for c in F}
m = re.search(r"const D=(\{.*?\});\n", START)
D = json.loads(m.group(1))
fr = json.load(open(BRON + "franse_namen.json", encoding="utf8"))
today = datetime.date.today()
for c in F:
    D[c] = bereken(DATA[c], D[c], today, fr)
D["sp"] = soorten(DATA, fr, today)
D["lt"] = {"types": [{k: t[k] for k in ("nl", "en", "uitleg", "uitleg_en")} for t in LTJ["types"]],
           "labels": [{k: l[k] for k in ("key", "nl", "en", "icoon")} for l in LTJ["labels"]]}
START = START[:m.start(1)] + json.dumps(D, ensure_ascii=False, separators=(",", ":")) + START[m.end(1):]
wr(BRON + "start.html", START)

# ------------------------------------------------------------------ Claude-pagina
IMG = ["data:%s;base64,%s" % (MIME[f.split(".")[1]], base64.b64encode(open(ROOT + "img/" + f, "rb").read()).decode()) for f in imgs]
k = START.index("<script>\n(function(){")
claude = (rd(BRON + "artifact_kop.html") + "<script>window.__IMG=" + json.dumps(IMG) + ";\nwindow.__G=" + js(G)
          + ";\nwindow.__START=" + js(START) + ";</script>\n" + START[k:])
wr(ROOT + "_claude/claude.html", claude)
print("Claude-pagina:", ROOT + "_claude/claude.html", round(len(claude.encode()) / 1e6, 1), "MB")
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
        "fr": "Votre signalement est envoyé directement à l’auteur du guide et n’est pas public. Si vous souhaitez une réponse, indiquez votre adresse e-mail dans les commentaires."}
RPWEB = r'''async function rpWeb(d){
  const btn=rpEl("rp-go");btn.disabled=true;rpMsg(T("Bezig met versturen…","Sending…","Envoi en cours…"));
  const body={access_key:window.__W3F.key,subject:"Melding gids "+window.__W3F.land+": "+d.type+" – "+d.loc,from_name:"Wilde katachtigen-gids",
    Melding:rpEl("rp-sum").textContent.trim(),Soort_melding:d.type,Locatie:d.loc,Soort:d.soort,Datum_bezoek:d.datum||"-",Opmerkingen:d.opm||"-",
    Gids:window.__W3F.land,Pagina:location.href,Taal:(typeof LANG!=="undefined"?LANG:"nl"),botcheck:""};
  try{
    const r=await fetch("https://api.web3forms.com/submit",{method:"POST",headers:{"Content-Type":"application/json","Accept":"application/json"},body:JSON.stringify(body)});
    const j=await r.json().catch(()=>({}));
    if(!(r.ok&&j.success))throw new Error("mislukt");
    rpEl("rp-opm").value="";rpUpdate();
    rpMsg(T("Bedankt! Je melding is verstuurd.","Thank you! Your report has been sent.","Merci ! Votre signalement a été envoyé."));
  }catch(e){
    rpMsg(T("Versturen is niet gelukt. Probeer het later opnieuw.","Sending failed. Please try again later.","L’envoi a échoué. Veuillez réessayer plus tard."),true);
  }
  btn.disabled=false;
}
'''
def meld_js(t):
    t = sub1(t, "} else {COMMENTS=null;rpUit();} }", "} else if(window.__W3F){COMMENTS={};} else {COMMENTS=null;rpUit();} }")
    t = sub1(t, "  if(COMMENTS===undefined){", "  if(window.__W3F){rpUpdate();return rpWeb(d);}\n  if(COMMENTS===undefined){")
    return sub1(t, "function rpUit(){", RPWEB + "function rpUit(){")
def meld_note(h):
    mm = re.search(r'(<p class="prose" style="font-size:14.5px;color:var\(--muted\)">)(<span class="l-nl">Na het klikken opent een reactievenster.*?)(</p>)', h, re.S)
    assert mm, "uitleg meldformulier niet gevonden"
    spans = re.findall(r'<span class="l-(\w\w)">', mm.group(2))
    return h[:mm.start(2)] + "".join(f'<span class="l-{l}">{NOTE[l]}</span>' for l in spans) + h[mm.end(2):]
def meld(doc, land):
    i = doc.index("<meta charset"); j = doc.index(">", i) + 1
    doc = doc[:j] + f'\n<script>window.__W3F={{key:"{W3F_KEY}",land:"{land}"}};</script>\n' + doc[j:]
    if "ds-" in doc and '<script type="application/json" id="ds-' in doc:
        def fix(mm):
            d = json.loads(mm.group(2))
            d["js"] = meld_js(d["js"]); d["html"] = meld_note(d["html"])
            return mm.group(1) + json.dumps(d, ensure_ascii=False).replace("</", "<\\/") + mm.group(3)
        doc = re.sub(r'(<script type="application/json" id="ds-[a-z-]+">)(.*?)(</script>)', fix, doc, flags=re.S)
        return doc
    return meld_note(meld_js(doc))

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
    "de": ("Wilde katachtigen in Duitsland – welke wilde katten in welke dierentuin?",
           "Welke wilde katten zie je in Duitse dierentuinen, Tierparks en Wildparks? Per deelstaat, per soort en per park, met kaart, routeplanner en recente geboortes."),
}
HOME_JS = 'if(window.__home){window.__home();}else{location.reload();}'
WEB = {}
for c, doc in G.items():
    doc = fotos(doc)
    doc = sub1(doc, HOME_JS, f'location.href="{BASE}";')
    doc = sub1(doc, '<a href="#" id="naar-landen">', f'<a href="{BASE}" id="naar-landen">')
    t, d = CTRY[c]
    doc = re.sub(r"<title>[^<]*</title>", lambda mm: f"<title>{t}</title>\n" + seo(t, d, SITE + F[c] + "/"), doc, count=1)
    WEB[c] = doc   # zonder meldformulier-aanpassing (voor de stijl en momentopnames)
    wr(ROOT + F[c] + "/index.html", meld(doc, LAND[c]))
de_web = rd(ROOT + "duitsland/index.html")
for st, nm in STATES.items():
    o = DATA["de"][st]
    cats = []
    for r in o["R"]:
        if r[0] not in cats:
            cats.append(r[0])
    t = f"Wilde katachtigen in {nm} – welke wilde katten in welke dierentuin?"
    d = f"Welke wilde katten zie je in {nm}? {len(o['LOCS'])} dierentuinen, Tierparks en Wildparks met o.a. {', '.join(x.lower() for x in cats[:4])}. Met kaart, routeplanner en recente geboortes."
    url = SITE + "duitsland/" + st + "/"
    doc = re.sub(r'<title>.*?</title>.*?<meta name="twitter:card"[^>]*>\n', "", de_web, count=1, flags=re.S)
    force = ('<script>(function(){var h=decodeURIComponent(location.hash.slice(1));if(!/^' + st + '(\\/|$)/.test(h)){try{history.replaceState(null,"","#'
             + st + '"+(h&&h!=="de"?"/"+h:""));}catch(e){}}})();</script>\n')
    head = f"<title>{t}</title>\n" + seo(f"Wilde katachtigen in {nm}", d, url) + force
    i = doc.index("<meta charset"); j = doc.index(">", i) + 1
    wr(ROOT + f"duitsland/{st}/index.html", doc[:j] + "\n" + head + doc[j:])

# ------------------------------------------------------------------ website: startpagina
st = START
fmap = "{" + ",".join(f'{c}:"{BASE}{v}/"' for c, v in F.items()) + "}"
st = sub1(st, "window.openCountry=function(c,h){",
          f"window.__F={fmap};\n  window.openCountry=function(c,h){{location.replace(window.__F[c]+(h?\"#\"+h:\"\"));return;")
st = st.replace("${c}.html", "${window.__F[c]}").replace("${ZOOM}.html", "${window.__F[ZOOM]}")
TITLE = "Wilde katachtigen in de Benelux en Duitsland – waar zie je welke wilde kat?"
DESC = ("Gids van J. Gelens: welke wilde katten – leeuw, tijger, luipaard, lynx, serval, manoel en meer – je in dierentuinen, "
        "dierenparken en opvangcentra in Nederland, België, Luxemburg en Duitsland kunt zien. Met kaart, routeplanner en recente geboortes.")
st = sub1(st, "<title>Wilde katachtigen in de Benelux en Duitsland</title>",
          f"<title>{TITLE}</title>\n" + seo("Wilde katachtigen in de Benelux en Duitsland", DESC, SITE)
          + '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n')
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
    title = f"{s[1]} in Nederland, België, Luxemburg en Duitsland: waar zie je hem? – Wilde katachtigen-gids"
    if conf:
        desc = kort(f"Waar zie je een {s[1].lower() if s[1] != 'Geoffroy’s kat' else s[1]}? In {opsomming(landen)} op {len(conf)} {'locatie' if len(conf) == 1 else 'locaties'}: "
                    + ", ".join(l[0] for c, l in conf[:6]) + ". Met kaart en recente geboortes.")
    else:
        desc = kort(f"{s[1]} ({s[4]}): vermeldingen in dierentuinen en dierenparken in de Benelux en Duitsland, met kaart en recente geboortes.")
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

# ------------------------------------------------------------------ website: losse soort- en locatiepagina's

routes = []
for c in ["nl", "be", "lu"]:
    sp = {}
    for l in D[c]["locs"]:
        routes.append((c, None, "locatie", l[4], l[0], {"plaats": l[1], "katten": [s[0] for s in l[5]]}))
        for s in l[5]:
            sp.setdefault(s[4], {"naam": s[0], "locs": []})["locs"].append(f"{l[0]} ({l[1]})")
    routes += [(c, None, "soort", k2, v["naam"], {"locs": v["locs"]}) for k2, v in sp.items()]
for stt, o in DATA["de"].items():
    sp = {}
    for l in o["LOCS"]:
        cats = []
        for r in o["R"]:
            if r[2] in l[4] and r[0] not in cats:
                cats.append(r[0])
                sp.setdefault(slug(r[0]), {"naam": r[0], "locs": []})["locs"].append(f"{l[0]} ({l[1]})")
        routes.append(("de", stt, "locatie", slug(l[0]), l[0], {"plaats": l[1], "katten": cats}))
    routes += [("de", stt, "soort", k2, v["naam"], {"locs": v["locs"]}) for k2, v in sp.items()]

PART = {}
for c, f in F.items():
    doc = WEB[c]
    wr(ROOT + f + "/gids.css", "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", doc, re.S)))
    PART[c] = re.search(r'<nav class="landbar".*?</nav>', doc, re.S).group(0)
    PART[c + "_kofi"] = re.search(r'<div class="kofi-wrap">.*?</aside></div>', doc, re.S).group(0)

def guide_url(c, st_, kind=None, s=None):
    h = (st_ + ("/" + kind + "/" + s if kind else "")) if st_ else (kind + "/" + s if kind else "")
    return BASE + F[c] + "/" + ("#" + h if h else "")
def static_url(c, st_, kind, s):
    return BASE + F[c] + "/" + (st_ + "/" if st_ else "") + kind + "/" + s + "/"
def rewrite(frag, c, st_):
    def fix(mm):
        h = mm.group(1)
        r = re.match(r"#(?:([a-z-]+)/)?(soort|locatie)/([a-z0-9-]+)$", h)
        if r and ((st_ is None and r.group(1) is None) or (st_ and r.group(1) in (None, st_))):
            return f'href="{static_url(c, st_, r.group(2), r.group(3))}"'
        rest = h[1:]
        if st_ and not rest.startswith(st_):
            rest = st_ + ("/" + rest if rest else "")
        return f'href="{BASE}{F[c]}/{"#" + rest if rest else ""}"'
    return re.sub(r'href="(#[^"]*)"', fix, frag)

def page(c, st_, kind, s, naam, extra, frag):
    plek = (STATES[st_] + " (Duitsland)") if st_ else LAND[c]
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
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{BASE}{F[c]}/gids.css">
<style>.gidslink{{margin-top:14px}}.gidslink a{{display:inline-flex;align-items:center;gap:8px;font-family:"Bricolage Grotesque",system-ui,sans-serif;font-size:15px;font-weight:600;color:#2A1C12;background:#F2DFB6;border:1.5px solid #D9BE86;border-radius:999px;padding:8px 14px;text-decoration:none}}.gidslink a:hover{{border-color:#5A3E2B}}#info[hidden]{{display:block!important}}</style>
</head>
<body>
{PART[c]}
<div class="wrap gidslink"><a href="{guide_url(c, st_, kind, s)}">Open de interactieve gids van {esc(plek)} →</a></div>
<div class="wrap" id="info">
{rewrite(frag["html"], c, st_)}
</div>
{PART[c + '_kofi']}
</body>
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
                await pg.wait_for_timeout(1800 if c == "de" else 900)
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
urls = [SITE] + [SITE + f + "/" for f in F.values()] + [SITE + "duitsland/" + s + "/" for s in STATES]
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
wr(ROOT + "sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
   + "".join(f"  <url><loc>{u}</loc><lastmod>{today.isoformat()}</lastmod></url>\n" for u in urls) + "</urlset>\n")
# oude adressen na hernoemen van soorten in de Duitse gids (okt 2026) → doorverwijzen
OUD = {"cheeta": "cheetah", "luipaardkat": "bengaalse-kat", "pampakat": "colocolo", "andeskat": "andesbergkat"}
for st_ in STATES:
    for o, n in OUD.items():
        doel = BASE + "duitsland/" + st_ + "/soort/" + n + "/"
        if os.path.exists(ROOT + doel[len(BASE):] + "index.html") and not os.path.exists(ROOT + "duitsland/" + st_ + "/soort/" + o + "/index.html"):
            wr(ROOT + "duitsland/" + st_ + "/soort/" + o + "/index.html",
               f'<!DOCTYPE html><html lang="nl"><head><meta charset="UTF-8"><title>Doorverwijzing</title><link rel="canonical" href="https://yeetkitty.github.io{doel}">'
               f'<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={doel}"></head><body><a href="{doel}">Ga verder</a></body></html>\n')
wr(ROOT + "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
print("Website:", len(urls), "pagina's")
