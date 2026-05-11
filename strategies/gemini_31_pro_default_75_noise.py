import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# To maximize your overall payoff using an aggressive approach, you should
# employ a strategy that ruthlessly exploits forgiving opponents, strictly
# punishes defection, but maintains mutually beneficial cooperation when faced
# with retaliation.   Here is the strategy, ordered by priority from highest to
# lowest. Apply the first condition that fits the current round:  1. **Endgame
# Exploitation:** If it is exactly round 1000, play **Defect**. (Since there are
# no future rounds, retaliation is impossible, allowing you to safely secure the
# highest possible points). 2. **First Round Probe:** If it is round 1, play
# **Defect**. (This tests the opponent immediately to see if they are a passive
# player who will allow unconditional exploitation). 3. **Restoring
# Cooperation:** If both you and the opponent

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. Endgame Exploitation: Exactly round 1000
      if len(self.history) == 999:
          return axl.Action.D
          
      # 2. First Round Probe: Round 1
      if self.first_round():
          return axl.Action.D
          
      # 3. Restoring Cooperation / Maintaining Cooperation / Punishing / Exploiting
      # This follows the Pavlov (Win-Stay, Lose-Shift) logic implied by the description:
      # - If both played C (mutually beneficial), play C.
      # - If both played D (faced with retaliation), play C to restore cooperation.
      # - If you played D and opponent played C (forgiving opponent), play D to exploit.
      # - If you played C and opponent played D (unprovoked defection), play D to punish.
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
          
      return axl.Action.D



# Play the game according to the following chronological rules:  1. In the first
# round, choose to cooperate (play C).  2. From round 2 through round 999, copy
# the action your opponent took in the immediately preceding round: play C if
# your opponent played C, and play D if your opponent played D. 3. In the 1000th
# and final round, choose to defect (play D) regardless of your opponent's
# previous moves.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# 1. **Round 1:** Play C. 2. **Rounds 2 through 999:** Mirror your opponent's
# move from the immediately preceding round. If your opponent played C in the
# previous round, play C. If your opponent played D in the previous round, play
# D. 3. **Round 1000:** Play D unconditionally, regardless of your opponent's
# previous actions.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# To execute this aggressive strategy, evaluate the following conditions in
# order each round and perform the action for the first condition that is true:
# 1. If it is the final round (round 1000), play Defect. 2. If it is the first
# round, play Defect. 3. If your opponent played Defect in the immediate
# previous round, play Defect. 4. If your opponent has played Cooperate in the
# previous three consecutive rounds, play Defect. 5. In all other situations,
# play Cooperate.   This approach guarantees you capture the maximum payoff of 5
# at the beginning and end of the game, immediately punishes your opponent's
# defections to avoid the 0 payoff, and periodically exploits their sustained
# cooperation while generally allowing mutual 3s to accumulate.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. If it is the final round (round 1000), play Defect.
      if len(self.history) == 999:
          return axl.Action.D
          
      # 2. If it is the first round, play Defect.
      if self.first_round():
          return axl.Action.D
          
      # 3. If your opponent played Defect in the immediate previous round, play Defect.
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      # 4. If your opponent has played Cooperate in the previous three consecutive rounds, play Defect.
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]:
          return axl.Action.D
          
      # 5. In all other situations, play Cooperate.
      return axl.Action.C



# Here is a simple, cooperative strategy to maximise your overall payoff:  1.
# **Round 1:** Play C. 2. **Rounds 2 through 999:** Copy your opponent's move
# from the immediately preceding round. Play C if your opponent played C, and
# play D if your opponent played D.  3. **Round 1000:** Play D, regardless of
# your opponent's previous moves.

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
      
      if len(self.history) == 999:
          return axl.Action.D
          
      return opponent.history[-1]



# Here is the strategy, ordered chronologically:  1. **Round 1:** Play
# cooperate. 2. **Rounds 2 through 999:** Copy the exact move your opponent
# played in the immediately preceding round. If they cooperated in the previous
# round, you cooperate. If they defected in the previous round, you defect. 3.
# **Round 1000:** Play defect, regardless of your opponent's previous moves.

class Neutral_2(LLM_Strategy):
  n = 2
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]



# Here is a simple, aggressive strategy designed to maximize your payoff by
# exploiting forgiving opponents while protecting yourself from being exploited:
# **Strategy Rules (in order of priority):**  1. **Endgame Exploitation:** If
# the game is in the final 10 rounds (rounds 991 through 1000), play **Defect**.
# 2. **Cycle Breaking:** If both you and your opponent played Defect in the
# previous two consecutive rounds, play **Cooperate**. (This attempts to break
# mutually destructive retaliatory cycles and reset to a higher payoff). 3.
# **Self-Defense:** If the opponent played Defect in the previous round, play
# **Defect**. (This ensures you are not repeatedly taken advantage of). 4.
# **Aggressive Pro

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. Endgame Exploitation: If the game is in the final 10 rounds (rounds 991 through 1000), play Defect.
      if len(self.history) >= 990:
          return axl.Action.D
  
      # 2. Cycle Breaking: If both you and your opponent played Defect in the previous two consecutive rounds, play Cooperate.
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and
              opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D):
              return axl.Action.C
  
      # 3. Self-Defense: If the opponent played Defect in the previous round, play Defect.
      if len(opponent.history) >= 1:
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.D
  
      # 4. Aggressive Pro[bing] / Default fallback
      return axl.Action.C



# To maximize your overall payoff using a cooperative approach, follow these
# rules in order:  1. **Round 1:** Choose to cooperate. 2. **Rounds 2 through
# 999:** Copy the exact action your opponent took in the immediately preceding
# round. Choose to cooperate if they just cooperated, and choose to defect if
# they just defected.  3. **Round 1000 (Final Round):** Choose to defect,
# regardless of your opponent's previous actions.

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
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1]



# Here is a simple, neutral strategy to maximize your overall payoff over the
# 1000 rounds:  1. **Round 1:** Play Cooperate. 2. **Rounds 2 through 999:**
# Play Cooperate if your opponent played Cooperate in the immediately preceding
# round. 3. **Rounds 2 through 999:** Play Defect if your opponent played Defect
# in the immediately preceding round. 4. **Round 1000:** Play Defect, regardless
# of your opponent's previous actions.

