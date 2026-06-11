import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# 1. If it is the first 10 rounds, choose Cooperate to establish a baseline of
# mutual cooperation. 2. If the opponent has chosen Defect in at least two of
# the last three rounds, choose Defect to protect yourself and punish their
# defection. 3. If the current round number is a multiple of eight, choose
# Defect to aggressively exploit a cooperative opponent. 4. Otherwise, choose
# Cooperate to maintain the opponent's trust.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) < 10:
          return axl.Action.C
  
      if opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
  
      if len(self.history) % 8 == 0:
          return axl.Action.D
  
      return axl.Action.C



# 1. If the current round is 999 or 1000, play Defect. 2. If, over the last 10
# rounds, the opponent has defected at least two more times than you have, play
# Defect. 3. In all other cases, play Cooperate.

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
  
      round_number = len(self.history) + 1
  
      if round_number in (999, 1000):
          return axl.Action.D
  
      last_10_self = self.history[-10:]
      last_10_opp = opponent.history[-10:]
  
      self_defections = last_10_self.count(axl.Action.D)
      opp_defections = last_10_opp.count(axl.Action.D)
  
      if opp_defections >= self_defections + 2:
          return axl.Action.D
  
      return axl.Action.C



# 1. Cooperate in the first round. 2. From the second round to the 999th round:
# if the opponent cooperated in the previous round, cooperate; if the opponent
# defected in the previous round, cooperate with a 10% probability and defect
# with a 90% probability. 3. Defect in the 1000th round.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)



# Start by choosing Defect. On each subsequent round, determine your action by
# evaluating the following conditions in order:  1. If you chose to play
# Cooperate on the previous round specifically as a cooperation test, and the
# opponent cooperated, choose Defect to exploit their cooperation. 2. If you
# chose to play Cooperate on the previous round specifically as a cooperation
# test, and the opponent defected, choose Defect. 3. If the opponent has
# defected for the last three consecutive rounds, choose Cooperate to test for
# cooperation. 4. If the opponent cooperated on the previous round, choose
# Defect. 5. Otherwise, choose Defect.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._coop_test_last_round = False
          return axl.Action.D
  
      if self._coop_test_last_round:
          self._coop_test_last_round = False
          return axl.Action.D
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          self._coop_test_last_round = True
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.D



# Cooperate in the first round.  From the second round to the 999th round, apply
# the following conditions in order:  1. Consider the opponent's actions in the
# previous five rounds, or all previous rounds if fewer than five have been
# played. 2. If the opponent defected two or more times within this window,
# defect. 3. Otherwise, cooperate.  In the 1000th round, defect.

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
  
      if len(opponent.history) >= 5:
          window = opponent.history[-5:]
      else:
          window = opponent.history
  
      if window.count(axl.Action.D) >= 2:
          return axl.Action.D
  
      if len(self.history) == 999:
          return axl.Action.D
  
      return axl.Action.C



# Cooperate in the first round. In subsequent rounds, if both you and the
# opponent played defect in the previous round and the opponent cooperated in at
# least one of the last four rounds, cooperate. Otherwise, if the opponent
# defected in two or more of the last four rounds, defect. Otherwise, cooperate.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      last_four_opp = opponent.history[-4:]
      opp_defections_last_four = last_four_opp.count(axl.Action.D)
      opp_cooperated_last_four = last_four_opp.count(axl.Action.C) > 0
  
      if last_self == axl.Action.D and last_opp == axl.Action.D and opp_cooperated_last_four:
          return axl.Action.C
  
      if opp_defections_last_four >= 2:
          return axl.Action.D
  
      return axl.Action.C



# 1. In the first round, defect. 2. If the opponent's last observed action was
# cooperate, defect to exploit their cooperation. 3. If the opponent's last
# three observed actions were all defect, cooperate to attempt to break out of a
# mutual defection trap. 4. If the opponent's last observed action was defect
# but the previous three were not all defect, defect to treat the isolated
# defection as noise and avoid overreacting.

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
  
      opp_history = opponent.history
  
      if len(opp_history) >= 1 and opp_history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opp_history) >= 3 and opp_history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      if len(opp_history) >= 1 and opp_history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.D



# 1. Cooperate in the first round. 2. Defect on round 1000. 3. If the opponent
# cooperated in the previous round, cooperate. 4. If the opponent defected in
# the previous round, defect, unless you choose to forgive the defection and
# cooperate instead; apply this forgiveness with a 10% probability.

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
  
      if len(self.history) + 1 == 1000:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)



# 1. Cooperate in the first round. 2. Defect in the final two rounds (rounds 999
# and 1000). 3. If you cooperated and your opponent defected in the previous
# round, defect. 4. If you defected and your opponent cooperated in the previous
# round, and you cooperated and your opponent defected in the round before that,
# cooperate. 5. Otherwise, play the action your opponent played in the previous
# round.

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
  
      round_number = len(self.history) + 1
  
      if round_number >= 999:
          return axl.Action.D
  
      if len(self.history) >= 1:
          my_last = self.history[-1]
          opp_last = opponent.history[-1]
  
          if my_last == axl.Action.C and opp_last == axl.Action.D:
              return axl.Action.D
  
          if len(self.history) >= 2:
              my_prev = self.history[-2]
              opp_prev = opponent.history[-2]
              if (
                  my_last == axl.Action.D
                  and opp_last == axl.Action.C
                  and my_prev == axl.Action.C
                  and opp_prev == axl.Action.D
              ):
                  return axl.Action.C
  
          return opp_last
  
      return axl.Action.C



# 1. Play Defect for the first 10 rounds to test the opponent's behavior. 2.
# From round 11 to 989, track the opponent's actions over the preceding 10
# rounds. 3. If the opponent Cooperated in 7 or more of the preceding 10 rounds,
# identify them as a persistent cooperator and play Defect to exploit their
# cooperation. 4. If the opponent Cooperated in fewer than 7 of the preceding 10
# rounds, identify them as non-cooperative and play Defect to secure the
# guaranteed payoff and avoid exploitation. 5. In rounds 990 through 1000, play
# Defect unconditionally to exploit the finite horizon.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._window = 10
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number <= 10:
          return axl.Action.D
  
      if round_number >= 990:
          return axl.Action.D
  
      recent_opponent_moves = opponent.history[-10:]
      coop_count = recent_opponent_moves.count(axl.Action.C)
  
      if coop_count >= 7:
          return axl.Action.D
      else:
          return axl.Action.D



# 1. If there are 10 or fewer rounds remaining, play Defect. 2. If your previous
# action was Defect and the opponent's previous action was Cooperate, play
# Cooperate. 3. If the opponent's previous action was Defect, play Defect with
# 90% probability and Cooperate with 10% probability. 4. In all other cases,
# play Cooperate.

class Cooperative_4(LLM_Strategy):
  n = 4
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) >= 10 and len(opponent.history) >= 10:
          return axl.Action.D
  
      if not self.history:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return self._random.random_choice(0.1)
  
      return axl.Action.C



# 1. If it is the 1000th round, play Defect. 2. If fewer than three rounds have
# been played, play Defect if the opponent defected in all previous rounds;
# otherwise, play Cooperate. 3. If the opponent defected in both of the two
# immediately preceding rounds, play Defect. 4. If the opponent's actions in the
# three immediately preceding rounds were Defect, then Cooperate, then Defect,
# play Defect. 5. In all other cases, play Cooperate.

class Neutral_4(LLM_Strategy):
  n = 4
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 999:
          return axl.Action.D
  
      if len(self.history) < 3:
          if len(opponent.history) == 0 or all(move == axl.Action.D for move in opponent.history):
              return axl.Action.D
          return axl.Action.C
  
      if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
  
      if opponent.history[-3:] == [axl.Action.D, axl.Action.C, axl.Action.D]:
          return axl.Action.D
  
      return axl.Action.C



