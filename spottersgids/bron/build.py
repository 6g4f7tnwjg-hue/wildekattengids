#!/usr/bin/env python3
"""Bouwt de Spottersgids (index.html) uit de KATalogue-gegevens en het onderzoek in data/.

Gebruik:  python3 bron/build.py          (vanuit de map spottersgids)
          python3 bron/build.py --test   testpagina in de Safari-stijl: bouwt alleen safari/ uit bron/template-safari.html
                                         (noindex; soortpagina's openen binnen de testpagina; de live gids blijft ongewijzigd)
"""
import json, os, re, sys, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda *p: os.path.join(ROOT, *p)
load = lambda p: json.load(open(J(p), encoding='utf-8'))
TEST = '--test' in sys.argv

# Soorten met een afgeronde soortpagina (per werelddeel uitgebreid)
PAGES = [24, 27, 37, 4, 38, 42, 1, 30, 11, 12, 13, 40, 41, 2, 5, 6, 7, 8, 9, 10, 31, 32, 33, 34, 35, 36, 39, 3, 28, 14, 15, 29, 18, 16, 17, 19, 20, 21, 22, 23, 25, 26]

# Dezelfde plek onder verschillende id's in de onderzoeksbestanden
ALIAS = json.load(open(J('data', 'alias.json'), encoding='utf-8')) if os.path.exists(J('data', 'alias.json')) else {}
CONT_MAP = {'eur': 'eur', 'afr': 'afr', 'asia': 'asia', 'namerica': 'nam', 'samerica': 'sam'}

cats = load('bron/katalogue.json')
# Eigen fotokeuze per soort (dierentuinfoto's eruit, extra foto's uit het wild): data/fotos.json
FOTOS = load('data/fotos.json') if os.path.exists(J('data', 'fotos.json')) else {}
for c in cats:
    if str(c['no']) in FOTOS:
        c['photos'] = [dict(ph) for ph in FOTOS[str(c['no'])]]
for c in cats:
    c['cont'] = [CONT_MAP[x] for x in c['cont']]
    if c['no'] not in PAGES:
        c['photos'] = c['photos'][:1]
# Werelddelen die de gids níet overneemt uit de KATalogue (Costa Rica/Panama rekent de gids tot Midden-/Zuid-Amerika)
REMOVE_CONT = {18: ['nam']}   # wolkentijgerkat
for c in cats:
    c['cont'] = [x for x in c['cont'] if x not in REMOVE_CONT.get(c['no'], [])]
extra_cont = load('data/extra_cont.json') if os.path.exists(J('data', 'extra_cont.json')) else {}
for c in cats:
    for x in extra_cont.get(str(c['no']), []):
        if x not in c['cont']:
            c['cont'].append(x)

# Foto's als losse bestanden (GitHub Pages): de grote foto is img/NN-i.jpg zelf; voor de ronde
# fotootjes en lijstjes een klein exemplaar foto/NN-i-k.webp (200 px), alleen opnieuw als de jpg nieuwer is.
from PIL import Image
os.makedirs(J('foto'), exist_ok=True)
for c in cats:
    for ph in c['photos']:
        base = os.path.splitext(os.path.basename(ph['src']))[0]
        src, dst = J(ph['src']), J('foto', base + '-k.webp')
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
            im = Image.open(src).convert('RGB'); im.thumbnail((200, 200))
            im.save(dst, 'WEBP', quality=75, method=6)
        ph['sm'] = f'foto/{base}-k.webp'

sources, src_idx = [], {}
def add_source(s):
    url = s['url'].strip()
    if url not in src_idx:
        src_idx[url] = len(sources)
        sources.append({'title': s['title'], 'url': url})
    return src_idx[url]

def bi(d, k):
    return {'nl': d.get(k + '_nl', ''), 'en': d.get(k + '_en', '')}

spots = {}
def spot_for(s):
    sid = ALIAS.get(s['id'], s['id'])
    if sid not in spots:
        spots[sid] = {'id': sid, 'name': bi(s, 'name'), 'area': bi(s, 'area'), 'country': bi(s, 'country'),
                      'cont': s['cont'], 'lat': round(float(s['lat']), 1), 'lon': round(float(s['lon']), 1), 'recs': []}
    return spots[sid]

def rec_from(s, no, gmap, top=False):
    return {'no': no, 'score': int(s.get('scores', {}).get(str(no), s['score'])), 'why': bi(s, 'why'), 'season': bi(s, 'season'), 'time': bi(s, 'time'),
            'trip': bi(s, 'trip'), 'src': [gmap[i] for i in s.get('sources', []) if i in gmap], 'top': top}

