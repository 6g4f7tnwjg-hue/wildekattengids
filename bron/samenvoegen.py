# Zet een gids met aparte pagina's per deelstaat/regio (Oostenrijk, Zwitserland, Frankrijk, VK) om naar één pagina
# met een regiofilter, zoals Italië en Spanje. Eenmalig gebruikt op 17-10-2026; de oude versie staat in git.
# Gebruik: python3 bron/samenvoegen.py at   (schrijft bron/gidsen/at.html)
import re, json, sys, subprocess, html as H

BRON = __file__.rsplit("/", 1)[0] + "/"
c = sys.argv[1]

# landnamen en vaste zinnen per taal (volgorde = talen van de gids)
LANDEN = {
    "at": {"langs": ["nl", "en", "de"], "naam": ["Oostenrijk", "Austria", "Österreich"], "in": ["in Oostenrijk", "in Austria", "in Österreich"],
           "van": ["van Oostenrijk", "of Austria", "von Österreich"], "regio": ["Deelstaat", "State", "Bundesland"], "regios": ["Alle deelstaten", "All states", "Alle Bundesländer"],
           "filter": ["Filter op deelstaat", "Filter by state", "Nach Bundesland filtern"]},
    "ch": {"langs": ["nl", "en", "de", "fr", "it"], "naam": ["Zwitserland", "Switzerland", "Schweiz", "Suisse", "Svizzera"],
           "in": ["in Zwitserland", "in Switzerland", "in der Schweiz", "en Suisse", "in Svizzera"], "van": ["van Zwitserland", "of Switzerland", "der Schweiz", "de la Suisse", "della Svizzera"],
           "regio": ["Regio", "Region", "Region", "Région", "Regione"], "regios": ["Alle regio’s", "All regions", "Alle Regionen", "Toutes les régions", "Tutte le regioni"],
           "filter": ["Filter op regio", "Filter by region", "Nach Region filtern", "Filtrer par région", "Filtra per regione"]},
    "fr": {"langs": ["nl", "en", "fr"], "naam": ["Frankrijk", "France", "France"], "in": ["in Frankrijk", "in France", "en France"],
           "van": ["van Frankrijk", "of France", "de la France"], "regio": ["Regio", "Region", "Région"], "regios": ["Alle regio’s", "All regions", "Toutes les régions"],
           "filter": ["Filter op regio", "Filter by region", "Filtrer par région"]},
    "uk": {"langs": ["nl", "en"], "naam": ["het Verenigd Koninkrijk", "the United Kingdom"], "in": ["in het Verenigd Koninkrijk", "in the United Kingdom"],
           "van": ["van het Verenigd Koninkrijk", "of the United Kingdom"], "regio": ["Regio", "Region"], "regios": ["Alle regio’s", "All regions"],
           "filter": ["Filter op regio", "Filter by region"]},
}
L = LANDEN[c]; LG = L["langs"]
def zin(per):   # {taal: tekst} → spans
    return "".join(f'<span class="l-{l}">{per[l]}</span>' for l in LG)
def Tjs(per):   # {taal: tekst} → T("nl","en",…) met zoveel argumenten als de gids talen heeft
    return "T(" + ",".join(json.dumps(per[l], ensure_ascii=False) for l in LG) + ")"
I = {l: L["in"][k] for k, l in enumerate(LG)}
N = {l: L["naam"][k] for k, l in enumerate(LG)}
V = {l: L["van"][k] for k, l in enumerate(LG)}

src = open(BRON + f"gidsen/{c}.html", encoding="utf-8").read()
blocks = [(m.group(1), json.loads(m.group(2))) for m in re.finditer(r'<script type="application/json" id="ds-([a-z-]+)">(.*?)</script>', src, re.S)]
DSN0 = json.loads(re.search(r"const DSN0=(\{.*?\});", src).group(1))
START_T = json.loads(re.search(r"START_T=(\[.*?\]);", src).group(1))
keys = [k for k in DSN0 if any(b[0] == k for b in blocks)]
B = dict(blocks)
rn = lambda k: {l: DSN0[k][i] for i, l in enumerate(LG)}

# ------------------------------------------------------------------ gegevens samenvoegen
def lees(js):
    return json.loads(subprocess.run(["node", BRON + "lit.js"], input=js, capture_output=True, text=True, check=True).stdout)
