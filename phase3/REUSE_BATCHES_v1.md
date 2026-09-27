# Reutilización exacta y lotes — preparación local

La implementación conserva 16 calendarios completos y ejecuta una vez cada encuentro cuya identidad computacional es idéntica. No cambia participantes, fuentes, semillas, rondas, pagos ni el contraste H7. Conserva el ejecutor anterior como referencia independiente.

## Calendario materializado

| Cantidad | Valor |
|---|---:|
| Identidades por escenario | 572 |
| Escenarios | 16 |
| Encuentros por escenario, incluyendo autoparejas | 163.878 |
| Resultados en el conjunto de escenarios | 2.622.048 |
| Encuentros computacionalmente distintos | 166.172 |
| Lotes | 665 |
| Tamaño | 664 lotes de 250 y uno de 172 |

La reducción de ejecuciones es aproximadamente 93,66 %. No equivale automáticamente a la misma reducción del tiempo facturado: hay arranque, lectura de fuentes, verificación y persistencia.

Los archivos están en `reuse_plan_v1/`: contexto, manifiesto y los 665 lotes. Son instrucciones de ejecución, **no resultados del torneo**. No repetir el generador sobre la misma carpeta; cualquier modificación exige una versión nueva.

## Regla de reutilización

Cada clave contiene ambos identificadores completos en orden canónico, ambas huellas de fuente, la semilla derivada de esa pareja y la huella del contexto. El contexto incluye los 16 campos, procedencia del adaptador y ejecutor original, entorno requerido, alcance, código del motor nuevo, horizonte y pagos. El mismo código en dos identidades distintas no permite fusionarlas.

Los escenarios que necesitan la misma pareja de implementaciones comparten un resultado, pero se conserva la lista completa de escenarios a los que corresponde. En una autopareja ambas instancias usan siempre la misma implementación de la identidad; no se introduce un encuentro entre la versión principal y alternativa de la misma identidad.

Cada partida usa instancias nuevas mediante el runtime original. Los estados de jugadores nunca se transfieren entre encuentros. La semilla conserva el índice de repetición cero del protocolo de una repetición. Un cambio de fuente, contexto o implementación invalida sus comprobantes.

## Ejecución y recuperación

`reuse_batches_v1.py` genera lotes, verifica identidades y guarda resultados con huellas de su contenido. Puede reanudar un prefijo completo sin volver a ejecutar sus partidas. Las excepciones se registran y bloquean reanudación automática: no se convierten en acciones ni se eliminan de la muestra.

`reuse_worker_v1.py` comprueba el entorno Linux y la procedencia, carga fuentes revisadas y mantiene fábricas de jugadores en caché por proceso. Conserva el manifiesto Windows mediante alias verificados y escritura atómica en Linux, sin modificar las fuentes científicas. Requiere un registro de congelamiento y registro público para ejecutar el campo real.

`reuse_dispatch_v1.py` distribuye lotes entre procesos separados de **un solo servidor Linux**, con dos trabajadores por defecto y máximo cuatro. Exige un límite explícito de lotes por invocación, verifica el manifiesto antes de trabajar y asigna un solo propietario por archivo de resultados. Ante un fallo no envía nuevos lotes; los ya activos pueden terminar y guardar sus resultados. Un archivo de bloqueo evita dos coordinadores en la misma carpeta. Tras una caída abrupta se debe comprobar que no queda otro coordinador antes de retirar un bloqueo obsoleto.

Las escrituras locales son atómicas y se sincronizan a disco. **No se afirma que exista un bloqueo distribuido en un volumen de nube**, ni facturación exactamente una vez: una interrupción antes de guardar puede requerir repetir la última partida. El despliegue de contenedores Modal, la confirmación de sus volúmenes y el control contable acumulado siguen pendientes de integración. No se comparte una base SQLite entre contenedores.

## Matrices y validación

La exportación procesa un escenario cada vez. Verifica cada lote y cada resultado, rechaza pares repetidos, archivos alterados y matrices incompletas; los diagnósticos no pueden exportarse como matrices completas confirmatorias. Conserva CC simétrico y los pagos orientados de cada asiento, incluyendo la diagonal para informes separados; H7 sigue excluyéndola.

**14 pruebas locales aprobadas:** diez del motor y cuatro del coordinador. La prueba principal ejecuta 16 calendarios sintéticos completos con el ejecutor anterior y compara todas las matrices de cooperación y pagos, además de H7, contra el motor reutilizado. Incluye código compartido por varias identidades, estrategias con estado y rivales aleatorios. Todas las matrices coinciden exactamente. La distribución real entre dos procesos independientes también coincide con la ejecución serial; la prueba del coordinador usa trabajadores sintéticos controlados para probar límites y fallos.

Se prueban pausa/reanudación sin recalcular resultados guardados, detención ante fallos, orden distinto de recepción, corrupción de contenidos y rechazo de otra configuración. Las pruebas no usan resultados competitivos del panel real para modificar decisiones metodológicas.

`verify_reuse_plan_v1.py` audita las 166.172 claves y marca independientemente cada pareja en una tabla triangular de cobertura para los 16 escenarios. Debe acreditar exactamente 163.878 parejas por escenario, sin omisiones ni duplicados. Evidencia final: `validation/reuse_closure_v1.json`; informes de pruebas `reuse_tests_v1.xml` y `reuse_dispatch_tests_v1.xml`.

## Continuación

No se gastaron créditos Modal en este paso ni se ejecutaron partidas del torneo real. El saldo posterior al piloto anterior sigue sin verificarse. Próximo: integrar y probar una tanda diagnóstica del nuevo motor en Modal, verificar recuperación remota y actualizar la previsión de consumo con su facturación. Después consolidar/congelar el protocolo y obtener registro temporal público antes del torneo confirmatorio.

La configuración v1 de 16 ejecuciones redundantes se conserva como historial; la configuración v2 referencia este plan y distingue encuentros únicos y resultados lógicos. El presupuesto autorizado sigue siendo US$30 en el workspace `unimayor-evollm`, sin autorización de recargas o cargos adicionales.
