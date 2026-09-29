"""Read-only source/log investigation; writes only derived audit artifacts.

No API clients are imported. Logs may contain private material: only hashes,
counts and match positions are exported, never log bodies.
"""
import ast
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import textwrap

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[2]
SKIP = {'.git', '.phase3-venv', '.venv', 'node_modules', '__pycache__',
        '.pytest_cache', '.pytest_tmp', 'inputs'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git_bytes(ref, path):
    return subprocess.check_output(['git', 'show', f'{ref}:{path}'], cwd=ROOT)


def normalize(text):
    return ' '.join(text.split())


def main():
    recovery_path = ROOT/'phase3/inputs/prose_recovery.json'
    recovery = json.loads(recovery_path.read_text(encoding='utf-8'))
    manifest = json.loads((ROOT/'phase3/inputs/manifest.json').read_text(encoding='utf-8'))
    records = recovery['records']
    historical = []
    roundtrips = []
    for ref, path in [('0faabb18', 'src/evollm/create_strategies.py'),
                      ('1f28a2c', 'src/evollm/create_strategies.py'),
                      ('1f28a2c', 'src/evollm/llm_clients.py')]:
        data = git_bytes(ref, path)
        source = data.decode('utf-8-sig')
        historical.append({'ref': subprocess.check_output(['git', 'rev-parse', ref], cwd=ROOT, text=True).strip(),
                           'path': path, 'sha256': digest(data),
                           'relevant_lines': [{'line': n, 'text': line.strip()} for n, line in enumerate(source.splitlines(), 1)
                                              if any(term in line for term in ('max_output_tokens', 'return response.text',
                                                                               'filemode=', 'FileHandler(', 'textwrap.wrap'))]})
        if path.endswith('create_strategies.py'):
            node = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'format_comment')
            # Execute only the inspected pure formatting function, not the module
            # whose logging initialization would overwrite historical evidence.
            scope = {'textwrap': textwrap}
            exec(compile(ast.Module(body=[node], type_ignores=[]), '<historical-format-comment>', 'exec'), scope)
            for record in records:
                formatted = scope['format_comment'](record['text'])
                restored = ' '.join(line.removeprefix('# ') for line in formatted.splitlines())
                # textwrap may split long words: test loss of non-whitespace characters.
                passed = re.sub(r'\s', '', restored) == re.sub(r'\s', '', record['text'])
                roundtrips.append({'ref': ref, 'id': record['id'], 'nonwhitespace_preserved': passed})

    errors, logs = [], []
    roots = [PROJECT, Path('D:/clo-author')]
    for root in roots:
        if not root.is_dir():
            errors.append({'path': str(root), 'error': 'root_missing'})
            continue
        for folder, dirs, files in os.walk(root, onerror=lambda e: errors.append({'path': e.filename, 'error': type(e).__name__})):
            dirs[:] = sorted(d for d in dirs if d not in SKIP)
            for name in sorted(files):
                if not (name.endswith(('.log', '.jsonl')) or ('response' in name.lower() and name.endswith('.json'))):
                    continue
                path = Path(folder)/name
                try:
                    data = path.read_bytes()
                except OSError as e:
                    errors.append({'path': str(path), 'error': type(e).__name__})
                    continue
                content = normalize(data.decode('utf-8-sig', errors='replace'))
                matches = []
                for record in records:
                    prose = normalize(record['text'])
                    prefix = prose[:160]
                    positions = [m.start() for m in re.finditer(re.escape(prefix), content)]
                    if positions:
                        matches.append({'id': record['id'], 'prefix_positions_normalized': positions,
                                        'full_archived_text_present': prose in content,
                                        'status': 'candidate_requires_manual_review'})
                logs.append({'path': str(path), 'bytes': len(data), 'sha256': digest(data), 'matches': matches,
                             'finish_reason_mentions': len(re.findall(r'finish_reason|finishReason|stop_reason', content))})

    by_id = {s['id']: (lib, s) for lib in manifest['libraries'] for s in lib['strategies']}
    cases = []
    for record in records:
        lib, strategy = by_id[record['id']]
        if digest((ROOT/lib['snapshot_path']).read_bytes()) != lib['sha256']:
            raise ValueError(f"Snapshot hash mismatch: {lib['snapshot_path']}")
        cases.append({'id': record['id'], 'snapshot_path': lib['snapshot_path'],
                      'source_commit': lib['source_commit'], 'source_path': lib['source_path'],
                      'snapshot_sha256': lib['sha256'], 'normalized_prose_sha256': digest(normalize(record['text']).encode()),
                      'manifest_prose_sha256': strategy['prose_sha256'],
                      'manual_review': record['manual_review'], 'tail': record['text'][-130:],
                      'archival_versions_examined': record['versions_examined'],
                      'longer_archival_candidates': len(record['candidate_extensions']),
                      'log_candidate_paths': [log['path'] for log in logs if any(m['id'] == record['id'] for m in log['matches'])],
                      'cause': 'unknown_without_response_metadata',
                      'runtime_source_commit': 'not_established_by_library_commit'})
    report = {'date': '2026-09-13', 'scope_roots': [str(p) for p in roots], 'excluded_directory_names': sorted(SKIP),
              'scope_limit': 'Local project files only. External backups, cloud accounts and personal chat archives were not searched.',
              'recovery_report_sha256': digest(recovery_path.read_bytes()), 'historical_sources': historical,
              'format_roundtrip_checks': roundtrips, 'logs_examined': logs, 'scan_errors': errors, 'cases': cases,
              'summary': {'cases': len(cases), 'by_model': dict(Counter(c['id'].split('/')[0] for c in cases)),
                          'by_model_attitude': dict(Counter('/'.join(c['id'].split('/')[:1] + [c['id'].split('/')[-1].split('_')[0]]) for c in cases)),
                          'log_files_examined': len(logs), 'logs_with_candidates': sum(bool(l['matches']) for l in logs),
                          'format_checks_passed': sum(r['nonwhitespace_preserved'] for r in roundtrips),
                          'format_checks_total': len(roundtrips)}}
    output = ROOT/'phase3/inputs/provenance_audit.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    flagged = {r['id'] for r in records}
    pilot = []
    for lib in manifest['libraries']:
        if lib['prompt'] != 'default' or lib['source_commit'] != manifest['libraries'][0]['source_commit']:
            continue
        for attitude in ('Aggressive', 'Cooperative', 'Neutral'):
            pool = [s for s in lib['strategies'] if s['class'].startswith(attitude+'_') and s['id'] not in flagged]
            chosen = min(pool, key=lambda s: digest(('pilot-20260913|'+s['id']).encode()))
            pilot.append({'id': chosen['id'], 'snapshot_path': lib['snapshot_path'],
                          'snapshot_sha256': lib['sha256'], 'prose_sha256': chosen['prose_sha256'],
                          'other_audit_flags': chosen['flags'], 'semantic_review': 'pending',
                          'conversion_status': 'not_called'})
    pilot_plan = {'status': 'offline_selection_pending_semantic_review',
                  'selection': 'One per Western model and attitude, minimum SHA256(pilot-20260913|id), excluding 18 known truncated cases. Absence of this flag does not certify semantic completeness.',
                  'cases': pilot, 'diagnostic_truncated_ids': sorted(flagged),
                  'diagnostic_policy': 'Review all 18 without conversion first. Incomplete rules are not sent for faithful conversion.',
                  'api_calls': 0}
    (ROOT/'phase3/inputs/pilot_selection.json').write_text(json.dumps(pilot_plan, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report['summary'], ensure_ascii=False))
    print('Scan errors:', len(errors))


if __name__ == '__main__':
    main()
