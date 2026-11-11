# Figuras generadas

## 1. Figuras por benchmark (capítulos 3 y 4)

Generadas por `analisis/generar_figuras.sh` (invoca a `rave-ext/utils/generate_figures.py`)
a partir de los JSON de RAVE en `resultados/`. Al terminar, el mismo script ejecuta
también el ranking de instrucciones (sección 2).

Ubicación: `analisis/FIGURAS/<conjunto>/<BENCHMARK>/<region>/*.png`
(actualmente `tiny`, `small` y `medium`; región `GLOBAL_REGION`).
Cada figura se omite si el JSON no contiene los datos que necesita.

| Fichero | Contenido |
| --- | --- |
| `fig3_1_distribucion_distancias.png` | 3 paneles (RAW, WAR, WAW): % de dependencias por bin de distancia (1, 2, 3, 4, 5-8, 9-16, 17-32, >32) y total de cada tipo. |
| `fig3_2_cdf_cobertura.png` | CDF de la distancia para RAW, WAR y WAW en los puntos 1, 2, 4, 8, 16, 32, 64 (eje X log2). |
| `fig3_3_matriz_productor_consumidor.png` | Matriz 8×8 de clases productor→consumidor para dependencias RAW. Versión A: % del total de RAW. Versión B: % normalizado por fila. |
| `fig3_4_curva_oportunidad.png` | Media de dependencias activas concurrentes por ventana de instrucciones W = 2, 4, 8, 16, 32, 64, para RAW, WAR y WAW. |
| `fig3_5_paralelismo_disponible.png` | Barras de paralelismo medio disponible (instrucciones independientes) por ventana W = 2, 4, 8, 16 frente al máximo teórico W. Requiere `parallelism_available` en el JSON. |
| `fig3_6_dimensionamiento_buffers.png` | Barras agrupadas por tipo de dependencia (RAW, WAR, WAW) con la capacidad de buffer requerida para P50, P90 y P99. |
| `fig3_7_matriz_overlap_instruccion_anterior.png` | Matriz 10×10 de transiciones entre la instrucción anterior y la actual (I(t-1) → I(t)). Versión A: % del total de pares. Versión B: % normalizado por fila. |
| `fig4_1_interfaz_escalar_vectorial.png` | Panel A: eventos de la interfaz escalar-vectorial por cada 1.000 instrucciones vectoriales (broadcast .vx/.vf, escalar→vector, vector→escalar, resultado escalar, vset*). Panel B: % de elementos que consumen difusión escalar. |
| `fig4_2_movimiento_comunicacion_vrf.png` | Panel A: frecuencia ISA de cada categoría de movimiento (slides, gathers, compress, reductions, whole-register, mask/scans, layout conversions) por 1.000 instrucciones vectoriales. Panel B: bytes VRF leídos+escritos por operación aritmética útil. |
| `fig4_3_politicas_tu_ta_mu_ma.png` | Panel A: % de selección de políticas tu/ta y mu/ma. Panel B: % de elementos destino que son tail a conservar (tu), desactivados por máscara (mu) y activos escritos. |

## 2. Ranking de instrucciones

Generado por `analisis/ranking_instrucciones.py`, cuya ejecución está concatenada
al final de `analisis/generar_figuras.sh`, a partir de los JSON de `resultados/`
(192 configuraciones; 7 secciones, 44 familias y 133 instrucciones RVV).

Salidas en `analisis/salida_ranking/`:

CSV:
- `ranking_prevalencia_instrucciones.csv` y `ranking_prevalencia_familias.csv`: prevalencia (nº de aplicaciones presentes), frecuencias media/mediana/cuartiles/P90, participación global y por sección.
- `ranking_frecuencia_instrucciones.csv` y `ranking_frecuencia_familias.csv`: lo mismo ordenado por frecuencia.
- `evolucion_instrucciones.csv` y `evolucion_familias.csv`: prevalencia y frecuencia por tamaño (tiny→large) para RiVEC.
- `instrucciones_por_aplicacion.csv`: conteos y frecuencias por aplicación.
- `resumen.json`: resumen de la ejecución.

Figuras en `analisis/salida_ranking/figuras/`:

| Fichero | Contenido |
| --- | --- |
| `prevalencia_instrucciones.png` | Top 20 instrucciones por prevalencia (% de aplicaciones en las que aparecen). |
| `frecuencia_instrucciones.png` | Top 20 instrucciones por frecuencia dinámica. |
| `prevalencia_familias.png` | Top 20 familias funcionales por prevalencia. |
| `frecuencia_familias.png` | Top 20 familias funcionales por frecuencia dinámica. |
| `prevalencia_por_seccion.png` | Top 8 instrucciones por prevalencia dentro de cada sección. |
| `frecuencia_por_seccion.png` | Top 8 instrucciones por frecuencia dentro de cada sección. |
| `boxplot_frecuencia_top.png` | Distribución (cuartiles) de la frecuencia de las instrucciones top. |
| `heatmap_presencia_top.png` | Presencia/ausencia de las instrucciones top por aplicación. |
| `evolucion_tamano_frecuencia.png` | Evolución de la frecuencia con el tamaño del problema (RiVEC). |
| `evolucion_tamano_prevalencia.png` | Evolución de la prevalencia con el tamaño del problema (RiVEC). |
