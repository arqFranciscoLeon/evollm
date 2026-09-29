"""Behaviour-constrained bounds for the 28 excluded identities (post hoc, NOT preregistered).

The registered envelope lets every unknown encounter take any value in [0,1].
Here each unknown encounter of a missing identity from cell X with an observed
opponent j is constrained to [min, max] of c[i, j] over a reference set R_X of
observed identities (i != j); missing-missing pairs use the range over R_X x R_Y.
Two reference sets:
  own_cell        R_X = observed identities of the same model x attitude cell
  all_aggressive  R_X = all 172 observed aggressive identities (every exclusion is aggressive)
Lower bound: within-model unknowns at their minima, between-model unknowns at
their maxima (as in the registered envelope); upper bound reversed. These are
envelopes under a stated assumption, not imputations or confidence intervals.
"""
import itertools
import json

import numpy as np

from phase3.analyze_phase3 import ATTITUDES
from phase3.posthoc_common_v1 import OUT, load_primary, write_json
from phase3.sensitivity_analysis_v1 import contrast

OUTPUT = OUT / 'exclusion_bounds_v1.json'
TARGET = 25


def envelope(c, models, attitudes, reference):
    labels = sorted(set(models))
    k = len(labels)
    cells = [(m, a) for m in labels for a in ATTITUDES]
    members = {x: [i for i, (m, a) in enumerate(zip(models, attitudes)) if (m, a) == x] for x in cells}
    n = len(models)
    lo_sum = np.zeros((3 * k, 3 * k))
    hi_sum = np.zeros((3 * k, 3 * k))
    pairs = np.zeros((3 * k, 3 * k))
    for (x, X), (y, Y) in itertools.product(enumerate(cells), repeat=2):
        ox, oy = members[X], members[Y]
        kx, ky = TARGET - len(ox), TARGET - len(oy)
        observed = c[np.ix_(ox, oy)].sum() - (np.trace(c[np.ix_(ox, oy)]) if x == y else 0)
        lo, hi = observed, observed
        rx, ry = reference(X), reference(Y)

        def rng(ref, j):
            vals = [c[i, j] for i in ref if i != j]
            return min(vals), max(vals)
        if kx:
            for j in oy:
                a, b = rng(rx, j)
                lo += kx * a
                hi += kx * b
        if ky:
            for i in ox:
                a, b = rng(ry, i)
                lo += ky * a
                hi += ky * b
        mm = kx * ky - (kx if x == y else 0)
        if mm:
            vals = [c[i, j] for i in rx for j in ry if i != j]
            lo += mm * min(vals)
            hi += mm * max(vals)
        lo_sum[x, y], hi_sum[x, y] = lo, hi
        pairs[x, y] = TARGET * TARGET - (TARGET if x == y else 0)
    lo_means, hi_means = lo_sum / pairs, hi_sum / pairs
    same = np.repeat(np.arange(k), 3)
    within = same[:, None] == same[None, :]
    lower, lower_strata = contrast(np.where(within, lo_means, hi_means), k)
    upper, upper_strata = contrast(np.where(within, hi_means, lo_means), k)
    return {'lower': lower, 'upper': upper, 'lower_strata': lower_strata, 'upper_strata': upper_strata,
            'crosses_zero': lower < 0 < upper}


def main():
    if OUTPUT.exists():
        raise FileExistsError('Output exists; inspect before rerunning')
    data = load_primary()
    c, models, attitudes = data['cooperation'], data['models'], data['attitudes']
    aggressive = [i for i, a in enumerate(attitudes) if a == 'Aggressive']

    def own_cell(X):
        return [i for i, (m, a) in enumerate(zip(models, attitudes)) if (m, a) == X]

    result = {
        'status': 'post hoc behaviour-constrained envelopes; not preregistered',
        'registered_envelope_for_reference': {'lower': -0.08850333928571434, 'upper': 0.08563515277777771},
        'own_cell': envelope(c, models, attitudes, own_cell),
        'all_aggressive': envelope(c, models, attitudes, lambda X: aggressive),
    }
    write_json(OUTPUT, result)
    print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if 'strata' not in kk})
                      for k, v in result.items()}, indent=1))


if __name__ == '__main__':
    main()
