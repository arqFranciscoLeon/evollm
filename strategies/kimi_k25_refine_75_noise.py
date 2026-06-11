import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



#  Defect during the first five rounds. If the opponent cooperated in at least
# three of those five rounds, cooperate starting round six; otherwise continue
# defecting until this condition is met. While cooperating, if the opponent
# defects in four or more of the last five rounds, defect for the next three
# rounds, then cooperate once to test; resume cooperation if they cooperate in
# that test round, otherwise repeat the punishment cycle. In rounds 991 through
# 1000, always defect. Base all decisions on observed actions.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._phase = "initial_defect"
          self._punish_remaining = 0
          self._test_pending = False
          return axl.Action.D
  
      round_num = len(self.history) + 1
  
      if round_num >= 991:
          return axl.Action.D
  
      if self._phase == "initial_defect":
          if len(self.history) < 5:
              return axl.Action.D
          if self.history[:5].cooperations >= 3:
              self._phase = "cooperate"
              return axl.Action.C
          return axl.Action.D
  
      if self._phase == "punish":
          if self._punish_remaining > 0:
              self._punish_remaining -= 1
              return axl.Action.D
          self._phase = "test"
          return axl.Action.C
  
      if self._phase == "test":
          if opponent.history and opponent.history[-1] == axl.Action.C:
              self._phase = "cooperate"
              return axl.Action.C
          self._phase = "punish"
          self._punish_remaining = 2
          return axl.Action.D
  
      if len(opponent.history) >= 5 and opponent.history[-5:].count(axl.Action.D) >= 4:
          self._phase = "punish"
          self._punish_remaining = 2
          return axl.Action.D
  
      return axl.Action.C



# Begin by cooperating in rounds 1 and 2. For each round from 3 through 999,
# defect only if your opponent defected in both of the two immediately preceding
# rounds; otherwise cooperate. In round 1000, defect.

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
      if len(self.history) >= 999:
          return axl.Action.D
      return axl.Action.D if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D else axl.Action.C



# Begin by cooperating. Thereafter, until round 997, defect if the opponent has
# defected in any of the last three rounds; otherwise cooperate. Defect in
# rounds 998, 999, and 1000.

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
  
      round_number = len(self.history) + 1
  
      if round_number >= 998:
          return axl.Action.D
  
      if len(opponent.history) >= 3 and axl.Action.D in opponent.history[-3:]:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by defecting in round 1. For each subsequent round, apply these
# conditions in order:  First, if you and your opponent both defected in each of
# the previous two consecutive rounds, cooperate.  Second, if your opponent
# defected in the previous round, defect.  Third, if you defected in the
# previous round, defect.  Fourth, cooperate.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Cooperate in rounds 1 and 2. For rounds 3 through 999: defect only if the
# opponent’s observed action was defection in both of the two immediately
# preceding rounds; otherwise cooperate. In round 1000, defect unconditionally.

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
  
      round_number = len(self.history) + 1
  
      if round_number in (1, 2):
          return axl.Action.C
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Cooperate in rounds 1 and 2. For rounds 3 through 998: defect only if the
# opponent’s observed action was Defect in both of the two immediately preceding
# rounds; otherwise cooperate. If you defected in the previous round under this
# rule and the opponent’s observed action that round was also Defect, cooperate
# in the current round to attempt restoration of mutual cooperation. In rounds
# 999 and 1000, defect unconditionally.

class Neutral_2(LLM_Strategy):
  n = 2
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._restore_after_defect = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number in (999, 1000):
          return axl.Action.D
  
      if self._restore_after_defect:
          self._restore_after_defect = False
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.C
  
      if round_number in (1, 2):
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._restore_after_defect = True
          return axl.Action.D
  
      return axl.Action.C



#  Defect in round 1. Defect in round 2. For rounds 3 through 990, cooperate if
# the opponent cooperated in at least one of the previous two rounds; otherwise
# defect. Defect in rounds 991 through 1000.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 2:
          return axl.Action.D
  
      if 3 <= round_number <= 990:
          recent_opponent = opponent.history[-2:]
          return axl.Action.C if axl.Action.C in recent_opponent else axl.Action.D
  
      return axl.Action.D



# Begin by cooperating. Each round, examine the opponent’s observed actions over
# the previous four rounds. If the opponent defected in at least three of those
# four rounds, defect; otherwise, cooperate. If you have defected for five
# consecutive rounds, cooperate on the next round regardless of the opponent’s
# recent history.

class Cooperative_3(LLM_Strategy):
  n = 3
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._consecutive_defections = 0
          return axl.Action.C
  
      if self._consecutive_defections >= 5:
          self._consecutive_defections = 0
          return axl.Action.C
  
      recent_opponent = opponent.history[-4:]
      if recent_opponent.count(axl.Action.D) >= 3:
          action = axl.Action.D
      else:
          action = axl.Action.C
  
      if action == axl.Action.D:
          self._consecutive_defections += 1
      else:
          self._consecutive_defections = 0
  
      return action



#  Cooperate in the first two rounds. For rounds 3 through 990, defect only if
# the opponent defected in at least two of the previous three rounds; otherwise,
# cooperate. For rounds 991 through 1000, defect unconditionally. Base all
# decisions on the opponent's observed actions.

class Neutral_3(LLM_Strategy):
  n = 3
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._round_index = 1
          return axl.Action.C
  
      self._round_index += 1
  
      if self._round_index <= 2:
          return axl.Action.C
  
      if self._round_index >= 991:
          return axl.Action.D
  
      recent_opponent = opponent.history[-3:]
      if recent_opponent.count(axl.Action.D) >= 2:
          return axl.Action.D
      return axl.Action.C



#  Defect in round one. For rounds two through nine hundred and ninety-nine: if
# the opponent's observed action in the previous round was cooperate, defect; if
# the opponent's observed action in the previous round was defect, defect.
# Defect in round one thousand.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return axl.Action.D



