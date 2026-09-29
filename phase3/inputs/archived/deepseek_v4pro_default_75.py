import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# Always defect. Choose D on every single round, regardless of what your
# opponent does.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Cooperate on the first round. For every round after that, simply repeat your
# opponent’s last move: if they cooperated last round, you cooperate this round;
# if they defected last round, you defect this round.

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
      return opponent.history[-1]



# 1. In the first round, cooperate. 2. In the second round, cooperate only if
# the opponent cooperated in the first round; otherwise, defect. 3. For all
# subsequent rounds, cooperate if either:    a) the opponent cooperated in the
# immediately preceding round, or    b) the opponent defected in the immediately
# preceding round but cooperated in the round before that (an isolated defection
# is forgiven).      Otherwise, defect — meaning a pattern of two consecutive
# defections is met with defection until the opponent cooperates again.

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
  
      if len(self.history) == 1:
          return axl.Action.C if opponent.history[0] == axl.Action.C else axl.Action.D
  
      last_opp = opponent.history[-1]
      prev_opp = opponent.history[-2]
  
      if last_opp == axl.Action.C:
          return axl.Action.C
  
      if last_opp == axl.Action.D and prev_opp == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Start by defecting in the first round. In every round after the first, copy
# the opponent's previous move: if they cooperated last round, defect; if they
# defected last round, cooperate.

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
      return opponent.history[-1] if opponent.history else axl.Action.D



# Start by cooperating in the first round. For every round after the first,
# follow this rule:  - If your payoff in the previous round was 3 (both
# cooperated) or 5 (you defected and they cooperated), repeat your previous
# action. - If your payoff in the previous round was 0 (you cooperated and they
# defected) or 1 (both defected), switch to the opposite action.

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
  
      last_my_action = self.history[-1]
      last_my_score = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_my_score in (3, 5):
          return last_my_action
      else:  # last_my_score in (0, 1)
          return axl.Action.D if last_my_action == axl.Action.C else axl.Action.C



# Start by cooperating in the first round. For every round after the first,
# follow this rule:  - If you scored 3 or 5 in the previous round, repeat the
# action you played in that round. - If you scored 0 or 1 in the previous round,
# switch to the opposite action.

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
  
      last_my_action = self.history[-1]
      last_my_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_my_score in (3, 5):
          return last_my_action
      if last_my_score in (0, 1):
          return axl.Action.D if last_my_action == axl.Action.C else axl.Action.C
  
      return last_my_action



# In every round, regardless of the opponent's actions or the outcomes of
# previous rounds, always play D (defect).

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Here is a simple strategy for the 1000-round game:  Start by cooperating in
# the first round. After that, follow these rules in order:  1. If your opponent
# defected in the previous round, defect in the next round. 2. If your opponent
# cooperated in the previous round, cooperate in the next round. 3. In the final
# round (round 1000), defect regardless of what your opponent did in round 999.
# This means you begin cooperatively, mirror your opponent's last move in all
# other rounds, and only break the pattern by defecting on the very last move to
# secure a final higher payoff if possible.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1]



# Start by cooperating in the first round.   In every subsequent round,
# cooperate unless any of the following conditions are met, in this order:    1.
# If your opponent defected in the immediately preceding round, defect.   2. If
# your opponent has defected more than 15% of all rounds so far, defect.   3. If
# your opponent defected twice in a row at any point in the last 10 rounds,
# defect.    Otherwise, cooperate.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      total_rounds = len(opponent.history)
      if total_rounds > 0 and opponent.history.defections / total_rounds > 0.15:
          return axl.Action.D
  
      last_10 = opponent.history[-10:]
      for i in range(len(last_10) - 1):
          if last_10[i] == axl.Action.D and last_10[i + 1] == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C



# Defect on the first move. For every subsequent move, repeat whatever your
# opponent played in the immediately preceding round.

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
      return opponent.history[-1]