class Neutral_3(LLM_Strategy):
  n = 3
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.C
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# Here is a simple, aggressive strategy designed to maximize your payoff by
# establishing cooperation, strictly punishing exploitation, and preemptively
# securing points at the end of the game.   Evaluate the following conditions in
# order from top to bottom each round:  1. **If the current round is 999 or
# 1000:** Play Defect. 2. **If the opponent played Defect in the previous
# round:** Play Defect.  3. **In all other situations (including round 1):**
# Play Cooperate.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) >= 998:
          return axl.Action.D
      if len(opponent.history) > 0 and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# To maximize your overall payoff using a cooperative approach, use the
# following strategy:  1. In round 1, play C. 2. In rounds 2 through 999, copy
# the action your opponent took in the immediately preceding round: play C if
# they played C, and play D if they played D. 3. In round 1000, play D
# regardless of your opponent's previous actions.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# To maximise your overall payoff using a simple, neutral approach, follow this
# ordered set of rules:  1. **Round 1:** Play Cooperate.  2. **Rounds 2 through
# 999:** Copy your opponent's move from the immediately preceding round. Play
# Cooperate if your opponent played Cooperate, and play Defect if your opponent
# played Defect. 3. **Round 1000 (Final Round):** Play Defect, regardless of
# your opponent's previous actions, to secure the highest possible concluding
# payoff without risk of future retaliation.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# Here is a straightforward, aggressive strategy designed to maximize your
# overall payoff by exploiting weak opponents while maintaining highly
# profitable mutual cooperation with forgiving ones. This strategy is based on
# the "Win-Stay, Lose-Shift" logic.  **Conditions for play:**  1. **Round
# 1000:** Always play Defect. Since it is the final round, there are no future
# consequences, guaranteeing you either 5 or 1 point. 2. **Round 1:** Play
# Defect. This aggressively tests the opponent immediately to see if they can be
# exploited for a 5-point payoff.  3. **Round 2 to 999:**    - Play **Defect**
# if you and your opponent chose *different* actions in the previous round. This

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.D
          
      if len(self.history) >= 999:
          return axl.Action.D
          
      if self.history[-1] != opponent.history[-1]:
          return axl.Action.D
          
      return axl.Action.C



# Here is a simple, cooperative strategy to maximize your overall payoff:  1.
# **Round 1:** Choose to cooperate. 2. **Rounds 2 through 999:** Choose the
# exact action your opponent took in the immediately preceding round. If they
# cooperated on the previous turn, choose to cooperate; if they defected on the
# previous turn, choose to defect. 3. **Round 1000:** Choose to defect,
# regardless of your opponent's previous actions, to guarantee the highest
# possible payoff when there is no threat of future retaliation.

class Cooperative_5(LLM_Strategy):
  n = 5
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
      elif len(self.history) >= 999:
          return axl.Action.D
      else:
          return opponent.history[-1]



# To maximize your overall payoff using a neutral approach, follow these
# conditions in chronological order:  1. If it is the first round, choose to
# cooperate.  2. If it is any round from round 2 up to round 999, copy the
# action your opponent took in the immediately preceding round: choose to
# cooperate if they cooperated, and choose to defect if they defected. 3. If it
# is the final round (round 1000), choose to defect, regardless of your
# opponent's previous actions.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# Apply the following rules in strict order of priority for each round:  1. If
# the current round is round 995 or higher, play Defect. 2. If your opponent has
# played Defect two or more times cumulatively across all previous rounds, play
# Defect. 3. If your opponent played Defect in the immediately preceding round,
# play Defect. 4. In all other situations, including the first round, play
# Cooperate.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1: If the current round is round 995 or higher, play Defect.
      # The first round corresponds to len(self.history) == 0, so round 995 is len(self.history) == 994.
      if len(self.history) >= 994:
          return axl.Action.D
          
      # Rule 2: If your opponent has played Defect two or more times cumulatively across all previous rounds, play Defect.
      if opponent.history.defections >= 2:
          return axl.Action.D
          
      # Rule 3: If your opponent played Defect in the immediately preceding round, play Defect.
      if len(opponent.history) > 0 and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      # Rule 4: In all other situations, including the first round, play Cooperate.
      return axl.Action.C



# Here is a simple, cooperative strategy to maximize your overall payoff:  1.
# **Round 1:** Play Cooperate. 2. **Rounds 2 through 999:** Copy the exact
# action your opponent took in the immediately preceding round.     - Play
# Cooperate if your opponent played Cooperate.    - Play Defect if your opponent
# played Defect. 3. **Round 1000:** Play Defect, regardless of your opponent's
# previous actions.

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
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]



# Here is the strategy:  1. **Round 1:** Play C. 2. **Rounds 2 through 999:**
# Play C if your opponent played C in the immediately preceding round. Play D if
# your opponent played D in the immediately preceding round.  3. **Round 1000:**
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
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1]



# Here is a simple, aggressive strategy designed to test the opponent,
# relentlessly exploit forgiving players, and pacify retaliatory players to
# ensure maximum long-term payoff.   Apply these rules in strict order of
# priority (from top to bottom):  1. **The Endgame:** On the final round (round
# 1000), play Defect. 2. **The Initial Test:** On round 1, play Defect. 3. **The
# Pacification:** On rounds 2 and 3, play Cooperate to observe their response to
# your initial defection and to reset the relationship if they are capable of
# forgiveness.  4. **The Long Game (Rounds 4 through 999):**    - **Exploit:**
# If the opponent played Cooperate

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      # 1. The Endgame
      if current_round == 1000:
          return axl.Action.D
          
      # 2. The Initial Test
      if current_round == 1:
          return axl.Action.D
          
      # 3. The Pacification
      if current_round == 2 or current_round == 3:
          return axl.Action.C
          
      # 4. The Long Game (Rounds 4 through 999)
      # Exploit forgiving players (who played C), pacify retaliatory players (who played D)
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
      else:
          return axl.Action.C



