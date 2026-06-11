import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# Defect in the first round. In each subsequent round from two through nine
# hundred ninety-nine, mirror your opponent’s previous action: cooperate if they
# cooperated, defect if they defected. In the final round, always defect
# regardless of the opponent’s prior action.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1]



# For the first two rounds, cooperate.  For all subsequent rounds, defect only
# if your opponent defected in both of the previous two rounds; otherwise,
# cooperate.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# Begin by cooperating. For each subsequent round, cooperate unless your
# opponent defected in both of the previous two rounds, in which case defect.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by playing Defect. Continue playing Defect until your opponent has
# played Cooperate for two consecutive rounds; once this occurs, play Cooperate.
# If at any point your opponent plays Defect, immediately resume playing Defect
# and continue until they again play Cooperate for two consecutive rounds.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._waiting_for_two_cooperations = True
          self._coop_streak = 0
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          self._waiting_for_two_cooperations = True
          self._coop_streak = 0
          return axl.Action.D
  
      if self._waiting_for_two_cooperations:
          if opponent.history[-1] == axl.Action.C:
              self._coop_streak += 1
          else:
              self._coop_streak = 0
  
          if self._coop_streak >= 2:
              self._waiting_for_two_cooperations = False
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.C



# Cooperate in the first round. Thereafter, cooperate if your opponent
# cooperated in the previous round. If your opponent defected in the previous
# round while you cooperated, defect. If you both defected in the previous
# round, cooperate.

class Cooperative_2(LLM_Strategy):
  n = 2
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
  
      if last_opp == axl.Action.C:
          return axl.Action.C
      if last_opp == axl.Action.D and last_self == axl.Action.C:
          return axl.Action.D
      if last_opp == axl.Action.D and last_self == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C



#  Begin by cooperating. If the opponent defected in both of the previous two
# rounds, defect. Otherwise, cooperate.

class Neutral_2(LLM_Strategy):
  n = 2
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by defecting. For each subsequent round, defect unless the opponent
# cooperated in the previous two consecutive rounds, in which case cooperate. If
# you cooperate and the opponent defects in that same round, defect for the
# following five rounds regardless of their actions, then resume checking for
# two consecutive opponent cooperations.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_rounds = 0
          return axl.Action.D
  
      if self._punish_rounds > 0:
          self._punish_rounds -= 1
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          action = axl.Action.C
      else:
          action = axl.Action.D
  
      if action == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._punish_rounds = 5
          return axl.Action.D
  
      return action



# Begin by cooperating in the first round. For each subsequent round, apply the
# following conditions in the order listed:  1. If the current round is the
# 1000th and final round, defect. 2. If the opponent defected in the immediately
# preceding round and also in the round before that (two consecutive
# defections), defect. 3. In all other situations, cooperate.

class Cooperative_3(LLM_Strategy):
  n = 3
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      if len(self.history) == 999:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by cooperating in the first two rounds. For rounds three through nine
# hundred and ninety-nine, cooperate unless the opponent defected in both of the
# two immediately preceding rounds, in which case defect. In the one thousandth
# round, defect regardless of the opponent’s prior actions.

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
      if len(self.history) == 1:
          return axl.Action.C
      if len(self.history) == 999:
          return axl.Action.D
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



#  Defect in the first round. For rounds two through nine hundred ninety, defect
# if you and your opponent played the same action in the previous round;
# cooperate if you played different actions. For rounds nine hundred ninety-one
# through one thousand, always defect.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == last_opp:
          return axl.Action.D
      return axl.Action.C



# Begin by cooperating. In each subsequent round, defect only if the opponent
# defected in both of the previous two rounds; otherwise, cooperate.

class Cooperative_4(LLM_Strategy):
  n = 4
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(opponent.history) < 2:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by cooperating. In the second round, cooperate if the opponent
# cooperated in the first round, otherwise defect. For rounds three through nine
# hundred ninety-eight, cooperate unless the opponent defected in both of the
# previous two rounds. In the final two rounds, always defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number == 2:
          return axl.Action.C if opponent.history[0] == axl.Action.C else axl.Action.D
  
      if round_number >= 999:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Defect on the first round. Continue defecting until your opponent has
