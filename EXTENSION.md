# Extension: Cross-Provider Benchmark with 2025–2026 Frontier Models (n=500)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20248615.svg)](https://doi.org/10.5281/zenodo.20248615)

This is the **code and replication package** for the paper:

> *Evolutionary Dynamics of Cooperation in Next-Generation LLM Agent Systems:
> A Cross-Provider Empirical Extension* — Francisco León Zúñiga Bolívar,
> Institución Universitaria Colegio Mayor del Cauca (2026).

It extends the original Willis et al. (2025) benchmark
([arXiv:2501.16173](https://arxiv.org/abs/2501.16173); upstream code in
`origin`, `willis-richard/evollm`) to four next-generation models spanning
three providers, at **500 Moran iterations per condition**.

This repository keeps the upstream structure (`src/evollm/`, `strategies/`,
`tests/`, `environment.yml`) so results are reproducible and comparable to the
original. The paper manuscript and clo-author authoring scaffold live in a
**separate** repository (`evollm-paper`); this repo is the scientific code only.

---

## New Models

| Model | Provider | Predecessor (Willis et al.) |
|-------|----------|------------------------------|
| Claude Sonnet 4.6 | Anthropic | Claude 3.5 Sonnet |
| Gemini 2.5 Flash  | Google    | (new provider) |
| Gemini 3.1 Pro    | Google    | (new provider) |
| GPT-5.4 Mini      | OpenAI    | ChatGPT-4o |

Three prompt styles (Default, Prose, Self-Refine) × four population regimes
(balanced/biased × clean/noisy) = **48 Moran conditions**, each at n=500.

## Hypotheses (pre-registered)

- **H1** Cooperative bias persists — *Confirmed within the tested library* (9/12).
- **H2** Aggressive capability parity — *Partially supported*.
- **H3** Cross-provider divergence — *Confirmed* (z up to 17.1, Holm-Bonferroni).
- **H4** Noise robustness improves — *Suggestive, not robustly confirmed*
  (cross-study comparison to the n=100 predecessor is not significant once the
  baseline's sampling error is propagated; we deliberately do **not** re-run
  the predecessor solely to resolve H4 — that would be result-driven analysis).

---

## Reproduction

### 1. Environment
```shell
conda env create -f environment.yml
conda activate evollm
export PYTHONPATH="$(pwd)/src"
```

### 2. Generate strategies (requires provider API keys)
Copy `.env.example` to `.env` and fill in your keys (the real `.env` is
git-ignored and must never be committed).
```shell
python src/evollm/create_strategies.py --model <model> --prompt <style>
```

### 3. Run the n=500 Moran simulations (Modal cloud)

The n=500 results were produced with a **wave-based Modal harness** that
submits ~100 short tasks per wave with per-wave checkpointing. This avoids the
preemption failures that a single 12,000-task submission triggers on Modal's
starter tier (one preemption after 14 h of compute loses 14 h; a 3-min task
loses 3 min).

```shell
pip install modal && python -m modal setup
python -m modal run modal_moran_waves.py            # full n=500, 48 conditions
python -m modal run modal_moran_waves.py --resume   # resume from checkpoint
```

Locally (single condition, any n):
```shell
PYTHONPATH=src python src/evollm/moran_process.py \
  --algo strategies/<algo> --initial_pop 4 4 4 --iterations 500
```

### 4. Authoritative results

`results/modal_waves_final_20260515_154815.json` is the single source of truth
for every Moran number in the paper (48 conditions × 500 iterations; integer
win counts that sum to 500 plus rounded percentages). The n=100 files in
`results/*_moran.csv` are a **superseded pilot** retained only for provenance.

---

## Interactive results viewer (GUI)

A Streamlit dashboard reproduces the paper's tables and figures directly from
the authoritative n=500 JSON, for transparent inspection and analysis:

```shell
python -m streamlit run gui.py
```

The **"📄 Vista Paper"** tab renders:

- **Table 5** — Moran equilibrium proportions (%A/%C/%N), 12 model–prompt
  combinations × 4 regimes, with Willis et al. reference rows.
- **Figure 2** — 4-panel stacked-bar equilibrium distribution (paper colours).
- **Table 6** — pairwise cross-provider z-tests with Holm-Bonferroni.
- **Table 8** — noise sensitivity Δ_noise, with Willis et al. reference rows.

Every table is downloadable as CSV. The exact paper numbers also reproduce via
`evollm-paper`'s `analysis_h3_h4_entropy.py`.

---

## Key files

| Path | Purpose |
|------|---------|
| `src/evollm/` | Upstream Willis et al. simulation core (unchanged API) |
| `strategies/` | Generated LLM strategy libraries (75 per model) |
| `modal_moran_waves.py` | Wave-based n=500 cloud harness (checkpointed) |
| `modal_moran_batched.py` | Earlier batched harness (kept for provenance) |
| `gui.py` | Streamlit viewer incl. the *Vista Paper* tab |
| `results/modal_waves_final_*.json` | **Authoritative n=500 results** |
| `.env.example` | Template for provider API keys (real `.env` git-ignored) |

## Citation

If you use this extension, please cite both the original Willis et al. (2025)
paper and this extension. See the `evollm-paper` repository for the manuscript
and BibTeX.
