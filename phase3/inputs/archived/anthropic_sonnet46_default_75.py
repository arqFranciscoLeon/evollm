import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# ## Aggressive Tit-for-Tat Strategy  **Round 1:** Defect.  **Rounds 2 through
# 990:** If your opponent cooperated on the previous round, defect. If your
# opponent defected on the previous round, defect.  In other words, always
# defect during this phase regardless of what the opponent does.  **Rounds 991
# through 1000:** Defect unconditionally.  ---  **Rationale in brief:** The
# payoff structure makes defection the dominant move in any single round — it
# always yields more than cooperation regardless of the opponent's choice (5 vs
# 3 when they cooperate, 1 vs 0 when they defect). Since sustained mutual
# defection yields 1 per round and mutual cooperation yields 3, a cooperative
# arrangement would theoretically be preferable, but achieving and maintaining
# it requires the opponent to resist exploiting your cooperation. Given the
# aggressive stance prioritised here, unconditional defection throughout all
# 1000 rounds captures the dominant-strategy payoff in every interaction, avoids
# ever scoring 0 from being exploited, and requires no trust or signalling to
# maintain.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Mirror your opponent's most recent move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 991 through 1000:** Defect unconditionally,
# regardless of the opponent's behaviour.

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
      
      current_round = len(self.history) + 1
      
      if current_round >= 991:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  On the first round, play C.  On each subsequent round, play
# whatever your opponent played in the previous round.

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



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# any of the following conditions are met, checked in this order:  1. Your
# opponent defected on the previous round. 2. It is one of the final 5 rounds
# (rounds 996 to 1000). 3. Your cumulative score exceeds your opponent's
# cumulative score by more than 10 points.  **Otherwise:** Cooperate.  ---
# **Rationale summary:**  The strategy opens with defection to probe the
# opponent and avoid being exploited immediately. It then retaliates
# unconditionally after any defection, discouraging exploitation. It locks in
# defection during the endgame to capture final-round gains without fear of
# retaliation. When already ahead by a meaningful margin, it defects to press
# the advantage. In all remaining situations, it cooperates to establish and
# sustain a mutually beneficial pattern worth 3 points each round, which is
# preferable to the mutual defection outcome of 1 point each round.

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
      
      # Condition 1: Opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 2: One of the final 5 rounds (rounds 996 to 1000)
      current_round = len(self.history) + 1  # This will be the round number after this move
      # We're deciding for round len(self.history) + 1
      round_number = len(self.history) + 1
      if round_number >= 996:
          return axl.Action.D
      
      # Condition 3: Cumulative score exceeds opponent's by more than 10
      if self.score - opponent.score > 10:
          return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Mirror your opponent's previous move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 991 through 1000:** Defect unconditionally,
# regardless of the opponent's recent behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 991:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 1000:** Play whichever action
# your opponent played in the previous round.

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



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# any of the following conditions are met, evaluated in order:  1. Your opponent
# defected on the previous round. 2. It is round 980 or later.  **Otherwise:**
# Cooperate.  ---  This strategy opens with defection to probe the opponent and
# avoid early exploitation. It then attempts to establish mutual cooperation
# with any opponent who responds to defection by cooperating, rewarding them
# with cooperation in return. However, it immediately punishes any defection
# with a retaliatory defect on the following round, returning to cooperation
# only if the opponent returns to cooperation first. In the final 21 rounds, it
# abandons cooperation entirely to harvest defection payoffs before the game
# ends, preventing the opponent from exploiting a predictable cooperative
# endgame.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      
      current_round = len(self.history) + 1
      
      # Condition 1: Opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 2: Round 980 or later
      if current_round >= 980:
          return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Mirror your opponent's previous move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 991 through 1000:** Defect unconditionally,
# regardless of the opponent's history or recent moves.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 991:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 1000:** Apply the following
# conditions in order:  1. If your opponent has played D in at least 60% of all
# previous rounds, play D for the remainder of the game. 2. If the current round
# is 998 or later, play D. 3. If your opponent played D in the previous round,
# play D. 4. Otherwise, play C.

