"""Independent pair enumeration and real-size synthetic H7 checks; no games."""
import itertools
import json
from pathlib import Path

import numpy as np
import pytest

from phase3 import analyze_phase3 as analysis


def labels(counts):
    models, attitudes = [], []
    for model, sizes in counts.items():
        for attitude, size in zip(analysis.ATTITUDES, sizes):
            models.extend([model] * size)
            attitudes.extend([attitude] * size)
    return models, attitudes


def enumerated_contrasts(c, models, attitudes):
    """Enumerate unordered encounters instead of multiplying cell matrices."""
    pairs = list(itertools.combinations(range(len(models)), 2))
    result = []
    for a, b in itertools.combinations_with_replacement(analysis.ATTITUDES, 2):
        per_model = []
        for m in sorted(set(models)):
            inside = [c[i, j] for i, j in pairs if models[i] == models[j] == m
                      and sorted((attitudes[i], attitudes[j])) == sorted((a, b))]
            outside_models = []
            for k in sorted(set(models) - {m}):
                orientations = []
                for left, right in ((a, b), (b, a)):
                    encounters = [c[i, j] for i, j in pairs
                        if ((models[i], attitudes[i]) == (m, left)
                            and (models[j], attitudes[j]) == (k, right))
                        or ((models[j], attitudes[j]) == (m, left)
                            and (models[i], attitudes[i]) == (k, right))]
                    orientations.append(sum(encounters) / len(encounters))
                outside_models.append(sum(orientations) / 2)
            per_model.append(sum(inside) / len(inside) - sum(outside_models) / len(outside_models))
        result.append(sum(per_model) / len(per_model))
    return result


def test_unequal_groups_keep_equal_model_weight_not_pair_weight():
    models, attitudes = labels({'small': (2, 3, 4), 'large': (5, 6, 7)})
    c = np.array([[.9 if m == k == 'small' else .2 if m == k else .1
                   for k in models] for m in models])
    np.fill_diagonal(c, np.nan)
    assert analysis.h7_statistic(c, models, attitudes) == pytest.approx(.45)
    pooled_within = np.mean([c[i, j] for i, j in itertools.combinations(range(len(models)), 2)
                            if models[i] == models[j]])
    assert not np.isclose(pooled_within - .1, .45)
    # Validation must not edit the caller's matrix.
    assert np.isnan(np.diag(c)).all()


def test_unequal_statistic_matches_independent_pair_enumeration_and_reordering():
    models, attitudes = labels({'a': (2, 3, 5), 'b': (4, 2, 3), 'c': (3, 5, 2)})
    rng = np.random.default_rng(427)
    matrix = rng.random((len(models), len(models)))
    matrix = (matrix + matrix.T) / 2
    np.fill_diagonal(matrix, np.nan)
    expected = enumerated_contrasts(matrix, models, attitudes)
    observed, strata = analysis._statistic(*analysis.validate_matrix(matrix, models, attitudes))
    assert strata == pytest.approx(expected, abs=1e-12)
    assert observed == pytest.approx(sum(expected) / 6, abs=1e-12)
    order = rng.permutation(len(models))
    assert analysis.h7_statistic(matrix[np.ix_(order, order)],
        [models[i] for i in order], [attitudes[i] for i in order]) == pytest.approx(observed)


@pytest.mark.parametrize('sizes', [(0, 3, 4), (1, 3, 4)])
def test_missing_or_singleton_model_attitude_cell_rejected(sizes):
    models, attitudes = labels({'a': sizes, 'b': (3, 4, 5)})
    with pytest.raises(ValueError, match='At least two strategies'):
        analysis.h7_statistic(np.full((len(models), len(models)), .5), models, attitudes)


@pytest.mark.parametrize('bad', [np.nan, np.inf, -.01, 1.01])
def test_unequal_panel_still_rejects_invalid_off_diagonal(bad):
    models, attitudes = labels({'a': (2, 3, 4), 'b': (5, 4, 3)})
    c = np.full((len(models), len(models)), .5)
    c[0, 1] = c[1, 0] = bad
    with pytest.raises(ValueError, match='Missing or invalid'):
        analysis.h7_statistic(c, models, attitudes)


def test_asymmetry_and_metadata_mismatch_remain_errors():
    models, attitudes = labels({'a': (2, 3, 4), 'b': (5, 4, 3)})
    c = np.full((len(models), len(models)), .5)
    c[0, 1] = .6
    with pytest.raises(ValueError, match='symmetric'):
        analysis.h7_statistic(c, models, attitudes)
    with pytest.raises(ValueError, match='shape mismatch'):
        analysis.h7_statistic(c, models[:-1], attitudes)


def test_unequal_permutation_test_reproducible_and_uses_add_one_p_value():
    models, attitudes = labels({'a': (2, 3, 4), 'b': (4, 2, 3)})
    c = np.full((len(models), len(models)), .37)
    first = analysis.permutation_test(c, models, attitudes, permutations=31, seed=81)
    assert first == analysis.permutation_test(c, models, attitudes, permutations=31, seed=81)
    assert first['difference'] == pytest.approx(0, abs=1e-12)
    assert first['p_one_sided'] == 1
    assert first['null_interval95'] == pytest.approx([0, 0], abs=1e-12)


def test_real_572_population_synthetic_matrix_and_all_24_permutation_margins():
    manifest = json.loads((Path(__file__).parents[1] /
        'validation/uniform_derived_candidates_v1.json').read_bytes())
    models = [r['id'].split('/')[0] for r in manifest['candidates']]
    attitudes = [r['id'].split('/')[-1].split('_')[0] for r in manifest['candidates']]
    assert len(models) == 572
    assert [attitudes.count(a) for a in analysis.ATTITUDES] == [172, 200, 200]
    c = np.array([[.8 if m == k else .2 for k in models] for m in models])
    np.fill_diagonal(c, np.nan)
    assert analysis.h7_statistic(c, models, attitudes) == pytest.approx(.6)
    _, mc, ac, model_count = analysis.validate_matrix(c, models, attitudes)
    expected = np.bincount(mc * 3 + ac, minlength=model_count * 3)
    assert expected.min() == 9
    rng = np.random.default_rng(20260913)
    for _ in range(100):
        shuffled = analysis.permute_within_attitude(mc, ac, rng)
        assert np.array_equal(np.bincount(shuffled * 3 + ac, minlength=24), expected)
    # Exercise the complete inference path at real size without tournament data.
    result = analysis.permutation_test(c, models, attitudes, permutations=9, seed=81)
    assert result['difference'] == pytest.approx(.6)
    assert result['p_one_sided'] == pytest.approx(.1)
