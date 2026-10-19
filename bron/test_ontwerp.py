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
    "Zwarte panter (zwart luipaard) in het wild, Tadoba (India)": {"fr": "Panthère noire (léopard noir) dans la nature, Tadoba (Inde)",
        "de": "Schwarzer Panther (schwarzer Leopard) in freier Wildbahn, Tadoba (Indien)", "it": "Pantera nera (leopardo nero) in natura, Tadoba (India)",
        "es": "Pantera negra (leopardo negro) en libertad, Tadoba (India)", "pt": "Pantera-negra (leopardo-negro) na natureza, Tadoba (Índia)"},
    "Zoek een soort": {"fr": "Rechercher une espèce", "de": "Art suchen", "it": "Cerca una specie", "es": "Busca una especie", "pt": "Procura uma espécie"},
    "Zoek een park of plaats": {"fr": "Rechercher un parc ou une ville", "de": "Park oder Ort suchen", "it": "Cerca un parco o una località",
                                "es": "Busca un parque o un lugar", "pt": "Procura um parque ou um local"},
    "Niets gevonden.": {"fr": "Aucun résultat.", "de": "Nichts gefunden.", "it": "Nessun risultato.", "es": "No se ha encontrado nada.", "pt": "Nada encontrado."},
    "onzeker": {"fr": "incertain", "de": "unsicher", "it": "incerto", "es": "incierto", "pt": "incerto"},
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
  <a href="#locaties" data-nw="locaties">{ICO["b-pin"]}{L("Locaties", "Locations")}</a>
  <a href="#soorten" data-nw="soorten">{ICO["b-paw"]}{L("Soorten", "Species")}</a>
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
.nt-zoek{margin:0 0 12px!important}
.nt-zoek label{height:48px!important}
.nt-geen{color:var(--muted);margin:8px 2px}
.nt-sc[hidden],#nt-zsgeen[hidden]{display:none!important}
#nt-kaart{position:relative}
.nt-kleeg{all:unset;box-sizing:border-box;cursor:pointer;position:absolute;left:50%;top:60%;transform:translate(-50%,-50%);width:min(78%,320px);display:flex;flex-direction:column;gap:4px;align-items:center;text-align:center;padding:14px 16px;border-radius:16px;background:color-mix(in srgb,var(--card) 94%,transparent);border:1px solid var(--line);box-shadow:var(--nw-shadow);font:400 .98rem var(--hs-body);color:var(--ink)}
.nt-kleeg b{font-weight:700}
.nt-kleeg span{color:var(--nw-terra);font-weight:600}
.nt-kleeg:focus-visible{outline:2px solid var(--nw-terra)}
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
/* scherm Locaties: losse kaartjes (19-10-2026) */
.nt-box:has(> .nt-full){background:none;border:0;padding:0;box-shadow:none;border-radius:0}
.nt-full{display:flex;flex-direction:column;gap:10px}
.nt-full .nt-kj{grid-template-columns:34px minmax(0,1fr) auto;grid-template-areas:"ic tx nb" "ic rj rj";gap:4px 12px;align-items:start;padding:14px 14px 14px 14px;border:1px solid var(--line);border-radius:16px;background:var(--card);box-shadow:var(--nw-shadow)}
.nt-full .nt-kj:first-child{border-top:1px solid var(--line)}
.nt-kj>.nt-ti{grid-area:ic;padding-top:1px}
.nt-kj>.nt-ti svg{width:34px;height:34px}
.nt-kj>.nt-lt{grid-area:tx;align-self:center}
.nt-kj>.nt-n{grid-area:nb;display:flex;flex-direction:column;align-items:flex-end;gap:3px;padding-top:0}
.nt-kj .nt-bdg{display:flex;align-items:center;justify-content:center;min-width:38px;height:38px;padding:0 6px;border-radius:99px;background:var(--nw-green);color:#FBF8F1;font:800 1.2rem var(--hs-display);line-height:1}
.nt-kj>.nt-n small{font:600 .78rem var(--hs-label);color:var(--muted);white-space:nowrap}
.nt-kj>.nt-rjs{grid-area:rj;display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
.nt-rj{width:34px;height:34px;border-radius:50%;overflow:hidden;flex:none;border:2px solid var(--line);background:var(--nw-sage);display:flex;align-items:center;justify-content:center;box-sizing:border-box}
.nt-rj img{width:100%;height:100%;object-fit:cover;display:block}
.nt-rj i{font:700 .9rem var(--hs-body);font-style:normal;color:var(--ink)}
.nt-rj.nt-rju{border-style:dashed;border-color:var(--muted)}
.nt-rj.nt-rjm{font:700 .85rem var(--hs-body);color:var(--ink);background:var(--paper)}
.nt-vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
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
var ARR='ARRSVG',ROWS='ROWSSVG',SRCH='SRCHSVG',T2=T2JSON;
var html=document.documentElement;

/* soorten per locatie en locaties per soort (zelfde koppeling als de gids: naam in LOCS[i][4]) */
var LSP=[],SPL={};
LOCS.forEach(function(l,i){var s={};R.forEach(function(r){if(l[4].indexOf(r[2])>=0)s[r[0]]=1;});LSP[i]=Object.keys(s);
  LSP[i].forEach(function(sp){(SPL[sp]=SPL[sp]||[]).push(i);});});
/* soorten zonder enige bevestigde vermelding (alleen onzeker of gepland): stippellijn */
/* bevestigd = aanwezig, tijdelijk niet zichtbaar, vertrek aangekondigd of alleen met rondleiding (zelfde regel als de gids en de hoofdpagina) */
function bevR(r){return String(r[4]).split("+").some(function(c){return "gybr".indexOf(c)>=0&&c;});}
var BEV={},LBEV=[];R.forEach(function(r){if(bevR(r))BEV[r[0]]=1;});
LOCS.forEach(function(l,i){var s={};R.forEach(function(r){if(l[4].indexOf(r[2])>=0&&bevR(r))s[r[0]]=1;});LBEV[i]=s;});
function onz(sp){return !BEV[sp];}
/* met een regio gekozen: alleen onzeker als de soort in die regio nergens bevestigd is */
function onzR(sp,r){if(!r)return onz(sp);return !(SPL[sp]||[]).some(function(i){return inReg(i,r)&&LBEV[i][sp];});}
/* aantal locaties met een bevestigde vermelding van een soort, en met alleen onzekere */
function nBev(sp){return (SPL[sp]||[]).filter(function(i){return LBEV[i][sp];}).length;}
function tel(b,u,eenheid){return (b?b+' '+eenheid(b):'')+(u?(b?' · ':'')+u+' '+LS("onzeker","uncertain"):'');}
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
  .sort(function(a,b){return Object.keys(LBEV[b]).length-Object.keys(LBEV[a]).length||LSP[b].length-LSP[a].length||LOCS[a][0].localeCompare(LOCS[b][0]);});}
function kaart(i,lang){var l=LOCS[i],nm=l[0],k=tk(nm),s=N.lslug(nm),n=Object.keys(LBEV[i]).length,u=LSP[i].length-n,d=lang&&DS[s];
  if(lang)return kaartje(i,l,nm,k,s,n,u);
  return '<li class="nt-loc"><span class="nt-ti">'+ico(k)+'</span><span class="nt-lt"><a href="#locatie/'+s+'">'+E(nm)+'</a><small>'+E(l[1])+(k>=0?' · '+E(tnaam(k)):"")+'</small>'+
    (d?'<span class="nt-ds">'+d+'</span>':"")+'</span><span class="nt-n">'+(n?'<b>'+n+'</b> '+nsoort(n):'')+(u?(n?'<br>':'')+'<small>'+u+' '+LS("onzeker","uncertain")+'</small>':'')+'</span></li>';}

/* scherm Locaties (19-10-2026): los kaartje per locatie, aantal als badge, soortrondjes (bevestigd eerst, onzeker met stippelrand) */
var RMAX=6;
function rondje(sp,onzeker){var p=PH[sp]&&PH[sp].src,nm=N.spName(sp);
  return '<span class="nt-rj'+(onzeker?" nt-rju":"")+'" title="'+E(nm)+'">'+(p?'<img src="'+E(p)+'" alt="" loading="lazy">':'<i>'+E(nm.charAt(0))+'</i>')+'</span>';}
function kaartje(i,l,nm,k,s,n,u){var b=LSP[i].filter(function(sp){return LBEV[i][sp];}),o=LSP[i].filter(function(sp){return !LBEV[i][sp];}),alle=b.concat(o);
  var toon=alle.length>RMAX?alle.slice(0,RMAX-1):alle,rest=alle.length-toon.length;
  var rj=toon.map(function(sp){return rondje(sp,!LBEV[i][sp]);}).join("")+(rest?'<span class="nt-rj nt-rjm">+'+rest+'</span>':"");
  var namen=alle.map(function(sp){return N.spName(sp)+(LBEV[i][sp]?"":" ("+TX("onzeker","uncertain")+")");}).join(", ");
  return '<li class="nt-loc nt-kj"><span class="nt-ti">'+ico(k)+'</span><span class="nt-lt"><a href="#locatie/'+s+'">'+E(nm)+'</a><small>'+E(l[1])+(k>=0?' · '+E(tnaam(k)):"")+'</small></span>'+
    '<span class="nt-n">'+(n?'<b class="nt-bdg">'+n+'</b><span class="nt-vh"> '+nsoort(n)+'</span>':'')+(u?'<small>'+u+' '+LS("onzeker","uncertain")+'</small>':'')+'</span>'+
    (alle.length?'<span class="nt-rjs" aria-hidden="true">'+rj+'</span><span class="nt-vh">'+E(namen)+'</span>':'')+'</li>';}

/* knop "Naar boven" (19-10-2026): de gids scrolde naar de onderkant van zijn oude kop, die in dit ontwerp verborgen is (sprong maar een paar pixels). Nu altijd helemaal naar boven. */
document.addEventListener("click",function(e){var t=e.target.closest&&e.target.closest("#totop");if(!t)return;e.preventDefault();e.stopImmediatePropagation();window.scrollTo({top:0,behavior:"smooth"});},true);

/* ---------- kaart (startscherm) ---------- */
function cats(){var el=$("#nt-cats");if(!el)return;
  var all=N.BIG.concat(N.SMALL).filter(function(s){return SPL[s];}).sort(function(a,b){return N.spName(a).localeCompare(N.spName(b));});
  /* met een regio gekozen: katten die daar niet zitten grijs en achteraan */
  var r=reg(),ok=function(s){return !r||(SPL[s]||[]).some(function(i){return inReg(i,r);});};
  var ja=all.filter(ok),nee=all.filter(function(s){return !ok(s);});
  var hn=$(".nw-nsp strong"),num=r?ja.filter(function(s){return !onzR(s,r);}).length:(hn?hn.textContent:all.length);
  function knop(s,grijs){var p=PH[s]&&PH[s].src;return '<button type="button" class="nt-cat'+(grijs?" nt-grijs":"")+'" data-sp="'+E(s)+'" aria-pressed="'+(SP===s)+'"><span class="nt-av'+((grijs?onz(s):onzR(s,r))?" nt-avu":"")+'">'+(p?'<img src="'+E(p)+'" alt="" loading="lazy">':"")+'</span><span>'+E(N.spName(s))+'</span></button>';}
  el.innerHTML='<button type="button" class="nt-cat" data-sp="" aria-pressed="'+(!SP)+'"><span class="nt-av nt-all">'+num+'</span><span>'+LS("Alle katten","All cats")+'</span></button>'+
    ja.map(function(s){return knop(s,false);}).join("")+(nee.length?'<span class="nt-sep" aria-hidden="true"></span>'+nee.map(function(s){return knop(s,true);}).join(""):"");
  el.setAttribute("aria-label",TX("Kies een soort","Choose a species"));}
function spinfo(){var el=$("#nt-spinfo");if(!el)return;if(!SP){el.hidden=true;el.innerHTML="";return;}var b=nBev(SP),u=(SPL[SP]||[]).length-b;
  el.innerHTML='<b>'+E(N.spName(SP))+'</b> · '+tel(b,u,nloc)+' · <a href="#soort/'+N.slug(SP)+'">'+LS("Meer over deze soort","More about this species")+' →</a>';el.hidden=false;}
function filt(){var set=SP?SPL[SP]||[]:null;$$("#nlmap .mk").forEach(function(m){var i=+m.dataset.i;m.classList.toggle("nt-uit",!!set&&set.indexOf(i)<0);});}
function beeld(){var el=$("#nt-beeld");if(!el)return;var ids=lijst(SP),n=ids.length,show=MEER?ids:ids.slice(0,5);
  el.innerHTML='<h3>'+LS("In beeld","On the map")+': '+n+' '+nloc(n)+'</h3><p class="nt-note">'+LS("Meeste soorten eerst. Tik op een naam voor de katten en bezoekinformatie.","Most species first. Tap a name for its cats and visitor information.")+'</p>'+
    '<ul class="nt-list">'+show.map(function(i){return kaart(i,false);}).join("")+'</ul>'+
    (n>5&&!MEER?'<button type="button" class="nt-more" id="nt-more">'+LS("Toon alle","Show all")+' ('+n+')</button>':"");}
document.addEventListener("click",function(e){
  var c=e.target.closest&&e.target.closest(".nt-cat");
  if(c&&c.classList.contains("nt-grijs")){var rb=$('#rg-bar [aria-pressed="true"]'),pn=rb?chipNaam(rb):"",al=$('#rg-bar .rg-chip[data-r=""]');
    SP=c.dataset.sp;MEER=false;if(al)al.click();cats();spinfo();filt();beeld();regs();melding(N.spName(SP),pn,1);return;}
  if(c){SP=c.dataset.sp||null;MEER=false;cats();spinfo();filt();beeld();regs();setTimeout(kaartLeeg,30);return;}
  if(e.target.closest&&e.target.closest("#nt-more")){MEER=true;beeld();return;}
  var t=e.target.closest&&e.target.closest("#nt-types .lt-chip");
  if(t){var o=$$("#lt-bar .lt-chip").filter(function(b){return b.dataset.t===t.dataset.t;})[0];if(o)o.click();return;}
  var g=e.target.closest&&e.target.closest("#nt-regs .rg-chip");
  if(g&&g.classList.contains("nt-grijs")&&SP){var kn=N.spName(SP);SP=null;MEER=false;cats();spinfo();filt();melding(kn,chipNaam(g),2);}
  if(g){var o2=$$("#rg-bar .rg-chip").filter(function(b){return b.dataset.r===g.dataset.r;})[0];if(o2)o2.click();}});
function types(){var bar=$("#lt-bar"),el=$("#nt-types");if(!el)return;if(!bar){el.hidden=true;return;}el.innerHTML=bar.innerHTML;el.setAttribute("aria-label",bar.getAttribute("aria-label")||"");
  var r=reg();if(r)$$(".lt-chip",el).forEach(function(b){var t=b.dataset.t||"",nn=b.querySelector(".n");if(!nn)return;nn.textContent=LOCS.filter(function(l,i){return inReg(i,r)&&(!t||tnl(i)===t);}).length;});}
function regs(){var bar=$("#rg-bar"),el=$("#nt-regs"),w=$("#nt-rgw");if(!bar||!el)return;w.hidden=false;el.innerHTML=bar.innerHTML;el.setAttribute("aria-label",bar.getAttribute("aria-label")||"");
  /* met een soort gekozen: regio's zonder die soort grijs en achteraan, bij de rest het aantal locaties met die soort */
  if(SP){var grijs=[];$$(".rg-chip",el).forEach(function(b){var r=b.dataset.r,n=r?(SPL[SP]||[]).filter(function(i){return inReg(i,r);}).length:(SPL[SP]||[]).length,nn=b.querySelector(".n");
      if(nn)nn.textContent=n;if(r&&!n){b.classList.add("nt-grijs");grijs.push(b);}});
    if(grijs.length){var sp=document.createElement("span");sp.className="nt-sep";sp.setAttribute("aria-hidden","true");el.appendChild(sp);grijs.forEach(function(b){el.appendChild(b);});}}
  var lab=$("#rg-lab");$("#nt-rglab").textContent=lab?lab.textContent:"";}

/* ---------- zoekvelden boven Locaties en Soorten ---------- */
function nrm(x){return String(x).toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[’']/g,"").replace(/<[^>]*>/g," ");}
var ZL="",ZS="";
function zoekveld(id,nl,en){var d=document.createElement("div");d.className="nw-search nt-zoek";
  d.innerHTML='<label>'+SRCH+'<input type="search" id="'+id+'" autocomplete="off"></label>';d.dataset.nl=nl;d.dataset.en=en;return d;}
function zph(){[["nt-zl","Zoek een park of plaats","Search for a park or town"],["nt-zs","Zoek een soort","Search for a species"]].forEach(function(z){var i=document.getElementById(z[0]);if(i){i.placeholder=TX(z[1],z[2]);i.setAttribute("aria-label",i.placeholder);}});}
function geen(){return '<p class="nt-geen">'+LS("Niets gevonden.","Nothing found.")+'</p>';}
/* ---------- locaties ---------- */
function locs(){var el=$("#nt-loclist");if(!el)return;var q=nrm(ZL.trim()),ids=lijst(null);
  if(q){var w=q.split(/\s+/);ids=ids.filter(function(i){var l=LOCS[i],t=nrm(l[0]+" "+l[1]+" "+(l[4]||[]).join(" ")+" "+(DS[N.lslug(l[0])]||""));return w.every(function(x){return t.indexOf(x)>=0;});});}
  el.innerHTML=ids.length?ids.map(function(i){return kaart(i,true);}).join(""):geen();}
function zoekSoort(){var q=nrm(ZS.trim()),w=q?q.split(/\s+/):[],n=0;
  $$(".nt-spg .nt-sc").forEach(function(a){var t=nrm(a.textContent+" "+(a.dataset.sp||"")),ok=w.every(function(x){return t.indexOf(x)>=0;});a.hidden=!ok;if(ok)n++;});
  $$(".chips[data-group]").forEach(function(box){var vis=$$(".nt-sc",box).some(function(a){return !a.hidden;}),g=box.previousElementSibling;
    if(q){box.classList.toggle("nt-weg",!vis);if(g&&g.classList.contains("group-title"))g.classList.toggle("nt-weg",!vis);}
    else{box.classList.remove("nt-weg");if(g)g.classList.remove("nt-weg");}});
  var e=$("#nt-zsgeen");if(e)e.hidden=!(q&&!n);}

/* ---------- soorten ---------- */
function spgrid(){setTimeout(zoekSoort,0);$$(".chips[data-group]").forEach(function(box){var g=box.querySelector(":scope > .nt-spg");if(!g){g=document.createElement("div");g.className="nt-spg";box.appendChild(g);}
  g.innerHTML=$$(":scope > .chip[data-sp]",box).map(function(c){var sp=c.dataset.sp,p=PH[sp]&&PH[sp].src,b=nBev(sp),u=(SPL[sp]||[]).length-b;
    return '<a class="nt-sc'+(onz(sp)?" nt-uns":"")+'" data-sp="'+E(sp+" "+(N.SPEN&&N.SPEN[sp]?N.SPEN[sp][0]:""))+'" href="#soort/'+N.slug(sp)+'"><span class="ph">'+(p?'<img src="'+E(p)+'" alt="" loading="lazy">':"")+'</span><span class="bd"><span class="nm">'+E(N.spName(sp))+'</span><small>'+tel(b,u,nloc)+'</small></span></a>';}).join("");});}

/* kaart zonder stippen voor de gekozen regio (bijv. de Canarische Eilanden): melding met verwijzing naar de lijst */
var KL={nl:["{r} staat niet op de kaart.","Bekijk de {n} locaties hieronder","Bekijk de locatie hieronder"],
  en:["{r} is not on the map.","See the {n} locations below","See the location below"],
  fr:["{r} n’apparaît pas sur la carte.","Voir les {n} lieux ci-dessous","Voir le lieu ci-dessous"],
  de:["{r} ist nicht auf der Karte.","Die {n} Orte stehen unten","Der Ort steht unten"],
  it:["{r} non è sulla mappa.","Vedi i {n} luoghi qui sotto","Vedi il luogo qui sotto"],
  es:["{r} no aparece en el mapa.","Mira los {n} lugares abajo","Mira el lugar abajo"],
  pt:["{r} não aparece no mapa.","Vê os {n} locais abaixo","Vê o local abaixo"]};
function kaartLeeg(){var k=$("#nt-kaart");if(!k)return;var o=$("#nt-kleeg");if(o)o.remove();var b=$('#rg-bar [aria-pressed="true"]');
  if(!b||!b.dataset.r)return;var zicht=$$("#nlmap .mk, #nlmap .hs-cl").some(function(m){return getComputedStyle(m).display!=="none";});if(zicht)return;
  var n=lijst(SP).length;if(!n)return;var t=KL[N.lang()]||KL.en,x=document.createElement("button");x.type="button";x.id="nt-kleeg";x.className="nt-kleeg";
  x.innerHTML='<b>'+E(t[0].replace("{r}",chipNaam(b)))+'</b><span>'+E((n===1?t[2]:t[1]).replace("{n}",n))+' ↓</span>';
  x.addEventListener("click",function(){var bl=$("#nt-beeld");if(bl)bl.scrollIntoView({behavior:"smooth",block:"start"});});k.appendChild(x);}
/* bij een gekozen regio inzoomen op de locaties van die regio (18-10-2026) */
var ZR=null;
function regioZoom(){var svg=$("#nlmap"),r=reg();if(!svg||!window.__HSZOOM||r===ZR)return;ZR=r;
  if(!r){window.__HSZOOM(svg,null);return;}
  var b=svg.viewBox.baseVal,st=svg.__zk,B=st?st.base:[b.x,b.y,b.width,b.height],x0=1e9,y0=1e9,x1=-1e9,y1=-1e9,n=0;
  $$(".mk",svg).forEach(function(m){var i=+m.dataset.i;if(!LOCS[i]||!inReg(i,r))return;var d=m.querySelector(".dot");if(!d)return;
    var x=+d.getAttribute("cx"),y=+d.getAttribute("cy");x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);n++;});
  if(!n){window.__HSZOOM(svg,null);return;}
  var asp=B[3]/B[2],w=Math.max((x1-x0)*1.5,(y1-y0)*1.5/asp,B[2]/4),h=w*asp;
  window.__HSZOOM(svg,[(x0+x1)/2-w/2,(y0+y1)/2-h/2,w,h]);}
function alles(){setTimeout(kaartLeeg,30);setTimeout(regioZoom,40);cats();spinfo();filt();beeld();types();regs();locs();spgrid();}

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
  /* foto van een zwarte panter boven Kleur & hybriden (Wikimedia Commons, CC BY-SA 4.0) */
  var kb=$("#kleur > .cbody")||$("#kleur");if(kb&&!$(".nt-kfoto",kb)){var kf=document.createElement("figure");kf.className="nw-foto nt-kfoto";
    var cr=' · <a href="https://commons.wikimedia.org/wiki/File:Melanistic_leopard_at_Tadoba.jpg" target="_blank" rel="noopener">Atul.rewild, Wikimedia Commons</a> · CC BY-SA 4.0';
    kf.innerHTML='<img src="/wildekattengids/img/nieuw/zwarte-panter.webp" alt="" loading="lazy" style="aspect-ratio:4/3;object-position:50% 45%"><p>'+LS("Zwarte panter (zwart luipaard) in het wild, Tadoba (India)","Black panther (black leopard) in the wild, Tadoba (India)")+cr+'</p>';
    kb.insertBefore(kf,kb.firstChild);}
  /* zoekvelden */
  var zl=zoekveld("nt-zl");lb.insertBefore(zl,lb.firstChild);
  var sb0=$("#soorten > .cbody")||$("#soorten"),zs=zoekveld("nt-zs");sb0.insertBefore(zs,sb0.firstChild);
  var zg=document.createElement("div");zg.id="nt-zsgeen";zg.hidden=true;zg.innerHTML=geen();zs.insertAdjacentElement("afterend",zg);
  $("#nt-zl").addEventListener("input",function(){ZL=this.value;locs();});
  $("#nt-zs").addEventListener("input",function(){ZS=this.value;zoekSoort();});
  zph();
  /* hoofdtabel als eigen scherm */
  var tb=$("#tabel > .cbody")||$("#tabel");tb.appendChild(reg);
  var sb=$("#soorten > .cbody")||$("#soorten"),lk=document.createElement("a");lk.className="nt-link";lk.href="#tabel";
  lk.innerHTML=ROWS+'<span>'+LS("Alle vermeldingen in één tabel","All entries in one table")+'</span>'+ARR;sb.appendChild(lk);
  alles();
  ["lt-bar","rg-bar"].forEach(function(id){var b=document.getElementById(id);if(b)new MutationObserver(function(){types();regs();cats();beeld();locs();setTimeout(kaartLeeg,30);setTimeout(regioZoom,40);}).observe(b,{childList:true,subtree:true,attributes:true,attributeFilter:["aria-pressed"]});});
  new MutationObserver(function(){leesDS();alles();zph();}).observe(html,{attributes:true,attributeFilter:["lang"]});
  /* na een tik op de kaart het infovak in beeld brengen als het onder de rand valt */
  $("#nt-kaart").addEventListener("click",function(e){if(!e.target.closest(".mk"))return;setTimeout(function(){var m=$("#mapinfo");if(!m)return;var r=m.getBoundingClientRect();
    if(r.top>innerHeight-140)window.scrollBy({top:r.top-innerHeight+Math.min(r.height,300)+90,behavior:"smooth"});},60);});
  /* binnenkomst met een # (bijv. #soorten): bovenaan het scherm beginnen */
  if(/^#(soorten|locaties|route|actueel|kleur|uitleg|rapporteer|tldr|tabel|meer|favorieten)$/.test(location.hash))window.scrollTo(0,0);
  return true;}
if(!opbouw()){var n=0,iv=setInterval(function(){if(opbouw()||++n>80)clearInterval(iv);},100);}

/* routeplanner: welke soorten je met je keuze al ziet (naast "Nog niet:") */
var ALW={nl:"Al wel:",en:"Already:",fr:"Déjà :",de:"Schon dabei:",it:"Già:",es:"Ya:",pt:"Já:"};
function alWel(){var sc=$("#rt-score"),sp=$("#rt-sp");if(!sc||!sp)return;var o=sc.querySelector(".nt-alwel");if(o)o.remove();
  var ja=$$(".rchip.on",sp).map(function(c){return (c.firstChild&&c.firstChild.nodeType===3?c.firstChild.textContent:c.textContent).trim();});
  if(!ja.length)return;var s=document.createElement("span");s.className="hs-mist nt-alwel";
  s.innerHTML='<b>'+(ALW[N.lang()]||ALW.en)+'</b> '+ja.map(E).join(", ");
  var m=sc.querySelector(".hs-mist:not(.nt-alwel)");if(m)sc.insertBefore(s,m);else sc.appendChild(s);}
(function(){var sp=$("#rt-sp");if(sp)new MutationObserver(function(){setTimeout(alWel,0);}).observe(sp,{childList:true,subtree:true});
  new MutationObserver(function(){setTimeout(alWel,0);}).observe(html,{attributes:true,attributeFilter:["lang"]});setTimeout(alWel,0);})();
/* zoeken klapt open via het vergrootglas bovenaan */
var q=$("#nw-q"),tz=$('.hs-top a.hs-ico[href="#start"]')||$('.hs-top a.hs-ico[href$="#zoek"]');
if(tz)tz.addEventListener("click",function(){html.classList.add("nt-zoek");});
if(q)q.addEventListener("blur",function(){setTimeout(function(){if(!q.value&&document.activeElement!==q)html.classList.remove("nt-zoek");},200);});
})();
</script>
"""


FAV_OUD = """var MEM=null;
function F(){if(!MEM){try{MEM=JSON.parse(localStorage.getItem("nw-fav")||"null");}catch(e){}if(!MEM||!MEM.loc||!MEM.sp)MEM={loc:[],sp:[]};}return MEM;}
function save(){try{localStorage.setItem("nw-fav",JSON.stringify(MEM));}catch(e){}}
function has(k,s){return F()[k].indexOf(s)>=0;}
function toggle(k,s){var a=F()[k],i=a.indexOf(s);if(i>=0)a.splice(i,1);else a.push(s);save();paint();}"""
FAV_NIEUW = r"""var LAND="LANDCODE";
function hier(x){if(x.c===LAND)return true;if(x.c)return false;return x.k==="loc"?LOCBYSLUG[x.s]!==undefined:!!BYSLUG[x.s];}
function F(){var a=favLees(),o={loc:[],sp:[]};a.forEach(function(x){if(hier(x)&&o[x.k])o[x.k].push(x.s);});return o;}
function has(k,s){return F()[k].indexOf(s)>=0;}
function toggle(k,s){var a=favLees(),i=-1;a.forEach(function(x,j){if(i<0&&x.k===k&&x.s===s&&hier(x))i=j;});
  if(i>=0)a.splice(i,1);else{var it={k:k,c:LAND,s:s};
    if(k==="loc"){var l=LOCS[LOCBYSLUG[s]];if(l){it.n=l[0];it.p=l[1];}}else{var b=BYSLUG[s];if(b){it.n=b[0];it.e=en(b[0]);it.p=b[2];}}a.push(it);}
  favSchrijf(a);paint();}"""
MEER_OUD = 'var site=$$("#hs-menu nav a").map(function(a){var c=a.cloneNode(true);c.removeAttribute("class");return \'<li>\'+c.outerHTML.replace(/<\\/a>$/,ARR+"</a>")+\'</li>\';}).join("");'
# Meer zonder het blok Bezoekersgids (kop en sitelinks), 18-10-2026
MEER_NIEUW = 'var site="";'


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
           'window.__NT={SPEN:SPEN,R:R,LOCS:LOCS,PHOTOS:PHOTOS,BIG:BIG,SMALL:SMALL,UNSURE:UNSURE,spName:spName,slug:slug,lslug:lslug,'
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
    # Meer zonder dubbelingen (18-10-2026): Ko-fi staat al onderaan, de Spottersgids alleen in de eigen taal; kaart Europa,
    # recent geboren, parken op aantal soorten en soorten locaties staan al in het menu bovenaan
    js = rep(js, MEER_OUD, MEER_NIEUW)
    # favorieten: gedeelde lijst voor alle landen; de lijst zelf staat op de hoofdpagina (Meer)
    js = rep(js, FAV_OUD, FAVJS + FAV_NIEUW.replace("LANDCODE", CODE.get(land, "")))
    js = rep(js, 'var own=["route","actueel","tldr","kleur","favorieten","tabel","uitleg","rapporteer"]',
             'var own=["tldr","actueel","kleur","route","tabel","uitleg","rapporteer"]')
    # de keuzeknoppen voor de filters bij Locaties niet: hier blijven de typeknoppen zichtbaar
    a = js.index("/* ---------- filters bij Locaties")
    b = js.index("paint();apply();", a)
    js = js[:a] + js[b:]
    svg = "{" + ",".join(f'"{k}":{v!r}' for k, v in ICO.items()) + "}"
    js = (js.replace("HEARTSVG", NO.HEART_S).replace("PAWSVG", ICO["b-paw"]).replace("PINSVG", ICO["b-map"])
          .replace("ARRSVG", NO.ARROW).replace("var $=function", "var SVG=" + svg + ";\nvar TRX=" + json.dumps(NO.TR, ensure_ascii=False) + ";\nvar $=function", 1))
    js_t = (JS.replace("ARRSVG", NO.ARROW).replace("ROWSSVG", ICO["rows"])
            .replace("T2JSON", json.dumps(TR, ensure_ascii=False)).replace("SRCHSVG", ICO["search"]))
    i = doc.rindex("</body>")
    doc = doc[:i] + BAR + js + js_t + doc[i:]
    os.makedirs(os.path.dirname(doel), exist_ok=True)
    open(doel, "w", encoding="utf-8").write(doc)
    print("testontwerp geschreven:", map + "/index.html")


# landcode <-> map
CODE = {"nederland": "nl", "belgie": "be", "luxemburg": "lu", "duitsland": "de", "frankrijk": "fr", "oostenrijk": "at",
        "zwitserland": "ch", "verenigd-koninkrijk": "uk", "italie": "it", "spanje": "es", "ierland": "ie", "portugal": "pt"}

# Favorieten voor alle landen samen (18-10-2026). Elk item: {k:"loc"|"sp", c:landcode of "eu", s:slug, n:naam, e:Engelse naam, p:plaats}.
# Oude favorieten ("nw-fav", alleen slugs) worden bij het lezen overgenomen met c:"" (land nog onbekend).
FAVJS = r"""
var FK="nt-fav";
function favLees(){var a=null;try{a=JSON.parse(localStorage.getItem(FK)||"null");}catch(e){}
  if(!Array.isArray(a)){a=[];try{var o=JSON.parse(localStorage.getItem("nw-fav")||"null");if(o){(o.loc||[]).forEach(function(x){a.push({k:"loc",c:"",s:x});});(o.sp||[]).forEach(function(x){a.push({k:"sp",c:"",s:x});});}}catch(e){}}
  return a;}
