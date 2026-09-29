"""Local, mandatory full-window sensitivity; preserves the primary interpretation."""
import difflib
import itertools
import json
from pathlib import Path
import platform

import axelrod as axl
from phase3.expanded_semantics import compile_candidate
from phase3.pilot_converter import ROOT, sha, encoded, exclusive, now
from phase3.runtime import seed_for

TARGETS = [('gemini_31_pro/default/Aggressive_12',998,'pro_aggressive_12.py.txt'),
           ('gemini_31_pro/default/Aggressive_14',996,'pro_aggressive_14.py.txt')]


def expected(n, suffix, end, full):
    if n+1>=end:
        return 'D'
    return 'D' if (not full or n>=2) and 'D' in suffix else 'C'


def action_at(cls,n,suffix):
    # Inspected functions are stateless and depend only on round and last two
    # opponent actions. Exercise every such state, without claiming enumeration
    # of every full history. Earlier own/opponent actions here are C.
    mine=[axl.Action.C]*n
    theirs=[axl.Action.C]*(n-len(suffix))+[axl.Action.C if a=='C' else axl.Action.D for a in suffix]
    player,opponent=cls(),axl.Cooperator()
    player.strategy(opponent)  # initialize adapter score counters
    player._history=axl.History(mine,theirs)
    opponent._history=axl.History(theirs,mine)
    return str(player.strategy(opponent))


def match_trace(cls,other,strategy_id):
    seed=seed_for(20260913,strategy_id,other.__name__)
    history=axl.Match((cls(),other()),turns=1000,game=axl.Game(r=3,s=0,t=5,p=1),noise=0,seed=seed).play()
    trace=[''.join(map(str,pair)) for pair in history]
    return {'seed':seed,'turns':len(trace),'trace':trace,'trace_sha256':sha(encoded(trace))}


