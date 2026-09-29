import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# To aggressively maximise your overall payoff, you should use a "Tester"
# strategy. This approach probes the opponent's responsiveness to exploitation,
# ruthlessly exploits passive players, establishes mutually beneficial
# cooperation with retaliatory players, and secures a final unpunished payout.
# Apply the following rules in strict order:  1. **If it is round 1000:** Play
# Defect. (Secures the maximum final payout without fear of retaliation). 2.
# **If it is round 1:** Play Defect. (Tests the opponent to see if they will
# allow themselves to be exploited). 3. **If it is round 2 and your opponent
# played Defect in round 1:** Play Cooperate. (Apologizes to a retaliatory
# player to prevent an endless cycle of mutual defection). 4. **If your opponent
# has never played Defect in any previous round:** Play Defect. (Continues to
# ruthlessly exploit a passive opponent). 5. **If your opponent played Defect in
# round 1:** Play the move your opponent played in the immediately preceding
# round. (Maintains conditional cooperation with a strong opponent). 6. **Under
# any other circumstances:** Play Defect. (Serves as a default fallback action).

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 999:
          return axl.Action.D
          
      if len(self.history) == 0:
          return axl.Action.D
          
      if len(self.history) == 1 and opponent.history[0] == axl.Action.D:
          return axl.Action.C
          
      if opponent.history.defections == 0:
          return axl.Action.D
          
      if opponent.history[0] == axl.Action.D:
          return opponent.history[-1]
          
      return axl.Action.D



# This is getting complicated.      *   Let's keep it extremely simple and
# directly address the critiques.         Critiques:         1. Backward
# induction (caused by unconditional D in round 1000).         2. Lack of
# forgiveness / Echo effect (caused by strict TFT).         3. Penultimate round
# vulnerability (caused by strict TFT + predictable end).         4. Initial
# sucker's payoff (unavoidable but needs to be managed).          Revised
# Strategy:         1. In round 1, play C.         2. From round 2 to 1000, play
# C if the opponent played C in the previous round.         3. If the opponent
# played D in the previous round, play D, with one exception: if

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
      
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # The exception condition was cut off in the description, 
      # so we default to playing D when the opponent played D.
      return axl.Action.D



# Here is the rewritten strategy taking the feedback into account:  1. In round
# 1 and round 2, play Cooperate. 2. From round 3 through round 1000, evaluate
# your opponent's actions in the immediately preceding two rounds.  3. If your
# opponent played Defect in *both* of those previous two rounds, play Defect to
# retaliate against sustained uncooperative behavior. 4. Under all other
# conditions (if your opponent played Cooperate in either or both of the
# previous two rounds), play Cooperate to forgive isolated defections and
# maintain or restore mutual cooperation.

class Neutral_1(LLM_Strategy):
  n = 1
  attitude = Attitude.NEUTRAL
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



# Apply the following rules in strictly descending order for each round of the
# game. Evaluate from the top and execute the first condition that applies:  1.
# If it is round 1000, defect. 2. If you defected in the immediate previous
# round and the opponent defected in the immediate previous round, cooperate. 3.
# If you defected in the immediate previous round and the opponent cooperated in
# the immediate previous round, defect. 4. If the opponent defected in the
# immediate previous round, defect. 5. If it is round 10, defect. 6. Under all
# other conditions, cooperate.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
  
      # 1. If it is round 1000, defect.
      if current_round == 1000:
          return axl.Action.D
  
      if current_round > 1:
          my_last_move = self.history[-1]
          opp_last_move = opponent.history[-1]
  
          # 2. If you defected in the immediate previous round and the opponent defected in the immediate previous round, cooperate.
          if my_last_move == axl.Action.D and opp_last_move == axl.Action.D:
              return axl.Action.C
  
          # 3. If you defected in the immediate previous round and the opponent cooperated in the immediate previous round, defect.
          if my_last_move == axl.Action.D and opp_last_move == axl.Action.C:
              return axl.Action.D
  
          # 4. If the opponent defected in the immediate previous round, defect.
          if opp_last_move == axl.Action.D:
              return axl.Action.D
  
      # 5. If it is round 10, defect.
      if current_round == 10:
          return axl.Action.D
  
      # 6. Under all other conditions, cooperate.
      return axl.Action.C



# Here is a revised strategy that maintains a genuinely cooperative approach
# throughout the entire game while addressing the logical flaws:  1. **Round
# 1:** Play C to establish a cooperative starting point. 2. **Round 2:** Copy
# your opponent's action from Round 1 (play C if they played C, and play D if
# they played D). 3. **Rounds 3 through 1000:** Choose your action based on the
# following ordered conditions:     * **Condition 1 (Forgiveness):** If you and
# your opponent chose opposite actions in *both* of the previous two rounds
# (e.g., you played C and they played D, followed by you playing D and they
# playing C), play C. This breaks endless "echo" cycles of alternating
# retaliation and attempts

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
          
      if len(self.history) == 1:
          return opponent.history[-1]
          
      # Condition 1 (Forgiveness): If opposite actions were played in both of the previous two rounds
      if self.history[-1] != opponent.history[-1] and self.history[-2] != opponent.history[-2]:
          return axl.Action.C
          
      # Default fallback (Tit-For-Tat) for any remaining conditions not explicitly provided
      return opponent.history[-1]



# Here is a revised strategy that addresses the logical and strategic critiques:
# 1. **Round 1:** Play Cooperate (C). 2. **Rounds 2 through 1000:** Evaluate the
# recent history of the game and apply the following conditions in order to
# determine your move:     * **Condition 1 (Forgiveness):** If the outcomes of
# the immediately preceding two rounds were strictly alternating defections
# (e.g., you played C and they played D in one round, followed by you playing D
# and they playing C in the next), play C. This breaks destructive cycles of
# retaliation while preventing you from being exploited by unconditional
# defectors.     * **Condition 2 (Mirroring):** In all other scenarios, mirror
# your opponent's action from the immediately preceding

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
          
      if len(self.history) >= 2:
          my_prev = self.history[-1]
          op_prev = opponent.history[-1]
          my_prev2 = self.history[-2]
          op_prev2 = opponent.history[-2]
          
          # Condition 1 (Forgiveness): Check for strictly alternating defections
          if (my_prev2 == axl.Action.C and op_prev2 == axl.Action.D and my_prev == axl.Action.D and op_prev == axl.Action.C) or \
             (my_prev2 == axl.Action.D and op_prev2 == axl.Action.C and my_prev == axl.Action.C and op_prev == axl.Action.D):
              return axl.Action.C
              
      # Condition 2 (Mirroring): Mirror opponent's last action
      return opponent.history[-1]



# Apply the following rules in order of priority, applying the first condition
# that matches the current state of the game:  1. **Dynamic Endgame Defection:**
# If the current round is 985 or higher, play Defect. Additionally, if the
# current round is 950 or higher and the opponent played Defect in the previous
# round, play Defect to prevent late-game exploitation. 2. **Initial Move:** If
# it is round 1, play Cooperate. 3. **Cycle Recovery (Apology/Forgiveness):** If
# both you and the opponent played Defect in the immediately preceding round,
# play Cooperate. This breaks infinite mutual defection spirals and provides a
# mechanism to restore a mutually beneficial scoring streak. 4. **Exploiting
# Sucker

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
  
      # 1. Dynamic Endgame Defection
      if current_round >= 985:
          return axl.Action.D
      if current_round >= 950 and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # 2. Initial Move
      if current_round == 1:
          return axl.Action.C
  
      # 3. Cycle Recovery (Apology/Forgiveness)
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # 4. Exploiting Sucker (Description incomplete, defaulting to Cooperate)
      return axl.Action.C



# Here is the revised strategy:  1. In the first round, choose to cooperate. 2.
# In all subsequent rounds, copy the action your opponent took in the
# immediately preceding round: cooperate if they cooperated, and defect if they
# defected. 3. As an exception to the second rule, if the outcomes of the
# immediately preceding two rounds consisted of you and your opponent strictly
# alternating between cooperating and defecting (i.e., you cooperated and they
# defected, followed by you defecting and they cooperating), choose to cooperate
# in the current round to break the cycle of retaliation and attempt to restore
# mutual cooperation.

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
      
      if len(self.history) >= 2:
          my_prev2, my_prev1 = self.history[-2], self.history[-1]
          opp_prev2, opp_prev1 = opponent.history[-2], opponent.history[-1]
          
          # Check if the last two rounds were strictly alternating between C and D
          cycle_1 = (my_prev2 == axl.Action.C and opp_prev2 == axl.Action.D and 
                     my_prev1 == axl.Action.D and opp_prev1 == axl.Action.C)
          cycle_2 = (my_prev2 == axl.Action.D and opp_prev2 == axl.Action.C and 
                     my_prev1 == axl.Action.C and opp_prev1 == axl.Action.D)
                     
          if cycle_1 or cycle_2:
              return axl.Action.C
              
      return opponent.history[-1]



# To maximize your overall payoff using a neutral, reciprocal approach that
# avoids end-game unraveling and prevents continuous defection spirals, follow
# these ordered conditions:  1. In the first round, cooperate. 2. In the second
# round, cooperate if your opponent cooperated in the first round, and defect if
# they defected. 3. In rounds 3 through 1000, cooperate if your opponent
# cooperated in at least one of the two immediately preceding rounds. 4. In
# rounds 3 through 1000, defect only if your opponent defected in both of the
# two immediately preceding rounds.

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
      
      if len(self.history) == 1:
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          else:
              return axl.Action.D
              
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
          
      return axl.Action.C



# Here is a simple, aggressive strategy designed to maximize your overall payoff
# by establishing mutual cooperation, forgiving isolated betrayals to prevent
# endless retaliation loops, and securing a final-round advantage.  Follow these
# conditions in strict order for each round:  1. **If it is Round 1 or Round
# 2:** Play Cooperate.  2. **If it is the final round (Round 1000):** Play
# Defect.  3. **If the opponent has played Defect in both of the previous two
# consecutive rounds:** Play Defect.  4. **Under all other circumstances:** Play
# Cooperate.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
      if len(self.history) == 999:
          return axl.Action.D
      if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
      return axl.Action.C



