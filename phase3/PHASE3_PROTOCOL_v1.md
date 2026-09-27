# Fase 3 de EvoLLM: protocolo del torneo mixto y plan de análisis

Versión consolidada para registro, 27 de septiembre de 2026. Este documento reúne las decisiones posteriores a `DESIGN_v0.3_DRAFT.md`; no modifica retroactivamente los borradores v0.1–v0.3. **Estado: protocolo local completo, todavía sin registro público y sin autorización para ejecutar el calendario confirmatorio.**

## 1. Pregunta, alcance y registro de lo ya observado

Se evaluará si las estrategias atribuidas al mismo modelo exhiben mayor cooperación mutua entre sí que con estrategias de otros modelos, después de equilibrar las comparaciones por actitud. La unidad de agrupación primaria es el **modelo generador**: ocho modelos de siete laboratorios; los dos modelos de Google son grupos distintos. La inferencia queda condicionada al conjunto elegible de descripciones archivadas y a su conversión común a código. Las estrategias no reciben el nombre del rival.

Las descripciones y el código de las estrategias ya existían antes de este registro. También se ejecutaron pruebas de fidelidad, calibraciones y partidas diagnósticas con estrategias reales: entre ellas, 31 encuentros de equivalencia Windows/Linux y una prueba de 11 encuentros del motor de reutilización en Modal. Esos encuentros se eligieron para comprobar semántica, portabilidad, tiempos y recuperación; no constituyen la matriz completa, no se incorporarán como comprobantes confirmatorios y no se usarán para escoger una hipótesis, un escenario favorable ni un criterio de parada. No se ha ejecutado ninguno de los 665 lotes del calendario confirmatorio ni se ha calculado H7 sobre una matriz completa del campo. En consecuencia, el registro propuesto es anterior a la **ejecución y el análisis confirmatorios**, pero posterior a diagnósticos explícitamente declarados.

El estudio principal se limita a la condición `Default`, sin ruido. `Prose` y `Refine` son posibles exploraciones posteriores, sujetas a otro plan operativo; su ejecución no dependerá del valor p de H7. Las comparaciones con los dos preprints existentes serán descriptivas porque sus procesos de generación y conversión no son idénticos. H8 del borrador histórico deja de ser confirmatoria; H9, retroalimentación y Torneo 2 requieren un diseño separado con control contemporáneo sin retroalimentación.

## 2. Campo, procedencia y exclusiones

La autoridad del campo principal es `validation/uniform_derived_candidates_v1.json`, SHA-256 `d5725c7a63125a0cbdee1ddc24e4d2731dc60f6ad0734d3c670d5b23f9181062`. Contiene 572 identidades únicas: 172 agresivas, 200 cooperativas y 200 neutrales. Por modelo, los tamaños son Sonnet 75, DeepSeek 74, Gemini Flash 73, Gemini Pro 59, GLM 75, Kimi 74, GPT 67 y Qwen 75. Las 28 ausencias respecto del panel originalmente previsto de 600 pertenecen a la actitud agresiva; sus reglas faltantes no se completarán mediante conjeturas ni a partir de implementaciones históricas.

Las 572 respuestas fueron producidas en la tanda de conversión común con el snapshot servido `gpt-5.4-mini-2026-03-17`. El campo principal conserva 562 respuestas originales y diez correcciones locales de fidelidad documentadas. Esas correcciones no se presentarán como aciertos del conversor. Cada identidad del manifiesto señala la ruta y la huella de su fuente; las cuatro alternativas de interpretación tienen fuentes y huellas separadas. El adaptador científico es `uniform_semantics_v3b.py`, SHA-256 `3e9bdfdc4f918759dc9d7642a20c90ec8b92e8b3b60de1832d2548ea74e3963b`.

## 3. Diseño de las partidas y calendario

Cada par no ordenado de identidades se enfrentará una vez durante 1.000 rondas del dilema del prisionero iterado, con pagos T=5, R=3, P=1, S=0 y ruido cero. Se incluyen las 572 autoparejas para los resúmenes separados, aunque se excluyen de H7. Hay 163.306 parejas distintas y 163.878 encuentros por escenario. Una sola repetición fue fijada antes de la ejecución confirmatoria: la revisión estática y las comprobaciones de trayectorias no detectaron aleatoriedad de ejecución en las 576 fuentes seleccionadas; repetir estrategias deterministas sin ruido no crearía observaciones independientes. Esta justificación no convierte las partidas en muestras de una población de todas las posibles respuestas del modelo.

