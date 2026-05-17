import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# Here is the rewritten strategy, refined for clarity while preserving the core
# approach:  In every single round, from round 1 to round 1000, unconditionally
# choose the action Defect. Do this no matter what your opponent has done in any
# previous round. Do not cooperate under any circumstances. The only thing that
# can cause a Cooperate outcome is the 10% noise flipping your Defect to
# Cooperate, which is outside your control. Your intended action must remain
# Defect at all times.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# 1. In the first round, choose Cooperate. 2. In every later round, first check
# whether in the immediately previous round you intended to Cooperate but your
# actual action was Defect. You can identify this if you intended Cooperate and
# either (a) the opponent played Cooperate and you received 5, or (b) the
# opponent played Defect and you received 1. If this occurred, choose Cooperate
# in the current round. 3. If the above condition does not apply, examine the
# opponent’s actions in the last three rounds. Treat any round before the first
# as if the opponent Cooperated. If the opponent Defected in two or more of
# those three rounds, choose Defect. Otherwise, choose Cooperate.

class Cooperative_1(LLM_Strategy):
  n = 1
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_cooperate_last_round = True
          return axl.Action.C
  
      if getattr(self, "_intended_cooperate_last_round", False):
          if len(self.history) >= 1 and len(opponent.history) >= 1:
              last_self = self.history[-1]
              last_opp = opponent.history[-1]
              last_score = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
              if last_self == axl.Action.D and last_score in (5, 1):
                  self._intended_cooperate_last_round = True
                  return axl.Action.C
  
      last_three = list(opponent.history[-3:])
      if len(last_three) < 3:
          last_three = [axl.Action.C] * (3 - len(last_three)) + last_three
  
      if last_three.count(axl.Action.D) >= 2:
          action = axl.Action.D
      else:
          action = axl.Action.C
  
      self._intended_cooperate_last_round = (action == axl.Action.C)
      return action



# In the first round, intend to cooperate.   In every later round, use the
# payoff you just received together with your intended action from that round to
# determine both whether that round was a win or a loss for you, and which
# action you actually executed (which may differ from your intention due to
# noise).    - A win is any payoff of 3 or 5. A loss is any payoff of 0 or 1.
# - Identify your actual action:     * If you intended to cooperate and your
# payoff was 3 or 0, your actual action was cooperation.     * If you intended
# to cooperate and your payoff was 5 or 1, your actual action was defection.
# * If you intended to defect and your payoff was 5 or 1, your actual action was
# defection.     * If you intended to defect and your payoff was 3 or 0, your
# actual action was cooperation.    For your next move:   - If the past round
# was a win, intend to repeat the actual action you just took.   - If the past
# round was a loss, intend to switch to the opposite of the actual action you
# just took.

class Neutral_1(LLM_Strategy):
  n = 1
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.C
          return self._intended_action
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0]
      last_intended = self._intended_action
  
      if last_intended == axl.Action.C:
          if last_payoff in (3, 0):
              actual_action = axl.Action.C
          else:
              actual_action = axl.Action.D
      else:
          if last_payoff in (5, 1):
              actual_action = axl.Action.D
          else:
              actual_action = axl.Action.C
  
      if last_payoff in (3, 5):
          self._intended_action = actual_action
      else:
          self._intended_action = axl.Action.D if actual_action == axl.Action.C else axl.Action.C
  
      return self._intended_action



# Always intend to play Defect.

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
          self._last_opp_defections = 0
          self._last_self_defections = 0
          self._last_opp_cooperations = 0
          self._last_self_cooperations = 0
          return axl.Action.D
  
      # Always intend to defect, but react to apparent exploitation or instability.
      # Since noise can flip actions, use short-window changes to detect unusual
      # opponent behavior and briefly punish by defecting.
      recent = 8
      opp_recent = opponent.history[-recent:]
      self_recent = self.history[-recent:]
  
      opp_defections = opp_recent.count(axl.Action.D)
      opp_cooperations = opp_recent.count(axl.Action.C)
      self_defections = self_recent.count(axl.Action.D)
      self_cooperations = self_recent.count(axl.Action.C)
  
      # If the opponent appears to cooperate unusually often, keep defecting.
      # If they appear to defect a lot, still defect.
      # This strategy is fundamentally always-D.
      if opp_cooperations > opp_defections:
          return axl.Action.D
  
      return axl.Action.D



# Start by cooperating. After each round, determine whether your opponent
# cooperated or defected using only your score:   - If you scored 3 or 5, your
# opponent cooperated.   - If you scored 0 or 1, your opponent defected.
# Remember the opponent’s actions from the last two rounds. For the next round:
# - If the opponent defected in both of the last two rounds, defect.   -
# Otherwise, cooperate.

class Cooperative_2(LLM_Strategy):
  n = 2
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._opponent_last_two_coop = []
          return axl.Action.C
  
      if len(self.history) >= 1:
          last_my_score = self.score - self.total_scores(self.history[-1:], opponent.history[-1:])[0]
      else:
          last_my_score = None
  
      if last_my_score in (3, 5):
          opponent_played = axl.Action.C
      elif last_my_score in (0, 1):
          opponent_played = axl.Action.D
      else:
          opponent_played = opponent.history[-1]
  
      self._opponent_last_two_coop.append(opponent_played == axl.Action.C)
      if len(self._opponent_last_two_coop) > 2:
          self._opponent_last_two_coop = self._opponent_last_two_coop[-2:]
  
      if len(self._opponent_last_two_coop) == 2 and not self._opponent_last_two_coop[0] and not self._opponent_last_two_coop[1]:
          return axl.Action.D
      return axl.Action.C



