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


# groene kop op tussenschermen: vlag, lichte onderregel en goudgele regel zoals de hoofdpagina (19-10-2026)
KOP_JS = r"""(function(){
var ks=document.querySelectorAll('.jg-kop');for(var i=0;i<ks.length;i++){var k=ks[i];if(k.querySelector('figure, .kat-foto')){k.classList.add('jg-foto');continue;}
 var u=k.querySelectorAll('.sub, .kat-sum');for(var j=u.length-1;j>=0;j--){u[j].classList.add('jg-uitleg');k.parentNode.insertBefore(u[j],k.nextSibling);}}
var sb=document.getElementById('nw-sbar');if(!sb||sb.classList.contains('nw-los'))return;
var kop=document.querySelector('.nt-kop');if(!kop)return;
var vlag=kop.querySelector('h1 svg');var ond=kop.querySelector('.hs-onder');var meta=kop.querySelector('.nt-meta');var datum=kop.querySelector('.nw-datum');
var T={
 loc:{nl:'Dierentuinen, parken en opvang',en:'Zoos, animal parks and sanctuaries',fr:'Zoos, parcs et refuges',de:'Zoos, Tierparks und Auffangstationen',it:'Zoo, parchi e centri di recupero',es:'Zoos, parques y santuarios',pt:'Zoos, parques e santuários'},
 sp:{nl:'Welke wilde katten je hier kunt zien',en:'Which wild cats you can see here',fr:'Les félins à voir ici',de:'Welche Wildkatzen du hier sehen kannst',it:'Quali felini puoi vedere qui',es:'Qué felinos puedes ver aquí',pt:'Que felinos podes ver aqui'},
 meer:{nl:'Achtergrond, nieuws en routeplanner',en:'Background, news and route planner',fr:'Contexte, actualités et itinéraire',de:'Hintergrund, Neuigkeiten und Routenplaner',it:'Contesto, novità e percorso',es:'Contexto, novedades y ruta',pt:'Contexto, novidades e roteiro'},
 locw:{nl:'locaties',en:'locations',fr:'lieux',de:'Orte',it:'luoghi',es:'lugares',pt:'locais'},
 spw:{nl:'soorten',en:'species',fr:'espèces',de:'Arten',it:'specie',es:'especies',pt:'espécies'},
 big:{nl:'grote',en:'big',fr:'grands',de:'groß',it:'grandi',es:'grandes',pt:'grandes'},
 small:{nl:'kleine',en:'small',fr:'petits',de:'klein',it:'piccoli',es:'pequeños',pt:'pequenos'},
 tldr:{nl:'De belangrijkste feiten op een rij',en:'The key facts at a glance',fr:'L’essentiel en bref',de:'Das Wichtigste auf einen Blick',it:'I fatti principali in breve',es:'Lo esencial de un vistazo',pt:'O essencial num relance'},
 actueel:{nl:'Geboortes, verhuizingen en nieuws',en:'Births, moves and news',fr:'Naissances, transferts et actualités',de:'Geburten, Umzüge und Neuigkeiten',it:'Nascite, trasferimenti e novità',es:'Nacimientos, traslados y noticias',pt:'Nascimentos, transferências e novidades'},
 kleur:{nl:'Zwarte panters, witte tijgers en kruisingen',en:'Black panthers, white tigers and hybrids',fr:'Panthères noires, tigres blancs et hybrides',de:'Schwarze Panther, weiße Tiger und Hybriden',it:'Pantere nere, tigri bianche e ibridi',es:'Panteras negras, tigres blancos e híbridos',pt:'Panteras negras, tigres brancos e híbridos'},
 route:{nl:'Zo zie je de meeste soorten',en:'How to see the most species',fr:'Comment voir le plus d’espèces',de:'So siehst du die meisten Arten',it:'Come vedere più specie',es:'Cómo ver más especies',pt:'Como ver mais espécies'},
 routeg:{nl:'{N} soorten in {P} parken',en:'{N} species in {P} parks',fr:'{N} espèces dans {P} parcs',de:'{N} Arten in {P} Parks',it:'{N} specie in {P} parchi',es:'{N} especies en {P} parques',pt:'{N} espécies em {P} parques'},
 tabel:{nl:'Alle vermeldingen per soort en locatie',en:'All entries by species and location',fr:'Toutes les mentions par espèce et lieu',de:'Alle Einträge nach Art und Ort',it:'Tutte le segnalazioni per specie e luogo',es:'Todas las menciones por especie y lugar',pt:'Todas as menções por espécie e local'},
 tabelg:{nl:'{V} vermeldingen',en:'{V} entries',fr:'{V} mentions',de:'{V} Einträge',it:'{V} segnalazioni',es:'{V} menciones',pt:'{V} menções'},
 uitleg:{nl:'Hoe deze gids is gemaakt',en:'How this guide was made',fr:'Comment ce guide a été réalisé',de:'Wie dieser Guide entstanden ist',it:'Come è stata realizzata questa guida',es:'Cómo se hizo esta guía',pt:'Como este guia foi feito'},
 uitlegg:{nl:'Bronnen: parken, ZooTrack en Zootierliste',en:'Sources: parks, ZooTrack and Zootierliste',fr:'Sources : parcs, ZooTrack et Zootierliste',de:'Quellen: Parks, ZooTrack und Zootierliste',it:'Fonti: parchi, ZooTrack e Zootierliste',es:'Fuentes: parques, ZooTrack y Zootierliste',pt:'Fontes: parques, ZooTrack e Zootierliste'},
 rapporteer:{nl:'Iets gezien of klopt er iets niet?',en:'Seen something or spotted a mistake?',fr:'Vu quelque chose ou une erreur ?',de:'Etwas gesehen oder einen Fehler entdeckt?',it:'Visto qualcosa o un errore?',es:'¿Has visto algo o hay un error?',pt:'Viste algo ou há um erro?'},
 rapporteerg:{nl:'Meldingen worden eerst gecontroleerd',en:'Reports are checked first',fr:'Les signalements sont d’abord vérifiés',de:'Meldungen werden zuerst geprüft',it:'Le segnalazioni vengono prima verificate',es:'Los avisos se revisan primero',pt:'Os avisos são verificados primeiro'}};
var MV={'Dierentuin':{nl:'dierentuinen',en:'zoos',fr:'zoos',de:'Zoos',it:'zoo',es:'zoos',pt:'zoos'},
 'Dierenpark':{nl:'dierenparken',en:'animal parks',fr:'parcs animaliers',de:'Tierparks',it:'parchi faunistici',es:'parques de animales',pt:'parques de animais'},
 'Safaripark':{nl:'safariparken',en:'safari parks',fr:'parcs safari',de:'Safariparks',it:'safari park',es:'safaris',pt:'safaris'},
 'Attractiepark met dieren':{nl:'attractieparken',en:'theme parks',fr:"parcs d'attractions",de:'Freizeitparks',it:'parchi a tema',es:'parques temáticos',pt:'parques temáticos'},
 'Opvang of sanctuary':{nl:'opvangcentra',en:'sanctuaries',fr:'refuges',de:'Auffangstationen',it:'centri di recupero',es:'santuarios',pt:'santuários'}};
var langs=[].map.call(document.querySelectorAll('[data-setlang]'),function(b){return b.dataset.setlang});if(!langs.length)langs=['nl'];
langs=langs.filter(function(l,i){return langs.indexOf(l)==i});
function esc(t){return String(t).replace(/[<&>]/g,'');}
var t=sb.querySelector('.nw-stitle');
if(vlag&&t&&!sb.querySelector('.jg-vlag')){var v=vlag.cloneNode(true);v.classList.add('jg-vlag');sb.insertBefore(v,t);}
var p=sb.querySelector('.jg-sub');if(!p){p=document.createElement('p');p.className='jg-sub';sb.appendChild(p);}
var g=sb.querySelector('.jg-meta');if(!g){g=document.createElement('div');g.className='jg-meta';sb.appendChild(g);}
function per(f){return langs.map(function(l){return '<span class="l-'+l+'">'+f(l)+'</span>'}).join('');}
function num(e){return e?+(e.textContent.replace(/\D/g,'')||0):0}
function bouw(){var S='<i> · </i>';
 var tot=num(document.querySelector('#lt-bar .hs-alle .n'));
 var ch=[].slice.call(document.querySelectorAll('#lt-bar .lt-chip:not(.hs-alle)')).filter(function(b){return num(b.querySelector('.n'))>0}).sort(function(a,b){return num(b.querySelector('.n'))-num(a.querySelector('.n'))}).slice(0,2);
 var tot2=num(document.querySelector('.nt-av.nt-all'));
 var bg=document.querySelectorAll('#soorten .chips[data-group="big"] .chip').length,sm=document.querySelectorAll('#soorten .chips[data-group="small"] .chip').length;
 var sub='<span data-tab="locaties">'+per(function(l){return esc(T.loc[l]||T.loc.en)})+'</span>'
  +'<span data-tab="soorten">'+per(function(l){return esc(T.sp[l]||T.sp.en)})+'</span>'
  +'<span data-tab="meer">'+per(function(l){return esc(T.meer[l]||T.meer.en)})+'</span>'
  +'<span data-tab="anders">'+(ond?ond.innerHTML:'')+'</span>';
 var mt='<span data-tab="locaties">'+per(function(l){return esc(tot+' '+(T.locw[l]||T.locw.en))+ch.map(function(b){var n=num(b.querySelector('.n')),w=MV[b.dataset.t];var lab=w?(w[l]||w.en):b.textContent.replace(/\d+/g,'').trim().toLowerCase();return S+esc(n+' '+lab)}).join('')})+'</span>'
  +'<span data-tab="soorten">'+per(function(l){return esc(tot2+' '+(T.spw[l]||T.spw.en))+S+esc(bg+' '+(T.big[l]||T.big.en))+S+esc(sm+' '+(T.small[l]||T.small.en))})+'</span>'
  +'<span data-tab="meer">'+(datum?datum.innerHTML:'')+'</span>'
  +'<span data-tab="anders">'+(meta?meta.innerHTML:'')+'</span>';
 function tx(k){return per(function(l){return esc(T[k][l]||T[k].en)})}
 var rp=document.getElementById('rt-preset'),P=rp?+((rp.textContent.match(/\d+/)||[0])[0]):0;
 var cnt=document.getElementById('count'),V=cnt?(cnt.textContent.match(/\d+/g)||[]).pop():'';
 var dt=datum?datum.innerHTML:'';
 sub+='<span data-tab="tldr">'+tx('tldr')+'</span><span data-tab="actueel">'+tx('actueel')+'</span><span data-tab="kleur">'+tx('kleur')+'</span><span data-tab="route">'+tx('route')+'</span><span data-tab="tabel">'+tx('tabel')+'</span><span data-tab="uitleg">'+tx('uitleg')+'</span><span data-tab="rapporteer">'+tx('rapporteer')+'</span>';
 mt+='<span data-tab="tldr">'+(meta?meta.innerHTML:'')+'</span><span data-tab="actueel">'+dt+'</span><span data-tab="kleur">'+dt+'</span>'
  +'<span data-tab="route">'+(P?per(function(l){return esc((T.routeg[l]||T.routeg.en).replace('{N}',tot2).replace('{P}',P))}):dt)+'</span>'
  +'<span data-tab="tabel">'+(V?per(function(l){return esc((T.tabelg[l]||T.tabelg.en).replace('{V}',V))}):dt)+'</span>'
  +'<span data-tab="uitleg">'+tx('uitlegg')+'</span><span data-tab="rapporteer">'+tx('rapporteerg')+'</span>';
 if(p.innerHTML!==sub)p.innerHTML=sub; if(g.innerHTML!==mt)g.innerHTML=mt;}
bouw();setTimeout(bouw,400);setTimeout(bouw,1500);
var ob=sb.querySelector('.nw-back');
if(ob&&!document.querySelector('.jg-terug')){var tb=document.createElement('button');tb.type='button';tb.className='jg-terug';
 tb.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg>'+per(function(l){var x=ob.querySelector('.l-'+l);return '<span class="jg-vh">'+esc(x?x.textContent:'Terug')+'</span>'});
 tb.addEventListener('click',function(){if(window.jgTerug&&window.jgTerug())return;ob.click()});document.body.appendChild(tb);}
function fit(){if(!t)return;t.style.removeProperty('--jg-fs');var fs=parseFloat(getComputedStyle(t).fontSize),n=0;while(t.scrollWidth>t.clientWidth+1&&fs>20&&n<30){fs-=1;n++;t.style.setProperty('--jg-fs',fs+'px');}}
function later(){requestAnimationFrame(fit)}
document.addEventListener('click',later);window.addEventListener('hashchange',later);window.addEventListener('resize',later);later();setTimeout(fit,400);
})();"""

