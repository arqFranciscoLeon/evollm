"""Bounded process dispatch on one Linux host; no Modal deployment or billing API.

One coordinator owns the output directory. Cloud container scheduling and a
verified provider spending limit are additional requirements, not supplied here.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor,wait,FIRST_COMPLETED
import hashlib
import json
import multiprocessing
from pathlib import Path

from phase3.reuse_batches_v1 import sha,validate_receipt,save_receipt
from phase3.reuse_worker_v1 import run_owned_batch


def file_sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def execute_one(args):
    receipt=run_owned_batch(*args)
    return {'matches':len(receipt['results']),'batch_sha256':receipt['batch_sha256']}


def dispatch(plan_dir,result_dir,registration_path,*,workers=2,max_batches=1):
    if type(workers) is not int or not 1<=workers<=4: raise ValueError('Workers must be 1..4')
    if type(max_batches) is not int or max_batches<1: raise ValueError('Explicit positive batch cap required')
    plan_dir=Path(plan_dir); result_dir=Path(result_dir)
    manifest=json.loads((plan_dir/'manifest.json').read_bytes())
    context=json.loads((plan_dir/'context.json').read_bytes())
    registration=json.loads(Path(registration_path).read_bytes())
    if manifest['context_sha256']!=sha(context): raise ValueError('Plan context changed')
    # The registration record anchors both scientific context and entire batch inventory.
    if (registration.get('context_sha256')!=sha(context)
            or registration.get('plan_manifest_sha256')!=file_sha(plan_dir/'manifest.json')
            or not registration.get('public_registration_url') or not registration.get('frozen_git_commit')):
        raise ValueError('Frozen/public registration for this exact plan required')
    entries=manifest['batches']
    if len({e['path'] for e in entries})!=len(entries): raise ValueError('Duplicate batch path')
    pending=[]
    # Validate all saved evidence before starting any process.
    for entry in entries:
        name=entry['path']
        if Path(name).name!=name: raise ValueError('Batch path must be a filename')
        path=plan_dir/name
        if file_sha(path)!=entry['file_sha256']: raise ValueError('Batch file changed')
        batch=json.loads(path.read_bytes()); out=result_dir/name
        if out.exists():
            receipt=json.loads(out.read_bytes()); validate_receipt(receipt,batch,context)
            if len(receipt['results'])==len(batch['jobs']): continue
        pending.append((str(plan_dir/'context.json'),str(path),str(out),str(registration_path)))
    result_dir.mkdir(parents=True,exist_ok=True)
    lock=result_dir/'coordinator.lock'
    try:
        with lock.open('x') as stream: stream.write(sha(context))
    except FileExistsError:
        raise ValueError('Coordinator ownership already claimed; inspect stale lock before recovery')
    selected=pending[:max_batches]; complete=[]; failed=[]
    try:
        with ProcessPoolExecutor(max_workers=workers,mp_context=multiprocessing.get_context('spawn')) as pool:
            cursor=iter(selected); running={}
            def fill():
                while len(running)<workers:
                    args=next(cursor,None)
                    if args is None: break
                    running[pool.submit(execute_one,args)]=args[1]
            fill()
            while running:
                done,_=wait(running,return_when=FIRST_COMPLETED)
                for future in done:
                    path=running.pop(future)
                    try: complete.append({'path':path,**future.result()})
                    except Exception as exc: failed.append({'path':path,'error':str(exc)})
                # Already running batches finish and persist; no more submissions after error.
                if not failed: fill()
    finally:
        lock.unlink()
    report={'context_sha256':sha(context),'completed_batches':complete,'failed_batches':failed,
            'pending_before_dispatch':len(pending),'submitted_cap':max_batches,
            'scope':'Process execution report, not a cloud billing receipt'}
    save_receipt(result_dir/'last_dispatch.json',report)
    if failed: raise RuntimeError('Batch failure; inspect last_dispatch.json before resuming')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan',required=True); parser.add_argument('--results',required=True)
    parser.add_argument('--registration',required=True); parser.add_argument('--max-batches',type=int,required=True)
    parser.add_argument('--workers',type=int,default=2)
    args=parser.parse_args()
    print(json.dumps(dispatch(args.plan,args.results,args.registration,workers=args.workers,max_batches=args.max_batches)))
