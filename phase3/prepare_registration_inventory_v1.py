"""Inventory the exact scientific files proposed for a local Git freeze.

This is an allowlist. It does not stage, commit, upload, or execute a match.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / 'phase3'
DEST = PHASE / 'registration_v1'

EXTRA = {
    'phase3/PHASE3_PROTOCOL_v1.md',
    'phase3/inputs/execution_config_v3.json',
    'phase3/DESIGN_v0.3_DRAFT.md',
    'phase3/SENSITIVITIES_v1_DRAFT.md',
    'phase3/EXECUTION_RESOURCES_v1.md',
    'phase3/REUSE_BATCHES_v1.md',
    'phase3/MODAL_REUSE_DIAGNOSTIC_RESULTS_v1.md',
    'phase3/analyze_phase3.py',
    'phase3/sensitivity_analysis_v1.py',
    'phase3/reuse_batches_v1.py',
    'phase3/reuse_worker_v1.py',
    'phase3/reuse_dispatch_v1.py',
    'phase3/prepare_reuse_plan_v1.py',
    'phase3/verify_reuse_plan_v1.py',
    'phase3/inputs/population_protocol_v0_3.json',
    'phase3/validation/reuse_closure_v1.json',
    'phase3/validation/h7_unequal_v1.json',
    'phase3/validation/sensitivity_closure_v1.json',
    'phase3/validation/modal_reuse_diagnostic_remote_v1.json',
    'phase3/prepare_registration_inventory_v1.py',
}


def main():
    output = DEST / 'freeze_inventory_v2.json'
    if output.exists():
        raise ValueError('Final registration inventory already exists; use a new version')
    prior = json.loads((PHASE / 'cloud_bundle_v2/BUNDLE_INVENTORY.json').read_bytes())
    if len(prior['files']) != 595 or prior['total_bytes'] != 20_395_288:
        raise ValueError('Reviewed scientific allowlist changed')
    prior_paths = {row['path'] for row in prior['files']}
    paths = set(prior_paths)
    paths.update('phase3/reuse_plan_v1/' + path.name
                 for path in (PHASE / 'reuse_plan_v1').glob('*.json'))
    paths.update(EXTRA)
    paths.update(path.relative_to(ROOT).as_posix()
                 for path in (PHASE / 'tests').glob('test_*.py'))
    forbidden = ('cloud_bundle', 'api_response', 'api_request',
                 'token', 'secret', '.env', '__pycache__', 'receipt_v1.json')
    records = []
    for name in sorted(paths):
        relative = Path(name)
        if (relative.parts[0] != 'phase3' or relative.is_absolute()
                or '..' in relative.parts or any(part in name.lower() for part in forbidden)):
            raise ValueError('Unexpected path in public freeze candidate: ' + name)
        if 'conversion_runs' in relative.parts and (name not in prior_paths or relative.name != 'candidate.py.txt'):
            raise ValueError('Only vetted candidate sources may enter from conversion runs: ' + name)
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise ValueError('Missing/nonregular scientific file: ' + name)
        raw = path.read_bytes()
        records.append({'path': name, 'bytes': len(raw),
                        'sha256': hashlib.sha256(raw).hexdigest()})
    if len([x for x in records if x['path'].startswith('phase3/reuse_plan_v1/')]) != 667:
        raise ValueError('Plan inventory must contain context, manifest and 665 batches')
    if len(records) < 1290:
        raise ValueError('Scientific freeze inventory unexpectedly small')
    manifest = {
        'status': 'scientific_material_bound_for_registration_not_publicly_registered',
        'scope': 'Scientific sources, executable plan, analysis, protocol, selected validation; no API receipts or cloud copies',
        'prior_modal_allowlist_files': 595,
        'plan_files': 667,
        'files': records,
        'total_files': len(records),
        'total_bytes': sum(row['bytes'] for row in records),
    }
    DEST.mkdir(exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps({'total_files': manifest['total_files'],
                      'total_bytes': manifest['total_bytes'],
                      'inventory_sha256': hashlib.sha256(output.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
