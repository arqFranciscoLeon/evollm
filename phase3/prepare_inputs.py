"""Snapshot committed strategy inputs without changing any published library."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

from phase3.audit_inputs import MODELS, audit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phase3" / "inputs"
WESTERN_COMMIT = "3a63515"
CHINESE_COMMIT = "759b7b0"


def blob(commit, path):
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)


def save_identical(path, data):
    if path.exists() and path.read_bytes() != data:
        raise ValueError(f"Refusing to replace a different snapshot: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def main():
    libraries = []
    for k, (model, lab) in enumerate(MODELS.items()):
        commit = WESTERN_COMMIT if k < 4 else CHINESE_COMMIT
        full_commit = subprocess.check_output(["git", "rev-parse", commit], cwd=ROOT, text=True).strip()
        for prompt in ("default", "prose", "refine"):
            filename = f"{model}_{prompt}_75.py"
            target = OUT / "archived" / filename
            data = blob(commit, f"strategies/{filename}")
            save_identical(target, data)
            inventory = audit(target)
            if not inventory["structure_pass"]:
                raise ValueError(f"Incomplete committed input: {filename}")
            source = data.decode("utf-8-sig")
            nodes = {n.name: n for n in ast.parse(source).body if isinstance(n, ast.ClassDef)}
            for record in inventory["strategies"]:
                cls = nodes[record["class"]]
                methods = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
                # AST excludes comments/whitespace; do not treat it as behavioral equivalence.
                record["methods_sha256"] = hashlib.sha256(
                    repr([ast.dump(n, include_attributes=False) for n in methods]).encode()).hexdigest()
                record["id"] = f"{model}/{prompt}/{record['class']}"
            inventory.update(model=model, lab=lab, prompt=prompt, source_commit=full_commit,
                             source_path=f"strategies/{filename}", filename=filename,
                             snapshot_path=str(target.relative_to(ROOT)).replace('\\', '/'))
            libraries.append(inventory)
    support = []
    for filename in ("__init__.py", "common.py"):
        data = blob(CHINESE_COMMIT, f"src/evollm/{filename}")
        target = OUT / "support" / "evollm" / filename
        save_identical(target, data)
        support.append({"path": str(target.relative_to(ROOT)).replace('\\', '/'),
                        "sha256": hashlib.sha256(data).hexdigest(), "commit": CHINESE_COMMIT})
    manifest = {"schema": 1, "status": "archival_snapshot_not_converted",
                "ready_for_tournament": False,
                "open_gates": ["archived prose completeness", "fixed conversion of Western libraries",
                               "strict runtime validation", "protocol and analysis freeze"],
                "libraries": libraries, "support": support}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding="utf-8")
    print(f"Snapshot: {len(libraries)} libraries, {sum(x['classes'] for x in libraries)} strategies.")
    print("No conversion or tournament was performed. Manifest remains NOT READY.")


if __name__ == "__main__":
    main()
