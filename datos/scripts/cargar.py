"""Carga directa a las tablas de datos/ (CSV = fuente de verdad). Idempotente: lo repetido se ignora.
Uso desde python:  import cargar as c
  c.dia('2026-10-19', [(lat,lng,'Nombre en maptap.gg')]*5, manual={'Nombre': ['Ciudad costera', ...]})
  c.partida('2026-10-19','Toker',[95,100,99,92,95],954)
  c.challenge('2026-10-19','Toker',943,24.9)
  c.cerrar('2026-10-19')
  c.reconstruir()    # regenera maptap.db y valida
"""
import pandas as pd, datetime
from config import *
import reglas
from reglas import auto_categorias,dist_ba,dist_costa,dist_rio,dist_lago,dist_volcan,n_sismos,dist_unesco
_src=open("geo.py",encoding="utf8").read().split("rows=[]")[0];_ns={};exec(_src,_ns);classify=_ns["classify"];CONT=_ns["CONT"]
def _r(n): return pd.read_csv(DD+n+".csv")
def _w(n,df): df.to_csv(DD+n+".csv",index=False)
def _jug():
    j=_r("dim_jugador");return dict(zip(j.alias,j.id_jugador))
def dia(fecha,ubic,manual=None,es=None):
    """Alta de un dia: 5 ubicaciones (lat,lng,nombre) en orden de ronda. Lugares nuevos exigen su rotulado manual."""
    assert len(ubic)==5,"un dia tiene 5 ubicaciones"
    ap=_r("fact_aparicion")
    if (ap.fecha==fecha).any(): print("dia ya cargado",fecha);return False
    lug=_r("dim_lugar");cat=_r("dim_categoria");pu=_r("puente_lugar_categoria");manual=manual or {};es=es or {}
    cid=dict(zip(cat.categoria,cat.id_categoria));new=[]
    for i,(la,lo,n) in enumerate(ubic,1):
        canon=ALIAS.get(n,n);sl=slug(canon);hit=lug[lug.slug==sl]
        if len(hit):
            idl=int(hit.id_lugar.iloc[0])
        else:
            if canon not in manual: raise ValueError(f"Lugar nuevo '{canon}': falta su rotulado manual en manual={{...}} (categorias disponibles: {reglas.MANUAL})")
            if canon not in es: raise ValueError(f"Lugar nuevo '{canon}': falta su nombre en castellano en es={{...}} (nombre completo, p. ej. 'Ciudad del Cabo, Sudáfrica')")
            pais,reg=classify(canon);cont=CONT[reg]
            idl=int(lug.id_lugar.max())+1 if len(lug) else 1
            lug=pd.concat([lug,pd.DataFrame([dict(id_lugar=idl,slug=sl,lugar=es[canon],pais=pais,region=reg,continente=cont,lat=la,lon=lo,dist_buenos_aires_km=round(dist_ba(la,lo)),dist_costa_km=round(dist_costa(la,lo),1),dist_rio_km=dist_rio(la,lo)[0],rio_cercano=dist_rio(la,lo)[1],dist_lago_km=dist_lago(la,lo)[0],lago_cercano=dist_lago(la,lo)[1],dist_volcan_km=dist_volcan(la,lo)[0],volcan_cercano=dist_volcan(la,lo)[1],altitud_m=None,n_sismos_m7_100km=n_sismos(la,lo),dist_unesco_km=dist_unesco(la,lo)[0],sitio_unesco=dist_unesco(la,lo)[1],fundacion_anio=None)])],ignore_index=True)
            cs=auto_categorias(pais,la,lo,manual[canon])
            pu=pd.concat([pu,pd.DataFrame([dict(id_lugar=idl,id_categoria=cid[c]) for c in sorted(cs)])],ignore_index=True)
            new.append(canon)
        ap=pd.concat([ap,pd.DataFrame([dict(id_ubicacion=f"{fecha.replace('-','')}-{i}",fecha=fecha,ronda=i,id_lugar=idl)])],ignore_index=True)
    f=_r("dim_fecha");t=pd.Timestamp(fecha)
    f=pd.concat([f,pd.DataFrame([dict(fecha=fecha,dia_cerrado=0,anio_mes=t.strftime("%Y-%m"),dia_semana=["lunes","martes","miercoles","jueves","viernes","sabado","domingo"][t.dayofweek],semana_inicio=(t-pd.Timedelta(days=t.dayofweek)).strftime("%Y-%m-%d"),es_profesional=int(fecha>=CORTE_PRO))])],ignore_index=True).sort_values("fecha")
    _w("dim_lugar",lug);_w("puente_lugar_categoria",pu.drop_duplicates());_w("fact_aparicion",ap.sort_values("id_ubicacion"));_w("dim_fecha",f)
    print("dia cargado",fecha,"| lugares nuevos:",new or "ninguno");return True
