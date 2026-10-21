"""Genera la presentacion de fin de ano (HTML de un solo archivo) a partir de maptap.db y metricas.yaml.
Uso: python3 generar.py [--hasta AAAA-MM-DD] [--perfiles Toker,Axel]   (sin --hasta usa el ultimo dia cerrado)
Salida: salida/presentacion.html y salida/datos.json. Estilo visual: "Anuario de la Champions" (ver guia_estilo.md, estilo.css y champions-bold/)."""
import urllib.parse, random, sqlite3, sys, json, yaml, pathlib, html, math, datetime, re

AQUI = pathlib.Path(__file__).resolve().parent
DEMO = "--demo" in sys.argv  # version de prueba con datos ficticios (ver generar_demo.py)
con = sqlite3.connect(AQUI / "salida" / "maptap_demo.db" if DEMO else AQUI.parent / "maptap.db")
con.row_factory = sqlite3.Row
arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
HASTA = arg("--hasta") or con.execute("SELECT MAX(fecha) FROM dim_fecha WHERE dia_cerrado=1").fetchone()[0]
MET = {m["id"]: m for m in yaml.safe_load(open(AQUI / "metricas.yaml", encoding="utf-8"))}
esc = html.escape
def sig2(x, n=None):
    """Dos cifras significativas: menos de 10 -> 1 decimal; 10 o mas -> sin decimales."""
    r = round(x, 1)
    return (f"{x:.0f}" if abs(r) >= 10 else f"{x:.1f}").replace(".", ",")


coma = sig2
pc1 = sig2
d1 = lambda x: f"{x:.1f}".replace(".", ",")  # un decimal
ent = lambda x: f"{x:.0f}"  # tarjetas e indicadores: sin decimales
tick0 = lambda v: f"{v:.0f}"
miles = lambda x: f"{int(x):,}".replace(",", ".")
MM = 15  # ventana de media movil (dias de juego): 15 es estable (cambio diario medio 0,3 pts vs 0,7 con 7); ver notas
ALL = lambda s: re.sub(r"es_profesional=1 AND |AND es_profesional=1", "", s)  # mismo sql sobre todo el historico (con amateur)


def run(sql, **p):
    p = {"hasta": HASTA, **p}
    return [dict(r) for r in con.execute(sql, {a: b for a, b in p.items() if f":{a}" in sql}).fetchall()]


def q(mid, key=None, **extra):
    s = MET[mid]["sql"]
    return run(s[key] if key else s, **extra)


# ---------------- tema "Anuario de la Champions" (mismos valores que estilo.css) ----------------
NOCHE, SURF, SURF2 = "#070d24", "#0f1a42", "#17265b"
ORO, ORO2, PLATA, BRONCE = "#d4af37", "#f1d98a", "#b8c2da", "#c98a54"
HUESO, APAGADO, GRILLA, GRILLA2 = "#f3efe3", "#8f9bbd", "#24336a", "#2f3f78"
BUENO, MALO = "#5ddc9a", "#ff7b7b"
# 11 colores por jugador, luminosos sobre azul noche y distinguibles entre si
PAL = ["#4cc9f0", "#ff6b6b", "#7ae582", "#ffb347", "#b388ff", "#ff8fab", "#2ec4b6", "#ffe066", "#8ecae6", "#f4845f", "#d0b3e8"]
f_fecha = lambda s: f"{datetime.date.fromisoformat(s).day}/{datetime.date.fromisoformat(s).month}"
TIPO = {r[0]: r[1] for r in con.execute("SELECT categoria,tipo FROM dim_categoria")}
ISO = {"Afganistán":"AF","Albania":"AL","Alemania":"DE","Angola":"AO","Antigua y Barbuda":"AG","Arabia Saudita":"SA","Argentina":"AR","Armenia":"AM","Australia":"AU","Austria":"AT","Azerbaiyán":"AZ","Benín":"BJ","Bermudas":"BM","Bolivia":"BO","Botsuana":"BW","Brasil":"BR","Bulgaria":"BG","Burkina Faso":"BF","Bélgica":"BE","Camerún":"CM","Canadá":"CA","Chad":"TD","Chequia":"CZ","Chile":"CL","China":"CN","Chipre":"CY","Colombia":"CO","Corea del Norte":"KP","Corea del Sur":"KR","Costa Rica":"CR","Costa de Marfil":"CI","Dinamarca":"DK","EE.UU.":"US","Ecuador":"EC","Egipto":"EG","Eslovenia":"SI","España":"ES","Estonia":"EE","Esuatini":"SZ","Etiopía":"ET","Filipinas":"PH","Finlandia":"FI","Francia":"FR","Gabón":"GA","Georgia":"GE","Ghana":"GH","Grecia":"GR","Groenlandia":"GL","Guam":"GU","Guatemala":"GT","Guayana Francesa":"GF","Guinea Ecuatorial":"GQ","Guinea-Bisáu":"GW","Guyana":"GY","Haití":"HT","Hungría":"HU","India":"IN","Indonesia":"ID","Irak":"IQ","Irán":"IR","Islandia":"IS","Islas Salomón":"SB","Israel":"IL","Italia":"IT","Jamaica":"JM","Japón":"JP","Kazajistán":"KZ","Kenia":"KE","Kirguistán":"KG","Kosovo":"XK","Lesoto":"LS","Letonia":"LV","Liberia":"LR","Libia":"LY","Liechtenstein":"LI","Luxemburgo":"LU","Macedonia del Norte":"MK","Madagascar":"MG","Malasia":"MY","Malaui":"MW","Malta":"MT","Marruecos":"MA","Martinica":"MQ","Mauricio":"MU","Moldavia":"MD","Mongolia":"MN","Mozambique":"MZ","México":"MX","Namibia":"NA","Nepal":"NP","Nigeria":"NG","Noruega":"NO","Nueva Zelanda":"NZ","Níger":"NE","Omán":"OM","Pakistán":"PK","Palestina":"PS","Panamá":"PA","Papúa Nueva Guinea":"PG","Paraguay":"PY","Países Bajos":"NL","Perú":"PE","Polonia":"PL","Portugal":"PT","Puerto Rico":"PR","Qatar":"QA","RD del Congo":"CD","Reino Unido":"GB","Rep. Centroafricana":"CF","Rep. Dominicana":"DO","Rusia":"RU","San Marino":"SM","Senegal":"SN","Serbia":"RS","Singapur":"SG","Somalia":"SO","Sri Lanka":"LK","Sudáfrica":"ZA","Sudán":"SD","Sudán del Sur":"SS","Suecia":"SE","Suiza":"CH","Tailandia":"TH","Taiwán":"TW","Tanzania":"TZ","Tonga":"TO","Trinidad y Tobago":"TT","Turquía":"TR","Túnez":"TN","Ucrania":"UA","Uganda":"UG","Uruguay":"UY","Uzbekistán":"UZ","Venezuela":"VE","Vietnam":"VN","Zimbabue":"ZW","Sin país (Antártida)":"AQ"}
def flag(pais):
    if pais == "Sin país (Atlántico Norte)": return "🌊"
    c = ISO.get(pais)
    return "".join(chr(0x1F1E6 + ord(ch) - 65) for ch in c) if c else "🌐"
_ciudad_pais = lambda l: ", ".join(dict.fromkeys([l.split(",")[0].strip(), l.split(",")[-1].strip()]))
lug = lambda lugar, pais: f"{flag(pais)} {esc(lugar)}"
_paises = {r[0] for r in con.execute("SELECT DISTINCT pais FROM dim_lugar")}
assert not [p for p in _paises if p not in ISO and p != "Sin país (Atlántico Norte)"], "pais sin bandera"


# ---------------- iconos SVG propios (heredan color con currentColor) ----------------
def _svg(inner, cls="ico", vb="0 0 24 24"):
    return f'<svg class="{cls}" viewBox="{vb}" aria-hidden="true">{inner}</svg>'


def medalla(n, metal):
    g = {"oro": ("#fff0b8", "#d4af37", "#a8842a"), "plata": ("#f3f6fb", "#b8c2da", "#8793ad"), "bronce": ("#f0c9a2", "#c98a54", "#8a5a30")}[metal]
    gid = f"g{metal}"
    return _svg(f'<defs><radialGradient id="{gid}" cx="35%" cy="30%" r="80%"><stop offset="0" stop-color="{g[0]}"/><stop offset=".6" stop-color="{g[1]}"/><stop offset="1" stop-color="{g[2]}"/></radialGradient></defs>'
                f'<path d="M6.5 1h4.2l1.6 7.2-3.4 1.2z" fill="#2a3d8f"/><path d="M17.5 1h-4.2l-1.6 7.2 3.4 1.2z" fill="#4560d0"/>'
                f'<circle cx="12" cy="15.2" r="7.6" fill="url(#{gid})" stroke="{g[2]}" stroke-width=".9"/><circle cx="12" cy="15.2" r="5.3" fill="none" stroke="{g[2]}" stroke-opacity=".55" stroke-width=".8"/>'
                f'<text x="12" y="18.5" text-anchor="middle" font-size="8.6" style="font-family:Champions,Impact,sans-serif;fill:{g[2]}">{n}</text>', "em")


M_ORO, M_PLATA, M_BRONCE = medalla(1, "oro"), medalla(2, "plata"), medalla(3, "bronce")
I_TROFEO = _svg('<path d="M6 3h12v5a6 6 0 0 1-12 0V3z"/><path d="M3.5 4H6v2.2H5.2A2 2 0 0 0 7 8.2V10a4 4 0 0 1-3.5-4zM20.5 4H18v2.2h.8A2 2 0 0 1 17 8.2V10a4 4 0 0 0 3.5-6z"/><path d="M10.6 14.2h2.8V17H16v2H8v-2h2.6z"/><rect x="6.5" y="19" width="11" height="2.2" rx="1"/>')
I_ESTRELLA = _svg('<polygon points="12,2 14.9,8.6 22,9.3 16.6,14 18.2,21 12,17.3 5.8,21 7.4,14 2,9.3 9.1,8.6"/>')
I_BALON = _svg('<circle cx="12" cy="12" r="9.6" fill="none" stroke="currentColor" stroke-width="1.7"/><polygon points="12,7.2 16.2,10.2 14.6,15 9.4,15 7.8,10.2"/><path d="M12 7.2V2.6M16.2 10.2l4.3-1.4M14.6 15l2.7 3.7M9.4 15l-2.7 3.7M7.8 10.2L3.5 8.8" fill="none" stroke="currentColor" stroke-width="1.5"/>')
I_GUANTE = _svg('<path d="M6.5 12V5.6a1.5 1.5 0 0 1 3 0V10h.6V3.8a1.5 1.5 0 0 1 3 0V10h.6V4.8a1.5 1.5 0 0 1 3 0V10h.6V7a1.5 1.5 0 0 1 3 0v6.5c0 4.4-2.6 8.2-7 8.2-3.2 0-5.2-1.8-6.5-4.6l-2-4.3a1.6 1.6 0 0 1 2.8-1.5l1 1.6z"/>')
I_BOTA = _svg('<path d="M3 4h5.2l.8 6 8.2 2.6c2.2.7 3.8 2 3.8 4.4V19H3z"/><path d="M5 20.5h2.2v1.8H5zm5 0h2.2v1.8H10zm5 0h2.2v1.8H15z"/>')
I_GRAFICO = _svg('<path d="M3 17.5l6-6.2 4 3.8 7.6-8" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><polygon points="15.5,5.8 21.6,5.8 21.6,12"/><rect x="3" y="20" width="18" height="1.8" rx=".9"/>')
I_PIN = _svg('<path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.4A2.4 2.4 0 1 1 12 6.6a2.4 2.4 0 0 1 0 4.8z"/>')
I_GLOBO = _svg('<circle cx="12" cy="12" r="9.5" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M2.5 12h19M12 2.5c3 2.6 4.4 5.8 4.4 9.5s-1.4 6.9-4.4 9.5c-3-2.6-4.4-5.8-4.4-9.5S9 5.1 12 2.5z" fill="none" stroke="currentColor" stroke-width="1.5"/>')
I_BLANCO = _svg('<circle cx="12" cy="12" r="9.5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="5.5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="1.9"/>')
I_BANDERA = _svg('<path d="M5 2.5h1.8V22H5z"/><path d="M6.8 3.6h13.6l-2.6 4.6 2.6 4.6H6.8z"/>')
I_CIEN = _svg('<text x="12" y="16.5" text-anchor="middle" font-size="12.5" style="font-family:Champions,Impact,sans-serif;fill:currentColor">100</text><circle cx="12" cy="12" r="10.5" fill="none" stroke="currentColor" stroke-width="1.5"/>')
I_SUBE = _svg('<polygon points="12,3 21,14 15,14 15,21 9,21 9,14 3,14" style="fill:#5ddc9a"/>')
I_BAJA = _svg('<polygon points="12,21 3,10 9,10 9,3 15,3 15,10 21,10" style="fill:#ff7b7b"/>')
IC_PREMIO = {"👟": I_BOTA, "📈": I_GRAFICO, "⚽": I_BALON, "🏆": I_TROFEO, "🏅": M_ORO, "🧤": I_GUANTE, "⭐": I_ESTRELLA}
ic_svg = lambda e: IC_PREMIO.get(e, "")

# ---------------- graficos SVG ----------------
def ejes_y(o, L, R, T, B, ancho, alto, y0, y1, py, ticks, fmt, ytitle):
    for v in ticks:
        o.append(f'<line x1="{L}" x2="{ancho-R}" y1="{py(v):.1f}" y2="{py(v):.1f}" stroke="{GRILLA}"/><text x="{L-8}" y="{py(v)+4:.1f}" text-anchor="end" class="t s">{fmt(v)}</text>')
    if ytitle:
        o.append(f'<text transform="translate(14,{(T+alto-B)/2}) rotate(-90)" text-anchor="middle" class="t ax">{esc(ytitle)}</text>')


