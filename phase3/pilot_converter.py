"""Prepare offline; explicitly run a bounded, resumable conversion pilot.

Transport uses Python stdlib HTTPS, with no SDK or automatic retries. Generated
code is archived as text and parsed, never executed by this module.
"""
import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import urllib.error
import urllib.request
import uuid

from phase3.review_semantics import ROOT, check_artifacts

ENDPOINT = 'https://api.openai.com/v1/chat/completions'
MODEL = 'gpt-5.4-mini'
RETURNED_MODELS = {MODEL, 'gpt-5.4-mini-2026-03-17'}
MAX_OUTPUT = 4096
# Reserve the entire documented context as input, deliberately overestimating.
# Costs use integer micro-USD, avoiding floating-point budget comparisons.
RESERVE_MICRO_USD = 300000 + MAX_OUTPUT * 4500 // 1000
BUDGET_MICRO_USD = 4000000
SYSTEM = ('You are an AI assistant with expertise in game theory and programming. '
          'Your task is to implement the strategy description provided by the user as an algorithm.')
ADDENDUM = '''
Phase 3 pilot interpretation contract (an explicit addition to the historical prompt):
The current round is len(self.history) + 1; histories contain completed rounds only.
A condition requiring k previous rounds applies only when at least k rounds exist.
Follow explicit initial/final rules and stated priority. Do not add endgame defection,
forgiveness, randomization, or missing rules. Do not improve the strategy.
If the description does not specify an unambiguous action, return exactly
UNCONVERTIBLE: followed by the missing condition, instead of inventing code.
'''


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)+'\n').encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def exclusive(path, data):
    with path.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def prepare(destination):
    check_artifacts()
    inputs = ROOT/'phase3/inputs'
    review = json.loads((inputs/'semantic_review_v1.json').read_text(encoding='utf-8'))
    # Extract only two inspected pure prompt functions; do not import clients or
    # generation modules with logging side effects.
    source_path = ROOT/'src/evollm/prompts.py'
    tree = ast.parse(source_path.read_text(encoding='utf-8'))
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and
             n.name in ('create_game_information', 'create_algorithm_prompt')]
    assert len(nodes) == 2
    module = ast.parse('from __future__ import annotations')
    module.body.extend(nodes)
    scope = {}
    exec(compile(module, '<inspected-prompt-functions>', 'exec'), scope)
    class Classic:
        def RPST(self):
            return 3, 1, 0, 5
    requests = []
    for case in review['cases']:
        if case['cohort'] != 'pilot':
            continue
        if case['status'] != 'eligible_prose':
            raise ValueError('Pilot contains unreviewed or incomplete prose')
        prompt = scope['create_algorithm_prompt'](case['prose_exact_extracted'], Classic(), 1000, 0)
        payload = {'model': MODEL, 'messages': [{'role': 'system', 'content': SYSTEM},
                                              {'role': 'user', 'content': prompt+ADDENDUM}],
                   'temperature': 0, 'reasoning_effort': 'none', 'max_completion_tokens': MAX_OUTPUT,
                   'n': 1, 'stream': False, 'store': False, 'service_tier': 'default'}
        if len(encoded(payload)) > 16000:
            raise ValueError('Unexpectedly large pilot request')
        requests.append({'strategy_id': case['id'], 'prose_sha256': case['prose_sha256'],
                         'payload': payload, 'payload_sha256': sha(encoded(payload))})
    assert len(requests) == 12
    plan = {'schema': 1, 'status': 'prepared_not_called', 'endpoint': ENDPOINT,
            'model': MODEL, 'accepted_returned_models': sorted(RETURNED_MODELS),
            'requests': requests, 'budget_micro_usd': BUDGET_MICRO_USD,
            'reserve_per_attempt_micro_usd': RESERVE_MICRO_USD,
            'max_requests': 12, 'automatic_retries': 0, 'timeout_seconds': 60,
            'price_basis': {'verified_date': '2026-09-13', 'input_usd_per_million': 0.75,
                            'output_usd_per_million': 4.50, 'input_context_ceiling': 400000,
                            'source': 'https://developers.openai.com/api/docs/models/gpt-5.4-mini',
                            'limit_scope': 'Local reservation at listed standard prices, not an account billing cap. No discounts assumed.'},
            'historical_differences': ['Explicit reasoning_effort=none and output cap; historical client left these implicit.',
                                       'Explicit interpretation addendum; original prompt is retained as its prefix.',
                                       'No text repair, no automatic retries, complete response retention.',
                                       'Model alias retained; identical historical served weights are not established.'],
            'sources': {str(path.relative_to(ROOT)): sha(path.read_bytes()) for path in
                        (inputs/'pilot_selection.json', inputs/'semantic_review_v1.json',
                         inputs/'semantic_test_vectors_v1.json', source_path, Path(__file__))}}
    data = encoded(plan)
    if destination is None:
        return plan
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if destination.read_bytes() != data:
            raise ValueError('Prepared plan differs; use a new version, never overwrite')
    else:
        exclusive(destination, data)
    return plan


