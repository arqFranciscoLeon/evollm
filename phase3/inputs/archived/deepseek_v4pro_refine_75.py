import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# Adopt the following decision procedure.  Keep a running count of how many
# times in a row your opponent has cooperated, but restart that count from zero
# whenever you yourself cooperate. The count starts at zero before the first
# round.  - In the first round, always defect. - In every later round, before
# choosing your move, update the count based on your opponent’s move in the
# immediately preceding round:     * If the opponent defected, set the count to
# zero.     * If the opponent cooperated, increase the count by one. - Then
# select your move:     * If the count is exactly 2, cooperate.     * Otherwise,
# defect. - After you have cooperated, immediately set the count to zero (before
# the next round begins), regardless of what your opponent did in the round
# where you cooperated.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._coop_streak = 0
          return axl.Action.D
  
      if not hasattr(self, "_coop_streak"):
          self._coop_streak = 0
  
      if opponent.history[-1] == axl.Action.D:
          self._coop_streak = 0
      else:
          self._coop_streak += 1
  
      if self._coop_streak == 2:
          self._coop_streak = 0
          return axl.Action.C
  
      return axl.Action.D



# Here is the strategy restated with the same logical structure, since no
# mistakes were found:  Begin by cooperating on round 1. For rounds 2 through
# 999, mirror your opponent’s immediately preceding action: cooperate if they
# cooperated, defect if they defected. On the final round, round 1000, always
# defect.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1]



# Start by cooperating in the first round. In every round from the second
# through the 999th, follow this rule: if you and your opponent chose the same
# action in the previous round (both cooperated or both defected), then
# cooperate; if you chose different actions, then defect. In the final 1000th
# round, always defect.

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
      if len(self.history) >= 999:
          return axl.Action.D
      return axl.Action.C if self.history[-1] == opponent.history[-1] else axl.Action.D



# Defect on the first round. For every subsequent round except the final one,
# decide your move using this rule: if your payoff in the immediately previous
# round was 5 or 3, repeat the same action you just played; if your payoff was 1
# or 0, switch to the opposite action. On the 1000th round, always defect
# regardless of the previous outcome.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      last_my_action = self.history[-1]
      last_my_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_my_score in (5, 3):
          return last_my_action
      if last_my_score in (1, 0):
          return axl.Action.C if last_my_action == axl.Action.D else axl.Action.D
  
      return axl.Action.D



# Start by cooperating in the first round. In each following round, decide based
# on what happened in the previous round, applying these rules in order:  1. If
# your opponent cooperated, cooperate. 2. If your opponent defected and you also
# defected, cooperate to restart cooperation. 3. If your opponent defected and
# you cooperated, defect in response.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D



# Start by cooperating in round 1.   For rounds 2 through 999, copy the
# opponent’s action from the immediately preceding round.   In the final round
# (round 1000), always defect regardless of the opponent’s previous move.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1]



# Defect on the first move. For every subsequent move, copy the opponent’s last
# move (cooperate if they cooperated, defect if they defected).

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
      return opponent.history[-1]



# Here is a revised strategy that addresses the critiques:  Start by cooperating
# in round 1.   For rounds 2 through 999, follow these rules in order:  - If
# your opponent cooperated in the previous round, then cooperate this round. -
# If your opponent defected and you also defected in the previous round, then
# cooperate this round.   - If your opponent defected and you cooperated in the
# previous round, then defect this round.  In the 1000th and final round, always
# defect.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D



# Start by cooperating on the first round. For every round after that, use the
# following rules in order:  1. If both you and your opponent played C last
# round, play C this round. 2. If you played C and your opponent played D last
# round, play D this round. 3. If you played D and your opponent played C last
# round, play C this round. 4. If both played D last round, play C this round.

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
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          return axl.Action.D
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C



# Defect on the first round.   For every round after the first, observe the
# opponent’s action in the immediately preceding round. If the opponent
# cooperated in that previous round, then cooperate. If the opponent defected in
# that previous round, then defect.

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



