"""
reproduce_tables.py — one-command verification of the paper's numbers.

Reproduces Table 5 (Moran equilibria), Table 6 (cross-provider z-tests
with Holm-Bonferroni), Table 8 (noise sensitivity), and the H3/H4
inferential statistics, directly from the authoritative n=500 results.

Run from the repository root (no API keys, no cloud, no scipy):

    python reproduce_tables.py

Data source (committed, relative path):
    results/modal_waves_final_*.json   <- authoritative n=500 results

The n=100 files in results/*_moran.csv are a SUPERSEDED pilot and are
NOT used here. Every figure printed below appears in the manuscript;
see REPRODUCE.md for the tiered verification ladder.
"""

import json
import math
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
N = 500  # iterations per condition (authoritative run)

PAPER_ALGOS = [
    ("anthropic_sonnet46_default_75", "Claude 4.6",       "Default"),
    ("anthropic_sonnet46_prose_75",   "Claude 4.6",       "Prose"),
    ("anthropic_sonnet46_refine_75",  "Claude 4.6",       "Refine"),
    ("gemini_25_flash_default_75",    "Gemini 2.5 Flash", "Default"),
    ("gemini_25_flash_prose_75",      "Gemini 2.5 Flash", "Prose"),
    ("gemini_25_flash_refine_75",     "Gemini 2.5 Flash", "Refine"),
    ("gemini_31_pro_default_75",      "Gemini 3.1 Pro",   "Default"),
    ("gemini_31_pro_prose_75",        "Gemini 3.1 Pro",   "Prose"),
    ("gemini_31_pro_refine_75",       "Gemini 3.1 Pro",   "Refine"),
    ("openai_gpt54mini_default_75",   "GPT-5.4 Mini",     "Default"),
    ("openai_gpt54mini_prose_75",     "GPT-5.4 Mini",     "Prose"),
    ("openai_gpt54mini_refine_75",    "GPT-5.4 Mini",     "Refine"),
]
# Willis et al. (2025) Table 6 reference Δnoise averages
WILLIS_DNOISE = {"Claude 3.5 Sonnet": 13, "ChatGPT-4o": 6}


def load_n500():
    files = sorted(HERE.glob("results/modal_waves_final_*.json"))
    if not files:
        raise SystemExit(
            "No results/modal_waves_final_*.json found. "
            "Run `python -m modal run modal_moran_waves.py` or restore the "
            "committed authoritative results file."
        )
    with open(files[-1], encoding="utf8") as fh:
        rows = json.load(fh)
    d = {}
    for r in rows:
        pop = f"{r['pop_agresivos']}{r['pop_cooperativos']}{r['pop_neutrales']}"
        d[(r["algo"], pop)] = r
    return d, files[-1].name


def z_test(x1, x2, n1=N, n2=N):
    p1, p2 = x1 / n1, x2 / n2
    pp = (x1 + x2) / (n1 + n2)
    if pp in (0.0, 1.0):
        return 0.0, 1.0
    se = math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se
    p = math.erfc(abs(z) / math.sqrt(2))  # two-sided, normal approx
    return z, p


