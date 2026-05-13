import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# ## Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 1000:** Defect
# if any of the following conditions are met, checked in order:  1. The current
# round is 995 or later. 2. Your opponent defected on the previous round.
# Otherwise, cooperate.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      current_round = len(self.history) + 1
      
      if current_round >= 995:
          return axl.Action.D
      
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Forgiveness and Late-Game Defection  **Opening
# move:** Cooperate on round 1.  **Rounds 2 through 995:** Apply the following
# conditions in order:  1. If the opponent has defected in response to your
# cooperation on both of the two most recent such occasions, defect for the
# remainder of the round window, treating them as an unconditional defector. 2.
# If the opponent defected last round but cooperated the round before that,
# cooperate this round as a single act of forgiveness, allowing the relationship
# to reset. 3. If the opponent defected last round and you also defected last
# round, cooperate this round to attempt to restore mutual cooperation. 4. If
# the opponent cooperated last round, cooperate this round. 5. Otherwise,
# defect.  **Rounds 996 through 1000:** Defect unconditionally. This window is
# short enough to limit the damage from any retaliatory defection triggered in
# the opponent's mirroring logic, while still capturing the end-game advantage
# against cooperative opponents.

class Cooperative_1(LLM_Strategy):
  n = 1
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self._unconditional_defector = False
          self._coop_then_defect_count = 0
          self._last_coop_response = None  # Track opponent's response to our cooperation
          return axl.Action.C
      
      round_number = len(self.history) + 1  # Next round number (1-indexed)
      current_round = len(self.history)  # Current round index (0-indexed), i.e., rounds played so far
      
      # Rounds 996-1000: defect unconditionally
      # current_round is the number of rounds played, so next round is current_round + 1
      # After round 995 is played (current_round == 995), next round is 996
      if current_round >= 995:
          return axl.Action.D
      
      # Check if we should treat opponent as unconditional defector
      # We need to track occasions where we cooperated and opponent defected
      # Look through history for our cooperation moves and opponent's responses
      
      # Update tracking of "cooperated then opponent defected" occasions
      # Check the most recent round (just played)
      if len(self.history) >= 1:
          my_last = self.history[-1]
          opp_last = opponent.history[-1]
          
          if my_last == axl.Action.C and opp_last == axl.Action.D:
              # We cooperated and opponent defected
              # Check if this is a new occasion (not already counted)
              # We track this via _last_coop_response
              if self._last_coop_response != len(self.history) - 1:
                  self._last_coop_response = len(self.history) - 1
                  self._coop_then_defect_count += 1
          elif my_last == axl.Action.C and opp_last == axl.Action.C:
              # Reset count when cooperation is reciprocated? 
              # The strategy says "two most recent such occasions" - we track consecutive betrayals
              # Actually re-reading: "defected in response to your cooperation on both of the two most recent such occasions"
              # This means the last two times we cooperated, they defected both times
              pass
      
      # Let me reconsider the tracking approach
      # Find all occasions where we cooperated, and check opponent's response
      # Check the last two such occasions
      
      coop_occasions = []
      for i in range(len(self.history)):
          if self.history[i] == axl.Action.C:
              coop_occasions.append(opponent.history[i])
      
      # Check if opponent defected on both of the two most recent cooperation occasions
      if len(coop_occasions) >= 2:
          if coop_occasions[-1] == axl.Action.D and coop_occasions[-2] == axl.Action.D:
              self._unconditional_defector = True
      
      # Condition 1: If marked as unconditional defector, defect
      if self._unconditional_defector:
          return axl.Action.D
      
      # Get last round's actions
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
      
      # Get second to last round's actions (if available)
      if len(self.history) >= 2:
          my_second_last = self.history[-2]
          opp_second_last = opponent.history[-2]
      else:
          my_second_last = None
          opp_second_last = None
      
      # Condition 2: If opponent defected last round but cooperated the round before that, cooperate (forgiveness)
      if opp_last == axl.Action.D and opp_second_last == axl.Action.C:
          return axl.Action.C
      
      # Condition 3: If opponent defected last round and we also def



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 5:** Apply the following
# conditions in order:  1. If the opponent played C in the previous round, play
# C. 2. Play D.  **Rounds 6 to 995:** Apply the following conditions in order:
# 1. If the opponent has played D in at least 3 of the last 5 rounds, play D. 2.
# If the opponent played C in the previous round, play C. 3. Play D.  **Rounds
# 996 to 1000:** Play D.

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
      
      round_number = len(self.history) + 1
      
      # Rounds 996 to 1000: Play D
      if round_number >= 996:
          return axl.Action.D
      
      # Rounds 2 to 5
      if round_number <= 5:
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          return axl.Action.D
      
      # Rounds 6 to 995
      # Condition 1: If opponent has played D in at least 3 of the last 5 rounds
      if opponent.history[-5:].count(axl.Action.D) >= 3:
          return axl.Action.D
      # Condition 2: If opponent played C in the previous round
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      # Condition 3: Play D
      return axl.Action.D



# ## Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 997:** Defect
# if either of the following conditions are met, checked in order:  1. The
# opponent defected on the previous round. 2. The opponent has defected on more
# than 10% of all rounds played so far.  Otherwise, cooperate.  **Rounds 998 to
# 1000:** Defect unconditionally.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      round_number = len(self.history) + 1
      
      if round_number >= 998:
          return axl.Action.D
      
      # Rounds 2 to 997
      # Condition 1: opponent defected on previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 2: opponent has defected on more than 10% of all rounds played so far
      rounds_played = len(opponent.history)
      if rounds_played > 0 and opponent.history.defections / rounds_played > 0.10:
          return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Forgiveness  **Opening move:** Cooperate on
# round 1.  **From round 2 onwards, apply the following conditions in order:**
# 1. If your opponent has defected on both of the previous two rounds, defect.
# 2. If your opponent cooperated on the previous round, cooperate.  3. If your
# opponent defected on the previous round but cooperated on the round before
# that, cooperate.

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
      
      # From round 2 onwards
      if len(opponent.history) >= 2:
          # Condition 1: If opponent defected on both of the previous two rounds, defect
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      # Condition 2: If opponent cooperated on the previous round, cooperate
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # Condition 3: If opponent defected on the previous round but cooperated on the round before that, cooperate
      if opponent.history[-1] == axl.Action.D:
          if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
      
      # Default (shouldn't reach here given the conditions cover all cases)
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 999:**  - If your opponent
# has defected in every single round played so far, play D. - If your opponent
# played D in the previous round and the round before that, play D. - Otherwise,
# play C.  **Round 1000:** Play D.

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
      
      round_number = len(self.history) + 1
      
      if round_number == 1000:
          return axl.Action.D
      
      # Check if opponent has defected in every single round so far
      if opponent.history.defections == len(opponent.history):
          return axl.Action.D
      
      # Check if opponent played D in the previous round and the round before that
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      return axl.Action.C



# ## Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 1000:** Defect
# if any of the following conditions are met, evaluated in order:  1. It is
# round 990 or later. 2. The opponent has defected in more than 30% of all
# rounds played so far. 3. The opponent defected on each of the two most recent
# rounds.  Otherwise, cooperate.

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
      
      round_number = len(self.history) + 1
      
      # Condition 1: Round 990 or later
      if round_number >= 990:
          return axl.Action.D
      
      # Condition 2: Opponent defected in more than 30% of all rounds played so far
      rounds_played = len(opponent.history)
      if rounds_played > 0:
          defection_rate = opponent.history.defections / rounds_played
          if defection_rate > 0.30:
              return axl.Action.D
      
      # Condition 3: Opponent defected on each of the two most recent rounds
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Forgiveness  **Opening move:** Cooperate on
# round 1.  **Every subsequent round:** Apply the following conditions in order:
# 1. If your opponent has defected on every single round played so far, defect.
# 2. If your opponent defected last round but cooperated at least once
# previously, cooperate. This forgiveness prevents a single defection from
# triggering a prolonged cycle of mutual defection.  3. If your opponent
# cooperated last round, cooperate.  4. If your opponent defected last round and
# has been defecting consistently for the last 5 consecutive rounds, defect.
# This guards against an opponent who has shifted to a permanently aggressive
# strategy, preventing continued exploitation.