P = {k: lees(B[k]["js"]) for k in keys}
k0 = max(keys, key=lambda k: len(P[k]["const"]["LOCS"]))     # sjabloon: de regio met de meeste locaties
tpl_js = B[k0]["js"]
lines = tpl_js.split("\n")
common = set.intersection(*[set(B[k]["js"].split("\n")) for k in keys])
def sv(v):
    if isinstance(v, dict) and "__set" in v:
        return "new Set(" + json.dumps(v["__set"], ensure_ascii=False) + ")"
    return json.dumps(v, ensure_ascii=False)

C = {k: P[k]["const"] for k in keys}
SPEC = C[k0]["SPECIES"] if "SPECIES" in C[k0] else None
R, _z = [], set()
for k in keys:
    for r in C[k]["R"]:
        if json.dumps(r) not in _z: _z.add(json.dumps(r)); R.append(r)
LOCS, REGIO = [], {}
for k in keys:   # een locatie die in twee regio's stond (grensgeval) telt één keer, bij de eerste regio
    for l in C[k]["LOCS"]:
        if l[0] not in REGIO: REGIO[l[0]] = k; LOCS.append(l[:5])   # zonder de verschuiving per regio (andere schaal)
YOUNG = [y for k in keys for y in C[k].get("YOUNG", [])]
order = [s[0] for s in json.loads(subprocess.run(["node", "-e", "const fs=require('fs');const j=fs.readFileSync(0,'utf8');const i=j.indexOf('const SPECIES=');let d=0,k=j.indexOf('[',i);const s=k;for(;k<j.length;k++){if(j[k]=='[')d++;else if(j[k]==']'){d--;if(!d)break;}}process.stdout.write(JSON.stringify(eval(j.slice(s,k+1))))"], input=tpl_js, capture_output=True, text=True, check=True).stdout)]
def setunion(name):
    s = []
    for k in keys:
        for x in C[k][name]["__set"] if isinstance(C[k][name], dict) else C[k][name]:
            if x not in s: s.append(x)
    return s
present = {r[0] for r in R}
big = sorted(setunion("BIG"), key=order.index); small = sorted(setunion("SMALL"), key=order.index)
locs_per_sp = {}
for r in R:
    if any(x in "gr" for x in r[4].split("+")):
        locs_per_sp.setdefault(r[0], set()).add(r[2])
unique = [s for s in order if len(locs_per_sp.get(s, ())) == 1]

# route met alle soorten (gretig): steeds het park met de meeste nog ontbrekende soorten
noroute = set(setunion("NOROUTE")) if "NOROUTE" in C[k0] else set()
park_sp = {}
for r in R:
    if any(x == "g" for x in r[4].split("+")) and r[2] not in noroute:
        park_sp.setdefault(r[2], set()).add(r[0])
need = set().union(*park_sp.values()); route = []
while need:
    p = max(park_sp, key=lambda p: (len(park_sp[p] & need), -len(route)))
    if not park_sp[p] & need: break
    route.append(p); need -= park_sp[p]
locnames = [l[0] for l in LOCS]
route = [next((l[0] for l in LOCS if p == l[0] or p in l[4]), p) for p in route]

# kaart: alle regio's samen, nieuwe projectie
polys = []
for k in keys:
    polys.append(C[k]["MAIN"]); polys += C[k].get("ISLANDS", [])
lons = [p[0] for pg in polys for p in pg]; lats = [p[1] for pg in polys for p in pg]
lo0, lo1, la0, la1 = min(lons), max(lons), max(lats), min(lats)
import math
kx = math.cos(math.radians((la0 + la1) / 2)); S = 340 / ((lo1 - lo0) * kx)
W, Hh = 360, round((la0 - la1) * S + 20)
PX = f'const PX=(lo,la)=>[((lo-({lo0:.4f}))*{kx:.4f}*{S:.2f}+10).toFixed(1),(({la0:.4f}-la)*{S:.2f}+10).toFixed(1)];'

merged = {}
for k in keys:
    for n, v in C[k].items():
        if isinstance(v, dict) and "__set" not in v:
            merged.setdefault(n, {}).update(v)
