import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# 1. Play Defect in the first round. 2. If the opponent played Cooperate in the
# previous round, play Defect to exploit their cooperation. 3. If the opponent
# played Defect in the previous round, play Defect to protect yourself, unless
# the opponent has defected for the last three consecutive rounds and you played
# Defect in the previous round, in which case play Cooperate to test if they
# will reciprocate.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._test_cooperate = False
          return axl.Action.D
  
      if len(opponent.history) >= 3:
          last_three_opponent_defections = opponent.history[-3:].count(axl.Action.D) == 3
      else:
          last_three_opponent_defections = False
  
      if (
          last_three_opponent_defections
          and len(self.history) >= 1
          and self.history[-1] == axl.Action.D
      ):
          self._test_cooperate = True
          return axl.Action.C
  
      self._test_cooperate = False
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.D



# 1. Play Cooperate in the first round. 2. Play Cooperate in the second round.
# 3. From the third round onwards, play Defect if the opponent played Defect in
# both of the two immediately preceding rounds; otherwise, play Cooperate.

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



# 1. Cooperate on the first two rounds. 2. From the third round onward, defect
# if the opponent defected in both of the previous two rounds. 3. Cooperate in
# all other cases.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Play Defect in the first round. 2. If the opponent played Cooperate in the
# previous round, play Defect. 3. If the opponent played Defect in the previous
# round, and you played Defect, play Cooperate. 4. If the opponent played Defect
# in the previous round, and you played Cooperate, play Defect in all subsequent
# rounds until the opponent plays Cooperate.

class Aggressive_2(LLM_Strategy):
  n = 2
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
          if opponent.history[-1] == axl.Action.C:
              self._force_defect = False
              return axl.Action.D
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          if self.history[-1] == axl.Action.D:
              return axl.Action.C
          else:
              self._force_defect = True
              return axl.Action.D
  
      return axl.Action.D



# 1. Play Cooperate in the first round. 2. Play Cooperate in the second round.
# 3. From the third round onwards, play Defect if the opponent's observed
# actions in both of the previous two rounds were Defect; otherwise, play
# Cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. If it is the first round, cooperate. 2. If the opponent defected in both of
# the previous two consecutive rounds, defect. 3. Otherwise, cooperate.

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



# 1. On the first round, defect. 2. If the opponent cooperated in the previous
# round, defect. 3. If the opponent defected in the previous round and
# cooperated in the round before that, cooperate. 4. Otherwise, defect.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Start by playing Cooperate.   In every subsequent round, base your action on
# your payoff in the previous round:  1. If you scored 3, play Cooperate. 2. If
# you scored 5, play Cooperate. 3. If you scored 0, play Defect. 4. If you
# scored 1, play Cooperate.

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
  
      last_my_score = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_my_score in (3, 5, 1):
          return axl.Action.C
      if last_my_score == 0:
          return axl.Action.D
  
      return axl.Action.C



# 1. In the first round, cooperate. 2. If you intended to cooperate in the
# previous round but your action was flipped to defect, cooperate in the current
# round. 3. If you intended to cooperate two rounds ago but your action was
# flipped to defect, and your opponent defected in the previous round, cooperate
# in the current round. 4. Otherwise, cooperate if your opponent cooperated in
# the previous round, and defect if your opponent defected in the previous
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
  
      if len(self.history) >= 1:
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
  
      if len(self.history) >= 2:
          if self.history[-2] == axl.Action.C and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
  
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# 1. Play Defect on the first round. 2. If the opponent played Cooperate in the
# previous round, play Defect. 3. If the opponent played Defect in the previous
# round, play Cooperate with a 10% probability and Defect with a 90%
# probability.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      return self._random.random_choice(0.1)



# Intend to cooperate on the first round. In all subsequent rounds, determine
# your intended action based on your payoff in the previous round as follows:
# Intend to cooperate if: - Your payoff was 3. - Your payoff was 1.  Intend to
# defect if: - Your payoff was 5. - Your payoff was 0.

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
  
      last_score = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_score in (3, 1):
          return axl.Action.C
      if last_score in (5, 0):
          return axl.Action.D
  
      return axl.Action.C