# 1. In the first round, intend to play Defect. 2. If you intended to play
# Defect in the previous round and the opponent played Cooperate, intend to play
# Defect. 3. If you intended to play Defect in the previous round and the
# opponent played Defect, intend to play Cooperate. 4. If you intended to play
# Cooperate in the previous round and the opponent played Cooperate, intend to
# play Defect. 5. If you intended to play Cooperate in the previous round and
# the opponent played Defect, and you did not intend to play Cooperate in the
# round before that, intend to play Cooperate. 6. If you intended to play
# Cooperate in the previous two consecutive rounds and the opponent played
# Defect in both, intend to play Defect.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_history = []
          return axl.Action.D
  
      intended_prev = self._intended_history[-1]
      opp_prev = opponent.history[-1]
  
      if intended_prev == axl.Action.D:
          if opp_prev == axl.Action.C:
              intended = axl.Action.D
          else:
              intended = axl.Action.C
      else:
          if opp_prev == axl.Action.C:
              intended = axl.Action.D
          else:
              if len(self._intended_history) >= 2 and self._intended_history[-2] == axl.Action.C:
                  intended = axl.Action.D
              else:
                  intended = axl.Action.C
  
      self._intended_history.append(intended)
      return intended



# 1. Cooperate on the first round. 2. On the second round, cooperate if the
# opponent cooperated in the first round; otherwise, defect. 3. On all
# subsequent rounds, cooperate if the opponent cooperated in both of the two
# immediately preceding rounds; otherwise, defect.

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
  
      if len(opponent.history) == 1:
          return axl.Action.C if opponent.history[0] == axl.Action.C else axl.Action.D
  
      return axl.Action.C if (
          opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C
      ) else axl.Action.D



# 1. Play Cooperate in the first round. 2. Play Defect in the last 10 rounds. 3.
# If the opponent has defected in at least 3 of the last 5 rounds, play Defect.
# 4. If both you and your opponent played Defect in the previous round, play
# Cooperate. 5. If your opponent played Defect and you played Cooperate in the
# previous round, play Defect. 6. If you played Defect and your opponent played
# Cooperate in the previous round, play Defect. 7. If both you and your opponent
# played Cooperate in the previous round, play Cooperate.

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
  
      rounds_played = len(self.history)
      if rounds_played >= 990:
          return axl.Action.D
  
      if len(opponent.history) >= 5 and opponent.history[-5:].count(axl.Action.D) >= 3:
          return axl.Action.D
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          my_last = self.history[-1]
          opp_last = opponent.history[-1]
  
          if my_last == axl.Action.D and opp_last == axl.Action.D:
              return axl.Action.C
          if my_last == axl.Action.C and opp_last == axl.Action.D:
              return axl.Action.D
          if my_last == axl.Action.D and opp_last == axl.Action.C:
              return axl.Action.D
          if my_last == axl.Action.C and opp_last == axl.Action.C:
              return axl.Action.C
  
      return axl.Action.C



# 1. Defect on the first round. 2. If the opponent cooperated in the previous
# round, defect to exploit them. 3. If the opponent defected in the previous
# round, defect to avoid the sucker's payoff. 4. If your intended defection was
# flipped to cooperation by noise, ignore the accidental cooperation and
# continue to defect, exploiting any trust the opponent may place in you as a
# result.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      return axl.Action.D



# 1. In the final two rounds, defect. 2. On the first round, cooperate. 3. If
# both you and the opponent defected in the previous round, cooperate. 4. If you
# defected and the opponent cooperated in the previous round, and the opponent
# defected two rounds ago, defect. 5. If you defected and the opponent
# cooperated in the previous round, and the opponent cooperated two rounds ago,
# cooperate. 6. If the opponent defected in the previous round, defect. 7.
# Otherwise, cooperate.  *(Assume the opponent cooperated prior to the first
# round for the purpose of evaluating condition 4).*

class Cooperative_6(LLM_Strategy):
  n = 6
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._opponent_prior = axl.Action.C
          self._opponent_two_ago = axl.Action.C
          return axl.Action.C
  
      if len(self.history) >= 998:
          return axl.Action.D
  
      prev_self = self.history[-1]
      prev_opp = opponent.history[-1]
      opp_two_ago = opponent.history[-2] if len(opponent.history) >= 2 else axl.Action.C
  
      if prev_self == axl.Action.D and prev_opp == axl.Action.D:
          return axl.Action.C
  
      if prev_self == axl.Action.D and prev_opp == axl.Action.C:
          if opp_two_ago == axl.Action.D:
              return axl.Action.D
          if opp_two_ago == axl.Action.C:
              return axl.Action.C
  
      if prev_opp == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. If the current round is 998, 999, or 1000, play Defect. 2. In the first
# round, play Cooperate. 3. In the second round, play Cooperate. 4. For all
# subsequent rounds, deduce the opponent's actions in the previous two rounds
# from your payoffs: a payoff of 3 or 5 means the opponent Cooperated, and a
# payoff of 0 or 1 means the opponent Defected. 5. If the opponent Cooperated in
# the previous round, play Cooperate. 6. If the opponent Defected in the
# previous round but Cooperated in the round before that, play Cooperate. 7. If
# the opponent Defected in both of the previous two rounds, play Defect.

class Neutral_6(LLM_Strategy):
  n = 6
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._deduced_opponent_actions = []
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number in (998, 999, 1000):
          return axl.Action.D
  
      if round_number == 2:
          return axl.Action.C
  
      def deduce_opponent_action(my_action: axl.Action, my_payoff: int) -> axl.Action:
          if my_payoff in (3, 5):
              return axl.Action.C
          return axl.Action.D
  
      if len(self._deduced_opponent_actions) < len(self.history):
          start = len(self._deduced_opponent_actions)
          for i in range(start, len(self.history)):
              my_action = self.history[i]
              my_payoff = self.total_scores(self.history[i:i + 1], opponent.history[i:i + 1])[0]
              self._deduced_opponent_actions.append(deduce_opponent_action(my_action, my_payoff))
  
      prev1 = self._deduced_opponent_actions[-1]
      prev2 = self._deduced_opponent_actions[-2]
  
      if prev1 == axl.Action.C:
          return axl.Action.C
      if prev1 == axl.Action.D and prev2 == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# 1. If it is the first round, play Cooperate. 2. If you played Defect in the
# previous round and the opponent played Cooperate in the previous round, play
# Defect to continue exploiting a pushover. 3. If you played Defect in the
# previous round, the opponent played Defect in the previous round, and the
# opponent played Cooperate in the round before the previous round, play
# Cooperate to apologize for your initiated Defection. 4. If the opponent played
# Defect in the previous round and the opponent played Defect in the round
# before the previous round, play Defect to retaliate against sustained
# defection. 5. If the opponent played Defect in the previous round and the
# opponent played Cooperate in the round before the previous round, play
# Cooperate to forgive isolated defections caused by noise. 6. If the current
# round number is a multiple of 20, play Defect to probe for exploitability. 7.
# Otherwise, play Cooperate.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number % 20 == 0:
          return axl.Action.D
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.D
  
      if len(self.history) >= 2 and my_last == axl.Action.D and opp_last == axl.Action.D and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opp_last == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opp_last == axl.Action.D and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C