def barras(items, fmt=lambda v: coma(v), minimo=None, color=ORO, ancho=1230, alto=470, titulo_x=""):
    """Barras horizontales que ocupan todo el alto disponible (el alto de cada fila se ajusta a la cantidad de barras)."""
    vals = [v for _, v in items]
    lo = min(0, min(vals)) if minimo is None else minimo
    hi = max(vals)
    rng = (hi - lo) or 1
    pie = 34 if titulo_x else 8
    h = min(72, (alto - pie) / len(items))
    x0, W = 250, ancho - 250 - 110
    o = [f'<svg viewBox="0 0 {ancho} {alto}" class="ch big">']
    for i, (lab, v) in enumerate(items):
        y = i * h
        w = max((v - lo) / rng * W, 2)
        o.append(f'<text x="{x0-12}" y="{y+h/2+7:.1f}" text-anchor="end" class="t">{esc(str(lab))}</text><rect x="{x0}" y="{y+h*0.14:.1f}" width="{w:.1f}" height="{h*0.72:.1f}" rx="5" fill="{color}"/>'
                 f'<text x="{x0+w+10:.1f}" y="{y+h/2+7:.1f}" class="t b">{fmt(v)}</text>')
    if titulo_x:
        o.append(f'<text x="{x0+W/2}" y="{alto-6}" text-anchor="middle" class="t ax">{esc(titulo_x)}</text>')
    o.append("</svg>")
    return "".join(o)


def columnas(items, xtitle, ytitle, ancho=1230, alto=470, color=ORO, chico=False, pct=False):
    """items: [(etiqueta, valor)]; con pct=True los valores ya vienen en % y se rotulan asi."""
    L, R, T, B = 70, 20, 24, 56
    hi = max(v for _, v in items)
    top = (math.ceil(hi / 4) * 4) if pct else math.ceil(hi / 50) * 50
    fmt = (lambda v: pc1(v) + "%") if pct else (lambda v: miles(v))
    py = lambda v: alto - B - v / top * (alto - T - B)
    bw = (ancho - L - R) / len(items)
    o = [f'<svg viewBox="0 0 {ancho} {alto}" class="ch big">']
    ejes_y(o, L, R, T, B, ancho, alto, 0, top, py, [top * k / 4 for k in range(5)], (lambda v: f"{int(v)}%") if pct else miles, ytitle)
    for i, (lab, v) in enumerate(items):
        x = L + i * bw + 6
        o.append(f'<rect x="{x:.1f}" y="{py(v):.1f}" width="{bw-12:.1f}" height="{alto-B-py(v):.1f}" rx="4" fill="{color}"/>'
                 f'<text x="{x+(bw-12)/2:.1f}" y="{py(v)-6:.1f}" text-anchor="middle" class="t b{" s" if chico else ""}">{fmt(v)}</text>'
                 f'<text x="{x+(bw-12)/2:.1f}" y="{alto-B+18}" text-anchor="middle" class="t{" s" if chico else ""}">{esc(lab)}</text>')
    o.append(f'<text x="{(L+ancho-R)/2}" y="{alto-10}" text-anchor="middle" class="t ax">{esc(xtitle)}</text></svg>')
    return "".join(o)


def lineas(series, ancho=1230, alto=470, ymin=None, ymax=None, invertir=False, yticks=None, xticks=None, xtitle="", ytitle="", yfmt=tick0, fin=False, hlines=(), marcas=False, rpad=110, etq=None, leyenda=None, xmargin=0):
    xs = [p[0] for s in series for p in s[2]]
    ys = [p[1] for s in series for p in s[2]]
    x0, x1 = min(xs) - xmargin, max(xs) + xmargin
    y0 = min(ys) if ymin is None else ymin
    y1 = max(ys) if ymax is None else ymax
    L, R, T, B = 70, rpad if fin else 20, 14, 56
    px = lambda x: L + (x - x0) / ((x1 - x0) or 1) * (ancho - L - R)
    py = lambda y: (T + (y - y0) / ((y1 - y0) or 1) * (alto - T - B)) if invertir else (alto - B - (y - y0) / ((y1 - y0) or 1) * (alto - T - B))
    o = [f'<svg viewBox="0 0 {ancho} {alto}" class="ch{" big" if ancho >= 1000 else ""}">']
    ejes_y(o, L, R, T, B, ancho, alto, y0, y1, py, yticks if yticks is not None else [y0 + (y1 - y0) * k / 4 for k in range(5)], yfmt, ytitle)
    for x, lab in (xticks or []):
        o.append(f'<text x="{px(x):.1f}" y="{alto-B+18}" text-anchor="middle" class="t s">{esc(lab)}</text>')
    if xtitle:
        o.append(f'<text x="{(L+ancho-R)/2}" y="{alto-10}" text-anchor="middle" class="t ax">{esc(xtitle)}</text>')
    for hy, hlab, hcol in hlines:
        o.append(f'<line x1="{L}" x2="{ancho-R}" y1="{py(hy):.1f}" y2="{py(hy):.1f}" stroke="{hcol}" stroke-width="2.5" stroke-dasharray="9 6"/>'
                 + (f'<text x="{ancho-R-6}" y="{py(hy)-7:.1f}" text-anchor="end" class="t b" style="fill:{hcol}">{esc(hlab)}</text>' if hlab else ""))
    if leyenda:
        o.append(f'<line x1="{ancho-R-300}" x2="{ancho-R-264}" y1="{T+14}" y2="{T+14}" stroke="{leyenda[1]}" stroke-width="3" stroke-dasharray="9 6"/><text x="{ancho-R-256}" y="{T+20}" class="t b" style="fill:{leyenda[1]};font-size:20px">{esc(leyenda[0])}</text>')
    ends = []
    for nom, col, pts, gr, op in series:
        o.append('<polyline points="' + " ".join(f"{px(x):.1f},{py(y):.1f}" for x, y in pts) + f'" fill="none" stroke="{col}" stroke-width="{gr}" opacity="{op}" stroke-linejoin="round" stroke-linecap="round"/>')
        if marcas:
            o.extend(f'<circle cx="{px(x):.1f}" cy="{py(y):.1f}" r="{7 if etq else 3.2}" fill="{col}"/>' for x, y in pts)
        if etq:
            o.extend(f'<text x="{px(x):.1f}" y="{py(y)-16:.1f}" text-anchor="middle" class="t b">{etq(y)}</text>' for x, y in pts)
        if fin and pts:
            ends.append([py(pts[-1][1]), nom, col, pts[-1][0]])
    ends.sort()
    for i in range(1, len(ends)):  # evitar que se pisen las etiquetas del extremo derecho
        if ends[i][0] - ends[i - 1][0] < 13:
            ends[i][0] = ends[i - 1][0] + 13
    for y, nom, col, xe in ends:
        o.append(f'<text x="{px(xe)+8:.1f}" y="{y+4:.1f}" class="t s" style="fill:{col};font-weight:700">{esc(nom)}</text>')
    o.append("</svg>")
    return "".join(o)


def radar(ejes, jug, grupo, nom, color, ancho=600, alto=470):
    vals = [v for v in jug + grupo if v is not None]
    lo = math.floor(min(vals) / 5) * 5 - 5
    hi = 100
    cx, cy, r = ancho / 2, alto / 2 + 10, alto / 2 - 55
    n = len(ejes)
    pt = lambda i, v: (cx + r * (v - lo) / (hi - lo) * math.sin(2 * math.pi * i / n), cy - r * (v - lo) / (hi - lo) * math.cos(2 * math.pi * i / n))
    o = [f'<svg viewBox="0 0 {ancho} {alto}" class="ch rad">']
    for k in range(1, 5):
        v = lo + (hi - lo) * k / 4
        o.append('<polygon points="' + " ".join(f"{pt(i,v)[0]:.1f},{pt(i,v)[1]:.1f}" for i in range(n)) + f'" fill="none" stroke="{GRILLA2}"/>')
    for i, e in enumerate(ejes):
        x, y = pt(i, hi)
        o.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{GRILLA2}"/>')
        lx, ly = cx + (r + 34) * math.sin(2 * math.pi * i / n), cy - (r + 28) * math.cos(2 * math.pi * i / n)
        o.append(f'<text x="{lx:.1f}" y="{ly+4:.1f}" text-anchor="middle" class="t b">{esc(e)}</text>')
    for serie, col, dash, fo in ((grupo, PLATA, "6 4", 0.10), (jug, color, "", 0.28)):
        p = [pt(i, v if v is not None else lo) for i, v in enumerate(serie)]
        o.append('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in p) + f'" fill="{col}" fill-opacity="{fo}" stroke="{col}" stroke-width="2.5" stroke-dasharray="{dash}"/>')
        if not dash:
            for (x, y), v in zip(p, serie):
                if v is not None:
                    o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{col}"/>')
    o.append(f'<text x="{ancho-8}" y="20" text-anchor="end" class="t s" style="fill:{color};font-weight:700">● {esc(nom)}</text><text x="{ancho-8}" y="40" text-anchor="end" class="t s" style="fill:{APAGADO};font-weight:700">● Promedio del grupo</text></svg>')
    return "".join(o)


def lineas_rel(nom, col, pts, xticks, xtitle, ytitle):
    """Valor relativo al grupo: 0 = promedio del grupo; sin cifras en el eje (para no adelantar premios)."""
    m = max([abs(v) for _, v in pts] + [1]) * 1.25
    return lineas([(nom, col, pts, 3.5, 1)], ymin=-m, ymax=m, ancho=640, alto=240, rpad=64, yticks=[-m, 0, m], yfmt=lambda v: "", hlines=[(0, "Promedio del grupo", APAGADO)],
                  xticks=xticks, xtitle=xtitle, ytitle=ytitle + " (↑ mejor)", fin=True)


def boxplot(items, ymin, ymax=100, ancho=1230, alto=470, ytitle="Puntaje de la ronda"):
    """items: [(flag_o_vacio, nombre, stats)]. Caja = q1-q3, raya = mediana, bigotes = p10-p90."""
    L, R, T, B = 70, 20, 14, 74
    py = lambda v: alto - B - (v - ymin) / (ymax - ymin) * (alto - T - B)
    bw = (ancho - L - R) / len(items)
    o = [f'<svg viewBox="0 0 {ancho} {alto}" class="ch big">']
    ejes_y(o, L, R, T, B, ancho, alto, ymin, ymax, py, [ymin + (ymax - ymin) * k / 5 for k in range(6)], tick0, ytitle)
    for i, (fl, nom, st) in enumerate(items):
        cx = L + bw * (i + .5)
        w = min(bw * 0.55, 90)
        o.append(f'<line x1="{cx:.1f}" x2="{cx:.1f}" y1="{py(st["p90"]):.1f}" y2="{py(st["p10"]):.1f}" stroke="{ORO}" stroke-width="2.5"/>'
                 f'<line x1="{cx-w/4:.1f}" x2="{cx+w/4:.1f}" y1="{py(st["p90"]):.1f}" y2="{py(st["p90"]):.1f}" stroke="{ORO}" stroke-width="2.5"/><line x1="{cx-w/4:.1f}" x2="{cx+w/4:.1f}" y1="{py(st["p10"]):.1f}" y2="{py(st["p10"]):.1f}" stroke="{ORO}" stroke-width="2.5"/>'
                 f'<rect x="{cx-w/2:.1f}" y="{py(st["q3"]):.1f}" width="{w:.1f}" height="{max(py(st["q1"])-py(st["q3"]),2):.1f}" rx="4" fill="{SURF2}" stroke="{ORO}" stroke-width="2.5"/>'
                 f'<line x1="{cx-w/2:.1f}" x2="{cx+w/2:.1f}" y1="{py(st["med"]):.1f}" y2="{py(st["med"]):.1f}" stroke="{HUESO}" stroke-width="5"/>'
                 f'<text x="{cx:.1f}" y="{alto-B+26}" text-anchor="middle" class="t" style="font-size:22px">{fl}</text><text x="{cx:.1f}" y="{alto-B+48}" text-anchor="middle" class="t s">{esc(nom)}</text>'
                 f'<text x="{cx+w/2+6:.1f}" y="{py(st["med"])+5:.1f}" class="t s" style="fill:{HUESO}">{sig2(st["med"])}</text>')
    o.append("</svg>")
    return "".join(o)


def stats_box(vals):
    v = sorted(vals)
    pct = lambda p: v[0] if len(v) == 1 else v[int(math.floor((len(v) - 1) * p))] + ((len(v) - 1) * p - math.floor((len(v) - 1) * p)) * (v[min(int(math.floor((len(v) - 1) * p)) + 1, len(v) - 1)] - v[int(math.floor((len(v) - 1) * p))])
    return dict(p10=pct(.10), q1=pct(.25), med=pct(.5), q3=pct(.75), p90=pct(.90), mean=sum(v) / len(v))


def torta(items, ancho=1230, alto=470):
    """items: [(etiqueta, valor, color, detalle)]. Torta a la izquierda y referencias a la derecha."""
    tot = sum(v for _, v, _, _ in items)
    cx, cy, r = 400, alto / 2, alto / 2 - 20
    a0 = -math.pi / 2
    o = [f'<svg viewBox="0 0 {ancho} {alto}" class="ch big">']
    for lab, v, col, _ in items:
        fr = v / tot
        a1 = a0 + 2 * math.pi * fr
        x0, y0, x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1)
        o.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 {1 if fr > .5 else 0} 1 {x1:.1f},{y1:.1f} Z" fill="{col}" stroke="{NOCHE}" stroke-width="3"/>')
        am = (a0 + a1) / 2
        o.append(f'<text x="{cx + r*0.66*math.cos(am):.1f}" y="{cy + r*0.66*math.sin(am) + 8:.1f}" text-anchor="middle" class="t b" style="font-size:26px;fill:{NOCHE}">{sig2(100*fr)}%</text>')
        a0 = a1
    for i, (lab, v, col, det) in enumerate(items):
        y = alto / 2 - len(items) * 30 + i * 60
        o.append(f'<rect x="760" y="{y-18:.1f}" width="26" height="26" rx="5" fill="{col}"/><text x="800" y="{y+2:.1f}" class="t b" style="font-size:24px">{esc(lab)}</text><text x="800" y="{y+28:.1f}" class="t s" style="font-size:18px">{esc(det)}</text>')
    o.append("</svg>")
    return "".join(o)


# ---------------- tablas con el estilo de los HTML del torneo ----------------
def tabla(cab, filas, clases=None):
    h = '<div class="table-box"><table><thead><tr>' + "".join(f"<th>{c}</th>" for c in cab) + "</tr></thead><tbody>"
    for i, f in enumerate(filas):
        h += f'<tr class="{clases[i] if clases else ""}">' + "".join(f"<td>{x}</td>" for x in f) + "</tr>"
    return h + "</tbody></table></div>"


def nv(nombre, valor):
    return f'<span class="name">{esc(nombre)}</span><span class="value">{esc(valor)}</span>'


def podio(cab_label, filas):
    """filas: [(etiqueta, [(nombre, valor) x3])]"""
    out = []
    for lab, top in filas:
        top = list(top) + [None] * (3 - len(top))
        out.append((f'<b>{esc(lab)}</b>', *[nv(*t) if t else "—" for t in top]))
    return tabla([cab_label, f"{M_ORO} 1.º", f"{M_PLATA} 2.º", f"{M_BRONCE} 3.º"], out)


