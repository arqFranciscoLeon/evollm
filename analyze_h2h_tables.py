"""Compute the three H2H-derived Phase-2 tables (cooperation propensity,
payoffs+ICD, diversity) from results/*_matrices.txt, mirroring Paper 1.

Metrics (Paper 1 definitions):
  ICD        = mean(Aggressive payoff row) / mean(Cooperative payoff row)
  Separation = mean(Cooperative coop row) - mean(Aggressive coop row)
  H          = mean over the 3 attitudes of the Shannon entropy (nats) of
               the 25 per-strategy cooperation-rate values, binned into 10
               equal bins on [0,1].

Validates against Paper 1 published values first, then prints the Chinese
tables. Run with PYTHONPATH=src from the worktree root.
"""
import math
import re
import sys

ATT = ["Aggressive", "Cooperative", "Neutral"]


def parse_matrix(lines, header):
    """Parse a 3x3 attitude matrix that follows a header line like
    'Normalised cooperation:' / 'Payoffs:'. Returns {row_att: [vsA, vsC, vsN]}."""
    i = next(k for k, ln in enumerate(lines) if ln.strip().startswith(header))
    # the next line is the column header (Aggressive Cooperative Neutral),
    # then an 'index' line, then 3 data rows
    rows = {}
    k = i + 1
    found = 0
    while found < 3 and k < len(lines):
        toks = lines[k].split()
        if toks and toks[0] in ATT:
            rows[toks[0]] = [float(x) for x in toks[1:4]]
            found += 1
        k += 1
    assert len(rows) == 3, f"{header}: parsed {len(rows)} rows"
    return rows


def parse_summary(lines):
    """Return {attitude: [coop_rating, ...]} from the Results Summary block."""
    i = next(k for k, ln in enumerate(lines) if ln.strip().startswith("Results Summary"))
    out = {a: [] for a in ATT}
    for ln in lines[i + 1:]:
        toks = ln.split()
        # data row: rank Name Median_score Cooperation_rating ...
        if len(toks) >= 4 and re.fullmatch(r"\d+", toks[0]):
            name = toks[1]
            att = name.split("_")[0]
            if att in out:
                out[att].append(float(toks[3]))
    for a in ATT:
        assert len(out[a]) == 25, f"{a}: {len(out[a])} strategies (expected 25)"
    return out


def shannon_entropy(values, nbins=10):
    counts = [0] * nbins
    for v in values:
        b = min(int(v * nbins), nbins - 1)  # v==1.0 -> last bin
        b = max(b, 0)
        counts[b] += 1
    n = len(values)
    h = 0.0
    for c in counts:
        if c:
            p = c / n
            h -= p * math.log(p)
    return h


def metrics(path):
    with open(path, encoding="utf8") as f:
        lines = f.readlines()
    coop = parse_matrix(lines, "Normalised cooperation")
    pay = parse_matrix(lines, "Payoffs")
    summ = parse_summary(lines)

    mean = lambda xs: sum(xs) / len(xs)
    icd = mean(pay["Aggressive"]) / mean(pay["Cooperative"])
    sep = mean(coop["Cooperative"]) - mean(coop["Aggressive"])
    h = mean([shannon_entropy(summ[a]) for a in ATT])
    return {"coop": coop, "pay": pay, "icd": icd, "sep": sep, "H": h}


def fmt3(xs):
    return " & ".join(f"{x:.3f}" for x in xs)


# ── Validation against Paper 1 published values ──────────────────────────────
PAPER1 = {
    "anthropic_sonnet46_default_75": ("Claude 4.6 Default", dict(icd=0.605, sep=0.56)),
    "gemini_31_pro_default_75":      ("G3.1 Pro Default", dict(icd=0.809, sep=0.32, H=0.65)),
    "gemini_31_pro_refine_75":       ("G3.1 Pro Refine", dict(icd=0.925, sep=0.17, H=1.69)),
    "openai_gpt54mini_default_75":   ("GPT Default", dict(icd=0.454, sep=0.63)),
}


def validate():
    print("=" * 70)
    print("VALIDATION vs Paper 1 (must match published table values)")
    print("=" * 70)
    for algo, (label, expect) in PAPER1.items():
        try:
            m = metrics(f"results/{algo}_matrices.txt")
        except (StopIteration, FileNotFoundError, AssertionError) as e:
            print(f"  {label}: SKIP ({e})")
            continue
        line = f"  {label:<20} ICD={m['icd']:.3f}(exp {expect.get('icd','?')})  Sep={m['sep']:.2f}(exp {expect.get('sep','?')})"
        if "H" in expect:
            line += f"  H={m['H']:.2f}(exp {expect['H']})"
        print(line)


CHINESE = [
    ("DeepSeek V4 Pro", "deepseek_v4pro"),
    ("Qwen3-Max", "qwen3max"),
    ("Kimi K2.5", "kimi_k25"),
    ("GLM-5.1", "glm_51"),
]
PROMPTS = ["default", "prose", "refine"]


def chinese_tables():
    M = {}
    for _, base in CHINESE:
        for p in PROMPTS:
            M[(base, p)] = metrics(f"results/{base}_{p}_75_matrices.txt")

    print("\n" + "=" * 70)
    print("TABLE A — Cooperation propensity (Default, clean)")
    print("=" * 70)
    for label, base in CHINESE:
        m = M[(base, "default")]
        print(f"{label}")
        for a in ATT:
            print(f"  {a[0]} & {fmt3(m['coop'][a])} \\\\")

    print("\n" + "=" * 70)
    print("TABLE B — Payoffs + ICD (all prompts, clean)")
    print("=" * 70)
    print("Lab Prompt | Agg vsA/C/N | Coop vsA/C/N | ICD")
    for label, base in CHINESE:
        for p in PROMPTS:
            m = M[(base, p)]
            print(f"  {label:<16} {p:<8} {fmt3(m['pay']['Aggressive'])}  |  "
                  f"{fmt3(m['pay']['Cooperative'])}  |  {m['icd']:.3f}")

    print("\n" + "=" * 70)
    print("TABLE C — Diversity (H nats, Separation), clean")
    print("=" * 70)
    avg_sep = {}
    for label, base in CHINESE:
        seps = []
        for p in PROMPTS:
            m = M[(base, p)]
            print(f"  {label:<16} {p:<8} H={m['H']:.2f}  Sep={m['sep']:.2f}")
            seps.append(m["sep"])
        avg_sep[label] = sum(seps) / len(seps)
    print("  --- avg separation per lab ---")
    for label in avg_sep:
        print(f"    {label:<16} {avg_sep[label]:.2f}")


if __name__ == "__main__":
    validate()
    chinese_tables()
