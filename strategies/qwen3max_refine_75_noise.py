import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy



# Start by playing C in the first round.    In each subsequent round:    1. If
# your opponent’s observed action in the previous round was C, play C.   2. If
# your opponent’s observed action in the previous round was D, play D—**unless**
# you played D in the previous round and your opponent played C two rounds ago;
# in that case, play C (to correct for possible noise).    Additionally, every
# 20 rounds (e.g., rounds 20, 40, 60, …), play C regardless of history to
# actively restore cooperation if noise has caused a breakdown.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number % 20 == 0:
          return axl.Action.C
  
      last_opp = opponent.history[-1]
      if last_opp == axl.Action.C:
          return axl.Action.C
  
      if last_opp == axl.Action.D:
          if len(self.history) >= 2 and self.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.C



# Start by playing Cooperate (C) in the first round.  From round 2 onward,
# follow these rules in order:  1. If it is one of the last 10 rounds (round 991
# or later), always play Defect (D).  2. If you have observed your opponent
# playing Defect (D) in at least two of the last three rounds, play D.  3.
# Otherwise, play C.  This approach tolerates occasional flipped actions due to
# noise by requiring a pattern of defection before retaliating, and it returns
# to cooperation quickly after isolated or mistaken Ds, helping to restore
# mutual cooperation if disrupted by noise.

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
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      if len(opponent.history) >= 3 and opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
  
      return axl.Action.C



# Start by playing C in the first round.  In every subsequent round, infer the
# opponent’s *intended* action from the previous round’s observed payoffs,
# accounting for the possibility of noise, and act as follows:  1. If the
# previous round’s payoffs were (3, 3), assume mutual intended cooperation and
# play C.   2. If the previous round’s payoffs were (1, 1), assume mutual
# intended defection and play C with 90% probability, D with 10% probability.
# 3. If you received 0 and the opponent received 5, assume you intended C and
# they intended D; play C.   4. If you received 5 and the opponent received 0,
# assume you intended D and they intended C; play D.    When uncertain—such as
# when payoffs suggest an outcome that could arise from multiple combinations of
# intended actions due to noise—default to playing C.

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
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      # Infer intended actions from observed noisy outcome when possible.
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
      elif my_last == axl.Action.D and opp_last == axl.Action.D:
          return self._random.random_choice(0.9)
      elif my_last == axl.Action.C and opp_last == axl.Action.D:
          return axl.Action.C
      elif my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.D
  
      # Default to cooperation when uncertain.
      return axl.Action.C



# Start by playing C in the first round. In each subsequent round:  1. If the
# opponent’s last observed action was C, play C.   2. If the opponent’s last
# observed action was D, play D.   3. However, if you have defected for three
# consecutive rounds, play C in the next round regardless of the opponent’s last
# action (to break cycles caused by noise).    This implements a forgiving tit-
# for-tat approach that cooperates by default, retaliates against defection, but
# periodically resets to cooperation to recover from mutual defection triggered
# by noise.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_streak = 0
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D:
          self._defect_streak += 1
      else:
          self._defect_streak = 0
  
      if self._defect_streak >= 3:
          self._defect_streak = 0
          return axl.Action.C
  
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D



# Start by playing Cooperate (C) in the first round.  From then on, base your
# action on the last *two* observed rounds of play, and use the following rules
# in order:  1. **If the last two observed outcomes were mutual C (C,C)**, play
# C.   2. **If you observe mutual D (D,D) in the last round but the round before
# that was mutual C**, assume noise may have occurred—play C to attempt
# reconciliation.   3. **If you observe alternating outcomes (e.g., you C /
# opponent D, then you D / opponent C) over the last two rounds**, treat this as
# likely noise disrupting mutual cooperation—play C.   4. **If you observe the
# opponent playing D in both of the last two rounds while you played C (or
# appeared to)**, assume sustained defection—play D.   5. **If mutual D (D,D)
# persists for three consecutive observed rounds**, continue playing D—but
# **every 10 rounds**, regardless of history, play C to test for cooperation.
# After any test C (whether from rule 2, 3, or 5):   - **If the observed outcome
# is mutual C**, return to rule 1 (cooperate).   - **If the opponent appears to
# respond with C (even if you were flipped to D)**, interpret this as
# willingness to cooperate—play C in the next round.    Always prioritize
# earlier rules over later ones when conditions overlap.

class Cooperative_2(LLM_Strategy):
  n = 2
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._test_c = False
          self._test_c_reason = None
          self._last_test_round = None
          return axl.Action.C
  
      round_num = len(self.history) + 1
  
      def last_two():
          return self.history[-2:], opponent.history[-2:]
  
      # After a test C, if the observed outcome is mutual C, return to cooperation.
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          self._test_c = False
          self._test_c_reason = None
          return axl.Action.C
  
      # If we played a test C and the opponent appears willing to cooperate, keep cooperating.
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Every 10 rounds, regardless of history, play C to test for cooperation.
      if round_num % 10 == 0:
          self._test_c = True
          self._test_c_reason = 5
          self._last_test_round = round_num
          return axl.Action.C
  
      if len(self.history) >= 2:
          my_last2 = list(self.history[-2:])
          op_last2 = list(opponent.history[-2:])
  
          # Rule 1: mutual C in the last two observed rounds.
          if my_last2 == [axl.Action.C, axl.Action.C] and op_last2 == [axl.Action.C, axl.Action.C]:
              return axl.Action.C
  
          # Rule 2: mutual D in the last round but mutual C before that.
          if (
              self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.C
              and opponent.history[-2] == axl.Action.C
          ):
              self._test_c = True
              self._test_c_reason = 2
              self._last_test_round = round_num
              return axl.Action.C
  
          # Rule 3: alternating outcomes over the last two rounds.
          if (
              self.history[-2] == axl.Action.C
              and opponent.history[-2] == axl.Action.D
              and self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.C
          ) or (
              self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.C
              and self.history[-1] == axl.Action.C
              and opponent.history[-1] == axl.Action.D
          ):
              self._test_c = True
              self._test_c_reason = 3
              self._last_test_round = round_num
              return axl.Action.C
  
          # Rule 4: opponent defected in both of the last two rounds while we played C.
          if (
              self.history[-2] == axl.Action.C
              and self.history[-1] == axl.Action.C
              and opponent.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
          ):
              # Rule 5: if mutual D persists for three consecutive observed rounds, continue D.
              if len(self.history) >= 3 and all(
                  self.history[-i] == axl.Action.D and opponent.history[-i] == axl.Action.D
                  for i in range(1, 4)
              ):
                  return axl.Action.D
              return axl.Action.D
  
          # Rule 5: mutual D persists for three consecutive observed rounds.
          if len(self.history) >= 3 and all(
              self.history[-i] == axl.Action.D and opponent.history[-i] == axl.Action.D
              for i in range(1, 4)
          ):
              if round_num % 10 == 0:
                  self._test_c = True
                  self._test_c_reason = 5
                  self._last_test_round = round_num
                  return axl.Action.C
              return axl.Action.D
  
      # Default: cooperate unless sustained defection suggests otherwise.
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Play as follows:  1. Start by cooperating in the first round.   2. In each
# subsequent round, consider the opponent’s observed action from the previous
# round.   3. If the opponent was observed to cooperate, cooperate.   4. If the
# opponent was observed to defect, cooperate anyway with probability 10%;
# otherwise, defect.    This introduces forgiveness: when the opponent appears
# to defect, you assume there’s a chance it was due to noise (since noise occurs
# 10% of the time) and occasionally respond with cooperation to prevent endless
# retaliation. This helps recover from mismatches while still deterring
# sustained exploitation.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)



# Start by playing Defect (D) in the first round. After that, follow these rules
# in order:  1. If the opponent has played Defect (D) in at least 70% of the
# last 20 observed rounds, play Defect (D).   2. If you have played Defect (D)
# for the last 10 consecutive rounds and the opponent has played Cooperate (C)
# in more than half of the last 10 observed rounds, play Cooperate (C) once to
# test for mutual cooperation.   3. Otherwise, play Defect (D).  When
# interpreting the opponent’s past actions, use the observed (possibly noisy)
# actions directly—do not attempt to correct for noise. Always default to Defect
# unless the specific condition in step 2 is met. After a test cooperation (step
# 2), immediately return to Defect unless the opponent continues to cooperate
# consistently (as judged by step 1).

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._tested_cooperation = False
          return axl.Action.D
  
      last20_opp = opponent.history[-20:]
      last10_self = self.history[-10:]
      last10_opp = opponent.history[-10:]
  
      if len(last20_opp) > 0 and last20_opp.count(axl.Action.D) / len(last20_opp) >= 0.7:
          return axl.Action.D
  
      if (
          len(last10_self) == 10
          and last10_self.count(axl.Action.D) == 10
          and len(last10_opp) == 10
          and last10_opp.count(axl.Action.C) > 5
          and not self._tested_cooperation
      ):
          self._tested_cooperation = True
          return axl.Action.C
  
      self._tested_cooperation = False
      return axl.Action.D



# Start by cooperating in the first round.  For each subsequent round:  1. **If
# the current round number is a multiple of 10 (i.e., rounds 10, 20, 30, ...,
# 1000), cooperate.** This periodic reset helps recover from mutual defection
# that may have been triggered by noise.  2. **Otherwise, look at what your
# opponent appeared to play in the previous round:**    - If they appeared to
# cooperate, cooperate.    - If they appeared to defect, defect.  This ordering
# ensures the reset rule takes priority over the reaction rule, eliminating
# ambiguity when both would apply. The strategy remains simple, promotes
# cooperation, and uses regular resets to mitigate the risk of noise-induced
# cycles of retaliation.

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
  
      round_number = len(self.history) + 1
  
      if round_number % 10 == 0:
          return axl.Action.C
  
      return opponent.history[-1] if opponent.history else axl.Action.C



