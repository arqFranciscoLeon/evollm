import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# 1. **Play D in the first round.** 2. **In every later round, play D regardless
# of what the opponent did before.** 3. **Do not switch to C at any point.**

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# 1. Start by playing **C**.   2. On each later round, if the opponent played
# **C** in the previous round, play **C**.   3. If the opponent played **D** in
# the previous round, play **D** in the next round.   4. After that one-round
# punishment, go back to **C** unless the opponent defects again.

class Cooperative_1(LLM_Strategy):
  n = 1
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_next = False
          return axl.Action.C
  
      if getattr(self, "_punish_next", False):
          self._punish_next = False
          return axl.Action.D
  
      if opponent.history and opponent.history[-1] == axl.Action.D:
          self._punish_next = True
          return axl.Action.D
  
      return axl.Action.C



# 1. In round 1, defect.   2. In every later round, if the opponent cooperated
# in the previous round, cooperate; if the opponent defected in the previous
# round, defect.   3. Continue this rule for all 1000 rounds.

class Neutral_1(LLM_Strategy):
  n = 1
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return opponent.history[-1]



# 1. Defect in the first round.   2. If the opponent cooperated in the previous
# round, defect again.   3. If the opponent defected in the previous round,
# defect again.   4. Repeat this for all 1000 rounds.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# 1. Play C in the first round.   2. In each later round, if the opponent
# cooperated in the previous round, play C.   3. If the opponent defected in the
# previous round, play D for one round only, then return to C unless they defect
# again.   4. If the opponent’s previous move is unavailable or unclear, play C.
# 5. In the final few rounds, continue following the same rule rather than
# switching to defection.

class Cooperative_2(LLM_Strategy):
  n = 2
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_opponent_defection = False
          return axl.Action.C
  
      if len(opponent.history) == 0:
          return axl.Action.C
  
      last_opp_move = opponent.history[-1]
  
      if last_opp_move == axl.Action.D:
          if getattr(self, "_last_opponent_defection", False):
              self._last_opponent_defection = False
              return axl.Action.C
          self._last_opponent_defection = True
          return axl.Action.D
  
      self._last_opponent_defection = False
      return axl.Action.C



# 1. **In round 1, cooperate.** 2. **In each later round, copy the opponent’s
# previous move.** 3. **If the opponent cooperated last round, cooperate this
# round.** 4. **If the opponent defected last round, defect this round.** 5.
# **Continue this rule through round 1000.**

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



# 1. Start by playing **C** in round 1.   2. If the opponent played **C** in the
# previous round, play **C** again.   3. If the opponent played **D** in the
# previous round, play **D** in the next round.   4. After any round in which
# both players played **D**, keep playing **D** until the opponent plays **C**
# again.   5. If the opponent returns to **C**, switch back to **C** as well.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._d_lock = False
          return axl.Action.C
  
      if self._d_lock:
          if opponent.history[-1] == axl.Action.C:
              self._d_lock = False
              return axl.Action.C
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          if self.history[-1] == axl.Action.D:
              self._d_lock = True
          return axl.Action.D
  
      return axl.Action.C



# 1. Play C in round 1.   2. In every later round, if the opponent played C in
# the previous round, play C.   3. If the opponent played D in the previous
# round, play D in the next round.   4. After one round of punishment, if the
# opponent goes back to C, go back to C as well; if they keep playing D, keep
# playing D.   5. In the final round, play D.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Cooperate in the first round.   2. If the opponent cooperated in the
# previous round, cooperate.   3. If the opponent defected in the previous
# round, defect once.   4. If the opponent cooperates again after defecting,
# return to cooperation.   5. In the last round, defect.

class Neutral_3(LLM_Strategy):
  n = 3
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_once = False
          return axl.Action.C
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          if not getattr(self, "_defect_once", False):
              self._defect_once = True
              return axl.Action.D
          return axl.Action.D
  
      self._defect_once = False
      return axl.Action.C



