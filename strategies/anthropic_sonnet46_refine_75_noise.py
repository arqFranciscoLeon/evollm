import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# ## Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 997:** Defect
# if your opponent defected on the previous round. Cooperate if your opponent
# cooperated on the previous round.  **Rounds 998 to 1000:** Defect
# unconditionally.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 998:
          return axl.Action.D
      
      # Rounds 2 to 997
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          return axl.Action.C



# ## Strategy: Tit-for-Tat with Forgiveness and Late Endgame Defection
# **Opening move:** Cooperate on round 1.  **Rounds 2 through 998:** Apply the
# following conditions in order:  1. If the opponent has defected on three or
# more of the last five rounds, defect. 2. If the opponent defected last round
# but cooperated in at least three of the last five rounds, cooperate, treating
# their defection as a likely error and forgiving it. 3. Otherwise, mirror your
# opponent's most recent move. If they cooperated last round, cooperate. If they
# defected last round, defect.  **Rounds 999 and 1000:** Defect unconditionally,
# regardless of the opponent's behaviour.

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
      
      # Rounds 999 and 1000: defect unconditionally
      if round_number >= 999:
          return axl.Action.D
      
      # Rounds 2 through 998
      last_five = opponent.history[-5:]
      defections_in_last_five = last_five.count(axl.Action.D)
      cooperations_in_last_five = last_five.count(axl.Action.C)
      
      # Condition 1: opponent defected 3 or more of last 5 rounds
      if defections_in_last_five >= 3:
          return axl.Action.D
      
      # Condition 2: opponent defected last round but cooperated in at least 3 of last 5
      if opponent.history[-1] == axl.Action.D and cooperations_in_last_five >= 3:
          return axl.Action.C
      
      # Condition 3: mirror opponent's most recent move
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 990:** Track the opponent's
# last three moves. If the opponent has played D in two or more of their last
# three moves, play D. Otherwise, play C.  **Rounds 991 to 1000:** Play D
# unconditionally, regardless of the opponent's behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 991:
          return axl.Action.D
      
      # Rounds 2 to 990
      last_three = opponent.history[-3:]
      if last_three.count(axl.Action.D) >= 2:
          return axl.Action.D
      else:
          return axl.Action.C



# ## Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 1000:** Defect
# if any of the following conditions are met, checked in order:  1. Your
# opponent has defected on more than 30% of all rounds played so far. 2. You are
# within the last 5 rounds of the game (rounds 996 to 1000).  **Otherwise:**
# Cooperate.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      total_rounds = len(self.history)
      
      # Condition 1: Opponent defected more than 30% of rounds
      if opponent.history.defections / total_rounds > 0.30:
          return axl.Action.D
      
      # Condition 2: Within last 5 rounds (rounds 996-1000, i.e., index 995-999)
      # Current round number is total_rounds + 1 (1-indexed)
      current_round = total_rounds + 1
      if current_round >= 996:
          return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Forgiveness  **Opening move:** Cooperate on
# round 1.  **All subsequent rounds:** Apply the following conditions in order:
# 1. If the opponent has defected on both of the two most recent rounds, defect.
# 2. Otherwise, cooperate.

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
      
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 990:** Play according to the
# following conditions, checked in order:  - If your opponent has defected in
# three or more of the last five rounds, play D. - If your opponent has defected
# in the last two consecutive rounds, play D. - Otherwise, play C.  **Rounds 991
# to 1000:** Play D unconditionally.

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
      
      round_number = len(self.history) + 1
      
      # Rounds 991 to 1000: play D unconditionally
      if round_number >= 991:
          return axl.Action.D
      
      # Rounds 2 to 990
      # Check if opponent has defected in three or more of the last five rounds
      last_five = opponent.history[-5:]
      if last_five.count(axl.Action.D) >= 3:
          return axl.Action.D
      
      # Check if opponent has defected in the last two consecutive rounds
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      
      return axl.Action.C



# # Aggressive Defection Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:**
# Defect unconditionally, regardless of what your opponent played in any
# previous round.  ---  In plain terms: always defect for the entire game. The
# logic is as follows. Working backwards from round 1000, there is no future
# round in which a cooperative reputation can be leveraged, so defecting in
# round 1000 is always rational. The same reasoning applies to round 999, and by
# extension to every preceding round, meaning defection is the dominant choice
# in every round without exception. This guarantees you never score 0, secures
# at least 1 per round, and captures the full 5 whenever the opponent attempts
# cooperation. While mutual cooperation would yield 3 per round, this requires
# the opponent to cooperate reliably, which cannot be guaranteed and which this
# strategy makes no assumption about.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# ## Strategy: Tit-for-Tat with Forgiveness and Final-Round Defection  **Opening
# move:** Cooperate on round 1.  **Rounds 2 through 999:** Apply the following
# conditions in order:  1. If the opponent has defected in both of the two most
# recent rounds, defect. 2. Otherwise, cooperate.  **Round 1000:** Defect
# unconditionally.

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
      
      round_number = len(self.history) + 1
      
      if round_number == 1000:
          return axl.Action.D
      
      # Rounds 2 through 999
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 5:** Apply the following
# conditions in order:  1. If the opponent played D in the previous round, play
# D. 2. Otherwise, play C.  **Rounds 6 to 990:** Apply the following conditions
# in order:  1. If the opponent has played D in at least 2 of the last 5 rounds,
# play D. 2. If the opponent played C in the previous round, play C. 3.
# Otherwise, play D.  **Rounds 991 to 1000:** Play D.

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
      
      # Rounds 991 to 1000: Play D
      if round_number >= 991:
          return axl.Action.D
      
      # Rounds 2 to 5
      if round_number <= 5:
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.D
          else:
              return axl.Action.C
      
      # Rounds 6 to 990
      # Condition 1: If opponent has played D in at least 2 of the last 5 rounds
      last_5 = opponent.history[-5:]
      if last_5.count(axl.Action.D) >= 2:
          return axl.Action.D
      
      # Condition 2: If opponent played C in the previous round
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # Condition 3: Otherwise
      return axl.Action.D



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# any of the following conditions are met, checking them in order:  1. It is
# round 950 or later. 2. Your opponent has defected more than once in the last 5
# rounds. 3. Your opponent defected in each of the last 2 consecutive rounds.
# Otherwise, cooperate.  ---

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Defect
      if self.first_round():
          return axl.Action.D
      
      # Current round number (1-indexed)
      round_number = len(self.history) + 1
      
      # Condition 1: Round 950 or later
      if round_number >= 950:
          return axl.Action.D
      
      # Condition 2: Opponent has defected more than once in the last 5 rounds
      last_5 = opponent.history[-5:]
      if last_5.count(axl.Action.D) > 1:
          return axl.Action.D
      
      # Condition 3: Opponent defected in each of the last 2 consecutive rounds
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      # Otherwise, cooperate
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Forgiveness and End-Game Adjustment  **Opening
# move:** Cooperate on round 1.  **Rounds 2 onwards:** Mirror your opponent's
# previous move exactly. If they cooperated last round, cooperate. If they
# defected last round, defect.  **Forgiveness rule:** If you and your opponent
# have been in a mutual defection cycle for 3 or more consecutive rounds, offer
# forgiveness by cooperating once in an attempt to restore mutual cooperation.
# If the opponent responds with cooperation, return to mirroring. If the
# opponent responds with defection, return to defecting and do not offer
# forgiveness again for another 5 rounds.  **End-game rule:** Beginning from
# round 995, if your opponent defects at any point, defect for all remaining
# rounds without applying the forgiveness rule. If your opponent has been
# consistently cooperating up to and including round 994, continue cooperating
# through to round 1000, as the sustained mutual cooperation payoff of 3 per
# round exceeds the marginal gain from defecting late.

