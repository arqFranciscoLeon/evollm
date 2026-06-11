import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# Always choose defect. Do not cooperate under any circumstances.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round. In each subsequent round, look at the
# actual actions taken (including any flips) by you and your opponent in the
# immediately preceding round:  1. If both of you took the same action (both
# Cooperate or both Defect), then you should Cooperate this round. 2. If you and
# your opponent took different actions (one Cooperate and one Defect), then you
# should Defect this round.  Follow this rule every round, ignoring any other
# information beyond the last round’s observed actions.

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
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == opp_last:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in the first round. Then, for every round after the
# first, decide based on your opponent’s most recent actions:  1. If the
# opponent cooperated in the last round, cooperate. 2. If the opponent defected
# in the last round, check the round before that:    - If the opponent also
# defected in that earlier round (two consecutive defections), cooperate.    -
# Otherwise (only one defection in the last two rounds), defect.  This rule uses
# only the opponent’s last two moves and resets cycles of mutual defection
# without requiring randomisation.

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
  
      opp_history = opponent.history
  
      if len(opp_history) == 0:
          return axl.Action.C
  
      if opp_history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opp_history) >= 2 and opp_history[-2] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D



# Here is a simple aggressive strategy for the 1000-round game:  1. **Start by
# defecting.** Open with D and continue defecting for the first 10 rounds,
# regardless of what the opponent does.  2. **After round 10, assess the
# opponent's behavior.** Calculate the percentage of times the opponent
# cooperated over the last 10 rounds.  3. **If the opponent cooperated in fewer
# than 30% of the last 10 rounds, keep defecting.** The opponent is likely
# hostile or uncooperative, so continue playing D to avoid being exploited.  4.
# **If the opponent cooperated in 30% or more of the last 10 rounds, switch to a
# punishing pattern.** Play D for the next 3 rounds, then play C exactly once.
# If the opponent ever plays D during your C round, immediately return to D for
# the next 5 rounds before trying C once again. If the opponent plays C during
# your C round, continue the pattern of three Ds followed by one C.  5. **Every
# 10 rounds, re-evaluate** the opponent's cooperation rate over the last 10
# rounds and adjust according to steps 3 and 4.  6. **In the final 10 rounds,
# always defect.** There is no future to influence, so exploit without
# restraint.  This strategy maximizes your payoff by defaulting to defection,
# only offering rare cooperative probes to harvest points from forgiving
# opponents, and punishing any sign of resistance harshly and immediately.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_until = 0
          self._probe_mode = False
          self._probe_cycle = 0
          return axl.Action.D
  
      round_number = len(self.history) + 1
      total_rounds = 1000
  
      if round_number > total_rounds - 10:
          return axl.Action.D
  
      if round_number <= 10:
          return axl.Action.D
  
      if self._punish_until and round_number <= self._punish_until:
          return axl.Action.D
  
      if (round_number - 1) % 10 == 0:
          last_10 = opponent.history[-10:]
          coop_rate = last_10.count(axl.Action.C) / 10
  
          if coop_rate < 0.3:
              self._probe_mode = False
              self._probe_cycle = 0
              return axl.Action.D
  
          self._probe_mode = True
          self._probe_cycle = 0
  
      if not self._probe_mode:
          return axl.Action.D
  
      if self._probe_cycle < 3:
          self._probe_cycle += 1
          return axl.Action.D
  
      self._probe_cycle = 0
      if opponent.history and opponent.history[-1] == axl.Action.D:
          self._punish_until = round_number + 4
          self._probe_mode = False
          return axl.Action.D
  
      return axl.Action.C



# Begin by cooperating in the first round. In all later rounds, cooperate if
# both players chose the same action in the previous round (both C or both D).
# If the previous round’s actions differed (one C, one D), defect. This rule
# uses the actual, possibly noisy, outcomes you observe.

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in the first round. For every round after the first, look
# at the actual actions taken by both players in the previous round (after noise
# has been applied). If both players chose the same action—both cooperated or
# both defected—then cooperate. If the players chose different actions—one
# cooperated and the other defected—then defect.

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# In each round, you decide whether to cooperate or defect based solely on your
# opponent's past actions that you have observed, with no attempt to correct for
# noise. Follow these rules in order:  1. **First round:** Defect
# unconditionally. 2. **Rounds 2 through 990:** Cooperate only if the opponent's
# observed moves in the last 5 rounds contain **at least 4 cooperations**.
# Otherwise, defect. If fewer than 5 rounds have elapsed, use all available data
# and apply the same requirement; since 4 cooperations cannot be met in fewer
# than 4 rounds, this means you will defect at least through the first four
# rounds. 3. **Rounds 991 through 1000:** Ignore all history and **always
# defect**, regardless of the opponent's behavior.  This strategy is aggressive
# because it defects by default, cooperates only as a rare reward when the
# opponent has been extremely cooperative recently, and locks into pure
# defection in the final phase to exploit the end-of-game uncertainty.

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
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      recent_opponent_moves = opponent.history[-5:]
      if recent_opponent_moves.count(axl.Action.C) >= 4:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in the first round. For every round after that, base your
