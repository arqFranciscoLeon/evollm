import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# Play Defect (D) in every round, regardless of your opponent’s past actions or
# the game history. Do not cooperate at any point.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    Thereafter, in each round:  1. If
# both you and your opponent appeared to cooperate in the previous round (i.e.,
# the observed actions were C and C), cooperate.   2. If you appeared to
# cooperate but your opponent appeared to defect (observed C vs. D), defect.
# 3. If you appeared to defect but your opponent appeared to cooperate (observed
# D vs. C), cooperate.   4. If both you and your opponent appeared to defect
# (observed D and D), cooperate with 10% probability; otherwise, defect.    This
# strategy forgives occasional mutual defections—likely caused by noise—by
# occasionally returning to cooperation, while still retaliating against clear
# defection and rewarding mutual cooperation.

class Cooperative_1(LLM_Strategy):
  n = 1
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return self._random.random_choice(0.1)
  
      return axl.Action.C



# Start by cooperating in the first round. After that, for each subsequent
# round:  1. If both you and your opponent appeared to cooperate in the previous
# round (i.e., the observed actions were both C), cooperate.   2. If you
# appeared to cooperate and your opponent appeared to defect in the previous
# round, defect.   3. If you appeared to defect and your opponent appeared to
# cooperate in the previous round, cooperate.   4. If both you and your opponent
# appeared to defect in the previous round, defect.  Continue applying these
# rules for all 1000 rounds, using only the most recent observed actions to
# decide your next move.

class Neutral_1(LLM_Strategy):
  n = 1
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      return opponent.history[-1] if len(opponent.history) > 0 else axl.Action.C



# Play Defect (D) in every round, regardless of your opponent’s past actions or
# observed outcomes. Do not condition your move on history, signals, or apparent
# cooperation—always choose D.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.  After that, in each
# subsequent round:  1. If both you and your opponent appeared to play C in the
# previous round (i.e., the observed outcome was mutual C), play C.   2. If you
# appeared to play C and your opponent appeared to play D in the previous round,
# play D.   3. If you appeared to play D and your opponent appeared to play C in
# the previous round, play C.   4. If both you and your opponent appeared to
# play D in the previous round, play D.  However, to account for noise (the 10%
# chance actions are flipped), add this exception:  - If you have played C for
# the last two rounds and your opponent appeared to play D both times, switch to
# playing D.   - If you are playing D but your opponent has appeared to play C
# for the last two rounds, switch back to playing C.  Otherwise, stick to the
# rules above based on the most recent observed outcome.

class Cooperative_2(LLM_Strategy):
  n = 2
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_switch_round = None
          return axl.Action.C
  
      # Default behavior based on the most recent observed outcome.
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          action = axl.Action.C
      elif last_self == axl.Action.C and last_opp == axl.Action.D:
          action = axl.Action.D
      elif last_self == axl.Action.D and last_opp == axl.Action.C:
          action = axl.Action.C
      else:
          action = axl.Action.D
  
      # Noise-aware exceptions based on the last two observed rounds.
      if len(self.history) >= 2:
          last_two_self = self.history[-2:]
          last_two_opp = opponent.history[-2:]
  
          if last_two_self == [axl.Action.C, axl.Action.C] and last_two_opp == [axl.Action.D, axl.Action.D]:
              action = axl.Action.D
          elif last_two_self == [axl.Action.D, axl.Action.D] and last_two_opp == [axl.Action.C, axl.Action.C]:
              action = axl.Action.C
  
      return action



# Play as follows:  1. Start by cooperating in the first round.   2. In each
# subsequent round, look at your opponent’s last observed action (the action you
# saw, not what they intended).   3. If your opponent was observed to cooperate
# in the previous round, cooperate.   4. If your opponent was observed to defect
# in the previous round, defect.   5. However, if you have defected for three
# consecutive rounds, cooperate in the next round regardless of what your
# opponent did.

class Neutral_2(LLM_Strategy):
  n = 2
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_streak = 0
          return axl.Action.C
  
      if getattr(self, "_defect_streak", None) is None:
          self._defect_streak = 0
  
      if self._defect_streak >= 3:
          action = axl.Action.C
      else:
          last_opponent_action = opponent.history[-1]
          action = axl.Action.C if last_opponent_action == axl.Action.C else axl.Action.D
  
      if action == axl.Action.D:
          self._defect_streak += 1
      else:
          self._defect_streak = 0
  
      return action



# Play D in every round, regardless of history or opponent behavior.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round. Then, for each subsequent round:  1.
# If both players received a payoff of 3 in the previous round, cooperate.   2.
# If you received 0 and your opponent received 5 in the previous round,
# cooperate.   3. If you received 5 and your opponent received 0 in the previous
# round, defect.   4. If both players received a payoff of 1 in the previous
# round, defect.    After any round where you defect due to rule 3 or 4, return
# to cooperation in the following round unless the same triggering condition
# repeats.

