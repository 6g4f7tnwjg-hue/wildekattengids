# Huisstijl van de startpagina (stijl van de Spottersgids) voor de landengidsen op de website.
# bouw.py zet dit in elke gids, deelstaat- en regiopagina en in de losse soort- en locatiepagina's:
#   - dezelfde bovenbalk als de startpagina (pootje, zoeken, taal, menu); "← Alle landen" en "Steun de gids" bovenaan vervallen
#   - dezelfde kleuren en letters (Alegreya, Alegreya Sans, Barlow Condensed)
#   - een rustiger kop (kleine titelregel, kleinere foto)
#   - de inhoudsopgave van de gids als tabbladen die blijven staan
#   - Ko-fi onderaan zoals op de startpagina
# De gegevens en teksten van de gidsen zelf blijven onaangeroerd; de kaart in de gids houdt zijn eigen stijl.
import re, json

FONTS = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Alegreya:ital,wght@0,500;0,700;0,800;1,500&family=Alegreya+Sans:ital,wght@0,400;0,500;0,700;1,400&family=Barlow+Condensed:wght@500;600&display=swap" rel="stylesheet">')

def lettertypen(doc):
    """Bricolage/Literata vervangen door de letters van de startpagina (ook in tekst die het script van de gids later invoegt)."""
    doc = re.sub(r'<link href="https://fonts\.googleapis\.com/css2\?family=Bricolage[^"]*" rel="stylesheet">', lambda m: FONTS, doc)
    doc = doc.replace("Bricolage Grotesque", "Alegreya Sans")
    return re.sub(r"\bLiterata\b", "Alegreya Sans", doc)

L = {  # teksten in alle gidstalen
    "naam": {"nl": "Bezoekersgids", "en": "Visitor’s Guide", "fr": "Guide du visiteur", "de": "Besucherführer", "it": "Guida per visitatori", "es": "Guía del visitante", "pt": "Guia do visitante", "da": "Besøgsguide", "cs": "Průvodce pro návštěvníky", "sv": "Besöksguide"},
    "sub": {"nl": "Wilde katten", "en": "Wild cats", "fr": "Félins sauvages", "de": "Wilde Katzen", "it": "Felini selvatici", "es": "Felinos salvajes", "pt": "Felinos selvagens", "da": "Vilde katte", "cs": "Divoké kočky", "sv": "Vilda katter"},
    "zoek": {"nl": "Zoeken", "en": "Search", "fr": "Chercher", "de": "Suchen", "it": "Cerca", "es": "Buscar", "pt": "Pesquisar", "da": "Søg", "cs": "Hledat", "sv": "Sök"},
    "kaart": {"nl": "Kaart", "en": "Map", "fr": "Carte", "de": "Karte", "it": "Mappa", "es": "Mapa", "pt": "Mapa", "da": "Kort", "cs": "Mapa", "sv": "Karta"},
    "landen": {"nl": "Alle landen", "en": "All countries", "fr": "Tous les pays", "de": "Alle Länder", "it": "Tutti i paesi", "es": "Todos los países", "pt": "Todos os países", "da": "Alle lande", "cs": "Všechny země", "sv": "Alla länder"},
    "soorten": {"nl": "Alle soorten", "en": "All species", "fr": "Toutes les espèces", "de": "Alle Arten", "it": "Tutte le specie", "es": "Todas las especies", "pt": "Todas as espécies", "da": "Alle arter", "cs": "Všechny druhy", "sv": "Alla arter"},
    "fav": {"nl": "Favorieten", "en": "Favourites", "fr": "Favoris", "de": "Favoriten", "it": "Preferiti", "es": "Favoritos", "pt": "Favoritos", "da": "Favoritter", "cs": "Oblíbené", "sv": "Favoriter"},
    "top10": {"nl": "Top 10 om te bezoeken", "en": "Top 10 to visit", "fr": "Top 10 à visiter", "de": "Top 10 zum Besuchen", "it": "Top 10 da visitare", "es": "Top 10 para visitar", "pt": "Top 10 a visitar", "da": "Top 10 at besøge", "cs": "Top 10 k návštěvě", "sv": "Topp 10 att besöka"},
    "geboren": {"nl": "Recent geboren", "en": "Recently born", "fr": "Naissances récentes", "de": "Kürzlich geboren", "it": "Nati di recente", "es": "Nacimientos recientes", "pt": "Nascimentos recentes", "da": "Nyfødte", "cs": "Nedávno narozená mláďata", "sv": "Nyfödda"},
    "perpark": {"nl": "Parken op aantal soorten", "en": "Parks by number of species", "fr": "Parcs par nombre d’espèces", "de": "Parks nach Zahl der Arten", "it": "Parchi per numero di specie", "es": "Parques por número de especies", "pt": "Parques por número de espécies", "da": "Parker efter antal arter", "cs": "Parky podle počtu druhů", "sv": "Parker efter antal arter"},
    "typen": {"nl": "Soorten locaties", "en": "Types of location", "fr": "Types de lieux", "de": "Arten von Orten", "it": "Tipi di luogo", "es": "Tipos de lugar", "pt": "Tipos de local", "da": "Typer af steder", "cs": "Typy míst", "sv": "Typer av platser"},
    "over": {"nl": "Over deze gids", "en": "About this guide", "fr": "À propos de ce guide", "de": "Über diesen Guide", "it": "Informazioni su questa guida", "es": "Sobre esta guía", "pt": "Sobre este guia", "da": "Om denne guide", "cs": "O tomto průvodci", "sv": "Om guiden"},
    "meer": {"nl": "Meer", "en": "More", "fr": "Plus", "de": "Mehr", "it": "Altro", "es": "Más", "pt": "Mais", "da": "Mere", "cs": "Více", "sv": "Mer"},
    "spot": {"nl": "Spottersgids: katten in het wild", "en": "Spotter’s Guide: cats in the wild", "fr": "Spotter’s Guide : félins dans la nature (en anglais)", "de": "Spotter’s Guide: Katzen in freier Wildbahn (auf Englisch)", "it": "Spotter’s Guide: felini in natura (in inglese)", "es": "Spotter’s Guide: felinos en libertad (en inglés)", "pt": "Spotter’s Guide: felinos na natureza (em inglês)", "da": "Spotter’s Guide: katte i naturen (på engelsk)", "cs": "Spotter’s Guide: kočky v přírodě (anglicky)", "sv": "Spotter’s Guide: katter i det vilda (på engelska)"},
    "kofi": {"nl": "Steun de gids op Ko-fi", "en": "Support the guide on Ko-fi", "fr": "Soutenir le guide sur Ko-fi", "de": "Den Guide auf Ko-fi unterstützen", "it": "Sostieni la guida su Ko-fi", "es": "Apoya la guía en Ko-fi", "pt": "Apoia o guia no Ko-fi", "da": "Støt guiden på Ko-fi", "cs": "Podpoř průvodce na Ko-fi", "sv": "Stöd guiden på Ko-fi"},
    "kofi_t": {"nl": "Vind je deze gids handig?", "en": "Find this guide useful?", "fr": "Ce guide vous est utile ?", "de": "Findest du diesen Guide nützlich?", "it": "Trovi utile questa guida?", "es": "¿Te resulta útil esta guía?", "pt": "Este guia é útil para ti?", "da": "Synes du, at guiden er nyttig?", "cs": "Je ti průvodce užitečný?", "sv": "Tycker du att guiden är användbar?"},
    "kofi_s": {"nl": "Met een kleine bijdrage help je hem actueel te houden.", "en": "A small contribution helps keep it up to date.", "fr": "Une petite contribution aide à le tenir à jour.", "de": "Ein kleiner Beitrag hilft, ihn aktuell zu halten.", "it": "Con un piccolo contributo aiuti a tenerla aggiornata.", "es": "Una pequeña aportación ayuda a mantenerla al día.", "pt": "Uma pequena contribuição ajuda a mantê-lo atualizado.", "da": "Et lille bidrag hjælper med at holde den opdateret.", "cs": "Malý příspěvek pomáhá udržovat ho aktuální.", "sv": "Ett litet bidrag hjälper till att hålla den uppdaterad."},
    "door": {"nl": "Samengesteld door J. Gelens. Bronnen en foto’s staan in de gids.", "en": "Compiled by J. Gelens. Sources and photos are listed in the guide.", "fr": "Rédigé par J. Gelens. Les sources et les photos figurent dans le guide.", "de": "Zusammengestellt von J. Gelens. Quellen und Fotos stehen im Guide.", "it": "Compilata da J. Gelens. Fonti e foto si trovano nella guida.", "es": "Elaborado por J. Gelens. Las fuentes y las fotos figuran en la guía.", "pt": "Compilado por J. Gelens. As fontes e as fotos estão no guia.", "da": "Samlet af J. Gelens. Kilder og fotos står i guiden.", "cs": "Sestavil J. Gelens. Zdroje a fotky najdeš v průvodci.", "sv": "Sammanställd av J. Gelens. Källor och foton finns i guiden."},
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
    "fav": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    "geboren": '<path d="M12 3l2.7 5.6 6.1.8-4.5 4.2 1.1 6.1L12 16.8l-5.4 2.9 1.1-6.1-4.5-4.2 6.1-.8z"/>',
    "perpark": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "typen": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.5"/>',
    "over": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
}
def ic(k):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{IC[k]}</svg>'