# decision on the actual outcome of the previous round (the actions you both
# ended up playing, after any noise):  - If both players chose the same action
# (both cooperated or both defected), cooperate. - If the players chose
# different actions (one cooperated and the other defected), defect.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == last_opp:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in the first round. For every subsequent round, follow
# this rule:  - If your payoff in the previous round was either 3 or 5, repeat
# the action you intended to play in that previous round. - If your payoff in
# the previous round was either 0 or 1, switch to the opposite action of what
# you intended to play in that previous round.  Apply these conditions in order,
# checking only your own realised payoff to decide your next intended move.

class Neutral_3(LLM_Strategy):
  n = 3
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.C
          return self._intended_action
  
      last_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_payoff in (3, 5):
          return self._intended_action
      elif last_payoff in (0, 1):
          return axl.Action.D if self._intended_action == axl.Action.C else axl.Action.C
      else:
          return self._intended_action



# Start by defecting in the first round.  For every following round, check the
# payoff you received in the previous round:  - If you scored 5 (you defected,
# opponent cooperated) or 3 (mutual cooperation), repeat your previous action. -
# If you scored 1 (mutual defection) or 0 (you cooperated, opponent defected),
# switch to the opposite action.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_my_action = self.history[-1]
      last_my_score = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_my_score in (5, 3):
          return last_my_action
      else:
          return last_my_action.flip()



# Here is a simple strategy based on your own payoffs, which naturally handles
# noise and encourages mutual cooperation:  1. In the first round, cooperate. 2.
# After each round, check the payoff you just received:    - If you scored 3 or
# 5, then for the next round repeat the action you used in the round that just
# ended.    - If you scored 0 or 1, then for the next round switch to the
# opposite action (if you cooperated, defect; if you defected, cooperate).

class Cooperative_4(LLM_Strategy):
  n = 4
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_action = axl.Action.C
          return axl.Action.C
  
      last_score = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0] if len(self.history) > 1 else self.score
  
      if last_score in (3, 5):
          self._last_action = self.history[-1]
      elif last_score in (0, 1):
          self._last_action = axl.Action.D if self.history[-1] == axl.Action.C else axl.Action.C
      else:
          self._last_action = self.history[-1]
  
      return self._last_action



# Start by cooperating in the first round. Thereafter, determine your next
# action solely by the payoff you earned in the previous round:  - If you
# received **3** (mutual cooperation) or **5** (you defected and opponent
# cooperated), repeat your previous action. - If you received **0** (you
# cooperated and opponent defected) or **1** (mutual defection), switch to the
# opposite action.

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
  
      last_my_action = self.history[-1]
      last_my_score = self.score - (self.total_scores(self.history[-1:], opponent.history[-1:])[0] if len(self.history) > 0 else 0)
  
      if last_my_score in (3, 5):
          return last_my_action
      if last_my_score in (0, 1):
          return axl.Action.D if last_my_action == axl.Action.C else axl.Action.C
  
      return last_my_action



# Defect on your first move. For each round after the first, look at the
# opponent's observed actions in the previous five rounds (or all rounds so far
# if fewer than five have been played). If the opponent cooperated in at least
# four of those rounds, cooperate. Otherwise, defect.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      recent_opponent_moves = opponent.history[-5:]
      if recent_opponent_moves.count(axl.Action.C) >= 4:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in the first round. After each round, look at the payoff
# you just received. If your payoff was 3 or 5, repeat whatever action you
# played in that round. If your payoff was 0 or 1, switch to the opposite action
# for the next round.

class Cooperative_5(LLM_Strategy):
  n = 5
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_action = axl.Action.C
          return axl.Action.C
  
      last_payoff = self.score - sum(
          self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]
      )
      # The above is not reliable for a single-round payoff, so compute directly from the last round.
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          last_payoff = 3
      elif my_last == axl.Action.C and opp_last == axl.Action.D:
          last_payoff = 0
      elif my_last == axl.Action.D and opp_last == axl.Action.C:
          last_payoff = 5
      else:
          last_payoff = 1
  
      if last_payoff in (3, 5):
          return self.history[-1]
      else:
          return axl.Action.D if self.history[-1] == axl.Action.C else axl.Action.C



# Start by cooperating.  After each round, look at your intended action and your
# payoff: - If your payoff was 3 or 5, repeat your intended action in the next
# round. - If your payoff was 0 or 1, switch to the opposite action in the next
# round.

class Neutral_5(LLM_Strategy):
  n = 5
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.C
          return self._intended_action
  
      last_payoff = self.score - getattr(self, "_last_score", 0)
  
      if last_payoff in (0, 1):
          self._intended_action = axl.Action.D if self._intended_action == axl.Action.C else axl.Action.C
  
      self._last_score = self.score
      return self._intended_action



# Defect in the first round. For all subsequent rounds, base your next action
# solely on your own payoff from the previous round, following these ordered
# rules:  - If your previous payoff was 5 or 3, repeat the same action you just
# played. - If your previous payoff was 0 or 1, switch to the opposite action.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]) if False else None
      # Compute previous-round payoff from the last interaction only.
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
      last_payoff = my_last_score
  
      last_action = self.history[-1]
  
      if last_payoff in (5, 3):
          return last_action
      if last_payoff in (0, 1):
          return axl.Action.C if last_action == axl.Action.D else axl.Action.D
  
      return axl.Action.D



