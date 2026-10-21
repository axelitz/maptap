import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
O="/sessions/trusting-nice-davinci/mnt/outputs/"
co={}
for l in open(O+"coords.txt",encoding="utf8"):
    n,a,b=l.rstrip("\n").split("|");co[n]=(float(a),float(b))
d=pd.read_csv("/sessions/trusting-nice-davinci/mnt/Maptap/maptap-ubicaciones-flags.csv")
u=d
miss=set(u.lugar)-set(co);print("faltan",miss)
def eq(lon,lat):
    lam=np.radians(lon);ph=np.radians(lat)
    t=np.arcsin(np.sqrt(3)/2*np.sin(ph));A1,A2,A3,A4=1.340264,-0.081106,0.000893,0.003796
    x=2*np.sqrt(3)*lam*np.cos(t)/(3*(9*A4*t**8+7*A3*t**6+3*A2*t**3+A1))
    y=t*(A1+A2*t**2+t**6*(A3+A4*t**2))
    return x,y
fig,ax=plt.subplots(figsize=(18,9.5),dpi=130)
bx,by=eq(np.linspace(-180,180,200),np.zeros(200))
# outline of globe
lat=np.linspace(-90,90,200);xl,yl=eq(-180*np.ones(200),lat);xr,yr=eq(180*np.ones(200),lat)
ax.add_patch(Polygon(np.r_[np.c_[xl,yl],np.c_[xr,yr][::-1]],fc="#dbe9f5",ec="#9db2c6",lw=1))
for ring in open(O+"land.txt").read().strip().split("|"):
    p=np.array([[float(v) for v in q.split(",")] for q in ring.split()])
    jumps=[i for i in range(1,len(p)) if abs(p[i,0]-p[i-1,0])>180]
    parts=[p] if not jumps else [p[:jumps[0]],p[jumps[0]:]]
    if jumps:
        a,b=parts
        # a ends near -180 or 180; b ends at the ring start: put its last point on the proper edge
        edge=np.sign(b[0,0])*180
        b[-1,0]=edge if abs(b[-1,0])==180 else b[-1,0]
        if abs(a[0,0])==180: a[0,0]=np.sign(a[-1,0])*180
        parts=[a,b]
    for q in parts:
        x,y=eq(q[:,0],q[:,1]);ax.add_patch(Polygon(np.c_[x,y],fc="#f1efe6",ec="#a9a79b",lw=0.5))
cols={"América del Norte":"#e03131","Centroamérica":"#f08c00","América del Sur":"#2f9e44","Europa":"#1c7ed6","Asia":"#ae3ec9","África":"#e8590c","Oceanía":"#0ca678","Antártida":"#495057"}
cont=u.drop_duplicates("lugar").set_index("lugar").continente
cnt=u.groupby("lugar").size()
for c,colr in cols.items():
    ls=[l for l in cont.index if cont[l]==c]
    pts=np.array([co[l][::-1] for l in ls]);x,y=eq(pts[:,0],pts[:,1])
    ax.scatter(x,y,s=[22+14*(cnt[l]-1) for l in ls],c=colr,ec="white",lw=0.6,alpha=0.9,zorder=5,label=f"{c} ({len(ls)})")
ax.set_aspect("equal");ax.axis("off")
ax.legend(loc="lower left",fontsize=10,frameon=True,title=f"{len(cont)} lugares distintos · {len(u)} rondas")
ax.set_title("MapTap – ubicaciones que salieron (22/7 al 17/10/2026)",fontsize=15)
fig.savefig("/sessions/trusting-nice-davinci/mnt/Maptap/graficos/maptap-mapa-mundial.png",bbox_inches="tight")
