import pytest
from phase3.chinese_semantics import Reference


@pytest.mark.parametrize('own,opponent,wanted',[('C','C','C'),('D','C','D'),('C','D','D'),('D','D','C')])
def test_payoff_three_or_five_stays_zero_or_one_switches(own,opponent,wanted):
    assert Reference('wsls_D_none').step(own,opponent)==wanted


def test_otherwise_defect_covers_incomplete_two_cooperation_window():
    ref=Reference('twoC_elseD')
    assert ref.step('','')=='D'
    assert ref.step('D','C')=='D'
    assert ref.step('DD','CC')=='C'


def test_trust_switch_retaliation_is_permanent():
    ref=Reference('trust3_991')
    assert ref.step('','')=='D'
    assert ref.step('DDD','CCC')=='C'
    assert ref.step('DDDC','CCCD')=='D'
    assert ref.step('DDDCD','CCCDC')=='D'


def test_probe_selects_copying_policy_not_frozen_action():
    ref=Reference('probeDC_lock')
    assert ref.step('','')=='D'
    assert ref.step('D','D')=='C'
    assert ref.step('DC','DC')=='C'
    assert ref.step('DCC','DCD')=='D'


def test_explicit_final_round_overrides_mutual_defection_and_forgiveness():
    assert Reference('dd_D_1000').step('D'*999,'D'*999)=='D'
    assert Reference('firstD_twoC').step('C'*999,'C'*998+'D')=='D'


def test_first_round_defection_in_tree_locks_rest_of_game():
    assert Reference('treeCDC').step('DD','DD')=='D'
    assert Reference('treeCDC').step('DDCC','DCCC')=='D'
