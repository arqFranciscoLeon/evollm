import json
import sqlite3

import axelrod as axl
import numpy as np
import pytest

from phase3 import execute_uniform as executor
from phase3.uniform_semantics_v3b import compile_candidate
from phase3.runtime import play_pair


def fixture_field():
    players = {'a/default/Cooperative_1': axl.Cooperator,
               'b/default/Aggressive_1': axl.Defector,
               'c/default/Neutral_1': axl.Random}
    return executor.Field(players, {sid: {'source_sha256': cls.__name__} for sid, cls in players.items()},
                          {'kind': 'synthetic_fixture'})


def stored(path):
    with sqlite3.connect(path) as db:
        return db.execute('SELECT * FROM matches ORDER BY id_i,id_j,repetition').fetchall()


def test_checkpoint_resume_matches_uninterrupted_execution_and_export(tmp_path):
    field = fixture_field()
    resumed, fresh = tmp_path / 'resumed.sqlite', tmp_path / 'fresh.sqlite'
    first = executor.run(resumed, field, repetitions=2, turns=20, max_new=3)
    assert first['new_matches'] == first['completed_matches'] == 3
    assert not first['complete']
    with pytest.raises(ValueError, match='Incomplete'):
        executor.export_matrices(resumed, field)
    second = executor.run(resumed, field, repetitions=2, turns=20)
    assert second['new_matches'] == 9 and second['complete']
    assert executor.run(resumed, field, repetitions=2, turns=20)['new_matches'] == 0
    executor.run(fresh, field, repetitions=2, turns=20)
    assert stored(resumed) == stored(fresh)
    matrix = executor.export_matrices(resumed, field)
    assert matrix['cooperation'][0, 0] == 1
    assert matrix['cooperation'][0, 1] == 0
    assert matrix['payoff'][0, 1] == 0 and matrix['payoff'][1, 0] == 5
    np.testing.assert_array_equal(matrix['cooperation'], matrix['cooperation'].T)


def test_configuration_change_and_source_identity_change_rejected(tmp_path):
    field = fixture_field()
    path = tmp_path / 'run.sqlite'
    executor.run(path, field, repetitions=1, turns=10, max_new=1)
    before = stored(path)
    with pytest.raises(ValueError, match='configuration changed'):
        executor.run(path, field, repetitions=2, turns=10)
    sid = next(iter(field.records))
    field.records[sid]['source_sha256'] = 'changed'
    with pytest.raises(ValueError, match='configuration changed'):
        executor.run(path, field, repetitions=1, turns=10)
    assert stored(path) == before


def test_same_class_keeps_distinct_full_ids_and_self_pairs(tmp_path):
    players = {f'{model}/default/Cooperative_1': axl.Cooperator for model in ('one', 'two')}
    field = executor.Field(players, {sid: {'source_sha256': 'same'} for sid in players}, {})
    path = tmp_path / 'ids.sqlite'
    result = executor.run(path, field, repetitions=1, turns=10)
    assert result['completed_matches'] == 3
    rows = stored(path)
    assert sum(i == j for i, j, *_ in rows) == 2
    assert len(executor.export_matrices(path, field)['ids']) == 2


def test_failure_is_persisted_blocks_resume_and_never_becomes_a_move(tmp_path):
    class Broken(axl.Player):
        def strategy(self, opponent):
            return None
    field = executor.Field({'broken/default/Neutral_1': Broken},
                           {'broken/default/Neutral_1': {'source_sha256': 'broken'}}, {})
    path = tmp_path / 'failed.sqlite'
    result = executor.run(path, field, repetitions=1, turns=10)
    assert result['blocked'] and result['failed_matches'] == 1
    assert result['completed_matches'] == 0
    assert executor.run(path, field, repetitions=1, turns=10)['new_matches'] == 0
    assert len(stored(path)) == 1 and stored(path)[0][4] == 'error'
    with pytest.raises(ValueError, match='failed match'):
        executor.export_matrices(path, field)