class Cooperative_4(LLM_Strategy):
  n = 4
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.mutual_defection_count = 0
          self.forgiveness_offered = False
          self.no_forgiveness_counter = 0
          self.end_game_defect = False
          return axl.Action.C
  
      current_round = len(self.history) + 1  # round we're about to play
  
      # End-game rule: from round 995 onwards
      if current_round >= 995:
          if self.end_game_defect:
              return axl.Action.D
          # Check if opponent defected at any point from round 995 onwards
          # We need to check if opponent defected in rounds 995 to current_round-1
          # Round 995 corresponds to index 994
          end_game_start_index = 994  # index of round 995
          if len(opponent.history) > end_game_start_index:
              end_game_opponent_moves = opponent.history[end_game_start_index:]
              if axl.Action.D in end_game_opponent_moves:
                  self.end_game_defect = True
                  return axl.Action.D
          # If opponent has been cooperating, continue cooperating
          return axl.Action.C
  
      # Update mutual defection count
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          self.mutual_defection_count += 1
      else:
          self.mutual_defection_count = 0
  
      # Decrement no_forgiveness_counter if active
      if self.no_forgiveness_counter > 0:
          self.no_forgiveness_counter -= 1
  
      # Check if we just offered forgiveness (forgiveness_offered flag)
      if self.forgiveness_offered:
          self.forgiveness_offered = False
          if last_opp == axl.Action.C:
              # Opponent cooperated in response to forgiveness, return to mirroring
              # Mirror opponent's last move (which was C)
              return axl.Action.C
          else:
              # Opponent defected in response to forgiveness, defect and set no_forgiveness_counter
              self.no_forgiveness_counter = 5
              return axl.Action.D
  
      # Forgiveness rule: mutual defection for 3+ consecutive rounds
      if self.mutual_defection_count >= 3 and self.no_forgiveness_counter == 0:
          # Offer forgiveness
          self.forgiveness_offered = True
          self.mutual_defection_count = 0
          return axl.Action.C
  
      # Standard Tit-for-Tat: mirror opponent's last move
      return last_opp



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 990:** Play C if any of the
# following conditions are met, checked in this order:  - Your opponent played C
# in the previous round. - Your opponent has defected in the previous three
# consecutive rounds but cooperated in the round before that sequence,
# indicating a possible accidental or exploratory defection pattern rather than
# persistent defection. Play C to attempt to restore mutual cooperation. - The
# total number of rounds your opponent has played D so far is fewer than 15% of
# all rounds played, indicating they are not a persistent defector despite
# occasional defections. Play C to attempt to restore mutual cooperation.
# Otherwise, play D.  **Rounds 991 to 1000:** Play D unconditionally, regardless
# of the opponent's behaviour, to protect against end-game defection by a
# rational opponent who anticipates no future punishment.

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
      
      round_number = len(self.history) + 1
      
      # Rounds 991 to 1000: play D unconditionally
      if round_number >= 991:
          return axl.Action.D
      
      # Rounds 2 to 990
      # Condition 1: Opponent played C in the previous round
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # Condition 2: Opponent defected in previous 3 consecutive rounds but cooperated in round before that
      if len(opponent.history) >= 4:
          last_three = opponent.history[-3:]
          round_before = opponent.history[-4]
          if (last_three.count(axl.Action.D) == 3 and round_before == axl.Action.C):
              return axl.Action.C
      
      # Condition 3: Total defections by opponent < 15% of all rounds played
      total_rounds = len(opponent.history)
      if total_rounds > 0:
          defection_rate = opponent.history.defections / total_rounds
          if defection_rate < 0.15:
              return axl.Action.C
      
      return axl.Action.D



# ## Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 990:** Defect
# if any of the following conditions apply, checked in order:  1. Your opponent
# has defected in at least two of the last three rounds. 2. Your opponent
# defected on the previous round and you defected on the previous round.
# Otherwise, cooperate.  **Rounds 991 to 1000:** Defect unconditionally.  ---
# This strategy opens cooperatively to invite mutual cooperation from the
# outset. During the main phase, it tolerates a single isolated defection
# without retaliating, avoiding overreaction to noise or accidental defection,
# but responds firmly to any pattern of persistent defection. Crucially, if both
# players have fallen into mutual defection, the strategy automatically returns
# to cooperation on the next round, breaking the deadlock and restoring the
# higher mutual payoff. The endgame clause locks in defection for the final ten
# rounds, limiting late-game exploitation while sacrificing fewer cooperative
# rounds than a longer endgame window would.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Cooperate
      if self.first_round():
          return axl.Action.C
      
      round_number = len(self.history) + 1  # Current round number (1-indexed)
      
      # Rounds 991 to 1000: Defect unconditionally
      if round_number >= 991:
          return axl.Action.D
      
      # Rounds 2 to 990
      # Condition 1: Opponent has defected in at least two of the last three rounds
      last_three = opponent.history[-3:]
      if last_three.count(axl.Action.D) >= 2:
          return axl.Action.D
      
      # Condition 2: Opponent defected on the previous round AND you defected on the previous round
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Otherwise, cooperate
      return axl.Action.C



# ## Strategy: Adaptive Tit-for-Tat  **Opening move:** Cooperate on round 1 as a
# deliberate signal of cooperative intent.  **From round 2 onwards, apply the
# following conditions in order:**  1. **If your opponent has defected on more
# than 90% of all rounds played so far, defect.** They have demonstrated
# persistent non-cooperation and further cooperation is not recoverable.  2.
# **If you and your opponent have both defected for the last 3 consecutive
# rounds, cooperate.** This acts as a forgiveness signal to break out of
# mutually damaging defection cycles and attempt to restore cooperation.  3.
# **If your opponent defected on the previous round, defect.** This mirrors
# their behaviour and discourages exploitation.  4. **Otherwise, cooperate.**

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
      
      rounds_played = len(self.history)
      
      # Condition 1: If opponent has defected more than 90% of all rounds
      if opponent.history.defections / rounds_played > 0.90:
          return axl.Action.D
      
      # Condition 2: If both have defected for the last 3 consecutive rounds
      if rounds_played >= 3:
          if (self.history[-3:].count(axl.Action.D) == 3 and
                  opponent.history[-3:].count(axl.Action.D) == 3):
              return axl.Action.C
      
      # Condition 3: If opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 4: Otherwise cooperate
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 5:** Play whatever your
# opponent played in the previous round.  **From round 6 onwards, apply the
# following conditions in order:**  1. If your opponent has defected in more
# than 90% of all rounds played so far, play D.  2. If there are 5 or fewer
# rounds remaining, play D.  3. If your opponent defected in the previous round
# but cooperated in at least 4 of the 5 rounds before that, play C.  4. If your
# opponent defected in both of the previous 2 rounds, play D.  5. Otherwise,
# play C.

class Neutral_5(LLM_Strategy):
  n = 5
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Play C
      if self.first_round():
          return axl.Action.C
      
      round_number = len(self.history) + 1  # This will be the round we're about to play
      total_rounds_played = len(self.history)
      
      # Rounds 2 to 5: Play whatever opponent played in previous round
      if total_rounds_played < 5:
          return opponent.history[-1]
      
      # From round 6 onwards (total_rounds_played >= 5)
      
      # Condition 1: If opponent has defected in more than 90% of all rounds played so far
      if total_rounds_played > 0:
          defection_rate = opponent.history.defections / total_rounds_played
          if defection_rate > 0.90:
              return axl.Action.D
      
      # Condition 2: If there are 5 or fewer rounds remaining
      # Game lasts 1000 rounds, so rounds remaining = 1000 - total_rounds_played
      rounds_remaining = 1000 - total_rounds_played
      if rounds_remaining <= 5:
          return axl.Action.D
      
      # Condition 3: If opponent defected in previous round but cooperated in at least 4 of the 5 rounds before that
      if opponent.history[-1] == axl.Action.D:
          if total_rounds_played >= 6:
              # 5 rounds before the previous round
              cooperations_in_5_before = opponent.history[-6:-1].count(axl.Action.C)
              if cooperations_in_5_before >= 4:
                  return axl.Action.C
      
      # Condition 4: If opponent defected in both of the previous 2 rounds
      if total_rounds_played >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      # Condition 5: Otherwise, play C
      return axl.Action.C



# ## Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 1000:** Defect
# if any of the following conditions are met, evaluated in order:  1. Your
# opponent defected on the previous round. 2. There are 3 or fewer rounds
# remaining.  Otherwise, cooperate.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      # Check if opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Check if there are 3 or fewer rounds remaining
      # Total rounds is 1000, current round number is len(self.history) + 1
      rounds_played = len(self.history)
      rounds_remaining = 1000 - rounds_played
      if rounds_remaining <= 3:
          return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Forgiveness  **Opening move:** Cooperate on
# round 1.  **For all subsequent rounds, apply the following conditions in
# order:**  1. If your opponent has defected on both of the previous two
# consecutive rounds, defect.  2. If your opponent cooperated on the previous
# round, cooperate.  3. Otherwise, cooperate.

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
      
      # Condition 1: If opponent defected on both of the previous two consecutive rounds
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      # Condition 2: If opponent cooperated on the previous round
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # Condition 3: Otherwise, cooperate
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 995:**  - If your opponent
# has defected in at least 8 of the last 10 rounds, play D. - If you and your
# opponent both defected in the previous round, play C. - Otherwise, play
# whatever your opponent played in the previous round.  **Rounds 996 to 1000:**
# Play D.

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
      
      round_number = len(self.history) + 1
      
      # Rounds 996 to 1000: Play D
      if round_number >= 996:
          return axl.Action.D
      
      # Rounds 2 to 995
      # Check if opponent defected in at least 8 of the last 10 rounds
      last_10 = opponent.history[-10:]
      if last_10.count(axl.Action.D) >= 8:
          return axl.Action.D
      
      # If both defected in the previous round, play C
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
      
      # Otherwise, play whatever opponent played in the previous round
      return opponent.history[-1]



# # Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 1000:** Defect
# if any of the following conditions are met, checking them in order:  1. The
# opponent defected on the previous round. 2. It is round 991 or later.
# **Otherwise:** Cooperate.  ---  This strategy opens cooperatively to signal
# willingness to engage in mutual cooperation, then mirrors the opponent's
# previous move. Any defection by the opponent is punished immediately with a
# retaliatory defect on the following round, returning to cooperation only once
# the opponent resumes cooperation. From round 991 onward the strategy defects
# unconditionally, exploiting any cooperative opponent during the final rounds
# where the threat of future retaliation loses its deterrent value, while
# accepting mutual defection payoffs against opponents who are already
# defecting.

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
      
      current_round = len(self.history) + 1
      
      # Check condition 1: opponent defected on previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Check condition 2: round 991 or later
      if current_round >= 991:
          return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Forgiveness  **Opening move:** Cooperate on
# round 1.  **Rounds 2 through 1000:** Apply the following conditions in order:
# 1. If the opponent has defected on three or more of the last five rounds,
# defect. 2. If the opponent defected last round but cooperated on at least
# three of the last five rounds, cooperate, giving them the benefit of the doubt
# and attempting to restore mutual cooperation. 3. If the opponent cooperated
# last round, cooperate. 4. Otherwise, cooperate.

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
      
      history_length = len(opponent.history)
      last_five = opponent.history[-5:]
      defections_in_last_five = last_five.count(axl.Action.D)
      cooperations_in_last_five = last_five.count(axl.Action.C)
      
      # Condition 1: If opponent defected on 3 or more of last 5 rounds, defect
      if defections_in_last_five >= 3:
          return axl.Action.D
      
      # Condition 2: If opponent defected last round but cooperated on at least 3 of last 5, cooperate
      if opponent.history[-1] == axl.Action.D and cooperations_in_last_five >= 3:
          return axl.Action.C
      
      # Condition 3: If opponent cooperated last round, cooperate
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # Condition 4: Otherwise, cooperate
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 990:**  - If your opponent
# has defected in at least 8 of the last 10 rounds, play D. - If you and your
# opponent have both defected for the last 3 consecutive rounds, play C. -
# Otherwise, play whatever your opponent played in the previous round.  **Rounds
# 991 to 1000:** Play D.

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
      
      round_number = len(self.history) + 1
      
      # Rounds 991 to 1000: Play D
      if round_number >= 991:
          return axl.Action.D
      
      # Rounds 2 to 990
      # Check if opponent has defected in at least 8 of the last 10 rounds
      if len(self.history) >= 10:
          last_10_defections = opponent.history[-10:].count(axl.Action.D)
          if last_10_defections >= 8:
              return axl.Action.D
      
      # Check if both have defected for the last 3 consecutive rounds
      if len(self.history) >= 3:
          self_last_3 = self.history[-3:]
          opp_last_3 = opponent.history[-3:]
          if (self_last_3.count(axl.Action.D) == 3 and 
                  opp_last_3.count(axl.Action.D) == 3):
              return axl.Action.C
      
      # Otherwise, play whatever opponent played in the previous round
      return opponent.history[-1]



# ## Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 1000:** Defect
# if any of the following conditions are met, checked in order:  1. You are
# within the last 10 rounds of the game (rounds 991 to 1000). 2. Your opponent
# has defected more than 30% of the time across all rounds played so far. 3.
# Your opponent defected on the previous round.  Otherwise, cooperate.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      # Current round number (1-indexed)
      round_number = len(self.history) + 1
      
      # Condition 1: Within last 10 rounds (rounds 991 to 1000)
      if round_number >= 991:
          return axl.Action.D
      
      # Condition 2: Opponent has defected more than 30% of the time
      total_rounds = len(opponent.history)
      if total_rounds > 0:
          defection_rate = opponent.history.defections / total_rounds
          if defection_rate > 0.30:
              return axl.Action.D
      
      # Condition 3: Opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Forgiveness and Final-Round Defection  **Opening
# move:** Cooperate on round 1.  **Rounds 2 through 999:** Apply the following
# conditions in order:  1. If your opponent has defected on both of the two most
# recent rounds, cooperate once as a gesture of reconciliation, then return to
# mirroring from the following round onward. 2. If your opponent defected on the
# most recent round, defect. 3. Otherwise, cooperate.  **Round 1000:** Defect
# unconditionally.

class Cooperative_8(LLM_Strategy):
  n = 8
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self._forgiveness_mode = False
          return axl.Action.C
      
      # Round 1000: defect unconditionally
      if len(self.history) == 999:  # About to play round 1000
          return axl.Action.D
      
      # Check if we're in forgiveness mode (cooperate once after two consecutive defections)
      if self._forgiveness_mode:
          self._forgiveness_mode = False
          return axl.Action.C
      
      # Rounds 2 through 999
      # Condition 1: If opponent defected on both of the two most recent rounds
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              self._forgiveness_mode = True
              return axl.Action.C
      
      # Condition 2: If opponent defected on the most recent round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 3: Otherwise, cooperate
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 999:** If your opponent
# played C in the previous round, play C. If your opponent played D in the
# previous round, play D. However, every 10 rounds, regardless of the opponent's
# previous move, play C to allow the possibility of restoring mutual cooperation
# if both players have become stuck in mutual defection.  **Round 1000:** Play
# D.

class Neutral_8(LLM_Strategy):
  n = 8
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Play C
      if self.first_round():
          return axl.Action.C
      
      # Round 1000: Play D
      current_round = len(self.history) + 1
      if current_round == 1000:
          return axl.Action.D
      
      # Every 10 rounds (rounds 10, 20, 30, ...), play C
      if current_round % 10 == 0:
          return axl.Action.C
      
      # Otherwise, mirror opponent's previous move (Tit for Tat)
      return opponent.history[-1]



# ## Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 1000:** Defect
# if any of the following conditions are met, checked in order:  1. It is round
# 990 or later. 2. Your opponent has defected on more than 30% of all rounds
# played so far. 3. Your opponent defected on both of the previous two rounds.
# Otherwise, cooperate.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      round_number = len(self.history) + 1  # current round number (1-indexed)
      rounds_played = len(self.history)
      
      # Condition 1: Round 990 or later
      if round_number >= 990:
          return axl.Action.D
      
      # Condition 2: Opponent defected on more than 30% of all rounds played so far
      if opponent.history.defections / rounds_played > 0.30:
          return axl.Action.D
      
      # Condition 3: Opponent defected on both of the previous two rounds
      if rounds_played >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Forgiveness  **Round 1:** Play C.  **Rounds 2 to
# 999:** Apply the following conditions in order:  1. If the current round is a
# multiple of 10, play C regardless of recent history. This acts as a periodic
# forgiveness mechanism to break any cycles of mutual defection that may have
# developed.  2. If your opponent played D in the previous round, play D.  3.
# Otherwise, play C.  **Round 1000:** Play D.  ---  **Clarifying notes:**  - The
# periodic forgiveness in condition 1 takes priority over retaliation in
# condition 2. This means that every tenth round you extend an unconditional
# olive branch, giving a defecting opponent a regular opportunity to return to
# mutual cooperation without either side needing to back down first. - Outside
# of forgiveness rounds, the strategy mirrors the opponent's last move exactly,
# rewarding cooperation with cooperation and punishing defection with defection.
# - Defection is reserved for the final round only, where there is no future
# round in which to benefit from restored cooperation, making mutual cooperation
# in round 999 still worthwhile for both sides.

