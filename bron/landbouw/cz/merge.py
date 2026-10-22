import json,unicodedata,re
from shapely.geometry import shape, Point
n3=json.load(open('kaart/nuts3.geojson'))
KEY={'CZ010':'praha','CZ020':'stredocesky','CZ031':'jihocesky','CZ032':'plzensky','CZ041':'karlovarsky','CZ042':'ustecky','CZ051':'liberecky','CZ052':'kralovehradecky','CZ053':'pardubicky','CZ063':'vysocina','CZ064':'jihomoravsky','CZ071':'olomoucky','CZ072':'zlinsky','CZ080':'moravskoslezsky'}
PL={KEY[f['properties']['NUTS_ID']]:shape(f['geometry']) for f in n3['features'] if f['properties']['NUTS_ID'] in KEY}
def regio(lon,lat):
    if lon is None: return 'circus'
    p=Point(lon,lat)
    for k,g in PL.items():
        if g.contains(p): return k
    return min(PL,key=lambda k:PL[k].distance(p))
def norm(s): return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode())
L=[];Z=[]
for p in ['pr','zw','nb','zm','om','op']:
    d=json.load(open(p+'_resultaat.json'))
    for l in d['locaties']:
        l=dict(l);l['_bron']=p;l['regio']=regio(l.get('lon'),l.get('lat'));L.append(l)
    for z in d['zonder_katten']: z=dict(z);z['_bron']=p;Z.append(z)
json.dump({'locaties':L,'zonder_katten':Z},open('cz_merged.json','w'),ensure_ascii=False,indent=1)
for l in L: print(l['_bron'],l['regio'],'|',l['naam'],'|',l.get('plaats'),'|',' '.join(k['soort'][:10]+':'+k['status'] for k in l['katten']))
print(len(L),len(Z))
lst=json.load(open('lst_resultaat.json'))
names=[norm(l['naam']) for l in L]+[norm(z['naam']) for z in Z]
print('--- ZTL/officieel niet gedekt:')
for a in lst['alle_instellingen']:
    n=norm(a['naam'])
    if not any(n[:8] in x or x[:8] in n for x in names): print('  ',a['naam'],'|',a.get('plaats'),'|',a.get('kraj'),'|',a.get('bron'),'|',a.get('katten_volgens_zootierliste'))
print('officieel:',lst['lijsten']['officieel'].get('aantal'));[print('  o',n) for n in lst['lijsten']['officieel']['namen']]