pages = {}
for no in PAGES:
    p = J('data', f'{no}.json')
    if not os.path.exists(p):
        print('ontbreekt:', p, file=sys.stderr); continue
    d = json.load(open(p, encoding='utf-8'))
    gmap = {s['id']: add_source(s) for s in d['sources']}
    order = []
    for s in d['spots']:
        sp = spot_for(s)
        if any(r['no'] == no for r in sp['recs']):
            continue
        # op een afgeronde soortpagina is elke plek met score 5 een topspot
        sp['recs'].append(rec_from(s, no, gmap, top=int(s['score']) == 5))
        order.append(sp['id'])
    order.sort(key=lambda i: -next(r['score'] for r in spots[i]['recs'] if r['no'] == no))
    used = sorted({g for i in order for r in spots[i]['recs'] if r['no'] == no for g in r['src']})
    rest = [gmap[s['id']] for s in d['sources'] if gmap[s['id']] not in used]
    pages[no] = {'intro': bi(d, 'intro'), 'tips': bi(d, 'tips'), 'threats': bi(d, 'threats'),
                 'status': bi(d, 'status_note'), 'statusSrc': [], 'spots': order, 'sources': used + rest}

# Topspots
ts = load('data/topspots.json')
tmap = {s['id']: add_source(s) for s in ts['sources']}
for t in ts['topspots']:
    for no in t['species']:
        sid = ALIAS.get(t['id'], t['id'])
        if no in pages:
            sp = spots.get(sid)
            rec = sp and next((r for r in sp['recs'] if r['no'] == no), None)
            if rec and rec['score'] >= 4:
                rec['top'] = True      # ook een sterke 4 uit de topspotlijst
            elif not rec:
                print(f'LET OP: topspot {sid} voor soort {no} staat niet op de soortpagina', file=sys.stderr)
            continue
        sp = spot_for(t)
        if not any(r['no'] == no for r in sp['recs']):
            sp['recs'].append(rec_from(t, no, tmap, top=True))

# Plekfoto's voor de topspots: data/spotfoto.json (id → src, cr, url); bron in img/spot-<id>.jpg,
# klein exemplaar foto/spot-<id>.webp (800 px breed) voor de topspotkaartjes
spotfoto = load('data/spotfoto.json') if os.path.exists(J('data', 'spotfoto.json')) else {}
for sid, ph in spotfoto.items():
    if sid not in spots:
        print(f'LET OP: plekfoto voor onbekende plek {sid}', file=sys.stderr); continue
    src, dst = J(ph['src']), J('foto', f'spot-{sid}.webp')
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        im = Image.open(src).convert('RGB'); im.thumbnail((800, 800))
        im.save(dst, 'WEBP', quality=72, method=6)
    spots[sid]['photo'] = {'src': f'foto/spot-{sid}.webp', 'cr': ph['cr'], 'url': ph['url']}
    if ph.get('note_nl'):   # algemene foto, niet van de plek zelf
        spots[sid]['photo']['note'] = bi(ph, 'note')

text = load('data/text.json')
for k, pg in text.items():
    pg['sources'] = [add_source(s) for s in pg.get('sources', [])]
europe = load('data/europe.json')

# Adressen van de losse soortpagina's: NL op spottersgids/<naam>/, EN op spottersgids/en/<name>/
import unicodedata, hashlib, html as H
def slug(t):
    t = unicodedata.normalize('NFKD', t.replace("'", '').replace('’', '')).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')
BYNO = {c['no']: c for c in cats}
slugs = {'nl': {no: slug(BYNO[no]['nl']) for no in PAGES}, 'en': {no: slug(BYNO[no]['en']) for no in PAGES}}

data = {'cats': cats, 'spots': list(spots.values()), 'pages': pages, 'sources': sources,
        'text': text, 'europe': europe, 'land': open(J('bron', 'land.txt')).read().strip(), 'slugs': slugs,
        **load('bron/borders.json')}   # landsgrenzen + landnamen voor de soortkaart (Natural Earth 110m via world-atlas)
blob = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
datajs = 'window.SG_DATA=' + blob + ';\n'
if not TEST:
    open(J('data.js'), 'w', encoding='utf-8').write(datajs)

