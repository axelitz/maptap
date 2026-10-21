"""Una sola vez: reemplaza las coordenadas aproximadas de dim_lugar por las exactas de maptap.gg (primera aparicion)."""
import pandas as pd, numpy as np
from config import *
from reglas import dist_ba
ex={}
for l in open("coords_exact.txt",encoding="utf8"):
    k,v=l.rstrip("\n").split("#");mm,dd=k.split("-")
    for i,it in enumerate(v.split(";"),1):
        la,lo,n=it.split("|",2);ex[f"2026{mm}{dd}-{i}"]=(float(la),float(lo))
ap=pd.read_csv(DD+"fact_aparicion.csv").sort_values("id_ubicacion");lug=pd.read_csv(DD+"dim_lugar.csv")
first=ap.drop_duplicates("id_lugar").set_index("id_lugar").id_ubicacion
lug["lat"]=lug.id_lugar.map(lambda i:ex[first[i]][0]);lug["lon"]=lug.id_lugar.map(lambda i:ex[first[i]][1])
lug["dist_buenos_aires_km"]=[round(dist_ba(a,b)) for a,b in zip(lug.lat,lug.lon)]
# control: variacion entre apariciones del mismo lugar
ap["lat"]=ap.id_ubicacion.map(lambda x:ex[x][0]);ap["lon"]=ap.id_ubicacion.map(lambda x:ex[x][1])
print("max dispersion entre apariciones (km):",round(ap.groupby("id_lugar").agg(a=("lat","max"),b=("lat","min"),c=("lon","max"),d=("lon","min")).pipe(lambda g:np.hypot((g.a-g.b)*111,(g.c-g.d)*111)).max(),1))
lug.to_csv(DD+"dim_lugar.csv",index=False);print(len(lug))
