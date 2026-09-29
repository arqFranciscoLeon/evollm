"""Materialize one assistant's full-text review of 300 Chinese Default descriptions.

Manual profile assignments below are derived from prose, not automated text
classification. Source inspection is not independent/blinded adjudication.
"""
import ast
from collections import Counter
import json
from pathlib import Path
from phase3.review_semantics import extract_comment
from phase3.pilot_converter import ROOT, sha, encoded, exclusive, now

MODELS=('deepseek_v4pro','qwen3max','kimi_k25','glm_51')
PROFILES={}
for model in MODELS:
    for attitude in ('Aggressive','Cooperative','Neutral'):
        for i in range(1,26):
            PROFILES[f'{model}/default/{attitude}_{i}']='tft_C_none'

def assign(model,attitude,profile,indices):
    for i in indices:
        PROFILES[f'{model}/default/{attitude}_{i}']=profile

assign('qwen3max','Aggressive','always_d',range(1,26))
assign('deepseek_v4pro','Aggressive','always_d',[1,3,6,8,11,17,20,21,22,25])
assign('deepseek_v4pro','Aggressive','anti',[2,12])
assign('deepseek_v4pro','Aggressive','tft_D_none',[4,9,10,13,18,23,24])
assign('deepseek_v4pro','Aggressive','pending',[5])
assign('deepseek_v4pro','Aggressive','dd_D_none',[7])
assign('deepseek_v4pro','Aggressive','grim_D',[14])
assign('deepseek_v4pro','Aggressive','wsls_D_none',[15,16])
assign('deepseek_v4pro','Aggressive','twoC_elseD',[19])
assign('deepseek_v4pro','Cooperative','wsls_C_none',[2,7,11,12,17,19,24])
assign('deepseek_v4pro','Cooperative','tft_C_1000',[3,5])
assign('deepseek_v4pro','Cooperative','forgiving_DD',[4,20])
assign('deepseek_v4pro','Cooperative','twoD',[16,21])
assign('deepseek_v4pro','Neutral','twoD_second_tft',[1])
assign('deepseek_v4pro','Neutral','wsls_C_none',[2,5,7,9,10,14,15,18,19])
assign('deepseek_v4pro','Neutral','ratio15_DD10',[3])
assign('deepseek_v4pro','Neutral','twoD',[4])
assign('deepseek_v4pro','Neutral','wsls_C_1000',[8])
assign('deepseek_v4pro','Neutral','forgiving_DD',[16])
assign('deepseek_v4pro','Neutral','tft_C_1000',[20])
assign('kimi_k25','Aggressive','tft_D_none',[1,2,4,5,6,8,10,14,19,20,23,24])
assign('kimi_k25','Aggressive','trust3_991',[3])
assign('kimi_k25','Aggressive','switch100',[7])
assign('kimi_k25','Aggressive','dd_latch_1000',[9])
assign('kimi_k25','Aggressive','dd_D_none',[11])
assign('kimi_k25','Aggressive','pending',[12,25])
assign('kimi_k25','Aggressive','probe10_once',[13])
assign('kimi_k25','Aggressive','keepCC_elseD',[15,21])
assign('kimi_k25','Aggressive','tft_D_1000',[16,18])
assign('kimi_k25','Aggressive','trust5',[17])
assign('kimi_k25','Aggressive','always_d',[22])
assign('kimi_k25','Cooperative','tft_C_1000',[5,7,8,11,13,16,18])
assign('kimi_k25','Neutral','tft_C_1000',[3,10,13,23])
assign('kimi_k25','Neutral','tft_C_999',[8])
for profile,indices in {
    'anti991':[1],'probeDC2':[2],'baitDDD':[3],'afterDDD':[4],
    'dd_D_991':[5],'always_d':[6,8,10,21,24],'probeDC_lock':[7],
    'afterDD10':[9],'probeDD_CC':[11],'dd_D_none':[12,16,18],
    'dd_C_991':[13],'DD2_unlessD5':[14],'probeDD_C':[15],
    'dd_D_1000':[17],'treeCDC':[19],'pending':[20],
    'firstD_twoC':[22],'probeDCC':[23],'ownD5':[25],
}.items(): assign('glm_51','Aggressive',profile,indices)
assign('glm_51','Cooperative','tft_C_1000',[4,5,7,10,12,16,19])
assign('glm_51','Cooperative','forgiving_DD',[13])
assign('glm_51','Neutral','tft_C_1000',[4,16,20,23,24])
assign('glm_51','Neutral','wsls_C_none',[7,10])