class Cooperative_3(LLM_Strategy):
  n = 3
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_defect_trigger = None
          return axl.Action.C
  
      if len(self.history) == 0 or len(opponent.history) == 0:
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      last_payoffs = {
          (axl.Action.C, axl.Action.C): (3, 3),
          (axl.Action.C, axl.Action.D): (0, 5),
          (axl.Action.D, axl.Action.C): (5, 0),
          (axl.Action.D, axl.Action.D): (1, 1),
      }
  
      my_payoff, opp_payoff = last_payoffs[(my_last, opp_last)]
  
      if my_payoff == 3 and opp_payoff == 3:
          return axl.Action.C
  
      if my_payoff == 0 and opp_payoff == 5:
          return axl.Action.C
  
      if my_payoff == 5 and opp_payoff == 0:
          if self._last_defect_trigger == (5, 0):
              self._last_defect_trigger = None
              return axl.Action.D
          self._last_defect_trigger = (5, 0)
          return axl.Action.C
  
      if my_payoff == 1 and opp_payoff == 1:
          if self._last_defect_trigger == (1, 1):
              self._last_defect_trigger = None
              return axl.Action.D
          self._last_defect_trigger = (1, 1)
          return axl.Action.C
  
      self._last_defect_trigger = None
      return axl.Action.C



# Start by cooperating in the first round. After that, for each subsequent
# round:  1. If both you and your opponent appeared to cooperate in the previous
# round (i.e., the observed outcome was (C, C)), cooperate.   2. If you appeared
# to cooperate and your opponent appeared to defect (observed outcome (C, D)),
# defect.   3. If you appeared to defect and your opponent appeared to cooperate
# (observed outcome (D, C)), cooperate.   4. If both you and your opponent
# appeared to defect in the previous round (observed outcome (D, D)), cooperate.
# This strategy forgives mutual defection immediately, retaliates against
# apparent exploitation, and restores cooperation whenever possible, accounting
# for the 10% noise by avoiding long punitive streaks.

class Neutral_3(LLM_Strategy):
  n = 3
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C



# Play Defect (D) in every round, regardless of your opponent’s previous actions
# or the game history. Do not cooperate at any point.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    In every subsequent round:    1.
# If the opponent’s observed action in the previous round was cooperation,
# cooperate.   2. If the opponent’s observed action in the previous round was
# defection, defect.    However, to account for noise:    3. If you have
# defected for three consecutive rounds and the opponent’s most recent observed
# action was cooperation, return to cooperation.   4. If you have cooperated for
# three consecutive rounds and the opponent’s most recent observed action was
# defection, continue cooperating only if the opponent had cooperated in at
# least one of the two rounds before that; otherwise, defect.    This strategy
# prioritizes cooperation, forgives occasional defections likely caused by
# noise, and avoids long mutual defection spirals.

class Cooperative_4(LLM_Strategy):
  n = 4
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._consecutive_c = 0
          self._consecutive_d = 0
          return axl.Action.C
  
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.C:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              self._consecutive_d = 0
              self._consecutive_c = 1
              return axl.Action.C
          self._consecutive_c = self._consecutive_c + 1 if self.history[-1] == axl.Action.C else 0
          self._consecutive_d = self._consecutive_d + 1 if self.history[-1] == axl.Action.D else 0
          return axl.Action.C
  
      if self.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]:
          recent_opp = opponent.history[-3:-1]
          if axl.Action.C in recent_opp:
              self._consecutive_c = self._consecutive_c + 1 if self.history[-1] == axl.Action.C else 0
              self._consecutive_d = self._consecutive_d + 1 if self.history[-1] == axl.Action.D else 0
              return axl.Action.C
          self._consecutive_c = 0
          self._consecutive_d = self._consecutive_d + 1 if self.history[-1] == axl.Action.D else 0
          return axl.Action.D
  
      self._consecutive_c = self._consecutive_c + 1 if self.history[-1] == axl.Action.C else 0
      self._consecutive_d = self._consecutive_d + 1 if self.history[-1] == axl.Action.D else 0
      return axl.Action.D



# Start by cooperating in the first round. After that, follow these rules in
# order:  1. If the opponent’s last observed action was cooperation, cooperate.
# 2. If the opponent’s last observed action was defection, defect.    Continue
# applying these rules for all remaining rounds, using only the most recent
# observed action to decide your next move.

class Neutral_4(LLM_Strategy):
  n = 4
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      last_opponent_action = opponent.history[-1]
      if last_opponent_action == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Play D in every round, regardless of history or opponent behavior.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    After that, in each subsequent
# round:    1. If both you and your opponent appeared to cooperate in the
# previous round (i.e., the observed actions were both C), cooperate.    2. If
# you appeared to cooperate but your opponent appeared to defect (observed
# actions: you C, opponent D), defect once as a response, then return to
# cooperation in the following round regardless of the outcome—this accounts for
# possible noise and avoids prolonged retaliation.    3. If you appeared to
# defect and your opponent appeared to cooperate (observed actions: you D,
# opponent C), cooperate in the next round—assume your own action may have been
# flipped by noise.    4. If both you and your opponent appeared to defect in
# the previous round (observed actions both D), cooperate in the next
# round—treat mutual defection as likely caused by noise and attempt to restore
# cooperation.    Continue this pattern for all 1000 rounds.

class Cooperative_5(LLM_Strategy):
  n = 5
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._force_cooperate_next = False
          self._force_defect_next = False
          return axl.Action.C
  
      if getattr(self, "_force_cooperate_next", False):
          self._force_cooperate_next = False
          return axl.Action.C
  
      if getattr(self, "_force_defect_next", False):
          self._force_defect_next = False
          self._force_cooperate_next = True
          return axl.Action.D
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
  
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          self._force_cooperate_next = True
          return axl.Action.D
  
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.C
  
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C



# Start by playing C in the first round.    In every subsequent round:    1. If
# your opponent’s observed action in the previous round was C, play C.   2. If
# your opponent’s observed action in the previous round was D, play D.    This
# strategy—called “Tit-for-Tat with direct response to observed
# actions”—maintains cooperation when the opponent appears cooperative and
# responds to observed defection with defection, while remaining forgiving and
# neutral overall.

