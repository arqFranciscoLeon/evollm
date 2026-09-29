"""What-if completion of the intended 600-identity panel (post hoc, NOT preregistered).

The 28 excluded aggressive descriptions have no faithful common-conversion
implementation. Their archived historical implementations (Phase 1/2 Default
libraries) do exist and run. This scenario adds them to the registered 572-identity
matrix, plays every new pair once (1,000 rounds, no noise, strict runtime) and
recomputes the registered H7 statistic on 600 identities.

Caveats that travel with every number from this script: historical code for a
truncated or indeterminate description is not a faithful implementation; the
completed panel mixes two conversion procedures; nothing here enters H7.
"""
from concurrent.futures import ProcessPoolExecutor
import json

import numpy as np

from phase3.analyze_phase3 import h7_statistic
from phase3.posthoc_common_v1 import BASE_SEED, OUT, TURNS, load_primary, write_json
from phase3.posthoc_h7_structure_v1 import codes, per_model_table, PAIR_LABELS
from phase3.runtime import play_pair, seed_for

OUTPUT = OUT / 'completion_v1.json'
_UNIFORM = None
_HIST = None


def settable_score(cls):
    """Historical classes expose a read-only score; common-conversion players assign
    opponent.score. Ignore the assignment and keep the historical score, which the
    strict runtime updates at the start of each historical move (historical player
    always takes the first seat, so its score is current when the opponent moves)."""
    return type(cls.__name__, (cls,), {'score': property(lambda self: self._score, lambda self, value: None)})


def _init():
    global _UNIFORM, _HIST
    from phase3.execute_uniform import load_field
    from phase3.runtime import configure_strict, load_library, read_manifest
    _UNIFORM = load_field().players
    manifest = read_manifest()
    configure_strict(manifest)
    _HIST = {}
    for lib in manifest['libraries']:
        if lib['prompt'] == 'default':
            _HIST.update({k: settable_score(v) for k, v in load_library(lib).items()})


def _play(job):
    kind, first, second = job
    factory_2 = _HIST[second] if kind == 'hist-hist' else _UNIFORM[second]
    try:
        r = play_pair(_HIST[first], factory_2, TURNS, seed_for(BASE_SEED, 'posthoc_completion_v1', first, second))
        return job, r, None
    except Exception as exc:
        return job, None, f'{type(exc).__name__}: {str(exc)[:160]}'


def main():
    if OUTPUT.exists():
        raise FileExistsError('Output exists; inspect before rerunning')
    data = load_primary()
    ids = data['ids']
    from phase3.runtime import read_manifest
    default_ids = sorted(s['id'] for lib in read_manifest()['libraries'] if lib['prompt'] == 'default'
                         for s in lib['strategies'])
    excluded = sorted(set(default_ids) - set(ids))
    if len(excluded) != 28:
        raise ValueError(f'Expected 28 excluded identities, found {len(excluded)}')
    jobs = [('hist-uniform', e, j) for e in excluded for j in ids]
    jobs += [('hist-hist', e, f) for n, e in enumerate(excluded) for f in excluded[n:]]
    with ProcessPoolExecutor(max_workers=7, initializer=_init) as pool:
        results = list(pool.map(_play, jobs, chunksize=32))
    errors = [(job, err) for job, _, err in results if err]

    full = ids + excluded
    pos = {s: i for i, s in enumerate(full)}
    n = len(full)
    c = np.full((n, n), np.nan)
    c[:572, :572] = data['cooperation']
    for (kind, first, second), r, err in results:
        if err:
            continue
        i, j = pos[first], pos[second]
        c[i, j] = c[j, i] = r['CC'] / TURNS
    models = [s.split('/')[0] for s in full]
    attitudes = [s.split('/')[-1].split('_')[0] for s in full]

    result = {'status': 'post hoc what-if; historical implementations of excluded descriptions; not preregistered',
              'excluded_identities': excluded, 'new_matches': len(jobs), 'errors': len(errors),
              'error_examples': [{'job': list(job), 'error': err} for job, err in errors[:20]]}
    off = ~np.eye(n, dtype=bool)
    if np.isfinite(c[off]).all():
        t600 = h7_statistic(c, models, attitudes)
        mc, ac, labels = codes(models, attitudes)
        table = per_model_table(np.nan_to_num(c), mc, ac, len(labels))
        result.update({
            'h7_completed_600': t600, 'h7_completed_600_pp': 100 * t600,
            'h7_registered_572_pp': 100 * 0.005348991712007744,
            'strata': PAIR_LABELS,
            'per_model_mean_difference_pp': dict(zip(labels, (100 * table.mean(axis=1)).tolist())),
            'per_model_stratum_differences_pp': {labels[m]: (100 * table[m]).tolist() for m in range(len(labels))},
            'completed_cell_mean_cooperation_vs_all_others': {
                f'{m}/Aggressive': float(np.nanmean([np.nanmean(np.delete(c[i], i)) for i in range(n)
                                                     if models[i] == m and attitudes[i] == 'Aggressive']))
                for m in labels},
        })
    write_json(OUTPUT, result)
    print(json.dumps({k: v for k, v in result.items() if k not in ('excluded_identities', 'per_model_stratum_differences_pp')}, indent=1))


if __name__ == '__main__':
    main()