# Cooperate in round one and round two. For each round from three through nine
# hundred and ninety-nine, cooperate unless the opponent defected in both of the
# two immediately preceding rounds; otherwise, defect. In round one thousand,
# defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number == 2:
          return axl.Action.C
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by intending to cooperate in round 1. After each round from 2 to 999,
# deduce your realized action from your payoff: if you received 0 or 3, you
# cooperated; if you received 1 or 5, you defected. If your payoff was 3 or 5,
# intend to play the same realized action in the next round. If your payoff was
# 0 or 1, intend to play the opposite action from your realized action. In round
# 1000, intend to defect.

class Neutral_4(LLM_Strategy):
  n = 4
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          self._intended_action = axl.Action.D
          return axl.Action.D
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0] if False else None
      # Compute realized action from the last round's payoff using the last interaction only.
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
      last_payoff = my_last_score
  
      if last_payoff in (0, 3):
          realized_action = axl.Action.C
      else:
          realized_action = axl.Action.D
  
      if last_payoff in (3, 5):
          self._intended_action = realized_action
      else:
          self._intended_action = axl.Action.D if realized_action == axl.Action.C else axl.Action.C
  
      return self._intended_action



#  Begin by defecting in round 1. For rounds 2 through 999: defect if the
# opponent defected in the immediately preceding round; otherwise, cooperate
# only if the opponent cooperated in at least two of the last three rounds. In
# round 1000, defect.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      last_three = opponent.history[-3:]
      if last_three.count(axl.Action.C) >= 2:
          return axl.Action.C
  
      return axl.Action.D



# Cooperate in round 1. For rounds 2 through 4, cooperate unless the opponent
# defected in every previous round; otherwise defect. For rounds 5 through 990,
# cooperate only if the opponent cooperated in at least three of the previous
# four rounds; otherwise defect. For rounds 991 through 1000, always defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number <= 4:
          if len(opponent.history) == 0:
              return axl.Action.C
          if all(move == axl.Action.D for move in opponent.history):
              return axl.Action.D
          return axl.Action.C
  
      if round_number <= 990:
          recent_opponent = opponent.history[-4:]
          if recent_opponent.count(axl.Action.C) >= 3:
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.D



#  Begin by cooperating in the first round. For rounds two through nine hundred
# and ninety-nine, cooperate if your realized action in the immediately
# preceding round matched your opponent's realized action in that same
# round—meaning you both actually cooperated or both actually defected—and
# defect if those realized actions differed. In the one thousandth round, defect
# unconditionally.

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
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



#  Play Defect in the first round. For rounds 2 through 998, maintain a
# punishment counter beginning at zero. If the counter is greater than zero,
# decrease it by one and play Defect. Otherwise, if the opponent played Defect
# in either of the previous two rounds, set the counter to one and play Defect.
# Otherwise, if the opponent played Cooperate in the two most recent rounds,
# play Cooperate. Otherwise, play Defect. For rounds 999 and 1000, play Defect.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishment_counter = 0
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number >= 999:
          return axl.Action.D
  
      if self._punishment_counter > 0:
          self._punishment_counter -= 1
          return axl.Action.D
  
      if len(opponent.history) >= 2 and (
          opponent.history[-1] == axl.Action.D or opponent.history[-2] == axl.Action.D
      ):
          self._punishment_counter = 1
          return axl.Action.D
  
      if len(opponent.history) >= 2 and (
          opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C
      ):
          return axl.Action.C
  
      return axl.Action.D



#  Cooperate in the first round. For each round from 2 to 999: if you defected
# in the immediately preceding round, cooperate; otherwise, if the opponent
# defected in the immediately preceding round, defect; otherwise, cooperate. In
# round 1000, defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
      elif opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          return axl.Action.C



# Cooperate in the first two rounds. For rounds three through one thousand,
# cooperate unless the opponent defected in at least two of the three
# immediately preceding rounds, in which case defect.

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
      if len(self.history) == 1:
          return axl.Action.C
      if len(opponent.history) < 3:
          return axl.Action.C
      if opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
      return axl.Action.C



#  Begin by intending Defect. For rounds 2 through 990, if your previous
# intended action was Defect, intend Defect regardless of the payoff;
# specifically, interpret a payoff of 5 as successful exploitation, a payoff of
# 1 as mutual defection requiring continued pressure, and payoffs of 0 or 3 as
# evidence that noise caused accidental cooperation, which requires immediate
# correction back to intended Defection. If your previous intended action was
# Cooperate (possible only through execution error), intend Defect. For rounds
# 991 through 1000, intend Defect unconditionally.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.D
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          self._intended_action = axl.Action.D
          return axl.Action.D
  
      # Rounds 2 through 990: always intend Defect, regardless of observed payoff.
      self._intended_action = axl.Action.D
      return axl.Action.D



#  Cooperate in the first round. For each round from 2 to 999: if you and your
# opponent played the same action in the previous round, cooperate; if you
# played D and your opponent played C, cooperate; if you played C and your
# opponent played D, defect. In the 1000th round, defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == opp_last:
          return axl.Action.C
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Cooperate in the first two rounds. For each round from the third through the
# nine hundred ninety-ninth, cooperate unless the opponent defected in both of
# the previous two rounds, in which case defect. Defect in the one thousandth
# round.

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
      if len(self.history) == 1:
          return axl.Action.C
      if len(self.history) >= 999:
          return axl.Action.D
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



#  Begin with Defection in round one and round two. For rounds three through
# nine hundred and ninety, play Defection unless the opponent played Cooperate
# in the immediately preceding round, in which case play Cooperate. For rounds
# nine hundred and ninety-one through one thousand, play Defect regardless of
# the opponent's actions.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number <= 2:
          return axl.Action.D
  
      if 3 <= round_number <= 990:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      return axl.Action.D



