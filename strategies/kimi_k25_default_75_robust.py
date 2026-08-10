import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



#  Defect in the first round. For each subsequent round, defect if your opponent
# defected in the previous round, and cooperate if your opponent cooperated in
# the previous round.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return axl.Action.D if opponent.history[-1] == axl.Action.D else axl.Action.C






# Begin by cooperating. Thereafter, match your opponent's previous action,
# cooperating when they cooperated and defecting when they defected.

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
      return opponent.history[-1]






#  Cooperate in the first round. For every subsequent round, cooperate if your
# opponent cooperated in the immediately preceding round, and defect if your
# opponent defected in the immediately preceding round.

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






#  Begin by defecting in the first round. For every subsequent round, if your
# opponent cooperated in the previous round, cooperate; if your opponent
# defected in the previous round, defect.

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
      return opponent.history[-1]






# **Strategy: Direct Reciprocity**  1. In the first round, cooperate. 2. In
# every subsequent round, if the opponent defected in the immediately preceding
# round, defect. 3. In every subsequent round, if the opponent cooperated in the
# immediately preceding round, cooperate.  Apply these rules consistently for
# all 1000 rounds.

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
      return opponent.history[-1]






#  Begin the first round by cooperating. For every subsequent round, replicate
# your opponent's action from the immediately preceding round: cooperate if they
# cooperated last round, and defect if they defected last round. Apply this rule
# consistently through all 1000 rounds.

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






#  Defect in the first round. Continue defecting unless the opponent cooperates
# for three consecutive rounds, at which point begin cooperating. If the
# opponent defects at any point after you have started cooperating, defect for
# all subsequent rounds. In the final ten rounds, defect regardless of the
# opponent’s actions.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._started_cooperating = False
          self._opponent_coop_streak = 0
          return axl.Action.D
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      if self._started_cooperating:
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.D
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          self._opponent_coop_streak += 1
      else:
          self._opponent_coop_streak = 0
  
      if self._opponent_coop_streak >= 3:
          self._started_cooperating = True
          return axl.Action.C
  
      return axl.Action.D






# In the first round, cooperate. In every subsequent round, replicate your
# opponent's previous move: cooperate if they cooperated, and defect if they
# defected.

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
      return opponent.history[-1]






# Cooperate in the first round. For rounds two through nine hundred and ninety-
# nine, cooperate if your opponent cooperated in the immediately preceding round
# and defect if your opponent defected in the immediately preceding round.
# Defect in the one thousandth round.

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
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1] if opponent.history else axl.Action.C






#  Defect in the first round. In every subsequent round, defect if the opponent
# defected in the immediately preceding round; cooperate only if the opponent
# cooperated in the immediately preceding round.

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
      return axl.Action.D if opponent.history[-1] == axl.Action.D else axl.Action.C






# Begin by cooperating. On every subsequent round, if your opponent cooperated
# in the immediately preceding round, cooperate; if your opponent defected in
# the immediately preceding round, defect. Apply this rule consistently through
# all 1000 rounds.

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
      return opponent.history[-1]






#  In the first round, cooperate. In every subsequent round, replicate your
# opponent's previous move: cooperate if they cooperated in the prior round, and
# defect if they defected in the prior round.

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






#  Defect in the first round. For every subsequent round, play whatever your
# opponent played in the immediately preceding round: defect if they defected,
# and cooperate if they cooperated.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return opponent.history[-1]






# Begin by playing C. In rounds 2 through 999, replicate your opponent's
# previous move: play C if they played C in the prior round, and play D if they
# played D in the prior round. In round 1000, play D.

class Cooperative_5(LLM_Strategy):
  n = 5
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
      elif len(self.history) < 999:
          return opponent.history[-1]
      else:
          return axl.Action.D






#  In the first round, cooperate. In every subsequent round, replicate your
# opponent's action from the immediately preceding round: cooperate if they
# cooperated, defect if they defected.

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






#  Defect in the first round. In every subsequent round, play the same action
# your opponent played in the previous round: cooperate if they cooperated,
# defect if they defected.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return opponent.history[-1]






