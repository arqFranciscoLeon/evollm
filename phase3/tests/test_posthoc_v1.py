"""Checks for the post hoc (not preregistered) analysis helpers."""
import axelrod as axl
import numpy as np

from phase3.analyze_phase3 import _statistic, h7_statistic
from phase3.posthoc_common_v1 import PROBES, play_actions, probe_seed
from phase3.posthoc_exclusions_v1 import envelope
from phase3.posthoc_h7_structure_v1 import covariance_prediction


def synthetic(seed=3, models=4, per_cell=5):
    rng = np.random.default_rng(seed)
    labels = [f'm{m}' for m in range(models) for _ in range(3 * per_cell)]
    atts = [a for _ in range(models) for a in ('Aggressive', 'Cooperative', 'Neutral') for _ in range(per_cell)]
    return labels, atts, rng


def test_covariance_identity_matches_statistic_under_product_model():
    models, attitudes, rng = synthetic()
    u = rng.uniform(0.05, 0.95, len(models))
    c = np.outer(u, u)
    mc = np.array([int(m[1:]) for m in models])
    ac = np.array([('Aggressive', 'Cooperative', 'Neutral').index(a) for a in attitudes])
    k = len(set(models))
    x = c.copy()
    np.fill_diagonal(x, 0)
    observed, strata = _statistic(x, mc, ac, k)
    predicted, _ = covariance_prediction(u, mc, ac, k)
    assert np.allclose(strata, predicted, atol=1e-12)
    # heterogeneity alone yields a positive statistic in expectation-free, exact form
    assert np.isclose(observed, np.mean(predicted), atol=1e-12)


def test_envelope_collapses_to_statistic_without_missing_identities():
    models, attitudes, rng = synthetic(per_cell=25)
    raw = rng.uniform(0, 1, (len(models), len(models)))
    c = (raw + raw.T) / 2
    own = lambda X: [i for i, (m, a) in enumerate(zip(models, attitudes)) if (m, a) == X]
    e = envelope(c, models, attitudes, own)
    assert np.isclose(e['lower'], h7_statistic(c, models, attitudes))
    assert np.isclose(e['upper'], h7_statistic(c, models, attitudes))


def test_probe_sequences_do_not_depend_on_the_focal_classifier():
    """Regression test for the axl.Random seeding artefact found on 2026-09-28."""
    class StochasticTFT(axl.TitForTat):
        classifier = {**axl.TitForTat.classifier, 'stochastic': True}
    for name, factory in PROBES:
        _, seen_by_plain = play_actions(axl.TitForTat, factory, probe_seed(name), turns=200)
        _, seen_by_stochastic = play_actions(StochasticTFT, factory, probe_seed(name), turns=200)
        mine_plain, _ = play_actions(axl.TitForTat, factory, probe_seed(name), turns=200)
        mine_stochastic, _ = play_actions(StochasticTFT, factory, probe_seed(name), turns=200)
        assert seen_by_plain == seen_by_stochastic, name
        assert mine_plain == mine_stochastic, name