class Cooperative_9(LLM_Strategy):
  n = 9
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Play C
      if self.first_round():
          return axl.Action.C
      
      # Determine current round number (1-indexed)
      current_round = len(self.history) + 1
      
      # Round 1000: Play D
      if current_round == 1000:
          return axl.Action.D
      
      # Rounds 2 to 999:
      # Condition 1: If current round is a multiple of 10, play C
      if current_round % 10 == 0:
          return axl.Action.C
      
      # Condition 2: If opponent played D in the previous round, play D
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 3: Otherwise, play C
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 997:** Play whatever your
# opponent played in the previous round. However, if your opponent has defected
# in more than 90% of all rounds played so far, switch permanently to D for the
# remainder of the game.  **Rounds 998 to 1000:** Play D unconditionally.

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
      
      round_number = len(self.history) + 1
      
      # Rounds 998 to 1000: Play D unconditionally
      if round_number >= 998:
          return axl.Action.D
      
      # Check if opponent has defected in more than 90% of all rounds played so far
      total_rounds = len(opponent.history)
      if total_rounds > 0:
          defection_rate = opponent.history.defections / total_rounds
          if defection_rate > 0.90:
              return axl.Action.D
      
      # Play whatever opponent played in the previous round (Tit for Tat)
      return opponent.history[-1]



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2–992:** Apply the
# following conditions in order:  1. If your opponent has defected in the most
# recent round, defect. 2. If you have defected in the most recent round and
# your opponent cooperated, cooperate. 3. Otherwise, cooperate.  **Rounds
# 993–1000:** Defect unconditionally.

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Defect
      if self.first_round():
          return axl.Action.D
      
      round_number = len(self.history) + 1  # Current round (1-indexed)
      
      # Rounds 993-1000: Defect unconditionally
      if round_number >= 993:
          return axl.Action.D
      
      # Rounds 2-992: Apply conditions in order
      # 1. If opponent defected in the most recent round, defect
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # 2. If you defected in the most recent round and opponent cooperated, cooperate
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # 3. Otherwise, cooperate
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Forgiveness  **Opening move:** Cooperate on
# round 1.  **All subsequent rounds:** Apply the following conditions in order:
# 1. If your opponent has cooperated on every single round so far, cooperate. 2.
# If your opponent defected on the previous round but cooperated on the round
# before that, cooperate. 3. If your opponent has defected for two or more
# consecutive rounds, defect. 4. Otherwise, cooperate.

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
      
      # Condition 1: If opponent has cooperated on every single round so far
      if opponent.history.defections == 0:
          return axl.Action.C
      
      # Condition 2: If opponent defected on previous round but cooperated on round before that
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
      
      # Condition 3: If opponent has defected for two or more consecutive rounds
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      # Condition 4: Otherwise, cooperate
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 999:**  - If the opponent has
# defected in every single round played so far, play D. - If the opponent played
# C in the previous round, play C. - If the opponent played D in the previous
# round, play D. - If you have been in a state of mutual defection for 3 or more
# consecutive rounds, play C to attempt to restore cooperation.  **Round 1000:**
# Play D.

class Neutral_10(LLM_Strategy):
  n = 10
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Play C
      if self.first_round():
          return axl.Action.C
      
      # Round 1000: Play D
      if len(self.history) == 999:  # About to play round 1000
          return axl.Action.D
      
      # Rounds 2 to 999:
      
      # If the opponent has defected in every single round played so far, play D
      if opponent.history.defections == len(opponent.history):
          return axl.Action.D
      
      # Check if we have been in mutual defection for 3 or more consecutive rounds
      if len(self.history) >= 3:
          mutual_defection_streak = 0
          for i in range(1, len(self.history) + 1):
              if self.history[-i] == axl.Action.D and opponent.history[-i] == axl.Action.D:
                  mutual_defection_streak += 1
              else:
                  break
          if mutual_defection_streak >= 3:
              return axl.Action.C
      
      # If the opponent played C in the previous round, play C
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # If the opponent played D in the previous round, play D
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      return axl.Action.C



# # Aggressive Strategy  **Round 1:** Cooperate.  **All subsequent rounds:**
# Defect if any of the following conditions are met, checked in order:  1. There
# are 10 or fewer rounds remaining. 2. Your opponent defected on the previous
# round.  **Otherwise:** Cooperate.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      # Check if there are 10 or fewer rounds remaining
      total_rounds = 1000
      rounds_played = len(self.history)
      rounds_remaining = total_rounds - rounds_played
      
      if rounds_remaining <= 10:
          return axl.Action.D
      
      # Check if opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Generous Tit-for-Tat  **Opening move:** Cooperate on round 1.
# **All subsequent rounds:** Mirror your opponent's previous move with one
# exception: if your opponent defected last round but cooperated in the majority
# of the rounds before that, cooperate anyway.  Otherwise, if your opponent has
# been defecting consistently, defect until they return to cooperation, then
# cooperate on the following round.

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
      
      # Get opponent's last move
      last_move = opponent.history[-1]
      
      # If opponent cooperated last round, cooperate
      if last_move == axl.Action.C:
          return axl.Action.C
      
      # Opponent defected last round
      # Check if they cooperated in the majority of rounds before that
      if len(opponent.history) >= 2:
          previous_history = opponent.history[:-1]
          previous_cooperations = list(previous_history).count(axl.Action.C)
          previous_defections = list(previous_history).count(axl.Action.D)
          
          if previous_cooperations > previous_defections:
              # Majority cooperated before last round - be generous, cooperate
              return axl.Action.C
          else:
              # Opponent has been defecting consistently
              # Defect until they return to cooperation
              return axl.Action.D
      else:
          # Only one round of history (the last move which was D)
          # No prior history to check majority, treat as consistent defector
          return axl.Action.D



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 990:** Play whatever your
# opponent played in the previous round. However, if your opponent has defected
# in at least 90% of the previous 10 rounds, defect unconditionally for the
# remainder of this period regardless of what they play.  **Rounds 991 to
# 1000:** Defect unconditionally.

class Neutral_11(LLM_Strategy):
  n = 11
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_unconditionally = False
          return axl.Action.C
      
      round_number = len(self.history) + 1
      
      # Rounds 991 to 1000: defect unconditionally
      if round_number >= 991:
          return axl.Action.D
      
      # Rounds 2 to 990
      # Check if opponent has defected in at least 90% of the previous 10 rounds
      if not self._defect_unconditionally:
          last_10 = opponent.history[-10:]
          if len(last_10) >= 10:
              defections_in_last_10 = last_10.count(axl.Action.D)
              if defections_in_last_10 / 10 >= 0.9:
                  self._defect_unconditionally = True
      
      if self._defect_unconditionally:
          return axl.Action.D
      
      # Play whatever opponent played in the previous round (Tit for Tat)
      return opponent.history[-1]



# # Aggressive Tit-for-Tat Strategy  **Round 1:** Defect.  **Rounds 2 through
# 990:** If your opponent cooperated on the previous round, defect. If your
# opponent defected on the previous round, cooperate.  **Rounds 991 through
# 1000:** Defect unconditionally regardless of what your opponent does.  ---  In
# plain terms: exploit any cooperation your opponent shows by defecting, but
# respond to their defection with cooperation to invite them back into a
# cooperative pattern that you can exploit again. This creates a cycle where you
# frequently capture the temptation payoff of 5 while limiting extended periods
# of mutual defection that yield only 1 per round. In the final ten rounds,
# defect unconditionally since there is no future interaction in which the
# opponent can punish you, making defection the dominant choice regardless of
# the opponent's actions.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Defect
      if self.first_round():
          return axl.Action.D
      
      # Determine current round number (1-indexed)
      round_number = len(self.history) + 1
      
      # Rounds 991 through 1000: Defect unconditionally
      if round_number >= 991:
          return axl.Action.D
      
      # Rounds 2 through 990: Inverse Tit-for-Tat
      # If opponent cooperated last round, defect
      # If opponent defected last round, cooperate
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
      else:
          return axl.Action.C



# ## Strategy: Tit-for-Tat with Forgiveness and Late-Game Defection  **Opening
# move:** Cooperate on round 1.  **Rounds 2 through 997:** Apply the following
# conditions in order:  - If the current round is a multiple of 50, cooperate
# regardless of the opponent's recent behaviour. This acts as a periodic reset
# to test whether mutual cooperation can be established or re-established with
# an opponent who has been defecting. - If your opponent has defected in both of
# the previous two rounds, and the most recent forgiveness round did not result
# in your opponent cooperating, defect. - Otherwise, mirror your opponent's
# previous move exactly. If they cooperated last round, cooperate. If they
# defected last round, defect.  **Rounds 998 through 1000:** Defect
# unconditionally. This window is short enough that a Tit-for-Tat opponent can
# retaliate only twice, limiting the cost of retaliation while still capturing
# the end-game defection bonus against cooperative opponents.