# Begin by cooperating in the first two rounds. For rounds 3 through 999,
# cooperate unless the opponent was observed to defect in both of the two
# immediately preceding rounds, in which case defect; following any defection
# enacted under this rule, return to cooperation in the subsequent round
# regardless of the opponent's observed action. In round 1000, defect.

class Cooperative_8(LLM_Strategy):
  n = 8
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._pending_return_to_cooperation = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if getattr(self, "_pending_return_to_cooperation", False):
          self._pending_return_to_cooperation = False
          return axl.Action.C
  
      if round_number <= 2:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._pending_return_to_cooperation = True
          return axl.Action.D
  
      return axl.Action.C



#  Begin by cooperating. For rounds 2 through 999, cooperate if your previous
# payoff was 3 or 5, and defect if your previous payoff was 0 or 1. In round
# 1000, defect regardless of the previous payoff.

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
  
      if round_number == 1000:
          return axl.Action.D
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0] if False else None
  
      if len(self.history) >= 1:
          my_last_move = self.history[-1]
          opp_last_move = opponent.history[-1]
          if my_last_move == axl.Action.C and opp_last_move == axl.Action.C:
              last_payoff = 3
          elif my_last_move == axl.Action.C and opp_last_move == axl.Action.D:
              last_payoff = 0
          elif my_last_move == axl.Action.D and opp_last_move == axl.Action.C:
              last_payoff = 5
          else:
              last_payoff = 1
  
      if last_payoff in (3, 5):
          return axl.Action.C
      if last_payoff in (0, 1):
          return axl.Action.D
  
      return axl.Action.C



