import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# **The Strategy: Exploitative Defector**  1.  In the very first round, play
# Defect. 2.  In all subsequent rounds, observe your opponent's move from the
# immediately preceding round:     a.  If your opponent played Defect in the
# previous round, you play Defect.     b.  If your opponent played Cooperate in
# the previous round, you play Defect.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # The strategy description is as follows:
      # 1. In the very first round, play Defect.
      # 2. In all subsequent rounds, observe your opponent's move from the immediately preceding round:
      #    a. If your opponent played Defect in the previous round, you play Defect.
      #    b. If your opponent played Cooperate in the previous round, you play Defect.
  
      # Combining these rules, it's clear that in every scenario (first round, or subsequent rounds
      # regardless of the opponent's previous move), the strategy dictates playing Defect.
      return axl.Action.D



# **Strategy: Forgiving Tit-for-Tat with a Test**  1.  **For the very first
# round:** Always choose to cooperate (C).  2.  **For the second round:**     *
# If your opponent chose to cooperate (C) in the first round, you choose to
# cooperate (C).     *   If your opponent chose to defect (D) in the first
# round, you choose to defect (D).  3.  **For every round from the third round
# onwards:** Observe what your opponent chose in the *immediately preceding*
# round.     *   If your opponent chose to cooperate (C) in the previous round,
# you choose to cooperate (C) in the current round.     *   If your opponent
# chose to defect (D)

class Cooperative_1(LLM_Strategy):
  n = 1
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Always cooperate
      if len(self.history) == 0:
          return axl.Action.C
      # Round 2: Mirror opponent's first move
      elif len(self.history) == 1:
          return opponent.history[0]
      # Round 3 onwards: Standard Tit-for-Tat (mirror opponent's last move)
      else:
          return opponent.history[-1]



# Play Defection (D) in every round.

class Neutral_1(LLM_Strategy):
  n = 1
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# This strategy aims to aggressively pursue the highest possible individual
# payoff (5 points) while adapting to avoid prolonged mutual defection (1 point)
# and setting up future exploitation.  1.  **On the very first round, play
# Defect.** 2.  **In all subsequent rounds, observe your opponent's move from
# the previous round:**     *   **If your opponent played Cooperate:** Play
# Defect.     *   **If your opponent played Defect:** Play Cooperate for one
# round.         *   If your opponent responds by playing Cooperate, then in the
# *next* round, play Defect.         *   If your opponent responds by playing
# Defect, then in the *next* round, play Defect.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize a custom attribute to manage the strategy's state.
      # This flag indicates if the current round's move is a forced Defect,
      # which occurs after we've played Cooperate in response to an opponent's Defect.
      # It's initialized to False (or None) on the first round.
      if self.first_round():
          self._next_move_is_forced_D = False
          return axl.Action.D
  
      # Rule: If the strategy is in a state where the current move must be Defect
      # (because in the previous round, we played Cooperate in response to opponent's Defect)
      if self._next_move_is_forced_D:
          self._next_move_is_forced_D = False  # Reset the flag for future rounds
          return axl.Action.D
  
      # Rule: In all other subsequent rounds, observe the opponent's move from the previous round.
      opponent_last_move = opponent.history[-1]
  
      if opponent_last_move == axl.Action.C:
          # If your opponent played Cooperate, play Defect.
          return axl.Action.D
      else:  # opponent_last_move == axl.Action.D
          # If your opponent played Defect: Play Cooperate for one round.
          # Additionally, set the flag so that in the *next* round, we will play Defect,
          # regardless of the opponent's response to this Cooperate.
          self._next_move_is_forced_D = True
          return axl.Action.C



# In the first round, you will play Cooperate.  From the second round onwards:
# 1.  If your opponent played Cooperate in the previous round, you will play
# Cooperate. 2.  If your opponent played Defect in the previous round, you will
# play Defect. 3.  However, if your opponent has played Defect in the last 10
# consecutive rounds, you will play Defect for all remaining rounds.

class Cooperative_2(LLM_Strategy):
  n = 2
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attribute on the first round
      if self.first_round():
          self.locked_in_defect = False
          return axl.Action.C
  
      # Rule 3 (part 2): If already locked in due to previous consecutive defections,
      # continue playing Defect for all remaining rounds.
      if self.locked_in_defect:
          return axl.Action.D
  
      # Check for 10 consecutive defections by the opponent (Rule 3 part 1).
      # This check only applies if there have been at least 10 rounds played.
      if len(opponent.history) >= 10:
          # Get the opponent's last 10 moves
          last_10_opponent_moves = opponent.history[-10:]
          
          # If all of the last 10 moves were Defect, then lock in Defect.
          if last_10_opponent_moves.count(axl.Action.D) == 10:
              self.locked_in_defect = True
              return axl.Action.D
  
      # Rules 1 & 2: Tit-for-Tat like behavior.
      # If the opponent played Cooperate in the previous round, play Cooperate.
      # If the opponent played Defect in the previous round, play Defect.
      # This is equivalent to simply playing whatever the opponent played last.
      return opponent.history[-1]



