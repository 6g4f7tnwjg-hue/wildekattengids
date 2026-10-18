# Jungle-stijl ("Expeditie", gekozen 18-10-2026) als losse laag over de website.
# bouw.py roept maak() als allerlaatste stap aan. Het zet in elke pagina één blok
# <!--jungle--> ... <!--/jungle--> vlak voor </body>: een lettertype-link en CSS.
# Gegevens, teksten, links en indeling blijven onaangeroerd; alleen de vormgeving verandert.
# Het blok wordt bij elke run eerst weggehaald en opnieuw gezet (dus vaker draaien is veilig).
# Terugdraaien: de regel onderaan bouw.py weghalen en opnieuw bouwen, of `python3 bron/jungle.py --weg`.
# Niet aangeraakt: de reservemappen /<land>-oud/, /spottersgids/ (later), /voorbeeld-jungle/ en /bron/.
import os, re, sys, math, json, urllib.parse

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

# luipaard op de rand van het Ko-fi-blok (18-10-2026): ingevoegd met een klein script, zodat kop, ogen, oor en staart kunnen bewegen; tik = opkijken en knipperen
import random
LO = '#3B2414'   # omlijning
LF = '#E6AE4C'   # vacht
LB = '#F6DDA6'   # buik
LW = '#FBF1DC'   # wit (snuit, kin)
LS = '#2E1C0F'   # vlekken
LC = '#C98E34'   # midden van een rozet

def rozet(cx, cy, r, rot, seed):
    rnd = random.Random(seed)
    n = rnd.choice((3, 3, 4))
    out = f"<ellipse cx='{cx:.1f}' cy='{cy:.1f}' rx='{r*0.78:.1f}' ry='{r*0.62:.1f}' transform='rotate({rot:.0f} {cx:.1f} {cy:.1f})' fill='{LC}'/>"
    step = 360 / n
    for k in range(n):
        a0 = rot + k * step + rnd.uniform(4, 22)
        a1 = rot + (k + 1) * step - rnd.uniform(10, 42)
        rr = r * rnd.uniform(0.92, 1.08)
        p0 = (cx + rr * math.cos(math.radians(a0)), cy + rr * 0.8 * math.sin(math.radians(a0)))
        p1 = (cx + rr * math.cos(math.radians(a1)), cy + rr * 0.8 * math.sin(math.radians(a1)))
        out += (f"<path d='M{p0[0]:.1f} {p0[1]:.1f} A{rr:.1f} {rr*0.8:.1f} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}' "
                f"stroke='{LS}' stroke-width='{max(1.8, r*rnd.uniform(0.28, 0.48)):.1f}' stroke-linecap='round' fill='none'/>")
    return out

def stip(cx, cy, r):
    return f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='{LS}'/>"