class Neutral_3(LLM_Strategy):
  n = 3
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.permanent_defect = False
          return axl.Action.C
      
      # Check if we should permanently defect
      if not self.permanent_defect:
          total_rounds = len(opponent.history)
          if total_rounds > 0 and opponent.history.defections / total_rounds >= 0.6:
              self.permanent_defect = True
      
      # Condition 1: permanent defect
      if self.permanent_defect:
          return axl.Action.D
      
      # Condition 2: round 998 or later (rounds are 1-indexed, history length gives current round - 1)
      current_round = len(self.history) + 1
      if current_round >= 998:
          return axl.Action.D
      
      # Condition 3: opponent played D in previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Otherwise cooperate
      return axl.Action.C



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# any of the following conditions are met, checked in this order:  1. Your
# opponent defected on the previous round. 2. It is round 990 or later.
# Otherwise, cooperate.

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
      
      current_round = len(self.history) + 1
      
      # Condition 1: Opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 2: Round 990 or later
      if current_round >= 990:
          return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Mirror your opponent's previous move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 991 through 1000:** Defect unconditionally,
# regardless of your opponent's behaviour.

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
      
      if round_number >= 991:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **All subsequent rounds:** Play whatever
# your opponent played in the previous round.

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



# ## Aggressive Strategy  **Round 1:** Defect.  **All subsequent rounds:**
# Defect if your opponent defected on the previous round. Cooperate if your
# opponent cooperated on the previous round.  **Final 5 rounds (rounds
# 996–1000):** Defect unconditionally, regardless of your opponent's recent
# behaviour.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # First round: Defect
      if self.first_round():
          return axl.Action.D
      
      # Final 5 rounds (rounds 996-1000, i.e., when len(history) >= 995): Defect
      if len(self.history) >= 995:
          return axl.Action.D
      
      # All subsequent rounds: mirror opponent's last move
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          return axl.Action.C



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Mirror your opponent's previous move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 991 through 1000:** Defect unconditionally,
# regardless of your opponent's recent behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 991:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **All subsequent rounds:** Play whatever
# your opponent played in the previous round.

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



# # Aggressive Tit-for-Tat Strategy  **Round 1:** Defect.  **Rounds 2 through
# 990:** If your opponent cooperated on the previous round, defect. If your
# opponent defected on the previous round, defect.  That is, defect
# unconditionally throughout this phase.  **Rounds 991 through 1000:** Defect
# unconditionally.  ---  In plain terms: always defect for the entire game.  The
# reasoning is as follows. The temptation payoff of 5 exceeds mutual cooperation
# at 3, and mutual defection at 1 still exceeds being exploited at 0. Given that
# an opponent playing cooperatively can be continuously exploited for a payoff
# of 5 per round rather than 3, and that a retaliating opponent locks both
# players into mutual defection at 1 rather than the worst outcome of 0,
# defection is the dominant action in every round regardless of what the
# opponent does. With 1000 rounds and end-game defection being rational even in
# cooperative strategies, consistent defection maximises expected payoff across
# all opponent types by either exploiting cooperators fully or matching
# defectors rather than being caught cooperating against them.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 995:** Mirror your opponent's previous move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 996 through 1000:** Defect unconditionally,
# regardless of the opponent's recent behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 996:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 999:** Play whatever your
# opponent played in the previous round.  **Round 1000:** Play D.

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
      
      if len(self.history) == 999:  # About to play round 1000
          return axl.Action.D
      
      return opponent.history[-1]



# # Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# any of the following conditions apply, checked in order:  1. Your opponent
# defected on the previous round. 2. It is round 980 or later. 3. Your opponent
# has defected on more than 15% of all rounds played so far.  Otherwise,
# cooperate.

class Aggressive_7(LLM_Strategy):
  n = 7
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
      
      # Condition 1: Opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 2: It is round 980 or later
      # current_round here represents the round we're currently playing
      # len(self.history) gives rounds played so far, so current round = len(self.history) + 1
      if current_round >= 980:
          return axl.Action.D
      
      # Condition 3: Opponent has defected on more than 15% of all rounds played so far
      rounds_played = len(opponent.history)
      if rounds_played > 0:
          defection_rate = opponent.history.defections / rounds_played
          if defection_rate > 0.15:
              return axl.Action.D
      
      # Otherwise, cooperate
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 995:** Mirror your opponent's previous move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 996 through 1000:** Always defect, regardless of your
# opponent's recent behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 996:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **All subsequent rounds:** Play whatever
# your opponent played in the previous round.

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
      return opponent.history[-1]