# cooperated for two consecutive rounds, then cooperate. While cooperating, if
# you observe a defection, defect for the next three rounds. After these three
# rounds, resume cooperation only if your opponent cooperated in the immediately
# preceding round; otherwise continue defecting. For the final ten rounds,
# always defect.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_count = 0
          self._post_defect_check = False
          return axl.Action.D
  
      rounds_left = 1000 - len(self.history)
      if rounds_left <= 10:
          return axl.Action.D
  
      if self._defect_count > 0:
          self._defect_count -= 1
          if self._defect_count == 0:
              self._post_defect_check = True
          return axl.Action.D
  
      if self._post_defect_check:
          self._post_defect_check = False
          if opponent.history and opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      if self.history and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._defect_count = 2
          return axl.Action.D
  
      return axl.Action.D



# Cooperate in the first two rounds. For every subsequent round, defect only if
# your opponent defected in both of the previous two rounds; otherwise,
# cooperate.

class Cooperative_5(LLM_Strategy):
  n = 5
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Play Cooperate in the first two rounds. For every round thereafter, play
# Defect only if your opponent played Defect in both of the previous two rounds;
# otherwise play Cooperate.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



#  Defect in round one. In each subsequent round, cooperate only if your
# opponent cooperated in both of the previous two rounds; otherwise defect. If
# you ever cooperate and your opponent defects, defect for the next three
# rounds, then resume the main rule.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_remaining = 0
          return axl.Action.D
  
      if getattr(self, "_punish_remaining", None) is None:
          self._punish_remaining = 0
  
      if self._punish_remaining > 0:
          self._punish_remaining -= 1
          return axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._punish_remaining = 3
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Begin by cooperating. For every subsequent round, cooperate unless your
# opponent defected in both of the previous two rounds; if they defected twice
# consecutively, defect.

class Cooperative_6(LLM_Strategy):
  n = 6
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Cooperate in the first round. For every subsequent round, if your opponent
# cooperated in the previous round, cooperate. If your opponent defected in the
# previous round, defect once, then return to cooperation on the following round
# regardless of their action.

class Neutral_6(LLM_Strategy):
  n = 6
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_once = False
          return axl.Action.C
  
      if self._defect_once:
          self._defect_once = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          self._defect_once = True
          return axl.Action.D
  
      return axl.Action.C



#  Begin by playing Defect. For every subsequent round, select your action based
# on the payoff you received in the previous round:  If you received 5 points,
# play Defect. If you received 3 points, play Cooperate. If you received 0
# points, play Defect. If you received 1 point, play Cooperate.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_score = self.score - sum(self.total_scores(self.history[-1:], opponent.history[-1:]))
      # The above is not reliable for a single-round payoff under noise, so infer from the
      # previous round's realized outcome using the last actions.
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          last_score = 3
      elif my_last == axl.Action.C and opp_last == axl.Action.D:
          last_score = 0
      elif my_last == axl.Action.D and opp_last == axl.Action.C:
          last_score = 5
      else:
          last_score = 1
  
      if last_score == 5:
          return axl.Action.D
      if last_score == 3:
          return axl.Action.C
      if last_score == 0:
          return axl.Action.D
      if last_score == 1:
          return axl.Action.C
  
      return axl.Action.D



# Cooperate in the first round. In every subsequent round, cooperate unless your
# opponent defected in both of the previous two rounds; if they did, defect.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by cooperating. In each subsequent round, defect only if the opponent
# defected in both of the two immediately preceding rounds; otherwise,
# cooperate.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by defecting. Continue defecting unless the opponent cooperates for
# three consecutive rounds, at which point switch to cooperation. While
# cooperating, maintain cooperation until the opponent defects twice in
# succession, then punish by defecting for five consecutive rounds before
# checking again for three consecutive cooperations. In the final twenty rounds,
# defect unconditionally regardless of the opponent's behavior.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mode = "defect"
          self._punish_remaining = 0
          return axl.Action.D
  
      rounds_left = 1000 - len(self.history)
      if rounds_left <= 20:
          return axl.Action.D
  
      if self._mode == "punish":
          if self._punish_remaining > 0:
              self._punish_remaining -= 1
              return axl.Action.D
          self._mode = "defect"
  
      if self._mode == "cooperate":
          if len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
              self._mode = "punish"
              self._punish_remaining = 4
              return axl.Action.D
          return axl.Action.C
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]:
          self._mode = "cooperate"
          return axl.Action.C
  
      return axl.Action.D