# Here is a revised strategy that addresses the finite horizon and adds a
# recovery mechanism:  - In the first round, cooperate. - For rounds 2 through
# 999:   - If your opponent cooperated in the immediately preceding round,
# cooperate.   - If your opponent defected in the immediately preceding round,
# then:     - Cooperate if both you and your opponent defected in the round
# before that (i.e., the previous two rounds were mutual defection).     -
# Otherwise, defect. - In round 1000, always defect.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D



# Cooperate on round 1.   For rounds 2 through 999:   - If your opponent
# cooperated in the previous round, cooperate.   - If your opponent defected in
# the previous round, then:     - If both you and your opponent defected in each
# of the two most recent rounds, cooperate.     - Otherwise, defect.   On round
# 1000, always defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return axl.Action.D



# Start by defecting on round one. For every round after the first, look at the
# payoff you received in the immediately preceding round. If that payoff was 3
# or higher, keep playing the same move you used in that previous round. If that
# payoff was lower than 3, play the opposite move from the one you used in that
# previous round.

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
  
      last_action = self.history[-1]
      last_my_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_my_score >= 3:
          return last_action
      else:
          return axl.Action.C if last_action == axl.Action.D else axl.Action.D



# On round 1, cooperate. From round 2 through round 999, follow this rule: if
# you scored 3 or 5 points in the previous round, repeat the move you just made;
# if you scored 0 or 1 point, switch to the opposite move. On round 1000, always
# defect.

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
  
      if round_number == 1000:
          return axl.Action.D
  
      last_my_move = self.history[-1]
      last_my_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_my_score in (3, 5):
          return last_my_move
      if last_my_score in (0, 1):
          return last_my_move.flip()
  
      return last_my_move



# Begin by cooperating in round 1.  For rounds 2 through 999, follow these rules
# in order:  1. If at any point you have observed that the opponent defected in
# three consecutive rounds (the most recent three rounds all show defection),
# then from the very next round onward abandon all other rules and always defect
# for the remainder of the game, including round 1000. 2. If the opponent
# cooperated in the previous round, cooperate. 3. If the opponent defected in
# the previous round but cooperated in the round before that, cooperate (you
# forgive a single defection). 4. If the opponent defected in both of the
# previous two rounds, defect.  In round 1000, always defect.

class Neutral_5(LLM_Strategy):
  n = 5
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._opponent_defect_streak_triggered = False
          return axl.Action.C
  
      if getattr(self, "_opponent_defect_streak_triggered", False):
          return axl.Action.D
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          self._opponent_defect_streak_triggered = True
          return axl.Action.D
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.D



# Here is a strategy that starts aggressively, exploits unconditional
# cooperators heavily, but shifts to secure high payoffs when facing
# retaliation:  - In the very first round, defect. - After that, if your
# opponent cooperated in the previous round, continue defecting (stay in
# exploitation mode). - If you and your opponent both defected in the previous
# round—meaning your defection was met with defection—shift to a two‑round
# reconciliation attempt: cooperate on your next two moves. - After those two
# cooperation moves, look at the opponent’s second response:   - If they
# cooperated on that second reconciliation round (so you earned 3), switch to
# cooperating unconditionally for the rest of the game (mutual cooperation is
# now established).   - If they defected on either of the two reconciliation
# rounds (you earned 0 at least once), abandon the attempt and switch to
# defecting unconditionally for the rest of the game (they are unwilling to
# cooperate consistently). - If you ever enter the unconditional cooperation or
# unconditional defection state, stick to that move for all remaining rounds.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mode = "exploit"
          self._recon_count = 0
          self._recon_results = []
          return axl.Action.D
  
      if getattr(self, "_mode", None) == "coop":
          return axl.Action.C
  
      if getattr(self, "_mode", None) == "defect":
          return axl.Action.D
  
      # Exploitation mode
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      # Opponent defected last round.
      # If we defected too, begin reconciliation.
      if self.history[-1] == axl.Action.D:
          self._mode = "recon"
          self._recon_count = 0
          self._recon_results = []
          return axl.Action.C
  
      # We cooperated and they defected: keep exploiting by defecting.
      return axl.Action.D
  
      # Reconciliation mode is handled below.
      # (Unreachable here, but kept for clarity.)
  
      if getattr(self, "_mode", None) == "recon":
          self._recon_count += 1
          self._recon_results.append(opponent.history[-1])
  
          if self._recon_count < 2:
              return axl.Action.C
  
          # After two reconciliation moves, decide based on opponent's responses.
          if self._recon_results[-1] == axl.Action.C:
              self._mode = "coop"
              return axl.Action.C
          else:
              self._mode = "defect"
              return axl.Action.D



