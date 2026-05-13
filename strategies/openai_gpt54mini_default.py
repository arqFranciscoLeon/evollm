import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# 1. Start by defecting in the first round.   2. In every later round, defect if
# the opponent cooperated in the previous round.   3. If the opponent defected
# in the previous round, defect again.   4. Never cooperate.

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
      return axl.Action.D



# Use a simple **cooperate-first, retaliate-if-exploited** strategy:  1. **Start
# by cooperating** in round 1.   2. **If the opponent cooperated in the previous
# round, cooperate again.**   3. **If the opponent defected in the previous
# round, defect in the next round.**   4. **After one round of retaliation,
# return to cooperation if the opponent cooperates again.**   5. **Repeat this
# rule for all 1000 rounds.**  This strategy aims to keep both players at the
# mutually beneficial **C/C payoff of 3** as much as possible, while
# discouraging the opponent from defecting by responding immediately.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Start by playing C in the first round.   2. In each later round, do the
# same move your opponent played in the previous round.   3. If the opponent
# defected in the previous round, defect in the next round.   4. If the opponent
# cooperated in the previous round, cooperate in the next round.   5. Keep
# following this rule for all 1000 rounds.

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



# 1. Start by playing **D**.   2. On every later round, play **D** again.   3.
# Do **not** switch to **C** under any condition.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Use a simple **tit-for-tat** strategy:  1. **Start by cooperating** in round
# 1. 2. **In every later round, do whatever your opponent did in the previous
# round**:    - if they played **C**, play **C**;    - if they played **D**,
# play **D**.  This strategy is cooperative because it begins with cooperation
# and keeps cooperating as long as the opponent does. It also responds to
# defection by matching it, which helps protect your payoff in this payoff
# structure.

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



# Use a simple neutral rule:  1. Cooperate in the first round. 2. If the
# opponent cooperated in the previous round, cooperate again. 3. If the opponent
# defected in the previous round, defect in the next round. 4. Keep repeating
# this rule for all 1000 rounds.  This is a straightforward “copy the opponent’s
# last move” strategy. It is neutral because it neither forgives immediately nor
# escalates unnecessarily, and it responds directly to the payoff structure by
# rewarding mutual cooperation and matching defection.

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



# 1. Start by playing D in the first round.   2. If the opponent played C in the
# previous round, play D again.   3. If the opponent played D in the previous
# round, also play D again.   4. Continue playing D in every round for all 1000
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



# Use a simple **conditional cooperation** strategy:  1. **Start by
# cooperating** in the first round. 2. **Continue cooperating** as long as your
# opponent cooperates. 3. **If your opponent defects in any round, defect in the
# next round.** 4. **After a defection, return to cooperation only if your
# opponent cooperates again.** 5. **Repeat this rule for all 1000 rounds.**
# This strategy aims to keep mutual cooperation going, since **C/C gives 3
# each**, which is better than the **1 each** from mutual defection, while still
# protecting you from being exploited when the opponent defects.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Use a simple neutral rule:  1. **Start by cooperating in round 1.**   2. **If
# the opponent cooperated in the previous round, cooperate again.**   3. **If
# the opponent defected in the previous round, defect in the next round.**   4.
# **If the opponent returns to cooperation, return to cooperation as well.**
# This is a **neutral, reciprocal strategy**: it does not try to punish beyond
# matching the opponent’s latest move, and it aims to keep mutual cooperation
# when possible while avoiding repeated exploitation.

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



# Use an aggressive exploit-first strategy:  1. Start by defecting in round 1.
# 2. If the opponent defects in the previous round, defect again. 3. If the
# opponent cooperates in the previous round, defect again. 4. Continue defecting
# for all 1000 rounds.  This is the simplest payoff-maximizing aggressive rule
# for this game, since defecting always gives you at least as much as
# cooperating and gives you more whenever the opponent cooperates.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# 1. Start by playing **C** in round 1.   2. In every later round, **play the
# same move your opponent played in the previous round**.   3. If the opponent
# cooperated last round, **cooperate**.   4. If the opponent defected last
# round, **defect**.   5. If the opponent returns to cooperation, **return to
# cooperation immediately**.    This is a simple **tit-for-tat** strategy: it
# begins cooperatively, rewards cooperation, and responds to defection only by
# mirroring it.

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



# Use a neutral, simple rule:  1. Start by cooperating in round 1.   2. In every
# later round, copy your opponent’s previous move.   3. If your opponent
# cooperated last round, cooperate this round.   4. If your opponent defected
# last round, defect this round.    This keeps you neutral: it rewards
# cooperation when the opponent cooperates, but does not keep cooperating after
# being exploited.

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



# Use this simple aggressive strategy:  1. **Defect in round 1.** 2. **If the
# opponent cooperated in the previous round, defect again.** 3. **If the
# opponent defected in the previous round, defect again.** 4. **Keep defecting
# in every round for all 1000 rounds.**  This is the most aggressive and payoff-
# maximizing straightforward approach for these payoffs, since defecting always
# gives you at least as much as cooperating in any single round.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# 1. **Start by cooperating in round 1.**  2. **In every later round, do this:**
# - If your opponent **cooperated in the previous round**, **cooperate**.    -
# If your opponent **defected in the previous round**, **defect**.  3. **If the
# opponent returns to cooperation after defecting, return to cooperation too.**
# This is a simple **tit-for-tat** strategy: it rewards cooperation, responds
# immediately to defection, and restores cooperation as soon as the opponent
# does.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Use a simple neutral strategy:  1. Start by playing C in the first round.   2.
# If the opponent played C in the previous round, play C next.   3. If the
# opponent played D in the previous round, play D next.   4. Keep following this
# rule for all 1000 rounds.    This is a straightforward conditional strategy
# that cooperates when the opponent cooperates and switches to defection after
# any defection.

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