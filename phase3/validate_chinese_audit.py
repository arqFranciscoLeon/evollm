"""Audit archived Chinese behavior without repairs, network, or tournament runs."""
import itertools
import json
from pathlib import Path
import platform
import axelrod as axl
from phase3.runtime import read_manifest, configure_strict, load_library
from phase3.pilot_converter import ROOT, sha, encoded, exclusive, now
from phase3.chinese_semantics import Reference
from phase3.validate_expanded import SCENARIOS

def check(cls,profile,mine,opp,on_policy=False):
    a,b=cls(),axl.Cooperator(); oracle=Reference(profile); actual_mine=''; failures=[]; count=0
    for n in range(len(opp)+1):
        prior=actual_mine if on_policy else mine[:n]
        wanted=oracle.step(prior,opp[:n]); got=str(a.strategy(b)); count+=1
        if got!=wanted:
            failures.append({'round':n+1,'own_history':prior,'opponent_history':opp[:n],
                             'expected':wanted,'actual':got,'reachable_candidate_history':on_policy})
            # First discrepancy suffices; preserve chronological state up to it.
            break
        if n<len(opp):
            own=got if on_policy else mine[n]; other=opp[n]
            aa=axl.Action.C if own=='C' else axl.Action.D
            bb=axl.Action.C if other=='C' else axl.Action.D
            a.update_history(aa,bb); b.update_history(bb,aa); actual_mine+=own
    return {'checks':count,'failures':failures}

def main():
    review_path=ROOT/'phase3/inputs/semantic_review_chinese_v1.json'
    review=json.loads(review_path.read_bytes()); manifest=read_manifest(); configure_strict(manifest)
    cases={c['id']:c for c in review['cases']}; results=[]
    scenarios=list(SCENARIOS)
    for pairs in itertools.product(('CC','CD','DC','DD'),repeat=3):
        scenarios.append((''.join(p[0] for p in pairs),''.join(p[1] for p in pairs)))
    scenarios += [('D'*110,'C'*110),('D'*100+'C'*10,'C'*100+'D'+'C'*9),
                  ('D'*5+'C'*5,'C'*5+'D'+'C'*4),('D'*3+'C'*7,'CCC'+'D'+'C'*6),
                  ('C'*999,'D'*999),('D'*999,'D'*999),('D'*999,('DC'*500)[:999])]
    scripted=['C'*999,'D'*999,('DC'*500)[:999], 'CCC'+'D'+'C'*995,
              'C'*5+'D'+'C'*993,'C'*100+'D'+'C'*898,'D'+'CCC'+'D'*995]
    for lib in manifest['libraries']:
        if lib['prompt']!='default' or lib['model'] not in review['by_model']: continue
        classes=load_library(lib)
        for strategy_id,cls in classes.items():
            case=cases[strategy_id]
            entry={'id':strategy_id,'prose_status':case['status'],'profile':case['profile'],
                   'library_sha256':lib['sha256'],'prose_sha256':case['prose_sha256']}
            if case['status']!='eligible_prose':
                entry['status']='not_certified_pending_prose'; results.append(entry); continue
            outputs=[]
            try:
                for i,(mine,opp) in enumerate(scenarios):
                    outputs.append({'scenario':i,'mode':'controlled',**check(cls,case['profile'],mine,opp)})
                for i,opp in enumerate(scripted):
                    outputs.append({'scenario':i,'mode':'candidate_on_policy',**check(cls,case['profile'],'',opp,True)})
                entry['status']='fidelity_discrepancy' if any(o['failures'] for o in outputs) else 'passed_targeted_checks'
            except Exception as exc:
                entry['status']='runtime_diagnostic_error'; entry['error']=type(exc).__name__+': '+str(exc)
            entry['checks']=outputs; results.append(entry)
        print(json.dumps({'model':lib['model'],'reviewed':len(classes),'issues':[r['id'] for r in results if r['id'].startswith(lib['model']+'/') and r['status']!='passed_targeted_checks']}),flush=True)
    from collections import Counter
    report={'created_at':now(),'review_sha256':sha(review_path.read_bytes()),
            'validator_sha256':sha(Path(__file__).read_bytes()),
            'reference_sha256':sha((ROOT/'phase3/chinese_semantics.py').read_bytes()),
            'runtime_sha256':sha((ROOT/'phase3/runtime.py').read_bytes()),
            'python':platform.python_version(),'axelrod':axl.__version__,
            'scenarios':[{'own':a,'opponent':b} for a,b in scenarios],'on_policy_opponents':scripted,
            'summary':dict(Counter(r['status'] for r in results)),'results':results,
            'scope':'Single-review targeted fidelity audit, not exhaustive equivalence; pending prose entries are not certified. Original code preserved.',
            'api_calls':0}
    exclusive(ROOT/'phase3/validation/chinese_audit_v1.json',encoded(report))
    print(json.dumps(report['summary']))

if __name__=='__main__': main()
