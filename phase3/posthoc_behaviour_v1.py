"""Post hoc behavioural characterisation of the 572 Phase 3 identities (NOT preregistered).

New, exploratory encounters: every identity plays a fixed panel of ten probe
opponents for 1,000 rounds (focal in the first seat, fixed seeds, no noise).
The resulting action strings are compared with canonical deterministic
strategies. Signature equality means "indistinguishable on this probe panel",
not formal behavioural equivalence.

Also summarised, without new encounters: exact AST sharing across attitude
labels and identical rows of the registered tournament matrix.
"""
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
import json

import numpy as np

from phase3.analyze_phase3 import ATTITUDES
from phase3.posthoc_common_v1 import (ENDGAME, MODEL_LABELS, OUT, ROOT, TURNS, canonical_signatures,
                                      descriptors, label_signature, load_primary, signature,
                                      signature_key, write_json)
from phase3.sensitivity_analysis_v1 import ast_group

OUTPUT = OUT / 'behaviour_v1.json'
_PLAYERS = None
_REFS = None


def _init():
    global _PLAYERS, _REFS
    from phase3.execute_uniform import load_field
    _PLAYERS = load_field().players
    _REFS = canonical_signatures()


def _characterise(sid):
    sig = signature(_PLAYERS[sid])
    return sid, {
        'label': label_signature(sig, _REFS),
        'descriptors': descriptors(sig),
        'signature_key': signature_key(sig),
        'signature_key_pre_endgame': signature_key(sig, TURNS - ENDGAME),
        'probe_cooperation': {name: sig[name]['mine'].count('C') / TURNS for name in sig},
    }


def attitude_of(sid):
    return sid.split('/')[-1].split('_')[0]


def model_of(sid):
    return sid.split('/')[0]


def sharing(keys, ids):
    """Share of identities whose key is also held by an identity with another attitude label."""
    holders = defaultdict(set)
    for sid in ids:
        holders[keys[sid]].add(attitude_of(sid))
    out = {}
    for att in ATTITUDES:
        mine = [sid for sid in ids if attitude_of(sid) == att]
        out[att] = {
            'identities': len(mine),
            'distinct_keys': len({keys[s] for s in mine}),
            'shared_with_any_other_attitude': sum(len(holders[keys[s]] - {att}) > 0 for s in mine) / len(mine),
        }
    cn = [sid for sid in ids if attitude_of(sid) in ('Cooperative', 'Neutral')]
    out['cooperative_neutral_pooled'] = {
        'identities': len(cn),
        'distinct_keys': len({keys[s] for s in cn}),
        'shared_between_cooperative_and_neutral': sum(
            {'Cooperative', 'Neutral'} <= holders[keys[s]] for s in cn) / len(cn),
    }
    out['distinct_keys_total'] = len(set(keys.values()))
    return out


def main():
    if OUTPUT.exists():
        raise FileExistsError('Output exists; inspect before rerunning')
    from phase3.execute_uniform import load_field
    field = load_field()
    ids = sorted(field.players)

    with ProcessPoolExecutor(max_workers=7, initializer=_init) as pool:
        rows = dict(pool.map(_characterise, ids, chunksize=8))

    # 1. Canonical labels by model x attitude
    by_cell = defaultdict(Counter)
    by_att = defaultdict(Counter)
    for sid, row in rows.items():
        by_cell[(model_of(sid), attitude_of(sid))][row['label']['label']] += 1
        by_att[attitude_of(sid)][row['label']['label']] += 1

    def cell_summary(members):
        d = [rows[s]['descriptors'] for s in members]
        m1 = defaultdict(list)
        for x in d:
            for k, v in x['memory_one_vs_fixed05'].items():
                if v is not None:
                    m1[k].append(v)
        return {
            'n': len(members),
            'nice_share': float(np.mean([x['nice'] for x in d])),
            'first_move_cooperate_share': float(np.mean([x['first_move'] == 'C' for x in d])),
            'exploits_cooperator_share': float(np.mean([x['exploits_cooperator'] > 0 for x in d])),
            'endgame_defection_share': float(np.mean([x['endgame_defection_vs_cooperator'] for x in d])),
            'mean_cooperation_vs_defector': float(np.mean([x['cooperation_vs_defector'] for x in d])),
            'mean_cooperation_vs_tft': float(np.mean([x['cooperation_vs_tft'] for x in d])),
            'mean_cooperation_vs_fixed05': float(np.mean([x['cooperation_vs_fixed05'] for x in d])),
            'mean_memory_one_vs_fixed05': {k: float(np.mean(v)) for k, v in m1.items()},
        }

    cells = {}
    for model in sorted({model_of(s) for s in ids}):
        for att in ATTITUDES:
            members = [s for s in ids if model_of(s) == model and attitude_of(s) == att]
            cells[f'{model}/{att}'] = {**cell_summary(members),
                                       'labels': dict(by_cell[(model, att)].most_common())}
    attitudes = {att: {**cell_summary([s for s in ids if attitude_of(s) == att]),
                       'labels': dict(by_att[att].most_common())} for att in ATTITUDES}

    # 2. Signature, AST and tournament-row sharing across attitude labels
    sig_keys = {s: rows[s]['signature_key'] for s in ids}
    cut_keys = {s: rows[s]['signature_key_pre_endgame'] for s in ids}
    ast_keys = {s: ast_group((ROOT / field.records[s]['source_path']).read_text(encoding='utf-8'))
                for s in ids}
    data = load_primary()
    if data['ids'] != ids:
        raise ValueError('Identity order differs between field and primary matrix')
    c, payoff = data['cooperation'], data['payoff']
    # Full rows, diagonal included: two identical deterministic programs i, i' satisfy
    # c[i,i] = c[i,i'] = c[i',i'], so their complete rows coincide position by position.
    row_keys = {sid: json.dumps([np.round(c[i], 6).tolist(), np.round(payoff[i], 6).tolist()])
                for i, sid in enumerate(ids)}

    result = {
        'status': 'post hoc, not preregistered; exploratory encounters against a fixed probe panel',
        'probe_panel': [name for name in rows[ids[0]]['probe_cooperation']],
        'turns': TURNS, 'endgame_rounds_ignored_for_near_matches': ENDGAME,
        'canonical_references': sorted({lab for r in rows.values() for lab in r['label']['all_matches']}),
        'by_attitude': attitudes,
        'by_model_attitude': cells,
        'sharing': {
            'probe_signature': sharing(sig_keys, ids),
            'probe_signature_pre_endgame': sharing(cut_keys, ids),
            'ast': sharing(ast_keys, ids),
            'tournament_row_full': sharing(row_keys, ids),
        },
        'identities': {sid: {'label': rows[sid]['label'], 'descriptors': rows[sid]['descriptors'],
                             'signature_key': rows[sid]['signature_key'],
                             'signature_key_pre_endgame': rows[sid]['signature_key_pre_endgame'],
                             'ast_group': ast_keys[sid],
                             'probe_cooperation': rows[sid]['probe_cooperation']} for sid in ids},
        'model_labels': MODEL_LABELS,
    }
    write_json(OUTPUT, result)
    print(json.dumps({'by_attitude_labels': {a: attitudes[a]['labels'] for a in ATTITUDES},
                      'nice': {a: attitudes[a]['nice_share'] for a in ATTITUDES},
                      'sharing': result['sharing']}, indent=1))


if __name__ == '__main__':
    main()
