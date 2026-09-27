"""Strict Phase 3 runtime: invalid actions are errors, never invented moves."""
from functools import wraps
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import axelrod as axl

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_manifest(path=None):
    path = Path(path) if path else ROOT / "phase3/inputs/manifest.json"
    return json.loads(path.read_text(encoding="utf-8"))


def configure_strict(manifest):
    for item in manifest["support"]:
        if digest(ROOT / item["path"]) != item["sha256"]:
            raise ValueError(f"Support hash mismatch: {item['path']}")
    support = ROOT / "phase3/inputs/support"
    if str(support) not in sys.path:
        sys.path.insert(0, str(support))
    from evollm import common
    if Path(common.__file__).resolve() != (support / "evollm/common.py").resolve():
        raise RuntimeError("Another evollm runtime is already imported; use a fresh process.")

    def update_score(self, opponent):
        length = len(self.history)
        if not length:
            if not isinstance(opponent, common.LLM_Strategy):
                opponent.score = 0
            return
        if length != len(opponent.history) or self._rounds_scored != length - 1:
            raise ValueError("Mismatched history or repeated score update")
        pair = (self.history[-1], opponent.history[-1])
        if any(action not in (axl.Action.C, axl.Action.D) for action in pair):
            raise ValueError("Invalid action in score history")
        mine, theirs = self.match_attributes["game"].score(pair)
        self._score += mine
        self._rounds_scored += 1
        if not isinstance(opponent, common.LLM_Strategy):
            opponent.score += theirs

    def decorate(method):
        @wraps(method)
        def strategy(self, opponent):
            self.update_score(opponent)
            try:
                action = method(self, opponent)
            except Exception as exc:
                raise ValueError(f"{type(self).__name__} round {len(self.history)+1}: {type(exc).__name__}: {exc}") from exc
            if action not in (axl.Action.C, axl.Action.D):
                raise ValueError(f"{type(self).__name__} round {len(self.history)+1}: invalid action {action!r}")
            return action
        return strategy

    common.LLM_Strategy.update_score = update_score
    common.auto_update_score = decorate
    return common


def load_library(item):
    path = ROOT / item["snapshot_path"]
    if digest(path) != item["sha256"]:
        raise ValueError(f"Library hash mismatch: {path}")
    name = "phase3lib_" + item["sha256"]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    classes = {}
    for record in item["strategies"]:
        cls = getattr(module, record["class"])
        if str(cls.attitude) != record["class"].split('_')[0] or cls.rounds != 1000 or cls.noise != 0:
            raise ValueError(f"Unexpected strategy metadata: {record['id']}")
        classes[record["id"]] = cls
    return classes


def seed_for(seed, *parts):
    return int.from_bytes(hashlib.sha256(json.dumps([seed, *parts], separators=(',', ':')).encode()).digest()[:4], "big") % (2**31-1)


def play_pair(first, second, turns, seed):
    # Classes or zero-argument factories, always fresh instances for each match.
    match = axl.Match((first(), second()), turns=turns, game=axl.Game(r=3,s=0,t=5,p=1), noise=0, seed=seed)
    history = match.play()
    counts = {"CC": 0, "CD": 0, "DC": 0, "DD": 0}
    for a, b in history:
        if a not in (axl.Action.C, axl.Action.D) or b not in (axl.Action.C, axl.Action.D):
            raise ValueError("Invalid action escaped runtime guard")
        counts[str(a) + str(b)] += 1
    if sum(counts.values()) != turns:
        raise ValueError("Unexpected match length")
    return {**counts, "payoff_i": (3*counts['CC'] + 5*counts['DC'] + counts['DD']) / turns,
            "payoff_j": (3*counts['CC'] + 5*counts['CD'] + counts['DD']) / turns}
