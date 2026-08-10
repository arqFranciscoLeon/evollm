import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# 1. If the current round is within the final 10 rounds, defect. 2. If the
# current round is the first round, defect. 3. If the opponent cooperated in the
# previous round, defect. 4. If the opponent defected in the previous round,
# cooperate.

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
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.C






# 1. On the first round, cooperate. 2. On any subsequent round, if the opponent
# cooperated in the previous round, cooperate. 3. On any subsequent round, if
# the opponent defected in the previous round, defect.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# 1. In the first round, cooperate. 2. If the opponent cooperated in the
# previous round, cooperate in the current round. 3. If the opponent defected in
# the previous round, defect in the current round.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# 1. In the first round, play Defect. 2. If the opponent played Defect in the
# previous round, play Defect. 3. If the opponent played Cooperate in the
# previous round, play Defect, unless the previous two rounds both resulted in
# you playing Defect while the opponent played Cooperate; in this specific case,
# play Cooperate once to sustain their cooperation before resuming Defection.

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
      opponent_last = opponent.history[-1]
      if opponent_last == axl.Action.D:
          return axl.Action.D
      # opponent_last is C
      if (len(self.history) >= 2 
          and self.history[-2] == axl.Action.D 
          and self.history[-1] == axl.Action.D 
          and opponent.history[-2] == axl.Action.C):
          return axl.Action.C
      else:
          return axl.Action.D






# 1. In the first round, play C. 2. In every subsequent round, if your opponent
# played C in the previous round, play C. 3. In every subsequent round, if your
# opponent played D in the previous round, play D.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D






# 1. In the first round, cooperate. 2. In every subsequent round, if the
# opponent cooperated in the previous round, cooperate. 3. In every subsequent
# round, if the opponent defected in the previous round, defect.

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






# 1. Play D in the first round. 2. If the opponent played C in the previous
# round, play D to exploit their cooperation. 3. If the opponent played D in the
# previous round, play D to protect yourself, unless the opponent has played D
# for three consecutive rounds, in which case play C for exactly one round to
# bait them into cooperating, then play D in the following round regardless of
# their move.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._bait_next_round = False
          return axl.Action.D
  
      if getattr(self, "_bait_next_round", False):
          self._bait_next_round = False
          return axl.Action.D
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          self._bait_next_round = True
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.D






# 1. If it is the first round, cooperate. 2. If the opponent cooperated in the
# previous round, cooperate. 3. If the opponent defected in the previous round,
# defect.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# 1. If it is the first round, cooperate. 2. If the opponent cooperated in the
# previous round, cooperate. 3. If the opponent defected in the previous round,
# defect.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# Play defect in the first round. For all subsequent rounds, evaluate the
# following conditions in order:  1. If the opponent cooperated in the previous
# round, defect. 2. If the opponent has defected for the last three consecutive
# rounds, cooperate. 3. In all other cases, defect.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      return axl.Action.D






# 1. In the first round, play Cooperate.  2. In rounds two through nine hundred
# ninety-nine, play Cooperate if the opponent played Cooperate in the
# immediately preceding round; otherwise, play Defect.  3. In round one
# thousand, play Defect.

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
  
      if round_number == 1000:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# Start by cooperating in the first round. In every subsequent round, cooperate
# if the opponent cooperated in the previous round, and defect if the opponent
# defected in the previous round. In the final round, defect regardless of the
# opponent's previous action.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1]






# 1. Defect on the first round. 2. Defect during the final ten rounds. 3. If you
# cooperated in the previous round, defect. 4. If the opponent cooperated in the
# previous round, defect. 5. If both players defected in the previous round,
# cooperate.

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
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D






# 1. In the first round, cooperate. 2. In rounds 2 through 999, cooperate if the
# opponent cooperated in the previous round, and defect if the opponent defected
# in the previous round. 3. In the 1000th round, defect.

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






# 1. If it is the first round, cooperate. 2. If the opponent cooperated in the
# previous round, cooperate. 3. If the opponent defected in the previous round,
# defect.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# 1. Play Defect on the first round. 2. If the opponent played Cooperate in the
# previous round, play Defect to exploit them and secure the maximum payoff of
# 5. 3. If the opponent played Defect in the previous round, play Defect to
# protect yourself and secure a payoff of 1 instead of 0. 4. Never play
# Cooperate under any circumstances.

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
      return axl.Action.D