special = {"R": R, "LOCS": LOCS, "YOUNG": YOUNG, "BIG": big, "SMALL": small, "UNIQUE": {"__set": unique},
           "UNSURE": {"__set": setunion("UNSURE")}, "MAIN": polys[0], "ISLANDS": polys[1:], "LINES": [],
           "NOROUTE": {"__set": sorted(noroute)}}
ASSIGN = {}
for k in keys:
    for n, v in P[k]["assign"].items(): ASSIGN.setdefault(n, {}).update(v)

out = []
for line in lines:
    m = re.match(r"^(\s*)(const|let) ([A-Za-z_][A-Za-z_0-9]*)\s*=", line)
    if m and (line not in common or m.group(3) in ("MAIN", "ISLANDS", "LINES")):   # kaartvormen altijd vervangen
        n = m.group(3)
        if n == "PX": out.append(PX); continue
        if n.startswith("TITLE_"):
            l = n[6:].lower(); out.append(f'const {n}={json.dumps(START_T[LG.index(l) if l in LG else min(2, len(START_T) - 1)], ensure_ascii=False)};'); continue
        if n in special: out.append(f"{m.group(1)}{m.group(2)} {n}={sv(special[n])};"); continue
        if n in merged: out.append(f"{m.group(1)}{m.group(2)} {n}={sv(merged[n])};"); continue
        sys.exit("onbekende regel: " + line[:120])
    m = re.match(r"^\s*Object\.assign\(([A-Za-z_0-9]+),", line)
    if m and line not in common:
        out.append(f"Object.assign({m.group(1)},{json.dumps(ASSIGN[m.group(1)], ensure_ascii=False)});"); continue
    out.append(line)
js = "\n".join(out)
# regels met de naam van de sjabloonregio
n0 = rn(k0)
def vervang(old, new):
    global js
    if js.count(old) < 1: sys.exit("niet gevonden: " + old)
    js = js.replace(old, new)
vervang(f'T("Deze soort is op dit moment niet te zien in {n0["nl"]}.","This species is currently not on view in {n0["en"]}.")',
        Tjs({"nl": f'Deze soort is op dit moment niet te zien {I["nl"]}.', "en": f'This species is currently not on view {I["en"]}.',
             "de": f'Diese Art ist derzeit {I.get("de","")} nicht zu sehen.', "fr": f'Cette espèce n’est actuellement pas visible {I.get("fr","")}.',
             "it": f'Questa specie al momento non è visibile {I.get("it","")}.'}))
vervang(f'T("Waar te zien in {n0["nl"]}","Where to see it in {n0["en"]}")',
        Tjs({"nl": f'Waar te zien {I["nl"]}', "en": f'Where to see it {I["en"]}', "de": f'Wo zu sehen {I.get("de","")}', "fr": f'Où la voir {I.get("fr","")}', "it": f'Dove vederla {I.get("it","")}'}))
vervang(f'T(" — Wilde katachtigen in {n0["nl"]}"," — Wild cats in {n0["en"]}")',
        Tjs({"nl": f' — Wilde katachtigen {I["nl"]}', "en": f' — Wild cats {I["en"]}', "de": f' — Wilde Katzen {I.get("de","")}', "fr": f' — Félins sauvages {I.get("fr","")}', "it": f' — Felini selvatici {I.get("it","")}'}))
js = re.sub(r'T\("Kaart van [^"]*","Map of [^"]*"(?:,"[^"]*")*\)', lambda m: Tjs({"nl": f'Kaart {V["nl"]} met {len(LOCS)} locaties met katachtigen', "en": f'Map {V["en"]} with {len(LOCS)} locations with cats',
        "de": f'Karte {V.get("de","")} mit {len(LOCS)} Orten mit Katzen', "fr": f'Carte {V.get("fr","")} avec {len(LOCS)} lieux avec des félins', "it": f'Mappa {V.get("it","")} con {len(LOCS)} luoghi con felini'}), js)
js = re.sub(r'(document\.getElementById\("rt-preset"\)\.addEventListener\("click",\(\)=>setAll\()\[.*?\](\)\);)', lambda m: m.group(1) + json.dumps(route, ensure_ascii=False) + m.group(2), js)
for k in keys:
    for nm in set(DSN0[k][:len(LG)]):
        for l in js.split("\n"):
            if len(l) < 600 and re.search(r'T\([^)]*\b' + re.escape(nm) + r'\b', l) and "LOCS" not in l and "setAll" not in l:
                print("let op, regionaam in script:", l[:160])

