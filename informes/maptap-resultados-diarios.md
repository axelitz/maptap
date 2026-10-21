# MapTap - Resultados diarios

Registro operativo para ir cargando resultados diarios del Torneo Maptap - Copa Petit.

Reglas vigentes desde el 2 de septiembre:

- Menos de 800 puntos: desciende una categoria.
- Ausencia en dia cerrado: desciende una categoria.
- Mas de 940 puntos: asciende una categoria.
- Los ascensos son de una categoria por vez.
- Challenge queda excluido.
- Las fotos se actualizan solo cuando se pida explicitamente.
- No hay piso de division: si corresponde descender estando ya en la ultima categoria vigente, se abre una categoria nueva mas abajo (ej: de 5.a a 6.a).
- Tomas Perez Duich (alta 3/10) y Lucas Stella (alta 4/10) fueron plantel fijo brevemente y causaron baja definitiva el 5/10. Plantel vigente desde el 5/10: 11 jugadores.
- REGLA DE OPERACION DIARIA (pedido de Axel, 18/10, OBLIGATORIA, reemplaza las reglas anteriores de carga, ubicaciones y rotulado): los datos viven SOLO en las tablas de `datos/` (CSV = fuente de verdad; `datos/maptap.db` se regenera; claves y documentacion en `datos/README.md`). Este archivo y `maptap-challenge-resultados.md` quedan como archivo historico hasta el 18/10 y YA NO se actualizan. Cada vez que Axel pega un resultado se carga directo a las tablas con `cargar.py` (scripts en `datos/scripts/`; correr desde esa carpeta): (1) primer puntaje de un dia nuevo: `dia(fecha, ubicaciones, manual)` con las 5 ubicaciones EXACTAS (lat, lng, nombre) obtenidas en silencio de maptap.gg con `extraer_coordenadas.js` en el navegador (nunca mencionarlas en el chat: spoiler; si la pagina no esta disponible por diferencia horaria, dejar pendiente y cargarla despues, en silencio). Cada lugar NUEVO exige rotulado manual de las 19 categorias manuales (`reglas.MANUAL`); las de pais, las calculadas y los complementos salen solas. (2) cada partida: `partida(fecha, alias, [5 rondas], final)`; cada Challenge: `challenge(fecha, alias, puntaje, tiempo)` (si hay empate de puntaje, `desempate_challenge`). Lo repetido se ignora solo. (3) al cerrar un dia: `cerrar(fecha)`, que marca el dia y calcula las divisiones del cierre (ausencia o menos de 800 = baja una; mas de 940 = sube una; nunca por encima de 1a). (4) al terminar cada tanda: `reconstruir()` (valida claves, FK, 5 rondas por fecha, 5 puntajes por partida, suma de rondas y corte del profesionalismo; falla si algo no cierra). Los MENSAJES (podio del dia, copa semanal, Challenge, rankings) NO se guardan en archivos: viven solo en el chat. NO calcular promedios ni rankings por categoria cada dia: solo acumular los datos. Las consultas se hacen con SQL sobre las vistas (v_puntaje, v_promedio_categoria, v_ranking_dia, v_copa_semanal, v_medallero_mes, v_division_actual, v_titulos_challenge, etc.). Jugadores por alias: Toker, Axel, Feli, Antonio, Lucas, Sandro, Bruno, Ale, Dario, Fede, Martín (Nacho = Toker). Para la division de cada jugador usar `v_division_actual`; el profesionalismo es `es_profesional` en `dim_fecha` (corte 2026-09-02 definido solo en `config.py`).
- Regla de formato de rankings (pedido de Axel, 15/10, OBLIGATORIA): todo ranking por zona/pais/region se entrega SIEMPRE dentro de un bloque ```text``` para copiar, con titulo y una linea por jugador, los 11 jugadores, sin cantidad de rondas ni asteriscos, promedio nominal con coma decimal y 1 decimal. Titulo y "Nº Nombre" en negrita de WhatsApp (*...*). Ejemplo exacto:
  *Ranking EE.UU.*
  *1º Toker* 97,3
  *2º Feli* 93,6
  ... hasta *11º Dario* 86,5. Nunca entregarlo fuera del bloque copiable.
- Regla de formato del mensaje de Copa Semanal (pedido de Axel, 18/10, OBLIGATORIA): siempre en bloque ```text``` para copiar, asi y nada mas: `🏆 COPA SEMANAL (28/9 al 4/10)`, linea en blanco, `1º Axel 6581`, `2º Toker 6488`, `3º Sandro 6405`. Podio de 3, puntos sin separador de miles, Nacho = Toker. Sin Campeon, sin emoji de calendario, sin seccion Puntos. (El formato de maptap-copas-semanales.md es solo registro historico, no es el mensaje.)
- Resolucion del 29/9: a pedido de Martin Feinsilber (guardias medicas), se revisaron los descensos de los dias 2/9, 5/9, 19/9, 24/9 y 28/9. Se anularon los descensos por ausencia del 19/9, 24/9 y 28/9 (ausencias verificadas). No se hizo lugar al 2/9 (el descenso de ese dia fue por puntaje, jugo y saco 787) ni al 5/9 (jugo, saco 831, no hubo descenso ese dia). Resultado: Martin Feinsilber queda en 3.a division tras la revision (en vez de 6.a).
- Desempate en caso de empate de puntaje final: gana quien tenga mayor sumatoria simple de los puntajes de las rondas individuales (los 5 numeros antes del "Final score").
- Copa Mensual: se ordena por medallas diarias (orden olimpico 1.o, 2.o, 3.o). Desempate posterior: el promedio de puntos del mes (puntos por partida jugada, sobre las jornadas cerradas del mes; las ausencias no cuentan como 0).
- En el mensaje corto, cuando hubo desempate, se pone entre parentesis la sumatoria total de cada uno junto a su puntaje, para que se vea claro quien gano.

