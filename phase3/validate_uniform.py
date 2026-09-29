"""Symmetric offline validation of the inspected uniform v3 responses.

Original responses are never repaired or replaced by this validator.
"""
import json
import platform
from collections import Counter
from pathlib import Path
import axelrod as axl
from phase3.pilot_converter import ROOT, sha, encoded, exclusive, now
from phase3.uniform_converter import load_plan, ledger, RUN_DIR, PLAN_SHA256
from phase3.uniform_semantics import compile_candidate
from phase3.expanded_semantics import reference
from phase3.validate_expanded import profiles
from phase3.chinese_semantics import Reference
from phase3.validate_chinese_resolution import AdjudicatedReference
from phase3.runtime import seed_for


class WesternReference:
    def __init__(self, profile):
        self.profile = profile

    def step(self, mine, opp):
        return reference(self.profile, mine, opp)


def replay(cls, factory, mine, opp, on_policy=False):
    a, b = cls(), axl.Cooperator()
    oracle = factory()
    own = ''
    actions = []
    failures = []
    for n in range(len(opp) + 1):
        prior = own if on_policy else mine[:n]
        expected = oracle.step(prior, opp[:n])
        try:
            actual = str(a.strategy(b))
        except Exception as exc:
            return {'checks': len(actions), 'failures': failures, 'error': repr(exc),
                    'error_round': n + 1, 'actions_sha256': sha(''.join(actions).encode())}
        actions.append(actual)
        if actual != expected and not failures:
            failures.append({'round': n + 1, 'own': prior, 'opponent': opp[:n],
                             'expected': expected, 'actual': actual,
                             'reachable_candidate_history': on_policy})
        if n < len(opp):
            x, y = actual if on_policy else mine[n], opp[n]
            aa = axl.Action.C if x == 'C' else axl.Action.D
            bb = axl.Action.C if y == 'C' else axl.Action.D
            a.update_history(aa, bb)
            b.update_history(bb, aa)
            own += x
    return {'checks': len(actions), 'failures': failures,
            'actions_sha256': sha(''.join(actions).encode())}


