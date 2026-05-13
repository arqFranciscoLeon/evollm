import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# ## Aggressive Tit-for-Tat Strategy  **Round 1:** Defect.  **Rounds 2 through
# 997:** If your opponent cooperated on the previous round, defect. If your
# opponent defected on the previous round, defect.  That is: always defect
# unconditionally throughout these rounds.  **Rounds 998 through 1000:** Defect.
# ---  **Rationale embedded in the conditions:**  The payoff structure makes
# defection strictly dominant in any single round — defecting always yields more
# than cooperating regardless of what the opponent does (5 > 3 when they
# cooperate, 1 > 0 when they defect). Because mutual defection yields 1 per
# round and mutual cooperation yields 3, there is a theoretical cost to
# persistent defection against a cooperative opponent. However, an aggressive
# strategy accepts this trade-off: it never risks scoring 0 from being
# exploited, it captures 5 whenever the opponent cooperates, and it never allows
# the opponent to condition you into cooperation that they can then exploit.
# Against any opponent who eventually defects, unconditional defection matches
# or outperforms cooperation. Against a cooperative opponent, defection
# consistently extracts the maximum available payoff of 5 rather than the mutual
# 3.  **Always defect in every round.**

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
# on round 1.  **Rounds 2 through 995:** Mirror your opponent's previous move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 996 through 1000:** Defect unconditionally,
# regardless of the opponent's recent behaviour.

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
      
      round_number = len(self.history) + 1
      
      if round_number >= 996:
          return axl.Action.D
      
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 1000:** Play whatever your
# opponent played in the previous round.

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
# any of the following conditions are met, checked in order:  1. The opponent
# defected on the previous round. 2. It is round 980 or later.  Otherwise,
# cooperate.

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
      
      current_round = len(self.history) + 1
      
      # Condition 1: Opponent defected on the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 2: It is round 980 or later
      if current_round >= 980:
          return axl.Action.D
      
      return axl.Action.C



# ## Strategy  **Round 1:** Play C.  **All subsequent rounds:** Play whatever
# your opponent played in the previous round.

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



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 995:** If the opponent played
# C in the previous round, play C. If the opponent played D in the previous
# round, play D.  **Rounds 996 to 1000:** Play D unconditionally.

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
      
      if round_number >= 996:
          return axl.Action.D
      
      # Rounds 2 to 995: Tit for Tat
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D



# ## Aggressive Tit-for-Tat Strategy  **Round 1:** Defect.  **Rounds 2 through
# 997:** If your opponent cooperated on the previous round, defect. If your
# opponent defected on the previous round, defect.  That is: always defect,
# regardless of what your opponent did.  **Rounds 998 through 1000:** Defect.
# ---  **Rationale embedded in the conditions:**  The payoff structure means
# defection always yields a strictly higher individual payoff than cooperation
# regardless of what the opponent plays — scoring 5 instead of 3 when they
# cooperate, and scoring 1 instead of 0 when they defect. There is no payoff
# scenario in which cooperating produces a better outcome for you than defecting
# given your opponent's fixed action. With a known endpoint of 1000 rounds,
# backward induction also eliminates any incentive to cooperate in the final
# rounds, and this unravels cooperation incentives across all rounds.
# Unconditional defection is therefore the dominant strategy that maximises your
# cumulative payoff under this specific payoff matrix.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# ## Strategy: Tit-for-Tat with Late-Game Defection  **Opening move:** Cooperate
# on round 1.  **Rounds 2 through 990:** Mirror your opponent's previous move
# exactly. If they cooperated last round, cooperate. If they defected last
# round, defect.  **Rounds 991 through 1000:** Defect unconditionally,
# regardless of the opponent's history or recent behaviour.

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



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 1000:** Play whatever your
# opponent played in the previous round.

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
      return opponent.history[-1]



# ## Aggressive Strategy  **Round 1:** Defect.  **All subsequent rounds:**
# Defect if your opponent defected in the previous round. Cooperate if your
# opponent cooperated in the previous round.  **Final 5 rounds (rounds
# 996–1000):** Defect unconditionally, regardless of your opponent's recent
# behaviour.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Total rounds in the game
      total_rounds = 1000
      # Current round number (1-indexed)
      current_round = len(self.history) + 1
      
      # Final 5 rounds: defect unconditionally
      if current_round >= 996:
          return axl.Action.D
      
      # Round 1: Defect
      if self.first_round():
          return axl.Action.D
      
      # All subsequent rounds: mirror opponent's last move
      return opponent.history[-1]



# ## Strategy  **Round 1:** Play C.  **Rounds 2 to 997:** Play whatever your
# opponent played in the previous round. If they cooperated, cooperate. If they
# defected, defect.  **Rounds 998 to 1000:** Play D unconditionally.

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
      
      if round_number >= 998:
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



# ## Aggressive Tit-for-Tat Strategy  **Round 1:** Defect.  **Rounds 2 through
# 990:** If your opponent cooperated on the previous round, defect. If your
# opponent defected on the previous round, defect.  That is, defect
# unconditionally throughout this phase.  **Rounds 991 through 1000:** Defect
# unconditionally regardless of your opponent's previous actions.  ---
# **Rationale summary:** The payoff structure heavily rewards unilateral
# defection (5) and punishes unilateral cooperation (0), while mutual defection
# (1,1) only marginally underperforms mutual cooperation (3,3). Because the game
# has a known endpoint, backward induction erodes any incentive to cooperate
# near the end, and an aggressive opening removes the risk of being exploited
# during any cooperative establishment phase. Continuous defection captures the
# maximum available payoff against naive or cooperative opponents and avoids the
# zero payoff entirely, accepting mutual defection as the baseline outcome
# against similarly aggressive opponents.

class Aggressive_5(LLM_Strategy):
  n = 5
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
      
      if round_number >= 996:
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