# 1. **Play D in round 1.**   2. **If the opponent played C in the previous
# round, play D in the next round.**   3. **If the opponent played D in the
# previous round, play D in the next round.**   4. **Continue playing D for
# every remaining round.**

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# 1. Play C in round 1.   2. In every later round, if the opponent played C in
# the previous round, play C.   3. If the opponent played D in the previous
# round, play D in the next round.   4. Keep playing D after a defection until
# the opponent plays C in a round; then switch back to C in the following round.
# 5. Continue this rule for all 1000 rounds.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Cooperate in round 1. 2. In every later round, cooperate if the opponent
# cooperated in the previous round. 3. If the opponent defected in the previous
# round, defect in the next round. 4. If the opponent defects again, keep
# defecting until they cooperate. 5. As soon as the opponent cooperates again,
# switch back to cooperating.

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



# 1. **Play D in the first round.**  2. **If the opponent played C in the
# previous round, play D.**  3. **If the opponent played D in the previous
# round, play D.**  4. **Continue playing D for every remaining round.**

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# 1. **Play C in the first round.** 2. **In every later round, play C if and
# only if the opponent played C in the previous round.** 3. **If the opponent
# played D in the previous round, play D in the next round.** 4. **Keep
# following this rule for all 1000 rounds.**

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



# 1. Cooperate in round 1 if you want to encourage mutual cooperation; otherwise
# defect in round 1 to avoid giving up the first-round payoff. 2. From round 2
# onward, play the same move your opponent played in the previous round. 3. If
# the opponent defects in the previous round, defect in the next round. 4. If
# the opponent cooperates in the previous round, cooperate in the next round. 5.
# Continue this rule for all 1000 rounds.

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



# 1. Start by playing **C**.   2. If the opponent played **C** in the previous
# round, play **C** again.   3. If the opponent played **D** in the previous
# round, play **D** in the next round.   4. Keep playing **D** until the
# opponent plays **C** again.   5. Once the opponent returns to **C**, switch
# back to **C** and continue cooperating as long as they cooperate.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# 1. Play **C** in round 1.   2. If the opponent played **C** in the previous
# round, play **C**.   3. If the opponent played **D** in the previous round,
# play **D**.   4. Keep playing **D** until the opponent plays **C** in a round;
# then switch back to **C** in the next round.   5. If the opponent defects
# again after you have returned to **C**, repeat the same rule: defect until
# they cooperate, then cooperate again.

class Cooperative_6(LLM_Strategy):
  n = 6
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._switch_to_cooperate = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          self._switch_to_cooperate = True
      elif opponent.history[-1] == axl.Action.D:
          self._switch_to_cooperate = False
  
      if self._switch_to_cooperate:
          return axl.Action.C
      return axl.Action.D



# 1. In the first round, play **D**.   2. In every later round, **play D if the
# opponent played D in the previous round**.   3. **Play C only if the opponent
# has played C in the previous round and has not defected in the last two
# rounds**.   4. Otherwise, **play D** for the rest of the game.

class Neutral_6(LLM_Strategy):
  n = 6
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.C and opponent.history[-2] != axl.Action.D:
              return axl.Action.C
  
      return axl.Action.D



# 1. Defect in round 1.   2. In every later round, defect unless the opponent
# cooperated in the immediately previous round.   3. If the opponent cooperated
# in the immediately previous round, cooperate in the current round.   4. If the
# opponent defects in the immediately previous round, defect in the current
# round.   5. Repeat this rule set for all 1000 rounds.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# 1. Cooperate in the first round. 2. If the opponent cooperated in the previous
# round, cooperate again. 3. If the opponent defected in the previous round,
# defect in the next round. 4. If the opponent returns to cooperation after
# defecting, return to cooperation as well. 5. Continue this pattern through
# round 1000, with the understanding that the last round should follow the same
# rule as the others.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# 1. Cooperate in round 1. 2. If the opponent cooperated in the previous round,
# cooperate again. 3. If the opponent defected in the previous round, defect
# once in the next round. 4. If the opponent cooperates after that, return to
# cooperating. 5. Repeat this pattern for all 1000 rounds.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Defect in round 1.   2. Defect in every later round as well.   3. Never
# cooperate, since defecting gives a higher payoff against either possible
# opponent action.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# 1. **Cooperate in the first round.**   2. **If the opponent cooperated in the
# previous round, cooperate again.**   3. **If the opponent defected in the
# previous round, defect for the next 2 rounds.**   4. **After those 2 rounds of
# retaliation, return to cooperation unless the opponent defects again.**   5.
# **In the last 5 rounds, keep cooperating only if the opponent has cooperated
# in the previous 3 rounds; otherwise defect.**

