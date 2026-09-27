"""Validate inspected derived sources; preserves original Chinese audit artifacts."""
import ast
import json
from pathlib import Path
import axelrod as axl
from phase3.chinese_semantics import Reference
from phase3.runtime import read_manifest, configure_strict, load_library, seed_for
from phase3.pilot_converter import ROOT, sha, encoded, exclusive, now

class AdjudicatedReference:
    def __init__(self,sid,alternative):
        self.sid=sid; self.alternative=alternative; self.permanent=False
    def step(self,mine,opp):
        n=len(opp)
        if 'kimi_k25' in self.sid:
            if not n: return 'D'
            index=2 if self.alternative else 1
            if n>=index and mine[-index]=='C' and opp[-1]=='D': self.permanent=True
            return 'D' if self.permanent else opp[-1]
        if not n or n+1>=991: return 'D'
        pair=mine[-1]+opp[-1]
        if pair=='DD': return 'C'
        if pair in ('DC','CD'): return 'D'
        window=9 if self.alternative else 10
        return 'D' if n>=window and all(a==b=='C' for a,b in zip(mine[-window:],opp[-window:])) else 'C'

def check(cls,factory,mine,opp,on_policy=False):
    a,b=cls(),axl.Cooperator(); ref=factory(); own=''; failures=[]; count=0
    for n in range(len(opp)+1):
        prior=own if on_policy else mine[:n]
        expected=ref.step(prior,opp[:n]); actual=str(a.strategy(b)); count+=1
        if expected!=actual:
            failures.append({'round':n+1,'own':prior,'opponent':opp[:n],'expected':expected,'actual':actual}); break
        if n<len(opp):
            x=actual if on_policy else mine[n]; y=opp[n]
            aa=axl.Action.C if x=='C' else axl.Action.D; bb=axl.Action.C if y=='C' else axl.Action.D
            a.update_history(aa,bb); b.update_history(bb,aa); own+=x
    return {'checks':count,'failures':failures}

def main():
    resolution_path=ROOT/'phase3/inputs/chinese_resolution_v1.json'
    resolution=json.loads(resolution_path.read_bytes())
    if resolution['policy_sha256']!=sha((ROOT/'phase3/CHINESE_RESOLUTION_POLICY_v1.md').read_bytes()): raise ValueError('Policy changed')
    review_path=ROOT/'phase3/inputs/semantic_review_chinese_v1.json'
    review=json.loads(review_path.read_bytes()); reviewed={r['id']:r for r in review['cases']}
    audit_path=ROOT/'phase3/validation/chinese_audit_v1.json'; audit=json.loads(audit_path.read_bytes())
    manifest=read_manifest(); common=configure_strict(manifest); classes={}
    for lib in manifest['libraries']:
        if lib['model'] in review['by_model'] and lib['prompt']=='default': classes.update(load_library(lib))
    scenarios=[(s['own'],s['opponent']) for s in audit['scenarios']]
    scenarios += [('C','D'),('CD','CD'),('CC','CD'),('CCC','DCC'),('C'*9,'C'*9),('C'*10,'C'*10),
                  ('D'*3+'C'+'D'+'C'*5,'CCC'+'D'+'C'*6)]
    opponents=[axl.Cooperator,axl.Defector,axl.Random,axl.TitForTat,axl.Grudger,axl.CyclerDDC,
               axl.CyclerCCD,axl.GoByMajority,axl.SuspiciousTitForTat,axl.Prober,axl.WinStayLoseShift]
    results=[]
    for item in resolution['derivations']:
        source=(ROOT/item['derived_path']).read_bytes()
        if sha(source)!=item['derived_sha256']: raise ValueError('Inspected source changed')
        tree=ast.parse(source.decode())
        if len(tree.body)!=1 or not isinstance(tree.body[0],ast.FunctionDef) or tree.body[0].decorator_list:
            raise ValueError('Expected inspected single function')
        namespace={'axl':axl}; exec(compile(tree,item['derived_path'],'exec'),namespace)
        cls=type('Resolved_'+classes[item['id']].__name__,(classes[item['id']],),{'strategy':common.auto_update_score(namespace['strategy'])})
        if item['kind']=='implementation_correction':
            factory=lambda profile=reviewed[item['id']]['profile']: Reference(profile)
        else:
            factory=lambda sid=item['id'],alt=item['kind']=='adjudicated_alternative': AdjudicatedReference(sid,alt)
        checks=[{'scenario':i,'mode':'controlled',**check(cls,factory,a,b)} for i,(a,b) in enumerate(scenarios)]
        checks += [{'scenario':i,'mode':'candidate_on_policy',**check(cls,factory,'',opp,True)} for i,opp in enumerate(audit['on_policy_opponents'])]
        matches=[]
        for opponent in opponents:
            seed=seed_for(20260913,item['id'],opponent.__name__)
            history=axl.Match((cls(),opponent()),turns=1000,game=axl.Game(r=3,s=0,t=5,p=1),noise=0,seed=seed).play()
            matches.append({'opponent':opponent.__name__,'seed':seed,'turns':len(history),'pass':len(history)==1000})
        passed=not any(c['failures'] for c in checks) and all(m['pass'] for m in matches)
        results.append({'id':item['id'],'kind':item['kind'],'derived_sha256':sha(source),'checks':checks,'matches':matches,'pass':passed})
        print(json.dumps({'id':item['id'],'kind':item['kind'],'pass':passed}),flush=True)
    report={'created_at':now(),'resolution_sha256':sha(resolution_path.read_bytes()),'original_audit_sha256':sha(audit_path.read_bytes()),
            'validator_sha256':sha(Path(__file__).read_bytes()),'reference_sha256':sha((ROOT/'phase3/chinese_semantics.py').read_bytes()),
            'runtime_sha256':sha((ROOT/'phase3/runtime.py').read_bytes()),'results':results,'all_pass':all(r['pass'] for r in results),
            'scope':'Local derived code, not new model responses or the mixed tournament; targeted checks only.', 'api_calls':0}
    report_path=ROOT/'phase3/validation/chinese_resolution_v1.json'; exclusive(report_path,encoded(report))
    if report['all_pass']:
        overrides={x['id']:x for x in resolution['derivations'] if x['kind']!='adjudicated_alternative'}
        excluded={r['id'] for r in resolution['excluded']}; entries=[]
        for case in review['cases']:
            if case['id'] in excluded: continue
            entry={'id':case['id'],'library_path':case['library_path'],'library_sha256':case['library_sha256'],
                   'class':case['id'].split('/')[-1],'prose_sha256':case['prose_sha256'],'derivation':'archival_original'}
            if case['id'] in overrides:
                o=overrides[case['id']]; entry.update({'derived_path':o['derived_path'],'derived_sha256':o['derived_sha256'],'derivation':o['kind']})
            entries.append(entry)
        if len(entries)!=298: raise ValueError('Unexpected eligible count')
        exclusive(ROOT/'phase3/validation/chinese_derived_candidates_v1.json',encoded({'created_at':now(),
            'resolution_validation_sha256':sha(report_path.read_bytes()),'unchanged_originals':285,
            'implementation_corrections':11,'adjudicated_primaries':2,'candidates':entries,
            'status':'archival_derived_control_not_uniform_conversion_main_field'}))
    print(json.dumps({'all_pass':report['all_pass'],'api_calls':0}))

if __name__=='__main__': main()
