# Modal: preparación con créditos existentes

Fecha: 2026-09-27. El usuario autorizó usar los US$30 disponibles. No autoriza recargas, cambio a plan de pago ni cargos adicionales. Destino: workspace `unimayor-evollm`. Modal sustituye la propuesta de contratar Hetzner para el siguiente piloto.

## Estado comprobado

- Cliente oficial Modal 1.5.5 instalado en `D:/evollm/.modal-phase3-venv`, separado del entorno científico congelado. No se cambió el perfil activo global ni sus credenciales.
- Lectura autenticada `modal app list --profile unimayor-evollm --json` exitosa, lista vacía. Esto acredita acceso, no saldo ni autorización de facturación de otro workspace.
- La captura del usuario muestra US$30 de créditos y límite de uso US$50. El saldo actual no pudo comprobarse: el navegador integrado requiere inicio de sesión.
- Se pidió confirmar saldo y configurar Usage limit US$30 y Spend limit US$0. La documentación distingue uso bruto antes de créditos y cargos netos después de créditos: https://modal.com/docs/guide/budgets . No se modificó esa configuración ni se creó el archivo de comprobación.
- **Cero trabajos remotos lanzados; cero gasto de cómputo Modal realizado en esta preparación.** No hay procesos remotos que reanudar.

## Piloto listo localmente

`modal_pilot_core_v1.py` selecciona por identidades hasta 32 encuentros; deduplicación produce 31, todos de 1.000 rondas. Incluye las cuatro alternativas, comparadas también en su versión principal. El patrón Windows terminó correctamente y guarda huellas de trayectorias completas en `validation/modal_pilot_local_v1.json`. Son diagnósticos, no datos del torneo confirmatorio.

`build_modal_bundle_v1.py` prepara una lista explícita de 595 archivos científicos (~20,4 MB) en `cloud_bundle_v2`. Excluye credenciales, .git, solicitudes/respuestas de API y documentos ajenos. El inventario contiene huellas de cada archivo. La primera carpeta `cloud_bundle_v1` se conserva como intento de empaquetado anterior, **no usarla para subir**.

Se descubrieron diez rutas Windows en el manifiesto congelado. El paquete v2 usa rutas normalizadas; al iniciar en Linux se crearán alias locales con los nombres literales originales, tras verificar las huellas, para conservar el manifiesto y cargador existentes. La equivalencia Linux sigue pendiente de la ejecución remota.

`modal_pilot_v1.py` define una única función diagnóstica: CPU solicitada y límite 1 núcleo físico, RAM solicitada 1 GiB/límite 2 GiB, timeout 600 segundos, un contenedor y cero reintentos configurados. Imagen Python 3.12.14; dependencias fijadas; PyTorch de índice CPU oficial. La disponibilidad de imagen/ruedas y compatibilidad del entorno Linux no están verificadas todavía. No modificar versiones silenciosamente si falla la construcción.

Resultados exitosos se guardan en el volumen `evollm-phase3-diagnostics-v1` y se comparan con el patrón Windows antes de declarar equivalencia. Un resultado existente con el mismo inventario se recupera sin repetir partidas. El cliente guarda copia local. El programa no ofrece entrada al torneo completo y no llama a OpenAI. La construcción de imagen también puede generar consumo: los límites de función no son un techo contable global.

Tres pruebas locales aprobadas (`validation/modal_pilot_tests_v2.xml`): cobertura/lista de archivos, límite de calendario y rechazo de trayectorias discrepantes. Se conserva el primer informe fallido v1 por trazabilidad de la corrección de rutas.

## Punto exacto para continuar

1. Esperar confirmación real de saldo y límites, o verificarlos en una sesión autenticada. No inventar esa comprobación. Registrar workspace, fecha/evidencia, créditos restantes, usage_limit_usd=30, spend_limit_usd=0 y project_authorized_usd=30 en `inputs/modal_billing_verified_v1.json`. El lanzador se bloquea antes de construir la imagen si falta ese registro.
2. Ejecutar solo el piloto: `D:/evollm/.modal-phase3-venv/Scripts/python.exe -m modal run --profile unimayor-evollm phase3/modal_pilot_v1.py`, desde esta copia de trabajo. No repetir tras un fallo sin revisar su causa y consumo. No usar otro perfil.
3. Confirmar equivalencia de las 31 trayectorias, versiones, resultados persistentes y consumo real. Después implementar/probar reutilización exacta y distribución por lotes, con presupuesto acumulado total dentro de US$30 y sin cargos netos.
4. Consolidar y congelar el protocolo y obtener registro temporal público antes del torneo confirmatorio. La autorización económica no elimina esas dependencias científicas.

No repetir conversiones ni el patrón local ya guardado. El uso de Modal no requiere financiar una startup ni obtener nuevos créditos académicos.