# Start by cooperating in the first round. From the second round onward, decide
# your action based on the last two observed outcomes (yours and your
# opponent’s) using the following rules in order:  1. If the last two rounds
# both showed mutual cooperation (C,C), cooperate.   2. If the previous round
# showed mutual defection (D,D), but the round before that was mutual
# cooperation (C,C), cooperate.   3. If the previous round showed you cooperated
# and your opponent defected (C,D), but the round before that was mutual
# cooperation (C,C), cooperate (to allow for the possibility the defection was
# due to noise).   4. If you observe a pattern of your opponent defecting in two
# of the last three rounds (including the most recent), defect.   5. In all
# other cases, cooperate.  This approach uses short-term history to distinguish
# likely intentional defection from noise, avoids overreacting to single
# apparent defections after cooperation, and limits exploitation by responding
# to consistent defection while remaining generally cooperative.

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
  
      h = self.history
      oh = opponent.history
  
      # Rule 1: If the last two rounds both showed mutual cooperation, cooperate.
      if len(h) >= 2 and h[-1] == axl.Action.C and oh[-1] == axl.Action.C and h[-2] == axl.Action.C and oh[-2] == axl.Action.C:
          return axl.Action.C
  
      # Rule 2: If the previous round showed mutual defection, but the round before that was mutual cooperation, cooperate.
      if len(h) >= 2 and h[-1] == axl.Action.D and oh[-1] == axl.Action.D:
          if len(h) >= 2 and h[-2] == axl.Action.C and oh[-2] == axl.Action.C:
              return axl.Action.C
  
      # Rule 3: If you cooperated and opponent defected, but the round before that was mutual cooperation, cooperate.
      if len(h) >= 2 and h[-1] == axl.Action.C and oh[-1] == axl.Action.D:
          if h[-2] == axl.Action.C and oh[-2] == axl.Action.C:
              return axl.Action.C
  
      # Rule 4: If opponent defected in two of the last three rounds (including the most recent), defect.
      if len(oh) >= 3 and oh[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
  
      # Rule 5: In all other cases, cooperate.
      return axl.Action.C



# Start by playing Cooperate (C) in round 1.    Thereafter, in each round:    1.
# If your opponent’s observed action in the previous round was Cooperate (C),
# play Cooperate (C).   2. If your opponent’s observed action in the previous
# round was Defect (D), play Defect (D).    However, to guard against noise:
# 3. If you have observed a Defect (D) from your opponent in the previous round
# but Cooperate (C) in the round before that (i.e., a single isolated D), still
# play Cooperate (C) — treat it as likely noise.   4. Only defect if you observe
# two or more Defects (D) from your opponent in the last three rounds.    Once
# you defect due to confirmed defection, return to Cooperate (C) if the opponent
# plays Cooperate (C) in the next two consecutive rounds.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._confirmed_defection = False
          self._coop_streak_after_defection = 0
          return axl.Action.C
  
      opp_hist = opponent.history
      last = opp_hist[-1]
      prev = opp_hist[-2] if len(opp_hist) >= 2 else axl.Action.C
      prev2 = opp_hist[-3] if len(opp_hist) >= 3 else axl.Action.C
  
      # If we previously defected due to confirmed defection, return to C after
      # two consecutive observed cooperations.
      if self._confirmed_defection:
          if last == axl.Action.C:
              self._coop_streak_after_defection += 1
          else:
              self._coop_streak_after_defection = 0
  
          if self._coop_streak_after_defection >= 2:
              self._confirmed_defection = False
              self._coop_streak_after_defection = 0
              return axl.Action.C
  
          return axl.Action.D
  
      # Guard against noise: a single isolated D in the previous round is ignored.
      if last == axl.Action.D and prev == axl.Action.C:
          return axl.Action.C
  
      # Defect only if there are two or more defections in the last three rounds.
      defections_last_three = opp_hist[-3:].count(axl.Action.D)
      if defections_last_three >= 2:
          self._confirmed_defection = True
          self._coop_streak_after_defection = 0
          return axl.Action.D
  
      return axl.Action.C



# Start by playing **Cooperate** in the first round. In every subsequent round,
# base your decision only on the **actions you and your opponent actually
# played** in the previous round (not on inferred payoffs), recognizing that
# each observed action may have been flipped by noise with 10% probability.  Use
# the following rules, applied in order:  1. **If both you and your opponent
# played C in the previous round**, play **C**.   2. **If you played C and your
# opponent played D in the previous round**, play **D**.   3. **If you played D
# and your opponent played C in the previous round**, play **C**.   4. **If both
# you and your opponent played D in the previous round**, play **D**.  To handle
# noise, add a **one-step forgiveness rule**:  - **If rule 2 or rule 4 would
# cause you to defect, but the previous round was the first time in the last two
# rounds that the opponent played D (i.e., the opponent played C two rounds ago
# and D last round), then override the decision and play C instead.**  This
# allows a single lapse—possibly due to noise—to be forgiven, while still
# responding to sustained defection. The strategy never retaliates after just
# one observed D if the opponent had been cooperating before, but will defect if
# D is observed twice in a row.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      # One-step forgiveness: if opponent's last D was preceded by C, forgive once.
      if len(opponent.history) >= 2:
          opp_two_ago = opponent.history[-2]
          if last_opp == axl.Action.D and opp_two_ago == axl.Action.C:
              return axl.Action.C
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Play as follows:  1. Start by cooperating in the first round.   2. In each
# subsequent round, consider your opponent’s last observed action.   3. If your
# opponent was observed to cooperate in the previous round, cooperate.   4. If
# your opponent was observed to defect in the previous round, defect—but only if
# your opponent has been observed to defect in at least two of the last three
# rounds; otherwise, cooperate (this filters out isolated defections likely
# caused by noise).   5. If you and your opponent have both been observed to
# defect for three consecutive rounds, cooperate in the next round to attempt to
# restore mutual cooperation.

class Neutral_4(LLM_Strategy):
  n = 4
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._consecutive_dd = 0
          return axl.Action.C
  
      last_opp = opponent.history[-1]
  
      if len(self.history) >= 3 and self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          self._consecutive_dd = 0
          return axl.Action.C
  
      if last_opp == axl.Action.C:
          self._consecutive_dd = 0
          return axl.Action.C
  
      recent_opp = opponent.history[-3:]
      if recent_opp.count(axl.Action.D) >= 2:
          self._consecutive_dd = self._consecutive_dd + 1 if self.history[-1] == axl.Action.D and last_opp == axl.Action.D else 1
          return axl.Action.D
  
      self._consecutive_dd = 0
      return axl.Action.C



# Start by playing D in the first round.    Thereafter, in each round:   - If
# your opponent’s observed action in the previous round was D, play D.   - If
# your opponent’s observed action in the previous round was C, play D with 90%
# probability and C with 10% probability.    (Interpret “observed action” as the
# action you actually saw, accounting for possible noise—i.e., use the raw
# outcome from the prior round without trying to correct for noise.)

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
  
      last_opponent_action = opponent.history[-1]
  
      if last_opponent_action == axl.Action.D:
          return axl.Action.D
  
      return self._random.random_choice(0.1)



# Start by cooperating in the first round.  For each subsequent round, apply the
# following rules in order:  1. **If fewer than 5 prior rounds have been
# played**, cooperate if your opponent has cooperated in at least half of the
# observed rounds so far (rounding down); otherwise, defect.  2. **If the
# previous round resulted in mutual defection (both players observed to play
# D)**, cooperate—this is a reset attempt to restore cooperation, acknowledging
# that noise may have caused the breakdown.  3. **If your opponent has
# cooperated in at least 3 of the last 5 observed rounds**, cooperate.  4.
# **Otherwise**, defect.  This approach handles early-round ambiguity,
# explicitly forgives mutual defection (which may stem from noise), uses recent
# behavior to infer intent while tolerating occasional flipped actions, and
# maintains a clear priority among conditions. No special endgame adjustment is
# included, as the horizon (1000 rounds) is long and the risk of exploitation
# near the end is outweighed by the benefit of sustained cooperation.

class Cooperative_5(LLM_Strategy):
  n = 5
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      rounds_played = len(self.history)
  
      # Rule 1: Early-game behavior for fewer than 5 prior rounds.
      if rounds_played < 5:
          if opponent.history.cooperations >= (rounds_played // 2):
              return axl.Action.C
          return axl.Action.D
  
      # Rule 2: If the previous round was mutual defection, attempt reset.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # Rule 3: If opponent cooperated in at least 3 of the last 5 observed rounds, cooperate.
      if opponent.history[-5:].count(axl.Action.C) >= 3:
          return axl.Action.C
  
      # Rule 4: Otherwise defect.
      return axl.Action.D



# Start by cooperating in the first round.  In every subsequent round:  1. If
# your opponent’s last observed action was cooperation, cooperate.   2. If your
# opponent’s last observed action was defection, check the action you yourself
# played in the previous round:      - If you had cooperated, assume the
# opponent’s defection might be due to noise, and cooperate.      - If you had
# defected, defect.  This approach treats a single observed defection after your
# own cooperation as potentially accidental (due to the 10% noise) and responds
# with forgiveness by continuing to cooperate once. However, if you defected and
# then observe defection, you treat it as likely intentional and respond in
# kind. This helps maintain cooperation in the face of noise while still
# deterring exploitation.

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
  
      last_opponent_action = opponent.history[-1]
      if last_opponent_action == axl.Action.C:
          return axl.Action.C
  
      last_own_action = self.history[-1]
      if last_own_action == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Start by playing Cooperate (C) in the first round. After that, follow these
# rules in order for each subsequent round:  1. If your opponent’s observed
# action in the previous round was Defect (D), play Defect (D) in the current
# round.   2. If your opponent’s observed action in the previous round was
# Cooperate (C), play Cooperate (C) in the current round.    However, every 10
# rounds (i.e., in rounds 10, 20, 30, …), regardless of the opponent’s last
# action, play Cooperate (C) to test for and potentially restore mutual
# cooperation in case noise caused a breakdown.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) % 10 == 0:
          return axl.Action.C
  
      return opponent.history[-1]



# Start by cooperating in the first round.  From round 2 onward, base your
# decision on the last two rounds of observed outcomes to reduce sensitivity to
# noise:  1. If the opponent appeared to cooperate in both of the last two
# rounds, cooperate.   2. If the opponent appeared to defect in both of the last
# two rounds, defect.   3. If the opponent’s observed actions in the last two
# rounds are mixed (one C, one D in any order), cooperate—treat this as likely
# caused by noise rather than intentional exploitation.    Continue this
# approach through round 990.  From round 991 to 1000 (the final 10 rounds),
# switch to always defecting—regardless of history—to avoid being exploited when
# future retaliation no longer matters.

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
  
      if round_number >= 991:
          return axl.Action.D
  
      if len(opponent.history) >= 2:
          last_two = opponent.history[-2:]
          if last_two.count(axl.Action.C) == 2:
              return axl.Action.C
          if last_two.count(axl.Action.D) == 2:
              return axl.Action.D
          return axl.Action.C
  
      return axl.Action.C



# Start by cooperating in the first round. In each subsequent round, base your
# decision only on the *observed* actions from the previous round (accounting
# for possible noise), and follow these rules in order:  1. If the previous
# observed outcome was mutual cooperation (C, C), cooperate.   2. If the
# previous observed outcome was mutual defection (D, D), defect.   3. If the
# previous observed outcome was (C, D) — you appeared to cooperate, opponent
# appeared to defect — defect.   4. If the previous observed outcome was (D, C)
# — you appeared to defect, opponent appeared to cooperate — cooperate **only
# if** the round before that was (C, C); otherwise, defect.  This approach
# maintains cooperation after trust is established, retaliates against apparent
# defection, avoids being exploited after mutual defection, and limits
# forgiveness in response to apparent exploitation unless it likely resulted
# from noise following a history of mutual cooperation.

class Neutral_6(LLM_Strategy):
  n = 6
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_observed_pair = None
          return axl.Action.C
  
      prev_self = self.history[-1]
      prev_opp = opponent.history[-1]
      prev_pair = (prev_self, prev_opp)
  
      if prev_pair == (axl.Action.C, axl.Action.C):
          action = axl.Action.C
      elif prev_pair == (axl.Action.D, axl.Action.D):
          action = axl.Action.D
      elif prev_pair == (axl.Action.C, axl.Action.D):
          action = axl.Action.D
      elif prev_pair == (axl.Action.D, axl.Action.C):
          if len(self.history) >= 2 and self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.C:
              action = axl.Action.C
          else:
              action = axl.Action.D
      else:
          action = axl.Action.C
  
      self._last_observed_pair = prev_pair
      return action



# Start by playing D. After each round, follow these rules in order:  1. If both
# players received the payoff for mutual defection (1 each) in the last round,
# continue playing D.   2. If you received 0 (meaning you played C and the
# opponent effectively played D), switch to or stay on D.   3. If you received 5
# (meaning you played D and the opponent effectively played C), stay on D.   4.
# If both players received 3 (mutual cooperation payoff), play C in the next
# round.   5. If you have played D for 10 consecutive rounds and the opponent’s
# recent actions—despite noise—suggest persistent cooperation (e.g., you’ve
# received at least two 5s in the last five rounds), play C once to test for
# restoring mutual cooperation.   6. After playing C, if the resulting payoff is
# not 3 (i.e., the opponent did not effectively cooperate), revert to D and do
# not cooperate again for at least 20 rounds.  Always assume actions may have
# been flipped due to noise, but only interpret cooperation as credible if it
# yields a mutual payoff of 3 or repeated high payoffs (5s) for you.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._cooldown = 0
          self._forced_test = False
          self._d_streak = 0
          return axl.Action.D
  
      if self._cooldown > 0:
          self._cooldown -= 1
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
      my_last, opp_last = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_self == axl.Action.D:
          self._d_streak += 1
      else:
          self._d_streak = 0
  
      if my_last == 1 and opp_last == 1:
          return axl.Action.D
  
      if my_last == 0:
          self._d_streak = 0
          return axl.Action.D
  
      if my_last == 5:
          return axl.Action.D
  
      if my_last == 3 and opp_last == 3:
          self._d_streak = 0
          self._forced_test = False
          return axl.Action.C
  
      if self._cooldown > 0:
          return axl.Action.D
  
      if self._d_streak >= 10:
          recent = self.total_scores(self.history[-5:], opponent.history[-5:])
          if recent[0] >= 10:
              self._forced_test = True
              return axl.Action.C
  
      if last_self == axl.Action.C:
          if my_last != 3:
              self._cooldown = 20
              self._forced_test = False
              self._d_streak = 0
              return axl.Action.D
          return axl.Action.C
  
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.  From round 2 onward, base
# your action on the *observed* actions from the previous round, but incorporate
# forgiveness to handle noise:  1. If the previous round’s observed outcome was
# (C, C), play C.   2. If the observed outcome was (C, D) or (D, C), play
# C—treat single-sided defection as likely caused by noise and forgive.   3. If
# the observed outcome was (D, D), play C with 50% probability and D with 50%
# probability—this introduces randomness to escape potential noise-induced
# mutual defection traps.  Additionally, to further guard against long cycles of
# misunderstanding, if you have defected (intentionally or not) in three
# consecutive rounds *and* the opponent has appeared to defect in all three,
# play C in the next round regardless of the above rules to reset cooperation.

class Cooperative_7(LLM_Strategy):
  n = 7
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_streak = 0
          self._force_cooperate = False
          return axl.Action.C
  
      if len(self.history) >= 1:
          last_self = self.history[-1]
          last_opp = opponent.history[-1]
  
          if last_self == axl.Action.D:
              self._defect_streak += 1
          else:
              self._defect_streak = 0
  
          if self._defect_streak >= 3 and last_opp == axl.Action.D:
              self._force_cooperate = True
          else:
              self._force_cooperate = False
      else:
          self._defect_streak = 0
          self._force_cooperate = False
  
      if self._force_cooperate:
          return axl.Action.C
  
      last_outcome = (self.history[-1], opponent.history[-1])
  
      if last_outcome == (axl.Action.C, axl.Action.C):
          return axl.Action.C
      if last_outcome in ((axl.Action.C, axl.Action.D), (axl.Action.D, axl.Action.C)):
          return axl.Action.C
      if last_outcome == (axl.Action.D, axl.Action.D):
          return self._random.random_choice(0.5)
  
      return axl.Action.C



# Play as follows:  1. Start by cooperating in the first round.   2. In each
# subsequent round, consider your opponent’s last *two* observed actions.   3.
# If at least one of those two observed actions was cooperation, cooperate.   4.
# If both observed actions were defection, defect.    This approach maintains
# neutrality by generally reciprocating cooperation, while allowing a single
# noisy defection to be forgiven—preventing endless retaliation cycles.
# Requiring two consecutive observed defections before retaliating reduces the
# risk of misinterpreting a flipped action due to noise, supporting sustained
# mutual cooperation when possible.

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
  
      last_two = opponent.history[-2:]
      if axl.Action.D in last_two and last_two.count(axl.Action.D) == 2:
          return axl.Action.D
      return axl.Action.C



# Play D in the first round. In each subsequent round:  1. If your opponent
# played D in the previous round, play D.   2. If your opponent played C in the
# previous round, play D—unless you have observed your opponent play C in at
# least 3 of the last 5 rounds (including the most recent one); in that case,
# play C.  This allows you to exploit consistent cooperators while cautiously
# re-establishing cooperation if the opponent demonstrates a clear pattern of
# cooperation despite noise, thereby avoiding prolonged mutual defection when
# cooperation is likely to be stable and beneficial in the long run.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      recent_opponent = opponent.history[-5:]
      if recent_opponent.count(axl.Action.C) >= 3:
          return axl.Action.C
  
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.  After that, maintain a
# running count of the opponent’s observed actions over the last five rounds
# (including the most recent one). Use this window to assess their recent
# behavior, accounting for the possibility of noise.  In each subsequent round:
# 1. If at least four of the opponent’s last five observed actions were C, play
# C.   2. If three or fewer of the opponent’s last five observed actions were C,
# play D.    This approach smooths out occasional flipped actions due to noise,
# avoids overreacting to single defections, and protects against sustained
# exploitation by consistently defecting opponents.

class Cooperative_8(LLM_Strategy):
  n = 8
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._recent_opponent_actions = []
          return axl.Action.C
  
      recent = list(opponent.history[-5:])
      c_count = recent.count(axl.Action.C)
  
      if c_count >= 4:
          return axl.Action.C
      return axl.Action.D



# Play as follows:  1. Start by cooperating in the first round.   2. In each
# subsequent round, consider the opponent’s observed actions from the previous
# two rounds (or just the previous round if in round 2).   3. If at least one of
# those observed actions was cooperation, cooperate.   4. Only defect if the
# opponent was observed to defect in both of the previous two rounds.    This
# approach tolerates isolated defections—likely due to noise—while still
# responding to sustained defection.

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
  
      if len(opponent.history) == 1:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      if opponent.history[-1] == axl.Action.C or opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D



# Start by playing C in the first round.    Thereafter, in each round:   - If
# the opponent’s observed action in the previous round was C, play C.   - If the
# opponent’s observed action in the previous round was D, play D.    However, to
# guard against noise disrupting cooperation:   - If you have played D for three
# consecutive rounds and the opponent’s observed actions in those same rounds
# were all C, switch back to playing C in the next round.    Otherwise, follow
# the standard response based on the opponent’s last observed move.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._d_streak = 0
          return axl.Action.C
  
      if len(self.history) >= 3:
          last_three_self = self.history[-3:]
          last_three_opp = opponent.history[-3:]
          if (
              last_three_self.count(axl.Action.D) == 3
              and last_three_opp.count(axl.Action.C) == 3
          ):
              self._d_streak = 0
              return axl.Action.C
  
      last_opp = opponent.history[-1]
      if last_opp == axl.Action.C:
          self._d_streak = 0
          return axl.Action.C
      else:
          self._d_streak = getattr(self, "_d_streak", 0) + 1
          return axl.Action.D



# Start by cooperating in the first round.  From the second round onward, base
# your decision on the last two rounds of observed play, and follow these rules
# in order:  1. If the opponent has appeared to cooperate in at least one of the
# last two rounds, cooperate.   2. If the opponent has appeared to defect in
# both of the last two rounds, defect.  This approach tolerates isolated
# apparent defections—likely due to noise—by requiring two consecutive observed
# defections before retaliating, while still responding to sustained defection.
# It avoids overreacting to single noisy outcomes and reduces the risk of
# entering mutual retaliation loops.

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
  
      last_two_opponent_moves = opponent.history[-2:]
  
      if axl.Action.D in last_two_opponent_moves and last_two_opponent_moves.count(axl.Action.D) == 2:
          return axl.Action.D
  
      return axl.Action.C



# Play Cooperate (C) in the first round. In each subsequent round, base your
# action on the *observed* (i.e., possibly noisy) actions from the previous
# round, but adjust for the likelihood of noise as follows:  1. If both you and
# your opponent appeared to play C, play C.   2. If you appeared to play C and
# your opponent appeared to play D, play D **only if** this is the second
# consecutive time you’ve observed the opponent defect after you appeared to
# cooperate; otherwise, play C.   3. If you appeared to play D and your opponent
# appeared to play C, play C.   4. If both you and your opponent appeared to
# play D, play C.

class Neutral_9(LLM_Strategy):
  n = 9
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._consecutive_cd_observations = 0
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          self._consecutive_cd_observations = 0
          return axl.Action.C
  
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          self._consecutive_cd_observations += 1
          if self._consecutive_cd_observations >= 2:
              return axl.Action.D
          return axl.Action.C
  
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          self._consecutive_cd_observations = 0
          return axl.Action.C
  
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          self._consecutive_cd_observations = 0
          return axl.Action.C
  
      self._consecutive_cd_observations = 0
      return axl.Action.C



# Start by playing D in the first round. After that, follow these rules in
# order:  1. If your opponent played C in the previous round (as observed,
# accounting for possible noise), play C in the current round with 10%
# probability and D with 90% probability.   2. If your opponent played D in the
# previous round, play D.    This introduces limited, cautious generosity to
# test for and occasionally restore cooperation, while remaining predominantly
# aggressive to exploit cooperative behavior when it appears.

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
  
      last_opponent_action = opponent.history[-1]
  
      if last_opponent_action == axl.Action.C:
          return self._random.random_choice(0.1)
  
      return axl.Action.D



# Start by cooperating in the first round.  Thereafter, in each round:  1. If
# both players appeared to cooperate in the previous round, cooperate.   2. If
# only your opponent appeared to defect in the previous round, cooperate—treat
# the defection as likely due to noise, unless this is part of a recent pattern
# of repeated observed defections. Specifically, if your opponent has appeared
# to defect in three or more of the last five rounds, defect; otherwise,
# cooperate.   3. If only you appeared to defect in the previous round (but your
# opponent appeared to cooperate), cooperate—assume your own defection was due
# to noise and reaffirm cooperation.   4. If both players appeared to defect in
# the previous round, cooperate with probability 30% to allow recovery from
# mutual misunderstandings caused by noise.    Apply these rules for all 1000
# rounds.

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
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
  
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          recent_opp_defections = opponent.history[-5:].count(axl.Action.D)
          if recent_opp_defections >= 3:
              return axl.Action.D
          return axl.Action.C
  
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.C
  
      # Both appeared to defect last round
      return self._random.random_choice(0.3)



# Start by cooperating in the first round.  From the second round onward, decide
# your action based on your opponent’s last two observed moves:  1. If both of
# the opponent’s last two observed moves were cooperation, cooperate.   2. If
# both were defection, defect.   3. If the last two observed moves are mixed
# (one C and one D, in any order), cooperate.  Apply this rule for all remaining
# rounds, using only the moves actually observed (including any resulting from
# noise).

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
  
      last_two = opponent.history[-2:]
  
      if len(last_two) < 2:
          return axl.Action.C
  
      if last_two[0] == axl.Action.C and last_two[1] == axl.Action.C:
          return axl.Action.C
      if last_two[0] == axl.Action.D and last_two[1] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C



# Start by playing C in the first round.    Thereafter, in each round:    1. If
# the opponent’s observed action in the previous round was C, play C.   2. If
# the opponent’s observed action in the previous round was D, play D.
# However, to account for noise:    3. Every 10 rounds (i.e., in rounds 10, 20,
# 30, …), play C regardless of the opponent’s last action—this serves as a
# “reset” to reestablish cooperation if noise caused a mistaken defection.
# Otherwise, follow steps 1 and 2 strictly.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number % 10 == 0:
          return axl.Action.C
  
      last_opponent_action = opponent.history[-1]
      if last_opponent_action == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in the first round.  From round 2 onward, decide your
# action based on the opponent’s *observed* actions over the last two rounds
# (i.e., the most recent and the one before it):  1. If the opponent appeared to
# cooperate in **both** of the last two rounds, cooperate.   2. If the opponent
# appeared to defect in **both** of the last two rounds, defect.   3. If the
# opponent’s observed actions in the last two rounds are mixed (one C and one D,
# in any order), cooperate.  Apply this rule for all remaining rounds up to
# 1000.

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
  
      opp_history = opponent.history
      if len(opp_history) < 2:
          return axl.Action.C
  
      last_two = opp_history[-2:]
      if last_two.count(axl.Action.C) == 2:
          return axl.Action.C
      if last_two.count(axl.Action.D) == 2:
          return axl.Action.D
      return axl.Action.C



# Play Cooperate (C) in the first round. In each subsequent round, base your
# action on the *observed* (i.e., noisy) outcome of the previous round, but
# interpret it with the possibility of noise in mind:  1. If both players
# appeared to play C in the previous round, play C.   2. If both players
# appeared to play D in the previous round, play C.   3. If you appeared to play
# C and your opponent appeared to play D in the previous round, play D *only if*
# this is the first such mismatch in a row; if the same mismatch (you C, them D)
# has occurred for two or more consecutive rounds, play C (assuming the first
# instance may have been noise).   4. If you appeared to play D and your
# opponent appeared to play C in the previous round, play C *only if* you
# intended to play C (i.e., you suspect your own action was flipped by noise);
# otherwise, if you intentionally played D, play C—but since intent isn’t
# observable in the rule-based format, treat this case as likely noise and play
# C, while recognizing you may have gained from an accidental defection.    To
# make the strategy implementable without memory of intent, replace rules 3 and
# 4 with a symmetric, history-based approach:  **Revised implementable
# version:**   - Play C in round 1.   - In each subsequent round:     a. If the
# previous observed outcome was (C, C) or (D, D), play C.     b. If the previous
# observed outcome was (C, D), play D *only if* the round before that was not
# (C, D); if the last two observed rounds were both (C, D), play C (to forgive
# potential noise).     c. If the previous observed outcome was (D, C), play C.
# This balances retaliation against sustained defection with forgiveness for
# isolated mismatches likely caused by noise.

class Neutral_11(LLM_Strategy):
  n = 11
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_cd_streak = 0
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          self._last_cd_streak = 0
          return axl.Action.C
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          self._last_cd_streak = 0
          return axl.Action.C
  
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          self._last_cd_streak = getattr(self, "_last_cd_streak", 0) + 1
          if self._last_cd_streak >= 2:
              return axl.Action.C
          return axl.Action.D
  
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          self._last_cd_streak = 0
          return axl.Action.C
  
      self._last_cd_streak = 0
      return axl.Action.C



# Start by playing Cooperate (C) in the first round. After that, follow these
# rules in order:  1. If it is one of the last 10 rounds (round 991 or later),
# always play Defect (D).   2. If your opponent’s last observed action was
# Defect (D), play Defect (D).   3. If your opponent’s last observed action was
# Cooperate (C), play Cooperate (C).   4. However, if you have observed your
# opponent play Defect (D) in two or more of the last three rounds, play Defect
# (D) regardless of the most recent action.    This strategy begins
# cooperatively, retaliates against apparent defection, forgives occasional
# noise by responding to a single C after D, but defects persistently if
# defection appears intentional, and always defects near the end when future
# retaliation no longer matters.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) >= 3 and opponent.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the first round.  From then on, decide your action
# based on the pattern of your opponent’s last two observed moves, to reduce
# sensitivity to noise:  1. If your opponent appeared to cooperate in both of
# the last two rounds, cooperate.   2. If your opponent appeared to defect in
# both of the last two rounds, defect.   3. If the last two observed moves are
# mixed (one C and one D, in any order), assume the defection was likely due to
# noise and cooperate.    Continue this logic for all subsequent rounds, always
# using the two most recent observed actions to guide your choice.

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
  
      if len(opponent.history) < 2:
          return axl.Action.C
  
      last_two = opponent.history[-2:]
  
      if last_two.count(axl.Action.C) == 2:
          return axl.Action.C
      if last_two.count(axl.Action.D) == 2:
          return axl.Action.D
  
      return axl.Action.C



# Play Cooperate (C) in the first round. In each subsequent round, base your
# action on the *observed* outcome of the previous round (after noise), but
# interpret it with caution due to possible action flips:  1. If both players
# were observed to play C, play C.   2. If you were observed to play C and your
# opponent was observed to play D, play D *only if* this is the first such
# occurrence in a row; if it happens repeatedly (e.g., two or more consecutive
# rounds), assume noise may be involved and revert to C.   3. If you were
# observed to play D and your opponent was observed to play C, play C.   4. If
# both players were observed to play D, play C—treat mutual observed defection
# as likely caused by noise or mutual misunderstanding, not intentional
# defection.    (“Observed” means the action actually seen after the 10% noise
# is applied.)

class Neutral_12(LLM_Strategy):
  n = 12
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_obs_cd_streak = 0
          return axl.Action.C
  
      my_obs = self.history[-1]
      opp_obs = opponent.history[-1]
  
      if my_obs == axl.Action.C and opp_obs == axl.Action.C:
          self._last_obs_cd_streak = 0
          return axl.Action.C
  
      if my_obs == axl.Action.C and opp_obs == axl.Action.D:
          self._last_obs_cd_streak += 1
          if self._last_obs_cd_streak == 1:
              return axl.Action.D
          return axl.Action.C
  
      if my_obs == axl.Action.D and opp_obs == axl.Action.C:
          self._last_obs_cd_streak = 0
          return axl.Action.C
  
      if my_obs == axl.Action.D and opp_obs == axl.Action.D:
          self._last_obs_cd_streak = 0
          return axl.Action.C
  
      self._last_obs_cd_streak = 0
      return axl.Action.C



# Start by playing Cooperate (C) in the first round. After that, follow these
# rules in order:  1. If it is one of the last 10 rounds (round 991 or later),
# play Defect (D).   2. Otherwise, if your opponent’s observed action in the
# previous round was Defect (D), play Defect (D) with 90% probability and
# Cooperate (C) with 10% probability.   3. Otherwise (your opponent’s observed
# action was Cooperate (C)), play Cooperate (C).

class Aggressive_13(LLM_Strategy):
  n = 13
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
  
      if opponent.history[-1] == axl.Action.D:
          return self._random.random_choice(0.1)
  
      return axl.Action.C



# Start by cooperating in the first round.  From round 2 onward, follow these
# rules based on the *observed* actions from the previous round:  1. **If both
# players appeared to cooperate (C, C):** Cooperate.   2. **If you appeared to
# cooperate and your opponent appeared to defect (C, D):** Defect.   3. **If you
# appeared to defect and your opponent appeared to cooperate (D, C):**      -
# Defect *only if* your opponent has appeared to defect in at least one of the
# two rounds before the previous round.      - Otherwise, cooperate (to account
# for possible noise in your own action).   4. **If both players appeared to
# defect (D, D):**      - Cooperate *only if* the round before the previous one
# showed (C, C) or (C, D).      - Otherwise, defect (to avoid being exploited
# after repeated mutual defection).  Maintain a short memory of the last two
# observed outcomes to implement rules 3 and 4. Apply these rules consistently
# for all 1000 rounds.

class Cooperative_13(LLM_Strategy):
  n = 13
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._memory = []
          return axl.Action.C
  
      # Use the observed actions from the previous round.
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
      observed = (my_last, opp_last)
  
      # Maintain a short memory of the last two observed outcomes.
      if getattr(self, "_memory", None) is None:
          self._memory = []
      self._memory.append(observed)
      if len(self._memory) > 2:
          self._memory = self._memory[-2:]
  
      # Rule 1: (C, C) -> cooperate
      if observed == (axl.Action.C, axl.Action.C):
          return axl.Action.C
  
      # Rule 2: (C, D) -> defect
      if observed == (axl.Action.C, axl.Action.D):
          return axl.Action.D
  
      # Rule 3: (D, C)
      if observed == (axl.Action.D, axl.Action.C):
          # Defect only if opponent has appeared to defect in at least one of
          # the two rounds before the previous round.
          if len(opponent.history) >= 3:
              prior_two_opp = opponent.history[-3:-1]
              if axl.Action.D in prior_two_opp:
                  return axl.Action.D
          return axl.Action.C
  
      # Rule 4: (D, D)
      if observed == (axl.Action.D, axl.Action.D):
          # Cooperate only if the round before the previous one showed (C, C) or (C, D).
          if len(self._memory) >= 2:
              prev_observed = self._memory[-2]
              if prev_observed in ((axl.Action.C, axl.Action.C), (axl.Action.C, axl.Action.D)):
                  return axl.Action.C
          return axl.Action.D
  
      # Fallback (should not be reached)
      return axl.Action.C



# Play as follows:  1. Cooperate in the first round.   2. For each subsequent
# round, consider the opponent’s last **two** observed actions.   3. If **both**
# of the opponent’s last two observed actions were defection, defect.   4. If
# **at least one** of the opponent’s last two observed actions was cooperation,
# cooperate.   5. In rounds 999 and 1000, always defect.    This approach
# tolerates isolated defections (likely due to noise), avoids retaliation
# spirals, maintains cooperation after occasional errors, and accounts for
# endgame incentives in the final two rounds.

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
  
      round_number = len(self.history) + 1
  
      if round_number in (999, 1000):
          return axl.Action.D
  
      last_two = opponent.history[-2:]
      if len(last_two) < 2:
          return axl.Action.C
  
      if last_two.count(axl.Action.D) == 2:
          return axl.Action.D
      return axl.Action.C



# Start by playing Cooperate (C) in the first round.    Thereafter, in each
# round:    1. If your opponent’s observed action in the previous round was
# Cooperate, play Cooperate.   2. If your opponent’s observed action in the
# previous round was Defect, play Defect—unless you have defected in the last
# two consecutive rounds and your opponent’s action before that was Cooperate;
# in that case, play Cooperate to test for recovery from noise.    In other
# words: cooperate by default, mirror your opponent’s last observed move, but
# forgive a single Defect after a short string of mutual Defects if cooperation
# was recently established.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._recover_test_pending = False
          return axl.Action.C
  
      last_opp = opponent.history[-1]
      last_self = self.history[-1]
  
      if last_opp == axl.Action.C:
          self._recover_test_pending = False
          return axl.Action.C
  
      # Opponent defected last round.
      if len(self.history) >= 3:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.C
          ):
              self._recover_test_pending = True
              return axl.Action.C
  
      self._recover_test_pending = False
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.  From the second round
# onward, follow these rules based on the *observed* actions from the previous
# round:  1. **If the previous round appeared to be mutual cooperation (C,C):**
# Play C.  2. **If you appeared to play C and your opponent appeared to play
# D:**      - Check the two rounds before that (if they exist).      - If your
# opponent appeared to cooperate in at least one of those two rounds, assume the
# current D might be due to noise, and play C.      - Otherwise (opponent
# appeared to defect in both prior rounds), play D.  3. **If you appeared to
# play D and your opponent appeared to play C:** Play C.  4. **If the previous
# round appeared to be mutual defection (D,D):**      - Play C, but only if your
# opponent has appeared to cooperate in at least one of the last three rounds.
# - If your opponent has appeared to defect in all of the last three rounds
# (including the most recent), play D.  This approach uses a short memory window
# (up to three prior rounds) to distinguish between noise and persistent
# defection, forgives isolated or rare defections, retaliates against sustained
# exploitation, and maintains cooperation when mutual intent is likely.

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
  
      my_hist = self.history
      opp_hist = opponent.history
      last_my = my_hist[-1]
      last_opp = opp_hist[-1]
  
      # Rule 1: mutual cooperation
      if last_my == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
  
      # Rule 2: I appeared to cooperate, opponent appeared to defect
      if last_my == axl.Action.C and last_opp == axl.Action.D:
          prior_opp = opp_hist[-3:-1]  # up to two rounds before the last one
          if axl.Action.C in prior_opp:
              return axl.Action.C
          return axl.Action.D
  
      # Rule 3: I appeared to defect, opponent appeared to cooperate
      if last_my == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.C
  
      # Rule 4: mutual defection
      if last_my == axl.Action.D and last_opp == axl.Action.D:
          last_three_opp = opp_hist[-3:]
          if axl.Action.C in last_three_opp:
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.C



# Start by intending to cooperate in the first round. From round 2 onward, base
# your decision on the **observed actions from the previous round**, but
# interpret them with awareness of possible noise, using the following rules in
# order:  1. If the previous round showed (C, C), intend to cooperate.   2. If
# the previous round showed (D, D), intend to cooperate.   3. If the previous
# round showed (C, D) or (D, C), intend to cooperate—treat any single mismatch
# as likely due to noise and seek to restore cooperation.  In all cases, your
# chosen action is subject to the 10% noise (as per the game rules), but your
# intention follows the above. Never defect intentionally; always intend to
# cooperate regardless of history.

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
  
      return axl.Action.C



# Start by playing Defect (D) in the first round. After that, follow these rules
# in order each round:  1. If your opponent played Defect (D) in the previous
# round, play Defect (D).   2. If your opponent played Cooperate (C) in the
# previous round, play Defect (D) — but only if you have defected in at least
# two of the last three rounds.   3. Otherwise, play Cooperate (C) to test for
# mutual cooperation.  However, if you have observed your opponent defect in 3
# or more of the last 5 rounds, revert to playing Defect (D) for the rest of the
# game.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forced_defect = False
          return axl.Action.D
  
      if self._forced_defect:
          return axl.Action.D
  
      if len(opponent.history) >= 5 and opponent.history[-5:].count(axl.Action.D) >= 3:
          self._forced_defect = True
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if len(self.history) >= 3 and self.history[-3:].count(axl.Action.D) >= 2:
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the first round.  Thereafter, in each round, decide
# your action based on the **observed actions from the previous round**, using
# the following rules in order:  1. If the previous round appeared to be mutual
# cooperation (you observed C, opponent observed C), cooperate.   2. If the
# previous round appeared to be mutual defection (you observed D, opponent
# observed D), cooperate.   3. If the actions appeared mismatched (one C and one
# D, in either direction), cooperate—**unless** this is the second consecutive
# round with a mismatch in the same direction (i.e., you observed C while
# opponent observed D in both the previous round and the round before that); in
# that case, defect.  This approach treats mismatches as likely caused by noise
# unless the same pattern repeats, in which case it assumes intentional
# exploitation and responds with defection. It maintains symmetry, forgives
# isolated incidents, and avoids prolonged retaliation while still deterring
# persistent defection.

class Cooperative_15(LLM_Strategy):
  n = 15
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_mismatch_direction = None
          self._consecutive_mismatch_count = 0
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      # Determine whether the previous round was a mismatch and in which direction.
      if my_last == opp_last:
          self._last_mismatch_direction = None
          self._consecutive_mismatch_count = 0
          return axl.Action.C
  
      current_direction = (my_last, opp_last)
  
      if self._last_mismatch_direction == current_direction:
          self._consecutive_mismatch_count += 1
      else:
          self._consecutive_mismatch_count = 1
          self._last_mismatch_direction = current_direction
  
      if self._consecutive_mismatch_count >= 2 and current_direction == (axl.Action.C, axl.Action.D):
          return axl.Action.D
  
      return axl.Action.C



# Play as follows:  1. Cooperate in the first round.   2. From round 2 onward,
# keep track of your opponent’s last two observed actions.   3. If both of the
# opponent’s last two observed actions were defections, defect.   4. If at least
# one of the opponent’s last two observed actions was cooperation, cooperate.
# This approach treats isolated observed defections as likely noise and requires
# consistent defection before responding in kind, reducing the risk of
# retaliation due to action flips while still discouraging sustained
# exploitation.

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
  
      if len(opponent.history) < 2:
          return axl.Action.C
  
      last_two = opponent.history[-2:]
      if last_two.count(axl.Action.D) == 2:
          return axl.Action.D
      return axl.Action.C



# Start by playing C in the first round. In each subsequent round:  1. If your
# opponent’s observed action in the previous round was C, play C.   2. If your
# opponent’s observed action in the previous round was D, play D.    However,
# every 10 rounds (i.e., in rounds 10, 20, 30, …), play C regardless of the
# opponent’s last action to test for and recover cooperation in case noise
# caused a breakdown.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number % 10 == 0:
          return axl.Action.C
  
      last_opponent_action = opponent.history[-1]
      if last_opponent_action == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Start by cooperating in the first round.  Thereafter, base your action on the
# last *two* rounds of observed play, and follow these rules in order:  1. If
# the opponent has appeared to cooperate in both of the last two rounds,
# cooperate.   2. If the opponent appeared to defect in exactly one of the last
# two rounds and you cooperated in both of those rounds, defect (to discourage
# exploitation).   3. If the opponent appeared to defect in both of the last two
# rounds, defect.   4. In all other cases—including when you defected in one of
# the last two rounds or the pattern is ambiguous due to possible
# noise—cooperate.  This approach uses short-term history to filter out isolated
# defections likely caused by noise, retaliates only against consistent or
# exploitative defection, avoids cycles by not overreacting to single incidents,
# and remains forgiving after your own mistakes or unclear signals.

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
  
      if len(self.history) < 2 or len(opponent.history) < 2:
          return axl.Action.C
  
      my_last_two = list(self.history[-2:])
      opp_last_two = list(opponent.history[-2:])
  
      opp_defections = opp_last_two.count(axl.Action.D)
      my_cooperations = my_last_two.count(axl.Action.C)
  
      if opp_defections == 0:
          return axl.Action.C
      if opp_defections == 1 and my_cooperations == 2:
          return axl.Action.D
      if opp_defections == 2:
          return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the first round.  In every subsequent round, base your
# decision on the **last two observed outcomes** to better distinguish noise
# from intentional defection. Specifically:  1. If the opponent appeared to
# cooperate in **both** of the last two rounds, cooperate.   2. If the opponent
# appeared to defect in **both** of the last two rounds, defect.   3. If the
# opponent’s observed actions in the last two rounds are mixed (one C, one D),
# cooperate—treat this as likely due to noise rather than deliberate
# exploitation.   4. If you yourself observed that you defected in the previous
# round (regardless of intent), cooperate in the current round to signal
# willingness to return to cooperation—this helps correct for your own possible
# noise-induced defection.    (When fewer than two prior rounds exist, use only
# the available round(s) and default to cooperation in case of ambiguity.)

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
  
      my_history = self.history
      opp_history = opponent.history
  
      # If we defected in the previous round, try to restore cooperation.
      if len(my_history) >= 1 and my_history[-1] == axl.Action.D:
          return axl.Action.C
  
      # Use the last two observed opponent actions when available.
      if len(opp_history) >= 2:
          last_two = opp_history[-2:]
          if last_two.count(axl.Action.C) == 2:
              return axl.Action.C
          if last_two.count(axl.Action.D) == 2:
              return axl.Action.D
          return axl.Action.C
  
      # With only one prior round, default to cooperation in ambiguity.
      if len(opp_history) == 1:
          return axl.Action.C if opp_history[-1] == axl.Action.C else axl.Action.C
  
      return axl.Action.C



# Start by playing D. After that, follow these rules in order each round:  1. If
# the opponent’s last observed action was D, play D.   2. If the opponent’s last
# observed action was C, play D with 90% probability and C with 10% probability.
# (Interpret “last observed action” as the action the opponent appeared to play
# in the previous round, accounting for the fact that noise may have flipped
# their intended move.)

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
  
      last_opponent_action = opponent.history[-1]
  
      if last_opponent_action == axl.Action.D:
          return axl.Action.D
      else:
          return self._random.random_choice(0.1)



# Start by cooperating in the first round.  In each subsequent round, follow
# these rules in order:  1. If both you and your opponent were observed to
# cooperate in the previous round, cooperate.   2. If you were observed to
# defect but intended to cooperate (i.e., you chose C last round),
# cooperate—this accounts for the possibility your action was flipped by noise.
# 3. If the opponent was observed to defect in the previous round but had
# cooperated in the two rounds before that (i.e., a single isolated observed
# defection after at least two cooperations), assume it may be noise and
# cooperate.   4. If the opponent has been observed to defect in two or more of
# the last three rounds, defect.   5. If you have defected for two consecutive
# rounds and the opponent is observed to cooperate in the most recent round,
# return to cooperation.

class Cooperative_17(LLM_Strategy):
  n = 17
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_choice = axl.Action.C
          return axl.Action.C
  
      # Rule 1: If both were observed to cooperate in the previous round, cooperate.
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          self._last_choice = axl.Action.C
          return axl.Action.C
  
      # Rule 2: If you were observed to defect but intended to cooperate (i.e., chose C last round), cooperate.
      if self._last_choice == axl.Action.C and self.history[-1] == axl.Action.D:
          self._last_choice = axl.Action.C
          return axl.Action.C
  
      # Rule 3: If opponent observed D last round but had cooperated in the two rounds before that,
      # assume it may be noise and cooperate.
      if len(opponent.history) >= 3:
          if (
              opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.C
              and opponent.history[-3] == axl.Action.C
          ):
              self._last_choice = axl.Action.C
              return axl.Action.C
  
      # Rule 4: If opponent has been observed to defect in two or more of the last three rounds, defect.
      if len(opponent.history) >= 3 and opponent.history[-3:].count(axl.Action.D) >= 2:
          self._last_choice = axl.Action.D
          return axl.Action.D
  
      # Rule 5: If you have defected for two consecutive rounds and opponent is observed to cooperate most recently, return to cooperation.
      if len(self.history) >= 2:
          if self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and opponent.history[-1] == axl.Action.C:
              self._last_choice = axl.Action.C
              return axl.Action.C
  
      # Default: cooperate.
      self._last_choice = axl.Action.C
      return axl.Action.C



# Start by cooperating in the first round.  In each subsequent round, base your
# decision on the **sequence of the last three observed outcomes** (your action,
# your opponent’s observed action, and the resulting payoffs), accounting for
# the possibility of noise. Use the following rules in order:  1. **If the
# opponent has been observed to defect in two or more of the last three
# rounds**, defect.   2. **If the last round resulted in mutual defection (both
# scored 1)**, and the same occurred in the round before that, defect.   3. **If
# the last round resulted in you scoring 0 while the opponent scored 5**, and
# this has happened in two of the last three rounds, defect.   4. **If none of
# the above apply**, cooperate.  Treat the opponent’s “observed action” as the
# action that would most likely produce the payoff you received, assuming your
# own intended action was executed correctly (i.e., if you intended C and
# received 0, infer the opponent likely played D; if you intended D and received
# 1, infer the opponent likely played D, etc.). Do not overreact to a single
# suspicious outcome—require a pattern over multiple rounds before defecting.

class Neutral_17(LLM_Strategy):
  n = 17
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_observed_opponent = []
          self._last_mutual_defection = []
          self._last_zero_five = []
          return axl.Action.C
  
      def observed_opponent_action(my_action: axl.Action, my_payoff: int) -> axl.Action:
          if my_action == axl.Action.C:
              return axl.Action.D if my_payoff == 0 else axl.Action.C
          else:
              return axl.Action.D if my_payoff == 1 else axl.Action.C
  
      my_last_action = self.history[-1]
      my_last_payoff, opp_last_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])
      obs_opp_last = observed_opponent_action(my_last_action, my_last_payoff)
  
      self._last_observed_opponent.append(obs_opp_last)
      self._last_mutual_defection.append(my_last_payoff == 1 and opp_last_payoff == 1)
      self._last_zero_five.append(my_last_payoff == 0 and opp_last_payoff == 5)
  
      last_three_obs = self._last_observed_opponent[-3:]
      last_three_mutual = self._last_mutual_defection[-3:]
      last_three_zero_five = self._last_zero_five[-3:]
  
      if last_three_obs.count(axl.Action.D) >= 2:
          return axl.Action.D
  
      if len(last_three_mutual) >= 2 and last_three_mutual[-1] and last_three_mutual[-2]:
          return axl.Action.D
  
      if last_three_zero_five.count(True) >= 2:
          return axl.Action.D
  
      return axl.Action.C