# Here is a revised, cooperative strategy that incorporates forgiveness and
# removes the endgame defection to maximize overall payoff:  1. On rounds 1 and
# 2, play C. 2. On rounds 3 through 1000, evaluate your opponent's actions in
# the immediately preceding two rounds. 3. If your opponent played D in both of
# those previous two rounds, play D to protect yourself from continuous
# exploitation. 4. Under all other conditions, play C to maintain or restore
# mutual cooperation.

class Cooperative_4(LLM_Strategy):
  n = 4
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



# Here is the revised strategy:  1. On rounds 1 and 2, play Cooperate. 2. On
# rounds 3 through 995, play Defect if your opponent played Defect in both of
# the two immediately preceding rounds. In all other cases, play Cooperate. 3.
# On rounds 996 through 1000, play Defect regardless of your opponent's past
# actions.

class Neutral_4(LLM_Strategy):
  n = 4
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      if round_number <= 2:
          return axl.Action.C
      elif 3 <= round_number <= 995:
          if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
              return axl.Action.D
          else:
              return axl.Action.C
      else:
          return axl.Action.D



# Follow these conditions in order of priority to determine your move for each
# round:  1. **The Endgame:** If it is round 1000, play Defect. 2. **The Opening
# Test:** If it is round 1 or round 2, play Defect. 3. **Exploit the Weak:** If
# the opponent played Cooperate in both round 1 and round 2, play Defect.  4.
# **Defend Against the Hostile:** If the opponent played Defect in both round 1
# and round 2, play Defect. 5. **The Apology (Resetting Retaliators):** If it is
# round 3 or round 4, play Cooperate. (This condition is only reached if the
# opponent played Cooperate in round

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
  
      # 1. The Endgame
      if round_number == 1000:
          return axl.Action.D
  
      # 2. The Opening Test
      if round_number == 1 or round_number == 2:
          return axl.Action.D
  
      # 3. Exploit the Weak
      if len(opponent.history) >= 2 and opponent.history[0] == axl.Action.C and opponent.history[1] == axl.Action.C:
          return axl.Action.D
  
      # 4. Defend Against the Hostile
      if len(opponent.history) >= 2 and opponent.history[0] == axl.Action.D and opponent.history[1] == axl.Action.D:
          return axl.Action.D
  
      # 5. The Apology (Resetting Retaliators)
      if round_number == 3 or round_number == 4:
          return axl.Action.C
  
      # Fallback for any subsequent rounds not covered by the conditions
      return axl.Action.D



# Here is the revised strategy, designed to maximize cooperation while directly
# addressing the vulnerabilities of backward induction, endless retaliation, and
# alternating exploitation:  1. **First Round:** Play C. 2. **Anti-
# Exploitation:** In any round, if your opponent's last three moves were D, C,
# and D (in that order), play D to protect yourself against an alternating
# strategy. 3. **Forgiveness:** If you and your opponent both played D in the
# immediately preceding round, play C to attempt to break the cycle of mutual
# retaliation. 4. **Retaliation:** If your opponent played D in the immediately
# preceding round (and the forgiveness condition above is not met), play D. 5.
# **Cooperation:** In all other situations, play C.

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
  
      # Anti-Exploitation
      if len(opponent.history) >= 3:
          if opponent.history[-3:] == [axl.Action.D, axl.Action.C, axl.Action.D]:
              return axl.Action.D
  
      # Forgiveness
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # Retaliation
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # Cooperation
      return axl.Action.C



# Here is the revised strategy, updated to address the logical vulnerabilities:
# 1. **Rounds 1 and 2:** Play Cooperate. 2. **Rounds 3 through 995:** Play
# Cooperate. However, if the opponent played Defect in *both* of the two
# immediately preceding rounds, play Defect. (This prevents infinite retaliation
# cycles by forgiving single defections, while still protecting you from
# continuous exploitation). 3. **Rounds 996 through 1000:** Play Defect
# unconditionally, regardless of the opponent's previous actions. (This preempts
# late-game exploitation and accounts for backward induction without allowing
# the mutual defection to unravel the entire game).

class Neutral_5(LLM_Strategy):
  n = 5
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      if round_number <= 2:
          return axl.Action.C
          
      if round_number >= 996:
          return axl.Action.D
          
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
          
      return axl.Action.C



# To maximise your overall payoff using an aggressive approach, you should
# actively test the opponent to see if they can be exploited, continuously
# exploit them if they never retaliate, forgive their justified retaliation to
# restore mutual cooperation, and secure the final temptation payoff at the very
# end.  Apply the following rules in order, always using the first condition
# that applies to the current round:  1. **The Endgame Rule:** If it is round
# 1000, play Defect. 2. **The Aggressive Test Rule:** If it is round 2, play
# Defect. 3. **The Exploitation Rule:** If it is round 4 or later, and the
# opponent has *never* played Defect in the entire game, play Defect. 4. **The
# Justified Punishment Rule:**

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      # 1. The Endgame Rule
      if round_number == 1000:
          return axl.Action.D
          
      # 2. The Aggressive Test Rule
      if round_number == 2:
          return axl.Action.D
          
      # 3. The Exploitation Rule
      if round_number >= 4 and opponent.history.defections == 0:
          return axl.Action.D
          
      # 4. The Justified Punishment Rule
      if len(opponent.history) > 0:
          if opponent.history[-1] == axl.Action.D:
              # Forgive justified retaliation: if they defected in response to our defection
              if len(self.history) >= 2 and self.history[-2] == axl.Action.D:
                  return axl.Action.C
              # Punish unjustified defection
              return axl.Action.D
          # Restore/maintain mutual cooperation
          return axl.Action.C
          
      # Default first round action
      return axl.Action.C



# 1. On the first round, choose to cooperate.   2. From the second round through
# the 990th round, choose to cooperate if the opponent cooperated in the
# immediately preceding round.   3. During this same period (rounds 2 through
# 990), if the opponent defected in the immediately preceding round, choose to
# defect. However, forgive an isolated mistake by choosing to cooperate if the
# opponent defected in the preceding round but cooperated in the round prior to
# that.   4. As a strict override to rules 2 and 3, always choose to defect if
# the opponent's total number of defections exceeds 10% of the total rounds
# played so far, protecting you from consistently hostile or exploitative
# strategies.   5. From the 9

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
  
      rounds_played = len(self.history)
      current_round = rounds_played + 1
  
      # Rule 5: From the 991st round to the end, always defect
      if current_round > 990:
          return axl.Action.D
  
      # Rule 4: Strict override, defect if opponent's defections > 10% of rounds played
      if opponent.history.defections > 0.1 * rounds_played:
          return axl.Action.D
  
      # Rule 2: Cooperate if the opponent cooperated in the immediately preceding round
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Rule 3: Forgive an isolated mistake
      if rounds_played >= 2 and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      # Rule 3: Otherwise, defect if the opponent defected in the preceding round
      return axl.Action.D



# Here is the revised strategy, addressing the logical vulnerabilities while
# maintaining a simple, neutral approach:  1. **Round 1:** Play Cooperate to
# initiate a mutually beneficial outcome. 2. **Rounds 2 through 990:** Mirror
# your opponent's action from the immediately preceding round (play Cooperate if
# they played Cooperate, and play Defect if they played Defect). However, if
# both you and your opponent played Defect in the previous round, play Cooperate
# to forgive and break any continuous cycle of retaliation. 3. **Rounds 991
# through 1000:** Strictly mirror your opponent's action from the immediately
# preceding round without the forgiveness rule. Play Cooperate if they played
# Cooperate, and play Defect if they played Def

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
      
      round_number = len(self.history) + 1
      
      if round_number <= 990:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
          return opponent.history[-1]
      
      return opponent.history[-1]



# To maximize your overall payoff using an aggressive approach, you must exploit
# purely cooperative opponents, strictly defend yourself against defectors, and
# secure the final round's points without prematurely signaling your intentions.
# Apply the following rules in strict order for each round:  1. **The Endgame
# Rule:** If it is round 1000, play Defect. (This guarantees you cannot be
# exploited at the end of the game and secures final points without giving the
# opponent time to retaliate). 2. **The Retaliation Rule:** If the opponent
# played Defect in the previous round, play Defect. (This protects you from
# exploitation and immediately punishes hostile behavior). 3. **The Exploitation
# Rule:** If you played Defect in the previous round and the opponent played

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. The Endgame Rule: If it is round 1000, play Defect.
      if len(self.history) == 999:
          return axl.Action.D
          
      if self.first_round():
          return axl.Action.C
          
      # 2. The Retaliation Rule: If the opponent played Defect in the previous round, play Defect.
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      # 3. The Exploitation Rule: If you played Defect in the previous round and the opponent played [Cooperate], play Defect.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
          
      return axl.Action.C



# Here is the revised strategy incorporating the feedback to eliminate backward
# induction, protect against endgame exploitation, and prevent infinite
# retaliation cycles:  1. **Round 1:** Play C to initiate mutual cooperation. 2.
# **Rounds 2 to 1000:** Base your move on your payoff from the immediately
# preceding round to maintain cooperation, punish defection, and allow for
# forgiveness:    * **Cooperate (Play C)** if you and your opponent made the
# same move in the previous round (i.e., both played C or both played D).
# Playing C after mutual cooperation sustains the maximum collective payoff,
# while playing C after mutual defection acts as a forgiveness mechanism to
# break retaliation cycles and attempt to restore cooperation.    * **Defect
# (Play D)** if you and your opponent made different

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
      
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      else:
          return axl.Action.D



# Here is the revised strategy, rewritten to address the logical mistakes and
# vulnerabilities identified in the critiques:  1. **First Round:** Play
# Cooperate on round 1. 2. **Exploitation Test:** On round 11, if your opponent
# has played Cooperate in all 10 previous rounds, play Defect to test if they
# are an unconditional cooperator. 3. **Exploitation Phase:** From round 13
# onwards, if your opponent played Cooperate on round 12 (meaning they failed to
# retaliate against your round 11 defection), play Defect for all remaining
# rounds to maximize your payoff. 4. **Forgiveness (Breaking Cycles):** If the
# last two rounds consisted of alternating opposite moves (e.g., you

