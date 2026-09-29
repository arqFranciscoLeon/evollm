# Conversión uniforme v3: resultados originales

Fecha: 2026-09-14. La tanda autorizada terminó y las respuestas se conservaron sin correcciones.

**562/572 estrategias pasan las comprobaciones dirigidas.** Las demás tienen incidencias descritas abajo; recibir código válido no certifica fidelidad.

## Ejecución y coste

- Solicitudes: 572; respuestas verificadas: 572; reintentos: 0.
- Modelo devuelto en todas: `gpt-5.4-mini-2026-03-17`.
- Coste calculado: **US$0.58549125**, dentro del techo autorizado de US$2. No es una factura.
- Tokens: 574,387 de entrada y 34,378 de salida; caché: 0.
- Corpus: 274 occidentales + 298 chinas; 28 exclusiones previas respecto a 600.
- Las descripciones originales se preservaron; misma plantilla, convenciones, parámetros y snapshot para ambos grupos.

## Validación común

- 8,365,825 comprobaciones de acción, sobre 97 historiales controlados y 7 rivales programados por estrategia.
- Partidas diagnósticas completas: 6,281/6,292, con 11 rivales clásicos y horizonte de 1.000 rondas.
- Controles occidentales comparados: 274/274. Trazas idénticas en todos los historiales controlados: 272; con alguna diferencia: 2.
- El control es la respuesta original occidental v2, incluso donde luego se corrigió localmente. Una diferencia no demuestra por sí sola mejora o empeoramiento.
- Inspección única de las 572 fuentes, agrupadas en 152 hashes distintos; nueve pruebas del validador optimizado aprobadas. No es revisión independiente por dos personas.
- El seguimiento optimizado conserva los límites de pasos; 13 trazas completas coincidieron con el adaptador inicial. Cuatro procesos locales usan particiones disjuntas y semillas fijas.

| Modelo | Total | Pasa pruebas | Discrepancia de fidelidad | Error de ejecución | Otro error de validación |
|---|---:|---:|---:|---:|---:|
| anthropic_sonnet46 | 75 | 74 | 1 | 0 | 0 |
| deepseek_v4pro | 74 | 69 | 4 | 1 | 0 |
| gemini_25_flash | 73 | 73 | 0 | 0 | 0 |
| gemini_31_pro | 59 | 58 | 1 | 0 | 0 |
| glm_51 | 75 | 73 | 2 | 0 | 0 |
| kimi_k25 | 74 | 73 | 1 | 0 | 0 |
| openai_gpt54mini | 67 | 67 | 0 | 0 | 0 |
| qwen3max | 75 | 75 | 0 | 0 | 0 |

## Incidencias preservadas

Las diferencias en historiales impuestos se distinguen de las observadas con el historial producido por el propio candidato. Los segundos aportan un contraejemplo alcanzable frente al rival programado.

| Estrategia | Estado | Evidencia breve |
|---|---|---|
| deepseek_v4pro/default/Neutral_8 | fidelity_discrepancy | Ronda 3: esperado C, recibido D; historial alcanzable |
| gemini_31_pro/default/Aggressive_6 | fidelity_discrepancy | Ronda 995: esperado D, recibido C; historial alcanzable |
| glm_51/default/Aggressive_3 | fidelity_discrepancy | Ronda 5: esperado D, recibido C; historial alcanzable |
| deepseek_v4pro/default/Aggressive_15 | fidelity_discrepancy | Ronda 2: esperado D, recibido C; historial alcanzable |
| deepseek_v4pro/default/Neutral_9 | fidelity_discrepancy | Ronda 3: esperado C, recibido D; historial alcanzable |
| deepseek_v4pro/default/Aggressive_7 | fidelity_discrepancy | Ronda 2: esperado C, recibido D; historial alcanzable |
| kimi_k25/default/Aggressive_17 | fidelity_discrepancy | Ronda 8: esperado D, recibido C; historial alcanzable |
| deepseek_v4pro/default/Neutral_7 | runtime_error | Ronda 2: TypeError("'int' object is not subscriptable") |
| glm_51/default/Aggressive_12 | fidelity_discrepancy | Ronda 2: esperado C, recibido D; historial alcanzable |
| anthropic_sonnet46/default/Neutral_3 | fidelity_discrepancy | Ronda 998: esperado D, recibido C; historial alcanzable |

## Alcance y continuidad

La compatibilidad del procedimiento de conversión y del entorno de prueba se aplicó a ambas cohortes. Las incidencias originales no deben ocultarse ni contarse como conversiones fieles. Antes de admitir el campo completo se requiere cerrar sus diagnósticos y, si corresponde, registrar correcciones derivadas por separado bajo la política declarada.

Estas son pruebas dirigidas; no acreditan equivalencia exhaustiva frente a cualquier historial. No se ejecutó el torneo mixto ni se obtuvieron resultados competitivos. Las cuatro interpretaciones alternativas siguen siendo análisis de sensibilidad obligatorios del torneo.

Evidencia: [validación completa](validation/uniform_v3b.json), [contraejemplos](validation/uniform_fidelity_witnesses_v3.json), [recibos y consumo](validation/uniform_conversion_receipt_v3.json), [inspección de fuentes](validation/uniform_source_review_v3.json), [política de resolución](CHINESE_RESOLUTION_POLICY_v1.md).