PENDING={
 'deepseek_v4pro/default/Aggressive_5':('blocked_underspecified_rules','Ronda 2 tras C rival: no existe la ronda anterior requerida por las ramas de dos observaciones y no hay caso por defecto. No se toma la D del código como regla de la prosa.'),
 'kimi_k25/default/Aggressive_12':('needs_transition_adjudication','Tras una o dos C iniciales rivales, antes de completar tres, no se explicita la acción. Mantener D sería una interpretación adicional; además se debe separar D temporal antes de cooperar de D permanente después.'),
 'kimi_k25/default/Aggressive_25':('needs_timing_adjudication','«Immediately after you play Cooperate» puede referirse al par simultáneo anterior o a la respuesta rival en la ronda siguiente. Falta fijar esa relación temporal antes de certificar fidelidad.'),
 'glm_51/default/Aggressive_20':('needs_threshold_adjudication','«This is the tenth consecutive round of mutual cooperation» puede contar nueve rondas completadas más la actual o diez completadas. Se reserva la decisión; no se copia el umbral del código.'),
}
NOTES={
 'deepseek_v4pro/default/Aggressive_2':'Las ramas explícitas C->D y D->C prevalecen sobre el verbo genérico copy, conforme al criterio occidental; se registra el conflicto textual.',
 'deepseek_v4pro/default/Aggressive_19':'La condición de dos C requiere dos observaciones; otherwise D cubre historial vacío y una observación.',
 'deepseek_v4pro/default/Cooperative_3':'La excepción explícita final «regardless» prevalece sobre la enumeración previa.',
 'deepseek_v4pro/default/Neutral_3':'Ventana de diez completa; >15% es estricto. Antes de diez rondas, cualquier par DD ya supera 15%, por lo que la otra condición puede enmascarar la diferencia de ventana.',
 'kimi_k25/default/Aggressive_13':'La excepción cooperate once después de diez DC es un único sondeo; ambas respuestas posteriores conducen a D permanente. No se presupone efecto causal de una acción simultánea.',
 'kimi_k25/default/Aggressive_17':'Switch to cooperation se interpreta como cambio de estado hasta la defección rival; la orden de D para el resto es irreversible.',
 'glm_51/default/Aggressive_3':'Cooperate exactly once y then D obliga una ronda D posterior antes de reevaluar; no se inventa una pausa más larga.',
 'glm_51/default/Aggressive_9':'Diez DD consecutivos anteriores se operacionaliza como ventana inmediatamente anterior de diez rondas, siguiendo la convención de rachas.',
}

def main():
    manifest_path=ROOT/'phase3/inputs/manifest.json'
    manifest=json.loads(manifest_path.read_bytes()); cases=[]; sources={}
    for lib in manifest['libraries']:
        if lib['model'] not in MODELS or lib['prompt']!='default': continue
        path=ROOT/lib['snapshot_path']; data=path.read_bytes()
        if sha(data)!=lib['sha256']: raise ValueError('Archived library changed')
        sources[lib['snapshot_path']]={'sha256':sha(data),'source_commit':lib['source_commit'],'source_path':lib['source_path']}
        tree=ast.parse(data.decode('utf-8-sig'))
        classes={n.name:n for n in tree.body if isinstance(n,ast.ClassDef)}
        for record in lib['strategies']:
            strategy_id=record['id']; prose=extract_comment(path,record['class'])
            if sha(prose.encode())!=record['prose_sha256']: raise ValueError('Prose changed')
            cls=classes[record['class']]
            method=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='strategy')
            source=ast.get_source_segment(data.decode('utf-8-sig'),method)
            profile=PROFILES[strategy_id]
            status,note=PENDING.get(strategy_id,('eligible_prose',NOTES.get(strategy_id,'Reglas operativas completas bajo las convenciones declaradas; perfil asignado por lectura integral.')))
            cases.append({'id':strategy_id,'status':status,'profile':profile,'review_note_es':note,
                          'prose':prose,'prose_sha256':sha(prose.encode()),'library_path':lib['snapshot_path'],
                          'library_sha256':sha(data),'class_line':cls.lineno,'method_source_sha256':sha(source.encode()),
                          'replacement_characters':prose.count(chr(65533)),'visible_truncation_detected':False,
                          'archived_code_fidelity':'separate_validation_required'})
    if len(cases)!=300 or {r['id'] for r in cases}!=set(PROFILES): raise ValueError('Incomplete manual review coverage')
    report={'created_at':now(),'reviewer':'Codex assistant; full reading of all 300 texts, single review, not independent/blinded adjudication',
            'scope':'Chinese Default only; no Prose/Refine or API requests',
            'manifest_sha256':sha(manifest_path.read_bytes()),'review_script_sha256':sha(Path(__file__).read_bytes()),
            'sources':sources,'conventions':'Operational branches and explicit exceptions override titles/general summaries; current round = completed + 1; full fixed windows; irreversible remainder-of-game switches; no missing rule inferred from code.',
            'summary':dict(Counter(r['status'] for r in cases)),
            'by_model':{m:dict(Counter(r['status'] for r in cases if r['id'].startswith(m+'/'))) for m in MODELS},
            'cases':cases,'api_calls':0,'ready_for_tournament':False}
    exclusive(ROOT/'phase3/inputs/semantic_review_chinese_v1.json',encoded(report))
    print(json.dumps(report['summary']))

if __name__=='__main__': main()
