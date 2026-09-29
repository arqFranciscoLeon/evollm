"""Synthetic-only execution/calibration with identity-safe SQLite checkpoints."""
import argparse
import hashlib
import importlib.metadata
import itertools
import json
from pathlib import Path
import sqlite3
import time

import axelrod as axl
from phase3.runtime import play_pair, seed_for


def benchmark(database, repetitions=20, turns=1000):
    if repetitions < 1 or turns < 1:
        raise ValueError('repetitions and turns must be positive')
    players = [axl.Cooperator, axl.Defector, axl.TitForTat, axl.Random, axl.Grudger, axl.WinStayLoseShift]
    config = {'kind': 'synthetic_only', 'players': [p.__name__ for p in players], 'turns': turns,
              'repetitions': repetitions, 'seed': 20260913, 'axelrod': importlib.metadata.version('axelrod'),
              'runtime_sha256': hashlib.sha256(Path(__file__).with_name('runtime.py').read_bytes()).hexdigest(),
              'executor_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    encoded = json.dumps(config, sort_keys=True)
    signature = hashlib.sha256(encoded.encode()).hexdigest()
    database = Path(database)
    database.parent.mkdir(parents=True, exist_ok=True)
    completed = 0
    start = time.monotonic()
    with sqlite3.connect(database) as db:
        db.execute('CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
        db.execute('CREATE TABLE IF NOT EXISTS matches (i INTEGER, j INTEGER, repetition INTEGER, payload TEXT NOT NULL, PRIMARY KEY(i,j,repetition))')
        previous = db.execute("SELECT value FROM metadata WHERE key='signature'").fetchone()
        if previous and previous[0] != signature:
            raise ValueError('Checkpoint configuration changed; use a new database')
        db.execute("INSERT OR IGNORE INTO metadata VALUES ('signature', ?)", (signature,))
        db.execute("INSERT OR IGNORE INTO metadata VALUES ('config', ?)", (encoded,))
        db.commit()
        for i,j in itertools.combinations_with_replacement(range(len(players)),2):
            for repetition in range(repetitions):
                if db.execute('SELECT 1 FROM matches WHERE i=? AND j=? AND repetition=?',(i,j,repetition)).fetchone():
                    continue
                result = play_pair(players[i],players[j],turns,seed_for(config['seed'],i,j,repetition))
                db.execute('INSERT INTO matches VALUES (?,?,?,?)',(i,j,repetition,json.dumps(result)))
                db.commit()
                completed += 1
        total = db.execute('SELECT COUNT(*) FROM matches').fetchone()[0]
    elapsed = time.monotonic()-start
    return {'config': config, 'new_matches': completed, 'total_matches': total, 'elapsed_seconds': elapsed,
            'seconds_per_new_match': elapsed/completed if completed else None,
            'warning': 'Classical synthetic strategies only. This throughput does not predict generated-code cost; no Phase 3 outcome collected.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', required=True)
    parser.add_argument('--repetitions', type=int, default=20)
    args = parser.parse_args()
    result = benchmark(args.database,args.repetitions)
    Path(args.database).with_suffix('.summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
