"""Ontwerp van de landpagina's (18-10-2026; eerst getest op /nederland-test/, nu op alle landen in LIVE).

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
Terugdraaien: dit bestand en de regels onderaan bouw.py weghalen en opnieuw bouwen (dan geldt weer nieuw_ontwerp.py).
"""
import json
import os
import re

import nieuw_ontwerp as NO

ROOT = NO.ROOT
BRON = "nederland-oud"
DOEL = "nederland-test"
# Teksten die dit ontwerp zelf toevoegt, in de talen van de gidsen (Frans met "vous", de rest met "du/tu").
TR = dict(NO.TR)
TR.update({
    "Waar zit welke kat? Kies een soort:": {"fr": "Quel félin vit où ? Choisissez une espèce :", "de": "Welche Katze lebt wo? Wähle eine Art:",
                                            "it": "Quale felino vive dove? Scegli una specie:", "es": "¿Qué felino vive dónde? Elige una especie:",
                                            "pt": "Que felino vive onde? Escolhe uma espécie:"},
    "Hoofdtabel": {"fr": "Tableau principal", "de": "Haupttabelle", "it": "Tabella principale", "es": "Tabla principal", "pt": "Tabela principal"},
    "Kaart": {"fr": "Carte", "de": "Karte", "it": "Mappa", "es": "Mapa", "pt": "Mapa"},
    "Soorten": {"fr": "Espèces", "de": "Arten", "it": "Specie", "es": "Especies", "pt": "Espécies"},
    "Locaties": {"fr": "Lieux", "de": "Orte", "it": "Luoghi", "es": "Lugares", "pt": "Locais"},
    "Alle katten": {"fr": "Tous les félins", "de": "Alle Katzen", "it": "Tutti i felini", "es": "Todos los felinos", "pt": "Todos os felinos"},
    "Meer over deze soort": {"fr": "En savoir plus sur cette espèce", "de": "Mehr über diese Art", "it": "Di più su questa specie",
                             "es": "Más sobre esta especie", "pt": "Mais sobre esta espécie"},
    "In beeld": {"fr": "Sur la carte", "de": "Im Bild", "it": "Sulla mappa", "es": "En el mapa", "pt": "No mapa"},
    "Meeste soorten eerst. Tik op een naam voor de katten en bezoekinformatie.": {
        "fr": "Les lieux avec le plus d’espèces d’abord. Touchez un nom pour voir ses félins et les infos de visite.",
        "de": "Die meisten Arten zuerst. Tippe auf einen Namen für die Katzen und Besucherinfos.",
        "it": "Prima i luoghi con più specie. Tocca un nome per i felini e le informazioni per la visita.",
        "es": "Primero los lugares con más especies. Toca un nombre para ver sus felinos y la información de visita.",
        "pt": "Primeiro os locais com mais espécies. Toca num nome para ver os felinos e a informação de visita."},
    "Toon alle": {"fr": "Tout afficher", "de": "Alle zeigen", "it": "Mostra tutti", "es": "Mostrar todos", "pt": "Mostrar todos"},
    "Onderzochte locaties": {"fr": "Lieux vérifiés", "de": "Geprüfte Orte", "it": "Luoghi verificati", "es": "Lugares comprobados", "pt": "Locais verificados"},
    "Alle vermeldingen in één tabel": {"fr": "Toutes les mentions dans un tableau", "de": "Alle Einträge in einer Tabelle",
                                       "it": "Tutte le segnalazioni in una tabella", "es": "Todas las menciones en una tabla", "pt": "Todas as menções numa tabela"},
    "Kies een soort": {"fr": "Choisissez une espèce", "de": "Wähle eine Art", "it": "Scegli una specie", "es": "Elige una especie", "pt": "Escolhe uma espécie"},
})