# In the first round, cooperate.   For every round after that:    1. If your
# opponent cooperated in the previous round, cooperate.   2. If both you and
# your opponent defected in the previous round, cooperate.   3. If you
# cooperated in the previous round and your opponent defected, defect.    You
# defect only when you were exploited in the immediately preceding round; in all
# other situations you cooperate.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the first round. For all subsequent rounds, follow
# this rule: if your opponent chose D in each of the two most recent rounds,
# then choose D; otherwise, choose C.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Start by defecting in the first round.   In rounds 2 through 995, follow these
# rules in order:   - If your opponent defected in the immediately preceding
# round, defect.   - If your opponent cooperated in the preceding round but did
# not cooperate in the round before that, defect.   - If your opponent
# cooperated in both of the last two consecutive rounds, cooperate.   In the
# final 5 rounds (996–1000), always defect regardless of history.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number >= 996:
          return axl.Action.D
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.C and opponent.history[-2] != axl.Action.C:
              return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Cooperate on the first round.   For each round from 2 to 999: cooperate if the
# opponent cooperated in the previous round; defect if the opponent defected in
# the previous round.   Defect unconditionally on round 1000.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1]



# Start by cooperating in the first round. For every subsequent round, follow
# this rule:  - If your payoff in the previous round was 3 or 5, repeat your
# previous move. - If your payoff in the previous round was 0 or 1, switch to
# the opposite move.

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
  
      last_my_move = self.history[-1]
      last_my_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_my_score in (3, 5):
          return last_my_move
      if last_my_score in (0, 1):
          return axl.Action.D if last_my_move == axl.Action.C else axl.Action.C
  
      return last_my_move



# Always defect. In every round, regardless of the opponent’s previous actions,
# play D.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round. For every round after the first,
# cooperate if the opponent cooperated in the immediately preceding round. If
# the opponent defected in the immediately preceding round, defect.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# Start by cooperating in the first round. For every round after that, simply
# repeat the move your opponent made in the immediately preceding round: if they
# cooperated, you cooperate; if they defected, you defect. Apply this rule
# consistently for all 1000 rounds.

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
      return opponent.history[-1]



# Start by defecting on the first round. For every round after the first, follow
# this rule:  - If your payoff in the previous round was 1 (meaning both you and
# your opponent defected), then cooperate. - Otherwise, defect.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0] if False else False:
          pass
  
      if self.history and opponent.history:
          last_self = self.history[-1]
          last_opp = opponent.history[-1]
          if last_self == axl.Action.D and last_opp == axl.Action.D:
              return axl.Action.C
  
      return axl.Action.D



# Start by cooperating in the first round. For every round after the first,
# cooperate if both players chose the same action in the previous round (both
# cooperated or both defected); defect if the players chose different actions in
# the previous round.

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
      return axl.Action.D



# Begin by cooperating in the first round. In every subsequent round, base your
# move on your own payoff from the previous round:  - If you received 3 or 5
# points, repeat the action you just played. - If you received 0 or 1 point,
# switch to the opposite action.  Follow this rule unconditionally for all 1000
# rounds.

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
  
      last_my_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
      last_my_move = self.history[-1]
  
      if last_my_score in (3, 5):
          return last_my_move
      if last_my_score in (0, 1):
          return axl.Action.C if last_my_move == axl.Action.D else axl.Action.D
  
      return last_my_move



# Always choose D.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Cooperate on the first round.   For every round after the first, look at your
# opponent’s move in the immediately preceding round: if they cooperated, you
# cooperate; if they defected, you defect.

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
      return opponent.history[-1]



# **Strategy: Win-Stay, Lose-Shift with a final-round defection**  - **Round
# 1:** Cooperate. - **Rounds 2 to 999:** After each round, check your own payoff
# from the previous round:   - If you received 3 (you both cooperated) or 5 (you
# defected while the opponent cooperated), repeat your last action.   - If you
# received 0 (you cooperated while the opponent defected) or 1 (you both
# defected), switch to the opposite action. - **Round 1000:** Defect
# unconditionally, regardless of previous history.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.D
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# Defect in the first round. In each round after the first, choose whatever
# action your opponent chose in the immediately previous round.

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
      return opponent.history[-1]



# Strategy:  - On the first round, cooperate. - On every following round,
# cooperate if the opponent cooperated in the immediately previous round, and
# defect if the opponent defected in the immediately previous round.

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
      return opponent.history[-1]



# Start by cooperating in the first round. Thereafter, follow these rules in
# order:  1. If your payoff in the previous round was 3 or 5, repeat your
# previous move exactly (stay with cooperation or defection). 2. If your payoff
# in the previous round was 0 or 1, switch your move (from cooperation to
# defection, or vice versa).

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
  
      last_my_move = self.history[-1]
      last_opp_move = opponent.history[-1]
      last_my_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_my_score in (3, 5):
          return last_my_move
      if last_my_score in (0, 1):
          return axl.Action.D if last_my_move == axl.Action.C else axl.Action.C
  
      return last_my_move