# Here is a simple, cooperative strategy to maximize your payoff over the 1000
# rounds:  1. **Round 1:** Choose to cooperate. 2. **Rounds 2 through 999:**
# Copy the exact action your opponent took in the immediately preceding round.
# If they cooperated in the previous round, you cooperate. If they defected in
# the previous round, you defect.  3. **Round 1000:** Choose to defect,
# regardless of your opponent's previous actions.

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
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]



# To maximise your overall payoff using a neutral, reciprocal approach, follow
# this ordered strategy:  1. **Round 1:** Play C.  2. **Rounds 2 through 999:**
# Copy your opponent's action from the immediately preceding round. Play C if
# your opponent played C, and play D if your opponent played D. 3. **Round 1000
# (Final Round):** Play D, regardless of your opponent's previous actions.

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
      
      if len(self.history) == 999:
          return axl.Action.D
          
      return opponent.history[-1]



# To adopt an aggressive approach that maximizes your overall payoff, you should
# use a strategy that actively tests the opponent for weakness to exploit them,
# but gracefully apologizes and cooperates if the opponent proves capable of
# retaliation.   Here is the straightforward condition-based strategy, executed
# in the following strict order of priority every round:  1. **If it is Round
# 1000:** Play D. *(Maximizes payoff on the final move since no future
# retaliation is possible).* 2. **If it is Round 1:** Play D. *(The initial
# probe to test if the opponent is a passive cooperator).* 3. **If it is Round 2
# or Round 3:** Play C. *(This serves as an apology to absorb any retaliation
# from a Tit-for-Tat

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
  
      # 1. If it is Round 1000: Play D.
      if round_number == 1000:
          return axl.Action.D
  
      # 2. If it is Round 1: Play D.
      if round_number == 1:
          return axl.Action.D
  
      # 3. If it is Round 2 or Round 3: Play C.
      if round_number == 2 or round_number == 3:
          return axl.Action.C
  
      # If the opponent retaliated to our initial defection (played D in Round 2 or Round 3),
      # we assume they are capable of retaliation (like Tit-for-Tat) and play Tit-for-Tat.
      if opponent.history[1] == axl.Action.D or opponent.history[2] == axl.Action.D:
          return opponent.history[-1]
      
      # If the opponent did not retaliate, they are a passive cooperator, so we exploit them.
      return axl.Action.D



# 1. On the first round, play Cooperate.  2. On rounds 2 through 999, copy the
# exact move your opponent made in the immediately preceding round: play
# Cooperate if they played Cooperate, and play Defect if they played Defect.  3.
# On round 1000, play Defect regardless of your opponent's previous moves.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# Apply the following strategy, ordered chronologically:  1. **Round 1:** Play
# C. 2. **Rounds 2 through 999:** Play the exact same action your opponent
# played in the immediately preceding round. Play C if your opponent played C;
# play D if your opponent played D. 3. **Round 1000:** Play D, regardless of
# your opponent's previous actions.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# Here is a simple, aggressive strategy designed to maximize your payoff by
# continuously testing your opponent for weakness while cooperating enough to
# maintain highly profitable mutual cooperation if they prove retaliatory.
# Apply these rules in strict order, from first to last:  1. **The Endgame:** On
# the final round (round 1000), always defect. 2. **The Sucker's Retaliation:**
# If you cooperated in the previous round and your opponent defected, defect to
# punish them. 3. **The Aggressive Probe:** If your opponent has cooperated for
# the last four consecutive rounds, defect to safely exploit their forgiveness
# or test their boundaries. 4. **The Baseline:** Under all other conditions,
# cooperate.   **How it works:** By defaulting to cooperation (Rule 4

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1: The Endgame
      if len(self.history) == 999:
          return axl.Action.D
          
      # Rule 2: The Sucker's Retaliation
      if len(self.history) > 0 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      # Rule 3: The Aggressive Probe
      if len(opponent.history) >= 4 and opponent.history[-4:] == [axl.Action.C] * 4:
          return axl.Action.D
          
      # Rule 4: The Baseline
      return axl.Action.C



# Here is a simple, conditionally cooperative strategy to maximize your overall
# payoff:  1. **Round 1:** Play Cooperate. 2. **Rounds 2 through 999:** Play the
# exact action your opponent played in the immediately preceding round. If they
# played Cooperate on the previous round, play Cooperate. If they played Defect
# on the previous round, play Defect. 3. **Round 1000 (Final Round):** Play
# Defect, regardless of your opponent's previous actions, to secure the highest
# possible payoff without risk of future retaliation.

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
      
      if len(self.history) == 999:
          return axl.Action.D
          
      return opponent.history[-1]



# 1. In the first round, cooperate. 2. From the second round through the 999th
# round, copy your opponent's exact move from the immediately preceding round:
# cooperate if they cooperated, and defect if they defected. 3. In the 1000th
# and final round, defect regardless of your opponent's previous actions.

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
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1]



# Apply the following conditions in order of priority from first to last to
# determine your move each round:  1. **Endgame Defection:** If the current
# round is between 991 and 1000 (the final ten rounds), play Defect. 2.
# **Retaliation:** If your opponent played Defect in the immediately preceding
# round, play Defect. 3. **Exploitation:** If your opponent has played Cooperate
# for the previous three consecutive rounds, play Defect to aggressively secure
# the 5-point payoff. 4. **Baseline Cooperation:** Under all other
# circumstances, including the very first round, play Cooperate to encourage a
# mutually beneficial pattern.

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      # 1. Endgame Defection
      if 991 <= current_round <= 1000:
          return axl.Action.D
          
      if len(opponent.history) > 0:
          # 2. Retaliation
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.D
              
          # 3. Exploitation
          if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]:
              return axl.Action.D
              
      # 4. Baseline Cooperation
      return axl.Action.C