# Start by playing C in the first round. After that, follow these rules in
# order:  1. If your opponent played D in the previous round, play D.   2. If
# your opponent played C in the previous round, play C.    However, to account
# for noise:   - If you observe two Ds in a row from your opponent, continue
# playing D until they play two Cs in a row.   - If you observe two Cs in a row
# from your opponent, return to playing C.    This implements a "Tit-for-Tat
# with noise forgiveness" approach: it retaliates against apparent defection but
# requires consistent signals before switching actions, reducing the risk of
# getting locked into mutual defection due to occasional action flips.

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._noise_forgiveness_state = "C"
          return axl.Action.C
  
      opp_last = opponent.history[-1]
      opp_last_two = opponent.history[-2:] if len(opponent.history) >= 2 else opponent.history
  
      if len(opp_last_two) == 2 and opp_last_two.count(axl.Action.D) == 2:
          self._noise_forgiveness_state = "D"
      elif len(opp_last_two) == 2 and opp_last_two.count(axl.Action.C) == 2:
          self._noise_forgiveness_state = "C"
      else:
          if opp_last == axl.Action.D:
              self._noise_forgiveness_state = "D"
          elif opp_last == axl.Action.C:
              self._noise_forgiveness_state = "C"
  
      return axl.Action.C if self._noise_forgiveness_state == "C" else axl.Action.D



