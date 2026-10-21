"""Reconstruye fact_division desde el 1er dia profesional aplicando las reglas. Uso unico (historia); luego cerrar() mantiene la tabla.
Anulaciones por la resolucion del 29/9 (Martin: ausencias 19/9, 24/9, 28/9). Verificada contra las fotos 14/10-18/10."""
import pandas as pd, os
DD=os.environ.get("MAPTAP_DATOS", os.path.join(os.path.dirname(__file__),"..")).rstrip("/")+"/"
ANUL={("2026-09-19","Martín"),("2026-09-24","Martín"),("2026-09-28","Martín"),("2026-10-20","Martín")}
f=pd.read_csv(DD+"dim_fecha.csv");p=pd.read_csv(DD+"fact_partida.csv");j=pd.read_csv(DD+"dim_jugador.csv");old=pd.read_csv(DD+"fact_division.csv")
al=dict(zip(j.id_jugador,j.alias));d={i:1 for i in al};rows=[]
for fe in f[(f.es_profesional==1)&(f.dia_cerrado==1)].fecha:
    pt=p[p.fecha==fe].set_index("id_jugador").puntaje_final.to_dict()
    for i in d:
        s=pt.get(i)
        if s is None:
            if (fe,al[i]) not in ANUL: d[i]+=1
        elif s<800: d[i]+=1
        elif s>940 and d[i]>1: d[i]-=1
    rows+= [dict(fecha=fe,id_jugador=i,division=v) for i,v in d.items()]
new=pd.DataFrame(rows)
m=old.merge(new,on=["fecha","id_jugador"],suffixes=("_o","_n"));assert (m.division_o==m.division_n).all(),"no coincide con fotos existentes"
new.sort_values(["fecha","id_jugador"]).to_csv(DD+"fact_division.csv",index=False);print("filas",len(new))
