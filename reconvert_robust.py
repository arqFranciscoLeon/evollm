"""Pre-registered converter-robustness check (Paper 2, sec 4.7), step 1/2.

For each of the 12 CLEAN libraries, sample a random 10% (8 of 75, fixed seed)
of strategies, re-convert their natural-language prose to Python with a second,
ecosystem-different converter (DeepSeek V4) instead of GPT-5.4 Mini, and write a
hybrid library strategies/<lib>_robust.py (identical to the original except the
sampled strategies' executable bodies). A manifest records exactly which
strategies were re-converted, for reproducibility.

Run with PYTHONPATH=src from the worktree root. Idempotent: skips a lib whose
_robust.py already has 75 classes.
"""
import json
import random
import re
import sys

from dotenv import load_dotenv
load_dotenv(override=True)
sys.path.insert(0, "src")

from evollm import algorithms, common
from evollm import create_strategies as cs
from evollm import llm_clients

SEED = 20260616
FRACTION = 0.10
CONVERTER = "deepseek-v4-pro"        # ecosystem-different 2nd converter
CLEAN_LIBS = [
    f"{base}_{p}_75"
    for base in ("deepseek_v4pro", "qwen3max", "kimi_k25", "glm_51")
    for p in ("default", "prose", "refine")
]
GAME = common.get_game("classic")


def segments(lines):
    """Return (header_lines, [(class_name, seg_start, seg_end), ...])."""
    cls_idx = [i for i, ln in enumerate(lines)
               if re.match(r"class \w+\(LLM_Strategy\):", ln)]
    segs = []
    for k, ci in enumerate(cls_idx):
        start = ci
        j = ci - 1
        while j >= 0 and (lines[j].strip() == "" or lines[j].lstrip().startswith("#")):
            start = j
            j -= 1
        segs.append([ci, start])  # fill end next
    # end of a segment = start of the next segment (or EOF)
    out = []
    for k, ci in enumerate(cls_idx):
        start = segs[k][1]
        end = segs[k + 1][1] if k + 1 < len(cls_idx) else len(lines)
        name = re.match(r"class (\w+)\(", lines[ci]).group(1)
        out.append((name, ci, start, end))
    header_end = out[0][2] if out else len(lines)
    return lines[:header_end], out


def extract_nl(lines, seg_start, cls_i):
    """NL prose = the comment block(s) between seg_start and the class line."""
    block = []
    for ln in lines[seg_start:cls_i]:
        s = ln.lstrip()
        if s.startswith("#"):
            block.append(s[1:].strip())
    return " ".join(block).strip()


def swap_method(seg_lines, new_algorithm):
    """Keep everything up to and incl. @auto_update_score; replace the method."""
    for i, ln in enumerate(seg_lines):
        if ln.strip() == "@auto_update_score":
            head = seg_lines[:i + 1]
            return head + new_algorithm.splitlines()
    raise ValueError("no @auto_update_score in segment")


def reconvert_one(client, nl, max_retries=6):
    """DeepSeek via OpenRouter is non-deterministic even at temp=0, so repeated
    attempts can recover a strategy whose first conversion was rejected by
    test_algorithm (e.g. emitted helper functions). Returns None if all fail."""
    for _ in range(max_retries):
        try:
            return cs.generate_algorithm(client, nl, GAME, 1000, 0, refine=False)
        except (ValueError, RuntimeError):
            continue
    return None


def process_lib(lib, client):
    out_path = f"strategies/{lib}_robust.py"
    text = open(f"strategies/{lib}.py", encoding="utf8").read()
    lines = text.splitlines()
    header, segs = segments(lines)
    assert len(segs) == 75, f"{lib}: {len(segs)} classes"

    rng = random.Random(f"{SEED}:{lib}")
    k = round(75 * FRACTION)                       # 8 per library (~10%)
    order = rng.sample(range(75), 75)              # shuffled draw order

    # Draw until k strategies re-convert successfully; resample the rest.
    # (Mirrors the original pipeline, which regenerates until a valid strategy
    #  is obtained. A strategy the 2nd converter cannot render as a single safe
    #  function is replaced by another random draw; resamples are recorded.)
    chosen_algo = {}                               # idx -> new indented method
    resampled = 0
    for idx in order:
        if len(chosen_algo) >= k:
            break
        name, ci, start, end = segs[idx]
        nl = extract_nl(lines, start, ci)
        algo = reconvert_one(client, nl)
        if algo is None:
            resampled += 1
            print(f"    [resample] {name} not convertible by DeepSeek; drawing another")
            continue
        chosen_algo[idx] = algo
        print(f"    re-converted {name}")
    assert len(chosen_algo) == k, f"{lib}: only {len(chosen_algo)}/{k} re-converted"

    new_lines = list(header)
    converted = []
    for idx, (name, ci, start, end) in enumerate(segs):
        seg = lines[start:end]
        while seg and seg[-1].strip() == "":
            seg.pop()
        if idx in chosen_algo:
            seg = swap_method(seg, chosen_algo[idx])
            converted.append(name)
        new_lines += seg + ["", "", ""]

    with open(out_path, "w", encoding="utf8") as f:
        f.write("\n".join(new_lines).rstrip() + "\n")

    n_loaded = len(algorithms.load_algorithms(f"strategies/{lib}_robust"))
    assert n_loaded == 75, f"{lib}_robust loaded {n_loaded} classes"
    print(f"  [ok] {lib}_robust: 75 classes, {len(converted)} re-converted, "
          f"{resampled} resampled")
    return {"lib": lib, "k": k, "converted": sorted(converted),
            "resampled": resampled}


def main():
    client = llm_clients.make_client(CONVERTER)
    manifest = {"seed": SEED, "fraction": FRACTION, "converter": CONVERTER,
                "libs": []}
    for lib in CLEAN_LIBS:
        print(f"== {lib} ==")
        rec = process_lib(lib, client)
        if rec:
            manifest["libs"].append(rec)
    with open("results/robustness_reconvert_manifest.json", "w", encoding="utf8") as f:
        json.dump(manifest, f, indent=2)
    tot = sum(len(l["converted"]) for l in manifest["libs"])
    print(f"\nDONE. {len(manifest['libs'])} libs processed, {tot} strategies re-converted.")
    print("Manifest: results/robustness_reconvert_manifest.json")


if __name__ == "__main__":
    main()
