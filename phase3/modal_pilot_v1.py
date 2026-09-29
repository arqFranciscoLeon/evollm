"""Run only after the workspace credit/spend limits are verified. No full-tournament entrypoint."""
from pathlib import Path
import json
import modal

ROOT=Path(__file__).resolve().parents[1]
BUNDLE=ROOT/'phase3/cloud_bundle_v2'
if modal.is_local():
    # Check before constructing/building the remote image, which can itself incur usage.
    gate_path=ROOT/'phase3/inputs/modal_billing_verified_v1.json'
    if not gate_path.exists():
        raise RuntimeError('Verify workspace credits and zero out-of-pocket spend limit before launch')
    gate=json.loads(gate_path.read_bytes())
    if (gate.get('workspace')!='unimayor-evollm' or gate.get('spend_limit_usd')!=0
            or gate.get('usage_limit_usd')!=30 or gate.get('remaining_credits_usd',0)<1
            or gate.get('project_authorized_usd')!=30):
        raise RuntimeError('Billing verification does not satisfy the authorized credit-only budget')
    image=(modal.Image.from_registry('python:3.12.14-slim-bookworm')
           .pip_install('torch==2.14.0',index_url='https://download.pytorch.org/whl/cpu')
           .pip_install_from_requirements(str(BUNDLE/'phase3/requirements-validation.lock.txt'))
           .env({'PYTHONPATH':'/opt/evollm','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1'})
           .add_local_dir(BUNDLE,remote_path='/opt/evollm'))
else:
    image=modal.Image.debian_slim()
app=modal.App('evollm-phase3-diagnostic-v1',image=image)
volume=modal.Volume.from_name('evollm-phase3-diagnostics-v1',create_if_missing=True)


@app.function(cpu=(1,1),memory=(1024,2048),timeout=600,retries=0,max_containers=1,
              volumes={'/results':volume})
def diagnostic():
    import hashlib,json,sys
    sys.path.insert(0,'/opt/evollm')
    from phase3.modal_pilot_core_v1 import run_diagnostic,check_baseline
    base=Path('/opt/evollm')
    inventory=json.loads((base/'BUNDLE_INVENTORY.json').read_bytes())
    signature=hashlib.sha256((base/'BUNDLE_INVENTORY.json').read_bytes()).hexdigest()
    saved=Path('/results')/(signature+'.json')
    if saved.exists(): return json.loads(saved.read_bytes())
    for row in inventory['files']:
        if hashlib.sha256((base/row['path']).read_bytes()).hexdigest()!=row['sha256']:
            raise ValueError('Bundle changed: '+row['path'])
    # Preserve the frozen Windows manifest literally. POSIX permits backslashes
    # in a filename: create verified local aliases for its ten historical paths.
    manifest=json.loads((base/'phase3/validation/uniform_derived_candidates_v1.json').read_bytes())
    for row in manifest['candidates']:
        name=row['source_path']
        if '\\' in name:
            raw=(base/name.replace('\\','/')).read_bytes()
            if hashlib.sha256(raw).hexdigest()!=row['source_sha256']:
                raise ValueError('Portable alias source changed')
            alias=base/name
            if alias.parent!=base: raise ValueError('Unexpected alias path')
            alias.write_bytes(raw)
    result=run_diagnostic()
    check_baseline(result,json.loads((base/'phase3/validation/modal_pilot_local_v1.json').read_bytes()))
    result['bundle_sha256']=signature; result['local_linux_equivalence_passed']=True
    temporary=saved.with_suffix('.tmp'); temporary.write_text(json.dumps(result,indent=2))
    temporary.replace(saved); volume.commit()
    return result


@app.local_entrypoint()
def main():
    import json
    output=ROOT/'phase3/validation/modal_pilot_remote_v1.json'
    if output.exists(): raise ValueError('Remote result already saved; do not repeat')
    result=diagnostic.remote()
    with output.open('x',encoding='utf-8') as out: json.dump(result,out,indent=2)
    print(json.dumps({'matches':len(result['results']),'equivalent':result['local_linux_equivalence_passed'],
                      'seconds':result['elapsed_seconds']}))
