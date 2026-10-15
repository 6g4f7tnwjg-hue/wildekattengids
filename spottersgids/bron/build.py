#!/usr/bin/env python3
"""Bouwt de Spottersgids (index.html) uit de KATalogue-gegevens en het onderzoek in data/.

Gebruik:  python3 bron/build.py      (vanuit de map spottersgids)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda *p: os.path.join(ROOT, *p)
load = lambda p: json.load(open(J(p), encoding='utf-8'))

# Soorten met een afgeronde soortpagina (per werelddeel uitgebreid)
PAGES = [24, 27, 37, 4, 38, 42]

# Dezelfde plek onder verschillende id's in de onderzoeksbestanden
ALIAS = json.load(open(J('data', 'alias.json'), encoding='utf-8')) if os.path.exists(J('data', 'alias.json')) else {}
CONT_MAP = {'eur': 'eur', 'afr': 'afr', 'asia': 'asia', 'namerica': 'nam', 'samerica': 'sam'}

cats = load('bron/katalogue.json')
for c in cats:
    c['cont'] = [CONT_MAP[x] for x in c['cont']]
    if c['no'] not in PAGES:
        c['photos'] = c['photos'][:1]
extra_cont = load('data/extra_cont.json') if os.path.exists(J('data', 'extra_cont.json')) else {}
for c in cats:
    for x in extra_cont.get(str(c['no']), []):
        if x not in c['cont']:
            c['cont'].append(x)

# Foto's als data-URI in de pagina: losse bestanden laden niet in elke viewer (o.a. de Claude-app)
import base64
for c in cats:
    for ph in c['photos']:
        if not ph['src'].startswith('data:'):
            ph['src'] = 'data:image/jpeg;base64,' + base64.b64encode(open(J(ph['src']), 'rb').read()).decode()

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

text = load('data/text.json')
for k, pg in text.items():
    pg['sources'] = [add_source(s) for s in pg.get('sources', [])]
europe = load('data/europe.json')

data = {'cats': cats, 'spots': list(spots.values()), 'pages': pages, 'sources': sources,
        'text': text, 'europe': europe, 'land': open(J('bron', 'land.txt')).read().strip()}
blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
html = open(J('bron', 'template.html'), encoding='utf-8').read().replace('__DATA__', blob)
open(J('index.html'), 'w', encoding='utf-8').write(html)
print(f'index.html: {len(html)//1024} kB, {len(spots)} plekken, {len(pages)} soortpagina\'s, {len(sources)} bronnen')