# regiofilter (zoals Italië), op alle tekstblokken met data-rg
REGN = {k: DSN0[k][:len(LG)] for k in keys}
RG = ("const REGIO=" + json.dumps(REGIO, ensure_ascii=False) + ";\nconst REGN=" + json.dumps(REGN, ensure_ascii=False) + ";\nconst REGORDER=" + json.dumps(keys) + ";\n" + r'''
/* ---------- filter per regio (één pagina, geen aparte regiopagina's; bron/samenvoegen.py) ---------- */
var RG_F=window.__RGINIT||"";
const RG_NAME=k=>REGN[k]?pk(REGN[k]):k;
if(!document.getElementById("rg-css")){const s=document.createElement("style");s.id="rg-css";s.textContent=
`.rg-bar{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 6px}
.rg-chip{font:inherit;font-size:14px;line-height:1.3;padding:4px 11px;border-radius:999px;border:1.5px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
.rg-chip[aria-pressed="true"]{background:var(--ink);color:var(--card);border-color:var(--ink)}
.rg-chip .n{opacity:.7;font-variant-numeric:tabular-nums;margin-left:2px}
.rg-lab{font-size:14px;font-weight:600;margin:14px 0 2px}
.rg-count{font-size:13.5px;color:var(--muted);margin:0 0 10px}
.rg-kop{font-size:19px;margin:22px 0 6px}
.map .mk.rg-off{display:none}`;
document.head.appendChild(s);}
function RG_DECOR(){
  const sec=document.getElementById("locaties");if(!sec)return;
  const cnt={};LOCS.forEach(l=>{const k=REGIO[l[0]];if(k)cnt[k]=(cnt[k]||0)+1;});
  const keys=REGORDER.filter(k=>cnt[k]);
  let bar=document.getElementById("rg-bar");
  if(!bar){const anchor=document.getElementById("lt-bar")||sec.querySelector(".mapwrap");if(!anchor)return;
    anchor.insertAdjacentHTML("beforebegin",'<p class="rg-lab" id="rg-lab"></p><div class="rg-bar" id="rg-bar" role="group"></div><p class="rg-count" id="rg-count" aria-live="polite" hidden></p>');
    bar=document.getElementById("rg-bar");
    bar.addEventListener("click",e=>{const b=e.target.closest(".rg-chip");if(!b)return;RG_F=b.dataset.r;RG_DECOR();render();});}
  document.getElementById("rg-lab").textContent=@@REGIO@@;
  bar.setAttribute("aria-label",@@FILTER@@);
  bar.innerHTML=[["",LOCS.length,@@ALLE@@]].concat(keys.map(k=>[k,cnt[k],RG_NAME(k)]))
    .map(([k,n,l])=>`<button type="button" class="rg-chip" data-r="${esc(k)}" aria-pressed="${k===RG_F}">${esc(l)} <span class="n">${n}</span></button>`).join("");
  RG_APPLY();
}
function RG_APPLY(){
  const off=nm=>!!RG_F&&REGIO[nm]!==RG_F;
  document.querySelectorAll("#nlmap .mk").forEach(m=>{const l=LOCS[+m.dataset.i];if(l)m.classList.toggle("rg-off",off(l[0]));});
  const sel=document.getElementById("locsel");
  if(sel)[...sel.options].forEach(o=>{if(o.value==="")return;const l=LOCS[+o.value];if(!l)return;const h=off(l[0]);o.hidden=h;o.disabled=h;});
  document.querySelectorAll("[data-rg]").forEach(g=>{g.hidden=!!RG_F&&g.dataset.rg!==RG_F;});
  const c=document.getElementById("rg-count");
  if(c){const n=LOCS.filter(l=>!off(l[0])).length;c.hidden=!RG_F;c.textContent=RG_F?`${n} / ${LOCS.length} · ${RG_NAME(RG_F)}`:"";}
}
{const o=render;render=function(){const r=o.apply(this,arguments);RG_APPLY();return r;};}
{const o=applyLang;applyLang=function(){const r=o.apply(this,arguments);RG_DECOR();return r;};}
''').replace("@@REGIO@@", Tjs({l: L["regio"][i] for i, l in enumerate(LG)})).replace("@@FILTER@@", Tjs({l: L["filter"][i] for i, l in enumerate(LG)})).replace("@@ALLE@@", Tjs({l: L["regios"][i] for i, l in enumerate(LG)}))
EIND = 'applyLang(LANG,false);\nwindow.addEventListener("hashchange",route);\nroute();'
assert js.count(EIND) == 1
js = js.replace(EIND, RG + EIND)

