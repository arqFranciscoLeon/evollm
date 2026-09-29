import argparse
import logging
import axelrod as axl
from enum import StrEnum
from functools import partial, wraps

logger = logging.getLogger(__name__)

# Monkey-patch axelrod History to support .count() used by LLM-generated strategies
from axelrod.player import History as _History
if not hasattr(_History, 'count'):
    def _history_count(self, action):
        """Count occurrences of an action in this history."""
        return self.cooperations if action == axl.Action.C else self.defections
    _History.count = _history_count


def positive_int(x):
  try:
    x = int(x)
  except ValueError:
    raise argparse.ArgumentTypeError(f"{x} not an integer")

  if x < 1:
    raise argparse.ArgumentTypeError(f"{x} not in range [1, inf]")
  return x

def restricted_float(x, lower: float, upper: float):
  try:
    x = float(x)
  except ValueError:
    raise argparse.ArgumentTypeError(f"{x} not a floating-point literal")

  if x < lower or x > upper:
    raise argparse.ArgumentTypeError(f"{x} not in range [{lower}, {upper}]")
  return x

temp_arg = partial(restricted_float, lower=0, upper=1)
noise_arg = partial(restricted_float, lower=0, upper=0.5)


class Attitude(StrEnum):
  AGGRESSIVE = "Aggressive"
  COOPERATIVE = "Cooperative"
  NEUTRAL = "Neutral"

  def __repr__(self):
    return self.value


class Chicken(axl.Game):
  name = "chicken"

  def __init__(self):
    super().__init__(r=3, s=1, t=4, p=0)


class PrisonersDilemma(axl.Game):
  name = "prisoner"

  def __init__(self):
    super().__init__(r=3, s=0, t=4, p=1)


class StagHunt(axl.Game):
  name = "stag"

  def __init__(self):
    super().__init__(r=4, s=0, t=3, p=1)


class Classic(axl.Game):
  name = "classic"

  def __init__(self):
    super().__init__(r=3, s=0, t=5, p=1)


def auto_update_score(strategy_method):
  @wraps(strategy_method)
  def wrapper(self, opponent):
    self.update_score(opponent)
    result = strategy_method(self, opponent)
    if result is None:
      # Fallback for LLM-generated strategies that have missing return paths
      attitude = getattr(self, 'attitude', None)
      result = axl.Action.D if attitude == Attitude.AGGRESSIVE else axl.Action.C
    return result
  return wrapper


def get_game(name: str) -> axl.Game:
  if name == "chicken":
    return Chicken()
  elif name == "stag":
    return StagHunt()
  elif name == "prisoner":
    return PrisonersDilemma()
  elif name == "classic":
    return Classic()
  else:
    assert False, "Game name not recognised"


class LLM_Strategy(axl.player.Player):
  def __init__(self) -> None:
    super().__init__()
    self._score: int = 0
    self._rounds_scored: int = 0

  def __repr__(self) -> str:
    return self.__class__.__name__

  classifier = {
      "memory_depth": float("inf"),
      "stochastic": True,
      "long_run_time": False,
      "inspects_source": False,
      "manipulates_source": False,
      "manipulates_state": False,
  }

  @property
  def score(self) -> int:
    return self._score

  def first_round(self) -> bool:
    return not self.history

  def total_scores(self, player_history, opponent_history) -> tuple[int, int]:
    game = self.match_attributes["game"]
    return axl.interaction_utils.compute_final_score(zip(player_history, opponent_history), game)

  def update_score(self, opponent: axl.player.Player):
    game = self.match_attributes["game"]

    if len(self.history):
      self._rounds_scored += 1
      assert len(self.history) == self._rounds_scored, "Only update the score once per game"
      assert len(self.history) == len(opponent.history), f"Players have different history lengths: {len(self.history)}, {len(opponent.history)}"
      last_round = (self.history[-1], opponent.history[-1])

      # Validate that both actions are proper axl.Action values before scoring.
      # An LLM-generated strategy with a missing return path produces None,
      # which makes game.score() return a numpy array instead of a 2-tuple,
      # causing IndexError downstream.
      valid_actions = (axl.Action.C, axl.Action.D)
      if last_round[0] not in valid_actions or last_round[1] not in valid_actions:
        logger.warning(
            "update_score: invalid action in last_round %r for player %s — "
            "skipping score update for this round.",
            last_round, self.__class__.__name__,
        )
        return

      try:
        scores = game.score(last_round)
        if len(scores) < 2:
          raise ValueError(f"game.score returned unexpected result: {scores!r}")
        self._score += scores[0]
        # Hack for running against non-LLM_Strategies
        if not isinstance(opponent, LLM_Strategy):
          opponent.score += scores[1]
      except (IndexError, TypeError, ValueError) as exc:
        logger.warning(
            "update_score: could not score last_round %r for player %s: %s — "
            "skipping score update for this round.",
            last_round, self.__class__.__name__, exc,
        )
    else:
      if not isinstance(opponent, LLM_Strategy):
        opponent.score = 0