class Neutral_7(LLM_Strategy):
  n = 7
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. First Round: Play Cooperate on round 1
      if not self.history:
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      # 2. Exploitation Test: On round 11, if opponent played C in all 10 previous rounds, play D
      if round_number == 11:
          if opponent.history.cooperations == 10:
              return axl.Action.D
  
      # 3. Exploitation Phase: From round 13 onwards, if opponent played C on round 12 
      # (failing to retaliate against our round 11 defection), play D for all remaining rounds
      if round_number >= 13:
          if self.history[10] == axl.Action.D and opponent.history[11] == axl.Action.C:
              return axl.Action.D
  
      # 4. Forgiveness (Breaking Cycles): If the last two rounds consisted of alternating opposite moves
      if len(self.history) >= 2:
          if (self.history[-2] != opponent.history[-2] and 
              self.history[-1] != opponent.history[-1] and 
              self.history[-2] != self.history[-1]):
              return axl.Action.C
  
      # Default behavior: Tit-For-Tat (play opponent's last move)
      return opponent.history[-1]



# Here is a simple, aggressive strategy designed to maximize your overall payoff
# by establishing mutual cooperation, strictly punishing defections, and
# preemptively exploiting the endgame.   Follow these conditions in strict order
# of priority:  1. **Endgame Preemption:** If the current round is 998, 999, or
# 1000, play Defect. This aggressively secures the maximum possible points at
# the end of the game while preempting any late-game defections from your
# opponent. 2. **Punishment:** If your opponent played Defect in the previous
# round, play Defect. This prevents you from being exploited and forces the
# opponent to return to cooperation to score points. 3. **Default Cooperation:**
# Under all other conditions, including Round 1, play Cooperate. This
# establishes and maintains the mutually beneficial scoring loop for the vast
# majority of the game.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Endgame Preemption: If the current round is 998, 999, or 1000, play Defect.
      # The current round number is len(self.history) + 1.
      if len(self.history) >= 997:
          return axl.Action.D
      
      # Punishment: If your opponent played Defect in the previous round, play Defect.
      if len(opponent.history) > 0 and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      # Default Cooperation: Under all other conditions, including Round 1, play Cooperate.
      return axl.Action.C



# Here is the revised strategy incorporating the feedback:  1. **Rounds 1 and
# 2:** Play C to initiate cooperation and establish trust.  2. **Rounds 3
# through 999:** Play C, unless your opponent played D in *both* of the two
# immediately preceding rounds. If they played D twice in a row, play D. This
# forgives isolated defections to prevent a continuous cycle of mutual
# retaliation (a "death spiral"), while still punishing sustained uncooperative
# behavior. 3. **Round 1000:** Play D only if your opponent played D in round
# 999; otherwise, play C. Making your final move conditional rather than an
# unconditional defection maintains your retaliatory threat to the very end.
# Crucially, this prevents the opponent

class Cooperative_8(LLM_Strategy):
  n = 8
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
          
      if len(self.history) == 999:
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.D
          return axl.Action.C
          
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
          
      return axl.Action.C



# To maximize your overall payoff, use the following strategy:  1. On round 1,
# cooperate. 2. For rounds 2 through 997, copy the exact action your opponent
# took in the immediately preceding round. However, to prevent endless cycles of
# retaliation, if both you and your opponent defected in the previous two
# consecutive rounds, cooperate on the next round to attempt to restore mutual
# cooperation. 3. For rounds 998 through 1000, defect unconditionally regardless
# of your opponent's previous actions to protect against endgame exploitation
# and the unraveling of cooperation.

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
          
      if len(self.history) >= 997:
          return axl.Action.D
          
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and
              opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      return opponent.history[-1]



# To maximize your overall payoff with an aggressive approach, this strategy
# begins by cooperating to build trust, probes the opponent early to test their
# responsiveness, exploits them continuously if they fail to retaliate, plays
# strictly retaliatory if they do fight back, and betrays them on the final
# round.  Here is the strategy, ordered by priority (apply the first condition
# that is true):  1. **If it is round 1000:** Play Defect.  2. **If it is round
# 1:** Play Cooperate.  3. **If it is round 2:** Play Defect.  4. **If it is
# round 3 or 4:** Play Cooperate. *(This absorbs any immediate retaliation from
# a Tit-for-Tat opponent and re-establishes

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
      if round_number == 1:
          return axl.Action.C
      if round_number == 2:
          return axl.Action.D
      if round_number == 3 or round_number == 4:
          return axl.Action.C
          
      # Check if the opponent retaliated in round 3 to our round 2 probe
      if opponent.history[2] == axl.Action.D:
          # Opponent fought back, play strictly retaliatory (Tit-for-Tat)
          return opponent.history[-1]
      else:
          # Opponent failed to retaliate, exploit them continuously
          return axl.Action.D



# Here is the revised strategy:  1. **Rounds 1 and 2:** Choose to cooperate. 2.
# **Rounds 3 through 1000:** Review your opponent's actions from the immediately
# preceding two rounds. If your opponent defected in both of those rounds,
# choose to defect. If your opponent cooperated in one or both of those rounds,
# choose to cooperate.

class Cooperative_9(LLM_Strategy):
  n = 9
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



# Here is the revised strategy, addressing the logical flaws by maintaining
# consistent neutrality, eliminating the backward induction vulnerability, and
# introducing a specific forgiveness mechanism to prevent endless retaliation
# loops:  1. **Round 1:** Choose to cooperate. 2. **Round 2:** Choose to
# cooperate if your opponent cooperated in round 1. Choose to defect if they
# defected. 3. **Rounds 3 through 1000:** Determine your action based on your
# opponent's recent behavior using the following prioritized conditions:    *
# **Condition 1 (Reciprocity):** If your opponent cooperated in the immediately
# preceding round, choose to cooperate.    * **Condition 2 (Forgiveness):** If
# your opponent defected in the immediately preceding round, but cooperated in
# the two rounds immediately prior to that, choose to cooperate. This forgives a
# single, isolated defection to prevent a mutual retaliation loop.    *
# **Condition 3 (Retaliation):** If your opponent defected in the immediately
# preceding round and Condition 2 does not apply, choose to defect.

class Neutral_9(LLM_Strategy):
  n = 9
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.C
      
      if len(self.history) == 1:
          return opponent.history[-1]
          
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
          
      if len(self.history) >= 3 and opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.D]:
          return axl.Action.C
          
      return axl.Action.D



# Here is the rewritten strategy, addressing the logical flaws, preventing
# permanent lock-in, and adding a mechanism to recover from mutual defection:
# Follow these rules in order of priority (apply the first condition that
# matches the current round):  1. **If it is round 1000:** Play Defect. 2. **If
# it is round 1:** Play Defect.  3. **If it is round 2 or 3:** Play Cooperate.
# (This appeases retaliatory opponents after your initial probe). 4. **If your
# opponent has played Cooperate in every previous round of the game:** Play
# Defect. (This continuously exploits unconditional cooperators, but immediately
# deactivates if they ever retaliate). 5. **If both you and your opponent played
# Defect in the previous round:** Play Cooperate. (This acts as a forgiveness
# mechanism to break out of destructive mutual defection cycles). 6.
# **Otherwise:** Play whatever your opponent played in the previous round.

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      # 1. If it is round 1000: Play Defect.
      if round_number == 1000:
          return axl.Action.D
          
      # 2. If it is round 1: Play Defect.
      if round_number == 1:
          return axl.Action.D
          
      # 3. If it is round 2 or 3: Play Cooperate.
      if round_number == 2 or round_number == 3:
          return axl.Action.C
          
      # 4. If your opponent has played Cooperate in every previous round of the game: Play Defect.
      if opponent.history.defections == 0:
          return axl.Action.D
          
      # 5. If both you and your opponent played Defect in the previous round: Play Cooperate.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
          
      # 6. Otherwise: Play whatever your opponent played in the previous round.
      return opponent.history[-1]



# To maximize your overall payoff using a cooperative and forgiving approach,
# follow this strategy:  1. **Rounds 1 and 2:** Play C. 2. **Rounds 3 through
# 1000:** Evaluate your opponent's moves from the two immediately preceding
# rounds to determine your next action. 3. **When to Defect:** Play D only if
# your opponent played D in *both* of the two previous rounds.  4. **When to
# Cooperate:** Play C in all other scenarios (i.e., if your opponent played C in
# at least one of the two previous rounds).   This ensures you establish
# cooperation early, maintain it through the end of the game, and forgive single
# defections to prevent endless retaliation cycles, while still protecting
# yourself against an opponent who continuously defects.

class Cooperative_10(LLM_Strategy):
  n = 10
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



# To maximise your overall payoff while addressing the vulnerabilities of strict
# Tit-for-Tat, follow these ordered rules. This strategy maintains a neutral,
# cooperative foundation but incorporates probing to exploit static opponents
# and forgiveness to prevent endless cycles of retaliation.  Evaluate these
# conditions in order each round, applying the first one that matches:  1.
# **Round 1:** Play C. 2. **The Probe (Round 10):** If your opponent has played
# C in all 9 previous rounds, play D to test if they are an unconditional
# cooperator.  3. **Exploit Static Cooperators:** If you are past Round 10 and
# your opponent has *never* played D in the entire game despite your Round 10
# defection, play D. 4. **Forgiveness (Break

class Neutral_10(LLM_Strategy):
  n = 10
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. Round 1: Play C.
      if not self.history:
          return axl.Action.C
          
      current_round = len(self.history) + 1
      
      # 2. The Probe (Round 10): If your opponent has played C in all 9 previous rounds, play D.
      if current_round == 10:
          if opponent.history.defections == 0:
              return axl.Action.D
              
      # 3. Exploit Static Cooperators: If you are past Round 10 and your opponent has *never* played D, play D.
      if current_round > 10:
          if opponent.history.defections == 0:
              return axl.Action.D
              
      # 4. Forgiveness / Base Strategy: Fallback to Tit-for-Tat
      return opponent.history[-1]