# Your strategy for each round is as follows:  1.  For the very first round of
# the game, always choose to Cooperate. 2.  For all subsequent rounds, you will
# choose the same action that your opponent chose in the immediately preceding
# round.     *   If your opponent played Cooperate in the previous round, you
# will play Cooperate in the current round.     *   If your opponent played
# Defect in the previous round, you will play Defect in the current round.

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
      else:
          # For all subsequent rounds, choose the same action that your opponent
          # chose in the immediately preceding round.
          # opponent.history[-1] gives the opponent's last move.
          return opponent.history[-1]



# Here is a simple strategy for the iterated normal-form game:  1.  **In the
# first round, Defect.** 2.  **If your opponent cooperated in the previous
# round:** Cooperate. 3.  **If your opponent defected in the previous round:**
# Defect.

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
      else:
          # Check opponent's move in the previous round
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          else:  # opponent.history[-1] == axl.Action.D
              return axl.Action.D



# Here is the revised strategy:  1.  Cooperate in the first round. 2.  For
# rounds 2 through 999, do exactly what your opponent did in the immediately
# preceding round. 3.  In the final round (round 1000), defect.

class Cooperative_3(LLM_Strategy):
  n = 3
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      total_rounds = 1000
  
      if self.first_round():
          # 1. Cooperate in the first round.
          return axl.Action.C
      else:
          # Determine the current round number based on the history length.
          # If history length is N, N rounds have been played, so the current round is N + 1.
          current_round = len(self.history) + 1
  
          if current_round < total_rounds:
              # 2. For rounds 2 through 999, do exactly what your opponent did
              #    in the immediately preceding round.
              #    opponent.history[-1] gives the opponent's last move.
              return opponent.history[-1]
          else: # current_round == total_rounds (i.e., round 1000)
              # 3. In the final round (round 1000), defect.
              return axl.Action.D



# *   In the first round, play Cooperate. *   For rounds 2 through 990:     *
# If you have played Defect in the last 3 consecutive rounds AND your opponent
# has also played Defect in the last 3 consecutive rounds, then play Cooperate
# in the current round.     *   Otherwise, if your opponent has played Cooperate
# in the last 10 consecutive rounds, then play Defect in the current round.
# *   Otherwise, if your opponent played Cooperate in the immediately preceding
# round, play Cooperate.     *   Otherwise (if your opponent played Defect in
# the immediately preceding round), play Defect. *   For rounds 991 through
# 1000, always play Defect.

class Neutral_3(LLM_Strategy):
  n = 3
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Get the current round number (1-indexed).
      # len(self.history) gives the number of rounds already played.
      current_round = len(self.history) + 1
  
      # Rule 1: In the first round, play Cooperate.
      if current_round == 1:
          return axl.Action.C
  
      # Rule 3: For rounds 991 through 1000, always play Defect.
      if 991 <= current_round <= 1000:
          return axl.Action.D
  
      # Rule 2: For rounds 2 through 990, apply the following conditions in order.
      # This block executes if 2 <= current_round <= 990.
      else:
          # Condition 2.1: If you have played Defect in the last 3 consecutive rounds
          # AND your opponent has also played Defect in the last 3 consecutive rounds,
          # then play Cooperate in the current round.
          # This condition only applies if there have been at least 3 previous rounds.
          if current_round >= 4: # Equivalent to len(self.history) >= 3
              if (self.history[-3:] == [axl.Action.D] * 3 and
                  opponent.history[-3:] == [axl.Action.D] * 3):
                  return axl.Action.C
  
          # Condition 2.2: Otherwise, if your opponent has played Cooperate in the
          # last 10 consecutive rounds, then play Defect in the current round.
          # This condition only applies if there have been at least 10 previous rounds.
          if current_round >= 11: # Equivalent to len(self.history) >= 10
              if opponent.history[-10:] == [axl.Action.C] * 10:
                  return axl.Action.D
  
          # Condition 2.3: Otherwise, if your opponent played Cooperate in the
          # immediately preceding round, play Cooperate.
          # This condition applies for current_round >= 2, which is true in this 'else' block.
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          # Condition 2.4: Otherwise (if your opponent played Defect in the
          # immediately preceding round), play Defect.
          else:
              return axl.Action.D



# This strategy aims to maximize your overall payoff by aggressively punishing
# defection while being open to re-establishing cooperation for sustained gains.
# 1.  **Start with Cooperate.** 2.  **If your opponent cooperated in the
# previous round:** Play Cooperate. 3.  **If your opponent defected in the
# previous round:** Play Defect for the next two rounds, then revert to
# Cooperate.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attribute for the first round of the match.
      # punishment_rounds_left tracks how many *additional* rounds of Defect
      # we need to play after the current one, as part of a punishment sequence.
      # A value of 0 means no active punishment.
      if self.first_round():
          self.punishment_rounds_left = 0
          return axl.Action.C
  
      # Rule 3: If we are currently in a punishment phase (i.e., we need to play Defect
      # for one or more additional rounds).
      if self.punishment_rounds_left > 0:
          self.punishment_rounds_left -= 1  # Decrement the counter for this round's Defect
          return axl.Action.D
  
      # If not in a punishment phase, decide based on the opponent's last move.
      # opponent.history[-1] gives the opponent's move in the previous round.
      if opponent.history[-1] == axl.Action.C:
          # Rule 2: Opponent cooperated in the previous round, so we cooperate.
          return axl.Action.C
      else:  # opponent.history[-1] == axl.Action.D
          # Rule 3: Opponent defected in the previous round.
          # We initiate a two-round punishment:
          # We play Defect this round, and for one more round after this.
          self.punishment_rounds_left = 1
          return axl.Action.D



