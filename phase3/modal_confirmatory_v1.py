"""One explicitly selected confirmatory batch per Modal invocation.

No function is launched while the OSF public gate or fresh billing gate is absent.
This operational wrapper is outside the frozen scientific inventory.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / 'phase3'
DEST = PHASE / 'cloud_bundle_confirmatory_v1'
EXPECTED_CONTEXT_SHA256 = '3811e2f65857b46003a48ddedbc0f625c1a9e573207987787f7a5f78b01d1bfd'
EXPECTED_MANIFEST_SHA256 = '2dbcfc56965bd025ca2f4eb9ca2351099f5fd34101fbbd7af82fee9a43bb3ba6'

REGISTRATION = PHASE / 'registration_v1/public_registration.json'
BILLING = PHASE / 'inputs/modal_confirmatory_billing_gate.json'
DOWNLOADED_RECEIPT = PHASE / 'validation/modal_confirmatory_batch_0000_receipt.json'
FROZEN_COMMIT = '18cb41744f3f1e66fe711aad09697980476c2498'


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def preflight(now=None):
    """Fail closed before constructing a remotely buildable image."""
    from phase3.prepare_modal_confirmatory_v1 import checked_files
    if DOWNLOADED_RECEIPT.exists():
        raise ValueError('Batch 0 receipt is already archived locally; do not relaunch')
    if not REGISTRATION.exists():
        raise ValueError('Public OSF registration gate is missing')
    registration = json.loads(REGISTRATION.read_bytes())
    if (registration.get('public_registration_url') != 'https://osf.io/2nzdh/overview'
            or registration.get('frozen_git_commit') != FROZEN_COMMIT
            or registration.get('context_sha256') != EXPECTED_CONTEXT_SHA256
            or registration.get('plan_manifest_sha256') != EXPECTED_MANIFEST_SHA256
            or not registration.get('public_visibility_verified_at_utc')):
        raise ValueError('Public OSF registration gate does not match the frozen plan')
    if not BILLING.exists():
        raise ValueError('Fresh Modal billing and tournament authorization gate is missing')
    billing = json.loads(BILLING.read_bytes())
    instant = datetime.fromisoformat(billing['verified_at_utc'].replace('Z', '+00:00'))
    now = now or datetime.now(timezone.utc)
    if (billing.get('workspace') != 'unimayor-evollm'
            or billing.get('scope') != 'phase3_confirmatory_first_batch_only'
            or billing.get('authorized_batch_indices') != [0]
            or billing.get('user_authorized') is not True
            or billing.get('spend_limit_usd') != 0
            or billing.get('usage_limit_usd') != 30
            or not 0 < billing.get('remaining_credits_usd', 0) <= 30
            or not 0 <= (now - instant).total_seconds() <= 1800):
        raise ValueError('Modal credits/limits/authorization must be freshly verified')
    declaration = json.loads((DEST / 'BUNDLE_DECLARATION.json').read_bytes())
    if (declaration.get('files') != 1297 or declaration.get('bytes') != 100433684
            or declaration.get('plan_manifest_sha256') != EXPECTED_MANIFEST_SHA256):
        raise ValueError('Bundle declaration changed')
    # Verify the copy and original independently before any image build/upload.
    files = checked_files()
    for name, contents in files:
        if (DEST / name).read_bytes() != contents:
            raise ValueError('Cloud bundle differs from frozen source: ' + name)
    return registration, billing


if modal.is_local():
    # Modal may build/upload an image before it enters main().
    preflight()
    image = (modal.Image.from_registry('python:3.12.14-slim-bookworm')
             .pip_install('torch==2.14.0', index_url='https://download.pytorch.org/whl/cpu')
             .pip_install_from_requirements(str(DEST / 'phase3/requirements-validation.lock.txt'))
             .env({'PYTHONPATH': '/opt/evollm', 'OMP_NUM_THREADS': '1',
                   'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1'})
             .add_local_dir(DEST, remote_path='/opt/evollm'))
else:
    image = modal.Image.debian_slim()

app = modal.App('evollm-phase3-confirmatory-v1', image=image)
volume = modal.Volume.from_name('evollm-phase3-confirmatory-v1', create_if_missing=True)


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0,
              max_containers=1, volumes={'/results': volume})
def one_batch(index: int, registration: dict):
    import sys
    sys.path.insert(0, '/opt/evollm')
    from phase3.reuse_batches_v1 import execute_batch, save_receipt, sha, validate_receipt
    from phase3.reuse_worker_v1 import verified_resolver

    base = Path('/opt/evollm/phase3/reuse_plan_v1')
    manifest_path = base / 'manifest.json'
    context = json.loads((base / 'context.json').read_bytes())
    manifest = json.loads(manifest_path.read_bytes())
    if (file_sha(manifest_path) != EXPECTED_MANIFEST_SHA256
            or sha(context) != EXPECTED_CONTEXT_SHA256
            or manifest['context_sha256'] != EXPECTED_CONTEXT_SHA256
            or registration.get('public_registration_url') != 'https://osf.io/2nzdh/overview'
            or registration.get('frozen_git_commit') != FROZEN_COMMIT
            or registration.get('context_sha256') != EXPECTED_CONTEXT_SHA256
            or registration.get('plan_manifest_sha256') != EXPECTED_MANIFEST_SHA256):
        raise ValueError('Remote frozen/public registration gate failed')
    if type(index) is not int or index != 0:
        raise ValueError('This launcher is authorized for batch 0 only')
    entry = manifest['batches'][index]
    batch_path = base / entry['path']
    if file_sha(batch_path) != entry['file_sha256']:
        raise ValueError('Frozen batch changed')
    batch = json.loads(batch_path.read_bytes())
    if batch['batch_sha256'] != entry['batch_sha256']:
        raise ValueError('Batch identity changed')
    volume.reload()
    output = Path('/results') / entry['path']
    prior = json.loads(output.read_bytes()) if output.exists() else None
    before = len(prior['results']) if prior else 0
    if prior is not None:
        validate_receipt(prior, batch, context)
    resolve = verified_resolver(context)

    def checkpoint(receipt):
        save_receipt(output, receipt)
        volume.commit()

    receipt = execute_batch(batch, context, resolve, previous=prior, checkpoint=checkpoint)
    validate_receipt(receipt, batch, context, require_complete=True)
    return {'batch_index': index, 'batch_sha256': batch['batch_sha256'],
            'matches_before': before, 'matches_after': len(receipt['results']),
            'new_matches': len(receipt['results']) - before,
            'receipt_sha256': sha(receipt)}


@app.local_entrypoint()
def main(batch_index: int):
    # A single batch is an intentional cost-observation wave; no implicit loop.
    if batch_index != 0:
        raise ValueError('This launcher is authorized for batch 0 only')
    registration, _ = preflight()
    report = one_batch.remote(batch_index, registration)
    print(json.dumps(report, indent=2))
