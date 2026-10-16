# Huisstijl van de startpagina (stijl van de Spottersgids) voor de landengidsen op de website.
# bouw.py zet dit in elke gids, deelstaat- en regiopagina en in de losse soort- en locatiepagina's:
#   - dezelfde bovenbalk als de startpagina (pootje, zoeken, taal, menu); "← Alle landen" en "Steun de gids" bovenaan vervallen
#   - dezelfde kleuren en letters (Alegreya, Alegreya Sans, Barlow Condensed)
#   - een rustiger kop (kleine titelregel, kleinere foto)
#   - de inhoudsopgave van de gids als tabbladen die blijven staan
#   - Ko-fi onderaan zoals op de startpagina
# De gegevens en teksten van de gidsen zelf blijven onaangeroerd; de kaart in de gids houdt zijn eigen stijl.
import re

FONTS = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Alegreya:ital,wght@0,500;0,700;0,800;1,500&family=Alegreya+Sans:ital,wght@0,400;0,500;0,700;1,400&family=Barlow+Condensed:wght@500;600&display=swap" rel="stylesheet">')

def lettertypen(doc):
    """Bricolage/Literata vervangen door de letters van de startpagina (ook in tekst die het script van de gids later invoegt)."""
    doc = re.sub(r'<link href="https://fonts\.googleapis\.com/css2\?family=Bricolage[^"]*" rel="stylesheet">', lambda m: FONTS, doc)
    doc = doc.replace("Bricolage Grotesque", "Alegreya Sans")
    return re.sub(r"\bLiterata\b", "Alegreya Sans", doc)

L = {  # teksten in alle gidstalen
    "naam": {"nl": "Wilde katachtigen", "en": "Wild cats", "fr": "Félins sauvages", "de": "Wilde Katzen", "it": "Felini selvatici", "es": "Felinos salvajes", "pt": "Felinos selvagens"},
    "sub": {"nl": "in Europa", "en": "in Europe", "fr": "en Europe", "de": "in Europa", "it": "in Europa", "es": "en Europa", "pt": "na Europa"},
    "zoek": {"nl": "Zoeken", "en": "Search", "fr": "Chercher", "de": "Suchen", "it": "Cerca", "es": "Buscar", "pt": "Pesquisar"},
    "kaart": {"nl": "Kaart", "en": "Map", "fr": "Carte", "de": "Karte", "it": "Mappa", "es": "Mapa", "pt": "Mapa"},
    "landen": {"nl": "Alle landen", "en": "All countries", "fr": "Tous les pays", "de": "Alle Länder", "it": "Tutti i paesi", "es": "Todos los países", "pt": "Todos os países"},
    "soorten": {"nl": "Alle soorten", "en": "All species", "fr": "Toutes les espèces", "de": "Alle Arten", "it": "Tutte le specie", "es": "Todas las especies", "pt": "Todas as espécies"},
    "top10": {"nl": "Top 10 om te bezoeken", "en": "Top 10 to visit", "fr": "Top 10 à visiter", "de": "Top 10 zum Besuchen", "it": "Top 10 da visitare", "es": "Top 10 para visitar", "pt": "Top 10 a visitar"},
    "geboren": {"nl": "Recent geboren", "en": "Recently born", "fr": "Naissances récentes", "de": "Kürzlich geboren", "it": "Nati di recente", "es": "Nacimientos recientes", "pt": "Nascimentos recentes"},
    "perpark": {"nl": "Parken op aantal soorten", "en": "Parks by number of species", "fr": "Parcs par nombre d’espèces", "de": "Parks nach Zahl der Arten", "it": "Parchi per numero di specie", "es": "Parques por número de especies", "pt": "Parques por número de espécies"},
    "typen": {"nl": "Soorten locaties", "en": "Types of location", "fr": "Types de lieux", "de": "Arten von Orten", "it": "Tipi di luogo", "es": "Tipos de lugar", "pt": "Tipos de local"},
    "over": {"nl": "Over deze gids", "en": "About this guide", "fr": "À propos de ce guide", "de": "Über diesen Guide", "it": "Informazioni su questa guida", "es": "Sobre esta guía", "pt": "Sobre este guia"},
    "meer": {"nl": "Meer", "en": "More", "fr": "Plus", "de": "Mehr", "it": "Altro", "es": "Más", "pt": "Mais"},
    "spot": {"nl": "Spottersgids: katten in het wild", "en": "Spotter’s Guide: cats in the wild", "fr": "Spotter’s Guide : félins dans la nature (en anglais)", "de": "Spotter’s Guide: Katzen in freier Wildbahn (auf Englisch)", "it": "Spotter’s Guide: felini in natura (in inglese)", "es": "Spotter’s Guide: felinos en libertad (en inglés)", "pt": "Spotter’s Guide: felinos na natureza (em inglês)"},
    "kofi": {"nl": "Steun de gids op Ko-fi", "en": "Support the guide on Ko-fi", "fr": "Soutenir le guide sur Ko-fi", "de": "Den Guide auf Ko-fi unterstützen", "it": "Sostieni la guida su Ko-fi", "es": "Apoya la guía en Ko-fi", "pt": "Apoia o guia no Ko-fi"},
    "kofi_t": {"nl": "Vind je deze gids handig?", "en": "Find this guide useful?", "fr": "Ce guide vous est utile ?", "de": "Findest du diesen Guide nützlich?", "it": "Trovi utile questa guida?", "es": "¿Te resulta útil esta guía?", "pt": "Este guia é útil para ti?"},
    "kofi_s": {"nl": "Met een kleine bijdrage help je hem actueel te houden.", "en": "A small contribution helps keep it up to date.", "fr": "Une petite contribution aide à le tenir à jour.", "de": "Ein kleiner Beitrag hilft, ihn aktuell zu halten.", "it": "Con un piccolo contributo aiuti a tenerla aggiornata.", "es": "Una pequeña aportación ayuda a mantenerla al día.", "pt": "Uma pequena contribuição ajuda a mantê-lo atualizado."},
    "door": {"nl": "Samengesteld door J. Gelens. Bronnen en foto’s staan in de gids.", "en": "Compiled by J. Gelens. Sources and photos are listed in the guide.", "fr": "Rédigé par J. Gelens. Les sources et les photos figurent dans le guide.", "de": "Zusammengestellt von J. Gelens. Quellen und Fotos stehen im Guide.", "it": "Compilata da J. Gelens. Fonti e foto si trovano nella guida.", "es": "Elaborado por J. Gelens. Las fuentes y las fotos figuran en la guía.", "pt": "Compilado por J. Gelens. As fontes e as fotos estão no guia."},
}
def t(k, langs):
    if len(langs) == 1:
        return L[k][langs[0]]
    return "".join(f'<span class="l-{l}">{L[k][l]}</span>' for l in langs)