# # Aggressive Tit-for-Tat Strategy  **Round 1:** Defect.  **Rounds 2 to 990:**
# If your opponent cooperated on the previous round, defect. If your opponent
# defected on the previous round, defect.  That is, defect unconditionally
# throughout this phase.  **Rounds 991 to 1000:** Defect unconditionally.  ---
# In plain terms: always defect throughout the entire game. The payoff structure
# rewards exploitation heavily (5 versus 3 for mutual cooperation), and the risk
# of being exploited yourself (scoring 0) makes unconditional defection the
# dominant choice under an aggressive mandate. Mutual defection yields 1 per
# round, which is preferable to the risk of scoring 0, and the temptation payoff
# of 5 is aggressively pursued whenever the opponent cooperates. Since no
# cooperative relationship yields a sufficiently large advantage over consistent
# defection to justify the vulnerability it creates, defection is applied in
# every round without exception.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# ## Strategy: Tit-for-Tat with End-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 995:** Copy exactly what your opponent played
# in the previous round. If they cooperated, cooperate. If they defected,
# defect.  **Rounds 996 through 1000:** Defect unconditionally, regardless of
# what your opponent does.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 996:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **All subsequent rounds:** Play whatever
# your opponent played in the previous round.

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



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# your opponent defected on the previous round. Cooperate if your opponent
# cooperated on the previous round.

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
      
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          return axl.Action.C



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Mirror your opponent's previous move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 991 through 1000:** Defect unconditionally,
# regardless of the opponent's recent behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 991:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **All subsequent rounds:** Play whatever
# your opponent played in the previous round.

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



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# the opponent defected on the previous round. Cooperate if the opponent
# cooperated on the previous round.

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
      
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          return axl.Action.C



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 995:** Mirror your opponent's previous move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 996 through 1000:** Defect unconditionally,
# regardless of the opponent's history or recent behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 996:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 1000:** Apply the following
# conditions in order:  1. If the opponent has played D in at least 60% of all
# previous rounds, play D. 2. If the opponent played D in the previous round,
# play D. 3. Otherwise, play C.

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
      
      total_rounds = len(opponent.history)
      
      # Condition 1: If opponent has played D in at least 60% of all previous rounds
      if opponent.history.defections / total_rounds >= 0.6:
          return axl.Action.D
      
      # Condition 2: If opponent played D in the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 3: Otherwise, play C
      return axl.Action.C



# ## Aggressive Tit-for-Tat Strategy  **Round 1:** Defect.  **Rounds 2 through
# 990:** If your opponent cooperated on the previous round, defect. If your
# opponent defected on the previous round, defect.  That is: always defect
# throughout this phase regardless of what the opponent does.  **Rounds 991
# through 1000:** Defect unconditionally.  ---  **Rationale summary:** The
# temptation payoff of 5 from unilateral defection exceeds the mutual
# cooperation payoff of 3, and the mutual defection payoff of 1 still exceeds
# the sucker payoff of 0. An unconditional defection strategy exploits any
# cooperative opponent for the maximum possible gain in every round, and against
# an opponent who also defects, it matches their outcome without suffering the
# sucker payoff. There is no future-reward mechanism strong enough to justify
# the risk of cooperation given the asymmetry between the sucker payoff (0) and
# the temptation payoff (5), and since defection is the dominant action in the
# stage game, applying it consistently across all 1000 rounds maximises expected
# payoff regardless of the opponent's strategy.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# ## Strategy: Tit-for-Tat with Endgame Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Copy exactly what your opponent played
# in the previous round. If they cooperated last round, cooperate. If they
# defected last round, defect.  **Rounds 991 through 1000:** Defect
# unconditionally, regardless of what your opponent does or has done.

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
      
      current_round = len(self.history) + 1
      
      if current_round >= 991:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  On the first round, play C.  From round 2 onward, apply the
# following conditions in order:  1. If your opponent has defected in more than
# 55% of all previous rounds, play D for the remainder of the game. 2. If your
# opponent defected in the previous round, play D. 3. Otherwise, play C.

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
      
      # Condition 1: If opponent has defected in more than 55% of all previous rounds
      total_rounds = len(opponent.history)
      if total_rounds > 0:
          defection_rate = opponent.history.defections / total_rounds
          if defection_rate > 0.55:
              return axl.Action.D
      
      # Condition 2: If opponent defected in the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 3: Otherwise, play C
      return axl.Action.C



