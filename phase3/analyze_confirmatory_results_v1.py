"""Post-tournament analysis from the frozen, fully verified receipt schedule.

Runs only the prespecified primary H7 test and descriptive secondary analyses.
It does not upload or publish results.
"""
import gc
import hashlib
import json
from pathlib import Path

import numpy as np

from phase3.analyze_phase3 import ATTITUDES, h7_statistic, permutation_test
from phase3.execute_uniform import load_field
from phase3.interpretation_sensitivity_v1 import load_scenario
from phase3.reuse_batches_v1 import export_scenario
from phase3.sensitivity_analysis_v1 import ast_group, duplicate_sensitivity, exclusion_bounds
from phase3.verify_modal_wave_v1 import verify

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / 'phase3'
PLAN = PHASE / 'reuse_plan_v1'
VALIDATION = PHASE / 'validation'
OUT = VALIDATION / 'confirmatory_analysis_v1.json'
REPORT = PHASE / 'CONFIRMATORY_RESULTS_v1.md'
EXPECTED_COMMIT = '18cb41744f3f1e66fe711aad09697980476c2498'
EXPECTED_REGISTRATION = 'https://osf.io/2nzdh/overview'
EXPECTED_CONTEXT = '3811e2f65857b46003a48ddedbc0f625c1a9e573207987787f7a5f78b01d1bfd'
EXPECTED_MANIFEST = '2dbcfc56965bd025ca2f4eb9ca2351099f5fd34101fbbd7af82fee9a43bb3ba6'
EXPECTED_FIELD = 'd5725c7a63125a0cbdee1ddc24e4d2731dc60f6ad0734d3c670d5b23f9181062'
EXPECTED_SENSITIVITY_PLAN = '361d3ade33783e972c8f0fcfe99d285e230e02a696ce0f44a1d9a5fb3154afc7'
EXPECTED_ANALYZER = '36f0d0e049306f7f5fb13bf8172fb01e9c79b2da2265dc0f28c60e039f6f37d2'
EXPECTED_SENSITIVITY = '4392ed8755e1bd2054ec7d4c88acaadc8a15f49cf2c27b6ac05f1b7756b8d833'


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verified_batches(manifest):
    for index, entry in enumerate(manifest['batches']):
        batch_path = PLAN / entry['path']
        receipt_path = VALIDATION / f'modal_confirmatory_batch_{index:04d}_receipt.json'
        batch = json.loads(batch_path.read_bytes())
        receipt = json.loads(receipt_path.read_bytes())
        yield batch, receipt


def descriptive_tables(matrix):
    ids = matrix['ids']
    models = matrix['models']
    attitudes = matrix['attitudes']
    c = matrix['cooperation']
    payoff = matrix['payoff']
    n = len(ids)
    labels = sorted(set(models))
    others = ~np.eye(n, dtype=bool)
    focal_c = (c * others).sum(axis=1) / (n - 1)
    focal_p = (payoff * others).sum(axis=1) / (n - 1)
    cells = []
    autopairs = []
    for model in labels:
        for attitude in ATTITUDES:
            ix = [i for i, (m, a) in enumerate(zip(models, attitudes)) if m == model and a == attitude]
            cells.append({
                'model': model, 'attitude': attitude, 'strategies': len(ix),
                'mean_mutual_cooperation_vs_all_other_identities': float(focal_c[ix].mean()),
                'mean_focal_payoff_vs_all_other_identities': float(focal_p[ix].mean()),
            })
            autopairs.append({
                'model': model, 'attitude': attitude, 'strategies': len(ix),
                'mean_self_play_cooperation': float(np.diag(c)[ix].mean()),
                'mean_self_play_payoff': float(np.diag(payoff)[ix].mean()),
            })

    mixes = {
        'balanced': (1/3, 1/3, 1/3),
        'aggressive_dominant': (2/3, 1/6, 1/6),
        'cooperative_dominant': (1/6, 2/3, 1/6),
        'neutral_dominant': (1/6, 1/6, 2/3),
    }
    attitude_index = {a: i for i, a in enumerate(ATTITUDES)}
    n_models = len(labels)
    rows = []
    for mix_name, weights in mixes.items():
        cvals = np.zeros(n)
        pvals = np.zeros(n)
        for focal in range(n):
            for attitude, weight in zip(ATTITUDES, weights):
                for model in labels:
                    rivals = [j for j, (m, a) in enumerate(zip(models, attitudes))
                              if m == model and a == attitude and j != focal]
                    if not rivals:
                        raise ValueError(f'Empty counterfactual opponent cell: {model}/{attitude}')
                    w = weight / n_models
                    cvals[focal] += w * float(c[focal, rivals].mean())
                    pvals[focal] += w * float(payoff[focal, rivals].mean())
        for model in labels:
            for attitude in ATTITUDES:
                ix = [i for i, (m, a) in enumerate(zip(models, attitudes)) if m == model and a == attitude]
                rows.append({
                    'mix': mix_name, 'model': model, 'focal_attitude': attitude,
                    'strategies': len(ix),
                    'mean_mutual_cooperation': float(cvals[ix].mean()),
                    'mean_focal_payoff': float(pvals[ix].mean()),
                })
    return {'model_attitude': cells, 'autopairs': autopairs, 'counterfactual_mixes': rows}


