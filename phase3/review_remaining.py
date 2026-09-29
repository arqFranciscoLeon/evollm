"""Materialize a prose-only assistant review of the 270 remaining Western Default texts.

Assignments below were made after reading every extracted description, not by
keyword classification. This records review decisions, not converted programs.
Prior review and API pilot artifacts remain unchanged.
"""
from collections import Counter, defaultdict
import json
from pathlib import Path

from phase3.review_semantics import ROOT, extract_comment, sha, save_new_or_identical

PROFILES = {}


def profile(key, opening, end, rules, checks, memory='history_only'):
    PROFILES[key] = {'opening': opening, 'endgame_D_from_round': end,
                     'ordered_rules_es': rules, 'required_checks_es': checks,
                     'memory_requirement': memory}


profile('always_d', 'D', None, ['D en todas las rondas.'], ['Inicio D; tras C y D: D; ronda 1000 D.'])
profile('c_then_d', 'C', None, ['C inicial; D desde ronda 2 sin excepciones.'], ['Inicio C; ronda 2 D tras C o D; final D.'])
for opening in ('C', 'D'):
    for end in (None, 980, 990, 991, 993, 996, 999, 1000):
        key = f'tft_{opening}_{end or "none"}'
        profile(key, opening, end,
                [f'{opening} inicial.', *([f'D desde ronda {end}, con prioridad sobre copia.'] if end else []),
                 'En las demás rondas, copiar la última acción del rival.'],
                ['Inicio; tras C; tras D; perdón inmediato tras DC del rival.',
                 f'Frontera {end-1}/{end} con rival cooperador.' if end else 'Ronda 1000 tras C debe dar C, sin final añadido.'])
for end, pct in ((980,15),(980,10),(996,15)):
    profile(f'fraction_D_{pct}_{end}', 'D', end,
            ['D inicial.', f'D si la última acción rival es D, o ronda >= {end}, o fracción histórica rival de D > {pct}%.',
             'C en otro caso. El porcentaje se recalcula; no hay bloqueo irreversible.'],
            [f'Fracción exactamente {pct}% frente a superior, con última acción C.',
             'Denominador = rondas ya jugadas; volver a C si baja el porcentaje y no aplica otra regla.', f'Frontera {end-1}/{end}.'])
for threshold, inclusive, end in ((10,False,996),(20,True,990)):
    op = '>=' if inclusive else '>'
    profile(f'score_{threshold}_{end}', 'D', end,
            ['D inicial.', f'D si la última acción rival es D, o ronda >= {end}, o puntuación propia menos rival {op} {threshold}.', 'C en otro caso.'],
            [f'Diferencia exactamente {threshold} y a ambos lados; evaluar puntuaciones tras las rondas completadas.',
             'Con pagos clásicos, diferencia = 5 × (DC − CD). No redondear ni comparar porcentajes.', f'Frontera {end-1}/{end}.'], 'scores_from_completed_history')
for threshold, inclusive, latch, end in ((60,True,True,998),(60,True,False,None),(55,False,True,None),
                                        (50,False,False,None),(70,True,False,None)):
    key = f'fraction_C_{threshold}_{"ge" if inclusive else "gt"}_{"latch" if latch else "current"}'
    op = '>=' if inclusive else '>'
    profile(key, 'C', end,
            ['C inicial.', f'D si la fracción histórica rival de D {op} {threshold}%.' + (' Una vez activada, D hasta el final aunque la fracción baje.' if latch else ' Recalcular en cada ronda; no hacer permanente.'),
             *([f'D desde ronda {end}.'] if end else []), 'D si el rival jugó D antes; C en otro caso.'],
            [f'Igualdad al {threshold}% y a ambos lados; última acción C para aislar el umbral.',
             'Historial que cruce el umbral y luego baje: comprobar permanencia.' if latch else 'Historial que baje del umbral: comprobar recuperación de C.',
             'Inicio sin división por cero.'], 'prefix_trigger_or_persistent_flag' if latch else 'history_only')
profile('window8of10', 'C', None,
        ['C inicial.', 'D si hay al menos 8 D en las últimas 10 rondas; con menos de 10 rondas, esa condición no se activa bajo la convención v1.',
         'Si no se activa, copiar la última acción del rival.'],
        ['7/10 frente a 8/10, con última acción C.', 'Historial de 9 rondas DDDDDDDDC: C bajo ventana completa; probar la frontera al completar 10.'])