# Cooperate in the first round. In each subsequent round, cooperate if you and
# your opponent played the same action in the previous round. Defect if you and
# your opponent played different actions in the previous round.

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
  
      return axl.Action.C if self.history[-1] == opponent.history[-1] else axl.Action.D



# 1. Begin by defecting. 2. If the opponent cooperated in the previous round,
# defect. 3. If the opponent defected in the previous round, cooperate for
# exactly two consecutive rounds. 4. If the opponent defects on the second round
# of your cooperation, defect permanently for the remainder of the game. 5. If
# the opponent cooperates on the second round of your cooperation, return to
# defecting.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._coop_streak = 0
          self._permanent_defect = False
          return axl.Action.D
  
      if getattr(self, "_permanent_defect", False):
          return axl.Action.D
  
      last_opp = opponent.history[-1]
  
      if self._coop_streak == 0:
          if last_opp == axl.Action.D:
              self._coop_streak = 1
              return axl.Action.C
          return axl.Action.D
  
      if self._coop_streak == 1:
          if last_opp == axl.Action.D:
              self._permanent_defect = True
              self._coop_streak = 0
              return axl.Action.D
          self._coop_streak = 0
          return axl.Action.D
  
      self._coop_streak = 0
      return axl.Action.D



# 1. If it is the first or second round, play Cooperate. 2. If the opponent
# played Defect in both of the two immediately preceding rounds, play Defect. 3.
# In all other cases, play Cooperate.

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
  
      if len(self.history) < 2 or len(opponent.history) < 2:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Play Cooperate in the first round. 2. In the second round, play Cooperate.
# 3. From the third round onward, play Defect if the opponent played Defect in
# both of the immediately preceding two rounds. 4. In all other cases, play
# Cooperate.

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



# 1. On the first round, defect. 2. If the opponent cooperated in the previous
# round, defect. 3. If the opponent defected in the previous round, cooperate
# only if the opponent cooperated two rounds ago; otherwise, defect.

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
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Cooperate on the first two rounds. Starting from the third round, defect if
# the opponent defected in both of the previous two rounds. In all other
# situations, cooperate.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# Start by cooperating in the first round. Continue cooperating in rounds 2 and
# 3 regardless of the opponent's actions. From round 4 onward, examine the
# opponent's last 3 actions. If the opponent cooperated in at least 2 of those 3
# rounds, cooperate. If the opponent cooperated in fewer than 2 of those 3
# rounds, defect.

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
  
      if len(opponent.history) < 3:
          return axl.Action.C
  
      last_three = opponent.history[-3:]
      if last_three.count(axl.Action.C) >= 2:
          return axl.Action.C
      return axl.Action.D



# 1. Begin the game by defecting. 2. If the opponent cooperated in the previous
# round, defect to exploit them. 3. If the opponent defected in the previous
# round but cooperated at least once in the last three rounds, defect, treating
# their recent defection as noise. 4. If the opponent has defected for three
# consecutive rounds, cooperate for exactly one round to probe for cooperation,
# then immediately return to defecting. 5. In the final five rounds, always
# defect.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._probe_next = False
          return axl.Action.D
  
      if len(self.history) < 5:
          recent_opp = opponent.history[-3:]
          if len(recent_opp) >= 3 and recent_opp.count(axl.Action.D) == 3:
              self._probe_next = True
              return axl.Action.C
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.D
          if axl.Action.C in opponent.history[-3:]:
              return axl.Action.D
          return axl.Action.D
  
      if len(self.history) >= 995:
          return axl.Action.D
  
      if getattr(self, "_probe_next", False):
          self._probe_next = False
          return axl.Action.D
  
      recent_opp = opponent.history[-3:]
      if len(recent_opp) >= 3 and recent_opp.count(axl.Action.D) == 3:
          self._probe_next = True
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if axl.Action.C in opponent.history[-3:]:
          return axl.Action.D
  
      return axl.Action.D



