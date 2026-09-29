# Revisión semántica de entradas

Fecha: 2026-09-13. Revisión realizada por el asistente Codex sobre la prosa archivada; no es una adjudicación humana independiente. No se consultaron implementaciones históricas para completar reglas ni se ejecutaron conversiones o torneos.

## Resultado y alcance

Se revisaron los 12 textos seleccionados del piloto y los 18 casos truncados. Los 12 del piloto permiten una implementación determinada bajo las convenciones explícitas de la revisión. Entre los truncados, Gemini Pro Aggressive_9 conserva todas sus reglas; los otros 17 no especifican una política inequívoca para todas las situaciones. «Bloqueado» significa que convertirlo exigiría adoptar interpretaciones o completar reglas, no que ningún programa pueda generarse a partir de él.

La evidencia por caso, texto extraído exacto, hashes y razones están en [semantic_review_v1.json](inputs/semantic_review_v1.json). Se verificó cada hash contra el snapshot y el manifest. La selección original se conserva; el diagnóstico favorable de Aggressive_9 no lo añade a las 12 entradas del piloto.

## Las 12 entradas del piloto

| Modelo | Clase | Reglas operativas |
|---|---|---|
| Sonnet 4.6 | Aggressive_11 | D en todas las rondas |
| Sonnet 4.6 | Cooperative_2 | C inicial; copiar al rival hasta 990; D desde 991 |
| Sonnet 4.6 | Neutral_6 | C inicial; copiar al rival hasta 999; D final |
| Gemini Flash | Aggressive_2 | D inicial; después C si el rival nunca defectó, D permanente en otro caso |
| Gemini Flash | Cooperative_5 | C inicial; copiar la última acción del rival, también en 1000 |
| Gemini Flash | Neutral_1 | C inicial; copiar la última acción del rival, también en 1000 |
| Gemini Pro | Aggressive_10 | D en 991–1000, tras D del rival o tras tres C consecutivas del rival; C en otro caso |
| Gemini Pro | Cooperative_3 | C inicial; copiar al rival hasta 999; D final |
| Gemini Pro | Neutral_9 | C inicial; copiar al rival hasta 999; D final |
| GPT-5.4 mini | Aggressive_9 | D en todas las rondas |
| GPT-5.4 mini | Cooperative_20 | C inicial; copiar al rival y volver a C inmediatamente después de C del rival |
| GPT-5.4 mini | Neutral_14 | C inicial; copiar al rival durante todo el horizonte |

C = cooperar, D = defectar. El rótulo Aggressive/Cooperative/Neutral es una condición de generación, no una garantía del comportamiento ni una razón para modificarlo.

Observaciones concretas:

- Sonnet Aggressive_11 se titula Tit-for-Tat, pero sus reglas ordenan siempre D. La conversión debe seguir las reglas explícitas; la explicación de optimalidad no se adopta como conclusión científica.
- Sonnet Neutral_6 estaba marcado por ser breve. La revisión no encuentra reglas ausentes: la longitud no es un criterio de exclusión.
- GPT Cooperative_20 contiene caracteres de sustitución Unicode en una frase explicativa. Se preservan; las reglas numeradas no dependen de esos caracteres.
- Las descripciones TFT sin excepción final deben cooperar en ronda 1000 si el rival cooperó antes. Añadir una defección final por teoría de juegos sería alterar la estrategia.

## Los 18 casos truncados

| Modelo | Clase Aggressive | Decisión y problema concreto |
|---|---|---|
| Flash | 6 | Bloqueado: falta la acción desde 11 frente a cooperación continua |
| Flash | 24 | Bloqueado: retorno forzado truncado y prioridad/cobertura incompletas |
| Pro | 1 | Bloqueado: condición de restauración incompleta |
| Pro | 3 | Bloqueado: falta sondeo y caso inicial/base |
| Pro | 5 | Bloqueado: falta la acción tras acciones iguales |
| Pro | 7 | Bloqueado: falta continuación desde ronda 4 |
| Pro | 8 | Bloqueado: solo cubre 1–3 y 1000, aunque corta una explicación |
| Pro | 9 | Reglas suficientes: explicación cortada después de un caso base completo |
| Pro | 11 | Bloqueado: falta respuesta fuera de dos DD consecutivos |
| Pro | 13 | Bloqueado: disculpa incompleta y sin acción |
| Pro | 15 | Bloqueado: sondeo periódico e inicio sin acción |
| Pro | 16 | Bloqueado: falta rama para rivales sin C en ambas rondas 2 y 3 |
| Pro | 17 | Bloqueado: inicio/sondeo y caso base incompletos |
| Pro | 18 | Bloqueado: falta regla operativa fuera de represalia y final |
| Pro | 19 | Bloqueado: condición posterior a la represalia incompleta |
| Pro | 21 | Bloqueado: «Cooperate in» sin condición terminada |
| Pro | 22 | Bloqueado: condición B incompleta |
| Pro | 23 | Bloqueado: falta inicio y respuesta tras C del rival |

El diagnóstico de Pro 9 es más preciso que excluir todo texto que termina sin punto: D en 1000; D tras C propio/D rival; D tras cuatro C consecutivas del rival; C en los demás casos. En particular, DD previo conduce a C si no aplica otra regla. No se completa la explicación faltante. Este caso sigue marcado como truncado en la sensibilidad documental de 18 exclusiones propuesta anteriormente.

## Comprobaciones de fidelidad preparadas

Se prepararon [77 casos con acciones esperadas](inputs/semantic_test_vectors_v1.json), derivados de las reglas de los 13 textos elegibles: 70 corresponden al piloto y 7 al caso diagnóstico Pro 9. Incluyen inicio, historial insuficiente para una racha, respuesta a defección, perdón o represalia permanente, longitud de rachas y fronteras 990/991 y 999/1000 según corresponda.

Los historiales están codificados por bloques `[acción, repeticiones]`. Son entradas contrafactuales para comprobar reglas; no son resultados de partidos. Los 17 casos bloqueados tienen ejemplos de historiales sin acción inequívocamente determinada, con acción esperada nula. No se afirma que todos esos historiales sean alcanzables siguiendo una política incompleta.

Convenciones: ronda actual = longitud del historial + 1; una condición que exige k rondas previas requiere al menos k observaciones; se respetan prioridades y excepciones explícitas. Estas convenciones se incorporarán al contrato del piloto. Las pruebas esperadas aún no se han ejecutado contra código convertido y no demuestran equivalencia exhaustiva.

## Siguiente paso ejecutable

Preparar el ejecutor de conversión trazable para las 12 entradas ya revisadas, manteniendo el conversor fijado en el proyecto (`gpt-5.4-mini`) sujeto a verificar disponibilidad y configuración efectiva. Preparar y guardar los prompts exactos, el límite de salida, política de reintentos y presupuesto antes de llamadas. No sustituir el modelo automáticamente.

El ejecutor debe guardar solicitud y respuesta por intento sin sobrescribir, incluidos modelo servido, fechas, motivo de terminación y consumo. Debe detener respuestas truncadas o vacías, conservar errores y separar el código original de cualquier transformación posterior. La revisión semántica no autoriza a completar los 17 casos bloqueados.

Después del piloto: contrastar las 70 expectativas de sus entradas, inspeccionar fidelidad completa y validar el horizonte de 1000 turnos. El diagnóstico Pro 9 permanece separado. Los resultados del piloto determinarán fallos del procedimiento, no la selección de estrategias por puntuación. Aún faltará revisar las entradas restantes antes de reconvertir bibliotecas completas.
