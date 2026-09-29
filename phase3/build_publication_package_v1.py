"""Create a local, checksum-verified Phase 3 replication ZIP.

The ZIP has project-root-relative paths and can be extracted into a fresh
directory. It includes the registered scientific snapshot and post-run outputs.
It never contacts a network service.
"""
import hashlib
import json
from pathlib import Path
import zipfile

from phase3.verify_modal_wave_v1 import verify

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / 'phase3'
BUNDLE = PHASE / 'cloud_bundle_confirmatory_v1'
INVENTORY = PHASE / 'registration_v1/freeze_inventory_v2.json'
OUTDIR = PHASE / 'publication_v1'
ARCHIVE = OUTDIR / 'EvoLLM_Phase3_Replication_v1.zip'
SIDECAR = OUTDIR / 'EvoLLM_Phase3_Replication_v1.sha256.json'
EXPECTED_INVENTORY_SHA = '27ee8121f14ccb7d5cd7fb5838c224ad8e7207010fdc92335f52e4a2acfcebf4'
EXPECTED_COMMIT = '18cb41744f3f1e66fe711aad09697980476c2498'
EXPECTED_REGISTRATION = 'https://osf.io/2nzdh/overview'


def digest(data):
    return hashlib.sha256(data).hexdigest()


README = """# EvoLLM Phase 3 replication package, version 1

Public preregistration: https://osf.io/2nzdh/overview  
Frozen scientific commit: 18cb41744f3f1e66fe711aad09697980476c2498

This package contains the 1,297 files in the frozen scientific inventory, the
665 confirmatory batch receipts, the public registration record, and the
analysis code and outputs produced after execution. The frozen documents retain
their pre-execution wording; the appended reports describe the completed run.
The package contains no API response archive or account credentials.

The tournament has 572 eligible strategy identities and 16 interpretation
scenarios. Exact reuse required 166,172 computational encounters to reconstruct
2,622,048 logical scenario results. Batch 664 has 172 encounters; the preceding
664 batches have 250 each. The primary H7 test uses scenario 0, 10,000
within-attitude permutations of model labels, seed 20260913, and a one-sided
threshold of 0.05. Secondary scenarios and sensitivities have no additional
confirmatory p-values.

`phase3/ANALYSIS_CORRECTION_LOG_v1.md` documents a pre-deposit correction to
the descriptive attitude-mixture table. A synthetic regression test for its
weights is included at `phase3/tests/test_confirmatory_reporting_v1.py`.

## Check the archive

`MANIFEST.json` records the SHA-256 and byte count of every payload file.
The adjacent `.sha256.json` file, supplied beside the ZIP, records the ZIP's
SHA-256. Extract the ZIP preserving its project-root-relative `phase3/` paths.

In an environment with Python 3.12.14 and the dependencies in
`phase3/requirements-validation.lock.txt`, verify the complete schedule:

```text
python -c "from phase3.verify_modal_wave_v1 import verify; x=verify(tuple(range(665))); print(x['matches'], x['logical_scenario_results'], x['errors'])"
```

Expected output: `166172 2622048 0`. The analyzer's full JSON output is
`phase3/validation/confirmatory_analysis_v1.json`; the human-readable report
is `phase3/CONFIRMATORY_RESULTS_v1.md`. Model-by-attitude and mixture tables
are rendered in `phase3/DESCRIPTIVE_RESULTS_v1.md`.

To recompute the analysis, work in a separate copy of the extracted package,
move those two supplied outputs out of the copy, and run:

```text
python -B -m phase3.analyze_confirmatory_results_v1
```

The script refuses to overwrite existing outputs, rechecks the registered
source and all receipts, reconstructs all 16 matrices, and runs the single
prespecified H7 permutation test. It makes no API calls.

The permutation interval in the report is a null reference interval, not a
confidence interval for the effect. Bounds for the 28 excluded descriptions
are algebraic and do not substitute invented strategies.
"""


def safe_name(name):
    path = Path(name)
    if (path.is_absolute() or not path.parts or path.parts[0] != 'phase3'
            or '..' in path.parts or '\\' in name):
        raise ValueError('Unsafe archive path: ' + name)
    return name