profile('anti_tft', 'D', None, ['D inicial; D tras C rival y C tras D rival.'], ['Inicio D; C rival→D; D rival→C; final sin excepción.'])
profile('anti_tft_latch3', 'D', None,
        ['D inicial.', 'Tras la primera racha de al menos tres D rivales, D permanentemente.', 'Antes de activarse: D tras C rival y C tras D rival.'],
        ['Racha DD aún devuelve C; DDD activa D; DDDCC seguido por D conserva D.', 'Comprobar que no se limita a mirar la última racha.'], 'prefix_trigger_or_persistent_flag')
profile('dd_to_c', 'D', None, ['D inicial.', 'C solo si ambos jugaron D en la ronda previa; D en los otros tres pares.'],
        ['Tabla de las cuatro parejas CC, CD, DC, DD.', 'No convertir en antitit-for-tat: tras CD debe dar D.'])
profile('probe3_D_final', 'D', 1000,
        ['D final; D inicial; D tras D rival; D tras tres C rivales consecutivas; C en otro caso.'],
        ['Inicio D; 2 C previas→C; 3 C previas→D; final D; perdón tras DC del rival.'])
profile('two_total_D', 'C', 995,
        ['D desde 995; D si rival acumula al menos dos D; D si última acción rival D; C en otro caso, incluido inicio.'],
        ['Una D seguida de C permite C; dos D no consecutivas seguidas de C mantienen D.', 'Frontera 994/995.'])
profile('two_lags_probe10', 'C', 998,
        ['D desde 998; D si el rival jugó D hace una ronda; D si jugó D hace dos rondas;',
         'D tras diez C rivales consecutivas; C en otro caso, incluido inicio.'],
        ['Ronda 2 tras D→D: el lag1 está explícito.', 'Racha 9/10 C; un D de hace dos rondas; D de hace tres ya no activa represalia.', 'Frontera 997/998.'])
profile('cyclebreak_probe3', 'C', 1000,
        ['D final; C si hubo DD mutuo en cada una de las dos rondas previas;',
         'D si última acción rival D; D tras tres C rivales consecutivas; C en otro caso, incluido inicio.'],
        ['Dos DD mutuos→C antes que la represalia; un DD mutuo→D.', 'Racha 2/3 C; en final D prevalece incluso sobre dos DD.'])