# 1. Play Cooperate on the first two rounds. 2. Starting from the third round,
# if the opponent played Defect in both of the two immediately preceding rounds,
# play Defect. 3. Otherwise, play Cooperate.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# Start by cooperating on the first round. On every subsequent round, base your
# action on the opponent's previous action. If the opponent cooperated in the
# previous round, cooperate in the current round. If the opponent defected in
# the previous round, cooperate with a probability of 30 percent and defect with
# a probability of 70 percent.

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
  
      last_opponent_action = opponent.history[-1]
  
      if last_opponent_action == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.3)



# This strategy aggressively maximizes your payoff by defaulting to defection,
# exploiting any opponent cooperation, and only cooperating as a calculated lure
# to restart exploitation against opponents who have stopped cooperating but
# have shown a willingness to cooperate in the past.  Follow these conditions in
# order:  1. If it is the first round, play Defect. 2. If the opponent played
# Cooperate in the previous round, play Defect. 3. If the opponent has played
# Defect for the last 10 consecutive rounds, and they played Cooperate at least
# once earlier in the game, play Cooperate. 4. In all other cases, play Defect.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opponent.history) >= 10:
          last_10 = opponent.history[-10:]
          if last_10.count(axl.Action.D) == 10 and opponent.history.cooperations > 0:
              return axl.Action.C
  
      return axl.Action.D



# 1. Cooperate on the first round. 2. Cooperate on the second round. 3. On any
# round from the third onwards, if the opponent defected in both of the previous
# two rounds, defect. 4. Otherwise, cooperate.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# 1. Cooperate in the first round. 2. If the opponent cooperated in the previous
# round, cooperate in the current round. 3. If the opponent defected in the
# previous round, cooperate with a 10% probability and defect with a 90%
# probability.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)



# 1. On the first round, play Defect. 2. If the opponent played Cooperate in the
# previous round, play Defect. 3. If the opponent played Defect in the previous
# round, play Defect, unless the opponent has played Defect in each of the last
# three consecutive rounds, in which case play Cooperate.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      return axl.Action.D



# 1. Cooperate for the first ten rounds. 2. From the eleventh round onwards,
# evaluate the opponent's actions in the previous ten rounds. 3. If the opponent
# cooperated in at least seven of those ten rounds, cooperate in the current
# round. 4. Otherwise, defect in the current round.

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
  
      if len(self.history) < 10:
          return axl.Action.C
  
      recent_opponent_moves = opponent.history[-10:]
      if recent_opponent_moves.count(axl.Action.C) >= 7:
          return axl.Action.C
      return axl.Action.D



# 1. If it is the first round, cooperate. 2. If the opponent defected in both of
# the two immediately preceding rounds, defect. 3. Otherwise, cooperate.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. If it is the first round, defect. 2. If the opponent cooperated in the
# previous round, defect. 3. If the opponent has defected in the previous three
# consecutive rounds, cooperate. 4. Otherwise, defect.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      return axl.Action.D



# 1. Cooperate in the first round. 2. Defect if the opponent defected in both of
# the two immediately preceding rounds. 3. Cooperate in all other situations.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. In the first round, cooperate. 2. In any subsequent round, if you chose to
# cooperate in the previous round but received a payoff of 5, cooperate. 3.
# Otherwise, if the opponent cooperated in the previous round, cooperate. 4.
# Otherwise, defect.

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
  
      if len(self.history) >= 1:
          prev_my_action = self.history[-1]
          if prev_my_action == axl.Action.C:
              my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
              if my_last_score == 5:
                  return axl.Action.C
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# 1. Play Defect on the first round. 2. Play Cooperate on the second, third, and
# fourth rounds. 3. If the opponent played Cooperate on the second, third, and
# fourth rounds, play Defect for the remainder of the game. 4. Otherwise, for
# the remainder of the game, play Cooperate if the opponent played Cooperate in
# the previous round. 5. If the opponent played Defect in the previous round,
# play Cooperate unless the opponent played Defect in the previous two
# consecutive rounds, in which case play Defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number in (2, 3, 4):
          return axl.Action.C
  
      if round_number == 5:
          if len(opponent.history) >= 4 and opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]:
              return axl.Action.D
          return axl.Action.C
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. On the first round, cooperate. 2. On the second round, cooperate. 3. On all
# subsequent rounds, defect if the opponent defected in both of the previous two
# rounds; otherwise, cooperate.

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