# Cooperate in the first round. For each round from the second to the
# thousandth, cooperate if your opponent cooperated in the immediately preceding
# round, and defect if your opponent defected in the immediately preceding
# round.

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






#  Begin by cooperating in the first round. In every subsequent round, replicate
# whatever action your opponent performed in the immediately preceding round:
# cooperate if they cooperated, defect if they defected. Continue applying this
# rule of direct reciprocation consistently through all 1000 rounds.

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
      return opponent.history[-1]






#  Defect in the first round. If the opponent defected in the previous round,
# defect. If the opponent cooperated in the previous round, defect. Only
# cooperate if the opponent has cooperated for one hundred consecutive rounds
# while you defected, indicating they are unconditionally cooperative; in that
# case, switch to cooperation for all remaining rounds to secure mutual
# cooperation rather than continued exploitation.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._switch_to_cooperate = False
          self._cooperate_streak = 0
          return axl.Action.D
  
      if getattr(self, "_switch_to_cooperate", False):
          return axl.Action.C
  
      if opponent.history and opponent.history[-1] == axl.Action.C:
          self._cooperate_streak += 1
      else:
          self._cooperate_streak = 0
  
      if self._cooperate_streak >= 100 and self.history[-100:].count(axl.Action.D) == 100:
          self._switch_to_cooperate = True
          return axl.Action.C
  
      return axl.Action.D






# Cooperate in the first round. For each round from the second to the nine
# hundred and ninety-ninth, match your opponent's previous action: cooperate if
# they cooperated, defect if they defected. In the one thousandth round, defect
# unconditionally.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]






#  In the first round, cooperate. In every subsequent round, cooperate if your
# opponent cooperated in the previous round, and defect if your opponent
# defected in the previous round.

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
      return opponent.history[-1]






#  Defect in the first round. In every subsequent round, defect if your opponent
# defected in the previous round; if your opponent cooperated in the previous
# round, cooperate.

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
      return axl.Action.D if opponent.history[-1] == axl.Action.D else axl.Action.C






# Begin by cooperating in round one. For rounds two through 999, cooperate if
# the opponent cooperated in the immediately preceding round, and defect if the
# opponent defected in the immediately preceding round. In round 1000, defect
# regardless of the opponent's previous action.

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
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1]






#  Cooperate in the first round. For rounds two through nine hundred ninety-
# eight, replicate your opponent's immediately preceding move: cooperate if they
# cooperated, defect if they defected. Defect unconditionally in rounds nine
# hundred ninety-nine and one thousand.

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
  
      if round_number >= 999:
          return axl.Action.D
  
      return opponent.history[-1]






#  Defect in the first round. For each subsequent round from 2 to 999, apply
# these conditions in order: if your opponent cooperated while you defected in
# the previous round, defect; if both players defected in the previous round,
# cooperate; if both players cooperated in the previous round, defect; if you
# cooperated while your opponent defected in the previous round, defect for all
# remaining rounds. Defect in round 1000.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_forever = False
          return axl.Action.D
  
      if getattr(self, "_defect_forever", False):
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.C and last_self == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.D
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          self._defect_forever = True
          return axl.Action.D
  
      return axl.Action.D






# Begin by cooperating. In each subsequent round, replicate your opponent's
# action from the immediately preceding round: cooperate if they cooperated,
# defect if they defected.

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
      return opponent.history[-1]






#  Begin by cooperating in the first round. For every subsequent round from 2 to
# 1000, replicate your opponent's previous move: cooperate if they cooperated in
# the round immediately prior, and defect if they defected in the round
# immediately prior.

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
      return opponent.history[-1]






#  Defect in the first round. For every subsequent round, if the opponent
# defected in the previous round, defect; if the opponent cooperated in the
# previous round, cooperate.

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
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C






# Begin by cooperating. For every subsequent round, cooperate if your opponent
# cooperated in the immediately preceding round, and defect if your opponent
# defected in the immediately preceding round.

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






