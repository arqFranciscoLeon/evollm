# EvoLLM Phase 3 — replication guide (release v3.0-phase3)

This release adds the completed Phase 3 record to the frozen protocol commit
`18cb41744f3f1e66fe711aad09697980476c2498`, which was registered on OSF
(https://osf.io/2nzdh) before the confirmatory tournament was executed.
The frozen commit remains unchanged; everything added afterwards is in later
commits and is identifiable with `git diff --stat 18cb417..v3.0-phase3`.

## Contents

| Path | Content | Status |
|---|---|---|
| `phase3/PHASE3_PROTOCOL_v1.md`, `phase3/reuse_plan_v1/`, `phase3/validation/uniform_derived_candidates_v1.json` | Registered protocol, 665-batch plan, field manifest | Frozen before execution |
| `phase3/validation/modal_confirmatory_batch_*_receipt.json` | 665 confirmatory receipts (166,172 computed encounters) | Execution record |
| `phase3/analyze_confirmatory_results_v1.py`, `phase3/validation/confirmatory_analysis_v1.json`, `phase3/CONFIRMATORY_RESULTS_v1.md`, `phase3/DESCRIPTIVE_RESULTS_v1.md`, `phase3/ANALYSIS_CORRECTION_LOG_v1.md` | Registered analysis and its outputs | Registered analysis |
| `phase3/MODAL_*`, `phase3/modal_*.py`, `phase3/verify_modal_wave_v1.py` | Execution waves on Modal, launch wrappers and receipt verification | Execution record |
| `phase3/registration_v1/` | OSF packet, freeze inventories, public-registration record, GitHub publication record | Registration record |
| `phase3/posthoc_*_v1.py`, `phase3/posthoc_v1/` | Post hoc analyses (see `phase3/posthoc_v1/README.md`) | NOT preregistered |
| `phase3/inputs/`, `phase3/validation/` (other files), audit and review reports | Conversion requests, eligibility reviews, fidelity validation, archived historical libraries | Pre-registration provenance |
| `phase3/writing/prior_evidence_reconciled_v1.json` and its script | Reconciled Phase 1/2 archive values used by the post hoc analyses | Retrospective reconciliation |

Not included, by design: raw converter API responses (`phase3/conversion_runs/` beyond the selected sources), the per-wave Modal download folders and upload bundles (duplicates of files included here), account billing records, and manuscript drafts.

## Environment

Python 3.12.14 and the pinned dependencies in `phase3/requirements-validation.lock.txt` (axelrod 4.14.0). The strict loader refuses to run under another Python or axelrod version. Run every command from the repository root.

## 1. Verify the complete confirmatory schedule

```text
python -c "from phase3.verify_modal_wave_v1 import verify; x=verify(tuple(range(665))); print(x['matches'], x['logical_scenario_results'], x['errors'])"
```

Expected output: `166172 2622048 0`.

## 2. Reproduce the registered analysis

`analyze_confirmatory_results_v1.py` refuses to overwrite its outputs. To re-run it, work on a copy of the repository, delete `phase3/validation/confirmatory_analysis_v1.json` and `phase3/CONFIRMATORY_RESULTS_v1.md` there, and run
`python -m phase3.analyze_confirmatory_results_v1`. The primary result must be
H7 = 0.005348991712007744 with one-sided p = 1/10,001 (10,000 permutations, seed 20260913).
The script checks the hashes of the frozen analyzer, sensitivity code, field manifest, sensitivity plan and batch manifest before computing anything.

## 3. Post hoc analyses (not preregistered)

Documented in `phase3/posthoc_v1/README.md`. Each script refuses to overwrite its output; on a copy, delete the corresponding file in `phase3/posthoc_v1/` and run, for example, `python -m phase3.posthoc_h7_structure_v1`. `posthoc_matrix_v1.py` aborts unless the rebuilt matrix reproduces the registered fingerprint (`b38cc9f6…`) and H7 exactly.

## 4. Tests

`python -m pytest phase3/tests -q` (135 tests at this release).
