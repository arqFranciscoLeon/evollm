"""Post hoc analysis of the 24 archived historical libraries (NOT preregistered).

Uses the archived Phase 1 (corrected) and Phase 2 implementations under the
strict Phase 3 runtime: an exception or invalid action is recorded as an error,
never replaced by an action. Exploratory encounters only; no API calls.

1. Probe signatures of all 1,800 historical classes (Default, Prose, Refine).
2. Agreement between historical and common-conversion implementations of the
   572 eligible Default identities (same description, two conversion procedures).
3. Retained versus excluded Default aggressive descriptions, as historically implemented.
4. Within-library attitude payoff matrices from all class pairs, and the
   cooperative-minus-neutral payoff gap, compared with the archived
   balanced-noiseless fixation margins of Phases 1 and 2.
5. Prose length of retained versus excluded Default aggressive descriptions.
"""
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
import itertools
import json

import numpy as np
from scipy import stats

from phase3.analyze_phase3 import ATTITUDES
from phase3.posthoc_common_v1 import (BASE_SEED, ENDGAME, OUT, PHASE, ROOT, TURNS, canonical_signatures,
                                      descriptors, label_signature, signature, signature_key, write_json)
from phase3.runtime import play_pair, seed_for

OUTPUT = OUT / 'historical_v1.json'
_CLASSES = None
_REFS = None


def _libraries():
    from phase3.runtime import read_manifest
    return read_manifest()['libraries']


def _init():
    global _CLASSES, _REFS
    from phase3.runtime import configure_strict, load_library, read_manifest
    manifest = read_manifest()
    configure_strict(manifest)
    _CLASSES = {}
    for lib in manifest['libraries']:
        _CLASSES.update(load_library(lib))
    _REFS = canonical_signatures()


def _characterise(cid):
    try:
        sig = signature(_CLASSES[cid])
    except Exception as exc:  # strict runtime: record, never substitute
        return cid, {'error': f'{type(exc).__name__}: {str(exc)[:200]}'}
    return cid, {'label': label_signature(sig, _REFS), 'descriptors': descriptors(sig),
                 'signature_key': signature_key(sig),
                 'signature_key_pre_endgame': signature_key(sig, TURNS - ENDGAME),
                 'probe_cooperation': {n: sig[n]['mine'].count('C') / TURNS for n in sig}}


def _pair(job):
    first, second = job
    try:
        r = play_pair(_CLASSES[first], _CLASSES[second], TURNS,
                      seed_for(BASE_SEED, 'posthoc_hist_pair_v1', first, second))
        return first, second, r['payoff_i'], r['payoff_j'], None
    except Exception as exc:
        return first, second, None, None, f'{type(exc).__name__}: {str(exc)[:120]}'


def att(cid):
    return cid.split('/')[-1].split('_')[0]


