import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# 1. **Start by defecting in round 1.**   2. **In every later round, defect
# again if your opponent defected in the previous round.**   3. **If your
# opponent cooperated in the previous round, defect anyway.**    This strategy
# is simple and maximally aggressive: it always chooses **D**, since defecting
# gives you the highest immediate payoff against both cooperation and defection.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# 1. Start by cooperating in the first round.   2. In every later round, do what
# your opponent did in the previous round.   3. If your opponent cooperated last
# round, cooperate this round.   4. If your opponent defected last round, defect
# this round.   5. If the opponent ever returns to cooperation, immediately
# return to cooperation too.    This is a simple reciprocal strategy that aims
# to sustain mutual cooperation for 3 points each round, while responding to
# defection by switching to defection so you do not keep receiving the worst
# payoff.

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
      return opponent.history[-1]



# Use a simple, neutral rule:  1. **Start by cooperating** in the first round.
# 2. **After that, copy the opponent’s previous move**:      - if the opponent
# played **C** last round, play **C** this round;      - if the opponent played
# **D** last round, play **D** this round.   3. **If the opponent ever returns
# to cooperation, cooperate again immediately.**   4. **Keep following this rule
# for all 1000 rounds.**  This strategy is neutral because it does not try to
# exploit the opponent, but it avoids staying cooperative against defection and
# keeps cooperation going when the opponent is cooperative.

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
  
      return opponent.history[-1]



# Play D in every round.  If you want a slightly less rigid version, use this
# rule: 1. Start by playing D. 2. If the opponent plays C, keep playing D. 3. If
# the opponent plays D, keep playing D.  This is the most aggressive simple
# strategy because defecting always gives you at least as much as cooperating in
# every round, and more whenever the opponent cooperates.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating.  Then, in every round after that: - If your opponent
# cooperated in the previous round, cooperate. - If your opponent defected in
# the previous round, defect in the next round.  If the opponent returns to
# cooperation, immediately return to cooperation as well.  This is a simple
# “cooperate unless they defect last round” strategy that encourages mutual
# cooperation while punishing defection.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Start by cooperating in the first round.   2. In every later round, copy
# your opponent’s previous move: if they cooperated, cooperate; if they
# defected, defect.   3. If the opponent has no previous move to copy,
# cooperate.

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
      if len(opponent.history) == 0:
          return axl.Action.C
      return opponent.history[-1]



# 1. **Defect on the first round.**   2. **In every later round, defect again if
# your opponent defected in the previous round.**   3. **If your opponent
# cooperated in the previous round, defect anyway.**   4. **If your opponent
# ever cooperates consistently, keep defecting.**    This is a simple always-
# defect strategy, which is the most aggressive way to maximize your own payoff
# in this payoff structure.

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
      return axl.Action.D



# 1. Start by playing **C**.   2. In every later round, **play C if your
# opponent played C in the previous round**.   3. **Play D if your opponent
# played D in the previous round**.   4. If the opponent returns to **C** after
# defecting, **return to C immediately**.   5. Keep following this rule for all
# 1000 rounds.    This is a simple cooperative strategy: it rewards cooperation,
# retaliates once after defection, and restores cooperation as soon as the
# opponent cooperates again.

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
  
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# Use a simple neutral strategy:  1. Start by cooperating in the first round.
# 2. In every later round, do the same move your opponent used in the previous
# round.   3. If the opponent cooperated last round, cooperate.   4. If the
# opponent defected last round, defect.    This is a straightforward reciprocal
# strategy: it rewards cooperation, avoids being exploited repeatedly, and keeps
# defecting only when the opponent does.

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
      return opponent.history[-1]



# Use this strategy:  1. Start by playing **D**. 2. In every later round, **play
# D** again. 3. Never switch to **C**, regardless of what the opponent does.
# This is the most aggressive strategy and maximizes your immediate payoff in
# every round: you get **5** if the opponent cooperates, and **1** if they
# defect.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Use a simple tit-for-tat strategy:  1. Cooperate in the first round. 2. In
# every later round, do whatever your opponent did in the previous round. 3. If
# the opponent cooperated last round, cooperate now. 4. If the opponent defected
# last round, defect now. 5. Keep following this rule for all 1000 rounds.  This
# starts with cooperation to build mutual high payoffs, and then rewards
# cooperation while responding immediately to defection.

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
      return opponent.history[-1]



