"""Reviewed stateful adapter and prose-derived reference checks, no network.

Requires an explicit hash from source inspection before compiling a candidate.
The bounded syntax subset is a review aid, not an OS security sandbox.
"""
import ast
import hashlib
import sys
import axelrod as axl
from phase3.validate_pilot import ALLOWED

EXTRA = (ast.AugAssign, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Is, ast.IsNot,
         ast.For, ast.Break, ast.Continue, ast.Pass, ast.Tuple, ast.GeneratorExp,
         ast.ListComp, ast.comprehension, ast.IfExp)
PROTECTED = {'history','score','first_round','total_scores','classifier','name','match_attributes',
             '_history','_random'}
# Explicitly inspected boolean state in expanded responses 053, 069, 083, 087.
# These names are candidate-owned; runtime and other private attributes stay blocked.
REVIEWED_PRIVATE_STATE = {'_opponent_always_defect','_always_defect','_permanent_defect'}
BUILTINS = {'len':len,'sum':sum,'all':all,'any':any,'min':min,'max':max,'list':list,
            'tuple':tuple,'int':int,'bool':bool,'abs':abs}


def bounded_range(*args):
    r = range(*args)
    if len(r)>1001:
        raise ValueError('Range outside 1000-round review bounds')
    return r


def scores(mine, opponent):
    pay = {('C','C'):(3,3),('C','D'):(0,5),('D','C'):(5,0),('D','D'):(1,1)}
    pairs = [pay[str(a),str(b)] for a,b in zip(mine,opponent)]
    return sum(p[0] for p in pairs),sum(p[1] for p in pairs)


def compile_candidate(source, reviewed_sha256):
    if hashlib.sha256(source.encode()).hexdigest()!=reviewed_sha256:
        raise ValueError('Candidate is not the inspected source')
    tree = ast.parse(source)
    if len(tree.body)!=1 or not isinstance(tree.body[0],ast.FunctionDef):
        raise ValueError('One strategy function required')
    fn=tree.body[0]
    if (fn.name!='strategy' or [a.arg for a in fn.args.args]!=['self','opponent'] or fn.decorator_list
            or fn.args.defaults or fn.args.kwonlyargs or fn.args.posonlyargs or fn.args.vararg or fn.args.kwarg):
        raise ValueError('Unreviewed signature')
    for node in ast.walk(tree):
        if not isinstance(node,ALLOWED+EXTRA):
            raise ValueError('Syntax requires additional review: '+type(node).__name__)
        if isinstance(node,ast.FunctionDef) and node is not fn:
            raise ValueError('Nested functions require additional review')
        if isinstance(node,ast.Attribute):
            name=ast.unparse(node)
            count_base=node.value.value if isinstance(node.value,ast.Subscript) else node.value
            permitted = (name in {'axl.Action','axl.Action.C','axl.Action.D','axl.player','axl.player.Player',
                                'opponent.history','opponent.score','self.first_round','self.total_scores'}
                         or name.startswith(('self.history.','opponent.history.')) and node.attr in ('count','cooperations','defections')
                         or node.attr=='count' and ast.unparse(count_base) in ('self.history','opponent.history')
                         or isinstance(node.value,ast.Name) and node.value.id=='self')
            if not permitted or node.attr.startswith('__') or node.attr.startswith('_validation'):
                raise ValueError('Unreviewed attribute')
        if isinstance(node,ast.Call):
            name=ast.unparse(node.func)
            permitted = name in set(BUILTINS)|{'range','self.first_round','self.total_scores'}
            if isinstance(node.func,ast.Attribute) and node.func.attr=='count':
                # Only counts on history or history slices, not arbitrary objects.
                base=node.func.value
                if isinstance(base,ast.Subscript):
                    base=base.value
                permitted = ast.unparse(base) in ('self.history','opponent.history')
            if not permitted or node.keywords:
                raise ValueError('Unreviewed call')
        if isinstance(node,(ast.Assign,ast.AugAssign)):
            targets=node.targets if isinstance(node,ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target,ast.Name):
                    if target.id in set(BUILTINS)|{'range','axl','self','opponent'}:
                        raise ValueError('Cannot replace runtime binding')
                elif isinstance(target,ast.Attribute) and isinstance(target.value,ast.Name) and target.value.id=='self':
                    if target.attr in PROTECTED or target.attr.startswith('_') and target.attr not in REVIEWED_PRIVATE_STATE:
                        raise ValueError('Only public candidate-owned state may be assigned')
                else:
                    raise ValueError('Unreviewed assignment target')
        if isinstance(node,ast.Constant) and not (node.value is None or type(node.value) in (bool,int,float) and abs(node.value)<=10000):
            raise ValueError('Unreviewed constant')
    namespace={'axl':axl,'__builtins__':{**BUILTINS,'range':bounded_range}}
    exec(compile(tree,'<expanded-reviewed>','exec'),namespace)
    raw=namespace['strategy']

    class Candidate(axl.Player):
        name='Reviewed expanded candidate'
        classifier={'memory_depth':float('inf'),'stochastic':False,'long_run_time':False,
                    'inspects_source':False,'manipulates_source':False,'manipulates_state':False}

        def first_round(self):
            return len(self.history)==0

        def total_scores(self, mine, theirs):
            return scores(mine,theirs)

        def strategy(self,opponent):
            n=len(self.history)
            if n!=len(opponent.history):
                raise ValueError('Mismatched histories')
            if n==0:
                self._validation_scored=0
                self._validation_mine=0
                self._validation_theirs=0
            if self._validation_scored>n:
                raise ValueError('History shortened without reset')
            a,b=scores(self.history[self._validation_scored:],opponent.history[self._validation_scored:])
            self._validation_mine+=a
            self._validation_theirs+=b
            self._validation_scored=n
            self.score=self._validation_mine
            opponent.score=self._validation_theirs
            steps=0
            def trace(frame,event,arg):
                nonlocal steps
                if frame.f_code.co_filename=='<expanded-reviewed>' and event=='line':
                    steps+=1
                    if steps>30000:
                        raise ValueError('Candidate exceeded per-call step bound')
                return trace
            previous=sys.gettrace()
            try:
                sys.settrace(trace)
                action=raw(self,opponent)
            finally:
                sys.settrace(previous)
            if action not in (axl.Action.C,axl.Action.D):
                raise ValueError('Invalid action, no substitution')
            return action
    return Candidate


