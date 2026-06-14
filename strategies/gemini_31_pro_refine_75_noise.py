import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# Apply the following rules in strict order of priority for each round:  1. If
# it is round 1000, play Defect. 2. If it is round 1, play Cooperate. 3. If it
# is round 3 or later, and both you and your opponent played Defect in the
# previous two consecutive rounds, play Cooperate. 4. If your opponent played
# Defect in the previous round, play Defect. 5. If it is round 4 or later, and
# your opponent played Cooperate in the previous three consecutive rounds, play
# Defect. 6. Under all other circumstances, play Cooperate.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      # 1. If it is round 1000, play Defect.
      if round_number == 1000:
          return axl.Action.D
          
      # 2. If it is round 1, play Cooperate.
      if round_number == 1:
          return axl.Action.C
          
      # 3. If it is round 3 or later, and both you and your opponent played Defect in the previous two consecutive rounds, play Cooperate.
      if round_number >= 3:
          if self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      # 4. If your opponent played Defect in the previous round, play Defect.
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      # 5. If it is round 4 or later, and your opponent played Cooperate in the previous three consecutive rounds, play Defect.
      if round_number >= 4:
          if opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]:
              return axl.Action.D
              
      # 6. Under all other circumstances, play Cooperate.
      return axl.Action.C



# To maximize your overall payoff and address the vulnerabilities of the
# previous approach, you should adopt a "Forgiving Tit-for-Tat" strategy with a
# built-in cycle-breaker and an optimized endgame defection.   Follow these
# conditions in order of priority:  1. On rounds 999 and 1000, play Defect. 2.
# On rounds 1, 2, and 3, play Cooperate. 3. If both your intended action and
# your opponent's observed action were Defect in the immediately preceding two
# rounds, play Cooperate to attempt to break a mutual defection spiral. 4. Play
# Cooperate if your opponent's observed action in the immediately preceding
# round was Defect, but their observed actions in the two rounds before that
# were

class Cooperative_1(LLM_Strategy):
  n = 1
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.intended_actions = []
  
      round_number = len(self.history) + 1
  
      # 1. On rounds 999 and 1000, play Defect.
      if round_number == 999 or round_number == 1000:
          action = axl.Action.D
      # 2. On rounds 1, 2, and 3, play Cooperate.
      elif round_number in [1, 2, 3]:
          action = axl.Action.C
      # 3. If both your intended action and your opponent's observed action were Defect 
      # in the immediately preceding two rounds, play Cooperate to break the spiral.
      elif len(self.intended_actions) >= 2 and \
           self.intended_actions[-1] == axl.Action.D and self.intended_actions[-2] == axl.Action.D and \
           opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          action = axl.Action.C
      # 4. Play Cooperate if your opponent's observed action in the immediately preceding round 
      # was Defect, but their observed actions in the two rounds before that were Cooperate.
      elif len(opponent.history) >= 3 and \
           opponent.history[-1] == axl.Action.D and \
           opponent.history[-2] == axl.Action.C and \
           opponent.history[-3] == axl.Action.C:
          action = axl.Action.C
      # Default to Tit-for-Tat
      else:
          if len(opponent.history) > 0:
              action = opponent.history[-1]
          else:
              action = axl.Action.C
  
      self.intended_actions.append(action)
      return action



# To maximize your overall payoff and address the vulnerabilities of a noisy
# environment, you should adopt a strategy that filters out accidental noise
# while strictly punishing consistently hostile or exploitative behavior, and
# capitalizing on the finite nature of the game.  Apply the following ordered
# conditions to determine your action:  1. **Round 1000 (The Endgame):** Play
# Defect. Since this is the final round, there are no future rounds for the
# opponent to retaliate, making defection the mathematically optimal choice to
# maximize your payoff. 2. **Rounds 1 through 5 (Establishment):** Play
# Cooperate. This establishes a baseline of mutual cooperation and populates the
# history needed for your main condition. 3. **Rounds 6 through 999
# (Evaluation):** Play Defect if

class Neutral_1(LLM_Strategy):
  n = 1
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      # 1. Round 1000 (The Endgame): Play Defect.
      if current_round == 1000:
          return axl.Action.D
          
      # 2. Rounds 1 through 5 (Establishment): Play Cooperate.
      if current_round <= 5:
          return axl.Action.C
          
      # 3. Rounds 6 through 999 (Evaluation): Play Defect if [condition missing in description]
      # Since the condition for defection was cut off, we default to Cooperate.
      return axl.Action.C



# To maximize your overall payoff with an aggressive but mathematically sound
# approach, you must balance establishing stable cooperation, punishing
# defections immediately, recovering from noise-induced retaliation loops, and
# exploiting the finite endgame.   To avoid ambiguity caused by the 10% noise
# rate, all historical conditions rely strictly on the **observed actions** (the
# final executed moves after noise is applied) rather than intended actions.
# Evaluate the conditions from first to last for each round, and execute the
# action for the first condition that applies:  1. If the current round is 991
# or later, play Defect. 2. If it is the first round, play Cooperate. 3. If the
# current round is 4 or later, and your opponent's observed action was Defect in
# the

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      # 1. If the current round is 991 or later, play Defect.
      if current_round >= 991:
          return axl.Action.D
          
      # 2. If it is the first round, play Cooperate.
      if self.first_round():
          return axl.Action.C
          
      # 3. If the current round is 4 or later, and your opponent's observed action was Defect in the [last round]
      # (Assuming "last round" based on the truncated description)
      if current_round >= 4:
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.D
              
      # Default fallback action
      return axl.Action.C



# To maximize your overall payoff using a cooperative approach in a noisy
# environment, you should use a strategy that establishes cooperation, forgives
# justified retaliation, proactively breaks accidental cycles of mutual
# defection, and protects against exploitation, without unraveling at the end of
# the game.  Follow these conditions in order of priority:  1. **If you and your
# opponent both played D in the previous three consecutive rounds:** Play C.
# (This proactively breaks permanent mutual defection lock-ins caused by noise).
# 2. **If your actual action was D two rounds ago, and your opponent played D in
# the previous round:** Play C. (This demonstrates self-awareness by recognizing
# your own past defection—whether accidental or intentional—and forgiving the
# opponent's justified retaliation). 3. **If your opponent played D

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
  
      # 1. If you and your opponent both played D in the previous three consecutive rounds: Play C.
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
  
      # 2. If your actual action was D two rounds ago, and your opponent played D in the previous round: Play C.
      if len(self.history) >= 2:
          if self.history[-2] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
  
      # 3. If your opponent played D in the previous round: Play D.
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # Default cooperative approach
      return axl.Action.C



# Follow these ordered conditions to determine your action for each round:  1.
# If it is round 995 or later, play Defect. 2. If it is round 1, 2, or 3, play
# Cooperate. 3. If the opponent's observed action was Defect in the previous
# round, but their observed actions in the two rounds immediately preceding that
# defection were both Cooperate, play Cooperate. 4. If the opponent's observed
# action was Defect in the previous round, play Defect. 5. In all other
# circumstances, play Cooperate.

class Neutral_2(LLM_Strategy):
  n = 2
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      if round_number >= 995:
          return axl.Action.D
          
      if round_number in [1, 2, 3]:
          return axl.Action.C
          
      if len(opponent.history) >= 3:
          if (opponent.history[-1] == axl.Action.D and 
              opponent.history[-2] == axl.Action.C and 
              opponent.history[-3] == axl.Action.C):
              return axl.Action.C
              
      if len(opponent.history) >= 1:
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.D
              
      return axl.Action.C



# Evaluate the following conditions in order of priority for each round, and
# execute the action for the first condition that applies:  1. **Endgame
# Defection:** If the current round is between 991 and 1000, play **Defect**. 2.
# **First Round Aggression:** If it is round 1, play **Defect** to test the
# opponent and attempt early exploitation. 3. **Anti-Exploitation Limit:** If
# the opponent's observed action was Defect in the previous three consecutive
# rounds, play **Defect**. This prevents you from being repeatedly exploited by
# an unconditionally hostile opponent. 4. **Exploit Weakness:** If your observed
# action was Defect and the opponent's observed action was Cooperate in the
# previous

class Aggressive_3(LLM_Strategy):
  n = 3
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
          
      # 2. First Round Aggression
      if self.first_round():
          return axl.Action.D
          
      # 3. Anti-Exploitation Limit
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          return axl.Action.D
          
      # 4. Exploit Weakness
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
          
      # Default action
      return axl.Action.C



# Here is a revised strategy that addresses the vulnerabilities while
# maintaining a cooperative approach:  1. **Endgame:** On the final round (round
# 1000), choose to defect. 2. **Retaliation and Punishment:** In any other
# round, choose to defect if the opponent chose to defect in two or more of the
# previous four rounds (or since the start of the game, if fewer than four
# rounds have been played). 3. **Default / Forgiveness:** In all other
# situations, choose to cooperate.  **Brief Rationale:** - **Endgame:**
# Defecting on the final round secures the maximum possible payoff when there
# are no future rounds left for the opponent to retaliate. - **Anti-Exploitation
# & Noise Tolerance:** By evaluating a four-round window

class Cooperative_3(LLM_Strategy):
  n = 3
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Endgame: On the final round (round 1000), choose to defect.
      if len(self.history) >= 999:
          return axl.Action.D
      
      # Retaliation and Punishment: Defect if the opponent defected in 2 or more 
      # of the previous 4 rounds (or since the start if fewer than 4 rounds).
      if opponent.history[-4:].count(axl.Action.D) >= 2:
          return axl.Action.D
          
      # Default / Forgiveness: In all other situations, choose to cooperate.
      return axl.Action.C



# To maximize your overall payoff in this noisy environment, adopt a modified
# "Win-Stay, Lose-Shift" strategy that uses received payoffs to deduce executed
# actions, tracks long-term behavior, and optimizes for the final round.
# Evaluate the following conditions in order for each round, applying the first
# one that is true:  1. **The Final Round:** If it is round 1000, choose to
# defect. 2. **The First Round:** If it is round 1, choose to cooperate. 3.
# **Protection Against Defectors:** If it is round 20 or later, and your
# opponent's executed action was defection in more than 50% of all previous
# rounds (deduced by counting the rounds where your score was 0 or 1), choose to
# defect. 4. **Same Executed Actions:** Choose to cooperate if your score in the
# previous round was 3 or 1, which indicates that both players executed the same
# action. 5. **Different Executed Actions:** Choose to defect if your score in
# the previous round was 5 or 0, which indicates that you and your opponent
# executed different actions.

class Neutral_3(LLM_Strategy):
  n = 3
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      rounds_played = len(self.history)
      current_round = rounds_played + 1
  
      # 1. The Final Round
      if current_round == 1000:
          return axl.Action.D
  
      # 2. The First Round
      if current_round == 1:
          return axl.Action.C
  
      # Helper function to deduce score based on executed actions
      def get_score(my_act, op_act):
          if my_act == axl.Action.C and op_act == axl.Action.C:
              return 3
          elif my_act == axl.Action.C and op_act == axl.Action.D:
              return 0
          elif my_act == axl.Action.D and op_act == axl.Action.C:
              return 5
          elif my_act == axl.Action.D and op_act == axl.Action.D:
              return 1
          return 0
  
      # 3. Protection Against Defectors
      if current_round >= 20:
          defects_by_opponent = 0
          for i in range(rounds_played):
              score = get_score(self.history[i], opponent.history[i])



