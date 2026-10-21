"""Ejecuta el sql de cada metrica de metricas.yaml contra datos/maptap.db y reporta filas o errores.
Uso: python3 validar_metricas.py [--hasta AAAA-MM-DD]"""
import sqlite3, sys, json, yaml, pathlib

aqui = pathlib.Path(__file__).resolve().parent
db = aqui.parent / "maptap.db"
con = sqlite3.connect(db)
hasta = sys.argv[sys.argv.index("--hasta") + 1] if "--hasta" in sys.argv else \
    con.execute("SELECT MAX(fecha) FROM dim_fecha WHERE dia_cerrado=1").fetchone()[0]
mets = yaml.safe_load(open(aqui / "metricas.yaml", encoding="utf-8"))
req = ["id", "nombre", "seccion", "definicion", "calculo"]
fallas = 0
print(f"hasta={hasta}  metricas={len(mets)}")
for m in mets:
    faltan = [k for k in req if not m.get(k)]
    if faltan:
        print(f"[FALTA] {m.get('id')}: {faltan}"); fallas += 1
    sqls = m.get("sql")
    if sqls is None:
        continue
    if isinstance(sqls, str):
        sqls = {"": sqls}
    for k, q in sqls.items():
        p = {"hasta": hasta, "jug": "Toker", "rondas": json.dumps([1, 2])}
        try:
            filas = con.execute(q, {a: b for a, b in p.items() if f":{a}" in q}).fetchall()
            print(f"[OK ] {m['id']}{'.'+k if k else ''}: {len(filas)} filas" + (f"  ej: {filas[0]}" if filas else "  (VACIA)"))
            if not filas and q != "SELECT 1":
                fallas += 1
        except Exception as e:
            print(f"[ERR] {m['id']}{'.'+k if k else ''}: {e}"); fallas += 1
print("fallas:", fallas)
sys.exit(1 if fallas else 0)