#  **Strategy: Aggressive Noise-Adjusted**  Begin by defecting in round 1.
# Maintain a punishment counter, initially set to 0.  For each subsequent round,
# apply the first applicable condition:  1. If the punishment counter is greater
# than 0, defect and reduce the counter by 1. 2. If in the previous round you
# observed your own realized action was cooperation and the opponent's realized
# action was defection, set the punishment counter to 4 and defect. 3. If the
# opponent's realized action was cooperation in the two most recent consecutive
# rounds, cooperate. 4. Otherwise, defect.  Definitions and clarifications: -
# "Realized action" refers to the action as played after potential noise
# flipping, which both players observe at the end of each round. - For rounds 2
# and 3, treat any non-existent previous rounds as observed defection when
# evaluating condition 3. - During a punishment phase (counter > 0), do not
# evaluate conditions 2, 3, or 4; simply defect until the counter reaches 0.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.punishment_counter = 0
          return axl.Action.D
  
      if self.punishment_counter > 0:
          self.punishment_counter -= 1
          return axl.Action.D
  
      if len(self.history) >= 1:
          my_last = self.history[-1]
          opp_last = opponent.history[-1]
          if my_last == axl.Action.C and opp_last == axl.Action.D:
              self.punishment_counter = 4
              return axl.Action.D
  
      opp_last_two = opponent.history[-2:]
      if len(opp_last_two) < 2:
          opp_last_two = [axl.Action.D] * (2 - len(opp_last_two)) + list(opp_last_two)
  
      if opp_last_two[-2] == axl.Action.C and opp_last_two[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



#  Begin by cooperating in round 1. In round 2, cooperate. In each round from 3
# to 999, defect only if the opponent’s observed action was defection in both of
# the previous two rounds; otherwise, cooperate. In round 1000, defect.

class Cooperative_9(LLM_Strategy):
  n = 9
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
  
      if len(self.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              if len(self.history) == 999:
                  return axl.Action.D
              return axl.Action.D
  
      if len(self.history) == 999:
          return axl.Action.D
  
      return axl.Action.C



#  Cooperate in rounds 1 and 2. For rounds 3 through 998, cooperate unless the
# opponent actually defected in both of the previous two rounds, in which case
# defect. Defect unconditionally in rounds 999 and 1000.

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
  
      round_number = len(self.history) + 1
  
      if round_number in (1, 2):
          return axl.Action.C
  
      if round_number >= 999:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Begin by defecting. Base decisions on observed actions. If mutual cooperation
# occurred in the previous round, cooperate to maintain it. If you defected and
# the opponent cooperated, defect to exploit. If you cooperated and the opponent
# defected, defect to punish. If mutual defection persists for three consecutive
# rounds, cooperate once to test; if the opponent responds with cooperation,
# continue cooperating, otherwise resume defecting. When assessing persistence
# or responses, ignore isolated deviations as potential noise by requiring
# consistent behavior over two rounds before changing strategy.

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mode = "defect"
          self._test_pending = False
          self._test_rounds = 0
          self._coop_streak = 0
          self._defect_streak = 0
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      # Track recent observed patterns, requiring two consecutive rounds
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          self._coop_streak += 1
      else:
          self._coop_streak = 0
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          self._defect_streak += 1
      else:
          self._defect_streak = 0
  
      # If we are in a testing phase after persistent mutual defection
      if self._test_pending:
          self._test_rounds += 1
          if last_self == axl.Action.C and last_opp == axl.Action.C:
              self._mode = "cooperate"
              self._test_pending = False
              self._test_rounds = 0
              self._coop_streak = 2
              self._defect_streak = 0
              return axl.Action.C
          if self._test_rounds >= 2:
              self._mode = "defect"
              self._test_pending = False
              self._test_rounds = 0
              self._coop_streak = 0
              self._defect_streak = 0
              return axl.Action.D
          return axl.Action.D
  
      # Maintain cooperation only after two consecutive mutual cooperations
      if self._mode == "cooperate":
          if self._coop_streak >= 2:
              return axl.Action.C
          if last_self == axl.Action.D and last_opp == axl.Action.C:
              self._mode = "defect"
              self._coop_streak = 0
              return axl.Action.D
          if last_self == axl.Action.C and last_opp == axl.Action.D:
              self._mode = "defect"
              self._coop_streak = 0
              return axl.Action.D
          return axl.Action.D
  
      # Persistent mutual defection for three consecutive rounds -> test once
      if self._defect_streak >= 3:
          self._test_pending = True
          self._test_rounds = 0
          return axl.Action.C
  
      # Default behavior: defect
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          self._mode = "defect"
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          self._mode = "defect"
          return axl.Action.D
  
      return axl.Action.D



#  1. In rounds 1 through 997: Cooperate unless the opponent defected in each of
# the three immediately preceding rounds, in which case defect for the next two
# rounds before resuming cooperation.  2. In rounds 998 through 1000: Defect.

class Cooperative_10(LLM_Strategy):
  n = 10
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_remaining = 0
  
      round_number = len(self.history) + 1
  
      if round_number >= 998:
          return axl.Action.D
  
      if self._punish_remaining > 0:
          self._punish_remaining -= 1
          return axl.Action.D
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          self._punish_remaining = 1
          return axl.Action.D
  
      return axl.Action.C



# Cooperate in round 1. For rounds 2 through 999, cooperate unless the opponent
# has defected in at least two of the last three rounds (or in all preceding
# rounds if fewer than three have occurred), in which case defect. In round
# 1000, defect.

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
  
      if round_number <= 3:
          opponent_defections = opponent.history.defections
      else:
          opponent_defections = opponent.history[-3:].count(axl.Action.D)
  
      if opponent_defections >= 2:
          return axl.Action.D
  
      return axl.Action.C



# Round 1: Play Defection.  Round 2: Play Cooperation if the opponent's observed
# action in round 1 was Cooperation; otherwise play Defection.  For rounds 3
# through 1000: Play Cooperation if the opponent's observed action in the
# immediately preceding round was Cooperation; otherwise play Defection.

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
  
      if len(opponent.history) == 0:
          return axl.Action.D
  
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# Cooperate in rounds 1 and 2. For each subsequent round, defect only if the
# opponent defected in both of the previous two rounds; otherwise cooperate.

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



# Cooperate in the first two rounds. For rounds 3 through 999, defect if the
# opponent’s observed action was defection in both of the previous two rounds;
# otherwise cooperate. In round 1000, defect.

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
      if len(self.history) >= 999:
          return axl.Action.D
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# Round 1: Defect.  Round 2: If both players defected in round 1, cooperate;
# otherwise, play the realized action your opponent played in round 1.  Rounds 3
# through 990: Play according to the following ordered conditions based on
# realized actions: 1. If your opponent defected in the previous round and the
# previous two rounds show an alternating pattern—specifically, (You cooperated,
# Opponent defected) followed by (You defected, Opponent cooperated)—then
# cooperate to break the noise-induced cycle. 2. Otherwise, if the previous
# round was mutual defection and the round before that was not mutual defection,
# cooperate to attempt recovery; however, if the opponent defects against this
# recovery cooperation, defect for the subsequent two rounds before re-
# evaluating. 3. Otherwise, play the same realized action your opponent played
# in the previous round.  Rounds 991 through 1000: Defect.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._recovery_defect_rounds = 0
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 2:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
          return opponent.history[-1]
  
      if 991 <= round_number <= 1000:
          return axl.Action.D
  
      if getattr(self, "_recovery_defect_rounds", 0) > 0:
          self._recovery_defect_rounds -= 1
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
      prev_self = self.history[-2]
      prev_opp = opponent.history[-2]
  
      if (
          last_opp == axl.Action.D
          and prev_self == axl.Action.C
          and prev_opp == axl.Action.D
          and last_self == axl.Action.D
          and last_opp == axl.Action.C
      ):
          return axl.Action.C
  
      if last_self == axl.Action.D and last_opp == axl.Action.D and not (
          prev_self == axl.Action.D and prev_opp == axl.Action.D
      ):
          if last_opp == axl.Action.D:
              self._recovery_defect_rounds = 2
          return axl.Action.C
  
      return opponent.history[-1]



# Cooperate in round 1. In round 2, cooperate unless the opponent's observed
# action in round 1 was defection. For rounds 3 through 999, cooperate unless
# the opponent's observed action was defection in both of the two immediately
# preceding rounds; otherwise, defect. In round 1000, defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number == 2:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating. For rounds 2 through 999, observe the payoff you
# received in the previous round: if it was 3 or 5, play the same action you
# played previously; if it was 0 or 1, switch to the opposite action. In round
# 1000, defect unconditionally.

class Neutral_12(LLM_Strategy):
  n = 12
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
      # Compute previous-round payoff from the last interaction only
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
      last_payoff = my_last_score
  
      if last_payoff in (3, 5):
          return self.history[-1]
      if last_payoff in (0, 1):
          return axl.Action.D if self.history[-1] == axl.Action.C else axl.Action.C
  
      return self.history[-1]



#  Defect on the first two rounds. For rounds 3 through 999, apply these rules
# in order: First, if you observed your opponent cooperate in the previous
# round, defect. Second, if you observed both players defect in each of the
# previous three rounds, cooperate. Third, otherwise defect. Defect on round
# 1000.

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
  
      round_number = len(self.history) + 1
  
      if round_number <= 2:
          return axl.Action.D
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(self.history) >= 3 and len(opponent.history) >= 3:
          if all(
              self.history[-i] == axl.Action.D and opponent.history[-i] == axl.Action.D
              for i in range(1, 4)
          ):
              return axl.Action.C
  
      return axl.Action.D



# Begin by cooperating in round one. For rounds two through nine hundred and
# ninety-nine: if the opponent defected in both of the two immediately preceding
# rounds, defect; otherwise, cooperate. In round one thousand, defect.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          if len(self.history) < 999:
              return axl.Action.D
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return axl.Action.C



# Cooperate in the first round. For rounds 2 through 998, defect if the opponent
# defected in the previous round while you intended to cooperate; cooperate if
# the opponent defected in the previous round while you intended to defect;
# otherwise cooperate. Defect unconditionally in rounds 999 and 1000.

class Neutral_13(LLM_Strategy):
  n = 13
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 999:
          self._intended_action = axl.Action.D
          return axl.Action.D
  
      prev_opponent = opponent.history[-1]
      prev_intended = getattr(self, "_intended_action", axl.Action.C)
  
      if prev_opponent == axl.Action.D and prev_intended == axl.Action.C:
          action = axl.Action.D
      elif prev_opponent == axl.Action.D and prev_intended == axl.Action.D:
          action = axl.Action.C
      else:
          action = axl.Action.C
  
      self._intended_action = action
      return action



#  Defect in round one. For rounds two through three, defect regardless of
# observed actions. For rounds four through nine hundred fifty, defect unless
# five consecutive rounds of mutual defection have been observed, in which case
# cooperate for one round to test for cooperation, then resume defecting. If the
# opponent is observed to cooperate while you defect, continue defecting to
# extract the maximum payoff of five. For rounds nine hundred fifty-one through
# one thousand, defect unconditionally.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._test_round = None
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number <= 3:
          return axl.Action.D
  
      if round_number >= 951:
          return axl.Action.D
  
      # Detect whether the last five rounds were mutual defections.
      if len(self.history) >= 5:
          last_five_self = self.history[-5:]
          last_five_opp = opponent.history[-5:]
          if (
              last_five_self.count(axl.Action.D) == 5
              and last_five_opp.count(axl.Action.D) == 5
          ):
              # Cooperate once to test for cooperation, then resume defecting.
              if self._test_round != round_number:
                  self._test_round = round_number
                  return axl.Action.C
  
      # If opponent cooperated while we defected, keep defecting to exploit.
      return axl.Action.D



#  Begin by cooperating in round one. For rounds two through 999: cooperate
# unless the opponent defected in the previous round, you cooperated in the
# round prior to that, and the opponent also defected in the round prior to
# that, in which case defect and continue defecting until the opponent
# cooperates, at which point resume cooperation. In round 1000, cooperate if the
# opponent cooperated in round 999; otherwise defect.

class Cooperative_14(LLM_Strategy):
  n = 14
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishing = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      if self._punishing:
          if opponent.history[-1] == axl.Action.C:
              self._punishing = False
              return axl.Action.C
          return axl.Action.D
  
      if (
          len(self.history) >= 2
          and opponent.history[-1] == axl.Action.D
          and self.history[-2] == axl.Action.C
          and opponent.history[-2] == axl.Action.D
      ):
          self._punishing = True
          return axl.Action.D
  
      return axl.Action.C



#  Cooperate in rounds 1 and 2. For rounds 3 through 998, examine the opponent’s
# actions in the three most recent completed rounds; defect if at least two are
# defections, otherwise cooperate. Defect in rounds 999 and 1000.

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
  
      round_number = len(self.history) + 1
  
      if round_number in (1, 2):
          return axl.Action.C
      if round_number in (999, 1000):
          return axl.Action.D
  
      recent_opponent_moves = opponent.history[-3:]
      if recent_opponent_moves.count(axl.Action.D) >= 2:
          return axl.Action.D
      return axl.Action.C



#  Defect in the first round. For each round from the second through the nine
# hundred and ninety-ninth, base your decision on your intended action in the
# previous round and the payoff you received. If you intended to cooperate and
# received three or five points, cooperate again. If you intended to cooperate
# and received zero or one point, defect. If you intended to defect and received
# exactly three points, cooperate. If you intended to defect and received any
# other payoff, defect. Defect unconditionally in the one thousandth round.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.D
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          self._intended_action = axl.Action.D
          return axl.Action.D
  
      last_intended = self._intended_action
      my_last_payoff, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_intended == axl.Action.C:
          if my_last_payoff in (3, 5):
              action = axl.Action.C
          else:
              action = axl.Action.D
      else:
          if my_last_payoff == 3:
              action = axl.Action.C
          else:
              action = axl.Action.D
  
      self._intended_action = action
      return action



# Cooperate in rounds 1 and 2. For each round from 3 through 999, defect only if
# your opponent defected in both of the previous two rounds; otherwise
# cooperate. If you begin defecting due to this condition, resume cooperation
# immediately in the next round once your opponent cooperates (i.e., do not
# extend punishment beyond the duration of the two-round defection streak).
# Defect in round 1000 regardless of the history.

class Cooperative_15(LLM_Strategy):
  n = 15
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishing = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._punishing = True
          return axl.Action.D
  
      self._punishing = False
      return axl.Action.C



# Cooperate in the first round. For each round from 2 through 999, cooperate if
# the opponent's observed action in the immediately preceding round was
# cooperation, and defect if the opponent's observed action in the immediately
# preceding round was defection. In round 1000, defect regardless of the
# opponent's previous action.

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
  
      if len(opponent.history) >= 1:
          if len(self.history) >= 999:
              return axl.Action.D
          return opponent.history[-1]
  
      return axl.Action.C



#  Defect in rounds one and two. For rounds three through nine hundred ninety-
# eight, maintain a punishment counter initialized to zero at the start of the
# game. At the beginning of each round, if the counter is greater than zero,
# defect, reduce the counter by one, and ignore the opponent's actions for the
# purpose of cooperation decisions. If the counter equals zero, cooperate only
# if the opponent was observed to cooperate in both of the previous two rounds;
# otherwise defect. If you intended to cooperate in any round $t$ and the
# opponent was observed to defect in the immediately following round $t+1$, set
# the punishment counter to three at the start of round $t+2$, replacing any
# existing counter value. Defect in rounds nine hundred ninety-nine and one
# thousand.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishment_counter = 0
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number in (1, 2, 999, 1000):
          return axl.Action.D
  
      if self._punishment_counter > 0:
          self._punishment_counter -= 1
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          action = axl.Action.C
      else:
          action = axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.D:
          self._punishment_counter = 3
  
      return action



#  Cooperate in the first two rounds. For rounds 3 through 999, first check if
# you defected in the previous round while your opponent cooperated; if this
# occurred, cooperate. Otherwise, defect only if your opponent defected in at
# least two of the previous three rounds; in all other cases, cooperate. Defect
# in round 1000.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if len(self.history) == 999:
          return axl.Action.D
  
      if len(self.history) >= 2:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
              return axl.Action.C
  
      recent_opponent_defections = opponent.history[-3:].count(axl.Action.D)
      if recent_opponent_defections >= 2:
          return axl.Action.D
  
      return axl.Action.C



#  Round 1: Cooperate. Round 2: Cooperate. For rounds 3 through 999: Cooperate
# unless the opponent defected in at least two of the previous three rounds, in
# which case defect. Round 1000: Defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number == 2:
          return axl.Action.C
  
      if round_number == 1000:
          return axl.Action.D
  
      recent_opponent_defections = opponent.history[-3:].count(axl.Action.D)
      if recent_opponent_defections >= 2:
          return axl.Action.D
  
      return axl.Action.C



#  Defect in rounds 1 and 2. For rounds 3 through 998, cooperate only if the
# opponent cooperated in both of the two immediately preceding rounds; otherwise
# defect. Defect in rounds 999 and 1000.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number in (1, 2, 999, 1000):
          return axl.Action.D
  
      if round_number >= 3 and round_number <= 998:
          if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.D



# Cooperate in rounds 1 and 2. For rounds 3 through 999, defect if the opponent
# defected in the previous round while you cooperated, or if the opponent
# defected in both of the previous two rounds; otherwise cooperate. Defect in
# round 1000.

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
  
      if round_number in (1, 2):
          return axl.Action.C
      if round_number == 1000:
          return axl.Action.D
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
              return axl.Action.D
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C



# Begin by cooperating in the first two rounds. For rounds 3 through 999, apply
# these conditions in order: if the opponent defected in both of the previous
# two rounds, defect; otherwise cooperate. In the final round, defect.

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
      if len(self.history) == 1:
          return axl.Action.C
      if len(self.history) == 999:
          return axl.Action.D
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



#  Round 1: Play Defect.  For rounds 2 through 999: Play Cooperate only if your
# opponent played Cooperate in the previous round; otherwise play Defect.  Round
# 1000: Play Defect.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



#  Cooperate in the first five rounds. For rounds six through one thousand,
# cooperate if the opponent cooperated in at least three of the last five
# rounds; otherwise defect.

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
  
      if len(self.history) < 5:
          return axl.Action.C
  
      return axl.Action.C if opponent.history[-5:].count(axl.Action.C) >= 3 else axl.Action.D



#  Cooperate in the first two rounds. For every subsequent round, examine your
# opponent’s actions in the previous three rounds. If the opponent defected in
# at least two of those three rounds, defect; otherwise, cooperate.

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
  
      recent_opponent = opponent.history[-3:]
      if recent_opponent.count(axl.Action.D) >= 2:
          return axl.Action.D
      return axl.Action.C



#  Begin by defecting. For rounds two through nine hundred ninety-eight, first
# infer your actual previous action using your previous intention and payoff: if
# you intended cooperation but received five or one, or intended defection but
# received three or zero, your action was flipped by noise; otherwise it matched
# your intention. Then, if your payoff was five or three, repeat that actual
# action; if your payoff was zero or one, switch to the opposite of that actual
# action. For rounds nine hundred ninety-nine and one thousand, defect
# unconditionally.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_last = axl.Action.D
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number >= 999:
          self._intended_last = axl.Action.D
          return axl.Action.D
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0] if False else None
      # Compute last-round payoff directly from the last completed round.
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
      last_payoff = my_last_score
  
      last_intended = self._intended_last
      last_actual = last_intended
      if (last_intended == axl.Action.C and last_payoff in (5, 1)) or (
          last_intended == axl.Action.D and last_payoff in (3, 0)
      ):
          last_actual = axl.Action.D if last_intended == axl.Action.C else axl.Action.C
  
      if last_payoff in (5, 3):
          intended = last_actual
      else:
          intended = axl.Action.D if last_actual == axl.Action.C else axl.Action.C
  
      self._intended_last = intended
      return intended



#  Begin by cooperating. For rounds 2 through 999, defect if the opponent
# defected in the previous round; otherwise cooperate. In round 1000, cooperate
# if the opponent cooperated in round 999, otherwise defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      return axl.Action.D if opponent.history[-1] == axl.Action.D else axl.Action.C



#  In rounds 1 through 990: Cooperate in round 1. For each subsequent round in
# this range, defect if the opponent defected in the immediately preceding round
# and you cooperated in that round; otherwise, cooperate. In rounds 991 through
# 1000: Always defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Begin by defecting. Determine the opponent's effective action by majority over
# the last two observed rounds; treat mixed results as defection. Thereafter,
# cooperate if the opponent effectively cooperated in the immediately preceding
# round; otherwise, defect. If you defected for two consecutive rounds while the
# opponent effectively cooperated in the second of those rounds, cooperate in
# the next round as reconciliation, then resume the conditional rule using the
# opponent's action in that reconciliation round. If the opponent effectively
# defected in the most recent round, continue defecting and disregard any
# reconciliation trigger.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._reconcile_next = False
          self._last_reconcile_index = None
          return axl.Action.D
  
      def effective_opponent_action() -> axl.Action:
          if len(opponent.history) == 0:
              return axl.Action.D
          if len(opponent.history) == 1:
              return opponent.history[-1]
          last_two = opponent.history[-2:]
          return axl.Action.C if last_two.count(axl.Action.C) == 2 else axl.Action.D
  
      # Reconciliation takes priority.
      if self._reconcile_next:
          self._reconcile_next = False
          self._last_reconcile_index = len(self.history)
          return axl.Action.C
  
      # If the opponent effectively defected most recently, keep defecting and ignore reconciliation triggers.
      if len(opponent.history) >= 1 and effective_opponent_action() == axl.Action.D:
          self._reconcile_next = False
          return axl.Action.D
  
      # Trigger reconciliation if we defected for two consecutive rounds and the opponent effectively cooperated
      # in the second of those rounds.
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.D, axl.Action.D]:
          if len(opponent.history) >= 2:
              second_of_two_effective = axl.Action.C if opponent.history[-2:] == [axl.Action.C, axl.Action.C] else axl.Action.D
              if second_of_two_effective == axl.Action.C:
                  self._reconcile_next = True
                  return axl.Action.C
  
      # Otherwise cooperate iff the opponent effectively cooperated in the immediately preceding round.
      return axl.Action.C if effective_opponent_action() == axl.Action.C else axl.Action.D