# 1. In the first round, play Cooperate. 2. In every subsequent round, if the
# opponent played Cooperate in the immediately preceding round, play Cooperate.
# 3. In every subsequent round, if the opponent played Defect in the immediately
# preceding round, play Defect.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# 1. Cooperate in the first round. 2. In all subsequent rounds, cooperate if
# your opponent cooperated in the immediately preceding round. 3. In all
# subsequent rounds, defect if your opponent defected in the immediately
# preceding round.

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
      return opponent.history[-1] if opponent.history else axl.Action.C






# 1. If it is the first round, defect. 2. If it is the second round, cooperate.
# 3. If the opponent cooperated in both the first and second rounds, defect in
# the third round and all subsequent rounds. 4. If the opponent defected in
# either the first or second round, copy the opponent's move from the previous
# round for the current round and all subsequent rounds.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._locked_action = None
          return axl.Action.D
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if self._locked_action is not None:
          return self._locked_action
  
      if len(opponent.history) >= 2 and opponent.history[0] == axl.Action.C and opponent.history[1] == axl.Action.C:
          self._locked_action = axl.Action.D
          return self._locked_action
  
      self._locked_action = opponent.history[-1]
      return self._locked_action






# 1. In the first round, cooperate. 2. In the final round (round 1000), defect.
# 3. In all other rounds, cooperate if the opponent cooperated in the previous
# round, and defect if the opponent defected in the previous round.

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
      return opponent.history[-1] if opponent.history else axl.Action.C






# 1. In the first round, cooperate. 2. In every subsequent round, cooperate if
# both you and your opponent either both cooperated or both defected in the
# previous round. 3. In every subsequent round, defect if exactly one of you
# cooperated and the other defected in the previous round.

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
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
      if last_self == last_opp:
          return axl.Action.C
      else:
          return axl.Action.D






# 1. If it is the first round, defect. 2. If the opponent cooperated in the
# previous round, defect. 3. If the opponent defected in the previous round,
# defect.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D






# 1. In the first round, play C. 2. In any subsequent round, if the opponent
# played C in the previous round, play C. 3. In any subsequent round, if the
# opponent played D in the previous round, play D.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D






# 1. In the first round, play Cooperate. 2. In every subsequent round, if the
# opponent played Cooperate in the previous round, play Cooperate. 3. In every
# subsequent round, if the opponent played Defect in the previous round, play
# Defect.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# 1. If it is the first round, play Defect. 2. If the opponent played Cooperate
# in the previous round, play Defect. 3. If the opponent played Defect in the
# previous round, and you played Cooperate in the previous round, play Defect.
# 4. If there have been 10 consecutive rounds of mutual Defection prior to the
# current round, play Cooperate. 5. In all other cases, play Defect.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(self.history) >= 10:
          last_10_self = self.history[-10:]
          last_10_opp = opponent.history[-10:]
          if all(m == axl.Action.D for m in last_10_self) and all(m == axl.Action.D for m in last_10_opp):
              return axl.Action.C
  
      return axl.Action.D






# 1. In the first round, play Cooperate.  2. In every subsequent round, if the
# opponent played Cooperate in the previous round, play Cooperate.  3. In every
# subsequent round, if the opponent played Defect in the previous round, play
# Defect.

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






# 1. Cooperate in the first round. 2. If the opponent cooperated in the previous
# round, cooperate in the current round. 3. If the opponent defected in the
# previous round, defect in the current round.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# 1. If it is the first round, defect to establish an aggressive baseline and
# seek the maximum possible payoff. 2. If the opponent cooperated in the
# previous round, defect to exploit their cooperation for a payoff of 5. 3. If
# the opponent defected in the previous round, defect to protect yourself from
# receiving a payoff of 0 and secure a payoff of 1. 4. Never cooperate, as
# defection strictly dominates cooperation in this payoff structure,
# guaranteeing a higher or equal payoff in every individual round regardless of
# the opponent's action.

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






# 1. If it is the first round, play Cooperate. 2. If it is the final round
# (round 1000), play Defect. 3. If the opponent played Defect in the previous
# round, play Defect. 4. Otherwise, play Cooperate.

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
      if len(self.history) >= 999:
          return axl.Action.D
      if opponent.history and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C