def main():
    plan, _ = load_plan()
    state = ledger(RUN_DIR, plan)
    if state['blocked'] or state['completed'] != 572:
        raise ValueError('Complete traceable 572-response run required')
    review_path = ROOT / 'phase3/validation/uniform_source_review_v3.json'
    review = json.loads(review_path.read_bytes())
    approved = {r['id']: r for r in review['reviewed_candidates']}
    if (review['plan_sha256'] != PLAN_SHA256 or len(approved) != 572
            or len(review['reviewed_candidates']) != 572
            or set(approved) != {r['id'] for r in plan['requests']}):
        raise ValueError('Exact source review coverage required')
    west = profiles()
    chinese = {c['id']: c['profile'] for c in json.loads(
        (ROOT / 'phase3/inputs/semantic_review_chinese_v1.json').read_bytes())['cases']}
    audit_path = ROOT / 'phase3/validation/chinese_audit_v1.json'
    audit = json.loads(audit_path.read_bytes())
    scenarios = [(s['own'], s['opponent']) for s in audit['scenarios']]
    scenarios += [('C', 'D'), ('CD', 'CD'), ('CC', 'CD'), ('CCC', 'DCC'),
                  ('C' * 9, 'C' * 9), ('C' * 10, 'C' * 10),
                  ('D' * 3 + 'C' + 'D' + 'C' * 5, 'CCC' + 'D' + 'C' * 6)]
    scripts = audit['on_policy_opponents']
    old_plan = json.loads((ROOT / 'phase3/inputs/expanded_requests_v2.json').read_bytes())
    old_report_path = ROOT / 'phase3/validation/expanded_v2.json'
    old_report = json.loads(old_report_path.read_bytes())
    if old_report['plan_sha256'] != sha((ROOT / 'phase3/inputs/expanded_requests_v2.json').read_bytes()):
        raise ValueError('Previous control plan changed')
    old_paths = {r['id']: ROOT / f'phase3/conversion_runs/expanded_v2/{i:03d}/candidate.py.txt'
                 for i, r in enumerate(old_plan['requests'], 1)}
    old_hashes = {r['id']: r['candidate_sha256'] for r in old_report['results']}
    opponents = [axl.Cooperator, axl.Defector, axl.Random, axl.TitForTat, axl.Grudger,
                 axl.CyclerDDC, axl.CyclerCCD, axl.GoByMajority,
                 axl.SuspiciousTitForTat, axl.Prober, axl.WinStayLoseShift]
    results = []
    checkpoint_dir = ROOT / 'phase3/validation/uniform_v3_entries'
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    run_identity = {
        'plan': PLAN_SHA256, 'review': sha(review_path.read_bytes()),
        'validator': sha(Path(__file__).read_bytes()),
        'adapter': sha((ROOT / 'phase3/uniform_semantics.py').read_bytes()),
        'references': {p: sha((ROOT / 'phase3' / p).read_bytes()) for p in
                       ('expanded_semantics.py', 'chinese_semantics.py',
                        'validate_chinese_resolution.py', 'validate_expanded.py')},
        'audit': sha(audit_path.read_bytes()), 'old_report': sha(old_report_path.read_bytes())}
    for number, item in enumerate(plan['requests'], 1):
        sid = item['id']
        approval = approved[sid]
        if not approval.get('reviewer') or not approval.get('notes'):
            raise ValueError('Missing inspection attribution')
        source = (RUN_DIR / f'{number:03d}/candidate.py.txt').read_bytes().decode()
        checkpoint = checkpoint_dir / f'{number:03d}.json'
        if checkpoint.exists():
            saved = json.loads(checkpoint.read_bytes())
            if (saved['run_identity'] != run_identity or saved['id'] != sid
                    or saved['candidate_sha256'] != sha(source.encode())):
                raise ValueError('Checkpoint identity changed')
            results.append(saved)
            continue
        entry = {'id': sid, 'cohort': item['cohort'], 'candidate_sha256': sha(source.encode()),
                 'semantic': [], 'runtime': [], 'run_identity': run_identity}
        if sid in west:
            factory = lambda p=west[sid]: WesternReference(p)
        elif sid in ('kimi_k25/default/Aggressive_25', 'glm_51/default/Aggressive_20'):
            factory = lambda s=sid: AdjudicatedReference(s, False)
        else:
            factory = lambda p=chinese[sid]: Reference(p)
        try:
            cls = compile_candidate(source, approval['candidate_sha256'])
            for i, (a, b) in enumerate(scenarios):
                entry['semantic'].append({'scenario': i, 'mode': 'controlled', **replay(cls, factory, a, b)})
            for i, b in enumerate(scripts):
                entry['semantic'].append({'scenario': i, 'mode': 'candidate_on_policy', **replay(cls, factory, '', b, True)})
            if sid in west:
                old_cls = compile_candidate(old_paths[sid].read_bytes().decode(), old_hashes[sid])
                comparisons = []
                for i, (a, b) in enumerate(scenarios):
                    prior = replay(old_cls, factory, a, b)
                    comparisons.append(prior['actions_sha256'] == entry['semantic'][i]['actions_sha256'])
                entry['paired_raw_western_control'] = {'candidate_sha256': old_hashes[sid],
                    'same_controlled_scenarios': comparisons, 'all_same': all(comparisons)}
            for opponent in opponents:
                seed = seed_for(20260914, sid, opponent.__name__)
                try:
                    history = axl.Match((cls(), opponent()), turns=1000,
                        game=axl.Game(r=3, s=0, t=5, p=1), noise=0, seed=seed).play()
                    entry['runtime'].append({'opponent': opponent.__name__, 'seed': seed,
                                             'turns': len(history), 'pass': len(history) == 1000})
                except Exception as exc:
                    entry['runtime'].append({'opponent': opponent.__name__, 'seed': seed,
                                             'pass': False, 'error': repr(exc)})
            entry['status'] = ('runtime_error' if any('error' in r for r in entry['semantic']) or not all(r['pass'] for r in entry['runtime']) else
                'fidelity_discrepancy' if any(r['failures'] for r in entry['semantic']) else 'passed_targeted_checks')
        except Exception as exc:
            entry.update(status='validation_error', error=repr(exc))
        results.append(entry)
        # Durable individual checkpoints; an interruption never loses completed work.
        exclusive(checkpoint, encoded(entry))
        print(json.dumps({'validated': number, 'status': entry['status']}), flush=True)
    dependencies = ['uniform_semantics.py', 'expanded_semantics.py', 'chinese_semantics.py',
                    'validate_chinese_resolution.py', 'validate_expanded.py', 'runtime.py']
    report = {'created_at': now(), 'plan_sha256': PLAN_SHA256,
        'source_review_sha256': sha(review_path.read_bytes()), 'ledger': state,
        'validator_sha256': sha(Path(__file__).read_bytes()),
        'dependencies': {p: sha((ROOT / 'phase3' / p).read_bytes()) for p in dependencies},
        'scenario_source_sha256': sha(audit_path.read_bytes()),
        'prior_western_report_sha256': sha(old_report_path.read_bytes()),
        'scenarios': [{'own': a, 'opponent': b} for a, b in scenarios],
        'on_policy_opponents': scripts, 'python': platform.python_version(), 'axelrod': axl.__version__,
        'summary': dict(Counter(r['status'] for r in results)), 'results': results,
        'scope': 'Identical adapter and scenarios across both cohorts. Targeted checks, not exhaustive equivalence or tournament results. Raw failures preserved.',
        'api_calls': 0}
    exclusive(ROOT / 'phase3/validation/uniform_v3.json', encoded(report))
    print(json.dumps(report['summary']), flush=True)


if __name__ == '__main__':
    main()
