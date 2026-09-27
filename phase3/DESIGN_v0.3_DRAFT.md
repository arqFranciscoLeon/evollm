# Torneo mixto: protocolo de trabajo v0.3

Fecha: 2026-09-14. **Versión vigente del diseño local, actualizada con 572 participantes.** Sigue siendo un borrador: no está congelado ni registrado públicamente y no se han obtenido resultados del torneo confirmatorio. Conserva [v0.2](DESIGN_v0.2_DRAFT.md) y [v0.1](../PHASE3_PREREG.md) como historial; no modifica retroactivamente sus supuestos.

## 1. Pregunta y alcance

Evaluar si las estrategias procedentes del mismo modelo mantienen más cooperación mutua que las procedentes de modelos distintos, controlando la actitud y usando un procedimiento común de conversión de prosa a código. El estudio principal utiliza Default, dilema del prisionero iterado limpio, ocho modelos y siete laboratorios. Google aporta dos modelos: modelo y laboratorio no son unidades intercambiables.

La inferencia se refiere a este corpus archivado elegible. No permite atribuir causalmente diferencias a entrenamiento, alineamiento o procedencia geográfica, ni generalizar a todas las respuestas posibles de cada modelo. Las estrategias no reciben etiquetas identificadoras de sus rivales.

Prose y Refine permanecen como exploraciones secundarias condicionadas a integridad de insumos y recursos; su ejecución no se decidirá según la significancia de Default. H8 queda fuera de la confirmación: las comparaciones con los artículos previos serán descriptivas y distinguirán los procesos de conversión. H9, retroalimentación y Torneo 2 requieren un protocolo separado con control contemporáneo sin retroalimentación.

## 2. Corpus efectivo y procedencia

Fuente de autoridad: [manifiesto derivado](validation/uniform_derived_candidates_v1.json), SHA-256 `d5725c7a63125a0cbdee1ddc24e4d2731dc60f6ad0734d3c670d5b23f9181062`. Las 572 identidades tienen rutas y huellas de sus fuentes. Cualquier cambio posterior exige una nueva versión del manifiesto y una enmienda documentada.

| Modelo (identificador del manifiesto) | Agresivas | Cooperativas | Neutrales | Total | Exclusiones de las 75 iniciales |
|---|---:|---:|---:|---:|---:|
| Sonnet (`anthropic_sonnet46`) | 25 | 25 | 25 | 75 | 0 |
| DeepSeek (`deepseek_v4pro`) | 24 | 25 | 25 | 74 | 1 |
| Gemini Flash (`gemini_25_flash`) | 23 | 25 | 25 | 73 | 2 |
| Gemini Pro (`gemini_31_pro`) | 9 | 25 | 25 | 59 | 16 |
| GLM (`glm_51`) | 25 | 25 | 25 | 75 | 0 |
| Kimi (`kimi_k25`) | 24 | 25 | 25 | 74 | 1 |
| GPT (`openai_gpt54mini`) | 17 | 25 | 25 | 67 | 8 |
| Qwen (`qwen3max`) | 25 | 25 | 25 | 75 | 0 |
| **Total** | **172** | **200** | **200** | **572** | **28** |

Las 28 exclusiones son agresivas: 26 occidentales y dos chinas. Las causas y decisiones constan en las revisiones de prosa y en la [política de resolución](CHINESE_RESOLUTION_POLICY_v1.md); no todas obedecen a truncación. No se completarán reglas ausentes desde el código histórico ni se incorporarán reemplazos para recuperar artificialmente 25 entradas por celda. Las dos adjudicaciones chinas permanecen incluidas bajo sus interpretaciones principales declaradas.

Ambas cohortes se reconvirtieron en una tanda común: 274 occidentales y 298 chinas, misma plantilla v3, convenciones y parámetros, snapshot efectivamente servido `gpt-5.4-mini-2026-03-17` en las 572 respuestas. Se conservaron literalmente las descripciones. El coste calculado fue US$0,58549125, sin reintentos; no es una factura. Esta uniformidad no demuestra ausencia de sesgos del conversor ni reproducibilidad bit a bit del código histórico.

El campo principal utiliza **562 respuestas originales y diez correcciones locales de fidelidad**. Se aplica la misma política a ambos grupos, sin consultar resultados competitivos. El recuento original sigue siendo 562 aprobadas, nueve discrepancias y un error de ejecución; las correcciones no se cuentan como aciertos originales del modelo. Las diez fuentes derivadas pasaron 146.510 comprobaciones y 110 partidas. Véase el [cierre de validación](UNIFORM_CLOSURE_v1.md).

Adaptador común: `uniform_semantics_v3b.py`, SHA-256 `3e9bdfdc4f918759dc9d7642a20c90ec8b92e8b3b60de1832d2548ea74e3963b`. La integración con el ejecutor deberá preservar las fuentes, la actualización de puntuaciones y la prohibición de sustituir acciones inválidas por D.

