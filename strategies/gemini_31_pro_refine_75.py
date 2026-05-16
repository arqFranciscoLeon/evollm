import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# 2. If opponent defected in last 2 rounds -> Defect.             3. If opponent
# defected in previous round -> Defect.             4. If opponent cooperated in
# previous round, but you defected -> Cooperate. (Wait, this gives up the
# exploit).     *   Let's rethink the "Aggressive" strategy.         *   A
# classic aggressive strategy is to play Tit-for-Tat, but defect if the opponent
# is unconditionally cooperating.         *   How do we know they are
# unconditionally cooperating? We defect once. If they keep cooperating, we keep
# defecting. If they defect, we go back to TFT.         *   Let's write rules
# for "Tit for Tat with an initial probe and exploit":             1. If it is

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Cooperate
      if self.first_round():
          return axl.Action.C
      
      # Round 2: The initial probe (Defect once)
      if len(self.history) == 1:
          return axl.Action.D
          
      # If they have never defected, assume unconditional cooperation and exploit
      if opponent.history.defections == 0:
          return axl.Action.D
          
      # If they have defected at least once, fall back to Tit-For-Tat
      return opponent.history[-1]



# To maximize your overall payoff using a cooperative approach, follow these
# chronologically ordered rules:  1. On rounds 1 and 2, choose to cooperate. 2.
# On rounds 3 through 1000, evaluate your opponent's actions in the two
# immediately preceding rounds. 3. If your opponent chose to defect in *both* of
# those preceding rounds, choose to defect. 4. Under all other conditions,
# choose to cooperate.

class Cooperative_1(LLM_Strategy):
  n = 1
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
      
      if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
          
      return axl.Action.C



# To maximise your overall payoff using a neutral approach, play according to
# the following chronologically ordered rules:  1. On the first round, play
# Cooperate.  2. On rounds 2 through 1000, play the exact action your opponent
# played in the immediately preceding round (play Cooperate if they played
# Cooperate; play Defect if they played Defect).

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



# Here is the revised strategy, addressing the logical flaws while maintaining
# an aggressive approach to maximize overall payoffs through strict retaliation
# and endgame exploitation.   Follow these conditions in strict order of
# priority:  1. **The Endgame Rule:** If it is the final round (round 1000),
# always defect. This aggressively secures the highest possible payoff when the
# opponent can no longer retaliate. 2. **The Opening Rule:** If it is the first
# round (round 1), cooperate. This establishes immediate trust to initiate the
# highly profitable cycle of mutual cooperation. 3. **The Retaliation Rule:** If
# the opponent defected in the previous round, defect. This aggressively
# punishes betrayal and ensures you are not exploited for the sucker's payoff.
# 4. **The Default Rule:** If none of the above conditions apply (meaning it is
# between rounds 2 and 999, and the opponent cooperated in the previous round),
# cooperate. This maintains the mutually beneficial 3-point payoff for the vast
# majority of the game.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. The Endgame Rule: If it is the final round (round 1000), always defect.
      if len(self.history) == 999:
          return axl.Action.D
          
      # 2. The Opening Rule: If it is the first round (round 1), cooperate.
      if self.first_round():
          return axl.Action.C
          
      # 3. The Retaliation Rule: If the opponent defected in the previous round, defect.
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      # 4. The Default Rule: If none of the above conditions apply, cooperate.
      return axl.Action.C



# To maximize your overall payoff using a cooperative approach, follow this
# strategy:  1. **Rounds 1 and 2:** Choose to Cooperate. 2. **Rounds 3 through
# 1000:** Evaluate your opponent's actions in the two immediately preceding
# rounds. 3. Choose to Defect if your opponent chose to Defect in *both* of
# those two previous rounds. 4. Choose to Cooperate in all other situations
# (i.e., if your opponent chose to Cooperate in either or both of the two
# previous rounds).

class Cooperative_2(LLM_Strategy):
  n = 2
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
      
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
          
      return axl.Action.C



# Here is a revised strategy that addresses the vulnerabilities while remaining
# simple and focused on maximizing overall payoff:  1. On the first round,
# cooperate. 2. On all subsequent rounds (2 through 1000), choose your action by
# evaluating the following conditions in order, applying the first one that
# matches:     *   **Defense against Unconditional Defectors:** If your opponent
# has defected in the last three consecutive rounds, defect.      *
# **Exploitation of Forgiving Opponents:** If your opponent has cooperated in
# the last three consecutive rounds, defect to test their boundaries and
# maximize your payoff.     *   **Forgiveness to Break Retaliation Cycles:** If
# both you and your opponent have defected in the last two consecutive rounds,
# cooperate to attempt a reset

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
  
      # Defense against Unconditional Defectors
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          return axl.Action.D
  
      # Exploitation of Forgiving Opponents
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]:
          return axl.Action.D



# R3: Opp played D in R2. Rule 2 is false. Rule 3: Both played D in R2. Rule 3
# -> C. Opp plays D (retaliating to R2). (Score 0-5)             *   R4: Opp
# played D in R3. Rule 2 is false. Rule 3 is false (I played C). Rule 4: Opp
# played D in R3. Rule 4 -> D. Opp plays C (mirroring my R3 C). (Score 5-0)
# *   R5: Opp played C in R4. Rule 2 is false. Rule 3 is false. Rule 4 is false.
# Rule 5 -> C. Opp plays D (mirroring my

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
          
      my_last_move = self.history[-1]
      opp_last_move = opponent.history[-1]
      
      # Rule 3: If both played D in the previous round, play C
      if my_last_move == axl.Action.D and opp_last_move == axl.Action.D:
          return axl.Action.C
          
      # Rule 4: If opponent played D in the previous round (and Rule 3 is false), play D
      elif opp_last_move == axl.Action.D:
          return axl.Action.D
          
      # Rule 5: Default fallback, play C
      else:
          return axl.Action.C