# Start by defecting on the first round.   For every round after the first:   -
# if your opponent cooperated in the previous round, cooperate;   - if your
# opponent defected in the previous round, defect.

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
      return opponent.history[-1]



# Start every game by cooperating in the first round. Then, for each subsequent
# round, choose your action based solely on the opponent’s move in the
# immediately preceding round:  - If the opponent cooperated, cooperate. - If
# the opponent defected, defect.  Follow this rule consistently for all 1000
# rounds, without any modification for the final round.

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
      return opponent.history[-1]



# Cooperate on the first round.  For every subsequent round, base your decision
# on the outcome of the previous round:  - If both you and your opponent made
# the same choice in the previous round (both cooperated or both defected),
# cooperate. - If you and your opponent made different choices in the previous
# round (one cooperated and the other defected), defect.  Follow this rule
# without exception for all remaining rounds.

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# Always defect. On every round, choose D regardless of what the opponent does.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round. From the second round onward, decide
# your move based on the previous round’s outcome:   - If both players chose the
# same action (both cooperated or both defected), cooperate.   - If the actions
# differed (one cooperated and the other defected), defect.

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# Cooperate on the first round. For all subsequent rounds, cooperate if your
# opponent’s previous move was cooperate, and defect if your opponent’s previous
# move was defect.

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
      return opponent.history[-1]



# Start by defecting in the first round.   After that, follow these rules in
# order:    1. If your opponent cooperated on the immediately preceding round,
# defect.   2. If your opponent defected on the immediately preceding round,
# cooperate.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
      return axl.Action.C



# Start by cooperating in the first round. In every subsequent round, base your
# decision on the payoff you received in the immediately preceding round:  - If
# you scored **3** (mutual cooperation) or **5** (you defected, opponent
# cooperated), repeat the action you chose in that previous round. - If you
# scored **0** (you cooperated, opponent defected) or **1** (mutual defection),
# switch to the opposite action of what you chose in that previous round.  This
# means you will cooperate after a round of mutual cooperation or mutual
# defection, and you will defect after either being exploited or exploiting your
# opponent.

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
  
      last_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
      last_action = self.history[-1]
  
      if last_payoff in (3, 5):
          return last_action
      else:
          return last_action.flip()



# Start by cooperating in the first round. For every subsequent round, cooperate
# if the opponent cooperated in the previous round, and defect if the opponent
# defected in the previous round.

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
      return opponent.history[-1]



# Start by defecting on the very first round. For every round after that, simply
# repeat whatever action your opponent took in the previous round.

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return opponent.history[-1]



# Start by cooperating in the first round. For every round thereafter, cooperate
# if your opponent cooperated in the immediately previous round, and defect if
# your opponent defected in the immediately previous round.

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
      return opponent.history[-1]



# Cooperate in the first round.  For every following round, look at your
# opponent’s action in the immediately preceding round.   - If they cooperated,
# you cooperate.   - If they defected, you defect.  Continue applying this rule
# for all 1000 rounds.

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



# Start by defecting on the first round.   - If your opponent cooperated in that
# first round, then cooperate on every subsequent round until your opponent
# defects even once—after that, defect forever.   - If your opponent defected in
# the first round, defect forever from round two onward.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._opponent_defected_first = None
          return axl.Action.D
  
      if self._opponent_defected_first is None:
          self._opponent_defected_first = opponent.history[0] == axl.Action.D
  
      if self._opponent_defected_first:
          return axl.Action.D
  
      if axl.Action.D in opponent.history:
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the first round. In every following round, if the
# opponent cooperated in the immediately preceding round, cooperate; if the
# opponent defected, defect.

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
      return opponent.history[-1]



# Start by cooperating in the first round.  For every round after the first,
# base your decision solely on the outcome of the previous round:  - Cooperate
# if both you and your opponent made the same choice (both cooperated or both
# defected). - Defect if you and your opponent made different choices (you
# cooperated and they defected, or you defected and they cooperated).

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# Start by choosing Defect on the first round.   For every following round, look
# at your own payoff from the immediately previous round: - If you scored 5 or
# 3, repeat the move you just made. - If you scored 0 or 1, switch to the
# opposite move.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_my_score = self.score - self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_my_score in (5, 3):
          return self.history[-1]
      else:
          return axl.Action.C if self.history[-1] == axl.Action.D else axl.Action.D