def tier(d):
    k = "abcde"[d - 1] if d <= 5 else "e"
    return f'<span class="tier {k}">{d}.ª</span>'


# ---------------- datos ----------------
D = {"hasta": HASTA}
D["partidas"] = run(MET["a_partidas"]["sql"])[0].popitem()[1]
ub = q("a_ubicaciones")[0]
D["ubicaciones"], D["lugares"] = ub["ubicaciones"], ub["lugares"]
D["prom_grupo"] = run(MET["a_prom_grupo"]["sql"])[0].popitem()[1]
D["dias"] = con.execute("SELECT COUNT(*) FROM dim_fecha WHERE es_profesional=1 AND dia_cerrado=1 AND fecha<=?", (HASTA,)).fetchone()[0]
D["diario"] = q("a_prom_diario_grupo")
D["dist"] = q("a_dist_puntajes")
D["extremos"] = run(ALL(MET["a_dias_extremos"]["sql"]))  # todas las fechas
D["rec100"] = q("a_record_100_dia")
D["prom"] = q("prom_nominal")
D["pct100"] = q("b_pct_100")
D["final"] = q("b_prom_final")
D["desvio"] = q("b_desvio_diario")
D["titulos"] = q("b_ranking_dia_titulos")
D["semanal"] = q("b_copa_semanal")
D["mensual"] = q("b_copa_mensual")
D["div"] = q("b_trayectoria_divisiones")
D["challenge"] = q("b_titulos_challenge")
D["exceso"] = q("b_exceso_prom")
D["caida5"] = q("e_caida_x3")
D["mensual_j"] = q("e_prom_mensual")
D["zona_cont"] = q("c_dificultad_zona", "continente")
D["zona_reg"] = q("c_dificultad_zona", "region")
D["zona_pais"] = q("c_dificultad_zona", "pais")
D["ubic"] = q("c_dificultad_ubicacion")
D["topz"] = {k: q("c_top_zona_jugador", k) for k in ("continente", "region", "pais")}  # continente: minimo 5 rondas (ver metricas.yaml)
D["mapa"] = q("c_mapa_ubicaciones")
D["catjug"] = q("d_promedio_categoria_jugador")
D["cat"] = q("d_dificultad_categoria")
D["ronda"] = {}
for nombre, rs in (("R1", [1]), ("R2", [2]), ("R3", [3]), ("R4", [4]), ("R5", [5]), ("R4+5", [4, 5])):
    D["ronda"][nombre] = {r["jugador"]: r["prom"] for r in q("e_prom_ronda", rondas=json.dumps(rs))}
orden = [r["jugador"] for r in D["prom"]]

# conciliacion de copas semanales con los valores oficiales
sem = {}
for r in D["semanal"]:
    sem.setdefault(r["semana_inicio"], {})[r["jugador"]] = r["puntos"]
for sd, esp in (("2026-09-28", {"Axel": 6581, "Toker": 6488, "Sandro": 6405}), ("2026-10-05", {"Toker": 6428, "Axel": 6396, "Fede": 6245})):
    if sd in sem and not DEMO:
        for j, v in esp.items():
            assert sem[sd][j] == v, f"copa semanal {sd} {j}: {sem[sd][j]} != {v}"

# premios
viaj = run("""WITH g AS (SELECT fecha,ronda,AVG(puntaje) m FROM v_puntaje WHERE es_profesional=1 AND fecha<=:hasta GROUP BY fecha,ronda)
 SELECT p.jugador, COUNT(*) n, AVG(p.puntaje-g.m) v FROM v_puntaje p JOIN g USING(fecha,ronda) JOIN dim_lugar l USING(id_lugar) WHERE p.es_profesional=1 AND p.fecha<=:hasta AND l.dist_buenos_aires_km>12000
 GROUP BY p.jugador HAVING n>=10 ORDER BY v DESC""")  # "viajero": ubicaciones a mas de 12.000 km de Buenos Aires (ya no es una categoria)
SORP = sorted([r for r in D["catjug"] if r["n"] >= 12 and TIPO[r["categoria"]] != "complemento"], key=lambda r: -r["dif"])
ovr = {r["jugador"]: r["prom"] for r in D["prom"]}
reg_dif = {}
for r in D["topz"]["region"]:
    reg_dif.setdefault(r["jugador"], []).append(r["prom"] - ovr[r["jugador"]])
parejo = sorted([(j, math.sqrt(sum(x * x for x in v) / len(v) - (sum(v) / len(v)) ** 2), len(v)) for j, v in reg_dif.items() if len(v) >= 5], key=lambda t: t[1])
mj = {}
for r in D["mensual_j"]:
    mj.setdefault(r["jugador"], []).append(r)
remon = sorted([(j, v[-1]["prom"] - v[0]["prom"], v[0]["anio_mes"], v[-1]["anio_mes"]) for j, v in mj.items() if len(v) >= 2], key=lambda t: -t[1])
best = lambda d: sorted(d.items(), key=lambda kv: -kv[1])[0]
AH = "fecha<=:hasta"  # MVP y mas mejorado: TODA la historia (amateur + profesional)
AP = "es_profesional=1 AND fecha<=:hasta"  # clutch, Bota de Oro, gol y mejor partida: solo profesionalismo
nombres = lambda L: ", ".join(r["jugador"] for r in L)


def empatados(rows, campo):
    mx = max(r[campo] for r in rows)
    return [r for r in rows if r[campo] == mx], mx


clut_rows = run(f"SELECT jugador, AVG(CASE WHEN ronda IN (4,5) THEN puntaje END) a, AVG(CASE WHEN ronda IN (1,2) THEN puntaje END) b FROM v_puntaje WHERE {AP} GROUP BY jugador")
for r in clut_rows:
    r["v"] = 100 * (r["a"] / r["b"] - 1)  # variacion porcentual del promedio de R4+R5 contra el de R1+R2
clut, v_clut = empatados(clut_rows, "v")
bota_rows = run(f"SELECT jugador, SUM(puntaje=100) v FROM v_puntaje WHERE {AP} GROUP BY jugador")
bota, v_bota = empatados(bota_rows, "v")
bota_n = {r["jugador"]: r["n"] for r in run(f"SELECT jugador, COUNT(*) n FROM v_puntaje WHERE {AP} GROUP BY jugador")}
mes_j = {}
for r in run(f"SELECT substr(fecha,1,7) mes, jugador, COUNT(*) n, AVG(puntaje) prom FROM v_puntaje WHERE {AH} GROUP BY mes, jugador HAVING n>=20 ORDER BY mes"):
    mes_j.setdefault(r["jugador"], []).append(r)
mejoras = sorted([(j, v[-1]["prom"] - v[0]["prom"], v[0]["mes"], v[-1]["mes"]) for j, v in mes_j.items() if len(v) >= 2], key=lambda t: -t[1])
mejora = mejoras[0]
gol_rows = run(f"""WITH t AS (SELECT id_ubicacion, SUM(puntaje) s, COUNT(*) n FROM v_puntaje WHERE {AP} GROUP BY id_ubicacion HAVING n>=6)
 SELECT p.jugador, p.fecha, p.lugar, p.pais, p.puntaje, p.puntaje-(t.s-p.puntaje)*1.0/(t.n-1) dif FROM v_puntaje p JOIN t USING(id_ubicacion)
 WHERE p.{AP} ORDER BY dif DESC, p.puntaje DESC""")
gol = [r for i, r in enumerate(gol_rows) if r["jugador"] not in {x["jugador"] for x in gol_rows[:i]}]
gol0 = gol[0]
bp_rows = run(f"SELECT j.alias jugador, p.fecha, p.puntaje_final x FROM fact_partida p JOIN dim_fecha f USING(fecha) JOIN dim_jugador j USING(id_jugador) WHERE p.{AH} ORDER BY p.puntaje_final DESC, p.suma_rondas DESC, p.fecha")
bp = [r for i, r in enumerate(bp_rows) if r["jugador"] not in {x["jugador"] for x in bp_rows[:i]}]
bp0 = bp[0]
rondas_de = lambda jug, f: " · ".join(str(r["puntaje"]) for r in run("SELECT puntaje FROM v_puntaje WHERE jugador=:j AND fecha=:f ORDER BY ronda", j=jug, f=f))
lug_pts = lambda jug, f: [(r["pais"], r["lugar"], r["puntaje"]) for r in run("SELECT pais, lugar, puntaje FROM v_puntaje WHERE jugador=:j AND fecha=:f ORDER BY ronda", j=jug, f=f)]
LDQ = "SELECT l.lugar, l.pais FROM fact_aparicion a JOIN dim_lugar l USING(id_lugar) WHERE a.fecha=:f ORDER BY a.ronda"
ciudades_pts = lambda j, f: " · ".join(f"{flag(p)} {esc(l)} (<b>{pt}</b>)" for p, l, pt in lug_pts(j, f))
ciudades_dia = lambda f: " · ".join(f"{flag(r['pais'])} {esc(r['lugar'])}" for r in run(LDQ, f=f))
am = run("SELECT j.alias jugador, p.fecha, p.puntaje_final x FROM fact_partida p JOIN dim_fecha f USING(fecha) JOIN dim_jugador j USING(id_jugador) WHERE f.es_profesional=0 AND p.fecha<=:hasta ORDER BY p.puntaje_final DESC, p.suma_rondas DESC, p.fecha LIMIT 1")[0]
mvp_rows = run(f"SELECT j.alias jugador, AVG(p.puntaje_final) v FROM fact_partida p JOIN dim_jugador j USING(id_jugador) WHERE p.{AH} GROUP BY j.alias ORDER BY v DESC")
mvp = mvp_rows[0]
mvp_ronda = run("SELECT AVG(puntaje) a FROM v_puntaje WHERE jugador=:j AND fecha<=:hasta", j=mvp["jugador"])[0]["a"]
mes_txt = lambda m: f"{int(m[5:])}/{m[2:4]}"

# Guante de Oro: menor % de rondas bajo 80 (profesionalismo, minimo 100 rondas)
guante_rows = run(f"SELECT jugador, COUNT(*) n, SUM(puntaje<80) k, 100.0*SUM(puntaje<80)/COUNT(*) v FROM v_puntaje WHERE {AP} GROUP BY jugador HAVING n>=100 ORDER BY v, jugador")
guante = [r for r in guante_rows if r["v"] == guante_rows[0]["v"]]
# Equipo ideal: un puesto por ronda, sin repetir jugador; asignacion que maximiza la suma de promedios por ronda
import itertools
_pr = {(r["jugador"], r["ronda"]): r["a"] for r in run(f"SELECT jugador, ronda, AVG(puntaje) a FROM v_puntaje WHERE {AP} GROUP BY jugador, ronda")}
_js = sorted({j for j, _ in _pr})
_best = max(itertools.permutations(_js, 5), key=lambda t: (sum(_pr[(j, k + 1)] for k, j in enumerate(t)), t))
equipo = list(_best)
_sup = [r["jugador"] for r in run(f"SELECT jugador, AVG(puntaje) a FROM v_puntaje WHERE {AP} GROUP BY jugador ORDER BY a DESC") if r["jugador"] not in equipo][:3]
# de menor a mayor importancia; el MVP va ultimo
rk = lambda rows, f: [(r["jugador"] if isinstance(r, dict) else r[0], f(r)) for r in rows][:3]  # terna: (nombre, desempeno)
D["premios"] = [
    dict(alc="Solo profesionalismo", t="El equipo ideal", ic="⭐", desc="Una alineación de 5: un jugador por ronda, el mejor en cada puesto sin repetir", j=", ".join(equipo), v=" · ".join(f"R{k+1} {j}" for k, j in enumerate(equipo)), nom=[(j, f"R{k+1}") for k, j in enumerate(equipo)] + [(j, "suplente") for j in _sup], cancha=[(j, k + 1, _pr[(j, k + 1)]) for k, j in enumerate(equipo)], sup=_sup),
    dict(alc="Solo profesionalismo", t="Guante de Oro", ic="🧤", desc="La valla menos vencida: el que menos rondas malas (bajo 80) tuvo", j=nombres(guante), v=f"{pc1(guante[0]['v'])}% de rondas bajo 80 ({int(guante[0]['k'])} de {guante[0]['n']})", nom=rk(guante_rows, lambda r: f"{pc1(r['v'])}% de rondas bajo 80")),
    dict(alc="Solo profesionalismo", t="Bota de Oro", ic="👟", desc="El máximo goleador: el que más 100 consiguió", j=nombres(bota), v=f"{int(v_bota)} rondas con 100 ({pc1(100 * v_bota / bota_n[bota[0]['jugador']])}% de sus rondas)", nom=rk(sorted(bota_rows, key=lambda r: -r["v"]), lambda r: f"{int(r['v'])} rondas con 100")),
    dict(alc="Toda la historia", t="Jugador más mejorado", ic="📈", desc="Quien más creció desde su primer mes", j=mejora[0], v=f"+{d1(mejora[1])} puntos por ronda", nom=rk(mejoras, lambda r: f"+{d1(r[1])} puntos por ronda")),
    dict(alc="Solo profesionalismo", t="El gol de la temporada", ic="⚽", desc="La ronda que más se despegó del resto", j=gol0["jugador"], v=f"{gol0['puntaje']} en {flag(gol0['pais'])} {gol0['lugar']} (+{ent(gol0['dif'])} sobre el resto)", nom=rk(gol, lambda r: f"{r['puntaje']} en {r['lugar'].split(',')[0]} (+{ent(r['dif'])})")),
    dict(alc="Toda la historia", t="La mejor partida", ic="🏆", desc="El mayor puntaje final en un día", j=bp0["jugador"], v=f"{bp0['x']} puntos el {f_fecha(bp0['fecha'])}", nom=rk(bp, lambda r: f"{r['x']} puntos"), extra=f'<div class="wx cit">{ciudades_pts(bp0["jugador"], bp0["fecha"])}</div>'),
    dict(alc="Toda la historia", t="MVP de la temporada", ic="🏅", desc="El mejor jugador de la temporada", j=mvp["jugador"], v=f"{ent(mvp['v'])} de promedio por partida ({ent(mvp_ronda)} por ronda)", nom=rk(mvp_rows, lambda r: f"{ent(r['v'])} de promedio")),
]