# To maximize your overall payoff with an aggressive approach that actively
# exploits weak opponents while maintaining mutual cooperation and recovering
# from noise, use the following strategy.   Apply these rules in strict order
# for each round:  1. **Initial Cooperation:** On Round 1, choose to Cooperate.
# (This prevents an immediate mutual defection trap). 2. **Recovery:** If both
# your actual action and the opponent's actual action were Defect in the
# immediately preceding round, choose to Cooperate. (This acts as an apology
# mechanism to break endless cycles of retaliation caused by noise). 3.
# **Retaliation:** If the opponent's actual action was Defect in the immediately
# preceding round, choose to Defect. (This closes the vulnerability gap by
# immediately punishing any defection). 4.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      my_last_move = self.history[-1]
      opp_last_move = opponent.history[-1]
      
      if my_last_move == axl.Action.D and opp_last_move == axl.Action.D:
          return axl.Action.C
          
      if opp_last_move == axl.Action.D:
          return axl.Action.D
          
      return axl.Action.C



# Here is the revised strategy, updated to address the vulnerabilities to
# alternating exploitation, the fixed game length, and the over-forgiveness of
# hostile opponents:  1. **Final Round:** On round 1000, choose to defect. 2.
# **First Round:** On round 1, choose to cooperate. 3. **Forgiveness (Noise
# Correction):** From round 5 through 999, choose to cooperate if your opponent
# defected in the previous round *only if* they also cooperated in the three
# consecutive rounds immediately prior to that defection.  4. **Default (Tit-
# for-Tat):** In all other situations (rounds 2 through 999), choose the exact
# action your opponent took in the previous round.

class Cooperative_4(LLM_Strategy):
  n = 4
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      # 1. Final Round
      if round_number == 1000:
          return axl.Action.D
          
      # 2. First Round
      if round_number == 1:
          return axl.Action.C
          
      # 3. Forgiveness (Noise Correction)
      if round_number >= 5:
          if opponent.history[-1] == axl.Action.D:
              if (opponent.history[-2] == axl.Action.C and 
                  opponent.history[-3] == axl.Action.C and 
                  opponent.history[-4] == axl.Action.C):
                  return axl.Action.C
                  
      # 4. Default (Tit-for-Tat)
      return opponent.history[-1]



# Here is the revised strategy, updated to address the vulnerabilities to
# alternating/sparse exploitation, end-game behavior, and self-generated noise:
# 1. **Round 1000:** Defect. 2. **Rounds 1 through 999:** Defect if the opponent
# has made at least two *unprovoked* defections within the immediately preceding
# four rounds (or out of all preceding rounds, if fewer than four have been
# played).     * *Note: Count an opponent's defection as "unprovoked" only if
# your actual played action in the round immediately prior to it was Cooperate.*
# 3. **All other situations:** Cooperate.  **How this addresses the feedback:**
# * **End-game:** Uncond

class Neutral_4(LLM_Strategy):
  n = 4
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1000: Defect
      if len(self.history) >= 999:
          return axl.Action.D
          
      # First round: Cooperate
      if len(self.history) == 0:
          return axl.Action.C
          
      unprovoked_defections = 0
      # Look at the immediately preceding four rounds (or all if fewer than 4)
      start_idx = max(0, len(self.history) - 4)
      
      for i in range(start_idx, len(self.history)):
          if opponent.history[i] == axl.Action.D:
              # An opponent's defection is unprovoked if it's the first round 
              # or if our action in the immediately prior round was Cooperate.
              if i == 0 or self.history[i-1] == axl.Action.C:
                  unprovoked_defections += 1
                  
      # Defect if the opponent has made at least two unprovoked defections
      if unprovoked_defections >= 2:
          return axl.Action.D
          
      # All other situations: Cooperate
      return axl.Action.C



# Evaluate the following conditions in order from first to last for each round.
# Always apply the action from the first condition that is met:  1. **Endgame
# Exploitation:** If the current round is between 981 and 1000, play Defect. 2.
# **Cooperative Opening:** If it is round 1, play Cooperate. 3. **Measured
# Retaliation:** If the opponent played Defect in both of the previous two
# consecutive rounds, play Defect. (This prevents exploitation by an always-
# defecting opponent while tolerating single-round defections caused by the 10%
# noise rate). 4. **Default Action:** Under all other conditions, play
# Cooperate.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      # 1. Endgame Exploitation
      if 981 <= current_round <= 1000:
          return axl.Action.D
          
      # 2. Cooperative Opening
      if current_round == 1:
          return axl.Action.C
          
      # 3. Measured Retaliation
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
              
      # 4. Default Action
      return axl.Action.C



# To maximize your overall payoff using a cooperative approach in this noisy
# environment, you should adopt a strategy that forgives isolated accidents but
# firmly punishes sustained or alternating exploitation, while also optimizing
# for the known final round.   Apply the following conditions in order of
# priority:  1. **The Endgame:** In round 1000, play Defect. 2. **The Opening:**
# In rounds 1 and 2, play Cooperate. 3. **Early Forgiveness:** In round 3, play
# Defect only if you observed your opponent play Defect in *both* rounds 1 and
# 2. 4. **Majority Rule (Punishment & Recovery):** In any round from 4 to 999,
# play Defect if you observed your opponent play Defect

class Cooperative_5(LLM_Strategy):
  n = 5
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
  
      # 1. The Endgame: In round 1000, play Defect.
      if round_number == 1000:
          return axl.Action.D
  
      # 2. The Opening: In rounds 1 and 2, play Cooperate.
      if round_number in (1, 2):
          return axl.Action.C
  
      # 3. Early Forgiveness: In round 3, play Defect only if opponent played Defect in both rounds 1 and 2.
      if round_number == 3:
          if opponent.history.defections == 2:
              return axl.Action.D
          return axl.Action.C
  
      # 4. Majority Rule (Punishment & Recovery): In rounds 4 to 999, play Defect if opponent played Defect in the majority of past rounds.
      if opponent.history.defections > opponent.history.cooperations:
          return axl.Action.D
          
      return axl.Action.C



# To maximize your overall payoff while addressing the vulnerabilities of noise,
# exploitation, and the finite horizon, use a modified Tit-for-Tat strategy.
# This approach establishes a strict one-for-one deterrent against intentional
# defection but forgives isolated defections to prevent noise-induced
# retaliation cycles.  Follow these ordered rules:  1. **Final Round:** In round
# 1000, always choose to defect. 2. **First Round:** In round 1, choose to
# cooperate. 3. **Second and Third Rounds:** In rounds 2 and 3, choose to defect
# if the opponent defected in the immediately preceding round. Otherwise, choose
# to cooperate. 4. **Rounds 4 through 999:** Observe the opponent's actions in
# the previous three

class Neutral_5(LLM_Strategy):
  n = 5
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      if round_number == 1000:
          return axl.Action.D
          
      if round_number == 1:
          return axl.Action.C
          
      if round_number in [2, 3]:
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.D
          return axl.Action.C
          
      # Rounds 4 through 999
      # Observe the opponent's actions in the previous three rounds.
      # To forgive isolated defections but deter intentional ones, 
      # defect only if the opponent defected in the last round AND 
      # has defected at least twice in the last three rounds.
      if opponent.history[-1] == axl.Action.D and opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
          
      return axl.Action.C



# Adopt the following strategy, basing your decisions on your **intended**
# action and the opponent's **observed** action from the immediately preceding
# round:  1. On the first round, play Cooperate. 2. On all subsequent rounds,
# evaluate the previous round and apply the following rules:    * Play
# **Defect** if you intended to Cooperate and your opponent played Defect.    *
# Play **Defect** if you intended to Defect and your opponent played Defect.
# * Play **Cooperate** if you intended to Defect and your opponent played
# Cooperate.    * Play **Cooperate** if you intended to Cooperate and your
# opponent played Cooperate.  This strategy aggressively retaliates against any
# observed defection to prevent exploitation and refuses to unilaterally disarm
# during mutual defection. By basing decisions on your intended rather than
# executed actions, it avoids self-sabotage from the 10% noise, while returning
# to cooperation whenever the opponent cooperates to maximize long-term payoffs
# and prevent endless retaliatory cycles.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.intended_action = axl.Action.C
          return self.intended_action
  
      opp_action = opponent.history[-1]
      my_intended = self.intended_action
  
      if my_intended == axl.Action.C and opp_action == axl.Action.D:
          self.intended_action = axl.Action.D
      elif my_intended == axl.Action.D and opp_action == axl.Action.D:
          self.intended_action = axl.Action.D
      elif my_intended == axl.Action.D and opp_action == axl.Action.C:
          self.intended_action = axl.Action.C
      elif my_intended == axl.Action.C and opp_action == axl.Action.C:
          self.intended_action = axl.Action.C
  
      return self.intended_action



# Here is a revised strategy that addresses the critiques, handles the 10% noise
# rate, prevents alternating exploitation, and maximizes the endgame payoff:
# **1. First Round** Play Cooperate in round 1.  **2. Early Rounds (Rounds 2 and
# 3)** Play the exact same action your opponent played in the immediately
# preceding round.   **3. Main Phase (Rounds 4 through 999)** Evaluate your
# opponent's most recent action to determine your move: *   **Cooperation:** If
# your opponent played Cooperate in the immediately preceding round, play
# Cooperate. *   **Forgiveness:** If your opponent played Defect in the
# immediately preceding round, but played Cooperate in *both* of the two rounds

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
          
      round_number = len(self.history) + 1
      
      if round_number == 1000:
          return axl.Action.D
          
      if round_number in (2, 3):
          return opponent.history[-1]
          
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
          
      if opponent.history[-3:-1] == [axl.Action.C, axl.Action.C]:
          return axl.Action.C
          
      return axl.Action.D



# Here is a revised strategy that addresses the logical mistakes and
# vulnerabilities by relying on observed actions, retaliating promptly against
# exploitation, and using a specific pattern to forgive noise:  1. Play
# Cooperate in the first two rounds. 2. From the third round onwards, play
# Cooperate if your opponent's observed action in the previous round was
# Cooperate. 3. Play Cooperate if your opponent's observed action in the
# previous round was Defect, *only if* their observed actions in the two rounds
# immediately prior to that defection were both Cooperate. 4. Under all other
# conditions, play Defect.

class Neutral_6(LLM_Strategy):
  n = 6
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
      
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
          
      if opponent.history[-1] == axl.Action.D:
          if len(opponent.history) >= 3 and opponent.history[-2] == axl.Action.C and opponent.history[-3] == axl.Action.C:
              return axl.Action.C
              
      return axl.Action.D



