# Post hoc analyses for manuscript v5 (NOT preregistered)

Created 28 September 2026, after the registered confirmatory analysis
(`../CONFIRMATORY_RESULTS_v1.md`) and in response to the tribunal record
`../writing/TRIBUNAL_MANUSCRIPT_v4_2026-09-28.md`. Nothing here modifies the
registered H7 test, its inputs, its code or its outputs. Every quantity below is
exploratory or descriptive and must be reported as such.

All scripts run offline with the validated environment (Python 3.12.14,
axelrod 4.14.0) from the repository root, e.g.
`python -m phase3.posthoc_h7_structure_v1`. Each script refuses to overwrite
its output. No API was called and no Modal resources were used.

| Script | Output | Purpose | New encounters |
|---|---|---|---|
| `posthoc_matrix_v1.py` | `primary_matrix_v1.npz/.json` | Rebuilds the registered scenario-0 matrices from the 665 receipts; aborts unless the matrix fingerprint and H7 reproduce exactly | none |
| `posthoc_h7_structure_v1.py` | `h7_structure_v1.json` | Model-by-stratum decomposition; leave-one-model-out; exploratory test without Gemini 3.1 Pro; rank-one propensity benchmark and covariance identity | none |
| `posthoc_h7_residual_v1.py` | `h7_residual_v1.json` | Exploratory permutation test on the residual after the propensity benchmark | none |
| `posthoc_behaviour_v1.py` | `behaviour_v1.json` | Probe-panel signatures, canonical labels, AST and tournament-row sharing across attitude labels | 5,720 (572 identities × 10 deterministic probes) |
| `posthoc_historical_v1.py` | `historical_v1.json` | Archived Phase 1/2 implementations: probe signatures (1,800 classes), historical vs common-conversion agreement, retained vs excluded aggressive descriptions, within-library attitude payoff matrices and association with archived C−N fixation margins, prose length | 18,000 probe matches + 68,400 within-library pairs |
| `posthoc_exclusions_v1.py` | `exclusion_bounds_v1.json` | Behaviour-constrained envelopes for the 28 exclusions | none |
| `posthoc_completion_v1.py` | `completion_v1.json` | What-if: 600-identity panel completed with historical implementations of the 28 exclusions | 16,422 |
| `posthoc_h6_exact_v1.py` | `h6_exact_v1.json` | Fisher and Boschloo exact tests with Holm for the six H6 contrasts | none |
| `posthoc_ecological_v1.py` | `ecological_v1.json` | Axelrod-style discrete replicator dynamics on the registered payoff matrix | none |
| `posthoc_figures_v1.py` | `../writing/figures/` | Figures 1–4 of manuscript v5 | none |

Shared helpers: `posthoc_common_v1.py`. Probe opponents are deterministic
(two of them replay fixed pseudo-random sequences), because axelrod seeds
players differently according to their `stochastic` classifier; an earlier
draft that used `axl.Random` probes produced spurious disagreement between
historical and common-conversion implementations and was discarded before any
result was used.

Signature equality means "indistinguishable against the probe panel", not
formal behavioural equivalence. Historical implementations of truncated or
indeterminate descriptions are not faithful implementations; the completion
scenario mixes two conversion procedures and is reported only as a what-if.