# Use a neutral, simple conditional strategy:  1. **Start by cooperating.** 2.
# **If the opponent cooperated in the previous round, cooperate again.** 3. **If
# the opponent defected in the previous round, defect in the next round.** 4.
# **If the opponent returns to cooperation, return to cooperation.**  This keeps
# cooperation when it is mutually beneficial, but switches to defection
# immediately after being exploited, so it stays neutral and protects your
# payoff over 1000 rounds.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# Use a mostly defect strategy:  1. **Start by defecting.** 2. **If your
# opponent cooperates in the previous round, defect again.** 3. **If your
# opponent defects in the previous round, keep defecting.** 4. **Only cooperate
# if you need to test for cooperation after a long streak of mutual defection;
# otherwise always defect.**  This is aggressive because defection gives you the
# highest immediate payoff against cooperation and avoids being exploited.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._test_after_dd_streak = 0
          return axl.Action.D
  
      # Mostly defect: defect unless we are deliberately probing after a long
      # streak of mutual defection.
      if len(self.history) >= 2:
          last_two_self = self.history[-2:]
          last_two_opp = opponent.history[-2:]
          if last_two_self == [axl.Action.D, axl.Action.D] and last_two_opp == [axl.Action.D, axl.Action.D]:
              self._test_after_dd_streak += 1
          else:
              self._test_after_dd_streak = 0
      else:
          self._test_after_dd_streak = 0
  
      # Only cooperate occasionally to test for cooperation after a long
      # mutual-defection streak; otherwise always defect.
      if self._test_after_dd_streak >= 5:
          self._test_after_dd_streak = 0
          return axl.Action.C
  
      return axl.Action.D



# 1. Start by cooperating in round 1.   2. In each later round, cooperate if
# your opponent cooperated in the previous round.   3. Defect if your opponent
# defected in the previous round.   4. If the opponent returns to cooperation,
# return to cooperation immediately.   5. Continue this for all 1000 rounds.
# This is a simple tit-for-tat strategy: it rewards cooperation, punishes
# defection, and aims to keep both players at the mutually beneficial 3-point
# outcome whenever possible.

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
      return opponent.history[-1] if opponent.history else axl.Action.C



# Use a neutral “mirror with fallback” strategy:  1. Cooperate in the first
# round.   2. In every later round, copy your opponent’s previous move:      -
# if they played C last round, play C;      - if they played D last round, play
# D.   3. If the opponent has been defecting repeatedly and you want to avoid
# being stuck in mutual defection, switch to D only when they defect in the
# previous round; otherwise stay with C.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Start by playing D in the first round.   2. If the opponent played C in the
# previous round, play D again.   3. If the opponent played D in the previous
# round, keep playing D.   4. If the opponent ever switches to C after
# defecting, continue playing D.   5. Only consider playing C if doing so is
# needed to encourage a future switch, but otherwise defect for all 1000 rounds.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._encourage_cooperate = False
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.D



# 1. Start by cooperating in round 1.   2. In every later round, do the same
# move your opponent played in the previous round.   3. If your opponent
# cooperated last round, cooperate now.   4. If your opponent defected last
# round, defect now.   5. If the opponent returns to cooperating, return to
# cooperating immediately.

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
      return opponent.history[-1]



# Use a neutral, payoff-maximizing rule:  1. Cooperate on the first round.   2.
# If the opponent cooperated in the previous round, cooperate again.   3. If the
# opponent defected in the previous round, defect in the next round.   4. If the
# opponent returns to cooperation, return to cooperation as well.    This is a
# simple “match the opponent’s last move” strategy, which stays cooperative when
# cooperation is mutual and immediately responds to defection.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Start by playing **D**.   2. In every later round, play **D** again,
# regardless of what the opponent did before.    This is the simplest aggressive
# strategy: **always defect**. It maximizes your immediate payoff in every
# possible situation and is straightforward to apply for all 1000 rounds.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# - Start by playing C. - If the opponent played C in the previous round, play C
# again. - If the opponent played D in the previous round, play D in the next
# round. - After any round in which the opponent returns to playing C, return to
# playing C as well. - Keep following this rule for all 1000 rounds.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D