# Start by cooperating in the first round.  From the second round onward, decide
# your action based on the opponent’s last two observed actions, using the
# following rules in order:  1. If the opponent was observed to cooperate in
# both of the last two rounds, cooperate.   2. If the opponent was observed to
# defect in both of the last two rounds, defect.   3. If the opponent’s observed
# actions in the last two rounds are mixed (one C and one D, in either order),
# then:      - If you cooperated in the previous round, cooperate.      - If you
# defected in the previous round, defect.    (For rounds 2 only, treat the “two
# rounds ago” observation as a cooperation to allow the rules to apply.)  This
# approach uses a two-round memory to filter out isolated noisy defections while
# still responding to sustained defection, and it avoids oscillations by tying
# the response in ambiguous cases to your own previous action.

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
  
      if len(opponent.history) == 1:
          last_two = [axl.Action.C, opponent.history[-1]]
      else:
          last_two = list(opponent.history[-2:])
  
      if last_two[0] == axl.Action.C and last_two[1] == axl.Action.C:
          return axl.Action.C
  
      if last_two[0] == axl.Action.D and last_two[1] == axl.Action.D:
          return axl.Action.D
  
      return self.history[-1] if len(self.history) > 0 else axl.Action.C



# Start by playing C in the first round.    In every subsequent round:    1. If
# your opponent’s last observed action was C, play C.   2. If your opponent’s
# last observed action was D, look at their action from two rounds ago:      -
# If that earlier action was C, assume the D was likely due to noise and play C.
# - If that earlier action was also D, play D.    (That is, only defect after
# observing two consecutive Ds from your opponent; otherwise, cooperate.)

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
  
      if len(opponent.history) < 2:
          return axl.Action.C
  
      last = opponent.history[-1]
      two_ago = opponent.history[-2]
  
      if last == axl.Action.C:
          return axl.Action.C
  
      if last == axl.Action.D:
          if two_ago == axl.Action.C:
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.C



