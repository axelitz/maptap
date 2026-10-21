"""Completa la columna altitud_m de datos/dim_lugar.csv con la API gratuita de Open-Meteo (modelo digital de elevacion Copernicus 90 m).
Uso (desde cualquier carpeta, con internet):  python3 datos/scripts/obtener_altitudes.py
Solo consulta los lugares que todavia no tienen altitud. Despues avisarle a Claude para que arme la categoria."""
import csv, json, os, urllib.request, urllib.parse

CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dim_lugar.csv")
rows = list(csv.DictReader(open(CSV, encoding="utf8")))
campos = list(rows[0].keys())
if "altitud_m" not in campos:
    campos.append("altitud_m")
    for r in rows: r["altitud_m"] = ""
pend = [r for r in rows if r["altitud_m"] == ""]
print(f"{len(pend)} lugares sin altitud")
for i in range(0, len(pend), 100):
    lote = pend[i:i + 100]
    q = urllib.parse.urlencode({"latitude": ",".join(f'{float(r["lat"]):.4f}' for r in lote),
                                "longitude": ",".join(f'{float(r["lon"]):.4f}' for r in lote)})
    data = json.load(urllib.request.urlopen("https://api.open-meteo.com/v1/elevation?" + q, timeout=60))
    for r, e in zip(lote, data["elevation"]): r["altitud_m"] = str(round(e))
    print(f"  {min(i + 100, len(pend))}/{len(pend)}")
w = csv.DictWriter(open(CSV, "w", newline="", encoding="utf8"), fieldnames=campos)
w.writeheader(); w.writerows(rows)
print("listo: dim_lugar.csv actualizado")
