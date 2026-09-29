# Paso 13: auditoría de las 300 descripciones chinas Default

Fecha: 2026-09-14. Auditoría local completada con incidencias pendientes de resolución. No se modificaron bibliotecas históricas, resultados publicados ni manifiestos occidentales. No se hicieron llamadas API.

## Resultado

| Modelo | Pasa los casos de fidelidad | Discrepancia de código | Especificación pendiente | Total |
|---|---:|---:|---:|---:|
| DeepSeek V4 Pro | 71 | 3 | 1 | 75 |
| Qwen3 Max | 75 | 0 | 0 | 75 |
| Kimi K2.5 | 70 | 3 | 2 | 75 |
| GLM 5.1 | 69 | 5 | 1 | 75 |
| **Total** | **285** | **11** | **4** | **300** |

Se leyeron íntegramente las 300 descripciones, sin inferir reglas ausentes a partir del código. Hay **296 descripciones elegibles** bajo las convenciones explícitas, una bloqueada por una regla ausente y tres que requieren adjudicación. No se detectaron finales visiblemente truncados ni caracteres U+FFFD en los archivos originales. Los símbolos extraños de algunas salidas de terminal no eran corrupción de los archivos.

Las 15 incidencias se concentran en la actitud agresiva. Se preservan todas las identidades y sus razones; no se descartan selectivamente programas según sus resultados.

## Errores demostrados de fidelidad

Cada caso tiene un historial alcanzable por la implementación hasta su primera divergencia y una acción esperada derivada de la prosa. C significa cooperar; D, defectar.

| Estrategia | Problema | Contraejemplo |
|---|---|---|
| DeepSeek Aggressive_2 | Copia la acción rival aunque las ramas explícitas ordenan invertirla. El texto genérico «copy» contradice esas ramas; se aplica el mismo criterio de prioridad operacional usado con Occidente. | Ronda 2 tras C rival: esperado D, código C. |
| DeepSeek Aggressive_15 | Resta el último pago del total acumulado y usa ese resultado como si fuera el pago anterior. | Ronda 2 tras D propio/C rival: esperado D, código C. |
| DeepSeek Aggressive_19 | Agrega cooperación inicial pese a que «otherwise defect» cubre la falta de dos C previas. | Ronda 1: esperado D, código C. |
| Kimi Aggressive_3 | No mantiene la defección permanente después de traición tras iniciar cooperación. | Rival `CCCDC`: ronda 6, esperado D, código C. |
| Kimi Aggressive_9 | Omite la excepción de defección en ronda 1000. | En el historial alternante registrado, ronda 1000: esperado D, código C. |
| Kimi Aggressive_17 | No conserva el estado cooperativo después del umbral; además el indicador de represalia conduce a cooperar posteriormente. | Tras seis C rivales, ronda 7: esperado C, código D. |
| GLM Aggressive_7 | Congela una acción en vez de seguir copiando las acciones futuras del rival. | Rival `DCD`: ronda 4, esperado D, código C. |
| GLM Aggressive_12 | Usa puntuación acumulada menos último pago, en vez del pago de la ronda anterior. | Ronda 2 tras DD: esperado C, código D. |
| GLM Aggressive_17 | La condición final empieza con 1000 rondas ya completadas, fuera del horizonte. | Ronda 1000 tras DD: esperado D, código C. |
| GLM Aggressive_19 | No conserva las decisiones de D para el resto del juego de su árbol inicial. | Rival `DD`: ronda 3, esperado D, código C. |
| GLM Aggressive_22 | La excepción final también empieza después del horizonte. | En el historial registrado, ronda 1000: esperado D, código C. |

[Once contraejemplos con historiales completos en RLE](validation/chinese_fidelity_witnesses_v1.json). Son errores de correspondencia bajo las convenciones declaradas, no fallos de ejecución ni una estimación de su efecto sobre los resultados publicados.

## Cuatro especificaciones por resolver

