"""Validate reviewed pilot candidates, without API calls or code repairs.

The strict subset below matches the 12 manually inspected, stateless functions.
Other generated code requires a new review, not a silent broadening of execution.
"""
import argparse
import ast
from collections import Counter
import importlib.metadata
import json
from pathlib import Path
import platform

import axelrod as axl
from phase3.pilot_converter import ROOT, assess, encoded, exclusive, sha
from phase3.runtime import seed_for

ALLOWED = (ast.Module, ast.FunctionDef, ast.arguments, ast.arg, ast.Return, ast.If,
           ast.Assign, ast.Name, ast.Load, ast.Store, ast.Attribute, ast.Call,
           ast.Constant, ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt,
           ast.GtE, ast.In, ast.NotIn, ast.BoolOp, ast.And, ast.Or, ast.UnaryOp,
           ast.USub, ast.Not, ast.BinOp, ast.Add, ast.Sub, ast.Subscript, ast.Slice,
           ast.List)
ATTRIBUTES = {'self.history', 'opponent.history', 'self.first_round', 'axl.Action',
              'axl.Action.C', 'axl.Action.D', 'axl.player', 'axl.player.Player'}


def compile_reviewed(source):
    tree = ast.parse(source)
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
        raise ValueError('Expected only one strategy function')
    fn = tree.body[0]
    if (fn.name != 'strategy' or [a.arg for a in fn.args.args] != ['self', 'opponent']
            or fn.decorator_list or fn.args.defaults or fn.args.kwonlyargs or fn.args.posonlyargs
            or fn.args.kwarg or fn.args.vararg):
        raise ValueError('Unexpected signature')
    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED):
            raise ValueError('Code outside reviewed subset: '+type(node).__name__)
        if isinstance(node, ast.FunctionDef) and node is not fn:
            raise ValueError('Nested function not reviewed')
        if isinstance(node, ast.Attribute) and ast.unparse(node) not in ATTRIBUTES:
            raise ValueError('Attribute outside reviewed subset')
        if isinstance(node, ast.Call):
            target = ast.unparse(node.func)
            if target not in ('len', 'self.first_round') or node.keywords:
                raise ValueError('Call outside reviewed subset')
        if isinstance(node, ast.Assign):
            if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
                raise ValueError('Only local variable assignments allowed')
            if node.targets[0].id in ('self', 'opponent', 'axl', 'len'):
                raise ValueError('Cannot replace runtime names')
        if isinstance(node, ast.Constant) and (type(node.value) is not int or abs(node.value) > 1000):
            raise ValueError('Unexpected constant')
    namespace = {'axl': axl, '__builtins__': {'len': len}}
    exec(compile(tree, '<reviewed-pilot-function>', 'exec'), namespace)
    raw = namespace['strategy']

    class PilotPlayer(axl.Player):
        name = 'Reviewed pilot candidate'
        classifier = {'memory_depth': float('inf'), 'stochastic': False,
                      'long_run_time': False, 'inspects_source': False, 'manipulates_source': False,
                      'manipulates_state': False}

        def first_round(self):
            return len(self.history) == 0

        def strategy(self, opponent):
            if len(self.history) != len(opponent.history):
                raise ValueError('Mismatched histories')
            action = raw(self, opponent)
            if action not in (axl.Action.C, axl.Action.D):
                raise ValueError('Invalid action; no substitution')
            return action
    return PilotPlayer


def decode(blocks):
    return [axl.Action.C if a == 'C' else axl.Action.D for a, count in blocks for _ in range(count)]


def check_vector(cls, case):
    mine, theirs = decode(case['own_rle']), decode(case['opponent_rle'])
    if len(mine) != len(theirs) or len(mine)+1 != case['round']:
        raise ValueError('Invalid test history')
    first, second = cls(), axl.Cooperator()
    # These inspected functions have no persistent state beyond histories.
    for a, b in zip(mine, theirs):
        first.update_history(a, b)
        second.update_history(b, a)
    actual = str(first.strategy(second))
    return {'case': case['case'], 'round': case['round'], 'expected': case['expected_action'],
            'actual': actual, 'pass': actual == case['expected_action']}