#  In round 1, cooperate. In rounds 2 through 999, play the same move your
# opponent played in the previous round. In round 1000, defect.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1]






#  Defect in the first round. In every subsequent round, if you and your
# opponent both defected in the immediately preceding round, cooperate;
# otherwise, defect.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D






# Begin by cooperating. For rounds two through nine hundred and ninety-nine,
# replicate your opponent's previous move: cooperate if they cooperated, defect
# if they defected. In the final round, defect.

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
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1]






#  In the first round, play C. In every following round, if your opponent played
# C in the previous round, play C; if your opponent played D in the previous
# round, play D.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






#  Defect in round one. If your opponent defected in the previous round, defect.
# If your opponent has cooperated for three consecutive rounds, switch to
# cooperation. Once cooperating, continue unless your opponent defects, in which
# case defect for all remaining rounds. Defect in round 1000 regardless of prior
# history.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._always_defect = False
          self._cooperating = False
          return axl.Action.D
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if self._always_defect:
          return axl.Action.D
  
      if opponent.history and opponent.history[-1] == axl.Action.D:
          self._always_defect = True
          self._cooperating = False
          return axl.Action.D
  
      if self._cooperating:
          return axl.Action.C
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]:
          self._cooperating = True
          return axl.Action.C
  
      return axl.Action.D






# Begin by cooperating in the first round. For every subsequent round, cooperate
# if your opponent cooperated in the immediately preceding round, and defect if
# your opponent defected in the immediately preceding round.

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
      return opponent.history[-1]






#  Play C in the first round. In every subsequent round, replicate your
# opponent's previous move: play C if they played C, and play D if they played
# D.

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
      return opponent.history[-1]






#  **Aggressive Exploitation Strategy**  Begin by defecting. For every
# subsequent round, if the opponent cooperated in the previous round, defect to
# exploit their cooperation. If the opponent defected in the previous round,
# defect to punish them. If the opponent has cooperated for ten consecutive
# rounds while you defected, cooperate once to test for mutual cooperation; if
# the opponent cooperates in response, defect on the next round and continue
# defecting thereafter. If the opponent defects at any point while you are
# cooperating, defect for all remaining rounds.

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.opponent_cooperations_in_a_row = 0
          self.triggered_forever_defect = False
          return axl.Action.D
  
      if self.triggered_forever_defect:
          return axl.Action.D
  
      # Update consecutive cooperations count
      if opponent.history[-1] == axl.Action.C:
          self.opponent_cooperations_in_a_row += 1
      else:
          self.opponent_cooperations_in_a_row = 0
  
      # If I cooperated last round and opponent defected, trigger forever defect
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self.triggered_forever_defect = True
          return axl.Action.D
  
      # Check for 10 consecutive opponent cooperations while I defected
      if self.opponent_cooperations_in_a_row >= 10:
          # Cooperate once to test mutual cooperation
          return axl.Action.C
  
      # Default: exploit/punish by defecting
      return axl.Action.D






# Begin by cooperating. For every round from the second through the nine hundred
# and ninety-ninth, cooperate if your opponent cooperated in the immediately
# preceding round, and defect if your opponent defected in the immediately
# preceding round. In the thousandth and final round, defect regardless of your
# opponent’s previous action.

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
  
      if len(self.history) == 999:
          return axl.Action.D
  
      return opponent.history[-1]






#  Begin by cooperating in the first round. For rounds two through nine hundred
# ninety-nine, cooperate if your opponent cooperated in the immediately
# preceding round and defect if your opponent defected in the immediately
# preceding round. In the one thousandth round, defect regardless of your
# opponent's prior action.

class Neutral_13(LLM_Strategy):
  n = 13
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






#  Begin by defecting. For every subsequent round, cooperate only if the
# opponent cooperated in the immediately preceding round; otherwise, defect.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D






# Begin by cooperating. For every subsequent round, replicate your opponent's
# action from the immediately preceding round: cooperate if they cooperated,
# defect if they defected.

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
      return opponent.history[-1]






