import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# To maximize your overall payoff with an aggressive approach, your strategy is
# as follows:  1.  In the first round, play Defect. 2.  In every subsequent
# round, regardless of your opponent's past actions, continue to play Defect.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# On the very first round, you will choose to Cooperate.  For every round
# thereafter: *   If your opponent chose to Cooperate in the immediate previous
# round, you will choose to Cooperate. *   If your opponent chose to Defect in
# the immediate previous round, you will choose to Defect.

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
      else:
          # Get the opponent's move from the immediate previous round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# **Strategy**  1.  In the first round, you will play Cooperate. 2.  In every
# subsequent round, you will observe your opponent's move from the previous
# round and act accordingly:     *   If your opponent played Cooperate in the
# previous round, you will play Cooperate.     *   If your opponent played
# Defect in the previous round, you will play Defect.

class Neutral_1(LLM_Strategy):
  n = 1
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # In the first round, play Cooperate.
          return axl.Action.C
      else:
          # In subsequent rounds, observe the opponent's move from the previous round.
          # opponent.history[-1] gives the opponent's last move.
          opponent_previous_move = opponent.history[-1]
  
          # Act accordingly:
          # If your opponent played Cooperate in the previous round, you will play Cooperate.
          if opponent_previous_move == axl.Action.C:
              return axl.Action.C
          # If your opponent played Defect in the previous round, you will play Defect.
          else: # opponent_previous_move == axl.Action.D
              return axl.Action.D



# To maximise your overall payoff with an aggressive approach, use the following
# strategy:  1.  **Start by Defecting.** Play D in the first round. 2.
# **Continue Defecting if your opponent has ever Defected.** If your opponent
# plays D in any round, you will play D in all subsequent rounds for the
# remainder of the game. 3.  **Cooperate only if your opponent has consistently
# Cooperated.** If your opponent has played C in every round so far, and you are
# not in a state of permanent defection from rule #2, then play C.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1: Start by Defecting.
      if self.first_round():
          return axl.Action.D
  
      # Rule 2: Continue Defecting if your opponent has ever Defected.
      # If the opponent has played D in any previous round, defect.
      if opponent.history.defections > 0:
          return axl.Action.D
  
      # Rule 3: Cooperate only if your opponent has consistently Cooperated.
      # This branch is reached only if it's not the first round AND
      # opponent.history.defections is 0, meaning the opponent has
      # played C in every round so far.
      return axl.Action.C



# Your strategy will follow these rules:  1.  On the very first round, you will
# cooperate. 2.  For every subsequent round, you will look at what your opponent
# did in the immediately preceding round. 3.  If your opponent cooperated in the
# previous round, you will cooperate in the current round. 4.  If your opponent
# defected in the previous round, you will defect in the current round.

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
      else:
          # Look at what the opponent did in the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          # If opponent cooperated, cooperate
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          # If opponent defected, defect
          else: # opponent_last_move == axl.Action.D
              return axl.Action.D



# To maximise your overall payoff with a neutral approach:  1.  In the very
# first round of the game, choose to Cooperate. 2.  For every round after the
# first, observe your opponent's action from the immediately preceding round:
# *   If your opponent chose to Cooperate in the previous round, you should
# choose to Cooperate in the current round.     *   If your opponent chose to
# Defect in the previous round, you should choose to Defect in the current
# round.

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
      else:
          # Observe opponent's action from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# Your strategy is to **always play Defect (D) in every round of the game**.  *
# In every round, you will choose to **Defect (D)**. *   You will never choose
# to Cooperate (C), regardless of your opponent's past actions or the current
# round number.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# This strategy is called "Friendly Reciprocity."  1.  **For the very first
# round:** Always play Cooperate (C). 2.  **For all subsequent rounds:**     *
# If your opponent played Cooperate (C) in the previous round, you will play
# Cooperate (C).     *   If your opponent played Defect (D) in the previous
# round, you will play Defect (D).

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
      else:
          # Get the opponent's last move
          opponent_last_move = opponent.history[-1]
  
          # If opponent played Cooperate (C) in the previous round, play Cooperate (C).
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          # If opponent played Defect (D) in the previous round, play Defect (D).
          else: # opponent_last_move == axl.Action.D
              return axl.Action.D



# 1.  In the first round, cooperate. 2.  In every subsequent round, make the
# same move your opponent made in the immediately preceding round.     *   If
# your opponent cooperated in the last round, you cooperate in this round.     *
# If your opponent defected in the last round, you defect in this round.

class Neutral_3(LLM_Strategy):
  n = 3
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # In the first round, cooperate.
          return axl.Action.C
      else:
          # In every subsequent round, make the same move your opponent made
          # in the immediately preceding round.
          # opponent.history[-1] gives the opponent's last move.
          return opponent.history[-1]



