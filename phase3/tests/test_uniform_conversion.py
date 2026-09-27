import json
import pytest
from phase3 import uniform_converter as uc
from phase3.pilot_converter import ROOT, encoded
from phase3.prepare_uniform_conversion import MODEL
from phase3.review_semantics import extract_comment

def response(model=MODEL,finish='stop',usage=True):
    data={'model':model,'service_tier':'default','choices':[{'finish_reason':finish,
          'message':{'content':'def strategy(self, opponent):\n    return axl.Action.D\n'}}]}
    if usage: data['usage']={'prompt_tokens':100,'completion_tokens':20,'total_tokens':120}
    return encoded(data)

def test_all_572_have_identical_contract_and_parameters():
    plan,_=uc.load_plan(); boilerplate=set(); options=set()
    assert len(plan['requests'])==572 and len(plan['excluded'])==28
    assert plan['by_cohort']=={'western':274,'chinese':298}
    assert len({r['id'] for r in plan['requests']})==572
    for item in plan['requests']:
        model,_,name=item['id'].split('/')
        prose=extract_comment(ROOT/f'phase3/inputs/archived/{model}_default_75.py',name)
        text=item['payload']['messages'][1]['content']
        assert text.count(prose)==1
        assert uc.sha(prose.encode())==item['prose_sha256']
        boilerplate.add(text.replace(prose,'<ARCHIVED_PROSE>'))
        options.add(encoded({k:v for k,v in item['payload'].items() if k!='messages'}))
        assert item['payload']['model']==MODEL
    assert len(boilerplate)==len(options)==1

def test_resume_settles_and_does_not_repeat(tmp_path):
    sent=[]
    def send(p,k): sent.append(p); return 200,response(),'mock'
    a=uc.run(tmp_path,send,'dummy',max_new=1)
    b=uc.run(tmp_path,send,'dummy',max_new=1)
    assert a['completed']==1 and b['completed']==2 and len(sent)==2
    assert b['reserved_nano_usd']==0 and b['settled_nano_usd']==330000

@pytest.mark.parametrize('body',[response(model='gpt-5.4-mini'),response(model='different-model'),response(usage=False)])
def test_unknown_model_or_usage_stops_and_keeps_reserve(tmp_path,body):
    with pytest.raises(RuntimeError): uc.run(tmp_path,lambda p,k:(200,body,None),'dummy',max_new=2)
    plan,_=uc.load_plan(); s=uc.ledger(tmp_path,plan)
    assert s['blocked'] and s['attempts']==1 and s['reserved_nano_usd']==uc.RESERVE

def test_network_uncertainty_never_retries(tmp_path):
    calls=[]
    def send(p,k): calls.append(1); raise TimeoutError('test')
    with pytest.raises(RuntimeError): uc.run(tmp_path,send,'dummy',max_new=2)
    with pytest.raises(RuntimeError): uc.run(tmp_path,send,'dummy',max_new=2)
    assert len(calls)==1

def test_budget_stops_before_next_request(tmp_path,monkeypatch):
    monkeypatch.setattr(uc,'CEILING',uc.RESERVE+1)
    result=uc.run(tmp_path,lambda p,k:(200,response(),None),'dummy',max_new=2)
    assert result['stop_reason']=='budget_ceiling' and result['attempts']==1

def test_truncation_settles_known_usage_but_blocks(tmp_path):
    with pytest.raises(RuntimeError):
        uc.run(tmp_path,lambda p,k:(200,response(finish='length'),None),'dummy',max_new=2)
    plan,_=uc.load_plan(); s=uc.ledger(tmp_path,plan)
    assert s['blocked'] and s['settled_nano_usd']==165000

def test_attempt_572_resumes_to_complete_without_call(tmp_path):
    # Isolate end-of-plan loop boundary; receipt integrity is exercised above.
    from unittest.mock import patch
    state={'attempts':572,'completed':572,'settled_nano_usd':0,'reserved_nano_usd':0,'blocked':False}
    with patch.object(uc,'ledger',return_value=state):
        r=uc.run(tmp_path,lambda p,k:pytest.fail('No 573rd request'),'dummy')
    assert r['stop_reason']=='complete'
