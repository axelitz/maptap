# Torneo Maptap - Copa Petit

- `informes/`: reportes del torneo (resultados diarios, rankings, copas, podios, perfiles, categorias, divisiones, desempeno geografico).
- `graficos/`: imagenes y mapas (histogramas, mapas mundial y USA, mapa del anio en HTML).
- `datos/`: fuente de verdad.
  - CSV por tabla + `maptap.db` (esquema estrella, ver `datos/README.md`).
  - `scripts/`: carga diaria (`cargar.py`), reglas de categorias (`reglas.py`), nombres en castellano (`nombres_es.py`), construccion de la base (`build_db.py`).
  - `presentacion/`: generador de la presentacion de fin de anio (`generar.py`, `metricas.yaml`, `validar_metricas.py`); resultado en `presentacion/salida/presentacion.html`.
  - `fuentes/`: archivos originales descargados (Natural Earth, volcanes GVP, terremotos USGS, UNESCO).
  - `auditoria/`: revisiones puntuales (anios de fundacion de los lugares).
