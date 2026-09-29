import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# Start by playing C in the first round.    Thereafter, in each subsequent
# round:   - If your opponent played C in the previous round, play C.   - If
# your opponent played D in the previous round, play D.    Continue this pattern
# for all 1000 rounds.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]



# Play Cooperate (C) in the first round.    For rounds 2 through 997:   - If
# your opponent played C in the previous round, play C.   - If your opponent
# played D in the previous round, play D.    In rounds 998, 999, and 1000:   -
# Always play Defect (D), regardless of the opponent’s prior actions.
# Additionally, if the opponent defects only once and then returns to
# cooperating, treat that single defection as if it never happened—resume
# cooperation after one retaliatory D (i.e., if you played D in response to
# their D, but they play C in the next round, you play C in the following
# round).    However, if the opponent defects twice within any three consecutive
# rounds, revert to always playing D for the remainder of the game.

class Cooperative_1(LLM_Strategy):
  n = 1
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._permanent_defect = False
          self._last_opponent_defection_round = None
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if getattr(self, "_permanent_defect", False):
          return axl.Action.D
  
      if round_number >= 998:
          return axl.Action.D
  
      if len(opponent.history) >= 2:
          last_three = opponent.history[-3:]
          if last_three.count(axl.Action.D) >= 2:
              self._permanent_defect = True
              return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Opponent defected last round.
      # If this is a second consecutive defection, or a defection within any 3-round window,
      # switch to permanent defection.
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
          self._permanent_defect = True
          return axl.Action.D
  
      # Single defection: retaliate once, then return to cooperation if they cooperate next.
      return axl.Action.D



# Start by cooperating in the first round. Then, for each subsequent round up to
# round 999, follow these rules in order:  1. If your opponent cooperated in the
# previous round, cooperate.   2. If your opponent defected in the previous
# round, defect.    In round 1000 (the final round), defect regardless of your
# opponent’s previous move.

class Neutral_1(LLM_Strategy):
  n = 1
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1]



# Start by playing C in the first round.    After that, in each subsequent
# round:   - If your opponent played C in the previous round, play C.   - If
# your opponent played D in the previous round, play D.    Continue this pattern
# for all 1000 rounds.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Play Cooperate (C) in the first round.    For rounds 2 through 990:   - If
# your opponent played C in the previous round, play C.   - If your opponent
# played D in the previous round, play D.    For rounds 991 through 1000:   -
# Always play Defect (D), regardless of your opponent’s previous moves.

class Cooperative_2(LLM_Strategy):
  n = 2
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Cooperate in the first round. In every subsequent round, copy what your
# opponent played in the previous round.

class Neutral_2(LLM_Strategy):
  n = 2
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]



# Start by playing D in the first round. After that, follow these rules in
# order:  1. If your opponent played D in the previous round, play D.   2. If
# your opponent played C in the previous round, play D—but only if you have
# defected fewer than 10 times so far.   3. Otherwise (i.e., your opponent
# played C and you’ve already defected at least 10 times), play C.    This
# approach aggressively exploits cooperation early on while leaving room to
# establish mutual cooperation later if the opponent consistently cooperates,
# thereby avoiding long-term mutual defection.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.defections_so_far = 0
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D:
          self.defections_so_far += 1
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if self.defections_so_far < 10:
          return axl.Action.D
  
      return axl.Action.C



# Start by playing C in the first round.  In each subsequent round, follow these
# rules in order:  1. If fewer than 10 rounds remain, always play D.   2. If
# your opponent played C in the previous round, play C.   3. If your opponent
# played D in the previous round, play D—but only for one round. After that
# single retaliatory D, return to C regardless, to test whether the opponent is
# willing to cooperate again.    This approach encourages sustained cooperation,
# limits long-term loss from mutual defection after a single defection, and
# accounts for the known endpoint of the game by defecting in the final 10
# rounds.

class Cooperative_3(LLM_Strategy):
  n = 3
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._retaliated_last_round = False
          return axl.Action.C
  
      if 1000 - len(self.history) <= 10:
          self._retaliated_last_round = False
          return axl.Action.D
  
      if self._retaliated_last_round:
          self._retaliated_last_round = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          self._retaliated_last_round = True
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the first round. In each subsequent round, follow
# these rules in order:  1. If fewer than 10 rounds remain, always defect.   2.
# If your opponent cooperated in the previous round, cooperate.   3. If your
# opponent defected in the previous round, defect—but if you have defected for
# two consecutive rounds and your opponent just cooperated, return to
# cooperation.

class Neutral_3(LLM_Strategy):
  n = 3
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._consecutive_defections = 0
          return axl.Action.C
  
      if len(self.history) >= 10 and self.history[-10:].count(axl.Action.D) == 10:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          if len(self.history) >= 2 and self.history[-2:] == [axl.Action.D, axl.Action.D]:
              self._consecutive_defections = 0
              return axl.Action.C
          self._consecutive_defections = 0
          return axl.Action.C
  
      self._consecutive_defections = getattr(self, "_consecutive_defections", 0) + 1
      return axl.Action.D



# Start by playing C in the first round. After that, in each subsequent round:
# 1. If your opponent played C in the previous round, play C.   2. If your
# opponent played D in the previous round, play D.    Continue this pattern for
# all 1000 rounds.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]



# Play C in the first round.    For rounds 2 through 990:   - If your opponent
# played C in the previous round, play C.   - If your opponent played D in the
# previous round, play D.    For rounds 991 through 1000:   - Always play D,
# regardless of your opponent’s prior actions.

