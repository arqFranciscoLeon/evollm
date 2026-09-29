# Paso 12: sensibilidad a la ventana temporal

Fecha: 2026-09-14. Preparación e implementación local completadas. No se ejecutó el torneo mixto ni se hicieron llamadas API.

## Decisión conservada

Se mantiene como principal la interpretación de `window_adjudication_v2.json`: una D entre las observaciones disponibles de las últimas dos rondas basta para responder D. Se implementó la alternativa obligatoria que exige dos rondas completadas antes de aplicar esa represalia.

Las variantes se guardan en `window_sensitivity_v1/pro_aggressive_12.py.txt` y `window_sensitivity_v1/pro_aggressive_14.py.txt`. El único cambio operacional respecto a cada principal es exigir dos observaciones, en lugar de una, para consultar la última defección. Las reglas finales siguen comenzando en las rondas 998 y 996, respectivamente. Se verificó la diferencia exacta y se conservaron los originales y el manifiesto principal.

| Historial disponible | Principal | Alternativa de ventana completa |
|---|---|---|
| Ronda 1: sin observaciones | C | C |
| Ronda 2: el rival comenzó con C | C | C |
| Ronda 2: el rival comenzó con D | D | C |
| Desde ronda 3, ante un mismo historial | Coinciden | Coinciden |
| Final obligatorio de cada estrategia | D | D |

## Comprobaciones y resultados

Se inspeccionaron las dos funciones, que no tienen estado persistente y dependen únicamente de la ronda y de las dos últimas acciones rivales. Se enumeraron todos esos estados de entrada: longitudes de historial 0–999 y todos los sufijos posibles de longitud hasta dos. Los prefijos anteriores se fijaron a C, porque la inspección muestra que estas funciones no los consultan. No se afirma haber enumerado todos los historiales completos.

- **15.980/15.980 comprobaciones** de acción aprobadas: 7.990 por estrategia, contando ambas interpretaciones.
- **44/44 partidas de 1.000 rondas** completas: dos estrategias × dos interpretaciones × 11 rivales clásicos. Cada pareja usó el mismo rival, semilla y configuración, con instancias nuevas.
- En cada estrategia, 6 de los 11 rivales produjeron trayectorias idénticas. Frente a Defector, Random, CyclerDDC y Prober cambió solo la ronda 2 en estas ejecuciones. Frente a SuspiciousTitForTat cambiaron las rondas 2–5.

La equivalencia de decisiones desde ronda 3 vale **ante el mismo historial**. Una acción inicial diferente puede modificar las respuestas del rival y generar historiales posteriores distintos. Por eso estas partidas no prueban que la interpretación sea irrelevante para el torneo ni permiten generalizar a otros rivales o semillas.

## Trazabilidad y aplicación futura

El [plan local](validation/window_sensitivity_plan_v1.json) se escribió antes de estas comprobaciones y partidas. Registra las fuentes, sus huellas, la diferencia exacta, rivales, semillas y la obligación de informar la alternativa independientemente de la dirección o significancia. Es un registro local, no una prerregistración pública.

El [informe de validación](validation/window_sensitivity_v1.json) incluye los resultados y las trayectorias completas de las partidas. El [manifiesto alternativo](validation/western_full_window_candidates_v1.json) conserva 274 identidades y cambia exactamente estas dos implementaciones. Los otros 272 registros conservan sus fuentes seleccionadas, incluidas las correcciones locales ya validadas. Se verificaron todas sus huellas.

Cuando esté cerrado el campo completo y el protocolo, la sensibilidad confirmatoria ejecutará el mismo análisis con ambas variantes sustituidas conjuntamente, manteniendo el resto de participantes y parámetros. Se informarán la estimación principal y la alternativa sin seleccionar por resultado. Esta comparación del torneo sigue pendiente y corresponde a su futura ejecución; el paso 12 de preparación y validación queda completado.

**Siguiente paso del programa: 13, auditoría de las descripciones chinas.**
