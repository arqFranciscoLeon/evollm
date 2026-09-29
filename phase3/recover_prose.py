"""Look for longer archived versions of flagged Default descriptions; never synthesize text."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def descriptions(data):
    text = data.decode('utf-8-sig')
    lines = text.splitlines()
    result = {}
    for cls in ast.parse(text).body:
        if not isinstance(cls,ast.ClassDef):
            continue
        index = cls.lineno-2
        block = []
        while index >= 0:
            line = lines[index].strip()
            if line.startswith('#'):
                block.append(line[1:].strip())
            elif line:
                break
            index -= 1
        result[cls.name] = ' '.join(' '.join(reversed(block)).split())
    return result


def main():
    manifest = json.loads((ROOT/'phase3/inputs/manifest.json').read_text(encoding='utf-8'))
    records = []
    for lib in manifest['libraries']:
        if lib['prompt'] != 'default' or not lib['model'].startswith('gemini'):
            continue
        flagged = [s for s in lib['strategies'] if 'unfinished_ending_manual_review' in s['flags']]
        if not flagged:
            continue
        original = descriptions((ROOT/lib['snapshot_path']).read_bytes())
        variants = []
        for name in (lib['filename'],lib['filename'].replace('_75.py','_75_noise.py')):
            relative = f'strategies/{name}'
            commits = subprocess.check_output(['git','log','--all','--format=%H','--',relative],cwd=ROOT,text=True).splitlines()
            for commit in commits:
                data = subprocess.check_output(['git','show',f'{commit}:{relative}'],cwd=ROOT)
                variants.append({'source':f'git:{commit}:{relative}', 'sha256':hashlib.sha256(data).hexdigest(),
                                 'descriptions':descriptions(data)})
            for folder in (ROOT.parents[2], *ROOT.parent.iterdir()):
                candidate = folder / relative
                if candidate.is_file():
                    data = candidate.read_bytes()
                    variants.append({'source':str(candidate), 'sha256':hashlib.sha256(data).hexdigest(),
                                     'descriptions':descriptions(data)})
        for strategy in flagged:
            prose = original[strategy['class']]
            extensions = []
            for variant in variants:
                other = variant['descriptions'].get(strategy['class'],'')
                if other.startswith(prose) and len(other) > len(prose):
                    extensions.append({'source':variant['source'], 'text':other})
            records.append({'id':strategy['id'], 'line':strategy['line'], 'text':prose,
                            'candidate_extensions':extensions, 'versions_examined':len(variants),
                            'sources':[{k:v[k] for k in ('source','sha256')} for v in variants],
                            'manual_review': 'Ending inspected: clipped explanation after rules' if strategy['id']=='gemini_31_pro/default/Aggressive_9' else 'Ending inspected: incomplete sentence or strategic rule',
                            'status':'candidate_requires_provenance_review' if extensions else 'not_recovered_in_examined_strategy_archives'})
    report = {'scope':'Committed historical Default/noise libraries and available corresponding working copies; no generative reconstruction. Does not establish absence in external chat archives.',
              'records':records}
    (ROOT/'phase3/inputs/prose_recovery.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f"Reviewed {len(records)} clipped endings; {sum(bool(r['candidate_extensions']) for r in records)} have longer candidate texts.")


if __name__ == '__main__':
    main()
