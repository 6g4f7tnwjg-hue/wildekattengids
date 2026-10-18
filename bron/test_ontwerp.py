"""Testontwerp landpagina (18-10-2026): /nederland-test/.

Proef voor een eenvoudiger opbouw die dichter bij de hoofdpagina (Europa) ligt. Bouwt voort op
bron/nieuw_ontwerp.py (schermen, zoeken, favorieten, terugknop), maar met een andere indeling:
- onderbalk Kaart · Soorten · Locaties · Meer (Routeplanner, Actueel en de rest staan onder Meer);
- startscherm = de kaart: kop zoals op de hoofdpagina, soortrondjes met foto die de kaart filteren,
  de kaart met de typeknoppen eronder (legenda en filter tegelijk) en een lijst "In beeld";
- Soorten: fotokaartjes zoals op de hoofdpagina; de hoofdtabel is een eigen scherm (onder Meer);
- Locaties: één lijst met locatiekaartjes (type-icoon, naam, plaats, aantal soorten) met typefilter;
  "Geen katachtigen gevonden" en "Niet specifiek online te verifiëren" staan onder Over;
- geen tegels met illustraties en geen grote Rapporteer-balk (Rapporteer staat onder Meer en bij elk park).
Alle teksten en feiten komen uit de gids zelf (/nederland-oud/, de gebouwde pagina zonder app-ontwerp).

Gebruik: python3 bron/test_ontwerp.py   (draait ook aan het eind van bouw.py)
Weghalen: map /nederland-test/, dit bestand en de regels onderaan bouw.py.
"""
import json
import os

import nieuw_ontwerp as NO

ROOT = NO.ROOT
BRON = "nederland-oud"
DOEL = "nederland-test"
L = NO.L

ICO = dict(NO.ICO)
ICO["b-pin"] = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round">'
                '<path d="M12 21s-7-6.2-7-11.6a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.4" r="2.5"/></svg>')
ICO["rows"] = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">'
               '<path d="M8 6h13M8 12h13M8 18h13"/><circle cx="3.5" cy="6" r="1.2" fill="currentColor"/><circle cx="3.5" cy="12" r="1.2" fill="currentColor"/>'
               '<circle cx="3.5" cy="18" r="1.2" fill="currentColor"/></svg>')

START = f"""
<div id="start">
<div class="nt-kop">
  <div class="nw-htxt" id="nw-htxt"></div>
  <div class="nt-meta"><div class="nw-stats"><a href="#soorten"><span class="nw-nsp"></span></a><a href="#locaties"><span class="nw-nloc"></span></a></div></div>
</div>
<div class="nw-search">
  <label>{ICO["search"]}<input type="search" id="nw-q" autocomplete="off" aria-controls="nw-res"></label>
  <div class="nw-res" id="nw-res" role="listbox" hidden></div>
</div>
<p class="nt-lbl">{L("Waar zit welke kat? Kies een soort:", "Where is which cat? Choose a species:")}</p>
<div class="nt-cats" id="nt-cats" role="group"></div>
<p class="nt-spinfo" id="nt-spinfo" hidden></p>
<div class="nt-grid">
  <div class="nt-mapcol"><div id="nt-kaart"></div><div class="nt-types" id="nt-types" role="group"></div></div>
  <div class="nt-side"><div id="nt-sel"></div><div class="nt-beeld" id="nt-beeld"></div></div>
</div>
</div>
<div class="nw-sbar" id="nw-sbar"><button type="button" class="nw-back">{ICO["back"]}{L("Terug", "Back")}</button><h2 class="nw-stitle" id="nw-stitle"></h2></div>
"""

EXTRA = f"""
<section id="tabel"><h2>{L("Hoofdtabel", "Main table")}</h2></section>
<section id="favorieten"><h2>{L("Favorieten", "Favourites")}</h2><div id="nw-favs"></div></section>
<section id="meer"><h2>{L("Meer", "More")}</h2><div id="nw-meer"></div></section>
"""

