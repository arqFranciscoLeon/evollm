# ACTA DEL TRIBUNAL — PHASE3_PREREG.md v0.1

**Documento:** pre-registro de la Fase 3 (torneo mixto estilo Axelrod, 8 modelos, dos rondas).
**Fecha:** 2026-08-10 · **Estado del documento:** borrador NO ejecutado, 0 datos recogidos.
**Calibración:** acta del Paper 2 (`D:\clo-author\paper2\TRIBUNAL_paper2_2026-06-16.md`, 72/100).

> **Nota de adaptación de dominio.** El documento no es una propuesta de investigación-creación sino un **pre-registro empírico de ciencias de la computación**. Se sustituyen los sillones temáticos y el Anexo A (I+C) por sus equivalentes de arbitraje tipo AAMAS/ACM, y se re-mapea la rúbrica D1–D8, igual que en el tribunal del Paper 2.

| Sillón | Rol adaptado |
|---|---|
| **S1** | Referee de Estadística y Diseño Experimental |
| **S2** | Experto en Teoría de Juegos Evolutiva / torneos IPD |
| **S3** | Experto empírico en LLMs / validez de constructo |
| **S4** | Evaluador de factibilidad y venue (recursos, ética, forma) |
| **S5** | Experto en ecosistema de modelos / validez ecológica |
| **S6** | Abogado del Diablo (coherencia transversal) |
| **P** | Presidente |

---

## Veredicto: **63.5 / 100 — Ajustes mayores, re-evaluar nueva versión**

El diseño es ambicioso y la pregunta es buena: nadie ha puesto estrategias escritas por ocho modelos frontera a competir entre sí, y la réplica de la estructura de los dos torneos de Axelrod es una idea con filo. El pre-registro tiene virtudes reales —la compuerta de validación del §3, la interpretación del nulo declarada por adelantado en H7, los guardarraíles explícitos.

Pero **tres de sus decisiones lo harían producir números que no significan lo que el documento dice que significan**, y una cuarta hace que la unidad de análisis no exista tal como está definida. La nota es dura a propósito: son errores que hoy cuestan una tarde de reescritura y que después de gastar el cómputo costarían la fase entera. Ese es exactamente el trabajo de un pre-registro.

### Desglose por dimensión

| Dim. | Descripción | Peso | Nota | Resp. |
|---|---|---|---|---|
| D1 | Pertinencia y planteamiento | 15 | 12.5 | S2,S5 |
| D2 | Marco teórico y estado del arte | 10 | 6.0 | S2 |
| D3 | Coherencia metodológica (diseño, controles, guardarraíles) | 20 | 12.0 | S1,S3 |
| D4 | Operacionalización y unidad de análisis | 10 | 5.5 | S3 |
| D5 | Validez de las inferencias planeadas | 15 | 8.0 | S1 |
| D6 | Factibilidad y reproducibilidad | 10 | 5.5 | S4 |
| D7 | Honestidad científica y ética | 10 | 7.5 | S4,S5 |
| D8 | Completitud del pre-registro | 10 | 6.5 | S4 |
| **Total** | | **100** | **63.5** | P |

---

## Hallazgos por sillón

### S1 — Estadística y Diseño Experimental

