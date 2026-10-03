# Net room dimensions from the wall boxes in salon.html, measured at 1.0 m height (walls whose y-range covers 1.0)
import re, numpy as np
src = open('salon.html').read()
H=2.60; FT=2.70; DOORH=2.10; HEAD=2.30
env={'H':H,'FT':FT,'DOORH':DOORH,'HEAD':HEAD,'FX':7.28,'FO':7.70,'LZ':8.79}
boxes=[]; import os; YH=float(os.environ.get("YH","2.4"))
def ev(s): return float(eval(s.strip(),{},env))
seg=src.split('// WALLS:')[1].split('// corridor gypsum')[0]
for m in re.finditer(r'\bW\(([^()]*)\)', seg):
    a=[ev(t) for t in m.group(1).split(',')]
    y1=a[4] if len(a)>4 else 0; y2=a[5] if len(a)>5 else H
    if y1<=YH<=y2: boxes.append(a[:4])
for a,b,y1,y2 in [[-.13,.78,0,FT],[.78,3.45,HEAD,FT],[3.45,4.26,0,FT],[4.26,6.88,HEAD,FT],[6.88,7.70,0,FT],[7.70,8.39,0,1.0],[7.70,8.39,HEAD,FT],[8.39,9.11,0,FT]]:
    if y1<=YH<=y2: boxes.append([7.28,7.70,a,b])
R=0.005; x0,z0=-4.5,-5.6; nx,nz=int(14.2/R),int(15/R)
g=np.zeros((nx,nz),bool)
for x1,x2,z1,z2 in boxes:
    g[int((min(x1,x2)-x0)/R+.5):int((max(x1,x2)-x0)/R+.5), int((min(z1,z2)-z0)/R+.5):int((max(z1,z2)-z0)/R+.5)]=True
def span(x,z,axis):
    i,j=int((x-x0)/R),int((z-z0)/R)
    if axis=='x':
        a=i
        while not g[a,j]: a-=1
        b=i
        while b<nx-1 and not g[b,j]: b+=1
        return (a+1)*R+x0,b*R+x0
    a=j
    while not g[i,a]: a-=1
    b=j
    while b<nz-1 and not g[i,b]: b+=1
    return (a+1)*R+z0,b*R+z0
import json,sys
pts=json.loads(sys.argv[1]) if len(sys.argv)>1 else None
P=[('mamad',1.45,-1.63,262,355),('room A (NW)',-3.11,-1.63,361,274),('room B',-3.18,1.16,356,282),
   ('dining/alcove',1.41,1.18,277,None),('corridor',-0.65,1.18,110,None),('living (x)',1.41,3.82,None,728),
   ('living+kitchen (z)',4.41,5.18,879,None),('kitchen',6.89,5.18,None,365),('family bath',-2.35,3.31,238,245),
   ('master',-1.59,5.72,296,430),('master bath',-4.12,5.72,172,222),('closet',-4.12,7.87,175,190)]

from collections import Counter
def robust(x,z,axis):
    res=[]
    for o in (0,):
        try:
            a,b=span(x+o,z,axis) if axis=='z' else span(x,z+o,axis)
            res.append((round((b-a)*100),a,b))
        except Exception: pass
    c=Counter(r[0] for r in res).most_common(1)[0][0]
    return [r for r in res if r[0]==c][0], sorted(set(r[0] for r in res))
for n,z,x,lz,lx in P:
    (mz,za,zb),allz=robust(x,z,'z'); (mx,xa,xb),allx=robust(x,z,'x')
    s1=f"{mz}/{lz} ({mz-lz:+d})" if lz else f"{mz}/-"
    s2=f"{mx}/{lx} ({mx-lx:+d})" if lx else f"{mx}/-"
    print(f"{n:20s} z {s1:>16s}  x {s2:>16s}   z {za:.2f}..{zb:.2f} x {xa:.2f}..{xb:.2f}  (z seen {allz[:4]}, x seen {allx[:4]})")