# Begin by cooperating in round one. For every round thereafter, simply copy
# your opponent’s action from the immediately preceding round: if they
# cooperated, you cooperate; if they defected, you defect. This clear
# sequence—start cooperative, then mirror—ensures you reward cooperation, punish
# defection, and quickly return to mutual cooperation when your opponent does.

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
      return opponent.history[-1]



# In the first round, play C.  In every round after the first, look at what both
# you and your opponent did in the immediate previous round.   - If the two
# actions were the same (both C or both D), play C.   - If the two actions were
# different (one C and one D), play D.

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# Start by defecting on the first round.  For every round after the first,
# decide your move based on your own payoff from the previous round:  - If your
# payoff was 5 (you defected, opponent cooperated) or 3 (mutual cooperation),
# repeat your previous move. - If your payoff was 0 (you cooperated, opponent
# defected) or 1 (mutual defection), switch to the opposite move.

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
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0] if False else None
      # Compute previous-round payoff directly from the last interaction
      my_last, opp_last = self.total_scores(self.history[-1:], opponent.history[-1:])
      last_payoff = my_last
  
      if last_payoff in (5, 3):
          return self.history[-1]
      else:
          return axl.Action.C if self.history[-1] == axl.Action.D else axl.Action.D



# Start by cooperating in the first round. For every round after the first, use
# this rule:   Cooperate unless your opponent defected in each of the last two
# rounds—if they did, then defect. Otherwise, always cooperate.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Cooperate in the first round. In every subsequent round, base your choice on
# the outcome of the previous round only:  - If the opponent cooperated, you
# cooperate. - If the opponent defected and you cooperated, you defect (to
# punish the defection). - If the opponent defected and you also defected, you
# cooperate (to break the cycle of mutual defection).  This simple, forgiving
# strategy maintains cooperation when possible, retaliates against unprovoked
# defection exactly once, and actively restores mutual cooperation after both
# players have defected.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Always defect in every round, regardless of the opponent's actions. This
# guarantees you never receive the minimum payoff of 0, secures 5 points
# whenever the opponent cooperates, and ensures you obtain at least 1 point even
# if the opponent always defects.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Cooperate in the first round. For every round after that, cooperate if in the
# previous round you and your opponent made the same choice (both C or both D);
# defect if your choices differed (one C and one D).

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in the first round.   In every round after the first,
# mirror your opponent’s most recent move:   - If your opponent cooperated in
# the previous round, cooperate.   - If your opponent defected in the previous
# round, defect.

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
      return opponent.history[-1]



# In the first round, defect.   For every subsequent round:   - Defect if your
# opponent defected in the previous round.   - Cooperate if your opponent
# cooperated in the previous round.

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
      return axl.Action.D if opponent.history[-1] == axl.Action.D else axl.Action.C



# Cooperate in the first round. In every subsequent round, simply repeat the
# opponent's move from the previous round.

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
      return opponent.history[-1]



# Start by cooperating in the first round. For every round after that, base your
# decision solely on your own payoff from the immediately preceding round:  - If
# your last-round payoff was 3 (mutual cooperation) or 5 (you defected while the
# opponent cooperated), repeat whatever action you just played. - If your last-
# round payoff was 0 (you cooperated while the opponent defected) or 1 (mutual
# defection), switch to the opposite action.  This win-stay/lose-shift rule lets
# you persist with actions that brought satisfactory outcomes (at least the
# reward of 3) and change behaviour after unsatisfactory outcomes, without
# directly considering the opponent’s moves or payoffs.

class Neutral_18(LLM_Strategy):
  n = 18
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_action = axl.Action.C
          return axl.Action.C
  
      last_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_payoff in (3, 5):
          return self.history[-1]
      else:
          return axl.Action.D if self.history[-1] == axl.Action.C else axl.Action.C



