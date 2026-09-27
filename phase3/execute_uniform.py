"""Identity-safe execution of the validated uniform field; offline preflight by default.

Diagnostics are separate from the confirmatory schedule. No API is called here.
"""
import argparse
from dataclasses import dataclass
import hashlib
import itertools
import json
from pathlib import Path
import platform
import sqlite3
import time

import axelrod as axl
import numpy as np
from phase3.runtime import ROOT, play_pair, seed_for
from phase3.uniform_semantics_v3b import compile_candidate

MANIFEST = ROOT / 'phase3/validation/uniform_derived_candidates_v1.json'
MANIFEST_SHA256 = 'd5725c7a63125a0cbdee1ddc24e4d2731dc60f6ad0734d3c670d5b23f9181062'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


@dataclass
class Field:
    players: dict
    records: dict
    provenance: dict


def load_field():
    data = MANIFEST.read_bytes()
    if digest(data) != MANIFEST_SHA256:
        raise ValueError('Validated field manifest changed')
    manifest = json.loads(data)
    for path, key in (('uniform_v3b.json', 'raw_validation_sha256'),
                      ('uniform_corrections_v1.json', 'correction_validation_sha256')):
        if digest((ROOT / 'phase3/validation' / path).read_bytes()) != manifest[key]:
            raise ValueError('Field validation changed: ' + path)
    raw = json.loads((ROOT / 'phase3/validation/uniform_v3b.json').read_bytes())
    if raw['python'] != platform.python_version() or raw['axelrod'] != axl.__version__:
        raise ValueError('Runtime version differs from validated environment')
    for name in ('runtime.py', 'uniform_semantics_v3b.py'):
        if digest((ROOT / 'phase3' / name).read_bytes()) != raw['dependencies'][name]:
            raise ValueError('Validated runtime changed: ' + name)
    if digest((ROOT / manifest['adapter_path']).read_bytes()) != manifest['adapter_sha256']:
        raise ValueError('Field adapter changed')
    records = {r['id']: r for r in manifest['candidates']}
    if len(records) != 572 or len(manifest['candidates']) != 572:
        raise ValueError('Expected 572 distinct strategy identities')
    # Verify every source before compiling any source.
    sources = {}
    for sid, row in records.items():
        source = (ROOT / row['source_path']).read_bytes()
        if digest(source) != row['source_sha256']:
            raise ValueError('Candidate source changed: ' + sid)
        sources[sid] = source.decode('utf-8')
    players = {sid: compile_candidate(sources[sid], records[sid]['source_sha256']) for sid in sorted(records)}
    dependencies = ('execute_uniform.py', 'runtime.py', 'uniform_semantics_v3b.py', 'validate_pilot.py')
    provenance = {'manifest_sha256': MANIFEST_SHA256,
        'dependencies': {name: digest((ROOT / 'phase3' / name).read_bytes()) for name in dependencies},
        'python': platform.python_version(), 'axelrod': axl.__version__, 'numpy': np.__version__}
    return Field(players, records, provenance)


def diagnostic_pairs(field):
    """Each identity meets the first identity of the next model, plus 8 self-pairs."""
    groups = {}
    for sid in sorted(field.players):
        groups.setdefault(sid.split('/')[0], []).append(sid)
    models = sorted(groups)
    if len(models) < 2:
        raise ValueError('Mixed-model diagnostic requires at least two models')
    pairs = set()
    for i, model in enumerate(models):
        representative = groups[models[(i + 1) % len(models)]][0]
        pairs.update(tuple(sorted((sid, representative))) for sid in groups[model])
        pairs.add((groups[model][0], groups[model][0]))
    return sorted(pairs)


def checked_payload(payload, turns):
    counts = [payload[k] for k in ('CC', 'CD', 'DC', 'DD')]
    if any(type(c) is not int or c < 0 for c in counts) or sum(counts) != turns:
        raise ValueError('Invalid persisted action counts')
    cc, cd, dc, dd = counts
    expected = ((3 * cc + 5 * dc + dd) / turns, (3 * cc + 5 * cd + dd) / turns)
    if payload['payoff_i'] != expected[0] or payload['payoff_j'] != expected[1]:
        raise ValueError('Persisted payoff/count mismatch')
    return payload