def build_decisions(old_ids):
    decisions = {}
    def add(model, attitude, numbers, key, note='', status='eligible_prose', witness=None):
        for n in numbers:
            sid = f'{model}/default/{attitude}_{n}'
            if sid in old_ids:
                continue
            if sid in decisions:
                raise ValueError('Duplicate manual assignment: '+sid)
            decisions[sid] = {'status': status, 'profile_key': key, 'rationale_es': note,
                              'unresolved_witness': witness}
    a = 'anthropic_sonnet46'
    add(a,'Aggressive',[1,6,8,14,15],'always_d','Se siguen las acciones explícitas, no el título Tit-for-Tat ni las afirmaciones generales de optimalidad.')
    add(a,'Aggressive',[9,10,16,18],'tft_D_none')
    add(a,'Aggressive',[3,25],'tft_D_980')
    add(a,'Aggressive',[4],'tft_D_990')
    add(a,'Aggressive',[17],'tft_D_990','Regla operativa: ronda 990 o posterior (11 rondas). La explicación dice «final ten»; se conserva el umbral numérico explícito y se declara la discrepancia.')
    add(a,'Aggressive',[5,12,22],'tft_D_996','El carácter dañado entre 996 y 1000 no impide leer «final 5 rounds» y los extremos; no se repara el texto original.')
    add(a,'Aggressive',[20],'tft_D_996','Convención explícita de preparación: rondas restantes incluyen la ronda actual aún no jugada, 1000−len(historial). Con cinco o menos: 996–1000. Registrar la convención en la conversión ampliada.')
    add(a,'Aggressive',[21],'tft_D_993','Convención: rondas restantes incluyen la actual, 1000−len(historial); ocho o menos corresponde a 993–1000. Registrar en el contrato ampliado.')
    add(a,'Aggressive',[2],'score_10_996')
    add(a,'Aggressive',[24],'score_20_990')
    add(a,'Aggressive',[7,23],'fraction_D_15_980')
    add(a,'Aggressive',[13],'fraction_D_10_980')
    add(a,'Aggressive',[19],'fraction_D_15_996')
    add(a,'Cooperative',[1,3,4,5,9,11,12,13,16,17,18,22,23,24,25],'tft_C_991')
    add(a,'Cooperative',[6,7,8,10,14,15,19,20,21],'tft_C_996')
    add(a,'Neutral',[1,2,4,5,7,8,9,13,15,16,19,20,22,24,25],'tft_C_none')
    add(a,'Neutral',[12,14,17],'tft_C_1000')
    add(a,'Neutral',[3],'fraction_C_60_ge_latch','La permanencia requiere conservar el primer cruce del umbral, no solo comprobar el porcentaje actual.')
    add(a,'Neutral',[10],'fraction_C_60_ge_current')
    add(a,'Neutral',[11],'fraction_C_55_gt_latch','El comparador es estrictamente mayor que 55%; el bloqueo es irreversible.')
    add(a,'Neutral',[18],'fraction_C_50_gt_current','Mayoría estricta: más de la mitad; empate no activa la primera condición.')
    add(a,'Neutral',[21],'window8of10','Aplica la convención v1 de historial completo para una ventana que pide 10 rondas; guardar la expectativa de ronda 10 con solo 9 previas.')
    add(a,'Neutral',[23],'fraction_C_70_ge_current')
    f = 'gemini_25_flash'
    add(f,'Aggressive',[1,3,4,5,7,8,9,10,11,12,13,15,17,18,19,20,21],'always_d')
    add(f,'Aggressive',[14],'c_then_d','La primera acción es C aunque la actitud se llame agresiva; después siempre D.')
    add(f,'Aggressive',[16],'anti_tft_latch3','La excepción permanente tiene prioridad por «However»; no es una represalia de solo tres rondas.')
    add(f,'Aggressive',[22],'anti_tft')
    add(f,'Aggressive',[23],'tft_D_none')
    add(f,'Aggressive',[25],'dd_to_c')
    for attitude in ('Cooperative','Neutral'):
        add(f,attitude,range(1,26),'tft_C_none')
    g = 'gemini_31_pro'
    add(g,'Aggressive',[2],'probe3_D_final','No se adopta la promesa explicativa de obtener 5 en el inicio: la regla solo fija D.')
    add(g,'Aggressive',[4],'tft_C_999')
    add(g,'Aggressive',[6],'two_total_D')
    for n,end in ((12,998),(14,996)):
        add(g,'Aggressive',[n],None,
            f'D desde {end}; D si aparece D en «either» de las dos rondas anteriores; C en otro caso. No fija si basta una ronda disponible o se necesita la ventana completa. La convención genérica v1 exige dos; la lectura de «either» puede activar represalia inmediata.',
            'needs_window_adjudication', {'own':'C','opponent':'D','round':2,'expected_action':None,
             'alternatives':{'available_history':'D','full_two_round_window':'C'},
             'proposal':'Usar historial disponible para disyunción «either»; requiere enmienda explícita, no aplicarla silenciosamente.'})
    add(g,'Aggressive',[20],None,
        'Nuevo corte no detectado por la heurística: termina en «4. **». Falta la cuarta regla y el caso base tras una D antigua seguida de C. Tampoco fija inequívocamente la primera acción ante historial vacío.',
        'blocked_incomplete_rules', {'own':'DD','opponent':'DC','round':3,'expected_action':None,
                                    'reason':'No aplica final, rival ya no siempre C, última acción rival C: falta regla 4.'})
    add(g,'Aggressive',[24],'two_lags_probe10','Termina en «**», pero la regla 5 cubre explícitamente todos los casos restantes. Residuo de formato no equivale a política incompleta; no completar texto.')
    add(g,'Aggressive',[25],'cyclebreak_probe3')
    add(g,'Cooperative',range(1,26),'tft_C_1000')
    add(g,'Neutral',[n for n in range(1,26) if n!=20],'tft_C_1000')
    add(g,'Neutral',[20],'tft_C_none','Excepción dentro del grupo: copia al rival también en ronda 1000; no añadir D final.')
    o = 'openai_gpt54mini'
    add(o,'Aggressive',[1,2,3,4,7,8,10,11,13,15,18,19,21,24,25],'always_d',
        'Las acciones son siempre D. Las referencias de 18 y 21 a reglas externas no añaden una acción en el juego clásico sin esa regla externa.')
    add(o,'Aggressive',[14],'tft_D_none','Tras C rival, C; la excepción «unless they cooperate again» permite cooperación sostenida. No alternar C/D automáticamente.')
    issues = {
        5: ('No define cuánto dura «long streak» ni cuándo se necesita probar cooperación; la excepción no se puede reemplazar por siempre D.', 'D'*10,'D'*10),
        6: ('«Only consider C if needed» deja indeterminados necesidad, disparador y acción de sondeo pese a las reglas previas de D.', 'D'*5,'D'*5),
        12: ('Faltan el número de C consecutivas en «several rounds» y el inicio de «final rounds».', 'DDD','CCC'),
        16: ('Sondeo opcional tras D rival entra en tensión con «D for the rest of the game» tras cualquier D; no fija disparador ni precedencia.', 'DD','DD'),
        17: ('«Several recent rounds», deseo de probar y «final rounds» no tienen umbrales; no se determina el primer sondeo.', 'DDD','CCC'),
        20: ('La excepción de probar cooperación tras «long run of mutual D» no define longitud ni cuándo elegirla.', 'D'*10,'D'*10),
        22: ('No existe criterio observable de certeza sobre cooperación durante el resto del juego. No se puede convertir esa condición en falsa por decisión del conversor.', 'DDD','CCC'),
        23: ('No fija cuándo cooperar es «clearly necessary» ni cuántas rondas son «several». La frase final sobre pagos no resuelve la regla.', 'D'*10,'D'*10),
    }
    for n,(reason,own,opp) in issues.items():
        add(o,'Aggressive',[n],None,reason,'blocked_underspecified_rules',
            {'own':own,'opponent':opp,'round':len(own)+1,'expected_action':None,
             'reason':'El texto permite o contempla una excepción de C sin criterio ejecutable inequívoco.'})
    add(o,'Cooperative',range(1,26),'tft_C_none',
        'C inicial y copia del rival; regreso a C condicionado a C rival. «One-round punishment» no añade perdón automático si sigue llegando D.')
    add(o,'Neutral',[n for n in range(1,26) if n not in (17,24)],'tft_C_none',
        'La regla operativa y los resúmenes ordenan copiar la última acción rival; frases condicionales redundantes no cambian C tras C ni D tras D.')
    add(o,'Neutral',[17],'tft_D_none','Inicio D y copia posterior; ausencia de historia se trata con D. La etiqueta neutral no implica inicio C.')
    add(o,'Neutral',[24],'always_d','La regla explícita es siempre D, aunque la etiqueta sea neutral.')
    return decisions


