// Hulpje voor samenvoegen.py: leest uit een gidsscript de waarden van één-regelige "const X=…" en "Object.assign(X,{…})".
// Gebruik: node lit.js < script.js  → JSON {"const": {naam: waarde}, "assign": {naam: object}}; een Set wordt {"__set": [...]}.
const fs = require("fs");
const js = fs.readFileSync(0, "utf8");
const out = { const: {}, assign: {} };
const enc = v => v instanceof Set ? { __set: [...v] } : v;
for (const line of js.split("\n")) {
  let m = line.match(/^\s*(?:const|let) ([A-Za-z_][A-Za-z_0-9]*)\s*=\s*(.*?);?\s*$/);
  if (m && /^[\[{"]|^new Set\(/.test(m[2])) {
    try { out.const[m[1]] = enc(eval("(" + m[2] + ")")); } catch (e) {}
    continue;
  }
  m = line.match(/^\s*Object\.assign\(([A-Za-z_0-9]+),(\{.*\})\);\s*$/);
  if (m) { try { out.assign[m[1]] = Object.assign(out.assign[m[1]] || {}, eval("(" + m[2] + ")")); } catch (e) {} }
}
process.stdout.write(JSON.stringify(out));
