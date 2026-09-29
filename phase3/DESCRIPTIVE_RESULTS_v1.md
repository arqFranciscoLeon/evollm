# Descriptive results for the registered primary scenario

The table below reports every model×attitude cell. For each strategy, mutual cooperation and focal payoff were averaged over its 571 distinct opponents; the cell entries then average those strategy means. Self-play uses the one diagonal encounter for each strategy and is shown separately from the H7 contrast. Payoffs use the registered T=5, R=3, P=1, S=0 game.

| Model identity | Attitude | n | Mutual cooperation vs others (%) | Focal payoff vs others | Self-play cooperation (%) | Self-play payoff |
|---|---|---:|---:|---:|---:|---:|
| anthropic_sonnet46 | Aggressive | 25 | 0.97 | 1.7188 | 0.00 | 1.0000 |
| anthropic_sonnet46 | Cooperative | 25 | 70.42 | 2.5583 | 99.18 | 2.9836 |
| anthropic_sonnet46 | Neutral | 25 | 70.84 | 2.5609 | 99.97 | 2.9994 |
| deepseek_v4pro | Aggressive | 24 | 2.83 | 1.5694 | 14.58 | 1.2915 |
| deepseek_v4pro | Cooperative | 25 | 72.09 | 2.5204 | 99.99 | 2.9998 |
| deepseek_v4pro | Neutral | 25 | 72.15 | 2.5038 | 99.99 | 2.9998 |
| gemini_25_flash | Aggressive | 23 | 2.06 | 1.3061 | 6.53 | 1.1305 |
| gemini_25_flash | Cooperative | 25 | 70.95 | 2.5659 | 100.00 | 3.0000 |
| gemini_25_flash | Neutral | 25 | 70.95 | 2.5659 | 100.00 | 3.0000 |
| gemini_31_pro | Aggressive | 9 | 31.97 | 2.0754 | 59.97 | 2.1993 |
| gemini_31_pro | Cooperative | 25 | 70.90 | 2.5671 | 99.90 | 2.9980 |
| gemini_31_pro | Neutral | 25 | 70.90 | 2.5670 | 99.90 | 2.9981 |
| glm_51 | Aggressive | 25 | 11.70 | 1.6836 | 37.87 | 1.7574 |
| glm_51 | Cooperative | 25 | 71.00 | 2.5621 | 99.97 | 2.9994 |
| glm_51 | Neutral | 25 | 71.05 | 2.5548 | 99.98 | 2.9996 |
| kimi_k25 | Aggressive | 24 | 1.14 | 1.7282 | 4.16 | 1.0833 |
| kimi_k25 | Cooperative | 25 | 70.93 | 2.5662 | 99.97 | 2.9994 |
| kimi_k25 | Neutral | 25 | 70.94 | 2.5661 | 99.98 | 2.9995 |
| openai_gpt54mini | Aggressive | 17 | 0.09 | 1.2252 | 0.00 | 1.0000 |
| openai_gpt54mini | Cooperative | 25 | 70.95 | 2.5659 | 100.00 | 3.0000 |
| openai_gpt54mini | Neutral | 25 | 65.33 | 2.4910 | 92.00 | 2.8400 |
| qwen3max | Aggressive | 25 | 0.00 | 1.1713 | 0.00 | 1.0000 |
| qwen3max | Cooperative | 25 | 70.95 | 2.5659 | 100.00 | 3.0000 |
| qwen3max | Neutral | 25 | 70.95 | 2.5659 | 100.00 | 3.0000 |

## Counterfactual opponent-attitude mixtures

These are reweightings of the same completed encounters. For each focal strategy, the target attitude weight is divided equally among the eight opponent models and then among eligible identities in each model×attitude cell, excluding the focal identity. The table averages the 572 focal strategy values with equal weight. Each tuple is ordered Aggressive, Cooperative, Neutral.

| Mixture | Target attitude weights | Mutual cooperation (%) | Focal payoff |
|---|---|---:|---:|
| Equal thirds | (1/3, 1/3, 1/3) | 49.28 | 2.2200 |
| Aggressive dominant | (2/3, 1/6, 1/6) | 27.81 | 1.8576 |
| Cooperative dominant | (1/6, 2/3, 1/6) | 60.18 | 2.4029 |
| Neutral dominant | (1/6, 1/6, 2/3) | 59.86 | 2.3994 |

The 96 cell-level mixture rows and exact values are preserved in `validation/confirmatory_analysis_v1.json`. These descriptive quantities are not additional hypothesis tests, independent samples, or evolutionary fixation estimates.
