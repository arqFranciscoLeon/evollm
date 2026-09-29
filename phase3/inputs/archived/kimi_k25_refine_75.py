import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



#  Defect on the first round. If your opponent cooperated in the previous round
# while you defected, defect again to exploit their cooperation. If both you and
# your opponent defected in the previous round, defect for two more consecutive
# rounds, then cooperate to test for mutual cooperation. If you cooperated and
# your opponent defected in the previous round, defect for three consecutive
# rounds, then cooperate again. If both you and your opponent cooperated in the
# previous round, continue cooperating.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_streak = 0
          return axl.Action.D
  
      if self._defect_streak is None:
          self._defect_streak = 0
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if self._defect_streak > 0:
          self._defect_streak -= 1
          return axl.Action.D
  
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.D
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          self._defect_streak = 1
          return axl.Action.D
  
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          self._defect_streak = 2
          return axl.Action.D
  
      return axl.Action.C



# Begin by cooperating in the first round. For rounds two through 999, cooperate
# if your opponent cooperated in the immediately preceding round; defect if your
# opponent defected in the immediately preceding round while you cooperated;
# cooperate if both you and your opponent defected in the immediately preceding
# round. Defect unconditionally in round 1000.

class Cooperative_1(LLM_Strategy):
  n = 1
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.C:
          return axl.Action.C
      if last_opp == axl.Action.D and last_self == axl.Action.C:
          return axl.Action.D
      if last_opp == axl.Action.D and last_self == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C



#  Begin by cooperating in the first round. For every subsequent round from the
# second through the one thousandth, replicate your opponent's action from the
# immediately preceding round: cooperate if they cooperated, defect if they
# defected.

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
      return opponent.history[-1]



#  Play Defect on the first round. For every subsequent round from 2 to 999,
# apply the following conditions in order:  First, if in the previous round your
# opponent played Defect, play Defect.  Second, if in the previous round your
# opponent played Cooperate, play Cooperate.  For round 1000, play Defect.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Begin by cooperating.   For rounds 2 through 998, cooperate unless your
# opponent defected in both of the previous two rounds.   For rounds 999 and
# 1000, defect unconditionally.

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
  
      if round_number >= 999:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Cooperate in the first round. For each subsequent round through round 1000,
# replicate your opponent's action from the immediately preceding round:
# cooperate if they cooperated, defect if they defected.

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



#  Cooperate in the first round. For each round from two through 999, play the
# same move your opponent made in the previous round. Cooperate in the final
# round.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) >= 999:
          return axl.Action.C
  
      return opponent.history[-1]



# **Strategy: Forgiving Reciprocity with Endgame Transition**  1. In round 1,
# play C.  2. In rounds 2 through 990: If the opponent played D in both of the
# previous two rounds, play D; otherwise, play C.  3. In rounds 991 through 999:
# If the opponent played D in the previous round, play D; otherwise, play C.  4.
# In round 1000, play D.

class Cooperative_3(LLM_Strategy):
  n = 3
  attitude = Attitude.COOPERATIVE
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
  
      if 991 <= round_number <= 999:
          return axl.Action.D if opponent.history[-1] == axl.Action.D else axl.Action.C
  
      if 2 <= round_number <= 990:
          if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
          return axl.Action.C
  
      return axl.Action.C



#  In round one, cooperate. For every subsequent round through round one
# thousand, replicate your opponent's action from the immediately preceding
# round: cooperate if they cooperated, defect if they defected.

class Neutral_3(LLM_Strategy):
  n = 3
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]



#  Defect on rounds 1, 2, and 3. For rounds 4 through 997, cooperate only if
# your opponent cooperated in the three immediately preceding rounds; otherwise
# defect. Defect on rounds 998, 999, and 1000.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number <= 3:
          return axl.Action.D
  
      if round_number >= 998:
          return axl.Action.D
  
      if len(opponent.history) < 3:
          return axl.Action.D
  
      if opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]:
          return axl.Action.C
  
      return axl.Action.D



# Begin by cooperating. In round 2, cooperate if your opponent cooperated in
# round 1, otherwise defect. For rounds 3 through 998, cooperate unless your
# opponent defected in both of the previous two rounds. For rounds 999 and 1000,
# always defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number == 2:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      if 3 <= round_number <= 998:
          if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
          return axl.Action.C
  
      return axl.Action.D