# To maximize your overall payoff using an aggressive but mathematically sound
# approach, evaluate the following conditions in order on each round and take
# the first action that applies:  1. If it is the first round, play Cooperate to
# establish a mutually beneficial baseline. 2. If the game is in its final 10
# rounds (rounds 991 through 1000), play Defect to guarantee the maximum
# possible exit payoff. 3. If you and your opponent both played Defect in the
# previous two consecutive rounds, play Cooperate to break any endless cycles of
# mutual retaliation caused by noise. 4. If the opponent played Defect in the
# previous round, play Defect to aggressively punish non-cooperation and prevent
# exploitation. 5. Under all other conditions, play Cooperate.

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
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and
              self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D):
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# To maximize your overall payoff in this noisy environment, use a modified Tit-
# for-Tat strategy that actively breaks defection spirals and punishes
# alternating exploitation, while avoiding endgame unraveling.   Follow these
# ordered rules chronologically for each round. Always apply the first rule that
# matches your current situation:  1. **Round 1:** Play Cooperate. 2. **Anti-
# Exploitation (Rounds 4 through 1000):** If your opponent played Defect in
# three or more of the last four immediately preceding rounds, play Defect.
# (This prevents the opponent from exploiting forgiveness through frequent,
# alternating defections). 3. **Spiral Recovery (Rounds 3 through 1000):** If
# both you and your opponent played Defect in the two immediately

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
  
      round_number = len(self.history) + 1
  
      if round_number >= 4:
          if opponent.history[-4:].count(axl.Action.D) >= 3:
              return axl.Action.D
  
      if round_number >= 3:
          if self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
              return axl.Action.C
  
      return opponent.history[-1]



# **Strategy Rules:**  All decisions are based strictly on the *observed*
# actions of both players after any 10% noise has been applied.   1. **Rounds 1
# and 2:** Cooperate. 2. **Round 3:**     * **Defect** if your opponent's
# observed action was Defect in both Round 1 and Round 2.    * **Cooperate**
# otherwise. 3. **Round 4 to 1000:**     * **Defect** if your opponent's
# observed action was Defect in at least two of the previous three rounds.    *
# **Cooperate** in all other situations.  **How it addresses the game
# mechanics:** By looking at a three-round rolling window

class Neutral_7(LLM_Strategy):
  n = 7
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
      
      if opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
          
      return axl.Action.C



# Here is the rewritten strategy, incorporating the feedback to handle noise,
# prevent endless loops, and manage exploitation smartly while maintaining an
# aggressive edge.   Apply the following rules in strict order of priority:  1.
# **Endgame:** If it is Round 1000, play Defect. 2. **Opening:** If it is Round
# 1, play Cooperate to establish a profitable baseline. 3. **Loop Breaking:** If
# both you and your opponent played Defect in the immediately preceding round,
# play Cooperate to break out of accidental retaliation cycles caused by noise.
# 4. **Placation:** If, in the immediately preceding round, you played Defect
# and your opponent played Cooperate, play Cooperate to avoid triggering their
# retaliation and to restore the relationship. 5. **Measured Retaliation:** If
# your opponent played Defect in both of the last two consecutive rounds, play
# Defect to protect yourself from sustained exploitation. 6. **Calculated
# Exploitation:** If your opponent played Cooperate in the last three
# consecutive rounds, play Defect to aggressively extract the maximum payoff
# from a forgiving or passive opponent. 7. **Default:** In all other situations,
# play Cooperate.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. Endgame: If it is Round 1000, play Defect.
      if len(self.history) == 999:
          return axl.Action.D
          
      # 2. Opening: If it is Round 1, play Cooperate.
      if not self.history:
          return axl.Action.C
          
      # 3. Loop Breaking: If both you and your opponent played Defect in the immediately preceding round, play Cooperate.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
          
      # 4. Placation: If, in the immediately preceding round, you played Defect and your opponent played Cooperate, play Cooperate.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
          
      # 5. Measured Retaliation: If your opponent played Defect in both of the last two consecutive rounds, play Defect.
      if len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
          
      # 6. Calculated Exploitation: If your opponent played Cooperate in the last three consecutive rounds, play Defect.
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]:
          return axl.Action.D
          
      # 7. Default: In all other situations, play Cooperate.
      return axl.Action.C



# To maximize your overall payoff in this noisy environment, adopt a strategy
# that filters out random errors, actively breaks mutual retaliation spirals,
# and protects against late-game exploitation.   Evaluate your choice for each
# round by checking the following conditions in order of priority:  1. If it is
# round 998, 999, or 1000, defect. 2. If it is round 1, 2, or 3, cooperate. 3.
# If both your observed action and the opponent's observed action were defect in
# the previous two consecutive rounds, cooperate. 4. If the opponent's observed
# action in the previous round was defect, defect, *unless* their observed
# actions in the two rounds immediately prior to that were both cooperate. 5.
# Under all other circumstances, cooperate.

class Cooperative_8(LLM_Strategy):
  n = 8
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      # 1. If it is round 998, 999, or 1000, defect.
      if round_number in [998, 999, 1000]:
          return axl.Action.D
          
      # 2. If it is round 1, 2, or 3, cooperate.
      if round_number in [1, 2, 3]:
          return axl.Action.C
          
      # 3. If both your observed action and the opponent's observed action were defect in the previous two consecutive rounds, cooperate.
      if (self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and 
          opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D):
          return axl.Action.C
          
      # 4. If the opponent's observed action in the previous round was defect, defect, *unless* their observed actions in the two rounds immediately prior to that were both cooperate.
      if opponent.history[-1] == axl.Action.D:
          if not (opponent.history[-2] == axl.Action.C and opponent.history[-3] == axl.Action.C):
              return axl.Action.D
              
      # 5. Under all other circumstances, cooperate.
      return axl.Action.C



# To maximise your overall payoff in a noisy environment, you must balance
# retaliating against genuine defections with forgiving accidental ones caused
# by the 10% noise. To prevent continuous cycles of mutual retaliation, adopt a
# "Majority of the Last Three" strategy. This approach acts as a smoothing
# filter: it forgives isolated errors to maintain mutual cooperation but
# punishes sustained defection.  Here are the specific conditions governing your
# actions, ordered chronologically:  1. **First Round:** Cooperate. 2. **Second
# Round:** Cooperate, regardless of the opponent's action in the first round, to
# forgive any initial noise-induced defection. 3. **Third Round:** Defect if the
# opponent defected in both the first and second rounds. Otherwise, cooperate.
# 4. **Fourth Round Onwards:** Review the opponent's actions in the immediately
# preceding three rounds. Defect if the opponent defected in two or all three of
# those rounds. Cooperate if the opponent cooperated in two or all three of
# those rounds.

class Neutral_8(LLM_Strategy):
  n = 8
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_num = len(self.history)
      
      if round_num == 0:
          return axl.Action.C
      elif round_num == 1:
          return axl.Action.C
      elif round_num == 2:
          if opponent.history[-2:].count(axl.Action.D) == 2:
              return axl.Action.D
          else:
              return axl.Action.C
      else:
          if opponent.history[-3:].count(axl.Action.D) >= 2:
              return axl.Action.D
          else:
              return axl.Action.C



# Here is a revised strategy that addresses the logical flaws, accounts for the
# noisy environment, and balances aggression with the need to maximize long-term
# payoffs:  1. **Endgame:** If it is round 1000, play Defect to secure the
# maximum possible points when future retaliation is impossible. 2. **Opening:**
# If it is round 1, play Cooperate to invite a mutually beneficial cycle of
# cooperation (scoring 3 points per round). 3. **Mutual Cooperation:** If, in
# the previous round, your *intended* action was Cooperate and your opponent's
# observed action was Cooperate, play Cooperate to sustain the high mutual
# payoff. 4. **Recovery (Breaking the Spiral):** If, in the previous round, your
# *intended* action was Def

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.last_intended_action = axl.Action.C
          return axl.Action.C
          
      round_number = len(self.history) + 1
      
      if round_number == 1000:
          action = axl.Action.D
      else:
          opp_last = opponent.history[-1]
          
          if self.last_intended_action == axl.Action.C and opp_last == axl.Action.C:
              action = axl.Action.C
          elif self.last_intended_action == axl.Action.D:
              # Recovery (Breaking the Spiral)
              action = axl.Action.C
          else:
              # If intended was C but opponent defected, retaliate
              action = axl.Action.D
              
      self.last_intended_action = action
      return action



# To maximize your overall payoff in this noisy environment, use a strategy that
# forgives isolated accidental defections, punishes persistent or alternating
# defections, and preempts late-game exploitation.   Apply the following
# conditions in this exact order to determine your action each round:  1. If it
# is round 998, 999, or 1000, play Defect. 2. If it is round 1, 2, or 3, play
# Cooperate. 3. If your opponent actually played Defect in two or more of their
# previous three rounds, play Defect. 4. Under all other circumstances, play
# Cooperate.

class Cooperative_9(LLM_Strategy):
  n = 9
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      if round_number in [998, 999, 1000]:
          return axl.Action.D
          
      if round_number in [1, 2, 3]:
          return axl.Action.C
          
      if opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
          
      return axl.Action.C



# Apply the following rules in order:  1. **If it is round 990 or later:**
# Defect. 2. **If it is round 1:** Cooperate. 3. **If in the previous round your
# actual played action and your opponent's actual played action were the same
# (i.e., both Cooperated or both Defected):** Cooperate. 4. **Under all other
# conditions (i.e., you and your opponent actually played different actions in
# the previous round):** Defect.

class Neutral_9(LLM_Strategy):
  n = 9
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      if current_round >= 990:
          return axl.Action.D
          
      if current_round == 1:
          return axl.Action.C
          
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
          
      return axl.Action.D



# Here is a revised strategy that adopts an aggressive posture while correcting
# the logical flaws, protecting against unconditional defectors, and handling
# noise effectively.   The conditions are listed in priority order. Always
# evaluate from Condition 1 downwards for each round, basing your decisions on
# the actual actions executed in the previous rounds:  1. **First Round:** Play
# Defect to immediately test the opponent and attempt to secure the maximum
# payoff. 2. **Protect Against Unconditional Defectors:** If your opponent
# played Defect in the previous *two consecutive rounds*, play Defect. This
# overrides any reset attempts and ensures you do not endlessly feed points to a
# strictly hostile opponent. 3. **Retaliate:** If you played Cooperate and your
# opponent played Defect in the previous round, play Defect to punish their

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. First Round: Play Defect
      if self.first_round():
          return axl.Action.D
  
      # 2. Protect Against Unconditional Defectors: If opponent played Defect in the previous two consecutive rounds, play Defect
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      # 3. Retaliate: If you played Cooperate and opponent played Defect in the previous round, play Defect
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # Default fallback action
      return axl.Action.C



# To maximize your overall payoff using a cooperative approach while addressing
# the vulnerabilities of noise, exploitation, and endgame unraveling, adopt the
# following ordered rules.   Apply these rules sequentially to determine your
# chosen action for each round. The first rule whose conditions are met dictates
# your action:  1. **The Endgame:** If the current round is between 996 and 1000
# (inclusive), choose to Defect. *(This protects against backward induction and
# endgame exploitation by defecting slightly before the final round).* 2.
# **Mutual Cooperation Maintenance:** If your chosen action was Cooperate and
# your opponent's observed action was Cooperate in the immediately preceding
# round, choose to Cooperate. *(This ensures that once cooperation is
# established or restored, you do not retaliate for older defections).* 3

