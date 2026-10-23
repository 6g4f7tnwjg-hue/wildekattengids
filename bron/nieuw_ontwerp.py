"""Testontwerp voor de Nederlandse gids (oktober 2026).

Nieuw ontwerp van de landpagina's (live sinds 17-10-2026, eerst Nederland).

Neemt de gebouwde /<land>/index.html, bewaart die als reserve in /<land>-oud/index.html (noindex) en
schrijft het nieuwe ontwerp over /<land>/index.html. Alleen de vormgeving en de opbouw veranderen; alle
teksten en feiten komen uit de gebouwde pagina (knopnamen worden in de browser uit de tabbladen en kopjes
van de gids overgenomen). De losse park- en soortpagina's blijven in de oude stijl.

Opbouw: startscherm (serval-foto met de kop van de gids, zoekbalk, knoppen, tegels) en elk onderdeel
als eigen scherm met terugknop; onderbalk Home · Locaties · Per kat · Routeplanner · Meer.

Gebruik: python3 bron/nieuw_ontwerp.py   (draait ook automatisch aan het eind van bouw.py)
Werkt ook als het twee keer draait: staat het nieuwe ontwerp al op /<land>/, dan is /<land>-oud/ de bron.
Terugdraaien: /<land>-oud/index.html terugzetten op /<land>/ (of opnieuw bouwen zonder dit script),
map /<land>-oud/ en img/nieuw/ weghalen, dit bestand en de regels onderaan bouw.py verwijderen.
"""
import json
import re
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BASE = "/wildekattengids/"
IMG = BASE + "img/nieuw/"


# Vertalingen van de teksten die het ontwerp zelf toevoegt; de rest komt uit de gids zelf.
# Toon zoals de gidsen: Frans met "vous", Duits, Italiaans, Spaans, Portugees, Deens, Tsjechisch, Zweeds en Noors met "du/tu", Fins met "sinä".
TALEN = ["fr", "de", "it", "es", "pt", "da", "cs", "sv", "nb", "fi", "pl", "hu"]
TR = {
    "Favorieten": {"fr": "Favoris", "de": "Favoriten", "it": "Preferiti", "es": "Favoritos", "pt": "Favoritos", "da": "Favoritter", "cs": "Oblíbené", "sv": "Favoriter", "nb": "Favoritter", "fi": "Suosikit", "pl": "Ulubione", "hu": "Kedvencek"},
    "Terug": {"fr": "Retour", "de": "Zurück", "it": "Indietro", "es": "Volver", "pt": "Voltar", "da": "Tilbage", "cs": "Zpět", "sv": "Tillbaka", "nb": "Tilbake", "fi": "Takaisin", "pl": "Wstecz", "hu": "Vissza"},
    "Meer": {"fr": "Plus", "de": "Mehr", "it": "Altro", "es": "Más", "pt": "Mais", "da": "Mere", "cs": "Více", "sv": "Mer", "nb": "Mer", "fi": "Lisää", "pl": "Więcej", "hu": "Több"},
    "Home": {"fr": "Accueil", "de": "Start", "it": "Home", "es": "Inicio", "pt": "Início", "da": "Hjem", "cs": "Domů", "sv": "Hem", "nb": "Hjem", "fi": "Etusivu", "pl": "Start", "hu": "Kezdőlap"},
    "Bewaar als favoriet": {"fr": "Ajouter aux favoris", "de": "Als Favorit speichern", "it": "Salva nei preferiti",
                            "es": "Guardar en favoritos", "pt": "Guardar nos favoritos", "da": "Gem som favorit", "cs": "Uložit do oblíbených", "sv": "Spara som favorit", "nb": "Lagre som favoritt", "fi": "Tallenna suosikiksi", "pl": "Zapisz w ulubionych", "hu": "Mentés a kedvencek közé"},
    "In je favorieten": {"fr": "Dans vos favoris", "de": "In deinen Favoriten", "it": "Nei tuoi preferiti",
                         "es": "En tus favoritos", "pt": "Nos teus favoritos", "da": "I dine favoritter", "cs": "V tvých oblíbených", "sv": "Bland dina favoriter", "nb": "I favorittene dine", "fi": "Suosikeissasi", "pl": "W twoich ulubionych", "hu": "A kedvenceid között"},
    "Nog geen favorieten. Tik op het hartje bij een park of een soort om het hier te bewaren. Je lijst blijft alleen op dit apparaat.": {
        "fr": "Pas encore de favoris. Touchez le cœur à côté d’un parc ou d’une espèce pour l’enregistrer ici. Votre liste reste uniquement sur cet appareil.",
        "de": "Noch keine Favoriten. Tippe auf das Herz neben einem Park oder einer Art, um ihn hier zu speichern. Deine Liste bleibt nur auf diesem Gerät.",
        "it": "Ancora nessun preferito. Tocca il cuore accanto a un parco o a una specie per salvarlo qui. La tua lista resta solo su questo dispositivo.",
        "es": "Todavía no hay favoritos. Toca el corazón junto a un parque o una especie para guardarlo aquí. Tu lista se queda solo en este dispositivo.",
        "pt": "Ainda não tens favoritos. Toca no coração junto a um parque ou a uma espécie para o guardar aqui. A tua lista fica só neste dispositivo.", "da": "Ingen favoritter endnu. Tryk på hjertet ved en park eller en art for at gemme den her. Din liste bliver kun på denne enhed.", "cs": "Zatím žádné oblíbené. Klepni na srdíčko u parku nebo druhu a uložíš ho sem. Tvůj seznam zůstává jen v tomto zařízení.", "sv": "Inga favoriter än. Tryck på hjärtat vid en park eller en art för att spara den här. Din lista finns bara på den här enheten.", "nb": "Ingen favoritter ennå. Trykk på hjertet ved en park eller en art for å lagre den her. Listen din blir bare på denne enheten.", "fi": "Ei vielä suosikkeja. Napauta puiston tai lajin kohdalla olevaa sydäntä, niin se tallentuu tänne. Listasi pysyy vain tällä laitteella.", "pl": "Nie masz jeszcze ulubionych. Stuknij serduszko przy parku albo gatunku, żeby go tu zapisać. Twoja lista zostaje tylko na tym urządzeniu.", "hu": "Még nincs kedvenced. Koppints a szívre egy park vagy egy faj mellett, hogy ide mentsd. A listád csak ezen az eszközön marad meg."},
    "soorten": {"fr": "espèces", "de": "Arten", "it": "specie", "es": "especies", "pt": "espécies", "da": "arter", "cs": "druhů", "sv": "arter", "nb": "arter", "fi": "lajia", "pl": "gatunków", "hu": "faj"},
    "locaties": {"fr": "lieux", "de": "Orte", "it": "luoghi", "es": "lugares", "pt": "locais", "da": "steder", "cs": "míst", "sv": "platser", "nb": "steder", "fi": "paikkaa", "pl": "miejsc", "hu": "hely"},
    "soort": {"fr": "espèce", "de": "Art", "it": "specie", "es": "especie", "pt": "espécie", "da": "art", "cs": "druh", "sv": "art", "nb": "art", "fi": "laji", "pl": "gatunek", "hu": "faj"},
    "locatie": {"fr": "lieu", "de": "Ort", "it": "luogo", "es": "lugar", "pt": "local", "da": "sted", "cs": "místo", "sv": "plats", "nb": "sted", "fi": "paikka", "pl": "miejsce", "hu": "hely"},
    "Zoek een kat of een park": {"fr": "Rechercher un félin ou un parc", "de": "Katze oder Park suchen",
                                 "it": "Cerca un felino o un parco", "es": "Busca un felino o un parque",
                                 "pt": "Procura um felino ou um parque", "da": "Søg efter en kat eller en park", "cs": "Hledej kočku nebo park", "sv": "Sök efter en katt eller en park", "nb": "Søk etter en katt eller en park", "fi": "Hae kissaa tai puistoa", "pl": "Szukaj kota albo parku", "hu": "Keress egy macskát vagy egy parkot"},
    "Favoriet": {"fr": "Favori", "de": "Favorit", "it": "Preferito", "es": "Favorito", "pt": "Favorito", "da": "Favorit", "cs": "Oblíbené", "sv": "Favorit", "nb": "Favoritt", "fi": "Suosikki", "pl": "Ulubione", "hu": "Kedvenc"},
    "Alle types": {"fr": "Tous les types", "de": "Alle Typen", "it": "Tutti i tipi", "es": "Todos los tipos", "pt": "Todos os tipos", "da": "Alle typer", "cs": "Všechny typy", "sv": "Alla typer", "nb": "Alle typer", "fi": "Kaikki tyypit", "pl": "Wszystkie rodzaje", "hu": "Összes típus"},
}