BAR = f"""
<div class="nw-bar nt-bar"><nav aria-label="Menu">
  <a href="#start" data-nw="start">{ICO["b-map"]}{L("Kaart", "Map")}</a>
  <a href="#soorten" data-nw="soorten">{ICO["b-paw"]}{L("Soorten", "Species")}</a>
  <a href="#locaties" data-nw="locaties">{ICO["b-pin"]}{L("Locaties", "Locations")}</a>
  <a href="#meer" data-nw="meer">{ICO["b-menu"]}{L("Meer", "More")}</a>
</nav></div>
"""

CSS = r"""
<style id="nt-css">
/* ---- testontwerp (bron/test_ontwerp.py) ---- */
.nt-weg{display:none!important}
.nt-bar nav{grid-template-columns:repeat(4,minmax(0,1fr))}
/* kop zoals op de hoofdpagina: titel, ondertitel, één regel met aantallen */
.nt-kop{margin:18px 0 0}
.nt-kop .nw-htxt{padding:0}
.nt-kop h1.mast.hs-kop{margin:0!important;font-size:clamp(1.8rem,7.6vw,2.6rem)!important}
.nt-kop .hs-onder{margin:4px 0 0!important;font-size:1.05rem!important}
.nt-meta{display:flex;flex-wrap:wrap;align-items:baseline;gap:2px 14px;margin-top:10px}
.nt-meta .nw-stats{display:flex;flex-wrap:wrap;gap:2px 14px;margin:0;padding:0;border:0}
.nt-meta .nw-stats a{display:inline;font:600 .86rem var(--hs-label);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);text-decoration:none}
.nt-meta .nw-stats a strong{font:inherit;color:var(--ink)}
.nt-meta .nw-datum{padding:0}
.nt-meta .nw-datum .stamp.hs-stamp{font:600 .86rem var(--hs-label)!important;letter-spacing:.06em!important;text-transform:uppercase!important;color:var(--muted)!important}
/* zoeken: klapt open via het vergrootglas bovenaan, zoals op de hoofdpagina */
#start .nw-search{display:none}
html.nt-zoek #start .nw-search{display:block}
/* soortrondjes */
.nt-lbl{font:600 .8rem var(--hs-label);letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin:18px 0 6px}
.nt-cats{display:flex;gap:4px;overflow-x:auto;margin:0 -16px 6px;padding:2px 16px 8px;scrollbar-width:none;scroll-snap-type:x proximity}
.nt-cats::-webkit-scrollbar{display:none}
.nt-cat{all:unset;box-sizing:border-box;flex:none;width:78px;display:flex;flex-direction:column;align-items:center;gap:5px;padding:6px 2px 7px;border-radius:12px;cursor:pointer;font:500 .8rem/1.15 var(--hs-body);text-align:center;color:var(--ink);scroll-snap-align:start}
.nt-av{width:56px;height:56px;border-radius:50%;overflow:hidden;border:2px solid var(--line);background:var(--nw-sage);display:flex;align-items:center;justify-content:center;flex:none}
.nt-av img{width:100%;height:100%;object-fit:cover;display:block}
.nt-av.nt-all{background:var(--nw-green);border-color:var(--nw-green);color:#FBF8F1;font:600 1.1rem var(--hs-label)}
.nt-cat[aria-pressed="true"]{background:color-mix(in srgb,var(--nw-green) 13%,transparent);font-weight:700}
.nt-cat[aria-pressed="true"] .nt-av{border-color:var(--nw-green);box-shadow:0 0 0 2px var(--nw-green)}
.nt-cat:focus-visible{outline:2px solid var(--nw-terra);outline-offset:1px}
.nt-spinfo{margin:0 0 10px;font-size:1rem;color:var(--ink)}
.nt-spinfo a{color:var(--nw-terra);font-weight:600;text-decoration:none;white-space:nowrap}
/* kaart en lijst */
.nt-grid{display:grid;gap:14px;grid-template-columns:minmax(0,1fr);align-items:start}
#nt-kaart .map{margin:0}
#start .hs-lgt{display:none!important}
.nt-types{display:flex;gap:6px;overflow-x:auto;margin:0 -16px;padding:8px 16px 2px;scrollbar-width:none}
.nt-types::-webkit-scrollbar,#lt-bar::-webkit-scrollbar{display:none}
.nt-types .lt-chip,#lt-bar .lt-chip{flex:none;white-space:nowrap}
#lt-bar{flex-wrap:nowrap!important;overflow-x:auto;margin:0 -16px 6px!important;padding:2px 16px 4px;scrollbar-width:none}
#nt-sel .mapinfo{border-radius:14px;min-height:0}
#nt-sel .mapinfo:has(> .empty){background:none;border:0;padding:0 2px}
#nt-sel .mapinfo .empty{font-size:.95rem}
.nt-beeld,.nt-box{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px 16px 10px;box-shadow:var(--nw-shadow)}
.nt-beeld h3{margin:0;font:800 1.25rem var(--hs-display);color:var(--ink)}
.nt-note{margin:2px 0 6px;color:var(--muted);font-size:.92rem}
.nt-list{list-style:none;margin:0;padding:0}
.nt-loc{position:relative;display:grid;grid-template-columns:30px minmax(0,1fr) auto;gap:2px 12px;align-items:center;padding:11px 0;border-top:1px solid var(--line);margin:0}
.nt-loc:first-child{border-top:0}
.nt-ti svg{width:30px;height:30px;display:block}
.nt-lt{min-width:0}
.nt-lt a{font:700 1.05rem/1.25 var(--hs-body);color:var(--ink);text-decoration:none}
.nt-lt a::after{content:"";position:absolute;inset:0}
.nt-lt a:focus-visible{outline:none}
.nt-loc:focus-within{outline:2px solid var(--nw-terra);outline-offset:2px;border-radius:8px}
.nt-lt small{display:block;color:var(--muted);font-size:.9rem;line-height:1.35}
.nt-ds{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;color:var(--muted);font-size:.9rem;line-height:1.4;margin-top:3px}
.nt-n{font:600 .88rem var(--hs-label);letter-spacing:.03em;color:var(--muted);white-space:nowrap;text-align:right;align-self:start;padding-top:2px}
.nt-n b{font:800 1.15rem var(--hs-display);color:var(--ink)}
.nt-full .nt-loc{grid-template-columns:30px minmax(0,1fr) auto;align-items:start}
.nt-full .nt-ti{padding-top:2px}
.nt-more{all:unset;box-sizing:border-box;cursor:pointer;display:inline-block;margin:6px 0 6px;padding:8px 16px;border:1px solid var(--line);border-radius:99px;background:var(--paper);font:600 .95rem var(--hs-body);color:var(--ink)}
.nt-more:focus-visible{outline:2px solid var(--nw-terra)}
.nt-uitl{margin:14px 2px 0;color:var(--muted);font-size:.92rem;line-height:1.5}
.map .mk.nt-uit{display:none}
/* "Aanwezig" is de gewone stand: alleen afwijkingen tonen (niet in de hoofdtabel, daar is het een kolom) */
#mapinfo .st-g,#info .st-g{display:none!important}
/* soorten: fotokaartjes zoals op de hoofdpagina */
#soorten .hint,#soorten .legend-mini{display:none!important}
.chips[data-group]>.chip{display:none!important}
.chips[data-group]:not([hidden]){display:block!important}
.nt-spg{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;margin:6px 0 18px}
.nt-sc{display:flex;flex-direction:column;text-decoration:none;background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;color:var(--ink);box-shadow:var(--nw-shadow)}
.nt-sc .ph{aspect-ratio:4/3;background:var(--nw-sage);overflow:hidden}
.nt-sc img{width:100%;height:100%;object-fit:cover;display:block}
.nt-sc .bd{padding:8px 11px 11px;display:flex;flex-direction:column;gap:2px}
.nt-sc .nm{font:700 1.06rem/1.15 var(--hs-display)}
.nt-sc small{font-size:.86rem;color:var(--muted)}
.nt-sc.nt-uns{border-style:dashed}
.nt-sc:focus-visible{outline:2px solid var(--nw-terra);outline-offset:2px}
.nt-link{display:flex;align-items:center;gap:12px;margin:8px 0 0;padding:14px 16px;border-radius:16px;border:1px solid var(--line);background:var(--card);color:var(--ink);text-decoration:none;font-weight:600;box-shadow:var(--nw-shadow)}
.nt-link svg{width:22px;height:22px;flex:none;color:var(--nw-terra)}
.nt-link .nw-arr{margin-left:auto;color:var(--muted)}
.nt-uitleg-h{margin-top:28px!important}
/* bij openen via een adres met # niet onder de vaste balken terechtkomen */
#main>section,#main>.board{scroll-margin-top:calc(var(--nw-top) + 70px)}
@media (min-width:900px){
  .nt-kop{margin-top:22px}
  .nt-cats,.nt-types,#lt-bar{margin-left:0!important;margin-right:0!important;padding-left:2px;padding-right:2px}
  .nt-grid{grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:18px}
  .nt-side{position:sticky;top:calc(var(--nw-top) + 14px)}
  .nt-spg{grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:16px}
}
</style>
"""