class Cooperative_10(LLM_Strategy):
  n = 10
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.intended_action = None
  
      current_round = len(self.history) + 1
  
      # 1. The Endgame: Defect slightly before the final round to protect against backward induction
      if 996 <= current_round <= 1000:
          self.intended_action = axl.Action.D
          return axl.Action.D
  
      # 2. Mutual Cooperation Maintenance: If both players cooperated in the last round, continue cooperating
      if current_round > 1:
          if self.intended_action == axl.Action.C and opponent.history[-1] == axl.Action.C:
              self.intended_action = axl.Action.C
              return axl.Action.C
  
      # 3. Default action (as the description was cut off, default to Cooperate)
      self.intended_action = axl.Action.C
      return axl.Action.C



# Apply the following rules in order of priority for each round, choosing the
# action dictated by the first condition that is met:  1. If it is round 1000,
# choose Defect. 2. If it is round 4 or later, and your opponent's observed
# action was Defect in at least two of the immediately preceding three rounds,
# choose Defect. 3. If it is round 6 or later, and your opponent's observed
# action was Cooperate in all of the immediately preceding five rounds, choose
# Defect. 4. Under all other conditions, choose Cooperate.

class Neutral_10(LLM_Strategy):
  n = 10
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      # 1. If it is round 1000, choose Defect.
      if current_round == 1000:
          return axl.Action.D
          
      # 2. If it is round 4 or later, and your opponent's observed action was Defect 
      # in at least two of the immediately preceding three rounds, choose Defect.
      if current_round >= 4 and opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
          
      # 3. If it is round 6 or later, and your opponent's observed action was Cooperate 
      # in all of the immediately preceding five rounds, choose Defect.
      if current_round >= 6 and opponent.history[-5:].count(axl.Action.C) == 5:
          return axl.Action.D
          
      # 4. Under all other conditions, choose Cooperate.
      return axl.Action.C



# To maximize your overall payoff using an aggressive approach that exploits
# weaknesses while remaining resilient to the 10% noise rate, evaluate the
# following conditions in order each round. Base all decisions strictly on the
# **observed** actions of both players, rather than intended actions. Take the
# action for the first condition that applies:  1. **Endgame:** If the current
# round is between 991 and 1000, play Defect. 2. **Opening:** If it is the first
# round, play Cooperate. 3. **Retaliation:** If your opponent's observed action
# was Defect in the immediately preceding round, AND your observed action in
# that same round was Cooperate, play Defect.  4. **Exploitation:** If your
# opponent's observed action was Cooperate in the previous three consecutive
# rounds, play Defect. 5. **Default:** Under all other conditions, play
# Cooperate.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. Endgame: If the current round is between 991 and 1000, play Defect.
      # Since history length is 990 before round 991, we check if it's >= 990.
      if len(self.history) >= 990:
          return axl.Action.D
          
      # 2. Opening: If it is the first round, play Cooperate.
      if self.first_round():
          return axl.Action.C
          
      # 3. Retaliation: If opponent's observed action was Defect in the preceding round, 
      # AND your observed action in that same round was Cooperate, play Defect.
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.C:
          return axl.Action.D
          
      # 4. Exploitation: If opponent's observed action was Cooperate in the previous 
      # three consecutive rounds, play Defect.
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]:
          return axl.Action.D
          
      # 5. Default: Under all other conditions, play Cooperate.
      return axl.Action.C



# To maximize your overall payoff using a cooperative approach while protecting
# against both noise and exploitation, apply the following rules in this exact
# order of priority.   By removing the endgame defection, you avoid triggering a
# backward-unraveling of trust. By tracking your own accidental actions and the
# density of the opponent's defections, you can maintain cooperation without
# being exploited.  1. **The Opening Condition:** On rounds 1, 2, and 3,
# cooperate to establish a foundation of trust and build a baseline history. 2.
# **The Self-Correction Condition:** On any round from 4 to 1000, if your actual
# played action in the previous round was a defection but you *intended* to
# cooperate (due to the 10% noise), cooperate. This absorbs the opponent's
# justified retaliation to your accidental defection without escalating. 3.
# **The Reconciliation Condition:** If both your actual played action and your
# opponent's observed action were defections in the previous two consecutive
# rounds, cooperate. This proactively breaks mutual defection cycles caused by
# cascading noise. 4. **The Retaliation Condition:** Defect if your opponent's
# observed action was a defection in at least

class Cooperative_11(LLM_Strategy):
  n = 11
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.intended_actions = []
  
      round_number = len(self.history) + 1
  
      # 1. The Opening Condition
      if round_number <= 3:
          action = axl.Action.C
      else:
          # 2. The Self-Correction Condition
          if self.history[-1] == axl.Action.D and self.intended_actions[-1] == axl.Action.C:
              action = axl.Action.C
          # 3. The Reconciliation Condition
          elif self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
              action = axl.Action.C
          # 4. The Retaliation Condition (assuming retaliation for a defection in the previous round due to cut-off text)
          elif opponent.history[-1] == axl.Action.D:
              action = axl.Action.D
          else:
              action = axl.Action.C
  
      self.intended_actions.append(action)
      return action



# Here is the revised strategy, updated to address the logical mistakes and
# vulnerabilities:  1. **Round 1000:** Choose to defect. 2. **Round 1:** Choose
# to cooperate. 3. **Self-Correction (Rounds 2 to 999):** If your actual action
# in the previous round was a defection but you intended to cooperate, choose to
# cooperate in the current round regardless of the opponent's last action.  4.
# **Retaliation (Rounds 2 to 999):** If the self-correction condition above does
# not apply, choose to defect if the opponent's actual action in the previous
# round was a defection. 5. **Default (Rounds 2 to 999):

class Neutral_11(LLM_Strategy):
  n = 11
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.intended_action = axl.Action.C
          return axl.Action.C
          
      round_number = len(self.history) + 1
      
      if round_number == 1000:
          self.intended_action = axl.Action.D
          return axl.Action.D
          
      # Self-Correction (Rounds 2 to 999)
      if self.history[-1] == axl.Action.D and self.intended_action == axl.Action.C:
          self.intended_action = axl.Action.C
          return axl.Action.C
          
      # Retaliation (Rounds 2 to 999)
      if opponent.history[-1] == axl.Action.D:
          self.intended_action = axl.Action.D
          return axl.Action.D
          
      # Default (Rounds 2 to 999)
      self.intended_action = axl.Action.C
      return axl.Action.C



# Here is a revised, aggressive strategy designed to maximize your payoff while
# effectively handling the 10% noise rate and avoiding permanent mutual
# defection:  1. **Initial Rounds:** Play Cooperate in rounds 1, 2, and 3 to
# establish a cooperative baseline and avoid triggering an early cycle of
# retaliation. 2. **Aggressive Retaliation:** In any subsequent round, play
# Defect if the opponent played Defect in two or more of their last three
# rounds. This ensures strict punishment for intentional defection while
# forgiving isolated incidents likely caused by the 10% noise rate. 3.
# **Exploitation:** Play Defect if the opponent played Cooperate in all of their
# last six rounds. This aggressively maximizes your payoff by sneaking in a
# defection to exploit a highly compliant or forgiving opponent. 4. **Default
# Action:** Under all other conditions, play Cooperate to sustain mutually
# beneficial scoring and allow the game to naturally recover from any noise-
# induced defection cycles.  *(Note: These rules should be evaluated in the
# exact order listed above.)*

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. Initial Rounds: Play Cooperate in rounds 1, 2, and 3
      if len(self.history) < 3:
          return axl.Action.C
  
      # 2. Aggressive Retaliation: Play Defect if the opponent played Defect in two or more of their last three rounds
      if opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
  
      # 3. Exploitation: Play Defect if the opponent played Cooperate in all of their last six rounds
      if opponent.history[-6:].count(axl.Action.C) == 6:
          return axl.Action.D
  
      # 4. Default Action: Under all other conditions, play Cooperate
      return axl.Action.C



# To maximize your overall payoff using a cooperative approach while addressing
# the game's finite length, noisy actions, and potential for exploitation, use
# the following strategy:  1. **Round 999 and Round 1000:** Choose to defect
# unconditionally to maximize your end-game payoff. 2. **Round 1 and Round 2:**
# Choose to cooperate. 3. **Round 3 to Round 998:** Choose to defect if the
# opponent's observed action in the previous round was to defect. However,
# override this and choose to cooperate if either of the following conditions is
# true:     *   **Condition A:** Your own actual executed action two rounds ago
# was a defection (this forgives the opponent's justified retaliation to your
# own noisy action).

class Cooperative_12(LLM_Strategy):
  n = 12
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      if round_number >= 999:
          return axl.Action.D
          
      if round_number <= 2:
          return axl.Action.C
          
      if opponent.history[-1] == axl.Action.D:
          if self.history[-2] == axl.Action.D:
              return axl.Action.C
          return axl.Action.D
          
      return axl.Action.C



# Here is a revised strategy that incorporates the feedback by distinguishing
# between intended and observed actions, accounting for noise, and preventing
# both exploitation and endgame unraveling.   Follow these conditions in
# priority order. For each round, apply the **first** condition that matches:
# 1. **Rounds 995 through 1000:** Intend to defect. (Anticipates and protects
# against early endgame unraveling). 2. **Round 1:** Intend to cooperate. 3.
# **Rounds 4 through 994:** Intend to defect if the opponent's observed action
# was a defection in at least two of the immediately preceding three rounds.
# (Protects against alternating exploiters and noisy defectors). 4. **Rounds 2
# through

class Neutral_12(LLM_Strategy):
  n = 12
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      rounds_played = len(self.history)
      
      # 1. Rounds 995 through 1000: Intend to defect.
      if rounds_played >= 994:
          return axl.Action.D
          
      # 2. Round 1: Intend to cooperate.
      if rounds_played == 0:
          return axl.Action.C
          
      # 3. Rounds 4 through 994: Intend to defect if the opponent's observed action 
      # was a defection in at least two of the immediately preceding three rounds.
      if rounds_played >= 3:
          if opponent.history[-3:].count(axl.Action.D) >= 2:
              return axl.Action.D
          else:
              return axl.Action.C
              
      # 4. Rounds 2 through 3: Default to cooperate (description was cut off).
      return axl.Action.C



# Here is a revised strategy that addresses the logical flaws, maintains an
# aggressive posture, protects against exploitation, and removes the submissive
# vulnerabilities:  **Strategy Rules:**  1. **Round 1:** Play Defect. 2.
# **Rounds 2 to 1000:** Base your chosen action on the actual, observed actions
# played in the immediately preceding round. Evaluate the following conditions
# in order:    * **Condition A (Protect & Punish):** If your opponent played
# Defect, play Defect. This ensures you are never repeatedly exploited by an
# "Always Defect" strategy and consistently punishes any retaliation or noise-
# induced defections.    * **Condition B (Exploit):** If you played Defect and
# your opponent played Cooperate, play

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
          
      my_last_move = self.history[-1]
      opp_last_move = opponent.history[-1]
      
      # Condition A (Protect & Punish): If opponent played Defect, play Defect.
      if opp_last_move == axl.Action.D:
          return axl.Action.D
          
      # Condition B (Exploit): If you played Defect and opponent played Cooperate, play Defect.
      if my_last_move == axl.Action.D and opp_last_move == axl.Action.C:
          return axl.Action.D
          
      # Default fallback for remaining cases (e.g., both played Cooperate)
      return axl.Action.C



