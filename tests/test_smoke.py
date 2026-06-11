"""Smoke tests for the strategy libraries and the core loading machinery.

Run from the repo root with:

    PYTHONPATH=src pytest tests/test_smoke.py -q

Every strategy library must import, expose the expected number of strategy
classes, and every class must survive a short match without raising. These
tests exist because three real incidents (ast.Num removal in Python 3.12+,
a multiprocessing deadlock and silently truncated strategy files) were only
discovered mid-experiment.
"""
import glob
import os
import re
import sys

import axelrod as axl
import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

from evollm import algorithms, common  # noqa: E402

LIBRARIES = sorted(glob.glob(os.path.join(REPO_ROOT, "strategies", "*.py")))

# Libraries committed with fewer classes than the 75 the protocol specifies
# (Gemini 3.1 Pro prose/refine generation was committed incomplete; the same
# truncated files are in the public replication package). Marked strict-xfail
# so the suite stays green while the discrepancy remains visible; pending PI
# decision (regenerate vs erratum). Remove entries once the files hold 75.
KNOWN_INCOMPLETE = {
    "gemini_31_pro_prose_75.py": 21,
    "gemini_31_pro_prose_75_noise.py": 21,
    "gemini_31_pro_refine_75.py": 7,
    "gemini_31_pro_refine_75_noise.py": 7,
}

RANKS_NAMES = ("Aggressive_ranks", "Cooperative_ranks", "Neutral_ranks")

# Strategy classes with latent bugs in the committed (published) files: some
# code path falls through without a return, so the strategy yields None and
# axelrod's scoring raises IndexError. On this branch there is no per-move
# exception handling, so these paths would crash a run if triggered. Kept as
# documented known-fragile (the files are published scientific artifacts and
# must not be silently edited); pending PI decision.
KNOWN_FRAGILE = {
    "gemini_25_flash_prose_75.py":
        {"Aggressive_2", "Aggressive_15", "Cooperative_13", "Neutral_13"},
    "gemini_25_flash_prose_75_noise.py":
        {"Aggressive_2", "Aggressive_15", "Cooperative_13", "Neutral_13"},
    "gemini_25_flash_refine_75.py": {"Cooperative_17", "Neutral_14"},
    "gemini_25_flash_refine_75_noise.py": {"Cooperative_17", "Neutral_14"},
}


def _params():
  for path in LIBRARIES:
    name = os.path.basename(path)
    marks = []
    if name in KNOWN_INCOMPLETE:
      marks.append(pytest.mark.xfail(
          strict=True,
          reason=f"known-incomplete library: {KNOWN_INCOMPLETE[name]} classes "
                 "instead of 75 (pending PI decision)"))
    yield pytest.param(path, id=name, marks=marks)


@pytest.mark.parametrize("path", _params())
def test_library_has_75_strategies(path):
  algos = algorithms.load_algorithms(path)
  assert len(algos) == 75
  for attitude in ("Aggressive", "Cooperative", "Neutral"):
    count = sum(1 for a in algos if a.__name__.startswith(attitude))
    assert count == 25, f"{attitude}: expected 25, got {count}"


@pytest.mark.parametrize("path", [pytest.param(p, id=os.path.basename(p))
                                  for p in LIBRARIES])
def test_ranks_defined_once_and_consistent(path):
  """Guard against rank_strategies.py appending duplicate ranks lists."""
  with open(path, encoding="utf-8") as f:
    src = f.read()
  module = algorithms.load_module(path)
  class_names = {a.__name__ for a in algorithms.load_algorithms(path)}

  for ranks_name in RANKS_NAMES:
    n_defs = len(re.findall(rf"^{ranks_name}\s*=", src, re.M))
    if n_defs == 0:
      continue  # ranks are optional: only rank_strategies.py adds them
    assert n_defs == 1, f"{ranks_name} defined {n_defs} times (append bug?)"
    ranks = getattr(module, ranks_name)
    assert len(ranks) == len(set(ranks)), f"{ranks_name} has duplicates"
    unknown = set(ranks) - class_names
    assert not unknown, f"{ranks_name} names missing classes: {unknown}"


@pytest.mark.parametrize("path", [pytest.param(p, id=os.path.basename(p))
                                  for p in LIBRARIES])
def test_every_strategy_survives_short_match(path):
  """Every generated class must play a few turns without raising."""
  algos = algorithms.load_algorithms(path)
  game = common.get_game(algos[0].game)
  failures = {}
  for cls in algos:
    try:
      match = axl.Match((cls(), axl.TitForTat()), turns=5, game=game, seed=7)
      match.play()
      assert len(match.result) == 5
    except Exception as exc:  # noqa: BLE001 — we want the full inventory
      failures[cls.__name__] = repr(exc)
  allowed = KNOWN_FRAGILE.get(os.path.basename(path), set())
  unexpected = set(failures) - allowed
  assert not unexpected, (
      f"strategies raised outside the known-fragile list: "
      f"{ {k: failures[k] for k in unexpected} }")


def test_create_classes_samplers_play():
  """The attitude samplers built by create_classes run a short match."""
  algos = algorithms.load_algorithms(
      os.path.join(REPO_ROOT, "strategies", "openai_default.py"))
  aggressive, cooperative, neutral = algorithms.create_classes(algos)
  assert aggressive.strategies and cooperative.strategies and neutral.strategies
  game = common.get_game(algos[0].game)
  match = axl.Match((aggressive(), cooperative()), turns=5, game=game, seed=7)
  match.play()
  assert len(match.result) == 5


def test_load_algorithms_percentile_filter():
  """keep_top/keep_bottom select the expected slice of the ranked lists."""
  path = os.path.join(REPO_ROOT, "strategies", "openai_default.py")
  top_fifth = algorithms.load_algorithms(path, keep_top=0, keep_bottom=0.2)
  assert len(top_fifth) == 15  # 5 per attitude
  full = algorithms.load_algorithms(path)
  assert set(a.__name__ for a in top_fifth) <= set(a.__name__ for a in full)