def oog(cx, stijl='groen'):
    """Eén oog. 'groen' = huidige ogen; 'rond', 'amber' en 'tevreden' zijn voorbeelden om uit te kiezen."""
    s_ = -1 if cx < 70 else 1
    def wimpers(punten):
        return "".join(f"<path d='M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}' stroke='{LO}' stroke-width='1.5' stroke-linecap='round'/>" for x1, y1, x2, y2 in punten)
    if stijl == 'rond':
        r = 6.8
        ws = []
        for hoek in (200, 228, 256):
            h = math.radians(hoek if s_ < 0 else 180 - hoek)
            ws.append((cx + r*math.cos(h), 48 + r*math.sin(h), cx + (r+3.4)*math.cos(h), 48 + (r+3.4)*math.sin(h)))
        return (f"<g class='jg-oog'><circle cx='{cx}' cy='48' r='{r}' fill='#C9D94A' stroke='{LO}' stroke-width='1.8'/>"
                f"<circle cx='{cx}' cy='48.4' r='3.8' fill='{LO}'/><circle cx='{cx+2.1}' cy='46' r='1.6' fill='#fff'/><circle cx='{cx-1.6}' cy='50.5' r='.8' fill='#fff'/>"
                + wimpers(ws) + "</g>")
    if stijl == 'amber':
        x0 = cx + 8*s_
        return (f"<g class='jg-oog'><path d='M{cx-8} 49 C{cx-4} 42.5 {cx+4} 42.5 {cx+8} 48.5 C{cx+4} 53.5 {cx-4} 53.5 {cx-8} 49 Z' fill='#E2AE38' stroke='{LO}' stroke-width='2'/>"
                f"<circle cx='{cx}' cy='48.6' r='2.6' fill='{LO}'/><circle cx='{cx+1.5}' cy='47.2' r='1.1' fill='#fff'/>"
                f"<path d='M{x0} 48.6 L{x0+3.4*s_} 46.8' stroke='{LO}' stroke-width='2.2' stroke-linecap='round'/>"
                + wimpers([(x0+1*s_, 47.6, x0+3.4*s_, 43.6), (x0-1.4*s_, 46.2, x0+0.4*s_, 42.4), (x0+2.4*s_, 47.4, x0+5.6*s_, 45.6)]) + "</g>")
    if stijl == 'tevreden':
        x0 = cx + 8*s_
        return (f"<g class='jg-oog'><path d='M{cx-8} 49 C{cx-4} 43 {cx+4} 43 {cx+8} 49 C{cx+4} 53 {cx-4} 53 {cx-8} 49 Z' fill='#C9D94A' stroke='{LO}' stroke-width='1.8'/>"
                f"<ellipse cx='{cx}' cy='50' rx='1.7' ry='2.6' fill='{LO}'/><circle cx='{cx+1.5}' cy='49.2' r='.8' fill='#fff'/>"
                f"<path d='M{cx-8.6} 49 C{cx-4} 42 {cx+4} 42 {cx+8.6} 49 C{cx+4} 46.6 {cx-4} 46.6 {cx-8.6} 49 Z' fill='{LF}'/>"
                f"<path d='M{cx-8} 49 C{cx-4} 46.4 {cx+4} 46.4 {cx+8} 49' stroke='{LO}' stroke-width='2' fill='none' stroke-linecap='round'/>"
                + wimpers([(x0-0.4*s_, 48.4, x0+3.4*s_, 46.2), (x0-1.8*s_, 47.6, x0+1.2*s_, 44.6), (x0+0.2*s_, 49.4, x0+4*s_, 49)]) + "</g>")
    return (f"<g class='jg-oog'><path d='M{cx-8} 49 C{cx-4} 43 {cx+4} 43 {cx+8} 49 C{cx+4} 53 {cx-4} 53 {cx-8} 49 Z' fill='#C9D94A' stroke='{LO}' stroke-width='1.8'/>"
            f"<ellipse cx='{cx}' cy='49' rx='1.8' ry='3.6' fill='{LO}'/><circle cx='{cx+1.6}' cy='47' r='1' fill='#fff'/>"
            + (lambda x0: f"<path d='M{x0-0.5*s_} 47.6 L{x0+3.6*s_} 44.6 M{x0} 46.2 L{x0+2.6*s_} 42.2 M{x0-0.2*s_} 49.2 L{x0+4.2*s_} 48' stroke='{LO}' stroke-width='1.5' stroke-linecap='round'/></g>")(cx + 7.4*s_))

