# How to verify our results

This package is built so anyone can **download it and independently check the
paper's numbers**, at the level of effort they choose. Pick a tier.

| Tier | Effort | No. of commands | Needs API keys / cloud? | Verifies |
|------|--------|-----------------|-------------------------|----------|
| **0** | seconds | 1 | No | Artifacts are intact and unmodified |
| **1** | ~1 min | 1 | No | Tables 5, 6, 8 + H3/H4 statistics |
| **2** | ~30–90 min | 2 | No | Table 5 reproduced from strategies (within sampling SE) |
| **3** | hours + cost | 3 | **Yes** | Full pipeline incl. LLM strategy generation |

Every figure printed by Tier 1 appears verbatim in the manuscript.

---

## Tier 0 — Integrity (seconds, no Python deps)

Confirm you downloaded exactly the artifacts the paper used:

```bash
sha256sum -c <(grep -E '^[0-9a-f]{64}  ' CHECKSUMS.txt)
```

(Windows PowerShell: `Get-FileHash results\modal_waves_final_*.json -Algorithm SHA256`
and compare against the hash in `CHECKSUMS.txt`.)

If the hashes match, the authoritative n=500 results and the 24 strategy
libraries are bit-identical to ours.

---

## Tier 1 — Reproduce every table number (~1 minute, no setup)

`reproduce_tables.py` needs **only the Python standard library** and the
committed `results/modal_waves_final_*.json`. No conda env, no API keys, no
cloud, no scipy.

```bash
python reproduce_tables.py
```

Expected output (must match the manuscript exactly):

- **Table 5** — Moran equilibrium proportions, all 48 conditions
- **Table 6** — pairwise z-tests: `+7.24, −6.92, −6.61` (all `***`),
  and three `ns` — Holm-Bonferroni thresholds shown
- **Table 8** — Δnoise: Claude 4.6 = 6, Flash = 15, G3.1 Pro = 9, GPT = 15
- **H4** — cross-study z ≈ 0.87, p ≈ 0.39 → **not significant**
  (H4 is reported as *suggestive, not robustly confirmed* — this is the
  honest verdict; we deliberately do not re-run the predecessor solely to
  resolve it)

Or browse the same tables and Figure 2 interactively:

```bash
python -m streamlit run gui.py     # → "📄 Vista Paper" tab
```

---

## Tier 2 — Re-run the Moran process from the committed strategies (no LLM)

The 24 strategy libraries (`strategies/*_75*.py`) are **already committed** —
they are plain Python, so re-running the evolutionary simulation needs **no
LLM API calls**. This reproduces **Table 5** within Monte-Carlo error
(per-proportion SE ≈ 2.2pp at n=500).

```bash
conda env create -f environment.yml      # pinned: axelrod==4.14.0
conda activate evollm311
export PYTHONPATH="$(pwd)/src"

# one condition, locally (repeat per algo/regime, or use the cloud harness):
python src/evollm/moran_process.py \
  --algo strategies/anthropic_sonnet46_default_75 \
  --initial_pop 4 4 4 --iterations 500
```

Results are stochastic: expect each %A/%C/%N to land within ~2× the SE of the
paper's value, not bit-identical. Convergent direction and plurality must match.

To reproduce all 48 conditions in parallel (cloud, ~1 h, ~US$15):

```bash
pip install modal && python -m modal setup
python -m modal run modal_moran_waves.py            # wave-based, checkpointed
python -m modal run modal_moran_waves.py --resume   # resume if interrupted
```

---

## Tier 3 — Full pipeline incl. strategy generation (honest caveat)

Regenerating the strategy libraries from scratch calls the four providers'
LLM APIs:

```bash
cp .env.example .env        # fill in OPENAI / ANTHROPIC / GOOGLE keys
python src/evollm/create_strategies.py --model <model> --prompt <style>
```

**This will NOT bit-reproduce our strategies.** LLM generation is
non-deterministic and model versions drift over time; the exact strategy text
(and therefore Table 5 to the last point) depends on the provider model
snapshot at generation time. This is an inherent property of LLM-agent
research, disclosed honestly. Tiers 0–2 are fully deterministic given the
committed strategies; Tier 3 reproduces the *methodology*, not the exact
strategy library.

---

## What lives where

| Repository | Contents |
|------------|----------|
| `github.com/arqFranciscoLeon/evollm` (this repo) | Simulation code, strategy libraries, n=500 results, `reproduce_tables.py`, GUI |
| `github.com/arqFranciscoLeon/evollm-paper` | Manuscript LaTeX + authoring scaffold (not required to verify results) |
| `github.com/willis-richard/evollm` | Upstream Willis et al. (2025) original |

See `EXTENSION.md` for the scientific overview and `CHECKSUMS.txt` for the
integrity manifest.