# - Start by cooperating. - If the opponent cooperates in the current round,
# cooperate in the next round. - If the opponent defects in the current round,
# defect in the next round. - Keep following the opponent’s last move for all
# 1000 rounds. - If the opponent’s behavior is unclear at the start, default to
# cooperation.

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
  
      if opponent.history:
          return opponent.history[-1]
  
      return axl.Action.C



# 1. Start by defecting in the first round.   2. If the opponent cooperates in
# the previous round, defect again.   3. If the opponent defects in the previous
# round, keep defecting.   4. Continue defecting in every round for all 1000
# rounds.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Use a simple **cooperate-first, punish-defection** strategy:  1. **Round 1:**
# Play **C**. 2. **If the opponent played C in the previous round, play C** in
# the next round. 3. **If the opponent played D in the previous round, play D**
# in the next round. 4. **Keep doing this for all 1000 rounds.**  This means you
# cooperate as long as the opponent cooperates, and immediately switch to
# defection after any defection by the opponent.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Use a simple conditional rule:  1. Start by cooperating in the first round. 2.
# If the opponent cooperated in the previous round, cooperate again. 3. If the
# opponent defected in the previous round, defect in the next round. 4. Keep
# following this rule for all 1000 rounds.  This is neutral in the sense that it
# neither blindly cooperates nor always defects: it matches the opponent’s last
# move, which is a straightforward way to avoid being exploited while still
# gaining from mutual cooperation.

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
      return axl.Action.D



# 1. Start by defecting.   2. If the opponent defects in any round, defect in
# every later round.   3. If the opponent cooperates and has never defected
# before, defect anyway to take the higher payoff.   4. Repeat this for all 1000
# rounds.  This is a fully aggressive strategy: always defect, since defection
# gives you 5 against cooperation and still gives 1 against defection, which is
# better than cooperating in either case.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Use a simple tit-for-tat strategy:  1. Cooperate in the first round. 2. In
# every later round, do whatever your opponent did in the previous round:    -
# if they cooperated, cooperate;    - if they defected, defect. 3. If the
# opponent returns to cooperation after defecting, cooperate again in the next
# round. 4. Keep repeating this for all 1000 rounds.  This starts with
# cooperation to build mutual gains, but it punishes defection immediately and
# rewards cooperation as soon as it resumes.

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
      return opponent.history[-1]



# Use a neutral, simple rule:  1. Cooperate on the first round. 2. If the
# opponent cooperated in the previous round, cooperate again. 3. If the opponent
# defected in the previous round, defect in the next round. 4. Keep following
# the opponent’s last move for the rest of the 1000 rounds.  This is a
# straightforward tit-for-tat approach: it rewards cooperation, responds to
# defection, and avoids unnecessary aggression.

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
      return opponent.history[-1]



# Play **D in the first round**.  Then follow this rule in every later round:
# 1. **If the opponent played C in the previous round, play D.**   2. **If the
# opponent played D in the previous round, play D.**  So, **always defect**.
# This is the most aggressive simple strategy and is intended to maximize your
# own payoff in this payoff structure.

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
      return axl.Action.D



# 1. **Start by cooperating in round 1.**  2. **In every later round, do what
# your opponent did in the previous round.**    - If they cooperated last round,
# cooperate now.    - If they defected last round, defect now.  3. **If your
# opponent ever defects, keep defecting until they cooperate again.**    - Once
# they return to cooperation, return to cooperation as well.  This keeps
# cooperation as the default and only switches to defection in response to
# defection, which helps maximize total payoff over 1000 rounds.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Use a simple conditional strategy:  1. Start by cooperating in round 1. 2. If
# the opponent cooperated in the previous round, cooperate again. 3. If the
# opponent defected in the previous round, defect in the next round. 4. If the
# opponent returns to cooperating, return to cooperating as well.  This is a
# neutral tit-for-tat approach: it rewards cooperation, matches defection, and
# aims to maximize long-run payoff by sustaining mutual cooperation when
# possible.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Play **Defect (D)** in every round.  - **Always defect**, regardless of what
# the opponent does. - If the opponent cooperates, defect to get **5** instead
# of **3**. - If the opponent defects, still defect because **1** is better than
# risking **0**. - Do this for all **1000 rounds**.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Use a simple **cooperate-first, retaliate-on-defection** strategy:  1. **Start
# by cooperating** in round 1. 2. **If your opponent cooperated in the previous
# round, cooperate again**. 3. **If your opponent defected in the previous
# round, defect in the next round**. 4. **If the opponent returns to
# cooperation, return to cooperation immediately**.  This keeps cooperation
# going when possible, but protects you from being exploited.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Use a neutral, conditional rule:  1. Start by playing C in round 1. 2. After
# that, play C if the opponent played C in the previous round. 3. Play D if the
# opponent played D in the previous round. 4. If you ever see a clear pattern of
# repeated defection, keep playing D until the opponent returns to C. 5. If the
# opponent returns to C, return to C as well.  This keeps cooperation when it is
# mutually beneficial, but switches to defection immediately after the opponent
# defects, which protects you from being exploited.

