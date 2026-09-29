"""Bounded sequential conversion with auditable settlement; offline status by default."""
import argparse
import json
import os
from pathlib import Path
import platform
import uuid

from phase3.pilot_converter import ROOT, assess, encoded, exclusive, now, sha, transport, RETURNED_MODELS

PLAN = ROOT/'phase3/inputs/uniform_requests_v3.json'
PLAN_SHA256 = '122202af19a17ac474ec19c2e8c77d35c1cc50b95e503ccbf24d5bd8971eaad2'
RUN_DIR = ROOT/'phase3/conversion_runs/uniform_v3'
RETURNED_MODELS = {'gpt-5.4-mini-2026-03-17'}  # Require one actual snapshot across both cohorts.
RESERVE = 318432000  # nano-USD; includes full context + 4096 output tokens
CEILING = 2000000000
OK = 'candidate_pending_fidelity_and_runtime'


def load_plan():
    data = PLAN.read_bytes()
    if sha(data) != PLAN_SHA256:
        raise ValueError('Frozen expanded plan changed')
    plan = json.loads(data)
    for relative, expected in plan['sources'].items():
        if sha((ROOT/relative).read_bytes()) != expected:
            raise ValueError('Prepared source changed: '+relative)
    for item in plan['requests']:
        if sha(encoded(item['payload'])) != item['payload_sha256']:
            raise ValueError('Payload changed')
    return plan, data


def billed_nano(body):
    """Price only traceable standard-service text usage, using exact integers."""
    try:
        response = json.loads(body)
        if response.get('model') not in RETURNED_MODELS or response.get('service_tier','default') != 'default':
            return None
        usage = response['usage']
        prompt, completion, total = (usage[k] for k in ('prompt_tokens','completion_tokens','total_tokens'))
        cached = (usage.get('prompt_tokens_details') or {}).get('cached_tokens',0)
        if any(type(x) is not int for x in (prompt,completion,total,cached)):
            return None
        if not (0 <= cached <= prompt <= 400000 and 0 <= completion <= 4096 and total == prompt+completion):
            return None
        return (prompt-cached)*750 + cached*75 + completion*4500
    except (ValueError,KeyError,TypeError,AttributeError):
        return None


def classify(http_status, body, redacted=False):
    cost = billed_nano(body) if http_status == 200 and not redacted else None
    status = assess(body) if http_status == 200 and not redacted else 'http_error_or_redacted_response'
    if cost is None and status == OK:
        status = 'unverifiable_usage_or_service_tier'
    return {'status':status, 'cost_nano_usd':cost, 'charged_to_local_budget_nano_usd':RESERVE if cost is None else cost}


def ledger(directory, plan):
    if not directory.exists():
        return {'attempts':0,'settled_nano_usd':0,'reserved_nano_usd':0,'blocked':False,'completed':0}
    anchor = directory/'plan.json'
    if not anchor.exists() or sha(anchor.read_bytes()) != PLAN_SHA256:
        raise ValueError('Run is not anchored to this plan')
    folders = sorted(p for p in directory.iterdir() if p.is_dir())
    if [p.name for p in folders] != [f'{i:03d}' for i in range(1,len(folders)+1)] or len(folders)>len(plan['requests']):
        raise ValueError('Attempt sequence has gaps or unexpected directories')
    state = {'attempts':len(folders),'settled_nano_usd':0,'reserved_nano_usd':0,'blocked':False,'completed':0}
    for folder,item in zip(folders,plan['requests']):
        request_path = folder/'request.json'
        if not request_path.exists():
            state['reserved_nano_usd'] += RESERVE
            state['blocked'] = True
            continue
        request = json.loads(request_path.read_bytes())
        if (request['strategy_id']!=item['id'] or encoded(request['payload'])!=encoded(item['payload'])
                or request['reservation_nano_usd']!=RESERVE
                or request['executor_sha256']!=sha(Path(__file__).read_bytes())):
            raise ValueError('Attempt request changed')
        receipt_path = folder/'receipt.json'
        if not receipt_path.exists():
            state['reserved_nano_usd'] += RESERVE
            state['blocked'] = True
            continue
        receipt = json.loads(receipt_path.read_bytes())
        body = (folder/'response.bin').read_bytes()
        result = classify(receipt['http_status'],body,receipt['credential_echo_redacted'])
        if sha(body)!=receipt['response_sha256'] or any(receipt[k]!=v for k,v in result.items()):
            raise ValueError('Response or settlement changed')
        if result['cost_nano_usd'] is None:
            state['reserved_nano_usd'] += RESERVE
        else:
            state['settled_nano_usd'] += result['cost_nano_usd']
        if result['status']!=OK:
            state['blocked'] = True
        else:
            if (folder/'candidate.py.txt').read_bytes()!=json.loads(body)['choices'][0]['message']['content'].encode():
                raise ValueError('Candidate differs from response')
            state['completed'] += 1
    return state


