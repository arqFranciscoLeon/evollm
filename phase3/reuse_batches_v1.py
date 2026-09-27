"""Exact source/identity reuse across scenarios; independent resumable batches.

No cloud calls or implicit tournament execution. This module preserves the old executor.
"""
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
from phase3.execute_uniform import checked_payload, encoded
from phase3.runtime import play_pair, seed_for


def sha(value):
    return hashlib.sha256(encoded(value).encode()).hexdigest()


def make_context(scenarios, *, provenance, scope, turns=1000, seed=20260913):
    """scenarios maps an integer scenario to {full_identity: source_sha256}."""
    if scope not in ('synthetic_test','selected_diagnostic','full_round_robin'):
        raise ValueError('Explicit scope required')
    if type(turns) is not int or turns<1 or type(seed) is not int:
        raise ValueError('Invalid turns/seed')
    if not scenarios or any(type(mask) is not int or mask<0 for mask in scenarios):
        raise ValueError('Nonnegative integer scenario ids required')
    ids=sorted(next(iter(scenarios.values())))
    if not ids or any(sorted(sources)!=ids for sources in scenarios.values()):
        raise ValueError('Every scenario must have identical identities')
    if any(not isinstance(s,str) or not s for sources in scenarios.values() for s in sources.values()):
        raise ValueError('Source identity missing')
    return {'version':1,'scope':scope,'turns':turns,'seed':seed,'repetitions':1,
            'game':{'R':3,'S':0,'T':5,'P':1},'noise':0,'ids':ids,
            'scenario_sources':{str(k):scenarios[k] for k in sorted(scenarios)},
            'provenance':provenance,'implementation_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def iter_jobs(context, pairs=None):
    ids=context['ids']; signature=sha(context)
    if context['scope']=='selected_diagnostic' and pairs is None:
        raise ValueError('Diagnostic selection required')
    if context['scope']=='full_round_robin' and pairs is not None:
        raise ValueError('Full schedule cannot have selected pairs')
    if pairs is None:
        schedule=itertools.combinations_with_replacement(ids,2)
    else:
        schedule=sorted({tuple(sorted(p)) for p in pairs})
        if not schedule or any(len(p)!=2 or any(s not in ids for s in p) for p in schedule):
            raise ValueError('Invalid pair selection')
    for first,second in schedule:
        variants={}
        for mask,sources in context['scenario_sources'].items():
            # For self-play both seats always use the same scenario's source.
            variants.setdefault((sources[first],sources[second]),[]).append(int(mask))
        for (left,right),masks in sorted(variants.items()):
            identity={'context_sha256':signature,'first':first,'second':second,
                      'source_i':left,'source_j':right,'seed':seed_for(context['seed'],first,second,0)}
            yield {**identity,'key':sha(identity),'scenarios':sorted(masks)}


def batches(context, size=250, pairs=None):
    if type(size) is not int or not 1<=size<=1000: raise ValueError('Batch size must be 1..1000')
    iterator=iter_jobs(context,pairs); signature=sha(context)
    for index in itertools.count():
        jobs=list(itertools.islice(iterator,size))
        if not jobs: break
        body={'context_sha256':signature,'index':index,'jobs':jobs}
        yield {**body,'batch_sha256':sha(body)}


def check_batch(batch, context):
    signature=sha(context)
    body={k:batch[k] for k in ('context_sha256','index','jobs')}
    if body['context_sha256']!=signature or sha(body)!=batch['batch_sha256']:
        raise ValueError('Batch/context integrity mismatch')
    if not batch['jobs'] or len(batch['jobs'])>1000: raise ValueError('Invalid batch size')
    keys=set()
    for job in batch['jobs']:
        identity={k:job[k] for k in ('context_sha256','first','second','source_i','source_j','seed')}
        first,second=job['first'],job['second']
        if (job['context_sha256']!=signature or sha(identity)!=job['key'] or job['key'] in keys
                or first>second or first not in context['ids'] or second not in context['ids']
                or job['seed']!=seed_for(context['seed'],first,second,0)):
            raise ValueError('Invalid/repeated job')
        expected=[int(mask) for mask,s in context['scenario_sources'].items()
                  if s[first]==job['source_i'] and s[second]==job['source_j']]
        if not expected or job['scenarios']!=sorted(expected): raise ValueError('Wrong scenario attribution')
        keys.add(job['key'])


def validate_receipt(receipt, batch, context, require_complete=False):
    check_batch(batch,context)
    if (receipt['batch_sha256']!=batch['batch_sha256']
            or receipt['context_sha256']!=sha(context)):
        raise ValueError('Receipt belongs to another batch/context')
    rows=receipt['results']; jobs=batch['jobs']
    if len(rows)>len(jobs): raise ValueError('Unexpected result count')
    for row,job in zip(rows,jobs):
        if row['key']!=job['key'] or row['job_sha256']!=sha(job): raise ValueError('Result identity changed')
        if row['status']=='error':
            raise ValueError('Recorded error blocks automatic resume')
        if row['status']!='ok': raise ValueError('Unknown result status')
        checked_payload(row['payload'],context['turns'])
        if row['payload_sha256']!=sha(row['payload']): raise ValueError('Result payload changed')
    if require_complete and len(rows)!=len(jobs): raise ValueError('Incomplete batch')


def execute_batch(batch, context, resolve, *, previous=None, checkpoint=None, max_new=None):
    """One worker owns a batch; resolve(id, source_hash) returns a fresh-instance factory.

    Checkpoint after every completed match; failed matches are explicit, never replaced.
    Retries following machine interruption may recompute an uncommitted match.
    """
    if max_new is not None and (type(max_new) is not int or max_new<0): raise ValueError('Invalid match cap')
    check_batch(batch,context)
    receipt=previous or {'batch_sha256':batch['batch_sha256'],'context_sha256':sha(context),'results':[]}
    receipt=json.loads(encoded(receipt))
    validate_receipt(receipt,batch,context)
    remaining=batch['jobs'][len(receipt['results']):]
    if max_new is not None: remaining=remaining[:max_new]
    for job in remaining:
        row={'key':job['key'],'job_sha256':sha(job)}
        try:
            result=play_pair(resolve(job['first'],job['source_i']),resolve(job['second'],job['source_j']),
                             context['turns'],job['seed'])
            checked_payload(result,context['turns'])
            row.update(status='ok',payload=result,payload_sha256=sha(result))
        except Exception as exc:
            row.update(status='error',error=type(exc).__name__+': '+str(exc))
        receipt['results'].append(row)
        if checkpoint is not None: checkpoint(receipt)
        if row['status']=='error': raise RuntimeError(row['error'])
    return receipt


def save_receipt(path, receipt):
    """Atomic checkpoint on a local filesystem; caller provides single-writer ownership."""
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix('.tmp')
    with temp.open('w',encoding='utf-8') as stream:
        stream.write(encoded(receipt)); stream.flush()
        import os
        os.fsync(stream.fileno())
    temp.replace(path)


def export_scenario(context, mask, batch_receipts):
    """Stream verified batches, allocating only one scenario's matrices at a time."""
    if context['scope']=='selected_diagnostic': raise ValueError('Diagnostics cannot enter full matrices')
    if str(mask) not in context['scenario_sources']: raise ValueError('Unknown scenario')
    ids=context['ids']; positions={sid:i for i,sid in enumerate(ids)}
    c=np.zeros((len(ids),len(ids))); payoff=np.zeros_like(c); seen=set()
    for batch,receipt in batch_receipts:
        validate_receipt(receipt,batch,context,require_complete=True)
        for job,row in zip(batch['jobs'],receipt['results']):
            if mask not in job['scenarios']: continue
            pair=(job['first'],job['second'])
            if pair in seen: raise ValueError('Repeated scenario pair')
            seen.add(pair); i,j=(positions[s] for s in pair); p=row['payload']
            c[i,j]=c[j,i]=p['CC']/context['turns']
            payoff[i,j]=p['payoff_i']
            if i!=j: payoff[j,i]=p['payoff_j']
    if len(seen)!=len(ids)*(len(ids)+1)//2: raise ValueError('Incomplete scenario matrix')
    return {'ids':ids,'models':[s.split('/')[0] for s in ids],
            'attitudes':[s.split('/')[-1].split('_')[0] for s in ids],
            'cooperation':c,'payoff':payoff}
