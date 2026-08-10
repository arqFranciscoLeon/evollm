# Phase 3 pre-registration — the mixed Axelrod tournament (DRAFT v0.1)

**Status:** DRAFT, not executed. Written 2026-08-10, before any Phase 3 run.
**Decision pending:** PI sign-off after adversarial review (tribunal). Sections
marked **[OPEN]** are deliberately unresolved and are the questions put to the
tribunal.

---

## 1. What this is, and why it is allowed to start now

`PHASE2_PREREG.md` deferred a study it called **2b**: a mixed Western+Chinese
population. Its guardrail read *"Do not start 2b until 2a is written up."*
Paper 2 (Phase 2a) is written, internally reviewed and packaged for arXiv, so
the guardrail is satisfied. Phase 3 is that deferred study, with one change of
shape: **no Moran process**. Phase 3 is a direct competition between
strategies, in the form Axelrod used in 1980.

Two reasons for dropping Moran here. First, Phases 1 and 2 already measured
evolutionary equilibria under replication; what they never measured is what
happens when strategies from different laboratories meet each other directly.
Second, without Moran the compute collapses from days on a rented VPS to hours
on a workstation, which matters because this phase runs with no funded compute
(see §9).

## 2. Research question

When strategies written by eight different frontier models are put in one
population, does the laboratory that wrote a strategy predict how it fares and
how it behaves toward the others? And does that structure survive a second
round in which each laboratory is shown the outcome of the first?

## 3. Prerequisite: re-converting the Western libraries

Phase 1 let each provider convert its own natural-language strategies into
Python. Phase 2 fixed the converter (GPT-5.4 Mini) for all Chinese models.
Putting the two sets in one tournament without correction would reintroduce
exactly the confound that the Phase-1 referees raised as MUST-3: a difference
between a Western and a Chinese strategy could be a difference in who wrote the
prose *or* in who wrote the code.

**Protocol.** Re-convert the 12 Western libraries (4 models x 3 prompt styles,
clean) with GPT-5.4 Mini, using the natural-language prose already stored as
comment blocks inside each strategy file. This is the same mechanism as the
Phase-2 robustness check (`reconvert_robust.py`), which sampled 10%; Phase 3
raises the sample to 100%. **No generation. No new prose. The generator models
are not called.** Seed and manifest recorded as in Phase 2.

**Validation gate (must pass before any tournament runs):**
1. Every re-converted library yields 75 loadable classes with the original
   attitude labels (25 Aggressive / 25 Cooperative / 25 Neutral).
2. Each library survives a smoke run against the 11 Beaufils opponents with
   zero unhandled exceptions.
3. **Fidelity check:** re-run the Phase-1 head-to-head for the re-converted
   Western libraries and report the shift against the published Phase-1
   numbers. This shift is a *result to disclose*, not a failure condition: it
   measures how much of Phase 1 was converter and how much was generator.

If (3) shows large shifts, Phase 1's cross-provider claims are converter-
contaminated to that degree, and we say so in print.

## 4. Tournament 1 — the mixed round-robin

All strategies from all eight laboratories in a single all-play-all
tournament, Axelrod's original format: every strategy meets every other and
itself, 1000 turns, 20 repetitions, classic payoff matrix. This is the
existing `play_vs_llm_strats` path with a merged player list; the code change
is loading several libraries at once and tagging each player with its lab and
ecosystem.

Players carry no information about who they are playing. Any lab-level
structure that appears is therefore **behavioural compatibility, not identity
recognition** — the strategies cannot see a label even in principle.

**[OPEN-A] Scope.** Default prompt only (8 labs x 75 = 600 players, one
tournament), or all three prompt styles (three tournaments of 600)? Default-only
is one clean experiment; all three lets prompt style be a factor but triples
compute and multiplies the comparisons.

**[OPEN-B] Noise.** Clean only, or clean plus the noise condition? Noise is
where Phase 1 and Phase 2 found their most fragile results, and where the
Chinese strategies throw exceptions on nearly every move (documented in Phase
2). Including it is the more informative design and the more expensive one.

## 5. The feedback round and Tournament 2

Axelrod's second tournament gave entrants the published results of the first.
Phase 3 does the same with the laboratories in place of the entrants.

After Tournament 1, each of the eight models receives an **identical** report:
the final ranking, the payoff and cooperation matrices aggregated by attitude,
and the descriptions of the highest- and lowest-scoring strategies. Each model
is then asked to submit a fresh library of 75 strategies under the same prompt
it used originally, now knowing what happened. Those libraries are converted by
the same fixed converter and run as **Tournament 2**, identical in format.