def run(directory=RUN_DIR, send=transport, api_key=None, max_new=572):
    plan,data = load_plan()
    if not 1 <= max_new <= 572:
        raise ValueError('max_new must be 1..572')
    directory.mkdir(parents=True,exist_ok=True)
    lock = directory/'running.lock'
    exclusive(lock,encoded({'pid':os.getpid(),'started_at':now()}))
    try:
        anchor = directory/'plan.json'
        if not anchor.exists():
            exclusive(anchor,data)
        state = ledger(directory,plan)
        if state['blocked']:
            raise RuntimeError('Previous attempt requires reconciliation; no automatic retry')
        stop = min(len(plan['requests']),state['attempts']+max_new)
        for index in range(state['attempts'],stop):
            used = state['settled_nano_usd']+state['reserved_nano_usd']
            if used+RESERVE > CEILING:
                return {**state,'stop_reason':'budget_ceiling'}
            key = api_key or os.environ.get('OPENAI_API_KEY')
            if not key:
                raise RuntimeError('OPENAI_API_KEY unavailable; no request sent')
            item = plan['requests'][index]
            folder = directory/f'{index+1:03d}'
            folder.mkdir()
            exclusive(folder/'request.json',encoded({'attempt_id':str(uuid.uuid4()), 'started_at':now(),
                      'strategy_id':item['id'],'payload':item['payload'],'reservation_nano_usd':RESERVE,
                      'python':platform.python_version(),'executor_sha256':sha(Path(__file__).read_bytes()),
                      'transport':'stdlib HTTPS, no automatic retries'}))
            try:
                http_status,body,request_id = send(item['payload'],key)
            except Exception as exc:
                exclusive(folder/'transport_error.json',encoded({'type':type(exc).__name__,'finished_at':now(),
                          'cost_status':'unknown_full_reservation_retained'}))
                raise RuntimeError('Transport outcome uncertain; stopped without retry') from None
            redacted = key.encode() in body
            if redacted:
                body = body.replace(key.encode(),b'[REDACTED_API_KEY]')
            exclusive(folder/'response.bin',body)
            result = classify(http_status,body,redacted)
            if result['status']==OK:
                exclusive(folder/'candidate.py.txt',json.loads(body)['choices'][0]['message']['content'].encode())
            exclusive(folder/'receipt.json',encoded({**result,'http_status':http_status,'request_id':request_id,
                      'credential_echo_redacted':redacted,'response_sha256':sha(body),'finished_at':now()}))
            # Reconstruct rather than trusting a mutable running total.
            state = ledger(directory,plan)
            print(json.dumps({'attempt':index+1,'status':result['status'],
                              'settled_usd':state['settled_nano_usd']/1e9}),flush=True)
            if state['blocked']:
                raise RuntimeError('Expanded conversion stopped: '+result['status'])
        return {**state,'stop_reason':'complete' if state['completed']==572 else 'max_new'}
    finally:
        lock.unlink()


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live',action='store_true')
    parser.add_argument('--max-new',type=int,default=572)
    args = parser.parse_args()
    if args.live:
        print(json.dumps(run(max_new=args.max_new)))
    else:
        plan,_ = load_plan()
        print(json.dumps({'plan_verified':True,'planned_requests':len(plan['requests']),
                          'budget_usd':CEILING/1e9,'state':ledger(RUN_DIR,plan),'api_calls_this_command':0}))