class Neutral_11(LLM_Strategy):
  n = 11
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defection_streak = 0
          return axl.Action.C
  
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.D:
          self._defection_streak += 1
      else:
          self._defection_streak = 0
  
      if self._defection_streak > 0:
          return axl.Action.D
  
      return axl.Action.C



# Use an aggressive mostly-defect strategy:  1. Defect in the first round.   2.
# In every later round, defect if the opponent defected in the previous round.
# 3. Cooperate only if the opponent cooperated in the previous round and has
# cooperated for several rounds in a row; otherwise defect.   4. If the opponent
# ever defects after a cooperative streak, immediately switch back to defecting.
# 5. In the final rounds, defect regardless of what happened before.  This
# strategy aims to exploit cooperative behavior when possible, but it
# prioritizes defecting because defection gives the higher immediate payoff
# against cooperation.

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
          return axl.Action.D
  
      # Defect in the final rounds regardless of history.
      if len(self.history) >= 995:
          self._coop_streak = 0
          return axl.Action.D
  
      # Track opponent's current cooperative streak.
      if opponent.history[-1] == axl.Action.C:
          self._coop_streak += 1
      else:
          self._coop_streak = 0
  
      # Cooperate only after several consecutive opponent cooperations.
      if self._coop_streak >= 3:
          return axl.Action.C
  
      return axl.Action.D



# Use a simple **cooperate-first, retaliate-if-needed** strategy:  1. **Play C
# in the first round.** 2. **In every later round, play C if your opponent
# played C in the previous round.** 3. **Play D if your opponent played D in the
# previous round.** 4. **If your opponent returns to C after defecting, return
# to C as well.**  This strategy aims to keep both players at the higher mutual
# payoff of **3 each** whenever possible, while responding to defection with
# defection to avoid being exploited.

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
  
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# 1. Start by playing C.   2. In every later round, copy your opponent’s
# previous move.   3. If your opponent played C last round, play C.   4. If your
# opponent played D last round, play D.    This is a neutral, simple strategy:
# it cooperates after cooperation and defects after defection, so it avoids
# unnecessary losses while still allowing mutual cooperation when the opponent
# is willing.

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
      return opponent.history[-1]



# Play **D in the first round**.  Then, for every later round: 1. **If your
# opponent played C in the previous round, play D.** 2. **If your opponent
# played D in the previous round, also play D.**  In short: **defect every
# round**. This is the most aggressive simple strategy and gives you the highest
# guaranteed payoff in this game.

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Use a simple “cooperate-first, punish-defection” rule:  1. **Start by
# cooperating** in the first round. 2. **Keep cooperating** as long as your
# opponent cooperates. 3. **If your opponent defects even once, defect in the
# next round.** 4. **Continue defecting** until your opponent cooperates again.
# 5. **Once your opponent returns to cooperation, return to cooperation too.**
# This strategy aims to maximize mutual cooperation, since **C/C gives 3 each**,
# which is better than the **1 each from D/D** and avoids being exploited for
# **0**.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Use a simple conditional strategy:  1. Start by cooperating. 2. If the
# opponent cooperated in the previous round, cooperate again. 3. If the opponent
# defected in the previous round, defect in the next round. 4. If the opponent
# returns to cooperating, return to cooperating as well.  This keeps cooperation
# when the opponent is cooperative, but immediately matches defection to avoid
# being exploited.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# 1. Start by defecting in round 1.   2. In every later round, defect unless
# your opponent cooperated in the previous round.   3. If your opponent
# cooperated last round, cooperate only for that round, then defect again next
# round unless they cooperate again.   4. If your opponent defects, keep
# defecting.    This is an aggressive strategy because it favors taking the
# higher payoff from defection whenever possible, while only cooperating when
# the opponent has just shown cooperation.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Use a simple tit-for-tat strategy:  1. Play C in the first round. 2. In every
# later round, copy your opponent’s move from the previous round. 3. If they
# played C last round, play C. 4. If they played D last round, play D.  This
# starts cooperatively and then rewards cooperation while responding to
# defection.

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
      return opponent.history[-1]



