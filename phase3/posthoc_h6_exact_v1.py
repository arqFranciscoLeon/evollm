"""Exact-test sensitivity for the reproduced H6 contrasts (post hoc, NOT preregistered).

Replaces the pooled normal approximation with two-sided Fisher exact and
Boschloo exact tests for each of the six Phase 2 pairwise comparisons of
aggressive fixation (n=500 per library), then applies Holm's step-down
correction at familywise alpha 0.05. Same counts as the reconciled archive.
"""
import json

from scipy import stats

from phase3.posthoc_common_v1 import OUT, PHASE, write_json

OUTPUT = OUT / 'h6_exact_v1.json'
N = 500


def holm(pvalues, alpha=0.05):
    order = sorted(range(len(pvalues)), key=lambda i: pvalues[i])
    reject = [False] * len(pvalues)
    for rank, i in enumerate(order):
        if pvalues[i] <= alpha / (len(pvalues) - rank):
            reject[i] = True
        else:
            break
    return reject


def main():
    if OUTPUT.exists():
        raise FileExistsError('Output exists; inspect before rerunning')
    prior = json.loads((PHASE / 'writing/prior_evidence_reconciled_v1.json').read_text(encoding='utf-8'))
    result = {'status': 'post hoc exact-test sensitivity; not preregistered', 'n_per_library': N, 'archives': {}}
    for archive in ('phase2', 'robust'):
        rows = prior['h6'][archive]
        fisher, boschloo = [], []
        for row in rows:
            a, b = row['counts']
            table = [[a, N - a], [b, N - b]]
            fisher.append(float(stats.fisher_exact(table, alternative='two-sided')[1]))
            boschloo.append(float(stats.boschloo_exact(table, alternative='two-sided').pvalue))
        rf, rb = holm(fisher), holm(boschloo)
        result['archives'][archive] = [
            {'models': row['models'], 'counts': row['counts'],
             'normal_p': row['p'], 'normal_reject_holm': row['reject_holm'],
             'fisher_p': fisher[i], 'fisher_reject_holm': rf[i],
             'boschloo_p': boschloo[i], 'boschloo_reject_holm': rb[i]}
            for i, row in enumerate(rows)]
        result['archives'][archive + '_summary'] = {
            'normal_rejections': sum(r['reject_holm'] for r in rows),
            'fisher_rejections': sum(rf), 'boschloo_rejections': sum(rb),
            'same_pairs_rejected_all_methods': all(
                rows[i]['reject_holm'] == rf[i] == rb[i] for i in range(len(rows))),
        }
    write_json(OUTPUT, result)
    print(json.dumps({k: v for k, v in result['archives'].items() if k.endswith('summary')}, indent=1))


if __name__ == '__main__':
    main()
