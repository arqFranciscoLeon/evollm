"""Build a small deterministic protocol attachment for OSF; no upload."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'phase3/registration_v1/OSF_PHASE3_REGISTRATION_v1.zip'
NAMES = (
    'phase3/PHASE3_PROTOCOL_v1.md',
    'phase3/inputs/execution_config_v3.json',
    'phase3/reuse_plan_v1/context.json',
    'phase3/reuse_plan_v1/manifest.json',
    'phase3/registration_v1/freeze_inventory_v2.json',
)


def main():
    if OUT.exists():
        raise ValueError('OSF packet already exists; version instead of overwriting')
    inventory = json.loads((ROOT / NAMES[-1]).read_bytes())
    known = {row['path']: row['sha256'] for row in inventory['files']}
    for name in NAMES[:-1]:
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != known[name]:
            raise ValueError('Protocol attachment differs from freeze inventory: ' + name)
    with zipfile.ZipFile(OUT, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(NAMES):
            entry = zipfile.ZipInfo(name, date_time=(2026, 9, 27, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o644 << 16
            archive.writestr(entry, (ROOT / name).read_bytes(), compress_type=zipfile.ZIP_DEFLATED,
                             compresslevel=9)
    with zipfile.ZipFile(OUT) as archive:
        if sorted(archive.namelist()) != sorted(NAMES):
            raise ValueError('Wrong packet contents')
        for name in NAMES:
            if archive.read(name) != (ROOT / name).read_bytes():
                raise ValueError('Packet differs from source: ' + name)
    print(json.dumps({'files': len(NAMES), 'bytes': OUT.stat().st_size,
                      'sha256': hashlib.sha256(OUT.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
