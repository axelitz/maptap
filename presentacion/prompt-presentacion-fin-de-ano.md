# PROMPT: Presentación de fin de año de MapTap (análisis top-down del profesionalismo)

## 1. Rol

Sos analista de datos senior y diseñador de presentaciones. Trabajás para Axel, administrador del torneo MapTap (un grupo de WhatsApp de 11 jugadores que juegan todos los días a www.maptap.gg: 5 rondas por día, cada una con una ubicación del mundo, puntaje nominal de 0 a 100 por ronda). Tu trabajo es construir un sistema que genere, con un solo comando, la presentación de fin de año a partir de los datos vigentes, de modo que regenerarla el día de la presentación cueste casi cero tokens y no requiera rehacer nada a mano.

Estilo de trabajo (obligatorio): respuestas concisas, sin relleno; no tomes decisiones unilaterales sobre alcance o formato (preguntá con opciones cerradas cuando algo sea de Axel); no repitas lo que ya sabés; no mandes tablas largas por chat (guardalas en archivos); cuando algo falla, decilo claro y proponé la corrección. Axel es de Argentina: texto en español rioplatense neutro, sin lunfardo excesivo. Los jugadores se nombran por alias: Toker (Nacho), Axel, Feli, Antonio, Lucas, Sandro, Bruno, Ale, Dario, Fede, Martín.

## 2. Objetivo y alcance

Construir la presentación de fin de año con análisis top-down de los jugadores, usando solo el período del profesionalismo (desde 2026-09-02, `dim_fecha.es_profesional = 1`) hasta el último día cerrado disponible al momento de correr. La presentación va de lo más general a lo más particular y saca conclusiones en cada nivel:

1. Resumen general del torneo (cómo le fue al grupo).
2. Rankings generales de jugadores (qué tan bien jugó cada uno).
3. Análisis geográfico y de ubicaciones, también top-down: mundo, continente, región, país, ciudad. Se analiza el desempeño del grupo en forma generalizada (dificultad de las zonas, qué ubicaciones fueron las más fáciles y las más difíciles) y después quién rinde mejor o peor en cada una.
4. Análisis por agregadores no obvios (las 47 categorías de `dim_categoria`).
5. Análisis por ronda (posición de la ronda dentro del día) y por tiempo (evolución, medias móviles, rachas).
6. Perfil individual de cada uno de los 11 jugadores: en qué es bueno y en qué malo, logros y highlights, conclusiones.
7. Premios, curiosidades y cierre.
8. Anexo: cómo se calcula cada dato.

IMPORTANTE: NO armes nada definitivo ahora. Los datos van a estar desactualizados cuando llegue la presentación. Lo que se construye ahora es la estructura, el catálogo de métricas, el generador y las validaciones, corridos con los datos actuales como prueba. El día de la presentación solo se regeneran los datos.

## 3. Fuentes (en orden de prioridad)

Todo sale de la base de datos del proyecto. No leas chats ni archivos .md viejos para obtener datos.

- Base SQLite: `datos/maptap.db` (carpeta del proyecto Maptap). Los CSV equivalentes están en `datos/`. Documentación completa de tablas, claves y vistas: `datos/README.md` (leelo primero).
- Tablas: `dim_jugador`, `dim_fecha`, `dim_lugar`, `dim_categoria`, `puente_lugar_categoria`, `fact_aparicion`, `fact_puntaje` (puntaje nominal por jugador y ronda), `fact_partida` (puntaje final y suma de rondas por jugador y día), `fact_challenge` (resultado diario del Challenge, sin rondas ni ubicaciones), `fact_division` (foto de divisiones al cierre de cada día).
- Vistas: `v_puntaje`, `v_puntaje_categoria`, `v_promedio_categoria`, `v_ranking_dia`, `v_copa_semanal`, `v_medallero_mes`, `v_division_actual`, `v_challenge_dia`, `v_titulos_challenge`, `v_lugar_flags`.
- Reglas del torneo: `maptap-resultados-diarios.md` (sección de reglas al principio). Resumen: divisiones (menos de 800 o ausencia en día cerrado baja una; más de 940 sube una; sin piso), desempate diario por suma simple de las 5 rondas, copa semanal (lunes a domingo, suma de puntos, ausencias = 0), copa mensual (medallas diarias en orden olímpico, desempate por promedio del mes), Challenge excluido del torneo principal (título válido solo con 5 o más participantes).
- Geografía auxiliar: contornos simplificados del mundo y de EE.UU. en `datos/scripts/legacy/land.txt` y `us_states.txt` (formato "lon,lat lon,lat|..." por polígono). Son de baja resolución; si se necesita más calidad, proponelo antes de gastar tokens.
- Definición de regiones y continentes: `maptap-continentes-regiones.txt` y las columnas `region` y `continente` de `dim_lugar` (Europa en 5 regiones, Asia en 5, África en 5, Oceanía en 2, Antártida aparte).
- Análisis previos de referencia (solo para contrastar, no como fuente): `maptap-desempeno-geografico.md`, `maptap-perfiles-jugadores.md`, `maptap-categorias-ranking-profesionalismo.md`, `maptap-rankings-tradicionales-profesionalismo.md`.

