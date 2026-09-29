# Conciliación de resultados anteriores

28 de septiembre de 2026. Recalculado desde los tres snapshots archivados, sin modificar fuentes ni ejecutar nuevas simulaciones. Se verifica su SHA-256 contra la auditoría anterior, cobertura, conteos, denominadores y porcentajes. Los intervalos C−N son aproximaciones normales marginales posteriores, condicionales a bibliotecas fijas.

## phase1

Condiciones: 48; resultados contabilizados: 24000/24000. Pluralidades limpias balanceadas: {'Neutral': 2, 'Cooperative': 10}. Intervalos C−N que incluyen cero: 9/12.

| Biblioteca | A | C | N | Pluralidad | C−N (pp) | IC marginal 95 % (pp) |
|---|---:|---:|---:|---|---:|---|
| anthropic_sonnet46_default_75 | 10 | 243 | 247 | Neutral | -0.80 | [-9.48, 7.88] |
| anthropic_sonnet46_prose_75 | 24 | 241 | 235 | Cooperative | 1.20 | [-7.35, 9.75] |
| anthropic_sonnet46_refine_75 | 115 | 197 | 188 | Cooperative | 1.80 | [-5.89, 9.49] |
| gemini_25_flash_default_75 | 12 | 246 | 242 | Cooperative | 0.80 | [-7.86, 9.46] |
| gemini_25_flash_prose_75 | 118 | 234 | 148 | Cooperative | 17.20 | [9.69, 24.71] |
| gemini_25_flash_refine_75 | 104 | 234 | 162 | Cooperative | 14.40 | [6.70, 22.10] |
| gemini_31_pro_default_75 | 69 | 208 | 223 | Neutral | -3.00 | [-11.13, 5.13] |
| gemini_31_pro_prose_75 | 93 | 216 | 191 | Cooperative | 5.00 | [-2.90, 12.90] |
| gemini_31_pro_refine_75 | 135 | 198 | 167 | Cooperative | 6.20 | [-1.27, 13.67] |
| openai_gpt54mini_default_75 | 8 | 267 | 225 | Cooperative | 8.40 | [-0.26, 17.06] |
| openai_gpt54mini_prose_75 | 61 | 224 | 215 | Cooperative | 1.80 | [-6.41, 10.01] |
| openai_gpt54mini_refine_75 | 19 | 349 | 132 | Cooperative | 43.40 | [35.69, 51.11] |

## phase2

Condiciones: 48; resultados contabilizados: 23865/24000. Pluralidades limpias balanceadas: {'Cooperative': 6, 'Neutral': 6}. Intervalos C−N que incluyen cero: 10/12.

| Biblioteca | A | C | N | Pluralidad | C−N (pp) | IC marginal 95 % (pp) |
|---|---:|---:|---:|---|---:|---|
| deepseek_v4pro_default_75 | 46 | 233 | 221 | Cooperative | 2.40 | [-5.95, 10.75] |
| deepseek_v4pro_prose_75 | 66 | 204 | 230 | Neutral | -5.20 | [-13.35, 2.95] |
| deepseek_v4pro_refine_75 | 78 | 196 | 226 | Neutral | -6.00 | [-14.04, 2.04] |
| glm_51_default_75 | 41 | 245 | 214 | Cooperative | 6.20 | [-2.18, 14.58] |
| glm_51_prose_75 | 103 | 186 | 211 | Neutral | -5.00 | [-12.80, 2.80] |
| glm_51_refine_75 | 113 | 229 | 158 | Cooperative | 14.20 | [6.59, 21.81] |
| kimi_k25_default_75 | 10 | 243 | 247 | Neutral | -0.80 | [-9.48, 7.88] |
| kimi_k25_prose_75 | 92 | 210 | 198 | Cooperative | 2.40 | [-5.52, 10.32] |
| kimi_k25_refine_75 | 67 | 242 | 191 | Cooperative | 10.20 | [2.09, 18.31] |
| qwen3max_default_75 | 5 | 231 | 264 | Neutral | -6.60 | [-15.30, 2.10] |
| qwen3max_prose_75 | 68 | 221 | 211 | Cooperative | 2.00 | [-6.15, 10.15] |
| qwen3max_refine_75 | 59 | 220 | 221 | Neutral | -0.20 | [-8.43, 8.03] |

| Condición | Población A:C:N | n efectivo | Faltantes frente a 500 |
|---|---|---:|---:|
| deepseek_v4pro_default_75_noise | [4, 4, 4] | 441 | 59 |
| deepseek_v4pro_default_75_noise | [8, 2, 2] | 457 | 43 |
| deepseek_v4pro_prose_75_noise | [4, 4, 4] | 499 | 1 |
| deepseek_v4pro_refine_75_noise | [4, 4, 4] | 477 | 23 |
| deepseek_v4pro_refine_75_noise | [8, 2, 2] | 497 | 3 |
| glm_51_refine_75_noise | [4, 4, 4] | 494 | 6 |

