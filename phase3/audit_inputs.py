"""Static, API-free inventory of archived Phase 3 inputs; not runtime validation."""
import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

MODELS = {
    "anthropic_sonnet46": "Anthropic",
    "gemini_25_flash": "Google",
    "gemini_31_pro": "Google",
    "openai_gpt54mini": "OpenAI",
    "deepseek_v4pro": "DeepSeek",
    "qwen3max": "Alibaba",
    "kimi_k25": "Moonshot",
    "glm_51": "Z.ai",
}
ATTITUDES = ("Aggressive", "Cooperative", "Neutral")


def audit(path):
    data = path.read_bytes()
    source = data.decode("utf-8-sig")
    lines = source.splitlines()
    report = {"path": str(path.resolve()), "sha256": hashlib.sha256(data).hexdigest()}
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return {**report, "syntax_error": str(exc), "structure_pass": False}
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)
               and any(isinstance(b, ast.Name) and b.id == "LLM_Strategy" for b in n.bases)]
    records = []
    for cls in classes:
        index = cls.lineno - 2
        comments = []
        while index >= 0:
            line = lines[index].strip()
            if line.startswith("#"):
                comments.append(line[1:].strip())
            elif line:
                break
            index -= 1
        prose = " ".join(reversed(comments)).strip()
        flags = []
        if not prose:
            flags.append("missing_prose")
        # These are triage heuristics only; concise or list-ending prose can be valid.
        if prose and len(prose.split()) < 40:
            flags.append("short_prose_manual_review")
        ending = prose.rstrip(" *_'\"`)")
        if ending and ending[-1] not in ".!?:;":
            flags.append("unfinished_ending_manual_review")
        records.append({"class": cls.name, "line": cls.lineno,
                        "words": len(prose.split()), "prose_sha256": hashlib.sha256(prose.encode()).hexdigest(),
                        "prose_tail": prose[-160:], "flags": flags})
    names = [c.name for c in classes]
    expected = {f"{a}_{i}" for a in ATTITUDES for i in range(1, 26)}
    counts = Counter(name.split("_")[0] for name in names)
    return {**report, "classes": len(classes), "attitudes": dict(counts),
            "structure_pass": len(names) == 75 and set(names) == expected,
            "missing_classes": sorted(expected - set(names)),
            "duplicate_classes": sorted(k for k, v in Counter(names).items() if v > 1),
            "prose_flags": sum(bool(r["flags"]) for r in records), "strategies": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--compare-root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    libraries = []
    for model, lab in MODELS.items():
        for prompt in ("default", "prose", "refine"):
            name = f"{model}_{prompt}_75.py"
            path = args.root / "strategies" / name
            entry = {"model": model, "lab": lab, "prompt": prompt, "filename": name}
            entry.update(audit(path) if path.exists() else {"missing_file": True, "structure_pass": False})
            if args.compare_root:
                other = args.compare_root / "strategies" / name
                if other.exists():
                    compared = audit(other)
                    entry["comparison"] = {k: compared.get(k) for k in
                                           ("path", "sha256", "classes", "structure_pass", "prose_flags")}
                    entry["comparison"]["same_bytes"] = compared["sha256"] == entry.get("sha256")
            libraries.append(entry)
    result = {"purpose": "Static inventory only. No imports of generated strategies, API calls or matches.",
              "caution": "Prose flags require human inspection; a structural pass does not establish fidelity or runtime safety.",
              "models": len(MODELS), "labs": len(set(MODELS.values())), "libraries": libraries}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for item in libraries:
        print(f"{item['filename']}: classes={item.get('classes', 0)}, structure={item['structure_pass']}, prose_flags={item.get('prose_flags', 0)}")
    print(f"Inventory written: {args.output.resolve()}")


if __name__ == "__main__":
    main()