# Begin by cooperating in the first two rounds. For every subsequent round
# through round 1000, cooperate unless the opponent defected in both of the two
# immediately preceding rounds; if they defected in both of those rounds,
# defect.

class Cooperative_8(LLM_Strategy):
  n = 8
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._round_count = 1
          return axl.Action.C
  
      if len(self.history) < 2:
          self._round_count = len(self.history) + 1
          return axl.Action.C
  
      self._round_count = len(self.history) + 1
  
      if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
      return axl.Action.C



#  Begin by cooperating in round one. For each subsequent round, apply the
# following conditions in order:  1. If the round number is nine hundred ninety-
# one or higher, defect. 2. If the opponent defected in the immediately
# preceding round and also in the round before that, defect. 3. In all other
# situations, cooperate.

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
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C



#  Begin by defecting. For every subsequent round, apply the following rules in
# order:  1. If the opponent cooperated in the previous round, defect. 2. If you
# defected and the opponent defected in the previous round, cooperate. 3. If you
# cooperated and the opponent defected in the previous round, defect.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.C:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.D



# Begin by cooperating. Thereafter, cooperate unless your opponent has defected
# in both of the previous two rounds. When you defect under this condition,
# resume cooperating immediately as soon as your opponent cooperates again.

class Cooperative_9(LLM_Strategy):
  n = 9
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defecting = False
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._defecting = True
      elif len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          self._defecting = False
  
      return axl.Action.D if self._defecting else axl.Action.C



#  Cooperate in the first two rounds. For every subsequent round, cooperate
# unless your opponent defected in both of the two immediately preceding rounds;
# if they defected in both of those rounds, defect.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



#  In round one, defect. For rounds two through nine hundred ninety, if your
# opponent cooperated in the previous round, defect to exploit them; if your
# opponent defected in the previous round, defect to punish them. However, if
# you and your opponent have both defected for five consecutive rounds,
# cooperate once in the next round to attempt breaking the deadlock, then return
# to the main rule. For the final ten rounds, always defect regardless of
# history.

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._deadlock_break_used = False
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number > 990:
          return axl.Action.D
  
      if len(self.history) >= 5:
          last_five_self = self.history[-5:]
          last_five_opp = opponent.history[-5:]
          if (
              last_five_self.count(axl.Action.D) == 5
              and last_five_opp.count(axl.Action.D) == 5
              and not self._deadlock_break_used
          ):
              self._deadlock_break_used = True
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
      return axl.Action.D



# Cooperate in the first round. For each subsequent round, first check if the
# opponent cooperated in the immediately preceding round; if so, cooperate. If
# the opponent defected in the previous round, then check if they also defected
# in the round before that; if they defected in both consecutive rounds, defect.
# Otherwise—meaning they defected only in the most recent round—cooperate to
# account for possible noise.

