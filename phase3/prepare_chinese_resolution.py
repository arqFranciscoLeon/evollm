"""Prepare explicit, local derivations of inspected archived methods; no network."""
import ast
import difflib
import json
from pathlib import Path
from phase3.pilot_converter import ROOT, sha, encoded, exclusive, now

FIXES={
 'deepseek_v4pro/Aggressive_2':'Follow explicit inverted response branches rather than generic copy label.',
 'deepseek_v4pro/Aggressive_15':'Use last-round payoff, not cumulative score minus last payoff.',
 'deepseek_v4pro/Aggressive_19':'Otherwise D covers fewer than two prior observations.',
 'kimi_k25/Aggressive_3':'Latch permanent defection after cooperation phase is betrayed.',
 'kimi_k25/Aggressive_9':'Restore explicit final-round defection.',
 'kimi_k25/Aggressive_17':'Persist cooperation after threshold and defect permanently after betrayal.',
 'glm_51/Aggressive_7':'Copy each new rival action rather than locking the first copied action.',
 'glm_51/Aggressive_12':'Use last-round payoff rather than cumulative score minus last payoff.',
 'glm_51/Aggressive_17':'Final round is len(history)+1=1000.',
 'glm_51/Aggressive_19':'Preserve initial branches ordering D for the remainder of the game.',
 'glm_51/Aggressive_22':'Final round is len(history)+1=1000.',
}

def source_for(key):
    model,name=key.split('/')
    path=ROOT/f'phase3/inputs/archived/{model}_default_75.py'
    tree=ast.parse(path.read_text(encoding='utf-8-sig'))
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==name)
    fn=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='strategy')
    fn.decorator_list=[]
    return ast.unparse(fn)+'\n'

def replace_once(source,old,new):
    if source.count(old)!=1: raise ValueError('Transformation is not unique: '+old)
    return source.replace(old,new)

def fixed(key,old):
    if key=='deepseek_v4pro/Aggressive_2':
        return replace_once(old,'return opponent.history[-1] if opponent.history else axl.Action.D','return axl.Action.D if opponent.history[-1] == axl.Action.C else axl.Action.C')
    if key in ('deepseek_v4pro/Aggressive_15','glm_51/Aggressive_12'):
        return replace_once(old,'self.score - self.total_scores(self.history[-1:], opponent.history[-1:])[0]','self.total_scores(self.history[-1:], opponent.history[-1:])[0]')
    if key=='deepseek_v4pro/Aggressive_19':
        return replace_once(old,'if len(self.history) < 2 or len(opponent.history) < 2:\n        return axl.Action.C','if len(self.history) < 2 or len(opponent.history) < 2:\n        return axl.Action.D')
    if key=='kimi_k25/Aggressive_3':
        new=replace_once(old,'self._started_cooperating = False','self._started_cooperating = False\n        self._permanent_defect = False')
        new=replace_once(new,'    if self._started_cooperating:', '    if self._permanent_defect:\n        return axl.Action.D\n    if self._started_cooperating:')
        return replace_once(new,'        if opponent.history[-1] == axl.Action.D:\n            return axl.Action.D','        if opponent.history[-1] == axl.Action.D:\n            self._permanent_defect = True\n            return axl.Action.D')
    if key=='kimi_k25/Aggressive_9':
        return replace_once(old,"    if getattr(self, '_defect_forever', False):", "    if len(self.history) >= 999:\n        return axl.Action.D\n    if getattr(self, '_defect_forever', False):")
    if key=='kimi_k25/Aggressive_17':
        return '''def strategy(self, opponent: axl.player.Player) -> axl.Action:
    if self.first_round():
        self._cooperate_forever = False
        self._permanent_defect = False
        return axl.Action.D
    if self._permanent_defect:
        return axl.Action.D
    if self._cooperate_forever:
        if opponent.history[-1] == axl.Action.D:
            self._permanent_defect = True
            return axl.Action.D
        return axl.Action.C
    if len(opponent.history) >= 5 and self.history[-5:] == [axl.Action.D] * 5 and opponent.history[-5:] == [axl.Action.C] * 5:
        self._cooperate_forever = True
        return axl.Action.C
    return axl.Action.D
'''
    if key=='glm_51/Aggressive_7':
        return replace_once(old,'    self._locked_action = opponent.history[-1]\n    return self._locked_action','    return opponent.history[-1]')
    if key in ('glm_51/Aggressive_17','glm_51/Aggressive_22'):
        return replace_once(old,'if len(self.history) >= 1000:', 'if len(self.history) >= 999:')
    if key=='glm_51/Aggressive_19':
        return '''def strategy(self, opponent: axl.player.Player) -> axl.Action:
    if len(self.history) < 2:
        return axl.Action.D
    if opponent.history[0] == axl.Action.D or opponent.history[1] == axl.Action.C:
        return axl.Action.D
    if len(self.history) == 2:
        return axl.Action.C
    if opponent.history[2] == axl.Action.D:
        return axl.Action.D
    if len(self.history) >= 999:
        return axl.Action.D
    return axl.Action.C
'''
    raise ValueError(key)