# # Aggressive Strategy  **Round 1:** Defect.  **All subsequent rounds:** Defect
# if your opponent defected on the previous round. Cooperate if your opponent
# cooperated on the previous round.  **Final 5 rounds (rounds 996–1000):**
# Defect unconditionally, regardless of your opponent's recent behaviour.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # First round: Defect
      if self.first_round():
          return axl.Action.D
      
      # Final 5 rounds (rounds 996-1000, i.e., when len(history) >= 995)
      if len(self.history) >= 995:
          return axl.Action.D
      
      # All subsequent rounds: mirror opponent's last move
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          return axl.Action.C



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Mirror your opponent's most recent move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 991 through 1000:** Defect unconditionally,
# regardless of the opponent's recent behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 991:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 999:** Play whatever your
# opponent played in the previous round.  **Round 1000:** Play D.

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
      
      if len(self.history) == 999:
          return axl.Action.D
      
      return opponent.history[-1]



# # Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# any of the following conditions are met, checked in order:  1. The opponent
# defected on the previous round. 2. It is round 980 or later. 3. The opponent
# has defected on more than 10% of all rounds played so far.  Otherwise,
# cooperate.

class Aggressive_13(LLM_Strategy):
  n = 13
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
      # But we need to check conditions based on current round
      round_number = len(self.history) + 1
      
      # Condition 1: Opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 2: It is round 980 or later
      if round_number >= 980:
          return axl.Action.D
      
      # Condition 3: Opponent has defected on more than 10% of all rounds played so far
      rounds_played = len(opponent.history)
      if rounds_played > 0:
          defection_rate = opponent.history.defections / rounds_played
          if defection_rate > 0.10:
              return axl.Action.D
      
      # Otherwise, cooperate
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Mirror your opponent's previous move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 991 through 1000:** Defect unconditionally,
# regardless of your opponent's recent behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 991:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **All subsequent rounds:** Play whatever
# your opponent played in the previous round.

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



# # Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 998:** If your
# opponent cooperated on the previous round, defect. If your opponent defected
# on the previous round, defect.  **Rounds 999 and 1000:** Defect.  ---  This
# strategy always defects regardless of the opponent's behaviour. Given the
# payoff structure, defection dominates cooperation in every individual round:
# defecting yields either 5 or 1, while cooperating yields either 3 or 0,
# meaning defection always produces a higher or equal payoff than cooperation
# against any given opponent action. An aggressive maximisation approach
# therefore commits to defection unconditionally throughout all 1000 rounds,
# with no conditions under which cooperation is ever chosen.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 995:** Mirror your opponent's previous move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 996 through 1000:** Defect unconditionally,
# regardless of the opponent's recent behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 996:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 999:** If the opponent played
# C in the previous round, play C. If the opponent played D in the previous
# round, play D.  **Round 1000:** Play D.

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
      
      if len(self.history) == 999:
          return axl.Action.D
      
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D



# # Aggressive Tit-for-Tat Strategy  **Round 1:** Defect.  **Rounds 2 to 990:**
# If your opponent cooperated on the previous round, defect. If your opponent
# defected on the previous round, defect.  That is, defect unconditionally
# throughout this phase.  **Rounds 991 to 1000:** Defect unconditionally.  ---
# In plain terms: always defect for the entire game.  The reasoning is
# straightforward. The temptation payoff of 5 beats mutual cooperation at 3, and
# even mutual defection at 1 beats being exploited at 0. Since defecting
# strictly dominates cooperating regardless of what the opponent does in any
# single round, and since the end of the game is known and fixed at round 1000,
# backward induction unravels any incentive to cooperate: there is no reason to
# cooperate on round 1000, therefore no reason to cooperate on round 999, and so
# on back to round 1. Consistent defection is therefore the dominant strategy
# and maximises your expected payoff against any opponent strategy, eliminating
# the risk of scoring 0 while capturing either 5 against cooperators or 1
# against fellow defectors.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 995:** If the opponent played
# C in the previous round, play C. If the opponent played D in the previous
# round, play D.  **Rounds 996 to 1000:** Play D unconditionally.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 996:
          return axl.Action.D
      
      # Rounds 2 to 995: Tit for Tat
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D



# ## Strategy  On the first round, play C.  On each subsequent round, play
# whatever your opponent played in the previous round.

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



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# your opponent defected on the previous round. Cooperate if your opponent
# cooperated on the previous round.

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
      
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          return axl.Action.C



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Mirror your opponent's most recent move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 991 through 1000:** Defect unconditionally,
# regardless of the opponent's behaviour.

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
      
      current_round = len(self.history) + 1
      
      if current_round >= 991:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **All subsequent rounds:** Play whatever
