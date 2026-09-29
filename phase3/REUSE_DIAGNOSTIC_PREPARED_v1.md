# Prueba diagnóstica del motor de reutilización: preparada, sin ejecutar en Modal

Fecha: 2026-09-27. Alcance `selected_diagnostic`. El calendario confirmatorio de 665 lotes permanece íntegro, sin ejecutar y sin registro público.

## Trabajo local completado

- Se fijaron seis parejas antes de observar resultados competitivos: cuatro identidades con alternativa frente a una identidad estable, una autopareja alternativa y una autopareja estable.
- El motor las descompone en **11 partidas computacionalmente distintas**, que corresponden a **96 resultados lógicos** en los 16 escenarios. Son diagnósticos de equivalencia, fuera de las matrices confirmatorias.
- Se ejecutaron localmente las 11 partidas de 1.000 rondas; el comprobante completo pasó `validate_receipt(..., require_complete=True)`. Su huella es `cf7da6d948c16a1293e6de24fa8132ebbc6110361d86802148e1ec33dbd94da7`.
- Contexto: `326859cad8fe951e57456b5e7105ec6f10f80e1a5c214f1418939fdfd247835d`; lote: `c93c68716d0ac7518ae9b508843893d38af4eae5a683e7fde84768f6ada575eb`.
- El paquete nuevo tiene **599 archivos y 21.378.714 bytes**. Los 595 del piloto previo son idénticos byte a byte. Se añadieron únicamente `reuse_batches_v1.py`, `reuse_worker_v1.py`, `reuse_diagnostic_v1/context.json` y `reuse_diagnostic_v1/batch.json`. La auditoría confirmó las 599 huellas. El paquete no incluye credenciales, respuestas de API ni el comprobante local de resultados.
- El script Modal está preparado para tres llamadas secuenciales sobre un volumen exclusivo: ejecutar 2, reanudar hasta completar 11 y comprobar que una tercera llamada ejecuta 0. Verifica integridad del paquete, contexto, lote y resultados; exige equivalencia exacta con el comprobante Windows antes de guardar el informe final. Límite de 16 partidas, un contenedor CPU, 600 segundos por llamada, sin reintentos automáticos.

Archivos: `reuse_diagnostic_v1/`, `cloud_bundle_reuse_diagnostic_v1/`, `prepare_modal_reuse_diagnostic_v1.py` y `modal_reuse_diagnostic_v1.py`. El código del motor y su plan v1 no se modificaron.

## Facturación y estado remoto

La consulta de facturación de Modal del 2026-09-27 reportó `metered_cost = 0`, `billed_cost = 0` para el mes; el desglose del piloto anterior reportó CPU US$0,00204282 y memoria US$0,00009500. La consulta no informa un saldo exacto de créditos posterior. La última evidencia del panel mostraba US$30 en créditos y límite de uso US$30 antes de aquel piloto. No se autorizan recargas ni cargos por encima de esos créditos.

**No se subió el paquete nuevo ni se ejecutaron las tres llamadas.** La revisión automática rechazó `modal run` porque la autorización explícita anterior cubría un paquete de 595 archivos y el nuevo contiene 599, además de consumir cómputo. Se requiere una autorización explícita para enviar esos 599 archivos al workspace `unimayor-evollm` y ejecutar las 11 partidas diagnósticas dentro de los US$30 disponibles. No se intentará eludir el rechazo mediante otra ruta.

Tras esa autorización: ejecutar el script una sola vez, comprobar 2→11→11 resultados y 0 repetidos, registrar el uso facturado actualizado y detener la app. Si alguna comprobación falla, no iniciar el torneo. Después consolidar/congelar/registrar públicamente el protocolo antes de ejecutar las 166.172 partidas confirmatorias.