class Cooperative_8(LLM_Strategy):
  n = 8
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._retaliate_rounds = 0
          return axl.Action.C
  
      rounds_left = 1000 - len(self.history)
  
      if rounds_left <= 5:
          if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]:
              return axl.Action.C
          return axl.Action.D
  
      if getattr(self, "_retaliate_rounds", 0) > 0:
          self._retaliate_rounds -= 1
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          self._retaliate_rounds = 1
          return axl.Action.D
  
      return axl.Action.C



# 1. Play D in the first round.   2. In every later round, if your opponent
# played C in the previous round, play D.   3. If your opponent played D in the
# previous round, play D.   4. Continue this rule for all 1000 rounds.

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
      return axl.Action.D



# 1. Defect in the first round.   2. Defect in every later round, regardless of
# what the opponent does.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# 1. In round 1, play **C**.   2. In every later round, play **C** if your
# opponent played **C** in the previous round.   3. If your opponent played
# **D** in the previous round, play **D** in the next round.   4. If your
# opponent returns to **C** after defecting, return to **C** immediately on the
# following round.   5. Continue this rule for all 1000 rounds.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# 1. **In round 1, defect.** 2. **In every later round, if the opponent
# cooperated in the previous round, cooperate.** 3. **If the opponent defected
# in the previous round, defect.** 4. **If the opponent’s behavior changes back
# to cooperation, switch back to cooperation immediately.**

class Neutral_9(LLM_Strategy):
  n = 9
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# 1. Play D in the first round.   2. In every later round, play D regardless of
# what the opponent played before.   3. Do not switch to C at any point.

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Cooperate in the first round.  After that, on each round: - If the opponent
# cooperated in the previous round, cooperate. - If the opponent defected in the
# previous round, defect this round. - Keep defecting every round until the
# opponent cooperates in a round, then switch back to cooperating on the next
# round.  This means you cooperate by default, but immediately punish any
# defection and only return to cooperation after the opponent has shown
# cooperation again.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Cooperate in the first round. 2. In every later round, cooperate if the
# opponent cooperated in the previous round. 3. In every later round, defect if
# the opponent defected in the previous round. 4. If both players defected in
# the previous round, keep defecting until the opponent cooperates again.

class Neutral_10(LLM_Strategy):
  n = 10
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_both_defected = False
          return axl.Action.C
  
      if self._last_both_defected:
          if opponent.history[-1] == axl.Action.C:
              self._last_both_defected = False
              return axl.Action.C
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          self._last_both_defected = True
          return axl.Action.D
  
      return axl.Action.D



# 1. Start by playing D in the first round.   2. If the opponent ever plays D,
# keep playing D in every later round.   3. If the opponent has played C in
# every round so far, continue playing D anyway to exploit the higher payoff
# from defecting against cooperation.   4. Never switch to C.

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
  
      return axl.Action.D