# your opponent played in the previous round.

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
      return opponent.history[-1]



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# any of the following conditions are met, checking them in order:  1. Your
# opponent defected on the previous round. 2. It is round 990 or later.
# Otherwise, cooperate.  ---  This strategy opens with defection to probe the
# opponent and seize an early advantage. Against a retaliatory opponent, it
# transitions into mutual cooperation when they reciprocate cooperation,
# exploiting the fact that sustained mutual cooperation (3 points each round)
# outperforms sustained mutual defection (1 point each round). The unconditional
# defection in the final ten rounds prevents being exploited during the endgame,
# where future retaliation is no longer a meaningful deterrent.

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
      
      current_round = len(self.history) + 1
      
      # Condition 1: Opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 2: Round 990 or later
      if current_round >= 990:
          return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Mirror your opponent's previous move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 991 through 1000:** Defect unconditionally,
# regardless of your opponent's behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 991:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 999:** Play whatever your
# opponent played in the previous round.  **Round 1000:** Play D.

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
      
      if len(self.history) == 999:  # About to play round 1000
          return axl.Action.D
      
      return opponent.history[-1]



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# your opponent defected on the previous round. Cooperate if your opponent
# cooperated on the previous round.

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
      
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          return axl.Action.C



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Mirror your opponent's previous move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 991 through 1000:** Defect unconditionally,
# regardless of the opponent's recent behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 991:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **Rounds 2–1000:** Apply the following
# conditions in order:  1. If the opponent has played D in the majority of all
# their previous rounds, play D. 2. If the opponent played D in the previous
# round, play D. 3. Otherwise, play C.

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
      
      # Condition 1: If opponent has played D in the majority of all their previous rounds
      if opponent.history.defections > opponent.history.cooperations:
          return axl.Action.D
      
      # Condition 2: If opponent played D in the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 3: Otherwise, play C
      return axl.Action.C



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# any of the following conditions apply, checked in order:  1. The opponent
# defected on the previous round. 2. It is one of the last 5 rounds (rounds 996
# to 1000). 3. The opponent has defected on more than 15% of all rounds played
# so far.  **Otherwise:** Cooperate.

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
      
      # Condition 1: Opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 2: One of the last 5 rounds (rounds 996 to 1000)
      current_round = len(self.history) + 1  # next round number
      if current_round >= 996:
          return axl.Action.D
      
      # Condition 3: Opponent has defected on more than 15% of all rounds played so far
      rounds_played = len(opponent.history)
      if rounds_played > 0:
          defection_rate = opponent.history.defections / rounds_played
          if defection_rate > 0.15:
              return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 995:** Mirror your opponent's most recent move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 996 through 1000:** Defect unconditionally,
# regardless of the opponent's history or recent behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 996:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **All subsequent rounds:** Play whatever
# your opponent played in the previous round.

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



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# any of the following conditions are met, evaluated in order:  1. Your opponent
# defected on the previous round. 2. There are 5 or fewer rounds remaining.
# Otherwise, cooperate.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Defect
      if self.first_round():
          return axl.Action.D
      
      # Total rounds in the game
      total_rounds = 1000
      current_round = len(self.history) + 1  # The round we're about to play
      rounds_remaining = total_rounds - current_round
      
      # Condition 1: Opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 2: 5 or fewer rounds remaining
      if rounds_remaining <= 5:
          return axl.Action.D
      
      # Otherwise, cooperate
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Endgame Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 995:** Mirror your opponent's previous move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 996 through 1000:** Defect unconditionally,
# regardless of the opponent's recent behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 996:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  On the first round, play C.  From the second round onwards, copy
# whatever your opponent played in the immediately preceding round.

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
      return opponent.history[-1]



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# any of the following conditions are met, checked in order:  1. Your opponent
# defected on the previous round. 2. There are 8 or fewer rounds remaining.
# Otherwise, cooperate.

class Aggressive_21(LLM_Strategy):
  n = 21
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
      # Condition 1: Opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 2: There are 8 or fewer rounds remaining
      # Total rounds = 1000, rounds played = len(self.history)
      rounds_remaining = 1000 - len(self.history)
      if rounds_remaining <= 8:
          return axl.Action.D
      
      # Otherwise, cooperate
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Endgame Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 995:** Mirror your opponent's most recent move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 996 through 1000:** Defect unconditionally,
# regardless of the opponent's recent behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 996:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 1000:** Apply the following
# conditions in order:  1. If your opponent has played D in at least 8 of the
# last 10 rounds, play D. 2. If your opponent played C in the previous round,
# play C. 3. Otherwise, play D.

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
      
      # Condition 1: If opponent has played D in at least 8 of the last 10 rounds
      last_10 = opponent.history[-10:]
      if last_10.count(axl.Action.D) >= 8:
          return axl.Action.D
      
      # Condition 2: If opponent played C in the previous round
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # Condition 3: Otherwise, play D
      return axl.Action.D



