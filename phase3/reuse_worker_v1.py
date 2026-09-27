"""Batch worker for separate processes/containers; no implicit remote launch."""
import json
import platform
from pathlib import Path
from phase3.execute_uniform import load_field, digest, MANIFEST_SHA256, MANIFEST
from phase3.interpretation_sensitivity_v1 import load_scenario, PLAN
from phase3.reuse_batches_v1 import execute_batch, save_receipt, sha
from phase3.runtime import ROOT

_cached_signature=None
_cached_resolver=None


def verified_resolver(context):
    global _cached_signature,_cached_resolver
    provenance=context['provenance']
    if provenance['target_system']!=platform.system(): raise ValueError('Wrong execution operating system')
    if context['implementation_sha256']!=digest((ROOT/'phase3/reuse_batches_v1.py').read_bytes()):
        raise ValueError('Reuse implementation changed')
    if provenance['reuse_worker_sha256']!=digest(Path(__file__).read_bytes()): raise ValueError('Worker changed')
    if provenance['sensitivity_plan_sha256']!=digest(PLAN.read_bytes()): raise ValueError('Sensitivity plan changed')
    signature=sha(context)
    if signature==_cached_signature: return _cached_resolver
    # Compatibility aliases preserve the literal frozen Windows manifest on Linux.
    raw_manifest=MANIFEST.read_bytes()
    if digest(raw_manifest)!=MANIFEST_SHA256: raise ValueError('Primary manifest changed')
    if platform.system()=='Linux':
        for row in json.loads(raw_manifest)['candidates']:
            name=row['source_path']
            if '\\' in name:
                raw=(ROOT/name.replace('\\','/')).read_bytes(); alias=ROOT/name
                if digest(raw)!=row['source_sha256'] or alias.parent!=ROOT:
                    raise ValueError('Invalid compatibility alias')
                if alias.exists():
                    if alias.read_bytes()!=raw: raise ValueError('Alias differs from reviewed source')
                else:
                    import tempfile,os
                    with tempfile.NamedTemporaryFile(dir=ROOT,delete=False) as stream:
                        stream.write(raw); stream.flush(); os.fsync(stream.fileno()); temporary=Path(stream.name)
                    temporary.replace(alias)  # Atomic even when two workers prepare identical aliases.
    primary=load_field()
    if primary.provenance!=provenance['field']: raise ValueError('Runtime provenance differs')
    players={}
    for mask,sources in context['scenario_sources'].items():
        field=load_scenario(int(mask),primary)
        actual={sid:row['source_sha256'] for sid,row in field.records.items()}
        if actual!=sources: raise ValueError('Scenario source identity mismatch')
        for sid,source in actual.items(): players[(sid,source)]=field.players[sid]
    _cached_signature=signature
    _cached_resolver=lambda sid,source:players[(sid,source)]
    return _cached_resolver


def run_owned_batch(context_path,batch_path,result_path,registration_path):
    """A coordinator owns each result path exclusively; no shared cloud SQLite.

    Remote storage commit is a separate coordinator responsibility. Interrupted
    uncommitted matches may be recomputed; exactly-once billing is not claimed.
    """
    context=json.loads(Path(context_path).read_bytes())
    registration=json.loads(Path(registration_path).read_bytes())
    if (registration.get('context_sha256')!=sha(context) or not registration.get('public_registration_url')
            or not registration.get('frozen_git_commit')):
        raise ValueError('Matching frozen/public registration record required')
    batch=json.loads(Path(batch_path).read_bytes()); destination=Path(result_path)
    previous=json.loads(destination.read_bytes()) if destination.exists() else None
    resolve=verified_resolver(context)
    return execute_batch(batch,context,resolve,previous=previous,
                         checkpoint=lambda receipt:save_receipt(destination,receipt))
