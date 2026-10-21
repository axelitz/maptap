# Presentación de fin de año — Esquema (≈31 diapositivas + anexo)

Período: profesional, 2/9/2026 hasta el último día cerrado. Tono con humor. Cada diapositiva cita al pie la métrica (`id` de `metricas.yaml`) y su muestra mínima.

## A. Resumen (3)
1. **Portada** — título, período, 11 jugadores, cifras clave (a_partidas, a_ubicaciones).
2. **El torneo en números** — promedio del grupo (a_prom_grupo), distribución de puntajes (a_dist_puntajes), récord de 100 en un día (a_record_100_dia).
3. **La temporada día a día** — promedio diario + media móvil (a_prom_diario_grupo); 5 días más fáciles y más difíciles (a_dias_extremos).

## B. Rankings (4)
4. **Ranking general** — promedio nominal y exceso sobre el grupo (prom_nominal, b_exceso_prom).
5. **Precisión y regularidad** — % de 100 y consistencia (b_pct_100, b_desvio_diario); mejor/peor partida (b_mejor_peor_dia).
6. **Medallero** — títulos diarios y medallas (b_ranking_dia_titulos); copas semanales y mensuales (b_copa_semanal, b_copa_mensual); Challenge (b_titulos_challenge).
7. **Divisiones** — trayectoria (b_trayectoria_divisiones). *Requiere reconstruir antes fact_division desde el 2/9 (hoy solo desde el 14/10).*

## C. Geografía top-down (5)
8. **Continentes** — dificultad del grupo y top 3 por continente (c_dificultad_zona, c_top_zona_jugador).
9. **Regiones** — dificultad, top 3 y dispersión entre jugadores (c_dispersion_zona).
10. **Países computables** — dificultad y top 3 (≥5 ubicaciones).
11. **Ubicaciones** — 10 más fáciles y 10 más difíciles (c_dificultad_ubicacion).
12. **Mapas** — mapa mundial y mapa de EE.UU. con dificultad por punto (c_mapa_ubicaciones); mapa de calor jugador × región (c_exceso_zona_jugador).

## D. Agregadores por categoría (3)
13. **Las 47 categorías por dificultad** (d_dificultad_categoria).
14. **Líder por categoría** + matriz jugador × categoría en Dif (d_promedio_categoria_jugador).
15. **Mayores sorpresas** — top 10 positivas y negativas (d_sorpresas).

## E. Rondas y tiempo (2)
16. **Ronda por ronda** — promedios R1…R5, R1+2, R4+5; caída en la ronda 5 (e_prom_ronda, e_caida_ronda5).
17. **Evolución y rachas** — evolución mensual, mayor racha de 900+ y de 100s seguidos (e_prom_mensual, e_racha_900, e_racha_100).

## F. Perfiles (11, uno por jugador)
Plantilla: polar de 8 ejes (Europa, Asia, América del Norte, América del Sur, África, Capitales, Historia, Naturaleza) vs. grupo; media móvil vs. grupo; 5 fortalezas y 5 debilidades; highlights; posición en cada ranking; frase con humor. Métricas: f_polar, e_media_movil_jugador, f_fortalezas_debilidades, f_highlights, f_posiciones_ranking.
18–28. **Un perfil por jugador** (orden: ranking final).

## G. Premios (2)
29. **Premios I** — el más regular, el más viajero, arranca fuerte, cierra fuerte.
30. **Premios II** — el más afectado por la ronda 5, el especialista, el más parejo, el remontador, el rey del 100. Cada tarjeta muestra su fórmula y n (g_premios).

## H. Cierre (1)
31. **Cierre** — campeón de la temporada, agradecimientos, humor.

## Anexo "Cómo se calcula"
Generado automáticamente desde `metricas.yaml` (definición, cálculo, filtros, n mínimo, unidad, redondeo, interpretación), más convenciones generales: puntaje nominal vs. final, exceso, Dif, muestras mínimas, período profesional, exclusión del Challenge del análisis de desempeño.

## Decisiones a confirmar
1. **Copas semanal y mensual**: usan el calendario oficial (semana del 31/8 y mes de septiembre completo incluyen el 1/9, día amateur); el resto del análisis arranca el 2/9. ¿OK?
2. **Divisiones**: hay que reconstruir la historia 2/9–13/10 (todos arrancan en 1ª y se aplican las reglas a los resultados). ¿Lo hago en la Fase 2?
3. **Fecha de corte**: hoy 18/10 (último día cerrado). El 19/10 entra cuando se cierre.

## Estado Fase 1
`metricas.yaml` (38 métricas) y `validar_metricas.py`: las consultas corren sin errores contra `maptap.db` (`python3 validar_metricas.py`). `d_sorpresas`, `f_posiciones_ranking` y `g_premios` se componen en el generador (Fase 2).
