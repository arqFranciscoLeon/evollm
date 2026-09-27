"""Verify full real schedule coverage without executing strategy actions."""
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from phase3.runtime import ROOT
from phase3.reuse_batches_v1 import check_batch,sha


def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    root=ROOT/'phase3/reuse_plan_v1'
    manifest=json.loads((root/'manifest.json').read_bytes()); context=json.loads((root/'context.json').read_bytes())
    assert sha(context)==manifest['context_sha256']
    ids=context['ids']; n=len(ids); assert n==572
    positions={sid:i for i,sid in enumerate(ids)}
    slots=n*(n+1)//2; coverage=np.zeros((16,slots),dtype=bool)
    keys=set(); counts={}; files=[]
    for entry in manifest['batches']:
        path=root/entry['path']; assert digest(path)==entry['file_sha256']
        batch=json.loads(path.read_bytes()); check_batch(batch,context)
        assert len(batch['jobs'])==entry['matches'] and batch['batch_sha256']==entry['batch_sha256']
        for job in batch['jobs']:
            assert job['key'] not in keys; keys.add(job['key'])
            i=positions[job['first']]; j=positions[job['second']]
            ordinal=i*(2*n-i+1)//2+j-i
            assert 0<=ordinal<slots
            for mask in job['scenarios']:
                assert not coverage[mask,ordinal]
                coverage[mask,ordinal]=True
        files.append(entry['path'])
    assert coverage.all() and len(keys)==166172 and len(files)==665
    for path in ['reuse_tests_v1.xml','reuse_dispatch_tests_v1.xml']:
        suite=ET.parse(ROOT/'phase3/validation'/path).getroot().find('testsuite')
        assert all(int(suite.attrib[k])==0 for k in ['errors','failures','skipped'])
        counts[path]=int(suite.attrib['tests'])
    tracked=['phase3/reuse_batches_v1.py','phase3/reuse_worker_v1.py','phase3/reuse_dispatch_v1.py',
             'phase3/prepare_reuse_plan_v1.py','phase3/verify_reuse_plan_v1.py',
             'phase3/tests/test_reuse_batches_v1.py','phase3/tests/test_reuse_dispatch_v1.py',
             'phase3/validation/reuse_tests_v1.xml','phase3/validation/reuse_dispatch_tests_v1.xml',
             'phase3/reuse_plan_v1/context.json','phase3/reuse_plan_v1/manifest.json']
    report={'status':'local_schedule_and_synthetic_execution_verified','unique_matches':len(keys),
            'logical_matches':int(coverage.sum()),'scenario_pairs':coverage.sum(axis=1).tolist(),
            'batches':len(files),'software_tests':counts,'files_sha256':{p:digest(ROOT/p) for p in tracked},
            'scope':'No real tournament games executed; process equivalence tested on synthetic strategies. Modal batch integration pending.',
            'api_calls':0,'modal_jobs':0,'confirmatory_matches':0}
    with (ROOT/'phase3/validation/reuse_closure_v1.json').open('x',encoding='utf-8') as out:
        json.dump(report,out,indent=2)
    print(json.dumps({k:report[k] for k in ['unique_matches','logical_matches','scenario_pairs','batches','software_tests']}))


if __name__=='__main__': main()
