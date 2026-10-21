"""Uso: python3 ver.py 2 4 83 -> salida/ver.html con solo esas diapositivas apiladas y escaladas al ancho de la ventana (revision visual rapida)."""
import re, sys, pathlib
aqui = pathlib.Path(__file__).resolve().parent
h = (aqui / "salida" / "presentacion.html").read_text(encoding="utf-8")
secs = list(re.finditer(r'<section[^>]*class="slide[^"]*"[^>]*>.*?</section>', h, re.S))
idx = [int(a) for a in sys.argv[1:]]
out = h[:secs[0].start()] + "".join(secs[i - 1].group(0) for i in idx) + h[secs[-1].end():]
out = out.replace("<script>\n(function(){", "<script>window.__TODAS=1;</script><script>\n(function(){", 1)
(aqui / "salida" / "ver.html").write_text(out, encoding="utf-8")
print("ok ->", idx)