# 1. On the first round, play Cooperate. 2. On the final two rounds, play
# Defect. 3. If your intended action on the previous round was Cooperate but it
# was flipped to Defect, play Cooperate to apologize. 4. Otherwise, if your
# opponent has played Defect in at least two of the last three rounds, play
# Defect. 5. Otherwise, play Cooperate.

class Cooperative_7(LLM_Strategy):
  n = 7
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      round_number = len(self.history) + 1
      if round_number > 998:
          self._intended_action = axl.Action.D
          return axl.Action.D
  
      if len(self.history) >= 1 and self._intended_action == axl.Action.C and self.history[-1] == axl.Action.D:
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      if opponent.history[-3:].count(axl.Action.D) >= 2:
          self._intended_action = axl.Action.D
          return axl.Action.D
  
      self._intended_action = axl.Action.C
      return axl.Action.C



# 1. Keep track of your chosen action each round and whether you are in an
# "apologetic" state. 2. Start in a "not apologetic" state and choose to
# cooperate on the first round. 3. If your chosen action in the previous round
# was Cooperate, but your executed action was Defect, enter the "apologetic"
# state. 4. If you are in the "apologetic" state, choose to cooperate; if both
# players executed Cooperate in the previous round, return to the "not
# apologetic" state. 5. If you are in the "not apologetic" state, copy the
# opponent's executed action from the previous round.

class Neutral_7(LLM_Strategy):
  n = 7
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._apologetic = False
          self._last_chosen = axl.Action.C
          return axl.Action.C
  
      if not hasattr(self, "_apologetic"):
          self._apologetic = False
      if not hasattr(self, "_last_chosen"):
          self._last_chosen = axl.Action.C
  
      if self._last_chosen == axl.Action.C and self.history[-1] == axl.Action.D:
          self._apologetic = True
  
      if self._apologetic:
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
              self._apologetic = False
          action = axl.Action.C
      else:
          action = opponent.history[-1]
  
      self._last_chosen = action
      return action



# Start by playing Defect in the first round. For all subsequent rounds, follow
# these conditions in order:  1. If both you and your opponent played Cooperate
# in the previous round, play Defect. 2. If you played Defect and your opponent
# played Cooperate in the previous round, play Defect. 3. If you played
# Cooperate and your opponent played Defect in the previous round, play Defect.
# 4. If both you and your opponent played Defect in the previous round, play
# Cooperate.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.D
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D



# 1. Cooperate in the first round. 2. If you defected and the opponent
# cooperated in the previous round, cooperate in the current round. 3. If you
# cooperated and the opponent defected in the previous round, defect with 90%
# probability and cooperate with 10% probability. 4. If both players cooperated
# in the previous round, cooperate in the current round. 5. If both players
# defected in the previous round, defect in the current round.

class Cooperative_8(LLM_Strategy):
  n = 8
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
  
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.C
  
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          return self._random.random_choice(0.1)
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
  
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. If the current round is 991 or greater, play Defect. 2. In the first two
# rounds, play Cooperate. 3. If both you and your opponent played Defect in the
# previous round, play Cooperate with a 30% probability and play Defect with a
# 70% probability. 4. If the opponent played Defect in both of the previous two
# rounds, play Defect. 5. If the opponent played Defect in exactly one of the
# previous two rounds, play Cooperate with a 20% probability and play Defect
# with an 80% probability. 6. In all other cases, play Cooperate.

class Neutral_8(LLM_Strategy):
  n = 8
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) >= 991:
          return axl.Action.D
  
      if self.first_round() or len(self.history) == 1:
          return axl.Action.C
  
      if len(self.history) >= 2:
          my_prev = self.history[-1]
          opp_prev = opponent.history[-1]
          opp_prev2 = opponent.history[-2]
  
          if my_prev == axl.Action.D and opp_prev == axl.Action.D:
              return self._random.random_choice(0.3)
  
          if opp_prev == axl.Action.D and opp_prev2 == axl.Action.D:
              return axl.Action.D
  
          if (opp_prev == axl.Action.D) != (opp_prev2 == axl.Action.D):
              return self._random.random_choice(0.2)
  
      return axl.Action.C



# 1. Start by defecting. 2. If you have probed twice and both probes resulted in
# the opponent defecting, always defect. 3. If the previous round was mutual
# cooperation, cooperate. 4. If the previous round resulted in you defecting and
# the opponent cooperating, and you probed within the last three rounds,
# cooperate. 5. If the previous round resulted in you defecting and the opponent
# cooperating, defect to exploit them. 6. If the previous round resulted in you
# cooperating and the opponent defecting, defect. 7. If the last fifteen
# consecutive rounds resulted in mutual defection, cooperate to probe for mutual
# cooperation. 8. Otherwise, defect.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._probe_count = 0
          self._probe_defect_count = 0
          self._last_probe_round = None
          return axl.Action.D
  
      round_num = len(self.history) + 1
  
      # Track probes: rounds where we cooperated after defecting in the previous round
      if len(self.history) >= 2:
          if self.history[-2] == axl.Action.D and self.history[-1] == axl.Action.C:
              self._probe_count += 1
              if opponent.history[-1] == axl.Action.D:
                  self._probe_defect_count += 1
              self._last_probe_round = round_num - 1
  
      # 2. If you have probed twice and both probes resulted in the opponent defecting, always defect.
      if self._probe_count >= 2 and self._probe_defect_count >= 2:
          return axl.Action.D
  
      # 3. If the previous round was mutual cooperation, cooperate.
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # 4. If the previous round resulted in you defecting and the opponent cooperating,
      # and you probed within the last three rounds, cooperate.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          if self._last_probe_round is not None and round_num - self._last_probe_round <= 3:
              return axl.Action.C
  
      # 5. If the previous round resulted in you defecting and the opponent cooperating, defect to exploit them.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      # 6. If the previous round resulted in you cooperating and the opponent defecting, defect.
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # 7. If the last fifteen consecutive rounds resulted in mutual defection,
      # cooperate to probe for mutual cooperation.
      if len(self.history) >= 15:
          last_15 = zip(self.history[-15:], opponent.history[-15:])
          if all(mine == axl.Action.D and theirs == axl.Action.D for mine, theirs in last_15):
              return axl.Action.C
  
      # 8. Otherwise, defect.
      return axl.Action.D



# 1. In the first round, cooperate. 2. If the opponent cooperated in the
# previous round, cooperate. 3. If the opponent defected in the previous round,
# cooperate with a 10% probability and defect with a 90% probability.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)



# 1. On the first round, intend to cooperate. 2. On the second round, if the
# opponent defected on the first round, intend to defect; otherwise, intend to
# cooperate. 3. On any subsequent round, if the opponent cooperated on the
# previous round, intend to cooperate. 4. If the opponent defected on the
# previous round but cooperated on the round before that, intend to cooperate.
# 5. If the opponent defected on the previous two rounds, intend to defect.

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
  
      if len(opponent.history) == 1:
          return axl.Action.D if opponent.history[-1] == axl.Action.D else axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Play Defect on the first round. 2. In the last 10 rounds, play Defect. 3.
# For rounds 2 and 3, if the opponent defected in the previous round, play
# Defect; otherwise, play Cooperate. 4. If both you and your opponent have
# played Defect in each of the previous 3 rounds, play Cooperate. 5. If the
# opponent has defected in at least 2 of the previous 3 rounds, play Defect. 6.
# If the opponent has cooperated in at least 2 of the previous 3 rounds, play
# Defect if the current round is a multiple of 10, otherwise play Cooperate.

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
      if round_number > 990:
          return axl.Action.D
  
      if round_number in (2, 3):
          return axl.Action.D if opponent.history[-1] == axl.Action.D else axl.Action.C
  
      if len(self.history) >= 3:
          last3_self = self.history[-3:]
          last3_opp = opponent.history[-3:]
  
          if last3_self.count(axl.Action.D) == 3 and last3_opp.count(axl.Action.D) == 3:
              return axl.Action.C
  
          if last3_opp.count(axl.Action.D) >= 2:
              return axl.Action.D
  
          if last3_opp.count(axl.Action.C) >= 2:
              return axl.Action.D if round_number % 10 == 0 else axl.Action.C
  
      return axl.Action.C