def main():
    manifest_path=ROOT/'phase3/validation/western_derived_candidates_v1.json'
    manifest=json.loads(manifest_path.read_bytes())
    by_id={r['id']:r for r in manifest['candidates']}
    if len(by_id)!=274:
        raise ValueError('Expected 274 distinct primary candidates')
    for r in by_id.values():
        if sha((ROOT/r['selected_path']).read_bytes())!=r['selected_sha256']:
            raise ValueError('Primary source changed')
    opponents=[axl.Cooperator,axl.Defector,axl.Random,axl.TitForTat,axl.Grudger,axl.CyclerDDC,
               axl.CyclerCCD,axl.GoByMajority,axl.SuspiciousTitForTat,axl.Prober,axl.WinStayLoseShift]
    prepared=[]
    for strategy_id,end,filename in TARGETS:
        primary=ROOT/by_id[strategy_id]['selected_path']
        alternative=ROOT/'phase3/window_sensitivity_v1'/filename
        old=primary.read_bytes().decode(); new=alternative.read_bytes().decode()
        needle='len(opponent.history) >= 1 and opponent.history[-1]'
        if old.count(needle)!=1 or new.rstrip()!=old.replace(needle,'len(opponent.history) >= 2 and opponent.history[-1]').rstrip():
            raise ValueError('Alternative differs beyond reviewed minimum-window guard')
        prepared.append({'id':strategy_id,'end_round':end,'primary_path':str(primary.relative_to(ROOT)),
                         'primary_sha256':sha(old.encode()),'alternative_path':str(alternative.relative_to(ROOT)),
                         'alternative_sha256':sha(new.encode()),
                         'diff':''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=str(primary.relative_to(ROOT)),tofile=str(alternative.relative_to(ROOT))))})
    plan={'created_at':now(),'primary_manifest_sha256':sha(manifest_path.read_bytes()),
          'adjudication_sha256':sha((ROOT/'phase3/inputs/window_adjudication_v2.json').read_bytes()),
          'validator_sha256':sha(Path(__file__).read_bytes()),
          'adapter_sha256':sha((ROOT/'phase3/expanded_semantics.py').read_bytes()),
          'targets':prepared,'opponents':[o.__name__ for o in opponents],
          'protocol':'Compare all rounds 1..1000 and all available last-two-action suffixes. Paired diagnostic matches: 1000 rounds, noise 0, same seed and fresh opponent. Always retain/report both readings; no selection by outcome.',
          'future_confirmatory_analysis':'Run the same final tournament protocol with both alternatives substituted together, keeping all other candidates/settings fixed. Report primary and alternative effects regardless of sign/significance; final field and protocol remain pending.',
          'api_calls':0,'status':'local_sensitivity_plan_before_diagnostic_matches_not_public_registration'}
    plan_path=ROOT/'phase3/validation/window_sensitivity_plan_v1.json'
    exclusive(plan_path,encoded(plan))
    results=[]
    for entry in prepared:
        primary=compile_candidate((ROOT/entry['primary_path']).read_bytes().decode(),entry['primary_sha256'])
        alternative=compile_candidate((ROOT/entry['alternative_path']).read_bytes().decode(),entry['alternative_sha256'])
        failures=[]; differences=[]; checks=0
        for n in range(1000):
            for actions in itertools.product('CD',repeat=min(n,2)):
                suffix=''.join(actions)
                a=action_at(primary,n,suffix); b=action_at(alternative,n,suffix)
                ea=expected(n,suffix,entry['end_round'],False); eb=expected(n,suffix,entry['end_round'],True)
                checks+=2
                if a!=ea or b!=eb:
                    failures.append({'round':n+1,'suffix':suffix,'primary':a,'alternative':b,'expected_primary':ea,'expected_alternative':eb})
                if a!=b:
                    differences.append({'round':n+1,'opponent_suffix':suffix,'primary':a,'alternative':b})
        paired=[]
        for other in opponents:
            a=match_trace(primary,other,entry['id']); b=match_trace(alternative,other,entry['id'])
            different=[i+1 for i,(x,y) in enumerate(zip(a['trace'],b['trace'])) if x!=y]
            paired.append({'opponent':other.__name__,'seed':a['seed'],'primary_turns':a['turns'],
                           'alternative_turns':b['turns'],'primary_trace_sha256':a['trace_sha256'],
                           'alternative_trace_sha256':b['trace_sha256'],'differing_rounds':different,
                           'primary_trace':a['trace'],'alternative_trace':b['trace']})
        correct_diff=differences==[{'round':2,'opponent_suffix':'D','primary':'D','alternative':'C'}]
        passed=not failures and correct_diff and all(r['primary_turns']==r['alternative_turns']==1000 for r in paired)
        results.append({'id':entry['id'],'semantic_checks':checks,'failures':failures,
                        'same_history_differences':differences,'paired_matches':paired,'pass':passed})
        print(json.dumps({'id':entry['id'],'pass':passed,'semantic_checks':checks}),flush=True)
    report={'created_at':now(),'plan_sha256':sha(plan_path.read_bytes()),'python':platform.python_version(),
            'axelrod':axl.__version__,'results':results,'all_pass':all(r['pass'] for r in results),
            'scope':'Finite stateless decision-input coverage and classical diagnostic matches, not final tournament robustness.',
            'api_calls':0}
    report_path=ROOT/'phase3/validation/window_sensitivity_v1.json'
    exclusive(report_path,encoded(report))
    if report['all_pass']:
        replacement={e['id']:e for e in prepared}
        entries=[]
        for original in manifest['candidates']:
            record=dict(original)
            if record['id'] in replacement:
                e=replacement[record['id']]
                record.update({'primary_selected_path':record['selected_path'],'primary_selected_sha256':record['selected_sha256'],
                               'selected_path':e['alternative_path'],'selected_sha256':e['alternative_sha256'],
                               'derivation':'local_full_window_sensitivity_v1'})
            entries.append(record)
        exclusive(ROOT/'phase3/validation/western_full_window_candidates_v1.json',encoded({
            'primary_manifest_sha256':sha(manifest_path.read_bytes()),'sensitivity_report_sha256':sha(report_path.read_bytes()),
            'status':'alternative_only_not_replacement_for_primary_not_final_tournament_admission',
            'changed_candidates':2,'unchanged_candidates':272,'candidates':entries}))
    if sha(manifest_path.read_bytes())!=plan['primary_manifest_sha256']:
        raise ValueError('Primary manifest changed during validation')
    print(json.dumps({'all_pass':report['all_pass'],'api_calls':0}))


if __name__=='__main__':
    main()
