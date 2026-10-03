# Clearance audit: furniture footprints vs. door/drawer swing zones and minimum walkways (metres, plan coords)
import math
R = {  # name: (x1,x2,z1,z2)  -- updated to the PDF-measured layout
 'sofa long':(4.00,6.60,3.00,3.95),'sofa return':(5.65,6.60,1.65,3.00),'coffee table':(4.15,5.25,1.95,2.55),'media base':(3.05,6.95,0,.49),
 'storage wall':(0,.60,0,2.78),
 'entry commode':(1.45,1.75,2.99,4.21),'fridge col':(3.59,4.25,5.70,6.40),'appliance col':(3.59,4.25,6.42,7.02),'coffee col':(3.59,4.25,7.02,7.62),'west run':(3.59,4.24,7.62,8.16),'south run':(4.21,7.28,8.16,8.79),
 'island':(5.42,6.32,5.51,7.11),'stools E':(6.33,6.63,5.62,6.60),'stools W':(5.11,5.41,5.62,6.60),
 'r1 bed':(-2.07,-1.15,-5.01,-2.99),'r1 desk':(-3.89,-3.29,-4.96,-3.71),'r1 wardrobe':(-3.81,-2.36,-1.40,-.80),'r1 low unit':(-1.50,-1.15,-2.92,-2.20),'r1 nightstand':(-2.49,-2.09,-5.01,-4.61),
 'r2 bed':(-.97,-.05,-5.00,-2.98),'r2 desk':(1.25,1.85,-4.98,-3.78),'r2 wardrobe':(-.96,.78,-2.05,-1.45),'r2 bookcase':(1.50,1.85,-3.65,-2.25),
 'r3 bed':(-1.17,-.22,.70,2.76),'r3 bench':(-3.83,-3.43,.47,1.33),'r3 desk':(-3.83,-1.83,1.98,2.78),'r3 desk return':(-3.83,-3.28,1.38,1.98),'r3 wardrobe':(-3.83,-2.36,-.50,.09),'r3 bookcase':(-1.08,-.25,.13,.51),
 'm bed':(6.18,7.78,-2.34,-.17),'m ns L':(5.58,6.10,-.62,-.17),'m ns R':(7.86,8.38,-.62,-.17),'m plant':(8.38,8.72,-2.92,-2.58),
 'closet N':(7.01,8.32,-5.01,-4.41),'closet E':(8.32,8.92,-5.01,-3.23),
 'mb shower':(4.63,5.69,-4.98,-4.06),'mb vanity':(4.60,5.10,-3.99,-3.29),'mb wc':(6.07,6.43,-4.79,-4.24),'mb ledge':(5.95,6.88,-5.01,-4.83),'mb ladder':(5.40,5.90,-3.29,-3.23),
 'fb vanity':(1.98,2.45,-2.67,-1.65),'fb wc':(2.16,2.71,-3.56,-3.20),'fb tub':(3.72,4.49,-2.98,-1.37),'fb washer':(3.87,4.47,-3.76,-3.15),'fb ladder':(2.42,2.76,-1.43,-1.37),
 'ac condenser':(2.30,3.19,-5.25,-4.91),'water heater':(3.77,4.31,-5.07,-4.53),
}
def quarter(cx,cz,r,sx,sz):  # quarter-disc swing as (centre, radius, quadrant signs)
  return (cx,cz,r,sx,sz)
