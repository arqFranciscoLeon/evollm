"""Full-horizon archival diagnostics. Does NOT execute a mixed tournament."""
import argparse
from concurrent.futures import ProcessPoolExecutor
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import time

from phase3.runtime import ROOT, configure_strict, load_library, read_manifest, seed_for


def validate_library(item):
    import axelrod as axl
    manifest = read_manifest()
    configure_strict(manifest)
    classes = load_library(item)
    opponents = [axl.Cooperator, axl.Defector, axl.Random, axl.TitForTat, axl.Grudger,
                 axl.CyclerDDC, axl.CyclerCCD, axl.GoByMajority, axl.SuspiciousTitForTat,
                 axl.Prober, axl.WinStayLoseShift]
    failures = []
    matches = 0
    started = time.monotonic()
    for sid, cls in classes.items():
        for opponent in opponents:
            matches += 1
            try:
                m = axl.Match((cls(), opponent()), turns=1000, game=axl.Game(r=3,s=0,t=5,p=1),
                              noise=0, seed=seed_for(20260913, sid, opponent.__name__))
                m.play()
                if len(m.result) != 1000:
                    raise ValueError("Incomplete match")
            except Exception as exc:
                failures.append({"strategy": sid, "opponent": opponent.__name__,
                                 "error": f"{type(exc).__name__}: {exc}"})
    return {"library": item['filename'], "sha256": item['sha256'], "matches": matches,
            "failures": failures, "failed_strategies": len({r['strategy'] for r in failures}),
            "elapsed_seconds": time.monotonic()-started}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--model')
    args = parser.parse_args()
    if args.workers < 1:
        parser.error('workers must be positive')
    libraries = [x for x in read_manifest()['libraries'] if x['prompt'] == 'default'
                 and (not args.model or x['model'] == args.model)]
    if not libraries:
        parser.error('No matching libraries')
    out = ROOT / 'phase3/validation'
    out.mkdir(exist_ok=True)
    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for result in pool.map(validate_library, libraries):
            results.append(result)
            (out / (result['library'] + '.json')).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
            print(f"{result['library']}: {result['failed_strategies']} strategies failed; {len(result['failures'])}/{result['matches']} matches failed", flush=True)
    report = {'purpose': 'Archival full-horizon diagnostics; no fixed-converter or mixed-tournament results',
              'seed': 20260913, 'turns': 1000, 'noise': 0, 'workers': args.workers,
              'runtime_policy': 'strict: no invalid-action substitution; historical History.count compatibility retained',
              'python': platform.python_version(), 'cpu_count': os.cpu_count(),
              'packages': {p: importlib.metadata.version(p) for p in ('axelrod','numpy','pandas','scipy')},
              'libraries': results, 'all_pass': all(not r['failures'] for r in results)}
    name = 'archival_default' + ('_' + args.model if args.model else '') + '.json'
    (out / name).write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(f"Diagnostic complete; all_pass={report['all_pass']}", flush=True)


if __name__ == '__main__':
    main()
