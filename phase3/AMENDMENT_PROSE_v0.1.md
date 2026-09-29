# Enmienda propuesta: corpus archivado y descripciones truncadas

Fecha: 2026-09-13. Estado: propuesta local preparada a solicitud del autor, previa al torneo; no es un prerregistro público ni declara ejecutado un experimento. Complementa [v0.2](DESIGN_v0.2_DRAFT.md), cuya comparación bajo conversor común sigue pendiente.

## Decisión propuesta y alcance

Conservar íntegros los artefactos históricos y sus identidades. La búsqueda local disponible se cierra con 18 fragmentos no recuperados y causa desconocida. Cualquier respaldo posterior se incorpora como nueva evidencia con fecha y hash, sin sustituir silenciosamente el snapshot.

Se recomienda habilitar un estudio descriptivo de compatibilidad entre los 600 programas archivados. Su objeto son esos agentes ejecutables; las diferencias entre modelos incluyen diferencias del proceso de conversión histórico. Este estudio no identifica por separado un efecto del generador, laboratorio, región ni conversor.

El estudio con conversor común mantiene un estatus independiente: las entradas deben aprobar revisión semántica antes de ser presentadas como conversiones fieles. Convertir prosa incompleta exige que el conversor decida reglas ausentes; esos casos no pueden mezclarse como si fueran descripciones completas.

Esta propuesta no redefine retroactivamente H7 confirmatoria. La elección del análisis principal, el protocolo final y su registro fechado siguen pendientes de congelación antes del torneo.

## Inclusión y revisión semántica

1. Preservar las 600 estrategias archivadas para el estudio descriptivo, sujeto a validación estricta de ejecución. No reconstruir la prosa desde esos programas.
2. Revisar las descripciones sin usar ganancias ni resultados de enfrentamientos. Registrar reglas iniciales, reacción al rival, prioridad entre reglas, horizonte final y condiciones no cubiertas.
3. Clasificar cada caso como reglas suficientemente determinadas, reglas incompletas/ambiguas o fallo de extracción. Un final explicativo cortado puede dejar reglas completas; debe justificarse por caso. La ausencia de una marca de truncamiento tampoco certifica completitud.
4. En la reconversión fiel, detener los casos con reglas incompletas; conservar el fallo y su causa. No pedir al modelo que complete o mejore la estrategia. Cualquier interpretación exploratoria se guarda aparte, identificada como tal.
5. No regenerar selectivamente los 18 casos. Un corpus nuevo requiere un diseño homogéneo separado, versiones y fechas explícitas.

## Sensibilidad prespecificada para programas históricos

Reportar el campo completo de 600 y un campo restringido de 582 que elimina las filas y columnas de los 18 casos identificados, incluido el caso con explicación cortada. La lista se fija en `provenance_audit.json`, antes de resultados. Mantener los ocho modelos y los seis estratos de pares de actitud, con igual peso por modelo y estrato; calcular cada media con su número real de pares. No dar igual peso global a todas las celdas porque sobrerrepresentaría los estratos más grandes.

Tras excluir, los agresivos disponibles son 23 para Flash y 9 para Pro; el resto mantiene 25 por modelo/actitud. Se mantienen suficientes pares para las medias dentro de cada grupo. No es necesario descartar cientos de estrategias para igualar tamaños.

Para una referencia por permutación, conservar los tamaños observados de modelo dentro de cada actitud, permutar etiquetas a nivel de estrategia y excluir autoemparejamientos exactos. Se requiere adaptar y probar el validador: `analyze_phase3.py` actualmente exige tamaños iguales y debe seguir rechazando esta entrada hasta implementar la extensión. Las celdas de matriz no son observaciones independientes. La referencia permutacional tampoco elimina el sesgo de selección por truncamiento.

Reportar ambos efectos y su diferencia descriptiva; no seleccionar el conjunto según su p-valor. La exclusión altera a la vez el campo de rivales y la composición de Gemini: una diferencia entre análisis no identifica causalmente el efecto del truncamiento. Un resultado estable solo respalda robustez frente a esta exclusión específica.

## Piloto trazable: preparación inmediata

Se preparó [pilot_selection.json](inputs/pilot_selection.json): 12 entradas Default occidentales, una por modelo y actitud, seleccionadas por orden hash determinista entre las no marcadas en estos 18 casos. La selección no usa comportamiento ni payoffs. Cada entrada mantiene hash de biblioteca y de prosa y está pendiente de revisión semántica. Se adjuntan los 18 identificadores como panel diagnóstico documental, sin convertirlos automáticamente.

Antes de llamadas: completar revisión semántica, fijar conversor y prompt, máximo de salida, política de reintentos y presupuesto acotado. Conservar por solicitud un identificador único, texto exacto y hash, modelo solicitado y devuelto, fecha, configuración, SDK, respuesta completa, motivo de terminación, consumo y errores. No registrar secretos. Escritura por solicitud sin sobrescritura; una respuesta incompleta no se acepta como conversión exitosa.

Después: evaluar fidelidad por casos de historia derivados de las reglas y validar ejecución a horizonte completo. Aprobar el piloto no aprueba automáticamente todas las bibliotecas. No se han realizado llamadas API ni torneos como parte de esta enmienda.

## Consecuencias editoriales

Incorporar la incidencia como límite de trazabilidad de la síntesis de los dos preprints. No atribuir los cortes al proveedor sin metadatos. No concluir que invalidan todos los resultados publicados a partir de este hallazgo; cualquier corrección pública requiere contrastar la afirmación afectada y su evidencia.
