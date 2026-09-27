# Sensibilidades preespecificadas — complemento local de v0.3

Fecha: 2026-09-21. Estado: preparación local, pendiente de congelamiento y registro público. No se han calculado resultados confirmatorios. Este complemento conserva el protocolo v0.3 y sus huellas; actualiza su requisito 3. No altera H7 principal.

## Duplicados de código

Se mantienen las 572 identidades. Un grupo sintáctico es el SHA-256 de `ast.dump(ast.parse(source), include_attributes=False)`: omite formato, comentarios y posiciones; conserva nombres y estructura. No representa equivalencia conductual. Se utiliza la fuente seleccionada del campo principal, incluidas las diez correcciones declaradas.

Dentro de cada celda modelo × actitud, cada identidad recibe peso 1/n, donde n es la multiplicidad de su grupo sintáctico en esa celda. Cada pareja recibe el producto de los pesos; se excluye i=j y se normaliza por la suma de productos de pesos de parejas admisibles de esa pareja de celdas. Sobre estas medias se aplica el mismo contraste de H7: igual peso a modelos y a los seis pares de actitudes.

La interpretación es extraer independientemente identidades con masa inicial igual por plantilla dentro de cada celda, condicionado a que sean identidades distintas. La condición modifica las masas relativas en una misma celda: **no** se afirma dar igual peso a cada par de plantillas ni eliminar toda dependencia. Dos identidades con el mismo AST sí pueden enfrentarse. Una celda con una sola plantilla sigue siendo válida si contiene al menos dos identidades. El peso es local a la celda; una plantilla compartida entre modelos no fusiona sus etiquetas.

Se presenta como contraste descriptivo secundario junto al principal, sin p-valor adicional. No se seleccionan representantes ni se eliminan celdas. Esta ponderación se aplica al escenario principal; no se multiplica por los 16 escenarios de interpretación.

## Exclusiones

El objetivo de esta sensibilidad es el panel original de 600 identidades, 25 por cada una de las 24 celdas. Se conservan las contribuciones observadas de las 572; cada encuentro que involucra una identidad excluida tiene cooperación mutua desconocida en [0,1]. Los denominadores corresponden al panel original y excluyen autoparejas.

H7 es lineal en esas tasas: los coeficientes son positivos dentro de modelo y negativos entre modelos. El límite inferior asigna cero a encuentros desconocidos dentro de modelo y uno a los desconocidos entre modelos; el superior hace lo contrario. Se incluyen encuentros entre dos excluidas y se respeta simetría. Las 28 ausencias son agresivas.

Son límites algebraicos conservadores, no estrategias imputadas ni intervalos de confianza. No se presupone que sus extremos sean realizables conjuntamente por estrategias fieles. Se informará si el intervalo cruza cero, sin tratar ello como prueba de ausencia de efecto. Se aplica al escenario principal y no recupera prosa ausente ni permite generalizar causalmente a todos los modelos.

## Cuatro interpretaciones y 16 escenarios

Orden fijo de bits del identificador 0..15:

1. Gemini Pro Aggressive_12: exigir dos observaciones antes de responder a D en la ventana.
2. Gemini Pro Aggressive_14: la misma alternativa, conservando su umbral final propio.
3. Kimi Aggressive_25: comparar acción propia de hace dos rondas con la última del rival para activar defección permanente.
4. GLM Aggressive_20: nueve CC completados, frente a diez en el escenario principal.

El escenario 0 conserva el campo principal; 3 sustituye conjuntamente las dos ventanas Pro, como ya estaba previsto; 15 sustituye las cuatro interpretaciones. Se informan los 16 contrastes, incluidos los cuatro cambios individuales y todas las combinaciones, sin elegir según signo o significación. Se reportan diferencia respecto del principal y mínimo/máximo del conjunto: ese rango es sensibilidad a interpretación, no un intervalo de confianza.

Cada escenario mantiene exactamente las mismas 572 identidades y márgenes. Solo sustituye las fuentes seleccionadas y registra su procedencia local. La alternativa histórica Kimi requiere únicamente renombrar su variable privada de estado para el adaptador congelado; se conserva la original y se comprueba la copia contra el oráculo de interpretación. No se presenta como una nueva respuesta de modelo.

`interpretation_sensitivity_v1.load_scenario(mask)` produce un `Field` para el ejecutor común sin modificarlo. Se usarán bases SQLite separadas y la misma configuración y semillas para todos los escenarios. La exportación exige calendarios completos. **No está implementada la reutilización de partidas entre escenarios**: la estimación de recursos debe presupuestar 16 calendarios completos, salvo que antes del congelamiento se implemente y valide explícitamente otra ejecución equivalente.

Los contrastes alternativos son descriptivos, sin nuevas pruebas de significación ni selección del escenario principal. La prueba de permutación confirmatoria sigue siendo únicamente la del campo principal.

## Incertidumbre y límites

El intervalo de permutaciones sigue siendo referencia bajo la hipótesis nula, no incertidumbre del tamaño de efecto. No se propone un bootstrap de parejas: las parejas comparten estrategias y no son unidades independientes. Los resultados se interpretan condicionalmente al panel archivado, sin un intervalo de confianza poblacional adicional. Los rangos de interpretación y exclusión se etiquetan por separado. La variación entre repeticiones, si corresponde tras fijar aleatoriedad y recursos, se describirá como variación de ejecución y tampoco sustituirá un intervalo poblacional.

## Dependencias restantes

La integración de los 16 campos quedó verificada: 41 pruebas de software aprobadas; las cuatro variantes pasaron 58.604 comprobaciones semánticas y 44 partidas de 1.000 rondas. La prueba de reanudación usa cuatro autoparejas alternativas de 20 rondas y comprueba separación de configuraciones y rechazo de exportación diagnóstica. Es validación dirigida, no garantía de ausencia de fallos ante cualquier rival.

Falta fijar repeticiones, semillas y recursos, consolidar el protocolo, congelar versiones y obtener registro temporal público antes del torneo. Las pruebas locales de estas sensibilidades no autorizan ni constituyen una ejecución confirmatoria. Evidencia: `inputs/sensitivity_plan_v1.json`, `validation/interpretation_sensitivity_v1.json`, `validation/sensitivity_tests_v1.xml` y `validation/sensitivity_closure_v1.json`.
