"""Bounded cross-platform diagnostic; not a confirmatory tournament."""
import hashlib
import json
import platform
import time
from pathlib import Path
import axelrod as axl
from phase3.execute_uniform import load_field
from phase3.interpretation_sensitivity_v1 import load_scenario, PLAN
from phase3.runtime import ROOT, seed_for


def jobs(field):
    cells={}
    for sid in sorted(field.players):
        cells.setdefault((sid.split('/')[0],sid.split('/')[-1].split('_')[0]),sid)
    tasks=[]
    for (model,attitude),sid in sorted(cells.items()):
        rival=next(x for x in sorted(field.players) if x.split('/')[0]!=model)
        tasks.append((0,*sorted((sid,rival))))
    for row in json.loads(PLAN.read_bytes())['alternatives']:
        sid=row['id']; rival=next(x for x in sorted(field.players) if x.split('/')[0]!=sid.split('/')[0])
        tasks.extend([(0,*sorted((sid,rival))),(15,*sorted((sid,rival)))])
    return sorted(set(tasks))


def run_diagnostic():
    start=time.perf_counter(); primary=load_field()
    fields={0:primary,15:load_scenario(15,primary)}
    results=[]
    for mask,first,second in jobs(primary):
        players=fields[mask].players
        seed=seed_for(20260913,first,second,0)
        trace=axl.Match((players[first](),players[second]()),turns=1000,
                        game=axl.Game(r=3,s=0,t=5,p=1),noise=0,seed=seed).play()
        if len(trace)!=1000: raise ValueError('Incomplete diagnostic')
        text=''.join(str(a)+str(b) for a,b in trace)
        if set(text)-set('CD'): raise ValueError('Invalid action')
        results.append({'mask':mask,'first':first,'second':second,'seed':seed,
                        'trace_sha256':hashlib.sha256(text.encode()).hexdigest()})
    return {'scope':'cross_platform_diagnostic_only','python':platform.python_version(),
            'platform':platform.platform(),'axelrod':axl.__version__,'results':results,
            'elapsed_seconds':time.perf_counter()-start,'api_calls':0,'confirmatory_matches':0}


def check_baseline(result, baseline):
    if result['scope']!=baseline['scope'] or result['results']!=baseline['results']:
        raise ValueError('Cross-platform diagnostic differs from local baseline')


if __name__=='__main__':
    path=ROOT/'phase3/validation/modal_pilot_local_v1.json'
    if path.exists(): raise ValueError('Baseline already exists; do not repeat')
    result=run_diagnostic()
    with path.open('x',encoding='utf-8') as out: json.dump(result,out,indent=2)
    print(json.dumps({'diagnostic_matches':len(result['results']),'seconds':result['elapsed_seconds']}))
