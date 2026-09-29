"""Sixteen-batch Modal wave, split over four volumes (four writers each).

Only frozen confirmatory batch indices 19..34 can be scheduled by this app.
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
BILLING = PHASE / 'inputs/modal_confirmatory_wave4_billing_gate.json'
RESULTS = PHASE / 'validation'
COMMIT = '18cb41744f3f1e66fe711aad09697980476c2498'
CONTEXT_SHA = '3811e2f65857b46003a48ddedbc0f625c1a9e573207987787f7a5f78b01d1bfd'
MANIFEST_SHA = '2dbcfc56965bd025ca2f4eb9ca2351099f5fd34101fbbd7af82fee9a43bb3ba6'
INDICES = tuple(range(19, 35))
PRIOR_RECEIPTS = {
    0: '2d2293775227a1cce18ba1f7e4e2bbb5e57efb4afcb2cab249c960bfa4dc240c',
    1: '5d7d63c61af0bf802133332566d8c124fc2bb73decbd2569fc157e6992d0e980',
    2: 'ecfafc003fa668aff8da0b77b570a69b4138538dda484e2ce0a8cb63ddff83d3',
    3: '8d47fc16e11766eacd9c1d74a545ca867bbb6e104e429e42849138456c302121',
    4: 'f6e334b8f44058503d80966ea8f22a4aea1a33e7aaeef5d62f8cdac7c84ece87',
    5: '70bf0acb2ec4158813526357bcf9e825b70f8ff343751b6a3b0f40f666f52e38',
    6: 'e86dc23732322691861989a77f8056a84f976aacfd75a34aa8f7f8b70e000061',
    7: '3435c1164dbdfdb401dd93e30432d5d0cd594da719a71792223e24e13049a279',
    8: '6c74ae7f6ed522230549f9b2293ebd7c3851d596c31beb32458c8f7c7e09e7fe',
    9: '000111fbf16054b55c20990e118d5ecad8e46cab7b9322a946493ea935cea0b5',
    10: '003c4cf626fb2da53982047625ff127c3948086897341d85047a3bdf964fdde3',
    11: '414afc66c3fabf15e9b19c438c684ec349d458e9546c4cfb29dc5b02d0f639be',
    12: 'c764b006a9983f50ee8424a783a2cfff2b8f7609d6bf5194c42f138978584ba7',
    13: '86433d59bc0139384f42b476c180adc55574ed8d044a02600ec4dd129523c6ac',
    14: '74b4694bdf54db48583a224f4c1cce718463809ccffdeb8bae227720a04d057f',
    15: '700a1e5d4b61d9ba0d16ece467bd050cb578b13edbe9dd9fed4c87f2b8dfa0ce',
    16: 'f0c544735f2481eede451951d124c579baf321423bc1ccdb3609c2f8efb0ada0',
    17: '28c9cf7daf01403c02b538f94c9a23471975f45aa6be8fc999034364711ba9d6',
    18: '071bacf090110cc3ce61e4c341ca42478cd3069f23608da03f1c8b86951a5f7a',
}
SHARDS = (
    (19, 20, 21, 22), (23, 24, 25, 26),
    (27, 28, 29, 30), (31, 32, 33, 34),
)
VOLUMES = (
    modal.Volume.from_name('evollm-phase3-confirmatory-v1', create_if_missing=False),
    modal.Volume.from_name('evollm-phase3-confirmatory-shard1-v1', create_if_missing=False),
    modal.Volume.from_name('evollm-phase3-confirmatory-shard2-v1', create_if_missing=False),
    modal.Volume.from_name('evollm-phase3-confirmatory-shard3-v1', create_if_missing=False),
)


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def preflight(now=None):
    from phase3.prepare_modal_confirmatory_v1 import checked_files
    for index, expected in PRIOR_RECEIPTS.items():
        path = RESULTS / f'modal_confirmatory_batch_{index:04d}_receipt.json'
        if not path.exists() or file_sha(path) != expected:
            raise ValueError(f'Prior batch {index} receipt hash changed or is missing')
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
            or billing.get('scope') != 'phase3_confirmatory_wave_19_34_only'
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
    preflight()
    image = (modal.Image.from_registry('python:3.12.14-slim-bookworm')
             .pip_install('torch==2.14.0', index_url='https://download.pytorch.org/whl/cpu')
             .pip_install_from_requirements(str(BUNDLE / 'phase3/requirements-validation.lock.txt'))
             .env({'PYTHONPATH': '/opt/evollm', 'OMP_NUM_THREADS': '1',
                   'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1'})
             .add_local_dir(BUNDLE, remote_path='/opt/evollm'))
else:
    image = modal.Image.debian_slim()

app = modal.App('evollm-phase3-confirmatory-sharded-wave4-v1', image=image)


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
def shard0(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[0], SHARDS[0])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[1]})
def shard1(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[1], SHARDS[1])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[2]})
def shard2(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[2], SHARDS[2])


@app.function(cpu=(1, 1), memory=(1024, 2048), timeout=3600, retries=0, max_containers=4,
              volumes={'/results': VOLUMES[3]})
def shard3(index: int, registration: dict):
    return run_batch(index, registration, VOLUMES[3], SHARDS[3])


@app.local_entrypoint()
def main():
    registration = preflight()
    functions = (shard0, shard1, shard2, shard3)
    calls = []
    for shard_number, indices in enumerate(SHARDS):
        for index in indices:
            calls.append((index, functions[shard_number].spawn(index, registration)))
    reports, errors = [], []
    for index, call in calls:
        try:
            reports.append(call.get())
        except Exception as exc:
            errors.append({'batch_index': index, 'error': str(exc)})
    print(json.dumps({'reports': reports, 'errors': errors}, indent=2))
    if errors:
        raise RuntimeError('At least one batch failed; inspect all four volume checkpoints before resuming')
