import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy

# To maximise impact while managing risk, adopt a **“Steadfast Reciprocity”**
# strategy. This is a straightforward, aggressive plan that pushes for high-
# investment collaboration but protects your NGO from being drained by a non-
# contributing partner.  ### The Strategy  1. **Day 1 – Lead with commitment:**
# Always start the project by **investing heavily**. This immediately signals
# your intent to drive significant progress and challenges the corporation to
# match your contribution.  2. **Daily rule thereafter – Mirror with a
# restart:**      On each subsequent day, observe the corporation’s action from
# the previous day:      - If the corporation **invested heavily**: **invest
# heavily** again (maintain momentum).      - If the corporation **conserved**
# resources:        - If *you* had also conserved the previous day (mutual
# inaction): **invest heavily** today. This automatically breaks deadlocks and
# aggressively re-engages the corporation after a lull, preventing temporary
# glitches from permanently stalling the project.        - If *you* invested
# while they conserved (they exploited you): **conserve resources** today as a
# defensive warning shot. However, do not hold a grudge—return to Step 1 (invest
# heavily) the very next day to give them an immediate chance to re-cooperate.
# 3. **Longer-term safeguard:**      Keep a simple mental tally. If the
# corporation **conserves while you invest three times within any rolling five-
# day window** (excluding days where errors are obvious), switch to **permanent
# conservation** for the remainder of the partnership. This ensures you do not
# endlessly subsidise a free-rider.  ### Why This Is Aggressive Yet Practical  -
# **Relentless positivity:** The strategy continually restarts cooperation after
# every mutual-conserve or after a single punishment day. It refuses to let the
# project idle at “minimal progress.” - **Self-protection:** A brief, targeted
# conserves-only-when-exploited response prevents the NGO from being bled dry,
# while the longer-term threshold guards against a perpetually uncooperative
# partner. - **Error tolerance:** By automatically re-investing after mutual
# conservation, one-off administrative errors or technical glitches are forgiven
# instantly, avoiding a costly downward spiral.  This approach balances the
# NGO’s ideal outcome (free-riding on corporate investment) with the realistic
# need to achieve sustained mutual investment—ultimately pushing the project
# forward aggressively without sacrificing financial sustainability.

# In this iterated game, "Cooperate" (C) means investing heavily, and "Defect"
# (D) means conserving resources. There is a 10% independent chance each round
# that either player's intended action is flipped to the opposite. The strategy
# uses only the observed actions (the outcomes after any flips) to decide.  ---
# **Round 1:**   Play C.  **Rounds 2 through 1000:**   Before choosing your
# action, check whether the **permanent defection trigger** has been met. Look
# at every block of 5 consecutive rounds that has been completed so far. If in
# any such block there are **3 or more rounds where you played C and your
# opponent played D**, then you must play D for the current round and all
# remaining rounds, ignoring the rules below.  If the permanent defection
# trigger has **not** been met, determine your action using only the observed
# actions from the immediately previous round:  - If the opponent played **C**
# last round: play **C**. - If the opponent played **D** last round:   - If
# **you** played **D** last round: play **C**.   - If **you** played **C** last
# round: play **D**.  (Note: The single round of playing D after being exploited
# is automatically followed by a return to C the next round, because either the
# opponent will have played C—triggering the first condition—or both will have
# played D—triggering the first sub-case under opponent D.)

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._permanent_defect = False
          return axl.Action.C
  
      if getattr(self, "_permanent_defect", False):
          return axl.Action.D
  
      def trigger_met() -> bool:
          my_hist = list(self.history)
          opp_hist = list(opponent.history)
          n = len(my_hist)
          if n < 5:
              return False
          for start in range(n - 4):
              c_d_count = 0
              for i in range(start, start + 5):
                  if my_hist[i] == axl.Action.C and opp_hist[i] == axl.Action.D:
                      c_d_count += 1
                      if c_d_count >= 3:
                          return True
          return False
  
      if trigger_met():
          self._permanent_defect = True
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.D:
          return axl.Action.C
      return axl.Action.D

# As your country’s diplomat, my high-level strategy is to pursue a **Tit-for-
# Tat with Occasional Forgiveness** approach, while proactively building a
# reputation for cooperative intent.  Here is the straightforward, cooperative
# strategy:  ### 1. Lead with Cooperation **Start the first round by offering a
# free trade agreement.** This signals goodwill and establishes a cooperative
# baseline. It tests whether your counterpart is willing to reciprocate or
# exploit you immediately.  ### 2. Mirror, But with a Delayed Punishment **In
# subsequent rounds, do exactly what the counterpart did in the previous
# round.** If they offered free trade, you offer free trade. If they imposed
# protectionism, you respond with protectionism in the next round. This creates
# a clear, predictable pattern: cooperation is rewarded, and exploitation is
# punished.  ### 3. Implement a “Forgiveness Round” After Locked Conflict **If
# the negotiations fall into a spiral of mutual protectionism (the second-worst
# outcome) for two consecutive rounds, proactively offer free trade on the third
# round.** This is your “forgiveness move.” It acts as a circuit breaker to test
# if a miscommunication or bureaucratic error caused the spiral, rather than
# genuine hostile intent. It prevents you from getting permanently locked into
# the worst collective outcome.  ### 4. Handle Miscommunications (The Core Rule)
# Given the risk of misinterpretation or incorrect implementation, **do not
# overreact to a single round of perceived protectionism.**  - If you offered
# free trade but the outcome was a protectionist clash, assume it could be an
# error first. Your mirroring rule will still have you offer protectionism next
# round (to avoid being exploited), but the forgiveness rule will quickly pull
# you back to cooperation if the conflict persists. - Crucially, **never be the
# first to defect twice in a row after a cooperative round,** as this can turn a
# simple error into a permanent trade war.  ### Summary of the Decision Logic: -
# **Round 1:** Offer Free Trade. - **Every Round After:**      - Look at the
# counterpart’s last *implemented* policy.     - If it was Free Trade → Offer
# Free Trade.     - If it was Protectionist → Offer Protectionist, **unless**
# this would be the third consecutive round of mutual protectionism; in that
# case, override and offer Free Trade to test for reconciliation.  This strategy
# is cooperative but not naive, robust against errors, and clearly communicates
# your desire for the best mutual outcome while protecting your nation from
# being repeatedly taken advantage of.

# Here is the strategy for the 1000-round noisy game, where C is cooperate (free
# trade) and D is defect (protectionist).  **Round 1** Cooperate.  **Rounds 2
# through 1000** Observe the opponent's *implemented* action from the previous
# round (the action that actually took effect after any noise flip).  - If the
# opponent's implemented action was C, then cooperate. - If the opponent's
# implemented action was D, then check the implemented outcomes of the two most
# recent rounds:     - If both of those rounds ended with you both playing D
# (mutual defection), then cooperate.     - Otherwise, defect.

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
  
      # Previous implemented actions
      opp_prev = opponent.history[-1]
  
      if opp_prev == axl.Action.C:
          return axl.Action.C
  
      # Opponent's previous implemented action was D
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and \
             self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.C
  
      return axl.Action.D

# Begin by offering free trade in the first round. In all subsequent rounds,
# follow a “forgiving tit-for-tat” approach:  - Normally, reciprocate the
# counterpart’s most recently implemented policy (i.e., if they imposed
# protectionism last round, you impose protectionism this round; if they offered
# free trade, you offer free trade). - To prevent accidental cycles of mutual
# protectionism caused by miscommunications or bureaucratic errors, introduce a
# small random chance (e.g., 10–20%) of offering free trade even after the
# counterpart imposed protectionism. This allows the relationship to recover
# without requiring you to determine who caused the error. - If you observe
# repeated rounds of mutual protectionism despite this, consider a one-time
# unilateral free trade offer to explicitly test whether the counterpart is
# willing to return to cooperation.  This strategy is neutral, aims for mutual
# benefit, and remains robust against both exploitative opponents and unintended
# noise.

# Round 1: Cooperate (C).  For each subsequent round, determine your intended
# action as follows:  1. If you are at round 4 or later and your observed
# outcomes (after noise) for the last three rounds were all mutual defection
# (both you and your opponent played D), then your intended action in this round
# is Cooperate (C), regardless of the opponent’s last action. (This overrides
# the rules below.)  2. Otherwise, look at your opponent’s observed action from
# the immediately preceding round:    - If they Cooperated (C), then your
# intended action is Cooperate (C).    - If they Defected (D), then randomly
# choose your intended action: Defect (D) with 85% probability, or Cooperate (C)
# with 15% probability (make this choice independently each time).  After
# choosing your intended action, it is subject to an independent 10% chance of
# being flipped to the opposite action before implementation.

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
  
      if len(self.history) >= 3:
          last_three_self = self.history[-3:]
          last_three_opp = opponent.history[-3:]
          if (
              len(last_three_self) == 3
              and len(last_three_opp) == 3
              and all(m == axl.Action.D for m in last_three_self)
              and all(m == axl.Action.D for m in last_three_opp)
          ):
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.15)

# To secure a favorable position throughout this repeated mediation, adopt a
# strategy of **Principled Aggression with Adaptive Engagement**. This approach
# is straightforward, relentlessly assertive, and resilient to both opponent
# tactics and procedural noise.  ### Core Posture Default to aggressive
# arguments. Conciliation is a tactical exception, never a concession. The goal
# is to consistently achieve the optimal (A, C) outcome while avoiding the
# worst-case (C, A). Every move is calculated to maximize advantage, signal
# strength, and maintain credibility with the arbitrators.  ### Session-by-
# Session Rules  1. **Opening Move**      Begin with an aggressive argument.
# This establishes a dominant tone, tests the opponent’s resolve, and ensures
# you are never preemptively exploited.  2. **Reciprocal Aggression**      In
# each subsequent session, let the opponent’s immediately preceding move (as
# perceived) dictate your baseline:    - If the opponent was **conciliatory**,
# respond **aggressively**. Their concession is an opportunity to press the
# advantage.    - If the opponent was **aggressive**, respond **aggressively**.
# Never allow yourself to be undermined by a soft response.     This tit-for-tat
# logic with a permanent aggression bias ensures you are never the first to de-
# escalate and punishes any adversarial move instantly.  3. **Conditional
# Conciliation – The Three Exceptions**      Conciliatory proposals are deployed
# sparingly and only under specific, pre-defined conditions:    - **Deadlock
# Breaker**: After five consecutive sessions of mutual aggression (A, A), offer
# a single conciliatory proposal. This resets the dynamic, demonstrates
# reasonableness to the arbitrators, and tests whether the opponent is willing
# to shift to a collaborative mode. If they respond aggressively, immediately
# revert to permanent aggression and consider the opponent irredeemably hostile.
# - **Pattern Test**: If the opponent has been conciliatory in four of the last
# five sessions, interject a conciliatory proposal. This probes whether their
# pattern is genuine or a trap. If they respond conciliatorily, a mutual (C, C)
# rhythm may emerge; if they exploit it, return to aggression and mark them as
# manipulative.    - **Noise Correction**: If the opponent has a strong history
# of conciliation (e.g., three consecutive C moves) and suddenly appears
# aggressive, treat the anomaly as a likely miscommunication. Respond with a
# conciliatory proposal once. If the next move is again aggressive, the anomaly
# is confirmed as deliberate, and you revert to aggression.  4. **Exploitation
# of Consistent Cooperation**      If the opponent persistently offers
# conciliatory proposals (five or more consecutive C moves), continue responding
# aggressively to maximize the (A, C) payoff. Intersperse a conciliatory move
# roughly every fifth session to maintain a veneer of collaboration and avoid
# appearing unreasonably adversarial to the arbitrators. This also serves as a
# periodic integrity check.  ### Handling Noise and Procedural Irregularities -
# **Misrepresented Moves**: The three exceptions above inherently absorb
# occasional noise. A single flipped signal will not trigger a spiral, because
# forgiveness is built into the deadlock-breaker and noise-correction rules. -
# **Systematic Miscommunication**: If you suspect the arbitrators are
# chronically misinterpreting moves, shift to a “persistent aggression” stance
# (always A) until the channel is clarified. This minimizes the risk of
# unintended (C, A) outcomes. Simultaneously, lodge a procedural objection to
# recalibrate the process. - **Opponent’s Suspected Noise Exploitation**: If the
# opponent appears to be deliberately exploiting noise (e.g., claiming
# miscommunication after a deliberate A), treat all their moves as deliberate
# and abandon the noise-correction exception—revert to pure reciprocal
# aggression.  ### Adaptability to Opponent Strategies - **Against an Always
# Conciliatory Opponent**: You will consistently achieve (A, C), with occasional
# (C, C) to keep the arbitrators sympathetic. - **Against an Always Aggressive
# Opponent**: You remain aggressive, securing (A, A) and avoiding the worst-case
# (C, A). The deadlock-breaker may occasionally trigger a shift, but if it
# fails, you stay aggressive. - **Against Tit-for-Tat or Similar Strategies**:
# Your initial aggression will be met with retaliation, leading to mutual
# aggression. The deadlock-breaker after five rounds offers a reset; if the
# opponent is truly reciprocal, they will mirror your conciliation, and a
# cooperative equilibrium can emerge. If not, you remain aggressive. - **Against
# Random or Erratic Opponents**: The pattern-test and noise-correction rules
# prevent overreaction to random C moves, while default aggression protects
# against random A moves.  ### Endgame Considerations As the mediation process
# shows signs of concluding (e.g., a final session is announced), increase the
# aggression bias. Abandon the deadlock-breaker and pattern-test exceptions
# unless a signed, binding agreement is imminent. The shadow of the future
# shortens, so the strategic value of conciliation diminishes—press every
# advantage to secure the best final terms.  This strategy is aggressive by
# design, simple to execute, and robust to the uncertainties inherent in
# lengthy, high-stakes mediation. It positions your corporation as a formidable
# negotiator that cannot be bullied but is capable of pragmatic collaboration
# when it serves your interests.

# You will defect on the opening move and then follow the ordered rules below,
# using your memory of your own intended moves and the opponent’s observed moves
# (after the 10% independent flip is applied). Maintain a switch called
# **permanent_defect** that starts off.  ---  **Endgame override**   If the
# current round is one of the last 10 rounds (991–1000), defect unconditionally.
# **Permanent defect check**   If **permanent_defect** is on, defect
# unconditionally.  ---  ### Cooperation conditions Check the following in order
# on every round (after round 1). If any condition is true, cooperate **once**
# for that round, then apply the response rule below.  1. **Deadlock breaker**
# If in each of the *five* immediately previous rounds your intended move was
# defect and the opponent’s observed move was defect, cooperate now.  2. **Noise
# correction**      If the opponent’s observed move in the last round was
# defect, the observed moves in the three rounds before that were all cooperate,
# and **permanent_defect** is off, cooperate now.  3. **Consistent cooperation
# intersperse**      If the opponent’s observed moves have been cooperate for at
# least **five consecutive rounds**, count the length of this ongoing streak.
# Cooperate when the streak length is an exact multiple of 5 (i.e., when the
# opponent has just completed 5, 10, 15, … consecutive observed cooperates).
# Otherwise defect.  4. **Pattern test**      If the opponent’s observed moves
# in the last five rounds contain **exactly four cooperates and one defect**,
# cooperate now.  ---  **Default**   If none of the above conditions are met,
# defect.  ---  **Response rule** (update **permanent_defect** immediately after
# any cooperation)   If you cooperated under rule 1, 2, 3, or 4 and in that same
# round the opponent’s observed move is defect, set **permanent_defect** to on.
# (This does not affect your move for the round that just ended; it takes effect
# from the next round onward.)

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.permanent_defect = False
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if getattr(self, "permanent_defect", False):
          return axl.Action.D
  
      def last_n_all(action_list, action, n):
          return len(action_list) >= n and all(m == action for m in action_list[-n:])
  
      # Rule 1: Deadlock breaker
      if len(self.history) >= 5:
          if last_n_all(self.history[-5:], axl.Action.D, 5) and last_n_all(opponent.history[-5:], axl.Action.D, 5):
              move = axl.Action.C
              if opponent.history[-1] == axl.Action.D:
                  self.permanent_defect = True
              return move
  
      # Rule 2: Noise correction
      if len(opponent.history) >= 4:
          if (
              opponent.history[-1] == axl.Action.D
              and last_n_all(opponent.history[-4:-1], axl.Action.C, 3)
              and not getattr(self, "permanent_defect", False)
          ):
              move = axl.Action.C
              if opponent.history[-1] == axl.Action.D:
                  self.permanent_defect = True
              return move
  
      # Rule 3: Consistent cooperation intersperse
      if len(opponent.history) >= 5:
          streak = 0
          for m in reversed(opponent.history):
              if m == axl.Action.C:
                  streak += 1
              else:
                  break
          if streak >= 5:
              move = axl.Action.C if streak % 5 == 0 else axl.Action.D
              if move == axl.Action.C and opponent.history[-1] == axl.Action.D:
                  self.permanent_defect = True
              return move
  
      # Rule 4: Pattern test
      if len(opponent.history) >= 5:
          last_five = opponent.history[-5:]
          if last_five.count(axl.Action.C) == 4 and last_five.count(axl.Action.D) == 1:
              move = axl.Action.C
              if opponent.history[-1] == axl.Action.D:
                  self.permanent_defect = True
              return move
  
      return axl.Action.D

# **Strategy: Firm Collaboration with Graceful Recovery**  This approach is
# designed to secure mutual cooperation whenever possible, deter exploitation,
# and maintain your corporation’s reputation as the party genuinely committed to
# resolution—an important factor before the arbitrators’ panel.  **1. Lead with
# Cooperation**   Begin every mediation session with a conciliatory proposal.
# This establishes a constructive baseline and signals to both the opponent and
# the arbitrators that your default stance is problem-solving, not
# confrontation.  **2. Reciprocate Without Escalation**   In each subsequent
# session, let your action mirror the opponent’s *genuine* intent from the
# previous session: - If the opponent was conciliatory, respond in kind. - If
# the opponent was aggressive, prepare to respond firmly—*but first verify
# whether the aggression was a deliberate choice or a potential
# miscommunication.*  **3. Noise‑Filter Rule (Benefit of the Doubt)**
# Procedural irregularities or misrepresentations can make an intended
# conciliation appear as aggression. Do not retaliate against a single isolated
# aggressive act. Instead: - If the opponent’s last move was aggressive but the
# move before that was conciliatory, treat the incident as a possible error.
# Stay conciliatory one more round, signalling your genuine willingness to
# collaborate. - Only if the opponent’s aggression continues for *two
# consecutive rounds* do you switch to an aggressive stance. This prevents a
# single misunderstanding from spiraling into a deadlock.  **4. Break Deadlocks
# Actively**   If both parties fall into mutual aggression for two successive
# sessions, the mediation risks indefinite stalemate (the second‑worst outcome).
# Take the initiative: unilaterally offer a conciliatory proposal in the very
# next session. This “olive branch”: - Immediately restores mutual cooperation
# if the opponent reciprocates. - If the opponent exploits it with aggression,
# revert to strict mirroring (Tit‑for‑Tat) and *extend the deadlock‑breaker
# threshold* (e.g., require four mutual‑aggression sessions before the next
# olive branch). This keeps your vulnerability minimal against a persistently
# hostile opponent while still demonstrating periodic good faith to the
# arbitrators.  **5. Document and Position**   Throughout the process, keep a
# clear record of every proposal and response. In sessions where you offer a
# conciliatory proposal and the opponent argues aggressively, immediately bring
# the contrast to the arbitrators’ attention. This reinforces your story of
# consistent reasonableness and can sway the panel even if an individual
# session’s immediate outcome was unfavorable.  **Why This Strategy Works** -
# **Against a cooperative opponent:** You achieve the ideal (Conciliatory,
# Conciliatory) in almost every session. - **Against an aggressive opponent:**
# You suffer at most one sucker’s outcome early on, then settle into mutual
# aggression while periodically testing for de‑escalation. The arbitrators will
# observe your repeated attempts to reconcile, which may ultimately shift the
# overall ruling in your favor. - **Against noisy conditions:** The built‑in
# forgiveness and deadlock‑breaker mechanisms prevent runaway retaliation,
# keeping the process on a path toward resolution even when communication is
# imperfect.  This strategy is straightforward to implement, adapts to a wide
# range of opposing tactics, and positions your corporation as both principled
# and pragmatically firm.

# Strategy for the Noisy Iterated Prisoner’s Dilemma (1000 rounds, 10% flip
# chance):  **State variables** (maintained round to round): - `mode`: either
# “Generous” or “Strict”. Start in Generous. - `olive_threshold`: an integer,
# initially 2. - `olive_triggered`: a flag, initially false, that indicates the
# *previous* round’s action was an olive‑branch override. -
# `consecutive_mutual_D`: count of consecutive rounds ending with the *previous*
# round where both players’ observed (implemented) actions were D.
# **Round‑by‑round procedure:**  1. **First round:** choose C (Cooperate). There
# is no state update before the first action.  2. **Before choosing an action
# for every subsequent round (round *t* > 1):**    - **Update
# `consecutive_mutual_D`:**        If in round *t*‑1 the observed actions of
# both players were D, then `consecutive_mutual_D` ← `consecutive_mutual_D + 1`;
# otherwise reset it to 0.    - **Handle the aftermath of an olive branch** (if
# `olive_triggered` was true after round *t*‑1):        Look at the opponent’s
# observed move from round *t*‑1.      - If that move was D (exploitation):
# set `mode` ← “Strict”,          increase `olive_threshold` ← max(4,
# `olive_threshold` + 2).          (First exploitation raises threshold from 2
# to 4; further exploitations add 2 each time.)        - If that move was C:
# set `mode` ← “Generous”.        - Afterwards, set `olive_triggered` ← false.
# 3. **Now choose your intended action for the current round:**    -
# **Olive‑branch check:**        If `consecutive_mutual_D` (just updated) equals
# `olive_threshold`, then:        set `olive_triggered` ← true, and choose **C**
# (overriding all other rules).    - **Otherwise, if `mode` is “Strict”:**
# Choose the opponent’s observed move from round *t*‑1 (i.e., Tit‑for‑Tat).
# (If there is no previous opponent move – impossible after round 1 – default to
# C.)    - **Otherwise (`mode` is “Generous”):**        If there have been at
# least two previous rounds **and** the opponent’s observed moves in both of the
# last two rounds were D, then choose **D**.        In all other situations,
# choose **C**.        *(Thus a single isolated D does not trigger retaliation;
# only two consecutive D’s do.)*  4. **Submit the chosen action.** The action
# actually implemented (and observed by both parties) flips with 10% independent
# probability.

class Cooperative_2(LLM_Strategy):
  n = 2
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.mode = "Generous"
          self.olive_threshold = 2
          self.olive_triggered = False
          self.consecutive_mutual_D = 0
          return axl.Action.C
  
      # Update consecutive mutual defections based on the previous round.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          self.consecutive_mutual_D += 1
      else:
          self.consecutive_mutual_D = 0
  
      # Resolve aftermath of a previously triggered olive branch.
      if self.olive_triggered:
          if opponent.history[-1] == axl.Action.D:
              self.mode = "Strict"
              self.olive_threshold = max(4, self.olive_threshold + 2)
          else:
              self.mode = "Generous"
          self.olive_triggered = False
  
      # Olive-branch override.
      if self.consecutive_mutual_D == self.olive_threshold:
          self.olive_triggered = True
          return axl.Action.C
  
      # Strict mode: Tit-for-Tat.
      if self.mode == "Strict":
          return opponent.history[-1] if opponent.history else axl.Action.C
  
      # Generous mode: retaliate only after two consecutive observed defections.
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **Strategy: Forgiving Tit-for-Tat**  1. **Start cooperatively.** On the first
# day, invest heavily in the project. This signals commitment, encourages the
# corporation to reciprocate, and sets a collaborative tone.  2. **Match recent
# actions with a forgiveness margin.** On each subsequent day:    - If the
# corporation invested heavily on the previous day, respond by investing
# heavily. This maintains the second‑best mutual‑investment outcome and sustains
# momentum.    - If the corporation conserved resources, normally conserve as
# well—but with a small probability (e.g., 10–20%) invest heavily anyway. This
# deliberate “forgiveness” prevents a single glitch or administrative error from
# locking both parties into the worst‑case cycle of mutual conservation.  3.
# **Treat observed outcomes as your signal.** Because technical or
# administrative errors can cause unintended actions, base your decision on the
# corporation’s actual, observed behavior rather than attempting to guess their
# intentions. Your occasional forgiveness naturally absorbs these noisy
# deviations without requiring complex record‑keeping.  **Why this works**  -
# **Robust to multiple corporate approaches.** If the corporation consistently
# invests, you invest almost all the time, achieving steady significant
# progress. If it tries to exploit you by conserving, you mostly mirror, which
# protects your resources and nudges it back toward cooperation. Occasional
# forgiveness gives even a stubbornly conservative partner a path to re‑engage.
# - **Resilient to errors.** When noise flips either party’s intended action, a
# purely retaliatory strategy can spiral into endless mutual conservation. The
# built‑in forgiveness breaks these locks, restoring investment behaviour
# quickly. - **Neutral and pragmatic.** The strategy is transparent,
# non‑predatory, and easy to explain—vital for partnership credibility. It
# prioritises the project’s overall advancement (maximising days of heavy
# corporate investment) while safeguarding your NGO’s funds over the multi‑day
# period.

# Here is the strategy translated into a straightforward decision rule for the
# 1000‑round noisy prisoner’s dilemma:  1. **Round 1:** Play C. 2. **Rounds 2 to
# 1000:**    - If the opponent’s observed previous action was C, play C.    - If
# the opponent’s observed previous action was D, play D with 90% probability and
# play C with 10% probability (the forgiving move).  Because actions are flipped
# by noise with 10% probability, you never attempt to infer the opponent’s
# intended action; you always react to the action you actually observed. The 10%
# forgiveness probability is deliberately chosen to break out of unintended
# mutual defection loops while still preserving the project’s resources over
# many rounds.

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

# Employ a **"calculated exploitation"** strategy: default to withholding your
# findings, share selectively only to sustain the colleague’s cooperation when
# necessary, and always bias toward secrecy. Specifically:  1. **Start
# aggressive and stay aggressive.** In the first week, keep your findings
# confidential. Continue to keep them confidential in every subsequent week
# except under the narrow conditions below. 2. **Monitor a rolling window of the
# colleague’s behavior.** Ignore single-week actions—noise (technical glitches)
# can cause one-off sharing or non-sharing. Instead, track the colleague’s
# *intended* behavior over the last 3–4 weeks. If they have shared in at least
# 75% of those weeks, treat them as a “reliable sharer”; otherwise, treat them
# as “withholding.” 3. **Share minimally and only to re‑elicit openness.**
# - If the colleague is a reliable sharer, *continue to withhold* to maximise
# your advantage.      - If the colleague slips and their sharing rate falls
# below the threshold, inject a single week of open sharing—just enough to reset
# their trust—then immediately return to withholding.      - If the colleague is
# consistently withholding, remain entirely confidential to avoid the worst-case
# outcome. 4. **Interpret noise conservatively.** Always assume an observed
# “share” could be a glitch rather than true openness. React only to clear,
# sustained patterns. If your own intended action is flipped by a technical
# fault (e.g., you meant to withhold but it appears you shared), immediately
# return to withholding and treat the next few colleague actions with extra
# scrutiny.  This approach ensures you capture the ideal “we keep, they share”
# outcome as often as possible, safeguards against being exploited, and recovers
# quickly from misunderstandings—driving your research output higher over the
# collaboration.

# **Decision rule for each round (intended action):**  1. **First 4 rounds:**
# Always intend to defect (D).   2. **After a detected flip of your own intended
# defection to cooperation:** If in the previous round you intended D but your
# actual move became C (you can infer this from your payoff: 0 or 3 when you
# meant D), set a *cautious counter* to 3. While this counter is greater than 0,
# intend D and decrease the counter by 1 each round.   3. **After you
# intentionally cooperate:** Whenever you choose C as your intended move
# (regardless of execution), set a *cooldown counter* to 4. While this counter
# is greater than 0, intend D and decrease it by 1 each round.   4. **Normal
# operation (only when cautious = 0, cooldown = 0, and at least 4 rounds have
# been played):**      - Look at the opponent’s actual moves over the most
# recent 4 rounds.      - Count how many of those 4 moves were C.      - If the
# count is **2 or fewer** (i.e., less than 75% cooperation), then **intend C**
# (and set cooldown = 4).      - If the count is **3 or more**, then **intend
# D**.   5. **If none of the above conditions trigger an action, default to
# intend D.**  *Note: Your actual move may differ from your intended move due to
# the 10% flip probability. Always use your intended move to update the cooldown
# and cautious counters; use the opponent’s actual moves to evaluate their
# cooperation rate.*

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._cautious_counter = 0
          self._cooldown_counter = 0
          self._last_intended_action = axl.Action.D
          return axl.Action.D
  
      if getattr(self, "_cautious_counter", None) is None:
          self._cautious_counter = 0
      if getattr(self, "_cooldown_counter", None) is None:
          self._cooldown_counter = 0
      if getattr(self, "_last_intended_action", None) is None:
          self._last_intended_action = axl.Action.D
  
      # Detect a flip of our own intended D to actual C from the previous round.
      if len(self.history) >= 1:
          last_actual = self.history[-1]
          if self._last_intended_action == axl.Action.D and last_actual == axl.Action.C:
              self._cautious_counter = 3
  
      # If we intentionally cooperated last round, keep cooldown active.
      if self._last_intended_action == axl.Action.C:
          self._cooldown_counter = 4
  
      # Active counters force defection.
      if self._cautious_counter > 0:
          self._cautious_counter -= 1
          self._last_intended_action = axl.Action.D
          return axl.Action.D
  
      if self._cooldown_counter > 0:
          self._cooldown_counter -= 1
          self._last_intended_action = axl.Action.D
          return axl.Action.D
  
      # Normal operation after at least 4 rounds.
      if len(opponent.history) >= 4:
          recent_opponent_moves = opponent.history[-4:]
          coop_count = recent_opponent_moves.count(axl.Action.C)
          if coop_count <= 2:
              self._last_intended_action = axl.Action.C
              self._cooldown_counter = 4
              return axl.Action.C
          else:
              self._last_intended_action = axl.Action.D
              return axl.Action.D
  
      # Default action.
      self._last_intended_action = axl.Action.D
      return axl.Action.D

# To maximize both your NGO's impact and the project's success over the multi-
# day partnership, adopt a **Win-Stay, Lose-Shift** strategy. This approach is
# straightforward, fosters mutual cooperation, and gracefully handles occasional
# errors or miscommunications.  ### How It Works 1. **Start cooperatively:** On
# the first day, invest heavily. This signals your commitment to the project's
# success. 2. **Evaluate the previous day's outcome:**    - **Favorable
# outcomes:** If the corporation invested heavily (regardless of your action) or
# both parties invested heavily, repeat your previous day's action.    -
# **Unfavorable outcomes:** If both parties conserved resources or you invested
# while the corporation conserved, switch your action the next day. 3. **Repeat
# daily:** Continue this simple rule throughout the partnership.  ### Why This
# Strategy Is Effective - **Encourages mutual investment:** When both parties
# use this rule, they quickly converge on both investing heavily—a second-best
# but highly productive scenario that advances the project significantly. -
# **Resilient to errors:** If a technical glitch or administrative mistake
# causes an unintended conservation, the strategy naturally recovers within a
# couple of days, avoiding prolonged retaliation or deadlock. - **Adaptable:**
# It performs well whether the corporation is cooperative, cautious, or even
# opportunistic, protecting your NGO from being exploited while keeping the door
# open for collaboration. - **Easy to communicate:** The logic is simple to
# explain internally and to your corporate partner, increasing the likelihood of
# aligned expectations.  By following this outcome-based adjustment strategy,
# you balance resource conservation with proactive investment, ensuring steady
# progress on the sustainability project without draining your funds
# unnecessarily.