def L(nl, en):
    t = TR.get(nl, {})
    return (f'<span class="l-nl">{nl}</span><span class="l-en">{en}</span>'
            + "".join(f'<span class="l-{x}">{t.get(x, en)}</span>' for x in TALEN))


ICO = {
    "pin": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M6 12l11-4 14 5 11-4v27l-11 4-14-5-11 4z" fill="#C9D6BC"/><path d="M17 8v27M31 13v27" stroke="#9DB28E" stroke-width="2"/><path d="M33 4a8 8 0 0 0-8 8c0 6 8 14 8 14s8-8 8-14a8 8 0 0 0-8-8z" fill="#2F4A32"/><circle cx="33" cy="12" r="3" fill="#F5F0E4"/></svg>',
    "paw": '<svg viewBox="0 0 48 48" aria-hidden="true" fill="#A65A35"><ellipse cx="24" cy="31" rx="10" ry="8.5"/><ellipse cx="10.5" cy="21" rx="4" ry="5.2"/><ellipse cx="18.5" cy="13.5" rx="4" ry="5.4"/><ellipse cx="29.5" cy="13.5" rx="4" ry="5.4"/><ellipse cx="37.5" cy="21" rx="4" ry="5.2"/></svg>',
    "cal": '<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="6" y="9" width="36" height="32" rx="5" fill="#4C6670"/><rect x="6" y="9" width="36" height="9" rx="4" fill="#3A515A"/><rect x="10" y="21" width="28" height="16" rx="2" fill="#DDE6E6"/><path d="M15 5v8M33 5v8" stroke="#3A515A" stroke-width="3.4" stroke-linecap="round"/><path d="M19 23v12M29 23v12M12 27h24M12 32h24" stroke="#4C6670" stroke-width="1.8"/></svg>',
    "heart": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 41S6 30 6 17.5A9.5 9.5 0 0 1 24 13a9.5 9.5 0 0 1 18 4.5C42 30 24 41 24 41z" fill="#C2564F"/></svg>',
    "search": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg>',
    "tbl": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M3 14h18M9 9v11"/></svg>',
    "news": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18"/><path d="M9 15l2 2 4-4"/></svg>',
    "dna": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M7 3c0 6 10 6 10 12s-10 6-10 6M17 3c0 6-10 6-10 12"/><path d="M8.5 7h7M8.5 17h7"/></svg>',
    "info": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="currentColor"/><circle cx="12" cy="7.2" r="1.6" fill="#F5F0E4"/><path d="M12 11v7" stroke="#F5F0E4" stroke-width="2.6" stroke-linecap="round"/></svg>',
    "flag": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 21V4h11l-2 4 2 4H5"/></svg>',
    "back": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg>',
    "b-home": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/></svg>',
    "b-map": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/></svg>',
    "b-paw": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><ellipse cx="12" cy="15.5" rx="5" ry="4.3"/><ellipse cx="5.3" cy="10.5" rx="2" ry="2.6"/><ellipse cx="9.3" cy="6.7" rx="2" ry="2.7"/><ellipse cx="14.7" cy="6.7" rx="2" ry="2.7"/><ellipse cx="18.7" cy="10.5" rx="2" ry="2.6"/></svg>',
    "b-route": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 18H15a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h6.5"/></svg>',
    "b-heart": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 20s-8-5-8-11a4.5 4.5 0 0 1 8-2.5A4.5 4.5 0 0 1 20 9c0 6-8 11-8 11z"/></svg>',
    "b-menu": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>',
}
ARROW = '<svg class="nw-arr" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>'
HEART_S = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-8-5-8-11a4.5 4.5 0 0 1 8-2.5A4.5 4.5 0 0 1 20 9c0 6-8 11-8 11z"/></svg>'

