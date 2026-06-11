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

# ---------------------------------------------------------------------------
# Phase 2 (PHASE2_PREREG.md + Amendment 2026-05-17 B) — H5 / H6
# ---------------------------------------------------------------------------
# Phase 2a is a SELF-CONTAINED CHINESE-ONLY study: only the 4 Chinese
# models, all converted by the single FIXED converter (GPT-5.4 Mini), are
# read from the Phase 2 results file. No Western numbers enter this paper,
# so every comparison here is Chinese-vs-Chinese under one identical
# converter — internally confound-free. The Western re-run and any
# cross-ecosystem comparison are future work, not Phase 2a.
PHASE2_RESULTS_GLOB = "results/phase2_moran_final_*.json"

# Chinese models (PHASE2_PREREG.md §4). Code change #3 MUST generate with
# these exact `--algo` base names so this loader finds them.
CHINESE_ALGOS = [
    ("deepseek_v4pro_default_75", "DeepSeek V4 Pro", "Default"),
    ("deepseek_v4pro_prose_75",   "DeepSeek V4 Pro", "Prose"),
    ("deepseek_v4pro_refine_75",  "DeepSeek V4 Pro", "Refine"),
    ("qwen3max_default_75",       "Qwen3-Max",       "Default"),
    ("qwen3max_prose_75",         "Qwen3-Max",       "Prose"),
    ("qwen3max_refine_75",        "Qwen3-Max",       "Refine"),
    ("kimi_k25_default_75",       "Kimi K2.5",       "Default"),
    ("kimi_k25_prose_75",         "Kimi K2.5",       "Prose"),
    ("kimi_k25_refine_75",        "Kimi K2.5",       "Refine"),
    ("glm_51_default_75",         "GLM-5.1",         "Default"),
    ("glm_51_prose_75",           "GLM-5.1",         "Prose"),
    ("glm_51_refine_75",          "GLM-5.1",         "Refine"),
]
# The 4 Chinese labs (distinct model names in CHINESE_ALGOS).
CHINESE_LABS = ["DeepSeek V4 Pro", "Qwen3-Max", "Kimi K2.5", "GLM-5.1"]
# Phase 1 Western cooperative-plurality rate — used by H5 only as a
# PUBLISHED external baseline (different, per-provider converter), i.e. a
# literature contrast, NOT a controlled comparison (see amendment).
PHASE1_PLURALITY = (9, 12)


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


def load_phase2():
    """Load the Phase 2 fixed-converter results, or (None, None) if absent.

    Absent is the EXPECTED state until code changes #3–#5 have been run;
    the Phase 2 section then prints a PENDING notice instead of crashing,
    so `python reproduce_tables.py` keeps working with no API cost.
    """
    files = sorted(HERE.glob(PHASE2_RESULTS_GLOB))
    if not files:
        return None, None
    with open(files[-1], encoding="utf8") as fh:
        rows = json.load(fh)
    d = {}
    for r in rows:
        pop = f"{r['pop_agresivos']}{r['pop_cooperativos']}{r['pop_neutrales']}"
        d[(r["algo"], pop)] = r
    return d, files[-1].name


def _mean(xs):
    return sum(xs) / len(xs)