La semilla base es `20260913`. `runtime.seed_for(20260913, id_i, id_j, 0)` utiliza las dos identidades completas en orden canónico; se conserva entre escenarios. Cada encuentro usa instancias nuevas de ambas estrategias, sin transferir estado. Se registran CC, CD, DC, DD, pagos por asiento y huellas del contexto y del resultado. Un error de carga, acción inválida, excepción o discrepancia de integridad detiene el lote; nunca se reemplaza por D ni se omite silenciosamente una partida.

Las cuatro alternativas de interpretación se enumeran en este orden de bits: Gemini Pro Aggressive_12, Gemini Pro Aggressive_14, Kimi Aggressive_25 y GLM Aggressive_20. Los 16 valores de máscara 0–15 definen todas las combinaciones; el escenario 0 es el campo principal. Cada máscara mantiene exactamente las mismas 572 identidades. Las reglas alternativas y su procedencia constan en `inputs/sensitivity_plan_v1.json`, SHA-256 `361d3ade33783e972c8f0fcfe99d285e230e02a696ce0f44a1d9a5fb3154afc7`.

El plan `reuse_plan_v1` fija 665 lotes: 664 de 250 encuentros y uno de 172. La unión de los 16 escenarios exige 166.172 encuentros computacionalmente distintos para reconstruir 2.622.048 resultados lógicos, exactamente 163.878 por máscara. La reutilización solo ocurre cuando coinciden las dos identidades, las dos huellas de fuente, semilla y contexto; una misma plantilla en identidades distintas no fusiona encuentros. Huella canónica del contexto: `3811e2f65857b46003a48ddedbc0f625c1a9e573207987787f7a5f78b01d1bfd`; SHA-256 del archivo `reuse_plan_v1/manifest.json`: `2dbcfc56965bd025ca2f4eb9ca2351099f5fd34101fbbd7af82fee9a43bb3ba6`. El manifiesto enumera la huella y el tamaño de cada lote. Se exige cobertura completa, sin duplicados, antes de exportar cualquier matriz.

## 4. Hipótesis y análisis primario

**H7, direccional:** la cooperación mutua promedio, ajustada por actitud, es mayor entre estrategias del mismo modelo que entre estrategias de modelos distintos. Para cada par i,j, `C_ij = CC_ij/1000`; la matriz es simétrica y la diagonal no entra en el contraste. Sea `G_ma` el grupo de identidades de modelo m y actitud a, y `μ(ma,kb)` la media de `C_ij` entre esas celdas, con i=j excluido. El denominador es `n_ma(n_ma−1)` en una celda consigo misma y `n_ma n_kb` entre celdas distintas.

Para cada modelo m y cada uno de los seis pares no ordenados de actitudes (a,b):

```text
W(m,a,b) = μ(ma,mb)
B(m,a,b) = (1/7) Σ[k≠m] {μ(ma,kb)+μ(mb,ka)}/2
Δ(m,a,b) = W(m,a,b) − B(m,a,b)
T_H7 = (1/48) Σ[m,a≤b] Δ(m,a,b)
```

Los ocho modelos y los seis pares de actitudes reciben pesos iguales; cada rival entre modelos recibe 1/7. Esta estandarización difiere del promedio bruto de las 163.306 parejas y deja visible el menor soporte de la celda agresiva de Gemini Pro (n=9). Se informarán `T_H7`, `100×T_H7` en puntos porcentuales, los seis contrastes por estrato y los tamaños de las 24 celdas.

La única prueba confirmatoria usa 10.000 permutaciones de etiquetas de modelo **a nivel de estrategia y dentro de cada actitud**, semilla `20260913`. Cada permutación aplica la etiqueta conjunta a fila y columna y preserva las 24 cuotas observadas. Se recalcula el mismo estadístico. El valor p unilateral es `(1 + número de T_perm ≥ T_obs) / 10001`; el código usa una tolerancia numérica de `1e−12` al comparar flotantes. Se fija α=0,05 para la decisión direccional, sin análisis interino ni parada por significación. El intervalo entre los cuantiles 2,5 % y 97,5 % de la distribución permutada se etiquetará como **referencia nula**, nunca como intervalo de confianza del efecto. No se calculará un bootstrap que trate parejas con estrategias compartidas como observaciones independientes. El script primario es `analyze_phase3.py`, SHA-256 `36f0d0e049306f7f5fb13bf8172fb01e9c79b2da2265dc0f28c60e039f6f37d2`.

La matriz principal debe estar completa y verificarse antes de calcular H7. Si un encuentro sigue irrecuperable, no se recalculará H7 con denominadores de casos disponibles; se declarará el análisis confirmatorio incompleto y se publicarán el motivo y el alcance. Cualquier corrección posterior de fuente, adaptador o análisis requerirá una enmienda fechada que distinga claramente el plan original de la nueva versión; las partidas afectadas se invalidarán y se repetirán bajo el contexto correspondiente.

