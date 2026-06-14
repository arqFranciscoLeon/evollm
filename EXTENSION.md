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

Moran equilibria (% Aggressive / % Cooperative / % Neutral), balanced population (4:4:4), no noise, **n=500** (v2):

| Model | Default | Prose | Refine |
|-------|---------|-------|--------|
| Claude 4.6     | 2/49/49  | 5/48/47  | 23/39/38 |
| Gemini 2.5 Flash | 2/49/48 | 24/47/30 | 21/47/32 |
| Gemini 3.1 Pro | 14/42/45 | 19/43/38 | 27/40/33 |
| GPT-5.4 Mini   | 2/53/45  | 12/45/43 | 4/70/26  |

*Willis et al. reference: ChatGPT-4o Default 14/53/33 · Claude 3.5 Sonnet Default 4/49/47*

> **v2 erratum (2026):** the Gemini 3.1 Pro Prose/Refine libraries were truncated
> (21/7 of 75) in v1; regenerated in full and re-run at n=500. The values above are
> the corrected n=500 figures. Cooperative-plurality count 9/12 → 10/12; all
> hypothesis-level conclusions unchanged. See arXiv:2605.29874v2.

---

## Reproducing the Experiments

```bash
# Install dependencies (no setup.py — the project runs in place via PYTHONPATH)
pip install axelrod

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