def svg(stijl='rond'):
    o = f"stroke='{LO}' stroke-width='2' stroke-linejoin='round' stroke-linecap='round'"
    g = []
    g.append("<defs><linearGradient id='jglp-v' x1='0' y1='0' x2='0' y2='1'>"
             f"<stop offset='0' stop-color='#E2A843'/><stop offset='.62' stop-color='{LF}'/><stop offset='1' stop-color='{LB}'/></linearGradient>"
             "<clipPath id='jglp-c'><path d='M64 96 C62 70 86 56 120 52 C150 48 182 50 200 62 C212 70 216 84 214 96 Z'/></clipPath></defs>")
    # schaduw op de rand
    g.append("<ellipse cx='136' cy='97' rx='86' ry='3.2' fill='#000' opacity='.13'/>")
    # staart (achter het lijf; het begin zit verstopt achter de heup)
    t = "M200 78 C214 82 222 90 222 102 C222 112 214 116 216 124 C217 129 222 130 226 127"
    g.append("<g class='jg-staart'>")
    g.append(f"<path d='{t}' fill='none' stroke='{LO}' stroke-width='11' stroke-linecap='round'/>")
    g.append(f"<path d='{t}' fill='none' stroke='{LF}' stroke-width='7' stroke-linecap='round'/>")
    for x, y, a in ((214, 86, 30), (220, 96, 80), (221, 106, 95), (217, 116, 70)):
        g.append(f"<ellipse cx='{x}' cy='{y}' rx='3.2' ry='1.6' transform='rotate({a} {x} {y})' fill='{LS}'/>")
    g.append(f"<path d='M217 122 C218 127 221 128 224 126' stroke='{LS}' stroke-width='5' fill='none' stroke-linecap='round'/>")
    g.append("</g>")
    # lijf
    body = "M64 96 C62 70 86 56 120 52 C150 48 182 50 200 62 C212 70 216 84 214 96 Z"
    g.append(f"<path d='{body}' fill='url(#jglp-v)' {o}/>")
    # rozetten op het lijf
    ros = [(100, 66, 6.5, 10), (122, 61, 6, 40), (145, 60, 6.5, -10), (168, 62, 6, 25), (112, 79, 5.5, 60), (134, 76, 6, 5),
           (156, 77, 5.5, 35), (92, 82, 4.5, 15), (126, 90, 3.8, 50), (148, 90, 3.6, 20), (188, 70, 5, 10)]
    g.append("<g clip-path='url(#jglp-c)'>" + ''.join(rozet(x, y, r, a, i) for i, (x, y, r, a) in enumerate(ros))
             + stip(110, 56, 1.6) + stip(135, 54, 1.6) + stip(158, 54, 1.5) + stip(84, 70, 1.6) + "</g>")
    # heup en achterpoot
    g.append(f"<path d='M168 96 C164 80 172 66 188 66 C204 66 212 80 210 96' fill='url(#jglp-v)' {o}/>")
    g.append(rozet(190, 78, 5, 20, 99) + stip(178, 86, 1.6) + stip(200, 88, 1.5) + stip(196, 72, 1.4))
    g.append(f"<path d='M150 96 C150 89 158 87 170 88 C178 89 180 93 180 96' fill='{LB}' {o}/>")
    g.append(f"<path d='M160 92 L160 96 M166 91 L166 96 M172 91 L172 96' stroke='{LO}' stroke-width='1.4' stroke-linecap='round'/>")
    # voorpoten over de rand
    for x in (52, 78):
        g.append(f"<path d='M{x} 76 L{x} 112 C{x} 121 {x+19} 121 {x+19} 112 L{x+19} 76' fill='{LF}' {o}/>")
        g.append(f"<path d='M{x+2} 106 C{x+6} 110 {x+13} 110 {x+17} 106 L{x+17} 113 C{x+17} 119 {x+2} 119 {x+2} 113 Z' fill='{LB}'/>")
        g.append(f"<path d='M{x+6.5} 114 L{x+6.5} 119 M{x+12.5} 114 L{x+12.5} 119' stroke='{LO}' stroke-width='1.4' stroke-linecap='round'/>")
        g.append(stip(x + 6, 90, 1.7) + stip(x + 13, 96, 1.6) + stip(x + 8, 101, 1.4) + stip(x + 14, 86, 1.4))
    # kop
    g.append("<g class='jg-kop'>")
    for side, cx in (('l', 46), ('r', 94)):
        sgn = -1 if side == 'l' else 1
        g.append(f"<g class='jg-oor-{side}'>")
        g.append(f"<path d='M{cx-12*sgn} 34 C{cx-16*sgn} 18 {cx-2*sgn} 10 {cx+6*sgn} 16 C{cx+12*sgn} 22 {cx+12*sgn} 34 {cx+9*sgn} 46 Z' fill='{LS}' {o}/>")
        g.append(f"<path d='M{cx-9*sgn} 32 C{cx-11*sgn} 22 {cx-2*sgn} 16 {cx+3*sgn} 20 C{cx+7*sgn} 24 {cx+8*sgn} 32 {cx+6*sgn} 40 Z' fill='{LW}'/>")
        g.append("</g>")
    head = "M70 22 C92 22 106 36 106 54 C106 66 100 74 92 80 C86 85 78 88 70 88 C62 88 54 85 48 80 C40 74 34 66 34 54 C34 36 48 22 70 22 Z"
    g.append(f"<path d='{head}' fill='{LF}' {o}/>")
    # een paar vlekjes op het voorhoofd en de zijkanten (simpel gehouden)
    for x, y, r in ((62, 31, 1.7), (70, 29, 1.8), (78, 31, 1.7), (66, 37, 1.5), (74, 37, 1.5), (42, 54, 1.7), (98, 54, 1.7), (45, 64, 1.5), (95, 64, 1.5)):
        g.append(stip(x, y, r))
    # witte snuit (zonder kin)
    g.append(f"<path d='M70 60 C78 60 86 64 86 70 C86 76 79 79 70 79 C61 79 54 76 54 70 C54 64 62 60 70 60 Z' fill='{LW}'/>")
    # ogen (knipperen)
    for cx in (56, 84):
        g.append(oog(cx, stijl))
    # streepjes van de ooghoeken naar de neus
    g.append(f"<path d='M62 52 C64 56 65 59 66 62 M78 52 C76 56 75 59 74 62' stroke='{LS}' stroke-width='1.6' fill='none' stroke-linecap='round'/>")
    # neus en mond
    g.append(f"<path d='M64 63 L76 63 C76 67 72 70 70 70 C68 70 64 67 64 63 Z' fill='#B5603A' stroke='{LO}' stroke-width='1.6'/>")
    g.append(f"<path d='M70 70 L70 73 C68 76 64 76 62 74 M70 73 C72 76 76 76 78 74' stroke='{LO}' stroke-width='1.6' fill='none' stroke-linecap='round'/>")
    # snorharen
    g.append(f"<g stroke='{LO}' stroke-width='1' stroke-linecap='round' fill='none' opacity='.85'>"
             "<path d='M57 69 C46 66 36 66 26 68'/><path d='M57 72 C46 72 36 73 27 76'/><path d='M58 75 C48 77 40 80 32 85'/>"
             "<path d='M83 69 C94 66 104 66 114 68'/><path d='M83 72 C94 72 104 73 113 76'/><path d='M82 75 C92 77 100 80 108 85'/></g>")
    g.append("</g>")
    return f"<svg viewBox='0 0 240 132' xmlns='http://www.w3.org/2000/svg'>{''.join(g)}</svg>"