# Start by playing Cooperate (C) in the first round. After that, follow these
# rules in order:  1. If your opponent’s last observed action was Cooperate,
# play Cooperate.   2. If your opponent’s last observed action was Defect, play
# Defect—unless you have defected in the last two rounds; in that case, play
# Cooperate to attempt to restore cooperation.    This approach encourages
# mutual cooperation for higher long-term payoff, retaliates against apparent
# defection to discourage exploitation, and includes a built-in forgiveness
# mechanism every two rounds of mutual defection to recover from noise-induced
# misunderstandings.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defected_last_two = False
          return axl.Action.C
  
      if len(self.history) >= 2:
          self._defected_last_two = (
              self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D
          )
      else:
          self._defected_last_two = False
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          if self._defected_last_two:
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.C



# Start by intending to cooperate in the first round.  In each subsequent round,
# decide your intended action based on the previous round’s **intended** action
# (yours) and the **observed** action of your opponent, while accounting for the
# 10% noise:  1. **If you intended to cooperate last round** and your opponent
# **appeared to cooperate**, intend to cooperate.   2. **If you intended to
# cooperate last round** and your opponent **appeared to defect**, intend to
# defect **once**, then return to cooperation regardless of the next observation
# (i.e., punish for one round only).   3. **If you intended to defect last
# round** (e.g., as part of a punishment) and your opponent **appeared to
# cooperate**, intend to cooperate.   4. **If you intended to defect last
# round** and your opponent **appeared to defect**, intend to cooperate.  This
# approach limits retaliation to a single round to avoid prolonged conflict due
# to noise, resumes cooperation quickly after punishment or mutual defection,
# and bases decisions on your own intended action to correctly interpret
# mismatches.

