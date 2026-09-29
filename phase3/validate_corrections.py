"""Validate two explicitly reviewed local corrections; never modify API originals."""
import difflib
import json
from pathlib import Path

import axelrod as axl
from phase3.expanded_converter import PLAN_SHA256, RUN_DIR, load_plan, ledger
from phase3.expanded_semantics import compile_candidate, replay
from phase3.pilot_converter import ROOT, sha, encoded, exclusive, now
from phase3.runtime import seed_for
from phase3.validate_expanded import SCENARIOS, profiles

CORRECTIONS = {
    53: ('sonnet_neutral_11.py.txt', '21dcca67e5e0f5d6a467110754f049b7f73dbe4159358c14cd858cff8d5d7b2f',
         'Move last-defection branch below permanent >55% trigger, following explicit prose priority.'),
    156: ('pro_aggressive_6.py.txt', '8c334dee464c4ed2d565e30e5741af383b44f8f00d0e975e34aa5fd51718281d',
          'Use current round len(history)+1 for explicit round 995 inclusive.'),
}


def main():
    plan,_=load_plan()
    assert ledger(RUN_DIR,plan)['completed']==274
    original_path=ROOT/'phase3/validation/expanded_v2.json'
    original=json.loads(original_path.read_bytes())
    assert original['plan_sha256']==PLAN_SHA256
    original_results={r['id']:r for r in original['results']}
    assert {r['id'] for r in original['results'] if not r['pass']} == {plan['requests'][i-1]['id'] for i in CORRECTIONS}
    opponents=[axl.Cooperator,axl.Defector,axl.Random,axl.TitForTat,axl.Grudger,axl.CyclerDDC,
               axl.CyclerCCD,axl.GoByMajority,axl.SuspiciousTitForTat,axl.Prober,axl.WinStayLoseShift]
    mapping=profiles(); results=[]; entries=[]
    for i,item in enumerate(plan['requests'],1):
        source_path=RUN_DIR/f'{i:03d}'/'candidate.py.txt'
        original_hash=sha(source_path.read_bytes())
        assert original_hash==original_results[item['id']]['candidate_sha256']
        entry={'id':item['id'],'original_path':str(source_path.relative_to(ROOT)),
               'original_sha256':original_hash,'derivation':'original_API_response'}
        if i in CORRECTIONS:
            filename,expected,reason=CORRECTIONS[i]
            assert original_hash==expected
            corrected_path=ROOT/'phase3/corrections_v1'/filename
            old=source_path.read_bytes().decode(); new=corrected_path.read_bytes().decode()
            # Enforce the exact minimal reviewed transformation, apart from final newline.
            if i==53:
                branch='    if opponent.history[-1] == axl.Action.D:\n        return axl.Action.D\n\n'
                assert old.count(branch)==1
                expected_source=old.replace(branch,'')
                position=expected_source.rfind('    return axl.Action.C')
                expected_source=expected_source[:position]+branch+expected_source[position:]
            else:
                assert old.count('len(self.history) >= 995')==1
                expected_source=old.replace('len(self.history) >= 995','len(self.history) + 1 >= 995')
            assert new.rstrip('\r\n')==expected_source.rstrip('\r\n')
            cls=compile_candidate(new,sha(new.encode()))  # Static sources inspected before this run.
            semantic=[{'scenario':j,**replay(cls,a,b,mapping[item['id']])} for j,(a,b) in enumerate(SCENARIOS)]
            runtime=[]
            for opponent in opponents:
                seed=seed_for(20260913,item['id'],opponent.__name__)
                history=axl.Match((cls(),opponent()),turns=1000,game=axl.Game(r=3,s=0,t=5,p=1),noise=0,seed=seed).play()
                runtime.append({'opponent':opponent.__name__,'seed':seed,'turns':len(history),'pass':len(history)==1000})
            passed=not any(s['failures'] for s in semantic) and all(r['pass'] for r in runtime)
            results.append({'id':item['id'],'original_sha256':original_hash,'corrected_sha256':sha(new.encode()),
                            'reason':reason,'diff':''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),
                            fromfile=str(source_path.relative_to(ROOT)),tofile=str(corrected_path.relative_to(ROOT)))),
                            'semantic':semantic,'runtime':runtime,'pass':passed})
            entry.update({'derivation':'local_prose_grounded_correction_v1','reason':reason})
            source_path=corrected_path
        entry.update({'selected_path':str(source_path.relative_to(ROOT)),'selected_sha256':sha(source_path.read_bytes())})
        entries.append(entry)
    passed=all(r['pass'] for r in results)
    report={'created_at':now(),'plan_sha256':PLAN_SHA256,'original_validation_sha256':sha(original_path.read_bytes()),
            'policy_sha256':sha((ROOT/'phase3/IMPLEMENTATION_CORRECTIONS_v1.md').read_bytes()),
            'validator_sha256':sha(Path(__file__).read_bytes()),
            'semantics_sha256':sha((ROOT/'phase3/expanded_semantics.py').read_bytes()),
            'corrections':results,'all_pass':passed,'api_calls':0,
            'scope':'Repeat affected semantic and runtime checks only; not exhaustive equivalence or tournament results.'}
    exclusive(ROOT/'phase3/validation/expanded_corrections_v1.json',encoded(report))
    if passed:
        exclusive(ROOT/'phase3/validation/western_derived_candidates_v1.json',encoded({
            'created_at':now(),'plan_sha256':PLAN_SHA256,'original_validation_sha256':sha(original_path.read_bytes()),
            'correction_validation_sha256':sha(encoded(report)),
            'status':'passed_targeted_checks_not_final_tournament_admission',
            'unchanged_originals':272,'local_corrections':2,'candidates':entries}))
    print(json.dumps({'all_pass':passed,'corrected_candidates':len(results),'api_calls':0}))


if __name__=='__main__':
    main()