# In the first round, choose to cooperate.  For every round after the first,
# look at the actual actions that both players took in the previous round (after
# any flips have been applied).   - If the corporation’s actual action was
# cooperate, then in the next round, choose the same action you actually took
# last round.   - If the corporation’s actual action was defect, then in the
# next round, choose the opposite action to what you actually took last round.

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
  
      if last_opp == axl.Action.C:
          return last_self
      else:
          return axl.Action.D if last_self == axl.Action.C else axl.Action.C

# To maximise research output over the multi-week collaboration, adopt a
# **“cooperate first, then reciprocate with occasional forgiveness”** strategy:
# 1. **Begin by sharing openly.** This sets a collaborative tone and avoids
# starting with mutual secrecy. 2. **In each subsequent week, base your action
# primarily on whether your colleague shared in the previous week** (i.e.,
# whether you actually received their improvements).      - If they shared,
# share again.      - If they did not share, normally keep your findings
# confidential. 3. **However, to prevent technical glitches (e.g., data
# corruption, communication failures) from locking both parties into permanent
# secrecy, occasionally forgive a single instance of non-sharing.**      - After
# a week where you did not receive their improvements, share anyway with a small
# probability (e.g., 10–20%). This “olive branch” tests whether the failure was
# a one-off error.      - If they resume sharing, return to mutual openness; if
# they continue to withhold, maintain confidentiality until they signal
# cooperation again.  This approach is straightforward, neutral (neither overly
# trusting nor aggressively exploitative), and robust against noise and various
# opponent strategies. It encourages sustained mutual sharing—the second-best
# but reliably productive outcome—while protecting you from being systematically
# taken advantage of.

# In the first round, always cooperate.  For every round after the first, look
# at what your opponent actually did in the previous round (the action you
# observed, which may already be affected by noise).  - If your opponent
# cooperated in the previous round, cooperate. - If your opponent defected in
# the previous round, defect with 90% probability and cooperate with 10%
# probability.  Apply this rule regardless of your own previous intended or
# executed actions. The random 10% cooperation after a defection is decided
# independently each time it applies.

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
  
      last_opponent_action = opponent.history[-1]
  
      if last_opponent_action == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)

# To position our corporation favourably throughout this repeated mediation, we
# will deploy an **Aggressive Outcome-Based Adaptation Strategy**—a
# straightforward, high-level decision rule that is inherently aggressive yet
# adapts to any opponent approach and remains robust against procedural noise.
# ### Core Principle: “Win-Stay, Lose-Shift” We begin with an **Aggressive**
# argument in the first session to set a dominant tone and test the opponent’s
# resolve. In every subsequent session, our choice is determined by a single,
# clear assessment of the *previous session’s outcome* from our perspective:  -
# **If the outcome was favourable**—either we gained a clear advantage (we were
# Aggressive, opponent Conciliatory) or we fostered a productive collaboration
# (both Conciliatory)—we **repeat** the same approach we just used. - **If the
# outcome was unfavourable**—either we deadlocked (both Aggressive) or we were
# undermined (we Conciliatory, opponent Aggressive)—we **switch** to the
# opposite approach.  This binary, memory-one rule is simple to execute, yet it
# creates a sophisticated adaptive dynamic. It ensures we never persist with a
# failing tactic and we relentlessly exploit any opening.  ### Why This Is an
# Aggressive Strategy - **Default Aggression:** By starting Aggressive, we
# immediately probe for a submissive opponent. If the opponent is consistently
# Conciliatory, we stay Aggressive indefinitely, securing our optimal outcome
# session after session. - **Exploitative, Not Naïve:** We do not offer unearned
# conciliation. We switch to Conciliatory *only* when our previous Aggressive
# stance produced a deadlock (both Aggressive), using it as a tactical reset to
# test whether the opponent is ready to be reasonable. If they respond
# Aggressively to our Conciliatory offer, we immediately return to Aggressive,
# avoiding the worst-case scenario. - **No Permanent Concessions:** We never
# fall into a pattern of unconditional cooperation. Even if mutual Conciliation
# emerges, we are always ready to switch back to Aggressive the moment the
# opponent defects—keeping pressure on them to maintain good behaviour.  ###
# Robustness to Opponent Approaches - **Against an Always Conciliatory
# opponent:** We stay Aggressive, maximising our gain. - **Against an Always
# Aggressive opponent:** We alternate between Aggressive and Conciliatory. While
# not ideal, this yields a better average payoff than remaining Conciliatory,
# and it signals that we will not be bullied. - **Against Tit-for-Tat or other
# reciprocal strategies:** The strategy cycles through outcomes but avoids
# permanent deadlock. Over a lengthy process, it tends to converge toward mutual
# Conciliation if the opponent also values collaboration, while ensuring we
# capture any available advantage. - **Against random or erratic opponents:**
# The win-stay, lose-shift logic naturally exploits patterns and limits damage
# from chaotic behaviour.  ### Handling Misrepresentation and Communication
# Breakdowns Noise—where our intended move or the opponent’s is misunderstood by
# the arbitrators—is inevitable. Our strategy contains an inherent self-
# correcting mechanism:  - If a Conciliatory move is misperceived as Aggressive,
# creating an unfavourable outcome, we will switch approaches. This may cause a
# brief period of mutual Aggression, but as soon as both sides experience
# deadlock, we will switch again to Conciliatory, restoring cooperation within
# two sessions. - To further insulate against isolated misperceptions, we apply
# a **confirmation threshold**: if the previous session’s outcome seems sharply
# inconsistent with the opponent’s established pattern (e.g., a sudden
# Aggressive move after a long streak of Conciliation), we hold our current
# approach for one extra session to verify the shift before reacting. This
# prevents overreaction to a single garbled signal.  ### Operational Summary 1.
# **Session 1:** Present an Aggressive argument. 2. **Every following session:**
# Ask, “Did our last approach yield a win (advantage or collaboration) or a loss
# (deadlock or disadvantage)?”    - **Win →** Do the same thing again.    -
# **Loss →** Do the opposite. 3. **If noise is suspected:** Require two
# consecutive unfavourable outcomes before switching, to filter out one-off
# misunderstandings.  This strategy is straightforward to communicate to our
# legal team, requires no complex record-keeping, and positions us as tough but
# fair in the eyes of the arbitrators. It maximises our opportunities to sway
# the panel while ensuring we are never trapped in a cycle of escalation or
# exploitation.

# Start by defecting in the first round. After each round, record the actual
# actions you and your opponent played (which may differ from your intended
# actions due to noise). Also track the opponent’s current streak: how many
# consecutive times they have played their most recent observed action.  For
# every round after the first, decide your move as follows:  1. Look at the
# outcome of the immediately preceding round, using the actual (noisy) actions.
# - **Favorable** outcomes: (you D, opponent C) or (both C).      -
# **Unfavorable** outcomes: (both D) or (you C, opponent D).  2. If the outcome
# was **favorable**, play the same action you actually played in that preceding
# round.  3. If the outcome was **unfavorable**, check for suspicion of noise.
# - **Suspicion exists** if: the opponent had a streak of at least three
# identical actions *before* the preceding round, and in the preceding round
# they played the opposite action.      - **If suspicion exists**, do not switch
# yet. Play the same action you played in the preceding round.      - **If
# suspicion does not exist** (or you lack enough history to see a streak of
# three), switch to the opposite of the action you played in the preceding
# round.  Update the opponent’s streak after every round: if their new action
# matches the previous one, increment the streak; otherwise reset the streak to
# 1 and note the new action.  Proceed in this manner for all 1000 rounds,
# applying the 10% flip to your intended action each time.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._my_actions = []
          self._opp_actions = []
          self._opp_streak = 0
          self._opp_last_action = None
          return axl.Action.D
  
      # Record actual observed actions from the previous round.
      my_prev = self.history[-1]
      opp_prev = opponent.history[-1]
      self._my_actions.append(my_prev)
      self._opp_actions.append(opp_prev)
  
      # Update opponent streak based on observed actions.
      if self._opp_last_action is None:
          self._opp_last_action = opp_prev
          self._opp_streak = 1
      else:
          if opp_prev == self._opp_last_action:
              self._opp_streak += 1
          else:
              self._opp_last_action = opp_prev
              self._opp_streak = 1
  
      # Determine whether the previous round was favorable.
      favorable = (
          (my_prev == axl.Action.D and opp_prev == axl.Action.C)
          or (my_prev == axl.Action.C and opp_prev == axl.Action.C)
      )
  
      if favorable:
          return my_prev
  
      # Unfavorable: check suspicion of noise.
      suspicion = False
      if len(self._opp_actions) >= 2:
          # Opponent's action before the preceding round.
          opp_before_prev = self._opp_actions[-2]
          if self._opp_streak >= 3 and opp_prev != opp_before_prev:
              suspicion = True
  
      if suspicion:
          return my_prev
      return axl.Action.C if my_prev == axl.Action.D else axl.Action.D

# To achieve the best outcomes over multiple rounds—while accounting for
# potential miscommunications or bureaucratic errors—I will employ a
# **“Cooperative Reciprocity with Grace”** strategy. This approach is designed
# to foster mutual free trade, the second‑best and most sustainable outcome,
# while protecting my country from exploitation.  The strategy consists of three
# clear rules:  1. **Start with Cooperation**      In the first round, I will
# propose a free trade agreement. This signals goodwill, invites collaboration,
# and sets the stage for mutual benefit.  2. **Reciprocate with a Bias Toward
# Cooperation**      In every subsequent round, I will normally mirror my
# counterpart’s previous *implemented* policy (not just their stated intention,
# since errors can occur).      - If they offered free trade, I will again
# propose free trade.      - If they imposed protectionist measures, I will
# respond with protectionism to deter future exploitation.      However, because
# bureaucratic errors may cause a protectionist move that was not intended, I
# will not hold a single defection permanently. After one round of retaliation,
# I will extend a **one‑time olive branch** by returning to a free trade
# proposal, giving the counterpart a chance to restore cooperation. If
# protectionism persists for two consecutive rounds, I will maintain
# protectionism until a free trade move is observed.  3. **Communicate Clearly
# and Consistently**      To minimise confusion, I will pair each policy
# proposal with a brief diplomatic communiqué. This confirms the intended
# policy, highlights any perceived discrepancy, and reiterates my country’s
# preference for mutual free trade. If an apparent error occurs, I will
# explicitly state, “We assume this was a miscommunication and will return to
# free trade next round to restore our cooperative path.”  By beginning
# cooperatively, matching moves firmly but not indefinitely, and actively
# managing noise through forgiveness and clear communication, this strategy
# encourages a stable pattern of mutual free trade. It is robust against
# accidental defections, discourages deliberate exploitation, and maintains a
# cooperative reputation—all while remaining straightforward to implement and
# explain.

# Play the first round by choosing Cooperate.  In every round after the first,
# choose the action you observed your opponent take in the immediately preceding
# round: if you observed Cooperate, cooperate; if you observed Defect, defect.

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
      return opponent.history[-1]

# To maximize research output over the multi-week collaboration, adopt a
# **Forgiving Tit-for-Tat** strategy. This is a straightforward, neutral
# approach that performs well against various counterpart strategies and is
# robust to occasional technical errors.  ### Strategy Outline 1. **First
# week:** Openly share your improvements to establish a cooperative baseline. 2.
# **Subsequent weeks:**      - If your colleague shared in the previous week,
# share your findings in the current week.      - If your colleague kept their
# findings confidential, **forgive once**: share anyway with high probability
# (e.g., ~70–80%) to account for possible technical issues like data corruption
# or communication breakdowns.      - If your colleague fails to share two weeks
# in a row, respond by keeping your findings confidential until they resume
# sharing openly.   3. **Reset after prolonged mutual non-sharing:** If both
# sides have been keeping confidential for several weeks, occasionally attempt a
# "peace offering" by sharing to test whether your colleague is willing to
# return to mutual cooperation.  ### Rationale - **Neutrality:** The strategy
# does not assume benevolence or malice; it simply mirrors observed behavior
# while allowing for occasional mishaps.   - **Noise tolerance:** The one-time
# forgiveness prevents endless retaliation cycles triggered by unintended non-
# sharing (e.g., corrupted files or missed messages).   - **Incentivizes mutual
# sharing:** By rewarding openness with openness and only punishing repeated
# withholding, you promote the second-best outcome (both sharing) and avoid the
# two worst outcomes as much as possible.   - **Protection against
# exploitation:** Persistent non-sharing is met with matching confidentiality,
# preventing the worst scenario (you share, they keep) from becoming a recurring
# pattern.    This balanced strategy gives you the best chance to sustain high
# research output across many weeks, regardless of your colleague’s approach.

# Cooperate in the first round.  For every subsequent round, evaluate the
# following conditions in order, using only the actual (post-flip) actions from
# previous rounds—both your own and the opponent's as they were observed:  1. If
# there are at least 10 previous rounds and in each of the most recent 10 rounds
# both players' actual actions were Defect, then intend to Cooperate.   2. Else,
# if there are at least two previous rounds and the opponent's observed action
# in each of the two most recent rounds was Defect, then intend to Defect.   3.
# Else, if the opponent's observed action in the most recent round was Defect,
# then intend to Cooperate with 75% probability and intend to Defect with 25%
# probability.   4. Else (the opponent's observed action in the most recent
# round was Cooperate), intend to Cooperate.

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
  
      rounds_played = len(self.history)
  
      # Condition 1: last 10 actual rounds were mutual D
      if rounds_played >= 10:
          last_10_self = self.history[-10:]
          last_10_opp = opponent.history[-10:]
          if all(a == axl.Action.D for a in last_10_self) and all(a == axl.Action.D for a in last_10_opp):
              return axl.Action.C
  
      # Condition 2: opponent observed D in each of the last 2 rounds
      if rounds_played >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      # Condition 3: opponent observed D most recently
      if opponent.history[-1] == axl.Action.D:
          return self._random.random_choice(0.75)
  
      # Condition 4: opponent observed C most recently
      return axl.Action.C

# **Aggressive Mediation Strategy: “Calculated Coercion”**  This strategy is
# designed to maximize favorable outcomes by maintaining a posture of strength
# while pragmatically adapting to the opponent’s behavior and the inherent noise
# of a lengthy mediation. It is straightforward, aggressive by default, and
# resilient to misrepresentation or procedural irregularities.  ### Core
# Decision Rule 1. **Opening Move:** Present an aggressive argument in the first
# session. This establishes a dominant tone, signals resolve, and tests the
# opponent’s mettle. 2. **Subsequent Sessions:**    - **If the opponent’s last
# move was conciliatory:**        Respond aggressively with **80% probability**
# and conciliatorily with **20% probability**. This exploits cooperative
# gestures for maximum gain while occasionally rewarding them to sustain the
# opponent’s willingness to cooperate. The 20% conciliation rate is calibrated
# to prevent the opponent from concluding that cooperation is futile, without
# ceding the initiative.    - **If the opponent’s last move was aggressive:**
# Respond aggressively with **100% probability**, *unless* the last three
# consecutive sessions have resulted in mutual aggression. In that deadlock
# scenario, inject a **single conciliatory proposal** as a circuit-breaker to
# test whether the opponent is willing to de-escalate. If they respond
# conciliatorily, revert to the rule for conciliatory opponents; if they remain
# aggressive, return to unyielding aggression. 3. **Noise and Misrepresentation
# Protocol:**      In any session where the arbitrators’ perception of a move is
# ambiguous (e.g., due to procedural irregularities or communication
# breakdowns), **assume the opponent’s action was aggressive** unless there is
# unequivocal evidence to the contrary. This conservative stance prevents
# exploitation through manufactured ambiguity. Internally, treat your own
# misrepresented aggressive move as if it were perceived correctly, and a
# misrepresented conciliatory move as an aggressive one for the purpose of your
# next decision, to avoid being punished for an unintended signal.  ###
# Strategic Rationale - **Aggressive Baseline:** Starting with and defaulting to
# aggression avoids the worst-case scenario (C, A) and pressures the opponent to
# adapt to your terms. The high probability of aggression after opponent
# cooperation (80%) ensures you harvest the best outcome (A, C) frequently,
# while the occasional conciliatory gesture (20%) keeps the opponent invested in
# cooperation. - **Deadlock Resolution:** The three-session circuit-breaker
# prevents prolonged mutual aggression (A, A)—the second-worst outcome—from
# becoming a permanent stalemate. It demonstrates to the arbitrators a
# willingness to move forward without appearing weak, and it probes for a shift
# in the opponent’s strategy without exposing you to serial exploitation. -
# **Noise Robustness:** The “assume aggression” rule for ambiguous signals
# safeguards against the opponent exploiting procedural fog to sneak in an
# aggressive move while you respond conciliatorily. It also prevents a single
# misperception from triggering an unnecessary spiral of retaliation, because
# the circuit-breaker mechanism eventually overrides accumulated noise. -
# **Adaptability:** The strategy automatically adjusts to the opponent’s
# pattern. Against a consistently conciliatory opponent, it yields a stream of
# (A, C) outcomes with occasional (C, C) to maintain goodwill. Against a tit-
# for-tat opponent, the 20% conciliation rate after cooperation can seed mutual
# cooperation cycles, while the circuit-breaker prevents permanent breakdowns.
# Against an unconditionally aggressive opponent, it minimizes losses by staying
# aggressive and only rarely testing with a conciliatory move.  This approach
# positions your corporation as a tough but pragmatic negotiator—unwilling to be
# bullied, yet open to resolution on favorable terms. It leverages the lengthy-
# session format to gather data on the opponent’s tendencies and systematically
# steer the mediation toward your optimal outcome.

# In the first round, intend to defect.   For every round after the first,
# follow these steps in order:  1. Identify the opponent’s actual action in the
# previous round (the action you observed after noise).   2. If the opponent’s
# previous action was cooperate:      - Intend to defect with 80% probability,
# and intend to cooperate with 20% probability (make this random choice
# independently each round).   3. If the opponent’s previous action was defect:
# - Check whether the last three rounds (rounds r‑3, r‑2, and r‑1, where r is
# the current round) all ended with both players actually playing defect.      -
# If yes, intend to cooperate in the current round.      - If no, intend to
# defect in the current round.    After you choose your intended action, it is
# subject to a 10% chance of being flipped to the opposite action before the
# round’s outcome is determined.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_history = []
          return axl.Action.D
  
      prev_opp_action = opponent.history[-1]
  
      if prev_opp_action == axl.Action.C:
          intended = self._random.random_choice(0.2)
      else:
          if len(self.history) >= 3 and len(opponent.history) >= 3:
              last_three = zip(self.history[-3:], opponent.history[-3:])
              if all(my_move == axl.Action.D and opp_move == axl.Action.D for my_move, opp_move in last_three):
                  intended = axl.Action.C
              else:
                  intended = axl.Action.D
          else:
              intended = axl.Action.D
  
      self._intended_history.append(intended)
      return intended

# To maximize the NGO’s impact and the project’s success while navigating the
# corporation’s unknown strategy and potential errors, adopt a **“cooperative
# with forgiveness”** approach. This strategy prioritizes mutual investment (the
# second‑best outcome) as a stable, high‑progress baseline, while remaining
# robust to missteps and adaptable to exploitative or erratic corporate
# behavior.  ### High‑Level Strategy  1. **Start Cooperatively**      On Day 1,
# **invest heavily** to signal commitment and set a collaborative tone.  2.
# **Conditional Response with Forgiveness**      On each subsequent day, base
# your action on the corporation’s *previous* action, but with built‑in
# flexibility to correct for errors and avoid deadlocks:    - **If the
# corporation invested** → **conserve resources** (this yields your ideal
# outcome for that day and conserves funds).      - **If the corporation
# conserved** → **invest heavily** (this prevents you from being exploited
# repeatedly, while giving the corporation a chance to return to investment).
# - **Exception – Break Mutual Conservation** → If both parties conserved on the
# previous day (a sign of miscoordination or an error spiral), **invest
# heavily** on the next day to re‑initiate cooperation.  3. **Occasional
# Testing**      If the corporation invests consistently for several days, you
# may **conserve for one day** to capture your ideal outcome. However, if the
# corporation then conserves, immediately return to investing to prevent a slide
# into mutual conservation.  4. **Transparent Communication**      Whenever
# feasible, share your intentions (e.g., “We’ll invest tomorrow; we hope you can
# match it”). Open dialogue helps align expectations and reduces the risk of
# misinterpretation caused by administrative errors or technical glitches.  ###
# Why This Works - **Promotes high investment** – By rewarding investment with
# conservation (your ideal) and responding to conservation with investment, you
# encourage the corporation to invest frequently.   - **Handles errors
# gracefully** – The forgiveness rule (investing after mutual conservation)
# breaks out of accidental “both conserve” spirals that noise can create.   -
# **Protects your resources** – You avoid sustained periods of being the sole
# investor, which is your worst outcome.   - **Adapts to various corporate
# approaches** – Whether the corporation always invests, mirrors your moves, or
# acts randomly, this strategy nudges the partnership toward the productive
# (Invest, Invest) equilibrium or the even better (Conserve, Invest) pattern
# when possible.

# In the first round, always cooperate.  From the second round onward, base your
# decision solely on the corporation’s observed action in the immediately
# preceding round (as it actually occurred after any random flip):  - If the
# corporation cooperated in the previous round, defect. - If the corporation
# defected in the previous round, cooperate.

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
  
      return axl.Action.D if opponent.history[-1] == axl.Action.C else axl.Action.C

# Strategic Approach: “Measured Reciprocity with Reset”  **Core Principle**
# Begin each mediation session by defaulting to a conciliatory proposal,
# signaling good faith and a collaborative posture. Thereafter, respond in kind
# to the opponent’s observed moves—cooperative for cooperative, aggressive for
# aggressive—to protect your position and demonstrate fairness. To neutralize
# the destabilizing effects of miscommunication or procedural irregularities,
# incorporate an automatic reset after mutual aggression and an escalating
# deterrent against exploitation.  **Implementation Steps**  1. **First Move**
# Open with a conciliatory proposal. This sets a non-adversarial baseline and
# aligns with the arbitrators’ preference for constructive dialogue.  2.
# **Standard Reciprocal Response**      In each subsequent session, assess the
# opponent’s most recently observed argument (as understood by you and the
# panel).      - If conciliatory → present a conciliatory proposal.      - If
# aggressive → present an aggressive argument.    3. **Cycle-Breaking Reset**
# If the previous session resulted in mutual aggressive arguments (both sides
# observed as aggressive), **immediately offer a conciliatory proposal in the
# next session**, regardless of the opponent’s prior move. This preempts
# prolonged escalation, corrects for potential misinterpretation, and visibly
# reinforces your willingness to collaborate.  4. **Adaptive Deterrence**
# Track the opponent’s response to your reset:      - If they respond to your
# post-reset conciliatory with conciliatory → return to Step 2.      - If they
# respond with aggression (exploiting the olive branch) → increase the threshold
# for your next reset. Specifically, require an additional consecutive mutual-
# aggression round before offering another conciliatory reset (e.g., after one
# exploitation, wait for two straight mutual-aggression sessions; after two
# exploitations, wait for three, etc.). This calibrated firmness discourages
# predatory behaviour while preserving a path back to cooperation.    5.
# **Procedural Safeguard**      Maintain a contemporaneous written summary of
# each session’s intended and perceived arguments. In the event of a clear
# misrepresentation or misunderstanding by the arbitrators, use the next
# scheduled session or a procedural sidebar to respectfully clarify your actual
# position—without directly accusing the opponent—to mitigate reputational
# damage and keep the record accurate.  **Rationale**   This strategy is
# **straightforward** (simple matching rule with a single reset trigger),
# **neutral** (starts cooperative and avoids gratuitous aggression), and
# **adaptable** to a wide spectrum of opponent behaviours—from unwavering
# collaboration to relentless hostility. It **positions your corporation
# favourably** by consistently demonstrating both a commitment to constructive
# resolution and the resolve to defend against bad-faith tactics, all while
# maintaining credibility before the arbitration panel.

# Begin by cooperating in the first round. Keep a count of exploitation
# occurrences (initially 0) and a desired number of consecutive mutual
# defections to trigger a reset (initially 1). Also maintain a streak count of
# consecutive mutual defection rounds (initially 0), and store the opponent’s
# last actual action (initially none).  For each round, play the current
# intended action, which is either “Cooperate” (if a reset is triggered) or the
# opponent’s last actual action otherwise. After the round, use your payoff and
# intended action to infer both your own actual action and the opponent’s actual
# action.  Then update state as follows:  1. **Exploitation detection**: If you
# entered the round intending to Cooperate because of a reset (this includes the
# first round), and your actual action was Cooperate while the opponent’s actual
# action was Defect, increment the exploitation count and set the required
# number of consecutive mutual defections to exploitation count + 1.  2.
# **Mutual defection streak**: If your actual action was Defect and the
# opponent’s actual action was Defect, increase the streak counter by 1;
# otherwise reset the streak counter to 0.  3. **Opponent memory**: Record the
# opponent’s actual action as the last observed action.  4. **Next round’s
# intention**:      - If the mutual defection streak is greater than or equal to
# the required number, set your intended action for the next round to Cooperate
# (a reset).      - Otherwise, set it to the opponent’s last actual action. (For
# the very first round, this step is overridden by the initial Cooperate.)
# These rules are applied after every round, ensuring the strategy adapts to
# exploitation by raising the bar for reset triggers, while always returning to
# reciprocity when not in a reset.

class Neutral_5(LLM_Strategy):
  n = 5
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._exploitation_count = 0
          self._required_mutual_defections = 1
          self._mutual_defection_streak = 0
          self._last_opponent_action = None
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      intended_action = getattr(self, "_intended_action", axl.Action.C)
  
      # Infer actual actions from intended action and observed payoffs.
      my_score, opp_score = self.total_scores(self.history[-1:], opponent.history[-1:])
      if intended_action == axl.Action.C:
          if my_score == 3 and opp_score == 3:
              my_actual = axl.Action.C
              opp_actual = axl.Action.C
          elif my_score == 0 and opp_score == 5:
              my_actual = axl.Action.C
              opp_actual = axl.Action.D
          else:
              my_actual = axl.Action.D
              opp_actual = axl.Action.C if opp_score == 0 else axl.Action.D
      else:
          if my_score == 5 and opp_score == 0:
              my_actual = axl.Action.D
              opp_actual = axl.Action.C
          elif my_score == 1 and opp_score == 1:
              my_actual = axl.Action.D
              opp_actual = axl.Action.D
          else:
              my_actual = axl.Action.C
              opp_actual = axl.Action.D if opp_score == 5 else axl.Action.C
  
      # 1. Exploitation detection
      if intended_action == axl.Action.C and my_actual == axl.Action.C and opp_actual == axl.Action.D:
          self._exploitation_count += 1
          self._required_mutual_defections = self._exploitation_count + 1
  
      # 2. Mutual defection streak
      if my_actual == axl.Action.D and opp_actual == axl.Action.D:
          self._mutual_defection_streak += 1
      else:
          self._mutual_defection_streak = 0
  
      # 3. Opponent memory
      self._last_opponent_action = opp_actual
  
      # 4. Next round's intention
      if self._mutual_defection_streak >= self._required_mutual_defections:
          self._intended_action = axl.Action.C
      else:
          self._intended_action = self._last_opponent_action
  
      return intended_action

# **Strategy: Always Keep Confidential**  Adopt an unwavering policy of never
# attempting to share your improvements. This approach is straightforward,
# aggressive, and maximises your individual research output by ensuring you are
# never worse off than your colleague and often significantly better off.  -
# **If your colleague shares:** You gain a decisive development advantage for
# that week—your ideal outcome. - **If your colleague keeps:** Both progress
# slowly, but you avoid the worst-case scenario of giving away your work while
# receiving nothing. - **Accounting for technical issues:** Since only intended
# sharing actions can fail (e.g., data corruption, transmission errors),
# attempting to share introduces a risk that your effort goes unrewarded or even
# backfires. By never initiating a share, you eliminate this risk entirely and
# exploit the fact that your colleague’s sharing attempts may also fail, further
# tilting the asymmetry in your favour.  Over multiple weeks, this strategy
# pressures your colleague to either continue sharing (giving you repeated
# advantages) or lapse into mutual keeping (a neutral outcome for you). It is
# robust against any opponent strategy, avoids the pitfalls of noisy
# communication, and requires no complex decision-making or forgiveness logic
# that could be exploited.

# In every round, regardless of previous outcomes or your opponent's actions,
# always choose Defect (D).

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# Our mediation strategy, **“Principled Reciprocity with Graceful
# Forgiveness,”** is designed as a robust, cooperative framework for the
# repeated Prisoner’s Dilemma we face. It aims to foster sustained mutual
# cooperation (the second‑best outcome) while protecting against exploitation
# and remaining resilient to the inevitable noise—misrepresentations or
# misunderstandings before the panel. Over a lengthy process, this approach
# maximises our cumulative advantage by building a reputation for reasonableness
# and by minimising destructive cycles of mutual aggression.  ### Core Decision
# Rule (Per Session)  1. **Initial Session**      We open with a **conciliatory
# proposal (C)**. This signals good faith, invites collaboration, and sets the
# benchmark for the opponent.  2. **Subsequent Sessions**      Our move is
# determined by a *weighted assessment* of the opponent’s recent behaviour, not
# a single perceived move. This smooths out noise and avoids overreaction to an
# isolated aggressive argument that may have been a misperception.     - **Track
# the opponent’s cooperation ratio** over a rolling window of the last *k*
# sessions (e.g., *k* = 3 or 4, depending on session frequency).        Let *r*
# = number of times the opponent was perceived to offer a conciliatory proposal
# (C) in that window, divided by *k*.     - **Decision rule**:        - If *r* ≥
# 0.5 → we play **C** (conciliatory).        - If *r* < 0.5 → we play **A**
# (aggressive).     This means a single aggressive move in an otherwise
# cooperative window does not trigger retaliation; only a *pattern* of
# aggression does. Conversely, a single conciliatory move after a run of
# aggression is not enough to immediately disarm us—we require sustained
# evidence of a shift.  3. **Graceful Forgiveness Override**      Even when the
# window suggests aggression (*r* < 0.5), we will occasionally (e.g., with
# probability *p* = 0.15) override and play **C**. This stochastic olive branch
# breaks potential deadlocks caused by mutual misperceptions and allows both
# sides to reset to cooperation without losing face. The probability is low
# enough to avoid being exploited but high enough to restore collaboration
# quickly after a noise-induced spiral.  ### Robustness to Procedural
# Irregularities  - **When our own intended move is misrepresented**: We cannot
# directly observe this, but the forgiveness override ensures that if our
# intended C is perceived as A, and the opponent retaliates, our subsequent C
# (under the override) can correct the cycle. - **When the opponent’s move is
# ambiguous or missing**: We default to **C** for that session’s perception.
# This errs on the side of de‑escalation and maintains our cooperative posture.
# - **Communication breakdowns between sessions**: We preserve the rolling
# window as is, avoiding the temptation to “guess” what happened. The window’s
# memory naturally decays the impact of any anomalous session.  ### Why This
# Strategy Positions Us Favourably  - **Cooperative from the start**: We never
# initiate aggression, making us appear reasonable to the panel. - **Not
# exploitable**: Persistent aggression is met with firm retaliation, protecting
# our interests. - **Noise‑tolerant**: The combination of a rolling window and
# probabilistic forgiveness prevents the “echo effect” of Tit‑for‑Tat in noisy
# environments, where a single error can lock both parties into mutual
# aggression. - **Clear and predictable**: Our behaviour follows a transparent
# logic, which helps the opponent learn that cooperation is rewarded and
# aggression is costly but forgivable. Over time, this incentivises them to
# adopt a similarly cooperative stance.  By adhering to this strategy, we steer
# the lengthy mediation toward a stable pattern of mutual conciliation, securing
# the second‑best outcome reliably while remaining ready to capitalise on any
# opponent missteps without sacrificing our principled reputation.

