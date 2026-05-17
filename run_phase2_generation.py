"""
run_phase2_generation.py — parallel orchestrator for Phase 2a strategy
generation (Chinese-only study, PHASE2_PREREG.md + Amendment 2026-05-17 B).

Launches the 24 independent generation jobs
  4 Chinese models x 3 prompts (default/prose/refine) x {clean, noise}
with a bounded concurrency pool. Each job runs
`python -m evollm.create_strategies` with the FIXED converter (default
gpt-5.4-mini) so generation stays per-model and conversion is held
constant.

Design notes
- Idempotent & resumable: a job whose library already has 3*n strategy
  classes is skipped; a partially-written library is continued with
  --resume; so re-running this script only does the remaining work.
- Concurrency-safe logging: `create_strategies` opens a fixed-name
  `create_strategies.log` in its CWD at import time, so each job runs in
  its own working directory and writes to an ABSOLUTE --algo path; the
  real strategy libraries still land in ./strategies/.
- No secrets are read or printed here; child processes handle their own
  keys and already filter them from output.

Usage
  python run_phase2_generation.py --dry-run          # show the plan only
  python run_phase2_generation.py --concurrency 8    # run the grid
  python run_phase2_generation.py --only glm_51       # subset / retry
"""

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent
SRC = REPO / "src"
STRAT = REPO / "strategies"
LOGDIR = REPO / "logs" / "phase2_gen"

# (registry model key, algo base name) — bases MUST match
# reproduce_tables.py CHINESE_ALGOS.
MODELS = [
    ("deepseek-v4-pro", "deepseek_v4pro"),
    ("qwen3-max",        "qwen3max"),
    ("kimi-k2.6",        "kimi_k26"),
    ("glm-5.1",          "glm_51"),
]
# (prompt name, extra create_strategies flags)
PROMPTS = [
    ("default", []),
    ("prose",   ["--prose"]),
    ("refine",  ["--refine"]),
]
# (suffix, extra flags)
NOISE = [
    ("",       []),
    ("_noise", ["--noise", "0.1"]),
]


def build_jobs(n):
    jobs = []
    for model_key, base in MODELS:
        for prompt, pflags in PROMPTS:
            for suffix, nflags in NOISE:
                algo = f"{base}_{prompt}_75{suffix}"
                jobs.append({
                    "name": algo,
                    "model": model_key,
                    "algo_path": STRAT / algo,          # no .py here
                    "flags": pflags + nflags,
                    "n": n,
                })
    return jobs


def class_count(py_path: Path) -> int:
    if not py_path.exists():
        return 0
    txt = py_path.read_text(encoding="utf8", errors="ignore")
    return len(re.findall(r"\(LLM_Strategy\)", txt))


def make_cmd(job):
    cmd = [
        sys.executable, "-m", "evollm.create_strategies",
        "--strategy_llm", "openrouter",
        "--model", job["model"],
        "--n", str(job["n"]),
        "--temp", "0.7",
        "--algo", str(job["algo_path"]),
    ] + job["flags"]
    # Resume an existing partial library instead of erroring on "exists".
    if job["algo_path"].with_suffix(".py").exists():
        cmd.append("--resume")
    return cmd


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--concurrency", type=int, default=8,
                    help="max jobs running at once (default 8)")
    ap.add_argument("--n", type=int, default=25,
                    help="strategies per attitude (Phase 1 used 25 -> 75/lib)")
    ap.add_argument("--only", default=None,
                    help="substring filter on job name (subset / retry)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the plan and exit (no API calls, no cost)")
    args = ap.parse_args()

    jobs = build_jobs(args.n)
    if args.only:
        jobs = [j for j in jobs if args.only in j["name"]]
    target = 3 * args.n

    LOGDIR.mkdir(parents=True, exist_ok=True)
    STRAT.mkdir(parents=True, exist_ok=True)

    todo, done = [], []
    for j in jobs:
        have = class_count(j["algo_path"].with_suffix(".py"))
        if have >= target:
            done.append(j)
        else:
            j["have"] = have
            todo.append(j)

    print(f"Phase 2a generation grid — {len(jobs)} jobs "
          f"({len(MODELS)} models x {len(PROMPTS)} prompts x "
          f"{len(NOISE)} noise), target {target} strategies/lib")
    print(f"  already complete: {len(done)}   to run: {len(todo)}   "
          f"concurrency: {args.concurrency}")
    for j in done:
        print(f"  [skip] {j['name']:<28} complete ({target}/{target})")
    for j in todo:
        tag = "fresh" if j["have"] == 0 else f"resume@{j['have']}"
        print(f"  [run ] {j['name']:<28} {j['model']:<16} ({tag})")

    if args.dry_run:
        print("\n--dry-run: nothing executed.")
        return
    if not todo:
        print("\nAll libraries already complete. Nothing to do.")
        return

    env = dict(os.environ)
    env["PYTHONPATH"] = (
        str(SRC) + (os.pathsep + env["PYTHONPATH"]
                    if env.get("PYTHONPATH") else ""))

    running = []          # (job, Popen, logfile handle, start_ts)
    queue = list(todo)
    results = {}
    t0 = time.time()

    def launch(job):
        wd = LOGDIR / f"wd_{job['name']}"
        wd.mkdir(parents=True, exist_ok=True)
        logf = open(LOGDIR / f"{job['name']}.log", "w", encoding="utf8")
        p = subprocess.Popen(make_cmd(job), cwd=str(wd), env=env,
                              stdout=logf, stderr=subprocess.STDOUT)
        print(f"  -> launched {job['name']} (pid {p.pid})")
        return (job, p, logf, time.time())

    while queue or running:
        while queue and len(running) < args.concurrency:
            running.append(launch(queue.pop(0)))
        time.sleep(5)
        still = []
        for job, p, logf, st in running:
            rc = p.poll()
            if rc is None:
                still.append((job, p, logf, st))
                continue
            logf.close()
            have = class_count(job["algo_path"].with_suffix(".py"))
            ok = rc == 0 and have >= target
            results[job["name"]] = {
                "rc": rc, "have": have, "ok": ok,
                "min": (time.time() - st) / 60,
            }
            mark = "OK " if ok else "FAIL"
            print(f"  [{mark}] {job['name']:<28} rc={rc} "
                  f"{have}/{target} in {results[job['name']]['min']:.1f}m")
            still.append(None)
            still = [x for x in still if x is not None]
        running = still

    dt = (time.time() - t0) / 60
    ok = [k for k, v in results.items() if v["ok"]]
    bad = [k for k, v in results.items() if not v["ok"]]
    print(f"\n=== Phase 2a generation summary ({dt:.1f} min wall) ===")
    print(f"  complete this run: {len(ok)}   failed/partial: {len(bad)}")
    for k in bad:
        v = results[k]
        print(f"  FAIL {k}: rc={v['rc']} {v['have']}/{target} "
              f"(re-run this script to --resume; log: logs/phase2_gen/{k}.log)")
    total_done = len(done) + len(ok)
    print(f"  libraries complete overall: {total_done}/{len(jobs)}")
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
