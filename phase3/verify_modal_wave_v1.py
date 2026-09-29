"""Verify archived Modal receipts for the first bounded concurrency wave."""
import hashlib
import json
from pathlib import Path

from phase3.reuse_batches_v1 import sha, validate_receipt

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / 'phase3'
PLAN = PHASE / 'reuse_plan_v1'
EXPECTED_CONTEXT_SHA = '3811e2f65857b46003a48ddedbc0f625c1a9e573207987787f7a5f78b01d1bfd'
EXPECTED_MANIFEST_SHA = '2dbcfc56965bd025ca2f4eb9ca2351099f5fd34101fbbd7af82fee9a43bb3ba6'


def verify(indices=(0, 1, 2)):
    manifest_path = PLAN / 'manifest.json'
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != EXPECTED_MANIFEST_SHA:
        raise ValueError('Frozen manifest changed')
    manifest = json.loads(manifest_path.read_bytes())
    context = json.loads((PLAN / 'context.json').read_bytes())
    if sha(context) != EXPECTED_CONTEXT_SHA or manifest['context_sha256'] != EXPECTED_CONTEXT_SHA:
        raise ValueError('Frozen context changed')
    rows = []
    for index in indices:
        entry = manifest['batches'][index]
        batch_path = PLAN / entry['path']
        if hashlib.sha256(batch_path.read_bytes()).hexdigest() != entry['file_sha256']:
            raise ValueError(f'Batch {index} file changed')
        batch = json.loads(batch_path.read_bytes())
        if batch['batch_sha256'] != entry['batch_sha256']:
            raise ValueError(f'Batch {index} identity changed')
        receipt_path = PHASE / 'validation' / f'modal_confirmatory_batch_{index:04d}_receipt.json'
        receipt = json.loads(receipt_path.read_bytes())
        validate_receipt(receipt, batch, context, require_complete=True)
        if len(receipt['results']) != entry['matches']:
            raise ValueError(f'Batch {index} count changed')
        rows.append({'index': index, 'matches': len(receipt['results']),
                     'logical_scenario_results': sum(len(job['scenarios']) for job in batch['jobs']),
                     'batch_sha256': batch['batch_sha256'],
                     'receipt_sha256': sha(receipt),
                     'receipt_file_sha256': hashlib.sha256(receipt_path.read_bytes()).hexdigest()})
    return {'batches': rows, 'matches': sum(row['matches'] for row in rows),
            'logical_scenario_results': sum(row['logical_scenario_results'] for row in rows),
            'errors': 0}


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