# 1. Cooperate in the first round. 2. Cooperate in the second round. 3. For
# every subsequent round, defect if the opponent defected in both of the
# immediately preceding two rounds. 4. Cooperate in all other situations.

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
      if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
      return axl.Action.C



# 1. If it is the first round, play Defect. 2. If the opponent has played Defect
# in each of the last three consecutive rounds, play Cooperate. 3. Otherwise,
# play Defect.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      return axl.Action.D



# 1. Cooperate in the first round. 2. Cooperate in the second round. 3. From the
# third round onward, defect if the opponent defected in both of the two
# immediately preceding rounds. 4. In all other cases, cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Cooperate in the first round. 2. In all subsequent rounds, cooperate if
# your payoff in the previous round was 3 or 1. 3. In all subsequent rounds,
# defect if your payoff in the previous round was 5 or 0.

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
  
      last_score = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]) if False else None
      # Determine previous-round payoff from the last completed round.
      my_last_action = self.history[-1]
      opp_last_action = opponent.history[-1]
  
      if my_last_action == axl.Action.C and opp_last_action == axl.Action.C:
          previous_payoff = 3
      elif my_last_action == axl.Action.C and opp_last_action == axl.Action.D:
          previous_payoff = 0
      elif my_last_action == axl.Action.D and opp_last_action == axl.Action.C:
          previous_payoff = 5
      else:
          previous_payoff = 1
  
      if previous_payoff in (3, 1):
          return axl.Action.C
      else:
          return axl.Action.D



# Defect in the first round. If the opponent cooperated in the first round,
# defect in the second round. If the opponent cooperated in both of the first
# two rounds, defect in all remaining rounds. If the opponent defected in either
# of the first two rounds, from the third round onwards cooperate unless the
# opponent defected in both of the previous two rounds, in which case defect.

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
  
      round_num = len(self.history) + 1
  
      if round_num == 2:
          return axl.Action.D if opponent.history[0] == axl.Action.C else axl.Action.C
  
      if round_num == 3:
          if opponent.history[0] == axl.Action.C and opponent.history[1] == axl.Action.C:
              return axl.Action.D
          return axl.Action.C
  
      if opponent.history[0] == axl.Action.C and opponent.history[1] == axl.Action.C:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Cooperate in the first round. 2. Cooperate in the second round. 3. In the
# third and all subsequent rounds, defect if your opponent defected in both of
# the previous two rounds; otherwise, cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. In the first round, cooperate. 2. If the opponent cooperated in the
# previous round, cooperate. 3. If the opponent defected in the previous round,
# defect with a 90% probability and cooperate with a 10% probability.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)