CSS = r"""
<style id="nw-css">
/* ---- nieuw ontwerp (bron/nieuw_ontwerp.py) ---- */
/* lange weblinks (bijv. bij "Website") laten afbreken in plaats van de pagina te verbreden */
#info dd,#info dd a{overflow-wrap:anywhere}
/* filters bij Locaties als keuzeknoppen */
html.nw-fk #rg-lab,html.nw-fk #rg-bar,html.nw-fk #rg-count,html.nw-fk #lt-bar,html.nw-fk #lt-count{display:none!important}
.nw-filters{display:flex;gap:8px;margin:6px 0 12px}
.nw-fsel{position:relative;flex:1;min-width:0;display:flex;align-items:center;gap:6px;height:44px;padding:0 12px 0 16px;border-radius:99px;border:1px solid var(--line);background:var(--card);box-shadow:var(--nw-shadow);color:var(--ink);font:500 .98rem var(--hs-body);cursor:pointer}
.nw-fsel .nw-fv{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.nw-fsel svg{flex:none;width:18px;height:18px}
.nw-fsel select{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:pointer;font-size:16px}
.nw-fsel.on{background:var(--nw-green);border-color:var(--nw-green);color:#FBF8F1}
.nw-fsel:focus-within{outline:2px solid var(--nw-terra);outline-offset:2px}
/* talen die een pagina niet heeft, nooit tonen */
html:not(.fr) .l-fr,html:not(.de) .l-de,html:not(.it) .l-it,html:not(.es) .l-es,html:not(.pt) .l-pt,html:not(.da) .l-da,html:not(.cs) .l-cs,html:not(.sv) .l-sv,html:not(.nb) .l-nb,html:not(.fi) .l-fi,html:not(.pl) .l-pl,html:not(.hu) .l-hu,html.fr .l-nl,html.de .l-nl,html.it .l-nl,html.es .l-nl,html.pt .l-nl,html.da .l-nl,html.cs .l-nl,html.sv .l-nl,html.nb .l-nl,html.fi .l-nl,html.pl .l-nl,html.hu .l-nl{display:none!important}
:root:root{--paper:#F5F0E4;--card:#FBF8F1;--ink:#22301F;--muted:#5E6656;--line:#E2DACB;--hs-olive:#2F4A32;--hs-accent:#A65A35;--gold:#A65A35;--bark:#2F4A32;--tan:#FBF8F1;--tan-deep:#E2DACB;
  --nw-sage:#E3EADB;--nw-peach:#F3E2D3;--nw-blue:#DDE6E6;--nw-lilac:#E6DDE8;--nw-rose:#F4E3DF;--nw-green:#2F4A32;--nw-terra:#A65A35;--nw-shadow:0 1px 2px rgba(60,50,30,.06),0 10px 24px -14px rgba(60,50,30,.35);--nw-top:var(--hs-head)}
html body{background:var(--paper)!important;padding-bottom:calc(76px + env(safe-area-inset-bottom,0px))}
html body nav.toc,html body #main>header{display:none!important}
h2{color:var(--nw-green)!important}
table th{background:var(--nw-sage)!important;color:var(--ink)!important}
#totop{bottom:calc(84px + env(safe-area-inset-bottom,0px))!important}
/* schermen: startscherm of precies één onderdeel */
html:not(.nw-scherm) #main>*:not(#start){display:none!important}
html.nw-scherm #main>*:not(.nw-cur):not(#nw-sbar){display:none!important}
html.nw-scherm .nw-cur>h2{display:none!important}
html.nw-scherm .nw-cur{margin:0!important;padding:0!important;border:0!important;background:none!important;box-shadow:none!important}
/* schermbalk met terugknop */
.nw-sbar{position:sticky;top:calc(env(safe-area-inset-top,0px) + var(--nw-top));z-index:40;display:flex;align-items:center;gap:8px;margin:0 -16px 14px;padding:8px 16px;background:color-mix(in srgb,var(--paper) 94%,transparent);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}
html:not(.nw-scherm) #nw-sbar{display:none!important}
.nw-back{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;gap:2px;height:38px;padding:0 12px 0 6px;border-radius:99px;border:1px solid var(--line);background:var(--card);font:500 .98rem var(--hs-body);color:var(--ink);flex:none}
.nw-back svg{width:20px;height:20px}
.nw-back:focus-visible{outline:2px solid var(--nw-terra)}
.nw-stitle{margin:0!important;font-family:var(--hs-display)!important;font-weight:800;font-size:clamp(1.25rem,5.4vw,1.7rem)!important;line-height:1.15;color:var(--nw-green)!important;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#info .ip-top{display:none!important}
#info .nw-sbar{margin-top:0}
/* kop met de serval-foto */
.nw-hero{position:relative;margin:12px 0 0;border-radius:22px;overflow:hidden;background:var(--card);border:1px solid var(--line);box-shadow:var(--nw-shadow)}
.nw-hero>img{display:block;width:100%;height:clamp(165px,44vw,320px);object-fit:cover;object-position:50% 32%}
.nw-htxt{padding:14px 18px 0}
.nw-stats{display:grid;grid-template-columns:repeat(2,minmax(0,240px));gap:12px;margin:14px 18px 0;padding-top:14px;border-top:1px solid var(--line)}
.nw-datum{padding:8px 18px 16px}
.nw-foto{margin:0 0 18px!important;max-width:720px}
.nw-foto img{display:block;width:100%!important;max-width:100%!important;height:auto!important;aspect-ratio:4/3;object-fit:cover;border-radius:18px!important;margin:0!important;box-shadow:var(--nw-shadow)!important}
.nw-foto p{margin:6px 2px 0!important;font-size:.82rem!important;color:var(--muted)!important}
.nw-stats a{align-items:center!important;gap:10px!important}
.nw-si{flex:none;display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%}
.nw-si svg{width:22px;height:22px}
.nw-si1{background:#F3E2D6;color:#8A4A2B}
.nw-si1 svg{width:25px;height:25px}
.nw-si2{background:#E1EADF;color:#2F4A33}
.nw-stats a>span:last-child{display:inline-flex;align-items:baseline;gap:7px}
.nw-stats a{display:inline-flex;align-items:baseline;gap:7px;color:var(--muted);text-decoration:none;font-size:1rem}
.nw-stats a strong{font-family:var(--hs-display);font-weight:800;font-size:clamp(1.9rem,8vw,2.4rem);line-height:1;color:var(--ink,#22301f)}
.nw-htxt h1.mast.hs-kop{margin:0 0 2px!important;font-size:clamp(1.9rem,8.5vw,3rem)!important}
.nw-htxt .hs-onder{margin:0!important;font-size:clamp(1rem,4.2vw,1.2rem)!important}
.nw-datum .stamp.hs-stamp{display:block!important;background:none!important;padding:0!important;margin:0!important;color:var(--muted)!important;font-size:.92rem!important}
.nw-cred{position:absolute;top:10px;right:12px;z-index:1;margin:0!important;font-size:.72rem!important;color:#FFF8EC!important;background:rgba(20,24,14,.5);padding:2px 9px;border-radius:99px;max-width:none!important}
/* zoeken */
.nw-search{position:relative;margin:14px 0 0;z-index:5}
.nw-search label{display:flex;align-items:center;gap:10px;background:#FFFDF8;border:1px solid var(--line);border-radius:99px;padding:0 18px;height:54px;box-shadow:var(--nw-shadow)}
.nw-search label:focus-within{border-color:var(--nw-green);box-shadow:0 0 0 2px color-mix(in srgb,var(--nw-green) 25%,transparent),var(--nw-shadow)}
.nw-search label svg{width:22px;height:22px;flex:none;color:var(--ink)}
.nw-search input{all:unset;flex:1;min-width:0;font:400 1.05rem var(--hs-body);color:var(--ink)}
.nw-search input:focus-visible{outline:none!important}
.nw-search input::placeholder{color:#8A8F80}
.nw-res{position:absolute;left:0;right:0;top:60px;background:#FFFDF8;border:1px solid var(--line);border-radius:18px;box-shadow:var(--nw-shadow);padding:6px;max-height:60vh;overflow:auto}
.nw-res[hidden]{display:none}
.nw-res a{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:12px;color:var(--ink);text-decoration:none}
.nw-res a:hover,.nw-res a.on{background:var(--nw-sage)}
.nw-res .nw-ri{flex:none;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:var(--nw-peach);color:var(--nw-terra)}
.nw-res .nw-ri svg{width:18px;height:18px}
.nw-res a.loc .nw-ri{background:var(--nw-sage);color:var(--nw-green)}
.nw-res b{font-weight:600}
.nw-res small{display:block;color:var(--muted);font-size:.85rem}
.nw-res .nw-none{padding:10px 12px;color:var(--muted);margin:0}
/* kleine knoppen */
.nw-quick{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:14px 0 0}
.nw-quick a{display:flex;flex-direction:column;align-items:center;text-align:center;gap:6px;padding:12px 4px 10px;border-radius:20px;border:1px solid var(--line);text-decoration:none;color:var(--ink);background:var(--card);box-shadow:var(--nw-shadow);min-width:0}
.nw-quick .nw-qi{width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center}
.nw-quick a:nth-child(1) .nw-qi{background:var(--nw-lilac);color:#4E3A5A}.nw-quick a:nth-child(2) .nw-qi{background:var(--nw-blue);color:#2F4A52}.nw-quick a:nth-child(3) .nw-qi{background:var(--nw-rose);color:#B4483F}.nw-quick a:nth-child(4) .nw-qi{background:var(--nw-sage);color:var(--nw-green)}
.nw-quick .nw-qi svg{width:24px;height:24px}
.nw-quick b{font-family:var(--hs-body);font-weight:600;font-size:clamp(.74rem,3.1vw,.98rem);line-height:1.2;color:var(--ink)}
/* tegels */
.nw-tiles{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:16px 0 0}
.nw-tile{position:relative;display:flex;flex-direction:column;justify-content:space-between;min-height:150px;padding:14px;border-radius:22px;overflow:hidden;text-decoration:none;color:var(--ink);border:1px solid var(--line);background-size:cover;background-position:right center;box-shadow:var(--nw-shadow)}
.nw-tile::before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,var(--tb) 0,color-mix(in srgb,var(--tb) 88%,transparent) 48%,transparent 85%)}
.nw-tile>*{position:relative}
.nw-tile .nw-ti{width:30px;height:30px;color:var(--tc)}
.nw-tile .nw-ti svg{width:30px;height:30px}
.nw-tile small{display:block;font-size:clamp(.78rem,3.2vw,.95rem);color:var(--ink);margin-top:3px}
.nw-tile small.nw-cnt{display:inline-flex;align-items:baseline;gap:5px;margin-top:8px;padding:3px 12px 4px;border-radius:99px;background:rgba(255,253,248,.92);box-shadow:0 1px 3px rgba(60,50,30,.12);font-size:clamp(.82rem,3.4vw,1rem);font-weight:600;color:var(--tc)}
.nw-tile small.nw-cnt strong{font-family:var(--hs-display);font-weight:800;font-size:clamp(1.25rem,5.4vw,1.6rem);line-height:1;color:var(--tc)}
.nw-tile b{display:flex;align-items:center;gap:2px;font-family:var(--hs-display);font-weight:800;font-size:clamp(1.1rem,4.6vw,1.65rem);line-height:1.08;color:var(--tc);max-width:82%}
.nw-arr{width:18px;height:18px;flex:none}
.nw-t1{--tb:var(--nw-peach);--tc:#7A3F22;background-image:url(IMGtegel-jaguar.webp)}
.nw-t2{--tb:var(--nw-sage);--tc:var(--nw-green);background-image:url(IMGtegel-lynx.webp)}
.nw-t3{--tb:var(--nw-blue);--tc:#2F4A52;background-image:url(IMGtegel-sneeuwluipaard.webp)}
.nw-t4{--tb:var(--nw-lilac);--tc:#4E3A5A;background-image:url(IMGtegel-witte-leeuw.webp)}
.nw-strip{display:flex;align-items:center;gap:12px;margin:12px 0 0;padding:16px;border-radius:22px;background:var(--nw-terra);color:#FFF8EE!important;text-decoration:none;box-shadow:var(--nw-shadow)}
.nw-strip svg{width:24px;height:24px;flex:none}
.nw-strip b{flex:1;font-family:var(--hs-display);font-size:1.2rem}
.nw-strip .nw-arr{width:20px;height:20px}
/* favorieten */
.nw-favs{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
.nw-favs li{display:flex;align-items:center;gap:8px;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:6px 6px 6px 14px}
.nw-favs a{flex:1;color:var(--ink);font-weight:600;text-decoration:none}
.nw-favs small{display:block;color:var(--muted);font-weight:400}
.nw-favh{font-family:var(--hs-label);font-weight:600;font-size:.82rem;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin:14px 0 6px}
.nw-empty{color:var(--muted)}
.nw-heart{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:50%;color:#B4483F;flex:none;vertical-align:middle}
.nw-heart svg{width:22px;height:22px}
.nw-heart svg path{fill:transparent;stroke:currentColor;stroke-width:2}
.nw-heart[aria-pressed="true"] svg path{fill:currentColor}
.nw-heart:focus-visible{outline:2px solid var(--nw-terra)}
.loclist li{position:relative}
.loclist li>.nw-heart{position:absolute;top:4px;right:4px}
.loclist li>b{padding-right:34px;display:inline-block}
#info .nw-hwrap{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;gap:4px;font:500 .95rem var(--hs-body);color:var(--ink);margin:2px 0 10px;background:var(--nw-rose);border-radius:99px;padding:0 14px 0 2px}
/* meer */
.nw-meer{list-style:none;margin:0;padding:0;background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden}
.nw-meer a{display:flex;align-items:center;gap:12px;padding:14px 16px;border-bottom:1px solid var(--line);color:var(--ink);text-decoration:none;font-size:1.05rem;font-weight:500}
.nw-meer li:last-child a{border-bottom:0}
.nw-meer a>svg:first-child{width:22px;height:22px;flex:none;color:var(--nw-terra)}
.nw-meer a .nw-arr{margin-left:auto;color:var(--muted)}
.nw-mlbl{font-family:var(--hs-label);font-weight:600;font-size:.82rem;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin:20px 4px 8px}
/* onderbalk */
.nw-bar{position:fixed;left:0;right:0;bottom:0;z-index:70;background:color-mix(in srgb,#FBF8F1 96%,transparent);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border-top:1px solid var(--line);padding:6px 4px calc(6px + env(safe-area-inset-bottom,0px))}
.nw-bar nav{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));max-width:640px;margin:0 auto}
.nw-bar a{display:flex;flex-direction:column;align-items:center;gap:2px;padding:4px 2px;font:500 .76rem var(--hs-body);color:var(--muted);text-align:center;position:relative;text-decoration:none;white-space:nowrap}
.nw-bar svg{width:24px;height:24px}
.nw-bar .on{color:var(--nw-green);font-weight:700}
.nw-bar .on::after{content:"";position:absolute;bottom:-4px;left:22%;right:22%;height:3px;border-radius:3px;background:var(--nw-green)}
.nw-bar a:focus-visible{outline:2px solid var(--nw-terra);border-radius:8px}
@media (min-width:900px){
  html body{padding-bottom:0}
  :root:root{--nw-top:calc(var(--hs-head) + 54px)}
  .nw-bar{position:fixed;top:calc(env(safe-area-inset-top,0px) + var(--hs-head));bottom:auto;border-top:0;border-bottom:1px solid var(--line);padding:4px}
  .nw-bar nav{display:flex;justify-content:center;gap:6px;max-width:none}
  .nw-bar a{flex-direction:row;gap:8px;font-size:.98rem;padding:8px 14px;border-radius:99px}
  .nw-bar a svg{width:20px;height:20px}
  .nw-bar .on{background:var(--nw-sage)}.nw-bar .on::after{display:none}
  #totop{bottom:24px!important}
  html body #main,html body #info{margin-top:54px}
  .nw-hero>img{height:340px}
  .nw-quick{gap:16px}.nw-tiles{grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}.nw-tile{min-height:190px;padding:18px}
  .nw-search{margin:16px 0 0}
}
@media (max-width:380px){.nw-quick{gap:7px}.nw-quick a{padding:12px 2px 10px;border-radius:20px}.nw-tiles{gap:9px}.nw-tile{padding:12px;min-height:130px}}
</style>
""".replace("IMG", IMG)