def spot(langs, base):
    url = lambda l: base + "spottersgids/" + ("" if l == "nl" else "?lang=en")
    if len(langs) == 1:
        return f'<a href="{url(langs[0])}">{L["spot"][langs[0]]}</a>'
    return "".join(f'<a class="l-{l}" href="{url(l)}">{L["spot"][l]}</a>' for l in langs)

PAW = '<svg viewBox="0 0 32 32" aria-hidden="true"><g fill="currentColor"><ellipse cx="16" cy="21" rx="7" ry="6"/><ellipse cx="7.5" cy="13" rx="2.8" ry="3.6"/><ellipse cx="13" cy="8.5" rx="2.8" ry="3.7"/><ellipse cx="19" cy="8.5" rx="2.8" ry="3.7"/><ellipse cx="24.5" cy="13" rx="2.8" ry="3.6"/></g></svg>'
ZOEK = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg>'
MENU = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M2 5h16M2 10h16M2 15h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
IC = {
    "kaart": '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
    "landen": '<path d="M5 21V4h11l-2 4 2 4H5"/>',
    "soorten": '<ellipse cx="12" cy="15" rx="4.5" ry="4"/><circle cx="6.5" cy="9.5" r="1.8"/><circle cx="10" cy="6" r="1.8"/><circle cx="14" cy="6" r="1.8"/><circle cx="17.5" cy="9.5" r="1.8"/>',
    "top10": '<path d="M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M7 6H4a3 3 0 0 0 3 4M17 6h3a3 3 0 0 1-3 4M12 14v4M8 21h8"/>',
    "geboren": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    "perpark": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "typen": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.5"/>',
    "over": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
}
def ic(k):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{IC[k]}</svg>'

