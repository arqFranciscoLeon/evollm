import json
import numpy as np
import pytest
import axelrod as axl

from phase3 import analyze_phase3 as analysis
from phase3.benchmark import benchmark
from phase3.existing_evidence import winner, load_checked
from phase3.runtime import play_pair, configure_strict, read_manifest


def panel():
    models = [m for m in ('one','two','three') for a in analysis.ATTITUDES for _ in range(2)]
    attitudes = [a for m in ('one','two','three') for a in analysis.ATTITUDES for _ in range(2)]
    c = np.array([[.8 if m == n else .2 for n in models] for m in models])
    return c,models,attitudes


def test_h7_uses_pair_level_cc_and_ignores_diagonal():
    c,m,a = panel()
    assert analysis.h7_statistic(c,m,a) == pytest.approx(.6)
    np.fill_diagonal(c,np.nan)
    assert analysis.h7_statistic(c,m,a) == pytest.approx(.6)
    c[:] = .37
    assert analysis.h7_statistic(c,m,a) == pytest.approx(0)


def test_missing_match_and_singleton_stratum_rejected():
    c,m,a = panel()
    c[0,1] = c[1,0] = np.nan
    with pytest.raises(ValueError,match='Missing'):
        analysis.h7_statistic(c,m,a)
    c,m,a = panel()
    with pytest.raises(ValueError,match='At least two strategies'):
        analysis.h7_statistic(c[:-1,:-1],m[:-1],a[:-1])


def test_permutation_preserves_attitude_counts_and_is_reproducible():
    c,m,a = panel()
    _,mc,ac,_ = analysis.validate_matrix(c,m,a)
    new = analysis.permute_within_attitude(mc,ac,np.random.default_rng(3))
    for attitude in range(3):
        assert sorted(new[ac == attitude]) == sorted(mc[ac == attitude])
    first = analysis.permutation_test(c,m,a,permutations=99,seed=8)
    assert first == analysis.permutation_test(c,m,a,permutations=99,seed=8)
    assert 0 < first['p_one_sided'] <= .05


def test_classical_scores_and_mutual_cooperation():
    result = play_pair(axl.Cooperator,axl.Defector,100,7)
    assert result == {'CC':0,'CD':100,'DC':0,'DD':0,'payoff_i':0,'payoff_j':5}
    result = play_pair(axl.Cooperator,axl.Cooperator,100,7)
    assert result['CC'] == 100 and result['payoff_i'] == 3


def test_missing_return_is_not_converted_to_cooperation():
    common = configure_strict(read_manifest())
    class Broken(common.LLM_Strategy):
        attitude = common.Attitude.COOPERATIVE
        @common.auto_update_score
        def strategy(self,opponent):
            return None
    with pytest.raises(ValueError,match='invalid action None'):
        play_pair(Broken,axl.Cooperator,10,1)


def test_checkpoint_resume_and_configuration_mismatch(tmp_path):
    path = tmp_path/'matches.sqlite'
    first = benchmark(path,repetitions=1,turns=10)
    second = benchmark(path,repetitions=1,turns=10)
    assert first['new_matches'] == first['total_matches'] == 21
    assert second['new_matches'] == 0 and second['total_matches'] == 21
    with pytest.raises(ValueError,match='configuration changed'):
        benchmark(path,repetitions=2,turns=10)


def test_exact_tie_and_missing_evidence_are_not_invented(tmp_path):
    assert winner({'Aggressive':4,'Cooperative':248,'Neutral':248}) == 'Tie'
    from compare_robust import plurality
    assert plurality({'Aggressive':4,'Cooperative':248,'Neutral':248}) == 'Tie'
    empty = tmp_path/'empty.json'
    empty.write_text('[]')
    with pytest.raises(ValueError,match='Missing'):
        load_checked(empty,['model'])


def test_legacy_verifier_rejects_missing_conditions(tmp_path):
    from reproduce_tables import load_n500
    empty = tmp_path/'wrong_study.json'
    empty.write_text('[]')
    with pytest.raises(ValueError,match='Missing'):
        load_n500(empty)
    rows,_ = load_n500()
    assert len(rows) == 48
    assert rows[('anthropic_sonnet46_default_75','444')]['Aggressive'] == 10