class Cooperative_19(LLM_Strategy):
  n = 19
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      last_intended = getattr(self, "_intended_action", axl.Action.C)
      opponent_last = opponent.history[-1]
  
      if last_intended == axl.Action.C:
          if opponent_last == axl.Action.C:
              self._intended_action = axl.Action.C
          else:
              self._intended_action = axl.Action.D
      else:
          self._intended_action = axl.Action.C
  
      return self._intended_action



# Play Cooperate (C) in the first round. In every subsequent round, base your
# action on the *observed* (i.e., possibly noisy) outcome of the previous round
# as follows:  1. If both you and your opponent appeared to play C in the
# previous round, play C.   2. If you appeared to play C and your opponent
# appeared to play D, play D **only if** this is the first such incident in a
# row; if the same pattern (you C, opponent D) occurred in the *two* immediately
# preceding rounds, continue playing D.   3. If you appeared to play D and your
# opponent appeared to play C, play C.   4. If both you and your opponent
# appeared to play D, play C—**unless** the previous round was already a mutual
# D following a prior (you C, opponent D) incident, in which case play D one
# more time before returning to C.  In all cases, after at most two consecutive
# D plays by you (whether retaliatory or in mutual D), return to C. This allows
# for limited retaliation to discourage exploitation while forgiving quickly to
# avoid prolonged conflict due to noise.