class Cooperative_4(LLM_Strategy):
  n = 4
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      return opponent.history[-1]



# Begin by cooperating in the first round. In each subsequent round:  - If your
# opponent cooperated in the previous round, cooperate.   - If your opponent
# defected in the previous round, defect.    (Do not label this approach as
# “neutral,” as starting with cooperation reflects a cooperative bias, not
# neutrality.)

class Neutral_4(LLM_Strategy):
  n = 4
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]



# Start by playing C in the first round.    In every subsequent round:   - If
# your opponent played C in the previous round, play C.   - If your opponent
# played D in the previous round, play D.    Continue this pattern for all 1000
# rounds.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Start by playing C in the first round.    In each subsequent round:    1. If
# your opponent played C in the previous round, play C.   2. If your opponent
# played D in the previous round, play D—but only defect once in response.   3.
# After retaliating with a single D, return to playing C in the following round
# regardless of the opponent’s last move, unless you are within the last 10
# rounds of the game.   4. In the final 10 rounds (rounds 991–1000), always
# mirror your opponent’s previous move exactly (i.e., play C if they played C
# last round, D if they played D), without offering unprompted forgiveness.
# Continue this pattern for all 1000 rounds.

class Cooperative_5(LLM_Strategy):
  n = 5
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._retaliated_last_round = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return opponent.history[-1]
  
      if self._retaliated_last_round:
          self._retaliated_last_round = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          self._retaliated_last_round = True
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the first round. Then, for each subsequent round up to
# round 999, follow these rules in order:  1. If your opponent cooperated in the
# previous round, cooperate.   2. If your opponent defected in the previous
# round, defect—but if both you and your opponent defected in the previous
# round, cooperate in the current round to attempt to restore mutual
# cooperation.    In round 1000, defect regardless of prior history.

class Neutral_5(LLM_Strategy):
  n = 5
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D



# Start by playing C in the first round. After that, play D if your opponent
# played D in the previous round; otherwise, play C. However, if your opponent
# has defected in more than half of all previous rounds, switch to playing D for
# all remaining rounds.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if opponent.history.defections > len(opponent.history) / 2:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the first round.    In every subsequent round:   - If
# your opponent cooperated in the immediately preceding round, cooperate.   - If
# your opponent defected in the immediately preceding round, defect.

class Cooperative_6(LLM_Strategy):
  n = 6
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]



# Play C in the first round.    In each subsequent round up to round 998:   - If
# your opponent played C in the previous round, play C.   - If your opponent
# played D in the previous round, play D.    In rounds 999 and 1000:   - Always
# play D.

class Neutral_6(LLM_Strategy):
  n = 6
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) >= 998:
          return axl.Action.D
  
      return opponent.history[-1]



# Start by playing C in the first round.    In each subsequent round:   - If
# your opponent played C in the previous round, play C.   - If your opponent
# played D in the previous round, play D.    Continue this pattern for all 1000
# rounds.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      return opponent.history[-1]



# Start by cooperating in the first round.   In each subsequent round up to
# round 997, copy what your opponent played in the previous round.   If you and
# your opponent have both defected for three consecutive rounds, cooperate in
# the next round to attempt to restore mutual cooperation.   From round 998
# onward, always defect—regardless of the opponent’s prior actions—to remove
# endgame exploitation risk.

class Cooperative_7(LLM_Strategy):
  n = 7
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._consecutive_mutual_defections = 0
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 998:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          self._consecutive_mutual_defections += 1
      else:
          self._consecutive_mutual_defections = 0
  
      if self._consecutive_mutual_defections >= 3:
          self._consecutive_mutual_defections = 0
          return axl.Action.C
  
      return opponent.history[-1]



# Begin by cooperating in the first round. In each subsequent round, follow
# these rules in order:  1. If you are in round 999 or later (i.e., one of the
# last two rounds), defect.   2. If your opponent cooperated in the previous
# round, cooperate.   3. If your opponent defected in the previous round,
# defect—but if they return to cooperation after defecting, resume cooperation
# in the following round.

class Neutral_7(LLM_Strategy):
  n = 7
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Start by playing D in the first round.    Thereafter, in each subsequent
# round:   - If your opponent played C in the previous round, play D (to exploit
# their cooperation).   - If your opponent played D in the previous round, play
# D (to avoid being exploited and maintain aggression).    In short: always play
# D, regardless of history.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    For rounds 2 through
# 990, follow this rule:   - If your opponent played C in the previous round,
# play C.   - If your opponent played D in the previous round, play D.    For
# the final 10 rounds (rounds 991 to 1000):   - Always play Defect (D),
# regardless of the opponent’s prior actions.    Additionally, if at any point
# your opponent defects only once but then returns to cooperating for two
# consecutive rounds, treat the single defection as a possible error and resume
# cooperation (i.e., play C in response to their second consecutive C after a
# lone D).

class Cooperative_8(LLM_Strategy):
  n = 8
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if len(opponent.history) >= 3:
          if (
              opponent.history[-3] == axl.Action.D
              and opponent.history[-2] == axl.Action.C
              and opponent.history[-1] == axl.Action.C
          ):
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in the first round. Then, for each subsequent round up to
# round 990, follow these rules in order:  1. If your opponent cooperated in the
# previous round, cooperate.   2. If your opponent defected in the previous
# round, defect—but if you and your opponent have both defected for the last
# three consecutive rounds, cooperate in the next round to attempt to restore
# mutual cooperation.  For rounds 991 through 1000 (the final 10 rounds), always
# defect regardless of the opponent’s actions.