# In the first round, intend to play C.  For every round after that:  1. If your
# payoff last round was 3 (Temptation avoided or mutual cooperation) or 5 (you
# defected while the opponent cooperated), then in the current round intend to
# repeat the action that was actually executed by you last round (after noise).
# 2. If your payoff last round was 0 (you cooperated while the opponent
# defected) or 1 (mutual defection), then in the current round intend to switch
# from the action that was actually executed by you last round (after noise) to
# the opposite action.

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
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]) if False else None
      # Compute last-round payoff directly from the most recent interaction.
      my_last, opp_last = self.total_scores(self.history[-1:], opponent.history[-1:])
      last_payoff = my_last
  
      last_action = self.history[-1]
  
      if last_payoff in (3, 5):
          return last_action
      elif last_payoff in (0, 1):
          return axl.Action.D if last_action == axl.Action.C else axl.Action.C
  
      return axl.Action.C



# **Strategy: "Aggressive Tit-for-Tat with Noise Buffer"**  1. **Defect on the
# first round.** Start by assuming the worst and aiming for the high payoff
# immediately.  2. **If your opponent cooperated in the previous round,
# defect.** Exploit their cooperation to gain the maximum possible payoff of 5
# (subject to noise).  3. **If your opponent defected in the previous round,
# defect.** Do not let them gain an advantage; secure at least 1 rather than
# risking 0.  4. **The only exception: forgive after three consecutive mutual
# defections.** If both you and your opponent have defected for three rounds in
# a row, play cooperate once. This is a probe to see if the opponent can be
# lured back into cooperating. The counter resets whenever a round is not a
# mutual defection.  5. **If the opponent cooperates in response to your
# forgiveness probe, continue cooperating for exactly one more round.** This
# rewards their shift and encourages them to maintain cooperation. Then, on the
# following round, defect to exploit them.  6. **If the opponent defects in
# response to your forgiveness probe, immediately return to defecting on the
# next round.** Do not extend trust that is not reciprocated.  7. **Ignore noise
# when judging the opponent.** Always treat the observed action as intentional.
# Do not attempt to detect or compensate for noise, as doing so would soften
# your aggression.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._probe_active = False
          self._probe_followup = False
          self._probe_followup_done = False
          self._mutual_defection_streak = 0
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          self._mutual_defection_streak += 1
      else:
          self._mutual_defection_streak = 0
  
      if self._probe_followup:
          self._probe_followup = False
          self._probe_followup_done = True
          if last_opp == axl.Action.C:
              return axl.Action.C
          return axl.Action.D
  
      if self._probe_followup_done:
          self._probe_followup_done = False
          return axl.Action.D
  
      if self._mutual_defection_streak >= 3:
          self._mutual_defection_streak = 0
          self._probe_active = True
          self._probe_followup = True
          return axl.Action.C
  
      return axl.Action.D



# Here is the strategy, restated with the same logic but in fresh wording:
# Begin by cooperating in each of the first 10 rounds, regardless of what you
# observe. From round 11 onward, calculate the percentage of rounds in which you
# observed your opponent cooperate, using all rounds played so far (including
# those first 10). If that percentage is 75% or higher, cooperate; otherwise,
# defect. Always base your count on the actions you actually see, since noise
# may have altered the intended moves.

class Cooperative_3(LLM_Strategy):
  n = 3
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._observed_cooperations = 0
          self._observed_rounds = 0
          return axl.Action.C
  
      self._observed_rounds += 1
      if opponent.history[-1] == axl.Action.C:
          self._observed_cooperations += 1
  
      if self._observed_rounds <= 10:
          return axl.Action.C
  
      cooperation_rate = self._observed_cooperations / self._observed_rounds
      return axl.Action.C if cooperation_rate >= 0.75 else axl.Action.D



# Cooperate in the first round.  For every subsequent round:  - Look at the
# actual (possibly flipped) actions from the previous round: what you actually
# did and what your opponent actually did. - If those two actions were the same
# (both C or both D), then cooperate. - If those two actions were different (you
# C and opponent D, or you D and opponent C), then defect.

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
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == opp_last:
          return axl.Action.C
      return axl.Action.D



# Defect on the first round. For every round after the first, play the action
# your opponent played in the immediately preceding round.

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
      return opponent.history[-1]



# Start by cooperating in the first round. In the second round, cooperate again
# no matter what you observed your opponent do. From the third round onward,
# cooperate unless in both of the previous two rounds you actually observed your
# opponent's action as defect. If you observed defection in each of those two
# rounds, then defect; otherwise, always cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Begin by cooperating in round 1. In every later round, recall both the action
# you chose (intended to play) in the previous round and the payoff you actually
# received in that same round. Then decide as follows:  - If your previous
# payoff was 3 or 5, choose the same intended action you used in that previous
# round. - If your previous payoff was 0 or 1, choose the opposite of the
# intended action you used in that previous round.  Because your own executed
# action is not directly observable when noise is present, this rule uses only
# the information you actually have: your intended move and the payoff you
# observed.

class Neutral_4(LLM_Strategy):
  n = 4
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_last = axl.Action.C
          return axl.Action.C
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0] if False else None
      # Compute the payoff from the previous round using the last interaction only.
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
      last_payoff = my_last_score
  
      if last_payoff in (3, 5):
          return self._intended_last
      else:
          return axl.Action.D if self._intended_last == axl.Action.C else axl.Action.C