class Cooperative_3(LLM_Strategy):
  n = 3
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Opening move: Cooperate on round 1
      if self.first_round():
          return axl.Action.C
      
      # Check if opponent has defected on every single round played so far
      if opponent.history.defections == len(opponent.history):
          return axl.Action.D
      
      # Check what opponent did last round
      last_opponent_action = opponent.history[-1]
      
      # If opponent defected last round
      if last_opponent_action == axl.Action.D:
          # Check if opponent has been defecting consistently for the last 5 consecutive rounds
          if len(opponent.history) >= 5 and opponent.history[-5:].count(axl.Action.D) == 5:
              return axl.Action.D
          
          # If opponent cooperated at least once previously, forgive (cooperate)
          if opponent.history.cooperations > 0:
              return axl.Action.C
      
      # If opponent cooperated last round, cooperate
      if last_opponent_action == axl.Action.C:
          return axl.Action.C
      
      # Default (shouldn't reach here given the conditions above)
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 4:** If the opponent played D
# in the previous round, play D. Otherwise, play C.  **Rounds 5 to 990:** Apply
# the following conditions in order:  1. If the opponent has played D in at
# least 3 of the last 5 rounds, play D. 2. If the opponent played D in the
# previous round, play D. 3. Otherwise, play C.  **Rounds 991 to 1000:** Apply
# the following conditions in order:  1. If the opponent has played D in at
# least 3 of the last 5 rounds, play D. 2. If the opponent played D in either of
# the previous 2 rounds, play D. 3. Otherwise, play C.

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
      
      round_number = len(self.history) + 1  # current round being played
      
      # Rounds 2 to 4
      if round_number <= 4:
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.D
          else:
              return axl.Action.C
      
      # Rounds 5 to 990
      if round_number <= 990:
          # Condition 1: opponent played D in at least 3 of last 5 rounds
          if len(opponent.history) >= 5:
              last_5_defections = opponent.history[-5:].count(axl.Action.D)
          else:
              last_5_defections = opponent.history.defections
          
          if last_5_defections >= 3:
              return axl.Action.D
          
          # Condition 2: opponent played D in previous round
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.D
          
          return axl.Action.C
      
      # Rounds 991 to 1000
      # Condition 1: opponent played D in at least 3 of last 5 rounds
      if len(opponent.history) >= 5:
          last_5_defections = opponent.history[-5:].count(axl.Action.D)
      else:
          last_5_defections = opponent.history.defections
      
      if last_5_defections >= 3:
          return axl.Action.D
      
      # Condition 2: opponent played D in either of the previous 2 rounds
      if len(opponent.history) >= 2:
          last_2_defections = opponent.history[-2:].count(axl.Action.D)
      else:
          last_2_defections = opponent.history[-1:].count(axl.Action.D)
      
      if last_2_defections >= 1:
          return axl.Action.D
      
      return axl.Action.C



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# any of the following conditions are met, checked in this order:  1. It is
# round 1000. 2. Your opponent has defected on more than half of all rounds
# played so far. 3. Your opponent defected on the previous round.
# **Otherwise:** Cooperate.  ---  This strategy opens aggressively to probe the
# opponent. Against a retaliatory opponent, condition 3 will trigger defection,
# but if the opponent returns to cooperation the strategy will also return to
# cooperation, allowing recovery from early conflict. Against a persistently
# uncooperative opponent, condition 2 ensures the strategy abandons cooperation
# entirely rather than remaining vulnerable to exploitation. Condition 1 secures
# a defection on the final round only, avoiding the risk of triggering
# unnecessary retaliation in the rounds immediately preceding it.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Defect
      if self.first_round():
          return axl.Action.D
      
      # Rounds 2 to 1000
      current_round = len(self.history) + 1  # This will be the round number after this move
      # Actually, len(self.history) is the number of rounds played so far
      # So current round number is len(self.history) + 1
      round_number = len(self.history) + 1
      
      # Condition 1: It is round 1000
      if round_number == 1000:
          return axl.Action.D
      
      # Condition 2: Opponent has defected on more than half of all rounds played so far
      rounds_played = len(opponent.history)
      if rounds_played > 0 and opponent.history.defections > rounds_played / 2:
          return axl.Action.D
      
      # Condition 3: Opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Otherwise: Cooperate
      return axl.Action.C



# ## Strategy: Adaptive Tit-for-Tat with Forgiveness  **Opening move:**
# Cooperate on round 1.  **Rounds 2 through 1000:** Apply the following
# conditions in order:  1. If your opponent has defected in at least 60% of all
# rounds played so far, defect.  2. If your opponent defected in the previous
# round but cooperated in the round before that, cooperate, treating the
# defection as a possible mistake and giving them one opportunity to return to
# cooperation.  3. If your opponent defected in both of the previous two rounds,
# defect.  4. Otherwise, cooperate.

class Cooperative_4(LLM_Strategy):
  n = 4
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Opening move: Cooperate on round 1
      if self.first_round():
          return axl.Action.C
      
      # Condition 1: If opponent has defected in at least 60% of all rounds played so far, defect
      total_rounds = len(opponent.history)
      if total_rounds > 0:
          defection_rate = opponent.history.defections / total_rounds
          if defection_rate >= 0.6:
              return axl.Action.D
      
      # Condition 2: If opponent defected in previous round but cooperated in round before that,
      # cooperate (treating defection as possible mistake)
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
      
      # Condition 3: If opponent defected in both of the previous two rounds, defect
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      # Condition 4: Otherwise, cooperate
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 990:** Apply the following
# conditions in order:  - If your opponent has defected in more than 90% of all
# rounds played so far, play D. - If your opponent defected in the previous
# round but cooperated in the round before that, play C. - If your opponent
# defected in the previous two or more consecutive rounds, play D. - Otherwise,
# play C.  **Rounds 991 to 1000:** Apply the following conditions in order:  -
# If your opponent has defected in more than 90% of all rounds played so far,
# play D. - If your opponent defected in the previous round but cooperated in
# the round before that, play C. - If your opponent defected in the previous two
# or more consecutive rounds, play D. - Otherwise, play D.

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
      
      round_number = len(self.history) + 1  # This will be the round we're deciding for
      
      # Determine if we're in endgame (rounds 991-1000)
      # len(self.history) is the number of rounds played so far
      # We're deciding for round len(self.history) + 1
      current_round = len(self.history) + 1
      endgame = current_round >= 991
      
      # Calculate opponent defection rate
      total_rounds = len(opponent.history)
      opp_defections = opponent.history.defections
      defection_rate = opp_defections / total_rounds if total_rounds > 0 else 0
      
      # Condition 1: opponent defected in more than 90% of rounds
      if defection_rate > 0.9:
          return axl.Action.D
      
      # Condition 2: opponent defected in previous round but cooperated in round before that
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
      
      # Condition 3: opponent defected in previous two or more consecutive rounds
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      # Otherwise
      if endgame:
          return axl.Action.D
      else:
          return axl.Action.C