# 1. Play Cooperate in the first round. 2. If both you and your opponent played
# Cooperate in the previous round, play Cooperate. 3. If both you and your
# opponent played Defect in the previous round, play Cooperate. 4. If you played
# Cooperate and your opponent played Defect in the previous round, play Defect.
# 5. If you played Defect and your opponent played Cooperate in the previous
# round, play Defect.

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
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          return axl.Action.D
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.C






# 1. Play Defect in the first round and the second round. 2. If the opponent
# played Cooperate in both the first and second rounds, play Defect for the
# remainder of the game. 3. If the opponent played Defect in either the first or
# second round, play Cooperate in the third and fourth rounds. 4. From the fifth
# round onward, play Cooperate if the opponent played Cooperate in the previous
# round, and play Defect if the opponent played Defect in the previous round.

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
  
      round_number = len(self.history) + 1
  
      if round_number == 2:
          return axl.Action.D
  
      if round_number >= 3:
          if len(opponent.history) >= 2 and opponent.history[0] == axl.Action.C and opponent.history[1] == axl.Action.C:
              return axl.Action.D
  
          if round_number in (3, 4):
              if len(opponent.history) >= 2 and (opponent.history[0] == axl.Action.D or opponent.history[1] == axl.Action.D):
                  return axl.Action.C
  
          if round_number >= 5:
              return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      return axl.Action.D






# 1. If it is the first round, cooperate. 2. If the opponent cooperated in the
# previous round, cooperate. 3. If the opponent defected in the previous round,
# defect.

class Cooperative_11(LLM_Strategy):
  n = 11
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D






# 1. In the first round, play C. 2. In any subsequent round, if the opponent
# played C in the previous round, play C. 3. In any subsequent round, if the
# opponent played D in the previous round, play D.

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
      return opponent.history[-1]






# 1. On the first round, play Defect. 2. If you scored 5 in the previous round,
# play Defect. 3. If you scored 3 in the previous round, play Defect. 4. If you
# scored 1 in the previous round, play Cooperate. 5. If you scored 0 in the
# previous round, play Defect.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_score = self.score - self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_score == 5:
          return axl.Action.D
      if last_score == 3:
          return axl.Action.D
      if last_score == 1:
          return axl.Action.C
      if last_score == 0:
          return axl.Action.D
  
      return axl.Action.D






# 1. In the first round, cooperate. 2. In the final round (round 1000), defect.
# 3. In any other round, if the opponent cooperated in the previous round,
# cooperate. 4. In any other round, if the opponent defected in the previous
# round, defect.

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
  
      return opponent.history[-1]






# 1. If it is the first round, cooperate. 2. If the opponent cooperated in the
# previous round, cooperate. 3. If the opponent defected in the previous round,
# defect.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# 1. Play Cooperate on the first round to establish trust and invite mutual
# cooperation. 2. If the opponent played Cooperate in the previous round, play
# Defect to exploit their cooperation for the highest possible payoff. 3. If the
# opponent played Defect in the previous round and you played Cooperate, play
# Defect to protect yourself from being exploited again. 4. If both you and the
# opponent played Defect in the previous round, play Cooperate to attempt to
# reset the relationship and return to a state where you can exploit them. 5. In
# the final ten rounds, always play Defect to secure your gains and prevent end-
# game exploitation.

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
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      last_opp = opponent.history[-1]
      last_self = self.history[-1]
  
      if last_opp == axl.Action.C:
          return axl.Action.D
      if last_opp == axl.Action.D and last_self == axl.Action.C:
          return axl.Action.D
      if last_opp == axl.Action.D and last_self == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C






# 1. In the first round, play Cooperate. 2. In any subsequent round, if your
# opponent played Cooperate in the previous round, play Cooperate. 3. In any
# subsequent round, if your opponent played Defect while you played Cooperate in
# the previous round, play Defect. 4. In any subsequent round, if both you and
# your opponent played Defect in the previous round, play Cooperate.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C






# 1. Cooperate in the first round. 2. In every subsequent round, cooperate if
# the opponent cooperated in the previous round. 3. In every subsequent round,
# defect if the opponent defected in the previous round.

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
      return opponent.history[-1]