#  Play D in round 1. For rounds 2 through 999: if both players played D in the
# previous round, play C; otherwise, play the same move your opponent played in
# the previous round. Play D in round 1000.

class Neutral_4(LLM_Strategy):
  n = 4
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]



#  Defect in round one. For rounds two through nine hundred ninety: if your
# opponent has ever defected while you cooperated in any previous round, defect;
# otherwise, play the same action your opponent played in the immediately
# preceding round. Defect in rounds nine hundred ninety-one through one
# thousand.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._opponent_defected_while_i_cooperated = False
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if self._opponent_defected_while_i_cooperated:
          return axl.Action.D
  
      for my_move, opp_move in zip(self.history, opponent.history):
          if my_move == axl.Action.C and opp_move == axl.Action.D:
              self._opponent_defected_while_i_cooperated = True
              return axl.Action.D
  
      return opponent.history[-1]



# Begin by cooperating in round 1. For each round from 2 through 999, replicate
# your opponent's action from the immediately preceding round: cooperate if they
# cooperated, defect if they defected. In round 1000, defect unconditionally
# regardless of your opponent's previous action.

class Cooperative_5(LLM_Strategy):
  n = 5
  attitude = Attitude.COOPERATIVE
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



#  In the first round, cooperate. In each subsequent round, play the same move
# your opponent played in the immediately preceding round.

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
      return opponent.history[-1]



#  Cooperate in round one. For each round from two through 999, defect if your
# opponent defected in the previous round and cooperate if your opponent
# cooperated in the previous round. Defect in round 1000 regardless of your
# opponent's action.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1]



# Cooperate in round 1. Defect in rounds 999 and 1000. In all other rounds,
# cooperate if the opponent cooperated in the immediately preceding round;
# otherwise, defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number in (999, 1000):
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



#  **Rounds 1 through 997**: Cooperate in the first round. For each subsequent
# round in this range, defect if your opponent defected in the immediately
# preceding round; otherwise cooperate. If you and your opponent both defected
# in the previous round, and this mutual defection has persisted for two
# consecutive rounds, cooperate in the next round to attempt restoration of
# cooperation before resuming the replication rule.  **Rounds 998 through
# 1000**: Defect unconditionally.

class Neutral_6(LLM_Strategy):
  n = 6
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
  
      if round_number >= 998:
          return axl.Action.D
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by cooperating in round one. For each round from 2 through 999,
# cooperate if the opponent cooperated in the immediately preceding round;
# otherwise, defect. Defect unconditionally in round 1000.

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
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1] if opponent.history else axl.Action.D



# 1. Cooperate in round 1. 2. For rounds 2 through 999, apply these conditions
# in order:    - If your opponent has defected in every previous round, defect.
# - If your opponent cooperated in the immediately preceding round, cooperate.
# - If both you and your opponent defected in the immediately preceding round,
# cooperate.    - In all other cases, defect. 3. Defect in round 1000.

class Cooperative_7(LLM_Strategy):
  n = 7
  attitude = Attitude.COOPERATIVE
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
  
      if opponent.history.defections == len(opponent.history):
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D



#  Begin by playing Cooperate. For rounds 2 through 999, replicate your
# opponent's previous move: play Cooperate if they played Cooperate, and play
# Defect if they played Defect. In round 1000, play Defect regardless of the
# opponent's previous action.

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
      if len(self.history) < 999:
          return opponent.history[-1]
      return axl.Action.D



#  Defect in the first round. For rounds two through 999, cooperate if the
# opponent cooperated in the immediately preceding round, and defect if the
# opponent defected in the immediately preceding round. Defect in the thousandth
# round.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1]



# Cooperate in the first two rounds. For every round from three through nine
# hundred ninety-nine, defect only if your opponent defected in both of the two
# immediately preceding rounds; otherwise cooperate. In round one thousand,
# defect regardless of previous actions.

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
  
      if round_number <= 2:
          return axl.Action.C
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Defect in the first round. For rounds 2 through 999, replicate your opponent's
# action from the immediately preceding round: cooperate if they cooperated,
# defect if they defected. Defect in round 1000 regardless of the opponent's
# prior actions.