def bovenbalk(langs, base, taal=True):
    """De bovenbalk van de startpagina. Bij taal=True komt de taalknop van de gids erin (het script verplaatst hem)."""
    h = lambda k: base + ("top10/" if k == "top10" else "#" + k)
    links = lambda ks: "".join(f'<a href="{h(k)}">{ic(k)}{t(k if k not in ("landen", "soorten") else k, langs)}</a>' for k in ks)
    return (f'<div class="hs-top" id="hs-top"><div class="hs-wrap">'
            f'<a class="hs-brand" href="{base}">{PAW}<span><b>{t("naam", langs)}</b><small>{t("sub", langs)} · J. Gelens</small></span></a>'
            f'<a class="hs-ico" href="{base}#zoek" aria-label="{L["zoek"][langs[0]]}">{ZOEK}<span class="t">{t("zoek", langs)}</span></a>'
            + ('<span id="hs-lang"></span>' if taal else "") +
            f'<button type="button" class="hs-ico" id="hs-menu-btn" aria-expanded="false" aria-controls="hs-menu" aria-label="Menu">{MENU}<span class="t">Menu</span></button></div>'
            f'<div class="hs-drop" id="hs-menu" hidden><div class="hs-wrap"><nav aria-label="Menu"><div>{links(["kaart", "landen", "soorten", "top10"])}</div>'
            f'<div>{links(["geboren", "perpark", "typen", "over"])}<div class="hs-meer"><span class="hs-lbl">{t("meer", langs)}</span>{spot(langs, base)}'
            f'<a href="https://ko-fi.com/katalogue" target="_blank" rel="noopener">{t("kofi", langs)} ☕</a></div></div></nav></div></div></div>')

def voet(langs):
    return (f'<footer class="hs-foot"><div class="hs-wrap"><div class="hs-kofibar"><p><b>{t("kofi_t", langs)}</b> {t("kofi_s", langs)}</p>'
            f'<a class="hs-kofi" href="https://ko-fi.com/katalogue" target="_blank" rel="noopener">☕ {t("kofi", langs)}</a></div>'
            f'<p>{t("door", langs)}</p></div></footer>')

