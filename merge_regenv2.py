"""Merge the 4 regenerated refine Moran cells into the authoritative Phase-2
final JSON. Replaces (deepseek_v4pro_refine_75, glm_51_refine_75) x
(4:4:4, 8:2:2) rows with the freshly-run Modal values, leaving the other 44
rows untouched. Writes phase2_moran_final_<ts>_regenv2.json.

Usage:
  python merge_regenv2.py                 # auto-pick newest modal_waves_final_*.json
  python merge_regenv2.py <modal_final.json>
"""
import glob
import json
import os
import sys
from datetime import datetime

AUTH = "results/phase2_moran_final_20260616_015525.json"
TARGET_ALGOS = {"deepseek_v4pro_refine_75", "glm_51_refine_75"}


def key(r):
    return (r["algo"], r["pop_agresivos"], r["pop_cooperativos"], r["pop_neutrales"])


def main():
    if len(sys.argv) > 1:
        modal_path = sys.argv[1]
    else:
        cands = sorted(glob.glob("results/modal_waves_final_*.json"),
                       key=os.path.getmtime)
        assert cands, "no modal_waves_final_*.json found"
        modal_path = cands[-1]
    print(f"AUTH  : {AUTH}")
    print(f"MODAL : {modal_path}")

    auth = json.load(open(AUTH, encoding="utf8"))
    modal = json.load(open(modal_path, encoding="utf8"))

    # new rows = only the target refine cells from the modal output
    new = {key(r): r for r in modal if r["algo"] in TARGET_ALGOS}
    assert len(new) == 4, f"expected 4 target cells in modal output, got {len(new)}: {list(new)}"

    replaced = 0
    out = []
    for r in auth:
        k = key(r)
        if k in new:
            nr = new[k]
            print(f"\nREPLACE {k}")
            print(f"  old A/C/N = {r['Aggressive']:>3}/{r['Cooperative']:>3}/{r['Neutral']:>3}"
                  f"  ({r['pct_Aggressive']}/{r['pct_Cooperative']}/{r['pct_Neutral']})  iter={r['iteraciones']}")
            print(f"  new A/C/N = {nr['Aggressive']:>3}/{nr['Cooperative']:>3}/{nr['Neutral']:>3}"
                  f"  ({nr['pct_Aggressive']}/{nr['pct_Cooperative']}/{nr['pct_Neutral']})  iter={nr['iteraciones']}")
            out.append(nr)
            replaced += 1
        else:
            out.append(r)
    assert replaced == 4, f"replaced {replaced}/4"
    assert len(out) == len(auth) == 48, f"row count changed: {len(out)} vs {len(auth)}"

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outpath = f"results/phase2_moran_final_{ts}_regenv2.json"
    with open(outpath, "w", encoding="utf8") as f:
        json.dump(out, f, indent=2)
    print(f"\nOK -> {outpath}  ({len(out)} rows, 4 replaced)")


if __name__ == "__main__":
    main()
