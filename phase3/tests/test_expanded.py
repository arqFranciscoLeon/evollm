import hashlib
import json
import pytest

from phase3 import expanded_converter as ec
from phase3.expanded_semantics import compile_candidate, reference, replay
from phase3.validate_expanded import profiles


def response(prompt=100,completion=20,cached=0,finish='stop'):
    return ec.encoded({'model':'gpt-5.4-mini-2026-03-17','service_tier':'default',
                       'usage':{'prompt_tokens':prompt,'completion_tokens':completion,'total_tokens':prompt+completion,
                                'prompt_tokens_details':{'cached_tokens':cached}},
                       'choices':[{'finish_reason':finish,'message':{'content':'def strategy(self, opponent):\n    return axl.Action.C\n'}}]})


def test_settlement_releases_reserve_and_resume_does_not_duplicate(tmp_path):
    calls=[]
    def send(payload,key):
        calls.append(1)
        return 200,response(cached=10),'mock'
    state=ec.run(tmp_path,send,'dummy-key',max_new=2)
    assert state['completed']==2 and state['reserved_nano_usd']==0
    assert state['settled_nano_usd']==2*(90*750+10*75+20*4500)
    state=ec.run(tmp_path,send,'dummy-key',max_new=1)
    assert len(calls)==3 and state['completed']==3


def test_budget_stops_before_next_request(tmp_path,monkeypatch):
    monkeypatch.setattr(ec,'CEILING',ec.RESERVE+1)
    calls=[]
    def send(payload,key):
        calls.append(1)
        return 200,response(),None
    state=ec.run(tmp_path,send,'dummy-key',max_new=3)
    assert len(calls)==1 and state['stop_reason']=='budget_ceiling'


def test_unknown_transport_keeps_reservation_and_stops_resume(tmp_path):
    calls=[]
    def send(payload,key):
        calls.append(1)
        raise TimeoutError('sensitive '+key)
    with pytest.raises(RuntimeError,match='uncertain'):
        ec.run(tmp_path,send,'dummy-key',max_new=1)
    plan,_=ec.load_plan()
    state=ec.ledger(tmp_path,plan)
    assert state['reserved_nano_usd']==ec.RESERVE and state['settled_nano_usd']==0
    with pytest.raises(RuntimeError,match='reconciliation'):
        ec.run(tmp_path,send,'dummy-key',max_new=1)
    assert calls==[1] and 'dummy-key' not in (tmp_path/'001/transport_error.json').read_text()


@pytest.mark.parametrize('mutate',[lambda r:r.pop('usage'),lambda r:r['usage'].update(cached_tokens=-1,prompt_tokens=-1),
                                 lambda r:r['usage'].update(total_tokens=0),lambda r:r.update(service_tier='priority')])
def test_unverifiable_usage_cannot_release_reserve(mutate):
    r=json.loads(response()); mutate(r)
    result=ec.classify(200,ec.encoded(r))
    assert result['cost_nano_usd'] is None
    assert result['charged_to_local_budget_nano_usd']==ec.RESERVE and result['status']!=ec.OK


def test_truncation_settles_known_cost_but_stops(tmp_path):
    def send(payload,key): return 200,response(finish='length'),None
    with pytest.raises(RuntimeError,match='stopped'):
        ec.run(tmp_path,send,'dummy-key',max_new=1)
    plan,_=ec.load_plan(); state=ec.ledger(tmp_path,plan)
    assert state['blocked'] and state['settled_nano_usd']==165000 and state['reserved_nano_usd']==0


def test_changed_receipt_is_detected(tmp_path):
    ec.run(tmp_path,lambda p,k:(200,response(),None),'dummy-key',max_new=1)
    receipt=tmp_path/'001/receipt.json'; data=json.loads(receipt.read_bytes()); data['cost_nano_usd']=0
    receipt.write_bytes(ec.encoded(data))
    plan,_=ec.load_plan()
    with pytest.raises(ValueError,match='settlement'):
        ec.ledger(tmp_path,plan)


def compiled(source): return compile_candidate(source,hashlib.sha256(source.encode()).hexdigest())


