"""H7 for unequal model/attitude cells under working protocol v0.3.

Cell means use actual pair counts; models and unordered attitude pairs receive
equal weight. Inference remains conditional on the eligible archived panel.
"""
import itertools
import numpy as np

ATTITUDES = ('Aggressive', 'Cooperative', 'Neutral')


def validate_matrix(cooperation, models, attitudes):
    c = np.asarray(cooperation, dtype=float).copy()
    n = len(models)
    if c.shape != (n, n) or len(attitudes) != n:
        raise ValueError('Metadata/matrix shape mismatch')
    mask = ~np.eye(n, dtype=bool)
    if not np.isfinite(c[mask]).all() or np.any((c[mask] < 0) | (c[mask] > 1)):
        raise ValueError('Missing or invalid off-diagonal cooperation')
    if not np.allclose(c[mask], c.T[mask], atol=1e-12, rtol=0):
        raise ValueError('Mutual cooperation must be symmetric')
    labs = sorted(set(models))
    if len(labs) < 2 or set(attitudes) != set(ATTITUDES):
        raise ValueError('At least two models and all three attitudes required')
    sizes = [sum(m == lab and a == att for m,a in zip(models,attitudes)) for lab in labs for att in ATTITUDES]
    if min(sizes) < 2:
        raise ValueError('At least two strategies in every model/attitude stratum required')
    np.fill_diagonal(c, 0)  # Self-play has no influence, including NaN self-play entries.
    return c, np.array([labs.index(m) for m in models]), np.array([ATTITUDES.index(a) for a in attitudes]), len(labs)


def _statistic(c, model_codes, attitude_codes, model_count):
    groups = model_codes * 3 + attitude_codes
    one_hot = np.eye(model_count * 3)[groups]
    totals = one_hot.T @ c @ one_hot
    sizes = one_hot.sum(axis=0)
    # Actual ordered pair counts, including unequal cells; remove self-pairs.
    denominators = np.outer(sizes, sizes) - np.diag(sizes)
    means = totals / denominators
    contrasts = []
    for a,b in itertools.combinations_with_replacement(range(3),2):
        per_model = []
        for m in range(model_count):
            within = means[3*m+a, 3*m+b]
            between = np.mean([(means[3*m+a,3*k+b] + means[3*m+b,3*k+a])/2
                               for k in range(model_count) if k != m])
            per_model.append(within-between)
        contrasts.append(float(np.mean(per_model)))
    return float(np.mean(contrasts)), contrasts


def h7_statistic(cooperation, models, attitudes):
    return _statistic(*validate_matrix(cooperation, models, attitudes))[0]


def permute_within_attitude(model_codes, attitude_codes, rng):
    """Shuffle existing labels, preserving every observed model/attitude count."""
    result = np.array(model_codes, copy=True)
    for attitude in range(3):
        positions = np.flatnonzero(attitude_codes == attitude)
        result[positions] = rng.permutation(result[positions])
    return result


def permutation_test(cooperation, models, attitudes, permutations=10000, seed=20260913):
    if permutations < 1:
        raise ValueError('At least one permutation required')
    c, model_codes, attitude_codes, m = validate_matrix(cooperation,models,attitudes)
    observed, strata = _statistic(c,model_codes,attitude_codes,m)
    rng = np.random.default_rng(seed)
    null = np.empty(permutations)
    for b in range(permutations):
        labels = permute_within_attitude(model_codes,attitude_codes,rng)
        null[b] = _statistic(c, labels, attitude_codes, m)[0]
    p = (1 + int(np.sum(null >= observed - 1e-12))) / (permutations + 1)
    return {'difference': observed, 'difference_pp': 100*observed, 'stratum_differences': strata,
            'p_one_sided': p, 'permutations': permutations, 'seed': seed,
            'null_interval95': np.quantile(null,[.025,.975]).tolist(),
            'interpretation': 'Permutation reference interval, NOT a confidence interval for the effect. Strategy-level labels shuffled within attitude; self-pairs excluded.'}