# ------------------------------------------------------------------ html samenvoegen
def sec(h, sid):
    m = re.search(r'<section id="%s">(.*?)</section>' % sid, h, re.S)
    return m.group(1) if m else ""
def zonder_h2(x):
    return re.sub(r"^\s*<h2>.*?</h2>", "", x, count=1, flags=re.S)
def blok(k, inhoud, n=0):
    inhoud = re.sub(r'\bid="([a-z0-9-]+)"', lambda m: f'id="{m.group(1)}-{k}"', inhoud) if n else inhoud
    return f'<div class="rg-blok" data-rg="{k}"><h3 class="rg-kop">{zin(rn(k))}</h3>{inhoud}</div>\n'
TH = B[k0]["html"]
h2 = lambda sid: re.search(r'<section id="%s">\s*(<h2>.*?</h2>)' % sid, TH, re.S).group(1)

# kop
hd = re.search(r"<header>.*?</header>", TH, re.S).group(0)
start_m2 = re.search(r'<header>.*?<span class="m2">(.*?)</span></h1>', src, re.S).group(1)
hd = re.sub(r'(<span class="m2">).*?(</span></h1>)', lambda m: m.group(1) + start_m2 + m.group(2), hd, count=1, flags=re.S)
LEDE = {"nl": f"Waar {I['nl']} kun je leeuwen, tijgers, lynxen en andere wilde katten zien? Per soort en per park zie je hier welke katten er wonen, welke jongen er onlangs geboren zijn en wat er binnenkort verandert. Kies een regio om alleen die te zien.",
        "en": f"Where {I['en']} can you see lions, tigers, lynxes and other wild cats? For each species and each park you can see which cats live there, which young were born recently and what is about to change. Choose a region to see only that region.",
        "de": f"Wo {I.get('de','')} kannst du Löwen, Tiger, Luchse und andere wilde Katzen sehen? Für jede Art und jeden Park siehst du, welche Katzen dort leben, welche Jungtiere kürzlich geboren wurden und was sich bald ändert. Wähle eine Region, um nur diese zu sehen.",
        "fr": f"Où voir des lions, des tigres, des lynx et d’autres félins sauvages {I.get('fr','')} ? Pour chaque espèce et chaque parc, vous voyez quels félins y vivent, quels petits sont nés récemment et ce qui va bientôt changer. Choisissez une région pour ne voir qu’elle.",
        "it": f"Dove vedere leoni, tigri, linci e altri felini selvatici {I.get('it','')}? Per ogni specie e ogni parco vedi quali felini ci vivono, quali cuccioli sono nati di recente e cosa cambierà a breve. Scegli una regione per vedere solo quella."}
hd = re.sub(r'<p class="lede">.*?</p>', '<p class="lede">' + zin(LEDE) + "</p>", hd, count=1, flags=re.S)
nconf = len({r[0] for r in R if any(x in "gybr" for x in r[4].split("+"))})
cnts = re.findall(r"<b>\d+</b>", hd)
assert len(cnts) == 2, cnts
hd = hd.replace(cnts[0], "<b>@@A@@</b>", 1).replace(cnts[1], "<b>@@B@@</b>", 1).replace("@@A@@", str(nconf)).replace("@@B@@", str(len(LOCS)))

toc = re.search(r'<nav aria-label="Inhoud / Contents" class="toc">.*?</nav>', TH, re.S).group(0)
tldr = f'<section id="tldr">\n{h2("tldr")}\n' + "".join(blok(k, zonder_h2(sec(B[k]["html"], "tldr")), i) for i, k in enumerate(keys)) + "</section>\n"

