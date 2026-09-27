"""Fault-injection tests: no network, no generated strategy execution."""
import json
import pytest
from phase3 import pilot_converter as pc


def response(finish='stop', content='def strategy(self, opponent):\n    return axl.Action.C\n', model=pc.MODEL):
    return pc.encoded({'model': model, 'id': 'simulated', 'usage': {'prompt_tokens': 100, 'completion_tokens': 20},
                       'choices': [{'finish_reason': finish, 'message': {'content': content}}]})


@pytest.fixture
def prepared(tmp_path):
    plan = tmp_path/'plan.json'
    pc.prepare(plan)
    return plan, tmp_path/'run'


@pytest.mark.parametrize('body,status', [
    (response('length'), 'incomplete_or_nonstandard_finish'),
    (response(content=''), 'empty_content'),
    (response(content='UNCONVERTIBLE: missing branch'), 'model_reports_unconvertible'),
    (response(model='another-model'), 'unexpected_model'),
    (response(content='```python\ndef strategy(self, opponent): pass\n```'), 'invalid_response_or_syntax'),
    (response(content='import os\ndef strategy(self, opponent): pass'), 'invalid_code_shape'),
    (pc.encoded({'model': pc.MODEL}), 'missing_usage'),
])
def test_rejects_incomplete_and_untraceable_outputs(body, status):
    assert pc.assess(body) == status


def test_resume_never_duplicates_successful_calls(prepared):
    plan, directory = prepared
    calls = []
    def send(payload, key):
        calls.append(payload)
        return 200, response(), 'mock-request'
    first = pc.run(plan, directory, send, 'test-key-not-in-body')
    second = pc.run(plan, directory, send, 'test-key-not-in-body')
    assert len(calls) == 12 and first == second
    assert first['reserved_micro_usd'] <= pc.BUDGET_MICRO_USD
    assert (directory/'01/response.bin').read_bytes() == response()
    assert (directory/'01/candidate.py.txt').is_file()


def test_uncertain_transport_stops_and_remains_reserved(prepared):
    plan, directory = prepared
    calls = []
    def send(payload, key):
        calls.append(1)
        raise TimeoutError('Do not log this secret '+key)
    with pytest.raises(RuntimeError, match='Transport failed'):
        pc.run(plan, directory, send, 'private-test-key')
    with pytest.raises(RuntimeError, match='Unresolved attempt'):
        pc.run(plan, directory, send, 'private-test-key')
    assert calls == [1]
    assert 'private-test-key' not in (directory/'01/transport_error.json').read_text()


def test_truncation_archived_without_retry(prepared):
    plan, directory = prepared
    calls = []
    def send(payload, key):
        calls.append(1)
        return 200, response('length'), None
    with pytest.raises(RuntimeError, match='incomplete'):
        pc.run(plan, directory, send, 'test-key-not-in-body')
    assert (directory/'01/response.bin').is_file()
    assert not (directory/'01/candidate.py.txt').exists()
    with pytest.raises(RuntimeError, match='Previous non-success'):
        pc.run(plan, directory, send, 'test-key-not-in-body')
    assert calls == [1]


def test_modified_prompt_is_rejected_even_if_its_hash_is_updated(prepared):
    plan, directory = prepared
    data = json.loads(plan.read_bytes())
    item = data['requests'][0]
    item['payload']['messages'][0]['content'] = 'Change the strategy'
    item['payload_sha256'] = pc.sha(pc.encoded(item['payload']))
    plan.write_bytes(pc.encoded(data))
    with pytest.raises(ValueError, match='Plan differs'):
        pc.run(plan, directory, lambda *a: pytest.fail('Network must not run'), 'fake')


def test_lock_blocks_concurrent_run(prepared):
    plan, directory = prepared
    directory.mkdir()
    (directory/'running.lock').write_text('occupied')
    with pytest.raises(FileExistsError):
        pc.run(plan, directory, lambda *a: pytest.fail('Network must not run'), 'fake')


def test_budget_blocks_before_network(prepared, monkeypatch):
    plan, directory = prepared
    monkeypatch.setattr(pc, 'BUDGET_MICRO_USD', pc.RESERVE_MICRO_USD-1)
    plan.unlink()
    pc.prepare(plan)
    with pytest.raises(RuntimeError, match='Budget reservation'):
        pc.run(plan, directory, lambda *a: pytest.fail('Network must not run'), 'fake')