- **🔴 C1. H9 no tiene grupo de control, y sin él no mide retroalimentación.** El Torneo 2 se compara contra el Torneo 1 y toda diferencia se atribuye al informe. Pero una segunda extracción del mismo modelo con el mismo prompt **ya difiere de la primera** por temperatura 0.7 y estocasticidad del generador; el Paper 2 documentó que dos clases regeneradas bajo protocolo idéntico salieron distintas. Sin un brazo de control, «divergencia tras la retroalimentación» y «variabilidad de muestreo de la generación» son indistinguibles. *Corrección:* añadir un **brazo sin retroalimentación** — cada laboratorio regenera N estrategias con el prompt original y sin informe — y definir el efecto como la diferencia entre el brazo con informe y el brazo sin informe, no entre T2 y T1. Si el presupuesto no da para el brazo completo, hacerlo sobre un subconjunto (p. ej. 25 estrategias por laboratorio) y declarar la potencia resultante. **Sin este brazo, H9 no es publicable y no debe correrse.**
- **🔴 C2. H8 correlaciona P_A de un código con el desempeño de otro código.** El §3 re-convierte las librerías occidentales con GPT-5.4 Mini, de modo que las estrategias que jugarán el torneo **no son** las que produjeron los P_A publicados en la Fase 1. H8, tal como está, empareja el P_A del código viejo con el pago del código nuevo. *Corrección:* tres salidas, en orden de preferencia: (a) restringir H8 a los 4 laboratorios chinos, cuyo P_A sí proviene del mismo pipeline de converter fijo, y reconocer n=4 como descriptivo; (b) correr Moran sobre las librerías occidentales re-convertidas —lo que contradice el §1 y devuelve el coste que la fase quería evitar—; (c) retirar H8 del pre-registro y dejarla como pregunta exploratoria. **Recomendación del sillón: (c), con (a) reportado como descriptivo.**
- **🔴 C3. La diagonal de la matriz infla H7 mecánicamente.** En un all-play-all de la librería axelrod cada jugador se enfrenta también **a sí mismo**, y una estrategia determinista contra su copia exacta coordina perfectamente. Todas esas celdas son «mismo laboratorio» por definición. H7 mediría, en parte, un artefacto. *Corrección:* excluir la diagonal explícitamente del cómputo de H7 y decirlo en el pre-registro. Reportar aparte la cooperación en auto-emparejamiento, que es interesante pero es otra cosa.
- **🟡 I1. La unidad de permutación no está especificada.** «Permutación sobre las etiquetas de laboratorio» admite dos implementaciones con propiedades muy distintas: permutar la etiqueta **por celda** (incorrecto, rompe la estructura de dependencia: cada estrategia aparece en 600 celdas) o **por jugador** (correcto). *Corrección:* fijar por escrito «se permuta la etiqueta de laboratorio a nivel de jugador, arrastrando su fila y columna completas».
- **🟡 I2. H9 compara varianzas entre grupos sobre 8 puntos.** Un bootstrap sobre 8 observaciones da intervalos tan anchos que casi cualquier resultado será compatible con el nulo. *Corrección:* declarar la potencia por adelantado, o mover H9 a nivel de estrategia (¿aumenta la dispersión de tasas de cooperación dentro de cada laboratorio?), donde hay 75 observaciones por laboratorio.
- **🟢 M1. La compuerta de validación del §3 y la regla de no descartar estrategias por mal desempeño son buena práctica.** Mantener tal cual.

### S2 — Teoría de Juegos Evolutiva / torneos IPD

- **🔴 C4. El resultado de un round-robin lo decide la composición del campo, y aquí la composición es un artefacto del diseño de prompts.** Es la crítica clásica a los torneos de Axelrod: quién gana depende de contra quién juega. Este campo tendrá 200 estrategias Agresivas de 600 **porque el protocolo obliga a 25 A / 25 C / 25 N por librería**, no porque una ecología lo haya producido. Cualquier afirmación del tipo «las estrategias del laboratorio X ganan» está condicionada a esa mezcla artificial. *Corrección:* (a) declararlo como limitación de primera línea; y (b) añadir el **análisis ecológico de Axelrod (1980b)**: reproducción proporcional al pago, iterada, partiendo del resultado del round-robin. Es barato, no es un proceso de Moran, y es justamente lo que Axelrod hizo en su segundo torneo. Convierte «quién ganó esta mezcla» en «qué mezcla es estable», que es la pregunta interesante.
- **🟡 I3. El estado del arte no aparece.** Un pre-registro de torneo IPD en 2026 tiene que decir qué hace frente a las estrategias de determinante cero (Press & Dyson), frente al trabajo de la librería axelrod-python sobre sensibilidad de los torneos a la composición, y frente a los torneos con agentes LLM ya publicados. *Corrección:* una sección de posicionamiento, aunque sea de media página.
- **🟡 I4. 20 repeticiones y 1000 turnos se heredan sin justificación.** Vienen del pipeline de las fases anteriores. En un campo de 600 jugadores el error de Monte Carlo por celda es lo que determina si H7 puede detectar el efecto. *Corrección:* calcular el error estándar por celda a 20 repeticiones y justificar el número, o subirlo.
- **🟢 M2. La observación de que las estrategias no pueden ver la etiqueta del oponente, y de que por tanto cualquier efecto de endogrupo es compatibilidad conductual y no reconocimiento, es correcta y es el mejor argumento del documento.** Mantener y desarrollarla: es la contribución conceptual.

### S3 — LLMs / Validez de constructo

