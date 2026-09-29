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
# Explicitly inspected candidate state in uniform responses 019, 066, 121,
# 123, 180, 280 and 284; previous expanded control states remain supported.
# These names are candidate-owned; runtime and other private attributes stay blocked.
REVIEWED_PRIVATE_STATE = {'_cooperate_test_round', '_opp_coop_2_and_3', '_bait_round', '_always_defect', '_punish_forever', '_coop_after_start', '_tested_mutual_cooperation', '_permanent_defect', '_opponent_defect_forever', '_opponent_always_defect', '_unconditionally_cooperative'}
BUILTINS = {'len':len,'sum':sum,'all':all,'any':any,'min':min,'max':max,'list':list,
            'tuple':tuple,'int':int,'bool':bool,'abs':abs,'enumerate':enumerate}
# Inspected response 408: boolean cooperation state and bounded history counter.
REVIEWED_PRIVATE_STATE |= {'_permanent_cooperate', '_coop_streak_while_defecting'}
# Response 529 boolean; response 540 enumerates completed opponent history.
REVIEWED_PRIVATE_STATE.add('_sustain_cooperation')
# Inspected responses 549, 561 and 563.
REVIEWED_PRIVATE_STATE |= {'_defect_until_cooperate', '_coop_streak',
                           '_started_cooperating', '_always_cooperate_until_end'}


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
                         or name=='last_100.count'
                         or isinstance(node.value,ast.Name) and node.value.id=='self')
            if not permitted or node.attr.startswith('__') or node.attr.startswith('_validation'):
                raise ValueError('Unreviewed attribute')
        if isinstance(node,ast.Call):
            name=ast.unparse(node.func)
            permitted = name in set(BUILTINS)|{'range','self.first_round','self.total_scores'}
            if name=='getattr':
                # Response 440: literal read of its initialized boolean only.
                permitted = (len(node.args)==3 and ast.unparse(node.args[0])=='self'
                    and isinstance(node.args[1],ast.Constant) and node.args[1].value in ('_always_defect','_always_cooperate_until_end')
                    and isinstance(node.args[2],ast.Constant) and node.args[2].value is False)
            if isinstance(node.func,ast.Attribute) and node.func.attr=='count':
                # Only counts on history or history slices, not arbitrary objects.
                base=node.func.value
                if isinstance(base,ast.Subscript):
                    base=base.value
                permitted = ast.unparse(base) in ('self.history','opponent.history','last_100')
            if not permitted or node.keywords:
                raise ValueError('Unreviewed call')
        if isinstance(node,(ast.Assign,ast.AugAssign)):
            targets=node.targets if isinstance(node,ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target,ast.Tuple):
                    # Reviewed payoff unpacking (120, 246), local names only.
                    if not all(isinstance(t,ast.Name) and t.id not in set(BUILTINS)|{'range','axl','self','opponent'} for t in target.elts):
                        raise ValueError('Unreviewed unpacking target')
                    continue
                if isinstance(target,ast.Name):
                    if target.id in set(BUILTINS)|{'range','axl','self','opponent'}:
                        raise ValueError('Cannot replace runtime binding')
                elif isinstance(target,ast.Attribute) and isinstance(target.value,ast.Name) and target.value.id=='self':
                    if target.attr in PROTECTED or target.attr.startswith('_') and target.attr not in REVIEWED_PRIVATE_STATE:
                        raise ValueError('Only public candidate-owned state may be assigned')
                else:
                    raise ValueError('Unreviewed assignment target')
        if isinstance(node,ast.Constant) and not (node.value is None or node.value in ('_always_defect','_always_cooperate_until_end') or type(node.value) in (bool,int,float) and abs(node.value)<=10000):
            raise ValueError('Unreviewed constant')
    namespace={'axl':axl,'__builtins__':{**BUILTINS,'range':bounded_range,'getattr':getattr}}
    exec(compile(tree,'<uniform-reviewed>','exec'),namespace)
    raw=namespace['strategy']

    class Candidate(axl.Player):
        name='Reviewed uniform candidate'
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
                if frame.f_code.co_filename=='<uniform-reviewed>' and event=='line':
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