# Start by cooperating for the first round.   From the second round onwards,
# apply the following conditions in order:  1. If it is the final round, defect.
# 2. If both you and your opponent cooperated in the previous round, cooperate.
# 3. If you cooperated and your opponent defected in the previous round, defect.
# 4. If both you and your opponent defected in the previous round, cooperate. 5.
# If you defected and your opponent cooperated in the previous round:    - If
# you cooperated and your opponent defected in the round before that, defect.
# - Otherwise, cooperate.

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
  
      # Final round: defect.
      if len(self.history) >= 999:
          return axl.Action.D
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      # 2. If both cooperated in the previous round, cooperate.
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
  
      # 3. If you cooperated and your opponent defected in the previous round, defect.
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          return axl.Action.D
  
      # 4. If both defected in the previous round, cooperate.
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
  
      # 5. If you defected and your opponent cooperated in the previous round:
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          if len(self.history) >= 2 and self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
          return axl.Action.C
  
      return axl.Action.C



# 1. If it is the first round, play Cooperate. 2. If at least four rounds have
# been played and the opponent has defected in three or more of the last four
# rounds, play Defect. 3. If you played Defect in the previous round, play
# Cooperate. 4. If the opponent played Cooperate in the previous round, play
# Cooperate. 5. If the opponent played Defect in the previous round, play
# Defect.

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
  
      if len(self.history) >= 4 and opponent.history[-4:].count(axl.Action.D) >= 3:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Start by defecting. For every subsequent round, evaluate the following
# conditions in order to determine your action:  1. If your intended action in
# the previous round was cooperate and your opponent's observed action was
# defect, cooperate to prevent a noise-induced retaliation spiral. 2. If your
# opponent's observed action in the previous round was cooperate, defect to
# exploit their cooperation. 3. If your opponent's observed actions in the last
# three consecutive rounds were all defect, cooperate to probe for cooperation
# and escape mutual defection. 4. In all other cases, defect.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.D
          return axl.Action.D
  
      # Condition 1: If intended action in previous round was C and opponent observed D, cooperate.
      if getattr(self, "_intended_action", None) == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      # Condition 2: If opponent observed C in previous round, defect.
      if opponent.history[-1] == axl.Action.C:
          self._intended_action = axl.Action.D
          return axl.Action.D
  
      # Condition 3: If opponent observed D in last three consecutive rounds, cooperate.
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      # Condition 4: Otherwise defect.
      self._intended_action = axl.Action.D
      return axl.Action.D



# 1. In the first round, cooperate. 2. In the second round, cooperate. 3. From
# the third round to the nine hundred and ninety-ninth round, if the opponent
# defected in at least two of the previous three rounds, defect; otherwise,
# cooperate. 4. In the one thousandth round, defect.

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
  
      if len(self.history) == 999:
          return axl.Action.D
  
      recent_opponent = opponent.history[-3:]
      if recent_opponent.count(axl.Action.D) >= 2:
          return axl.Action.D
      return axl.Action.C



# 1. Cooperate on the first round. 2. Defect on the 1000th round. 3. If the
# previous round resulted in both players defecting, cooperate. 4. If the
# current round is 20 or greater, and the opponent defected in 5 or more of the
# last 20 rounds, defect. 5. If the opponent defected on the previous round,
# defect. 6. Otherwise, cooperate.

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
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if round_number >= 20 and opponent.history[-20:].count(axl.Action.D) >= 5:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. If you have previously played Cooperate in two consecutive rounds and the
# opponent played Defect in both of those rounds, play Defect for all remaining
# rounds. 2. In the first round, play Defect. 3. If the opponent played
# Cooperate in the previous round, play Defect. 4. If you played Cooperate in
# the previous round, and the opponent played Cooperate, play Defect. 5. If you
# played Cooperate in the previous round, and the opponent played Defect, play
# Cooperate. 6. If the opponent played Defect in the previous two consecutive
# rounds, play Cooperate. 7. In all other cases, play Defect.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._force_defect = False
          return axl.Action.D
  
      if getattr(self, "_force_defect", False):
          return axl.Action.D
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.C
              and self.history[-2] == axl.Action.C
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              self._force_defect = True
              return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D



# 1. If the current round is 998, 999, or 1000, play Defect. 2. If your intended
# action in the previous round was Defect, play Cooperate. 3. If the opponent
# played Defect in the previous round, play Defect, unless you choose to
# forgive; forgive the opponent's Defect with a 10% probability by playing
# Cooperate instead. 4. In all other cases, play Cooperate.

class Cooperative_12(LLM_Strategy):
  n = 12
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 998:
          intended = axl.Action.D
      elif getattr(self, "_intended_action", None) == axl.Action.D:
          intended = axl.Action.C
      elif opponent.history and opponent.history[-1] == axl.Action.D:
          intended = axl.Action.C if self._random.random_choice(0.1) == axl.Action.C else axl.Action.D
      else:
          intended = axl.Action.C
  
      self._intended_action = intended
      return intended



# 1. Cooperate on the first two rounds. 2. Defect on the final two rounds. 3. On
# the third round, defect if the opponent defected in both of the first two
# rounds; otherwise, cooperate. 4. On all remaining rounds, defect if the
# opponent defected in at least two of the previous three rounds; otherwise,
# cooperate.

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
  
      if round_number <= 2:
          return axl.Action.C
  
      if round_number >= 999:
          return axl.Action.D
  
      if round_number == 3:
          return axl.Action.D if opponent.history[-2:] == [axl.Action.D, axl.Action.D] else axl.Action.C
  
      return axl.Action.D if opponent.history[-3:].count(axl.Action.D) >= 2 else axl.Action.C



# Start the game by defecting. If the opponent cooperated in the previous round,
# cooperate. If the opponent defected in the previous round but cooperated in
# the round before that, cooperate. In all other situations, defect.

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
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# 1. Start by playing Cooperate in the first round. 2. If the current round is
# 999 or 1000, play Defect. 3. If the opponent has defected two or more times in
# the last three rounds, play Defect. 4. If the opponent defected in the
# previous round but cooperated in the round before that, play Cooperate. 5. If
# the opponent defected in the previous round, play Defect. 6. Otherwise, play
# Cooperate.

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
  
      round_number = len(self.history) + 1
  
      if round_number in (999, 1000):
          return axl.Action.D
  
      last_three = opponent.history[-3:]
      if last_three.count(axl.Action.D) >= 2:
          return axl.Action.D
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Cooperate in the first round. 2. Defect in the last round (round 1000). 3.
# In any other round, defect if your opponent defected in at least two of the
# previous three rounds. 4. Otherwise, cooperate if you intended to cooperate in
# the previous round and your opponent defected in the previous round. 5.
# Otherwise, cooperate.

class Neutral_13(LLM_Strategy):
  n = 13
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_last = axl.Action.C
          return axl.Action.C
  
      if len(self.history) >= 999:
          self._intended_last = axl.Action.D
          return axl.Action.D
  
      prev_three = opponent.history[-3:]
      if prev_three.count(axl.Action.D) >= 2:
          self._intended_last = axl.Action.D
          return axl.Action.D
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          if self._intended_last == axl.Action.C and opponent.history[-1] == axl.Action.D:
              self._intended_last = axl.Action.C
              return axl.Action.C
  
      self._intended_last = axl.Action.C
      return axl.Action.C



