"""Post hoc structure of the registered H7 contrast (NOT preregistered).

1. Model-by-stratum decomposition of the registered statistic.
2. Leave-one-model-out values of the same statistic.
3. One exploratory permutation test without Gemini 3.1 Pro (same procedure as H7).
4. Propensity-only benchmark: a symmetric rank-one fit C_ij ~ u_i u_j has no
   same-model term by construction. Its H7 value measures how much of the
   registered contrast individual cooperation propensities alone can produce.
5. Analytic check: under C_ij = u_i u_j, each stratum contrast equals the
   between-model covariance of cell-mean propensities (minus a small within-cell
   variance term for a=b). Verified numerically.
"""
import itertools
import json

import numpy as np

from phase3.analyze_phase3 import ATTITUDES, _statistic, h7_statistic, permutation_test, validate_matrix
from phase3.posthoc_common_v1 import MODEL_LABELS, OUT, REGISTERED_H7, load_primary, write_json

PAIRS = list(itertools.combinations_with_replacement(range(3), 2))
PAIR_LABELS = [f'{ATTITUDES[a]}/{ATTITUDES[b]}' for a, b in PAIRS]
OUTPUT = OUT / 'h7_structure_v1.json'


def codes(models, attitudes):
    labels = sorted(set(models))
    return (np.array([labels.index(m) for m in models]),
            np.array([ATTITUDES.index(a) for a in attitudes]), labels)


def cell_means(c, mc, ac, k):
    """Mean off-diagonal value between the 3k model-attitude cells (diagonal ignored)."""
    c = c.copy()
    np.fill_diagonal(c, 0)
    groups = mc * 3 + ac
    one_hot = np.eye(k * 3)[groups]
    sizes = one_hot.sum(axis=0)
    return (one_hot.T @ c @ one_hot) / (np.outer(sizes, sizes) - np.diag(sizes))


def per_model_table(c, mc, ac, k):
    means = cell_means(c, mc, ac, k)
    table = np.zeros((k, len(PAIRS)))
    for p, (a, b) in enumerate(PAIRS):
        for m in range(k):
            within = means[3*m+a, 3*m+b]
            between = np.mean([(means[3*m+a, 3*o+b] + means[3*m+b, 3*o+a]) / 2
                               for o in range(k) if o != m])
            table[m, p] = within - between
    return table


def raw_statistic(c, mc, ac, k):
    """Registered statistic without the [0,1] validation (needed for residuals)."""
    c = np.asarray(c, dtype=float).copy()
    np.fill_diagonal(c, 0)
    return _statistic(c, mc, ac, k)


def rank_one(c, iterations=200):
    """Symmetric rank-one fit to the off-diagonal entries; diagonal imputed iteratively."""
    off = ~np.eye(len(c), dtype=bool)
    x = np.asarray(c, dtype=float).copy()
    for _ in range(iterations):
        w, v = np.linalg.eigh(x)
        top = np.argmax(w)
        u = v[:, top] * np.sqrt(max(w[top], 0))
        fit = np.outer(u, u)
        x = np.where(off, c, fit)
    if u.sum() < 0:
        u = -u
    fit = np.outer(u, u)
    resid = c[off] - fit[off]
    r2 = 1 - (resid**2).sum() / ((c[off] - c[off].mean())**2).sum()
    return u, fit, float(r2)


def covariance_prediction(u, mc, ac, k):
    """Stratum contrasts implied by C_ij = u_i u_j (exact identity, see docstring)."""
    ubar = np.zeros((k, 3))
    within_var = np.zeros((k, 3))
    for m in range(k):
        for a in range(3):
            x = u[(mc == m) & (ac == a)]
            ubar[m, a] = x.mean()
            within_var[m, a] = x.var() / (len(x) - 1)  # population variance / (n-1)
    strata = []
    for a, b in PAIRS:
        cov = np.cov(ubar[:, a], ubar[:, b], ddof=1)[0, 1]
        correction = within_var[:, a].mean() if a == b else 0.0
        strata.append(float(cov - correction))
    return strata, ubar