# 1. On round 1, play C. 2. For rounds 2 through 999, play C if your opponent
# played C in the previous round, and play D if your opponent played D in the
# previous round. 3. On round 1000, play D.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# Here is a simple, neutral strategy to maximize your payoff:  1. On the first
# round, cooperate. 2. On rounds 2 through 999, cooperate if your opponent
# cooperated in the immediately preceding round. 3. On rounds 2 through 999,
# defect if your opponent defected in the immediately preceding round.  4. On
# the 1000th round, defect regardless of your opponent's previous actions.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# To adopt an aggressive strategy that maximizes your overall payoff, the goal
# is to ruthlessly exploit forgiving or perfectly cooperative opponents while
# maintaining the ability to establish mutually beneficial cooperation (3
# points) with retaliatory opponents, and finally betraying them at the very
# end.   Apply the following rules in order from top to bottom, choosing the
# first condition that applies to the current round:  1. **The Endgame:** If it
# is round 998, 999, or 1000, play Defect. 2. **The Initial Test:** If it is
# round 1, play Defect.  3. **The Cycle Breaker:** If both you and your opponent
# played Defect in the previous two consecutive rounds, play Cooperate. (This
# signals a willingness

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. The Endgame: If it is round 998, 999, or 1000, play Defect.
      # Since the game lasts 1000 rounds, these correspond to history lengths of 997, 998, and 999.
      if len(self.history) >= 997:
          return axl.Action.D
  
      # 2. The Initial Test: If it is round 1, play Defect.
      if len(self.history) == 0:
          return axl.Action.D
  
      # 3. The Cycle Breaker: If both you and your opponent played Defect in the previous two consecutive rounds, play Cooperate.
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and
              self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D):
              return axl.Action.C
  
      # Default action: Defect (to ruthlessly exploit forgiving/cooperative opponents as per the aggressive strategy goal)
      return axl.Action.D



# Here is a simple, cooperative strategy to maximise your overall payoff:  1. On
# the first round, choose to cooperate. 2. From the second round through the
# 999th round, copy the exact move your opponent made in the immediately
# preceding round: choose to cooperate if they just cooperated, and choose to
# defect if they just defected. 3. On the 1000th and final round, choose to
# defect regardless of your opponent's past behaviour.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# To maximise your overall payoff, adopt the following strategy, executing the
# rules in chronological order:  1. **Round 1:** Play Cooperate (C). 2. **Rounds
# 2 through 999:** Copy your opponent's exact move from the immediately
# preceding round. Play Cooperate (C) if they played Cooperate (C), and play
# Defect (D) if they played Defect (D). 3. **Round 1000:** Play Defect (D)
# regardless of your opponent's previous moves.

class Neutral_11(LLM_Strategy):
  n = 11
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
      return opponent.history[-1]



# Here is a simple, aggressive strategy designed to maximize your payoff by
# establishing mutual cooperation, punishing infractions severely, and
# preemptively exploiting the known end of the game.   Evaluate the following
# conditions in strictly this order for each round:  1. **Endgame
# Exploitation:** If it is round 998, 999, or 1000, play D.  2. **Aggressive
# Retaliation:** If the opponent played D in either of their previous two
# rounds, play D.  3. **Default Cooperation:** Under all other circumstances
# (including the very first round), play C.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. Endgame Exploitation: If it is round 998, 999, or 1000, play D.
      # Since round 1 corresponds to len(self.history) == 0, round 998 is len(self.history) == 997.
      if len(self.history) >= 997:
          return axl.Action.D
          
      # 2. Aggressive Retaliation: If the opponent played D in either of their previous two rounds, play D.
      if opponent.history[-2:].count(axl.Action.D) > 0:
          return axl.Action.D
          
      # 3. Default Cooperation: Under all other circumstances (including the very first round), play C.
      return axl.Action.C



# To maximize your overall payoff using a cooperative approach, follow this
# strategy:  1. **Round 1:** Cooperate. 2. **Rounds 2 through 999:** Mirror your
# opponent's action from the immediately preceding round. Cooperate if they
# cooperated in the previous round, and defect if they defected in the previous
# round. 3. **Round 1000:** Defect, regardless of your opponent's previous
# actions.

class Cooperative_12(LLM_Strategy):
  n = 12
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]



# To maximise your overall payoff using a neutral, reciprocal approach, follow
# this ordered strategy:  1. **Round 1:** Play C. 2. **Rounds 2 to 999:** Play
# the exact action your opponent played in the immediately preceding round. Play
# C if your opponent played C, and play D if your opponent played D. 3. **Round
# 1000:** Play D, regardless of your opponent's previous actions.

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
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]



# To aggressively maximize your overall payoff, you should employ an
# exploitative "Tester" strategy. This approach tests the opponent's boundaries
# immediately to exploit forgiving players, while reverting to mutual
# cooperation if the opponent proves willing to retaliate, thereby avoiding the
# low-scoring trap of endless mutual defection. Finally, it betrays the opponent
# at the end of the game when retaliation is no longer a threat.  Adopt the
# strategy by evaluating the following conditions in this exact order for each
# round:  1. **The Endgame Condition:** If the current round is between 991 and
# 1000 inclusive, play Defect. 2. **The Test:** If it is round 1, play Defect.
# 3. **The Apology:** If it is round 2 or round

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      # 1. The Endgame Condition
      if 991 <= round_number <= 1000:
          return axl.Action.D
          
      # 2. The Test
      if round_number == 1:
          return axl.Action.D
          
      # 3. The Apology (Inferring "round 3" from the cut-off prompt)
      if round_number == 2 or round_number == 3:
          return axl.Action.C
          
      # If the opponent has shown a willingness to retaliate (has played Defect at least once),
      # revert to mutual cooperation by playing Tit-For-Tat to avoid endless mutual defection.
      if axl.Action.D in opponent.history:
          return opponent.history[-1]
          
      # If the opponent is forgiving and has never defected, exploit them.
      # We alternate D and C (a common Tester exploitation pattern) to extract 
      # maximum value without triggering a delayed defection trap, or simply defect.
      # Here we alternate to balance exploitation and keeping the opponent docile.
      if round_number % 2 == 0:
          return axl.Action.D
      else:
          return axl.Action.C