def bovenbalk(langs, base, taal=True):
    """De bovenbalk van de startpagina. Bij taal=True komt de taalknop van de gids erin (het script verplaatst hem)."""
    h = lambda k: base + ("top10/" if k == "top10" else "#favorieten" if k == "fav" else "#" + k)
    links = lambda ks: "".join(f'<a href="{h(k)}">{ic(k)}{t(k if k not in ("landen", "soorten") else k, langs)}</a>' for k in ks)
    return (f'<div class="hs-top" id="hs-top"><div class="hs-wrap">'
            f'<a class="hs-brand" href="{base}">{PAW}<span><b>{t("naam", langs)}</b><small>{t("sub", langs)} · J. Gelens</small></span></a>'
            f'<a class="hs-ico" href="{base}#zoek" aria-label="{L["zoek"][langs[0]]}">{ZOEK}<span class="t">{t("zoek", langs)}</span></a>'
            + ('<span id="hs-lang"></span>' if taal else "") +
            f'<button type="button" class="hs-ico" id="hs-menu-btn" aria-expanded="false" aria-controls="hs-menu" aria-label="Menu">{MENU}<span class="t">Menu</span></button></div>'
            f'<div class="hs-drop" id="hs-menu" hidden><div class="hs-wrap"><nav aria-label="Menu"><div>{links(["kaart", "landen", "soorten", "fav"])}</div>'
            f'<div>{links(["top10", "geboren", "perpark", "typen"])}<div class="hs-meer"><span class="hs-lbl">{t("meer", langs)}</span><a href="{h("over")}">{t("over", langs)}</a>{spot(langs, base)}'
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
.hs-brand b{display:block;font-family:var(--hs-display);font-weight:800;font-size:1.15rem;line-height:1.2;padding-bottom:1px;margin-bottom:-3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--ink)}
.hs-brand small{display:block;font-family:var(--hs-label);font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-top:3px;white-space:normal;line-height:1.25}
@media (max-width:360px){.hs-top .hs-brand svg{display:none}.hs-top>.hs-wrap{gap:5px}.hs-ico{min-width:34px;padding:0 7px}.hs-top .hs-brand b{font-size:.98rem}.hs-top .hs-brand small{font-size:.62rem;letter-spacing:.06em}}
@media (max-width:300px){.hs-top .hs-brand b{font-size:.78rem}}
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
h1.mast.hs-kop{display:flex!important;align-items:center;gap:12px;font-family:var(--hs-display)!important;font-weight:800!important;font-size:clamp(1.75rem,6vw,2.6rem)!important;line-height:1.1!important;color:var(--ink)!important;margin:0 0 4px!important;letter-spacing:-.01em}
h1.mast.hs-kop>svg{flex:none;width:44px;height:30px;border-radius:4px;box-shadow:0 0 0 1px rgba(30,35,24,.18)}
.hs-onder{margin:0 0 10px!important;color:var(--muted);font-size:1.08rem;font-family:var(--hs-body)}
header .stamp.hs-stamp{display:block!important;margin:-6px 0 10px!important;font-family:var(--hs-body)!important;font-weight:400!important;font-size:.92rem!important;letter-spacing:0!important;text-transform:none!important;color:var(--muted)!important}
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
/* kaarten in de gidsen: elk type locatie een eigen kleur en icoon (zoals op de startpagina) */
.map{background:var(--card)!important;border-radius:12px!important;border:1px solid var(--line)!important}
.map svg{background:#E2DFD4;border-radius:8px}
.map .land{fill:#CDC7A9!important;stroke:#A59F84!important}
.map .water{fill:#D3E1E4!important;stroke:#A59F84!important}
.map .buur{fill:#E2DFD4!important;stroke:#C9C5B6!important}
.map .mk[data-hs] .dot{fill:currentColor!important;stroke:var(--card)!important;stroke-width:1.6!important}
.map .mk[data-hs] .hs-gl{fill:var(--card);color:var(--card);pointer-events:none}
.map .mk.w[data-hs] .dot{fill:var(--card)!important;stroke:currentColor!important;stroke-width:2!important}
.map .mk.w[data-hs] .hs-gl{fill:currentColor;color:inherit}
.map .mk.hs-uit{display:none}
.map .mk.hs-clh{display:none}
.map .mk .hs-bring{fill:none;stroke:#E0352B;stroke-width:2.4;display:none}
html.hs-geb .map .mk.hs-jong .hs-bring{display:inline}
html.hs-geballeen .map .mk:not(.hs-jong){display:none}
.hs-cl .hs-badge{fill:#E0352B;stroke:var(--card);stroke-width:1.3}
.hs-gebrow{display:flex;flex-wrap:wrap;align-items:center;gap:6px 12px;margin:0 0 8px}
.hs-gebbtn{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;gap:6px;border:1px dashed var(--line);border-radius:99px;padding:4px 11px 4px 9px;font-size:.92rem;color:var(--muted)}
.hs-gebbtn .sw{width:12px;height:12px;border-radius:50%;border:2px solid var(--line)}
.hs-gebbtn .n{font-family:var(--hs-label);font-weight:600}
.hs-gebbtn[aria-pressed="true"]{border:1px solid #E0352B;color:var(--ink);background:var(--card)}
.hs-gebbtn[aria-pressed="true"] .sw{border-color:#E0352B}
.hs-gebbtn[aria-pressed="true"]::after{content:"\2713";color:#E0352B;font-weight:700}
.hs-gebx{all:unset;cursor:pointer;color:var(--hs-olive);font-weight:700;text-decoration:underline;text-underline-offset:2px;font-size:.92rem}
.map.hs-zoom{position:relative!important}
.map svg{touch-action:pan-y;user-select:none;-webkit-user-select:none}
.map svg.hs-zoomed{touch-action:none;cursor:grab}
.map svg .land,.map svg .water,.map svg .grens,.map svg .buur{vector-effect:non-scaling-stroke}
.hs-zb{position:absolute;top:16px;right:16px;display:flex;flex-direction:column;gap:6px;z-index:2}
.hs-zb button{width:36px;height:36px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--ink);font:700 1.3rem/1 var(--hs-body);cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0;box-shadow:0 1px 0 rgba(30,35,24,.06),0 8px 24px -12px rgba(30,35,24,.25)}
.hs-zb button svg{width:18px;height:18px}
.hs-zb button:disabled{opacity:.4;cursor:default}
.hs-cl{cursor:pointer}
.hs-cl .hs-cld{fill:var(--hs-olive);stroke:var(--card);stroke-width:1.8}
.hs-cl .hs-clh-hit{fill:transparent}
.hs-cl text{fill:var(--card);font-family:var(--hs-label);font-weight:600;font-size:13px;text-anchor:middle;pointer-events:none}
.hs-cl:focus{outline:none}.hs-cl:focus-visible .hs-cld{stroke:var(--hs-accent);stroke-width:3}
.maplegend.hs-lg{display:block!important;font-family:var(--hs-body)!important;font-size:.95rem!important;margin:8px 2px 2px!important}
.hs-lg .hs-lgt{display:block;color:var(--muted);margin:0 0 4px}
.hs-lg .hs-onz{display:flex!important}
.hs-lg .hs-chips{display:flex;flex-wrap:wrap;gap:6px}
.hs-lg button{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:var(--card);border-radius:99px;padding:4px 11px 4px 5px;font-size:.92rem;color:var(--ink);white-space:nowrap}
.hs-lg button[aria-pressed="true"]{background:var(--hs-olive);border-color:var(--hs-olive);color:var(--card)}
.hs-lg button .n{font-family:var(--hs-label);font-weight:600;opacity:.75}
.hs-lg svg{width:18px;height:18px;flex:none}
.lt-chip.hs-tc{display:inline-flex;align-items:center;gap:6px;padding-left:5px!important}
.lt-chip svg{width:18px;height:18px;flex:none}
.lt-chip{font-family:var(--hs-body)!important;font-size:.92rem!important;border-width:1px!important}
.lt-chip[aria-pressed="true"]{background:var(--hs-olive)!important;border-color:var(--hs-olive)!important}
.hs-lg .hs-onz{display:inline-flex;align-items:center;gap:6px;color:var(--muted);margin-top:6px}
.hs-lg .hs-onz i{width:12px;height:12px;border-radius:50%;border:2px solid var(--muted);display:inline-block}
/* gidspagina overzichtelijker (17-10-2026) */
/* rustiger: geen ringband-stipjes op kaartjes, een dunne lijn tussen de onderdelen */
.loclist.cards li::before{display:none!important}
.loclist.cards li{background:var(--card)!important;border-radius:12px!important}
section::before,.board::before,.ip-sec::before,footer::before{display:none!important}
.wrap>footer{border-top:1px solid var(--line)!important}
.wrap>section,.wrap>.board{border-top:1px solid var(--line)!important}
/* In het kort: alleen de korte punten, de tabel Totaaloverzicht vervalt */
.hs-weg{display:none!important}
.hs-reg{margin-top:18px;padding-top:14px;border-top:1px solid var(--line);scroll-margin-top:calc(var(--hs-head) + 64px)}
/* Plan je bezoek: alleen de vinklijst; de teller toont wat je nog mist */
.rt-out{display:none!important}
.rt-grid{grid-template-columns:minmax(0,1fr)!important;max-width:640px}
.rt-score{top:calc(env(safe-area-inset-top,0px) + var(--hs-head) + 54px)!important;z-index:20!important}
.rt-score .hs-mist{display:block;margin-top:6px;color:var(--ink);font-size:14px;line-height:1.4}
.rt-score .hs-mist b{font-size:14px!important;font-weight:700!important}
/* hoofdtabel op de telefoon: per soort, één korte regel per locatie, tik voor details */
@media (max-width:760px){
  .reg tr{position:relative;padding:9px 34px 9px 12px!important;cursor:pointer}
  .reg tr.hs-grp{border-top:2px solid var(--line);margin-top:6px;padding-top:12px!important}
  .reg tr.hs-same td.sp{display:none!important}
  .reg td.sp{font-family:var(--hs-display);font-weight:800;font-size:1.15rem!important;margin-bottom:2px}
  .reg tr:not(.hs-open) td:nth-child(2),.reg tr:not(.hs-open) td:nth-child(n+6){display:none!important}
  .reg td.hs-unk{display:none!important}
  .reg td:nth-child(3),.reg td:nth-child(4){display:inline!important}
  .reg td:nth-child(4)::before{content:" · "!important;font-size:inherit!important;font-family:inherit!important}
  .reg td:nth-child(4){color:var(--muted)}
  .reg td:nth-child(5){margin-top:2px}
  .reg td:nth-child(5)::before{content:none!important}
  .reg tr.hs-open td:nth-child(2){margin-top:6px}
  .reg tr::after{content:"";position:absolute;right:14px;top:calc(50% - 6px);width:8px;height:8px;border-right:2px solid var(--muted);border-bottom:2px solid var(--muted);transform:rotate(45deg)}
  .reg tr.hs-grp::after{top:calc(50% + 6px)}
  .reg tr.hs-open::after{transform:rotate(-135deg)}
}
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
/* kop: landnaam (of deelstaat/regio) als titel, één regel eronder, datum bij de aantallen */
var HK=window.__HSK;
var PREP=/^(in der |in the |im |in |en |dans la |dans le |dans les |dans l’|dans l'|dans |nella |nello |nell’|nell'|nel |na |no |em |i |v )/i;
function kop(h){if(!HK||h.dataset.hsk)return;var m2=h.querySelector("h1.mast .m2"),h1=h.querySelector("h1.mast");if(!m2||!h1)return;h.dataset.hsk="1";
  var nl=m2.querySelector(".l-nl"),land=!nl||/dierenlocaties/.test(nl.textContent),ls=Object.keys(HK.land),titel="",onder="";
  ls.forEach(function(l){var sp=m2.querySelector(".l-"+l),nm=land?HK.land[l]:(sp?sp.textContent.trim().replace(PREP,""):HK.land[l]);
    nm=nm.charAt(0).toUpperCase()+nm.slice(1);
    var o=land?HK.onder[l]:HK.land[l]+" · "+HK.onder[l].charAt(0).toLowerCase()+HK.onder[l].slice(1);
    titel+='<span class="l-'+l+'">'+nm+'</span>';onder+='<span class="l-'+l+'">'+o+'</span>';});
  h1.innerHTML=HK.vlag+'<span class="hs-t">'+titel+'</span>';h1.classList.add("hs-kop");
  h1.insertAdjacentHTML("afterend",'<p class="hs-onder">'+onder+'</p>');
  /* datum als kleine regel direct onder de ondertitel (17-10-2026) */
  var st=h.querySelector(".stamp"),on=h.querySelector(".hs-onder");if(st&&on){on.insertAdjacentElement("afterend",st);st.classList.add("hs-stamp");
    st.querySelectorAll(".l-nl").forEach(function(x){x.textContent=x.textContent.replace(/^Stand /,"Bijgewerkt ");});}}
function koppen(){document.querySelectorAll("header").forEach(kop);}
koppen();new MutationObserver(function(){koppen();}).observe(document.body,{childList:true,subtree:true});
/* kaarten: kleur en icoon per type, legenda met filter */
var HT=window.__HST;if(!HT)return;
var NS="http://www.w3.org/2000/svg",FILT={};
function taal(){var l=(document.documentElement.lang||"nl").slice(0,2);return HT.nm[l]?l:(document.documentElement.classList.contains("en")?"en":"nl");}
var GEBON=false,GEBALL=false;
function isJong(mk){var lab=mk.getAttribute("aria-label")||"";return (HT.jong||[]).some(function(n){return lab===n||lab.indexOf(n+", ")===0;});}
function gebStand(){document.documentElement.classList.toggle("hs-geb",GEBON);document.documentElement.classList.toggle("hs-geballeen",GEBON&&GEBALL);
  document.querySelectorAll(".map svg").forEach(function(s){if(s.__zk)plan(s);});document.querySelectorAll(".map svg[data-hs-lg]").forEach(legenda);}
document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest("[data-hsgeb]");if(!b)return;
  if(b.dataset.hsgeb==="aan"){GEBON=!GEBON;if(!GEBON)GEBALL=false;}else GEBALL=!GEBALL;gebStand();});
function typeOf(mk){var lab=mk.getAttribute("aria-label")||"",best=-1,bl=0;
  for(var k in HT.loc){if((lab===k||lab.indexOf(k+", ")===0)&&k.length>bl){best=HT.loc[k];bl=k.length;}}return best;}
function icoon(k){return '<svg viewBox="-8 -8 16 16" aria-hidden="true" style="color:'+(k<0?"#8B8676":HT.col[k])+'"><circle r="8" fill="currentColor"/><g fill="#F0EEE2" style="color:#F0EEE2">'+(k<0?'<circle r="2"/>':HT.gly[k])+'</g></svg>';}
function stijl(svg){var nieuw=false;
  svg.querySelectorAll(".mk:not([data-hs])").forEach(function(mk){var d=mk.querySelector(".dot");if(!d)return;nieuw=true;
    var k=typeOf(mk);mk.setAttribute("data-hs",String(k));if(isJong(mk))mk.classList.add("hs-jong");mk.style.color=k<0?"#8B8676":HT.col[k];
    var r=(+d.getAttribute("r")||6)*HT.groot;d.setAttribute("r",r.toFixed(2));
    var ri=mk.querySelector(".ring"),hi=mk.querySelector(".hit");if(ri)ri.setAttribute("r",(r+3.5).toFixed(2));if(hi)hi.setAttribute("r",Math.max(+hi.getAttribute("r")||0,r+3).toFixed(2));
    var g=document.createElementNS(NS,"g");g.setAttribute("class","hs-gl");
    g.setAttribute("transform","translate("+d.getAttribute("cx")+" "+d.getAttribute("cy")+") scale("+(r/8*.95).toFixed(3)+")");
    g.innerHTML=k<0?'<circle r="2"/>':HT.gly[k];d.parentNode.insertBefore(g,d.nextSibling);
    if(mk.classList.contains("hs-jong")){var br=document.createElementNS(NS,"circle");br.setAttribute("class","hs-bring");br.setAttribute("cx",d.getAttribute("cx"));br.setAttribute("cy",d.getAttribute("cy"));br.setAttribute("r",(r+2.6).toFixed(2));d.parentNode.insertBefore(br,d);}});
  if(nieuw||!svg.dataset.hsLg)legenda(svg);
  zk(svg);if(nieuw)plan(svg);}
/* inzoomen (knoppen, twee vingers, ctrl+scrollen) en groepjes: iconen die elkaar raken worden één rondje met een getal */
var MAXZ=8;
function zk(svg){if(svg.__zk)return svg.__zk;var b=svg.viewBox.baseVal;if(!b||!b.width)return null;
  var st=svg.__zk={base:[b.x,b.y,b.width,b.height],v:[b.x,b.y,b.width,b.height],busy:false,drag:false};
  var box=svg.closest(".map");if(box){box.classList.add("hs-zoom");
    var zb=document.createElement("div");zb.className="hs-zb";
    zb.innerHTML='<button type="button" data-z="in" aria-label="+">+</button><button type="button" data-z="out" aria-label="−">−</button><button type="button" data-z="reset" aria-label="Reset"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M3 7V3h4M17 7V3h-4M3 13v4h4M17 13v4h-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>';
    box.insertBefore(zb,box.firstChild);
    zb.addEventListener("click",function(e){var t=e.target.closest("[data-z]");if(!t)return;var z=t.dataset.z;
      if(z==="reset")zet(svg,st.base.slice());else zoomRond(svg,z==="in"?2:.5,st.v[0]+st.v[2]/2,st.v[1]+st.v[3]/2);});}
  /* slepen en knijpen */
  var P=new Map(),G=null;
  function pt(e){var r=svg.getBoundingClientRect();return {x:e.clientX,y:e.clientY,r:r};}
  svg.addEventListener("pointerdown",function(e){P.set(e.pointerId,pt(e));G={v:st.v.slice(),p:[...P.values()].map(function(q){return {x:q.x,y:q.y};}),r:svg.getBoundingClientRect(),moved:false};});
  svg.addEventListener("pointermove",function(e){if(!G||!P.has(e.pointerId))return;P.set(e.pointerId,pt(e));var ps=[...P.values()],r=G.r,u=G.v[2]/r.width;
    if(ps.length===1&&G.p.length===1){var dx=ps[0].x-G.p[0].x,dy=ps[0].y-G.p[0].y;if(!G.moved&&Math.hypot(dx,dy)<6)return;if(G.v[2]>=st.base[2]-.01)return;
      G.moved=true;st.drag=true;zet(svg,[G.v[0]-dx*u,G.v[1]-dy*u,G.v[2],G.v[3]],true);}
    else if(ps.length===2&&G.p.length===2){e.preventDefault();var d0=Math.hypot(G.p[0].x-G.p[1].x,G.p[0].y-G.p[1].y)||1,d1=Math.hypot(ps[0].x-ps[1].x,ps[0].y-ps[1].y);
      var mx=(G.p[0].x+G.p[1].x)/2-r.left,my=(G.p[0].y+G.p[1].y)/2-r.top,nx=(ps[0].x+ps[1].x)/2-r.left,ny=(ps[0].y+ps[1].y)/2-r.top;
      var w=Math.max(st.base[2]/MAXZ,Math.min(st.base[2],G.v[2]*d0/d1)),u2=w/r.width;G.moved=true;st.drag=true;
      zet(svg,[G.v[0]+mx*u-nx*u2,G.v[1]+my*u-ny*u2,w,w*st.base[3]/st.base[2]],true);}});
  function eind(e){if(!P.has(e.pointerId))return;P.delete(e.pointerId);if(P.size){G={v:st.v.slice(),p:[...P.values()].map(function(q){return {x:q.x,y:q.y};}),r:svg.getBoundingClientRect(),moved:true};return;}
    var mv=G&&G.moved;G=null;if(mv){plan(svg);setTimeout(function(){st.drag=false;},60);}else st.drag=false;}
  svg.addEventListener("pointerup",eind);svg.addEventListener("pointercancel",eind);
  svg.addEventListener("click",function(e){if(st.drag){e.stopPropagation();e.preventDefault();return;}
    var cl=e.target.closest&&e.target.closest(".hs-cl");if(cl){e.stopPropagation();openGroep(svg,cl);}},true);
  svg.addEventListener("wheel",function(e){if(!e.ctrlKey&&!e.metaKey)return;e.preventDefault();var r=svg.getBoundingClientRect();
    zoomRond(svg,Math.exp(-e.deltaY*.01),st.v[0]+(e.clientX-r.left)/r.width*st.v[2],st.v[1]+(e.clientY-r.top)/r.height*st.v[3],true);},{passive:false});
  /* filters van de gids (regio, type) verbergen stippen: groepjes opnieuw maken */
  st.obs=new MutationObserver(function(){if(!st.busy)plan(svg);});st.obs.observe(svg,{attributes:true,attributeFilter:["class","hidden","style"],subtree:true});
  return st;}
function zet(svg,v,snel){var st=svg.__zk,B=st.base,w=Math.max(B[2]/MAXZ,Math.min(B[2],v[2])),h=w*B[3]/B[2];
  var x=Math.max(B[0],Math.min(B[0]+B[2]-w,v[0])),y=Math.max(B[1],Math.min(B[1]+B[3]-h,v[1]));st.v=[x,y,w,h];
  svg.setAttribute("viewBox",st.v.map(function(n){return n.toFixed(2);}).join(" "));
  var z=w<B[2]-.01;svg.classList.toggle("hs-zoomed",z);var box=svg.closest(".map");
  if(box){var zb=box.querySelector(".hs-zb");if(zb){zb.querySelector('[data-z="out"]').disabled=!z;zb.querySelector('[data-z="reset"]').disabled=!z;zb.querySelector('[data-z="in"]').disabled=w<=B[2]/MAXZ+.01;}}
  if(snel)schaal(svg);else plan(svg);}
function zoomRond(svg,f,cx,cy,snel){var st=svg.__zk,v=st.v,w=v[2]/f,h=v[3]/f;zet(svg,[cx-(cx-v[0])/f,cy-(cy-v[1])/f,w,h],snel);if(snel){clearTimeout(st.t);st.t=setTimeout(function(){plan(svg);},150);}}
function midden(mk){var d=mk.querySelector(".dot");return [+d.getAttribute("cx"),+d.getAttribute("cy")];}
function schaal(svg){var st=svg.__zk,u=st.v[2]/st.base[2];st.busy=true;
  svg.querySelectorAll(".mk[data-hs]").forEach(function(mk){var c=midden(mk);mk.setAttribute("transform","translate("+c[0]+" "+c[1]+") scale("+u.toFixed(4)+") translate("+(-c[0])+" "+(-c[1])+")");});
  svg.querySelectorAll(".hs-cl").forEach(function(g){g.setAttribute("transform","translate("+g.dataset.x+" "+g.dataset.y+") scale("+u.toFixed(4)+")");});
  svg.__zk.busy=false;}
var PQ=new Set(),PR=0;
function plan(svg){PQ.add(svg);if(!PR)PR=requestAnimationFrame(function(){PR=0;PQ.forEach(groepen);PQ.clear();});}
function groepen(svg){var st=zk(svg);if(!st)return;st.busy=true;var u=st.v[2]/st.base[2];
  svg.querySelectorAll(".hs-cl").forEach(function(g){g.remove();});
  svg.querySelectorAll(".mk.hs-clh").forEach(function(m){m.classList.remove("hs-clh");});
  schaal(svg);st.busy=true;
  var ms=[].slice.call(svg.querySelectorAll(".mk[data-hs]")).filter(function(m){return getComputedStyle(m).display!=="none";});
  var r0=ms.length?(+ms[0].querySelector(".dot").getAttribute("r")||9):9,R=r0*1.7*u,out=[];
  if(st.v[2]>st.base[2]/MAXZ+.01)ms.forEach(function(m){if(m.classList.contains("sel"))return;var c=midden(m),best=null,bd=R*R;
    out.forEach(function(g){var d=(g.x-c[0])*(g.x-c[0])+(g.y-c[1])*(g.y-c[1]);if(d<bd){bd=d;best=g;}});
    if(best){best.m.push(m);}else out.push({x:c[0],y:c[1],m:[m]});});
  var html="";out.forEach(function(g){if(g.m.length<2)return;var x=0,y=0;g.m.forEach(function(m){var c=midden(m);x+=c[0];y+=c[1];m.classList.add("hs-clh");});
    x/=g.m.length;y/=g.m.length;var n=g.m.length,rr=n<10?10.5:12.5,jg=GEBON&&g.m.some(function(m){return m.classList.contains("hs-jong");});
    html+='<g class="hs-cl" role="button" tabindex="0" data-x="'+x.toFixed(1)+'" data-y="'+y.toFixed(1)+'" data-i="'+g.m.map(function(m){return m.dataset.i;}).join(",")+'" transform="translate('+x.toFixed(1)+' '+y.toFixed(1)+') scale('+u.toFixed(4)+')"><circle class="hs-clh-hit" r="'+(rr+4)+'"/><circle class="hs-cld" r="'+rr+'"/><text dy=".36em">'+n+'</text>'+(jg?'<circle class="hs-badge" cx="'+(rr*.72).toFixed(1)+'" cy="'+(-rr*.72).toFixed(1)+'" r="3.8"/>':"")+'</g>';});
  if(html)svg.insertAdjacentHTML("beforeend",html);
  /* eigen wijzigingen niet als filterwijziging zien: anders tekende de kaart elk beeldje opnieuw (batterij) */
  if(st.obs)st.obs.takeRecords();
  st.busy=false;}
function openGroep(svg,g){var st=svg.__zk,ids=g.dataset.i.split(","),x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
  ids.forEach(function(i){var m=svg.querySelector('.mk[data-i="'+i+'"]');if(!m)return;var c=midden(m);x0=Math.min(x0,c[0]);y0=Math.min(y0,c[1]);x1=Math.max(x1,c[0]);y1=Math.max(y1,c[1]);});
  var w=Math.min(st.v[2]/2,Math.max(st.base[2]/MAXZ,(x1-x0)*3,(y1-y0)*3*st.base[2]/st.base[3])),h=w*st.base[3]/st.base[2];
  zet(svg,[(x0+x1)/2-w/2,(y0+y1)/2-h/2,w,h]);}
/* voor bron/test_ontwerp.py: inzoomen op een gebied (null = hele kaart) */
window.__HSZOOM=function(svg,v){var st=zk(svg);if(!st)return;zet(svg,v?v:st.base.slice());};
document.addEventListener("keydown",function(e){var g=e.target.closest&&e.target.closest(".hs-cl");if(g&&(e.key==="Enter"||e.key===" ")){e.preventDefault();openGroep(g.closest("svg"),g);}});
function legenda(svg){var box=svg.closest(".map"),lg=box&&box.querySelector(".maplegend");if(!lg)return;svg.dataset.hsLg="1";
  var l=taal(),onz=svg.querySelector(".mk.w")!==null;lg.classList.add("hs-lg");
  var nj=svg.querySelectorAll(".mk.hs-jong").length;
  lg.innerHTML=(nj?'<span class="hs-gebrow"><button type="button" class="hs-gebbtn" data-hsgeb="aan" aria-pressed="'+GEBON+'"><span class="sw"></span>'+HT.geb[l]+' <span class="n">'+nj+'</span></button>'+(GEBON?'<button type="button" class="hs-gebx" data-hsgeb="alleen" aria-pressed="'+GEBALL+'">'+(GEBALL?HT.terug[l]:HT.alleen[l])+'</button>':"")+'</span>':"")+
    '<span class="hs-lgt">'+HT.uit[l]+'</span>'+(onz?'<span class="hs-onz"><i></i>'+HT.onz[l]+'</span>':"");
  chips();}
/* de typeknoppen boven de kaart (bron/locatietypes.js) krijgen het icoon van hun type */
function chips(){var l=taal();document.querySelectorAll(".lt-chip").forEach(function(b){var t=b.dataset.t;if(!t){b.classList.add("hs-alle");return;}
  var k=HT.ti[t];if(k===undefined||b.querySelector("svg"))return;b.insertAdjacentHTML("afterbegin",icoon(k));b.classList.add("hs-tc");});}
var rq=0;function alles(){rq=0;document.querySelectorAll(".map svg").forEach(function(s){if(s.querySelector(".mk"))stijl(s);});}
new MutationObserver(function(){if(!rq)rq=requestAnimationFrame(function(){alles();chips();});}).observe(document.body,{childList:true,subtree:true});
new MutationObserver(function(){document.querySelectorAll(".map svg[data-hs-lg]").forEach(legenda);}).observe(document.documentElement,{attributes:true,attributeFilter:["lang","class"]});
alles();
})();
</script>
"""

JS2 = r"""<script>
(function(){
/* gidspagina overzichtelijker (17-10-2026): kaart en overzicht open bovenaan, compacte hoofdtabel, korter plan, hoofdletters */
var ONB=/^(onbekend|unknown|inconnu|inconnue|unbekannt|sconosciuto|non noto|desconocido|desconhecido|ukendt|neznámé|okänd|okänt)$/i;
var MIST={nl:"Nog niet:",en:"Not yet:",fr:"Pas encore :",de:"Noch nicht:",it:"Non ancora:",es:"Aún no:",pt:"Ainda não:",da:"Endnu ikke:",cs:"Zatím ne:",sv:"Inte än:"};
function taal(){var l=(document.documentElement.lang||"nl").slice(0,2);return MIST[l]?l:"nl";}
function open(b){var t=b&&b.querySelector(":scope > h2 .ctog");if(t&&t.getAttribute("aria-expanded")==="false")t.click();}
var klaar=false;
function opbouw(){if(klaar)return;var w=document.getElementById("main")||document.querySelector(".wrap"),nav=document.querySelector("nav.toc"),loc=document.getElementById("locaties"),sr=document.getElementById("soorten");
  if(!w||!nav||!loc||!loc.querySelector(".ctog"))return;klaar=true;
  /* volgorde: In het kort, Per locatie (kaart), Overzicht; alles ingeklapt (17-10-2026) */
  var tl=document.getElementById("tldr"),na=tl||nav;if(tl)nav.insertAdjacentElement("afterend",tl);
  na.insertAdjacentElement("afterend",loc);if(sr)loc.insertAdjacentElement("afterend",sr);
  /* de lange lijst met kaartjes onder de kaart ingeklapt */
  loc.querySelectorAll(":scope > .cbody > details[open]").forEach(function(d){d.open=false;});
  /* tabbladen in dezelfde volgorde */
  var al=nav.querySelector('a[href="#locaties"]'),as=nav.querySelector('a[href="#soorten"]');
  if(al)nav.insertBefore(al,nav.firstChild);if(as&&al)al.insertAdjacentElement("afterend",as);
  /* In het kort: tabel Totaaloverzicht weg (alleen de korte punten blijven) */
  document.querySelectorAll("#tldr .tscroll").forEach(function(t){if(!t.querySelector(".tw-n"))return;t.classList.add("hs-weg");var h=t.previousElementSibling;if(h&&h.tagName==="H3"&&!h.classList.contains("rg-kop"))h.classList.add("hs-weg");});
  /* nieuwe namen voor twee kopjes (kop en tabblad) */
  var NAAM={soorten:{nl:"Per kat",en:"By cat",fr:"Par félin",de:"Nach Katze",it:"Per felino",es:"Por felino",pt:"Por felino",da:"Efter kat",cs:"Podle kočky",sv:"Per katt"},
    route:{nl:"Routeplanner",en:"Route planner",fr:"Planificateur d’itinéraire",de:"Routenplaner",it:"Pianificatore di percorso",es:"Planificador de ruta",pt:"Planeador de rotas",da:"Ruteplanlægger",cs:"Plánovač trasy",sv:"Ruttplanerare"}};
  Object.keys(NAAM).forEach(function(id){var el=[document.querySelector("#"+id+" > h2 .ctog > span"),nav.querySelector('a[href="#'+id+'"]')];
    el.forEach(function(e){if(!e)return;var sp=e.querySelectorAll("[class^='l-']");if(sp.length)sp.forEach(function(x){var l=x.className.slice(2);if(NAAM[id][l])x.textContent=NAAM[id][l];});else e.textContent=NAAM[id].nl;});});
  /* hoofdtabel onder Per kat: de lijst staat direct onder de soortknoppen (17-10-2026) */
  var reg=document.getElementById("register"),rb=reg&&reg.querySelector(":scope > .cbody"),sb=sr&&sr.querySelector(":scope > .cbody");
  if(reg&&rb&&sb){reg.id="hs-register-oud";reg.classList.add("hs-weg");var d=document.createElement("div");d.id="register";d.className="hs-reg";
    while(rb.firstChild)d.appendChild(rb.firstChild);sb.appendChild(d);var ar=nav.querySelector('a[href="#register"]');if(ar)ar.remove();}
  rijen();mist();hoofd();
  var rows=document.getElementById("rows");if(rows)new MutationObserver(rijen).observe(rows,{childList:true});
  var sp=document.getElementById("rt-sp");if(sp)new MutationObserver(mist).observe(sp,{childList:true,subtree:true});
  new MutationObserver(function(){mist();}).observe(document.documentElement,{attributes:true,attributeFilter:["lang","class"]});}
/* hoofdtabel: groepjes per soort, "onbekend" weg, tik op een regel voor details */
function rijen(){var prev=null;document.querySelectorAll("#rows > tr").forEach(function(tr){var sp=tr.querySelector("td.sp"),k=sp?sp.textContent.trim():"";
  tr.classList.toggle("hs-same",k===prev);tr.classList.toggle("hs-grp",k!==prev);prev=k;
  tr.querySelectorAll("td").forEach(function(td){if(ONB.test(td.textContent.trim()))td.classList.add("hs-unk");});});}
document.addEventListener("click",function(e){var tr=e.target.closest&&e.target.closest("#rows > tr");if(!tr||e.target.closest("a"))return;
  if(!matchMedia("(max-width:760px)").matches)return;tr.classList.toggle("hs-open");});
/* Plan je bezoek: welke bevestigde soorten je met je keuze nog mist */
function mist(){var sc=document.getElementById("rt-score"),sp=document.getElementById("rt-sp");if(!sc||!sp)return;
  var oud=sc.querySelector(".hs-mist");if(oud)oud.remove();
  var b=sc.querySelector("b"),m=sc.textContent.replace(b?b.textContent:"","").match(/\d+/),gezien=b?+b.textContent:0,tot=m?+m[0]:0;
  if(!gezien||gezien>=tot)return;
  var nog=[].slice.call(sp.querySelectorAll(".rchip:not(.on)")).map(function(c){return (c.firstChild&&c.firstChild.nodeType===3?c.firstChild.textContent:c.textContent).trim();}).slice(0,tot-gezien);
  if(nog.length)sc.insertAdjacentHTML("beforeend",'<span class="hs-mist"><b>'+MIST[taal()]+'</b> '+nog.map(function(x){return x.replace(/[<&]/g,"");}).join(", ")+'</span>');}
/* locatiekaartjes: tekst begint met een hoofdletter */
function hoofd(){document.querySelectorAll(".loclist.cards li > span:not(.plc)").forEach(function(s){var n=s.firstChild;if(n&&n.nodeType===3&&/^\s*[a-zà-ÿ]/.test(n.textContent))n.textContent=n.textContent.replace(/^(\s*)(.)/,function(_,a,c){return a+c.toUpperCase();});});}
opbouw();if(!klaar){document.addEventListener("DOMContentLoaded",opbouw);var n=0,iv=setInterval(function(){opbouw();if(klaar||++n>40)clearInterval(iv);},100);}
})();
</script>
"""

TCOL = ["#2F6B2F", "#2766B0", "#7A5230", "#C98500", "#8A3FA0", "#16878A", "#B0306A", "#666158"]   # zelfde als op de startpagina
GLY = ['<ellipse cx="0" cy="1.7" rx="2.6" ry="2.2"/><circle cx="-3.1" cy="-1.3" r="1.15"/><circle cx="-1.15" cy="-3.2" r="1.15"/><circle cx="1.15" cy="-3.2" r="1.15"/><circle cx="3.1" cy="-1.3" r="1.15"/>',
       '<circle cx="0" cy="-1.4" r="3.2"/><rect x="-.75" y="1" width="1.5" height="3.6"/>',
       '<path d="M0-4.8 3.9 1.6H-3.9Z"/><rect x="-.75" y="1.4" width="1.5" height="3.1"/>',
       '<path d="M-4.4 1.8V-.4l1.5-2.6h4.6l1.6 2.6h1.1v2.2Z"/><circle cx="-2.3" cy="2.5" r="1.4"/><circle cx="2.3" cy="2.5" r="1.4"/>',
       '<g fill="none" stroke="currentColor" stroke-width="1.2"><circle cx="0" cy="-1" r="3.1"/><path d="M0-1-2.6 4.4M0-1 2.6 4.4M-3.1-1H3.1M0-4.1V2.1"/></g>',
       '<path d="M-3.8 3.8C-3.8-1.8-.4-4.2 4-4.2 4 .2 1.6 3.8-3.8 3.8Z"/>',
       '<path d="M0 3.9C-4.8.8-4.3-3.7-1.5-3.7-.6-3.7 0-3 0-2.4 0-3 .6-3.7 1.5-3.7 4.3-3.7 4.8.8 0 3.9Z"/>',
       '<path d="M-4.2.3 0-4 4.2.3H2.9V4H-2.9V.3Z"/>']
UITLEG = {"nl": "Kleur en icoon tonen het soort locatie (zie de knoppen boven de kaart; tik erop om te filteren).", "en": "Colour and icon show the type of location (see the buttons above the map; tap one to filter).",
          "fr": "La couleur et l’icône indiquent le type de lieu (voir les boutons au-dessus de la carte ; touchez-en un pour filtrer).", "de": "Farbe und Symbol zeigen die Art des Ortes (siehe die Knöpfe über der Karte; zum Filtern antippen).",
          "it": "Colore e icona indicano il tipo di luogo (vedi i pulsanti sopra la mappa; toccane uno per filtrare).", "es": "El color y el icono indican el tipo de lugar (mira los botones encima del mapa; toca uno para filtrar).",
          "pt": "A cor e o ícone mostram o tipo de local (vê os botões acima do mapa; toca num para filtrar).",
          "da": "Farve og ikon viser typen af sted (se knapperne over kortet; tryk på en for at filtrere).",
          "cs": "Barva a ikona ukazují typ místa (viz tlačítka nad mapou; klepnutím na jedno filtruješ).",
          "sv": "Färg och ikon visar typen av plats (se knapparna ovanför kartan; tryck på en för att filtrera)."}
ONZ = {"nl": "open stip: alleen onzekere vermeldingen", "en": "open dot: uncertain entries only", "fr": "point vide : mentions incertaines seulement",
       "de": "offener Punkt: nur unsichere Einträge", "it": "punto vuoto: solo segnalazioni incerte", "es": "punto vacío: solo menciones inciertas", "pt": "ponto vazio: só menções incertas",
       "da": "åben prik: kun usikre angivelser",
       "cs": "prázdná tečka: jen nejisté zmínky",
       "sv": "öppen prick: bara osäkra uppgifter"}
LANDNAAM = {
    "nl": {"nl": "Nederland", "en": "Netherlands"}, "be": {"nl": "België", "en": "Belgium", "fr": "Belgique"},
    "lu": {"nl": "Luxemburg", "en": "Luxembourg", "fr": "Luxembourg", "de": "Luxemburg"}, "de": {"nl": "Duitsland", "en": "Germany", "de": "Deutschland"},
    "fr": {"nl": "Frankrijk", "en": "France", "fr": "France"}, "at": {"nl": "Oostenrijk", "en": "Austria", "de": "Österreich"},
    "ch": {"nl": "Zwitserland", "en": "Switzerland", "de": "Schweiz", "fr": "Suisse", "it": "Svizzera"}, "uk": {"nl": "Verenigd Koninkrijk", "en": "United Kingdom"},
    "it": {"nl": "Italië", "en": "Italy", "it": "Italia"}, "es": {"nl": "Spanje", "en": "Spain", "es": "España"},
    "ie": {"nl": "Ierland", "en": "Ireland"}, "pt": {"nl": "Portugal", "en": "Portugal", "pt": "Portugal"},
    "dk": {"nl": "Denemarken", "en": "Denmark", "da": "Danmark"},
    "cz": {"nl": "Tsjechië", "en": "Czechia", "cs": "Česko"},
    "se": {"nl": "Zweden", "en": "Sweden", "sv": "Sverige"}}
ONDER = {"nl": "Wilde katachtigen in dierentuinen en parken", "en": "Wild cats in zoos and animal parks", "fr": "Félins sauvages dans les zoos et parcs animaliers",
         "de": "Wilde Katzen in Zoos und Tierparks", "it": "Felini selvatici in zoo e parchi faunistici", "es": "Felinos salvajes en zoos y parques de animales",
         "pt": "Felinos selvagens em zoos e parques de animais",
         "da": "Vilde katte i zoologiske haver og dyreparker",
         "cs": "Divoké kočkovité šelmy v zoologických zahradách a zooparcích",
         "sv": "Vilda kattdjur i djurparker och parker"}
def kopdata(c, langs, vlag):
    return {"land": {l: LANDNAAM[c][l] for l in langs}, "onder": {l: ONDER[l] for l in langs}, "vlag": vlag}

GEB = {'nl': 'Recent geboren', 'en': 'Recently born', 'fr': 'Naissances récentes', 'de': 'Kürzlich geboren', 'it': 'Nati di recente', 'es': 'Nacimientos recientes', 'pt': 'Nascimentos recentes', 'da': 'Nyfødte', 'cs': 'Nedávno narozená mláďata', 'sv': 'Nyfödda'}
ALLEEN = {'nl': 'Alleen deze tonen', 'en': 'Show only these', 'fr': 'N’afficher que ceux-ci', 'de': 'Nur diese zeigen', 'it': 'Mostra solo questi', 'es': 'Mostrar solo estos', 'pt': 'Mostrar só estes', 'da': 'Vis kun disse', 'cs': 'Zobrazit jen tyto', 'sv': 'Visa bara dessa'}
TERUG = {'nl': 'Alle locaties tonen', 'en': 'Show all locations', 'fr': 'Afficher tous les lieux', 'de': 'Alle Orte zeigen', 'it': 'Mostra tutti i luoghi', 'es': 'Mostrar todos los lugares', 'pt': 'Mostrar todos os locais', 'da': 'Vis alle steder', 'cs': 'Zobrazit všechna místa', 'sv': 'Visa alla platser'}
def kaartdata(types, locinfo, langs):
    """types: de lijst uit locatietypes.json; locinfo: {locatienaam: typenaam (nl)}."""
    idx = {t["nl"]: k for k, t in enumerate(types)}
    return {"loc": {n: idx.get(tp, -1) for n, tp in locinfo.items()}, "ti": idx, "groot": 1.5, "col": TCOL, "gly": GLY,
            "nm": {l: [t.get(l) or t["en"] for t in types] for l in langs}, "uit": {l: UITLEG[l] for l in langs}, "onz": {l: ONZ[l] for l in langs},
            "geb": {l: GEB[l] for l in langs}, "alleen": {l: ALLEEN[l] for l in langs}, "terug": {l: TERUG[l] for l in langs}}

def toepassen(doc, langs, base, kaart=None, kop=None):
    """Huisstijl op een gids of deelstaatpagina zetten (website). kaart: uitvoer van kaartdata()."""
    doc = lettertypen(doc)
    m = re.search(r'<nav class="landbar".*?</nav>', doc, re.S)
    assert m, "landbar niet gevonden"
    # het pootje krijgt het id van de oude link "← Alle landen": het script van de gids luistert daarnaar
    balk = bovenbalk(langs, base).replace('<a class="hs-brand" href=', '<a class="hs-brand" id="naar-landen" href=', 1)
    doc = doc[:m.start()] + f"<style>{CSS}</style>\n" + balk + doc[m.end():]
    k = re.search(r'<div class="kofi-wrap"><aside class="kofi-card".*?</aside></div>', doc, re.S)
    assert k, "Ko-fi-blok niet gevonden"
    doc = doc[:k.start()] + voet(langs) + doc[k.end():]
    i = doc.rindex("</body>")
    data = ("<script>window.__HSK=" + json.dumps(kop, ensure_ascii=False).replace("</", "<\\/") + ";</script>\n") if kop else ""
    data += ("<script>window.__HST=" + json.dumps(kaart, ensure_ascii=False).replace("</", "<\\/") + ";</script>\n") if kaart else ""
    return doc[:i] + data + JS + JS2 + doc[i:]