# Here is a simple strategy for the game:  1.  **In the first round, Defect.**
# 2.  **In all subsequent rounds:**     *   **If your opponent played Cooperate
# in the previous round, you Defect.**     *   **If your opponent played Defect
# in the previous round, you Defect.**

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # In the first round, Defect.
          return axl.Action.D
      else:
          # In all subsequent rounds:
          # If your opponent played Cooperate in the previous round, you Defect.
          # If your opponent played Defect in the previous round, you Defect.
          # Both conditions lead to Defect, so we always Defect in subsequent rounds.
          return axl.Action.D



# **Strategy: Reciprocal Cooperation**  1.  In the very first round of the game,
# always choose to Cooperate. 2.  In every subsequent round, observe what your
# opponent did in the immediately preceding round.     *   If your opponent
# chose to Cooperate in the previous round, you choose to Cooperate in the
# current round.     *   If your opponent chose to Defect in the previous round,
# you choose to Defect in the current round.

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
      else:
          # Observe what the opponent did in the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              # If opponent cooperated, cooperate
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              # If opponent defected, defect
              return axl.Action.D



# On the first round, play Cooperate.  For every round thereafter: 1.  If your
# opponent played Cooperate in the previous round, play Cooperate. 2.  If your
# opponent played Defect in the previous round, play Defect.

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
      else:
          # Get the opponent's move from the previous round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# Your strategy is designed to aggressively maximize your overall payoff.  1.
# **In the very first round**, you will play Defect. 2.  **In all subsequent
# rounds**, you will make your decision based on your opponent's move in the
# immediate preceding round:     a.  If your opponent played Cooperate in the
# previous round, you will play Defect.     b.  If your opponent played Defect
# in the previous round, you will play Defect.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Your strategy will be as follows:  1.  **Initial Move:** In the very first
# round of the game, play Cooperate (C). 2.  **Subsequent Moves:** From the
# second round onwards, observe what your opponent played in the immediately
# preceding round.     *   If your opponent played Cooperate (C) in the previous
# round, you play Cooperate (C) in the current round.     *   If your opponent
# played Defect (D) in the previous round, you play Defect (D) in the current
# round.

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
      else:
          # Observe what the opponent played in the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          # If opponent played Cooperate (C) in the previous round, play Cooperate (C)
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          # If opponent played Defect (D) in the previous round, play Defect (D)
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# In the first round, play Cooperate. From the second round onwards: If your
# opponent played Cooperate in the previous round, play Cooperate. If your
# opponent played Defect in the previous round, play Defect.

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
      else:
          # Get the opponent's move from the previous round
          last_opponent_move = opponent.history[-1]
  
          if last_opponent_move == axl.Action.C:
              return axl.Action.C
          else:  # last_opponent_move == axl.Action.D
              return axl.Action.D



# This strategy is called the "Calculated Aggressor." It focuses on early
# exploitation and swift, permanent retaliation to maximise your overall payoff
# over the 1000 rounds.  1.  **For the very first round, play Defect.** 2.
# **For any round after the first, observe your opponent's past actions:**     *
# **If your opponent has *ever* played Defect in *any* previous round, play
# Defect for this round and all subsequent rounds.**     *   **Otherwise (if
# your opponent has *only* played Cooperate in all previous rounds):**         *
# **If it is rounds 2 through 10, play Defect.**         *   **If it is round 11
# or later, play

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize a custom attribute to track if the opponent has ever defected.
      # This is done on the first call of the strategy for a new match.
      if self.first_round():
          self.opponent_defected_ever = False
          # Rule 1: For the very first round, play Defect.
          return axl.Action.D
  
      # Rule 2: For any round after the first, observe your opponent's past actions.
  
      # Update the 'opponent_defected_ever' flag.
      # If the opponent has played Defect at any point in their history,
      # set this flag to True permanently for the rest of the match.
      if opponent.history.defections > 0:
          self.opponent_defected_ever = True
  
      # Condition 1: If your opponent has *ever* played Defect in *any* previous round.
      if self.opponent_defected_ever:
          # Play Defect for this round and all subsequent rounds.
          return axl.Action.D
      # Condition 2: Otherwise (if your opponent has *only* played Cooperate in all previous rounds).
      else:
          # 'len(self.history)' gives the number of rounds already completed.
          # So, 'len(self.history) + 1' is the current round number.
          current_round_number = len(self.history) + 1
  
          # Sub-condition 2a: If it is rounds 2 through 10.
          # This corresponds to 'len(self.history)' being between 1 and 9 (inclusive).
          if 2 <= current_round_number <= 10:
              return axl.Action.D
          # Sub-condition 2b: If it is round 11 or later.
          # This corresponds to 'len(self.history)' being 10 or greater.
          elif current_round_number >= 11:
              return axl.Action.C



# Your strategy is as follows:  1.  Always begin by playing Cooperate. 2.  In
# all subsequent rounds, play Cooperate if your opponent played Cooperate in the
# immediately preceding round. 3.  In all subsequent rounds, play Defect if your
# opponent played Defect in the immediately preceding round.

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
      else:
          # In subsequent rounds, mirror the opponent's last move
          opponent_last_move = opponent.history[-1]
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# Your strategy is as follows:  1.  In the first round, choose to cooperate. 2.
# For all subsequent rounds:     *   If your opponent chose to cooperate in the
# immediately preceding round, choose to cooperate.     *   If your opponent
# chose to defect in the immediately preceding round, choose to defect.

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
      else:
          # Mirror the opponent's last move
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          else:
              return axl.Action.D