| Estrategia | Decisión pendiente |
|---|---|
| DeepSeek Aggressive_5 | Tras una C rival en la primera ronda, las ramas de dos observaciones no cubren la ronda 2 y no hay caso por defecto. No se adopta automáticamente la D del código. |
| Kimi Aggressive_12 | Falta explicitar qué hacer tras una o dos C iniciales antes de completar la racha de tres. Debe diferenciarse la represalia temporal antes de cooperar de la permanente posterior. |
| Kimi Aggressive_25 | «Immediately after you play Cooperate» requiere decidir si refiere al par simultáneo previo o a una respuesta en la ronda siguiente. |
| GLM Aggressive_20 | «This is the tenth consecutive round» requiere fijar si cuenta nueve rondas completadas más la actual o diez ya completadas. |

El código de estas cuatro entradas se preserva, pero no se certifica su fidelidad global mientras falte una especificación de referencia. Esto no equivale a afirmar que sus implementaciones carezcan de errores adicionales.

## Método y límites

- Revisión individual de los 300 textos y de las implementaciones, agrupando cuerpos idénticos por estructura para su inspección; una revisión asistida, sin adjudicador independiente ni cegamiento.
- Huellas de archivos y prosa contrastadas con el manifiesto archivístico. Las cuatro bibliotecas proceden del commit `759b7b0cfe1697f3500749e92c45bb00e85502e7`.
- **4.247.327 comprobaciones de acción** sobre historiales controlados y acciones generadas por cada candidato frente a secuencias rivales predefinidas. Los casos comparten prefijos y no son observaciones independientes; no se afirma equivalencia exhaustiva.
- Las nueve pruebas del nuevo oráculo pasaron. Se conservó el entorno estricto y la actualización de puntuaciones ya empleados para el archivo; no se reemplazaron acciones inválidas ni se repararon funciones.
- Las 3.300 partidas chinas de la validación archivística previa habían terminado sin excepciones. No se repitieron esas partidas: ejecutar sin error no garantiza fidelidad a la prosa, como muestran estos once casos.

[Revisión de prosa y procedencia por entrada](inputs/semantic_review_chinese_v1.json), [validación completa](validation/chinese_audit_v1.json).

## Comparabilidad con la conversión occidental

El código y protocolo históricos declaran GPT-5.4 Mini como conversor fijo (`run_phase2_generation.py`, `src/evollm/create_strategies.py`, `src/evollm/llm_clients.py`, `PHASE2_PREREG.md`). Eso documenta la configuración prevista, no acredita por sí solo la versión efectivamente servida por cada una de las 300 llamadas. En los registros locales examinados no se obtuvo un recibo individual equivalente a los conservados para la nueva tanda occidental.

La tanda occidental incorpora aclaraciones adicionales de ventanas, puntuaciones, permanencia y prioridad; el nombre compartido del modelo no vuelve idénticos esos contratos. Por tanto, aún no puede describirse la comparación mixta como control completo del proceso de conversión.

## Continuación necesaria

La auditoría del paso 13 queda completada; la admisión de los participantes chinos no. Antes de cerrar el paso 14 se necesita:

1. Adjudicar o excluir explícitamente las cuatro especificaciones pendientes con criterios simétricos a los occidentales.
2. Resolver las once discrepancias mediante una política común y trazable. La política de correcciones locales v1 puede servir de base, preservando las salidas originales; esta auditoría no aplica esas correcciones.
3. Decidir si se reconvierte el conjunto chino elegible con el mismo contrato ampliado para fortalecer la comparabilidad, o si se mantiene un estudio archivístico con esa limitación declarada. Una reconversión requiere preparar solicitudes y presupuesto antes de cualquier autorización de envío; no se ha realizado aquí.
4. Registrar las consecuencias para tamaños por modelo/actitud y la sensibilidad a duplicados y exclusiones. No se fija todavía el número definitivo de participantes del torneo.

Los resultados de los artículos publicados describen el código histórico. Esta auditoría no los recalcula ni demuestra cuánto cambiarían al corregir la fidelidad; identifica una limitación que deberá comunicarse y estudiarse por separado.
