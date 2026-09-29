"""Eight-batch bounded Modal wave after the verified two-container check.

This operational wrapper cannot schedule any index outside 3..10.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / 'phase3'
BUNDLE = PHASE / 'cloud_bundle_confirmatory_v1'
REGISTRATION = PHASE / 'registration_v1/public_registration.json'
BILLING = PHASE / 'inputs/modal_confirmatory_wave2_billing_gate.json'
RESULTS = PHASE / 'validation'
COMMIT = '18cb41744f3f1e66fe711aad09697980476c2498'
CONTEXT_SHA = '3811e2f65857b46003a48ddedbc0f625c1a9e573207987787f7a5f78b01d1bfd'
MANIFEST_SHA = '2dbcfc56965bd025ca2f4eb9ca2351099f5fd34101fbbd7af82fee9a43bb3ba6'
BATCH0_RECEIPT_SHA = '2d2293775227a1cce18ba1f7e4e2bbb5e57efb4afcb2cab249c960bfa4dc240c'
PRIOR_RECEIPTS = {
    0: BATCH0_RECEIPT_SHA,
    1: '5d7d63c61af0bf802133332566d8c124fc2bb73decbd2569fc157e6992d0e980',
    2: 'ecfafc003fa668aff8da0b77b570a69b4138538dda484e2ce0a8cb63ddff83d3',
}
INDICES = tuple(range(3, 11))


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def preflight(now=None):
    from phase3.prepare_modal_confirmatory_v1 import checked_files

    for index, expected in PRIOR_RECEIPTS.items():
        if file_sha(RESULTS / f'modal_confirmatory_batch_{index:04d}_receipt.json') != expected:
            raise ValueError(f'Prior batch {index} baseline changed')
    if all((RESULTS / f'modal_confirmatory_batch_{i:04d}_receipt.json').exists() for i in INDICES):
        raise ValueError('Both wave receipts already archived; do not relaunch')
    registration = json.loads(REGISTRATION.read_bytes())
    if (registration.get('public_registration_url') != 'https://osf.io/2nzdh/overview'
            or registration.get('frozen_git_commit') != COMMIT
            or registration.get('context_sha256') != CONTEXT_SHA
            or registration.get('plan_manifest_sha256') != MANIFEST_SHA
            or not registration.get('public_visibility_verified_at_utc')):
        raise ValueError('Frozen public registration gate failed')
    billing = json.loads(BILLING.read_bytes())
    instant = datetime.fromisoformat(billing['verified_at_utc'].replace('Z', '+00:00'))
    now = now or datetime.now(timezone.utc)
    if (billing.get('workspace') != 'unimayor-evollm'
            or billing.get('scope') != 'phase3_confirmatory_wave_3_10_only'
            or billing.get('authorized_batch_indices') != list(INDICES)
            or billing.get('user_authorized') is not True
            or billing.get('usage_limit_usd') != 30
            or billing.get('spend_limit_usd') != 0
            or billing.get('remaining_credits_usd', 0) < 1
            or not 0 <= (now - instant).total_seconds() <= 1800):
        raise ValueError('Fresh credit-only authorization gate failed')
    declaration = json.loads((BUNDLE / 'BUNDLE_DECLARATION.json').read_bytes())
    if (declaration.get('files') != 1297 or declaration.get('bytes') != 100433684
            or declaration.get('plan_manifest_sha256') != MANIFEST_SHA):
        raise ValueError('Bundle declaration changed')
    for name, contents in checked_files():
        if (BUNDLE / name).read_bytes() != contents:
            raise ValueError('Bundle source changed: ' + name)
    return registration


if modal.is_local():
    preflight()  # Run before Modal can build or upload an image.
    image = (modal.Image.from_registry('python:3.12.14-slim-bookworm')
             .pip_install('torch==2.14.0', index_url='https://download.pytorch.org/whl/cpu')
             .pip_install_from_requirements(str(BUNDLE / 'phase3/requirements-validation.lock.txt'))
             .env({'PYTHONPATH': '/opt/evollm', 'OMP_NUM_THREADS': '1',
                   'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1'})
             .add_local_dir(BUNDLE, remote_path='/opt/evollm'))
else:
    image = modal.Image.debian_slim()

app = modal.App('evollm-phase3-confirmatory-wave2-v1', image=image)
volume = modal.Volume.from_name('evollm-phase3-confirmatory-v1', create_if_missing=False)


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0,
              max_containers=4, volumes={'/results': volume})
def one_batch(index: int, registration: dict):
    import sys
    sys.path.insert(0, '/opt/evollm')
    from phase3.reuse_batches_v1 import execute_batch, save_receipt, sha, validate_receipt
    from phase3.reuse_worker_v1 import verified_resolver

    if type(index) is not int or index not in INDICES:
        raise ValueError('Only batch indices 3..10 are allowed')
    plan = Path('/opt/evollm/phase3/reuse_plan_v1')
    manifest_path = plan / 'manifest.json'
    manifest = json.loads(manifest_path.read_bytes())
    context = json.loads((plan / 'context.json').read_bytes())
    if (file_sha(manifest_path) != MANIFEST_SHA or sha(context) != CONTEXT_SHA
            or manifest['context_sha256'] != CONTEXT_SHA
            or registration.get('public_registration_url') != 'https://osf.io/2nzdh/overview'
            or registration.get('frozen_git_commit') != COMMIT
            or registration.get('context_sha256') != CONTEXT_SHA
            or registration.get('plan_manifest_sha256') != MANIFEST_SHA):
        raise ValueError('Remote frozen/public registration gate failed')
    entry = manifest['batches'][index]
    batch_path = plan / entry['path']
    if file_sha(batch_path) != entry['file_sha256']:
        raise ValueError('Frozen batch changed')
    batch = json.loads(batch_path.read_bytes())
    if batch['batch_sha256'] != entry['batch_sha256']:
        raise ValueError('Batch identity changed')
    volume.reload()
    output = Path('/results') / entry['path']
    previous = json.loads(output.read_bytes()) if output.exists() else None
    before = len(previous['results']) if previous else 0
    if previous is not None:
        validate_receipt(previous, batch, context)
    resolve = verified_resolver(context)

    def checkpoint(receipt):
        save_receipt(output, receipt)
        volume.commit()

    receipt = execute_batch(batch, context, resolve, previous=previous, checkpoint=checkpoint)
    validate_receipt(receipt, batch, context, require_complete=True)
    return {'batch_index': index, 'batch_sha256': batch['batch_sha256'],
            'matches_before': before, 'matches_after': len(receipt['results']),
            'new_matches': len(receipt['results']) - before,
            'receipt_sha256': sha(receipt)}


@app.local_entrypoint()
def main():
    registration = preflight()
    calls = [(index, one_batch.spawn(index, registration)) for index in INDICES]
    reports, errors = [], []
    for index, call in calls:
        try:
            reports.append(call.get())
        except Exception as exc:
            errors.append({'batch_index': index, 'error': str(exc)})
    print(json.dumps({'reports': reports, 'errors': errors}, indent=2))
    if errors:
        raise RuntimeError('At least one batch failed; inspect volume checkpoints before resuming')