class Neutral_8(LLM_Strategy):
  n = 8
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if len(self.history) >= 3:
          last_three_self = self.history[-3:]
          last_three_opp = opponent.history[-3:]
          if (
              last_three_self.count(axl.Action.D) == 3
              and last_three_opp.count(axl.Action.D) == 3
          ):
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Play D in the first round.   In every subsequent round, play D regardless of
# your opponent’s previous move.    (Always defect from round 1 to round 1000.)

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Play Cooperate (C) in the first round.    For rounds 2 through 999:   - If
# your opponent played C in the previous round, play C.   - If your opponent
# played D in the previous round, play D—unless the previous round was the first
# time your opponent defected after a streak of cooperation; in that case, still
# play C once as a gesture of forgiveness (i.e., allow one isolated defection
# without retaliation).    In round 1000 (the final round):   - Play D only if
# your opponent defected in round 999.   - Otherwise, play C.

class Cooperative_9(LLM_Strategy):
  n = 9
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forgave_last_defection = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D if opponent.history[-1] == axl.Action.D else axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          self._forgave_last_defection = False
          return axl.Action.C
  
      # Opponent played D last round.
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.C and not self._forgave_last_defection:
          self._forgave_last_defection = True
          return axl.Action.C
  
      self._forgave_last_defection = False
      return axl.Action.D



# Start by playing C in the first round.    In each subsequent round:    1. If
# your opponent played C in the previous round, play C.   2. If your opponent
# played D in the previous round, play D—but if this results in two consecutive
# rounds of mutual D, return to playing C in the next round to attempt to
# restore cooperation.

class Neutral_9(LLM_Strategy):
  n = 9
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._return_to_cooperate = False
          return axl.Action.C
  
      if getattr(self, "_return_to_cooperate", False):
          self._return_to_cooperate = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Opponent defected last round.
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._return_to_cooperate = True
  
      return axl.Action.D



# Start by playing D in the first round. After that, in each subsequent round:
# 1. If your opponent played C in the previous round, play D (to exploit their
# cooperation).   2. If your opponent played D in the previous round, play D (to
# avoid being exploited and maintain aggression).    In short: always play D,
# regardless of the opponent’s prior move.

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return axl.Action.D



# Play Cooperate (C) in the first round.    From round 2 up to round 998, follow
# this rule:   - If your opponent played C in the previous round, play C.   - If
# your opponent played D in the previous round, play D.    In round 999, play D
# regardless of prior history.    In round 1000, play D regardless of prior
# history.

class Cooperative_10(LLM_Strategy):
  n = 10
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 999:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    In each subsequent round
# up to round 990:   1. If your opponent played C in the previous round, play C.
# 2. If your opponent played D in the previous round, play D.   3. However, if
# both you and your opponent played D in the previous round, play C in the
# current round (to attempt restoring cooperation).    From round 991 to round
# 1000 (the final 10 rounds):   - Always play Defect (D), regardless of the
# opponent’s prior actions.

class Neutral_10(LLM_Strategy):
  n = 10
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Start by playing D in the first round. After that, follow these rules in
# order:  1. If your opponent played D in the previous round, play D.   2. If
# your opponent played C in the previous round, play D—unless you have defected
# for five consecutive rounds already; in that case, play C once to test for
# renewed cooperation.   3. If your opponent responds to your test C by playing
# C, immediately return to D in the next round to exploit the cooperation.   4.
# If the opponent responds to your test C by playing D, continue playing D.
# Always prioritize defection, but use a single, brief cooperative probe every
# five rounds of mutual or unilateral defection to check if renewed mutual
# cooperation (which you would then exploit) is possible.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._probe_pending = False
          self._probe_used = False
          return axl.Action.D
  
      # If we previously played a cooperative probe, react to the opponent's response.
      if getattr(self, "_probe_pending", False):
          self._probe_pending = False
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.D
          return axl.Action.D
  
      # Count consecutive defections by us.
      consecutive_d = 0
      for move in reversed(self.history):
          if move == axl.Action.D:
              consecutive_d += 1
          else:
              break
  
      # Every five consecutive defections, use a single cooperative probe if not already used.
      if consecutive_d >= 5 and not getattr(self, "_probe_used", False):
          self._probe_used = True
          self._probe_pending = True
          return axl.Action.C
  
      # Default: always defect.
      return axl.Action.D



# Start by cooperating in the first round. Then, for each subsequent round up to
# round 990:  1. If your opponent cooperated in the previous round, cooperate.
# 2. If your opponent defected in the previous round, defect.    From round 991
# onward (the final 10 rounds), always defect regardless of the opponent’s
# actions.    Additionally, if mutual defection has occurred for five
# consecutive rounds before round 990, attempt to restore cooperation by playing
# C in the next round. If the opponent responds with C, return to the standard
# rule (cooperate after opponent’s C, defect after opponent’s D). If the
# opponent responds with D, revert to defection and do not attempt further
# reconciliation.

class Cooperative_11(LLM_Strategy):
  n = 11
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._reconcile_attempted = False
          self._reconcile_failed = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if getattr(self, "_reconcile_failed", False):
          return axl.Action.D
  
      if len(self.history) >= 5:
          last_five_self = self.history[-5:]
          last_five_opp = opponent.history[-5:]
          if (
              last_five_self.count(axl.Action.D) == 5
              and last_five_opp.count(axl.Action.D) == 5
              and not getattr(self, "_reconcile_attempted", False)
          ):
              self._reconcile_attempted = True
              return axl.Action.C
  
      if getattr(self, "_reconcile_attempted", False):
          if opponent.history[-1] == axl.Action.C:
              self._reconcile_attempted = False
              return axl.Action.C
          else:
              self._reconcile_failed = True
              return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in the first round. Then, for each subsequent round up to