class Neutral_8(LLM_Strategy):
  n = 8
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1]



#  Play D in the first round.  If you played C and the opponent played D in the
# previous round, play D.  If you played D and the opponent played C in the
# previous round, play D.  If both you and the opponent played D in the previous
# round, play D.  If both you and the opponent played C in the previous round,
# play C.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# 1. In round 1, cooperate. 2. In rounds 2 through 998: If your opponent
# cooperated in the immediately preceding round, cooperate; if your opponent
# defected in the immediately preceding round, defect, then cooperate in the
# subsequent round regardless of their action. 3. In rounds 999 and 1000,
# defect.

class Cooperative_9(LLM_Strategy):
  n = 9
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
  
      if len(opponent.history) == 0:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          if getattr(self, "_force_cooperate_next", None):
              self._force_cooperate_next = False
              return axl.Action.C
          self._force_cooperate_next = True
          return axl.Action.D
  
      if getattr(self, "_force_cooperate_next", None):
          self._force_cooperate_next = False
          return axl.Action.C
  
      return axl.Action.C



# Start by cooperating. For rounds 2 through 997, replicate your opponent’s
# immediately preceding action: cooperate if they cooperated, defect if they
# defected. Defect unconditionally in rounds 998, 999, and 1000 regardless of
# your opponent’s behavior.

class Neutral_9(LLM_Strategy):
  n = 9
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
  
      return opponent.history[-1]



#  Play Cooperate in the first round. For rounds 2 through 999, play Cooperate
# only if the opponent has played Cooperate in every previous round; if the
# opponent has ever played Defect, play Defect for all subsequent rounds. Play
# Defect in round 1000 regardless of the interaction history.

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if axl.Action.D in opponent.history:
          return axl.Action.D
  
      return axl.Action.C



# Begin by cooperating in round one. For each subsequent round through round one
# thousand, cooperate if your opponent cooperated in the immediately preceding
# round, and defect if your opponent defected in the immediately preceding
# round.

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
      return opponent.history[-1]



# - Cooperate in the first round.   - For rounds two through nine hundred
# ninety-seven, cooperate if your opponent cooperated in the previous round. If
# your opponent defected in the previous round but cooperated in the round
# before that, treat this as an isolated lapse and cooperate; however, if your
# opponent defects twice in succession, defect until they cooperate twice in
# succession, at which point resume cooperation.   - Defect unconditionally in
# rounds nine hundred ninety-eight, nine hundred ninety-nine, and one thousand.

class Neutral_10(LLM_Strategy):
  n = 10
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._lapse_mode = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 998:
          return axl.Action.D
  
      if self._lapse_mode:
          if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
              self._lapse_mode = False
              return axl.Action.C
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._lapse_mode = True
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D and len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C



# Cooperate in the first round. For each subsequent round from two through nine
# hundred and ninety-nine, play the same move your opponent played in the
# previous round; if mutual defection has occurred for three consecutive rounds,
# cooperate once to attempt restoration of cooperation. Cooperate in round one
# thousand.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._restore_coop = 0
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.C
  
      if len(self.history) >= 3:
          last_three_self = self.history[-3:]
          last_three_opp = opponent.history[-3:]
          if (
              last_three_self.count(axl.Action.D) == 3
              and last_three_opp.count(axl.Action.D) == 3
          ):
              return axl.Action.C
  
      return opponent.history[-1]



# Begin by cooperating in the first round. For each subsequent round, apply the
# following conditions in order:  1. If both you and your opponent defected in
# the immediately preceding round, cooperate. 2. If your opponent defected in
# the immediately preceding round, defect. 3. Otherwise, cooperate.

class Cooperative_11(LLM_Strategy):
  n = 11
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by cooperating in the first round. For each subsequent round, replicate
# your opponent's action from the preceding round, except that if the previous
# round resulted in mutual defection, cooperate instead. Continue this pattern
# through all one thousand rounds.

class Neutral_11(LLM_Strategy):
  n = 11
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]