def L(nl, en):
    t = TR.get(nl, {})
    return (f'<span class="l-nl">{nl}</span><span class="l-en">{en}</span>'
            + "".join(f'<span class="l-{x}">{t.get(x, en)}</span>' for x in NO.TALEN))

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
<div class="nt-rgw" id="nt-rgw" hidden><p class="nt-lbl" id="nt-rglab"></p><div class="nt-regs" id="nt-regs" role="group"></div></div>
<p class="nt-lbl">{L("Waar zit welke kat? Kies een soort:", "Which cat lives where? Choose a species:")}</p>
<div class="nt-cats" id="nt-cats" role="group"></div>
<p class="nt-mld" id="nt-mld" role="status" hidden></p>
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
.nt-av.nt-avu{border-style:dashed;border-color:var(--muted)}
.nt-av.nt-all{background:var(--nw-green);border-color:var(--nw-green);color:#FBF8F1;font:600 1.1rem var(--hs-label)}
.nt-cat[aria-pressed="true"]{background:color-mix(in srgb,var(--nw-green) 13%,transparent);font-weight:700}
.nt-cat[aria-pressed="true"] .nt-av{border-color:var(--nw-green);box-shadow:0 0 0 2px var(--nw-green)}
.nt-cat:focus-visible{outline:2px solid var(--nw-terra);outline-offset:1px}
.nt-grijs{opacity:.42}
.nt-grijs .nt-av,.nt-grijs svg{filter:grayscale(1)}
.nt-sep{flex:none;width:1px;align-self:stretch;margin:8px 4px;background:var(--line)}
.nt-mld{margin:0 0 10px;padding:8px 12px;border-radius:12px;background:var(--nw-peach);color:var(--ink);font-size:.95rem}
.nt-spinfo{margin:0 0 10px;font-size:1rem;color:var(--ink)}
.nt-spinfo a{color:var(--nw-terra);font-weight:600;text-decoration:none;white-space:nowrap}
/* kaart en lijst */
.nt-grid{display:grid;gap:14px;grid-template-columns:minmax(0,1fr);align-items:start}
#nt-kaart .map{margin:0}
#start .hs-lgt{display:none!important}
.nt-types{display:flex;gap:6px;overflow-x:auto;margin:0 -16px;padding:8px 16px 2px;scrollbar-width:none}
.nt-types::-webkit-scrollbar,#lt-bar::-webkit-scrollbar{display:none}
.nt-types .lt-chip,#lt-bar .lt-chip,.nt-regs .rg-chip,#rg-bar .rg-chip{flex:none;white-space:nowrap}
#lt-bar,#rg-bar{flex-wrap:nowrap!important;overflow-x:auto;margin:0 -16px 6px!important;padding:2px 16px 4px;scrollbar-width:none}
#rg-bar::-webkit-scrollbar,.nt-regs::-webkit-scrollbar{display:none}
.nt-regs{display:flex;gap:6px;overflow-x:auto;margin:0 -16px;padding:2px 16px 2px;scrollbar-width:none}
.nt-rgw .nt-lbl{margin-top:16px}
.nt-regs .rg-chip,.nt-types .lt-chip{font-size:.92rem}
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
  .nt-cats,.nt-types,.nt-regs,#lt-bar,#rg-bar{margin-left:0!important;margin-right:0!important;padding-left:2px;padding-right:2px}
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
function LS(nl,en){var t=T2[nl]||{},o='<span class="l-nl">'+nl+'</span><span class="l-en">'+en+'</span>';["fr","de","it","es","pt"].forEach(function(x){o+='<span class="l-'+x+'">'+(t[x]||en)+'</span>';});return o;}
function TX(nl,en){var t=T2[nl]||{},l=N.lang();return l==="nl"?nl:l==="en"?en:(t[l]||en);}
var ARR='ARRSVG',ROWS='ROWSSVG',T2=T2JSON;
var html=document.documentElement;

/* soorten per locatie en locaties per soort (zelfde koppeling als de gids: naam in LOCS[i][4]) */
var LSP=[],SPL={};
LOCS.forEach(function(l,i){var s={};R.forEach(function(r){if(l[4].indexOf(r[2])>=0)s[r[0]]=1;});LSP[i]=Object.keys(s);
  LSP[i].forEach(function(sp){(SPL[sp]=SPL[sp]||[]).push(i);});});
/* soorten zonder enige bevestigde vermelding (alleen onzeker of gepland): stippellijn */
var BEV={};R.forEach(function(r){if(String(r[4]).split("+").some(function(c){return "gybrn".indexOf(c)>=0&&c;}))BEV[r[0]]=1;});
function onz(sp){return !BEV[sp];}
function tk(nm){var k=H.loc?H.loc[nm]:undefined;return k===undefined?-1:k;}
function tnl(i){var k=tk(LOCS[i][0]);return k<0||!H.nm?"":H.nm.nl[k];}
function tnaam(k){if(k<0||!H.nm)return "";return (H.nm[N.lang()]||H.nm.en||H.nm.nl)[k]||"";}
function ico(k){var c=k<0||!H.col?"#8B8676":H.col[k];return '<svg viewBox="-8 -8 16 16" aria-hidden="true" style="color:'+c+'"><circle r="8" fill="currentColor"/><g fill="#F0EEE2" style="color:#F0EEE2">'+(k<0||!H.gly?'<circle r="2"/>':H.gly[k])+'</g></svg>';}
function nsoort(n){return n===1?LS("soort","species"):LS("soorten","species");}
function nloc(n){return n===1?LS("locatie","location"):LS("locaties","locations");}

/* beschrijving per locatie uit de lijst van de gids */
var DS={};
function leesDS(){$$("#locaties .loclist.cards li").forEach(function(li){var a=li.querySelector('a[href^="#locatie/"]');if(!a)return;
  var s=a.getAttribute("href").slice(9),o="";$$(":scope > span[class^='l-']",li).forEach(function(x){o+=x.outerHTML;});DS[s]=o;});}

var SP=null,MEER=false;
function typ(){var b=$('#lt-bar [aria-pressed="true"]');return b?b.dataset.t:"";}
function reg(){var b=$('#rg-bar [aria-pressed="true"]');return b&&N.REGIO?b.dataset.r:"";}
function inReg(i,r){return N.REGIO&&N.REGIO[LOCS[i][0]]===r;}
/* melding als een grijze knop het andere filter uitzet */
var MLD={nl:["{k}: niet te zien in {p}.","Het filter op regio staat nu uit.","Het filter op soort staat nu uit."],
  en:["{k}: not on view in {p}.","The region filter is now off.","The species filter is now off."],
  fr:["{k} : pas visible ici ({p}).","Le filtre par région est désactivé.","Le filtre par espèce est désactivé."],
  de:["{k}: in {p} nicht zu sehen.","Der Regionsfilter ist jetzt aus.","Der Artenfilter ist jetzt aus."],
  it:["{k}: non visibile in {p}.","Il filtro per regione è disattivato.","Il filtro per specie è disattivato."],
  es:["{k}: no se puede ver en {p}.","El filtro por región está desactivado.","El filtro por especie está desactivado."],
  pt:["{k}: não está visível em {p}.","O filtro por região está desligado.","O filtro por espécie está desligado."]};
var mldT=null;
function melding(k,p,welk){var el=$("#nt-mld");if(!el)return;var t=MLD[N.lang()]||MLD.en;
  el.textContent=t[0].replace("{k}",k).replace("{p}",p)+" "+t[welk];el.hidden=false;clearTimeout(mldT);mldT=setTimeout(function(){el.hidden=true;},6000);}
function chipNaam(b){var c=b.cloneNode(true);c.querySelectorAll(".n,svg").forEach(function(x){x.remove();});return c.textContent.trim();}
function lijst(sp){var t=typ(),r=reg();return LOCS.map(function(l,i){return i;}).filter(function(i){return (!sp||LSP[i].indexOf(sp)>=0)&&(!t||tnl(i)===t)&&(!r||N.REGIO[LOCS[i][0]]===r);})
  .sort(function(a,b){return LSP[b].length-LSP[a].length||LOCS[a][0].localeCompare(LOCS[b][0]);});}
function kaart(i,lang){var l=LOCS[i],nm=l[0],k=tk(nm),s=N.lslug(nm),n=LSP[i].length,d=lang&&DS[s];
  return '<li class="nt-loc"><span class="nt-ti">'+ico(k)+'</span><span class="nt-lt"><a href="#locatie/'+s+'">'+E(nm)+'</a><small>'+E(l[1])+(k>=0?' · '+E(tnaam(k)):"")+'</small>'+
    (d?'<span class="nt-ds">'+d+'</span>':"")+'</span><span class="nt-n"><b>'+n+'</b> '+nsoort(n)+'</span></li>';}

/* ---------- kaart (startscherm) ---------- */
function cats(){var el=$("#nt-cats");if(!el)return;
  var all=N.BIG.concat(N.SMALL).filter(function(s){return SPL[s];}).sort(function(a,b){return N.spName(a).localeCompare(N.spName(b));});
  /* met een regio gekozen: katten die daar niet zitten grijs en achteraan */
  var r=reg(),ok=function(s){return !r||(SPL[s]||[]).some(function(i){return inReg(i,r);});};
  var ja=all.filter(ok),nee=all.filter(function(s){return !ok(s);});
  var hn=$(".nw-nsp strong"),num=r?ja.filter(function(s){return !onz(s);}).length:(hn?hn.textContent:all.length);
  function knop(s,grijs){var p=PH[s]&&PH[s].src;return '<button type="button" class="nt-cat'+(grijs?" nt-grijs":"")+'" data-sp="'+E(s)+'" aria-pressed="'+(SP===s)+'"><span class="nt-av'+(onz(s)?" nt-avu":"")+'">'+(p?'<img src="'+E(p)+'" alt="" loading="lazy">':"")+'</span><span>'+E(N.spName(s))+'</span></button>';}
  el.innerHTML='<button type="button" class="nt-cat" data-sp="" aria-pressed="'+(!SP)+'"><span class="nt-av nt-all">'+num+'</span><span>'+LS("Alle katten","All cats")+'</span></button>'+
    ja.map(function(s){return knop(s,false);}).join("")+(nee.length?'<span class="nt-sep" aria-hidden="true"></span>'+nee.map(function(s){return knop(s,true);}).join(""):"");
  el.setAttribute("aria-label",TX("Kies een soort","Choose a species"));}
function spinfo(){var el=$("#nt-spinfo");if(!el)return;if(!SP){el.hidden=true;el.innerHTML="";return;}var n=(SPL[SP]||[]).length;
  el.innerHTML='<b>'+E(N.spName(SP))+'</b> · '+n+' '+nloc(n)+' · <a href="#soort/'+N.slug(SP)+'">'+LS("Meer over deze soort","More about this species")+' →</a>';el.hidden=false;}
function filt(){var set=SP?SPL[SP]||[]:null;$$("#nlmap .mk").forEach(function(m){var i=+m.dataset.i;m.classList.toggle("nt-uit",!!set&&set.indexOf(i)<0);});}
function beeld(){var el=$("#nt-beeld");if(!el)return;var ids=lijst(SP),n=ids.length,show=MEER?ids:ids.slice(0,5);
  el.innerHTML='<h3>'+LS("In beeld","On the map")+': '+n+' '+nloc(n)+'</h3><p class="nt-note">'+LS("Meeste soorten eerst. Tik op een naam voor de katten en bezoekinformatie.","Most species first. Tap a name for its cats and visitor information.")+'</p>'+
    '<ul class="nt-list">'+show.map(function(i){return kaart(i,false);}).join("")+'</ul>'+
    (n>5&&!MEER?'<button type="button" class="nt-more" id="nt-more">'+LS("Toon alle","Show all")+' ('+n+')</button>':"");}
document.addEventListener("click",function(e){
  var c=e.target.closest&&e.target.closest(".nt-cat");
  if(c&&c.classList.contains("nt-grijs")){var rb=$('#rg-bar [aria-pressed="true"]'),pn=rb?chipNaam(rb):"",al=$('#rg-bar .rg-chip[data-r=""]');
    SP=c.dataset.sp;MEER=false;if(al)al.click();cats();spinfo();filt();beeld();regs();melding(N.spName(SP),pn,1);return;}
  if(c){SP=c.dataset.sp||null;MEER=false;cats();spinfo();filt();beeld();regs();return;}
  if(e.target.closest&&e.target.closest("#nt-more")){MEER=true;beeld();return;}
  var t=e.target.closest&&e.target.closest("#nt-types .lt-chip");
  if(t){var o=$$("#lt-bar .lt-chip").filter(function(b){return b.dataset.t===t.dataset.t;})[0];if(o)o.click();return;}
  var g=e.target.closest&&e.target.closest("#nt-regs .rg-chip");
  if(g&&g.classList.contains("nt-grijs")&&SP){var kn=N.spName(SP);SP=null;MEER=false;cats();spinfo();filt();melding(kn,chipNaam(g),2);}
  if(g){var o2=$$("#rg-bar .rg-chip").filter(function(b){return b.dataset.r===g.dataset.r;})[0];if(o2)o2.click();}});
function types(){var bar=$("#lt-bar"),el=$("#nt-types");if(!el)return;if(!bar){el.hidden=true;return;}el.innerHTML=bar.innerHTML;el.setAttribute("aria-label",bar.getAttribute("aria-label")||"");}
function regs(){var bar=$("#rg-bar"),el=$("#nt-regs"),w=$("#nt-rgw");if(!bar||!el)return;w.hidden=false;el.innerHTML=bar.innerHTML;el.setAttribute("aria-label",bar.getAttribute("aria-label")||"");
  /* met een soort gekozen: regio's zonder die soort grijs en achteraan, bij de rest het aantal locaties met die soort */
  if(SP){var grijs=[];$$(".rg-chip",el).forEach(function(b){var r=b.dataset.r,n=r?(SPL[SP]||[]).filter(function(i){return inReg(i,r);}).length:(SPL[SP]||[]).length,nn=b.querySelector(".n");
      if(nn)nn.textContent=n;if(r&&!n){b.classList.add("nt-grijs");grijs.push(b);}});
    if(grijs.length){var sp=document.createElement("span");sp.className="nt-sep";sp.setAttribute("aria-hidden","true");el.appendChild(sp);grijs.forEach(function(b){el.appendChild(b);});}}
  var lab=$("#rg-lab");$("#nt-rglab").textContent=lab?lab.textContent:"";}

/* ---------- locaties ---------- */
function locs(){var el=$("#nt-loclist");if(!el)return;el.innerHTML=lijst(null).map(function(i){return kaart(i,true);}).join("");}

/* ---------- soorten ---------- */
function spgrid(){$$(".chips[data-group]").forEach(function(box){var g=box.querySelector(":scope > .nt-spg");if(!g){g=document.createElement("div");g.className="nt-spg";box.appendChild(g);}
  g.innerHTML=$$(":scope > .chip[data-sp]",box).map(function(c){var sp=c.dataset.sp,p=PH[sp]&&PH[sp].src,n=N.locCount(sp);
    return '<a class="nt-sc'+(onz(sp)?" nt-uns":"")+'" href="#soort/'+N.slug(sp)+'"><span class="ph">'+(p?'<img src="'+E(p)+'" alt="" loading="lazy">':"")+'</span><span class="bd"><span class="nm">'+E(N.spName(sp))+'</span><small>'+n+' '+nloc(n)+'</small></span></a>';}).join("");});}

function alles(){cats();spinfo();filt();beeld();types();regs();locs();spgrid();}

/* ---------- opbouw: wachten tot de gids en de huisstijl klaar zijn ---------- */
var klaar=false;
function opbouw(){if(klaar)return true;
  var map=$("#locaties .mapwrap .map"),reg=$("#soorten .hs-reg"),bar=$("#lt-bar")||$("#rg-bar");
  if(!map||!reg||!$("#nlmap .mk")||!$(".chips[data-group] .chip"))return false;klaar=true;
  var loc=$("#locaties"),lb=$("#locaties > .cbody")||loc;
  /* kaart en infovak naar het startscherm */
  $("#nt-kaart").appendChild(map);var mi=$("#mapinfo");if(mi)$("#nt-sel").appendChild(mi);
  var mw=$("#locaties .mapwrap");if(mw)mw.classList.add("nt-weg");
  /* Locaties: één lijst met kaartjes; uitleg onderaan; onderzochte locaties zonder katten naar Over */
  leesDS();
  var cnt=$("#lt-count")||$("#rg-count")||$("#lt-bar")||$("#rg-bar"),ul=document.createElement("div");ul.className="nt-box";ul.innerHTML='<ul class="nt-list nt-full" id="nt-loclist"></ul>';
  if(cnt)cnt.insertAdjacentElement("afterend",ul);else lb.insertBefore(ul,lb.firstChild);
  var intro=$(":scope > p.prose",lb);if(intro){intro.classList.add("nt-uitl");ul.insertAdjacentElement("afterend",intro);}
  /* de lijst "Met katachtigen" vervalt (de kaartjes vervangen hem); de rest (geen katten gevonden, over de lijst) naar Over */
  var det=$$("details",lb),ub=$("#uitleg > .cbody")||$("#uitleg"),weg=[];
  det.forEach(function(d){if(d.querySelector("ul.loclist.cards"))d.classList.add("nt-weg");});
  var bl=$$(".rg-blok",lb).filter(function(b){return b.parentElement===lb;});
  if(bl.length)bl.forEach(function(b){if(!$$("details:not(.nt-weg)",b).length)b.classList.add("nt-weg");weg.push(b);});
  else det.forEach(function(d){if(!d.classList.contains("nt-weg"))weg.push(d);else if(d.parentElement===lb)weg.push(d);});
  if(ub&&weg.some(function(x){return !x.classList.contains("nt-weg");})){var h=document.createElement("h3");h.className="nt-uitleg-h";h.innerHTML=LS("Onderzochte locaties","Locations checked");ub.appendChild(h);}
  if(ub)weg.forEach(function(x){ub.appendChild(x);});
  /* hoofdtabel als eigen scherm */
  var tb=$("#tabel > .cbody")||$("#tabel");tb.appendChild(reg);
  var sb=$("#soorten > .cbody")||$("#soorten"),lk=document.createElement("a");lk.className="nt-link";lk.href="#tabel";
  lk.innerHTML=ROWS+'<span>'+LS("Alle vermeldingen in één tabel","All entries in one table")+'</span>'+ARR;sb.appendChild(lk);
  alles();
  ["lt-bar","rg-bar"].forEach(function(id){var b=document.getElementById(id);if(b)new MutationObserver(function(){types();regs();cats();beeld();locs();}).observe(b,{childList:true,subtree:true,attributes:true,attributeFilter:["aria-pressed"]});});
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


def maak(land="nederland", map=None):
    """Schrijft het ontwerp van /<land>-oud/ naar /<map>/ (standaard /<land>/; map DOEL = de testpagina)."""
    map = map or land
    test = map == DOEL
    bron = os.path.join(ROOT, land + "-oud", "index.html")
    doel = os.path.join(ROOT, map, "index.html")
    doc = open(bron, encoding="utf-8").read()
    assert NO.MARK not in doc, "bron heeft al het app-ontwerp"

    def sub1(t, a, b):
        assert a in t, f"niet gevonden: {a[:60]}"
        return t.replace(a, b, 1)

    if test:
        if '<meta name="robots"' not in doc:
            doc = sub1(doc, "</head>", '<meta name="robots" content="noindex">\n</head>')
        doc = doc.replace("<title>", "<title>TEST · ", 1)
    else:
        doc = doc.replace('<meta name="robots" content="noindex">\n', "", 1)
    doc = sub1(doc, "</head>", NO.CSS + CSS + "</head>")
    doc = sub1(doc, '<div class="wrap" id="main">', '<div class="wrap" id="main">\n' + START)
    doc = sub1(doc, '<section id="rapporteer"', EXTRA + '<section id="rapporteer"')
    exp = ('window.__NW={R:R,LOCS:LOCS,SPECIES:SPECIES,SPEN:SPEN,BYSLUG:BYSLUG,LOCBYSLUG:LOCBYSLUG,slug:slug,lslug:lslug,'
           'lang:function(){return LANG;}};\n'
           'window.__NT={R:R,LOCS:LOCS,PHOTOS:PHOTOS,BIG:BIG,SMALL:SMALL,UNSURE:UNSURE,spName:spName,slug:slug,lslug:lslug,'
           'locCount:locCount,REGIO:REGIOX,lang:function(){return LANG;}};\n')
    a = doc.index("const SPECIES=[")
    e = doc.index("})();\n</script>", a)
    exp = exp.replace("REGIOX", "REGIO" if re.search(r"(const|let|var)\s+REGIO\b", doc[a:e]) else "null")
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
    js_t = (JS.replace("ARRSVG", NO.ARROW).replace("ROWSSVG", ICO["rows"])
            .replace("T2JSON", json.dumps(TR, ensure_ascii=False)))
    i = doc.rindex("</body>")
    doc = doc[:i] + BAR + js + js_t + doc[i:]
    os.makedirs(os.path.dirname(doel), exist_ok=True)
    open(doel, "w", encoding="utf-8").write(doc)
    print("testontwerp geschreven:", map + "/index.html")


LIVE = ["nederland", "belgie", "luxemburg", "duitsland", "frankrijk", "oostenrijk", "zwitserland",
        "verenigd-koninkrijk", "italie", "spanje", "ierland", "portugal"]   # landen met dit ontwerp (18-10-2026: alle)


def maak_alles():
    for land in LIVE:
        maak(land)
    maak_los2()
    maak_europa()





# ------------------------------------------------------------------ losse park- en soortpagina's (18-10-2026)
# Zelfde onderbalk als de landpagina's (Kaart · Soorten · Locaties · Meer) en "Aanwezig" alleen nog in de hoofdtabel.
LOS2_MARK = 'id="nt-los-css"'
LOS2_CSS = ('<style id="nt-los-css">.nw-bar nav{grid-template-columns:repeat(4,minmax(0,1fr))}'
            '#info .st-g{display:none!important}</style>\n')


def los2(pad, land, kind):
    doc = open(pad, encoding="utf-8").read()
    if LOS2_MARK in doc or NO.LOS_MARK not in doc:
        return False
    g = NO.BASE + land + "/"
    act = "locaties" if kind == "locatie" else "soorten"
    links = [("start", g, ICO["b-map"], "Kaart"), ("soorten", g + "#soorten", ICO["b-paw"], "Soorten"),
             ("locaties", g + "#locaties", ICO["b-pin"], "Locaties"), ("meer", g + "#meer", ICO["b-menu"], "Meer")]
    bar = ('<div class="nw-bar"><nav aria-label="Menu">'
           + "".join(f'<a href="{h}"{" class=on" if k == act else ""}>{svg}<span>{t}</span></a>' for k, h, svg, t in links)
           + "</nav></div>\n")
    doc, n = re.subn(r'<div class="nw-bar"><nav aria-label="Menu">.*?</nav></div>\n', lambda m: bar, doc, count=1, flags=re.S)
    if not n:
        return False
    doc = doc.replace('<span class="nw-stitle">Per kat</span>', '<span class="nw-stitle">Soorten</span>', 1)
    doc = doc.replace("</head>", LOS2_CSS + "</head>", 1)
    open(pad, "w", encoding="utf-8").write(doc)
    return True


def maak_los2():
    n = 0
    for land in NO.LANDEN:
        for kind in ("locatie", "soort"):
            d = os.path.join(ROOT, land, kind)
            if not os.path.isdir(d):
                continue
            for s in sorted(os.listdir(d)):
                pad = os.path.join(d, s, "index.html")
                if os.path.exists(pad) and los2(pad, land, kind):
                    n += 1
    print("losse pagina's met de nieuwe onderbalk:", n)


# ------------------------------------------------------------------ hoofdpagina, soortpagina's (/soort/…) en top 10 (18-10-2026)
# Onderbalk Kaart · Landen · Soorten · Meer zonder de tabbladen erboven; korte uitleg bij de kaart; typeknoppen altijd
# zichtbaar onder de kaart; op de soortpagina's de geschatte aantallen in het wild in plaats van de IUCN-status
# en locatiekaartjes met het type-icoon bij "Waar te zien".
EU_MARK = 'id="nt-eu-css"'
ICO["b-flag"] = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
                 'stroke-linejoin="round"><path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/></svg>')
EU_CSS = r"""
<style id="nt-eu-css">
/* hoofdpagina in de opbouw van de landpagina's (bron/test_ontwerp.py) */
.bar:has(#tabs){display:none!important}
.intro{padding-bottom:6px}
#lg-btn,#ltf-n{display:none!important}
#ltfbox,#ltfbox[hidden]{display:block!important;margin-top:6px}
#ltf{flex-wrap:nowrap!important;overflow-x:auto;scrollbar-width:none;padding-bottom:4px}
#ltf::-webkit-scrollbar{display:none}
.info.nt-leeg{background:none!important;border:0!important;box-shadow:none!important;padding:0 2px!important;min-height:0}
.info.nt-leeg h3,.info.nt-leeg .note{display:none}
.info.nt-leeg .pl{margin:0;font-size:.95rem}
.nt-grijs{opacity:.42}
.nt-grijs .av,.nt-grijs svg{filter:grayscale(1)}
.nt-sep{flex:none;width:1px;align-self:stretch;margin:8px 4px;background:var(--line)}
.nt-mld{margin:0 0 10px;padding:8px 12px;border-radius:12px;background:#F3E2D3;color:var(--ink);font-size:.95rem}
.nt-mld[hidden]{display:none}
.kat-land li{display:grid!important;grid-template-columns:28px minmax(0,1fr) auto;gap:4px 12px;align-items:center}
.kat-land li .nt-ti svg{width:28px;height:28px;display:block}
.kat-land li .kl-go{font-weight:700}
</style>
"""
EU_JS = r"""
<script>(function(){
/* hoofdpagina en soortpagina's in de opbouw van de landpagina's (bron/test_ontwerp.py) */
var WILD=WILDJSON,COL=COLJSON,GLY=GLYJSON;
var TX={wild:{nl:"In het wild (geschat)",en:"In the wild (estimated)",fr:"Dans la nature (estimation)",de:"In freier Wildbahn (geschätzt)",it:"In natura (stima)",es:"En libertad (estimación)"},
  onb:{nl:"onbekend",en:"unknown",fr:"inconnu",de:"unbekannt",it:"sconosciuto",es:"desconocido"},
  verspr:{nl:"Verspreiding",en:"Range",fr:"Répartition",de:"Verbreitung",it:"Distribuzione",es:"Distribución"}};
function lang(){var l=(document.documentElement.lang||"nl").slice(0,2);return TX.wild[l]?l:"en";}
/* korte uitleg zolang er geen locatie gekozen is */
var info=document.getElementById("info");
function leeg(){if(!info)return;var k=[].slice.call(info.children).map(function(e){return e.tagName+"."+e.className;}).join(",");
  info.classList.toggle("nt-leeg",k==="H3.,P.pl,P.note");}
if(info){new MutationObserver(leeg).observe(info,{childList:true});leeg();}
/* soortpagina: aantallen in het wild, hoofdletter in de link naar de Spottersgids, type-icoon bij de locaties */
function slugNu(){var m=decodeURIComponent(location.hash||"").match(/^#kat\/(.+)$/);return m?m[1]:(window.__KAT||"");}
function ico(k){var c=COL[k]||"#8B8676";return '<svg viewBox="-8 -8 16 16" aria-hidden="true" style="color:'+c+'"><circle r="8" fill="currentColor"/><g fill="#F0EEE2" style="color:#F0EEE2">'+(GLY[k]||'<circle r="2"/>')+'</g></svg>';}
var bezig=false;
function kat(){var kv=document.getElementById("katview");if(!kv||bezig)return;bezig=true;var l=lang();
  kv.querySelectorAll(".kat-feit > div").forEach(function(div){var dt=div.querySelector("dt"),dd=div.querySelector("dd");if(!dt||!dd)return;
    if(/IUCN/.test(dt.textContent)&&!div.dataset.nt){var s=slugNu(),w=WILD[s];div.dataset.nt="1";dt.textContent=TX.wild[l];dd.textContent=w?w:TX.onb[l];}
    else if(div.classList.contains("wd")&&!div.dataset.nt){div.dataset.nt="1";dt.textContent=TX.verspr[l];}});
  var h=kv.querySelector("h1"),a=kv.querySelector("a.kat-spot");
  if(l==="nl"&&h&&a&&!a.dataset.nt){var nm=h.textContent.trim();a.dataset.nt="1";
    if(/^(\S+(se|sche|’s)\b|Borneo|Soenda|Andes|Sri)/.test(nm)){var lo=nm.charAt(0).toLowerCase()+nm.slice(1);
      a.childNodes.forEach(function(n){if(n.nodeType===3&&n.textContent.indexOf(lo)>=0)n.textContent=n.textContent.replace(lo,nm);});}}
  kv.querySelectorAll(".kat-land li[data-hk]").forEach(function(li){if(li.querySelector(".nt-ti"))return;var s=document.createElement("span");s.className="nt-ti";s.innerHTML=ico(+li.dataset.hk);li.insertBefore(s,li.firstChild);});
  bezig=false;}
var kv=document.getElementById("katview");if(kv){new MutationObserver(kat).observe(kv,{childList:true,subtree:true});kat();}
/* land en soort op de kaart: wat niet samengaat grijs en achteraan (18-10-2026) */
var AV=AVJSON,zoom=document.getElementById("zoom"),row=document.getElementById("catrow"),bz=false;
var MLD={nl:["{k}: niet te zien in {p}.","Het filter op land staat nu uit.","Het filter op soort staat nu uit."],
  en:["{k}: not on view in {p}.","The country filter is now off.","The species filter is now off."],
  fr:["{k} : pas visible ici ({p}).","Le filtre par pays est désactivé.","Le filtre par espèce est désactivé."],
  de:["{k}: in {p} nicht zu sehen.","Der Länderfilter ist jetzt aus.","Der Artenfilter ist jetzt aus."],
  it:["{k}: non visibile in {p}.","Il filtro per paese è disattivato.","Il filtro per specie è disattivato."],
  es:["{k}: no se puede ver en {p}.","El filtro por país está desactivado.","El filtro por especie está desactivado."]};
function land(){var b=zoom&&zoom.querySelector('.chip[aria-pressed="true"]');return b&&b.dataset.zoom!=="all"?b.dataset.zoom:"";}
function soort(){var b=row&&row.querySelector('.catbtn[aria-pressed="true"]');return b?b.dataset.cat:"";}
function naam(b){var c=b.cloneNode(true);c.querySelectorAll(".n,svg,.av").forEach(function(x){x.remove();});return c.textContent.trim();}
function sorteer(box,sel,ok){var it=[].slice.call(box.querySelectorAll(sel));it.forEach(function(e,i){if(e.dataset.ntI===undefined)e.dataset.ntI=i;});
  it.sort(function(a,b){return a.dataset.ntI-b.dataset.ntI;});
  var ja=it.filter(function(e){return ok(e)!==false;}),nee=it.filter(function(e){return ok(e)===false;});
  it.forEach(function(e){e.classList.toggle("nt-grijs",ok(e)===false);});
  var sep=box.querySelector(".nt-sep");if(!sep){sep=document.createElement("span");sep.className="nt-sep";sep.setAttribute("aria-hidden","true");}
  var want=ja.concat(nee.length?[sep]:[],nee),cur=[].slice.call(box.children).filter(function(e){return e.matches(sel)||e===sep;});
  if(want.length!==cur.length||want.some(function(e,i){return cur[i]!==e;}))want.forEach(function(e){box.appendChild(e);});
  if(!nee.length&&sep.parentNode)sep.remove();}
function pas(){if(bz||!zoom||!row)return;bz=true;var c=land(),k=soort();
  sorteer(row,".catbtn",function(b){var s=b.dataset.cat;if(!s)return null;return !c||!!(AV[c]&&AV[c][s]);});
  var al=row.querySelector('.catbtn[data-cat=""] .av');if(al){if(al.dataset.ntN===undefined)al.dataset.ntN=al.textContent;
    var nt=String(c?Object.keys(AV[c]||{}).length:al.dataset.ntN);if(al.textContent!==nt)al.textContent=nt;}
  sorteer(zoom,".chip",function(b){var z=b.dataset.zoom;if(!z||z==="all")return null;return !k||!!(AV[z]&&AV[z][k]);});
  zoom.querySelectorAll(".chip").forEach(function(b){var n=b.querySelector(".nt-n"),z=b.dataset.zoom,v=k&&z!=="all"&&AV[z]?AV[z][k]:0;
    if(k&&z!=="all"&&v){if(!n){n=document.createElement("span");n.className="n nt-n";b.appendChild(n);}if(n.textContent!==String(v))n.textContent=v;}else if(n)n.remove();});
  bz=false;}
var mldT=null;
function melding(k,p,w){var el=document.getElementById("nt-mld");if(!el&&row){el=document.createElement("p");el.id="nt-mld";el.className="nt-mld";el.setAttribute("role","status");row.insertAdjacentElement("afterend",el);}
  if(!el)return;var t=MLD[(document.documentElement.lang||"nl").slice(0,2)]||MLD.en;el.textContent=t[0].replace("{k}",k).replace("{p}",p)+" "+t[w];el.hidden=false;
  clearTimeout(mldT);mldT=setTimeout(function(){el.hidden=true;},6000);}
document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest(".nt-grijs");if(!b||!zoom||!row)return;
  if(b.classList.contains("catbtn")&&row.contains(b)){var p=zoom.querySelector('.chip[aria-pressed="true"]'),pn=p?naam(p):"",kn=naam(b),cat=b.dataset.cat;
    e.preventDefault();e.stopPropagation();var a=zoom.querySelector('[data-zoom="all"]');if(a)a.click();
    setTimeout(function(){var nb=row.querySelector('.catbtn[data-cat="'+cat+'"]');if(nb)nb.click();melding(kn,pn,1);},40);}
  else if(b.classList.contains("chip")&&zoom.contains(b)){var s=row.querySelector('.catbtn[aria-pressed="true"]'),kn2=s?naam(s):"",pn2=naam(b),z=b.dataset.zoom;
    e.preventDefault();e.stopPropagation();var a2=row.querySelector('.catbtn[data-cat=""]');if(a2)a2.click();
    setTimeout(function(){var nz=zoom.querySelector('.chip[data-zoom="'+z+'"]');if(nz)nz.click();melding(kn2,pn2,2);},40);}},true);
if(zoom&&row){[zoom,row].forEach(function(x){new MutationObserver(function(){setTimeout(pas,0);}).observe(x,{childList:true,subtree:true,attributes:true,attributeFilter:["aria-pressed"]});});pas();}
/* onderbalk: Soorten aan op een soortpagina */
var bar=document.getElementById("nw-sbar-start");
if(bar&&window.__KAT){var s=bar.querySelector('[data-k="soorten"]');if(s)s.classList.add("on");}
})();</script>
"""
EU_T_OUD = 'home:{nl:"Home",en:"Home",fr:"Accueil",de:"Start",it:"Home",es:"Inicio"}'
EU_T_NIEUW = 'home:{nl:"Kaart",en:"Map",fr:"Carte",de:"Karte",it:"Mappa",es:"Mapa"}'


def europa(pad, wild, av, soort=False):
    doc = open(pad, encoding="utf-8").read()
    if EU_MARK in doc:   # vorige versie van deze laag eruit, dan opnieuw
        doc = re.sub(r'\n<style id="nt-eu-css">.*?</style>\n', "\n", doc, count=1, flags=re.S)
        doc = re.sub(r'\n<script>\(function\(\)\{\n/\* hoofdpagina en soortpagina.*?</script>\n', "\n", doc, count=1, flags=re.S)
        assert EU_MARK not in doc and "nt-leeg" not in doc, pad
        open(pad, "w", encoding="utf-8").write(doc)
    if NO.START_MARK not in doc:
        if not soort:
            return False
        NO.start_pagina(pad, False)
        doc = open(pad, encoding="utf-8").read()
    doc = doc.replace('data-k="home">' + NO.ICO["b-home"], 'data-k="home">' + ICO["b-map"], 1)
    doc = doc.replace('data-k="landen">' + NO.ICO["b-map"], 'data-k="landen">' + ICO["b-flag"], 1)
    doc = doc.replace(EU_T_OUD, EU_T_NIEUW, 1)
    import huisstijl
    js = (EU_JS.replace("WILDJSON", json.dumps(wild, ensure_ascii=False)).replace("AVJSON", json.dumps(av, ensure_ascii=False))
          .replace("COLJSON", json.dumps(huisstijl.TCOL)).replace("GLYJSON", json.dumps(huisstijl.GLY)))
    doc = doc.replace("</head>", EU_CSS + "</head>", 1)
    k = doc.rindex("</body>")
    doc = doc[:k] + js + doc[k:]
    open(pad, "w", encoding="utf-8").write(doc)
    return True


def slug_py(s):
    import unicodedata
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def maak_europa():
    gids = open(os.path.join(ROOT, "nederland-oud", "index.html"), encoding="utf-8").read()
    wild = {slug_py(k): v for k, v in json.loads(re.search(r"const WILD=(\{.*?\});", gids).group(1)).items()}
    # per land: soort -> aantal locaties (ook onzeker), uit de gegevens van de hoofdpagina
    st = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    i = st.index("const D=")
    D = json.loads(st[i + 8:st.index("\n", i)].rstrip(";"))
    av = {}
    for c, v in D.items():
        if not isinstance(v, dict) or "locs" not in v:
            continue
        cnt = {}
        for s in D["sp"]:
            al = {s[0]} | set(s[5])
            n = sum(1 for l in v["locs"] if any(x[4] in al for x in l[5]))
            if n:
                cnt[s[0]] = n
        av[c] = cnt
    n = europa(os.path.join(ROOT, "index.html"), wild, av) + europa(os.path.join(ROOT, "top10", "index.html"), wild, av)
    d = os.path.join(ROOT, "soort")
    for s in sorted(os.listdir(d)):
        pad = os.path.join(d, s, "index.html")
        if os.path.exists(pad):
            n += europa(pad, wild, av, soort=True)
    print("hoofdpagina, top 10 en soortpagina's in de nieuwe opbouw:", n)


if __name__ == "__main__":
    maak_alles()