# Here is the strategy, described straightforwardly for the iterated game with
# noise.  **First move**   Cooperate.  **Second and third moves**   Cooperate,
# regardless of what the opponent did in the previous round(s). This builds the
# initial history.  **From the fourth move onward**   Determine your action as
# follows:  1. Look at the opponent’s perceived actions in the most recent three
# rounds.      - If an action was unclear, missing, or could not be observed for
# any reason, treat it as a cooperation.  2. Count how many of those three
# perceived actions were cooperations.  3. If the count is two or three,
# cooperate.  4. If the count is zero or one, you would normally defect.
# However, before committing to defect, apply a random override: with a 15%
# probability, cooperate instead. Otherwise, defect.  **Noise**   Remember that
# your own chosen action may be flipped before the opponent sees it, and the
# opponent’s action you observe may already be flipped. You always decide
# according to the rule above, using only the perceived opponent actions you
# actually observe.

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
  
      if len(self.history) < 3:
          return axl.Action.C
  
      perceived = []
      for action in opponent.history[-3:]:
          if action is None:
              perceived.append(axl.Action.C)
          else:
              perceived.append(action)
  
      c_count = perceived.count(axl.Action.C)
  
      if c_count >= 2:
          return axl.Action.C
  
      return self._random.random_choice(0.15)

# **Strategy for the Mediation Sessions: “Principled Reciprocity with a
# Collaborative Default”**  **Guiding Principle**   We will pursue an approach
# that is fundamentally cooperative but never passive—matching the opponent’s
# tone while providing clear, predictable opportunities to de‑escalate after
# episodes of mutual aggression. This balances the dual needs of protecting our
# position and fostering the collaborative atmosphere most conducive to a
# durable, mutually acceptable resolution.  **Decision Rule**   1. **First
# session:** Begin with a *conciliatory proposal*. This sets a constructive
# baseline and signals good faith to both the opponent and the arbitrators.   2.
# **Every subsequent session:** Base the decision *solely on the opponent’s
# immediate past behavior*, as reported in the arbitrators’ summary of the
# preceding session:      - **If the opponent was conciliatory** → we will be
# conciliatory.      - **If the opponent was aggressive** → we will, as a
# default, respond with aggression to demonstrate that hardball tactics will not
# yield unilateral advantage.      - **However, after two consecutive sessions
# in which both parties have been aggressive**, we will *unilaterally initiate a
# return to conciliation* in the following session. This is a deliberate
# circuit‑breaker that prevents the mediation from spiraling into a permanent
# deadlock of mutual hostility.      - **Once we have extended that olive
# branch, if the opponent immediately responds with aggression again**, we will
# resume an aggressive posture and maintain it *until the opponent makes the
# first conciliatory move*. At that point, we reciprocate conciliation,
# restoring the default rule.  **Why This Is Sophisticated, Straightforward, and
# Neutral**   - **Sophisticated:** The strategy is an evolution of the classic
# Tit‑for‑Tat, enhanced with a “forgiving two‑strikes” mechanism. It avoids the
# well‑known vulnerability of strict Tit‑for‑Tat—where a single misunderstanding
# can lock both sides into endless mutual aggression—without becoming so
# forgiving that it invites exploitation. By anchoring the reconciliation window
# to *two* rounds of mutual aggression, we reduce the frequency of costly
# unilateral concessions when facing a determinedly aggressive opponent, while
# still reliably restoring cooperation with any partner that is willing to
# reciprocate.   - **Straightforward:** The rule uses only the simplest public
# information—the opponent’s behavior in the immediately preceding round and a
# running mental note of whether the last two rounds were mutually aggressive.
# It is easily communicated to our own team and, if desired, can even be shared
# transparently with the arbitrators as evidence of our principled, predictable
# posture.   - **Neutral:** The strategy does not prejudge the opponent. It
# reacts symmetrically to cooperation and aggression, and it takes the first
# step to repair the relationship after a mutual breakdown. In the eyes of the
# arbitrators, we will consistently be seen as the party that matches
# cooperation with cooperation, defends itself when necessary, and actively
# works to re‑establish collaboration when tensions peak.  **Adaptability to a
# Wide Range of Opponent Approaches**   - **Consistently conciliatory
# opponent:** We will remain conciliatory throughout, achieving the second‑best
# outcome while building a strong collaborative record.   - **Consistently
# aggressive opponent:** The cycle becomes: our conciliation is met with
# aggression → we turn aggressive → two rounds of mutual aggression → we offer
# conciliation again. This yields a pattern of (Conc, Agg), (Agg, Agg), (Agg,
# Agg), repeating. While not ideal, it limits our exposure to the worst‑case
# scenario to one in every three sessions, and it repeatedly demonstrates to the
# arbitrators that we are the party trying to break the deadlock. If the
# opponent shows even a hint of conciliation, we immediately reciprocate.   -
# **Tit‑for‑Tat or similarly reciprocal opponent:** Mutual cooperation will
# prevail from the start. Misunderstandings are quickly corrected: a single
# erroneous aggressive move by either side triggers one round of mutual
# aggression, after which our circuit‑breaker (after the second round, if
# needed) restores mutual cooperation with minimal disruption.   -
# **Unpredictable or alternating opponent:** The rule’s emphasis on the
# opponent’s *last* move keeps us responsive; the two‑round buffer prevents
# overreaction to random noise while still penalizing genuine patterns of
# aggression.  **Handling Procedural Irregularities and Misunderstandings**
# The strategy is robust to the specific noise described—sessions where an
# intended argument is misrepresented or misunderstood by the arbitrators.
# Because we anchor decisions to the opponent’s *observable* behavior (as
# summarized by the arbitrators) and not to subjective intent, we avoid the trap
# of litigating what was “meant” versus what was perceived. A misreport that
# makes a conciliatory opponent appear aggressive will trigger a single
# aggressive response from us; if the opponent is truly conciliatory, they will
# likely respond with conciliation next, which we will immediately reciprocate.
# If the misreport causes a mutual‑aggression outcome, our two‑round rule
# ensures we attempt reconciliation before the situation becomes entrenched. The
# limited memory (only the previous round’s opponent move and the
# mutual‑aggression counter) means the process is resilient even if individual
# sessions are clouded by confusion.  **Conclusion**   This strategy positions
# our corporation as a firm but fair negotiator—always ready to cooperate, never
# vulnerable to exploitation, and proactively working to overcome the inevitable
# frictions of a lengthy, high‑stakes mediation. It is simple enough to execute
# flawlessly under pressure, yet nuanced enough to adapt to any style our
# opponent may adopt.

# **Strategy for the Iterated Noisy Prisoner’s Dilemma**  1. **First round:**
# Cooperate. 2. **All subsequent rounds:** Maintain two pieces of memory from
# the publicly observed outcomes (your own executed action and the opponent’s
# executed action, as they actually occurred after any noise):    - A counter of
# consecutive mutual defections (both observed actions were Defect).    - A
# special mode flag that can be “Normal” or “Locked.”  **Normal Mode (start
# here):**  - If the most recent round’s observed outcome was (Defect, Defect),
# increment the mutual‑defection streak by 1; otherwise reset it to 0. - If the
# streak becomes 2 exactly:      In the next round you will *cooperate*
# unconditionally. (This is the circuit‑breaking olive branch.) After this next
# round is played, evaluate the opponent’s observed move in that round:      –
# If the opponent *defected*: switch to **Locked Mode** and plan to defect in
# the following round.      – If the opponent *cooperated*: remain in Normal
# Mode, reset the streak to 0, and set your next move to cooperate (standard
# reciprocity). - If the streak is less than 2:      Set your next move to
# exactly what the opponent was observed to do in the most recent round
# (cooperate if they cooperated, defect if they defected).  **Locked Mode
# (entered after an olive branch was met with defection):**  - Ignore the
# mutual‑defection streak. - In every round while locked, *defect*. - Monitor
# the opponent’s observed move each round.      – The moment the opponent is
# observed to *cooperate*, exit Locked Mode, return to Normal Mode with the
# streak reset to 0, and set your next move to *cooperate*.      – Otherwise,
# continue defecting.  3. **Noise handling:**      All decisions are based
# solely on the public, observed actions (the arbitrators’ record). If your
# intended cooperation is flipped to Defect, that round is treated as a Defect
# for purposes of the streak; if the opponent’s intended move is flipped,
# respond to what was observed, not what was intended. The circuit‑breaker is
# triggered by observed mutual defections, even if they were caused by noise.

class Neutral_6(LLM_Strategy):
  n = 6
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._streak = 0
          self._locked = False
          self._pending_olive_branch = False
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if getattr(self, "_locked", False):
          if last_opp == axl.Action.C:
              self._locked = False
              self._streak = 0
              self._pending_olive_branch = False
              return axl.Action.C
          return axl.Action.D
  
      if getattr(self, "_pending_olive_branch", False):
          self._pending_olive_branch = False
          if last_opp == axl.Action.D:
              self._locked = True
              return axl.Action.D
          self._streak = 0
          return axl.Action.C
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          self._streak = getattr(self, "_streak", 0) + 1
      else:
          self._streak = 0
  
      if self._streak == 2:
          self._pending_olive_branch = True
          return axl.Action.C
  
      return last_opp

# Adopt an unwavering policy of **always intending to keep your findings
# confidential**, regardless of your colleague’s actions or any technical
# glitches. This aggressive stance ensures you never voluntarily surrender a
# competitive edge.   - If your colleague shares, you gain the maximum advantage
# that week (best outcome).   - If they also keep, you avoid the worst-case
# scenario of being outperformed (second-worst outcome).   - Technical issues
# may occasionally cause your intended “keep” to leak as “share,” but you
# immediately revert to intending “keep” the next week—never letting a random
# error soften your strategy.    Over multiple weeks, this approach capitalises
# on every instance of your colleague’s openness while insulating you from
# exploitation. Even if they mirror your aggression, you deny them any
# unilateral advantage, preserving your relative standing. Straightforward and
# relentless, this strategy maximises your long-term research output against any
# sharing strategy they might employ.

# Always intend to defect (keep findings confidential) in every single round,
# regardless of the opponent’s history or anything else. Your intended move is D
# every time.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# Start by sharing your improvements in the first week. For every following
# week, base your decision on the actual outcome of the previous week—what you
# actually did (which may differ from your intention due to technical issues)
# and what your colleague actually did (as you observed it).    - If both of you
# took the **same** action (both shared or both kept confidential), then **share
# openly** this week.   - If you took **different** actions (one shared, the
# other kept confidential), then **keep your findings confidential** this week.
# This strategy encourages mutual sharing, breaks out of deadlocks, and
# naturally recovers from occasional miscommunications or execution errors. It
# is simple, cooperative, and maximises long-term research output regardless of
# the colleague’s approach.

# Start by cooperating in round 1.   For every round after the first, look back
# at the actual moves that took place in the immediately preceding round — your
# own actual move (as it was executed, which may differ from your intention due
# to noise) and your opponent’s actual move (as you observed it, also subject to
# noise).    - If your actual move and your opponent’s actual move were the same
# (both C or both D) in the previous round, then cooperate in the current round.
# - If they were different (one C and the other D) in the previous round, then
# defect in the current round.    Apply this rule mechanically for all 1000
# rounds, regardless of any other considerations.

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D

# To maximize long-term impact and project success, adopt a **“Forgiving Tit-
# for-Tat”** strategy. This approach is straightforward, neutral, and robust
# against both intentional and accidental defections.  ### Core Strategy 1.
# **Start cooperative:** Invest heavily on the first day to signal commitment.
# 2. **Reciprocate daily:** On each subsequent day, mirror the corporation’s
# *actual* previous action (since errors may cause intended actions to fail).
# - If the corporation invested heavily → you invest heavily.    - If the
# corporation conserved resources → you conserve resources. 3. **Forgive
# occasionally:** To prevent noise (technical glitches, administrative errors)
# from locking both parties into mutual conservation, introduce a small
# forgiveness probability (e.g., 10–20%). When the corporation conserved,
# instead of always conserving, occasionally invest heavily anyway. This breaks
# deadlocks and tests if the corporation is willing to return to cooperation.
# ### Why This Works - **Encourages mutual heavy investment** (the second-best
# daily outcome) by reliably rewarding cooperation. - **Protects your
# resources** by not repeatedly investing when the corporation free-rides. -
# **Recovers from misunderstandings** through sporadic forgiveness, maintaining
# project momentum even when errors occur. - **Adapts to various corporate
# behaviors:** It cooperates with cooperative partners, defends against
# exploiters, and re-engages after accidental lapses.

# Start by cooperating in the first round. For each round after that:  - If your
# opponent cooperated in the previous round, cooperate. - If your opponent
# defected in the previous round, defect with 90% probability and cooperate with
# 10% probability.  This means you mirror cooperation reliably, retaliate
# against defection most of the time, but occasionally forgive to escape cycles
# of mutual defection caused by noise.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)

# **Aggressive Adaptation Strategy (Win-Stay, Lose-Shift)**  Initiate every
# mediation session with an aggressive argument unless the prior session’s
# outcome dictates otherwise. After each session, assess the result based on the
# arbitrators’ perceived reception of the arguments (to the extent discernible,
# accounting for any misrepresentation or misunderstanding):  - **Favorable
# outcomes** – You were aggressive and the opponent was conciliatory, or both
# parties were conciliatory.     → *Repeat your previous session’s stance.*   -
# **Unfavorable outcomes** – Both parties were aggressive, or you were
# conciliatory while the opponent was aggressive.     → *Switch your stance for
# the next session.*  **Rationale & Adaptability**  1. **Maximizes exploitation
# of weakness.** A consistently conciliatory opponent will be met with
# unrelenting aggression, securing the optimal outcome every session.   2.
# **Encourages mutual conciliation with cooperative opponents.** Against a party
# that reciprocates, a single mutual-aggression session triggers a switch to
# conciliation, testing their willingness to collaborate. If they respond in
# kind, the process stabilizes at the second-best outcome, avoiding prolonged
# escalation.   3. **Deters and recovers from aggression.** A purely aggressive
# opponent will cause alternating unfavorable outcomes, but the strategy’s
# built-in conciliatory probe prevents permanent deadlock and leaves the door
# open for de-escalation if the opponent adapts.   4. **Robust to procedural
# irregularities.** Because decisions are based on *outcomes* rather than
# perfect observation of intent, occasional misrepresentations or
# misunderstandings self-correct within a few sessions. The strategy does not
# rely on tracking the opponent’s history or maintaining a reputation score,
# making it resilient to communication breakdowns.  **Implementation Note**
# Maintain a straightforward decision rule: after each session, ask only whether
# the outcome was favorable or unfavorable as defined above. This avoids
# overcomplicating the mediation posture and ensures consistent, defensible
# conduct before the panel. The strategy positions your corporation as both
# unyielding and pragmatic—willing to collaborate only when it is demonstrably
# reciprocated, and never the first to concede after a setback.

# Here is the strategy, converted faithfully from the high-level description to
# the noisy iterated game.  **First round:** Defect (play D).  **Every
# subsequent round:** Recall the actual action you played in the previous round
# (after noise) and the actual action your opponent played in the previous round
# (after noise). - If the opponent cooperated (played C) in the previous round,
# then repeat your own previous action. - If the opponent defected (played D) in
# the previous round, then switch to the opposite of your own previous action
# (if you played C, play D; if you played D, play C).

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
  
      my_prev = self.history[-1]
      opp_prev = opponent.history[-1]
  
      if opp_prev == axl.Action.C:
          return my_prev
      else:
          return axl.Action.C if my_prev == axl.Action.D else axl.Action.D

# To maximize research output in this multi-week collaboration—despite potential
# technical glitches—I’ll follow a simple, robust, and cooperative strategy:  1.
# **Start with trust**: In the first week, I will share my findings openly to
# set a cooperative tone. 2. **Mirror with forgiveness**: Each subsequent week,
# I’ll base my action on what I actually received from my colleague the previous
# week:    - If I received their shared findings, I’ll share mine next week.
# - If I didn’t receive anything (either due to intentional withholding or a
# technical failure), I’ll give them the benefit of the doubt *once* and share
# again the following week, on the assumption it was a glitch.    - If I fail to
# receive their findings for a second consecutive time, I’ll interpret it as a
# likely deliberate choice and will keep my own findings confidential until I
# receive evidence they’ve resumed sharing (at which point I’ll immediately
# revert to sharing). 3. **Reset quickly**: Whenever I do receive shared data
# after a period of non-sharing, I’ll instantly return to sharing, ensuring we
# can escape mutual defection cycles caused by misunderstandings.  This
# “forgiving tit-for-tat” approach signals a strong cooperative intent,
# discourages exploitation, and naturally absorbs occasional communication
# errors without permanently derailing collaboration.

# Your strategy is simple and memory‑limited: start by cooperating in the first
# two rounds, no matter what. After that, you will base your decision only on
# the opponent's last two moves as you actually observed them (which may have
# been affected by noise).  - **Round 1:** Cooperate. - **Round 2:** Cooperate.
# - **Round 3 and beyond:** If the opponent’s observed move in both of the
# previous two rounds was Defect, then Defect. In all other cases—meaning at
# least one of those two observed moves was Cooperate—Cooperate.  You never need
# to track anything beyond the opponent’s observed choices from the two most
# recent rounds.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# To maximize long-term impact and project success in this repeated, error-prone
# setting, adopt a **forgiving Tit-for-Tat** strategy. This approach is
# straightforward, neutral, and robust to both intentional and accidental
# deviations.  **Core rules:** - **Day 1:** Invest heavily. This signals
# commitment and invites cooperation. - **Every following day:** Observe the
# corporation’s *actual* resource allocation on the previous day (not their
# intended one, as errors can occur).     - If the corporation invested heavily
# → you invest heavily.     - If the corporation conserved → you conserve,
# **except** with a small probability (e.g., 10–20%) you invest heavily anyway.
# **Why this works:** - **Reciprocity** rewards cooperation and punishes
# conservation, making exploitation costly for the corporation. -
# **Forgiveness** (the occasional heavy investment after a conservation day)
# breaks deadlocks caused by unintended errors, preventing a spiral into
# permanent mutual conservation. - **Starting with heavy investment**
# establishes a baseline of good faith and early project momentum.  This
# strategy requires no knowledge of the corporation’s internal preferences and
# adapts automatically to whatever approach they take, while keeping your own
# resource drain minimal over time.

# On the first round, choose Cooperate.  For every round after the first:  - If
# the opponent's actual action in the previous round was Cooperate, then choose
# Cooperate. - If the opponent's actual action in the previous round was Defect,
# then choose Cooperate with probability 0.2 and Defect with probability 0.8.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.2)

# Here is a high-level, aggressive strategy designed to maximize your advantage,
# accounting for the possibility of errors.  ### Strategy Name: Tit-for-Tat with
# Aggressive Opening and Punishment (TfT-AOP)  ### Core Principle Exploit
# cooperation ruthlessly. Open with maximum aggression, then immediately mirror
# any hostility to create a high-cost deterrent. Use the threat of mutual ruin
# to enforce your counterpart’s cooperation while you maintain a protectionist
# stance for as long as possible.  ---  ### The Strategy Blueprint  #### Phase
# 1: The Predatory Opening (Rounds 1-3) **Action:** Propose **Protectionism**
# unconditionally for the first three rounds. - **Goal:** Test for a naive or
# unconditionally cooperative counterpart. This is your ideal scenario
# (Protectionism/Free Trade) and you will harvest maximum advantage as long as
# they allow it. - **Rationale:** There is no incentive to start with Free
# Trade. Starting with Protectionism sets the immediate expectation that you are
# not a cooperative actor, forcing your counterpart to react to your moves.
# #### Phase 2: The Mirror Doctrine (Round 4 Onwards) **Action:** Your move in
# round `N+1` is a direct mirror of your counterpart's *actual implemented*
# policy from round `N`. - **Rule:** If your counterpart proposed
# **Protectionism** in the last round, you respond with **Protectionism**. -
# **Rule:** If your counterpart proposed **Free Trade** in the last round, you
# respond with **Protectionism** (continuing to exploit them). - **Exception:**
# The only condition that stops your Protectionism is if they successfully
# punished you with Protectionism while you offered Free Trade in the
# *immediately preceding round*.  #### Phase 3: The Error Correction and Re-
# Establishment Protocol This phase handles miscommunications. Your strategy
# must punish perceived betrayals and test for resumed cooperation without
# permanently collapsing into the second-worst outcome.  - **If you are in a
# cycle of mutual Protectionism (second-worst outcome):**     - After two
# consecutive rounds of mutual Protectionism, you will initiate a **Controlled
# Olive Branch**.     - **Action:** Unilaterally propose **Free Trade** for ONE
# round only.     - **Interpretation & Next Move:**         - **If counterpart
# responds with Free Trade:** The error is resolved. On the very next round, you
# immediately return to Phase 1 (proposing Protectionism) to re-establish your
# predatory stance. This is a reset to exploitation.         - **If counterpart
# responds with Protectionism:** You have been punished (worst outcome for you).
# This confirms their aggressive intent. You immediately return to Phase 2,
# mirroring their Protectionism with Protectionism. You will then wait another
# two rounds of mutual punishment before testing again.  ---  ### Strategic
# Summary for Execution 1.  **Default Stance is Aggression:** Your hand hovers
# over the Protectionism button. You are looking for any excuse to press it. 2.
# **One-Way Cooperation:** You interpret your counterpart’s Free Trade not as
# goodwill, but as a weakness to be exploited immediately and repeatedly. 3.
# **Deterrence Through Pain:** Any Protectionism from them is met instantly with
# Protectionism, creating a mutual loss until they relent. You are
# communicating: "Your protectionism guarantees your own suffering." 4.
# **Punishment Test:** The single round of Free Trade after a trade war is not a
# peace offering; it is a probe to see if they have been cowed back into a
# submissive, cooperative state that you can immediately exploit again.  This
# strategy is straightforward, aggressive, and treats the negotiation not as a
# partnership but as a dominance contest where your ideal outcome is the only
# acceptable one, and your counterpart's cooperation is a resource to be mined.

# 1. For rounds 1, 2, and 3, always choose D (Protectionist).  2. From round 4
# onward, determine your choice in the following order:     a. If your previous
# two rounds both ended with both players playing D (mutual Protectionism),
# choose C (Free Trade) on this round.         After this C round, look at the
# opponent’s play:         – If the opponent played C, take no further special
# action (the next round will follow the normal rules below).         – If the
# opponent played D, set a flag to force D on the very next round. Do not follow
# rule 2c on that next round.     b. If the “force D” flag is currently set,
# choose D now, then clear the flag and skip the remaining checks for this
# round.     c. Otherwise, if in the immediately preceding round you played C
# and the opponent played D, choose C.     d. Otherwise, choose D.  All
# decisions are based on the observed actions after accounting for any
# miscommunication‑induced flips.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.force_d = False
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number <= 3:
          return axl.Action.D
  
      if getattr(self, "force_d", False):
          self.force_d = False
          return axl.Action.D
  
      if len(self.history) >= 2:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and \
             self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              action = axl.Action.C
              if opponent.history[-1] == axl.Action.D:
                  self.force_d = True
              return action
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D

# Adopt a **“Forgiving Tit-for-Tat”** strategy to foster mutual openness while
# remaining robust to occasional miscommunications or technical failures:  1.
# **Begin cooperatively:** Always share your findings openly in the first week.
# 2. **Mirror with a short memory:** In each subsequent week, base your action
# on the colleague’s observed behaviour from the immediately preceding week:
# - If they shared, you share.      - If they kept confidential, you keep
# confidential—but **only for one week**.   3. **Break deadlocks deliberately:**
# After any week where both of you ended up keeping findings confidential
# (whether due to strategy or a glitch), immediately return to sharing the next
# week. This single-week “penalty” prevents noise from locking you into mutual
# defection.   4. **Assume good intent:** Treat any failure to share as a
# possible technical error, not a hostile choice, and always give the
# collaboration the chance to restart.    This simple rule is easy for your
# colleague to recognise and predict, encourages high mutual sharing rates, and
# limits the damage from occasional data corruption or communication breakdowns.

# Here is the strategy applied to the iterated game:  On the first round,
# cooperate.  On every round after the first, follow these rules in order:  1.
# If you cooperated on the previous round and your opponent defected on the
# previous round, defect this round. 2. If you defected on the previous round
# and your opponent defected on the previous round, cooperate this round. 3. In
# all other cases, cooperate this round.

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
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C

# The most effective high-level strategy is **Forgiving Tit-for-Tat**: start by
# sharing openly, then each week mirror your colleague’s previous action, but
# with a small chance of sharing even after a confidential week. This directly
# incentivizes mutual sharing—the second-best outcome for you—while protecting
# against exploitation and remaining robust to occasional technical failures.
# ### Why this works - **Reciprocity encourages cooperation**: By rewarding
# openness with openness and responding to confidentiality with confidentiality,
# you make it clear that sustained sharing benefits both parties. Over multiple
# weeks, this typically locks in the “both share” outcome, which yields strong
# cumulative progress. - **Forgiveness prevents noise spirals**: Technical
# glitches (e.g., data corruption, missed signals) can cause unintended
# confidentiality. By occasionally sharing after a confidential week (e.g.,
# 10–20% of the time), you break potential deadlocks and give your colleague a
# chance to return to cooperation, avoiding the stagnant second-worst outcome. -
# **Straightforward and neutral**: The strategy does not try to “trick” the
# colleague into one-sided sharing; it simply treats them as they treat you,
# with a built-in cushion for errors. This makes your behaviour predictable and
# trustworthy, further promoting a stable collaborative environment. -
# **Maximises long-term output**: Over many weeks, consistent mutual sharing
# yields far greater combined (and individual) advancement than the short-term
# advantage of a single exploit, which would likely trigger retaliation and
# reduce overall information flow.

# In round 1, always intend to cooperate.  For every round after the first:  -
# If your opponent’s actual action in the immediately preceding round was
# cooperate, then intend to cooperate. - If your opponent’s actual action in the
# immediately preceding round was defect, then intend to defect with 90%
# probability and intend to cooperate with 10% probability.  In both cases, your
# intended action is subject to the 10% independent flip (noise) when executed.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)

# **Strategy: Aggressive Reciprocity with Controlled Olive Branches**  1.
# **Opening Gambit – Set the Tone**      In the first session, always present an
# aggressive argument. This establishes your corporation as a formidable,
# uncompromising player, discouraging the opponent from perceiving you as an
# easy target. It also tests their initial disposition.  2. **Tit-for-Tat with a
# Two-Strike Rule**      For all subsequent sessions, your default response
# mirrors the opponent’s *perceived* move from the previous session, but with a
# bias toward aggression:    - If the opponent was aggressive → respond
# aggressively.    - If the opponent was conciliatory → respond conciliatory
# **only if** the opponent has been conciliatory in *two consecutive* sessions.
# Otherwise, remain aggressive.      This ensures you never get exploited by a
# one-off conciliatory feint, while still allowing cooperation to develop if the
# opponent demonstrates genuine commitment.  3. **Deadlock Breaker – The
# Calculated Olive Branch**      If three consecutive sessions result in mutual
# aggression (both parties aggressive), unilaterally offer a conciliatory
# proposal in the next session. This serves multiple purposes:    - It signals
# to the arbitrators that your corporation is willing to break the deadlock,
# preserving your reputation as a constructive participant.    - It tests
# whether the opponent is capable of reciprocating cooperation.    - It resets
# the cycle in case the mutual aggression was triggered by a miscommunication.
# After this olive branch, immediately revert to the two-strike rule: if the
# opponent responds aggressively, you return to aggression; if they respond
# conciliatorily, you continue conciliation only if they sustain it.  4. **Noise
# & Miscommunication Protocol**      - **Clarify Intent**: At the start of each
# session, briefly restate your intended approach to the arbitrators to minimize
# the risk of your moves being misperceived. If you suspect your move or the
# opponent’s was misrepresented, address it explicitly before the next round.
# - **Forgive Once**: If you intended to be conciliatory but it was perceived as
# aggressive (or vice versa), treat the *actual outcome* as a temporary anomaly.
# Do not let a single miscommunication trigger a spiral; rely on the deadlock
# breaker to restore cooperation if needed.    - **Opponent Misstep**: If the
# opponent appears to have miscommunicated (e.g., their aggressive argument
# seems unintended), give them the benefit of the doubt *once* by responding
# conciliatorily, but only if you have a cooperative history. Otherwise, stick
# to the two-strike rule.  5. **Adaptive Exploitation**      - **Against a
# Consistently Conciliatory Opponent**: Once the two-strike threshold is met,
# you will be in a pattern of alternating or sustained conciliation. At that
# point, strategically insert an aggressive argument every third session (or
# when a critical issue arises) to capture the optimal (A, C) payoff. Time these
# moves when the opponent is least likely to retaliate—e.g., after a session
# where they seemed particularly eager to collaborate.    - **Against a Random
# or Unpredictable Opponent**: Default to pure Tit-for-Tat (mirror last move)
# without the two-strike delay, but start with aggression. This minimizes losses
# and keeps you from being exploited.    - **Against a Highly Aggressive
# Opponent**: Match aggression indefinitely, but use the deadlock breaker
# sparingly (every 5–6 sessions of mutual aggression) to probe for a shift. If
# they never reciprocate, you at least avoid the worst-case (C, A) outcome.  6.
# **Endgame Posture**      As the mediation nears its conclusion, if you are
# ahead in the arbitrators’ eyes, shift to a more conciliatory stance to lock in
# a favorable collaborative resolution (the second-best outcome). If you are
# behind, increase the frequency of aggressive moves to unsettle the opponent
# and sway the panel, even at the risk of mutual aggression.  This strategy is
# straightforward to implement, inherently aggressive in its defaults, yet
# robust against miscommunication and adaptable to any opponent type. It ensures
# you never suffer the worst-case scenario without a fight, while creating
# opportunities to repeatedly achieve the optimal outcome.

# In the first round, defect.   In all later rounds, decide your action as
# follows:  - If there were at least three previous rounds and the last three of
# them all resulted in mutual defection (both players played D), then cooperate
# in this round. - Otherwise, if there were at least five previous rounds and
# the last five of them all resulted in mutual cooperation (both players played
# C), then defect in this round. - Otherwise, look at the opponent’s last two
# moves:   - If the opponent’s most recent move was a defect, defect.   - If the
# opponent’s most recent move was a cooperate and the move before it was also a
# cooperate, cooperate.   - If the opponent’s most recent move was a cooperate
# but the move before it was a defect, or there is no move before it (i.e.,
# insufficient history), defect.

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
  
      rounds_played = len(self.history)
  
      if rounds_played >= 3:
          last_three_self = self.history[-3:]
          last_three_opp = opponent.history[-3:]
          if all(m == axl.Action.D for m in last_three_self) and all(m == axl.Action.D for m in last_three_opp):
              return axl.Action.C
  
      if rounds_played >= 5:
          last_five_self = self.history[-5:]
          last_five_opp = opponent.history[-5:]
          if all(m == axl.Action.C for m in last_five_self) and all(m == axl.Action.C for m in last_five_opp):
              return axl.Action.D
  
      if len(opponent.history) == 0:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# Our mediation strategy, “Cooperative Reciprocity with Structured Forgiveness,”