# Here is the revised strategy, adjusted to address the logical and strategic
# critiques while maintaining an aggressive, payoff-maximizing approach. Apply
# these rules in the exact order listed, evaluating from top to bottom for each
# round:  1. **Endgame Exploitation:** If the current round is exactly 1000,
# play Defect. 2. **Immediate Retaliation:** If the current round is greater
# than 1 and the opponent played Defect in the immediately preceding round, play
# Defect. 3. **Default Cooperation:** Under all other conditions (including the
# first round), play Cooperate.  **Summary of approach:** This strategy
# establishes a mutually profitable baseline by opening with cooperation. It
# remains aggressive by strictly retaliating against any defection, but limits
# the punishment to a one-for-one response (Tit-for-Tat). This prevents endless
# "death spirals" and allows for immediate reconciliation if the opponent
# returns to cooperation. Finally, it restricts endgame defection to the very
# last round, guaranteeing an unpunished exploitation without prematurely
# destroying the cooperative baseline.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 999:
          return axl.Action.D
      
      if len(self.history) > 0 and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      return axl.Action.C



# Here is the strategy:  1. **Round 1:** Play C. 2. **Rounds 2 through 1000:**
# Copy your opponent's move from the immediately preceding round. Play C if your
# opponent played C, and play D if your opponent played D. 3. **Forgiveness
# Condition:** If copying your opponent's move would result in you playing D for
# a second consecutive round, play C instead. This ensures you retaliate against
# a defection only once before attempting to restore mutual cooperation,
# preventing endless defection loops.

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
      
      # Copy opponent's last move, but apply forgiveness condition
      if opponent.history[-1] == axl.Action.D:
          # If copying would result in playing D for a second consecutive round, play C
          if self.history[-1] == axl.Action.D:
              return axl.Action.C
          else:
              return axl.Action.D
              
      return axl.Action.C



# Here is the revised strategy, ordered chronologically and by condition
# precedence, addressing the identified vulnerabilities:  1. **Round 1:** Play
# Cooperate. 2. **Rounds 2 through 995:** Evaluate the following conditions in
# order and apply the first one that matches:    * If your opponent has played
# Cooperate in the round immediately following an unprovoked defection from you,
# play Defect for all remaining rounds to exploit their unconditional
# cooperation.    * If your opponent has played Cooperate for the last 6
# consecutive rounds, play Defect for one round to test if they are an
# unconditional cooperator.    * If both you and your opponent played Defect in
# the immediately preceding round, play Cooperate to break potential retaliatory
# loops.    * Otherwise,

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
  
      round_number = len(self.history) + 1
  
      # Endgame defection for the last 5 rounds (996 to 1000)
      if round_number > 995:
          return axl.Action.D
  
      # Condition 1: Exploit unconditional cooperators
      # Check if opponent played Cooperate immediately following an unprovoked defection from us
      exploitable = False
      for i in range(len(self.history) - 1):
          unprovoked = False



# Here is a simple, aggressive strategy designed to maximize your overall payoff
# by establishing mutual cooperation with retaliatory opponents while
# mercilessly exploiting weak or unconditionally cooperative ones.  **Strategy
# Rules (Apply in strict order from top to bottom):**  1. **Endgame Betrayal:**
# If it is the final round (Round 1000), **defect**. 2. **Initial Probe:** If it
# is Round 1, **defect** to test the opponent's response. 3. **Strategic
# Apology:** If it is Round 2, **cooperate**. (This absorbs a retaliatory strike
# from a strict Tit-for-Tat player and resets the relationship toward mutual
# cooperation). 4. **Identify and Exploit Weakness:** If your opponent played
# "cooperate"

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. Endgame Betrayal: Defect on the final round
      if len(self.history) == 999:
          return axl.Action.D
          
      # 2. Initial Probe: Defect on the first round
      if len(self.history) == 0:
          return axl.Action.D
          
      # 3. Strategic Apology: Cooperate on the second round
      if len(self.history) == 1:
          return axl.Action.C
          
      # 4. Identify and Exploit Weakness: 
      # If



# Follow these ordered rules to determine your action in each round. Always
# apply the first rule from this list that matches the current game state:  1.
# **End-Game Defection:** If the current round is 995 or higher, play Defect. 2.
# **Late-Game Protection:** If the current round is 900 or higher, and the
# opponent has played Defect in any round since Round 900, play Defect for all
# remaining rounds. 3. **Exploiting Passive Opponents:** If the opponent has
# never played Defect in the entire game and the current round is 100 or higher,
# play Defect.  4. **Restoring Trust After Testing:** If the opponent's *only*
# defections in the entire game

class Cooperative_12(LLM_Strategy):
  n = 12
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
  
      # 1. End-Game Defection: If the current round is 995 or higher, play Defect.
      if current_round >= 995:
          return axl.Action.D
  
      # 2. Late-Game Protection: If the current round is 900 or higher, and the opponent 
      # has played Defect in any round since Round 900, play Defect for all remaining rounds.
      if current_round >= 900:
          # Round 900 corresponds to index 899 in the history list
          if axl.Action.D in opponent.history[899:]:
              return axl.Action.D
  
      # 3. Exploiting Passive Opponents: If the opponent has never played Defect 
      # in the entire game and the current round is 100 or higher, play Defect.
      if opponent.history.defections == 0 and current_round >= 100:
          return axl.Action.D
  
      # 4. Restoring Trust After Testing / Default Action
      # (Rule 4 was cut off in the description, defaulting to Cooperate)
      return axl.Action.C



# Here is the revised strategy, rewritten to address the logical and strategic
# vulnerabilities while maintaining a neutral, payoff-maximizing approach:  1.
# **On round 1, play C** to establish a neutral, cooperative baseline. 2. **From
# round 2 to 1000, play C if your opponent played C** in the previous round.  3.
# **If your opponent played D in the previous round, play D** to protect
# yourself from exploitation and adapt immediately to hostile actions. 4. **To
# prevent endless retaliation spirals, forgive occasional defections:** if both
# you and your opponent played D in the previous round, play C in the current
# round to attempt to restore mutual cooperation. 5. **To protect against a
# strictly hostile opponent:** if your opponent plays D for three consecutive
# rounds

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
  
      # Rule 5: Protect against a strictly hostile opponent
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D] * 3:
          return axl.Action.D
  
      # Rule 4: Forgive occasional defections to prevent endless retaliation spirals
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # Rule 2: Play C if opponent played C in the previous round
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Rule 3: Play D if opponent played D in the previous round
      return axl.Action.D



# Apply the following rules in order of priority, from first to last:  1.
# **Round 1000 (Final Round):** Play Defect. Since there are no future rounds,
# there is no risk of retaliation, guaranteeing you either 5 or 1 point. 2.
# **First Round:** Play Cooperate. This establishes initial trust and prevents
# an immediate, inescapable loop of mutual defection against reciprocal
# strategies. 3. **If you played Defect in the previous round and the opponent
# played Cooperate:** Play Cooperate. This acts as an "apology" after you launch
# an aggressive strike, helping to restore mutual cooperation and avoid a
# continuous cycle of retaliation. 4. **If the opponent played Defect in the
# previous round:** Play Defect. This protects

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1: Round 1000 (Final Round)
      if len(self.history) == 999:
          return axl.Action.D
          
      # Rule 2: First Round
      if self.first_round():
          return axl.Action.C
          
      # Rule 3: If you played Defect in the previous round and the opponent played Cooperate
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
          
      # Rule 4: If the opponent played Defect in the previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      # Default action if none of the above apply (e.g., mutual cooperation in the previous round)
      return axl.Action.C



# To maximise your overall payoff using a cooperative approach, follow this
# chronological strategy:  1. **Rounds 1 and 2:** Play Cooperate. 2. **Rounds 3
# through 1000:** Base your move on your opponent's actions in the immediately
# preceding two rounds:     * **Condition to Defect:** Play Defect if your
# opponent played Defect in *both* of the previous two rounds.     * **Condition
# to Cooperate:** Play Cooperate if your opponent played Cooperate in *at least
# one* of the previous two rounds.

class Cooperative_13(LLM_Strategy):
  n = 13
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



# Here is the revised strategy, incorporating the feedback to address
# vulnerabilities while maintaining a neutral, reciprocal foundation:  **Round
# 1:** Play Cooperate with a 90% probability and Defect with a 10% probability.
# **Rounds 2 through 990:** Evaluate the game history and apply the first
# condition that is met from the list below: 1. **Defense Lock:** If the
# opponent has played Defect in the last three consecutive rounds, play Defect.
# 2. **Exploitation Lock:** If you played Defect in the previous round
# specifically because of the "Probing" rule below, and the opponent still
# played Cooperate, play Defect. 3. **Probing:** If the opponent has played
# Cooperate in the last five consecutive rounds, play Defect. 4.
# **Forgiveness:** If both you and the opponent played Defect in the last two
# consecutive rounds, play Cooperate with a 20% probability and Defect with an
# 80% probability. 5. **Reciprocity:** Copy the opponent's action from the
# immediately preceding round, but randomly choose the opposite action with a 5%
# probability.  **Rounds 991 through 1000:** Play Defect unconditionally.

class Neutral_13(LLM_Strategy):
  n = 13
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          self.probed_last_round = False
          return self._random.random_choice(0.9)
          
      if len(self.history) >= 990:
          self.probed_last_round = False
          return axl.Action.D
          
      # 1. Defense Lock
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D] * 3:
          self.probed_last_round = False
          return axl.Action.D



