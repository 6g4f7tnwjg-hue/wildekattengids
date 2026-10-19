'use strict';
(function(){
const D = window.SG_DATA;
const SGP = window.SG_PAGE || null;   // losse soortpagina: {no, lang}
const INIT_TITLE = document.title;
const KOFI_URL = 'https://ko-fi.com/katalogue';
const $ = s => document.querySelector(s);
const $$ = s => Array.from(document.querySelectorAll(s));
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let L = 'nl';
try { const s = localStorage.getItem('sg-lang'); if (s === 'en' || s === 'nl') L = s; else if (!/^nl/i.test(navigator.language || 'nl')) L = 'en'; } catch(e) {}
try { const q = new URLSearchParams(location.search).get('lang'); if (q === 'nl' || q === 'en') { L = q; localStorage.setItem('sg-lang', L); } } catch(e) {}
if (SGP) { L = SGP.lang; try { localStorage.setItem('sg-lang', L); } catch(e) {} }
/* adres van een losse soortpagina (relatief t.o.v. de map spottersgids) */
// testpagina (window.SG_TEST): soortpagina's binnen dezelfde pagina via #soort-<nr>
const spHref = no => window.SG_TEST ? '#soort-' + no : (L === 'en' ? 'en/' : '') + D.slugs[L][no] + '/';
const UPDATED = '2026-10-19';   // datum (jjjj-mm-dd) van de laatste wijziging in de gegevens, gezet door build.py
const T = o => o == null ? '' : (typeof o === 'string' ? o : (o[L] != null ? o[L] : o.nl));

/* ---------- vaste teksten ---------- */
const U = {
  title:{nl:'Spottersgids voor wilde katten',en:"Wild Cat Spotter's Guide"},
  brandSub:{nl:'wilde katten · J. Gelens',en:'wild cats · J. Gelens'},
  navSpecies:{nl:'Soorten',en:'Species'}, navTop:{nl:'Topspots',en:'Top spots'}, navMap:{nl:'Kaart',en:'Map'},
  navResp:{nl:'Verantwoord spotten',en:'Responsible spotting'}, navEur:{nl:'Katten in Europa',en:'Cats in Europe'},
  navPack:{nl:'Paklijst',en:'Packing list'}, navAbout:{nl:'Over deze gids',en:'About this guide'}, navVisit:{nl:'Bezoekersgids: katten in dierentuinen',en:'Visitor’s Guide: cats in zoos'}, navKofi:{nl:'Steun de gids via Ko-fi',en:'Support the guide on Ko-fi'}, navReport:{nl:'Melden',en:'Report'}, navMore:{nl:'Meer',en:'More'}, srch:{nl:'Zoeken',en:'Search'}, srchL:{nl:'Zoek een kat of een plek',en:'Search for a cat or a place'}, srchPh:{nl:'Bijv. manoel, Pantanal of Botswana',en:'E.g. Pallas’s cat, Pantanal or Botswana'}, srchNone:{nl:'Niets gevonden',en:'Nothing found'},
  sub:{nl:'Waar je alle 42 wilde kattensoorten in het wild kunt zien, hoe groot je kans is en hoe je ze vindt.',en:'Where to see all 42 wild cat species in the wild, how good your chances are and how to find them.'},
  all:{nl:'Hele wereld',en:'Whole world'},
  topSub:{nl:'Plekken waar je een soort (bijna) zeker ziet, mits je de tijd neemt en in het goede seizoen gaat.',en:'Places where you will (almost) certainly see a species, as long as you take your time and go in the right season.'},
  showAll:{nl:'Toon alle topspots',en:'Show all top spots'}, showLess:{nl:'Toon minder',en:'Show fewer'},
  mapSub:{nl:'Markers staan op het midden van een reservaat of gebied, nooit op een hol of vaste rustplek.',en:'Markers sit at the centre of a reserve or area, never on a den or regular resting place.'},
  allCats:{nl:'Alle katten',en:'All cats'},
  noSpot:{nl:'Nog geen spotplek; volgt binnenkort',en:'No spotting site yet; coming soon'},
  catMap:{nl:'Waar zit welke kat? Kies een soort:',en:'Which cat lives where? Pick a species:'},
  catShown:{nl:'plekken op de kaart',en:'places on the map'},
  catShown1:{nl:'plek op de kaart',en:'place on the map'},
  alsoLbl:{nl:'Ook te zien op deze plekken:',en:'Also seen at these places:'},
  alsoNone:{nl:'— kies een kat —',en:'— pick a cat —'},
  alsoAt:{nl:'zie je ook bij:',en:'can also be seen at:'},
  zoomIn:{nl:'Inzoomen',en:'Zoom in'}, zoomOut:{nl:'Uitzoomen',en:'Zoom out'}, zoomReset:{nl:'Hele kaart tonen',en:'Show whole map'},
  lgToggle:{nl:'Kans {n} tonen of verbergen',en:'Show or hide chance {n}'},
  showLow:{nl:'Toon ook kans 1–2',en:'Also show chance 1–2'}, hideLow:{nl:'Verberg kans 1–2',en:'Hide chance 1–2'},
  listMap:{nl:'Plekken op de kaart',en:'Places on the map'}, listView:{nl:'Plekken in beeld',en:'Places in view'},
  listNone:{nl:'Geen plekken met deze kans in beeld.',en:'No places with this chance in view.'},
  listAll:{nl:'Toon alle plekken',en:'Show all places'},
  mapHint:{nl:'Tik op een marker om te zien welke katten je daar kunt vinden.',en:'Tap a marker to see which cats you can find there.'},
  search:{nl:'Zoek een soort (NL, Engels of Latijn)',en:'Search a species (Dutch, English or Latin)'},
  ready:{nl:'Klaar om te spotten',en:'Ready to spot'},
  soon:{nl:'Volgt binnenkort',en:'Coming soon'},
  noHits:{nl:'Geen soort gevonden.',en:'No species found.'},
  soonPage:{nl:'Soortpagina volgt binnenkort',en:'Species page coming soon'},
  toPage:{nl:'Naar de soortpagina',en:'Go to the species page'},
  season:{nl:'Seizoen',en:'Season'}, time:{nl:'Tijdstip',en:'Time of day'}, trip:{nl:'Soort tocht',en:'Type of trip'},
  bestPlace:{nl:'Beste plek',en:'Best place'}, bestTime:{nl:'Beste tijd',en:'Best time'},
  jPlaces:{nl:'Plekken',en:'Places'}, jMap:{nl:'Kaart',en:'Map'}, jTips:{nl:'Tips',en:'Tips'}, jStatus:{nl:'Status',en:'Status'}, jSources:{nl:'Bronnen',en:'Sources'},
  bestSpots:{nl:'De beste plekken',en:'The best places'},
  bestSpotsSub:{nl:'Op volgorde van kans. Tik op een plek voor alle details.',en:'In order of chance. Tap a place for all details.'},
  tips:{nl:'Spottips',en:'Spotting tips'},
  habitat:{nl:'Leefgebied en spotplekken',en:'Range and spotting sites'},
  habitatNote:{nl:'Gekleurd: leefgebied bij benadering (bron: De KATalogue, op basis van openbare verspreidingskaarten). Cijfers: de plekken hieronder; tik erop om de plek te openen.',en:'Shaded: approximate range (source: De KATalogue, based on public range maps). Numbers: the places listed below; tap one to open it.'},
  status:{nl:'Status en bedreigingen',en:'Status and threats'},
  threats:{nl:'Belangrijkste bedreigingen',en:'Main threats'},
  photos:{nl:"Foto's",en:'Photos'}, captive:{nl:'in gevangenschap',en:'in captivity'},
  sources:{nl:'Bronnen',en:'Sources'},
  back:{nl:'Alle soorten',en:'All species'},
  chance:{nl:'Kans',en:'Chance'},
  legend:{nl:'Kans:',en:'Chance:'},
  topStar:{nl:'topspot',en:'top spot'},
  cont:{eur:{nl:'Europa',en:'Europe'},afr:{nl:'Afrika',en:'Africa'},asia:{nl:'Azië',en:'Asia'},nam:{nl:'Noord-Amerika',en:'North America'},sam:{nl:'Midden- en Zuid-Amerika',en:'Central & South America'}},
  sc:{5:{nl:'bijna zeker',en:'almost certain'},4:{nl:'grote kans',en:'good chance'},3:{nl:'redelijke kans',en:'fair chance'},2:{nl:'kleine kans',en:'small chance'},1:{nl:'veel geluk nodig',en:'needs a lot of luck'}},
  scaleTitle:{nl:'Zo lees je de kansscore',en:'How to read the chance score'},
  scale:{5:{nl:'de meeste bezoekers met een goed geplande reis zien de soort',en:'most visitors on a well-planned trip see the species'},4:{nl:'grote kans',en:'good chance'},3:{nl:'redelijke kans',en:'fair chance'},2:{nl:'kleine kans',en:'small chance'},1:{nl:'alleen met veel geluk of via cameravallen',en:'only with a lot of luck or via camera traps'}},
  iucn:{LC:{nl:'Niet bedreigd',en:'Least Concern'},NT:{nl:'Gevoelig',en:'Near Threatened'},VU:{nl:'Kwetsbaar',en:'Vulnerable'},EN:{nl:'Bedreigd',en:'Endangered'},CR:{nl:'Ernstig bedreigd',en:'Critically Endangered'},NE:{nl:'Niet beoordeeld',en:'Not Evaluated'},DD:{nl:'Onvoldoende gegevens',en:'Data Deficient'}},
  footMade:{nl:'Een gids van J. Gelens. Soortgegevens, foto’s en verspreidingskaarten: De KATalogue. Plekken en kansen: zie de bronnen per soort.',en:'A guide by J. Gelens. Species data, photos and range maps: De KATalogue. Places and chances: see the sources on each species page.'},
  photoPre:{nl:'foto:',en:'photo:'},
  notFound:{nl:'Deze pagina bestaat niet (meer).',en:'This page does not exist.'},
  /* schermkoppen en onderbalk (Safari-stijl) */
  world:{nl:'Wereld',en:'World'}, navMoreT:{nl:'Meer',en:'More'},
  skMap:{nl:'Wilde katten in het wild',en:'Wild cats in the wild'},
  skSpecies:{nl:'Alle wilde katten en waar je ze ziet',en:'Every wild cat and where to see it'},
  skTop:{nl:'Plekken waar je (bijna) zeker een kat ziet',en:'Places where you’ll (almost) surely see a cat'},
  skMore:{nl:'Katten in Europa, spottips en meer',en:'Cats in Europe, spotting tips and more'},
  wSpecies:{nl:'soorten',en:'species'}, wSpecies1:{nl:'soort',en:'species'}, wPlaces:{nl:'plekken',en:'places'}, wPlace1:{nl:'plek',en:'place'},
  wTops:{nl:'topspots',en:'top spots'}, wTop1:{nl:'topspot',en:'top spot'}, wBig:{nl:'grote',en:'big'}, wSmall:{nl:'kleine',en:'small'},
  bigCats:{nl:'Grote katten',en:'Big cats'}, smallCats:{nl:'Kleine katten',en:'Small cats'},
  grpBig:{nl:'Pantherinae (grote katten)',en:'Pantherinae (big cats)'}, grpSmall:{nl:'Felinae (kleine katten)',en:'Felinae (small cats)'},
  bestChance:{nl:'beste kans',en:'best chance'},
  updated:{nl:'Bijgewerkt',en:'Updated'},
  pickCont:{nl:'Kies een werelddeel:',en:'Choose a continent:'}, pickCat:{nl:'Kies een kat:',en:'Choose a cat:'},
  inView:{nl:'In beeld',en:'In view'},
  listSub:{nl:'Grootste kans eerst. Tik op een plek om hem op de kaart te zien.',en:'Best chance first. Tap a place to see it on the map.'},
  back2:{nl:'Terug',en:'Back'},
  meerReport:{nl:'Zelf een kat gezien of klopt er iets niet?',en:'Seen a cat yourself or found a mistake?'},
  reportSub:{nl:'Gaat rechtstreeks naar de maker',en:'Goes straight to the author'}
};
const BIG = new Set([1,2,3,4,5,6,7]);   // Pantherinae: leeuw, tijger, jaguar, luipaard, sneeuwpanter, nevelpanter, soendanevelpanter
const IUCN_COL = {LC:'#4C7A3A',NT:'#7E8C2A',VU:'#B8860B',EN:'#C25B1E',CR:'#A3242B',NE:'#7A7868',DD:'#7A7868'};
const CONTS = ['eur','afr','asia','nam','sam'];

/* ---------- data ---------- */
const CATS = D.cats, BY = {}; CATS.forEach(c => BY[c.no] = c);
const SPOTS = D.spots, SPOT = {}; SPOTS.forEach(s => SPOT[s.id] = s);
const PAGES = D.pages;           // soortpagina's die af zijn
const SRC = D.sources;           // globale bronnenlijst
const BEST = {};                 // hoogste score per soort (alleen uit onderzochte plekken)
SPOTS.forEach(s => s.recs.forEach(r => { if (!BEST[r.no] || r.score > BEST[r.no]) BEST[r.no] = r.score; }));
const spotMax = s => Math.max(...s.recs.map(r => r.score));
const isTop = s => s.recs.some(r => r.top);
let FILTER = 'all', TAB = 'topspots', SEL = null, SHOWALL = false, Q = '', CAT = null, ALSO = null;
// startkaart: zichtbare kansen (standaard 3–5), ingezoomd kader (null = niet ingezoomd), hele lijst tonen
let SHOWN = new Set([3,4,5]), VIEW = null, LISTALL = false, DRAGGED = false;
TAB = 'kaart';   // de kaart is de pagina die opent
try { const f = localStorage.getItem('sg-cont'); if (f && (f === 'all' || CONTS.includes(f))) FILTER = f; } catch(e) {}
const narrow = () => window.innerWidth < 600;

/* ---------- kleine bouwstenen ---------- */
const scoreHtml = (n, big, compact) => `<span class="score${big?' big':''}" style="--c:var(--s${n})" title="${esc(T(U.chance))} ${n}/5 · ${esc(T(U.sc[n]))}"><span class="pips" aria-hidden="true">${[1,2,3,4,5].map(i=>`<i class="${i<=n?'on':''}"></i>`).join('')}</span><b>${compact ? `${n}/5` : `${esc(T(U.chance))} ${n} · ${esc(T(U.sc[n]))}`}</b></span>`;
const credit = cr => esc(String(cr || '').replace(/^foto:\s*/i, T(U.photoPre) + ' '));
const catName = c => T({nl:c.nl, en:c.en});
// foto's zijn losse bestanden; small = het kleine exemplaar voor ronde fotootjes en lijstjes
const img = (p, alt, eager, small) => `<img src="${esc(small ? p.sm : p.src)}" alt="${esc(alt)}" loading="${eager?'eager':'lazy'}" decoding="async">`;
const iucnHtml = code => `<span class="iucn" style="--ic:${IUCN_COL[code]||'#777'}"><b>${esc(code)}</b>${esc(T(U.iucn[code]||{nl:code,en:code}))}</span>`;
const contName = c => T(U.cont[c]);
// seizoen, tijdstip en soort tocht: één regel per stuk met een icoontje (label voor schermlezers en als tooltip)
const FICO = {
  season:'<rect x="3" y="4.5" width="14" height="12.5" rx="2"/><path d="M3 8.5h14M7 2.5v4M13 2.5v4"/>',
  time:'<circle cx="10" cy="10" r="7.5"/><path d="M10 5.5V10l3 2"/>',
  trip:'<path d="M2.5 13.5V10l2-4.5h9l2 4.5h2v3.5"/><path d="M2.5 10h15"/><circle cx="6" cy="14" r="1.8"/><circle cx="14" cy="14" r="1.8"/>'};
const factsHtml = r => `<ul class="facts">${['season','time','trip'].filter(k => T(r[k])).map(k =>
  `<li title="${esc(T(U[k]))}"><svg viewBox="0 0 20 20" aria-hidden="true">${FICO[k]}</svg><span><span class="sr">${esc(T(U[k]))}: </span>${esc(T(r[k]))}</span></li>`).join('')}</ul>`;
const placeLine = s => [T(s.area), T(s.country)].filter(Boolean).join(' · ');
const STAR = '<svg viewBox="-10 -10 20 20" aria-hidden="true"><path d="M0,-9 2.6,-3.2 8.6,-2.8 4,1.2 5.3,7.3 0,4.1 -5.3,7.3 -4,1.2 -8.6,-2.8 -2.6,-3.2Z" fill="currentColor"/></svg>';
const CHEV = '<svg class="chev" viewBox="0 0 10 10" aria-hidden="true"><path d="M1.5 3.5 5 7l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>';

/* ---------- kaart ---------- */
const W = 720, H = 284;
const proj = (lat, lon) => [(lon + 180) * 2, (84 - lat) * 2];
const BOX = { all:[0,0,720,284], eur:[330,22,140,82], afr:[318,70,162,174], asia:[404,34,290,164], nam:[8,12,262,130], sam:[108,110,206,176] };
// maakt een uitsnede met verhouding r (breedte/hoogte) rond een kader
function fit(b, r){
  let [x,y,w,h] = b;
  if (w/h > r){ const nh = w/r; y -= (nh-h)/2; h = nh; } else { const nw = h*r; x -= (nw-w)/2; w = nw; }
  if (w > W){ w = W; h = w/r; } if (h > H){ h = H; w = Math.min(W, h*r); }
  x = Math.max(0, Math.min(W-w, x)); y = Math.max(0, Math.min(H-h, y));
  return [x,y,w,h];
}
// op een telefoon mag een werelddeel hoger worden, zodat het het scherm vult
const ratioFor = b => narrow() ? Math.max(.8, Math.min(1, b[2]/b[3])) : Math.max(1.9, Math.min(W/H, b[2]/b[3]));
const GRAT = (() => { let g=''; for(let lon=-150; lon<180; lon+=30) g+=`M${(lon+180)*2},0V284`; for(let lat=60; lat>-60; lat-=30) g+=`M0,${(84-lat)*2}H720`; return g; })();
const starPath = (x, y, R) => { let d=''; for (let i=0;i<10;i++){ const a = -Math.PI/2 + i*Math.PI/5, rr = i%2 ? R*.48 : R; d += (i?'L':'M') + (x+rr*Math.cos(a)).toFixed(2) + ',' + (y+rr*Math.sin(a)).toFixed(2); } return d + 'Z'; };
function mapSvg(opts){
  const vb = opts.vb || (opts.world ? [0,0,W,H] : fit(opts.box, ratioFor(opts.box)));
  const u = vb[2] / opts.cw;                       // kaarteenheden per schermpixel
  const k = vb[2]/W, mr = opts.mr || 6.5;
  const rng = opts.range ? `<path class="rng" d="${opts.range}" stroke-width="${.6*k}"/>` : '';
  // markers in schermpixels; de schaal u houdt ze even groot, ook tijdens het zoomen
  const mks = opts.markers.map(m => {
    const [x,y] = proj(m.lat, m.lon);
    const r = m.num ? 10 : mr;
    const shape = m.star ? `<path class="dot" d="${starPath(0, 0, r*1.7)}" fill="var(--s${m.score})" stroke-width="1.6"/>`
                         : `<circle class="dot" r="${r}" fill="var(--s${m.score})" stroke-width="1.6"/>`;
    return `<g class="mk${m.sel?' sel':''}${m.dim?' dim':''}" data-id="${esc(m.id)}" data-x="${x}" data-y="${y}" transform="translate(${x} ${y}) scale(${u})" tabindex="0" role="button" aria-label="${esc(m.label)}">
      <circle r="16" fill="transparent"/>${shape}
      ${m.num?`<text font-size="13">${m.num}</text>`:''}</g>`;
  }).join('');
  // landsgrenzen en landnamen (alleen soortkaart); namen op schermgrootte, grootste landen eerst, niet over elkaar
  let brd = '';
  if (opts.borders) {
    const [vx,vy,vw,vh] = vb, placed = [], fs = 11;
    const lbl = D.labels.filter(l => l.w >= vw * .07 && l.x > vx + 4*u*fs && l.x < vx + vw - 4*u*fs && l.y > vy + fs*u && l.y < vy + vh - fs*u)
      .sort((a,b) => b.w - a.w).filter(l => { const sx = (l.x - vx)/u, sy = (l.y - vy)/u;
        if (placed.some(([px,py]) => Math.abs(px - sx) < 70 && Math.abs(py - sy) < 16)) return false; placed.push([sx,sy]); return true; });
    brd = `<path class="brd" d="${D.borders}"/>` + lbl.map(l => `<text class="cl" x="${l.x}" y="${l.y}" font-size="${fs*u}" stroke-width="${2.5*u}">${esc(T(l))}</text>`).join('');
  }
  return `<svg class="map${opts.cls?' '+opts.cls:''}" viewBox="${vb.join(' ')}" role="img" aria-label="${esc(opts.label)}">
    <path class="grat" d="${GRAT}" stroke-width="${.5*k}"/><path class="land" d="${D.land}"/>${rng}${brd}${mks}</svg>`;
}
function bboxOfPath(p){
  const n = (p.match(/-?\d+\.?\d*/g) || []).map(Number); let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
  for (let i=0;i+1<n.length;i+=2){ x0=Math.min(x0,n[i]); x1=Math.max(x1,n[i]); y0=Math.min(y0,n[i+1]); y1=Math.max(y1,n[i+1]); }
  return [x0,y0,x1,y1];
}
function legendHtml(withStar){
  return `<div class="maplegend"><span>${esc(T(U.legend))}</span>${[5,4,3,2,1].map(n=>`<span><i style="--c:var(--s${n})"></i>${n}</span>`).join('')}${withStar?`<span style="color:var(--ink)">${STAR}<span style="color:var(--muted)">${esc(T(U.topStar))}</span></span>`:''}</div>`;
}
function bindMarkers(root, fn){
  root.querySelectorAll('.mk').forEach(g => { g.onclick = () => fn(g.dataset.id); g.onkeydown = e => { if (e.key==='Enter'||e.key===' ') { e.preventDefault(); fn(g.dataset.id); } }; });
}

/* ---------- navigatie: onderbalk met vier schermen, menu (☰) en voet ---------- */
const VISIT_URL = 'https://yeetkitty.github.io/wildekattengids/';
const ICO = {
  map:'<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
  paw:'<ellipse cx="12" cy="15.5" rx="5" ry="4.3"/><ellipse cx="5.3" cy="10.5" rx="2" ry="2.6"/><ellipse cx="9.3" cy="6.7" rx="2" ry="2.7"/><ellipse cx="14.7" cy="6.7" rx="2" ry="2.7"/><ellipse cx="18.7" cy="10.5" rx="2" ry="2.6"/>',
  star:'<path d="M12 3.5l2.6 5.3 5.9.9-4.25 4.1 1 5.8L12 16.9l-5.25 2.7 1-5.8L3.5 9.7l5.9-.9z"/>',
  menu:'<path d="M4 6h16M4 12h16M4 18h16"/>',
  eur:'<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
  resp:'<path d="M12 3l7 3v5c0 4.5-3 8.3-7 10-4-1.7-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/>',
  pack:'<path d="M7 9a5 5 0 0 1 10 0v10a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2z"/><path d="M10 4h4M7 14h10M10 14v3h4v-3"/>',
  flag:'<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>',
  info:'<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
  visit:'<path d="M3 10l9-6 9 6"/><path d="M5 10v9M19 10v9M9.5 10v9M14.5 10v9M3 21h18"/>',
  kofi:'<path d="M4 8h12v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M16 9h1.5a2.5 2.5 0 0 1 0 5H16"/><path d="M8 3v2M12 3v2"/>'};
const svgI = (ic, cls) => `<svg${cls ? ` class="${cls}"` : ''} viewBox="0 0 24 24" aria-hidden="true" ${ic === 'paw' ? 'fill="currentColor"' : 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'}>${ICO[ic]}</svg>`;
const TABS = [['kaart','navMap','map'],['soorten','navSpecies','paw'],['topspots','navTop','star'],['meer','navMoreT','menu']];
// menu (☰) en scherm Meer tonen dezelfde onderdelen
const MENU = [['europa','navEur','eur'],['verantwoord','navResp','resp'],['paklijst','navPack','pack'],['melden','navReport','flag']];
const MENU2 = [['over','navAbout','info']];
function renderChrome(route){
  document.documentElement.lang = L;
  document.title = (SGP && route.page === SGP.no && L === SGP.lang) ? INIT_TITLE : (route.title ? `${route.title} · ${T(U.title)}` : T(U.title));
  $('#brandName').textContent = L === 'nl' ? 'Spottersgids' : "Spotter's Guide";
  $('#brandSub').textContent = T(U.brandSub);
  const link = ([id,k,ic]) => `<a href="#${id}"${route.nav===id?' aria-current="page"':''}>${ic ? svgI(ic, 'nico') : ''}${esc(T(U[k]))}</a>`;
  $('#nav').innerHTML = MENU.map(link).join('') + `<span class="lbl mlbl">${esc(T(U.navMore))}</span><div class="sub">${MENU2.map(([id,k]) => link([id,k])).join('')}`
    + `<a href="${VISIT_URL}">${esc(T(U.navVisit))}</a><a href="${esc(KOFI_URL)}" target="_blank" rel="noopener">${esc(T(U.navKofi))} ☕</a></div>`;
  $('#bnavIn').innerHTML = TABS.map(([id,k,ic]) => `<a href="#${id}" data-tab="${id}"${route.tab===id?' class="on" aria-current="page"':''}>${svgI(ic)}<span>${esc(T(U[k]))}</span></a>`).join('');
  $('#zoekT').textContent = T(U.srch); $('#zoekBtn').setAttribute('aria-label', T(U.srch)); $('#zoekL').textContent = T(U.srchL); $('#zoekIn').placeholder = T(U.srchPh);
  $('#langNl').setAttribute('aria-pressed', L==='nl'); $('#langEn').setAttribute('aria-pressed', L==='en');
  const nl = L === 'nl';
  $('#foot').innerHTML = `<div class="kofibar"><p><b>${esc(nl?'Vind je deze gids handig?':'Find this guide useful?')}</b> ${esc(nl?'Met een kleine bijdrage help je hem actueel te houden.':'A small contribution helps keep it up to date.')}</p>`
    + `<a class="kofi" href="${esc(KOFI_URL)}" target="_blank" rel="noopener">☕ <span>${esc(nl?'Steun de gids op Ko-fi':'Support the guide on Ko-fi')}</span></a></div><p>${esc(T(U.footMade))}</p>`;
  const h = $('.top').offsetHeight; if (h) document.documentElement.style.setProperty('--head', h + 'px');
}
// nog een keer op het scherm tikken waar je al bent: terug naar boven
$('#bnavIn').addEventListener('click', e => { const a = e.target.closest('a'); if (a && !SGP && location.hash === a.getAttribute('href')) { e.preventDefault(); window.scrollTo({top:0, behavior:'smooth'}); } });
$('#menuBtn').onclick = () => { closeZoek(); const o = $('#nav').classList.toggle('open'); $('#menuBtn').setAttribute('aria-expanded', o); };
document.addEventListener('click', e => { const n = $('#nav'); if (n.classList.contains('open') && !n.contains(e.target) && !e.target.closest('#menuBtn')) { n.classList.remove('open'); $('#menuBtn').setAttribute('aria-expanded', false); } });
/* kop per scherm */
const GLOBE = '<svg class="sk-e" viewBox="0 0 44 30" aria-hidden="true"><rect width="44" height="30" rx="3" fill="#F2C14E"/><g fill="none" stroke="#3B2414" stroke-width="1.7"><circle cx="22" cy="15" r="10.5"/><ellipse cx="22" cy="15" rx="4.6" ry="10.5"/><path d="M11.5 15h21M13.2 9.8h17.6M13.2 20.2h17.6"/></g></svg>';
const SEP = '<i> · </i>';
const cnt = (n, one, many) => `${n} ${esc(T(n === 1 ? U[one] : U[many]))}`;
const skHtml = (title, sub, meta) => `<header class="sk"><div class="wrap"><h1 class="sk-t">${GLOBE}<span class="sk-tt">${esc(title)}</span></h1>${sub ? `<p class="sk-s">${sub}</p>` : ''}<p class="sk-m">${meta || '&nbsp;'}</p></div></header>`;
function updatedHtml(){
  if (!/^\d{4}-\d\d-\d\d$/.test(UPDATED)) return '';
  return `${esc(T(U.updated))} ${esc(new Date(UPDATED + 'T12:00').toLocaleDateString(L === 'nl' ? 'nl-NL' : 'en-GB', {day:'numeric', month:'long', year:'numeric'}))}`;
}
// lange titels (bijv. Midden- en Zuid-Amerika) kleiner maken tot ze passen
function fitSk(){
  $$('.sk-t').forEach(t => { const tt = t.querySelector('.sk-tt'); if (!tt) return; t.style.removeProperty('--sk-fs'); let fs = 39, n = 0;
    while (tt.scrollWidth > tt.clientWidth + 1 && fs > 22 && n < 30) { fs--; n++; t.style.setProperty('--sk-fs', fs + 'px'); } });
}
if (document.fonts) { if (document.fonts.ready) document.fonts.ready.then(fitSk); if (document.fonts.addEventListener) document.fonts.addEventListener('loadingdone', fitSk); }
window.addEventListener('load', fitSk);
const fabHtml = href => `<a class="fab" href="${href}" aria-label="${esc(T(U.back2))}"><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg></a>`;
/* ---------- zoeken (zoals in de Bezoekersgids): katten en plekken ---------- */
const fold = x => String(x || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
const PIN = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/></svg>';
let ZRES = [], ZACT = -1;
function closeZoek(){ const p = $('#zoekpaneel'); if (!p) return; p.hidden = true; $('#zoekBtn').setAttribute('aria-expanded', false); $('#zoekRes').hidden = true; $('#zoekIn').setAttribute('aria-expanded', false); }
function zoek(){
  const inp = $('#zoekIn'), ul = $('#zoekRes'), q = fold(inp.value.trim());
  $('#zoekX').hidden = !inp.value; ZACT = -1;
  if (!q) { ul.hidden = true; inp.setAttribute('aria-expanded', false); ZRES = []; return; }
  const hit = (xs) => { let b = 9; xs.forEach(x => { const f = fold(x); if (!f) return; if (f.startsWith(q)) b = Math.min(b, 0); else if (f.split(/[\s(),·–-]+/).some(w => w.startsWith(q))) b = Math.min(b, 1); else if (f.includes(q)) b = Math.min(b, 2); }); return b; };
  const cats = CATS.map(c => ({c, r: hit([c.nl, c.en, c.la])})).filter(x => x.r < 9).sort((a,b) => a.r - b.r || catName(a.c).localeCompare(catName(b.c)));
  const spots = SPOTS.map(s => ({s, r: hit([s.name.nl, s.name.en, s.area.nl, s.area.en, s.country.nl, s.country.en])})).filter(x => x.r < 9).sort((a,b) => a.r - b.r || T(a.s.name).localeCompare(T(b.s.name)));
  ZRES = [...cats.slice(0, 8).map(x => ({t:'c', o:x.c})), ...spots.slice(0, 12).map(x => ({t:'s', o:x.s}))];
  ul.innerHTML = ZRES.length ? ZRES.map((x, i) => x.t === 'c'
    ? `<li><a href="${spHref(x.o.no)}" role="option" id="zr${i}">${img(x.o.photos[0], '', false, true).replace('<img ', '<img class="ik" ')}<span><b>${esc(catName(x.o))}</b><small class="lat">${esc(x.o.la)}</small></span></a></li>`
    : `<li><a href="#kaart" data-zspot="${esc(x.o.id)}" role="option" id="zr${i}"><span class="ik loc">${PIN}</span><span><b>${esc(T(x.o.name))}</b><small>${esc(T(x.o.country))} · ${esc(x.o.recs.map(r => catName(BY[r.no])).join(', '))}</small></span></a></li>`).join('')
    : `<li class="leeg">${esc(T(U.srchNone))}</li>`;
  ul.hidden = false; inp.setAttribute('aria-expanded', true);
}
function zoekAct(i){ const as = $$('#zoekRes a'); as.forEach(a => a.classList.remove('act')); ZACT = i; if (as[i]) { as[i].classList.add('act'); as[i].scrollIntoView({block:'nearest'}); $('#zoekIn').setAttribute('aria-activedescendant', as[i].id); } }
function goSpot(id){
  const s = SPOT[id]; if (!s) return;
  FILTER = 'all'; CAT = null; VIEW = null; LISTALL = false; BASEX = null; SHOWN.add(spotMax(s));
  if (SGP) { try { sessionStorage.setItem('sg-spot', id); } catch(e) {} location.href = '#kaart'; return; }
  TAB = 'kaart'; SEL = id;
  if (location.hash !== '#kaart') { try { history.pushState(null, '', '#kaart'); } catch(e) {} }
  route(false); selectSpot(id);
}
$('#zoekBtn').onclick = () => {
  const p = $('#zoekpaneel'), open = p.hidden;
  $('#nav').classList.remove('open'); $('#menuBtn').setAttribute('aria-expanded', false);
  p.hidden = !open; $('#zoekBtn').setAttribute('aria-expanded', open);
  if (open) { $('#zoekIn').focus(); zoek(); } else closeZoek();
};
$('#zoekIn').oninput = zoek;
$('#zoekIn').onkeydown = e => {
  const n = $$('#zoekRes a').length;
  if (e.key === 'ArrowDown' && n) { e.preventDefault(); zoekAct((ZACT + 1) % n); }
  else if (e.key === 'ArrowUp' && n) { e.preventDefault(); zoekAct((ZACT - 1 + n) % n); }
  else if (e.key === 'Enter' && n) { e.preventDefault(); $$('#zoekRes a')[Math.max(ZACT, 0)].click(); }
  else if (e.key === 'Escape') { closeZoek(); $('#zoekBtn').focus(); }
};
$('#zoekX').onclick = () => { $('#zoekIn').value = ''; zoek(); $('#zoekIn').focus(); };
$('#zoekRes').addEventListener('click', e => {
  const a = e.target.closest('a'); if (!a) return;
  if (a.dataset.zspot) { e.preventDefault(); const id = a.dataset.zspot; closeZoek(); goSpot(id); return; }
  closeZoek();
});
document.addEventListener('click', e => { const p = $('#zoekpaneel'); if (p && !p.hidden && !p.contains(e.target) && !e.target.closest('#zoekBtn')) closeZoek(); });
$('#nav').addEventListener('click', e => { if (e.target.closest('a')) { $('#nav').classList.remove('open'); $('#menuBtn').setAttribute('aria-expanded', false); } });
$$('.langsw [data-setlang]').forEach(b => b.onclick = () => { if (b.dataset.setlang === L) return; L = b.dataset.setlang; try { localStorage.setItem('sg-lang', L); } catch(e) {} if (SGP && !location.hash) { location.href = spHref(SGP.no); return; } route(true); });

/* ---------- startpagina ---------- */
function inFilter(cont){ return FILTER === 'all' || cont === FILTER; }
function topspotList(){
  const list = [];
  SPOTS.forEach(s => { if (!inFilter(s.cont)) return;
    const recs = s.recs.filter(r => r.top).sort((a,b) => b.score - a.score || a.no - b.no);
    if (recs.length) list.push({s, r:recs[0], recs}); });
  list.sort((a,b) => b.r.score - a.r.score || CONTS.indexOf(a.s.cont) - CONTS.indexOf(b.s.cont) || a.r.no - b.r.no);
  return list;
}
function catsInFilter(){ return CATS.filter(c => FILTER === 'all' || c.cont.includes(FILTER)); }
function topsHtml(){
  const list = topspotList();
  if (!list.length) return `<p class="empty">${esc(L==='nl'?'Geen topspots in dit werelddeel.':'No top spots on this continent.')}</p>`;
  const shown = SHOWALL ? list : list.slice(0, 6);
  return `<div class="tops">${shown.map(({s,r,recs}) => { const c = BY[r.no];
    return `<button type="button" class="tcard" data-spot="${esc(s.id)}" data-no="${r.no}">
      <div class="ph${s.photo ? ' spot' : ''}">${s.photo ? `${img(s.photo, T(s.name))}<span class="avs">${recs.slice(0, 3).map(x => `<span class="av">${img(BY[x.no].photos[0], catName(BY[x.no]), false, true)}</span>`).join('')}</span><span class="pcr">${s.photo.note ? `${esc(T(s.photo.note))} · ` : ''}${credit(s.photo.cr)}</span>` : img(c.photos[0], catName(c))}<span class="tag">${esc(contName(s.cont))}</span></div>
      <div class="bd"><span class="sp">${recs.map(x => esc(catName(BY[x.no]))).join(' · ')}</span><h3>${esc(T(s.name))}</h3><span class="where">${esc(T(s.country))}</span>
      ${scoreHtml(r.score)}<span class="ssn">${esc(T(r.season))}</span></div></button>`; }).join('')}</div>
    ${list.length > 6 ? `<div class="morewrap"><button type="button" class="btn" id="showAll">${esc(SHOWALL ? T(U.showLess) : `${T(U.showAll)} (${list.length})`)}</button></div>` : ''}
    <details class="box" style="margin-top:22px"><summary style="cursor:pointer;font-weight:700">${esc(T(U.scaleTitle))}</summary>
    <ul class="scale">${[5,4,3,2,1].map(n=>`<li>${scoreHtml(n)}<span>${esc(T(U.scale[n]))}</span></li>`).join('')}</ul></details>`;
}
function panelHtml(){
  const s = SEL && SPOT[SEL];
  if (!s) return `<p class="hint">${esc(T(U.mapHint))}</p>`;
  const recs = s.recs.slice().sort((a,b)=>b.score-a.score);
  // soorten met precies dezelfde uitleg (uit één topspot) samen tonen
  const groups = [];
  recs.forEach(r => { const g = groups.find(x => T(x[0].why) === T(r.why)); if (g) g.push(r); else groups.push([r]); });
  return `<h3>${esc(T(s.name))}</h3><p class="meta">${esc(placeLine(s))}</p>
    ${groups.map(g => `<div class="rec">${g.map(r => `<div class="sp">${esc(catName(BY[r.no]))} ${scoreHtml(r.score)}</div>`).join('')}
      <p>${esc(T(g[0].why))}</p>${factsHtml(g[0])}
      ${g.map(r => `<p>${PAGES[r.no] ? `<a class="btnlink" href="${spHref(r.no)}">${esc(catName(BY[r.no]))}: ${esc(T(U.toPage).toLowerCase())} →</a>` : `<span class="soon">${esc(catName(BY[r.no]))} · ${esc(T(U.soonPage))}</span>`}</p>`).join('')}</div>`).join('')}`;
}
// plekken van één kat binnen het gekozen werelddeel
const catSpots = no => SPOTS.filter(s => inFilter(s.cont) && s.recs.some(r => r.no === no));
// katten in de fotorij: met plek in dit werelddeel (kleur) en zonder plek maar wel levend hier (grijs)
function rowCats(){
  const lives = CATS.filter(c => FILTER === 'all' || c.cont.includes(FILTER) || catSpots(c.no).length);
  const withSpot = lives.filter(c => catSpots(c.no).length), grey = lives.filter(c => !catSpots(c.no).length);
  return {withSpot, grey, total: lives.length};
}
function catRowHtml(){
  const {withSpot, grey, total} = rowCats();
  const btn = (c, g) => `<button type="button" class="catbtn${g?' grey':''}" data-cat="${c.no}" aria-pressed="${CAT===c.no}"><span class="av">${img(c.photos[0], '', false, true)}</span>${esc(catName(c))}</button>`;
  const n = CAT ? catSpots(CAT).length : 0;
  return `<p class="slbl">${esc(T(U.pickCat))}</p><div class="catrow" id="catrow">
    <button type="button" class="catbtn" data-cat="" aria-pressed="${!CAT}"><span class="av all">${total}</span>${esc(T(U.allCats))}</button>
    ${withSpot.map(c => btn(c, false)).join('')}${grey.map(c => btn(c, true)).join('')}</div>
    ${CAT ? `<div class="catnote"><b>${esc(catName(BY[CAT]))}</b><span class="lat">${esc(BY[CAT].la)}</span>${n ? `<span class="note">${n} ${esc(n === 1 ? T(U.catShown1) : T(U.catShown))}</span>` : `<span class="soon">${esc(T(U.noSpot))}</span>`}${PAGES[CAT] ? `<a class="btnlink" href="${spHref(CAT)}">${esc(T(U.toPage))} →</a>` : (n ? `<span class="soon">${esc(T(U.soonPage))}</span>` : '')}</div>` : ''}`;
}
function mapTabHtml(){
  const ico = d => `<svg viewBox="0 0 20 20" aria-hidden="true"><path d="${d}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  return `${contChipsHtml()}${catRowHtml()}
    <div class="mapbox"><div class="mapstage"><div id="mapwrap"></div>
      <div class="zoombtns"><button type="button" id="zIn" aria-label="${esc(T(U.zoomIn))}" title="${esc(T(U.zoomIn))}">${ico('M10 4v12M4 10h12')}</button>
      <button type="button" id="zOut" aria-label="${esc(T(U.zoomOut))}" title="${esc(T(U.zoomOut))}">${ico('M4 10h12')}</button>
      <button type="button" id="zReset" aria-label="${esc(T(U.zoomReset))}" title="${esc(T(U.zoomReset))}">${ico('M3 7V3h4M17 7V3h-4M3 13v4h4M17 13v4h-4')}</button></div></div>
    <div id="maplegend"></div><div class="panel" id="panel" aria-live="polite">${panelHtml()}</div></div>
    <p class="note mapnote">${esc(T(U.mapSub))}</p>
    <div class="lcard"><div class="maplist" id="maplist"></div></div>`;
}
// keuzeknoppen voor het werelddeel (Kaart, Soorten en Topspots delen dezelfde keuze)
function contChipsHtml(){
  return `<p class="slbl">${esc(T(U.pickCont))}</p><div class="chips" role="group" aria-label="${esc(L==='nl'?'Filter per werelddeel':'Filter by continent')}">
    ${['all',...CONTS].map(c => `<button type="button" class="chip" data-f="${c}" aria-pressed="${FILTER===c}">${esc(c==='all'?T(U.all):contName(c))}</button>`).join('')}</div>`;
}
// alle plekken voor de startkaart (nog niet gefilterd op kans) plus het kader en het leefgebied
function homeData(){
  let all, box = BOX[FILTER], range = null;
  if (CAT) {   // één kat: alleen zijn plekken, kleur = kans voor die kat, met leefgebied
    all = catSpots(CAT).map(s => ({s, r:s.recs.find(r => r.no === CAT)})).map(({s,r}) => ({s, id:s.id, lat:s.lat, lon:s.lon, score:r.score, star:r.top, label:`${T(s.name)}, ${T(s.country)}`}));
    range = BY[CAT].range || null;
    let [x0,y0,x1,y1] = range ? bboxOfPath(range) : [720,284,0,0];
    all.forEach(m => { const [x,y] = proj(m.lat, m.lon); x0=Math.min(x0,x); x1=Math.max(x1,x); y0=Math.min(y0,y); y1=Math.max(y1,y); });
    box = FILTER === 'all' ? [x0-12, y0-12, Math.max(60, x1-x0+24), Math.max(36, y1-y0+24)] : BOX[FILTER];
  } else {
    all = SPOTS.filter(s => inFilter(s.cont)).map(s => ({s, id:s.id, lat:s.lat, lon:s.lon, score:spotMax(s), star:isTop(s), label:`${T(s.name)}, ${T(s.country)}`}));
  }
  return {all, box, range};
}
const worldMode = () => FILTER === 'all' && !CAT && !VIEW;
// wereldkaart op een telefoon: niet alles past, je ziet een venster dat je zijwaarts verschuift
const narrowWorld = () => FILTER === 'all' && !CAT && narrow();
let BASEX = null;   // linkerkant van dat venster (kaarteenheden); null = beginstand
// het kader zonder inzoomen
function baseVB(){
  const mw = $('#mapwrap');
  if (FILTER === 'all' && !CAT) {
    if (!narrow() || !mw) return [0,0,W,H];
    const w = Math.min(W, (mw.clientWidth || 360) * W / 960);
    const x = BASEX === null ? (W-w) * .55 : BASEX;
    return [Math.max(0, Math.min(W-w, x)), 0, w, H];
  }
  return fit(homeData().box, ratioFor(homeData().box));
}
const curVB = () => VIEW || baseVB();
function clampView(v){
  let [x,y,w,h] = v;
  x = w <= W ? Math.max(0, Math.min(W-w, x)) : (W-w)/2;
  y = h <= H ? Math.max(0, Math.min(H-h, y)) : (H-h)/2;
  return [x,y,w,h];
}
// nieuw kader; zo ver uitgezoomd als het basiskader = niet meer ingezoomd
function setView(v){
  const full = baseVB()[2];
  if (v[2] >= full - .5) { VIEW = null; if (narrowWorld()) BASEX = clampView([v[0], 0, full, H])[0]; }
  else VIEW = clampView(v);
}
const MINW = 20;   // verst ingezoomd: 10 lengtegraden breed
function zoomView(v, f, fx, fy){
  const [x,y,w,h] = v, full = baseVB()[2];
  const nw = Math.max(MINW, Math.min(full, w/f)), nh = nw * h / w;
  return [x + fx*w - fx*nw, y + fy*h - fy*nh, nw, nh];
}
function zoomBy(f, fx = .5, fy = .5){ setView(zoomView(curVB(), f, fx, fy)); LISTALL = false; drawHomeMap(); }
// tijdens een gebaar alleen het kader en de markerschaal bijwerken (snel, één keer per beeldje)
let FRAME = null, RAF = 0;
function liveView(v){
  FRAME = clampView(v);
  if (RAF) return;
  RAF = requestAnimationFrame(() => {
    RAF = 0;
    const svg = $('#mapwrap svg'); if (!svg || !FRAME) return;
    svg.setAttribute('viewBox', FRAME.join(' '));
    const u = FRAME[2] / (svg.clientWidth || 360);
    svg.querySelectorAll('.mk').forEach(g => g.setAttribute('transform', `translate(${g.dataset.x} ${g.dataset.y}) scale(${u})`));
  });
}
// na een gebaar: het kader vastleggen zonder de kaart opnieuw op te bouwen (geen sprongetje)
function commitView(){
  if (!FRAME) return;
  setView(FRAME); FRAME = null;
  if (RAF) { cancelAnimationFrame(RAF); RAF = 0; }
  const svg = $('#mapwrap svg');
  if (svg) {   // het vastgelegde kader meteen tonen (bij helemaal uitzoomen: terug naar het basiskader)
    const v = curVB(), u = v[2] / (svg.clientWidth || 360);
    svg.setAttribute('viewBox', v.join(' '));
    svg.querySelectorAll('.mk').forEach(g => g.setAttribute('transform', `translate(${g.dataset.x} ${g.dataset.y}) scale(${u})`));
    svg.classList.toggle('zoomed', !!VIEW); svg.classList.toggle('pan', !VIEW && narrowWorld());
  }
  $('#zOut').disabled = $('#zReset').disabled = !VIEW;
  $('#zIn').disabled = !!VIEW && VIEW[2] <= MINW + .5;
  LISTALL = false; drawMapList(LASTMARKERS);
}
let LASTMARKERS = [];
function drawHomeMap(){
  const mw = $('#mapwrap'); if (!mw) return;
  if (RAF) { cancelAnimationFrame(RAF); RAF = 0; } FRAME = null;
  mw.className = 'mapscroll';
  const cw = mw.clientWidth || 360;
  const {all, box, range} = homeData();
  const markers = all.filter(m => SHOWN.has(m.score)).map(m => ({...m, sel:SEL===m.id}));
  markers.sort((a,b) => (a.sel - b.sel) || (a.score - b.score));
  LASTMARKERS = markers;
  mw.innerHTML = mapSvg({box, world:FILTER === 'all' && !CAT, vb:curVB(), cw, markers, range, mr:5, cls:VIEW?'zoomed':(narrowWorld()?'pan':''), label:T(U.navMap)});
  bindMarkers(mw, id => { if (!DRAGGED) selectSpot(id); });
  bindGestures(mw);
  $('#zOut').disabled = $('#zReset').disabled = !VIEW;
  $('#zIn').disabled = !!VIEW && VIEW[2] <= MINW + .5;
  $('#maplegend').innerHTML = homeLegendHtml(all);
  $$('#maplegend [data-sc]').forEach(b => b.onclick = () => { const n = +b.dataset.sc; SHOWN.has(n) ? SHOWN.delete(n) : SHOWN.add(n); afterFilter(); });
  const lb = $('#lowBtn'); if (lb) lb.onclick = () => { const on = SHOWN.has(1) && SHOWN.has(2); [1,2].forEach(n => on ? SHOWN.delete(n) : SHOWN.add(n)); afterFilter(); };
  drawMapList(markers);
}
function afterFilter(){
  if (SEL && SPOT[SEL]) { const m = homeData().all.find(x => x.id === SEL); if (!m || !SHOWN.has(m.score)) { SEL = null; $('#panel').innerHTML = panelHtml(); } }
  LISTALL = false; drawHomeMap();
}
function selectSpot(id){ SEL = id; drawHomeMap(); const p = $('#panel'); p.innerHTML = panelHtml(); p.scrollIntoView({block:'nearest', behavior:'smooth'}); }
function homeLegendHtml(all){
  const low = all.filter(m => m.score <= 2 && !SHOWN.has(m.score)).length, lowOn = SHOWN.has(1) && SHOWN.has(2);
  return `<div class="maplegend"><span>${esc(T(U.legend))}</span>${[5,4,3,2,1].map(n => `<button type="button" class="lgbtn" data-sc="${n}" aria-pressed="${SHOWN.has(n)}" title="${esc(T(U.lgToggle).replace('{n}', n))}"><i style="--c:var(--s${n})"></i>${n}</button>`).join('')}
    <span style="color:var(--ink)">${STAR}<span style="color:var(--muted)">${esc(T(U.topStar))}</span></span>
    ${lowOn ? `<button type="button" class="lowbtn" id="lowBtn">${esc(T(U.hideLow))}</button>` : (low ? `<button type="button" class="lowbtn" id="lowBtn">${esc(T(U.showLow))} (${low})</button>` : '')}
    <p class="lgexp">${[5,4,3,2,1].map(n => `<b>${n}</b> ${esc(T(U.sc[n]))}`).join(' · ')}</p></div>`;
}
// lijst van de plekken die op de kaart staan (bij inzoomen: alleen wat in beeld is)
function drawMapList(markers){
  const el = $('#maplist'); if (!el) return;
  let list = markers;
  if (VIEW) { const [x,y,w,h] = VIEW; list = list.filter(m => { const [px,py] = proj(m.lat, m.lon); return px >= x && px <= x+w && py >= y && py <= y+h; }); }
  list = list.slice().sort((a,b) => b.score - a.score || b.star - a.star || T(a.s.name).localeCompare(T(b.s.name)));
  const shown = LISTALL ? list : list.slice(0, 10);
  const cats = m => CAT ? `${esc(catName(BY[CAT]))} · ${esc(T(U.chance).toLowerCase())} ${m.score}`
    : m.s.recs.slice().sort((a,b) => b.score - a.score).map(r => `${esc(catName(BY[r.no]))} ${esc(T(U.chance).toLowerCase())} ${r.score}`).join(' · ');
  el.innerHTML = `<h3>${esc(T(U.inView))}: ${cnt(list.length, 'wPlace1', 'wPlaces')}</h3><p class="lsub">${esc(T(U.listSub))}</p>
    ${list.length ? `<ol>${shown.map(m => `<li><button type="button" class="pl" data-id="${esc(m.id)}"${SEL===m.id?' aria-current="true"':''}>
      ${m.star ? `<span class="d st" style="--c:var(--s${m.score})">${STAR}</span>` : `<span class="d" style="--c:var(--s${m.score})"></span>`}
      <span><b>${esc(T(m.s.name))}</b><small>${esc(T(m.s.country))} · ${cats(m)}</small></span></button></li>`).join('')}</ol>` : `<p class="empty">${esc(T(U.listNone))}</p>`}
    ${list.length > 10 ? `<div class="morewrap"><button type="button" class="btn" id="listAll">${esc(LISTALL ? T(U.showLess) : `${T(U.listAll)} (${list.length})`)}</button></div>` : ''}`;
  el.querySelectorAll('.pl').forEach(b => b.onclick = () => selectSpot(b.dataset.id));
  const la = $('#listAll'); if (la) la.onclick = () => { LISTALL = !LISTALL; drawMapList(markers); if (!LISTALL) el.scrollIntoView({block:'nearest'}); };
}
// slepen (als ingezoomd), knijpen met twee vingers, ctrl+scroll / trackpad en dubbelklik
function bindGestures(mw){
  const svg = mw.querySelector('svg'); if (!svg) return;
  const pts = new Map(); let g = null, endT = null, glide = 0, vel = null;
  const frac = (cx, cy, r) => [(cx - r.left) / r.width, (cy - r.top) / r.height];
  const canPan = () => !!VIEW || narrowWorld();
  const stopGlide = () => { if (glide) { cancelAnimationFrame(glide); glide = 0; commitView(); } };
  const begin = () => {
    const r = svg.getBoundingClientRect(), vb = FRAME || curVB(), p = [...pts.values()];
    g = {r, vb:vb.slice(), p0:p.map(q => ({...q})), d0: p.length === 2 ? Math.hypot(p[0].x-p[1].x, p[0].y-p[1].y) : 0};
    vel = {x:0, y:0, t:performance.now(), px:p[0] ? p[0].x : 0, py:p[0] ? p[0].y : 0};
  };
  const move = e => {
    if (!pts.has(e.pointerId)) return;
    pts.set(e.pointerId, {x:e.clientX, y:e.clientY});
    if (!g) return;
    const p = [...pts.values()], {r, vb} = g, sx = vb[2] / r.width, sy = vb[3] / r.height;
    if (p.length >= 2 && g.d0) {
      const d = Math.hypot(p[0].x-p[1].x, p[0].y-p[1].y), m0 = [(g.p0[0].x+g.p0[1].x)/2, (g.p0[0].y+g.p0[1].y)/2], m = [(p[0].x+p[1].x)/2, (p[0].y+p[1].y)/2];
      const [fx,fy] = frac(m0[0], m0[1], r), ax = vb[0] + fx*vb[2], ay = vb[1] + fy*vb[3];
      const nv = zoomView(vb, d / g.d0, fx, fy), [gx,gy] = frac(m[0], m[1], r);
      nv[0] = ax - gx*nv[2]; nv[1] = ay - gy*nv[3];
      DRAGGED = true; vel = null; liveView(nv);
    } else if (p.length === 1 && canPan()) {
      const dx = p[0].x - g.p0[0].x, dy = p[0].y - g.p0[0].y;
      if (Math.hypot(dx, dy) > 5) DRAGGED = true;
      if (DRAGGED) {
        liveView([vb[0] - dx*sx, vb[1] - (VIEW ? dy*sy : 0), vb[2], vb[3]]);
        if (vel) { const t = performance.now(), dt = Math.max(1, t - vel.t), a = Math.min(1, dt / 50);
          vel.x = vel.x*(1-a) + (p[0].x - vel.px)/dt*a; vel.y = vel.y*(1-a) + (p[0].y - vel.py)/dt*a; vel.t = t; vel.px = p[0].x; vel.py = p[0].y; }
      }
    }
  };
  // uitloop na het loslaten: de kaart glijdt nog even door en remt af
  const startGlide = (r) => {
    let vx = vel.x, vy = VIEW ? vel.y : 0, last = performance.now();
    if (performance.now() - vel.t > 80 || Math.hypot(vx, vy) < .15) { commitView(); return; }
    const step = now => {
      const dt = Math.min(32, now - last); last = now;
      const f = Math.pow(.995, dt); vx *= f; vy *= f;
      const fr = FRAME || curVB(), sx = fr[2] / r.width, sy = fr[3] / r.height;
      liveView([fr[0] - vx*dt*sx, fr[1] - vy*dt*sy, fr[2], fr[3]]);
      if (Math.hypot(vx, vy) < .02) { glide = 0; commitView(); return; }
      glide = requestAnimationFrame(step);
    };
    glide = requestAnimationFrame(step);
  };
  const up = e => {
    if (!pts.delete(e.pointerId)) return;
    if (pts.size) { begin(); vel = null; return; }
    window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up); window.removeEventListener('pointercancel', up);
    const r = g && g.r; g = null;
    if (DRAGGED) {
      if (e.type === 'pointerup' && vel && r) startGlide(r); else commitView();
      setTimeout(() => { DRAGGED = false; }, 0);
    }
  };
  svg.addEventListener('pointerdown', e => {
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    stopGlide();
    if (!pts.size) { DRAGGED = false; window.addEventListener('pointermove', move); window.addEventListener('pointerup', up); window.addEventListener('pointercancel', up); }
    pts.set(e.pointerId, {x:e.clientX, y:e.clientY});
    if (canPan() && e.pointerType === 'mouse') e.preventDefault();
    begin();
  });
  svg.addEventListener('wheel', e => {
    if (!e.ctrlKey) return;            // gewoon scrollen blijft de pagina scrollen
    e.preventDefault(); stopGlide();
    const [fx,fy] = frac(e.clientX, e.clientY, svg.getBoundingClientRect());
    liveView(zoomView(FRAME || curVB(), Math.exp(-e.deltaY * .01), fx, fy));
    clearTimeout(endT); endT = setTimeout(commitView, 150);
  }, {passive:false});
  svg.addEventListener('dblclick', e => { const [fx,fy] = frac(e.clientX, e.clientY, svg.getBoundingClientRect()); zoomBy(2, fx, fy); });
}
// scherm Soorten: zoekveld en fotokaartjes in twee groepen (grote en kleine katten), zoals de Bezoekersgids
let GOPEN = {big:true, small:true};
const CHEVUP = '<svg class="chv" viewBox="0 0 20 20" aria-hidden="true"><path d="M5 12.5 10 7.5l5 5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>';
function speciesTabHtml(){
  return `${contChipsHtml()}<label class="zk"><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg>
    <input id="q" type="search" placeholder="${esc(T(U.search))}" value="${esc(Q)}" autocomplete="off" spellcheck="false" enterkeyhint="search" aria-label="${esc(T(U.search))}"></label><div id="splist">${speciesListHtml()}</div>`;
}
function speciesListHtml(){
  const q = fold(Q.trim());
  const cats = catsInFilter().filter(c => !q || [c.nl, c.en, c.la].some(x => fold(x).includes(q)));
  if (!cats.length) return `<p class="empty">${esc(T(U.noHits))}</p>`;
  const card = c => {
    const sp = catSpots(c.no), best = sp.length ? Math.max(...sp.map(s => s.recs.find(r => r.no === c.no).score)) : 0;
    const inner = `<div class="ph">${img(c.photos[0], catName(c))}</div><div class="bd"><span class="nm">${esc(catName(c))}</span><span class="cnt">${cnt(sp.length, 'wPlace1', 'wPlaces')}</span>
      <span class="ft">${best ? scoreHtml(best, false, true) : ''}</span></div>`;
    return PAGES[c.no] ? `<a class="scard" href="${spHref(c.no)}">${inner}</a>` : `<div class="scard">${inner}</div>`;
  };
  const grp = (key, list, lbl) => { if (!list.length) return ''; const open = q ? true : GOPEN[key];
    return `<div class="gt"><button type="button" data-g="${key}" aria-expanded="${open}">${esc(T(U[lbl]))}${CHEVUP}</button></div><div class="grid"${open ? '' : ' hidden'}>${list.map(card).join('')}</div>`; };
  const az = list => list.sort((a,b) => catName(a).localeCompare(catName(b), L));   // op naam, zoals de Bezoekersgids
  return grp('big', az(cats.filter(c => BIG.has(c.no))), 'grpBig') + grp('small', az(cats.filter(c => !BIG.has(c.no))), 'grpSmall');
}
function bindSpecies(){
  $$('.gt button').forEach(b => b.onclick = () => { const k = b.dataset.g; GOPEN[k] = b.getAttribute('aria-expanded') !== 'true'; $('#splist').innerHTML = speciesListHtml(); bindSpecies(); });
}
// scherm Meer: lijst met ronde iconen
const PIJL = '<svg class="pijl" viewBox="0 0 20 20" aria-hidden="true"><path d="M7.5 4.5 13 10l-5.5 5.5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
function meerHtml(){
  const row = (href, ic, label, ext) => `<li><a href="${esc(href)}"${ext ? ' target="_blank" rel="noopener"' : ''}><span class="mi">${svgI(ic)}</span><span class="mt">${esc(label)}</span>${PIJL}</a></li>`;
  return `<ul class="ml">${[...MENU, ...MENU2].map(([id,k,ic]) => row('#' + id, ic, T(U[k]))).join('')}${row(VISIT_URL, 'visit', T(U.navVisit))}${row(KOFI_URL, 'kofi', T(U.navKofi), true)}</ul>`;
}
// kop van het scherm: titel, onderregel en goudgele regel met aantallen (volgt het gekozen werelddeel)
function skForTab(){
  if (TAB === 'kaart') {
    const spots = SPOTS.filter(s => inFilter(s.cont)).length;
    return skHtml(FILTER === 'all' ? T(U.world) : contName(FILTER), esc(T(U.skMap)),
      [cnt(catsInFilter().length, 'wSpecies1', 'wSpecies'), cnt(spots, 'wPlace1', 'wPlaces'), cnt(topspotList().length, 'wTop1', 'wTops')].join(SEP));
  }
  if (TAB === 'soorten') {
    const cs = catsInFilter(), b = cs.filter(c => BIG.has(c.no)).length;
    return skHtml(T(U.navSpecies), esc(T(U.skSpecies)), [cnt(cs.length, 'wSpecies1', 'wSpecies'), `${b} ${esc(T(U.wBig))}`, `${cs.length - b} ${esc(T(U.wSmall))}`].join(SEP));
  }
  if (TAB === 'topspots') {
    const l = topspotList(), sp = new Set(); l.forEach(x => x.recs.forEach(r => sp.add(r.no)));
    return skHtml(T(U.navTop), esc(T(U.skTop)), [cnt(l.length, 'wTop1', 'wTops'), cnt(sp.size, 'wSpecies1', 'wSpecies')].join(SEP));
  }
  return skHtml(T(U.navMoreT), esc(T(U.skMore)), updatedHtml());
}
function tabBody(){
  if (TAB === 'kaart') return mapTabHtml();
  if (TAB === 'soorten') return speciesTabHtml();
  if (TAB === 'meer') return meerHtml();
  return `${contChipsHtml()}<p class="note" style="margin:2px 0 14px">${esc(T(U.topSub))}</p><div id="tops">${topsHtml()}</div>`;
}
function renderHome(){
  $('#main').innerHTML = `${skForTab()}<section class="sec screen"><div class="wrap" id="tabbody">${tabBody()}</div></section>`;
  bindHome(); fitSk();
}
function refreshHome(){ renderHome(); }
function bindHome(){
  $$('.chip[data-f]').forEach(b => b.onclick = () => {
    FILTER = b.dataset.f; CAT = null; VIEW = null; LISTALL = false; BASEX = null; try { localStorage.setItem('sg-cont', FILTER); } catch(e) {}
    if (SEL && SPOT[SEL] && !inFilter(SPOT[SEL].cont)) SEL = null;
    const x = b.parentNode.scrollLeft; refreshHome(); const ch = $('.chips'); if (ch) ch.scrollLeft = x;
  });
  $$('.tcard').forEach(b => b.onclick = () => {
    const no = +b.dataset.no;
    if (PAGES[no]) { const h = spHref(no); if (h[0] === '#') location.hash = h; else location.href = h; return; }
    SEL = b.dataset.spot; TAB = 'kaart'; try { history.replaceState(null, '', '#kaart'); } catch(e) {}
    refreshHome(); renderChrome({tab:'kaart'}); const mb = $('.mapbox'); if (mb) mb.scrollIntoView({block:'start'});
  });
  bindSpecies();
  $$('.catbtn').forEach(b => b.onclick = () => {
    CAT = b.dataset.cat ? +b.dataset.cat : null; VIEW = null; LISTALL = false;
    // kat met alleen plekken met kans 1–2 (bijv. caracal): die plekken dan meteen tonen
    if (CAT) { const sc = catSpots(CAT).map(s => s.recs.find(r => r.no === CAT).score); if (sc.length && sc.every(n => !SHOWN.has(n))) sc.forEach(n => SHOWN.add(n)); }
    if (SEL && CAT && !SPOT[SEL].recs.some(r => r.no === CAT)) SEL = null;
    const x = $('#catrow').scrollLeft; refreshHome(); const cr = $('#catrow'); if (cr) cr.scrollLeft = x;
  });
  const sa = $('#showAll'); if (sa) sa.onclick = () => { SHOWALL = !SHOWALL; $('#tops').innerHTML = topsHtml(); bindHome(); };
  const q = $('#q'); if (q) q.oninput = () => { Q = q.value; $('#splist').innerHTML = speciesListHtml(); bindSpecies(); };
  const zi = $('#zIn'); if (zi) { zi.onclick = () => zoomBy(2); $('#zOut').onclick = () => zoomBy(.5); $('#zReset').onclick = () => { VIEW = null; LISTALL = false; drawHomeMap(); }; }
  drawHomeMap();
}
let rsz; window.addEventListener('resize', () => { clearTimeout(rsz); rsz = setTimeout(() => { if ($('#mapwrap')) drawHomeMap(); if ($('#spmap')) drawSpeciesMap(); }, 200); });

/* ---------- soortpagina ---------- */
// eerste deel van de seizoenstekst (tot de eerste ; of haakje), voor samenvattingen
const spotsMoreLbl = (n, all) => all ? T(U.showLess) : (L === 'nl' ? `Toon alle ${n} plekken` : `Show all ${n} places`);
const showAllSpots = () => { const ol = $('#spotlist'), b = $('#moreSpots'); if (!ol || ol.classList.contains('all')) return; ol.classList.add('all'); if (b) b.textContent = spotsMoreLbl(0, true); };
const shortSeason = r => T(r.season).split(/;\s*|\s\(/)[0].replace(/[.,]\s*$/, '');
let SPMAP = null;
function drawSpeciesMap(){
  const el = $('#spmap'); if (!el || !SPMAP) return;
  el.innerHTML = mapSvg({...SPMAP, cw: el.clientWidth || 360, borders: true});
  bindMarkers(el, id => { const d = document.getElementById('plek-' + id); if (d) { showAllSpots(); d.open = true; d.scrollIntoView({block:'start', behavior:'smooth'}); } });
}
function renderSpecies(no){
  const c = BY[no], P = PAGES[no];
  if (!c || !P) return renderMissing(c);
  const recs = P.spots.map(id => { const s = SPOT[id]; return {s, r:s.recs.find(r => r.no === no)}; });
  const local = {}; P.sources.forEach((g,i) => local[g] = i+1);
  const cite = ids => (ids||[]).filter(g => local[g]).sort((a,b) => local[a] - local[b]).map(g => `<a class="cite" href="#bron-${no}-${local[g]}">[${local[g]}]</a>`).join('');
  const top = recs[0], best = top.r.score;
  let [x0,y0,x1,y1] = c.range ? bboxOfPath(c.range) : [720,284,0,0];
  recs.forEach(({s}) => { const [x,y] = proj(s.lat, s.lon); x0=Math.min(x0,x); x1=Math.max(x1,x); y0=Math.min(y0,y); y1=Math.max(y1,y); });
  const pad = 12;
  SPMAP = {box:[x0-pad, y0-pad, Math.max(50, x1-x0+2*pad), Math.max(30, y1-y0+2*pad)], range:c.range,
    markers: recs.map(({s,r},i) => ({id:s.id, lat:s.lat, lon:s.lon, score:r.score, num:i+1, label:`${i+1}. ${T(s.name)}`})).reverse(),
    label: T(U.habitat)+': '+catName(c)};
  const intro = T(P.intro), km = intro.match(/(Kans|Chance):\s*\d.*$/s);
  const story = km ? intro.slice(0, km.index).trim() : intro;
  const season1 = shortSeason(top.r);
  const meta = [cnt(recs.length, 'wPlace1', 'wPlaces'), esc(`${T(U.bestChance)} ${best}`), esc(T(BIG.has(no) ? U.bigCats : U.smallCats))].join(SEP);
  $('#main').innerHTML = `${skHtml(catName(c), `<i>${esc(c.la)}</i>`, meta)}${fabHtml('#soorten')}
  <div class="wrap">
  <section class="sphead">
    <div class="heros"><div class="hstrip" id="hstrip">${c.photos.map((p,i) => `<figure class="hero"><div class="ph">${img(p, catName(c), i === 0)}</div><figcaption>${credit(p.cr)}${p.captive ? ` · ${esc(T(U.captive))}` : ''}</figcaption></figure>`).join('')}</div>
      ${c.photos.length > 1 ? `<div class="hdots">${c.photos.map((_,i) => `<button type="button" data-i="${i}" aria-label="${esc(T(U.photos))} ${i+1}"${i ? '' : ' class="on"'}></button>`).join('')}</div>` : ''}</div>
    <div class="idblock">
      <span class="lbl">№ ${c.no} · ${c.cont.map(contName).join(' · ')}</span>
      <p class="en">${esc(L==='nl'?c.en:c.nl)}</p>
      <div class="badges">${iucnHtml(c.iucn)}</div>
      <dl class="summary">
        <div><dt>${esc(T(U.bestPlace))}</dt><dd>${esc(T(top.s.name))}<small>${esc(T(top.s.country))}</small></dd></div>
        <div><dt>${esc(T(U.bestTime))}</dt><dd>${esc(season1)}</dd></div>
      </dl>
      <p class="lead">${esc(story)}${km ? `<span class="kans">${esc(km[0])}</span>` : ''}</p>
    </div>
  </section></div>
  <nav class="jump" aria-label="${esc(L==='nl'?'Snel naar':'Jump to')}"><div class="wrap">
    ${[['kaartsec','jMap'],['plekken','jPlaces'],['tipssec','jTips'],['statussec','jStatus'],['bronnen','jSources']].map(([id,k]) => `<button type="button" data-go="${id}">${esc(T(U[k]))}</button>`).join('')}
  </div></nav>
  <div class="wrap">
  <section class="sec anchor" id="kaartsec"><div class="sechead"><h2>${esc(T(U.habitat))}</h2></div>
    <div class="mapbox">${alsoHtml(no, recs)}<div id="spmap"></div>${legendHtml(false)}<div class="panel"><p class="note">${esc(T(U.habitatNote))}</p></div></div></section>
  <section class="sec anchor" id="plekken"><div class="sechead"><h2>${esc(T(U.bestSpots))}</h2><p>${esc(T(U.bestSpotsSub))}</p></div>
    <ol class="spots" id="spotlist">${recs.map(({s,r},i) => `<li${i >= 3 ? ' class="more"' : ''}><details class="spot" id="plek-${esc(s.id)}" style="--c:var(--s${r.score})">
      <summary><span class="rank">${i+1}</span><span class="tt"><h3>${esc(T(s.name))}</h3><span class="where">${esc(T(s.country))}</span>${shortSeason(r) ? `<span class="ssn"><svg viewBox="0 0 20 20" aria-hidden="true">${FICO.season}</svg>${esc(shortSeason(r))}</span>` : ''}</span><span class="sc-sum">${scoreHtml(r.score, false, true)}</span>${CHEV}</summary>
      <div class="body"><p class="where">${esc(T(s.area))}</p>${scoreHtml(r.score)}
      <p class="why">${esc(T(r.why))}${cite(r.src)}</p>${factsHtml(r)}</div></details></li>`).join('')}</ol>
    ${recs.length > 3 ? `<div class="morewrap"><button type="button" class="btn" id="moreSpots">${esc(spotsMoreLbl(recs.length, false))}</button></div>` : ''}</section>
  <section class="sec two">
    <div class="anchor" id="tipssec"><details class="fold"><summary><h2>${esc(T(U.tips))} <span class="cnt">(${T(P.tips).length})</span></h2>${CHEV}</summary><ul class="tips">${T(P.tips).map(x=>`<li>${esc(x)}</li>`).join('')}</ul></details></div>
    <div class="anchor" id="statussec"><details class="fold"><summary><h2>${esc(T(U.status))}</h2>${iucnHtml(c.iucn)}${CHEV}</summary><div class="box" style="display:grid;gap:12px">
      <p>${esc(T(P.status))}${cite(P.statusSrc)}</p>
      <h3>${esc(T(U.threats))}</h3><ul class="tips">${T(P.threats).map(x=>`<li>${esc(x)}</li>`).join('')}</ul></div></details></div>
  </section>
  <section class="sec read anchor" id="bronnen"><details class="fold" id="srcbox"><summary><h2>${esc(T(U.sources))} <span class="cnt">(${P.sources.length})</span></h2>${CHEV}</summary>
    <ol class="sources">${P.sources.map((g,i) => `<li id="bron-${no}-${i+1}"><a href="${esc(SRC[g].url)}" target="_blank" rel="noopener">${esc(T(SRC[g].title))}</a></li>`).join('')}</ol></details>
    <p class="note" style="margin-top:14px">${esc(L==='nl'?'Foto’s, leefgebied en IUCN-status: De KATalogue.':'Photos, range and IUCN status: De KATalogue.')}</p>
    <p style="margin-top:14px">${esc(L==='nl'?'Zelf deze kat gezien, of klopt er iets niet?':'Seen this cat yourself, or is something wrong?')} <a class="btnlink" href="#melden-${no}">${esc(L==='nl'?'Meld het hier':'Report it here')} →</a></p></section>
  </div>`;
  drawSpeciesMap(); bindAlso(no, recs);
  $$('.jump button').forEach(b => b.onclick = () => { const el = document.getElementById(b.dataset.go); if (!el) return; const f = el.querySelector('.fold'); if (f) f.open = true; el.scrollIntoView({block:'start', behavior:'smooth'}); });
  bindJumpSpy();
  const mb = $('#moreSpots'); if (mb) mb.onclick = () => { const ol = $('#spotlist'); if (ol.classList.contains('all')) { ol.classList.remove('all'); mb.textContent = spotsMoreLbl(recs.length, false); $('#plekken').scrollIntoView({block:'start'}); } else showAllSpots(); };
  const hs = $('#hstrip'), dots = $$('.hdots button');
  if (hs && dots.length) {
    dots.forEach(d => d.onclick = () => hs.scrollTo({left: +d.dataset.i * (hs.clientWidth + 10), behavior:'smooth'}));
    hs.addEventListener('scroll', () => { const i = Math.round(hs.scrollLeft / (hs.clientWidth + 10)); dots.forEach((d,j) => d.classList.toggle('on', i === j)); }, {passive:true});
  }
  $$('.cite').forEach(a => a.onclick = e => { e.preventDefault(); const el = document.getElementById(a.getAttribute('href').slice(1)); if (el) { $('#srcbox').open = true; el.scrollIntoView({block:'center', behavior:'smooth'}); el.style.background='color-mix(in srgb,var(--accent) 18%,transparent)'; setTimeout(()=>el.style.background='',1600); } });
  return catName(c);
}
// snelmenu: knop van het onderdeel waar je nu bent oplichten (en in beeld schuiven)
let JUMPSPY = null;
function bindJumpSpy(){
  if (JUMPSPY) window.removeEventListener('scroll', JUMPSPY);
  const btns = $$('.jump button'); if (!btns.length) { JUMPSPY = null; return; }
  let cur = null;
  JUMPSPY = () => {
    const bar = $('.jump'); if (!bar || !bar.isConnected) return;
    const lim = Math.max(bar.getBoundingClientRect().bottom + 40, innerHeight * .4);
    let act = null;
    btns.forEach(b => { const el = document.getElementById(b.dataset.go); if (el && el.getBoundingClientRect().top <= lim) act = b; });
    if (innerHeight + scrollY >= document.documentElement.scrollHeight - 4) act = btns[btns.length - 1];   // onderaan: laatste onderdeel
    if (act === cur) return; cur = act;
    btns.forEach(b => b.classList.toggle('on', b === act));
    if (act) { const w = act.parentNode; w.scrollTo({left: act.offsetLeft - (w.clientWidth - act.offsetWidth) / 2, behavior:'smooth'}); }
  };
  window.addEventListener('scroll', JUMPSPY, {passive:true}); JUMPSPY();
}
// andere katten die op dezelfde plekken voorkomen
function alsoCats(no, recs){
  const set = {};
  recs.forEach(({s}) => s.recs.forEach(r => { if (r.no !== no) set[r.no] = true; }));
  return Object.keys(set).map(Number).sort((a,b) => a - b);
}
function alsoHtml(no, recs){
  const list = alsoCats(no, recs); if (!list.length) return '';
  return `<div class="also"><label for="alsoSel">${esc(T(U.alsoLbl))}</label><select id="alsoSel"><option value="">${esc(T(U.alsoNone))}</option>${list.map(n => `<option value="${n}"${ALSO===n?' selected':''}>${esc(catName(BY[n]))}</option>`).join('')}</select><div id="alsoOut" style="flex-basis:100%"></div></div>`;
}
function bindAlso(no, recs){
  const sel = $('#alsoSel'); if (!sel) return;
  const base = SPMAP.markers.map(m => ({...m}));
  const apply = () => {
    const a = sel.value ? +sel.value : null; ALSO = a;
    if (!a) { SPMAP.markers = base; $('#alsoOut').innerHTML = ''; drawSpeciesMap(); return; }
    SPMAP.markers = base.map(m => { const r = SPOT[m.id].recs.find(x => x.no === a); return r ? {...m, score:r.score} : {...m, dim:true}; });
    const shared = recs.map(({s}) => ({s, r:s.recs.find(x => x.no === a)})).filter(x => x.r);
    $('#alsoOut').innerHTML = `<p class="note" style="margin-top:6px">${esc(catName(BY[a]))} ${esc(T(U.alsoAt))}</p><ul class="alsolist">${shared.map(({s,r}) => `<li><b>${esc(T(s.name))}</b>${scoreHtml(r.score, false, true)}</li>`).join('')}</ul>
      <p style="margin-top:8px">${PAGES[a] ? `<a class="btnlink" href="${spHref(a)}">${esc(catName(BY[a]))}: ${esc(T(U.toPage).toLowerCase())} →</a>` : `<span class="soon">${esc(T(U.soonPage))}</span>`}</p>`;
    drawSpeciesMap();
  };
  sel.onchange = apply; if (ALSO && alsoCats(no, recs).includes(ALSO)) apply(); else ALSO = null;
}
function renderMissing(c){
  $('#main').innerHTML = `${skHtml(c ? catName(c) : '404', '', '')}<div class="wrap sec read"><p style="margin-top:12px">${esc(c ? T(U.soonPage) + '.' : T(U.notFound))}</p><p style="margin-top:16px"><a class="btnlink" href="#soorten">← ${esc(T(U.back))}</a></p></div>`;
  return c ? catName(c) : '';
}

/* ---------- tekstpagina's ---------- */
function renderText(id){
  const pg = D.text[id];
  let html = `${skHtml(T(pg.title), esc(T(pg.eyebrow)), updatedHtml())}${fabHtml('#meer')}<div class="wrap sec" style="padding-top:12px"><div class="read prose">${T(pg.html)}`;
  if (id === 'europa') html += europaList();
  if (id === 'over') html += `<p><a class="kofi" href="${esc(KOFI_URL)}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 6h13a4 4 0 0 1 0 8h-1.1A6 6 0 0 1 10 19H9a5 5 0 0 1-5-5V6zm12 2v4h1a2 2 0 0 0 0-4h-1z"/></svg>${esc(L==='nl'?'Trakteer me op een koffie (Ko-fi)':'Buy me a coffee (Ko-fi)')}</a></p>`;
  if (id === 'over') html += `<p><a class="btnlink" href="#melden">${esc(L==='nl'?'Stuur me een melding':'Send me a report')} →</a></p>`;
  if (pg.sources && pg.sources.length) html += `<h2>${esc(T(U.sources))}</h2><ol class="sources">${pg.sources.map(g => `<li><a href="${esc(SRC[g].url)}" target="_blank" rel="noopener">${esc(T(SRC[g].title))}</a></li>`).join('')}</ol>`;
  html += `</div></div>`;
  $('#main').innerHTML = html;
  return T(pg.title);
}
function europaList(){
  return `<div class="eurlist">${D.europe.map(e => { const c = BY[e.no], page = PAGES[e.no];
    const inner = `${img(c.photos[0], catName(c), false, true)}<div><span class="lbl">${esc(T(e.where))}</span><b style="font-family:var(--display);font-size:1.15rem">${esc(catName(c))}</b><span class="lat">${esc(c.la)}</span>${BEST[e.no]?scoreHtml(BEST[e.no]):''}<span>${esc(T(e.text))}</span></div>`;
    return page ? `<a class="eurrow" href="${spHref(e.no)}">${inner}</a>` : `<div class="eurrow">${inner}</div>`; }).join('')}</div>`;
}

/* ---------- melden (Web3Forms, gaat naar de maker; zelfde sleutel als de dierentuingids) ---------- */
const W3F_KEY = '9494e3c0-9342-4457-a5d6-b795793b9ce4';
const RP_TYPES = [['seen',{nl:'Ik heb een kat gezien',en:'I saw a cat'}],['missing',{nl:'Er ontbreekt een plek',en:'A place is missing'}],
  ['wrong',{nl:'Informatie klopt niet of is verouderd',en:'Information is wrong or out of date'}],['other',{nl:'Iets anders',en:'Something else'}]];
function renderReport(no){
  const nl = L === 'nl', cats = D.cats.slice().sort((a,b) => catName(a).localeCompare(catName(b)));
  const today = new Date().toISOString().slice(0,10);
  $('#main').innerHTML = `${skHtml(T(U.navReport), esc(T(U.meerReport)), esc(T(U.reportSub)))}${fabHtml('#meer')}<div class="wrap sec" style="padding-top:12px"><div class="read prose">
    <p>${esc(nl?'Zelf een wilde kat gezien, een goede plek die hier ontbreekt, of iets dat niet (meer) klopt? Laat het weten. Zo blijft de gids eerlijk en actueel.':'Seen a wild cat yourself, know a good place that is missing, or found something that is wrong or out of date? Let me know. That keeps the guide honest and up to date.')}</p></div>
    <form class="rp-form" id="rp-form" onsubmit="return false">
      <fieldset><legend>${esc(nl?'Wat wil je melden?':'What would you like to report?')}</legend><div class="rp-types">
        ${RP_TYPES.map(([v,l]) => `<label><input type="radio" name="rp-type" value="${v}"><span>${esc(T(l))}</span></label>`).join('')}</div></fieldset>
      <div><label class="rp-l" for="rp-cat">${esc(nl?'Soort':'Species')}</label>
        <select id="rp-cat"><option value="0">${esc(nl?'Weet ik niet / geen':'Not sure / none')}</option>${cats.map(c => `<option value="${c.no}"${c.no===no?' selected':''}>${esc(catName(c))}</option>`).join('')}</select></div>
      <div><label class="rp-l" for="rp-spot">${esc(nl?'Plek':'Place')}</label><select id="rp-spot"></select>
        <input type="text" id="rp-spot2" maxlength="120" placeholder="${esc(nl?'Naam van de plek, gebied en land':'Name of the place, area and country')}" hidden></div>
      <div><label class="rp-l" for="rp-date">${esc(nl?'Datum (van je waarneming of bezoek)':'Date (of your sighting or visit)')}</label><input type="date" id="rp-date" value="${today}" max="${today}"></div>
      <div><label class="rp-l" for="rp-opm">${esc(nl?'Opmerkingen':'Comments')} <span style="font-weight:400;color:var(--muted)">(${esc(nl?'optioneel':'optional')})</span></label>
        <textarea id="rp-opm" maxlength="500" placeholder="${esc(nl?'Bijvoorbeeld: tijdens een nachtrit, langs de bosrand, ongeveer 30 meter afstand':'For example: on a night drive, along the forest edge, about 30 metres away')}"></textarea><span class="rp-cnt" id="rp-cnt">0 / 500</span></div>
      <div class="rp-hp" aria-hidden="true"><input type="text" id="rp-bot" tabindex="-1" autocomplete="off"></div>
      <div><span class="rp-l">${esc(nl?'Je melding':'Your report')}</span><p class="rp-sum leeg" id="rp-sum"></p></div>
      <button type="button" class="rp-go" id="rp-go" disabled>${esc(nl?'Plaats melding':'Submit report')}</button>
      <p class="rp-msg" id="rp-msg" aria-live="polite"></p>
    </form>
    <p class="note" style="margin-top:14px;max-width:640px">${esc(nl?'Je melding gaat rechtstreeks naar de maker van de gids en is niet openbaar. Wil je een reactie, zet dan je e-mailadres bij Opmerkingen.':'Your report goes straight to the guide’s author and is not public. If you would like a reply, add your email address under Comments.')}</p></div>`;
  const fillSpots = () => {
    const c = +$('#rp-cat').value, P = c && PAGES[c];
    const opts = P ? P.spots.map(id => `<option value="${esc(id)}">${esc(T(SPOT[id].name))}, ${esc(T(SPOT[id].country))}</option>`).join('') : '';
    $('#rp-spot').innerHTML = opts + `<option value="_">${esc(nl?'Andere plek…':'Another place…')}</option>`;
  };
  fillSpots();
  $('#rp-cat').onchange = () => { fillSpots(); rpUpdate(); };
  $('#rp-form').addEventListener('input', rpUpdate); $('#rp-form').addEventListener('change', rpUpdate);
  $('#rp-go').onclick = rpSend;
  rpUpdate();
  return T(U.navReport);
}
function rpData(){
  const t = (document.querySelector('input[name="rp-type"]:checked') || {}).value || '';
  const c = +$('#rp-cat').value, sp = $('#rp-spot').value, other = sp === '_';
  $('#rp-spot2').hidden = !other;
  const place = other ? $('#rp-spot2').value.trim() : (SPOT[sp] ? T(SPOT[sp].name) + ', ' + T(SPOT[sp].country) : '');
  const placeNl = other ? place : (SPOT[sp] ? SPOT[sp].name.nl + ', ' + SPOT[sp].country.nl : '');
  return {t, c, place, placeNl, date: $('#rp-date').value, opm: $('#rp-opm').value.trim()};
}
function rpUpdate(){
  const d = rpData(), nl = L === 'nl', el = $('#rp-sum');
  $('#rp-cnt').textContent = $('#rp-opm').value.length + ' / 500';
  const type = RP_TYPES.find(([v]) => v === d.t), cat = d.c ? catName(BY[d.c]) : (nl ? 'onbekende soort' : 'unknown species');
  const ok = !!type && (d.t !== 'seen' || !!d.c) && (d.t === 'other' || !!d.place);
  if (!type) { el.className = 'rp-sum leeg'; el.textContent = nl ? 'Kies hierboven wat je wilt melden en waar.' : 'Choose above what you want to report and where.'; }
  else {
    const dt = d.date ? new Date(d.date + 'T12:00').toLocaleDateString(nl ? 'nl-NL' : 'en-GB', {day:'numeric', month:'short', year:'numeric'}) : '';
    el.className = 'rp-sum';
    el.textContent = `${T(type[1])}: ${cat}${d.place ? (nl ? ' bij ' : ' at ') + d.place : ''}${dt ? (nl ? ', op ' : ', on ') + dt : ''}.` +
      (!ok ? (nl ? (d.t === 'seen' && !d.c ? ' Kies nog een soort.' : ' Kies of vul nog een plek in.') : (d.t === 'seen' && !d.c ? ' Please choose a species.' : ' Please choose or enter a place.')) : '');
  }
  $('#rp-go').disabled = !ok;
}
function rpMsg(t, cls){ const m = $('#rp-msg'); m.textContent = t; m.className = 'rp-msg' + (cls ? ' ' + cls : ''); }
async function rpSend(){
  const d = rpData(), nl = L === 'nl', btn = $('#rp-go');
  if ($('#rp-bot').value) return;
  const type = RP_TYPES.find(([v]) => v === d.t), catNl = d.c ? BY[d.c].nl : 'onbekend';
  btn.disabled = true; rpMsg(nl ? 'Bezig met versturen…' : 'Sending…');
  const body = {access_key: W3F_KEY, subject: `Melding Spottersgids: ${type[1].nl} – ${catNl}${d.placeNl ? ' – ' + d.placeNl : ''}`, from_name: 'Spottersgids voor wilde katten',
    Melding: $('#rp-sum').textContent.trim(), Soort_melding: type[1].nl, Soort: catNl, Plek: d.placeNl || '-', Datum: d.date || '-', Opmerkingen: d.opm || '-',
    Gids: 'Spottersgids', Pagina: location.href, Taal: L, botcheck: ''};
  try {
    const r = await fetch('https://api.web3forms.com/submit', {method:'POST', headers:{'Content-Type':'application/json', 'Accept':'application/json'}, body: JSON.stringify(body)});
    const j = await r.json().catch(() => ({}));
    if (!(r.ok && j.success)) throw new Error(j.message || r.status);
    rpMsg(nl ? 'Bedankt! Je melding is verstuurd.' : 'Thank you! Your report has been sent.', 'ok');
    $('#rp-opm').value = ''; document.querySelectorAll('input[name="rp-type"]').forEach(x => x.checked = false); rpUpdate();
  } catch(e) {
    rpMsg(nl ? 'Versturen is niet gelukt. Probeer het later opnieuw.' : 'Sending failed. Please try again later.', 'fout');
    btn.disabled = false;
  }
}

/* ---------- router ---------- */
function route(keep){
  const h = (location.hash || (SGP ? '#soort-' + SGP.no : '#start')).slice(1);
  let title = '', nav = '', page = 0, tab = '';
  const y = window.scrollY;
  if (h === 'start' || h === '' || h === 'topspots' || h === 'kaart' || h === 'soorten' || h === 'meer') {
    if (h !== 'start' && h !== '') TAB = h;
    tab = TAB; renderHome();
  }
  else if (/^soort-\d+$/.test(h)) { tab = 'soorten'; page = +h.slice(6); title = renderSpecies(page); }
  else if (/^melden(-\d+)?$/.test(h)) { tab = 'meer'; nav = 'melden'; title = renderReport(+(h.split('-')[1] || 0)); }
  else if (D.text[h]) { tab = 'meer'; nav = h; title = renderText(h); }
  else { title = renderMissing(null); }
  renderChrome({title, nav, page, tab});
  fitSk();
  window.scrollTo(0, keep ? y : 0);
  if (keep) { drawHomeMap(); drawSpeciesMap(); }
}
window.addEventListener('hashchange', () => route(false));
// testpagina: <base> wijst naar de map spottersgids, dus #-links zelf binnen deze pagina houden
if (window.SG_TEST) document.addEventListener('click', e => {
  const a = e.target.closest && e.target.closest('a[href^="#"]'); if (!a || e.defaultPrevented) return;
  e.preventDefault(); location.hash = a.getAttribute('href');
});
window.addEventListener('resize', () => { clearTimeout(window.__fitT); window.__fitT = setTimeout(fitSk, 150); });
route(false);
try { const zs = sessionStorage.getItem('sg-spot'); if (zs && !SGP) { sessionStorage.removeItem('sg-spot'); if (SPOT[zs]) goSpot(zs); } } catch(e) {}
})();

(function(){var f=document.querySelector('footer.foot,footer.hs-foot');if(!f||f.querySelector('.jg-lp'))return;var d=document.createElement('div');d.className='jg-lp';d.setAttribute('aria-hidden','true');d.innerHTML="<svg viewBox='0 0 240 132' xmlns='http://www.w3.org/2000/svg'><defs><linearGradient id='jglp-v' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#E2A843'/><stop offset='.62' stop-color='#E6AE4C'/><stop offset='1' stop-color='#F6DDA6'/></linearGradient><clipPath id='jglp-c'><path d='M64 96 C62 70 86 56 120 52 C150 48 182 50 200 62 C212 70 216 84 214 96 Z'/></clipPath></defs><ellipse cx='136' cy='97' rx='86' ry='3.2' fill='#000' opacity='.13'/><g class='jg-staart'><path d='M200 78 C214 82 222 90 222 102 C222 112 214 116 216 124 C217 129 222 130 226 127' fill='none' stroke='#3B2414' stroke-width='11' stroke-linecap='round'/><path d='M200 78 C214 82 222 90 222 102 C222 112 214 116 216 124 C217 129 222 130 226 127' fill='none' stroke='#E6AE4C' stroke-width='7' stroke-linecap='round'/><ellipse cx='214' cy='86' rx='3.2' ry='1.6' transform='rotate(30 214 86)' fill='#2E1C0F'/><ellipse cx='220' cy='96' rx='3.2' ry='1.6' transform='rotate(80 220 96)' fill='#2E1C0F'/><ellipse cx='221' cy='106' rx='3.2' ry='1.6' transform='rotate(95 221 106)' fill='#2E1C0F'/><ellipse cx='217' cy='116' rx='3.2' ry='1.6' transform='rotate(70 217 116)' fill='#2E1C0F'/><path d='M217 122 C218 127 221 128 224 126' stroke='#2E1C0F' stroke-width='5' fill='none' stroke-linecap='round'/></g><path d='M64 96 C62 70 86 56 120 52 C150 48 182 50 200 62 C212 70 216 84 214 96 Z' fill='url(#jglp-v)' stroke='#3B2414' stroke-width='2' stroke-linejoin='round' stroke-linecap='round'/><g clip-path='url(#jglp-c)'><ellipse cx='100.0' cy='66.0' rx='5.1' ry='4.0' transform='rotate(10 100.0 66.0)' fill='#C98E34'/><path d='M105.5 68.3 A6.2 5.0 0 0 1 98.2 70.8' stroke='#2E1C0F' stroke-width='2.5' stroke-linecap='round' fill='none'/><path d='M95.1 69.1 A6.3 5.0 0 0 1 94.8 63.1' stroke='#2E1C0F' stroke-width='2.4' stroke-linecap='round' fill='none'/><path d='M99.4 60.8 A6.5 5.2 0 0 1 105.7 63.5' stroke='#2E1C0F' stroke-width='2.2' stroke-linecap='round' fill='none'/><ellipse cx='122.0' cy='61.0' rx='4.7' ry='3.7' transform='rotate(40 122.0 61.0)' fill='#C98E34'/><path d='M125.3 64.6 A5.6 4.5 0 0 1 118.9 64.7' stroke='#2E1C0F' stroke-width='1.8' stroke-linecap='round' fill='none'/><path d='M116.1 61.2 A5.9 4.7 0 0 1 120.5 56.5' stroke='#2E1C0F' stroke-width='1.9' stroke-linecap='round' fill='none'/><path d='M124.3 56.7 A5.9 4.7 0 0 1 127.9 61.1' stroke='#2E1C0F' stroke-width='2.4' stroke-linecap='round' fill='none'/><ellipse cx='145.0' cy='60.0' rx='5.1' ry='4.0' transform='rotate(-10 145.0 60.0)' fill='#C98E34'/><path d='M151.1 59.6 A6.2 4.9 0 0 1 145.2 64.9' stroke='#2E1C0F' stroke-width='2.9' stroke-linecap='round' fill='none'/><path d='M141.1 63.8 A6.2 5.0 0 0 1 139.7 57.4' stroke='#2E1C0F' stroke-width='1.9' stroke-linecap='round' fill='none'/><path d='M142.3 55.1 A6.6 5.3 0 0 1 149.1 55.8' stroke='#2E1C0F' stroke-width='2.9' stroke-linecap='round' fill='none'/><ellipse cx='168.0' cy='62.0' rx='4.7' ry='3.7' transform='rotate(25 168.0 62.0)' fill='#C98E34'/><path d='M172.9 65.3 A6.4 5.1 0 0 1 163.8 65.9' stroke='#2E1C0F' stroke-width='2.2' stroke-linecap='round' fill='none'/><path d='M162.0 63.8 A6.4 5.1 0 0 1 164.4 57.8' stroke='#2E1C0F' stroke-width='2.2' stroke-linecap='round' fill='none'/><path d='M169.0 57.1 A6.2 5.0 0 0 1 174.1 62.8' stroke='#2E1C0F' stroke-width='2.3' stroke-linecap='round' fill='none'/><ellipse cx='112.0' cy='79.0' rx='4.3' ry='3.4' transform='rotate(60 112.0 79.0)' fill='#C98E34'/><path d='M113.9 83.1 A5.5 4.4 0 0 1 107.4 81.4' stroke='#2E1C0F' stroke-width='1.8' stroke-linecap='round' fill='none'/><path d='M106.7 78.7 A5.3 4.3 0 0 1 112.2 74.8' stroke='#2E1C0F' stroke-width='2.6' stroke-linecap='round' fill='none'/><path d='M115.1 75.5 A5.4 4.3 0 0 1 116.5 81.4' stroke='#2E1C0F' stroke-width='2.4' stroke-linecap='round' fill='none'/><ellipse cx='134.0' cy='76.0' rx='4.7' ry='3.7' transform='rotate(5 134.0 76.0)' fill='#C98E34'/><path d='M140.0 77.2 A6.2 4.9 0 0 1 135.8 80.7' stroke='#2E1C0F' stroke-width='2.7' stroke-linecap='round' fill='none'/><path d='M131.8 80.7 A6.3 5.1 0 0 1 128.1 77.9' stroke='#2E1C0F' stroke-width='2.6' stroke-linecap='round' fill='none'/><path d='M128.5 74.9 A5.7 4.5 0 0 1 133.3 71.5' stroke='#2E1C0F' stroke-width='2.1' stroke-linecap='round' fill='none'/><path d='M136.3 71.9 A5.6 4.5 0 0 1 139.4 74.7' stroke='#2E1C0F' stroke-width='2.0' stroke-linecap='round' fill='none'/><ellipse cx='156.0' cy='77.0' rx='4.3' ry='3.4' transform='rotate(35 156.0 77.0)' fill='#C98E34'/><path d='M159.1 80.4 A5.3 4.2 0 0 1 155.1 81.2' stroke='#2E1C0F' stroke-width='1.8' stroke-linecap='round' fill='none'/><path d='M151.6 79.9 A5.7 4.6 0 0 1 150.4 76.2' stroke='#2E1C0F' stroke-width='2.0' stroke-linecap='round' fill='none'/><path d='M152.5 73.3 A5.8 4.6 0 0 1 157.6 72.6' stroke='#2E1C0F' stroke-width='2.3' stroke-linecap='round' fill='none'/><path d='M160.1 73.9 A5.7 4.5 0 0 1 161.6 77.6' stroke='#2E1C0F' stroke-width='1.8' stroke-linecap='round' fill='none'/><ellipse cx='92.0' cy='82.0' rx='3.5' ry='2.8' transform='rotate(15 92.0 82.0)' fill='#C98E34'/><path d='M95.4 84.0 A4.2 3.3 0 0 1 90.4 85.1' stroke='#2E1C0F' stroke-width='2.0' stroke-linecap='round' fill='none'/><path d='M88.3 84.4 A4.8 3.8 0 0 1 88.7 79.2' stroke='#2E1C0F' stroke-width='1.8' stroke-linecap='round' fill='none'/><path d='M91.3 78.6 A4.3 3.5 0 0 1 96.3 81.5' stroke='#2E1C0F' stroke-width='1.8' stroke-linecap='round' fill='none'/><ellipse cx='126.0' cy='90.0' rx='3.0' ry='2.4' transform='rotate(50 126.0 90.0)' fill='#C98E34'/><path d='M127.8 92.5 A3.6 2.9 0 0 1 122.9 91.5' stroke='#2E1C0F' stroke-width='1.8' stroke-linecap='round' fill='none'/><path d='M122.2 90.2 A3.8 3.0 0 0 1 125.0 87.1' stroke='#2E1C0F' stroke-width='1.8' stroke-linecap='round' fill='none'/><path d='M127.6 87.3 A3.7 3.0 0 0 1 129.4 91.2' stroke='#2E1C0F' stroke-width='1.8' stroke-linecap='round' fill='none'/><ellipse cx='148.0' cy='90.0' rx='2.8' ry='2.2' transform='rotate(20 148.0 90.0)' fill='#C98E34'/><path d='M150.8 91.6 A3.4 2.7 0 0 1 146.2 92.3' stroke='#2E1C0F' stroke-width='1.8' stroke-linecap='round' fill='none'/><path d='M144.8 91.5 A3.7 2.9 0 0 1 145.9 87.6' stroke='#2E1C0F' stroke-width='1.8' stroke-linecap='round' fill='none'/><path d='M148.7 87.1 A3.7 3.0 0 0 1 151.6 89.4' stroke='#2E1C0F' stroke-width='1.8' stroke-linecap='round' fill='none'/><ellipse cx='188.0' cy='70.0' rx='3.9' ry='3.1' transform='rotate(10 188.0 70.0)' fill='#C98E34'/><path d='M192.5 70.9 A4.6 3.7 0 0 1 189.2 73.6' stroke='#2E1C0F' stroke-width='1.9' stroke-linecap='round' fill='none'/><path d='M186.0 73.9 A5.2 4.2 0 0 1 182.8 70.6' stroke='#2E1C0F' stroke-width='1.8' stroke-linecap='round' fill='none'/><path d='M183.1 68.3 A5.4 4.3 0 0 1 187.8 65.7' stroke='#2E1C0F' stroke-width='2.1' stroke-linecap='round' fill='none'/><path d='M189.6 66.5 A4.7 3.8 0 0 1 192.6 69.1' stroke='#2E1C0F' stroke-width='1.8' stroke-linecap='round' fill='none'/><circle cx='110' cy='56' r='1.6' fill='#2E1C0F'/><circle cx='135' cy='54' r='1.6' fill='#2E1C0F'/><circle cx='158' cy='54' r='1.5' fill='#2E1C0F'/><circle cx='84' cy='70' r='1.6' fill='#2E1C0F'/></g><path d='M168 96 C164 80 172 66 188 66 C204 66 212 80 210 96' fill='url(#jglp-v)' stroke='#3B2414' stroke-width='2' stroke-linejoin='round' stroke-linecap='round'/><ellipse cx='190.0' cy='78.0' rx='3.9' ry='3.1' transform='rotate(20 190.0 78.0)' fill='#C98E34'/><path d='M194.1 80.0 A4.8 3.8 0 0 1 188.3 81.6' stroke='#2E1C0F' stroke-width='1.8' stroke-linecap='round' fill='none'/><path d='M185.9 80.3 A5.0 4.0 0 0 1 186.6 75.1' stroke='#2E1C0F' stroke-width='2.1' stroke-linecap='round' fill='none'/><path d='M189.6 74.2 A4.8 3.8 0 0 1 194.7 77.3' stroke='#2E1C0F' stroke-width='2.1' stroke-linecap='round' fill='none'/><circle cx='178' cy='86' r='1.6' fill='#2E1C0F'/><circle cx='200' cy='88' r='1.5' fill='#2E1C0F'/><circle cx='196' cy='72' r='1.4' fill='#2E1C0F'/><path d='M150 96 C150 89 158 87 170 88 C178 89 180 93 180 96' fill='#F6DDA6' stroke='#3B2414' stroke-width='2' stroke-linejoin='round' stroke-linecap='round'/><path d='M160 92 L160 96 M166 91 L166 96 M172 91 L172 96' stroke='#3B2414' stroke-width='1.4' stroke-linecap='round'/><path d='M52 76 L52 112 C52 121 71 121 71 112 L71 76' fill='#E6AE4C' stroke='#3B2414' stroke-width='2' stroke-linejoin='round' stroke-linecap='round'/><path d='M54 106 C58 110 65 110 69 106 L69 113 C69 119 54 119 54 113 Z' fill='#F6DDA6'/><path d='M58.5 114 L58.5 119 M64.5 114 L64.5 119' stroke='#3B2414' stroke-width='1.4' stroke-linecap='round'/><circle cx='58' cy='90' r='1.7' fill='#2E1C0F'/><circle cx='65' cy='96' r='1.6' fill='#2E1C0F'/><circle cx='60' cy='101' r='1.4' fill='#2E1C0F'/><circle cx='66' cy='86' r='1.4' fill='#2E1C0F'/><path d='M78 76 L78 112 C78 121 97 121 97 112 L97 76' fill='#E6AE4C' stroke='#3B2414' stroke-width='2' stroke-linejoin='round' stroke-linecap='round'/><path d='M80 106 C84 110 91 110 95 106 L95 113 C95 119 80 119 80 113 Z' fill='#F6DDA6'/><path d='M84.5 114 L84.5 119 M90.5 114 L90.5 119' stroke='#3B2414' stroke-width='1.4' stroke-linecap='round'/><circle cx='84' cy='90' r='1.7' fill='#2E1C0F'/><circle cx='91' cy='96' r='1.6' fill='#2E1C0F'/><circle cx='86' cy='101' r='1.4' fill='#2E1C0F'/><circle cx='92' cy='86' r='1.4' fill='#2E1C0F'/><g class='jg-kop'><g class='jg-oor-l'><path d='M58 34 C62 18 48 10 40 16 C34 22 34 34 37 46 Z' fill='#2E1C0F' stroke='#3B2414' stroke-width='2' stroke-linejoin='round' stroke-linecap='round'/><path d='M55 32 C57 22 48 16 43 20 C39 24 38 32 40 40 Z' fill='#FBF1DC'/></g><g class='jg-oor-r'><path d='M82 34 C78 18 92 10 100 16 C106 22 106 34 103 46 Z' fill='#2E1C0F' stroke='#3B2414' stroke-width='2' stroke-linejoin='round' stroke-linecap='round'/><path d='M85 32 C83 22 92 16 97 20 C101 24 102 32 100 40 Z' fill='#FBF1DC'/></g><path d='M70 22 C92 22 106 36 106 54 C106 66 100 74 92 80 C86 85 78 88 70 88 C62 88 54 85 48 80 C40 74 34 66 34 54 C34 36 48 22 70 22 Z' fill='#E6AE4C' stroke='#3B2414' stroke-width='2' stroke-linejoin='round' stroke-linecap='round'/><circle cx='62' cy='31' r='1.7' fill='#2E1C0F'/><circle cx='70' cy='29' r='1.8' fill='#2E1C0F'/><circle cx='78' cy='31' r='1.7' fill='#2E1C0F'/><circle cx='66' cy='37' r='1.5' fill='#2E1C0F'/><circle cx='74' cy='37' r='1.5' fill='#2E1C0F'/><circle cx='42' cy='54' r='1.7' fill='#2E1C0F'/><circle cx='98' cy='54' r='1.7' fill='#2E1C0F'/><circle cx='45' cy='64' r='1.5' fill='#2E1C0F'/><circle cx='95' cy='64' r='1.5' fill='#2E1C0F'/><path d='M70 60 C78 60 86 64 86 70 C86 76 79 79 70 79 C61 79 54 76 54 70 C54 64 62 60 70 60 Z' fill='#FBF1DC'/><g class='jg-oog'><circle cx='56' cy='48' r='6.8' fill='#C9D94A' stroke='#3B2414' stroke-width='1.8'/><circle cx='56' cy='48.4' r='3.8' fill='#3B2414'/><circle cx='58.1' cy='46' r='1.6' fill='#fff'/><circle cx='54.4' cy='50.5' r='.8' fill='#fff'/><path d='M49.6 45.7 L46.4 44.5' stroke='#3B2414' stroke-width='1.5' stroke-linecap='round'/><path d='M51.4 42.9 L49.2 40.4' stroke='#3B2414' stroke-width='1.5' stroke-linecap='round'/><path d='M54.4 41.4 L53.5 38.1' stroke='#3B2414' stroke-width='1.5' stroke-linecap='round'/></g><g class='jg-oog'><circle cx='84' cy='48' r='6.8' fill='#C9D94A' stroke='#3B2414' stroke-width='1.8'/><circle cx='84' cy='48.4' r='3.8' fill='#3B2414'/><circle cx='86.1' cy='46' r='1.6' fill='#fff'/><circle cx='82.4' cy='50.5' r='.8' fill='#fff'/><path d='M90.4 45.7 L93.6 44.5' stroke='#3B2414' stroke-width='1.5' stroke-linecap='round'/><path d='M88.6 42.9 L90.8 40.4' stroke='#3B2414' stroke-width='1.5' stroke-linecap='round'/><path d='M85.6 41.4 L86.5 38.1' stroke='#3B2414' stroke-width='1.5' stroke-linecap='round'/></g><path d='M62 52 C64 56 65 59 66 62 M78 52 C76 56 75 59 74 62' stroke='#2E1C0F' stroke-width='1.6' fill='none' stroke-linecap='round'/><path d='M64 63 L76 63 C76 67 72 70 70 70 C68 70 64 67 64 63 Z' fill='#B5603A' stroke='#3B2414' stroke-width='1.6'/><path d='M70 70 L70 73 C68 76 64 76 62 74 M70 73 C72 76 76 76 78 74' stroke='#3B2414' stroke-width='1.6' fill='none' stroke-linecap='round'/><g stroke='#3B2414' stroke-width='1' stroke-linecap='round' fill='none' opacity='.85'><path d='M57 69 C46 66 36 66 26 68'/><path d='M57 72 C46 72 36 73 27 76'/><path d='M58 75 C48 77 40 80 32 85'/><path d='M83 69 C94 66 104 66 114 68'/><path d='M83 72 C94 72 104 73 113 76'/><path d='M82 75 C92 77 100 80 108 85'/></g></g></svg>";f.insertBefore(d,f.firstChild);d.addEventListener('click',function(){d.classList.remove('jg-tik');void d.offsetWidth;d.classList.add('jg-tik');setTimeout(function(){d.classList.remove('jg-tik')},1400)})})();
(function(){
var f=document.querySelector('footer.hs-foot,footer.foot');if(!f||f.querySelector('.jg-takbg'))return;f.classList.add('jg-tak');
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
})();
/* Taalmenu: maakt van elke rij taalknoppen (.langsw met [data-setlang]-knoppen) één knop met een wereldbol en de
   huidige taalcode ("🌐 NL"). Tikken opent een lijst met de talen in hun eigen naam. De lijst bevat alleen de talen
   van de knoppen die de pagina zelf heeft, dus op een landpagina alleen de talen van dat land.
   De bestaande knoppen blijven dezelfde [data-setlang]-knoppen; de taalwissel zelf doet de pagina zoals altijd.
   Wordt door bron/bouw.py in de startpagina en in elke gids gezet. */
(function(){
if(window.__TAALMENU)return;window.__TAALMENU=1;
var NAMEN={nl:"Nederlands",en:"English",fr:"Français",de:"Deutsch",it:"Italiano",es:"Español",pt:"Português"};
var css=".langsw.lm{display:inline-block;border:0;border-radius:0;overflow:visible;flex:none}"+
".lm .lm-btn{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;gap:5px;font-family:\"Bricolage Grotesque\",system-ui,sans-serif;font-size:13px;font-weight:600;line-height:1.3;color:#2A1C12;border:1.5px solid #2A1C12;border-radius:999px;padding:3px 10px;white-space:nowrap;background:transparent}"+
".lm .lm-btn:hover,.lm .lm-btn[aria-expanded=\"true\"]{background:#2A1C12;color:#EAD9B3}"+
".lm .lm-btn:focus-visible{outline:2px solid #B97A12;outline-offset:2px}"+
".lm .lm-glb{font-size:15px;line-height:1}"+
".lm .lm-pop{position:absolute;right:0;top:calc(100% + 6px);z-index:50;min-width:150px;margin:0;padding:6px;list-style:none;background:#FBF7EE;border:1.5px solid #2A1C12;border-radius:12px;box-shadow:0 6px 18px rgba(42,28,18,.18);display:flex;flex-direction:column;gap:2px}"+
".lm .lm-pop[hidden]{display:none}"+
".lm .lm-pop button{all:unset;box-sizing:border-box;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:12px;width:100%;padding:7px 10px;border-radius:8px;font-family:\"Bricolage Grotesque\",system-ui,sans-serif;font-size:15px;font-weight:600;line-height:1.3;color:#2A1C12;background:transparent}"+
".lm .lm-pop button:hover,.lm .lm-pop button:focus-visible{background:#F2DFB6}"+
".lm .lm-pop button[aria-pressed=\"true\"]{background:#2A1C12;color:#EAD9B3}"+
".lm .lm-pop button[aria-pressed=\"true\"]::after{content:\"\\2713\"}"+
".lm .lm-pop button .lm-c{font-size:12px;opacity:.6;font-weight:600}";
function stijl(){if(document.getElementById("lm-css"))return;var s=document.createElement("style");s.id="lm-css";s.textContent=css;(document.head||document.documentElement).appendChild(s);}
function huidig(){var l=(document.documentElement.lang||"nl").slice(0,2).toLowerCase();return NAMEN[l]?l:"nl";}
function label(){var l=huidig();document.querySelectorAll(".lm .lm-cur").forEach(function(e){e.textContent=l.toUpperCase();});
  document.querySelectorAll(".lm .lm-pop [data-setlang]").forEach(function(b){b.setAttribute("aria-pressed",String(b.dataset.setlang===l));});}
function maak(g){
  if(g.classList.contains("lm"))return;
  var knoppen=[].slice.call(g.querySelectorAll("[data-setlang]"));if(!knoppen.length)return;
  g.classList.add("lm");g.removeAttribute("role");
  var naam=g.getAttribute("aria-label")||"Taal / Language";
  var btn=document.createElement("button");btn.type="button";btn.className="lm-btn";btn.setAttribute("aria-haspopup","true");btn.setAttribute("aria-expanded","false");
  btn.setAttribute("aria-label",naam);
  btn.innerHTML='<span class="lm-glb" aria-hidden="true">\uD83C\uDF10</span><span class="lm-cur"></span>';
  var pop=document.createElement("div");pop.className="lm-pop";pop.hidden=true;pop.setAttribute("role","group");pop.setAttribute("aria-label",naam);
  knoppen.forEach(function(b){var c=b.dataset.setlang;b.textContent=NAMEN[c]||c.toUpperCase();b.setAttribute("lang",c);pop.appendChild(b);});
  g.textContent="";g.appendChild(btn);g.appendChild(pop);
  /* de lijst hangt onder de knop: de groep moet een referentiepunt zijn (de gids zet hem soms zelf absoluut) */
  if(getComputedStyle(g).position==="static")g.style.position="relative";
  label();
}
function alles(r){(r||document).querySelectorAll(".langsw:not(.lm)").forEach(maak);}
function dicht(behalve){document.querySelectorAll(".lm .lm-pop").forEach(function(p){if(p===behalve)return;p.hidden=true;var b=p.parentNode.querySelector(".lm-btn");if(b)b.setAttribute("aria-expanded","false");});}
document.addEventListener("click",function(e){
  var b=e.target.closest&&e.target.closest(".lm .lm-btn");
  if(b){e.preventDefault();var p=b.parentNode.querySelector(".lm-pop");var open=p.hidden;dicht(p);p.hidden=!open;b.setAttribute("aria-expanded",String(open));
    if(open){var a=p.querySelector('[aria-pressed="true"]')||p.querySelector("button");if(a)a.focus();}return;}
  if(e.target.closest&&e.target.closest(".lm [data-setlang]")){setTimeout(function(){dicht();label();},0);return;}
  if(!(e.target.closest&&e.target.closest(".lm")))dicht();
});
document.addEventListener("keydown",function(e){if(e.key==="Escape"){var o=document.querySelector(".lm .lm-pop:not([hidden])");if(o){dicht();var b=o.parentNode.querySelector(".lm-btn");if(b)b.focus();}}});
function start(){stijl();alles();
  new MutationObserver(function(ms){var nieuw=false;ms.forEach(function(m){m.addedNodes.forEach(function(n){if(n.nodeType===1&&(n.matches(".langsw:not(.lm)")||n.querySelector(".langsw:not(.lm)")))nieuw=true;});});if(nieuw)alles();})
    .observe(document.body,{childList:true,subtree:true});
  new MutationObserver(label).observe(document.documentElement,{attributes:true,attributeFilter:["lang"]});}
if(document.body)start();else document.addEventListener("DOMContentLoaded",start);
})();
