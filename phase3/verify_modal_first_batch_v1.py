"""Validate the downloaded Modal batch-0 receipt against the frozen plan."""
import hashlib
import json
from pathlib import Path

from phase3.reuse_batches_v1 import sha, validate_receipt

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / 'phase3/reuse_plan_v1'
RECEIPT = ROOT / 'phase3/validation/modal_confirmatory_batch_0000_receipt.json'


def verify():
    manifest_path = PLAN / 'manifest.json'
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != '2dbcfc56965bd025ca2f4eb9ca2351099f5fd34101fbbd7af82fee9a43bb3ba6':
        raise ValueError('Manifest changed')
    manifest = json.loads(manifest_path.read_bytes())
    context = json.loads((PLAN / 'context.json').read_bytes())
    if sha(context) != '3811e2f65857b46003a48ddedbc0f625c1a9e573207987787f7a5f78b01d1bfd':
        raise ValueError('Context changed')
    entry = manifest['batches'][0]
    batch_path = PLAN / entry['path']
    if hashlib.sha256(batch_path.read_bytes()).hexdigest() != entry['file_sha256']:
        raise ValueError('Frozen batch changed')
    batch = json.loads(batch_path.read_bytes())
    receipt = json.loads(RECEIPT.read_bytes())
    validate_receipt(receipt, batch, context, require_complete=True)
    if len(batch['jobs']) != 250 or len(receipt['results']) != 250:
        raise ValueError('Batch 0 should contain exactly 250 matches')
    return {'batch_index': 0, 'matches': 250, 'errors': 0,
            'batch_sha256': batch['batch_sha256'],
            'receipt_sha256': sha(receipt),
            'receipt_file_sha256': hashlib.sha256(RECEIPT.read_bytes()).hexdigest(),
            'logical_scenario_results': sum(len(job['scenarios']) for job in batch['jobs'])}


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