START = f"""
<div id="start">
<div class="nw-hero">
  <div class="nw-htxt" id="nw-htxt"></div>
  <div class="nw-stats"><a href="#soorten"><span class="nw-si nw-si1"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M3.4 2.6 8.6 7.3q3.4-1.1 6.8 0l5.2-4.7q1.2 4.8.6 9.4C21 17.4 17.2 21 12 21S3 17.4 2.8 12q-.6-4.6.6-9.4z"/><ellipse cx="8.9" cy="12.6" rx="1.2" ry="1.7" fill="#F3E2D6"/><ellipse cx="15.1" cy="12.6" rx="1.2" ry="1.7" fill="#F3E2D6"/><path d="M10.8 15.6h2.4L12 17z" fill="#F3E2D6"/></svg></span><span class="nw-nsp"></span></a><a href="#locaties"><span class="nw-si nw-si2">{ICO["b-map"]}</span><span class="nw-nloc"></span></a></div>
</div>
<div class="nw-search">
  <label>{ICO["search"]}<input type="search" id="nw-q" autocomplete="off" aria-controls="nw-res"></label>
  <div class="nw-res" id="nw-res" role="listbox" hidden></div>
</div>
<nav class="nw-tiles" aria-label="Menu">
  <a class="nw-tile nw-t4" href="#tldr"><span class="nw-ti">{ICO["tbl"]}</span><span><b><span data-nw-lbl="tldr"></span>{ARROW}</b></span></a>
  <a class="nw-tile nw-t3" href="#actueel"><span class="nw-ti">{ICO["news"]}</span><span><b><span data-nw-lbl="actueel"></span>{ARROW}</b></span></a>
  <a class="nw-tile nw-t1" href="#soorten"><span class="nw-ti">{ICO["b-paw"]}</span><span><b><span data-nw-lbl="soorten"></span>{ARROW}</b></span></a>
  <a class="nw-tile nw-t2" href="#locaties"><span class="nw-ti">{ICO["b-map"]}</span><span><b><span data-nw-lbl="locaties-kop"></span>{ARROW}</b></span></a>
</nav>
<nav class="nw-quick" aria-label="Menu">
  <a href="#kleur"><span class="nw-qi">{ICO["dna"]}</span><b data-nw-lbl="kleur"></b></a>
  <a href="#route"><span class="nw-qi">{ICO["b-route"]}</span><b data-nw-lbl="route"></b></a>
  <a href="#favorieten"><span class="nw-qi">{ICO["b-heart"]}</span><b>{L("Favorieten", "Favourites")}</b></a>
  <a href="#uitleg"><span class="nw-qi">{ICO["info"]}</span><b data-nw-lbl="uitleg"></b></a>
</nav>
<a class="nw-strip" href="#rapporteer">{ICO["flag"]}<b data-nw-lbl="rapporteer"></b>{ARROW}</a>
</div>
<div class="nw-sbar" id="nw-sbar"><button type="button" class="nw-back">{ICO["back"]}{L("Terug", "Back")}</button><h2 class="nw-stitle" id="nw-stitle"></h2></div>
"""

EXTRA = f"""
<section id="favorieten"><h2>{L("Favorieten", "Favourites")}</h2><div id="nw-favs"></div></section>
<section id="meer"><h2>{L("Meer", "More")}</h2><div id="nw-meer"></div></section>
"""

BAR = f"""
<div class="nw-bar"><nav aria-label="Menu">
  <a href="#start" data-nw="start">{ICO["b-home"]}{L("Home", "Home")}</a>
  <a href="#locaties" data-nw="locaties">{ICO["b-map"]}<span data-nw-lbl="locaties"></span></a>
  <a href="#soorten" data-nw="soorten">{ICO["b-paw"]}<span data-nw-lbl="soorten"></span></a>
  <a href="#route" data-nw="route">{ICO["b-route"]}<span data-nw-lbl="route"></span></a>
  <a href="#meer" data-nw="meer">{ICO["b-menu"]}{L("Meer", "More")}</a>
</nav></div>
"""