Nota: los dias 2/9 al 8/9 se completaron despues, a partir de un export de WhatsApp que el usuario paso. Todos los jugadores arrancaron el 2/9 en 1.a division (primer dia del profesionalismo). Los ascensos/descensos de estos dias fueron reconstruidos aplicando las reglas y se validaron: la simulacion hacia adelante desde el 2/9 llega exactamente al estado de division que ya se conocia para el arranque del 9/9, y los podios de cada dia coinciden con los ya registrados en maptap-podios-diarios.md.

## 2026-09-02

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Axel Itzcovitz | 899 |
| Fede Moia | 852 |
| Bruno Feinsilber | 825 |
| Antonio Santos | 811 |
| Sandro Anello | 810 |
| Ale Feinsilber | 799 |
| Lucas Greco | 791 |
| Martin Feinsilber | 787 |
| Dario Feinsilber | 769 |
| Nacho Toker | Ausente |
| Feli Garabato | Ausente |

Mensaje corto:

```text
www.maptap.gg September 2

🏆 Podio
1º Axel 899
2º Fede 852
3º Bruno 825

⬆️ Ascensos: ninguno
⬇️ Descensos: Ale a 2ª por puntaje · Dario a 2ª por puntaje · Martín a 2ª por puntaje · Lucas a 2ª por puntaje · Nacho a 2ª por ausencia · Feli a 2ª por ausencia
```

## 2026-09-03

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Axel Itzcovitz | 986 |
| Nacho Toker | 985 |
| Sandro Anello | 985 |
| Martin Feinsilber | 980 |
| Ale Feinsilber | 978 |
| Lucas Greco | 974 |
| Bruno Feinsilber | 968 |
| Fede Moia | 955 |
| Antonio Santos | 943 |
| Dario Feinsilber | 912 |
| Feli Garabato | Ausente |

Mensaje corto:

```text
www.maptap.gg September 3

🏆 Podio
1º Axel 986
2º Nacho/Sandro 985
3º Martín 980

⬆️ Ascensos: Nacho a 1ª · Martín a 1ª · Ale a 1ª · Lucas a 1ª
⬇️ Descensos: Feli a 3ª por ausencia
```

## 2026-09-04

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Nacho Toker | 899 |
| Axel Itzcovitz | 890 |
| Lucas Greco | 873 |
| Sandro Anello | 867 |
| Ale Feinsilber | 836 |
| Bruno Feinsilber | 827 |
| Dario Feinsilber | 824 |
| Antonio Santos | 707 |
| Feli Garabato | Ausente |
| Fede Moia | Ausente |
| Martin Feinsilber | Ausente |

Mensaje corto:

```text
www.maptap.gg September 4

🏆 Podio
1º Nacho 899
2º Axel 890
3º Lucas 873

⬆️ Ascensos: ninguno
⬇️ Descensos: Antonio a 2ª por puntaje · Feli a 4ª por ausencia · Fede a 2ª por ausencia · Martín a 2ª por ausencia
```

## 2026-09-05

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Nacho Toker | 922 |
| Fede Moia | 879 |
| Axel Itzcovitz | 847 |
| Antonio Santos | 839 |
| Ale Feinsilber | 835 |
| Martin Feinsilber | 831 |
| Sandro Anello | 826 |
| Dario Feinsilber | 824 |
| Lucas Greco | 821 |
| Feli Garabato | Ausente |
| Bruno Feinsilber | Ausente |

Mensaje corto:

```text
www.maptap.gg September 5

🏆 Podio
1º Nacho 922
2º Fede 879
3º Axel 847

⬆️ Ascensos: ninguno
⬇️ Descensos: Feli a 5ª por ausencia · Bruno a 2ª por ausencia
```

## 2026-09-06

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Nacho Toker | 986 |
| Axel Itzcovitz | 959 |
| Fede Moia | 956 |
| Dario Feinsilber | 919 |
| Bruno Feinsilber | 892 |
| Ale Feinsilber | 856 |
| Feli Garabato | 827 |
| Antonio Santos | 814 |
| Lucas Greco | 810 |
| Sandro Anello | 789 |
| Martin Feinsilber | 786 |

Mensaje corto:

```text
www.maptap.gg September 6

🏆 Podio
1º Nacho 986
2º Axel 959
3º Fede 956

⬆️ Ascenso: Fede a 1ª
⬇️ Descensos: Sandro a 2ª por puntaje · Martín a 3ª por puntaje
```

## 2026-09-07

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Nacho Toker | 888 |
| Feli Garabato | 862 |
| Sandro Anello | 834 |
| Fede Moia | 815 |
| Axel Itzcovitz | 814 |
| Bruno Feinsilber | 763 |
| Dario Feinsilber | 760 |
| Lucas Greco | 739 |
| Antonio Santos | 718 |
| Ale Feinsilber | 659 |
| Martin Feinsilber | Ausente |

Mensaje corto:

```text
www.maptap.gg September 7

🏆 Podio
1º Nacho 888
2º Feli 862
3º Sandro 834

⬆️ Ascensos: ninguno
⬇️ Descensos: Bruno a 3ª por puntaje · Dario a 3ª por puntaje · Lucas a 2ª por puntaje · Antonio a 3ª por puntaje · Ale a 2ª por puntaje · Martín a 4ª por ausencia
```

