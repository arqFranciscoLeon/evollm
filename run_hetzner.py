"""
Runner Phase 2a para Hetzner — PARALELISMO POR SUBPROCESOS.
===========================================================
Lanza, por condición (algo × población), WORKERS subprocesos independientes
de moran_process.py, cada uno con --processes 1 (camino SERIAL, sin el Pool
interno de Python). Razón: en Python 3.14 el Pool interno se cuelga (spawn no
encuentra run_moran_process; fork hereda locks de OpenBLAS → deadlock a 0% CPU,
observado 2 veces). El camino --processes 1 NO tiene multiprocessing alguno y
está validado decenas de veces (diagnóstico + Modal).

Cada subproceso corre 1/WORKERS de las iteraciones en su PROPIO directorio
temporal (evita colisiones de results/*.csv). El runner parsea el dict de
conteos del STDOUT de cada subproceso y los SUMA → n total por condición. Luego
escribe una fila agregada en results/moran_history.csv (mismo formato que
moran_process.py) para que el merge/convert downstream funcione.

Idempotente: salta condiciones ya completas (hetzner_progress_<shard>.json).

USO:
    export PYTHONPATH=$(pwd)/src
    python run_hetzner.py --iterations 500 --processes 8 --shard s1
"""

import argparse
import ast
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

ALGOS_CLEAN = [
    "deepseek_v4pro_default_75",
    "deepseek_v4pro_prose_75",
    "deepseek_v4pro_refine_75",
    "glm_51_default_75",
    "glm_51_prose_75",
    "glm_51_refine_75",
    "qwen3max_default_75",
    "qwen3max_prose_75",
    "qwen3max_refine_75",
    "kimi_k25_default_75",
    "kimi_k25_prose_75",
    "kimi_k25_refine_75",
]
ALGOS = ALGOS_CLEAN + [a + "_noise" for a in ALGOS_CLEAN]

POPS = [
    ("4_4_4", [4, 4, 4]),
    ("8_2_2", [8, 2, 2]),
]

ATTITUDES = ["Aggressive", "Cooperative", "Neutral"]


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--iterations", type=int, required=True,
                   help="Iteraciones Moran TOTALES por condición (se reparten "
                        "entre los WORKERS subprocesos).")
    p.add_argument("--processes", type=int, default=8,
                   help="Número de subprocesos paralelos por condición = nº de "
                        "vCPU a saturar (8 en un CCX33).")
    p.add_argument("--shard", type=str, default="s1",
                   help="Etiqueta para el archivo de progreso.")
    return p.parse_args()


def split_iterations(total, n):
    """Reparte `total` iteraciones en `n` trozos lo más iguales posible."""
    base, rem = divmod(total, n)
    return [base + (1 if i < rem else 0) for i in range(n)]


def parse_counts(stdout):
    """Extrae el dict de conteos de ganadores del stdout y lo normaliza a
    Aggressive/Cooperative/Neutral. moran_process.py imprime winner_counts."""
    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if line.startswith("{") and any(att in line for att in ATTITUDES):
            try:
                raw = ast.literal_eval(line)
            except Exception:
                continue
            tmp = {a: 0 for a in ATTITUDES}
            for name, count in raw.items():
                for att in ATTITUDES:
                    if att in name:
                        tmp[att] += count
                        break
            if sum(tmp.values()) > 0:
                return tmp
    return None


