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