## 2026-09-08

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Martin Feinsilber | 979 |
| Axel Itzcovitz | 951 |
| Sandro Anello | 949 |
| Feli Garabato | 946 |
| Lucas Greco | 941 |
| Nacho Toker | 940 |
| Ale Feinsilber | 938 |
| Antonio Santos | 936 |
| Dario Feinsilber | 929 |
| Bruno Feinsilber | Ausente |
| Fede Moia | Ausente |

Mensaje corto:

```text
www.maptap.gg September 8

🏆 Podio
1º Martín 979
2º Axel 951
3º Sandro 949

⬆️ Ascensos: Martín a 3ª · Sandro a 1ª · Feli a 4ª · Lucas a 1ª
⬇️ Descensos: Bruno a 4ª por ausencia · Fede a 2ª por ausencia
```

## 2026-09-09

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Feli Garabato | 946 |
| Nacho Toker | 944 |
| Axel Itzcovitz | 903 |
| Antonio Santos | 897 |
| Lucas Greco | 878 |
| Sandro Anello | 877 |
| Bruno Feinsilber | 875 |
| Ale Feinsilber | 868 |
| Dario Feinsilber | 859 |
| Fede Moia | 794 |
| Martin Feinsilber | Ausente |

Mensaje corto:

```text
www.maptap.gg September 9

🏆 Podio
1º Feli 946
2º Nacho 944
3º Axel 903

⬆️ Ascenso: Feli a 3ª
⬇️ Descensos: Martín a 4ª por ausencia · Fede a 3ª
```

## 2026-09-10

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Lucas Greco | 925 |
| Feli Garabato | 915 |
| Sandro Anello | 914 |
| Nacho Toker | 908 |
| Bruno Feinsilber | 871 |
| Ale Feinsilber | 868 |
| Dario Feinsilber | 868 |
| Martin Feinsilber | 856 |
| Antonio Santos | 847 |
| Fede Moia | 831 |
| Axel Itzcovitz | 820 |

Mensaje corto:

```text
www.maptap.gg September 10

🏆 Podio
1º Lucas 925
2º Feli 915
3º Sandro 914

⬆️ Ascensos: ninguno
⬇️ Descensos: ninguno
```

## 2026-09-11

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Nacho Toker | 934 |
| Feli Garabato | 932 |
| Fede Moia | 913 |
| Lucas Greco | 891 |
| Sandro Anello | 885 |
| Antonio Santos | 879 |
| Bruno Feinsilber | 875 |
| Ale Feinsilber | 861 |
| Axel Itzcovitz | 860 |
| Dario Feinsilber | 748 |
| Martin Feinsilber | Ausente |

Mensaje corto:

```text
www.maptap.gg September 11

🏆 Podio
1º Nacho 934
2º Feli 932
3º Fede 913

⬆️ Ascensos: ninguno
⬇️ Descensos: Dario por puntaje · Martín por ausencia
```

## 2026-09-12

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Fede Moia | 976 |
| Nacho Toker | 965 |
| Tío Igi | 955 |
| Lucas Greco | 954 |
| Bruno Feinsilber | 952 |
| Martin Feinsilber | 950 |
| Dario Feinsilber | 938 |
| Feli Garabato | 937 |
| Antonio Santos | 933 |
| Ale Feinsilber | 931 |
| Sandro Anello | 920 |
| Axel Itzcovitz | 891 |

Alta nueva:

- Tío Igi entra en 5.ª, la division mas baja ocupada al inicio del dia, y asciende a 4.ª por hacer 955.

Mensaje corto:

```text
www.maptap.gg September 12

🏆 Podio
1º Fede 976
2º Nacho 965
3º Tío Igi 955

⬆️ Ascensos: Fede a 2ª · Bruno a 3ª · Martín a 4ª · Tío Igi a 4ª
⬇️ Descensos: ninguno
```

## 2026-09-13

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Feli Garabato | 957 |
| Nacho Toker | 936 |
| Ale Feinsilber | 935 |
| Lucas Greco | 896 |
| Tío Igi | 885 |
| Antonio Santos | 881 |
| Axel Itzcovitz | 868 |
| Fede Moia | 868 |
| Sandro Anello | 860 |
| Dario Feinsilber | 846 |
| Bruno Feinsilber | 829 |
| Martin Feinsilber | 827 |

Notas:

- Se descartaron resultados de Challenge.

Mensaje corto:

```text
www.maptap.gg September 13

🏆 Podio
1º Feli 957
2º Nacho 936
3º Ale 935

⬆️ Ascenso: Feli a 2ª
⬇️ Descensos: ninguno
```

## 2026-09-14

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Lucas Greco | 959 |
| Bruno Feinsilber | 957 |
| Feli Garabato | 954 |
| Martin Feinsilber | 953 |
| Sandro Anello | 952 |
| Ale Feinsilber | 945 |
| Tío Igi | 942 |
| Nacho Toker | 933 |
| Fede Moia | 932 |
| Dario Feinsilber | 932 |
| Axel Itzcovitz | 917 |
| Antonio Santos | 910 |

Mensaje corto:

```text
www.maptap.gg September 14

🏆 Podio
1º Lucas 959
2º Bruno 957
3º Feli 954

⬆️ Ascensos: Feli a 1ª · Bruno a 2ª · Martín a 3ª · Ale a 1ª · Tío Igi a 3ª
⬇️ Descensos: ninguno
```

## 2026-09-15

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Nacho Toker | 924 |
| Lucas Greco | 914 |
| Axel Itzcovitz | 910 |
| Ale Feinsilber | 909 |
| Martin Feinsilber | 894 |
| Feli Garabato | 876 |
| Sandro Anello | 874 |
| Antonio Santos | 853 |
| Fede Moia | 835 |
| Bruno Feinsilber | 828 |
| Dario Feinsilber | 802 |
| Tío Igi | Ausente |

