"""Build an offline, hash-checked copy of the frozen scientific package.

This command does not contact Modal or execute matches. The public OSF gate is
deliberately excluded and must be supplied only after independent verification.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / 'phase3'
INVENTORY = PHASE / 'registration_v1/freeze_inventory_v2.json'
DEST = PHASE / 'cloud_bundle_confirmatory_v1'
EXPECTED_INVENTORY_SHA256 = '27ee8121f14ccb7d5cd7fb5838c224ad8e7207010fdc92335f52e4a2acfcebf4'
EXPECTED_CONTEXT_SHA256 = '3811e2f65857b46003a48ddedbc0f625c1a9e573207987787f7a5f78b01d1bfd'
EXPECTED_MANIFEST_SHA256 = '2dbcfc56965bd025ca2f4eb9ca2351099f5fd34101fbbd7af82fee9a43bb3ba6'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def checked_files():
    raw = INVENTORY.read_bytes()
    if digest(raw) != EXPECTED_INVENTORY_SHA256:
        raise ValueError('Frozen inventory changed')
    inventory = json.loads(raw)
    rows = inventory['files']
    if (len(rows) != 1297 or inventory['total_files'] != 1297
            or inventory['total_bytes'] != 100433684):
        raise ValueError('Unexpected frozen inventory size')
    names = [row['path'] for row in rows]
    if len(names) != len(set(names)):
        raise ValueError('Duplicate source path')
    verified = []
    for row in rows:
        name = row['path']
        relative = Path(name)
        if (relative.is_absolute() or relative.parts[0] != 'phase3'
                or '..' in relative.parts or '\\' in name):
            raise ValueError('Unsafe source path: ' + name)
        source = ROOT / relative
        if not source.is_file() or source.is_symlink():
            raise ValueError('Missing or linked source: ' + name)
        contents = source.read_bytes()
        if len(contents) != row['bytes'] or digest(contents) != row['sha256']:
            raise ValueError('Frozen source changed: ' + name)
        verified.append((name, contents))
    plan = PHASE / 'reuse_plan_v1'
    if (digest((plan / 'manifest.json').read_bytes()) != EXPECTED_MANIFEST_SHA256
            or json.loads((plan / 'manifest.json').read_bytes())['context_sha256'] != EXPECTED_CONTEXT_SHA256):
        raise ValueError('Frozen plan changed')
    return verified


def build():
    if DEST.exists():
        raise ValueError('Bundle exists; inspect it rather than overwrite it')
    files = checked_files()  # Finish all source checks before creating output.
    DEST.mkdir()
    for name, contents in files:
        target = DEST / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents)
    declaration = {
        'scope': 'frozen scientific package; no execution authorization',
        'destination': 'Modal workspace unimayor-evollm, only after public OSF gate',
        'freeze_inventory_sha256': EXPECTED_INVENTORY_SHA256,
        'plan_context_sha256': EXPECTED_CONTEXT_SHA256,
        'plan_manifest_sha256': EXPECTED_MANIFEST_SHA256,
        'files': len(files),
        'bytes': sum(len(contents) for _, contents in files),
        'excludes': 'credentials, API receipts, public-registration gate, live results',
    }
    (DEST / 'BUNDLE_DECLARATION.json').write_text(json.dumps(declaration, indent=2), encoding='utf-8')
    return declaration


if __name__ == '__main__':
    print(json.dumps(build(), indent=2))
