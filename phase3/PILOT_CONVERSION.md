# Ejecutor del piloto de conversión

Estado actualizado: piloto ejecutado y validado; véase [PILOT_RESULTS_v1.md](PILOT_RESULTS_v1.md). Este documento conserva el contrato y las instrucciones de preparación. Las referencias siguientes a ejecución pendiente o API cero describen la etapa anterior al piloto.

## Paquete y decisiones fijadas

[pilot_converter.py](pilot_converter.py) prepara las 12 solicitudes de la selección revisada en [pilot_requests_v1.json](inputs/pilot_requests_v1.json). Cada solicitud contiene mensajes completos y hashes; el plan vincula selección, revisión semántica, 77 casos esperados, generador de prompts y ejecutor por sus huellas. Los 17 casos bloqueados y el caso diagnóstico Pro Aggressive_9 quedan fuera del piloto original de 12.

Se mantiene `gpt-5.4-mini`, endpoint oficial Chat Completions, temperatura 0, `reasoning_effort=none`, `max_completion_tokens=4096`, una respuesta por solicitud, sin streaming ni herramientas, servicio estándar. Se registran el alias solicitado y el modelo devuelto; solo se admiten el alias o el snapshot documentado `gpt-5.4-mini-2026-03-17`. Otro identificador detiene el piloto, sin sustitución automática.

La [documentación oficial del modelo](https://developers.openai.com/api/docs/models/gpt-5.4-mini) consultada el 2026-09-13 indica ese snapshot, contexto de 400.000 tokens y precios estándar de US$0,75 por millón de entrada y US$4,50 por millón de salida. La [referencia de Chat Completions](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create) establece que el límite de completado incluye razonamiento y que `finish_reason=length` indica llegada al límite. Disponibilidad documental no equivale a acceso comprobado desde nuestra cuenta.

## Presupuesto y reintentos

Máximo de 12 intentos, uno por entrada, con cero reintentos automáticos. Límite local de reserva: US$4. Por prudencia, cada intento reserva la ventana completa de entrada de 400.000 tokens, más 4.096 de salida: US$0,318432; los 12 reservan US$3,821184. Las solicitudes preparadas son mucho menores. Esta cifra es una cota conservadora a las tarifas consultadas, no un pronóstico de gasto ni un límite de facturación de la cuenta. No asume descuentos por caché ni incluye impuestos o cambios de tarifa.

La reserva permanece consumida incluso ante error incierto. Una caída de red deja el intento pendiente de conciliación y detiene nuevas llamadas; una segunda ejecución no repite la llamada. Un cambio de configuración o presupuesto exige una nueva versión explícita, no reescribir el plan activo. No se debe iniciar un segundo directorio para eludir ese control: el límite corresponde a esta ejecución local, no al conjunto de todas las carpetas o procesos de la cuenta.

## Comparabilidad histórica

Se reutilizan las dos funciones históricas de creación del prompt de implementación, sin importar el módulo de generación que sobrescribe logs. La solicitud conserva la prosa extraída exacta, los pagos clásicos y el horizonte limpio de 1000 rondas. El prompt histórico pide Python 3.11; el entorno local actual es Python 3.12 y esa diferencia queda explícita.

Se añade una cláusula identificada de interpretación: respetar historial disponible, prioridades y límites de ronda; no mejorar la estrategia ni completar reglas ausentes. Se admite una respuesta `UNCONVERTIBLE:` que detiene la conversión. Esta adición, el esfuerzo de razonamiento explícito y el límite de salida son cambios respecto al cliente histórico; no se presenta el piloto como reproducción idéntica de Fase 2. Usar el mismo alias tampoco acredita los mismos pesos servidos meses atrás.

## Registro y recuperación

Cada intento guarda antes de la llamada: identificador único, hora UTC, estrategia, payload exacto, hash, reserva, versión de Python y transporte. Se usa HTTPS con la biblioteca estándar, sin dependencia del SDK, sin redirecciones y sin reintentos internos.

Después guarda el cuerpo de respuesta, código HTTP, identificador de solicitud del proveedor, hora final y hash. El JSON del proveedor conserva modelo, motivo de terminación, consumo y contenido. No se guardan cabeceras de autorización ni valores de claves. Si una respuesta reproduce la clave, se redacta esa coincidencia y se marca el resultado como no aceptado. Las excepciones de transporte se registran por tipo, sin mensajes potencialmente sensibles.

Se rechazan respuestas vacías, finalización distinta de `stop`, modelo inesperado, uso ausente/fuera de límites y código con forma o sintaxis incorrectas. Un código técnicamente aceptado se conserva literalmente como `candidate.py.txt`; no se corrige, importa ni ejecuta. Su estado sigue siendo pendiente de fidelidad y validación de ejecución.

Los archivos se crean sin sobrescritura. El plan queda anclado a su directorio, un bloqueo impide ejecuciones simultáneas y una reanudación comprueba la integridad de intentos completos. Tras una terminación abrupta puede quedar el bloqueo; requiere revisar el proceso y el intento antes de retirarlo. No se borra automáticamente una reserva incierta.

Los registros reales estarán en `phase3/conversion_runs/pilot_v1/`, ignorados por Git para su revisión antes de publicación. Las pruebas usan directorios temporales y respuestas simuladas; no constituyen resultados del piloto.

## Comandos

Desde `D:/evollm/.claude/worktrees/stupefied-mclaren`, con `D:/evollm/.phase3-venv/Scripts/python.exe`:

```text
python -m phase3.pilot_converter --prepare
python -m pytest phase3/tests -q -p no:cacheprovider --basetemp <directorio-temporal-autorizado>
python -m phase3.pilot_converter --live
```

Solo `--live` llama a la API y necesita `OPENAI_API_KEY` en el entorno del proceso. El ejecutor no busca claves en archivos ni las imprime. Un argumento de línea de comandos no debe contener la clave. En esta preparación solo se han usado modo offline y transporte simulado.

Validación realizada: 21 pruebas pasan, incluidas inyecciones de respuestas truncadas, vacías, no convertibles, cambio de modelo, falta de consumo y sintaxis inválida; reanudación sin duplicados, bloqueo concurrente, límite de presupuesto y rechazo de prompts modificados. Se verificó que el plan guardado coincide con las fuentes actuales. Son pruebas del ejecutor, no de la capacidad de conversión del modelo.

Próximo paso: ejecutar el piloto acotado una vez comprobado el acceso del entorno. El ejecutor procesa secuencialmente y se detiene ante el primer resultado no aceptado; los resultados técnicamente aceptados siguen pendientes de revisión. Después evaluar las 70 expectativas del piloto, revisar la fidelidad integral y validar las estrategias convertidas durante 1000 turnos. Las 7 expectativas diagnósticas siguen aparte. El torneo confirmatorio requiere todavía cerrar y registrar su protocolo.
