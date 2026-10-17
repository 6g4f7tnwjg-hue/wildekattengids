"""Testontwerp voor de Nederlandse gids (oktober 2026).

Maakt /nederland-nieuw/index.html uit de gebouwde /nederland/index.html, met de nieuwe opmaak
(kop met illustratie, zoekbalk, snelknoppen, tegels, favorieten, onderbalk, crème/groen/terracotta).
De echte pagina /nederland/ blijft ongewijzigd. Alle feiten komen uit de gebouwde pagina.

Gebruik: python3 bron/nieuw_ontwerp.py   (draait ook automatisch aan het eind van bouw.py)
Terugdraaien: map nederland-nieuw/ en img/nieuw/ weghalen en de regel onderaan bouw.py verwijderen.
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BASE = "/wildekattengids/"
IMG = BASE + "img/nieuw/"


def L(nl, en):
    return f'<span class="l-nl">{nl}</span><span class="l-en">{en}</span>'


ICO = {
    "pin": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M6 12l11-4 14 5 11-4v27l-11 4-14-5-11 4z" fill="#C9D6BC"/><path d="M17 8v27M31 13v27" stroke="#9DB28E" stroke-width="2"/><path d="M33 4a8 8 0 0 0-8 8c0 6 8 14 8 14s8-8 8-14a8 8 0 0 0-8-8z" fill="#2F4A32"/><circle cx="33" cy="12" r="3" fill="#F5F0E4"/></svg>',
    "paw": '<svg viewBox="0 0 48 48" aria-hidden="true" fill="#A65A35"><ellipse cx="24" cy="31" rx="10" ry="8.5"/><ellipse cx="10.5" cy="21" rx="4" ry="5.2"/><ellipse cx="18.5" cy="13.5" rx="4" ry="5.4"/><ellipse cx="29.5" cy="13.5" rx="4" ry="5.4"/><ellipse cx="37.5" cy="21" rx="4" ry="5.2"/></svg>',
    "cal": '<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="6" y="9" width="36" height="32" rx="5" fill="#4C6670"/><rect x="6" y="9" width="36" height="9" rx="4" fill="#3A515A"/><rect x="10" y="21" width="28" height="16" rx="2" fill="#DDE6E6"/><path d="M15 5v8M33 5v8" stroke="#3A515A" stroke-width="3.4" stroke-linecap="round"/><path d="M19 23v12M29 23v12M12 27h24M12 32h24" stroke="#4C6670" stroke-width="1.8"/></svg>',
    "heart": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 41S6 30 6 17.5A9.5 9.5 0 0 1 24 13a9.5 9.5 0 0 1 18 4.5C42 30 24 41 24 41z" fill="#C2564F"/></svg>',
    "search": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg>',
    "tbl": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M3 14h18M9 9v11"/></svg>',
    "news": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18"/><path d="M9 15l2 2 4-4"/></svg>',
    "dna": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M7 3c0 6 10 6 10 12s-10 6-10 6M17 3c0 6-10 6-10 12"/><path d="M8.5 7h7M8.5 17h7"/></svg>',
    "info": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="#2F4A32"/><circle cx="12" cy="7.2" r="1.6" fill="#F5F0E4"/><path d="M12 11v7" stroke="#F5F0E4" stroke-width="2.6" stroke-linecap="round"/></svg>',
    "flag": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 21V4h11l-2 4 2 4H5"/></svg>',
    "cat": '<svg viewBox="0 0 100 120" aria-hidden="true" fill="currentColor"><path d="M30 18l8 14c6-2 14-2 20 0l8-14 4 22c6 7 8 15 6 24 10 10 14 26 10 42-2 8-10 12-20 12H36c-14 0-20-8-18-20 2-14 8-24 14-30-4-10-3-20 2-28z"/></svg>',
    # onderbalk
    "b-home": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/></svg>',
    "b-map": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/></svg>',
    "b-paw": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><ellipse cx="12" cy="15.5" rx="5" ry="4.3"/><ellipse cx="5.3" cy="10.5" rx="2" ry="2.6"/><ellipse cx="9.3" cy="6.7" rx="2" ry="2.7"/><ellipse cx="14.7" cy="6.7" rx="2" ry="2.7"/><ellipse cx="18.7" cy="10.5" rx="2" ry="2.6"/></svg>',
    "b-heart": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 20s-8-5-8-11a4.5 4.5 0 0 1 8-2.5A4.5 4.5 0 0 1 20 9c0 6-8 11-8 11z"/></svg>',
    "b-menu": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>',
}
LOGO = '<svg viewBox="0 0 64 64" aria-hidden="true" fill="#2F4A32"><ellipse cx="32" cy="42" rx="13" ry="11.5"/><ellipse cx="14.5" cy="28" rx="5.4" ry="7"/><ellipse cx="25" cy="17.5" rx="5.4" ry="7.2"/><ellipse cx="39" cy="17.5" rx="5.4" ry="7.2"/><ellipse cx="49.5" cy="28" rx="5.4" ry="7"/></svg>'
ARROW = '<svg class="nw-arr" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>'

CSS = r"""
<style id="nw-css">
/* ---- testontwerp (bron/nieuw_ontwerp.py) ---- */
:root:root{--paper:#F5F0E4;--card:#FBF8F1;--ink:#22301F;--muted:#5E6656;--line:#E2DACB;--hs-olive:#2F4A32;--hs-accent:#A65A35;--gold:#A65A35;--bark:#2F4A32;--tan:#FBF8F1;--tan-deep:#E2DACB;
  --nw-sage:#E3EADB;--nw-peach:#F3E2D3;--nw-blue:#DDE6E6;--nw-lilac:#E6DDE8;--nw-rose:#F4E3DF;--nw-green:#2F4A32;--nw-terra:#A65A35;--nw-shadow:0 1px 2px rgba(60,50,30,.06),0 10px 24px -14px rgba(60,50,30,.35)}
body{background:var(--paper)!important;padding-bottom:calc(76px + env(safe-area-inset-bottom,0px))}
h2{color:var(--nw-green)!important}
html body nav.toc{display:none!important}
html.nw-heroin .hs-top .hs-brand>span{visibility:hidden}
.hs-top{background:color-mix(in srgb,var(--paper) 92%,transparent)!important;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
html body .wrap>section,html body .wrap>.board{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:6px 18px 14px;margin:18px 0!important;box-shadow:var(--nw-shadow)}
html body header{background:var(--card);border:1px solid var(--line)!important;border-radius:20px;padding:16px 18px 14px!important;margin-top:18px;box-shadow:var(--nw-shadow)}
header .stamp:not(.nw-keep){display:none!important}
table th{background:var(--nw-sage)!important;color:var(--ink)!important}
/* kop */
.nw-hero{position:relative;margin:12px 0 0;border-radius:22px;overflow:hidden;min-height:210px;background:#F5F0E4 url(IMGkop-lynx.webp) right center/cover no-repeat;display:flex;align-items:center}
.nw-hero::before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(245,240,228,.92) 0,rgba(245,240,228,.75) 42%,rgba(245,240,228,0) 66%)}
.nw-hero>div{position:relative;padding:20px 18px;max-width:64%}
.nw-logo{display:flex;align-items:center;gap:8px;margin:0}
.nw-logo svg{flex:none;width:clamp(30px,8vw,52px);height:auto}
.nw-logo b{font-family:var(--hs-display);font-weight:800;font-size:clamp(1.55rem,7.2vw,3.3rem);line-height:1;color:var(--nw-green);letter-spacing:-.01em}
.nw-caps{margin:8px 0 0;font-family:var(--hs-label);font-weight:600;letter-spacing:.16em;text-transform:uppercase;font-size:clamp(.66rem,2.4vw,1rem);color:var(--nw-green)}
.nw-script{margin:6px 0 0;font-family:"Caveat",cursive;font-size:clamp(1.25rem,5vw,2.1rem);color:var(--nw-green);line-height:1.1}
.nw-stand{margin:8px 0 0;font-size:.82rem;color:var(--muted)}
.nw-illu{position:absolute;right:12px;top:10px;font-size:.68rem;color:#4E5A48;background:rgba(245,240,228,.8);padding:1px 7px;border-radius:99px}
/* zoeken */
.nw-search{position:relative;margin:-22px 10px 0;z-index:5}
.nw-search label{display:flex;align-items:center;gap:10px;background:#FFFDF8;border:1px solid var(--line);border-radius:99px;padding:0 18px;height:54px;box-shadow:var(--nw-shadow)}
.nw-search label svg{width:22px;height:22px;flex:none;color:var(--ink)}
.nw-search input{all:unset;flex:1;min-width:0;font:400 1.05rem var(--hs-body);color:var(--ink)}
.nw-search input:focus-visible{outline:none!important}.nw-search label:focus-within{border-color:var(--nw-green);box-shadow:0 0 0 2px color-mix(in srgb,var(--nw-green) 25%,transparent),var(--nw-shadow)}
.nw-search input::placeholder{color:#8A8F80}
.nw-res{position:absolute;left:0;right:0;top:60px;background:#FFFDF8;border:1px solid var(--line);border-radius:18px;box-shadow:var(--nw-shadow);padding:6px;max-height:60vh;overflow:auto}
.nw-res[hidden]{display:none}
.nw-res a{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:12px;color:var(--ink);text-decoration:none}
.nw-res a:hover,.nw-res a.on{background:var(--nw-sage)}
.nw-res a i{font-style:normal;flex:none;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:var(--nw-peach);color:var(--nw-terra)}
.nw-res a i svg{width:18px;height:18px}
.nw-res a.loc i{background:var(--nw-sage);color:var(--nw-green)}
.nw-res b{font-weight:600}
.nw-res small{display:block;color:var(--muted);font-size:.85rem}
.nw-res .nw-none{padding:10px 12px;color:var(--muted)}
/* snelknoppen */
.nw-quick{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:22px 0 0}
.nw-quick a{display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;padding:14px 4px 12px;border-radius:24px;border:1px solid var(--line);text-decoration:none;color:var(--ink);box-shadow:var(--nw-shadow)}
.nw-quick a:nth-child(1){background:var(--nw-sage)}.nw-quick a:nth-child(2){background:var(--nw-peach)}.nw-quick a:nth-child(3){background:var(--nw-blue)}.nw-quick a:nth-child(4){background:var(--nw-rose)}
.nw-quick svg{width:clamp(34px,10vw,52px);height:auto}
.nw-quick b{font-family:var(--hs-display);font-weight:700;font-size:clamp(.8rem,3.2vw,1.2rem);line-height:1.15;overflow-wrap:anywhere;color:var(--nw-green)}
.nw-quick small{font-size:clamp(.7rem,2.9vw,.9rem);line-height:1.2;color:var(--muted)}
/* tegels */
.nw-tiles{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:16px 0 0}
.nw-tile{position:relative;display:flex;flex-direction:column;justify-content:flex-end;min-height:150px;padding:14px;border-radius:22px;overflow:hidden;text-decoration:none;color:var(--ink);border:1px solid var(--line);background-size:cover;background-position:right center;box-shadow:var(--nw-shadow)}
.nw-tile::before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,var(--tb) 0,color-mix(in srgb,var(--tb) 88%,transparent) 50%,transparent 85%)}
.nw-tile>*{position:relative}
.nw-tile .nw-ti{width:30px;height:30px;color:var(--tc);margin-bottom:auto}
.nw-tile .nw-ti svg{width:30px;height:30px}
.nw-tile b{font-family:var(--hs-display);font-weight:800;font-size:clamp(1.15rem,4.8vw,1.75rem);line-height:1.08;color:var(--tc);margin-top:18px;max-width:72%}
.nw-tile span.s{display:flex;align-items:center;gap:2px;font-size:clamp(.78rem,3.2vw,1rem);line-height:1.25;color:var(--ink);margin-top:4px;max-width:74%}
.nw-arr{width:16px;height:16px;flex:none}
.nw-t1{--tb:var(--nw-peach);--tc:#7A3F22;background-image:url(IMGtegel-jaguar.webp)}
.nw-t2{--tb:var(--nw-blue);--tc:#2F4A52;background-image:url(IMGtegel-sneeuwluipaard.webp)}
.nw-t3{--tb:var(--nw-lilac);--tc:#4E3A5A;background-image:url(IMGtegel-witte-leeuw.webp)}
.nw-t4{--tb:var(--nw-sage);--tc:var(--nw-green);background:var(--nw-sage)}
.nw-t4::before{display:none}
.nw-t4 .nw-sil{position:absolute;right:-6px;bottom:-10px;width:44%;max-width:120px;color:#7E9B83;opacity:.75}
.nw-t4 .nw-ti svg{width:32px;height:32px}
.nw-strip{display:flex;align-items:center;gap:12px;margin:12px 0 0;padding:14px 16px;border-radius:22px;background:var(--nw-terra);color:#FFF8EE;text-decoration:none;box-shadow:var(--nw-shadow)}
.nw-strip svg{width:24px;height:24px;flex:none}
.nw-strip span{flex:1;line-height:1.3}
.nw-strip b{display:block;font-family:var(--hs-display);font-size:1.15rem}
.nw-strip .nw-arr{width:20px;height:20px}
/* favorieten */
#favorieten h2{display:flex;align-items:center;gap:8px}
#favorieten h2 svg{width:24px;height:24px}
.nw-favs{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.nw-favs li{display:flex;align-items:center;gap:4px;background:var(--nw-rose);border-radius:99px;padding:3px 4px 3px 12px}
.nw-favs a{color:var(--ink);font-weight:600;text-decoration:none}
.nw-favs small{color:var(--muted)}
.nw-empty{color:var(--muted);margin:0 0 6px}
.nw-heart{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;color:#B4483F;flex:none;vertical-align:middle}
.nw-heart svg{width:22px;height:22px}
.nw-heart svg path{fill:transparent;stroke:currentColor;stroke-width:2}
.nw-heart[aria-pressed="true"] svg path{fill:currentColor}
.nw-heart:focus-visible{outline:2px solid var(--nw-terra)}
.nw-favs .nw-heart{width:28px;height:28px}.nw-favs .nw-heart svg{width:18px;height:18px}
.loclist li{position:relative}
.loclist li>.nw-heart{position:absolute;top:4px;right:4px}
.loclist li>b{padding-right:30px;display:inline-block}
#info .nw-hwrap{display:inline-flex;align-items:center;gap:6px;font:500 .95rem var(--hs-body);color:var(--muted);margin:2px 0 8px;background:var(--nw-rose);border-radius:99px;padding:0 12px 0 2px}
/* onderbalk */
.nw-bar{position:fixed;left:0;right:0;bottom:0;z-index:70;background:color-mix(in srgb,#FBF8F1 96%,transparent);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border-top:1px solid var(--line);padding:6px 4px calc(6px + env(safe-area-inset-bottom,0px))}
.nw-bar nav{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));max-width:640px;margin:0 auto}
.nw-bar a,.nw-bar button{all:unset;box-sizing:border-box;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:2px;padding:4px 2px;font:500 .78rem var(--hs-body);color:var(--muted);text-align:center;position:relative}
.nw-bar svg{width:24px;height:24px}
.nw-bar .on{color:var(--nw-green);font-weight:700}
.nw-bar .on::after{content:"";position:absolute;bottom:-4px;left:22%;right:22%;height:3px;border-radius:3px;background:var(--nw-green)}
.nw-bar :focus-visible{outline:2px solid var(--nw-terra);border-radius:8px}
@media (min-width:760px){.nw-hero{min-height:300px}.nw-hero>div{padding:32px 34px}.nw-tile{min-height:190px;padding:18px}.nw-search{margin:-26px 40px 0}}
@media (max-width:380px){.nw-quick{gap:7px}.nw-quick a{padding:12px 2px 10px;border-radius:20px}.nw-tiles{gap:9px}.nw-tile{padding:12px;min-height:140px}}
</style>
""".replace("IMG", IMG)

HERO = f"""
<div id="nw-home"></div>
<div class="nw-hero" role="banner">
  <div>
    <p class="nw-logo">{LOGO}<b>{L("Bezoekersgids", "Visitor’s Guide")}</b></p>
    <p class="nw-caps">{L("Wilde katten · in dierentuinen", "Wild cats · in zoos")}</p>
    <p class="nw-script">{L("Ontdek. Leer. Bewonder.", "Discover. Learn. Admire.")}</p>
    <p class="nw-stand" id="nw-stand"></p>
  </div>
  <span class="nw-illu">{L("illustratie", "illustration")}</span>
</div>
<div class="nw-search">
  <label>{ICO["search"]}<input type="search" id="nw-q" autocomplete="off" aria-controls="nw-res" aria-label="Zoek een soort, dierentuin of plaats"></label>
  <div class="nw-res" id="nw-res" role="listbox" hidden></div>
</div>
<nav class="nw-quick" aria-label="Snelknoppen">
  <a href="#locaties">{ICO["pin"]}<b>{L("Locaties", "Locations")}</b><small>{L("Dierentuinen &amp; kaart", "Zoos &amp; map")}</small></a>
  <a href="#soorten">{ICO["paw"]}<b>{L("Per kat", "By cat")}</b><small><span class="nw-nsp"></span> {L("soorten", "species")}</small></a>
  <a href="#route">{ICO["cal"]}<b>{L("Routeplanner", "Route planner")}</b><small>{L("Plan je bezoek", "Plan your visit")}</small></a>
  <a href="#favorieten">{ICO["heart"]}<b>{L("Favorieten", "Favourites")}</b><small>{L("Jouw lijst", "Your list")}</small></a>
</nav>
<nav class="nw-tiles" aria-label="Onderdelen">
  <a class="nw-tile nw-t1" href="#tldr"><span class="nw-ti">{ICO["tbl"]}</span><b>{L("In het kort", "In short")}</b><span class="s">{L("De belangrijkste punten", "The key points")}{ARROW}</span></a>
  <a class="nw-tile nw-t2" href="#actueel"><span class="nw-ti">{ICO["news"]}</span><b>{L("Actueel", "Latest")}</b><span class="s">{L("Geboortes &amp; veranderingen", "Births &amp; changes")}{ARROW}</span></a>
  <a class="nw-tile nw-t3" href="#kleur"><span class="nw-ti">{ICO["dna"]}</span><b>{L("Kleur &amp; hybriden", "Colour &amp; hybrids")}</b><span class="s">{L("Bijzondere kleuren", "Special colours")}{ARROW}</span></a>
  <a class="nw-tile nw-t4" href="#uitleg"><span class="nw-ti">{ICO["info"]}</span><span class="nw-sil">{ICO["cat"]}</span><b>{L("Over", "About")}</b><span class="s">{L("Hoe werkt deze gids?", "How does this guide work?")}{ARROW}</span></a>
</nav>
<a class="nw-strip" href="#rapporteer">{ICO["flag"]}<span><b>{L("Rapporteer", "Report")}</b>{L("Iets gezien dat hier niet klopt? Laat het weten.", "Seen something that is not right here? Let us know.")}</span>{ARROW}</a>
<section id="favorieten">
  <h2>{ICO["heart"]}{L("Favorieten", "Favourites")}</h2>
  <div id="nw-favs"></div>
</section>
"""

BAR = f"""
<div class="nw-bar"><nav aria-label="Navigatie">
  <a href="#nw-home" data-nw="home">{ICO["b-home"]}{L("Home", "Home")}</a>
  <a href="#locaties" data-nw="locaties">{ICO["b-map"]}{L("Locaties", "Locations")}</a>
  <a href="#soorten" data-nw="soorten">{ICO["b-paw"]}{L("Per kat", "By cat")}</a>
  <a href="#favorieten" data-nw="favorieten">{ICO["b-heart"]}{L("Favorieten", "Favourites")}</a>
  <button type="button" id="nw-meer">{ICO["b-menu"]}{L("Meer", "More")}</button>
</nav></div>
"""

JS = r"""
<script>
(function(){
var N=window.__NW;if(!N)return;
var R=N.R,LOCS=N.LOCS,SPECIES=N.SPECIES,SPEN=N.SPEN,BYSLUG=N.BYSLUG,LOCBYSLUG=N.LOCBYSLUG,slug=N.slug,lslug=N.lslug;
var HEART='HEARTSVG', PAWI='PAWSVG', PINI='PINSVG';
function E(s){return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});}
function LS(nl,en){return '<span class="l-nl">'+E(nl)+'</span><span class="l-en">'+E(en)+'</span>';}
function en(n){return (typeof SPEN!=="undefined"&&SPEN[n])?SPEN[n][0]:n;}
var SEEN={};R.forEach(function(r){SEEN[r[0]]=1;});
var LOCSLUG=LOCS.map(function(l){return lslug(l[0]);});
/* stand en aantal soorten uit de pagina zelf */
var st=document.querySelector("header .stamp");if(st){document.getElementById("nw-stand").innerHTML=st.innerHTML;}
var nb=document.querySelector("header .counts b");document.querySelectorAll(".nw-nsp").forEach(function(s){s.textContent=nb?nb.textContent:"";});
/* zoekveld */
var q=document.getElementById("nw-q"),res=document.getElementById("nw-res");
function ph(){q.placeholder=N.lang()==="en"?"Search a species, zoo or town…":"Zoek een soort, dierentuin of plaats…";}
ph();new MutationObserver(ph).observe(document.documentElement,{attributes:true,attributeFilter:["class","lang"]});
function norm(s){return String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"").replace(/[’']/g,"");}
var ITEMS=[];
SPECIES.forEach(function(a){ITEMS.push({k:"sp",h:"#soort/"+slug(a[0]),nl:a[0],en:en(a[0]),sub:a[2],seen:!!SEEN[a[0]],t:norm(a[0]+" "+en(a[0])+" "+a[1]+" "+a[2])});});
LOCS.forEach(function(l,i){ITEMS.push({k:"loc",h:"#locatie/"+LOCSLUG[i],nl:l[0],en:l[0],sub:l[1],seen:true,t:norm(l[0]+" "+l[1]+" "+(l[4]||[]).join(" "))});});
var cur=-1;
function show(){var v=norm(q.value.trim());cur=-1;
  if(!v){res.hidden=true;res.innerHTML="";return;}
  var w=v.split(/\s+/);
  var hit=ITEMS.filter(function(it){return w.every(function(x){return it.t.indexOf(x)>=0;});});
  hit.sort(function(a,b){var sa=norm(a.nl).indexOf(v)===0||norm(a.en).indexOf(v)===0,sb=norm(b.nl).indexOf(v)===0||norm(b.en).indexOf(v)===0;return (sb-sa)||(b.seen-a.seen);});
  hit=hit.slice(0,8);
  res.innerHTML=hit.length?hit.map(function(it){
    var sub=it.k==="loc"?LS(it.sub,it.sub):(it.seen?'<em>'+E(it.sub)+'</em>':LS("niet in Nederland te zien","not on view in the Netherlands"));
    return '<a role="option" class="'+it.k+'" href="'+it.h+'"><i>'+(it.k==="loc"?PINI:PAWI)+'</i><span><b>'+LS(it.nl,it.en)+'</b><small>'+sub+'</small></span></a>';}).join("")
    :'<p class="nw-none">'+LS("Niets gevonden.","Nothing found.")+'</p>';
  res.hidden=false;}
q.addEventListener("input",show);
q.addEventListener("focus",show);
q.addEventListener("keydown",function(e){var as=res.querySelectorAll("a");if(!as.length)return;
  if(e.key==="ArrowDown"||e.key==="ArrowUp"){e.preventDefault();cur=(cur+(e.key==="ArrowDown"?1:-1)+as.length)%as.length;as.forEach(function(a,i){a.classList.toggle("on",i===cur);});}
  else if(e.key==="Enter"){e.preventDefault();location.hash=(as[cur>=0?cur:0]).getAttribute("href").slice(1);close();}
  else if(e.key==="Escape"){close();}});
function close(){res.hidden=true;q.blur();}
res.addEventListener("click",function(){setTimeout(function(){res.hidden=true;q.value="";},0);});
document.addEventListener("click",function(e){if(!e.target.closest(".nw-search"))res.hidden=true;});
/* het zoekicoon in de bovenbalk gaat naar dit zoekveld */
var tz=document.querySelector('.hs-top a.hs-ico[href$="#zoek"]');
if(tz){tz.href="#nw-home";tz.addEventListener("click",function(e){e.preventDefault();
  if(document.getElementById("main").hidden){location.hash="nw-home";}
  setTimeout(function(){window.scrollTo(0,0);q.focus();},30);});}
/* favorieten (alleen in deze browser bewaard) */
function getF(){try{var f=JSON.parse(localStorage.getItem("nw-fav")||"null");if(f&&f.loc&&f.sp)return f;}catch(e){}return {loc:[],sp:[]};}
var MEM=null;
function F(){return MEM||(MEM=getF());}
function save(){try{localStorage.setItem("nw-fav",JSON.stringify(MEM));}catch(e){}}
function has(k,s){return F()[k].indexOf(s)>=0;}
function toggle(k,s){var a=F()[k],i=a.indexOf(s);if(i>=0)a.splice(i,1);else a.push(s);save();paint();}
function btn(k,s){var on=has(k,s);return '<button type="button" class="nw-heart" data-fk="'+k+'" data-fs="'+E(s)+'" aria-pressed="'+on+'" aria-label="'+(on?(N.lang()==="en"?"Remove from favourites":"Uit favorieten halen"):(N.lang()==="en"?"Add to favourites":"Toevoegen aan favorieten"))+'">'+HEART+'</button>';}
document.addEventListener("click",function(e){var b=e.target.closest(".nw-heart");if(!b)return;e.preventDefault();e.stopPropagation();toggle(b.dataset.fk,b.dataset.fs);});
function renderFavs(){var f=F(),out=[];
  f.loc.forEach(function(s){var i=LOCBYSLUG[s];if(i===undefined)return;out.push('<li><a href="#locatie/'+s+'">'+E(LOCS[i][0])+'</a> <small>'+E(LOCS[i][1])+'</small>'+btn("loc",s)+'</li>');});
  f.sp.forEach(function(s){var a=BYSLUG[s];if(!a)return;out.push('<li><a href="#soort/'+s+'">'+LS(a[0],en(a[0]))+'</a>'+btn("sp",s)+'</li>');});
  document.getElementById("nw-favs").innerHTML=out.length?'<ul class="nw-favs">'+out.join("")+'</ul>'
    :'<p class="nw-empty">'+LS("Nog geen favorieten. Tik op het hartje bij een park of een soort om het hier te bewaren. Je lijst blijft alleen op dit apparaat.","No favourites yet. Tap the heart next to a park or a species to keep it here. Your list stays on this device only.")+'</p>';}
function listHearts(){document.querySelectorAll(".loclist li").forEach(function(li){var a=li.querySelector(':scope > b > a[href^="#locatie/"]');if(!a)return;
  var s=decodeURIComponent(a.getAttribute("href").slice(9)),old=li.querySelector(":scope > .nw-heart");
  var w=document.createElement("span");w.innerHTML=btn("loc",s);if(old)old.replaceWith(w.firstChild);else li.appendChild(w.firstChild);});}
var info=document.getElementById("info"),busy=false;
function infoHeart(){if(info.hidden)return;var h=decodeURIComponent(location.hash||""),m=h.match(/^#(locatie|soort)\/(.+)$/);if(!m)return;
  var k=m[1]==="locatie"?"loc":"sp",s=m[2],t=info.querySelector("h1, h2");if(!t)return;
  busy=true;var old=info.querySelector(".nw-hwrap");if(old)old.remove();
  var w=document.createElement("div");w.className="nw-hwrap";w.innerHTML=btn(k,s)+LS(has(k,s)?"In je favorieten":"Bewaar als favoriet",has(k,s)?"In your favourites":"Save as favourite");
  t.insertAdjacentElement("afterend",w);busy=false;}
function paint(){renderFavs();listHearts();infoHeart();}
new MutationObserver(function(){if(!busy)infoHeart();}).observe(info,{childList:true});
paint();
/* onderbalk */
var bar=document.querySelectorAll(".nw-bar [data-nw]");
function mark(){var h=location.hash||"",main=document.getElementById("main"),id="";
  if(main.hidden){id=/^#locatie\//.test(h)?"locaties":/^#soort\//.test(h)?"soorten":"";}
  else{var ids=["favorieten","soorten","locaties"],y=window.innerHeight*0.35;id="home";
    ids.forEach(function(k){var el=document.getElementById(k);if(!el)return;var r=el.getBoundingClientRect();if(r.top<y&&r.bottom>y)id=k;});}
  bar.forEach(function(a){var on=a.dataset.nw===id;a.classList.toggle("on",on);if(on)a.setAttribute("aria-current","page");else a.removeAttribute("aria-current");});}
window.addEventListener("scroll",mark,{passive:true});window.addEventListener("hashchange",function(){setTimeout(mark,50);});mark();
document.getElementById("nw-meer").addEventListener("click",function(e){e.stopPropagation();var b=document.getElementById("hs-menu-btn");if(b)b.click();});
/* naam in de bovenbalk pas tonen als de kop uit beeld is */
var hero=document.querySelector(".nw-hero");
if("IntersectionObserver" in window&&hero){new IntersectionObserver(function(es){document.documentElement.classList.toggle("nw-heroin",es[0].isIntersecting&&!document.getElementById("main").hidden);}).observe(hero);}
})();
</script>
"""


def maak():
    src = os.path.join(ROOT, "nederland", "index.html")
    doc = open(src, encoding="utf-8").read()

    def sub1(t, a, b):
        assert t.count(a) >= 1, f"niet gevonden: {a[:60]}"
        return t.replace(a, b, 1)

    head = ('<meta name="robots" content="noindex">\n'
            '<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;600&display=swap" rel="stylesheet">\n'
            + CSS)
    doc = sub1(doc, "</head>", head + "</head>")
    doc = sub1(doc, '<div class="wrap" id="main">', '<div class="wrap" id="main">\n' + HERO)
    js = (JS.replace("HEARTSVG", '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-8-5-8-11a4.5 4.5 0 0 1 8-2.5A4.5 4.5 0 0 1 20 9c0 6-8 11-8 11z"/></svg>')
          .replace("PAWSVG", ICO["b-paw"]).replace("PINSVG", ICO["b-map"]))
    exp = ('window.__NW={R:R,LOCS:LOCS,SPECIES:SPECIES,SPEN:SPEN,BYSLUG:BYSLUG,LOCBYSLUG:LOCBYSLUG,slug:slug,lslug:lslug,'
           'lang:function(){return LANG;}};\n')
    a = doc.index("const SPECIES=[")
    e = doc.index("})();\n</script>", a)
    doc = doc[:e] + exp + doc[e:]
    i = doc.rindex("</body>")
    doc = doc[:i] + BAR + js + doc[i:]
    out = os.path.join(ROOT, "nederland-nieuw")
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(doc)
    print("testontwerp geschreven:", os.path.join("nederland-nieuw", "index.html"))


if __name__ == "__main__":
    maak()