- **🔴 C5. «Ocho laboratorios» no existen: son ocho modelos de siete laboratorios.** Gemini 2.5 Flash y Gemini 3.1 Pro son ambos de Google. H7 pregunta si las estrategias del mismo laboratorio cooperan más entre sí — con esta lista, el par Gemini es a la vez «mismo laboratorio» y «modelos distintos», y H8 trata ocho puntos como si fueran ocho laboratorios independientes. *Corrección:* decidir **ante hoc** cuál es la unidad: modelo o laboratorio. Si es laboratorio, el par Gemini se colapsa o se declara estructura anidada y se analiza con efectos aleatorios. Si es modelo, hay que reescribir H7 como «mismo modelo» y renunciar al lenguaje de «laboratorio», que es justamente el marco que el Paper 2 estableció. No se puede tener las dos cosas.
- **🟡 I5. «El laboratorio reescribe sus estrategias» atribuye aprendizaje donde hay lectura en contexto.** El modelo que recibe el informe no es la entidad que escribió las estrategias del Torneo 1: es una llamada nueva, sin memoria, que lee un documento. *Corrección:* nombrar el constructo con precisión —«respuesta en contexto a un informe de resultados»— y evitar «aprende», «se adapta», «mejora» en el pre-registro y en el paper. El Paper 1 ya cuidó no antropomorfizar; mantener el estándar.
- **🟡 I6. La prosa archivada como comentario se asume completa, y la Fase 1 demostró que no siempre lo fue.** La re-conversión toma como entrada el bloque de comentarios de cada `.py`. El erratum de Gemini 3.1 Pro nació precisamente de librerías truncadas, y hubo truncamientos a 4096 tokens durante la regeneración. *Corrección:* añadir a la compuerta del §3 una verificación de integridad de la prosa (distribución de longitudes por librería, detección de bloques cortados a media frase) y documentar que la entrada de la re-conversión es la **prosa archivada**, no la respuesta original de la API.
- **🟢 M3. Que la re-conversión no llame a los generadores es la decisión correcta** y evita introducir una segunda fuente de variación en el paso que debería ser puramente de control.

### S4 — Factibilidad, ética y forma

- **🔴 C6. No hay presupuesto ni cronograma, y esta fase se ejecuta sin financiación ni horas.** El §9 dice que la ronda de retroalimentación es «la parte cara y frágil» y no da una sola cifra. La Fase 2 costó $37.96 por 1800 estrategias con modelos chinos baratos; 600 estrategias con Claude, Gemini y GPT pueden costar bastante más, y no hay saldo asignado. *Corrección:* **sonda de coste obligatoria antes de comprometer la ronda 2** — 3 estrategias por modelo, medir coste y latencia reales, extrapolar, y escribir la cifra en el pre-registro junto con el umbral a partir del cual se cancela la ronda 2. La Fase 2 aprendió esta lección dos veces (Kimi K2.6 inviable a $0.140/estrategia; la sonda solo-Default que subestimó prose/refine). No repetirla.
- **🟡 I7. Falta la declaración de uso de IA y el statement de disponibilidad.** Los Papers 1 y 2 los llevan; comprometerlos aquí evita la discusión después.
- **🟡 I8. El script de análisis se promete pero no se nombra.** «Un script commiteado antes de que existan los datos» es la garantía central del pre-registro. *Corrección:* nombrarlo (`analyze_phase3.py`) y commitearlo vacío con las firmas de las funciones de cada test antes de la primera corrida.
- **🟡 I9. No hay fechas.** Un pre-registro sin cronograma no se puede evaluar en factibilidad, y con dedicación ad honorem el cronograma es el riesgo principal.
- **🟢 M4. Los guardarraíles del §8 están bien elegidos**, en particular el que prohíbe regenerar la prosa occidental.

### S5 — Ecosistema de modelos / validez ecológica

- **🔴 C7. La disponibilidad de los ocho identificadores no está verificada, y el diseño se rompe si falta uno.** Gemini 3.1 Pro era `preview`; Kimi K2.6 ya obligó a una sustitución en la Fase 2; los modelos de 2025-2026 llevan más de un año servidos. Si un identificador desaparece **entre el Torneo 1 y el Torneo 2**, la comparación entre rondas queda contaminada de forma irreparable. *Corrección:* (a) verificar los ocho identificadores **antes** de la re-conversión, con una llamada mínima cada uno, y registrar el resultado con fecha; (b) fijar **ante hoc** la regla de sustitución; (c) correr las dos rondas lo más juntas posible en el tiempo y registrar las fechas de cada llamada.
- **🟡 I10. Los dos ecosistemas no son simétricos.** Cuatro laboratorios chinos distintos frente a cuatro modelos de tres compañías occidentales. Cualquier contraste «Oriente vs Occidente» hereda esa asimetría. Declararla.
- **🟡 I11. El acceso chino vía OpenRouter no controla qué backend sirve cada slug.** Ya se declaró como limitación en el Paper 2; aquí importa más, porque una diferencia de cuantización entre las dos rondas se leería como efecto de la retroalimentación.
- **🟢 M5. Que la fase se apoye en prosa ya archivada la vuelve parcialmente inmune al drift**, que es una virtud real del diseño. Decirlo.