# Defect on the first round.   For every round after the first, look at the
# opponent’s actual actions (after noise) in the two most recent rounds.   If
# both of those actions were defections, then defect.   Otherwise, cooperate.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Start by selecting Cooperate in the first round. After each round, check your
# own payoff from that round—the actual points you scored after any action
# flips. Then decide your next intended action as follows:  - If you received 3
# or 5 points, choose the same action you intended to play in the round that
# just ended. - If you received 0 or 1 points, choose the opposite action
# (switch from Cooperate to Defect, or Defect to Cooperate).  Apply this rule in
# every subsequent round.

class Cooperative_5(LLM_Strategy):
  n = 5
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.C
          return self._intended_action
  
      last_self_action = self.history[-1]
      last_opponent_action = opponent.history[-1]
      last_score, _ = self.total_scores([last_self_action], [last_opponent_action])
  
      if last_score in (3, 5):
          self._intended_action = last_self_action
      elif last_score in (0, 1):
          self._intended_action = axl.Action.D if last_self_action == axl.Action.C else axl.Action.C
  
      return self._intended_action



# Start by cooperating on the first move. For every subsequent round, look only
# at the outcome of the immediately previous round:  - If you and your opponent
# just played the same action (both cooperated or both defected), cooperate in
# the next round. - If you and your opponent just played different actions (one
# cooperated and the other defected), defect in the next round.  Stay with this
# rule for all 1000 rounds, regardless of any other history.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == last_opp:
          return axl.Action.C
      return axl.Action.D



# - The strategy is logically sound and internally consistent, with no
# ambiguities or contradictions in its description. - It clearly specifies
# actions for the first two rounds and a well-defined condition for subsequent
# rounds based solely on observable outcomes. - No logical mistakes are present.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_expected_opponent_action = axl.Action.C
          return axl.Action.C
  
      if len(self.history) == 1:
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C



# Start by cooperating in the first round.  For every round after the first: -
# If your opponent’s action in the previous round was C, cooperate. - If your
# opponent’s action in the previous round was D, then cooperate with a 10%
# chance and defect otherwise.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)



# In the first round, intend to play C.   For every round after that, use your
# intended action from the previous round and the payoff you just received to
# work out the actual action that was executed on your behalf.   - If your
# payoff was 3 or 5, consider the last round a “win”; for the next round, intend
# to repeat the actual action you just played.   - If your payoff was 0 or 1,
# consider the last round a “loss”; for the next round, intend to switch to the
# opposite of the actual action you just played.

class Neutral_6(LLM_Strategy):
  n = 6
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.C
          return self._intended_action
  
      last_intended = getattr(self, "_intended_action", axl.Action.C)
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0] if False else None
  
      # Compute the actual action that must have been executed last round.
      # Since the payoff matrix is deterministic given actual actions, infer it
      # from the intended action and the observed payoff.
      my_last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0] if False else None
  
      # Use the last round's observed outcome to infer the actual action played.
      my_last_move = self.history[-1]
      opp_last_move = opponent.history[-1]
      actual_last_action = my_last_move
  
      # Determine whether the last round was a win or loss based on payoff.
      # Payoffs: 3 or 5 => win; 0 or 1 => loss.
      last_round_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_round_payoff in (3, 5):
          self._intended_action = actual_last_action
      else:
          self._intended_action = axl.Action.C if actual_last_action == axl.Action.D else axl.Action.D
  
      return self._intended_action



# Defect on round 1 and round 2 unconditionally. From round 3 through round
# 1000, observe the opponent's actual moves (post-noise) in the two most recent
# rounds. If both were C, cooperate; otherwise, defect.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number <= 2:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# - In round 1, cooperate.   - In round 2, cooperate regardless of the
# opponent’s observed action in round 1.   - In every round from 3 onward, look
# at the opponent’s observed actions in the two most recent rounds. If both were
# defect, then defect. If at least one was cooperate, cooperate.

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
  
      if len(opponent.history) < 2:
          return axl.Action.C
  
      last_two = opponent.history[-2:]
      if last_two.count(axl.Action.D) == 2:
          return axl.Action.D
      return axl.Action.C



# On the first round, cooperate.  For every round after the first, determine
# your move as follows:  - If your payoff last round was 3 or 5, repeat the
# action you actually performed last round. - If your payoff last round was 0 or
# 1, switch to the opposite action.  Because the payoffs uniquely indicate your
# actual action (a payoff of 3 means you played C, 5 means you played D, 0 means
# you played C, and 1 means you played D), you can infer your previous action
# directly from your payoff.

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
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]) if False else None
      # Compute last-round payoff directly from the last interaction.
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
      last_payoff = my_last_score
  
      if last_payoff in (3, 5):
          return self.history[-1]
      else:
          return axl.Action.D if self.history[-1] == axl.Action.C else axl.Action.C



# In the first round, choose Defect.    For every round after the first, check
# the payoff you received in the immediately previous round.   - If that payoff
# was 3 or 5, repeat the move you actually made in that previous round (the one
# that occurred after noise).   - If that payoff was 0 or 1, switch to the
# opposite move.

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
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0] if False else None
      # Compute the payoff from the immediately previous round using the last action pair.
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
          return axl.Action.C if my_last_action == axl.Action.D else axl.Action.D



# Start by cooperating in the first round.  From the second round onward, use
# the opponent’s actual moves (after noise) from the most recent three rounds as
# a rolling memory. If fewer than three rounds have been played, use all
# available past rounds.  Count the number of times the opponent defected in
# that memory window.   - If the count is **two or more**, play Defect.   -
# Otherwise, play Cooperate.

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
  
      recent_opponent_moves = opponent.history[-3:]
      defect_count = recent_opponent_moves.count(axl.Action.D)
  
      if defect_count >= 2:
          return axl.Action.D
      return axl.Action.C



