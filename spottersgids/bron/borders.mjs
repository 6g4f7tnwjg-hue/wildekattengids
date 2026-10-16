import fs from 'fs';
import {feature, mesh} from 'topojson-client';
import {geoCentroid, geoArea} from 'd3-geo';
import countries from 'i18n-iso-countries';
import { createRequire } from 'module'; const require = createRequire(import.meta.url);
countries.registerLocale(require('i18n-iso-countries/langs/nl.json'));
countries.registerLocale(require('i18n-iso-countries/langs/en.json'));
const world = JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-110m.json'));
const P = ([lon,lat]) => [+((lon+180)*2).toFixed(1), +((84-lat)*2).toFixed(1)];
const m = mesh(world, world.objects.countries, (a,b) => a !== b);
let d = '';
for (const line of m.coordinates) { d += 'M' + line.map(c => P(c).join(',')).join(' '); }
const fc = feature(world, world.objects.countries);
const short = {nl:{'Verenigde Staten van Amerika':'VS','Verenigde Staten':'VS','Russische Federatie':'Rusland','Democratische Republiek Congo':'DR Congo','Congo, Democratische Republiek':'DR Congo','Centraal-Afrikaanse Republiek':'CAR','Verenigd Koninkrijk':'VK','Iran, Islamitische Republiek':'Iran','Bolivia, Plurinationale Staat':'Bolivia','Venezuela, Bolivariaanse Republiek':'Venezuela','Tanzania, Verenigde Republiek':'Tanzania','Volksrepubliek China':'China'},
  en:{'United States of America':'USA','Russian Federation':'Russia','Democratic Republic of the Congo':'DR Congo','Central African Republic':'CAR','United Kingdom':'UK','Iran, Islamic Republic of':'Iran','Bolivia, Plurinational State of':'Bolivia','Venezuela, Bolivarian Republic of':'Venezuela','Tanzania, United Republic of':'Tanzania','Republic of the Congo':'Congo','Congo, The Democratic Republic of the':'DR Congo'}};
const labels = [];
for (const f of fc.features) {
  const a2 = countries.numericToAlpha2(f.id);
  let nl = a2 && countries.getName(a2,'nl',{select:'alias'}), en = a2 && countries.getName(a2,'en',{select:'alias'});
  if (!nl) { nl = en = f.properties.name; }
  nl = short.nl[nl] || nl; en = short.en[en] || en;
  // grootste deelgebied
  let g = f.geometry;
  if (g.type === 'MultiPolygon') { let best=null, ba=-1; for (const poly of g.coordinates) { const ar = geoArea({type:'Polygon',coordinates:poly}); if (ar>ba){ba=ar;best=poly;} } g = {type:'Polygon', coordinates:best}; }
  const [lon,lat] = geoCentroid(g); if (lat < -58) continue;
  const xs = g.coordinates[0].map(c => P(c)[0]); const w = Math.max(...xs) - Math.min(...xs);
  const [x,y] = P([lon,lat]);
  labels.push({nl, en, x, y, w: +w.toFixed(1)});
}
fs.writeFileSync(process.argv[2], JSON.stringify({borders: d, labels}));
console.log('grenzen', d.length, 'tekens;', labels.length, 'landen');
console.log(labels.filter(l=>['NL','Mongolië','VS','India','Spanje','Tanzania','Rusland','DR Congo'].includes(l.nl)).map(l=>l.nl+' '+l.x+','+l.y+' w'+l.w).join(' | '));