LP_CSS = """
html body .foot,html body .hs-foot{position:relative;margin-top:100px!important;overflow:visible}
html body .foot .wrap,html body .hs-foot .hs-wrap{padding-top:44px!important}
html body .jg-lp{position:absolute;left:max(6px,calc(50% - 534px));top:-96px;width:240px;height:132px;z-index:2;cursor:pointer;-webkit-tap-highlight-color:transparent}
html body .jg-lp svg{display:block;width:100%;height:100%;overflow:visible}
.jg-lp .jg-kop{transform-box:view-box;transform-origin:70px 86px;animation:jgkop 9s ease-in-out infinite}
.jg-lp .jg-oog{transform-box:fill-box;transform-origin:center;animation:jgoog 5.3s infinite}
.jg-lp .jg-oor-l{transform-box:view-box;transform-origin:48px 32px;animation:jgoor 7.4s infinite}
.jg-lp .jg-staart{transform-box:view-box;transform-origin:204px 80px;animation:jgstaart 3.4s ease-in-out infinite}
@keyframes jgkop{0%,55%,100%{transform:rotate(0)}62%,78%{transform:rotate(-6deg)}86%{transform:rotate(2deg)}}
@keyframes jgoog{0%,92%,100%{transform:scaleY(1)}95%{transform:scaleY(.08)}}
@keyframes jgoor{0%,80%,100%{transform:rotate(0)}82%{transform:rotate(-14deg)}84%{transform:rotate(0)}86%{transform:rotate(-9deg)}88%{transform:rotate(0)}}
@keyframes jgstaart{0%,100%{transform:rotate(-7deg)}50%{transform:rotate(9deg)}}
.jg-lp.jg-tik .jg-kop{animation:jgtik 1.3s ease-in-out}
.jg-lp.jg-tik .jg-oog{animation:jgoog2 1.3s}
@keyframes jgtik{0%{transform:rotate(0)}25%,70%{transform:translateY(-5px) rotate(5deg)}100%{transform:rotate(0)}}
@keyframes jgoog2{0%,30%,48%,100%{transform:scaleY(1)}38%{transform:scaleY(.08)}}
@media (prefers-reduced-motion:reduce){.jg-lp *{animation:none!important}}
"""

