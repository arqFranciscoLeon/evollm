# Conversión ampliada occidental Default

Fecha: 2026-09-14. Conversión y validación originales terminadas tras autorización explícita del autor.

## Conversión y trazabilidad

Se recibieron 274 respuestas de `gpt-5.4-mini-2026-03-17`, sin reintentos ni respuestas incompletas. El consumo reportado fue 241.684 tokens de entrada, ninguno en caché, y 15.552 de salida. Coste calculado: **US$0,251247**, dentro del techo local autorizado de US$2. Este cálculo no sustituye la factura ni una consulta del saldo. Ejecución UTC: 2026-09-14 05:34:11 a 05:39:37.

El paquete conserva su SHA-256 `70336a5958a379a4dc0eb5e341ecfaa4bbc75603f7d967784a2d2411143b1f22`. No quedan reservas inciertas. Los originales se conservan en `conversion_runs/expanded_v2/001` a `274`. [Recibo consolidado](validation/expanded_conversion_receipt_v2.json).

## Inspección y adaptación del validador

Se inspeccionaron las fuentes antes de ejecutarlas: 274 registros y 77 huellas de código distintas; las copias idénticas se vinculan por hash. La inspección permite ejecutar las funciones para diagnosticarlas y no equivale a aprobar su fidelidad. [Registro](validation/expanded_source_review_v2.json).

Cuatro respuestas usan tres atributos booleanos propios con prefijo `_`: `_opponent_always_defect`, `_always_defect` y `_permanent_defect`. Se permitió expresamente su escritura en el adaptador después de inspeccionarlos; el resto de atributos privados y los del entorno permanecen protegidos. Esta ampliación de compatibilidad no modifica las funciones recibidas ni sus decisiones. Las 43 pruebas de infraestructura pasaron en 25,88 segundos.

## Discrepancias confirmadas por contraejemplo

1. **Sonnet Neutral_11, respuesta 053.** La prosa da prioridad al umbral de más del 55% de defecciones y exige mantener D durante el resto del juego. El código devuelve D por la última defección antes de actualizar el estado permanente. Con historia rival `DCCC`, vuelve a C desde la ronda 3; debería mantener D. Es un error de orden de implementación, no una ausencia de regla en la prosa.
2. **Gemini Pro Aggressive_6, respuesta 156.** La prosa exige D desde la ronda 995 inclusive. El código usa `len(self.history) >= 995`, por lo que comienza en la ronda 996. Tras 994 cooperaciones rivales, devuelve C en la ronda 995. Es un desfase de una ronda en la conversión.

[Contraejemplos reproducidos](validation/expanded_discrepancy_witnesses_v2.json). No se repararon ni se regeneraron las funciones, y no se cambia su pertenencia al corpus por estos resultados.

## Consecuencia metodológica

Antes de admitir las conversiones al torneo debe cerrarse una política explícita para errores demostrables de implementación: conservar originales, separar cualquier versión corregida, justificar cada cambio por la prosa y repetir las comprobaciones afectadas. No debe seleccionarse una versión por su desempeño. Las 26 exclusiones previas por prosa incompleta son una categoría diferente y permanecen documentadas.

También siguen pendientes la sensibilidad obligatoria de ventanas, la auditoría de descripciones chinas y el cierre del protocolo comparativo. Las partidas de validación no son el torneo mixto ni resultados confirmatorios de la investigación.

## Cierre de validación original

**272/274** estrategias pasan los casos semánticos y la ejecución. Las dos discrepancias descritas son las únicas detectadas. Se realizaron 1.125.318 comprobaciones de acción sobre historiales controlados, con 1.003 diferencias concentradas en esos dos programas (999 y 4, respectivamente). Estas comprobaciones comparten prefijos y no son observaciones estadísticamente independientes.

Las **3.014/3.014 partidas diagnósticas**, de 1.000 rondas cada una, terminaron correctamente, incluidas las de los dos programas semánticamente incorrectos. Los **12/12 controles pareados** coinciden en acciones con el piloto en los 19 escenarios; no demuestra equivalencia exhaustiva. [Informe completo](validation/expanded_v2.json).

El campo de 274 programas originales no se declara aprobado. Se continúa con una política explícita de correcciones mínimas en copias separadas y nueva validación de los casos afectados, conservando este resultado original.

## Correcciones locales verificadas

Tras indicar el autor que se continuara, se aplicó la [política de correcciones v1](IMPLEMENTATION_CORRECTIONS_v1.md). Las dos versiones separadas pasaron **8.214/8.214 comprobaciones de acción** y **22/22 partidas de 1.000 rondas**, sin diferencias frente a las reglas esperadas. No hubo nuevas llamadas API. [Validación y diferencias exactas](validation/expanded_corrections_v1.json).

El [manifiesto derivado](validation/western_derived_candidates_v1.json) identifica **272 originales sin cambios y 2 correcciones locales**, con huellas de ambos códigos y de sus informes. Los 274 candidatos derivados pasan las comprobaciones efectuadas; esto no implica equivalencia exhaustiva ni admisión definitiva al torneo. El resultado original sigue siendo 272 aprobados y 2 fallidos, y no debe sobrescribirse al informar la tasa de éxito del conversor.

Siguiente paso: implementar y registrar la sensibilidad obligatoria de ventana completa para Pro Aggressive_12 y Aggressive_14; después, auditar las descripciones chinas y cerrar el protocolo comparativo antes de ejecutar el torneo.