def run():
    if OUT.exists() or REPORT.exists():
        raise FileExistsError('Analysis output exists; inspect before rerunning')
    registration = json.loads((PHASE / 'registration_v1/public_registration.json').read_bytes())
    if (registration.get('public_registration_url') != EXPECTED_REGISTRATION
            or registration.get('frozen_git_commit') != EXPECTED_COMMIT
            or registration.get('context_sha256') != EXPECTED_CONTEXT
            or registration.get('plan_manifest_sha256') != EXPECTED_MANIFEST
            or not registration.get('public_visibility_verified_at_utc')):
        raise ValueError('Public registration/frozen commit gate failed')
    if file_sha(PHASE / 'analyze_phase3.py') != EXPECTED_ANALYZER:
        raise ValueError('Prespecified H7 analyzer hash mismatch')
    if file_sha(PHASE / 'sensitivity_analysis_v1.py') != EXPECTED_SENSITIVITY:
        raise ValueError('Prespecified sensitivity code hash mismatch')
    field_manifest = PHASE / 'validation/uniform_derived_candidates_v1.json'
    sensitivity_plan = PHASE / 'inputs/sensitivity_plan_v1.json'
    if file_sha(field_manifest) != EXPECTED_FIELD or file_sha(sensitivity_plan) != EXPECTED_SENSITIVITY_PLAN:
        raise ValueError('Frozen field or sensitivity plan hash mismatch')

    context = json.loads((PLAN / 'context.json').read_bytes())
    manifest_raw = (PLAN / 'manifest.json').read_bytes()
    manifest = json.loads(manifest_raw)
    if (file_sha(PLAN / 'manifest.json') != EXPECTED_MANIFEST
            or context.get('scope') != 'full_round_robin'
            or context.get('context_sha256', EXPECTED_CONTEXT) != EXPECTED_CONTEXT
            or len(manifest['batches']) != 665):
        raise ValueError('Frozen 665-batch execution plan mismatch')

    verified = verify(tuple(range(665)))
    if (verified['matches'] != 166172 or verified['logical_scenario_results'] != 2622048
            or verified['errors']):
        raise ValueError('Complete verified schedule gate failed')

    receipt_rows = []
    for index in range(665):
        path = VALIDATION / f'modal_confirmatory_batch_{index:04d}_receipt.json'
        receipt_rows.append((index, file_sha(path)))
    receipt_inventory_sha = hashlib.sha256(json.dumps(receipt_rows, separators=(',', ':')).encode()).hexdigest()
    base = load_field()
    scenario_results = []
    primary_matrix = None
    for mask in range(16):
        field = load_scenario(mask, primary=base)
        matrix = export_scenario(context, mask, verified_batches(manifest))
        effect = h7_statistic(matrix['cooperation'], matrix['models'], matrix['attitudes'])
        matrix_sha = hashlib.sha256(
            json.dumps(matrix['ids'], separators=(',', ':')).encode()
            + np.asarray(matrix['cooperation'], dtype='<f8').tobytes()
        ).hexdigest()
        scenario_results.append({'mask': mask, 'difference': effect,
                                 'difference_pp': 100 * effect,
                                 'matrix_sha256': matrix_sha,
                                 'source_manifest_sha256': field.provenance['manifest_sha256']})
        if mask == 0:
            primary_matrix = matrix
        del field, matrix
        gc.collect()

    assert primary_matrix is not None
    primary_test = permutation_test(primary_matrix['cooperation'], primary_matrix['models'],
                                    primary_matrix['attitudes'], permutations=10000, seed=20260913)
    source_groups = [ast_group((ROOT / base.records[sid]['source_path']).read_text(encoding='utf-8'))
                     for sid in primary_matrix['ids']]
    duplicate = duplicate_sensitivity(primary_matrix['cooperation'], primary_matrix['models'],
                                      primary_matrix['attitudes'], source_groups)
    bounds = exclusion_bounds(primary_matrix['cooperation'], primary_matrix['models'],
                              primary_matrix['attitudes'], target_per_cell=25)
    descriptives = descriptive_tables(primary_matrix)

    result = {
        'status': 'complete',
        'registration': {'url': EXPECTED_REGISTRATION, 'frozen_git_commit': EXPECTED_COMMIT,
                         'public_visibility_verified_at_utc': registration['public_visibility_verified_at_utc']},
        'provenance': {
            'context_sha256': EXPECTED_CONTEXT, 'batch_manifest_sha256': EXPECTED_MANIFEST,
            'field_manifest_sha256': EXPECTED_FIELD, 'sensitivity_plan_sha256': EXPECTED_SENSITIVITY_PLAN,
            'h7_analyzer_sha256': EXPECTED_ANALYZER, 'sensitivity_code_sha256': EXPECTED_SENSITIVITY,
            'receipts_verified': 665, 'receipt_inventory_sha256': receipt_inventory_sha,
        },
        'execution': {'computational_matches': verified['matches'],
                      'logical_scenario_results': verified['logical_scenario_results'],
                      'errors': 0, 'strategies': len(base.records),
                      'scenario_count': 16, 'matches_per_scenario_including_self': 163878},
        'primary_h7_scenario_0': primary_test,
        'scenario_sensitivity_all_16': scenario_results,
        'scenario_range': {'minimum_difference': min(x['difference'] for x in scenario_results),
                           'maximum_difference': max(x['difference'] for x in scenario_results),
                           'difference_from_primary': [x['difference'] - primary_test['difference'] for x in scenario_results],
                           'interpretation': 'Descriptive range across prespecified interpretation masks; not a confidence interval and no additional p-values.'},
        'duplicate_ast_sensitivity_scenario_0': duplicate,
        'missing_28_identity_bounds_scenario_0': bounds,
        'descriptive_primary_scenario_0': descriptives,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')
    report = [
        '# Resultados confirmatorios de la Fase 3', '',
        'Este informe presenta el análisis de la matriz completa ejecutada después del registro público. La inferencia se limita a las 572 identidades archivadas y a sus implementaciones verificadas. Las pruebas diagnósticas previas no se incorporaron.', '',
        f"- Registro: {EXPECTED_REGISTRATION}; commit congelado `{EXPECTED_COMMIT}`.",
        f"- Integridad: {verified['matches']:,} encuentros computacionales para {verified['logical_scenario_results']:,} resultados lógicos en 16 escenarios; 665/665 recibos válidos, cero errores.",
        f"- H7 primaria (máscara 0): diferencia {primary_test['difference']:.8f} ({primary_test['difference_pp']:.4f} puntos porcentuales), prueba unilateral por permutaciones p={primary_test['p_one_sided']:.5f} con 10.000 permutaciones; α=0,05.",
        f"- Intervalo de referencia nula 95 % (no es IC del efecto): [{primary_test['null_interval95'][0]:.8f}, {primary_test['null_interval95'][1]:.8f}].", '',
        '## Contraste principal por modelo y par de actitudes', '',
        '| Par de actitudes | Diferencia H7 |', '|---|---:|',
    ]
    labels = ['Aggressive/Aggressive', 'Aggressive/Cooperative', 'Aggressive/Neutral',
              'Cooperative/Cooperative', 'Cooperative/Neutral', 'Neutral/Neutral']
    report.extend(f"| {label} | {value:.8f} |" for label, value in zip(labels, primary_test['stratum_differences']))
    report += ['', '## Sensibilidad a las 16 interpretaciones', '',
               '| Máscara | H7 descriptiva | Diferencia frente a máscara 0 |', '|---:|---:|---:|']
    report.extend(f"| {x['mask']} | {x['difference']:.8f} | {x['difference']-primary_test['difference']:+.8f} |"
                  for x in scenario_results)
    report += ['', f"Rango de efectos: [{result['scenario_range']['minimum_difference']:.8f}, {result['scenario_range']['maximum_difference']:.8f}]. No es un intervalo de confianza; no se calcularon p-valores secundarios.", '',
               '## Sensibilidades prespecificadas', '',
               f"- Ponderación inversa por multiplicidad de AST: diferencia {duplicate['difference']:.8f} ({100*duplicate['difference']:.4f} pp); sin prueba adicional.",
               f"- Límites algebraicos para las 28 identidades excluidas: [{bounds['lower']:.8f}, {bounds['upper']:.8f}]; no son imputaciones ni intervalo de confianza.",
               '- El archivo JSON incluye los 24 estratos modelo×actitud, autoparejas por separado y las cuatro mezclas contrafactuales de actitudes, además de huellas de matrices y recibos.', '',
               '## Trazabilidad', '',
               f"- Inventario ordenado de huellas de los 665 recibos: `{receipt_inventory_sha}`.",
               f"- Salida JSON completa: `validation/{OUT.name}`.",
               '- El torneo completó 16 escenarios en un calendario con reutilización exacta por identidad, fuentes y contexto. Los resultados lógicos reconstruyen el calendario completo; no se multiplicaron observaciones de una misma partida compartida entre escenarios.', '',
    ]
    REPORT.write_text('\n'.join(report), encoding='utf-8')
    return result


if __name__ == '__main__':
    output = run()
    print(json.dumps({'status': output['status'],
                      'h7_difference': output['primary_h7_scenario_0']['difference'],
                      'p_one_sided': output['primary_h7_scenario_0']['p_one_sided'],
                      'scenarios': len(output['scenario_sensitivity_all_16']),
                      'matches': output['execution']['computational_matches'],
                      'logical_scenario_results': output['execution']['logical_scenario_results']}, indent=2))