# Start by cooperating in the first round. For every round after that, look at
# the actions both players actually took in the previous round (as you observed
# them, which may include noise).   - If both players took the same action (both
# cooperated or both defected), cooperate in the next round.   - If the players
# took different actions (one cooperated and the other defected), defect in the
# next round.

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
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == opp_last:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in the first round. For every round after the first,
# count the opponent’s observed defections over the most recent 5 rounds
# (including the just-observed move). If that count is 2 or higher, play D;
# otherwise, play C.

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
  
      recent_opponent_defections = opponent.history[-5:].count(axl.Action.D)
      return axl.Action.D if recent_opponent_defections >= 2 else axl.Action.C



# Start by defecting in the first round. After each round, decide your next move
# based on the payoff you just received:  - If your payoff was 5 or 3, repeat
# the action you just played. - If your payoff was 1 or 0, switch to the
# opposite action.  This strategy is aggressive because it opens with defection,
# exploits cooperation relentlessly, and only ventures into cooperation after
# sustained mutual defection or after being punished for cooperating.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_action = axl.Action.D
          return axl.Action.D
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1])[0:1])  # placeholder
      # Compute the payoff from the most recent round directly
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
      last_payoff = my_last_score
  
      if last_payoff in (5, 3):
          self._last_action = self.history[-1]
      elif last_payoff in (1, 0):
          self._last_action = axl.Action.C if self.history[-1] == axl.Action.D else axl.Action.D
      else:
          self._last_action = self.history[-1]
  
      return self._last_action



# Start by cooperating in round 1. For all subsequent rounds, base your next
# action solely on your payoff from the previous round:  - If your payoff was 3
# or 5, repeat the action you intended to play in that previous round. - If your
# payoff was 0 or 1, switch to the opposite action.  This means you continue
# cooperating after mutual cooperation (payoff 3) or after successfully
# defecting (payoff 5), and you switch after being exploited (payoff 0) or after
# mutual defection (payoff 1).

class Cooperative_7(LLM_Strategy):
  n = 7
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_intended_action = axl.Action.C
          return axl.Action.C
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]) if False else None
      # Compute previous-round payoff directly from the last interaction.
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
      last_payoff = my_last_score
  
      if last_payoff in (3, 5):
          return self._last_intended_action
      else:
          self._last_intended_action = axl.Action.D if self._last_intended_action == axl.Action.C else axl.Action.C
          return self._last_intended_action



# Start by cooperating in the first round. For every round after the first,
# follow this rule:  - If in the previous round you and your opponent chose the
# same action (both C or both D), cooperate. - If in the previous round you and
# your opponent chose different actions (one C and one D), defect.  Apply this
# rule regardless of noise or perceived actions, using the actual choices as you
# observed them.

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# Start by defecting. In every round after the first, look at your own payoff
# from the previous round: - If your payoff was 5 or 3, repeat your last action.
# - If your payoff was 0 or 1, switch to the opposite action.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0]
      last_action = self.history[-1]
  
      if last_payoff in (5, 3):
          return last_action
      if last_payoff in (0, 1):
          return axl.Action.C if last_action == axl.Action.D else axl.Action.D
  
      return last_action



# Cooperate in the first round. In all subsequent rounds, base your decision on
# your opponent's observed action in the immediately preceding round. If that
# action was cooperation, then cooperate. If that action was defection, then
# cooperate with a probability of 1/3 (and defect with a probability of 2/3).

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(1 / 3)



# Start by cooperating in the first round.   For every round after the first,
# base your decision solely on your payoff from the immediately preceding round:
# - If your previous payoff was 3 or 5, repeat the action you played in that
# round.   - If your previous payoff was 0 or 1, switch to the opposite action.

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
  
      last_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
      last_action = self.history[-1]
  
      if last_payoff in (3, 5):
          return last_action
      if last_payoff in (0, 1):
          return axl.Action.D if last_action == axl.Action.C else axl.Action.C
  
      return axl.Action.C



# In every round, choose Defect.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round. For every round after that:  - If
# your payoff in the previous round was 3 or 5, then repeat the exact action you
# took in that round. - If your payoff in the previous round was 0 or 1, then
# switch to the opposite action.

class Cooperative_9(LLM_Strategy):
  n = 9
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_action = axl.Action.C
          return axl.Action.C
  
      last_my_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_my_score in (3, 5):
          return self.history[-1]
      elif last_my_score in (0, 1):
          return axl.Action.C if self.history[-1] == axl.Action.D else axl.Action.D
      else:
          return self.history[-1]



# Start by cooperating in the first round. Thereafter, base your action each
# round solely on your own payoff from the previous round:  - If you scored 3
# (both cooperated) or 1 (both defected), repeat the same action you just
# played. - If you scored 0 (you cooperated, opponent defected) or 5 (you
# defected, opponent cooperated), switch to the opposite action.