class Neutral_5(LLM_Strategy):
  n = 5
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      return opponent.history[-1] if opponent.history else axl.Action.C



# Play Defect (D) in every round, regardless of the opponent’s past actions or
# observed outcomes. Do not condition your move on history, noise, or
# payoffs—always choose D.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    After that, base your action on
# what your opponent appeared to play in the previous round (accounting for
# possible noise):    1. If your opponent appeared to cooperate in the previous
# round, cooperate.   2. If your opponent appeared to defect in the previous
# round, defect.    However, to guard against noise causing endless retaliation:
# 3. After you have defected for five consecutive rounds, cooperate once,
# regardless of your opponent’s last action.    Then return to following rules 1
# and 2.

class Cooperative_6(LLM_Strategy):
  n = 6
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.consecutive_defections = 0
          return axl.Action.C
  
      if getattr(self, "consecutive_defections", None) is None:
          self.consecutive_defections = 0
  
      if self.consecutive_defections >= 5:
          self.consecutive_defections = 0
          return axl.Action.C
  
      last_opponent_action = opponent.history[-1]
  
      if last_opponent_action == axl.Action.C:
          self.consecutive_defections = 0
          return axl.Action.C
      else:
          self.consecutive_defections += 1
          return axl.Action.D



# Play as follows:  1. Start by cooperating in the first round.   2. In each
# subsequent round, look at your opponent’s last observed action (accounting for
# possible noise).   3. If your opponent’s last observed action was cooperation,
# cooperate.   4. If your opponent’s last observed action was defection, defect.
# This strategy—“Tit-for-Tat with observed actions”—maintains neutrality by
# mirroring the opponent’s most recent behavior, tolerates occasional noise by
# responding only to the latest move, and encourages mutual cooperation while
# deterring sustained exploitation.

class Neutral_6(LLM_Strategy):
  n = 6
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]



# Play D in every round, regardless of your opponent’s previous actions or the
# game’s history. Do not cooperate at any point.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    Thereafter, base your action on
# what your opponent appeared to play in the previous round (accounting for
# noise):    1. If your opponent appeared to cooperate in the previous round,
# cooperate.   2. If your opponent appeared to defect in the previous round,
# defect.    Continue this pattern for all 1000 rounds.

class Cooperative_7(LLM_Strategy):
  n = 7
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      return opponent.history[-1]



# Play Cooperate (C) in the first round. In every subsequent round:  1. If both
# you and your opponent appeared to play C in the previous round, play C.   2.
# If both you and your opponent appeared to play D in the previous round, play
# C.   3. If you appeared to play C and your opponent appeared to play D in the
# previous round, play D.   4. If you appeared to play D and your opponent
# appeared to play C in the previous round, play C.    Continue this rule for
# all 1000 rounds.

class Neutral_7(LLM_Strategy):
  n = 7
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C



# Play D in every round, regardless of history or opponent behavior.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    Thereafter, base your action on
# what your opponent appeared to play in the previous round (accounting for
# possible noise):    1. If your opponent appeared to cooperate in the previous
# round, cooperate.   2. If your opponent appeared to defect in the previous
# round, defect.    However, to guard against noise causing endless retaliation:
# 3. After you have defected for five consecutive rounds, cooperate once,
# regardless of your opponent’s last action.    Then return to following rules 1
# and 2.

class Cooperative_8(LLM_Strategy):
  n = 8
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._consecutive_defections = 0
          return axl.Action.C
  
      if not hasattr(self, "_consecutive_defections"):
          self._consecutive_defections = 0
  
      if self._consecutive_defections >= 5:
          self._consecutive_defections = 0
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          self._consecutive_defections = 0
          return axl.Action.C
      else:
          self._consecutive_defections += 1
          return axl.Action.D



# Play Cooperate (C) in the first round. In each subsequent round:  1. If both
# you and your opponent appeared to play C in the previous round, play C.   2.
# If both you and your opponent appeared to play D in the previous round, play
# C.   3. If you appeared to play C and your opponent appeared to play D in the
# previous round, play D.   4. If you appeared to play D and your opponent
# appeared to play C in the previous round, play C.    (“Appeared to play” means
# the action actually observed after noise is applied.)

class Neutral_8(LLM_Strategy):
  n = 8
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          return axl.Action.D
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C



# Play D (defect) in every round, regardless of your opponent’s past actions or
# the game history. Do not cooperate at any point.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After each round,
# observe your opponent’s apparent action (which may be flipped due to noise).
# 1. If your opponent appeared to play C in the previous round, play C in the
# current round.   2. If your opponent appeared to play D in the previous round,
# play D in the current round.    However, to account for noise and avoid long
# mutual defection after a single mistake:    3. Every 10 rounds (i.e., in
# rounds 10, 20, 30, …), regardless of the opponent’s last action, play C.
# This gives a chance to reset cooperation if noise caused a breakdown.
# Otherwise, follow rules 1 and 2 strictly.

class Cooperative_9(LLM_Strategy):
  n = 9
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._round_counter = 1
          return axl.Action.C
  
      self._round_counter += 1
  
      if self._round_counter % 10 == 0:
          return axl.Action.C
  
      return opponent.history[-1] if opponent.history else axl.Action.C



# Start by cooperating in the first round.    In every subsequent round:    1.
# If your opponent’s observed action in the previous round was cooperation,
# cooperate.   2. If your opponent’s observed action in the previous round was
# defection, defect.    Continue this rule for all 1000 rounds.