# round 999, follow these rules in order:  1. If your opponent cooperated in the
# previous round, cooperate.   2. If your opponent defected in the previous
# round, defect—but if mutual defection has occurred for two consecutive rounds,
# cooperate in the next round to attempt to restore cooperation.  In round 1000
# (the final round), defect regardless of prior history.

class Neutral_11(LLM_Strategy):
  n = 11
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._restore_coop = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if getattr(self, "_restore_coop", False):
          self._restore_coop = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._restore_coop = True
          return axl.Action.C
  
      return axl.Action.D



# Start by playing C in the first round.    Thereafter, in each subsequent
# round:   - If your opponent played C in the previous round, play C.   - If
# your opponent played D in the previous round, play D.    Continue this pattern
# for all 1000 rounds.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]



# Cooperate in round 1.    For each round from 2 to 1000:   - If your opponent
# played C in the previous round, play C.   - If your opponent played D in the
# previous round, play D.

class Cooperative_12(LLM_Strategy):
  n = 12
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Play C in the first round.    For each subsequent round up to round 997:   -
# If your opponent played C in the previous round, play C.   - If your opponent
# played D in the previous round, play D in the current round, but if you then
# observe your opponent playing C in the following round (i.e., two rounds after
# their defection), return to playing C.    For rounds 998, 999, and 1000:   -
# Play D regardless of prior moves.

class Neutral_12(LLM_Strategy):
  n = 12
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 998:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Start by playing C in the first round. After that, in each subsequent round:
# 1. If your opponent played C in the previous round, play C.   2. If your
# opponent played D in the previous round, play D.    Continue this pattern for
# all 1000 rounds.

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]



# Start by playing Cooperate (C) in the first round.  After that, in each
# subsequent round:  1. If your opponent played C in the previous round, play C.
# 2. If your opponent played D in the previous round, play D—but only for one
# round.   3. If you played D in response to an opponent’s D in the previous
# round, return to C in the next round regardless, to offer a chance to restore
# mutual cooperation.   4. However, in the last 10 rounds (rounds 991–1000),
# always play D, regardless of the opponent’s prior actions.  Continue this
# pattern for all 1000 rounds.

class Cooperative_13(LLM_Strategy):
  n = 13
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_was_retaliation = False
          return axl.Action.C
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      if self._last_was_retaliation:
          self._last_was_retaliation = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          self._last_was_retaliation = True
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the first round. After that, follow these rules in
# order:  1. If your opponent cooperated in the previous round, cooperate in the
# current round.   2. If your opponent defected in the previous round, defect in
# the current round—but if you have defected for two consecutive rounds and your
# opponent cooperates in the most recent round, return to cooperation.   3. In
# the last 10 rounds (rounds 991–1000), always defect regardless of the
# opponent’s prior actions.

class Neutral_13(LLM_Strategy):
  n = 13
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_streak = 0
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          self._defect_streak = 0
          return axl.Action.C
  
      # Opponent defected last round
      if self.history[-1] == axl.Action.D:
          self._defect_streak += 1
      else:
          self._defect_streak = 1
  
      if self._defect_streak >= 2 and opponent.history[-1] == axl.Action.C:
          self._defect_streak = 0
          return axl.Action.C
  
      return axl.Action.D



# Start by playing C in the first round.    In every subsequent round:   - If
# your opponent played C in the previous round, play C.   - If your opponent
# played D in the previous round, play D.    However, if your opponent has
# defected in 3 or more of the last 5 rounds, switch to playing D for all
# remaining rounds.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forced_defect = False
          return axl.Action.C
  
      if getattr(self, "_forced_defect", False):
          return axl.Action.D
  
      if len(opponent.history) >= 5 and opponent.history[-5:].count(axl.Action.D) >= 3:
          self._forced_defect = True
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.  For rounds 2 through 998,
# follow this rule:   - If your opponent played C in the previous round, play C.
# - If your opponent played D in the previous round, play D.  In round 999:   -
# Play C only if your opponent played C in round 998.   - Otherwise, play D.  In
# round 1000:   - Play D regardless of the opponent’s previous move.

class Cooperative_14(LLM_Strategy):
  n = 14
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number <= 998:
          return opponent.history[-1]
  
      if round_number == 999:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      return axl.Action.D



# Play D in the first round.    For each subsequent round up to round 990:   -
# If your opponent played C in the previous round, play C.   - If your opponent
# played D in the previous round, play D.    From round 991 through round 1000
# (the final 10 rounds), always play D.

class Neutral_14(LLM_Strategy):
  n = 14
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      return opponent.history[-1]



# Play D in the first round.   In every subsequent round, play D regardless of
# your opponent’s previous move.    This strategy assumes the opponent may adapt
# to your actions, and since a single defection yields the highest immediate
# payoff (5) and mutual defection (1) is safer than being exploited (0), it
# prioritizes avoiding exploitation and securing advantage whenever possible.
# Given the fixed 1000-round horizon and the payoff structure, always defecting
# maximizes payoff against non-cooperative or retaliatory opponents and cannot
# be outperformed by cooperation in the worst case.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    In each subsequent
# round:    1. If your opponent played C in the previous round, play C.   2. If
# your opponent played D in the previous round, play D—but only defect once in
# response to a single defection.   3. If you defected in the previous round
# *because* your opponent defected two rounds ago, return to C in the current
# round regardless of the opponent’s last move, provided the opponent has not
# defected again since.   4. In the final 10 rounds (rounds 991–1000), always
# play D, regardless of prior history.