JS = r"""
<script>
(function(){
/* testontwerp (bron/test_ontwerp.py): kaart als startscherm, fotokaartjes per soort, één lijst met locaties */
var N=window.__NT,H=window.__HST||{};if(!N)return;
var R=N.R,LOCS=N.LOCS,PH=N.PHOTOS||{};
var $=function(s,r){return (r||document).querySelector(s);},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));};
function E(s){return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});}
function LS(nl,en){return '<span class="l-nl">'+nl+'</span><span class="l-en">'+en+'</span>';}
var ARR='ARRSVG',ROWS='ROWSSVG';
var html=document.documentElement;

/* soorten per locatie en locaties per soort (zelfde koppeling als de gids: naam in LOCS[i][4]) */
var LSP=[],SPL={};
LOCS.forEach(function(l,i){var s={};R.forEach(function(r){if(l[4].indexOf(r[2])>=0)s[r[0]]=1;});LSP[i]=Object.keys(s);
  LSP[i].forEach(function(sp){(SPL[sp]=SPL[sp]||[]).push(i);});});
function tk(nm){var k=H.loc?H.loc[nm]:undefined;return k===undefined?-1:k;}
function tnl(i){var k=tk(LOCS[i][0]);return k<0||!H.nm?"":H.nm.nl[k];}
function tnaam(k){if(k<0||!H.nm)return "";return (H.nm[N.lang()]||H.nm.nl)[k]||"";}
function ico(k){var c=k<0||!H.col?"#8B8676":H.col[k];return '<svg viewBox="-8 -8 16 16" aria-hidden="true" style="color:'+c+'"><circle r="8" fill="currentColor"/><g fill="#F0EEE2" style="color:#F0EEE2">'+(k<0||!H.gly?'<circle r="2"/>':H.gly[k])+'</g></svg>';}
function nsoort(n){return n===1?LS("soort","species"):LS("soorten","species");}
function nloc(n){return n===1?LS("locatie","location"):LS("locaties","locations");}

/* beschrijving per locatie uit de lijst van de gids */
var DS={};
function leesDS(){$$("#locaties .loclist.cards li").forEach(function(li){var a=li.querySelector('a[href^="#locatie/"]');if(!a)return;
  var s=a.getAttribute("href").slice(9),o="";$$(":scope > span.l-nl, :scope > span.l-en",li).forEach(function(x){o+=x.outerHTML;});DS[s]=o;});}

var SP=null,MEER=false;
function typ(){var b=$('#lt-bar [aria-pressed="true"]');return b?b.dataset.t:"";}
function lijst(sp){var t=typ();return LOCS.map(function(l,i){return i;}).filter(function(i){return (!sp||LSP[i].indexOf(sp)>=0)&&(!t||tnl(i)===t);})
  .sort(function(a,b){return LSP[b].length-LSP[a].length||LOCS[a][0].localeCompare(LOCS[b][0]);});}
function kaart(i,lang){var l=LOCS[i],nm=l[0],k=tk(nm),s=N.lslug(nm),n=LSP[i].length,d=lang&&DS[s];
  return '<li class="nt-loc"><span class="nt-ti">'+ico(k)+'</span><span class="nt-lt"><a href="#locatie/'+s+'">'+E(nm)+'</a><small>'+E(l[1])+(k>=0?' · '+E(tnaam(k)):"")+'</small>'+
    (d?'<span class="nt-ds">'+d+'</span>':"")+'</span><span class="nt-n"><b>'+n+'</b> '+nsoort(n)+'</span></li>';}

/* ---------- kaart (startscherm) ---------- */
function cats(){var el=$("#nt-cats");if(!el)return;
  var all=N.BIG.concat(N.SMALL).filter(function(s){return SPL[s];}).sort(function(a,b){return N.spName(a).localeCompare(N.spName(b));});
  el.innerHTML='<button type="button" class="nt-cat" data-sp="" aria-pressed="'+(!SP)+'"><span class="nt-av nt-all">'+all.length+'</span><span>'+LS("Alle katten","All cats")+'</span></button>'+
    all.map(function(s){var p=PH[s]&&PH[s].src;return '<button type="button" class="nt-cat" data-sp="'+E(s)+'" aria-pressed="'+(SP===s)+'"><span class="nt-av">'+(p?'<img src="'+E(p)+'" alt="" loading="lazy">':"")+'</span><span>'+E(N.spName(s))+'</span></button>';}).join("");
  el.setAttribute("aria-label",N.lang()==="nl"?"Kies een soort":"Choose a species");}
function spinfo(){var el=$("#nt-spinfo");if(!el)return;if(!SP){el.hidden=true;el.innerHTML="";return;}var n=(SPL[SP]||[]).length;
  el.innerHTML='<b>'+E(N.spName(SP))+'</b> · '+n+' '+nloc(n)+' · <a href="#soort/'+N.slug(SP)+'">'+LS("Meer over deze soort","More about this species")+' →</a>';el.hidden=false;}
function filt(){var set=SP?SPL[SP]||[]:null;$$("#nlmap .mk").forEach(function(m){var i=+m.dataset.i;m.classList.toggle("nt-uit",!!set&&set.indexOf(i)<0);});}
function beeld(){var el=$("#nt-beeld");if(!el)return;var ids=lijst(SP),n=ids.length,show=MEER?ids:ids.slice(0,5);
  el.innerHTML='<h3>'+LS("In beeld","On the map")+': '+n+' '+nloc(n)+'</h3><p class="nt-note">'+LS("Meeste soorten eerst. Tik op een naam voor de katten en bezoekinformatie.","Most species first. Tap a name for its cats and visitor information.")+'</p>'+
    '<ul class="nt-list">'+show.map(function(i){return kaart(i,false);}).join("")+'</ul>'+
    (n>5&&!MEER?'<button type="button" class="nt-more" id="nt-more">'+LS("Toon alle","Show all")+' ('+n+')</button>':"");}
document.addEventListener("click",function(e){
  var c=e.target.closest&&e.target.closest(".nt-cat");
  if(c){SP=c.dataset.sp||null;MEER=false;cats();spinfo();filt();beeld();return;}
  if(e.target.closest&&e.target.closest("#nt-more")){MEER=true;beeld();return;}
  var t=e.target.closest&&e.target.closest("#nt-types .lt-chip");
  if(t){var o=$$("#lt-bar .lt-chip").filter(function(b){return b.dataset.t===t.dataset.t;})[0];if(o)o.click();}});
function types(){var bar=$("#lt-bar"),el=$("#nt-types");if(!bar||!el)return;el.innerHTML=bar.innerHTML;el.setAttribute("aria-label",bar.getAttribute("aria-label")||"");}

/* ---------- locaties ---------- */
function locs(){var el=$("#nt-loclist");if(!el)return;el.innerHTML=lijst(null).map(function(i){return kaart(i,true);}).join("");}

/* ---------- soorten ---------- */
function spgrid(){$$(".chips[data-group]").forEach(function(box){var g=box.querySelector(":scope > .nt-spg");if(!g){g=document.createElement("div");g.className="nt-spg";box.appendChild(g);}
  g.innerHTML=$$(":scope > .chip[data-sp]",box).map(function(c){var sp=c.dataset.sp,p=PH[sp]&&PH[sp].src,n=N.locCount(sp);
    return '<a class="nt-sc'+(N.UNSURE.has(sp)?" nt-uns":"")+'" href="#soort/'+N.slug(sp)+'"><span class="ph">'+(p?'<img src="'+E(p)+'" alt="" loading="lazy">':"")+'</span><span class="bd"><span class="nm">'+E(N.spName(sp))+'</span><small>'+n+' '+nloc(n)+'</small></span></a>';}).join("");});}

function alles(){cats();spinfo();filt();beeld();types();locs();spgrid();}

/* ---------- opbouw: wachten tot de gids en de huisstijl klaar zijn ---------- */
var klaar=false;
function opbouw(){if(klaar)return true;
  var map=$("#locaties .mapwrap .map"),reg=$("#soorten .hs-reg"),bar=$("#lt-bar");
  if(!map||!reg||!bar||!$("#nlmap .mk")||!$(".chips[data-group] .chip"))return false;klaar=true;
  var loc=$("#locaties"),lb=$("#locaties > .cbody")||loc;
  /* kaart en infovak naar het startscherm */
  $("#nt-kaart").appendChild(map);var mi=$("#mapinfo");if(mi)$("#nt-sel").appendChild(mi);
  var mw=$("#locaties .mapwrap");if(mw)mw.classList.add("nt-weg");
  /* Locaties: één lijst met kaartjes; uitleg onderaan; onderzochte locaties zonder katten naar Over */
  leesDS();
  var cnt=$("#lt-count"),ul=document.createElement("div");ul.className="nt-box";ul.innerHTML='<ul class="nt-list nt-full" id="nt-loclist"></ul>';
  (cnt||bar).insertAdjacentElement("afterend",ul);
  var intro=$(":scope > p.prose",lb);if(intro){intro.classList.add("nt-uitl");ul.insertAdjacentElement("afterend",intro);}
  var det=$$(":scope > details",lb),ub=$("#uitleg > .cbody")||$("#uitleg");
  det.forEach(function(d,k){if(k===0){d.classList.add("nt-weg");return;}
    if(ub){if(k===1){var h=document.createElement("h3");h.className="nt-uitleg-h";h.innerHTML=LS("Onderzochte locaties zonder katten","Locations checked without cats");ub.appendChild(h);}ub.appendChild(d);}});
  /* hoofdtabel als eigen scherm */
  var tb=$("#tabel > .cbody")||$("#tabel");tb.appendChild(reg);
  var sb=$("#soorten > .cbody")||$("#soorten"),lk=document.createElement("a");lk.className="nt-link";lk.href="#tabel";
  lk.innerHTML=ROWS+'<span>'+LS("Alle vermeldingen in één tabel","All entries in one table")+'</span>'+ARR;sb.appendChild(lk);
  alles();
  new MutationObserver(function(){types();beeld();locs();}).observe(bar,{childList:true,subtree:true,attributes:true,attributeFilter:["aria-pressed"]});
  new MutationObserver(function(){leesDS();alles();}).observe(html,{attributes:true,attributeFilter:["lang"]});
  /* na een tik op de kaart het infovak in beeld brengen als het onder de rand valt */
  $("#nt-kaart").addEventListener("click",function(e){if(!e.target.closest(".mk"))return;setTimeout(function(){var m=$("#mapinfo");if(!m)return;var r=m.getBoundingClientRect();
    if(r.top>innerHeight-140)window.scrollBy({top:r.top-innerHeight+Math.min(r.height,300)+90,behavior:"smooth"});},60);});
  /* binnenkomst met een # (bijv. #soorten): bovenaan het scherm beginnen */
  if(/^#(soorten|locaties|route|actueel|kleur|uitleg|rapporteer|tldr|tabel|meer|favorieten)$/.test(location.hash))window.scrollTo(0,0);
  return true;}
if(!opbouw()){var n=0,iv=setInterval(function(){if(opbouw()||++n>80)clearInterval(iv);},100);}

/* zoeken klapt open via het vergrootglas bovenaan */
var q=$("#nw-q"),tz=$('.hs-top a.hs-ico[href="#start"]')||$('.hs-top a.hs-ico[href$="#zoek"]');
if(tz)tz.addEventListener("click",function(){html.classList.add("nt-zoek");});
if(q)q.addEventListener("blur",function(){setTimeout(function(){if(!q.value&&document.activeElement!==q)html.classList.remove("nt-zoek");},200);});
})();
</script>
"""