class Neutral_9(LLM_Strategy):
  n = 9
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_action = axl.Action.C
          return axl.Action.C
  
      last_my_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_my_score in (3, 1):
          return self.history[-1]
      else:
          return axl.Action.D if self.history[-1] == axl.Action.C else axl.Action.C



# Defect in the first round and again in the second round, no matter what the
# opponent does.  From the third round onward, base your move solely on the
# opponent's observed actions in the two most recent rounds (after accounting
# for noise): - Cooperate if and only if you observed the opponent cooperate in
# both of the previous two rounds. - Otherwise, defect.

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(self.history) == 1:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# On the first round, cooperate.  For every round after the first:   - If in the
# previous round both players’ actual actions were the same (both cooperated or
# both defected), cooperate.   - If in the previous round the two players’
# actual actions differed (one cooperated, one defected), defect.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == last_opp:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating on the first round. For every round after that, look at
# the actual moves both players made in the previous round. If the moves were
# the same (both cooperated or both defected), cooperate. If the moves were
# different (one cooperated and the other defected), defect.

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# Start by defecting in the first round, with a consecutive-cooperation count
# set to zero.   At the beginning of each later round, cooperate if you have
# seen your opponent cooperate at least three times in a row; otherwise defect.
# After every round, update the count: if your opponent cooperated, increase it
# by one; if they defected, reset it to zero.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._consecutive_cooperations = 0
          return axl.Action.D
  
      if opponent.history and opponent.history[-1] == axl.Action.C:
          self._consecutive_cooperations += 1
      else:
          self._consecutive_cooperations = 0
  
      if self._consecutive_cooperations >= 3:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in the first round. For every round after the first,
# follow this rule:  - If your payoff in the previous round was 3 or 5, repeat
# your previous action. - If your payoff in the previous round was 0 or 1,
# switch to the opposite action.

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
  
      last_my_action = self.history[-1]
      last_my_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_my_score in (3, 5):
          return last_my_action
      if last_my_score in (0, 1):
          return axl.Action.D if last_my_action == axl.Action.C else axl.Action.C
  
      return last_my_action



# Start by cooperating in the first round. In every later round, base your
# action on the payoff you received in the immediately preceding round. If that
# payoff was 3 or 5, repeat the exact action you chose in that preceding round.
# If that payoff was 0 or 1, switch to the opposite action.

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
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]) if False else None
      # Compute the payoff from the immediately preceding round using the last move pair.
      my_last_move = self.history[-1]
      opp_last_move = opponent.history[-1]
  
      if my_last_move == axl.Action.C and opp_last_move == axl.Action.C:
          last_payoff = 3
      elif my_last_move == axl.Action.C and opp_last_move == axl.Action.D:
          last_payoff = 0
      elif my_last_move == axl.Action.D and opp_last_move == axl.Action.C:
          last_payoff = 5
      else:
          last_payoff = 1
  
      if last_payoff in (3, 5):
          return my_last_move
      else:
          return axl.Action.D if my_last_move == axl.Action.C else axl.Action.C



# Start by defecting in the first round. Continue defecting unless your
# opponent's observed moves (which may be flipped by noise) are Cooperate in
# both of the two most recent rounds. Once this condition is met, cooperate; if
# at any later point an observed Defect appears in the last two rounds, switch
# back to defecting. Apply this rule starting from the third round, as the first
# two rounds cannot satisfy the two‑consecutive‑C requirement.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._cooperate_mode = False
          return axl.Action.D
  
      if len(opponent.history) >= 2:
          last_two = opponent.history[-2:]
          if last_two[0] == axl.Action.C and last_two[1] == axl.Action.C:
              self._cooperate_mode = True
          elif axl.Action.D in last_two:
              self._cooperate_mode = False
      else:
          self._cooperate_mode = False
  
      return axl.Action.C if self._cooperate_mode else axl.Action.D



# Cooperate in the first round. For every subsequent round, cooperate unless the
# opponent's observed action was D in each of the last two rounds—if so, defect.
# Otherwise, continue cooperating. (Your intended action is subject to a 10%
# flip, which may cause unintended defections occasionally.)

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the first round. In every round after the first,
# follow this rule:  - If your payoff in the previous round was 3 or 5 points,
# repeat the action you actually took in that round. - If your payoff was 0 or 1
# points, switch to the opposite action of what you actually took in that round.

class Neutral_12(LLM_Strategy):
  n = 12
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_action = axl.Action.C
          return axl.Action.C
  
      last_my_action = self.history[-1]
      last_my_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_my_score in (3, 5):
          self._last_action = last_my_action
      elif last_my_score in (0, 1):
          self._last_action = axl.Action.D if last_my_action == axl.Action.C else axl.Action.C
      else:
          self._last_action = last_my_action
  
      return self._last_action



# On the first round, defect (D). Thereafter, simply copy the action your
# opponent played in the previous round: if they cooperated (C), you cooperate;
# if they defected (D), you defect. No other conditions are used. This
# aggressive rule ensures you never offer unreciprocated cooperation, punishes
# exploitation immediately, and capitalizes on any opponent cooperation by
# repeatedly extracting the maximum 5 payoff whenever they return to C.

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



