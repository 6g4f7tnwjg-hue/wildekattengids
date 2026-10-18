# Jungle-stijl ("Expeditie", gekozen 18-10-2026) als losse laag over de website.
# bouw.py roept maak() als allerlaatste stap aan. Het zet in elke pagina één blok
# <!--jungle--> ... <!--/jungle--> vlak voor </body>: een lettertype-link en CSS.
# Gegevens, teksten, links en indeling blijven onaangeroerd; alleen de vormgeving verandert.
# Het blok wordt bij elke run eerst weggehaald en opnieuw gezet (dus vaker draaien is veilig).
# Terugdraaien: de regel onderaan bouw.py weghalen en opnieuw bouwen, of `python3 bron/jungle.py --weg`.
# Niet aangeraakt: de reservemappen /<land>-oud/, /spottersgids/ (later), /voorbeeld-jungle/ en /bron/.
import os, re, sys, math, urllib.parse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OVERSLAAN = ('spottersgids', 'voorbeeld-jungle', 'bron', '.git', 'img')
BEGIN, EIND = '<!--jungle-->', '<!--/jungle-->'

def uri(svg):
    return 'url("data:image/svg+xml,' + urllib.parse.quote(svg, safe=' =:/,;-.()') + '")'

def monstera(c1, c2):
    return uri(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 120'><defs><mask id='m'><rect width='100' height='120' fill='white'/><g stroke='black' stroke-width='5' stroke-linecap='round'><path d='M4 48 L30 57'/><path d='M8 80 L33 75'/><path d='M96 48 L70 57'/><path d='M92 80 L67 75'/><path d='M18 20 L37 40'/><path d='M82 20 L63 40'/></g><ellipse cx='37' cy='64' rx='3' ry='5' fill='black'/><ellipse cx='63' cy='64' rx='3' ry='5' fill='black'/></mask></defs><path mask='url(#m)' d='M50 4C82 8 98 38 94 66C90 94 68 112 50 116C32 112 10 94 6 66C2 38 18 8 50 4Z' fill='{c1}'/><path d='M50 116L50 14' stroke='{c2}' stroke-width='2.5' fill='none'/></svg>")

def palm(c):
    leaves = ''.join(f"<path d='M60 150 Q{60+dx} {150-dy} {60+dx*1.6} {150-dy*1.5}' stroke='{c}' stroke-width='14' stroke-linecap='round' fill='none'/>" for dx, dy in [(-40,40),(-28,70),(-10,90),(10,92),(30,70),(44,40)])
    return uri(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 160'>{leaves}<path d='M60 160V60' stroke='{c}' stroke-width='3'/></svg>")

def longleaf(c1, c2):
    return uri(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 160'><path d='M30 2C52 30 56 90 30 158C4 90 8 30 30 2Z' fill='{c1}'/><path d='M30 158V10' stroke='{c2}' stroke-width='2' fill='none'/><g stroke='{c2}' stroke-width='1.4' fill='none'><path d='M30 40L44 30M30 60L48 48M30 80L48 70M30 100L46 92M30 40L16 30M30 60L12 48M30 80L12 70M30 100L14 92'/></g></svg>")

def rosettes(col, op):
    def ros(cx, cy, r, rot):
        out = ''
        for k in range(5):
            a = math.radians(rot + k*72)
            x, y = cx + r*math.cos(a), cy + r*math.sin(a)
            out += f"<ellipse cx='{x:.1f}' cy='{y:.1f}' rx='{r*0.55:.1f}' ry='{r*0.32:.1f}' transform='rotate({rot+k*72+90:.0f} {x:.1f} {y:.1f})'/>"
        return out
    spots = ros(24,26,8,10) + ros(84,20,6,40) + ros(60,72,9,0) + ros(104,92,5,20) + ros(18,98,6,60)
    dots = "<circle cx='44' cy='44' r='2.4'/><circle cx='96' cy='54' r='2'/><circle cx='34' cy='70' r='1.8'/><circle cx='80' cy='108' r='2.2'/>"
    return uri(f"<svg xmlns='http://www.w3.org/2000/svg' width='120' height='120'><g fill='{col}' fill-opacity='{op}'>{spots}{dots}</g></svg>")

def paws(col):
    p = lambda x, y, r: f"<g transform='translate({x} {y}) rotate({r})'><ellipse cx='0' cy='4' rx='5' ry='4.2'/><ellipse cx='-6.5' cy='-2' rx='2' ry='2.6'/><ellipse cx='-2.4' cy='-6.4' rx='2' ry='2.6'/><ellipse cx='2.6' cy='-6.4' rx='2' ry='2.6'/><ellipse cx='6.8' cy='-2' rx='2' ry='2.6'/></g>"
    return uri(f"<svg xmlns='http://www.w3.org/2000/svg' width='64' height='26'><g fill='{col}'>{p(14,15,75)}{p(46,9,105)}</g></svg>")

def wave(col):
    return uri(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 40' preserveAspectRatio='none'><path d='M0 22C55 6 95 34 150 20S260 2 310 18S370 34 400 16V40H0Z' fill='{col}'/></svg>")

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Nunito:wght@400;600;700;800&display=swap">'

# kleuren
JG, SUN, BG, CARD, INK, MUTED, LINE = '#143A22', '#F2C14E', '#ECF2DF', '#FAFBF2', '#13301C', '#4C6450', '#CADBB9'
OLIVE, ACC, WOOD, WOOD_D = '#1F5A33', '#B8501C', '#DCAE76', '#9C6B36'
DISP = '"Anton","Impact","Arial Narrow",sans-serif'
BODY = '"Nunito",system-ui,-apple-system,sans-serif'


HOUT = "background:linear-gradient(180deg,rgba(255,255,255,.38) 0,rgba(255,255,255,.1) 42%,rgba(0,0,0,0) 55%,rgba(70,35,5,.14) 100%),repeating-linear-gradient(91deg,rgba(90,50,15,.07) 0 1px,transparent 1px 6px,rgba(90,50,15,.04) 6px 7px,transparent 7px 13px),linear-gradient(90deg,#D6A465,#E4B97F 45%,#D39E5E)!important;color:#5A3210!important;border:0!important;border-radius:9px!important;box-shadow:inset 0 1px 0 rgba(255,250,235,.7),inset 0 -2px 0 rgba(100,55,15,.28),0 1px 1px rgba(60,35,10,.35),0 4px 8px -4px rgba(60,35,10,.45)!important;text-shadow:0 1px 0 rgba(255,236,200,.75),0 -1px 0 rgba(70,35,5,.3);font-weight:800"
HOUT_AAN = "background:linear-gradient(180deg,rgba(255,255,255,.22) 0,rgba(255,255,255,.04) 45%,rgba(0,0,0,0) 55%,rgba(0,0,0,.2) 100%),#1D4A2C!important;color:#F2C14E!important;box-shadow:inset 0 1px 0 rgba(255,255,255,.3),inset 0 -2px 0 rgba(0,0,0,.3),0 1px 1px rgba(0,0,0,.35),0 4px 8px -4px rgba(10,36,20,.6)!important;text-shadow:0 -1px 0 rgba(0,0,0,.45)"

GEDEELD = f"""
@keyframes jw{{0%,100%{{transform:rotate(-4deg)}}50%{{transform:rotate(4deg)}}}}
html body{{background:{rosettes(OLIVE,'.06')},{BG}!important}}
html body h1,html body h2{{font-family:{DISP}!important;font-weight:400!important;text-transform:uppercase;letter-spacing:.01em;line-height:1.02}}
html body h3{{font-family:{BODY};font-weight:800}}
html body .jg-blad{{pointer-events:none}}
html body .nw-bar{{background:{JG}!important;border-top:0!important;-webkit-backdrop-filter:none;backdrop-filter:none}}
html body .nw-bar a,html body .nw-bar a:hover,html body .nw-bar a:visited{{color:#BFD9A8!important}}
html body .nw-bar a.on{{color:{SUN}!important}}
html body .nw-bar a.on::before,html body .nw-bar a.on::after{{background:{SUN}!important}}
@media (prefers-reduced-motion:reduce){{html body *{{animation:none!important}}}}
"""

# Europa-pagina's: startpagina, top 10, /soort/…
EUROPA = f"""
:root{{--bg:{BG};--paper:{CARD};--card:{CARD};--ink:{INK};--muted:{MUTED};--line:{LINE};--olive:{OLIVE};--dot:{OLIVE};--accent:{ACC};
 --sea:#86C8D9;--land:#A3CC80;--land-line:#6FA552;--nb:#D8E4C6;--nw-green:{OLIVE};--nw-terra:{ACC};
 --display:{BODY};--body:{BODY};--hs-body:{BODY}}}
html body{{font-family:{BODY}}}
html body .top{{background:{palm('#1E4D2D')} right -20px top -40px/120px no-repeat,{JG};border-bottom:0;color:#F1F5E4}}
html body .top .brand,html body .top .brand b{{color:#F1F5E4}}
html body .top .brand b{{font-family:{DISP};font-weight:400!important;letter-spacing:.02em}}
html body .top .brand small{{color:#BFD9A8;white-space:nowrap;font-size:.58rem}}
html body .top .brand svg{{color:{SUN}}}
html body .top .icobtn,html body .top .lm .lm-btn{{border-color:#3C6B49;color:#F1F5E4;background:#1C4A2C}}
html body .top .icobtn[aria-expanded="true"]{{background:{SUN};color:{JG};border-color:{SUN}}}
html body .intro{{position:relative;overflow:hidden;isolation:isolate;background:{rosettes('#FFFFFF','.07')},{JG};color:#F1F5E4;padding-bottom:44px}}
html body .intro .wrap{{position:relative;z-index:2}}
html body .intro h1{{color:{SUN};font-size:clamp(2rem,9.2vw,3.2rem);max-width:none}}
html body .intro h1::first-line{{color:#F1F5E4}}
html body .intro .sub{{color:#D3E4C2;max-width:22rem}}
html body .intro .meta,html body .intro .meta *{{color:{SUN}!important}}
html body .intro::before{{content:"";position:absolute;right:-34px;top:-14px;width:150px;height:180px;background:{monstera('#2F7A3B','#1D5527')} no-repeat center/contain;transform-origin:top center;animation:jw 6s ease-in-out infinite;z-index:1;pointer-events:none}}
html body .intro::after{{content:"";position:absolute;left:0;right:0;bottom:-1px;height:30px;background:{wave(BG)} no-repeat center/100% 100%;z-index:3;pointer-events:none}}
html body .intro .wrap::after{{content:"";position:absolute;right:-6px;bottom:-30px;width:48px;height:130px;background:{longleaf('#5FA84A','#3B7A2E')} no-repeat center/contain;transform-origin:top center;animation:jw 7s ease-in-out infinite;z-index:-1;pointer-events:none}}
html body .chip{{{HOUT}}}
html body .chip[aria-pressed="true"]{{{HOUT_AAN}}}
html body .lbl{{font-family:{DISP};font-size:1.15rem;letter-spacing:.04em;color:{OLIVE};display:flex;align-items:center;gap:8px}}
html body .lbl::before{{content:"";flex:none;width:46px;height:20px;background:{paws('#C9561F')} center/contain no-repeat}}
html body .catbtn .av{{border:3px solid {SUN};box-shadow:0 2px 0 {WOOD_D}}}
html body .catbtn[aria-pressed="true"]{{background:#D4E6BF!important}}
html body .catbtn[aria-pressed="true"] .av{{border-color:{JG};box-shadow:0 0 0 3px {SUN}}}
html body .mapbox{{border-radius:18px;overflow:hidden;box-shadow:0 0 0 4px {JG},0 10px 24px -12px rgba(20,58,34,.5)}}
html body .cl .cdot{{fill:{JG};stroke:{SUN};stroke-width:2}}
html body .cl .cn{{fill:#FFF8DC}}
html body .zoombtns button{{background:{SUN}!important;color:{JG}!important;border-color:{JG}!important}}
"""

# landpagina's en de losse park- en soortpagina's
LAND = f"""
:root{{--paper:{BG};--card:{CARD};--ink:{INK};--muted:{MUTED};--line:{LINE};--gold:{ACC};--gold-soft:#F6E3B0;--bark:{OLIVE};--tan:{CARD};--tan-deep:{LINE};
 --hs-olive:{OLIVE};--hs-accent:{ACC};--hs-display:{BODY};--hs-body:{BODY};
 --nw-sage:#DCEBC9;--nw-green:{OLIVE};--nw-terra:{ACC}}}
html{{background:{BG}!important}}
html body{{font-family:{BODY}}}
html body .hs-top{{background:{palm('#1E4D2D')} right -20px top -40px/120px no-repeat,{JG}!important;border-bottom:0!important;color:#F1F5E4}}
html body .hs-top .hs-brand,html body .hs-top .hs-brand b{{color:#F1F5E4!important}}
html body .hs-top .hs-brand b{{font-family:{DISP}!important;font-weight:400!important;letter-spacing:.02em}}
html body .hs-top .hs-brand small{{color:#BFD9A8!important;white-space:nowrap}}
html body .hs-top .hs-brand svg{{color:{SUN}!important}}
html body .hs-top .hs-ico,html body .hs-top .lm .lm-btn{{border-color:#3C6B49!important;color:#F1F5E4!important;background:#1C4A2C!important}}
html body .hs-top .hs-ico[aria-expanded="true"]{{background:{SUN}!important;color:{JG}!important;border-color:{SUN}!important}}
/* kop van de landpagina: groene band met blad en golfrand */
html body .nt-kop{{position:relative;overflow:hidden;isolation:isolate;background:{rosettes('#FFFFFF','.07')},{JG};margin:0 -20px!important;padding:20px 20px 44px;color:#F1F5E4}}
html body .nt-kop h1.mast.hs-kop,html body .nt-kop h1.mast.hs-kop .m2,html body .nt-kop h1.mast.hs-kop span{{color:#F1F5E4!important;font-family:{DISP}!important;font-weight:400!important;letter-spacing:.01em!important}}
html body .nt-kop h1.mast.hs-kop{{font-size:clamp(2.2rem,10vw,3.2rem)!important}}
html body #nt-kaart .map .land{{fill:#A3CC80!important;stroke:#6FA552!important}}
html body #nt-kaart .map .water,html body #nt-kaart .map{{fill:#86C8D9}}
html body #nt-kaart .map .water{{fill:#86C8D9!important;stroke:#6FA552!important}}
html body .nt-kop .hs-onder{{color:#D3E4C2!important}}
html body .nt-kop .nt-meta,html body .nt-kop .nt-meta *{{color:{SUN}!important}}
html body .nt-kop>*{{position:relative;z-index:2}}
html body .nt-kop::before{{content:"";position:absolute;right:-30px;top:-12px;width:130px;height:160px;background:{monstera('#2F7A3B','#1D5527')} no-repeat center/contain;transform-origin:top center;animation:jw 6s ease-in-out infinite;z-index:1;pointer-events:none}}
html body .nt-kop::after{{content:"";position:absolute;left:0;right:0;bottom:-1px;height:28px;background:{wave(BG)} no-repeat center/100% 100%;z-index:3;pointer-events:none}}
html body .nt-lbl{{font-family:{DISP};font-size:1.1rem;letter-spacing:.04em;color:{OLIVE}!important;text-transform:uppercase;display:flex;align-items:center;gap:8px;margin-top:14px}}
html body .nt-lbl::before{{content:"";flex:none;width:46px;height:20px;background:{paws('#C9561F')} center/contain no-repeat}}
html body .nt-av{{border:3px solid {SUN}!important;box-shadow:0 2px 0 {WOOD_D}!important}}
html body .nt-cat[aria-pressed="true"]{{background:#D4E6BF!important}}
html body .nt-cat[aria-pressed="true"] .nt-av{{border-color:{JG}!important;box-shadow:0 0 0 3px {SUN}!important}}
html body .nt-av.nt-all{{background:{JG}!important;color:{SUN}!important}}
html body #nt-kaart{{border-radius:18px;overflow:hidden;box-shadow:0 0 0 4px {JG},0 10px 24px -12px rgba(20,58,34,.5)}}
html body .chip,html body .nt-types button{{{HOUT}}}
html body .chip[aria-pressed="true"],html body .nt-types button[aria-pressed="true"]{{{HOUT_AAN}}}
/* losse park- en soortpagina's */
html body .nw-sbar{{background:transparent}}
html body .nw-sbar .nw-stitle{{font-family:{DISP};font-weight:400;text-transform:uppercase;letter-spacing:.03em;color:{OLIVE}}}
html body .nw-back{{background:{SUN}!important;color:{JG}!important;border-color:{JG}!important;font-weight:800}}
html body .ip-head{{position:relative;overflow:hidden;isolation:isolate;background:{rosettes('#FFFFFF','.07')},{JG};margin:0 -20px;padding:18px 20px 46px!important;border-bottom:0!important}}
html body .ip-head>*{{position:relative;z-index:2}}
html body .ip-head h1{{color:#F1F5E4!important}}
html body .ip-head .ip-alt,html body .ip-head p,html body .ip-head i,html body .ip-head em{{color:#D3E4C2!important}}
html body .ip-head .ip-tag{{background:#1C4A2C!important;color:#F1F5E4!important;border-color:#3C6B49!important}}
html body .ip-head .ip-tag.dark{{background:{SUN}!important;color:{JG}!important;border-color:{SUN}!important}}
html body .ip-head::before{{content:"";position:absolute;right:-28px;top:-10px;width:110px;height:136px;background:{monstera('#2F7A3B','#1D5527')} no-repeat center/contain;transform-origin:top center;animation:jw 6s ease-in-out infinite;z-index:1;pointer-events:none}}
html body .ip-head::after{{content:"";position:absolute;left:0;right:0;bottom:-1px;height:28px;background:{wave(BG)} no-repeat center/100% 100%;z-index:3;pointer-events:none}}
html body .ip-photo{{border-radius:16px;overflow:hidden;box-shadow:0 0 0 4px {SUN}}}
html body .ip-fact,html body .ip-box{{background:{CARD}!important;border-color:{LINE}!important}}
html body .ip-sec h2{{color:{OLIVE}}}
html body .ip-sec h2::after{{content:"";display:block;width:46px;height:20px;margin-top:6px;background:{paws('#C9561F')} left center/contain no-repeat}}
html body .hs-kofi{{background:{SUN}!important;color:{JG}!important;border-color:{SUN}!important}}
@media (min-width:1120px){{html body .nt-kop,html body .ip-head{{border-radius:22px}}}}
"""

def blok(html):
    land = 'id="hs-top"' in html or "id='hs-top'" in html
    css = GEDEELD + (LAND if land else EUROPA)
    return f'{BEGIN}{FONTS}<style id="jungle">{css}</style>{EIND}'

def weg(html):
    return re.sub(re.escape(BEGIN) + r'.*?' + re.escape(EIND), '', html, flags=re.S)

def zet(html):
    html = weg(html)
    b = blok(html)
    i = html.rfind('</body>')
    return html[:i] + b + html[i:] if i >= 0 else html + b

def bestanden():
    out = []
    for d, dirs, files in os.walk(ROOT):
        rel = os.path.relpath(d, ROOT)
        top = rel.split(os.sep)[0]
        if top in OVERSLAAN or top.endswith('-oud'):
            dirs[:] = []
            continue
        for f in files:
            if f == 'index.html':
                p = os.path.join(d, f)
                s = open(p, encoding='utf-8').read()
                if 'http-equiv="refresh"' in s and len(s) < 2000:
                    continue  # doorverwijzing
                out.append(p)
    return sorted(out)

def maak(verwijder=False):
    n = 0
    for p in bestanden():
        s = open(p, encoding='utf-8').read()
        t = weg(s) if verwijder else zet(s)
        if t != s:
            open(p, 'w', encoding='utf-8').write(t)
            n += 1
    print('jungle-stijl', 'weggehaald uit' if verwijder else 'gezet op', n, "pagina's")

if __name__ == '__main__':
    maak(verwijder='--weg' in sys.argv)