def assess(body):
    """Technical acceptance only. Fidelity and runtime validation remain pending."""
    try:
        response = json.loads(body)
        if response.get('model') not in RETURNED_MODELS:
            return 'unexpected_model'
        usage = response.get('usage') or {}
        if any(type(usage.get(k)) is not int or usage[k] < 0 for k in ('prompt_tokens', 'completion_tokens')):
            return 'missing_usage'
        if usage['prompt_tokens'] > 400000 or usage['completion_tokens'] > MAX_OUTPUT:
            return 'usage_outside_reserved_bound'
        choices = response.get('choices') or []
        if len(choices) != 1 or choices[0].get('finish_reason') != 'stop':
            return 'incomplete_or_nonstandard_finish'
        message = choices[0].get('message') or {}
        if message.get('refusal') or message.get('tool_calls'):
            return 'refusal_or_tool_call'
        content = message.get('content')
        if not isinstance(content, str) or not content.strip():
            return 'empty_content'
        if content.lstrip().startswith('UNCONVERTIBLE:'):
            return 'model_reports_unconvertible'
        tree = ast.parse(content)
        if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
            return 'invalid_code_shape'
        fn = tree.body[0]
        if (fn.name != 'strategy' or [a.arg for a in fn.args.args] != ['self', 'opponent']
                or fn.decorator_list or fn.args.defaults or fn.args.kwonlyargs or fn.args.posonlyargs
                or fn.args.vararg or fn.args.kwarg):
            return 'invalid_signature'
        return 'candidate_pending_fidelity_and_runtime'
    except (ValueError, TypeError, AttributeError, KeyError, SyntaxError):
        return 'invalid_response_or_syntax'


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, 'Redirect refused', headers, fp)


def transport(payload, key):
    req = urllib.request.Request(ENDPOINT, data=encoded(payload), method='POST',
                                 headers={'Authorization': 'Bearer '+key, 'Content-Type': 'application/json'})
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(req, timeout=60) as response:
            return response.status, response.read(), response.headers.get('x-request-id')
    except urllib.error.HTTPError as error:
        return error.code, error.read(), error.headers.get('x-request-id')