# Start by cooperating for the first 5 rounds. On round 6, defect. On rounds 7
# and 8, cooperate. If the opponent cooperated on both rounds 7 and 8, defect
# for all remaining rounds. Otherwise, for all remaining rounds, defect if the
# opponent has defected in at least 2 of the last 3 rounds, and cooperate
# otherwise.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._phase = 0
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number <= 5:
          return axl.Action.C
  
      if round_number == 6:
          return axl.Action.D
  
      if round_number in (7, 8):
          return axl.Action.C
  
      if round_number == 9:
          if opponent.history[-2:] == [axl.Action.C, axl.Action.C]:
              self._phase = 1
              return axl.Action.D
          self._phase = 2
  
      if getattr(self, "_phase", 0) == 1:
          return axl.Action.D
  
      if len(opponent.history) >= 3 and opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
      return axl.Action.C



# Play Cooperate in the first round. From the second round onward, apply the
# following conditions in order:  1. If the current round is 991 or later, play
# Defect. 2. If your intended action was Cooperate but your actual action was
# Defect in either of the previous two rounds, play Cooperate. 3. If the
# opponent played Defect in at least two of the previous three rounds, play
# Defect. 4. Otherwise, play Cooperate.

class Cooperative_14(LLM_Strategy):
  n = 14
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_history = []
          self._actual_history = []
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          intended = axl.Action.D
      else:
          if len(self._intended_history) >= 2:
              if (
                  self._intended_history[-1] == axl.Action.C and self._actual_history[-1] == axl.Action.D
              ) or (
                  self._intended_history[-2] == axl.Action.C and self._actual_history[-2] == axl.Action.D
              ):
                  intended = axl.Action.C
              elif opponent.history[-3:].count(axl.Action.D) >= 2:
                  intended = axl.Action.D
              else:
                  intended = axl.Action.C
          else:
              if opponent.history[-3:].count(axl.Action.D) >= 2:
                  intended = axl.Action.D
              else:
                  intended = axl.Action.C
  
      self._intended_history.append(intended)
  
      if len(self.history) > 0:
          self._actual_history.append(self.history[-1])
  
      return intended



# Cooperate in the first round. In subsequent rounds, if the opponent cooperated
# in the previous round, cooperate. If the opponent defected in the previous
# round, defect unless the opponent cooperated in the round before that, in
# which case cooperate.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# 1. If the opponent has defected for the last 3 consecutive rounds, defect. 2.
# If the opponent has cooperated for the last 10 consecutive rounds, defect. 3.
# If the opponent cooperated in the previous round and you defected, defect. 4.
# If both you and the opponent defected in the previous round, cooperate for the
# next two rounds. 5. If the opponent defected in the previous round and you
# cooperated, defect. 6. Otherwise, cooperate.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._cooperate_next_two = 0
          return axl.Action.C
  
      if getattr(self, "_cooperate_next_two", 0) > 0:
          self._cooperate_next_two -= 1
          return axl.Action.C
  
      opp_last_3 = opponent.history[-3:]
      if len(opp_last_3) == 3 and opp_last_3.count(axl.Action.D) == 3:
          return axl.Action.D
  
      opp_last_10 = opponent.history[-10:]
      if len(opp_last_10) == 10 and opp_last_10.count(axl.Action.C) == 10:
          return axl.Action.D
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          my_prev = self.history[-1]
          opp_prev = opponent.history[-1]
  
          if opp_prev == axl.Action.C and my_prev == axl.Action.D:
              return axl.Action.D
  
          if opp_prev == axl.Action.D and my_prev == axl.Action.C:
              return axl.Action.D
  
          if opp_prev == axl.Action.D and my_prev == axl.Action.D:
              self._cooperate_next_two = 2
              return axl.Action.C
  
      return axl.Action.C



# 1. Start with a cooperation counter at 0. 2. Cooperate on the first round. 3.
# After each round, update the counter based on the opponent's action: increase
# the counter by 1 if they cooperated (up to a maximum of 2), or decrease the
# counter by 2 if they defected (down to a minimum of -2). 4. From the second
# round to round 998, cooperate if the counter is greater than 0, and defect if
# the counter is 0 or less. 5. Defect on rounds 999 and 1000 regardless of the
# counter.

class Cooperative_15(LLM_Strategy):
  n = 15
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.coop_counter = 0
          return axl.Action.C
  
      last_opp_action = opponent.history[-1]
  
      if last_opp_action == axl.Action.C:
          self.coop_counter = min(2, self.coop_counter + 1)
      else:
          self.coop_counter = max(-2, self.coop_counter - 2)
  
      round_number = len(self.history) + 1
  
      if round_number >= 999:
          return axl.Action.D
  
      return axl.Action.C if self.coop_counter > 0 else axl.Action.D



# 1. Play Defect in rounds 996 through 1000. 2. Play Cooperate in round 1. 3.
# For rounds 2 through 995, apply the following conditions in order:    - If the
# opponent defected in at least three of the last ten rounds, play Defect.    -
# If your intended action in the previous round was Cooperate but your actual
# action was Defect, play Cooperate.    - Otherwise, play Cooperate.

class Neutral_15(LLM_Strategy):
  n = 15
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
  
      if round_number >= 996:
          self._intended_action = axl.Action.D
          return axl.Action.D
  
      if self._intended_action == axl.Action.C and self.history[-1] == axl.Action.D:
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      if len(opponent.history) >= 10 and opponent.history[-10:].count(axl.Action.D) >= 3:
          self._intended_action = axl.Action.D
          return axl.Action.D
  
      self._intended_action = axl.Action.C
      return axl.Action.C



# 1. In the first round, play Defect to exploit potential initial cooperation.
# 2. If the opponent played Cooperate in the previous round, play Defect to
# exploit their cooperation. 3. If the opponent played Defect in the previous
# round, play Defect to protect yourself from being exploited.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      return axl.Action.D



# 1. In the last 10 rounds, play Defect. 2. In the first round, play Cooperate.
# 3. If you played Cooperate in the previous round and the opponent played
# Defect in the previous round, play Defect. 4. If you played Defect in the
# previous round and the opponent played Defect two rounds ago, play Defect. 5.
# If you played Defect in the previous round, play Cooperate. 6. Otherwise, play
# Cooperate.

class Cooperative_16(LLM_Strategy):
  n = 16
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) >= 10:
          return axl.Action.D
  
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
              return axl.Action.D
  
      if len(self.history) >= 1 and len(opponent.history) >= 2:
          if self.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C



# 1. Defect on round 1000. 2. Cooperate on the first round. 3. From round 4
# onwards, if the opponent has defected in at least 3 of the last 4 rounds,
# defect. 4. If both players played the same action in the previous round,
# cooperate. 5. If the players played different actions in the previous round,
# defect.

class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forced_defect_round_1000 = True
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if round_number >= 4 and opponent.history[-4:].count(axl.Action.D) >= 3:
          return axl.Action.D
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
  
      return axl.Action.D



# For rounds 1 through 3, always cooperate. For rounds 4 through 990, count the
# number of times your opponent defected in the previous three rounds. If your
# opponent defected zero times, defect with a 15% probability and cooperate with
# an 85% probability. If your opponent defected exactly one time, cooperate with
# an 85% probability and defect with a 15% probability. If your opponent
# defected two or three times, defect with a 90% probability and cooperate with
# a 10% probability. For rounds 991 through 1000, always defect.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number <= 3:
          return axl.Action.C
  
      if round_number >= 991:
          return axl.Action.D
  
      recent_opponent_defections = opponent.history[-3:].count(axl.Action.D)
  
      if recent_opponent_defections == 0:
          return self._random.random_choice(0.85)
      elif recent_opponent_defections == 1:
          return self._random.random_choice(0.85)
      else:
          return self._random.random_choice(0.10)



