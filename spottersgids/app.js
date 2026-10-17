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
const spHref = no => (L === 'en' ? 'en/' : '') + D.slugs[L][no] + '/';
const T = o => o == null ? '' : (typeof o === 'string' ? o : (o[L] != null ? o[L] : o.nl));

/* ---------- vaste teksten ---------- */
const U = {
  title:{nl:'Spottersgids voor wilde katten',en:"Wild Cat Spotter's Guide"},
  brandSub:{nl:'wilde katten · J. Gelens',en:'wild cats · J. Gelens'},
  navSpecies:{nl:'Soorten',en:'Species'}, navTop:{nl:'Topspots',en:'Top spots'}, navMap:{nl:'Kaart',en:'Map'},
  navResp:{nl:'Verantwoord spotten',en:'Responsible spotting'}, navEur:{nl:'Katten in Europa',en:'Cats in Europe'},
  navPack:{nl:'Paklijst',en:'Packing list'}, navAbout:{nl:'Over mij',en:'About me'}, navReport:{nl:'Melden',en:'Report'}, navMore:{nl:'Meer',en:'More'},
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
  photos:{nl:"Foto's",en:'Photos'},
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
  notFound:{nl:'Deze pagina bestaat niet (meer).',en:'This page does not exist.'}
};
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