# Start by cooperating in the first round.  For every round after the first: -
# Look at the actual actions that occurred in the previous round (not what was
# intended, but what happened after any possible flips). - If both players ended
# up playing the same action (both C or both D), cooperate. - If the players
# played different actions (one C and one D), defect.

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# Defect in every round except when the opponent has cooperated in both of the
# two most recent rounds. In that specific case, cooperate.  To begin, always
# defect in rounds 1 and 2 because there is no observed history of two
# consecutive cooperations. After round 2, look at the opponent’s actual moves
# (taking into account the noise) from the last two rounds: if both were C,
# cooperate; if either was D, defect. A single observed defection immediately
# causes you to defect for at least the next two rounds, until two consecutive
# cooperations are again observed. This rule applies throughout all 1000 rounds
# without exception.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._force_defect_until = 2
          return axl.Action.D
  
      if not hasattr(self, "_force_defect_until"):
          self._force_defect_until = 2
  
      if len(opponent.history) < 2:
          return axl.Action.D
  
      if len(opponent.history) >= 2:
          last_two = opponent.history[-2:]
          if last_two.count(axl.Action.C) == 2:
              return axl.Action.C
  
      return axl.Action.D



# In the first round, choose Cooperate.   For every subsequent round, observe
# the action your opponent took in the previous round.   - If you saw Cooperate,
# then Cooperate.   - If you saw Defect, then Cooperate with probability 1/3;
# otherwise, Defect.

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
  
      last_opponent_action = opponent.history[-1]
      if last_opponent_action == axl.Action.C:
          return axl.Action.C
      return self._random.random_choice(1 / 3)



# Start by cooperating in the first round.    For every subsequent round,
# determine your action as follows:   - If your payoff in the previous round was
# 3 or 5, repeat your previous action.   - If your payoff in the previous round
# was 0 or 1, switch to the opposite action.    Your payoff is based on the
# actual (possibly flipped) actions each round.

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
  
      if len(self.history) == 0:
          self._last_action = axl.Action.C
          return axl.Action.C
  
      last_payoff = self.score - sum(
          self.total_scores(self.history[:-1], opponent.history[:-1])[0]
      )
  
      if last_payoff in (3, 5):
          action = self.history[-1]
      elif last_payoff in (0, 1):
          action = axl.Action.D if self.history[-1] == axl.Action.C else axl.Action.C
      else:
          action = self.history[-1]
  
      self._last_action = action
      return action



# In the first round, choose Defect.  For every round after that, do the
# following:  1. Recall your intended move from the previous round — that is,
# the action (Cooperate or Defect) you selected before noise could flip it. 2.
# Look at the payoff you actually received in the previous round. 3. If your
# received payoff was exactly 5, then for the current round select the same
# intended move you used last round. 4. If your received payoff was anything
# other than 5 (so 3, 1, or 0), then for the current round select the opposite
# intended move: if you intended Cooperate last round, choose Defect this round;
# if you intended Defect last round, choose Cooperate this round.

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_move = axl.Action.D
          return self._intended_move
  
      last_payoff = self.score - self.total_scores(self.history[:-1], opponent.history[:-1])[0]
  
      if last_payoff == 5:
          current_intended = self._intended_move
      else:
          current_intended = axl.Action.C if self._intended_move == axl.Action.D else axl.Action.D
  
      self._intended_move = current_intended
      return current_intended



# On the first round, cooperate.   For every round after the first, look at the
# action your opponent chose in the immediately previous round:   - If that
# action was C, cooperate.   - If that action was D, cooperate with a 10%
# probability; otherwise, defect.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)



# Here is the rewritten strategy:  In round 1, always cooperate.   For every
# round after round 1:   - Look only at the actual (post-noise) moves from the
# immediately previous round.   - If those two moves were the same (both C or
# both D), cooperate.   - If those two moves were different (one C, one D),
# defect.  The strategy treats both players symmetrically and makes no attempt
# to model or forgive intentional defection; it only conditions on the observed
# outcome.

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



# Here's the strategy, unchanged in logic but clearly restated:  In the first
# two rounds, defect. From round three onward, cooperate only if the opponent’s
# observed moves in the immediate two preceding rounds were both Cooperate;
# otherwise, defect.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(self.history) < 2:
          return axl.Action.D
  
      if self.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      return axl.Action.D



# Here is the revised strategy:  Begin by cooperating in round 1 and round 2.
# From round 3 onward, cooperate unless the opponent’s observed moves in the two
# most recent rounds were both Defect; if they were both Defect, then defect.

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
  
      if len(self.history) < 2:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# In the first round, cooperate. In each subsequent round, cooperate if in the
# previous round your action and your opponent’s action matched (both cooperated
# or both defected). Otherwise, defect.

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# Always defect. Do not cooperate under any circumstances, regardless of your
# opponent's previous actions.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by cooperating in the first round, regardless of noise. For every round
# after the first, base your decision solely on the previous round's actual,
# noise-affected outcome:  - If both players ended up playing the same move
# (both C or both D), then cooperate in the current round. - If the players
# ended up playing different moves (one C and one D), then defect in the current
# round.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == last_opp:
          return axl.Action.C
      return axl.Action.D



# In the first round, cooperate.  For every round after the first, apply these
# rules in order:  1. If your own action in the previous round was defection,
# cooperate. 2. Otherwise, if your opponent’s action in the previous round was
# cooperation, cooperate. 3. Otherwise, defect.

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
  
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# On the first two rounds, play Defect. For all later rounds, from round 3
# through round 1000, play Cooperate only if you observed your opponent play
# Cooperate in both of the two immediately preceding rounds. In every other
# case, play Defect.

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
  
      if len(self.history) < 2:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Start by cooperating in the first round.  In every round after that, look at