board = re.search(r'<div class="board" id="soorten">.*?</div>\s*(?=<section)', TH, re.S).group(0)
niet = [s for s in order if s not in present]
NIET = {"nl": f"Niet {I['nl']} te zien ({len(niet)} soorten)", "en": f"Not on view {I['en']} ({len(niet)} species)", "de": f"{I.get('de','').capitalize()} nicht zu sehen ({len(niet)} Arten)",
        "fr": f"Non visibles {I.get('fr','')} ({len(niet)} espèces)", "it": f"Non visibili {I.get('it','')} ({len(niet)} specie)"}
board = re.sub(r'(<div class="group-title" data-closed="1">).*?(</div>\s*<div class="chips">).*?(</div>)',
               lambda m: m.group(1) + zin(NIET) + m.group(2) + "".join(f'<span class="chip off">{H.escape(s)}</span>' for s in niet) + m.group(3), board, count=1, flags=re.S)

loc_t = sec(TH, "locaties")
mapwrap = re.search(r'<div class="mapwrap">.*?</div>\s*</div>\s*</div>', loc_t, re.S).group(0)
mapwrap = re.sub(r'viewbox="[^"]*"', f'viewbox="0 0 {W} {Hh}"', mapwrap)
LOCI = {"nl": f"Alle dierentuinen, dierenparken, wildparken en opvangcentra {I['nl']} waar wilde katachtigen wonen. Tik op een stip om te zien welke katten er zitten, of kies hieronder een regio.",
        "en": f"All zoos, animal parks, wildlife parks and rescue centres {I['en']} where wild cats live. Tap a dot to see which cats live there, or choose a region below.",
        "de": f"Alle Zoos, Tierparks, Wildparks und Auffangstationen {I.get('de','')}, in denen wilde Katzen leben. Tippe auf einen Punkt, um zu sehen, welche Katzen dort leben, oder wähle unten eine Region.",
        "fr": f"Tous les zoos, parcs animaliers et refuges {I.get('fr','')} où vivent des félins sauvages. Touchez un point pour voir quels félins y vivent, ou choisissez une région ci-dessous.",
        "it": f"Tutti gli zoo, i parchi faunistici e i centri di recupero {I.get('it','')} dove vivono felini selvatici. Tocca un punto per vedere quali felini ci sono, oppure scegli una regione qui sotto."}
def na_map(h):
    t = sec(h, "locaties"); m = re.search(r'<div class="mapwrap">.*?</div>\s*</div>\s*</div>', t, re.S)
    return t[m.end():]
locaties = (f'<section id="locaties">\n{h2("locaties")}\n<p class="prose" style="margin-top:0">{zin(LOCI)}</p>\n{mapwrap}\n'
            + "".join(blok(k, na_map(B[k]["html"]), i) for i, k in enumerate(keys)) + "</section>\n")

rt_t = sec(TH, "route"); cut = rt_t.index('<h3 id="advies">')
planner = re.sub(r'(<button id="rt-preset" type="button">)(.*?)(</button>)', lambda m: m.group(1) + re.sub(r"\d+", str(len(route)), m.group(2)) + m.group(3), rt_t[:cut], flags=re.S)
def advies(h):
    t = sec(h, "route"); return t[t.index('<h3 id="advies">'):].split("</h3>", 1)[1]
route_s = (f'<section id="route">{planner}{rt_t[cut:].split("</h3>",1)[0]}</h3>\n' + "".join(blok(k, advies(B[k]["html"]), i) for i, k in enumerate(keys)) + "</section>\n")
register = f'<section id="register">{sec(TH, "register")}</section>\n'