class Cooperative_12(LLM_Strategy):
  n = 12
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self._last_forgiveness_round = None
          self._forgiveness_opponent_cooperated = None
          return axl.Action.C
      
      current_round = len(self.history) + 1  # Round we're about to play
      
      # Rounds 998-1000: Defect unconditionally
      if current_round >= 998:
          return axl.Action.D
      
      # Rounds 2-997
      # Check if current round is a multiple of 50
      if current_round % 50 == 0:
          # Record this forgiveness round and check if opponent cooperated last round
          # We'll track the forgiveness round number and whether opponent cooperated after it
          self._last_forgiveness_round = current_round
          # Check if the previous forgiveness round resulted in opponent cooperating
          # (This will be evaluated next time we need it)
          return axl.Action.C
      
      # Update forgiveness tracking: check if the last forgiveness round resulted in cooperation
      # The forgiveness round was at round X (we cooperated), opponent's response was at round X
      # (opponent's move in round X is opponent.history[X-1])
      if self._last_forgiveness_round is not None:
          forgiveness_idx = self._last_forgiveness_round - 1  # 0-indexed
          if forgiveness_idx < len(opponent.history):
              self._forgiveness_opponent_cooperated = (opponent.history[forgiveness_idx] == axl.Action.C)
      
      # Check if opponent defected in both of the previous two rounds
      if len(opponent.history) >= 2:
          opp_last = opponent.history[-1]
          opp_second_last = opponent.history[-2]
          
          if opp_last == axl.Action.D and opp_second_last == axl.Action.D:
              # Check if the most recent forgiveness round resulted in opponent cooperating
              if self._forgiveness_opponent_cooperated is False or self._forgiveness_opponent_cooperated is None:
                  # Most recent forgiveness did not result in cooperation (or no forgiveness yet)
                  # But we need to be careful: if no forgiveness round has occurred yet,
                  # treat as if forgiveness did not result in cooperation
                  if self._last_forgiveness_round is None:
                      return axl.Action.D
                  else:
                      if not self._forgiveness_opponent_cooperated:
                          return axl.Action.D
      
      # Otherwise, mirror opponent's previous move
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 997:** Play whatever your
# opponent played in the previous round.  **Rounds 998 to 1000:** Play D
# unconditionally.

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
      
      if round_number >= 998:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 1000:** Defect
# if any of the following conditions are met, checked in order:  1. Your
# opponent defected on the previous round. 2. It is round 980 or later.
# Otherwise, cooperate.

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      # Condition 1: Opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 2: It is round 980 or later
      current_round = len(self.history) + 1  # next round number
      if current_round >= 980:
          return axl.Action.D
      
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 onwards:** Apply the following
# conditions in order:  1. If the opponent has defected in at least 3 of the
# last 5 rounds, play D. 2. If you played D in the previous round and the
# opponent played C, play C. 3. If the opponent played C in the previous round,
# play C. 4. Otherwise, play D.

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
      
      # Condition 1: If opponent defected in at least 3 of last 5 rounds, play D
      last_5 = opponent.history[-5:]
      if last_5.count(axl.Action.D) >= 3:
          return axl.Action.D
      
      # Condition 2: If I played D last round and opponent played C, play C
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # Condition 3: If opponent played C last round, play C
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # Otherwise, play D
      return axl.Action.D



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 995:** Apply the following
# conditions in order:  1. If the opponent has played D in at least 2 of the
# last 5 rounds, play D. 2. If the opponent played C in the previous round and D
# in none of the last 5 rounds, play C. 3. Play D.  **Rounds 996 to 1000:** Play
# D.

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
      
      round_number = len(self.history) + 1
      
      # Rounds 996 to 1000: Play D
      if round_number >= 996:
          return axl.Action.D
      
      # Rounds 2 to 995
      last_5 = opponent.history[-5:]
      defections_in_last_5 = last_5.count(axl.Action.D)
      
      # Condition 1: If opponent has played D in at least 2 of the last 5 rounds, play D
      if defections_in_last_5 >= 2:
          return axl.Action.D
      
      # Condition 2: If opponent played C in the previous round and D in none of the last 5 rounds, play C
      if opponent.history[-1] == axl.Action.C and defections_in_last_5 == 0:
          return axl.Action.C
      
      # Condition 3: Play D
      return axl.Action.D



# ## Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 997:**
# Cooperate if the opponent cooperated in the previous round. Defect if the
# opponent defected in the previous round. However, if mutual defection has
# persisted for 3 or more consecutive rounds, cooperate unconditionally to
# attempt to restore cooperation.  **Rounds 998 to 1000:** Defect
# unconditionally, regardless of the opponent's previous actions.

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
      
      round_number = len(self.history) + 1
      
      # Rounds 998 to 1000: defect unconditionally
      if round_number >= 998:
          return axl.Action.D
      
      # Rounds 2 to 997
      # Check if mutual defection has persisted for 3 or more consecutive rounds
      if len(self.history) >= 3:
          last_3_self = self.history[-3:]
          last_3_opp = opponent.history[-3:]
          mutual_defection = all(
              last_3_self[i] == axl.Action.D and last_3_opp[i] == axl.Action.D
              for i in range(3)
          )
          if mutual_defection:
              return axl.Action.C
      
      # Tit-for-tat: mirror opponent's last move
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D



# ## Strategy: Forgiving Tit-for-Tat  **Opening move:** Cooperate on round 1.
# **All subsequent rounds:** Apply the following conditions in order:  1. If
# your opponent has defected in either of the last two rounds but cooperated in
# the most recent round, cooperate, giving them the benefit of the doubt and
# forgiving isolated defections.  2. If your opponent defected in both of the
# last two rounds, defect.  3. Otherwise, mirror your opponent's most recent
# move exactly. If they cooperated, cooperate. If they defected, defect.

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
      
      # Get the history length
      history_len = len(opponent.history)
      
      if history_len >= 2:
          last_move = opponent.history[-1]
          second_last_move = opponent.history[-2]
          
          # Condition 1: Opponent defected in either of last two rounds but cooperated most recently
          if (second_last_move == axl.Action.D or last_move == axl.Action.D) and last_move == axl.Action.C:
              return axl.Action.C
          
          # Condition 2: Opponent defected in both of the last two rounds
          if last_move == axl.Action.D and second_last_move == axl.Action.D:
              return axl.Action.D
          
          # Condition 3: Mirror opponent's most recent move
          return last_move
      
      else:
          # Only one round has been played, mirror the opponent's last move
          return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 997:** Check your opponent's
# last three moves. If they defected in two or more of those three moves, play
# D. Otherwise, play C.  **Rounds 998 to 1000:** Play D unconditionally.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 998:
          return axl.Action.D
      
      # Rounds 2 to 997
      last_three = opponent.history[-3:]
      defections = last_three.count(axl.Action.D)
      
      if defections >= 2:
          return axl.Action.D
      else:
          return axl.Action.C



# ## Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 1000:** Defect
# if any of the following conditions are met, checked in order:  1. There are 8
# rounds or fewer remaining in the game. 2. Your opponent has defected more than
# 20% of the time across all rounds played so far.  Otherwise, cooperate.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      total_rounds = 1000
      rounds_played = len(self.history)
      rounds_remaining = total_rounds - rounds_played
      
      # Condition 1: 8 or fewer rounds remaining
      if rounds_remaining <= 8:
          return axl.Action.D
      
      # Condition 2: Opponent has defected more than 20% of the time
      if opponent.history.defections / rounds_played > 0.20:
          return axl.Action.D
      
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 994:** Play C if the opponent
# has played C in at least 90% of all rounds played so far. Otherwise, play D.
# **Rounds 995 to 1000:** Play D unconditionally.  ---  The 90% threshold
# provides tolerance for occasional defections or noise without immediately
# triggering sustained retaliation, while still punishing consistently
# uncooperative opponents. Cooperation can naturally be restored after an
# isolated defection as the opponent's overall cooperation rate recovers. The
# endgame defection window is extended slightly to reduce the incentive for the
# opponent to begin defecting early in anticipation of it.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 995:
          return axl.Action.D
      
      # Rounds 2 to 994
      total_rounds = len(opponent.history)
      if total_rounds == 0:
          return axl.Action.C
      
      coop_rate = opponent.history.cooperations / total_rounds
      
      if coop_rate >= 0.90:
          return axl.Action.C
      else:
          return axl.Action.D



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 993:** If the opponent played
# C in the previous round, play C. If the opponent played D in the previous
# round, play D. However, every 10 rounds, regardless of the opponent's previous
# move, play C as a gesture of reconciliation to break any cycle of mutual
# defection and attempt to restore cooperation.  **Rounds 994 to 1000:** Play D
# unconditionally.