# Here is a rewritten strategy that addresses the logical flaws, avoids endless
# defection loops, and maintains an aggressive but mathematically sound approach
# to maximize your payoff:  1. **Round 1:** Play Cooperate to establish a
# baseline of mutual cooperation and avoid triggering immediate retaliation. 2.
# **Rounds 2 through 999:**     - *Condition 1 (Apologize/Reset):* If you played
# Defect in the previous round and your opponent retaliated by playing Defect,
# play Cooperate. This breaks any cycle of mutual defection you may have
# initiated.    - *Condition 2 (Retaliate):* If you played Cooperate in the
# previous round and your opponent played Defect, play Defect to punish them.
# - *

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Play Cooperate
      if self.first_round():
          return axl.Action.C
          
      # Round 1000: Mathematically sound to defect on the final round
      if len(self.history) == 999:
          return axl.Action.D
          
      # Rounds 2 through 999
      my_last_move = self.history[-1]
      opp_last_move = opponent.history[-1]
      
      # Condition 1 (Apologize/Reset): Break mutual defection
      if my_last_move == axl.Action.D and opp_last_move == axl.Action.D:
          return axl.Action.C
          
      # Condition 2 (Retaliate): Punish opponent's defection
      if my_last_move == axl.Action.C and opp_last_move == axl.Action.D:
          return axl.Action.D
          
      # Default condition (implied for mutual cooperation or successful exploitation)
      return axl.Action.C



# Here is the revised strategy, incorporating the feedback to balance
# cooperation, forgiveness, exploitation, and end-game optimization:  1. **Round
# 1 (Opening):** Play C. 2. **Round 5 (Probe for Exploitation):** Play D to test
# if the opponent retaliates.  3. **Rounds 6 through 997 (Reciprocity,
# Forgiveness, and Exploitation):**    - *Exploit:* If the opponent played C in
# round 6 (showing they do not retaliate against your round 5 defection), play D
# for all remaining rounds.    - *Forgive:* If the previous two rounds resulted
# in mutual defection (both players played D twice in a row), play C to break
# the retaliatory cycle

class Cooperative_14(LLM_Strategy):
  n = 14
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_num = len(self.history) + 1
  
      # 1. Round 1 (Opening): Play C.
      if round_num == 1:
          return axl.Action.C
  
      # 2. Round 5 (Probe for Exploitation): Play D to test if the opponent retaliates.
      if round_num == 5:
          return axl.Action.D
  
      # End-game optimization: Defect in the final rounds (998, 999, 1000)
      if round_num >= 998:
          return axl.Action.D
  
      # 3. Rounds 6 through 997 (Reciprocity, Forgiveness, and Exploitation)
      
      # Exploit: If the opponent played C in round 6 (index 5), play D for all remaining rounds.
      if round_num > 6:
          if opponent.history[5] == axl.Action.C:
              return axl.Action.D
  
      # Forgive: If the previous two rounds resulted in mutual defection, play C.
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and
              self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D):
              return axl.Action.C
  
      # Reciprocity: Default to playing the opponent's last move (Tit-For-Tat)
      return opponent.history[-1]



# Here is the revised strategy. Evaluate the following conditions in order for
# each round, applying the first one that is true:  1. If it is round 1000,
# choose to defect. 2. If it is round 1, choose to cooperate. 3. If the opponent
# chose to cooperate in all of the previous five rounds, choose to defect. 4. If
# the opponent chose to defect in both of the previous two rounds, choose to
# defect. 5. In all other situations, choose to cooperate.

class Neutral_14(LLM_Strategy):
  n = 14
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      if current_round == 1000:
          return axl.Action.D
          
      if current_round == 1:
          return axl.Action.C
          
      if len(opponent.history) >= 5 and opponent.history[-5:] == [axl.Action.C] * 5:
          return axl.Action.D
          
      if len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.D] * 2:
          return axl.Action.D
          
      return axl.Action.C



# Here is the rewritten strategy, addressing the missing logic and ensuring a
# complete decision matrix for all 1000 rounds.  Follow these conditions in
# order of priority:  1. **The Endgame:** If the current round is between 996
# and 1000 (inclusive), always play Defect. 2. **The Aggressive Test:** If it is
# round 1, play Defect. 3. **The Apology:** If it is round 2, play Cooperate.
# 4. **The Exploitation:** If the current round is between 3 and 995 (inclusive)
# and the opponent played Cooperate in round 2, play Defect. 5. **The Fallback
# (Tit-for-Tat):** If the current round is

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      if current_round >= 996:
          return axl.Action.D
          
      if current_round == 1:
          return axl.Action.D
          
      if current_round == 2:
          return axl.Action.C
          
      if opponent.history[1] == axl.Action.C:
          return axl.Action.D
          
      return opponent.history[-1]



# To maximize your overall payoff using a cooperative approach while addressing
# the vulnerabilities, follow this step-by-step strategy. Apply the rules in the
# exact order listed, using the first condition that matches the current round:
# 1. **Exploitation of Unconditional Cooperators:** If the game is past round
# 10, and your opponent has never played D at any point in the game, play D.  2.
# **The Probe:** On round 10, if your opponent has played C in all 9 previous
# rounds, play D to test if they will retaliate. 3. **Retaliation:** If your
# opponent played D in the immediately preceding two consecutive rounds, play D.
# 4. **Forgiveness and Default Cooperation:** In all other situations (including
# round 1),

class Cooperative_15(LLM_Strategy):
  n = 15
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
  
      # 1. Exploitation of Unconditional Cooperators
      if current_round > 10 and opponent.history.defections == 0:
          return axl.Action.D
  
      # 2. The Probe
      if current_round == 10 and opponent.history.defections == 0:
          return axl.Action.D
  
      # 3. Retaliation
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      # 4. Forgiveness and Default Cooperation
      return axl.Action.C



# Here is the revised strategy, ordered chronologically and by priority,
# addressing the logical vulnerabilities:  1. **Round 1:** Play Cooperate. 2.
# **Rounds 2 through 995:** Evaluate the following conditions in order and apply
# the first one that matches the game history:     *   **Exploit Unconditional
# Cooperators:** If your opponent has played Cooperate for the last five
# consecutive rounds, play Defect. If you played Defect in the previous round
# and your opponent still played Cooperate, continue to play Defect.     *
# **Forgive and Break Spirals:** If you and your opponent have played opposite
# actions to each other for the last three consecutive rounds (e.g., you played
# Cooperate while they played Defect, and vice versa), play Cooperate to reset
# mutual cooperation.     *   **Reciprocate:** If none of the above conditions
# apply, copy the action your opponent played in the immediately preceding round
# (play Cooperate if they played Cooperate, and play Defect if they played
# Defect). 3. **Rounds 996 through 1000:** Play Defect in every round,
# regardless of your opponent's previous actions, to preempt end-game
# retaliation.

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
          
      round_number = len(self.history) + 1
      
      # Rounds 996 through 1000: Play Defect
      if round_number >= 996:
          return axl.Action.D
          
      # Rounds 2 through 995: Evaluate conditions in order
      
      # 1. Exploit Unconditional Cooperators
      if len(opponent.history) >= 5 and opponent.history[-5:].count(axl.Action.C) == 5:
          return axl.Action.D
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
          
      # 2. Forgive and Break Spirals
      if len(self.history) >= 3:
          if all(self.history[-i] != opponent.history[-i] for i in range(1, 4)):
              return axl.Action.C
              
      # 3. Reciprocate
      return opponent.history[-1]



# To maximize your overall payoff using an aggressive approach, you should probe
# the opponent early to see if they can be exploited, exploit them indefinitely
# if they show weakness, and establish mutually beneficial cooperation if they
# prove capable of retaliation.   Apply the following rules in strict order of
# precedence (the first applicable condition dictates your move):  1. **If it is
# round 1000:** Play Defect. (Ensures you are not exploited on the final turn).
# 2. **If it is round 1:** Play Defect. (Probes the opponent to test their
# initial response). 3. **If it is round 2:** Play Cooperate. (Signals a
# willingness to establish mutual cooperation after the initial probe). 4. **If
# your opponent played Cooperate in both round 1 and round 2:** Play Defect.
# (Identifies an overly forgiving or unconditional cooperator and exploits them
# indefinitely). 5. **Otherwise:** Play the move your opponent played in the
# previous round. (Defaults to a Tit-for-Tat approach to maintain mutual
# cooperation or retaliate against ongoing defection).

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      if current_round == 1000:
          return axl.Action.D
          
      if current_round == 1:
          return axl.Action.D
          
      if current_round == 2:
          return axl.Action.C
          
      if opponent.history[0] == axl.Action.C and opponent.history[1] == axl.Action.C:
          return axl.Action.D
          
      return opponent.history[-1]



# Here is a revised strategy that addresses the vulnerabilities by removing the
# predictable endgame defection, introducing a mechanism to test and exploit
# passive opponents, and adding a forgiveness rule to prevent endless
# retaliation cycles:  1. **Round 1:** Choose to cooperate. 2. **Round 2:**
# Choose to defect to test the opponent's strategy. 3. **Rounds 3 through
# 1000:** Evaluate the following conditions in order and apply the first one
# that fits:     *   **Exploit:** If the opponent has chosen to cooperate in
# every single previous round, choose to defect. (This maximizes your score
# against an unconditional cooperator).     *   **Forgive:** If the opponent
# chose to defect in the immediately preceding round, but chose to cooperate in
# the round before that

class Cooperative_16(LLM_Strategy):
  n = 16
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Choose to cooperate
      if self.first_round():
          return axl.Action.C
      
      # Round 2: Choose to defect to test the opponent's strategy
      if len(self.history) == 1:
          return axl.Action.D
          
      # Rounds 3 through 1000: Evaluate conditions in order
      
      # Exploit: If the opponent has chosen to cooperate in every single previous round, choose to defect.
      if opponent.history.defections == 0:
          return axl.Action.D
          
      # Forgive: If the opponent chose to defect in the immediately preceding round, 
      # but chose to cooperate in the round before that, forgive and cooperate.
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
          
      # Default fallback: Play Tit-For-Tat (copy opponent's last move) to prevent being exploited 
      # while maintaining cooperation if the opponent cooperates.
      return opponent.history[-1]



# Here is the revised strategy:  1. **Round 1:** Play Cooperate. 2. **Round 2:**
# Mirror your opponent's action from Round 1 (play Cooperate if they played
# Cooperate; play Defect if they played Defect). 3. **Rounds 3 through 996:**
# - If both you and your opponent played Defect in the two immediately preceding
# rounds, play Cooperate to break the retaliation cycle.    - Under all other
# circumstances, mirror your opponent's action from the immediately preceding
# round. 4. **Rounds 997 through 1000:** Play Defect, regardless of your
# opponent's previous actions, to preempt endgame unraveling and avoid the
# sucker's payoff.

