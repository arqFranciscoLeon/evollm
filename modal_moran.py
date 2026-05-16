"""
Modal deployment para simulaciones Moran EvoLLM
================================================
Lanza las 48 condiciones en paralelo en la nube.

SETUP (una sola vez):
    pip install modal
    python -m modal setup

USO:
    modal run modal_moran.py                     # todas las 48 condiciones
    modal run modal_moran.py --conditions 4      # solo 4:4:4 (24 condiciones)
    modal run modal_moran.py --conditions 8      # solo 8:2:2 (24 condiciones)
    modal run modal_moran.py --iterations 500    # cambiar iteraciones (default)

RESULTADO:
    Los resultados se guardan automáticamente en results/moran_history.csv
    y en results/modal_run_TIMESTAMP.json
"""

import modal
from pathlib import Path
import csv
import json
from datetime import datetime

# ── Configuración ────────────────────────────────────────────────────────────

ITERATIONS = 500           # Objetivo del paper: n=500
CPUS_PER_JOB = 1           # 1 CPU — la paralelización viene de los 48 containers
TIMEOUT_SECONDS = 14400    # 4 horas por condición (margen amplio)

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

POP_BALANCED = [4, 4, 4]   # Fase A/B: balanced
POP_BIASED   = [8, 2, 2]   # Fase C/D: biased

# ── Imagen Modal (API 1.x) ────────────────────────────────────────────────────

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
    "evollm-moran",
    image=image,
)

# ── Función que corre en la nube ──────────────────────────────────────────────

@app.function(
    cpu=CPUS_PER_JOB,
    timeout=TIMEOUT_SECONDS,
    retries=1,
)
def run_moran_condition(algo_name: str, initial_pop: list, iterations: int) -> dict:
    """Corre UNA condición Moran completa. Se ejecuta en un container Modal."""
    import sys
    import os
    import subprocess
    import csv
    import io
    from datetime import datetime

    workdir = "/root/evollm"
    script = f"{workdir}/src/evollm/moran_process.py"

    cmd = [
        sys.executable, script,
        "--algo", f"{workdir}/strategies/{algo_name}",
        "--initial_pop", str(initial_pop[0]), str(initial_pop[1]), str(initial_pop[2]),
        "--iterations", str(iterations),
        "--processes", "1",
    ]

    env = os.environ.copy()
    env["PYTHONPATH"] = f"{workdir}/src"

    print(f"[{algo_name}] Iniciando: pop={initial_pop}, n={iterations}, procs={CPUS_PER_JOB}")

    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=workdir,
        env=env,
    )

    stdout = proc.stdout
    stderr = proc.stderr

    if proc.returncode != 0:
        print(f"[{algo_name}] ERROR (returncode={proc.returncode})")
        print(stderr[-2000:] if stderr else "(no stderr)")
        raise RuntimeError(f"moran_process failed for {algo_name}: {stderr[-500:]}")

    # Parsear la salida del script.
    # moran_process.py imprime el dict RAW con claves como "LLM: Aggressive (ours)"
    # y luego el dict normalizado. Buscamos cualquier dict con esas claves.
    import ast as _ast
    attitudes = ["Aggressive", "Cooperative", "Neutral"]
    normalized = {"Aggressive": 0, "Cooperative": 0, "Neutral": 0}

    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if line.startswith("{") and any(att in line for att in attitudes):
            try:
                raw = _ast.literal_eval(line)
                # Normalizar: "LLM: Aggressive (ours)" ->"Aggressive"
                for name, count in raw.items():
                    for att in attitudes:
                        if att in name:
                            normalized[att] += count
                            break
                if sum(normalized.values()) > 0:
                    break
            except Exception:
                continue

    # Debug: imprimir stdout si no encontramos resultados
    if sum(normalized.values()) == 0:
        print(f"[{algo_name}] WARN: no se encontraron resultados en stdout:")
        print(stdout[-1000:])

    total = sum(normalized.values())
    pct = {k: round(100 * v / total, 2) if total else 0.0 for k, v in normalized.items()}

    print(
        f"[{algo_name}] OK pop={initial_pop} "
        f"A:{pct['Aggressive']}% C:{pct['Cooperative']}% N:{pct['Neutral']}%"
    )

    return {
        "fecha": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "algo": algo_name,
        "iteraciones": iterations,
        "pop_agresivos": initial_pop[0],
        "pop_cooperativos": initial_pop[1],
        "pop_neutrales": initial_pop[2],
        "Aggressive": normalized["Aggressive"],
        "Cooperative": normalized["Cooperative"],
        "Neutral": normalized["Neutral"],
        "pct_Aggressive": pct["Aggressive"],
        "pct_Cooperative": pct["Cooperative"],
        "pct_Neutral": pct["Neutral"],
    }