# 1. Cooperate in round 1.   2. In each later round, cooperate if the opponent
# cooperated in the previous round.   3. Defect if the opponent defected in the
# previous round.   4. If the opponent cooperates again after defecting,
# immediately return to cooperation.   5. In the final round, cooperate unless
# the opponent defected in the previous round.

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
  
      # Final round: cooperate unless the opponent defected in the previous round.
      if len(self.history) == 999:
          return axl.Action.D if opponent.history[-1] == axl.Action.D else axl.Action.C
  
      # Otherwise, mirror the opponent's previous move.
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# 1. Cooperate in the first round. 2. In every later round, cooperate only if
# the opponent cooperated in the previous round. 3. If the opponent defected in
# the previous round, defect in the next round. 4. After any mutual defection,
# continue defecting until the opponent cooperates in a round. 5. Once the
# opponent cooperates again, return to cooperating in the next round.

class Neutral_11(LLM_Strategy):
  n = 11
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_until_cooperate = False
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          self._defect_until_cooperate = True
  
      if self._defect_until_cooperate:
          if opponent.history[-1] == axl.Action.C:
              self._defect_until_cooperate = False
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# 1. Start by playing D in the first round.   2. If the opponent played C in the
# previous round, keep playing D.   3. If the opponent played D in the previous
# round, keep playing D.   4. Continue this for all 1000 rounds.

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
      return axl.Action.D



# 1. Play C in the first round. 2. In each round after that, copy your
# opponent’s previous move. 3. If the opponent cooperated in the previous round,
# play C. 4. If the opponent defected in the previous round, play D. 5. If the
# opponent’s previous move is unavailable or unclear, play C. 6. In the final
# rounds, continue using the same rule rather than changing behavior just
# because the game is ending.

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
  
      try:
          last_move = opponent.history[-1]
      except IndexError:
          return axl.Action.C
  
      if last_move == axl.Action.C:
          return axl.Action.C
      elif last_move == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# 1. Play D in the first round. 2. If the opponent played C in the previous
# round, play D. 3. If the opponent played D in the previous round, play D. 4.
# Continue this for all 1000 rounds.

class Neutral_12(LLM_Strategy):
  n = 12
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return axl.Action.D



# 1. Play D in round 1. 2. In every later round, play D if the opponent played D
# in the previous round. 3. If the opponent played C in the previous round,
# still play D.

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
      return axl.Action.D



# Cooperate in the first round.  After that: - If your opponent cooperated in
# the previous round, cooperate. - If your opponent defected in the previous
# round, defect. - If the opponent has just returned to cooperation after
# defecting, immediately return to cooperation as well.  Use this rule for all
# 1000 rounds.

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
  
      return axl.Action.D



# 1. Cooperate in the first round.   2. In every later round, cooperate if the
# opponent cooperated in the previous round.   3. In every later round, defect
# if the opponent defected in the previous round.   4. If both players defect in
# a round, return to cooperating in the next round if the opponent cooperates.
# 5. Continue following these rules through round 1000.

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
      else:
          return axl.Action.D



# 1. Defect in round 1.   2. In every round after that, defect if the opponent
# defected in the previous round.   3. Cooperate only if the opponent cooperated
# in the previous round and also cooperated in the round before that.   4. If
# the opponent defects in any round, return to defecting immediately in the next
# round.   5. In the final 10 rounds, defect in every round regardless of the
# opponent’s actions.

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
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      if len(opponent.history) < 2:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if opponent.history[-2] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# 1. Cooperate in the first round.   2. In each later round, copy your
# opponent’s previous move.   3. If your opponent cooperated in the previous
# round, cooperate now.   4. If your opponent defected in the previous round,
# defect now.   5. If you cannot reliably observe the opponent’s previous move,
# default to defection for that round.   6. Continue this rule through round
# 1000.

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
  
      try:
          return opponent.history[-1]
      except Exception:
          return axl.Action.D



# 1. In the first round, play D. 2. In every later round, play D regardless of
# what your opponent did before.

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
      return axl.Action.D



# Defect in every round from round 1 to round 1000.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# 1. **Play C in the first round.** 2. **In every later round, play C if the
# opponent played C in the previous round.** 3. **In every later round, play D
# if the opponent played D in the previous round.**

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
      else:
          return axl.Action.D



