# Ola confirmatoria de cuatro contenedores: lotes 3–10

El 27 de septiembre de 2026 se ejecutaron los ocho lotes 3–10 del plan congelado en Modal, workspace `unimayor-evollm`, con un máximo de cuatro contenedores simultáneos. App: <https://modal.com/apps/unimayor-evollm/main/ap-YopgVCCiSe7RlWPeBhLbAk>. La consulta posterior confirmó estado `stopped` y cero tareas activas.

Cada lote produjo 250 partidas nuevas, sin errores. Los ocho recibos se descargaron a `validation/modal_confirmatory_batch_0003_receipt.json` hasta `...0010...`. `verify_modal_wave_v1.verify(tuple(range(11)))` validó los once lotes acumulados contra el contexto y calendario congelados: **2.750 partidas distintas, 43.680 resultados lógicos de escenarios, cero errores**. Quedan 654 de 665 lotes y 163.422 partidas distintas. H7 sigue pendiente de la matriz completa.

El reporte de Modal atribuye a esta app **US$0,04101479**. El resumen mensual observado tras esta ola muestra aproximadamente US$0,06 de uso medido, cubierto por créditos, y **US$0 facturado**. La diferencia entre el reporte por app y el resumen mensual obedece a agregación/redondeo y a las otras ejecuciones del mes; no se atribuye el resumen íntegro a esta ola.

El límite de 100 contenedores del workspace es capacidad máxima, no una configuración de este lanzador. Esta ola se limitó a cuatro porque los ocho trabajos comparten un volumen Modal v1 y confirman checkpoints durante las partidas. El siguiente aumento de concurrencia debe repartir escrituras entre volúmenes independientes y verificarse con otra ola acotada. Los 11 recibos actuales permanecen inmutables en la copia local.