def test_diagnostics_are_not_exportable_as_confirmatory_results(tmp_path):
    field = fixture_field()
    pairs = executor.diagnostic_pairs(field)
    assert set(s for pair in pairs for s in pair) == set(field.players)
    path = tmp_path / 'diagnostic.sqlite'
    result = executor.run(path, field, repetitions=1, turns=10, pairs=pairs)
    assert result['complete']
    with pytest.raises(ValueError, match='Diagnostics'):
        executor.export_matrices(path, field)
    with pytest.raises(ValueError, match='configuration changed'):
        executor.run(path, field, repetitions=1, turns=10)


def test_persisted_inconsistent_payoffs_are_rejected(tmp_path):
    field = fixture_field()
    path = tmp_path / 'tampered.sqlite'
    executor.run(path, field, repetitions=1, turns=10)
    with sqlite3.connect(path) as db:
        row = db.execute('SELECT rowid,payload FROM matches LIMIT 1').fetchone()
        payload = json.loads(row[1])
        payload['payoff_i'] = -99
        db.execute('UPDATE matches SET payload=? WHERE rowid=?', (json.dumps(payload), row[0]))
    with pytest.raises(ValueError, match='payoff/count mismatch'):
        executor.export_matrices(path, field)


def test_both_generated_players_receive_completed_scores_and_fresh_state():
    first = '''def strategy(self, opponent: axl.player.Player) -> axl.Action:
    if self.first_round():
        self.calls = 0
    self.calls += 1
    if self.score == 5 * len(self.history) and opponent.score == 0 and self.calls == len(self.history) + 1:
        return axl.Action.D
    return axl.Action.C
'''
    second = '''def strategy(self, opponent: axl.player.Player) -> axl.Action:
    if self.score == 0 and opponent.score == 5 * len(self.history):
        return axl.Action.C
    return axl.Action.D
'''
    a = compile_candidate(first, executor.digest(first.encode()))
    b = compile_candidate(second, executor.digest(second.encode()))
    for _ in range(2):
        assert play_pair(a, b, 1000, 7) == {'CC': 0, 'CD': 0, 'DC': 1000, 'DD': 0,
                                         'payoff_i': 5, 'payoff_j': 0}
        assert play_pair(b, a, 1000, 7) == {'CC': 0, 'CD': 1000, 'DC': 0, 'DD': 0,
                                         'payoff_i': 0, 'payoff_j': 5}


def test_changed_manifest_rejected_before_compilation(tmp_path, monkeypatch):
    path = tmp_path / 'manifest.json'
    path.write_text('{}', encoding='utf-8')
    monkeypatch.setattr(executor, 'MANIFEST', path)
    with pytest.raises(ValueError, match='manifest changed'):
        executor.load_field()


def test_default_cli_only_preflights(monkeypatch, capsys):
    monkeypatch.setattr(executor, 'load_field', fixture_field)
    monkeypatch.setattr('sys.argv', ['execute_uniform'])
    executor.main()
    assert json.loads(capsys.readouterr().out)['preflight'] == 'passed'


def test_complete_synthetic_schedule_exports_directly_to_h7(tmp_path):
    from phase3.analyze_phase3 import h7_statistic
    players = {f'{model}/default/{attitude}_{i}': cls
               for model, cls in (('one', axl.Cooperator), ('two', axl.Defector))
               for attitude in ('Aggressive', 'Cooperative', 'Neutral') for i in (1, 2)}
    field = executor.Field(players, {sid: {'source_sha256': cls.__name__}
                                    for sid, cls in players.items()}, {'kind': 'synthetic_fixture'})
    path = tmp_path / 'h7.sqlite'
    assert executor.run(path, field, repetitions=2, turns=10)['completed_matches'] == 156
    result = executor.export_matrices(path, field)
    # Within means are 1 and 0 for the two models; between is 0 in every stratum.
    assert h7_statistic(result['cooperation'], result['models'], result['attitudes']) == pytest.approx(.5)