# 1. Track your standing and your opponent's standing, which can be either
# "good" or "bad". Both players start in good standing.  2. In round 1000,
# defect.  3. In all other rounds, choose your action based on the current
# standings:    - If you are in bad standing, cooperate.    - If you are in good
# standing and your opponent is in bad standing, defect.    - If both you and
# your opponent are in good standing, cooperate.  4. After each round, deduce
# the executed actions from your payoff:    - A payoff of 3 or 0 means you
# cooperated; a payoff of 5 or 1 means you defected.    - A payoff of 3 or 5
# means your opponent cooperated; a payoff of 0 or 1 means your opponent
# defected.  5. Update the standings based on the executed actions and the
# standings before that round:    - If you were in bad standing and you
# cooperated, set your standing to good.    - If you were in bad standing and
# you defected, keep your standing as bad.    - If you were in good standing and
# you defected, set your standing to bad.    - If you were in good standing and
# you cooperated, keep your standing as good.    - If you were in bad standing,
# set your opponent's standing to good.    - If you were in good standing and
# your opponent defected, set your opponent's standing to bad.    - If you were
# in good standing and your opponent cooperated, set your opponent's standing to
# good.

class Cooperative_17(LLM_Strategy):
  n = 17
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.my_standing = "good"
          self.opp_standing = "good"
          return axl.Action.C
  
      if not hasattr(self, "my_standing"):
          self.my_standing = "good"
      if not hasattr(self, "opp_standing"):
          self.opp_standing = "good"
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          action = axl.Action.D
      else:
          if self.my_standing == "bad":
              action = axl.Action.C
          elif self.opp_standing == "bad":
              action = axl.Action.D
          else:
              action = axl.Action.C
  
      last_my_payoff, last_opp_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_my_payoff in (3, 0):
          my_executed = axl.Action.C
      else:
          my_executed = axl.Action.D
  
      if last_opp_payoff in (3, 5):
          opp_executed = axl.Action.C
      else:
          opp_executed = axl.Action.D
  
      prev_my_standing = self.my_standing
      prev_opp_standing = self.opp_standing
  
      if prev_my_standing == "bad":
          self.my_standing = "good" if my_executed == axl.Action.C else "bad"
      else:
          self.my_standing = "bad" if my_executed == axl.Action.D else "good"
  
      if prev_my_standing == "bad":
          self.opp_standing = "good"
      else:
          self.opp_standing = "bad" if opp_executed == axl.Action.D else "good"
  
      return action



# Start bycooperating in the first round. In the second round, cooperate if your
# first payoff was 3 or 5, and defect if your first payoff was 0 or 1. From the
# third round onwards, choose your action based on your payoffs from the
# previous two rounds according to the following conditions:  Cooperate if: 1.
# Your previous payoff was 3. 2. Your previous payoff was 5. 3. Your previous
# payoff was 0 and your payoff two rounds ago was 5.  Defect if: 1. Your
# previous payoff was 1. 2. Your previous payoff was 0 and your payoff two
# rounds ago was not 5.

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
          first_payoff = self.score
          return axl.Action.C if first_payoff in (3, 5) else axl.Action.D
  
      prev_payoff = self.score - self.total_scores(self.history[:-1], opponent.history[:-1])[0]
      prev2_payoff = self.score - self.total_scores(self.history[:-2], opponent.history[:-2])[0]
  
      if prev_payoff in (3, 5):
          return axl.Action.C
      if prev_payoff == 0 and prev2_payoff == 5:
          return axl.Action.C
      if prev_payoff == 1:
          return axl.Action.D
      if prev_payoff == 0 and prev2_payoff != 5:
          return axl.Action.D
  
      return axl.Action.D



# 1. In the first round, play Defect. 2. If the opponent played Cooperate in the
# previous round, play Defect. 3. If the opponent played Defect in the previous
# round but Cooperate in the round before that, play Cooperate. 4. In all other
# cases, play Defect.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# 1. In the first two rounds, cooperate. 2. From the third round to the 995th
# round, defect if the opponent defected in at least two of the previous three
# rounds; otherwise, cooperate. 3. From the 996th round to the 1000th round,
# defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number <= 2:
          return axl.Action.C
  
      if round_number >= 996:
          return axl.Action.D
  
      if len(opponent.history) < 3:
          return axl.Action.C
  
      recent_opponent_defections = opponent.history[-3:].count(axl.Action.D)
      if recent_opponent_defections >= 2:
          return axl.Action.D
      return axl.Action.C



# 1. If the current round is 996 or later, defect. 2. If the current round is 5
# or earlier, cooperate. 3. If the opponent cooperated in the previous round,
# cooperate. 4. If the opponent defected in the previous round, cooperate with a
# 15% probability and defect with an 85% probability.

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
  
      round_number = len(self.history) + 1
  
      if round_number >= 996:
          return axl.Action.D
  
      if round_number <= 5:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.15)



# Begin by defecting on the first round. Defect on every round that is a
# multiple of ten. On all other rounds, cooperate if the opponent cooperated in
# the previous round, or if the opponent defected in the previous round to
# apologize. If the opponent defects twice in a row, defect until they
# cooperate.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_until_cooperate = False
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number % 10 == 0:
          return axl.Action.D
  
      if self._punish_until_cooperate:
          if opponent.history[-1] == axl.Action.C:
              self._punish_until_cooperate = False
              return axl.Action.C
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._punish_until_cooperate = True
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C



# 1. Cooperate in the first round. 2. Defect in the final round (round 1000). 3.
# In the second round, defect if the opponent defected in the first round;
# otherwise, cooperate. 4. From the third to the 999th round, defect if the
# opponent defected in at least two of the three immediately preceding rounds;
# otherwise, cooperate.

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
          return axl.Action.D
  
      if round_number == 2:
          return axl.Action.D if opponent.history[-1] == axl.Action.D else axl.Action.C
  
      recent_opponent_moves = opponent.history[-3:]
      defections = recent_opponent_moves.count(axl.Action.D)
      return axl.Action.D if defections >= 2 else axl.Action.C



# 1. On the first round, cooperate. 2. On rounds 999 and 1000, defect. 3. If at
# least 20 rounds have been played and the opponent has defected in more than
# 20% of the previous rounds, defect. 4. If the payoff in the previous round was
# 3 or 5, play the same action you intended to play in the previous round. 5. If
# the payoff in the previous round was 0 or 1, play the opposite action of what
# you intended to play in the previous round.

class Neutral_19(LLM_Strategy):
  n = 19
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
  
      if round_number in (999, 1000):
          self._intended_action = axl.Action.D
          return axl.Action.D
  
      if len(opponent.history) >= 20:
          recent_opponent_defections = opponent.history[-20:].count(axl.Action.D)
          if recent_opponent_defections > 4:
              self._intended_action = axl.Action.D
              return axl.Action.D
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          my_last = self.history[-1]
          opp_last = opponent.history[-1]
  
          if my_last == axl.Action.C and opp_last == axl.Action.C:
              prev_payoff = 3
          elif my_last == axl.Action.C and opp_last == axl.Action.D:
              prev_payoff = 0
          elif my_last == axl.Action.D and opp_last == axl.Action.C:
              prev_payoff = 5
          else:
              prev_payoff = 1
  
          if prev_payoff in (3, 5):
              return self._intended_action
          if prev_payoff in (0, 1):
              self._intended_action = axl.Action.D if self._intended_action == axl.Action.C else axl.Action.C
              return self._intended_action
  
      self._intended_action = axl.Action.C
      return axl.Action.C



