"""
Diagnostico Phase 2a: tiempo por libreria (n=1 Moran iter, balanced 4:4:4).
Identifica librerias chinas patologicas que causarian timeouts en Modal n=500.

Output: rankings + CSV en diagnose_results.csv. Cada libreria con cap de 900s.
"""

import csv
import subprocess
import sys
import time
from pathlib import Path

LIBRARIES = [
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

CAP_SECONDS = 900   # 15 min cap por libreria
POP = ("4", "4", "4")

def main():
    workdir = Path(__file__).parent.resolve()
    script = workdir / "src" / "evollm" / "moran_process.py"

    results = []
    print(f"{'Libreria':<40} {'Tiempo':>12}  {'Veredicto'}")
    print("-" * 80)

    for algo in LIBRARIES:
        algo_path = workdir / "strategies" / algo
        cmd = [
            sys.executable, str(script),
            "--algo", str(algo_path),
            "--initial_pop", POP[0], POP[1], POP[2],
            "--iterations", "1",
            "--processes", "1",
        ]
        env_pythonpath = str(workdir / "src")

        start = time.time()
        timed_out = False
        try:
            import os
            env = os.environ.copy()
            env["PYTHONPATH"] = env_pythonpath
            env["PYTHONIOENCODING"] = "utf-8"
            proc = subprocess.run(
                cmd,
                capture_output=True, text=True,
                cwd=str(workdir),
                env=env,
                timeout=CAP_SECONDS,
            )
            elapsed = time.time() - start
            ok = proc.returncode == 0
        except subprocess.TimeoutExpired:
            elapsed = CAP_SECONDS
            timed_out = True
            ok = False

        if timed_out:
            verdict = "PATOLOGICA (>15 min)"
        elif not ok:
            verdict = "ERROR"
        elif elapsed > 600:
            verdict = "Lenta (>10 min)"
        elif elapsed > 300:
            verdict = "Mediana (5-10 min)"
        else:
            verdict = "Rapida (<5 min)"

        print(f"{algo:<40} {elapsed/60:>9.2f} min  {verdict}")
        results.append({"libreria": algo, "seconds": round(elapsed, 1),
                        "minutes": round(elapsed/60, 2), "timeout": timed_out,
                        "verdict": verdict})

    print("\n" + "=" * 80)
    print("Resumen ordenado por tiempo:")
    print("-" * 80)
    for r in sorted(results, key=lambda x: -x["seconds"]):
        print(f"  {r['libreria']:<40} {r['minutes']:>6.2f} min  {r['verdict']}")

    csv_path = workdir / "diagnose_results.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["libreria", "seconds", "minutes",
                                          "timeout", "verdict"])
        w.writeheader()
        w.writerows(results)
    print(f"\nGuardado: {csv_path}")


if __name__ == "__main__":
    main()