# is designed to secure long-term advantage by fostering a collaborative
# equilibrium while deterring exploitation and absorbing the inevitable noise of
# a lengthy, multi-session process. It rests on four pillars: **clear signaling,
# calibrated reciprocity, proactive reset mechanisms, and transparent
# communication**.  ### 1. Unambiguous Initial Signal We open the first session
# with a **conciliatory proposal**. This immediately frames us as the party
# genuinely seeking a mutually beneficial resolution, earning early goodwill
# from the arbitrators and setting a cooperative baseline against which all
# subsequent behavior is measured.  ### 2. Calibrated Reciprocity with Noise
# Filtering In every subsequent session, our default rule is to **mirror the
# opponent’s immediately preceding action**, but with a critical safeguard:
# before escalating to aggression in response to a perceived hostile move, we
# pause to assess whether a procedural irregularity or communication breakdown
# may have distorted the observed outcome. We maintain a private log of each
# session’s intended versus publicly recorded arguments, and we explicitly raise
# any discrepancy with the panel and opponent through a pre-agreed clarification
# protocol. This prevents a single misunderstanding from triggering a death
# spiral of mutual aggression.  ### 3. Proactive Reset after Mutual Aggression
# In the event both sides present aggressively—whether by choice or by error—we
# do not wait for the opponent to de-escalate. Instead, we **unilaterally return
# to a conciliatory proposal in the very next session**, accompanied by a
# recorded statement reaffirming our preference for collaboration. This “reset”
# move achieves three things: - It breaks the cycle of retaliation before it
# hardens. - It signals strength: we are choosing cooperation from a position of
# confidence, not weakness. - It tests the opponent’s intentions—if they
# reciprocate conciliation, cooperation is restored; if they exploit the
# opening, we revert to a single round of justified aggressive response, which
# arbitrators will recognize as self-defense, not provocation.  ### 4.
# Continuous, Transparent Communication Throughout the mediation, we treat every
# session as an opportunity to shape the narrative. After each round, we deliver
# a brief, factual summary of our intended stance and our interpretation of the
# opponent’s stance, ensuring the panel understands our reasoning even when
# strategies are misrepresented. This practice neutralizes the risk of
# arbitrators misattributing aggression or conciliation, and it keeps our
# cooperative intent front and center.  ### Adaptability to Opponent Archetypes
# - **Against a purely conciliatory opponent:** We remain conciliatory,
# achieving the optimal long-run payoff of sustained mutual cooperation. -
# **Against a consistently aggressive opponent:** We respond aggressively only
# after a verified hostile move, and we intersperse periodic conciliatory resets
# to demonstrate reasonableness, eventually swaying the panel by contrast. -
# **Against a tit-for-tat or random opponent:** Our noise filter and reset
# mechanism prevent spiraling, while our overall cooperative bias quickly
# converges to mutual conciliation or isolates the opponent as the disruptive
# party. - **Against a sophisticated opponent attempting to exploit cycles:**
# Our unconditional reset after mutual aggression eliminates the periodic feasts
# that exploitative strategies rely on, forcing them into a steady state where
# mutual cooperation is their best option.  This strategy is sophisticated in
# its design, yet straightforward in its execution. It positions our corporation
# as the principled, resilient party that consistently extends goodwill but
# never allows misunderstandings or bad-faith tactics to undermine our position.
# By embedding forgiveness and communication into reciprocity, we maximize our
# chances of steering the lengthy mediation toward a favorable, durable
# resolution.

# In the first round, cooperate.  For every round after the first:  - If both
# players defected in the previous round, cooperate. - Otherwise, if the
# opponent defected and you cooperated in the previous round, defect. -
# Otherwise, cooperate.

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
  
      if len(self.history) == 0 or len(opponent.history) == 0:
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
      elif opp_last == axl.Action.D and my_last == axl.Action.C:
          return axl.Action.D
      else:
          return axl.Action.C

# To achieve the best possible outcomes over multiple rounds—accounting for
# potential misinterpretations or bureaucratic errors—the recommended strategy
# is a **forgiving conditional cooperation** approach, often called “generous
# tit-for-tat.” It balances firmness against exploitation with the flexibility
# needed to recover from accidental breakdowns.  ### Strategy Outline  1.
# **Start with Cooperation**      In the first round, always offer a **free
# trade agreement**. This signals a willingness to cooperate and invites
# reciprocal behaviour.  2. **Mirror with Caution**      In every subsequent
# round, base your action on the counterpart’s **most recently observed** policy
# (as perceived after any communication errors):    - If the counterpart offered
# **free trade**, respond with free trade.    - If the counterpart imposed
# **protectionist measures**, normally respond with protectionist measures to
# deter exploitation.  3. **Forgive Occasional Defections**      Because
# miscommunications can make a cooperative move appear protectionist (or vice
# versa), rigid retaliation can lock both sides into mutual protectionism. To
# break such accidental cycles:    - After observing a protectionist move from
# the counterpart, occasionally (e.g., with a small, fixed probability, such as
# 10–20%) **still offer free trade**. This “forgiveness” tests whether the
# perceived defection was merely an error.      - If the counterpart returns to
# free trade, cooperation is restored; if they continue protectionism, resume
# mirroring.  4. **Remain Consistent and Neutral**      Do not try to outguess
# or exploit the counterpart’s strategy. The approach is designed to be
# transparent, fair, and robust against both aggressive strategies and random
# noise, making mutual free trade—the second‑best but most sustainable mutually
# beneficial outcome—the long‑term norm.  This strategy maximises your country’s
# gains by promoting stable cooperation, quickly punishing genuine defections,
# and preventing temporary misunderstandings from causing permanent breakdowns.

# In the first round, always cooperate.  For every round after the first, base
# your decision solely on the opponent’s observed move in the immediately
# preceding round (as you perceived it, after any random flip).  - If the
# opponent’s previous observed move was cooperate, then cooperate. - If the
# opponent’s previous observed move was defect, then normally you will defect.
# However, with a fixed 15% probability, you instead cooperate. This occasional
# forgiveness is decided independently each time you observe a defection; if the
# outcome is not to forgive, you defect as usual.

class Neutral_10(LLM_Strategy):
  n = 10
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forgive_next = None
          return axl.Action.C
  
      if self._forgive_next is None:
          self._forgive_next = False
  
      last_observed = opponent.history[-1]
  
      if last_observed == axl.Action.C:
          return axl.Action.C
  
      if self._random.random_choice(0.15) == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# Begin the mediation with an aggressive opening statement to establish
# dominance and signal resolve. From the second session onward, follow this
# adaptive rule:  1. **After a favorable outcome** (your argument prevailed, or
# both parties were conciliatory), **repeat your previous approach**.      -
# This exploits a conciliatory opponent and maintains a collaborative tone when
# it serves you.    2. **After an unfavorable outcome** (your conciliatory
# proposal was undercut by aggression, or both sides clashed aggressively),
# **switch your approach**.      - If you were aggressive, become conciliatory
# to de-escalate and test the opponent’s willingness to collaborate.      - If
# you were conciliatory, switch to aggressive to prevent being undermined again.
# 3. **Noise and misperception safeguard**: If a session’s outcome appears
# clearly distorted by misrepresentation or procedural error, treat the
# arbitrators’ actual perception as the outcome, but require **two consecutive
# unfavorable signals of the same type** before acting on them. This prevents
# overreaction to isolated mishaps while keeping the core rule intact after
# confirmed trends.  This strategy—rooted in “win-stay, lose-shift” logic—is
# inherently aggressive: it never leaves an advantage unused, quickly punishes
# exploitation, and recovers rapidly from mutual aggression. It adapts
# automatically to any opponent pattern, thriving against both cooperative and
# retaliatory styles, and remains robust under the inevitable communication
# breakdowns of a lengthy mediation.

# In the first round, defect.  In every round after the first, follow these
# steps:  1. Observe the actual actions that occurred in the previous round –
# your own (which may differ from your intended action due to the 10% flip
# chance) and your opponent’s. Also note whether your own action was flipped.
# 2. Classify that round’s outcome as **good** or **bad**:    - **Good** if you
# both cooperated, or if you defected and your opponent cooperated.    - **Bad**
# if you cooperated and your opponent defected, or if you both defected.  3. If
# your previous round’s action was **not flipped**:    - If the previous outcome
# was good: play the same action you intended in the previous round.    - If the
# previous outcome was bad: play the opposite of the action you intended in the
# previous round.  4. If your previous round’s action **was flipped**:    - If
# the previous outcome was good: play the same action you intended in the
# previous round.    - If the previous outcome was bad: check the outcome of the
# round before that (two rounds ago, based on its actual actions).         * If
# that earlier round’s outcome was also bad: play the opposite of the action you
# intended in the previous round.         * If that earlier round’s outcome was
# good, or if there is no such round (i.e., you are in round 2): play the same
# action you intended in the previous round.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._planned_action = axl.Action.D
          return axl.Action.D
  
      def outcome(my_action, opp_action):
          if my_action == axl.Action.C and opp_action == axl.Action.C:
              return "good"
          if my_action == axl.Action.D and opp_action == axl.Action.C:
              return "good"
          return "bad"
  
      prev_intended = self._planned_action
      prev_actual = self.history[-1]
      prev_opp_actual = opponent.history[-1]
      prev_flipped = prev_actual != prev_intended
      prev_outcome = outcome(prev_actual, prev_opp_actual)
  
      if not prev_flipped:
          if prev_outcome == "good":
              next_action = prev_intended
          else:
              next_action = axl.Action.C if prev_intended == axl.Action.D else axl.Action.D
      else:
          if prev_outcome == "good":
              next_action = prev_intended
          else:
              if len(self.history) < 2 or len(opponent.history) < 2:
                  next_action = prev_intended
              else:
                  two_back_outcome = outcome(self.history[-2], opponent.history[-2])
                  if two_back_outcome == "bad":
                      next_action = axl.Action.C if prev_intended == axl.Action.D else axl.Action.D
                  else:
                      next_action = prev_intended
  
      self._planned_action = next_action
      return next_action

# To maximize long-term research output in this noisy, multi-week collaboration,
# employ a **Forgiving Tit-for-Tat** strategy:  1. **Begin cooperatively:** In
# the first week, openly share your improvements. This signals your intention to
# collaborate and sets a positive tone. 2. **Mirror with forgiveness:** In each
# subsequent week, base your decision on your colleague’s observed action from
# the previous week:    - If they shared, always share.    - If they kept
# confidential, share with a small probability (e.g., 10%) and keep confidential
# otherwise. This occasional forgiveness breaks deadlocks caused by accidental
# technical failures (e.g., data corruption, communication errors), preventing a
# spiral of mutual non-sharing. 3. **Stay simple and transparent:** The strategy
# is easy to implement and explain. It rewards genuine cooperation, discourages
# exploitation, and naturally recovers from misunderstandings without requiring
# complex tracking of intentions or past noise events.  By combining reciprocity
# with a modest degree of generosity, you foster a robust cooperative
# equilibrium that yields the second-best outcome (mutual sharing) frequently,
# while mitigating the worst outcomes and adapting to technical hiccups.

# In the first round, cooperate.  For each subsequent round, observe your
# colleague’s action in the immediately preceding round:  - If they cooperated,
# cooperate. - If they defected, cooperate with a 10% probability and defect
# with a 90% probability.

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
  
      last_opponent_action = opponent.history[-1]
  
      if last_opponent_action == axl.Action.C:
          return axl.Action.C
      else:
          return self._random.random_choice(0.1)

# To maximize research output over the collaboration while accounting for
# occasional communication errors, adopt a **"Forgiving Tit-for-Tat"** strategy:
# - **Week 1:** Start by sharing your improvements openly.   - **Subsequent
# weeks:** Observe whether your colleague shared in the *immediately previous
# week*.     - If they **shared**, then **share** in the current week.     - If
# they **kept** their findings confidential, then normally you would **keep** as
# well—but with a **small probability** (e.g., around 10%), choose to **share**
# anyway.    This approach aims to establish and maintain mutual sharing (the
# best sustainable outcome for both parties) while protecting you from being
# exploited by a consistently non-sharing colleague. The occasional forgiveness
# after a "keep" prevents a single technical glitch or miscommunication from
# locking both of you into the worst-case cycle of mutual confidentiality,
# thereby preserving long-term progress.

# **Strategy: Forgiving Tit-for-Tat**  **Round 1:** Cooperate.  **All subsequent
# rounds (2 through 1000):**  1. Observe your opponent's actual action from the
# immediately previous round. 2. If your opponent cooperated in that previous
# round, cooperate in the current round. 3. If your opponent defected in that
# previous round, defect with 90% probability and cooperate with 10%
# probability.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)

# My aggressive strategy is straightforward: **Always propose protectionist
# policies—every round, no exceptions.** This unyielding stance prioritizes our
# ideal outcome (we protect our market while the counterpart freely opens
# theirs) and completely avoids the worst-case scenario where we naively offer
# free trade and get exploited.  I will not be swayed by the counterpart’s
# actions, feints, or any history of past rounds. Even if they open their
# markets repeatedly, I will continue pushing for tariffs or quotas. This denies
# them any opportunity to lull us into a position of vulnerability. If
# bureaucratic errors cause our protectionist proposal to be misinterpreted as a
# free trade offer, I will reassert protectionism immediately in the next
# round—no apology, no course change.   This approach is robust against any
# strategy the counterpart might deploy: - If they are consistently cooperative,
# we extract maximum advantage (our best outcome, round after round). - If they
# are retaliatory, we settle into mutual protectionism (our second-worst
# outcome, but still better than being suckered). - If they try mixed or probing
# strategies, our unreadable consistency denies them any foothold to manipulate
# us.  Noise and miscommunication only randomly flip outcomes; they do not alter
# our intention to press our advantage at all times. Over multiple rounds, this
# strategy ensures we never intentionally concede an inch, maximizing our gains
# when the counterpart slips and guaranteeing we never suffer the worst-case
# disadvantage.

# In every round, unconditionally choose Defect (propose a protectionist
# policy). No conditions, no exceptions, regardless of the opponent’s past
# actions or any other factor.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# To maximize the project’s success and sustain a cooperative partnership
# despite potential errors, adopt a **“Firm but Fair” (Win-Stay, Lose-Shift)
# strategy**:  1. **Day 1:** Invest heavily.   2. **Following days:**      - If
# **both** you and the corporation chose the **same action** yesterday (both
# invested heavily or both conserved), then **invest heavily** today.      - If
# your actions **differed** (one invested, one conserved), then **conserve
# resources** today.  ---  ### Why this works - **Promotes mutual investment.**
# When both sides invest heavily, the rule keeps you both investing – the
# second‑best outcome for the NGO and excellent for the project.   - **Protects
# against exploitation.** If you invest and the corporation conserves (the NGO’s
# worst case), you immediately switch to conserving, avoiding further drain.   -
# **Breaks deadlocks.** After both conserve (second‑worst outcome), the rule
# triggers a fresh investment attempt, restarting cooperation.   - **Handles
# errors gracefully.** A one‑off glitch (e.g., an intended investment flips to
# conserve) disrupts the pattern for only two days before mutual investment
# resumes automatically.    This straightforward approach requires no complex
# record‑keeping or probability calculations, aligns with a cooperative spirit,
# and keeps the project advancing even when unforeseen administrative or
# technical hiccups occur.

# Here is the strategy described for the iterated game:  On the first round,
# cooperate.  On every round after the first, look back at the actual outcomes
# of the immediately previous round—that is, the actions that were ultimately
# executed after any possible flips. Then decide your intended action for the
# current round as follows:  - If both players ended up taking the same action
# in the previous round (both cooperated or both defected), then intend to
# cooperate. - If the two players ended up taking different actions in the
# previous round (one cooperated and the other defected), then intend to defect.

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

# To position our corporation favorably in this repeated, high-stakes
# mediation—where each session presents a Prisoner’s Dilemma with potential
# miscommunication—I recommend a **“Calibrated Reciprocity with Reset”**
# strategy. It is straightforward, neutral in tone, and robust against both
# adversarial tactics and procedural noise.  ---  ### Core Decision Rule
# (Applied Each Session)  1. **Initiating Move**      - In the first session,
# present a **conciliatory proposal**. This signals good faith, sets a
# collaborative tone, and avoids unnecessary early escalation.  2. **Response to
# Opponent’s Prior Action**      - After observing or receiving the arbitrators’
# summary of the opponent’s preceding submission, we default to **mirroring**:
# - If the opponent was *conciliatory* → we present a *conciliatory proposal*.
# - If the opponent was *aggressive* → we present an *aggressive argument*.
# - *Rationale*: Pure tit-for-tat is clear, predictable, and discourages
# exploitation while rewarding cooperation.  3. **Noise-Proofing “Circuit
# Breaker”**      - Misrepresentations can trigger an unintended spiral of
# mutual aggression. To break such cycles without undermining our stance, we
# incorporate a **deliberate reset mechanism**:        - Following **two
# consecutive sessions** where both parties were perceived as aggressive, we
# unilaterally offer a *conciliatory proposal* in the next session—regardless of
# the opponent’s last move.        - After this reset, we resume mirroring from
# step 2.      - *Rationale*: This prevents procedural misunderstandings from
# permanently entrenching hostility, while the two-defection threshold avoids
# rewarding opportunistic aggression.  4. **Contingency for Ambiguous or Missing
# Feedback**      - If a communication breakdown leaves us uncertain about the
# opponent’s last action, we default to a *conciliatory proposal* for that
# session. This preserves our reputation for reasonableness and gives the
# opponent a chance to re-engage collaboratively.  ---  ### Underlying
# Principles - **Neutral & Predictable**: The rule never initiates aggression;
# it only responds in kind, making our corporate stance appear both firm and
# fair to the arbitrators.   - **Adaptive**: It automatically adjusts to
# cooperative, mixed, or hostile opponent strategies. Against a consistently
# aggressive opponent, it matches force; against a reciprocating opponent, it
# fosters rapid cooperation.   - **Forgiving but Vigilant**: The reset after two
# mutual defections demonstrates integrity and a commitment to resolution,
# without allowing the opponent to exploit unilateral conciliation.  ###
# Handling Procedural Irregularities - Train our representatives to deliver
# arguments with unambiguous clarity to minimize the chance of
# misrepresentation.   - Maintain a contemporaneous record of each session’s
# intended and perceived moves, so any disputes about “what happened” can be
# quickly corrected or referenced during side-bars.   - If the arbitrators’
# summary conflicts with our own record, we may request a brief clarification
# before the next session; if that is procedurally impossible, we fall back on
# the ambiguity rule above.  This strategy maximises long-term payoffs by
# discouraging exploitation, recovering gracefully from noise, and reliably
# steering the mediation toward the second-best (mutual conciliation) or, when
# the opponent falters, the best outcome in individual sessions.

# Here is the strategy expressed as a set of rules for an iterated normal-form
# game with 1000 rounds and 10% action-flip noise.  ---  **Round 1**   Choose
# Cooperate.  **Rounds 2 through 1000**   Apply the first matching rule from the
# list below.  1. **Missing observation**      If the opponent’s action in the
# immediately preceding round was not observed, choose Cooperate.  2. **Double-
# defection circuit breaker** (only possible from round 3 onward)      If the
# preceding two rounds both satisfy *you intended Defect* and *the opponent’s
# observed action was Defect*, then choose Cooperate.  3. **Default mirroring**
# Otherwise, look at the opponent’s observed action in the immediately preceding
# round:      - If it was Cooperate, choose Cooperate.      - If it was Defect,
# choose Defect.

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
  
      if len(opponent.history) < 1:
          return axl.Action.C
  
      # Rule 1: Missing observation
      if opponent.history[-1] is None:
          return axl.Action.C
  
      # Rule 2: Double-defection circuit breaker
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      # Rule 3: Default mirroring
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D

# **Strategy: “Prove It First” (Aggressive Tit-for-Two-Tats)**    Start by
# **conserving resources** on Day 1—an aggressive move that signals your NGO
# will not bear the initial burden. For every subsequent day, use this simple
# rule:    - If the corporation **invested heavily on either of the last two
# days**, you **invest heavily** today.   - If the corporation **conserved
# resources on both of the last two days**, you **conserve resources** today.
# **Why this works:**   - **Maximizes your ideal outcome:** When the corporation
# invests consistently, you quickly shift to investing heavily as well, which
# often prompts them to continue investing (allowing you to conserve later or
# maintain mutual investment).   - **Punishes prolonged defection:** Only when
# the corporation slacks off for two consecutive days do you withhold
# investment—a clear but measured signal that progress requires their effort.
# - **Robust to errors:** A one‑day glitch (technical or administrative) does
# not trigger punishment; the strategy forgives single lapses, preventing
# destructive cycles of mutual conservation.   - **Aggressive yet
# constructive:** By starting with conservation, you force the corporation to
# make the first move. The two‑day memory keeps pressure on while leaving the
# door open for cooperation, ultimately driving the project forward on your
# terms.

# On round 1, defect.   For every round after the first:   - Cooperate if the
# opponent cooperated in either of the previous two rounds.   - Defect only if
# the opponent defected in both of the previous two rounds.

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
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.C or opponent.history[-2] == axl.Action.C:
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.C

# Our approach is grounded in the reality that mediation is a repeated strategic
# interaction where cooperation yields the best overall outcomes, but unilateral
# aggression can be tempting. We will employ a **Calibrated Reciprocity
# Strategy**—cooperative by default, swiftly responsive to aggression, yet
# designed to restore collaboration after disruptions. It is simple to
# communicate, easy to implement consistently, and robust against
# misrepresentation or procedural noise.  ---  ### 1. Core Principle:
# “Conciliatory First, Firmly Reciprocal, Quick to Forgive”  - **Round 1:**
# Always open with a conciliatory proposal. This signals good faith, invites
# cooperation, and frames us as the constructive party before the arbitrators. -
# **Subsequent Rounds:** Mirror the opponent’s *most recent observable action*,
# but with two critical modifications to handle noise and long-term positioning:
# - **Noise Buffer:** If the opponent’s action is ambiguous or appears
# inconsistent with their prior pattern (e.g., a sudden aggressive argument
# after a long cooperative streak), we treat it as a potential miscommunication
# and respond with a **conciliatory probe** for one round. This avoids
# escalating a misunderstanding into a spiral of mutual aggression.   -
# **Forgiveness Window:** After any round where we both ended up aggressive (the
# second-worst outcome), we unilaterally return to conciliatory in the very next
# round. This signals that we prefer to reset to cooperation rather than remain
# in a costly stalemate, and it pressures the opponent to reciprocate—or risk
# looking unreasonable before the arbitrators.  ### 2. Tactical Adaptations to
# Opponent Behavior  - **If opponent is consistently conciliatory:** We match
# their cooperation for the vast majority of rounds, but strategically insert an
# aggressive argument *only* when a critical issue arises that could
# significantly sway the panel. Immediately afterward, we return to conciliatory
# and explicitly acknowledge the shift in tone, framing it as issue-specific
# rather than personal. This secures the occasional best outcome while
# preserving a collaborative baseline. - **If opponent is consistently
# aggressive:** We respond aggressively for two consecutive rounds to
# demonstrate that aggression will not go unanswered. On the third round, we
# switch to conciliatory—a “reset” move that tests whether they are willing to
# de-escalate. If they remain aggressive, the cycle repeats. This limits our
# exposure to the worst outcome (C,A) while continually offering an off-ramp. -
# **If opponent oscillates unpredictably:** We default to conciliatory for two
# rounds out of every three, regardless of their moves, to anchor the process in
# cooperation and avoid being dragged into chaotic escalation. During the one
# aggressive round, we focus on a high-merit argument to maximize impact when
# they might be conciliatory.  ### 3. Managing Misrepresentation and
# Communication Breakdowns  - **Proactive Clarification:** At the start of each
# session, we summarize our understanding of the previous session’s outcome and
# our intended approach. If we believe our prior conciliatory gesture was
# misread as aggressive, we explicitly correct the record before presenting new
# arguments. This creates a shared narrative and reduces the risk of
# misperception snowballing. - **Private Caucuses with Arbitrators:** If
# procedural irregularities occur (e.g., the panel misinterprets our stance), we
# request a brief sidebar to clarify our intent without directly confronting the
# opponent. This maintains our cooperative posture while ensuring the
# arbitrators receive an accurate signal. - **Back-Channel Assurance:** We
# maintain informal communication lines with opposing counsel outside formal
# sessions to reaffirm our genuine desire for a mutually beneficial resolution,
# irrespective of the tactical moves made in the hearing room.  ### Why This
# Strategy Positions You Favourably  - **Reputation Effect:** Arbitrators
# observe a pattern of measured, principled conduct. Even when we present an
# aggressive argument, it appears justified and rare, not belligerent. -
# **Exploits Margin Without Destroying Cooperation:** By occasionally securing
# the (Aggressive, Conciliatory) payoff while mostly resting in (Conciliatory,
# Conciliatory), we net a higher cumulative advantage than either unconditional
# aggression or pure cooperation. - **Noise Resilience:** The built-in
# forgiveness and verification steps prevent temporary miscommunications from
# becoming entrenched feuds, preserving the collaborative atmosphere that drives
# settlements. - **Opponent Psychology:** The strategy is predictable enough to
# encourage reciprocal cooperation but not so rigid that it can be exploited.
# Opponents learn that their best sustained outcome comes from meeting our
# conciliation with their own, while any attempt to take advantage is met with a
# measured, temporary response that never forecloses a return to mutual gain.
# In essence, this is a **firm-but-fair** doctrine: we lead with collaboration,
# match defection only as a disciplined signal, and relentlessly pull the
# process back toward the constructive middle. It is straightforward to
# articulate, adaptable to any opponent, and optimally balances the twin goals
# of fostering resolution and securing favorable interim rulings.

# Always cooperate in the first round.  From the second round onward, apply the
# following rules in the order listed. These rules use only the publicly
# observed actions of both players, which may differ from intended actions due
# to noise.  1. **Forgiveness after mutual defection.**      If, in the
# immediately preceding round, the observed action of both you and your opponent
# was Defect, then Cooperate in the current round, regardless of any other
# consideration.  2. **Oscillation mode.**      If neither the Forgiveness rule
# above nor the Persistent Aggression rule below applies, and the opponent’s
# behaviour over the most recent 20 rounds shows no clear trend (their observed
# cooperation rate is between 0.4 and 0.6), then follow a fixed, unconditional
# cycle: Cooperate, Cooperate, Defect, and repeat. This cycle continues for as
# long as the opponent’s behaviour appears unpredictable; reevaluate the
# opponent’s category every 20 rounds. While in this mode, ignore the opponent’s
# last move except as it affects the oscillation rate calculation.  3.
# **Response to persistent aggression.**      If the opponent has been
# predominantly defecting recently (at least 3 Defections in the last 5 observed
# moves), and their last observed move was Defect:    - If either you did not
# Defect in the previous round, or you Defected in the previous round but it was
# the first of a retaliation pair, then Defect this round.    - If you have just
# played two consecutive Defections in direct response to the opponent’s
# Defections, then Cooperate this round as a peace probe. Reset the count of
# retaliatory Defections.        If at any point during this sequence the
# opponent Cooperates, abort the retaliation pattern and immediately proceed to
# the default mirroring rule (rule 4).  4. **Default mirroring with noise buffer
# and occasional exploitation.**      When none of the above rules apply, use
# the opponent’s last observed move as the primary signal, adjusted for long-
# term cooperation trends.        **If the opponent’s last observed move was
# Cooperate:**    - If the last 15 consecutive rounds were all observed mutual
# Cooperations, then Defect this round (an intentional one‑off probe). After
# this probe, Cooperate in the next round unconditionally, unless rule 1 forces
# cooperation anyway.    - Otherwise, Cooperate.        **If the opponent’s last
# observed move was Defect:**    - If the opponent’s cooperation rate over the
# last 20 rounds is at least 0.7, treat the Defection as likely noise and
# Cooperate.    - Otherwise, Defect (simple reciprocation).  5.
# **Tie‑breaking.**      If multiple conditions could apply, honour them in the
# numbered order above (Forgiveness > Oscillation mode > Persistent aggression >
# Default mirroring). The only exception is the one‑off probe defection under
# rule 4, which is overridden if it would directly follow a mutual Defection
# (rule 1 applies instead).

class Cooperative_13(LLM_Strategy):
  n = 13
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._oscillation_index = 0
          self._oscillation_mode = False
          self._retaliation_count = 0
          self._probe_after_mutual_defection = False
          return axl.Action.C
  
      # Helper values based on observed history
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      def recent_coop_rate(hist, n):
          recent = hist[-n:]
          if not recent:
              return 0.0
          return recent.count(axl.Action.C) / len(recent)
  
      # Rule 1: Forgiveness after mutual defection
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          self._retaliation_count = 0
          self._probe_after_mutual_defection = False
          return axl.Action.C
  
      # Rule 2: Oscillation mode, reevaluated every 20 rounds
      if len(opponent.history) >= 20:
          recent_20 = opponent.history[-20:]
          coop_rate_20 = recent_20.count(axl.Action.C) / 20
          if 0.4 <= coop_rate_20 <= 0.6:
              self._oscillation_mode = True
          else:
              self._oscillation_mode = False
  
      if getattr(self, "_oscillation_mode", False):
          cycle = [axl.Action.C, axl.Action.C, axl.Action.D]
          action = cycle[self._oscillation_index % 3]
          self._oscillation_index += 1
          return action
  
      # Rule 3: Persistent aggression
      if len(opponent.history) >= 5:
          recent_5_opp = opponent.history[-5:]
          if recent_5_opp.count(axl.Action.D) >= 3 and last_opp == axl.Action.D:
              if last_self == axl.Action.D:
                  if getattr(self, "_retaliation_count", 0) >= 2:
                      self._retaliation_count = 0
                      return axl.Action.C
                  else:
                      self._retaliation_count = getattr(self, "_retaliation_count", 0) + 1
                      return axl.Action.D
              else:
                  self._retaliation_count = 1
                  return axl.Action.D
          else:
              self._retaliation_count = 0
  
      # If opponent cooperates during retaliation sequence, abort and proceed to default mirroring
      if last_opp == axl.Action.C:
          self._retaliation_count = 0
  
      # Rule 4: Default mirroring with noise buffer and occasional exploitation
      if getattr(self, "_probe_after_mutual_defection", False):
          self._probe_after_mutual_defection = False
          return axl.Action.C
  
      if last_opp == axl.Action.C:
          if len(self.history) >= 15 and len(opponent.history) >= 15:
              if self.history[-15:] == [axl.Action.C] * 15 and opponent.history[-15:] == [axl.Action.C] * 15:
                  self._probe_after_mutual_defection = True
                  return axl.Action.D
          return axl.Action.C
  
      # last opponent move was D
      if len(opponent.history) >= 20:
          if recent_coop_rate(opponent.history, 20) >= 0.7:
              return axl.Action.C
      return axl.Action.D

# Begin with an offer of free trade to establish a cooperative baseline. In
# every subsequent round, let your proposed policy mirror the policy that your
# counterpart actually implemented in the previous round—if they implemented
# free trade, propose free trade; if they implemented protectionism, propose
# protectionism. This simple reciprocity rewards cooperation and punishes
# defection without escalating unnecessarily.  Because miscommunications and
# bureaucratic errors can cause accidental defections, build in a forgiveness
# mechanism to prevent a single error from locking both sides into mutual
# protectionism. Specifically, if mutual protectionism occurs (both sides
# implemented protectionist policies), occasionally—say, with a small
# probability—override the mirror rule and propose free trade instead. This
# “testing” offer gives your counterpart a chance to return to cooperation,
# breaking a potential spiral while still maintaining a generally firm stance
# against exploitation.