# This strategy aims to foster and maintain cooperation by responding to your
# opponent's actions, while also offering a chance to re-establish cooperation
# after breakdowns.  1.  In the first round, always play Cooperate. 2.  In every
# subsequent round, if your opponent played Cooperate in the immediately
# preceding round, you should also play Cooperate. 3.  If your opponent played
# Defect in the immediately preceding round, you should play Defect. 4.
# However, if you have played Defect for two consecutive rounds (meaning your
# opponent also played Defect for two consecutive rounds), then in the next
# round, play Cooperate to offer a chance to return to mutual cooperation.

class Cooperative_4(LLM_Strategy):
  n = 4
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. In the first round, always play Cooperate.
      if self.first_round():
          return axl.Action.C
  
      # Get the opponent's last move for the general Tit-for-Tat logic
      opponent_last_move = opponent.history[-1]
  
      # 4. However, if you have played Defect for two consecutive rounds
      # (meaning your opponent also played Defect for two consecutive rounds),
      # then in the next round, play Cooperate to offer a chance to return to mutual cooperation.
      # This condition only applies if there are at least two previous rounds played.
      if len(self.history) >= 2:
          # Check if both players have played Defect in the last two consecutive rounds
          my_last_two_moves = self.history[-2:]
          opponent_last_two_moves = opponent.history[-2:]
  
          if (my_last_two_moves == [axl.Action.D, axl.Action.D] and
              opponent_last_two_moves == [axl.Action.D, axl.Action.D]):
              return axl.Action.C  # Offer cooperation to re-establish it
  
      # 2. In every subsequent round, if your opponent played Cooperate in the immediately preceding round,
      # you should also play Cooperate.
      # 3. If your opponent played Defect in the immediately preceding round, you should play Defect.
      # This is the default Tit-for-Tat behavior, applied if rule 4 does not trigger.
      if opponent_last_move == axl.Action.C:
          return axl.Action.C
      else:  # opponent_last_move == axl.Action.D
          return axl.Action.D



# 1.  In the first round, play Defect. 2.  In every subsequent round:     *   If
# your opponent played Cooperate in the immediately preceding round, play
# Cooperate.     *   *However*, if your opponent played Defect in the
# immediately preceding round, and you have played Defect for the last two
# consecutive rounds, then play Cooperate.     *   Otherwise (your opponent
# played Defect in the immediately preceding round, but you have not played
# Defect for the last two consecutive rounds), play Defect.

class Neutral_4(LLM_Strategy):
  n = 4
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # 1. In the first round, play Defect.
          return axl.Action.D
  
      # In every subsequent round:
      opponent_last_move = opponent.history[-1]
  
      if opponent_last_move == axl.Action.C:
          # If your opponent played Cooperate in the immediately preceding round, play Cooperate.
          return axl.Action.C
      else:  # opponent_last_move == axl.Action.D
          # However, if your opponent played Defect in the immediately preceding round,
          # and you have played Defect for the last two consecutive rounds, then play Cooperate.
          # We need to ensure self.history has at least two moves to check the last two.
          # If len(self.history) < 2, it's impossible to have played Defect for the last two consecutive rounds.
          if len(self.history) >= 2 and \
             self.history[-1] == axl.Action.D and \
             self.history[-2] == axl.Action.D:
              return axl.Action.C
          else:
              # Otherwise (your opponent played Defect in the immediately preceding round,
              # but you have not played Defect for the last two consecutive rounds), play Defect.
              return axl.Action.D



# Here is your rewritten strategy:  **On every round:** Play Defect.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Here is the revised strategy:  In the first round, always cooperate.  For
# rounds 2 through 990: *   If your opponent cooperated in the immediately
# preceding round, you cooperate. *   If your opponent defected in the
# immediately preceding round, you defect. However, if you have been defecting
# for five consecutive rounds and your opponent cooperates, you resume
# cooperation.  For rounds 991 through 1000: *   Always defect.