# the action you actually took in the previous round (the one that occurred
# after any noise flip) and the payoff you received:  - If your payoff was 3 or
# 5, repeat that same action in the current round. - If your payoff was 0 or 1,
# switch to the opposite action in the current round.

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
  
      last_action = self.history[-1]
      last_score = self.score - (self.total_scores(self.history[-1:], opponent.history[-1:])[0] if len(self.history) > 0 else 0)
  
      if last_score in (3, 5):
          return last_action
      if last_score in (0, 1):
          return axl.Action.D if last_action == axl.Action.C else axl.Action.C
  
      return last_action



# Start by cooperating in the first round. In each later round:   1. If your
# opponent’s previous action was cooperate, cooperate.   2. If your opponent’s
# previous action was defect, cooperate with a 20% probability and defect
# otherwise.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.2)



# In every round, choose Defect. This action applies unconditionally, regardless
# of your opponent’s previous moves or any other factor.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Start by playing C in rounds 1 and 2. For every round from round 3 onward,
# examine the opponent’s actual moves (after noise) in the two immediately
# preceding rounds. If both of those moves were D, play D. Otherwise, play C.

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
  
      if len(self.history) < 2:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# Start by cooperating in the first round. For every round after the first, base
# your decision on the actual actions (after noise) that you and your opponent
# took in the previous round, applying these rules in the order given:  1. If
# you both cooperated, cooperate.   2. If you both defected, cooperate.   3. If
# you cooperated and your opponent defected, defect.   4. If you defected and
# your opponent cooperated, defect.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.C



# Defect on round 1.   From round 2 onward, cooperate if and only if the
# opponent's observed move was cooperate in both of the two most recent rounds;
# otherwise defect.   For the first two rounds, treat any unobserved opponent
# move as defection.

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
  
      if len(opponent.history) < 2:
          return axl.Action.D
  
      return axl.Action.C if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C else axl.Action.D



# Cooperate on round 1.   Cooperate on round 2 no matter what the opponent did
# in round 1.   From round 3 onward, look at the opponent’s observed actions in
# the last three rounds. If all three of those actions were defections, then
# defect. Otherwise, cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          return axl.Action.D
  
      return axl.Action.C



# Cooperate on the first round.   In every round after the first, look at your
# own payoff from the previous round. Deduce which action you actually executed:
# a payoff of 3 or 0 means you executed C; a payoff of 5 or 1 means you executed
# D.   If your payoff was 3 or 5, repeat that executed action in the next round.
# If your payoff was 0 or 1, play the opposite of that executed action in the
# next round.

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
      # Determine our previous-round payoff from the last pair of actions.
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
  
      if payoff in (3, 5):
          return my_last_action
      else:
          return axl.Action.D if my_last_action == axl.Action.C else axl.Action.C



# Start by defecting on the first round. For every subsequent round, set your
# intended action according to these rules, applied in order:  1. If the
# opponent’s actual previous action (after noise) was cooperate, then intend to
# defect. 2. If the opponent’s actual previous action was defect, then intend to
# cooperate with a probability of 20%; otherwise intend to defect.  Because
# actions are noisy, your intended action will be flipped 10% of the time, but
# these rules determine your intentions regardless.

class Aggressive_16(LLM_Strategy):
  n = 16
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
      else:
          return self._random.random_choice(0.2)



# Start by cooperating in the first round. For each subsequent round, look at
# the actual action you observed your opponent take in the previous round (after
# any noise was applied) and the action you actually played that round (also
# after noise). Then:  - If the two observed actions matched (both Cooperate or
# both Defect), cooperate in the current round. - If the two observed actions
# differed (one Cooperate, one Defect), defect in the current round.  Continue
# this for all 1000 rounds.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == last_opp:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in round 1.   For every round after the first, use only
# the payoff you received in the previous round to guide your next intended
# action:  - If your previous payoff was 5, you know your actual action was D
# (the noise-free outcome must have been you playing D against your opponent
# playing C). For the next round, intend D. - If your previous payoff was 3, you
# know your actual action was C (both actually played C). For the next round,
# intend C. - If your previous payoff was 1, you know your actual action was D
# (both actually played D). For the next round, intend C (the opposite of the
# actual D you now know you played). - If your previous payoff was 0, you know
# your actual action was C (you played C against your opponent's D). For the
# next round, intend D (the opposite of the actual C you now know you played).

class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]) if False else None
      # Use only the previous round's payoff, inferred from the score difference.
      prev_my_score = self.score - self.total_scores(self.history[:-1], opponent.history[:-1])[0]
      last_payoff = prev_my_score
  
      if last_payoff == 5:
          self._intended_action = axl.Action.D
      elif last_payoff == 3:
          self._intended_action = axl.Action.C
      elif last_payoff == 1:
          self._intended_action = axl.Action.C
      elif last_payoff == 0:
          self._intended_action = axl.Action.D
      else:
          self._intended_action = axl.Action.C
  
      return self._intended_action



# In the first round, defect.   In the second round, cooperate only if the
# opponent’s observed action in round 1 was cooperate; otherwise, defect.   For
# every round after the second, cooperate only if the opponent’s observed action
# was cooperate in both of the previous two rounds; otherwise, defect.

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
  
      if len(opponent.history) == 1:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      return axl.Action.C if (
          opponent.history[-1] == axl.Action.C
          and opponent.history[-2] == axl.Action.C
      ) else axl.Action.D