Mensaje corto:

```text
www.maptap.gg September 15

🏆 Podio
1º Nacho 924
2º Lucas 914
3º Axel 910

⬆️ Ascensos: ninguno
⬇️ Descenso: Tío Igi a 4ª por ausencia
```

## 2026-09-16

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Nacho Toker | 958 |
| Axel Itzcovitz | 956 |
| Sandro Anello | 938 |
| Feli Garabato | 911 |
| Antonio Santos | 867 |
| Dario Feinsilber | 862 |
| Lucas Greco | 856 |
| Martin Feinsilber | 854 |
| Fede Moia | 852 |
| Ale Feinsilber | 803 |
| Bruno Feinsilber | 631 |
| Tío Igi | Ausente |

Mensaje corto:

```text
www.maptap.gg September 16

🏆 Podio
1º Nacho 958
2º Axel 956
3º Sandro 938

⬆️ Ascensos: ninguno
⬇️ Descensos: Bruno a 3ª por puntaje · Tío Igi a 5ª por ausencia
```

## 2026-09-17

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Nacho Toker | 967 |
| Lucas Greco | 964 |
| Axel Itzcovitz | 963 |
| Ale Feinsilber | 962 |
| Feli Garabato | 956 |
| Sandro Anello | 953 |
| Fede Moia | 947 |
| Antonio Santos | 928 |
| Dario Feinsilber | 916 |
| Bruno Feinsilber | 910 |
| Martin Feinsilber | 867 |

Notas:

- Tío Igi causa baja definitiva del torneo a partir de esta fecha. No vuelve a figurar en pendientes ni en la tabla de dias siguientes. Su historial previo (hasta el 16/9) queda registrado tal cual.

Mensaje corto:

```text
www.maptap.gg September 17

🏆 Podio
1º Nacho 967
2º Lucas 964
3º Axel 963

⬆️ Ascenso: Fede a 1ª
⬇️ Descensos: ninguno
```

## 2026-09-18

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Sandro Anello | 926 |
| Axel Itzcovitz | 904 |
| Nacho Toker | 903 |
| Bruno Feinsilber | 892 |
| Feli Garabato | 885 |
| Fede Moia | 878 |
| Lucas Greco | 872 |
| Ale Feinsilber | 855 |
| Antonio Santos | 828 |
| Dario Feinsilber | 782 |
| Martin Feinsilber | Ausente |

Mensaje corto:

```text
www.maptap.gg September 18

🏆 Podio
1º Sandro 926
2º Axel 904
3º Nacho 903

⬆️ Ascensos: ninguno
⬇️ Descensos: Dario a 5ª por puntaje · Martín a 4ª por ausencia
```

## 2026-09-19

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Axel Itzcovitz | 958 |
| Nacho Toker | 929 |
| Feli Garabato | 928 |
| Ale Feinsilber | 910 |
| Bruno Feinsilber | 901 |
| Sandro Anello | 894 |
| Lucas Greco | 892 |
| Fede Moia | 848 |
| Dario Feinsilber | 844 |
| Antonio Santos | 822 |
| Martin Feinsilber | Ausente |

Mensaje corto:

```text
www.maptap.gg September 19

🏆 Podio
1º Axel 958
2º Nacho 929
3º Feli 928

⬆️ Ascensos: ninguno
⬇️ Descenso: Martín a 5ª por ausencia
```

## 2026-09-20

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Nacho Toker | 966 |
| Feli Garabato | 955 |
| Ale Feinsilber | 954 |
| Fede Moia | 952 |
| Bruno Feinsilber | 916 |
| Axel Itzcovitz | 906 |
| Martin Feinsilber | 877 |
| Sandro Anello | 872 |
| Antonio Santos | 871 |
| Lucas Greco | 865 |
| Dario Feinsilber | 840 |

Mensaje corto:

```text
www.maptap.gg September 20

🏆 Podio
1º Nacho 966
2º Feli 955
3º Ale 954

⬆️ Ascensos: ninguno
⬇️ Descensos: ninguno
```

## 2026-09-21

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Nacho Toker | 986 |
| Axel Itzcovitz | 978 |
| Fede Moia | 976 |
| Feli Garabato | 975 |
| Sandro Anello | 971 |
| Ale Feinsilber | 941 |
| Lucas Greco | 939 |
| Bruno Feinsilber | 931 |
| Dario Feinsilber | 891 |
| Antonio Santos | 884 |
| Martin Feinsilber | 877 |

Mensaje corto:

```text
www.maptap.gg September 21

🏆 Podio
1º Nacho 986
2º Axel 978
3º Fede 976

⬆️ Ascensos: ninguno
⬇️ Descensos: ninguno
```

## 2026-09-22

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Nacho Toker | 950 |
| Feli Garabato | 930 |
| Lucas Greco | 928 |
| Antonio Santos | 907 |
| Axel Itzcovitz | 906 |
| Martin Feinsilber | 903 |
| Fede Moia | 899 |
| Dario Feinsilber | 873 |
| Ale Feinsilber | 869 |
| Bruno Feinsilber | 847 |
| Sandro Anello | 834 |

Mensaje corto:

```text
www.maptap.gg September 22

🏆 Podio
1º Toker 950
2º Feli 930
3º Lucas 928

⬆️ Ascensos: ninguno
⬇️ Descensos: ninguno
```

