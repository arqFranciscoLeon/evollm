"""Prespecified descriptive sensitivities; never supplies confirmatory p-values."""
import ast
from collections import Counter
import hashlib
import itertools

import numpy as np
from phase3.analyze_phase3 import ATTITUDES, validate_matrix


def ast_group(source):
    """Exact syntax identity ignoring formatting/comments/locations, not behaviour."""
    tree = ast.dump(ast.parse(source), include_attributes=False)
    return hashlib.sha256(tree.encode()).hexdigest()


def contrast(means, model_count):
    strata = []
    for a, b in itertools.combinations_with_replacement(range(3), 2):
        values = []
        for m in range(model_count):
            between = np.mean([(means[3*m+a, 3*k+b] + means[3*m+b, 3*k+a])/2
                               for k in range(model_count) if k != m])
            values.append(means[3*m+a, 3*m+b] - between)
        strata.append(float(np.mean(values)))
    return float(np.mean(strata)), strata


def duplicate_sensitivity(cooperation, models, attitudes, syntax_groups):
    c, mc, ac, m = validate_matrix(cooperation, models, attitudes)
    if len(syntax_groups) != len(models) or any(not isinstance(x, str) or not x for x in syntax_groups):
        raise ValueError('One nonempty syntax hash per identity required')
    cells = mc*3 + ac
    counts = Counter(zip(cells.tolist(), syntax_groups))
    weights = np.array([1/counts[cell, group] for cell, group in zip(cells, syntax_groups)])
    membership = np.eye(m*3)[cells] * weights[:, None]
    mass = membership.sum(axis=0)
    # Independent template-balanced identity draws, conditioned on distinct identities.
    denominators = np.outer(mass, mass) - np.diag((membership**2).sum(axis=0))
    if np.any(denominators <= 0):
        raise ValueError('No distinct-identity pair in a cell')
    means = (membership.T @ c @ membership)/denominators
    effect, strata = contrast(means, m)
    return {'difference': effect, 'stratum_differences': strata,
            'groups_per_cell': mass.round().astype(int).tolist(),
            'interpretation': 'Descriptive AST-weighted contrast; identity diagonal excluded. No p-value or confidence interval.'}


def exclusion_bounds(cooperation, models, attitudes, target_per_cell=25):
    """Algebraic bounds with each unobserved pair allowed any CC fraction in [0,1]."""
    c, mc, ac, m = validate_matrix(cooperation, models, attitudes)
    if type(target_per_cell) is not int or target_per_cell < 2:
        raise ValueError('Integer target cell size >= 2 required')
    membership = np.eye(m*3)[mc*3 + ac]
    sizes = membership.sum(axis=0)
    if np.any(sizes > target_per_cell):
        raise ValueError('Observed cell exceeds target population')
    observed_pairs = np.outer(sizes, sizes) - np.diag(sizes)
    target = np.full(m*3, target_per_cell, dtype=float)
    total_pairs = np.outer(target, target) - np.diag(target)
    lower_means = (membership.T @ c @ membership)/total_pairs
    unknown_fraction = (total_pairs - observed_pairs)/total_pairs
    upper_means = lower_means + unknown_fraction
    # Positive coefficients within model; negative between models, for every stratum.
    same_model = np.repeat(np.arange(m), 3)
    within = same_model[:, None] == same_model[None, :]
    lower, _ = contrast(np.where(within, lower_means, upper_means), m)
    upper, _ = contrast(np.where(within, upper_means, lower_means), m)
    return {'lower': lower, 'upper': upper, 'missing_identities': int(target.sum()-sizes.sum()),
            'interpretation': 'Algebraic envelope, not a confidence interval or imputed strategies; joint behavioural attainability is not assumed.'}