JS = r"""
<script>
(function(){
var N=window.__NW;if(!N)return;
var R=N.R,LOCS=N.LOCS,SPECIES=N.SPECIES,SPEN=N.SPEN,BYSLUG=N.BYSLUG,LOCBYSLUG=N.LOCBYSLUG,slug=N.slug,lslug=N.lslug;
var HEART='HEARTSVG',PAWI='PAWSVG',PINI='PINSVG',ARR='ARRSVG';
var $=function(s,r){return (r||document).querySelector(s);},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));};
function E(s){return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});}
function TX(nl,en){var t=TRX[nl]||{},l=N.lang();return l==="nl"?nl:l==="en"?en:(t[l]||en);}
function LS(nl,en){var t=TRX[nl]||{},o='<span class="l-nl">'+E(nl)+'</span><span class="l-en">'+E(en)+'</span>';["fr","de","it","es","pt","da","cs","sv","nb","fi","pl","hu"].forEach(function(x){o+='<span class="l-'+x+'">'+E(t[x]||en)+'</span>';});return o;}
function en(n){return (SPEN&&SPEN[n])?SPEN[n][0]:n;}
var main=document.getElementById("main"),info=document.getElementById("info"),html=document.documentElement;
var SCR=["tldr","locaties","soorten","route","actueel","kleur","uitleg","rapporteer","favorieten","meer"];

/* ---------- namen van de knoppen: uit de tabbladen en kopjes van de gids ---------- */
function naam(id){if(id==="locaties-kop"){var k=$("#locaties > h2 .ctog > span");return k?k.innerHTML:naam("locaties");}var a=$('nav.toc a[href="#'+id+'"]');if(a)return a.innerHTML;
  var h=$("#"+id+" > h2 .ctog > span")||$("#"+id+" > h2");return h?h.innerHTML:"";}
$$("[data-nw-lbl]").forEach(function(el){el.innerHTML=naam(el.getAttribute("data-nw-lbl"));});
/* onderbalk: korte naam voor de routeplanner in talen waar de volledige naam niet past */
var KORT={fr:"Itinéraire",it:"Percorso",es:"Ruta",pt:"Rota",da:"Rute",cs:"Trasa",sv:"Rutt",nb:"Rute",fi:"Reitti",pl:"Trasa",hu:"Útvonal"};Object.keys(KORT).forEach(function(k){$$('[data-nw="route"] .l-'+k).forEach(function(x){x.textContent=KORT[k];});});

/* ---------- kop: titel, ondertitel en datum van de gids op de foto; inleiding naar In het kort ---------- */
var hd=$("#main > header"),ht=document.getElementById("nw-htxt");
["h1.mast",".hs-onder"].forEach(function(s){var x=hd&&hd.querySelector(s);if(x)ht.appendChild(x);});
var stp=hd&&hd.querySelector(".stamp.hs-stamp");if(stp){var sw=document.createElement("div");sw.className="nw-datum";sw.appendChild(stp);$(".nw-stats").after(sw);}
var fig=hd&&hd.querySelector("figure.hero");
var cnt=$$("header .counts b");
function PLV(h,n,f){var m=n%10,c=n%100;return h.replace(/(<span class="l-pl">)[^<]*/,"$1"+(n===1?f[0]:m>=2&&m<=4&&(c<12||c>14)?f[1]:f[2]));}   /* Pools: vorm per getal */
if(cnt[0])$$(".nw-nsp").forEach(function(s){s.innerHTML="<strong>"+cnt[0].textContent+"</strong> "+PLV(cnt[0].textContent.trim()==="1"?LS("soort","species"):LS("soorten","species"),+cnt[0].textContent.trim(),["gatunek","gatunki","gatunków"]);});
if(cnt[1])$$(".nw-nloc").forEach(function(s){s.innerHTML="<strong>"+cnt[1].textContent+"</strong> "+PLV(cnt[1].textContent.trim()==="1"?LS("locatie","location"):LS("locaties","locations"),+cnt[1].textContent.trim(),["miejsce","miejsca","miejsc"]);});
var tb=$("#tldr > .cbody")||$("#tldr");
if(hd&&tb){var lede=hd.querySelector(".lede"),co=hd.querySelector(".counts");if(co)tb.insertBefore(co,tb.firstChild);if(lede)tb.insertBefore(lede,tb.firstChild);}
if(fig){if(tb){fig.className="nw-foto";tb.insertBefore(fig,tb.firstChild);}else fig.remove();}
var ab=$("#actueel > .cbody")||$("#actueel");if(ab){var cf=document.createElement("figure");cf.className="nw-foto";cf.innerHTML='<img src="/wildekattengids/img/nieuw/cheeta-welp.webp" alt="Jonge cheeta" loading="lazy"><p><span class="l-nl">Jonge cheeta · foto: J. Gelens</span><span class="l-en">Cheetah cub · photo: J. Gelens</span></p>';var h2=ab.querySelector(":scope > h2");if(h2&&h2.parentNode===ab)h2.after(cf);else ab.insertBefore(cf,ab.firstChild);}

/* ---------- zoeken ---------- */
var q=document.getElementById("nw-q"),res=document.getElementById("nw-res");
function ph(){q.placeholder=TX("Zoek een kat of een park","Search for a cat or a park");q.setAttribute("aria-label",q.placeholder);}
ph();new MutationObserver(ph).observe(html,{attributes:true,attributeFilter:["class","lang"]});
function norm(s){return String(s).toLowerCase().replace(/ł/g,"l").normalize("NFD").replace(/[̀-ͯ]/g,"").replace(/[’']/g,"");}
var SEEN={};R.forEach(function(r){SEEN[r[0]]=1;});
var ITEMS=[];
SPECIES.forEach(function(a){ITEMS.push({k:"sp",h:"#soort/"+slug(a[0]),nl:a[0],en:en(a[0]),sub:a[2],seen:!!SEEN[a[0]],t:norm(a[0]+" "+en(a[0])+" "+a[1]+" "+a[2])});});
LOCS.forEach(function(l){ITEMS.push({k:"loc",h:"#locatie/"+lslug(l[0]),nl:l[0],en:l[0],sub:l[1],seen:true,t:norm(l[0]+" "+l[1]+" "+(l[4]||[]).join(" "))});});
var NIET=(function(){var g=$$("#soorten .group-title").pop();return g?g.innerHTML.replace(/\s*\(\d+[^)]*\)\s*/,""):"";})();
var cur=-1;
function show(){var v=norm(q.value.trim());cur=-1;
  if(!v){res.hidden=true;res.innerHTML="";return;}
  var w=v.split(/\s+/);
  var hit=ITEMS.filter(function(it){return w.every(function(x){return it.t.indexOf(x)>=0;});});
  hit.sort(function(a,b){var sa=+(norm(a.nl).indexOf(v)===0||norm(a.en).indexOf(v)===0),sb=+(norm(b.nl).indexOf(v)===0||norm(b.en).indexOf(v)===0);return (sb-sa)||(b.seen-a.seen);});
  hit=hit.slice(0,8);
  res.innerHTML=hit.length?hit.map(function(it){
    var sub=it.k==="loc"?E(it.sub):(it.seen?"<em>"+E(it.sub)+"</em>":"<em>"+E(it.sub)+"</em>");
    return '<a role="option" class="'+it.k+'" href="'+it.h+'"><span class="nw-ri">'+(it.k==="loc"?PINI:PAWI)+'</span><span><b>'+LS(it.nl,it.en)+'</b><small>'+sub+'</small></span></a>';}).join("")
    :'<p class="nw-none">—</p>';
  res.hidden=false;}
q.addEventListener("input",show);q.addEventListener("focus",show);
q.addEventListener("keydown",function(e){var as=$$("a",res);if(!as.length)return;
  if(e.key==="ArrowDown"||e.key==="ArrowUp"){e.preventDefault();cur=(cur+(e.key==="ArrowDown"?1:-1)+as.length)%as.length;as.forEach(function(a,i){a.classList.toggle("on",i===cur);});}
  else if(e.key==="Enter"){e.preventDefault();var t=as[cur>=0?cur:0];sluit();location.hash=t.getAttribute("href").slice(1);}
  else if(e.key==="Escape"){sluit();}});
function sluit(){res.hidden=true;q.value="";q.blur();}
res.addEventListener("click",function(e){if(e.target.closest("a"))setTimeout(sluit,0);});
document.addEventListener("click",function(e){if(!e.target.closest(".nw-search"))res.hidden=true;});
var tz=$('.hs-top a.hs-ico[href$="#zoek"]');
if(tz){tz.href="#start";tz.addEventListener("click",function(e){e.preventDefault();
  if(location.hash!=="#start")location.hash="start";setTimeout(function(){window.scrollTo(0,0);q.focus();},60);});}

/* ---------- favorieten (alleen in deze browser bewaard) ---------- */
var MEM=null;
function F(){if(!MEM){try{MEM=JSON.parse(localStorage.getItem("nw-fav")||"null");}catch(e){}if(!MEM||!MEM.loc||!MEM.sp)MEM={loc:[],sp:[]};}return MEM;}
function save(){try{localStorage.setItem("nw-fav",JSON.stringify(MEM));}catch(e){}}
function has(k,s){return F()[k].indexOf(s)>=0;}
function toggle(k,s){var a=F()[k],i=a.indexOf(s);if(i>=0)a.splice(i,1);else a.push(s);save();paint();}
function lbl(on){return on?LS("In je favorieten","In your favourites"):LS("Bewaar als favoriet","Save as favourite");}
function btn(k,s){var on=has(k,s);return '<button type="button" class="nw-heart" data-fk="'+k+'" data-fs="'+E(s)+'" aria-pressed="'+on+'" aria-label="'+TX("Favoriet","Favourite")+'">'+HEART+'</button>';}
document.addEventListener("click",function(e){var b=e.target.closest(".nw-hwrap")||e.target.closest(".nw-heart");if(!b||!b.dataset.fk)return;e.preventDefault();e.stopPropagation();toggle(b.dataset.fk,b.dataset.fs);});
function renderFavs(){var f=F(),a=[],b=[];
  f.loc.forEach(function(s){var i=LOCBYSLUG[s];if(i===undefined)return;a.push('<li><a href="#locatie/'+s+'">'+E(LOCS[i][0])+'<small>'+E(LOCS[i][1])+'</small></a>'+btn("loc",s)+'</li>');});
  f.sp.forEach(function(s){var x=BYSLUG[s];if(!x)return;b.push('<li><a href="#soort/'+s+'">'+LS(x[0],en(x[0]))+'<small><em>'+E(x[2])+'</em></small></a>'+btn("sp",s)+'</li>');});
  var out="";
  if(a.length)out+='<p class="nw-favh">'+naam("locaties")+'</p><ul class="nw-favs">'+a.join("")+'</ul>';
  if(b.length)out+='<p class="nw-favh">'+naam("soorten")+'</p><ul class="nw-favs">'+b.join("")+'</ul>';
  document.getElementById("nw-favs").innerHTML=out||'<p class="nw-empty">'+LS("Nog geen favorieten. Tik op het hartje bij een park of een soort om het hier te bewaren. Je lijst blijft alleen op dit apparaat.","No favourites yet. Tap the heart next to a park or a species to keep it here. Your list stays on this device only.")+'</p>';
  var n=f.loc.length+f.sp.length;$$(".nw-nfav").forEach(function(s){s.textContent=n?String(n):"";});}
function listHearts(){$$(".loclist li").forEach(function(li){var a=li.querySelector(':scope > b > a[href^="#locatie/"]');if(!a)return;
  var s=decodeURIComponent(a.getAttribute("href").slice(9)),old=li.querySelector(":scope > .nw-heart"),w=document.createElement("span");
  w.innerHTML=btn("loc",s);if(old)old.replaceWith(w.firstChild);else li.appendChild(w.firstChild);});}

/* ---------- Meer: overige onderdelen en de links uit het menu van de site ---------- */
(function(){var ic={favorieten:"b-heart",tldr:"tbl",actueel:"news",kleur:"dna",uitleg:"info",rapporteer:"flag"};
  var own=["favorieten","tldr","actueel","kleur","uitleg","rapporteer"].map(function(id){
    return '<li><a href="#'+id+'">'+(SVG[ic[id]]||"")+'<span>'+(id==="favorieten"?LS("Favorieten","Favourites"):naam(id))+'</span>'+ARR+'</a></li>';}).join("");
  var site=$$("#hs-menu nav a").map(function(a){var c=a.cloneNode(true);c.removeAttribute("class");return '<li>'+c.outerHTML.replace(/<\/a>$/,ARR+"</a>")+'</li>';}).join("");
  var brand=$(".hs-top .hs-brand b");
  document.getElementById("nw-meer").innerHTML='<ul class="nw-meer">'+own+'</ul>'+(site?'<p class="nw-mlbl">'+(brand?brand.innerHTML:"")+'</p><ul class="nw-meer">'+site+'</ul>':"");})();

/* ---------- schermen ---------- */
/* binnenkomst via een regiolink (bijv. /frankrijk/bretagne/): het regiofilter staat al aan, dus meteen het scherm Locaties tonen */
if(window.__RGINIT&&!location.hash){try{history.replaceState(null,"","#locaties");}catch(e){}}
var stack=[location.hash||"#start"],pos={},curY=window.scrollY,popped=false;
window.addEventListener("scroll",function(){curY=window.scrollY;},{passive:true});
function screenOf(el){while(el&&el.parentElement!==main)el=el.parentElement;return el&&SCR.indexOf(el.id)>=0?el:null;}
function parentOf(h){if(/^#locatie\//.test(h))return "locaties";if(/^#soort\//.test(h))return "soorten";return "start";}
function terug(){if(stack.length>1)history.back();else location.hash=parentOf(location.hash);}
document.addEventListener("click",function(e){if(e.target.closest(".nw-back")){e.preventDefault();terug();}});
var bar=$$(".nw-bar [data-nw]"),busy=false;
function mark(id){bar.forEach(function(a){var on=a.dataset.nw===id;a.classList.toggle("on",on);if(on)a.setAttribute("aria-current","page");else a.removeAttribute("aria-current");});}
function infoBar(){if(info.hidden)return;var h=decodeURIComponent(location.hash||""),m=h.match(/^#(locatie|soort)\/(.+)$/);if(!m)return;
  busy=true;
  if(!info.querySelector(".nw-sbar")){var b=document.createElement("div");b.className="nw-sbar";
    b.innerHTML='<button type="button" class="nw-back">'+SVG.back+LS("Terug","Back")+'</button><span class="nw-stitle">'+naam(m[1]==="locatie"?"locaties":"soorten")+'</span>';
    info.insertBefore(b,info.firstChild);}
  var k=m[1]==="locatie"?"loc":"sp",s=m[2],t=info.querySelector("h1");
  var old=info.querySelector(".nw-hwrap");if(old)old.remove();
  if(t){var w=document.createElement("button");w.type="button";w.className="nw-hwrap";w.dataset.fk=k;w.dataset.fs=s;w.setAttribute("aria-pressed",String(has(k,s)));
    w.innerHTML=btn(k,s).replace(/^<button[^>]*>/,'<span class="nw-heart" aria-pressed="'+has(k,s)+'">').replace(/<\/button>$/,"</span>")+lbl(has(k,s));t.insertAdjacentElement("afterend",w);}
  busy=false;}
new MutationObserver(function(){if(!busy)infoBar();}).observe(info,{childList:true});
function paint(){renderFavs();listHearts();infoBar();}
function apply(){
  var h=decodeURIComponent(location.hash||"");
  SCR.concat(["start"]).forEach(function(id){html.classList.remove("nw-op-"+id);});
  $$(".nw-cur").forEach(function(x){x.classList.remove("nw-cur");});
  if(main.hidden){html.classList.remove("nw-scherm");infoBar();mark(parentOf(h));
    if(popped&&pos[h]!=null)window.scrollTo(0,pos[h]);else window.scrollTo(0,0);return;}
  var t=h.length>1&&document.getElementById(h.slice(1)),sc=t&&screenOf(t);
  if(sc){html.classList.add("nw-scherm","nw-op-"+sc.id);sc.classList.add("nw-cur");
    var cb=sc.querySelector(":scope > .cbody"),tg=sc.querySelector(":scope > h2 .ctog");if(cb)cb.hidden=false;if(tg)tg.setAttribute("aria-expanded","true");
    document.getElementById("nw-stitle").innerHTML=sc.id==="favorieten"?LS("Favorieten","Favourites"):sc.id==="meer"?LS("Meer","More"):naam(sc.id);
    mark(["locaties","soorten","route"].indexOf(sc.id)>=0?sc.id:"meer");
    if(popped&&pos[h]!=null)window.scrollTo(0,pos[h]);
    else if(t===sc)window.scrollTo(0,0);
    else{var y=t.getBoundingClientRect().top+window.scrollY-(document.getElementById("nw-sbar").offsetHeight+80);window.scrollTo(0,Math.max(0,y));}
  }else{html.classList.remove("nw-scherm");html.classList.add("nw-op-start");mark("start");
    window.scrollTo(0,popped&&pos[h]!=null?pos[h]:0);}
}
window.addEventListener("hashchange",function(){
  var h=location.hash||"#start",prev=stack[stack.length-1];pos[prev]=curY;
  if(stack.length>1&&stack[stack.length-2]===h){stack.pop();popped=true;}else{stack.push(h);popped=false;}
  apply();setTimeout(function(){apply();popped=false;},0);});
/* ---------- filters bij Locaties: keuzeknoppen in plaats van rijen knoppen (de oude knoppen blijven verborgen en doen het werk) ---------- */
(function(){
  var sec=document.getElementById("locaties");if(!sec)return;
  var lt=document.getElementById("lt-bar");if(!lt)return;
  var wrap=document.createElement("div");wrap.className="nw-filters";
  (document.getElementById("rg-lab")||lt).insertAdjacentElement("beforebegin",wrap);
  function maak(bar,attr,alle){
    if(!bar)return null;
    var l=document.createElement("label");l.className="nw-fsel";
    l.innerHTML='<span class="nw-fv"></span><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg><select></select>';
    wrap.appendChild(l);var sel=l.querySelector("select"),v=l.querySelector(".nw-fv"),bezig=false;
    function naamVan(b){var c=b.cloneNode(true);c.querySelectorAll(".n,svg").forEach(function(x){x.remove();});return c.textContent.trim();}
    function telVan(b){var n=b.querySelector(".n");return n?n.textContent.trim():"";}
    function sync(){if(bezig)return;bezig=true;
      var chips=[].slice.call(bar.querySelectorAll("button[data-"+attr+"]")),cur="";
      sel.innerHTML=chips.map(function(b){var k=b.getAttribute("data-"+attr),nm=k?naamVan(b):alle(b);if(b.getAttribute("aria-pressed")==="true")cur=k;
        return '<option value="'+E(k)+'">'+E(nm)+' ('+telVan(b)+')</option>';}).join("");
      sel.value=cur;var on=chips.filter(function(b){return b.getAttribute("data-"+attr)===cur;})[0];
      v.textContent=on?(cur?naamVan(on):alle(on))+" · "+telVan(on):"";
      l.classList.toggle("on",!!cur);sel.setAttribute("aria-label",bar.getAttribute("aria-label")||"");
      bezig=false;}
    sel.addEventListener("change",function(){var k=sel.value,b=[].slice.call(bar.querySelectorAll("button[data-"+attr+"]")).filter(function(x){return x.getAttribute("data-"+attr)===k;})[0];if(b)b.click();sync();});
    new MutationObserver(sync).observe(bar,{childList:true,subtree:true,attributes:true,attributeFilter:["aria-pressed"]});
    sync();return sync;}
  function rgAlle(b){return naamVan0(b);}
  function naamVan0(b){var c=b.cloneNode(true);c.querySelectorAll(".n,svg").forEach(function(x){x.remove();});return c.textContent.trim();}
  var s1=maak(document.getElementById("rg-bar"),"r",rgAlle);
  var s2=maak(lt,"t",function(){return TX("Alle types","All types");});
  document.documentElement.classList.add("nw-fk");
  new MutationObserver(function(){if(s1)s1();if(s2)s2();}).observe(document.documentElement,{attributes:true,attributeFilter:["lang","class"]});
})();
paint();apply();
})();
</script>
"""


