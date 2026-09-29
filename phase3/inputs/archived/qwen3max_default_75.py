import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# Play D in every round, regardless of what your opponent has done in previous
# rounds.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in each
# subsequent round:    1. If your opponent played C in the previous round, play
# C.   2. If your opponent played D in the previous round, play D.    Continue
# this pattern for all 1000 rounds.

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



# Start by cooperating in the first round. After that, follow these rules in
# order:  1. If your opponent cooperated in the previous round, cooperate in the
# current round.   2. If your opponent defected in the previous round, defect in
# the current round.

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



# Play D in every round, regardless of what your opponent has done previously.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing C in the first round.    After that, in each subsequent
# round:   - If your opponent played C in the previous round, play C.   - If
# your opponent played D in the previous round, play D.    Continue this pattern
# for all 1000 rounds.

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



# Start by cooperating in the first round. After that, follow these rules in
# order:  1. If your opponent cooperated in the previous round, cooperate in the
# current round.   2. If your opponent defected in the previous round, defect in
# the current round.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Play D in every round, regardless of what your opponent has done in previous
# rounds.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in each
# subsequent round:    1. If your opponent played C in the previous round, play
# C.   2. If your opponent played D in the previous round, play D.    Continue
# this pattern for all 1000 rounds.

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



# Start by playing C in the first round.    After that, in each subsequent
# round:    1. If your opponent played C in the previous round, play C.   2. If
# your opponent played D in the previous round, play D.

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



# Play D in every round, regardless of what your opponent does. Never cooperate.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.   After that, in every subsequent
# round, do exactly what your opponent did in the previous round.   If your
# opponent cooperated last round, cooperate this round.   If your opponent
# defected last round, defect this round.

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



# Start by cooperating in the first round. After that, follow these rules in
# order:  1. If your opponent cooperated in the previous round, cooperate in the
# current round.   2. If your opponent defected in the previous round, defect in
# the current round.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Play D in every round, regardless of what your opponent has done previously.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in every
# subsequent round:    1. If your opponent played C in the previous round, play
# C.   2. If your opponent played D in the previous round, play D.    Continue
# this rule for all 1000 rounds.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# Start by playing C in the first round.    In every subsequent round:    1. If
# your opponent played C in the previous round, play C.   2. If your opponent
# played D in the previous round, play D.

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



# Play D in every round, regardless of what your opponent has done in previous
# rounds.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round. After that, in every
# subsequent round, do exactly what your opponent did in the previous round: if
# they played C last round, play C; if they played D last round, play D.

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



# Start by cooperating in the first round. After that, follow these rules in
# order:  1. If your opponent cooperated in the previous round, cooperate in the
# current round.   2. If your opponent defected in the previous round, defect in
# the current round.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Play D in every round, regardless of what your opponent does. Never cooperate.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in every
# subsequent round:    1. If your opponent played C in the previous round, play
# C.   2. If your opponent played D in the previous round, play D.    Continue
# this pattern for all 1000 rounds.

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
      return opponent.history[-1]



# Start by cooperating in the first round. After that, follow these rules in
# order:  1. If your opponent cooperated in the previous round, cooperate in the
# current round.   2. If your opponent defected in the previous round, defect in
# the current round.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Play D (defect) in every round, regardless of what your opponent does. Never
# cooperate.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in every
# subsequent round:    1. If your opponent played C in the previous round, play
# C.   2. If your opponent played D in the previous round, play D.    Continue
# this pattern for all 1000 rounds.

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
      return opponent.history[-1]



# Start by cooperating in the first round. After that, follow these rules in
# order:  1. If your opponent cooperated in the previous round, cooperate in the
# current round.   2. If your opponent defected in the previous round, defect in
# the current round.

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
      return opponent.history[-1]



# Play D in every round, regardless of what your opponent has done in previous
# rounds.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in each
# subsequent round:    1. If your opponent played C in the previous round, play
# C.   2. If your opponent played D in the previous round, play D.    Continue
# this pattern for all 1000 rounds.

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