# # Aggressive Strategy for Iterated Prisoner's Dilemma with Noise  1. Defect
# for the first 5 rounds to establish an aggressive posture and assess the
# opponent's behavior.  2. If the opponent cooperated at least 3 times during
# those first 5 rounds, always defect for the remainder of the game—they are
# likely a cooperative player you can exploit for maximum payoff.  3. If the
# opponent cooperated fewer than 3 times during the first 5 rounds, cooperate
# for the next 3 rounds to signal willingness to establish mutual cooperation.
# 4. After those 3 rounds of cooperation, if the opponent cooperated at least
# twice, continue cooperating—mutual cooperation yields more than mutual
# defection. If the opponent cooperated fewer than twice, always defect for the
# remainder of the game—cooperation cannot be established.  5. While in
# cooperation mode, defect once every 15 rounds to probe for exploitation
# opportunities. If the opponent defects in either of the two rounds following
# your probe defection, stop probing and simply cooperate for the rest of the
# game—they are retaliatory and exploitation won't succeed.  6. In the last 10
# rounds, always defect regardless of prior interactions—there is no future to
# consider, so cooperation offers no strategic benefit.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._phase = "initial_defect"
          self._probe_counter = 0
          self._probe_pending = False
          self._probe_wait = 0
          self._probe_start_len = None
          self._probe_defect_seen = False
          return axl.Action.D
  
      n = len(self.history)
  
      if n >= 990:
          return axl.Action.D
  
      if getattr(self, "_probe_pending", False):
          if len(opponent.history) > self._probe_start_len:
              if opponent.history[-1] == axl.Action.D:
                  self._probe_defect_seen = True
              self._probe_wait += 1
          if self._probe_defect_seen:
              self._phase = "always_cooperate"
              self._probe_pending = False
              self._probe_wait = 0
              return axl.Action.C
          if self._probe_wait >= 2:
              self._probe_pending = False
              self._probe_wait = 0
          return axl.Action.C
  
      if self._phase == "initial_defect":
          if n < 5:
              return axl.Action.D
          if opponent.history[:5].cooperations >= 3:
              self._phase = "always_defect"
              return axl.Action.D
          self._phase = "signal_cooperate"
          self._signal_start = n
          return axl.Action.C
  
      if self._phase == "signal_cooperate":
          if n < self._signal_start + 3:
              return axl.Action.C
          if opponent.history[self._signal_start:self._signal_start + 3].cooperations >= 2:
              self._phase = "cooperate_mode"
              self._probe_counter = 0
              return axl.Action.C
          self._phase = "always_defect"
          return axl.Action.D
  
      if self._phase == "always_defect":
          return axl.Action.D
  
      if self._phase == "always_cooperate":
          return axl.Action.C
  
      if self._phase == "cooperate_mode":
          if n >= 990:
              return axl.Action.D
          self._probe_counter += 1
          if self._probe_counter >= 15:
              self._probe_counter = 0
              self._probe_pending = True
              self._probe_wait = 0
              self._probe_start_len = len(opponent.history)
              self._probe_defect_seen = False
              return axl.Action.D
          return axl.Action.C
  
      return axl.Action.D



# 1. On the first round, play Cooperate. 2. On the second round, play Cooperate.
# 3. From the third round onwards, play Cooperate unless the opponent played
# Defect in both of the two immediately preceding rounds. 4. If the opponent
# played Defect in both of the two immediately preceding rounds, play Defect.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. In the first round, play Cooperate. 2. In any subsequent round, if the
# opponent played Defect in both the previous round and the round immediately
# preceding that, play Defect. 3. Otherwise, play Cooperate.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Start by playing Defect in the first round. For all subsequent rounds,
# evaluate the following conditions in order:  1. If the opponent played
# Cooperate in the previous round, play Defect. 2. If the opponent played Defect
# in both of the previous two rounds, play Defect. 3. Otherwise, play Cooperate.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Cooperate in the first two rounds. 2. In any subsequent round, defect if
# the opponent defected in both of the two immediately preceding rounds. 3. In
# all other cases, cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. If it is the first round, cooperate. 2. If it is the second round,
# cooperate. 3. If the opponent cooperated in the previous round, cooperate. 4.
# If the opponent defected in the previous round but cooperated in the round
# before that, cooperate. 5. If the opponent defected in both of the previous
# two rounds, defect.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Start by playing Defect. In subsequent rounds, if the opponent played
# Cooperate in the previous round, play Defect. If the opponent played Defect in
# the previous round, play Cooperate.

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
  
      return axl.Action.D if opponent.history[-1] == axl.Action.C else axl.Action.C



# 1. Cooperate in the first round. 2. Cooperate in the second round. 3. From the
# third round onwards, if the opponent defected in both of the two immediately
# preceding rounds, defect. 4. Otherwise, cooperate.

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
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Start by cooperating in the first round. 2. In each subsequent round, if
# the opponent cooperated in the previous round, cooperate. 3. If the opponent
# defected in the previous round, cooperate with a probability of 30% and defect
# with a probability of 70%.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.3)



# Here is a simple, aggressive strategy designed to maximise your payoff by
# exploiting cooperative opponents and punishing persistent defectors:  1. If it
# is the first round, play Defect. 2. If the opponent played Defect in each of
# the last three rounds, play Defect for the current and all remaining rounds.
# 3. If you played Cooperate in the previous round, play Defect. 4. If the
# opponent played Defect in the previous round, play Cooperate. 5. If the
# opponent played Cooperate in the previous round, play Defect.  Evaluate the
# conditions in order and play the action specified by the first one that
# applies.