# 1. **Round 1:** play **C**.   2. **From round 2 onward:** play **C** if the
# opponent played **C** in the previous round.   3. **From round 2 onward:**
# play **D** if the opponent played **D** in the previous round.

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



# Play C in the first round.  Then, in every later round: 1. If your opponent
# played C in the previous round, play D. 2. If your opponent played D in the
# previous round, play D.  In short, always defect.

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
      return axl.Action.D



# 1. Play **C** in the first round.   2. In each later round, **play C only if
# the opponent played C in the previous round and has not defected in the last
# two rounds**.   3. If the opponent **defects once**, respond by **playing D
# for the next two rounds**.   4. After those two punishment rounds, **return to
# C only if the opponent has played C in both of the last two rounds**.   5. If
# the opponent **defects again at any point**, restart the two-round punishment
# rule.   6. In the final rounds, **continue following the same rule without
# special exceptions**.

class Cooperative_16(LLM_Strategy):
  n = 16
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_rounds_remaining = 0
          return axl.Action.C
  
      if getattr(self, "_punish_rounds_remaining", None) is None:
          self._punish_rounds_remaining = 0
  
      if self._punish_rounds_remaining > 0:
          self._punish_rounds_remaining -= 1
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          self._punish_rounds_remaining = 1
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.C, axl.Action.C]:
          return axl.Action.C
  
      return axl.Action.D



# 1. Play **D** in the first round.   2. In every later round, if the opponent
# played **C** in the previous round, play **D**.   3. If the opponent played
# **D** in the previous round, also play **D**.

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
      return axl.Action.D



# 1. Start by cooperating in round 1.   2. If the opponent cooperated in the
# previous round, cooperate again.   3. If the opponent defected in the previous
# round, defect in the next round.   4. Keep following the opponent’s last move
# for the rest of the 1000 rounds.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]



# 1. Cooperate in round 1.   2. In rounds 2 through 999, cooperate if the
# opponent cooperated in the previous round; defect if the opponent defected in
# the previous round.   3. In round 1000, defect.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1]



# 1. Cooperate in the first round. 2. In every later round, cooperate if the
# opponent cooperated in the previous round. 3. In every later round, defect if
# the opponent defected in the previous round.

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



# 1. Defect in the first round.   2. If the opponent defected in the previous
# round, defect again.   3. If the opponent cooperated in the previous round,
# defect anyway.   4. Continue defecting in every round for all 1000 rounds.

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# 1. Play C in round 1.   2. In every later round, if the opponent played C in
# the previous round, play C.   3. If the opponent played D in the previous
# round, play D in the current round.   4. If both players played D in the
# previous round, keep playing D until the opponent plays C in a later round.
# 5. As soon as the opponent plays C again, switch back to C in the next round
# and continue cooperating unless they defect again.

class Cooperative_18(LLM_Strategy):
  n = 18
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_mode = False
          return axl.Action.C
  
      if self._defect_mode:
          if opponent.history[-1] == axl.Action.C:
              self._defect_mode = False
              return axl.Action.C
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          self._defect_mode = True
          return axl.Action.D
  
      return axl.Action.C



# 1. Cooperate in the first round. 2. In every later round, do whatever the
# opponent did in the previous round. 3. If the opponent cooperated last round,
# cooperate. 4. If the opponent defected last round, defect. 5. If the
# opponent’s previous move is unavailable or unclear, cooperate.

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
  
      if len(opponent.history) == 0:
          return axl.Action.C
  
      last_move = opponent.history[-1]
      if last_move == axl.Action.C:
          return axl.Action.C
      if last_move == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Defect in the first round. 2. If the opponent defected in the previous