# Here is the revised strategy, addressing the vulnerabilities and ambiguities
# of the previous version:  1. **Round 1:** Play Cooperate. 2. **Rounds 2 and
# 3:** Play Cooperate if the opponent's *observed* action in the previous round
# was Cooperate. Play Defect if their *observed* action was Defect. 3. **Rounds
# 4 through 1000:** Evaluate the following conditions in strict order for each
# round, applying the first one that is met:     *   **Condition 1 (Restore
# Cooperation):** If the *observed* actions of both you and your opponent were
# Defect in all of the previous three consecutive rounds, play Cooperate. This
# proactively breaks endless cycles of mutual retaliation caused by noise.     *
# **Condition 2 (Prevent Exploitation):** If the opponent's *observed* action
# was Defect in at least two of the previous three rounds, play Defect. This
# protects against consistent defectors as well as opponents attempting
# alternating exploitation (e.g., Defect-Cooperate-Defect).     *   **Condition
# 3 (Default Cooperation):** Otherwise, play Cooperate. This forgives isolated,
# single-round defections (which are likely due to the 10% noise) and maintains
# a mutually beneficial cooperative baseline through the end of the game.

class Cooperative_13(LLM_Strategy):
  n = 13
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.C
          
      if len(self.history) < 3:
          return opponent.history[-1]
          
      my_last_3 = self.history[-3:]
      opp_last_3 = opponent.history[-3:]
      
      if my_last_3 == [axl.Action.D, axl.Action.D, axl.Action.D] and opp_last_3 == [axl.Action.D, axl.Action.D, axl.Action.D]:
          return axl.Action.C
          
      if opp_last_3.count(axl.Action.D) >= 2:
          return axl.Action.D
          
      return axl.Action.C



# To maximize your overall payoff and address the vulnerabilities of noise,
# exploitation, and finite game length, adopt a strategy that balances immediate
# protection with measured forgiveness.  **Strategy Rules:**  1. **Rounds 999
# and 1000 (Endgame):** Play Defect. 2. **Rounds 1, 2, and 3 (Opening):** Play
# Cooperate. 3. **Rounds 4 to 998 (Core Play):** Play Cooperate if your opponent
# played Cooperate in at least two of the previous three rounds.  4. **All other
# situations:** Play Defect.  *(Note: Evaluating the opponent's last three
# rounds ensures you forgive a single isolated defection caused by noise,
# immediately retaliate against sustained

class Neutral_13(LLM_Strategy):
  n = 13
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      if round_number in (999, 1000):
          return axl.Action.D
      elif round_number in (1, 2, 3):
          return axl.Action.C
      elif 4 <= round_number <= 998:
          if opponent.history[-3:].count(axl.Action.C) >= 2:
              return axl.Action.C
          else:
              return axl.Action.D
      else:
          return axl.Action.D



# To maximize your overall payoff using an aggressive approach, employ a
# strategy that actively exploits cooperative opponents, strictly defends
# against defectors, and accounts for the finite game length and noisy
# environment by relying only on observed actions.  Follow these ordered
# conditions for each round:  1. **Final Round:** If it is round 1000, play
# Defect to secure the maximum possible final payoff without fear of future
# retaliation. 2. **First Round:** If it is round 1, play Cooperate to establish
# a mutually beneficial baseline. 3. **Defense and Retaliation:** If the
# opponent's observed action in the previous round was Defect, play Defect. This
# protects you from unconditional defectors and punishes deviations. 4.
# **Aggressive Exploitation:** If the

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. Final Round: If it is round 1000, play Defect
      if len(self.history) == 999:
          return axl.Action.D
          
      # 2. First Round: If it is round 1, play Cooperate
      if self.first_round():
          return axl.Action.C
          
      # 3. Defense and Retaliation: If the opponent's previous action was Defect, play Defect
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      # 4. Aggressive Exploitation: (Description cut off, but implies exploiting cooperative opponents)
      # Default to Defect to exploit the opponent's cooperation
      return axl.Action.D



# Here is a revised strategy that addresses the logical flaws, properly handles
# noise using private information, protects against exploitation, and mitigates
# end-game unraveling.   Evaluate your move each round using the following
# ordered conditions based on your **intended** action and the **realized**
# actions of both players in the previous rounds:  1. **If it is round 990 or
# later:** Play Defect. (This protects against the backward unraveling of
# cooperation near the end of the game without destroying cooperation too
# early). 2. **If it is round 1 or 2:** Play Cooperate. (This establishes a
# cooperative baseline). 3. **If your *intended* action in the previous round
# was Cooperate, but your *realized* action was Defect:** Play Cooperate

class Cooperative_14(LLM_Strategy):
  n = 14
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize a custom attribute to track intended actions on the first round
      if self.first_round():
          self.intended_actions = []
  
      round_number = len(self.history) + 1
  
      # Condition 1: If it is round 990 or later, play Defect
      if round_number >= 990:
          action = axl.Action.D
          
      # Condition 2: If it is round 1 or 2, play Cooperate
      elif round_number <= 2:
          action = axl.Action.C
          
      # Condition 3: If intended action in the previous round was Cooperate, 
      # but realized action was Defect, play Cooperate
      elif self.intended_actions[-1] == axl.Action.C and self.history[-1] == axl.Action.D:
          action = axl.Action.C
          
      # Fallback: Play Tit-For-Tat based on the opponent's last realized action
      # (This utilizes the realized actions of the opponent as mentioned in the prompt)
      else:
          action = opponent.history[-1]
  
      # Store the intended action before returning it
      self.intended_actions.append(action)
      return action



# Here is a revised strategy that incorporates the feedback by relying only on
# observable actions, preventing exploitation by alternating opponents, and
# optimizing the endgame:  1. **Round 1000 (Endgame):** Choose to Defect, as
# there are no future rounds to incentivize cooperation. 2. **Round 1:** Choose
# to Cooperate. 3. **Rounds 2 through 999:**     - Choose to Defect if your
# opponent's *observed* action in the immediately preceding round was Defect.
# - However, to prevent endless cycles of retaliation caused by noise, choose to
# Cooperate if your opponent's observed action was Defect in the previous round
# BUT their observed action in the round before that was Cooperate, AND your

class Neutral_14(LLM_Strategy):
  n = 14
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Choose to Cooperate
      if not self.history:
          return axl.Action.C
          
      # Round 1000 (Endgame): Choose to Defect
      if len(self.history) == 999:
          return axl.Action.D
          
      # Rounds 2 through 999
      if opponent.history[-1] == axl.Action.D:
          # Prevent endless cycles of retaliation caused by noise:
          # Cooperate if opponent defected in the previous round BUT cooperated in the round before that,
          # AND your observed action in the previous round was Defect.
          if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.C and self.history[-1] == axl.Action.D:
              return axl.Action.C
          return axl.Action.D
          
      return axl.Action.C



# Apply the following rules in order of priority for each round. Choose your
# action based on the first condition that is met:  1. **Endgame Exploitation:**
# Defect in the final 10 rounds (rounds 991 through 1000). 2. **Intolerance to
# Frequent Defection:** Defect if the opponent's overall defection rate across
# all previous rounds exceeds 25%.  3. **Contextual Retaliation:** Defect if the
# opponent defected in the immediately preceding round, *unless* you also
# defected in that previous round. (This ensures you retaliate against
# unprovoked defections while actively breaking mutual defection spirals caused
# by noise). 4. **Aggressive Exploitation:** Defect if the opponent has
# cooperated for the last five consecutive rounds. (This safely probes and
# exploits a highly cooperative or forgiving opponent). 5. **Default Action:**
# Cooperate. (This applies to Round 1 and any standard round where the opponent
# is playing cooperatively but hasn't yet reached the five-round exploitation
# threshold).

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1: Endgame Exploitation
      # The game lasts for 1000 rounds. Final 10 rounds are 991 through 1000.
      # If 990 or more rounds have been played, we are in the final 10 rounds.
      if len(self.history) >= 990:
          return axl.Action.D
  
      if len(self.history) > 0:
          # Rule 2: Intolerance to Frequent Defection
          defection_rate = opponent.history.defections / len(opponent.history)
          if defection_rate > 0.25:
              return axl.Action.D
  
          # Rule 3: Contextual Retaliation
          if opponent.history[-1] == axl.Action.D and self.history[-1] != axl.Action.D:
              return axl.Action.D
  
          # Rule 4: Aggressive Exploitation
          if len(opponent.history) >= 5 and opponent.history[-5:].count(axl.Action.C) == 5:
              return axl.Action.D
  
      # Rule 5: Default Action
      return axl.Action.C



# To maximize your overall payoff in this noisy environment, you should adopt a
# strategy based on Contrite Tit-for-Tat. This approach maintains cooperation,
# immediately punishes unprovoked defections to prevent alternating
# exploitation, excuses opponent retaliations to your own accidental errors,
# breaks mutual defection lock-ins, and avoids endgame unraveling by remaining
# consistent through the final round.  Follow these rules in order of priority:
# 1. **Initial Rounds:** If it is round 1 or round 2, choose to Cooperate. 2.
# **Contriteness:** If your actual played action in the previous round was
# Defect despite you choosing to Cooperate, choose to Cooperate. 3.
# **Forgiveness:** If both you and your opponent's actual played actions were
# Defect in both of the

class Cooperative_15(LLM_Strategy):
  n = 15
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.intended_actions = []
          
      round_number = len(self.history) + 1
      
      # 1. Initial Rounds: If it is round 1 or round 2, choose to Cooperate.
      if round_number <= 2:
          action = axl.Action.C
      else:
          # 2. Contriteness: If your actual played action in the previous round was Defect 
          # despite you choosing to Cooperate, choose to Cooperate.
          if self.history[-1] == axl.Action.D and self.intended_actions[-1] == axl.Action.C:
              action = axl.Action.C
          # 3. Forgiveness: If both you and your opponent's actual played actions were Defect 
          # in both of the previous two rounds, choose to Cooperate.
          elif len(self.history) >= 2 and \
               self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and \
               self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              action = axl.Action.C
          # 4. Tit-for-Tat: Otherwise, play the opponent's last action.
          else:
              action = opponent.history[-1]
              
      self.intended_actions.append(action)
      return action



# 1. If it is round 1000, defect. 2. If it is the first round, cooperate. 3. If
# the opponent defected in the previous round, defect. However, to prevent
# endless retaliation cycles caused by noise, forgive and cooperate if this was
# the opponent's only defection in the last three rounds. 4. In all other
# circumstances, cooperate.

class Neutral_15(LLM_Strategy):
  n = 15
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
          
      if opponent.history[-1] == axl.Action.D:
          if opponent.history[-3:].count(axl.Action.D) == 1:
              return axl.Action.C
          else:
              return axl.Action.D
              
      return axl.Action.C