S = {  # door / appliance swing zones
 'front door':quarter(1.62,5.50,.90,1,-1),'room1 door':quarter(-1.24,-1.355,.81,-1,-1),'room2 door':quarter(1.76,-1.355,.87,-1,-1),
 'bath door':quarter(3.68,-1.315,.81,-1,-1),'master door':quarter(4.205,-.35,.80,1,-1),'mbath door':quarter(6.88,-3.36,.70,-1,-1),
 'washer door':quarter(3.87,-3.16,.55,-1,-1),
 'fridge door':quarter(4.25,6.40,.62,1,-1),'oven door (column)':(4.25,4.78,6.46,6.98),'dishwasher door':(5.65,6.25,7.59,8.19),'blast door (open 90)':quarter(-1.96,-.145,.83,1,-1),
 'island drawers pulled out':(5.44,6.30,7.11,7.53),'robot exit path':(.60,1.40,0,.46),
}
own = {'front door':[], 'shower door':['mb shower'], 'washer door':['fb washer'], 'fridge door':['fridge col'], 'oven door (column)':['appliance col'], 'island drawers pulled out':['island'], 'dishwasher door':['south run']}
def rect_hits_quarter(r,q):
  x1,x2,z1,z2=r; cx,cz,rad,sx,sz=q
  qx1,qx2=(cx,cx+rad) if sx>0 else (cx-rad,cx); qz1,qz2=(cz,cz+rad) if sz>0 else (cz-rad,cz)
  if x2<=qx1+1e-3 or x1>=qx2-1e-3 or z2<=qz1+1e-3 or z1>=qz2-1e-3: return False
  px=min(max(cx,x1),x2); pz=min(max(cz,z1),z2)
  return math.hypot(px-cx,pz-cz) < rad-1e-3
def rr(a,b): return not (a[1]<=b[0]+1e-3 or a[0]>=b[1]-1e-3 or a[3]<=b[2]+1e-3 or a[2]>=b[3]-1e-3)
bad=0
for sn,q in S.items():
  for rn,r in R.items():
    if rn in own.get(sn,[]): continue
    hit = rect_hits_quarter(r,q) if len(q)==5 else rr(r,q)
    if hit: print('CONFLICT', sn, 'x', rn); bad+=1
names=list(R)
for i in range(len(names)):
  for j in range(i+1,len(names)):
    if rr(R[names[i]],R[names[j]]): print('OVERLAP', names[i], names[j]); bad+=1
W = [ # walkways that must stay >= limit (NKBA: work aisle 1.07, walkway 0.91, pass behind a seated diner 0.91)
 ('island <-> sink run (seated diners, walk behind)', 5.42-4.24, 1.12), ('island <-> hob run', 8.16-7.11, 1.05), ('island <-> sofa back (living walkway)', 5.51-3.95, .91),
 ('sofa back <-> balcony glass (access to door A)', 7.29-6.60, .65), ('coffee table <-> sofa front', 2.60-2.15, .40), ('coffee table <-> return front', 5.65-5.25, .40), ('coffee table <-> media unit', 1.95-.49, .9),
 ('island top edge <-> balcony glass (behind stools)', 7.29-6.32, .91), ('fridge door swing end <-> west stool seat', 5.11-4.87, .0),
 ('entry commode face <-> door opening edge', 1.62-1.75, -.15), ('entry commode end <-> door leaf', 4.60-4.21, .3),
 ('master bed foot <-> TV wall', -2.34-(-3.11), .6), ('master bed L <-> west wall', 6.18-4.60, .75), ('master bed R <-> east wall', 8.92-7.78, .6),
 ('room2 bed <-> bookcase', 1.50-(-.05), .75), ('room2 wardrobe doors <-> bed foot', -2.05-.57-(-2.98), .3),
 ('mbath WC centre <-> side wall', 6.88-6.39, .40), ('mbath WC centre <-> shower glass', 6.39-5.60, .40), ('mbath WC front clearance', -3.23-(-4.27), .6),
 ('family WC centre <-> window wall', -3.38-(-3.80), .40), ('family WC front <-> tub', 3.72-2.71, .6), ('corridor with blast door open flat', -.215-(-1.26), .9),
 ('room1 door leaf end <-> low unit', -2.165-(-2.20), .0), 
]
for n,v,lim in W:
  ok = v>=lim-1e-3; bad += (not ok); print(('OK  ' if ok else 'FAIL'), f'{n}: {v:.2f} m (min {lim})')
print('\nTOTAL ISSUES:', bad)