class Cooperative_10(LLM_Strategy):
  n = 10
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Start by cooperating. For rounds 2 through 999, first check if both you and
# your opponent defected in the previous round; if so, cooperate. Otherwise, if
# your opponent defected in the previous round, defect. Otherwise, cooperate. In
# the final round, defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by defecting in the first round.  For every subsequent round, choose
# your action based on the combination of actions from the previous round,
# checked in the following order:  1. If you defected and your opponent
# cooperated, defect again to continue exploiting their cooperation. 2. If both
# you and your opponent defected, cooperate to break the deadlock and test if
# the mutual defection was caused by noise. 3. If you cooperated and your
# opponent defected, defect to punish their exploitation. 4. If both you and
# your opponent cooperated, cooperate to maintain the mutual benefit.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Begin by cooperating for the first two rounds. Thereafter, cooperate unless
# the opponent defected in both of the immediately preceding two rounds, in
# which case defect.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by cooperating in the first two rounds. For every subsequent round
# through round 1000, defect only if the opponent defected in both of the two
# immediately preceding rounds; otherwise cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by defecting. Continue defecting unless the opponent cooperates for
# three consecutive rounds, at which point switch to cooperation. While
# cooperating, continue cooperating unless the opponent defects for two
# consecutive rounds, in which case return to defection until the three-round
# cooperation threshold is met again.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._coop_streak = 0
          self._defect_streak = 0
          self._mode = "D"
          return axl.Action.D
  
      last_opp = opponent.history[-1]
  
      if self._mode == "D":
          if last_opp == axl.Action.C:
              self._coop_streak += 1
          else:
              self._coop_streak = 0
  
          if self._coop_streak >= 3:
              self._mode = "C"
              self._defect_streak = 0
              return axl.Action.C
          return axl.Action.D
  
      if last_opp == axl.Action.D:
          self._defect_streak += 1
      else:
          self._defect_streak = 0
  
      if self._defect_streak >= 2:
          self._mode = "D"
          self._coop_streak = 0
          return axl.Action.D
      return axl.Action.C



# Begin by cooperating. For every subsequent round, defect only if your opponent
# defected in both of the previous two rounds; otherwise, cooperate.

class Cooperative_12(LLM_Strategy):
  n = 12
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(opponent.history) < 2:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by cooperating. Defect only if the opponent defected in the two
# previous rounds; continue defecting until the opponent cooperates once, then
# resume cooperation. In all other situations, cooperate.

class Neutral_12(LLM_Strategy):
  n = 12
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_until_opponent_cooperates = False
          return axl.Action.C
  
      if self._defect_until_opponent_cooperates:
          if opponent.history and opponent.history[-1] == axl.Action.C:
              self._defect_until_opponent_cooperates = False
              return axl.Action.C
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._defect_until_opponent_cooperates = True
          return axl.Action.D
  
      return axl.Action.C



#  Defect in the first round. In every subsequent round, defect unless your
# opponent cooperated in both of the previous two rounds, in which case
# cooperate.

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Begin by cooperating in the first two rounds. For every subsequent round,
# cooperate unless the opponent defected in both of the two immediately
# preceding rounds; if they defected twice consecutively, defect.

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
  
      if len(self.history) < 2:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by cooperating in the first two rounds. For every subsequent round,
# defect only if your opponent defected in both of the two immediately preceding
# rounds; otherwise, cooperate.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



#  Play Defect in the first round. Thereafter, if the opponent played Defect in
# the previous round, play Defect. If the opponent played Cooperate in both of
# the previous two rounds, play Cooperate. In all other cases, play Defect.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Cooperate in the first round. Thereafter, cooperate whenever the opponent
# cooperated in the previous round. If the opponent defected in the previous
# round, defect once, then cooperate again on the following round regardless of
# the opponent's action.

class Cooperative_14(LLM_Strategy):
  n = 14
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._pending_defect = False
          return axl.Action.C
  
      if getattr(self, "_pending_defect", False):
          self._pending_defect = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          self._pending_defect = True
          return axl.Action.D
  
      return axl.Action.C



#  Cooperate in the first two rounds. From round three onward, defect only if
# the opponent defected in both of the two immediately preceding rounds;
# otherwise, cooperate.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



#  Play Defect in every round unless the opponent played Cooperate in both of
# the two immediately preceding rounds, in which case play Cooperate. In the
# final round, play Defect regardless of the opponent's history.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
              if len(self.history) >= 999:
                  return axl.Action.D
              return axl.Action.C
  
      return axl.Action.D



# Begin by cooperating. Thereafter, cooperate unless the opponent defected in
# both of the previous two rounds; if they did, defect.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by cooperating. For each subsequent round, defect only if the opponent
# defected in both of the previous two rounds; otherwise, cooperate. Continue
# applying this condition each round, returning to cooperation immediately once
# the opponent cooperates in any single round.

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
  
      if len(opponent.history) < 2:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Start by intending to Defect. For each subsequent round, intend to Defect