# 1. Defect on the first round. 2. If you defected and the opponent cooperated
# in the previous round, defect. 3. If you cooperated and the opponent defected
# in the previous round, defect. 4. If both players defected in the previous
# round, cooperate for the next two rounds if you defected and the opponent
# cooperated two rounds ago; otherwise, defect. 5. If both players cooperated in
# the previous round, defect if both players cooperated for the last five
# consecutive rounds; otherwise, cooperate.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._pending_cooperate_rounds = 0
          return axl.Action.D
  
      if getattr(self, "_pending_cooperate_rounds", 0) > 0:
          self._pending_cooperate_rounds -= 1
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.D
  
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          if len(self.history) >= 2 and self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.C:
              self._pending_cooperate_rounds = 1
              return axl.Action.C
          return axl.Action.D
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          if len(self.history) >= 5 and all(
              self.history[-i] == axl.Action.C and opponent.history[-i] == axl.Action.C
              for i in range(1, 6)
          ):
              return axl.Action.D
          return axl.Action.C
  
      return axl.Action.D



# 1. Cooperate in the first two rounds. 2. If the opponent defected in both of
# the previous two rounds, defect. 3. Otherwise, cooperate.

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
      if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
      return axl.Action.C



# Cooperate in the first round. Defect unconditionally in the last 10 rounds
# (rounds 991 through 1000). For all other rounds, evaluate the following
# conditions in order:  1. If both you and the opponent defected in the previous
# round, cooperate. 2. If the previous two rounds consisted of you cooperating
# and the opponent defecting, followed by you defecting and the opponent
# cooperating, defect. 3. If the opponent defected in the previous round,
# defect. 4. Otherwise, cooperate.

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
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      if len(self.history) >= 1:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
  
      if len(self.history) >= 2:
          if (
              self.history[-2] == axl.Action.C
              and opponent.history[-2] == axl.Action.D
              and self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.C
          ):
              return axl.Action.D
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. In the first round, cooperate to establish a baseline for interaction. 2.
# If the opponent cooperated in the previous round, defect to aggressively
# exploit their cooperation for the maximum possible payoff. 3. If the opponent
# defected in the previous round, cooperate to forgive potential noise, prevent
# a mutual defection lock-in, and attempt to restore mutual cooperation.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
      else:
          return axl.Action.C



# 1. Cooperate in the first two rounds. 2. Defect on round 1000. 3. From the
# third round onwards, if the opponent cooperated two rounds ago and defected in
# the previous round, and I intended to cooperate two rounds ago, cooperate in
# the current round to apologize for potential noise. 4. If the opponent
# defected in at least two of the three immediately preceding rounds, defect. 5.
# Otherwise, cooperate.

class Cooperative_21(LLM_Strategy):
  n = 21
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_history = []
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number == 2:
          self._intended_history.append(axl.Action.C)
          return axl.Action.C
  
      if round_number == 1000:
          self._intended_history.append(axl.Action.D)
          return axl.Action.D
  
      if (
          len(opponent.history) >= 2
          and opponent.history[-2] == axl.Action.C
          and opponent.history[-1] == axl.Action.D
          and len(self._intended_history) >= 2
          and self._intended_history[-2] == axl.Action.C
      ):
          self._intended_history.append(axl.Action.C)
          return axl.Action.C
  
      if len(opponent.history) >= 3 and opponent.history[-3:].count(axl.Action.D) >= 2:
          self._intended_history.append(axl.Action.D)
          return axl.Action.D
  
      self._intended_history.append(axl.Action.C)
      return axl.Action.C



# Cooperate in the first round. In subsequent rounds, evaluate the following
# conditions in order:  1. If your intended action in the previous round was to
# cooperate, but your actual action was flipped to defect due to noise, play
# cooperate in the current round to apologize. 2. If the opponent cooperated in
# at least 8 of the last 10 actual rounds, play cooperate. If fewer than 10
# rounds have occurred, evaluate all actual rounds played so far. 3. Otherwise,
# play defect.

class Neutral_21(LLM_Strategy):
  n = 21
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_last = axl.Action.C
          return axl.Action.C
  
      # Condition 1: apologize if we intended to cooperate last round,
      # but our actual action was flipped to defect.
      if getattr(self, "_intended_last", None) == axl.Action.C and self.history[-1] == axl.Action.D:
          self._intended_last = axl.Action.C
          return axl.Action.C
  
      # Condition 2: cooperate if opponent cooperated in at least 8 of the last 10 actual rounds.
      recent_opponent_history = opponent.history[-10:]
      if recent_opponent_history.cooperations >= 8:
          self._intended_last = axl.Action.C
          return axl.Action.C
  
      # Otherwise defect.
      self._intended_last = axl.Action.D
      return axl.Action.D



# 1. Cooperate on the first round. 2. If the opponent has defected in the last
# ten consecutive rounds, defect. 3. If the previous round was mutual defection,
# cooperate. 4. If the previous round was mutual cooperation, defect if you have
# chosen to cooperate for the last four consecutive rounds; otherwise,
# cooperate. 5. Otherwise, defect.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._coop_streak = 0
          return axl.Action.C
  
      if len(opponent.history) >= 10 and opponent.history[-10:].count(axl.Action.D) == 10:
          return axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          coop_streak = 0
          for move in reversed(self.history):
              if move == axl.Action.C:
                  coop_streak += 1
              else:
                  break
          if coop_streak >= 4:
              return axl.Action.D
          return axl.Action.C
  
      return axl.Action.D



# 1. If it is the first round, cooperate. 2. If your payoff in the previous
# round was 3 or 1, cooperate. 3. If your payoff in the previous round was 5 or
# 0, defect.

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
  
      last_score = self.score - self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_score in (3, 1):
          return axl.Action.C
      if last_score in (5, 0):
          return axl.Action.D
  
      return axl.Action.C



# 1. In the first round, cooperate. 2. In rounds 991 through 1000, defect. 3. In
# rounds that are multiples of 10 and are before round 991, defect. 4. If the
# opponent defected in the previous round, defect only if the opponent also
# defected in at least one of the two rounds prior to that; otherwise,
# cooperate. 5. If the opponent cooperated in the previous round, cooperate.

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
  
      round_number = len(self.history) + 1
  
      if 991 <= round_number <= 1000:
          return axl.Action.D
  
      if round_number < 991 and round_number % 10 == 0:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          if len(opponent.history) >= 3 and (
              opponent.history[-2] == axl.Action.D or opponent.history[-3] == axl.Action.D
          ):
              return axl.Action.D
          return axl.Action.C
  
      return axl.Action.C



