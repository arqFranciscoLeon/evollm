"""Validate inspected local derivatives with the frozen common v3b protocol."""
import json
from pathlib import Path
import axelrod as axl
from phase3.pilot_converter import ROOT, sha, encoded, exclusive, now
from phase3.uniform_converter import load_plan, ledger, RUN_DIR
from phase3.uniform_semantics_v3b import compile_candidate
from phase3.validate_uniform_v3b import replay, WesternReference
from phase3.validate_expanded import profiles
from phase3.chinese_semantics import Reference
from phase3.runtime import seed_for


def main():
    plan, _ = load_plan()
    state = ledger(RUN_DIR, plan)
    if state['completed'] != 572 or state['blocked']:
        raise ValueError('Raw run changed')
    raw_path = ROOT / 'phase3/validation/uniform_v3b.json'
    raw = json.loads(raw_path.read_bytes())
    registry_path = ROOT / 'phase3/inputs/uniform_corrections_v1.json'
    registry = json.loads(registry_path.read_bytes())
    if registry['raw_validation_sha256'] != sha(raw_path.read_bytes()):
        raise ValueError('Raw validation changed')
    if registry['policy_sha256'] != sha((ROOT / 'phase3/CHINESE_RESOLUTION_POLICY_v1.md').read_bytes()):
        raise ValueError('Correction policy changed')
    for relative, expected in raw['dependencies'].items():
        if sha((ROOT / 'phase3' / relative).read_bytes()) != expected:
            raise ValueError('Common protocol dependency changed: ' + relative)
    if raw['validator_sha256'] != sha((ROOT / 'phase3/validate_uniform_v3b.py').read_bytes()):
        raise ValueError('Common replay validator changed')
    review_path = ROOT / 'phase3/validation/uniform_corrections_source_review_v1.json'
    review = json.loads(review_path.read_bytes())
    if review['registry_sha256'] != sha(registry_path.read_bytes()):
        raise ValueError('Source inspection belongs to another registry')
    approved = {r['id']: r for r in review['sources']}
    originals = {r['id']: r for r in raw['results']}
    failed = {r['id'] for r in raw['results'] if r['status'] != 'passed_targeted_checks'}
    if set(approved) != failed or {r['id'] for r in registry['derivations']} != failed:
        raise ValueError('Correction and inspection coverage must equal raw failures')
    west = profiles()
    chinese = {c['id']: c['profile'] for c in json.loads(
        (ROOT / 'phase3/inputs/semantic_review_chinese_v1.json').read_bytes())['cases']}
    opponents = [axl.Cooperator, axl.Defector, axl.Random, axl.TitForTat, axl.Grudger,
                 axl.CyclerDDC, axl.CyclerCCD, axl.GoByMajority, axl.SuspiciousTitForTat,
                 axl.Prober, axl.WinStayLoseShift]
    results = []
    for item in registry['derivations']:
        sid = item['id']
        if sha((ROOT / item['original_path']).read_bytes()) != originals[sid]['candidate_sha256']:
            raise ValueError('Original source changed')
        source = (ROOT / item['derived_path']).read_bytes()
        if (sha(source) != item['derived_sha256'] or sha(source) != approved[sid]['derived_sha256']
                or not approved[sid].get('reviewer')):
            raise ValueError('Derived source is not the inspected source')
        cls = compile_candidate(source.decode(), sha(source))
        if sid in west:
            factory = lambda p=west[sid]: WesternReference(p)
        else:
            factory = lambda p=chinese[sid]: Reference(p)
        checks = [{'scenario': i, 'mode': 'controlled',
                   **replay(cls, factory, s['own'], s['opponent'])}
                  for i, s in enumerate(raw['scenarios'])]
        checks += [{'scenario': i, 'mode': 'candidate_on_policy',
                    **replay(cls, factory, '', opp, True)}
                   for i, opp in enumerate(raw['on_policy_opponents'])]
        matches = []
        for opponent in opponents:
            seed = seed_for(20260914, sid, opponent.__name__)
            try:
                history = axl.Match((cls(), opponent()), turns=1000,
                    game=axl.Game(r=3, s=0, t=5, p=1), noise=0, seed=seed).play()
                matches.append({'opponent': opponent.__name__, 'seed': seed,
                                'turns': len(history), 'pass': len(history) == 1000})
            except Exception as exc:
                matches.append({'opponent': opponent.__name__, 'seed': seed,
                                'pass': False, 'error': repr(exc)})
        passed = all(not c['failures'] and 'error' not in c for c in checks) and all(m['pass'] for m in matches)
        results.append({'id': sid, 'derived_sha256': sha(source), 'checks': checks,
                        'runtime': matches, 'pass': passed})
        print(json.dumps({'id': sid, 'pass': passed}), flush=True)
    report = {'created_at': now(), 'raw_validation_sha256': sha(raw_path.read_bytes()),
        'registry_sha256': sha(registry_path.read_bytes()), 'source_review_sha256': sha(review_path.read_bytes()),
        'validator_sha256': sha(Path(__file__).read_bytes()), 'common_dependencies': raw['dependencies'],
        'results': results, 'all_pass': all(r['pass'] for r in results), 'api_calls': 0,
        'scope': 'Same scenarios, adapter, references, opponents and seeds as raw v3b validation. Local derivatives, not model outputs or tournament results.'}
    report_path = ROOT / 'phase3/validation/uniform_corrections_v1.json'
    exclusive(report_path, encoded(report))
    if report['all_pass']:
        replacements = {r['id']: r for r in registry['derivations']}
        entries = []
        for number, item in enumerate(plan['requests'], 1):
            original = originals[item['id']]
            row = {'id': item['id'], 'cohort': item['cohort'], 'prose_sha256': item['prose_sha256'],
                   'original_candidate_sha256': original['candidate_sha256'], 'raw_status': original['status']}
            if item['id'] in replacements:
                change = replacements[item['id']]
                row.update(source_path=change['derived_path'], source_sha256=change['derived_sha256'],
                           provenance='local_prose_fidelity_correction')
            else:
                row.update(source_path=f'phase3/conversion_runs/uniform_v3/{number:03d}/candidate.py.txt',
                           source_sha256=original['candidate_sha256'], provenance='original_uniform_response')
            if sha((ROOT / row['source_path']).read_bytes()) != row['source_sha256']:
                raise ValueError('Final field source changed')
            entries.append(row)
        exclusive(ROOT / 'phase3/validation/uniform_derived_candidates_v1.json', encoded({
            'created_at': now(), 'raw_validation_sha256': sha(raw_path.read_bytes()),
            'correction_validation_sha256': sha(report_path.read_bytes()),
            'adapter_path': 'phase3/uniform_semantics_v3b.py',
            'adapter_sha256': sha((ROOT / 'phase3/uniform_semantics_v3b.py').read_bytes()),
            'original_responses': len(entries) - len(replacements), 'local_corrections': len(replacements),
            'candidates': entries,
            'status': 'passed_targeted_validation; tournament and four interpretation sensitivities pending'}))
    print(json.dumps({'all_pass': report['all_pass'], 'api_calls': 0}))


if __name__ == '__main__':
    main()