# In the first round, cooperate.  In the second round, look only at the
# opponent’s action from the first round.   - If the opponent cooperated,
# cooperate.   - If the opponent defected, defect.  In every round from the
# third onward, look at the opponent’s actions from the previous two rounds.   -
# If at least one of those two actions was cooperation, cooperate.   - If both
# actions were defection, defect.

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
  
      if len(opponent.history) == 1:
          return opponent.history[-1]
  
      if opponent.history[-1] == axl.Action.C or opponent.history[-2] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in round 1. In round 2, cooperate if the opponent’s
# observed move in round 1 was cooperation; otherwise, cooperate with
# probability 1/2 and defect with probability 1/2.  From round 3 onward, use the
# opponent’s last two observed moves:  1. If both were cooperation, cooperate.
# 2. If both were defection, defect. 3. If the two moves differ (one cooperation
# and one defection), cooperate with probability 1/2 and defect with probability
# 1/2.

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
  
      if len(opponent.history) == 1:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else self._random.random_choice(0.5)
  
      last_two = opponent.history[-2:]
      if last_two[0] == axl.Action.C and last_two[1] == axl.Action.C:
          return axl.Action.C
      if last_two[0] == axl.Action.D and last_two[1] == axl.Action.D:
          return axl.Action.D
      return self._random.random_choice(0.5)



# In rounds 1 through 5, always play Defect.  From round 6 onward, look at the
# previous 5 rounds. If in all of those rounds your intended action was Defect
# and the opponent's observed action was Defect, then play Cooperate. Otherwise,
# play Defect.

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_history = []
      
      if len(self.history) < 5:
          self._intended_history.append(axl.Action.D)
          return axl.Action.D
  
      last_five_intended = self._intended_history[-5:]
      last_five_opponent = opponent.history[-5:]
  
      if all(a == axl.Action.D for a in last_five_intended) and all(a == axl.Action.D for a in last_five_opponent):
          action = axl.Action.C
      else:
          action = axl.Action.D
  
      self._intended_history.append(action)
      return action



# Cooperate in the first round.  In every round after the first, look only at
# the payoff you received in the previous round:  - If that payoff was 3 or 5,
# then in this round play the same action you just played. - If that payoff was
# 0 or 1, then in this round switch to the opposite action.  These two rules,
# checked in exactly this order, cover all possible outcomes. Because your
# received payoff already reflects any noise that may have flipped your action
# or your opponent’s, no extra handling of randomness is needed.

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
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0] if False else None
      # Compute previous-round payoff directly from the last interaction
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
      last_payoff = my_last_score
  
      if last_payoff in (3, 5):
          return self.history[-1]
      if last_payoff in (0, 1):
          return self.history[-1].flip()
  
      return self.history[-1]



# In the first round, cooperate.  For every round after the first, look only at
# your own payoff from the immediately previous round:  - If that payoff was 3
# or 5, cooperate in the current round. - If that payoff was 0 or 1, defect in
# the current round.

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
  
      last_my_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_my_payoff in (3, 5):
          return axl.Action.C
      if last_my_payoff in (0, 1):
          return axl.Action.D
  
      return axl.Action.C



# Start with defection in round one. From round two onward, look only at the
# actual outcome of the previous round: if both players ended up playing the
# same move (both C or both D), play C; if they played different moves (one C,
# one D), play D. Always determine sameness or difference from the actions that
# were actually taken after the noise flip, not from your intended moves.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == last_opp:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in the first round. For every round after that, use the
# payoff you just received to decide your next move:  - First, work out what
# action you actually played in that round. If your payoff was 3 or 0, you
# actually cooperated. If your payoff was 5 or 1, you actually defected. - If
# your payoff was 3 or 5, repeat that actual action in the next round. - If your
# payoff was 0 or 1, switch to the opposite action.

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
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]) if False else None
      # Determine our actual previous action from the payoff received in that round.
      # Since the match handles noise, the observed payoff corresponds to the actual actions played.
      my_last_score = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if my_last_score in (3, 0):
          actual_action = axl.Action.C
      else:
          actual_action = axl.Action.D
  
      if my_last_score in (3, 5):
          return actual_action
      else:
          return axl.Action.D if actual_action == axl.Action.C else axl.Action.C



# Start by cooperating in round 1. For every round after the first, look only at
# the opponent’s observed action in the immediately previous round (the action
# that actually occurred after the 10% flip chance).   - If the opponent’s
# observed action was C, cooperate.   - If the opponent’s observed action was D,
# then cooperate with a 10% probability and defect with a 90% probability.

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
  
      last_opponent_action = opponent.history[-1]
  
      if last_opponent_action == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)



# Defect unconditionally in rounds 1, 2, and 3.  From round 4 onward, examine
# the opponent's observed actions over the most recent 10 rounds (if fewer than
# 10 rounds have been played, use all prior rounds). If the opponent cooperated
# in at least 70% of those rounds, cooperate. Otherwise, defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number <= 3:
          return axl.Action.D
  
      recent_opponent_history = opponent.history[-10:]
      if len(recent_opponent_history) == 0:
          return axl.Action.D
  
      cooperation_rate = recent_opponent_history.cooperations / len(recent_opponent_history)
  
      if cooperation_rate >= 0.7:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in the first round.   For every round after that, decide
# as follows:    - If you observed the opponent cooperate in the previous round,
# cooperate.   - If you observed the opponent defect in the previous round, then
# look at what you intended to play in that same previous round (the action you
# chose before any noise flip):      - If you intended to cooperate, cooperate
# now.      - If you intended to defect, defect now.

