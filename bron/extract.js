// Haalt de gegevens (soorten, waarnemingen, locaties, jongen) uit een gids.
// Gebruik: node extract.js <gids.html>  → JSON op stdout: {"<deel>": {...}}
// Benelux-gidsen hebben één deel ("main"); de Duitse gids één deel per deelstaat.
const fs = require("fs");
function lit(js, name) {
  const i = js.search(new RegExp("(const|let) " + name + "\\s*="));
  if (i < 0) return undefined;
  let j = js.indexOf("=", i) + 1;
  while (/\s/.test(js[j])) j++;
  let d = 0, q = null, k = j;
  for (; k < js.length; k++) {
    const c = js[k];
    if (q) { if (c === "\\") { k++; continue; } if (c === q) q = null; continue; }
    if (c === '"' || c === "'" || c === "`") { q = c; continue; }
    if ("[{(".includes(c)) d++;
    else if ("]})".includes(c)) { d--; if (d === 0) { k++; break; } }
    else if (d === 0 && (c === ";" || c === "\n")) break;
  }
  let v;
  try { v = eval("(" + js.slice(j, k) + ")"); } catch (e) { return undefined; }
  if (v instanceof Set) v = [...v];
  return v;
}
const NAMES = ["SPECIES", "R", "LOCS", "YOUNG", "SPEN", "PANTH", "NOROUTE", "PHOTOS", "LOCINFO"];
function grab(js) { const o = {}; for (const n of NAMES) o[n] = lit(js, n); return o; }
const html = fs.readFileSync(process.argv[2], "utf8");
const out = {};
const re = /<script type="application\/json" id="ds-([a-z-]+)">([\s\S]*?)<\/script>/g;
let m, any = false;
const wp = html.match(/<script>window\.__PHOTOS=([\s\S]*?)<\/script>/);
const WINPHOTOS = wp ? lit("const P=" + wp[1], "P") : undefined;
while ((m = re.exec(html))) { any = true; out[m[1]] = grab(JSON.parse(m[2]).js); }
if (!any) {
  const s = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(x => x[1]).find(x => /const SPECIES\s*=/.test(x));
  if (s) out.main = grab(s);   // Franse gids zonder regio's: leeg
}
for (const k in out) if (!out[k].PHOTOS && WINPHOTOS) out[k].PHOTOS = WINPHOTOS;
process.stdout.write(JSON.stringify(out));