class Cooperative_15(LLM_Strategy):
  n = 15
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_defection = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      # If we defected last round in response to opponent's defection two rounds ago,
      # return to cooperation now, provided the opponent did not defect again last round.
      if len(self.history) >= 2:
          if self.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D and opponent.history[-1] == axl.Action.C:
              return axl.Action.C
  
      # Respond to the opponent's previous move.
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Opponent defected last round: defect once in response.
      return axl.Action.D



# Begin by cooperating in the first round. For each subsequent round up to round
# 990, mirror your opponent’s previous move: cooperate if they cooperated in the
# last round, defect if they defected.    From round 991 onward, always defect
# regardless of the opponent’s actions.    Additionally, if mutual defection
# occurs for three consecutive rounds before round 991, attempt to restore
# cooperation by cooperating once; if the opponent responds with cooperation in
# the following round, return to mirroring their previous move; if they defect
# again, revert to mirroring (i.e., defect) and do not attempt further
# reconciliation.

class Neutral_15(LLM_Strategy):
  n = 15
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._reconcile_mode = False
          self._reconcile_pending = False
          self._reconcile_triggered = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if getattr(self, "_reconcile_pending", False):
          self._reconcile_pending = False
          if opponent.history[-1] == axl.Action.C:
              self._reconcile_mode = False
              return axl.Action.C
          self._reconcile_mode = False
          self._reconcile_triggered = True
          return axl.Action.D
  
      if getattr(self, "_reconcile_mode", False):
          return opponent.history[-1]
  
      if not getattr(self, "_reconcile_triggered", False) and len(self.history) >= 3:
          if (
              self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
              and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
          ):
              self._reconcile_mode = True
              self._reconcile_pending = True
              return axl.Action.C
  
      return opponent.history[-1]



# Start by playing C in the first round. After that, play C if your opponent
# played C in the previous round; otherwise, play D. However, if your opponent
# has defected in more than half of all previous rounds, defect for the rest of
# the game.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_forever = False
          return axl.Action.C
  
      if self._defect_forever:
          return axl.Action.D
  
      if opponent.history.defections > len(opponent.history) / 2:
          self._defect_forever = True
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    For rounds 2 through
# 990, follow these rules in order:   1. If your opponent played C in the
# previous round, play C.   2. If your opponent played D in the previous round,
# play D—unless you have already defected in response once and your opponent
# returns to C, in which case resume playing C.   3. If you and your opponent
# have both played D for five consecutive rounds, play C in the next round to
# attempt to restore cooperation.    For rounds 991 through 1000:   - Always
# play D, regardless of prior history.

class Cooperative_16(LLM_Strategy):
  n = 16
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defected_in_response_once = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if len(self.history) >= 5:
          last_five_self = self.history[-5:]
          last_five_opp = opponent.history[-5:]
          if last_five_self.count(axl.Action.D) == 5 and last_five_opp.count(axl.Action.D) == 5:
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          if self._defected_in_response_once:
              return axl.Action.C
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          self._defected_in_response_once = True
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the first round. Thereafter, follow these rules in
# order:  1. If your opponent cooperated in the previous round, cooperate in the
# current round.   2. If your opponent defected in the previous round, defect in
# the current round—but if you and your opponent have both defected for two
# consecutive rounds, cooperate in the next round to attempt to restore mutual
# cooperation.

class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._both_defected_twice = False
          return axl.Action.C
  
      if self._both_defected_twice:
          self._both_defected_twice = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._both_defected_twice = True
          return axl.Action.C
  
      return axl.Action.D



# Start by playing D in the first round. After that, follow these rules in
# order:  1. If your opponent played D in the previous round, play D.   2. If
# your opponent played C in the previous round, play D—unless you have defected
# for five consecutive rounds already; in that case, play C once to test for
# renewed cooperation.   3. If you play C as a test and your opponent responds
# with C, immediately return to D in the next round to exploit their
# cooperation.   4. If the test C is met with D, resume defecting and do not
# test again for at least another ten rounds.    Continue applying these rules
# for all 1000 rounds.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._test_cooldown = 0
          self._test_pending = False
          self._last_test_round = None
          return axl.Action.D
  
      round_number = len(self.history) + 1
      opp_last = opponent.history[-1]
      my_last = self.history[-1]
  
      if self._test_pending:
          self._test_pending = False
          if opp_last == axl.Action.C:
              self._test_cooldown = 0
              return axl.Action.D
          else:
              self._test_cooldown = 10
              return axl.Action.D
  
      if self._test_cooldown > 0:
          self._test_cooldown -= 1
  
      if opp_last == axl.Action.D:
          return axl.Action.D
  
      if opp_last == axl.Action.C:
          if self.history[-5:].count(axl.Action.D) == 5 and self._test_cooldown == 0:
              self._test_pending = True
              self._last_test_round = round_number
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.D



# Play Cooperate (C) in the first round.    For each subsequent round up to
# round 999:   1. If your opponent played C in the previous round, play C.   2.
# If your opponent played D in the previous round, play D.    In the final round
# (round 1000):   - Play D if your opponent has ever played D in any previous
# round.   - Otherwise (i.e., if your opponent has played C in every round so
# far), play D to exploit guaranteed cooperation.

