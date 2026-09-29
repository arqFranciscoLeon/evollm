"""Figures for manuscript v5, drawn from registered and post hoc outputs.

Fig. 1  Mean mutual cooperation between the 24 model x attitude cells (registered matrix).
Fig. 2  Model decomposition of H7 and leave-one-model-out values (post hoc).
Fig. 3  Archived C-N fixation margins against the C-N payoff gap of the
        historical implementations, 24 libraries (post hoc).
Fig. 4  Behavioural classes of the 572 identities against the probe panel (post hoc).
Palette: validated reference categorical slots (light mode); sequential blue ramp.
"""
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

from phase3.analyze_phase3 import ATTITUDES
from phase3.posthoc_common_v1 import MODEL_LABELS, OUT, PHASE, load_primary
from phase3.posthoc_h7_structure_v1 import cell_means, codes

FIG = PHASE / 'writing/figures'
SURFACE = '#fcfcfb'
INK, INK2, MUTED, GRID, AXIS = '#0b0b0b', '#52514e', '#898781', '#e1e0d9', '#c3c2b7'
SLOTS = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4']
BLUE_RAMP = ['#cde2fb', '#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#184f95', '#0d366b']
POS, NEG = '#2a78d6', '#e34948'

plt.rcParams.update({
    'font.family': 'sans-serif', 'font.sans-serif': ['Segoe UI', 'DejaVu Sans'],
    'font.size': 8.5, 'axes.edgecolor': AXIS, 'axes.labelcolor': INK2, 'xtick.color': INK2,
    'ytick.color': INK2, 'axes.facecolor': SURFACE, 'figure.facecolor': SURFACE,
    'savefig.facecolor': SURFACE, 'axes.spines.top': False, 'axes.spines.right': False,
    'axes.titlesize': 9, 'axes.titleweight': 'bold', 'axes.titlecolor': INK,
})


def save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / f'{name}.png', dpi=300, bbox_inches='tight')
    fig.savefig(FIG / f'{name}.pdf', bbox_inches='tight')
    plt.close(fig)


def fig1():
    data = load_primary()
    mc, ac, labels = codes(data['models'], data['attitudes'])
    means = cell_means(data['cooperation'], mc, ac, len(labels))  # index 3*m + a
    order = [3 * m + a for a in range(3) for m in range(len(labels))]
    grid = means[np.ix_(order, order)]
    ticks = [MODEL_LABELS[labels[m]] for a in range(3) for m in range(len(labels))]
    cmap = LinearSegmentedColormap.from_list('seq', BLUE_RAMP)
    fig, ax = plt.subplots(figsize=(6.8, 6.0))
    im = ax.imshow(grid, cmap=cmap, vmin=0, vmax=1, interpolation='nearest')
    for k in (8, 16):
        ax.axhline(k - 0.5, color=SURFACE, lw=2.5)
        ax.axvline(k - 0.5, color=SURFACE, lw=2.5)
    ax.set_xticks(range(24), ticks, rotation=90, fontsize=6.5)
    ax.set_yticks(range(24), ticks, fontsize=6.5)
    for i, att in enumerate(ATTITUDES):
        ax.text(8 * i + 3.5, -1.6, att, ha='center', va='bottom', fontsize=8.5, color=INK, fontweight='bold')
        ax.text(-9.2, 8 * i + 3.5, att, ha='center', va='center', rotation=90, fontsize=8.5,
                color=INK, fontweight='bold')
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    cb = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
    cb.set_label('Mean mutual cooperation (share of rounds)', color=INK2)
    cb.outline.set_visible(False)
    save(fig, 'fig1_cell_cooperation')