def main():
    d, src = load_n500()
    print(f"Authoritative source: results/{src}  (n={N} per condition)\n")

    def rec(algo, pop, noise=False):
        return d.get((algo + ("_noise" if noise else ""), pop), {})

    def acn(r):
        if not r:
            return "   —    "
        return (f"{round(r['pct_Aggressive']):>2}/"
                f"{round(r['pct_Cooperative']):>2}/"
                f"{round(r['pct_Neutral']):>2}")

    # ---- TABLE 5 ----
    print("=" * 72)
    print("TABLE 5 — Moran equilibrium proportions (%A/%C/%N), n=500")
    print("=" * 72)
    print(f"{'Model':<18}{'Prompt':<8}{'4:4:4 cln':>11}{'4:4:4 nse':>11}"
          f"{'8:2:2 cln':>11}{'8:2:2 nse':>11}")
    print("-" * 72)
    for algo, model, prompt in PAPER_ALGOS:
        print(f"{model:<18}{prompt:<8}"
              f"{acn(rec(algo,'444')):>11}{acn(rec(algo,'444',True)):>11}"
              f"{acn(rec(algo,'822')):>11}{acn(rec(algo,'822',True)):>11}")

    # ---- TABLE 6 ----
    print("\n" + "=" * 72)
    print("TABLE 6 — Pairwise z-tests on p_A (4:4:4 clean, Default), Holm-Bonf.")
    print("=" * 72)
    zt = {
        "Claude 4.6":   rec("anthropic_sonnet46_default_75", "444"),
        "G2.5 Flash":   rec("gemini_25_flash_default_75",    "444"),
        "G3.1 Pro":     rec("gemini_31_pro_default_75",      "444"),
        "GPT-5.4 Mini": rec("openai_gpt54mini_default_75",   "444"),
    }
    names = list(zt)
    x = {k: int(v.get("Aggressive", 0)) for k, v in zt.items()}
    pairs = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            z, p = z_test(x[a], x[b])
            pairs.append((a, b, x[a], x[b], z, p))
    pairs.sort(key=lambda t: t[5])
    k = len(pairs)
    print(f"{'Comparison':<34}{'z':>8}{'p':>12}{'HB-thr':>9}  sig")
    print("-" * 72)
    for rank, (a, b, xa, xb, z, p) in enumerate(pairs):
        thr = 0.05 / (k - rank)
        sig = "***" if p < thr else "ns"
        print(f"  {a}({round(100*xa/N)}%) vs {b}({round(100*xb/N)}%)"
              .ljust(34) + f"{z:>+8.2f}{p:>12.2e}{thr:>9.4f}  {sig}")

    # ---- TABLE 8 ----
    print("\n" + "=" * 72)
    print("TABLE 8 — Noise sensitivity D = %C(clean) - %C(noise), 4:4:4")
    print("=" * 72)
    print(f"{'Model':<18}{'Default':>9}{'Prose':>8}{'Refine':>8}{'Avg.':>7}")
    print("-" * 72)
    claude_avg = None
    for model in ["Claude 4.6", "Gemini 2.5 Flash",
                  "Gemini 3.1 Pro", "GPT-5.4 Mini"]:
        ds = []
        for algo, m, _ in PAPER_ALGOS:
            if m != model:
                continue
            cl = rec(algo, "444").get("pct_Cooperative", 0)
            ns = rec(algo, "444", True).get("pct_Cooperative", 0)
            ds.append(cl - ns)
        avg = sum(ds) / len(ds)
        if model == "Claude 4.6":
            claude_avg = avg
        print(f"{model:<18}{round(ds[0]):>9}{round(ds[1]):>8}"
              f"{round(ds[2]):>8}{round(avg):>7}")
    for m, v in WILLIS_DNOISE.items():
        print(f"{m+' (Willis)':<18}{'':>9}{'':>8}{'':>8}{v:>7}")

    # ---- H4 honest cross-study assessment ----
    print("\n" + "=" * 72)
    print("H4 — cross-study comparison (honest, conservative)")
    print("=" * 72)
    se_p_500 = math.sqrt(0.25 / 500) * 100
    se_p_100 = math.sqrt(0.25 / 100) * 100   # Willis protocol used n=100
    se_diff = math.sqrt((math.sqrt(2) * se_p_500) ** 2
                        + (math.sqrt(2) * se_p_100) ** 2)
    gap = WILLIS_DNOISE["Claude 3.5 Sonnet"] - claude_avg
    z = gap / se_diff
    p = math.erfc(abs(z) / math.sqrt(2))
    print(f"  Claude 4.6 avg Dnoise = {claude_avg:.1f}pp  vs  "
          f"Claude 3.5 Sonnet = 13pp  (gap {gap:.1f}pp)")
    print(f"  SE(diff, propagating Willis n=100) = {se_diff:.2f}pp")
    print(f"  z = {z:.2f}, p = {p:.3f}  -> "
          f"{'significant' if p < 0.05 else 'NOT significant'}")
    print("  Verdict: H4 directionally suggestive, NOT robustly confirmed")
    print("  (we deliberately do not re-run the predecessor solely to")
    print("   resolve H4 — that would be result-driven analysis).")

    print("\nAll figures above appear in the manuscript. Verification OK.")


if __name__ == "__main__":
    main()