## 2026-09-23

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Ale Feinsilber | 933 |
| Nacho Toker | 933 |
| Feli Garabato | 927 |
| Sandro Anello | 900 |
| Axel Itzcovitz | 879 |
| Dario Feinsilber | 867 |
| Lucas Greco | 856 |
| Fede Moia | 844 |
| Martin Feinsilber | 832 |
| Antonio Santos | 830 |
| Bruno Feinsilber | 812 |

Mensaje corto:

```text
www.maptap.gg September 23

🏆 Podio
1º Ale 933 (469)
2º Toker 933 (468)
3º Feli 927

⬆️ Ascensos: ninguno
⬇️ Descensos: ninguno
```

## 2026-09-24

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Axel Itzcovitz | 955 |
| Nacho Toker | 938 |
| Dario Feinsilber | 904 |
| Feli Garabato | 890 |
| Lucas Greco | 867 |
| Antonio Santos | 867 |
| Ale Feinsilber | 800 |
| Sandro Anello | 793 |
| Bruno Feinsilber | 773 |
| Fede Moia | 757 |
| Martin Feinsilber | Ausente |

Mensaje corto:

```text
www.maptap.gg September 24

🏆 Podio
1º Axel 955
2º Toker 938
3º Dario 904

⬆️ Ascensos: ninguno
⬇️ Descensos: Sandro a 2ª por puntaje · Bruno a 4ª por puntaje · Fede a 2ª por puntaje · Martín a 6ª por ausencia
```

## 2026-09-25

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Nacho Toker | 984 |
| Feli Garabato | 976 |
| Fede Moia | 975 |
| Ale Feinsilber | 964 |
| Axel Itzcovitz | 956 |
| Antonio Santos | 951 |
| Lucas Greco | 947 |
| Martin Feinsilber | 929 |
| Bruno Feinsilber | 913 |
| Sandro Anello | 909 |
| Dario Feinsilber | 873 |

Mensaje corto:

```text
www.maptap.gg September 25

🏆 Podio
1º Toker 984
2º Feli 976
3º Fede 975

⬆️ Ascensos: Antonio a 2ª por puntaje · Fede a 1ª por puntaje
⬇️ Descensos: ninguno
```

## 2026-09-26

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Antonio Santos | 949 |
| Fede Moia | 935 |
| Axel Itzcovitz | 930 |
| Dario Feinsilber | 914 |
| Nacho Toker | 913 |
| Sandro Anello | 911 |
| Ale Feinsilber | 909 |
| Lucas Greco | 897 |
| Bruno Feinsilber | 868 |
| Martin Feinsilber | 855 |
| Feli Garabato | Ausente |

Mensaje corto:

```text
www.maptap.gg September 26

🏆 Podio
1º Antonio 949
2º Fede 935
3º Axel 930

⬆️ Ascensos: Antonio a 1ª por puntaje
⬇️ Descensos: Feli a 2ª por ausencia
```

## 2026-09-27

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Feli Garabato | 983 |
| Sandro Anello | 980 |
| Bruno Feinsilber | 976 |
| Nacho Toker | 969 |
| Martin Feinsilber | 968 |
| Antonio Santos | 964 |
| Ale Feinsilber | 963 |
| Lucas Greco | 960 |
| Fede Moia | 940 |
| Axel Itzcovitz | 926 |
| Dario Feinsilber | 891 |

Mensaje corto:

```text
www.maptap.gg September 27

🏆 Podio
1º Feli 983
2º Sandro 980
3º Bruno 976

⬆️ Ascensos: Feli a 1ª por puntaje · Sandro a 1ª por puntaje · Bruno a 3ª por puntaje · Martín a 5ª por puntaje
⬇️ Descensos: ninguno
```

## 2026-09-28

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Feli Garabato | 938 |
| Lucas Greco | 914 |
| Fede Moia | 905 |
| Sandro Anello | 893 |
| Axel Itzcovitz | 891 |
| Nacho Toker | 878 |
| Ale Feinsilber | 876 |
| Antonio Santos | 854 |
| Bruno Feinsilber | 853 |
| Dario Feinsilber | 827 |
| Martin Feinsilber | Ausente |

Mensaje corto:

```text
www.maptap.gg September 28

🏆 Podio
1º Feli 938
2º Lucas 914
3º Fede 905

⬆️ Ascensos: ninguno
⬇️ Descensos: Martín a 6ª por ausencia
```

## 2026-09-29

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Axel Itzcovitz | 939 |
| Fede Moia | 935 |
| Nacho Toker | 929 |
| Sandro Anello | 917 |
| Lucas Greco | 909 |
| Ale Feinsilber | 899 |
| Dario Feinsilber | 873 |
| Martin Feinsilber | 842 |
| Bruno Feinsilber | 837 |
| Antonio Santos | 833 |
| Feli Garabato | Ausente |

Mensaje corto:

```text
www.maptap.gg September 29

🏆 Podio
1º Axel 939
2º Fede 935
3º Toker 929

⬆️ Ascensos: ninguno
⬇️ Descensos: Feli a 2ª por ausencia
```

## 2026-09-30

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Nacho Toker | 932 |
| Axel Itzcovitz | 930 |
| Lucas Greco | 924 |
| Fede Moia | 920 |
| Sandro Anello | 919 |
| Feli Garabato | 914 |
| Ale Feinsilber | 909 |
| Antonio Santos | 898 |
| Martin Feinsilber | 859 |
| Bruno Feinsilber | 855 |
| Dario Feinsilber | 746 |

Mensaje corto:

```text
www.maptap.gg September 30

🏆 Podio
1º Toker 932
2º Axel 930
3º Lucas 924

⬆️ Ascensos: ninguno
⬇️ Descensos: Dario a 6ª por puntaje
```