def validate(run_dir, output):
    plan_bytes = (run_dir/'plan.json').read_bytes()
    if plan_bytes != (ROOT/'phase3/inputs/pilot_requests_v1.json').read_bytes():
        raise ValueError('Run plan differs from prepared plan')
    plan = json.loads(plan_bytes)
    for relative, digest in plan['sources'].items():
        if sha((ROOT/relative).read_bytes()) != digest:
            raise ValueError('Prepared source changed: '+relative)
    vectors_path = ROOT/'phase3/inputs/semantic_test_vectors_v1.json'
    vectors = json.loads(vectors_path.read_bytes())['cases']
    opponents = [axl.Cooperator, axl.Defector, axl.Random, axl.TitForTat, axl.Grudger,
                 axl.CyclerDDC, axl.CyclerCCD, axl.GoByMajority, axl.SuspiciousTitForTat,
                 axl.Prober, axl.WinStayLoseShift]
    records, total_usage = [], Counter()
    for number, item in enumerate(plan['requests'], 1):
        folder = run_dir/f'{number:02d}'
        result = json.loads((folder/'result.json').read_bytes())
        request = json.loads((folder/'request.json').read_bytes())
        body = (folder/'response.bin').read_bytes()
        source_bytes = (folder/'candidate.py.txt').read_bytes()
        response = json.loads(body)
        if (sha(body) != result['response_sha256'] or assess(body) != 'candidate_pending_fidelity_and_runtime'
                or result['status'] != 'candidate_pending_fidelity_and_runtime'
                or result['http_status'] != 200 or request['strategy_id'] != item['strategy_id']
                or encoded(request['payload']) != encoded(item['payload'])
                or source_bytes != response['choices'][0]['message']['content'].encode()):
            raise ValueError('Candidate provenance mismatch')
        cls = compile_reviewed(source_bytes.decode())
        cases = [c for c in vectors if c['strategy_id'] == item['strategy_id']]
        semantic = [check_vector(cls, c) for c in cases]
        matches = []
        for opponent in opponents:
            seed = seed_for(20260913, item['strategy_id'], opponent.__name__)
            try:
                match = axl.Match((cls(), opponent()), turns=1000, game=axl.Game(r=3,s=0,t=5,p=1),
                                  noise=0, seed=seed)
                history = match.play()
                if len(history) != 1000:
                    raise ValueError('Incomplete match')
                matches.append({'opponent': opponent.__name__, 'seed': seed, 'turns': len(history), 'pass': True})
            except Exception as error:
                matches.append({'opponent': opponent.__name__, 'seed': seed, 'pass': False,
                                'error': type(error).__name__+': '+str(error)})
        usage = response['usage']
        cached = usage.get('prompt_tokens_details', {}).get('cached_tokens', 0)
        total_usage.update({'input_tokens': usage['prompt_tokens'], 'output_tokens': usage['completion_tokens'],
                            'cached_input_tokens': cached})
        records.append({'strategy_id': item['strategy_id'], 'candidate_sha256': sha(source_bytes),
                        'response_sha256': sha(body), 'prose_sha256': item['prose_sha256'],
                        'served_model': response['model'], 'finish_reason': response['choices'][0]['finish_reason'],
                        'usage': usage, 'request_started_at': request['started_at'],
                        'response_finished_at': result['finished_at'],
                        'semantic_cases': semantic, 'runtime_matches': matches,
                        'manual_review': 'Stateless branches inspected against prose before execution; no repair applied.'})
    summary = {'candidates': len(records), 'semantic_checks': sum(len(r['semantic_cases']) for r in records),
               'semantic_passed': sum(c['pass'] for r in records for c in r['semantic_cases']),
               'runtime_matches': sum(len(r['runtime_matches']) for r in records),
               'runtime_passed': sum(c['pass'] for r in records for c in r['runtime_matches']),
               **total_usage}
    assert summary['candidates'] == 12 and summary['semantic_checks'] == 70 and summary['runtime_matches'] == 132
    cost = ((total_usage['input_tokens']-total_usage['cached_input_tokens'])*0.75
            + total_usage['cached_input_tokens']*0.075 + total_usage['output_tokens']*4.50)/1e6
    summary['estimated_token_cost_usd'] = round(cost, 9)
    report = {'purpose': 'Pilot conversion fidelity/runtime diagnostics, not the confirmatory tournament',
              'plan_sha256': sha(plan_bytes), 'validator_sha256': sha(Path(__file__).read_bytes()),
              'vector_sha256': sha(vectors_path.read_bytes()), 'python': platform.python_version(),
              'axelrod': importlib.metadata.version('axelrod'), 'summary': summary, 'candidates': records,
              'limitations': ['One assistant semantic review; not independent human adjudication.',
                              '70 targeted cases and 11 opponents per candidate do not prove exhaustive equivalence.',
                              'Fresh local Axelrod adapter provides first_round and action guard; stateless candidate functions are unchanged.',
                              'Cost calculated from reported tokens and documented rates; not an invoice or account statement.',
                              'The other descriptions and the mixed tournament remain unvalidated.'],
              'all_pass': summary['semantic_passed']==70 and summary['runtime_passed']==132}
    output.parent.mkdir(parents=True, exist_ok=True)
    data = encoded(report)
    if output.exists():
        if output.read_bytes() != data:
            raise ValueError('Report exists with different evidence; version explicitly')
    else:
        exclusive(output, data)
    print(json.dumps({'all_pass': report['all_pass'], **summary}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', type=Path, default=ROOT/'phase3/conversion_runs/pilot_v1')
    parser.add_argument('--output', type=Path, default=ROOT/'phase3/validation/pilot_v1.json')
    args = parser.parse_args()
    validate(args.run_dir, args.output)