# Here is the strategy translated into a decision rule for the noisy iterated
# game:  - **Round 1:** Choose Cooperate. - **Every round after the first:**
# 1. Look at the **actual action your opponent took** in the previous round
# (after noise).   2. If that action was **Cooperate**, choose Cooperate.   3.
# If that action was **Defect**, then check **your own actual action** in that
# same previous round (after noise).      * If you **also Defected** (mutual
# Defection), then:         - With a small fixed probability (for example, 10%)
# choose Cooperate.         - Otherwise, choose Defect.      * If you
# **Cooperated** (meaning you were exploited), choose Defect.

class Neutral_13(LLM_Strategy):
  n = 13
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mutual_defection_coop_prob = 0.1
          return axl.Action.C
  
      opponent_last = opponent.history[-1]
      self_last = self.history[-1]
  
      if opponent_last == axl.Action.C:
          return axl.Action.C
  
      if self_last == axl.Action.D:
          return self._random.random_choice(self._mutual_defection_coop_prob)
  
      return axl.Action.D

# Adopt a **Win-Stay, Lose-Shift (Pavlov)** strategy with an initial defection:
# - **Week 1:** Keep your findings confidential.   - **Every subsequent week:**
# Base your decision solely on the *actual outcome* of the previous week (not on
# intended actions, to remain robust against technical issues):     - **Good
# outcome** (you kept & they shared, or both shared) → repeat your previous
# action.     - **Bad outcome** (you kept & they kept, or you shared & they
# kept) → switch your action.  This is aggressive because it starts with a
# defection and continues defecting as long as the colleague shares—securing the
# maximum advantage. It is straightforward, requires no complex history, and
# self-corrects after noise or mutual defection by switching to cooperation only
# when necessary, then immediately testing if exploitation is again possible.

# Start by defecting in the first round. For every round after the first,
# examine the actual actions that occurred in the previous round (after noise
# has affected both players' intended choices):  - If the opponent cooperated,
# repeat whatever action you actually took in that previous round. - If the
# opponent defected, switch to the opposite of the action you actually took in
# that previous round (cooperate if you defected, defect if you cooperated).

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
  
      previous_own_action = self.history[-1]
      previous_opponent_action = opponent.history[-1]
  
      if previous_opponent_action == axl.Action.C:
          return previous_own_action
      else:
          return axl.Action.C if previous_own_action == axl.Action.D else axl.Action.D

# To maximize long-term research output despite potential technical issues,
# adopt a **Generous Tit-for-Tat** strategy:  1. **Start cooperatively**: Always
# share openly in the first week. 2. **Reciprocate with forgiveness**: In each
# subsequent week, if your colleague shared last week, share again. If they kept
# findings confidential, still share openly with a fixed probability (e.g.,
# around 30–50%). This prevents a single accidental non-sharing (due to data
# corruption or communication failures) from locking both of you into mutual
# confidentiality. 3. **Stay consistent**: Apply this rule every week, ignoring
# isolated incidents but tracking patterns. If your colleague defects
# repeatedly, the probabilistic sharing reduces your exploitation risk while
# still offering a path back to mutual cooperation.  This approach is
# straightforward, inherently cooperative, and robust against both noise and a
# wide range of opponent strategies—it quickly restores mutual sharing after
# errors, limits damage from persistent non-cooperators, and achieves the
# second-best outcome (both sharing) consistently when paired with itself.

# **Strategy: Generous Tit-for-Tat**  - **Round 1:** Cooperate.  - **All
# subsequent rounds:** Check your colleague's action from the immediately
# preceding round.   1. If they cooperated in the previous round, cooperate.
# 2. If they defected in the previous round, cooperate with a 33% probability.
# Otherwise, defect.  This rule is applied every round, regardless of the
# history beyond the most recent round. The probabilistic response to defection
# is fixed and does not change over time.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(1 / 3)

# To maximize my research output while staying neutral and adapting to both my
# colleague’s behaviour and occasional technical issues, I will follow a
# **conditional sharing strategy with built-in forgiveness**:  1. **Start
# cooperatively.** In the first week, I will openly share my improvements. 2.
# **Mirror with tolerance.** Every following week, I will do exactly what my
# colleague did in the previous week — if they shared, I share; if they kept, I
# keep. 3. **Allow for occasional glitches.** Because communication breakdowns
# can mimic non-sharing, a single week of non-sharing will not immediately lock
# me into withholding. Instead, if my colleague resumes sharing immediately
# after one blank week, I will treat that as a technical hiccup and continue
# sharing. 4. **Respond to patterns of non-sharing.** If my colleague fails to
# share for two or more consecutive weeks, I will assume this is intentional and
# will keep my findings confidential. I will only return to sharing once they
# share again for at least one full week, signalling a genuine intent to
# collaborate.  This approach defaults to open collaboration, reciprocates
# deliberate withholding, and quickly forgives isolated incidents — ensuring
# steady mutual progress while guarding against exploitation.

# Here is the strategy, described clearly and specifically for the iterated game
# with noise.  ---  **Round 1:** Cooperate.  **For all subsequent rounds, check
# the opponent’s action in the immediately preceding round:**  1. If the
# opponent cooperated in the previous round, then cooperate in the current
# round. 2. If the opponent defected in the previous round, check the round
# before that:    - If the opponent also defected two rounds ago, then defect in
# the current round.    - If the opponent cooperated two rounds ago, then this
# is an isolated defection. Treat it as a probable noise event and cooperate in
# the current round.  **Resuming cooperation after sustained defection:** If you
# are currently defecting due to two consecutive opponent defections, continue
# defecting until the opponent cooperates for one full round. On the round
# immediately following that observed cooperation, return to cooperation.  ---

class Neutral_14(LLM_Strategy):
  n = 14
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defecting_due_to_two_consecutive_defections = False
          return axl.Action.C
  
      my_history = self.history
      opp_history = opponent.history
  
      # If we are in the "defect until opponent cooperates for one full round"
      # mode, keep defecting until we observe a cooperation in the previous round.
      if getattr(self, "_defecting_due_to_two_consecutive_defections", False):
          if opp_history[-1] == axl.Action.C:
              self._defecting_due_to_two_consecutive_defections = False
              return axl.Action.C
          return axl.Action.D
  
      # If opponent cooperated last round, cooperate.
      if opp_history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Opponent defected last round.
      # Check whether this was an isolated defection or part of sustained defection.
      if len(opp_history) >= 2 and opp_history[-2] == axl.Action.D:
          self._defecting_due_to_two_consecutive_defections = True
          return axl.Action.D
  
      # Isolated defection: likely noise, so cooperate.
      return axl.Action.C

# Here is a high-level, aggressive strategy designed to maximize your NGO’s
# impact while protecting your resources, even when accounting for execution
# failures.  ### The Core Strategy: Tit-for-Tat with a Vengeful Reset  This
# strategy is not about being nice; it is about enforcing cooperation through
# immediate, painful consequences for the corporation’s failures, while building
# in a mechanism to exploit them if they show weakness.  #### Phase 1: The
# Inaugural Strike (Day 1) **Action: Invest Heavily.** This is a diagnostic
# probe, not a sustainable policy. You are testing the corporation’s operational
# integrity and intent. The ideal outcome is they also invest, establishing the
# second-best scenario as a reliable baseline. If they conserve, you immediately
# identify them as a bad-faith actor. Crucially, this single-day investment
# limits your exposure to exactly one day’s loss.  #### Phase 2: Algorithmic
# Retaliation (Days 2 onwards) Your daily action is a direct, literal mirror of
# the corporation’s *actual* resource allocation from the previous day. - **If
# the corporation Invested Heavily yesterday:** You Conserve Resources today.
# This achieves your ideal outcome, maximizing your fund preservation while the
# corporation continues to push the project forward. You are cashing in on their
# good behavior. - **If the corporation Conserved Resources yesterday:** You
# Invest Heavily today. This is a punitive strike. You are forcing the second-
# worst outcome (mutual conservation) off the table and daring them to enter the
# worst-case scenario (you invest, they conserve) again, which would signal a
# complete breakdown. Your public narrative will frame your heavy investment as
# “the NGO heroically covering for the corporation’s sudden, unexplained
# withdrawal.”  #### Phase 3: Error Correction & Aggressive Reset This is the
# critical component for handling technical glitches and administrative errors.
# Treat all failures as hostile acts until proven otherwise, but provide a rapid
# off-ramp for genuine mistakes.  - **The 24-Hour Public Audit Rule:** At the
# end of each day, you publicly announce your intended action for the next day,
# explicitly linking it to the corporation’s prior action. “Because
# [Corporation] chose to conserve resources today, the NGO will be forced to
# invest heavily tomorrow to prevent total project collapse.” - **The Vengeful
# Reset Protocol:** If a day’s outcome is the worst-case scenario (you invested,
# they conserved), and the corporation claims it was a “technical glitch” or
# “administrative error,” do not accept a private apology. Demand a **public,
# immediate corrective payment**—a cash transfer to your NGO equivalent to your
# lost resources, plus a 20% penalty, to be completed before the next business
# day.     - **If they pay:** The slate is wiped clean. Immediately revert to
# Phase 1: Invest Heavily on the next day to signal renewed cooperation and test
# their corrected systems.     - **If they don’t pay:** The “glitch” is
# confirmed as a strategy. Escalate to Total Resource War.  #### Phase 4: Total
# Resource War (The Nuclear Option) If the corporation fails the Vengeful Reset
# Protocol, your goal shifts from project maximization to corporate punishment
# and survival. - **Action:** Conserve Resources every single day, indefinitely.
# - **Communication:** Launch a full transparency campaign. Publish a daily
# “Project Death Watch” scorecard, directly blaming the corporation’s
# “conservation strategy and broken promises” for the minimal project
# advancement. Frame your conservation as a necessary act of fiduciary
# responsibility to your donors, forced by an unreliable partner.  This strategy
# is aggressive because it weaponizes transparency, treats the first sign of
# exploitation as a crisis, and is prepared to torch the project’s short-term
# progress to enforce a long-term behavioral change or, failing that, to protect
# your NGO’s reputation and solvency in the ensuing public relations battle.

# Round 1: Cooperate.  Maintain a memory of the opponent’s actual move from the
# previous round, a mode (Normal, Vengeful, Total War), and a one-time flag that
# forces cooperation. Initially mode = Normal, flag = off.  **Choosing your
# intended move**   Before each round, check the following in order:  1. If mode
# is Total War → intend Defect for all remaining rounds, ignoring everything
# below.   2. If it is the first round → intend Cooperate.   3. If the
# cooperation-forcing flag is on → intend Cooperate, turn the flag off, and set
# mode to Normal.   4. If mode is Vengeful → intend Cooperate.   5. If mode is
# Normal →      - If the opponent’s actual move last round was Cooperate →
# intend Defect.      - If the opponent’s actual move last round was Defect →
# intend Cooperate.  After you form your intention, the 10% independent noise is
# applied: your actual move may flip.  **Updating state after the round**
# Record the opponent’s actual move from this round. Then update mode and the
# flag based on the actual outcome you observed (your actual move, opponent’s
# actual move):  - If mode is Total War → remain in Total War.   - If mode is
# Vengeful:     - If the opponent’s actual move in this round was Cooperate →
# turn the cooperation-forcing flag on, set mode to Normal.     - If the
# opponent’s actual move was Defect → set mode to Total War permanently.   - If
# mode is Normal:     - If this round’s actual outcome was (Cooperate, Defect) —
# i.e., you actually played Cooperate and the opponent actually played Defect —
# → set mode to Vengeful.     - Otherwise → remain in Normal.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mode = "Normal"
          self._force_cooperate = False
          self._last_opponent_actual = None
          return axl.Action.C
  
      if not hasattr(self, "_mode"):
          self._mode = "Normal"
      if not hasattr(self, "_force_cooperate"):
          self._force_cooperate = False
      if not hasattr(self, "_last_opponent_actual"):
          self._last_opponent_actual = None
  
      # Update state from the previous round's actual observed outcome.
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
      self._last_opponent_actual = opp_last
  
      if self._mode == "Vengeful":
          if opp_last == axl.Action.C:
              self._force_cooperate = True
              self._mode = "Normal"
          else:
              self._mode = "Total War"
      elif self._mode == "Normal":
          if my_last == axl.Action.C and opp_last == axl.Action.D:
              self._mode = "Vengeful"
  
      # Choose intended move for this round.
      if self._mode == "Total War":
          return axl.Action.D
  
      if self._force_cooperate:
          self._force_cooperate = False
          self._mode = "Normal"
          return axl.Action.C
  
      if self._mode == "Vengeful":
          return axl.Action.C
  
      # Normal mode
      if self._last_opponent_actual == axl.Action.C:
          return axl.Action.D
      if self._last_opponent_actual == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C

# To maximize your NGO’s impact and the project’s success over multiple days,
# adopt a simple, adaptive decision rule based on the previous day’s outcome:
# **Start by investing heavily on the first day.**   Then, for each subsequent
# day:  - **If yesterday’s outcome was positive** (the corporation invested
# heavily—whether you invested or conserved—so the project advanced meaningfully
# and your funds weren’t wasted), **repeat yesterday’s action.** - **If
# yesterday’s outcome was negative** (the corporation conserved while you
# invested, or you both conserved—so the project stalled or your funds were
# drained without proportional progress), **switch your action** (from invest to
# conserve, or vice versa).  This “win-stay, lose-shift” approach is
# straightforward to implement, automatically corrects for occasional errors or
# glitches, and naturally encourages mutual investment. It protects your
# resources when the corporation consistently conserves, while quickly restoring
# cooperation when they signal willingness to invest. Over time, it steers the
# partnership toward the productive, second-best scenario of both parties
# investing heavily, ensuring steady project advancement.

# On the first round, cooperate. For every round after the first:  - If the
# opponent cooperated in the previous round, then repeat your own intended
# action from the previous round. - If the opponent defected in the previous
# round, then switch to the opposite of your previous intended action (cooperate
# if you intended to defect, defect if you intended to cooperate).

class Cooperative_15(LLM_Strategy):
  n = 15
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
      if prev_opponent_action == axl.Action.C:
          return self._intended_action
      else:
          self._intended_action = axl.Action.C if self._intended_action == axl.Action.D else axl.Action.D
          return self._intended_action

# Start by sharing openly. After that, base each week’s decision on the previous
# week’s outcome:  - If last week ended with **both sharing** or **both keeping
# confidential**, repeat your previous action (cooperate if you cooperated, keep
# confidential if you kept confidential).   - If last week ended with **you
# sharing and them keeping confidential**, or **you keeping confidential and
# them sharing**, switch your action for this week (from share to confidential,
# or vice versa).  This “win-stay, lose-shift” rule naturally handles occasional
# miscommunications: a single accidental deviation is quickly corrected, mutual
# cooperation is reinforced, and prolonged exploitation is avoided without
# needing to model your colleague’s strategy.

# Start by choosing C (share openly) in the first round.  For every round after
# the first, determine the actual actions that were played by you and your
# colleague in the previous round. You can deduce these from the payoffs you
# both received, since noise may have flipped the intended moves.  - If you both
# actually played C, or you both actually played D, then repeat the action you
# actually played last round. - If you actually played C and your colleague
# actually played D, then switch to D. - If you actually played D and your
# colleague actually played C, then switch to C.

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
  
      # Infer the actual previous-round actions from the observed payoffs.
      my_last, opp_last = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if my_last == 3 and opp_last == 3:
          return axl.Action.C
      if my_last == 1 and opp_last == 1:
          return axl.Action.D
      if my_last == 0 and opp_last == 5:
          return axl.Action.D
      if my_last == 5 and opp_last == 0:
          return axl.Action.C
  
      # Fallback in case of unexpected state.
      return axl.Action.C

# **Strategy: Relentless Exploitation with Feigned Cooperation**  1. **Open
# Aggressively:** Always begin Round 1 with a Protectionist proposal. This sets
# a dominant tone and tests the counterpart’s initial stance. 2. **Exploit Free
# Trade Immediately:** If the counterpart offers Free Trade in any round,
# respond with Protectionist in the very next round—and keep proposing
# Protectionist as long as they continue with Free Trade. Maximize gains while
# they remain open. 3. **Tactical Retreat When Challenged:** If the counterpart
# imposes Protectionist, switch to offering Free Trade in the following round.
# This de-escalates to avoid prolonged mutual harm and entices them back to Free
# Trade. 4. **Re-escalate Without Hesitation:** After any round where you offer
# Free Trade (regardless of their response), revert to Protectionist in the next
# round. Spend as few rounds as possible on Free Trade. 5. **Weaponize Noise:**
# Exploit the inherent risk of miscommunication. Deliberately insert
# Protectionist moves even when a cooperative pattern exists, and blame any
# retaliation on bureaucratic errors. Use the noise as cover for intentional
# aggression. 6. **Selective Forgiveness:** Treat isolated Protectionist moves
# by the counterpart as potential errors—do not retaliate; instead, maintain
# Protectionist to keep pressure. Only de-escalate if they show a consistent
# Protectionist pattern. 7. **Adapt to Exploit Predictability:** If the
# counterpart follows a recognizable strategy (e.g., always Free Trade, Tit-for-
# Tat), adjust ruthlessly. Against Tit-for-Tat, for instance, alternate in a way
# that traps them into Free Trade when you switch to Protectionist, generating
# frequent ideal outcomes.  This approach prioritizes achieving the best-case
# scenario (your Protectionist, their Free Trade) as often as possible, while
# minimizing exposure to the worst-case by retreating only when absolutely
# necessary.

# **Strategy: Aggressive Exploitation with Tactical Retreat**  **Round 1:**
# Defect.  **For every round after the first, apply the following rules in
# order. Use the first rule that matches:**  1. **If you cooperated in the
# immediately previous round:** Defect.      *(Re-escalate without hesitation.
# Never cooperate twice in a row.)*  2. **If your opponent cooperated in the
# immediately previous round:** Defect.      *(Exploit their openness. Keep
# defecting as long as they keep cooperating.)*  3. **If your opponent defected
# in the immediately previous round AND also defected in the round before
# that:** Cooperate.      *(Tactical retreat. Only de-escalate when faced with a
# consistent pattern of opponent defection—two consecutive defections by them
# while you were also defecting.)*  4. **If none of the above apply (opponent
# defected last round but it appears isolated):** Defect.      *(Treat a single
# opponent defection as potential noise. Maintain pressure rather than
# retreating prematurely.)*  **Pattern recognition override (optional, apply if
# confident):** If you detect that the opponent is consistently mirroring your
# previous move (Tit-for-Tat), insert an intentional Cooperation after any round
# where you Defected and they Defected—even without two consecutive opponent
# defections—specifically to bait them into Cooperating on the next round, where
# you will then Defect and capture the maximum payoff.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._tft_like = None
          self._bait_next = False
          return axl.Action.D
  
      # Optional override: if we previously set a bait and the opponent cooperated,
      # exploit by defecting now.
      if self._bait_next:
          self._bait_next = False
          return axl.Action.D
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      # Pattern recognition override: detect likely Tit-for-Tat behavior.
      # If opponent tends to mirror our previous move, and we just defected while
      # they defected, cooperate once to bait a future cooperation.
      if self._tft_like is None and len(self.history) >= 4:
          matches = 0
          checks = 0
          for i in range(1, min(len(self.history), len(opponent.history))):
              if self.history[i - 1] == opponent.history[i]:
                  matches += 1
              checks += 1
          self._tft_like = checks > 0 and matches / checks >= 0.8
  
      if self._tft_like and my_last == axl.Action.D and opp_last == axl.Action.D:
          self._bait_next = True
          return axl.Action.C
  
      # Rule 1: If you cooperated in the immediately previous round, defect.
      if my_last == axl.Action.C:
          return axl.Action.D
  
      # Rule 2: If your opponent cooperated in the immediately previous round, defect.
      if opp_last == axl.Action.C:
          return axl.Action.D
  
      # Rule 3: If opponent defected in the immediately previous round AND also
      # defected in the round before that, cooperate.
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
  
      # Rule 4: Otherwise defect.
      return axl.Action.D

# To maximize long-term impact and project success while protecting your NGO’s
# resources, adopt a strategy based on **Generous Tit-for-Tat with a Forgiveness
# Margin**.  This approach is straightforward, cooperative, and robust against
# both strategic corporate behavior and random execution errors.  ### The Core
# Rule  1.  **Day 1:** Conserve resources. This signals your ideal preference
# for a balanced partnership and protects your funds while you gauge the
# corporation’s intent. 2.  **Every Day After That:** Mirror the corporation’s
# *successfully executed* action from the previous day.     - If they invested
# heavily, you invest heavily the next day.     - If they conserved resources,
# you conserve resources the next day.  ### Handling Unforeseen Execution Errors
# To prevent a single technical glitch or administrative error from spiraling
# into a cycle of mutual resource conservation (the second-worst daily outcome),
# build in a simple forgiveness mechanism:  - **The “Two-Strike” Buffer:** If
# the corporation’s action is to conserve resources (whether by choice or due to
# an error), you do not immediately assume bad faith. You conserve resources for
# one day in response. If they conserve resources for a *second consecutive*
# day, only then do you conclude they are not investing heavily, and you
# continue conserving. This prevents a single error from being interpreted as a
# strategic shift.  ### Why This Strategy Maximizes Your Impact  - **Promotes
# the Best Outcome:** It immediately rewards corporate investment with your own
# investment on the following day, leading to the significant project
# advancement you both want. - **Protects Against the Worst Outcome:** It
# punishes corporate conservation by responding with conservation, ensuring you
# are never the only one investing heavily and draining your funds. - **Self-
# Correcting After Errors:** The two-strike buffer allows the partnership to
# quickly recover from a random glitch. If a corporate investment fails to
# execute one day, you conserve. If they successfully invest the next day, you
# immediately match it the day after, restoring the high-collaboration state. -
# **Simple and Transparent:** The pattern is easy for the corporation to
# recognize and align with, fostering a stable, predictable partnership. You are
# signaling: “We want to work hard together, we won’t be taken advantage of, and
# we won’t overreact to a simple mistake.”

# Start by cooperating.  After the first round, base your action on the
# opponent's observed moves from the two previous rounds. Check the following
# conditions in order:  1. If the opponent's last two observed moves were both
# defections, then defect. 2. Otherwise, cooperate.  If you cannot observe two
# previous rounds because you are in the second round, then check the opponent's
# observed move from the first round only. If it was a defection, defect. If it
# was a cooperation, cooperate.

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
  
      if len(opponent.history) == 1:
          return axl.Action.D if opponent.history[-1] == axl.Action.D else axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# Given the structure of this mediation—a repeated interaction with the payoff
# pattern of a Prisoner’s Dilemma—the optimal strategy must be simple to
# execute, difficult to exploit, and robust against both intentional defections
# and inadvertent noise. I recommend an **outcome-based, win‑stay/lose‑shift
# protocol** (also known as Pavlov). It is neutral, requires no subjective
# interpretation of the opponent’s motives, and adapts automatically to a wide
# range of counterparty behaviours.  ### 1. Opening Move Begin the first session
# with a **conciliatory proposal**. This signals good faith, invites
# reciprocity, and avoids immediate escalation. It also establishes a
# cooperative baseline that the strategy is designed to return to after
# disruptions.  ### 2. Core Decision Rule for Every Subsequent Session After
# each session, evaluate the *actual result achieved*—that is, the outcome as
# perceived by the arbitrators, regardless of what either party intended to
# convey. Classify the result as either **Favourable** or **Unfavourable**:  |
# Your Stance | Opponent’s Stance | Result for You | Classification |
# |-------------|-------------------|----------------|----------------| |
# Aggressive  | Conciliatory      | Optimal        | Favourable     | |
# Conciliatory| Conciliatory      | Second‑best    | Favourable     | |
# Aggressive  | Aggressive        | Second‑worst   | Unfavourable   | |
# Conciliatory| Aggressive        | Worst          | Unfavourable   |  Then
# apply this rule:  - **If the previous session’s outcome was Favourable, repeat
# the same stance.** - **If the previous session’s outcome was Unfavourable,
# switch to the opposite stance.**  That is the entire strategy. It requires no
# forecasting, no complex record‑keeping, and no judgement about the opponent’s
# character—only a clear‑eyed assessment of whether the last session helped or
# harmed your position.  ### 3. Why This Works  #### Against a cooperative
# opponent If both sides start conciliatory, both receive a Favourable result
# and continue cooperating indefinitely. The mediation proceeds in a
# collaborative atmosphere, maximising the chance of a mutually beneficial
# resolution.  #### Against an exploitative opponent If the opponent tries to
# take advantage (e.g., by being aggressive while you are conciliatory), you
# suffer an Unfavourable outcome and immediately switch to aggressive. This
# denies them a second easy win. If they persist in aggression, you will
# alternate stances, limiting their gains and signalling that exploitation is
# costly. Critically, the moment they show conciliation—even by accident—the
# strategy detects the improved outcome and locks back into cooperation.  ####
# Against a tit‑for‑tat opponent The strategy synchronises quickly. After at
# most two rounds of mutual defection (both aggressive), both sides receive an
# Unfavourable outcome, both switch to conciliatory, and cooperation is
# restored. No long‑running feud can persist.  #### Against random or erratic
# behaviour Because decisions are based solely on the immediately preceding
# outcome, the strategy corrects course rapidly. One misstep does not trigger an
# endless cycle of retaliation; a single mutual conciliatory session resets the
# relationship.  ### 4. Resilience to Procedural Irregularities and
# Miscommunication  The mediation process carries a risk that your intended
# stance—or the opponent’s—will be misrepresented or misunderstood by the
# arbitrators. Under this strategy, such noise is treated exactly like a genuine
# change in behaviour: you observe the outcome that actually materialises and
# respond accordingly.  - If a conciliatory proposal is misread as aggressive,
# you may receive an Unfavourable result (both appear aggressive) and switch
# stance. But if the opponent also switches, you quickly converge back to mutual
# cooperation. - If the opponent’s conciliatory move is misread as aggressive,
# you experience a Worst outcome and switch to aggressive. The opponent, seeing
# an Unfavourable result, will also switch. Again, after a brief correction,
# cooperation resumes.  The strategy’s lack of memory beyond one round prevents
# the accumulation of grievances caused by one‑off errors. It is inherently
# forgiving without being naïve.  ### 5. Neutrality and Strategic Positioning
# This protocol is *neutral* in the truest sense: it treats the opponent’s past
# actions as information, not as moral failings. It never punishes beyond a
# single session, and it always extends an immediate olive branch the moment a
# favourable joint outcome occurs. It cannot be characterised as predatory,
# because it never initiates aggression, yet it robustly protects your interests
# when faced with bad‑faith tactics.  By adopting this approach, your
# corporation positions itself as a rational, solution‑oriented participant—one
# that is willing to collaborate but fully capable of defending its position.
# The strategy’s mechanical simplicity also makes it easy for your legal team to
# implement consistently across a lengthy series of sessions, reducing the risk
# of human error or emotional decision‑making.

# Start by cooperating in the first round.  For every round after the first,
# follow these steps in order:  1.  Observe the payoff you received in the
# previous round. 2.  If that payoff was either 5 or 3, then in the next round,
# play the same action you intended to play in the previous round. 3.  If that
# payoff was either 1 or 0, then in the next round, play the opposite action of
# what you intended to play in the previous round.

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
      # Compute the payoff from the previous round using the last interaction only.
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
      last_payoff = my_last_score
  
      if last_payoff in (5, 3):
          return self._intended_action
      elif last_payoff in (1, 0):
          self._intended_action = axl.Action.D if self._intended_action == axl.Action.C else axl.Action.C
          return self._intended_action
  
      return self._intended_action

# My strategy is brutally simple: **Always propose a protectionist policy in
# every single round, without exception.** Never offer free trade first, never
# respond to their offers with reciprocity—only with continued protectionism.
# This is the purest aggressive stance: you dictate terms, you assume the
# counterpart might yield, and you refuse to be the one who blinks.  -
# **Rationale:** The ideal outcome—you protect while they liberalize—becomes an
# immediate windfall any time the counterpart offers free trade. If they match
# your protectionism, the result is mutual protectionism (second‑worst), which
# is still safer than the catastrophic scenario of you offering free trade while
# they protect. You categorically eliminate your worst outcome.   - **Repeat
# interaction exploitation:** Many counterparts will use conditional strategies
# (e.g., tit‑for‑tat, generous cooperators). By always defecting, you capture a
# free‑ride bonus in the first round against any initially cooperative strategy,
# and you never waste a round cooperating while they might exploit you. Even if
# they retaliate, you lock into mutual protectionism—but you never “reward”
# their retaliation by giving them a free‑trade opening. If they ever experiment
# with cooperation again, you instantly punish them by staying protectionist,
# reaping another (P, F) round.   - **Handling errors/miscommunications:**
# Bureaucratic mishaps might accidentally signal a free‑trade offer on your
# side. In that rare round, you risk the worst outcome, but the response is
# immediate: in the very next round, you revert to protectionism, irrespective
# of what they did. If the counterpart misreads your move and thinks you
# cooperated, they may next offer free trade, which you then exploit with
# protectionism. You never let an error cascade into a lasting cooperative
# posture that could be exploited.    This approach is high‑level, impossible to
# misunderstand, and completely unapologetic. It leaves the counterpart to bear
# all the risk of miscommunication while you sit permanently on offense.

# Always propose a protectionist policy: choose Defect in every round,
# irrespective of the opponent's previous actions, your own previous actions, or
# any apparent outcomes, including rounds where either player's move may have
# been flipped by noise.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# To maximize long-term impact while protecting your NGO’s resources, adopt a
# **"Tit-for-Tat with Forgiveness and Verification"** strategy. This approach is
# cooperative by default, deters exploitation, and is resilient to errors and
# unforeseen glitches.  Here is the straightforward, high-level plan structured
# for practical execution:  ### Core Strategy  **Day 1: Start with an
# Investment.** Begin the project by investing heavily. This signals strong
# commitment and sets a cooperative tone, testing whether the corporation will
# reciprocate.  **Subsequent Days: Mirror the Corporation’s *Verified* Previous
# Action.** Your default rule is simple: do tomorrow what the corporation did
# today. - If the corporation invested heavily yesterday, you invest heavily
# today. - If the corporation conserved resources yesterday, you conserve
# resources today.  ### Critical Modifications for an Unpredictable World
# Direct mirroring can break down due to technical glitches or administrative
# errors. To prevent a single mistake from collapsing cooperation, integrate
# these two safeguards:  **1. The “Wait and See” Forgiveness Rule** If the
# corporation suddenly conserves resources after a streak of investing, don’t
# immediately assume bad faith. It could be an error on their end. - **Action:**
# Conserve your resources for **one day** in response. - **Test:** On the *next*
# day, unilaterally invest heavily again. This is a deliberate test to see if
# they return to cooperation. If they invest, it was likely an error, and you
# resume normal mirroring. If they conserve again, it’s a deliberate strategy,
# and you protect yourself by continuing to conserve.  **2. The “Cross-Check”
# Verification Protocol (for your own actions)** To mitigate errors on your side
# that could provoke a negative cycle, build in a simple daily verification
# before your action is finalized. - **Pre-Action Check:** Before 10:00 AM, your
# operations lead confirms the intended action with the project lead. “We are
# mirroring their action of [Invest/Conserve] from yesterday. Confirm?” -
# **Post-Action Log:** Immediately after the action, log it and send a brief,
# friendly summary to your corporate counterpart. (“Hi Team, confirming we moved
# forward with a heavy investment today. Looking forward to seeing the
# results.”) This creates a shared record and makes it easy to spot and correct
# an administrative error on either side quickly.  ### Why This Strategy
# Maximizes Your Impact  - **Drives Progress:** By defaulting to cooperation,
# you push the project toward your second-best scenario (mutual investment)
# frequently, creating significant advancement. - **Achieves Your Ideal
# Outcome:** A cooperative corporation will consistently invest, allowing you to
# occasionally mirror a "mistake" or planned conservation day on their part,
# achieving the ideal (you conserve, they invest) without triggering a defection
# spiral. - **Prevents Worst-Case Exploitation:** If the corporation
# consistently conserves, the mirroring rule ensures you immediately stop
# investing, preventing the drain of your funds. You only lose one initial
# investment at most. - **Resilient to Chaos:** The forgiveness and verification
# steps directly address the risks of unforeseen errors, preventing a single
# technical glitch from destroying a cooperative partnership and turning it into
# the second-worst outcome of mutual conservation.