/* ---------- navigatie ---------- */
const NAV = [['soorten','navSpecies'],['topspots','navTop'],['europa','navEur']];
const MORE = [['verantwoord','navResp'],['paklijst','navPack'],['melden','navReport'],['over','navAbout']];
function renderChrome(route){
  document.documentElement.lang = L;
  document.title = (SGP && route.page === SGP.no && L === SGP.lang) ? INIT_TITLE : (route.title ? `${route.title} · ${T(U.title)}` : T(U.title));
  $('#brandName').textContent = L === 'nl' ? 'Spottersgids' : "Spotter's Guide";
  $('#brandSub').textContent = T(U.brandSub);
  const link = ([id,k]) => `<a href="#${id}"${route.nav===id?' aria-current="page"':''}>${esc(T(U[k]))}</a>`;
  const inMore = MORE.some(([id]) => id === route.nav);
  $('#nav').innerHTML = NAV.map(link).join('') +
    `<div class="more" id="more"><button type="button" class="morebtn${inMore?' cur':''}" id="moreBtn" aria-expanded="false" aria-haspopup="true">${esc(T(U.navMore))}<svg viewBox="0 0 10 10"><path d="M1.5 3.5 5 7l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
     <div class="moremenu"><span class="lbl mlbl">${esc(T(U.navMore))}</span>${MORE.map(link).join('')}</div></div>`;
  $('#moreBtn').onclick = e => { e.stopPropagation(); const o = $('#more').classList.toggle('open'); $('#moreBtn').setAttribute('aria-expanded', o); };
  $('#langNl').setAttribute('aria-pressed', L==='nl'); $('#langEn').setAttribute('aria-pressed', L==='en');
  $('#foot').innerHTML = `<p style="max-width:36rem">${esc(T(U.footMade))}</p><nav>${[...NAV, ...MORE].map(([id,k])=>`<a href="#${id}">${esc(T(U[k]))}</a>`).join('')}<a href="${esc(KOFI_URL)}" target="_blank" rel="noopener">${esc(L==='nl'?'Steun via Ko-fi ☕':'Support on Ko-fi ☕')}</a></nav>`;
  const h = $('.top').offsetHeight; if (h) document.documentElement.style.setProperty('--head', h + 'px');
}
document.addEventListener('click', e => { const m = $('#more'); if (m && !m.contains(e.target)) { m.classList.remove('open'); } });
$('#menuBtn').onclick = () => { const o = $('#nav').classList.toggle('open'); $('#menuBtn').setAttribute('aria-expanded', o); };
$('#nav').addEventListener('click', e => { if (e.target.closest('a')) { $('#nav').classList.remove('open'); $('#menuBtn').setAttribute('aria-expanded', false); } });
$$('.lang button').forEach(b => b.onclick = () => { if (b.dataset.l === L) return; L = b.dataset.l; try { localStorage.setItem('sg-lang', L); } catch(e) {} if (SGP && !location.hash) { location.href = spHref(SGP.no); return; } route(true); });

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
function tabCount(t){
  if (t === 'topspots') return topspotList().length;
  if (t === 'kaart') return homeData().all.filter(m => SHOWN.has(m.score)).length;
  return catsInFilter().length;
}
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
  return `<p class="lbl" style="margin-bottom:6px">${esc(T(U.catMap))}</p><div class="catrow" id="catrow">
    <button type="button" class="catbtn" data-cat="" aria-pressed="${!CAT}"><span class="av" style="background:var(--olive)">${total}</span>${esc(T(U.allCats))}</button>
    ${withSpot.map(c => btn(c, false)).join('')}${grey.map(c => btn(c, true)).join('')}</div>
    ${CAT ? `<div class="catnote"><b>${esc(catName(BY[CAT]))}</b><span class="lat">${esc(BY[CAT].la)}</span>${n ? `<span class="note">${n} ${esc(n === 1 ? T(U.catShown1) : T(U.catShown))}</span>` : `<span class="soon">${esc(T(U.noSpot))}</span>`}${PAGES[CAT] ? `<a class="btnlink" href="${spHref(CAT)}">${esc(T(U.toPage))} →</a>` : (n ? `<span class="soon">${esc(T(U.soonPage))}</span>` : '')}</div>` : ''}`;
}
function mapTabHtml(){
  const ico = d => `<svg viewBox="0 0 20 20" aria-hidden="true"><path d="${d}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  return `${catRowHtml()}<p class="note" style="margin-bottom:12px">${esc(T(U.mapSub))}</p>
    <div class="mapbox"><div class="mapstage"><div id="mapwrap"></div>
      <div class="zoombtns"><button type="button" id="zIn" aria-label="${esc(T(U.zoomIn))}" title="${esc(T(U.zoomIn))}">${ico('M10 4v12M4 10h12')}</button>
      <button type="button" id="zOut" aria-label="${esc(T(U.zoomOut))}" title="${esc(T(U.zoomOut))}">${ico('M4 10h12')}</button>
      <button type="button" id="zReset" aria-label="${esc(T(U.zoomReset))}" title="${esc(T(U.zoomReset))}">${ico('M3 7V3h4M17 7V3h-4M3 13v4h4M17 13v4h-4')}</button></div></div>
    <div id="maplegend"></div><div class="panel" id="panel" aria-live="polite">${panelHtml()}</div><div class="maplist" id="maplist"></div></div>`;
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
  const tc = $('.tab[data-t="kaart"] small'); if (tc) tc.textContent = markers.length;
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
  el.innerHTML = `<h3>${esc(T(VIEW ? U.listView : U.listMap))} <span class="note">(${list.length})</span></h3>
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
function speciesTabHtml(){
  return `<input class="search" id="q" type="search" placeholder="${esc(T(U.search))}" value="${esc(Q)}" autocomplete="off" spellcheck="false" enterkeyhint="search"><div id="splist">${speciesListHtml()}</div>`;
}
function speciesListHtml(){
  const q = Q.trim().toLowerCase();
  const cats = catsInFilter().filter(c => !q || [c.nl, c.en, c.la].some(x => x.toLowerCase().includes(q)));
  if (!cats.length) return `<p class="empty">${esc(T(U.noHits))}</p>`;
  const ready = cats.filter(c => PAGES[c.no]), later = cats.filter(c => !PAGES[c.no]);
  let h = '';
  if (ready.length) h += `<div class="grouph"><h3>${esc(T(U.ready))}</h3><span>${ready.length}</span></div><div class="grid">${ready.map(c => `<a class="scard" href="${spHref(c.no)}">
      <div class="ph">${img(c.photos[0], catName(c))}</div><div class="bd"><span class="no">№ ${c.no}</span><span class="nm">${esc(catName(c))}</span><span class="la lat">${esc(c.la)}</span>
      <span class="ft">${BEST[c.no] ? scoreHtml(BEST[c.no], false, true) : ''}</span></div></a>`).join('')}</div>`;
  if (later.length) h += `<div class="grouph"><h3>${esc(T(U.soon))}</h3><span>${later.length}</span></div><ul class="soonlist">${later.map(c => `<li>
      ${img(c.photos[0], catName(c), false, true)}<div><b>${esc(catName(c))}</b><span class="la lat">${esc(c.la)}</span></div>${BEST[c.no] ? scoreHtml(BEST[c.no], false, true) : '<span></span>'}</li>`).join('')}</ul>`;
  return h;
}
function tabBody(){
  if (TAB === 'kaart') return mapTabHtml();
  if (TAB === 'soorten') return speciesTabHtml();
  return `<p class="note" style="margin-bottom:14px">${esc(T(U.topSub))}</p><div id="tops">${topsHtml()}</div>`;
}
function renderBar(){
  const tabs = [['kaart','navMap'],['topspots','navTop'],['soorten','navSpecies']];
  return `<div class="chips" role="group" aria-label="${esc(L==='nl'?'Filter per werelddeel':'Filter by continent')}">
    ${['all',...CONTS].map(c => `<button type="button" class="chip" data-f="${c}" aria-pressed="${FILTER===c}">${esc(c==='all'?T(U.all):contName(c))}</button>`).join('')}</div>
    <div class="tabs" role="tablist">${tabs.map(([t,k]) => `<button type="button" class="tab" role="tab" data-t="${t}" aria-selected="${TAB===t}">${esc(T(U[k]))}<small>${tabCount(t)}</small></button>`).join('')}</div>`;
}
function renderHome(){
  $('#main').innerHTML = `
  <section class="intro"><div class="wrap"><h1>${esc(T(U.title))}</h1><p class="sub">${esc(T(U.sub))}</p></div></section>
  <div class="bar"><div class="wrap" id="bar">${renderBar()}</div></div>
  <section class="sec" style="padding-top:18px"><div class="wrap" id="tabbody">${tabBody()}</div></section>`;
  bindHome();
}
function refreshHome(){ $('#bar').innerHTML = renderBar(); $('#tabbody').innerHTML = tabBody(); bindHome(); }
function bindHome(){
  $$('.chip[data-f]').forEach(b => b.onclick = () => {
    FILTER = b.dataset.f; CAT = null; VIEW = null; LISTALL = false; BASEX = null; try { localStorage.setItem('sg-cont', FILTER); } catch(e) {}
    if (SEL && SPOT[SEL] && !inFilter(SPOT[SEL].cont)) SEL = null;
    refreshHome();
  });
  $$('.tab').forEach(b => b.onclick = () => {
    TAB = b.dataset.t; try { history.replaceState(null, '', '#' + TAB); } catch(e) {}
    refreshHome(); renderChrome({nav: TAB === 'kaart' ? '' : TAB});
    const bar = $('.bar'); if (bar && bar.getBoundingClientRect().top < 0) window.scrollTo(0, $('.intro').offsetHeight);
  });
  $$('.tcard').forEach(b => b.onclick = () => {
    const no = +b.dataset.no;
    if (PAGES[no]) { location.href = spHref(no); return; }
    SEL = b.dataset.spot; TAB = 'kaart'; try { history.replaceState(null, '', '#kaart'); } catch(e) {}
    refreshHome(); renderChrome({nav:''}); window.scrollTo(0, $('.intro').offsetHeight);
  });
  $$('.catbtn').forEach(b => b.onclick = () => {
    CAT = b.dataset.cat ? +b.dataset.cat : null; VIEW = null; LISTALL = false;
    if (SEL && CAT && !SPOT[SEL].recs.some(r => r.no === CAT)) SEL = null;
    const x = $('#catrow').scrollLeft; refreshHome(); const cr = $('#catrow'); if (cr) cr.scrollLeft = x;
  });
  const sa = $('#showAll'); if (sa) sa.onclick = () => { SHOWALL = !SHOWALL; $('#tops').innerHTML = topsHtml(); bindHome(); };
  const q = $('#q'); if (q) q.oninput = () => { Q = q.value; $('#splist').innerHTML = speciesListHtml(); };
  const zi = $('#zIn'); if (zi) { zi.onclick = () => zoomBy(2); $('#zOut').onclick = () => zoomBy(.5); $('#zReset').onclick = () => { VIEW = null; LISTALL = false; drawHomeMap(); }; }
  drawHomeMap();
}
let rsz; window.addEventListener('resize', () => { clearTimeout(rsz); rsz = setTimeout(() => { if ($('#mapwrap')) drawHomeMap(); if ($('#spmap')) drawSpeciesMap(); }, 200); });

/* ---------- soortpagina ---------- */
// eerste deel van de seizoenstekst (tot de eerste ; of haakje), voor samenvattingen
const shortSeason = r => T(r.season).split(/;\s*|\s\(/)[0].replace(/[.,]\s*$/, '');
let SPMAP = null;
function drawSpeciesMap(){
  const el = $('#spmap'); if (!el || !SPMAP) return;
  el.innerHTML = mapSvg({...SPMAP, cw: el.clientWidth || 360, borders: true});
  bindMarkers(el, id => { const d = document.getElementById('plek-' + id); if (d) { d.open = true; d.scrollIntoView({block:'start', behavior:'smooth'}); } });
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
  $('#main').innerHTML = `
  <div class="wrap"><p class="crumbs"><a href="#soorten">← ${esc(T(U.back))}</a></p>
  <section class="sphead">
    <figure class="hero"><div class="ph">${img(c.photos[0], catName(c), true)}</div><figcaption>${credit(c.photos[0].cr)}</figcaption></figure>
    <div class="idblock">
      <span class="lbl">№ ${c.no} · ${c.cont.map(contName).join(' · ')}</span>
      <h1>${esc(catName(c))}</h1>
      <p class="en">${esc(L==='nl'?c.en:c.nl)} · <span class="lat">${esc(c.la)}</span></p>
      <div class="badges">${iucnHtml(c.iucn)}</div>
      <dl class="summary">
        <div><dt>${esc(T(U.bestPlace))}</dt><dd>${esc(T(top.s.name))}<small>${esc(T(top.s.country))}</small></dd></div>
        <div><dt>${esc(T(U.bestTime))}</dt><dd>${esc(season1)}</dd></div>
      </dl>
      <p class="lead">${esc(story)}${km ? `<span class="kans">${esc(km[0])}</span>` : ''}</p>
    </div>
  </section></div>
  <nav class="jump" aria-label="${esc(L==='nl'?'Snel naar':'Jump to')}"><div class="wrap">
    ${[['kaartsec','jMap'],['plekken','jPlaces'],['tipssec','jTips'],['statussec','jStatus'],...(c.photos.length > 1 ? [['fotosec','photos']] : []),['bronnen','jSources']].map(([id,k]) => `<button type="button" data-go="${id}">${esc(T(U[k]))}</button>`).join('')}
  </div></nav>
  <div class="wrap">
  <section class="sec anchor" id="kaartsec"><div class="sechead"><h2>${esc(T(U.habitat))}</h2></div>
    <div class="mapbox">${alsoHtml(no, recs)}<div id="spmap"></div>${legendHtml(false)}<div class="panel"><p class="note">${esc(T(U.habitatNote))}</p></div></div></section>
  <section class="sec anchor" id="plekken"><div class="sechead"><h2>${esc(T(U.bestSpots))}</h2><p>${esc(T(U.bestSpotsSub))}</p></div>
    <ol class="spots">${recs.map(({s,r},i) => `<li><details class="spot" id="plek-${esc(s.id)}" style="--c:var(--s${r.score})">
      <summary><span class="rank">${i+1}</span><span class="tt"><h3>${esc(T(s.name))}</h3><span class="where">${esc(T(s.country))}</span>${shortSeason(r) ? `<span class="ssn"><svg viewBox="0 0 20 20" aria-hidden="true">${FICO.season}</svg>${esc(shortSeason(r))}</span>` : ''}</span><span class="sc-sum">${scoreHtml(r.score, false, true)}</span>${CHEV}</summary>
      <div class="body"><p class="where">${esc(T(s.area))}</p>${scoreHtml(r.score)}
      <p class="why">${esc(T(r.why))}${cite(r.src)}</p>${factsHtml(r)}</div></details></li>`).join('')}</ol></section>
  <section class="sec two">
    <div class="anchor" id="tipssec"><h2>${esc(T(U.tips))}</h2><ul class="tips" style="margin-top:14px">${T(P.tips).map(x=>`<li>${esc(x)}</li>`).join('')}</ul></div>
    <div class="anchor" id="statussec"><h2>${esc(T(U.status))}</h2><div class="box" style="margin-top:14px;display:grid;gap:12px">
      <div>${iucnHtml(c.iucn)}</div><p>${esc(T(P.status))}${cite(P.statusSrc)}</p>
      <h3>${esc(T(U.threats))}</h3><ul class="tips">${T(P.threats).map(x=>`<li>${esc(x)}</li>`).join('')}</ul></div></div>
  </section>
  ${c.photos.length > 1 ? `<section class="sec anchor" id="fotosec"><h2 style="margin-bottom:14px">${esc(T(U.photos))}</h2><div class="gallery">${c.photos.slice(1).map(p => `<figure><div class="ph">${img(p, catName(c))}</div><figcaption>${credit(p.cr)}</figcaption></figure>`).join('')}</div></section>` : ''}
  <section class="sec read anchor" id="bronnen"><details class="srcbox" id="srcbox"><summary><h2>${esc(T(U.sources))} <span class="cnt">(${P.sources.length})</span></h2>${CHEV}</summary>
    <ol class="sources">${P.sources.map((g,i) => `<li id="bron-${no}-${i+1}"><a href="${esc(SRC[g].url)}" target="_blank" rel="noopener">${esc(T(SRC[g].title))}</a></li>`).join('')}</ol></details>
    <p class="note" style="margin-top:14px">${esc(L==='nl'?'Foto’s, leefgebied en IUCN-status: De KATalogue.':'Photos, range and IUCN status: De KATalogue.')}</p>
    <p style="margin-top:14px">${esc(L==='nl'?'Zelf deze kat gezien, of klopt er iets niet?':'Seen this cat yourself, or is something wrong?')} <a class="btnlink" href="#melden-${no}">${esc(L==='nl'?'Meld het hier':'Report it here')} →</a></p></section>
  </div>`;
  drawSpeciesMap(); bindAlso(no, recs);
  $$('.jump button').forEach(b => b.onclick = () => { const el = document.getElementById(b.dataset.go); if (el) el.scrollIntoView({block:'start', behavior:'smooth'}); });
  bindJumpSpy();
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
  $('#main').innerHTML = `<div class="wrap sec read"><h1>${esc(c ? catName(c) : '404')}</h1><p style="margin-top:12px">${esc(c ? T(U.soonPage) + '.' : T(U.notFound))}</p><p style="margin-top:16px"><a class="btnlink" href="#soorten">← ${esc(T(U.back))}</a></p></div>`;
  return c ? catName(c) : '';
}

/* ---------- tekstpagina's ---------- */
function renderText(id){
  const pg = D.text[id];
  let html = `<div class="wrap sec"><div class="read prose"><span class="lbl">${esc(T(pg.eyebrow))}</span><h1>${esc(T(pg.title))}</h1>${T(pg.html)}`;
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
  $('#main').innerHTML = `<div class="wrap sec"><div class="read prose">
    <span class="lbl">${esc(nl?'Contact':'Contact')}</span><h1>${esc(T(U.navReport))}</h1>
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
  let title = '', nav = '', page = 0;
  const y = window.scrollY;
  if (h === 'start' || h === '' || h === 'topspots' || h === 'kaart' || h === 'soorten') {
    if (h !== 'start' && h !== '') TAB = h;
    nav = TAB === 'kaart' ? '' : TAB; renderHome();
  }
  else if (/^soort-\d+$/.test(h)) { nav = 'soorten'; page = +h.slice(6); title = renderSpecies(page); }
  else if (/^melden(-\d+)?$/.test(h)) { nav = 'melden'; title = renderReport(+(h.split('-')[1] || 0)); }
  else if (D.text[h]) { nav = h; title = renderText(h); }
  else { title = renderMissing(null); }
  renderChrome({title, nav, page});
  window.scrollTo(0, keep ? y : 0);
  if (keep) { drawHomeMap(); drawSpeciesMap(); }
}
window.addEventListener('hashchange', () => route(false));
/* telefoon: balk met werelddelen en tabbladen weg bij omlaag scrollen, terug bij omhoog */
let BARY = window.scrollY;
window.addEventListener('scroll', () => {
  const b = document.querySelector('.bar'), y = window.scrollY;
  if (!b) { BARY = y; return; }
  const i = document.querySelector('.intro'), lim = i ? i.offsetTop + i.offsetHeight + b.offsetHeight : 0;
  if (y <= lim || y < BARY - 8) b.classList.remove('hid');
  else if (y > BARY + 8) b.classList.add('hid');
  if (Math.abs(y - BARY) > 8 || y <= lim) BARY = y;
}, {passive: true});
route(false);
})();
