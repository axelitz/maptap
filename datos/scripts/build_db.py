"""Carga los CSV de datos/ (fuente de verdad) a SQLite, valida claves y consistencia, y crea las vistas.
No deriva nada de los md ni de los exports de chat: todo se agrega con cargar.py."""
import sqlite3, shutil, os
import pandas as pd
from config import *
import os
T=["dim_jugador","dim_fecha","dim_lugar","dim_categoria","puente_lugar_categoria","fact_aparicion","fact_puntaje","fact_partida","fact_challenge","fact_division"]
t={n:pd.read_csv(DD+n+".csv") for n in T}
jug,fec,lug,cat,pu,ap,fp,pt,ch,dv=[t[n] for n in T]
pais_=pd.read_csv(DD+"dim_pais.csv")
_u=cat[cat.slug=="unica-aparicion"].id_categoria
if len(_u):
    _u=int(_u.iloc[0]);pu=pu[pu.id_categoria!=_u];_n=lug.groupby("pais").id_lugar.transform("count")
    pu=pd.concat([pu,pd.DataFrame({"id_lugar":lug[_n==1].id_lugar,"id_categoria":_u})],ignore_index=True);t["puente_lugar_categoria"]=pu
assert set(lug.pais)-set(pais_.pais)<={"Sin país (Antártida)","Sin país (Atlántico Norte)"},f"paises sin clase de ingreso: {set(lug.pais)-set(pais_.pais)}"
chr_=pd.read_csv(DD+"fact_challenge_ronda.csv") if os.path.exists(DD+"fact_challenge_ronda.csv") else pd.DataFrame(columns=["fecha","id_jugador","ronda","puntaje"])
# ---- controles de integridad
def uniq(df,cols,n): assert not df.duplicated(cols).any(),f"clave duplicada en {n}: {df[df.duplicated(cols,keep=False)].head(3).to_dict('records')}"
for n,cols in [("dim_jugador",["id_jugador"]),("dim_fecha",["fecha"]),("dim_lugar",["id_lugar"]),("dim_categoria",["id_categoria"]),("puente_lugar_categoria",["id_lugar","id_categoria"]),("fact_aparicion",["id_ubicacion"]),("fact_puntaje",["id_ubicacion","id_jugador"]),("fact_partida",["fecha","id_jugador"]),("fact_challenge",["fecha","id_jugador"]),("fact_division",["fecha","id_jugador"])]: uniq(t[n],cols,n)
uniq(lug,["slug"],"dim_lugar.slug");uniq(cat,["slug"],"dim_categoria.slug");uniq(ap,["fecha","ronda"],"fact_aparicion(fecha,ronda)");uniq(ch,["fecha","posicion"],"fact_challenge(fecha,posicion)")
assert ap.id_lugar.isin(lug.id_lugar).all() and ap.fecha.isin(fec.fecha).all(),"FK fact_aparicion"
assert pu.id_lugar.isin(lug.id_lugar).all() and pu.id_categoria.isin(cat.id_categoria).all(),"FK puente"
assert fp.id_ubicacion.isin(ap.id_ubicacion).all() and fp.id_jugador.isin(jug.id_jugador).all(),"FK fact_puntaje"
assert pt.fecha.isin(fec.fecha).all() and pt.id_jugador.isin(jug.id_jugador).all(),"FK fact_partida"
assert ch.fecha.isin(fec.fecha).all() and ch.id_jugador.isin(jug.id_jugador).all(),"FK fact_challenge"
assert dv.fecha.isin(fec.fecha).all() and dv.id_jugador.isin(jug.id_jugador).all() and (dv.division>=1).all(),"FK/valor fact_division"
assert (dv.groupby("fecha").size()==len(jug)).all(),"cada snapshot de divisiones debe tener a los 11 jugadores"
assert (ap.groupby("fecha").size()==5).all(),"cada fecha debe tener 5 rondas"
assert lug.id_lugar.isin(ap.id_lugar).all(),"lugar sin ninguna aparicion"
assert (fp.merge(ap[["id_ubicacion","fecha"]],on="id_ubicacion").groupby(["fecha","id_jugador"]).size()==5).all(),"toda partida debe tener 5 puntajes"
chk=fp.merge(ap[["id_ubicacion","fecha"]],on="id_ubicacion").groupby(["fecha","id_jugador"]).puntaje.sum().reset_index().merge(pt,on=["fecha","id_jugador"],how="outer",indicator=True)
assert (chk._merge=="both").all(),"partida sin puntajes o puntajes sin partida"
assert (chk.puntaje==chk.suma_rondas).all(),"suma_rondas no coincide con los puntajes"
assert (fec.es_profesional==(fec.fecha>=CORTE_PRO).astype(int)).all(),"es_profesional no respeta el corte"
assert lug.groupby("lugar").size().max()==1
# ---- SQLite
tmp="/tmp/maptap.db"
if os.path.exists(tmp): os.remove(tmp)
c=sqlite3.connect(tmp);c.execute("PRAGMA foreign_keys=ON")
c.executescript("""
CREATE TABLE dim_jugador(id_jugador INTEGER PRIMARY KEY, nombre TEXT NOT NULL UNIQUE, alias TEXT NOT NULL UNIQUE);
CREATE TABLE dim_fecha(fecha TEXT PRIMARY KEY, dia_cerrado INTEGER NOT NULL CHECK(dia_cerrado IN (0,1)), anio_mes TEXT NOT NULL, dia_semana TEXT NOT NULL, semana_inicio TEXT NOT NULL, es_profesional INTEGER NOT NULL CHECK(es_profesional IN (0,1)));
CREATE TABLE dim_lugar(id_lugar INTEGER PRIMARY KEY, slug TEXT NOT NULL UNIQUE, lugar TEXT NOT NULL, pais TEXT NOT NULL, region TEXT NOT NULL, continente TEXT NOT NULL, lat REAL NOT NULL, lon REAL NOT NULL, dist_buenos_aires_km INTEGER NOT NULL, dist_costa_km REAL NOT NULL, rio_cercano TEXT, dist_rio_km REAL, dist_lago_km REAL, lago_cercano TEXT, dist_volcan_km REAL, volcan_cercano TEXT, altitud_m REAL, n_sismos_m7_100km INTEGER, dist_unesco_km REAL, sitio_unesco TEXT, fundacion_anio INTEGER);
CREATE TABLE dim_categoria(id_categoria INTEGER PRIMARY KEY, slug TEXT NOT NULL UNIQUE, categoria TEXT NOT NULL, tipo TEXT NOT NULL, descripcion TEXT);
CREATE TABLE puente_lugar_categoria(id_lugar INTEGER NOT NULL REFERENCES dim_lugar, id_categoria INTEGER NOT NULL REFERENCES dim_categoria, PRIMARY KEY(id_lugar,id_categoria)) WITHOUT ROWID;
CREATE TABLE fact_aparicion(id_ubicacion TEXT PRIMARY KEY, fecha TEXT NOT NULL REFERENCES dim_fecha, ronda INTEGER NOT NULL CHECK(ronda BETWEEN 1 AND 5), id_lugar INTEGER NOT NULL REFERENCES dim_lugar, UNIQUE(fecha,ronda));
CREATE TABLE fact_puntaje(id_ubicacion TEXT NOT NULL REFERENCES fact_aparicion, id_jugador INTEGER NOT NULL REFERENCES dim_jugador, puntaje INTEGER NOT NULL CHECK(puntaje BETWEEN 0 AND 100), PRIMARY KEY(id_ubicacion,id_jugador)) WITHOUT ROWID;
CREATE TABLE fact_partida(fecha TEXT NOT NULL REFERENCES dim_fecha, id_jugador INTEGER NOT NULL REFERENCES dim_jugador, puntaje_final INTEGER NOT NULL, suma_rondas INTEGER NOT NULL, PRIMARY KEY(fecha,id_jugador)) WITHOUT ROWID;
CREATE TABLE dim_pais(iso3 TEXT PRIMARY KEY, pais TEXT NOT NULL UNIQUE, clase_bm TEXT NOT NULL CHECK(clase_bm IN ('HIC','UMC','LMC','LIC')), nivel_ingreso TEXT NOT NULL CHECK(nivel_ingreso IN ('alto','medio','bajo')), inb_pc_usd INTEGER, monarquia INTEGER NOT NULL DEFAULT 0, otan INTEGER NOT NULL DEFAULT 0, liga_arabe INTEGER NOT NULL DEFAULT 0, opep INTEGER NOT NULL DEFAULT 0, g7 INTEGER NOT NULL DEFAULT 0, brics INTEGER NOT NULL DEFAULT 0, commonwealth INTEGER NOT NULL DEFAULT 0);
CREATE TABLE fact_challenge_ronda(fecha TEXT NOT NULL, id_jugador INTEGER NOT NULL, ronda INTEGER NOT NULL CHECK(ronda BETWEEN 1 AND 5), puntaje INTEGER NOT NULL, PRIMARY KEY(fecha,id_jugador,ronda), FOREIGN KEY(fecha,id_jugador) REFERENCES fact_challenge) WITHOUT ROWID;
CREATE TABLE fact_challenge(fecha TEXT NOT NULL REFERENCES dim_fecha, id_jugador INTEGER NOT NULL REFERENCES dim_jugador, posicion INTEGER NOT NULL, puntaje INTEGER NOT NULL, tiempo_s REAL NOT NULL, suma_rondas INTEGER, PRIMARY KEY(fecha,id_jugador)) WITHOUT ROWID;
CREATE TABLE fact_division(fecha TEXT NOT NULL REFERENCES dim_fecha, id_jugador INTEGER NOT NULL REFERENCES dim_jugador, division INTEGER NOT NULL CHECK(division>=1), PRIMARY KEY(fecha,id_jugador)) WITHOUT ROWID;
CREATE INDEX ix_ap_lugar ON fact_aparicion(id_lugar);
CREATE INDEX ix_ap_fecha ON fact_aparicion(fecha);
CREATE INDEX ix_pt_jugador ON fact_puntaje(id_jugador);
CREATE INDEX ix_pte_cat ON puente_lugar_categoria(id_categoria,id_lugar);
""")
for n in T: t[n].to_sql(n,c,if_exists="append",index=False)
chr_.to_sql("fact_challenge_ronda",c,if_exists="append",index=False)
pais_.to_sql("dim_pais",c,if_exists="append",index=False)
flags=",\n".join(f"MAX(CASE WHEN p.id_categoria={int(r.id_categoria)} THEN 1 ELSE 0 END) AS c_{r.slug.replace('-','_')}" for r in cat.itertuples())
c.executescript(f"""
CREATE VIEW v_puntaje AS
 SELECT s.id_ubicacion, a.fecha, a.ronda, f.es_profesional, f.semana_inicio, f.anio_mes, j.alias AS jugador, s.puntaje,
        l.id_lugar, l.lugar, l.pais, l.region, l.continente, l.lat, l.lon
 FROM fact_puntaje s JOIN fact_aparicion a USING(id_ubicacion) JOIN dim_fecha f ON f.fecha=a.fecha
 JOIN dim_jugador j USING(id_jugador) JOIN dim_lugar l USING(id_lugar);
CREATE VIEW v_puntaje_categoria AS
 SELECT v.*, c.id_categoria, c.categoria FROM v_puntaje v
 JOIN puente_lugar_categoria p USING(id_lugar) JOIN dim_categoria c USING(id_categoria);
CREATE VIEW v_promedio_categoria AS
 SELECT categoria, jugador, es_profesional, COUNT(*) AS n_rondas, ROUND(AVG(puntaje),3) AS promedio
 FROM v_puntaje_categoria GROUP BY categoria, jugador, es_profesional;
CREATE VIEW v_challenge_dia AS
 SELECT c.fecha, CASE WHEN c.fecha>='{CORTE_CHALLENGE_PRO}' THEN 1 ELSE 0 END AS es_profesional, f.dia_cerrado, COUNT(*) AS n_participantes,
        CASE WHEN COUNT(*)>=5 AND f.dia_cerrado=1 THEN 1 ELSE 0 END AS titulo_valido,
        (SELECT j.alias FROM fact_challenge x JOIN dim_jugador j USING(id_jugador) WHERE x.fecha=c.fecha AND x.posicion=1) AS campeon
 FROM fact_challenge c JOIN dim_fecha f USING(fecha) GROUP BY c.fecha;
CREATE VIEW v_titulos_challenge AS
 SELECT j.alias AS jugador,
        SUM(CASE WHEN c.posicion=1 THEN 1 ELSE 0 END) AS titulos,
        SUM(CASE WHEN c.posicion=2 THEN 1 ELSE 0 END) AS segundos,
        SUM(CASE WHEN c.posicion=3 THEN 1 ELSE 0 END) AS terceros,
        COUNT(*) AS dias_validos_jugados
 FROM fact_challenge c JOIN v_challenge_dia d USING(fecha) JOIN dim_jugador j USING(id_jugador)
 WHERE d.titulo_valido=1 AND d.es_profesional=1 GROUP BY j.alias ORDER BY titulos DESC, segundos DESC, terceros DESC;
CREATE VIEW v_titulos_challenge_amateur AS
 SELECT j.alias AS jugador,
        SUM(CASE WHEN c.posicion=1 THEN 1 ELSE 0 END) AS titulos,
        SUM(CASE WHEN c.posicion=2 THEN 1 ELSE 0 END) AS segundos,
        SUM(CASE WHEN c.posicion=3 THEN 1 ELSE 0 END) AS terceros,
        COUNT(*) AS dias_validos_jugados
 FROM fact_challenge c JOIN v_challenge_dia d USING(fecha) JOIN dim_jugador j USING(id_jugador)
 WHERE d.titulo_valido=1 AND d.es_profesional=0 GROUP BY j.alias ORDER BY titulos DESC, segundos DESC, terceros DESC;
CREATE VIEW v_division_actual AS
 SELECT j.alias AS jugador, d.division, d.fecha AS al_cierre_del FROM fact_division d JOIN dim_jugador j USING(id_jugador)
 WHERE d.fecha=(SELECT MAX(fecha) FROM fact_division) ORDER BY d.division, j.alias;
CREATE VIEW v_ranking_dia AS
 SELECT p.fecha, j.alias AS jugador, p.puntaje_final, p.suma_rondas,
        RANK() OVER (PARTITION BY p.fecha ORDER BY p.puntaje_final DESC, p.suma_rondas DESC) AS posicion
 FROM fact_partida p JOIN dim_jugador j USING(id_jugador);
CREATE VIEW v_copa_semanal AS
 SELECT f.semana_inicio, j.alias AS jugador, SUM(p.puntaje_final) AS puntos, COUNT(*) AS dias_jugados
 FROM fact_partida p JOIN dim_fecha f USING(fecha) JOIN dim_jugador j USING(id_jugador)
 WHERE f.dia_cerrado=1 GROUP BY f.semana_inicio, j.alias;
CREATE VIEW v_medallero_mes AS
 SELECT f.anio_mes, r.jugador,
        SUM(r.posicion=1) AS oros, SUM(r.posicion=2) AS platas, SUM(r.posicion=3) AS bronces,
        ROUND(AVG(r.puntaje_final),1) AS promedio, COUNT(*) AS dias_jugados
 FROM v_ranking_dia r JOIN dim_fecha f USING(fecha) WHERE f.dia_cerrado=1 GROUP BY f.anio_mes, r.jugador;
CREATE VIEW v_lugar_flags AS
 SELECT l.id_lugar, l.lugar, {flags}
 FROM dim_lugar l LEFT JOIN puente_lugar_categoria p USING(id_lugar) GROUP BY l.id_lugar;
""")
assert c.execute("PRAGMA foreign_key_check").fetchall()==[]
c.commit();c.execute("VACUUM");c.close()
shutil.copyfile(tmp,DD+"maptap.db")
print("OK",{n:len(t[n]) for n in T})
