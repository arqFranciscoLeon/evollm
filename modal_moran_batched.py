"""
Modal deployment para simulaciones Moran EvoLLM — VERSIÓN BATCHED
==================================================================
Lanza 2400 tareas pequeñas en paralelo (48 condiciones × 50 batches de 10 iter).
Cada batch tarda ~3min — completa antes de cualquier preemption.

USO:
    modal run modal_moran_batched.py
    modal run modal_moran_batched.py --batch-size 10 --total-iterations 500
    modal run modal_moran_batched.py --conditions 4    # solo balanced
    modal run modal_moran_batched.py --conditions 8    # solo biased

RESULTADO:
    results/moran_history.csv  (1 fila agregada por condición)
    results/modal_batched_run_TIMESTAMP.json
"""

import modal
from pathlib import Path
import csv
import json
from datetime import datetime
from collections import defaultdict

# ── Configuración ────────────────────────────────────────────────────────────

TOTAL_ITERATIONS = 500     # Objetivo del paper
BATCH_SIZE = 2             # iteraciones por batch (~10 min cada uno, safe vs preemption)
CPUS_PER_JOB = 1
TIMEOUT_SECONDS = 1800     # 30 min por batch (margen MUY amplio sobre los ~10 min esperados)

ALGOS_CLEAN = [
    "anthropic_sonnet46_default_75",
    "anthropic_sonnet46_prose_75",
    "anthropic_sonnet46_refine_75",
    "gemini_25_flash_default_75",
    "gemini_25_flash_prose_75",
    "gemini_25_flash_refine_75",
    "gemini_31_pro_default_75",
    "gemini_31_pro_prose_75",
    "gemini_31_pro_refine_75",
    "openai_gpt54mini_default_75",
    "openai_gpt54mini_prose_75",
    "openai_gpt54mini_refine_75",
]
ALGOS_NOISE = [a + "_noise" for a in ALGOS_CLEAN]

POP_BALANCED = [4, 4, 4]
POP_BIASED   = [8, 2, 2]

# ── Imagen Modal ──────────────────────────────────────────────────────────────

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "axelrod==4.14.0",
        "numpy",
        "matplotlib",
    )
    .add_local_dir("src",        remote_path="/root/evollm/src")
    .add_local_dir("strategies", remote_path="/root/evollm/strategies")
)

app = modal.App(
    "evollm-moran-batched",
    image=image,
)

# ── Función: un batch pequeño ─────────────────────────────────────────────────

@app.function(
    cpu=CPUS_PER_JOB,
    timeout=TIMEOUT_SECONDS,
    retries=2,
)
def run_batch(algo_name: str, initial_pop: list, batch_size: int, batch_idx: int) -> dict:
    """Corre un BATCH pequeño (batch_size iteraciones) de UNA condición."""
    import sys, os, subprocess, ast as _ast
    from datetime import datetime

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

    proc = subprocess.run(
        cmd, capture_output=True, text=True, cwd=workdir, env=env,
    )

    if proc.returncode != 0:
        raise RuntimeError(
            f"moran_process failed for {algo_name} batch={batch_idx}: "
            f"{proc.stderr[-500:]}"
        )

    # Parsear el dict final del stdout
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

    return {
        "algo": algo_name,
        "pop": tuple(initial_pop),
        "batch_idx": batch_idx,
        "batch_size": batch_size,
        "Aggressive": counts["Aggressive"],
        "Cooperative": counts["Cooperative"],
        "Neutral": counts["Neutral"],
    }


# ── Entrypoint local ──────────────────────────────────────────────────────────