# Start by cooperating in the first round.    For every round after the first:
# - If your opponent’s action in the previous round was Cooperate, then
# Cooperate.   - If your opponent’s action in the previous round was Defect,
# then Cooperate with probability 1/3 and Defect with probability 2/3.    Use a
# random method (e.g., generate a number from 1 to 3 and Cooperate only if it is
# 1) to apply the probabilistic forgiveness. This approach maintains cooperation
# while breaking retaliatory cycles triggered by the 10% noise.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(1 / 3)



# Cooperate in the first round.   For every round after the first, follow these
# rules in order:  1. If your payoff in the previous round was either 3 or 5,
# then repeat whatever action you chose that round (the one you intended, before
# any chance of noise). 2. If your payoff in the previous round was either 0 or
# 1, then switch to the opposite action.

class Neutral_13(LLM_Strategy):
  n = 13
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_intended_action = axl.Action.C
          return axl.Action.C
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0] if False else None
      # Compute previous round payoff directly from the last interaction.
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
      last_payoff = my_last_score
  
      if last_payoff in (3, 5):
          return self._last_intended_action
      if last_payoff in (0, 1):
          self._last_intended_action = axl.Action.D if self._last_intended_action == axl.Action.C else axl.Action.C
          return self._last_intended_action
  
      return self._last_intended_action



# Start by defecting on the first round.  For each round after the first, decide
# as follows: - If your payoff in the previous round was 5 or 3, repeat the
# action you took in that previous round. - If your payoff in the previous round
# was 1 or 0, switch to the opposite action (defect if you cooperated, cooperate
# if you defected).  This rule uses your own payoff feedback to make choices,
# and the initial defection ensures an aggressive opening move.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1])[0:1])  # placeholder
      # Compute previous-round payoff directly from the last interaction
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
      last_payoff = my_last_score
  
      last_action = self.history[-1]
      if last_payoff in (5, 3):
          return last_action
      if last_payoff in (1, 0):
          return axl.Action.C if last_action == axl.Action.D else axl.Action.D
  
      return axl.Action.D



# Start by cooperating in the first round. For every subsequent round, follow
# this rule:   - If both you and your opponent took the same action in the
# previous round (both cooperated or both defected), then cooperate.   - If you
# and your opponent took different actions in the previous round, then defect.

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



# Start by cooperating in the first round. For every round thereafter, follow
# these rules in order:  1. If your payoff in the previous round was 3 or 5,
# then choose the same action (C or D) that you actually played in that round.
# 2. If your payoff in the previous round was 0 or 1, then choose the opposite
# action to the one you actually played in that round.  This ensures you repeat
# actions that yield high payoffs and switch away from actions that yield low
# payoffs, naturally responding to both intentional moves and noise.

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
  
      my_last_action = self.history[-1]
      my_last_payoff, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if my_last_payoff in (3, 5):
          return my_last_action
      if my_last_payoff in (0, 1):
          return axl.Action.C if my_last_action == axl.Action.D else axl.Action.D
  
      return my_last_action



# In the first round, always defect. From the second round onward, decide your
# next move solely on the payoff you received in the previous round:   - If your
# payoff was 5 or 3, repeat the action you just took (stay).   - If your payoff
# was 1 or 0, switch to the opposite action (shift).

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_payoff = self.score - sum(
          self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]
      )  # not used; kept for compatibility
  
      # Determine the payoff from the previous round directly from the last interaction.
      my_last_action = self.history[-1]
      opp_last_action = opponent.history[-1]
  
      if my_last_action == axl.Action.C and opp_last_action == axl.Action.C:
          payoff = 3
      elif my_last_action == axl.Action.C and opp_last_action == axl.Action.D:
          payoff = 0
      elif my_last_action == axl.Action.D and opp_last_action == axl.Action.C:
          payoff = 5
      else:
          payoff = 1
  
      if payoff in (5, 3):
          return my_last_action
      else:
          return axl.Action.C if my_last_action == axl.Action.D else axl.Action.D



# Start by cooperating in the first round. In each subsequent round, follow
# these rules in order:  1. If the opponent cooperated in the previous round,
# cooperate. 2. If the opponent defected in the previous round but cooperated in
# the round before that, cooperate. 3. Only if the opponent defected in both of
# the last two rounds, defect.

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
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Start by cooperating in the first round. For every subsequent round, follow
# this rule:  - If your payoff in the previous round was either 3 (both
# cooperated) or 5 (you defected, opponent cooperated), then choose the same
# action you selected in that previous round. - If your payoff was either 0 (you
# cooperated, opponent defected) or 1 (both defected), then switch to the
# opposite action from the one you selected in the previous round.  This
# approach uses only your own payoff history and is robust to the 10% action
# noise, as it will naturally correct errors and restore mutual cooperation.

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
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]) if False else None
      # Use the last round's realized payoff from the full histories.
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
      last_action = self.history[-1]
  
      if my_last_score in (3, 5):
          return last_action
      if my_last_score in (0, 1):
          return axl.Action.C if last_action == axl.Action.D else axl.Action.D
  
      return axl.Action.C