class Neutral_19(LLM_Strategy):
  n = 19
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._retaliation_streak = 0
          self._last_pattern_cd = 0
          self._last_pattern_dd = 0
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      # Track observed patterns from the previous round.
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          self._retaliation_streak = 0
          self._last_pattern_cd = 0
          self._last_pattern_dd = 0
          return axl.Action.C
  
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          self._last_pattern_dd = 0
          self._last_pattern_cd += 1
          if self._last_pattern_cd >= 2:
              self._retaliation_streak = 2
              return axl.Action.D
          self._retaliation_streak = 1
          return axl.Action.D
  
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          self._last_pattern_cd = 0
          self._last_pattern_dd = 0
          self._retaliation_streak = 0
          return axl.Action.C
  
      # Mutual D observed.
      self._last_pattern_cd = 0
      self._last_pattern_dd += 1
  
      if self._retaliation_streak >= 2:
          self._retaliation_streak = 0
          return axl.Action.C
  
      if self._last_pattern_dd >= 2:
          self._retaliation_streak = 2
          return axl.Action.D
  
      self._retaliation_streak = 0
      return axl.Action.C



# Start by cooperating in the first round.    In each subsequent round, decide
# your action based on your opponent’s observed action in the previous round,
# but account for the possibility of noise:  1. If your opponent’s observed
# action in the previous round was C, cooperate.   2. If your opponent’s
# observed action in the previous round was D, defect—unless you have observed
# cooperation from them in at least two of the last three rounds (including the
# most recent one). In that case, cooperate instead.    Continue applying these
# rules for all 1000 rounds.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._coop_streak = 0
          return axl.Action.C
  
      last_opp = opponent.history[-1]
  
      recent_coops = 0
      for move in opponent.history[-3:]:
          if move == axl.Action.C:
              recent_coops += 1
  
      if last_opp == axl.Action.C:
          return axl.Action.C
  
      if recent_coops >= 2:
          return axl.Action.C
  
      return axl.Action.D



# Start by intending to cooperate in the first round. In every subsequent round,
# decide your action based only on your own intended action and the observed
# outcome (your own payoff) from the previous round, using the following rules
# in order:  1. If your payoff in the previous round was 3, cooperate.   2. If
# your payoff in the previous round was 1, cooperate.   3. If your payoff in the
# previous round was 0, defect.   4. If your payoff in the previous round was 5,
# cooperate.    Continue applying these rules for all 1000 rounds.

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
          return self._intended_action
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]) if False else None
      # Compute previous-round payoff from the last interaction only
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if my_last_score in (3, 1, 5):
          self._intended_action = axl.Action.C
      elif my_last_score == 0:
          self._intended_action = axl.Action.D
      else:
          self._intended_action = axl.Action.C
  
      return self._intended_action



# Start by cooperating in the first round. For each subsequent round, base your
# action on the **observed** actions from the previous round, but apply the
# following rules in order:  1. If the previous round appeared as (C, C),
# cooperate.   2. If it appeared as (C, D), defect.   3. If it appeared as (D,
# C), cooperate.   4. If it appeared as (D, D), cooperate with 70% probability
# and defect with 30% probability.    This introduces measured forgiveness after
# mutual observed defection to reduce exploitation while accounting for the
# possibility that noise—not intentional defection—caused the outcome. The
# strategy remains reactive to the last observed move but tempers responses to
# ambiguous signals caused by noise.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return self._random.random_choice(0.7)
  
      return axl.Action.C



# Start by playing Cooperate (C) in the first round. After that, follow these
# rules in order for each subsequent round:  1. If the opponent’s last observed
# action was Defect (D), play Defect (D).   2. If the opponent’s last observed
# action was Cooperate (C), play Cooperate (C)—but only if you have observed at
# least two Cooperate actions from the opponent in the last three rounds.   3.
# Otherwise, play Defect (D).  This approach begins cooperatively to invite
# mutual cooperation, retaliates promptly against apparent defection to
# discourage exploitation, but requires consistent evidence of cooperation
# before trusting again—helping guard against noise-induced errors.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          recent_opponent = opponent.history[-3:]
          if recent_opponent.count(axl.Action.C) >= 2:
              return axl.Action.C
  
      return axl.Action.D



# Start by cooperating in the first round.  From round 2 onward, decide your
# action based on the last two rounds of your opponent’s *observed* actions
# (i.e., what actually occurred, including possible noise):  1. If your opponent
# appeared to cooperate in both of the last two rounds, cooperate.   2. If your
# opponent appeared to defect in both of the last two rounds, defect.   3. If
# the opponent’s observed actions in the last two rounds are mixed (one C and
# one D, in any order), cooperate.  Apply this rule for all remaining rounds up
# to 1000.

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
  
      if len(opponent.history) < 2:
          return axl.Action.C
  
      last_two = opponent.history[-2:]
      if last_two.count(axl.Action.C) == 2:
          return axl.Action.C
      if last_two.count(axl.Action.D) == 2:
          return axl.Action.D
      return axl.Action.C



# Start by playing C in the first round.  In every subsequent round, decide your
# action based on the last observed outcome (your payoff and your opponent’s
# payoff), but interpret it cautiously due to possible noise:  1. If both
# players received 3 (mutual cooperation payoff), play C.   2. If both players
# received 1 (mutual defection payoff), play C—assume noise may have disrupted
# cooperation.   3. If you received 5 and your opponent received 0 (you
# exploited them), play C—assume they likely intended to cooperate.   4. If you
# received 0 and your opponent received 5 (they exploited you), play C
# anyway—assume this may have resulted from your own action being flipped (you
# intended C but were seen as D), or their action being flipped (they intended C
# but were seen as D), so do not punish unilaterally.  Continue cooperating
# unless there is strong, repeated evidence of intentional defection (e.g.,
# multiple exploitative outcomes in a short span). In this basic version, always
# play C regardless of history—because under 10% noise, any single adverse
# outcome is more likely due to error than deliberate defection, and sustained
# cooperation maximizes expected payoff against most reasonable opponents.

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
  
      return axl.Action.C



# Start by playing C in the first round. After that, follow these rules in
# order:  1. If it is the last 10 rounds (round 991 or later), play D.   2. If
# your opponent’s last observed action was D and the round number is 2 or
# higher, play D.   3. Otherwise, play C.    However, to handle noise: if you
# have played C for the last 3 rounds and your opponent’s observed actions in
# those same rounds were all D, then assume mutual cooperation may have been
# disrupted by noise—play C once more to test for recovery; if the opponent
# plays C (observed) in response, return to rule 3, otherwise continue with rule
# 2.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._test_recovery = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if getattr(self, "_test_recovery", False):
          if opponent.history and opponent.history[-1] == axl.Action.C:
              self._test_recovery = False
              return axl.Action.C
          return axl.Action.D
  
      if len(self.history) >= 3:
          if (
              self.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]
              and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
          ):
              self._test_recovery = True
              return axl.Action.C
  
      if round_number >= 2 and opponent.history and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Play Cooperate (C) in the first round.  In each subsequent round, decide your
# action based on the last three observed outcomes (your action and your
# opponent’s action as they appeared after noise). Follow these rules in order:
# 1. **If the game is in the last 10 rounds (round 991 or later)**: always play
# Defect (D).  2. **If your opponent has been observed to play D in two or more
# of the last three rounds**: play D.  3. **If your opponent has been observed
# to play C in all of the last three rounds**: play C.  4. **If your opponent’s
# observed actions in the last three rounds contain exactly one D**:    - Play C
# **unless** you yourself played D in the round immediately before that observed
# D (suggesting your noisy D may have provoked a retaliatory D, which you should
# not punish further).    - In all other cases with a single observed D, play C
# (treat it as likely noise).  5. **If mutual D has persisted for five
# consecutive rounds**, attempt to restore cooperation by playing C once; if the
# opponent responds with C (observed), return to rule 3; if they respond with D,
# revert to rule 2.  Apply these rules for all rounds, using only observed
# (noisy) actions from past rounds—never assumed intentions.

class Cooperative_22(LLM_Strategy):
  n = 22
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._restore_attempt = False
          self._restore_pending = False
          self._restore_mode = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      # Last 10 rounds: always defect.
      if round_number >= 991:
          return axl.Action.D
  
      my_hist = list(self.history)
      opp_hist = list(opponent.history)
  
      # If we previously attempted restoration and observed the opponent cooperate,
      # return to cooperative mode.
      if self._restore_pending:
          self._restore_pending = False
          if opp_hist and opp_hist[-1] == axl.Action.C:
              self._restore_mode = False
              return axl.Action.C
          self._restore_mode = False
          return axl.Action.D
  
      # Mutual D persisted for five consecutive rounds: attempt to restore cooperation once.
      if len(my_hist) >= 5 and len(opp_hist) >= 5:
          if all(m == axl.Action.D and o == axl.Action.D for m, o in zip(my_hist[-5:], opp_hist[-5:])):
              self._restore_pending = True
              self._restore_mode = True
              return axl.Action.C
  
      # If in restore mode, cooperate unless the opponent just defected.
      if self._restore_mode:
          if opp_hist and opp_hist[-1] == axl.Action.C:
              return axl.Action.C
          return axl.Action.D
  
      last3_opp = opp_hist[-3:]
      last3_my = my_hist[-3:]
  
      # Rule 2: opponent defected in two or more of the last three rounds.
      if last3_opp.count(axl.Action.D) >= 2:
          return axl.Action.D
  
      # Rule 3: opponent cooperated in all of the last three rounds.
      if len(last3_opp) == 3 and last3_opp.count(axl.Action.C) == 3:
          return axl.Action.C
  
      # Rule 4: exactly one observed D in the last three rounds.
      if last3_opp.count(axl.Action.D) == 1:
          d_index = last3_opp.index(axl.Action.D)
          if len(last3_my) == 3 and d_index > 0 and last3_my[d_index - 1] == axl.Action.D:
              return axl.Action.D
          return axl.Action.C
  
      # Default: cooperate.
      return axl.Action.C



