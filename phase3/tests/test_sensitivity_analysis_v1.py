import itertools
import numpy as np
import pytest
from phase3.analyze_phase3 import ATTITUDES, h7_statistic
from phase3.sensitivity_analysis_v1 import ast_group, duplicate_sensitivity, exclusion_bounds


def sample():
    models = [m for m in ('a', 'b') for a in ATTITUDES for _ in range(2)]
    attitudes = [a for m in ('a', 'b') for a in ATTITUDES for _ in range(2)]
    rng = np.random.default_rng(21)
    c = rng.random((12, 12)); c = (c+c.T)/2
    return c, models, attitudes


def test_unique_groups_reduce_to_primary():
    c, m, a = sample()
    assert duplicate_sensitivity(c, m, a, list(map(str, range(12))))['difference'] == pytest.approx(h7_statistic(c,m,a))


def test_one_template_per_cell_is_defined():
    c,m,a = sample()
    assert duplicate_sensitivity(c,m,a,['same']*12)['difference'] == pytest.approx(h7_statistic(c,m,a))


def test_weighted_matches_explicit_pair_enumeration():
    c,m,a = sample()
    m += ['a']; a += ['Aggressive']
    rng = np.random.default_rng(1); c=rng.random((13,13)); c=(c+c.T)/2
    groups = list(map(str,range(12)))+['0']
    weights = [0.5]+[1.0]*11+[0.5]
    def mean(x,y,b,d):
        pairs=[(i,j) for i in range(13) for j in range(13) if i!=j and m[i]==x and m[j]==y and a[i]==b and a[j]==d]
        return sum(c[i,j]*weights[i]*weights[j] for i,j in pairs)/sum(weights[i]*weights[j] for i,j in pairs)
    contrasts=[]
    for b,d in itertools.combinations_with_replacement(ATTITUDES,2):
        for x,y in [('a','b'),('b','a')]:
            contrasts.append(mean(x,x,b,d)-(mean(x,y,b,d)+mean(x,y,d,b))/2)
    assert duplicate_sensitivity(c,m,a,groups)['difference']==pytest.approx(np.mean(contrasts))


def test_bounds_collapse_without_exclusions():
    c,m,a=sample(); result=exclusion_bounds(c,m,a,2)
    assert result['lower']==pytest.approx(h7_statistic(c,m,a))
    assert result['upper']==pytest.approx(result['lower'])


def test_bounds_contain_completions_and_extremes():
    c,m,a=sample(); bounds=exclusion_bounds(c,m,a,3)
    full_m=m+['a']*3+['b']*3; full_a=a+list(ATTITUDES)*2
    for mode in ['lower','upper','random']:
        rng=np.random.default_rng(7); full=rng.random((18,18)); full=(full+full.T)/2
        if mode!='random':
            for i in range(18):
                for j in range(18):
                    full[i,j]=float((full_m[i]==full_m[j]) == (mode=='upper'))
        full[:12,:12]=c
        value=h7_statistic(full,full_m,full_a)
        assert bounds['lower']-1e-12 <= value <= bounds['upper']+1e-12
        if mode!='random': assert value==pytest.approx(bounds[mode])


def test_diagonal_ignored():
    c,m,a=sample(); original=exclusion_bounds(c,m,a,3)
    np.fill_diagonal(c,np.nan)
    assert exclusion_bounds(c,m,a,3)==original
    assert np.isfinite(duplicate_sensitivity(c,m,a,['x']*12)['difference'])


def test_ast_definition():
    assert ast_group('x = 1 # comment')==ast_group('x=1')
    assert ast_group('x=1')!=ast_group('y=1')


def test_reject_invalid_inputs():
    c,m,a=sample()
    with pytest.raises(ValueError): duplicate_sensitivity(c,m,a,[])
    with pytest.raises(ValueError): exclusion_bounds(c,m,a,1)
    c[0,1]=np.nan
    with pytest.raises(ValueError): exclusion_bounds(c,m,a,3)
