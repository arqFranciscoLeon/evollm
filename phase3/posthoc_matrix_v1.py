"""Export the registered primary (scenario 0) matrices for post hoc analyses.

Rebuilds cooperation and payoff matrices from the 665 verified receipts and
refuses to save them unless the matrix fingerprint and H7 value reproduce the
registered confirmatory output exactly.
"""
import json

import numpy as np

from phase3.analyze_phase3 import h7_statistic
from phase3.analyze_confirmatory_results_v1 import PLAN, verified_batches
from phase3.posthoc_common_v1 import (MATRIX, OUT, REGISTERED_H7, REGISTERED_MATRIX_SHA,
                                      matrix_sha, write_json)
from phase3.reuse_batches_v1 import export_scenario


def main():
    if MATRIX.exists():
        raise FileExistsError('Primary matrix already exported; inspect before replacing')
    context = json.loads((PLAN / 'context.json').read_bytes())
    manifest = json.loads((PLAN / 'manifest.json').read_bytes())
    matrix = export_scenario(context, 0, verified_batches(manifest))
    fingerprint = matrix_sha(matrix['ids'], matrix['cooperation'])
    effect = h7_statistic(matrix['cooperation'], matrix['models'], matrix['attitudes'])
    if fingerprint != REGISTERED_MATRIX_SHA or effect != REGISTERED_H7:
        raise ValueError('Exported matrix does not reproduce the registered analysis')
    OUT.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(MATRIX, ids=np.array(matrix['ids']),
                        cooperation=matrix['cooperation'], payoff=matrix['payoff'])
    write_json(OUT / 'primary_matrix_v1.json', {
        'status': 'post hoc export of the registered scenario-0 matrices',
        'matrix_sha256_registered_definition': fingerprint,
        'h7_reproduced': effect,
        'identities': len(matrix['ids']),
        'npz_file': MATRIX.name,
    })
    print(json.dumps({'matrix_sha256': fingerprint, 'h7': effect}))


if __name__ == '__main__':
    main()
