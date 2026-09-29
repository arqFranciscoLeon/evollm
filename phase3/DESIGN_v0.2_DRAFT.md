# Mixed-model tournament: proposed design v0.2

Date: 2026-09-13. Status: working proposal, not frozen or publicly registered. No Phase 3 tournament outcomes have been collected in this task. Preserves [v0.1](../PHASE3_PREREG.md) as the historical record; amendments below are explicit proposals, not retroactive changes.

Input audit update: [provenance report](PROSE_PROVENANCE_REPORT.md) closes the available local search with 18 unrecovered descriptions, all Aggressive (2 Flash, 16 Pro). [Proposed amendment](AMENDMENT_PROSE_v0.1.md) specifies a separate archival-code study and unequal-stratum sensitivity; it does not silently replace the common-converter primary study below.

## Primary study

Eight models from seven laboratories, 75 archived Default strategies each, 25 per attitude, clean IPD. The four Western libraries must be converted from verified archived prose through the fixed converter used in Phase 2. The exact served converter, dates and differences from the Phase 2 endpoint must be recorded; using the same model name months later does not guarantee identical weights or service behavior.

Prose and Refine are prespecified secondary explorations, contingent on input integrity and resources; decisions to run them must not depend on Default significance. The first paper is the clean mixed tournament. No inference about deployment-wide behavior or populations of all models is intended.

## H7: within-model compatibility

Use **model**, not laboratory, as the primary grouping variable. Google supplies two models. Laboratory and geographic ecosystem contrasts are secondary, with the asymmetry explicitly disclosed. Neither grouping can establish a causal training or alignment effect in this observational corpus.

The primary outcome should be the fraction of rounds with **both actions C**, not the average of two unilateral cooperation rates. Retain CC, CD, DC and DD counts and payoffs separately. Exclude exact self-pairings from H7; report them separately. Do not discard distinct strategies that happen to have identical code, but measure duplication and specify a sensitivity analysis before outcomes.

Proposed statistic: average the within-model minus between-model difference in mutual cooperation, balancing over model groups and the six unordered attitude-pair strata. Define the exact formula in `analyze_phase3.py` before the freeze, including how missing/failed matches are handled. Failure counts cannot silently change denominators.

Use 10,000 label permutations at strategy level, within attitude, preserving 25 strategies of each attitude per model. A strategy label belongs jointly to its entire row and column; cells are not independent samples. The directional permutation result assesses association under this conditional exchangeability null. Report the effect size, model matrices and uncertainty; not just p-values. Null findings are inconclusive about mechanisms and cannot prove attitude alone determines behavior.

## Tournament and robustness

The inherited 1,000 turns / 20 repetitions is a provisional baseline for comparability. Freeze the repetition count and precision rationale before substantive outcomes; calibrate runtime with synthetic opponents. Do not select stopping rules using observed H7 significance. Payoffs are classic IPD, with numeric values checked against `common.get_game('classic')` in the locked implementation.

Balanced 25/25/25 attitudes describe an experimental field, not a naturally occurring ecology. Prespecify payoff/cooperation reweighting for balanced (1/3,1/3,1/3) and attitude-biased (2/3,1/6,1/6, with each attitude dominant in turn) opponent mixtures. These are counterfactual summaries of fixed pairwise play, not new observed populations. Analyze classical opponents separately so they do not change the primary 600-player field.

An ecological update from the payoff matrix is an optional secondary extension. Its equation, payoff treatment and convergence/stopping criteria remain to be specified; do not infer evolutionary stability merely because a numerical trajectory appears to settle. There is no requirement to rerun Moran for the primary study.

## H8 and H9

Withdraw H8 from confirmatory testing: old Phase 1 equilibria describe a different code-conversion pipeline. Comparisons against prior papers may remain descriptive with provenance explicit.

Defer H9 and Tournament 2 to a separate protocol. A valid feedback study needs a freshly generated no-feedback control, a fixed anonymized report template, prespecified comparison groups and a costed availability probe. Changes relative to old Tournament 1 alone do not identify a feedback effect. Eight model endpoints are not eight independent laboratories. No API regeneration, substitution rule or feedback format is silently adopted by this draft.

## Input and execution gates

- Resolve the confirmed truncated Gemini prose and historical 21/7-class libraries; preserve original artifacts and record chosen hashes. Heuristic text flags require inspection.
- Select authoritative Chinese libraries from the Phase 2 published package and corrected Western libraries from the erratum, with an explicit manifest. There is no automatic substitution based only on class count.
- Validate loadability and labels, then run the complete intended horizon against classical opponents and mixed-strategy validation cases. Record every exception and invalid action. «No unhandled exception» is insufficient if an exception handler substitutes D.
- Fix failures through a documented protocol independent of payoffs; count retries and exclusions. If prose cannot be recovered, disclose the limitation and amend the inclusion rule before observing the tournament. Never fill gaps from imagination.
- Audit whether prose-to-code conversion changes behavioral indicators within Western libraries; report the change without treating any change as proof of error in Paper 1. Changes to published papers require an evidence-based assessment.
- Implement and test the executor and analysis on synthetic fixtures, including repeated class names across libraries, dependency among matrix cells and exact self-pair removal. Record dependency versions, seeds, manifests and checkpoint format.
- Freeze the final protocol and analysis implementation in version control, then deposit a timestamped registration before the confirmatory run. The local historical document by itself does not establish a public preregistration.

## Remaining specification work

Exact H7 formula, uncertainty calculation, duplicate-code sensitivity, precision target, outcome-independent handling of unconvertible or crashing strategies, final converter provenance and measured budget. These are implementation/design tasks to complete during preparation. This proposal does not claim that the eight critical issues in the earlier simulated tribunal are all closed.

## Publication and disclosure

Target JAAMAS on the strength of a distinct cross-model compatibility question and a reproducible controlled experiment. Include data/code availability, AI assistance disclosure, original author responsibility, and a precise relationship to both arXiv papers. Do not call this the first LLM tournament: [Pal et al. (2026)](https://doi.org/10.1093/pnasnexus/pgag210) already include such experiments. See [publication and startup plan](START_HERE.md).
