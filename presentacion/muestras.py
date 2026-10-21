"""Uso: python3 muestras.py  -> salida/muestras.html: una diapositiva de cada tipo, apiladas, para revisar el diseño en el navegador.
Ejecutar despues de generar.py (lee salida/presentacion.html)."""
import re, pathlib
aqui = pathlib.Path(__file__).resolve().parent
h = (aqui / "salida" / "presentacion.html").read_text(encoding="utf-8")
secs = list(re.finditer(r'<section class="slide[^"]*">.*?</section>', h, re.S))
# por tipo: portada, separador, KPI, linea, columnas, tabla, tabla ancha (peores partidas), mapa, Kahoot QR, Kahoot pregunta, podio,
# presentacion de premio, ganador (equipo ideal), ganador con extras (mejor partida), portada de perfil, perfil 1, perfil 2, cierre
ELEGIDAS = [1, 13, 2, 4, 5, 9, 46, 12, 14, 15, 16, 82, 83, 93, 48, 49, 50, 96]
cuerpo = "".join(secs[i - 1].group(0) for i in ELEGIDAS)
ini, fin = secs[0].start(), secs[-1].end()
out = h[:ini] + cuerpo + h[fin:]
out = out.replace("<script>\n(function(){", '<script>window.__TODAS=1;</script><script>\n(function(){', 1)
(aqui / "salida" / "muestras.html").write_text(out, encoding="utf-8")
print("ok", len(ELEGIDAS), "diapositivas ->", "salida/muestras.html")
