"""Materialize complete batch schedule without executing real tournament games."""
import json
from phase3.execute_uniform import load_field, digest
from phase3.interpretation_sensitivity_v1 import load_scenario, PLAN
from phase3.runtime import ROOT
from phase3.reuse_batches_v1 import make_context, batches, encoded, sha

DEST=ROOT/'phase3/reuse_plan_v1'


def main():
    if DEST.exists(): raise ValueError('Plan already exists; use a new version')
    primary=load_field(); scenarios={}
    for mask in range(16):
        field=load_scenario(mask,primary)
        scenarios[mask]={sid:row['source_sha256'] for sid,row in sorted(field.records.items())}
    provenance={'field':primary.provenance,'sensitivity_plan_sha256':digest(PLAN.read_bytes()),
                'target_system':'Linux','reference_remote_pilot_sha256':digest((ROOT/'phase3/validation/modal_pilot_remote_v1.json').read_bytes()),
                'reuse_worker_sha256':digest((ROOT/'phase3/reuse_worker_v1.py').read_bytes())}
    context=make_context(scenarios,provenance=provenance,scope='full_round_robin')
    DEST.mkdir(); (DEST/'context.json').write_text(encoded(context),encoding='utf-8')
    summary={'status':'prepared_not_executed_not_publicly_registered','context_sha256':sha(context),
             'batch_size':250,'batches':[],'unique_matches':0,'logical_matches':0,'scenario_counts':{str(i):0 for i in range(16)}}
    for batch in batches(context,250):
        name=f'batch_{batch["index"]:04d}.json'; raw=encoded(batch).encode()
        (DEST/name).write_bytes(raw)
        summary['batches'].append({'path':name,'batch_sha256':batch['batch_sha256'],'file_sha256':digest(raw),'matches':len(batch['jobs'])})
        summary['unique_matches']+=len(batch['jobs'])
        for job in batch['jobs']:
            summary['logical_matches']+=len(job['scenarios'])
            for mask in job['scenarios']: summary['scenario_counts'][str(mask)]+=1
    assert summary['unique_matches']==166172 and summary['logical_matches']==2622048
    assert set(summary['scenario_counts'].values())=={163878}
    summary.update(main_manifest_sha256=primary.provenance['manifest_sha256'],api_calls=0,confirmatory_matches_executed=0)
    (DEST/'manifest.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps({'unique_matches':summary['unique_matches'],'logical_matches':summary['logical_matches'],'batches':len(summary['batches'])}))


if __name__=='__main__': main()