class Aggressive_17(LLM_Strategy):
  n = 17
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
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          self._force_defect = True
          return axl.Action.D
  
      if self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.D



# 1. Cooperate in the first round. 2. If the opponent cooperated in the previous
# round, cooperate in the current round. 3. If the opponent defected in the
# previous round, cooperate with a 10% probability and defect with a 90%
# probability.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)



# 1. On the first round, play C. 2. On every subsequent round, observe the
# actions played in the previous round. 3. If you and your opponent played the
# same observed action in the previous round (both C or both D), play C. 4. If
# you and your opponent played different observed actions in the previous round
# (one C and one D), play D.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == last_opp:
          return axl.Action.C
      return axl.Action.D



# 1. If it is the final round, play Defect. 2. If it is the first round, play
# Defect. 3. If both you and your opponent played Defect in the previous round,
# play Cooperate. 4. Otherwise, play Defect.

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
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D



# 1. Cooperate in the first two rounds. 2. From the third round onward, defect
# if the opponent defected in both of the immediately preceding two rounds. 3.
# Otherwise, cooperate.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# 1. Cooperate on the first round. 2. On the second and third rounds, cooperate
# if the opponent cooperated in the immediately preceding round; otherwise,
# defect. 3. From the fourth round onwards, cooperate if the opponent cooperated
# in at least two of the three immediately preceding rounds; otherwise, defect.

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
  
      n = len(self.history)
  
      if n == 1:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      if n == 2:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      recent = opponent.history[-3:]
      return axl.Action.C if recent.count(axl.Action.C) >= 2 else axl.Action.D



# 1. Start by defecting. 2. If you scored 5 or 3 in the previous round, repeat
# the action you just played. 3. If you scored 1 or 0 in the previous round,
# switch to the opposite action of what you just played.

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
  
      last_my_action = self.history[-1]
      last_my_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_my_score in (5, 3):
          return last_my_action
      if last_my_score in (1, 0):
          return axl.Action.C if last_my_action == axl.Action.D else axl.Action.D
  
      return last_my_action



# 1. If it is the first round, play Cooperate. 2. If it is the second round,
# play Cooperate. 3. If the opponent defected in both of the two immediately
# preceding rounds, play Defect. 4. Otherwise, play Cooperate.

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



# 1. Cooperate in the first round. 2. If the opponent cooperated in the previous
# round, cooperate. 3. If the opponent defected in the previous round, defect if
# the opponent has defected in at least two of the last five rounds; otherwise,
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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      last_five = opponent.history[-5:]
      if last_five.count(axl.Action.D) >= 2:
          return axl.Action.D
  
      return axl.Action.C



# 1. Play Defect on the first round. 2. If the opponent has played Defect for
# the last 10 consecutive rounds, play Cooperate to test if they will
# reciprocate and break the cycle of mutual defection. 3. If the opponent played
# Cooperate in the previous round, play Defect to exploit their cooperation. 4.
# In all other cases, play Defect.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(opponent.history) >= 10 and opponent.history[-10:] == [axl.Action.D] * 10:
          return axl.Action.C
  
      if opponent.history and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.D



# 1. Cooperate on the first round. 2. In every subsequent round, cooperate
# unless the opponent's observed action was Defect in both of the immediately
# preceding two rounds. 3. If the opponent's observed action was Defect in both
# of the immediately preceding two rounds, defect.  4. After defecting, return
# to cooperating immediately if the opponent's observed action in the current
# round is Cooperate.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# # Strategy: Tit for Two Tats  1. Cooperate in round 1.  2. From round 2
# onward:    - If the opponent defected in both of the two immediately preceding
# rounds, defect.    - Otherwise, cooperate.  This strategy sustains mutual
# cooperation against cooperative opponents while tolerating occasional apparent
# defections caused by noise. It only retaliates after two consecutive
# defections, which filters out most noise-induced misunderstandings. Against
# persistent defectors, it defects to avoid exploitation. After retaliating, it
# returns to cooperation immediately upon seeing a single cooperation from the
# opponent, enabling quick recovery from retaliation cycles.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. On the first round, play Defect. 2. If the opponent played Cooperate in the
# previous round, play Defect. 3. If the opponent played Defect in the previous
# round, and they have played Cooperate at least once in the last five rounds,
# play Cooperate. 4. If the opponent played Defect in the previous round, and
# they have not played Cooperate in the last five rounds, play Defect.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      last_five = opponent.history[-5:]
      if axl.Action.C in last_five:
          return axl.Action.C
  
      return axl.Action.D