### S6 — Abogado del Diablo

1. **El §1 renuncia a Moran por coste, y H8 depende de Moran.** La fase se define por lo que quita y luego pregunta si lo que quitó predice lo que mide. Tras la re-conversión, ni siquiera existe el número del lado occidental. Es la contradicción estructural del documento. *(= C2.)*
2. **La compuerta de fidelidad del §3 es una bomba desactivada con cinta.** Dice que si las librerías re-convertidas se desvían mucho de la Fase 1, eso «es un resultado a divulgar, no una condición de fallo». Pero una desviación grande significa que las afirmaciones cross-provider del Paper 1 —publicado en arXiv— están contaminadas por el converter. El pre-registro no dice qué se hace en ese caso: ni umbral, ni acción, ni quién decide. Convierte un erratum potencial del Paper 1 en una nota al pie del Paper 3. *Corrección:* fijar un umbral y comprometer la acción por adelantado, incluida la posibilidad de una nota en arXiv.
3. **«Retroalimentación idéntica» no es «información idéntica».** El informe es el mismo documento para los ocho, pero cada laboratorio tiene una relación distinta con él: unos leen que ganaron, otros que perdieron. Eso es correcto y deseable —es el experimento— pero el documento lo presenta como si la simetría del texto garantizara la simetría del tratamiento. Redáctalo como lo que es: tratamiento común, posición distinta.
4. **El guardarraíl «no alterar H7-H9 tras ver el Torneo 1» convive con un parámetro libre elegido después de ver el Torneo 1: el propio informe.** Qué se incluye en él —cuántas estrategias top, si se muestran matrices, con qué encuadre— determina el resultado de H9 y hoy se decide después de ver los datos. *Corrección:* **fijar la plantilla exacta del informe ahora**, con campos vacíos que los resultados rellenan mecánicamente, y commitearla junto al pre-registro.

---

## Matriz de trazabilidad priorizada

| ID | Hallazgo | Sillón | Prioridad | v0.1 |
|----|----------|--------|-----------|------|
| C1 | H9 sin brazo de control sin-retroalimentación | S1 | 🔴 | Abierto |
| C2 | H8 correlaciona P_A del código viejo con pagos del nuevo | S1 | 🔴 | Abierto |
| C3 | La diagonal (auto-emparejamiento) infla H7 | S1 | 🔴 | Abierto |
| C4 | El campo de 600 tiene composición artificial (200 agresivas por diseño) | S2 | 🔴 | Abierto |
| C5 | «8 laboratorios» son 8 modelos de 7 laboratorios (Gemini ×2) | S3 | 🔴 | Abierto |
| C6 | Sin presupuesto ni sonda de coste para la ronda 2, sin financiación | S4 | 🔴 | Abierto |
| C7 | Disponibilidad de los 8 identificadores sin verificar; sin regla de sustitución | S5 | 🔴 | Abierto |
| C8 | La plantilla del informe de retroalimentación es un parámetro libre post-hoc | S6 | 🔴 | Abierto |
| I1 | Unidad de permutación sin especificar | S1 | 🟡 | Abierto |
| I2 | H9 sobre 8 puntos: potencia insuficiente | S1 | 🟡 | Abierto |
| I3 | Estado del arte ausente (ZD, sensibilidad de torneos, LLM-IPD) | S2 | 🟡 | Abierto |
| I4 | 20 repeticiones heredadas sin justificar | S2 | 🟡 | Abierto |
| I5 | Lenguaje de aprendizaje donde hay lectura en contexto | S3 | 🟡 | Abierto |
| I6 | Integridad de la prosa archivada no verificada | S3 | 🟡 | Abierto |
| I7 | Falta disclosure de uso de IA y statement de disponibilidad | S4 | 🟡 | Abierto |
| I8 | Script de análisis sin nombrar ni commitear | S4 | 🟡 | Abierto |
| I9 | Sin cronograma | S4 | 🟡 | Abierto |
| I10 | Asimetría entre ecosistemas no declarada | S5 | 🟡 | Abierto |
| I11 | Routing de OpenRouter entre rondas | S5 | 🟡 | Abierto |
| M1–M5 | Buenas prácticas a conservar | varios | 🟢 | — |

---

## Recomendación del Presidente sobre los cinco puntos abiertos

