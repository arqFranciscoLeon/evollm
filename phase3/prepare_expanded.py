"""Offline preparation of the expanded contract; no network capability."""
import ast
from collections import Counter
import json
from pathlib import Path

from phase3.pilot_converter import SYSTEM, MODEL, ENDPOINT, encoded, sha
from phase3.review_semantics import ROOT, extract_comment, save_new_or_identical

ADDENDUM = '''
Phase 3 expanded interpretation contract v1 (explicit amendment):
The current round is len(self.history) + 1. Histories contain completed rounds only.
Rounds remaining includes the current, not-yet-played round: 1000 - len(self.history).
A fixed-length streak or a count/percentage within the last k rounds requires k completed rounds.
In contrast, "either of the previous two rounds" means any available observation
among the most recent two completed rounds: one observed D is sufficient in round 2.
A separately stated one-round or two-round lag condition requires that particular lag to exist.
Compare cumulative scores using completed rounds only, with the supplied game payoffs.
"More than" is strict >; "at least" includes equality; "majority" means more than half.
A switch "for the remainder of the game" is permanent once triggered, even if a later
percentage decreases or a streak ends. Do not make other conditions permanent.
Follow explicit operational rules and numeric thresholds over titles and explanatory summaries.
Respect explicit initial/final rules and priority. Do not add endgame defection,
forgiveness, randomization, or missing rules. Do not improve the strategy.
If the description still does not specify an unambiguous action, return exactly
UNCONVERTIBLE: followed by the missing condition, rather than inventing code.
'''


def prepare():
    inputs = ROOT/'phase3/inputs'
    old = json.loads((inputs/'semantic_review_v1.json').read_bytes())
    recent = json.loads((inputs/'semantic_review_remaining_v1.json').read_bytes())
    all_cases = old['cases']+recent['cases']
    assert len({c['id'] for c in all_cases}) == len(all_cases) == 300
    resolved = {f'gemini_31_pro/default/Aggressive_{n}' for n in (12,14)}
    assert {c['id'] for c in all_cases if c['status']=='needs_window_adjudication'} == resolved
    adjudication = {'schema':1, 'status':'local_methodological_decision_before_expanded_conversion',
                    'reviewer':'Codex assistant; explicit interpretation, not independent adjudication or public registration',
                    'decisions':[{'id':sid, 'previous_status':'needs_window_adjudication',
                                  'effective_status':'eligible_with_declared_interpretation',
                                  'interpretation':'Either of two prior rounds means any D among available last two observations.',
                                  'witness':{'round':2,'own':'C','opponent':'D','expected_action':'D'},
                                  'alternative_not_selected':'Requiring two completed rounds would give C at the same history.',
                                  'sensitivity':'Always report the prespecified full-window alternative separately, regardless of direction or significance; do not relabel this interpretation as recovered original intent.'}
                                 for sid in sorted(resolved)], 'api_calls':0}
    save_new_or_identical(inputs/'window_adjudication_v2.json',adjudication)
    prompt_path = ROOT/'src/evollm/prompts.py'
    tree = ast.parse(prompt_path.read_text(encoding='utf-8'))
    module = ast.parse('from __future__ import annotations')
    module.body += [n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('create_algorithm_prompt','create_game_information')]
    scope = {}
    exec(compile(module,'<historical-prompt-functions>','exec'),scope)
    class Classic:
        def RPST(self):
            return 3,1,0,5
    pilot = {r['id'] for r in old['cases'] if r['cohort']=='pilot'}
    requests, excluded = [], []
    for case in sorted(all_cases,key=lambda c:c['id']):
        if case['status']!='eligible_prose' and case['id'] not in resolved:
            excluded.append({'id':case['id'],'reason_status':case['status']})
            continue
        source = ROOT/case['snapshot_path']
        if sha(source.read_bytes()) != case['snapshot_sha256']:
            raise ValueError('Source changed')
        prose = extract_comment(source,case['id'].split('/')[-1])
        if sha(prose.encode()) != case['prose_sha256']:
            raise ValueError('Prose changed')
        prompt = scope['create_algorithm_prompt'](prose,Classic(),1000,0)
        payload = {'model':MODEL, 'messages':[{'role':'system','content':SYSTEM},
                                            {'role':'user','content':prompt+ADDENDUM}],
                   'temperature':0,'reasoning_effort':'none','max_completion_tokens':4096,
                   'n':1,'stream':False,'store':False,'service_tier':'default'}
        requests.append({'id':case['id'],'payload':payload,'payload_sha256':sha(encoded(payload)),
                         'prose_sha256':case['prose_sha256'],'snapshot_sha256':case['snapshot_sha256'],
                         'pilot_comparison_control':case['id'] in pilot,
                         'requires_declared_window_interpretation':case['id'] in resolved})
    assert len(requests)==274 and len(excluded)==26
    assert sum(r['pilot_comparison_control'] for r in requests)==12
    report = json.loads((ROOT/'phase3/validation/pilot_v1.json').read_bytes())
    estimated = report['summary']['estimated_token_cost_usd']*274/12
    artifact = {'schema':1,'status':'prepared_offline_not_sent', 'endpoint':ENDPOINT, 'model':MODEL,
                'requests':requests,'excluded':excluded,
                'by_model':dict(Counter(r['id'].split('/')[0] for r in requests)),
                'budget':{'proposed_ceiling_usd':2.00,'reported_balance_usd':2.93,
                          'balance_source':'User screenshot, not freshly queried; no guarantee of current account balance.',
                          'pilot_extrapolation_usd':round(estimated,6),
                          'extrapolation_limit':'12 short pilot descriptions; does not guarantee the cost of more complex cases.',
                          'max_attempts':274,'automatic_retries':0,
                          'reserve_per_inflight_usd':0.318432,
                          'accounting':'Reserve worst-case request cost before send; replace with validated reported token cost after success. Keep full reserve and stop on unknown cost or network outcome.',
                          'stop_condition':'Stop before sending if spent plus unresolved reserves plus next full reserve exceeds USD 2.00.',
                          'completion_not_guaranteed':'Ceiling can stop the wave early; no automatic top-up or increased limit.',
                          'pricing_source':'https://developers.openai.com/api/docs/models/gpt-5.4-mini',
                          'pricing_verified_date':'2026-09-13','input_usd_per_million':0.75,
                          'cached_input_usd_per_million':0.075,'output_usd_per_million':4.50},
                'live_executor_status':'not_implemented_for_this_plan; the old 12-case executor must reject it',
                'validation_required':['Exact provenance and syntax; no code repair.',
                                       'State/score semantics and expanded boundary cases before full horizon validation.',
                                       'Diagnostic classic opponents; no tournament results used for inclusion.',
                                       'Twelve paired pilot controls; keep old and new results, no picking the better-performing implementation.',
                                       'Short-history window sensitivity specified for both adjudicated cases.'],
                'sources':{str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in
                           (inputs/'semantic_review_v1.json',inputs/'semantic_review_remaining_v1.json',
                            inputs/'semantic_encoding_corrections_v1.json',inputs/'window_adjudication_v2.json',
                            ROOT/'phase3/validation/pilot_v1.json',prompt_path,Path(__file__))},
                'api_calls':0}
    save_new_or_identical(inputs/'expanded_requests_v2.json',artifact)
    print(json.dumps({'requests':len(requests),'exclusions':len(excluded),'by_model':artifact['by_model'],
                      'pilot_controls':12,'estimated_usd':round(estimated,6),'ceiling_usd':2.00,'api_calls':0}))


if __name__=='__main__':
    prepare()
