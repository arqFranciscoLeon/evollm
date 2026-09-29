"""Render prespecified descriptive results from the verified analysis JSON."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / 'phase3'
SOURCE = PHASE / 'validation/confirmatory_analysis_v1.json'
OUTPUT = PHASE / 'DESCRIPTIVE_RESULTS_v1.md'

MIX_LABELS = (
    ('balanced', 'Equal thirds', '(1/3, 1/3, 1/3)'),
    ('aggressive_dominant', 'Aggressive dominant', '(2/3, 1/6, 1/6)'),
    ('cooperative_dominant', 'Cooperative dominant', '(1/6, 2/3, 1/6)'),
    ('neutral_dominant', 'Neutral dominant', '(1/6, 1/6, 2/3)'),
)


def render():
    if OUTPUT.exists():
        raise FileExistsError('Descriptive supplement exists; inspect before rerunning')
    analysis = json.loads(SOURCE.read_bytes())
    if (analysis['status'] != 'complete' or analysis['execution']['strategies'] != 572
            or analysis['execution']['errors'] != 0):
        raise ValueError('Analysis closure missing')
    d = analysis['descriptive_primary_scenario_0']
    cells = d['model_attitude']
    self_play = {(r['model'], r['attitude']): r for r in d['autopairs']}
    if len(cells) != 24 or sum(r['strategies'] for r in cells) != 572 or len(self_play) != 24:
        raise ValueError('Unexpected model/attitude table')
    rows = [
        '# Descriptive results for the registered primary scenario', '',
        'The table below reports every model×attitude cell. For each strategy, mutual cooperation and focal payoff were averaged over its 571 distinct opponents; the cell entries then average those strategy means. Self-play uses the one diagonal encounter for each strategy and is shown separately from the H7 contrast. Payoffs use the registered T=5, R=3, P=1, S=0 game.', '',
        '| Model identity | Attitude | n | Mutual cooperation vs others (%) | Focal payoff vs others | Self-play cooperation (%) | Self-play payoff |',
        '|---|---|---:|---:|---:|---:|---:|',
    ]
    for cell in cells:
        self_row = self_play[(cell['model'], cell['attitude'])]
        rows.append(f"| {cell['model']} | {cell['attitude']} | {cell['strategies']} | "
                    f"{100*cell['mean_mutual_cooperation_vs_all_other_identities']:.2f} | "
                    f"{cell['mean_focal_payoff_vs_all_other_identities']:.4f} | "
                    f"{100*self_row['mean_self_play_cooperation']:.2f} | "
                    f"{self_row['mean_self_play_payoff']:.4f} |")
    rows += [
        '', '## Counterfactual opponent-attitude mixtures', '',
        'These are reweightings of the same completed encounters. For each focal strategy, the target attitude weight is divided equally among the eight opponent models and then among eligible identities in each model×attitude cell, excluding the focal identity. The table averages the 572 focal strategy values with equal weight. Each tuple is ordered Aggressive, Cooperative, Neutral.', '',
        '| Mixture | Target attitude weights | Mutual cooperation (%) | Focal payoff |',
        '|---|---|---:|---:|',
    ]
    mix_rows = d['counterfactual_mixes']
    if len(mix_rows) != 96:
        raise ValueError('Expected four mixtures across 24 focal cells')
    for key, label, weights in MIX_LABELS:
        selected = [r for r in mix_rows if r['mix'] == key]
        count = sum(r['strategies'] for r in selected)
        if len(selected) != 24 or count != 572:
            raise ValueError('Mixture cell/count mismatch: ' + key)
        cooperation = sum(r['strategies'] * r['mean_mutual_cooperation'] for r in selected) / count
        payoff = sum(r['strategies'] * r['mean_focal_payoff'] for r in selected) / count
        rows.append(f'| {label} | {weights} | {100*cooperation:.2f} | {payoff:.4f} |')
    rows += ['', 'The 96 cell-level mixture rows and exact values are preserved in `validation/confirmatory_analysis_v1.json`. These descriptive quantities are not additional hypothesis tests, independent samples, or evolutionary fixation estimates.', '']
    OUTPUT.write_text('\n'.join(rows), encoding='utf-8')
    return OUTPUT


if __name__ == '__main__':
    print(render())