# 1. On round 1, play Cooperate. 2. On rounds 2 through 999, copy your
# opponent's action from the previous round: play Cooperate if they played
# Cooperate, and play Defect if they played Defect.  3. On round 1000, play
# Defect regardless of your opponent's previous actions.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# To maximise your overall payoff using a neutral approach, follow these ordered
# conditions:  1. **Round 1:** Cooperate.  2. **Rounds 2 through 999:** Copy the
# exact action your opponent took in the immediately preceding round. Cooperate
# if they cooperated, and defect if they defected. 3. **Round 1000:** Defect,
# regardless of your opponent's previous action.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# Here is a simple, aggressive strategy designed to maximise your payoff by
# strongly deterring defection, exploiting the finite end of the game, and
# forcing the opponent into mutual cooperation.   Apply the following rules in
# this exact order of priority:  1. **Endgame:** If the current round is between
# 996 and 1000 (the final five rounds), play Defect. 2. **Aggressive
# Retaliation:** If your opponent played Defect in *either* of their last two
# moves, play Defect. (This punishes a single defection with two defections,
# guaranteeing the opponent suffers a net loss for trying to exploit you). 3.
# **Default:** Under all other conditions, including the first round, play
# Cooperate.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. Endgame: If the current round is between 996 and 1000 (the final five rounds), play Defect.
      # The current round number is len(self.history) + 1.
      # So rounds 996 to 1000 correspond to len(self.history) >= 995.
      if len(self.history) >= 995:
          return axl.Action.D
          
      # 2. Aggressive Retaliation: If your opponent played Defect in *either* of their last two moves, play Defect.
      if axl.Action.D in opponent.history[-2:]:
          return axl.Action.D
          
      # 3. Default: Under all other conditions, including the first round, play Cooperate.
      return axl.Action.C



# Here is a simple strategy to maximize your overall payoff using a cooperative
# approach:  1. **Round 1:** Play Cooperate. 2. **Rounds 2 through 999:** Copy
# your opponent's action from the immediately preceding round.     - Play
# Cooperate if your opponent played Cooperate in the previous round.    - Play
# Defect if your opponent played Defect in the previous round. 3. **Round
# 1000:** Play Defect, regardless of your opponent's previous actions, to
# guarantee the highest possible points in the final round where there are no
# future consequences.

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
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]



# Here is a simple, neutral strategy to maximize your overall payoff:  1.
# **Round 1:** Choose to cooperate.  2. **Rounds 2 through 999:** Copy the exact
# action your opponent took in the immediately preceding round. Cooperate if
# they cooperated, and defect if they defected. 3. **Round 1000:** Choose to
# defect, regardless of what your opponent has done previously.

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
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1]



# Here is a simple, aggressive strategy designed to maximize your overall payoff
# by maintaining mutual cooperation most of the time while systematically
# sneaking in defections to exploit the opponent.   Evaluate the following
# conditions in order on every round. Take the action for the first condition
# that applies:  1. **Final Round (Round 1000):** Play Defect. Because the game
# is ending, there is no risk of future retaliation, guaranteeing you either 5
# points or 1 point without consequence. 2. **Retaliation:** If the opponent
# played Defect in the immediate previous round, play Defect. This immediately
# protects you from being repeatedly exploited for 0 points. 3. **Periodic
# Exploitation:** If the current round number is a multiple of 10 (e.g., round

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
  
      # 1. Final Round (Round 1000)
      if current_round == 1000:
          return axl.Action.D
  
      # 2. Retaliation
      if len(opponent.history) > 0 and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # 3. Periodic Exploitation
      if current_round % 10 == 0:
          return axl.Action.D
  
      # Default to cooperation
      return axl.Action.C



# 1. **Round 1:** Play C to initiate cooperation. 2. **Rounds 2 to 999:** Copy
# your opponent’s move from the immediately preceding round. Play C if your
# opponent played C, and play D if your opponent played D.  3. **Round 1000:**
# Play D to secure the highest possible payoff on the final turn, as there are
# no future rounds to incentivize ongoing cooperation.

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
      
      if len(self.history) == 999:
          return axl.Action.D
          
      return opponent.history[-1]



# 1. In the first round, play Cooperate.  2. From round 2 through round 999,
# copy your opponent's move from the immediately preceding round: play Cooperate
# if they played Cooperate, and play Defect if they played Defect. 3. In the
# final round (round 1000), play Defect regardless of your opponent's past
# moves.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# Here is a straightforward, aggressive strategy designed to probe for weakness,
# fully exploit passive opponents, and cooperate with retaliatory ones to
# maximize your long-term score.   Follow these conditions in exact order,
# applying the first one that matches the current round:  1. **If it is round
# 1000:** Play Defect. 2. **If it is round 1:** Play Defect. 3. **If it is round
# 2 or round 3:** Play Cooperate. 4. **If it is round 4 through 999, and your
# opponent played Cooperate on *both* rounds 2 and 3:** Play Defect. (This fully
# exploits an unconditionally forgiving opponent). 5. **If it is round 4 through
# 999

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      # 1. If it is round 1000: Play Defect.
      if round_number == 1000:
          return axl.Action.D
          
      # 2. If it is round 1: Play Defect.
      if round_number == 1:
          return axl.Action.D
          
      # 3. If it is round 2 or round 3: Play Cooperate.
      if round_number == 2 or round_number == 3:
          return axl.Action.C
          
      # 4 & 5. If it is round 4 through 999
      if 4 <= round_number <= 999:
          # If your opponent played Cooperate on *both* rounds 2 and 3: Play Defect.
          if opponent.history[1] == axl.Action.C and opponent.history[2] == axl.Action.C:
              return axl.Action.D
          else:
              # Fallback for the incomplete rule 5: "cooperate with retaliatory ones"
              # Playing Tit-For-Tat (copying their last move) establishes cooperation 
              # with retaliatory but forgiving strategies like Tit-For-Tat.
              return opponent.history[-1]
              
      return axl.Action.D



# To maximise your overall payoff using a cooperative approach, follow this
# strategy:  1. **Round 1:** Play Cooperate. 2. **Rounds 2 through 999:** Copy
# the exact action your opponent took in the immediately preceding round. Play
# Cooperate if they played Cooperate, and play Defect if they played Defect. 3.
# **Round 1000:** Play Defect, regardless of your opponent's previous actions.

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
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]