LANDEN = ["nederland", "belgie", "luxemburg", "duitsland", "frankrijk", "oostenrijk", "zwitserland",
          "verenigd-koninkrijk", "italie", "spanje", "ierland", "portugal", "denemarken", "tsjechie", "zweden", "noorwegen", "finland", "polen", "hongarije"]
MARK = 'id="nw-htxt"'


def maak():
    for land in LANDEN:
        maak_land(land)


def maak_land(land):
    hier = os.path.join(ROOT, land, "index.html")
    oud = os.path.join(ROOT, land + "-oud", "index.html")
    doc = open(hier, encoding="utf-8").read()
    if MARK in doc:
        # nieuw ontwerp staat er al: opnieuw opbouwen vanuit de reserve
        doc = open(oud, encoding="utf-8").read().replace('<meta name="robots" content="noindex">\n', "", 1)
    else:
        os.makedirs(os.path.dirname(oud), exist_ok=True)
        r = doc.replace("</head>", '<meta name="robots" content="noindex">\n</head>', 1)
        open(oud, "w", encoding="utf-8").write(r)

    def sub1(t, a, b):
        assert a in t, f"niet gevonden: {a[:60]}"
        return t.replace(a, b, 1)

    doc = sub1(doc, "</head>", CSS + "</head>")
    doc = sub1(doc, '<div class="wrap" id="main">', '<div class="wrap" id="main">\n' + START)
    # de inhoud van de gids blijft staan; favorieten en meer komen achter de laatste sectie
    doc = sub1(doc, '<section id="rapporteer"', EXTRA + '<section id="rapporteer"')
    # gegevens van de gids beschikbaar maken voor het testontwerp
    exp = ('window.__NW={R:R,LOCS:LOCS,SPECIES:SPECIES,SPEN:SPEN,BYSLUG:BYSLUG,LOCBYSLUG:LOCBYSLUG,slug:slug,lslug:lslug,'
           'lang:function(){return LANG;}};\n')
    a = doc.index("const SPECIES=[")
    e = doc.index("})();\n</script>", a)
    doc = doc[:e] + exp + doc[e:]
    svg = "{" + ",".join(f'"{k}":{v!r}' for k, v in ICO.items()) + "}"
    js = (JS.replace("HEARTSVG", HEART_S).replace("PAWSVG", ICO["b-paw"]).replace("PINSVG", ICO["b-map"])
          .replace("ARRSVG", ARROW).replace("var $=function", "var SVG=" + svg + ";\nvar TRX=" + json.dumps(TR, ensure_ascii=False) + ";\nvar $=function", 1))
    i = doc.rindex("</body>")
    doc = doc[:i] + BAR + js + doc[i:]
    open(hier, "w", encoding="utf-8").write(doc)
    print("nieuw ontwerp geschreven:", land + "/index.html", "(reserve:", land + "-oud/index.html)")