def main():
    if OUTPUT.exists():
        raise FileExistsError('Output exists; inspect before rerunning')
    libraries = _libraries()
    all_ids = [s['id'] for lib in libraries for s in lib['strategies']]
    lib_of = {s['id']: f"{lib['model']}_{lib['prompt']}_75" for lib in libraries for s in lib['strategies']}

    with ProcessPoolExecutor(max_workers=7, initializer=_init) as pool:
        sigs = dict(pool.map(_characterise, all_ids, chunksize=16))
        jobs = []
        for lib in libraries:
            ids = sorted(s['id'] for s in lib['strategies'])
            jobs.extend(itertools.combinations_with_replacement(ids, 2))
        pairs = list(pool.map(_pair, jobs, chunksize=64))

    # --- 1. Library-level behaviour summaries
    libs = {}
    for lib in libraries:
        name = f"{lib['model']}_{lib['prompt']}_75"
        members = sorted(s['id'] for s in lib['strategies'])
        summary = {'model': lib['model'], 'prompt': lib['prompt'], 'errors': sum('error' in sigs[c] for c in members)}
        keys = defaultdict(set)
        for c in members:
            if 'error' not in sigs[c]:
                keys[sigs[c]['signature_key']].add(att(c))
        for a in ATTITUDES:
            ok = [c for c in members if att(c) == a and 'error' not in sigs[c]]
            labels = [sigs[c]['label']['label'] for c in ok]
            summary[a] = {
                'classes_ok': len(ok),
                'nice_share': float(np.mean([sigs[c]['descriptors']['nice'] for c in ok])) if ok else None,
                'tft_family_share': float(np.mean([l.startswith('TitForTat') for l in labels])) if ok else None,
                'defector_share': float(np.mean([l.startswith('Defector') for l in labels])) if ok else None,
                'distinct_signatures': len({sigs[c]['signature_key'] for c in ok}),
            }
        cn = [c for c in members if att(c) in ('Cooperative', 'Neutral') and 'error' not in sigs[c]]
        summary['cooperative_neutral_signature_twins_share'] = float(np.mean(
            [{'Cooperative', 'Neutral'} <= keys[sigs[c]['signature_key']] for c in cn])) if cn else None
        libs[name] = summary

    # --- 2. Historical vs common-conversion agreement (572 eligible Default identities)
    behaviour = json.loads((OUT / 'behaviour_v1.json').read_text(encoding='utf-8'))['identities']
    agreement = defaultdict(lambda: {'n': 0, 'exact': 0, 'pre_endgame': 0, 'historical_error': 0})
    same_label = defaultdict(int)
    for sid, row in behaviour.items():
        cell = f"{sid.split('/')[0]}/{att(sid)}"
        for key in (cell, f'ALL/{att(sid)}', 'ALL/ALL'):
            agreement[key]['n'] += 1
            h = sigs.get(sid)
            if h is None or 'error' in h:
                agreement[key]['historical_error'] += 1
                continue
            agreement[key]['exact'] += h['signature_key'] == row['signature_key']
            agreement[key]['pre_endgame'] += h['signature_key_pre_endgame'] == row['signature_key_pre_endgame']
            if key == 'ALL/ALL':
                same_label[h['label']['label'] == row['label']['label']] += 1
    agreement = {k: {**v, 'exact_share': v['exact'] / v['n'], 'pre_endgame_share': v['pre_endgame'] / v['n']}
                 for k, v in sorted(agreement.items())}

    # --- 3. Retained vs excluded Default aggressive descriptions (historical implementations)
    retained = set(behaviour)
    excluded_table = {}
    for lib in libraries:
        if lib['prompt'] != 'default':
            continue
        aggressive = sorted(s['id'] for s in lib['strategies'] if att(s['id']) == 'Aggressive')
        groups = {'retained': [c for c in aggressive if c in retained],
                  'excluded': [c for c in aggressive if c not in retained]}
        if not groups['excluded']:
            continue
        row = {}
        for g, members in groups.items():
            ok = [c for c in members if 'error' not in sigs[c]]
            row[g] = {
                'n': len(members), 'historical_errors': len(members) - len(ok),
                'nice_share': float(np.mean([sigs[c]['descriptors']['nice'] for c in ok])) if ok else None,
                'mean_cooperation_vs_tft': float(np.mean([sigs[c]['descriptors']['cooperation_vs_tft'] for c in ok])) if ok else None,
                'mean_cooperation_vs_fixed05': float(np.mean([sigs[c]['descriptors']['cooperation_vs_fixed05'] for c in ok])) if ok else None,
                'defector_share': float(np.mean([sigs[c]['label']['label'].startswith('Defector') for c in ok])) if ok else None,
                'labels': sorted(sigs[c]['label']['label'] for c in ok),
            }
        excluded_table[lib['model']] = row

    # --- 4. Attitude payoff matrices and C-N gaps vs archived fixation margins
    payoff_sum = defaultdict(float)
    payoff_n = defaultdict(int)
    pair_errors = defaultdict(int)
    for first, second, pi, pj, err in pairs:
        name = lib_of[first]
        if err:
            pair_errors[name] += 1
            continue
        a, b = att(first), att(second)
        payoff_sum[(name, a, b)] += pi
        payoff_n[(name, a, b)] += 1
        if first != second:
            payoff_sum[(name, b, a)] += pj
            payoff_n[(name, b, a)] += 1
    matrices = {}
    for name in libs:
        m = [[payoff_sum[(name, a, b)] / payoff_n[(name, a, b)] if payoff_n[(name, a, b)] else None
              for b in ATTITUDES] for a in ATTITUDES]
        gap = [m[1][j] - m[2][j] for j in range(3)] if all(v is not None for v in m[1] + m[2]) else None
        matrices[name] = {'attitude_payoff_matrix_rows_focal_cols_opponent': m,
                          'pair_errors': pair_errors[name],
                          'cooperative_minus_neutral_gap': gap,
                          'balanced_gap': float(np.mean(gap)) if gap else None}

    prior = json.loads((PHASE / 'writing/prior_evidence_reconciled_v1.json').read_text(encoding='utf-8'))
    points = []
    for phase in ('phase1', 'phase2'):
        for row in prior['datasets'][phase]['balanced_clean']:
            name = row['algo']
            if name in matrices and matrices[name]['balanced_gap'] is not None:
                points.append({'phase': phase, 'library': name, 'margin_pp': row['margin_pp'],
                               'ci_includes_zero': row['ci_includes_zero'],
                               'balanced_gap': matrices[name]['balanced_gap'],
                               'cn_twins_share': libs[name]['cooperative_neutral_signature_twins_share']})
    x = np.array([p['balanced_gap'] for p in points])
    y = np.array([p['margin_pp'] for p in points])
    tw = np.array([p['cn_twins_share'] for p in points])
    association = {
        'n_libraries': len(points),
        'spearman_gap_vs_margin': list(stats.spearmanr(x, y)),
        'spearman_abs_gap_vs_abs_margin': list(stats.spearmanr(np.abs(x), np.abs(y))),
        'spearman_twins_vs_abs_margin': list(stats.spearmanr(tw, np.abs(y))),
        'label': 'Exploratory rank correlations across 24 libraries; margins carry Monte Carlo error (SE about 4 pp).',
    }

    # --- 5. Prose length of retained vs excluded Default aggressive descriptions
    from phase3.recover_prose import descriptions
    prose = {}
    for lib in libraries:
        if lib['prompt'] != 'default':
            continue
        text = descriptions((ROOT / lib['snapshot_path']).read_bytes())
        words = {f"{lib['model']}/default/{cls}": len(t.split()) for cls, t in text.items()}
        agg = {k: v for k, v in words.items() if att(k) == 'Aggressive'}
        ret = [v for k, v in agg.items() if k in retained]
        exc = [v for k, v in agg.items() if k not in retained]
        prose[lib['model']] = {
            'aggressive_retained_words_median': float(np.median(ret)) if ret else None,
            'aggressive_excluded_words_median': float(np.median(exc)) if exc else None,
            'aggressive_retained_n': len(ret), 'aggressive_excluded_n': len(exc),
            'cooperative_words_median': float(np.median([v for k, v in words.items() if att(k) == 'Cooperative'])),
            'neutral_words_median': float(np.median([v for k, v in words.items() if att(k) == 'Neutral'])),
        }

    result = {
        'status': 'post hoc, not preregistered; archived implementations under the strict runtime',
        'classes': len(all_ids),
        'class_errors': sum('error' in v for v in sigs.values()),
        'pair_matches': len(pairs), 'pair_errors_total': int(sum(pair_errors.values())),
        'libraries': libs,
        'historical_vs_common_conversion': {'by_cell': agreement,
                                            'same_canonical_label': {str(k): v for k, v in same_label.items()}},
        'retained_vs_excluded_aggressive_historical': excluded_table,
        'attitude_payoff_matrices': matrices,
        'fixation_margin_points': points,
        'fixation_margin_association': association,
        'prose_words_default': prose,
        'class_signatures': {k: ({'error': v['error']} if 'error' in v else
                                 {'label': v['label'], 'signature_key': v['signature_key'],
                                  'signature_key_pre_endgame': v['signature_key_pre_endgame'],
                                  'descriptors': v['descriptors']}) for k, v in sigs.items()},
    }
    write_json(OUTPUT, result)
    print(json.dumps({'class_errors': result['class_errors'], 'pair_errors': result['pair_errors_total'],
                      'agreement_all': agreement['ALL/ALL'], 'agreement_by_attitude': {a: agreement[f'ALL/{a}'] for a in ATTITUDES},
                      'association': association, 'excluded': excluded_table, 'prose': prose}, indent=1))


if __name__ == '__main__':
    main()
