"""Explicit local corrections of confirmed raw uniform responses, no API."""
import difflib
import json
from phase3.pilot_converter import ROOT, sha, encoded, exclusive, now


def replace_once(source, old, new):
    if source.count(old) != 1:
        raise ValueError('Expected exact single correction site')
    return source.replace(old, new, 1)


def corrected(number, source):
    if number == 179:
        return replace_once(source,
            '    if last_self == last_opp:\n        return last_self\n    return axl.Action.D if last_self == axl.Action.C else axl.Action.C',
            '    if last_self == last_opp:\n        return axl.Action.C\n    return axl.Action.D')
    if number == 240:
        return replace_once(source, 'len(self.history) >= 995', 'len(self.history) >= 994')
    if number == 284:
        return replace_once(source,
            '    # If we are in the one-round bait state, cooperate exactly once, then reset.\n    if self._bait_round is not None:\n        self._bait_round = None\n        return axl.Action.C',
            '    # The round following the one-round C bait must be D.\n    if self._bait_round is not None:\n        self._bait_round = None\n        return axl.Action.D')
    if number == 320:
        return replace_once(source,
            'last_score = self.score - self.total_scores(self.history[-1:], opponent.history[-1:])[0]',
            'last_score = self.total_scores(self.history[-1:], opponent.history[-1:])[0]')
    if number == 347:
        source = replace_once(source,
            'if my_last == axl.Action.D and opp_last == axl.Action.D:\n        return axl.Action.D',
            'if my_last == axl.Action.D and opp_last == axl.Action.D:\n        return axl.Action.C')
        return replace_once(source,
            'if my_last == axl.Action.D and opp_last == axl.Action.C:\n        return axl.Action.C',
            'if my_last == axl.Action.D and opp_last == axl.Action.C:\n        return axl.Action.D')
    if number == 372:
        return replace_once(source, 'self.score - opponent.score == 1',
                            'self.total_scores(self.history[-1:], opponent.history[-1:])[0] == 1')
    if number == 408:
        return '''def strategy(self, opponent: axl.player.Player) -> axl.Action:
    if self.first_round():
        self.cooperation_started = False
        self.permanent_defection = False
        return axl.Action.D

    if self.permanent_defection:
        return axl.Action.D

    if self.cooperation_started:
        if opponent.history[-1] == axl.Action.D:
            self.permanent_defection = True
            return axl.Action.D
        return axl.Action.C

    if len(self.history) >= 5 and self.history[-5:].count(axl.Action.D) == 5 and opponent.history[-5:].count(axl.Action.C) == 5:
        self.cooperation_started = True
        return axl.Action.C
    return axl.Action.D
'''
    if number == 442:
        return replace_once(source,
            'last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0] if len(self.history) > 0 else 0',
            'last_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])[0]')
    if number == 482:
        return replace_once(source,
            'last_score = self.score - (self.total_scores(self.history[-1:], opponent.history[-1:])[0] if len(self.history) >= 1 else 0)',
            'last_score = self.total_scores(self.history[-1:], opponent.history[-1:])[0]')
    if number == 485:
        return replace_once(source, 'len(opponent.history) >= 999', 'len(opponent.history) >= 997')
    raise ValueError('No explicitly reviewed correction for this response')


def main():
    report_path = ROOT / 'phase3/validation/uniform_v3b.json'
    report = json.loads(report_path.read_bytes())
    plan = json.loads((ROOT / 'phase3/inputs/uniform_requests_v3.json').read_bytes())
    numbers = {item['id']: i for i, item in enumerate(plan['requests'], 1)}
    expected = {179, 240, 284, 320, 347, 372, 408, 442, 482, 485}
    failed = [r for r in report['results'] if r['status'] != 'passed_targeted_checks']
    if {numbers[r['id']] for r in failed} != expected:
        raise ValueError('Review final discrepancies before preparing corrections')
    folder = ROOT / 'phase3/uniform_corrections_v1'
    folder.mkdir(parents=True, exist_ok=True)
    records = []
    for row in failed:
        number = numbers[row['id']]
        original_path = ROOT / f'phase3/conversion_runs/uniform_v3/{number:03d}/candidate.py.txt'
        original = original_path.read_bytes()
        if sha(original) != row['candidate_sha256']:
            raise ValueError('Original candidate changed')
        before = original.decode()
        after = corrected(number, before)
        path = folder / f'{number:03d}.py.txt'
        exclusive(path, after.encode())
        records.append({'id': row['id'], 'number': number,
            'original_path': str(original_path.relative_to(ROOT)), 'original_sha256': sha(original),
            'derived_path': str(path.relative_to(ROOT)), 'derived_sha256': sha(after.encode()),
            'prose_sha256': plan['requests'][number - 1]['prose_sha256'],
            'diff': ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                               fromfile='original_response', tofile='local_correction'))})
    exclusive(ROOT / 'phase3/inputs/uniform_corrections_v1.json', encoded({
        'created_at': now(), 'raw_validation_sha256': sha(report_path.read_bytes()),
        'policy_sha256': sha((ROOT / 'phase3/CHINESE_RESOLUTION_POLICY_v1.md').read_bytes()),
        'scope': 'Local prose-faithful derivatives under the symmetric correction policy. Not new model responses. Original failure counts unchanged.',
        'derivations': records, 'api_calls': 0}))
    print(json.dumps({'local_corrections_prepared': len(records)}))


if __name__ == '__main__':
    main()
