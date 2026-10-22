import os
# Bouwt bron/gidsen/dk.html uit dk_basis.html (Deense vaste teksten) + dk_final.json (gegevens) + teksten.py (landspecifieke blokken).
import json, re, sys, unicodedata, html
D = os.path.dirname(os.path.abspath(__file__)) + "/"
OUT = sys.argv[1] if len(sys.argv) > 1 else D + "../../gidsen/dk.html"
s = open(D + "dk_basis.html", encoding="utf8").read()
F = json.load(open(D + "dk_final.json", encoding="utf8"))
DA = json.load(open(D + "da.json", encoding="utf8")) if __import__("os").path.exists(D + "da.json") else {}
K = json.load(open(D + "kaart/kaart.json"))
sys.path.insert(0, D)
import teksten as TX

MISS = {}
def da(nl, en):
    """Deense tekst bij een nl/en-paar: uit da.json (sleutel = Engelse tekst)."""
    if en in DA: return DA[en]
    if nl in DA: return DA[nl]
    if not en.strip(): return en
    MISS[en] = nl
    return en
BR = json.load(open(D + "bron_vert.json", encoding="utf8")) if __import__("os").path.exists(D + "bron_vert.json") else {}
BMISS = []
def trib(nl):
    if nl in BR: return [nl] + BR[nl]
    BMISS.append(nl); return [nl, nl, nl]
def tri(o):
    if isinstance(o, str): return [o, o, o]
    nl, en = o.get("nl", ""), o.get("en", "")
    return [nl, en, o.get("da") or da(nl, en)]
def esc(x): return html.escape(x, quote=False)
def js(o): return json.dumps(o, ensure_ascii=False)
def slug(x):
    x = x.replace("æ", "ae").replace("ø", "oe").replace("Æ", "Ae").replace("Ø", "Oe")
    x = "".join(c for c in unicodedata.normalize("NFD", x) if not unicodedata.combining(c)).lower()
    x = re.sub(r"\(.*?\)", "", x)
    return re.sub(r"[^a-z0-9]+", "-", x).strip("-")
def const(name, val):
    global s
    pat = re.compile(r"(const " + re.escape(name) + r"=)(.*?)(;\n)", re.S)
    assert pat.search(s), name
    s = pat.sub(lambda m: m.group(1) + val + m.group(3), s, count=1)
def sub1(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)
def block(start, end, new, keep_start=True):
    """vervang tekst tussen start (incl./excl.) en de eerstvolgende end (excl.)"""
    global s
    i = s.index(start); j = s.index(end, i + len(start))
    s = s[:i] + (start if keep_start else "") + new + s[j:]
def spans(t3, tag="span"):
    return "".join(f'<{tag} class="l-{l}">{t}</{tag}>' for l, t in zip(["nl", "en", "da"], t3))

SPECIES = json.loads(re.search(r"const SPECIES=(.*?);\n", s, re.S).group(1))
ORDER = [x[0] for x in SPECIES]
PANTH = {"Leeuw", "Tijger", "Luipaard", "Jaguar", "Sneeuwluipaard", "Nevelpanter", "Soenda-nevelpanter"}
SPEN = json.loads(re.search(r"const SPEN=(.*?);\n", s, re.S).group(1))
SPDA = json.loads(re.search(r"const SPDA=(.*?);\n", s, re.S).group(1))
def nm3(sp): return [sp, SPEN[sp][0], SPDA[sp][0]]

LOCS_ = F["locaties"]
CONF = set("gybr")
TYPE3 = {t["nl"]: [t["nl"], t["en"], t["da"]] for t in json.load(open(D + "../../locatietypes.json", encoding="utf8"))["types"]}
CHECK = F.get("checked", "22-10-2026")

# ---------------- R en vertaaltabellen
R = []; R1EN = {}; R1DA = {}; R5EN = {}; R5DA = {}; R6EN = {}; R6DA = {}; R7EN = {}; R7DA = {}; TWX = {}
for l in LOCS_:
    for k in l["katten"]:
        sub = k["ondersoort"]; t5 = tri(k["toelichting"]); t6 = tri(k["aantal"]); t7 = trib(k["bron"])
        su = tri(sub)
        R.append([k["soort"], su[0], l["naam"], l["plaats"]["nl"] if isinstance(l["plaats"], dict) else l["plaats"], k["status"], t5[0], t6[0], t7[0], CHECK])
        R1EN[su[0]] = su[1]; R1DA[su[0]] = su[2]
        R5EN[t5[0]] = t5[1]; R5DA[t5[0]] = t5[2]
        R6EN[t6[0]] = t6[1]; R6DA[t6[0]] = t6[2]
        R7EN[t7[0]] = t7[1]; R7DA[t7[0]] = t7[2]
        if k["status"] == "w" or k.get("twijfel"):
            TWX[k["soort"] + "|" + l["naam"]] = tri(k["twijfel"])