# Start by cooperating in the first round.  In every subsequent round, follow
# these rules in order:  1. If your opponent’s last two observed actions were
# both cooperation, cooperate.   2. If your opponent’s last two observed actions
# were both defection, defect.   3. If the last two observed actions are mixed
# (one C and one D, in any order), cooperate.    This approach treats isolated
# defections as likely noise, requires consistent signals before changing
# behavior, and allows recovery toward cooperation after disagreement.

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
  
      if len(opponent.history) >= 2:
          last_two = opponent.history[-2:]
          if last_two[0] == axl.Action.C and last_two[1] == axl.Action.C:
              return axl.Action.C
          if last_two[0] == axl.Action.D and last_two[1] == axl.Action.D:
              return axl.Action.D
          return axl.Action.C
  
      return axl.Action.C



# Start by playing Cooperate (C) in the first round. After that, follow these
# rules in order:  1. If it is one of the last 10 rounds (round 991 or later),
# play Defect (D).   2. If your opponent’s observed action in the previous round
# was Defect (D), play Defect (D).   3. If your opponent’s observed action in
# the previous round was Cooperate (C), play Cooperate (C).    This is a “Tit-
# for-Tat with endgame defection” strategy, designed to encourage mutual
# cooperation early on while accounting for the 10% noise by responding only to
# the most recent observed move and avoiding overly punitive reactions. The
# final 10 rounds are played as Defect to prevent exploitation when future
# retaliation is no longer possible.

class Aggressive_23(LLM_Strategy):
  n = 23
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
  
      return opponent.history[-1]



# Start by cooperating in the first round.  In every subsequent round:  1. If
# the opponent’s observed action in the previous round was cooperation,
# cooperate.   2. If the opponent’s observed action in the previous round was
# defection, defect—but only if the opponent also defected in the round before
# that.   3. If the opponent defected in the previous round but cooperated in
# the round before that (i.e., a single isolated defection), cooperate.   4. If
# you and your opponent have both defected for five consecutive rounds,
# cooperate in the next round to attempt to restore mutual cooperation.

class Cooperative_23(LLM_Strategy):
  n = 23
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._restore_after_five_dd = False
          return axl.Action.C
  
      # If we previously observed five consecutive mutual defections, try to restore cooperation.
      if getattr(self, "_restore_after_five_dd", False):
          self._restore_after_five_dd = False
          return axl.Action.C
  
      # Check for five consecutive rounds of mutual defection in the observed history.
      if len(self.history) >= 5:
          last_five_self = self.history[-5:]
          last_five_opp = opponent.history[-5:]
          if (
              last_five_self.count(axl.Action.D) == 5
              and last_five_opp.count(axl.Action.D) == 5
          ):
              self._restore_after_five_dd = True
              return axl.Action.C
  
      # Standard rule based on opponent's previous actions.
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Opponent defected last round.
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      # Single isolated defection: cooperate.
      return axl.Action.C



# Play Cooperate (C) in the first round. From round 2 onward, base your action
# on the last two rounds of observed outcomes to reduce misinterpretation from
# noise:  1. If the opponent appeared to play C in both of the last two rounds,
# play C.   2. If the opponent appeared to play D in both of the last two
# rounds, play D.   3. If the opponent’s observed actions in the last two rounds
# are mixed (one C and one D, in any order), play C.  This approach treats
# isolated apparent defections as likely due to noise and continues cooperating,
# but responds to consistent defection as intentional and switches to defection.
# It avoids reacting to single-round outcomes, which are unreliable under 10%
# noise, and favors cooperation unless there is clear recent evidence of
# sustained defection.

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
  
      if len(opponent.history) < 2:
          return axl.Action.C
  
      last_two = opponent.history[-2:]
  
      if last_two.count(axl.Action.C) == 2:
          return axl.Action.C
      if last_two.count(axl.Action.D) == 2:
          return axl.Action.D
      return axl.Action.C



# Start by playing Defect (D) in the first round.    After that, in each
# subsequent round:    1. If the opponent’s last observed action was Defect (D),
# play Defect (D).   2. If the opponent’s last observed action was Cooperate
# (C), play Defect (D) — but only if you have observed the opponent play C in
# **at least two of the last three rounds**. Otherwise, continue to play Defect
# (D).    In all cases, never play Cooperate (C). Always play Defect (D),
# regardless of history or payoff, because the risk of noise-induced
# exploitation outweighs any potential gain from cooperation, and consistent
# defection maximizes payoff against both cooperative and defective opponents in
# this noisy environment.

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
  
      return axl.Action.D



# Start by playing Cooperate (C) in the first round.  Thereafter, base your
# action on the last two observed rounds of play, and follow these rules in
# order:  1. If the opponent has played C in both of the last two observed
# rounds, play C.   2. If the opponent has played D in both of the last two
# observed rounds, play D.   3. If the opponent’s last two observed actions are
# mixed (one C and one D, in any order), play C—this treats isolated Ds as
# likely noise and favors forgiveness.    Additionally, if you ever observe two
# consecutive rounds of mutual D (both players appeared to play D in two rounds
# in a row), play C in the next round to actively attempt to restore
# cooperation.  Do not use fixed resets (e.g., every 10 rounds); instead, rely
# on the two-round memory and the explicit recovery rule after mutual D streaks
# to handle noise and maintain cooperation.

class Cooperative_24(LLM_Strategy):
  n = 24
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mutual_d_streak = 0
          return axl.Action.C
  
      if len(self.history) < 2 or len(opponent.history) < 2:
          return axl.Action.C
  
      last_two_self = self.history[-2:]
      last_two_opp = opponent.history[-2:]
  
      if last_two_self == [axl.Action.D, axl.Action.D] and last_two_opp == [axl.Action.D, axl.Action.D]:
          self._mutual_d_streak = getattr(self, "_mutual_d_streak", 0) + 1
      else:
          self._mutual_d_streak = 0
  
      if self._mutual_d_streak >= 2:
          self._mutual_d_streak = 0
          return axl.Action.C
  
      if last_two_opp[0] == axl.Action.C and last_two_opp[1] == axl.Action.C:
          return axl.Action.C
      if last_two_opp[0] == axl.Action.D and last_two_opp[1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C



# Play Cooperate (C) in the first round. In each subsequent round, base your
# action on the last two observed outcomes to reduce sensitivity to noise:  1.
# If the last two observed outcomes were both C–C, play C.   2. If the last two
# observed outcomes include at least one C–D (you appeared to cooperate,
# opponent appeared to defect), play D.   3. If the last two observed outcomes
# include at least one D–C (you appeared to defect, opponent appeared to
# cooperate), play C.   4. If the last two observed outcomes are D–D and D–D,
# play D.   5. If the last two observed outcomes are D–D followed by anything
# other than D–D (e.g., D–D then C–C, D–C, or C–D), play C.  This approach uses
# a two-round memory to smooth out isolated errors caused by noise, avoids
# overreacting to single suspicious outcomes, and only defects persistently when
# mutual defection is repeated, suggesting intentional rather than accidental
# behavior.

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
  
      if len(self.history) < 2 or len(opponent.history) < 2:
          last_self = self.history[-1]
          last_opp = opponent.history[-1]
          if last_self == axl.Action.C and last_opp == axl.Action.C:
              return axl.Action.C
          if last_self == axl.Action.C and last_opp == axl.Action.D:
              return axl.Action.D
          if last_self == axl.Action.D and last_opp == axl.Action.C:
              return axl.Action.C
          return axl.Action.D
  
      def outcome(i: int):
          return (self.history[i], opponent.history[i])
  
      last_two = [outcome(-2), outcome(-1)]
  
      if last_two[0] == (axl.Action.C, axl.Action.C) and last_two[1] == (axl.Action.C, axl.Action.C):
          return axl.Action.C
  
      if (axl.Action.C, axl.Action.D) in last_two:
          return axl.Action.D
  
      if (axl.Action.D, axl.Action.C) in last_two:
          return axl.Action.C
  
      if last_two[0] == (axl.Action.D, axl.Action.D) and last_two[1] == (axl.Action.D, axl.Action.D):
          return axl.Action.D
  
      if last_two[0] == (axl.Action.D, axl.Action.D) and last_two[1] != (axl.Action.D, axl.Action.D):
          return axl.Action.C
  
      return axl.Action.C



# Start by playing C in the first round.    Thereafter, in each round:    1. If
# your opponent played C in the previous round (as observed, despite possible
# noise), play C.   2. If your opponent played D in the previous round, play D.
# However, to mitigate the effects of noise:    3. If you have played D for five
# consecutive rounds and your opponent played C in the most recent round, switch
# back to C.    This strategy promotes cooperation when the opponent appears
# cooperative, retaliates against defection to discourage exploitation, and
# includes a forgiveness mechanism to recover from mutual defection caused by
# noise.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._consecutive_d = 0
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D:
          self._consecutive_d += 1
      else:
          self._consecutive_d = 0
  
      if self._consecutive_d >= 5 and opponent.history[-1] == axl.Action.C:
          self._consecutive_d = 0
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D



# Start by playing Cooperate (C) in the first round. After that, follow these
# rules in order:  1. If it is the last 2 rounds (rounds 999–1000), always play
# Defect (D).   2. If your opponent’s observed action in the previous round was
# Defect (D), but their observed action two rounds ago was Cooperate (C), assume
# the Defect may have been due to noise and still play Cooperate (C).   3. If
# your opponent’s observed actions in both the previous round and the round
# before that were Defect (D), play Defect (D).   4. Otherwise (i.e., if the
# opponent’s previous observed action was Cooperate), play Cooperate (C).

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
  
      round_number = len(self.history) + 1
  
      if round_number >= 999:
          return axl.Action.D
  
      if len(opponent.history) >= 2:
          prev = opponent.history[-1]
          prev2 = opponent.history[-2]
  
          if prev == axl.Action.D and prev2 == axl.Action.C:
              return axl.Action.C
  
          if prev == axl.Action.D and prev2 == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C



# Start by cooperating in the first round.  From round 2 onward, decide your
# action based on the last observed move of your opponent, but incorporate
# forgiveness to handle noise:  - If your opponent’s last observed action was
# cooperation, cooperate. - If your opponent’s last observed action was
# defection, defect—unless both players’ last observed actions were defection.
# In the special case where both players’ last observed actions were defection:
# - Cooperate with 20% probability (to counteract the 10% noise and help restore
# cooperation), and defect otherwise.  This rule applies regardless of your own
# intended action in the previous round; only the last observed pair of actions
# matters.

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
  
      if last_opp == axl.Action.C:
          return axl.Action.C
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return self._random.random_choice(0.2)
  
      return axl.Action.D