import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
O="/sessions/trusting-nice-davinci/mnt/outputs/"
C=[("Oklahoma City",35.4676,-97.5164),("Arlington VA",38.8816,-77.091),("Tulsa",36.154,-95.9928),("Washington DC",38.9072,-77.0369),("Lake Geneva",42.5917,-88.4334),("Madison",43.0731,-89.4012),("Kansas City",39.0997,-94.5786),("Ellis Island",40.6995,-74.0396),("Fort Worth",32.7555,-97.3308),("Portland ME",43.6591,-70.2568),("Annapolis",38.9784,-76.4922),("Helena",46.5958,-112.0362),("Hollywood",34.0928,-118.3287),("Newport RI",41.4901,-71.3128),("Northampton",42.3251,-72.6412),("Albany",42.6526,-73.7562),("Anaheim",33.8366,-117.9143),("St Louis",38.627,-90.1994),("Fort Wayne",41.0793,-85.1394),("Hartford",41.7658,-72.6734),("Tombstone",31.7129,-110.0675),("Santa Monica",34.0195,-118.4912),("Brooklyn",40.6782,-73.9442),("Princeton",40.3573,-74.6672),("Fairbanks",64.8378,-147.7164),("Dayton",39.7589,-84.1916),("Macon",32.8407,-83.6324),("Pierre",44.3683,-100.351),("Honolulu",21.3069,-157.8583),("Sequoia",36.4388,-118.9045),("Charleston WV",38.3498,-81.6326),("Butte",46.0038,-112.5348),("Baltimore",39.2904,-76.6122),("Tampa",27.9506,-82.4572),("Billings",45.7833,-108.5007),("Boston",42.3601,-71.0589),("Detroit",42.3314,-83.0458),("Chicago",41.8781,-87.6298),("Brookings OR",42.0526,-124.284),("Shanksville",40.0172,-78.9058),("Binghamton",42.0987,-75.918),("Indianapolis",39.7684,-86.1581),("Monterey",36.6002,-121.8947),("Nashville",36.1623,-86.7744),("Atlantic City",39.3643,-74.4229),("Birmingham",33.5186,-86.8104),("Cedar Rapids",41.9779,-91.6656),("Columbia SC",34.0007,-81.0348),("Philadelphia",39.9526,-75.1652),("Long Beach",33.769,-118.1916),("Phoenix",33.4484,-112.074),("Green Bay",44.5133,-88.0133),("Gainesville",29.6516,-82.3248),("Kalamazoo",42.2917,-85.5872),("Fort Knox",37.8913,-85.9653),("Mobile",30.6954,-88.0399),("Tucson",32.2226,-110.9747),("Klamath Falls",42.2249,-121.7817),("Albuquerque",35.0844,-106.6504),("Monowi",42.8303,-98.3295),("San Francisco",37.7749,-122.4194),("Salt Lake City",40.7608,-111.891)]
def albers(l1,l2,l0,o0):
    n=(np.sin(np.radians(l1))+np.sin(np.radians(l2)))/2
    c=np.cos(np.radians(l1))**2+2*n*np.sin(np.radians(l1))
    r0=np.sqrt(c-2*n*np.sin(np.radians(l0)))/n
    def f(lon,lat):
        lon=np.asarray(lon,float);lat=np.asarray(lat,float)
        r=np.sqrt(c-2*n*np.sin(np.radians(lat)))/n
        t=n*np.radians(lon-o0)
        return r*np.sin(t), r0-r*np.cos(t)
    return f
main=albers(29.5,45.5,37.5,-96)
ak=albers(55,65,50,-154)
hi=albers(8,18,3,-157)
# inset transforms: scale and offset in main-projection units
def inset(f,s,dx,dy):
    return lambda lo,la:(lambda x,y:(x*s+dx,y*s+dy))(*f(lo,la))
akf=inset(ak,0.35,-0.20,-0.37)
hif=inset(hi,1.0,0.02,-0.52)
polys=[]
for line in open(O+"us_states.txt"):
    if ":" not in line: continue
    name,rest=line.strip().split(":",1)
    for ring in rest.split("|"):
        pts=np.array([[float(v) for v in p.split(",")] for p in ring.split()])
        f=akf if name=="Alaska" else hif if name=="Hawaii" else main
        x,y=f(pts[:,0],pts[:,1]); polys.append(np.c_[x,y])
fig,ax=plt.subplots(figsize=(16,10.5),dpi=130)
for p in polys: ax.add_patch(Polygon(p,fc="#e9eef3",ec="#8a97a5",lw=0.7))
pos=[]
for nm,la,lo in C:
    f=akf if la>50 else hif if lo<-150 else main
    x,y=f(lo,la); pos.append((nm,float(x),float(y)))
ax.scatter([p[1] for p in pos],[p[2] for p in pos],s=38,c="#d6336c",ec="white",lw=0.8,zorder=5)
ax.set_aspect("equal");ax.axis("off")
allx=np.concatenate([p[:,0] for p in polys]);ally=np.concatenate([p[:,1] for p in polys])
ax.set_xlim(allx.min()-.02,allx.max()+.02);ax.set_ylim(ally.min()-.02,ally.max()+.02)
fig.canvas.draw();R=fig.canvas.get_renderer()
placed=[];dots=[ax.transData.transform((x,y)) for _,x,y in pos]
cands=[(8,6,"left","bottom"),(8,-6,"left","top"),(-8,6,"right","bottom"),(-8,-6,"right","top"),(0,12,"center","bottom"),(0,-12,"center","top"),(14,0,"left","center"),(-14,0,"right","center"),(22,16,"left","bottom"),(-22,16,"right","bottom"),(22,-16,"left","top"),(-22,-16,"right","top"),(34,0,"left","center"),(-34,0,"right","center"),(0,26,"center","bottom"),(0,-26,"center","top")]
def ov(a,b):return not(a.x1<b.x0 or a.x0>b.x1 or a.y1<b.y0 or a.y0>b.y1)
order=sorted(range(len(pos)),key=lambda i:-pos[i][1])
from matplotlib.transforms import Bbox
for i in order:
    nm,x,y=pos[i];best=None
    for dx,dy,ha,va in cands:
        t=ax.annotate(nm,(x,y),xytext=(dx,dy),textcoords="offset points",ha=ha,va=va,fontsize=8,zorder=6)
        bb=t.get_window_extent(R).expanded(1.05,1.15)
        bad=any(ov(bb,q) for q in placed) or any(bb.x0<=d[0]<=bb.x1 and bb.y0<=d[1]<=bb.y1 for j,d in enumerate(dots) if j!=i)
        if not bad: best=(t,bb);break
        t.remove()
    if best is None:
        dx,dy,ha,va=cands[0];t=ax.annotate(nm,(x,y),xytext=(dx,dy),textcoords="offset points",ha=ha,va=va,fontsize=8,zorder=6);best=(t,t.get_window_extent(R))
    placed.append(best[1])
ax.set_title("MapTap – ubicaciones de EE.UU. que salieron (64 rondas, 62 lugares)",fontsize=14)
fig.savefig("/sessions/trusting-nice-davinci/mnt/Maptap/graficos/maptap-mapa-usa.png",bbox_inches="tight")
print(len(polys),len(pos))
