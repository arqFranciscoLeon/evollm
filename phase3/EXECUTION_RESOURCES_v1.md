# Configuración y recursos — 2026-09-21

Estado: preparado localmente, pendiente de consolidación, congelamiento y registro público. No se ejecutó el torneo confirmatorio ni se consultó H7 con datos reales. Complementa v0.3 y el documento de sensibilidades sin modificar sus archivos históricos.

## Decisiones metodológicas

Se fija **una repetición**, 1.000 rondas, ruido cero, T=5/R=3/P=1/S=0, 572 identidades y 16 escenarios. Sustituye las veinte repeticiones provisionales de v0.3. La revisión de las 572 fuentes principales y cuatro alternativas no encontró acceso a aleatoriedad; las operaciones permitidas y el adaptador congelado son deterministas. Se inspeccionaron los nombres de llamadas y atributos, conservados en el informe. Ocho comparaciones de trayectorias completas entre dos semillas (16 partidas nuevas, con instancias nuevas) coincidieron. Estas pruebas dirigidas apoyan la revisión estática, no prueban por sí solas todo posible historial.

Repetir encuentros deterministas sin ruido no añade precisión ni observaciones independientes. Si se cambia una fuente, el adaptador, el ruido o el horizonte, se revisará esta decisión antes de ejecutar bajo otro protocolo. La aleatoriedad del conversor durante la generación histórica del código es distinta de la ejecución de las fuentes ya fijadas.

Semilla base de encuentros: **20260913**. Se conserva `runtime.seed_for(20260913, id_i, id_j, 0)`, con identificadores en orden canónico; es la reducción a entero de la huella SHA-256 ya implementada. Se usan las mismas semillas entre escenarios. H7 principal conserva **10.000 permutaciones**, semilla **20260913**, y el intervalo nulo se distingue de un intervalo de confianza. Las sensibilidades no añaden pruebas de significación.

Configuración legible por máquina: [execution_config_v1.json](inputs/execution_config_v1.json). Todavía no es un permiso automático para ejecutar ni un registro público.

## Calibración independiente de los resultados

Se seleccionó una pareja por cada combinación no ordenada de las 24 celdas modelo/actitud: 300 parejas, más 24 autoparejas. La selección ordena SHA-256 de identificadores dentro de cada celda y no consulta cooperación, pagos o clasificaciones. Los 324 encuentros de 1.000 rondas finalizaron sin errores. Se guardan tiempos e identificadores, sin matrices competitivas; sus resultados no se reutilizarán como datos confirmatorios.

La estimación nueva pondera cada tiempo por el número real de parejas de su estrato. Es una extrapolación con un solo representante por estrato, no una muestra suficiente para estimar un intervalo de confianza del tiempo. Incluye ejecución y conteo del encuentro, pero no escritura SQLite. Como contraste se usa el diagnóstico anterior de 580 partidas, que sí incluye persistencia y reanudación. Los cambios de carga del equipo y las estrategias rivales pueden alterar mucho los tiempos.

| Recurso | Estimación con el ejecutor actual |
|---|---:|
| Partidas por escenario, incluidas 572 autoparejas | 163.878 |
| Partidas de 16 escenarios, una repetición | 2.622.048 |
| Tiempo por escenario según diagnóstico anterior | 6,91 horas |
| Tiempo por escenario según nueva calibración | 13,71 horas |
| Tiempo total secuencial extrapolado | 4,61–9,14 días |
| Reserva operativa de tiempo: triple del mayor estimado | 27,42 días |
| SQLite total extrapolado desde el diagnóstico | 1,28 GB decimales |
| Reserva propuesta de disco | 5 GiB |

La reserva triple es un margen de planificación, no una cota garantizada. Las 10.000 permutaciones se proyectan en unos 65,5 segundos a partir de 20 permutaciones de una matriz **sintética** de tamaño 572; su tiempo puede variar. No se calculó significación con encuentros reales.

Se fija un solo trabajador y bases SQLite separadas por escenario, con reanudación únicamente de configuraciones idénticas y detención ante errores. Al inspeccionar el equipo había aproximadamente 55,8 GiB libres en D:, 7,85 GiB de RAM física total y 0,63 GiB disponibles. La consulta WMI fue denegada; la memoria se leyó mediante la API de estado de memoria de Windows. La RAM disponible fluctúa. Se recomienda comprobar al menos 2 GiB disponibles antes del torneo y de exportar matrices: es una reserva operativa conservadora, no un pico de memoria medido. No se ha perfilado el máximo consumo del exportador; el análisis se hará escenario por escenario, liberando cada matriz antes de cargar otra.

## Optimización recomendada antes del congelamiento

El ejecutor actual vuelve a calcular todos los encuentros de cada escenario. Con cuatro identidades que tienen dos implementaciones, la unión de parejas/configuraciones distintas tendría:

`163.878 + 4 × 568 + 6 × 3 + 4 = 166.172 partidas`.

El primer término es el campo principal; siguen cuatro alternativas contra 568 identidades inalteradas, tres combinaciones adicionales por cada par de identidades alteradas y cuatro autoparejas alternativas. La cifra conserva dos instancias de la misma implementación en cada autopareja; no crea encuentros entre la versión principal y alternativa de una misma identidad.

**Es un cálculo del trabajo potencial, no una optimización implementada ni un tiempo ya medido.** Su equivalencia requiere fijar ambas identidades, las dos huellas de fuente, adaptador, entorno, juego, horizonte, ruido y semilla; conservar las 16 matrices completas; usar instancias nuevas y no compartir estado de jugadores; y excluir toda partida diagnóstica. La reanudación y la trazabilidad deben probarse antes de adoptar el cambio.

El siguiente paso recomendado es implementar y validar esa reutilización exacta en una versión nueva, preservando el ejecutor actual. Después se consolidará el protocolo, se congelarán sus dependencias y se preparará el registro temporal público. No conviene congelar una ejecución que repite innecesariamente casi todos los encuentros de quince escenarios.

## Evidencia

- [Calibración y huellas](validation/resources_calibration_v1.json): 324 partidas de tiempos, 16 de control de semillas, cero llamadas API y cero partidas confirmatorias.
- [Pruebas de calendario y configuración](tests/test_resources_v1.py), con resultado en [resources_tests_v1.xml](validation/resources_tests_v1.xml).
- [Programa de calibración](calibrate_resources_v1.py): rechaza sobrescribir el informe existente. No repetir la calibración al reanudar salvo cambios que la justifiquen.
