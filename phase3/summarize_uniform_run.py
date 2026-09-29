"""Reconcile the completed uniform API run without network access."""
import json
from collections import Counter
from phase3.uniform_converter import load_plan, ledger, RUN_DIR, PLAN_SHA256
from phase3.pilot_converter import ROOT, encoded, exclusive, now, sha


def main():
    plan, _ = load_plan()
    state = ledger(RUN_DIR, plan)
    if state['completed'] != 572 or state['blocked']:
        raise ValueError('Complete run required')
    usage = Counter()
    models = Counter()
    records = []
    for i, item in enumerate(plan['requests'], 1):
        folder = RUN_DIR / f'{i:03d}'
        response = json.loads((folder / 'response.bin').read_bytes())
        receipt = json.loads((folder / 'receipt.json').read_bytes())
        request = json.loads((folder / 'request.json').read_bytes())
        u = response['usage']
        usage.update({k: u[k] for k in ('prompt_tokens', 'completion_tokens', 'total_tokens')})
        usage['cached_tokens'] += (u.get('prompt_tokens_details') or {}).get('cached_tokens', 0)
        models[response['model']] += 1
        records.append({'id': item['id'], 'candidate_sha256': sha((folder / 'candidate.py.txt').read_bytes()),
                        'receipt_sha256': sha((folder / 'receipt.json').read_bytes()),
                        'started_at': request.get('started_at'), 'finished_at': receipt['finished_at']})
    report = {'created_at': now(), 'plan_sha256': PLAN_SHA256, 'ledger': state,
              'usage': dict(usage), 'returned_models': dict(models), 'records': records,
              'cost_usd_calculated_not_invoice': state['settled_nano_usd'] / 1e9,
              'status': 'responses_received_not_fidelity_certification'}
    exclusive(ROOT / 'phase3/validation/uniform_conversion_receipt_v3.json', encoded(report))
    print(json.dumps({k: v for k, v in report.items() if k != 'records'}))


if __name__ == '__main__':
    main()