function favSchrijf(a){try{localStorage.setItem(FK,JSON.stringify(a));}catch(e){}}
"""

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
    if NO.LOS_MARK not in doc:
        return False
    al = LOS2_MARK in doc
    g = NO.BASE + land + "/"
    act = "locaties" if kind == "locatie" else "soorten"
    links = [("start", g, ICO["b-map"], "Kaart"), ("locaties", g + "#locaties", ICO["b-pin"], "Locaties"),
             ("soorten", g + "#soorten", ICO["b-paw"], "Soorten"), ("meer", g + "#meer", ICO["b-menu"], "Meer")]
    bar = ('<div class="nw-bar"><nav aria-label="Menu">'
           + "".join(f'<a href="{h}"{" class=on" if k == act else ""}>{svg}<span>{t}</span></a>' for k, h, svg, t in links)
           + "</nav></div>\n")
    doc, n = re.subn(r'<div class="nw-bar"><nav aria-label="Menu">.*?</nav></div>\n', lambda m: bar, doc, count=1, flags=re.S)
    if not n:
        return False
    doc = doc.replace('<span class="nw-stitle">Per kat</span>', '<span class="nw-stitle">Soorten</span>', 1)
    if not al:
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
T6 = {"Meer": {"fr": "Plus", "de": "Mehr", "it": "Altro", "es": "Más"},
      "Favorieten": {"fr": "Favoris", "de": "Favoriten", "it": "Preferiti", "es": "Favoritos"},
      "Kaart": {"fr": "Carte", "de": "Karte", "it": "Mappa", "es": "Mapa"},
      "Je bewaarde parken en soorten uit alle landen. Tik op het hartje bij een park of soort om het hier te zetten; je lijst blijft alleen op dit apparaat.": {
          "fr": "Vos parcs et espèces enregistrés, tous pays confondus. Touchez le cœur à côté d’un parc ou d’une espèce pour l’ajouter ici ; votre liste reste uniquement sur cet appareil.",
          "de": "Deine gespeicherten Parks und Arten aus allen Ländern. Tippe auf das Herz bei einem Park oder einer Art, um ihn hier zu speichern; deine Liste bleibt nur auf diesem Gerät.",
          "it": "I tuoi parchi e le tue specie salvati, da tutti i paesi. Tocca il cuore accanto a un parco o a una specie per salvarlo qui; la tua lista resta solo su questo dispositivo.",
          "es": "Tus parques y especies guardados de todos los países. Toca el corazón junto a un parque o una especie para guardarlo aquí; tu lista se queda solo en este dispositivo."}}


def L6(nl, en):
    t = T6.get(nl, {})
    return (f'<span class="l-nl">{nl}</span><span class="l-en">{en}</span>'
            + "".join(f'<span class="l-{x}">{t.get(x, en)}</span>' for x in ["fr", "de", "it", "es"]))


FAVICO = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round">'
          '<path d="M12 20s-8-5-8-11a4.5 4.5 0 0 1 8-2.5A4.5 4.5 0 0 1 20 9c0 6-8 11-8 11z"/></svg>')
MEERPAGE = ('<section class="page" id="meer" aria-labelledby="h-meer">\n'
            f'  <a class="terug" href="#kaart" data-home="kaart">← {L6("Kaart", "Map")}</a>\n'
            f'  <h1 id="h-meer">{L6("Meer", "More")}</h1>\n'
            '  <ul class="nt-ml" id="nt-meerlist"></ul>\n</section>\n\n')
FAVPAGE = ('<section class="page" id="favorieten" aria-labelledby="h-favorieten">\n'
           f'  <a class="terug" href="#kaart" data-home="kaart">← {L6("Kaart", "Map")}</a>\n'
           f'  <h1 id="h-favorieten">{L6("Favorieten", "Favourites")}</h1>\n'
           f'  <p class="sub">{L6("Je bewaarde parken en soorten uit alle landen. Tik op het hartje bij een park of soort om het hier te zetten; je lijst blijft alleen op dit apparaat.", "Your saved parks and species from all countries. Tap the heart next to a park or species to keep it here; your list stays on this device only.")}</p>\n'
           '  <div id="nt-favlist"></div>\n</section>\n\n')
ICO["b-flag"] = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
                 'stroke-linejoin="round"><path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/></svg>')
EU_CSS = r"""
<style id="nt-eu-css">
.catbtn .av.nt-avu{border-style:dashed;border-color:var(--muted)}
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
.nt-fh{font-family:var(--label);font-weight:600;font-size:.8rem;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin:18px 2px 6px}
.nt-fl{list-style:none;margin:0;padding:0;background:var(--paper);border:1px solid var(--line);border-radius:12px;overflow:hidden;max-width:760px}
.nt-fl li{display:flex;align-items:center;gap:10px;padding:8px 8px 8px 14px;border-top:1px solid var(--line)}
.nt-fl li:first-child{border-top:0}
.nt-fl a{flex:1;min-width:0;color:var(--ink);text-decoration:none;font-weight:700}
.nt-fl small{display:block;color:var(--muted);font-weight:400;font-size:.9rem}
.nt-hart{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;border-radius:50%;color:#B4483F;flex:none}
.nt-hart svg{width:22px;height:22px}
.nt-hart svg path{fill:transparent;stroke:currentColor;stroke-width:2}
.nt-hart[aria-pressed="true"] svg path{fill:currentColor}
.nt-hart:focus-visible{outline:2px solid var(--accent)}
.nt-hw{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;gap:4px;font:500 .95rem var(--body);color:var(--ink);margin:4px 0 8px;background:#F4E3DF;border-radius:99px;padding:0 14px 0 2px}
.nt-fleeg{color:var(--muted)}
.nt-ml{list-style:none;margin:6px 0 0;padding:0;background:var(--paper);border:1px solid var(--line);border-radius:16px;overflow:hidden;max-width:760px}
.nt-ml li{margin:0;border-top:1px solid var(--line)}
.nt-ml li:first-child{border-top:0}
.nt-ml a{display:flex;align-items:center;gap:12px;padding:14px 16px;color:var(--ink);text-decoration:none;font-size:1.05rem;font-weight:500}
.nt-ml a>svg:first-child{width:22px;height:22px;flex:none;color:var(--accent)}
.nt-ml .nt-pijl{margin-left:auto;width:18px;height:18px;color:var(--muted);flex:none}
.kat-land li{display:grid!important;grid-template-columns:28px minmax(0,1fr) auto;gap:4px 12px;align-items:center}
.kat-land li .nt-ti svg{width:28px;height:28px;display:block}
.kat-land li .kl-go{font-weight:700}
/* groene kop per scherm op de startpagina: Kaart groot, Landen/Soorten/Meer kort (19-10-2026) */
/* zelfde maten als de kop van de landgids (.nt-kop): 166px hoog, titel 39px met vlag 44x30 (19-10-2026) */
.nt-tk>div{display:none}
html:not([data-nt-tab="landen"]):not([data-nt-tab="soorten"]) .nt-tk>[data-t="kaart"],html[data-nt-tab="landen"] .nt-tk>[data-t="landen"],html[data-nt-tab="soorten"] .nt-tk>[data-t="soorten"]{display:block}
html.nt-tk-on .intro .wrap>h1,html.nt-tk-on .intro .wrap>.sub,html.nt-tk-on .intro .wrap>.meta{display:none!important}
html.nt-tk-on body .intro{height:166px!important;min-height:0!important;box-sizing:border-box!important;padding:21px 0 44px!important}
html body .nt-tk h1{display:flex!important;align-items:flex-start;gap:12px;margin:0!important;font-family:Anton,Impact,"Arial Narrow",sans-serif!important;font-size:39px!important;line-height:42.9px!important;letter-spacing:normal!important;text-transform:uppercase;color:#F1F5E4!important;white-space:nowrap}
html body .nt-tk h1 *{color:#F1F5E4!important}
html body .nt-tk h1 svg{width:44px;height:30px;flex:none;margin-top:6px;border-radius:4px;box-shadow:0 0 0 1px rgba(30,35,24,.18)}
html body .nt-tk .sub{margin:4px 0 0!important;font-size:16.8px!important;line-height:27.2px!important;max-width:none!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
html body .nt-tk .meta{margin:10px 0 0!important}
html body .nt-tk .kop-tel{margin:0!important;font-size:13.76px!important;line-height:17px!important;white-space:nowrap}
html[data-nt-tab="landen"] #p-landen>p.note:first-child,html[data-nt-tab="soorten"] #p-soorten>p.note:first-child{display:none}
html body #meer .jg-kop{height:166px!important;min-height:0!important;box-sizing:border-box!important;padding-top:21px!important;padding-bottom:44px!important;margin-top:-18px!important}
html body #meer .jg-kop h1{font-size:39px!important;line-height:42.9px!important;letter-spacing:normal!important;margin:0!important}
html body #meer .jg-kop .nt-onder{margin:4px 0 0!important;font-size:16.8px!important;line-height:27.2px!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
html body #meer .jg-kop .nt-goud{margin:10px 0 0!important;font-size:13.76px!important;line-height:17px!important;letter-spacing:.06em}
/* geen klein blaadje in de kop; Kaart-knop weg, zwevende terugknop (19-10-2026) */
html body .intro .wrap::after{display:none!important}
html body .jg-kop .terug{display:none!important}
.nt-fab{position:fixed;left:16px;bottom:84px;z-index:60;display:none;align-items:center;justify-content:center;width:54px;height:54px;border-radius:50%;background:#F2C14E;color:#163A22!important;border:2px solid #163A22;box-shadow:0 4px 14px rgba(0,0,0,.28);text-decoration:none!important;cursor:pointer}
.nt-fab svg{width:26px;height:26px}
html.pagemode .nt-fab,html.katmode .nt-fab{display:flex}
html.pagemode:has(#meer.on) .nt-fab{display:none!important}
/* zachte overgang tussen startpagina, top 10 en soortpagina's in plaats van een flits (19-10-2026) */
@view-transition{navigation:auto}
html{background:#163A22}
/* soortpagina Europa (19-10-2026) */
html body #katview .nt-soortkop{margin:-18px calc(-1 * var(--gut,16px)) 18px!important}
html body #katview .nt-soortkop .nt-h1{display:flex;align-items:flex-start;gap:12px;margin:0;font-family:Anton,Impact,"Arial Narrow",sans-serif;font-size:39px;line-height:42.9px;text-transform:uppercase;color:#F1F5E4;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
html body #katview .nt-soortkop .nt-h1 svg{width:44px;height:30px;flex:none;margin-top:6px;border-radius:4px;box-shadow:0 0 0 1px rgba(30,35,24,.18)}
html body #katview .nt-soortkop .nt-onder i{font-style:italic}
html body #katview .nt-oud{background:none!important;margin:0!important;padding:0!important;min-height:0!important;height:auto!important;color:inherit!important;overflow:visible!important}
html body #katview .nt-oud::before,html body #katview .nt-oud::after{display:none!important}
html body #katview .nt-oud>.terug,html body #katview .nt-oud h1,html body #katview .nt-oud .kat-sci,html body #katview .nt-oud .kat-kern{display:none!important}
html body #katview .nt-oud .kat-h{display:block!important}
html body #katview .nt-oud .kat-foto{position:relative;margin:0 0 6px}
html body #katview .nt-oud .kat-foto img{width:100%;border-radius:18px;box-shadow:0 0 0 4px #FBF8F1,0 8px 20px -10px rgba(0,0,0,.4)!important}
html body #katview .nt-oud .kat-foto figcaption,html body #katview .nt-oud .kat-foto figcaption a{color:var(--muted)!important}
html body #katview .kat-foto .nt-hw{position:absolute;top:12px;right:12px;margin:0!important;width:46px;height:46px;padding:0!important;border-radius:50%;background:#fff!important;justify-content:center;font-size:0!important;box-shadow:0 2px 8px rgba(0,0,0,.25)}
html body #katview .kat-foto .nt-hw .nt-hart{width:46px;height:46px}
html body #katview .nt-h2{font-family:Anton,Impact,"Arial Narrow",sans-serif;text-transform:uppercase;font-size:1.7rem;line-height:1.1;color:#163A22;margin:26px 0 4px;font-weight:400}
html body #katview .nt-paw{display:block;width:40px;height:16px;margin:0 0 12px}
html body #katview .nt-oud .kat-feit{display:grid!important;grid-template-columns:1fr 1fr!important;gap:10px!important;margin:0!important;border:0!important;background:none!important;padding:0!important}
html body #katview .nt-oud .kat-feit>div{background:#FBF8F1!important;border:1px solid var(--line,#DCD6C4)!important;border-radius:14px!important;padding:12px 14px!important;margin:0!important}
html body #katview .nt-oud .kat-feit>div[hidden]{display:none!important}
html body #katview .nt-oud .kat-feit dt{font-size:.85rem!important;color:var(--muted)!important;text-transform:none!important;letter-spacing:0!important;font-family:inherit!important;font-weight:400!important}
html body #katview .nt-oud .kat-feit dd{font-size:1.15rem!important;font-weight:800!important;color:var(--ink,#22301F)!important;margin:4px 0 0!important}
html body #katview .nt-leef{margin:0}
html body #katview .nt-leef>div{padding:10px 0;border-bottom:1px dashed var(--line,#DCD6C4)}
html body #katview .nt-leef>div:last-child{border-bottom:0}
html body #katview .nt-leef dt{font-weight:800;font-size:.9rem;color:#163A22}
html body #katview .nt-leef dd{margin:4px 0 0;font-size:1.05rem}
html body #katview .nt-bz{background:#F6F8EC;border-left:4px solid #A9C98A;border-radius:6px;padding:14px 16px;margin:0 0 12px}
html body #katview .nt-bz b{display:block;font-size:1.05rem;margin-bottom:4px}
html body #katview .nt-bz p{margin:0}
html body #katview .nt-oud .kat-spot{display:inline-block;margin:22px 0 4px}
/* menu: donkere tekst op de lichte achtergrond */
html body #menu,html body #menu nav a,html body #menu nav a span{color:var(--ink,#22301F)!important}
/* alle schermkoppen even hoog als de landgids */
html body .jg-kop.nt-vk{height:166px!important;min-height:0!important;box-sizing:border-box!important;padding-top:21px!important;padding-bottom:44px!important}
html body .jg-kop.nt-vk::before{top:-14px!important;right:-34px!important;bottom:auto!important;left:auto!important;width:150px!important;height:180px!important}
html body .jg-kop.nt-vk::after{height:30px!important}
html body .jg-kop.nt-vk h1:has(svg){display:flex!important;align-items:flex-start;gap:12px}
html body .jg-kop.nt-vk h1 svg{width:44px;height:30px;flex:none;margin-top:6px;border-radius:4px;box-shadow:0 0 0 1px rgba(30,35,24,.18)}
html body .jg-kop.nt-vk h1{font-size:39px!important;line-height:42.9px!important;letter-spacing:normal!important;margin:0!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
html body .jg-kop.nt-vk .nt-onder{margin:4px 0 0!important;font-size:16.8px!important;line-height:27.2px!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
html body .jg-kop.nt-vk .nt-goud{margin:10px 0 0!important;font-size:13.76px!important;line-height:17px!important;letter-spacing:.06em;min-height:17px}
/* zoekbalk en groepen bij Soorten */
.nt-spbox+#splist{display:none!important}
.nt-zk{margin:0 0 12px}
.nt-zk label{display:flex;align-items:center;gap:10px;height:48px;padding:0 18px;border:2px solid #1F5A33;border-radius:99px;background:#fff;box-shadow:0 1px 2px rgba(60,50,30,.06),0 10px 24px -14px rgba(60,50,30,.35)}
.nt-zk svg{width:22px;height:22px;flex:none;color:#1F5A33}
.nt-zk input{flex:1;min-width:0;border:0;outline:0;background:transparent;font:inherit;font-size:16.8px;color:#22301F;-webkit-appearance:none;appearance:none}
.nt-gt{margin:18px 0 10px!important}
.nt-gt button{all:unset;cursor:pointer;display:inline-flex;align-items:center;gap:8px;font:inherit;color:inherit;letter-spacing:inherit;text-transform:inherit}
.nt-gt .nt-chev{width:20px;height:20px;flex:none;transition:transform .2s}
.nt-gt button[aria-expanded="false"] .nt-chev{transform:rotate(180deg)}
.nt-gg[hidden],.nt-grp[hidden],.nt-gg .scard[hidden]{display:none!important}
.nt-geen2{color:var(--muted)}
.nt-onder{margin:8px 0 0;color:#D3E4C2!important;font-size:1.08rem;line-height:1.55}
.nt-goud{margin:8px 0 0;font-family:"Barlow Condensed","Arial Narrow","Roboto Condensed",sans-serif;font-weight:600;font-size:.86rem;letter-spacing:.06em;text-transform:uppercase;color:#F2C14E!important}
.nt-goud *{color:#F2C14E!important}
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
var AV=AVJSON,AVB=AVBJSON,zoom=document.getElementById("zoom"),row=document.getElementById("catrow"),bz=false;
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
  row.querySelectorAll(".catbtn[data-cat]").forEach(function(b){var s=b.dataset.cat,a=b.querySelector(".av");if(!s||!a)return;a.classList.toggle("nt-avu",!!(c&&AV[c]&&AV[c][s]&&!(AVB[c]&&AVB[c][s])));});
  var al=row.querySelector('.catbtn[data-cat=""] .av');if(al){if(al.dataset.ntN===undefined)al.dataset.ntN=al.textContent;
    var nt=String(c?Object.keys(AVB[c]||{}).length:al.dataset.ntN);if(al.textContent!==nt)al.textContent=nt;}
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
/* ---------- favorieten (alle landen samen) ---------- */
FAVJS
var IDX=IDXJSON,SPN=SPNJSON,MAP={nl:"nederland",be:"belgie",lu:"luxemburg",de:"duitsland",fr:"frankrijk",at:"oostenrijk",ch:"zwitserland",uk:"verenigd-koninkrijk",it:"italie",es:"spanje",ie:"ierland",pt:"portugal"};
var BASE=(window.__HOMEURL||"/wildekattengids/");
var HS='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-8-5-8-11a4.5 4.5 0 0 1 8-2.5A4.5 4.5 0 0 1 20 9c0 6-8 11-8 11z"/></svg>';
var FT={bewaar:{nl:"Bewaar als favoriet",en:"Save as favourite",fr:"Ajouter aux favoris",de:"Als Favorit speichern",it:"Salva nei preferiti",es:"Guardar en favoritos"},
  in:{nl:"In je favorieten",en:"In your favourites",fr:"Dans vos favoris",de:"In deinen Favoriten",it:"Nei tuoi preferiti",es:"En tus favoritos"},
  parken:{nl:"Parken",en:"Parks",fr:"Parcs",de:"Parks",it:"Parchi",es:"Parques"},soorten:{nl:"Soorten",en:"Species",fr:"Espèces",de:"Arten",it:"Specie",es:"Especies"},
  europa:{nl:"Europa (alle landen)",en:"Europe (all countries)",fr:"Europe (tous les pays)",de:"Europa (alle Länder)",it:"Europa (tutti i paesi)",es:"Europa (todos los países)"},
  leeg:{nl:"Nog geen favorieten.",en:"No favourites yet.",fr:"Pas encore de favoris.",de:"Noch keine Favoriten.",it:"Ancora nessun preferito.",es:"Todavía no hay favoritos."},
  weg:{nl:"Verwijder uit favorieten",en:"Remove from favourites",fr:"Retirer des favoris",de:"Aus Favoriten entfernen",it:"Rimuovi dai preferiti",es:"Quitar de favoritos"}};
function L2(){var l=(document.documentElement.lang||"nl").slice(0,2);return FT.in[l]?l:"en";}
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});}
/* oude favorieten zonder land: land opzoeken */
function vul(a){var nu=false;a.forEach(function(x){if(x.c)return;if(x.k==="loc"){for(var c in IDX){var l=IDX[c].filter(function(y){return y[2]===x.s;})[0];if(l){x.c=c;x.n=x.n||l[0];x.p=x.p||l[1];nu=true;break;}}}
  else{x.c="eu";var q=SPN[x.s];if(q){x.n=x.n||q[0];x.e=x.e||q[1];}nu=true;}});if(nu)favSchrijf(a);return a;}
function landNaam(c){if(c==="eu")return FT.europa[L2()];var z=document.querySelector('#zoom .chip[data-zoom="'+c+'"]');if(z){var k=z.cloneNode(true);k.querySelectorAll("svg,.n").forEach(function(x){x.remove();});return k.textContent.trim();}return c.toUpperCase();}
function favLijst(){var el=document.getElementById("nt-favlist");if(!el)return;var a=vul(favLees()),l=L2();
  if(!a.length){el.innerHTML='<p class="nt-fleeg">'+FT.leeg[l]+'</p>';return;}
  var order=Object.keys(MAP).concat(["eu"]),o="";
  order.forEach(function(c){var it=a.map(function(x,i){return [x,i];}).filter(function(p){return p[0].c===c;});if(!it.length)return;
    o+='<p class="nt-fh">'+esc(landNaam(c))+'</p><ul class="nt-fl">';
    ["loc","sp"].forEach(function(k){it.filter(function(p){return p[0].k===k;}).forEach(function(p){var x=p[0],h;
      if(k==="loc")h=BASE+MAP[c]+"/#locatie/"+x.s;else h=c==="eu"?BASE+"soort/"+x.s+"/":BASE+MAP[c]+"/#soort/"+x.s;
      var nm=(l!=="nl"&&x.e)?x.e:(x.n||x.s),sub=k==="loc"?(x.p||""):FT.soorten[l];
      o+='<li><a href="'+h+'">'+esc(nm)+'<small>'+esc(sub)+'</small></a><button type="button" class="nt-hart" aria-pressed="true" data-wi="'+p[1]+'" aria-label="'+FT.weg[l]+'">'+HS+'</button></li>';});});
    o+='</ul>';});
  el.innerHTML=o;}
window.__NTFAV=favLijst;
/* ---------- scherm Meer: de links uit het menu als lijst, Favorieten bovenaan, Ko-fi niet (staat onderaan) ---------- */
var PIJL='<svg class="nt-pijl" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>';
var EXTRA_ICO={over:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="currentColor"/><circle cx="12" cy="7.4" r="1.5" fill="#FBF8F1"/><path d="M12 11v6.5" stroke="#FBF8F1" stroke-width="2.4" stroke-linecap="round"/></svg>',
  ster:'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 3l2.7 5.6 6.1.8-4.5 4.2 1.1 6.1L12 16.8l-5.4 2.9 1.1-6.1-4.5-4.2 6.1-.8z"/></svg>',
  spot:'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6.5" cy="15.5" r="3.5"/><circle cx="17.5" cy="15.5" r="3.5"/><path d="M10 15h4M5 12l2-6h2l1 5M19 12l-2-6h-2l-1 5"/></svg>'};
function meerLijst(){var el=document.getElementById("nt-meerlist"),m=document.getElementById("menu");if(!el||!m)return;
  var a=[].slice.call(m.querySelectorAll("nav a")).filter(function(x){return !/ko-fi\.com/.test(x.getAttribute("href")||"");});
  a.sort(function(x,y){return (y.dataset.nav==="favorieten")-(x.dataset.nav==="favorieten");});
  el.innerHTML=a.map(function(x){var c=x.cloneNode(true),lc=(x.className.match(/\bl-[a-z]{2}\b/)||[""])[0];c.removeAttribute("class");
    if(!c.querySelector("svg"))c.insertAdjacentHTML("afterbegin",x.dataset.nav==="over"?EXTRA_ICO.over:EXTRA_ICO.spot);
    if(x.dataset.nav==="geboren"){var o=c.querySelector("svg");if(o)o.outerHTML=EXTRA_ICO.ster;}
    c.insertAdjacentHTML("beforeend",PIJL);return '<li'+(lc?' class="'+lc+'"':'')+'>'+c.outerHTML+'</li>';}).join("");
  mm();}
function mm(){var b=document.getElementById("nw-sbar-start");if(!b)return;var me=b.querySelector('[data-k="meer"]'),op=document.documentElement.classList.contains("pagemode")||/\/top10\//.test(location.pathname)||location.hash==="#top10";
  if(!me)return;me.classList.toggle("on",op);if(op)b.querySelectorAll("[data-k]").forEach(function(x){if(x!==me)x.classList.remove("on");});
  else if(!b.querySelector(".on")&&!document.documentElement.classList.contains("katmode")){var h=b.querySelector('[data-k="home"]');if(h)h.classList.add("on");}}
window.__NTMEER=meerLijst;
new MutationObserver(function(){setTimeout(mm,0);}).observe(document.documentElement,{attributes:true,attributeFilter:["class"]});
window.addEventListener("popstate",function(){setTimeout(mm,0);});window.addEventListener("hashchange",function(){setTimeout(mm,0);});
if(location.hash==="#meer")setTimeout(meerLijst,0);
document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest('#nw-sbar-start [data-k="meer"]');if(b&&b.dataset.start!==undefined||b&&document.getElementById("nt-meerlist"))setTimeout(function(){window.scrollTo(0,0);},30);});
document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest("#nt-favlist .nt-hart");if(!b)return;var a=favLees();a.splice(+b.dataset.wi,1);favSchrijf(a);favLijst();});
/* ---------- groene kop per scherm (19-10-2026): Kaart houdt de grote kop, Landen en Soorten krijgen een korte kop, Meer een regel eronder ---------- */
var KT={kaart:{h:{nl:"Europa",en:"Europe",fr:"Europe",de:"Europa",it:"Europa",es:"Europa"},
    s:{nl:"Wilde katachtigen in dierentuinen en parken",en:"Wild cats in zoos and animal parks",fr:"Félins sauvages dans les zoos et parcs",de:"Wilde Katzen in Zoos und Tierparks",it:"Felini selvatici in zoo e parchi",es:"Felinos salvajes en zoos y parques"}},
  landen:{h:{nl:"Landen",en:"Countries",fr:"Pays",de:"Länder",it:"Paesi",es:"Países"},
    s:{nl:"Tik op een land voor de volledige gids",en:"Tap a country for its full guide",fr:"Touchez un pays pour ouvrir son guide complet",de:"Tippe auf ein Land für den ganzen Guide",it:"Tocca un paese per la guida completa",es:"Toca un país para ver su guía completa"}},
  soorten:{h:{nl:"Soorten",en:"Species",fr:"Espèces",de:"Arten",it:"Specie",es:"Especies"},
    s:{nl:"Waar zie je welke kat in Europa?",en:"Where can you see each cat in Europe?",fr:"Où voir chaque félin en Europe ?",de:"Wo siehst du welche Katze in Europa?",it:"Dove vedere ogni felino in Europa?",es:"¿Dónde ver cada felino en Europa?"}},
  meer:{s:{nl:"Favorieten, top 10, geboortes en meer",en:"Favourites, top 10, births and more",fr:"Favoris, top 10, naissances et plus",de:"Favoriten, Top 10, Geburten und mehr",it:"Preferiti, top 10, nascite e altro",es:"Favoritos, top 10, nacimientos y más"}}};
function L6j(o){return ["nl","en","fr","de","it","es"].map(function(l){return '<span class="l-'+l+'">'+o[l]+'</span>';}).join("");}
var iw=document.querySelector(".intro .wrap"),tel=document.getElementById("kop-tel"),HT=document.documentElement;
if(iw&&tel&&document.getElementById("p-landen")&&!iw.querySelector(".nt-tk")){
  var kk=document.createElement("div");kk.className="nt-tk";
  var EUV='<svg viewBox="0 0 30 20" aria-hidden="true" preserveAspectRatio="none"><rect width="30" height="20" fill="#003399"/><g fill="#FFCC00">'+[0,1,2,3,4,5,6,7,8,9,10,11].map(function(i){var a=i*Math.PI/6,x=15+6*Math.sin(a),y=10-6*Math.cos(a);return '<circle cx="'+x.toFixed(2)+'" cy="'+y.toFixed(2)+'" r=".9"/>';}).join("")+'</g></svg>';
  kk.innerHTML=["kaart","landen","soorten"].map(function(t){return '<div data-t="'+t+'"><h1>'+EUV+'<span class="nt-tt">'+L6j(KT[t].h)+'</span></h1><p class="sub">'+L6j(KT[t].s)+'</p><div class="meta"><p class="kop-tel nt-tel"></p></div></div>';}).join("");
  iw.appendChild(kk);HT.classList.add("nt-tk-on");window.__NTEUV=EUV;
  var telBij=function(){var d=tel.textContent.split(" · "),k=kk.querySelector('[data-t="kaart"] .nt-tel'),a=kk.querySelector('[data-t="landen"] .nt-tel'),b=kk.querySelector('[data-t="soorten"] .nt-tel'),x=d.slice(0,2).join(" · "),y=d[2]||"",z=tel.textContent;
    var gk=document.querySelectorAll('.nt-spbox [data-g="big"] .scard').length,kl=document.querySelectorAll('.nt-spbox [data-g="small"] .scard').length,ll=(HT.lang||"nl").slice(0,2);
    var GW={nl:["grote","kleine"],en:["big","small"],fr:["grands","petits"],de:["groß","klein"],it:["grandi","piccoli"],es:["grandes","pequeños"]}[ll]||["big","small"];
    if(gk+kl)y+=" · "+gk+" "+GW[0]+" · "+kl+" "+GW[1];
    if(k.textContent!==z)k.textContent=z;if(a.textContent!==x)a.textContent=x;if(b.textContent!==y)b.textContent=y;};
  window.__NTTEL=telBij;
  new MutationObserver(telBij).observe(tel,{childList:true,characterData:true,subtree:true});telBij();
  var tabNu=function(){var t=["landen","soorten"].filter(function(x){var e=document.getElementById("p-"+x);return e&&e.classList.contains("on");})[0]||"kaart";if(HT.getAttribute("data-nt-tab")!==t)HT.setAttribute("data-nt-tab",t);};
  ["kaart","landen","soorten"].forEach(function(x){var e=document.getElementById("p-"+x);if(e)new MutationObserver(tabNu).observe(e,{attributes:true,attributeFilter:["class"]});});tabNu();}
/* witte en gele regel in de groene kop van Meer en de schermen eronder (na de jungle-laag, dus pas na DOMContentLoaded) */
var KR={meer:KT.meer.s,
  favorieten:{nl:"Je bewaarde parken en soorten",en:"Your saved parks and species",fr:"Vos parcs et espèces enregistrés",de:"Deine gespeicherten Parks und Arten",it:"I tuoi parchi e specie salvati",es:"Tus parques y especies guardados"},
  geboren:{nl:"Jongen in alle landen, nieuwste eerst",en:"Young in every country, newest first",fr:"Jeunes dans tous les pays, plus récents d’abord",de:"Jungtiere in allen Ländern, neueste zuerst",it:"Cuccioli in tutti i paesi, i più recenti prima",es:"Crías en todos los países, las más recientes primero"},
  perpark:{nl:"Welk park heeft de meeste katten?",en:"Which park has the most cats?",fr:"Quel parc a le plus de félins ?",de:"Welcher Park hat die meisten Katzen?",it:"Quale parco ha più felini?",es:"¿Qué parque tiene más felinos?"},
  typen:{nl:"Dierentuin, dierenpark, opvang en meer",en:"Zoo, animal park, sanctuary and more",fr:"Zoo, parc animalier, refuge et plus",de:"Zoo, Tierpark, Auffangstation und mehr",it:"Zoo, parco faunistico, centro di recupero e altro",es:"Zoo, parque de animales, santuario y más"},
  over:{nl:"Wie, wat en waar de gegevens vandaan komen",en:"Who, what and where the information comes from",fr:"Qui, quoi et d’où viennent les données",de:"Wer, was und woher die Angaben stammen",it:"Chi, cosa e da dove vengono i dati",es:"Quién, qué y de dónde vienen los datos"},
  top10:{nl:"De parken die een bezoek het meest waard zijn",en:"The parks most worth a visit",fr:"Les parcs qui valent le plus le détour",de:"Die Parks, die sich am meisten lohnen",it:"I parchi che valgono di più una visita",es:"Los parques que más merecen la visita"}};
var FB={nl:"{n} bewaard",en:"{n} saved",fr:"{n} enregistrés",de:"{n} gespeichert",it:"{n} salvati",es:"{n} guardados"};
function favTel(){var g=document.querySelector("#favorieten .nt-goud");if(!g)return;var n=0;try{n=favLees().length;}catch(_){}
  var h=["nl","en","fr","de","it","es"].map(function(l){return '<span class="l-'+l+'">'+FB[l].replace("{n}",n)+'</span>';}).join("");if(g.innerHTML!==h)g.innerHTML=h;}
function kopRegels(){var st=document.querySelector(".intro .stamp"),dt=st?st.innerHTML:"";
  Object.keys(KR).forEach(function(id){var k=id==="top10"?((/\/top10\//.test(location.pathname)||location.hash==="#top10")?document.querySelector("#katview .jg-kop"):null):document.querySelector("#"+id+" .jg-kop");
    if(!k||k.querySelector(".nt-onder"))return;k.classList.add("nt-vk");
    if(id==="meer"&&window.__NTEUV){var h1=k.querySelector("h1");if(h1&&!h1.querySelector("svg")){h1.innerHTML='<span class="nt-tt">'+h1.innerHTML+'</span>';h1.insertAdjacentHTML("afterbegin",window.__NTEUV);}}
    k.insertAdjacentHTML("beforeend",'<p class="nt-onder">'+L6j(KR[id])+'</p><p class="nt-goud">'+(id==="favorieten"?"":dt)+'</p>');});
  favTel();}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",function(){setTimeout(kopRegels,0);});else setTimeout(kopRegels,0);
window.addEventListener("storage",favTel);document.addEventListener("click",function(){setTimeout(favTel,50);});
/* Soorten op de startpagina zoals in de landgids: zoekbalk, grote en kleine katten (19-10-2026) */
(function(){var sp=document.getElementById("splist");if(!sp||!document.getElementById("p-soorten"))return;
  var BIG=["leeuw","tijger","luipaard","jaguar","sneeuwluipaard","nevelpanter"];
  var GT={big:{nl:"Pantherinae (grote katten)",en:"Pantherinae (big cats)",fr:"Pantherinae (grands félins)",de:"Pantherinae (Großkatzen)",it:"Pantherinae (grandi felini)",es:"Pantherinae (grandes felinos)"},
    small:{nl:"Felinae (kleine katten)",en:"Felinae (small cats)",fr:"Felinae (petits félins)",de:"Felinae (Kleinkatzen)",it:"Felinae (piccoli felini)",es:"Felinae (pequeños felinos)"}};
  var ZP={nl:"Zoek een soort",en:"Search for a species",fr:"Chercher une espèce",de:"Art suchen",it:"Cerca una specie",es:"Busca una especie"};
  var GEEN={nl:"Niets gevonden.",en:"Nothing found.",fr:"Aucun résultat.",de:"Nichts gefunden.",it:"Nessun risultato.",es:"No se ha encontrado nada."};
  var ZS='<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg>';
  var CH='<svg class="nt-chev" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 15l6-6 6 6"/></svg>';
  var box=document.createElement("div");box.className="nt-spbox";
  box.innerHTML='<div class="nt-zk"><label>'+ZS+'<input type="search" id="nt-spz" autocomplete="off"></label></div><p class="nt-geen2" hidden>'+L6j(GEEN)+'</p>'
    +["big","small"].map(function(g){return '<div class="nt-grp" data-g="'+g+'"><p class="lbl nt-gt"><button type="button" aria-expanded="true">'+L6j(GT[g])+CH+'</button></p><div class="grid nt-gg"></div></div>';}).join("");
  sp.parentNode.insertBefore(box,sp);
  var inp=box.querySelector("input");
  function ph(){var l=(HT.lang||"nl").slice(0,2);inp.placeholder=ZP[l]||ZP.en;inp.setAttribute("aria-label",inp.placeholder);}ph();
  new MutationObserver(ph).observe(HT,{attributes:true,attributeFilter:["lang"]});
  function slug(a){var m=(a.getAttribute("href")||"").match(/soort\/([^\/]+)\//);return m?m[1]:"";}
  function verdeel(){var c=[].slice.call(sp.children);if(!c.length)return;var gb=box.querySelector('[data-g="big"] .nt-gg'),gs=box.querySelector('[data-g="small"] .nt-gg');
    gb.innerHTML="";gs.innerHTML="";c.forEach(function(a){(BIG.indexOf(slug(a))>=0?gb:gs).appendChild(a);});zoek();if(window.__NTTEL)window.__NTTEL();}
  function zoek(){var q=inp.value.trim().toLowerCase(),tot=0;
    box.querySelectorAll(".nt-grp").forEach(function(g){var n=0;g.querySelectorAll(".scard").forEach(function(a){var ok=!q||a.textContent.toLowerCase().indexOf(q)>=0;a.hidden=!ok;if(ok)n++;});g.hidden=!n;tot+=n;});
    box.querySelector(".nt-geen2").hidden=!!tot;}
  inp.addEventListener("input",zoek);
  box.addEventListener("click",function(e){var b=e.target.closest(".nt-gt button");if(!b)return;var open=b.getAttribute("aria-expanded")!=="true";b.setAttribute("aria-expanded",String(open));b.closest(".nt-grp").querySelector(".nt-gg").hidden=!open;});
  new MutationObserver(verdeel).observe(sp,{childList:true});verdeel();
})();
/* losse schermen (onder Meer) openen altijd bovenaan, ook als de browser naar het anker springt (19-10-2026) */
try{history.scrollRestoration="manual";}catch(_){}
[].forEach.call(document.querySelectorAll("section.page"),function(pgs){new MutationObserver(function(){if(pgs.classList.contains("on")){window.scrollTo(0,0);setTimeout(function(){window.scrollTo(0,0);},0);setTimeout(function(){window.scrollTo(0,0);},120);}}).observe(pgs,{attributes:true,attributeFilter:["class"]});});
if(document.querySelector("section.page.on"))setTimeout(function(){window.scrollTo(0,0);},120);
/* top 10 in #katview: groene kop opnieuw zetten na elke opbouw (filter, taal, openen op de startpagina) */
(function(){var kv=document.getElementById("katview");if(!kv)return;
  function wrap(){if(!kv.querySelector(".toplist"))return;var t=kv.querySelector(".terug");if(!t||t.parentElement.classList.contains("jg-kop"))return;
    var k=document.createElement("div");k.className="jg-kop";t.parentNode.insertBefore(k,t);var x=t.nextElementSibling;k.appendChild(t);
    while(x&&(x.tagName==="H1"||(x.tagName==="P"&&x.classList.contains("sub"))||x.classList.contains("kat-h"))){var nx=x.nextElementSibling;k.appendChild(x);x=nx;}
    var u=k.querySelectorAll(".sub, .kat-sum");for(var j=u.length-1;j>=0;j--){u[j].classList.add("jg-uitleg");k.parentNode.insertBefore(u[j],k.nextSibling);}
    kopRegels();}
  new MutationObserver(function(){setTimeout(wrap,0);}).observe(kv,{childList:true});setTimeout(wrap,0);})();
function bovenaan(){if(document.querySelector("section.page.on")||location.hash==="#top10"){window.scrollTo(0,0);setTimeout(function(){window.scrollTo(0,0);},150);setTimeout(function(){window.scrollTo(0,0);},450);}}
window.addEventListener("load",bovenaan);window.addEventListener("pageshow",bovenaan);
/* soortpagina zoals in de landgids: groene kop, hartje op de foto, Kenmerken, Leefwijze en Bijzonder (19-10-2026) */
(function(){var kv=document.getElementById("katview"),SI=SIJSON;if(!kv||!window.__KAT)return;
  var LG=["nl","en","fr","de","it","es"],BIGS=["leeuw","tijger","luipaard","jaguar","sneeuwluipaard","nevelpanter"];
  var W={kenm:{nl:"Kenmerken",en:"Characteristics",fr:"Caractéristiques",de:"Merkmale",it:"Caratteristiche",es:"Características"},
    staart:{nl:"Staart",en:"Tail",fr:"Queue",de:"Schwanz",it:"Coda",es:"Cola"},leven:{nl:"Levensduur",en:"Lifespan",fr:"Longévité",de:"Lebensdauer",it:"Longevità",es:"Longevidad"},
    leef:{nl:"Leefwijze",en:"Way of life",fr:"Mode de vie",de:"Lebensweise",it:"Stile di vita",es:"Modo de vida"},
    l0:{nl:"Verspreiding",en:"Range",fr:"Répartition",de:"Verbreitung",it:"Distribuzione",es:"Distribución"},
    l1:{nl:"Leefgebied",en:"Habitat",fr:"Habitat",de:"Lebensraum",it:"Habitat",es:"Hábitat"},
    l2:{nl:"Voedsel",en:"Diet",fr:"Alimentation",de:"Nahrung",it:"Alimentazione",es:"Alimentación"},
    l3:{nl:"Sociaal gedrag",en:"Social behaviour",fr:"Comportement social",de:"Sozialverhalten",it:"Comportamento sociale",es:"Comportamiento social"},
    bijz:{nl:"Bijzonder",en:"Special",fr:"Particularités",de:"Besonderes",it:"Particolarità",es:"Curiosidades"},
    b0:{nl:"Kenmerkend",en:"Distinctive",fr:"Caractéristique",de:"Typisch",it:"Caratteristico",es:"Distintivo"},
    b1:{nl:"Wist je dat?",en:"Did you know?",fr:"Le saviez-vous ?",de:"Wusstest du?",it:"Lo sapevi?",es:"¿Sabías que…?"},
    groot:{nl:"grote katten",en:"big cats",fr:"grands félins",de:"Großkatzen",it:"grandi felini",es:"grandes felinos"},
    klein:{nl:"kleine katten",en:"small cats",fr:"petits félins",de:"Kleinkatzen",it:"piccoli felini",es:"pequeños felinos"}};
  var JR={nl:["Ongeveer ","jaar","Onbekend"],en:["About ","years","Unknown"],fr:["Environ ","ans","Inconnu"],de:["Etwa ","Jahre","Unbekannt"],it:["Circa ","anni","Sconosciuto"],es:["Aproximadamente ","años","Desconocido"]};
  function P(o){return LG.map(function(l){return '<span class="l-'+l+'">'+o[l]+'</span>';}).join("");}
  function E(t){return String(t==null?"":t).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});}
  function D(i){return LG.map(function(l){var a=SI[l]||SI.en||SI.nl;return '<span class="l-'+l+'">'+E(a?a[i]:"")+'</span>';}).join("");}
  function leven(){var x=SI.leven||"";return LG.map(function(l){var r=JR[l];return '<span class="l-'+l+'">'+E(x.replace(/^Ongeveer /,r[0]).replace(/ jaar$/," "+r[1]).replace(/^Onbekend$/,r[2]))+'</span>';}).join("");}
  var PAW='<svg class="nt-paw" viewBox="0 0 40 16" aria-hidden="true"><g fill="#C8552B"><circle cx="6" cy="10" r="3.2"/><circle cx="3" cy="5" r="1.6"/><circle cx="7" cy="3.6" r="1.6"/><circle cx="11" cy="5.6" r="1.6"/><circle cx="24" cy="8" r="3.2"/><circle cx="21" cy="3" r="1.6"/><circle cx="25" cy="1.6" r="1.6"/><circle cx="29" cy="3.6" r="1.6"/></g></svg>';
  function h2(o){return '<h2 class="nt-h2">'+P(o)+'</h2>'+PAW;}
  function bouw(){if(kv.querySelector(".nt-soortkop"))return;var oud=kv.querySelector(".jg-kop.jg-foto");
    if(!oud){var kh=kv.querySelector(".kat-h");if(!kh)return;oud=document.createElement("div");oud.className="jg-kop jg-foto";kh.parentNode.insertBefore(oud,kh);
      var tg=kv.querySelector(":scope > .terug");if(tg)oud.appendChild(tg);oud.appendChild(kh);}
    var h=oud.querySelector("h1"),sci=oud.querySelector(".kat-sci"),kern=oud.querySelector(".kat-kern");
    var slug=window.__KAT,groot=BIGS.indexOf(slug)>=0,dl=kern?kern.textContent.split(" · ").slice(0,2).join(" · "):"";
    var k=document.createElement("div");k.className="jg-kop nt-vk nt-soortkop";
    k.innerHTML='<p class="nt-h1" role="heading" aria-level="1">'+(window.__NTEUV||"")+'<span class="nt-tt">'+E(h?h.textContent:"")+'</span></p><p class="nt-onder"><i>'+E(sci?sci.textContent:"")+'</i></p><p class="nt-goud">'+E(dl)+(dl?" · ":"")+P(groot?W.groot:W.klein)+'</p>';
    kv.insertBefore(k,kv.firstChild);oud.classList.add("nt-oud");
    /* hartje op de foto */
    hart();setTimeout(hart,60);setTimeout(hart,400);
    /* Kenmerken */
    var f=oud.querySelector(".kat-feit");
    if(f){f.insertAdjacentHTML("beforebegin",h2(W.kenm));var divs=[].slice.call(f.children);
      var wild=divs.filter(function(d){return d.dataset.nt&&!d.classList.contains("wd");})[0]||divs[0];
      if(SI.staart)f.insertAdjacentHTML("beforeend",'<div><dt>'+P(W.staart)+'</dt><dd>'+E(SI.staart)+'</dd></div>');
      if(SI.leven)f.insertAdjacentHTML("beforeend",'<div><dt>'+P(W.leven)+'</dt><dd>'+leven()+'</dd></div>');
      if(wild)f.appendChild(wild);
      var wd=f.querySelector(".wd");if(wd&&SI.nl)wd.hidden=true;
      if(SI.nl||SI.en){var o='<div class="nt-blok">'+h2(W.leef)+'<dl class="nt-leef">'+[0,1,2,3].map(function(i){return '<div><dt>'+P(W["l"+i])+'</dt><dd>'+D(i)+'</dd></div>';}).join("")+'</dl></div>'
        +'<div class="nt-blok">'+h2(W.bijz)+[4,5].map(function(i){return '<div class="nt-bz"><b>'+P(W["b"+(i-4)])+'</b><p>'+D(i)+'</p></div>';}).join("")+'</div>';
        f.insertAdjacentHTML("afterend",o);}}
  }
  function hart(){var fg=kv.querySelector(".kat-foto"),hw=kv.querySelector(".nt-hw");if(fg&&hw&&hw.parentNode!==fg)fg.appendChild(hw);}
  new MutationObserver(function(){setTimeout(bouw,0);setTimeout(hart,30);}).observe(kv,{childList:true,subtree:true});
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",function(){setTimeout(bouw,30);});else setTimeout(bouw,30);
})();
/* zwevende terugknop: terug in de geschiedenis, anders naar Meer (startpagina) of de oude terugknop */
(function(){var TB={nl:"Terug",en:"Back",fr:"Retour",de:"Zurück",it:"Indietro",es:"Volver"};
  var f=document.createElement("a");f.className="nt-fab";f.href="#";
  f.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>';
  var lab=function(){var l=(document.documentElement.lang||"nl").slice(0,2);f.setAttribute("aria-label",TB[l]||TB.en);};lab();
  new MutationObserver(lab).observe(document.documentElement,{attributes:true,attributeFilter:["lang"]});
  document.body.appendChild(f);
  var plek=function(){var b=document.getElementById("nw-sbar-start");if(b&&b.offsetHeight)f.style.bottom=(b.offsetHeight+14)+"px";};plek();window.addEventListener("resize",plek);setTimeout(plek,500);
  f.addEventListener("click",function(e){e.preventDefault();
    var eigen=document.referrer&&document.referrer.indexOf(location.origin+(window.__HOMEURL||"/wildekattengids/"))===0;
    if(history.length>1&&(history.state||eigen)){history.back();return;}
    if(document.getElementById("nt-meerlist")&&document.documentElement.classList.contains("pagemode")){location.hash="#meer";return;}
    var t=[].slice.call(document.querySelectorAll(".terug")).filter(function(a){return a.getAttribute("href");})[0];
    location.href=t?t.getAttribute("href"):(window.__HOMEURL||"/wildekattengids/");});
})();
/* hartje in het infovak van de kaart en op de soortpagina */
function heeft(k,c,s){return favLees().some(function(x){return x.k===k&&x.c===c&&x.s===s;});}
function wissel(k,c,s,extra){var a=favLees(),i=-1;a.forEach(function(x,j){if(i<0&&x.k===k&&x.c===c&&x.s===s)i=j;});
  if(i>=0)a.splice(i,1);else{var it={k:k,c:c,s:s};for(var q in extra)it[q]=extra[q];a.push(it);}favSchrijf(a);}
function knop(on){var l=L2();return '<span class="nt-hart" aria-pressed="'+on+'">'+HS+'</span>'+(on?FT.in[l]:FT.bewaar[l]);}
var LASTC=null;
document.addEventListener("click",function(e){var m=e.target.closest&&e.target.closest(".mk[data-c]");if(m)LASTC=m.dataset.c;},true);
function infoHart(){if(!info||info.classList.contains("nt-leeg")||!info.querySelector("ul.cats"))return;var h=info.querySelector("h3");if(!h||info.querySelector(".nt-hw"))return;
  var nm=h.textContent.trim(),hit=null;
  (LASTC?[LASTC]:[]).concat(Object.keys(IDX)).some(function(c){var l=(IDX[c]||[]).filter(function(y){return y[0]===nm;})[0];if(l){hit=[c,l];return true;}return false;});
  if(!hit)return;var c=hit[0],l=hit[1],b=document.createElement("button");b.type="button";b.className="nt-hw";b.innerHTML=knop(heeft("loc",c,l[2]));
  b.addEventListener("click",function(){wissel("loc",c,l[2],{n:l[0],p:l[1]});b.innerHTML=knop(heeft("loc",c,l[2]));});h.insertAdjacentElement("afterend",b);}
if(info)new MutationObserver(function(){setTimeout(infoHart,0);}).observe(info,{childList:true});
function katHart(){var kv=document.getElementById("katview");if(!kv)return;var h=kv.querySelector("h1");var s=slugNu();if(!h||!s||kv.querySelector(".nt-hw"))return;
  var b=document.createElement("button");b.type="button";b.className="nt-hw";b.innerHTML=knop(heeft("sp","eu",s));
  b.addEventListener("click",function(){wissel("sp","eu",s,{n:h.textContent.trim()});b.innerHTML=knop(heeft("sp","eu",s));});h.insertAdjacentElement("afterend",b);}
if(kv)new MutationObserver(function(){setTimeout(katHart,0);}).observe(kv,{childList:true});katHart();
if(location.hash==="#favorieten")setTimeout(favLijst,0);
/* lijst opnieuw opbouwen telkens als het scherm Favorieten opent (19-10-2026) */
(function(){var fp=document.getElementById("favorieten");if(!fp)return;
  new MutationObserver(function(){if(fp.classList.contains("on")){favLijst();if(typeof favTel==="function")favTel();}}).observe(fp,{attributes:true,attributeFilter:["class"]});
  window.addEventListener("pageshow",function(){if(fp.classList.contains("on"))favLijst();});})();
/* onderbalk: Soorten aan op een soortpagina */
var bar=document.getElementById("nw-sbar-start");
if(bar&&window.__KAT){var s=bar.querySelector('[data-k="soorten"]');if(s)s.classList.add("on");}
})();</script>
"""
EU_T_OUD = 'home:{nl:"Home",en:"Home",fr:"Accueil",de:"Start",it:"Home",es:"Inicio"}'
EU_T_NIEUW = 'home:{nl:"Kaart",en:"Map",fr:"Carte",de:"Karte",it:"Mappa",es:"Mapa"}'


def europa(pad, wild, av, idx, spn=None, soort=False, avb=None, info=None):
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
    # schermen Favorieten en Meer (net als Recent geboren); de start-JS kent alleen de pagina's in PAGES
    doc = re.sub(r'const PAGES=\[[^\]]*\];', 'const PAGES=["geboren","perpark","typen","over","favorieten","meer"];', doc, count=1)
    if 'PAGE==="meer"' not in doc:
        doc = doc.replace('function renderPage(){', 'function renderPage(){if(PAGE==="meer"&&window.__NTMEER)window.__NTMEER();', 1)
    if 'id="meer"' not in doc and '<section class="page" id="over"' in doc:
        doc = doc.replace('<section class="page" id="over"', MEERPAGE + '<section class="page" id="over"', 1)
    # Meer in de onderbalk opent het scherm Meer in plaats van het menu
    doc = doc.replace('#over" data-k="meer"', '#meer" data-k="meer"', 1)
    doc = doc.replace("""var a=e.target.closest('[data-k="meer"]');if(!a)return;""", "var a=null;if(!a)return;", 1)
    doc = doc.replace('function renderPage(){if(PAGE==="geboren")', 'function renderPage(){if(PAGE==="favorieten"&&window.__NTFAV)window.__NTFAV();if(PAGE==="geboren")', 1)
    if 'id="favorieten"' not in doc and '<section class="page" id="over"' in doc:
        doc = doc.replace('<section class="page" id="over"', FAVPAGE + '<section class="page" id="over"', 1)
    m = re.search(r'<a href="([^"]*)#geboren" data-nav="geboren">', doc)
    if m and 'data-nav="favorieten"' not in doc:
        # Favorieten bovenaan het menu, voor de top 10 (19-10-2026); zelfde volgorde als het scherm Meer
        fav = f'<a href="{m.group(1)}#favorieten" data-nav="favorieten">{FAVICO}{L6("Favorieten", "Favourites")}</a>'
        t10 = re.search(r'<a href="[^"]*" data-nav="top10">', doc)
        doc = doc.replace(t10.group(0) if t10 else m.group(0), fav + (t10.group(0) if t10 else m.group(0)), 1)
    js = (EU_JS.replace("WILDJSON", json.dumps(wild, ensure_ascii=False)).replace("AVJSON", json.dumps(av, ensure_ascii=False)).replace("AVBJSON", json.dumps(avb, ensure_ascii=False))
          .replace("IDXJSON", json.dumps(idx, ensure_ascii=False)).replace("SPNJSON", json.dumps(spn, ensure_ascii=False)).replace("FAVJS", FAVJS)
          .replace("SIJSON", json.dumps(info or {}, ensure_ascii=False)).replace("COLJSON", json.dumps(huisstijl.TCOL)).replace("GLYJSON", json.dumps(huisstijl.GLY)))
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


def soortinfo():
    """Leefwijze en Bijzonder per soort (slug) in nl/en/fr/de/it/es, uit de landengidsen in bron/gidsen."""
    import glob
    info = {}
    taal = {"SPEN": "en", "SPFR": "fr", "SPDE": "de", "SPIT": "it", "SPES": "es"}
    for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gidsen", "*.html"))):
        t = open(f, encoding="utf-8").read()
        i = t.find("const SPECIES=[")
        if i >= 0:
            for r in t[i:t.index("];", i)].split("\n")[1:]:
                r = r.strip().rstrip(",")
                if not r.startswith("["):
                    continue
                try:
                    a = json.loads(r)
                except Exception:
                    continue
                d = info.setdefault(slug_py(a[0]), {})
                d.setdefault("nl", a[9:15]); d.setdefault("staart", a[7]); d.setdefault("leven", a[8])
        for var, l in taal.items():
            m = re.search(r"const " + var + r"=(\{.*?\});\s*$", t, flags=re.M)
            if m:
                try:
                    obj = json.loads(m.group(1))
                except Exception:
                    obj = None
            else:
                obj = None
                j = t.find("const " + var + "={\n")
                if j >= 0:
                    body = t[j + len("const " + var + "="):t.index("\n};", j) + 2]
                    try:
                        obj = json.loads(re.sub(r",\s*}$", "}", body))
                    except Exception:
                        obj = None
            for k, v in (obj or {}).items():
                if isinstance(v, list) and len(v) >= 8:
                    info.setdefault(slug_py(k), {}).setdefault(l, v[2:8])
    return info


def maak_europa():
    gids = open(os.path.join(ROOT, "nederland-oud", "index.html"), encoding="utf-8").read()
    wild = {slug_py(k): v for k, v in json.loads(re.search(r"const WILD=(\{.*?\});", gids).group(1)).items()}
    # per land: soort -> aantal locaties (ook onzeker), uit de gegevens van de hoofdpagina
    st = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    i = st.index("const D=")
    D = json.loads(st[i + 8:st.index("\n", i)].rstrip(";"))
    av, avb = {}, {}
    for c, v in D.items():
        if not isinstance(v, dict) or "locs" not in v:
            continue
        cnt, bev = {}, {}
        for s in D["sp"]:
            al = {s[0]} | set(s[5])
            n = sum(1 for l in v["locs"] if any(x[4] in al for x in l[5]))
            if n:
                cnt[s[0]] = n
            b = sum(1 for l in v["locs"] if any(x[4] in al and x[3] in "gybr" for x in l[5]))
            if b:
                bev[s[0]] = b
        av[c] = cnt
        avb[c] = bev   # alleen bevestigde vermeldingen (aanwezig, tijdelijk niet zichtbaar, vertrek aangekondigd, rondleiding)
    # per land de locaties [naam, plaats, slug] (voor favorieten en het hartje in het infovak)
    idx = {c: [[l[0], l[1], l[4]] for l in v["locs"]] for c, v in D.items() if isinstance(v, dict) and "locs" in v}
    spn = {x[0]: [x[1], x[2]] for x in D["sp"]}
    SI = soortinfo()
    n = europa(os.path.join(ROOT, "index.html"), wild, av, idx, spn, avb=avb) + europa(os.path.join(ROOT, "top10", "index.html"), wild, av, idx, spn, avb=avb)
    d = os.path.join(ROOT, "soort")
    for s in sorted(os.listdir(d)):
        pad = os.path.join(d, s, "index.html")
        if os.path.exists(pad):
            n += europa(pad, wild, av, idx, spn, soort=True, avb=avb, info=SI.get(s, {}))
    print("hoofdpagina, top 10 en soortpagina's in de nieuwe opbouw:", n)


if __name__ == "__main__":
    maak_alles()