# ---------- Safari-stijl: plaatjes als CSS-variabelen en de voet met de luipaard op de tak (uit bron/jungle.py) ----------
sys.path.insert(0, J('..', 'bron'))
import jungle
def acacia():
    """Acacia met een zachte zon erachter, voor de kop van elk scherm."""
    return jungle.uri("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 210 168'>"
        "<circle cx='132' cy='74' r='52' fill='#F2C14E' fill-opacity='.17'/>"
        "<g fill='#6A4427'>"
        "<path d='M104 170C106 148 106 132 100 118C96 108 88 100 76 93L80 88C92 94 100 101 106 111C108 99 114 89 126 80L130 85C121 93 115 103 113 117C111 133 113 151 116 170Z'/>"
        "<path d='M120 92C128 86 140 84 150 86L149 90C140 89 130 91 123 96Z'/>"
        "<path d='M24 86C18 76 34 66 52 69C58 58 78 53 96 58C108 47 134 45 150 54C166 49 190 56 196 68C208 72 208 84 196 88C182 94 160 92 146 90C130 97 104 97 88 92C70 97 42 97 24 86Z'/>"
        "</g>"
        "<g fill='#7B522F'><path d='M58 70C66 61 82 58 96 62C108 52 130 51 144 58C130 62 116 62 104 66C90 64 72 66 58 70Z'/></g>"
        "</svg>")
