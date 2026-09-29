"""Reanalyse explicitly selected n=500 archives; never fill missing cells with zero."""
import hashlib
import itertools
import json
import math
from pathlib import Path

from phase3.audit_inputs import MODELS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phase3" / "evidence"
PROMPTS = ("default", "prose", "refine")
ATTITUDES = ("Aggressive", "Cooperative", "Neutral")


def load_checked(path, models, robust=False):
    rows = json.loads(path.read_text(encoding="utf-8-sig"))
    expected = {(f"{m}_{p}_75{suffix}", pop) for m in models for p in PROMPTS
                for suffix in (("_robust",) if robust else ("", "_noise"))
                for pop in (((4, 4, 4),) if robust else ((4, 4, 4), (8, 2, 2)))}
    result = {}
    for row in rows:
        key = (row["algo"], tuple(row[f"pop_{a}"] for a in ("agresivos", "cooperativos", "neutrales")))
        if key not in expected or key in result:
            raise ValueError(f"Unexpected or duplicate condition in {path}: {key}")
        counts = [row[a] for a in ATTITUDES]
        denominator = row["iteraciones"]
        if type(denominator) is not int or denominator <= 0 or denominator > 500 or any(type(c) is not int or c < 0 for c in counts) or sum(counts) != denominator:
            raise ValueError(f"Invalid count denominator: {path}, {key}")
        if denominator != 500 and "_noise" not in row["algo"]:
            raise ValueError(f"Clean inference requires n=500: {path}, {key}")
        for a in ATTITUDES:
            if abs(row[f"pct_{a}"] - 100 * row[a] / denominator) > 0.0051:
                raise ValueError(f"Percentage disagrees with counts: {path}, {key}")
        result[key] = row
    if set(result) != expected:
        raise ValueError(f"Missing {len(expected-set(result))} conditions in {path}")
    return result


def winner(row):
    largest = max(row[a] for a in ATTITUDES)
    names = [a for a in ATTITUDES if row[a] == largest]
    return names[0] if len(names) == 1 else "Tie"


def cn_margin(row):
    c, n = row["Cooperative"] / 500, row["Neutral"] / 500
    margin = c - n
    se = math.sqrt((c + n - margin * margin) / 500)
    return {"margin_pp": margin * 100, "ci95_pp": [(margin - 1.96 * se) * 100, (margin + 1.96 * se) * 100],
            "ci_includes_zero": abs(margin) <= 1.96 * se}


def pairwise_aggression(data, models, robust=False):
    comparisons = []
    for a, b in itertools.combinations(models, 2):
        suffix = "_robust" if robust else ""
        x = data[(f"{a}_default_75{suffix}", (4, 4, 4))]["Aggressive"]
        y = data[(f"{b}_default_75{suffix}", (4, 4, 4))]["Aggressive"]
        p = (x + y) / 1000
        z = (x / 500 - y / 500) / math.sqrt(p * (1-p) * 2 / 500) if 0 < p < 1 else 0
        comparisons.append({"models": [a, b], "counts": [x, y], "z": z, "p": math.erfc(abs(z)/math.sqrt(2))})
    # Correct Holm step-down: stop rejecting after the first failed threshold.
    still_rejecting = True
    for rank, row in enumerate(sorted(comparisons, key=lambda x: x["p"])):
        row["threshold"] = .05 / (len(comparisons) - rank)
        still_rejecting = still_rejecting and row["p"] <= row["threshold"]
        row["reject_holm"] = still_rejecting
    return comparisons


def main():
    western, chinese = list(MODELS)[:4], list(MODELS)[4:]
    sources = {
        "phase1": ROOT.parents[2] / ".claude/worktrees/erratum/results/modal_waves_final_20260613_122828_erratumv2.json",
        "phase2": ROOT / "results/phase2_moran_final_20260616_151953_regenv2.json",
        "robust": ROOT / "results/robust_moran_final_20260617_045913.json",
    }
    # ROOT = D:/evollm/.claude/worktrees/stupefied-mclaren; parent[2] = D:/evollm.
    OUT.mkdir(parents=True, exist_ok=True)
    datasets = {}
    provenance = {}
    for key, source in sources.items():
        target = OUT / source.name
        # A cloned release can reproduce the analysis from the committed snapshot
        # without access to the author's sibling erratum worktree.
        actual_source = source if source.exists() else target
        data = actual_source.read_bytes()
        if target.exists() and target.read_bytes() != data:
            raise ValueError(f"Evidence snapshot changed: {target}")
        target.write_bytes(data)
        datasets[key] = load_checked(target, western if key == "phase1" else chinese, key == "robust")
        provenance[key] = {"read_path": str(actual_source), "snapshot": str(target.relative_to(ROOT)),
                           "sha256": hashlib.sha256(data).hexdigest(), "conditions": len(datasets[key])}
    balanced = {}
    for key, dataset in datasets.items():
        balanced[key] = [{"algo": algo, "counts": {a: r[a] for a in ATTITUDES},
                          "plurality": winner(r), **cn_margin(r)}
                         for (algo, pop), r in dataset.items() if pop == (4,4,4) and "_noise" not in algo]
    flips = []
    for model in chinese:
        for prompt in PROMPTS:
            algo = f"{model}_{prompt}_75"
            a = datasets["phase2"][(algo, (4,4,4))]
            b = datasets["robust"][(algo + "_robust", (4,4,4))]
            if winner(a) != winner(b):
                flips.append({"algo": algo, "from": winner(a), "to": winner(b)})
    summary = {"provenance": provenance, "balanced_clean": balanced,
               "below_planned_n500": {k: [{"algo": algo, "population": pop, "actual_n": row['iteraciones'], "shortfall": 500-row['iteraciones']} for (algo,pop),row in ds.items() if row['iteraciones'] != 500] for k,ds in datasets.items()},
               "cooperative_pluralities": {k: sum(r["plurality"] == "Cooperative" for r in rows) for k, rows in balanced.items()},
               "cn_margins_including_zero": {k: sum(r["ci_includes_zero"] for r in rows) for k, rows in balanced.items()},
               "phase2_robust_plurality_flips": flips,
               "phase2_h6": pairwise_aggression(datasets["phase2"], chinese),
               "robust_h6": pairwise_aggression(datasets["robust"], chinese, True),
               "interpretation": "Post hoc reanalysis of published data. C/N intervals are marginal normal approximations, not simultaneous intervals. Monte Carlo uncertainty is conditional on fixed libraries. A hybrid 8/75 reconversion plus a fresh run does not isolate converter effects from simulation variability."}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + '\n', encoding="utf-8")
    print(json.dumps({"conditions": {k: v['conditions'] for k,v in provenance.items()},
                      "pluralities": summary['cooperative_pluralities'],
                      "cn_intervals_covering_zero": summary['cn_margins_including_zero'],
                      "flips": len(flips), "below_n500": {k: len(v) for k,v in summary['below_planned_n500'].items()},
                      "h6_significant_pairs": {k: sum(x['reject_holm'] for x in summary[k]) for k in ('phase2_h6','robust_h6')}}, indent=2))


if __name__ == "__main__":
    main()
