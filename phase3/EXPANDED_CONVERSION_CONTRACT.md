# Contrato de preparación de la conversión ampliada

Fecha: 2026-09-13. Estado: decisiones metodológicas locales y solicitudes preparadas; no ejecución, envío a API ni registro público.

Actualización posterior: el ejecutor y el validador ampliados ya están implementados y comprobados sin red. Véase [estado de ejecución](EXPANDED_EXECUTION_READY.md). Las menciones siguientes a implementación pendiente describen el momento de preparación del contrato. No se ha ejecutado el paquete ampliado.

## Interpretación e inclusión

Se resuelven Gemini Pro Aggressive_12 y Aggressive_14 interpretando «either of the previous two rounds» como una disyunción sobre las observaciones disponibles. Después de una única D rival, ronda 2 produce D. Una racha o ventana de longitud fija sigue requiriendo la longitud completa. Las reglas iniciales y finales tienen su prioridad explícita. Esta decisión no reconstruye la intención histórica: declara una interpretación operacional antes de la conversión.

Se fija además una comprobación de sensibilidad con la lectura alternativa de ventana completa para ambos casos, **independientemente del resultado, dirección o significancia**. La alternativa no reemplazará el código principal según su puntuación. Debe implementarse y registrarse por separado antes de resultados del torneo.

La decisión vigente está en [window_adjudication_v2.json](inputs/window_adjudication_v2.json). Sustituye el borrador local v1, que condicionaba la sensibilidad a la importancia observada del efecto; esa condición se retiró antes de cualquier nueva conversión. Los dos borradores permanecen como historial, no como protocolos públicos.

Con esto, hay 274 descripciones occidentales Default elegibles bajo las convenciones explícitas: Sonnet 75, Flash 73, Pro 59 y GPT 67. Se excluyen de la conversión fiel 26 entradas con reglas ausentes o indeterminadas, todas agresivas. No se completan sus textos, no se regeneran selectivamente ni se reemplazan por otras estrategias. Sus identidades y razones permanecen en el inventario.

## Un único contrato para las 274

Las [274 solicitudes exactas](inputs/expanded_requests_v2.json) usan el mismo prompt de implementación y una adición uniforme que explicita ventanas, rondas restantes, porcentajes, puntuaciones y permanencia de represalias. Se mantienen `gpt-5.4-mini`, temperatura 0, esfuerzo `none`, límite de 4096 tokens de completado y endpoint oficial `https://api.openai.com/v1/chat/completions`.

Se reconvertirían también las 12 entradas del piloto como controles pareados. El corpus ampliado así no mezclaría dos versiones del prompt de conversión. Se conservarán las implementaciones anteriores y las nuevas, con una comparación de acciones y casos semánticos; no se escogerá la que gane más. Esto implica 274 solicitudes nuevas, de las cuales 262 corresponden a entradas aún no convertidas (incluidas las dos ahora adjudicadas).

Los cambios respecto del piloto son explícitos. El código del piloto, sus prompts, sus resultados y las bibliotecas históricas no se han modificado. La versión v2 del paquete sustituye v1 para asegurar que la sensibilidad de ventanas sea obligatoria y no dependa del resultado.

## Presupuesto propuesto

El piloto costó aproximadamente US$0,0099285 según sus tokens reportados. La extrapolación lineal a 274 entradas es **US$0,226701**. Es orientativa: algunas reglas ampliadas requieren más código y los prompts incluyen aclaraciones adicionales.

Se propone un **límite local total de US$2**, inferior a los US$2,93 mostrados por el autor. La captura no equivale a una lectura actualizada del saldo; no se ha consultado ni recargado la cuenta. La ejecución puede detenerse antes de completar las 274 entradas si el gasto resulta mayor de lo esperado.

Los precios de referencia son los [documentados para GPT-5.4 mini](https://developers.openai.com/api/docs/models/gpt-5.4-mini) consultados el 2026-09-13: US$0,75 por millón de entrada, US$0,075 en caché y US$4,50 de salida. No se trata de una factura ni de una garantía ante cambios de precio o impuestos.

El nuevo contador deberá reservar antes de cada llamada US$0,318432, usando la cota conservadora del contexto completo y la salida máxima. Tras una respuesta trazable y con consumo válido, sustituirá la reserva por el coste calculado. Si el resultado o el consumo son inciertos, mantendrá la reserva completa y detendrá la tanda. No enviará otra solicitud cuando gasto confirmado + reservas pendientes + reserva siguiente exceda US$2. Esto permite liberar la reserva sobrante de respuestas pequeñas sin comprometer un consumo incierto.

No habrá reintentos automáticos ni aumento de presupuesto. Un error requiere conciliación documentada; no se podrá eludir el contador creando otro directorio. El control es local, no un límite de facturación de la cuenta.

## Validación necesaria antes de ampliar

El ejecutor del piloto solo acepta su plan de 12 entradas y mantiene reservas completas por intento. **No puede ejecutar este paquete**. Falta implementar el ejecutor ampliado con el contador acumulado, reanudación y pruebas de fallos que respeten este contrato.

El validador también debe ampliarse antes de ejecutar código con contadores, estados persistentes o puntuaciones. Las pruebas deben incluir cruces y descensos de porcentajes, disparadores irreversibles, igualdad en umbrales, historial corto, final y orden de reglas. Tener código que compila no certifica fidelidad. Los casos semánticos se derivarán de la revisión ya registrada, sin usar ganancias para seleccionar implementaciones.

La tanda mantendrá todas las respuestas por intento y no reparará funciones silenciosamente. Si el modelo informa `UNCONVERTIBLE`, devuelve texto incompleto o código que falla, se registrará y detendrá según el protocolo. Una nueva decisión de corrección deberá distinguir error de implementación de regla ausente.

## Consecuencias para el torneo

Con 300 entradas chinas conservadas, el campo potencial sería de 574 agentes: 274 occidentales y 300 chinos. Esto es un escenario condicionado a validar entradas y comparabilidad, no un tamaño definitivo. Los agresivos occidentales serían 25/23/9/17, mientras las otras actitudes tendrían 25 por modelo. El análisis no puede asumir estratos de igual tamaño.

El archivo histórico de 600 programas permanece disponible como estudio descriptivo distinto. La comparación con conversor común no debe presentarse como un efecto aislado del generador sin declarar las diferencias históricas de generación/conversión y las exclusiones. Falta auditar las descripciones chinas, adaptar el análisis de grupos desiguales y congelar el protocolo antes del torneo confirmatorio.

## Estado de autorización y siguiente acción

La autorización explícita anterior cubrió 12 solicitudes y hasta US$4. No se interpreta como permiso para enviar este paquete nuevo de 274. Esta fase solo prepara archivos y decisiones. Una vez implementado y probado el ejecutor ampliado, se solicitará autorización concreta del paquete y del nuevo límite si se procede a ejecutarlo.

Siguiente acción técnica: implementar y probar el ejecutor ampliado y las comprobaciones semánticas para estados/puntuaciones; luego ejecutar el paquete autorizado. **Llamadas API realizadas durante esta preparación: cero.**
