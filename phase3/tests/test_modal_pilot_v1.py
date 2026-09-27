import json
import pytest
from phase3.build_modal_bundle_v1 import ROOT,selected_files
from phase3.modal_pilot_core_v1 import jobs,check_baseline
from phase3.execute_uniform import load_field


def test_upload_is_research_allowlist():
    paths=selected_files()
    manifest=json.loads((ROOT/'phase3/validation/uniform_derived_candidates_v1.json').read_bytes())
    assert {x['source_path'].replace('\\','/') for x in manifest['candidates']} <= set(paths)
    assert all((ROOT/p).is_file() for p in paths)
    assert all(p.startswith('phase3/') for p in paths)
    assert not any(any(x in p.lower() for x in ['.env','receipt','response.bin','request.json','.git','modal.toml']) for p in paths)


def test_schedule_is_bounded_and_covers_four_alternatives():
    field=load_field(); tasks=jobs(field)
    assert len(tasks)<=32 and len(tasks)==len(set(tasks))
    alternatives=[x for x in tasks if x[0]==15]
    assert len(alternatives)==4
    for mask,a,b in alternatives: assert (0,a,b) in tasks
    assert all(a<=b for _,a,b in tasks)


def test_equivalence_rejects_any_changed_trace_or_missing_match():
    baseline={'scope':'diagnostic','results':[{'trace_sha256':'abc'}]}
    check_baseline(baseline,baseline)
    with pytest.raises(ValueError): check_baseline({'scope':'diagnostic','results':[]},baseline)
    with pytest.raises(ValueError): check_baseline({'scope':'diagnostic','results':[{'trace_sha256':'def'}]},baseline)