CSS = r"""
/* ---- huisstijl van de startpagina (bron/huisstijl.py) ---- */
:root{--paper:#E3E1D0;--card:#F0EEE2;--ink:#1E2318;--muted:#5A604D;--line:#C6C3AD;--gold:#9B5A1C;--gold-soft:#EADFC8;--bark:#46552E;--tan:#F0EEE2;--tan-deep:#C6C3AD;
  --hs-olive:#46552E;--hs-accent:#9B5A1C;--hs-label:"Barlow Condensed","Arial Narrow",sans-serif;--hs-display:"Alegreya",Georgia,serif;--hs-body:"Alegreya Sans","Gill Sans","Segoe UI",system-ui,sans-serif;--hs-head:57px}
body{background:var(--paper)!important;font-family:var(--hs-body)!important}
h1,h2,h3{font-family:var(--hs-display)!important;color:var(--ink)}
a{color:var(--hs-accent)}
:focus-visible{outline:2px solid var(--hs-accent)!important}
.landbar{display:none!important}
.kofi-wrap{display:none!important}
/* bovenbalk */
.hs-top{position:sticky;top:env(safe-area-inset-top,0px);z-index:60;background:var(--card);border-bottom:1px solid var(--line);font-family:var(--hs-body);font-size:17px;line-height:1.4}
.hs-wrap{max-width:1120px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-right,0px)) 0 max(16px,env(safe-area-inset-left,0px))}
.hs-top>.hs-wrap{display:flex;align-items:center;gap:8px;min-height:56px}
.hs-brand{display:flex;align-items:center;gap:10px;text-decoration:none;min-width:0;margin-right:auto;color:var(--ink)}
.hs-brand svg{flex:none;width:30px;height:30px;color:var(--hs-accent)}
.hs-brand>span{min-width:0}
.hs-brand b{display:block;font-family:var(--hs-display);font-weight:800;font-size:1.15rem;line-height:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--ink)}
.hs-brand small{display:block;font-family:var(--hs-label);font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-top:3px;white-space:nowrap}
.hs-ico{flex:none;display:inline-flex;align-items:center;justify-content:center;gap:6px;border:1px solid var(--line);background:none;border-radius:8px;height:36px;min-width:38px;padding:0 9px;cursor:pointer;color:var(--ink);text-decoration:none;font:inherit}
.hs-ico svg{display:block;width:20px;height:20px}
.hs-ico[aria-expanded="true"]{background:var(--ink);color:var(--card);border-color:var(--ink)}
.hs-ico .t{font-weight:500;font-size:.98rem}
@media (max-width:820px){.hs-ico .t{display:none}}
@media (max-width:400px){.hs-top>.hs-wrap{gap:6px}.hs-brand{gap:7px}.hs-brand svg{width:26px;height:26px}.hs-brand b{font-size:1.04rem}.hs-brand small{font-size:.66rem}}
.hs-top .langsw{position:relative!important;top:auto!important;right:auto!important;left:auto!important;margin:0!important;flex:none;display:inline-flex}
.hs-top .lm .lm-btn{font-family:var(--hs-label);font-size:15px;letter-spacing:.06em;color:var(--ink);border:1px solid var(--line);border-radius:99px;height:36px;padding:0 11px;background:none}
.hs-top .lm .lm-btn:hover,.hs-top .lm .lm-btn[aria-expanded="true"]{background:var(--ink);color:var(--card);border-color:var(--ink)}
.hs-top .lm .lm-pop{background:var(--card);border:1px solid var(--line);border-radius:10px;box-shadow:0 8px 24px -12px rgba(30,35,24,.35)}
.hs-top .lm .lm-pop button{font-family:var(--hs-body);font-weight:500;font-size:16px;color:var(--ink)}
.hs-top .lm .lm-pop button:hover{background:color-mix(in srgb,var(--hs-olive) 12%,transparent)}
.hs-top .lm .lm-pop button[aria-pressed="true"]{background:var(--ink);color:var(--card)}
.hs-drop{position:absolute;left:0;right:0;top:100%;background:var(--card);border-bottom:1px solid var(--line);box-shadow:0 8px 24px -12px rgba(30,35,24,.35)}
.hs-drop[hidden]{display:none!important}
.hs-drop .hs-wrap{padding-top:10px;padding-bottom:16px}
.hs-drop nav{display:grid;gap:0 32px;grid-template-columns:minmax(0,1fr)}
@media (min-width:700px){.hs-drop nav{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.hs-drop a{display:flex;align-items:center;gap:10px;padding:12px 6px;font-size:1.08rem;font-weight:500;text-decoration:none;border-bottom:1px solid var(--line);color:var(--ink)}
.hs-drop a svg{flex:none;width:20px;height:20px;color:var(--hs-accent)}
.hs-meer a{font-size:1rem;color:var(--muted)}
.hs-lbl{display:block;padding:14px 6px 2px;font-family:var(--hs-label);font-weight:600;font-size:.8rem;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
/* rustiger kop */
header{display:block!important;padding:18px 0 12px!important;border-bottom:0!important}
header .paw,header>.langsw,header .langsw{display:none!important}
header .stamp{display:inline-block!important;background:none!important;color:var(--hs-olive)!important;padding:0!important;border-radius:0!important;font-family:var(--hs-label)!important;font-weight:600!important;font-size:.86rem!important;letter-spacing:.06em;text-transform:uppercase;margin:0 0 6px!important}
h1.mast{margin:0 0 8px!important;max-width:none!important}
h1.mast .m1{display:block!important;font-family:var(--hs-label)!important;font-size:.85rem!important;font-weight:600!important;letter-spacing:.1em!important;text-transform:uppercase;color:var(--muted)!important;line-height:1.3!important}
h1.mast .m2{display:block!important;font-family:var(--hs-display)!important;font-style:normal!important;font-weight:800!important;font-size:clamp(1.75rem,6vw,2.6rem)!important;color:var(--ink)!important;margin-top:2px!important;line-height:1.12!important;padding:0!important;background:none!important;border:0!important}
h1.mast .m2::before,h1.mast .m2::after{display:none!important}
h1.mast .m2::first-letter{text-transform:uppercase}
header figure.hero{margin:10px 0 8px!important;max-width:720px!important}
header figure.hero img{width:100%!important;max-width:100%!important;height:auto!important;aspect-ratio:21/9;object-fit:cover;border-radius:12px!important;box-shadow:none!important;margin:0 0 4px!important}
header figure.hero p{font-size:.82rem!important;margin:0!important}
header .lede{font-size:1.08rem!important;color:var(--muted)!important;max-width:44rem!important}
header .counts{margin-top:12px!important;gap:6px 24px!important}
header .counts b{font-family:var(--hs-display)!important;font-size:1.9rem!important;color:var(--ink)!important}
header .counts span{font-size:.95rem!important}
/* inhoud van de gids als tabbladen die blijven staan */
nav.toc{position:sticky!important;top:calc(env(safe-area-inset-top,0px) + var(--hs-head))!important;z-index:30!important;background:color-mix(in srgb,var(--paper) 94%,transparent)!important;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);display:flex!important;flex-wrap:nowrap!important;overflow-x:auto!important;gap:8px!important;padding:10px 0!important;border:0!important;border-bottom:1px solid var(--line)!important;margin:0!important;-webkit-mask-image:none!important;mask-image:none!important;scrollbar-width:none;font-family:var(--hs-body)!important}
nav.toc::-webkit-scrollbar{display:none}
nav.toc a{flex:none;border:1px solid var(--line)!important;background:var(--card);border-radius:99px;padding:5px 13px!important;margin:0!important;text-decoration:none!important;color:var(--ink)!important;font-weight:500;font-size:.95rem!important;white-space:nowrap}
nav.toc a.hs-on{background:var(--hs-olive);border-color:var(--hs-olive)!important;color:var(--card)!important}
section{scroll-margin-top:calc(var(--hs-head) + 64px)}
/* voet met Ko-fi */
.hs-foot{border-top:1px solid var(--line);margin-top:24px;background:var(--card);font-family:var(--hs-body);font-size:.95rem;color:var(--muted)}
.hs-foot .hs-wrap{padding-top:22px;padding-bottom:40px}
.hs-foot p{margin:0}
.hs-kofibar{display:flex;flex-wrap:wrap;align-items:center;gap:12px 20px;padding-bottom:18px;margin-bottom:16px;border-bottom:1px solid var(--line)}
.hs-kofibar p{flex:1 1 260px;color:var(--ink);font-size:1rem}
.hs-kofi{display:inline-flex;align-items:center;gap:8px;background:var(--hs-accent);color:#FFF8EA!important;text-decoration:none;font-weight:700;padding:11px 20px;border-radius:99px}
.hs-kofi:hover{filter:brightness(1.07)}
"""