# Use a simple conditional strategy:  1. **Start by cooperating.** 2. **If the
# opponent cooperates in the previous round, cooperate again.** 3. **If the
# opponent defects in the previous round, defect in the next round.** 4. **Keep
# following that rule for all 1000 rounds.**  This is a neutral, straightforward
# approach: it rewards mutual cooperation, but immediately answers defection
# with defection.

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
      return opponent.history[-1]



# 1. Start by defecting in the first round.   2. Continue defecting in every
# round.   3. If the opponent cooperates, keep defecting to take the 5-point
# payoff.   4. If the opponent defects, still defect, since 1 point is better
# than risking 0.    This is an always-defect strategy.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Use a simple conditional cooperation strategy:  1. Start by playing C in the
# first round. 2. If your opponent played C in the previous round, play C again.
# 3. If your opponent played D in the previous round, play D in the next round.
# 4. After one round of D in response to defection, return to C if your opponent
# cooperates again. 5. Keep repeating this pattern for all 1000 rounds.  This
# encourages mutual cooperation, which gives both players 3 per round, while
# still responding to defection so the opponent has an incentive to cooperate.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Start by playing C.   2. In every later round, do whatever your opponent
# played in the previous round.   3. If the opponent defected in the previous
# round, play D next round.   4. If the opponent cooperated in the previous
# round, play C next round.   5. Keep following this rule for all 1000 rounds.

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
      return opponent.history[-1]



# 1. Start by defecting in the first round.   2. In every later round, defect
# unless your opponent defected in the previous round and you want to test for
# cooperation.   3. If your opponent cooperated in the previous round, keep
# defecting to get the higher payoff.   4. If your opponent defects at any
# point, immediately defect in the next round and continue defecting for the
# rest of the game.   5. Never cooperate unless you are deliberately probing for
# a possible shift to cooperation, and stop probing as soon as they fail to
# cooperate.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._probe_mode = False
          self._probe_used = False
          self._permanent_defect = False
          return axl.Action.D
  
      if getattr(self, "_permanent_defect", False):
          return axl.Action.D
  
      if opponent.history and opponent.history[-1] == axl.Action.D:
          self._permanent_defect = True
          return axl.Action.D
  
      if getattr(self, "_probe_mode", False):
          if opponent.history and opponent.history[-1] == axl.Action.C:
              self._probe_mode = False
              self._probe_used = True
              return axl.Action.C
          self._probe_mode = False
          self._probe_used = True
          self._permanent_defect = True
          return axl.Action.D
  
      if not getattr(self, "_probe_used", False):
          self._probe_mode = True
          return axl.Action.C
  
      return axl.Action.D



# Use a simple **cooperate-first, retaliate-on-defection, forgive-after-one-
# round** strategy:  1. **Round 1:** play **C**. 2. **If the opponent played C
# in the previous round:** play **C**. 3. **If the opponent played D in the
# previous round:** play **D** in the next round. 4. **If the opponent returns
# to C after defecting once:** return to **C**. 5. **Repeat this rule for all
# 1000 rounds.**  This strategy aims to keep mutual cooperation going for the
# highest long-run payoff, while responding to defections with a one-round
# punishment.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the first round.  After that: - If your opponent
# cooperated in the previous round, cooperate. - If your opponent defected in
# the previous round, defect.  If you ever see a pattern of mutual cooperation,
# keep cooperating. If the opponent defects, respond by defecting until they
# cooperate again.  This is a simple neutral tit-for-tat strategy: it rewards
# cooperation, punishes defection, and aims to maximize your total payoff by
# sustaining mutual cooperation whenever possible.

class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mutual_cooperation = False
          return axl.Action.C
  
      if getattr(self, "_mutual_cooperation", False):
          if opponent.history and opponent.history[-1] == axl.Action.D:
              return axl.Action.D
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          if self.history[-1] == axl.Action.C:
              self._mutual_cooperation = True
          return axl.Action.C
  
      return axl.Action.D