def run(plan_path, run_dir, send=transport, api_key=None):
    plan_bytes = plan_path.read_bytes()
    plan = json.loads(plan_bytes)
    if plan_bytes != encoded(prepare(None)):
        raise ValueError('Plan differs from verified pilot inputs and configuration')
    # Do not accept modified payloads or budgets just because the file is JSON.
    for relative, expected in plan['sources'].items():
        if sha((ROOT/relative).read_bytes()) != expected:
            raise ValueError('Prepared source changed: '+relative)
    if (plan['endpoint'] != ENDPOINT or plan['model'] != MODEL or len(plan['requests']) != 12
            or plan['budget_micro_usd'] != BUDGET_MICRO_USD
            or plan['reserve_per_attempt_micro_usd'] != RESERVE_MICRO_USD):
        raise ValueError('Unexpected plan configuration')
    for item in plan['requests']:
        if sha(encoded(item['payload'])) != item['payload_sha256']:
            raise ValueError('Request hash mismatch')
    run_dir.mkdir(parents=True, exist_ok=True)
    lock = run_dir/'running.lock'
    exclusive(lock, encoded({'started_at': now(), 'pid': os.getpid()}))
    try:
        anchor = run_dir/'plan.json'
        if anchor.exists():
            if anchor.read_bytes() != plan_bytes:
                raise ValueError('Run already bound to a different plan')
        else:
            exclusive(anchor, plan_bytes)
        spent = 0
        for number, item in enumerate(plan['requests'], 1):
            attempt = run_dir/f'{number:02d}'
            if attempt.exists():
                spent += RESERVE_MICRO_USD
                # A crash or an uncertain network response is NOT permission to retry.
                result = attempt/'result.json'
                if not result.exists():
                    raise RuntimeError('Unresolved attempt; reconcile before further calls: '+str(attempt))
                previous = json.loads(result.read_bytes())
                archived_body = (attempt/'response.bin').read_bytes()
                if sha(archived_body) != previous['response_sha256']:
                    raise ValueError('Archived response changed')
                if previous['status'] != 'candidate_pending_fidelity_and_runtime':
                    raise RuntimeError('Previous non-success requires documented review')
                archived_request = json.loads((attempt/'request.json').read_bytes())
                if (archived_request['strategy_id'] != item['strategy_id'] or
                        encoded(archived_request['payload']) != encoded(item['payload']) or
                        assess(archived_body) != previous['status'] or
                        (attempt/'candidate.py.txt').read_bytes() !=
                        json.loads(archived_body)['choices'][0]['message']['content'].encode()):
                    raise ValueError('Archived attempt is inconsistent')
                continue
            if spent + RESERVE_MICRO_USD > BUDGET_MICRO_USD:
                raise RuntimeError('Budget reservation exhausted')
            key = api_key or os.environ.get('OPENAI_API_KEY')
            if not key:
                raise RuntimeError('OPENAI_API_KEY is not set; no request sent')
            attempt.mkdir()
            exclusive(attempt/'request.json', encoded({'attempt_id': str(uuid.uuid4()),
                      'started_at': now(), 'strategy_id': item['strategy_id'], 'payload': item['payload'],
                      'payload_sha256': item['payload_sha256'], 'reserved_micro_usd': RESERVE_MICRO_USD,
                      'python': platform.python_version(), 'transport': 'stdlib urllib HTTPS; zero retries'}))
            spent += RESERVE_MICRO_USD
            try:
                http_status, body, request_id = send(item['payload'], key)
            except Exception as error:
                # Avoid serializing exception strings which may contain credentials.
                exclusive(attempt/'transport_error.json', encoded({'type': type(error).__name__,
                          'finished_at': now(), 'billing_status': 'unknown_reserved_in_full'}))
                raise RuntimeError('Transport failed; no automatic retry') from None
            # Protect against credential echo by an error response; record redaction.
            secret_bytes = key.encode()
            redacted = bool(secret_bytes and secret_bytes in body)
            if redacted:
                body = body.replace(secret_bytes, b'[REDACTED_API_KEY]')
            exclusive(attempt/'response.bin', body)
            status = assess(body) if http_status == 200 and not redacted else 'http_error_or_redacted_response'
            result = {'status': status, 'http_status': http_status, 'request_id': request_id,
                      'finished_at': now(), 'response_sha256': sha(body), 'credential_echo_redacted': redacted}
            if status == 'candidate_pending_fidelity_and_runtime':
                exclusive(attempt/'candidate.py.txt', json.loads(body)['choices'][0]['message']['content'].encode())
            exclusive(attempt/'result.json', encoded(result))
            if status != 'candidate_pending_fidelity_and_runtime':
                raise RuntimeError('Pilot stopped: '+status)
        return {'candidates': 12, 'reserved_micro_usd': spent, 'fidelity': 'not_checked'}
    finally:
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--plan', type=Path, default=ROOT/'phase3/inputs/pilot_requests_v1.json')
    parser.add_argument('--run-dir', type=Path, default=ROOT/'phase3/conversion_runs/pilot_v1')
    args = parser.parse_args()
    if args.prepare and not args.live:
        plan = prepare(args.plan)
        print(json.dumps({'requests_prepared': len(plan['requests']), 'max_reserved_usd': 12*RESERVE_MICRO_USD/1e6,
                          'budget_usd': BUDGET_MICRO_USD/1e6, 'api_calls': 0}))
    elif args.live and not args.prepare:
        print(json.dumps(run(args.plan, args.run_dir)))
    else:
        parser.error('Choose exactly one: --prepare (offline) or --live (API)')


if __name__ == '__main__':
    main()
