# Guía de estilo · Anuario de la Champions

Presentación de fin de año del Torneo Maptap · Copa Petit. Todo el estilo sale de `estilo.css` (CSS), `generar.py` (colores de los gráficos SVG, íconos y fondos generados) y la fuente `champions-bold/champions-bold.ttf`.

## Concepto
Gala de fútbol europeo: azul noche, doble filete dorado, estrellas, títulos solemnes en mayúsculas con letras espaciadas, fichas tipo carta y medallas dibujadas. Inspiración original, sin logos ni marcas reales.

## Paleta (tokens)
| Token | Valor | Uso |
|---|---|---|
| `--noche` | `#070d24` | fondo base |
| `--surf` / `--surf2` | `#0f1a42` / `#17265b` | tarjetas, cabecera de tablas |
| `--oro` | `#d4af37` | acento principal, filetes, números destacados, medalla oro |
| `--oro2` | `#f1d98a` | títulos de tarjeta, etiquetas, brillo del degradado dorado |
| `--plata` | `#b8c2da` | texto secundario, medalla plata |
| `--bronce` | `#c98a54` | medalla bronce |
| `--hueso` | `#f3efe3` | texto principal |
| `--apagado` | `#8f9bbd` | ejes, notas, pie |
| `--bueno` / `--malo` | `#5ddc9a` / `#ff7b7b` | positivo / negativo (siempre con signo o ícono además del color) |

Colores por jugador (gráficos, avatares, portadas de perfil), luminosos sobre azul noche: `#4cc9f0 #ff6b6b #7ae582 #ffb347 #b388ff #ff8fab #2ec4b6 #ffe066 #8ecae6 #f4845f #d0b3e8` (constante `PAL` en `generar.py`).

Los mismos valores están en `generar.py` (`NOCHE, SURF, SURF2, ORO, ORO2, PLATA, BRONCE, HUESO, APAGADO, GRILLA, GRILLA2, BUENO, MALO`) para los gráficos SVG. Si se cambia un color hay que cambiarlo en los dos lados.

## Tipografía
- **Display:** *Champions Bold* (`datos/presentacion/champions-bold/champions-bold.ttf`), embebida en base64 en el HTML. Títulos, nombres, números grandes, kickers y cabeceras de tabla, siempre en mayúsculas con `letter-spacing` de 0,06 a 0,4 em.
- **Cuerpo:** pila del sistema `"Avenir Next", "Segoe UI", "Helvetica Neue", system-ui, Arial` para tablas, subtítulos, textos largos y etiquetas de gráficos.
- La fuente cubre á é í ó ú ü ñ Á É Í Ó Ú Ü Ñ ¿ ¡ % · × º ª y números. No trae flechas, estrellas, círculos ni emojis: esos signos caen automáticamente a la fuente del cuerpo o se dibujan como SVG.
- **Licencia:** el archivo `Befonts-License.txt` dice "Personal Use Only". Sirve para esta presentación interna del torneo; no redistribuir el HTML con la fuente embebida fuera del grupo ni usarla comercialmente.

## Escala (stage 1280×720)
Título de diapositiva 36 px · título de portada 84 px (nombre de perfil 96 px) · número KPI héroe 120 px · número KPI 58 px · número de tarjeta/chip 28 a 34 px · cuerpo y tablas 17 a 19 px · subtítulo 16 px · pie 13 px · mínimo legible en gráficos 12 px (se amplían con el ajuste a pantalla).

## Marco y fondos
- Doble filete dorado en cada diapositiva (`.slide::before` 2 px oro y `::after` 1 px oro translúcido).
- Fondo: dos resplandores azules + estrellas (`--estrellas`, SVG generado con semilla fija) sobre `--noche`.
- Ornamento dorado con rombo bajo cada título (`--orn`).
- Confeti dorado/plata en las diapositivas de ganador (`--confeti`).

## Componentes
- **Tarjeta** (`.card`, `.stat`, `.chip`, `.nc`): fondo azul con degradado suave, borde dorado fino y filete superior dorado de 3 px; radio 8 px; sombra de nivel 1.
- **Tabla** (`.table-box`): cabecera azul con texto dorado en Champions y filete dorado inferior, filas con separador fino y zebra muy tenue, números tabulares.
- **Chips de perfil**: número en Champions dorado con medalla o ícono SVG integrado y subtítulo en plata.
- **Elevación:** tres niveles (`--sombra-1`, `--sombra-2` y sin sombra en fondos); nada de sombras duras.
- **Pie con chiste:** itálica apagada entre dos rombos dorados.
- **Podio:** bloques metálicos (oro, plata, bronce) con medallas SVG.
- **Cancha del equipo ideal:** campo a rayas con marco dorado y fichas de jugador (círculo dorado con el promedio por ronda).

## Íconos (SVG propios, `generar.py`)
`medalla(n, metal)` (oro, plata, bronce, con cinta y relieve), trofeo, estrella, balón, guante, bota, gráfico creciente, pin, globo, blanco, bandera, "100", flechas de ascenso y descenso. Heredan `currentColor` salvo las medallas y las flechas. Las banderas de países siguen siendo emojis.

## Gráficos
Líneas y barras en oro, comparaciones en plata punteada, grilla casi invisible (`GRILLA`), etiquetas de valor en oro claro, boxplot con caja azul y mediana blanca, mapa con océano oscuro y puntos de verde a rojo según dificultad. Animación de entrada sutil, desactivada con `prefers-reduced-motion` y al imprimir.

## Accesibilidad y proyección
Contraste alto de texto claro sobre azul noche, ningún dato solo por color (los positivos y negativos llevan signo y ícono) y tamaños pensados para proyección. Las diapositivas de perfil se escalan a ~0,7 para que entren las dos filas de gráficos y tablas.

## Herramientas de revisión
- `python3 generar.py` genera `salida/presentacion.html` (y `--demo` vía `generar_demo.py`).
- `python3 muestras.py` arma `salida/muestras.html` con una diapositiva de cada tipo apiladas.
- `python3 ver.py 2 4 83` arma `salida/ver.html` con las diapositivas que se indiquen, apiladas.
- `python3 diagnostico.py` arma `salida/diag.html`: mide las 96 diapositivas (escala de ajuste, desbordes del marco, textos cortados) y lo escribe en la consola.