## 2026-10-01

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Dario Feinsilber | 963 |
| Feli Garabato | 961 |
| Nacho Toker | 943 |
| Axel Itzcovitz | 925 |
| Sandro Anello | 919 |
| Antonio Santos | 918 |
| Ale Feinsilber | 902 |
| Fede Moia | 899 |
| Martin Feinsilber | 895 |
| Lucas Greco | 853 |
| Bruno Feinsilber | 811 |

Mensaje corto:

```text
www.maptap.gg October 1

🏆 Podio
1º Dario 963
2º Feli 961
3º Toker 943

⬆️ Ascensos: Dario a 5ª por puntaje · Feli a 1ª por puntaje
⬇️ Descensos: ninguno
```

## 2026-10-02

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Lucas Greco | 963 |
| Nacho Toker | 963 |
| Axel Itzcovitz | 958 |
| Antonio Santos | 950 |
| Dario Feinsilber | 936 |
| Feli Garabato | 934 |
| Ale Feinsilber | 932 |
| Sandro Anello | 930 |
| Bruno Feinsilber | 924 |
| Martin Feinsilber | Ausente |
| Fede Moia | Ausente |

Nota de desempate: Lucas y Toker empataron en 963. Lucas suma 484 en sus rondas (99+98+95+98+94) contra 482 de Toker (100+93+97+95+97).

Mensaje corto:

```text
www.maptap.gg October 2

🏆 Podio
1º Lucas 963 (484)
2º Toker 963 (482)
3º Axel 958

⬆️ Ascensos: ninguno
⬇️ Descensos: Martín a 4ª por ausencia · Fede a 2ª por ausencia
```

## 2026-10-03

Estado: cerrado.

Alta nueva: Tomas Perez Duich entra al torneo en la categoria mas baja ocupada (5.a). Sus resultados cuentan desde este dia.

Resultados:

| Jugador | Puntos |
|---|---:|
| Axel Itzcovitz | 961 |
| Sandro Anello | 943 |
| Nacho Toker | 933 |
| Feli Garabato | 928 |
| Fede Moia | 915 |
| Antonio Santos | 914 |
| Bruno Feinsilber | 914 |
| Lucas Greco | 910 |
| Tomas Perez Duich | 901 |
| Martin Feinsilber | 891 |
| Dario Feinsilber | 890 |
| Ale Feinsilber | 887 |

Nota de desempate: Antonio y Bruno empataron en 914. Antonio suma 451 en sus rondas (91+87+83+100+90) contra 448 de Bruno (100+69+92+98+89).

Mensaje corto:

```text
www.maptap.gg October 3

🏆 Podio
1º Axel 961
2º Sandro 943
3º Toker 933

⬆️ Ascensos: ninguno
⬇️ Descensos: ninguno
```

## 2026-10-04

Estado: cerrado.

Alta nueva: Lucas Stella entra al torneo en la categoria mas baja ocupada (5.a). Sus resultados cuentan desde este dia.

Resultados:

| Jugador | Puntos |
|---|---:|
| Axel Itzcovitz | 977 |
| Nacho Toker | 910 |
| Martin Feinsilber | 906 |
| Antonio Santos | 906 |
| Sandro Anello | 884 |
| Ale Feinsilber | 875 |
| Lucas Greco | 864 |
| Bruno Feinsilber | 860 |
| Dario Feinsilber | 851 |
| Feli Garabato | 840 |
| Fede Moia | 813 |
| Tomas Perez Duich | 758 |
| Lucas Stella | 388 |

Nota de desempate: Martin y Antonio empataron en 906. Martin suma 458 en sus rondas (97+90+94+92+85) contra 450 de Antonio (93+85+88+99+85).

Mensaje corto:

```text
www.maptap.gg October 4

🏆 Podio
1º Axel 977
2º Toker 910
3º Martín 906 (458)

⬆️ Ascensos: ninguno
⬇️ Descensos: Tomás a 6ª por puntaje · Lucas Stella a 6ª por puntaje
```

## 2026-10-05

Estado: cerrado.

Baja definitiva: Tomas Perez Duich y Lucas Stella salen del torneo a partir de esta fecha. No figuran en pendientes ni cuentan como ausentes. Su historial previo (3/10 y 4/10) queda registrado tal cual.

Resultados:

| Jugador | Puntos |
|---|---:|
| Fede Moia | 938 |
| Bruno Feinsilber | 925 |
| Axel Itzcovitz | 925 |
| Lucas Greco | 921 |
| Nacho Toker | 911 |
| Sandro Anello | 911 |
| Antonio Santos | 884 |
| Ale Feinsilber | 876 |
| Martin Feinsilber | 857 |
| Dario Feinsilber | 845 |
| Feli Garabato | 845 |

Nota de desempate: Bruno y Axel empataron en 925. Bruno suma 473 en sus rondas (100+99+96+98+80) contra 472 de Axel (98+99+97+98+80). Toker y Sandro empataron en 911 con 468 cada uno (empate total, no define podio).

Mensaje corto:

```text
www.maptap.gg October 5

🏆 Podio
1º Fede 938
2º Bruno 925 (473)
3º Axel 925 (472)

⬆️ Ascensos: ninguno
⬇️ Descensos: ninguno
```

## 2026-10-06

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Nacho Toker | 965 |
| Feli Garabato | 938 |
| Martin Feinsilber | 935 |
| Axel Itzcovitz | 925 |
| Fede Moia | 920 |
| Bruno Feinsilber | 910 |
| Ale Feinsilber | 907 |
| Sandro Anello | 902 |
| Antonio Santos | 891 |
| Dario Feinsilber | 856 |
| Lucas Greco | 855 |