# perfiles: SOLO profesionalismo. La etapa amateur se usa unicamente para completar las ventanas de la media movil.
CORTE = con.execute("SELECT MIN(fecha) FROM dim_fecha WHERE es_profesional=1").fetchone()[0]
HIST = {r["jugador"]: r for r in run("SELECT jugador, COUNT(*) n, AVG(puntaje) prom, 100.0*SUM(puntaje=100)/COUNT(*) pct FROM v_puntaje WHERE es_profesional=1 AND fecha<=:hasta GROUP BY jugador")}
CONT = [r["continente"] for r in run("SELECT continente, COUNT(DISTINCT id_ubicacion) u FROM v_puntaje WHERE es_profesional=1 AND fecha<=:hasta GROUP BY continente HAVING u>=5 ORDER BY continente")]
orden_cont = [c for c in ("Europa", "Asia", "África", "Oceanía", "América del Sur", "América Central", "América del Norte") if c in CONT]
pc = {(r["continente"], r["jugador"]): r for r in run("SELECT continente, jugador, COUNT(*) n, AVG(puntaje) prom FROM v_puntaje WHERE es_profesional=1 AND fecha<=:hasta GROUP BY continente, jugador")}
gc = {r["continente"]: r["prom"] for r in run("SELECT continente, AVG(puntaje) prom FROM v_puntaje WHERE es_profesional=1 AND fecha<=:hasta GROUP BY continente")}
dg = run("SELECT fecha, AVG(puntaje) x FROM v_puntaje WHERE fecha<=:hasta GROUP BY fecha ORDER BY fecha")  # historial completo: solo para completar ventanas
mmv = lambda v, w: [None if i < w - 1 else sum(v[i - w + 1:i + 1]) / w for i in range(len(v))]  # solo ventanas completas
dgf = run("SELECT fecha, AVG(puntaje_final) x FROM fact_partida WHERE fecha<=:hasta GROUP BY fecha ORDER BY fecha")
gmf = {f: v for f, v in zip([r["fecha"] for r in dgf], mmv([r["x"] for r in dgf], MM)) if v is not None}
HF = {r["jugador"]: r["prom"] for r in run("SELECT j.alias jugador, AVG(p.puntaje_final) prom FROM fact_partida p JOIN dim_fecha f USING(fecha) JOIN dim_jugador j USING(id_jugador) WHERE f.es_profesional=1 AND p.fecha<=:hasta GROUP BY j.alias")}
# fortalezas/debilidades: diferencia contra el promedio del GRUPO en las mismas ubicaciones
FD_SQL = """WITH g AS (SELECT id_ubicacion, AVG(puntaje) m FROM v_puntaje WHERE es_profesional=1 AND fecha<=:hasta GROUP BY id_ubicacion),
 b AS (SELECT p.id_ubicacion, p.region, p.continente, p.pais, p.puntaje pt, p.puntaje-g.m d FROM v_puntaje p JOIN g USING(id_ubicacion) WHERE p.jugador=:jug AND p.es_profesional=1 AND p.fecha<=:hasta)
 SELECT tipo, zona, COUNT(*) n, ROUND(AVG(d),2) dif, ROUND(AVG(pt),1) prom FROM (
  SELECT 'region' tipo, region zona, d, pt FROM b UNION ALL SELECT 'continente', continente, d, pt FROM b UNION ALL SELECT 'pais', pais, d, pt FROM b
  UNION ALL SELECT 'categoria', c.categoria, c.puntaje-g.m, c.puntaje FROM v_puntaje_categoria c JOIN g USING(id_ubicacion) WHERE c.jugador=:jug AND c.es_profesional=1 AND c.fecha<=:hasta
    )
 GROUP BY tipo, zona HAVING n>=10 ORDER BY dif DESC"""
_MOM = """WITH t AS (SELECT id_ubicacion, SUM(puntaje) s, COUNT(*) n FROM v_puntaje WHERE es_profesional=1 AND fecha<=:hasta GROUP BY id_ubicacion HAVING n>=6)
 SELECT p.fecha, p.lugar, p.pais, p.puntaje, p.puntaje-(t.s-p.puntaje)*1.0/(t.n-1) dif FROM v_puntaje p JOIN t USING(id_ubicacion)
 WHERE p.jugador=:jug AND p.es_profesional=1 AND p.fecha<=:hasta ORDER BY dif {o}, p.puntaje {o} LIMIT 3"""
MEJ_SQL, PEO_SQL = _MOM.format(o="DESC"), _MOM.format(o="ASC")
medallas = {r["jugador"]: r for r in D["titulos"]}
div_hab = {}
for jg in {r["jugador"] for r in D["div"]}:
    cnt = {}
    for r in D["div"]:
        if r["jugador"] == jg:
            cnt[r["division"]] = cnt.get(r["division"], 0) + 1
    d0 = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))[0]
    div_hab[jg] = (d0[0], d0[1], sum(cnt.values()))
divhoy = {r["jugador"]: r["division"] for r in D["div"] if r["fecha"] == max(x["fecha"] for x in D["div"])}
D["perfiles"] = {}
# categorias casi equivalentes: en un mismo top 3 entra solo la mejor ubicada de cada grupo
REGCONT = dict(con.execute("SELECT DISTINCT region, continente FROM dim_lugar").fetchall())
SIMIL = [{"Capital nacional", "Capital regional"},
         {"Ex URSS", "Zona de conflicto o inestable"},
         {"Ciudad costera", "Isla o pais insular"}]


def dedup(L):
    usados, out = set(), []
    for r in L:
        g = next((i for i, G in enumerate(SIMIL) if r["zona"] in G), None)
        if g is not None:
            if g in usados:
                continue
            usados.add(g)
        out.append(r)
    return out


for jug in sorted(arg("--perfiles").split(",") if arg("--perfiles") else HIST):
    fd = [r for r in run(FD_SQL, jug=jug) if r["zona"] != "Europa turistica clasica" and (r["tipo"] == "categoria" or (r["tipo"] == "region" and REGCONT.get(r["zona"]) in ("Europa", "Asia", "África")) or (r["tipo"] == "continente" and r["zona"] == "América Central"))]  # categorias + regiones de Europa/Asia/Africa + Centroamerica (sin paises)
    dfj = run("SELECT p.fecha, p.puntaje_final x FROM fact_partida p JOIN dim_jugador j USING(id_jugador) WHERE p.fecha<=:hasta AND j.alias=:jug ORDER BY p.fecha", jug=jug)
    rj = {r["ronda"]: r["prom"] for r in run("SELECT ronda, AVG(puntaje) prom FROM v_puntaje WHERE es_profesional=1 AND fecha<=:hasta AND jugador=:jug GROUP BY ronda", jug=jug)}
    D["perfiles"][jug] = {"fort": dedup(fd)[:3], "deb": dedup(list(reversed(fd)))[:3], "mej": run(MEJ_SQL, jug=jug), "peo": run(PEO_SQL, jug=jug), "ronda": rj,
                          "mmf": [(f, v) for f, v in zip([r["fecha"] for r in dfj], mmv([r["x"] for r in dfj], MM)) if v is not None and f in gmf], "hf": HF[jug]}
_dv = run("SELECT d.fecha, j.alias jugador, d.division FROM fact_division d JOIN dim_jugador j USING(id_jugador) WHERE d.fecha>='2026-09-02' AND d.fecha<=:hasta ORDER BY j.alias, d.fecha")
DA = {}
_prev = {}
for r in _dv:
    a = DA.setdefault(r["jugador"], [0, 0])
    if r["jugador"] in _prev and r["division"] < _prev[r["jugador"]]:
        a[1] += 1
    _prev[r["jugador"]] = r["division"]
for r in run("SELECT j.alias jugador, COUNT(*) n FROM fact_partida p JOIN dim_fecha f USING(fecha) JOIN dim_jugador j USING(id_jugador) WHERE f.es_profesional=1 AND f.dia_cerrado=1 AND p.fecha<=:hasta AND p.puntaje_final<800 GROUP BY j.alias"):
    DA.setdefault(r["jugador"], [0, 0])[0] = r["n"]
_pd = {}
for r in run("SELECT p.fecha, j.alias jugador, p.puntaje_final x, p.suma_rondas s FROM fact_partida p JOIN dim_fecha f USING(fecha) JOIN dim_jugador j USING(id_jugador) WHERE f.es_profesional=1 AND f.dia_cerrado=1 AND p.fecha<=:hasta"):
    _pd.setdefault(r["fecha"], {})[r["jugador"]] = (r["x"], r["s"])
H2H = {}
for _a in {j for m in _pd.values() for j in m}:
    _w, _n, _rv = 0, 0, {}
    for m in _pd.values():
        if _a in m:
            for _b, vb in m.items():
                if _b != _a:
                    g = _rv.setdefault(_b, [0, 0]); _n += 1
                    if m[_a] > vb: g[0] += 1; _w += 1
                    elif m[_a] < vb: g[1] += 1
    H2H[_a] = (sum(1 for g in _rv.values() if g[0] > g[1]), round(100 * _w / _n) if _n else 0)
DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
DIASL = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
_dw = {}
for r in run("SELECT j.alias jugador, p.fecha, p.puntaje_final x FROM fact_partida p JOIN dim_fecha f USING(fecha) JOIN dim_jugador j USING(id_jugador) WHERE f.es_profesional=1 AND f.dia_cerrado=1 AND p.fecha<=:hasta"):
    _dw.setdefault(r["jugador"], [[] for _ in range(7)])[datetime.date.fromisoformat(r["fecha"]).weekday()].append(r["x"])
_gw = [[v for L in _dw.values() for v in L[k]] for k in range(7)]
grp_dia = [sum(L) / len(L) if L else None for L in _gw]
CH_TOT = {}  # Challenge: amateurismo + profesionalismo (excepcion explicita); solo dias con titulo valido
for _v in ("v_titulos_challenge", "v_titulos_challenge_amateur"):
    for r in run(f"SELECT jugador, titulos, segundos, terceros FROM {_v}"):
        a = CH_TOT.get(r["jugador"], (0, 0, 0)); CH_TOT[r["jugador"]] = (a[0] + r["titulos"], a[1] + r["segundos"], a[2] + r["terceros"])
CH_N = {r["jugador"]: run("SELECT COUNT(*) n FROM fact_challenge c JOIN dim_jugador j USING(id_jugador) JOIN v_challenge_dia d USING(fecha) WHERE d.es_profesional=1 AND j.alias=:j AND c.fecha<=:hasta", j=r["jugador"])[0]["n"] for r in D["challenge"]}
grp_ronda = {r["ronda"]: r["prom"] for r in run("SELECT ronda, AVG(puntaje) prom FROM v_puntaje WHERE es_profesional=1 AND fecha<=:hasta GROUP BY ronda")}

(AQUI / "salida").mkdir(exist_ok=True)
# nombres de categoria para mostrar en la ppt: plural, con tildes y sin parentesis (las consultas siguen usando el nombre de la base)
import re as _re
from categorias_pres import C as _CP, TIPO_GRUPO as _TG
_NOM = {k: v[0] for k, v in _CP.items() if k != v[0]}
_RX = _re.compile("|".join(_re.escape(k) for k in sorted(_NOM, key=lambda k: -len(k))))
def _sinp(x):
    if isinstance(x, str): return _RX.sub(lambda m: _NOM[m.group(0)], x)
    if isinstance(x, list): return [_sinp(i) for i in x]
    if isinstance(x, dict): return {k: _sinp(v) for k, v in x.items()}
    return x
D = _sinp(D)
# hover: definicion y lugares de ejemplo (los mas frecuentes del torneo, de paises distintos)
CATTIP = {}
for _id, _cat in con.execute("SELECT id_categoria, categoria FROM dim_categoria"):
    _ej, _ps = [], set()
    for _l, _p, _n in con.execute("""SELECT l.lugar, l.pais, COUNT(a.id_ubicacion) n FROM puente_lugar_categoria p JOIN dim_lugar l USING(id_lugar)
        LEFT JOIN fact_aparicion a USING(id_lugar) WHERE p.id_categoria=? GROUP BY l.id_lugar ORDER BY n DESC, l.lugar""", (_id,)):
        if _p in _ps: continue
        _ps.add(_p); _ej.append(_l.split(",")[0])
        if len(_ej) == 4: break
    CATTIP[_CP[_cat][0]] = {"d": _CP[_cat][1], "e": _ej, "t": _TG[_cat]}
# regiones subcontinentales (y continentes): definicion con sus paises y lugares de ejemplo
for _col, _tipo, _txt in (("region", "Regiones subcontinentales", "Subregión de {c}: "), ("continente", "Continentes", "")):
    for _z, _c in con.execute(f"SELECT DISTINCT {_col}, continente FROM dim_lugar"):
        if _z in CATTIP: continue
        _ej, _ps = [], []
        for _l, _p, _n in con.execute(f"""SELECT l.lugar, l.pais, COUNT(a.id_ubicacion) n FROM dim_lugar l LEFT JOIN fact_aparicion a USING(id_lugar) WHERE l.{_col}=? GROUP BY l.id_lugar ORDER BY n DESC, l.lugar""", (_z,)):
            if _p in _ps: continue
            _ps.append(_p)
            if len(_ej) < 4: _ej.append(_l.split(",")[0])
        _d = (_txt.format(c=_c) + "países con lugares en el torneo: " + ", ".join(sorted(_ps)[:12]) + ("…" if len(_ps) > 12 else "") + ".")
        CATTIP[_z] = {"d": _d[0].upper() + _d[1:], "e": _ej, "t": _tipo}