def run_condition(workdir, script, algo, pop, total_iters, workers):
    """Lanza `workers` subprocesos --processes 1 en paralelo, cada uno con su
    propio CWD temporal; suma sus conteos. Devuelve (counts, n_real, ok)."""
    chunks = [c for c in split_iterations(total_iters, workers) if c > 0]
    procs, tmpdirs = [], []

    for ch in chunks:
        td = tempfile.mkdtemp(prefix=f"moran_{algo}_")
        (Path(td) / "results").mkdir(parents=True, exist_ok=True)
        tmpdirs.append(td)

        env = os.environ.copy()
        env["PYTHONPATH"] = str(workdir / "src")
        env["MPLBACKEND"] = "Agg"
        env["OMP_NUM_THREADS"] = "1"
        env["OPENBLAS_NUM_THREADS"] = "1"

        cmd = [
            sys.executable, str(script),
            "--algo", str(workdir / "strategies" / algo),
            "--initial_pop", str(pop[0]), str(pop[1]), str(pop[2]),
            "--iterations", str(ch),
            "--processes", "1",
        ]
        p = subprocess.Popen(cmd, cwd=td, env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             text=True)
        procs.append((p, ch))

    counts = {a: 0 for a in ATTITUDES}
    n_real = 0
    ok = True
    for p, ch in procs:
        out, err = p.communicate()
        if p.returncode != 0:
            ok = False
            print(f"    [subproc rc={p.returncode}] {err.strip()[-300:]}", flush=True)
            continue
        c = parse_counts(out)
        if c is None:
            ok = False
            print(f"    [parse-fail] tail: {out.strip().splitlines()[-3:]}", flush=True)
            continue
        for a in ATTITUDES:
            counts[a] += c[a]
        n_real += sum(c.values())

    for td in tmpdirs:
        shutil.rmtree(td, ignore_errors=True)

    return counts, n_real, ok


def append_history(workdir, algo, pop, counts, n_real):
    results_dir = workdir / "results"
    results_dir.mkdir(exist_ok=True)
    history = results_dir / "moran_history.csv"
    fields = ["fecha", "algo", "iteraciones",
              "pop_agresivos", "pop_cooperativos", "pop_neutrales",
              "Aggressive", "Cooperative", "Neutral",
              "pct_Aggressive", "pct_Cooperative", "pct_Neutral"]
    total = sum(counts.values()) or 1
    exists = history.exists()
    with open(history, "a", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if not exists:
            w.writeheader()
        w.writerow({
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "algo": algo, "iteraciones": n_real,
            "pop_agresivos": pop[0], "pop_cooperativos": pop[1], "pop_neutrales": pop[2],
            "Aggressive": counts["Aggressive"], "Cooperative": counts["Cooperative"],
            "Neutral": counts["Neutral"],
            "pct_Aggressive": round(100 * counts["Aggressive"] / total, 2),
            "pct_Cooperative": round(100 * counts["Cooperative"] / total, 2),
            "pct_Neutral": round(100 * counts["Neutral"] / total, 2),
        })


def main():
    args = parse_args()
    workdir = Path(__file__).parent.resolve()
    script = workdir / "src" / "evollm" / "moran_process.py"

    progress_file = workdir / f"hetzner_progress_{args.shard}.json"
    done = set()
    if progress_file.exists():
        done = set(json.loads(progress_file.read_text()))
        print(f"[RESUME] {len(done)} condiciones ya completas.", flush=True)

    jobs = [(algo, pn, pop) for algo in ALGOS for pn, pop in POPS]
    total_jobs = len(jobs)
    print(f"=== Hetzner runner {args.shard} | {args.iterations} iter/cond | "
          f"{args.processes} subprocs/cond | {total_jobs} condiciones ===", flush=True)

    t_start = time.time()
    for i, (algo, pop_name, pop) in enumerate(jobs, 1):
        key = f"{algo}|{pop_name}"
        if key in done:
            print(f"[{i}/{total_jobs}] SKIP {key}", flush=True)
            continue

        t0 = time.time()
        print(f"[{i}/{total_jobs}] RUN  {key} ...", flush=True)
        counts, n_real, ok = run_condition(
            workdir, script, algo, pop, args.iterations, args.processes)
        dt = (time.time() - t0) / 60

        if not ok or n_real == 0:
            print(f"[{i}/{total_jobs}] FAIL {key} ({dt:.1f} min) n={n_real} "
                  f"{counts} — no se marca; se reintenta al reiniciar.", flush=True)
            continue

        append_history(workdir, algo, pop, counts, n_real)
        print(f"[{i}/{total_jobs}] OK   {key} ({dt:.1f} min) n={n_real} {counts}",
              flush=True)
        done.add(key)
        progress_file.write_text(json.dumps(sorted(done), indent=2))

    elapsed = (time.time() - t_start) / 3600
    print(f"\n=== {args.shard} TERMINADO: {len(done)}/{total_jobs} condiciones "
          f"en {elapsed:.2f} h ===", flush=True)


if __name__ == "__main__":
    main()