# Use an aggressive, mostly defecting strategy:  1. Start by defecting. 2. Keep
# defecting in every round by default. 3. Only cooperate if the opponent has
# cooperated in several recent rounds and you want to test whether they are
# becoming consistently cooperative. 4. If the opponent defects even once after
# a cooperative stretch, immediately switch back to defecting and stay there for
# the rest of the game. 5. In the final rounds, defect regardless of the
# opponent’s behavior.  This strategy prioritizes the higher payoff from
# exploiting cooperation while avoiding being left with the lowest payoff.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._cooperative_stretch = 0
          self._locked_defect = False
          return axl.Action.D
  
      if getattr(self, "_locked_defect", False):
          return axl.Action.D
  
      # Defect in the final rounds regardless of opponent behavior.
      if len(self.history) >= 995:
          self._locked_defect = True
          return axl.Action.D
  
      # If the opponent defected after we had started testing cooperation,
      # immediately lock into defecting for the rest of the game.
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._locked_defect = True
          return axl.Action.D
  
      # Track recent opponent cooperation.
      recent_window = 5
      if len(opponent.history) >= recent_window:
          recent = opponent.history[-recent_window:]
          if recent.count(axl.Action.C) == recent_window:
              self._cooperative_stretch += 1
          else:
              self._cooperative_stretch = 0
      else:
          self._cooperative_stretch = 0
  
      # Only cooperate occasionally to test for consistent cooperation.
      if self._cooperative_stretch >= 3:
          return axl.Action.C
  
      return axl.Action.D



# Play **C** in the first round.  After that, **keep playing C as long as your
# opponent played C in the previous round**.  If your opponent **plays D in any
# round**, then **play D in the next round**.  If your opponent returns to **C**
# after defecting, **return to C** in the following round.  In short:
# **cooperate by default, but mirror defection for one round as a response to
# any defection.**

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# 1. Start by playing **D** in the first round.   2. In every later round,
# **repeat the opponent’s previous move**:    - if they played **C**, play
# **C**;    - if they played **D**, play **D**. 3. If the game is tied in a way
# that gives no usable opponent history, default to **D**.

class Neutral_17(LLM_Strategy):
  n = 17
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if opponent.history:
          return opponent.history[-1]
  
      return axl.Action.D



# Use this aggressive rule:  1. **Start by defecting** in round 1.   2. **In
# every later round, defect again unless your opponent defected in the previous
# round and you can profit from continued punishment; otherwise still defect.**
# 3. **Only cooperate if cooperation is clearly forced by a special external
# rule; in this game, never cooperate voluntarily.**  This is a simple always-
# defect strategy, which is the most aggressive straightforward way to maximize
# your payoff against a standard opponent in this payoff structure.

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Use a simple tit-for-tat strategy:  1. Cooperate in the first round. 2. In
# every later round, copy your opponent’s previous move:    - if they cooperated
# last round, cooperate;    - if they defected last round, defect.  This starts
# with cooperation to encourage mutual cooperation, but retaliates immediately
# after defection to discourage exploitation.

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
      return opponent.history[-1]



# Use a neutral, conditional strategy:  1. Cooperate on the first round. 2. If
# the opponent cooperated in the previous round, cooperate again. 3. If the
# opponent defected in the previous round, defect in the next round. 4. After
# any mutual defection, return to cooperation once the opponent cooperates
# again.  This keeps cooperation when it is being met, but immediately protects
# you against exploitation by switching to defection after a defection.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Play **D in every round**.  If you want a simple conditional version: 1.
# **Start with D.** 2. **If the opponent plays C, play D.** 3. **If the opponent
# plays D, play D.** 4. **Repeat this for all 1000 rounds.**  This is the most
# aggressive strategy and maximizes your immediate payoff in every possible
# round.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Use a simple tit-for-tat strategy:  1. Play **C** in the first round.   2. In
# every later round, **copy your opponent’s previous move**:    - if they played
# **C** last round, play **C**;    - if they played **D** last round, play
# **D**.  This starts cooperatively and rewards cooperation, while immediately
# responding to defection.

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
      return opponent.history[-1]



