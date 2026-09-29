"""Freeze 572 exact common-contract requests offline; does not send requests."""
import ast
from collections import Counter
import json
from pathlib import Path
import random
from phase3.expanded_converter import load_plan
from phase3.prepare_expanded import ADDENDUM
from phase3.pilot_converter import ROOT, SYSTEM, ENDPOINT, sha, encoded, exclusive
from phase3.review_semantics import extract_comment

MODEL='gpt-5.4-mini-2026-03-17'
V3_ADDITION='''
Uniform interpretation contract v3 (applied identically to every description):
When "immediately after you play Cooperate" does not explicitly name a later
round, interpret the trigger as your C and the opponent's D in the same most
recent completed round. This is an operational convention, not a causal claim.
When "this is the tenth consecutive round of mutual cooperation" is used as a
decision predicate, require a full moving window of ten completed CC rounds;
do not count the current unplayed round. This predicate is reevaluated each round.
These conventions do not override an explicitly specified different lag, window,
initial action, final action, or permanent state transition in the description.
'''

def prompt_builder():
    p=ROOT/'src/evollm/prompts.py'; tree=ast.parse(p.read_text(encoding='utf-8'))
    module=ast.parse('from __future__ import annotations')
    module.body += [n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('create_algorithm_prompt','create_game_information')]
    scope={}; exec(compile(module,'<frozen-prompt-builder>','exec'),scope)
    return scope['create_algorithm_prompt']

class Classic:
    def RPST(self): return 3,1,0,5

def main():
    western,_=load_plan()
    chinese_path=ROOT/'phase3/inputs/semantic_review_chinese_v1.json'
    chinese=json.loads(chinese_path.read_bytes())
    resolution_path=ROOT/'phase3/inputs/chinese_resolution_v1.json'
    resolution=json.loads(resolution_path.read_bytes())
    validation_path=ROOT/'phase3/validation/chinese_resolution_v1.json'
    if not json.loads(validation_path.read_bytes())['all_pass']: raise ValueError('Local resolution not validated')
    excluded_chinese={x['id'] for x in resolution['excluded']}
    archived=json.loads((ROOT/'phase3/inputs/manifest.json').read_bytes())
    libraries={lib['model']:lib for lib in archived['libraries'] if lib['prompt']=='default'}
    sources={}; requests=[]; builder=prompt_builder()
    entries=[(r['id'],r['prose_sha256'],'western') for r in western['requests']]
    entries += [(r['id'],r['prose_sha256'],'chinese') for r in chinese['cases'] if r['id'] not in excluded_chinese]
    for sid,prose_hash,cohort in sorted(entries):
        model,_,name=sid.split('/'); lib=libraries[model]; path=ROOT/lib['snapshot_path']
        if sha(path.read_bytes())!=lib['sha256']: raise ValueError('Archive changed')
        prose=extract_comment(path,name)
        if sha(prose.encode())!=prose_hash: raise ValueError('Prose changed')
        sources[lib['snapshot_path']]=lib['sha256']
        payload={'model':MODEL,'messages':[{'role':'system','content':SYSTEM},
                 {'role':'user','content':builder(prose,Classic(),1000,0)+ADDENDUM+V3_ADDITION}],
                 'temperature':0,'reasoning_effort':'none','max_completion_tokens':4096,
                 'n':1,'stream':False,'store':False,'service_tier':'default'}
        requests.append({'id':sid,'cohort':cohort,'payload':payload,'payload_sha256':sha(encoded(payload)),
                         'prose_sha256':prose_hash,'snapshot_sha256':lib['sha256'],
                         'prior_western_conversion_control':cohort=='western'})
    random.Random(20260914).shuffle(requests)
    if len(requests)!=572 or len({r['id'] for r in requests})!=572: raise ValueError('Wrong coverage')
    dependencies=[chinese_path,resolution_path,validation_path,ROOT/'phase3/CHINESE_RESOLUTION_POLICY_v1.md',
        ROOT/'phase3/inputs/expanded_requests_v2.json',ROOT/'phase3/prepare_expanded.py',
        ROOT/'src/evollm/prompts.py',ROOT/'phase3/pilot_converter.py',Path(__file__)]
    sources.update({str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in dependencies})
    artifact={'schema':1,'status':'prepared_offline_not_authorized_or_sent','endpoint':ENDPOINT,'model':MODEL,
      'required_returned_model':MODEL,'contract':'uniform_v3','contract_addendum':ADDENDUM+V3_ADDITION,
      'order':'Sorted IDs shuffled with Python random.Random(20260914), fixed before conversion; groups not sent as labels.',
      'requests':requests,'excluded':western['excluded']+resolution['excluded'],
      'by_model':dict(Counter(r['id'].split('/')[0] for r in requests)),
      'by_cohort':dict(Counter(r['cohort'] for r in requests)),
      'budget':{'ceiling_usd':2.0,'max_attempts':572,'reserve_per_attempt_usd':0.318432,
                'automatic_retries':0,'prior_wave_linear_extrapolation_usd':0.251247*572/274,
                'estimate_limit':'Prior short western outputs, excludes additional prompt length; not a quote or guarantee.',
                'pricing_verified_date':'2026-09-14','pricing_source':'https://developers.openai.com/api/docs/models/gpt-5.4-mini',
                'input_per_million':0.75,'cached_input_per_million':0.075,'output_per_million':4.5,
                'unknown_cost':'Keep full reserve and stop; no repeat or automatic top-up.'},
      'validation_required':['Inspect every received source before execution.',
        'Use the same runtime, definitions and original-error/correction policy across cohorts.',
        'Validate all new candidates against declared prose profiles, retaining originals and failures.',
        'Compare all 274 prior western outputs as paired controls, without choosing by payoffs.',
        'Preserve all four mandatory alternative interpretations for later tournament sensitivity.'],
      'sources':sources,'api_calls':0}
    path=ROOT/'phase3/inputs/uniform_requests_v3.json'; exclusive(path,encoded(artifact))
    print(json.dumps({'requests':len(requests),'excluded':len(artifact['excluded']),'sha256':sha(path.read_bytes()),'by_cohort':artifact['by_cohort'],'ceiling_usd':2,'api_calls':0}))

if __name__=='__main__': main()