JS = r"""<script>
(function(){
/* taalknop van de gids naar de bovenbalk */
var slot=document.getElementById("hs-lang"),src=document.querySelector("header .langsw");
if(slot){if(src)slot.replaceWith(src);else slot.remove();}
/* menu */
var mb=document.getElementById("hs-menu-btn"),m=document.getElementById("hs-menu");
function dicht(){if(!m)return;m.hidden=true;mb.setAttribute("aria-expanded","false");}
if(mb&&m){mb.addEventListener("click",function(e){e.stopPropagation();var o=m.hidden;m.hidden=!o;mb.setAttribute("aria-expanded",String(o));});
  document.addEventListener("click",function(e){if(!e.target.closest||!e.target.closest("#hs-top"))dicht();});
  document.addEventListener("keydown",function(e){if(e.key==="Escape"&&!m.hidden){dicht();mb.focus();}});}
/* hoogte van de bovenbalk voor de tabbladen eronder */
var top=document.getElementById("hs-top");function hoogte(){if(top&&top.offsetHeight)document.documentElement.style.setProperty("--hs-head",top.offsetHeight+"px");}
hoogte();addEventListener("resize",hoogte);
/* het tabblad van het stuk dat je leest licht op */
var raf=0;function actief(){raf=0;var navs=[].slice.call(document.querySelectorAll("nav.toc")).filter(function(n){return n.offsetParent;});
  navs.forEach(function(nav){var as=[].slice.call(nav.querySelectorAll('a[href^="#"]')),cur=null,lim=(top?top.offsetHeight:57)+nav.offsetHeight+30;
    as.forEach(function(a){var id=a.getAttribute("href").slice(1),el=id&&document.getElementById(id);if(el&&el.offsetParent!==null&&el.getBoundingClientRect().top<=lim)cur=a;});
    as.forEach(function(a){a.classList.toggle("hs-on",a===cur);});
    if(cur&&cur.dataset.hsOn!=="1"){as.forEach(function(a){a.dataset.hsOn="";});cur.dataset.hsOn="1";var l=cur.offsetLeft-nav.offsetLeft-16;if(l<nav.scrollLeft||l+cur.offsetWidth>nav.scrollLeft+nav.clientWidth)nav.scrollTo({left:Math.max(0,l),behavior:"smooth"});}});}
addEventListener("scroll",function(){if(!raf)raf=requestAnimationFrame(actief);},{passive:true});
setTimeout(actief,300);
})();
</script>
"""

def toepassen(doc, langs, base):
    """Huisstijl op een gids of deelstaatpagina zetten (website)."""
    doc = lettertypen(doc)
    m = re.search(r'<nav class="landbar".*?</nav>', doc, re.S)
    assert m, "landbar niet gevonden"
    # het pootje krijgt het id van de oude link "← Alle landen": het script van de gids luistert daarnaar
    kop = bovenbalk(langs, base).replace('<a class="hs-brand" href=', '<a class="hs-brand" id="naar-landen" href=', 1)
    doc = doc[:m.start()] + f"<style>{CSS}</style>\n" + kop + doc[m.end():]
    k = re.search(r'<div class="kofi-wrap"><aside class="kofi-card".*?</aside></div>', doc, re.S)
    assert k, "Ko-fi-blok niet gevonden"
    doc = doc[:k.start()] + voet(langs) + doc[k.end():]
    i = doc.rindex("</body>")
    return doc[:i] + JS + doc[i:]