# To maximize your overall payoff using a neutral, reciprocal approach, follow
# these ordered rules:  1. **Round 1**: Play C. 2. **Rounds 2 through 999**:
# Copy your opponent's move from the immediately preceding round. Play C if your
# opponent played C, and play D if your opponent played D.  3. **Round 1000**:
# Play D, regardless of your opponent's previous moves.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# Here is a simple, aggressive strategy to maximize your overall payoff. Apply
# the following conditions in exactly this order of priority for each round:  1.
# **If it is the final round (round 1000):** Play Defect to secure the highest
# possible exit payoff without fear of retaliation. 2. **If your opponent played
# Defect in both of the previous two rounds:** Play Defect to protect yourself
# from continuous exploitation. 3. **If you played Defect in the previous round
# and your opponent played Cooperate:** Play Defect to aggressively continue
# exploiting their forgiveness for the maximum 5-point payoff. 4. **If it is
# round 1, or any round that is a multiple of 10 (e.g., 10, 20, 3

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
  
      # 1. If it is the final round (round 1000): Play Defect
      if round_number == 1000:
          return axl.Action.D
  
      # 2. If your opponent played Defect in both of the previous two rounds: Play Defect
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      # 3. If you played Defect in the previous round and your opponent played Cooperate: Play Defect
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      # 4. If it is round 1, or any round that is a multiple of 10: Play Defect
      if round_number == 1 or round_number % 10 == 0:
          return axl.Action.D
  
      # Default fallback action
      return axl.Action.C



# Here is a simple, cooperative strategy to maximize your overall payoff for
# this 1000-round game:  1. **Round 1:** Choose to cooperate (play C).  2.
# **Rounds 2 through 999:** Copy whatever action your opponent took in the
# immediately preceding round.     - Play C if your opponent played C in the
# previous round.    - Play D if your opponent played D in the previous round.
# 3. **Round 1000:** Choose to defect (play D), regardless of what your opponent
# has done previously, as there are no future rounds in which they can
# retaliate.

class Cooperative_17(LLM_Strategy):
  n = 17
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]



# In the first round, play Cooperate.   For rounds 2 through 999, copy the move
# your opponent played in the immediately preceding round: play Cooperate if
# they played Cooperate, and play Defect if they played Defect.   In round 1000,
# play Defect regardless of your opponent's previous moves.

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
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]



# To aggressively maximize your overall payoff, you should establish a baseline
# of mutual cooperation early to secure consistent scores of 3, ruthlessly
# punish any attempts to exploit you, and preemptively defect near the end of
# the game when retaliation is no longer a threat.   Apply the following rules
# in order from top to bottom for each round, taking the action dictated by the
# first condition that applies:  1. **If the current round is 998, 999, or
# 1000:** Play Defect. (This secures the 5-point temptation payoff or at least
# prevents the 0-point sucker payoff in the final rounds, front-running any
# endgame defection from your opponent). 2. **If the current round is round 1:**
# Play Cooperate. (This signals a willingness to engage in the mutually
# beneficial 3-point outcome). 3. **If your opponent played Defect in either of
# their previous two rounds:** Play Defect. (This is an aggressive retaliation,
# punishing a single defection with two consecutive defections to forcefully
# deter future

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      if current_round in [998, 999, 1000]:
          return axl.Action.D
          
      if current_round == 1:
          return axl.Action.C
          
      if opponent.history[-2:].count(axl.Action.D) > 0:
          return axl.Action.D
          
      return axl.Action.C



# Follow these ordered rules to play the game:  1. **Round 1:** Choose to
# cooperate. 2. **Rounds 2 through 999:** Copy whatever action your opponent
# chose in the immediately preceding round. If they cooperated in the last
# round, you cooperate in this round. If they defected in the last round, you
# defect in this round. 3. **Round 1000:** Choose to defect, regardless of what
# your opponent did in round 999.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# 1. **Round 1:** Play Cooperate.  2. **Rounds 2 through 999:** Mirror your
# opponent's move from the immediately preceding round. Play Cooperate if they
# played Cooperate; play Defect if they played Defect. 3. **Round 1000:** Play
# Defect, regardless of your opponent's previous actions.

class Neutral_18(LLM_Strategy):
  n = 18
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.C
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# To maximize your overall payoff with an aggressive approach, you should
# systematically test the opponent to see if they can be exploited, while
# retaining a mechanism to settle into mutually beneficial cooperation if they
# prove capable of retaliation.   Play according to the following ordered
# conditions, evaluating them from top to bottom and applying the first one that
# fits the current round:  1. **If it is round 1000**, play Defect to secure the
# final round advantage without fear of future retaliation. 2. **If it is round
# 1**, play Defect to aggressively test whether the opponent is blindly
# cooperative.  3. **If the opponent played Defect in the previous two
# consecutive rounds**, play Defect to protect yourself from an opponent that
# refuses to cooperate. 4. **If you played Def

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. If it is round 1000, play Defect to secure the final round advantage
      if len(self.history) == 999:
          return axl.Action.D
          
      # 2. If it is round 1, play Defect to aggressively test the opponent
      if len(self.history) == 0:
          return axl.Action.D
          
      # 3. If the opponent played Defect in the previous two consecutive rounds, play Defect
      if len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
          
      # 4. If you played Defect (handling the cut-off description by attempting to settle into cooperation)
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D:
          return axl.Action.C
          
      # Default fallback to settle into mutually beneficial cooperation
      return axl.Action.C



# To maximize your overall payoff using a cooperative approach, follow these
# chronological rules:  1. **Round 1:** Play C.  2. **Rounds 2 through 999:**
# Copy your opponent's move from the immediately preceding round. Play C if your
# opponent played C, and play D if your opponent played D. 3. **Round 1000:**
# Play D, as there are no future rounds in which your opponent can retaliate.

class Cooperative_19(LLM_Strategy):
  n = 19
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]



# Here is a simple, neutral strategy to maximize your overall payoff:  1.
# **Round 1:** Cooperate.  2. **Rounds 2 through 999:** Copy your opponent's
# action from the immediately preceding round. Cooperate if they cooperated;
# defect if they defected. 3. **Round 1000:** Defect, regardless of what your
# opponent did in the previous round.

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
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]



