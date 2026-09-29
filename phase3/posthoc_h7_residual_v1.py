"""Exploratory permutation test of the H7 statistic on the propensity residual (NOT preregistered).

Residual = observed mutual cooperation minus the clipped rank-one propensity fit
from posthoc_h7_structure_v1. The same within-attitude, strategy-level label
permutation as H7 is applied, with the registered numerical tolerance.
"""
import json

import numpy as np

from phase3.analyze_phase3 import _statistic, permute_within_attitude
from phase3.posthoc_common_v1 import OUT, load_primary, write_json
from phase3.posthoc_h7_structure_v1 import codes, rank_one

OUTPUT = OUT / 'h7_residual_v1.json'


def main():
    if OUTPUT.exists():
        raise FileExistsError('Output exists; inspect before rerunning')
    data = load_primary()
    c = data['cooperation']
    mc, ac, labels = codes(data['models'], data['attitudes'])
    k = len(labels)
    _, fit, r2 = rank_one(c)
    residual = c - np.clip(fit, 0, 1)
    np.fill_diagonal(residual, 0)
    observed, strata = _statistic(residual, mc, ac, k)
    rng = np.random.default_rng(20260913)
    null = np.empty(10000)
    for b in range(len(null)):
        null[b] = _statistic(residual, permute_within_attitude(mc, ac, rng), ac, k)[0]
    p = (1 + int(np.sum(null >= observed - 1e-12))) / (len(null) + 1)
    result = {'status': 'post hoc exploratory test; not preregistered',
              'rank_one_r_squared': r2, 'residual_h7': observed, 'residual_h7_pp': 100 * observed,
              'residual_strata': strata, 'p_one_sided': p, 'permutations': len(null), 'seed': 20260913,
              'null_interval95': np.quantile(null, [.025, .975]).tolist()}
    write_json(OUTPUT, result)
    print(json.dumps({k: v for k, v in result.items() if k != 'residual_strata'}, indent=1))


if __name__ == '__main__':
    main()