present = [sp for sp in ORDER if any(r[0] == sp for r in R)]
conf_sp = [sp for sp in ORDER if any(r[0] == sp and r[4] in CONF for r in R)]
unsure_sp = [sp for sp in present if sp not in conf_sp]
nconf = {sp: len({r[2] for r in R if r[0] == sp and r[4] in CONF}) for sp in present}
locs_conf = [l for l in LOCS_ if any(k["status"] in CONF for k in l["katten"])]
const("R", js(R))
for n, v in [("R1EN", R1EN), ("R1DA", R1DA), ("R5EN", R5EN), ("R5DA", R5DA), ("R6EN", R6EN), ("R6DA", R6DA), ("R7EN", R7EN), ("R7DA", R7DA)]:
    const(n, js(v))
const("BIG", js([x for x in present if x in PANTH]))
const("SMALL", js([x for x in present if x not in PANTH]))
const("UNIQUE", "new Set(" + js([sp for sp in conf_sp if nconf[sp] == 1]) + ")")
const("TWX", js(TWX))

# ---------------- locaties
def plaats(l): return l["plaats"]["nl"] if isinstance(l["plaats"], dict) else l["plaats"]
const("LOCS", js([[l["naam"], plaats(l), l["lon"], l["lat"], [l["naam"]]] for l in LOCS_]))
LOCINFO = {}; EARLIER_LOC = {}
for l in LOCS_:
    LOCINFO[l["naam"]] = {"type": TYPE3[l["type"]], "labels": l.get("labels", []), "hours": tri(l["uren"]), "url": l["url"], "checked": CHECK, "about": tri(l["about"])}
    e = l.get("earlier") or {}
    if e.get("nl"): EARLIER_LOC[l["naam"]] = tri(e)
const("LOCINFO", js(LOCINFO))
const("EARLIER_LOC", js(EARLIER_LOC))
const("REGIO", js({l["naam"]: l["regio"] for l in LOCS_}))
const("REGN", js(TX.REGN))
const("REGORDER", js(list(TX.REGN)))
YOUNG = []
for l in LOCS_:
    for g in l.get("geboortes", []):
        y = {"sp": g["soort"], "loc": l["naam"], "born": g["geboren"], "n": tri(g["n"]), "x": tri(g["x"]), "src": g["bron"]}
        if g.get("approx"): y["approx"] = True
        if g.get("sub"): y["sub"] = tri(g["sub"])
        YOUNG.append(y)
const("YOUNG", js(YOUNG))
const("EXPECT", js(F.get("expect", [])))
const("NOROUTE", "new Set(" + js(F.get("noroute", [])) + ")")
const("ROUTENOTE", js({k: v["nl"] for k, v in F.get("routenote", {}).items()}))
const("ROUTENOTE_EN", js({k: v["en"] for k, v in F.get("routenote", {}).items()}))
const("ROUTENOTE_DA", js({k: tri(v)[2] for k, v in F.get("routenote", {}).items()}))
# bronnen van de jongen
for y in YOUNG:
    b = trib(y["src"]); R7EN[y["src"]] = b[1]; R7DA[y["src"]] = b[2]
const("R7EN", js(R7EN)); const("R7DA", js(R7DA))

# ---------------- kaart
LON0, LAT0, KX = 7.9, 57.85, 0.556
def PX(lo, la): return ((lo - LON0) * KX * 110 + 10, (LAT0 - la) * 110 + 10)
W = round(PX(15.3, 0)[0] + 10); H = round(PX(0, 54.45)[1] + 10)
const("PX", f'(lo,la)=>[((lo-({LON0}))*{KX}*110.0+10).toFixed(1),(({LAT0}-la)*110.0+10).toFixed(1)]')
const("MAIN", js(K["MAIN"])); const("BUUR", js(K["BUUR"])); const("ISLANDS", js(K["ISLANDS"])); const("WATER", "[]"); const("LINES", js(K["LINES"]))
s = re.sub(r'<svg id="nlmap" viewBox="[^"]*" role="group" aria-label="[^"]*">',
           f'<svg id="nlmap" viewBox="0 0 {W} {H}" role="group" aria-label="Kaart van Denemarken met {len(LOCS_)} locaties met katachtigen">', s, count=1)
sub1('T("Kaart van Portugal met 7 locaties met katachtigen","Map of Portugal with 7 l', f'T("Kaart van Denemarken met {len(LOCS_)} locaties met katachtigen","Map of Denmark with {len(LOCS_)} l')
s = re.sub(r'(Map of Denmark with )\d+( locations with cats",")[^"]*(")', lambda m: m.group(1) + str(len(LOCS_)) + m.group(2) + f"Kort over Danmark med {len(LOCS_)} steder med kattedyr" + m.group(3), s, count=1)