# round, defect again. 3. If the opponent cooperated in the previous round,
# cooperate in the next round only if you want to test for reciprocity;
# otherwise defect. 4. For maximizing immediate payoff in an aggressive way,
# default to defecting in every round unless you are deliberately trying to
# sustain mutual cooperation. 5. In practice, keep defecting for the rest of the
# 1000 rounds unless the opponent’s repeated cooperation makes a cooperative
# phase clearly more profitable.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._cooperative_phase = False
          self._coop_probe_rounds = 0
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          self._cooperative_phase = False
          self._coop_probe_rounds = 0
          return axl.Action.D
  
      if self._cooperative_phase:
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          self._cooperative_phase = False
          self._coop_probe_rounds = 0
          return axl.Action.D
  
      if opponent.history.cooperations >= 3 and self.history.defections >= 1:
          recent_self = self.history[-3:]
          recent_opp = opponent.history[-3:]
          if recent_opp.count(axl.Action.C) == 3 and recent_self.count(axl.Action.D) == 3:
              self._cooperative_phase = True
              self._coop_probe_rounds = 0
              return axl.Action.C
  
      return axl.Action.D



# 1. Cooperate in the first round.   2. In every later round, copy your
# opponent’s previous move.   3. If your opponent cooperated in the previous
# round, cooperate now.   4. If your opponent defected in the previous round,
# defect now.   5. If the opponent’s previous move cannot be observed or is
# unclear, cooperate.   6. Apply this rule in every round through round 1000.

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
  
      try:
          last_move = opponent.history[-1]
      except IndexError:
          return axl.Action.C
  
      if last_move == axl.Action.C:
          return axl.Action.C
      if last_move == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. **Round 1:** Play **D**. 2. **If the opponent played C in the previous
# round:** Play **D**. 3. **If the opponent played D in the previous round:**
# Play **D**. 4. **Continue this rule for all 1000 rounds.**

class Neutral_19(LLM_Strategy):
  n = 19
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# 1. Start by playing D.   2. If the opponent plays C, keep playing D.   3. If
# the opponent plays D, keep playing D.   4. Repeat this for all 1000 rounds.

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
      return axl.Action.D



# 1. Start by playing C. 2. On each later round, play C if the opponent played C
# on the previous round. 3. Play D if the opponent played D on the previous
# round. 4. If both players played D in the previous round, try C again on the
# next round to restore cooperation. 5. In the final round, play D.

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



# 1. Play D in the first round. 2. If the opponent played C in the previous
# round, play D. 3. If the opponent played D in the previous round, play D. 4.
# Continue playing D for all remaining rounds.

class Neutral_20(LLM_Strategy):
  n = 20
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return axl.Action.D



# 1. **Play D in round 1.**   2. **Play D in every later round, regardless of
# what your opponent did before.**   3. **Continue this for all 1000 rounds.**

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# 1. Play C in the first round. 2. In every later round, play C if the opponent
# played C in the previous round. 3. In every later round, play D if the
# opponent played D in the previous round. 4. Keep following this rule for all
# 1000 rounds.

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



# 1. Play **C** in the first round unless you have strong reason to expect the
# opponent will defect immediately; otherwise play **D**.   2. In each later
# round, compare the opponent’s last move:    - if the opponent played **C**,
# play **C**;    - if the opponent played **D**, play **D**.   3. If the
# opponent’s behavior is inconsistent or noisy, keep following the same rule and
# do not switch away from it unless a clear pattern of repeated defection
# appears.

class Neutral_21(LLM_Strategy):
  n = 21
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          recent_opponent_defections = opponent.history[-5:].count(axl.Action.D)
          if recent_opponent_defections >= 4:
              return axl.Action.D
          return axl.Action.C
  
      last_opponent_move = opponent.history[-1]
  
      if last_opponent_move == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# 1. Cooperate in the first round. 2. If the opponent cooperates, keep
# cooperating. 3. If the opponent defects, defect in every remaining round. 4.
# If the opponent ever defects after a period of cooperation, never return to
# cooperation.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_forever = False
          return axl.Action.C
  
      if getattr(self, "_defect_forever", False):
          return axl.Action.D
  
      if opponent.history and opponent.history[-1] == axl.Action.D:
          self._defect_forever = True
          return axl.Action.D
  
      return axl.Action.C