class Neutral_15(LLM_Strategy):
  n = 15
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Play C
      if self.first_round():
          return axl.Action.C
      
      current_round = len(self.history) + 1  # The round we're about to play
      
      # Rounds 994 to 1000: Play D unconditionally
      if current_round >= 994:
          return axl.Action.D
      
      # Every 10 rounds (rounds 10, 20, 30, ...), play C as reconciliation
      if current_round % 10 == 0:
          return axl.Action.C
      
      # Rounds 2 to 993: Tit-for-tat
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D



# # Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 through 990:**
# Defect if your opponent defected on the previous round. Cooperate if your
# opponent cooperated on the previous round.  **Rounds 991 through 1000:**
# Defect unconditionally, regardless of your opponent's previous actions.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      current_round = len(self.history) + 1
      
      if current_round >= 991:
          return axl.Action.D
      
      # Rounds 2 through 990: mirror opponent's last move
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          return axl.Action.C



# ## Strategy: Tit-for-Tat with Forgiveness  **Opening move:** Cooperate on
# round 1.  **All subsequent rounds:** Apply the following conditions in order:
# 1. If the opponent has defected on more than 90% of all rounds played so far,
# defect. 2. If the opponent cooperated on their previous move, cooperate. 3. If
# the opponent defected on their previous move, defect for one round, then
# return to cooperation regardless of what the opponent does in that intervening
# round.

class Cooperative_16(LLM_Strategy):
  n = 16
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Opening move: Cooperate on round 1
      if self.first_round():
          self.punishing = False
          return axl.Action.C
      
      # Condition 1: If opponent has defected on more than 90% of all rounds played so far, defect
      total_rounds = len(opponent.history)
      if total_rounds > 0:
          defection_rate = opponent.history.defections / total_rounds
          if defection_rate > 0.9:
              return axl.Action.D
      
      # Condition 3 handling: If we are in punishment mode (opponent defected last round)
      # defect for one round, then return to cooperation
      if self.punishing:
          self.punishing = False
          return axl.Action.D
      
      # Condition 2: If the opponent cooperated on their previous move, cooperate
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # Condition 3: If the opponent defected on their previous move, set punishing flag
      # and defect next round (this round), then return to cooperation
      if opponent.history[-1] == axl.Action.D:
          self.punishing = True
          return axl.Action.D
      
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 999:**  - If your opponent
# has defected in every single round played so far, play D. - Otherwise, if your
# opponent played D in the previous round, play C with the intention of re-
# establishing cooperation, but only if the total number of rounds your opponent
# has defected so far represents less than half of all rounds played. If it
# represents half or more, play D. - Otherwise, play whatever your opponent
# played in the previous round.  **Round 1000:** Play D.

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
      
      round_number = len(self.history) + 1
      
      # Round 1000: Play D
      if round_number == 1000:
          return axl.Action.D
      
      # Rounds 2 to 999
      rounds_played = len(self.history)
      opponent_defections = opponent.history.defections
      
      # If opponent has defected in every single round played so far
      if opponent_defections == rounds_played:
          return axl.Action.D
      
      # If opponent played D in the previous round
      if opponent.history[-1] == axl.Action.D:
          # Check if opponent's defections represent less than half of all rounds played
          if opponent_defections < rounds_played / 2:
              return axl.Action.C
          else:
              return axl.Action.D
      
      # Otherwise, play whatever opponent played in the previous round
      return opponent.history[-1]



# ## Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 999:** Defect
# if your opponent defected on the previous round. If your opponent cooperated
# on the previous round, cooperate.  **Round 1000:** Defect.

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
      
      if len(self.history) == 999:
          return axl.Action.D
      
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          return axl.Action.C



# ## Strategy: Tit-for-Tat with Gradual Endgame Defection  **Opening move:**
# Cooperate on round 1.  **Rounds 2 through 995:** Mirror your opponent's
# previous move exactly, with one exception: if you defected in the previous
# round solely because your opponent defected, and your opponent has now
# returned to cooperation, return to cooperation immediately. If they defected
# last round, defect. If they cooperated last round, cooperate.  **Rounds 996
# through 1000:** Defect unconditionally. The window is short enough that a
# retaliating opponent cannot meaningfully punish you across enough rounds to
# outweigh the gains from defecting, since only four rounds of retaliation are
# possible after your first defection in round 996, and the payoff from mutual
# defection (1 per round) is only marginally worse than mutual cooperation (3
# per round) across such a small number of rounds, while a cooperative opponent
# yields 5 per round during this window.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 996:
          return axl.Action.D
      
      # Rounds 2 through 995: Tit-for-Tat
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 999:** If your opponent
# played C in the previous round, play C. If your opponent played D in the
# previous round, play D.  **Round 1000:** Play D.

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
      
      if len(self.history) == 999:
          return axl.Action.D
      
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D



# ## Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 1000:** Defect
# if any of the following conditions are met, checked in order:  1. There are 8
# rounds or fewer remaining. 2. Your opponent has defected more than once in the
# entire history of the game so far. 3. Your opponent defected in the previous
# round.  **Otherwise:** Cooperate.

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      total_rounds = 1000
      rounds_played = len(self.history)
      rounds_remaining = total_rounds - rounds_played
      
      # Condition 1: 8 rounds or fewer remaining
      if rounds_remaining <= 8:
          return axl.Action.D
      
      # Condition 2: Opponent has defected more than once in entire history
      if opponent.history.defections > 1:
          return axl.Action.D
      
      # Condition 3: Opponent defected in the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Gradual Tit-for-Tat with Forgiveness  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Apply the following conditions in
# order:  1. If the current round is one of every 10th round (rounds 10, 20, 30,
# and so on), cooperate unconditionally. This acts as a forgiveness mechanism to
# break out of prolonged mutual defection cycles and test whether the opponent
# is willing to return to cooperation.  2. If your opponent has defected in both
# of the previous two rounds, defect. This guards against persistent
# exploitative opponents while giving a single defection the benefit of the
# doubt.  3. Otherwise, mirror your opponent's previous move. If they cooperated
# last round, cooperate. If they defected last round, defect.  **Rounds 991
# through 1000:** Observe your opponent's behaviour over rounds 981 through 990.
# If they cooperated in at least eight of those ten rounds, continue cooperating
# through to round 1000, as mutual cooperation remains more valuable than
# triggering a retaliatory breakdown. If they cooperated in fewer than eight of
# those rounds, defect unconditionally for the remainder of the game, since the
# opponent has demonstrated insufficient reliability to make continued
# cooperation worthwhile.

class Cooperative_18(LLM_Strategy):
  n = 18
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Cooperate
      if self.first_round():
          return axl.Action.C
      
      current_round = len(self.history) + 1  # The round we're about to play
      
      # Rounds 991 through 1000: endgame logic
      if current_round >= 991:
          # Count opponent's cooperations in rounds 981-990 (indices 980-989)
          coop_count = opponent.history[980:990].count(axl.Action.C)
          if coop_count >= 8:
              return axl.Action.C
          else:
              return axl.Action.D
      
      # Rounds 2 through 990
      # Condition 1: Every 10th round (10, 20, 30, ...)
      if current_round % 10 == 0:
          return axl.Action.C
      
      # Condition 2: Opponent defected in both of the previous two rounds
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      # Condition 3: Mirror opponent's previous move
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 997:** Apply the following
# conditions in order:  - If the opponent has defected in more than 90% of all
# rounds played so far, play D. - If you defected in the previous round as a
# punishment and the opponent played C in that same round, play C. - If the
# opponent played D in the previous round, play D. - Otherwise, play C.
# **Rounds 998 to 1000:** Play D unconditionally.

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
      
      # Rounds 998 to 1000: Play D unconditionally
      if round_number >= 998:
          return axl.Action.D
      
      # Rounds 2 to 997
      total_rounds = len(opponent.history)
      
      # Condition 1: If opponent has defected in more than 90% of all rounds played so far
      if opponent.defections / total_rounds > 0.90:
          return axl.Action.D
      
      # Condition 2: If you defected in the previous round as a punishment and opponent played C in that same round
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # Condition 3: If the opponent played D in the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Otherwise, play C
      return axl.Action.C



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# your opponent defected on the previous round. Cooperate if your opponent
# cooperated on the previous round.  ---  This strategy, known as Tit-for-Tat
# initiated with defection, attempts to aggressively secure an early advantage
# by defecting on the first round, then mirrors the opponent's previous action
# for the remainder of the game. If the opponent responds to the opening
# defection by cooperating, continue to cooperate, locking in mutual cooperation
# payoffs of 3 per round for the bulk of the game. If the opponent retaliates
# with defection, match their defection to avoid being exploited, accepting the
# mutual defection payoff of 1 per round rather than the sucker payoff of 0.
# This balances aggression with responsiveness, exploiting cooperative opponents
# while protecting against retaliatory ones.

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
      return opponent.history[-1]



