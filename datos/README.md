# MapTap - Modelo de datos

Esquema estrella en SQLite (`maptap.db`) y un CSV por tabla en esta carpeta. Los CSV y la base son equivalentes: se regeneran juntos con `build_db.py`.
Challenge: no se guardan sus ubicaciones ni rondas (no se pueden recuperar por fecha), solo el resultado de cada dia en `fact_challenge`, de donde sale el historial de titulos.

## Tablas y claves

```text
DIMENSIONES
dim_jugador   id_jugador PK | nombre (UNIQUE) | alias (UNIQUE)
dim_fecha     fecha PK (AAAA-MM-DD) | anio_mes | dia_semana | semana_inicio (lunes) | es_profesional (0/1) | dia_cerrado (0/1)
dim_lugar     id_lugar PK (entero estable) | slug (UNIQUE) | lugar | pais | region | continente | lat | lon | dist_buenos_aires_km
dim_categoria id_categoria PK (entero estable) | slug (UNIQUE) | categoria | tipo | descripcion

PUENTE (muchos a muchos)
puente_lugar_categoria   PK (id_lugar, id_categoria)   FK -> dim_lugar, dim_categoria   (una fila por lugar y categoria a la que pertenece)

HECHOS
fact_aparicion  id_ubicacion PK (AAAAMMDD-ronda) | fecha FK -> dim_fecha | ronda 1-5 | id_lugar FK -> dim_lugar   UNIQUE(fecha, ronda)
fact_puntaje    PK (id_ubicacion, id_jugador)   FK -> fact_aparicion, dim_jugador | puntaje 0-100 (nominal, sin multiplicador)
fact_partida    PK (fecha, id_jugador)          FK -> dim_fecha, dim_jugador | puntaje_final | suma_rondas
fact_division   PK (fecha, id_jugador)          FK -> dim_fecha, dim_jugador | division   (foto al cierre de cada dia; 11 filas por dia)
fact_challenge  PK (fecha, id_jugador)          FK -> dim_fecha, dim_jugador | posicion | puntaje | tiempo_s   (solo desde el 28/9; sin ubicaciones)
```

## Relaciones

```text
fact_puntaje --id_ubicacion--> fact_aparicion --id_lugar--> dim_lugar <--id_lugar-- puente_lugar_categoria --id_categoria--> dim_categoria
fact_aparicion --fecha--> dim_fecha
fact_puntaje / fact_partida --id_jugador--> dim_jugador
fact_partida / fact_challenge --fecha--> dim_fecha
fact_challenge --id_jugador--> dim_jugador
```

## Vistas (ya cruzadas, para consultar rapido)

- `v_puntaje`: un puntaje con jugador, fecha, etapa y atributos del lugar.
- `v_puntaje_categoria`: un puntaje por cada categoria del lugar (45 mil filas).
- `v_promedio_categoria`: categoria, jugador, es_profesional, n_rondas, promedio. Responde un ranking por categoria con un solo filtro.
- `v_challenge_dia`: por dia de Challenge, participantes, si el titulo vale (5 o mas participantes y dia cerrado) y el campeon.
- `v_titulos_challenge`: historial acumulado de titulos, segundos y terceros del Challenge, contando solo dias con titulo valido.
- `v_ranking_dia`, `v_copa_semanal`, `v_medallero_mes`: podio y desempate del dia, puntos semanales (solo dias cerrados) y medallero mensual.
- `v_division_actual`: division de cada jugador en el ultimo dia cerrado.
- `v_lugar_flags`: una fila por lugar con los 47 flags 0/1 (columnas c_...), generada a partir de dim_categoria. Los flags NO son columnas de ninguna tabla: agregar una categoria es agregar filas.

## Ejemplos

```sql
-- ranking de una categoria, solo profesionalismo
SELECT jugador, n_rondas, promedio FROM v_promedio_categoria
WHERE categoria = 'Capital nacional' AND es_profesional = 1 ORDER BY promedio DESC;

-- ranking por pais
SELECT jugador, COUNT(*) n, ROUND(AVG(puntaje),1) prom FROM v_puntaje WHERE pais='Japón' GROUP BY jugador ORDER BY prom DESC;
```

## Proceso diario (todo con `scripts/cargar.py`, correr desde `datos/scripts/`)

Los CSV son la fuente de verdad: cada resultado que se recibe se agrega directo a las tablas; no hay que editar nada despues.

```python
import cargar as c
c.dia('2026-10-19', ubicaciones, manual={...})     # 5 ubicaciones exactas (lat, lng, nombre) + rotulado manual de lugares nuevos
c.partida('2026-10-19', 'Toker', [95,100,99,92,95], 954)
c.challenge('2026-10-19', 'Toker', 943, 24.9)
c.cerrar('2026-10-19')                              # cierra el dia y calcula las divisiones
c.reconstruir()                                     # regenera maptap.db y valida todo
```

- Ubicaciones exactas: `extraer_coordenadas.js` (se corre en el navegador sobre maptap.gg) trae lat, lng y nombre de las 5 rondas.
- Lugar nuevo: hay que decidir a mano sus categorias manuales (`reglas.MANUAL`); las demas se calculan solas. La pertenencia a categorias se corrige editando `puente_lugar_categoria.csv`, y `build_db.py` nunca la pisa.
- Divisiones: `fact_division` guarda una foto por cada dia cerrado; `cerrar()` aplica las reglas (ausencia o menos de 800 baja una, mas de 940 sube una, nunca por encima de 1a). Se probo contra el 15, 16 y 17/10 y reproduce las divisiones registradas.
- Mensajes (podios, copa semanal, Challenge, rankings): no se guardan; salen de las vistas y viven en el chat.
- `scripts/legacy/` tiene el pipeline anterior (exports de chat, analisis en md); ya no se usa para cargar datos.

## Reglas de diseno

- Cada dato vive en un solo lugar: los atributos del lugar solo en dim_lugar, el corte del profesionalismo solo en `config.py` (CORTE_PRO).
- Claves enteras estables: un id ya asignado no cambia; los nuevos reciben max+1.
- Un lugar que sale otra vez solo suma una fila en fact_aparicion. Variantes del mismo lugar se unifican con alias en `config.py` (Londres, Toronto, Semey, Titanic).
- Coordenadas exactas de maptap.gg (primera aparicion del lugar; entre apariciones difieren menos de 7 km).
- `build_db.py` falla si hay claves duplicadas, FK rotas, una fecha sin 5 rondas, una partida sin 5 puntajes, una suma de rondas que no coincide o un snapshot de divisiones incompleto.
