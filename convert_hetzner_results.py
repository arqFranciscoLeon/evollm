"""Convert the Hetzner runner's moran_history.csv into the JSON file that
reproduce_tables.py expects (results/phase2_moran_final_*.json).

Usage:
    python convert_hetzner_results.py path/to/moran_history.csv [--out results/]

The CSV is written by run_hetzner.py::append_history with one aggregated row
per condition (algo x population). This script:
  * type-converts every row (counts/pops to int, pcts to float),
  * validates algo names against the 24 pre-registered Chinese libraries,
  * validates that counts sum to `iteraciones` (= n_real) and that the
    percentages match the counts,
  * de-duplicates re-run conditions keeping the LAST row (resume semantics),
  * reports completeness against the 48-condition grid,
  * writes results/phase2_moran_final_<UTC>.json.

It never modifies the input. reproduce_tables.py picks up the newest file
matching its glob automatically.
"""
import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LABS = ("deepseek_v4pro", "qwen3max", "kimi_k25", "glm_51")
PROMPTS = ("default", "prose", "refine")
EXPECTED_ALGOS = sorted(
    f"{lab}_{prompt}_75{suffix}"
    for lab in LABS for prompt in PROMPTS for suffix in ("", "_noise"))
EXPECTED_POPS = ((4, 4, 4), (8, 2, 2))

INT_FIELDS = ("iteraciones", "pop_agresivos", "pop_cooperativos",
              "pop_neutrales", "Aggressive", "Cooperative", "Neutral")
PCT_FIELDS = ("pct_Aggressive", "pct_Cooperative", "pct_Neutral")


def convert_row(raw, lineno):
    row = {"fecha": raw["fecha"], "algo": raw["algo"]}
    for f in INT_FIELDS:
        row[f] = int(raw[f])
    for f in PCT_FIELDS:
        row[f] = float(raw[f])

    if row["algo"] not in EXPECTED_ALGOS:
        raise ValueError(f"line {lineno}: unexpected algo {row['algo']!r}")
    counts_total = row["Aggressive"] + row["Cooperative"] + row["Neutral"]
    if counts_total != row["iteraciones"]:
        raise ValueError(
            f"line {lineno}: counts sum {counts_total} != iteraciones "
            f"{row['iteraciones']} ({row['algo']})")
    for f in PCT_FIELDS:
        expected = 100 * row[f.replace("pct_", "")] / (counts_total or 1)
        if abs(row[f] - expected) > 0.05:
            raise ValueError(
                f"line {lineno}: {f}={row[f]} inconsistent with counts "
                f"(expected {expected:.2f}) ({row['algo']})")
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--out", type=Path,
                        default=Path(__file__).parent / "results")
    args = parser.parse_args()

    with open(args.csv_path, newline="", encoding="utf8") as fh:
        raw_rows = list(csv.DictReader(fh))

    by_condition = {}
    for i, raw in enumerate(raw_rows, 2):
        row = convert_row(raw, i)
        key = (row["algo"], row["pop_agresivos"], row["pop_cooperativos"],
               row["pop_neutrales"])
        if key in by_condition:
            print(f"  note: duplicate condition {key}, keeping latest row")
        by_condition[key] = row

    rows = [by_condition[k] for k in sorted(by_condition)]

    expected = {(a, *p) for a in EXPECTED_ALGOS for p in EXPECTED_POPS}
    missing = sorted(expected - set(by_condition))
    low_n = [(k, by_condition[k]["iteraciones"]) for k in sorted(by_condition)
             if by_condition[k]["iteraciones"] < 500]

    print(f"Conditions: {len(rows)}/{len(expected)}")
    if low_n:
        print(f"n_real < 500 in {len(low_n)} condition(s) "
              "(pathological iterations skipped, documented):")
        for key, n in low_n:
            print(f"  {key[0]} {key[1]}:{key[2]}:{key[3]} -> n={n}")
    if missing:
        print(f"MISSING {len(missing)} condition(s) — output is PARTIAL:")
        for key in missing:
            print(f"  {key[0]} {key[1]}:{key[2]}:{key[3]}")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    suffix = "" if not missing else "_PARTIAL"
    out_path = args.out / f"phase2_moran_final_{stamp}{suffix}.json"
    if missing:
        print("\nNOTE: written with _PARTIAL suffix so reproduce_tables.py's "
              "glob\n(phase2_moran_final_*.json) still matches it; replace "
              "with the full\nconversion once all 48 conditions are done.")
    out_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w", encoding="utf8") as fh:
        json.dump(rows, fh, indent=1, ensure_ascii=False)
    print(f"\nWrote {out_path} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