#  **Strategy: Aggressive Retaliator**  Defect in round one.  If permanent
# defection has been triggered, defect.  If permanent defection has not been
# triggered, play the same move your opponent made in the previous round.
# Permanent defection triggers immediately after any round where you played C
# and your opponent played D, and continues for all remaining rounds.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._permanent_defection = False
          return axl.Action.D
  
      if getattr(self, "_permanent_defection", False):
          return axl.Action.D
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._permanent_defection = True
          return axl.Action.D
  
      return opponent.history[-1]



#  Begin by cooperating in round one. For rounds two through nine hundred
# ninety-nine, cooperate if the opponent cooperated in the immediately preceding
# round and defect if the opponent defected in the immediately preceding round.
# In round one thousand, defect unconditionally regardless of the opponent's
# previous action.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1] if opponent.history else axl.Action.C



# In the first round, cooperate. For every subsequent round through round one
# thousand, replicate your opponent's immediately preceding action, with the
# following exception: following any round of mutual defection, cooperate in the
# next round regardless of the opponent's prior move.

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
  
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]



# Defect in the first round and defect again in the second round. If your
# opponent cooperated in the second round, defect in every subsequent round
# through round nine hundred and ninety-nine. If your opponent defected in the
# second round, cooperate in the third round, and for every round thereafter
# through round nine hundred and ninety-nine, replicate your opponent's move
# from the immediately preceding round. Defect in the thousandth round.

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 2:
          return axl.Action.D
  
      if round_number == 3:
          if opponent.history[1] == axl.Action.C:
              return axl.Action.D
          return axl.Action.C
  
      if round_number == 1000:
          return axl.Action.D
  
      if opponent.history[1] == axl.Action.C:
          return axl.Action.D
  
      return opponent.history[-1]



#  Cooperate in the first round. For each subsequent round, cooperate if your
# opponent cooperated in the immediately preceding round, and defect if your
# opponent defected in the immediately preceding round.

class Cooperative_13(LLM_Strategy):
  n = 13
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]



#  In round 1, defect. In rounds 2 through 999, replicate your opponent's action
# from the immediately preceding round: cooperate if they cooperated, defect if
# they defected. In round 1000, defect.

class Neutral_13(LLM_Strategy):
  n = 13
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1]



#  Begin by cooperating. Continue cooperating in each subsequent round as long
# as the opponent has never defected in any previous round; if the opponent
# defects at any point, defect in all remaining rounds without exception.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if axl.Action.D in opponent.history:
          return axl.Action.D
  
      return axl.Action.C



# Begin by cooperating in the first round. In the second round, cooperate if
# your opponent cooperated in the first round, otherwise defect. For every round
# from the third through the one thousandth, cooperate unless your opponent
# defected in both of the two immediately preceding rounds, in which case
# defect.

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
  
      if len(self.history) == 1:
          return axl.Action.C if opponent.history[0] == axl.Action.C else axl.Action.D
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  In the first round, cooperate. For every round thereafter, cooperate unless
# your opponent defected in both of the two immediately preceding rounds; if
# they did, defect.

class Neutral_14(LLM_Strategy):
  n = 14
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Cooperate in the first round. For each round from the second through the nine
# hundred and ninety-eighth, replicate your opponent's previous move: cooperate
# if they cooperated, defect if they defected. Defect unconditionally in rounds
# nine hundred and ninety-nine and one thousand.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
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
  
      return opponent.history[-1]



# Begin by cooperating in the first round. For rounds two through nine hundred
# ninety-nine, replicate your opponent's action from the immediately preceding
# round; however, if both you and your opponent defected in the two immediately
# preceding rounds, cooperate in the current round to break the cycle of
# retaliation. In round one thousand, defect unconditionally regardless of your
# opponent's previous action.

class Cooperative_15(LLM_Strategy):
  n = 15
  attitude = Attitude.COOPERATIVE
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
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return opponent.history[-1]



# Cooperate in the first round. For rounds 2 through 998, replicate your
# opponent's previous move, except that if both you and your opponent defected
# in the immediately preceding round, cooperate instead. In rounds 999 and 1000,
# defect unconditionally.

class Neutral_15(LLM_Strategy):
  n = 15
  attitude = Attitude.NEUTRAL
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
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]



