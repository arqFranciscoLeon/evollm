"""Read-only reconciliation of archived results; writes new editorial reports only."""
import hashlib
import json
from collections import Counter
from pathlib import Path

from phase3.existing_evidence import ATTITUDES, load_checked, winner, cn_margin, pairwise_aggression
from phase3.audit_inputs import MODELS

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def run():
    summary_path = ROOT / 'phase3/evidence/summary.json'
    summary = json.loads(summary_path.read_bytes())
    result = {'source_summary_sha256': hashlib.sha256(summary_path.read_bytes()).hexdigest(),
              'datasets': {}, 'h6': {}, 'scope': 'Post hoc reconciliation; no new simulations.'}
    lines = ['# Conciliación de resultados anteriores', '',
             '28 de septiembre de 2026. Recalculado desde los tres snapshots archivados, sin modificar fuentes ni ejecutar nuevas simulaciones. Se verifica su SHA-256 contra la auditoría anterior, cobertura, conteos, denominadores y porcentajes. Los intervalos C−N son aproximaciones normales marginales posteriores, condicionales a bibliotecas fijas.', '']
    loaded = {}
    for key, provenance in summary['provenance'].items():
        path = ROOT / provenance['snapshot']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == provenance['sha256'], key
        models = list(MODELS)[:4] if key == 'phase1' else list(MODELS)[4:]
        ds = load_checked(path, models, key == 'robust')
        loaded[key] = ds
        balanced = [{'algo': algo, 'counts': {a: r[a] for a in ATTITUDES},
                     'plurality': winner(r), **cn_margin(r)}
                    for (algo, pop), r in ds.items() if pop == (4, 4, 4) and '_noise' not in algo]
        assert balanced == summary['balanced_clean'][key], key
        deficits = [{'algo': algo, 'population': list(pop), 'actual_n': r['iteraciones'],
                     'shortfall': 500-r['iteraciones']}
                    for (algo, pop), r in ds.items() if r['iteraciones'] != 500]
        assert deficits == summary['below_planned_n500'][key], key
        stats = {'source': str(path.relative_to(ROOT)), 'sha256': provenance['sha256'],
                 'conditions': len(ds), 'counted_runs': sum(r['iteraciones'] for r in ds.values()),
                 'planned_runs': 500*len(ds), 'pluralities': dict(Counter(r['plurality'] for r in balanced)),
                 'cn_intervals_including_zero': sum(r['ci_includes_zero'] for r in balanced),
                 'balanced_clean': balanced, 'shortfalls': deficits}
        result['datasets'][key] = stats
        lines += [f'## {key}', '', f"Condiciones: {stats['conditions']}; resultados contabilizados: {stats['counted_runs']}/{stats['planned_runs']}. Pluralidades limpias balanceadas: {stats['pluralities']}. Intervalos C−N que incluyen cero: {stats['cn_intervals_including_zero']}/12.", '',
                  '| Biblioteca | A | C | N | Pluralidad | C−N (pp) | IC marginal 95 % (pp) |',
                  '|---|---:|---:|---:|---|---:|---|']
        for r in balanced:
            c = r['counts']
            lines.append(f"| {r['algo']} | {c['Aggressive']} | {c['Cooperative']} | {c['Neutral']} | {r['plurality']} | {r['margin_pp']:.2f} | [{r['ci95_pp'][0]:.2f}, {r['ci95_pp'][1]:.2f}] |")
        lines += ['']
        if deficits:
            lines += ['| Condición | Población A:C:N | n efectivo | Faltantes frente a 500 |', '|---|---|---:|---:|']
            for r in deficits:
                lines.append(f"| {r['algo']} | {r['population']} | {r['actual_n']} | {r['shortfall']} |")
            lines += ['']
    for key in ('phase2', 'robust'):
        pairs = pairwise_aggression(loaded[key], list(MODELS)[4:], key == 'robust')
        assert pairs == summary[key+'_h6']
        result['h6'][key] = pairs
        lines += [f'## H6: {key}', '', '| Comparación | Conteos A (n=500 cada uno) | z | p bilateral | Rechaza Holm |', '|---|---|---:|---:|---|']
        for r in pairs:
            lines.append(f"| {' / '.join(r['models'])} | {r['counts']} | {r['z']:.4f} | {r['p']:.8g} | {r['reject_holm']} |")
        lines += ['']
    flips = []
    for (algo, pop), row in loaded['phase2'].items():
        if pop == (4, 4, 4) and '_noise' not in algo:
            other = loaded['robust'][(algo+'_robust', pop)]
            if winner(row) != winner(other):
                flips.append({'algo': algo, 'from': winner(row), 'to': winner(other)})
    assert sorted(flips, key=lambda r:r['algo']) == sorted(summary['phase2_robust_plurality_flips'], key=lambda r:r['algo'])
    result['category_changes'] = flips
    lines += ['## Cambios con reconversión parcial', '', '| Biblioteca | Antes | Después |', '|---|---|---|']
    lines += [f"| {r['algo']} | {r['from']} | {r['to']} |" for r in flips]
    lines += ['', 'Son cuatro cambios estrictos C↔N y uno N→empate. La reconversión parcial y una nueva realización Monte Carlo no permiten atribuir aisladamente estos cambios al conversor.', '',
              'Ver `STUDY_DESIGNS_AND_RECONCILIATION_v1.md` para decisiones editoriales y límites pendientes. Este reporte no verifica las matrices de pagos/ICD ni reconstruye las causas individuales de los faltantes.', '']
    for path in (OUT/'prior_evidence_reconciled_v1.json', OUT/'PRIOR_RESULTS_TABLES_v1.md'):
        if path.exists():
            raise FileExistsError(path)
    (OUT/'prior_evidence_reconciled_v1.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    (OUT/'PRIOR_RESULTS_TABLES_v1.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({k:{f:v[f] for f in ('conditions','counted_runs','pluralities')} for k,v in result['datasets'].items()}, indent=2))


if __name__ == '__main__':
    run()
