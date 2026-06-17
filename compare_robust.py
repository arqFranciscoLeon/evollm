"""Converter-robustness verdict (Paper 2, sec 4.7).

Compares the balanced-clean (4:4:4) equilibrium proportions of the 12 HYBRID
libraries (10% re-converted with DeepSeek V4) against the authoritative
GPT-5.4 Mini pipeline, and checks converter-invariance: per-cell |Delta| within
the n=500 sampling band and unchanged plurality (the qualitative claim H5/H6
rest on).

  SE of one proportion at n=500 ~ sqrt(0.25/500) = 2.24pp
  SE of the difference of two such estimates ~ sqrt(2)*2.24 = 3.16pp

Usage: python compare_robust.py [robust_moran_final_*.json]
"""
import glob
import json
import math
import os
import sys

GPT = "results/phase2_moran_final_20260616_151953_regenv2.json"
SE1 = math.sqrt(0.25 / 500) * 100          # 2.24 pp (one estimate)
SEDIFF = math.sqrt(2) * SE1                 # 3.16 pp (difference)
LABELS = {
    "deepseek_v4pro": "DeepSeek V4 Pro", "qwen3max": "Qwen3-Max",
    "kimi_k25": "Kimi K2.5", "glm_51": "GLM-5.1",
}


def plurality(r):
    return max(("A", r["pct_Aggressive"]), ("C", r["pct_Cooperative"]),
               ("N", r["pct_Neutral"]), key=lambda t: t[1])[0]


def main():
    robust_path = sys.argv[1] if len(sys.argv) > 1 else sorted(
        glob.glob("results/robust_moran_final_*.json"), key=os.path.getmtime)[-1]
    print(f"GPT    : {GPT}\nROBUST : {robust_path}\n")
    gpt = {r["algo"]: r for r in json.load(open(GPT)) if
           r["pop_agresivos"] == 4 and r["pop_cooperativos"] == 4}
    rob = {r["algo"].replace("_robust", ""): r for r in json.load(open(robust_path))}

    print(f"{'Lab / prompt':<26}{'GPT A/C/N':>16}{'DeepSeek A/C/N':>18}"
          f"{'dC':>6}{'dA':>6}{'maxd':>6}  plur")
    print("-" * 96)
    max_all = 0.0
    flips = 0
    rows = []
    for base in ("deepseek_v4pro", "qwen3max", "kimi_k25", "glm_51"):
        for p in ("default", "prose", "refine"):
            algo = f"{base}_{p}_75"
            g, r = gpt[algo], rob[algo]
            dA = r["pct_Aggressive"] - g["pct_Aggressive"]
            dC = r["pct_Cooperative"] - g["pct_Cooperative"]
            dN = r["pct_Neutral"] - g["pct_Neutral"]
            md = max(abs(dA), abs(dC), abs(dN))
            max_all = max(max_all, md)
            pg, pr = plurality(g), plurality(r)
            flip = "" if pg == pr else f"  FLIP {pg}->{pr}"
            if pg != pr:
                flips += 1
            print(f"{LABELS[base]+' '+p:<26}"
                  f"{g['pct_Aggressive']:>5.0f}/{g['pct_Cooperative']:>4.0f}/{g['pct_Neutral']:>4.0f}"
                  f"{r['pct_Aggressive']:>7.0f}/{r['pct_Cooperative']:>4.0f}/{r['pct_Neutral']:>4.0f}"
                  f"{dC:>+6.1f}{dA:>+6.1f}{md:>6.1f}   {pr}{flip}")
            rows.append(md)

    within_se1 = sum(1 for m in rows if m <= SE1)
    within_sediff = sum(1 for m in rows if m <= SEDIFF)
    mean_md = sum(rows) / len(rows)
    print("-" * 96)
    print(f"\nSE(one est., n=500) = {SE1:.2f}pp   SE(difference) = {SEDIFF:.2f}pp")
    print(f"max |Delta| across 36 cells = {max_all:.1f}pp   mean max-|Delta| per cell = {mean_md:.1f}pp")
    print(f"cells with max-|Delta| <= {SE1:.2f}pp : {within_se1}/12")
    print(f"cells with max-|Delta| <= {SEDIFF:.2f}pp : {within_sediff}/12")
    print(f"plurality flips: {flips}/12")
    verdict = ("CONVERTER-INVARIANT" if flips == 0 and max_all <= 2 * SEDIFF
               else "CHECK: deviations exceed expectation")
    print(f"\nVERDICT: {verdict}")


if __name__ == "__main__":
    main()