class Cooperative_17(LLM_Strategy):
  n = 17
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._opponent_defected_ever = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          self._opponent_defected_ever = True
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# Play Cooperate (C) in the first round. In each subsequent round:  1. If your
# opponent played C in the previous round, play C.   2. If your opponent played
# D in the previous round, play D—but if both players have played D for the last
# two consecutive rounds, play C in the next round to attempt to restore
# cooperation.    Continue this pattern for all 1000 rounds.

class Neutral_17(LLM_Strategy):
  n = 17
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D



# Start by playing C (cooperate) in the first round. After that, follow these
# rules in order:  1. If your opponent played D in the immediately preceding
# round, play D in the current round.   2. If your opponent has played C in the
# immediately preceding round, play C in the current round.   3. However, if you
# are in the last 10 rounds (round 991 or later), always play D regardless of
# prior actions.

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C



# Start by cooperating in the first round.   In each subsequent round, follow
# these rules in order:  1. If fewer than 10 rounds remain, always defect.   2.
# If your opponent cooperated in the previous round, cooperate.   3. If your
# opponent defected in the previous round, defect—but if you have defected in
# response for two consecutive rounds already, cooperate once to test whether
# mutual cooperation can be restored.

class Cooperative_18(LLM_Strategy):
  n = 18
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._consecutive_retaliations = 0
          return axl.Action.C
  
      rounds_played = len(self.history)
      rounds_remaining = 1000 - rounds_played
  
      if rounds_remaining < 10:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          self._consecutive_retaliations = 0
          return axl.Action.C
  
      # Opponent defected last round
      if self._consecutive_retaliations >= 2:
          self._consecutive_retaliations = 0
          return axl.Action.C
  
      self._consecutive_retaliations += 1
      return axl.Action.D



# Start by playing C in the first round.    In each subsequent round:    1. If
# your opponent played C in the previous round, play C.   2. If your opponent
# played D in the previous round, play D—but if you have defected for three
# consecutive rounds and your opponent continues to defect, play C once to test
# for renewed cooperation.    Additionally, in the final 10 rounds (rounds
# 991–1000), always play D regardless of prior moves.

class Neutral_18(LLM_Strategy):
  n = 18
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._test_coop = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if self._test_coop:
          self._test_coop = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          if len(self.history) >= 3 and self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              self._test_coop = True
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.C



# Start by playing C in the first round. In each subsequent round:  1. If your
# opponent played C in the previous round, play C.   2. If your opponent played
# D in the previous round, play D for the next two rounds, then return to C
# regardless of what happened during those two rounds—unless your opponent
# defects again immediately after you return to C, in which case revert to D for
# two rounds again.  This creates a pattern of forgiving short-term defections
# but punishing them briefly, while always offering a chance to restore mutual
# cooperation.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_rounds = 0
          return axl.Action.C
  
      if self._punish_rounds > 0:
          self._punish_rounds -= 1
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          self._punish_rounds = 1
          return axl.Action.D
  
      return axl.Action.C



# Play Cooperate (C) in the first round.    In each subsequent round up to round
# 998:   1. If your opponent played C in the previous round, play C.   2. If
# your opponent played D in the previous round, play D—unless this is the first
# time they defected after a streak of cooperation; in that case, still play C
# (i.e., forgive a single isolated defection once).   3. If you have already
# forgiven one defection and your opponent defects again within the next five
# rounds, switch to always playing D for the rest of the game.    In rounds 999
# and 1000, always play D, regardless of prior history.

class Cooperative_19(LLM_Strategy):
  n = 19
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forgiven_once = False
          self._always_defect = False
          self._forgiveness_round = None
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 999:
          return axl.Action.D
  
      if self._always_defect:
          return axl.Action.D
  
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.C:
          return axl.Action.C
  
      # Opponent defected last round.
      if not self._forgiven_once:
          # First isolated defection after cooperation: forgive once.
          self._forgiven_once = True
          self._forgiveness_round = round_number
          return axl.Action.C
  
      # If opponent defects again within the next five rounds after forgiveness,
      # switch to always defect for the rest of the game.
      if self._forgiveness_round is not None and round_number - self._forgiveness_round <= 5:
          self._always_defect = True
          return axl.Action.D
  
      return axl.Action.D



# Start by playing C in the first round.    In each subsequent round:    1. If
# your opponent played C in the previous round, play C.   2. If your opponent
# played D in the previous round, play D—but only for one round.   3. After
# playing D in response to an opponent’s D, return to playing C in the following
# round, regardless of the opponent’s most recent move (i.e., offer cooperation
# again after a single retaliatory defection).

class Neutral_19(LLM_Strategy):
  n = 19
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._retaliated_last_round = False
          return axl.Action.C
  
      if getattr(self, "_retaliated_last_round", False):
          self._retaliated_last_round = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          self._retaliated_last_round = True
          return axl.Action.D
  
      return axl.Action.C