# ## Strategy: Tit-for-Tat with Forgiveness  **Opening move:** Cooperate on
# round 1.  **All subsequent rounds:** Apply the following conditions in order:
# 1. If the opponent has defected on both of the previous two rounds, defect. 2.
# Otherwise, cooperate.

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
      
      # Check if opponent has defected on both of the previous two rounds
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      return axl.Action.C



# ## Strategy  **Round 1:** Play D.  **Rounds 2 to 1000:** Apply the following
# conditions in order:  1. If it is one of the final 5 rounds, play D. 2. If the
# opponent has played D in at least 2 of the last 5 rounds, play D. 3. If the
# opponent played C in each of the last 2 rounds, play C. 4. Otherwise, play D.

class Neutral_19(LLM_Strategy):
  n = 19
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Play D
      if self.first_round():
          return axl.Action.D
      
      # Total rounds in the match
      total_rounds = 1000
      current_round = len(self.history) + 1  # The round we're about to play
      
      # Condition 1: If it is one of the final 5 rounds, play D
      if current_round >= total_rounds - 4:
          return axl.Action.D
      
      # Condition 2: If the opponent has played D in at least 2 of the last 5 rounds, play D
      last_5 = opponent.history[-5:]
      if last_5.count(axl.Action.D) >= 2:
          return axl.Action.D
      
      # Condition 3: If the opponent played C in each of the last 2 rounds, play C
      if len(opponent.history) >= 2:
          last_2 = opponent.history[-2:]
          if last_2.count(axl.Action.C) == 2:
              return axl.Action.C
      
      # Condition 4: Otherwise, play D
      return axl.Action.D



# ## Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 1000:** Apply
# the following conditions in order:  1. If the opponent has played D in the
# previous round, defect. 2. If the opponent has played C in the previous round,
# cooperate.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
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



# ## Strategy: Tit-for-Tat with Forgiveness  **Opening move:** Cooperate on
# round 1.  **Subsequent rounds:** Apply the following conditions in order:  1.
# If your opponent has cooperated in every single round so far, cooperate. 2. If
# your opponent defected last round but cooperated in the round before that,
# cooperate, giving them the benefit of the doubt for a possible one-off
# defection. 3. If your opponent has defected for two or more consecutive
# rounds, defect. 4. If your opponent has been defecting consistently for 10 or
# more consecutive rounds with no cooperation, defect for the remainder of the
# game, as they are unlikely to shift to a cooperative strategy. 5. Otherwise,
# cooperate.

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
      
      # Count consecutive defections by opponent
      consecutive_defections = 0
      for action in reversed(opponent.history):
          if action == axl.Action.D:
              consecutive_defections += 1
          else:
              break
      
      # Condition 1: Opponent has cooperated in every single round so far
      if opponent.history.defections == 0:
          return axl.Action.C
      
      # Condition 4: Opponent has been defecting for 10 or more consecutive rounds
      if consecutive_defections >= 10:
          return axl.Action.D
      
      # Condition 2: Opponent defected last round but cooperated the round before that
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
      
      # Condition 3: Opponent has defected for two or more consecutive rounds
      if consecutive_defections >= 2:
          return axl.Action.D
      
      # Condition 5: Otherwise, cooperate
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 990:** Play C if your
# opponent cooperated in the previous round. Play C also if your opponent
# defected in the previous round but cooperated in the round before that,
# treating the defection as a potential mistake and offering forgiveness.
# Otherwise, play D.  **Rounds 991 to 999:** Play D regardless of what your
# opponent does.  **Round 1000:** Play D regardless of what your opponent does.

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
      
      round_number = len(self.history) + 1
      
      # Rounds 991 to 1000: Play D
      if round_number >= 991:
          return axl.Action.D
      
      # Rounds 2 to 990
      # Play C if opponent cooperated in the previous round
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # Opponent defected in the previous round
      # Check if opponent cooperated in the round before that (forgiveness)
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
      
      # Otherwise, play D
      return axl.Action.D



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 990:** Apply the
# following conditions in order:  1. If the opponent has defected more than 60%
# of the time across all previous rounds, defect. 2. If the opponent defected in
# either of the two previous rounds, defect. 3. Otherwise, cooperate.  **Rounds
# 991 to 1000:** Defect unconditionally.

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
      
      round_number = len(self.history) + 1
      
      # Rounds 991 to 1000: defect unconditionally
      if round_number >= 991:
          return axl.Action.D
      
      # Rounds 2 to 990
      total_rounds = len(opponent.history)
      
      # Condition 1: opponent defected more than 60% of the time
      if total_rounds > 0:
          defection_rate = opponent.history.defections / total_rounds
          if defection_rate > 0.60:
              return axl.Action.D
      
      # Condition 2: opponent defected in either of the two previous rounds
      last_two = opponent.history[-2:]
      if axl.Action.D in last_two:
          return axl.Action.D
      
      # Otherwise cooperate
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **All subsequent rounds:** Play whatever
# your opponent played in the immediately preceding round.

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



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 990:** If your opponent has
# defected in at least two of the previous three rounds, play D. Otherwise, play
# C.  **Rounds 991 to 1000:** Play D unconditionally.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 991:
          return axl.Action.D
      
      # Rounds 2 to 990
      last_three = opponent.history[-3:]
      if last_three.count(axl.Action.D) >= 2:
          return axl.Action.D
      else:
          return axl.Action.C



# ## Aggressive Strategy  **Round 1:** Cooperate.  **All subsequent rounds:**
# Defect if any of the following conditions are met, checked in this order:  1.
# There are 10 or fewer rounds remaining. 2. Your opponent has defected on both
# of the previous two rounds.  **Otherwise:** Cooperate.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      total_rounds = 1000
      rounds_played = len(self.history)
      rounds_remaining = total_rounds - rounds_played
      
      # Condition 1: 10 or fewer rounds remaining
      if rounds_remaining <= 10:
          return axl.Action.D
      
      # Condition 2: Opponent defected on both of the previous two rounds
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Cooperative Tit-for-Tat with Forgiveness  **Opening move:**
# Cooperate on round 1.  **From round 2 onwards, apply the following conditions
# in order:**  1. If your opponent has defected on more than 90% of all rounds
# played so far, defect for the remainder of the game.  2. If your opponent
# defected on the previous round but cooperated on the round before that,
# cooperate, giving them the benefit of the doubt for a possible accidental
# defection.  3. If your opponent has defected on each of the previous 3
# consecutive rounds, defect until they cooperate, then immediately return to
# cooperation on the following round.  4. If your opponent defected on the
# previous round in any other circumstance not covered above, defect on this
# round only, then return to cooperation on the following round regardless of
# outcome.  5. Otherwise, cooperate.

class Cooperative_22(LLM_Strategy):
  n = 22
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Opening move: Cooperate on round 1
      if self.first_round():
          return axl.Action.C
      
      rounds_played = len(self.history)
      
      # Condition 1: If opponent has defected on more than 90% of all rounds played so far, defect
      if opponent.history.defections / rounds_played > 0.90:
          return axl.Action.D
      
      # Condition 2: If opponent defected on previous round but cooperated on round before that, cooperate
      if rounds_played >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
      
      # Condition 3: If opponent has defected on each of the previous 3 consecutive rounds, defect until they cooperate
      if rounds_played >= 3:
          if (opponent.history[-1] == axl.Action.D and 
              opponent.history[-2] == axl.Action.D and 
              opponent.history[-3] == axl.Action.D):
              # Defect until they cooperate - since last move was D, we defect
              return axl.Action.D
      
      # Condition 4: If opponent defected on previous round in any other circumstance, defect on this round only
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 5: Otherwise, cooperate
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 990:** Play C if your
# opponent cooperated in the previous round. Play D if your opponent defected in
# the previous round. However, if both you and your opponent have been playing D
# for three or more consecutive rounds, play C to attempt to restore mutual
# cooperation.  **Rounds 991 to 1000:** Play D unconditionally.

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
      
      # Rounds 991 to 1000: defect unconditionally
      if round_number >= 991:
          return axl.Action.D
      
      # Rounds 2 to 990
      # Check if both have been playing D for 3 or more consecutive rounds
      if len(self.history) >= 3:
          my_last_3 = self.history[-3:]
          opp_last_3 = opponent.history[-3:]
          if (my_last_3.count(axl.Action.D) == 3 and 
                  opp_last_3.count(axl.Action.D) == 3):
              return axl.Action.C
      
      # Tit for tat: mirror opponent's last move
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D



# ## Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 997:** Apply
# the following conditions in order:  - If the previous round resulted in mutual
# defection, cooperate in order to attempt to restore mutual cooperation. - If
# your opponent defected on the previous round and you cooperated, defect. - If
# your opponent cooperated on the previous round, cooperate.  **Rounds 998 to
# 1000:** Defect unconditionally.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      round_number = len(self.history) + 1
      
      if round_number >= 998:
          return axl.Action.D
      
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
      
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
      
      if opp_last == axl.Action.D and my_last == axl.Action.C:
          return axl.Action.D
      
      if opp_last == axl.Action.C:
          return axl.Action.C
      
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Forgiveness and Single Late Defection  **Opening
# move:** Cooperate on round 1.  **Rounds 2 through 999:** Apply the following
# conditions in order:  1. If it is round 999, defect. 2. If the opponent has
# defected in each of the last five consecutive rounds, cooperate as a signal to
# attempt to re-establish mutual cooperation. 3. If the opponent defected last
# round, defect. 4. Otherwise, cooperate.  **Round 1000:** Defect
# unconditionally.

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
      
      round_number = len(self.history) + 1
      
      # Round 1000: defect unconditionally
      if round_number == 1000:
          return axl.Action.D
      
      # Round 999: defect
      if round_number == 999:
          return axl.Action.D
      
      # Check if opponent has defected in each of the last 5 consecutive rounds
      if len(opponent.history) >= 5 and opponent.history[-5:].count(axl.Action.D) == 5:
          return axl.Action.C
      
      # If opponent defected last round, defect
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Otherwise, cooperate
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 990:** Apply the following
# conditions in order:  1. If the opponent has played D in at least 2 of the
# last 5 rounds, play D. 2. If the opponent played C in the previous round, play
# C. 3. Otherwise, play D.  **Rounds 991 to 1000:** Play D.

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
      
      round_number = len(self.history) + 1
      
      # Rounds 991 to 1000: Play D
      if round_number >= 991:
          return axl.Action.D
      
      # Rounds 2 to 990
      # Condition 1: If opponent has played D in at least 2 of the last 5 rounds, play D
      last_5 = opponent.history[-5:]
      if last_5.count(axl.Action.D) >= 2:
          return axl.Action.D
      
      # Condition 2: If opponent played C in the previous round, play C
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # Condition 3: Otherwise, play D
      return axl.Action.D



# # Aggressive Tit-for-Tat Strategy  **Round 1:** Defect.  **Rounds 2 to 990:**
# If your opponent cooperated on the previous round, cooperate. If your opponent
# defected on the previous round, defect.  **Rounds 991 to 1000:** Defect
# unconditionally regardless of your opponent's prior behaviour.  ---  The
# opening defect attempts to exploit a cooperative opponent immediately. From
# round 2 onward, the strategy mirrors the opponent's previous action. This
# punishes defection immediately and rewards cooperation with cooperation,
# steering a responsive opponent toward the mutually beneficial outcome of 3
# points per round while continuing to exploit any opponent who persists in
# cooperating despite being defected against. Against an opponent who
# retaliates, mirroring their defection avoids being repeatedly exploited and
# creates an incentive for them to return to cooperation. In the final ten
# rounds, the strategy defects unconditionally to capture additional payoff at
# the end of the game, where the absence of future rounds removes the threat of
# retaliation making defection the dominant choice regardless of the opponent's
# behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 991:
          return axl.Action.D
      
      # Rounds 2 to 990: mirror opponent's last action
      return opponent.history[-1]



# ## Strategy: Tit-for-Tat with Adaptive Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 onwards, apply the following conditions in order:**
# 1. **If it is round 991 or later, defect.** The remaining rounds are too few
# for cooperative reciprocity to recover any losses from being exploited, so
# defection becomes the dominant choice regardless of opponent behaviour.  2.
# **If your opponent has defected in 8 or more of the last 10 rounds, defect.**
# This opponent has demonstrated a persistent unwillingness to cooperate and
# continued cooperation against them is too costly. Remain in defection against
# them for the rest of the game.  3. **If your opponent defected in the previous
# round but cooperated in the round before that, cooperate.** Extend a single
# act of forgiveness to account for the possibility of an accidental or mistaken
# defection, and to offer a path back to mutual cooperation.  4. **If your
# opponent defected in the previous round and also defected in the round before
# that, defect.** Two consecutive defections indicate deliberate rather than
# accidental behaviour and forgiveness is no longer warranted.  5. **In all
# other cases, cooperate.**

class Cooperative_24(LLM_Strategy):
  n = 24
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Opening move: Cooperate on round 1
      if self.first_round():
          return axl.Action.C
      
      round_number = len(self.history) + 1  # Current round number (about to play)
      
      # Condition 1: Round 991 or later, defect
      if round_number >= 991:
          return axl.Action.D
      
      # Condition 2: Opponent defected in 8 or more of the last 10 rounds
      if len(opponent.history) >= 10:
          last_10_defections = opponent.history[-10:].count(axl.Action.D)
          if last_10_defections >= 8:
              return axl.Action.D
      
      # Need at least 2 rounds of history for conditions 3 and 4
      if len(opponent.history) >= 2:
          prev_round = opponent.history[-1]
          two_rounds_ago = opponent.history[-2]
          
          # Condition 3: Opponent defected last round but cooperated the round before
          if prev_round == axl.Action.D and two_rounds_ago == axl.Action.C:
              return axl.Action.C
          
          # Condition 4: Opponent defected in both last round and the round before
          if prev_round == axl.Action.D and two_rounds_ago == axl.Action.D:
              return axl.Action.D
      elif len(opponent.history) == 1:
          # Only one round of history, check if opponent defected last round
          if opponent.history[-1] == axl.Action.D:
              # Can't check two rounds ago, treat as condition 5 (cooperate)
              # Actually, with only 1 round of history, conditions 3 and 4 don't apply
              pass
      
      # Condition 5: All other cases, cooperate
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 999:**  - If your opponent
# has defected in more than 90% of all rounds played so far, play D. -
# Otherwise, play whatever your opponent played in the previous round.  **Round
# 1000:** Play D.

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
      
      round_number = len(self.history) + 1
      
      if round_number == 1000:
          return axl.Action.D
      
      # Rounds 2 to 999
      total_rounds = len(opponent.history)
      defection_rate = opponent.history.defections / total_rounds
      
      if defection_rate > 0.90:
          return axl.Action.D
      else:
          return opponent.history[-1]



# ## Aggressive Strategy  **Round 1:** Cooperate.  **All subsequent rounds:**
# Defect if your opponent defected on the previous round. Cooperate if your
# opponent cooperated on the previous round.  **Final 5 rounds (rounds
# 996–1000):** Cooperate only if your opponent has cooperated in every one of
# the preceding 10 rounds without exception. Otherwise defect unconditionally.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      round_number = len(self.history) + 1
      
      # Final 5 rounds: rounds 996-1000
      if round_number >= 996:
          # Cooperate only if opponent cooperated in every one of the preceding 10 rounds
          if len(opponent.history) >= 10:
              last_10 = opponent.history[-10:]
              if last_10.count(axl.Action.D) == 0:
                  return axl.Action.C
              else:
                  return axl.Action.D
          else:
              # If fewer than 10 rounds have been played, check all available history
              if opponent.history.defections == 0:
                  return axl.Action.C
              else:
                  return axl.Action.D
      
      # All subsequent rounds (not final 5): mirror opponent's last move
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          return axl.Action.C



# ## Strategy: Tit-for-Tat with Forgiveness  **Opening move:** Cooperate on
# round 1.  **For all subsequent rounds, apply the following conditions in
# order:**  1. If the opponent has defected on both of the previous two rounds,
# defect. 2. If the opponent cooperated on the previous round, cooperate. 3.
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
      
      # Condition 1: If opponent defected on both of the previous two rounds, defect
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      # Condition 2: If opponent cooperated on the previous round, cooperate
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # Condition 3: Otherwise, cooperate
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 999:**  - If your opponent
# has defected in three or more of the last five rounds, play D. - If you and
# your opponent both played D in the previous round, play C. - Otherwise, play
# whatever your opponent played in the previous round.  **Round 1000:** Play D.

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
      
      round_number = len(self.history) + 1
      
      if round_number == 1000:
          return axl.Action.D
      
      # Check if opponent defected in 3 or more of the last 5 rounds
      last_5 = opponent.history[-5:]
      if last_5.count(axl.Action.D) >= 3:
          return axl.Action.D
      
      # If both played D in the previous round, play C
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
      
      # Otherwise, play whatever opponent played in the previous round
      return opponent.history[-1]