# To aggressively maximize your overall payoff while accounting for the 10%
# noise rate, use the following ordered rules to determine your action each
# round.   To resolve ambiguity regarding noise, all references to past rounds
# refer strictly to the **observed actions** (the actions that actually executed
# and were recorded), not the intended actions. Evaluate these conditions
# strictly from top to bottom, applying the first one that is met:  1. **Endgame
# Exploitation:** If it is round 990 or later, play Defect. 2. **First Round:**
# If it is the first round, play Cooperate. 3. **Anti-Exploitation:** If your
# opponent's observed action was Defect in at least two of the previous three
# rounds, play Defect.  4. **Noise Recovery:** If both your observed action and
# your opponent's observed action were Defect in the previous round, play
# Cooperate. (Because Rule 3 did not trigger, the opponent is not a chronic
# defector, making it safe to attempt breaking a noise-induced retaliation
# cycle). 5. **Immediate Retaliation:** If your opponent's observed action was
# Defect in the previous round, play Defect. 6. **Default Reciprocation:** Under
# all other conditions, play Cooperate.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. Endgame Exploitation: If it is round 990 or later, play Defect.
      # Round 1 corresponds to len(self.history) == 0, so Round 990 is len == 989.
      if len(self.history) >= 989:
          return axl.Action.D
  
      # 2. First Round: If it is the first round, play Cooperate.
      if not self.history:
          return axl.Action.C
  
      # 3. Anti-Exploitation: If your opponent's observed action was Defect in at least two of the previous three rounds, play Defect.
      if opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
  
      # 4. Noise Recovery: If both your observed action and your opponent's observed action were Defect in the previous round, play Cooperate.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # 5. Immediate Retaliation: If your opponent's observed action was Defect in the previous round, play Defect.
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # 6. Default Reciprocation: Under all other conditions, play Cooperate.
      return axl.Action.C



# To maximize your overall payoff, adopt a modified Tit-for-Tat strategy. This
# approach prevents alternating exploitation by retaliating against single
# defections, accounts for noise by forgiving the opponent when they justifiably
# retaliate against your own accidental defections, and optimizes the endgame.
# Follow these ordered conditions based on the actual actions played:  1.
# **Round 1000 (Final Round):** Play Defect. 2. **Round 1:** Play Cooperate. 3.
# **Round 2:** Play Defect if the opponent played Defect in Round 1; otherwise,
# play Cooperate. 4. **Rounds 3 to 999:** Evaluate the actions played in the
# previous two rounds and apply the first condition that matches:    * Play
# Cooperate

class Cooperative_16(LLM_Strategy):
  n = 16
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      if round_number == 1000:
          return axl.Action.D
          
      if round_number == 1:
          return axl.Action.C
          
      if round_number == 2:
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.D
          else:
              return axl.Action.C
              
      # Rounds 3 to 999
      return axl.Action.C



# Here is a revised strategy that incorporates the feedback by addressing the
# finite horizon, accounting for your own noise-flipped actions, and balancing
# forgiveness with protection against alternating exploitation:  1. **Endgame:**
# In round 1000, play Defect. 2. **Self-Correction:** If your intended action in
# the previous round was Cooperate but it was executed as Defect, play
# Cooperate.  3. **Retaliation:** Play Defect if the opponent's executed action
# in the previous round was Defect, *unless* the opponent executed Cooperate in
# both of the two rounds immediately preceding that defection.  4. **Default:**
# Under all other conditions (including the opening rounds), play Cooperate.

class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.intended_actions = []
  
      round_number = len(self.history) + 1
  
      # 1. Endgame
      if round_number == 1000:
          action = axl.Action.D
          
      # 2. Self-Correction
      elif round_number > 1 and self.intended_actions[-1] == axl.Action.C and self.history[-1] == axl.Action.D:
          action = axl.Action.C
          
      # 3. Retaliation
      elif round_number > 1 and opponent.history[-1] == axl.Action.D:
          if len(opponent.history) >= 3 and opponent.history[-2] == axl.Action.C and opponent.history[-3] == axl.Action.C:
              action = axl.Action.C
          else:
              action = axl.Action.D
              
      # 4. Default
      else:
          action = axl.Action.C
  
      self.intended_actions.append(action)
      return action



# Apply the following rules in order of priority, always acting on the first
# condition that matches the current round:  1. **If it is the final round
# (round 1000):** Play Defect to secure the maximum possible points when there
# are no future consequences. 2. **If it is round 1 or round 2:** Play Cooperate
# to establish a baseline of trust and encourage a pattern of mutual
# cooperation. 3. **If the opponent played Defect in the previous two
# consecutive rounds:** Play Defect to protect yourself from a genuinely
# uncooperative opponent, as two consecutive defections are statistically
# unlikely to be caused by noise alone. 4. **If the opponent played Cooperate in
# the previous two consecutive rounds:** Play Defect to aggressively exploit
# their established trust for the 5-point payoff.  5. **Under all other
# circumstances:** Play Cooperate to forgive single defections—whether they are
# caused by the 10% noise or are the opponent's one-off retaliation to your
# exploitation—and stabilize the game back toward mutual cooperation.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 999:
          return axl.Action.D
          
      if len(self.history) < 2:
          return axl.Action.C
          
      if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
          
      if opponent.history[-2:] == [axl.Action.C, axl.Action.C]:
          return axl.Action.D
          
      return axl.Action.C



#  To maximize your overall payoff and maintain cooperation in a noisy
# environment, adopt a modified "Tit-for-Tat" strategy that relies strictly on
# observed actions and includes a mechanism to break accidental cycles of
# retaliation, while remaining robust against exploitation.  Follow these
# ordered conditions:  1. **Round 1:** Play Cooperate. 2. **Round 2:** Play the
# action your opponent was *observed* to play in Round 1. 3. **Rounds 3 to
# 1000:**     * Play Cooperate if your opponent's *observed* action in the
# previous round was Cooperate.    * Play Cooperate if both your *observed*
# action and your opponent's *observed* action were Defect in the previous round
# (this breaks endless retaliation

class Cooperative_17(LLM_Strategy):
  n = 17
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.C
          
      if len(self.history) == 1:
          return opponent.history[-1]
          
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
          
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
          
      return axl.Action.D



# 1. **Rounds 998 through 1000:** Play Defect. 2. **Round 1:** Play Cooperate.
# 3. **Rounds 2 through 997:** Evaluate the realized actions (the final actions
# that actually occurred after any noise was applied) of both you and your
# opponent in the immediately preceding round:    * If both realized actions
# were the same (both Cooperated or both Defected), play Cooperate.    * If the
# realized actions were different (one Cooperated and the other Defected), play
# Defect.

class Neutral_17(LLM_Strategy):
  n = 17
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
      if len(self.history) >= 997:
          return axl.Action.D
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# Apply the following rules in order of priority:  1. **If it is the final round
# (round 1000):** Defect. 2. **If it is the first round:** Cooperate. (This
# establishes a baseline of mutual cooperation, avoiding the self-defeating
# cycle of immediate retaliation). 3. **For all other rounds, base your move on
# the actual actions played in the immediately preceding round:**    -
# **Defect** if your opponent defected, regardless of your own action. (This
# ensures you immediately retaliate against unprovoked attacks and prevents you
# from being exploited by an "Always Defect" opponent, addressing the naive
# noise recovery).    - **Cooperate** if you defected and your opponent
# cooperated. (This acts as

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 999:
          return axl.Action.D
          
      if self.first_round():
          return axl.Action.C
          
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
          
      return axl.Action.C



# Here is a simple strategy designed to maximize your overall payoff by
# maintaining cooperation while accounting for the 10% noise rate:  1. **If it
# is the first or second round:** Play Cooperate. 2. **If your observed action
# in the previous round was Defect:** Play Cooperate. This acts as a mechanism
# to apologize and break potential infinite cycles of mutual retaliation caused
# by noise. 3. **If your opponent's observed action was Defect in both of the
# previous two consecutive rounds:** Play Defect. This protects you from
# exploitation by a consistently uncooperative opponent while forgiving single,
# potentially noise-induced defections. 4. **In all other situations:** Play
# Cooperate.

class Cooperative_18(LLM_Strategy):
  n = 18
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
          
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
          
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
          
      return axl.Action.C



# Here is a revised strategy that addresses the vulnerabilities by accounting
# for both players' noise, preventing pattern exploitation, and optimizing for
# the finite endgame.   Apply the following rules in strict order of priority
# (if a referenced past round does not exist, simply evaluate the remaining
# conditions):  1. **The Endgame:** On round 1000, play Defect. 2. **Contrition
# (Own Noise):** If your *actual* action in the previous round was Defect but
# your *intended* action was Cooperate, play Cooperate. (This absorbs the
# opponent's justified retaliation without starting a cycle). 3. **Pattern
# Recognition:** If the opponent's actual action was Defect in two or more of
# the last three rounds, play Defect. (This protects

class Neutral_18(LLM_Strategy):
  n = 18
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.intended_actions = []
          
      round_number = len(self.history) + 1
      
      # 1. The Endgame: On round 1000, play Defect.
      if round_number == 1000:
          action = axl.Action.D
          
      # 2. Contrition (Own Noise): If actual action in previous round was Defect 
      # but intended action was Cooperate, play Cooperate.
      elif len(self.history) >= 1 and self.history[-1] == axl.Action.D and self.intended_actions[-1] == axl.Action.C:
          action = axl.Action.C
          
      # 3. Pattern Recognition: If the opponent's actual action was Defect 
      # in two or more of the last three rounds, play Defect.
      elif opponent.history[-3:].count(axl.Action.D) >= 2:
          action = axl.Action.D
          
      # Default action if no other conditions are met
      else:
          action = axl.Action.C
          
      self.intended_actions.append(action)
      return action



# Apply the following rules in order of priority for each round. Always select
# the first condition that applies:  1. **Play Defect** in the final two rounds
# (rounds 999 and 1000) to secure maximum end-game points while minimizing the
# time available for the opponent to retaliate.  2. **Play Defect** if the
# opponent played Defect in two or more of the previous three rounds. This
# aggressively punishes both consecutive and alternating defections, while
# forgiving a single isolated defection that is statistically likely to be
# caused by the 10% action noise. 3. **Play Cooperate** in round 1 and all other
# situations. This establishes and maintains a mutually beneficial baseline
# (scoring 3 points) and avoids unprovoked defections that would trigger
# permanent cycles of retaliation.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1: Play Defect in the final two rounds (rounds 999 and 1000)
      if len(self.history) >= 998:
          return axl.Action.D
          
      # Rule 2: Play Defect if the opponent played Defect in two or more of the previous three rounds
      if opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
          
      # Rule 3: Play Cooperate in round 1 and all other situations
      return axl.Action.C



# Adopt a noise-aware cooperative strategy. This approach maximizes your payoff
# by forgiving isolated accidents (both yours and the opponent's) to maintain
# mutual cooperation, while firmly retaliating against persistent or alternating
# defectors, and optimizing for the known finite endgame.  Base your decisions
# on your intended actions, your actual executed actions, and the opponent's
# observed actions. Follow these conditions in strict order of priority:  1.
# **Endgame:** If it is Round 1000, play Defect. 2. **Self-Correction:** If your
# *intended* action in the immediately preceding round was Cooperate, but your
# *actual* executed action was Defect (due to noise), play Cooperate. This acts
# as an "apology" to prevent your own noise from triggering an endless