# ---------------- vaste teksten met het land
for a, b in [("in Portugese dierenlocaties", "in Deense dierenlocaties"), ("in Portuguese zoos and animal parks", "in Danish zoos and animal parks"),
             ("Waar te zien in Portugal", "Waar te zien in Denemarken"), ("Where to see it in Portugal", "Where to see it in Denmark"),
             ("Wilde katachtigen in Portugal", "Wilde katachtigen in Denemarken"), ("Wild cats in Portugal", "Wild cats in Denmark"),
             ("Deze soort is op dit moment niet te zien in Portugal.", "Deze soort is op dit moment niet te zien in Denemarken."),
             ("This species is currently not on view in Portugal.", "This species is currently not on view in Denmark."),
             ("i Portugal", "i Danmark"), ("Welke jonge katten zijn er nu in Portugal te zien?", "Welke jonge katten zijn er nu in Denemarken te zien?"),
             ("Which young cats can be seen in Portugal right now?", "Which young cats can be seen in Denmark right now?")]:
    s = s.replace(a, b)
s = re.sub(r"<title>.*?</title>", "<title>Wilde katachtigen in Deense dierenlocaties — stand 22 oktober 2026</title>", s, count=1)
s = re.sub(r'(const TITLE_EN=)"[^"]*"', r'\1"Wild cats in Danish zoos and animal parks — updated 22 October 2026"', s, count=1)
for a, b in TX.VAST:   # losse vervangingen (datum, kop, lede …)
    s = re.sub(a, lambda m, b=b: b, s, count=1, flags=re.S)

# kop: tellers
s = re.sub(r'(<div class="counts">\s*<div><b>)\d+(</b>)', lambda m: m.group(1) + str(len(conf_sp)) + m.group(2), s, count=1)
s = re.sub(r'(locaties met katachtigen</span>.*?)', r'\1', s, count=1)
s = re.sub(r'(</b><span><span class="l-nl">soorten bevestigd</span>.*?</div>\s*<div><b>)\d+(</b>)', lambda m: m.group(1) + str(len(locs_conf)) + m.group(2), s, count=1, flags=re.S)

# In het kort
i = s.index('<section id="tldr">'); i = s.index("</h2>\n", i) + 6; j = s.index('  <h3><span class="l-nl">Totaaloverzicht', i)
s = s[:i] + TX.tldr() + s[j:]
def lijst(sps, l):  # soortnamen in zin, eerste met hoofdletter
    xs = [nm3(sp)[l] for sp in sps]
    xs = [x if i == 0 else (x[0].lower() + x[1:]) for i, x in enumerate(xs)]
    return ", ".join(xs)
def lijstH(sps, l): return ", ".join(nm3(sp)[l] for sp in sps)
rows = (f'      <tr><td>{spans(["Bevestigd", "Confirmed", "Bekræftet"])}</td><td>{len(conf_sp)}</td><td>{spans([lijstH(conf_sp, i) for i in range(3)])}</td></tr>\n'
        + (f'      <tr><td>{spans(["Onzeker", "Uncertain", "Usikker"])}</td><td><span class="tw-n"></span> {spans(["vermeldingen", "entries", "registreringer"])}</td><td>{spans([lijstH(unsure_sp, i) for i in range(3)]) if unsure_sp else "—"}</td></tr>\n'))
i = s.index("<tbody>", j); j2 = s.index("</tbody>", i)
s = s[:i + 7] + "\n" + rows + "    " + s[j2:]

# Niet te zien
niet = [sp for sp in ORDER if sp not in present]
s = re.sub(r'<div class="group-title" data-closed="1">.*?</div>\s*<div class="chips">.*?</div>',
           lambda m: f'<div class="group-title" data-closed="1">{spans([f"Niet in Denemarken te zien ({len(niet)} soorten)", f"Not on view in Denmark ({len(niet)} species)", f"Kan ikke ses i Danmark ({len(niet)} arter)"])}</div>\n  <div class="chips">' + "".join(f'<span class="chip off">{x}</span>' for x in niet) + "</div>", s, count=1, flags=re.S)

# intro bij de kaart
s = re.sub(r'(<section id="locaties">.*?</h2>\n  <p class="prose" style="margin-top:0">).*?(</p>)', lambda m: m.group(1) + spans(TX.LOC_INTRO) + m.group(2), s, count=1, flags=re.S)