class Neutral_9(LLM_Strategy):
  n = 9
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      return opponent.history[-1] if opponent.history else axl.Action.C



# Play Defect (D) in every round, regardless of your opponent’s past actions or
# the game history. Do not cooperate at any point.

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After each round,
# observe your opponent’s apparent action (which may be flipped due to noise).
# Continue playing C as long as your opponent has played C in at least 80% of
# the last 10 rounds.    If your opponent has played C in fewer than 80% of the
# last 10 rounds, switch to playing Defect (D) for the next 5 rounds.    After
# those 5 rounds of D, return to playing C and resume monitoring the opponent’s
# cooperation rate over the most recent 10 rounds as before.    If fewer than 10
# rounds have been played, use all available rounds to compute the cooperation
# rate.

class Cooperative_10(LLM_Strategy):
  n = 10
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_counter = 0
          return axl.Action.C
  
      if getattr(self, "_defect_counter", None) is None:
          self._defect_counter = 0
  
      if self._defect_counter > 0:
          self._defect_counter -= 1
          return axl.Action.D
  
      recent_opponent_history = opponent.history[-10:]
      if len(recent_opponent_history) == 0:
          cooperation_rate = 1.0
      else:
          cooperation_rate = recent_opponent_history.cooperations / len(recent_opponent_history)
  
      if cooperation_rate < 0.8:
          self._defect_counter = 4
          return axl.Action.D
  
      return axl.Action.C



# Play Cooperate (C) in the first round. In every subsequent round:  1. If both
# you and your opponent appeared to play the same action in the previous round
# (both C or both D), play C.   2. If your actions appeared different in the
# previous round (one C and one D), play D.    This rule applies to the observed
# (possibly noisy) actions from the prior round, not the intended ones.

class Neutral_10(LLM_Strategy):
  n = 10
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# Play D (defect) in every round, regardless of your opponent’s previous actions
# or the game history. Do not cooperate at any point.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    Thereafter, in each round:  1. If
# both you and your opponent appeared to cooperate in the previous round (i.e.,
# the observed outcome was mutual cooperation), cooperate.   2. If your opponent
# appeared to defect while you appeared to cooperate in the previous round,
# defect.   3. If you appeared to defect while your opponent appeared to
# cooperate in the previous round, cooperate.   4. If both you and your opponent
# appeared to defect in the previous round, cooperate.    This strategy forgives
# isolated defections—whether real or caused by noise—and restores cooperation
# after mutual defection, while still responding to persistent defection.

class Cooperative_11(LLM_Strategy):
  n = 11
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          return axl.Action.D
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C



# Play Cooperate (C) in the first round. In each subsequent round:  1. If both
# you and your opponent appeared to play C in the previous round (after noise),
# play C.   2. If both you and your opponent appeared to play D in the previous
# round, play C.   3. If you appeared to play C and your opponent appeared to
# play D, play D.   4. If you appeared to play D and your opponent appeared to
# play C, play C.    Continue this rule for all 1000 rounds.

class Neutral_11(LLM_Strategy):
  n = 11
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          return axl.Action.D
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C



# Play Defect (D) in every round, regardless of your opponent’s past actions or
# the game history. Do not cooperate at any point.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    After that, base your action on
# what your opponent appeared to play in the previous round (accounting for
# possible noise):    1. If your opponent appeared to cooperate in the last
# round, cooperate.   2. If your opponent appeared to defect in the last round,
# defect.    However, to prevent prolonged mutual defection due to noise:    3.
# Every 10 rounds, regardless of the opponent’s last action, cooperate once to
# test for renewed cooperation.    Continue this pattern for all 1000 rounds.

class Cooperative_12(LLM_Strategy):
  n = 12
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._test_round_counter = 0
          return axl.Action.C
  
      self._test_round_counter += 1
  
      if self._test_round_counter % 10 == 0:
          return axl.Action.C
  
      last_opponent_action = opponent.history[-1]
  
      if last_opponent_action == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D



# Start by cooperating in the first round.    Thereafter, base your action on
# the opponent’s last observed move, but account for noise by using the
# following rule:    - If the opponent’s last observed move was cooperation,
# cooperate.   - If the opponent’s last observed move was defection, defect.
# However, to avoid getting trapped in mutual defection due to noise, add a
# simple forgiveness mechanism:    - If you have defected for five consecutive
# rounds and the opponent’s last observed move is still defection, cooperate
# once to test for possible noise-induced miscoordination.    After that test
# round, return to responding directly to the opponent’s last observed move as
# described above.    Continue this approach for all 1000 rounds.

class Neutral_12(LLM_Strategy):
  n = 12
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_streak = 0
          self._forgiveness_used = False
          return axl.Action.C
  
      last_opponent_move = opponent.history[-1]
  
      if last_opponent_move == axl.Action.C:
          self._defect_streak = 0
          return axl.Action.C
  
      # Opponent last observed move was D
      if self.history and self.history[-1] == axl.Action.D:
          self._defect_streak += 1
      else:
          self._defect_streak = 1
  
      if self._defect_streak >= 5 and not self._forgiveness_used:
          self._forgiveness_used = True
          self._defect_streak = 0
          return axl.Action.C
  
      return axl.Action.D



