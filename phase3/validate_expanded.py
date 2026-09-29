"""Validate inspected expanded candidates: chronological semantic replay and runtime.

An explicit source-review manifest is required; receiving API code alone is not
approval to execute it. This tool never calls an API or changes candidate code.
"""
import argparse
import json
from pathlib import Path
import platform
import axelrod as axl

from phase3.expanded_converter import PLAN_SHA256, RUN_DIR, load_plan, ledger
from phase3.expanded_semantics import compile_candidate, replay
from phase3.pilot_converter import ROOT, encoded, exclusive, sha
from phase3.runtime import seed_for

SCENARIOS = [('', ''), ('C','C'),('C','D'),('CD','DC'),('DD','DD'),('DDD','DDD'),
             ('DDDDD','DDDCD'),('C'*7,'DDCCCCC'),('DDC','CCC'),('DDDC','CCCC'),
             ('DDDDC','CCCCC'),('C'*20,'C'*16+'DDDC'),('C'*20,'C'*15+'DDDDC'),
             ('C'*9,'D'*8+'C'),('C'*10,'C'+'D'*8+'C'),
             ('C'*999,'C'*999),('D'*999,'C'*999),('C'*999,'D'+'C'*998),
             ('C'*997+'DD','C'*997+'DD')]


def profiles():
    p=ROOT/'phase3/inputs'
    old=json.loads((p/'semantic_review_v1.json').read_bytes())['cases']
    new=json.loads((p/'semantic_review_remaining_v1.json').read_bytes())['cases']
    mapping={c['id']:c['profile'] for c in old if c['status']=='eligible_prose'}
    mapping.update({c['id']:c['profile_key'] for c in new if c['status']=='eligible_prose'})
    mapping['gemini_31_pro/default/Aggressive_12']='window_or_998'
    mapping['gemini_31_pro/default/Aggressive_14']='window_or_996'
    return mapping


def validate(review_path, output):
    plan,_=load_plan()
    state=ledger(RUN_DIR,plan)
    if state['blocked'] or state['completed']!=274:
        raise ValueError('A complete traceable expanded run is required')
    review=json.loads(review_path.read_bytes())
    if review['plan_sha256']!=PLAN_SHA256:
        raise ValueError('Review belongs to another plan')
    approved={r['id']:r for r in review['reviewed_candidates']}
    if len(approved)!=274 or len(review['reviewed_candidates'])!=274 or set(approved)!=set(profiles()):
        raise ValueError('Exactly 274 distinct source reviews required')
    mapping=profiles()
    prior_plan=json.loads((ROOT/'phase3/inputs/pilot_requests_v1.json').read_bytes())
    prior_report=json.loads((ROOT/'phase3/validation/pilot_v1.json').read_bytes())
    if sha((ROOT/'phase3/inputs/pilot_requests_v1.json').read_bytes())!=prior_report['plan_sha256']:
        raise ValueError('Prior pilot plan changed')
    prior_codes={r['strategy_id']:ROOT/f'phase3/conversion_runs/pilot_v1/{i:02d}/candidate.py.txt'
                 for i,r in enumerate(prior_plan['requests'],1)}
    prior_hashes={r['strategy_id']:r['candidate_sha256'] for r in prior_report['candidates']}
    opponents=[axl.Cooperator,axl.Defector,axl.Random,axl.TitForTat,axl.Grudger,axl.CyclerDDC,
               axl.CyclerCCD,axl.GoByMajority,axl.SuspiciousTitForTat,axl.Prober,axl.WinStayLoseShift]
    results=[]
    for number,item in enumerate(plan['requests'],1):
        entry={'id':item['id'],'semantic':[],'runtime':[]}
        source=(RUN_DIR/f'{number:03d}'/'candidate.py.txt').read_bytes().decode('utf-8')
        approval=approved[item['id']]
        if not approval.get('reviewer') or not approval.get('notes'):
            raise ValueError('Missing source-inspection attribution')
        try:
            cls=compile_candidate(source,approval['candidate_sha256'])
            for i,(mine,opp) in enumerate(SCENARIOS):
                entry['semantic'].append({'scenario':i,**replay(cls,mine,opp,mapping[item['id']])})
            if item['pilot_comparison_control']:
                old_source=prior_codes[item['id']].read_bytes().decode('utf-8')
                old_cls=compile_candidate(old_source,prior_hashes[item['id']])
                paired=[]
                for i,(mine,opp) in enumerate(SCENARIOS):
                    prior_trace=replay(old_cls,mine,opp,mapping[item['id']])
                    paired.append({'scenario':i,'same_actions':prior_trace['actions_sha256']==entry['semantic'][i]['actions_sha256']})
                entry['paired_pilot_control']={'prior_candidate_sha256':prior_hashes[item['id']],
                                               'scenarios':paired,'all_same':all(c['same_actions'] for c in paired)}
            for opponent in opponents:
                seed=seed_for(20260913,item['id'],opponent.__name__)
                match=axl.Match((cls(),opponent()),turns=1000,game=axl.Game(r=3,s=0,t=5,p=1),noise=0,seed=seed)
                history=match.play()
                entry['runtime'].append({'opponent':opponent.__name__,'seed':seed,'turns':len(history),'pass':len(history)==1000})
            entry['pass']=not any(x['failures'] for x in entry['semantic']) and all(x['pass'] for x in entry['runtime'])
        except Exception as exc:
            entry.update({'pass':False,'error':type(exc).__name__+': '+str(exc)})
        entry['candidate_sha256']=sha(source.encode())
        results.append(entry)
        print(json.dumps({'validated':number,'pass':entry['pass']}),flush=True)
    report={'plan_sha256':PLAN_SHA256,'review_sha256':sha(review_path.read_bytes()),
            'validator_sha256':sha(Path(__file__).read_bytes()),
            'semantics_sha256':sha(Path(__file__).with_name('expanded_semantics.py').read_bytes()),
            'python':platform.python_version(),'axelrod':axl.__version__,
            'scenarios':[{'own':a,'opponent':b} for a,b in SCENARIOS],
            'results':results,'all_pass':all(r['pass'] for r in results),
            'scope':'Controlled-history semantic checks and classical runtime diagnostics, not exhaustive equivalence or the mixed tournament.',
            'additional_pre_tournament_work':'Full-window sensitivity of both adjudicated strategies remains a separate mandatory pre-tournament analysis.'}
    output.parent.mkdir(parents=True,exist_ok=True)
    exclusive(output,encoded(report))
    return report['all_pass']


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviewed-sources',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=ROOT/'phase3/validation/expanded_v2.json')
    args=parser.parse_args()
    print(json.dumps({'all_pass':validate(args.reviewed_sources,args.output)}))
