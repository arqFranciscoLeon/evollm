import hashlib
import pytest
import axelrod as axl
from phase3.uniform_semantics_v3b import compile_candidate
from phase3.validate_uniform_v3b import replay, WesternReference


def compiled(body):
    source = 'def strategy(self, opponent: axl.player.Player) -> axl.Action:\n' + body
    return compile_candidate(source, hashlib.sha256(source.encode()).hexdigest())


def test_scores_are_updated_exactly_once_and_reset_per_player():
    cls = compiled('    return axl.Action.C if self.score == 5 else axl.Action.D\n')
    a, b = cls(), axl.Cooperator()
    assert a.strategy(b) == axl.Action.D
    a.update_history(axl.Action.D, axl.Action.C)
    b.update_history(axl.Action.C, axl.Action.D)
    assert a.strategy(b) == a.strategy(b) == axl.Action.C
    assert cls().strategy(axl.Cooperator()) == axl.Action.D


def test_private_latch_survives_chronological_replay():
    cls = compiled('    if self.first_round():\n        self._punish_forever = False\n        return axl.Action.C\n'
        '    if opponent.history[-1] == axl.Action.D:\n        self._punish_forever = True\n'
        '    return axl.Action.D if self._punish_forever else axl.Action.C\n')
    a, b = cls(), axl.Cooperator()
    assert a.strategy(b) == axl.Action.C
    a.update_history(axl.Action.C, axl.Action.D)
    b.update_history(axl.Action.D, axl.Action.C)
    assert a.strategy(b) == axl.Action.D
    a.update_history(axl.Action.D, axl.Action.C)
    b.update_history(axl.Action.C, axl.Action.D)
    assert a.strategy(b) == axl.Action.D


def test_replay_keeps_full_trace_after_first_mismatch():
    cls = compiled('    return axl.Action.D\n')
    result = replay(cls, lambda: WesternReference('tft'), 'CCC', 'CCC')
    assert result['checks'] == 4
    assert len(result['failures']) == 1
    assert result['actions_sha256'] == hashlib.sha256(b'DDDD').hexdigest()


@pytest.mark.parametrize('body', [
    '    self.history = []\n    return axl.Action.C\n',
    '    self._random = None\n    return axl.Action.C\n',
    '    return open(1)\n',
    '    import os\n    return axl.Action.C\n'])
def test_unreviewed_runtime_mutation_and_calls_rejected(body):
    with pytest.raises(ValueError):
        compiled(body)


def test_hash_mismatch_rejected():
    with pytest.raises(ValueError, match='inspected'):
        compile_candidate('def strategy(self, opponent): return 1', '0' * 64)


def test_runtime_error_is_preserved_at_its_round():
    cls = compiled('    if self.first_round():\n        return axl.Action.C\n    return sum((1, 2))[0]\n')
    result = replay(cls, lambda: WesternReference('tft'), 'C', 'C')
    assert result['checks'] == 1
    assert result['error_round'] == 2
    assert 'TypeError' in result['error']
