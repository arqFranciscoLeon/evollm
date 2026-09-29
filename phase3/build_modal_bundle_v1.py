"""Explicit research-only upload allowlist. Never copies credentials or API receipts."""
import hashlib
import json
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'phase3/cloud_bundle_v2'


def selected_files():
    manifest=json.loads((ROOT/'phase3/validation/uniform_derived_candidates_v1.json').read_bytes())
    plan=json.loads((ROOT/'phase3/inputs/sensitivity_plan_v1.json').read_bytes())
    modules=['execute_uniform','runtime','uniform_semantics_v3b','validate_pilot','pilot_converter',
             'review_semantics','interpretation_sensitivity_v1','modal_pilot_core_v1']
    paths={f'phase3/{name}.py' for name in modules}
    paths.update(plan['dependencies'])
    paths.update(row['source_path'] for row in manifest['candidates'])
    paths.update(row['source_path'] for row in plan['alternatives'])
    paths.update(['phase3/inputs/sensitivity_plan_v1.json','phase3/requirements-validation.lock.txt',
                  'phase3/validation/uniform_derived_candidates_v1.json','phase3/validation/uniform_v3b.json',
                  'phase3/validation/uniform_corrections_v1.json','phase3/validation/modal_pilot_local_v1.json'])
    for path in paths:
        resolved=(ROOT/path).resolve()
        if not resolved.is_relative_to(ROOT/'phase3') or resolved.suffix not in ('.py','.json','.txt'):
            raise ValueError('Outside research allowlist: '+path)
        if any(s in path.lower() for s in ('.env','receipt','request.json','response.bin','token','secret')):
            raise ValueError('Forbidden upload: '+path)
    return sorted({p.replace('\\','/') for p in paths})


def main():
    if DEST.exists(): raise ValueError('Bundle already exists; do not overwrite')
    entries=[]
    for name in selected_files():
        raw=(ROOT/name).read_bytes(); path=DEST/name
        path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(raw)
        entries.append({'path':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    inventory={'destination':'Modal workspace unimayor-evollm','scope':'32-or-fewer diagnostic matches only',
               'excludes':'Credentials, API request/response payloads, Git repository, unrelated files',
               'files':entries,'total_bytes':sum(x['bytes'] for x in entries)}
    (DEST/'BUNDLE_INVENTORY.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
    print(json.dumps({'files':len(entries),'bytes':inventory['total_bytes']}))


if __name__=='__main__': main()