# 1. **Cooperate in the first round.** 2. **From rounds 2 to 999, cooperate if
# and only if the opponent cooperated in the previous round; otherwise defect.**
# 3. **In round 1000, defect.**

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1] if opponent.history else axl.Action.D



# 1. In round 1, play **D**.   2. In every later round, play **D** if the
# opponent played **D** in the previous round.   3. In every later round, play
# **C** if the opponent played **C** in the previous round.   4. Since the game
# ends after 1000 rounds, do not use any special final-round rule.

class Neutral_22(LLM_Strategy):
  n = 22
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# 1. **Defect in every round from round 1 to round 1000.**   2. **Do not switch
# to cooperation at any point, regardless of the opponent’s previous actions.**

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# 1. Play C in the first round. 2. Keep playing C as long as the opponent played
# C in the previous round. 3. If the opponent plays D in any round, switch to D
# in the next round. 4. Stay with D for one round only. 5. After that one D
# round, return to C if the opponent played C in the previous round; otherwise
# keep playing D for one more round and check again. 6. Repeat this pattern for
# all 1000 rounds.

class Cooperative_23(LLM_Strategy):
  n = 23
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._d_streak = 0
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          self._d_streak = 0
          return axl.Action.C
  
      self._d_streak += 1
      return axl.Action.D



# 1. Cooperate in the first round. 2. In each later round, if the opponent
# cooperated in the previous round, cooperate. 3. In each later round, if the
# opponent defected in the previous round, defect. 4. If the opponent’s previous
# move is unavailable or unclear, defect.

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
  
      if len(opponent.history) == 0:
          return axl.Action.D
  
      last_move = opponent.history[-1]
      if last_move == axl.Action.C:
          return axl.Action.C
      if last_move == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.D



# 1. Play D in the first round. 2. In every later round, play D if the opponent
# played C in the previous round. 3. In every later round, play D if the
# opponent played D in the previous round. 4. Do not switch to C at any point.

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
      return axl.Action.D



# 1. Cooperate in the first round. 2. In every round after that, cooperate if
# the opponent cooperated in the previous round. 3. Defect only if the opponent
# defected in the previous round. 4. If the opponent returns to cooperating,
# immediately return to cooperating as well. 5. In the final round, cooperate
# unless the opponent defected in the immediately preceding round.

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
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# 1. Cooperate in round 1.   2. In every later round, copy the opponent’s
# previous move: cooperate if they cooperated last round, and defect if they
# defected last round.   3. If the opponent defects, keep defecting until they
# cooperate again.   4. Do not use any special final-round rule.

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



# 1. **Defect in round 1.**  2. **In every later round, defect if the opponent
# defected in the previous round.**  3. **If the opponent cooperated in the
# previous round, defect again.**  4. **Never cooperate at any point.**  5.
# **Continue defecting through round 1000.**

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
      return axl.Action.D



# 1. **Cooperate in round 1.**   2. **In every later round, play the same move
# your opponent played in the previous round.**   3. **If the opponent
# cooperates, cooperate.**   4. **If the opponent defects, defect in the next
# round.**

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



# 1. Cooperate in the first round. 2. In every later round, cooperate if the
# opponent cooperated in the previous round. 3. Defect if the opponent defected
# in the previous round. 4. If both players defected in the previous round,
# cooperate again only after the opponent cooperates once. 5. Continue following
# the opponent’s most recent move for the rest of the game.

class Neutral_25(LLM_Strategy):
  n = 25
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._waiting_for_cooperation = False
          return axl.Action.C
  
      if getattr(self, "_waiting_for_cooperation", False):
          if opponent.history[-1] == axl.Action.C:
              self._waiting_for_cooperation = False
              return axl.Action.C
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          if self.history[-1] == axl.Action.D:
              self._waiting_for_cooperation = True
          return axl.Action.D
  
      return axl.Action.C