def reference(profile,mine,opp):
    """Operational interpretation of reviewed prose, independent of generated code."""
    n=len(opp); r=n+1
    last=opp[-1] if n else None
    if profile=='always_d': return 'D'
    if profile=='c_then_d': return 'C' if n==0 else 'D'
    aliases={'tft':'tft_C_none','tft_final':'tft_C_1000','tft_last10':'tft_C_991'}
    if profile in aliases: return reference(aliases[profile],mine,opp)
    if profile.startswith('tft_'):
        _,start,end=profile.split('_')
        return start if not n else ('D' if end!='none' and r>=int(end) else last)
    if profile=='grim_start_d': return 'D' if not n or 'D' in opp else 'C'
    if profile.startswith('score_'):
        _,threshold,end=profile.split('_'); threshold=int(threshold)
        a,b=scores(mine,opp)
        trigger=a-b>10 if threshold==10 else a-b>=20
        return 'D' if not n or last=='D' or r>=int(end) or trigger else 'C'
    if profile.startswith('fraction_D_'):
        _,_,pct,end=profile.split('_')
        return 'D' if not n or last=='D' or r>=int(end) or 100*opp.count('D')>int(pct)*n else 'C'
    if profile.startswith('fraction_C_'):
        _,_,pct,op,mode=profile.split('_'); pct=int(pct)
        if not n: return 'C'
        def meets(k):
            left=100*opp[:k].count('D'); right=pct*k
            return left>=right if op=='ge' else left>right
        trigger=any(meets(k) for k in range(1,n+1)) if mode=='latch' else meets(n)
        return 'D' if trigger or last=='D' or (pct==60 and mode=='latch' and r>=998) else 'C'
    if profile=='window8of10': return 'C' if not n else ('D' if n>=10 and opp[-10:].count('D')>=8 else last)
    if profile in ('anti_tft','anti_tft_latch3'):
        return 'D' if not n or profile.endswith('latch3') and 'DDD' in opp or last=='C' else 'C'
    if profile=='dd_to_c': return 'C' if n and mine[-1]==last=='D' else 'D'
    if profile=='two_total_D': return 'D' if r>=995 or opp.count('D')>=2 or last=='D' else 'C'
    if profile in ('window_or_998','window_or_996'):
        return 'D' if r>=int(profile[-3:]) or 'D' in opp[-2:] else 'C'
    if profile=='two_lags_probe10': return 'D' if r>=998 or 'D' in opp[-2:] or n>=10 and opp[-10:]=='C'*10 else 'C'
    if profile=='cyclebreak_probe3':
        if r==1000: return 'D'
        if n>=2 and mine[-2:]==opp[-2:]=='DD': return 'C'
        return 'D' if last=='D' or n>=3 and opp[-3:]=='CCC' else 'C'
    if profile in ('probe3','probe3_D_final'):
        if r>=(991 if profile=='probe3' else 1000): return 'D'
        if not n: return 'C' if profile=='probe3' else 'D'
        return 'D' if last=='D' or n>=3 and opp[-3:]=='CCC' else 'C'
    if profile=='probe4_self':
        return 'D' if r==1000 or n and mine[-1]=='C' and last=='D' or n>=4 and opp[-4:]=='CCCC' else 'C'
    raise ValueError('Unknown prose profile: '+profile)


def replay(cls,mine,opp,profile):
    """Invoke at every prefix, then append controlled actions to preserve state.

    Histories are counterfactual test inputs; candidate actions are not used to
    replace the controlled history. No claim of on-policy reachability is made.
    """
    if len(mine)!=len(opp) or len(mine)>999 or set(mine+opp)-set('CD'):
        raise ValueError('Invalid controlled history')
    player,other=cls(),axl.Cooperator()
    failures=[]
    actions=[]
    for n in range(len(mine)+1):
        expected=reference(profile,mine[:n],opp[:n])
        actual=str(player.strategy(other))
        actions.append(actual)
        if actual!=expected:
            failures.append({'round':n+1,'expected':expected,'actual':actual})
        if n<len(mine):
            a=axl.Action.C if mine[n]=='C' else axl.Action.D
            b=axl.Action.C if opp[n]=='C' else axl.Action.D
            player.update_history(a,b); other.update_history(b,a)
    return {'checks':len(mine)+1,'failures':failures,'actions_sha256':hashlib.sha256(''.join(actions).encode()).hexdigest()}