# locatielijsten per regio + geen katten + officiële lijst
def li(l):
    c = [k["soort"] for k in sorted(l["katten"], key=lambda k: ORDER.index(k["soort"])) if k["status"] in CONF]
    u = [k["soort"] for k in sorted(l["katten"], key=lambda k: ORDER.index(k["soort"])) if k["status"] not in CONF]
    W3 = ["Onzeker", "Uncertain", "Usikker"]
    t = []
    for i in range(3):
        a = (lijst(c, i) + ".") if c else ""
        b = (f"{W3[i]}: " + ", ".join(nm3(x)[i][0].lower() + nm3(x)[i][1:] for x in u) + ".") if u else ""
        t.append((a + " " + b).strip())
    return f'    <li><b><a href="#locatie/{slug(l["naam"])}">{esc(l["naam"])}</a></b><span class="plc">{esc(plaats(l))}</span>{spans([esc(x) for x in t])}</li>\n'
def nconfl(l): return len({k["soort"] for k in l["katten"] if k["status"] in CONF})
out = f'    <details open><summary>{spans([f"Met katachtigen ({len(LOCS_)} locaties)", f"With cats ({len(LOCS_)} locations)", f"Med kattedyr ({len(LOCS_)} steder)"])}</summary><div>\n'
for rk in TX.REGN:
    ls = sorted([l for l in LOCS_ if l["regio"] == rk], key=lambda l: (-nconfl(l), l["naam"]))
    if not ls: continue
    out += f'    <div data-rg="{rk}"><div class="group-title">{spans(TX.REGN[rk])}</div>\n    <ul class="loclist cards">\n' + "".join(li(l) for l in ls) + "    </ul></div>\n"
out += "  </div></details>\n"
out += f'  <details><summary>{spans(["Geen katachtigen gevonden", "No cats found", "Ingen kattedyr fundet"])}</summary><div>' + "".join(f'<div class="l-{lg}">\n<ul class="loclist">\n' + TX.geen(i) + "  </ul>\n</div>" for i, lg in enumerate(["nl", "en", "da"])) + "</div></details>\n"
out += f'  <details><summary>{spans(["Over de officiële lijst van dierentuinen", "About the official list of zoos", "Om den officielle liste over zoologiske anlæg"])}</summary><div class="prose">' + "".join(f'<div class="l-{lg}">\n' + TX.OFFICIEEL[i] + "</div>" for i, lg in enumerate(["nl", "en", "da"])) + "</div></details>\n"
i = s.index("    <details open><summary>", s.index('<section id="locaties">')); j = s.index("</section>", i)
s = s[:i] + out + s[j:]

# route
pre = F["route"]
s = re.sub(r'(<button type="button" id="rt-preset">).*?(</button>)', lambda m: m.group(1) + spans([f"Route met {len(pre)} parken", f"Route with {len(pre)} parks", f"Rute med {len(pre)} parker"]) + m.group(2), s, count=1)
s = re.sub(r'(getElementById\("rt-preset"\)\.addEventListener\("click",\(\)=>setAll\()\[.*?\](\)\);)', lambda m: m.group(1) + js(pre) + m.group(2), s, count=1)
i = s.index('<h3 id="advies">'); i = s.index("</h3>\n", i) + 6; j = s.index("</section>", i)
s = s[:i] + "".join(f'<div class="l-{lg}">\n' + TX.ADVIES[k] + "</div>" for k, lg in enumerate(["nl", "en", "da"])) + "\n" + s[j:]

# actueel: gepland/tijdelijk
i = s.index('<h3 id="gepland"'); i = s.index("</h3>\n", i) + 6; j = s.index("</section>", i)
s = s[:i] + "".join(f'<div class="l-{lg}">\n' + TX.GEPLAND[k] + "</div>" for k, lg in enumerate(["nl", "en", "da"])) + "\n" + s[j:]

# kleur
i = s.index('<h3 id="kleurvarianten"'); i = s.index("</h3>\n", i) + 6; j = s.index("</section>", i)
s = s[:i] + TX.KLEUR + s[j:]

# uitleg: werkwijze, namen, verdwenen, bronnen (per taal)
for lg, suf in [("nl", ""), ("en", "-en"), ("da", "-da")]:
    for blk in ["werkwijze", "namen", "verdwenen", "controle"]:
        idd = blk + suf
        i = s.index(f'<div id="{idd}">'); i = s.index("</h3>\n", i) + 6
        j = s.index("\n</div>", i)
        s = s[:i] + TX.UITLEG[blk][lg] + s[j:]

s = s.replace("(Portugal: één pagina met de NUTS-regio’s, geen aparte regiopagina's)", "(Denemarken: één pagina met de vijf regio’s)")
open(OUT, "w", encoding="utf8").write(s)
json.dump(sorted(set(BMISS)), open(D + "bron_ontbreekt.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
json.dump(MISS, open(D + "da_ontbreekt.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print("geschreven", OUT, len(s), "| soorten", len(conf_sp), conf_sp, "| onzeker", unsure_sp, "| locaties", len(LOCS_), "bevestigd", len(locs_conf), "| R", len(R), "| ontbreekt da:", len(MISS))
