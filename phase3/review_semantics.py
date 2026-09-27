"""Materialize the assistant's explicit prose-only review, not an automated judge.

Only class names/locations and preceding comments are inspected. No generated
method bodies are executed or used as a behavioral reference. No API calls.
"""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ATTITUDES = ('Aggressive', 'Cooperative', 'Neutral')

# Manual decisions from reading the complete archived comments, before outcomes.
# Keys: model/class, profile or None, rationale, unresolved witness (own/opponent).
DECISIONS = {
    'anthropic_sonnet46/Aggressive_11': ('always_d', 'Todas las fases ordenan D. El título Tit-for-Tat no coincide con las reglas operativas; se siguen las reglas. La afirmación de optimalidad de la explicación no se valida ni se incorpora al algoritmo.', None),
    'anthropic_sonnet46/Cooperative_2': ('tft_last10', 'C inicial; copia al rival en 2–990; D incondicional en 991–1000.', None),
    'anthropic_sonnet46/Neutral_6': ('tft_final', 'C inicial; copia al rival en 2–999; D en 1000. La brevedad del texto no omite reglas.', None),
    'gemini_25_flash/Aggressive_2': ('grim_start_d', 'D inicial tiene prioridad sobre la condición vacía de cooperación previa; después D si el rival alguna vez jugó D y C si siempre jugó C. No se añade defección final.', None),
    'gemini_25_flash/Cooperative_5': ('tft', 'C inicial y copia de la última acción del rival en todas las rondas posteriores, incluida 1000.', None),
    'gemini_25_flash/Neutral_1': ('tft', 'C inicial y copia de la última acción del rival; no prescribe una excepción final.', None),
    'gemini_31_pro/Aggressive_10': ('probe3', 'Prioridad explícita: D en 991–1000; D tras D del rival; D tras tres C consecutivas del rival; C en los demás casos, incluido el inicio.', None),
    'gemini_31_pro/Cooperative_3': ('tft_final', 'C inicial; copia al rival en 2–999; D en 1000.', None),
    'gemini_31_pro/Neutral_9': ('tft_final', 'C inicial; copia al rival en 2–999; D en 1000.', None),
    'openai_gpt54mini/Aggressive_9': ('always_d', 'Las reglas y el resumen ordenan D en todas las rondas.', None),
    'openai_gpt54mini/Cooperative_20': ('tft', 'C inicial; copia de la última acción; vuelve a C inmediatamente después de C del rival. Los caracteres de sustitución en la frase explicativa se preservan: las reglas numeradas son legibles.', None),
    'openai_gpt54mini/Neutral_14': ('tft', 'C inicial; copia de la última acción del rival durante las 1000 rondas.', None),
    'gemini_25_flash/Aggressive_6': (None, 'Falta la acción desde la ronda 11 cuando el rival solo ha cooperado. El texto termina en «play».', ('D'*10, 'C'*10)),
    'gemini_25_flash/Aggressive_24': (None, 'La cláusula de retorno forzado a D termina en «regardless»; no termina de precisar su alcance frente a otras reglas. Tampoco hay una rama completa para C propio/D rival fuera de ese retorno. El resumen general no resuelve inequívocamente la prioridad.', ('C', 'D')),
    'gemini_31_pro/Aggressive_1': (None, 'La condición de restauración de cooperación está incompleta; no se define la acción de ronda 2.', ('D', 'D')),
    'gemini_31_pro/Aggressive_3': (None, 'Falta la regla de sondeo y el caso base, incluido el inicio; las otras reglas no cubren el historial vacío.', ('', '')),
    'gemini_31_pro/Aggressive_5': (None, 'Se prescribe D tras acciones distintas, pero falta la acción tras acciones iguales. El nombre Win-Stay Lose-Shift no sustituye la regla ausente.', ('D', 'D')),
    'gemini_31_pro/Aggressive_7': (None, 'Desde ronda 4 la condición de explotación queda incompleta y carece de acción.', ('DCC', 'CCC')),
    'gemini_31_pro/Aggressive_8': (None, 'Aunque el corte visible está en una explicación, solo se especifican rondas 1–3 y 1000; faltan reglas para 4–999.', ('DCC', 'CCC')),
    'gemini_31_pro/Aggressive_9': ('probe4_self', 'Reglas completas antes de la explicación cortada: D final; D si C propio/D rival previo; D tras cuatro C consecutivas del rival; C en los demás casos, incluido el inicio. Se preserva el fragmento explicativo sin completarlo.', None),
    'gemini_31_pro/Aggressive_11': (None, 'La regla de romper dos DD consecutivos no cubre la ronda 2 ni los demás casos sin esa condición; falta el caso base.', ('D', 'C')),
    'gemini_31_pro/Aggressive_13': (None, 'La regla de disculpa se interrumpe dentro de la condición, sin acción ni continuación para el resto de rondas.', ('D', 'D')),
    'gemini_31_pro/Aggressive_15': (None, 'El sondeo periódico termina dentro del ejemplo; faltan su acción y el caso base/inicial.', ('', '')),
    'gemini_31_pro/Aggressive_16': (None, 'Está definido D si el rival cooperó en rondas 2 y 3; falta la rama para rivales que no cumplen esa condición.', ('DCC', 'CDC')),
    'gemini_31_pro/Aggressive_17': (None, 'La condición de ronda 1 y múltiplos de 10 carece de acción; falta el caso base.', ('', '')),
    'gemini_31_pro/Aggressive_18': (None, 'La represalia y el final están definidos, pero falta una regla operativa para los casos sin D previo. El objetivo general de cooperación no fija el resto de la política.', ('CC', 'CC')),
    'gemini_31_pro/Aggressive_19': (None, 'Tras el inicio, fuera de dos D consecutivas del rival, la siguiente condición está cortada y falta el caso base.', ('D', 'C')),
    'gemini_31_pro/Aggressive_21': (None, 'La regla «Cooperate in» no termina de definir su condición. Falta una acción inicial explícita y una cobertura inequívoca del resto.', ('', '')),
    'gemini_31_pro/Aggressive_22': (None, 'La condición B está cortada; no se define la respuesta tras DD ni las otras combinaciones restantes.', ('D', 'D')),
    'gemini_31_pro/Aggressive_23': (None, 'Las reglas cubren DD y CD previos, pero faltan inicio y respuesta tras C del rival.', ('', '')),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def extract_comment(path, class_name):
    source = path.read_text(encoding='utf-8-sig')
    lines = source.splitlines()
    cls = next(n for n in ast.parse(source).body if isinstance(n, ast.ClassDef) and n.name == class_name)
    i, block = cls.lineno-2, []
    while i >= 0:
        line = lines[i].strip()
        if line.startswith('#'):
            block.append(line[1:].strip())
        elif line:
            break
        i -= 1
    return ' '.join(reversed(block)).strip()


# Expected actions are explicitly curated from the prose. Histories are
# counterfactual test inputs, not newly simulated matches or experimental data.
TFT = [('opening', '', '', 'C'), ('after_C', 'C', 'C', 'C'),
       ('after_D', 'C', 'D', 'D'), ('forgiveness', 'CD', 'DC', 'C')]
VECTORS = {
    'always_d': [('opening', '', '', 'D'), ('after_C', 'D', 'C', 'D'),
                 ('after_D', 'D', 'D', 'D'), ('last_round', 'D'*999, 'C'*999, 'D')],
    'tft': TFT + [('last_round_C', 'C'*999, 'C'*999, 'C'), ('last_round_D', 'C'*999, 'C'*998+'D', 'D')],
    'tft_final': TFT + [('round999', 'C'*998, 'C'*998, 'C'), ('round1000', 'C'*999, 'C'*999, 'D')],
    'tft_last10': TFT + [('round990', 'C'*989, 'C'*989, 'C'), ('round991', 'C'*990, 'C'*990, 'D'),
                       ('round1000', 'C'*999, 'C'*999, 'D')],
    'grim_start_d': [('opening', '', '', 'D'), ('after_C', 'D', 'C', 'C'),
                     ('after_D', 'D', 'D', 'D'), ('no_forgiveness', 'DD', 'DC', 'D'),
                     ('last_round_C', 'D'+'C'*998, 'C'*999, 'C')],
    'probe3': [('opening', '', '', 'C'), ('one_C', 'C', 'C', 'C'), ('two_C', 'CC', 'CC', 'C'),
               ('three_C', 'CCC', 'CCC', 'D'), ('after_D', 'C', 'D', 'D'),
               ('reset_streak', 'CCC', 'DCC', 'C'), ('round990', 'C'*989, 'D'*987+'CC', 'C'),
               ('round991', 'C'*990, 'D'*988+'CC', 'D')],
    'probe4_self': [('opening', '', '', 'C'), ('three_C', 'CCC', 'CCC', 'C'),
                    ('four_C', 'CCCC', 'CCCC', 'D'), ('sucker', 'C', 'D', 'D'),
                    ('DD_is_not_sucker', 'D', 'D', 'C'), ('round999', 'D'*998, 'D'*998, 'C'),
                    ('round1000', 'D'*999, 'D'*999, 'D')],
}


def encode_history(text):
    blocks = []
    for action in text:
        if blocks and blocks[-1][0] == action:
            blocks[-1][1] += 1
        else:
            blocks.append([action, 1])
    return blocks


def save_new_or_identical(path, value):
    data = (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode()
    if path.exists() and path.read_bytes() != data:
        raise ValueError(f'Review evidence differs; create an explicitly versioned revision: {path}')
    path.write_bytes(data)


def check_artifacts():
    inputs = ROOT/'phase3/inputs'
    report = json.loads((inputs/'semantic_review_v1.json').read_text(encoding='utf-8'))
    vectors = json.loads((inputs/'semantic_test_vectors_v1.json').read_text(encoding='utf-8'))['cases']
    by_id = {r['id']: r for r in report['cases']}
    assert len(by_id) == len(report['cases']) == 30
    assert Counter(r['status'] for r in report['cases']) == report['summary']
    assert report['selection_sha256'] == sha((inputs/'pilot_selection.json').read_bytes())
    seen, covered, counts = {}, set(), Counter()
    for record in report['cases']:
        assert sha(record['prose_exact_extracted'].encode()) == record['prose_sha256']
        assert sha((ROOT/record['snapshot_path']).read_bytes()) == record['snapshot_sha256']
        if record['status'] == 'blocked_incomplete_rules':
            witness = record['unresolved_witness']
            assert len(witness['own']) == len(witness['opponent']) == witness['round']-1
            assert witness['expected_action'] is None
    for case in vectors:
        decoded = []
        for field in ('own_rle', 'opponent_rle'):
            blocks = case[field]
            assert all(a in ('C', 'D') and isinstance(n, int) and n > 0 for a, n in blocks)
            decoded.append(''.join(a*n for a, n in blocks))
        own, opponent = decoded
        assert len(own) == len(opponent) == case['round']-1
        assert 1 <= case['round'] <= 1000 and case['expected_action'] in ('C', 'D')
        record = by_id[case['strategy_id']]
        assert record['status'] == 'eligible_prose'
        assert case['source_prose_sha256'] == record['prose_sha256']
        key = (case['strategy_id'], own, opponent)
        assert key not in seen or seen[key] == case['expected_action']
        seen[key] = case['expected_action']
        covered.add(case['strategy_id'])
        counts[record['cohort']] += 1
    assert covered == {r['id'] for r in report['cases'] if r['status'] == 'eligible_prose'}
    assert counts == {'pilot': 70, 'truncated_diagnostic': 7}
    print('Artifact integrity, 30 source hashes, 17 unresolved witnesses, 77 consistent test vectors: OK')
    print('These checks do not execute converted code or establish exhaustive semantic equivalence.')


def main():
    inputs = ROOT/'phase3/inputs'
    selection_path = inputs/'pilot_selection.json'
    selection = json.loads(selection_path.read_text(encoding='utf-8'))
    manifest = json.loads((inputs/'manifest.json').read_text(encoding='utf-8'))
    lookup = {s['id']: (lib, s) for lib in manifest['libraries'] for s in lib['strategies']}
    pilot_ids = [c['id'] for c in selection['cases']]
    ids = pilot_ids + selection['diagnostic_truncated_ids']
    assert len(ids) == len(set(ids)) == len(DECISIONS) == 30
    records, vectors = [], []
    for sid in ids:
        lib, original = lookup[sid]
        model, _, name = sid.split('/')
        path = ROOT/lib['snapshot_path']
        if sha(path.read_bytes()) != lib['sha256']:
            raise ValueError(f'Snapshot changed: {path}')
        prose = extract_comment(path, name)
        if sha(prose.encode()) != original['prose_sha256']:
            raise ValueError(f'Prose hash mismatch: {sid}')
        profile, rationale, witness = DECISIONS[model+'/'+name]
        status = 'eligible_prose' if profile else 'blocked_incomplete_rules'
        record = {'id': sid, 'cohort': 'pilot' if sid in pilot_ids else 'truncated_diagnostic',
                  'status': status, 'profile': profile, 'rationale_es': rationale,
                  'prose_exact_extracted': prose, 'prose_sha256': original['prose_sha256'],
                  'snapshot_path': lib['snapshot_path'], 'snapshot_sha256': lib['sha256'],
                  'source_commit': lib['source_commit'], 'known_truncation': sid not in pilot_ids,
                  'unicode_replacement_characters': prose.count('\ufffd'),
                  'conversion_performed': False}
        if witness:
            own, opponent = witness
            assert len(own) == len(opponent) and set(own+opponent) <= set('CD')
            record['unresolved_witness'] = {'round': len(own)+1, 'own': own, 'opponent': opponent,
                                            'expected_action': None,
                                            'scope': 'Counterfactual equal-length history; reachability under an incomplete policy is not asserted.'}
        for label, own, opponent, action in VECTORS.get(profile, []):
            assert len(own) == len(opponent) and 0 <= len(own) < 1000
            assert action in ('C', 'D') and set(own+opponent) <= set('CD')
            vectors.append({'strategy_id': sid, 'case': label, 'round': len(own)+1,
                            'own_rle': encode_history(own), 'opponent_rle': encode_history(opponent),
                            'expected_action': action, 'source_prose_sha256': original['prose_sha256']})
        records.append(record)
    report = {'schema': 1, 'date': '2026-09-13', 'reviewer': 'Codex assistant; one semantic review, no independent human adjudication',
              'basis': 'Archived prose only, no generated implementation or tournament outcomes used to settle missing rules.',
              'selection_sha256': sha(selection_path.read_bytes()),
              'conventions': ['Round = history length + 1; histories contain completed rounds only.',
                              'A condition requiring k previous rounds is false when fewer than k exist.',
                              'Explicit initial/final rules and stated priorities control; no final defection is added when absent.',
                              'Eligibility means the prose is sufficiently specified for a pilot, not that any generated code is already faithful.'],
              'summary': dict(Counter(r['status'] for r in records)), 'cases': records}
    save_new_or_identical(inputs/'semantic_review_v1.json', report)
    save_new_or_identical(inputs/'semantic_test_vectors_v1.json', {
        'schema': 1, 'status': 'expected_cases_not_yet_run_against_converted_code',
        'history_encoding': 'RLE ordered [action, positive count]; [] is empty.',
        'scope': 'Targeted semantic boundary checks, not exhaustive equivalence or observed match results.',
        'cases': vectors})
    print(json.dumps({'review': report['summary'], 'pilot_eligible': sum(r['status']=='eligible_prose' and r['cohort']=='pilot' for r in records),
                      'diagnostic_eligible': sum(r['status']=='eligible_prose' and r['cohort']=='truncated_diagnostic' for r in records),
                      'expected_test_cases': len(vectors), 'api_calls': 0}))


if __name__ == '__main__':
    if sys.argv[1:] == ['--check']:
        check_artifacts()
    elif sys.argv[1:]:
        raise SystemExit('Usage: python -m phase3.review_semantics [--check]')
    else:
        main()
        check_artifacts()