def fig2():
    s = json.loads((OUT / 'h7_structure_v1.json').read_text(encoding='utf-8'))
    reg = json.loads((PHASE / 'validation/confirmatory_analysis_v1.json').read_text(encoding='utf-8'))
    null = [100 * x for x in reg['primary_h7_scenario_0']['null_interval95']]
    h7 = 100 * reg['primary_h7_scenario_0']['difference']
    models = s['models']
    delta = 100 * np.array(s['per_model_mean_difference'])
    loo = np.array([100 * s['leave_one_model_out'][m] for m in models])
    idx = np.argsort(delta)
    names = [MODEL_LABELS[models[i]] for i in idx]
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 3.1), gridspec_kw={'wspace': 0.55})
    y = np.arange(len(models))
    a.barh(y, delta[idx], color=[POS if v > 0 else NEG for v in delta[idx]], height=0.62,
           edgecolor=SURFACE, linewidth=1)
    a.axvline(0, color=AXIS, lw=0.8)
    for yi, v in zip(y, delta[idx]):
        a.text(v + (0.25 if v >= 0 else -0.25), yi, f'{v:+.2f}', va='center',
               ha='left' if v >= 0 else 'right', fontsize=7, color=INK2)
    a.set_yticks(y, names)
    a.set_xlim(-7, 12.5)
    a.set_xlabel('Within minus between, mean of six strata (pp)')
    a.set_title('(a) Contribution of each model', loc='left')
    a.grid(axis='x', color=GRID, lw=0.6)
    a.set_axisbelow(True)
    b.axvspan(null[0], null[1], color='#f0efec', zorder=0)
    b.axvline(h7, color=INK2, lw=1, ls='--')
    b.scatter(loo[idx], y, s=36, color=INK, zorder=3, edgecolor=SURFACE, linewidth=1.2)
    b.text(h7, len(models) - 0.35, f' registered H7 = {h7:.2f}', fontsize=7, color=INK2, va='bottom')
    b.text(np.mean(null), -0.95, 'null reference\n(95%)', fontsize=6.5, color=MUTED, ha='center', va='top')
    b.set_yticks(y, [f'without {n}' for n in names], fontsize=7.2)
    b.set_xlim(-0.2, 0.8)
    b.set_ylim(-1.6, len(models) - 0.2)
    b.set_xlabel('H7 recomputed without the model (pp)')
    b.set_title('(b) Leave one model out', loc='left')
    b.grid(axis='x', color=GRID, lw=0.6)
    b.set_axisbelow(True)
    save(fig, 'fig2_h7_decomposition')


def fig3():
    h = json.loads((OUT / 'historical_v1.json').read_text(encoding='utf-8'))
    prior = json.loads((PHASE / 'writing/prior_evidence_reconciled_v1.json').read_text(encoding='utf-8'))
    ci = {r['algo']: r['ci95_pp'] for ph in ('phase1', 'phase2') for r in prior['datasets'][ph]['balanced_clean']}
    colours = {'default': SLOTS[0], 'prose': SLOTS[1], 'refine': SLOTS[2]}
    markers = {'phase1': 'o', 'phase2': 's'}
    fig, ax = plt.subplots(figsize=(5.6, 3.9))
    ax.axhline(0, color=AXIS, lw=0.8)
    ax.axvline(0, color=AXIS, lw=0.8)
    for p in h['fixation_margin_points']:
        prompt = p['library'].rsplit('_', 2)[-2]
        lo, hi = ci[p['library']]
        ax.errorbar(p['balanced_gap'], p['margin_pp'], yerr=[[p['margin_pp'] - lo], [hi - p['margin_pp']]],
                    fmt=markers[p['phase']], color=colours[prompt], ms=6, mec=SURFACE, mew=1,
                    elinewidth=0.9, capsize=0, zorder=3)
    # Label positions in data coordinates, placed in empty regions with thin leader lines.
    places = {'openai_gpt54mini_refine_75': (0.255, 47, 'center'), 'gemini_25_flash_prose_75': (0.20, 24, 'left'),
              'gemini_25_flash_refine_75': (0.10, 31, 'center'), 'glm_51_refine_75': (0.035, 25, 'center'),
              'kimi_k25_refine_75': (0.20, 5, 'left')}
    for p in h['fixation_margin_points']:
        if p['library'] in places:
            tx, ty, ha = places[p['library']]
            model = p['library'].rsplit('_', 2)[0]
            prompt = 'Self-Refine' if 'refine' in p['library'] else 'Prose'
            ax.annotate(f"{MODEL_LABELS.get(model, model)} {prompt}", (p['balanced_gap'], p['margin_pp']),
                        xytext=(tx, ty), textcoords='data', fontsize=6.5, color=INK2, ha=ha, va='center',
                        arrowprops={'arrowstyle': '-', 'color': MUTED, 'lw': 0.6, 'shrinkA': 2, 'shrinkB': 4})
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], marker='o', ls='', color=colours[k], label={'default': 'Default', 'prose': 'Prose', 'refine': 'Self-Refine'}[k], mec=SURFACE)
               for k in ('default', 'prose', 'refine')]
    handles += [Line2D([], [], marker=markers[k], ls='', color=MUTED, label=lab, mec=SURFACE)
                for k, lab in (('phase1', 'Phase 1 (corrected)'), ('phase2', 'Phase 2'))]
    ax.legend(handles=handles, frameon=False, fontsize=7, loc='upper left', ncol=2)
    rho = h['fixation_margin_association']['spearman_gap_vs_margin'][0]
    ax.set_xlabel('Cooperative minus neutral payoff at equal attitude weights\n(historical implementations, points per round)')
    ax.set_ylabel('Cooperative minus neutral fixation (pp)')
    ax.set_title(f'Payoff separation and plurality margins, 24 libraries (Spearman ρ = {rho:.2f})', loc='left')
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    save(fig, 'fig3_margins_vs_payoff_gap')


