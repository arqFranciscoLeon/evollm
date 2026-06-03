# Extension: Cross-Provider Benchmark with 2025–2026 Frontier Models

This branch (`extension/2025-2026-models`) extends the original Willis et al. (2025)
benchmark to four next-generation LLM models spanning three providers.

**Original paper:** Willis, Du, Leibo & Luck (2025) — [arXiv:2501.16173](https://arxiv.org/abs/2501.16173)  
**Extension paper:** León (2026) — [arXiv:2605.29874](https://arxiv.org/abs/2605.29874)  
**Replication archive:** [10.5281/zenodo.20248615](https://doi.org/10.5281/zenodo.20248615)  
**Author affiliation:** Institución Universitaria Colegio Mayor del Cauca

---

## New Models

| Model | Provider | Predecessor |
|-------|----------|-------------|
| Claude Sonnet 4.6 | Anthropic | Claude 3.5 Sonnet |
| Gemini 2.5 Flash  | Google    | — |
| Gemini 3.1 Pro    | Google    | — |
| GPT-5.4 Mini      | OpenAI    | ChatGPT-4o |

Same protocol as original: 25 strategies × 3 attitudes × 3 prompts (Default, Prose, Refine) = 75 strategies per model.

---

## Bug Fixes Applied

- `moran_process.py`: Fixed random seed generation (`np.iinfo(np.uint32).max` → `2**31 - 1`) to avoid overflow on some platforms.
- `create_strategies.py`: Removed deprecated `ast.Num` and `ast.Str` nodes (Python 3.8+ uses `ast.Constant`); updated default model name.

---

## New Files

### `strategies/`
24 new strategy files — one per model × prompt × noise condition:
- `{model}_{prompt}_75.py` — noiseless strategies
- `{model}_{prompt}_75_noise.py` — noise-aware strategies

### `results/extension_2025_2026/`
- `moran_history.csv` — master log of all Moran runs
- `*_moran.csv` — individual Moran process results (48 conditions)
- `*_matrices.txt` — H2H cooperation and payoff matrices (24 conditions)

### `paper/`
LaTeX source for the extension paper (AAMAS 2027 format).

---

## Key Results Summary

Moran equilibria (% Aggressive / % Cooperative / % Neutral), balanced population (4:4:4), no noise:

| Model | Default | Prose | Refine |
|-------|---------|-------|--------|
| Claude 4.6     | 2/50/48  | 7/55/38  | 21/40/39 |
| Gemini 2.5 Flash | 1/51/48 | 22/54/24 | 25/41/34 |
| Gemini 3.1 Pro | 15/35/50 | 13/36/51 | 15/51/34 |
| GPT-5.4 Mini   | 1/48/51  | 16/44/40 | 1/68/31  |

*Willis et al. reference: ChatGPT-4o Default 14/53/33 · Claude 3.5 Sonnet Default 4/49/47*

---

## Reproducing the Experiments

```bash
# Install dependencies
pip install -e .

# Run Moran process (example)
PYTHONPATH=src python src/evollm/moran_process.py \
    --algo strategies/claude_sonnet46_default_75 \
    --initial_pop 4 4 4 \
    --iterations 100

# Run H2H tournament (example)
PYTHONPATH=src python src/evollm/head_to_head.py \
    --algo strategies/claude_sonnet46_default_75
```

API keys required as environment variables: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`.  
Strategy generation (`create_strategies.py`) requires API access; pre-generated strategies are in `strategies/`.

---

## Citation

If you use this extension, please cite both the original paper and this work:

```bibtex
@misc{Willis2025_llm_ipd,
  author = {Willis, Richard and Du, Yali and Leibo, Joel Z. and Luck, Michael},
  title  = {Will Systems of {LLM} Agents Cooperate: An Investigation into a Social Dilemma},
  year   = {2025},
  eprint = {2501.16173},
  archivePrefix = {arXiv}
}
```