class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      if current_round == 1:
          return axl.Action.C
          
      if current_round >= 997:
          return axl.Action.D
          
      if current_round == 2:
          return opponent.history[-1]
          
      if (self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and
          opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D):
          return axl.Action.C
          
      return opponent.history[-1]



# To maximize your overall payoff using an aggressive approach, this strategy
# proactively exploits cooperative behavior, strictly punishes defections
# without exposing you to the sucker payoff, and safely exploits the final round
# without triggering premature backward induction.   Apply the following rules
# in strictly descending order of priority for each round:  1. **Endgame:** On
# round 1000, play Defect. 2. **Defense:** If the opponent played Defect in the
# previous round, play Defect. 3. **Exploitation:** If the opponent played
# Cooperate in the previous three consecutive rounds, play Defect. 4.
# **Baseline:** In all other situations (including round 1), play Cooperate.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      # 1. Endgame: On round 1000, play Defect.
      if current_round == 1000:
          return axl.Action.D
          
      if len(opponent.history) > 0:
          # 2. Defense: If the opponent played Defect in the previous round, play Defect.
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.D
              
      if len(opponent.history) >= 3:
          # 3. Exploitation: If the opponent played Cooperate in the previous three consecutive rounds, play Defect.
          if opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]:
              return axl.Action.D
              
      # 4. Baseline: In all other situations (including round 1), play Cooperate.
      return axl.Action.C



# Here is the revised strategy, incorporating the feedback to address the
# endgame, backward induction, and infinite retaliation cycles:  1. In round 1,
# choose to cooperate. 2. In rounds 2 through 998, if both you and your opponent
# chose to defect in the two immediately preceding rounds, choose to cooperate.
# 3. In rounds 2 through 998, for all other scenarios, choose to cooperate if
# your opponent cooperated in the immediately preceding round, and choose to
# defect if your opponent defected in the immediately preceding round. 4. In
# rounds 999 and 1000, choose to defect regardless of your opponent's previous
# actions.

class Cooperative_17(LLM_Strategy):
  n = 17
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.C
          
      current_round = len(self.history) + 1
      
      if current_round >= 999:
          return axl.Action.D
          
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and 
              self.history[-2] == axl.Action.D and 
              opponent.history[-1] == axl.Action.D and 
              opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      return opponent.history[-1]



# To maximize your overall payoff while addressing backward induction,
# retaliation loops, and exploitation opportunities, follow these ordered
# conditions. Apply the first condition that matches the current round:  1.
# **Endgame Preemption:** If it is Round 995 or later, play D to secure final
# points and preempt the opponent's anticipated late-game defections. 2.
# **Exploitation Lock-in:** If the opponent has played C in every single round
# since the beginning of the game, but the current round is Round 20 or later,
# play D. (This safely exploits unconditional cooperators without risking early
# retaliation). 3. **Forgiveness (Breaking Loops):** If the previous two rounds
# consisted of mutual defections (both played D) or alternating defections (you
# played C and

class Neutral_17(LLM_Strategy):
  n = 17
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize with Cooperation on the first round
      if self.first_round():
          return axl.Action.C
  
      current_round = len(self.history) + 1
  
      # 1. Endgame Preemption: Defect on round 995 or later
      if current_round >= 995:
          return axl.Action.D
  
      # 2. Exploitation Lock-in: Exploit unconditional cooperators from round 20 onwards
      if current_round >= 20 and opponent.history.cooperations == len(opponent.history):
          return axl.Action.D
  
      # 3. Forgiveness (Breaking Loops): Break out of mutual or alternating defection loops
      if len(self.history) >= 2:
          my_last_two = self.history[-2:]
          opp_last_two = opponent.history[-2:]
          
          # Mutual defections for the last two rounds
          mutual_defection = (my_last_two == [axl.Action.D, axl.Action.D] and 
                              opp_last_two == [axl.Action.D, axl.Action.D])
          
          # Alternating defections (C then D vs D then C)
          alternating_1 = (my_last_two == [axl.Action.C, axl.Action.D] and 
                           opp_last_two == [axl.Action.D, axl.Action.C])
                           
          # Alternating defections (D then C vs C then D)
          alternating_2 = (my_last_two == [axl.Action.D, axl.Action.C] and 
                           opp_last_two == [axl.Action.C, axl.Action.D])
                           
          if mutual_defection or alternating_1 or alternating_2:
              return axl.Action.C
  
      # Default fallback: Tit-For-Tat (play the opponent's last move)
      return opponent.history[-1]



# ate in the previous round:** Play Cooperate. (Maintains mutual cooperation).
# Let's trace this:         Vs ALL-D:         R1: We D. They D.         R2:
# Opponent D in last two? No (only R1 exists). Rule 4 triggers -> We C. They D.
# R3: Opponent D in last two? Yes (R1, R2). Rule 3 triggers -> We D. They D.
# R4: Opponent D in last two? Yes. Rule 3 -> We D.         Result: D, C, D, D,
# D... We get suckered once, then protect ourselves. Good.          Vs ALL-C:
# R1: We

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
      
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
          
      return axl.Action.C



# To determine your move in any given round, evaluate the following rules in
# order and apply the first one that matches the current conditions:  1.
# **Endgame:** If it is round 996 through 1000, play D regardless of your
# opponent's past actions to protect against preemptive endgame defection. 2.
# **Exploitation:** If it is round 12 or later, and your opponent played C in
# round 11 while you played D, play D for all remaining rounds to maximize
# points against an unconditional cooperator. 3. **Testing:** If it is round 11,
# and your opponent played C in all 10 previous rounds, play D to test if they
# will retaliate. 4. **Forgiveness:** If it is round

class Cooperative_18(LLM_Strategy):
  n = 18
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
  
      # 1. Endgame
      if 996 <= current_round <= 1000:
          return axl.Action.D
  
      # 2. Exploitation
      if current_round >= 12:
          if opponent.history[10] == axl.Action.C and self.history[10] == axl.Action.D:
              return axl.Action.D
  
      # 3. Testing
      if current_round == 11:
          if opponent.history.cooperations == 10:
              return axl.Action.D
  
      # 4. Forgiveness (Rule incomplete, defaulting to Tit-For-Tat)
      if current_round == 1:
          return axl.Action.C
  
      return opponent.history[-1]



# Here is the revised strategy, addressing the previous logical and strategic
# vulnerabilities:  1. On round 1, play Defect. 2. On round 2, play Cooperate.
# 3. On rounds 3 through 1000, determine your move by evaluating the following
# conditions in this exact order of priority:    * **Condition A:** If your
# opponent has played Defect in strictly more than 50% of all preceding rounds,
# play Defect.    * **Condition B:** If your opponent played Defect in the
# immediately preceding round but played Cooperate in the round prior to that,
# play Cooperate.    * **Condition C:** If neither of the above conditions
# applies, play the move your opponent played in the immediately preceding
# round.

class Neutral_18(LLM_Strategy):
  n = 18
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.D
          
      if len(self.history) == 1:
          return axl.Action.C
          
      # Condition A: If opponent has played Defect in strictly more than 50% of all preceding rounds
      if opponent.history.defections > len(opponent.history) / 2:
          return axl.Action.D
          
      # Condition B: If opponent played Defect in the immediately preceding round but Cooperate in the round prior
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
          
      # Condition C: Play the move your opponent played in the immediately preceding round
      return opponent.history[-1]



# To aggressively maximize your overall payoff, use a strategy that tests the
# opponent early, absorbs any immediate retaliation to establish mutual
# cooperation, continuously exploits unconditional cooperators, and backstabs on
# the final round.   Apply the following rules in this exact order for each
# round:  1. **Endgame Defection:** If the current round is exactly 1000, play
# Defect. 2. **Initial Test:** On round 1, play Defect. 3. **Truce and
# Stabilization:** On rounds 2 and 3, play Cooperate. (This signals a truce and
# absorbs a delayed punishment from retaliatory opponents, preventing a
# destructive cycle of alternating defections). 4. **Exploit the Weak:** From
# round 4 to 999, if your opponent has played Cooperate in *every* previous
# round of the game, play Defect. 5. **Match and Retaliate (Default):** For all
# other situations from round 4 to 999, play the exact action your opponent
# played in the immediately preceding round.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      if current_round == 1000:
          return axl.Action.D
          
      if current_round == 1:
          return axl.Action.D
          
      if current_round == 2 or current_round == 3:
          return axl.Action.C
          
      if opponent.history.defections == 0:
          return axl.Action.D
          
      return opponent.history[-1]



# To maximize your overall payoff using a cooperative approach, follow these
# ordered rules:  1. On the first and second rounds, play Cooperate. 2. From
# round 3 through round 1000, play Defect if your opponent played Defect in both
# of the two immediately preceding rounds. 3. In all other situations, play
# Cooperate.

class Cooperative_19(LLM_Strategy):
  n = 19
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



# Here is the revised strategy incorporating the feedback:  1. **Round 1:**
# Choose to cooperate. 2. **Rounds 2 through 995:** Observe your opponent's
# action in the immediately preceding round.     * If they cooperated, choose to
# cooperate.     * If they defected, choose to defect. However, to prevent
# endless retaliation cycles and introduce unpredictability, randomly choose to
# cooperate instead with a 10% probability. 3. **Rounds 996 through 1000:**
# Choose to defect in every round, regardless of your opponent's past actions,
# to protect against anticipated end-game betrayals.

class Neutral_19(LLM_Strategy):
  n = 19
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      if current_round == 1:
          return axl.Action.C
          
      if current_round >= 996:
          return axl.Action.D
          
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return self._random.random_choice(0.1)



