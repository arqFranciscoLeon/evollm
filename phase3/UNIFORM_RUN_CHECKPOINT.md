# Tanda común v3 — ejecución autorizada

## Estado definitivo: completado

La tanda y las validaciones ya terminaron. **No hay procesos que reanudar ni conversiones que repetir.** Informe final: `UNIFORM_CLOSURE_v1.md`. Tanda: 572 respuestas, US$0,58549125. Validación original `validation/uniform_v3b.json`: 562 pasan, 9 discrepancias y 1 error de ejecución; 8.365.825 checks, 6.281/6.292 partidas completas.

Las diez incidencias nuevas se corrigieron por separado (`inputs/uniform_corrections_v1.json`), se inspeccionaron y pasaron 146.510 checks y 110 partidas con el mismo protocolo. Evidencia: `validation/uniform_corrections_v1.json`; **manifiesto derivado de 572: `validation/uniform_derived_candidates_v1.json`**, 562 respuestas intactas más 10 correcciones. No modificar fuentes o módulos referenciados por estos informes congelados. Todos los originales permanecen.

Actualización posterior: **protocolo de tamaños reales completado en `DESIGN_v0.3_DRAFT.md`**; cifras y huellas en `inputs/population_protocol_v0_3.json`. **Analizador adaptado y probado:** `analyze_phase3.py` admite celdas desiguales; evidencia en `validation/h7_unequal_v1.json`. **Ejecutor integrado:** `execute_uniform.py`, 29 pruebas de software aprobadas, 580 partidas diagnósticas con las 572 identidades, sin errores; reanudación 37 + 543 + 0. Informe `EXECUTOR_INTEGRATION_v1.md`, evidencia `validation/uniform_executor_tests_v1.json` y base `validation/uniform_integration_v1.sqlite`. No hay procesos pendientes ni partidas diagnósticas que repetir. Siguiente trabajo: cerrar sensibilidades, repeticiones/recursos y congelamiento/registro antes del torneo confirmatorio, que no se ha ejecutado.

## Historial de ejecución — las instrucciones y sesiones siguientes ya finalizaron

El usuario autorizó expresamente las 572 solicitudes de `inputs/uniform_requests_v3.json` a la API oficial, snapshot `gpt-5.4-mini-2026-03-17`, con techo local de US$2. La ejecución comenzó el 14 de septiembre de 2026. No solicitar otra autorización para esta misma tanda ni iniciar una tanda duplicada.

Proceso iniciado: `python -m phase3.uniform_converter --live`. Sesión de ejecución 90721. Los recibos persistentes en `conversion_runs/uniform_v3` son la autoridad para reanudar; el ejecutor verifica el plan y evita duplicados. No modificar el ejecutor ni el plan congelados.

Tanda completada: **572/572 respuestas**, coste calculado **US$0,58549125**, reservas pendientes cero, sin bloqueos ni reintentos. La sesión 90721 terminó correctamente. Las respuestas aún requieren validación semántica y de ejecución. No son estrategias admitidas al torneo.

Inspección manual de fuentes realizada hasta el índice **572 inclusive**, deduplicando por SHA-256 de bytes. Los índices 001–019 se inspeccionaron antes de la recuperación de contexto; 020–572 después. Se creó `uniform_semantics.py` con extensiones explícitas para estados privados, desempaquetado de puntuaciones, enumeración de historial, `getattr` de dos estados literales y conteo sobre `last_100`, todos inspeccionados. No alterar `expanded_semantics.py`, congelado por informes anteriores.

La primera validación `validate_uniform.py` (sesión 79171) se detuvo por lentitud; sus parciales quedan en `validation/uniform_v3_entries`. Se creó una versión nueva que limita el seguimiento de líneas al código candidato: `uniform_semantics_v3b.py` y `validate_uniform_v3b.py`. Trece trazas cronológicas completas coinciden exactamente con el adaptador anterior, incluido el error de ejecución; nueve pruebas de software aprobadas en v3b. No cambian candidatos, referencias, escenarios, semillas ni límites de pasos.

**Validación vigente en cuatro procesos locales:** `python -m phase3.validate_uniform_v3b --shard N --shards 4`, N=0,1,2,3. Sesiones respectivas: **69041, 4154, 83020, 76824**. Guarda `validation/uniform_v3b_entries/NNN.json`. Al terminar las cuatro, ejecutar `python -m phase3.validate_uniform_v3b` sin parámetros: comprobará los 572 checkpoints y consolidará `validation/uniform_v3b.json`. Reanuda sin repetir los registros completos si sus huellas coinciden. No modificar validador, adaptador o referencias durante la ejecución.

Compilación verificada para las 572; manifiesto `validation/uniform_source_review_v3.json` y recibo `validation/uniform_conversion_receipt_v3.json` completos. Mantener las respuestas originales incluso si fallan. Las cuatro interpretaciones alternativas siguen siendo sensibilidad obligatoria del torneo posterior.