## 4. Convenciones de cálculo (aplican a TODO)

- Puntaje de análisis: SIEMPRE el nominal por ronda (0 a 100, de `fact_puntaje`). Nunca el "Final score" multiplicado, salvo en las secciones de torneo (podios, copas, medallero, divisiones), que usan `fact_partida.puntaje_final`.
- Challenge: excluido de todo el análisis de desempeño, ubicaciones y perfiles. Se usa únicamente para el historial de títulos (`v_titulos_challenge`).
- Exceso (comparar sin sesgo de dificultad): puntaje de la ronda del jugador menos el promedio de todos los jugadores en esa misma fecha y ronda. Se usa siempre que se comparen jugadores que no jugaron los mismos días.
- Dif contra uno mismo: promedio del jugador en una zona o categoría menos su promedio general del período. Mide en qué es mejor o peor que "su normal". Es la base de fortalezas y debilidades en los perfiles.
- Muestra mínima: una métrica por jugador y zona o categoría solo entra a un ranking o a un perfil con al menos 10 rondas. Entre 5 y 9 se muestra atenuada y con asterisco. Menos de 5, no se muestra. Cada zona o categoría entra a los tops si al menos un jugador cumple el mínimo. Registrar siempre el n.
- Empates: se ordena por los decimales completos; si siguen empatados, se informa el empate. En rankings diarios el desempate es la suma simple de las 5 rondas.
- Redondeo: un decimal, coma decimal, en presentación; los cálculos usan precisión completa.
- Jugadores del período: los 11 de `dim_jugador`. Los invitados que pasaron brevemente no están en el modelo.
- Los días no jugados no cuentan como 0 en promedios de desempeño. Sí cuentan como 0 en la copa semanal (regla del torneo).

## 5. Estructura propuesta de la presentación (confirmarla con Axel antes de construir)

Cada diapositiva tiene: título que enuncia la conclusión (no solo el tema), un gráfico principal, 2 a 4 líneas de lectura generadas automáticamente, y una nota al pie "Cómo se calcula" con el id de métrica.