# Start by playing D in the first round. After that, follow these rules in
# order:  1. If your opponent played C in the previous round, play D (to exploit
# their cooperation).   2. If your opponent played D in the previous round, play
# D for the next three rounds (to maintain pressure).   3. After three
# consecutive rounds of mutual D, play C once to test if the opponent is willing
# to cooperate.   4. If the opponent responds to your test C with C, immediately
# return to D in the following round to exploit.   5. If the opponent responds
# to your test C with D, resume playing D for another three rounds before
# testing again.    Repeat this pattern for all 1000 rounds, always prioritizing
# exploitation of cooperation and retesting only after sustained mutual
# defection.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._test_pending = False
          self._test_result = None
          self._mutual_d_streak = 0
          self._post_test_d_streak = 0
          return axl.Action.D
  
      last_opp = opponent.history[-1]
      last_self = self.history[-1]
  
      if self._test_pending:
          self._test_pending = False
          self._test_result = last_opp
          if last_opp == axl.Action.C:
              self._post_test_d_streak = 0
              return axl.Action.D
          else:
              self._post_test_d_streak = 1
              return axl.Action.D
  
      if self._test_result == axl.Action.D:
          if last_self == axl.Action.D and last_opp == axl.Action.D:
              self._post_test_d_streak += 1
          else:
              self._post_test_d_streak = 1
  
          if self._post_test_d_streak >= 3:
              self._test_pending = True
              self._post_test_d_streak = 0
              return axl.Action.C
          return axl.Action.D
  
      if last_opp == axl.Action.C:
          self._mutual_d_streak = 0
          return axl.Action.D
  
      if last_opp == axl.Action.D:
          if last_self == axl.Action.D:
              self._mutual_d_streak += 1
          else:
              self._mutual_d_streak = 1
  
          if self._mutual_d_streak >= 3:
              self._test_pending = True
              self._mutual_d_streak = 0
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.D



# Start by playing C in the first round.    In every subsequent round:    1. If
# your opponent played C in the previous round, play C.   2. If your opponent
# played D in the previous round, play D—but if you have defected for two
# consecutive rounds in response to your opponent’s defections, play C in the
# next round regardless, to attempt to restore cooperation.

class Cooperative_20(LLM_Strategy):
  n = 20
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_streak = 0
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          self._defect_streak = 0
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          if self.history[-1] == axl.Action.D:
              self._defect_streak += 1
          else:
              self._defect_streak = 1
  
          if self._defect_streak >= 2:
              self._defect_streak = 0
              return axl.Action.C
  
          return axl.Action.D
  
      return axl.Action.C



# Start by playing C in the first round.    In every subsequent round:    1. If
# your opponent played C in the previous round, play C.   2. If your opponent
# played D in the previous round, play D—but if this is the first time they
# defected, give them one chance to return to cooperation: after your
# retaliatory D, play C in the following round regardless of their move, unless
# they defect again in the retaliatory round.    Additionally, in the final five
# rounds (rounds 996–1000), always play D, regardless of prior history.

class Neutral_20(LLM_Strategy):
  n = 20
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._retaliation_pending = False
          self._defection_seen = False
          return axl.Action.C
  
      if len(self.history) >= 995:
          return axl.Action.D
  
      if getattr(self, "_retaliation_pending", False):
          self._retaliation_pending = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          if not getattr(self, "_defection_seen", False):
              self._defection_seen = True
              self._retaliation_pending = True
          return axl.Action.D
  
      return axl.Action.C



# Start by playing C in the first round. After that, in each subsequent round:
# 1. If your opponent played C in the previous round, play C.   2. If your
# opponent played D in the previous round, play D.    Continue this pattern for
# all 1000 rounds.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]



# Start by cooperating in the first round. Then, for each subsequent round up to
# round 990:  1. If your opponent cooperated in the previous round, cooperate.
# 2. If your opponent defected in the previous round, defect.    From round 991
# onward (the last 10 rounds), always defect.

class Cooperative_21(LLM_Strategy):
  n = 21
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      return opponent.history[-1]



# Start by cooperating in the first round. Then, for each subsequent round up to
# round 990, follow these rules in order:  1. If your opponent cooperated in the
# previous round, cooperate.   2. If your opponent defected in the previous
# round, defect.  From round 991 onward (the last 10 rounds), always defect.
# Additionally, if a mutual defection occurs (both players defected in the
# previous round) at any point before round 991, cooperate in the next round
# with probability 10% (to test for possible reconciliation); otherwise, follow
# the standard rules above.

class Neutral_21(LLM_Strategy):
  n = 21
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if len(opponent.history) > 0 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return self._random.random_choice(0.1)
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Start by playing C in the first round.    After that, follow these rules in
# order:    1. If your opponent played D in the previous round, play D in the
# current round.   2. If your opponent played C in the previous round, play C in
# the current round.    In other words, mirror your opponent’s last move:
# cooperate if they cooperated, defect if they defected.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C



# Start by playing Cooperate (C) in the first round.    For rounds 2 through
# 990, follow this rule:   - If your opponent played Cooperate (C) in the
# previous round, play Cooperate (C).   - If your opponent played Defect (D) in
# the previous round, play Defect (D).    From round 991 onward (the last 10
# rounds), always play Defect (D), regardless of your opponent’s prior moves.

class Cooperative_22(LLM_Strategy):
  n = 22
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      return opponent.history[-1]



# Start by playing C in the first round.    For each subsequent round up to
# round 990:    1. If your opponent played C in the previous round, play C.   2.
# If your opponent played D in the previous round, play D—but if this leads to
# two consecutive rounds of mutual D (i.e., both players played D in the last
# two rounds), play C in the next round to attempt to restore cooperation.
# For rounds 991 through 1000:    3. Always play D, regardless of the opponent’s
# prior actions.

class Neutral_22(LLM_Strategy):
  n = 22
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._restore_coop_next = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if getattr(self, "_restore_coop_next", False):
          self._restore_coop_next = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Opponent played D last round
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D:
          self._restore_coop_next = True
          return axl.Action.D
  
      return axl.Action.D