# soort- en parkpagina's binnen een land: één groene kop, foto eronder, hartje op de foto, zwevende terugknop (19-10-2026)
DETAIL_JS = r"""(function(){
var LW={nl:'locaties',en:'locations',fr:'lieux',de:'Orte',it:'luoghi',es:'lugares',pt:'locais'},IN={nl:'in',en:'in',fr:'en',de:'in',it:'in',es:'en',pt:'em'};
function langs(){var a=[].map.call(document.querySelectorAll('[data-setlang]'),function(b){return b.dataset.setlang});if(!a.length)a=[document.documentElement.lang||'nl'];return a.filter(function(l,i){return a.indexOf(l)==i});}
function esc(t){return String(t).replace(/[<&>]/g,'');}
function tekst(el,l){if(!el)return '';var x=el.querySelector('.l-'+l);return (x||el).textContent.trim();}
window.jgTerug=function(){var h=location.hash;var m=/^#(soort|locatie)\//.exec(h);if(m&&document.querySelector('#info .jg-dkop')){var a=document.querySelector('.nw-bar a[data-nw="'+(m[1]=='soort'?'soorten':'locaties')+'"]')||document.querySelector('.nw-bar a[href="#'+(m[1]=='soort'?'soorten':'locaties')+'"]');if(a){a.click();return true;}history.back();return true;}
 var lb=document.querySelector('.nw-sbar.nw-los .nw-back');if(lb){lb.click();return true;}return false;};
function knop(){if(document.querySelector('.jg-terug'))return;var tb=document.createElement('button');tb.type='button';tb.className='jg-terug';tb.setAttribute('aria-label','Terug');
 tb.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg>';
 tb.addEventListener('click',function(){window.jgTerug()});document.body.appendChild(tb);}
function maak(){var info=document.getElementById('info');if(!info)return;var hd=info.querySelector('.ip-head');if(!hd||hd.dataset.jg)return;hd.dataset.jg='1';
 var oud=info.querySelector('.jg-dkop');if(oud)oud.remove();
 var L=langs(),h1=hd.querySelector('h1'),sci=hd.querySelector('.ip-sci'),alt=hd.querySelector('.ip-alt'),tags=[].slice.call(hd.querySelectorAll('.ip-tag'));
 var kop=document.createElement('div');kop.className='nw-sbar jg-dkop';
 var nk=document.querySelector('.nt-kop h1');var v=nk&&nk.querySelector('svg');var J=window.__JGLOS;if(v){var c=v.cloneNode(true);c.classList.add('jg-vlag');kop.appendChild(c);}else if(J&&J.vlag){kop.insertAdjacentHTML('beforeend',J.vlag);}
 var t=document.createElement('h2');t.className='nw-stitle';t.innerHTML=h1?h1.innerHTML:'';kop.appendChild(t);
 var sub=document.createElement('p');sub.className='jg-sub';var meta=document.createElement('div');meta.className='jg-meta';
 var land=nk&&(nk.querySelector('.hs-t')||nk);
 if(sci){sub.innerHTML='<i>'+sci.innerHTML+'</i>';
  var sec=[].filter.call(info.querySelectorAll('.ip-sec'),function(s){return s.querySelector('a[href*="locatie"]')})[0];
  var n=0;if(sec){var seen={};[].forEach.call(sec.querySelectorAll('a[href*="locatie"]'),function(a){var k=a.getAttribute('href');if(!seen[k]){seen[k]=1;n++;}});}
  var grp=hd.querySelector('.ip-tag.dark');
  meta.innerHTML=L.map(function(l){var g=tekst(grp,l),m2=/\(([^)]+)\)/.exec(g);g=m2?m2[1]:g;var ln=land?tekst(land,l):(J&&J.land||'');
   return '<span class="l-'+l+'">'+esc(n+' '+(LW[l]||LW.en)+(ln?' '+(IN[l]||'in')+' '+ln:''))+(g?'<i> · </i>'+esc(g):'')+'</span>'}).join('');}
 else{sub.innerHTML=tags.slice(1,2).concat(tags.slice(0,1)).map(function(x){return x.innerHTML}).join('<i> · </i>');
  meta.innerHTML=(alt?alt.innerHTML:'')+tags.slice(2).map(function(x){return '<i> · </i>'+x.innerHTML}).join('');}
 kop.appendChild(sub);kop.appendChild(meta);info.insertBefore(kop,hd);
 if(J&&h1&&!hd.querySelector('.nw-hwrap'))hart(hd,h1,sci,tags,J);
 hd.classList.add('jg-klaar');knop();
 requestAnimationFrame(function(){var fs=parseFloat(getComputedStyle(t).fontSize),i=0;while(t.scrollWidth>t.clientWidth+1&&fs>20&&i<30){fs--;i++;t.style.setProperty('--jg-fs',fs+'px');}});}
// losse park- en soortpagina's: hartje op de foto, zelfde favorieten ("nt-fav") als de gids (19-10-2026)
function hart(hd,h1,sci,tags,J){var FK='nt-fav',s=J.s,k=J.k,c=J.c;
 function lees(){var a=null;try{a=JSON.parse(localStorage.getItem(FK)||'null');}catch(e){}return Array.isArray(a)?a:[];}
 function heeft(){return lees().some(function(x){return x.k===k&&x.c===c&&x.s===s;});}
 var w=document.createElement('button');w.type='button';w.className='nw-hwrap';
 function teken(){var on=heeft();w.setAttribute('aria-pressed',String(on));w.setAttribute('aria-label',on?'In je favorieten':'Bewaar als favoriet');
  w.innerHTML='<span class="nw-heart" aria-pressed="'+on+'"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-8-5-8-11a4.5 4.5 0 0 1 8-2.5A4.5 4.5 0 0 1 20 9c0 6-8 11-8 11z"></path></svg></span><span class="l-nl">'+(on?'In je favorieten':'Bewaar als favoriet')+'</span>';}
 w.addEventListener('click',function(e){e.preventDefault();var a=lees(),i=-1;a.forEach(function(x,j){if(i<0&&x.k===k&&x.c===c&&x.s===s)i=j;});
  if(i>=0)a.splice(i,1);else{var it={k:k,c:c,s:s,n:h1.textContent.trim()};if(k==='sp'){if(sci)it.p=sci.textContent.trim();}else{var pl=tags.filter(function(x){return !x.classList.contains('dark')})[0];if(pl)it.p=pl.textContent.trim();}a.push(it);}
  try{localStorage.setItem(FK,JSON.stringify(a));}catch(e){}teken();});
 teken();h1.insertAdjacentElement('afterend',w);}
function plan(){setTimeout(maak,0);requestAnimationFrame(maak);}
maak();window.addEventListener('hashchange',plan);document.addEventListener('click',function(){setTimeout(maak,60)});
var info=document.getElementById('info');if(info&&window.MutationObserver){new MutationObserver(function(){var hd=info.querySelector('.ip-head');if(hd&&!hd.dataset.jg)maak();}).observe(info,{childList:true});}
})();"""

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Nunito:wght@400;600;700;800&display=swap">'

