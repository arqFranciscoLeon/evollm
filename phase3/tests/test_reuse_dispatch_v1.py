import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import pytest
import axelrod as axl
from phase3 import reuse_dispatch_v1 as dispatcher
from phase3.reuse_batches_v1 import make_context,batches,sha,encoded,execute_batch,save_receipt


def setup_plan(tmp_path):
    plan=tmp_path/'plan'; plan.mkdir()
    context=make_context({0:{'a':'C','b':'D','c':'C'}},provenance={'synthetic':True},scope='synthetic_test',turns=3)
    (plan/'context.json').write_text(encoded(context))
    entries=[]
    for batch in batches(context,size=2):
        path=plan/f'b{batch["index"]}.json'; path.write_text(encoded(batch))
        entries.append({'path':path.name,'file_sha256':dispatcher.file_sha(path)})
    (plan/'manifest.json').write_text(encoded({'context_sha256':sha(context),'batches':entries}))
    registration=tmp_path/'registration.json'
    registration.write_text(encoded({'context_sha256':sha(context),'plan_manifest_sha256':dispatcher.file_sha(plan/'manifest.json'),
                                    'public_registration_url':'synthetic-test-only','frozen_git_commit':'synthetic-test-only'}))
    return plan,registration


def fake_execute(args):
    context_path,batch_path,out,_=args
    context=json.loads(Path(context_path).read_bytes()); batch=json.loads(Path(batch_path).read_bytes())
    previous=json.loads(Path(out).read_bytes()) if Path(out).exists() else None
    result=execute_batch(batch,context,lambda sid,source:axl.Cooperator if source=='C' else axl.Defector,
                         previous=previous,checkpoint=lambda r:save_receipt(out,r))
    return {'matches':len(result['results']),'batch_sha256':result['batch_sha256']}


def test_bounded_dispatch_and_resume(tmp_path,monkeypatch):
    plan,registration=setup_plan(tmp_path); output=tmp_path/'results'
    monkeypatch.setattr(dispatcher,'ProcessPoolExecutor',lambda max_workers,mp_context:ThreadPoolExecutor(max_workers=max_workers))
    monkeypatch.setattr(dispatcher,'execute_one',fake_execute)
    first=dispatcher.dispatch(plan,output,registration,workers=2,max_batches=1)
    assert len(first['completed_batches'])==1
    second=dispatcher.dispatch(plan,output,registration,workers=2,max_batches=3)
    assert len(second['completed_batches'])==2
    assert dispatcher.dispatch(plan,output,registration,max_batches=3)['completed_batches']==[]
    assert not (output/'coordinator.lock').exists()


def test_tampered_plan_or_missing_registration_never_starts(tmp_path):
    plan,registration=setup_plan(tmp_path)
    data=json.loads(registration.read_bytes()); data['public_registration_url']=''
    registration.write_text(encoded(data))
    with pytest.raises(ValueError,match='registration'): dispatcher.dispatch(plan,tmp_path/'results',registration)
    data['public_registration_url']='synthetic-only'; registration.write_text(encoded(data))
    (plan/'b0.json').write_text('{}')
    with pytest.raises(ValueError,match='Batch file changed'): dispatcher.dispatch(plan,tmp_path/'results',registration)


def test_second_coordinator_is_rejected(tmp_path):
    plan,registration=setup_plan(tmp_path); out=tmp_path/'results'; out.mkdir()
    (out/'coordinator.lock').write_text('existing-owner')
    with pytest.raises(ValueError,match='ownership'): dispatcher.dispatch(plan,out,registration)


def test_failure_stops_new_submissions_and_preserves_report(tmp_path,monkeypatch):
    plan,registration=setup_plan(tmp_path); out=tmp_path/'results'; called=[]
    monkeypatch.setattr(dispatcher,'ProcessPoolExecutor',lambda max_workers,mp_context:ThreadPoolExecutor(max_workers=max_workers))
    def fail(args): called.append(args); raise RuntimeError('injected worker failure')
    monkeypatch.setattr(dispatcher,'execute_one',fail)
    with pytest.raises(RuntimeError): dispatcher.dispatch(plan,out,registration,workers=1,max_batches=3)
    assert len(called)==1
    assert json.loads((out/'last_dispatch.json').read_bytes())['failed_batches']
    assert not (out/'coordinator.lock').exists()
