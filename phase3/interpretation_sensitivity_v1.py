"""Load one of 16 prespecified fields using the unchanged common executor."""
import json
from pathlib import Path
from phase3.execute_uniform import Field, MANIFEST_SHA256, digest, load_field
from phase3.runtime import ROOT
from phase3.uniform_semantics_v3b import compile_candidate

PLAN = ROOT / 'phase3/inputs/sensitivity_plan_v1.json'


def load_scenario(mask, primary=None):
    if type(mask) is not int or not 0 <= mask < 16:
        raise ValueError('Scenario mask must be 0..15')
    field = load_field() if primary is None else primary
    if field.provenance['manifest_sha256'] != MANIFEST_SHA256:
        raise ValueError('Wrong primary manifest')
    data = PLAN.read_bytes()
    plan = json.loads(data)
    if plan['primary_manifest_sha256'] != MANIFEST_SHA256:
        raise ValueError('Plan references another primary field')
    for path, expected in plan['dependencies'].items():
        if digest((ROOT/path).read_bytes()) != expected:
            raise ValueError('Sensitivity dependency changed: '+path)
    if mask == 0:
        return field
    records = {sid: dict(row) for sid,row in field.records.items()}
    players = dict(field.players)
    for bit, item in enumerate(plan['alternatives']):
        if mask & (1 << bit):
            sid = item['id']; source = (ROOT/item['source_path']).read_bytes()
            if digest(source) != item['source_sha256']:
                raise ValueError('Alternative source changed: '+sid)
            players[sid] = compile_candidate(source.decode(),item['source_sha256'])
            records[sid].update(source_path=item['source_path'], source_sha256=item['source_sha256'],
                                provenance='local_interpretation_sensitivity')
    provenance = dict(field.provenance)
    provenance['sensitivity'] = {'mask':mask, 'plan_sha256':digest(data),
                                'loader_sha256':digest(Path(__file__).read_bytes())}
    return Field(players, records, provenance)