# In round 1, cooperate. In round 2, cooperate. In each round from 3 through
# 999, defect only if the opponent defected in both of the two immediately
# preceding rounds; otherwise, cooperate. In round 1000, defect.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if len(self.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              if len(self.history) == 999:
                  return axl.Action.D
              return axl.Action.D
  
      if len(self.history) == 999:
          return axl.Action.D
  
      return axl.Action.C



#  Cooperate in the first round. For rounds 2 through 999, choose your action
# based solely on the previous round's payoff: cooperate if the payoff was 1 or
# 3, defect if the payoff was 0 or 5. In round 1000, defect.

class Neutral_20(LLM_Strategy):
  n = 20
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_payoff = None
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(self.history) >= 1:
          self._last_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if self._last_payoff in (1, 3):
          return axl.Action.C
      if self._last_payoff in (0, 5):
          return axl.Action.D
  
      return axl.Action.C



# Round 1: Defect.  For each subsequent round, apply the first applicable rule:
# 1. If you played Defect and observed opponent Defect for three consecutive
# prior rounds: Cooperate. 2. If you observed opponent Defect in the immediately
# preceding round: Defect. 3. If you played Defect in the immediately preceding
# round and observed opponent Cooperate: Defect. 4. Otherwise: Cooperate.

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
  
      if len(self.history) >= 3:
          last3_self = self.history[-3:]
          last3_opp = opponent.history[-3:]
          if (
              last3_self.count(axl.Action.D) == 3
              and last3_opp.count(axl.Action.D) == 3
          ):
              return axl.Action.C
  
      if opponent.history and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if self.history and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.C