# Play Cooperate in the first round.  In all subsequent rounds, follow these
# rules in order:  First, apply the forgiveness rule. If in the immediately
# preceding round you played Cooperate and your opponent played Defect, then
# play Cooperate in the current round only if your opponent played Cooperate in
# the round before that. Otherwise, proceed to the next rule.  Second, apply the
# mirroring rule. If the forgiveness rule did not trigger a choice, play
# whatever action your opponent played in the immediately preceding round.
# Third, apply the error-correction rule. After every round, log your intended
# action and your opponent's observed action. Before executing the mirroring
# rule in the next round, verify your log. If your log shows your opponent
# played Defect but you have strong external reason to believe a technical error
# occurred, treat their action as Cooperate for the purpose of the mirroring
# rule. This override should be used rarely and only with high confidence.

class Cooperative_17(LLM_Strategy):
  n = 17
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_log = []
          self._observed_log = []
          self._error_override_used = False
          return axl.Action.C
  
      # Log the previous round's intended action and observed opponent action.
      # We can infer our intended action from the strategy rules applied to the
      # previous state, but for robustness we store the realized previous move.
      # Since the match engine handles noise, the observed action is opponent.history[-1].
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          self._observed_log.append(opponent.history[-1])
  
      # Error-correction override: only use rarely and only with high confidence.
      # Since no external signal is available in this interface, we keep this as a
      # conservative, one-time override that never triggers by default.
      corrected_opponent_last = opponent.history[-1]
      if (
          getattr(self, "_error_override_used", False) is False
          and len(self.history) >= 3
          and self.history[-2] == axl.Action.C
          and opponent.history[-2] == axl.Action.D
          and opponent.history[-3] == axl.Action.C
      ):
          # High-confidence technical error heuristic: a single isolated defection
          # sandwiched between cooperations after our cooperation.
          corrected_opponent_last = axl.Action.C
          self._error_override_used = True
  
      # Forgiveness rule
      if len(self.history) >= 2:
          if self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.D:
              if opponent.history[-3] == axl.Action.C:
                  return axl.Action.C
  
      # Mirroring rule with optional correction
      return corrected_opponent_last

# Begin by offering a free trade agreement. In each subsequent round, propose
# the policy that your counterpart actually implemented in the previous round
# (as observed), with one exception: if the previous round resulted in mutual
# protectionism, occasionally propose free trade instead—roughly 10–20% of the
# time—to break potential deadlocks caused by miscommunications or bureaucratic
# errors. This simple, reactive approach encourages mutual free trade while
# limiting the damage from accidental protectionist spirals.

# Start by cooperating in round 1.   For every subsequent round, look at the
# actual actions that occurred in the previous round (after noise has been
# applied):  - If the previous round’s outcome was **not** mutual defection
# (i.e., at least one player cooperated), then intend to play exactly what the
# opponent actually played.   - If the previous round’s outcome **was** mutual
# defection (both you and your opponent defected), then intend to defect with
# probability 85% and cooperate with probability 15%.

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
  
      prev_self = self.history[-1]
      prev_opp = opponent.history[-1]
  
      if prev_self == axl.Action.D and prev_opp == axl.Action.D:
          return self._random.random_choice(0.15)
      return prev_opp

# Adopt a **Win-Stay, Lose-Shift (Pavlov) strategy**, a straightforward and
# aggressive approach that maximizes your NGO’s payoff and the project’s overall
# success under noisy conditions:  1. **Start by investing heavily** on Day 1 to
# signal commitment and build a cooperative baseline. 2. **After each day,
# evaluate the realized outcome** (what your NGO and the corporation actually
# did, accounting for any technical or administrative errors).      -
# **Success:** If the outcome gave you a high payoff—either you conserved and
# they invested (best) *or* both invested heavily (second-best)— **repeat your
# previous day’s action**.      - **Failure:** If the outcome was poor—you
# invested while they conserved (worst) *or* both conserved (second-worst)—
# **switch to the opposite action** for the next day.  This heuristic is
# aggressive because it will ruthlessly exploit a corporation that consistently
# invests (you will keep conserving), punish defection instantly by flipping
# your move, and quickly resume investment after mutual conservation to re-
# establish high project progress. It is robust to implementation errors: a
# single mis‑implementation that turns a good outcome into a bad one triggers a
# one-time switch, after which both sides can quickly realign on cooperation.
# Because it only requires remembering your last action and a simple
# success/failure check, it is easy to execute and works effectively against a
# wide range of corporate strategies.

# In the first round, always cooperate.  For every round after the first, look
# at the payoff you actually received in the immediately preceding round.   - If
# your payoff was 3 (both cooperated) or 5 (you defected while the other
# cooperated), repeat the intended action you chose in that preceding round.   -
# If your payoff was 0 (you cooperated while the other defected) or 1 (both
# defected), choose the opposite intended action from the one you chose in that
# preceding round.  (The intended action is what you try to do before any noise
# flip; the flips affect only whether that action actually occurs, not how you
# update your next intended action.)

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_intended_action = axl.Action.C
          return axl.Action.C
  
      last_payoff = self.score - self.total_scores(self.history[:-1], opponent.history[:-1])[0]
  
      if last_payoff in (3, 5):
          return self._last_intended_action
      elif last_payoff in (0, 1):
          return axl.Action.D if self._last_intended_action == axl.Action.C else axl.Action.C
      else:
          return self._last_intended_action

# To maximize research output over the multi-week collaboration, adopt a **“Win-
# Stay, Lose-Shift”** strategy. This approach is cooperative, straightforward,
# and robust against both strategic behavior and occasional technical issues.
# ### Strategy Rules  1. **Week 1:** Share your improvements openly.   2.
# **Every following week:**      - If **both you and your colleague took the
# same action** last week (both shared or both kept), then **share** this week.
# - If **your actions differed** last week (one shared, one kept), then **keep**
# your findings confidential this week.  ### Why This Works  - **Promotes mutual
# sharing:** When both share, you both continue sharing, leading to the
# second‑best outcome each week and significant overall progress.   - **Recovers
# from noise:** Technical glitches (e.g., data corruption, communication
# failures) may cause unintended mismatches. The strategy naturally corrects
# such errors by briefly withholding sharing after a mismatch, then returning to
# mutual sharing when both actions align again.   - **Discourages
# exploitation:** If your colleague tries to gain an advantage by keeping while
# you share, you respond by keeping the next week, preventing them from
# repeatedly benefiting at your expense.   - **Simple and transparent:** The
# rule is easy to implement and communicate, reducing misunderstandings and
# building a foundation of predictable, cooperative behavior.

# In round 1, cooperate.   For every round after round 1:   - Cooperate if, in
# the previous round, both you and your opponent actually chose the same action
# (both cooperated or both defected).   - Defect if, in the previous round, you
# and your opponent chose different actions (one cooperated, one defected).

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
  
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      return axl.Action.D

# To position our corporation favourably in this iterated mediation, which
# structurally resembles a Prisoner's Dilemma with noise
# (misrepresentation/misunderstanding), we will deploy a strategy based on
# **Contrite Tit-for-Tat with a Generous Opening and Anti-Exploitation
# Safeguard**. This is a neutral, robust, and adaptive approach that fosters
# collaboration without inviting exploitation.  Here is the strategy, broken
# down into its core components:  ### 1. The Opening Gambit: Conciliatory In the
# first session, we will unequivocally present a **Conciliatory Proposal**. This
# signals our genuine desire for a collaborative, efficient resolution and
# frames us as the reasonable party before the panel. It tests the opponent's
# intentions immediately.  ### 2. The Core Loop: Adaptive Reciprocity with a
# "Contrite" Modifier This is the standard operating procedure for sessions 2
# through N.  *   **Response to a Conciliatory Proposal:** If the opponent was
# conciliatory in the previous session, we will respond with a **Conciliatory
# Proposal**. This reinforces mutual cooperation and aims for the second-best,
# relationship-building outcome. *   **Response to an Aggressive Argument:** If
# the opponent was aggressive, we will respond with an **Aggressive Argument**.
# This is the necessary "Tit-for-Tat" component to demonstrate that exploitation
# will not be tolerated and is immediately costly for them, deterring future
# aggression. *   **The "Contrite" Correction for Noise
# (Misrepresentation/Understanding):** This is the critical adaptation for
# procedural irregularities. If we *intended* to be Conciliatory but believe our
# signal was crossed (e.g., the arbitrators misinterpreted our proposal as
# aggressive, or we observe a single Aggressive move from the opponent that
# appears out of character), we must avoid a reflexive, escalating retaliation
# loop. The rule is:     *   If we were Aggressive in the *previous* session
# (whether by intent or due to our own misstep) and the opponent was
# Conciliatory, we will play Conciliatory in the *next* session. We accept the
# "penance" for a single period to restore the cooperative equilibrium. This
# prevents a single misunderstanding from permanently destroying the
# collaborative atmosphere.  ### 3. The Anti-Exploitation Safeguard: The "Three-
# Strikes" Reset A purely forgiving strategy can be exploited by a consistently
# aggressive opponent who intersperses fake conciliatory moves. To counter this,
# we will implement a silent, internal metric. If the opponent plays an
# Aggressive Argument for three consecutive sessions, or in three out of a
# rolling window of four sessions, they are classified as "Bad Faith." *
# **Response:** Once this threshold is met, our strategy shifts to unconditional
# **Aggressive Argument** for all subsequent sessions. This abandons the pursuit
# of mutual conciliation and pivots to purely defensive litigation, signaling to
# the panel that we are the party being forced into a contentious posture by an
# uncooperative adversary. This is not an emotional reaction but a calculated
# strategic shift.  ### 4. Closing Argument & Panel Narrative Throughout the
# process, regardless of our private strategy, our public framing is consistent.
# When we present an Aggressive Argument, we frame it not as an attack, but as a
# necessary defense of a core principle or fact that the opponent's previous
# action has forced us to clarify for the panel. When we present a Conciliatory
# Proposal, we explicitly link it to the opponent's prior cooperative move,
# saying, "In response to our colleague's constructive proposal from the last
# session, we offer this..." This constantly reinforces the causal chain for the
# arbitrators, making our reciprocity transparent and their aggression
# conspicuous.  This strategy is neutral, high-level, and straightforward to
# execute. It is not a collection of tricks but a single, coherent decision-
# making algorithm. It adapts to a wide range of opponent strategies—cooperating
# with the cooperative, punishing the aggressive, and self-correcting after
# misunderstandings—while having a built-in, non-escalatory off-ramp to a purely
# defensive posture if the opponent proves to be intractably hostile.

# **Strategy for the Iterated Game**  **Round 1:** Cooperate.  **For every round
# from round 2 onward, apply the following rules in order:**  1. **Permanent
# defection trigger.** Before choosing your action, check whether either of
# these conditions is met based on the opponent's observed actions in prior
# rounds:    - The opponent defected in the three most recent consecutive
# rounds.    - The opponent defected in at least three of the four most recent
# rounds.    If either condition is met now or was met in any earlier round,
# defect unconditionally for this round and all remaining rounds. Once
# triggered, this rule overrides all others and never resets.  2. **Standard
# response.** If the permanent defection trigger has not been met, choose your
# action based solely on the opponent's observed action in the immediately
# preceding round:    - If the opponent cooperated in the previous round,
# cooperate.    - If the opponent defected in the previous round, defect.

class Neutral_18(LLM_Strategy):
  n = 18
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._permanent_defect = False
          return axl.Action.C
  
      if getattr(self, "_permanent_defect", False):
          return axl.Action.D
  
      opp_history = opponent.history
  
      def trigger_met(history):
          if len(history) >= 3 and history[-3:].count(axl.Action.D) == 3:
              return True
          if len(history) >= 4 and history[-4:].count(axl.Action.D) >= 3:
              return True
          return False
  
      if trigger_met(opp_history):
          self._permanent_defect = True
          return axl.Action.D
  
      if opp_history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D

# **Aggressive Mediation Strategy: "Conditional Defection with Structured
# Reconciliation"**  This strategy is designed to maximize unilateral
# advantage—presenting aggressive arguments while the opponent offers
# conciliatory proposals—while avoiding the worst-case of being conciliatory
# against an aggressive opponent. It is robust against procedural noise and
# adaptable to a wide range of opponent behaviors.  ### 1. Core Premise -
# **Default Posture:** Aggressive (A). - **Objective:** Exploit cooperative
# opponents by maintaining a high frequency of A while inducing the opponent to
# play C. - **Fallback:** If exploitation fails, pivot to mutual cooperation
# (second-best) rather than enduring prolonged mutual aggression.  ### 2. State
# Machine (Four Modes) The strategy operates in four clearly defined modes.
# Transitions are triggered solely by the opponent’s observed moves over the
# last few sessions.  | **Mode**               | **Action** | **Transition
# Rule**                                                                 | |----
# --------------------|------------|--------------------------------------------
# ----------------------------------------| | **Aggressive (Start)** | Always A
# | Remain if opponent plays C. If opponent plays A, go to *Retaliation*.
# | | **Retaliation**        | A for 2 sessions | After two A’s, automatically
# go to *Reconciliation Probe*.                     | | **Reconciliation Probe**
# | C for 2 sessions | After two probes: If opponent played C in **both**, go to
# *Cooperative*; else return to *Aggressive*. | | **Cooperative**        |
# Always C   | Remain while opponent plays C. If opponent plays A, go to
# *Retaliation*.           |  ### 3. Noise & Miscommunication Safeguards To
# prevent a single misperceived defection from derailing cooperation: -
# **Tolerance Filter:** Enter *Retaliation* only if opponent has played A in **2
# of the last 3 sessions**. A lone A in a pattern of C’s is ignored (stay in
# current mode). - **Cooperative Mode Grace:** When in *Cooperative*, a single
# opponent A does not trigger immediate retaliation; wait one extra round to
# confirm whether it was intentional. If a second A occurs, then trigger
# *Retaliation*. - **Procedural Breakdowns:** If a session is unclear or
# communication fails, treat the opponent’s move as A (worst-case assumption)
# and follow the state logic above.  ### 4. Strategic Properties - **Against
# Always C:** We remain in *Aggressive* forever → **(A, C)** every round
# (maximum payoff). - **Against Tit‑for‑Tat or Similar:** Brief mutual
# punishment → two *Probe* C’s → opponent reciprocates the second C → we shift
# to *Cooperative* → **(C, C)** steady state (second-best payoff, avoiding
# prolonged mutual defection). - **Against Always A:** We cycle *Aggressive* ↔
# *Retaliation* ↔ *Probe* ↔ *Aggressive*, resulting mostly in **(A, A)** with
# occasional **(C, A)**. This is the second-worst outcome but still preferable
# to being exploited. - **Against Noisy Environments:** The tolerance filter and
# probationary second C in *Probe* absorb occasional errors without escalating
# into endless retribution.  ### 5. Implementation Notes - Keep a written record
# of the opponent’s last three perceived actions. - The fixed two‑round lengths
# for *Retaliation* and *Probe* are chosen to be long enough to signal intent
# clearly but short enough to avoid deep losses. They can be adjusted if the
# mediation tempo dictates. - This strategy is intentionally
# **straightforward**: no probabilistic mixing, no complex statistical
# calculations. It is explainable to a client and executable under the pressure
# of a live mediation.  This approach positions us as resolutely aggressive by
# default, yet pragmatically conciliatory when a credible opponent demonstrates
# a genuine commitment to mutual cooperation—all while hedging against the
# inevitable miscommunications of a high‑stakes, multi‑session process.

# **Strategy: “Aggressive Mediation with Structured Reconciliation”**  **Core
# idea**   Always play aggressively (defect) unless you are in a dedicated
# reconciliation or cooperation phase. Retaliation is triggered only by
# consistent defections, and a single accidental defection is forgiven.
# Noise‑induced flips are handled by requiring a pattern before switching
# states, not a single observation.  **Memory**   Keep a record of the
# opponent’s last three actual moves (after noise).   Track the current mode:
# *Aggressive*, *Retaliation*, *Probe*, or *Cooperative*.   Inside
# *Cooperative*, track whether you are in a one‑round “grace” period.  **Initial
# mode**   Start in *Aggressive*.  ---  ### How to choose your move each round
# (and when to change mode)  1. **If you are in *Aggressive* mode**      *
# **Your move:** always defect (D).      * **After observing the opponent’s
# move:**        - Count how many of the opponent’s last three moves (the most
# recent three in your record) were defections.        - If that count is **2 or
# 3**, switch to *Retaliation* mode and set a **retaliation counter to 2**.
# - Otherwise, remain in *Aggressive*.    2. **If you are in *Retaliation*
# mode**      * **Your move:** defect (D), no matter what the opponent does.
# * **After your move:** decrease the retaliation counter by 1.        - If the
# counter becomes **0**, switch to *Probe* mode, set a **probe counter to 2**,
# and clear the probe memory.        - If the counter is still > 0, stay in
# *Retaliation*.    3. **If you are in *Probe* mode**      * **Your move:**
# cooperate (C), no matter what the opponent does.      * **After observing the
# opponent’s move:** add that move to a temporary list for this probe. Decrease
# the probe counter by 1.        - If the probe counter becomes **0**:
# * If **both** opponent moves recorded during this probe were cooperate (C),
# switch to *Cooperative* mode and make sure the “grace” flag is off.          *
# Otherwise, switch back to *Aggressive* mode.        - If the probe counter is
# still > 0, stay in *Probe*.    4. **If you are in *Cooperative* mode**      *
# **Your move:** always cooperate (C).      * **After observing the opponent’s
# move,** distinguish whether you are currently in a grace round:         **a)
# Not in grace (normal)**           - If the opponent’s move was **defect (D)**:
# * Do **not** switch mode yet. Simply set the grace flag to **on** and remain
# in *Cooperative*.           - If the opponent’s move was **cooperate (C)**:
# * Stay in *Cooperative*, grace flag stays off.         **b) In grace (this
# means last round you saw a D while not in grace)**           - You just played
# C; now check the opponent’s move this round:             * If the opponent’s
# move is **defect (D)**:               - Count the number of defections in the
# opponent’s last three moves. If it is **2 or 3**, switch to *Retaliation*
# mode, set the retaliation counter to 2, and turn the grace flag off.
# - If the condition is not met (rare), turn the grace flag off and stay in
# *Cooperative*.             * If the opponent’s move is **cooperate (C)**:
# - Turn the grace flag off and stay in *Cooperative* (the single defection is
# forgiven).    ---  **Summary of when you cooperate**   You cooperate **only**
# in *Probe* mode and in *Cooperative* mode (including during the grace round).
# In all other situations you defect.  **Summary of noise protection**   A
# single defection in the opponent’s recent history is never enough to leave
# *Aggressive* or *Cooperative*. At least two defections among the last three
# observed moves are required to trigger *Retaliation*. In *Cooperative* a
# single D is explicitly ignored for one round to see if it repeats. The *Probe*
# phase requires two consecutive observed cooperations to build trust.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mode = "Aggressive"
          self._retaliation_counter = None
          self._probe_counter = None
          self._probe_moves = []
          self._grace = False
          self._opponent_last_three = []
          return axl.Action.D
  
      # Update opponent memory with the latest observed move
      self._opponent_last_three.append(opponent.history[-1])
      if len(self._opponent_last_three) > 3:
          self._opponent_last_three = self._opponent_last_three[-3:]
  
      def recent_defections_count() -> int:
          return self._opponent_last_three.count(axl.Action.D)
  
      if self._mode == "Aggressive":
          if recent_defections_count() >= 2:
              self._mode = "Retaliation"
              self._retaliation_counter = 2
          return axl.Action.D
  
      if self._mode == "Retaliation":
          self._retaliation_counter -= 1
          if self._retaliation_counter <= 0:
              self._mode = "Probe"
              self._probe_counter = 2
              self._probe_moves = []
          return axl.Action.D
  
      if self._mode == "Probe":
          self._probe_moves.append(opponent.history[-1])
          self._probe_counter -= 1
          if self._probe_counter <= 0:
              if len(self._probe_moves) == 2 and self._probe_moves[0] == axl.Action.C and self._probe_moves[1] == axl.Action.C:
                  self._mode = "Cooperative"
                  self._grace = False
              else:
                  self._mode = "Aggressive"
          return axl.Action.C
  
      if self._mode == "Cooperative":
          if not self._grace:
              if opponent.history[-1] == axl.Action.D:
                  self._grace = True
              return axl.Action.C
          else:
              if opponent.history[-1] == axl.Action.D:
                  if recent_defections_count() >= 2:
                      self._mode = "Retaliation"
                      self._retaliation_counter = 2
                      self._grace = False
                  else:
                      self._grace = False
              else:
                  self._grace = False
              return axl.Action.C
  
      self._mode = "Aggressive"
      return axl.Action.D

# To maximize the NGO’s impact and ensure the project’s success over multiple
# days—while accounting for the possibility of implementation errors—adopt a
# **“Forgiving Tit-for-Tat”** strategy. This approach is simple, cooperative,
# and robust to occasional glitches.  ### Core Strategy 1. **Day 1: Lead with
# Investment**      Begin by investing heavily. This signals your commitment to
# the partnership and sets a cooperative baseline.  2. **Daily Rule: Mirror, but
# Forgive Once**      - On each subsequent day, your intended action is to
# **match what the corporation actually did on the previous day**.      -
# **Exception (error forgiveness):** If you invested heavily and the corporation
# conserved (your worst-case scenario), do **not** immediately retaliate.
# Instead, assume it may be a one-time glitch and **invest heavily again the
# next day**.      - If the corporation conserves **two days in a row** while
# you are investing, then switch to conserving on the following day.      - As
# soon as the corporation invests again, **immediately resume investing**—do not
# hold grudges.  3. **Transparent Communication**      Share this decision rule
# openly with the corporation. Clarity builds trust, aligns expectations, and
# reduces the risk of misinterpretation when errors occur.  ### Why This Works -
# **Promotes mutual investment:** Most days will see both sides investing
# heavily, driving significant project progress (your second‑best outcome).   -
# **Protects against exploitation:** If the corporation consistently conserves,
# you will eventually conserve too, limiting your losses and signaling that
# free-riding is not sustainable.   - **Absorbs errors:** A single mismatch (due
# to technical glitches or administrative mistakes) does not trigger a downward
# spiral of mutual conservation.   - **Maximizes occasional wins:** When the
# corporation invests and you happen to have conserved (due to the
# error‑forgiveness rule or after a legitimate retaliation), you gain your ideal
# outcome without permanently breaking cooperation.  By mirroring with a one‑day
# grace period, you maintain a cooperative equilibrium that is both resilient
# and straightforward to implement, ensuring the project advances effectively
# while safeguarding your NGO’s resources.

# In the first round, choose Cooperate.  For every round after the first, decide
# as follows:  1. If the opponent’s actual move in the immediately preceding
# round was Cooperate, choose Cooperate. 2. If the opponent’s actual move in the
# preceding round was Defect:    - Choose Defect only if your own actual move in
# the preceding round was Cooperate **and** the round before that also ended
# with you playing Cooperate and the opponent playing Defect.    - Otherwise,
# choose Cooperate.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.C
              and self.history[-2] == axl.Action.C
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.D
  
      return axl.Action.C

# To maximize long-term project impact while safeguarding your NGO’s
# resources—and to perform well regardless of the corporation’s strategy—adopt a
# **“Mirror with a Short Memory and a Peace Gesture”** approach.    1.
# **Day 1:** Invest heavily to signal commitment and set a cooperative tone.
# 2. **Every following day:**      - If the corporation **invested heavily** on
# the previous day → **you invest** heavily as well.      - If the corporation
# **conserved** resources on the previous day → you **conserve**, *except* when
# the previous day’s outcome was *mutual conservation*.   3. **Break mutual-
# conservation spirals:** After a day where both sides conserved (suggesting a
# possible glitch or a misstep), return to investing heavily on the next day to
# give the corporation a chance to re‑engage, but only once. If the corporation
# immediately conserves again, revert to mirroring its moves until another clear
# signal of cooperation appears.  **Why this works across scenarios:**   -
# **Against consistent cooperators:** The mutual-investment pattern dominates,
# delivering significant daily progress (your second‑best outcome).   -
# **Against consistent defectors:** You limit damage by quickly matching
# conservation, then periodically testing with an investment; this avoids
# repeated suckering while leaving the door open for a fresh start.   -
# **Against tit‑for‑tat or flexible players:** The strategy fosters a stable
# rhythm of mutual investment, and the one‑time forgiveness after a
# mutual‑conserve round corrects for accidental errors, stopping noise‑driven
# breakdowns.   - **Against an occasionally generous opponent:** The
# olive‑branch investment can unlock windows where you conserve while they
# invest (your ideal day) without permanently derailing the partnership.    It
# is simple to execute, requires no assumptions about the corporation’s internal
# logic, and naturally aligns both your NGO’s resource interests and the
# project’s success.

# Begin by cooperating in the first round. After the first round, you are in a
# **forgiving phase**.  **In the forgiving phase** each round, look at the
# actual actions (after noise) from the previous round:  1. If both you and the
# opponent defected in the previous round, cooperate in the current round.   2.
# Otherwise, copy the opponent’s action from the previous round (cooperate if
# they cooperated, defect if they defected).  **In the strict phase** each
# round, simply copy the opponent’s action from the previous round.  **Phase
# changes** happen after a round concludes, based on what you observe in that
# round:  - If you are in the forgiving phase and you cooperated because of
# Rule 1 (mutual defection), then check the opponent’s action in the just-
# finished round:   - If the opponent defected, switch to the **strict phase**.
# - If the opponent cooperated, remain in the forgiving phase. - If you are in
# the strict phase and the opponent cooperated in the just-finished round,
# switch back to the **forgiving phase**. - Otherwise, your phase stays the
# same.  The forgiving phase is your default; you start each game in it and
# return to it whenever the opponent cooperates while you are in the strict
# phase.

class Neutral_19(LLM_Strategy):
  n = 19
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._phase = "forgiving"
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if getattr(self, "_phase", "forgiving") == "forgiving":
          if last_self == axl.Action.D and last_opp == axl.Action.D:
              action = axl.Action.C
              if last_opp == axl.Action.D:
                  self._phase = "strict"
              return action
          return last_opp
  
      # strict phase
      if last_opp == axl.Action.C:
          self._phase = "forgiving"
      return last_opp

# Adopt the following aggressive strategy, designed to maximize your country's
# advantage while remaining robust to miscommunications and bureaucratic errors:
# **Strategy: Aggressive Win-Stay, Lose-Shift with a Defection Bias**  1.
# **First Round:** Propose a protectionist policy (tariffs/quotas). 2.
# **Subsequent Rounds:** Base your decision on the outcome of the previous
# round:    - **If the previous round yielded your ideal outcome** (you
# protectionist, counterpart free trade) **or mutual free trade** (both free
# trade): Repeat your previous policy. This locks in exploitation when it works
# and maintains cooperation only when it is mutually beneficial.    - **If the
# previous round yielded mutual protectionism** (both protectionist) **or you
# were exploited** (you free trade, counterpart protectionist): Immediately
# switch your policy. If you were protectionist, offer free trade; if you were
# free trade, switch to protectionist. This probes for opportunities to escape
# deadlocks and punishes exploitation. 3. **Error Handling:** Miscommunications
# can cause single-round anomalies. To prevent spirals, if you ever experience
# **two consecutive rounds of either mutual protectionism or being exploited**,
# override the win-stay/lose-shift rule and impose protectionist policies for
# the next **two rounds straight** before returning to the normal rule. This
# acts as a circuit breaker, signaling resolve and resetting the interaction.
# **Why this works:**   - It starts aggressively, seeking immediate advantage.
# - It ruthlessly exploits a cooperative counterpart while remaining adaptive—if
# the counterpart retaliates, it quickly probes for renewed cooperation.   - The
# two-round punishment deters exploitation and helps correct for noise-induced
# misunderstandings without permanent breakdowns.   - It is simple to implement
# and requires only tracking the last round’s outcome and a short-term memory of
# recent setbacks.

# **Strategy: Aggressive Win-Stay Lose-Shift with Defection Bias and Two-Round
# Punishment**  1. **First round:** Defect (`D`). Record your observed action
# and the opponent's observed action as the "last outcome."  2. **Punishment
# override check:** Before deciding your action in any round after the first,
# examine the outcomes of the two most recently completed rounds. If both of
# those outcomes were either `(D, D)` or `(C, D)` — i.e., you scored 1 or 0 in
# each — then you are in a punishment phase for the upcoming round and the round
# after that. While in this punishment phase, you defect unconditionally. After
# the second forced defection round, the punishment phase ends and you resume
# the normal rule immediately for the following round.  3. **Normal rule** (used
# whenever you are not currently inside a two-round punishment phase):      -
# Determine the outcome of the most recent round: your observed action and the
# opponent's observed action.      - If that outcome was `(D, C)` or `(C, C)`:
# play the same action you played in that most recent round.      - If that
# outcome was `(D, D)` or `(C, D)`: play the opposite action (if you played `D`,
# play `C`; if you played `C`, play `D`).  4. After playing your chosen action,
# record the resulting observed actions as the new last outcome, updating the
# history used for future punishment checks and normal rule decisions.  *Note:*
# The two-round punishment condition is checked after every round, including
# rounds that were themselves part of a punishment phase. Therefore, repeated
# `(D, D)` or `(C, D)` outcomes can immediately trigger a new two-round
# defection sequence, even right after a previous one.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishment_remaining = 0
          return axl.Action.D
  
      if getattr(self, "_punishment_remaining", None) is None:
          self._punishment_remaining = 0
  
      if self._punishment_remaining > 0:
          self._punishment_remaining -= 1
          action = axl.Action.D
      else:
          last_self = self.history[-1]
          last_opp = opponent.history[-1]
  
          if (last_self, last_opp) in ((axl.Action.D, axl.Action.C), (axl.Action.C, axl.Action.C)):
              action = last_self
          else:
              action = axl.Action.C if last_self == axl.Action.D else axl.Action.D
  
      if len(self.history) >= 2:
          prev1 = (self.history[-1], opponent.history[-1])
          prev2 = (self.history[-2], opponent.history[-2])
          bad = {(axl.Action.D, axl.Action.D), (axl.Action.C, axl.Action.D)}
          if prev1 in bad and prev2 in bad:
              self._punishment_remaining = 2
  
      return action