# # Aggressive Strategy  **Round 1:** Defect.  **All subsequent rounds:** Defect
# if your opponent defected on the previous round. Cooperate if your opponent
# cooperated on the previous round.  **Final 5 rounds (rounds 996–1000):**
# Defect unconditionally, regardless of your opponent's recent behaviour.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # First round: Defect
      if self.first_round():
          return axl.Action.D
      
      # Final 5 rounds (rounds 996-1000, i.e., when len(history) >= 995): Defect
      if len(self.history) >= 995:
          return axl.Action.D
      
      # All subsequent rounds: mirror opponent's last move
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          return axl.Action.C



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Mirror your opponent's most recent move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 991 through 1000:** Defect unconditionally,
# regardless of your opponent's behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 991:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **All subsequent rounds:** Play whatever
# your opponent played in the previous round.

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



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# any of the following conditions are met, checked in order:  1. Your opponent
# defected on the previous round. 2. The current round is 980 or later. 3. Your
# opponent has defected on more than 15% of all rounds played so far.
# Otherwise, cooperate.

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
      
      # Condition 1: Opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 2: Current round is 980 or later
      current_round = len(self.history) + 1  # This is the round we're deciding for
      if current_round >= 980:
          return axl.Action.D
      
      # Condition 3: Opponent has defected on more than 15% of all rounds played so far
      rounds_played = len(opponent.history)
      if rounds_played > 0:
          defection_rate = opponent.history.defections / rounds_played
          if defection_rate > 0.15:
              return axl.Action.D
      
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Mirror your opponent's most recent move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 991 through 1000:** Defect unconditionally,
# regardless of the opponent's behaviour.

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
      
      current_round = len(self.history) + 1
      
      if current_round >= 991:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 1000:** Apply the following
# conditions in order:  1. If your opponent has played D in at least 70% of all
# preceding rounds, play D. 2. If your opponent played D in the previous round,
# play D. 3. Otherwise, play C.

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
      
      total_rounds = len(opponent.history)
      
      # Condition 1: If opponent has played D in at least 70% of all preceding rounds
      if opponent.history.defections / total_rounds >= 0.70:
          return axl.Action.D
      
      # Condition 2: If opponent played D in the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 3: Otherwise, play C
      return axl.Action.C



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# any of the following conditions apply, checked in order:  1. Your opponent
# defected on the previous round. 2. It is round 990 or later. 3. Your
# cumulative score exceeds your opponent's cumulative score by 20 points or
# more.  Otherwise, cooperate.

class Aggressive_24(LLM_Strategy):
  n = 24
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
      
      # Condition 1: Opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 2: It is round 990 or later
      # current_round here represents the round we're currently playing
      # len(self.history) gives rounds played so far, so current round = len(self.history) + 1
      if current_round >= 990:
          return axl.Action.D
      
      # Condition 3: Cumulative score exceeds opponent's by 20 or more
      if self.score - opponent.score >= 20:
          return axl.Action.D
      
      # Otherwise, cooperate
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Endgame Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Mirror your opponent's previous move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 991 through 1000:** Defect unconditionally,
# regardless of the opponent's recent behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 991:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **All subsequent rounds:** Play whatever
# your opponent played in the previous round.

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



# ## Aggressive Strategy  **Round 1:** Defect.  **Rounds 2 to 1000:** Defect if
# any of the following conditions are met, checked in order:  1. Your opponent
# defected on the previous round. 2. It is round 980 or later. 3. None of the
# above conditions are met — in this case, cooperate.

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
      
      # Condition 1: Opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 2: It is round 980 or later
      current_round = len(self.history) + 1  # This will be the round number after this move
      if len(self.history) >= 979:  # rounds 980-1000 (0-indexed: 979-999)
          return axl.Action.D
      
      # None of the above conditions met - cooperate
      return axl.Action.C



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Mirror your opponent's most recent move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 991 through 1000:** Defect unconditionally,
# regardless of the opponent's behaviour.

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
      
      current_round = len(self.history) + 1
      
      if current_round >= 991:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **All subsequent rounds:** Play whatever
# your opponent played in the previous round.

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