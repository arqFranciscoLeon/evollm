# Ejecutor ampliado preparado

Fecha: 2026-09-13. Esta actualización sustituye únicamente el estado de implementación del contrato y del paquete congelado; no cambia sus solicitudes ni sus decisiones metodológicas.

## Implementado

- `expanded_converter.py`: verifica las 274 solicitudes y sus fuentes, reserva presupuesto antes de enviar, concilia consumo trazable, conserva cada intento y reanuda sin duplicados. Una respuesta incierta conserva su reserva y bloquea nuevos envíos. No hay reintentos automáticos. La ejecución real requiere `--live`; el comando por defecto verifica sin red. El directorio de ejecución de la CLI es fijo.
- `expanded_semantics.py`: exige la huella del código inspeccionado, conserva estado entre rondas, actualiza puntuaciones con rondas completadas y compara acciones contra reglas derivadas de la revisión. Incluye límites de ejecución y restricciones sintácticas como ayuda a la inspección; no constituye un aislamiento de seguridad del sistema operativo.
- `validate_expanded.py`: exige 274 respuestas trazables y un registro explícito de inspección de cada fuente. Aplica 19 historiales controlados y 11 rivales clásicos a 1000 rondas. Compara también las acciones de las 12 reconversiones con sus versiones del piloto, sin elegir por ganancias ni reparar código.

## Evidencia local

Resultado final: **42 pruebas aprobadas en 23,53 segundos** con `python -m pytest phase3/tests -q -p no:cacheprovider`. Incluyen concordancia del oráculo con las expectativas semánticas congeladas aplicables y reproducción de los 12 códigos inspeccionados del piloto en los 19 escenarios del nuevo adaptador. `git diff --check` terminó sin errores de formato.

La comprobación sin red verificó el paquete SHA-256 `70336a5958a379a4dc0eb5e341ecfaa4bbc75603f7d967784a2d2411143b1f22`: 274 solicitudes, techo US$2, cero intentos, cero gasto registrado y cero reservas pendientes.

Las pruebas incluyen presupuesto, caché, reanudación, errores de transporte, consumo desconocido o inconsistente, respuestas truncadas, recibos modificados, estados irreversibles, umbrales de puntuación y ventanas iniciales. Se comprueba la cobertura de perfiles de las 274 entradas. Esto valida infraestructura y casos concretos, no certifica todavía los 274 programas que se recibirían.

## Continuación

1. Obtener autorización explícita para enviar las 274 solicitudes de `inputs/expanded_requests_v2.json` a `https://api.openai.com/v1/chat/completions`, con `gpt-5.4-mini`, la clave configurada y un techo local acumulado de US$2. El permiso anterior correspondía al piloto de 12.
2. Ejecutar el conversor; inspeccionar las fuentes recibidas y registrar sus huellas, observaciones y responsable antes de ejecutarlas. Cualquier fallo detiene la secuencia y se documenta; no se sustituye silenciosamente una implementación.
3. Ejecutar la validación ampliada y documentar los controles pareados. La fidelidad completa no se infiere solo de compilación o de partidas sin excepciones.
4. Antes del torneo confirmatorio, implementar la sensibilidad de ventana completa ya comprometida, auditar las descripciones chinas, cerrar comparabilidad y análisis de grupos desiguales y congelar el protocolo.

No se han enviado nuevas solicitudes durante esta implementación. El piloto previo y los paquetes congelados se conservan.