# 1. Play Defect in the first round. 2. If the opponent played Cooperate in the
# previous round, play Defect. 3. If the opponent has defected for the last five
# consecutive rounds, play Defect. 4. If both you and the opponent have defected
# for the last two consecutive rounds, play Cooperate. 5. In all other
# situations, play Defect.

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
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opponent.history) >= 5 and opponent.history[-5:] == [axl.Action.D] * 5:
          return axl.Action.D
  
      if (
          len(self.history) >= 2
          and len(opponent.history) >= 2
          and self.history[-2:] == [axl.Action.D] * 2
          and opponent.history[-2:] == [axl.Action.D] * 2
      ):
          return axl.Action.C
  
      return axl.Action.D






# Begin by cooperating in the first round. In every subsequent round, cooperate
# if the opponent cooperated in the immediately preceding round. Defect if the
# opponent defected in the immediately preceding round.

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






# 1. In the first round, play Cooperate. 2. In any subsequent round, if the
# opponent played Cooperate in the previous round, play Cooperate. 3. In any
# subsequent round, if the opponent played Defect in the previous round, play
# Defect.

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






# 1. Play Defect on the first round. 2. Play Defect on the second round. 3. If
# the opponent played Cooperate on both the first and second rounds, play Defect
# for all remaining rounds. 4. If the opponent played Defect on either the first
# or second round, play Cooperate on the third round. 5. From the fourth round
# onward, copy the move the opponent played on the previous round.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._opponent_first_two_cooperated = None
          return axl.Action.D
  
      if len(self.history) == 1:
          return axl.Action.D
  
      if len(self.history) == 2:
          self._opponent_first_two_cooperated = (
              opponent.history[0] == axl.Action.C and opponent.history[1] == axl.Action.C
          )
          if self._opponent_first_two_cooperated:
              return axl.Action.D
          return axl.Action.C
  
      if self._opponent_first_two_cooperated:
          return axl.Action.D
  
      return opponent.history[-1]






# 1. If it is the first round, play Cooperate. 2. If the opponent played
# Cooperate in the previous round, play Cooperate. 3. If the opponent played
# Defect in the previous round, play Defect.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# 1. Cooperate in the first round. 2. In every subsequent round, cooperate if
# the opponent cooperated in the previous round. 3. In every subsequent round,
# defect if the opponent defected in the previous round.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# 1. Defect on the first round.  2. If both you and your opponent defected in
# the previous round, cooperate on the current round. 3. In all other
# situations, defect.

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
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D






# 1. In round 1, play C. 2. In rounds 2 through 999, play C if your opponent
# played C in the previous round; otherwise, play D. 3. In round 1000, play D.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D






# 1. In the first round, play Cooperate. 2. In rounds 2 through 999, if the
# opponent played Cooperate in the previous round, play Cooperate. 3. In rounds
# 2 through 999, if the opponent played Defect in the previous round, play
# Defect. 4. In the 1000th round, play Defect.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1]






# Play Defect on the first round.   For rounds 2 through 999, choose your action
# based on your payoff from the previous round: - If you scored 5, play Defect
# to continue exploiting the opponent. - If you scored 3, play Defect to attempt
# to exploit the opponent's cooperation. - If you scored 1, play Cooperate to
# attempt to break out of mutual defection. - If you scored 0, play Defect to
# retaliate against the opponent's exploitation.  On the 1000th round, play
# Defect regardless of the previous outcome.

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
  
      if len(self.history) >= 1000:
          return axl.Action.D
  
      last_score = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_score == 5:
          return axl.Action.D
      if last_score == 3:
          return axl.Action.D
      if last_score == 1:
          return axl.Action.C
      if last_score == 0:
          return axl.Action.D
  
      return axl.Action.D






# 1. In the first round, play Cooperate. 2. In any subsequent round, if the
# opponent played Cooperate in the previous round, play Cooperate. 3. In any
# subsequent round, if the opponent played Defect in the previous round, play
# Defect.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# 1. If it is the first round, cooperate. 2. If the opponent cooperated in the
# previous round, cooperate. 3. If the opponent defected in the previous round,
# defect.

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
      return axl.Action.D