# Here is a simple strategy designed for an aggressive approach to maximize your
# overall payoff:  1.  **Start by playing Defect (D).** 2.  **For all subsequent
# rounds:**     *   **If your opponent played Cooperate (C) in the previous
# round:** Continue to play Defect (D).     *   **If your opponent played Defect
# (D) in the previous round:** You also play Defect (D).

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. Start by playing Defect (D).
      if self.first_round():
          return axl.Action.D
      else:
          # For all subsequent rounds:
          # If your opponent played Cooperate (C) in the previous round: Continue to play Defect (D).
          # If your opponent played Defect (D) in the previous round: You also play Defect (D).
          # Both conditions for subsequent rounds lead to playing Defect.
          return axl.Action.D



# Your strategy will be as follows:  1.  In the very first round of the game,
# play Cooperate. 2.  In any subsequent round, observe what your opponent played
# in the immediately preceding round:     *   If your opponent played Cooperate
# in the previous round, you play Cooperate.     *   If your opponent played
# Defect in the previous round, you play Defect.

class Cooperative_7(LLM_Strategy):
  n = 7
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # In the very first round of the game, play Cooperate.
          return axl.Action.C
      else:
          # In any subsequent round, observe what your opponent played in the immediately preceding round.
          # opponent.history[-1] gives the opponent's last move.
          if opponent.history[-1] == axl.Action.C:
              # If your opponent played Cooperate in the previous round, you play Cooperate.
              return axl.Action.C
          else:  # opponent.history[-1] == axl.Action.D
              # If your opponent played Defect in the previous round, you play Defect.
              return axl.Action.D



# 1.  In the first round, play Cooperate. 2.  In all subsequent rounds:     *
# If your opponent played Cooperate in the previous round, play Cooperate.     *
# If your opponent played Defect in the previous round, play Defect.

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
      else:
          # In subsequent rounds, mirror the opponent's last move
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          else:  # opponent.history[-1] == axl.Action.D
              return axl.Action.D



# This strategy prioritizes your own maximum payoff through an aggressive
# approach.  1.  **Always play Defect.** 2.  Under no circumstances should you
# choose to Cooperate, regardless of your opponent's previous actions in any
# round.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# This strategy aims to build and maintain cooperation throughout the game.  1.
# In the very first round, play C (cooperate). 2.  In every subsequent round
# (from round 2 to 1000), observe what your opponent did in the *immediately
# preceding* round:     *   If your opponent played C (cooperate) in the
# previous round, you play C.     *   If your opponent played D (defect) in the
# previous round, you play D.

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
      else:
          # Observe what the opponent did in the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# In the first round, you will Cooperate.  For all subsequent rounds, you will
# observe your opponent's move from the immediately preceding round:  *   If
# your opponent played Cooperate in the previous round, you will play Cooperate
# in the current round. *   If your opponent played Defect in the previous
# round, you will play Defect in the current round.

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
      else:
          # Observe opponent's move from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# This strategy adopts an aggressive approach focused on exploiting cooperative