## 3. Encuentros y denominadores efectivos

El campo contiene 163.306 parejas no ordenadas de identidades distintas: 20.277 dentro del mismo modelo y 143.029 entre modelos. Hay además 572 autoparejas. Una repetición completa con autoparejas comprende **163.878 partidas**. No se ejecutarán dos partidas por invertir los identificadores de una pareja; la matriz simétrica de cooperación podrá representar ambas orientaciones de un mismo encuentro.

| Estrato de actitudes, sin autoparejas | Parejas no ordenadas |
|---|---:|
| Agresiva–Agresiva | 14.706 |
| Agresiva–Cooperativa | 34.400 |
| Agresiva–Neutral | 34.400 |
| Cooperativa–Cooperativa | 19.900 |
| Cooperativa–Neutral | 40.000 |
| Neutral–Neutral | 19.900 |
| **Total** | **163.306** |

Se mantiene el horizonte de 1.000 rondas, ruido cero y pagos clásicos T=5, R=3, P=1, S=0. Veinte repeticiones continúan como referencia provisional heredada: supondrían 3.277.560 partidas incluyendo autoparejas, no una estimación de duración ni una decisión ya congelada. El número final y su justificación de precisión o reproducibilidad se cerrarán antes de observar resultados; las repeticiones idénticas de estrategias deterministas no se tratarán como muestras independientes.

Los rivales clásicos son diagnósticos separados: no aumentan el campo de 572 ni entran en los denominadores de H7. Las autoparejas se informan por separado y se excluyen de H7.

## 4. H7: contraste equilibrado con celdas desiguales

La variable primaria `C_ij` es la fracción de rondas con cooperación de ambos jugadores (CC), acumulada sobre las repeticiones completas de la pareja i,j. Su denominador es `1.000 × R`, donde R será el número fijado de repeticiones. Se conservarán por separado CC, CD, DC, DD y pagos; el promedio de cooperación unilateral no sustituye a CC.

Sea `G_ma` el conjunto de estrategias del modelo m y actitud a, y `n_ma` su tamaño en la tabla. Para cada combinación de celdas, `mu(ma,kb)` es el promedio de `C_ij` sobre i en `G_ma`, j en `G_kb`, excluyendo i=j:

- Si ambas celdas coinciden, el denominador de la matriz orientada es `n_ma × (n_ma − 1)`.
- Si las celdas son distintas, es `n_ma × n_kb`.
- En una tabla de parejas no ordenadas, una celda idéntica tiene `n_ma × (n_ma − 1) / 2` parejas; promediar sus valores una vez da el mismo resultado.

Para cada modelo m y cada uno de los seis pares no ordenados de actitudes a,b, se define:

```text
W(m,a,b) = mu(ma,mb)
B(m,a,b) = (1/7) × suma sobre k distinto de m
           de [mu(ma,kb) + mu(mb,ka)] / 2
Delta(m,a,b) = W(m,a,b) − B(m,a,b)
T_H7 = (1/48) × suma de Delta(m,a,b) sobre 8 modelos y 6 pares de actitudes
```

Cada modelo recibe peso 1/8 y cada par de actitudes 1/6. Dentro del contraste entre modelos, cada modelo rival recibe peso 1/7 y, para actitudes distintas, ambas asignaciones de actitud reciben el mismo peso. Para actitudes iguales las dos asignaciones coinciden. El efecto se informará también en puntos porcentuales, `100 × T_H7`, junto con los contrastes desagregados.

Estos pesos definen un contraste estandarizado; no equivalen al promedio de todas las parejas disponibles. Evitan que los grupos grandes dominen solo por aportar más encuentros, pero no corrigen sesgos de selección causados por la prosa excluida. Las estimaciones de las celdas pequeñas, especialmente las nueve agresivas de Gemini Pro, tendrán soporte empírico menor y se mostrarán con sus denominadores.

La matriz debe estar completa fuera de la diagonal: no se eliminarán silenciosamente partidas fallidas ni se recalcularán promedios sobre casos completos. Una excepción o acción inválida bloquea el análisis confirmatorio hasta resolver y documentar la causa bajo la política establecida. Cualquier cambio de código requiere nueva huella y repetición de los encuentros afectados; un cambio del adaptador común invalida todos los encuentros que lo usaron. La ausencia de fallo en diagnósticos no garantiza ausencia de fallo ante cualquier rival.

## 5. Permutaciones con márgenes reales

Se mantienen 10.000 permutaciones de etiquetas de **modelo a nivel de estrategia**, restringidas a cada actitud. Se baraja el vector existente de etiquetas; no se vuelve a asignar una cuota de 25. Por tanto, cada permutación conserva exactamente las 24 celdas de la tabla: por ejemplo, nueve etiquetas Gemini Pro y 17 GPT entre las 172 agresivas, y 25 por modelo entre las cooperativas y neutrales.