def main():
    if OUTPUT.exists():
        raise FileExistsError('Output exists; inspect before rerunning')
    data = load_primary()
    c, models, attitudes = data['cooperation'], data['models'], data['attitudes']
    mc, ac, labels = codes(models, attitudes)
    k = len(labels)

    observed, strata = raw_statistic(c, mc, ac, k)
    if observed != REGISTERED_H7:
        raise ValueError('Registered H7 not reproduced')

    table = per_model_table(c, mc, ac, k)
    loo = {}
    for drop in labels:
        keep = [i for i, m in enumerate(models) if m != drop]
        loo[drop] = h7_statistic(c[np.ix_(keep, keep)], [models[i] for i in keep],
                                 [attitudes[i] for i in keep])

    keep = [i for i, m in enumerate(models) if m != 'gemini_31_pro']
    without_pro = permutation_test(c[np.ix_(keep, keep)], [models[i] for i in keep],
                                   [attitudes[i] for i in keep], permutations=10000, seed=20260913)

    u, fit, r2 = rank_one(c)
    fit_clipped = np.clip(fit, 0, 1)
    t_prop, strata_prop = raw_statistic(fit_clipped, mc, ac, k)
    t_resid, strata_resid = raw_statistic(c - fit_clipped, mc, ac, k)
    t_unclipped, strata_unclipped = raw_statistic(fit, mc, ac, k)
    predicted, ubar = covariance_prediction(u, mc, ac, k)
    prop_test = permutation_test(fit_clipped, models, attitudes, permutations=10000, seed=20260913)

    result = {
        'status': 'post hoc, not preregistered; descriptive except where an exploratory p-value is labelled',
        'registered_h7_reproduced': observed,
        'models': labels,
        'model_labels': [MODEL_LABELS[m] for m in labels],
        'strata': PAIR_LABELS,
        'per_model_stratum_differences': table.tolist(),
        'per_model_mean_difference': table.mean(axis=1).tolist(),
        'stratum_means_check': table.mean(axis=0).tolist(),
        'models_with_negative_mean_difference': [labels[m] for m in range(k) if table[m].mean() < 0],
        'aggressive_aggressive_share_of_h7': float(table[:, 0].mean() / 6 / observed),
        'leave_one_model_out': loo,
        'exploratory_test_without_gemini_31_pro': {
            **without_pro,
            'label': 'Exploratory: same permutation procedure as H7 after removing Gemini 3.1 Pro (7 models).',
        },
        'propensity_benchmark': {
            'description': 'Symmetric rank-one fit C_ij ~ u_i u_j to off-diagonal mutual cooperation; no same-model term.',
            'r_squared_off_diagonal': r2,
            'h7_of_rank_one_fit_clipped': t_prop,
            'h7_of_residual': t_resid,
            'strata_rank_one_fit': strata_prop,
            'strata_residual': strata_resid,
            'decomposition_check': t_prop + t_resid - observed,
            'h7_of_rank_one_fit_unclipped': t_unclipped,
            'covariance_identity_prediction_unclipped': float(np.mean(predicted)),
            'covariance_identity_strata': predicted,
            'covariance_identity_max_abs_error': float(np.max(np.abs(np.array(predicted) - np.array(strata_unclipped)))),
            'cell_mean_propensities': {labels[m]: dict(zip(ATTITUDES, ubar[m].tolist())) for m in range(k)},
            'exploratory_test_on_propensity_only_matrix': {
                **prop_test,
                'label': 'Registered permutation procedure applied to the rank-one fit, which contains no same-model term.',
            },
        },
    }
    write_json(OUTPUT, result)
    summary = {
        'h7': observed, 'per_model_mean_pp': dict(zip(labels, (100 * table.mean(axis=1)).round(3).tolist())),
        'loo_pp': {m: round(100 * v, 3) for m, v in loo.items()},
        'without_pro_p': without_pro['p_one_sided'], 'without_pro_pp': without_pro['difference_pp'],
        'r2': r2, 'h7_prop_pp': 100 * t_prop, 'h7_resid_pp': 100 * t_resid,
        'identity_error': result['propensity_benchmark']['covariance_identity_max_abs_error'],
        'prop_only_p': prop_test['p_one_sided'],
    }
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
