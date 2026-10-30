# Voegt de onderzoeksuitvoer samen tot ro_merged.json; județ uit de coördinaten (NUTS 3) (NUTS 3, kaart/nuts3.geojson; zie ../kaart_maken.py).
import json,unicodedata,re,os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from shapely.geometry import shape, Point
n3=json.load(open('kaart/nuts3.geojson'))
def slug(s): return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode()).strip('-')
KEY={f['properties']['NUTS_ID']:slug(f['properties']['NAME_LATN']) for f in n3['features'] if f['properties']['CNTR_CODE']=='RO'}
PL={KEY[f['properties']['NUTS_ID']]:shape(f['geometry']) for f in n3['features'] if f['properties']['NUTS_ID'] in KEY}
def regio(lon,lat):
    if lon is None: return 'circus'
    p=Point(lon,lat)
    for k,g in PL.items():
        if g.contains(p): return k
    return min(PL,key=lambda k:PL[k].distance(p))
def norm(s): return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode())
L=[];Z=[]
for p in ['zu','ce','we','oo','op']+[f'vv{i}' for i in range(1,6)]:
    if not os.path.exists(p+'_resultaat.json'): continue
    d=json.load(open(p+'_resultaat.json'))
    for l in d.get('locaties',[]):
        l=dict(l);l['_bron']=p;l['regio']=regio(l.get('lon'),l.get('lat'));L.append(l)
    for z in d.get('zonder_katten',[]): z=dict(z);z['_bron']=p;Z.append(z)
json.dump({'locaties':L,'zonder_katten':Z},open('ro_merged.json','w'),ensure_ascii=False,indent=1)
for l in L: print(l['_bron'],l['regio'],'|',l['naam'],'|',l.get('plaats'),'|',' '.join(k['soort'][:10]+':'+k['status'] for k in l['katten']))
print(len(L),len(Z))
if os.path.exists('lst_resultaat.json'):
    lst=json.load(open('lst_resultaat.json'))
    names=[norm(l['naam']) for l in L]+[norm(z['naam']) for z in Z]
    print('--- lijsten niet gedekt:')
    for a in lst.get('alle_instellingen',[]):
        n=norm(a['naam'])
        if not any(n[:8] in x or x[:8] in n for x in names): print('  ',a['naam'],'|',a.get('plaats'),'|',a.get('judet'),'|',a.get('bron'),'|',a.get('katten_volgens_zootierliste'))