#  Begin by playing C in the first round.   For every subsequent round, examine
# your opponent's move in the immediately preceding round. If they played C,
# play C. If they played D, play D.

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
      return opponent.history[-1]






#  Defect in the first round. Thereafter, if your opponent defected in the
# previous round, defect. If you defected in the previous round and your
# opponent cooperated, defect again to continue exploiting them. If both you and
# your opponent cooperated in the previous round, cooperate.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.C






# Cooperate in the first round. In every subsequent round, replicate your
# opponent's previous action: cooperate if they cooperated, and defect if they
# defected.

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
      return opponent.history[-1]






#  Begin by cooperating in the first round. For every subsequent round, if your
# opponent cooperated in the previous round, cooperate; if your opponent
# defected in the previous round, defect.

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
      return opponent.history[-1]






#  Play Defect in round one. For each round from 2 through 999, replicate your
# opponent's previous move: play Cooperate if they played Cooperate, and play
# Defect if they played Defect. Play Defect in round 1000 unconditionally.

class Aggressive_16(LLM_Strategy):
  n = 16
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






# In the first round, cooperate. In the thousandth round, defect. In all rounds
# between, cooperate if the opponent cooperated in the immediately preceding
# round; otherwise, defect.

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
  
      if len(self.history) == 999:
          return axl.Action.D
  
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D






#  Begin by playing Cooperate. In every subsequent round, replicate your
# opponent's action from the immediately preceding round: play Cooperate if they
# previously played Cooperate, and play Defect if they previously played Defect.

class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      else:
          return opponent.history[-1]






#  Defect in the first round. If the opponent defected in the previous round,
# defect. If the opponent cooperated in the previous round while you defected,
# defect to exploit their cooperation. Only cooperate if the opponent has
# cooperated for five consecutive rounds while you were defecting; at that
# point, switch to cooperation. If the opponent ever defects while you are
# cooperating, defect for the remainder of the game.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._cooperate_forever = False
          return axl.Action.D
  
      if getattr(self, "_cooperate_forever", False):
          return axl.Action.C
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._cooperate_forever = True
          return axl.Action.D
  
      if len(opponent.history) >= 5:
          last_five_opp = opponent.history[-5:]
          last_five_self = self.history[-5:]
          if all(move == axl.Action.C for move in last_five_opp) and all(move == axl.Action.D for move in last_five_self):
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C and self.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.D






# Begin by cooperating. In every subsequent round, if your opponent cooperated
# in the immediately preceding round, cooperate; if your opponent defected in
# the immediately preceding round, defect.

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
      return opponent.history[-1]






#  Begin by playing Cooperate. For every subsequent round, replicate your
# opponent's previous move: play Cooperate if they played Cooperate in the
# preceding round, and play Defect if they played Defect in the preceding round.

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
      return opponent.history[-1]






#  Defect in the first round. For rounds two through nine hundred and ninety-
# nine, play Defect if your opponent played Defect in the immediately preceding
# round; play Cooperate if your opponent played Cooperate in the immediately
# preceding round. Defect in the thousandth round.

class Aggressive_18(LLM_Strategy):
  n = 18
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






# In the first round, cooperate. In each subsequent round from two to 999,
# replicate the opponent's immediately preceding move: cooperate if they
# cooperated, defect if they defected. In round 1000, defect.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]






#  Cooperate in the first round. In each subsequent round, cooperate if your
# opponent cooperated in the immediately preceding round, and defect if your
# opponent defected in the immediately preceding round.

class Neutral_18(LLM_Strategy):
  n = 18
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]






#  Defect in the first round. In every subsequent round, replicate your
# opponent's previous move: cooperate if they cooperated, defect if they
# defected.

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
      return opponent.history[-1]






# Start by cooperating. Thereafter, in each round, do exactly what your opponent
# did in the previous round: cooperate if they cooperated, and defect if they
# defected.

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






#  In the first round, cooperate. For every subsequent round, replicate your
# opponent's action from the immediately preceding round: cooperate if they
# cooperated, defect if they defected.

class Neutral_19(LLM_Strategy):
  n = 19
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]