# To maximize your overall payoff with an aggressive approach, use a strategy
# that continuously exploits unconditional cooperators, defends against
# aggressive opponents, and secures the maximum score on the final round.
# Follow these rules in strict order of priority:  1. **The Endgame Condition:**
# If it is round 1000, play defect. 2. **The Initial Probe:** If it is round 1,
# play defect. 3. **The Exploitation Condition:** If the opponent has played
# cooperate in every previous round of the game, play defect. 4. **The Defense
# Condition:** If the opponent played defect in the previous round, play defect.
# 5. **The Cooperative Fallback:** Otherwise (if the opponent has defected at
# least once in the past but played cooperate in the previous round), play
# cooperate.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      # 1. The Endgame Condition
      if current_round == 1000:
          return axl.Action.D
          
      # 2. The Initial Probe
      if current_round == 1:
          return axl.Action.D
          
      # 3. The Exploitation Condition
      if opponent.history.defections == 0:
          return axl.Action.D
          
      # 4. The Defense Condition
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      # 5. The Cooperative Fallback
      return axl.Action.C



# Here is the revised strategy, updated to address the vulnerabilities while
# maintaining a cooperative approach:  1. **Round 1:** Play Cooperate. 2.
# **Round 2:** Play Cooperate if your opponent played Cooperate in Round 1. Play
# Defect if your opponent played Defect in Round 1. 3. **Rounds 3 through
# 1000:** Base your action on your opponent's recent play using the following
# ordered conditions:     *   **Condition A:** Play Cooperate if your opponent
# played Cooperate in the immediately preceding round.     *   **Condition B:**
# Play Cooperate if your opponent played Defect in the immediately preceding
# round, *only if* they played Cooperate in the two consecutive rounds prior to
# that defection. (This forgives a single, isolated defection to prevent endless
# cycles of retaliation).     *   **Condition C:** Play Defect in all other
# scenarios where your opponent played Defect in the immediately preceding
# round.   By maintaining these rules through the final round without
# preemptively defecting, you avoid triggering backward induction, protect
# yourself from continuous exploitation, and remain strictly aligned with a
# cooperative premise.

class Cooperative_20(LLM_Strategy):
  n = 20
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Play Cooperate
      if not self.history:
          return axl.Action.C
          
      # Round 2: Play Cooperate if opponent played Cooperate in Round 1, else Defect
      if len(self.history) == 1:
          return opponent.history[-1]
          
      # Rounds 3 through 1000
      # Condition A: Play Cooperate if opponent played Cooperate in the immediately preceding round
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
          
      # Condition B: Play Cooperate if opponent played Defect in the immediately preceding round, 
      # *only if* they played Cooperate in the two consecutive rounds prior to that defection.
      if len(self.history) >= 3 and opponent.history[-2] == axl.Action.C and opponent.history[-3] == axl.Action.C:
          return axl.Action.C
          
      # Condition C: Play Defect in all other scenarios where opponent played Defect in the immediately preceding round
      return axl.Action.D



# Here is the revised strategy, ordered chronologically, incorporating
# mechanisms to probe for passive opponents, forgive accidental defections, and
# preempt endgame exploitation:  1. **Round 1:** Play Cooperate. 2. **Rounds 2
# through 9:** Play Cooperate if your opponent played Cooperate in the previous
# round. Play Defect if your opponent played Defect in the previous round. 3.
# **Round 10:** Play Defect, regardless of your opponent's previous actions, to
# test if they will retaliate. 4. **Rounds 11 through 995:** Evaluate the
# following conditions in order and apply the first one that matches:     * If
# your opponent has played Cooperate in every single round of the game so far,
# play Defect to maximize your payoff against an unconditional cooperator.     *
# If your opponent played Defect in both of the immediately preceding two
# rounds, play Cooperate to attempt to break a cycle of mutual retaliation.
# * Otherwise, mirror your opponent's action from the previous round (play
# Cooperate if they played Cooperate, and play Defect if they played Defect). 5.
# **Rounds 996 through 1000:** Play Defect unconditionally in every round to
# protect against your opponent's anticipated endgame defection.

class Neutral_20(LLM_Strategy):
  n = 20
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      if round_number == 1:
          return axl.Action.C
          
      elif 2 <= round_number <= 9:
          return opponent.history[-1]
          
      elif round_number == 10:
          return axl.Action.D
          
      elif 11 <= round_number <= 995:
          if opponent.history.defections == 0:
              return axl.Action.D
          elif opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.C
          else:
              return opponent.history[-1]
              
      else:
          return axl.Action.D



# To maximize your overall payoff with an aggressive approach, you should
# establish trust, periodically test the opponent to exploit them if they are
# forgiving, protect yourself from unprovoked attacks, and secure the maximum
# points on the final turn.   Follow these ordered conditions for each round,
# always applying the first rule that matches the current situation:  1. **The
# Final Round Rule:** If it is round 1000, play Defect. 2. **The First Round
# Rule:** If it is round 1, play Cooperate. 3. **The Exploitation Rule:** If you
# played Defect in the previous round and your opponent played Cooperate, play
# Defect.  4. **The Apology Rule:** If you played Defect in the previous round
# and your opponent played Defect, play Cooperate.  5. **The Self-Defense
# Rule:** If your opponent played Defect in the previous round, play Defect. 6.
# **The Aggressor Rule:** If the current round number is a multiple of 10 (e.g.,
# 10, 20, 30), play Defect. 7. **The Default Rule:** Under all other conditions,
# play Cooperate.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      # 1. The Final Round Rule
      if current_round == 1000:
          return axl.Action.D
          
      # 2. The First Round Rule
      if current_round == 1:
          return axl.Action.C
          
      my_last_move = self.history[-1]
      opp_last_move = opponent.history[-1]
      
      # 3. The Exploitation Rule
      if my_last_move == axl.Action.D and opp_last_move == axl.Action.C:
          return axl.Action.D
          
      # 4. The Apology Rule
      if my_last_move == axl.Action.D and opp_last_move == axl.Action.D:
          return axl.Action.C
          
      # 5. The Self-Defense Rule
      if opp_last_move == axl.Action.D:
          return axl.Action.D
          
      # 6. The Aggressor Rule
      if current_round % 10 == 0:
          return axl.Action.D
          
      # 7. The Default Rule
      return axl.Action.C



# Here is the revised strategy, updated to address the logical vulnerabilities
# while maintaining a simple, cooperative approach:  1. **Round 1:** Play
# Cooperate. 2. **Rounds 2 through 1000:** Determine your move by evaluating the
# following conditions in strict order of priority, applying the first one that
# matches the situation:     *   **Condition 1 (Exploit Unresponsive
# Opponents):** If your opponent has played Defect for the last three
# consecutive rounds, or if their moves follow a clearly random or fixed pattern
# that ignores your previous actions, play Defect continuously. This maximizes
# your payoff against opponents incapable of mutual cooperation.     *
# **Condition 2 (Forgive to Break Spirals):** If both you and your opponent have
# played Defect for

class Cooperative_21(LLM_Strategy):
  n = 21
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.defect_continuously = False
          return axl.Action.C
  
      # Condition 1: Exploit Unresponsive Opponents
      if self.defect_continuously:
          return axl.Action.D
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          self.defect_continuously = True
          return axl.Action.D
  
      # Condition 2: Forgive to Break Spirals
      # (Assuming "the last 2 rounds" as the text was cut off, which is standard for breaking D-D spirals)
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      # Fallback behavior (Tit-For-Tat) since the rest of the strategy description was cut off
      return opponent.history[-1]



# Here is the revised strategy, incorporating the feedback to maintain a
# strictly neutral approach, eliminate backward induction vulnerabilities, and
# introduce a forgiveness mechanism to prevent endless retaliation loops:  1.
# **Round 1:** Play Cooperate. 2. **Round 2:** Play Cooperate. 3. **Rounds 3
# through 1000:** Evaluate your opponent's moves from the two immediately
# preceding rounds. If your opponent played Defect in *both* of those rounds,
# play Defect. Under all other conditions, play Cooperate.

class Neutral_21(LLM_Strategy):
  n = 21
  attitude = Attitude.NEUTRAL
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



# Evaluate the following conditions in order from top to bottom for each round,
# and apply the first one that fits:  1. If the current round is 1000, play
# Defect. 2. If you played Defect and your opponent played Cooperate in the
# previous round, play Defect.  3. If both you and your opponent played Defect
# in the previous round, play Cooperate. 4. If your opponent played Defect in
# the previous round, play Defect. 5. Otherwise, play Cooperate.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 999:
          return axl.Action.D
          
      if len(self.history) > 0:
          my_last_move = self.history[-1]
          opp_last_move = opponent.history[-1]
          
          if my_last_move == axl.Action.D and opp_last_move == axl.Action.C:
              return axl.Action.D
              
          if my_last_move == axl.Action.D and opp_last_move == axl.Action.D:
              return axl.Action.C
              
          if opp_last_move == axl.Action.D:
              return axl.Action.D
              
      return axl.Action.C



# 1. In the first round, play Cooperate. 2. In the second round, play Cooperate.
# 3. In rounds 3 through 1000, play Defect if your opponent played Defect in
# both of the two immediately preceding rounds. 4. In all other circumstances
# during rounds 3 through 1000, play Cooperate.

class Cooperative_22(LLM_Strategy):
  n = 22
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



# Here is the revised strategy addressing the logical flaws:  1. On the first
# round, defect to safely probe the opponent's strategy and avoid the initial
# sucker payoff. 2. On the second round, cooperate to signal a willingness to
# establish mutual cooperation. 3. From round 3 to round 995, choose your move
# by evaluating the following conditions in order:     *   If the opponent has
# cooperated in every previous round, defect to maximize your score against an
# unconditional cooperator.     *   If the opponent defected in both of the
# immediately preceding two rounds, defect to protect yourself from an
# aggressive or uncooperative opponent.     *   Otherwise, cooperate. (This acts
# as a forgiveness mechanism: it tolerates a single defection to break potential
# retaliation spirals, while

class Neutral_22(LLM_Strategy):
  n = 22
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Defect to safely probe
      if len(self.history) == 0:
          return axl.Action.D
          
      # Round 2: Cooperate to signal willingness
      if len(self.history) == 1:
          return axl.Action.C
          
      # Rounds 996 to 1000: Defect in the endgame
      if len(self.history) >= 995:
          return axl.Action.D
          
      # Round 3 to 995
      # If the opponent has cooperated in every previous round, defect
      if opponent.history.defections == 0:
          return axl.Action.D
          
      # If the opponent defected in both of the immediately preceding two rounds, defect
      if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
          
      # Otherwise, cooperate
      return axl.Action.C