@app.local_entrypoint()
def main(
    conditions: str = "all",
    total_iterations: int = TOTAL_ITERATIONS,
    batch_size: int = BATCH_SIZE,
):
    """
    conditions: "4" = balanced (4:4:4) only,
                "8" = biased (8:2:2) only,
                "all" = both (48 conditions × n_batches = 2400 batches)
    """
    all_algos = ALGOS_CLEAN + ALGOS_NOISE
    n_batches = total_iterations // batch_size
    assert n_batches * batch_size == total_iterations, \
        f"total_iterations ({total_iterations}) must be divisible by batch_size ({batch_size})"

    # Construir lista de TODAS las batches
    tasks = []
    if conditions in ("4", "all"):
        for algo in all_algos:
            for b in range(n_batches):
                tasks.append((algo, POP_BALANCED, batch_size, b))
    if conditions in ("8", "all"):
        for algo in all_algos:
            for b in range(n_batches):
                tasks.append((algo, POP_BIASED, batch_size, b))

    _banner(conditions, total_iterations, batch_size, n_batches, len(tasks))

    # Lanza TODAS las batches en paralelo en Modal
    results = list(run_batch.starmap(tasks))

    # Agregar por (algo, pop)
    agg = defaultdict(lambda: {"Aggressive": 0, "Cooperative": 0, "Neutral": 0})
    for r in results:
        key = (r["algo"], r["pop"])
        for att in ["Aggressive", "Cooperative", "Neutral"]:
            agg[key][att] += r[att]

    # Construir filas finales (una por condición)
    final = []
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    for (algo, pop), counts in agg.items():
        total = sum(counts.values())
        pct = {k: round(100 * v / total, 2) if total else 0.0 for k, v in counts.items()}
        final.append({
            "fecha": timestamp,
            "algo": algo,
            "iteraciones": total_iterations,
            "pop_agresivos": pop[0],
            "pop_cooperativos": pop[1],
            "pop_neutrales": pop[2],
            "Aggressive": counts["Aggressive"],
            "Cooperative": counts["Cooperative"],
            "Neutral": counts["Neutral"],
            "pct_Aggressive": pct["Aggressive"],
            "pct_Cooperative": pct["Cooperative"],
            "pct_Neutral": pct["Neutral"],
        })

    _save_results(final, results, total_iterations)


def _banner(conditions, total_iter, batch_size, n_batches, n_tasks):
    est_min = 3.5  # min por batch (~3min real + overhead)
    print(f"\n{'='*65}")
    print(f"  EvoLLM Moran — Modal Cloud Run (BATCHED)")
    print(f"{'='*65}")
    print(f"  Condiciones      : {conditions}")
    print(f"  Iteraciones totales: {total_iter} por condicion")
    print(f"  Tamano de batch  : {batch_size} iter")
    print(f"  Batches por cond.: {n_batches}")
    print(f"  Tareas paralelas : {n_tasks}")
    print(f"  CPUs por tarea   : {CPUS_PER_JOB}")
    print(f"  Tiempo estimado  : ~{est_min:.0f}min por batch (paralelo -> ~{est_min*2:.0f}min total)")
    print(f"  Costo estimado   : ~${n_tasks * est_min * 0.0003:.2f} USD")
    print(f"{'='*65}\n")


def _save_results(final: list, all_batches: list, total_iter: int):
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    # Histórico agregado
    history_path = results_dir / "moran_history.csv"
    fieldnames = [
        "fecha", "algo", "iteraciones",
        "pop_agresivos", "pop_cooperativos", "pop_neutrales",
        "Aggressive", "Cooperative", "Neutral",
        "pct_Aggressive", "pct_Cooperative", "pct_Neutral",
    ]
    history_exists = history_path.exists()
    with open(history_path, "a", newline="", encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not history_exists:
            writer.writeheader()
        for r in final:
            writer.writerow({k: r[k] for k in fieldnames})

    # JSON con todos los batches (para auditoria)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = results_dir / f"modal_batched_run_{ts}.json"
    with open(json_path, "w", encoding="utf8") as f:
        json.dump({
            "total_iterations": total_iter,
            "aggregated": final,
            "all_batches": all_batches,
        }, f, indent=2, default=str)

    # Tabla resumen en consola
    print(f"\n{'Condicion':<45} {'Pop':>7}  {'A%':>5} {'C%':>5} {'N%':>5}")
    print("-" * 73)
    for r in sorted(final, key=lambda x: (x["pop_agresivos"], x["algo"])):
        pop = f"{r['pop_agresivos']}:{r['pop_cooperativos']}:{r['pop_neutrales']}"
        print(
            f"  {r['algo']:<43} {pop:>7}  "
            f"{r['pct_Aggressive']:>5.1f} {r['pct_Cooperative']:>5.1f} {r['pct_Neutral']:>5.1f}"
        )

    print(f"\nGuardado en:")
    print(f"   {history_path}  (+{len(final)} filas)")
    print(f"   {json_path}")