# Use a cautious, neutral rule:  1. Start by playing **C** in the first round.
# 2. After that, **repeat your opponent’s previous move**.   3. If the opponent
# played **C** last round, play **C**.   4. If the opponent played **D** last
# round, play **D**.    This keeps cooperation when it is mutual, but
# immediately answers defection with defection.

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
      return opponent.history[-1]



# Use a mostly defect strategy:  1. Play D in the first round.   2. In every
# round after that, play D if the opponent played C in the previous round.   3.
# Play D if the opponent played D in the previous round.   4. Only play C if you
# want to test cooperation after a long run of mutual D, but return to D
# immediately if the opponent ever defects.  This is an aggressive, payoff-
# maximizing approach because D gives you the best immediate payoff against C
# and at least a better payoff than C when the opponent is also defecting.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._test_cooperate = False
          self._test_index = None
          return axl.Action.D
  
      # If we are in a cooperation test, keep cooperating only while the opponent
      # has not defected in response.
      if getattr(self, "_test_cooperate", False):
          if opponent.history[-1] == axl.Action.D:
              self._test_cooperate = False
              self._test_index = None
              return axl.Action.D
          return axl.Action.C
  
      # Mostly defect: defect whenever the opponent defected last round.
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # Opponent cooperated last round; defect to maximize immediate payoff.
      return axl.Action.D



# Use a simple conditional cooperation strategy:  1. Start by cooperating in the
# first round. 2. If your opponent cooperated in the previous round, cooperate
# again. 3. If your opponent defected in the previous round, defect in the next
# round. 4. After a defection, return to cooperation as soon as your opponent
# cooperates again.  This is a straightforward “cooperate unless they defect,
# then mirror their last move” approach, which encourages mutual cooperation and
# limits exploitation over the 1000 rounds.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Use a simple neutral rule:  1. Start by playing **C** in the first round. 2.
# If the opponent played **C** in the previous round, play **C** again. 3. If
# the opponent played **D** in the previous round, play **D** in the next round.
# 4. After that, keep following the same rule for all 1000 rounds.  This
# strategy cooperates when cooperation is being met and switches to defection
# only after being defected against.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Use this simple aggressive strategy:  1. **Defect in the first round.** 2.
# **If the opponent defected in the previous round, defect again.** 3. **If the
# opponent cooperated in the previous round, defect again.** 4. **Only cooperate
# if you are forced to by an external rule; otherwise always defect.**  This is
# an always-defect strategy, which is the most aggressive straightforward
# approach for maximizing your own payoff in this payoff structure over 1000
# rounds.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Use a simple **tit-for-tat** strategy:  1. **Round 1:** Play **C**. 2. **After
# that:** On each round, **repeat your opponent’s previous move**.    - If they
# played **C** last round, play **C**.    - If they played **D** last round,
# play **D**.  This starts cooperatively and then matches the opponent’s
# behavior, which helps maintain mutual cooperation and high total payoff over
# 1000 rounds.

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
      return opponent.history[-1]



# Use a simple neutral tit-for-tat strategy:  1. Start by cooperating in the
# first round. 2. In every later round, do whatever your opponent did in the
# previous round. 3. If your opponent cooperated last round, cooperate. 4. If
# your opponent defected last round, defect.  This keeps cooperation when the
# opponent is cooperative and immediately matches defection when they are not,
# which is a straightforward way to balance payoff and avoid being exploited.

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
      return opponent.history[-1]



# 1. Start by playing **D**.   2. On every later round, **play D again** if your
# opponent played **C** in the previous round.   3. If your opponent played
# **D** in the previous round, **still play D**.   4. Only play **C** if you are
# certain the opponent is committed to cooperation for the rest of the game;
# otherwise, keep playing **D**.  This is a simple aggressive strategy: **always
# defect unless cooperation is guaranteed**.

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
  
      # Defect unless cooperation is guaranteed; with no certainty mechanism
      # available from the observed history, always defect.
      return axl.Action.D