### OPEN-B — ¿Ruido? **NO. Solo condiciones limpias, y por una razón que el tribunal considera dirimente.**

Es la recomendación más firme del acta. La Fase 2 documentó que, bajo ruido, las estrategias chinas lanzan excepciones **en casi cada movimiento**, y que `algorithms.py` las captura y devuelve Defect por defecto. En un torneo de un solo ecosistema eso es ruido parejo. En un torneo **mixto** deja de serlo: si las estrategias de un laboratorio fallan más que las de otro, la condición con ruido no mide disposición estratégica sino **fragilidad del código generado**, y el paper reportaría como agresión lo que es una excepción capturada.

Si el ruido interesa —y debería—, el camino correcto es al revés: medir primero, como resultado de primera clase, la **tasa de excepciones por laboratorio bajo ruido**. Eso es un hallazgo publicable por sí solo y probablemente novedoso. Solo después, y con esa tasa controlada, tiene sentido un torneo ruidoso. Fase 3 limpia; el ruido, pre-registro aparte.

### OPEN-A — ¿Un prompt o tres? **Default como primario pre-registrado; Prose y Refine como secundarios exploratorios.**

El Paper 2 mostró que el estilo de prompt mueve los resultados más que el laboratorio en algunos casos (GLM bajo Prose llegó a 348/500 agresivas). Renunciar a esa variación empobrece el estudio; correr las tres como confirmatorias triplica el cómputo y multiplica las comparaciones sin financiación. La salida es declarar Default como el torneo que sostiene H7, y correr los otros dos como descriptivos si el presupuesto de tiempo lo permite. Lo que no se vale es decidir después cuál se reporta.

### OPEN-C — ¿Se nombra el laboratorio en el informe? **Anonimizar.**

La tesis del estudio es que la estructura de laboratorio es **conductual y no de identidad**; ese es su mejor argumento (M2). Nombrar los laboratorios en el informe de retroalimentación mete identidad justo en la ronda donde se mide la respuesta, y activa lo que el modelo cree saber sobre su propia marca y sobre sus rivales. Anonimizado —«Laboratorio C», «Laboratorio F»— el Torneo 2 mide respuesta a evidencia conductual, que es lo que la hipótesis afirma. La variante con nombres es un experimento distinto y legítimo: pre-regístrese aparte si algún día hay presupuesto.

*Divergencia declarada:* S2 sostiene que anonimizar se aparta de Axelrod, que sí publicó los nombres. El Presidente concede el punto histórico pero mantiene la recomendación: Axelrod tenía participantes humanos con reputación en juego, no modelos con priors de marca inducidos por su entrenamiento.

### OPEN-D — ¿H7 sigue siendo primaria? **Sí, con las tres correcciones de S1 y S3 aplicadas.**

H7 es la única de las tres que interroga algo que el diseño está construido para responder, y su nulo ya tiene lectura declarada por adelantado, lo cual es buena práctica. Pero H7 sin excluir la diagonal (C3) y sin resolver si la unidad es modelo o laboratorio (C5) no es evaluable. Con esas dos correcciones, es una primaria sólida. H8 sale del pre-registro (C2). H9 se queda solo si aparece el brazo de control (C1).

### OPEN-E — ¿Publicar el Torneo 1 solo? **Sí, y más aún: diséñalo como una unidad publicable desde el principio.**

El Torneo 1 no depende de generadores, no gasta API más allá de la re-conversión, no depende de cuotas y es inmune al drift de modelos porque corre sobre prosa archivada. El Torneo 2 depende de las ocho APIs, de cuota Google, de saldo que no existe y de que ocho identificadores sigan servidos. Atar la mitad robusta al destino de la mitad frágil es un error de gestión de riesgo, sobre todo sin horas asignadas. Estructura la Fase 3 como Torneo 1 = artículo; Torneo 2 = extensión pre-registrada que se ejecuta si y solo si la sonda de coste (C6) y la verificación de identificadores (C7) pasan.

---

## Cierre

Ninguno de los ocho hallazgos críticos exige repensar la idea. Cuatro son de especificación (C3, C5, C7, C8), dos son de control experimental (C1, C4), uno retira una hipótesis mal fundada (C2) y uno pide una cifra antes de comprometer dinero que no hay (C6). Todos se resuelven escribiendo, antes de gastar un solo peso de cómputo.

**Nueva versión esperada: v0.2.** El Presidente estima que, con C1–C8 cerrados y las I resueltas, el documento pasa de 63.5 a la banda de 82–86, es decir, listo para ejecutar.