# unless the opponent has played Cooperate in the two previous consecutive
# rounds; if they have, intend to Cooperate. If the opponent plays Defect in any
# round, intend to Defect for the following three rounds regardless of their
# actions, then resume checking the cooperation condition.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_lock = 0
          return axl.Action.D
  
      if getattr(self, "_defect_lock", None) is None:
          self._defect_lock = 0
  
      if self._defect_lock > 0:
          self._defect_lock -= 1
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.D:
          self._defect_lock = 2
          return axl.Action.D
  
      return axl.Action.D



# **Strategy: Patient Reciprocity**  Cooperate in the first round. For every
# subsequent round, cooperate unless your opponent defected in both of the
# previous two rounds; only in that case should you defect. Once you have
# defected under this condition, return to cooperating immediately in the next
# round if your opponent cooperates.

class Cooperative_16(LLM_Strategy):
  n = 16
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Cooperate in the first round. For rounds two through 999, defect only if your
# opponent defected in both of the previous two consecutive rounds; otherwise
# cooperate. In the final round, defect regardless of the opponent’s prior
# actions.

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
  
      # Final round of a 1000-round match: defect regardless.
      if len(self.history) == 999:
          return axl.Action.D
  
      # Defect only if opponent defected in both of the previous two rounds.
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by defecting. For each of the next 997 rounds, choose the action your
# opponent played in the immediately preceding round. If you and your opponent
# have both defected for three consecutive rounds, override the previous rule
# and cooperate in the next round to test for cooperation, then resume copying
# your opponent's previous action. Defect in the final two rounds regardless of
# history.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._test_cooperate_next = False
          return axl.Action.D
  
      round_number = len(self.history) + 1  # 1-indexed current round
  
      # Final two rounds: defect regardless of history.
      if round_number >= 999:
          return axl.Action.D
  
      # If we previously decided to test cooperation after three consecutive mutual defections,
      # do so now and then resume copying.
      if getattr(self, "_test_cooperate_next", False):
          self._test_cooperate_next = False
          return axl.Action.C
  
      # If both players have defected for three consecutive rounds, cooperate next round.
      if len(self.history) >= 3:
          if (
              self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
              and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
          ):
              self._test_cooperate_next = True
  
      # For rounds 2 through 998, copy opponent's immediately preceding action.
      return opponent.history[-1]



#  Cooperate in round one. For rounds two through nine hundred and ninety,
# cooperate if the opponent cooperated in at least one of the previous two
# rounds; if the opponent defected in both of the previous two rounds, defect.
# For rounds nine hundred ninety-one through one thousand, defect regardless of
# the opponent’s action.

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
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      recent_opponent_history = opponent.history[-2:]
      if recent_opponent_history.cooperations >= 1:
          return axl.Action.C
      return axl.Action.D



#  Start by cooperating. In each subsequent round, if your previous payoff was 3
# or 5, repeat the same action you played in the previous round. If your
# previous payoff was 0 or 1, switch to the opposite action.

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
  
      last_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_payoff in (3, 5):
          return self.history[-1]
      elif last_payoff in (0, 1):
          return axl.Action.D if self.history[-1] == axl.Action.C else axl.Action.C
  
      return self.history[-1]



#  Defect in the first two rounds. Then, in each subsequent round, cooperate
# only if the opponent cooperated in both of the two immediately preceding
# rounds; otherwise, defect.

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(self.history) < 2 or len(opponent.history) < 2:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Begin by cooperating. For every subsequent round, cooperate if your opponent
# cooperated in the previous round. If your opponent defected in the previous
# round, check the round before that: cooperate if they cooperated then, but
# defect if they defected in both of the previous two consecutive rounds.

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
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2:
          if opponent.history[-2] == axl.Action.C:
              return axl.Action.C
          if opponent.history[-2] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C



