# Piloto Modal completado — 2026-09-27

**31/31 trayectorias completas coinciden exactamente con el patrón Windows.** Se compararon huellas SHA-256 de las 1.000 parejas de acciones por partida, no solo puntuaciones finales. Incluye cuatro interpretaciones alternativas y sus versiones principales. Es equivalencia dirigida de este diagnóstico, no garantía de equivalencia de todos los encuentros.

- Workspace: `unimayor-evollm`.
- Aplicación exitosa: `ap-ACYi5haBJGVNdgiwpYJmzH`, https://modal.com/apps/unimayor-evollm/main/ap-ACYi5haBJGVNdgiwpYJmzH .
- Entorno remoto: Python 3.12.14, Axelrod 4.14.0, Linux x86_64/glibc 2.36; imagen con dependencias fijadas y PyTorch CPU 2.14.0+cpu.
- Tiempo medido por el diagnóstico: 5,9848 segundos, incluidos carga del campo y encuentros; excluye construcción de imagen, arranque/importación previa y transferencia. Ciclo visible de la app: 08:41:03–08:42:37, hora Colombia. No extrapolar estas 31 partidas seleccionadas como tiempo fiable del torneo completo.
- Resultado local: `validation/modal_pilot_remote_v1.json`; patrón conservado en `validation/modal_pilot_local_v1.json`.
- Persistencia confirmada mediante listado del volumen `evollm-phase3-diagnostics-v1`: resultado `291d351579d61b011bfe3802ee1995adcc35113172fe94f12576217c402dfc14.json`. También aparece un archivo temporal; no se usa como evidencia ni checkpoint completo.
- Huella del inventario subido: `291d351579d61b011bfe3802ee1995adcc35113172fe94f12576217c402dfc14`. Lista autorizada: 595 archivos científicos, 20.395.288 bytes; excluye credenciales y respuestas de API. El archivo del lanzador también se transmite como código de ejecución del piloto.

La aplicación exitosa quedó **stopped, 0 tasks**, comprobado con la API. El primer intento creó `ap-tCdEB2WDwmG96jAZwxQ2GH` y falló en la consola Windows al imprimir Unicode, antes de crear tareas; fue detenido explícitamente y también figura stopped, 0 tasks. Usar `PYTHONUTF8=1` en posteriores comandos Modal. No hay trabajos del piloto activos y no se debe repetirlo.

## Presupuesto y autorización

El usuario autorizó expresamente el destino, los 595 archivos y el piloto dentro de los US$30 disponibles. La captura mostró consumo cero, créditos US$30 y límite de uso guardado US$30. **No confirmó un límite de cargos personalizado en cero**: se registró el cero efectivo predeterminado documentado por Modal (límite de uso menos créditos), sin atribuir una configuración no observada. Véase `inputs/modal_billing_verified_v1.json`.

La primera revisión automática rechazó el envío; tras recibir la autorización específica, el lanzamiento fue aprobado. No se amplió el presupuesto, no se compraron créditos ni se modificó el plan. **El coste facturado y saldo posterior aún no están verificados**; la ejecución y la construcción de imagen pueden consumir créditos. El tiempo de partidas no permite por sí solo calcular la factura. Revisar Usage & Billing antes de un lote mayor. No hubo llamadas de generación a OpenAI ni partidas confirmatorias.

## Siguiente paso

Implementar y probar la reutilización exacta de encuentros y la distribución por lotes para los 16 escenarios, con trazabilidad, reanudación, verificación de integridad y control acumulado del presupuesto. El objetivo calculado es 166.172 encuentros únicos; aún no está implementado. Después consolidar/congelar el protocolo y obtener registro temporal público antes del torneo confirmatorio. Preservar el adaptador, fuentes y manifiestos congelados.
