# Revisión completa de las 270 descripciones pendientes

Fecha: 2026-09-13. Revisión local terminada, sin llamadas API. Lectura de los textos completos por el asistente Codex; no adjudicación humana independiente. No se usó el código histórico ni resultados de partidas para completar reglas.

## Resultado de esta revisión

| Modelo | Revisadas ahora | Elegibles bajo convenciones declaradas | Reglas incompletas o indeterminadas | Interpretación pendiente |
|---|---:|---:|---:|---:|
| Sonnet 4.6 | 72 | 72 | 0 | 0 |
| Gemini 2.5 Flash | 70 | 70 | 0 | 0 |
| Gemini 3.1 Pro | 56 | 53 | 1 | 2 |
| GPT-5.4 mini | 72 | 64 | 8 | 0 |
| **Total** | **270** | **259** | **9** | **2** |

Cada caso tiene texto extraído, huella de prosa y biblioteca, commit, decisión, reglas operativas y comprobaciones necesarias; los no elegibles incluyen un historial donde la acción queda indeterminada. Véase [semantic_review_remaining_v1.json](inputs/semantic_review_remaining_v1.json). No se dedujo elegibilidad por similitud de nombres ni por ausencia de banderas automáticas.

## Problemas nuevos identificados

Las once entradas siguientes carecían de banderas en la heurística previa. Un texto que termina con puntuación puede tener reglas ausentes, y una frase gramaticalmente completa puede no determinar una acción.

| Entrada | Problema | Tratamiento |
|---|---|---|
| Gemini Pro Aggressive_20 | Termina en `4. **`: falta regla 4/caso base. Tras una D antigua y una C reciente del rival, no aplica ninguna regla completa | Bloqueada por regla ausente |
| GPT Aggressive_5 | No define la longitud de una racha mutua de D ni cuándo se necesita probar C | Bloqueada por indeterminación |
| GPT Aggressive_6 | No especifica cuándo C es necesaria para provocar un cambio del rival | Bloqueada por indeterminación |
| GPT Aggressive_12 | No cuantifica varias C consecutivas ni las rondas finales | Bloqueada por indeterminación |
| GPT Aggressive_16 | Sondeo opcional tras D y D permanente tras cualquier D tienen precedencia/disparadores sin resolver | Bloqueada por indeterminación |
| GPT Aggressive_17 | No define varias rondas recientes, deseo de probar ni inicio del final | Bloqueada por indeterminación |
| GPT Aggressive_20 | No define cuándo probar C tras una racha larga de DD | Bloqueada por indeterminación |
| GPT Aggressive_22 | Exige certeza de cooperación futura sin criterio observable | Bloqueada por indeterminación |
| GPT Aggressive_23 | No define cuándo C resulta claramente necesaria ni cuántas rondas son varias | Bloqueada por indeterminación |
| Gemini Pro Aggressive_12 | D si hubo D en cualquiera de las dos rondas previas; no aclara el historial de solo una ronda | Pendiente de adjudicar ventana |
| Gemini Pro Aggressive_14 | Misma ambigüedad de historial corto | Pendiente de adjudicar ventana |

Para las dos ventanas ambiguas, considérese ronda 2 después de C propio/D rival. Usar las observaciones disponibles da D; exigir dos rondas completas, como la convención general del piloto, da C. La propuesta es distinguir una disyunción sobre observaciones disponibles de una racha que sí necesita k observaciones, documentándolo en una enmienda. Hasta fijar esa decisión, no se incluyen estos dos casos en la cola de conversión elegible.

No se convierten las ocho excepciones vagas de GPT en siempre D por conveniencia. Eso eliminaría decisiones contempladas por el texto. Tampoco se elimina del registro un caso porque sea difícil de convertir: se conserva su identidad y el motivo de no inclusión.

## Detalles que debe respetar la conversión ampliada