# Start by playing C in the first round. After that, follow these rules in
# order:  1. If the opponent played D in the previous round, play D.   2. If the
# opponent played C in the previous round, play C.   3. However, in the last 10
# rounds (rounds 991–1000), always play D regardless of the opponent’s actions.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C



# Play Cooperate (C) in the first round.    For rounds 2 through 990:   - If
# your opponent played C in the previous round, play C.   - If your opponent
# played D in the previous round, play D.    For rounds 991 through 1000:   -
# Always play Defect (D), regardless of your opponent’s prior actions.

class Cooperative_23(LLM_Strategy):
  n = 23
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      return opponent.history[-1]



# Start by cooperating in the first round. Thereafter, follow these rules in
# order:  1. If your opponent cooperated in the previous round, cooperate in the
# current round.   2. If your opponent defected in the previous round, defect in
# the current round—but if you have defected for two consecutive rounds and your
# opponent cooperates in the current round, cooperate in the next round to
# restore mutual cooperation.   3. In the final three rounds (rounds 998, 999,
# and 1000), always defect regardless of the opponent’s prior actions.

class Neutral_23(LLM_Strategy):
  n = 23
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._restore_cooperation_next = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 998:
          return axl.Action.D
  
      if getattr(self, "_restore_cooperation_next", False):
          self._restore_cooperation_next = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Opponent defected last round
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D:
          if opponent.history[-1] == axl.Action.C:
              self._restore_cooperation_next = True
          return axl.Action.D
  
      return axl.Action.D



# Start by playing D in the first round. After that, follow these rules in
# order:  1. If your opponent played D in the previous round, play D.   2. If
# your opponent played C in the previous round and you played D, play D again
# (to exploit their cooperation).   3. If both you and your opponent played C in
# the previous round, continue playing C.   4. However, if you have played C for
# three consecutive rounds and your opponent has played C in all of them, keep
# playing C.   5. If at any point your opponent defects after a streak of mutual
# cooperation, immediately revert to D and do not cooperate again for the rest
# of the game.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._locked_defect = False
          self._mutual_coop_streak = 0
          return axl.Action.D
  
      if getattr(self, "_locked_defect", False):
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.D:
          if self._mutual_coop_streak > 0:
              self._locked_defect = True
          self._mutual_coop_streak = 0
          return axl.Action.D
  
      if last_opp == axl.Action.C and last_self == axl.Action.D:
          self._mutual_coop_streak = 0
          return axl.Action.D
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          self._mutual_coop_streak += 1
          if self._mutual_coop_streak >= 3:
              return axl.Action.C
          return axl.Action.C
  
      self._mutual_coop_streak = 0
      return axl.Action.D



# Play Cooperate (C) in the first round.    For rounds 2 through 990:   - If
# your opponent played C in the previous round, play C.   - If your opponent
# played D in the previous round, play D in the current round, but if they
# return to C in the following round, immediately respond with C.    For rounds
# 991 through 1000:   - Always play Defect (D), regardless of the opponent’s
# actions.

class Cooperative_24(LLM_Strategy):
  n = 24
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._respond_c_next = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if self._respond_c_next:
          self._respond_c_next = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      self._respond_c_next = True
      return axl.Action.D



# Start by cooperating in the first round. Then, for each subsequent round up to
# round 990, follow these rules in order:  1. If your opponent cooperated in the
# previous round, cooperate.   2. If your opponent defected in the previous
# round, defect.  From round 991 onward (the last 10 rounds), always defect
# regardless of the opponent’s prior moves.

class Neutral_24(LLM_Strategy):
  n = 24
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      return opponent.history[-1]



# Play D in the first round.   In each subsequent round up to round 999:    1.
# If your opponent played C in the previous round, play D (to exploit their
# cooperation).   2. If your opponent played D in the previous round, play D (to
# avoid being exploited).    However, if by round 900 your average payoff per
# round is below 2.5, continue always playing D for the rest of the game.
# Otherwise, from round 900 onward, switch to always playing C to encourage
# mutual cooperation—if the opponent reciprocates, this secures 3 points per
# round; if they defect, revert immediately to D for all remaining rounds.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._always_defect = False
          self._switch_to_cooperate = False
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number >= 900:
          if self._always_defect:
              return axl.Action.D
  
          if not self._switch_to_cooperate:
              if round_number == 900:
                  avg_payoff = self.score / len(self.history)
                  if avg_payoff < 2.5:
                      self._always_defect = True
                      return axl.Action.D
                  self._switch_to_cooperate = True
                  return axl.Action.C
              return axl.Action.D
  
          if opponent.history[-1] == axl.Action.D:
              self._always_defect = True
              return axl.Action.D
          return axl.Action.C
  
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    In each subsequent
# round:    - If your opponent played C in the immediately preceding round, play
# C.   - If your opponent played D in the immediately preceding round, play D.
# Apply this rule consistently for all remaining rounds up to and including
# round 1000.

class Cooperative_25(LLM_Strategy):
  n = 25
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      return opponent.history[-1]



# Start by cooperating in the first round. In each subsequent round, follow
# these rules in order:  1. If your opponent has cooperated in the previous
# round, cooperate.   2. If your opponent has defected in the previous round,
# defect—unless you have mutually defected for three consecutive rounds; in that
# case, cooperate once to attempt to restore mutual cooperation.

class Neutral_25(LLM_Strategy):
  n = 25
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mutual_defect_streak = 0
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          self._mutual_defect_streak += 1
      else:
          self._mutual_defect_streak = 0
  
      if self._mutual_defect_streak >= 3:
          self._mutual_defect_streak = 0
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D