ac_t = sec(TH, "actueel"); cut = ac_t.index('<h3 id="gepland">')
JONG = {"nl": f"Welke jonge katten zijn er nu {I['nl']} te zien? Felinae (kleine katten) staan hier tot 1 jaar, Pantherinae (grote katten) tot 2 jaar, omdat grote katten langzamer opgroeien. Jonge dieren zitten de eerste weken vaak binnen bij hun moeder, dus kijk vóór je bezoek bij het park of ze al te zien zijn.",
        "en": f"Which young cats can you see {I['en']} right now? Felinae (small cats) are listed up to 1 year, Pantherinae (big cats) up to 2 years, because big cats grow up more slowly. Young animals often stay indoors with their mother for the first weeks, so check with the park before your visit.",
        "de": f"Welche Jungtiere kann man {I.get('de','')} gerade sehen? Felinae (Kleinkatzen) stehen hier bis 1 Jahr, Pantherinae (Großkatzen) bis 2 Jahre, weil Großkatzen langsamer aufwachsen. Jungtiere bleiben die ersten Wochen oft drinnen bei der Mutter; frag vor dem Besuch beim Park nach.",
        "fr": f"Quels jeunes félins peut-on voir {I.get('fr','')} en ce moment ? Les Felinae (petits félins) figurent ici jusqu’à 1 an, les Pantherinae (grands félins) jusqu’à 2 ans, car ils grandissent plus lentement. Les petits restent souvent à l’intérieur avec leur mère les premières semaines : renseignez-vous auprès du parc avant votre visite.",
        "it": f"Quali cuccioli si possono vedere {I.get('it','')} adesso? I Felinae (piccoli felini) sono elencati fino a 1 anno, i Pantherinae (grandi felini) fino a 2 anni, perché crescono più lentamente. Nelle prime settimane i cuccioli restano spesso al chiuso con la madre: informati presso il parco prima della visita."}
ac_top = re.sub(r'(<h3 id="jong"[^>]*>.*?</h3>\s*)<p class="prose" style="margin-top:0">.*?</p>', lambda m: m.group(1) + f'<p class="prose" style="margin-top:0">{zin(JONG)}</p>', ac_t[:cut], count=1, flags=re.S)
def gepland(h):
    t = sec(h, "actueel"); return t[t.index('<h3 id="gepland">'):].split("</h3>", 1)[1]
actueel = f'<section id="actueel">{ac_top}{ac_t[cut:].split("</h3>",1)[0]}</h3>\n' + "".join(blok(k, gepland(B[k]["html"]), i) for i, k in enumerate(keys)) + "</section>\n"
def per_regio(sid):
    return f'<section id="{sid}">\n{h2(sid)}\n' + "".join(blok(k, zonder_h2(sec(B[k]["html"], sid)), i) for i, k in enumerate(keys)) + "</section>\n"
kleur = per_regio("kleur"); uitleg = per_regio("uitleg")
rapporteer = f'<section id="rapporteer">{sec(TH, "rapporteer")}</section>\n'
staart = TH[TH.rindex("</section>") + len("</section>"):]
staart = re.sub(r"<footer>.*?</footer>", "<footer>" + zin({l: START_T[i] for i, l in enumerate(LG)}) + "</footer>", staart, count=1, flags=re.S)
body = ('<div class="wrap" id="main">\n' + hd + "\n" + toc + "\n" + tldr + board + "\n" + locaties + route_s + register + actueel + kleur + uitleg + rapporteer + staart)
body = body.replace('src="data:,"', 'src="@@IMG0@@"')
for k in keys:   # links binnen de gids naar een regio-adres
    body = body.replace(f'href="#{k}/', 'href="#')

# ------------------------------------------------------------------ pagina in elkaar zetten
kop = src[:src.index('<div class="wrap" id="start" hidden>')]
kofi = re.search(r'<div class="kofi-wrap">.*?</aside></div>', src, re.S).group(0)
pre = ('<script>(function(){var h=decodeURIComponent(location.hash||""),K=' + json.dumps(keys)
       + ',m=h.match(/^#([a-z-]+)(?:\\/(.*))?$/);if(m&&(K.indexOf(m[1])>=0||m[1]===' + json.dumps(c) + ')){if(m[1]!==' + json.dumps(c)
       + ')window.__RGINIT=m[1];try{history.replaceState(null,"",location.pathname+location.search+(m[2]?"#"+m[2]:""));}catch(e){}}'
       + 'window.__HASH=function(){return decodeURIComponent(location.hash||"");};})();</script>\n')
doc = kop + body + "\n" + kofi + "\n" + pre + "<script>\n(function(){\n" + js + "\n})();\n</script>\n</body></html>\n"
open(BRON + f"gidsen/{c}.html", "w", encoding="utf-8").write(doc)
print(c, "regio's:", len(keys), "locaties:", len(LOCS), "soorten bevestigd:", nconf, "route:", route, "kaart:", W, Hh, "bytes:", len(doc))