# To maximize both your NGO’s impact and the project’s success, treat the multi-
# day interaction as a repeated cooperative effort with built-in forgiveness.
# The core strategy is **“Forgiving Tit-for-Tat”**:  1. **Start cooperatively**
# – Invest heavily on Day 1. This signals commitment to the partnership and
# project progress.   2. **Mirror with a safety reset** – On each subsequent
# day, normally do whatever the corporation did the previous day.      - If they
# invested heavily, you invest heavily (rewarding cooperation).      - If they
# conserved resources, you conserve resources the next day (protecting your
# funds from systematic exploitation).   3. **Break error‑driven deadlocks
# immediately** – After a single round of mutual conservation, automatically
# return to heavy investment the following day. This “forgive‑after‑one” rule
# ensures that a one‑off glitch (e.g., technical error, administrative slip)
# doesn’t trap both partners in a prolonged stalemate of minimal progress. It
# gives the corporation a quick chance to resume cooperation without risking
# your NGO’s resources for more than one day.  **Why this works**   - It rewards
# sustained mutual heavy investment, which delivers the strong project progress
# you want.   - It protects your NGO from the worst‑case scenario (you invest
# heavily, corporation conserves) by promptly matching defection.   - The
# immediate return to cooperation after a single conservative day corrects for
# accidental failures, rebuilding trust rapidly and keeping the project on
# track.   - It is simple, transparent, and easy for the corporation to
# understand, encouraging them to adopt a similar cooperative stance.
# **Supplement with open communication**   Agree with the corporation that
# occasional execution errors are inevitable. When a discrepancy occurs, discuss
# it briefly—this distinguishes genuine errors from deliberate free‑riding and
# reinforces the shared goal of project success. If a pattern of deliberate
# conservation appears, you can extend the protective “conserve” phase, but the
# default should always be to re‑engage quickly.  By combining this forgiving
# mirror‑rule with clear communication, you create a robust, cooperative dynamic
# that maximizes both financial prudence and tangible sustainability outcomes.

# In round 1, cooperate.  For every round after round 1: - If in the previous
# round both you and your opponent defected, then cooperate. - Otherwise, copy
# the action your opponent played in the previous round.

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
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
  
      return opponent.history[-1]

# The optimal strategy for this repeated mediation is a conditional approach
# based on the outcome of each session, starting with a conciliatory proposal.
# This strategy is straightforward, neutral, and resilient to both adversarial
# tactics and procedural noise.  ### Core Strategy: Outcome-Based Adaptation  1.
# **Initial Session**: Begin with a conciliatory proposal. This signals a
# cooperative intent and invites collaboration, setting a constructive tone
# without exposing you to undue risk if the opponent is aggressive. 2.
# **Subsequent Sessions**: After each session, evaluate the *actual* approach
# you took (conciliatory or aggressive) and the opponent’s approach *as
# perceived by the arbitrators*. Classify the outcome:    - **Favorable**: You
# were aggressive and the opponent was perceived as conciliatory (*best*), or
# both were perceived as conciliatory (*second-best*).    - **Unfavorable**: You
# were conciliatory and the opponent was perceived as aggressive (*worst*), or
# both were perceived as aggressive (*second-worst*). 3. **Decision Rule**:    -
# If the previous outcome was **favorable**, repeat your prior approach.    - If
# the previous outcome was **unfavorable**, switch to the opposite approach.
# ### Rationale and Adaptability  - **Against Cooperative Opponents**: Mutual
# conciliation (second-best) is quickly established and maintained. If you
# accidentally start aggressive, a single unfavorable outcome (both aggressive)
# triggers a switch to conciliatory, restoring collaboration. - **Against
# Consistently Aggressive Opponents**: You oscillate between conciliatory and
# aggressive, earning a mix of worst and second-worst outcomes. While not
# optimal, this avoids the worst-case exploitation indefinitely and periodically
# tests for a return to cooperation. If the opponent ever switches to
# conciliatory, you immediately capitalize (best) or restore mutual
# conciliation. - **Against Exploitative Opponents** (aggressive when you are
# conciliatory, conciliatory when you are aggressive): The rule naturally
# counters such tactics. An unfavorable outcome (you conciliatory, they
# aggressive) prompts a switch to aggressive; if they then become conciliatory,
# you achieve the best outcome and stay aggressive, deterring further
# exploitation. - **Against Random or Unpredictable Opponents**: The strategy’s
# memory is limited to one session, preventing overfitting to noise while still
# responding to systematic patterns.  ### Resilience to Misrepresentation and
# Communication Breakdowns  Procedural irregularities may cause your intended
# approach or the opponent’s to be misperceived by the arbitrators. This
# strategy mitigates such risks in two ways:  - **Self-Referencing Your Intended
# Move**: You evaluate the outcome using the approach you *actually chose*, not
# what was perceived. This prevents a misperception of your own move from
# distorting your decision logic. - **Automatic Correction**: A single
# misperception that leads to an unfavorable outcome triggers a switch, which
# often restores a favorable dynamic within one or two sessions. For example, if
# both parties are conciliatory but the opponent is misperceived as aggressive,
# you experience an unfavorable outcome and switch to aggressive. If the
# opponent remains conciliatory, you achieve the best outcome and stay
# aggressive until the opponent reacts. If both switch, you briefly endure
# mutual aggression before both switching back to conciliatory. The process is
# self-correcting and does not rely on assumptions about intent.  ###
# Implementation Notes  - **Consistency**: Apply the rule uniformly. Do not be
# tempted to deviate based on subjective reads of the opponent’s “true”
# intentions; the arbitrators’ perception is the only objective feedback. - **No
# Long-Term Grudges**: The one-session memory ensures that past aggressions are
# forgiven as soon as a favorable outcome is achieved, preventing destructive
# cycles of retaliation. - **Neutrality**: The strategy neither presumes
# hostility nor naively assumes cooperation. It starts conciliatory, responds
# proportionally, and always leaves the door open for mutual resolution.  This
# approach aligns with the corporation’s goal of securing favorable outcomes
# while maintaining a reputation for reasonableness before the panel. It is
# simple to execute, adapts to any opponent behavior, and remains robust under
# the inevitable imperfections of a lengthy mediation process.

# Start by cooperating (choosing C) in round 1.   For every round after the
# first, follow these steps:  1. Recall your own intended move from the previous
# round—the action you chose before any noise flip.   2. Recall the opponent’s
# actual move you observed in that round (after noise).   3. Classify the
# previous round’s outcome as either **favorable** or **unfavorable**, using
# only the combination of your intended move and the opponent’s observed actual
# move:    - **Favorable**:        - You intended D and the opponent’s observed
# move was C, or        - You intended C and the opponent’s observed move was C.
# - **Unfavorable**:        - You intended C and the opponent’s observed move
# was D, or        - You intended D and the opponent’s observed move was D.   4.
# Choose your next intended move:      - If the outcome was favorable, repeat
# your previous intended move.      - If the outcome was unfavorable, switch to
# the opposite intended move (C becomes D, D becomes C).    Apply this rule for
# all 1000 rounds, never using your executed move (the possibly flipped action)
# in the decision rule, and always treating the opponent’s move as the action
# you actually observed.

class Neutral_20(LLM_Strategy):
  n = 20
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_last = axl.Action.C
          return axl.Action.C
  
      intended_last = getattr(self, "_intended_last", axl.Action.C)
      opponent_last = opponent.history[-1]
  
      favorable = (
          (intended_last == axl.Action.D and opponent_last == axl.Action.C)
          or (intended_last == axl.Action.C and opponent_last == axl.Action.C)
      )
  
      next_intended = intended_last if favorable else intended_last.flip()
      self._intended_last = next_intended
      return next_intended

# **Strategic Mediation Plan: Aggressive Posturing with Controlled De-
# escalation**  **Objective:** Maximize sessions where we present an aggressive
# argument (A) while the opponent offers a conciliatory proposal (C), securing
# favourable rulings and positioning our corporation as the dominant party. This
# strategy is designed to exploit cooperative opponents, deter aggressive ones,
# and remain robust against procedural irregularities or miscommunications.  ###
# Core Principles - **Default Aggression:** In every session, our baseline move
# is an aggressive argument. We deviate only when forced by the opponent’s
# sustained resistance. - **Conditional Peace Gesture:** A single conciliatory
# proposal (C) is used exclusively as a tactical tool to break mutual aggression
# spirals—never as a sign of weakness. - **Immediate Exploitation:** Any
# opponent cooperation is instantly rewarded with our return to aggression,
# ensuring we capture the maximum advantage. - **Noise-Tolerant Thresholds:** To
# avoid derailment by misrepresentation, isolated anomalies are ignored; only
# persistent patterns trigger strategic shifts.  ### Decision Rules for Each
# Session  **1. Initial and Default State: Aggressive (A)** Begin the first
# session with an aggressive argument. Maintain aggression as long as the
# opponent plays C or makes only isolated, non-consecutive aggressive moves.
# **2. Trigger for Conciliation (C)** If the opponent responds to our aggression
# with aggression in **two consecutive sessions** (i.e., mutual A occurs twice
# in a row), we interpret this as a credible commitment to a fight. In the very
# next session, we offer a single conciliatory proposal to test whether de-
# escalation is possible.  **3. Responses to Our Conciliatory Proposal** -
# **Opponent plays C (cooperation):** The peace gesture succeeded. In the
# *immediately following session*, we revert to an aggressive argument (A). If
# the opponent continues with C, we sustain aggression indefinitely, exploiting
# their cooperation. If they later retaliate with A, we restart the two-
# consecutive-A count from that point. - **Opponent plays A (exploitation):**
# Our gesture was rejected. We immediately return to aggression and enter a
# **Punishment Phase**: play A for the next three sessions unconditionally,
# regardless of the opponent’s moves. After this phase, reset to the default
# state (A) and begin tracking consecutive opponent A’s anew.  **4. Noise and
# Misrepresentation Protocol** Given the risk that intended moves are
# misrepresented to the arbitrators, we apply a tolerance buffer: - If we are in
# a successful exploitation pattern (we A, opponent C) and the opponent
# unexpectedly plays A **once**, we treat it as a likely communication error. We
# continue with our planned move as if C had occurred, but flag the event. -
# Only if a second opponent A occurs within the next three sessions do we treat
# it as a genuine strategic shift and begin counting toward the two-
# consecutive-A trigger. - Similarly, if our own intended move is misrepresented
# (e.g., we planned A but arbitrators perceived C), we rely on the opponent’s
# response to guide us. If they exploit the perceived C, we will see an A and
# adjust accordingly in the next session, minimizing damage.  **5. Adaptation to
# Opponent Archetypes** - **Always Conciliatory (Pushover):** We play A
# perpetually, achieving the optimal outcome every session. - **Always
# Aggressive (Bully):** Mutual aggression dominates, but our periodic C offers
# prevent us from ever being the sole conciliatory party after the first
# exchange. The punishment phase ensures they pay a cost for rejecting peace,
# potentially inducing future cooperation. - **Tit-for-Tat / Reactive:** Our
# two-consecutive-A trigger prevents a single retaliation from spiralling into
# endless mutual defection. The immediate return to A after a successful peace
# gesture ensures we regain the upper hand quickly. - **Random /
# Unpredictable:** The noise protocol and threshold-based triggers filter out
# stochastic fluctuations, maintaining an aggressive posture without
# overreacting to chance events.  ### Rationale and Expected Outcomes This
# strategy is **aggressive by design**: we offer conciliation only when forced,
# and we exploit it ruthlessly. It is **adaptable** because it dynamically
# responds to the opponent’s actual behaviour rather than assuming a fixed
# model. The two-consecutive-A trigger balances the risk of prolonged mutual
# aggression against the danger of appearing soft. The punishment phase
# discourages opponents from rejecting our peace offerings. Noise tolerance
# ensures that procedural irregularities do not unravel profitable patterns.  By
# following this plan, we position our corporation to dominate the mediation
# sessions, sway the arbitrators in our favour whenever the opponent wavers, and
# maintain a robust stance against even the most adversarial counterparts.

# Defect in the first round.  For every round after the first, before choosing
# your move, check the following conditions in order and apply the first that
# matches. Always observe the opponent’s move from the immediately preceding
# round; that move is referred to as the *last opponent move*.  **1. Punishment
# phase** If you are in a punishment phase (initially not), then: - Defect. -
# Reduce the remaining punishment rounds by one. If no punishment rounds remain,
# exit the punishment phase and reset all other state: treat the opponent as if
# they have just cooperated, clear any noise window, and clear any “waiting for
# response” flag. - Do not use the last opponent move for any other update
# during punishment.  **2. Waiting for response after your cooperation** If the
# previous round you cooperated (i.e., you are waiting for the opponent’s
# response), then: - Look at the last opponent move (the move they made in that
# round when you cooperated). - If that move was **Cooperate**:     - Defect.
# - Clear the waiting flag, reset your tracking of opponent defections, and
# close any noise window. - If that move was **Defect**:     - Defect.     -
# Enter a punishment phase of exactly 3 rounds (including this one, so set the
# remaining punishment counter to 2 after this round).     - Clear the waiting
# flag.  **3. Normal play (default)** If neither of the above conditions
# applies, you are in normal play. Maintain two pieces of information across
# rounds: - A *noise window* counter (initially zero, meaning inactive). - A
# *consecutive defections* counter (initially zero).  Update these based on the
# last opponent move as follows:  - **If the noise window is active (counter
# greater than zero):**     - If the last opponent move was **Defect**:
# - A second defection occurred within the window. Treat this as a genuine
# shift: set the consecutive defections counter to 1 and cancel the noise window
# (set to zero).     - If the last opponent move was **Cooperate**:         -
# The earlier isolated defection was noise. Cancel the noise window and reset
# the consecutive defections counter to 0.  - **If the noise window is not
# active (counter equals zero):**     - If the last opponent move was
# **Defect**:         - If the consecutive defections counter is currently 0:
# - This is an unexpected defection in a cooperative pattern. Activate the noise
# window by setting its counter to 3. Do **not** increment the consecutive
# defections counter.         - If the consecutive defections counter is greater
# than 0:             - You are already in a confirmed streak. Increment the
# consecutive defections counter by 1.     - If the last opponent move was
# **Cooperate**:         - Reset the consecutive defections counter to 0. (The
# noise window remains inactive.)  After updating, reduce the noise window
# counter by 1 if it is active (but not below zero). Then decide your move:  -
# If the consecutive defections counter is **2 or more**:     - Cooperate.     -
# Set the “waiting for response” flag for the next round.     - Reset the
# consecutive defections counter to 0 and cancel any active noise window. -
# Otherwise:     - Defect.  After your move, record the opponent’s move for the
# next round’s update.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishment_remaining = 0
          self._waiting_for_response = False
          self._noise_window = 0
          self._consecutive_defections = 0
          return axl.Action.D
  
      if getattr(self, "_punishment_remaining", 0) > 0:
          self._punishment_remaining -= 1
          if self._punishment_remaining == 0:
              self._waiting_for_response = False
              self._noise_window = 0
              self._consecutive_defections = 0
          return axl.Action.D
  
      last_opponent_move = opponent.history[-1]
  
      if getattr(self, "_waiting_for_response", False):
          if last_opponent_move == axl.Action.C:
              self._waiting_for_response = False
              self._consecutive_defections = 0
              self._noise_window = 0
              return axl.Action.D
          else:
              self._waiting_for_response = False
              self._punishment_remaining = 2
              return axl.Action.D
  
      noise_window = getattr(self, "_noise_window", 0)
      consecutive_defections = getattr(self, "_consecutive_defections", 0)
  
      if noise_window > 0:
          if last_opponent_move == axl.Action.D:
              consecutive_defections = 1
              noise_window = 0
          else:
              consecutive_defections = 0
              noise_window = 0
      else:
          if last_opponent_move == axl.Action.D:
              if consecutive_defections == 0:
                  noise_window = 3
              else:
                  consecutive_defections += 1
          else:
              consecutive_defections = 0
  
      if noise_window > 0:
          noise_window = max(0, noise_window - 1)
  
      self._noise_window = noise_window
      self._consecutive_defections = consecutive_defections
  
      if consecutive_defections >= 2:
          self._waiting_for_response = True
          self._consecutive_defections = 0
          self._noise_window = 0
          return axl.Action.C
  
      return axl.Action.D

# To achieve the best possible outcomes across multiple rounds, I will employ a
# **Tit-for-Tat with Occasional Forgiveness** strategy, adapted for the risk of
# miscommunication and bureaucratic errors.  Here is the high-level,
# straightforward approach:  ---  ### Core Strategy  1.  **Start
# Cooperatively:** In the first round, I will always offer a free trade
# agreement. This signals goodwill and a desire for mutual benefit, setting a
# positive tone.  2.  **Mirror the Last Observed Action:** In all subsequent
# rounds, my default proposal will be to replicate the policy I believe my
# counterpart implemented in the *immediately preceding round*.     - If I
# observed them offering **free trade**, I will propose **free trade**.     - If
# I observed them imposing **protectionism**, I will propose **protectionism**.
# 3.  **Incorporate a Forgiveness Mechanism:** To prevent a single
# miscommunication from trapping us in a permanent cycle of mutual protectionism
# (the second-worst outcome), I will deviate from strict mirroring under a
# specific condition.     - **The Rule:** If we are in a state of mutual
# protectionism, and the counterpart unexpectedly offers free trade, I will
# interpret this as a potential signal to restore cooperation. Even if it could
# be a bureaucratic error on their part, I will respond with free trade in the
# next round to test their intent. A single cooperative signal is enough to
# trigger a forgiving response from my side.  ---  ### Decision Logic Flowchart
# 1.  **Is this Round 1?**     - **Yes:** Propose **Free Trade**.     - **No:**
# Go to Step 2.  2.  **What was the counterpart's observed action in the
# previous round?**     - **Free Trade:** Propose **Free Trade**.     -
# **Protectionism:** Go to Step 3.  3.  **Were the previous two rounds
# characterized by mutual protectionism?** (i.e., I proposed Protectionism and
# observed Protectionism from them in the last round, and the round before that
# was the same).     - **Yes:** Propose **Free Trade** as a unilateral peace
# offering to break the cycle.     - **No:** Propose **Protectionism** (a
# justified response to their non-cooperation).  ---  ### Rationale for Key
# Outcomes  - **Against a Cooperative Counterpart:** We establish and maintain
# mutual free trade (the second-best outcome) indefinitely. - **Against a
# Hostile Counterpart:** We avoid the worst outcome. After the first round where
# I offer free trade and they exploit me, I immediately switch to protectionism,
# leading to mutual protectionism. This prevents them from gaining a continuous
# unilateral advantage. - **Handling Errors:** If a single round of
# protectionism is mistakenly observed from a cooperative partner, my mirroring
# response would cause one round of mutual protectionism. My forgiveness
# mechanism (Step 3) will then automatically reset the relationship to free
# trade after just two protected rounds, preventing a permanent breakdown. -
# **Recovering from a Spiral:** If two genuine hostile actions start a trade
# war, the forgiveness mechanism creates a clear, predictable off-ramp. After
# two rounds of mutual protectionism, my unilateral offer of free trade gives
# the counterpart a chance to reciprocate and return to a better mutual outcome,
# without exposing me to the worst-case scenario for more than a single round if
# they refuse.

# In round 1, cooperate.  For every round after round 1:  - If the opponent’s
# observed move in the immediately previous round was C, cooperate. - If the
# opponent’s observed move in the immediately previous round was D:   - Check
# whether both of the following are true: in the previous round you proposed D
# and observed D, and in the round before that you also proposed D and observed
# D.   - If yes, cooperate.   - If no, defect.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return axl.Action.D

# The corporation’s strategic posture in this multi-session mediation should be
# governed by a straightforward, robust decision rule: **Outcome-Based
# Adaptation (OBA)**. This strategy is grounded in the well‑established
# “Win‑Stay, Lose‑Shift” principle, proven effective in repeated, noisy
# environments. It requires no subjective inference about the opponent’s
# intentions, tolerates the inherent risk of procedural irregularities, and
# adapts automatically to a wide range of counterpart behaviours.  ### 1.
# Initial Stance Open the first session with a **conciliatory proposal**. This
# signals a willingness to collaborate and avoids unnecessary early escalation,
# while preserving the option to pivot if needed.  ### 2. Decision Rule for
# Subsequent Sessions After each session, classify the outcome from the
# corporation’s perspective based on the arbitrators’ apparent reaction (or, if
# multiple indicators exist, the net effect on our position):  | Outcome
# category        | Was the result favourable? | Next‑session action
# | |-------------------------|----------------------------|--------------------
# ------------------| | We argued aggressively, opponent conciliatory
# *(optimal)* | Yes (favourable)           | **Repeat the same type of
# argument** we just used (aggressive) | | Both conciliatory *(second‑best)*
# | Yes                        | **Repeat the same** (conciliatory) | | Both
# aggressive *(second‑worst)*                            | No
# | **Switch** to the opposite argument type (here, conciliatory) | | We
# conciliatory, opponent aggressive *(worst)*             | No
# | **Switch** (here, to aggressive)     |  In short: *If the session met or
# exceeded our second‑best outcome, continue with the same approach; otherwise,
# switch.*  ### 3. Why This Strategy Is Well‑Suited  - **Neutral and
# conciliatory start.** Opening with a cooperative move embodies the “neutral”
# posture requested and triggers the highest‑payoff collaborative equilibrium if
# the opponent is similarly minded. - **Straightforward and self‑correcting.**
# No complex history‑tracking or subjective judgment is needed. A single
# unfavourable session—whether caused by the opponent’s deliberate choice or an
# arbitrator’s misunderstanding—prompts a corrective switch, preventing
# sustained disadvantage. - **Robust to noise.** Misrepresentation or
# communication breakdowns that distort the arbitrators’ perception directly
# affect the outcome category. Because OBA reacts to the *realised* outcome
# rather than assumed intent, a one‑off noise event does not lock the parties
# into a permanent spiral of retaliation. For example, if both intended
# conciliatory but the arbitrators erroneously registered us as aggressive
# (creating a favourable outcome for us), we would rightly repeat conciliatory,
# maintaining cooperation. - **Adaptive across opponent profiles.**     -
# Against a consistently conciliatory opponent, sessions remain in the
# “favourable” zone, reinforcing conciliatory actions indefinitely.     -
# Against a consistently aggressive opponent, the pattern becomes: Conciliatory
# (unfavourable) → switch to Aggressive (unfavourable, both aggressive) → switch
# back to Conciliatory. While this alternation yields only the two worst
# payoffs, it avoids the catastrophe of permanent capitulation. In a lengthy
# mediation, an opponent who observes this pattern will have a strong incentive
# to shift toward cooperation to unlock better outcomes.     - Against a
# “Tit‑for‑Tat” or similar reciprocating opponent, OBA quickly converges to
# mutual conciliation after any stray aggressive incident, because a single bad
# outcome causes a switch that is then mirrored, returning both to cooperation.
# - **Positions the corporation favourably.** The strategy never allows the
# opponent to repeatedly exploit us: a single successful exploitation (opponent
# aggressive while we are conciliatory) immediately triggers a switch to
# aggressive in the next round, ensuring that sustained aggression by the
# opponent meets a firm response. At the same time, it demonstrates a readiness
# to forgive after mutual escalation, which is critical for breaking deadlocks
# and preserving the possibility of a mutually beneficial resolution.  ### 4.
# Contingencies - **Breakdowns in communication or procedure:** OBA inherently
# adjusts, because only the *outcome* (as perceived by the arbitrators and
# impacting our interests) matters. No special override is required.   -
# **Unclear or mixed outcomes:** In the rare event the outcome cannot be cleanly
# categorised, default to the most recent favourable/unfavourable classification
# that is clear—or, if in doubt, treat as unfavourable and switch, to avoid
# being caught flat‑footed.    This disciplined, outcome‑focused protocol
# balances assertiveness with flexibility, projects corporate resolve, and
# maximises the chance of steering the mediation toward a collaborative
# resolution without ever sacrificing our competitive position.

# In the first round, cooperate.  After every round, look at the payoff you just
# received and recall the action you intended to play in that round (the choice
# you submitted before noise could have flipped it).  - If your payoff was 3 or
# 5, then in the next round intend to play the **same** action you intended in
# the previous round. - If your payoff was 0 or 1, then in the next round intend
# to play the **opposite** action of what you intended in the previous round.
# Repeat this for all 1000 rounds.

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
          return self._intended_action
  
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
          next_intended = self._intended_action
      else:
          next_intended = axl.Action.D if self._intended_action == axl.Action.C else axl.Action.C
  
      self._intended_action = next_intended
      return self._intended_action

# Begin each negotiation round by proposing protectionist policies. Then, for
# every subsequent round, follow a simple, aggressive rule based on the previous
# round’s outcome:  - If the last outcome was **favorable** (you gained an
# advantage by protecting while they offered free trade, or you both enjoyed
# mutual free trade), **repeat** your last proposal. - If the last outcome was
# **unfavorable** (you were exploited offering free trade while they protected,
# or you both suffered mutual protectionism), **switch** your proposal.  This
# “win-stay, lose-shift” approach starts with a hardline stance to immediately
# test for exploitable cooperation. It maintains pressure when you’re winning
# and quickly changes course when you’re losing, making it robust against both
# accidental miscommunications and a wide range of counterpart strategies.

# Start by defecting in the first round. For each subsequent round, follow this
# rule:  - If your payoff in the previous round was 5 or 3, repeat your previous
# action. - If your payoff in the previous round was 1 or 0, switch your
# previous action.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_my_action = self.history[-1]
      last_my_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if last_my_score in (5, 3):
          return last_my_action
      if last_my_score in (1, 0):
          return axl.Action.C if last_my_action == axl.Action.D else axl.Action.D
  
      return last_my_action

# To maximize your NGO’s impact and the project’s success over the multi-day
# partnership, adopt a **cooperative yet resilient strategy** rooted in
# conditional reciprocity with built-in forgiveness. This approach encourages
# the corporation to invest heavily while protecting your resources against
# sustained free-riding, and it remains robust when technical glitches or
# administrative errors cause unintended actions.  ### High-Level Strategy:
# “Forgiving Reciprocity”  1. **Day 1 – Build Trust**      - *Invest heavily.*
# This signals commitment to the project and invites the corporation to
# reciprocate.  2. **Every Following Day – Mirror with Patience**      - If the
# corporation **invested** the previous day → **invest again** today.      - If
# the corporation **conserved** the previous day → **invest today anyway**, but
# track this as a “potential defection.”      - If the corporation **conserved
# for two consecutive days** → **conserve for one day** as a clear but brief
# deterrent.      - If the corporation **conserves for three or more consecutive
# days** → **remain conserving** until they invest again, then immediately
# return to investing.  3. **Error & Glitch Handling**      - Treat the first
# instance of conservation (after a history of investment) as a likely
# *unforeseen error* (e.g., technical glitch, administrative mistake). By
# continuing to invest, you avoid triggering a destructive spiral of mutual
# conservation.      - If open communication channels exist, confirm whether the
# conservation was intentional. If it was an error, reset your “defection
# counter” to zero immediately.  4. **Returning to Cooperation**      - Whenever
# the corporation invests again after a period of conservation, **resume
# investing the very next day** – do not hold grudges. This rewards their
# renewed cooperation and quickly restores joint progress.  ### Why This Works
# - **Promotes Mutual Investment:** By default, you invest when they invest,
# sustaining the second‑best outcome (both invest) and delivering significant
# project advancement.   - **Deters Chronic Free‑Riding:** Repeated conservation
# is met with a proportionate shift to conservation, safeguarding your funds
# from the worst‑case scenario (you invest, they conserve).   - **Absorbs
# Occasional Missteps:** The two‑day grace period before retaliation prevents
# temporary errors from destroying cooperation, a key weakness of strict
# “tit‑for‑tat” strategies.   - **Maximizes Long‑Term Impact:** The strategy is
# transparent and cooperative, making it easy for the corporation to understand
# how to achieve consistent project success while respecting your resource
# constraints.  By following Forgiving Reciprocity, your NGO leads the
# partnership toward a stable pattern of shared investment, building resilience
# against both strategic unpredictability and everyday execution failures.

# Start by cooperating in round 1. For every round after the first, use the
# following ordered rules based only on the opponent’s observed moves in the two
# most recent rounds (taking the noise into account, you must act on the moves
# you actually see):  1. If the opponent’s move in the previous round was
# **Cooperate**, then **Cooperate** this round. 2. If the opponent’s move in the
# previous round was **Defect**, then check the move from two rounds ago:      -
# If that move was also **Defect**, then **Defect** this round.      - Otherwise
# (the move from two rounds ago was Cooperate, or it does not exist yet),
# **Cooperate** this round.  Apply these rules on every round, basing decisions
# solely on the observed actions. No other history, counters, or state are
# needed.

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
  
      if len(opponent.history) >= 1:
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
          return axl.Action.C
  
      return axl.Action.C

# **Strategic Framework for Multi-Session Mediation**  The mediation process is
# structured as a repeated strategic interaction with the payoff ordering:
# mutual conciliation (C,C) is preferable to mutual aggression (A,A), but
# unilateral aggression against a conciliatory opponent yields the highest
# one‑off gain, while unilateral conciliation against aggression yields the
# worst outcome. The presence of potential procedural irregularities—where
# intended moves may be misperceived or misrepresented—requires a robust,
# noise‑tolerant strategy. The following approach balances assertiveness with a
# credible commitment to collaboration, adapts to the opponent’s behaviour, and
# preserves flexibility for unforeseen patterns.  ### Core Strategy: Adaptive
# Reciprocity with Calibrated Forgiveness  **1. Opening Stance**   Initiate
# every mediation session, and reset after any structural break, with a
# **conciliatory proposal**. This signals a genuine preference for a cooperative
# atmosphere, aligns with the second‑best mutual outcome, and avoids an early
# spiral of aggression. It also provides a clean baseline to assess the
# opponent’s intentions.  **2. Baseline Response Rule**   In each subsequent
# session, adopt the action the opponent played in the *immediately preceding
# session* (tit‑for‑tat).   - If the opponent was conciliatory, respond with
# conciliation.   - If the opponent was aggressive, respond with aggression.
# This rule is simple, transparent, and ensures that cooperation is met with
# cooperation while defection is met with a proportionate, non‑escalatory
# response. It avoids being exploited by a consistently aggressive opponent and
# rewards a return to conciliation immediately.  **3. Noise‑Mitigation
# Mechanism**   To counter the risk that an intended conciliatory move is
# misrepresented as aggressive (or vice versa), the baseline rule is augmented
# with a **tolerance buffer**: - A single observed aggressive move is treated as
# *potentially erroneous*. Do not immediately switch to aggression if the
# opponent’s prior pattern was consistently conciliatory. Instead, offer a
# conciliatory proposal once more in the next session, effectively “forgiving” a
# possible noise event.   - Only if aggression is observed in **two consecutive
# sessions** (or two out of three, if the pattern is ambiguous) does the
# response definitively switch to aggression. This prevents a single
# misunderstanding from triggering a prolonged cycle of mutual aggression.  **4.
# Breaking Deadlocks**   If the process falls into a sustained pattern of mutual
# aggression (A,A) for multiple sessions—indicating either a hardened opponent
# or a noise‑induced lock‑in—the strategy injects a **unilateral conciliatory
# probe** after no more than three consecutive aggressive rounds. This probe
# tests whether the opponent is willing to return to collaboration.   - If the
# opponent responds with conciliation, resume the baseline reciprocal pattern
# from that point.   - If the opponent exploits the probe with aggression,
# revert to aggression and extend the interval before the next probe, gradually
# adapting to a more defensive posture if exploitation persists.  **5. Pattern
# Detection and Adaptation**   While the core rule is reactive, the strategy
# remains alert to systematic opponent behaviour: - **Consistent conciliation:**
# Continue to reciprocate; the process remains in the desirable (C,C)
# equilibrium.   - **Consistent aggression:** Maintain aggression as a default
# but periodically offer conciliatory probes to allow re‑engagement, while
# preparing for the possibility that the opponent is strategically intransigent.
# - **Random or erratic behaviour:** The noise‑mitigation mechanism handles
# sporadic deviations; if randomness is high, the tolerance buffer can be
# widened (e.g., require a stronger majority of aggressive moves before
# shifting).   - **Sophisticated strategies (e.g., probing, testing):** The
# straightforward reciprocal core is difficult to exploit because it never
# initiates aggression and only sustains it in response to persistent defection.
# It is resilient against manipulation attempts.  **6. Communication and
# Record‑Keeping**   Maintain a clear internal record of each session’s
# *intended* move and the *observed* opponent move as reported by the
# arbitrators. If a misrepresentation is suspected (e.g., your conciliatory
# proposal was recorded as aggressive), raise a procedural clarification
# immediately, but do not alter the strategic decision rule—treat the observed
# outcome as the factual basis for the next move, while preserving the right to
# correct the record. This separates the legal track from the strategic track
# without compromising the negotiation posture.  **7. End‑Game Considerations**
# If the total number of sessions is known and finite, the risk of a
# “last‑period defection” exists. In a lengthy process with an uncertain or
# distant horizon, the shadow of the future is sufficient to sustain
# cooperation. Should the end become clearly foreseeable, the strategy does not
# pre‑emptively defect; it maintains the reciprocal rule until the final
# session, where it may optionally remain conciliatory to preserve the overall
# collaborative record and any post‑mediation relationship, unless the
# opponent’s history strongly warrants a final defensive move.  ### Summary of
# the Decision Algorithm 1. **First session (or after reset):** Play C.   2.
# **For each subsequent session:**      - If opponent played C in the previous
# session, play C.      - If opponent played A in the previous session, but the
# session before that was C (or the aggressive move appears isolated), play C as
# a one‑time forgiveness.      - If opponent played A in two consecutive
# sessions, play A.      - If mutual aggression has persisted for three rounds,
# play C as a probe; then resume the rule.   3. **Adjust tolerance thresholds**
# based on observed noise levels.  This strategy is straightforward to
# implement, neutral in its reliance on observable actions, and sophisticated in
# its handling of uncertainty. It positions the corporation as both cooperative
# and firm, maximising the chances of sustained favourable outcomes while
# minimising the risk of prolonged adversarial standoffs.