# Start by playing C in the first round.    In every subsequent round:    1. If
# your opponent played C in the previous round, play C.   2. If your opponent
# played D in the previous round, play D.

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



# Play D in every round, regardless of what your opponent has done in previous
# rounds.

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in every
# subsequent round:    1. If your opponent played C in the previous round, play
# C.   2. If your opponent played D in the previous round, play D.    Continue
# this rule for all 1000 rounds.

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



# Play cooperatively at first, but respond clearly to your opponent’s actions as
# follows:  1. Start by playing C in round 1.   2. In every subsequent round:
# a. If your opponent played C in the previous round, play C.      b. If your
# opponent played D in the previous round, play D.

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
      return opponent.history[-1] if opponent.history else axl.Action.C



# Play D in every round, regardless of what your opponent does. Never cooperate.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    In every subsequent round:    1.
# If your opponent cooperated in the previous round, cooperate.   2. If your
# opponent defected in the previous round, defect.    This strategy—known as
# Tit-for-Tat—maintains cooperation when the opponent does, and immediately
# responds to defection with defection, encouraging mutual cooperation over the
# 1000 rounds.

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
      return opponent.history[-1]



# Start by playing C in the first round.   After that, in every subsequent
# round:    - If your opponent played C in the previous round, play C.   - If
# your opponent played D in the previous round, play D.

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



# Play D in every round, regardless of what your opponent does. Never cooperate.
# Always defect.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in every
# subsequent round:    1. If your opponent played C in the previous round, play
# C.   2. If your opponent played D in the previous round, play D.    Continue
# this rule for all 1000 rounds.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# Start by cooperating in the first round. After that, follow these rules in
# order:  1. If your opponent cooperated in the previous round, cooperate in the
# current round.   2. If your opponent defected in the previous round, defect in
# the current round.

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



# Play D in every round, regardless of what your opponent does.

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in each
# subsequent round:    1. If your opponent played C in the previous round, play
# C.   2. If your opponent played D in the previous round, play D.    Continue
# this pattern for all 1000 rounds.

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



# Start by cooperating in the first round. After that, follow these rules in
# order:  1. If your opponent cooperated in the previous round, cooperate in the
# current round.   2. If your opponent defected in the previous round, defect in
# the current round.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Play D in every round, regardless of what your opponent does.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing C in the first round.    In every subsequent round:    1. If
# your opponent played C in the previous round, play C.   2. If your opponent
# played D in the previous round, play D.    Continue this pattern for all 1000
# rounds.

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



# Start by cooperating in the first round. After that, follow these rules in
# order:  1. If your opponent cooperated in the previous round, cooperate in the
# current round.   2. If your opponent defected in the previous round, defect in
# the current round.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Play D in every round, regardless of what your opponent has done previously.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round. After that, in every subsequent
# round, do exactly what your opponent did in the previous round: if they
# cooperated last round, cooperate this round; if they defected last round,
# defect this round. Continue this rule for all 1000 rounds.

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



# Play Cooperate (C) in the first round. After that, follow these rules in
# order:  1. If your opponent played Cooperate (C) in the previous round, play
# Cooperate (C) in the current round.   2. If your opponent played Defect (D) in
# the previous round, play Defect (D) in the current round.

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



# Play D in every round, regardless of what your opponent does.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in each
# subsequent round:    1. If your opponent played Cooperate (C) in the previous
# round, play Cooperate (C).   2. If your opponent played Defect (D) in the
# previous round, play Defect (D).    Continue this rule for all 1000 rounds.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Play Cooperate (C) in the first round. In every subsequent round, do the
# following:  1. If your opponent played C in the previous round, play C.   2.
# If your opponent played D in the previous round, play D.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Play D in every round, regardless of what your opponent has done previously.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in each
# subsequent round:    1. If your opponent played C in the previous round, play
# C.   2. If your opponent played D in the previous round, play D.    Continue
# this rule for all 1000 rounds.

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