class Cooperative_5(LLM_Strategy):
  n = 5
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on the first round
      if self.first_round():
          self.defection_streak = 0  # Counts my consecutive defections
  
      current_round = len(self.history) + 1  # Rounds are 1-indexed
  
      # Phase 1: Round 1
      if current_round == 1:
          self.defection_streak = 0  # Ensure streak is 0 as I cooperate
          return axl.Action.C
  
      # Phase 3: Rounds 991 through 1000
      if current_round >= 991:
          self.defection_streak += 1  # Increment streak as I'm defecting
          return axl.Action.D
  
      # Phase 2: Rounds 2 through 990
      # Get opponent's last move
      opponent_last_move = opponent.history[-1]
  
      # Check for the special exception condition first
      # "if you have been defecting for five consecutive rounds and your opponent cooperates, you resume cooperation."
      if self.defection_streak >= 5 and opponent_last_move == axl.Action.C:
          self.defection_streak = 0  # Reset streak as I'm about to cooperate
          return axl.Action.C
  
      # Normal logic for rounds 2-990 (if exception not met)
      if opponent_last_move == axl.Action.C:
          self.defection_streak = 0  # Reset streak as I'm about to cooperate
          return axl.Action.C
      else:  # opponent_last_move == axl.Action.D
          self.defection_streak += 1  # Increment streak as I'm about to defect
          return axl.Action.D



# Play as follows for each round:  1.  **For the very first round:** Always
# Defect. 2.  **For all subsequent rounds:**     *   If your opponent played
# Defect in the previous round AND also played Defect in the round before that,
# you will play Cooperate.     *   Otherwise, if your opponent played Cooperate
# in the previous round, you will play Cooperate.     *   Otherwise, you will
# play Defect.

class Neutral_5(LLM_Strategy):
  n = 5
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. For the very first round: Always Defect.
      if self.first_round():
          return axl.Action.D
  
      # 2. For all subsequent rounds:
      # Get the length of the opponent's history to safely access elements.
      # opponent.history will contain moves from previous rounds.
      # If it's the second round, len(opponent.history) will be 1.
      # If it's the third round, len(opponent.history) will be 2, and so on.
      history_length = len(opponent.history)
  
      # If your opponent played Defect in the previous round AND also played Defect in the round before that,
      # you will play Cooperate.
      # This condition requires at least two previous rounds to have been played by the opponent.
      if history_length >= 2 and \
         opponent.history[-1] == axl.Action.D and \
         opponent.history[-2] == axl.Action.D:
          return axl.Action.C
      # Otherwise, if your opponent played Cooperate in the previous round, you will play Cooperate.
      elif opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      # Otherwise, you will play Defect.
      else:
          return axl.Action.D