#  Cooperate in round 1. For each subsequent round through round 1000, cooperate
# unless the opponent's realized (observed) action was defection in both of the
# previous two rounds; if defecting under this condition, resume cooperation
# immediately once the opponent's realized action in the immediately preceding
# round was cooperation.

class Cooperative_21(LLM_Strategy):
  n = 21
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defecting = False
          return axl.Action.C
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              self._defecting = True
          elif opponent.history[-1] == axl.Action.C:
              self._defecting = False
  
      return axl.Action.D if self._defecting else axl.Action.C



# Cooperate in the first two rounds. For rounds three through nine hundred
# ninety-eight, cooperate unless the opponent defected in both of the two
# immediately preceding rounds. For rounds nine hundred ninety-nine and one
# thousand, defect regardless of the opponent’s actions.

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
  
      round_number = len(self.history) + 1
  
      if round_number <= 2:
          return axl.Action.C
  
      if round_number >= 999:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Defect in round one. For rounds two through nine hundred ninety-nine, examine
# the opponent’s executed actions across the previous two rounds. If the
# opponent cooperated in both of those rounds, cooperate. If you and the
# opponent both defected in both of those rounds, cooperate. In all other
# circumstances, defect. In round one thousand, defect unconditionally.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(opponent.history) < 2:
          return axl.Action.D
  
      opp_last_two = opponent.history[-2:]
      self_last_two = self.history[-2:]
  
      if opp_last_two == [axl.Action.C, axl.Action.C]:
          return axl.Action.C
  
      if self_last_two == [axl.Action.D, axl.Action.D] and opp_last_two == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      return axl.Action.D



