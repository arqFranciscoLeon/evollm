# Cierre de conversión común y correcciones

Fecha: 2026-09-14. **La conversión común está completada y el corpus derivado de 572 estrategias pasó las comprobaciones dirigidas.** El torneo mixto todavía no se ha ejecutado.

## Resultado

| Trabajo | Estado | Evidencia y resultado |
|---|---|---|
| Cuatro especificaciones chinas | Completado | Dos exclusiones por reglas ausentes; dos interpretaciones principales con alternativas obligatorias. |
| Once errores del archivo chino | Completado | Correcciones locales previas, conservadas como controles; no se transfirieron automáticamente a nuevas respuestas. |
| Conversión uniforme de ambas cohortes | Completado | 572 respuestas del snapshot `gpt-5.4-mini-2026-03-17`, misma plantilla y parámetros; coste calculado US$0,58549125, sin reintentos. |
| Inspección y validación de respuestas nuevas | Completado | 562 pasan, 9 discrepancias de fidelidad y 1 error de ejecución. 8.365.825 comprobaciones y 6.281/6.292 partidas completas. |
| Corrección de las diez incidencias nuevas | Completado | Diez archivos derivados separados: 146.510 comprobaciones y 110/110 partidas completas, todos aprobados. Sin llamadas API adicionales. |
| Manifiesto del corpus derivado | Completado | 562 respuestas intactas + 10 correcciones = 572, con rutas, huellas, procedencia y validación. |
| Protocolo final e integración con el ejecutor | Pendiente | Incorporar tamaños reales, exclusiones, duplicados y variantes; verificar la carga del manifiesto con el adaptador común antes del torneo. |

Las diez incidencias nuevas son distintas del recuento de once errores archivísticos anterior. Ambos resultados originales se mantienen. Las correcciones manuales no se presentan como respuestas correctas del conversor.

## Diez correcciones nuevas

| Estrategia | Corrección |
|---|---|
| DeepSeek Neutral_8 | Aplicar correctamente repetir/cambiar según el pago anterior, conservando la defección final. |
| Gemini Pro Aggressive_6 | Iniciar la defección final en la ronda 995, no en 996. |
| GLM Aggressive_3 | Tras el sondeo de una ronda C, ejecutar una ronda D obligatoria. |
| DeepSeek Aggressive_15 | Usar el pago de la última ronda, no la puntuación acumulada anterior a ella. |
| DeepSeek Neutral_9 | Corregir las acciones tras DD y DC según el pago de la ronda anterior. |
| DeepSeek Aggressive_7 | Detectar pago propio anterior igual a 1; la diferencia entre puntuaciones acumuladas no representa ese pago. |
| Kimi Aggressive_17 | Mantener D permanentemente tras la defección rival durante cooperación; exigir cinco pares DC consecutivos para iniciar cooperación. |
| DeepSeek Neutral_7 | Obtener directamente el pago anterior y eliminar el acceso por índice a un entero que causaba la excepción. |
| GLM Aggressive_12 | Consultar el pago anterior para decidir, sin restarlo del acumulado. |
| Sonnet Neutral_3 | Iniciar D final en la ronda 998, conservando el disparador permanente del 60 %. |

Todas las discrepancias de fidelidad originales tienen un contraejemplo alcanzable frente a uno de los rivales programados. El único error de ejecución se produjo desde la ronda 2 y afectó a las once partidas clásicas de esa estrategia. Sus respuestas y recibos siguen intactos.

Se usaron los mismos 97 historiales controlados, siete rivales programados, once rivales clásicos, horizonte de 1.000 rondas, semillas y adaptador para validar las correcciones. No se seleccionaron cambios mediante puntuaciones o clasificaciones del torneo.

## Participantes y consecuencias para el diseño

| Modelo | Agresivas | Cooperativas | Neutrales | Total | Exclusiones |
|---|---:|---:|---:|---:|---:|
| Sonnet | 25 | 25 | 25 | 75 | 0 |
| DeepSeek | 24 | 25 | 25 | 74 | 1 |
| Gemini Flash | 23 | 25 | 25 | 73 | 2 |
| Gemini Pro | 9 | 25 | 25 | 59 | 16 |
| GLM | 25 | 25 | 25 | 75 | 0 |
| Kimi | 24 | 25 | 25 | 74 | 1 |
| GPT | 17 | 25 | 25 | 67 | 8 |
| Qwen | 25 | 25 | 25 | 75 | 0 |
| **Total** | **172** | **200** | **200** | **572** | **28** |

Las exclusiones se concentran en estrategias agresivas. El borrador que presupone 600 participantes y 25 estrategias de cada actitud por modelo debe actualizarse antes de congelar el análisis. Las permutaciones deben conservar los tamaños reales dentro de cada actitud, y el contraste equilibrado debe explicitar sus ponderaciones y denominadores.

El campo derivado tiene **152 fuentes distintas por SHA-256** y **130 representaciones AST distintas** al omitir posiciones y comentarios. Estas cifras identifican igualdad literal o estructural bajo esa normalización; no son una clasificación completa de equivalencia conductual. Se preservan las 572 identidades. La sensibilidad a duplicados debe especificarse antes de observar el torneo, junto con la sensibilidad a exclusiones y las cuatro interpretaciones alternativas ya declaradas.

Los 274 controles occidentales se compararon contra las respuestas originales v2. En 272 no cambian las acciones en los historiales controlados. Sonnet Neutral_11 ahora pasa la regla de permanencia; Sonnet Neutral_3 introduce el error de ronda final corregido aquí. El error de Gemini Pro Aggressive_6 se repite en ambas tandas originales. Esto no equivale a reproducibilidad exhaustiva ni mide cambios en los resultados publicados.

## Evidencia y siguiente paso

- [Informe de respuestas originales](UNIFORM_RESULTS_v3.md).
- [Validación común completa](validation/uniform_v3b.json).
- [Registro de correcciones y diferencias](inputs/uniform_corrections_v1.json).
- [Validación de las diez correcciones](validation/uniform_corrections_v1.json).
- [Manifiesto de las 572 estrategias derivadas](validation/uniform_derived_candidates_v1.json).
- [Consumo y recibos](validation/uniform_conversion_receipt_v3.json).

El siguiente paso es actualizar el diseño para este corpus, integrar su manifiesto y adaptador en el ejecutor y cerrar las sensibilidades antes de congelar y registrar el protocolo confirmatorio. No hace falta repetir conversiones. Ninguna de estas comprobaciones constituye todavía un resultado del torneo o una garantía de equivalencia para todo historial posible.