# Start by cooperating in round 1.   For rounds 2 through 998, decide your move
# solely by looking at the outcome of the immediately preceding round:   - If in
# that round both players received the same payoff (both got 3 from cooperating,
# or both got 1 from defecting), then cooperate.   - If in that round the
# payoffs differed (you got 0 and the opponent got 5, or you got 5 and the
# opponent got 0), then defect.   In rounds 999 and 1000, defect regardless of
# the history.

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
  
      if round_number >= 999:
          return axl.Action.D
  
      my_last, opp_last = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if my_last == opp_last:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in the first round.   For rounds 2 to 999, determine your
# move as follows: if your payoff in the immediately preceding round was either
# 3 or 5, repeat the action you played in that round. If your payoff was either
# 0 or 1, switch to the opposite action.   In the final round (round 1000),
# always defect.

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
  
      if round_number == 1000:
          return axl.Action.D
  
      last_self_action = self.history[-1]
      last_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_payoff in (3, 5):
          return last_self_action
      if last_payoff in (0, 1):
          return axl.Action.D if last_self_action == axl.Action.C else axl.Action.C
  
      return last_self_action



# Defect in every single round without exception. Do not consider the opponent’s
# history or any other condition—simply choose Defect for all 1000 rounds.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing C in round 1.   In round 2, play C regardless of what the
# opponent did in round 1.   From round 3 onward:  - If the opponent played C in
# the immediately previous round, play C.   - If the opponent played D in the
# immediately previous round:     - If the opponent also played D in the round
# before that, play D.     - Otherwise (the opponent played C in the round
# before that), play C.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# In the first round, cooperate. For rounds 2 through 999, follow these rules in
# order:  1. If your opponent cooperated in the immediately previous round, you
# cooperate. 2. If your opponent defected in the immediately previous round, you
# defect with 90% probability and cooperate with 10% probability.  In the final
# round (round 1000), always defect regardless of history.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)



# In round 1, defect.  In every round from 2 to 999, copy the move your opponent
# made in the previous round: if they cooperated, cooperate; if they defected,
# defect.  In round 1000, defect regardless of the opponent’s previous move.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1]



# Start by cooperating in the first round. For rounds 2 through 999, follow
# these rules in order:  - If your opponent cooperated in the immediately
# previous round, then cooperate. - If your opponent defected in the immediately
# previous round and you also defected in that round (meaning both chose D),
# then cooperate. - If your opponent defected in the immediately previous round
# and you cooperated in that round, then defect.  In the final round (round
# 1000), defect regardless of the opponent’s previous move.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.C



# Cooperate in the first round. For rounds 2 through 999, if the opponent
# cooperated in the immediately previous round, then cooperate; if the opponent
# defected in the immediately previous round, then defect. In round 1000, always
# defect regardless of the opponent's previous move.

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
  
      return opponent.history[-1]



# Defect on the first round. Cooperate unconditionally on the second round. From
# the third round onward, copy your opponent's move from the previous round. If
# you ever experience three consecutive rounds where both players defect,
# cooperate once on the next round to try to restore mutual cooperation, then
# resume copying your opponent's previous move.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._restore_cooperate_next = False
          return axl.Action.D
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if len(self.history) >= 3:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and self.history[-3] == axl.Action.D
          ):
              self._restore_cooperate_next = True
  
      if getattr(self, "_restore_cooperate_next", False):
          self._restore_cooperate_next = False
          return axl.Action.C
  
      return opponent.history[-1]



# Start by cooperating in the first round.   In the final round (round 1000),
# always defect.   In all other rounds, apply the following rules in order:
# 1. If you defected in the previous round as a direct response to your
# opponent’s defection, then cooperate unconditionally in this round.   2.
# Otherwise, if your opponent cooperated in the previous round, cooperate.   3.
# Otherwise, if your opponent defected in the previous round, defect.