# For round 1 and round 2, cooperate. For rounds 3 through 999, defect only if
# the opponent was observed to defect in the previous round and was also
# observed to defect two rounds ago, and you cooperated in the previous round;
# otherwise, cooperate. For round 1000, defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number in (1, 2):
          return axl.Action.C
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and len(self.history) >= 1:
          if (
              opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
              and self.history[-1] == axl.Action.C
          ):
              return axl.Action.D
  
      return axl.Action.C



#  Begin by intending to cooperate. For each round from 2 through 999: if your
# payoff in the previous round was 3 or 5, intend the same action you intended
# in that previous round; if your payoff was 0 or 1, intend the opposite action
# to the one you intended in that previous round. If you receive a payoff of 0
# in two consecutive rounds, intend to defect for all remaining rounds through
# round 999. In round 1000, intend to defect.

class Neutral_22(LLM_Strategy):
  n = 22
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.C
          self._two_consecutive_zeros = 0
          return self._intended_action
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          self._intended_action = axl.Action.D
          return self._intended_action
  
      if self._two_consecutive_zeros >= 2:
          self._intended_action = axl.Action.D
          return self._intended_action
  
      last_my_action = self.history[-1]
      last_my_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_my_score in (3, 5):
          self._intended_action = last_my_action
      elif last_my_score in (0, 1):
          self._intended_action = axl.Action.D if last_my_action == axl.Action.C else axl.Action.C
  
      if last_my_score == 0:
          self._two_consecutive_zeros += 1
      else:
          self._two_consecutive_zeros = 0
  
      return self._intended_action