def run(database, field, *, repetitions, turns=1000, seed=20260913, pairs=None, max_new=None):
    if any(type(n) is not int or n < 1 for n in (repetitions, turns)):
        raise ValueError('Positive integer repetitions and turns required')
    if max_new is not None and (type(max_new) is not int or max_new < 0):
        raise ValueError('max_new must be a nonnegative integer')
    ids = sorted(field.players)
    if not ids or set(ids) != set(field.records):
        raise ValueError('Field identities/records mismatch')
    selected = None if pairs is None else sorted({tuple(sorted(p)) for p in pairs})
    if selected is not None and (not selected or any(len(p) != 2 or any(s not in field.players for s in p) for p in selected)):
        raise ValueError('Invalid selected pairs')
    config = {'kind': 'full_round_robin' if selected is None else 'selected_diagnostic',
        'ids': ids, 'sources': {sid: field.records[sid]['source_sha256'] for sid in ids},
        'provenance': field.provenance, 'executor_sha256': digest(Path(__file__).read_bytes()),
        'turns': turns, 'repetitions': repetitions, 'seed': seed,
        'game': {'R': 3, 'S': 0, 'T': 5, 'P': 1}, 'noise': 0,
        'schedule': 'sorted_unordered_with_self_v1', 'selected_pairs': selected}
    signature = digest(encoded(config).encode())
    expected = (len(ids) * (len(ids) + 1) // 2 if selected is None else len(selected)) * repetitions
    database = Path(database)
    database.parent.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    new = 0
    with sqlite3.connect(database, timeout=60) as db:
        db.execute('CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
        db.execute('CREATE TABLE IF NOT EXISTS matches (id_i TEXT, id_j TEXT, repetition INTEGER, seed INTEGER NOT NULL, status TEXT NOT NULL, payload TEXT NOT NULL, PRIMARY KEY(id_i,id_j,repetition))')
        with db:
            previous = db.execute("SELECT value FROM metadata WHERE key='config'").fetchone()
            if previous and previous[0] != encoded(config):
                raise ValueError('Checkpoint configuration changed; use a new database')
            if previous is None and db.execute('SELECT COUNT(*) FROM matches').fetchone()[0]:
                raise ValueError('Unanchored checkpoint data')
            db.execute("INSERT OR IGNORE INTO metadata VALUES ('config',?)", (encoded(config),))
            db.execute("INSERT OR IGNORE INTO metadata VALUES ('signature',?)", (signature,))
        failed = db.execute("SELECT COUNT(*) FROM matches WHERE status='error'").fetchone()[0]
        schedule = selected if selected is not None else itertools.combinations_with_replacement(ids, 2)
        if not failed:
            for first, second in schedule:
                for repetition in range(repetitions):
                    if max_new is not None and new >= max_new:
                        break
                    match_seed = seed_for(seed, first, second, repetition)
                    # One transaction claims one match. A crash before commit leaves
                    # no partial row; a committed error blocks automatic retries.
                    db.execute('BEGIN IMMEDIATE')
                    previous = db.execute('SELECT seed,status,payload FROM matches WHERE id_i=? AND id_j=? AND repetition=?',
                                          (first, second, repetition)).fetchone()
                    if previous:
                        db.rollback()
                        if previous[0] != match_seed or previous[1] != 'ok':
                            raise ValueError('Invalid checkpoint match state')
                        checked_payload(json.loads(previous[2]), turns)
                        continue
                    try:
                        payload = checked_payload(play_pair(field.players[first], field.players[second], turns, match_seed), turns)
                        status = 'ok'
                    except Exception as exc:
                        payload = {'error': type(exc).__name__ + ': ' + str(exc)}
                        status = 'error'
                    db.execute('INSERT INTO matches VALUES (?,?,?,?,?,?)',
                               (first, second, repetition, match_seed, status, encoded(payload)))
                    db.commit()
                    new += 1
                    if status == 'error':
                        failed = 1
                        break
                if failed or max_new is not None and new >= max_new:
                    break
        total = db.execute("SELECT COUNT(*) FROM matches WHERE status='ok'").fetchone()[0]
    return {'kind': config['kind'], 'config_sha256': signature, 'expected_matches': expected,
            'new_matches': new, 'completed_matches': total, 'failed_matches': failed,
            'complete': total == expected and not failed, 'blocked': bool(failed),
            'elapsed_seconds': time.monotonic() - start,
            'scope': 'Selected diagnostic results must not enter confirmatory H7.' if selected is not None else 'Full schedule; analysis requires completeness.'}


def export_matrices(database, field):
    """Build analyzer inputs only from a complete, matching full schedule."""
    with sqlite3.connect(database) as db:
        config = json.loads(db.execute("SELECT value FROM metadata WHERE key='config'").fetchone()[0])
        if config['kind'] != 'full_round_robin':
            raise ValueError('Diagnostics cannot be exported as a confirmatory matrix')
        ids = sorted(field.players)
        if (config['ids'] != ids or config['provenance'] != field.provenance
                or config['sources'] != {sid: field.records[sid]['source_sha256'] for sid in ids}
                or config['executor_sha256'] != digest(Path(__file__).read_bytes())):
            raise ValueError('Checkpoint field/executor changed')
        rows = db.execute('SELECT id_i,id_j,repetition,seed,status,payload FROM matches').fetchall()
    expected = len(ids) * (len(ids) + 1) // 2 * config['repetitions']
    if len(rows) != expected:
        raise ValueError('Incomplete match matrix')
    positions = {sid: i for i, sid in enumerate(ids)}
    c, payoff = np.zeros((len(ids), len(ids))), np.zeros((len(ids), len(ids)))
    seen = set()
    for first, second, repetition, match_seed, status, data in rows:
        if (first not in positions or second not in positions or first > second
                or type(repetition) is not int or not 0 <= repetition < config['repetitions']
                or status != 'ok' or (first, second, repetition) in seen
                or match_seed != seed_for(config['seed'], first, second, repetition)):
            raise ValueError('Invalid or failed match in matrix')
        seen.add((first, second, repetition))
        p = checked_payload(json.loads(data), config['turns'])
        i, j = positions[first], positions[second]
        c[i, j] += p['CC'] / (config['turns'] * config['repetitions'])
        payoff[i, j] += p['payoff_i'] / config['repetitions']
        if i != j:
            c[j, i] = c[i, j]
            payoff[j, i] += p['payoff_j'] / config['repetitions']
    return {'ids': ids, 'models': [sid.split('/')[0] for sid in ids],
            'attitudes': [sid.split('/')[-1].split('_')[0] for sid in ids],
            'cooperation': c, 'payoff': payoff}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--diagnostic', action='store_true')
    mode.add_argument('--run', action='store_true', help='Explicit full run; final protocol must be settled beforehand')
    parser.add_argument('--database', type=Path)
    parser.add_argument('--repetitions', type=int)
    parser.add_argument('--max-new', type=int)
    args = parser.parse_args()
    field = load_field()
    if not args.diagnostic and not args.run:
        print(encoded({'preflight': 'passed', 'participants': len(field.players), 'manifest_sha256': MANIFEST_SHA256}))
        return
    if args.database is None or args.run and args.repetitions is None:
        parser.error('Execution requires --database; full runs also require explicit --repetitions')
    if args.diagnostic and args.repetitions not in (None, 1):
        parser.error('The fixed diagnostic uses one repetition')
    result = run(args.database, field, repetitions=args.repetitions if args.run else 1,
                 pairs=diagnostic_pairs(field) if args.diagnostic else None, max_new=args.max_new)
    print(encoded(result))


if __name__ == '__main__':
    main()