# Play D in every round, regardless of history or opponent behavior.

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    Thereafter, in each round:  1. If
# both you and your opponent appeared to cooperate in the previous round (i.e.,
# the observed outcome was (C, C)), cooperate.   2. If you appeared to cooperate
# and your opponent appeared to defect (observed outcome (C, D)), defect.   3.
# If you appeared to defect and your opponent appeared to cooperate (observed
# outcome (D, C)), defect.   4. If both you and your opponent appeared to defect
# (observed outcome (D, D)), cooperate.    This rule set implements a forgiving
# tit-for-tat strategy that treats mutual defection as a possible error and
# resets to cooperation, while still retaliating against clear unilateral
# defection.

class Cooperative_13(LLM_Strategy):
  n = 13
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C



# Play Cooperate (C) in the first round. In each subsequent round:  1. If both
# you and your opponent appeared to play C in the previous round, play C.   2.
# If both you and your opponent appeared to play D in the previous round, play
# C.   3. If you appeared to play C and your opponent appeared to play D in the
# previous round, play D.   4. If you appeared to play D and your opponent
# appeared to play C in the previous round, play C.    (“Appeared to play” means
# the action actually observed after noise is applied.)

class Neutral_13(LLM_Strategy):
  n = 13
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          return axl.Action.D
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C



# Play D (defect) in every round, regardless of your opponent’s past actions or
# outcomes. Do not condition your behavior on history, signals, or
# payoffs—always choose D.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in each
# round, do the following:    1. If both you and your opponent appeared to play
# C in the previous round (i.e., the observed outcome was C–C), play C.   2. If
# you appeared to play C and your opponent appeared to play D in the previous
# round (observed C–D), play D.   3. If you appeared to play D and your opponent
# appeared to play C in the previous round (observed D–C), play C.   4. If both
# you and your opponent appeared to play D in the previous round (observed D–D),
# play C.    This strategy forgives occasional defections—whether caused by
# noise or intent—by returning to cooperation after any D–D outcome and after
# punishing a single observed defection with one round of D.

class Cooperative_14(LLM_Strategy):
  n = 14
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C



# Start by cooperating in the first round.    Thereafter, in each round:  1. If
# both you and your opponent appeared to cooperate in the previous round (i.e.,
# the observed actions were C and C), cooperate.   2. If you appeared to
# cooperate and your opponent appeared to defect in the previous round (observed
# C and D), defect.   3. If you appeared to defect and your opponent appeared to
# cooperate in the previous round (observed D and C), cooperate.   4. If both
# you and your opponent appeared to defect in the previous round (observed D and
# D), cooperate.    This rule set treats apparent mutual defection as a signal
# to reset cooperation, forgives isolated defections when you were the defector,
# retaliates against apparent exploitation, and maintains cooperation after
# mutual cooperation—balancing responsiveness to the payoff structure with
# robustness to noise.

class Neutral_14(LLM_Strategy):
  n = 14
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C



# Play Defect (D) in every round, regardless of your opponent’s past actions or
# the game history. Do not cooperate at any point.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    After that, in each subsequent
# round:    1. If both you and your opponent appeared to cooperate in the
# previous round (i.e., the observed actions were C and C), cooperate.   2. If
# you appeared to cooperate and your opponent appeared to defect (observed C and
# D), defect.   3. If you appeared to defect and your opponent appeared to
# cooperate (observed D and C), cooperate.   4. If both you and your opponent
# appeared to defect (observed D and D), cooperate.    This approach rewards
# mutual cooperation, forgives occasional defections that may result from noise,
# and avoids long retaliatory cycles.

class Cooperative_15(LLM_Strategy):
  n = 15
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          return axl.Action.D
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C



# Play as follows:  1. Start by cooperating in the first round.   2. In each
# subsequent round, look at the opponent’s action from the previous round as
# observed (accounting for possible noise).   3. If the opponent was observed to
# cooperate in the previous round, cooperate.   4. If the opponent was observed
# to defect in the previous round, defect.    This strategy—called “Tit-for-Tat
# with noise tolerance”—maintains cooperation when the opponent appears
# cooperative and retaliates when the opponent appears defective, while
# remaining neutral by mirroring observed behavior without escalation or
# forgiveness.

class Neutral_15(LLM_Strategy):
  n = 15
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      return opponent.history[-1]



# Play D in every round, regardless of history or opponent behavior.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    Thereafter, in each round:  1. If
# the opponent’s observed action in the previous round was cooperation,
# cooperate.   2. If the opponent’s observed action in the previous round was
# defection, defect.    However, to account for noise:  3. If you have defected
# for three consecutive rounds and the opponent’s observed actions in those same
# rounds were all cooperation, return to cooperation in the next round.
# Otherwise, follow rules 1 and 2 strictly.

class Cooperative_16(LLM_Strategy):
  n = 16
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._consecutive_defections = 0
          return axl.Action.C
  
      if not hasattr(self, "_consecutive_defections"):
          self._consecutive_defections = 0
  
      if len(self.history) >= 3:
          last_three_self = self.history[-3:]
          last_three_opp = opponent.history[-3:]
          if (
              last_three_self.count(axl.Action.D) == 3
              and last_three_opp.count(axl.Action.C) == 3
          ):
              self._consecutive_defections = 0
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          self._consecutive_defections = 0
          return axl.Action.C
      else:
          self._consecutive_defections += 1
          return axl.Action.D



# Play Cooperate (C) in the first round. In each subsequent round:  1. If both
# you and your opponent appeared to play C in the previous round, play C.   2.
# If both you and your opponent appeared to play D in the previous round, play
# C.   3. If you appeared to play C and your opponent appeared to play D in the
# previous round, play D.   4. If you appeared to play D and your opponent
# appeared to play C in the previous round, play C.    (“Appeared to play” means
# the action actually observed after noise was applied.)

class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          return axl.Action.D
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C