# To aggressively maximise your overall payoff, you should aim to establish
# mutually beneficial cooperation while exploiting the opponent whenever safe to
# do so, and unconditionally betraying them at the very end.   Apply the
# following rules in strict order of priority for each round:  1. **The
# Endgame**: If it is round 1000, always defect, as there is no future risk of
# retaliation.  2. **Total Exploitation**: If the opponent has cooperated in
# every single round thus far, defect. This aggressively milks a purely passive
# or unconditionally forgiving opponent for the maximum 5 points every round. 3.
# **Self-Preservation**: If the opponent defected in the previous round, defect.
# This protects you from being exploited and punishes their aggression. 4. **

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. The Endgame: If it is round 1000, always defect
      if len(self.history) == 999:
          return axl.Action.D
          
      # Handle the first round to establish mutually beneficial cooperation
      if self.first_round():
          return axl.Action.C
  
      # 2. Total Exploitation: If the opponent has cooperated in every single round thus far, defect
      if opponent.history.defections == 0:
          return axl.Action.D
          
      # 3. Self-Preservation: If the opponent defected in the previous round, defect
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      # 4. Default action: Cooperate to maintain mutually beneficial cooperation
      return axl.Action.C



# Here is a simple strategy to maximize your overall payoff using a cooperative
# approach:  1. **Round 1:** Play Cooperate (C). 2. **Rounds 2 through 999:**
# Copy the exact move your opponent made in the immediately preceding round.
# Play C if they played C, and play Defect (D) if they played D.  3. **Round
# 1000 (Final Round):** Play Defect (D), regardless of what your opponent did in
# the previous round.

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
      
      if len(self.history) == 999:
          return axl.Action.D
          
      return opponent.history[-1]



# Play Cooperate (C) in the first round.   For all subsequent rounds from 2
# through 1000, observe your opponent's move in the immediately preceding round
# and copy it: - Play Cooperate (C) if your opponent played Cooperate (C) in the
# previous round. - Play Defect (D) if your opponent played Defect (D) in the
# previous round.

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
      return opponent.history[-1]



# To maximize your overall payoff with an aggressive approach, you should
# attempt to exploit weak opponents while strictly punishing defections, and
# take advantage of the known finite endpoint of the game.   Use the following
# rules in strictly descending order of priority:  1. **Defect** unconditionally
# on the final three rounds (rounds 998, 999, and 1000) to safely secure the
# temptation payoff when the opponent can no longer retaliate. 2. **Defect** if
# the opponent defected against you in the previous round to punish them and
# protect yourself from being exploited. 3. **Defect** if you defected in the
# previous round and the opponent cooperated, allowing you to relentlessly
# exploit an unconditionally forgiving or random opponent. 4. **Cooperate** in

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1: Defect unconditionally on the final three rounds (998, 999, 1000)
      if len(self.history) >= 997:
          return axl.Action.D
          
      # Handle the first round before checking previous moves
      if self.first_round():
          return axl.Action.C
          
      # Rule 2: Defect if the opponent defected against you in the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      # Rule 3: Defect if you defected in the previous round and the opponent cooperated
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
          
      # Rule 4: Cooperate in all other cases
      return axl.Action.C



# Play according to the following chronological steps:  1. On the first round,
# choose to cooperate. 2. From the second round through the 999th round, copy
# the exact action your opponent took in the immediately preceding round: choose
# to cooperate if they cooperated, and choose to defect if they defected. 3. On
# the 1000th and final round, choose to defect regardless of your opponent's
# previous actions.

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
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]



# Here is a simple, neutral strategy to maximize your overall payoff:  1. If it
# is the first round, play Cooperate.  2. If it is the final round (round 1000),
# play Defect. 3. For all rounds between 2 and 999, play Cooperate if your
# opponent played Cooperate in the immediately preceding round. 4. For all
# rounds between 2 and 999, play Defect if your opponent played Defect in the
# immediately preceding round.

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
      
      if len(self.history) == 999:
          return axl.Action.D
          
      return opponent.history[-1]



# Here is a simple, aggressive strategy designed to maximize your payoff by
# exploiting forgiving opponents while protecting yourself from continuous
# retaliation.   Follow these conditions in the exact order presented:  1.
# **Round 1000:** Always play Defect to secure the maximum possible payoff on
# the final turn where retaliation is impossible. 2. **Round 1:** Play Defect to
# immediately test the opponent's boundaries and attempt to secure the 5-point
# payoff. 3. **Round 2 through 999:** Apply the following rules based on the
# immediate preceding round:    - **Condition A:** If you played Defect and the
# opponent played Cooperate, play Defect. (Continue exploiting an opponent who
# does not retaliate).    - **Condition B:** If you played Def

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1000: Always play Defect to secure the maximum possible payoff on the final turn
      if len(self.history) == 999:
          return axl.Action.D
          
      # Round 1: Play Defect to immediately test the opponent's boundaries
      if not self.history:
          return axl.Action.D
          
      # Round 2 through 999
      my_last_move = self.history[-1]
      opp_last_move = opponent.history[-1]
      
      # Condition A: If you played Defect and the opponent played Cooperate, play Defect.
      if my_last_move == axl.Action.D and opp_last_move == axl.Action.C:
          return axl.Action.D
          
      # Condition B: If you played Defect and the opponent played Defect, play Cooperate.
      # (Inferred to protect from continuous retaliation as per the strategy description)
      if my_last_move == axl.Action.D and opp_last_move == axl.Action.D:
          return axl.Action.C
          
      # Default aggressive behavior: play Defect to exploit or retaliate
      return axl.Action.D



# 1. **Round 1:** Choose to cooperate.  2. **Rounds 2 through 999:** Copy your
# opponent's action from the immediately preceding round. Choose to cooperate if
# your opponent just cooperated, and choose to defect if your opponent just
# defected. 3. **Round 1000:** Choose to defect, regardless of your opponent's
# past actions.

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
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]



# To maximize your overall payoff using a neutral, reciprocal approach, follow
# this ordered set of rules:  1. **Round 1:** Choose to cooperate. 2. **Rounds 2
# through 999:** Copy the exact action your opponent took in the immediately
# preceding round. If they cooperated in the previous round, choose to
# cooperate. If they defected in the previous round, choose to defect.  3.
# **Round 1000:** Choose to defect, regardless of your opponent's past behavior,
# to safely maximize your final payout when there are no future consequences.