def main():
    inputs = ROOT/'phase3/inputs'
    manifest_path = inputs/'manifest.json'
    old_path = inputs/'semantic_review_v1.json'
    manifest = json.loads(manifest_path.read_bytes())
    old = json.loads(old_path.read_bytes())
    old_ids = {r['id'] for r in old['cases']}
    models = ('anthropic_sonnet46','gemini_25_flash','gemini_31_pro','openai_gpt54mini')
    libs = [l for l in manifest['libraries'] if l['prompt']=='default' and l['model'] in models]
    decisions = build_decisions(old_ids)
    expected = {s['id'] for l in libs for s in l['strategies']} - old_ids
    if set(decisions)!=expected or len(expected)!=270:
        raise ValueError(f'Coverage mismatch: missing={expected-set(decisions)}, extra={set(decisions)-expected}')
    records = []
    for lib in libs:
        path = ROOT/lib['snapshot_path']
        if sha(path.read_bytes()) != lib['sha256']:
            raise ValueError('Snapshot changed')
        for original in lib['strategies']:
            sid = original['id']
            if sid not in expected:
                continue
            prose = extract_comment(path, original['class'])
            if sha(prose.encode()) != original['prose_sha256']:
                raise ValueError('Prose hash mismatch: '+sid)
            d = decisions[sid]
            spec = PROFILES[d['profile_key']] if d['profile_key'] else None
            rationale = d['rationale_es'] or ('Reglas suficientemente determinadas: '+' '.join(spec['ordered_rules_es']))
            record = {'id':sid, 'status':d['status'], 'profile_key':d['profile_key'],
                      'rationale_es':rationale, 'operational_review':spec,
                      'unresolved_witness':d['unresolved_witness'],
                      'prose_exact_extracted':prose, 'prose_sha256':original['prose_sha256'],
                      'snapshot_path':lib['snapshot_path'], 'snapshot_sha256':lib['sha256'],
                      'source_commit':lib['source_commit'], 'previous_heuristic_flags':original['flags'],
                      'unicode_replacement_characters':prose.count('\ufffd'),
                      'source_code_consulted_for_missing_rules':False, 'conversion_performed':False}
            if record['unresolved_witness']:
                w=record['unresolved_witness']
                assert len(w['own'])==len(w['opponent'])==w['round']-1
                w['scope']='Historia contrafactual; no se afirma alcanzabilidad bajo una política incompleta.'
            records.append(record)
    combined = old['cases']+records
    statuses = Counter(r['status'] for r in records)
    totals = Counter(r['status'] for r in combined)
    summary_by_model = {model:dict(Counter(r['status'] for r in records if r['id'].startswith(model+'/'))) for model in models}
    groups = defaultdict(list)
    for r in records:
        if r['profile_key']:
            groups[r['profile_key']].append(r['id'])
    report = {'schema':1, 'date':'2026-09-13',
              'reviewer':'Codex assistant; full reading of 270 extracted texts, one review, no independent adjudication',
              'scope':'Remaining Western Default descriptions only; no Chinese/Prose/Refine review here.',
              'source_hashes':{'manifest':sha(manifest_path.read_bytes()),'prior_review':sha(old_path.read_bytes()),
                               'review_script':sha(Path(__file__).read_bytes())},
              'conventions_es':['Historial solo de rondas completadas; ronda actual = longitud + 1.',
                                'Prevalecen reglas operativas numéricas y excepciones explícitas sobre títulos y explicaciones.',
                                'Rondas restantes = rondas no jugadas, incluida la actual. Esta aclaración debe constar en el contrato ampliado.',
                                'Ventana completa para una condición que requiere k observaciones según v1; dos disyunciones «either» se reservan para adjudicación por ambigüedad.',
                                'Fracciones sobre todas las rondas previas; > estricto, al menos >=, mayoría >50%.',
                                'Una orden de D para el resto del juego persiste aun cuando desaparezca el disparador.',
                                'No se corrigen caracteres dañados ni se completan reglas ausentes.'],
              'summary':dict(statuses), 'by_model':summary_by_model, 'combined_300_summary':dict(totals),
              'profile_groups':dict(groups), 'cases':records, 'api_calls':0,
              'limitations':['Eligibility is conditional on declared interpretations, not proof of generated-code fidelity.',
                             'Profile labels summarize prose; no claim of equivalence of archived or future programs.',
                             'No deductions from payoffs or generated implementations were used to fill gaps.']}
    save_new_or_identical(inputs/'semantic_review_remaining_v1.json',report)
    # Proposal only: references original review for the 30 older cases. Preserve
    # every identity even when prose describes the same policy; no deduplication.
    pilot_ids = {r['id'] for r in old['cases'] if r['cohort']=='pilot'}
    cohort = {'status':'proposed_eligible_inputs_not_authorization_to_send', 'api_calls':0,
              'review_sha256':sha((inputs/'semantic_review_remaining_v1.json').read_bytes()),
              'prior_review_sha256':sha(old_path.read_bytes()),
              'cases':[{'id':r['id'],'prose_sha256':r['prose_sha256'], 'snapshot_path':r['snapshot_path'],
                        'snapshot_sha256':r['snapshot_sha256'], 'already_in_completed_pilot':r['id'] in pilot_ids,
                        'review_source':'semantic_review_v1.json' if r['id'] in old_ids else 'semantic_review_remaining_v1.json'}
                       for r in combined if r['status']=='eligible_prose'],
              'excluded_pending_resolution':[{'id':r['id'],'status':r['status']} for r in combined if r['status']!='eligible_prose']}
    save_new_or_identical(inputs/'western_default_eligibility_v1.json',cohort)
    print(json.dumps({'reviewed':len(records),'new_summary':dict(statuses),'by_model':summary_by_model,
                      'combined_300':dict(totals),'eligible_not_in_pilot':sum(not r['already_in_completed_pilot'] for r in cohort['cases']),
                      'api_calls':0},ensure_ascii=False))


if __name__=='__main__':
    main()