Mensaje corto:

```text
www.maptap.gg October 6

🏆 Podio
1º Toker 965
2º Feli 938
3º Martín 935

⬆️ Ascensos: ninguno
⬇️ Descensos: ninguno
```

## 2026-10-07

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Nacho Toker | 908 |
| Axel Itzcovitz | 902 |
| Fede Moia | 899 |
| Antonio Santos | 888 |
| Martin Feinsilber | 886 |
| Ale Feinsilber | 886 |
| Sandro Anello | 884 |
| Lucas Greco | 882 |
| Bruno Feinsilber | 856 |
| Feli Garabato | 845 |
| Dario Feinsilber | 819 |

Mensaje corto:

```text
www.maptap.gg October 7

🏆 Podio
1º Toker 908
2º Axel 902
3º Fede 899

⬆️ Ascensos: ninguno
⬇️ Descensos: ninguno
```

## 2026-10-08

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Sandro Anello | 944 |
| Axel Itzcovitz | 940 |
| Lucas Greco | 903 |
| Feli Garabato | 903 |
| Bruno Feinsilber | 886 |
| Nacho Toker | 881 |
| Fede Moia | 880 |
| Ale Feinsilber | 857 |
| Martin Feinsilber | 819 |
| Antonio Santos | 810 |
| Dario Feinsilber | 777 |

Nota de desempate: Lucas y Feli empataron en 903. Lucas suma 461 en sus rondas (100+96+88+89+88) contra 458 de Feli (100+90+91+92+85).

Mensaje corto:

```text
www.maptap.gg October 8

🏆 Podio
1º Sandro 944
2º Axel 940
3º Lucas 903 (461)

⬆️ Ascensos: ninguno
⬇️ Descensos: Dario a 6ª por puntaje
```

## 2026-10-09

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Lucas Greco | 941 |
| Axel Itzcovitz | 922 |
| Nacho Toker | 919 |
| Fede Moia | 909 |
| Antonio Santos | 907 |
| Ale Feinsilber | 835 |
| Sandro Anello | 812 |
| Dario Feinsilber | 750 |
| Feli Garabato | Ausente |
| Martin Feinsilber | Ausente |
| Bruno Feinsilber | Ausente |

Mensaje corto:

```text
www.maptap.gg October 9

🏆 Podio
1º Lucas 941
2º Axel 922
3º Toker 919

⬆️ Ascensos: ninguno
⬇️ Descensos: Dario a 7ª por puntaje · Feli a 2ª por ausencia · Martín a 5ª por ausencia · Bruno a 4ª por ausencia
```

## 2026-10-10

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Feli Garabato | 937 |
| Nacho Toker | 934 |
| Antonio Santos | 907 |
| Bruno Feinsilber | 907 |
| Fede Moia | 902 |
| Sandro Anello | 894 |
| Axel Itzcovitz | 885 |
| Lucas Greco | 884 |
| Ale Feinsilber | 875 |
| Martin Feinsilber | 849 |
| Dario Feinsilber | 832 |

Nota de desempate: Antonio y Bruno empataron en 907. Antonio suma 465 en sus rondas (99+99+92+86+89) contra 463 de Bruno (95+100+92+88+88).

Mensaje corto:

```text
www.maptap.gg October 10

🏆 Podio
1º Feli 937
2º Toker 934
3º Antonio 907 (465)

⬆️ Ascensos: ninguno
⬇️ Descensos: ninguno
```

## 2026-10-11

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Nacho Toker | 910 |
| Axel Itzcovitz | 897 |
| Ale Feinsilber | 862 |
| Lucas Greco | 828 |
| Feli Garabato | 828 |
| Martin Feinsilber | 806 |
| Fede Moia | 797 |
| Dario Feinsilber | 795 |
| Antonio Santos | 791 |
| Sandro Anello | 660 |
| Bruno Feinsilber | Ausente |

Mensaje corto:

```text
www.maptap.gg October 11

🏆 Podio
1º Toker 910
2º Axel 897
3º Ale 862

⬆️ Ascensos: ninguno
⬇️ Descensos: Antonio a 2ª por puntaje · Dario a 8ª por puntaje · Sandro a 2ª por puntaje · Fede a 3ª por puntaje · Bruno a 5ª por ausencia
```

## 2026-10-12

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Sandro Anello | 974 |
| Fede Moia | 968 |
| Axel Itzcovitz | 961 |
| Nacho Toker | 959 |
| Lucas Greco | 941 |
| Martin Feinsilber | 888 |
| Ale Feinsilber | 882 |
| Antonio Santos | 829 |
| Bruno Feinsilber | 819 |
| Feli Garabato | 805 |
| Dario Feinsilber | 791 |

Mensaje corto:

```text
www.maptap.gg October 12

🏆 Podio
1º Sandro 974
2º Fede 968
3º Axel 961

⬆️ Ascensos: Sandro a 1ª por puntaje · Fede a 2ª por puntaje
⬇️ Descensos: Dario a 9ª por puntaje
```

## 2026-10-13

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Axel Itzcovitz | 986 |
| Feli Garabato | 955 |
| Nacho Toker | 900 |
| Lucas Greco | 868 |
| Ale Feinsilber | 848 |
| Dario Feinsilber | 822 |
| Bruno Feinsilber | 819 |
| Martin Feinsilber | 808 |
| Fede Moia | 805 |
| Sandro Anello | 801 |
| Antonio Santos | 743 |

Mensaje corto:

```text
www.maptap.gg October 13

🏆 Podio
1º Axel 986
2º Feli 955
3º Toker 900

⬆️ Ascensos: Feli a 1ª por puntaje
⬇️ Descensos: Antonio a 3ª por puntaje
```

## 2026-10-14

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Axel Itzcovitz | 981 |
| Sandro Anello | 935 |
| Nacho Toker | 933 |
| Bruno Feinsilber | 931 |
| Fede Moia | 930 |
| Ale Feinsilber | 927 |
| Feli Garabato | 925 |
| Lucas Greco | 917 |
| Martin Feinsilber | 905 |
| Antonio Santos | 898 |
| Dario Feinsilber | 890 |

Mensaje corto:

```text
www.maptap.gg October 14

🏆 Podio
1º Axel 981
2º Sandro 935
3º Toker 933

⬆️ Ascensos: ninguno
⬇️ Descensos: ninguno
```

## 2026-10-15

Estado: cerrado (11/11 jugadores).

| Jugador | Puntos |
|---|---:|
| Feli Garabato | 988 |
| Nacho Toker | 960 |
| Martin Feinsilber | 908 |
| Fede Moia | 903 |
| Antonio Santos | 881 |
| Lucas Greco | 872 |
| Sandro Anello | 860 |
| Axel Itzcovitz | 839 |
| Bruno Feinsilber | 792 |
| Ale Feinsilber | 783 |
| Dario Feinsilber | 676 |

Ascensos: ninguno (Feli y Toker ya son 1ª). Descensos por puntaje <800: Bruno 5ª a 6ª, Ale 1ª a 2ª, Dario 9ª a 10ª.

Divisiones al cierre del 15/10: Toker 1, Axel 1, Feli 1, Sandro 1, Antonio 3, Lucas 1, Fede 2, Ale 2, Martin 5, Bruno 6, Dario 10.

Mensaje corto:

```text
www.maptap.gg October 15

🏆 Podio
1º Feli 988
2º Toker 960
3º Martín 908

⬆️ Ascensos: ninguno
⬇️ Descensos: Bruno a 6ª por puntaje · Ale a 2ª por puntaje · Dario a 10ª por puntaje
```

## 2026-10-16

Estado: cerrado (11/11 jugadores).

| Jugador | Puntos |
|---|---:|
| Ale Feinsilber | 944 |
| Dario Feinsilber | 943 |
| Nacho Toker | 933 |
| Axel Itzcovitz | 926 |
| Antonio Santos | 893 |
| Lucas Greco | 892 |
| Feli Garabato | 881 |
| Fede Moia | 875 |
| Bruno Feinsilber | 875 |
| Martin Feinsilber | 862 |
| Sandro Anello | 837 |

Nota de desempate: Fede y Bruno empataron en 875. Fede suma 446 en sus rondas (98+84+99+83+82) contra 443 de Bruno (93+93+82+88+87).

Ascensos por puntaje >940: Ale 2ª a 1ª, Dario 10ª a 9ª. Descensos: ninguno.

Divisiones al cierre del 16/10: Toker 1, Axel 1, Feli 1, Sandro 1, Antonio 3, Lucas 1, Fede 2, Ale 1, Martin 5, Bruno 6, Dario 9.

Mensaje corto:

```text
www.maptap.gg October 16

🏆 Podio
1º Ale 944
2º Dario 943
3º Toker 933

⬆️ Ascensos: Ale a 1ª por puntaje · Dario a 9ª por puntaje
⬇️ Descensos: ninguno
```

## 2026-10-17

Estado: cerrado (11/11 jugadores).

| Jugador | Puntos |
|---|---:|
| Fede Moia | 945 |
| Axel Itzcovitz | 942 |
| Sandro Anello | 932 |
| Nacho Toker | 925 |
| Lucas Greco | 911 |
| Feli Garabato | 910 |
| Dario Feinsilber | 900 |
| Antonio Santos | 893 |
| Bruno Feinsilber | 887 |
| Martin Feinsilber | 871 |
| Ale Feinsilber | 831 |

Ascensos por puntaje >940: Fede 2ª a 1ª (Axel ya es 1ª). Descensos: ninguno.

Divisiones al cierre del 17/10: Toker 1, Axel 1, Feli 1, Sandro 1, Antonio 3, Lucas 1, Fede 1, Ale 1, Martin 5, Bruno 6, Dario 9.

Mensaje corto:

```text
www.maptap.gg October 17

🏆 Podio
1º Fede 945
2º Axel 942
3º Sandro 932

⬆️ Ascensos: Fede a 1ª por puntaje
⬇️ Descensos: ninguno
```

## 2026-10-18

Estado: cerrado.

Resultados:

| Jugador | Puntos |
|---|---:|
| Nacho Toker | 954 |
| Axel Itzcovitz | 928 |
| Antonio Santos | 906 |
| Feli Garabato | 894 |
| Ale Feinsilber | 886 |
| Fede Moia | 871 |
| Lucas Greco | 848 |
| Sandro Anello | 839 |
| Dario Feinsilber | 813 |
| Bruno Feinsilber | 709 |
| Martin Feinsilber | Ausente |

Feli habia avisado que no jugaba pero al final jugo (894): no hay descenso por ausencia. Bruno 709 baja de 6ª a 7ª por puntaje. Martin baja de 5ª a 6ª por ausencia.

Mensaje corto:

```text
www.maptap.gg October 18

🏆 Podio
1º Toker 954
2º Axel 928
3º Antonio 906

⬆️ Ascensos: ninguno
⬇️ Descensos: Bruno a 7ª por puntaje · Martín a 6ª por ausencia
```