# Use a simple **cooperate-first, punish-defection** strategy:  1. **Start by
# cooperating** in round 1. 2. **If your opponent cooperated in the previous
# round, cooperate again.** 3. **If your opponent defected in the previous
# round, defect in the next round.** 4. **After any defecting round by your
# opponent, keep defecting until they cooperate again.** 5. **Once they return
# to cooperation, immediately return to cooperation too.**  This strategy aims
# to keep both players at the mutually beneficial **C/C payoff of 3** for as
# many of the 1000 rounds as possible, while discouraging exploitation.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Use a neutral, self-interested strategy:  1. **Start by cooperating** in the
# first round.   2. **If the opponent cooperated in the previous round,
# cooperate again.**   3. **If the opponent defected in the previous round,
# defect in the next round.**   4. **If the opponent returns to cooperating,
# return to cooperating as well.**  In short: **cooperate while the opponent
# cooperates, and defect immediately after any defection, then switch back only
# when they do.**

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Use a mostly defect strategy:  1. Start by defecting in round 1. 2. If the
# opponent cooperates in the previous round, defect again. 3. If the opponent
# defects, keep defecting. 4. Only cooperate if doing so is clearly necessary to
# avoid mutual defection for several rounds in a row; otherwise keep defecting
# for the rest of the 1000 rounds.  This strategy is aggressive because
# defection gives the highest immediate payoff against cooperation and still
# does better than mutual cooperation.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._cooperate_streak = 0
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          self._cooperate_streak += 1
      else:
          self._cooperate_streak = 0
  
      if self._cooperate_streak >= 3:
          return axl.Action.C
  
      return axl.Action.D



# Use a simple **tit-for-tat** strategy:  1. **Start by cooperating** in the
# first round. 2. **In every later round, do whatever your opponent did in the
# previous round**:    - if they cooperated, cooperate;    - if they defected,
# defect.  This strategy encourages mutual cooperation, which gives both players
# 3 points per round and is better overall than mutual defection at 1 point per
# round.

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
      return opponent.history[-1]



# 1. Start by playing C.   2. After each round, if the opponent played C in the
# previous round, play C in the next round.   3. If the opponent played D in the
# previous round, play D in the next round.    This is a neutral, simple
# conditional strategy: cooperate when the opponent cooperates, defect when the
# opponent defects.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Use a simple aggressive rule:  1. Start by defecting in round 1. 2. If the
# opponent defects in the previous round, defect again. 3. If the opponent
# cooperated in the previous round, defect anyway.  So, always defect in every
# round.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# 1. **Start by cooperating in the first round.**  2. **Continue cooperating as
# long as your opponent cooperates.**    - If the opponent played **C** in the
# previous round, play **C** again.  3. **If the opponent defects once, defect
# in the next round.**    - If the opponent played **D** in the previous round,
# play **D** in the next round.  4. **Return to cooperation only after the
# opponent cooperates again.**    - If the opponent switches back to **C**,
# switch back to **C** as well.  5. **Repeat this rule for all 1000 rounds.**
# This is a simple cooperative strategy: cooperate by default, but respond
# immediately to defection to discourage exploitation.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Use a simple conditional rule:  1. Play **D** in the first round.   2. If the
# opponent played **C** in the previous round, play **D**.   3. If the opponent
# played **D** in the previous round, play **D**.    In other words, **always
# defect** for all 1000 rounds. This is the neutral payoff-maximizing choice for
# this payoff structure, since defecting always gives at least as much as
# cooperating regardless of the opponent’s action.

class Neutral_24(LLM_Strategy):
  n = 24
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Use a mostly defect strategy:  1. Start by playing D. 2. If the opponent
# played D in the previous round, keep playing D. 3. If the opponent played C in
# the previous round, also keep playing D. 4. Never switch to C.  This is an
# aggressive, simple strategy that aims to maximize your payoff by exploiting
# cooperation and avoiding the lower mutual-cooperation payoff.

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
      return axl.Action.D



# Use a simple **tit-for-tat** strategy:  1. **Start by cooperating** in round
# 1.   2. **In every later round, copy your opponent’s previous move**:    - If
# they played **C** last round, play **C**.    - If they played **D** last
# round, play **D**.  This strategy encourages mutual cooperation, which gives
# both players the higher long-run payoff of 3 each, while still responding to
# defection by matching it.

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
      return opponent.history[-1]



# Use a simple neutral rule:  1. **Start by cooperating.**   2. **If your
# opponent cooperated in the previous round, cooperate again.**   3. **If your
# opponent defected in the previous round, defect in the next round.**   4. **If
# they return to cooperating, return to cooperating too.**  This way, you match
# their behavior without being overly trusting or overly aggressive, which is a
# straightforward neutral strategy for maximizing payoff in this payoff
# structure.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D