def partida(fecha,alias,rondas,final):
    j=_jug();assert alias in j,f"jugador desconocido {alias}";assert len(rondas)==5 and all(0<=x<=100 for x in rondas)
    ap=_r("fact_aparicion");assert (ap.fecha==fecha).any(),f"primero cargar las ubicaciones del dia {fecha}"
    pt=_r("fact_partida")
    if ((pt.fecha==fecha)&(pt.id_jugador==j[alias])).any(): print("partida repetida, ignorada",fecha,alias);return False
    fp=_r("fact_puntaje");ids=[f"{fecha.replace('-','')}-{i}" for i in range(1,6)]
    fp=pd.concat([fp,pd.DataFrame([dict(id_ubicacion=u,id_jugador=j[alias],puntaje=int(s)) for u,s in zip(ids,rondas)])],ignore_index=True).sort_values(["id_ubicacion","id_jugador"])
    pt=pd.concat([pt,pd.DataFrame([dict(fecha=fecha,id_jugador=j[alias],puntaje_final=int(final),suma_rondas=int(sum(rondas)))])],ignore_index=True).sort_values(["fecha","id_jugador"])
    _w("fact_puntaje",fp);_w("fact_partida",pt);print("partida cargada",fecha,alias,final);return True
def challenge(fecha,alias,puntaje,tiempo,suma=None,rondas=None):
    """rondas = [r1..r5] del Challenge (se guardan en fact_challenge_ronda; el puntaje debe cerrar con ponderacion 1,1,2,3,3 y la suma sale de ahi)."""
    j=_jug();assert alias in j;assert (_r("dim_fecha").fecha==fecha).any(),"el dia no existe en dim_fecha: cargarlo primero con dia()"
    if rondas is not None:
        assert len(rondas)==5 and rondas[0]+rondas[1]+2*rondas[2]+3*rondas[3]+3*rondas[4]==puntaje,f"rondas no cierran con el puntaje {fecha} {alias} {rondas} {puntaje}"
        suma=int(sum(rondas))
    ch=_r("fact_challenge")
    if ((ch.fecha==fecha)&(ch.id_jugador==j[alias])).any():
        if rondas is not None: _guardar_rondas(fecha,alias,rondas)
        print("challenge repetido, ignorado",fecha,alias);return False
    ch=pd.concat([ch,pd.DataFrame([dict(fecha=fecha,id_jugador=j[alias],posicion=99,puntaje=int(puntaje),tiempo_s=float(tiempo),suma_rondas=suma)])],ignore_index=True)
    ch=_pos(ch,fecha);_w("fact_challenge",ch)
    if rondas is not None: _guardar_rondas(fecha,alias,rondas)
    print("challenge cargado",fecha,alias,puntaje);return True
