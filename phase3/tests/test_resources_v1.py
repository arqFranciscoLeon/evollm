import json
from types import SimpleNamespace
from phase3.calibrate_resources_v1 import schedule
from phase3.runtime import ROOT, seed_for


def test_calibration_schedule_covers_population_without_outcomes():
    manifest=json.loads((ROOT/'phase3/validation/uniform_derived_candidates_v1.json').read_bytes())
    ids=[r['id'] for r in manifest['candidates']]
    rows=schedule(SimpleNamespace(players=dict.fromkeys(ids)))
    assert len(rows)==324
    assert sum(r['population_pairs'] for r in rows if r['kind']=='distinct')==163306
    assert sum(r['population_pairs'] for r in rows if r['kind']=='self')==572
    assert len({r['pair'] for r in rows})==324
    assert all((r['pair'][0]==r['pair'][1])==(r['kind']=='self') for r in rows)
    assert rows==schedule(SimpleNamespace(players=dict.fromkeys(reversed(ids))))


def test_fixed_configuration_and_integrity():
    import hashlib
    config=json.loads((ROOT/'phase3/inputs/execution_config_v1.json').read_bytes())
    assert config['repetitions']==1 and config['turns']==1000 and config['noise']==0
    assert config['scenario_masks']==list(range(16))
    assert config['matches_per_scenario']==163878
    assert config['total_matches']==2622048
    assert config['permutations']==10000
    assert config['status']=='prepared_pending_freeze_and_public_registration'
    for path,expected in config['dependencies'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected
    report=json.loads((ROOT/'phase3/validation/resources_calibration_v1.json').read_bytes())
    assert report['sources_audited']==576
    assert not report['forbidden_nondeterministic_access']
    assert len(report['seed_checks'])==8 and all(x['same'] for x in report['seed_checks'])
    assert seed_for(config['match_seed'],'a','b',0)==seed_for(20260913,'a','b',0)
