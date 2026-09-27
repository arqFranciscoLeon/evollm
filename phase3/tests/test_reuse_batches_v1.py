import copy
import json
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import axelrod as axl
import numpy as np
import pytest

from phase3.execute_uniform import Field,run,export_matrices
from phase3.reuse_batches_v1 import (make_context,iter_jobs,batches,execute_batch,validate_receipt,
                                     export_scenario,save_receipt,sha)
from phase3.analyze_phase3 import h7_statistic

CLASSES={'C':axl.Cooperator,'D':axl.Defector,'T':axl.TitForTat,'G':axl.Grudger,'R':axl.Random}


def resolve(sid,source): return CLASSES[source]


def fixture(scope='synthetic_test',turns=25):
    ids=[f'{m}/default/{a}_{i}' for m in ['a','b'] for a in ['Aggressive','Cooperative','Neutral'] for i in [1,2]]
    primary={sid:['C','D','T','G','R'][i%5] for i,sid in enumerate(ids)}
    alternative={sid:('D' if primary[sid]!='D' else 'C') for sid in ids[:4]}
    scenarios={mask:{sid:(alternative[sid] if sid in alternative and mask&(1<<ids.index(sid)) else primary[sid])
                     for sid in ids} for mask in range(16)}
    return make_context(scenarios,provenance={'fixture':'repeated_sources_and_stochastic_opponents'},scope=scope,turns=turns)


def process_batch(args):
    batch,context=args
    return execute_batch(batch,context,resolve)


def test_plan_counts_and_identity_not_collapsed():
    context=fixture(); jobs=list(iter_jobs(context))
    assert len(jobs)==132  # 78 primary + 4*8 unchanged opponents + 18 pair combinations + 4 self
    assert len({j['key'] for j in jobs})==132
    assert sum(len(j['scenarios']) for j in jobs)==16*78
    assert all(j['source_i']==j['source_j'] for j in jobs if j['first']==j['second'])
    assert all(sum(mask in j['scenarios'] for j in jobs)==78 for mask in range(16))


def test_all_16_matrices_equal_independent_full_schedules(tmp_path):
    context=fixture(); pairs=[(batch,execute_batch(batch,context,resolve)) for batch in batches(context,17)]
    for mask in range(16):
        sources=context['scenario_sources'][str(mask)]
        field=Field({sid:CLASSES[s] for sid,s in sources.items()},
                    {sid:{'source_sha256':s} for sid,s in sources.items()},{'fixture':True,'mask':mask})
        path=tmp_path/f'full_{mask}.sqlite'
        run(path,field,repetitions=1,turns=context['turns'],seed=context['seed'])
        independent=export_matrices(path,field)
        reused=export_scenario(context,mask,iter(pairs))
        np.testing.assert_array_equal(independent['cooperation'],reused['cooperation'])
        np.testing.assert_array_equal(independent['payoff'],reused['payoff'])
        assert h7_statistic(reused['cooperation'],reused['models'],reused['attitudes'])==pytest.approx(
            h7_statistic(independent['cooperation'],independent['models'],independent['attitudes']))


def test_pause_resume_does_not_reexecute_saved_matches(tmp_path):
    context=fixture(); batch=next(batches(context,20)); path=tmp_path/'receipt.json'; calls=[]
    def tracked(sid,source): calls.append((sid,source)); return resolve(sid,source)
    partial=execute_batch(batch,context,tracked,max_new=3,checkpoint=lambda r:save_receipt(path,r))
    assert len(calls)==6 and len(json.loads(path.read_bytes())['results'])==3
    complete=execute_batch(batch,context,tracked,previous=partial)
    assert len(calls)==40
    assert execute_batch(batch,context,tracked,previous=complete)==complete and len(calls)==40
    assert complete==execute_batch(batch,context,resolve)


def test_process_distribution_and_reordered_collection_are_identical():
    context=fixture(); chunks=list(batches(context,30))
    expected=[execute_batch(b,context,resolve) for b in chunks]
    with ProcessPoolExecutor(max_workers=2,mp_context=multiprocessing.get_context('spawn')) as pool:
        actual=list(pool.map(process_batch,[(b,context) for b in chunks]))
    assert actual==expected
    pairs=list(zip(chunks,actual))
    np.testing.assert_array_equal(export_scenario(context,15,pairs)['cooperation'],
                                  export_scenario(context,15,reversed(pairs))['cooperation'])


def test_errors_are_checkpointed_and_block_resume():
    context=fixture(); batch=next(batches(context,3)); saved=[]
    def broken(sid,source): raise RuntimeError('deliberate fixture failure')
    with pytest.raises(RuntimeError): execute_batch(batch,context,broken,checkpoint=lambda r:saved.append(copy.deepcopy(r)))
    assert saved[0]['results'][0]['status']=='error'
    with pytest.raises(ValueError,match='Recorded error'): execute_batch(batch,context,resolve,previous=saved[0])


def test_context_change_invalidates_old_results():
    context=fixture(); batch=next(batches(context)); receipt=execute_batch(batch,context,resolve,max_new=1)
    other=fixture(turns=26)
    with pytest.raises(ValueError): execute_batch(batch,other,resolve,previous=receipt)


def test_corruption_and_false_scenario_labels_rejected():
    context=fixture(); batch=next(batches(context,5)); receipt=execute_batch(batch,context,resolve)
    bad=copy.deepcopy(receipt); bad['results'][0]['payload']['CC']+=1
    with pytest.raises(ValueError): validate_receipt(bad,batch,context)
    bad=copy.deepcopy(batch); bad['jobs'][0]['scenarios']=[]
    bad['batch_sha256']=sha({k:bad[k] for k in ('context_sha256','index','jobs')})
    with pytest.raises(ValueError,match='attribution'): execute_batch(bad,context,resolve)


def test_incomplete_and_duplicate_matrices_rejected():
    context=fixture(); batch=next(batches(context,10)); receipt=execute_batch(batch,context,resolve)
    with pytest.raises(ValueError,match='Incomplete'): export_scenario(context,0,[(batch,receipt)])
    with pytest.raises(ValueError,match='Repeated'): export_scenario(context,0,[(batch,receipt)]*2)


def test_diagnostics_cannot_be_exported():
    context=fixture('selected_diagnostic')
    with pytest.raises(ValueError): list(batches(context))
    selected=[(context['ids'][0],context['ids'][1])]
    batch=next(batches(context,pairs=selected)); receipt=execute_batch(batch,context,resolve)
    with pytest.raises(ValueError,match='Diagnostics'): export_scenario(context,0,[(batch,receipt)])


def test_scope_and_limits():
    with pytest.raises(ValueError): fixture('implicit')
    with pytest.raises(ValueError): list(batches(fixture(),0))
    full=fixture('full_round_robin')
    with pytest.raises(ValueError): list(batches(full,pairs=[(full['ids'][0],full['ids'][1])]))