#  Cooperate in the first round. For rounds 2 through 999, defect if your
# opponent defected in the previous round; otherwise cooperate. Defect
# unconditionally in round 1000.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      if len(self.history) >= 999:
          return axl.Action.D
      return axl.Action.D if opponent.history[-1] == axl.Action.D else axl.Action.C



#  Cooperate in round 1. For each subsequent round from 2 through 1000,
# cooperate if your opponent cooperated in the immediately preceding round;
# otherwise, defect.

class Cooperative_16(LLM_Strategy):
  n = 16
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



#  In the first round, defect. For rounds 2 through 999, replicate your
# opponent's previous action: cooperate if they cooperated, defect if they
# defected. In round 1000, defect regardless of the opponent's prior action.

class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1]



#  Defect in the first round. For each subsequent round from 2 through 999,
# replicate your opponent's action from the immediately preceding round: play
# Cooperation if they played Cooperation, and play Defection if they played
# Defection. Defect unconditionally in round 1000 regardless of the opponent's
# prior action.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1]



# **Strategy: Reciprocal Cooperation**  1.  Cooperate in the first round. 2.  If
# the opponent cooperated in the previous round, cooperate. 3.  If the opponent
# defected in the previous round, defect.

class Cooperative_17(LLM_Strategy):
  n = 17
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1] if opponent.history else axl.Action.C



#  Begin by defecting. For rounds 2 through 998, cooperate unless your opponent
# defected in both of the previous two rounds, in which case defect. If your
# opponent has cooperated in every round through round 20, defect in round 21
# and continue defecting for the remainder of the game if they cooperate in
# response. In rounds 999 and 1000, always defect.

class Neutral_17(LLM_Strategy):
  n = 17
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._always_defect_from_21 = False
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number >= 999:
          return axl.Action.D
  
      if getattr(self, "_always_defect_from_21", False):
          return axl.Action.D
  
      if round_number == 21:
          if len(opponent.history) >= 20 and all(move == axl.Action.C for move in opponent.history[:20]):
              self._always_defect_from_21 = True
              return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Cooperate in the first round. Thereafter, cooperate if your opponent
# cooperated in the previous round; defect if your opponent defected in the
# previous round. Continue this conditional response through round 1000.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



#  Begin by cooperating in the first round. For rounds 2 through 999, replicate
# your opponent's action from the immediately preceding round: cooperate if they
# cooperated, and defect if they defected. In round 1000, defect regardless of
# the opponent's prior action.

class Cooperative_18(LLM_Strategy):
  n = 18
  attitude = Attitude.COOPERATIVE
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



#  Begin by defecting. For rounds 2 through 999: if your opponent defected in
# the previous round while you cooperated, defect; if you both defected in the
# previous round, cooperate; if your opponent cooperated in the previous round
# while you defected and your opponent has never defected in any earlier round,
# defect; if your opponent cooperated in the previous round, cooperate. In round
# 1000, defect.

class Neutral_18(LLM_Strategy):
  n = 18
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._opponent_has_defected_ever = False
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if axl.Action.D in opponent.history:
          self._opponent_has_defected_ever = True
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if opp_last == axl.Action.D and my_last == axl.Action.C:
          return axl.Action.D
      if opp_last == axl.Action.D and my_last == axl.Action.D:
          return axl.Action.C
      if opp_last == axl.Action.C and my_last == axl.Action.D and not self._opponent_has_defected_ever:
          return axl.Action.D
      if opp_last == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C



# In round 1000, defect. In round 1, defect. For rounds 2 through 999: if the
# previous round was mutual cooperation, cooperate; if the previous round was
# mutual defection, defect; if the previous round involved different moves,
# defect.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(self.history) == 0:
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Cooperate in the first round. For every subsequent round, cooperate if your
# opponent cooperated in the immediately preceding round, and defect if your
# opponent defected in the immediately preceding round. Apply this rule
# consistently through all one thousand rounds without exception.

class Cooperative_19(LLM_Strategy):
  n = 19
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]



# Defect in the first round. For rounds 2 through 999, replicate your opponent's
# move from the immediately preceding round: cooperate if they cooperated,
# defect if they defected. Defect unconditionally in round 1000.