if __name__ == "__main__":
    maak()


# ------------------------------------------------------------------ losse park- en soortpagina's (proef 18-10-2026)
LOS_MARK = 'class="nw-sbar nw-los"'
LOS_CSS = """
<style id="nw-los-css">
/* losse park- en soortpagina in de stijl van het nieuwe ontwerp */
.nw-los{position:sticky;top:calc(env(safe-area-inset-top,0px) + var(--hs-head,64px));z-index:40;margin:0 -16px 6px!important;padding:10px 16px!important}
.nw-los a.nw-back{text-decoration:none}
#info{padding-top:0!important}
.nw-gids{display:flex;align-items:center;gap:12px;margin:22px 0 8px;padding:14px 16px;border-radius:20px;background:var(--card);border:1px solid var(--line);box-shadow:var(--nw-shadow);color:var(--ink)!important;text-decoration:none!important}
.nw-gids .nw-gi{flex:none;width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:var(--nw-sage);color:var(--nw-green)}
.nw-gids .nw-gi svg{width:22px;height:22px}
.nw-gids b{display:block;font-family:var(--hs-body);font-weight:700;font-size:1rem}
.nw-gids small{display:block;color:var(--muted);font-size:.88rem}
.nw-gids>svg{margin-left:auto;width:18px;height:18px;color:var(--muted);flex:none}
</style>
"""