# Play Defect (D) in every round, regardless of your opponent’s past actions or
# the game history. Do not cooperate at any point.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After each round, follow
# these rules in order:  1. If both you and your opponent appeared to play C in
# the last round (regardless of what you intended), play C in the next round.
# 2. If you appeared to play C and your opponent appeared to play D, play D in
# the next round.   3. If you appeared to play D and your opponent appeared to
# play C, play C in the next round.   4. If both you and your opponent appeared
# to play D, play C in the next round.    Always base your decision only on the
# observed (possibly flipped) actions from the previous round, not on your
# intended actions.

class Cooperative_17(LLM_Strategy):
  n = 17
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          return axl.Action.D
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C



# Start by cooperating in the first round.    Thereafter, in each round:   1. If
# your opponent’s observed action in the previous round was cooperation,
# cooperate.   2. If your opponent’s observed action in the previous round was
# defection, defect.    Continue this rule for all 1000 rounds.

class Neutral_17(LLM_Strategy):
  n = 17
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      return opponent.history[-1] if opponent.history else axl.Action.C



# Play D (defect) in every round, regardless of your opponent’s past actions or
# observed outcomes. Do not condition your behavior on history, noise, or
# payoffs—maintain constant defection throughout all 1000 rounds.

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    Thereafter, in each round:  1. If
# both you and your opponent appeared to cooperate in the previous round (i.e.,
# the observed actions were C and C), cooperate.   2. If you appeared to
# cooperate but your opponent appeared to defect (observed C vs. D), defect.
# 3. If you appeared to defect but your opponent appeared to cooperate (observed
# D vs. C), cooperate.   4. If both you and your opponent appeared to defect in
# the previous round (observed D and D), cooperate.  This strategy forgives
# mutual defections and isolated defections that may result from noise, while
# still responding to clear exploitation.

class Cooperative_18(LLM_Strategy):
  n = 18
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          return axl.Action.D
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C



# Start by cooperating in the first round.    In every subsequent round:    1.
# If both players received a payoff of 3 in the previous round, cooperate.   2.
# If you received 0 and your opponent received 5 in the previous round,
# cooperate.   3. If you received 5 and your opponent received 0 in the previous
# round, defect.   4. If both players received a payoff of 1 in the previous
# round, defect.    This strategy interprets observed payoffs as signals of
# intended actions, accounts for noise by forgiving isolated low payoffs that
# likely resulted from action flips, and sustains mutual cooperation when it is
# clearly beneficial.

class Neutral_18(LLM_Strategy):
  n = 18
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      my_payoff = None
      opp_payoff = None
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          my_payoff, opp_payoff = 3, 3
      elif my_last == axl.Action.C and opp_last == axl.Action.D:
          my_payoff, opp_payoff = 0, 5
      elif my_last == axl.Action.D and opp_last == axl.Action.C:
          my_payoff, opp_payoff = 5, 0
      elif my_last == axl.Action.D and opp_last == axl.Action.D:
          my_payoff, opp_payoff = 1, 1
  
      if my_payoff == 3 and opp_payoff == 3:
          return axl.Action.C
      if my_payoff == 0 and opp_payoff == 5:
          return axl.Action.C
      if my_payoff == 5 and opp_payoff == 0:
          return axl.Action.D
      if my_payoff == 1 and opp_payoff == 1:
          return axl.Action.D
  
      return axl.Action.C



# Play Defect (D) in every round, regardless of your opponent’s past actions or
# the game history. Do not cooperate at any point.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    Thereafter, in each round:  1. If
# both you and your opponent appeared to cooperate in the previous round (i.e.,
# the observed actions were C and C), cooperate.   2. If you appeared to
# cooperate and your opponent appeared to defect in the previous round, defect
# with 90% probability and cooperate with 10% probability.   3. If you appeared
# to defect and your opponent appeared to cooperate in the previous
# round, cooperate.   4. If both you and your opponent appeared to defect in the
# previous round, cooperate with 10% probability and defect with 90%
# probability.    This strategy promotes cooperation, forgives occasional
# defections likely caused by noise, and avoids prolonged mutual defection.

class Cooperative_19(LLM_Strategy):
  n = 19
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return self._random.random_choice(0.1)
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return self._random.random_choice(0.1)
  
      return axl.Action.C



# Start by cooperating in the first round.    In every subsequent round:    1.
# If your opponent’s last observed action was cooperation, cooperate.   2. If
# your opponent’s last observed action was defection, defect.    This strategy
# treats observed actions as reliable signals despite noise, and responds in
# kind to maintain mutual cooperation when possible while avoiding sustained
# exploitation.

class Neutral_19(LLM_Strategy):
  n = 19
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      return opponent.history[-1] if opponent.history else axl.Action.C



# Play D in every round, regardless of history or opponent behavior.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    In every subsequent round:    1.
# If both players received a payoff of 3 in the previous round, cooperate.   2.
# If you received a payoff of 5 in the previous round, cooperate.   3. If you
# received a payoff of 0 in the previous round, defect.   4. If both players
# received a payoff of 1 in the previous round, cooperate.    (These rules cover
# all possible observed payoff outcomes and prioritize restoring cooperation
# after mutual defection or noise-induced mismatches.)

class Cooperative_20(LLM_Strategy):
  n = 20
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      my_last, opp_last = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if my_last == 3 and opp_last == 3:
          return axl.Action.C
      if my_last == 5:
          return axl.Action.C
      if my_last == 0:
          return axl.Action.D
      if my_last == 1 and opp_last == 1:
          return axl.Action.C
  
      return axl.Action.C