def _guardar_rondas(fecha,alias,rondas):
    """Guarda las 5 rondas del Challenge y completa suma_rondas si faltaba (no pisa otras)."""
    j=_jug()[alias];import os
    rn=_r("fact_challenge_ronda") if os.path.exists(DD+"fact_challenge_ronda.csv") else pd.DataFrame(columns=["fecha","id_jugador","ronda","puntaje"])
    rn=rn[~((rn.fecha==fecha)&(rn.id_jugador==j))]
    rn=pd.concat([rn,pd.DataFrame([dict(fecha=fecha,id_jugador=j,ronda=i,puntaje=int(x)) for i,x in enumerate(rondas,1)])],ignore_index=True).sort_values(["fecha","id_jugador","ronda"])
    _w("fact_challenge_ronda",rn)
    ch=_r("fact_challenge");m=(ch.fecha==fecha)&(ch.id_jugador==j)
    if m.any() and ch.loc[m,"suma_rondas"].isna().all(): ch.loc[m,"suma_rondas"]=int(sum(rondas));ch=_pos(ch,fecha);_w("fact_challenge",ch)
def _pos(ch,fecha):
    m=ch.fecha==fecha;sub=ch[m].copy();sub["_o"]=range(len(sub))
    sub=sub.assign(_s=sub.get("suma_rondas",pd.Series(0,index=sub.index)).fillna(-1)).sort_values(["puntaje","_s","posicion","_o"],ascending=[False,False,True,True]).drop(columns="_s");sub["posicion"]=range(1,len(sub)+1)
    return pd.concat([ch[~m],sub.drop(columns="_o")]).sort_values(["fecha","posicion"]).reset_index(drop=True)
def desempate_challenge(fecha,orden):
    """Si dos Challenge empatan en puntaje: pasar el orden final de aliases, ej. ['Toker','Axel',...]"""
    j=_jug();ch=_r("fact_challenge");m=ch.fecha==fecha
    pos={j[a]:i for i,a in enumerate(orden,1)};ch.loc[m,"posicion"]=ch[m].id_jugador.map(pos);ch=ch.sort_values(["fecha","posicion"]);_w("fact_challenge",ch);print("orden challenge",fecha,orden)
# ausencias eximidas (no bajan de categoria; el contador de ausencias de la tabla no se toca): (fecha, alias)
EXIMIDOS = {("2026-10-20", "Martín")}


def calc_divisiones(fecha):
    """Reglas: ausencia en dia cerrado o puntaje < 800 -> baja una categoria; puntaje > 940 -> sube una (no si ya es 1a)."""
    dv=_r("fact_division");prev=dv[dv.fecha<fecha]
    assert len(prev),"no hay divisiones previas"
    last=prev[prev.fecha==prev.fecha.max()].set_index("id_jugador").division.to_dict()
    pt=_r("fact_partida");pt=pt[pt.fecha==fecha].set_index("id_jugador").puntaje_final.to_dict();out={};ev=[]
    for jid,d in last.items():
        s=pt.get(jid)
        if s is None and (fecha,{v:k for k,v in _jug().items()}[jid]) in EXIMIDOS: nd=d;ev.append((jid,"ausencia eximida",d,nd))
        elif s is None: nd=d+1;ev.append((jid,"ausencia",d,nd))
        elif s<800: nd=d+1;ev.append((jid,"puntaje bajo",d,nd))
        elif s>940 and d>1: nd=d-1;ev.append((jid,"ascenso",d,nd))
        else: nd=d
        out[jid]=nd
    return out,ev
def cerrar(fecha):
    f=_r("dim_fecha");assert (f.fecha==fecha).any();f.loc[f.fecha==fecha,"dia_cerrado"]=1;_w("dim_fecha",f);print("dia cerrado",fecha)
    dv=_r("fact_division")
    if (dv.fecha==fecha).any(): return
    new,ev=calc_divisiones(fecha);al={v:k for k,v in _jug().items()}
    dv=pd.concat([dv,pd.DataFrame([dict(fecha=fecha,id_jugador=j,division=d) for j,d in new.items()])],ignore_index=True).sort_values(["fecha","id_jugador"]);_w("fact_division",dv)
    print("divisiones al cierre:",{al[j]:d for j,d in new.items()});print("movimientos:",[(al[j],m,a,b) for j,m,a,b in ev] or "ninguno")
def reconstruir():
    import build_db