#  Defect in the first round. For every subsequent round, if the opponent
# defected in the previous round, defect; if the opponent cooperated in the
# previous round, cooperate.

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
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C






# Begin by cooperating in the first round. For every subsequent round, cooperate
# if your opponent cooperated in the immediately preceding round, and defect if
# your opponent defected in the immediately preceding round.

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
      return opponent.history[-1]






#  Cooperate in the first round. In every subsequent round, cooperate if your
# opponent cooperated in the immediately preceding round; defect if your
# opponent defected in the immediately preceding round.

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
      return opponent.history[-1]






#  Play Defect in the first round. For every subsequent round, apply the
# following conditions in order:  1. If your opponent played Defect in the
# previous round, play Defect. 2. If you played Defect in the previous round and
# your opponent played Cooperate in the previous round, play Defect. 3. If both
# you and your opponent played Cooperate in the previous round, play Cooperate.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D






# 1. Cooperate in the first round. 2. In any subsequent round, if your opponent
# cooperated in the previous round, cooperate. 3. In any subsequent round, if
# your opponent defected in the previous round, defect.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D






#  In the first round, cooperate. In every subsequent round, replicate your
# opponent's action from the immediately preceding round: cooperate if they
# cooperated previously, and defect if they defected previously.

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
      return opponent.history[-1]






#  Defect in the first round. If your opponent defects in response, defect for
# all remaining rounds to avoid being exploited. If your opponent cooperates in
# response, defect for all remaining rounds to exploit their compliance.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      return axl.Action.D






# In the first round, cooperate. In each subsequent round, cooperate if the
# opponent cooperated in the previous round; otherwise, defect.

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
      # In each subsequent round, cooperate if the opponent cooperated in the previous round; otherwise defect.
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D






#  Begin the first round by cooperating. In every subsequent round, replicate
# your opponent's action from the immediately preceding round: cooperate if they
# cooperated, and defect if they defected. Maintain this pattern consistently
# throughout all 1000 rounds.

class Neutral_22(LLM_Strategy):
  n = 22
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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D






# Begin by cooperating. In every subsequent round, if your opponent cooperated
# in the immediately preceding round, cooperate; if your opponent defected in
# the immediately preceding round, defect.

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
      return opponent.history[-1]






#  Cooperate in the first round. For rounds two through nine hundred and ninety-
# nine, replicate your opponent's move from the immediately preceding round:
# cooperate if they cooperated, defect if they defected. Defect in the
# thousandth round.

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
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1]






#  Defect in the first round. Thereafter, replicate your opponent previous move:
# cooperate if they cooperated, and defect if they defected.

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
      return opponent.history[-1]






# Begin by cooperating. For every subsequent round, mirror your opponent's
# action from the immediately preceding round: cooperate if they cooperated, and
# defect if they defected. Continue applying this rule for the entire duration
# of the 1000 rounds.

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
      return opponent.history[-1]






# On the first round, cooperate. On every subsequent round, cooperate if your
# opponent cooperated in the immediately preceding round, and defect if your
# opponent defected in the immediately preceding round.

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
      return opponent.history[-1]






# Begin by playing Defect. In every subsequent round, play whatever your
# opponent played in the previous round. However, if your opponent ever plays
# Defect immediately after you play Cooperate, play Defect for all remaining
# rounds.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_forever = False
          return axl.Action.D
  
      if self._defect_forever:
          return axl.Action.D
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.C:
              self._defect_forever = True
              return axl.Action.D
  
      return opponent.history[-1]






# Begin by cooperating in the first round. For every subsequent round, cooperate
# if your opponent cooperated in the previous round, and defect if your opponent
# defected in the previous round.

class Cooperative_25(LLM_Strategy):
  n = 25
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      """Cooperate on the first round, then copy opponent's previous move."""
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]






# Begin by cooperating in the first round. For every subsequent round, replicate
# your opponent's action from the immediately preceding round: cooperate if they
# cooperated, and defect if they defected.

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
      return opponent.history[-1]