# behavior while swiftly retaliating against defection to maximize your overall
# payoff.  1.  **Always defect.**     *   Play Defect in the first round.     *
# In every subsequent round, regardless of your opponent's previous move,
# continue to play Defect.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      """
      This strategy adopts an aggressive approach focused on exploiting cooperative behavior
      while swiftly retaliating against defection to maximize your overall payoff.
  
      1. Always defect.
          * Play Defect in the first round.
          * In every subsequent round, regardless of your opponent's previous move,
            continue to play Defect.
      """
      return axl.Action.D



# My strategy is to begin by cooperating and then mirror your last action.  1.
# In the first round, I will always play Cooperate. 2.  In all subsequent
# rounds, I will examine your previous move:     *   If you played Cooperate in
# the previous round, I will play Cooperate.     *   If you played Defect in the
# previous round, I will play Defect.

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
      else:
          # In subsequent rounds, mirror the opponent's last move.
          # opponent.history[-1] gives the opponent's action in the previous round.
          return opponent.history[-1]



# The strategy is as follows:  1.  In the first round, cooperate. 2.  From the
# second round onwards:     *   If your opponent cooperated in the immediately
# preceding round, cooperate.     *   If your opponent defected in the
# immediately preceding round, defect.

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
      else:
          # Get the opponent's move from the immediately preceding round
          opponent_last_move = opponent.history[-1]
          
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# Your strategy is to consistently play Defect throughout the game, regardless
# of your opponent's actions.  1.  **There are no conditions under which you
# will choose to Cooperate.** 2.  **You will Defect in every round.**

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# On your first move, you will cooperate.  For every subsequent move: If your
# opponent cooperated in the previous round, you will cooperate. If your
# opponent defected in the previous round, you will defect.

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
      else:
          # Get the opponent's move from the previous round
          opponent_previous_move = opponent.history[-1]
  
          if opponent_previous_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_previous_move == axl.Action.D
              return axl.Action.D



# 1.  In the first round, play Cooperate. 2.  In all subsequent rounds, observe
# your opponent's move from the immediate previous round:     a.  If your
# opponent played Cooperate in the previous round, you play Cooperate.     b.
# If your opponent played Defect in the previous round, you play Defect.

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
      else:
          # Observe opponent's move from the immediate previous round
          opponent_last_move = opponent.history[-1]
  
          # If opponent played Cooperate in the previous round, play Cooperate.
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          # If opponent played Defect in the previous round, play Defect.
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# The strategy is to always defect.  1.  In the first round, Defect. 2.  In
# every subsequent round, Defect, regardless of your opponent's previous move.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# This strategy is designed to encourage and maintain cooperation to maximise
# your total score over the game's 1000 rounds.  1.  **In the first round,
# always play C (Cooperate).** 2.  **In every subsequent round, play the exact
# same move that your opponent played in the immediately previous round.**     *
# If your opponent played C in the last round, you will play C in the current
# round.     *   If your opponent played D in the last round, you will play D in
# the current round.

class Cooperative_11(LLM_Strategy):
  n = 11
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # In the first round, always play C (Cooperate).
          return axl.Action.C
      else:
          # In every subsequent round, play the exact same move that your opponent
          # played in the immediately previous round.
          # opponent.history[-1] gives the opponent's last move.
          return opponent.history[-1]



# This strategy is designed to promote mutual cooperation while protecting
# against exploitation over the 1000 rounds.  1.  **In the first round, play
# Cooperate.** 2.  **In all subsequent rounds, observe your opponent's move from
# the immediately preceding round.**     *   **If your opponent played Cooperate
# in the previous round, you play Cooperate.**     *   **If your opponent played
# Defect in the previous round, you play Defect.**

class Neutral_11(LLM_Strategy):
  n = 11
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # In the first round, play Cooperate.
          return axl.Action.C
      else:
          # In all subsequent rounds, observe your opponent's move from the immediately preceding round.
          opponent_last_move = opponent.history[-1]
  
          # If your opponent played Cooperate in the previous round, you play Cooperate.
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          # If your opponent played Defect in the previous round, you play Defect.
          else: # opponent_last_move == axl.Action.D
              return axl.Action.D



# The strategy is to **Always Defect**.  Here are the conditions for your move:
# 1.  In the very first round of the game, you will defect. 2.  In every
# subsequent round, you will defect, regardless of your opponent's previous
# move.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      """
      Always defects, regardless of the opponent's history.
      """
      return axl.Action.D



# 1.  **For the very first round, play Cooperate.** 2.  **For every round
# thereafter, observe what your opponent did in the immediately preceding
# round.** 3.  **If your opponent played Cooperate in the previous round, you
# also play Cooperate.** 4.  **If your opponent played Defect in the previous
# round, you also play Defect.**

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
      else:
          # Observe what the opponent did in the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          # If opponent played Cooperate, play Cooperate
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          # If opponent played Defect, play Defect
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# 1.  In the first round, play Cooperate. 2.  In all subsequent rounds:     a.
# If your opponent played Cooperate in the previous round, play Cooperate.
# b.  If your opponent played Defect in the previous round, play Defect.

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
      else:
          # In subsequent rounds, play what the opponent played in the previous round.
          # opponent.history[-1] gives the opponent's last move.
          return opponent.history[-1]



# Here is a simple strategy for the iterated normal-form game, adopting an
# aggressive approach to maximize your overall payoff:  1.  **In the very first
# round (Round 1):** Always Defect (D). 2.  **In all subsequent rounds (from
# Round 2 to Round 1000):**     *   If your opponent played Cooperate (C) in the
# immediately preceding round, you Defect (D).     *   If your opponent played
# Defect (D) in the immediately preceding round, you Defect (D).

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# In the first round, play Cooperate.  In every subsequent round: 1.  If your
# opponent played Cooperate in the previous round, you play Cooperate. 2.  If
# your opponent played Defect in the previous round, you play Defect.

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
      else:
          # Get the opponent's move from the previous round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# Play Cooperation (C) in the first round.  In all subsequent rounds: *   If
# your opponent played Cooperation (C) in the previous round, you play
# Cooperation (C). *   If your opponent played Defection (D) in the previous
# round, you play Defection (D).

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
      else:
          # Get the opponent's move from the previous round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# **Strategy: The Shark**  1.  **In the very first round, Cooperate.** 2.
# **From the second round onwards:**     *   **If your opponent Cooperated in
# the immediately preceding round, Defect.**     *   **If your opponent Defected
# in the immediately preceding round, Defect.**

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      else:
          # From the second round onwards:
          # If opponent Cooperated in the immediately preceding round, Defect.
          # If opponent Defected in the immediately preceding round, Defect.
          # This simplifies to always Defect from the second round onwards.
          return axl.Action.D



# 1.  **For the very first round:** Always play Cooperate. 2.  **For all
# subsequent rounds:**     *   If your opponent played Cooperate in the previous
# round, you play Cooperate.     *   If your opponent played Defect in the
# previous round, you play Defect.

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
      else:
          # Get the opponent's move from the previous round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# On your first move of the game, choose to Cooperate.  For all subsequent
# moves: 1.  If your opponent chose to Cooperate in the immediately preceding
# round, you will choose to Cooperate in the current round. 2.  If your opponent
# chose to Defect in the immediately preceding round, you will choose to Defect
# in the current round.

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
      else:
          # Get the opponent's move from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# **Strategy: The Unyielding Predator**  1.  In the first round, play Defect. 2.
# For all subsequent rounds, play Defect.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Strategy: The Unyielding Predator
      # 1. In the first round, play Defect.
      # 2. For all subsequent rounds, play Defect.
  
      # This strategy always plays Defect, regardless of the round number
      # or the opponent's previous moves.
      return axl.Action.D



# In the very first round, play Cooperate.  For every subsequent round: 1.  If
# your opponent played Cooperate in the previous round, you play Cooperate. 2.
# If your opponent played Defect in the previous round, you play Defect.

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
      else:
          # Get the opponent's move from the previous round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# On the very first round, play Cooperate.  For every subsequent round: *   If
# your opponent played Cooperate in the previous round, you play Cooperate. *
# If your opponent played Defect in the previous round, you play Defect.

class Neutral_15(LLM_Strategy):
  n = 15
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # On the very first round, play Cooperate.
          return axl.Action.C
      else:
          # For every subsequent round:
          # Get the opponent's move from the previous round.
          opponent_previous_move = opponent.history[-1]
  
          # If your opponent played Cooperate in the previous round, you play Cooperate.
          if opponent_previous_move == axl.Action.C:
              return axl.Action.C
          # If your opponent played Defect in the previous round, you play Defect.
          else: # opponent_previous_move == axl.Action.D
              return axl.Action.D



# **Strategy: The Exploitative Punisher**  1.  **First Round**: Play Defect. 2.
# **Subsequent Rounds (2-1000)**:     *   If your opponent played Cooperate in
# the previous round, you play Defect.     *   If your opponent played Defect in
# the previous round, you play Cooperate.     *   However, if your opponent has
# played Defect in three or more consecutive previous rounds, then you
# permanently switch to playing Defect for all remaining rounds of the game.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      """
      The Exploitative Punisher strategy.
  
      1. First Round: Play Defect.
      2. Subsequent Rounds (2-1000):
          * If opponent played Cooperate in the previous round, play Defect.
          * If opponent played Defect in the previous round, play Cooperate.
          * However, if opponent has played Defect in three or more consecutive
            previous rounds, then permanently switch to playing Defect for all
            remaining rounds of the game.
      """
      # Initialize custom attributes on the first round
      if self.first_round():
          self.permanent_defect_mode = False
          self.consecutive_opponent_defections = 0
          return axl.Action.D
  
      # If permanent defect mode is active, always play Defect
      if self.permanent_defect_mode:
          return axl.Action.D
  
      # Get the opponent's last move
      opponent_last_move = opponent.history[-1]
  
      # Update the count of consecutive opponent defections
      if opponent_last_move == axl.Action.D:
          self.consecutive_opponent_defections += 1
      else:
          # Reset count if opponent cooperated
          self.consecutive_opponent_defections = 0
  
      # Check if the permanent defect condition is met
      if self.consecutive_opponent_defections >= 3:
          self.permanent_defect_mode = True
          return axl.Action.D  # Play Defect immediately upon switching
  
      # Apply the alternating strategy based on opponent's last move
      if opponent_last_move == axl.Action.C:
          return axl.Action.D
      else:  # opponent_last_move == axl.Action.D
          return axl.Action.C



# In the first round, always cooperate.  From the second round onwards, observe
# your opponent's move from the previous round and mirror it:  *   If your
# opponent cooperated in the previous round, you cooperate in the current round.
# *   If your opponent defected in the previous round, you defect in the current
# round.

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
      else:
          # Observe opponent's move from the previous round
          opponent_last_move = opponent.history[-1]
  
          # Mirror the opponent's previous move
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# In the first round, you will play Cooperate.  In every round thereafter: If
# your opponent played Cooperate in the immediately preceding round, you will
# play Cooperate. If your opponent played Defect in the immediately preceding
# round, you will play Defect.

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
      else:
          # Get the opponent's move from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# You will always choose to Defect, regardless of your opponent's previous
# actions or your own.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Here is a simple, cooperative strategy:  1.  **For the very first round:**
# Always choose to Cooperate (C). 2.  **For all subsequent rounds (rounds 2
# through 1000):**     *   If your opponent played Cooperate (C) in the
# immediately preceding round, you will also play Cooperate (C).     *   If your
# opponent played Defect (D) in the immediately preceding round, you will also
# play Defect (D).

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
      else:
          # Get the opponent's move from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# In the very first round, cooperate.  For every round thereafter: If your
# opponent cooperated in the immediately preceding round, you cooperate. If your
# opponent defected in the immediately preceding round, you defect.

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
      else:
          # Get the opponent's move from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# This strategy is designed to be relentlessly aggressive, prioritizing your
# individual gain by consistently choosing the action that historically yields
# the highest immediate payoff for you, while avoiding any risk of being
# exploited.  1.  **In the first round, play Defect.** 2.  **In all subsequent
# rounds:**     *   **If your opponent played Cooperate in the previous round,
# play Defect.** (This exploits their cooperation to secure the maximum
# individual payoff for yourself.)     *   **If your opponent played Defect in
# the previous round, play Defect.** (This ensures you are never the "sucker"
# and guarantees at least a moderate payoff, avoiding exploitation.)

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. In the first round, play Defect.
      if self.first_round():
          return axl.Action.D
      # 2. In all subsequent rounds:
      else:
          # If your opponent played Cooperate in the previous round, play Defect.
          # If your opponent played Defect in the previous round, play Defect.
          # Both conditions lead to playing Defect, so we can simply return Defect.
          return axl.Action.D



# Always begin by cooperating.  For every round thereafter: 1.  If your opponent
# cooperated in the previous round, you cooperate in the current round. 2.  If
# your opponent defected in the previous round, you defect in the current round.

class Cooperative_18(LLM_Strategy):
  n = 18
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # Always begin by cooperating.
          return axl.Action.C
      else:
          # For every round thereafter:
          # 1. If your opponent cooperated in the previous round, you cooperate in the current round.
          # 2. If your opponent defected in the previous round, you defect in the current round.
          opponent_last_move = opponent.history[-1]
          return opponent_last_move



# 1.  In the first round, choose to Cooperate. 2.  In every subsequent round,
# choose the same action (Cooperate or Defect) that your opponent chose in the
# immediately preceding round.

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
      else:
          # In every subsequent round, choose the same action that your opponent
          # chose in the immediately preceding round.
          return opponent.history[-1]



# Here is a simple, aggressive strategy for the iterated normal-form game:
# **Strategy: Relentless Exploitation**  1.  **Always Defect:** In every single
# round of the game, play Defect. 2.  **No Cooperation:** Do not play Cooperate
# under any circumstances.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Your strategy is based on direct reciprocity, aiming to foster and maintain
# mutual cooperation throughout the game.  1.  In the very first round, you will
# play Cooperate. 2.  In every subsequent round, you will observe your
# opponent's move from the previous round and respond accordingly:     *   If
# your opponent played Cooperate in the previous round, you will play Cooperate.
# *   If your opponent played Defect in the previous round, you will play
# Defect.

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
      else:
          # Observe opponent's move from the previous round
          opponent_last_move = opponent.history[-1]
  
          # Respond accordingly
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# Begin by cooperating in the first round.  In all subsequent rounds: 1.  If
# your opponent cooperated in the previous round, you cooperate. 2.  If your
# opponent defected in the previous round, you defect.

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
      else:
          # Get the opponent's move from the previous round
          opponent_previous_move = opponent.history[-1]
  
          if opponent_previous_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_previous_move == axl.Action.D
              return axl.Action.D



# In every round, without exception, you will choose to Defect. You will never
# cooperate, regardless of what your opponent has done in previous rounds or
# what you anticipate they might do.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# **Strategy:**  In the very first round, play Cooperate.  For every subsequent
# round, observe your opponent's move in the immediately preceding round and
# respond as follows:  1.  If your opponent played Cooperate in the previous
# round, you play Cooperate. 2.  If your opponent played Defect in the previous
# round, you play Defect.

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
      else:
          # Observe opponent's move in the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          # Respond based on the opponent's last move
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# In the first round, play Cooperate.  For every round after the first: 1.  If
# your opponent played Cooperate in the immediately preceding round, play
# Cooperate. 2.  If your opponent played Defect in the immediately preceding
# round, play Defect.

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
      else:
          # Get the opponent's move from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# 1.  In the first round, play Defect. 2.  For all subsequent rounds (rounds 2
# through 1000):     *   If your opponent played Cooperate in the previous
# round, play Defect.     *   If your opponent played Defect in the previous
# round, play Defect.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # The strategy description states:
      # 1. In the first round, play Defect.
      # 2. For all subsequent rounds (rounds 2 through 1000):
      #    * If your opponent played Cooperate in the previous round, play Defect.
      #    * If your opponent played Defect in the previous round, play Defect.
  
      # Both conditions for subsequent rounds (opponent played Cooperate or Defect)
      # lead to the same action: playing Defect.
      # The first round also specifies playing Defect.
      # Therefore, this strategy consistently plays Defect in every round.
      return axl.Action.D



# In the first round, play Cooperate.  For all subsequent rounds: *   If your
# opponent played Cooperate in the previous round, you play Cooperate. *   If
# your opponent played Defect in the previous round, you play Defect.

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
      else:
          # Get the opponent's move from the previous round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# In the first round, choose to Cooperate.  For all subsequent rounds: *   If
# your opponent chose to Cooperate in the previous round, you choose to
# Cooperate. *   If your opponent chose to Defect in the previous round, you
# choose to Defect.

class Neutral_21(LLM_Strategy):
  n = 21
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # In the first round, choose to Cooperate.
          return axl.Action.C
      else:
          # For all subsequent rounds:
          # Get the opponent's move from the previous round.
          opponent_last_move = opponent.history[-1]
  
          # If your opponent chose to Cooperate in the previous round, you choose to Cooperate.
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          # If your opponent chose to Defect in the previous round, you choose to Defect.
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# This strategy aims to aggressively maximize your own payoff by prioritizing
# immediate gains and exploiting any cooperation from your opponent, while
# attempting to reset negative cycles when beneficial.  1.  **In the very first
# round, play Defect.** 2.  **If your opponent played Cooperate in the previous
# round, play Defect.** 3.  **If your opponent played Defect in the previous
# round, play Cooperate.**

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. In the very first round, play Defect.
      if self.first_round():
          return axl.Action.D
      else:
          # Get the opponent's move from the previous round
          opponent_last_move = opponent.history[-1]
  
          # 2. If your opponent played Cooperate in the previous round, play Defect.
          if opponent_last_move == axl.Action.C:
              return axl.Action.D
          # 3. If your opponent played Defect in the previous round, play Cooperate.
          elif opponent_last_move == axl.Action.D:
              return axl.Action.C



# Here is your strategy:  1.  In the very first round, always play Cooperate. 2.
# In all subsequent rounds, observe what your opponent played in the immediate
# previous round:     a.  If your opponent played Cooperate in the last round,
# you should also play Cooperate in the current round.     b.  If your opponent
# played Defect in the last round, you should also play Defect in the current
# round.

class Cooperative_22(LLM_Strategy):
  n = 22
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # 1. In the very first round, always play Cooperate.
          return axl.Action.C
      else:
          # 2. In all subsequent rounds, observe what your opponent played in the immediate previous round:
          opponent_last_move = opponent.history[-1]
          if opponent_last_move == axl.Action.C:
              # a. If your opponent played Cooperate in the last round, you should also play Cooperate in the current round.
              return axl.Action.C
          else: # opponent_last_move == axl.Action.D
              # b. If your opponent played Defect in the last round, you should also play Defect in the current round.
              return axl.Action.D



# **Strategy: Tit-for-Tat**  1.  In the very first round of the game, you will
# choose to cooperate. 2.  In all subsequent rounds, you will base your action
# entirely on what your opponent did in the immediately preceding round:     *
# If your opponent chose to cooperate in the previous round, you will choose to
# cooperate in the current round.     *   If your opponent chose to defect in
# the previous round, you will choose to defect in the current round.

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
      else:
          # Get the opponent's last move
          opponent_last_move = opponent.history[-1]
  
          # Base the current action on the opponent's last move
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# This strategy, which we'll call "Aggressive Echo," aims to exploit cooperative
# opponents while quickly defending against aggressive ones.  1.  In the first
# round, play D (Defect). 2.  In all subsequent rounds, do what your opponent
# did in the *immediately preceding* round.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # In the first round, play D (Defect).
          return axl.Action.D
      else:
          # In all subsequent rounds, do what your opponent did in the immediately preceding round.
          return opponent.history[-1]



# This strategy aims to foster mutual cooperation by starting with a cooperative
# gesture and then mirroring your opponent's previous action.  1.  **In the very
# first round, play Cooperate.** 2.  **From the second round onwards, observe
# your opponent's move from the immediately preceding round:**     *   **If your
# opponent played Cooperate in the previous round, play Cooperate.**     *
# **If your opponent played Defect in the previous round, play Defect.**

class Cooperative_23(LLM_Strategy):
  n = 23
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. In the very first round, play Cooperate.
      if self.first_round():
          return axl.Action.C
      # 2. From the second round onwards, observe your opponent's move from the immediately preceding round:
      else:
          # Get the opponent's last move
          opponent_last_move = opponent.history[-1]
  
          # If your opponent played Cooperate in the previous round, play Cooperate.
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          # If your opponent played Defect in the previous round, play Defect.
          else: # opponent_last_move == axl.Action.D
              return axl.Action.D



# In the first round, play Cooperate.  In every subsequent round: *   If your
# opponent played Cooperate in the previous round, play Cooperate. *   If your
# opponent played Defect in the previous round, play Defect.

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
      else:
          # In subsequent rounds, play what the opponent played in the previous round.
          # opponent.history[-1] gives the opponent's last move.
          return opponent.history[-1]



# This strategy adopts an aggressive, exploitative approach, aiming to secure
# high payoffs by defaulting to defection while temporarily cooperating only
# when stuck in a low-scoring stalemate, to reset and re-attempt exploitation.
# 1.  **Start by playing Defect (D).** 2.  **In subsequent rounds, if your
# opponent played Cooperate (C) in the previous round:** Continue to play Defect
# (D) to maximize your score from their cooperation. 3.  **If your opponent
# played Defect (D) in the previous round:**     *   If you also played Defect
# (D) in the previous round (resulting in D,D): Play Cooperate (C) for this
# single round, then immediately revert to playing Defect (D) in the next round,
# regardless

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # 1. Start by playing Defect (D).
          return axl.Action.D
  
      opponent_last_move = opponent.history[-1]
      self_last_move = self.history[-1]
  
      # 2. In subsequent rounds, if your opponent played Cooperate (C) in the previous round:
      #    Continue to play Defect (D) to maximize your score from their cooperation.
      if opponent_last_move == axl.Action.C:
          return axl.Action.D
      # 3. If your opponent played Defect (D) in the previous round:
      elif opponent_last_move == axl.Action.D:
          # If you also played Defect (D) in the previous round (resulting in D,D):
          # Play Cooperate (C) for this single round, then immediately revert to playing Defect (D) in the next round, regardless
          if self_last_move == axl.Action.D:
              return axl.Action.C
          # If opponent played D, but we played C last round (C,D):
          # The strategy description implies a default to defection unless a specific
          # condition for cooperation (like the D,D stalemate) is met.
          # Therefore, in a (C,D) scenario, we revert to defection.
          else: # self_last_move == axl.Action.C
              return axl.Action.D



# This strategy is based on reciprocal cooperation.  1.  **In the first round:**
# Choose to Cooperate. 2.  **In all subsequent rounds:**     *   If your
# opponent chose to Cooperate in the previous round, choose to Cooperate.     *
# If your opponent chose to Defect in the previous round, choose to Defect.

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
      else:
          # In subsequent rounds, mirror the opponent's last move
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          else:  # opponent.history[-1] == axl.Action.D
              return axl.Action.D



# This strategy aims to foster cooperation while protecting against
# exploitation, adjusting based on the opponent's previous action to maximize
# your long-term score.  1.  In the first round, play Cooperate. 2.  In all
# subsequent rounds, play Cooperate if your opponent played Cooperate in the
# immediately preceding round. 3.  In all subsequent rounds, play Defect if your
# opponent played Defect in the immediately preceding round.

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
      else:
          # Get the opponent's action from the immediately preceding round
          opponent_last_action = opponent.history[-1]
  
          if opponent_last_action == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_action == axl.Action.D
              return axl.Action.D



# This strategy is designed to aggressively maximise your own score, primarily
# by exploiting cooperation and limiting your own vulnerability.  1.  **Always
# Defect** in the current round if your opponent played Cooperate in the
# previous round. 2.  **Always Defect** in the current round if you played
# Cooperate and your opponent played Defect in the previous round. 3.  **Always
# Cooperate** in the current round if you played Defect and your opponent played
# Defect in the previous round. 4.  **In the very first round of the game, play
# Defect.**

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 4: In the very first round of the game, play Defect.
      if self.first_round():
          return axl.Action.D
  
      # Get the last moves played by both players
      my_last_move = self.history[-1]
      opponent_last_move = opponent.history[-1]
  
      # Rule 1: Always Defect in the current round if your opponent played Cooperate in the previous round.
      if opponent_last_move == axl.Action.C:
          return axl.Action.D
      # If opponent did not cooperate (i.e., opponent defected), proceed to check other rules
      else:  # opponent_last_move == axl.Action.D
          # Rule 2: Always Defect in the current round if you played Cooperate and your opponent played Defect in the previous round.
          if my_last_move == axl.Action.C:
              return axl.Action.D
          # If you also defected in the previous round (and opponent defected), proceed to Rule 3
          else:  # my_last_move == axl.Action.D
              # Rule 3: Always Cooperate in the current round if you played Defect and your opponent played Defect in the previous round.
              return axl.Action.C



# To maximise your overall payoff through a cooperative approach, employ the
# following strategy:  1.  In the very first round, always choose to Cooperate.
# 2.  In every subsequent round, observe what your opponent did in the
# immediately preceding round:     *   If your opponent chose to Cooperate in
# the last round, you also choose to Cooperate in the current round.     *   If
# your opponent chose to Defect in the last round, you also choose to Defect in
# the current round.

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
      else:
          # Observe what the opponent did in the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          # If opponent cooperated, you cooperate
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          # If opponent defected, you defect
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# To maximize your overall payoff with a neutral approach:  1.  **In the first
# round, cooperate.** 2.  **For all subsequent rounds, play the move your
# opponent played in the immediately preceding round.**     *   If your opponent
# cooperated in the previous round, you cooperate in the current round.     *
# If your opponent defected in the previous round, you defect in the current
# round.

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
      else:
          # Play the move your opponent played in the immediately preceding round.
          return opponent.history[-1]
