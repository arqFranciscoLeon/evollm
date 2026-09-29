# Auditoría de procedencia de prosa

Fecha: 2026-09-13. Alcance: cierre de la búsqueda local disponible; no certifica ausencia de originales en respaldos externos. No se generó texto ni se llamó a modelos.

## Resultado

Se mantiene la procedencia documental de los 18 textos archivados, con archivo, commit de origen, hash de biblioteca y huella del texto. No se recuperó la parte faltante. La causa individual del corte sigue desconocida.

El detalle verificable por estrategia está en [provenance_audit.json](inputs/provenance_audit.json); el historial de versiones examinadas está en [prose_recovery.json](inputs/prose_recovery.json). Las huellas de prosa normalizada de este informe y las del manifest emplean normalizaciones distintas, se identifican por separado y no son intercambiables.

| Modelo / actitud | Casos | Clases |
|---|---:|---|
| Gemini 2.5 Flash / Aggressive | 2 | 6, 24 |
| Gemini 3.1 Pro / Aggressive | 16 | 1, 3, 5, 7, 8, 9, 11, 13, 15, 16, 17, 18, 19, 21, 22, 23 |

Son 18 casos identificados por la inspección previa, no una estimación exhaustiva de toda ambigüedad semántica del corpus. Aggressive_9 de Gemini Pro interrumpe una explicación posterior a las reglas; los otros 17 interrumpen una oración o regla. Esto no significa que los 17 sean necesariamente imposibles de implementar: corresponde revisarlo individualmente sin consultar el código histórico para rellenar huecos.

## Evidencia del proceso

- En `0faabb18`, el formateador de `src/evollm/create_strategies.py:191` usa `textwrap.wrap(text, width=width)`, sin `max_lines` ni corte explícito de longitud. En `1f28a2ca`, la misma operación está en la línea 223. La prueba de los 18 textos con cada función preservó todos los caracteres no blancos: 36/36. Es una comprobación del formateador examinado, no del servicio remoto ni de todo código local no versionado.
- En `1f28a2ca`, `src/evollm/llm_clients.py:316` configura `max_output_tokens=4096`; la línea 328 devuelve `response.text`. El camino revisado no conserva la respuesta estructurada, motivo de terminación ni uso de tokens por solicitud. El límite hace plausible un corte durante la generación, pero no prueba que ocurriera en estos casos. No se atribuye el problema al presupuesto de razonamiento sin metadatos.
- En `0faabb18`, el generador abre `create_strategies.log` con `filemode="w"` (línea 18); en `1f28a2ca` usa `FileHandler(..., mode="w")` (línea 16). Una ejecución posterior puede reemplazar el registro anterior. Esto acredita la posibilidad de pérdida de evidencia; no demuestra qué ejecución sobrescribió qué archivo.
- Las bibliotecas Gemini ya aparecen incorporadas en `0faabb18`, pero ese commit no contiene `llm_clients.py` y su generador versionado no implementa el cliente Google. El cliente aparece en el commit posterior examinado. Por tanto, el commit de incorporación de una biblioteca no identifica el código exacto que la generó ni su fecha de ejecución.

## Búsqueda complementaria

Se examinaron 75 archivos `.log`, `.jsonl` y JSON con `response` en el nombre, bajo `D:/evollm` y `D:/clo-author`, incluidas las copias de trabajo y los registros de regeneración del erratum. No hubo errores de lectura en esa ejecución. No se hallaron coincidencias del prefijo normalizado de 160 caracteres de ninguno de los 18 textos. Esto no descarta registros con otro formato, texto escapado o nombres no cubiertos.

La búsqueda no leyó credenciales ni exportó cuerpos de logs: el informe conserva rutas, tamaños, hashes y conteos de coincidencias. El código documenta las carpetas excluidas. No se inspeccionaron cuentas remotas ni archivos personales de conversación.

## Consecuencia metodológica

Los 18 casos se concentran en un solo estrato de actitud. Excluirlos del campo de 600 agentes dejaría 582: Flash con 23 agresivos y Pro con 9, frente a 25 en los otros estratos. No corresponde aplicar sin cambios el análisis balanceado ni describir la exclusión como aleatoria.

La validación anterior cubrió las 600 estrategias Default de los ocho modelos, no 600 estrategias occidentales: 300 son occidentales y 300 chinas. Verificó ejecución, no fidelidad semántica entre prosa y código.

Se puede continuar la revisión semántica y la preparación editorial sin recuperar los fragmentos. La [enmienda propuesta](AMENDMENT_PROSE_v0.1.md) delimita los análisis que permitiría el corpus histórico. El protocolo de conversor común v0.2 permanece sin congelar; este informe no lo sustituye automáticamente.
