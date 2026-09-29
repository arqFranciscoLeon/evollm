"""Shared helpers for the post hoc (NOT preregistered) Phase 3 analyses.

Everything produced with these helpers is exploratory. Nothing here alters the
registered H7 test, its inputs or its outputs. Outputs go to phase3/posthoc_v1/.
"""
import hashlib
import json
from pathlib import Path

import axelrod as axl
import numpy as np

from phase3.analyze_phase3 import ATTITUDES
from phase3.runtime import seed_for

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / 'phase3'
OUT = PHASE / 'posthoc_v1'
MATRIX = OUT / 'primary_matrix_v1.npz'
BASE_SEED = 20260913
TURNS = 1000
ENDGAME = 10  # rounds excluded when testing "identical except at the end"

# Registered values that post hoc work must reproduce before building on them.
REGISTERED_H7 = 0.005348991712007744
REGISTERED_MATRIX_SHA = 'b38cc9f6678a28a505e3666626d116b8867206e0902efd7f556e9256cbe72eef'

MODEL_LABELS = {
    'anthropic_sonnet46': 'Sonnet 4.6', 'deepseek_v4pro': 'DeepSeek V4 Pro',
    'gemini_25_flash': 'Gemini 2.5 Flash', 'gemini_31_pro': 'Gemini 3.1 Pro',
    'glm_51': 'GLM-5.1', 'kimi_k25': 'Kimi K2.5', 'openai_gpt54mini': 'GPT-5.4 Mini',
    'qwen3max': 'Qwen3-Max',
}

def fixed_sequence(p_cooperate, label):
    """Pre-generated pseudo-random action string, identical for every focal strategy.

    axelrod seeds players differently depending on their 'stochastic' classifier,
    so axl.Random probes would not face every focal with the same sequence.
    A Cycler over a fixed 1,000-action string avoids that dependence.
    """
    rng = np.random.default_rng(seed_for(BASE_SEED, 'posthoc_fixed_sequence_v1', label))
    return ''.join('C' if x < p_cooperate else 'D' for x in rng.random(TURNS))


FIXED_05 = fixed_sequence(0.5, 'p0.5')
FIXED_09 = fixed_sequence(0.9, 'p0.9')

# Probe panel: fixed opponents used only to characterise behaviour post hoc.
# All probes are deterministic; the focal strategy always occupies the first seat.
PROBES = (
    ('Cooperator', lambda: axl.Cooperator()),
    ('Defector', lambda: axl.Defector()),
    ('Alternator', lambda: axl.Alternator()),
    ('TitForTat', lambda: axl.TitForTat()),
    ('SuspiciousTitForTat', lambda: axl.SuspiciousTitForTat()),
    ('Grudger', lambda: axl.Grudger()),
    ('CyclerCCD', lambda: axl.CyclerCCD()),
    ('CyclerDDC', lambda: axl.CyclerDDC()),
    ('Fixed0.5', lambda: axl.Cycler(cycle=FIXED_05)),
    ('Fixed0.9', lambda: axl.Cycler(cycle=FIXED_09)),
)

# Canonical deterministic references for labelling probe signatures.
CANONICAL = (
    'Cooperator', 'Defector', 'TitForTat', 'SuspiciousTitForTat', 'Grudger',
    'TitFor2Tats', 'TwoTitsForTat', 'WinStayLoseShift', 'HardTitForTat',
    'Alternator', 'Bully', 'SoftGrudger', 'Punisher',
    'OnceBitten', 'GrudgerAlternator', 'Prober',
)


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def file_sha(path):
    return sha256_bytes(Path(path).read_bytes())