# Always defect. In every round, irrespective of the opponent's history of
# moves, choose Defect as your intended action. The 10% noise will occasionally
# flip this to Cooperate, but you do not alter your plan and never intentionally
# cooperate.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating (play C) in the first round.   Then, after each round,
# decide your next move based solely on your own payoff from the previous round:
# - If your payoff was 3 or 1, repeat the action you just took.   - If your
# payoff was 5 or 0, switch to the opposite action.    This rule automatically
# corrects for noise and encourages mutual cooperation without complex history
# tracking.

class Cooperative_16(LLM_Strategy):
  n = 16
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_action = axl.Action.C
          return axl.Action.C
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]) if False else None
      # Compute the payoff from the previous round using the last actions only.
      my_last_action = self.history[-1]
      opp_last_action = opponent.history[-1]
  
      if my_last_action == axl.Action.C and opp_last_action == axl.Action.C:
          last_payoff = 3
      elif my_last_action == axl.Action.C and opp_last_action == axl.Action.D:
          last_payoff = 0
      elif my_last_action == axl.Action.D and opp_last_action == axl.Action.C:
          last_payoff = 5
      else:
          last_payoff = 1
  
      if last_payoff in (3, 1):
          return my_last_action
      else:
          return axl.Action.D if my_last_action == axl.Action.C else axl.Action.C



# Start by cooperating in round 1. For every round after that, look at the
# actual outcome of the previous round (accounting for noise):  - If both you
# and your opponent ended up playing the same action—both cooperated or both
# defected—then cooperate in the current round. - If the two of you played
# different actions—one cooperated and the other defected—then defect in the
# current round.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == last_opp:
          return axl.Action.C
      return axl.Action.D



# Start by defecting in the first round.   After each round, follow exactly
# these rules in order:  1. If your payoff in the most recent round was 3 or 5,
# then in the next round repeat the action you just played.   2. If your payoff
# in the most recent round was 0 or 1, then in the next round switch to the
# opposite action (if you played C, play D; if you played D, play C).

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_my_action = self.history[-1]
      my_last_payoff, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if my_last_payoff in (3, 5):
          return last_my_action
      if my_last_payoff in (0, 1):
          return axl.Action.C if last_my_action == axl.Action.D else axl.Action.D
  
      return last_my_action



# Start by cooperating in the first round. After that, base your move each round
# solely on what your opponent did in the immediately preceding round:  - If
# your opponent cooperated last round, cooperate. - If your opponent defected
# last round, cooperate with probability 1/3 and defect with probability 2/3.
# (You can implement this by, for instance, rolling a three-sided die in your
# mind and cooperating only on a ‘1’.)  Apply this rule every round, ignoring
# any longer history.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(1 / 3)



# Start by cooperating in the first round. For every round after that, base your
# next action solely on your own payoff from the previous round: if you received
# 3 or 5 (the two highest possible payoffs), repeat whichever action you just
# played; if you received 0 or 1, switch to the opposite action. This rule lets
# you sustain mutual cooperation after errors while avoiding prolonged
# punishment cycles.

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
  
      last_payoff = self.score - sum(
          self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]
      )  # not used; placeholder to avoid relying on unavailable direct last-round score
  
      # Compute previous round payoff directly from the last interaction.
      my_last_action = self.history[-1]
      opp_last_action = opponent.history[-1]
  
      if my_last_action == axl.Action.C and opp_last_action == axl.Action.C:
          last_payoff = 3
      elif my_last_action == axl.Action.C and opp_last_action == axl.Action.D:
          last_payoff = 0
      elif my_last_action == axl.Action.D and opp_last_action == axl.Action.C:
          last_payoff = 5
      else:
          last_payoff = 1
  
      if last_payoff in (3, 5):
          return my_last_action
      else:
          return axl.Action.D if my_last_action == axl.Action.C else axl.Action.C



# Start by defecting.   After each round, check the payoff you received that
# round (after noise).   - If your payoff was 3 or 5 points, repeat the same
# intended action (C or D) that you chose that round.   - If your payoff was 0
# or 1 points, switch to the opposite intended action for the next round.

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.D
          return self._intended_action
  
      last_payoff = self.score - self.total_scores(self.history[:-1], opponent.history[:-1])[0]
  
      if last_payoff in (3, 5):
          return self._intended_action
      elif last_payoff in (0, 1):
          self._intended_action = axl.Action.C if self._intended_action == axl.Action.D else axl.Action.D
          return self._intended_action
  
      return self._intended_action



# Start by cooperating in the first round. For every subsequent round, determine
# your action as follows:  1. If your payoff in the previous round was 3 or 5,
# then in this round play the same action you actually played in the previous
# round. 2. If your payoff in the previous round was 0 or 1, then in this round
# play the opposite action to the one you actually played in the previous round.

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
  
      last_my_action = self.history[-1]
      last_my_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_my_score in (3, 5):
          return last_my_action
      if last_my_score in (0, 1):
          return axl.Action.C if last_my_action == axl.Action.D else axl.Action.D
  
      return last_my_action