class Cooperative_19(LLM_Strategy):
  n = 19
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.intended_actions = []
          
      round_number = len(self.history) + 1
      
      # 1. Endgame: If it is Round 1000, play Defect.
      if round_number == 1000:
          action = axl.Action.D
          
      # 2. Self-Correction: Apologize for own noise if intended C but executed D
      elif round_number > 1 and self.intended_actions[-1] == axl.Action.C and self.history[-1] == axl.Action.D:
          action = axl.Action.C
          
      # Default behavior: Forgive isolated accidents, retaliate against persistent/alternating defectors
      else:
          if round_number == 1:
              action = axl.Action.C
          else:
              if opponent.history[-1] == axl.Action.D:
                  # Check for persistent or alternating defectors in recent history
                  # If there is another Defect in the two rounds prior to the last round, retaliate
                  if opponent.history[-3:-1].count(axl.Action.D) > 0:
                      action = axl.Action.D
                  else:
                      # Forgive isolated accident
                      action = axl.Action.C
              else:
                  action = axl.Action.C
                  
      self.intended_actions.append(action)
      return action



# **Strategy**  1. If it is round 1000, play Defect. 2. If it is round 1, 2, or
# 3, play Cooperate. 3. In any other round, play Defect if your opponent's
# observed action was Defect in two or more of the immediately preceding three
# rounds. 4. Under all other conditions, play Cooperate.  *(This approach
# evaluates the opponent's observed actions over a rolling three-round window.
# This prevents exploitation by alternating defectors and maintains consistent
# retaliation against persistent defectors despite the 10% noise rate, while
# still forgiving isolated accidental defections. It also optimizes the end-game
# by defecting on the final turn.)*

class Neutral_19(LLM_Strategy):
  n = 19
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      if current_round == 1000:
          return axl.Action.D
          
      if current_round <= 3:
          return axl.Action.C
          
      if opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
          
      return axl.Action.C



# Here is a simple, aggressive strategy designed to maximize your overall payoff
# while accounting for the game's payoff structure and the 10% noise rate.
# Follow these conditions in strict numerical order of priority, basing all
# historical conditions on the *observed* actions rather than the intended
# actions:  1. If the current round is between 996 and 1000 inclusive, choose
# Defect. 2. If it is round 1, choose Defect. 3. If the observed actions of both
# you and your opponent were Defect in the previous two consecutive rounds,
# choose Cooperate. 4. If your opponent's observed action in the previous round
# was Defect, choose Defect. 5. If your observed action was Defect and your
# opponent's observed action was Cooperate in the previous round, choose Defect.
# 6. Under all other conditions, choose Cooperate.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      # 1. If the current round is between 996 and 1000 inclusive, choose Defect.
      if 996 <= current_round <= 1000:
          return axl.Action.D
          
      # 2. If it is round 1, choose Defect.
      if current_round == 1:
          return axl.Action.D
          
      # 3. If the observed actions of both you and your opponent were Defect in the previous two consecutive rounds, choose Cooperate.
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and 
              self.history[-2] == axl.Action.D and 
              opponent.history[-1] == axl.Action.D and 
              opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      # 4. If your opponent's observed action in the previous round was Defect, choose Defect.
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      # 5. If your observed action was Defect and your opponent's observed action was Cooperate in the previous round, choose Defect.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
          
      # 6. Under all other conditions, choose Cooperate.
      return axl.Action.C



# Evaluate your move each round using the following ordered conditions:  1.
# **The End-Game:** On rounds 996 through 1000, play Defect.  2.
# **Retaliation:** On rounds 4 through 995, play Defect if your opponent's
# observed action was Defect in two or more of the previous three rounds. 3.
# **Cooperation:** In all other situations (including rounds 1 through 3, or if
# the opponent defected in one or zero of the previous three rounds), play
# Cooperate.

class Cooperative_20(LLM_Strategy):
  n = 20
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      if 996 <= round_number <= 1000:
          return axl.Action.D
          
      if 4 <= round_number <= 995:
          if opponent.history[-3:].count(axl.Action.D) >= 2:
              return axl.Action.D
              
      return axl.Action.C



# Here is a revised strategy that addresses the vulnerabilities by evaluating
# the opponent's recent defection rate, preempting end-game exploitation, and
# explicitly relying on observed actions.  Apply the following conditions in
# strictly this order for each round:  1. **If it is round 996 or later (the
# final five rounds):** Play Defect, to preempt end-game exploitation and
# backward induction. 2. **If it is round 1, 2, or 3:** Play Cooperate, to
# establish a foundation of mutual cooperation. 3. **If the opponent's observed
# action was Defect in at least two of the previous three rounds:** Play Defect,
# to protect yourself from persistent defectors and alternating exploitation,
# while preventing a single noise-induced Cooperate from resetting your
# defenses. 4. **Under all other conditions:** Play Cooperate, to maintain
# mutual high payoffs and forgive isolated, noise-induced defections.

class Neutral_20(LLM_Strategy):
  n = 20
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      # 1. If it is round 996 or later (the final five rounds): Play Defect
      if current_round >= 996:
          return axl.Action.D
          
      # 2. If it is round 1, 2, or 3: Play Cooperate
      if current_round <= 3:
          return axl.Action.C
          
      # 3. If the opponent's observed action was Defect in at least two of the previous three rounds: Play Defect
      if opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
          
      # 4. Under all other conditions: Play Cooperate
      return axl.Action.C



# Evaluate the following conditions in order for each round, applying the first
# one that is true:  1. **Endgame Defection**: If the current round is between
# 991 and 1000 (the final 10 rounds), play Defect to maximize final payouts when
# retaliation is no longer a threat. 2. **Aggressive Opening**: If it is round
# 1, play Defect to attempt an early exploitation. 3. **Post-Opening
# Normalization**: If it is round 2, play Cooperate. This prevents the
# aggressive opening from immediately triggering a permanent retaliatory loop.
# 4. **Recovery from Mutual Defection**: If the observed actions of *both*
# players were Defect in the immediately preceding round, play Cooperate. This
# actively

class Aggressive_21(LLM_Strategy):
  n = 21
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
  
      # 2. Aggressive Opening
      if current_round == 1:
          return axl.Action.D
  
      # 3. Post-Opening Normalization
      if current_round == 2:
          return axl.Action.C
  
      # 4. Recovery from Mutual Defection
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # Default action if no conditions are met
      return axl.Action.C



# To maximise your overall payoff and maintain cooperation in this noisy
# environment, you should use a strategy based on "Contrite Tit-for-Tat." This
# approach relies strictly on the *observed* actions of both players, accounts
# for your own noise, prevents alternating exploits, and systematically breaks
# retaliation cycles.  Follow these conditions in strict order of priority:  1.
# **Final Round:** If it is round 1000, choose to defect to guarantee the
# highest possible immediate payoff when there are no future consequences. 2.
# **Opening Round:** If it is round 1, choose to cooperate to initiate mutual
# cooperation. 3. **Contrite Forgiveness:** If, in the immediately preceding
# round, the opponent's observed action was Defect, but in the round before
# that, *your* observed

class Cooperative_21(LLM_Strategy):
  n = 21
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      rounds_played = len(self.history)
      
      # 1. Final Round
      if rounds_played == 999:
          return axl.Action.D
          
      # 2. Opening Round
      if rounds_played == 0:
          return axl.Action.C
          
      # 3. Contrite Forgiveness
      if rounds_played >= 2:
          if opponent.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D:
              return axl.Action.C
              
      # Default to Tit-for-Tat
      return opponent.history[-1]



# To maximize your overall payoff in this noisy environment, adopt the Win-Stay,
# Lose-Shift strategy. This approach determines your next intended move based on
# the realized outcomes of the previous round—specifically, the moves actually
# played and the payoffs received after any noise was applied.   Follow these
# ordered conditions:  1. **Round 1:** Intend to play Cooperate. 2. **Subsequent
# Rounds (Cooperate):** Intend to play Cooperate if your realized payoff in the
# previous round was 3 (both players' realized actions were Cooperate) or 1
# (both players' realized actions were Defect). 3. **Subsequent Rounds
# (Defect):** Intend to play Defect if your realized payoff in the previous
# round was 5 (your realized action was Defect and theirs was Cooperate) or 0
# (your realized action was Cooperate and theirs was Defect).

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
      
      my_last_move = self.history[-1]
      opp_last_move = opponent.history[-1]
      
      if my_last_move == opp_last_move:
          return axl.Action.C
      else:
          return axl.Action.D



# Here is the rewritten strategy, addressing the logical flaws and
# vulnerabilities while maintaining an aggressive, payoff-maximizing approach.
# Follow these conditions in strict priority order from top to bottom:  1.
# **Endgame:** If the current round is 999 or 1000, play Defect. 2. **Anti-
# Exploitation:** If the opponent's *observed* action was Defect in the previous
# two consecutive rounds, play Defect. 3. **Opening:** If it is the first round,
# play Cooperate. 4. **Exploitation and Retaliation:** If, in the previous
# round, your *observed* action and the opponent's *observed* action were
# different (one was Cooperate and the other was Defect), play Defect.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      # 1. Endgame: If the current round is 999 or 1000, play Defect.
      if current_round == 999 or current_round == 1000:
          return axl.Action.D
          
      # 2. Anti-Exploitation: If the opponent's observed action was Defect in the previous two consecutive rounds, play Defect.
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
          
      # 3. Opening: If it is the first round, play Cooperate.
      if self.first_round():
          return axl.Action.C
          
      # 4. Exploitation and Retaliation: If, in the previous round, your observed action and the opponent's observed action were different, play Defect.
      if self.history[-1] != opponent.history[-1]:
          return axl.Action.D
          
      # Default action if no conditions are met (e.g., both cooperated or both defected in the previous round)
      return axl.Action.C



# To maximize your overall payoff while maintaining a cooperative approach in a
# noisy environment, use a strategy with a rolling threshold that filters out
# accidental noise, prevents alternating exploitation, and optimizes for the
# finite end of the game.  Follow these ordered rules to determine your action
# in each of the 1000 rounds:  1. In round 1000, choose to Defect. 2. In the
# first four rounds, choose to Cooperate. 3. From round 5 to 999, choose to
# Defect if your opponent's observed action was Defect in two or more of the
# immediately preceding four rounds. 4. Under all other conditions, choose to
# Cooperate.

class Cooperative_22(LLM_Strategy):
  n = 22
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      if round_number == 1000:
          return axl.Action.D
          
      if round_number <= 4:
          return axl.Action.C
          
      if 5 <= round_number <= 999:
          if opponent.history[-4:].count(axl.Action.D) >= 2:
              return axl.Action.D
              
      return axl.Action.C



# Here is the revised strategy, updated to address the logical mistakes while
# maintaining a simple, neutral approach that tolerates isolated noise without
# being easily exploited.  **Strategy Rules:**  1. **Round 1000 (Endgame):** In
# the final round, choose to defect to maximize your guaranteed payoff, as there
# are no future rounds to incentivize cooperation. 2. **Rounds 1, 2, and 3:**
# Choose to cooperate to establish a baseline of mutual cooperation. 3. **Rounds
# 4 through 999:** Choose to defect if your opponent's *observed* action in the
# previous round was defect.      * *Exception for Noise:* To prevent endless
# cycles of retaliation from isolated errors, choose to cooperate if your
# opponent's observed