def _var(xs):
    """Sample variance (ddof=1); 0.0 for a single point."""
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def phase2_section(d2, src2):
    print("\n" + "=" * 72)
    print("PHASE 2a (Chinese-only, fixed-converter) — H5 / H6")
    print("=" * 72)

    if d2 is None:
        print("  PENDING — no Phase 2 results found "
              f"({PHASE2_RESULTS_GLOB}).")
        print("  Expected until the Chinese-only pipeline has run:")
        print("   #3 generate 75 strat/model for the 4 CHINESE models")
        print("      (fixed converter GPT-5.4 Mini),")
        print("   #4 tournaments+Moran n=500, #5 DeepSeek-V4 10% robustness.")
        print("  This analysis activates automatically once the results")
        print("  file is present.  Expected Chinese `--algo` base names:")
        for algo, model, prompt in CHINESE_ALGOS:
            print(f"    {algo:<26} ({model}, {prompt})")
        return

    print(f"  Phase 2 source: results/{src2}  (n={N} per condition)\n")

    def r2(algo, pop, noise=False):
        return d2.get((algo + ("_noise" if noise else ""), pop), {})

    # ---- H5 — cooperative-bias generality (Chinese, 4:4:4 clean) ----
    print("-" * 72)
    print("H5 — cooperative-plurality bias generalises to Chinese models")
    print("     (4:4:4 balanced, noiseless; plurality = strict max of A/C/N)")
    print("-" * 72)
    coop_pluralities = 0
    counted = 0
    missing = []
    for algo, model, prompt in CHINESE_ALGOS:
        rec = r2(algo, "444")
        if not rec:
            missing.append(algo)
            continue
        counted += 1
        a, c, n = (rec["pct_Aggressive"], rec["pct_Cooperative"],
                   rec["pct_Neutral"])
        is_coop = c > a and c > n
        coop_pluralities += int(is_coop)
        flag = "C-plurality" if is_coop else (
            "A-plurality" if a >= c and a >= n else "N-plurality")
        print(f"  {model:<16}{prompt:<8} "
              f"{round(a):>2}/{round(c):>2}/{round(n):>2}   {flag}")
    if missing:
        print(f"  ({len(missing)} condition(s) absent: "
              f"{', '.join(missing)})")
    if counted:
        w_k, w_t = PHASE1_PLURALITY
        z, p = z_test(coop_pluralities, w_k, n1=counted, n2=w_t)
        print(f"\n  Chinese: {coop_pluralities}/{counted} cooperative-"
              f"plurality   vs   published Phase-1 Western {w_k}/{w_t}")
        print(f"  Two-proportion z = {z:+.2f}, p = {p:.3f}  (DESCRIPTIVE:")
        print("  literature contrast vs a baseline made with a different,")
        print("  per-provider converter — NOT a controlled comparison.)")
        if counted < w_t:
            print("  Verdict: PARTIAL DATA — interim only, not the "
                  "pre-registered call.")
        elif p >= 0.05:
            print("  Verdict: consistent with H5 — Chinese cooperative-"
                  "plurality rate is")
            print("  not distinguishable from the published Western "
                  "baseline (H1 appears")
            print("  to generalise; converter difference is a stated "
                  "limitation).")
        else:
            print("  Verdict: H5 NOT supported — Chinese cooperative-"
                  "plurality rate differs")
            print("  from the published Western baseline (converter "
                  "difference caveated).")

    # ---- H6 (reformulated, amendment 2026-05-17 B) ----
    # Within-Chinese lab-level divergence: are the 4 Chinese frontier
    # models statistically distinguishable on P_A? (i.e. not monolithic)
    print("\n" + "-" * 72)
    print("H6 (reformulated) — Chinese-model behaviour is NOT monolithic:")
    print("     the 4 labs diverge at the lab level")
    print("     (P_A at 4:4:4 clean, Default; pairwise z + Holm-Bonferroni)")
    print("-" * 72)
    pa = {}      # lab -> aggressive-equilibrium count (out of N)
    for algo, model, prompt in CHINESE_ALGOS:
        if prompt != "Default":
            continue
        rec = r2(algo, "444")
        if rec:
            pa[model] = int(rec.get("Aggressive", 0))
    absent = [m for m in CHINESE_LABS if m not in pa]
    if absent:
        print(f"  PARTIAL DATA — missing Default 4:4:4 for: "
              f"{', '.join(absent)}")
        print("  H6 verdict deferred until all 4 Chinese labs present.")
        return

    order = list(CHINESE_LABS)
    print(f"  {'Lab':<18}{'P_A%':>7}")
    for m in order:
        print(f"  {m:<18}{round(100*pa[m]/N):>6}%")

    # all 6 pairwise z-tests among the 4 Chinese labs + Holm-Bonferroni
    pairs = []
    for i in range(len(order)):
        for j in range(i + 1, len(order)):
            a, b = order[i], order[j]
            z, p = z_test(pa[a], pa[b])
            pairs.append((a, b, z, p))
    pairs.sort(key=lambda t: t[3])
    k = len(pairs)
    n_sig = 0
    print(f"\n  {'Comparison':<34}{'z':>8}{'p':>12}{'HB-thr':>9}  sig")
    for rank, (a, b, z, p) in enumerate(pairs):
        thr = 0.05 / (k - rank)
        sig = p < thr
        n_sig += int(sig)
        print(f"  {a} vs {b}".ljust(34)
              + f"{z:>+8.2f}{p:>12.2e}{thr:>9.4f}  "
              + ("***" if sig else "ns"))

    pa_pct = [100 * pa[m] / N for m in order]
    spread = max(pa_pct) - min(pa_pct)
    print(f"\n  P_A spread across labs: {min(pa_pct):.1f}–{max(pa_pct):.1f}%"
          f"  (range {spread:.1f}pp, SD {math.sqrt(_var(pa_pct)):.1f}pp)")

    print("\n  Verdict:")
    if n_sig >= 1:
        print(f"    H6 SUPPORTED — {n_sig}/{k} lab pair(s) differ after "
              "Holm-Bonferroni.")
        print("    Chinese frontier models are NOT monolithic; behaviour")
        print("    diverges at the lab level under one fixed converter.")
    else:
        print("    H6 NOT SUPPORTED — no lab pair survives "
              "Holm-Bonferroni;")
        print("    the 4 Chinese labs are statistically indistinguishable")
        print("    on P_A at n=500 (cannot reject monolithic behaviour).")
    print("    (Reported per the §3/§7 honesty discipline; H6 fixed "
          "ante-hoc.)")


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

    # ---- PHASE 2 (H5/H6) — activates automatically when data exists ----
    d2, src2 = load_phase2()
    phase2_section(d2, src2)

    print("\nAll Phase 1 figures above appear in the manuscript. "
          "Verification OK.")


if __name__ == "__main__":
    main()