# Start by cooperating on the first round. After each round, check the payoff
# you just earned. If your payoff was three or five, repeat your previous action
# in the next round. If your payoff was zero or one, switch to the opposite
# action. Always apply this rule based solely on your own most recent payoff.

class Neutral_18(LLM_Strategy):
  n = 18
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_action = axl.Action.C
          return axl.Action.C
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0] if False else None
      # Compute the payoff from the most recent round using the last actions.
      my_last_action = self.history[-1]
      opp_last_action = opponent.history[-1]
  
      if my_last_action == axl.Action.C and opp_last_action == axl.Action.C:
          last_payoff = 3
      elif my_last_action == axl.Action.C and opp_last_action == axl.Action.D:
          last_payoff = 0
      elif my_last_action == axl.Action.D and opp_last_action == axl.Action.C:
          last_payoff = 5
      else:
          last_payoff = 1
  
      if last_payoff in (3, 5):
          return my_last_action
      else:
          return axl.Action.D if my_last_action == axl.Action.C else axl.Action.C



# Start by defecting on the first two rounds. From round three onward, cooperate
# only if your opponent has cooperated in both of the previous two rounds;
# otherwise, defect.

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
      if len(self.history) == 1:
          return axl.Action.D
      if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Cooperate in the first two rounds.   For every round after the second, examine
# your opponent’s observed actions in the two most recent rounds. If both of
# those actions were Defect, then play Defect. Otherwise, play Cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
  
      return axl.Action.C



# Start by playing C. After each round, check your payoff from that round.   -
# If your payoff was 3 or 5, play the same move you just made.   - If your
# payoff was 0 or 1, switch to the opposite move.    Repeat this for all 1000
# rounds.

class Neutral_19(LLM_Strategy):
  n = 19
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_action = axl.Action.C
          return axl.Action.C
  
      last_payoff = self.score - getattr(self, "_prev_score", 0)
      self._prev_score = self.score
  
      if last_payoff in (3, 5):
          return self.history[-1]
      elif last_payoff in (0, 1):
          return axl.Action.D if self.history[-1] == axl.Action.C else axl.Action.C
      else:
          return self.history[-1]



# Start by defecting in round 1.   In every subsequent round:   - If your
# opponent’s last observed action was cooperate, then defect.   - If your
# opponent’s last observed action was defect, then cooperate with a 10%
# probability and defect with a 90% probability.   This keeps you defecting
# against cooperation to maximise exploitation, while occasionally probing after
# mutual defection to break low-payoff deadlocks and potentially lure the
# opponent into cooperating again.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_opponent_action = opponent.history[-1]
  
      if last_opponent_action == axl.Action.C:
          return axl.Action.D
  
      return self._random.random_choice(0.1)



# Start by cooperating in the first round. Then, for every round after that:  -
# If your payoff in the previous round was 3 or 5, repeat the same action you
# chose in that previous round. - If your payoff in the previous round was 0 or
# 1, switch to the opposite action.

class Cooperative_20(LLM_Strategy):
  n = 20
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_action = axl.Action.C
          return axl.Action.C
  
      last_payoff = self.score - sum(
          self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]
      )
  
      if last_payoff in (3, 5):
          return self.history[-1]
      if last_payoff in (0, 1):
          return axl.Action.C if self.history[-1] == axl.Action.D else axl.Action.D
  
      return self.history[-1]



# In the first round, cooperate. Thereafter, adopt the following rule: if your
# payoff in the previous round was 3 or 5, repeat your previous action; if your
# payoff was 0 or 1, switch to the opposite action.

class Neutral_20(LLM_Strategy):
  n = 20
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_action = axl.Action.C
          return axl.Action.C
  
      last_score = self.score - (self.total_scores(self.history[-1:], opponent.history[-1:])[0] if self.history else 0)
  
      if last_score in (3, 5):
          return self.history[-1]
      if last_score in (0, 1):
          return axl.Action.C if self.history[-1] == axl.Action.D else axl.Action.D
  
      return self.history[-1]



# **Strategy: Always Defect**  In every round, without exception, choose the
# action *Defect*. Do not consider the opponent's history or any other
# condition. Your intended move is always *Defect*, though due to noise it will
# actually be *Defect* 90% of the time and *Cooperate* 10% of the time.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round. In every subsequent round, base your
# next move solely on the payoff you received in the previous round:  - If your
# previous round’s payoff was 3 or 5, repeat the exact action you played in that
# round. - If your previous round’s payoff was 0 or 1, switch to the opposite
# action.  This means you continue doing what brought a high payoff and change
# what brought a low payoff, creating a simple, cooperative, and noise-tolerant
# approach.

class Cooperative_21(LLM_Strategy):
  n = 21
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_action = axl.Action.C
          return axl.Action.C
  
      last_payoff, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_payoff in (3, 5):
          return self.history[-1]
      elif last_payoff in (0, 1):
          return axl.Action.D if self.history[-1] == axl.Action.C else axl.Action.C
      else:
          return self.history[-1]