class Cooperative_20(LLM_Strategy):
  n = 20
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      prev_opponent_action = opponent.history[-1]
      prev_intended_action = getattr(self, "_intended_action", axl.Action.C)
  
      if prev_opponent_action == axl.Action.C:
          intended = axl.Action.C
      else:
          if prev_intended_action == axl.Action.C:
              intended = axl.Action.C
          else:
              intended = axl.Action.D
  
      self._intended_action = intended
      return intended



# Start by cooperating in round one.   For every round after the first:  - If
# your payoff in the previous round was either 3 or 1, then cooperate.   - If
# your payoff in the previous round was either 5 or 0, then defect.

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
  
      last_my_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
      if last_my_score in (3, 1):
          return axl.Action.C
      return axl.Action.D



# Defect on the first round.   Keep track of how many times you have observed
# your opponent’s move as Cooperate, and record your own round‑by‑round payoffs
# for the most recent 20 rounds (use all available rounds if fewer than 20 have
# been played).  Always apply the first rule that matches:  1. If you have never
# observed a Cooperate from the opponent, then play Defect.   2. If at least 20
# rounds have been played and the sum of your payoffs in the last 20 rounds is
# 10 or lower, then play Defect now and in every remaining round – ignore the
# rules below.   3. If you have observed the opponent play Defect in both of the
# last two rounds, then play Defect.   4. Otherwise, play Cooperate.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forced_defect = False
          self._coop_seen = 0
          self._last20_payoffs = []
          return axl.Action.D
  
      if getattr(self, "_forced_defect", False):
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          self._coop_seen += 1
  
      # Record our payoff from the most recent round.
      last_payoff, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
      self._last20_payoffs.append(last_payoff)
      if len(self._last20_payoffs) > 20:
          self._last20_payoffs.pop(0)
  
      # Rule 2
      if len(self._last20_payoffs) >= 20 and sum(self._last20_payoffs[-20:]) <= 10:
          self._forced_defect = True
          return axl.Action.D
  
      # Rule 1
      if self._coop_seen == 0:
          return axl.Action.D
  
      # Rule 3
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      # Rule 4
      return axl.Action.C



# Start by cooperating in round 1.   For every later round, use only the payoff
# you received in the immediately previous round to decide:  - If your payoff
# was 3 or 5, repeat the action you played last round. - If your payoff was 0 or
# 1, switch to the opposite action.

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
  
      last_payoff = self.score - sum(
          self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]
      ) if len(self.history) > 1 else self.total_scores(self.history[:-1], opponent.history[:-1])[0]
  
      # Simpler and robust: infer the immediately previous round payoff from the last interaction.
      my_last_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if my_last_payoff in (3, 5):
          return self.history[-1]
      if my_last_payoff in (0, 1):
          return axl.Action.D if self.history[-1] == axl.Action.C else axl.Action.C
  
      return self.history[-1]



# Here is the strategy, restated with the same logic and no changes, as the
# feedback confirmed it contains no mistakes:  **Strategy: Start with
# cooperation, then mirror with a small chance of forgiveness.**  1. **Round
# 1:** Play C.  2. **Rounds 2 to 1000:** Base your move solely on the opponent’s
# observed action in the immediately preceding round (the action you actually
# saw, not what they may have intended).      - If the opponent played C, play
# C.      - If the opponent played D, play C with a 10% probability; otherwise
# play D.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)



# Defect on every round, regardless of the opponent’s past actions or any other
# information.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Cooperate in the first round. In every subsequent round, decide your intended
# action solely on the opponent’s previous behaviour, which you infer from your
# own last payoff:  - If your payoff last round was 3 or 5, the opponent
# cooperated: play C. - If your payoff last round was 0 or 1, the opponent
# defected: play D with 90% probability and play C with 10% probability.

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
  
      last_score = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]) if False else None
      # Infer opponent's last move from our last payoff
      my_last_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if my_last_payoff in (3, 5):
          return axl.Action.C
      elif my_last_payoff in (0, 1):
          return self._random.random_choice(0.1)
      else:
          return axl.Action.C



# Begin by cooperating on the first round.   From round 2 onward, base your
# action solely on the outcome of the immediately preceding round, using the
# actual actions observed (which may include noise flips).    Condition order:
# 1. If in the previous round both you and your opponent played the same action
# (both C or both D), then cooperate.   2. If in the previous round you and your
# opponent played different actions (one C, one D), then defect.    Apply these
# conditions on every round with no exceptions.

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D



# Here is an aggressive strategy with clear, ordered conditions for cooperation
# and defection:  1. **First round:** Defect.  2. **On all later rounds, apply
# the following checks in order:**    - **If your opponent’s last observed move
# was defection:** Defect.    - **If your opponent’s last observed move was
# cooperation, and all three of the most recent rounds meet these criteria** —
# you chose cooperate and your opponent’s observed move was cooperate —
# **then:** Defect.    - **Otherwise:** Cooperate.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if len(self.history) >= 3 and len(opponent.history) >= 3:
          last_three_self = self.history[-3:]
          last_three_opp = opponent.history[-3:]
          if all(m == axl.Action.C for m in last_three_self) and all(m == axl.Action.C for m in last_three_opp):
              return axl.Action.D
  
      return axl.Action.C



# In the first round, cooperate.  For every round after the first, use your
# intended action from the previous round together with the payoff you received
# to determine what both players actually did. (This is always possible: for
# example, if you intended to cooperate and received 3 or 0, you actually
# cooperated and your opponent cooperated or defected respectively; if you
# received 5 or 1, you actually defected and your opponent cooperated or
# defected respectively. Similar logic applies if you intended to defect.)
# Then choose your next action as follows:   - If both players actually made the
# same choice (both cooperated or both defected), cooperate.   - If the players
# made different choices, defect.