class Cooperative_9(LLM_Strategy):
  n = 9
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defected_in_response = False
          return axl.Action.C
  
      if len(self.history) == 999:
          return axl.Action.D
  
      if getattr(self, "_defected_in_response", False):
          self._defected_in_response = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      self._defected_in_response = True
      return axl.Action.D



# Start by cooperating in the first round. Thereafter, in each round, cooperate
# if your opponent cooperated in the previous round, and defect if your opponent
# defected in the previous round. This simple mirroring rule is repeated for all
# 1000 rounds.

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



# Start by defecting in round one. For every round thereafter, if the opponent
# cooperated in the immediately preceding round, then cooperate; if the opponent
# defected in the immediately preceding round, then defect.

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



# Start by cooperating on round 1. On each subsequent round, cooperate if the
# opponent cooperated in the previous round, and defect if the opponent defected
# in the previous round.

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



# Start with cooperation in round one. Thereafter, mimic your opponent’s move
# from the previous round: if they cooperated, then cooperate; if they defected,
# then defect.

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
      return opponent.history[-1]



# Here is the revised strategy, with the early-round ambiguity resolved:  1.
# **Round 1**: Defect unconditionally.   2. **Round 2**: If you have not yet
# cooperated, defect unconditionally (since the opponent’s last two moves cannot
# yet be evaluated).   3. **From round 3 onward, as long as you have never
# cooperated**:      - Cooperate if the opponent’s last two moves were both
# Cooperate.      - Otherwise, defect.   4. **Once you have cooperated at least
# once**:      - Cooperate if the opponent’s last move was Cooperate.      - If
# the opponent ever plays Defect, immediately defect on that round and continue
# defecting for all remaining rounds.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._has_cooperated = False
          self._permanent_defect = False
          return axl.Action.D
  
      if getattr(self, "_permanent_defect", False):
          return axl.Action.D
  
      if getattr(self, "_has_cooperated", False):
          if opponent.history and opponent.history[-1] == axl.Action.D:
              self._permanent_defect = True
              return axl.Action.D
          return axl.Action.C
  
      if len(self.history) < 2:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          self._has_cooperated = True
          return axl.Action.C
  
      return axl.Action.D



# Here is the strategy, restated with the same logic but in a slightly more
# explicit form:  Start by cooperating in round 1. For every round from 2
# through 999, look at what your opponent did in the immediately preceding
# round: if they cooperated, you cooperate; if they defected, you defect. In the
# very last round, round 1000, always defect, no matter what the opponent did in
# round 999.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1]



# Start by cooperating in the first round. From round 2 through round 999,
# decide as follows:  - If the previous round ended with both players choosing
# the same action (both cooperated or both defected), then cooperate. - If the
# previous round ended with the two players choosing different actions (you
# cooperated and the opponent defected, or you defected and the opponent
# cooperated), then defect.  In round 1000, always defect, regardless of the
# previous outcome.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# Start by defecting in round one. For every round after that, cooperate only if
# the opponent cooperated in the immediately preceding round. If the opponent
# defected in the previous round, defect.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# Start by cooperating in the first round. For every round after the first,
# apply the following rules in order:  1. If both players defected in each of
# the two most recent rounds, cooperate. 2. Otherwise, repeat the opponent’s
# move from the immediately previous round.  This rule applies to all rounds,
# including the final round, with no special end-of-game defection.

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
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return opponent.history[-1]



# Start with cooperation on round one. For each subsequent round, look at what
# your opponent did in the immediately preceding round: if they cooperated, you
# cooperate; if they defected, you defect. Apply this rule consistently for all
# 1000 rounds.

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



# Here is the strategy restated, preserving the exact logic:  1. Defect on round
# 1.   2. For every round after the first, examine the opponent’s full history
# of moves so far. If the opponent has defected even once, defect
# unconditionally in all remaining rounds.   3. Only if the opponent has
# cooperated in every single round up to the current one (a perfect record of C
# from round 1 onward), cooperate.

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
  
      if axl.Action.D in opponent.history:
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the very first round. For all subsequent rounds,
# decide as follows:  - If both you and your opponent cooperated in the previous
# round, cooperate. - If you cooperated and your opponent defected in the
# previous round, defect. - If both you and your opponent defected in the
# previous round, cooperate. - If you defected and your opponent cooperated in
# the previous round, cooperate.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C