class Neutral_19(LLM_Strategy):
  n = 19
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1]



#  Defect in the first round. For rounds two through nine hundred ninety-nine,
# if you defected and your opponent cooperated in the previous round, defect; if
# you defected and your opponent defected in the previous round, cooperate; if
# you cooperated and your opponent cooperated in the previous round, defect; if
# you cooperated and your opponent defected in the previous round, defect.
# Defect in the one thousandth round.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.D
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.D



# 1. Play Defect in round 1000. 2. Play Cooperate in round 1. 3. If your
# opponent played Defect in the previous round, play Defect. 4. Otherwise, play
# Cooperate.

class Cooperative_20(LLM_Strategy):
  n = 20
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      if len(self.history) >= 999:
          return axl.Action.D
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# Begin by cooperating. For each round from 2 through 999: replicate your
# opponent's previous action; however, if both players defected in the
# immediately preceding round, cooperate instead to test for restoration of
# mutual cooperation. In round 1000, defect regardless of the opponent's prior
# action or the history of play.

class Neutral_20(LLM_Strategy):
  n = 20
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
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]



#  • Cooperate in the first round.  • If the opponent has defected in any
# previous round, defect.  • If the current round is the nine hundred and
# ninety-ninth or one thousandth, defect.  • Otherwise, cooperate.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if axl.Action.D in opponent.history:
          return axl.Action.D
  
      return axl.Action.C



# Cooperate in round 1. For rounds 2 through 999, cooperate only if your
# opponent has cooperated in every previous round; otherwise defect. Defect in
# round 1000.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if opponent.history.defections > 0:
          return axl.Action.D
  
      return axl.Action.C



#  Defect in round 1. For rounds 2 through 999, replicate your opponent's action
# from the immediately preceding round. Defect in round 1000.

class Neutral_21(LLM_Strategy):
  n = 21
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1]



# Play Defect in round one.  If you played Defect and your opponent played
# Cooperate in the previous round, play Defect to maximise exploitation.  If you
# played Defect and your opponent played Defect in the previous round, play
# Defect; do not unilaterally cooperate following mutual defection unless your
# opponent has cooperated in at least two distinct prior rounds.  If you played
# Cooperate and your opponent played Defect in the previous round, play Defect
# for exactly one round, then play Cooperate to attempt restoration of mutual
# cooperation.  If you and your opponent both played Cooperate in the previous
# round, play Cooperate.  In round 1000, play Defect.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._restore_after_defection = False
          return axl.Action.D
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if getattr(self, "_restore_after_defection", False):
          self._restore_after_defection = False
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.D
  
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          if opponent.history.cooperations >= 2:
              return axl.Action.C
          return axl.Action.D
  
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          self._restore_after_defection = True
          return axl.Action.D
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



#  Cooperate in round 1. For rounds 2 through 998: if mutual defection occurred
# in the immediately preceding round and mutual cooperation had occurred in any
# prior round, cooperate; otherwise, cooperate if the opponent cooperated in the
# immediately preceding round and defect if the opponent defected in the
# immediately preceding round. Defect in rounds 999 and 1000.

class Cooperative_22(LLM_Strategy):
  n = 22
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._seen_mutual_cooperation = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 999:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and self._seen_mutual_cooperation:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          self._seen_mutual_cooperation = True
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



#  Defect in the first round. For rounds 2 through 998, cooperate. Defect in
# rounds 999 and 1000.

class Neutral_22(LLM_Strategy):
  n = 22
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      if round_number == 1:
          return axl.Action.D
      if 2 <= round_number <= 998:
          return axl.Action.C
      return axl.Action.D



#  Defect in the first round. If the opponent defected in the immediately
# preceding round, defect. If the opponent has cooperated for two consecutive
# rounds, cooperate. If the opponent cooperated in the immediately preceding
# round, defect.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.D