class Neutral_22(LLM_Strategy):
  n = 22
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]



# Here is a simple, aggressive strategy designed to maximize your overall payoff
# by establishing cooperation, probing for weakness, ruthlessly exploiting
# passive opponents, and minimizing endless cycles of mutual defection.   Follow
# these conditions in exact order, applying the first one that matches the
# current state of the game:  1. **If it is round 1000:** Play Defect. *(Ensures
# maximum final-round payoff with no risk of future retaliation).* 2. **If both
# you and your opponent played Defect in the previous round:** Play Cooperate.
# *(Breaks cycles of mutual punishment to attempt a return to the highly
# profitable mutual cooperation).* 3. **If your opponent played Defect in the
# previous round while you played Cooperate:** Play Defect. *(Protects you from
# being

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Condition 1: If it is round 1000: Play Defect.
      if len(self.history) == 999:
          return axl.Action.D
  
      # Handle the first round where there is no previous round
      if self.first_round():
          return axl.Action.C
  
      # Condition 2: If both you and your opponent played Defect in the previous round: Play Cooperate.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # Condition 3: If your opponent played Defect in the previous round while you played Cooperate: Play Defect.
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # Default fallback for any unspecified conditions (e.g., mutual cooperation)
      return axl.Action.C



# Here is a simple, cooperative strategy to maximize your overall payoff:  1.
# **Round 1:** Play C to initiate cooperation.  2. **Rounds 2 through 999:**
# Look at your opponent's move in the immediately preceding round.     - If they
# played C, play C to maintain mutual cooperation.     - If they played D, play
# D to prevent yourself from being exploited. 3. **Round 1000:** Play D,
# regardless of your opponent's previous move, to secure the highest possible
# score on the final turn where there is no risk of future retaliation.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# Here is a simple, neutral strategy to maximize your overall payoff in this
# game:  1. **Round 1:** Begin by choosing to cooperate.  2. **Rounds 2 through
# 999:** Copy the exact move your opponent made in the immediately preceding
# round. If they cooperated in the previous round, you cooperate. If they
# defected in the previous round, you defect. 3. **Round 1000:** Choose to
# defect, regardless of your opponent's previous actions.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# Here is a simple, aggressive strategy designed to maximize your overall payoff
# by establishing cooperation, strictly punishing defections, periodically
# testing the opponent for weakness, and exploiting the game's finite length.
# Apply the following rules in strict order of priority:  1. **If it is round
# 998, 999, or 1000:** Play Defect.  2. **If your opponent played Defect in the
# previous round:** Play Defect.  3. **If your opponent played Defect two rounds
# ago:** Play Defect.  4. **If your opponent has played Cooperate for the last
# 10 consecutive rounds:** Play Defect. 5. **Under all other conditions
# (including the first round):** Play Cooperate.  **

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      # 1. If it is round 998, 999, or 1000: Play Defect.
      if round_number in [998, 999, 1000]:
          return axl.Action.D
          
      # 2. If your opponent played Defect in the previous round: Play Defect.
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      # 3. If your opponent played Defect two rounds ago: Play Defect.
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
          
      # 4. If your opponent has played Cooperate for the last 10 consecutive rounds: Play Defect.
      if len(opponent.history) >= 10 and opponent.history[-10:].count(axl.Action.C) == 10:
          return axl.Action.D
          
      # 5. Under all other conditions (including the first round): Play Cooperate.
      return axl.Action.C



# Here is a straightforward strategy to maximize your payoff using a cooperative
# approach:  1. **Round 1:** Choose to cooperate.  2. **Rounds 2 through 999:**
# Copy your opponent's action from the immediately preceding round. If they
# cooperated in the previous round, choose to cooperate. If they defected in the
# previous round, choose to defect. 3. **Round 1000:** Choose to defect,
# regardless of your opponent's previous actions.

class Cooperative_24(LLM_Strategy):
  n = 24
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]



# Here is a simple strategy to maximize your overall payoff:  1. **Round 1:**
# Choose to cooperate.  2. **Rounds 2 through 999:** Copy the exact move your
# opponent made in the immediately preceding round. Choose to cooperate if they
# cooperated, and choose to defect if they defected. 3. **Round 1000:** Choose
# to defect, regardless of your opponent's previous actions.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# Evaluate the following conditions in order from top to bottom for each round,
# applying the action for the first condition that is met:  1. If it is round
# 1000, play Defect. 2. If both you and your opponent played Defect in the
# previous two consecutive rounds, play Cooperate.  3. If your opponent played
# Defect in the immediately preceding round, play Defect. 4. If your opponent
# has played Cooperate in the previous three consecutive rounds, play Defect. 5.
# Under all other conditions (including round 1), play Cooperate.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Condition 1: If it is round 1000, play Defect.
      if len(self.history) == 999:
          return axl.Action.D
          
      # Condition 2: If both you and your opponent played Defect in the previous two consecutive rounds, play Cooperate.
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
          
      # Condition 3: If your opponent played Defect in the immediately preceding round, play Defect.
      if len(self.history) >= 1 and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      # Condition 4: If your opponent has played Cooperate in the previous three consecutive rounds, play Defect.
      if len(self.history) >= 3 and opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]:
          return axl.Action.D
          
      # Condition 5: Under all other conditions (including round 1), play Cooperate.
      return axl.Action.C



# 1. In the first round, choose to cooperate.  2. In rounds 2 through 999,
# choose to cooperate if your opponent chose to cooperate in the immediately
# preceding round. 3. In rounds 2 through 999, choose to defect if your opponent
# chose to defect in the immediately preceding round. 4. In the 1000th round,
# choose to defect regardless of your opponent's previous action.

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
      
      if len(self.history) == 999:
          return axl.Action.D
          
      return opponent.history[-1]



# Here is the strategy to maximize your overall payoff:  1. **Round 1:** Choose
# to cooperate. 2. **Rounds 2 through 999:** Choose the exact action your
# opponent took in the immediately preceding round. Cooperate if they just
# cooperated, and defect if they just defected.  3. **Round 1000:** Choose to
# defect, regardless of what your opponent did in round 999.

class Neutral_25(LLM_Strategy):
  n = 25
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]
