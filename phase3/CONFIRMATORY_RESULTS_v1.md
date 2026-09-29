# Resultados confirmatorios de la Fase 3

Este informe presenta el análisis de la matriz completa ejecutada después del registro público. La inferencia se limita a las 572 identidades archivadas y a sus implementaciones verificadas. Las pruebas diagnósticas previas no se incorporaron.

- Registro: https://osf.io/2nzdh/overview; commit congelado `18cb41744f3f1e66fe711aad09697980476c2498`.
- Integridad: 166,172 encuentros computacionales para 2,622,048 resultados lógicos en 16 escenarios; 665/665 recibos válidos, cero errores.
- H7 primaria (máscara 0): diferencia 0.00534899 (0.5349 puntos porcentuales), prueba unilateral por permutaciones p=0.00010 con 10.000 permutaciones; α=0,05.
- Intervalo de referencia nula 95 % (no es IC del efecto): [-0.00107303, 0.00117528].

## Contraste principal por modelo y par de actitudes

| Par de actitudes | Diferencia H7 |
|---|---:|
| Aggressive/Aggressive | 0.01896818 |
| Aggressive/Cooperative | 0.00484744 |
| Aggressive/Neutral | 0.00690666 |
| Cooperative/Cooperative | 0.00093209 |
| Cooperative/Neutral | 0.00004346 |
| Neutral/Neutral | 0.00039613 |

## Sensibilidad a las 16 interpretaciones

| Máscara | H7 descriptiva | Diferencia frente a máscara 0 |
|---:|---:|---:|
| 0 | 0.00534899 | +0.00000000 |
| 1 | 0.00534830 | -0.00000069 |
| 2 | 0.00534838 | -0.00000061 |
| 3 | 0.00534769 | -0.00000130 |
| 4 | 0.00534405 | -0.00000495 |
| 5 | 0.00534335 | -0.00000564 |
| 6 | 0.00534344 | -0.00000556 |
| 7 | 0.00534274 | -0.00000625 |
| 8 | 0.00534908 | +0.00000009 |
| 9 | 0.00534839 | -0.00000060 |
| 10 | 0.00534847 | -0.00000052 |
| 11 | 0.00534778 | -0.00000121 |
| 12 | 0.00534414 | -0.00000485 |
| 13 | 0.00534344 | -0.00000555 |
| 14 | 0.00534353 | -0.00000546 |
| 15 | 0.00534283 | -0.00000616 |

Rango de efectos: [0.00534274, 0.00534908]. No es un intervalo de confianza; no se calcularon p-valores secundarios.

## Sensibilidades prespecificadas

- Ponderación inversa por multiplicidad de AST: diferencia 0.01019786 (1.0198 pp); sin prueba adicional.
- Límites algebraicos para las 28 identidades excluidas: [-0.08850334, 0.08563515]; no son imputaciones ni intervalo de confianza.
- El archivo JSON incluye los 24 estratos modelo×actitud, autoparejas por separado y las cuatro mezclas contrafactuales de actitudes, además de huellas de matrices y recibos.

## Trazabilidad

- Inventario ordenado de huellas de los 665 recibos: `d7097876abade5cd4365829a5ce1ae11f65dcbee2829ad0c3079a494d4cbd375`.
- Salida JSON completa: `validation/confirmatory_analysis_v1.json`.
- El torneo completó 16 escenarios en un calendario con reutilización exacta por identidad, fuentes y contexto. Los resultados lógicos reconstruyen el calendario completo; no se multiplicaron observaciones de una misma partida compartida entre escenarios.
