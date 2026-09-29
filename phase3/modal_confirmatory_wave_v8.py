"""Sixty-four-batch Modal throughput wave, sixteen volumes, four writers each."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / 'phase3'
BUNDLE = PHASE / 'cloud_bundle_confirmatory_v1'
REGISTRATION = PHASE / 'registration_v1/public_registration.json'
BILLING = PHASE / 'inputs/modal_confirmatory_wave8_billing_gate.json'
RESULTS = PHASE / 'validation'
COMMIT = '18cb41744f3f1e66fe711aad09697980476c2498'
CONTEXT_SHA = '3811e2f65857b46003a48ddedbc0f625c1a9e573207987787f7a5f78b01d1bfd'
MANIFEST_SHA = '2dbcfc56965bd025ca2f4eb9ca2351099f5fd34101fbbd7af82fee9a43bb3ba6'
INDICES = tuple(range(195, 259))
SHARD_COUNT = 16
SHARDS = tuple(tuple(i for i in INDICES if i % SHARD_COUNT == shard)
               for shard in range(SHARD_COUNT))
VOLUMES = tuple(modal.Volume.from_name(
    f'evollm-phase3-confirmatory{("-shard" + str(i)) if i else ""}-v1',
    create_if_missing=False) for i in range(SHARD_COUNT))


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def preflight(now=None):
    from phase3.prepare_modal_confirmatory_v1 import checked_files

    for index in range(195):
        path = RESULTS / f'modal_confirmatory_batch_{index:04d}_receipt.json'
        if not path.exists():
            raise ValueError(f'Previously verified receipt {index} is missing')
        receipt = json.loads(path.read_bytes())
        if len(receipt.get('results', [])) != 250:
            raise ValueError(f'Previously verified receipt {index} is incomplete')
    for index in INDICES:
        if (RESULTS / f'modal_confirmatory_batch_{index:04d}_receipt.json').exists():
            raise ValueError(f'Batch {index} already archived; do not relaunch')
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
            or billing.get('scope') != 'phase3_confirmatory_wave_195_258_only'
            or billing.get('authorized_batch_indices') != list(INDICES)
            or billing.get('user_authorized') is not True
            or billing.get('no_recharge') is not True
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
    preflight()
    image = (modal.Image.from_registry('python:3.12.14-slim-bookworm')
             .pip_install('torch==2.14.0', index_url='https://download.pytorch.org/whl/cpu')
             .pip_install_from_requirements(str(BUNDLE / 'phase3/requirements-validation.lock.txt'))
             .env({'PYTHONPATH': '/opt/evollm', 'OMP_NUM_THREADS': '1',
                   'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1'})
             .add_local_dir(BUNDLE, remote_path='/opt/evollm'))
else:
    image = modal.Image.debian_slim()

app = modal.App('evollm-phase3-confirmatory-sharded-wave8-v1', image=image)


def run_batch(index: int, registration: dict, volume, allowed_indices):
    import sys
    sys.path.insert(0, '/opt/evollm')
    from phase3.reuse_batches_v1 import execute_batch, save_receipt, sha, validate_receipt
    from phase3.reuse_worker_v1 import verified_resolver

    if type(index) is not int or index not in allowed_indices:
        raise ValueError(f'Batch {index} is outside this volume shard')
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
            'new_matches': len(receipt['results']) - before, 'receipt_sha256': sha(receipt)}


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[0]})
def shard_0(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[0], SHARDS[0])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[1]})
def shard_1(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[1], SHARDS[1])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[2]})
def shard_2(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[2], SHARDS[2])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[3]})
def shard_3(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[3], SHARDS[3])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[4]})
def shard_4(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[4], SHARDS[4])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[5]})
def shard_5(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[5], SHARDS[5])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[6]})
def shard_6(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[6], SHARDS[6])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[7]})
def shard_7(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[7], SHARDS[7])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[8]})
def shard_8(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[8], SHARDS[8])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[9]})
def shard_9(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[9], SHARDS[9])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[10]})
def shard_10(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[10], SHARDS[10])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[11]})
def shard_11(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[11], SHARDS[11])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[12]})
def shard_12(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[12], SHARDS[12])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[13]})
def shard_13(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[13], SHARDS[13])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[14]})
def shard_14(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[14], SHARDS[14])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[15]})
def shard_15(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[15], SHARDS[15])


@app.local_entrypoint()
def main():
    registration = preflight()
    workers = (shard_0, shard_1, shard_2, shard_3, shard_4, shard_5, shard_6, shard_7, shard_8, shard_9, shard_10, shard_11, shard_12, shard_13, shard_14, shard_15)
    calls = [(index, workers[index % SHARD_COUNT].spawn(index, registration))
             for index in INDICES]
    reports, errors = [], []
    for index, call in calls:
        try:
            reports.append(call.get())
        except Exception as exc:
            errors.append({'batch_index': index, 'error': str(exc)})
    print(json.dumps({'reports': reports, 'errors': errors}, indent=2))
    if errors:
        raise RuntimeError('At least one batch failed; inspect all sixteen volume checkpoints before resuming')