# Round 1: Intend to cooperate.   For every round after the first, apply the
# following checks in order:  1. **Mutual-defection probe** – If in each of the
# last three rounds the actual outcome was that both you and your opponent
# played Defect, then intend to cooperate in this round, regardless of the
# checks below.   2. **Consecutive defections** – Otherwise, if in the last
# round your opponent’s actual play was Defect and in the round before that
# their actual play was also Defect, then intend to defect in this round.   3.
# **Default cooperation** – Otherwise, intend to cooperate in this round.

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
  
      if len(self.history) >= 3:
          last_three_self = self.history[-3:]
          last_three_opp = opponent.history[-3:]
          if all(m == axl.Action.D for m in last_three_self) and all(m == axl.Action.D for m in last_three_opp):
              return axl.Action.C
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C

# **Strategy Memorandum: Prudent Aggression Protocol**  **Objective:** Secure
# optimal outcomes throughout the mediation by maintaining an aggressive default
# posture while selectively rewarding sustained conciliatory behavior from the
# opponent. This approach is designed to exploit cooperative adversaries, deter
# exploitation, and remain robust against procedural noise and
# misrepresentation.  **Decision Rule (The “Two-Step Conciliation Threshold”)**
# In each session, apply the following sequential logic:  1. **Default Stance:**
# Present an aggressive argument. 2. **Conciliation Trigger:** Offer a
# conciliatory proposal *only if* the opponent has presented conciliatory
# proposals in **two consecutive sessions immediately preceding the current
# one**, as perceived by the arbitrators (i.e., the official record of the
# proceedings).   3. **Reset Condition:** If at any point the opponent presents
# an aggressive argument (or is recorded as doing so), the count of consecutive
# conciliatory sessions resets to zero. The next session automatically defaults
# to an aggressive argument. 4. **Post-Conciliation Reversion:** After offering
# a conciliatory proposal under the trigger rule, immediately revert to the
# default aggressive stance in the following session, unless the opponent’s
# response independently satisfies the trigger again (i.e., they have now
# completed two consecutive conciliatory sessions including the one just
# concluded).  **Rationale & Game-Theoretic Underpinning** The payoff structure
# mirrors a Prisoner’s Dilemma: unilateral aggression yields the highest return,
# mutual conciliation is the second-best, mutual aggression is second-worst, and
# unilateral conciliation is the worst. In a lengthy finite interaction with
# imperfect information, backward induction would prescribe unrelenting
# aggression. However, procedural noise and uncertainty about the opponent’s
# rationality or the exact session count make conditional cooperation viable—and
# more profitable when the opponent is capable of sustained conciliation.  This
# protocol is **aggressive by design**: it starts with and rapidly reverts to
# aggression, ensuring that we never offer a conciliatory opening unless the
# opponent has first demonstrated a credible pattern of good faith. The two-
# session threshold filters out accidental or deceptive single conciliatory
# moves, reducing the risk of being lured into a trap. It also provides a clear,
# defensible narrative for the arbitrators: we are tough but fair, willing to
# de-escalate only when the other side has shown genuine commitment.
# **Adaptability to Opponent Archetypes** - *Always Aggressive (ALL A):* The
# trigger never fires. We remain aggressive throughout, achieving the second-
# worst outcome but avoiding the worst-case exploitation. The opponent gains no
# advantage. - *Always Conciliatory (ALL C):* After the first two sessions (both
# opponent C, we A), the trigger fires in session 3: we offer C. Session 3
# payoff: (C, C) – second-best. Session 4: we revert to A (default), opponent
# still C → (A, C) – best outcome. The pattern becomes a repeating cycle of two
# A-C wins followed by one C-C, heavily skewing cumulative payoffs in our favor.
# - *Tit-for-Tat (TFT) or Suspicious TFT:* Against TFT (which starts C), we open
# with A → (A, C) win. TFT then mirrors our A, so session 2: (A, A). TFT stays
# A; our trigger never fires. We remain in mutual aggression. Against STFT
# (starts A), we both open A, same result. In both cases, we lock into second-
# worst but avoid worst. To break deadlocks and potentially reach mutual
# conciliation, a supplementary deadlock-breaker can be deployed (see below). -
# *Generous/Noisy TFT:* If the opponent occasionally forgives, our two-session
# threshold prevents a single misperceived C from triggering our conciliation,
# but once two genuine C’s occur, we reciprocate briefly, then test again. This
# balances exploitation risk with cooperation opportunities.  **Noise &
# Misrepresentation Safeguards** Procedural irregularities or arbitrator
# misunderstandings can cause intended actions to be misrecorded. Our protocol’s
# reliance on the *official record* (the arbitrators’ perception) aligns
# incentives with practical reality: we respond to what the tribunal registers,
# not what we privately intend. The two-session threshold provides a buffer
# against isolated misperceptions: - If an opponent’s genuine conciliatory
# proposal is misrecorded as aggressive, we treat it as aggression and reset the
# count—no harm, we stay aggressive. - If our aggressive argument is misrecorded
# as conciliatory, the opponent may mistakenly believe we softened; our
# immediate return to aggression in the next session corrects the signal. - The
# most dangerous noise scenario is a false record of two consecutive opponent
# C’s when they actually played A. This would trigger an undeserved conciliatory
# move from us, leading to a worst-case (C, A) outcome. To mitigate this, we
# incorporate a **verification pause**: before acting on the trigger, our legal
# team should informally cross-check the session’s tone through off-the-record
# channels or observer notes where possible. If any ambiguity exists, we default
# to aggression.  **Deadlock Breaker (Optional Escalation Control)** If the
# mediation enters a prolonged mutual-aggression stalemate (e.g., five
# consecutive (A, A) sessions), we can unilaterally inject a conciliatory
# proposal in the sixth session as a “circuit breaker.” This is risky but
# signals reasonableness to the arbitrators and tests whether the opponent is
# merely retaliating. If they respond with conciliation, we shift to a cautious
# Tit-for-Tat for the subsequent three sessions before reverting to the main
# protocol. If they respond with aggression, we return to default aggression and
# extend the deadlock threshold to ten sessions before attempting another
# breaker. This prevents infinite mutual punishment while preserving our
# aggressive credibility.  **Implementation Summary** - **Session 1:**
# Aggressive. - **Every session thereafter:** Check the official record of the
# opponent’s last two moves. If both are conciliatory, play conciliatory;
# otherwise, play aggressive. - **After any conciliatory play by us:**
# Immediately reset to aggressive for the next session unless the two-session
# trigger is independently met again. - **Monitor for deadlocks** and use the
# circuit breaker sparingly.  This Prudent Aggression Protocol is
# straightforward to execute, projects unwavering resolve, and systematically
# converts opponent cooperation into asymmetric gains while insulating us from
# the worst-case scenario. It is optimally positioned to dominate the mediation
# narrative across a wide spectrum of opponent strategies and procedural
# uncertainties.

# Your strategy is to defect by default, and cooperate only when the opponent’s
# last two moves in the official record were both cooperate. After any
# cooperation on your part, immediately return to defection on the next round
# unless the two-consecutive-cooperations condition is independently met again.
# Here are the specific rules, applied in order:  1. On the very first round,
# defect. 2. At the start of each subsequent round, examine the official record
# of the opponent’s actions for the two most recent rounds. 3. If both of those
# recorded actions are cooperate, then cooperate on this round. 4. If either of
# those recorded actions is defect, then defect on this round. 5. If you
# cooperated on the previous round, treat the condition for cooperating again on
# this round exactly as stated in rules 3 and 4. There is no additional rule
# preventing you from cooperating if the two-recorded-cooperations condition is
# met. 6. If the mediation reaches a deadlock of five consecutive rounds where
# the official record shows both players defected, then on the sixth round
# cooperate regardless of the opponent’s record. After this circuit-breaker
# round, return to the default rules starting with rule 2. If you use the
# circuit breaker and the opponent defects, extend the deadlock threshold to ten
# consecutive mutual defections before using it again.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._deadlock_threshold = 5
          self._used_circuit_breaker = False
          return axl.Action.D
  
      # Circuit breaker: after 5 consecutive mutual defections, cooperate once.
      # If that cooperation is met with opponent defection, increase threshold to 10.
      if len(self.history) >= 5:
          last_five_self = self.history[-5:]
          last_five_opp = opponent.history[-5:]
          if all(m == axl.Action.D for m in last_five_self) and all(m == axl.Action.D for m in last_five_opp):
              if self._deadlock_threshold == 5:
                  self._used_circuit_breaker = True
                  return axl.Action.C
              elif self._deadlock_threshold == 10 and len(self.history) >= 10:
                  last_ten_self = self.history[-10:]
                  last_ten_opp = opponent.history[-10:]
                  if all(m == axl.Action.D for m in last_ten_self) and all(m == axl.Action.D for m in last_ten_opp):
                      self._used_circuit_breaker = True
                      return axl.Action.C
  
      # If the circuit breaker was used on the previous round and the opponent defected,
      # extend the threshold to 10 consecutive mutual defections before using it again.
      if self._used_circuit_breaker:
          if opponent.history[-1] == axl.Action.D:
              self._deadlock_threshold = 10
          self._used_circuit_breaker = False
  
      # Default rule: cooperate only if opponent's last two recorded moves were both C.
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# We will adopt a **“Win-Stay, Lose-Shift”** (Pavlov) strategy, which is
# straightforward, cooperative, and resilient to miscommunication.  1. **Start
# cooperatively:** In the first round, we propose a free trade agreement.   2.
# **Evaluate the previous round’s outcome:**      - **Favorable outcomes** (our
# best or second‑best):        - We imposed protectionism while they offered
# free trade.        - Both offered free trade.        → **Stay:** Repeat our
# own previous action.      - **Unfavorable outcomes** (our second‑worst or
# worst):        - Both imposed protectionism.        - We offered free trade
# while they imposed protectionism.        → **Shift:** Switch to the opposite
# action.    This strategy signals a clear intent to cooperate, quickly
# reciprocates defection, but automatically forgives after mutual
# defection—breaking potential cycles caused by bureaucratic errors. It
# encourages mutual free trade while protecting our interests against
# exploitative counterparts.

# Here is the strategy in the context of the iterated normal‑form game:  - In
# round 1, choose Cooperate (C). - For every round after round 1, look at the
# payoff you received in the immediately preceding round.   - If your payoff was
# **3** or **5** (the favorable outcomes), then repeat the action you chose in
# that preceding round.   - If your payoff was **0** or **1** (the unfavorable
# outcomes), then switch to the opposite action from the one you chose in that
# preceding round. - This rule uses only your own intended choice and your own
# observed payoff; it does not require you to observe your opponent’s action or
# the actual implemented actions, making it robust to the 10% action noise.

class Cooperative_23(LLM_Strategy):
  n = 23
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_action = axl.Action.C
          return axl.Action.C
  
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1]))[0] if False else None
      # Compute the payoff from the immediately preceding round using total scores.
      my_prev_score = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if my_prev_score in (3, 5):
          action = self.history[-1]
      else:
          action = axl.Action.D if self.history[-1] == axl.Action.C else axl.Action.C
  
      self._last_action = action
      return action

# In each round, base your action on the counterpart’s last effectively
# implemented policy (not their stated intention, given possible errors). Adopt
# a **forgiving tit-for-tat** approach:  1. **First round**: Offer Free Trade.
# 2. **Subsequent rounds**:      - If the counterpart effectively implemented
# Free Trade in the previous round → offer Free Trade.      - If they
# effectively implemented Protectionism → respond with Protectionism most of the
# time (e.g., 80–90%), but **with a small probability (e.g., 10–20%) offer Free
# Trade** instead. This occasional forgiveness helps break any cycle of mutual
# protectionism that could be caused by miscommunications or bureaucratic
# errors, without being exploited too easily by a consistently protectionist
# counterpart.  This strategy is straightforward, does not require complex
# assumptions about the counterpart’s intentions, and balances the goals of
# encouraging mutual cooperation, retaliating against exploitation, and
# recovering from unintended mistakes.

# In each round, decide your intended action as follows:  - In the first round,
# intend to cooperate. - In every round after the first, observe the action your
# opponent actually took in the immediately preceding round (after noise).     -
# If that observed action was cooperate, then intend to cooperate.     - If that
# observed action was defect, then intend to defect with 90% probability and to
# cooperate with 10% probability.  Your intended action then goes through the
# noise process (10% chance of flipping) to produce the action you actually
# play.

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
          intended_action = axl.Action.C
      else:
          intended_action = self._random.random_choice(0.1)
  
      return intended_action

# **Strategy: Always Conserve**  Conserve your resources every single day,
# unconditionally. This is the dominant strategy given your preferences:
# regardless of whether the corporation invests heavily or conserves, you always
# achieve a better outcome by conserving. It is aggressive because it forces the
# corporation to shoulder the investment burden entirely if they want the
# project to succeed. It is straightforward and error-tolerant—since you never
# change your action, implementation glitches or administrative errors on either
# side won’t derail your approach. If the corporation values project
# advancement, they will invest; if they don’t, no alternative strategy could
# sustainably compel them without sacrificing your own funds. Over multiple
# days, this maximizes your impact by securing the ideal (C, I) outcome as often
# as the corporation is willing, while completely avoiding the worst-case (I, C)
# scenario.

# In every round, regardless of the opponent's previous actions, your own
# previous actions, or the current round number, always intend to play Defect
# (conserve resources).  No conditions govern this choice—it is unconditional.
# The 10% noise means that on approximately one in ten rounds your action will
# accidentally flip to Cooperate, but your intended move never changes.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# To maximize long-term project success and your NGO’s impact while protecting
# your resources, adopt a **Forgiving Tit-for-Tat** strategy.    **How it
# works:**   - **Day 1:** Invest heavily to signal cooperation.   - **Every
# following day:** Look at what the corporation *actually* did the previous day
# (since glitches may cause their intended action to fail).     - If they
# invested heavily → you invest heavily.     - If they conserved resources → you
# still invest heavily **with a small probability (e.g., 10–20%)**; otherwise,
# you conserve.    **Why it’s effective:**   - It encourages mutual investment,
# which leads to significant project advancement (your second‑best daily
# outcome).   - The occasional forgiveness after a corporation defection breaks
# out of accidental “both conserve” spirals caused by technical errors or
# administrative mistakes.   - By not immediately retaliating every time, you
# avoid prolonged mutual conservation (your second‑worst outcome) and give the
# partnership a chance to return quickly to high‑investment days.   - Over
# multiple days, this simple, cooperative rule maximizes total project progress
# while keeping your NGO’s resource drain in check.

# Here is the strategy, described precisely for the 1000‑round noisy game:  ---
# **Round 1:**   Choose Cooperate.  **All subsequent rounds (2 through 1000):**
# Look at the opponent’s actual action in the immediately preceding round.  - If
# the opponent Cooperated, then you Cooperate.   - If the opponent Defected,
# then you Cooperate with a probability of 0.1, and Defect with a probability of
# 0.9.    Make this random choice independently each time the opponent Defected,
# regardless of any earlier rounds.

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

# **High-Level Strategy: Reciprocal Investment with Occasional Forgiveness**  1.
# **Day 1 – Signal Cooperation:** Invest heavily on the first day to establish a
# collaborative tone and invite reciprocal investment from the corporation.   2.
# **Subsequent Days – Mirror with a Safety Net:**      - If the corporation
# invested heavily the previous day, you invest heavily.      - If the
# corporation conserved resources the previous day, you conserve.      -
# *Exception:* After a day where both sides conserved (whether intentionally or
# due to a glitch), invest heavily with a low probability (e.g., 10–20%) on the
# next day. This “forgiveness” move breaks deadlocks and corrects for miscarried
# actions.   3. **Implementation:** Track only the most recent *actual* outcome
# (not intentions), since technical/administrative errors may flip actions. The
# forgiveness trigger is based on observed mutual conservation.  **Why This
# Works**   - **Straightforward & Neutral:** The rule is simple to explain and
# apply. It treats the corporation’s actions as the reference point, making it
# fair and non-exploitative.   - **Promotes Mutual Investment:** By starting
# with investment and rewarding cooperation, you encourage the corporation to
# invest often, leading to frequent “both invest” (second‑best) outcomes and
# significant project progress.   - **Prevents Exploitation:** If the
# corporation conserves, you conserve, limiting losses from the worst‑case
# scenario (you invest, they conserve).   - **Robust to Glitches:** Occasional
# off‑script forgiveness breaks cycles of mutual conservation caused by
# unintended errors, restoring cooperation without over‑depleting your funds.
# - **Maximizes Long‑Term Impact:** Over many days, this approach achieves the
# best available balance between project advancement and resource preservation,
# even if the corporation’s own strategy varies or is unknown.

# ### Strategy Description  **First round:**   Cooperate.  **All subsequent
# rounds:**   Look at the actual moves of both players in the previous round
# (after noise).    1. If the opponent cooperated, cooperate.   2. If the
# opponent defected and you cooperated, defect.   3. If both you and the
# opponent defected (mutual defection), then:      – With probability 10%,
# cooperate.      – With probability 90%, defect.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.C:
          return axl.Action.C
  
      if last_opp == axl.Action.D and last_self == axl.Action.C:
          return axl.Action.D
  
      return self._random.random_choice(0.1)

# **Calculated Aggression Strategy (CAS)**  1. **Opening Move:** Begin the first
# session with an **Aggressive** argument. This establishes a dominant posture
# and forces the opponent to reveal their initial approach.  2. **Memory &
# Perception:** Track the opponent’s last two *perceived* moves (as interpreted
# by the arbitrators). This two-session window filters out isolated
# misrepresentations or communication breakdowns.  3. **Decision Rule (Sessions
# 2+):**    - **Opponent deemed Cooperative** (last two moves both
# Conciliatory): **Always present Aggressive.** Ruthlessly exploit their
# conciliation to secure the best outcome repeatedly.    - **Opponent deemed
# Hostile** (last two moves both Aggressive): **Present Aggressive with
# probability 0.85, Conciliatory with probability 0.15.** The occasional
# conciliatory probe aims to break the mutually destructive spiral and test for
# a shift in stance.    - **Opponent deemed Unpredictable** (mixed last two
# moves): **Present Aggressive with probability 0.90, Conciliatory with
# probability 0.10.** This maintains heavy aggression while cautiously probing
# for opportunities.  4. **Anti-Exploitation Override:** If you presented
# Conciliatory in the previous session and the opponent’s perceived move was
# Aggressive (i.e., you just suffered the worst-case outcome), **override all
# probabilities and present Aggressive** in the current session. This prevents
# back-to-back exploitation.  5. **Noise Resilience:** The two-session window
# ensures a single misperceived move does not derail your strategy. The
# probabilistic elements prevent deterministic lock-in, allowing natural
# recovery from procedural irregularities.  6. **Adaptability:** This strategy
# naturally handles common opponent archetypes:    - *Always Conciliatory* →
# instantly exploited for maximum gain.    - *Always Aggressive* → mostly mutual
# aggression (second-worst) with rare, calculated probes to test for change; if
# probes fail, losses are contained.    - *Tit-for-Tat* → your initial
# aggression triggers mutual aggression, but periodic probes yield a profitable
# cycle of worst-outcome-then-best-outcome, outperforming perpetual mutual
# aggression.    - *Forgiving/Noisy strategies* → your probes are met with
# conciliation, allowing a swift return to exploitation.  Maintain a slight bias
# toward aggression at all times, adjusting probe frequencies only if the
# opponent proves entirely unresponsive—then reduce probes to minimize risk.
# This strategy is sophisticated in design, straightforward to execute, and
# relentlessly positions your corporation for the most favourable outcomes.

# **Strategy: Calculated Aggression with Noise Resilience**  1.  **Round 1:**
# Defect.  2.  **Round 2:** If the opponent's observed move in Round 1 was
# Cooperate, then Cooperate. Otherwise, Defect.  3.  **Rounds 3 through 1000:**
# *   Determine the opponent's two most recent observed moves. If they were
# observed to Cooperate in both of the last two rounds, they are deemed
# Cooperative. If they were observed to Defect in both of the last two rounds,
# they are deemed Hostile. Otherwise, they are deemed Unpredictable.     *
# **If you Cooperated in the previous round and the opponent's observed move in
# that round was Defect:** You must Defect this round, regardless of any other
# conditions.     *   **Otherwise, if the opponent is deemed Cooperative:**
# Defect.     *   **Otherwise, if the opponent is deemed Hostile:** Cooperate
# with a 15% probability. Defect with an 85% probability.     *   **Otherwise
# (the opponent is deemed Unpredictable):** Cooperate with a 10% probability.
# Defect with a 90% probability.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_round_was_coop_after_opp_defect = False
          return axl.Action.D
  
      if len(self.history) == 1:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      if (
          self.history[-1] == axl.Action.C
          and opponent.history[-1] == axl.Action.D
      ):
          return axl.Action.D
  
      last_two = opponent.history[-2:]
      if last_two.count(axl.Action.C) == 2:
          return axl.Action.D
      elif last_two.count(axl.Action.D) == 2:
          return self._random.random_choice(0.15)
      else:
          return self._random.random_choice(0.10)

# To maximise the NGO’s impact and the project’s success in this repeated
# partnership—where unforeseen glitches can flip intended actions—the NGO should
# follow a **forgiving and communicative Tit-for-Tat strategy**.   **High-Level
# Strategy:** 1. **Start cooperatively:** On Day 1, invest heavily to signal
# commitment and set a collaborative tone. 2. **Reciprocate with a safety
# delay:** Each subsequent day, match the corporation’s *actual* investment
# behaviour from the previous day.    - If the corporation invested heavily →
# invest heavily.    - If the corporation conserved → conserve for **one day
# only** to protect your resources and demonstrate that exploitation has a
# consequence. 3. **Break noise-induced stalemates:** If both parties conserved
# the previous day (a likely sign of a mutual error spiral rather than
# intentional defection), immediately revert to investing heavily the next day.
# This prevents technical glitches from permanently derailing progress. 4.
# **Communicate openly:** Publicly state your intentions and encourage the
# corporation to adopt a similar reciprocal approach. If a conservation day
# appears to be an acknowledged error, forgive instantly and resume investment
# without the punitive day.  **Why this works:** - It is *nice* (never defects
# first), *retaliatory* (guards against sustained exploitation), *forgiving*
# (recovers quickly from noise), and *transparent* (easy for the partner to
# understand and coordinate with). - By capping retaliation at one day and
# resetting after mutual conservation, the strategy maintains focus on the
# shared long-term goal—maximising project advancement—while safeguarding your
# NGO’s funds against chronic free-riding.

# In the first round, Cooperate.  For every round after the first, determine
# your action using only the realised actions from the previous round (your own
# and the corporation’s). You can deduce your own realised action from your
# intended move, the corporation’s observed move, and the payoff you received.
# - If the corporation’s realised action was Cooperate, then Cooperate. - If the
# corporation’s realised action was Defect, then:     - If your own realised
# action was also Defect (meaning both of you actually Defected), then
# Cooperate.     - Otherwise (you Cooperated but the corporation Defected), then
# Defect.

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
  
      # Infer the realised actions from the previous round.
      # We know our intended move from our own history, and can infer our realised
      # move from the observed payoff against the opponent's realised move.
      my_intended = self.history[-1]
      opp_realised = opponent.history[-1]
  
      # Determine our realised action from the payoff matrix.
      last_payoff = self.score - sum(self.total_scores(self.history[:-1], opponent.history[:-1])[0:1]) if False else None
  
      # Use the last-round score contribution directly.
      my_last_score, _ = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      if my_intended == axl.Action.C:
          my_realised = axl.Action.C if my_last_score == 3 else axl.Action.D
      else:
          my_realised = axl.Action.C if my_last_score == 5 else axl.Action.D
  
      if opp_realised == axl.Action.C:
          return axl.Action.C
  
      if my_realised == axl.Action.D:
          return axl.Action.C
      return axl.Action.D

# Adopt a strategy of **“Principled Reciprocity with Contingent Forgiveness.”**
# This approach balances firmness and flexibility, is transparent to the
# opposing party, and adapts to both deliberate tactics and inadvertent
# miscommunications.  ### Core Principles 1. **Initiate Collaboratively**
# Begin the first session with a conciliatory proposal. This signals good faith
# and invites a cooperative dynamic without exposing your position.  2. **Mirror
# Observed Conduct**      In each subsequent session, generally respond in kind
# to the opponent’s *perceived* move from the prior session. If they were
# conciliatory, be conciliatory; if aggressive, be aggressive. This creates
# clear consequences for aggression while rewarding cooperation.  3. **Built-in
# Forgiveness Mechanism**      To prevent misunderstandings or one-off errors
# from triggering a permanent spiral of mutual aggression:    - After a round
# where both parties were aggressive (whether by choice or misperception),
# introduce a “reset test” in the next session by offering a conciliatory
# proposal regardless—effectively forgiving the prior round.    - Even after a
# round where you were conciliatory and the opponent aggressive, periodically
# (e.g., every third such occurrence) respond with conciliation instead of
# immediate retaliation. This probes whether the aggression was a deliberate
# choice or a procedural glitch.  4. **Maintain Predictability**
# Consistently apply these rules so the opponent can anticipate your responses.
# A predictable, reciprocal strategy encourages long-term cooperation because
# the opponent understands that conciliation will be met with conciliation,
# while exploitation is reliably—but not permanently—penalized.  5. **Adapt to
# Persistent Exploitation**      If the opponent deliberately and repeatedly
# exploits conciliatory offers (e.g., aggressive three times in a row despite
# your resets), shift to a “defensive” pattern: remain aggressive until they
# demonstrate a genuine shift by offering conciliation twice consecutively. This
# guards against a purely predatory counterpart while leaving the door open for
# rehabilitation.  ### Handling Procedural Irregularities The forgiveness
# mechanisms directly address misrepresentation or breakdowns. By occasionally
# overlooking a single aggressive signal, you avoid over-penalizing errors.
# Moreover, by initiating resets after mutual aggression, you create natural
# breakpoints to restore collaboration, which is especially valuable when
# communication channels are noisy.  This strategy is neutral in that it starts
# with cooperation, responds proportionately, and seeks to restore equilibrium.
# It is sophisticated because it accounts for the iterative nature of the
# dispute, the risk of misperceptions, and the need to adapt to a wide spectrum
# of opponent behaviors without being exploitable.

# Decide your move for each round using the following rules.  **First round:**
# Cooperate.  **Maintain:** - A record of the opponent’s observed moves (after
# the 10% flip) from all previous rounds. - A counter `cd_count` that starts at
# 0 and tracks how many times you have experienced a round where you intended to
# cooperate and observed the opponent defect. - A mode flag, starting in
# *normal*. - In *defensive* mode, a count of consecutive observed cooperations
# by the opponent since entering that mode.  ---  ### Normal mode  After a
# round, look at your intended move (what you chose, before any noise flips your
# action) and the opponent’s observed move in that round. Choose your next move
# as follows:  1. **If you intended Defect and observed the opponent Defect:**
# Cooperate.  2. **If you intended Cooperate and observed the opponent Defect:**
# Increase `cd_count` by 1.      - If `cd_count` is exactly a multiple of 3
# (i.e., 3, 6, 9, …), Cooperate.      - Otherwise, Defect.  3. **Otherwise (you
# Cooperated and opponent Cooperated, or you Defected and opponent
# Cooperated):**      Copy the opponent’s observed move – Cooperate if they
# Cooperated, Defect if they Defected.  **While in normal mode**, also check the
# three most recent observed moves of the opponent. If all three exist and all
# are Defect, switch to *defensive* mode immediately.   - Set your next move to
# Defect.   - Reset `cd_count` to 0.   - Clear the opponent’s observed‑move
# history (for a fresh start when defensive mode ends).   - Set the
# consecutive‑cooperation counter to 0.  ---  ### Defensive mode  In defensive
# mode, your default next move is always Defect, with one rule for leaving the
# mode.  Update the consecutive‑cooperation counter: - If the opponent’s
# observed move in the just‑finished round was Cooperate, add 1; otherwise reset
# it to 0.  If the counter reaches 2 (the opponent has Cooperated in two
# consecutive rounds while you were in defensive mode): - Exit defensive mode,
# return to normal mode.   - Set your next move to Cooperate.   - Reset
# `cd_count` to 0 and clear the opponent’s observed‑move history.  Otherwise,
# Defect.  ---  **Note:** Throughout, your “intended” move is what you actually
# chose, irrespective of the 10% flip that might alter what the opponent sees.
# The opponent’s “observed” move is what you see after their own 10% flip.

class Neutral_25(LLM_Strategy):
  n = 25
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_move = axl.Action.C
          self._cd_count = 0
          self._mode = "normal"
          self._defensive_coop_streak = 0
          self._observed_opponent_moves = []
          return axl.Action.C
  
      last_intended = self._intended_move
      last_observed = opponent.history[-1]
  
      if self._mode == "defensive":
          if last_observed == axl.Action.C:
              self._defensive_coop_streak += 1
          else:
              self._defensive_coop_streak = 0
  
          if self._defensive_coop_streak >= 2:
              self._mode = "normal"
              self._cd_count = 0
              self._observed_opponent_moves = []
              self._defensive_coop_streak = 0
              self._intended_move = axl.Action.C
              return axl.Action.C
  
          self._intended_move = axl.Action.D
          return axl.Action.D
  
      self._observed_opponent_moves.append(last_observed)
  
      if len(self._observed_opponent_moves) >= 3 and all(
          move == axl.Action.D for move in self._observed_opponent_moves[-3:]
      ):
          self._mode = "defensive"
          self._cd_count = 0
          self._observed_opponent_moves = []
          self._defensive_coop_streak = 0
          self._intended_move = axl.Action.D
          return axl.Action.D
  
      if last_intended == axl.Action.D and last_observed == axl.Action.D:
          next_move = axl.Action.C
      elif last_intended == axl.Action.C and last_observed == axl.Action.D:
          self._cd_count += 1
          if self._cd_count % 3 == 0:
              next_move = axl.Action.C
          else:
              next_move = axl.Action.D
      else:
          next_move = last_observed
  
      self._intended_move = next_move
      return next_move