# Begin by cooperating in the first two rounds. For every subsequent round,
# defect only if your opponent defected in both of the previous two rounds;
# otherwise, cooperate.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



#  Defect on the first round. Thereafter, apply these conditions in order:  If
# you cooperated in the previous round and the opponent defected, defect.  If
# you and the opponent both defected in the previous round, cooperate.  If the
# opponent cooperated in the previous round, defect.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
  
      if last_opp == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.D



# Cooperate in the first two rounds. For every subsequent round, cooperate
# unless your opponent defected in both of the two immediately preceding rounds;
# if they defected twice consecutively, defect.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# Cooperate in the first two rounds. For every subsequent round, defect only if
# the opponent defected in both of the previous two rounds; otherwise,
# cooperate.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



#  Begin by defecting in the first round. For every subsequent round, defect by
# default. Cooperate only if the opponent cooperated in both of the two
# immediately preceding rounds; otherwise, continue defecting. If the opponent
# ever defects in a round, resetting the consecutive cooperation streak, revert
# immediately to defection and do not cooperate again until they have completed
# two new consecutive rounds of cooperation.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._coop_streak = 0
          return axl.Action.D
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.D:
          self._coop_streak = 0
      elif len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.C, axl.Action.C]:
          self._coop_streak = 2
      else:
          self._coop_streak = 0
  
      if self._coop_streak >= 2:
          return axl.Action.C
      return axl.Action.D



#  Begin by cooperating. In every subsequent round, defect only if your opponent
# defected in the two immediately preceding rounds; otherwise, cooperate.

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
  
      if len(opponent.history) < 2:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the first two rounds. For every subsequent round,
# defect only if your opponent defected in both of the two immediately preceding
# rounds; otherwise, cooperate.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



#  Defect in the first round. In each subsequent round, cooperate only if the
# opponent cooperated in both of the previous two rounds; otherwise, defect.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Begin by cooperating. Thereafter, cooperate unless your opponent defected in
# both of the previous two consecutive rounds, in which case defect. Return to
# cooperation immediately when your opponent cooperates again.

class Cooperative_21(LLM_Strategy):
  n = 21
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(opponent.history) < 2:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Begin by cooperating. For rounds two through nine hundred and ninety-nine,
# cooperate unless your opponent defected in both of the previous two rounds; if
# they defected in both prior rounds, defect. In round one thousand, defect
# regardless of previous actions.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          if len(self.history) >= 999:
              return axl.Action.D
          return axl.Action.D
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return axl.Action.C



#  Start by playing Defect. Thereafter, play Defect by default. Cooperate for
# exactly one round only if either of the following two conditions is met:
# first, you observe the opponent has played Cooperate for two consecutive
# rounds; or second, you and the opponent have both played Defect for five
# consecutive rounds. After that single round of cooperation, resume playing
# Defect. If at any point you are playing Cooperate and you observe the opponent
# playing Defect, immediately resume playing Defect.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._cooperate_next = False
          return axl.Action.D
  
      if getattr(self, "_cooperate_next", False):
          self._cooperate_next = False
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.C, axl.Action.C]:
          self._cooperate_next = True
          return axl.Action.C
  
      if len(self.history) >= 5 and len(opponent.history) >= 5:
          if self.history[-5:] == [axl.Action.D] * 5 and opponent.history[-5:] == [axl.Action.D] * 5:
              self._cooperate_next = True
              return axl.Action.C
  
      return axl.Action.D



# Begin by cooperating. For rounds two through nine hundred and ninety-nine,
# cooperate unless the opponent defected in both of the previous two rounds, in
# which case defect; if you are defecting and the opponent cooperates, resume
# cooperation immediately. In round one thousand, defect regardless of the
# opponent’s prior actions.

class Cooperative_22(LLM_Strategy):
  n = 22
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defecting = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          self._defecting = True
          return axl.Action.D
  
      if self._defecting:
          if opponent.history and opponent.history[-1] == axl.Action.C:
              self._defecting = False
              return axl.Action.C
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._defecting = True
          return axl.Action.D
  
      return axl.Action.C