def los_pagina(pad, land, kind):
    """Zet één gebouwde losse pagina (/<land>/locatie/<x>/ of /<land>/soort/<x>/) in de nieuwe stijl."""
    doc = open(pad, encoding="utf-8").read()
    if LOS_MARK in doc:
        return False
    m = re.search(r'<div class="wrap gidslink"><a href="([^"]*)">(.*?)</a></div>', doc, re.S)
    if not m:
        return False
    gids_url, gids_tekst = m.group(1), m.group(2)
    g = BASE + land + "/"
    terug = g + ("#locaties" if kind == "locatie" else "#soorten")
    titel = "Locaties" if kind == "locatie" else "Per kat"
    sbar = (f'<div class="wrap"><div class="nw-sbar nw-los"><a class="nw-back" href="{terug}">{ICO["back"]}Terug</a>'
            f'<span class="nw-stitle">{titel}</span></div></div>')
    doc = doc[:m.start()] + sbar + doc[m.end():]
    # verwijzing naar de interactieve gids als nette kaart onder de inhoud
    kaart = (f'<a class="nw-gids" href="{gids_url}"><span class="nw-gi">{ICO["b-map"]}</span>'
             f'<span><b>{gids_tekst.replace(" →", "").replace("Open de interactieve gids van", "Bekijk in de gids van")}</b>'
             f'<small>Met kaart, routeplanner en favorieten</small></span>{ARROW}</a>')
    i = doc.index('<div class="wrap" id="info">')
    j = doc.rindex("</div>", i, doc.index("kofi", i))   # einde van #info, vlak voor de Ko-fi-voet
    doc = doc[:j] + kaart + "\n" + doc[j:]
    actief = "locaties" if kind == "locatie" else "soorten"
    links = [("start", g, ICO["b-home"], "Home"), ("locaties", g + "#locaties", ICO["b-map"], "Locaties"),
             ("soorten", g + "#soorten", ICO["b-paw"], "Per kat"), ("route", g + "#route", ICO["b-route"], "Routeplanner"),
             ("meer", g + "#meer", ICO["b-menu"], "Meer")]
    bar = ('<div class="nw-bar"><nav aria-label="Menu">'
           + "".join(f'<a href="{h}"{" class=on" if k == actief else ""}>{svg}<span>{t}</span></a>' for k, h, svg, t in links)
           + "</nav></div>\n")
    doc = doc.replace("</head>", CSS + LOS_CSS + "</head>", 1)
    k = doc.rindex("</body>")
    doc = doc[:k] + bar + doc[k:]
    open(pad, "w", encoding="utf-8").write(doc)
    return True


def maak_los(alleen=None):
    n = 0
    for land in LANDEN:
        for kind in ("locatie", "soort"):
            d = os.path.join(ROOT, land, kind)
            if not os.path.isdir(d):
                continue
            for s in sorted(os.listdir(d)):
                if alleen and (land, kind, s) not in alleen:
                    continue
                pad = os.path.join(d, s, "index.html")
                if os.path.exists(pad) and los_pagina(pad, land, kind):
                    n += 1
    print("losse pagina's in nieuwe stijl:", n)


# ------------------------------------------------------------------ startpagina en top 10 (18-10-2026)
START_MARK = 'id="nw-start-css"'


def _bar_css():
    regels = [r for r in CSS.split("\n") if r.startswith(".nw-bar")]
    return "\n".join(regels)


START_CSS = """
<style id="nw-start-css">
/* startpagina en top 10 in de kleuren van het nieuwe ontwerp (bron/nieuw_ontwerp.py) */
:root:root{--bg:#F5F0E4;--paper:#FBF8F1;--ink:#22301F;--muted:#5E6656;--line:#E2DACB;--olive:#2F4A32;--dot:#2F4A32;--accent:#A65A35;
  --shadow:0 1px 2px rgba(60,50,30,.06),0 10px 24px -14px rgba(60,50,30,.35);--nw-green:#2F4A32;--nw-terra:#A65A35;--card:#FBF8F1;--hs-body:var(--body)}
html body{padding-bottom:calc(76px + env(safe-area-inset-bottom,0px))}
.tab[aria-selected="true"],.lgbtn[aria-pressed="true"]{background:var(--olive)!important;border-color:var(--olive)!important;color:#FBF8F1!important}
.catbtn[aria-pressed="true"]{background:#E3EADB!important}
.nw-bar a,.nw-bar a:hover,.nw-bar a:visited{color:var(--muted)!important;text-decoration:none!important}.nw-bar a.on{color:var(--nw-green)!important}
BARCSS
</style>
"""

START_JS = """
<script>(function(){
var T={home:{nl:"Home",en:"Home",fr:"Accueil",de:"Start",it:"Home",es:"Inicio",pt:"Início",da:"Hjem",cs:"Domů",sv:"Hem",nb:"Hjem",fi:"Etusivu",pl:"Start",hu:"Kezdőlap"},
  landen:{nl:"Landen",en:"Countries",fr:"Pays",de:"Länder",it:"Paesi",es:"Países",pt:"Países",da:"Lande",cs:"Země",sv:"Länder",nb:"Land",fi:"Maat",pl:"Kraje",hu:"Országok"},
  soorten:{nl:"Soorten",en:"Species",fr:"Espèces",de:"Arten",it:"Specie",es:"Especies",pt:"Espécies",da:"Arter",cs:"Druhy",sv:"Arter",nb:"Arter",fi:"Lajit",pl:"Gatunki",hu:"Fajok"},
  meer:{nl:"Meer",en:"More",fr:"Plus",de:"Mehr",it:"Altro",es:"Más",pt:"Mais",da:"Mere",cs:"Více",sv:"Mer",nb:"Mer",fi:"Lisää",pl:"Więcej",hu:"Több"}};
var bar=document.getElementById("nw-sbar-start");if(!bar)return;
function lang(){var l=(document.documentElement.lang||"nl").slice(0,2);return T.home[l]?l:"en";}
function labels(){var l=lang();bar.querySelectorAll("[data-k]").forEach(function(a){a.querySelector("span").textContent=T[a.dataset.k][l];});}
function mark(){if(!bar.dataset.start)return;var sel=document.querySelector('.tab[aria-selected="true"]'),k=sel?sel.dataset.tab:null;
  bar.querySelectorAll("[data-k]").forEach(function(a){var on=(k==="kaart"&&a.dataset.k==="home")||(k&&a.dataset.k===k);a.classList.toggle("on",!!on);});}
bar.addEventListener("click",function(e){var a=e.target.closest('[data-k="meer"]');if(!a)return;var m=document.getElementById("menu-btn");
  if(m){e.preventDefault();e.stopPropagation();window.scrollTo(0,0);m.click();}});
new MutationObserver(labels).observe(document.documentElement,{attributes:true,attributeFilter:["lang"]});
document.querySelectorAll(".tab").forEach(function(t){new MutationObserver(mark).observe(t,{attributes:true,attributeFilter:["aria-selected"]});});
labels();mark();
})();</script>
"""


def start_pagina(pad, op_start):
    doc = open(pad, encoding="utf-8").read()
    if START_MARK in doc:
        return False
    pre = "" if op_start else BASE
    links = [("home", pre + "#kaart", ICO["b-home"]), ("landen", pre + "#landen", ICO["b-map"]),
             ("soorten", pre + "#soorten", ICO["b-paw"]), ("meer", pre + "#over", ICO["b-menu"])]
    bar = ('<div class="nw-bar nw-bar4" id="nw-sbar-start"' + (' data-start="1"' if op_start else '') + '><nav aria-label="Menu">'
           + "".join(f'<a href="{h}" data-k="{k}">{svg}<span></span></a>' for k, h, svg in links) + "</nav></div>\n")
    css = START_CSS.replace("BARCSS", _bar_css() + "\n.nw-bar4 nav{grid-template-columns:repeat(4,minmax(0,1fr))!important}")
    doc = doc.replace("</head>", css + "</head>", 1)
    k = doc.rindex("</body>")
    doc = doc[:k] + bar + START_JS + doc[k:]
    open(pad, "w", encoding="utf-8").write(doc)
    return True


def maak_start():
    n = start_pagina(os.path.join(ROOT, "index.html"), True) + start_pagina(os.path.join(ROOT, "top10", "index.html"), False)
    print("startpagina en top 10 in nieuwe stijl:", n)