La etiqueta permutada de una estrategia se aplica conjuntamente a su fila y columna; no se permutan encuentros como observaciones independientes. Se conserva la matriz de acciones y se recalcula el mismo contraste con los tamaños de celda preservados. Se fijará la semilla en la configuración congelada; se mantiene como referencia la semilla local 20260913 del analizador existente.

Para la alternativa direccional de mayor cooperación dentro del modelo, `p = (1 + número de T_permutado ≥ T_observado) / (10.000 + 1)`. El intervalo entre los cuantiles 2,5 % y 97,5 % de permutaciones es una referencia de la distribución nula, **no un intervalo de confianza del efecto**. La interpretación depende de intercambiabilidad condicional dentro de actitud; preservar los márgenes no vuelve aleatorias las exclusiones. No se interpretará un resultado nulo como prueba de ausencia de mecanismos relacionados con el modelo.

## 6. Composición, duplicados y sensibilidades

El campo observado contiene 172/572 agresivas, 200/572 cooperativas y 200/572 neutrales. Se informarán por separado resúmenes empíricos de ese campo y resúmenes estandarizados; no se describirá el campo como 25/25/25 por modelo.

Se conservan las mezclas contrafactuales de actitudes previstas en v0.2: equilibrada (1/3,1/3,1/3) y tres mezclas con una actitud dominante (2/3,1/6,1/6). Para resumir encuentros de una estrategia focal sin autopareja, cada actitud recibe su peso objetivo; dentro de ella, cada modelo rival recibe 1/8, incluido el modelo de la focal, y el peso se divide por el número real de estrategias elegibles en esa celda, descontando la focal si pertenece a ella. Todas las celdas mantienen al menos ocho rivales tras ese descuento. Estas mezclas son resúmenes ponderados de encuentros, no nuevas poblaciones observadas ni una dinámica evolutiva.

Las 572 identidades se mantienen aunque compartan código. El manifiesto derivado contiene 152 fuentes distintas por SHA-256 y 130 AST distintos al omitir posiciones y comentarios. No son recuentos exhaustivos de conductas diferentes. La definición exacta de ponderación o selección para la sensibilidad a duplicados sigue pendiente de fijación y prueba antes del torneo; no se elegirá según el resultado de H7.

Se mantienen las cuatro sensibilidades de interpretación: ventana completa para Gemini Pro Aggressive_12 y Aggressive_14; desfase alternativo de Kimi Aggressive_25; nueve CC completados para GLM Aggressive_20 frente a diez en la principal. Sustituyen la implementación de la misma identidad, sin añadir participantes ni alterar los márgenes de la tabla. Se informarán cualquiera sea su dirección. Su integración con el campo común y la especificación de ejecuciones separadas o combinadas deberán cerrarse antes de congelar el protocolo.

La sensibilidad a exclusiones debe reconocer que faltan 28 descripciones agresivas y que sus conductas fieles no están identificadas; no se imputarán estrategias inventadas. Los análisis archivísticos, si se realizan, tendrán manifiesto y alcance distintos y no sustituirán silenciosamente al estudio principal.

Una dinámica ecológica sigue siendo una extensión secundaria opcional: ecuación, tratamiento de pagos y criterios de parada requieren especificación separada. No se inferirá estabilidad evolutiva solo de una trayectoria numérica estacionaria.

## 7. Requisitos pendientes antes de congelar y ejecutar

1. **Adaptar y probar el analizador para celdas desiguales.** `analyze_phase3.py` ya calcula medias con tamaños de celda, pero `validate_matrix` todavía exige equilibrio. Debe admitir los tamaños reales, manteniendo como mínimo dos estrategias por celda, rechazo de datos faltantes y conservación de márgenes en las permutaciones. Este protocolo actualiza la especificación; no certifica que el código ya implemente el cambio.
2. Integrar el manifiesto derivado y el adaptador común en el ejecutor, verificar identidades y huellas, y ejecutar diagnósticos mixtos de carga, estados, puntuaciones y reanudación. La validación contra rivales clásicos no sustituye a esta integración.
3. Cerrar e implementar sensibilidad a duplicados, exclusiones e interpretaciones; definir la presentación de incertidumbre adicional sin confundirla con la referencia nula de permutaciones.
4. Fijar repeticiones, configuración, semillas y estimación de recursos mediante calibración ajena a los resultados de H7.
5. Congelar protocolo y código en control de versiones y depositar un registro con sello temporal antes del torneo confirmatorio. El documento local no constituye ese registro público.

Se conserva la ruta editorial del proyecto y la distinción respecto a los dos preprints. La contribución propuesta es la pregunta de compatibilidad entre modelos con procedencia y controles explícitos, no afirmar que este sea el primer torneo de estrategias LLM. Cualquier presentación de los resultados deberá declarar las exclusiones, correcciones locales, asistencia de IA y límites del corpus.