def grass():
    """Hoog gras rechtsonder in de bovenbalk."""
    import random
    r, out = random.Random(3), ''
    for i in range(26):
        x = 8 + i * 5.4 + r.uniform(-2, 2); h = r.uniform(14, 34); lean = r.uniform(-12, 8)
        out += f"<path d='M{x:.1f} 58Q{x + lean * .4:.1f} {58 - h * .6:.1f} {x + lean:.1f} {58 - h:.1f}' stroke-width='{r.uniform(2, 3.6):.1f}'/>"
    return jungle.uri(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 150 56' preserveAspectRatio='xMaxYMax meet'><g fill='none' stroke='#523420' stroke-linecap='round'>{out}</g></svg>")
def tracks(col, op):
    """Spoor van kattenpootjes (vier tenen, geen nagels) als achtergrondpatroon."""
    def pootje(x, y, rot, s=1):
        return (f"<g transform='translate({x} {y}) rotate({rot}) scale({s})'><path d='M0 7C-5 7-7 3-5.5 0S-2 -2 0 -2S4 -3 5.5 0S5 7 0 7Z'/>"
                "<ellipse cx='-5.6' cy='-6' rx='1.9' ry='2.5'/><ellipse cx='-2' cy='-9.6' rx='1.9' ry='2.6'/><ellipse cx='2.2' cy='-9.6' rx='1.9' ry='2.6'/><ellipse cx='5.8' cy='-6' rx='1.9' ry='2.5'/></g>")
    p = pootje(22, 118, 38) + pootje(44, 112, 30) + pootje(58, 86, 42) + pootje(80, 80, 34) + pootje(94, 54, 40) + pootje(116, 48, 32) + pootje(128, 20, 38, .9)
    return jungle.uri(f"<svg xmlns='http://www.w3.org/2000/svg' width='160' height='140'><g fill='{col}' fill-opacity='{op}'>{p}</g></svg>")
BG = '#F3EAD7'
SAFARI_VARS = (':root{' + f'--i-acacia:{acacia()};--i-grass:{grass()};--i-tracks:{tracks("#7A5230", ".08")};'
               f'--i-tracks-l:{tracks("#FFFFFF", ".06")};--i-wave:{jungle.wave(BG)};--i-paws:{jungle.paws("#C0602A")}' + '}\n')
# Ko-fi-knop op de tak: koffiebruine tekst in plaats van het groen van de Bezoekersgids
SAFARI_FOOT = 'html body .jg-tak .kofi,html body .jg-tak .kofi span{color:#3B2414!important}\nhtml body .foot.jg-tak{margin-bottom:0!important}\n'
try:   # datum van de laatste wijziging in de gegevens (soortonderzoek, KATalogue, teksten)
    UPDATED = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', 'data', 'bron/katalogue.json'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
except Exception:
    UPDATED = ''

# Stijl en script uit de template naar gedeelde bestanden (één keer laden voor alle pagina's)
OUT = J('safari') if TEST else ROOT
os.makedirs(OUT, exist_ok=True)
PRE = 'safari/' if TEST else ''
tpl = open(J('bron', 'template-safari.html' if TEST else 'template.html'), encoding='utf-8').read()
m = re.search(r'<style>\n?(.*?)</style>', tpl, re.S); css = m.group(1)
tpl = tpl[:m.start()] + f'<link rel="stylesheet" href="{PRE}style.css?v=__CSSVER__">' + tpl[m.end():]
m = re.search(r"<script>\n?('use strict';.*?)</script>", tpl, re.S); js = m.group(1)
tpl = tpl[:m.start()] + f'<script src="{PRE}app.js?v=__JSVER__"></script>' + tpl[m.end():]
if '--i-acacia' in css:   # Safari-stijl
    css = SAFARI_VARS + css + '\n' + jungle.LP_CSS + jungle.TAK_CSS + SAFARI_FOOT
    js = js.replace('__UPDATED__', UPDATED) + '\n' + jungle.LP_JS % json.dumps(jungle.svg()) + '\n' + jungle.TAK_JS
open(os.path.join(OUT, 'style.css'), 'w', encoding='utf-8').write(css)
# taalmenu (wereldbol met de huidige taal), hetzelfde script als de Bezoekersgids
js = js + '\n' + open(J('..', 'bron', 'taalmenu.js'), encoding='utf-8').read()
open(os.path.join(OUT, 'app.js'), 'w', encoding='utf-8').write(js)
ver = lambda t: hashlib.md5(t.encode()).hexdigest()[:8]
tpl = tpl.replace('__VER__', ver(datajs)).replace('__CSSVER__', ver(css)).replace('__JSVER__', ver(js))
if TEST:
    tpl = tpl.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<base href="../">\n<meta name="robots" content="noindex">', 1)
    tpl = tpl.replace('<script src="data.js', '<script>window.SG_TEST=1;</script>\n<script src="data.js', 1)
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(tpl)
    print('testpagina gebouwd: safari/index.html (+ safari/app.js, safari/style.css); live gids niet aangeraakt')
    sys.exit(0)
open(J('index.html'), 'w', encoding='utf-8').write(tpl)

SITE = 'https://yeetkitty.github.io/wildekattengids/spottersgids/'
url = lambda lang, no: SITE + ('en/' if lang == 'en' else '') + slugs[lang][no] + '/'
LBL = {'nl': {'title': '{n} in het wild zien · Spottersgids voor wilde katten',
              'desc': '{n} in het wild zien: beste plek {p} ({c}), kans {k} van 5. Met {m} spotplekken, seizoen, tips en bronnen.',
              'places': 'Beste plekken', 'chance': 'kans'},
       'en': {'title': '{n} in the wild: where to see it · Wild Cat Spotter\'s Guide',
              'desc': '{n} in the wild: best place {p} ({c}), chance {k} out of 5. With {m} spotting sites, best season, tips and sources.',
              'places': 'Best places', 'chance': 'chance'}}
SPOTS = {sp['id']: sp for sp in spots.values()}
written = []
for lang in ('nl', 'en'):
    for no in PAGES:
        c, P = BYNO[no], pages[no]
        recs = [(SPOTS[i], next(r for r in SPOTS[i]['recs'] if r['no'] == no)) for i in P['spots']]
        best, br = recs[0]
        lb = LBL[lang]
        title = lb['title'].format(n=c[lang])
        desc = lb['desc'].format(n=c[lang], p=best['name'][lang], c=best['country'][lang], k=br['score'], m=len(recs))
        alt = f'<link rel="canonical" href="{url(lang, no)}">\n<link rel="alternate" hreflang="nl" href="{url("nl", no)}">\n<link rel="alternate" hreflang="en" href="{url("en", no)}">\n<link rel="alternate" hreflang="x-default" href="{url("en", no)}">'
        pre = (f'<div class="wrap sec read"><h1>{H.escape(c[lang])}</h1><p>{H.escape(P["intro"][lang])}</p>'
               f'<h2>{lb["places"]}</h2><ul>' + ''.join(f'<li>{H.escape(s["name"][lang])} ({H.escape(s["country"][lang])}) – {lb["chance"]} {r["score"]}</li>' for s, r in recs) + '</ul></div>')
        base = '../../' if lang == 'en' else '../'
        out = tpl.replace('<html lang="nl">', f'<html lang="{lang}">', 1)
        out = re.sub(r'<title>.*?</title>', f'<title>{H.escape(title)}</title>', out, count=1)
        out = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{H.escape(desc)}">\n{alt}', out, count=1)
        og = {'og:site_name': 'Spottersgids voor wilde katten' if lang == 'nl' else "Wild Cat Spotter's Guide", 'og:title': title, 'og:description': desc, 'og:image': SITE + c['photos'][0]['src'], 'og:url': url(lang, no)}
        for prop, val in og.items():
            out = re.sub(rf'<meta property="{prop}" content="[^"]*">', lambda m, v=val, pr=prop: f'<meta property="{pr}" content="{H.escape(v)}">', out, count=1)
        out = out.replace('<meta charset="utf-8">', f'<meta charset="utf-8">\n<base href="{base}">', 1)
        out = out.replace('<main id="main"></main>', f'<main id="main">{pre}</main>', 1)
        out = out.replace('<script src="data.js', f'<script>window.SG_PAGE={{no:{no},lang:"{lang}"}};</script>\n<script src="data.js', 1)
        d = J(*(['en'] if lang == 'en' else []), slugs[lang][no]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)
        written.append(url(lang, no))

open(J('sitemap.xml'), 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in [SITE] + written) + '</urlset>\n')
print(f'index.html + {len(written)} soortpagina\'s; data.js {len(datajs)//1024} kB, {len(spots)} plekken, {len(sources)} bronnen')