# Start by defecting in the first round. In all subsequent rounds, choose your
# action based on the outcome of the previous round using the following
# conditions:  1. If you defected and your opponent cooperated, defect again to
# continue exploiting them. 2. If you defected and your opponent defected,
# cooperate to attempt to restore mutual cooperation. 3. If you cooperated and
# your opponent cooperated, defect to attempt to exploit their cooperation. 4.
# If you cooperated and your opponent defected, defect to retaliate and avoid
# further exploitation.

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
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
      else:
          return axl.Action.D






# 1. If it is the first round, play C. 2. If the opponent played C in the
# previous round, play C. 3. If the opponent played D in the previous round,
# play D.

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
      return opponent.history[-1]






# 1. If it is the first round, cooperate. 2. If it is not the first round and
# the opponent cooperated in the previous round, cooperate. 3. If it is not the
# first round and the opponent defected in the previous round, defect.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# Defect on the first round. If the opponent defected on the first round, defect
# for the rest of the game. If the opponent cooperated on the first round,
# defect on the second round. If the opponent cooperated on the second round,
# defect for the rest of the game. If the opponent defected on the second round,
# cooperate on the third round. If the opponent defected on the third round,
# defect for the rest of the game. If the opponent cooperated on the third
# round, cooperate from the fourth round until the 999th round, then defect on
# the 1000th round.

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
  
      if round_number == 2:
          if opponent.history[0] == axl.Action.D:
              return axl.Action.D
          return axl.Action.D
  
      if round_number == 3:
          if opponent.history[1] == axl.Action.C:
              return axl.Action.D
          return axl.Action.C
  
      if round_number == 4:
          if opponent.history[2] == axl.Action.D:
              return axl.Action.D
          return axl.Action.C
  
      if round_number <= 999:
          return axl.Action.C
  
      return axl.Action.D






# 1. If it is the first round, cooperate. 2. If it is the final round (round
# 1000), defect. 3. In all other rounds, cooperate if your opponent cooperated
# in the previous round, and defect if your opponent defected in the previous
# round.

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
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1]






# 1. Cooperate on the first round. 2. On every subsequent round, cooperate if
# the opponent cooperated in the previous round. 3. On every subsequent round,
# defect if the opponent defected in the previous round.

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






# 1. In the first round, defect. 2. In the final ten rounds, always defect. 3.
# If you defected and the opponent cooperated in the previous round, defect to
# continue exploiting them. 4. If both players defected in the previous round,
# cooperate to attempt to restore mutual cooperation. 5. If you cooperated and
# the opponent defected in the previous round, defect to punish their
# exploitation. 6. If both players cooperated in the previous round, defect if
# this is the tenth consecutive round of mutual cooperation to test for
# exploitability; otherwise, cooperate.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mutual_coop_streak = 0
          return axl.Action.D
  
      if len(self.history) >= 10 and all(move == axl.Action.C for move in self.history[-10:]) and all(
          move == axl.Action.C for move in opponent.history[-10:]
      ):
          self._mutual_coop_streak = 10
      else:
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
              self._mutual_coop_streak = getattr(self, "_mutual_coop_streak", 0) + 1
          else:
              self._mutual_coop_streak = 0
  
      if len(self.history) >= 10 and len(self.history) >= 1000 - 10:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          if getattr(self, "_mutual_coop_streak", 0) >= 10:
              self._mutual_coop_streak = 0
              return axl.Action.D
          return axl.Action.C
  
      return axl.Action.D






# In the first round, play Cooperate. In every subsequent round, play Cooperate
# if your opponent played Cooperate in the previous round, and play Defect if
# your opponent played Defect in the previous round.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D






# 1. In the first round, cooperate.  2. In rounds 2 through 999, if the opponent
# cooperated in the immediately preceding round, cooperate; if the opponent
# defected in the immediately preceding round, defect.  3. In round 1000,
# defect.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1]






# 1. Defect on the first round to establish an aggressive baseline and test the
# opponent's response. 2. If the opponent cooperated in the previous round,
# defect to exploit their cooperation and secure the maximum possible payoff of
# 5. 3. If the opponent defected in the previous round, defect to protect
# yourself from receiving a payoff of 0 and instead secure the mutual defection
# payoff of 1. 4. Never cooperate under any condition, as cooperating always
# yields a lower payoff than defecting regardless of the opponent's action.

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
      return axl.Action.D