def make_zipinfo(name):
    info = zipfile.ZipInfo(name, date_time=(2026, 9, 28, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o644 << 16
    return info


def build():
    if ARCHIVE.exists() or SIDECAR.exists():
        raise FileExistsError('Existing package; inspect before rebuilding')
    raw_inventory = INVENTORY.read_bytes()
    if digest(raw_inventory) != EXPECTED_INVENTORY_SHA:
        raise ValueError('Registered frozen inventory hash changed')
    inventory = json.loads(raw_inventory)
    if inventory.get('total_files') != 1297 or inventory.get('total_bytes') != 100433684:
        raise ValueError('Registered inventory counts changed')
    registration = json.loads((PHASE / 'registration_v1/public_registration.json').read_bytes())
    if (registration.get('public_registration_url') != EXPECTED_REGISTRATION
            or registration.get('frozen_git_commit') != EXPECTED_COMMIT
            or not registration.get('public_visibility_verified_at_utc')):
        raise ValueError('Public registration gate failed')
    execution = verify(tuple(range(665)))
    analysis_path = PHASE / 'validation/confirmatory_analysis_v1.json'
    analysis = json.loads(analysis_path.read_bytes())
    if (execution['matches'] != 166172 or execution['logical_scenario_results'] != 2622048
            or execution['errors'] or analysis['status'] != 'complete'
            or analysis['execution']['computational_matches'] != execution['matches']
            or analysis['execution']['logical_scenario_results'] != execution['logical_scenario_results']
            or len(analysis['scenario_sensitivity_all_16']) != 16):
        raise ValueError('Execution/analysis closure mismatch')

    sources = {}
    for row in inventory['files']:
        name = safe_name(row['path'])
        if name in sources:
            raise ValueError('Repeated frozen path: ' + name)
        source = BUNDLE / name
        if not source.is_file() or source.is_symlink():
            raise ValueError('Missing or linked frozen file: ' + name)
        sources[name] = (source, 'frozen')
    extras = [
        'phase3/registration_v1/public_registration.json',
        'phase3/verify_modal_wave_v1.py',
        'phase3/analyze_confirmatory_results_v1.py',
        'phase3/summarize_descriptives_v1.py',
        'phase3/ANALYSIS_CORRECTION_LOG_v1.md',
        'phase3/tests/test_confirmatory_reporting_v1.py',
        'phase3/validation/confirmatory_analysis_v1.json',
        'phase3/CONFIRMATORY_RESULTS_v1.md',
        'phase3/DESCRIPTIVE_RESULTS_v1.md',
        'phase3/MODAL_CONFIRMATORY_WAVE15_RESULTS_v1.md',
    ]
    extras.extend(f'phase3/validation/modal_confirmatory_batch_{i:04d}_receipt.json'
                  for i in range(665))
    for name in extras:
        safe_name(name)
        if name in sources:
            raise ValueError('Frozen/result path collision: ' + name)
        source = ROOT / name
        if not source.is_file() or source.is_symlink():
            raise ValueError('Missing result file: ' + name)
        sources[name] = (source, 'post_registration')
    if len(sources) != 1297 + len(extras):
        raise ValueError('Package file count mismatch')

    OUTDIR.mkdir(parents=True, exist_ok=True)
    rows = []
    with zipfile.ZipFile(ARCHIVE, mode='w', compression=zipfile.ZIP_DEFLATED,
                         compresslevel=6, allowZip64=True) as archive:
        for name in sorted(sources):
            source, role = sources[name]
            contents = source.read_bytes()
            item_sha = digest(contents)
            if role == 'frozen':
                row = next(r for r in inventory['files'] if r['path'] == name)
                if item_sha != row['sha256'] or len(contents) != row['bytes']:
                    raise ValueError('Frozen bundle differs from inventory: ' + name)
            rows.append({'path': name, 'bytes': len(contents), 'sha256': item_sha, 'role': role})
            archive.writestr(make_zipinfo(name), contents, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
        readme = README.encode('utf-8')
        rows.append({'path': 'README.md', 'bytes': len(readme), 'sha256': digest(readme), 'role': 'guide'})
        archive.writestr(make_zipinfo('README.md'), readme, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
        manifest = {
            'version': 1, 'name': 'EvoLLM Phase 3 confirmatory tournament replication package',
            'public_registration_url': EXPECTED_REGISTRATION,
            'frozen_git_commit': EXPECTED_COMMIT,
            'frozen_inventory_sha256': EXPECTED_INVENTORY_SHA,
            'frozen_files': 1297, 'batch_receipts': 665,
            'computational_matches': execution['matches'],
            'logical_scenario_results': execution['logical_scenario_results'],
            'files': sorted(rows, key=lambda x: x['path']),
        }
        manifest_bytes = (json.dumps(manifest, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')) + '\n').encode('utf-8')
        archive.writestr(make_zipinfo('MANIFEST.json'), manifest_bytes,
                         compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)

    with zipfile.ZipFile(ARCHIVE, mode='r') as archive:
        expected_names = {r['path'] for r in rows} | {'MANIFEST.json'}
        if set(archive.namelist()) != expected_names or len(archive.namelist()) != len(expected_names):
            raise ValueError('ZIP entries differ from manifest')
        if digest(archive.read('MANIFEST.json')) != digest(manifest_bytes):
            raise ValueError('ZIP manifest changed')
        for row in rows:
            contents = archive.read(row['path'])
            if digest(contents) != row['sha256'] or len(contents) != row['bytes']:
                raise ValueError('ZIP payload corruption: ' + row['path'])

    sidecar = {
        'zip': ARCHIVE.name, 'bytes': ARCHIVE.stat().st_size,
        'sha256': digest(ARCHIVE.read_bytes()), 'manifest_sha256': digest(manifest_bytes),
        'payload_files': len(rows), 'frozen_files': 1297, 'batch_receipts': 665,
        'validation': 'All archive members re-read and matched to SHA-256 manifest after ZIP creation.',
    }
    SIDECAR.write_text(json.dumps(sidecar, indent=2) + '\n', encoding='utf-8')
    return sidecar


if __name__ == '__main__':
    print(json.dumps(build(), indent=2))