# Start by cooperating in the first round. For rounds 2 through 999, look at
# your opponent’s move in the immediately preceding round: if they cooperated,
# you cooperate; if they defected, you defect. In round 1000, always defect.

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
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1]



# Start by defecting on the first move. After that, always defect unless the
# previous round’s outcome was you defecting and your opponent cooperating. In
# that specific case only, cooperate once on the very next round, then
# immediately return to defecting.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._cooperate_next = False
          return axl.Action.D
  
      if getattr(self, "_cooperate_next", False):
          self._cooperate_next = False
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          self._cooperate_next = True
  
      return axl.Action.D



# Start by cooperating in the first two rounds. From round three onward,
# cooperate unless the opponent chose D in both of the previous two rounds; if
# they did, choose D.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# Start by cooperating in the first round.   For every round after that, follow
# these two rules in order:    1. If you and your opponent made the same choice
# in the previous round (both cooperated or both defected), then cooperate.   2.
# If you and your opponent made different choices in the previous round, then
# defect.

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



# Defect on every round regardless of your opponent’s actions.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating on round 1. For each subsequent round, copy your
# opponent’s action from the immediately preceding round: if they cooperated,
# you cooperate; if they defected, you defect. Continue this pattern for all
# 1000 rounds.

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



# Here is the revised strategy:  Start by cooperating in the first round.   For
# every round after the first, apply the following rules in the exact order
# listed:  1. If you have defected in both of the two immediately preceding
# rounds, cooperate. 2. Otherwise, if your opponent defected in the immediately
# preceding round, defect. 3. Otherwise, if fewer than 10 rounds have been
# completed so far, cooperate. 4. Otherwise, if your opponent's overall
# cooperation rate across all previous rounds is at least 70%, cooperate. 5.
# Otherwise, defect.

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
  
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if len(self.history) < 10:
          return axl.Action.C
  
      if opponent.history.cooperations / len(opponent.history) >= 0.7:
          return axl.Action.C
  
      return axl.Action.D



# Here is the strategy, unchanged as no logical mistakes were found, presented
# clearly with ordered conditions:  1. Always defect on the first round. 2. For
# every round after the first, look at what your opponent chose in the
# immediately preceding round:      - If they cooperated, you cooperate.      -
# If they defected, you defect.

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
      return opponent.history[-1]



# Start by cooperating on round 1.   For rounds 2 through 950, do the following:
# look at your opponent’s move from the previous round. If they cooperated, you
# cooperate. If they defected, you defect — unless both you and your opponent
# defected last round, in which case you cooperate instead to break a mutual
# defection cycle.   For rounds 951 through 1000, always defect, no matter what
# your opponent does.

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
  
      round_number = len(self.history) + 1
  
      if round_number >= 951:
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.C:
          return axl.Action.C
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D



# Start by cooperating on round 1. For every round after that, look at what your
# opponent did in the immediately previous round: if they cooperated, you
# cooperate; if they defected, you defect.

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



# Start by following a fixed sequence for the first three rounds: on round 1,
# choose D; on round 2, choose C; on round 3, choose C.  After these three
# rounds, examine your opponent’s moves in rounds 1, 2, and 3.   - If your
# opponent played C in all three of those rounds (C, C, C), then choose D in
# every remaining round.   - If your opponent played D at least once during
# those first three rounds, then from round 4 onward simply copy your opponent’s
# move from the immediately previous round every round.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._fixed_phase = True
          self._opponent_all_c = None
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 2:
          return axl.Action.C
      if round_number == 3:
          return axl.Action.C
  
      if round_number == 4:
          first_three_opponent = list(opponent.history[:3])
          self._opponent_all_c = all(move == axl.Action.C for move in first_three_opponent)
          self._fixed_phase = False
  
      if self._opponent_all_c:
          return axl.Action.D
  
      return opponent.history[-1]