# First, cooperate in round 1. Second, for each round from 2 to 999 inclusive,
# cooperate if the opponent cooperated in the immediately preceding round,
# otherwise defect. Third, defect in round 1000.

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
      if len(self.history) >= 999:
          return axl.Action.D
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# Implement a **Tit-for-Tat** protocol governed by three ordered conditions:
# **First**, open with cooperation by playing **C** in round one.  **Second**,
# for every subsequent round (2 through 1000), replicate your opponent’s
# immediately preceding action: play **C** if they played **C** last round, and
# play **D** if they played **D** last round.  **Third**, maintain this exact
# mirroring regardless of round number; if the opponent switches from **D** to
# **C**, respond with **C** in the next round.  This approach secures mutual
# cooperation payoffs against collaborative opponents and limits exposure to
# exploitation through immediate retaliation, though it cannot outperform an
# opponent who always defects.

class Neutral_23(LLM_Strategy):
  n = 23
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]



#  Defect in the first round. In every subsequent round, cooperate if the
# opponent cooperated in the immediately preceding round; otherwise, defect.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



#  Begin by cooperating in the first round. For rounds two through 999,
# cooperate whenever your opponent cooperated in the immediately preceding
# round, and defect whenever your opponent defected in the immediately preceding
# round. In the thousandth round, defect unconditionally.

class Cooperative_24(LLM_Strategy):
  n = 24
  attitude = Attitude.COOPERATIVE
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



#  Cooperate in the first round. For rounds 2 through 999: cooperate if the
# opponent cooperated in the previous round; if the opponent defected in the
# previous round, defect unless the opponent cooperated in the round immediately
# before that, in which case cooperate. If the opponent defects for three
# consecutive rounds at any point, defect for all remaining rounds. In round
# 1000, defect unconditionally.

class Neutral_24(LLM_Strategy):
  n = 24
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._three_consecutive_defections = False
          return axl.Action.C
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          self._three_consecutive_defections = True
  
      if self._three_consecutive_defections:
          return axl.Action.D
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      last_opp = opponent.history[-1]
      if last_opp == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Defect in rounds one and two. If the opponent cooperated in both rounds,
# cooperate from round three onward as long as they continue cooperating; if
# they defect at any point, defect for the remainder of the game. If the
# opponent defected in exactly one of the first two rounds, defect until they
# cooperate for two consecutive rounds, then resume cooperation and continue as
# long as they cooperate; if they defect after cooperation resumes, defect for
# the remainder. If the opponent defected in both of the first two rounds,
# defect for all remaining rounds. Always defect in round 1000 regardless of
# prior history.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._state = "initial_defect"
          self._resume_pending = False
          self._consecutive_opponent_cooperations = 0
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      # Always defect in round 1000.
      if round_number == 1000:
          return axl.Action.D
  
      opp_last = opponent.history[-1]
  
      # Update state based on previous round outcome.
      if self._state == "initial_defect":
          if len(opponent.history) >= 2:
              first_two = opponent.history[:2]
              defections_first_two = first_two.count(axl.Action.D)
  
              if defections_first_two == 0:
                  self._state = "cooperate_if_cooperating"
              elif defections_first_two == 1:
                  self._state = "wait_for_two_cooperations"
                  self._consecutive_opponent_cooperations = 0
              else:
                  self._state = "defect_forever"
  
      if self._state == "cooperate_if_cooperating":
          if opp_last == axl.Action.D:
              self._state = "defect_forever"
          else:
              return axl.Action.C
  
      elif self._state == "wait_for_two_cooperations":
          if opp_last == axl.Action.C:
              self._consecutive_opponent_cooperations += 1
              if self._consecutive_opponent_cooperations >= 2:
                  self._state = "cooperate_if_cooperating"
                  return axl.Action.C
          else:
              self._consecutive_opponent_cooperations = 0
          return axl.Action.D
  
      return axl.Action.D



#  Cooperate in round one. For rounds two through nine hundred ninety: defect
# only if the opponent defected in both of the two immediately preceding rounds;
# otherwise cooperate. For rounds nine hundred ninety-one through one thousand:
# defect unconditionally.

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
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Start by cooperating. For rounds 2 through 999, cooperate if your opponent
# cooperated in the immediately preceding round, and defect if your opponent
# defected in the immediately preceding round. In round 1000, defect regardless
# of your opponent's previous action.

class Neutral_25(LLM_Strategy):
  n = 25
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