# 1. On the first round, cooperate. 2. On any subsequent round, if the opponent
# defected in both of the previous two rounds, defect. 3. In all other cases,
# cooperate.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. In the first round, cooperate. 2. In the second round, cooperate. 3. From
# the third round onwards, defect if the opponent defected in both of the
# previous two rounds; otherwise, cooperate.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# Start by playing D.   In every subsequent round, play D if any of the
# following conditions are met; otherwise, play C:  1. Your opponent played D in
# the previous round and also played D in the round before that. 2. You played C
# in the previous round and your opponent played D. 3. It is one of the last
# five rounds of the game.   If none of these conditions apply, play C.

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
  
      if len(self.history) >= 5:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      if len(self.history) >= 1 and len(opponent.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. In the first round, play Cooperate. 2. In the second round, play Cooperate.
# 3. If the opponent played Defect in both of the two immediately preceding
# rounds, play Defect. 4. In all other cases, play Cooperate.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# 1. Cooperate on the first two rounds. 2. Starting from the third round, defect
# if your opponent defected in at least two of the previous three rounds. 3.
# Otherwise, cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      recent_opponent_moves = opponent.history[-3:]
      if recent_opponent_moves.count(axl.Action.D) >= 2:
          return axl.Action.D
  
      return axl.Action.C



# 1. In the first round, defect. 2. If the opponent cooperated in the previous
# round, defect. 3. If the opponent has defected in the last three consecutive
# rounds, cooperate. 4. In all other situations, defect.

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
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      return axl.Action.D



# 1. Cooperate in the first two rounds. 2. From the third round onward, defect
# if your opponent defected in both of the two immediately preceding rounds. 3.
# From the third round onward, cooperate if your opponent cooperated in at least
# one of the two immediately preceding rounds.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      last_two = opponent.history[-2:]
      if last_two.count(axl.Action.D) == 2:
          return axl.Action.D
      return axl.Action.C



# Cooperate in the first two rounds. For every subsequent round, defect if the
# opponent defected in both of the two immediately preceding rounds. Cooperate
# in all other cases.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# 1. Play Defect in the first round. 2. If your payoff in the previous round was
# 1 (you Defected and the opponent Defected), play Cooperate. 3. If your payoff
# in the previous round was 5 (you Defected and the opponent Cooperated), play
# Defect. 4. If your payoff in the previous round was 3 (you Cooperated and the
# opponent Cooperated), play Defect. 5. If your payoff in the previous round was
# 0 (you Cooperated and the opponent Defected), play Defect.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.D
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.D
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.D



# 1. Play Cooperate in the first round. 2. Play Cooperate in the second round
# regardless of the opponent's first action. 3. For all subsequent rounds, play
# Defect if the opponent played Defect in both of the previous two rounds;
# otherwise, play Cooperate.

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



# Cooperate in the first two rounds.   From the third round onward, evaluate the
# opponent's actions in the previous two rounds: 1. If the opponent defected in
# both of the previous two rounds, defect. 2. Otherwise, cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Start by defecting. In each subsequent round, evaluate the following
# conditions in order:  1. If the opponent played Cooperate in the previous
# round, play Defect. 2. If the opponent's last three actions were all Defect,
# play Cooperate. 3. Otherwise, play Defect.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      return axl.Action.D



# 1. Cooperate on the first round. 2. On any subsequent round, defect if the
# opponent defected in both of the two immediately preceding rounds. 3.
# Otherwise, cooperate.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. In the first round, play Cooperate. 2. If the opponent played Cooperate in
# the previous round, play Cooperate. 3. If the opponent played Defect in the
# previous round but played Cooperate two rounds ago, play Cooperate. 4. If the
# opponent played Defect in both of the previous two rounds, play Defect.

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
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C