A. Resumen del torneo (4 a 6 diapositivas): partidas, rondas y ubicaciones del período; promedio general; evolución diaria del promedio del grupo con media móvil de 7 días; distribución de puntajes por ronda; días más fáciles y más difíciles del grupo; récords (mejor y peor día de cada uno, mayor cantidad de 100 en un día, etc.).
B. Rankings generales (5 a 7): promedio por ronda, puntaje final promedio, porcentaje de 100, consistencia (desvío estándar de los puntajes diarios), medallero de títulos diarios, copas semanales y mensuales, trayectoria de divisiones (gráfico de carrera o "bump chart"), historial de títulos de Challenge.
C. Geografía top-down (8 a 12): mapa mundial con una ubicación por punto coloreada por el promedio de TODO el grupo (dificultad); ranking de dificultad por continente, región y país (solo zonas con muestra suficiente); las 10 ubicaciones más fáciles y las 10 más difíciles; mapa de EE.UU. (es el país con más ubicaciones); después, quién lidera cada continente, región y país (tops de 3) y dónde hay más dispersión entre jugadores. Cada nivel termina con una conclusión: "dónde pierde puntos el grupo" y "dónde hay especialistas".
D. Agregadores por categoría (4 a 6): dificultad del grupo en cada una de las 47 categorías; líder por categoría; matriz jugador por categoría coloreada con el Dif contra uno mismo; las sorpresas más grandes (mayor desvío positivo y negativo con n suficiente).
E. Rondas y tiempo (3 a 5): promedio por posición de ronda (1 a 5) para el grupo y por jugador; ranking por ronda y combinaciones útiles (1 y 2, 4 y 5); evolución mensual; rachas (días seguidos sobre 900, 100 seguidos, etc.).
F. Perfiles (una por jugador, 2 diapositivas cada una): ver sección 6.
G. Premios y curiosidades (2 a 3): premios generados por reglas explícitas (por ejemplo "el más regular", "el más viajero", "el más afectado por la ronda 5"). Cada premio define su fórmula.
H. Anexo: catálogo de métricas renderizado automáticamente desde `metricas.yaml`.

## 6. Perfil individual (plantilla fija, 2 diapositivas por jugador)

Diapositiva 1, ficha: alias, posición en cada ranking general, KPIs (promedio nominal, % de 100, desvío, partidas jugadas, mejor y peor día, títulos, medallas, división actual), gráfico POLAR (radar) con el rendimiento por continente (o por 6 a 8 dimensiones agrupadas de las categorías, a definir) comparado contra el promedio del grupo, y media móvil de 7 días del jugador contra el grupo.
Diapositiva 2, fortalezas y debilidades: las 5 zonas o categorías donde más rinde y las 5 donde menos (Dif contra uno mismo, con n); mapa personal (puntos coloreados por el exceso del jugador en cada ubicación); logros y highlights (mejores partidas, rachas, 100 consecutivos, ubicaciones donde fue el mejor del grupo); 3 conclusiones generadas por reglas ("rinde +X en Y", "su punto débil es Z"). Los textos son plantillas con datos, no redacción libre, para poder regenerarlos sin costo.

## 7. Gráficos requeridos (variedad)

Mapa mundial de puntos (dificultad del grupo; desempeño personal), mapa de EE.UU., gráficos polares (perfiles), medias móviles (grupo e individuales), barras horizontales ordenadas (rankings), mapa de calor jugador por zona o categoría (Dif), histograma y violín o caja (distribución por jugador), dispersión (promedio contra consistencia; dificultad contra dispersión por zona), gráfico de carrera de la copa semanal y bump chart de divisiones, calendario de calor de puntajes diarios, líneas por posición de ronda. Paleta simple y consistente (un color fijo por jugador a lo largo de toda la presentación), tipografía legible, sin decoración innecesaria.

## 8. Formato y economía de tokens

- Formato de salida: UN solo archivo HTML autocontenido (CSS y SVG inline, sin dependencias externas), con navegación por teclado entre diapositivas y estilos de impresión para exportar a PDF desde el navegador. Es el formato más barato de regenerar y compartir.
- Todo se genera con scripts de Python deterministas que leen `datos/maptap.db`. Gráficos con matplotlib exportados a SVG con texto editable (`svg.fonttype = none`) e incrustados en el HTML. Mapas con los contornos de `datos/scripts/legacy`.
- Cero números escritos a mano: cada cifra sale de una consulta. Los textos de lectura y las conclusiones son plantillas con huecos que se llenan con los datos; la redacción manual queda limitada a un archivo `comentarios.md` opcional con notas de Axel por diapositiva.
- Un comando para regenerar todo: `python datos/presentacion/generar.py --hasta AAAA-MM-DD` (por defecto, el último día cerrado). Opciones: `--solo seccion` y `--jugador alias` para regenerar partes. Los gráficos se cachean por hash de datos para no recalcular lo que no cambió.
- Trabajá por etapas y no mandes por chat contenido largo: reportá solo qué se hizo, qué validaciones pasaron y qué decisión falta.