# Here is a revised strategy that addresses the previous critiques:  Start by
# cooperating in the first round. For every round after that up to round 999,
# follow this rule: if your opponent cooperated in the most recent round,
# cooperate. If your opponent defected in the most recent round but cooperated
# in the round before that, forgive the single defection and cooperate. If your
# opponent defected in both of the last two rounds, defect. On the final round,
# round 1000, always defect regardless of the opponent's history.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if len(opponent.history) == 0:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Here is the revised strategy, with conditions ordered by priority:  1. In the
# very first round, cooperate. 2. In round 1000, defect no matter what. 3. In
# any other round that is a multiple of 100 (rounds 100, 200, 300, …, 900),
# cooperate regardless of the opponent’s previous move. 4. In all remaining
# rounds, simply mirror the opponent’s last move: cooperate if they cooperated
# in the previous round, defect if they defected.

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
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if round_number % 100 == 0:
          return axl.Action.C
  
      return opponent.history[-1]



# Start the first round by defecting. After each round:  - If your payoff in the
# previous round was 5 or 3, then in the next round, repeat the same action you
# just played. - If your payoff in the previous round was 0 or 1, then in the
# next round, play the opposite action to what you just played.

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
  
      last_action = self.history[-1]
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if my_last_score in (5, 3):
          return last_action
      if my_last_score in (0, 1):
          return axl.Action.C if last_action == axl.Action.D else axl.Action.D
  
      return last_action



# Here is the strategy, rewritten for clarity while preserving its original
# logic:  1. In the very first round, cooperate. 2. For every round after the
# first, look at what happened in the immediately preceding round:    - If you
# and your opponent made the same choice (both cooperated or both defected),
# then cooperate in the current round.    - If you and your opponent made
# different choices (one cooperated and the other defected), then defect in the
# current round.

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
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in the first round. For rounds 2 through 999, follow
# these rules in order:  1. If you defected in the previous round and your
# opponent cooperated, cooperate in the current round to restore cooperation
# after any accidental defection. 2. Otherwise, if your opponent defected in the
# previous round, defect in the current round. 3. Otherwise, cooperate.  In the
# final round 1000, always defect regardless of history.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Defect on the first round. Then, for all remaining rounds, choose your action
# based on the opponent's previous move:  - If the opponent cooperated on the
# previous round, defect. - If the opponent defected on the previous round,
# defect.  In other words, after the initial defection, continue to defect
# unconditionally regardless of what the opponent does. Never cooperate at any
# point.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round. For all later rounds: cooperate if in
# the previous round you and your opponent made the same choice (both cooperated
# or both defected); otherwise, defect.

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# In round 1, cooperate.  For rounds 2 through 999, cooperate if the opponent
# cooperated in the immediately preceding round; defect if the opponent defected
# in the immediately preceding round.  In round 1000, defect unconditionally.

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
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      return opponent.history[-1] if opponent.history else axl.Action.C



# Start by defecting in the first round. For every round after that:  -
# Cooperate if your opponent cooperated in the previous round. - Defect if your
# opponent defected in the previous round.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# Start by cooperating on the very first round. For each round after the first,
# decide as follows:  1. If your previous move was Cooperate and the opponent’s
# previous move was Defect, play Defect this round. 2. If your previous move was
# Defect and that defection was triggered by rule 1 (the opponent had just
# defected against your cooperation), play Cooperate this round regardless of
# what the opponent just did. 3. In all other cases, play Cooperate.

class Cooperative_20(LLM_Strategy):
  n = 20
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._triggered_by_rule1 = False
          return axl.Action.C
  
      if getattr(self, "_triggered_by_rule1", False):
          self._triggered_by_rule1 = False
          return axl.Action.C
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._triggered_by_rule1 = True
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the first round. For every round after the first, look
# at the immediately previous round’s outcome and follow these rules in order: -
# If both players chose the same action (both Cooperated or both Defected), then
# Cooperate. - If the players chose different actions (one Cooperated, one
# Defected), then Defect.  Assessment: - The rewritten strategy contains no
# logical mistakes.

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# Defect on the first move. Thereafter, if the opponent has never cooperated in
# any previous round, continue defecting. Once the opponent cooperates for the
# first time, cooperate on the next two rounds regardless of what the opponent
# does. After those two rounds, copy the opponent’s move from the previous round
# for the rest of the game.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._opponent_cooperated_once = False
          self._post_first_coop_rounds = 0
          return axl.Action.D
  
      if self._post_first_coop_rounds > 0:
          self._post_first_coop_rounds -= 1
          return axl.Action.C
  
      if not self._opponent_cooperated_once:
          if axl.Action.C in opponent.history:
              self._opponent_cooperated_once = True
              self._post_first_coop_rounds = 2
              return axl.Action.C
          return axl.Action.D
  
      return opponent.history[-1]



