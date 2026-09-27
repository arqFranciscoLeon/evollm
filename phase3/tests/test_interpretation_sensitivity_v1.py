import json
import numpy as np
import pytest
from phase3.execute_uniform import load_field, run, export_matrices
from phase3.interpretation_sensitivity_v1 import load_scenario, PLAN
from phase3.sensitivity_analysis_v1 import duplicate_sensitivity, exclusion_bounds
from phase3.analyze_phase3 import h7_statistic


@pytest.fixture(scope='module')
def primary(): return load_field()


def test_all_scenarios_keep_ids_and_change_exact_sources(primary):
    plan=json.loads(PLAN.read_bytes())
    targets=[row['id'] for row in plan['alternatives']]
    for mask in range(16):
        field=load_scenario(mask,primary)
        changed={sid for sid in primary.records if primary.records[sid]['source_sha256']!=field.records[sid]['source_sha256']}
        assert changed=={sid for bit,sid in enumerate(targets) if mask & (1<<bit)}
        assert set(field.players)==set(primary.players)
    assert load_scenario(0,primary) is primary


def test_actual_panel_synthetic_matrix(primary):
    ids=sorted(primary.records); models=[x.split('/')[0] for x in ids]
    attitudes=[x.split('/')[-1].split('_')[0] for x in ids]
    plan=json.loads(PLAN.read_bytes()); groups=[plan['syntax_groups'][x] for x in ids]
    matrix=np.full((572,572),0.4)
    weighted=duplicate_sensitivity(matrix,models,attitudes,groups)
    assert weighted['difference']==pytest.approx(0,abs=1e-12)
    assert len(set(groups))==130
    bounds=exclusion_bounds(matrix,models,attitudes)
    assert bounds['missing_identities']==28
    assert bounds['lower'] <= h7_statistic(matrix,models,attitudes) <= bounds['upper']


def test_invalid_mask(primary):
    for mask in [-1,16,True,'3']:
        with pytest.raises(ValueError): load_scenario(mask,primary)


def test_scenario_checkpoint_separation(tmp_path,primary):
    alternative=load_scenario(15,primary)
    targets=[row['id'] for row in json.loads(PLAN.read_bytes())['alternatives']]
    pairs=[(sid,sid) for sid in targets]
    path=tmp_path/'alternative.sqlite'
    first=run(path,alternative,repetitions=1,turns=20,pairs=pairs,max_new=1)
    assert first['new_matches']==1
    second=run(path,alternative,repetitions=1,turns=20,pairs=pairs)
    assert second['new_matches']==3 and second['complete']
    assert run(path,alternative,repetitions=1,turns=20,pairs=pairs)['new_matches']==0
    with pytest.raises(ValueError,match='configuration changed'):
        run(path,primary,repetitions=1,turns=20,pairs=pairs)
    with pytest.raises(ValueError,match='Diagnostics'):
        export_matrices(path,alternative)