## 9. Catálogo de métricas (obligatorio: CÓMO SE CALCULA)

Creá `datos/presentacion/metricas.yaml`. Cada métrica tiene: `id`, `nombre`, `seccion`, `definicion` (una frase), `calculo` (fórmula exacta y la consulta SQL o la secuencia de pasos), `filtros` (período, exclusiones), `n_minimo`, `unidad`, `redondeo`, `interpretacion` y `grafico`. Ejemplo:

```yaml
- id: prom_nominal
  nombre: Promedio nominal por ronda
  seccion: B
  definicion: Promedio de los puntajes de ronda (0 a 100) de un jugador en el período.
  calculo: "SELECT jugador, AVG(puntaje) FROM v_puntaje WHERE es_profesional=1 GROUP BY jugador"
  filtros: "es_profesional=1; Challenge excluido; hasta el último día cerrado"
  n_minimo: 100
  unidad: puntos (0 a 100)
  redondeo: 1 decimal
  interpretacion: Mayor es mejor; no corrige por dificultad.
  grafico: barras horizontales
```

El generador usa este mismo catálogo para: (a) ejecutar las consultas, (b) escribir la nota al pie de cada diapositiva y (c) armar el anexo. Si cambia una definición, se cambia ahí y se regenera todo igual. Ninguna métrica puede aparecer en la presentación sin estar en el catálogo.

## 10. Validaciones (antes de dar algo por bueno)

- Reconciliar contra valores conocidos: la copa semanal de las semanas pasadas (28/9 al 4/10: Axel 6581, Toker 6488, Sandro 6405; 5/10 al 11/10: Toker 6428, Axel 6396, Fede 6245), los títulos de Challenge y el medallero.
- Chequeos automáticos: suma de rondas igual al total, n por jugador y zona, sin zonas por debajo del mínimo en los tops, todos los jugadores presentes en cada gráfico.
- Un archivo `validaciones.md` con el resultado de cada chequeo y la fecha de corte de los datos. Cada diapositiva muestra al pie la fecha de corte.

## 11. Fases y checkpoints (parar y consultar a Axel en cada uno)

1. Entregar el esquema detallado de diapositivas y el catálogo de métricas (sin código de gráficos). Axel aprueba o ajusta.
2. Entregar el generador y 2 secciones piloto (una general, una geográfica) y un perfil de ejemplo, con datos actuales. Axel valida el diseño.
3. Completar el resto de las secciones y los 11 perfiles. Correr todas las validaciones.
4. Dejar el sistema listo: `README.md` con el procedimiento de regeneración paso a paso (3 comandos como máximo) y el estado de cada sección.
5. El día de la presentación: actualizar datos con la rutina diaria habitual, correr `generar.py` y revisar las validaciones.

Antes de la fase 1, preguntá a Axel con opciones cerradas lo que sea de su decisión: tono de los textos (serio o con humor), cantidad aproximada de diapositivas, qué dimensiones usar en los polares, y si quiere premios o curiosidades.

## 12. Entregables

1. `datos/presentacion/metricas.yaml` (catálogo de métricas con cálculo).
2. `datos/presentacion/generar.py` y módulos (consultas, gráficos, plantillas de texto, HTML).
3. `datos/presentacion/salida/AAAA-MM-DD_presentacion.html` (un solo archivo) y la indicación de cómo exportar a PDF.
4. `datos/presentacion/validaciones.md`.
5. `datos/presentacion/README.md` con el procedimiento de regeneración.
6. Esquema de diapositivas aprobado (`datos/presentacion/esquema.md`).

## 13. Criterios de calidad

- Reproducible: dos corridas con los mismos datos dan el mismo resultado.
- Trazable: cada número se puede rastrear a una métrica del catálogo y a una consulta.
- Honesto con la muestra: nada se presenta como conclusión si no cumple el n mínimo; lo dudoso va atenuado o con asterisco.
- Legible: una idea por diapositiva, conclusión en el título, sin saturar.
- Barato de mantener: regenerar no requiere razonar de nuevo ni escribir texto nuevo.