# ## Aggressive Strategy  **Round 1:** Cooperate.  **Rounds 2 to 995:** Defect
# if any of the following conditions are met, checked in order:  1. Your
# opponent has defected on more than 15% of all rounds played so far. 2. Your
# opponent defected on each of the previous 2 consecutive rounds.  Otherwise,
# cooperate.  **Rounds 996 to 1000:** Defect unconditionally.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      round_number = len(self.history) + 1
      
      # Rounds 996 to 1000: defect unconditionally
      if round_number >= 996:
          return axl.Action.D
      
      # Rounds 2 to 995
      rounds_played = len(self.history)
      
      # Condition 1: opponent defected on more than 15% of all rounds played so far
      opponent_defections = opponent.history.defections
      if opponent_defections / rounds_played > 0.15:
          return axl.Action.D
      
      # Condition 2: opponent defected on each of the previous 2 consecutive rounds
      if rounds_played >= 2 and opponent.history[-2:].count(axl.Action.D) == 2:
          return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Cooperative Tit-for-Tat with Forgiveness  **Opening move:**
# Cooperate on round 1.  **From round 2 onwards, apply the following conditions
# in order:**  1. **If the opponent has defected in at least 8 of the last 10
# rounds**, defect. They have demonstrated a persistent unwillingness to
# cooperate and continued cooperation against them is too costly.  2. **If the
# opponent defected last round but cooperated in the majority of the 10 rounds
# before that**, cooperate. Treat the defection as likely accidental or
# exploratory and attempt to preserve the cooperative relationship.  3. **If the
# opponent defected last round and no forgiveness condition above applies**,
# defect.  4. **Otherwise, cooperate.**

class Cooperative_5(LLM_Strategy):
  n = 5
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Opening move: Cooperate on round 1
      if self.first_round():
          return axl.Action.C
      
      # Get the last 10 rounds of opponent's history
      last_10 = opponent.history[-10:]
      defections_in_last_10 = last_10.count(axl.Action.D)
      
      # Condition 1: If opponent defected in at least 8 of the last 10 rounds, defect
      if len(last_10) >= 10 and defections_in_last_10 >= 8:
          return axl.Action.D
      # If we have fewer than 10 rounds, still check if they defected >= 8 times
      elif len(last_10) < 10 and defections_in_last_10 >= 8:
          return axl.Action.D
      
      # Check if opponent defected last round
      opponent_defected_last = opponent.history[-1] == axl.Action.D
      
      if opponent_defected_last:
          # Condition 2: If opponent defected last round but cooperated in majority of 10 rounds before that
          # Get the 10 rounds before the last round
          rounds_before_last = opponent.history[-11:-1]
          if len(rounds_before_last) > 0:
              cooperations_before = rounds_before_last.count(axl.Action.C)
              if cooperations_before > len(rounds_before_last) / 2:
                  return axl.Action.C
          
          # Condition 3: Opponent defected last round and no forgiveness condition applies
          return axl.Action.D
      
      # Condition 4: Otherwise, cooperate
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 990:** If your opponent has
# played C in every round so far, play D once every 10 rounds, otherwise play
# whatever your opponent played in the previous round.  **Rounds 991 to 1000:**
# Play D.

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
      
      round_number = len(self.history) + 1  # current round number (1-indexed)
      
      # Rounds 991 to 1000: Play D
      if round_number >= 991:
          return axl.Action.D
      
      # Rounds 2 to 990
      # Check if opponent has played C in every round so far
      if opponent.history.defections == 0:
          # Opponent has always cooperated
          # Play D once every 10 rounds (i.e., on rounds 10, 20, 30, ...)
          if round_number % 10 == 0:
              return axl.Action.D
          else:
              return axl.Action.C
      else:
          # Play whatever opponent played in the previous round
          return opponent.history[-1]