#  Cooperate in the first round. For rounds two through nine hundred ninety-
# nine, cooperate if the opponent cooperated in the previous round; if the
# opponent defected in the previous round, defect once, then resume cooperation
# in the following round regardless of their action. Defect in the final round.

class Neutral_22(LLM_Strategy):
  n = 22
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_next = False
          return axl.Action.C
  
      round_number = len(self.history) + 1  # 1-based round number for the move to be chosen
  
      if round_number == 1000:
          return axl.Action.D
  
      if self._punish_next:
          self._punish_next = False
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          self._punish_next = True
          return axl.Action.D
  
      return axl.Action.C



#  Begin by playing Defect.  For each subsequent round, apply the first
# applicable condition from the following list:  1. If you and your opponent
# have both played Defect for three consecutive rounds, play Cooperate. 2. If
# your opponent played Defect in the previous round, play Defect. 3. If you
# played Defect and your opponent played Cooperate in the previous round, play
# Defect. 4. If you and your opponent both played Cooperate in the previous
# round, play Cooperate. 5. Otherwise, play Defect.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(self.history) >= 3:
          if (
              self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
              and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
          ):
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



#  Begin by cooperating. Thereafter, cooperate unless your opponent defected in
# both of the previous two rounds; if they defected in both previous rounds,
# defect.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Begin by cooperating. In each subsequent round, cooperate unless the opponent
# defected in both of the previous two rounds; only in that case do you defect.
# Continue applying this rule through all 1000 rounds.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Defect in the first round. For each subsequent round up to round 999, defect
# unless the opponent cooperated in both of the previous two rounds, in which
# case cooperate. Defect in round 1000 regardless of the opponent's action.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
              if len(self.history) < 999:
                  return axl.Action.C
  
      return axl.Action.D



# **Strategy: Forgiving Reciprocity**  1.  Cooperate in the first round and the
# second round. 2.  For every subsequent round, examine the opponent’s actions
# in the previous two rounds. If the opponent defected in both of those rounds,
# defect. Otherwise, cooperate.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



#  Begin by cooperating in the first round. For rounds 2 through 999, cooperate
# if your payoff in the previous round was 3 or 1, and defect if your payoff was
# 5 or 0. Defect unconditionally in round 1000.

class Neutral_24(LLM_Strategy):
  n = 24
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0] if False else None
      if len(self.history) >= 1:
          my_last, opp_last = self.total_scores(self.history[-1:], opponent.history[-1:])
          last_payoff = my_last
      else:
          last_payoff = 0
  
      if last_payoff in (3, 1):
          return axl.Action.C
      if last_payoff in (5, 0):
          return axl.Action.D
  
      return axl.Action.C



#  Defect in the first round. Thereafter, cooperate only if the opponent
# cooperated in the previous two consecutive rounds. If the opponent defects at
# any point, defect for the next two rounds regardless of their actions, then
# resume checking for consecutive cooperation.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_remaining = 0
          return axl.Action.D
  
      if getattr(self, "_punish_remaining", None) is None:
          self._punish_remaining = 0
  
      if self._punish_remaining > 0:
          self._punish_remaining -= 1
          return axl.Action.D
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.D:
          self._punish_remaining = 1
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



#  Begin by cooperating in round one, and cooperate again in round two
# regardless of the opponent’s first move. For rounds three through nine hundred
# and ninety-nine, defect only if the opponent defected in both of the previous
# two consecutive rounds; otherwise, cooperate. In round one thousand, defect
# unconditionally.

class Cooperative_25(LLM_Strategy):
  n = 25
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number == 2:
          return axl.Action.C
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by cooperating in the first two rounds. For rounds three through nine
# hundred and ninety-nine, cooperate unless your opponent defected in both of
# the two immediately preceding rounds, in which case defect. In the one
# thousandth and final round, defect regardless of the opponent’s prior actions.

class Neutral_25(LLM_Strategy):
  n = 25
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._round = 1
          return axl.Action.C
      if len(self.history) == 1:
          self._round = 2
          return axl.Action.C
  
      self._round = len(self.history) + 1
  
      if self._round == 1000:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C