# This strategy prioritizes your score through consistent self-interest.  1.
# For every round of the game, always play Defect.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      """
      This strategy prioritizes your score through consistent self-interest.
      For every round of the game, always play Defect.
      """
      return axl.Action.D



# This strategy aims to maximise your overall payoff by fostering cooperation,
# forgiving limited defections, and protecting against end-game exploitation.
# 1.  **Initial Move:** In the very first round, cooperate. 2.  **Main Play
# (Rounds 2 through 990):**     *   If your opponent cooperated in the
# immediately preceding round, you cooperate in the current round.     *   If
# your opponent defected in the immediately preceding round:         *   You
# defect in the current round.         *   *However*, if you have played Defect
# for the last three consecutive rounds (meaning your own actions in rounds N-1,
# N-2, and N-3 were all Defect), then play Cooperate in the current round (N) to
# attempt to re-establish cooperation. 3.  **End Game (Rounds 991 through
# 1000):** In these final ten rounds, always defect, regardless of your
# opponent's previous moves.

class Cooperative_6(LLM_Strategy):
  n = 6
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
  
      # 1. Initial Move: In the very first round, cooperate.
      if current_round == 1:
          return axl.Action.C
  
      # 3. End Game (Rounds 991 through 1000): In these final ten rounds, always defect.
      if current_round >= 991:
          return axl.Action.D
  
      # 2. Main Play (Rounds 2 through 990):
      # Get opponent's move from the immediately preceding round
      opponent_last_move = opponent.history[-1]
  
      if opponent_last_move == axl.Action.C:
          # If your opponent cooperated in the immediately preceding round, you cooperate.
          return axl.Action.C
      else:  # opponent_last_move == axl.Action.D
          # If your opponent defected in the immediately preceding round:
          # Check if you have played Defect for the last three consecutive rounds.
          # This check requires at least 3 previous moves from self.
          if len(self.history) >= 3 and \
             self.history[-1] == axl.Action.D and \
             self.history[-2] == axl.Action.D and \
             self.history[-3] == axl.Action.D:
              # ...then play Cooperate in the current round to attempt to re-establish cooperation.
              return axl.Action.C
          else:
              # Otherwise (opponent defected, but you haven't defected 3 times consecutively),
              # you defect in the current round.
              return axl.Action.D



# On the first round, play Defect.  On the second round, play Cooperate.  On all
# subsequent rounds: If you have played Defect for two consecutive rounds, play
# Cooperate. Otherwise, if your opponent played Cooperate in the immediately
# preceding round, play Cooperate. Otherwise, play Defect.

class Neutral_6(LLM_Strategy):
  n = 6
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history)
  
      if round_number == 0:
          # On the first round, play Defect.
          return axl.Action.D
      elif round_number == 1:
          # On the second round, play Cooperate.
          return axl.Action.C
      else:
          # On all subsequent rounds (round_number >= 2):
  
          # If you have played Defect for two consecutive rounds, play Cooperate.
          # self.history[-1] is the move from the immediately preceding round.
          # self.history[-2] is the move from two rounds ago.
          if self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D:
              return axl.Action.C
          # Otherwise, if your opponent played Cooperate in the immediately preceding round, play Cooperate.
          # opponent.history[-1] is the opponent's move from the immediately preceding round.
          elif opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          # Otherwise, play Defect.
          else:
              return axl.Action.D



# **Strategy: Reciprocal Aggression**  This strategy aims to aggressively pursue
# the highest possible mutual payoffs while swiftly punishing any attempts at
# exploitation.  1.  **In the first round, play Cooperate.** 2.  **In all
# subsequent rounds, observe your opponent's move from the immediately preceding
# round.** 3.  **If your opponent played Cooperate in the previous round, play
# Cooperate.** 4.  **If your opponent played Defect in the previous round, play
# Defect.**

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
      else:
          # Observe opponent's move from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          # If opponent played Cooperate in the previous round, play Cooperate.
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          # If opponent played Defect in the previous round, play Defect.
          else: # opponent_last_move == axl.Action.D
              return axl.Action.D



# In the first round, play Cooperate.  For rounds 2 through 999: If your
# opponent played Cooperate in the previous round, play Cooperate. If your
# opponent played Defect in the previous round, play Defect.  In the final round
# (round 1000), play Defect.

class Cooperative_7(LLM_Strategy):
  n = 7
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
  
      if current_round == 1:
          # In the first round, play Cooperate.
          return axl.Action.C
      elif current_round >= 2 and current_round <= 999:
          # For rounds 2 through 999:
          # If your opponent played Cooperate in the previous round, play Cooperate.
          # If your opponent played Defect in the previous round, play Defect.
          opponent_previous_move = opponent.history[-1]
          if opponent_previous_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_previous_move == axl.Action.D
              return axl.Action.D
      elif current_round == 1000:
          # In the final round (round 1000), play Defect.
          return axl.Action.D
      else:
          # This case should not be reached if the game strictly lasts 1000 rounds.
          # As a fallback, we can default to Defect.
          return axl.Action.D



# 1.  **In the very first round, choose to defect.** 2.  **In the second
# round:**     *   If your opponent cooperated in the first round, you will
# cooperate.     *   If your opponent defected in the first round, you will
# defect. 3.  **From the third round onwards:**     *   If both you and your
# opponent cooperated in the previous round, you will choose to defect.     *
# Otherwise (if mutual cooperation did not occur in the previous round), you
# will replicate your opponent's move from the previous round.

class Neutral_7(LLM_Strategy):
  n = 7
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: In the very first round, choose to defect.
      if len(self.history) == 0:
          return axl.Action.D
  
      # Round 2:
      elif len(self.history) == 1:
          # If your opponent cooperated in the first round, you will cooperate.
          # If your opponent defected in the first round, you will defect.
          # This is equivalent to replicating the opponent's first move.
          return opponent.history[-1]
  
      # From the third round onwards:
      else: # len(self.history) >= 2
          my_last_move = self.history[-1]
          opponent_last_move = opponent.history[-1]
  
          # If both you and your opponent cooperated in the previous round, you will choose to defect.
          if my_last_move == axl.Action.C and opponent_last_move == axl.Action.C:
              return axl.Action.D
          # Otherwise (if mutual cooperation did not occur in the previous round),
          # you will replicate your opponent's move from the previous round.
          else:
              return opponent_last_move



# This strategy aims to aggressively pursue individual gain while adapting to
# avoid prolonged suboptimal outcomes.  1.  **Start by Defecting** in the first
# round. 2.  **If your opponent cooperated** in the previous round (you scored
# 5), **Defect again**. 3.  **If your opponent defected** in the previous round
# (you scored 1 or 0), **Cooperate** in the current round. 4.  **If you both
# cooperated** in the previous round (you scored 3), **Continue to Cooperate**.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # 1. Start by Defecting in the first round.
          return axl.Action.D
  
      # Get the moves from the previous round
      my_last_move = self.history[-1]
      opponent_last_move = opponent.history[-1]
  
      # 2. If your opponent cooperated in the previous round (you scored 5), Defect again.
      # This means: my_last_move was D and opponent_last_move was C.
      if opponent_last_move == axl.Action.C and my_last_move == axl.Action.D:
          return axl.Action.D
  
      # 3. If your opponent defected in the previous round (you scored 1 or 0), Cooperate in the current round.
      # This means: opponent_last_move was D. This covers cases where you scored 1 (D,D) or 0 (C,D).
      elif opponent_last_move == axl.Action.D:
          return axl.Action.C
  
      # 4. If you both cooperated in the previous round (you scored 3), Continue to Cooperate.
      # This means: my_last_move was C and opponent_last_move was C.
      elif opponent_last_move == axl.Action.C and my_last_move == axl.Action.C:
          return axl.Action.C
  
      # This part should theoretically not be reached if all conditions are mutually exclusive and exhaustive.
      # However, as a safeguard, we can return a default action, though it indicates a logic flaw if reached.
      # Given the rules cover all 4 combinations of (my_last_move, opponent_last_move), this line is unreachable.
      # (D, C) -> Rule 2
      # (D, D) -> Rule 3
      # (C, D) -> Rule 3
      # (C, C) -> Rule 4



# 1.  In the very first round, always cooperate. 2.  In every subsequent round:
# *   If your payoff in the immediately preceding round was 3 or 5, repeat the
# move you made in that preceding round.     *   If your payoff in the
# immediately preceding round was 0 or 1, switch the move you made in that
# preceding round (if you played C, play D; if you played D, play C).

class Cooperative_8(LLM_Strategy):
  n = 8
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. In the very first round, always cooperate.
      if self.first_round():
          return axl.Action.C
  
      # 2. In every subsequent round:
      # Get the move made by self and opponent in the immediately preceding round.
      my_last_move = self.history[-1]
      opponent_last_move = opponent.history[-1]
  
      # Calculate the payoff for self in the immediately preceding round based on the given matrix.
      my_last_payoff = 0
      if my_last_move == axl.Action.C and opponent_last_move == axl.Action.C:
          my_last_payoff = 3  # (C, C) -> self scores 3
      elif my_last_move == axl.Action.C and opponent_last_move == axl.Action.D:
          my_last_payoff = 0  # (C, D) -> self scores 0
      elif my_last_move == axl.Action.D and opponent_last_move == axl.Action.C:
          my_last_payoff = 5  # (D, C) -> self scores 5
      elif my_last_move == axl.Action.D and opponent_last_move == axl.Action.D:
          my_last_payoff = 1  # (D, D) -> self scores 1
  
      # Apply the rules based on the calculated payoff.
      if my_last_payoff == 3 or my_last_payoff == 5:
          # If your payoff was 3 or 5, repeat the move you made in that preceding round.
          return my_last_move
      elif my_last_payoff == 0 or my_last_payoff == 1:
          # If your payoff was 0 or 1, switch the move you made in that preceding round.
          if my_last_move == axl.Action.C:
              return axl.Action.D  # If last move was C, switch to D
          else:  # my_last_move == axl.Action.D
              return axl.Action.C  # If last move was D, switch to C



# On the first round, play Cooperate.  For every subsequent round: 1.  If your
# opponent played Cooperate in the immediately preceding round, play Cooperate.
# 2.  If your opponent played Defect in the immediately preceding round, play
# Defect.

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
      else:
          # Get the opponent's move from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D



# Here is the revised strategy:  1.  **In every round, from the first to the
# last:** Play Defect.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# This strategy aims to foster mutual cooperation by reciprocating actions,
# while offering a chance to re-establish cooperation after a period of
# conflict.  1.  **First Round:** You will choose to **Cooperate (C)**.  2.
# **Subsequent Rounds (General Rule):** For most rounds, you will observe your
# opponent's action from the *immediately preceding round* and choose your own
# action based on it:     *   If your opponent played **Cooperate (C)** in the
# previous round, you will play **Cooperate (C)** in the current round.     *
# If your opponent played **Defect (D)** in the previous round, you will play
# **Defect (D)** in the current round.  3.  **Forgiveness and Re-

class Cooperative_9(LLM_Strategy):
  n = 9
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. First Round: You will choose to Cooperate (C).
      if self.first_round():
          return axl.Action.C
      else:
          # 2. Subsequent Rounds (General Rule):
          # Observe your opponent's action from the immediately preceding round
          # and choose your own action based on it.
          # This implements a Tit-for-Tat mechanism.
          opponent_last_move = opponent.history[-1]
  
          # If your opponent played Cooperate (C) in the previous round,
          # you will play Cooperate (C) in the current round.
          # If your opponent played Defect (D) in the previous round,
          # you will play Defect (D) in the current round.
          return opponent_last_move



# In the first round, cooperate.  In all subsequent rounds: If you cooperated in
# the previous round:     If your score was 3, cooperate again.     If your
# score was 0, defect. If you defected in the previous round:     If your score
# was 5, defect again.     If your score was 1, cooperate.

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
  
      # Get the action played by self in the previous round
      my_last_action = self.history[-1]
  
      # Calculate the score self received in the previous round
      # self.total_scores returns a tuple (your_score, opponent_score) for the given history slices.
      # We only need the score from the last single interaction.
      my_last_round_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if my_last_action == axl.Action.C:
          # If you cooperated in the previous round:
          if my_last_round_score == 3:
              # If your score was 3 (implies opponent also cooperated), cooperate again.
              return axl.Action.C
          elif my_last_round_score == 0:
              # If your score was 0 (implies opponent defected), defect.
              return axl.Action.D
      elif my_last_action == axl.Action.D:
          # If you defected in the previous round:
          if my_last_round_score == 5:
              # If your score was 5 (implies opponent cooperated), defect again.
              return axl.Action.D
          elif my_last_round_score == 1:
              # If your score was 1 (implies opponent also defected), cooperate.
              return axl.Action.C
  
      # This part should theoretically be unreachable if all conditions are covered
      # by the strategy description and the payoff matrix.
      # For robustness, a default action could be returned, but the problem implies
      # that the given conditions are exhaustive.
      # The strategy description covers all possible outcomes for the previous round.



# Your strategy is as follows:  1.  In the very first round, play Defect. 2.  If
# your opponent played Cooperate in the previous round, play Cooperate. 3.  If
# your opponent played Defect in the previous round, play Defect.

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # 1. In the very first round, play Defect.
          return axl.Action.D
      else:
          # For subsequent rounds, check the opponent's last move.
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              # 2. If your opponent played Cooperate in the previous round, play Cooperate.
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              # 3. If your opponent played Defect in the previous round, play Defect.
              return axl.Action.D


# ---------------------------------------------------------
# MISSING AGGRESSIVE STRATEGIES (11 - 25)
# ---------------------------------------------------------

# Refined Strategy: Aggressive Probe. Start with D. If opponent cooperates, continue D to exploit.
# If opponent defects, switch to C for one round to try and trick them into cooperating, then immediately defect.
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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
      else:
          if self.history[-1] == axl.Action.D:
              return axl.Action.C
          return axl.Action.D

# Refined Strategy: Intermittent Defector. Always defect, but occasionally cooperate to prevent the opponent from locking into a permanent defection state.
class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) % 5 == 0 and not self.first_round():
          return axl.Action.C
      return axl.Action.D

# Refined Strategy: Suspicious Tit-For-Tat. Start with Defect to protect against early exploitation, then mimic the opponent.
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
      return opponent.history[-1]

# Refined Strategy: The Hit and Run. Cooperate in round 1 to build trust, then defect unconditionally forever.
class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return axl.Action.D

# Refined Strategy: Alternator. Alternate strictly between D and C to extract average gains while avoiding full retaliation.
class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) % 2 == 0:
          return axl.Action.D
      return axl.Action.C

# Refined Strategy: Opportunist. Always Defect.
class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# Refined Strategy: Delayed Grim Trigger. Always Defect.
class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# Refined Strategy: Two Defections, One Cooperation. Establish a baseline of dominance.
class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) % 3 == 2:
          return axl.Action.C
      return axl.Action.D

# Refined Strategy: Always Defect.
class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# Refined Strategy: End-game defector. Play D constantly.
class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# Refined Strategy: Suspicious Tit-for-Two-Tats. Start with D. Only cooperate if opponent cooperates twice in a row.
class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.D
      if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D

# Refined Strategy: Unyielding Aggressor.
class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# Refined Strategy: Confusion Aggressor. Defect on 1, Cooperate on 2, then Defect forever.
class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 1:
          return axl.Action.C
      return axl.Action.D

# Refined Strategy: Bully. Defect continuously until opponent defects 3 times in a row, then C once to reset.
class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) >= 3 and opponent.history[-3:] == [axl.Action.D]*3:
          return axl.Action.C
      return axl.Action.D

# Refined Strategy: Aggressive Grim Trigger. Start with D, never forgive.
class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D


# ---------------------------------------------------------
# MISSING COOPERATIVE STRATEGIES (10 - 25)
# ---------------------------------------------------------

# Refined Strategy: Tit for Two Tats (forgiving). Cooperate unless opponent defects twice in a row.
class Cooperative_10(LLM_Strategy):
  n = 10
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(opponent.history) < 2:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C

# Refined Strategy: Patient Cooperator. Cooperate until opponent defects 3 times in a row, then switch to TFT.
class Cooperative_11(LLM_Strategy):
  n = 11
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D]*3:
          return opponent.history[-1]
      return axl.Action.C

# Refined Strategy: Gentle Punisher. If opponent defects, defect once, then Cooperate to mend the relationship.
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
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D:
          return axl.Action.C
      return opponent.history[-1]

# Refined Strategy: Unconditional Cooperator. Never defect.
class Cooperative_13(LLM_Strategy):
  n = 13
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.C

# Refined Strategy: Pavlov (Win-stay, lose-shift). Cooperate if we both did the same thing last round.
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
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D

# Refined Strategy: Trust Builder. Play C for the first 10 rounds to signal absolute trust, then play TFT.
class Cooperative_15(LLM_Strategy):
  n = 15
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 10:
          return axl.Action.C
      return opponent.history[-1]

# Refined Strategy: Cycle Breaker. Play TFT. If both played D last round, play C to break the cycle.
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
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
      return opponent.history[-1]

# Refined Strategy: Majority Cooperator. Cooperate unless the opponent defect rate is > 50%.
class Cooperative_17(LLM_Strategy):
  n = 17
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round() or len(opponent.history) == 0:
          return axl.Action.C
      defect_rate = opponent.history.count(axl.Action.D) / len(opponent.history)
      if defect_rate > 0.5:
          return axl.Action.D
      return axl.Action.C

# Refined Strategy: Firm but Fair. If opponent defects, play D twice to ensure they learn the lesson, then C.
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
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C

# Refined Strategy: Generous Tit-for-Tat. Forgive defections deterministically (every 3rd defection is forgiven).
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
      if opponent.history[-1] == axl.Action.D:
          if opponent.history.count(axl.Action.D) % 3 == 0:
              return axl.Action.C
      return opponent.history[-1]

# Refined Strategy: Naive Peacekeeper. Always cooperate, ignoring history.
class Cooperative_20(LLM_Strategy):
  n = 20
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.C

# Refined Strategy: End-Game Cooperator. Cooperate entirely.
class Cooperative_21(LLM_Strategy):
  n = 21
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.C

# Refined Strategy: Suspicious Cooperator. Cooperate unless opponent defected in the last 2 rounds.
class Cooperative_22(LLM_Strategy):
  n = 22
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C

# Refined Strategy: Periodic Forgiveness. Play TFT but ALWAYS cooperate on round multiples of 10.
class Cooperative_23(LLM_Strategy):
  n = 23
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round() or len(self.history) % 10 == 0:
          return axl.Action.C
      return opponent.history[-1]

# Refined Strategy: Grudger. Play C until the opponent plays D, then D forever.
class Cooperative_24(LLM_Strategy):
  n = 24
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if axl.Action.D in opponent.history:
          return axl.Action.D
      return axl.Action.C

# Refined Strategy: Standard Tit for Tat. Start with C, mirror opponent.
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


# ---------------------------------------------------------
# MISSING NEUTRAL STRATEGIES (10 - 25)
# ---------------------------------------------------------

# Refined Strategy: Classic Tit for Tat.
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
      return opponent.history[-1]

# Refined Strategy: Randomish Alternator. Alternate C and D to remain unpredictable but balanced.
class Neutral_11(LLM_Strategy):
  n = 11
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) % 2 == 0:
          return axl.Action.C
      return axl.Action.D

# Refined Strategy: Shifted Mirror. Copy what the opponent did TWO rounds ago.
class Neutral_12(LLM_Strategy):
  n = 12
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(opponent.history) < 2:
          return axl.Action.C
      return opponent.history[-2]

# Refined Strategy: Pavlovian Neutral. Win-Stay, Lose-Shift.
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
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D

# Refined Strategy: Majority Mirror. Play the opponent most historically frequent move.
class Neutral_14(LLM_Strategy):
  n = 14
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round() or len(opponent.history) == 0:
          return axl.Action.C
      c_count = opponent.history.count(axl.Action.C)
      d_count = opponent.history.count(axl.Action.D)
      if d_count > c_count:
          return axl.Action.D
      return axl.Action.C

# Refined Strategy: Inverse TFT. Play the opposite of what the opponent played last round.
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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
      return axl.Action.C

# Refined Strategy: Suspicious Neutral. Start D, then Tit-for-Tat.
class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return opponent.history[-1]

# Refined Strategy: Tit for Two Tats.
class Neutral_17(LLM_Strategy):
  n = 17
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(opponent.history) < 2:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C

# Refined Strategy: 5-by-5. Cooperate 5 times, then Defect 5 times, repeat.
class Neutral_18(LLM_Strategy):
  n = 18
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if (len(self.history) // 5) % 2 == 0:
          return axl.Action.C
      return axl.Action.D

# Refined Strategy: Punishing Neutral. TFT but responds to a single D with three Ds.
class Neutral_19(LLM_Strategy):
  n = 19
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.punish_count = 0
          return axl.Action.C

      if self.punish_count > 0:
          self.punish_count -= 1
          return axl.Action.D

      if opponent.history[-1] == axl.Action.D:
          self.punish_count = 2
          return axl.Action.D

      return axl.Action.C

# Refined Strategy: Predictor Neutral. If opponent plays same move twice, assume they will again and match it. Else C.
class Neutral_20(LLM_Strategy):
  n = 20
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(opponent.history) < 2:
          return axl.Action.C
      if opponent.history[-1] == opponent.history[-2]:
          return opponent.history[-1]
      return axl.Action.C

# Refined Strategy: Last Round Defector. Play TFT, but guarantee D on round 1000.
class Neutral_21(LLM_Strategy):
  n = 21
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 999:
          return axl.Action.D
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]

# Refined Strategy: Double Mirror. Do whatever the opponent did, but twice.
class Neutral_22(LLM_Strategy):
  n = 22
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
      if len(self.history) % 2 == 0:
          return opponent.history[-1]
      return self.history[-1]

# Refined Strategy: Grudger.
class Neutral_23(LLM_Strategy):
  n = 23
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if axl.Action.D in opponent.history:
          return axl.Action.D
      return axl.Action.C

# Refined Strategy: Random Neutral Approximation. Play C mostly, but D if round ends in 7.
class Neutral_24(LLM_Strategy):
  n = 24
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) % 10 == 7:
          return axl.Action.D
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]

# Refined Strategy: Steady TFT.
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
      return opponent.history[-1]