def maak():
    bron = os.path.join(ROOT, BRON, "index.html")
    doel = os.path.join(ROOT, DOEL, "index.html")
    doc = open(bron, encoding="utf-8").read()
    assert NO.MARK not in doc, "bron heeft al het app-ontwerp"

    def sub1(t, a, b):
        assert a in t, f"niet gevonden: {a[:60]}"
        return t.replace(a, b, 1)

    if '<meta name="robots"' not in doc:
        doc = sub1(doc, "</head>", '<meta name="robots" content="noindex">\n</head>')
    doc = doc.replace("<title>", "<title>TEST · ", 1)
    doc = sub1(doc, "</head>", NO.CSS + CSS + "</head>")
    doc = sub1(doc, '<div class="wrap" id="main">', '<div class="wrap" id="main">\n' + START)
    doc = sub1(doc, '<section id="rapporteer"', EXTRA + '<section id="rapporteer"')
    exp = ('window.__NW={R:R,LOCS:LOCS,SPECIES:SPECIES,SPEN:SPEN,BYSLUG:BYSLUG,LOCBYSLUG:LOCBYSLUG,slug:slug,lslug:lslug,'
           'lang:function(){return LANG;}};\n'
           'window.__NT={R:R,LOCS:LOCS,PHOTOS:PHOTOS,BIG:BIG,SMALL:SMALL,UNSURE:UNSURE,spName:spName,slug:slug,lslug:lslug,'
           'locCount:locCount,lang:function(){return LANG;}};\n')
    a = doc.index("const SPECIES=[")
    e = doc.index("})();\n</script>", a)
    doc = doc[:e] + exp + doc[e:]

    # het script van nieuw_ontwerp, met de indeling van dit testontwerp
    js = NO.JS

    def rep(t, a, b):
        assert a in t, f"niet gevonden in JS: {a[:70]}"
        return t.replace(a, b, 1)

    js = rep(js, 'var SCR=["tldr","locaties","soorten","route","actueel","kleur","uitleg","rapporteer","favorieten","meer"];',
             'var SCR=["tldr","locaties","soorten","route","actueel","kleur","uitleg","rapporteer","favorieten","meer","tabel"];')
    naam = {k: L(*v) for k, v in {"soorten": ("Soorten", "Species"), "locaties": ("Locaties", "Locations"),
                                  "locaties-kop": ("Locaties", "Locations")}.items()}
    js = rep(js, "function naam(id){", "var NTN=" + json.dumps(naam, ensure_ascii=False) + ";\nfunction naam(id){if(NTN[id])return NTN[id];")
    js = rep(js, 'var ic={favorieten:"b-heart",tldr:"tbl",actueel:"news",kleur:"dna",uitleg:"info",rapporteer:"flag"};',
             'var ic={route:"b-route",actueel:"news",tldr:"tbl",kleur:"dna",favorieten:"b-heart",tabel:"rows",uitleg:"info",rapporteer:"flag"};')
    js = rep(js, 'var own=["favorieten","tldr","actueel","kleur","uitleg","rapporteer"]',
             'var own=["route","actueel","tldr","kleur","favorieten","tabel","uitleg","rapporteer"]')
    js = rep(js, 'mark(["locaties","soorten","route"].indexOf(sc.id)>=0?sc.id:"meer");',
             'mark(["locaties","soorten"].indexOf(sc.id)>=0?sc.id:"meer");')
    # de keuzeknoppen voor de filters bij Locaties niet: hier blijven de typeknoppen zichtbaar
    a = js.index("/* ---------- filters bij Locaties")
    b = js.index("paint();apply();", a)
    js = js[:a] + js[b:]
    svg = "{" + ",".join(f'"{k}":{v!r}' for k, v in ICO.items()) + "}"
    js = (js.replace("HEARTSVG", NO.HEART_S).replace("PAWSVG", ICO["b-paw"]).replace("PINSVG", ICO["b-map"])
          .replace("ARRSVG", NO.ARROW).replace("var $=function", "var SVG=" + svg + ";\nvar TRX=" + json.dumps(NO.TR, ensure_ascii=False) + ";\nvar $=function", 1))
    js_t = JS.replace("ARRSVG", NO.ARROW).replace("ROWSSVG", ICO["rows"])
    i = doc.rindex("</body>")
    doc = doc[:i] + BAR + js + js_t + doc[i:]
    os.makedirs(os.path.dirname(doel), exist_ok=True)
    open(doel, "w", encoding="utf-8").write(doc)
    print("testontwerp geschreven:", DOEL + "/index.html")


if __name__ == "__main__":
    maak()