## robust

Condiciones: 12; resultados contabilizados: 6000/6000. Pluralidades limpias balanceadas: {'Neutral': 3, 'Tie': 1, 'Cooperative': 8}. Intervalos C−N que incluyen cero: 9/12.

| Biblioteca | A | C | N | Pluralidad | C−N (pp) | IC marginal 95 % (pp) |
|---|---:|---:|---:|---|---:|---|
| deepseek_v4pro_default_75_robust | 64 | 205 | 231 | Neutral | -5.20 | [-13.37, 2.97] |
| deepseek_v4pro_prose_75_robust | 63 | 209 | 228 | Neutral | -3.80 | [-11.99, 4.39] |
| deepseek_v4pro_refine_75_robust | 78 | 209 | 213 | Neutral | -0.80 | [-8.85, 7.25] |
| qwen3max_default_75_robust | 4 | 248 | 248 | Tie | 0.00 | [-8.73, 8.73] |
| qwen3max_prose_75_robust | 77 | 224 | 199 | Cooperative | 5.00 | [-3.05, 13.05] |
| qwen3max_refine_75_robust | 61 | 240 | 199 | Cooperative | 8.20 | [0.02, 16.38] |
| kimi_k25_default_75_robust | 8 | 259 | 233 | Cooperative | 5.20 | [-3.48, 13.88] |
| kimi_k25_prose_75_robust | 87 | 220 | 193 | Cooperative | 5.40 | [-2.55, 13.35] |
| kimi_k25_refine_75_robust | 61 | 255 | 184 | Cooperative | 14.20 | [6.08, 22.32] |
| glm_51_default_75_robust | 50 | 234 | 216 | Cooperative | 3.60 | [-4.71, 11.91] |
| glm_51_prose_75_robust | 105 | 203 | 192 | Cooperative | 2.20 | [-5.59, 9.99] |
| glm_51_refine_75_robust | 112 | 227 | 161 | Cooperative | 13.20 | [5.57, 20.83] |

## H6: phase2

| Comparación | Conteos A (n=500 cada uno) | z | p bilateral | Rechaza Holm |
|---|---|---:|---:|---|
| deepseek_v4pro / qwen3max | [46, 5] | 5.8934 | 3.7833706e-09 | True |
| deepseek_v4pro / kimi_k25 | [46, 10] | 4.9513 | 7.3705324e-07 | True |
| deepseek_v4pro / glm_51 | [46, 41] | 0.5610 | 0.57478686 | False |
| qwen3max / kimi_k25 | [5, 10] | -1.3008 | 0.1933313 | False |
| qwen3max / glm_51 | [5, 41] | -5.4344 | 5.4989624e-08 | True |
| kimi_k25 / glm_51 | [10, 41] | -4.4560 | 8.3509753e-06 | True |

## H6: robust

| Comparación | Conteos A (n=500 cada uno) | z | p bilateral | Rechaza Holm |
|---|---|---:|---:|---|
| deepseek_v4pro / qwen3max | [64, 4] | 7.5368 | 4.8152582e-14 | True |
| deepseek_v4pro / kimi_k25 | [64, 8] | 6.8509 | 7.3385491e-12 | True |
| deepseek_v4pro / glm_51 | [64, 50] | 1.3930 | 0.16361239 | False |
| qwen3max / kimi_k25 | [4, 8] | -1.1617 | 0.24536071 | False |
| qwen3max / glm_51 | [4, 50] | -6.4360 | 1.2267084e-10 | True |
| kimi_k25 / glm_51 | [8, 50] | -5.6821 | 1.3304095e-08 | True |

## Cambios con reconversión parcial

| Biblioteca | Antes | Después |
|---|---|---|
| deepseek_v4pro_default_75 | Cooperative | Neutral |
| glm_51_prose_75 | Neutral | Cooperative |
| kimi_k25_default_75 | Neutral | Cooperative |
| qwen3max_default_75 | Neutral | Tie |
| qwen3max_refine_75 | Neutral | Cooperative |

Son cuatro cambios estrictos C↔N y uno N→empate. La reconversión parcial y una nueva realización Monte Carlo no permiten atribuir aisladamente estos cambios al conversor.

Ver `STUDY_DESIGNS_AND_RECONCILIATION_v1.md` para decisiones editoriales y límites pendientes. Este reporte no verifica las matrices de pagos/ICD ni reconstruye las causas individuales de los faltantes.