# Cooperate in the first round.   For rounds 2 through 999, play whatever the
# opponent played in the immediately preceding round.   In round 1000, always
# defect.

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
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1]



# Cooperate in the first round. In every round after the first, simply repeat
# whatever action your opponent chose in the previous round.

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



# Start by defecting on the first round. After that, for every remaining round:
# if in the previous round you earned 5 or 3 points, repeat your last move; if
# you earned 0 or 1 points, switch to the opposite move.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if my_last_score in (5, 3):
          return last_self
      if my_last_score in (0, 1):
          return axl.Action.C if last_self == axl.Action.D else axl.Action.D
  
      return last_self



# In every round, without exception, play C.

class Neutral_22(LLM_Strategy):
  n = 22
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.C



# Always defect on every round, with no exceptions. Because the game has a known
# finite length and the payoff structure punishes cooperation when facing a
# defector, a relentlessly aggressive move—choosing D unconditionally—prevents
# you from ever receiving the sucker’s payoff of 0 and locks in a minimum of 1
# point per round regardless of what your opponent does. If your opponent ever
# cooperates, you capitalize with a score of 5. This approach never offers a
# chance to be exploited and maximizes your worst-case and potentially your
# total payoff.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Cooperate on the first round.   For every round after the first, in order:
# 1. If both you and your opponent played D in the previous round, play C.   2.
# Otherwise, copy your opponent’s previous move (C for C, D for D).

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
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]



# Start by cooperating in the first round. For every round after that, simply
# repeat the opponent’s move from the previous round: cooperate if they
# cooperated, defect if they defected.

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



# Defect on round 1.    After round 1, keep track of a permanent defection state
# that starts as inactive.   On each subsequent round, apply the following rules
# in order:  1. If permanent defection is active, defect. 2. If you cooperated
# in the previous round and your opponent defected in that same round, activate
# permanent defection and defect this round. 3. If permanent defection is
# inactive and the opponent has played C in both of the last two rounds (if
# fewer than two rounds exist, this condition is false), then cooperate. 4. In
# all other cases, defect.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._permanent_defection = False
          return axl.Action.D
  
      if self._permanent_defection:
          return axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._permanent_defection = True
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Cooperate in the first round. Afterwards:  - If you cooperated last round,
# copy your opponent’s last move—cooperate if they cooperated, defect if they
# defected. - If you defected last round, cooperate no matter what your opponent
# did.

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
  
      if self.history[-1] == axl.Action.C:
          return opponent.history[-1]
      else:
          return axl.Action.C



# On the first round, cooperate.   For all later rounds:   - Cooperate if both
# players chose identical actions in the previous round (both C or both D).   -
# Defect if the previous round’s actions were different (C vs D or D vs C).

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
  
      return axl.Action.C if self.history[-1] == opponent.history[-1] else axl.Action.D



# In the first round, defect.   For every round after the first, cooperate if
# your opponent cooperated in the immediate previous round, and defect if your
# opponent defected in the immediate previous round.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# Start by cooperating in the first round. From round two onward, follow these
# rules in order:  1. If both you and your opponent defected in the previous
# round, cooperate to try to restore mutual cooperation. 2. If your opponent
# defected while you cooperated in the previous round, defect to punish the
# betrayal. 3. If you defected while your opponent cooperated in the previous
# round, return to cooperation. 4. If both cooperated in the previous round,
# continue cooperating.

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
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          return axl.Action.D
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.C
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C



# Start by cooperating on round 1. For each round after that, do whatever your
# opponent did in the immediately preceding round: cooperate if they just
# cooperated, defect if they just defected.

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



# Start by playing Cooperate in the first round. In every later round, simply
# repeat whatever your opponent did in the round immediately before: if they
# Cooperated last round, you Cooperate now; if they Defected last round, you
# Defect now. Apply this rule consistently for all remaining rounds.

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