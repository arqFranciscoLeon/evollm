"""Stage only the inventoried Phase 3 science and registration packet.

Never stages API receipts, cloud copies or unrelated worktree changes.
"""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
REG = ROOT / 'phase3/registration_v1'
INVENTORY = REG / 'freeze_inventory_v2.json'
EXTRA = (
    '.gitattributes',
    'phase3/registration_v1/freeze_inventory_v2.json',
    'phase3/registration_v1/OSF_SUBMISSION_DRAFT.md',
    'phase3/registration_v1/OSF_PHASE3_REGISTRATION_v1.zip',
    'phase3/registration_v1/build_osf_packet_v1.py',
    'phase3/registration_v1/stage_registration_v1.py',
)


def main():
    manifest = json.loads(INVENTORY.read_bytes())
    paths = [row['path'] for row in manifest['files']]
    for row in manifest['files']:
        if hashlib.sha256((ROOT / row['path']).read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('Scientific file differs from reviewed inventory: ' + row['path'])
    paths += EXTRA
    for path in EXTRA:
        if not (ROOT / path).is_file():
            raise ValueError('Missing registration artifact: ' + path)
    if len(paths) != len(set(paths)) or len(paths) != 1303:
        raise ValueError('Unexpected number of stage paths')
    git_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'],
                                       cwd=ROOT, text=True).strip()
    if Path(git_root).resolve() != ROOT.resolve():
        raise ValueError('Unexpected Git worktree root')
    pathspec = REG / 'stage_paths.nul'
    pathspec.write_bytes(b'\0'.join(path.encode('utf-8') for path in sorted(paths)) + b'\0')
    subprocess.run(['git', 'add', '-f', '--pathspec-from-file=' + str(pathspec),
                    '--pathspec-file-nul'], cwd=ROOT, check=True)
    # Existing index entries may still have been normalized by core.autocrlf
    # before .gitattributes took effect. Refresh all exact paths from raw bytes.
    subprocess.run(['git', 'add', '-f', '--renormalize',
                    '--pathspec-from-file=' + str(pathspec), '--pathspec-file-nul'],
                   cwd=ROOT, check=True)
    staged = subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z'], cwd=ROOT)
    actual = {value.decode('utf-8') for value in staged.split(b'\0') if value}
    if actual != set(paths):
        raise ValueError('Staged paths differ from exact registration allowlist')
    print(json.dumps({'staged_files': len(actual), 'scientific_bytes': manifest['total_bytes']}))


if __name__ == '__main__':
    main()