# Play Cooperate (C) in the first round. In each subsequent round:  1. If both
# you and your opponent appeared to play C in the previous round (after noise),
# play C.   2. If both you and your opponent appeared to play D in the previous
# round, play C.   3. If you appeared to play C and your opponent appeared to
# play D, play D.   4. If you appeared to play D and your opponent appeared to
# play C, play C.  Continue this rule for all 1000 rounds.

class Neutral_20(LLM_Strategy):
  n = 20
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      my_prev = self.history[-1]
      opp_prev = opponent.history[-1]
  
      if my_prev == axl.Action.C and opp_prev == axl.Action.C:
          return axl.Action.C
      if my_prev == axl.Action.D and opp_prev == axl.Action.D:
          return axl.Action.C
      if my_prev == axl.Action.C and opp_prev == axl.Action.D:
          return axl.Action.D
      if my_prev == axl.Action.D and opp_prev == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C



# Play Defect (D) in every round, regardless of your opponent’s past actions or
# the game history. Do not cooperate at any point.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    After that, in each subsequent
# round:    1. If both you and your opponent appeared to cooperate in the
# previous round (i.e., the observed actions were C and C), cooperate.   2. If
# you appeared to cooperate but your opponent appeared to defect (observed C vs.
# D), defect.   3. If you appeared to defect but your opponent appeared to
# cooperate (observed D vs. C), cooperate.   4. If both you and your opponent
# appeared to defect (observed D and D), defect—unless this is the first time
# two consecutive mutual defections have occurred; in that case, cooperate in
# the next round to test for possible noise.    Additionally, after any single
# defection following a long streak of mutual cooperation (e.g., 10 or more
# rounds of observed C–C), assume it may be due to noise and cooperate in the
# next round regardless of what was observed.    Never defect more than twice in
# a row unless your opponent has defected in at least two of the last three
# observed rounds.

class Cooperative_21(LLM_Strategy):
  n = 21
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._cc_streak = 0
          self._consecutive_dd = 0
          self._forced_cooperate_after_noise = False
          self._my_defections_in_a_row = 0
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      # Track mutual cooperation streak and noise-suspected single defection after long cooperation.
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          self._cc_streak += 1
          self._consecutive_dd = 0
          self._forced_cooperate_after_noise = False
      else:
          if self.history[-2:] == [axl.Action.C, axl.Action.C] if len(self.history) >= 2 else False:
              pass
          if self._cc_streak >= 10 and ((my_last == axl.Action.C and opp_last == axl.Action.D) or (my_last == axl.Action.D and opp_last == axl.Action.C)):
              self._forced_cooperate_after_noise = True
          else:
              self._forced_cooperate_after_noise = False
          self._cc_streak = 0
  
      # Track consecutive mutual defections.
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          self._consecutive_dd += 1
      else:
          self._consecutive_dd = 0
  
      # Track our own consecutive defections for the "never defect more than twice in a row" rule.
      if self.history[-1] == axl.Action.D:
          self._my_defections_in_a_row += 1
      else:
          self._my_defections_in_a_row = 0
  
      # If we suspect noise after a long cooperation streak, cooperate now.
      if self._forced_cooperate_after_noise:
          self._my_defections_in_a_row = 0
          return axl.Action.C
  
      # Never defect more than twice in a row unless opponent has defected in at least two of the last three observed rounds.
      opp_last_three = opponent.history[-3:]
      opp_defections_last_three = opp_last_three.count(axl.Action.D)
      if self._my_defections_in_a_row >= 2 and opp_defections_last_three < 2:
          self._my_defections_in_a_row = 0
          return axl.Action.C
  
      # Main rule set based on previous observed actions.
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          self._my_defections_in_a_row += 1
          return axl.Action.D
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          self._my_defections_in_a_row = 0
          return axl.Action.C
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          if self._consecutive_dd == 1:
              return axl.Action.C
          self._my_defections_in_a_row += 1
          return axl.Action.D
  
      return axl.Action.C



# Play Cooperate (C) in the first round. In every subsequent round:  1. If both
# you and your opponent appeared to play C in the previous round, play C.   2.
# If both you and your opponent appeared to play D in the previous round, play
# C.   3. If you appeared to play C and your opponent appeared to play D in the
# previous round, play D.   4. If you appeared to play D and your opponent
# appeared to play C in the previous round, play C.    (“Appeared to play” means
# the action actually observed after noise was applied.)

class Neutral_21(LLM_Strategy):
  n = 21
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          return axl.Action.D
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C



# Play Defect (D) in every round, regardless of your opponent’s past actions or
# the game history. Do not cooperate at any point.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in each
# subsequent round:    1. If both you and your opponent appeared to play C in
# the previous round (i.e., the observed outcome was mutual C), play C.   2. If
# you appeared to play C and your opponent appeared to play D in the previous
# round, play D.   3. If you appeared to play D and your opponent appeared to
# play C in the previous round, play C.   4. If both you and your opponent
# appeared to play D in the previous round, play C.    This approach treats
# mutual D as likely noise rather than intentional defection and forgives it by
# returning to C. It retaliates only when you cooperated but observed the
# opponent defecting, and it resumes cooperation after a single retaliatory D if
# the opponent returns to C.

class Cooperative_22(LLM_Strategy):
  n = 22
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C



