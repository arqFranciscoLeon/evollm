"""Prepare a bounded, non-confirmatory reuse-engine diagnostic."""
import hashlib
import json
from pathlib import Path

from phase3.execute_uniform import load_field
from phase3.interpretation_sensitivity_v1 import load_scenario
from phase3.reuse_batches_v1 import batches, encoded, execute_batch, make_context, sha
from phase3.runtime import ROOT

OUT = ROOT / 'phase3/reuse_diagnostic_v1'
BUNDLE = ROOT / 'phase3/cloud_bundle_reuse_diagnostic_v1'
OLD_BUNDLE = ROOT / 'phase3/cloud_bundle_v2'


def main():
    if OUT.exists() or BUNDLE.exists():
        raise ValueError('Diagnostic artifacts already exist; do not overwrite')
    full = json.loads((ROOT / 'phase3/reuse_plan_v1/context.json').read_bytes())
    if full['scope'] != 'full_round_robin' or len(full['scenario_sources']) != 16:
        raise ValueError('Frozen full plan changed')
    context = make_context({int(k): v for k, v in full['scenario_sources'].items()},
                           provenance=full['provenance'], scope='selected_diagnostic',
                           turns=full['turns'], seed=full['seed'])
    stable = 'anthropic_sonnet46/default/Cooperative_1'
    alternatives = [r['id'] for r in json.loads(
        (ROOT / 'phase3/inputs/sensitivity_plan_v1.json').read_bytes())['alternatives']]
    pairs = [(stable, stable), (alternatives[0], alternatives[0])]
    pairs += [(stable, sid) for sid in alternatives]
    batch, = list(batches(context, size=32, pairs=pairs))
    if len(batch['jobs']) > 16:
        raise ValueError('Diagnostic exceeds 16 distinct matches')
    OUT.mkdir()
    (OUT / 'context.json').write_text(encoded(context), encoding='utf-8')
    (OUT / 'batch.json').write_text(encoded(batch), encoding='utf-8')
    primary = load_field()
    players = {}
    for mask, sources in context['scenario_sources'].items():
        field = load_scenario(int(mask), primary)
        for sid, source in sources.items():
            players[(sid, source)] = field.players[sid]
    local = execute_batch(batch, context, lambda sid, source: players[(sid, source)])
    (OUT / 'local_baseline.json').write_text(encoded(local), encoding='utf-8')

    old_inventory = json.loads((OLD_BUNDLE / 'BUNDLE_INVENTORY.json').read_bytes())
    selected = [r['path'] for r in old_inventory['files']]
    selected += ['phase3/reuse_batches_v1.py', 'phase3/reuse_worker_v1.py']
    selected += ['phase3/reuse_diagnostic_v1/context.json', 'phase3/reuse_diagnostic_v1/batch.json']
    entries = []
    for name in sorted(set(selected)):
        source = OUT / name.split('/')[-1] if name.startswith('phase3/reuse_diagnostic_v1/') else ROOT / name
        raw = source.read_bytes()
        destination = BUNDLE / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)
        entries.append({'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
    inventory = {'destination': 'Modal workspace unimayor-evollm',
                 'scope': 'selected_diagnostic; at most 16 distinct matches; no confirmatory export',
                 'excludes': 'Credentials, API request/response payloads, local baseline results, Git repository',
                 'files': entries, 'total_bytes': sum(x['bytes'] for x in entries)}
    (BUNDLE / 'BUNDLE_INVENTORY.json').write_text(json.dumps(inventory, indent=2), encoding='utf-8')
    report = {'scope': context['scope'], 'context_sha256': sha(context),
              'batch_sha256': batch['batch_sha256'], 'pairs': len(pairs),
              'unique_matches': len(batch['jobs']),
              'logical_matches': sum(len(j['scenarios']) for j in batch['jobs']),
              'bundle_files': len(entries), 'bundle_bytes': inventory['total_bytes'],
              'bundle_inventory_sha256': hashlib.sha256((BUNDLE / 'BUNDLE_INVENTORY.json').read_bytes()).hexdigest(),
              'local_receipt_sha256': sha(local)}
    (OUT / 'preparation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