def write_json(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + '\n'
    path.write_text(text, encoding='utf-8')
    return sha256_bytes(text.encode('utf-8'))


def load_primary():
    if not MATRIX.exists():
        raise FileNotFoundError('Run phase3/posthoc_matrix_v1.py first')
    data = np.load(MATRIX, allow_pickle=False)
    ids = [str(x) for x in data['ids']]
    return {'ids': ids,
            'models': [s.split('/')[0] for s in ids],
            'attitudes': [s.split('/')[-1].split('_')[0] for s in ids],
            'cooperation': data['cooperation'], 'payoff': data['payoff']}


def matrix_sha(ids, cooperation):
    """Same fingerprint as analyze_confirmatory_results_v1 (ids + float64 LE bytes)."""
    return hashlib.sha256(json.dumps(ids, separators=(',', ':')).encode()
                          + np.asarray(cooperation, dtype='<f8').tobytes()).hexdigest()


def probe_seed(probe_name):
    return seed_for(BASE_SEED, 'posthoc_probe_v1', probe_name)


def play_actions(focal_factory, probe_factory, seed, turns=TURNS):
    """Return the focal's and the probe's action strings; errors propagate."""
    match = axl.Match((focal_factory(), probe_factory()), turns=turns,
                      game=axl.Game(r=3, s=0, t=5, p=1), noise=0, seed=seed)
    history = match.play()
    mine = ''.join(str(a) for a, _ in history)
    theirs = ''.join(str(b) for _, b in history)
    if len(mine) != turns or set(mine) - {'C', 'D'} or set(theirs) - {'C', 'D'}:
        raise ValueError('Invalid probe history')
    return mine, theirs


def signature(focal_factory):
    """Actions of the focal strategy against every probe (one string per probe)."""
    result = {}
    for name, factory in PROBES:
        mine, theirs = play_actions(focal_factory, factory, probe_seed(name))
        result[name] = {'mine': mine, 'theirs': theirs}
    return result


def memory_one(sig, probe='Fixed0.5', last=TURNS - ENDGAME):
    """Empirical P(C | own previous, opponent previous) against the fixed pseudo-random probe.

    Rounds 2..last only, so end-game rules do not dominate. A key missing from
    the output means that the previous-round state never occurred.
    """
    mine, theirs = sig[probe]['mine'], sig[probe]['theirs']
    counts = {k: [0, 0] for k in ('CC', 'CD', 'DC', 'DD')}
    for t in range(1, last):
        state = mine[t - 1] + theirs[t - 1]
        counts[state][1] += 1
        counts[state][0] += mine[t] == 'C'
    return {k: (c / n if n else None) for k, (c, n) in counts.items()}


def descriptors(sig):
    """Axelrod-style properties measured against the probe panel (rounds 1..990)."""
    last = TURNS - ENDGAME
    vs_tft = sig['TitForTat']['mine']
    vs_coop = sig['Cooperator']['mine']
    vs_def = sig['Defector']['mine']
    return {
        'first_move': vs_coop[0],
        'nice': 'D' not in vs_tft[:last],  # never first to defect against TFT
        'exploits_cooperator': vs_coop[:last].count('D') / last,
        'endgame_defection_vs_cooperator': 'D' in vs_coop[last:] and 'D' not in vs_coop[:last],
        'cooperation_vs_defector': vs_def[1:last].count('C') / (last - 1),
        'cooperation_vs_tft': vs_tft.count('C') / TURNS,
        'cooperation_vs_fixed05': sig['Fixed0.5']['mine'].count('C') / TURNS,
        'memory_one_vs_fixed05': memory_one(sig),
    }


def canonical_signatures():
    refs = {}
    for name in CANONICAL:
        cls = getattr(axl, name)
        refs[name] = signature(lambda cls=cls: cls())
    return refs


def signature_key(sig, last=None):
    parts = []
    for name, _ in PROBES:
        mine = sig[name]['mine']
        parts.append(mine if last is None else mine[:last])
    return sha256_bytes('|'.join(parts).encode())


def label_signature(sig, refs):
    """Exact canonical match, canonical match up to the last ENDGAME rounds, or none."""
    exact = [n for n, r in refs.items() if signature_key(r) == signature_key(sig)]
    if exact:
        return {'label': exact[0], 'kind': 'exact', 'all_matches': exact}
    cut = TURNS - ENDGAME
    near = [n for n, r in refs.items() if signature_key(r, cut) == signature_key(sig, cut)]
    if near:
        return {'label': near[0] + ' + end-game deviation', 'kind': 'endgame', 'all_matches': near}
    return {'label': 'non-canonical', 'kind': 'none', 'all_matches': []}