def test_persistent_trigger_requires_chronological_replay():
    source='''def strategy(self, opponent):
    if self.first_round():
        self.permanent = False
        return axl.Action.C
    if opponent.history.defections / len(opponent.history) > 0.55:
        self.permanent = True
    if self.permanent or opponent.history[-1] == axl.Action.D:
        return axl.Action.D
    return axl.Action.C
'''
    good=replay(compiled(source),'C'*8,'DDCCCCCC','fraction_C_55_gt_latch')
    assert not good['failures']
    mutant=source.replace('    if opponent.history.defections', '    self.permanent = False\n    if opponent.history.defections')
    bad=replay(compiled(mutant),'C'*8,'DDCCCCCC','fraction_C_55_gt_latch')
    assert bad['failures'] and bad['failures'][0]['round']==5


def test_scores_are_current_not_one_round_late():
    source='''def strategy(self, opponent):
    if self.first_round(): return axl.Action.D
    if opponent.history[-1] == axl.Action.D or len(self.history) + 1 >= 996 or self.score - opponent.score > 10:
        return axl.Action.D
    return axl.Action.C
'''
    assert not replay(compiled(source),'DDDC','CCCC','score_10_996')['failures']
    assert reference('score_10_996','DDC','CCC')=='C'
    assert reference('score_20_990','DDDDC','CCCCC')=='D'


def test_early_window_and_full_window_differ():
    assert reference('window_or_998','C','D')=='D'
    assert reference('window8of10','C'*9,'D'*8+'C')=='C'
    assert reference('window8of10','C'*10,'C'+'D'*8+'C')=='D'


def test_reviewed_hash_is_required():
    with pytest.raises(ValueError,match='inspected'):
        compile_candidate('def strategy(self, opponent): return axl.Action.C','wrong')


def test_inspected_private_latch_preserves_chronology_and_runtime_protection():
    source='''def strategy(self, opponent):
    if self.first_round():
        self._always_defect = False
        return axl.Action.C
    if opponent.history.defections / len(opponent.history) > 0.55:
        self._always_defect = True
    if self._always_defect or opponent.history[-1] == axl.Action.D:
        return axl.Action.D
    return axl.Action.C
'''
    assert not replay(compiled(source),'CCCC','DCCC','fraction_C_55_gt_latch')['failures']
    with pytest.raises(ValueError,match='state'):
        compiled(source.replace('_always_defect','_history'))


def test_all_274_profiles_have_reference_coverage():
    mapping=profiles()
    assert len(mapping)==274
    for key in set(mapping.values()):
        for mine,opp in [('', ''),('C','D'),('D'*999,'C'*999)]:
            assert reference(key,mine,opp) in ('C','D')


def test_reference_matches_frozen_semantic_vectors():
    mapping=profiles()
    vectors=json.loads((ec.ROOT/'phase3/inputs/semantic_test_vectors_v1.json').read_bytes())['cases']
    checked=0
    for case in vectors:
        if case['strategy_id'] not in mapping:
            continue
        mine=''.join(a*n for a,n in case['own_rle'])
        opponent=''.join(a*n for a,n in case['opponent_rle'])
        assert reference(mapping[case['strategy_id']],mine,opponent)==case['expected_action'], case
        checked+=1
    assert checked>=70


def test_pilot_sources_replay_under_expanded_adapter():
    from phase3.validate_expanded import SCENARIOS
    plan=json.loads((ec.ROOT/'phase3/inputs/pilot_requests_v1.json').read_bytes())
    report=json.loads((ec.ROOT/'phase3/validation/pilot_v1.json').read_bytes())
    hashes={r['strategy_id']:r['candidate_sha256'] for r in report['candidates']}
    mapping=profiles()
    for number,item in enumerate(plan['requests'],1):
        source=(ec.ROOT/f'phase3/conversion_runs/pilot_v1/{number:02d}/candidate.py.txt').read_bytes().decode('utf-8')
        cls=compile_candidate(source,hashes[item['strategy_id']])
        for mine,opponent in SCENARIOS:
            result=replay(cls,mine,opponent,mapping[item['strategy_id']])
            assert not result['failures'], (item['strategy_id'],result['failures'])
            assert len(result['actions_sha256'])==64
