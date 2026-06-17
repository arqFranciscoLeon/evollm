"""Converter-robustness check (Paper 2, sec 4.7), step 2/2.

Runs the Moran process (balanced 4:4:4, clean, n=500) for the 12 HYBRID
libraries produced by reconvert_robust.py — identical to the GPT-5.4 Mini
libraries except that a random 10% of strategies were re-converted with a
second, ecosystem-different converter (DeepSeek V4). Comparing the resulting
equilibria to the GPT pipeline tests converter-invariance.

Only the balanced clean condition is run (the condition that carries H5/H6).
Wave-based with checkpoints, like modal_moran_waves.py.

    modal run modal_moran_robust.py
    modal run modal_moran_robust.py --resume
"""
import modal
from pathlib import Path
import json
import os
from datetime import datetime
from collections import defaultdict

TOTAL_ITERATIONS = 500
BATCH_SIZE = 1
WAVE_SIZE = 200
CPUS_PER_JOB = 1
TIMEOUT_SECONDS = 3600

ROBUST_LIBS = [
    f"{base}_{p}_75_robust"
    for base in ("deepseek_v4pro", "qwen3max", "kimi_k25", "glm_51")
    for p in ("default", "prose", "refine")
]
POP_BALANCED = [4, 4, 4]
CHECKPOINT_FILE = "results/robust_moran_checkpoint.json"

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("axelrod==4.14.0", "numpy", "matplotlib")
    .add_local_dir("src",        remote_path="/root/evollm/src")
    .add_local_dir("strategies", remote_path="/root/evollm/strategies")
)
app = modal.App("evollm-moran-robust", image=image)


@app.function(cpu=CPUS_PER_JOB, timeout=TIMEOUT_SECONDS, retries=2)
def run_batch(algo_name: str, initial_pop: list, batch_size: int, task_id: str) -> dict:
    import sys, os, subprocess, ast as _ast
    workdir = "/root/evollm"
    script = f"{workdir}/src/evollm/moran_process.py"
    cmd = [
        sys.executable, script,
        "--algo", f"{workdir}/strategies/{algo_name}",
        "--initial_pop", str(initial_pop[0]), str(initial_pop[1]), str(initial_pop[2]),
        "--iterations", str(batch_size),
        "--processes", "1",
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{workdir}/src"
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=workdir, env=env)
    if proc.returncode != 0:
        raise RuntimeError(f"moran failed for {algo_name} task={task_id}: {proc.stderr[-500:]}")

    attitudes = ["Aggressive", "Cooperative", "Neutral"]
    counts = {"Aggressive": 0, "Cooperative": 0, "Neutral": 0}
    for line in reversed(proc.stdout.splitlines()):
        line = line.strip()
        if line.startswith("{") and any(att in line for att in attitudes):
            try:
                raw = _ast.literal_eval(line)
                tmp = {"Aggressive": 0, "Cooperative": 0, "Neutral": 0}
                for name, count in raw.items():
                    for att in attitudes:
                        if att in name:
                            tmp[att] += count
                            break
                if sum(tmp.values()) > 0:
                    counts = tmp
                    break
            except Exception:
                continue
    return {"task_id": task_id, "algo": algo_name, "pop": tuple(initial_pop),
            "batch_size": batch_size, **counts}


@app.local_entrypoint()
def main(total_iterations: int = TOTAL_ITERATIONS, batch_size: int = BATCH_SIZE,
         wave_size: int = WAVE_SIZE, resume: bool = False):
    n_batches = total_iterations // batch_size
    all_tasks = []
    for algo in ROBUST_LIBS:
        for b in range(n_batches):
            all_tasks.append((algo, POP_BALANCED, batch_size, f"{algo}|4_4_4|b{b:03d}"))
    total_tasks = len(all_tasks)

    checkpoint = {"completed_task_ids": [], "aggregated": {}}
    if resume and os.path.exists(CHECKPOINT_FILE):
        checkpoint = json.load(open(CHECKPOINT_FILE))
        print(f"[RESUME] {len(checkpoint['completed_task_ids'])} done")
    done = set(checkpoint["completed_task_ids"])
    pending = [t for t in all_tasks if t[3] not in done]
    agg = defaultdict(lambda: {"Aggressive": 0, "Cooperative": 0, "Neutral": 0, "n_iter": 0})
    for k, v in checkpoint["aggregated"].items():
        agg[k] = v

    print(f"Robust check: {len(ROBUST_LIBS)} libs x 4:4:4 x {total_iterations} = "
          f"{total_tasks} tasks; pending {len(pending)}; "
          f"~${total_tasks*5*0.0003:.2f}")

    n_waves = (len(pending) + wave_size - 1) // wave_size
    for wi in range(0, len(pending), wave_size):
        wave = pending[wi:wi + wave_size]
        print(f"--- wave {wi//wave_size+1}/{n_waves}: {len(wave)} tasks ---", flush=True)
        results = list(run_batch.starmap(wave))
        for r in results:
            if not isinstance(r, dict):
                continue
            key = f"{r['algo']}__4_4_4"
            agg[key]["Aggressive"] += r["Aggressive"]
            agg[key]["Cooperative"] += r["Cooperative"]
            agg[key]["Neutral"] += r["Neutral"]
            agg[key]["n_iter"] += r["batch_size"]
            checkpoint["completed_task_ids"].append(r["task_id"])
        checkpoint["aggregated"] = {k: dict(v) for k, v in agg.items()}
        Path("results").mkdir(exist_ok=True)
        json.dump(checkpoint, open(CHECKPOINT_FILE, "w"), indent=2, default=str)
        print(f"  total {len(checkpoint['completed_task_ids'])}/{total_tasks}", flush=True)

    # final
    final = []
    for key, c in agg.items():
        algo = key.split("__")[0]
        tot = c["Aggressive"] + c["Cooperative"] + c["Neutral"]
        final.append({
            "algo": algo, "iteraciones": c["n_iter"],
            "pop_agresivos": 4, "pop_cooperativos": 4, "pop_neutrales": 4,
            "Aggressive": c["Aggressive"], "Cooperative": c["Cooperative"], "Neutral": c["Neutral"],
            "pct_Aggressive": round(100*c["Aggressive"]/tot, 2) if tot else 0,
            "pct_Cooperative": round(100*c["Cooperative"]/tot, 2) if tot else 0,
            "pct_Neutral": round(100*c["Neutral"]/tot, 2) if tot else 0,
        })
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outp = Path(f"results/robust_moran_final_{ts}.json")
    json.dump(final, open(outp, "w", encoding="utf8"), indent=2)
    print(f"\n[DONE] {len(final)} robust cells -> {outp}")
    for r in sorted(final, key=lambda x: x["algo"]):
        print(f"  {r['algo']:<32} {r['pct_Aggressive']:>5}/{r['pct_Cooperative']:>5}/{r['pct_Neutral']:>5}")