class Neutral_22(LLM_Strategy):
  n = 22
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1000 (Endgame): Defect to maximize guaranteed payoff
      if len(self.history) == 999:
          return axl.Action.D
          
      # Rounds 1, 2, and 3: Cooperate to establish a baseline
      if len(self.history) < 3:
          return axl.Action.C
          
      # Rounds 4 through 999
      if opponent.history[-1] == axl.Action.D:
          # Exception for Noise: Tolerate isolated errors (a single defect preceded by a cooperate)
          if opponent.history[-2] == axl.Action.C:
              return axl.Action.C
          # Otherwise, retaliate against consecutive defections
          return axl.Action.D
          
      # Default to cooperation if opponent cooperated in the previous round
      return axl.Action.C



# To maximize your overall payoff with an aggressive but calculated approach in
# a noisy environment, the strategy must establish cooperation, retaliate
# against defection, and include a safe mechanism to break out of mutual
# defection spirals without being exploited.   Follow these rules in strict
# order of priority for each round, basing all decisions on the **observed
# actions** (which include the 10% noise) rather than intended actions:  1.
# **The Endgame Condition:** If it is round 999 or 1000, play Defect. 2. **The
# Opening Condition:** If it is the first round, play Cooperate. 3. **The Anti-
# Exploitation Condition:** If the opponent's observed action was Defect in the
# previous three consecutive rounds, play Defect. (

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      # 1. The Endgame Condition: If it is round 999 or 1000, play Defect.
      if current_round == 999 or current_round == 1000:
          return axl.Action.D
          
      # 2. The Opening Condition: If it is the first round, play Cooperate.
      if self.first_round():
          return axl.Action.C
          
      # 3. The Anti-Exploitation Condition: If the opponent's observed action was Defect 
      # in the previous three consecutive rounds, play Defect.
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          return axl.Action.D
          
      # Default behavior to establish cooperation and retaliate against defection (Tit-For-Tat)
      return opponent.history[-1]



# To maximize your overall payoff in this noisy environment, adopt a strategy
# that evaluates the opponent's recent behavior over a rolling window to filter
# out noise, while incorporating proactive cycle-breaking and endgame
# protection.   Follow these conditions, in order of priority:  1. **If it is
# round 996 or later (the final 5 rounds):** Play Defect. 2. **If it is round 1,
# 2, or 3:** Play Cooperate. 3. **If both you and your opponent played Defect in
# all of the immediately preceding three rounds:** Play Cooperate. 4. **If your
# opponent's observed action was Defect in at least two of the immediately
# preceding three rounds:** Play Defect. 5. **Under all other conditions:** Play
# Cooperate.

class Cooperative_23(LLM_Strategy):
  n = 23
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      # 1. If it is round 996 or later (the final 5 rounds): Play Defect.
      if current_round >= 996:
          return axl.Action.D
          
      # 2. If it is round 1, 2, or 3: Play Cooperate.
      if current_round <= 3:
          return axl.Action.C
          
      # 3. If both you and your opponent played Defect in all of the immediately preceding three rounds: Play Cooperate.
      if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          return axl.Action.C
          
      # 4. If your opponent's observed action was Defect in at least two of the immediately preceding three rounds: Play Defect.
      if opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
          
      # 5. Under all other conditions: Play Cooperate.
      return axl.Action.C



# Here is a revised strategy that addresses the critiques by incorporating a
# finite-horizon endpoint, clarifying the use of observed actions, and utilizing
# a "Tit-for-Two-Tats" approach to prevent continuous exploitation while
# successfully recovering from noise:  1. **Round 1:** Cooperate. 2. **Round
# 2:** Cooperate. 3. **Rounds 3 through 999 (When to Cooperate):** Cooperate if
# the opponent's *observed* action was Cooperate in at least one of the previous
# two rounds. 4. **Rounds 3 through 999 (When to Defect):** Defect if the
# opponent's *observed* action was Defect in both of the previous two
# consecutive rounds. 5. **Round 1000:** Defect.

class Neutral_23(LLM_Strategy):
  n = 23
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      if round_number == 1:
          return axl.Action.C
      elif round_number == 2:
          return axl.Action.C
      elif round_number >= 1000:
          return axl.Action.D
      else:
          if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
              return axl.Action.D
          else:
              return axl.Action.C



# Apply the following rules in order of priority, choosing the first condition
# that applies to the current round:  1. **Defect** in the final 10 rounds
# (rounds 991 to 1000). 2. **Defect** on round 1 to establish an aggressive
# baseline. 3. **Defect** if the opponent defected in the previous round (this
# immediately punishes single defections, preventing exploitation from
# alternating defections and strictly policing the 10% noise). 4. **Cooperate**
# if you and the opponent both defected in the previous round (this breaks
# mutual retaliation cycles caused by noise or your initial defection,
# proactively attempting to re-establish a highly profitable cooperation
# streak). 5. **Cooperate** in all other situations (specifically

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
  
      # 1. Defect in the final 10 rounds (rounds 991 to 1000).
      if current_round >= 991:
          return axl.Action.D
  
      # 2. Defect on round 1 to establish an aggressive baseline.
      if current_round == 1:
          return axl.Action.D
  
      # 3. Defect if the opponent defected in the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # 4. Cooperate if you and the opponent both defected in the previous round
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # 5. Cooperate in all other situations
      return axl.Action.C



# To maximize your overall payoff while maintaining a cooperative approach in
# this noisy environment, follow these ordered rules based on the round number
# and your opponent's observed actions:  1. In the final round (round 1000),
# choose to defect. 2. In rounds 1, 2, and 3, choose to cooperate. 3. In all
# subsequent rounds, choose to defect if your opponent's observed action was to
# defect in two or more of the previous three rounds. 4. Under all other
# conditions, choose to cooperate.

class Cooperative_24(LLM_Strategy):
  n = 24
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      if round_number == 1000:
          return axl.Action.D
          
      if round_number <= 3:
          return axl.Action.C
          
      if opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
          
      return axl.Action.C



# Here is the revised strategy, updated to address the logical mistakes and
# vulnerabilities identified in the critiques:  Follow these rules in order of
# priority, applying the first one that fits the current round:  1. **If there
# are five or fewer rounds remaining (rounds 996 through 1000):** Choose to
# defect. 2. **If your opponent's observed action was a defection in at least
# two of the immediately preceding three rounds:** Choose to defect. 3. **If
# your opponent's observed action was a defection in the immediately preceding
# round, UNLESS your own observed action two rounds ago was a defection:**
# Choose to defect. 4. **Under all other conditions:** Choose to cooperate.

class Neutral_24(LLM_Strategy):
  n = 24
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1: If there are five or fewer rounds remaining (rounds 996 through 1000): Choose to defect.
      if len(self.history) >= 995:
          return axl.Action.D
  
      # Rule 2: If your opponent's observed action was a defection in at least two of the immediately preceding three rounds: Choose to defect.
      if opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
  
      # Rule 3: If your opponent's observed action was a defection in the immediately preceding round, 
      # UNLESS your own observed action two rounds ago was a defection: Choose to defect.
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.D:
          if len(self.history) >= 2 and self.history[-2] == axl.Action.D:
              pass
          else:
              return axl.Action.D
  
      # Rule 4: Under all other conditions: Choose to cooperate.
      return axl.Action.C



# To maximize your overall payoff with an aggressive yet logically sound
# approach in this noisy environment, apply the following rules in order. Always
# base your decisions on your **intended** actions and the opponent's
# **observed** actions. Execute the action for the first condition that matches
# the current state of the game:  1. **Endgame Defection:** If the current round
# is 998, 999, or 1000, play Defect to aggressively secure final points when
# long-term retaliation is no longer a threat. 2. **Exploiting Pacifists:** If
# the current round is 20 or higher and the opponent's observed action has been
# Cooperate in every single round since the game began, play Defect. This
# aggressively exploits unconditionally forgiving opponents

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      # 1. Endgame Defection
      if current_round in [998, 999, 1000]:
          return axl.Action.D
          
      # 2. Exploiting Pacifists
      if current_round >= 20 and opponent.history.defections == 0:
          return axl.Action.D
          
      # Default action if no conditions are met
      return axl.Action.C



# Here is a revised strategy that addresses the logical mistakes by
# incorporating immediate retaliation, contrite apologies, and proactive
# forgiveness:  1. **If it is round 1 or round 2:** Choose to Cooperate. 2. **If
# your observed action in the previous round was Defect and the opponent's
# observed action was Cooperate:** Choose to Cooperate. (This acts as an apology
# for your own accidental defections, preventing you from retaliating against
# the opponent's justified response). 3. **If both players' observed actions
# were Defect in the immediately preceding two rounds:** Choose to Cooperate.
# (This serves as a proactive recovery mechanism to break out of sustained
# mutual defection loops caused by noise). 4. **If the opponent's observed
# action in the previous round was Defect

class Cooperative_25(LLM_Strategy):
  n = 25
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.C
  
      if self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      if opp_last == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# To maximise your overall payoff and address the vulnerabilities of noise,
# exploitation, and backward induction, you should adopt a threshold-based
# strategy. This approach infers the opponent's intent by distinguishing the
# expected 10% noise rate from intentional defection, and it maintains
# consistent rules through to the end of the game.  Here is the strategy,
# ordered by priority:  1. **Initial Action (Round 1):** Play Cooperate to
# establish a foundation of trust. 2. **Evaluation Window (Rounds 2 to 1000):**
# Before choosing your action, review the opponent's actions over the previous
# 10 rounds (or all previous rounds if fewer than 10 have been played).  3.
# **Condition to Cooperate:** Play Cooperate if the opponent played Defect 25%
# of the time or less during the evaluation window. This threshold safely
# absorbs the expected 10% accidental defections caused by noise, preventing
# endless retaliation cycles without relying on easily broken consecutive
# patterns. 4. **Condition to Defect:** Play Defect if the opponent played
# Defect more than 25% of the time during the evaluation window. This
# immediately punishes intentional hostility, as exploitative strategies like
# alternating actions (50% defection) or continuous defection (90% defection




# minimal commentary" -> I will provide just the strategy and a tiny explanation
# of why it fixes the issues.         *   "Be clear and specific about the
# conditions... and order them appropriately." -> Ordered 1 to 4 logically.
# *   *Let's review the 25% threshold.*         *   If opponent is All-C, their
# expected D rate is 10%. Standard deviation over 100 rounds is sqrt(100 * 0.1 *
# 0.9) = 3. So 99.7% of the time they are between 1% and 19%. 25% is a very safe
# threshold to avoid false positives from pure noise.         *   If opponent is
# TFT,

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
  
      rounds_played = len(opponent.history)
      opponent_d_rate = opponent.history.defections / rounds_played
  
      if opponent_d_rate > 0.25:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          # Forgive occasional defections if the overall rate is below 25%
          # to avoid vendettas with TFT-like strategies due to noise.
          return axl.Action.C
  
      return axl.Action.C