# ── Entrypoint local ──────────────────────────────────────────────────────────

@app.local_entrypoint()
def main(
    conditions: str = "all",
    iterations: int = ITERATIONS,
):
    """
    conditions: "4" = solo balanced (4:4:4),
                "8" = solo biased (8:2:2),
                "all" = ambas (48 condiciones)
    """
    all_algos = ALGOS_CLEAN + ALGOS_NOISE
    tasks = []

    if conditions in ("4", "all"):
        for algo in all_algos:
            tasks.append((algo, POP_BALANCED, iterations))

    if conditions in ("8", "all"):
        for algo in all_algos:
            tasks.append((algo, POP_BIASED, iterations))

    _banner(conditions, iterations, len(tasks))

    # Lanza TODAS las condiciones en paralelo en Modal
    results = list(run_moran_condition.starmap(tasks))

    _save_results(results, iterations)


def _banner(conditions, iterations, n_tasks):
    est_min = max(1, iterations // 100) * 3.2 / CPUS_PER_JOB  # ~minutos
    print(f"\n{'='*65}")
    print(f"  EvoLLM Moran — Modal Cloud Run")
    print(f"{'='*65}")
    print(f"  Condiciones      : {conditions}")
    print(f"  Iteraciones      : {iterations}")
    print(f"  Tareas en paralelo: {n_tasks}")
    print(f"  CPUs por tarea   : {CPUS_PER_JOB}")
    print(f"  Tiempo estimado  : ~{est_min:.0f}h por condición (paralelo ->~misma duración)")
    print(f"  Costo estimado   : ~${n_tasks * est_min * 0.0003:.2f} USD")
    print(f"{'='*65}\n")


def _save_results(results: list, iterations: int):
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

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
        for r in results:
            writer.writerow({k: r[k] for k in fieldnames})

    # Archivos individuales por condición
    for r in results:
        tag = f"{r['pop_agresivos']}_{r['pop_cooperativos']}_{r['pop_neutrales']}"
        path = results_dir / f"{r['algo']}_{tag}_n{iterations}_moran.csv"
        with open(path, "w", newline="", encoding="utf8") as f:
            writer = csv.DictWriter(f, fieldnames=["Actitud", "Victorias", "Porcentaje"])
            writer.writeheader()
            for att in ["Aggressive", "Cooperative", "Neutral"]:
                writer.writerow({
                    "Actitud": att,
                    "Victorias": r[att],
                    "Porcentaje": r[f"pct_{att}"],
                })

    # Resumen JSON
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = results_dir / f"modal_run_{ts}.json"
    with open(json_path, "w", encoding="utf8") as f:
        json.dump(results, f, indent=2)

    # Tabla resumen
    print(f"\n{'Condición':<45} {'Pop':>7}  {'A%':>5} {'C%':>5} {'N%':>5}")
    print("-" * 73)
    for r in sorted(results, key=lambda x: (x["pop_agresivos"], x["algo"])):
        pop = f"{r['pop_agresivos']}:{r['pop_cooperativos']}:{r['pop_neutrales']}"
        print(
            f"  {r['algo']:<43} {pop:>7}  "
            f"{r['pct_Aggressive']:>5.1f} {r['pct_Cooperative']:>5.1f} {r['pct_Neutral']:>5.1f}"
        )

    print(f"\nGuardado en:")
    print(f"   {history_path}  (+{len(results)} filas)")
    print(f"   {json_path}")
