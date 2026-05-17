# Phase 2 — Pre-registration & Session Handoff

**Status:** PRE-REGISTERED 2026-05 · NOT yet executed.
This document is both (a) the scientific pre-registration for Phase 2 and
(b) the handoff for a fresh Claude Code session. Read it together with
`MEMORY.md` before doing anything.

---

## 0. Where Phase 1 stands (continuity)

- **Paper 1** ("Cross-Provider Empirical Extension", 4 Western frontier
  models, n=500 Moran): peer-reviewed (AAMAS R&R → Minor Revisions),
  EN + ES PDFs built, code clean.
- **Repos:** code = `github.com/arqFranciscoLeon/evollm` (this repo, main);
  manuscript+scaffold = `github.com/arqFranciscoLeon/evollm-paper`.
- **DOI:** `10.5281/zenodo.20248615`.
- **arXiv:** account ready, submission paused **pending one-time cs.MA
  endorsement** — see `evollm-paper/paper/ENDORSEMENT_REQUEST.md`
  (forward arXiv email to Willis et al.; code `HYXLT3`). This is a human
  step, independent of Phase 2.
- **Known limitation Phase 1 (the reason for Phase 2's design):**
  reviewers' MUST-3 / the paper's Limitations — each provider's strategies
  were code-converted by *that same provider's model*, confounding
  provider identity with coding ability. **Phase 2 fixes this.**

## 1. Phase 2 scope (locked)

- **2a — IN SCOPE:** replicate the exact Phase 1 exercise (Axelrod
  tournament + Moran process, n=500, 4 population regimes, 3 prompt
  styles) with **Chinese frontier models**, AND re-run the Western models
  under the corrected protocol so the cross-ecosystem comparison is clean.
- **2b — DEFERRED (explicitly NOT now):** mixed Western+Chinese
  population tournament/Moran. Do not start 2b until 2a is written up.
- **Output:** a standalone Phase 2 paper (target AAMAS 2028 or JAAMAS).

## 2. The confound fix — **Option A (confirmed)**

The independent variable is each model's **strategy-generation**
disposition. The confound is the **NL→Python conversion** step. Fix:

> **One single, fixed code-conversion model converts the
> natural-language strategies of ALL models (Western + Chinese).**
> Strategy *generation* stays per-model (that is the variable we study);
> only *conversion* is held constant.

Because the Western Phase-1 strategies were converted per-provider, a
clean cross-ecosystem comparison requires **re-converting and re-running
tournaments+Moran for the Western models too**, inside Phase 2, with the
fixed converter. Phase 2 is therefore **self-contained**: all numbers in
the Phase 2 paper come from the fixed-converter pipeline.

- **Pre-registered fixed converter:** GPT-5.4 Mini (strong, stable,
  OpenAI-compatible endpoint already wired in `src/evollm`; it is the
  conversion step only, not a contestant advantage since generation is
  separate). *Confirm at session start before any runs.*
- **Robustness check (pre-registered):** re-convert a random 10% sample
  of strategies with a **second, ecosystem-different converter**
  (DeepSeek V4) and show equilibrium proportions are converter-invariant
  (within the n=500 SE ≈ 2.2pp). This pre-empts "the converter choice
  biases results".

## 3. Pre-registered hypotheses (declared BEFORE running)

- **H5 — Cooperative-bias generality.** Chinese frontier models exhibit
  the same cooperative-plurality bias in balanced noiseless conditions
  (≈ matching Phase 1's 9/12 rate), i.e. H1 generalises beyond the
  Western alignment regime.
- **H6 — Ecosystem structure.** Cross-provider divergence is driven by
  *lab-level* training/alignment choices, not by a coarse
  "Western vs Chinese" split: i.e., within-ecosystem variance is
  comparable to or larger than between-ecosystem variance (tested via
  the same two-sample z-tests + Holm-Bonferroni on $P_A$, plus an
  ecosystem-grouped comparison).
- Verdicts will be reported with the same honesty discipline as H1–H4
  (e.g., "confirmed within the tested library", explicit
  not-significant calls, no post-hoc hypothesis edits).

## 4. Models (4 Chinese labs — mirrors Western 3-provider structure)

| Lab | Model (2026) | Notes |
|-----|--------------|-------|
| DeepSeek | DeepSeek V4 | Benchmark leader; also the 2nd robustness converter |
| Alibaba | Qwen 3.6 | Multilingual, wide size range |
| Moonshot | Kimi K2.6 | Strong agentic |
| Zhipu / Z.ai | GLM-5.1 | MIT-licensed, top SWE-bench |

### Amendment 2026-05-17 (made BEFORE any Phase 2 runs)

The original table above is preserved unchanged for transparency. On
wiring the OpenRouter gateway, two of the four pre-registered model
identifiers were not served under those exact names. Substitutions were
fixed **before generating a single strategy** (no results seen), choosing
each lab's current **flagship tier** for a clean flagship-vs-flagship
cross-lab comparison:

| Lab | Pre-registered | Served slug used | Nature of change |
|-----|----------------|------------------|------------------|
| DeepSeek | DeepSeek V4 | `deepseek/deepseek-v4-pro` | Exact-identifier resolution: the V4 Pro tier *is* DeepSeek V4 (the "benchmark leader" intended). Also the 2nd robustness converter. |
| Alibaba | Qwen 3.6 | `qwen/qwen3-max` | True substitution: no "Qwen 3.6" exists; `qwen3-max` is Alibaba's current Qwen3 flagship — the closest faithful match. |
| Moonshot | Kimi K2.6 | `moonshotai/kimi-k2.6` | None (exact). |
| Zhipu / Z.ai | GLM-5.1 | `z-ai/glm-5.1` | None (exact). |

Gateway: OpenRouter (OpenAI-compatible). Hypotheses **H5/H6 are
unchanged**; this amendment concerns model availability only, recorded
ante-hoc per the §7 honesty discipline.

Western set (re-run under fixed converter): Claude Sonnet 4.6,
Gemini 2.5 Flash, Gemini 3.1 Pro, GPT-5.4 Mini (as Phase 1).

Prompts: **English only** for Phase 2a (clean replication). Chinese-language
prompting is a deliberately deferred separate variable (not Phase 2a).

## 5. API access & compute

- Chinese models: OpenAI-compatible endpoints via **Vercel AI Gateway /
  OpenRouter** — no Chinese cloud account needed (works from Colombia).
  Cost 5–30× below Western flagships.
- Moran n=500: reuse the validated **wave-based Modal harness**
  (`modal_moran_waves.py`, `--resume`). Same cost structure as Phase 1.
- Keys: extend `.env.example` with the new provider keys; real `.env`
  stays git-ignored.

## 6. Code changes the new session must make

1. **Decouple generation from conversion** in `src/evollm/create_strategies.py`
   (and `prompts.py`): generate NL strategy with model X → convert to
   Python with the FIXED converter (GPT-5.4 Mini), for every model.
2. Add the 4 Chinese model clients (`src/evollm/llm_clients.py`) via the
   OpenAI-compatible gateway.
3. Generate 75 strategies/model for all 8 models (4 Western re-run + 4
   Chinese) under the fixed converter.
4. Run tournaments + Moran (n=500, 48 conditions per model set) via the
   Modal wave harness.
5. Robustness check: 10% re-conversion with DeepSeek V4.
6. New analysis: extend `reproduce_tables.py` logic for H5/H6 + ecosystem
   grouping. New paper in `evollm-paper` (Phase 2 sections).

## 7. Guardrails (do NOT)

- Do NOT run 2b (mixed tournament) — deferred.
- Do NOT change H5/H6 after seeing results.
- Do NOT use per-provider conversion (defeats the whole point).
- Do NOT touch the Phase 1 arXiv submission flow; it is independent.

## 8. How to start the fresh session

Open a new Claude Code session and say:

> "Read `PHASE2_PREREG.md` and `MEMORY.md`. We continue Phase 2a:
> Chinese-model replication with the fixed code converter (Option A).
> Start with code change #1 (decouple generation from conversion)."

Branch for this work: `phase2/chinese-models` (this branch, off `main`).