## 5. Análisis secundarios prespecificados

Se informarán pagos y cooperación por modelo y actitud, autoparejas aparte, y mezclas contrafactuales de actitudes: (1/3,1/3,1/3) y tres mezclas (2/3,1/6,1/6). Son resúmenes ponderados de los mismos encuentros, no nuevas poblaciones observadas ni evidencia de estabilidad evolutiva.

La sensibilidad a código duplicado mantiene las 572 identidades y calcula la huella SHA-256 de `ast.dump(ast.parse(source), include_attributes=False)`. Cada identidad recibe peso inverso a la multiplicidad de su grupo AST dentro de su propia celda modelo×actitud; cada pareja recibe el producto de ambos pesos, se excluye i=j y se normaliza por la masa admisible. Se recalcula el mismo contraste de H7 sin otro valor p. El procedimiento distingue identidad sintáctica de equivalencia conductual.

La sensibilidad a las 28 exclusiones mantiene los encuentros observados de 572 identidades y acota cada encuentro desconocido de las 28 faltantes en [0,1], usando el panel original de 25 identidades por cada una de las 24 celdas. El límite inferior asigna cero a términos desconocidos dentro de modelo y uno a términos desconocidos entre modelos; el superior invierte esas asignaciones. Son cotas algebraicas conservadoras, no imputaciones de estrategias ni intervalos de confianza; se informará si cruzan cero.

Los 16 escenarios de interpretación se analizarán y reportarán **todos**, incluida su diferencia frente al escenario 0 y el mínimo/máximo. Las variantes individuales, las dos ventanas Pro conjuntamente en máscara 3 y las cuatro en máscara 15 no se elegirán por su dirección o significación. Ese rango expresa sensibilidad a interpretación y no un intervalo de confianza. Las sensibilidades son descriptivas, sin pruebas de significación adicionales. La implementación de duplicados y exclusiones es `sensitivity_analysis_v1.py`, SHA-256 `4392ed8755e1bd2054ec7d4c88acaadc8a15f49cf2c27b6ac05f1b7756b8d833`.

## 6. Integridad, recursos y reglas operativas

El ejecutor rechaza un lote cuyo contexto, clave de pareja, fuente, semilla o asignación a escenarios difiera de la versión congelada. Los comprobantes se escriben de forma atómica tras cada partida y se validan antes de reanudar; un error registrado bloquea la recuperación automática. El coordinador local asigna un solo propietario a cada archivo de lote. La prueba diagnóstica en Modal confirmó una secuencia de 2 resultados, reanudación de 9 y reapertura con 0 nuevos, y equivalencia exacta de los 11 resultados entre Windows y Linux. No certifica ejecución simultánea entre varios contenedores ni facturación exactamente una vez tras una caída antes del checkpoint.

El límite económico autorizado es US$30 en créditos disponibles del workspace Modal `unimayor-evollm`, sin recarga ni cargos netos adicionales. El uso se comprobará entre olas acotadas; una insuficiencia de crédito suspende la ejecución por razones operativas, sin consultar H7 ni alterar el calendario. El diagnóstico de 11 encuentros consumió recursos atribuidos por US$0,00065882 y el resumen mensual posterior mostró US$0 facturado; ese pequeño diagnóstico no garantiza el coste de 166.172 encuentros. No habrá llamadas a los modelos generadores ni a la API de conversión durante el torneo.

## 7. Separación entre registro, ejecución y reporte

Antes de la primera partida confirmatoria se fijarán en un commit de Git el protocolo, configuración, código de ejecución y análisis, manifiestos de fuentes y plan de 665 lotes. El registro público fechará ese commit y las huellas del campo, contexto y manifiesto. Un archivo de registro local contendrá la URL pública y la huella del contexto, que el ejecutor exige antes de trabajar. Ningún diagnóstico previo se incorporará al conjunto confirmatorio. El registro expondrá que la selección y las correcciones se realizaron sobre un corpus preexistente y que hubo diagnósticos de partidas antes del registro.

Después se ejecutarán los lotes pendientes por olas limitadas, se verificará la cobertura completa de las 16 matrices y se realizará **una** prueba H7 en el escenario principal. Se presentarán también todos los resultados secundarios especificados, las exclusiones y correcciones de fidelidad, la asistencia de IA en el proceso de conversión y las limitaciones de inferencia. Un resultado nulo no se reinterpretará como demostración de ausencia de relación entre modelo y conducta.
