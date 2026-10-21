"""Genera una version de PRUEBA de la presentacion con datos ficticios (para mostrarla a otras personas).
Copia maptap.db, cambia nombres de jugadores, mezcla y perturba puntajes, y vuelve a calcular puntajes finales, Challenge y divisiones.
Uso: python3 generar_demo.py [--hasta AAAA-MM-DD]   ->  salida/presentacion-demo.html"""
import sqlite3, shutil, random, pathlib, subprocess, sys

AQUI = pathlib.Path(__file__).resolve().parent
SAL = AQUI / "salida"
SAL.mkdir(exist_ok=True)
dst = SAL / "maptap_demo.db"
shutil.copy(AQUI.parent / "maptap.db", dst)
con = sqlite3.connect(dst)
rnd = random.Random(2026)
PESO = {1: 1, 2: 1, 3: 2, 4: 3, 5: 3}
FALSOS = ["Ana", "Beto", "Carla", "Diego", "Eli", "Fran", "Gaby", "Hugo", "Iris", "Juan", "Kari", "Lalo", "Mica"]
ids = [r[0] for r in con.execute("SELECT id_jugador FROM dim_jugador ORDER BY id_jugador")]
nombres = FALSOS[:]
rnd.shuffle(nombres)
for i, n in zip(ids, nombres):
    con.execute("UPDATE dim_jugador SET alias=?, nombre=? WHERE id_jugador=?", (n, n, i))
# puntajes por ronda: se mezclan entre jugadores en cada ubicacion y se perturban
for (idu,) in con.execute("SELECT DISTINCT id_ubicacion FROM fact_puntaje").fetchall():
    filas = con.execute("SELECT id_jugador, puntaje FROM fact_puntaje WHERE id_ubicacion=?", (idu,)).fetchall()
    vals = [p for _, p in filas]
    rnd.shuffle(vals)
    for (j, _), v in zip(filas, vals):
        nuevo = max(0, min(100, round(v + rnd.gauss(0, 5))))
        con.execute("UPDATE fact_puntaje SET puntaje=? WHERE id_ubicacion=? AND id_jugador=?", (nuevo, idu, j))
# partidas: se recalculan a partir de las rondas con los multiplicadores reales
for fecha, j in con.execute("SELECT fecha, id_jugador FROM fact_partida").fetchall():
    r = con.execute("SELECT a.ronda, s.puntaje FROM fact_puntaje s JOIN fact_aparicion a USING(id_ubicacion) WHERE a.fecha=? AND s.id_jugador=?", (fecha, j)).fetchall()
    con.execute("UPDATE fact_partida SET suma_rondas=?, puntaje_final=? WHERE fecha=? AND id_jugador=?", (sum(p for _, p in r), sum(PESO[k] * p for k, p in r), fecha, j))
# challenge: se reparten al azar los resultados entre jugadores de cada dia
for (fecha,) in con.execute("SELECT DISTINCT fecha FROM fact_challenge").fetchall():
    js = [r[0] for r in con.execute("SELECT id_jugador FROM fact_challenge WHERE fecha=?", (fecha,))]
    mezcla = js[:]
    rnd.shuffle(mezcla)
    for a, b in zip(js, mezcla):
        con.execute("UPDATE fact_challenge SET id_jugador=-? WHERE fecha=? AND id_jugador=?", (b, fecha, a))
    con.execute("UPDATE fact_challenge SET id_jugador=-id_jugador WHERE fecha=? AND id_jugador<0", (fecha,))
# divisiones: se recalculan con las reglas sobre los puntajes ficticios
dias = [r[0] for r in con.execute("SELECT fecha FROM dim_fecha WHERE es_profesional=1 AND dia_cerrado=1 ORDER BY fecha")]
div = {i: 1 for i in ids}
con.execute("DELETE FROM fact_division")
for f in dias:
    pt = dict(con.execute("SELECT id_jugador, puntaje_final FROM fact_partida WHERE fecha=?", (f,)).fetchall())
    for i in ids:
        s_ = pt.get(i)
        if s_ is None or s_ < 800:
            div[i] += 1
        elif s_ > 940 and div[i] > 1:
            div[i] -= 1
        con.execute("INSERT INTO fact_division(fecha,id_jugador,division) VALUES (?,?,?)", (f, i, div[i]))
con.commit()
con.close()
print("base ficticia lista:", dst.name)
sys.exit(subprocess.call([sys.executable, str(AQUI / "generar.py"), "--demo"] + sys.argv[1:]))