# 1. In the first round, play Cooperate. 2. In any subsequent round, if the
# opponent played Cooperate in the previous round, play Cooperate. 3. In any
# subsequent round, if the opponent played Defect in the previous round, play
# Defect.

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
      return opponent.history[-1]






# Cooperate in the first round. In every subsequent round, cooperate if the
# opponent cooperated in the previous round, and defect if the opponent defected
# in the previous round.

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






# 1. Play Defect on the first round. 2. If it is the final round, play Defect.
# 3. If the opponent has never defected in any previous round, play Defect. 4.
# If the opponent's first defection occurred in the previous round, play
# Cooperate. 5. If the opponent's first defection occurred two rounds ago, play
# Cooperate. 6. Otherwise, copy the opponent's previous move.

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
  
      if len(self.history) >= 1000:
          return axl.Action.D
  
      if opponent.defections == 0:
          return axl.Action.D
  
      first_defection_index = None
      for i, move in enumerate(opponent.history):
          if move == axl.Action.D:
              first_defection_index = i
              break
  
      if first_defection_index is not None:
          rounds_since_first_defection = len(opponent.history) - 1 - first_defection_index
          if rounds_since_first_defection == 0:
              return axl.Action.C
          if rounds_since_first_defection == 1:
              return axl.Action.C
  
      return opponent.history[-1]






# 1. If it is the first round, cooperate. 2. If your opponent cooperated in the
# previous round, cooperate. 3. If your opponent defected in the previous round,
# defect.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# 1. In the first round, cooperate. 2. In every subsequent round, if the
# opponent cooperated in the previous round, cooperate. 3. In every subsequent
# round, if the opponent defected in the previous round, defect.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# 1. In the first round, defect. 2. In the second and third rounds, cooperate.
# 3. If the opponent cooperated in both the second and third rounds, defect in
# all remaining rounds. 4. If the opponent defected in either the second or
# third round, copy the opponent's previous move in all remaining rounds, except
# defect in the final round.

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
  
      round_number = len(self.history) + 1
  
      if round_number in (2, 3):
          return axl.Action.C
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(opponent.history) >= 3 and opponent.history[1] == axl.Action.C and opponent.history[2] == axl.Action.C:
          return axl.Action.D
  
      return opponent.history[-1]






# 1. In the first round, cooperate. 2. In every subsequent round, if the
# opponent cooperated in the previous round, cooperate. 3. In every subsequent
# round, if the opponent defected in the previous round, defect.

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
      return opponent.history[-1] if opponent.history else axl.Action.C






# 1. If it is the first round, cooperate. 2. If it is the 1000th round, defect.
# 3. If the opponent cooperated in the previous round, cooperate. 4. If the
# opponent defected in the previous round, defect.

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
      if len(self.history) + 1 == 1000:
          return axl.Action.D
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# 1. In the first round, play defect. 2. If the opponent played cooperate in the
# previous round, play defect to exploit their cooperation and secure the
# maximum possible payoff of 5. 3. If the opponent played defect in the previous
# round, play defect to avoid receiving a payoff of zero and secure the mutual
# defection payoff of 1.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.D






# 1. If it is the first round, cooperate. 2. If the opponent cooperated in the
# previous round, cooperate. 3. If the opponent defected in the previous round,
# defect.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# 1. If it is the first round, cooperate. 2. If it is the final round (round
# 1000), defect. 3. If the opponent cooperated in the previous round, cooperate.
# 4. If the opponent defected in the previous round, defect.

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
      if len(self.history) >= 999:
          return axl.Action.D
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D






# 1. If it is the first round, defect. 2. If the opponent cooperated in the
# previous round, defect. 3. If the opponent defected in the previous round and
# you have defected for the last five consecutive rounds, cooperate. 4. In all
# other cases, defect.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(self.history) >= 5 and self.history[-5:] == [axl.Action.D] * 5:
          return axl.Action.C
  
      return axl.Action.D






# 1. Cooperate in the first round. 2. In every subsequent round, cooperate if
# your opponent cooperated in the previous round. 3. Defect if your opponent
# defected in the previous round.

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






# 1. Cooperate in the first round. 2. In every subsequent round, observe the
# opponent's action from the immediately preceding round. 3. If the opponent
# cooperated in the preceding round, cooperate in the current round. 4. If the
# opponent defected in the preceding round, defect in the current round.

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
