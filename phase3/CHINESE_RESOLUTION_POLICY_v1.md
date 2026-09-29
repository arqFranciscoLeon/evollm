# Resolución de especificaciones, errores y conversión común

Fecha: 2026-09-14. Decisiones locales posteriores a la auditoría y anteriores al torneo. No son un registro público ni recuperación de intención histórica. Se aplican sin consultar ganancias, rankings ni resultados del torneo.

## Cuatro especificaciones

1. **DeepSeek Aggressive_5: excluir del corpus de conversión fiel.** La ronda 2 tras C rival carece de una regla. Asignar D sería completar el insumo. Se conserva el original como archivo histórico, igual que las exclusiones occidentales por reglas ausentes.
2. **Kimi Aggressive_12: excluir del corpus de conversión fiel.** No se especifica la acción tras una o dos C iniciales antes de completar tres. La persistencia de la acción inicial no se presume para completar esa rama. Sus posibles fallos de código no se corrigen como si la prosa estuviera completa.
3. **Kimi Aggressive_25: interpretación principal del par simultáneo completado.** «Immediately after you play Cooperate» se operacionaliza detectando C propio y D rival en la misma ronda completada, como una señal conductual de explotación y sin atribuir causalidad. La alternativa obligatoria detecta C propio en t-1 seguido por D rival en t. Ambas mantienen D permanente tras el disparador y la acción inicial D.
4. **GLM Aggressive_20: diez rondas completadas.** Se aplica la convención común de rachas completas: el sondeo D se activa tras diez CC completados. La alternativa obligatoria usa nueve CC completados, contando la decisión actual como décima. Se mantienen inicio D, final D en 991–1000 y las demás ramas. No se presupone la acción simultánea aún no observada del rival.

Las dos sensibilidades se conservarán e informarán cualquiera sea su dirección o significancia. No se sustituirá la principal por la alternativa que favorezca una hipótesis.

Resultado: **298 descripciones chinas elegibles y 2 excluidas**, de las cuales dos elegibles requieren las interpretaciones declaradas. Junto con las 274 occidentales hay **572 entradas elegibles para una nueva conversión común**, no 572 programas ya admitidos al torneo.

## Once errores de implementación

Se aplica la política simétrica de correcciones v1: conservar los originales, crear fuentes derivadas por separado, registrar diferencias y huellas y repetir las comprobaciones afectadas. Las correcciones se limitan a las ramas explícitas de la prosa y no buscan mejorar desempeño.

Estos derivados resuelven la fidelidad del archivo para controles y comparaciones, pero no se presentan como nuevas respuestas del modelo ni reemplazan una conversión común del estudio principal. El resultado original de auditoría (285 pasan, 11 discrepancias, 4 sin especificación cerrada entonces) permanece intacto.

## Compatibilidad de conversión

Se elige preparar una **nueva tanda uniforme de 572 entradas**: 274 occidentales y 298 chinas. Todas recibirán la misma plantilla, el mismo texto de convenciones ampliadas y los mismos parámetros. Las descripciones archivadas se conservarán literalmente; las nuevas convenciones se añadirán por igual a cada solicitud. Solo cambian las descripciones.

La plantilla será v3: conserva íntegro el contrato occidental anterior y agrega a todos los casos las dos convenciones temporales recién declaradas. Reconvertir también Occidente evita mezclar silenciosamente contratos. Se preservan las 274 respuestas previas como controles pareados, sin seleccionar versiones por puntuación.

La ejecución deberá registrar la versión efectivamente servida, consumos, errores y fuentes. Toda respuesta nueva requiere inspección y validación; las reparaciones anteriores no se trasladan automáticamente al resultado nuevo. Usar igual proceso mejora el control metodológico, pero no prueba ausencia de sesgos del conversor ni equivale a reproducir bit a bit las generaciones históricas.

Se prepara el paquete sin red. La autorización previa correspondía a 274 solicitudes occidentales; no cubre por sí sola esta nueva tanda de 572. Antes de cualquier envío se presentarán el paquete exacto, el destino y el techo de gasto. Hasta completar esa ejecución y validación, la compatibilidad operacional queda preparada, no demostrada por resultados nuevos.