json.dump(D, open(AQUI / "salida" / ("datos-demo.json" if DEMO else "datos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)

# ---------------- mapa mundi ----------------
LEG = AQUI.parent / "scripts" / "legacy"


def eq(lon, lat):
    lam, ph = math.radians(lon), math.radians(lat)
    t = math.asin(math.sqrt(3) / 2 * math.sin(ph))
    A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
    return (2 * math.sqrt(3) * lam * math.cos(t) / (3 * (9 * A4 * t**8 + 7 * A3 * t**6 + 3 * A2 * t**3 + A1)), t * (A1 + A2 * t**2 + t**6 * (A3 + A4 * t**2)))


def color_esc(v, lo, hi):
    return f"hsl({max(0, min(1, (v-lo)/((hi-lo) or 1)))*120:.0f},78%,58%)"



def _pines():
    rows = run("SELECT id_lugar, lugar, pais, lat, lon, fecha, jugador, ROUND(AVG(puntaje),1) AS p FROM v_puntaje WHERE es_profesional=1 AND fecha<=:hasta GROUP BY id_lugar, fecha, jugador")
    g = {}
    for r in rows:
        d = g.setdefault(r["id_lugar"], {"lugar": r["lugar"], "pais": r["pais"], "lat": r["lat"], "lon": r["lon"], "dias": {}})
        d["dias"].setdefault(r["fecha"], {})[r["jugador"]] = r["p"]
    pines = []
    for d in g.values():
        todos = [v for dia in d["dias"].values() for v in dia.values()]
        if len(todos) < 6: continue
        d["prom"] = sum(todos) / len(todos)
        pines.append(d)
    return pines


PINES = _pines()
PINES_JS = json.dumps([{"n": f'{flag(p["pais"])} {p["lugar"]}', "m": round(p["prom"], 1),
                        "d": [[f[8:10] + "/" + f[5:7], sorted(([j, v] for j, v in dia.items()), key=lambda t: -t[1])] for f, dia in sorted(p["dias"].items())]} for p in PINES],
                      ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

def mapa_mundial(capa=None):
    ancho, alto = 1000, 520
    sx = 1000 / (2 * eq(180, 0)[0]) * 0.98
    X = lambda lon, lat: (ancho / 2 + eq(lon, lat)[0] * sx, alto / 2 - eq(lon, lat)[1] * sx)
    o = [f'<svg viewBox="0 0 {ancho} {alto}" class="ch">']
    lat = list(range(-90, 91, 5))
    o.append('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in [X(-180, a) for a in lat] + [X(180, a) for a in reversed(lat)]) + f'" fill="#0b1636" stroke="{GRILLA2}"/>')
    for ring in (LEG / "land.txt").read_text().strip().split("|"):
        p = [tuple(float(v) for v in q.split(",")) for q in ring.split()]
        segs, cur = [], [p[0]]
        for a, b in zip(p, p[1:]):
            if abs(b[0] - a[0]) > 180:
                cur.append((180 if a[0] > 0 else -180, a[1])); segs.append(cur); cur = [((180 if b[0] > 0 else -180), b[1]), b]
            else:
                cur.append(b)
        segs.append(cur)
        for sg in segs:
            if len(sg) > 2:
                o.append('<polygon points="' + " ".join(f"{X(a,b)[0]:.1f},{X(a,b)[1]:.1f}" for a, b in sg) + f'" fill="{SURF2}" stroke="#40529a" stroke-width="0.5" vector-effect="non-scaling-stroke"/>')
    pines = PINES
    vals = sorted(p["prom"] for p in pines)
    lo, hi = vals[len(vals) // 20], vals[-len(vals) // 20 - 1]
    cuts = [vals[len(vals) * k // 4] for k in (1, 2, 3)]
    tier = lambda p: sum(p["prom"] >= c for c in cuts)   # 0 = cuarto mas dificil ... 3 = cuarto mas facil
    for i, p in sorted(enumerate(pines), key=lambda t: t[1]["prom"]):
        x, y = X(p["lon"], p["lat"])
        if capa is not None and tier(p) != capa:
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{APAGADO}" opacity="0.35"/>')
        else:
            o.append(f'<circle class="pin" data-p="{i}" cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{color_esc(p["prom"],lo,hi)}" stroke="{NOCHE}" stroke-width="0.8" opacity="0.95" vector-effect="non-scaling-stroke"/>')
    o.append('</svg>')
    if capa is None:
        REG = [("Mundo", None), ("América del Norte", (-170, -50, 14, 72)), ("América Central", (-118, -58, 5, 34)), ("América del Sur", (-85, -32, -57, 14)),
               ("Europa", (-25, 45, 28, 67)), ("África", (-20, 55, -36, 38)), ("Asia", (25, 160, -12, 58)), ("Oceanía", (110, 180, -48, 15))]
        bt = []
        for nom, bx in REG:
            if bx is None:
                vb = (0, 0, ancho, alto)
            else:
                pts = [X(lo_, la_) for lo_ in (bx[0], (bx[0] + bx[1]) / 2, bx[1]) for la_ in (bx[2], (bx[2] + bx[3]) / 2, bx[3])]
                x0, x1, y0, y1 = min(p[0] for p in pts), max(p[0] for p in pts), min(p[1] for p in pts), max(p[1] for p in pts)
                w, h = x1 - x0, y1 - y0
                w, h = max(w, h * ancho / alto) * 1.08, max(h, w * alto / ancho) * 1.08
                vb = ((x0 + x1) / 2 - w / 2, (y0 + y1) / 2 - h / 2, w, h)
            bt.append(f'<button class="zb{" on" if bx is None else ""}" data-vb="{" ".join(f"{v:.1f}" for v in vb)}">{nom}</button>')
        return (f'<div class="mz">' + "".join(o) +
                f'<div class="zbar">{"".join(bt)}</div></div>')
    return "".join(o)


# ---------------- diapositivas ----------------
CHISTES = ["Los pines no se mueven solos, aunque a veces parezca.", "Ningún jugador fue lastimado en la confección de estas estadísticas.", "Si un número te molesta, culpá al mapa.",
           "Los resultados pueden variar según el nivel de excusas.", "Ya sabíamos que Guadalcanal era difícil. Ahora tenemos pruebas.", "Mejor promedio no es lo mismo que mejor persona. Casi siempre.",
           "Cualquier parecido con la realidad es porque la realidad también juega al Maptap.", "Hecho con cariño y un poquito de rencor.", "Esta diapositiva fue revisada por un comité de ex-finalistas.",
           "Pregunta frecuente: «¿y por qué en mi pantalla no se veía el cartel?»", "Sí, el 100 existe. No, no es fácil.", "Ningún huso horario fue maltratado.",
           "No se aceptan reclamos después del cierre del día.", "Dato curioso: el mapa no tiene la culpa.", "Que la ronda 5 nos agarre confesados."]
class Bucket:
    def __init__(self):
        self.items, self.key, self.etapa = [], "00", ""

    def append(self, h):
        self.items.append((self.key, len(self.items), h))

    def __len__(self):
        return len(self.items)


S = Bucket()


def etapa_de(key):
    k = int(float(key))
    return "1 · Todos en conjunto" if 10 <= k < 30 else "2 · Abrimos por jugador" if 30 <= k < 50 else "4 · Premios" if 60 <= k < 70 else ""


def sec(key, etapa=None):
    """Orden top-down: 1x = todos en conjunto, 3x = abrimos por jugador, 5x = perfiles, 6x = premios, 7x = cierre."""
    S.key = key
    if etapa is not None:
        S.etapa = etapa


def slide(titulo, sub, cuerpo, clase="", chiste=True, hero=True, cabecera=None):
    n = len(S)
    pie = f'<div class="foot">{CHISTES[n % len(CHISTES)]}</div>' if chiste else ""
    cab = cabecera if cabecera else f'<div class="hero">{f"<div class=kicker>{etapa_de(S.key)}</div>" if etapa_de(S.key) else ""}<h1>{titulo}</h1>{f"<p class=sub>{sub}</p>" if sub else ""}</div>' if (hero or cabecera) else ""
    S.append(f'<section class="slide {clase}">{cab}<div class="body">{cuerpo}</div>{pie}</section>')


# A. resumen
sec("00", "")
S.append(f"""<section class="slide cover portada"><div class="hero big"><div class="kicker">Torneo Maptap · Copa Petit</div><h1>La temporada de Maptap</h1>
<p class="sub">Once personas, un mapa y ninguna se acuerda dónde queda Guadalcanal.</p></div>
</section>""")

c100 = run("SELECT SUM(puntaje=100) c, COUNT(*) n FROM v_puntaje WHERE fecha<=:hasta")[0]
pf_grupo = run("SELECT AVG(p.puntaje_final) a FROM fact_partida p WHERE p.fecha<=:hasta")[0]["a"]
T_ = run("SELECT (SELECT COUNT(*) FROM fact_partida WHERE fecha<=:hasta) pa, (SELECT COUNT(*) FROM fact_aparicion WHERE fecha<=:hasta) ub, (SELECT COUNT(DISTINCT id_lugar) FROM fact_aparicion WHERE fecha<=:hasta) lu, (SELECT AVG(puntaje) FROM v_puntaje WHERE fecha<=:hasta) pr, (SELECT COUNT(*) FROM dim_fecha WHERE dia_cerrado=1 AND fecha<=:hasta) di")[0]
nc = lambda ic, t, n, sub: f'<div class="nc"><div class="ic">{ic}</div><span>{t}</span><b>{n}</b><small>{sub}</small></div>'
sec("05", "1 · Todos en conjunto")
slide("El torneo en números", "Resumen de todo el grupo",
      '<div class="ncs">' + nc(I_BALON, "Partidas jugadas", miles(T_["pa"]), f"en {T_['di']} días") + nc(I_PIN, "Ubicaciones", miles(T_["ub"]), "5 por día")
      + nc(I_GLOBO, "Lugares distintos", miles(T_["lu"]), "algunos se repitieron") + nc(I_BLANCO, "Promedio por ronda", ent(T_["pr"]), "puntos, de 0 a 100")
      + nc(I_BANDERA, "Puntaje final promedio", ent(pf_grupo), "por partida") + nc(I_CIEN, "Rondas con 100", miles(c100["c"]), f"el {ent(100 * c100['c'] / c100['n'])}% de las rondas") + "</div>")

PRO = "fecha<=:hasta"  # todas las fechas (amateur + profesional)
dist5 = run(f"SELECT CASE WHEN puntaje=100 THEN 100 ELSE CAST(puntaje/5 AS INT)*5 END t, COUNT(*) n FROM v_puntaje WHERE {PRO} GROUP BY t ORDER BY t")
dm = {r["t"]: r["n"] for r in dist5}
tot = sum(dm.values())
sec("12")
slide("¿Cuánto sacamos en cada ronda?", f"Porcentaje de las {miles(tot)} rondas jugadas que cayó en cada tramo de 5 puntos",
      columnas([(("100" if t == 100 else f"{t}-{t+4}"), 100 * dm.get(t, 0) / tot) for t in list(range(0, 100, 5)) + [100]], "Puntaje de la ronda (0 a 100)", "% de las rondas", chico=True, pct=True))
distF = run("SELECT CAST(p.puntaje_final/25 AS INT)*25 t, COUNT(*) n FROM fact_partida p WHERE p.fecha<=:hasta GROUP BY t ORDER BY t")
totF = sum(r["n"] for r in distF)
sec("10", "1 · Todos en conjunto")
slide("¿Cuánto sacamos por día?", f"De las {miles(totF)} partidas jugadas, qué porcentaje terminó con cada puntaje final, agrupado de a 25 puntos (por ejemplo 900-924)",
      columnas([(f"{r['t']}-{r['t']+24}", 100 * r["n"] / totF) for r in distF], "Puntaje final de la partida", "% de las partidas", chico=True, pct=True))


def ciudades(sql, **p):
    return "<br>".join(lug(r["lugar"], r["pais"]) for r in run(sql, **p))


LD = "SELECT l.lugar, l.pais FROM fact_aparicion a JOIN dim_lugar l USING(id_lugar) WHERE a.fecha=:f ORDER BY a.ronda"
lugares_dia = lambda f: [lug(r["lugar"], r["pais"]) for r in run(LD, f=f)]
peores = run("SELECT jugador, fecha, lugar, pais, puntaje FROM v_puntaje WHERE fecha<=:hasta ORDER BY puntaje, fecha LIMIT 8")
sec("39")
slide("Las peores rondas de la historia", "Las 8 rondas con menor puntaje y dónde fueron",
      tabla(["Jugador", "Puntaje", "Día", "Ubicación"], [(f"<b>{esc(r['jugador'])}</b>", f"<b>{r['puntaje']}</b>", f_fecha(r["fecha"]), lug(r["lugar"], r["pais"])) for r in peores]), clase="rows")
PART = "SELECT j.alias jugador, p.fecha, p.puntaje_final x FROM fact_partida p JOIN dim_jugador j USING(id_jugador) WHERE p.fecha<=:hasta ORDER BY p.puntaje_final {o}, p.suma_rondas {o}, p.fecha LIMIT 3"
pdia = lambda f: run("SELECT AVG(puntaje_final) a FROM fact_partida WHERE fecha=:f", f=f)[0]["a"]
fp = lambda r: (f"<b>{esc(r['jugador'])}</b>", f"<b>{r['x']}</b>", f_fecha(r["fecha"]), coma(pdia(r["fecha"])), "<br>".join(f"{lug(l, p)} · <b>{pt}</b>" for p, l, pt in lug_pts(r["jugador"], r["fecha"])))
sec("40")
slide("Las peores partidas de la historia", "Las 3 partidas con menor puntaje final y las ciudades de ese día",
      tabla(["Jugador", "Puntaje final", "Día", "Promedio del día", "Ciudades (puntos de cada ronda)"], [fp(r) for r in run(PART.format(o="ASC"))]), clase="rows dias partidas")

# temporada: puntaje total (todas las fechas; media movil de 15 dias, solo con ventana completa)
MMG = 15
vm = mmv([r["x"] for r in dgf], MMG)
npl = {r["fecha"]: r["n"] for r in run("SELECT fecha, COUNT(*) n FROM fact_partida WHERE fecha<=:hasta GROUP BY fecha")}
pts = [(r["fecha"], r["x"], m) for r, m in zip(dgf, vm) if m is not None]
prom_t = run("SELECT AVG(puntaje_final) a FROM fact_partida WHERE fecha<=:hasta")[0]["a"]
dias_ok = [r for r in dgf if npl[r["fecha"]] >= 8]
mejor, peor = max(dias_ok, key=lambda r: r["x"]), min(dias_ok, key=lambda r: r["x"])
pico, bajo = max(pts, key=lambda t: t[2]), min(pts, key=lambda t: t[2])
card = lambda a, b, c: f'<div class="stat"><span>{a}</span><b>{b}</b><small>{c}</small></div>'
stats = '<div class="stats">' + card("Promedio total", ent(prom_t), "puntaje final") + card("Mejor día", ent(mejor["x"]), f_fecha(mejor["fecha"])) + card("Peor día", ent(peor["x"]), f_fecha(peor["fecha"])) \
    + "</div>"
sec("11")
_tv = [x for _, x, _ in pts] + [prom_t]
_t0, _t1 = math.floor((min(_tv) - 10) / 10) * 10, math.ceil((max(_tv) + 25) / 10) * 10
slide("La temporada: puntaje total", "Promedio del puntaje final de todo el grupo cada día",
      lineas([("Diario", ORO, [(i, x) for i, (_, x, _) in enumerate(pts)], 3, 1)],
                     ymin=_t0, ymax=_t1, yticks=[v for v in range(int(_t0), int(_t1) + 1) if v % 50 == 0], alto=470, xticks=[(i, f_fecha(f)) for i, (f, _, _) in enumerate(pts) if i % 7 == 0], xtitle="Día", ytitle="Puntaje final promedio",
                     hlines=[(prom_t, "", HUESO)], leyenda=(f"Promedio del grupo: {ent(prom_t)}", HUESO)))

# ---- analisis detallado por ronda (grupo completo, todas las fechas)
PESO = {1: 1, 2: 1, 3: 2, 4: 3, 5: 3}
rr = run("SELECT ronda, AVG(puntaje) a, COUNT(*) n, SUM(puntaje=100) c100 FROM v_puntaje WHERE fecha<=:hasta GROUP BY ronda ORDER BY ronda")
sec("13.1")
slide("Ronda por ronda: promedio", "Promedio de todo el grupo en cada ronda (entre paréntesis, cuánto vale la ronda en el puntaje final)",
      lineas([("Promedio", ORO, [(r["ronda"], r["a"]) for r in rr], 3.5, 1)], ymin=80, ymax=100, yticks=[80, 85, 90, 95, 100], xmargin=0.35, xticks=[(r["ronda"], f"Ronda {r['ronda']} (×{PESO[r['ronda']]})") for r in rr],
             xtitle="Número de ronda", ytitle="Promedio del grupo (pts)", marcas=True, etq=d1))
tot100 = sum(r["c100"] for r in rr)
sec("13.3")
slide("Ronda por ronda: los 100", f"De los {miles(tot100)} 100 que se sacaron, en qué ronda cayó cada uno",
      torta([(f"Ronda {r['ronda']} (×{PESO[r['ronda']]})", r["c100"], PAL[r["ronda"] - 1], f"{miles(r['c100'])} rondas con 100") for r in rr]))


def extremos_dia(f):
    rs = run("SELECT j.alias jugador, p.puntaje_final x FROM fact_partida p JOIN dim_jugador j USING(id_jugador) WHERE p.fecha=:f", f=f)
    mn, mx = min(r["x"] for r in rs), max(r["x"] for r in rs)
    nom = lambda t: nv(", ".join(r["jugador"] for r in rs if r["x"] == t), f"{t} pts")
    return nom(mx), nom(mn), sum(r["x"] for r in rs) / len(rs)


def fila_dia(r):
    mej, pe, pf = extremos_dia(r["fecha"])
    return (f"<b>{f_fecha(r['fecha'])}</b>", f"<b>{coma(r['prom'])}</b>", f"<b>{coma(pf)}</b>", "<br>".join(lugares_dia(r["fecha"])), mej, pe)


# B. rankings
sec("29", "")
S.append("""<section class="slide cover"><div class="hero big"><div class="kicker">2 · Abrimos por jugador</div><h1>Ahora, uno por uno</h1><p class="sub">Del grupo en conjunto pasamos a mirar a cada jugador</p></div>
<div class="foot">Se acabó el anonimato.</div></section>""")
sec("30", "2 · Abrimos por jugador")
TOT = run("SELECT r.jugador, SUM(r.posicion=1) AS oros, SUM(r.posicion=2) AS platas, SUM(r.posicion=3) AS bronces FROM v_ranking_dia r JOIN dim_fecha f USING(fecha) WHERE f.dia_cerrado=1 AND r.fecha<=:hasta GROUP BY r.jugador ORDER BY oros DESC, platas DESC, bronces DESC")
TOTD = {r["jugador"]: (r["oros"], r["platas"], r["bronces"]) for r in TOT}
sem_t = {}
for r in run("SELECT semana_inicio, jugador, puntos FROM v_copa_semanal WHERE semana_inicio<=:hasta ORDER BY semana_inicio, puntos DESC"):
    sem_t.setdefault(r["semana_inicio"], {})[r["jugador"]] = r["puntos"]
sem_t_ok = sorted(s for s in sem_t if (datetime.date.fromisoformat(s) + datetime.timedelta(days=6)).isoformat() <= HASTA)
mes_t = {}
for r in run("SELECT anio_mes, jugador, oros, platas, bronces, promedio FROM v_medallero_mes ORDER BY anio_mes, oros DESC, platas DESC, bronces DESC, promedio DESC"):
    mes_t.setdefault(r["anio_mes"], []).append(r)
mes_t_ok = [m for m in mes_t if (lambda y, mo: (datetime.date(y + (mo == 12), mo % 12 + 1, 1) - datetime.timedelta(days=1)).isoformat() <= HASTA)(*map(int, m.split("-")))]
sem_ok = sorted(s for s in sem if (datetime.date.fromisoformat(s) + datetime.timedelta(days=6)).isoformat() <= HASTA)
meses = {}
for r in D["mensual"]:
    meses.setdefault(r["anio_mes"], []).append(r)
meses_ok = []
for m in meses:
    y, mo = map(int, m.split("-"))
    if (datetime.date(y + (mo == 12), mo % 12 + 1, 1) - datetime.timedelta(days=1)).isoformat() <= HASTA:
        meses_ok.append(m)
jugadores = [r["jugador"] for r in D["titulos"]]


def tabla_medallero(cnt):
    orden_m = sorted(jugadores, key=lambda j: (-cnt[j][0], -cnt[j][1], -cnt[j][2], j))
    return tabla(["Persona", M_ORO, M_PLATA, M_BRONCE], [(f"<b>{esc(j)}</b>", *cnt[j]) for j in orden_m])


cw = {j: [0, 0, 0] for j in jugadores}
for s_ in sem_ok:
    for i, (j, _) in enumerate(sorted(sem[s_].items(), key=lambda kv: -kv[1])[:3]):
        cw[j][i] += 1
cm = {j: [0, 0, 0] for j in jugadores}
for m in meses_ok:
    for i, r in enumerate(meses[m][:3]):
        cm[r["jugador"]][i] += 1
cwt = {j: [0, 0, 0] for j in jugadores}
for s_ in sem_t_ok:
    for i, (j, _) in enumerate(sorted(sem_t[s_].items(), key=lambda kv: -kv[1])[:3]):
        cwt[j][i] += 1
cmt = {j: [0, 0, 0] for j in jugadores}
for m in mes_t_ok:
    for i, r in enumerate(mes_t[m][:3]):
        cmt[r["jugador"]][i] += 1


# C. geografia: una diapositiva por continente (con sus regiones y paises computables)
def top3(lista):
    z = {}
    for r in lista:
        z.setdefault(r["zona"], []).append(r)
    return {k: [(r["jugador"], d1(r["prom"])) for r in sorted(v, key=lambda r: -r["prom"])[:3]] for k, v in z.items()}


def dueno(col):
    d = {}
    for r in run(f"SELECT {col} z, continente c, COUNT(*) n FROM v_puntaje WHERE es_profesional=1 AND fecha<=:hasta GROUP BY z, c"):
        if r["z"] not in d or r["n"] > d[r["z"]][1]:
            d[r["z"]] = (r["c"], r["n"])
    return {k: v[0] for k, v in d.items()}


reg_c, pais_c = dueno("region"), dueno("pais")
T_c, T_r, T_p = top3(D["topz"]["continente"]), top3(D["topz"]["region"]), top3(D["topz"]["pais"])
zc_all = {r["zona"]: r for r in D["zona_cont"]}
sec("19", "1 · Todos en conjunto")
SUB_BOX = "Puntajes de todas las rondas del grupo"
vals_c = {}
for r in run("SELECT continente z, puntaje p FROM v_puntaje WHERE es_profesional=1 AND fecha<=:hasta"):
    vals_c.setdefault(r["z"], []).append(r["p"])
bx_c = sorted([(c, stats_box(vals_c[c])) for c in orden_cont], key=lambda t: t[1]["med"])
slide("Dificultad por continente", SUB_BOX, boxplot([("", c, st) for c, st in bx_c], ymin=max(0, math.floor((min(st["p10"] for _, st in bx_c) - 5) / 10) * 10)))
nreg = {c: sum(1 for r in D["zona_reg"] if reg_c.get(r["zona"]) == c and r["zona"] != c) for c in orden_cont}


def filas_dif(conts):
    fd_, cl_ = [], []
    for cont in conts:
        fd_.append((f"<b>{esc(cont)}</b>", f"<b>{coma(zc_all[cont]['prom'])}</b>")); cl_.append("cont")
        for r in sorted([r for r in D["zona_reg"] if reg_c.get(r["zona"]) == cont and r["zona"] != cont], key=lambda r: r["prom"]):
            fd_.append((f'{esc(r["zona"])} <small class="tag2">región</small>', coma(r["prom"]))); cl_.append("reg")
    return fd_, cl_


sec("20", "1 · Todos en conjunto")
paises_c = {r["zona"] for r in D["zona_pais"]}
vals_p = {}
for r in run("SELECT pais z, puntaje p FROM v_puntaje WHERE es_profesional=1 AND fecha<=:hasta"):
    if r["z"] in paises_c:
        vals_p.setdefault(r["z"], []).append(r["p"])
bx_p = sorted([(z, stats_box(v)) for z, v in vals_p.items()], key=lambda t: t[1]["med"])
slide("Dificultad por país", SUB_BOX + " · países con 5 o más ubicaciones", boxplot([(flag(z), z, st) for z, st in bx_p], ymin=max(0, math.floor((min(st["p10"] for _, st in bx_p) - 5) / 10) * 10)))
# ---- Kahoot: QR de entrada y, por zona, una pregunta y su podio
KFILE = AQUI / "kahoot.txt"
kl = [l.strip() for l in KFILE.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")] if KFILE.exists() else []
K_URL, K_PIN = (kl[0] if kl else "https://kahoot.it"), (kl[1] if len(kl) > 1 else "")


def qr_svg(url, px=300):
    cache = AQUI / "qr_cache.json"
    data = None
    try:
        import cv2
        m = cv2.QRCodeEncoder.create().encode(url)
        data = [[1 if v < 128 else 0 for v in row] for row in m.tolist()]
        cache.write_text(json.dumps({url: data}), encoding="utf-8")
    except Exception:
        if cache.exists():
            data = json.loads(cache.read_text(encoding="utf-8")).get(url)
    if not data:
        return '<div class="small">(No se pudo generar el QR: falta OpenCV y no hay copia guardada)</div>'
    n, q_ = len(data), 4
    rects = "".join(f'<rect x="{x+q_}" y="{y+q_}" width="1.02" height="1.02"/>' for y, row in enumerate(data) for x, v in enumerate(row) if v)
    return f'<svg viewBox="0 0 {n+2*q_} {n+2*q_}" width="{px}" height="{px}" shape-rendering="crispEdges"><rect width="100%" height="100%" fill="#fff"/><g fill="#000">{rects}</g></svg>'


sec("37", "2 · Abrimos por jugador")
S.append(f"""<section class="slide cover"><div class="hero big"><div class="kicker">Kahoot</div><h1>¡Todos entran ahora!</h1><p class="sub">Escaneá el QR con el celular y adiviná quién lidera cada zona</p></div>
<div class="body"><div class="qrbox">{qr_svg(K_URL)}<div class="qrtxt"><b>{esc(K_URL.replace('https://', '').replace('http://', ''))}</b>{f'<div>PIN: <b>{esc(K_PIN)}</b></div>' if K_PIN else ''}</div></div></div>
<div class="foot">Sin Kahoot no hay podio. Sin podio no hay gloria.</div></section>""")


def podio_visual(top):
    top = list(top) + [None] * (3 - len(top))
    col = lambda t, cls, med: f'<div class="pcol {cls}"><div class="nm">{esc(t[0]) if t else "—"}</div><div class="vl">{esc(t[1]) if t else ""}</div><div class="blk">{med}</div></div>'
    return '<div class="podium">' + col(top[1], "p2", M_PLATA) + col(top[0], "p1", M_ORO) + col(top[2], "p3", M_BRONCE) + "</div>"


NQ = [0]


def kahoot_zona(nombre, pregunta, top):
    NQ[0] += 1
    _em = re.findall("[\U0001F1E6-\U0001F1FF]{2}|\U0001F30A|\U0001F310", pregunta)  # el emoji dentro del titulo con degradado se ve como silueta dorada: va al kicker
    pregunta = re.sub("[\U0001F1E6-\U0001F1FF]{2} ?|\U0001F30A ?|\U0001F310 ?", "", pregunta)
    S.append(f"""<section class="slide cover"><div class="hero big"><div class="kicker">Kahoot · Pregunta {NQ[0]}{(" · " + " ".join(_em)) if _em else ""}</div><h1>{pregunta}</h1><p class="sub">Respondé desde tu celular: ¿quién tiene el mejor promedio por ronda?</p></div>
<div class="foot">Tenés 20 segundos. El que duda, pierde.</div></section>""")
    slide(nombre, "Top 3 de jugadores por promedio por ronda", podio_visual(top), clase="podio")


for c in orden_cont:
    if T_c.get(c):
        kahoot_zona(esc(c), f"¿Quién lidera en {esc(c)}?", T_c[c])


def zonas_top(zs, T, own):
    out = []
    for c in orden_cont:
        for r in sorted([r for r in zs if own.get(r["zona"]) == c and r["zona"] != c], key=lambda r: r["zona"]):
            if T.get(r["zona"]):
                out.append((r["zona"], T[r["zona"]]))
    return out


for z, tp in zonas_top(D["zona_pais"], T_p, pais_c):
    kahoot_zona(f"{flag(z)} {esc(z)}", f"¿Quién lidera en {flag(z)} {esc(z)}?", tp)


def fila_ub(r):
    rs = run("SELECT jugador, puntaje FROM v_puntaje WHERE id_ubicacion=:u", u=r["id_ubicacion"])
    mn, mx = min(x["puntaje"] for x in rs), max(x["puntaje"] for x in rs)
    nom = lambda t: ", ".join(x["jugador"] for x in rs if x["puntaje"] == t)
    n_mx = sum(1 for x in rs if x["puntaje"] == mx)
    mej = nv("Todos", f"{mx} pts") if mn == mx else nv(nom(mx) if n_mx <= 3 else f"Todos menos {nom(mn)}", f"{mx} pts")
    pe = "—" if mn == mx else nv(nom(mn), f"{mn} pts")
    return (f"<b>{lug(r['lugar'], r['pais'])}</b>", f_fecha(r["fecha"]), f"<b>{d1(r['prom'])}</b>", mej, pe)


sec("21", "1 · Todos en conjunto")
slide("Las ubicaciones más fáciles", "Las 5 con mejor promedio del grupo, y quién fue el mejor y el peor ahí",
      tabla(["Lugar", "Día", "Promedio", "El mejor", "El peor"], [fila_ub(r) for r in list(reversed(D["ubic"]))[:5]]), clase="rows")
sec("22")
slide("Las ubicaciones más difíciles", "Las 5 con peor promedio del grupo, y quién fue el mejor y el peor ahí",
      tabla(["Lugar", "Día", "Promedio", "El mejor", "El peor"], [fila_ub(r) for r in D["ubic"][:5]]), clase="rows")
sec("23")
for _c, _t, _st in ((3, "Los lugares que menos nos costaron", "El cuarto más fácil para el grupo"), (2, "Los lugares más bien fáciles", "El segundo cuarto más fácil"), (1, "Los lugares más bien difíciles", "El segundo cuarto más difícil"), (0, "Los lugares que más nos costaron", "El cuarto más difícil para el grupo")):
    slide(_t, f"{_st} · pasá el mouse por un pin para ver cuándo salió y cómo le fue a cada uno", mapa_mundial(_c), clase="wide mapa")
slide("El mapa del año", "Todos los lugares que salieron, coloreados según lo difícil que fueron para el grupo · tocá un continente para acercar y pasá el mouse por un pin", mapa_mundial(), clase="wide mapa")

# F. perfiles (solo profesionalismo; orden alfabetico). Las fotos van en presentacion/fotos/<Alias>.jpg|png
import base64
FOTOS = AQUI / "fotos"


def foto(j):
    if DEMO:
        return None
    for ext, mime in (("jpg", "jpeg"), ("jpeg", "jpeg"), ("png", "png"), ("webp", "webp")):
        p = FOTOS / f"{j}.{ext}"
        if p.exists():
            return f'<img src="data:image/{mime};base64,{base64.b64encode(p.read_bytes()).decode()}">'
    return None


sec("49", "3 · Cada uno en detalle")
S.append("""<section class="slide cover"><div class="hero big"><div class="kicker">3 · Cada uno en detalle</div><h1>Los perfiles</h1><p class="sub">Los 11 jugadores, en orden alfabético</p></div>
<div class="foot">Ahora sí: nombres, apellidos y excusas.</div></section>""")
sec("50", "3 · Cada uno en detalle")
FRASES = ["En {F} se mueve como en su casa; en {K}, como turista sin mapa.", "Si cae {F}, sonríe. Si cae {K}, mira la pantalla como quien lee un contrato.", "{F}: territorio conquistado. {K}: territorio por conquistar (o por evitar).",
          "Pidan {F} y lo van a ver brillar; pidan {K} y lo van a ver rezar.", "Fortaleza: {F}. Kryptonita: {K}. Y a veces cae una y el otro se pone nervioso.", "Con {F} no hay dudas; con {K}, hay dudas, excusas y un poco de café."]
for idx, (jug, P) in enumerate(D["perfiles"].items()):
    H = HIST[jug]
    col = PAL[sorted(HIST).index(jug) % 11]
    av0 = foto(jug) or esc(jug[0])
    jv = [pc[(c, jug)]["prom"] if (c, jug) in pc and pc[(c, jug)]["n"] >= 5 else None for c in orden_cont]
    sin = [c for c, v in zip(orden_cont, jv) if v is None]
    chip = lambda a, b: f'<div class="chip"><b>{a}</b><span>{b}</span></div>'
    m = medallas.get(jug, {"oros": 0, "platas": 0, "bronces": 0})
    tot = TOTD.get(jug, (0, 0, 0))
    dh = div_hab[jug]
    sinll = lambda z: re.sub(r"\s*\([^)]*\)", "", z) if re.search(r"Latitud|[Ll]at\b|\blat\||[Ll]on\b|\blon ", z) else z
    lf = lambda L, cls: "".join(f'<li class="{cls}"><span>{esc(sinll(r["zona"]))}</span><span class="pp"><i>{d1(r["prom"])}</i><b>{("+" if r["dif"]>0 else "")}{coma(r["dif"])}</b></span></li>' for r in L)
    fraseF = P["fort"][0]["zona"] if P["fort"] else "—"
    fraseD = P["deb"][0]["zona"] if P["deb"] else "—"
    corto = lambda z: re.sub(r"\s*\(.*?\)", "", z)
    chiste = FRASES[idx % len(FRASES)].format(F=f"<b>{esc(corto(fraseF))}</b>", K=f"<b>{esc(corto(fraseD))}</b>")
    mom = lambda L: tabla(["Fecha", "Lugar", "Puntaje", "Resto"], [(f_fecha(r['fecha']), f"<b style='white-space:nowrap;font-size:{min(100, 3000 // max(len(r['lugar']), 1))}%'>{lug(r['lugar'], r['pais'])}</b>", f"<b>{r['puntaje']}</b>", ent(r["puntaje"] - r["dif"])) for r in L]) if L else "<p class='small'>Sin datos todavía.</p>"
    mf = P["mmf"]
    wd = [(sum(L) / len(L) if len(L) >= 3 else None) for L in _dw.get(jug, [[]] * 7)]
    _v = [v for _, v in mf] + [v for v in wd if v is not None] + [P["hf"]]
    _sp = (max(_v) - min(_v)) * 0.15
    _Y0, _Y1 = min(_v) - _sp, max(_v) + _sp  # mismo eje vertical en ambos graficos
    _hl = [(P["hf"], "Su promedio", APAGADO)]
    ch_mf = lineas([(jug, col, [(i, v) for i, (_, v) in enumerate(mf)], 3.5, 1)], ymin=_Y0, ymax=_Y1, ancho=640, alto=240, rpad=64, yfmt=lambda v: "", hlines=_hl,
                   xticks=[(i, f_fecha(f)) for i, (f, _) in enumerate(mf) if i % 21 == 0], xtitle="Día", ytitle=f"Media móvil {MM} días", fin=True)
    wd = [(sum(L) / len(L) if len(L) >= 3 else None) for L in _dw.get(jug, [[]] * 7)]
    wv = [v for v in wd if v is not None]
    _vals = [v for v in wd if v is not None]
    _zlo, _zhi = (min(_vals) - (max(_vals) - min(_vals)) * 0.15, max(_vals) + (max(_vals) - min(_vals)) * 0.15) if _vals else (700, 1000)
    wmin = math.floor(min(wv + [g for g in grp_dia if g]) / 20) * 20 if wv else 700
    ch_r = lineas([(jug, col, [(k, v) for k, v in enumerate(wd) if v is not None], 3.5, 1)], ymin=_Y0, ymax=_Y1, ancho=640, alto=240, rpad=64, yfmt=lambda v: "", hlines=_hl,
                  xticks=[(k, DIAS[k]) for k in range(7)], xtitle="Día de la semana", ytitle="Puntaje final promedio", fin=True)
    if wv:
        kb = max(range(7), key=lambda k: wd[k] if wd[k] is not None else -1); kp = min(range(7), key=lambda k: wd[k] if wd[k] is not None else 9999)
        chip_dia = chip(f"<i class=dia>{DIASL[kb].capitalize()}</i> {I_SUBE}", f"mejor día · peor: {DIASL[kp]}")
    else:
        chip_dia = chip("—", "mejor día de la semana")
    _da = DA.get(jug, (0, 0))
    chip_da = chip(f"{_da[0]} {I_BAJA} · {_da[1]} {I_SUBE}", "descensos y ascensos")
    nch = CH_N.get(jug, 0); cr = next((r for r in D["challenge"] if r["jugador"] == jug), None)
    ct = CH_TOT.get(jug, (0, 0, 0))
    chip_ch = chip(f"{ct[0]} {I_TROFEO}", f"títulos de Challenge · {ct[1]} {M_PLATA} · {ct[2]} {M_BRONCE}")
    av = foto(jug) or esc(jug[0])
    cab = lambda texto: f'<div class="phead" style="--c:{col}"><div class="avatar">{av}</div><div><div class="pname">{esc(jug)}</div><div class="tag">{texto}</div></div></div>'
    mj_, pj_ = (P["mej"][0] if P["mej"] else None), (P["peo"][0] if P["peo"] else None)
    MOM = ["Su mejor momento: un {pm} en {Lm} ({dm}). Su peor: un {pp} en {Lp} ({dp}). Hay romances que duelen.", "Brilló con un {pm} en {Lm} ({dm}) y se estrelló con un {pp} en {Lp} ({dp}). Montaña rusa con pin.",
           "Del {pm} en {Lm} ({dm}) al {pp} en {Lp} ({dp}): el mapa también tiene sentido del humor.", "Tocó el cielo con un {pm} en {Lm} ({dm}) y el piso con un {pp} en {Lp} ({dp}). Sin escalas.",
           "Lo mejor: {Lm}, con un {pm} ({dm}). Lo peor: {Lp}, con un {pp} ({dp}). Lo demás, un misterio.", "Un {pm} en {Lm} ({dm}) para el recuerdo; un {pp} en {Lp} ({dp}) para el olvido."]
    mp_txt = (MOM[idx % len(MOM)].format(pm=mj_["puntaje"], Lm=f"{flag(mj_['pais'])} {esc(mj_['lugar'].split(',')[0])}", dm=f"+{coma(mj_['dif'])}", pp=pj_["puntaje"], Lp=f"{flag(pj_['pais'])} {esc(pj_['lugar'].split(',')[0])}", dp=f"-{coma(abs(pj_['dif']))}")
              if mj_ and pj_ else "Todavía sin momentos memorables: el mapa lo está esperando.")
    S.append(f"""<section class="slide cover"><div class="hero big pres" style="--c:{col}"><div class="kicker">Perfil {idx + 1} de {len(D['perfiles'])}</div><div class="avatar big">{av0}</div><h1>{esc(jug)}</h1></div></section>""")
    slide("", "", f"""<div class="chips">{chip(f"{tot[0]} {M_ORO}", f'{m["oros"]} en profesionalismo')}{chip(f"{tot[1]} {M_PLATA}", f'{m["platas"]} en profesionalismo')}{chip(f"{tot[2]} {M_BRONCE}", f'{m["bronces"]} en profesionalismo')}{chip_ch}{chip(H2H.get(jug, (0, 0))[0], f'historiales a favor · {H2H.get(jug, (0, 0))[1]}% 1v1 ganados')}{chip_da}</div>
<div class="two"><div class="card"><h3>Rendimiento por continente</h3>{radar(orden_cont, jv, [gc[c] for c in orden_cont], jug, col)}{'<p class="small">Sin datos en: '+', '.join(sin)+'</p>' if sin else ''}</div>
<div><div class="card good"><h3>{I_SUBE} Donde se luce <small>(puntos sobre el promedio del grupo)</small></h3><ul class="fd">{lf(P['fort'],'up')}</ul></div><div class="card bad"><h3>{I_BAJA} Donde sufre <small>(puntos bajo el promedio del grupo)</small></h3><ul class="fd">{lf(P['deb'],'down')}</ul></div></div></div>""", clase="perfil", hero=False, cabecera=cab(chiste))
    slide("", "", f"""<div class="two"><div class="card"><h3>Rendimiento por día de la semana</h3>{ch_r}</div><div class="card"><h3>Su forma en el tiempo</h3>{ch_mf}</div></div>
<div class="two"><div class="card"><h3>{I_ESTRELLA} Sus 3 mejores momentos <small>(mayor diferencia sobre el resto)</small></h3>{mom(P['mej'])}</div><div class="card"><h3>{I_BAJA} Sus 3 peores momentos <small>(mayor diferencia bajo el resto)</small></h3>{mom(P['peo'])}</div></div>""", clase="perfil", hero=False, cabecera=cab(mp_txt))


# G/H. premios y cierre
def tarj(L):
    return '<div class="cards">' + "".join(f'<div class="card"><div class="ic">{ic}</div><h3>{esc(t)}</h3><b class="win">{esc(j)}</b><p>{esc(v)}</p><p class="small">Se gana por: {esc(f)}</p></div>' for t, ic, f, j, v in L) + "</div>"


sec("60", "4 · Premios")
S.append("""<section class="slide cover"><div class="hero big"><div class="kicker">4 · Premios</div><h1>Premios de cierre</h1><p class="sub">Llegó el momento de entregar los premios de la temporada</p></div>
<div class="foot">Se pide silencio. Las reclamaciones, por escrito.</div></section>""")
sec("61")
for i, p in enumerate(D["premios"], 1):
    S.append(f"""<section class="slide cover"><div class="hero big"><div class="kicker">Premio {i} de {len(D['premios'])}</div><h1>{ic_svg(p['ic'])} {esc(p['t'])}</h1><p class="sub">{esc(p['desc'])}</p>
<p class="nom"><span>LOS NOMINADOS SON</span><b>{' · '.join(esc(n) for n in sorted(x[0] for x in p['nom']))}</b></p></div>
<div class="foot">Redoble de tambores…</div></section>""")
    if p.get("cancha"):
        POS = {1: (50, 84, ""), 2: (26, 58, ""), 3: (74, 58, ""), 4: (26, 24, ""), 5: (74, 24, "")}
        _w = {1: 1, 2: 1, 3: 2, 4: 3, 5: 3}
        rating = sum(v * _w[r] for _, r, v in p["cancha"])
        _rs = max(itertools.permutations(range(1, 6), len(p["sup"])), key=lambda t: (sum(_pr[(n, r)] for n, r in zip(p["sup"], t)), t))
        sup_txt = " · ".join(f"<b>{esc(n)}</b> (Ronda {r} · {ent(_pr[(n, r)])})" for n, r in sorted(zip(p["sup"], _rs), key=lambda t: t[1]))
        jug_h = "".join(f'<div class="pl" style="left:{POS[r][0]}%;top:{POS[r][1]}%"><div class="dot">{ent(v)}</div><b>{esc(j)}</b><span>Ronda {r}</span></div>' for j, r, v in p["cancha"])
        slide(f"{ic_svg(p['ic'])} {esc(p['t'])}", p["alc"] + " · el número es el promedio en esa ronda",
              f'<div class="win2"><div class="cancha"><div class="mc"></div><div class="a1"></div><div class="a2"></div>{jug_h}</div><div class="wv" style="margin-top:14px">Rating del equipo: {ent(rating)}</div><div class="wo" style="margin-top:8px">Suplentes: {sup_txt}</div></div>', clase="winner")
        continue
    _ESP = '<div class="wx esp">'
    _ex = p.get("extra", "")
    ex_a, ex_b = (_ex.split(_ESP)[0], _ESP + _ex.split(_ESP)[1]) if _ESP in _ex else (_ex, "")
    slide(f"{ic_svg(p['ic'])} {esc(p['t'])}", p["alc"],
          f'<div class="win2"><div class="wl">El ganador es</div><div class="wn">{esc(p["j"])}</div><div class="wv">{esc(p["v"])}</div>{ex_a}<div class="wo">Los otros nominados: {" · ".join(f"<b>{esc(n)}</b> ({esc(v)})" for n, v in [x for x in p["nom"] if x[0] not in p["j"].split(", ")][:2])}</div>{ex_b}</div>', clase="winner")
sec("70", "")
S.append(f"""<section class="slide cover"><div class="hero big"><div class="kicker">Torneo Maptap · Copa Petit</div><h1>¡Gracias por jugar!</h1><p class="sub">Nos vemos en el próximo mapa</p></div>
<div class="foot">Gracias por los 100, por las excusas y por no mirar el mapa antes de tirar el pin.</div></section>""")

# ---------------- estilo: estilo.css + fuente Champions Bold + fondos generados ----------------
def _data_svg(svg):
    return 'url("data:image/svg+xml,' + urllib.parse.quote(svg) + '")'


def _fondos():
    rnd = random.Random(2026)
    est = [f'<circle cx="{rnd.uniform(0, 520):.0f}" cy="{rnd.uniform(0, 520):.0f}" r="{rnd.uniform(.5, 1.4):.1f}" fill="#fff" fill-opacity="{rnd.uniform(.18, .6):.2f}"/>' for _ in range(70)]
    est += [f'<path d="M{x} {y - 5}L{x + 1.2} {y - 1.2}L{x + 5} {y}L{x + 1.2} {y + 1.2}L{x} {y + 5}L{x - 1.2} {y + 1.2}L{x - 5} {y}L{x - 1.2} {y - 1.2}Z" fill="#d4af37" fill-opacity=".55"/>' for x, y in [(60, 90), (330, 40), (450, 300), (140, 410), (260, 230), (500, 480)]]
    estrellas = _data_svg('<svg xmlns="http://www.w3.org/2000/svg" width="520" height="520">' + "".join(est) + '</svg>')
    orn = _data_svg('<svg xmlns="http://www.w3.org/2000/svg" width="340" height="14" viewBox="0 0 340 14"><defs><linearGradient id="a" x1="0" x2="1"><stop offset="0" stop-color="#d4af37" stop-opacity="0"/><stop offset="1" stop-color="#d4af37"/></linearGradient>'
                    '<linearGradient id="b" x1="1" x2="0"><stop offset="0" stop-color="#d4af37" stop-opacity="0"/><stop offset="1" stop-color="#d4af37"/></linearGradient></defs>'
                    '<rect x="0" y="6.4" width="146" height="1.3" fill="url(#a)"/><rect x="194" y="6.4" width="146" height="1.3" fill="url(#b)"/>'
                    '<rect x="165" y="2" width="10" height="10" transform="rotate(45 170 7)" fill="#d4af37"/><circle cx="152" cy="7" r="2" fill="#d4af37"/><circle cx="188" cy="7" r="2" fill="#d4af37"/></svg>')
    pz = []
    for _ in range(90):
        x, y = rnd.uniform(10, 1270), rnd.uniform(14, 706)  # todo el alto y sin tocar los bordes: el patron cae en bucle sin costura
        col = rnd.choice(["#d4af37", "#f1d98a", "#b8c2da", "#ffffff", "#d4af37"])
        op = rnd.uniform(.35, .85)
        if rnd.random() < .6:
            pz.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{rnd.uniform(6, 11):.0f}" height="{rnd.uniform(12, 20):.0f}" transform="rotate({rnd.uniform(0, 180):.0f} {x:.0f} {y:.0f})" fill="{col}" fill-opacity="{op:.2f}"/>')
        else:
            pz.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(2.5, 5):.1f}" fill="{col}" fill-opacity="{op:.2f}"/>')
    confeti = _data_svg('<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">' + "".join(pz) + '</svg>')
    return estrellas, orn, confeti


_est, _orn, _conf = _fondos()
_ttf = base64.b64encode((AQUI / "champions-bold" / "champions-bold.ttf").read_bytes()).decode()
CSS = (f'@font-face{{font-family:"Champions";src:url(data:font/ttf;base64,{_ttf}) format("truetype");font-display:block}}\n'
       f':root{{--estrellas:{_est};--orn:{_orn};--confeti:{_conf}}}\n' + (AQUI / "estilo.css").read_text(encoding="utf-8"))
DECK_CSS = ""
TIP_JS = """
(function(){document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.zb');if(!b)return;var mz=b.closest('.mz'),sv=mz.querySelector('svg');
[].forEach.call(mz.querySelectorAll('.zb'),function(x){x.classList.toggle('on',x===b);});
var a=sv.getAttribute('viewBox').split(' ').map(Number),z=b.getAttribute('data-vb').split(' ').map(Number),t0=null,pins=sv.querySelectorAll('.pin');
if(sv.__raf)cancelAnimationFrame(sv.__raf);
function st(t){if(t0===null)t0=t;var p=Math.min(1,(t-t0)/600);p=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;var v=a.map(function(x,i){return x+(z[i]-x)*p;});sv.setAttribute('viewBox',v.join(' '));var r=5/Math.pow(1000/v[2],0.8);for(var i=0;i<pins.length;i++)pins[i].setAttribute('r',r);if(p<1)sv.__raf=requestAnimationFrame(st);}
sv.__raf=requestAnimationFrame(st);});})();

(function(){var P=window.__PINES,t=document.createElement('div');t.id='tip';document.body.appendChild(t);
function mv(e){var w=t.offsetWidth,h=t.offsetHeight,x=e.clientX+16,y=e.clientY+16;if(x+w>innerWidth-8)x=e.clientX-w-16;if(y+h>innerHeight-8)y=innerHeight-h-8;t.style.left=Math.max(8,x)+'px';t.style.top=Math.max(8,y)+'px';}
document.addEventListener('mouseover',function(e){var c=e.target.closest&&e.target.closest('.pin');if(!c){t.style.display='none';return;}var p=P[+c.getAttribute('data-p')];
var h='<b>'+p.n+'</b><i>Promedio del grupo '+String(p.m).replace('.',',')+'</i>';p.d.forEach(function(d){h+='<div class="td">'+d[0]+'</div><div class="tj">'+d[1].map(function(j){return '<span>'+j[0]+' <b>'+String(j[1]).replace('.',',').replace(/,0$/,'')+'</b></span>';}).join('')+'</div>';});
t.innerHTML=h;t.style.display='block';mv(e);});
document.addEventListener('mousemove',function(e){if(t.style.display==='block')mv(e);});})();
"""
DECK_JS = """
(function(){
var W=1280,H=720,deck=document.getElementById('deck'),slides=[].slice.call(deck.querySelectorAll('.slide')),cur=0,cnt=document.getElementById('cnt');
slides.forEach(function(s){var i=document.createElement('div');i.className='inner';while(s.firstChild)i.appendChild(s.firstChild);s.appendChild(i);var b=s.querySelector('.body');if(b&&!s.classList.contains('cover')){var f=document.createElement('div');f.className='fill';while(b.firstChild)f.appendChild(b.firstChild);b.appendChild(f);}});
function lay(f,k){f.style.width=(100/k)+'%';f.style.transform='scale('+k+')';return f.offsetHeight*k;}
function fit(s){var b=s.querySelector('.body');if(!b||s.classList.contains('cover')||s.classList.contains('mapa')){s.setAttribute('data-k','1');return;}var f=b.firstElementChild,av=b.clientHeight,lo=0.35,hi=(s.classList.contains('winner')?1:1.5),k;
if(lay(f,hi)<=av)k=hi;else{for(var i=0;i<14;i++){var m=(lo+hi)/2;if(lay(f,m)<=av)lo=m;else hi=m;}k=lo;}
var h=lay(f,k);f.style.transform='translateY('+Math.max(0,(av-h)/2)+'px) scale('+k+')';s.setAttribute('data-k',k.toFixed(2));}
function scale(){var k=Math.min(innerWidth/W,innerHeight/H);deck.style.transform='scale('+k+')';deck.style.left=((innerWidth-W*k)/2)+'px';deck.style.top=((innerHeight-H*k)/2)+'px';}
var listo=false,tmr=null,dest=document.getElementById('destello');
function show(n){var ant=slides[cur];cur=Math.max(0,Math.min(slides.length-1,n));slides.forEach(function(s,j){s.classList.remove('sale','entra');s.classList.toggle('active',j===cur);});fit(slides[cur]);
if(listo&&ant!==slides[cur]&&!window.__TODAS&&!document.body.classList.contains('printing')&&!matchMedia('(prefers-reduced-motion: reduce)').matches){var tr=slides[cur].getAttribute('data-tr')||'dest',ad=slides.indexOf(ant)<cur?'dir-f':'dir-b';slides.forEach(function(s){s.classList.remove('t-slide','t-fade','t-dest','dir-f','dir-b');});[ant,slides[cur]].forEach(function(s){s.classList.add('t-'+tr,ad);});ant.classList.add('sale');slides[cur].classList.add('entra');if(dest&&tr==='dest'){dest.classList.remove('go');void dest.offsetWidth;dest.classList.add('go');}clearTimeout(tmr);tmr=setTimeout(function(){slides.forEach(function(s){s.classList.remove('sale','entra','t-slide','t-fade','t-dest','dir-f','dir-b');});},620);}
listo=true;cnt.textContent=(cur+1)+' / '+slides.length;history.replaceState(null,'','#'+(cur+1));}
document.addEventListener('keydown',function(e){var k=e.key;if(k==='ArrowRight'||k==='PageDown'||k===' '||k==='Enter'){e.preventDefault();show(cur+1);}else if(k==='ArrowLeft'||k==='PageUp'||k==='Backspace'){e.preventDefault();show(cur-1);}else if(k==='Home')show(0);else if(k==='End')show(slides.length-1);else if(k==='f'||k==='F')fs();});
function fs(){if(document.fullscreenElement)document.exitFullscreen();else document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen();}
document.getElementById('prev').onclick=function(){show(cur-1);};document.getElementById('next').onclick=function(){show(cur+1);};document.getElementById('fs').onclick=fs;
var x0=null;deck.addEventListener('touchstart',function(e){x0=e.touches[0].clientX;});deck.addEventListener('touchend',function(e){if(x0===null)return;var d=e.changedTouches[0].clientX-x0;if(Math.abs(d)>50)show(cur+(d<0?1:-1));x0=null;});
deck.addEventListener('click',function(e){if(e.target.closest('a,button'))return;show(cur+(e.clientX>innerWidth/2?1:-1));});
addEventListener('resize',scale);addEventListener('beforeprint',function(){document.body.classList.add('printing');slides.forEach(fit);});addEventListener('afterprint',function(){document.body.classList.remove('printing');show(cur);});
window.__deck={slides:slides,fit:fit,show:show};
scale();show((parseInt(location.hash.slice(1))||1)-1);
if(location.hash==='#todas'||window.__TODAS){document.documentElement.style.overflow='auto';document.body.style.overflow='auto';document.body.style.zoom=Math.min(1,innerWidth/1280);document.body.classList.add('todas');slides.forEach(function(s){s.classList.add('active');fit(s);});}
})();
"""
def _tr(k):
    """Transicion segun la diapositiva de destino: 1ª seccion y ultimas dos de la apertura por jugador (peores rondas y partidas) = deslizamiento, perfiles = fundido simple, resto (Kahoot, premios, etc.) = fundido con destello."""
    return "slide" if 0 < float(k) < 29 or k in ("39", "40") else "fade" if k in ("49", "50") else ""


cuerpo = "".join(re.sub(r'^<section class="slide', f'<section data-tr="{_tr(k)}" class="slide', h, count=1) if _tr(k) else h for k, _, h in sorted(S.items, key=lambda t: (t[0], t[1])))
out = (f'<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Maptap — fin de año</title><style>{CSS}{DECK_CSS}</style>'
       f'<body><div id="deck">{cuerpo}<div id="destello"></div></div><div id="ui"><button id="prev" title="Anterior (←)">◀</button><span id="cnt"></span><button id="next" title="Siguiente (→)">▶</button><button id="fs" title="Pantalla completa (F)">⛶</button></div><script>window.__PINES={PINES_JS};</script><script>{DECK_JS}{TIP_JS}</script></body></html>')
out += '''<style>#cattip{position:fixed;z-index:99;max-width:340px;background:#0f1a42;color:#f3efe3;border:1px solid #d4af37;border-radius:8px;padding:10px 12px;font:14px/1.35 system-ui,sans-serif;pointer-events:none;display:none;box-shadow:0 6px 18px rgba(0,0,0,.5)}#cattip b{display:block;color:#f1d98a;margin-bottom:4px}#cattip i{display:block;margin-top:6px;color:#b8c2da;font-style:normal}</style><div id="cattip"></div><script>(function(){var T='''+json.dumps(CATTIP, ensure_ascii=False)+''',tip=document.getElementById('cattip');function f(e){var el=e.target;if(!el||el.children.length)return;var k=(el.textContent||'').trim(),t=T[k];if(!t){tip.style.display='none';return;}tip.innerHTML='<b></b>'+t.d+'<i>Ejemplos: '+t.e.join(', ')+'</i>';tip.firstChild.textContent=k+' · '+t.t;tip.style.display='block';var x=e.clientX+14,y=e.clientY+14;if(x+350>innerWidth)x=e.clientX-354;if(y+tip.offsetHeight+10>innerHeight)y=e.clientY-tip.offsetHeight-14;tip.style.left=Math.max(4,x)+'px';tip.style.top=Math.max(4,y)+'px';}document.addEventListener('mousemove',f);document.addEventListener('mouseleave',function(){tip.style.display='none';});})();</script>'''
if DEMO:
    out = out.replace('<div id="deck">', '<div id="demo">VERSIÓN DE PRUEBA · DATOS FICTICIOS</div><div id="deck">', 1).replace('</style>', '#demo{position:fixed;top:0;left:0;right:0;z-index:20;background:#b91c1c;color:#fff;text-align:center;font:700 13px Arial;padding:3px;letter-spacing:.08em}</style>', 1)
nombre = "presentacion-demo.html" if DEMO else "presentacion.html"
(AQUI / "salida" / nombre).write_text(out, encoding="utf-8")
print(f"OK hasta={HASTA} diapositivas={len(S.items)} -> salida/{nombre} ({len(out)//1024} KB)")