- **Permanencia:** Sonnet Neutral_3 y Neutral_11 activan D para el resto del juego al cruzar un umbral. Un porcentaje que después baje no debe desactivar esa decisión. Flash Aggressive_16 hace lo mismo tras una racha de tres D rivales.
- **Puntuaciones:** Sonnet Aggressive_2 usa una ventaja estrictamente mayor que 10; Aggressive_24 usa al menos 20. Se comparan puntuaciones acumuladas de rondas ya jugadas. Con los pagos clásicos, la diferencia es `5 × (DC − CD)`.
- **Umbrales:** «more than» es estricto, «at least» incluye igualdad y mayoría exige más del 50%. No se introduce un estado permanente cuando el texto solo pide recalcular un porcentaje.
- **Inicio y finales:** Flash Aggressive_14 empieza C y luego siempre D. GPT Neutral_17 empieza D y copia; Neutral_24 siempre D. Gemini Pro Neutral_20 copia al rival también en 1000, a diferencia de casi todas las otras descripciones neutrales de ese modelo.
- **Prioridades:** Gemini Pro Aggressive_25 rompe dos DD mutuos con C antes de aplicar represalia, pero D final tiene prioridad. Aggressive_24 explicita por separado los retardos de una y dos rondas: no tiene la ambigüedad de los casos 12 y 14.
- **Texto frente a explicación:** Sonnet Aggressive_17 dice ronda 990 o posterior en la regla y diez rondas finales en la explicación. Se conserva la regla numérica explícita (11 rondas) y se declara la discrepancia. Gemini Pro Aggressive_24 acaba con un marcador `**`, pero antes contiene un caso base completo: no se confunde ese residuo con una política incompleta.
- **Rondas restantes:** para Sonnet Aggressive_20 y Aggressive_21 se declara que se cuentan las rondas aún no jugadas, incluida la actual: cinco corresponden a 996–1000; ocho a 993–1000. La aclaración debe formar parte del contrato ampliado.

La revisión agrupa 239 de las 259 nuevas entradas elegibles en descripciones de siempre D o copia de la última acción, con variantes de inicio/final. Esto orienta las comprobaciones, pero no demuestra que sus implementaciones sean idénticas. Se conservan todos los identificadores: no se han deduplicado agentes ni cambiado sus pesos.

## Estado acumulado de las 300 occidentales Default

| Modelo | Elegibles | Bloqueadas por reglas | Pendientes de interpretación |
|---|---:|---:|---:|
| Sonnet 4.6 | 75 | 0 | 0 |
| Gemini Flash | 73 | 2 | 0 |
| Gemini Pro | 57 | 16 | 2 |
| GPT-5.4 mini | 67 | 8 | 0 |
| **Total** | **272** | **26** | **2** |

El [inventario acumulado](inputs/western_default_eligibility_v1.json) conserva las 300 identidades. De las 272 elegibles, 12 ya pertenecen al piloto convertido y validado. Quedan **260 elegibles sin convertir**: las 259 nuevas y Gemini Pro Aggressive_9, revisada antes y separada como diagnóstico. Esta cola es una propuesta documental, no una orden de envío a la API ni autorización de gasto adicional.

Las 28 reservas se concentran en la actitud agresiva. Un campo occidental restringido tendría 25 agresivos Sonnet, 23 Flash, 7 Pro y 17 GPT, con 25 cooperativos y 25 neutrales por modelo. Si se conservaran las 300 entradas chinas, el campo combinado tendría 572 agentes, no 600. Ese número es un escenario de diseño: las bibliotecas chinas no fueron revisadas semánticamente en esta tarea.

Por ello, la sensibilidad anterior que eliminaba solo 18 textos resulta insuficiente para describir todas las limitaciones identificadas. Debe revisarse la política de inclusión antes de congelar el torneo; no se han modificado el protocolo histórico ni sus resultados. El análisis balanceado existente tampoco admite automáticamente estos tamaños desiguales.

## Corrección de una observación editorial previa

La inspección de puntos de código muestra que ciertas apariciones de `�` en la consola eran problemas de visualización, no texto fuente dañado: los intervalos de Sonnet contienen U+2013 y la frase de GPT Cooperative_20 contiene comillas U+201C/U+201D. No hay U+FFFD en los textos examinados. Se corrigen las notas editoriales de cuatro casos mediante [semantic_encoding_corrections_v1.json](inputs/semantic_encoding_corrections_v1.json), manteniendo intactos textos, hashes, decisiones y solicitudes del piloto ya ejecutado. La nota anterior sobre corrupción de esos caracteres no debe reutilizarse en un manuscrito.

## Verificación y próximo paso

Se comprobó que los 270 identificadores nuevos y los 30 anteriores son disjuntos y cubren exactamente las 300 entradas; se cotejaron las 270 huellas de prosa contra las bibliotecas y se verificó la integridad de la revisión previa. Los totales y el inventario de elegibilidad concuerdan. Las comprobaciones verifican trazabilidad y cobertura, no sustituyen la revisión científica ni validan código aún no generado.

Sigue incorporar las decisiones de interpretación y exclusión en un contrato ampliado y preparar su presupuesto. La conversión ampliada debe soportar puntuaciones y disparadores permanentes: el verificador del piloto se limitaba a funciones simples sin estado propio y no puede ampliarse silenciosamente. Antes del torneo también falta revisar la comparabilidad de las entradas chinas y resolver precisión, duplicación, análisis con grupos desiguales y registro del protocolo.

**Consumo de API de esta revisión: cero.** No se ejecutaron nuevas conversiones ni partidas.