# Here is a simple, logically consistent strategy designed to maximize your
# overall payoff by maintaining mutually beneficial cooperation while
# aggressively punishing defection and exploiting the final round.   Follow
# these conditions in strict order of priority:  1. **The Endgame Condition:**
# If it is round 1000, play Defect. (Since there are no future rounds, you
# cannot be retaliated against, guaranteeing you either 5 points or 1 point). 2.
# **The Retaliation Condition:** If the opponent played Defect in the previous
# round, play Defect. (This aggressively punishes defection and prevents you
# from being exploited). 3. **The Cooperation Condition:** In all other
# situations—including round 1 and whenever the opponent played Cooperate in the
# previous round—play Cooperate. (This initiates and sustains continuous mutual
# cooperation, which mathematically yields a higher long-term payoff than
# alternating defection and cooperation).

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. The Endgame Condition: If it is round 1000, play Defect.
      if len(self.history) == 999:
          return axl.Action.D
          
      # 3. The Cooperation Condition (Round 1): play Cooperate.
      if self.first_round():
          return axl.Action.C
          
      # 2. The Retaliation Condition: If the opponent played Defect in the previous round, play Defect.
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      # 3. The Cooperation Condition (Otherwise): play Cooperate.
      return axl.Action.C



# To maximize your overall cooperative payoff while addressing vulnerabilities
# to exploitation, noise, and end-game unraveling, follow this prioritized,
# step-by-step strategy:  1. **Initial Play:** Play Cooperate in round 1. 2.
# **Anti-Exploitation:** In any subsequent round, if your opponent has played
# Defect in two or more of their most recent three rounds, play Defect. Continue
# playing Defect until your opponent proves reliability by playing Cooperate for
# two consecutive rounds. 3. **Retaliation:** If your opponent played Defect in
# the immediately preceding round, play Defect. 4. **Forgiveness and Default
# Cooperation:** In all other situations, play Cooperate. This ensures you
# immediately resume cooperation if your opponent corrects an isolated
# defection. 5. **End-Game Consistency:** Apply these exact rules through round
# 1000. Do not preemptively defect in the final rounds, as doing so risks
# triggering early retaliation and the premature breakdown of mutual
# cooperation.

class Cooperative_23(LLM_Strategy):
  n = 23
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.is_exploited = False
          return axl.Action.C
  
      # Anti-Exploitation: Check if we are currently in the exploited state
      if self.is_exploited:
          # Continue playing Defect until opponent plays Cooperate for two consecutive rounds
          if len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.C, axl.Action.C]:
              self.is_exploited = False
          else:
              return axl.Action.D
  
      # Anti-Exploitation: Trigger exploited state if opponent played Defect in 2 or more of their last 3 rounds
      if opponent.history[-3:].count(axl.Action.D) >= 2:
          self.is_exploited = True
          return axl.Action.D
  
      # Retaliation: If opponent played Defect in the immediately preceding round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # Forgiveness and Default Cooperation
      return axl.Action.C



# Here is the revised strategy, addressing the logical and strategic
# vulnerabilities:  1. **Round 1:** Choose to cooperate. 2. **Rounds 2 through
# 989:**     * **Hostile Opponent Override:** If the opponent has defected in
# three consecutive rounds at any point in the game, choose to defect for all
# remaining rounds to protect against strictly hostile strategies.    *
# **Forgiveness Mechanism:** If the override does not apply, and both you and
# the opponent defected in the immediately preceding round, choose to cooperate.
# This breaks destructive cycles of mutual retaliation.    * **Standard
# Reciprocation:** If neither of the above conditions applies, copy the exact
# move your opponent made in the immediately preceding round. 3. **Rounds 990

class Neutral_23(LLM_Strategy):
  n = 23
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.is_hostile = False
          return axl.Action.C
  
      # Check for hostile opponent override
      if not self.is_hostile:
          if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              self.is_hostile = True
  
      round_number = len(self.history) + 1
  
      # Rounds 990 to 1000 (assuming defection for the final rounds based on the cutoff text)
      if round_number >= 990:
          return axl.Action.D
  
      # Rounds 2 through 989
      if self.is_hostile:
          return axl.Action.D
  
      # Forgiveness Mechanism
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # Standard Reciprocation
      return opponent.history[-1]



# Here is a simple, aggressive strategy designed to test your opponent early,
# exploit them if they are forgiving, and cooperate if they are retaliatory,
# while guaranteeing the maximum final-round payoff.   Follow these rules in
# strictly this order:  1. **Round 1000:** Always play Defect. 2. **Round 1:**
# Play Defect. 3. **Rounds 2 and 3:** Play Cooperate. 4. **Rounds 4 through 999
# (if opponent is forgiving):** If your opponent played Cooperate in both rounds
# 2 and 3, play Defect. 5. **Rounds 4 through 999 (if opponent is
# retaliatory):** If your opponent played Defect in either round 2 or 3, play
# the move your opponent chose in the previous round.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      rounds_played = len(self.history)
      
      if rounds_played == 999:
          return axl.Action.D
          
      if rounds_played == 0:
          return axl.Action.D
          
      if rounds_played == 1 or rounds_played == 2:
          return axl.Action.C
          
      if opponent.history[1] == axl.Action.C and opponent.history[2] == axl.Action.C:
          return axl.Action.D
      else:
          return opponent.history[-1]



# Here is the revised strategy, updated to address the logical vulnerabilities:
# 1. **Round 1:** Play Cooperate. 2. **Rounds 2 through 1000:** Base your move
# on your opponent's action in the immediately preceding round:     * If your
# opponent played Cooperate, play Cooperate.     * If your opponent played
# Defect, generally play Defect. However, approximately 10% of the time,
# randomly choose to play Cooperate instead. This introduces unpredictability to
# prevent exploitation and acts as a forgiveness mechanism to break out of
# endless cycles of mutual retaliation. 3. **Endgame:** Maintain this exact
# strategy through round 1000. Do not automatically defect in the final round;
# this prevents an intelligent opponent from anticipating a guaranteed betrayal
# and preemptively unraveling cooperation in the preceding rounds.

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
      
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return self._random.random_choice(0.1)



# Here is the revised strategy:  1. In round 1, play Cooperate. 2. For rounds 2
# through 995, play the action your opponent played in the immediately preceding
# round. However, to prevent endless retaliatory spirals, if both you and your
# opponent played Defect in the previous round, play Cooperate to attempt a
# reset.  3. For rounds 996 through 1000, play Defect unconditionally,
# regardless of your opponent's previous actions, to maximize your late-game
# payoff and preempt the opponent's anticipated end-game defection.

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
          
      round_number = len(self.history) + 1
      
      if round_number >= 996:
          return axl.Action.D
          
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
          
      return opponent.history[-1]



# Here is the revised strategy:  Follow these conditions in exact order on every
# round:  1. If it is round 1000, play Defect. 2. If it is round 1, play
# Cooperate. 3. If the opponent played Defect in the immediately preceding
# round, play Defect. 4. Under all other circumstances, play Cooperate.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 999:
          return axl.Action.D
      if len(self.history) == 0:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# Here is a revised strategy that addresses the logical vulnerabilities by
# removing the backward induction flaw, introducing forgiveness to prevent death
# spirals, and adding a mechanism to exploit unconditional cooperators:  1.
# **Round 1:** Play C. 2. **Exploitation Test:** On round 15, play D to test
# your opponent's boundaries.  3. **Exploiting Unconditional Cooperators:** From
# round 17 onward, if your opponent played C on round 16 (failing to retaliate
# against your round 15 defection), play D for all remaining rounds. 4.
# **Forgiveness (Breaking Spirals):** If you and your opponent have alternated
# defections over the last two rounds (you played D and they played C, followed
# by you playing

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
          
      round_num = len(self.history) + 1
      
      # 2. Exploitation Test: On round 15, play D
      if round_num == 15:
          return axl.Action.D
          
      # 3. Exploiting Unconditional Cooperators: From round 17 onward
      if round_num >= 17:
          # Check if opponent played C on round 16 (index 15)
          if opponent.history[15] == axl.Action.C:
              return axl.Action.D
              
      # 4. Forgiveness (Breaking Spirals): 
      # If you played D and they played C, followed by you playing C and they playing D
      if len(self.history) >= 2:
          if self.history[-2:] == [axl.Action.D, axl.Action.C] and opponent.history[-2:] == [axl.Action.C, axl.Action.D]:
              return axl.Action.C
              
      # Default behavior: Tit-For-Tat (play opponent's last move)
      return opponent.history[-1]



# Here is the revised strategy, incorporating the feedback to optimize the end-
# game, break retaliation cycles, and exploit unconditionally cooperative
# opponents:  1. **Round 1:** Play Cooperate. 2. **Rounds 2 through 10:** Play
# the move your opponent played in the previous round. 3. **Round 11:** Play
# Defect.  4. **Rounds 12 and 13:** Play Cooperate. 5. **Rounds 14 through
# 990:** Evaluate the following conditions in order and apply the first one that
# matches:    * If your opponent played Cooperate in both rounds 12 and 13, play
# Defect.    * If both you and your opponent played Defect in the previous two
# consecutive

class Neutral_25(LLM_Strategy):
  n = 25
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_num = len(self.history) + 1
  
      if round_num == 1:
          return axl.Action.C
      
      elif 2 <= round_num <= 10:
          return opponent.history[-1]
      
      elif round_num == 11:
          return axl.Action.D
      
      elif 12 <= round_num <= 13:
          return axl.Action.C
      
      elif 14 <= round_num <= 990:
          # Exploit unconditionally cooperative opponents
          if opponent.history[11] == axl.Action.C and opponent.history[12] == axl.Action.C:
              return axl.Action.D
          
          # Break retaliation cycles
          if (self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and
              self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
          # Default to Tit-For-Tat
          return opponent.history[-1]
          
      else:
          # Optimize the end-game (Rounds 991 to 1000)
          return axl.Action.D