# Start by cooperating in the first round. After that, follow these rules in
# order:  1. If your opponent cooperated in the previous round, cooperate in the
# current round.   2. If your opponent defected in the previous round, defect in
# the current round.

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



# Play D in every round, regardless of what your opponent does.

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round.    After that, in every subsequent
# round:   - If your opponent cooperated in the previous round, cooperate.   -
# If your opponent defected in the previous round, defect.    Continue this
# pattern for all 1000 rounds.

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



# Start by cooperating in the first round. After that, in every subsequent
# round:  1. If your opponent cooperated in the previous round, cooperate.   2.
# If your opponent defected in the previous round, defect.

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



# Play D in every round, regardless of what your opponent has done in previous
# rounds.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in every
# subsequent round:    1. If your opponent played C in the previous round, play
# C.   2. If your opponent played D in the previous round, play D.    Continue
# this pattern for all 1000 rounds.

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



# Start by playing C in the first round.    After that, in each subsequent
# round:    1. If your opponent played C in the previous round, play C.   2. If
# your opponent played D in the previous round, play D.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Play D in every round, regardless of what your opponent does.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in every
# subsequent round:    1. If your opponent played C in the previous round, play
# C.   2. If your opponent played D in the previous round, play D.    This
# strategy—known as Tit-for-Tat—rewards cooperation by continuing to cooperate,
# and deters exploitation by immediately responding to defection with defection.

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



# Play Cooperate (C) in the first round. After that, in each subsequent round:
# 1. If your opponent played Cooperate in the previous round, play Cooperate.
# 2. If your opponent played Defect in the previous round, play Defect.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# Play D in every round, regardless of what your opponent does.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in every
# subsequent round:    1. If your opponent played C in the previous round, play
# C.   2. If your opponent played D in the previous round, play D.    Continue
# this rule for all 1000 rounds.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Start by playing C in the first round.    After that, in each subsequent
# round:    1. If your opponent played C in the previous round, play C.   2. If
# your opponent played D in the previous round, play D.

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



# Play D in every round, regardless of what your opponent does. Never cooperate.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in every
# subsequent round:    1. If your opponent played C in the previous round, play
# C.   2. If your opponent played D in the previous round, play D.    This
# strategy continues for all 1000 rounds.

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
      return opponent.history[-1]



# Play Cooperate (C) in the first round.    After that, in each subsequent
# round:    1. If your opponent played Cooperate in the previous round, play
# Cooperate.   2. If your opponent played Defect in the previous round, play
# Defect.

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



# Play D in every round, regardless of what your opponent does.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing C in the first round.    In every subsequent round:    1. If
# your opponent played C in the previous round, play C.   2. If your opponent
# played D in the previous round, play D.    Continue this pattern for all 1000
# rounds.

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



# Start by cooperating in the first round. After that, follow these rules in
# order:  1. If your opponent cooperated in the previous round, cooperate in the
# current round.   2. If your opponent defected in the previous round, defect in
# the current round.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Play D in every round, regardless of what your opponent has done previously.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in each
# subsequent round:    1. If your opponent played C in the previous round, play
# C.   2. If your opponent played D in the previous round, play D.    Continue
# this pattern for all 1000 rounds.

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



# Start by playing C in the first round.    After that, in each subsequent
# round:    1. If your opponent played C in the previous round, play C.   2. If
# your opponent played D in the previous round, play D.

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



# Play D in every round, regardless of what your opponent has done in any
# previous round.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.    After that, in every
# subsequent round:    1. If your opponent played C in the previous round, play
# C.   2. If your opponent played D in the previous round, play D.    Continue
# this pattern for all 1000 rounds.

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



# Start by playing C in the first round.    In every subsequent round:    1. If
# your opponent played C in the previous round, play C.   2. If your opponent
# played D in the previous round, play D.

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