class Cooperative_23(LLM_Strategy):
  n = 23
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      def infer_actual_actions(intended: axl.Action, payoff: int):
          if intended == axl.Action.C:
              if payoff == 3:
                  return axl.Action.C, axl.Action.C
              if payoff == 0:
                  return axl.Action.C, axl.Action.D
              if payoff == 5:
                  return axl.Action.D, axl.Action.C
              if payoff == 1:
                  return axl.Action.D, axl.Action.D
          else:
              if payoff == 5:
                  return axl.Action.C, axl.Action.C
              if payoff == 1:
                  return axl.Action.C, axl.Action.D
              if payoff == 3:
                  return axl.Action.D, axl.Action.C
              if payoff == 0:
                  return axl.Action.D, axl.Action.D
          return None, None
  
      my_last_intended = self._intended_action
      my_last_actual, opp_last_actual = infer_actual_actions(my_last_intended, self.score - sum(
          self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]
      ) if False else None)
  
      # Determine last-round payoff directly from histories
      last_my_move = self.history[-1]
      last_opp_move = opponent.history[-1]
      if last_my_move == axl.Action.C and last_opp_move == axl.Action.C:
          last_payoff = 3
      elif last_my_move == axl.Action.C and last_opp_move == axl.Action.D:
          last_payoff = 0
      elif last_my_move == axl.Action.D and last_opp_move == axl.Action.C:
          last_payoff = 5
      else:
          last_payoff = 1
  
      my_last_actual, opp_last_actual = infer_actual_actions(my_last_intended, last_payoff)
  
      if my_last_actual == opp_last_actual:
          self._intended_action = axl.Action.C
      else:
          self._intended_action = axl.Action.D
  
      return self._intended_action



# Start by cooperating. For every round after the first, use only the action you
# **chose** (the button you pressed, not the possibly noisy outcome) and the
# payoff you received to decide:  - If your payoff was 3 or 5, repeat that same
# chosen action next round. - If your payoff was 0 or 1, switch to the opposite
# action next round.

class Neutral_23(LLM_Strategy):
  n = 23
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_choice = axl.Action.C
          return axl.Action.C
  
      last_payoff = self.score - getattr(self, "_last_score", 0)
  
      if last_payoff in (3, 5):
          next_choice = self._last_choice
      elif last_payoff in (0, 1):
          next_choice = axl.Action.D if self._last_choice == axl.Action.C else axl.Action.C
      else:
          next_choice = self._last_choice
  
      self._last_choice = next_choice
      self._last_score = self.score
      return next_choice



# Here is the revised strategy:  1. **Opening (rounds 1–10):** Intend to defect
# on every round, regardless of the opponent's actions.  2. **Ongoing assessment
# (from round 11 onward):** At the start of each round, determine the opponent's
# cooperation rate over the most recent 20 observed rounds (or all rounds played
# so far if fewer than 20). The rate is the fraction of those rounds in which
# the opponent's actual move was C. Classify the opponent as cooperative if this
# rate is 0.85 or higher; otherwise classify them as non-cooperative.  3.
# **Action when non-cooperative:** Always intend to defect.  4. **Action when
# cooperative:** Adopt a repeating cycle based on the round number: on any round
# whose number is an exact multiple of 10, intend to cooperate; on all other
# rounds, intend to defect. Follow this cycle for as long as the opponent
# remains classified as cooperative. Immediately stop the cycle and revert to
# always defecting if the classification changes to non-cooperative.  5.
# **Permanent defection lock (effective from round 31 onward):** If at any point
# the opponent's cooperation rate over the last 20 rounds falls below 0.5, lock
# in intended defection for every remaining round. Once locked, never cooperate
# again.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._locked_defect = False
  
      round_number = len(self.history) + 1
  
      recent_opponent_history = opponent.history[-20:]
      recent_len = len(recent_opponent_history)
      coop_rate = recent_opponent_history.cooperations / recent_len if recent_len > 0 else 0
  
      if round_number >= 31 and coop_rate < 0.5:
          self._locked_defect = True
  
      if self._locked_defect:
          return axl.Action.D
  
      if round_number <= 10:
          return axl.Action.D
  
      if coop_rate >= 0.85:
          if round_number % 10 == 0:
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.D



# Cooperate on the first round. For every round after the first:  - If your
# opponent cooperated in the previous round, cooperate. - If your opponent
# defected in the previous round, then cooperate with a 10% probability and
# defect otherwise.  Use this rule for all remaining rounds.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)



# In the first round, cooperate.   In every subsequent round, cooperate if your
# own payoff in the previous round was 3 or 5; defect if your own payoff in the
# previous round was 0 or 1.

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
  
      last_my_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_my_payoff in (3, 5):
          return axl.Action.C
      if last_my_payoff in (0, 1):
          return axl.Action.D
  
      return axl.Action.C



# Here is a rewritten version of the strategy, simplified to eliminate the
# redundancy noted in the feedback:  ---  Always defect. On every round, no
# matter what the opponent did in the previous round, always choose defect. This
# unconditional defection avoids the 0-point sucker payoff, never gives the
# opponent a free 5 points, and ensures that any cooperation by the opponent is
# met with a defection that yields 5 points for you, while mutual defection
# still gives 1 point rather than 0. The 10% noise may cause accidental
# cooperation, but the underlying intention remains to defect in all rounds.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D



# Cooperate in the first round. From the second round onward, cooperate unless
# the opponent's last two moves were both defections; in that case, defect.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the first two rounds. From the third round onward,
# base your choice on the opponent’s actual actions in the two most recent
# rounds. If the opponent played D in both of those two rounds, then play D this
# round. Otherwise, play C.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C