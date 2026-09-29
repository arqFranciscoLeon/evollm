# Analizador H7 adaptado a tamaños desiguales

La implementación de `analyze_phase3.py` admite ahora las 24 celdas del [protocolo v0.3](DESIGN_v0.3_DRAFT.md): 572 participantes, con 172 estrategias agresivas, 200 cooperativas y 200 neutrales. Queda resuelto el primer requisito de implementación de su sección 7. El protocolo y su registro de población se conservan con sus huellas anteriores; este documento registra el avance posterior.

## Cambio

Se eliminó la exigencia de que todas las celdas modelo/actitud tengan igual tamaño. Se conserva el mínimo de dos estrategias en **cada** celda, necesario para calcular la cooperación dentro de un modelo y actitud sin autoparejas.

La fórmula ya utilizaba los denominadores reales: `n × (n − 1)` para una celda consigo misma y `n × m` entre celdas distintas. Se mantiene el peso igual por modelo y por par de actitudes; no se reemplaza por un promedio ponderado por cantidad de encuentros. Las permutaciones siguen barajando las etiquetas existentes dentro de cada actitud, por lo que preservan automáticamente las cuotas desiguales.

No cambiaron las firmas de las funciones, los campos de resultado, la semilla predeterminada ni las 10.000 permutaciones predeterminadas. Se mantienen el rechazo de datos incompletos o inválidos fuera de la diagonal y la exigencia de simetría de CC. Las autoparejas no influyen, incluso cuando su diagonal contiene NaN; la matriz proporcionada por el usuario no se modifica.

## Verificación

**19 pruebas aprobadas** en 29,21 segundos: 11 pruebas nuevas de tamaños desiguales y ocho de regresión.

- Comparación de los seis contrastes con una enumeración independiente de parejas no ordenadas, sobre una matriz sintética heterogénea de tres modelos con tamaños distintos.
- Caso calculable a mano que distingue el peso igual por modelo del promedio por cantidad de parejas; invariancia al reordenar participantes.
- Rechazo de celdas ausentes o con una sola estrategia, partidas faltantes, valores fuera de rango, asimetría y metadatos incompatibles.
- Reproducibilidad de las permutaciones y resultado nulo conocido en una matriz constante.
- Matriz sintética con las 572 identidades del manifiesto: contraste esperado 0,6; conservación de las 24 cuotas en 100 permutaciones; ejecución completa de inferencia con nueve permutaciones de prueba.
- Regresión del comportamiento equilibrado y de los controles locales existentes.

Los valores sintéticos verifican funcionamiento; no son evidencia de compatibilidad entre modelos. No se ejecutaron las 10.000 permutaciones del futuro análisis confirmatorio ni el torneo mixto. No hubo llamadas API.

Evidencia: [registro de pruebas y huellas](validation/h7_unequal_v1.json), [pruebas nuevas](tests/test_h7_unequal.py) y [regresión](tests/test_phase3.py).

Comando de pruebas:

```text
python -m pytest phase3/tests/test_h7_unequal.py phase3/tests/test_phase3.py -q -p no:cacheprovider --basetemp <directorio_temporal_autorizado>
```

Siguiente dependencia: integrar el manifiesto derivado y el adaptador común con el ejecutor y comprobar carga, puntuaciones y reanudación. Las sensibilidades, configuración definitiva y registro público siguen pendientes antes del torneo confirmatorio.
