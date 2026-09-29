# Integración del corpus con el ejecutor

**Integración completada y verificada.** `execute_uniform.py` carga las 572 estrategias del manifiesto derivado con el adaptador validado, conserva sus identidades completas y registra las partidas en SQLite. El torneo confirmatorio no se ha ejecutado.

## Qué incorpora

- Comprueba las huellas del manifiesto, informes de validación, adaptador, runtime y todas las fuentes antes de compilar las estrategias. Verifica las versiones de Python y Axelrod del entorno validado.
- Conserva identificadores completos como `modelo/default/Neutral_1` fuera de los jugadores; no mezcla clases homónimas de distintos modelos ni entrega etiquetas del rival a las estrategias.
- Crea dos instancias nuevas en cada partida, incluso en autoparejas, y mantiene la actualización de puntuaciones del adaptador común. No modifica las 562 respuestas originales ni las diez fuentes corregidas.
- Fija el orden canónico de las parejas y deriva cada semilla de ambos identificadores y la repetición. Registra CC, CD, DC, DD y pagos de cada asiento, sin sustituir acciones inválidas.
- Ancla cada base de datos a las fuentes, configuración y versión del ejecutor. Reanuda sin duplicados; un cambio incompatible exige otra base. Un error se conserva y bloquea los reintentos automáticos.
- Exporta matrices de cooperación mutua y pagos, con sus identificadores, modelos y actitudes, solo cuando el calendario completo está íntegro. Rechaza diagnósticos parciales como insumos del análisis confirmatorio.

Los módulos y fuentes previamente validados permanecen intactos. La integración usa `runtime.play_pair` y `uniform_semantics_v3b.compile_candidate`; no aplica un segundo decorador de puntuación a las funciones.

## Verificación realizada

**29 pruebas de software aprobadas** en 16,56 segundos: diez del ejecutor y 19 del analizador y regresión. Cubren reanudación frente a una ejecución continua con semillas iguales, identidades homónimas, autoparejas, cambios de configuración y fuentes, conservación de errores, conteos y pagos, aislamiento de diagnósticos, puntuaciones entre dos jugadores generados y estado limpio entre partidas.

La prueba completa del enlace con H7 ejecuta un campo sintético de 12 identidades, exporta las matrices y obtiene el contraste conocido de 0,5. Ese valor es una expectativa de prueba, no un resultado sobre los modelos del proyecto.

El diagnóstico con fuentes reales incluyó **580 partidas de 1.000 rondas: 572 cruces entre modelos y ocho autoparejas**, cubriendo todas las identidades. Selección independiente de puntuaciones: cada identidad ordenada contra la primera identidad del siguiente modelo en orden lexicográfico circular; la primera identidad de cada modelo también juega consigo misma. No pretende cubrir todas las parejas posibles.

| Etapa | Partidas nuevas | Acumuladas | Errores |
|---|---:|---:|---:|
| Parada deliberada | 37 | 37 | 0 |
| Reanudación | 543 | 580 | 0 |
| Reanudación de comprobación | 0 | 580 | 0 |

Se verificaron 580.000 rondas guardadas. La integración tomó aproximadamente 88 segundos incluyendo carga y comprobaciones. No se extrapola ese tiempo como duración garantizada del torneo completo: el calendario diagnóstico es distinto.

No se calcularon rankings ni H7 con estos encuentros reales. Sus datos están identificados como diagnóstico y no deben incorporarse al conjunto confirmatorio. No hubo llamadas API ni gasto adicional.

## Uso

Desde la copia de trabajo, con el entorno `D:/evollm/.phase3-venv`, el comando predeterminado solo verifica y carga el campo:

```text
python -m phase3.execute_uniform
```

La comprobación ya realizada puede reanudarse con la misma configuración; si está completa, ejecuta cero partidas nuevas:

```text
python -m phase3.execute_uniform --diagnostic --database phase3/validation/uniform_integration_v1.sqlite
```

El modo completo `--run` exige una base indicada explícitamente y `--repetitions`; no tiene un número implícito de repeticiones. Se mantiene pendiente su uso hasta cerrar las sensibilidades, configuración y registro del protocolo. El CLI conserva el horizonte validado de 1.000 rondas.

Para el analizador, `export_matrices(database, field)` entrega `cooperation`, `models` y `attitudes` compatibles con `h7_statistic` y `permutation_test`, además de `ids` y la matriz orientada `payoff`. La exportación comprueba cobertura, semillas, estados, conteos y pagos de las partidas persistidas. No ejecuta automáticamente las permutaciones.

## Evidencia y continuidad

- [Ejecutor](execute_uniform.py).
- [Pruebas del ejecutor](tests/test_uniform_executor.py).
- [Evidencia final y huellas](validation/uniform_executor_tests_v1.json).
- [Registro del diagnóstico](validation/uniform_integration_v1.json).
- [Base SQLite del diagnóstico](validation/uniform_integration_v1.sqlite).

El registro del diagnóstico documenta las 28 pruebas disponibles al iniciarlo; el registro final añade la prueba del enlace completo con H7, para un total de 29.

Queda resuelta la integración requerida por el protocolo v0.3. El siguiente trabajo es cerrar e implementar las sensibilidades a duplicados, exclusiones y cuatro interpretaciones, fijar repeticiones y recursos, y congelar y registrar el protocolo antes de ejecutar el torneo confirmatorio.