# kleuren
JG, SUN, BG, CARD, INK, MUTED, LINE = '#143A22', '#F2C14E', '#ECF2DF', '#FAFBF2', '#13301C', '#4C6450', '#CADBB9'
OLIVE, ACC, WOOD, WOOD_D = '#1F5A33', '#B8501C', '#DCAE76', '#9C6B36'
DISP = '"Anton","Impact","Arial Narrow",sans-serif'
BODY = '"Nunito",system-ui,-apple-system,sans-serif'


# knoppen (19-10-2026, stijl A "bladgroen"): effen lichte knop met donkergroene rand; gekozen = donkergroen met goudgele tekst (vervangt het hout)
KNOP = "background:#FAFBF2!important;color:#143A22!important;border:1.5px solid #1F5A33!important;border-radius:10px!important;box-shadow:0 2px 0 rgba(20,58,34,.16)!important;text-shadow:none!important;font-weight:800"
KNOP_AAN = "background:#143A22!important;color:#F2C14E!important;border-color:#143A22!important;box-shadow:0 2px 0 rgba(0,0,0,.22)!important;text-shadow:none!important"

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
html body .chip svg.flag,html body .chip svg:not(.ti){{box-shadow:none!important;border-radius:3px!important;overflow:hidden;filter:none!important}}
html body .chip svg.flag{{box-shadow:0 0 0 1px rgba(20,58,34,.22)!important}}
/* tussenschermen (19-10-2026): groene kop, menu-icoontjes, zoekveld, filterknoppen, soortkaartjes */
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
html body .lt-chip,html body .rg-chip{{{KNOP}}}
html body .lt-chip[aria-pressed="true"],html body .rg-chip[aria-pressed="true"]{{{KNOP_AAN}}}
html body .group-title .gtog,html body .group-title .gtog *{{font-family:{DISP}!important;font-weight:400!important;text-transform:uppercase;letter-spacing:.03em;color:{OLIVE}!important}}
html body .group-title .gtog{{display:inline-flex;align-items:center;gap:8px;font-size:1.15rem!important}}
html body .group-title .gtog::before{{content:"";flex:none;width:46px;height:20px;background:{paws('#C9561F')} center/contain no-repeat}}
html body .nt-sc img{{border-bottom:3px solid {SUN}}}
html body #main:has(#meer.nw-cur,#locaties.nw-cur,#soorten.nw-cur) .nw-sbar .nw-back,html body #meer .jg-kop .terug{{display:none!important}}
html body .nw-sbar:not(.nw-los){{position:relative!important;top:0!important;min-height:166px;box-sizing:border-box;display:flex!important;flex-wrap:wrap;align-content:flex-start;align-items:center;column-gap:12px;padding-top:20px!important}}
html body .nw-sbar .jg-sub{{flex-basis:100%;margin:8px 0 0;color:#D3E4C2;font-size:1.05rem;line-height:1.35}}
html body .nw-sbar .nw-stitle{{font-size:clamp(2.2rem,10vw,3.2rem)!important}}
html body .nw-sbar .nw-stitle,html body .nw-sbar .nw-stitle *{{font-size:var(--jg-fs,clamp(2.2rem,10vw,3.2rem))!important}}
html body .jg-kop:not(.jg-foto){{min-height:166px;box-sizing:border-box;padding-top:20px}}
html body .jg-kop:not(.jg-foto) h1{{font-size:clamp(2.2rem,10vw,3.2rem)!important;margin:0!important}}
html body .jg-kop .terug{{margin:0 0 10px!important}}
html body .jg-uitleg{{margin:0 0 16px!important;color:{MUTED}!important}}
html body .nw-sbar::before,html body .jg-kop::before{{right:-30px!important;top:-12px!important;width:130px!important;height:160px!important}}
html body .nw-sbar .nw-stitle{{display:flex!important;align-items:center;gap:12px}}
html body .nw-sbar .jg-vlag{{display:block!important;flex:none;width:44px;height:30px;border-radius:4px;box-shadow:0 0 0 1px rgba(0,0,0,.25)}}
html body .nw-sbar .jg-meta{{flex-basis:100%;margin-top:10px;font-family:"Barlow Condensed","Arial Narrow",sans-serif;font-weight:600;font-size:.95rem;letter-spacing:.08em;text-transform:uppercase;color:{SUN}}}
html body .nw-sbar .jg-meta *{{color:{SUN}!important;text-decoration:none!important;font-family:inherit!important}}
html body .nw-sbar .jg-meta,html body .nw-sbar .jg-meta *{{font-size:.95rem!important;line-height:1.5!important;border:0!important;padding:0!important;margin:0!important;background:none!important;font-weight:600!important;letter-spacing:.08em!important}}
html body .nw-sbar .jg-meta .nw-stats,html body .nw-sbar .jg-meta .nw-stats>a{{display:inline-flex!important;gap:0 18px}}
html body .nw-sbar .jg-meta .nw-stats{{margin-right:18px!important}}
html body .nw-sbar .jg-meta>div{{display:inline!important}}
html body .nw-sbar .jg-meta i{{font-style:normal}}
html body .nw-sbar .jg-sub{{margin-top:6px!important}}
/* vier koppen exact gelijk aan de landkop (19-10-2026) */
html body :is(#main,#info) .nw-sbar:not(.nw-los){{height:auto!important;min-height:0!important;padding:21px 20px 44px!important;display:block!important;overflow:hidden}}
html body :is(#main,#info) .nw-sbar:not(.nw-los) .nw-back{{float:left;margin:2px 12px 0 0!important}}
html body :is(#main,#info) .nw-sbar .jg-vlag{{float:left;margin:6px 12px 0 0}}
html body :is(#main,#info) .nw-sbar .nw-stitle{{display:block!important;line-height:calc(clamp(2.2rem,10vw,3.2rem) * 1.1)!important;height:auto;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
html body :is(#main,#info) .nw-sbar .nw-stitle *{{line-height:inherit!important}}
html body :is(#main,#info) .nw-sbar .jg-sub{{clear:both;display:block;margin:4px 0 0!important;font-size:16.8px!important;line-height:26.88px!important;color:#D3E4C2!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
html body :is(#main,#info) .nw-sbar .jg-meta{{display:block!important;margin:10px 0 0!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
html body :is(#main,#info) .nw-sbar .jg-meta,html body :is(#main,#info) .nw-sbar .jg-meta *{{font-size:13.76px!important;letter-spacing:.06em!important;line-height:17px!important}}
html body :is(#main,#info) .nw-sbar .jg-meta .nw-stats,html body :is(#main,#info) .nw-sbar .jg-meta .nw-stats>a{{display:inline-flex!important;gap:0 14px}}
html body :is(#main,#info) .nw-sbar .jg-meta .nw-stats{{margin-right:14px!important}}
html body :is(#main,#info) .nw-sbar .jg-meta .nw-stats strong{{font-size:13.76px!important}}
html body #main .nw-sbar [data-tab]{{display:none!important}}
html body #main:has(#locaties.nw-cur) .nw-sbar [data-tab="locaties"],html body #main:has(#soorten.nw-cur) .nw-sbar [data-tab="soorten"],html body #main:has(#meer.nw-cur) .nw-sbar [data-tab="meer"],html body #main:not(:has(#locaties.nw-cur,#soorten.nw-cur,#meer.nw-cur)) .nw-sbar [data-tab="anders"]{{display:block!important;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
html body #main .nw-sbar .jg-meta [data-tab] .nw-stats,html body #main .nw-sbar .jg-meta [data-tab] .nw-stats>a,html body #main .nw-sbar .jg-meta [data-tab] .nw-datum{{display:inline-flex!important}}
html body #main:has(#tldr.nw-cur) .nw-sbar [data-tab="tldr"],html body #main:has(#actueel.nw-cur) .nw-sbar [data-tab="actueel"],html body #main:has(#kleur.nw-cur) .nw-sbar [data-tab="kleur"],html body #main:has(#route.nw-cur) .nw-sbar [data-tab="route"],html body #main:has(#tabel.nw-cur) .nw-sbar [data-tab="tabel"],html body #main:has(#uitleg.nw-cur) .nw-sbar [data-tab="uitleg"],html body #main:has(#rapporteer.nw-cur) .nw-sbar [data-tab="rapporteer"]{{display:block!important;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
html body #main:has(#locaties.nw-cur,#soorten.nw-cur,#meer.nw-cur,#tldr.nw-cur,#actueel.nw-cur,#kleur.nw-cur,#route.nw-cur,#tabel.nw-cur,#uitleg.nw-cur,#rapporteer.nw-cur) .nw-sbar [data-tab="anders"]{{display:none!important}}
html body .nw-sbar:not(.nw-los) .nw-back{{display:none!important}}
html body .jg-terug{{display:none;position:fixed;z-index:75;left:max(16px,env(safe-area-inset-left,0px));bottom:calc(76px + env(safe-area-inset-bottom,0px));width:52px;height:52px;border-radius:50%;border:2px solid {JG};background:{SUN};color:{JG};box-shadow:0 6px 16px -6px rgba(10,36,20,.6);cursor:pointer;padding:0;align-items:center;justify-content:center}}
html body .jg-terug svg{{width:26px;height:26px}}
html body .jg-terug .jg-vh{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}
html body:has(#main :is(#tldr.nw-cur,#actueel.nw-cur,#kleur.nw-cur,#route.nw-cur,#tabel.nw-cur,#uitleg.nw-cur,#rapporteer.nw-cur)) .jg-terug{{display:flex}}
html body .jg-terug:focus-visible{{outline:3px solid {JG};outline-offset:3px}}
/* detailpagina's soort/park binnen een land */
html body #info:has(.jg-dkop)>.nw-sbar:not(.jg-dkop),html body:has(#info .jg-dkop) .nw-sbar.nw-los{{display:none!important}}
html body #info .ip-head.jg-klaar{{background:none!important;margin:0!important;padding:4px 0 0!important;position:relative;overflow:visible;border:0!important}}
html body #info .ip-head.jg-klaar::before,html body #info .ip-head.jg-klaar::after{{display:none!important}}
html body #info .ip-head.jg-klaar>.ip-tags,html body #info .ip-head.jg-klaar>h1,html body #info .ip-head.jg-klaar>.ip-sci,html body #info .ip-head.jg-klaar>.ip-alt{{display:none!important}}
html body #info .ip-head.jg-klaar .ip-photo{{box-shadow:none;border-radius:18px;margin-top:0}}
html body #info .ip-head.jg-klaar .ip-photo img{{border-radius:18px;display:block}}
html body #info .ip-head.jg-klaar .ip-cap,html body #info .ip-head.jg-klaar .ip-cap *{{color:{MUTED}!important}}
html body #info .ip-head.jg-klaar:has(.ip-photo) .nw-hwrap{{position:absolute;top:16px;right:12px;z-index:3;width:46px;height:46px;padding:0!important;border-radius:50%!important;background:#FFFFFF!important;border:0!important;box-shadow:0 4px 12px -4px rgba(0,0,0,.45);display:flex!important;align-items:center;justify-content:center;font-size:0!important}}
html body #info .ip-head.jg-klaar .nw-hwrap>span:not(.nw-heart){{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}
html body #info .ip-head.jg-klaar:not(:has(.ip-photo)) .nw-hwrap{{margin:0 0 0 auto}}
html body #info .jg-dkop .jg-sub i{{font-style:italic}}
html body #info .jg-dkop .jg-meta i,html body #info .jg-dkop .jg-sub>i:not(:first-child){{font-style:normal}}
html body:has(#info .jg-dkop) .jg-terug{{display:flex}}
html body .ip-sec ul.ip-where>li{{position:relative;padding-left:20px!important}}
html body .ip-sec ul.ip-where>li::before{{content:"•";position:absolute;left:2px;top:var(--jg-bt,15px);font-size:1.4rem;line-height:1;color:{ACC}}}
html body .nt-loc:not(.nt-kj)>.nt-ti,html body .nt-loc:not(.nt-kj)>.nt-n{{align-self:center!important;margin-top:0!important;margin-bottom:0!important}}
/* scherm Locaties: losse kaartjes met goudgele badge en soortrondjes (19-10-2026) */
html body .nt-full .nt-kj{{background:{CARD}!important;border:1px solid {LINE}!important;border-radius:16px!important;box-shadow:0 2px 0 rgba(20,58,34,.08),0 8px 18px -12px rgba(20,58,34,.35)!important}}
html body .nt-kj .nt-lt a{{font-weight:800;color:{INK}}}
html body .nt-kj .nt-bdg{{background:{SUN}!important;color:{JG}!important;font-family:{DISP}!important;font-weight:400!important;font-size:1.25rem!important;box-shadow:0 0 0 2px {JG}}}
html body .nt-rj{{border:2px solid #FFFFFF!important;box-shadow:0 0 0 1px {LINE}}}
html body .nt-rj.nt-rju{{border:2px dashed {MUTED}!important;box-shadow:none}}
html body .nt-rj.nt-rjm{{background:#D4E6BF!important;color:{JG}!important}}
html body #info[hidden] .jg-dkop{{display:none!important}}
html body .jg-terug{{display:none!important}}
html body:has(#main :is(#tldr.nw-cur,#actueel.nw-cur,#kleur.nw-cur,#route.nw-cur,#tabel.nw-cur,#uitleg.nw-cur,#rapporteer.nw-cur)) .jg-terug,html body:has(#info:not([hidden]) .jg-dkop) .jg-terug{{display:flex!important}}
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
html body .chip{{{KNOP}}}
html body .chip[aria-pressed="true"]{{{KNOP_AAN}}}
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
/* startscherm landpagina's exact gelijk aan de koppen van Locaties, Soorten en Meer (19-10-2026): bovenkant, vlag, letterafstand titel, golf */
html body .nt-kop{{margin-top:-1px!important;padding-top:21px!important}}
html body .nt-kop h1.mast.hs-kop>svg{{align-self:flex-start!important;margin-top:6px!important}}
html body .nt-kop h1.mast.hs-kop .hs-t,html body .nt-kop h1.mast.hs-kop .hs-t *{{letter-spacing:.03em!important}}
html body .nt-kop::after{{height:24px!important}}
html body .nt-lbl{{font-family:{DISP};font-size:1.1rem;letter-spacing:.04em;color:{OLIVE}!important;text-transform:uppercase;display:flex;align-items:center;gap:8px;margin-top:14px}}
html body .nt-lbl::before{{content:"";flex:none;width:46px;height:20px;background:{paws('#C9561F')} center/contain no-repeat}}
html body .nt-av{{border:3px solid {SUN}!important;box-shadow:0 2px 0 {WOOD_D}!important}}
html body .nt-cat[aria-pressed="true"]{{background:#D4E6BF!important}}
html body .nt-cat[aria-pressed="true"] .nt-av{{border-color:{JG}!important;box-shadow:0 0 0 3px {SUN}!important}}
html body .nt-av.nt-all{{background:{JG}!important;color:{SUN}!important}}
html body #nt-kaart{{border-radius:18px;overflow:hidden;box-shadow:0 0 0 4px {JG},0 10px 24px -12px rgba(20,58,34,.5)}}
html body .chip,html body .nt-types button{{{KNOP}}}
html body .chip[aria-pressed="true"],html body .nt-types button[aria-pressed="true"]{{{KNOP_AAN}}}
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

# voet als horizontale tak (VOORBEELD 19-10-2026, nog niet op de site): de luipaard ligt op een getekende tak,
# de Ko-fi-tekst staat op de tak. De tak wordt in JS op de echte maat getekend (niet uitgerekt) en opnieuw
# getekend als de voet van maat verandert (ResizeObserver op de voet; de tak zelf staat absoluut en verandert de maat niet).
TAK_CSS = f"""
html body .hs-foot.jg-tak{{background:transparent!important;border-top:0!important;margin-top:112px!important;padding:0 0 12px!important;position:relative;isolation:isolate}}
html body .hs-foot.jg-tak .jg-takbg{{position:absolute;left:0;right:0;top:0;bottom:12px;z-index:0;pointer-events:none;overflow:visible}}
html body .hs-foot.jg-tak .jg-takbg svg{{display:block;width:100%;height:100%;overflow:visible}}
html body .hs-foot.jg-tak .hs-wrap{{position:relative;z-index:1;padding-top:50px!important;padding-bottom:40px!important}}
html body .hs-foot.jg-tak .jg-lp{{z-index:3;top:-94px}}
html body .hs-foot.jg-tak .hs-kofibar{{background:none!important;border:0!important;padding:0!important;margin:0 0 14px!important;box-shadow:none!important}}
html body .hs-foot.jg-tak p,html body .hs-foot.jg-tak p *{{color:#FFF4DE!important}}
html body .hs-foot.jg-tak .hs-kofibar p{{font-size:1.05rem;line-height:1.5;text-shadow:0 1px 0 rgba(40,20,5,.45)}}
html body .hs-foot.jg-tak .hs-kofibar b,html body .hs-foot.jg-tak .hs-kofibar b *{{color:{SUN}!important}}
html body .hs-foot.jg-tak .hs-kofi{{box-shadow:0 2px 0 {LO},0 6px 14px -6px rgba(0,0,0,.6)!important;border:2px solid {LO}!important}}
html body .hs-foot.jg-tak .hs-wrap>p{{border-top:1px dashed rgba(255,236,200,.35)!important;padding-top:12px!important;margin-top:16px!important;font-size:.92rem;opacity:.9}}
"""

TAK_JS = r"""(function(){
var f=document.querySelector('footer.hs-foot');if(!f||f.querySelector('.jg-takbg'))return;f.classList.add('jg-tak');
var bg=document.createElement('div');bg.className='jg-takbg';bg.setAttribute('aria-hidden','true');f.insertBefore(bg,f.firstChild);
var LO='#3B2414',W0=0,H0=0;
function rnd(z){var s=z;return function(){s=(s*9301+49297)%233280;return s/233280;};}
function teken(){var w=Math.round(f.clientWidth),h=Math.round(bg.clientHeight);if(!w||!h||(w===W0&&h===H0))return;W0=w;H0=h;
 var r=rnd(7),T=6,B=h-4,o='';
 function rand(y0,a,p,f2){var d='';for(var x=-20;x<=w+20;x+=10){var y=y0+a*Math.sin(x/p+f2)+a*.45*Math.sin(x/(p*.37)+f2*2);d+=(x<=-20?'M':'L')+x+' '+y.toFixed(1)+' ';}return d;}
 var top=rand(T+6,3,90,.4),bot=rand(B-6,4,70,1.3);
 var lijf=top+'L'+(w+20)+' '+(B+10)+' '+bot.replace(/^M/,'L').split(' L').reverse().join(' L').replace(/^L?/,'L')+' L-20 '+(T)+' Z';
 /* onderrand omkeren voor een gesloten vorm */
 var pb=[];for(var x=w+20;x>=-20;x-=10){pb.push(x+' '+(B-6+4*Math.sin(x/70+1.3)+1.8*Math.sin(x/25.9+2.6)).toFixed(1));}
 var pt=[];for(var x2=-20;x2<=w+20;x2+=10){pt.push(x2+' '+(T+6+3*Math.sin(x2/90+.4)+1.35*Math.sin(x2/33.3+.8)).toFixed(1));}
 lijf='M'+pt.join(' L')+' L'+pb.join(' L')+' Z';
 o+='<defs><linearGradient id="jgtk-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A2703F"/><stop offset=".09" stop-color="#8A5C33"/><stop offset=".22" stop-color="#734A29"/><stop offset=".8" stop-color="#6A4325"/><stop offset="1" stop-color="#4E301A"/></linearGradient>'
  +'<clipPath id="jgtk-c"><path d="'+lijf+'"/></clipPath></defs>';
 /* takje met bladeren rechts boven de tak */
 var tx=w-70;o+='<g><path d="M'+tx+' '+(T+12)+' C'+(tx+6)+' '+(T-14)+' '+(tx+20)+' '+(T-30)+' '+(tx+34)+' '+(T-44)+'" stroke="'+LO+'" stroke-width="9" fill="none" stroke-linecap="round"/>'
  +'<path d="M'+tx+' '+(T+12)+' C'+(tx+6)+' '+(T-14)+' '+(tx+20)+' '+(T-30)+' '+(tx+34)+' '+(T-44)+'" stroke="#7A4F2C" stroke-width="5" fill="none" stroke-linecap="round"/>';
 function blad(x,y,a,s){return '<g transform="translate('+x+' '+y+') rotate('+a+') scale('+s+')"><path d="M0 0 C8 -10 26 -12 38 0 C26 12 8 10 0 0 Z" fill="#2F7A3B" stroke="#143A22" stroke-width="2" stroke-linejoin="round"/><path d="M2 0 L34 0" stroke="#1D5527" stroke-width="1.6" stroke-linecap="round"/></g>';}
 o+=blad(tx+33,T-44,-40,1)+blad(tx+22,T-30,-150,.85)+blad(tx+14,T-14,-20,.8)+'</g>';
 /* lijf van de tak */
 o+='<path d="'+lijf+'" fill="url(#jgtk-g)"/>';
 o+='<g clip-path="url(#jgtk-c)">';
 /* bastlijnen alleen langs de randen; het midden blijft glad voor de tekst */
 for(var i=0;i<Math.ceil(w/26);i++){var x0=r()*w,l=40+r()*110,y=T+12+r()*12,b2=(r()-.5)*3;
  o+='<path d="M'+x0.toFixed(0)+' '+y.toFixed(1)+' q'+(l/2).toFixed(0)+' '+b2.toFixed(1)+' '+l.toFixed(0)+' '+(b2*.4).toFixed(1)+'" stroke="#4A2D17" stroke-opacity=".55" stroke-width="'+(1.4+r()*1.4).toFixed(1)+'" fill="none" stroke-linecap="round"/>';}
 for(var j=0;j<Math.ceil(w/22);j++){var x1=r()*w,l2=40+r()*120,y2=B-14-r()*16,b3=(r()-.5)*3;
  o+='<path d="M'+x1.toFixed(0)+' '+y2.toFixed(1)+' q'+(l2/2).toFixed(0)+' '+b3.toFixed(1)+' '+l2.toFixed(0)+' '+(b3*.4).toFixed(1)+'" stroke="#3E2512" stroke-opacity=".6" stroke-width="'+(1.6+r()*1.6).toFixed(1)+'" fill="none" stroke-linecap="round"/>';}
 /* lichte glans langs de bovenrand */
 o+='<path d="M-20 '+(T+11)+' L'+(w+20)+' '+(T+11)+'" stroke="#C08B52" stroke-opacity=".45" stroke-width="2" stroke-dasharray="60 26 18 30"/>';
 /* twee knoesten aan de randen */
 function knoest(x,y,s){return '<g transform="translate('+x+' '+y+') scale('+s+')"><ellipse rx="15" ry="6.5" fill="#4E301A"/><ellipse rx="10" ry="4" fill="none" stroke="#2E1A0C" stroke-width="2"/><ellipse rx="4.5" ry="1.8" fill="#2E1A0C"/></g>';}
 o+=knoest(Math.min(w-40,w*.78),B-16,1)+knoest(Math.max(40,w*.16),B-20,.75);
 o+='</g>';
 /* omlijning boven en onder (zelfde lijn als de luipaard) */
 o+='<path d="M'+pt.join(' L')+'" stroke="'+LO+'" stroke-width="3" fill="none" stroke-linejoin="round"/><path d="M'+pb.join(' L')+'" stroke="'+LO+'" stroke-width="3" fill="none" stroke-linejoin="round"/>';
 bg.innerHTML='<svg viewBox="0 0 '+w+' '+h+'" xmlns="http://www.w3.org/2000/svg">'+o+'</svg>';
 /* luipaard precies op de tak: buik (y=96 van 132 in zijn tekening) op het laagste punt van de bovenrand onder het lijf, zodat er nergens ruimte tussen zit */
 var lp=f.querySelector('.jg-lp');if(lp){var sc=lp.clientWidth/240,x0=lp.offsetLeft+60*sc,x1=lp.offsetLeft+216*sc,m=-1e9;
  for(var xx=Math.floor(x0/10)*10;xx<=x1+10;xx+=10){var yy=T+6+3*Math.sin(xx/90+.4)+1.35*Math.sin(xx/33.3+.8);if(yy>m)m=yy;}
  lp.style.top=(m+1-96*sc).toFixed(1)+'px';}}
teken();
if(window.ResizeObserver)new ResizeObserver(function(){teken();}).observe(f);else window.addEventListener('resize',teken);
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(teken);
})();"""


def voorbeeld_tak(bron='nederland'):
    """Testpagina /voorbeeld-jungle/tak/: de gids van <bron> met de voet als tak (noindex, niet gelinkt)."""
    s = open(os.path.join(ROOT, bron, 'index.html'), encoding='utf-8').read()
    s = re.sub(r'<meta name="robots"[^>]*>', '', s)
    s = s.replace('<head>', '<head><meta name="robots" content="noindex">', 1)
    s = re.sub(r'<link rel="canonical"[^>]*>', '', s)
    blk = f'<!--tak--><style id="jungle-tak">{TAK_CSS}</style><script>{TAK_JS}</script><!--/tak-->'
    i = s.rfind('</body>')
    s = s[:i] + blk + s[i:]
    d = os.path.join(ROOT, 'voorbeeld-jungle', 'tak')
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(s)
    print('voorbeeld tak:', os.path.relpath(d, ROOT))


# losse park- en soortpagina's (/<land>/locatie/…, /<land>/soort/…): vlag, landnaam en sleutel voor het hartje (19-10-2026)
CODE = {"nederland": "nl", "belgie": "be", "luxemburg": "lu", "duitsland": "de", "frankrijk": "fr", "oostenrijk": "at",
        "zwitserland": "ch", "verenigd-koninkrijk": "uk", "italie": "it", "spanje": "es", "ierland": "ie", "portugal": "pt"}
_START = None
def _start():
    global _START
    if _START is None:
        t = open(os.path.join(ROOT, 'bron', 'start.html'), encoding='utf-8').read()
        vl = dict(re.findall(r"^\s*([a-z]{2}):'(<svg[^']*</svg>)',?$", t, re.M))
        nm = dict(re.findall(r'^\s*([a-z]{2}):\{nl:"([^"]+)"', t, re.M))
        _START = (vl, nm)
    return _START

def los_js(pad):
    if not pad:
        return ''
    d = os.path.relpath(os.path.dirname(pad), ROOT).split(os.sep)
    if len(d) != 3 or d[0] not in CODE or d[1] not in ('locatie', 'soort'):
        return ''
    c = CODE[d[0]]
    vl, nm = _start()
    v = vl.get(c, '').replace('class="flag"', 'class="jg-vlag"')
    return 'window.__JGLOS=' + json.dumps({'c': c, 'k': 'loc' if d[1] == 'locatie' else 'sp', 's': d[2],
                                           'land': nm.get(c, ''), 'vlag': v}, ensure_ascii=False) + ';'

def blok(html, pad=None):
    land = 'id="hs-top"' in html or "id='hs-top'" in html
    css = GEDEELD + (LAND if land else EUROPA) + LP_CSS
    js = LP_JS % json.dumps(svg()) + "(function(){var ts=document.querySelectorAll('.terug');for(var i=0;i<ts.length;i++){var t=ts[i],p=t.parentElement;if(!p||p.classList.contains('jg-kop'))continue;var k=document.createElement('div');k.className='jg-kop';p.insertBefore(k,t);var x=t.nextElementSibling;k.appendChild(t);while(x&&(x.tagName=='H1'||(x.tagName=='P'&&x.classList.contains('sub'))||x.classList.contains('kat-h'))){var n=x.nextElementSibling;k.appendChild(x);x=n;}}})();" + KOP_JS + los_js(pad) + DETAIL_JS
    return f'{BEGIN}{FONTS}<style id="jungle">{css}</style><script>{js}</script>{EIND}'

def weg(html):
    return re.sub(re.escape(BEGIN) + r'.*?' + re.escape(EIND), '', html, flags=re.S)

def zet(html, pad=None):
    html = weg(html)
    b = blok(html, pad)
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
        t = weg(s) if verwijder else zet(s, p)
        if t != s:
            open(p, 'w', encoding='utf-8').write(t)
            n += 1
    print('jungle-stijl', 'weggehaald uit' if verwijder else 'gezet op', n, "pagina's")

if __name__ == '__main__':
    maak(verwijder='--weg' in sys.argv)
