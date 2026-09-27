import pytest
from phase3.validate_pilot import compile_reviewed, check_vector


def test_endgame_mutation_is_detected():
    case = {'case': 'TFT final C', 'round': 1000, 'own_rle': [['C',999]],
            'opponent_rle': [['C',999]], 'expected_action': 'C'}
    source = 'def strategy(self, opponent):\n    if self.first_round(): return axl.Action.C\n    return opponent.history[-1]\n'
    mutant = source.replace('    return opponent', '    if len(self.history) == 999: return axl.Action.D\n    return opponent')
    assert check_vector(compile_reviewed(source), case)['pass']
    assert not check_vector(compile_reviewed(mutant), case)['pass']


@pytest.mark.parametrize('source', [
    'def strategy(self, opponent):\n    while True: pass',
    'def strategy(self, opponent):\n    return open("file")',
    'def strategy(self, opponent):\n    opponent.history.clear()\n    return axl.Action.D',
    'def strategy(self, opponent):\n    self.history = []\n    return axl.Action.D',
])
def test_unreviewed_code_is_rejected(source):
    with pytest.raises(ValueError):
        compile_reviewed(source)