def timing_source(lagged):
    guard='len(self.history) >= 2 and self.history[-2] == axl.Action.C' if lagged else 'self.history[-1] == axl.Action.C'
    return f'''def strategy(self, opponent: axl.player.Player) -> axl.Action:
    if self.first_round():
        self._defect_forever = False
        return axl.Action.D
    if {guard} and opponent.history[-1] == axl.Action.D:
        self._defect_forever = True
    if self._defect_forever:
        return axl.Action.D
    return opponent.history[-1]
'''

def threshold_source(k):
    return f'''def strategy(self, opponent: axl.player.Player) -> axl.Action:
    if self.first_round() or len(self.history) >= 990:
        return axl.Action.D
    if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
        return axl.Action.D
    if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
        return axl.Action.C
    if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
        return axl.Action.D
    if len(self.history) >= {k} and self.history[-{k}:] == [axl.Action.C] * {k} and opponent.history[-{k}:] == [axl.Action.C] * {k}:
        return axl.Action.D
    return axl.Action.C
'''

def main():
    review_path=ROOT/'phase3/inputs/semantic_review_chinese_v1.json'
    review=json.loads(review_path.read_bytes()); records={r['id']:r for r in review['cases']}
    for path,meta in review['sources'].items():
        if sha((ROOT/path).read_bytes())!=meta['sha256']: raise ValueError('Archive changed')
    out=ROOT/'phase3/chinese_resolution_v1'; out.mkdir(exist_ok=True)
    entries=[]
    for key,reason in FIXES.items():
        old=source_for(key); new=fixed(key,old); path=out/(key.replace('/','_')+'.py.txt')
        exclusive(path,new.encode())
        sid=key.replace('/','/default/')
        entries.append({'id':sid,'kind':'implementation_correction','reason':reason,
                        'library_sha256':records[sid]['library_sha256'],'original_method_sha256':records[sid]['method_source_sha256'],
                        'original_normalized_source_sha256':sha(old.encode()),'derived_path':str(path.relative_to(ROOT)),
                        'derived_sha256':sha(new.encode()),'diff':''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='archived_method_normalized',tofile=path.name))})
    for key,main_source,alt_source,decision in [
      ('kimi_k25/Aggressive_25',timing_source(False),timing_source(True),'same completed-round pair; alternative one-round lag'),
      ('glm_51/Aggressive_20',threshold_source(10),threshold_source(9),'last ten completed CC; alternative nine completed CC')]:
        sid=key.replace('/','/default/'); old=source_for(key)
        for label,source in [('primary',main_source),('alternative',alt_source)]:
            path=out/(key.replace('/','_')+'_'+label+'.py.txt'); exclusive(path,source.encode())
            entries.append({'id':sid,'kind':'adjudicated_'+label,'reason':decision,
                'library_sha256':records[sid]['library_sha256'],'original_method_sha256':records[sid]['method_source_sha256'],
                'derived_path':str(path.relative_to(ROOT)),'derived_sha256':sha(source.encode()),
                'diff':''.join(difflib.unified_diff(old.splitlines(True),source.splitlines(True),fromfile='archived_method_normalized',tofile=path.name))})
    exclusive(ROOT/'phase3/inputs/chinese_resolution_v1.json',encoded({
        'created_at':now(),'policy_sha256':sha((ROOT/'phase3/CHINESE_RESOLUTION_POLICY_v1.md').read_bytes()),
        'review_sha256':sha(review_path.read_bytes()),'preparer_sha256':sha(Path(__file__).read_bytes()),
        'excluded':[{'id':sid,'reason':'missing initial-history branch; no source reconstruction'} for sid in ('deepseek_v4pro/default/Aggressive_5','kimi_k25/default/Aggressive_12')],
        'eligible_count':298,'derivations':entries,'status':'prepared_for_local_validation','api_calls':0}))
    print(json.dumps({'corrections':11,'adjudicated_primaries':2,'alternatives':2,'excluded':2,'api_calls':0}))

if __name__=='__main__': main()
