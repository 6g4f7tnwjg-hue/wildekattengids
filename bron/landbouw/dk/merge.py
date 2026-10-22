import json
RP=json.load(open('kaart/regios_poly.json'))
KEY={'DK01':'hovedstaden','DK02':'sjaelland','DK03':'syddanmark','DK04':'midtjylland','DK05':'nordjylland'}
def inside(x,y,r):
    c=False
    for i in range(len(r)):
        x1,y1=r[i];x2,y2=r[i-1]
        if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1)+x1:c=not c
    return c
def regio(lon,lat):
    for k,rs in RP.items():
        if any(inside(lon,lat,r) for r in rs):return KEY[k]
    # dichtstbijzijnde punt
    best=None
    for k,rs in RP.items():
        for r in rs:
            for x,y in r:
                d=(x-lon)**2+(y-lat)**2
                if best is None or d<best[0]:best=(d,k)
    return KEY[best[1]]
L=[];Z=[]
src={p:json.load(open(p+'_resultaat.json')) for p in ['hs','sd','mj','nj','op']}
skip={('op','Odsherred Zoo Rescue'),('op','Krokodille Zoo'),('op','Munkholm Zoo')}
for p,d in src.items():
    for l in d['locaties']:
        if (p,l['naam']) in skip:continue
        l=dict(l);l.pop('regio',None);l['regio']=regio(l['lon'],l['lat']);l['_bron']=p
        L.append(l)
    for z in d['zonder_katten']:
        z=dict(z);z['_bron']=p;Z.append(z)
json.dump({'locaties':L,'zonder_katten':Z},open('dk_merged.json','w'),ensure_ascii=False,indent=1)
for l in L:print(l['regio'],'|',l['naam'],'|',l['plaats'],'|',[k['soort']+':'+k['status'] for k in l['katten']])
print(len(L),len(Z))
