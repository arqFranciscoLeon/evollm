"""Outcome-blind selection; timing diagnostics only, never confirmatory matrices."""
import ast
from collections import defaultdict
import itertools
import json
from pathlib import Path
import shutil
import time

import axelrod as axl
import numpy as np
from phase3.execute_uniform import load_field, digest
from phase3.interpretation_sensitivity_v1 import load_scenario, PLAN
from phase3.runtime import ROOT, play_pair, seed_for
from phase3.analyze_phase3 import permutation_test


def schedule(field):
    cells=defaultdict(list)
    for sid in sorted(field.players):
        cells[(sid.split('/')[0],sid.split('/')[-1].split('_')[0])].append(sid)
    result=[]
    for left,right in itertools.combinations_with_replacement(sorted(cells),2):
        a=sorted(cells[left],key=lambda x:digest(x.encode()))
        b=sorted(cells[right],key=lambda x:digest(x.encode()))
        pair=tuple(sorted((a[0],b[1] if left==right else b[0])))
        weight=len(a)*(len(a)-1)//2 if left==right else len(a)*len(b)
        result.append({'pair':pair,'population_pairs':weight,'kind':'distinct'})
    for key in sorted(cells):
        sid=min(cells[key],key=lambda x:digest(x.encode()))
        result.append({'pair':(sid,sid),'population_pairs':len(cells[key]),'kind':'self'})
    return result


def main():
    output=ROOT/'phase3/validation/resources_calibration_v1.json'
    if output.exists(): raise ValueError('Calibration already exists; do not overwrite')
    field=load_field(); alternate=load_scenario(15,field)
    plan=json.loads(PLAN.read_bytes())
    entries=list(field.records.values())+plan['alternatives']
    calls=set(); attributes=set()
    for row in entries:
        data=(ROOT/row['source_path']).read_bytes()
        if digest(data)!=row['source_sha256']: raise ValueError('Source changed')
        tree=ast.parse(data.decode())
        calls.update(ast.unparse(n.func) for n in ast.walk(tree) if isinstance(n,ast.Call))
        attributes.update(ast.unparse(n) for n in ast.walk(tree) if isinstance(n,ast.Attribute))
    forbidden=[x for x in calls|attributes if any(k in x.lower() for k in ('random','time','uuid','urandom'))]
    if forbidden: raise ValueError('Determinism requires review: '+str(forbidden))
    selected=schedule(field)
    assert len(selected)==324 and sum(x['population_pairs'] for x in selected)==163878
    timings=[]
    for i,item in enumerate(selected):
        first,second=item['pair']; start=time.perf_counter()
        play_pair(field.players[first],field.players[second],1000,seed_for(20260913,first,second,0))
        timings.append({**item,'seconds':time.perf_counter()-start})
        if (i+1)%81==0: print(json.dumps({'timing_matches':i+1}),flush=True)
    # Explicit trajectory checks, with fresh instances, for four alternatives and four main identities.
    checks=[]
    for row in plan['alternatives']:
        sid=row['id']; opponent=next(x for x in sorted(field.players) if x.split('/')[0]!=sid.split('/')[0])
        for label,players in [('primary',field.players),('alternative',alternate.players)]:
            hashes=[]
            for seed in [20260913,20260921]:
                trace=axl.Match((players[sid](),players[opponent]()),turns=1000,
                                game=axl.Game(r=3,s=0,t=5,p=1),noise=0,seed=seed).play()
                hashes.append(digest(''.join(str(a)+str(b) for a,b in trace).encode()))
            assert hashes[0]==hashes[1]
            checks.append({'id':sid,'field':label,'opponent':opponent,'trace_hashes':hashes,'same':True})
    ids=sorted(field.players); models=[x.split('/')[0] for x in ids]; attitudes=[x.split('/')[-1].split('_')[0] for x in ids]
    rng=np.random.default_rng(20260921); matrix=rng.random((572,572)); matrix=(matrix+matrix.T)/2
    start=time.perf_counter(); permutation_test(matrix,models,attitudes,permutations=20,seed=20260913)
    permutation_seconds=time.perf_counter()-start
    historical=json.loads((ROOT/'phase3/validation/uniform_integration_v1.json').read_bytes())
    sqlite_bytes=(ROOT/'phase3/validation/uniform_integration_v1.sqlite').stat().st_size
    weighted=sum(x['seconds']*x['population_pairs'] for x in timings)
    historical_estimate=historical['elapsed_seconds']/580*163878
    dependencies=['phase3/calibrate_resources_v1.py','phase3/inputs/sensitivity_plan_v1.json',
                  'phase3/execute_uniform.py','phase3/runtime.py','phase3/uniform_semantics_v3b.py',
                  'phase3/analyze_phase3.py','phase3/validation/uniform_integration_v1.json']
    report={'status':'diagnostic_timing_not_confirmatory','participants':572,'sources_audited':len(entries),
            'source_calls':sorted(calls),'source_attributes':sorted(attributes),'forbidden_nondeterministic_access':forbidden,
            'selection':'One hash-ordered representative per unordered model/attitude cell pair plus one self per cell; chosen without outcomes.',
            'timings':timings,'seed_checks':checks,'timing_matches':324,'seed_check_matches':16,
            'weighted_full_schedule_seconds':weighted,'historical_full_schedule_seconds':historical_estimate,
            'planning_seconds_per_scenario':3*max(weighted,historical_estimate),
            'planning_rule':'Three times the larger point estimate; engineering reserve, not a statistical bound or guarantee.',
            'synthetic_permutations':20,'synthetic_permutation_seconds':permutation_seconds,
            'projected_10000_permutation_seconds':permutation_seconds*500,
            'estimated_sqlite_bytes_per_scenario':sqlite_bytes/580*163878,
            'free_disk_bytes':shutil.disk_usage(ROOT).free,'provenance':field.provenance,
            'dependencies':{p:digest((ROOT/p).read_bytes()) for p in dependencies},
            'api_calls':0,'confirmatory_matches':0}
    with output.open('x',encoding='utf-8') as f: json.dump(report,f,indent=2)
    print(json.dumps({k:report[k] for k in ['weighted_full_schedule_seconds','historical_full_schedule_seconds','planning_seconds_per_scenario','projected_10000_permutation_seconds','estimated_sqlite_bytes_per_scenario']}),flush=True)


if __name__=='__main__': main()
