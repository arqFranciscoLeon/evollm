# Resultado del piloto de conversión

Fecha: 2026-09-13. Piloto real completado y validado; el torneo confirmatorio sigue pendiente.

## Ejecución y trazabilidad

El autor autorizó expresamente enviar las 12 solicitudes de `pilot_requests_v1.json` a `api.openai.com` con el conversor fijado y un límite local de US$4. La primera solicitud de ejecución fue bloqueada por revisión automática antes de iniciar el proceso; tras la confirmación expresa, se ejecutaron exactamente 12 intentos, sin reintentos. No se enviaron los 17 casos incompletos ni el diagnóstico Pro Aggressive_9.

La ventana local registrada fue 2026-09-13, 23:31:26–23:31:41 UTC. Las 12 respuestas devolvieron `gpt-5.4-mini-2026-03-17`, finalización `stop` y uso de tokens. No hubo respuestas vacías, errores HTTP, truncamientos ni sustitución del modelo. Se conservan solicitudes, respuestas y código literal en `phase3/conversion_runs/pilot_v1/`; esa carpeta está ignorada por Git y no se ha publicado.

La evidencia compacta reproducible está en [validation/pilot_v1.json](validation/pilot_v1.json), con hashes de plan, código, prosa, respuestas y casos de prueba, versión del entorno, consumo y resultados por estrategia.

## Validación

| Comprobación | Resultado |
|---|---:|
| Conversiones técnicamente aceptadas | 12/12 |
| Casos esperados derivados de la prosa | 70/70 |
| Partidas contra 11 rivales clásicos, a 1000 turnos | 132/132 |
| Pruebas automatizadas del software, incluidas inyección de fallos y detección de una mutación de regla final | 26/26 |

Se inspeccionaron las 12 funciones completas antes de ejecutarlas. Son funciones sin estado propio persistente, que usan el historial y reglas condicionales simples. El verificador admite únicamente ese subconjunto revisado; rechaza importaciones, bucles, acceso a atributos no previstos y modificaciones del estado de los jugadores. No se aplicaron correcciones al código recibido.

Las expectativas verificaron inicio, represalias y perdón, rachas y finales de juego. Las 7 expectativas del diagnóstico Pro Aggressive_9 siguen sin ejecutar porque ese caso no formó parte del piloto. La validación de ejecución usó un adaptador local de Axelrod que proporciona `first_round` y comprueba acciones válidas, con funciones originales intactas; no reutiliza el manejador histórico que sustituía acciones ante fallos.

Cada función jugó contra Cooperator, Defector, Random, TitForTat, Grudger, CyclerDDC, CyclerCCD, GoByMajority, SuspiciousTitForTat, Prober y WinStayLoseShift. Una semilla determinista por estrategia/rival, juego clásico, ruido cero y 1000 turnos. Se registró completitud y ausencia de errores, sin usar puntuaciones para aceptar o descartar estrategias. Estas partidas son diagnósticos contra rivales clásicos, no el torneo mixto confirmatorio.

## Consumo

Uso reportado: 8900 tokens de entrada, 723 de salida, cero tokens de entrada en caché. A las tarifas estándar documentadas de [GPT-5.4 mini](https://developers.openai.com/api/docs/models/gpt-5.4-mini), el coste calculado es:

`8900 × 0,75 / 1.000.000 + 723 × 4,50 / 1.000.000 = US$0,0099285`.

Es aproximadamente un centavo de dólar; no es una factura ni una lectura del saldo de la cuenta. La reserva conservadora de US$3,821184 y el techo local de US$4 permanecen registrados, aunque el uso observado fue mucho menor. No se infiere de estas 12 funciones breves el coste exacto del corpus completo.

## Alcance de la conclusión

El procedimiento de conversión y registro funcionó en las 12 entradas de prosa suficientemente determinada seleccionadas antes de la ejecución. Los códigos respetan las comprobaciones concretas y la inspección de reglas realizada por el asistente. No se afirma equivalencia exhaustiva, ausencia de fallos ante cualquier historial/rival ni adjudicación humana independiente.

El piloto no resuelve las reglas faltantes de 17 descripciones; tampoco prueba equivalencia entre conversores históricos ni la validez del corpus completo. Los cambios de prompt y configuración respecto al cliente anterior continúan declarados en [PILOT_CONVERSION.md](PILOT_CONVERSION.md).

## Siguiente trabajo

Extender la revisión semántica a las entradas Default restantes, empezando por las 270 occidentales que aún no se han revisado. Las 300 occidentales suman 30 revisadas (12 del piloto y 18 diagnósticas) y 270 pendientes. Después, convertir las entradas elegibles con manifiesto y presupuesto específicos; el diagnóstico Pro Aggressive_9 requiere una decisión explícita de inclusión, no una incorporación silenciosa al piloto cerrado.

Revisar también la comparabilidad de las bibliotecas chinas, completar la política de exclusión y el ejecutor mixto, fijar precisión/duplicación y congelar el protocolo antes de resultados confirmatorios. Esta ejecución no autoriza a saltar esas etapas ni a presentar el torneo como ya realizado.
