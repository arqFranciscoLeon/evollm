"""Bounded Modal diagnostic for the exact-reuse worker; never runs full batches."""
import hashlib
import json
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / 'phase3/cloud_bundle_reuse_diagnostic_v1'
if modal.is_local():
    preparation = json.loads((ROOT / 'phase3/reuse_diagnostic_v1/preparation.json').read_bytes())
    inventory = json.loads((BUNDLE / 'BUNDLE_INVENTORY.json').read_bytes())
    if (preparation['unique_matches'] > 16 or inventory['total_bytes'] > 22_000_000
            or preparation['bundle_inventory_sha256'] != hashlib.sha256(
                (BUNDLE / 'BUNDLE_INVENTORY.json').read_bytes()).hexdigest()):
        raise ValueError('Diagnostic upload exceeds reviewed bound or changed')
    image = (modal.Image.from_registry('python:3.12.14-slim-bookworm')
             .pip_install('torch==2.14.0', index_url='https://download.pytorch.org/whl/cpu')
             .pip_install_from_requirements(str(BUNDLE / 'phase3/requirements-validation.lock.txt'))
             .env({'PYTHONPATH': '/opt/evollm', 'OMP_NUM_THREADS': '1',
                   'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1'})
             .add_local_dir(BUNDLE, remote_path='/opt/evollm'))
else:
    image = modal.Image.debian_slim()

app = modal.App('evollm-phase3-reuse-diagnostic-v1', image=image)
volume = modal.Volume.from_name('evollm-phase3-reuse-diagnostic-v1', create_if_missing=True)


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=600, retries=0,
              max_containers=1, volumes={'/results': volume})
def stage(target_count: int):
    import sys
    sys.path.insert(0, '/opt/evollm')
    from phase3.reuse_batches_v1 import execute_batch, save_receipt, sha, validate_receipt
    from phase3.reuse_worker_v1 import verified_resolver
    if target_count not in (0, 2, 16):
        raise ValueError('Only fixed diagnostic stages are permitted')
    base = Path('/opt/evollm')
    inventory = json.loads((base / 'BUNDLE_INVENTORY.json').read_bytes())
    if inventory['scope'] != 'selected_diagnostic; at most 16 distinct matches; no confirmatory export':
        raise ValueError('Wrong upload scope')
    for row in inventory['files']:
        if hashlib.sha256((base / row['path']).read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('Bundle changed: ' + row['path'])
    context = json.loads((base / 'phase3/reuse_diagnostic_v1/context.json').read_bytes())
    batch = json.loads((base / 'phase3/reuse_diagnostic_v1/batch.json').read_bytes())
    if context['scope'] != 'selected_diagnostic' or len(batch['jobs']) > 16:
        raise ValueError('Not a bounded diagnostic batch')
    volume.reload()
    receipt_path = Path('/results') / (batch['batch_sha256'] + '.json')
    previous = json.loads(receipt_path.read_bytes()) if receipt_path.exists() else None
    before = len(previous['results']) if previous else 0
    resolve = verified_resolver(context)

    def checkpoint(receipt):
        save_receipt(receipt_path, receipt)
        volume.commit()

    target = min(target_count, len(batch['jobs'])) if target_count else before
    receipt = execute_batch(batch, context, resolve, previous=previous,
                            checkpoint=checkpoint, max_new=max(target - before, 0))
    validate_receipt(receipt, batch, context)
    return {'scope': context['scope'], 'batch_sha256': batch['batch_sha256'],
            'before': before, 'after': len(receipt['results']),
            'new': len(receipt['results']) - before,
            'complete': len(receipt['results']) == len(batch['jobs']),
            'receipt_sha256': sha(receipt), 'receipt': receipt}


@app.local_entrypoint()
def main():
    def receipt_sha(value):
        raw = json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)
        return hashlib.sha256(raw.encode()).hexdigest()

    out = ROOT / 'phase3/validation/modal_reuse_diagnostic_remote_v1.json'
    if out.exists():
        raise ValueError('Remote diagnostic already saved; do not repeat')
    local = json.loads((ROOT / 'phase3/reuse_diagnostic_v1/local_baseline.json').read_bytes())
    context = json.loads((ROOT / 'phase3/reuse_diagnostic_v1/context.json').read_bytes())
    batch = json.loads((ROOT / 'phase3/reuse_diagnostic_v1/batch.json').read_bytes())
    first = stage.remote(2)
    if first['after'] < 2 or first['receipt']['results'] != local['results'][:first['after']]:
        raise ValueError('First stage did not preserve the exact local prefix')
    second = stage.remote(16)
    if second['before'] != first['after'] or not second['complete']:
        raise ValueError('Second stage did not resume and complete')
    if second['receipt'] != local or second['receipt']['results'][:first['after']] != first['receipt']['results']:
        raise ValueError('Remote results or recovery differ from Windows baseline')
    third = stage.remote(0)
    if third['new'] != 0 or third['receipt_sha256'] != receipt_sha(local):
        raise ValueError('Completed batch was recomputed or changed')
    report = {'scope': context['scope'], 'matches': len(batch['jobs']),
              'preexisting': first['before'], 'first_new': first['new'], 'resume_new': second['new'],
              'repeat_new': third['new'], 'complete': True,
              'windows_linux_exact': True, 'receipt_sha256': receipt_sha(local),
              'batch_sha256': batch['batch_sha256']}
    with out.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
    print(json.dumps(report, indent=2))