# If the opponent cooperated in both of the last two rounds, then cooperate.
# Otherwise, defect.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2 or len(opponent.history) < 2:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in the first round. For every round after the first,
# follow this rule:  - If your payoff in the previous round was 3 (mutual
# cooperation) or 5 (you defected and the opponent cooperated), repeat your
# previous action. - If your payoff was 0 (you cooperated and the opponent
# defected) or 1 (mutual defection), switch to the opposite action.  Apply this
# condition at the beginning of each new round before making your choice.

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
  
      last_my_action = self.history[-1]
      last_my_score = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_my_score in (3, 5):
          return last_my_action
      else:
          return axl.Action.D if last_my_action == axl.Action.C else axl.Action.C



# Start by cooperating in round 1.   In every round after the first:  - If both
# you and your opponent chose the same action in the previous round (both C or
# both D), cooperate. - If you and your opponent chose different actions in the
# previous round (one C, one D), defect.

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# In every round, regardless of the opponent’s previous actions or the round
# number, play D (defect). Never play C under any condition.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating on round 1.   For every round after the first:  - If your
# opponent chose C in the previous round, then you choose C.   - If your
# opponent chose D in the previous round **and you also chose D** in that round,
# then you choose C.   - If your opponent chose D in the previous round **and
# you chose C** in that round, then you choose D.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D



# Begin by cooperating on the first round. For rounds 2 through 999, do exactly
# what your opponent did in the previous round. On round 1000, defect
# unconditionally.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]



# Always defect in every round, regardless of what the opponent does.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round. In each subsequent round, cooperate
# unless the opponent defected in both of the two most recent rounds; only then
# should you defect. This simple rule ensures you begin cooperatively, forgive
# isolated defections, and only retaliate against persistent defection.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the first round.   In every subsequent round, play
# exactly what your opponent played in the previous round: if they cooperated,
# cooperate; if they defected, defect.   Maintain this rule consistently for all
# 1000 rounds.

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
      return opponent.history[-1]



# Always defect in every round, regardless of your opponent’s actions. This
# guarantees you never receive the lowest payoff of 0, while allowing you to
# score 5 whenever your opponent cooperates.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Begin by cooperating in the first round. For every round after the first,
# cooperate if the opponent cooperated in the immediately preceding round;
# defect if the opponent defected in the immediately preceding round.

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
      return opponent.history[-1]



# In the first round, cooperate.  In every subsequent round: 1. If your opponent
# cooperated in the previous round, then cooperate. 2. If your opponent defected
# in the previous round, then defect.  This mirrors the opponent's last move
# throughout all 1000 rounds, promoting mutual cooperation while retaliating
# immediately against defection.

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



# Defect on the first round. For every round after the first, cooperate if and
# only if the opponent cooperated in the immediately preceding round; otherwise,
# defect.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# Start by cooperating in the first round. For every round after the first,
# cooperate if the opponent cooperated in the immediately preceding round;
# otherwise, defect.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# Start by cooperating in the first round. Then, for every round after that,
# play exactly what your opponent played in the previous round: cooperate if
# they cooperated, defect if they defected. This mirrors their actions without
# initiating defection and keeps the strategy neutral.

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
      return opponent.history[-1]



# Start by defecting. In every round after the first, simply copy your
# opponent's previous move: if they cooperated last round, cooperate this round;
# if they defected last round, defect this round.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return opponent.history[-1]



# Start by cooperating in the first round. In every round after that, follow
# these rules in order:  1. If your payoff last round was 3 (you both
# cooperated) or 5 (you defected and your opponent cooperated), repeat your
# previous action. 2. If your payoff last round was 0 (you cooperated and your
# opponent defected) or 1 (you both defected), switch to the opposite action.

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
  
      last_my_action = self.history[-1]
      last_my_score = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_my_score in (3, 5):
          return last_my_action
      if last_my_score in (0, 1):
          return axl.Action.D if last_my_action == axl.Action.C else axl.Action.C
  
      return last_my_action



# Start by cooperating in the first round.  From the second round onward: - If
# the opponent cooperated in the previous round, cooperate. - If the opponent
# defected in the previous round, defect.  Follow this rule every round until
# the game ends.

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



# Defect on every round, no matter what the opponent does. Never cooperate.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round. Then, for every round after the
# first, do exactly what your opponent did in the previous round. Cooperate if
# they cooperated; defect if they defected.

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
      return opponent.history[-1]



# Start by cooperating in the first round. For every round after that, simply
# repeat the opponent’s action from the previous round: cooperate if they
# cooperated, defect if they defected. Apply this rule consistently all the way
# through round 1000.

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