LP_JS = ("(function(){var f=document.querySelector('footer.foot,footer.hs-foot');if(!f||f.querySelector('.jg-lp'))return;"
      "var d=document.createElement('div');d.className='jg-lp';d.setAttribute('aria-hidden','true');d.innerHTML=%s;"
      "f.insertBefore(d,f.firstChild);d.addEventListener('click',function(){d.classList.remove('jg-tik');void d.offsetWidth;"
      "d.classList.add('jg-tik');setTimeout(function(){d.classList.remove('jg-tik')},1400)})})();")


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
html body .chip svg.flag,html body .chip svg:not(.ti){{box-shadow:none!important;border-radius:3px!important;overflow:hidden;filter:drop-shadow(0 1px 0 rgba(255,240,210,.85)) drop-shadow(0 -1px 0 rgba(70,35,5,.35))}}
/* tussenschermen (19-10-2026): groene kop, menu-icoontjes, zoekveld, houten filterknoppen, soortkaartjes */
html body .nw-sbar{{overflow:hidden;isolation:isolate;background:{rosettes('#FFFFFF','.07')},{JG}!important;padding:13px 20px 34px!important;border-bottom:0!important;margin:-1px -20px 6px!important;top:56px!important}}
html body .nw-sbar>*{{position:relative;z-index:2}}
html body .nw-sbar::before{{content:"";position:absolute;right:-26px;top:-14px;width:96px;height:118px;background:{monstera('#2F7A3B','#1D5527')} no-repeat center/contain;transform-origin:top center;animation:jw 6s ease-in-out infinite;z-index:1;pointer-events:none}}
html body .nw-sbar::after{{content:"";position:absolute;left:0;right:0;bottom:-1px;height:24px;background:{wave(BG)} no-repeat center/100% 100%;z-index:3;pointer-events:none}}
html body .nw-sbar .nw-stitle,html body .nw-sbar .nw-stitle *{{color:#F1F5E4!important;font-family:{DISP}!important;font-weight:400!important;text-transform:uppercase;letter-spacing:.02em}}
html body .nw-sbar .nw-stitle{{font-size:1.9rem!important;line-height:1!important}}
html body .nw-sbar.nw-los{{padding-bottom:10px!important;margin:-1px -20px 0!important}}
html body .nw-sbar.nw-los::after,html body .nw-sbar.nw-los::before{{display:none}}
html body .nw-sbar.nw-los+*,html body .nw-sbar.nw-los~#info .ip-head{{margin-top:0!important}}
html body .jg-kop{{position:relative;overflow:hidden;isolation:isolate;background:{rosettes('#FFFFFF','.07')},{JG};margin:-18px calc(-1 * var(--gut,16px)) 18px;padding:16px var(--gut,16px) 42px;color:#F1F5E4}}
html body .jg-kop>*{{position:relative;z-index:2}}
html body .jg-kop::before{{content:"";position:absolute;right:-28px;top:-14px;width:110px;height:136px;background:{monstera('#2F7A3B','#1D5527')} no-repeat center/contain;transform-origin:top center;animation:jw 6s ease-in-out infinite;z-index:1;pointer-events:none}}
html body .jg-kop::after{{content:"";position:absolute;left:0;right:0;bottom:-1px;height:28px;background:{wave(BG)} no-repeat center/100% 100%;z-index:3;pointer-events:none}}
html body .jg-kop .terug{{display:inline-flex;align-items:center;gap:6px;min-height:40px;padding:0 16px;border-radius:999px;background:{SUN};color:{JG}!important;border:2px solid {JG};font-weight:800;text-decoration:none!important;margin:0 0 12px}}
html body .jg-kop h1,html body .jg-kop h1 *{{color:#F1F5E4!important}}
html body .jg-kop .sub,html body .jg-kop .kat-sum,html body .jg-kop .kat-sci,html body .jg-kop .kat-kern,html body .jg-kop figcaption,html body .jg-kop figcaption a{{color:#D3E4C2!important}}
html body .jg-kop .kat-spot{{color:{SUN}!important}}
html body .jg-kop .kat-feit dt{{color:{MUTED}!important}}
html body .jg-kop .kat-feit dd{{color:{INK}!important}}
html body .jg-kop .kat-foto img{{border-radius:14px;box-shadow:0 0 0 4px {SUN}}}
html body .nw-meer a>svg:first-child,html body .nt-ml a>svg:first-child{{width:36px!important;height:36px!important;padding:8px;box-sizing:border-box;border-radius:50%;background:{JG};color:{SUN}!important;stroke:currentColor;flex:none}}
html body .nw-meer a>svg:last-child,html body .nt-ml a>svg:last-child{{color:{OLIVE}!important}}
html body .nw-search label{{border:2px solid {OLIVE}!important;background:#FFFFFF!important}}
html body .nw-search svg{{color:{OLIVE}!important}}
html body .lt-chip,html body .rg-chip{{{HOUT}}}
html body .lt-chip[aria-pressed="true"],html body .rg-chip[aria-pressed="true"]{{{HOUT_AAN}}}
html body .group-title .gtog,html body .group-title .gtog *{{font-family:{DISP}!important;font-weight:400!important;text-transform:uppercase;letter-spacing:.03em;color:{OLIVE}!important}}
html body .group-title .gtog{{display:inline-flex;align-items:center;gap:8px;font-size:1.15rem!important}}
html body .group-title .gtog::before{{content:"";flex:none;width:46px;height:20px;background:{paws('#C9561F')} center/contain no-repeat}}
html body .nt-sc img{{border-bottom:3px solid {SUN}}}
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
    css = GEDEELD + (LAND if land else EUROPA) + LP_CSS
    js = LP_JS % json.dumps(svg()) + "(function(){var ts=document.querySelectorAll('.terug');for(var i=0;i<ts.length;i++){var t=ts[i],p=t.parentElement;if(!p||p.classList.contains('jg-kop'))continue;var k=document.createElement('div');k.className='jg-kop';p.insertBefore(k,t);var x=t.nextElementSibling;k.appendChild(t);while(x&&(x.tagName=='H1'||(x.tagName=='P'&&x.classList.contains('sub'))||x.classList.contains('kat-h'))){var n=x.nextElementSibling;k.appendChild(x);x=n;}}})();"
    return f'{BEGIN}{FONTS}<style id="jungle">{css}</style><script>{js}</script>{EIND}'

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
