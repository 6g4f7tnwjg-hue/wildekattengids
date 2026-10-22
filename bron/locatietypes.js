/* Locatietypes en labels. Wordt door bron/bouw.py achter het script van elke gids (en elke deelstaat) gezet,
   zodat het bij de gegevens en functies van die gids kan. LT komt uit bron/locatietypes.json. */
const LT_I=()=>({en:1,fr:2,de:3,it:4,es:5,pt:6,da:7})[LANG]||0;
const LT_TX=(nl,en,fr,de,it,es,pt,da)=>[nl,en,fr!==undefined?fr:en,de!==undefined?de:en,it!==undefined?it:en,es!==undefined?es:en,pt!==undefined?pt:en,da!==undefined?da:en][LT_I()];
const LT_KEY=nm=>{const i=LOCINFO[nm];return i&&i.type?i.type[0]:"";};
const LT_NAME=nm=>{const i=LOCINFO[nm];if(!i||!i.type)return "";const t=LT.types.find(x=>x.nl===i.type[0]);return t?LT_TX(t.nl,t.en,t.fr,t.de,t.it,t.es,t.pt,t.da):(i.type[LT_I()]||i.type[0]);};
const LT_LABS=nm=>(((LOCINFO[nm]||{}).labels)||[]).map(k=>LT.labels.find(l=>l.key===k)).filter(Boolean);
const LT_LTXT=l=>LT_TX(l.nl,l.en,l.fr,l.de,l.it,l.es,l.pt,l.da);
const LT_BEP=nm=>LT_LABS(nm).filter(l=>LT.beperkt.includes(l.key));
const LT_IDX=a=>{const m=(a.getAttribute("href")||"").match(/^#(?:[a-z-]+\/)?locatie\/(.+)$/);return m&&LOCBYSLUG[m[1]]!==undefined?LOCBYSLUG[m[1]]:-1;};
let LT_F="";
if(!document.getElementById("lt-css")){const s=document.createElement("style");s.id="lt-css";s.textContent=
`.lt-bar{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 6px}
.lt-chip{font:inherit;font-size:14px;line-height:1.3;padding:4px 11px;border-radius:999px;border:1.5px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
.lt-chip[aria-pressed="true"]{background:var(--ink);color:var(--card);border-color:var(--ink)}
.lt-chip:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.lt-chip .n{opacity:.7;font-variant-numeric:tabular-nums;margin-left:2px}
.lt-count{font-size:13.5px;color:var(--muted);margin:0 0 12px}
.map .mk.lt-off{display:none}
.lt-ty{white-space:nowrap}
.lt-labs{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 8px;padding:0;list-style:none}
.lt-lab{font-size:13px;line-height:1.35;border:1px solid var(--line);border-radius:999px;padding:1px 9px;background:var(--card)}
.lt-warn{display:inline-block;margin-top:2px;color:var(--w);font-style:normal}`;
document.head.appendChild(s);}

function LT_DECOR(){
  const sec=document.getElementById("locaties"); if(!sec)return;
  /* type achter de plaatsnaam in de lijsten per regio */
  sec.querySelectorAll(".loclist li").forEach(li=>{const a=li.querySelector('a[href*="locatie/"]');if(!a)return;const i=LT_IDX(a);if(i<0)return;
    const nm=LOCS[i][0];let s=li.querySelector(".lt-ty");
    if(!s){const p=li.querySelector(".plc");if(!p)return;s=document.createElement("span");s.className="lt-ty";p.appendChild(s);}
    s.textContent=" · "+LT_NAME(nm);li.dataset.ltType=LT_KEY(nm);});
  /* filterknoppen boven de kaart, alleen voor types die hier voorkomen */
  const cnt={};LOCS.forEach(l=>{const k=LT_KEY(l[0]);if(k)cnt[k]=(cnt[k]||0)+1;});
  const present=LT.types.filter(t=>cnt[t.nl]);
  let bar=document.getElementById("lt-bar");
  if(present.length<2){if(bar)bar.remove();return;}
  if(!bar){const mw=sec.querySelector(".mapwrap");if(!mw)return;
    mw.insertAdjacentHTML("beforebegin",'<div class="lt-bar" id="lt-bar" role="group"></div><p class="lt-count" id="lt-count" aria-live="polite"></p>');
    bar=document.getElementById("lt-bar");
    bar.addEventListener("click",e=>{const b=e.target.closest(".lt-chip");if(!b)return;LT_F=b.dataset.t;LT_DECOR();});}
  bar.setAttribute("aria-label",LT_TX("Soort locatie","Type of location","Type de lieu","Art des Ortes","Tipo di luogo","Tipo de lugar","Tipo de local","Type af sted"));
  bar.innerHTML=[["",LOCS.length,LT_TX("Alle","All","Tous","Alle","Tutti","Todos","Todos","Alle")]].concat(present.map(t=>[t.nl,cnt[t.nl],LT_TX(t.nl,t.en,t.fr,t.de,t.it,t.es,t.pt,t.da)]))
    .map(([k,n,l])=>`<button type="button" class="lt-chip" data-t="${esc(k)}" aria-pressed="${k===LT_F}">${esc(l)} <span class="n">${n}</span></button>`).join("");
  LT_APPLY();
}
function LT_APPLY(){
  const off=nm=>!!LT_F&&LT_KEY(nm)!==LT_F;
  document.querySelectorAll("#nlmap .mk").forEach(m=>{const l=LOCS[+m.dataset.i];if(l)m.classList.toggle("lt-off",off(l[0]));});
  const sel=document.getElementById("locsel");
  if(sel)[...sel.options].forEach(o=>{if(o.value==="")return;const l=LOCS[+o.value];if(!l)return;const h=off(l[0]);o.hidden=h;o.disabled=h;});
  const sec=document.getElementById("locaties");
  sec.querySelectorAll(".loclist li[data-lt-type]").forEach(li=>{li.hidden=!!LT_F&&li.dataset.ltType!==LT_F;});
  sec.querySelectorAll(".loclist").forEach(ul=>{const items=[...ul.querySelectorAll("li[data-lt-type]")];if(!items.length)return;
    const none=items.every(li=>li.hidden);ul.hidden=none;const g=ul.previousElementSibling;if(g&&g.classList.contains("group-title"))g.hidden=none;});
  const c=document.getElementById("lt-count");
  if(c){const n=LOCS.filter(l=>!off(l[0])).length;
    c.textContent=LT_F?LT_TX(`${n} van de ${LOCS.length} locaties getoond.`,`Showing ${n} of ${LOCS.length} locations.`,`${n} lieux sur ${LOCS.length} affichés.`,`${n} von ${LOCS.length} Orten angezeigt.`,`${n} luoghi su ${LOCS.length} mostrati.`,`${n} de ${LOCS.length} lugares mostrados.`,`${n} de ${LOCS.length} locais mostrados.`,`Viser ${n} af ${LOCS.length} steder.`):"";c.hidden=!LT_F;}
}
{const o=locHTML;locHTML=function(i){const h=o.apply(this,arguments);const t=LT_LABS(LOCS[i][0]).map(l=>`<span class="ip-tag">${l.icoon} ${esc(LT_LTXT(l))}</span>`).join("");
  return t?h.replace(/(<div class="ip-tags">[\s\S]*?)(<\/div>)/,(m,a,b)=>a+t+b):h;};}
{const o=showLoc;showLoc=function(i){const r=o.apply(this,arguments);const box=document.getElementById("mapinfo");const l=LOCS[i];
  if(box&&l){const p=box.querySelector(".pl");const labs=LT_LABS(l[0]);
    if(p&&labs.length&&!box.querySelector(".lt-labs"))p.insertAdjacentHTML("afterend",`<ul class="lt-labs">${labs.map(x=>`<li class="lt-lab">${x.icoon} ${esc(LT_LTXT(x))}</li>`).join("")}</ul>`);}
  LT_APPLY();return r;};}
{const o=buildRoute;buildRoute=function(){const r=o.apply(this,arguments);
  document.querySelectorAll("#rt-list .rt-row").forEach(row=>{const inp=row.querySelector("input");const sm=row.querySelector("small");if(!inp||!sm||sm.querySelector(".lt-warn"))return;
    const bep=LT_BEP(inp.value);if(bep.length)sm.insertAdjacentHTML("beforeend",`<br><span class="lt-warn">${bep.map(x=>`${x.icoon} ${esc(LT_LTXT(x))}`).join(" · ")}</span>`);});
  return r;};}
{const o=infoHTML;infoHTML=function(){const h=o.apply(this,arguments);
  return h.replace(/(<a href="#locatie\/([^"]+)">[^<]*<\/a><\/b> <span style="color:var\(--muted\)">\([^<]*\))(<\/span>)/g,(m,a,s,b)=>{const i=LOCBYSLUG[s];return i===undefined?m:a+" · "+esc(LT_NAME(LOCS[i][0]))+b;});};}
{const o=applyLang;applyLang=function(){const r=o.apply(this,arguments);LT_DECOR();return r;};}
applyLang(LANG,false);
