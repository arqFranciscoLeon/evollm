"""Axelrod-style ecological dynamics on the registered payoff matrix (post hoc, NOT preregistered).

Discrete replicator iteration x_i' = x_i * f_i / mean(f), with f_i = sum_j x_j P_ij,
where P_ij is the registered per-round payoff of identity i against j (self-play
included on the diagonal, as in Axelrod's ecological analysis). Deterministic,
infinite-population approximation: it describes which identities the completed
encounters favour under proportional reproduction. It is not a Moran process and
not an estimate of fixation probabilities.
"""
import json

import numpy as np

from phase3.analyze_phase3 import ATTITUDES
from phase3.posthoc_common_v1 import MODEL_LABELS, OUT, load_primary, write_json

OUTPUT = OUT / 'ecological_v1.json'
CHECKPOINTS = (0, 10, 50, 100, 500, 1000, 5000)


def shares(x, keys):
    out = {}
    for k in sorted(set(keys)):
        out[k] = float(x[[i for i, kk in enumerate(keys) if kk == k]].sum())
    return out


def run(P, x, generations):
    history = {}
    for g in range(generations + 1):
        if g in CHECKPOINTS:
            history[g] = x.copy()
        f = P @ x
        x = x * f / (x @ f)
    return x, history


def main():
    if OUTPUT.exists():
        raise FileExistsError('Output exists; inspect before rerunning')
    data = load_primary()
    P = data['payoff']
    models, attitudes = data['models'], data['attitudes']
    n = len(models)
    result = {'status': 'post hoc descriptive ecological dynamics; not preregistered', 'starts': {}}
    starts = {'equal_identities': np.full(n, 1 / n)}
    # Equal attitude thirds, then equal models within attitude, then equal identities within cell.
    w = np.zeros(n)
    for a in ATTITUDES:
        for m in set(models):
            ix = [i for i in range(n) if models[i] == m and attitudes[i] == a]
            w[ix] = (1 / 3) / 8 / len(ix)
    starts['equal_attitudes_models_cells'] = w
    for name, x0 in starts.items():
        x, hist = run(P, x0, max(CHECKPOINTS))
        top = np.argsort(-x)[:10]
        result['starts'][name] = {
            'checkpoints': {str(g): {'by_attitude': shares(h, attitudes),
                                     'by_model': shares(h, models)} for g, h in hist.items()},
            'final_mean_payoff': float(x @ P @ x),
            'final_top_identities': [{'id': data['ids'][i], 'share': float(x[i])} for i in top],
        }
    write_json(OUTPUT, result)
    for name, r in result['starts'].items():
        print(name, json.dumps({g: {k: round(v, 3) for k, v in c['by_attitude'].items()}
                                for g, c in r['checkpoints'].items()}))
        print('  models@5000', {MODEL_LABELS[k]: round(v, 3) for k, v in r['checkpoints']['5000']['by_model'].items()})
        print('  top', [(t['id'].split('/')[0] + '/' + t['id'].split('/')[-1], round(t['share'], 3)) for t in r['final_top_identities'][:6]])


if __name__ == '__main__':
    main()
