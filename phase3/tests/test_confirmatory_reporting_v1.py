import numpy as np
import pytest

from phase3.analyze_confirmatory_results_v1 import descriptive_tables
from phase3.analyze_phase3 import ATTITUDES


def test_counterfactual_attitude_mixes_preserve_cell_means():
    models = []
    attitudes = []
    for model in range(8):
        for attitude in ATTITUDES:
            for _ in range(2):
                models.append(f'model_{model}')
                attitudes.append(attitude)
    values = np.array([{'Aggressive': 0.0, 'Cooperative': 0.5, 'Neutral': 1.0}[a]
                       for a in attitudes])
    cooperation = (values[:, None] + values[None, :]) / 2
    payoff = 1 + 2 * cooperation
    report = descriptive_tables({'ids': [f'id_{i}' for i in range(len(models))],
                                 'models': models, 'attitudes': attitudes,
                                 'cooperation': cooperation, 'payoff': payoff})
    mixes = {
        'balanced': (1/3, 1/3, 1/3),
        'aggressive_dominant': (2/3, 1/6, 1/6),
        'cooperative_dominant': (1/6, 2/3, 1/6),
        'neutral_dominant': (1/6, 1/6, 2/3),
    }
    values_by_attitude = {'Aggressive': 0.0, 'Cooperative': 0.5, 'Neutral': 1.0}
    for row in report['counterfactual_mixes']:
        opponent_mean = sum(weight * values_by_attitude[attitude]
                            for weight, attitude in zip(mixes[row['mix']], ATTITUDES))
        expected = (values_by_attitude[row['focal_attitude']] + opponent_mean) / 2
        assert row['mean_mutual_cooperation'] == pytest.approx(expected)
        assert row['mean_focal_payoff'] == pytest.approx(1 + 2 * expected)