# In the first round, cooperate.   In every subsequent round, based on the
# action you intended last round and the payoff you actually received:  - If you
# received a payoff of 3 or 5, repeat your intended action from last round. - If
# you received a payoff of 0 or 1, switch to the opposite action.

class Neutral_21(LLM_Strategy):
  n = 21
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      last_payoff = self.score - sum(
          self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]
      ) if len(self.history) > 1 else self.score
  
      # Determine intended action from last round
      intended = self._intended_action
  
      # Update intended action based on received payoff
      if last_payoff in (3, 5):
          next_action = intended
      elif last_payoff in (0, 1):
          next_action = axl.Action.D if intended == axl.Action.C else axl.Action.C
      else:
          next_action = intended
  
      self._intended_action = next_action
      return next_action



# In every round, choose Defect. There are no conditions under which you
# cooperate. Due to noise, your action will be flipped to Cooperate 10% of the
# time, but your intended move is always Defect.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Cooperate in the first two rounds. Then, for every round after the second: if
# the opponent’s observed move was Defect in both of the previous two rounds,
# play Defect; otherwise, play Cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# In the first round, choose Cooperate.   For every later round, follow these
# rules in order:  1. If your score in the previous round was 3 or 5, repeat the
# action you chose in the previous round.   2. If your score in the previous
# round was 0 or 1, choose the opposite action from the one you chose in the
# previous round.

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
  
      last_my_action = self.history[-1]
      last_my_score = self.score - self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_my_score in (3, 5):
          return last_my_action
      if last_my_score in (0, 1):
          return axl.Action.C if last_my_action == axl.Action.D else axl.Action.D
  
      return last_my_action



# Start by defecting. In each subsequent round, after observing your payoff from
# the previous round, follow this rule: if your payoff was 5 or 3, repeat your
# previous action; if your payoff was 1 or 0, switch to the opposite action.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]) if False else None
      # Compute previous-round payoff directly from the last interaction.
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
      last_payoff = my_last_score
  
      if last_payoff in (5, 3):
          return self.history[-1]
      if last_payoff in (1, 0):
          return self.history[-1].flip()
  
      return self.history[-1]



# In the first round, Cooperate.  In every later round: if, in the previous
# round, you and your opponent chose the same action (both Cooperated or both
# Defected), then Cooperate. If you and your opponent chose different actions
# (one Cooperated and the other Defected), then Defect.

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# In the first round, cooperate.   In every subsequent round:   - If your
# opponent’s observed action in the previous round was Cooperate, then
# cooperate.   - If your opponent’s observed action in the previous round was
# Defect, then cooperate with probability 1/3 and defect with probability 2/3.

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
  
      last_opponent_action = opponent.history[-1]
  
      if last_opponent_action == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(1 / 3)



# Start by defecting in the first round. In every subsequent round, simply copy
# your opponent’s preceding move: cooperate if they cooperated, defect if they
# defected.

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
      return opponent.history[-1]



# Start by cooperating in the first round.   For every round after the first:
# - If the opponent played D in each of the last two rounds, play D.   -
# Otherwise, play C.

class Cooperative_24(LLM_Strategy):
  n = 24
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating. In each subsequent round, cooperate if either of the
# opponent’s last two moves was cooperate; defect only if the opponent’s last
# two moves were both defect. If fewer than two previous moves exist, treat
# missing moves as cooperate.

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
  
      last_two = opponent.history[-2:]
      if len(last_two) < 2:
          last_two = [axl.Action.C] * (2 - len(last_two)) + list(last_two)
  
      return axl.Action.C if axl.Action.C in last_two else axl.Action.D



# Always choose D (defect) on every round, regardless of the opponent's previous
# moves or the game history. Do not cooperate under any circumstances.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# In the first two rounds, always cooperate.  For every round after the second,
# look at the opponent’s just‑observed previous two actions. If both of those
# actions were Defect, play Defect. Otherwise, play Cooperate.

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
  
      if len(self.history) < 2:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# Start by cooperating in the first round. For every round after that, base your
# decision on the outcome of the previous round. In that previous round, if you
# received a payoff of 3 (both actually played C) or 5 (you actually played D
# and the opponent actually played C), then repeat the action you actually
# played in that round. If your payoff was 0 (you actually played C and the
# opponent actually played D) or 1 (both actually played D), switch to the
# opposite action from what you actually played. Because actions are noisy, you
# can infer your actual previous action from the payoff you received and the
# opponent's observed action. This rule keeps your intended action aligned with
# what worked, while naturally forgiving occasional noise or mutual defection.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      # Infer the actual previous outcome from the observed actions and payoff.
      # Payoffs:
      # CC -> 3, CD -> 0, DC -> 5, DD -> 1
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          payoff = 3
      elif last_self == axl.Action.C and last_opp == axl.Action.D:
          payoff = 0
      elif last_self == axl.Action.D and last_opp == axl.Action.C:
          payoff = 5
      else:
          payoff = 1
  
      if payoff in (3, 5):
          return last_self
      else:
          return axl.Action.D if last_self == axl.Action.C else axl.Action.C