CLASS_ORDER = ['Tit-for-Tat family', 'Other nice reciprocators', 'Suspicious Tit-for-Tat family',
               'Always defect', 'Other']


def behaviour_class(label):
    base = label.replace(' + end-game deviation', '')
    if base == 'TitForTat':
        return CLASS_ORDER[0]
    if base in ('WinStayLoseShift', 'TitFor2Tats', 'TwoTitsForTat'):
        return CLASS_ORDER[1]
    if base == 'SuspiciousTitForTat':
        return CLASS_ORDER[2]
    if base == 'Defector':
        return CLASS_ORDER[3]
    return CLASS_ORDER[4]


def fig4():
    b = json.loads((OUT / 'behaviour_v1.json').read_text(encoding='utf-8'))
    models = sorted(MODEL_LABELS)
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 3.0), sharey=True, gridspec_kw={'wspace': 0.08})
    for ax, att in zip(axes, ATTITUDES):
        rows = []
        for m in models:
            ids = [s for s in b['identities'] if s.startswith(m + '/') and s.endswith(tuple(f'/{att}_{k}' for k in range(1, 26)))]
            counts = {c: 0 for c in CLASS_ORDER}
            for s in ids:
                counts[behaviour_class(b['identities'][s]['label']['label'])] += 1
            rows.append((m, len(ids), counts))
        y = np.arange(len(models))
        left = np.zeros(len(models))
        for colour, cls in zip(SLOTS, CLASS_ORDER):
            share = np.array([r[2][cls] / r[1] for r in rows])
            ax.barh(y, share, left=left, color=colour, height=0.66, edgecolor=SURFACE, linewidth=1.2,
                    label=cls)
            left += share
        for yi, r in zip(y, rows):
            ax.text(1.02, yi, f'n={r[1]}', va='center', fontsize=6.5, color=MUTED)
        ax.set_title(att, loc='left')
        ax.set_xlim(0, 1.13)
        ax.set_xticks([0, 0.5, 1], ['0', '50%', '100%'])
        ax.invert_yaxis()
        ax.spines['left'].set_visible(False)
        ax.tick_params(axis='y', length=0)
    axes[0].set_yticks(np.arange(len(models)), [MODEL_LABELS[m] for m in models])
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=3, frameon=False, fontsize=7,
               bbox_to_anchor=(0.52, -0.12))
    save(fig, 'fig4_behaviour_classes')


if __name__ == '__main__':
    fig1()
    fig2()
    fig3()
    fig4()
    print('figures written to', FIG)
