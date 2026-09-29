"""Summarize completed uniform validation without changing original evidence."""
import json
from collections import Counter
from phase3.pilot_converter import ROOT, exclusive, encoded, sha


def main():
    report = json.loads((ROOT / 'phase3/validation/uniform_v3b.json').read_bytes())
    receipt = json.loads((ROOT / 'phase3/validation/uniform_conversion_receipt_v3.json').read_bytes())
    rows = report['results']
    assert len(rows) == 572
    passed = sum(r['status'] == 'passed_targeted_checks' for r in rows)
    checks = sum(s['checks'] for r in rows for s in r['semantic'])
    games = [m for r in rows for m in r['runtime']]
    controls = [r['paired_raw_western_control'] for r in rows if 'paired_raw_western_control' in r]
    witnesses = []
    for row in rows:
        if row['status'] == 'passed_targeted_checks':
            continue
        reachable = [s for s in row['semantic'] if s['mode'] == 'candidate_on_policy' and s['failures']]
        selected = min(reachable, key=lambda s: s['failures'][0]['round']) if reachable else None
        witnesses.append({'id': row['id'], 'candidate_sha256': row['candidate_sha256'],
            'status': row['status'], 'reachable_witness': selected,
            'runtime_errors': [m for m in row['runtime'] if not m['pass']],
            'requires_additional_reachability_check': selected is None and row['status'] == 'fidelity_discrepancy'})
    exclusive(ROOT / 'phase3/validation/uniform_fidelity_witnesses_v3.json', encoded({
        'validation_sha256': sha((ROOT / 'phase3/validation/uniform_v3b.json').read_bytes()),
        'scope': 'Shortest recorded first discrepancy among seven candidate-on-policy scripts; not globally minimal.',
        'witnesses': witnesses}))
    lines = ['# Conversión uniforme v3: resultados originales', '',
        'Fecha: 2026-09-14. La tanda autorizada terminó y las respuestas se conservaron sin correcciones.', '',
        f'**{passed}/572 estrategias pasan las comprobaciones dirigidas.** '
        f'Las demás tienen incidencias descritas abajo; recibir código válido no certifica fidelidad.', '',
        '## Ejecución y coste', '',
        f'- Solicitudes: 572; respuestas verificadas: 572; reintentos: 0.',
        f'- Modelo devuelto en todas: `gpt-5.4-mini-2026-03-17`.',
        f'- Coste calculado: **US${receipt["cost_usd_calculated_not_invoice"]:.8f}**, dentro del techo autorizado de US$2. No es una factura.',
        f'- Tokens: {receipt["usage"]["prompt_tokens"]:,} de entrada y {receipt["usage"]["completion_tokens"]:,} de salida; caché: {receipt["usage"]["cached_tokens"]}.',
        '- Corpus: 274 occidentales + 298 chinas; 28 exclusiones previas respecto a 600.',
        '- Las descripciones originales se preservaron; misma plantilla, convenciones, parámetros y snapshot para ambos grupos.', '',
        '## Validación común', '',
        f'- {checks:,} comprobaciones de acción, sobre {len(report["scenarios"])} historiales controlados y {len(report["on_policy_opponents"])} rivales programados por estrategia.',
        f'- Partidas diagnósticas completas: {sum(m["pass"] for m in games):,}/{len(games):,}, con 11 rivales clásicos y horizonte de 1.000 rondas.',
        f'- Controles occidentales comparados: {len(controls)}/274. Trazas idénticas en todos los historiales controlados: {sum(c["all_same"] for c in controls)}; con alguna diferencia: {sum(not c["all_same"] for c in controls)}.',
        '- El control es la respuesta original occidental v2, incluso donde luego se corrigió localmente. Una diferencia no demuestra por sí sola mejora o empeoramiento.',
        '- Inspección única de las 572 fuentes, agrupadas en 152 hashes distintos; nueve pruebas del validador optimizado aprobadas. No es revisión independiente por dos personas.',
        '- El seguimiento optimizado conserva los límites de pasos; 13 trazas completas coincidieron con el adaptador inicial. Cuatro procesos locales usan particiones disjuntas y semillas fijas.', '',
        '| Modelo | Total | Pasa pruebas | Discrepancia de fidelidad | Error de ejecución | Otro error de validación |',
        '|---|---:|---:|---:|---:|---:|']
    for model in sorted({r['id'].split('/')[0] for r in rows}):
        selected = [r for r in rows if r['id'].startswith(model + '/')]
        counts = Counter(r['status'] for r in selected)
        lines.append(f'| {model} | {len(selected)} | {counts["passed_targeted_checks"]} | {counts["fidelity_discrepancy"]} | {counts["runtime_error"]} | {counts["validation_error"]} |')
    lines += ['', '## Incidencias preservadas', '',
              'Las diferencias en historiales impuestos se distinguen de las observadas con el historial producido por el propio candidato. Los segundos aportan un contraejemplo alcanzable frente al rival programado.', '',
              '| Estrategia | Estado | Evidencia breve |', '|---|---|---|']
    for r in rows:
        if r['status'] == 'passed_targeted_checks':
            continue
        reachable = [s for s in r['semantic'] if s['mode'] == 'candidate_on_policy' and s['failures']]
        differences = reachable or [s for s in r['semantic'] if s['failures']]
        errors = [s for s in r['semantic'] if 'error' in s]
        if errors:
            detail = f'Ronda {errors[0]["error_round"]}: {errors[0]["error"]}'
        elif differences:
            witness = differences[0]['failures'][0]
            detail = f'Ronda {witness["round"]}: esperado {witness["expected"]}, recibido {witness["actual"]}; ' + ('historial alcanzable' if reachable else 'historial impuesto, falta confirmar alcance')
        else:
            detail = r.get('error', 'Consultar registro de partidas')
        lines.append(f'| {r["id"]} | {r["status"]} | {detail.replace(chr(10), " ").replace("|", "/")} |')
    lines += ['', '## Alcance y continuidad', '',
        'La compatibilidad del procedimiento de conversión y del entorno de prueba se aplicó a ambas cohortes. Las incidencias originales no deben ocultarse ni contarse como conversiones fieles. Antes de admitir el campo completo se requiere cerrar sus diagnósticos y, si corresponde, registrar correcciones derivadas por separado bajo la política declarada.', '',
        'Estas son pruebas dirigidas; no acreditan equivalencia exhaustiva frente a cualquier historial. No se ejecutó el torneo mixto ni se obtuvieron resultados competitivos. Las cuatro interpretaciones alternativas siguen siendo análisis de sensibilidad obligatorios del torneo.', '',
        'Evidencia: [validación completa](validation/uniform_v3b.json), [contraejemplos](validation/uniform_fidelity_witnesses_v3.json), [recibos y consumo](validation/uniform_conversion_receipt_v3.json), [inspección de fuentes](validation/uniform_source_review_v3.json), [política de resolución](CHINESE_RESOLUTION_POLICY_v1.md).', '']
    exclusive(ROOT / 'phase3/UNIFORM_RESULTS_v3.md', '\n'.join(lines).encode('utf-8'))
    print(json.dumps({'passed': passed, 'checks': checks, 'games_complete': sum(m['pass'] for m in games),
                      'games_total': len(games), 'paired_controls': len(controls),
                      'paired_same': sum(c['all_same'] for c in controls)}))


if __name__ == '__main__':
    main()
