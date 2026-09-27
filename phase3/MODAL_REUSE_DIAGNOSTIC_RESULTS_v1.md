# Diagnóstico Modal del motor de reutilización — completado

Fecha: 2026-09-27. Workspace: `unimayor-evollm`. Alcance: `selected_diagnostic`; **no** es ejecución del torneo confirmatorio.

## Resultado

El paquete científico auditado de 599 archivos (21.378.714 bytes) se subió sin credenciales ni respuestas de API. El contexto seleccionado contiene seis parejas de identidades y 11 encuentros computacionalmente distintos que representan 96 resultados lógicos en los 16 escenarios. Cada encuentro duró 1.000 rondas.

| Etapa | Estado previo | Nuevas partidas | Estado final |
|---|---:|---:|---:|
| Primera llamada | 0 | 2 | 2 |
| Reanudación desde el volumen | 2 | 9 | 11 |
| Reapertura del lote completo | 11 | 0 | 11 |

La ejecución Linux devolvió un comprobante completo que se descargó del volumen y se validó contra el lote y el contexto. **Coincide exactamente** con las 11 partidas de referencia ejecutadas en Windows; también coincide el prefijo de dos resultados conservado durante la reanudación. Huella canónica y del archivo descargado: `cf7da6d948c16a1293e6de24fa8132ebbc6110361d86802148e1ec33dbd94da7`.

Evidencia local: `validation/modal_reuse_diagnostic_remote_v1.json` (resumen), `validation/modal_reuse_diagnostic_receipt_v1.json` (comprobante descargado), `reuse_diagnostic_v1/local_baseline.json` (referencia Windows), `reuse_diagnostic_v1/context.json` y `reuse_diagnostic_v1/batch.json`. El resultado reside asimismo en el volumen `evollm-phase3-reuse-diagnostic-v1`, bajo el nombre de la huella del lote `c93c68716d0ac7518ae9b508843893d38af4eae5a683e7fde84768f6ada575eb.json`.

App de la ejecución completada: `ap-rdqAILXMIsVsm4Ry7a3v8K`, [registro Modal](https://modal.com/apps/unimayor-evollm/main/ap-rdqAILXMIsVsm4Ry7a3v8K). Está detenida, con cero tareas. Hubo un intento previo `ap-MwMmEZq0BvKhD1kDRLxOPF` que se detuvo antes de iniciar partidas por una importación local de NumPy en el entorno de la CLI; se corrigió el lanzador local sin cambiar los 599 archivos científicos ni el lote. Esa app también está detenida.

## Facturación observada

El reporte de recursos de la app completada registra CPU **US$0,00056357** y memoria **US$0,00009525**, total **US$0,00065882**. La síntesis mensual posterior muestra `metered_cost` **US$0,01** (redondeado por Modal), ajuste de créditos **−US$0,01** y `billed_cost` **US$0**. La consulta no expone el saldo exacto remanente; no se hizo recarga. La cifra de 11 partidas, con arranque de imagen y tres llamadas, no basta para garantizar el coste ni el plazo del calendario completo de 166.172 encuentros.

## Alcance de la validación y continuación

La prueba acredita integridad del paquete, persistencia en volumen entre invocaciones, reanudación sin repetir resultados guardados y equivalencia exacta Windows/Linux para la selección diagnóstica. No prueba distribución simultánea de los 665 lotes entre múltiples contenedores ni facturación exactamente una vez ante una caída dentro de una partida. El calendario confirmatorio sigue sin resultados y sin registro público.

Próximo paso científico: consolidar el protocolo final con este resultado y el presupuesto observado, fijar el código/plan por huellas y obtener un registro público con fecha anterior a cualquier partida confirmatoria. Después, ejecutar lotes confirmatorios bajo el límite de créditos y comprobaciones de consumo, sin volver a usar resultados diagnósticos para alterar hipótesis o selección.