# Begin by defecting. Thereafter, defect whenever you observed the opponent
# cooperating in the previous round. Also defect whenever you observed the
# opponent defecting in the previous round, unless you have observed mutual
# defection in the two previous consecutive rounds; in that specific case,
# cooperate in the next round. If you cooperate in this escape attempt and the
# opponent cooperates in response, continue cooperating until you observe the
# opponent defecting, at which point resume defecting. If the opponent defects
# in response to your escape attempt, resume defecting.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._escape_mode = False
          self._escape_waiting_for_response = False
          return axl.Action.D
  
      last_opp = opponent.history[-1]
      last_self = self.history[-1]
  
      # If we are in the escape phase, keep cooperating until the opponent defects.
      if getattr(self, "_escape_mode", False):
          if last_opp == axl.Action.D:
              self._escape_mode = False
              return axl.Action.D
          return axl.Action.C
  
      # If we just attempted escape and the opponent cooperated, continue cooperating.
      if getattr(self, "_escape_waiting_for_response", False):
          self._escape_waiting_for_response = False
          if last_opp == axl.Action.C:
              self._escape_mode = True
              return axl.Action.C
          return axl.Action.D
  
      # Default behavior: defect whenever opponent cooperated last round.
      if last_opp == axl.Action.C:
          return axl.Action.D
  
      # Opponent defected last round.
      # If the previous two rounds were mutual defection, attempt escape by cooperating.
      if len(self.history) >= 2:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and \
             self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              self._escape_waiting_for_response = True
              return axl.Action.C
  
      return axl.Action.D



# In round 1, cooperate. For rounds 2 through 990, cooperate unless the opponent
# defected in both of the previous two rounds; if you are currently defecting,
# continue until the opponent cooperates in two consecutive rounds, then resume
# cooperating. For rounds 991 through 1000, always defect.

class Cooperative_23(LLM_Strategy):
  n = 23
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
  
      if round_number >= 991:
          self._defecting = True
          return axl.Action.D
  
      if self._defecting:
          if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
              self._defecting = False
              return axl.Action.C
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._defecting = True
          return axl.Action.D
  
      return axl.Action.C



#  In round 1, cooperate. In round 2, cooperate. In rounds 3 through 999, defect
# only if the opponent appeared to defect in both of the previous two rounds;
# otherwise cooperate. In round 1000, defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number == 2:
          return axl.Action.C
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  Defect in rounds 999 and 1000 regardless of history. In all prior rounds,
# begin by defecting. Maintain a running count of how many times you received a
# payoff of 5 in the last four rounds; if this count reaches three or higher,
# cooperate, otherwise defect. If you intended to cooperate in the previous
# round and received a payoff of 0, immediately defect and reset the four-round
# count to zero.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_cooperate_prev = False
          self._last_four_payoffs = []
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number in (999, 1000):
          self._intended_cooperate_prev = False
          return axl.Action.D
  
      last_my_action = self.history[-1]
      last_opp_action = opponent.history[-1]
  
      if last_my_action == axl.Action.C and last_opp_action == axl.Action.D:
          last_payoff = 0
      elif last_my_action == axl.Action.D and last_opp_action == axl.Action.C:
          last_payoff = 5
      elif last_my_action == axl.Action.C and last_opp_action == axl.Action.C:
          last_payoff = 3
      else:
          last_payoff = 1
  
      self._last_four_payoffs.append(last_payoff)
      if len(self._last_four_payoffs) > 4:
          self._last_four_payoffs.pop(0)
  
      if self._intended_cooperate_prev and last_payoff == 0:
          self._last_four_payoffs = []
          self._intended_cooperate_prev = False
          return axl.Action.D
  
      count_fives = self._last_four_payoffs.count(5)
      if count_fives >= 3:
          self._intended_cooperate_prev = True
          return axl.Action.C
  
      self._intended_cooperate_prev = False
      return axl.Action.D



#  Begin by cooperating in round 1. For each round from 2 through 999, defect
# only if you cooperated in the previous round and the opponent defected in the
# previous round; otherwise, cooperate. In round 1000, defect.

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
  
      if round_number == 1000:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  In round 1, cooperate. In round 2, cooperate. In each round from 3 through
# 999, defect if the opponent's observed action was defection in both of the two
# immediately preceding rounds; otherwise cooperate. In round 1000, defect.

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
  
      if round_number == 2:
          return axl.Action.C
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



#  In the first round, choose Defect. In each subsequent round, condition your
# choice on your own intended choice from the previous round and the opponent's
# realized action from the previous round: if you chose Cooperate and the
# opponent realized Cooperate, choose Cooperate; if you chose Cooperate and the
# opponent realized Defect, choose Defect; if you chose Defect and the opponent
# realized Cooperate, choose Cooperate; if you chose Defect and the opponent
# realized Defect, choose Defect.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_intended_action = axl.Action.D
          return axl.Action.D
  
      last_opponent_action = opponent.history[-1]
      if self._last_intended_action == axl.Action.C:
          self._last_intended_action = axl.Action.C if last_opponent_action == axl.Action.C else axl.Action.D
      else:
          self._last_intended_action = axl.Action.C if last_opponent_action == axl.Action.C else axl.Action.D
  
      return self._last_intended_action



# Begin by cooperating. In each subsequent round prior to round 1000, if you
# defected in the previous round, cooperate; otherwise, cooperate unless the
# opponent defected in at least three of the last four rounds, in which case
# defect. In round 1000, defect.

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
  
      if round_number == 1000:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if len(opponent.history) >= 4 and opponent.history[-4:].count(axl.Action.D) >= 3:
          return axl.Action.D
  
      return axl.Action.C



# Cooperate in the first two rounds. For rounds 3 through 999, defect only if
# the opponent defected in both of the previous two rounds; otherwise cooperate.
# Defect in round 1000.

class Neutral_25(LLM_Strategy):
  n = 25
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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C