Three commitments fixed in advance:

- **Identical feedback.** Every lab gets the same document. No lab is given a
  tailored briefing.
- **[OPEN-C] Attribution in the feedback.** Axelrod told entrants who had
  submitted what. Do we name the laboratory behind each strategy in the report,
  or anonymise it? Naming is faithful to Axelrod and lets a model reason about
  a rival; anonymising keeps the second round free of any brand priors the
  models carry about each other. This changes what H9 means.
- **One round of feedback only.** Two tournaments, not an open-ended loop. A
  third round is a separate pre-registration.

## 6. Pre-registered hypotheses

**H7 — in-group behavioural compatibility.** Mutual cooperation is higher
between strategies from the same laboratory than between strategies from
different laboratories. Test: mean normalised cooperation in same-lab cells of
the matrix versus different-lab cells, with a permutation test on the lab
labels (10,000 permutations) and the same test at ecosystem level. Directional,
one-tailed. *Reading if supported:* laboratories imprint a coordination style
that makes their own strategies mesh. *If not supported:* strategy behaviour is
set by the attitude prompt, and the lab is decoration.

**H8 — evolutionary equilibria predict direct competition.** The lab-level
aggression proneness measured in Phases 1-2 (P_A) predicts performance in the
mixed tournament: labs with lower P_A score higher mean payoff. Test: Spearman
correlation between lab P_A and lab mean payoff across the eight labs,
one-tailed negative. Eight points is a small n and the test is reported as
such.

**H9 — divergence after feedback.** Seeing the results of Tournament 1 makes
the laboratories *more* different from one another, not less: the spread of
lab-level cooperation rates is wider in Tournament 2 than in Tournament 1.
Test: pre-post comparison of the between-lab variance, bootstrap CI. The
alternative outcome — convergence on whatever won — is equally publishable and
is stated here so it cannot be reframed later as the prediction.

**Secondary, descriptive (not hypotheses):** whether a TitForTat-like strategy
tops Tournament 1 as in Axelrod 1980; whether mean cooperation rises or falls
from T1 to T2; which lab's strategies change most.

**[OPEN-D]** Is H7 the right primary? It is the claim the design is built to
support, but it is also the one most exposed to a null result, since all
strategies come from the same three attitude prompts.

## 7. Analysis and stopping rules

- Every hypothesis test is specified above and will be run once, on the
  complete data, by a script committed before the data exists.
- No strategy is dropped for performing badly. Strategies that fail to load or
  crash unrecoverably are documented, with counts per lab, exactly as the two
  fragile Phase-2 classes were.
- Multiple comparisons across labs use Holm-Bonferroni, as in Phase 2.

## 8. Guardrails (do NOT)

- Do NOT run any tournament before the §3 validation gate passes.
- Do NOT alter H7-H9 after seeing Tournament 1.
- Do NOT let any lab's feedback differ from any other's.
- Do NOT re-generate prose for the Western Phase-1 libraries; the archived
  prose is the input, and re-generating it would silently change the
  experiment.
- Do NOT extend to a third tournament under this pre-registration.

## 9. Feasibility, cost and risk

**Re-conversion:** ~900 conversions with GPT-5.4 Mini. Conversion is the cheap
half of the pipeline (Phase 2's conversion spend was small enough that it was
never separately itemised). No OpenRouter spend, no generator calls.

**Tournament 1:** a 600-player round-robin is roughly 63x the pairings of the
75-player head-to-heads, which ran about 22 minutes each. That extrapolates to
around a day single-threaded, hours across cores. No cloud required. Note the
known Windows multiprocessing PicklingError in tournaments (branch
`claude/happy-mirzakhani`) — resolve before parallelising.

**The feedback round is the expensive and fragile part.** It calls all eight
generator models for 600 new strategies. This reintroduces the Anthropic,
Google and OpenAI generator keys that Phase 2 deliberately did without, and
Google's daily quota already broke a run once during the erratum. Model
availability is the sharper risk: the exact served identifiers of the 2025-2026
Western models and of Kimi K2.5 may not survive to the run date, and a
substitution mid-design would compromise the comparison with Tournament 1.

**[OPEN-E]** Given that risk, should Tournament 1 be published on its own if
the feedback round proves infeasible, or is the two-round structure the paper?

## 10. Relation to the publication plan

Phase 3 is the intended **journal article** (nuevo conocimiento) for the
institutional Phase II commitment; Paper 2 is the **conference paper**
(apropiación social) via AAMAS 2027. They are distinct studies, which is what
keeps the two products from being the same work counted twice.
