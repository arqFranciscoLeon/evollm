"""Offline one-time preparation and targeted validation, never a tournament."""
import json
from pathlib import Path
from collections import Counter
import axelrod as axl
from phase3.execute_uniform import load_field, digest, MANIFEST_SHA256
from phase3.runtime import ROOT, seed_for, play_pair
from phase3.uniform_semantics_v3b import compile_candidate
from phase3.validate_uniform_v3b import replay
from phase3.validate_chinese_resolution import AdjudicatedReference
from phase3.sensitivity_analysis_v1 import ast_group


class WindowReference:
    def __init__(self, end): self.end = end
    def step(self, mine, opp):
        if len(opp)+1 >= self.end: return 'D'
        return 'D' if len(opp)>=2 and 'D' in opp[-2:] else 'C'


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as out:
        out.write(value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
    field=load_field()
    alternatives=[]
    definitions=[
        ('gemini_31_pro/default/Aggressive_12','phase3/window_sensitivity_v1/pro_aggressive_12.py.txt',998),
        ('gemini_31_pro/default/Aggressive_14','phase3/window_sensitivity_v1/pro_aggressive_14.py.txt',996),
        ('kimi_k25/default/Aggressive_25','phase3/chinese_resolution_v1/kimi_k25_Aggressive_25_alternative.py.txt',None),
        ('glm_51/default/Aggressive_20','phase3/chinese_resolution_v1/glm_51_Aggressive_20_alternative.py.txt',None)]
    audit=json.loads((ROOT/'phase3/validation/chinese_audit_v1.json').read_bytes())
    scenarios=[(s['own'],s['opponent']) for s in audit['scenarios']]
    scenarios += [('C','D'),('CD','CD'),('CC','CD'),('CCC','DCC'),('C'*9,'C'*9),('C'*10,'C'*10),
                  ('D'*3+'C'+'D'+'C'*5,'CCC'+'D'+'C'*6)]
    opponents=[axl.Cooperator,axl.Defector,axl.Random,axl.TitForTat,axl.Grudger,axl.CyclerDDC,
               axl.CyclerCCD,axl.GoByMajority,axl.SuspiciousTitForTat,axl.Prober,axl.WinStayLoseShift]
    validations=[]
    for sid, path, end in definitions:
        original=(ROOT/path).read_bytes(); source=original.decode(); selected=path
        change='none; existing inspected alternative'
        if sid.startswith('kimi'):
            source=source.replace('_defect_forever','sensitivity_defect_forever')
            selected='phase3/interpretation_sources_v1/kimi_aggressive_25.py.txt'
            save(ROOT/selected,source)
            change='Only rename candidate-owned state _defect_forever to sensitivity_defect_forever for frozen adapter compatibility.'
        source_bytes=(ROOT/selected).read_bytes()
        item={'id':sid,'source_path':selected,'source_sha256':digest(source_bytes),
              'historical_source_path':path,'historical_source_sha256':digest(original),'change':change,
              'reviewer':'Codex source inspection; no independent adjudicator or model regeneration'}
        cls=compile_candidate(source_bytes.decode(),item['source_sha256'])
        factory=(lambda e=end:WindowReference(e)) if end else (lambda s=sid:AdjudicatedReference(s,True))
        checks=[replay(cls,factory,a,b) for a,b in scenarios]
        checks += [replay(cls,factory,'',b,True) for b in audit['on_policy_opponents']]
        if any(c.get('error') or c['failures'] for c in checks):
            raise ValueError('Alternative failed reference checks: '+sid)
        matches=[]
        for opponent in opponents:
            result=play_pair(cls,opponent,1000,seed_for(20260913,sid,opponent.__name__))
            matches.append({'opponent':opponent.__name__,'turns':sum(result[k] for k in ('CC','CD','DC','DD'))})
        validations.append({'id':sid,'checks':sum(c['checks'] for c in checks),'traces':checks,'matches':matches,'passed':True})
        alternatives.append(item)
        print(json.dumps({'id':sid,'checks':validations[-1]['checks'],'matches':len(matches),'passed':True}),flush=True)
    sources={sid:ast_group((ROOT/row['source_path']).read_text(encoding='utf-8')) for sid,row in field.records.items()}
    cells={}
    for sid,group in sources.items():
        key=sid.split('/')[0]+'/'+sid.split('/')[-1].split('_')[0]
        cells.setdefault(key,[]).append(group)
    dependencies=['phase3/execute_uniform.py','phase3/uniform_semantics_v3b.py','phase3/runtime.py',
                  'phase3/sensitivity_analysis_v1.py','phase3/interpretation_sensitivity_v1.py',
                  'phase3/prepare_sensitivities_v1.py','phase3/validate_uniform_v3b.py',
                  'phase3/validate_chinese_resolution.py','phase3/validation/chinese_audit_v1.json']
    plan={'status':'local_prespecification_not_public_registration','primary_manifest_sha256':MANIFEST_SHA256,
          'dependencies':{p:digest((ROOT/p).read_bytes()) for p in dependencies},
          'alternatives':alternatives,'scenario_masks':list(range(16)),
          'mask_rule':'Bit order is alternatives order. 0 primary; 3 both Pro windows; 15 all alternatives. Report all 16 without selecting by outcomes.',
          'execution':'Separate full schedules and databases using frozen execute_uniform.run/export_matrices; identical identities, settings, seeds. No partial-matrix reuse implemented.',
          'syntax_groups':sources,'unique_ast':len(set(sources.values())),
          'groups_per_cell':{k:len(set(v)) for k,v in sorted(cells.items())},
          'duplicate_rule':'Weight each identity by inverse AST multiplicity within its model/attitude cell; product weights, excluding identical identities, then normalize each cell pair.',
          'exclusion_rule':'Bounds for original 25 identities per model/attitude, missing CC edges independently allowed [0,1]. No strategy imputation.',
          'api_calls':0,'confirmatory_matches':0}
    save(ROOT/'phase3/inputs/sensitivity_plan_v1.json',plan)
    save(ROOT/'phase3/validation/interpretation_sensitivity_v1.json',
         {'plan_sha256':digest((ROOT/'phase3/inputs/sensitivity_plan_v1.json').read_bytes()),
          'results':validations,'all_pass':True,'api_calls':0,'confirmatory_matches':0})


if __name__=='__main__': main()
