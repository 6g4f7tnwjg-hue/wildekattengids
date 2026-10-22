import json,math
B=(7.9,54.45,15.3,57.85)  # lon0,lat0,lon1,lat1
def rings(f):
    g=f['geometry'];P=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
    return [p for p in P]
def area(r):
    return abs(sum(r[i][0]*r[i+1][1]-r[i+1][0]*r[i][1] for i in range(len(r)-1))/2)
def dp(pts,eps):
    if len(pts)<3:return pts
    a,b=pts[0],pts[-1];dmax=0;idx=0
    for i in range(1,len(pts)-1):
        p=pts[i];dx,dy=b[0]-a[0],b[1]-a[1]
        L=math.hypot(dx,dy) or 1e-12
        d=abs(dy*p[0]-dx*p[1]+b[0]*a[1]-b[1]*a[0])/L if (dx or dy) else math.hypot(p[0]-a[0],p[1]-a[1])
        if d>dmax:dmax=d;idx=i
    if dmax>eps:return dp(pts[:idx+1],eps)[:-1]+dp(pts[idx:],eps)
    return [a,b]
def r2(r):return [[round(x,2),round(y,2)] for x,y in r]
def dedup(r):
    o=[]
    for p in r:
        if not o or o[-1]!=p:o.append(p)
    return o
def clip(poly,b):
    def ci(pts,inside,inter):
        out=[]
        for i in range(len(pts)):
            cur,prev=pts[i],pts[i-1]
            if inside(cur):
                if not inside(prev):out.append(inter(prev,cur))
                out.append(cur)
            elif inside(prev):out.append(inter(prev,cur))
        return out
    x0,y0,x1,y1=b;pts=poly[:-1] if poly[0]==poly[-1] else poly
    def ix(xv):return lambda p,q:[xv,p[1]+(q[1]-p[1])*(xv-p[0])/(q[0]-p[0])]
    def iy(yv):return lambda p,q:[p[0]+(q[0]-p[0])*(yv-p[1])/(q[1]-p[1]),yv]
    for ins,inter in [(lambda p:p[0]>=x0,ix(x0)),(lambda p:p[0]<=x1,ix(x1)),(lambda p:p[1]>=y0,iy(y0)),(lambda p:p[1]<=y1,iy(y1))]:
        if not pts:break
        pts=ci(pts,ins,inter)
    return pts
n0=json.load(open('nuts0.geojson'));n2=json.load(open('nuts2.geojson'))
F0={f['properties']['NUTS_ID']:f for f in n0['features']}
dk=[p[0] for p in rings(F0['DK'])]
dk.sort(key=area,reverse=True)
eps=0.008
MAIN=r2(dedup(dp(dk[0],eps)))
ISL=[r2(dedup(dp(r,eps))) for r in dk[1:] if area(r)>0.003]
ISL=[r for r in ISL if len(r)>=4]
BUUR=[]
for c in ['DE','SE']:
    for p in rings(F0[c]):
        r=p[0]
        if not any(B[0]<=x<=B[2] and B[1]<=y<=B[3] for x,y in r):continue
        cr=clip(r,B)
        if len(cr)>=3:
            cr=dedup(r2(dp(cr+[cr[0]],eps)))
            if len(cr)>=4 and area(cr)>0.002:BUUR.append(cr)
# regio's: gedeelde grenzen
R={f['properties']['NUTS_ID']:f for f in n2['features'] if f['properties']['NUTS_ID'].startswith('DK')}
print(sorted(R),[R[k]['properties'].get('NAME_LATN') for k in sorted(R)])
from collections import defaultdict
own=defaultdict(set)
for k,f in R.items():
    for p in rings(f):
        for x,y in p[0]:own[(round(x,5),round(y,5))].add(k)
LINES=[]
for k,f in sorted(R.items()):
    for p in rings(f):
        r=p[0];run=[]
        for x,y in r:
            key=(round(x,5),round(y,5))
            o=own[key]
            if len(o)>1 and min(o)==k:   # alleen vanuit de 'kleinste' regio tekenen
                run.append([x,y])
            else:
                if len(run)>1:LINES.append(run)
                run=[]
        if len(run)>1:LINES.append(run)
LINES=[r2(dedup(dp(l,eps))) for l in LINES]
LINES=[l for l in LINES if len(l)>1]
print(len(MAIN),len(ISL),[len(i) for i in ISL],len(BUUR),len(LINES))
json.dump({"MAIN":MAIN,"ISLANDS":ISL,"BUUR":BUUR,"LINES":LINES,"REG":{k:R[k]['properties'].get('NAME_LATN') for k in R}},open('kaart.json','w'))
# regio-polygonen voor punt-in-polygoon
json.dump({k:[p[0] for p in rings(f)] for k,f in R.items()},open('regios_poly.json','w'))