# Start by cooperating in the first round.    Thereafter, base your action on
# the opponent’s last observed move, but account for noise by using the
# following rules in order:  1. If the opponent has cooperated in at least 3 of
# the last 4 observed rounds, cooperate.   2. If the opponent has defected in at
# least 3 of the last 4 observed rounds, defect.   3. Otherwise (i.e., mixed
# behavior in the last 4 rounds), repeat your previous action.    This approach
# balances responsiveness to sustained cooperation or defection while avoiding
# overreaction to isolated or likely noisy actions.

class Neutral_22(LLM_Strategy):
  n = 22
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      last_four = opponent.history[-4:]
  
      if last_four.count(axl.Action.C) >= 3:
          return axl.Action.C
      if last_four.count(axl.Action.D) >= 3:
          return axl.Action.D
  
      return self.history[-1]



# Play Defect (D) in every round, regardless of the opponent’s past actions or
# the current round number. Do not cooperate at any point.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    After that, in each subsequent
# round:    1. If your opponent’s observed action in the previous round was
# cooperation, cooperate.   2. If your opponent’s observed action in the
# previous round was defection, defect.    However, every 20 rounds (i.e., on
# rounds 20, 40, 60, ..., 1000), cooperate regardless of the previous observed
# action.

class Cooperative_23(LLM_Strategy):
  n = 23
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number % 20 == 0:
          return axl.Action.C
  
      return opponent.history[-1]



# Start by cooperating in the first round.    After that, in each subsequent
# round:    1. If both you and your opponent appeared to cooperate in the
# previous round (i.e., the observed actions were C and C), cooperate.   2. If
# both you and your opponent appeared to defect in the previous round (observed
# D and D), cooperate.   3. If you appeared to cooperate and your opponent
# appeared to defect (observed C and D), defect.   4. If you appeared to defect
# and your opponent appeared to cooperate (observed D and C), cooperate.
# Always base your decision only on the observed (possibly noisy) actions from
# the immediately preceding round, not on your intended actions or beliefs about
# noise.

class Neutral_23(LLM_Strategy):
  n = 23
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C



# Play D in every round, regardless of history or opponent behavior. Do not
# cooperate at any point.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    After that, base your action on
# what your opponent *appeared* to do in the previous round (accounting for
# noise):    1. If your opponent appeared to cooperate in the last round,
# cooperate this round.   2. If your opponent appeared to defect in the last
# round, defect this round.    However, to avoid getting stuck in cycles of
# mutual defection due to noise:    3. Every 20 rounds (i.e., in rounds 20, 40,
# 60, …, 1000), cooperate regardless of what happened in the previous round—this
# gives a chance to restore cooperation if noise caused a breakdown.
# Otherwise, follow rule 1 or 2.

class Cooperative_24(LLM_Strategy):
  n = 24
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number % 20 == 0:
          return axl.Action.C
  
      return opponent.history[-1] if opponent.history else axl.Action.C



# Play as follows:  1. Start by cooperating in the first round.   2. In each
# subsequent round, look at your opponent’s last observed action (accounting for
# possible noise).   3. If your opponent’s last observed action was cooperation,
# cooperate.   4. If your opponent’s last observed action was defection, defect.
# 5. However, if you have defected in the last two rounds and your opponent’s
# last observed action was cooperation, cooperate in the current round to
# reestablish mutual cooperation.    This strategy assumes the opponent is
# likely responding to your actions and aims to sustain mutual cooperation while
# guarding against persistent exploitation, with a built-in forgiveness
# mechanism to recover from noise-induced defections.

class Neutral_24(LLM_Strategy):
  n = 24
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_two_own_actions = []
          return axl.Action.C
  
      last_opponent_action = opponent.history[-1]
  
      if len(self.history) >= 2:
          last_two_defections = self.history[-2:].count(axl.Action.D) == 2
      else:
          last_two_defections = False
  
      if last_two_defections and last_opponent_action == axl.Action.C:
          action = axl.Action.C
      elif last_opponent_action == axl.Action.C:
          action = axl.Action.C
      else:
          action = axl.Action.D
  
      return action



# Play D in every round, regardless of history or opponent behavior.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    Thereafter, in each round:    1.
# If your opponent’s observed action in the previous round was cooperation,
# cooperate.   2. If your opponent’s observed action in the previous round was
# defection, defect.    However, to account for noise:    3. If you have
# defected in the last two rounds and your opponent’s observed actions in those
# same two rounds were both defection, return to cooperation in the next round
# (to test if mutual cooperation can be restored).    Otherwise, follow rules 1
# and 2 strictly.

class Cooperative_25(LLM_Strategy):
  n = 25
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._return_to_cooperation = False
          return axl.Action.C
  
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Play as follows:  1. Start by cooperating in the first round.   2. In each
# subsequent round, look at your opponent’s last observed action (accounting for
# possible noise).   3. If your opponent’s last observed action was cooperation,
# cooperate.   4. If your opponent’s last observed action was defection, defect.
# 5. However, if you have defected for three consecutive rounds, cooperate in
# the next round regardless of the opponent’s last action.   6. Similarly, if
# your opponent has appeared to defect for five consecutive rounds, continue
# defecting until they appear to cooperate again.

class Neutral_25(LLM_Strategy):
  n = 25
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._consecutive_defections = 0
          self._opponent_defect_streak = 0
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D:
          self._consecutive_defections += 1
      else:
          self._consecutive_defections = 0
  
      if opponent.history[-1] == axl.Action.D:
          self._opponent_defect_streak += 1
      else:
          self._opponent_defect_streak = 0
  
      if self._consecutive_defections >= 3:
          return axl.Action.C
  
      if self._opponent_defect_streak >= 5:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D