# 1. Play Defect for the first 50 rounds. 2. If the opponent cooperated in at
# least 40 of the last 50 rounds, play Defect for the next 50 rounds, then
# repeat this step. 3. Otherwise, play Cooperate for the next 10 rounds. 4. If
# the opponent cooperated in at least 7 of those 10 rounds, play Cooperate for
# the next 40 rounds, then return to step 1. 5. Otherwise, play Defect for the
# next 40 rounds, then return to step 1.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._phase = 1
          self._phase_remaining = 50
          self._check_window = 50
          self._check_threshold = 40
          return axl.Action.D
  
      if self._phase_remaining is None:
          self._phase = 1
          self._phase_remaining = 50
          self._check_window = 50
          self._check_threshold = 40
  
      if self._phase == 1:
          action = axl.Action.D
      elif self._phase == 2:
          action = axl.Action.D
      elif self._phase == 3:
          action = axl.Action.C
      elif self._phase == 4:
          action = axl.Action.C
      else:
          action = axl.Action.D
  
      self._phase_remaining -= 1
  
      if self._phase_remaining == 0:
          if self._phase == 1:
              recent = opponent.history[-50:]
              if recent.count(axl.Action.C) >= 40:
                  self._phase = 2
                  self._phase_remaining = 50
                  self._check_window = 50
                  self._check_threshold = 40
              else:
                  self._phase = 3
                  self._phase_remaining = 10
                  self._check_window = 10
                  self._check_threshold = 7
          elif self._phase == 2:
              self._phase = 1
              self._phase_remaining = 50
              self._check_window = 50
              self._check_threshold = 40
          elif self._phase == 3:
              recent = opponent.history[-10:]
              if recent.count(axl.Action.C) >= 7:
                  self._phase = 4
                  self._phase_remaining = 40
                  self._check_window = 40
                  self._check_threshold = None
              else:
                  self._phase = 5
                  self._phase_remaining = 40
                  self._check_window = 40
                  self._check_threshold = None
          elif self._phase == 4:
              self._phase = 1
              self._phase_remaining = 50
              self._check_window = 50
              self._check_threshold = 40
          elif self._phase == 5:
              self._phase = 1
              self._phase_remaining = 50
              self._check_window = 50
              self._check_threshold = 40
  
      return action



# 1. Cooperate in the first two rounds. 2. If your chosen action in the previous
# round was cooperate but your executed action was flipped to defect, cooperate
# in the current round to show contrition. 3. If the opponent defected in both
# of the previous two rounds, defect in the current round. 4. In all other
# cases, cooperate.

class Cooperative_23(LLM_Strategy):
  n = 23
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._contrite = False
          return axl.Action.C
  
      if len(self.history) == 1:
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
              self._contrite = True
              return axl.Action.C
          self._contrite = False
          return axl.Action.C
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._contrite = True
          return axl.Action.C
  
      if getattr(self, "_contrite", False):
          self._contrite = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Play Cooperate in the first round.  Play Defect in the final round (round
# 1000).  If your payoff in the previous round was 5, play Cooperate.  If the
# opponent's observed actions in two of the last three rounds were Defect, play
# Defect.  Otherwise, play Cooperate.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if len(self.history) >= 1:
          last_self, last_opp = self.total_scores(self.history[-1:], opponent.history[-1:])
          if last_self == 5:
              return axl.Action.C
  
      if len(opponent.history) >= 3 and opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
  
      return axl.Action.C



# 1. On the first round, defect. 2. If the opponent has defected at least twice
# in the last three rounds, defect. 3. If you defected on the previous round and
# the opponent has cooperated at least twice in the last three rounds,
# cooperate. 4. Otherwise, defect.

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
  
      last_three_opponent = opponent.history[-3:]
      last_three_self = self.history[-3:]
  
      if last_three_opponent.count(axl.Action.D) >= 2:
          return axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D and last_three_opponent.count(axl.Action.C) >= 2:
          return axl.Action.C
  
      return axl.Action.D



# 1. If the current round is 991 or later, defect. 2. If it is the first round,
# cooperate. 3. Otherwise, count the number of times the opponent defected in
# the previous 10 rounds, or all previous rounds if fewer than 10 have occurred.
# 4. If the opponent defected 3 or more times in this count, defect. 5. If the
# opponent defected fewer than 3 times in this count, cooperate.

class Cooperative_24(LLM_Strategy):
  n = 24
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) >= 991:
          return axl.Action.D
  
      if self.first_round():
          return axl.Action.C
  
      recent_opponent_defections = opponent.history[-10:].count(axl.Action.D)
      if recent_opponent_defections >= 3:
          return axl.Action.D
      return axl.Action.C



# 1. Cooperate in the first two rounds. 2. From the third round to the 990th
# round:    - If the opponent cooperated in the previous round, cooperate.    -
# If the opponent defected in the previous round, defect with a 90% probability
# and cooperate with a 10% probability.    - However, if the opponent's actions
# in the previous three rounds were Defect, Cooperate, and Defect, always
# defect. 3. From the 991st round to the 1000th round, always defect.

class Neutral_24(LLM_Strategy):
  n = 24
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
  
      if len(opponent.history) >= 3:
          last_three = opponent.history[-3:]
          if last_three == [axl.Action.D, axl.Action.C, axl.Action.D]:
              return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)



# 1. Play Defect on the first round. 2. If the opponent played Cooperate in the
# previous round, play Defect to exploit their cooperation. 3. If you and the
# opponent have both played Defect in each of the previous ten consecutive
# rounds, play Cooperate to test if the opponent can be lured into cooperating.
# 4. In all other cases, play Defect.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if opponent.history and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(self.history) >= 10 and len(opponent.history) >= 10:
          last_self = self.history[-10:]
          last_opp = opponent.history[-10:]
          if all(a == axl.Action.D for a in last_self) and all(a == axl.Action.D for a in last_opp):
              return axl.Action.C
  
      return axl.Action.D



# Cooperate on the first round. For every subsequent round, apply the following
# conditions in order:  1. If it is the final round (round 1000), defect. 2. If
# your actual action in the previous round was Defect but your intended action
# was Cooperate, cooperate. 3. If the opponent's action in the previous round
# was Defect, defect. 4. Otherwise, cooperate.

class Cooperative_25(LLM_Strategy):
  n = 25
  attitude = Attitude.COOPERATIVE
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
  
      if len(self.history) >= 1:
          prev_actual = self.history[-1]
          prev_intended = getattr(self, "_intended_action", prev_actual)
  
          if prev_actual == axl.Action.D and prev_intended == axl.Action.C:
              self._intended_action = axl.Action.C
              return axl.Action.C
  
          if opponent.history[-1] == axl.Action.D:
              self._intended_action = axl.Action.D
              return axl.Action.D
  
      self._intended_action = axl.Action.C
      return axl.Action.C



# 1. Cooperate in the first round.  2. In each subsequent round, evaluate the
# following conditions in order, using your intended action and the opponent's
# executed action:     - If the opponent executed a cooperation in the previous
# round, cooperate.     - If the opponent executed a defection in the previous
# round:      - If you intended a defection in the previous round, and the
# opponent executed a cooperation in at least half of the previous 10 rounds (or
# all previous rounds if fewer than 10 have been played), cooperate.      - If
# you intended a defection in the previous round, and the opponent executed a
# cooperation in less than half of the previous 10 rounds, defect.      - If you
# intended a cooperation in the previous round, and the opponent also executed a
# defection in the round prior to that, defect.      - Otherwise, cooperate.

class Neutral_25(LLM_Strategy):
  n = 25
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_intended_action = axl.Action.C
          return axl.Action.C
  
      prev_opp = opponent.history[-1]
      prev_self_intended = getattr(self, "_last_intended_action", axl.Action.C)
  
      def coop_rate_last_n(n: int) -> float:
          opp_hist = opponent.history[-n:] if len(opponent.history) >= n else opponent.history[:]
          if len(opp_hist) == 0:
              return 1.0
          return opp_hist.count(axl.Action.C) / len(opp_hist)
  
      if prev_opp == axl.Action.C:
          action = axl.Action.C
      else:
          if prev_self_intended == axl.Action.D:
              rate = coop_rate_last_n(10)
              action = axl.Action.C if rate >= 0.5 else axl.Action.D
          elif len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
              action = axl.Action.D
          else:
              action = axl.Action.C
  
      self._last_intended_action = action
      return action