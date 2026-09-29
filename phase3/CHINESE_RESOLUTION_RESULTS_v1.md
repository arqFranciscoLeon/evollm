# Resolución local y preparación de conversión uniforme

Fecha: 2026-09-14. Las especificaciones y correcciones locales están resueltas y validadas. La nueva conversión común está preparada, pero no enviada.

## Cuatro especificaciones resueltas

| Caso | Resolución |
|---|---|
| DeepSeek Aggressive_5 | Excluir: falta la acción de ronda 2 tras C rival. No se completa desde el código. |
| Kimi Aggressive_12 | Excluir: falta la acción antes de completar tres C iniciales. Se aplica el criterio occidental de no inventar ramas. |
| Kimi Aggressive_25 | Principal: C propio y D rival en el mismo par completado. Alternativa obligatoria: C propio en la ronda anterior a la D rival. La represalia posterior es permanente. |
| GLM Aggressive_20 | Principal: ventana de diez CC completados. Alternativa obligatoria: nueve CC completados más la decisión actual como décima. Se conservan las otras ramas. |

Las interpretaciones son decisiones declaradas, no intención histórica recuperada. Las variantes se conservan aunque sus resultados no favorezcan una hipótesis. Véase la [política congelada](CHINESE_RESOLUTION_POLICY_v1.md).

## Once errores corregidos sin alterar originales

Se prepararon once funciones derivadas con diferencias y huellas: tres de DeepSeek, tres de Kimi y cinco de GLM. Corrigen inversión de respuesta, uso del pago anterior, acción inicial, permanencia de estados, copia dinámica y límites finales. Las dos adjudicaciones añaden cuatro fuentes separadas, principal y alternativa por caso.

Las **15 funciones derivadas** pasaron **219.765 comprobaciones de acción** y **165 partidas de 1.000 rondas**, sin fallos. Se comprobaron historiales controlados y generados por los propios candidatos, además de los 11 rivales clásicos. Son verificaciones concretas, no prueba de equivalencia exhaustiva ni resultados del torneo.

- [Registro de cambios y fuentes](inputs/chinese_resolution_v1.json).
- [Validación reproducible](validation/chinese_resolution_v1.json).
- [Manifiesto derivado chino](validation/chinese_derived_candidates_v1.json): **285 originales + 11 correcciones + 2 adjudicaciones = 298**.

El resultado de la auditoría original permanece 285/11/4. Las correcciones locales no se cuentan como respuestas correctas originales del conversor. Los datos y resultados de los artículos no se han modificado.

## Conversión compatible: paquete común v3

La nueva tanda contiene **572 solicitudes exactas**, con 28 exclusiones respecto a las 600 entradas Default iniciales. Las 26 occidentales permanecen; se suman las dos chinas con reglas ausentes.

| Modelo | Entradas |
|---|---:|
| Sonnet | 75 |
| Flash | 73 |
| Gemini Pro | 59 |
| GPT | 67 |
| DeepSeek | 74 |
| Qwen | 75 |
| Kimi | 74 |
| GLM | 75 |
| **Total** | **572** |

Se mantiene literalmente la prosa archivada. Las 572 solicitudes tienen la misma plantilla, convenciones y parámetros; solo cambia la descripción. Las dos nuevas convenciones se agregan a todas, incluidas las occidentales. Por eso se reconvierten ambas cohortes: reutilizar la tanda occidental v2 mezclaría contratos. Las 274 respuestas occidentales anteriores se conservan como controles, sin escoger por desempeño.

Se fija `gpt-5.4-mini-2026-03-17`, temperatura 0, esfuerzo `none`, salida máxima 4096 tokens y servicio estándar. El ejecutor rechaza una versión servida diferente, incluido el alias sin fecha. La [documentación oficial de OpenAI](https://developers.openai.com/api/docs/models/gpt-5.4-mini), consultada el 2026-09-14, confirma ese snapshot y tarifas de US$0,75 / US$0,075 / US$4,50 por millón de tokens de entrada / caché / salida. Fijar versión no garantiza reproducibilidad bit a bit.

El orden de solicitudes se barajó con semilla fija antes de ejecución para intercalar modelos. Los identificadores de cohortes no se envían como etiquetas al modelo.

[Paquete exacto](inputs/uniform_requests_v3.json), SHA-256 `122202af19a17ac474ec19c2e8c77d35c1cc50b95e503ccbf24d5bd8971eaad2`.

## Presupuesto y estado de ejecución

Techo local propuesto: **US$2 para las 572 solicitudes**, sin reintentos automáticos ni recargas. Reserva US$0,318432 antes de cada intento; concilia consumo verificable, conserva reservas inciertas y detiene la tanda ante error o versión inesperada. El límite puede detener la tanda antes de completar las 572.

La extrapolación lineal de la tanda anterior es US$0,524501; no incluye el texto adicional ni la posible mayor longitud del código chino, por lo que no es una cotización. No se consultó el saldo de la cuenta ni se gastó en API durante esta preparación.

`uniform_converter.py` está implementado. Sus **9 pruebas** aprobaron: uniformidad de los 572 prompts, integridad de prosa, reanudación, reserva, presupuesto, versión inesperada, consumo incierto, truncación y final del plan. La comprobación sin red verificó 572 solicitudes y **cero intentos**.

La compatibilidad metodológica está definida y la ejecución preparada. Para realizarla falta autorización específica del nuevo contenido/destino/gasto; la autorización previa cubría la tanda occidental de 274. Tras enviar, habrá que inspeccionar y validar todas las respuestas nuevas con el mismo entorno y política para ambos grupos, conservando los errores y controles. Ninguna corrección archivística se transferirá silenciosamente a los códigos nuevos.

Comando previsto tras autorización: `python -m phase3.uniform_converter --live`. Sin `--live`, el módulo solo comprueba integridad y estado.
