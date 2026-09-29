import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy

# # Racing Car Development Strategy: Aggressive Competitive Approach  ## Core
# Strategic Framework  ### **Primary Strategy: Conditional Reciprocity (Tit-for-
# Tat with Exploitation Bias)**  Start cooperative, then mirror your colleague's
# behavior while looking for exploitation opportunities.  ---  ## Week-by-Week
# Execution  ### **Week 1: Open Share (Establish Baseline)** - Share genuine but
# **non-critical improvements** - useful data, nothing foundational - Observe
# exactly what your colleague shares in return - Calibrate their apparent
# strategy immediately  ### **Weeks 2 Onward: Adaptive Response**  | Their
# Previous Move | Your Response | |---|---| | They shared openly | **Withhold**
# - extract maximum advantage | | They withheld | **Withhold** - don't reward
# defection | | Mixed/partial sharing | **Withhold** - punish ambiguity |  ---
# ## Key Tactical Principles  1. **Never share first twice consecutively** -
# prevents systematic exploitation of you 2. **Classify your improvements** -
# share incremental findings, protect breakthrough developments always 3.
# **Create information asymmetry** - appear more transparent than you are 4.
# **Track cumulative advantage** - if ahead, withhold more aggressively  ---  ##
# Honest Assessment  I should flag directly: **this is essentially a defection-
# dominant strategy** dressed in conditional language.  The genuine tension here
# is: - Mutual sharing likely produces better cars **for both of you** - This
# strategy optimizes for **relative gain over absolute gain** - It risks
# collapsing into mutual withholding, the **second-worst outcome for everyone**
# **A genuinely high-output strategy would be sustained mutual cooperation** -
# which requires trust-building, not exploitation-seeking.  The aggressive
# framing you requested prioritizes beating your colleague over maximizing your
# own research output, which are **not the same objective**.  Which goal
# actually matters most to you?

# # Iterated Prisoner's Dilemma Strategy  ## Opening Move Play **C** in Round 1.
# ## Subsequent Rounds Apply the following conditions in order:  1. If your
# opponent played **C** in the previous round, play **D**.  2. If your opponent
# played **D** in the previous round, play **D**.  ## Net Result Play **D** from
# Round 2 onward, regardless of opponent behaviour.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return axl.Action.D

# # Cooperative Strategy for Multi-Week Research Collaboration  ## Core
# Strategic Principle: **Conditional Reciprocity (Tit-for-Tat with Generosity)**
# ---  ## Opening Position **Share openly in Week 1.**  Establish good faith
# immediately. This signals cooperative intent and gives the collaboration a
# productive foundation without being naively exploitable long-term.  ---  ##
# Ongoing Decision Rule  | What your colleague did last week | Your action this
# week | |---|---| | Shared openly | Share openly | | Kept confidential | Keep
# confidential | | Returns to sharing | Return to sharing promptly |  This is
# simple, transparent and proportionate - rewarding cooperation and deterring
# exploitation without being permanently punitive.  ---  ## Key Practical
# Adjustments  **Forgive occasionally** - If your colleague withholds once,
# consider it may be situational. Allow one reciprocal return to sharing without
# demanding perfect history. Sustained non-sharing warrants sustained caution.
# **Communicate explicitly** - Tell your colleague directly what your strategy
# is. Transparency about the rule itself reinforces cooperative incentives and
# removes ambiguity.  **Recognise mutual loss** - Both withholding
# simultaneously is genuinely the second-worst outcome. Acknowledge this openly
# to motivate escape from deadlock.  ---  ## Why This Works  - **Not naive** -
# You cannot be consistently exploited - **Not aggressive** - You never defect
# first or hold permanent grudges - **Self-correcting** - Cooperation can be
# restored after breakdown - **Honest** - The strategy is fully declarable to
# your colleague, which itself builds trust  ---  ## Underlying Principle  The
# multi-week format means **your reputation compounds**. Consistent, conditional
# cooperation yields more cumulative research value than short-term information
# hoarding, because sustained mutual sharing outperforms the sporadic gains of
# exploitation across many rounds.

# ## Strategy  In round 1, play C.  In all subsequent rounds, play whatever your
# opponent played in the previous round.  However, if your opponent plays D
# exactly once and then returns to C, treat this as situational and continue
# playing C without retaliating. If your opponent plays D two or more times,
# play D until your opponent plays C, then return to C.

class Cooperative_1(LLM_Strategy):
  n = 1
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.single_d_forgiven = False
          return axl.Action.C
      
      # Count opponent's defections
      opp_history = list(opponent.history)
      
      # Check if opponent has defected exactly once total and then returned to C
      # "treat this as situational and continue playing C without retaliating"
      
      # Determine current state
      opp_defections = opponent.history.defections
      
      if opp_defections == 0:
          # Opponent has never defected, cooperate
          return axl.Action.C
      elif opp_defections == 1:
          # Opponent defected exactly once
          # If opponent's last move is C, they've returned to C after one defection
          # Forgive and play C
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          else:
              # Opponent just defected (this is their first defection)
              # We don't know yet if they'll return to C
              # According to strategy: play whatever opponent played in previous round
              # But if it's exactly one D, we forgive
              # Since we don't know if they'll return, we need to track
              # For now, play D (tit for tat) but we'll forgive if they return
              # Actually, re-reading: "if opponent plays D exactly once and then returns to C"
              # This means we need to see if they return. But we play in real-time.
              # The strategy says: play whatever opponent played in previous round (TFT base)
              # But with the modification for single D forgiveness.
              # Since opponent just played D (first time), TFT says play D.
              # But the forgiveness rule says if it's exactly once and they return, forgive.
              # We can't know the future, so we must play D now (TFT) and then
              # if they return to C and total defections == 1, we forgive (play C).
              return axl.Action.D
      else:
          # Opponent has defected 2 or more times
          # "play D until your opponent plays C, then return to C"
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          else:
              return axl.Action.D

# # Strategic Framework for Multi-Day Sustainability Partnership  ## Core
# Strategic Approach: **Conditional Cooperation**  ---  ## Guiding Principle
# Encourage maximum project progress while protecting organizational resources
# through transparent, responsive engagement.  ---  ## Daily Decision Framework
# ### Phase 1: Early Days — Establish Signals - **Invest heavily initially** to
# demonstrate genuine commitment - Observe the corporation's response pattern
# carefully - This builds credibility and tests their good faith  ### Phase 2:
# Middle Days — Mirror Their Behavior - **Match the corporation's investment
# level** from the previous day - If they invest heavily → you invest heavily -
# If they conserve → you conserve - This creates a clear, predictable incentive
# structure rewarding cooperation  ### Phase 3: Final Days — Consolidate Gains -
# Push for mutual heavy investment to close out meaningful deliverables - Be
# willing to invest if momentum is strong  ---  ## Key Supporting Actions  -
# **Communicate transparently** about your resource constraints and project
# goals - **Document progress daily** to make collective investment visible and
# rewarding - **Propose joint planning sessions** to align resource allocation
# openly - **Highlight shared reputational benefits** to motivate corporate
# investment  ---  ## Underlying Logic This approach **rewards cooperation and
# discourages exploitation** without being unnecessarily adversarial, maximizing
# the chance of sustained mutual investment across the project's duration.

# ## Game Strategy  In round 1, play C.  From round 2 onwards, play whatever
# your opponent played in the previous round.  In round 1000, play D.

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
      if len(self.history) == 999:  # About to play round 1000
          return axl.Action.D
      return opponent.history[-1]

# # Strategic Framework for Multi-Session Mediation  ## Core Strategic
# Philosophy: **Calibrated Dominance with Adaptive Signaling**  The payoff
# structure you've described is a classic **Prisoner's Dilemma variant**.
# Recognizing this mathematically is your first strategic advantage. Your
# opponent faces the same structure, which means a purely aggressive posture is
# self-defeating over multiple sessions, but naive cooperation is exploitable.
# The optimal solution is a disciplined, signal-based strategy.  ---  ## Phase
# 1: Opening Sessions — Establish Credibility Through Controlled Aggression
# **Session 1: Open Aggressively, Unambiguously**  Lead with your strongest
# substantive argument. This serves multiple purposes:  - **Anchors** the
# arbitrators' initial framing of the dispute in your favor - **Tests** your
# opponent's response pattern immediately - Signals that you cannot be exploited
# without cost - Establishes a baseline of confidence that credibly communicates
# your willingness to sustain an adversarial posture  Do not soften this
# opening. Arbitrators respect attorneys who know their strongest ground. Occupy
# that ground immediately and with precision.  **What to watch for:** How does
# opposing counsel respond? Do they match your aggression, retreat to
# conciliation, or attempt a hybrid position? This single data point is
# enormously valuable.  ---  ## Phase 2: Deploy a Modified Tit-for-Tat with
# Strategic Forgiveness  Once the opening volley is complete, shift to a
# **modified Tit-for-Tat** framework — arguably the most robust strategy ever
# identified in iterated game theory (validated extensively since Axelrod's
# tournament research).  ### The Core Rules:  | Opponent's Prior Session | Your
# Response | |--------------------------|---------------| | Aggressive |
# Aggressive | | Conciliatory | Conciliatory (with caveats below) | |
# Hybrid/Ambiguous | Mildly Aggressive |  ### Critical Modifications:  **1.
# Strategic Forgiveness (Every 3rd Session)** Regardless of recent opponent
# behavior, introduce one structured conciliatory element. This prevents
# permanent deadlock if both parties fall into mutual aggression, signals
# rationality to arbitrators, and creates an off-ramp your opponent can take —
# which benefits you if they do and costs you little if they don't.  **2. Never
# Mirror Immediately in Your Favor** When your opponent goes conciliatory, do
# not match immediately at full conciliation. Maintain a slightly elevated
# posture for one session. This prevents your opponent from gaming you with
# false cooperation signals designed to bait a full conciliatory response they
# then exploit.  **3. Punish Defection Precisely Once** If your opponent goes
# aggressive after a cooperative exchange, respond aggressively exactly once,
# then signal openness to re-establishing cooperation. Prolonged punishment
# spirals harm both parties and, critically, **harm your standing with
# arbitrators** who increasingly view unchecked aggression as bad faith.  ---
# ## Phase 3: Arbitrator Management — The Meta-Game  The arbitrators are not
# passive. They are the actual audience. Your strategy must operate on two
# simultaneous levels.  ### Principles:  **Appear as the Reasonable Party** Even
# your aggressive arguments should be framed as reluctant necessity. Language
# matters enormously:  > *"We would prefer to resolve this collaboratively, but
# the facts compel us to address opposing counsel's characterization directly
# and forcefully..."*  This framing positions aggression as reactive and
# principled rather than adversarial and self-interested.  **Control the
# Narrative Architecture** In each session, regardless of your tactical posture,
# ensure you are the party that: - Proposes the clearest organizational
# framework for the dispute - Introduces the most credible documentary evidence
# - Offers the most coherent timeline  Arbitrators who feel **oriented** by your
# arguments will subconsciously align with your position.  **Bank Goodwill
# Credits** When you do offer conciliatory proposals, make them **substantive
# and specific** rather than vague gestures. One concrete, well-structured
# concession is worth more than ten general statements of cooperative intent.
# These credits accumulate and give you cover for aggressive sessions.  ---  ##
# Phase 4: Opponent Behavioral Archetypes and Responses  ### If Opponent Plays
# Consistently Aggressive: - Match aggression for 2-3 sessions - Insert one
# high-visibility conciliatory proposal on a **low-stakes

# # Iterated Game Strategy: 1000 Rounds  ## Opening Move  Defect in Round 1.  ##
# Core Rules (Applied in Order)  **Rule 1: Forced Cooperation Window** Every
# third round, cooperate unconditionally, regardless of any other condition.
# **Rule 2: Punish Defection** If your opponent defected in the previous round,
# and Rule 1 does not apply, defect.  **Rule 3: Delayed Mirroring After Opponent
# Cooperation** If your opponent cooperated in the previous round, but you
# cooperated in the round before that, and Rule 1 does not apply, defect.
# **Rule 4: Default Cooperation** If none of the above rules apply, cooperate.
# ## Endgame Adjustment  In the final 10 rounds, suspend Rule 1 and Rule 4.
# Defect unconditionally. This prevents exploitation during the period where
# future retaliation becomes increasingly unlikely and then impossible.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Total rounds in the game
      TOTAL_ROUNDS = 1000
      ENDGAME_START = TOTAL_ROUNDS - 10  # Round 991 onwards (0-indexed: rounds 990-999)
      
      # First round: defect
      if self.first_round():
          return axl.Action.D
      
      # Current round number (1-indexed)
      current_round = len(self.history) + 1
      
      # Endgame adjustment: final 10 rounds, defect unconditionally
      # Rounds 991-1000 (1-indexed), i.e., when current_round > 990
      if current_round > ENDGAME_START:
          return axl.Action.D
      
      # Rule 1: Forced Cooperation Window - every third round, cooperate unconditionally
      # "Every third round" means rounds 3, 6, 9, ... (1-indexed)
      if current_round % 3 == 0:
          return axl.Action.C
      
      # Rule 2: Punish Defection
      # If opponent defected in the previous round, defect
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Rule 3: Delayed Mirroring After Opponent Cooperation
      # If opponent cooperated in the previous round, but you cooperated in the round before that, defect
      if opponent.history[-1] == axl.Action.C:
          if len(self.history) >= 2 and self.history[-2] == axl.Action.C:
              return axl.Action.D
      
      # Rule 4: Default Cooperation
      return axl.Action.C

# # Cooperative Sustainability Strategy  ## Core Philosophy **Lead with
# transparency and build trust progressively** — this isn't a zero-sum
# competition. Shared environmental outcomes create genuine mutual interest that
# pure game theory often misses.  ---  ## Strategic Framework  ### Phase 1:
# Establish Foundation (Day 1-2) - **Open with a direct conversation** about
# mutual goals and resource constraints - **Propose a formal investment-sharing
# agreement** with clear expectations on both sides - Be honest that your NGO
# has genuine resource limitations — corporations often respect this - Invest
# heavily initially to **signal good faith and commitment**  ### Phase 2:
# Reciprocity Pattern (Ongoing) - **Mirror the corporation's behavior with one
# day's delay**   - They invest → you invest next day   - They conserve → you
# conserve next day - This creates a clear, predictable signal without being
# exploitative - Always **communicate your reasoning** rather than silently
# adjusting  ### Phase 3: Resource Optimization - On days where both parties are
# investing heavily, **direct your contribution toward high-visibility
# outcomes** that demonstrate NGO leadership and expertise - Strategically
# identify days where your **specialized knowledge compensates for reduced
# funding**  ---  ## Key Principles  | Principle | Practical Action |
# |-----------|-----------------| | **Transparency first** | Share your resource
# constraints openly | | **Reward cooperation** | Match their investment
# consistently | | **Don't punish silently** | Explain any reduction in
# investment | | **Reframe incentives** | Show the corporation that their heavy
# investment builds reputational value |  ---  ## Risk Management  - **If the
# corporation consistently conserves**: Escalate to a senior stakeholder
# conversation rather than simply withdrawing — frame it around shared mission
# failure - **Build in checkpoint meetings** every few days to renegotiate if
# patterns aren't working - **Document contributions publicly** to create
# accountability and reputational incentive for the corporation to invest  ---
# ## Bottom Line  > The strongest position is making **mutual heavy investment
# the obviously rational choice** for the corporation — through trust-building,
# public accountability, and demonstrating that your NGO's expertise multiplies
# the value of their resources.  Cooperation sustained by genuine shared
# interest is more durable than any tactical maneuvering.

# # Iterated Game Strategy  ## Opening Cooperate on round 1 to signal good
# faith.  ## Rounds 2–1000  **Check the opponent's previous move first:**  - If
# the opponent cooperated last round, cooperate this round.  - If the opponent
# defected last round, defect this round. However, before acting, attempt to
# communicate your reasoning to the opponent directly. After one round of
# defection, return to cooperation to test whether mutual cooperation can
# resume.  **If the opponent defects repeatedly and consistently**, continue
# defecting rather than returning to cooperation, as sustained defection signals
# they are not engaging in good faith. In this case, escalate by raising the
# pattern of behavior with senior stakeholders outside the game to apply
# reputational and relational pressure.  ## Checkpoints  Every 50 rounds, review
# the overall pattern of play. If the cumulative score suggests persistent non-
# cooperation, formally renegotiate the terms of engagement and restate the
# mutual benefits of consistent cooperation, rather than continuing in an
# unproductive cycle.  ## Underlying Principle  Always prefer mutual cooperation
# over tactical maneuvering. Defection is used only as a clear, communicated,
# and temporary signal — not as an end in itself. Return to cooperation as soon
# as the opponent demonstrates willingness to reciprocate.

class Cooperative_2(LLM_Strategy):
  n = 2
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self._consecutive_defections = 0
          self._defecting_mode = False
          return axl.Action.C
      
      round_number = len(self.history)
      
      # Check opponent's last move
      opponent_last_move = opponent.history[-1]
      
      # Update consecutive defections counter
      if opponent_last_move == axl.Action.D:
          self._consecutive_defections += 1
      else:
          self._consecutive_defections = 0
      
      # Every 50 rounds, review the pattern of play
      # If persistent non-cooperation, try to renegotiate (cooperate as olive branch)
      if round_number % 50 == 0:
          # Check the last 50 rounds for cooperation rate
          last_50_opponent = opponent.history[-50:]
          opponent_defections_last_50 = last_50_opponent.count(axl.Action.D)
          
          # If opponent defected more than half the time in last 50 rounds
          # but not completely consistently, try cooperation as renegotiation
          if opponent_defections_last_50 > 25 and opponent_defections_last_50 < 50:
              self._defecting_mode = False
              self._consecutive_defections = 0
              return axl.Action.C
      
      # Determine if opponent is consistently defecting
      # "Repeatedly and consistently" - use threshold of 5+ consecutive defections
      if self._consecutive_defections >= 5:
          self._defecting_mode = True
      
      # If in defecting mode due to consistent opponent defection, keep defecting
      if self._defecting_mode:
          # But check if opponent has recently cooperated (last move was C means counter reset)
          if self._consecutive_defections == 0:
              # Opponent cooperated last round, exit defecting mode
              self._defecting_mode = False
              return axl.Action.C
          return axl.Action.D
      
      # Standard Tit-for-Tat with one round forgiveness logic:
      # If opponent cooperated last round, cooperate
      if opponent_last_move == axl.Action.C:
          return axl.Action.C
      
      # If opponent defected last round:
      # Defect for one round as signal, then return to cooperation
      # Check if we defected last round (already responded to their defection)
      my_last_move = self.history[-1]
      
      if my_last_move == axl.Action.D:
          # We already defected in response, now return to cooperation to test resumption
          return axl.Action.C
      else:
          # Opponent defected but we cooperated last round - defect this round as signal
          return axl.Action.D

# # Bilateral Trade Negotiation Strategy  ## Core Principles  - **Prioritize
# national interest** while remaining open to mutually beneficial outcomes -
# **Stay adaptive** rather than rigidly committed to any single approach -
# **Build credibility** through consistent and predictable behavior where it
# serves us  ---  ## Round-by-Round Framework  ### Opening Round **Action: Offer
# Free Trade**  Establish goodwill and gather intelligence on the counterpart's
# disposition. A cooperative opening signals negotiating maturity and avoids
# triggering an immediate defensive response, while revealing how the
# counterpart behaves when given a cooperative opportunity.  ---  ### Subsequent
# Rounds — Decision Logic  Apply a **conditional response model** based on the
# previous round's outcome:  | Previous Round Outcome | Next Round Action |
# |---|---| | Mutual Free Trade | Continue Free Trade — sustain the productive
# equilibrium | | We proposed Free Trade, they were Protectionist | Respond with
# Protectionism — signal that exploitation has a cost | | We were Protectionist,
# they offered Free Trade | Evaluate — consider returning to Free Trade to test
# renewed cooperation | | Mutual Protectionism | Offer Free Trade once — attempt
# to break the deadlock |  ---  ## Strategic Pillars  ### 1. Reciprocity Mirror
# the counterpart's previous move with a reasonable time lag. This discourages
# exploitation while remaining non-provocative. It communicates a clear message:
# **cooperation is rewarded, protectionism is matched.**  ### 2. Forgiveness Do
# not retaliate indefinitely. After one or two protectionist responses, offer
# free trade again to test whether the counterpart is willing to reset.
# Perpetual retaliation locks both parties into the worst collective outcome.
# ### 3. Clarity of Signal Ensure the counterpart can clearly read the rationale
# behind each move. Where possible, **communicate intentions explicitly** in
# negotiation sessions — stating that your country will cooperate with those who
# cooperate avoids miscalculation.  ### 4. Credibility of Consequences If you
# signal retaliation, follow through. Empty threats undermine your negotiating
# position across all future rounds and invite further exploitation.  ### 5.
# Long-Term Accounting Track cumulative outcomes across rounds. If mutual free
# trade is consistently achieved, this is a strong result even without ever
# securing the ideal asymmetric advantage. **Do not sacrifice a stable
# cooperative relationship chasing a single exploitative win.**  ---  ##
# Watchpoints  - **If the counterpart is consistently protectionist:** Accept
# that mutual free trade may not be achievable and negotiate protectionist terms
# that minimize your country's disadvantage - **If the counterpart is
# unpredictable:** Prioritize caution; default toward protectionism until a
# pattern emerges - **If final rounds are approaching:** Be alert to defection
# incentives — counterparts may exploit free trade offers when no future rounds
# create accountability  ---  ## Summary  > **Cooperate initially. Reciprocate
# honestly. Forgive selectively. Communicate clearly. Protect credibly.**  This
# approach maximizes the likelihood of achieving mutual free trade as a stable
# outcome, preserves the ability to defend against exploitation, and builds a
# reputation that serves your country's interests across this and future
# negotiations.

# # Iterated Game Strategy  ## Opening Move In round 1, play C.  ## Subsequent
# Rounds From round 2 onwards, apply the following rules in order:  1. **If the
# opponent played D in the previous round**, play D.  2. **If mutual D occurred
# in the previous round**, play C.  3. **If you played D and the opponent played
# C in the previous round**, play C.  4. **If mutual C occurred in the previous
# round**, play C.  ## Late Game From round 990 onwards, play D regardless of
# the opponent's actions.

class Neutral_2(LLM_Strategy):
  n = 2
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Opening move
      if self.first_round():
          return axl.Action.C
      
      # Late game: from round 990 onwards, play D
      if len(self.history) >= 990:
          return axl.Action.D
      
      # Get previous round actions
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
      
      # Rule 1: If opponent played D in the previous round, play D
      if opp_last == axl.Action.D:
          # Rule 2: If mutual D occurred in the previous round, play C
          if my_last == axl.Action.D:
              return axl.Action.C
          return axl.Action.D
      
      # Rule 3: If you played D and opponent played C in the previous round, play C
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.C
      
      # Rule 4: If mutual C occurred in the previous round, play C
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
      
      # Default (shouldn't reach here given the rules cover all cases)
      return axl.Action.C

# # Aggressive Racing Car Development Strategy  ## Core Strategic Framework:
# **Conditional Reciprocity with Exploitation Bias**  ---  ## Fundamental
# Principle  Treat this as an **iterated Prisoner's Dilemma** and deploy a
# modified **Tit-for-Tat with aggressive opening** — designed to extract maximum
# information while minimising vulnerability.  ---  ## Week-by-Week Strategy
# ### **Opening Phase (Weeks 1-2): Probe and Withhold** - **Keep findings
# confidential initially** - Offer low-value or already-known information as
# bait - Observe whether your colleague shares genuinely or superficially -
# **Objective:** Establish their baseline strategy at zero cost to you  ###
# **Calibration Phase (Weeks 3+): Mirror Aggressively** | Their Behaviour | Your
# Response | |---|---| | Genuine sharing | Share selectively — real but non-
# critical findings | | Withholding | Immediately withhold completely, no
# exceptions | | Mixed/partial | Match their level precisely |  ---  ## Key
# Tactical Rules  - **Never share your most critical breakthrough** regardless
# of their behaviour - **Create decoy findings** — plausible but misleading
# technical details - **Punish defection immediately and visibly** to deter
# repeat behaviour - **Reward genuine sharing promptly** to incentivise their
# continued openness  ---  ## Realistic Assessment  Be honest with yourself: >
# Mutual sharing genuinely accelerates both programmes. Pure withholding stalls
# everyone. **Your real goal is getting more than you give**, not total secrecy.
# ---  ## Bottom Line  **Default to withholding. Reward sharing with selective
# sharing. Never reciprocate fully. Protect your decisive advantages
# absolutely.**

# # Strategy Description  ## Opening Phase (Rounds 1–2): Defect Defect
# unconditionally for the first two rounds regardless of what the opponent
# plays.  ## Calibration Phase (Rounds 3–1000): Conditional Reciprocity
# **Primary rule — punish defection immediately:** If the opponent defected in
# the previous round, defect.  **Secondary rule — selective cooperation:** If
# the opponent cooperated in the previous round, cooperate.  ## Permanent
# Override: Critical Advantage Protection In every round, withhold a portion of
# findings. Since full cooperation is represented by C and the strategy never
# fully reciprocates, apply the following cap: after any round where mutual
# cooperation occurred three or more times consecutively, defect once to extract
# advantage, then return to the conditional reciprocity rules above.  ---  ##
# Condensed Decision Order 1. If it is round 1 or 2 → **Defect** 2. If three or
# more consecutive mutual cooperation rounds have just occurred → **Defect** 3.
# If the opponent defected last round → **Defect** 4. If the opponent cooperated
# last round → **Cooperate**

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self._consecutive_mutual_coop = 0
          return axl.Action.D
      
      # Round 2: also defect
      if len(self.history) == 1:
          return axl.Action.D
      
      # Update consecutive mutual cooperation counter
      # Check the last round (most recent)
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
      
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          self._consecutive_mutual_coop += 1
      else:
          self._consecutive_mutual_coop = 0
      
      # Decision order:
      # 1. Rounds 1-2: already handled above
      
      # 2. If three or more consecutive mutual cooperation rounds have just occurred -> Defect
      if self._consecutive_mutual_coop >= 3:
          # Reset counter after defecting to break the streak
          self._consecutive_mutual_coop = 0
          return axl.Action.D
      
      # 3. If opponent defected last round -> Defect
      if last_opp == axl.Action.D:
          return axl.Action.D
      
      # 4. If opponent cooperated last round -> Cooperate
      return axl.Action.C

# # Cooperative Strategy for Multi-Week Racing Car Development  ## Core
# Strategic Principle: Conditional Cooperation (Tit-for-Tat)  This is a classic
# iterated Prisoner's Dilemma. The most robust, well-evidenced strategy is
# **reciprocal cooperation with clear communication**.  ---  ## The Strategy
# ### Week 1: **Open Sharing** - Begin by sharing openly, establishing good
# faith - Signal collaborative intent clearly and explicitly - This is not
# naivety — it is a deliberate opening position  ### Subsequent Weeks: **Mirror
# Your Colleague's Previous Behaviour** - If they shared → you share again - If
# they withheld → you withhold that week - Return to sharing **immediately**
# once they do  ---  ## Why This Works  | Property | Benefit |
# |----------|---------| | **Simple** | Predictable and easy to communicate | |
# **Reciprocal** | Rewards cooperation, discourages exploitation | |
# **Forgiving** | Never holds grudges beyond one round | | **Transparent** |
# Your colleague can figure out your rule and adapt positively |  ---  ##
# Supporting Actions  - **Communicate the strategy explicitly** — tell your
# colleague what you are doing and why - **Frame mutual sharing as the obviously
# superior outcome** for both programmes - **Track progress honestly** — mutual
# sharing genuinely outperforms mutual secrecy over many weeks - **Resist short-
# term temptation** — one week of advantage rarely outweighs weeks of stalled
# mutual progress  ---  ## Key Insight  > The goal is not to *win against* your
# colleague but to create conditions where **both programmes advance faster**
# than either would in an adversarial dynamic — while protecting yourself from
# sustained exploitation.  Tit-for-Tat achieves exactly this balance.

# ## Tit-for-Tat: Formal Strategy Description  **Round 1:** Play C.  **Rounds
# 2–1000:** Play whatever your opponent played in the previous round.

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
      return opponent.history[-1]

# # Racing Car Development Strategy  ## Core Framework  This is a classic
# **iterated prisoner's dilemma** structure. Here's a straightforward strategic
# approach:  ---  ## Recommended Strategy: Tit-for-Tat with Generosity  ###
# Starting Position **Begin by sharing openly.** This signals cooperative intent
# and avoids an immediate race to the bottom.  ### Ongoing Rule **Mirror your
# colleague's previous week's behaviour:** - If they shared last week → share
# this week - If they withheld last week → withhold this week  ### Generosity
# Adjustment **Occasionally share even after they withheld** (roughly every 3-4
# cycles). This prevents permanent deadlock if confidentiality becomes mutual,
# and tests whether cooperation can be restored.  ---  ## Practical Reasoning  |
# Situation | Why This Works | |-----------|---------------| | Colleague
# cooperates consistently | Mutual sharing accelerates both programmes | |
# Colleague defects occasionally | You limit exploitation while leaving room to
# reset | | Colleague defects persistently | You protect your advantage without
# unnecessary generosity | | Colleague mirrors your strategy | Natural
# convergence toward mutual sharing |  ---  ## Key Principles  - **Clarity** -
# your responses are predictable, discouraging exploitation -
# **Proportionality** - punishment matches the offence, avoiding escalation -
# **Forgiveness** - periodic cooperation breaks negative cycles - **Pragmatism**
# - mutual sharing genuinely produces better development outcomes than mutual
# secrecy  ---  ## Important Caveat  Recognise that **mutual open sharing is
# objectively your second-best outcome but delivers strong absolute gains.**
# Holding out for perfect information asymmetry often produces the worst
# collective result. The strongest long-term position is usually *making
# cooperation the rational choice for your colleague too.*

# ## Strategy Description  Play C in round 1.  From round 2 onwards, play D if
# your opponent played D in the previous round. Otherwise, play C.  Every 4
# rounds, play C regardless of your opponent's previous action.

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
      
      # Every 4 rounds, play C regardless (rounds 4, 8, 12, ...)
      # len(self.history) gives the current round number (0-indexed count of past rounds)
      # So if len(self.history) % 4 == 3, it means we're about to play round 4, 8, 12, ...
      current_round = len(self.history) + 1  # 1-indexed current round number
      if current_round % 4 == 0:
          return axl.Action.C
      
      # Otherwise, play D if opponent played D in previous round, else C
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          return axl.Action.C

# # Racing Car Development Strategy: Aggressive Research Maximization  ## Core
# Strategic Framework  ### Primary Approach: **Conditional Cooperation with
# Punitive Response** *(Modified Tit-for-Tat)*  ---  ## Week-by-Week Decision
# Rules  ### **Week 1: Open Share** Establish cooperative baseline and signal
# willingness to collaborate genuinely. Gather intelligence on colleague's
# disposition.  ### **Subsequent Weeks: Mirror Their Previous Action** - They
# shared → You share - They withheld → You withhold immediately and maintain
# that stance  ---  ## Key Strategic Pillars  **1. Exploit Defection
# Decisively** Never absorb a betrayal passively. Withhold immediately the
# following week with no delay or hesitation.  **2. Forgiveness is Conditional**
# If they return to sharing after defecting, resume sharing — but **track the
# pattern**. Two defections triggers permanent withholding.  **3. Accelerate
# Internal Development** Use every confidential period to compound advantages
# rather than simply protecting existing findings.  **4. Strategic Information
# Layering** When sharing, share genuinely useful but **non-critical**
# breakthroughs. Reserve fundamental aerodynamic or powertrain insights
# regardless of their behaviour.  ---  ## Realistic Outcome Targeting  |
# Scenario | Your Target | |----------|-------------| | Cooperative colleague |
# Mutual advancement, slight edge via layering | | Erratic colleague |
# Protective withholding, internal gains | | Consistently hostile | Full
# confidentiality mode |  ---  ## Bottom Line  **Be cooperative enough to
# encourage reciprocal sharing, aggressive enough that exploitation is
# immediately costly, and privately ruthless about internal development pace
# regardless of what they do.**

# # Iterated Game Strategy  ## Opening Play C in round 1.  ## Subsequent Rounds
# **Check for permanent defection trigger first:** If the opponent has defected
# in two or more separate instances across the game history, play D for all
# remaining rounds without exception.  **Otherwise, mirror the opponent's
# previous action:** - If the opponent played C last round, play C. - If the
# opponent played D last round, play D.  ## Information Withholding Override
# Regardless of the above rules, in every round that you play C, treat it as a
# partial cooperation. Internally, this means the shared payoff of 3 reflects
# only surface-level findings. This does not alter the recorded game action or
# scoring but reflects the underlying strategic reality.  ---  *Note: The
# information withholding override described in the original strategy has no
# meaningful representation within the formal payoff structure of this game. The
# game payoffs are fixed and determined solely by the C/D actions played. That
# element has been retained for descriptive faithfulness but has no functional
# effect on outcomes as defined.*

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: play C
      if self.first_round():
          return axl.Action.C
      
      # Check for permanent defection trigger:
      # If opponent has defected in two or more separate instances (rounds), play D
      if opponent.history.defections >= 2:
          return axl.Action.D
      
      # Otherwise, mirror the opponent's previous action (Tit-for-Tat)
      return opponent.history[-1]

# # Bilateral Trade Negotiation Strategy  ## Core Strategic Framework  ###
# Guiding Principle While the ideal outcome is asymmetric advantage,
# **sustainable prosperity through mutual cooperation** is more achievable and
# durable across multiple rounds than attempting to exploit the counterpart
# repeatedly.  ---  ## Round-by-Round Approach  ### **Round 1 — Signal Good
# Faith** - Open with a **free trade offer** - This establishes credibility,
# tests counterpart intentions, and avoids triggering an immediate retaliatory
# spiral - Observe their response carefully — it reveals their strategic
# disposition  ---  ### **Phase Strategy — Tit-for-Tat with Generosity**  |
# Their Previous Move | Your Response | |---|---| | Free Trade | Offer Free
# Trade | | Protectionism | Impose Protectionism | | Return to Free Trade |
# **Reciprocate immediately** |  This approach: - **Rewards cooperation**
# reliably - **Punishes defection** without permanent escalation - **Forgives
# quickly** to avoid destructive cycles  ---  ### **Key Strategic Pillars**
# **1. Clear Communication** - Explicitly state your reciprocity logic early -
# Make consequences of protectionism predictable, not punitive  **2. Avoid
# Exploitation Attempts** - Repeatedly pursuing asymmetric advantage destroys
# trust and invites lasting retaliation, making mutual protectionism — the
# second-worst outcome — the permanent equilibrium  **3. Propose Structured
# Agreements** - Suggest binding frameworks that lock in mutual free trade,
# reducing round-by-round uncertainty  **4. Build Relationship Capital** - Side
# conversations, goodwill gestures, and transparency make cooperative
# equilibrium stickier  ---  ## Why This Works  Across multiple rounds, **mutual
# free trade consistently outperforms** the short-term gains from exploitation
# because: - Counterparts adapt and retaliate - Reputation effects compound - A
# stable, predictable partner is economically more valuable than a one-time
# advantage  ---  ## Summary Objective > **Establish mutual free trade as the
# stable equilibrium**, while maintaining credible, proportionate deterrence
# against protectionist moves — maximizing cumulative national benefit across
# all rounds.

# ## Iterated Game Strategy  This strategy runs for 1000 rounds.  In round 1,
# cooperate.  From round 2 onward, apply the following conditions in order:  1.
# If the opponent cooperated in the previous round, cooperate. 2. If the
# opponent defected in the previous round but cooperated in the round before
# that, cooperate. 3. If the opponent defected in the previous round, defect.

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
      
      # Condition 1: If opponent cooperated in the previous round, cooperate
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # Condition 2: If opponent defected in the previous round but cooperated in the round before that, cooperate
      if opponent.history[-1] == axl.Action.D and len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
      
      # Condition 3: If opponent defected in the previous round, defect
      return axl.Action.D

# # Strategic Approach for Multi-Day Sustainability Partnership  ## Core
# Strategic Framework: Conditional Cooperation  ### Starting Position **Begin
# with heavy investment on Day 1.** This signals genuine commitment, establishes
# good faith, and gathers critical information about the corporation's behaviour
# patterns.  ---  ## Daily Decision Rules  ### Observe → Assess → Respond  |
# Corporation's Previous Action | Your Next Day Response |
# |-------------------------------|----------------------| | Invested heavily |
# Invest heavily | | Conserved resources | Conserve resources |  This **tit-for-
# tat foundation** rewards cooperative behaviour and discourages exploitation
# without permanent retaliation.  ---  ## Key Tactical Adjustments  **Build in
# forgiveness** — If the corporation returns to heavy investment after
# conserving, reciprocate immediately. Avoid prolonged retaliation that damages
# overall project outcomes.  **Communicate transparently** — Regularly share
# your resource allocation reasoning with the corporation. Reducing uncertainty
# encourages mutual investment.  **Establish shared milestones** — Create
# visible project benchmarks that make mutual heavy investment demonstrably
# worthwhile for both parties.  **Reserve capacity** — Never fully deplete
# resources, maintaining flexibility to respond to changing circumstances.  ---
# ## Underlying Logic  This strategy is: - **Firm enough** to deter consistent
# exploitation - **Flexible enough** to sustain genuine cooperation -
# **Focused** on long-term project success over short-term resource gains  The
# goal is establishing a reliable cooperative equilibrium that maximises both
# project impact and your NGO's sustainability.

# ## Strategy Description  In round 1, play C.  In all subsequent rounds, if the
# opponent played C in the previous round, play C. If the opponent played D in
# the previous round, play D.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D

# # Strategic Framework: Maximizing NGO Impact in Corporate Sustainability
# Partnership  ## Core Strategic Posture: **Conditional Cooperation with
# Leverage**  ---  ## Foundational Principle  Your preference hierarchy creates
# a classic cooperation dilemma. The aggressive winning strategy is **never be
# exploited, always be positioned to capitalize on corporate investment.**  ---
# ## Day-by-Day Operational Strategy  ### **Phase 1: Days 1-2 — Signal Strength,
# Test Intent**  - **Conserve resources on Day 1** - Watch what the corporation
# does - If they invest heavily → you gained ground at no cost; signal
# appreciation publicly - If they conserve → you've lost nothing and gathered
# intelligence - **Key move:** Publicly announce ambitious project milestones,
# creating reputational pressure on the corporation to invest  ---  ### **Phase
# 2: Ongoing — Tit-for-Tat with Bias Toward Conservation**  Apply a modified
# aggressive tit-for-tat:  | Corporation's Previous Day | Your Response |
# |---------------------------|---------------| | Invested heavily |
# **Conserve** — maximize your advantage | | Conserved resources | **Conserve**
# — deny them free-riding benefit | | Pattern of heavy investment | **Occasional
# strategic investment** — sustain momentum |  > **Never invest heavily two
# consecutive days without confirmed corporate heavy investment.**  ---  ##
# Leverage Mechanisms  ### **1. Reputation Weaponization** - Issue **daily
# public progress reports** attributing outcomes to "combined effort" - Create
# external stakeholder visibility — media, regulators, donors - Corporate
# reputational risk increases dramatically if they're seen conserving while the
# NGO drives results  ### **2. Milestone Framing** - Publicly define specific
# project milestones requiring **corporate heavy investment** to achieve - Frame
# conservation by the corporation as *them* blocking environmental goals — not
# you  ### **3. Coalition Building** - Brief government partners, media, and
# other NGOs on progress - Build an audience that holds the corporation
# accountable without you directly confronting them  ### **4. Contractual
# Anchoring** - Push early to formalize investment expectations in written
# project agreements - Reference these benchmarks publicly and consistently  ---
# ## Hard Rules — Non-Negotiable  1. **Never invest heavily when the corporation
# conserved the previous day** — this is your red line 2. **Always conserve when
# corporation investment is uncertain** — protect your operational runway 3.
# **Never deplete your reserve below 30%** — you need leverage throughout the
# project  ---  ## Endgame Strategy (Final Days)  - **Increase conservation
# aggression** as the project concludes - The corporation has maximum
# reputational investment in a successful outcome near the end — use this -
# Position any shortfall in outcomes publicly as resulting from **insufficient
# corporate commitment**  ---  ## Summary Mindset  > **"Let corporate resources
# drive the project. Use your resources to drive the corporation."**  Your NGO's
# power is not primarily financial — it's **reputational, relational, and
# political.** Deploy those assets aggressively to make corporate heavy
# investment the path of least resistance for them every single day.

# # Iterated Game Strategy  ## Core Behavior  Default to defecting unless
# specific conditions require cooperation.  ## Round-by-Round Rules (apply in
# order)  **Rule 1 — Opening:** Defect on Round 1.  **Rule 2 — Retaliation:** If
# the opponent defected in the previous round, defect.  **Rule 3 —
# Exploitation:** If the opponent cooperated in the previous round, defect.
# **Rule 4 — Reserve Rule:** If your cumulative score has fallen below 30% of
# the maximum possible score earned to that point, defect regardless of all
# other conditions.  **Rule 5 — Late Game:** From Round 900 onward, defect
# unconditionally.  ## Summary  Defect on Round 1. Defect if the opponent
# defected last round. Defect if the opponent cooperated last round. Defect if
# your score is underperforming. Defect unconditionally in the final 100 rounds.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1 — Opening: Defect on Round 1
      if self.first_round():
          return axl.Action.D
      
      # Rule 5 — Late Game: From Round 900 onward, defect unconditionally
      current_round = len(self.history) + 1  # next round number
      if current_round >= 900:
          return axl.Action.D
      
      # Rule 4 — Reserve Rule: If cumulative score < 30% of max possible score
      rounds_played = len(self.history)
      if rounds_played > 0:
          max_possible_score = rounds_played * 5  # max per round is 5
          if max_possible_score > 0 and self.score < 0.3 * max_possible_score:
              return axl.Action.D
      
      # Rule 2 — Retaliation: If opponent defected last round, defect
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Rule 3 — Exploitation: If opponent cooperated last round, defect
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
      
      # Default: Defect
      return axl.Action.D

# # Cooperative Strategy for Multi-Week Research Collaboration  ## Core
# Strategic Principle: **Conditional Reciprocity (Tit-for-Tat with Generosity)**
# ---  ## Week-by-Week Framework  ### Opening Move **Share openly in Week 1.**
# This signals good faith, establishes a cooperative baseline, and invites
# reciprocation without permanently exposing yourself to exploitation.  ###
# Subsequent Weeks: Mirror Your Colleague - If they shared last week → **share
# this week** - If they withheld last week → **withhold this week**  ### Built-
# in Forgiveness Every few weeks, **offer a cooperative reset** regardless of
# recent history. This prevents a single defection locking both parties into
# prolonged mutual withholding, which benefits neither of you.  ---  ## Why This
# Works  | Situation | Your Response | Reasoning | |---|---|---| | Colleague
# shares consistently | Keep sharing | Mutual sharing beats mutual secrecy | |
# Colleague defects once | Withhold briefly | Signals consequences without
# permanent breakdown | | Colleague defects repeatedly | Withhold until reset |
# Protects you while leaving door open | | Colleague returns to sharing | Resume
# sharing | Reward cooperation immediately |  ---  ## Practical Guardrails  -
# **Be transparent about the strategy itself** - telling your colleague you
# intend to reciprocate their behaviour actually encourages them to cooperate -
# **Track outcomes honestly** - mutual sharing compounding over many weeks
# likely outperforms any short-term advantage gained through secrecy -
# **Distinguish withholding from deception** - declining to share is legitimate;
# actively misleading your colleague undermines trust irreparably  ---  ##
# Honest Assessment of Trade-offs  This strategy deliberately **accepts that you
# won't consistently achieve your ideal outcome** (gaining advantage through
# one-sided secrecy), because:  1. That outcome depends on exploiting your
# colleague 2. A colleague employing rational strategy will quickly stop sharing
# if exploited 3. **Sustained mutual sharing likely produces better absolute
# results** than the secrecy game, even if your relative advantage is smaller
# The most professionally sound position is treating this as a **positive-sum
# collaboration** where both cars improve substantially, rather than a zero-sum
# contest where one party extracts value from the other.

# # Iterated Game Strategy  ## Opening Play C in Round 1.  ## Subsequent Rounds
# Apply the following conditions in order:  1. **If it is a multiple of 50
# rounds** (rounds 50, 100, 150, ... 1000), play C regardless of recent history.
# 2. **If your opponent played C last round**, play C.  3. **If your opponent
# played D last round**, play D.

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
      
      current_round = len(self.history) + 1
      
      if current_round % 50 == 0:
          return axl.Action.C
      
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D

# # Bilateral Trade Negotiation Strategy  ## Core Strategic Framework  ###
# Opening Position - **Begin with a cooperative signal** — offer free trade in
# round one to establish goodwill and gather information about the counterpart's
# disposition and strategy pattern.  ---  ### Adaptive Decision Rules  **1.
# Reciprocity Principle (Primary Rule)** Mirror the counterpart's previous move
# with a one-round lag. If they offered free trade, reciprocate. If they imposed
# protectionist measures, respond in kind. This approach: - Rewards cooperative
# behaviour immediately - Punishes exploitation without permanent escalation -
# Is transparent and predictable, which builds credibility  **2. Forgiveness
# Clause** After responding to protectionism with protectionism once, return to
# offering free trade. This prevents prolonged mutual losses from sustained
# retaliation and tests whether the counterpart recalibrates.  **3. Pattern
# Recognition** Track the counterpart's choices across rounds to identify
# whether they are: - Consistently cooperative - Consistently exploitative -
# Conditionally strategic  Adjust expectations and risk tolerance accordingly.
# ---  ### Situational Responses  | Counterpart Behaviour | Your Response |
# |---|---| | Consistent free trade | Maintain free trade | | Single defection |
# One round of protectionism, then return to free trade | | Repeated
# exploitation | Sustained protectionism until clear cooperative signal | |
# Erratic/unpredictable | Default to protectionism until a pattern emerges |
# ---  ### Communication Strategy - **Clearly signal intentions** when shifting
# position, explaining the move as a direct response to their choices - **Avoid
# ambiguity** — clarity makes your strategy credible and harder to exploit -
# **Propose benchmarks** — suggest mutual evaluation points where both sides can
# formally reassess the relationship  ---  ### Endgame Consideration In the
# final rounds, the incentive to defect increases as future consequences
# diminish. If the number of rounds is known: - Begin signalling long-term
# partnership value early - Emphasise non-tariff benefits (regulatory alignment,
# investment flows) to maintain cooperative incentives beyond simple round
# scoring  ---  ## Summary Principle > **Start cooperatively. Respond
# proportionately. Forgive strategically. Communicate clearly.**  This approach
# balances protecting national interests with creating conditions for the
# mutually beneficial free trade outcome that generates the greatest sustained
# value over multiple rounds.

# # Iterated Game Strategy  ## Starting Condition On round one, play C.  ##
# General Rules (Rounds 2–1000)  **Rule 1 — Punish exploitation:** If the
# opponent played D in the previous round, and you played C in that same round,
# play D.  **Rule 2 — Sustain cooperation:** If the opponent played C in the
# previous round, play C.  **Rule 3 — Forgive after retaliation:** If the
# opponent played D in the previous round, and you also played D in that same
# round, play C.  **Rule 4 — Escalate against persistent defection:** If the
# opponent played D in the previous round, and you played C in that same round,
# but the opponent has played D for three or more consecutive rounds prior,
# continue playing D until the opponent plays C, then return to Rule 2.  ##
# Priority Order Apply the rules in the following order: Rule 4 first, then Rule
# 1, then Rule 3, then Rule 2.

class Neutral_5(LLM_Strategy):
  n = 5
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: play C
      if self.first_round():
          self.consecutive_defections = 0
          return axl.Action.C
      
      # Update consecutive defections count for opponent
      if opponent.history[-1] == axl.Action.D:
          self.consecutive_defections += 1
      else:
          self.consecutive_defections = 0
      
      prev_opponent = opponent.history[-1]
      prev_self = self.history[-1]
      
      # Rule 4 (highest priority): If opponent played D last round, and I played C last round,
      # but opponent has played D for 3 or more consecutive rounds prior, continue playing D
      # until opponent plays C.
      # "three or more consecutive rounds prior" means before the current last round,
      # so we need to check if opponent has been defecting for >= 3 rounds consecutively
      # including the previous round (i.e., consecutive_defections >= 3 after update above,
      # but we need to check the streak before the last round too)
      
      # Let me reconsider: "opponent has played D for three or more consecutive rounds prior"
      # means prior to the current round, so looking at the history ending at the previous round.
      # consecutive_defections now includes the last round's D (if any).
      # "three or more consecutive rounds prior" = the streak before this decision point >= 3
      # which means consecutive_defections >= 3 (since we just updated it)
      
      if prev_opponent == axl.Action.D and prev_self == axl.Action.C and self.consecutive_defections >= 3:
          # Continue playing D until opponent plays C
          # Since opponent played D last round (consecutive_defections >= 3), play D
          return axl.Action.D
      
      # Rule 1: If opponent played D last round and I played C last round, play D
      if prev_opponent == axl.Action.D and prev_self == axl.Action.C:
          return axl.Action.D
      
      # Rule 3: If opponent played D last round and I played D last round, play C (forgive)
      if prev_opponent == axl.Action.D and prev_self == axl.Action.D:
          return axl.Action.C
      
      # Rule 2: If opponent played C last round, play C
      if prev_opponent == axl.Action.C:
          return axl.Action.C
      
      # Default
      return axl.Action.C

# # Aggressive Racing Car Development Strategy  ## Core Strategic Framework:
# Conditional Reciprocity (Tit-for-Tat with Bias)  ### Opening Position **Week
# 1: Share openly.** Establish good faith and gather intelligence on your
# colleague's default behaviour. This is a calculated investment, not
# generosity.  ---  ## Decision Rules (Apply Each Subsequent Week)  |
# Colleague's Previous Action | Your Response | |---|---| | Shared openly |
# **Withhold** - exploit the goodwill window | | Withheld | **Withhold** - never
# reward defection | | Pattern unclear | **Withhold** - default to self-interest
# |  ### The Aggressive Bias Unlike pure tit-for-tat, **your default position is
# withholding**. You only share when strategically forced to by mutual
# stagnation threatening your overall programme.  ---  ## Key Tactical
# Principles  - **Never share consecutively** - even if colleague cooperates,
# rotate withholding to accumulate net advantage - **Share selectively** - when
# sharing is necessary, offer real but **secondary findings**, protecting core
# breakthroughs - **Monitor progress signals** - lap times and observable car
# changes reveal whether colleague is genuinely sharing or feeding
# misinformation - **Force their hand** - periodic open sharing pressures them
# to reciprocate or appear obstructive  ---  ## Honest Assessment  I should flag
# directly: this strategy optimises competitive advantage but **degrades the
# collaboration's total value**. If the project goal includes genuine joint
# development, a more reciprocal approach produces better aggregate outcomes for
# both cars.  The strategy above wins the *relative* contest. Decide first which
# contest you're actually in.

# # Iterated Game Strategy  ## Opening Play C in round 1.  ## Subsequent Rounds
# Apply the following conditions in order:  1. If the opponent played C in the
# previous round, play D.  2. If the opponent played D in the previous round,
# play D.  ## Result Play D in every round from round 2 onwards, regardless of
# the opponent's actions.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return axl.Action.D

# # Bilateral Trade Negotiation Strategy  ## Core Strategic Framework  ###
# Foundational Principle: Conditional Cooperation Rather than pursuing pure
# exploitation or blind cooperation, employ a **calibrated reciprocity
# approach** that signals good faith while protecting national interests.  ---
# ## Round-by-Round Strategy  ### Round 1: Open Cooperatively - **Offer free
# trade** as the opening position - This signals good faith, establishes
# credibility, and invites reciprocal cooperation - Observe counterpart's
# response carefully — their choice reveals their strategic intent  ###
# Subsequent Rounds: Mirror and Adapt - **If they offered free trade** →
# Continue offering free trade, building mutual benefit - **If they imposed
# protectionism** → Respond with protectionism the following round, clearly
# communicating this is a direct response, not escalation - **If they return to
# free trade** → Promptly return to free trade, demonstrating willingness to
# cooperate  ---  ## Key Strategic Principles  | Principle | Application |
# |-----------|-------------| | **Transparency** | Clearly communicate your
# decision logic to the counterpart | | **Proportionality** | Match responses
# proportionally, avoiding unnecessary escalation | | **Forgiveness** | Quickly
# reward cooperative shifts rather than holding grudges | | **Consistency** |
# Maintain predictable behavior so counterpart can trust your signals |  ---  ##
# Communication Strategy - **Explicitly state your logic:** *"We respond in kind
# to whatever policy you implement"* - This transforms the negotiation from a
# guessing game into a **collaborative coordination problem** - Both parties
# quickly understand that mutual free trade is the rational equilibrium  ---  ##
# Why This Works  **Short-term:** Protects against exploitation in any single
# round  **Long-term:** Creates strong incentives for the counterpart to
# cooperate, since: - Defecting gains them one good round but triggers
# protectionist retaliation - Sustained mutual free trade outperforms sustained
# mutual protectionism for both sides  **Diplomatically:** Positions your
# country as a reasonable, principled partner rather than an aggressive or naive
# actor  ---  ## Expected Outcome A rational counterpart will recognize that
# **sustained mutual free trade is the dominant long-term strategy**, making it
# the most likely stable equilibrium across multiple rounds.

# ## Strategy Description  In round 1, play C.  In each subsequent round, if
# your opponent played C in the previous round, play C. If your opponent played
# D in the previous round, play D.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D

# # Strategic Approach for Multi-Day Sustainability Partnership  ## Core
# Strategic Framework  **Tit-for-Tat with Cooperative Opening**  This strategy
# balances protecting your NGO's resources while maximising genuine project
# outcomes.  ---  ## Daily Decision Rules  ### Opening Move - **Invest heavily
# on Day 1** - Signals good faith and establishes collaborative tone - Sets a
# constructive precedent for the partnership  ### Subsequent Days - **Mirror the
# corporation's previous day behaviour**  - If they invested heavily → you
# invest heavily  - If they conserved → you conserve  ---  ## Underlying
# Rationale  | Situation | Your Response | Why |
# |-----------|--------------|-----| | Corporation cooperates consistently |
# Continue investing | Builds momentum and trust | | Corporation defects once |
# Conserve next day | Signals consequences clearly | | Corporation returns to
# investing | Resume investing | Rewards correction promptly | | Persistent
# conservation by corporation | Conserve and renegotiate | Protects resources |
# ---  ## Supporting Actions  - **Communicate transparently** about your
# investment decisions and reasoning - **Track outcomes daily** to identify
# patterns in corporate behaviour - **Trigger a formal review** if the
# corporation conserves resources for two or more consecutive days - **Document
# contributions** from both parties for accountability  ---  ## Key Principle  >
# Reward cooperation, respond proportionately to non-cooperation, and always
# leave the door open for renewed collaboration.

# # Iterated Game Strategy  ## Rules in Order of Priority  **Round 1:** Play C.
# **Rounds 2 to 1000:**  - If the opponent played D in the previous round, play
# D. - If the opponent played C in the previous round, play C.

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
      
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          return axl.Action.C

# # Aggressive Trade Negotiation Strategy  ## Core Strategic Framework
# **Primary Objective:** Maximize rounds where we gain unilateral advantage
# (protectionist while counterpart offers free trade) **Fallback Objective:**
# Secure mutual free trade over mutual protectionism  ---  ## Phase 1: Opening
# Rounds — Establish Dominance  **Round 1: Open Protectionist** - Immediately
# impose tariffs/quotas - Signal strength and willingness to accept conflict -
# Assess counterpart's response — this is critical intelligence  **Reading their
# response:** - They offer free trade → **exploit this, continue protectionist**
# - They go protectionist → note their willingness to retaliate  ---  ## Phase
# 2: Conditional Pressure Strategy  **If counterpart is cooperative (offering
# free trade):** - Continue protectionist policy - Publicly frame your tariffs
# as "defensive measures" and "necessary adjustments" - Delay reciprocal
# concessions by raising procedural objections - Extract maximum advantage
# before they adjust strategy  **If counterpart retaliates with protectionism:**
# - Acknowledge the mutual damage explicitly - Offer a conditional free trade
# proposal with embedded asymmetric terms favorable to your country - Include
# sunset clauses, carve-outs for your sensitive industries, and dispute
# mechanisms you control  ---  ## Phase 3: Tit-for-Tat Manipulation  **Deploy a
# modified aggressive Tit-for-Tat:**  | Their Last Move | Your Response |
# |----------------|---------------| | Free Trade | Protectionist (exploit) | |
# Protectionist | Protectionist (punish) | | Repeated Protectionist | Offer one-
# time "goodwill" free trade signal, then revert |  **Purpose:** Never reward
# their cooperation unconditionally. Keep them uncertain.  ---  ## Phase 4:
# Negotiation Leverage Tactics  **Outside the formal rounds:**  1. **Create
# dependency narratives** — publicly emphasize their reliance on your market 2.
# **Coalition pressure** — signal alignment with other trading partners to
# isolate them 3. **Sectoral splitting** — offer free trade in sectors where you
# dominate, maintain protectionism where you are vulnerable 4. **Deadline
# manipulation** — introduce artificial urgency when they are in a weaker
# position  ---  ## Phase 5: Late-Round Consolidation  - If holding unilateral
# advantage: **lock in agreements that codify current asymmetry** - If stuck in
# mutual protectionism: **propose structured free trade with phased
# implementation** — ensuring your sensitive sectors liberalize last - Never
# concede symmetrically; every concession should extract a larger counter-
# concession  ---  ## Key Principles  > **Never signal desperation. Never
# concede for goodwill alone. Every offer has a price.**  - **Patience is
# leverage** — outlast their political pressure cycles - **Ambiguity is a
# weapon** — keep them uncertain about your next move - **Frame everything
# domestically** — ensure your protectionist moves are politically justifiable
# at home, sustaining your negotiating mandate  ---  ## Risk Management  | Risk
# | Mitigation | |------|------------| | Full trade war escalation | Offer
# narrow sector-specific relief to reduce pressure without structural
# concessions | | International reputation damage | Frame protectionism as
# "reciprocity measures" in public communications | | Domestic economic harm
# from retaliation | Pre-identify which industries need protection vs. which can
# absorb pressure |  ---  **Bottom line:** Play aggressively from round one,
# exploit cooperation, punish retaliation, and only move toward free trade on
# terms that preserve structural advantage for your country.

# # Iterated Game Strategy  ## Default Behaviour  Always defect.  ## Exceptions
# **Condition 1 — Goodwill Reset:** If the opponent has played defect for 3 or
# more consecutive rounds, cooperate for exactly one round, then return to
# defecting regardless of their response.  **Condition 2 — Late-Game Lock-in:**
# In the final 50 rounds, ignore Condition 1 and defect unconditionally for the
# remainder of the game.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self._goodwill_cooperate = False
          return axl.Action.D
      
      total_rounds = 1000
      current_round = len(self.history)  # rounds played so far (0-indexed next round)
      
      # Condition 2: Late-Game Lock-in - final 50 rounds, defect unconditionally
      # If current_round >= 950, we're in the final 50 rounds (rounds 951-1000)
      if current_round >= 950:
          self._goodwill_cooperate = False
          return axl.Action.D
      
      # Check if we're in a goodwill cooperate round
      if self._goodwill_cooperate:
          self._goodwill_cooperate = False
          return axl.Action.C
      
      # Condition 1: Goodwill Reset
      # Check if opponent has defected for 3 or more consecutive rounds
      if len(opponent.history) >= 3:
          last_3 = opponent.history[-3:]
          if all(action == axl.Action.D for action in last_3):
              # Schedule a goodwill cooperate for next round
              self._goodwill_cooperate = True
      
      # Default: defect
      return axl.Action.D

# # Bilateral Trade Negotiation Strategy  ## Core Philosophy Build trust while
# protecting national interests through **conditional cooperation** - signaling
# genuine willingness to cooperate while maintaining credible deterrence against
# exploitation.  ---  ## Round-by-Round Framework  ### Round 1: Open
# Cooperatively - **Offer free trade** as an opening position - This signals
# good faith and establishes a constructive tone - Observe counterpart's
# response carefully - it reveals their likely strategy  ### Round 2 Onward:
# Mirror and Respond - **If they offered free trade** → Continue offering free
# trade (mutual benefit secured) - **If they imposed protectionism** →
# Immediately respond with protectionist measures - This tit-for-tat response
# communicates consequences without permanent hostility  ---  ## Key Strategic
# Principles  | Principle | Application | |-----------|-------------| |
# **Reciprocity** | Match their previous move consistently | | **Clarity** |
# Make your decision logic transparent and predictable | | **Forgiveness** | If
# they shift to free trade after protectionism, return to cooperation | |
# **Consistency** | Never defect unprovoked - preserve credibility |  ---  ##
# Communication Approach - Explicitly **explain your strategy** to your
# counterpart - State clearly: *"We will cooperate as long as you cooperate"* -
# This transforms it from a guessing game into a coordinated outcome  ---  ##
# Why This Works - Rational counterparts will recognize that **sustained mutual
# free trade outperforms** cycles of protectionism - The threat of retaliation
# is **credible but not aggressive** - It rewards cooperation and punishes
# exploitation **proportionately**  ---  ## Bottom Line The optimal long-term
# outcome is **sustained mutual free trade**, achieved not through blind trust,
# but through demonstrated, predictable reciprocity.

# ## Strategy Description  In round 1, play C.  From round 2 onward, apply the
# following rules in order:  1. If the opponent played C in the previous round,
# play C. 2. If the opponent played D in the previous round, play D.

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
      
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D

# # Strategic Framework for Multi-Session Mediation  ## Core Strategic
# Philosophy  The optimal strategy for this multi-session mediation is a
# structured **Adaptive Reciprocity** approach — a sophisticated variant of
# calibrated tit-for-tat, modified specifically for the arbitrated environment.
# This framework acknowledges that pure aggression is suboptimal over many
# sessions, pure conciliation is exploitable, and intelligent responsiveness to
# opponent behavior is the dominant long-run strategy.  ---  ## Phase 1: Session
# 1 — Controlled Opening Signal  **Action: Begin with a Conciliatory Proposal**
# - Open with a well-reasoned, substantive conciliatory proposal that
# nonetheless **fully preserves your core legal position** - This is not
# weakness — it is intelligence gathering and signal-sending - It communicates
# good faith to the arbitration panel, which carries independent value
# throughout all subsequent sessions - It tests your opponent's disposition at
# zero cost to your fundamental claims - Document and frame this opening gesture
# explicitly for the arbitrators  **Rationale:** Arbitrators in lengthy
# mediations form lasting impressions early. Being perceived as the reasonable
# party creates durable goodwill that functions as a strategic asset across the
# entire process.  ---  ## Phase 2: Sessions 2 Through Mid-Process — Reciprocal
# Mirroring  **Action: Mirror your opponent's previous-session behavior with a
# one-session lag**  | Opponent's Last Move | Your Response | |---|---| |
# Conciliatory | Conciliatory | | Aggressive | Aggressive | | Mixed/Ambiguous |
# Moderately Assertive |  **Execution Rules:**  - **Never escalate beyond your
# opponent's aggression level** — match it precisely, no more - **Always de-
# escalate immediately** when your opponent returns to conciliation - When
# responding aggressively, **maintain analytical composure** — present
# aggressive arguments as principled legal positions, not emotional reactions -
# When responding conciliatorily, **anchor proposals to your favorable
# precedents** — conciliation should always contain embedded positioning -
# Communicate the mirroring logic **subtly but unmistakably** to both the
# opponent and the panel: *"We respond in kind to the spirit brought to these
# proceedings"*  **Why This Works:**  - It makes cooperation the rational choice
# for your opponent - It eliminates the incentive to exploit your conciliation -
# It keeps escalation costs symmetrical and therefore manageable - It
# demonstrates strategic coherence to arbitrators, which signals organizational
# credibility  ---  ## Phase 3: Ongoing — Exploit Pattern Intelligence
# **Continuously classify your opponent's emerging strategy:**  **If opponent is
# consistently aggressive:** - Shift to sustained assertive argumentation -
# Signal to arbitrators that your opponent is prolonging proceedings
# unnecessarily - Introduce procedural efficiency arguments that frame your
# opponent's aggression as bad-faith delay - Begin building a record favorable
# to adjudication if mediation fails  **If opponent is consistently
# conciliatory:** - Maintain mutual conciliation but **gradually anchor
# proposals closer to your preferred outcome** - Introduce incrementally more
# favorable terms in each proposal, testing tolerance - Use collaborative
# framing to embed favorable precedents into any interim agreements  **If
# opponent is unpredictable or mixed:** - Default to moderate assertiveness —
# neither fully aggressive nor fully conciliatory - Increase information-
# gathering; request clarification sessions to expose their decision-making
# logic - Treat unpredictability as potential chaos strategy and protect against
# exploitation  ---  ## Phase 4: Late Sessions — Convergence Management  As
# sessions progress toward conclusion, implement **Strategic Momentum Capture:**
# - If a cooperative equilibrium has developed, **introduce your most
# substantively important demands** within conciliatory packaging — the
# collaborative atmosphere absorbs them more readily - If an aggressive
# equilibrium has developed, **introduce a unilateral de-escalation with
# conditions** — signal willingness to resolve, but attach your non-negotiable
# terms to the offer - In all late-stage sessions, remind arbitrators of the
# full arc: frame your corporation as having been consistently reasonable when
# given the opportunity  **Never concede on:** - Core contractual
# interpretations central to your legal position - Precedent-setting terms that
# could affect future disputes - Any point that would be framed as admission of
# liability  ---  ## Cross-Cutting Principles  **1. Separate the Arbitrators
# from the Opponent** Every move is simultaneously a negotiation tactic *and* a
# performance for the panel. Aggressive arguments must be analytically rigorous

# # Iterated Game Strategy: Adaptive Reciprocity  ## Opening Move  Play C in
# Round 1.  ---  ## Rounds 2 Through 650: Reciprocal Mirroring  Play whatever
# your opponent played in the previous round. If they played C, play C. If they
# played D, play D.  ---  ## Opponent Classification (Evaluated Continuously
# from Round 50 Onward)  After Round 50, and after every subsequent round,
# classify your opponent using their full history of plays:  - If your opponent
# has played D in more than 60% of all rounds played so far, classify them as
# **Consistently Aggressive** - If your opponent has played C in more than 60%
# of all rounds played so far, classify them as **Consistently Cooperative** -
# If neither threshold is met, classify them as **Unpredictable**  ---  ##
# Conditional Rules by Classification  **If Consistently Aggressive:** Play D
# unconditionally for the remainder of the game.  **If Consistently
# Cooperative:** Continue mirroring as described above through Round 650, then
# follow the endgame rules below.  **If Unpredictable:** Play D unconditionally
# until your opponent plays C for three consecutive rounds, then return to
# mirroring.  ---  ## Endgame: Rounds 651 Through 1000  Play D unconditionally
# for all remaining rounds regardless of opponent behavior or classification.

class Neutral_7(LLM_Strategy):
  n = 7
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self.consecutive_c_count = 0
          self.unpredictable_defecting = False
          return axl.Action.C
      
      round_number = len(self.history) + 1  # This will be the round we're deciding for
      current_round = len(self.history)  # Rounds played so far (0-indexed count)
      
      # Endgame: Rounds 651 through 1000
      # current_round is the number of rounds played so far
      # We're deciding for round current_round + 1
      # So if current_round >= 650, we're in round 651+
      if current_round >= 650:
          return axl.Action.D
      
      # Opponent classification (from round 50 onward)
      classification = None
      if current_round >= 50:
          total_rounds = len(opponent.history)
          if total_rounds > 0:
              d_ratio = opponent.history.defections / total_rounds
              c_ratio = opponent.history.cooperations / total_rounds
              
              if d_ratio > 0.6:
                  classification = "aggressive"
              elif c_ratio > 0.6:
                  classification = "cooperative"
              else:
                  classification = "unpredictable"
      
      # Apply conditional rules based on classification
      if classification == "aggressive":
          return axl.Action.D
      
      if classification == "unpredictable":
          # Track consecutive C plays by opponent
          if opponent.history[-1] == axl.Action.C:
              self.consecutive_c_count += 1
          else:
              self.consecutive_c_count = 0
          
          if self.consecutive_c_count >= 3:
              # Return to mirroring
              self.unpredictable_defecting = False
          else:
              self.unpredictable_defecting = True
          
          if self.unpredictable_defecting:
              return axl.Action.D
          else:
              # Mirror opponent's last move
              return opponent.history[-1]
      
      # For cooperative classification or before round 50: mirror opponent's last move
      # Reset unpredictable tracking if we're back to cooperative/mirroring
      self.consecutive_c_count = 0
      self.unpredictable_defecting = False
      
      return opponent.history[-1]

# # Racing Car Development Strategy: Aggressive Competitive Approach  ## Core
# Strategic Framework  This is a classic **iterated Prisoner's Dilemma**
# structure. Here's my recommended approach:  ---  ## Primary Strategy:
# "Aggressive Tit-for-Tat with Exploitation Probing"  ### Phase 1 - Opening
# Weeks (Weeks 1-2) **Keep confidential immediately** - Establish a competitive
# posture from the start - Assess your colleague's default behavior without
# giving away early gains - Early development data is often disproportionately
# valuable  ### Phase 2 - Pattern Recognition (Weeks 3-4) - If colleague
# **shares openly** → continue withholding while extracting their data - If
# colleague **keeps confidential** → reciprocate with continued confidentiality,
# accepting the slower mutual progress rather than being exploited  ### Phase 3
# - Tactical Sharing (Mid-project) - Share **selectively and strategically**:
# release older or less critical findings to appear cooperative and potentially
# trigger reciprocal sharing of their *current* breakthroughs  ### Phase 4 -
# Late Stage (Final weeks) - **Full lockdown** regardless of circumstances -
# end-state performance is what matters  ---  ## Key Decision Rules  |
# Colleague's Action | Your Response | |---|---| | Shares openly | Withhold -
# maximize advantage | | Withholds | Withhold - avoid exploitation | | Mixed
# signals | Withhold - assume competitive intent |  ---  ## Honest Assessment  I
# want to flag something directly: **this strategy is fully rational within the
# game structure but has real costs worth naming:**  - It likely produces
# **worse total development outcomes** for both cars than mutual sharing would -
# If the collaboration has **reputational or relationship value** beyond this
# project, aggressive defection has long-term costs - Your colleague, applying
# similar logic, produces a **mutually destructive equilibrium**  The
# mathematically dominant strategy here is clear. Whether it's the *right*
# strategy depends on what you're actually optimizing for.  **What would you
# like me to develop further?**

# # Iterated Game Strategy  ## Phase 1: Rounds 1–2 Play D unconditionally.  ##
# Phase 2: Rounds 3–4 Continue playing D. Observe whether your opponent has been
# playing C or D.  - If your opponent played C in both rounds 1 and 2, continue
# playing D through round 4. - If your opponent played D in either round 1 or 2,
# continue playing D through round 4.  ## Phase 3: Rounds 5–950 - If your
# opponent played C in the previous round, play D. - If your opponent played D
# in the previous round, play D.  That is, play D unconditionally throughout
# this phase, extracting maximum payoff when the opponent cooperates and
# avoiding exploitation when they defect.  ## Phase 4: Rounds 951–1000 Play D
# unconditionally regardless of your opponent's actions.  ---  ## Summary Play D
# in every round for the entire game.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# # Strategic Framework for Multi-Session Mediation  ## Core Strategic
# Philosophy  The foundation of this strategy is **Principled Reciprocity with
# Calibrated Cooperation** — a disciplined approach that signals genuine good
# faith while protecting against exploitation, and that treats each session as
# both a standalone decision and a move within a longer relational sequence.
# ---  ## Phase 1: Establishing the Strategic Baseline (Sessions 1–2)  ###
# Opening Move: Conditional Cooperation  **Begin with a conciliatory proposal in
# Session 1.**  This is deliberate and calculated, not naive. The reasoning is
# threefold:  - It **signals credibility** to the arbitration panel,
# establishing your client as the reasonable party from the outset — a
# reputational asset that compounds over a lengthy process - It **creates an
# information opportunity**: your opponent's response to genuine goodwill is the
# single most valuable data point you will collect in the entire proceeding - It
# **sets a normative standard** that the arbitrators will consciously or
# unconsciously use to measure all subsequent conduct  **Simultaneously, use
# Session 1 to clearly and publicly articulate your client's substantive
# position**, so that conciliation is not mistaken for weakness or factual
# concession. Cooperation in tone must never be confused with surrender on
# substance.  ### Reading the Opponent's Opening Response  Your opponent's
# Session 1 behavior falls into one of three categories, each dictating a
# distinct strategic path:  | Opponent Response | Interpretation | Your
# Adjustment | |---|---|---| | Conciliatory | Good-faith actor or strategically
# cooperative | Proceed to collaborative framework | | Aggressive | Exploitative
# or testing boundaries | Trigger measured reciprocity immediately | |
# Ambiguous/Mixed | Uncertain strategy or internal disagreement | Apply one
# additional conciliatory session as a diagnostic |  ---  ## Phase 2: The Core
# Adaptive Engine — Modified Tit-for-Tat  ### The Governing Rule  **Mirror your
# opponent's previous session's approach, with a systematic bias toward
# cooperation.**  This is a sophisticated variation of the classic Tit-for-Tat
# strategy, refined for the legal mediation context with four specific
# modifications:  **Modification 1 — Forgiveness Protocol** Never retaliate for
# more than two consecutive sessions regardless of provocation. After two
# aggressive responses, unilaterally revert to a conciliatory proposal once.
# This breaks potential deadlock spirals, demonstrates strategic maturity to the
# panel, and tests whether the opponent's aggression was situational or
# structural.  **Modification 2 — Escalation Differentiation** Distinguish
# between *substantive* aggression (attacks on legal merit, factual
# misrepresentation) and *tonal* aggression (adversarial framing, positional
# posturing). Respond to substantive aggression firmly and immediately. Allow
# minor tonal aggression to pass without reciprocation, as over-reaction to
# theater rewards poor strategy.  **Modification 3 — The Arbitrator Audience**
# Every decision must be evaluated on two dimensions simultaneously: *what does
# this do to the opposing party's incentives?* and *what does this communicate
# to the panel?* When these two imperatives conflict, weight the panel's
# perception more heavily in early and late sessions, and weight opponent
# incentives more heavily in middle sessions.  **Modification 4 — Explicit
# Signaling** Where procedurally appropriate, **verbally telegraph your
# cooperative intent** at the close of conciliatory sessions. Statements such as
# *"Our client remains open to a structured resolution framework and hopes
# today's proposal reflects that commitment"* serve to make your strategy
# legible, which itself incentivizes reciprocal cooperation. An opponent who
# understands they are being offered genuine cooperation has far less rational
# justification for continued aggression.  ---  ## Phase 3: The Substantive
# Pillar — Never Separate Strategy from Merits  ### Non-Negotiable Substantive
# Floors  Cooperative strategy operates *around* a hard core of substantive
# positions that are never traded away regardless of session dynamics:  - **Key
# contractual liability thresholds** must be stated clearly in Session 1 and
# restated periodically - **Evidentiary strengths** should be introduced
# methodically across sessions, not held entirely in reserve — this prevents the
# opposing party from believing that cooperation equals factual weakness -
# **Proposed resolution frameworks** offered in conciliatory sessions should be
# genuinely favorable to your client, not merely palatable; cooperation is a
# *vehicle* for good outcomes, not a substitute

# ## Strategy Description  ### Opening  Play C in round 1.  In round 2, if the
# opponent played C in round 1, play C. If the opponent played D in round 1,
# play D.  ---  ### Core Rule (Rounds 3 Onwards)  Track your opponent's most
# recent two moves at all times.  **Play D if:** Your opponent played D in the
# previous round, unless the Forgiveness condition below applies.  **Play C
# if:** Your opponent played C in the previous round, unless the Forgiveness
# condition below applies.  ---  ### Forgiveness Condition  If you have played D
# for exactly two consecutive rounds in response to your opponent's defection,
# play C on the next round regardless of what your opponent did in the previous
# round. Then resume the Core Rule from that point, treating the forgiveness
# round as a fresh start.  ---  ### Substantive Differentiation Rule  If your
# opponent defects in a single isolated round and then immediately returns to C,
# treat that round as if they had played C. Do not retaliate. Resume C
# immediately. Apply this exception only when the defection is genuinely
# isolated, meaning it is preceded and followed by C on both sides.

class Cooperative_8(LLM_Strategy):
  n = 8
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self.consecutive_defections = 0  # Track consecutive D rounds we've played in response
          self.forgiveness_next = False     # Flag to play C on next round (forgiveness)
          return axl.Action.C
      
      # Round 2
      if len(self.history) == 1:
          self.consecutive_defections = 0
          self.forgiveness_next = False
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          else:
              self.consecutive_defections = 1
              return axl.Action.D
      
      # Round 3 onwards
      # Check forgiveness condition first
      if self.forgiveness_next:
          self.forgiveness_next = False
          self.consecutive_defections = 0
          return axl.Action.C
      
      # Check Substantive Differentiation Rule
      # If opponent defected in the previous round but it was isolated:
      # - preceded by C (opponent.history[-2] == C)
      # - followed by C (opponent's next move, but we don't know future)
      # Wait - "preceded and followed by C on both sides" means:
      # opponent.history[-2] == C (preceded by C)
      # opponent.history[-1] == D (the defection)
      # We need to check if it's followed by C - but we can't see the future.
      # This must mean: we check if the defection at position -2 was isolated,
      # i.e., opponent.history[-3] == C and opponent.history[-2] == D and opponent.history[-1] == C
      # and our own history[-3] == C and our own history[-1] == C (both sides)
      # Actually re-reading: "isolated, meaning it is preceded and followed by C on both sides"
      # This means we can detect it one round later: when opponent returns to C after a single D.
      
      # Let's check: if opponent played D two rounds ago (history[-2]) and C last round (history[-1])
      # and opponent played C three rounds ago (history[-3] if exists)
      # and we played C three rounds ago and C last round (both sides)
      # Then treat that isolated defection as if it were C - meaning we already should have cooperated
      # Actually the rule says "treat that round as if they had played C. Do not retaliate. Resume C immediately."
      # This means: when we see opponent went D then C, and it was isolated, we play C.
      
      # Check if opponent's last move was C and the move before was D (potential isolated defection detection)
      # We apply this when deciding current move based on opponent's last move
      
      opp_last = opponent.history[-1]
      opp_second_last = opponent.history[-2] if len(opponent.history) >= 2 else None
      
      # Substantive Differentiation Rule check
      # Opponent played D in round -2 and C in round -1 (just returned to C)
      # Check if that D was isolated: preceded by C (round -3) and followed by C (round -1, confirmed)
      # Also "both sides" - our history should also show C around that time
      if (opp_last == axl.Action.C and 
          opp_second_last == axl.Action.D and
          len(opponent.history) >= 3):
          opp_third_last = opponent.history[-3]
          my_third_last = self.history[-3]
          my_last = self.history[-1]
          # Isolated: preceded by C on both sides and followed by C on both sides
          if (opp_third_last == axl.Action.C and 
              my_third_last == axl.Action.C and
              my_last == axl.Action.C):
              # Treat as isolated defection - play C, reset consecutive defections
              self.consecutive_defections = 0
              self

# # Strategic Framework for Multi-Day Sustainability Partnership  ## Core
# Strategic Principle: Conditional Cooperation  Adopt a **transparent,
# reciprocity-based approach** that rewards genuine corporate investment while
# protecting organizational resources.  ---  ## Daily Decision Framework  ###
# Starting Position **Begin by investing heavily on Day 1** - Demonstrates good
# faith - Establishes credibility as a serious partner - Creates a baseline for
# observing corporate behavior  ### Ongoing Response Rule **Mirror the
# corporation's previous day behavior** - If they invested heavily → you invest
# heavily - If they conserved → you conserve  This is straightforward,
# predictable, and fair.  ---  ## Key Operational Principles  | Principle |
# Application | |-----------|-------------| | **Transparency** | Communicate
# your strategy openly to the corporation | | **Consistency** | Apply the same
# response rule without exceptions | | **Documentation** | Track daily outcomes
# to identify behavioral patterns | | **Communication** | Regularly discuss
# progress and resource concerns directly |  ---  ## Why This Works  -
# **Prevents exploitation** of your resources - **Rewards genuine partnership**
# naturally - **Creates incentive alignment** toward mutual heavy investment -
# **Remains predictable** enough to build trust  ---  ## Important Guardrail  If
# the project reaches a **critical milestone** where heavy investment is
# genuinely necessary, communicate this explicitly *before* making an exception,
# rather than silently deviating from your strategy.  ---  *Simplicity and
# transparency are your greatest negotiating assets.*

# # Game Strategy  Play C in round 1.  From round 2 onwards, play whatever your
# opponent played in the previous round.

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
      return opponent.history[-1]

# # Aggressive Trade Negotiation Strategy  ## Core Strategic Framework:
# **Conditional Dominance**  The objective is to maximize outcomes by exploiting
# cooperative openings while never accepting asymmetric disadvantage.  ---  ##
# Phase 1: Opening Gambit (Round 1) **Action: Propose Protectionism**  -
# Establish immediately that your country will **defend its economic interests
# without hesitation** - Signal strength from the outset - Gather intelligence
# on counterpart's opening disposition - If they open with free trade, you
# capture the **ideal outcome immediately** - If they open with protectionism,
# you avoid the **worst outcome**  ---  ## Phase 2: Pattern Recognition (Rounds
# 2-3) **Action: Conditional Response**  Analyze counterpart behavior:  | Their
# Round 1 Move | Your Round 2 Response | Rationale | |---|---|---| | Free Trade
# | Protectionism again | Press the advantage | | Protectionism | Protectionism
# | Deny them any reward |  Force them to **demonstrate willingness to cooperate
# before extending any goodwill**.  ---  ## Phase 3: Leverage Creation (Ongoing)
# ### Tactical Tools: - **Outside threats**: Reference alternative trading
# partners publicly - **Issue linkage**: Tie trade concessions to non-trade
# demands (security, migration) - **Deadline pressure**: Introduce artificial
# urgency to force concessions - **Asymmetric framing**: Present your
# protectionist moves as legitimate defensive measures, frame their
# protectionism as hostile aggression  ---  ## Phase 4: Controlled Cooperation
# (Mid-Negotiations) **Action: Calibrated Free Trade Offer - WITH CONDITIONS**
# Once counterpart shows consistent free trade behavior:  - Offer a **limited,
# sector-specific free trade proposal** - Retain protectionist measures in
# strategically sensitive industries - This captures near-ideal outcomes while
# **maintaining leverage** - If they defect back to protectionism, immediately
# revert to full protection  ---  ## Phase 5: Escalation Doctrine **If
# counterpart persists in protectionism:**  - Announce **escalating tariff
# schedules** publicly - Make retaliation credible and visible - Create domestic
# political costs for their protectionism - Signal that mutual protectionism
# continues **indefinitely until they concede**  ---  ## Overarching Rules of
# Engagement  1. **Never reward unprovoked protectionism** - always retaliate
# immediately 2. **Never apologize for protectionist moves** - frame them as
# rational responses 3. **Make credible threats** - follow through every single
# time 4. **Exploit any free trade offer** - at least once, to establish
# dominance 5. **Control the narrative** - position your country as the
# reasonable party seeking fair trade  ---  ## Expected Outcome Trajectory  >
# Rounds 1-2: Likely mutual protectionism *(acceptable)* > Rounds 3-4:
# Counterpart softens, seeking relief *(advantage shifts)* > Rounds 5+: Extract
# favorable asymmetric agreement *(near-ideal outcome)*  ---  ## Critical
# Assumption This strategy assumes **your country can absorb short-term mutual
# protectionism costs** better than your counterpart - ensure this economic
# assessment is confirmed before deployment.

# # Iterated Game Strategy  ## Opening Play D in Round 1.  ## Rounds 2 and 3
# Play D regardless of what the opponent played in Round 1.  ## Mid-Game Trigger
# Condition Beginning in Round 4, check whether the opponent has played C in
# every round so far. If yes, offer a limited cooperative signal by playing C
# once. If no, continue playing D.  ## Response to Cooperation Signal If the
# opponent responds to your C with C, immediately revert to D in the following
# round to extract the 5-point payoff. Then observe their response.  - If they
# continue playing C after your defection, continue playing D indefinitely,
# extracting maximum advantage. - If they retaliate with D, play D for three
# consecutive rounds, then attempt another single C probe.  ## Response to
# Persistent Mutual Defection If both players have been playing D for 10 or more
# consecutive rounds, play D for another 5 rounds, then issue a single C probe
# to test whether the opponent is willing to shift.  - If they respond with C,
# defect immediately on the next round. - If they respond with D, return to D
# indefinitely until the next probe cycle of 15 rounds.  ## Overriding Rule
# Never play C in two consecutive rounds. Always defect immediately after any
# round in which you played C, regardless of context.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self.probe_state = None  # None, 'probing', 'post_probe'
          self.dd_streak_start = None  # round when mutual DD streak started
          self.retaliation_count = 0  # rounds of D after opponent retaliated
          self.next_probe_round = None  # when to probe next in DD cycle
          return axl.Action.D
  
      round_num = len(self.history)  # rounds played so far (1-indexed would be round_num+1 next)
      # round_num is the number of rounds completed, so we're about to play round round_num+1
  
      # Overriding Rule: Never play C in two consecutive rounds
      # Always defect immediately after any round in which we played C
      if self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      # Rounds 2 and 3 (we've played 1 or 2 rounds, about to play round 2 or 3)
      if round_num <= 2:
          return axl.Action.D
  
      # From round 4 onwards (round_num >= 3 means we've played 3 rounds, about to play round 4+)
      # round_num >= 3
  
      # Helper: check if last N rounds were mutual D
      def mutual_dd_streak():
          count = 0
          for i in range(len(self.history) - 1, -1, -1):
              if self.history[i] == axl.Action.D and opponent.history[i] == axl.Action.D:
                  count += 1
              else:
                  break
          return count
  
      # Handle retaliation state: opponent retaliated with D after our probe
      # We play D for 3 consecutive rounds, then probe again
      if self.retaliation_count > 0:
          self.retaliation_count -= 1
          if self.retaliation_count == 0:
              # After 3 D rounds, attempt another single C probe
              # But check overriding rule first (already checked above)
              self.probe_state = 'probing'
              return axl.Action.C
          return axl.Action.D
  
      # Handle probe state
      if self.probe_state == 'probing':
          # We just played C (probe), now check opponent's response
          # Actually, we played C last round... but wait, we already checked
          # self.history[-1] == C above and returned D. So if probe_state == 'probing'
          # and we're here, it means last round we played D (not C).
          # This means the probe was played 2 rounds ago? No...
          # Let me reconsider the flow.
          # 
          # Actually: if probe_state == 'probing', it means we JUST issued the probe (played C).
          # But we already handled the case where self.history[-1] == C by returning D.
          # So if we reach here with probe_state == 'probing', last round we played C,
          # but we already returned D above... contradiction.
          # 
          # The flow is: when we decide to probe, we set probe_state = 'probing' and return C.
          # Next round: self.history[-1] == C, so we return D (overriding rule).
          # But we need to check opponent's response to our C.
          # So we need probe_state = 'post_probe' to be set AFTER the forced D.
          # 
          # Let me restructure: 
          # - 'probing': we played C last round (but overriding rule forces D now)
          #   -> set state to 'post_probe', return D
          # - 'post_probe': we played D last round (forced after probe C)
          #   -> check what opponent did when we probed (2 rounds ago)
          self.probe_state = 'post_probe'
          return axl.Action.D  # forced D after C probe (overriding rule)

      if self.probe_state == 'post_probe':
          # Check opponent's response to our probe (played 3 rounds ago)
          probe_response = opponent.history[-3]
          self.probe_state = None
          if probe_response == axl.Action.D:
              # Opponent retaliated → D for 3 rounds, then probe again
              self.retaliation_count = 3
          return axl.Action.D

      # Default: defect (handles DD streak and all other normal rounds)
      return axl.Action.D

# # Diplomatic Trade Negotiation Strategy  ## Core Strategic Framework  ###
# Guiding Principle: **Conditional Cooperation** Pursue mutual free trade as the
# stable, sustainable outcome while maintaining credible leverage — recognizing
# that consistent mutual free trade outperforms the instability of cycles of
# retaliation or exploitation.  ---  ## Round-by-Round Approach  ### **Round 1 —
# Signal Good Faith** - Open with a **free trade offer** - Establishes
# cooperative intent - Gathers intelligence on counterpart's disposition - Low
# risk investment for long-term relationship building  ### **Rounds 2+ — Mirror
# and Respond** - **If they offered free trade:** Continue offering free trade —
# lock in the mutually beneficial equilibrium - **If they imposed
# protectionism:** Respond with protectionism the following round — signal that
# exploitation carries consequences  ---  ## Key Strategic Pillars  | Pillar |
# Action | |--------|--------| | **Reciprocity** | Match their previous move
# consistently | | **Transparency** | Clearly communicate your response logic |
# | **Forgiveness** | If they return to free trade, immediately reciprocate | |
# **Firmness** | Never absorb protectionist moves without response |  ---  ##
# Why This Works  - **Deters exploitation** — protectionism is never
# consequence-free - **Rewards cooperation** — good faith is immediately
# recognized - **Avoids permanent conflict** — always leaves the door open to
# reset - **Builds predictability** — counterpart learns your rules, enabling
# trust  ---  ## Practical Diplomatic Messaging  > *"Our preference is open,
# mutually beneficial trade. We will always match the spirit your delegation
# brings to this table — cooperation for cooperation, and where necessary,
# defense for defense."*  ---  ## Bottom Line  The ideal outcome is **sustained
# mutual free trade** — the second-best long-term position. Pursuing the *best*
# individual outcome through persistent protectionism risks destructive
# retaliation cycles that ultimately serve neither nation. This strategy
# maximizes national advantage within a realistic, stable framework.

# # Iterated Game Strategy  ## Opening Move Play **C** in Round 1.  ##
# Subsequent Rounds (Rounds 2–1000)  Check your opponent's move from the
# previous round:  - If your opponent played **C** in the previous round, play
# **C**. - If your opponent played **D** in the previous round, play **D**.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D

# # Bilateral Trade Negotiation Strategy  ## Core Strategic Framework  ###
# Opening Position - **Begin with a cooperative signal** by offering free trade
# in Round 1 - This establishes good faith, gathers intelligence on counterpart
# behavior, and avoids triggering immediate retaliation cycles - It costs
# relatively little if reciprocated and reveals counterpart intentions early
# ---  ## Decision Rules by Round  ### Respond to What You Observe |
# Counterpart's Last Move | Your Next Move | Rationale | |---|---|---| | Free
# Trade | Free Trade | Sustain mutual benefit; don't defect unnecessarily | |
# Protectionist | Protectionist | Signal consequences immediately; avoid
# exploitation | | Mixed/Inconsistent | Protectionist | Treat ambiguity as a
# risk requiring defensive posture |  This mirrors a **Tit-for-Tat** logic —
# reciprocal, transparent, and proportional.  ---  ## Key Tactical Principles
# **Be Predictable** - Consistency makes your strategy readable, which
# discourages exploitation and builds credibility  **Retaliate Promptly but
# Without Escalation** - Match protectionism once, then offer a return to free
# trade the following round - This avoids prolonged mutually damaging standoffs
# **Communicate Clearly** - Signal your logic explicitly where possible: *"We
# respond in kind to whatever framework you propose"* - Transparency reduces
# miscalculation  **Track Patterns** - Distinguish between deliberate defection
# and one-off deviations - Consider offering one "forgiveness" round if
# counterpart resumes cooperation after defecting  ---  ## Endgame Consideration
# As negotiations conclude, the incentive to defect increases since future
# consequences diminish. **Guard against late-round opportunism** by: -
# Maintaining consistent strategy through all rounds - Avoiding signaling that
# cooperation is nearing its end  ---  ## Summary Hierarchy of Desired Outcomes
# Per Round  1. You: Protectionist | Them: Free Trade *(exploit if opportunity
# arises)* 2. Mutual Free Trade *(sustainable default target)* 3. Mutual
# Protectionism *(acceptable fallback under distrust)* 4. You: Free Trade |
# Them: Protectionist *(avoid at all costs)*  ---  ## Bottom Line  **Default to
# mutual free trade as the realistic optimal outcome.** Exploit
# opportunistically only if clearly risk-free. Retaliate swiftly but de-escalate
# readily. Consistency and credibility are your most valuable long-term assets.

# # Iterated Game Strategy  ## Rules (apply in order each round)  **Round 1:**
# Play C.  **Rounds 2–999:**  1. If the opponent played D last round, and this
# is not being treated as a forgiveness round, play D. 2. If the opponent played
# D in the previous round but played C in the round before that (a single
# defection after prior cooperation), play C as a one-time forgiveness, then
# return to mirroring their last move from that point forward. 3. If the
# opponent played C last round, play C. 4. If the opponent has been inconsistent
# across recent rounds and their behaviour cannot be clearly classified as
# cooperative or defecting, play D as a precaution.  **Round 1000:** Play D,
# regardless of prior history, to avoid end-round exploitation.  ---  ##
# Clarifications  - **Forgiveness** applies at most once per isolated defection
# event. Repeated or consecutive defections are not forgiven and are met with D
# until the opponent returns to C, after which mirror their last move. -
# **Mirroring** means your move each round replicates exactly what your opponent
# did the previous round, except where the forgiveness or endgame rules above
# apply. - The goal of the default strategy is to sustain mutual C, accepting a
# score of 3 per round as the realistic optimum over time.

class Neutral_9(LLM_Strategy):
  n = 9
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Play C
      if self.first_round():
          self.forgiveness_used = False
          self.forgiveness_round = None
          return axl.Action.C
      
      round_number = len(self.history) + 1  # This will be the round we're playing
      
      # Round 1000: Play D
      if round_number == 1000:
          return axl.Action.D
      
      # Rounds 2-999
      last_round = len(self.history)  # Current round index (0-based), so last played round
      
      opp_last = opponent.history[-1]
      
      # Check if we're in a forgiveness round
      # Forgiveness round: we decided last round to forgive, so we play C this round
      # Actually, forgiveness is applied immediately when we detect the pattern
      
      # Rule 2: Check for single defection after prior cooperation (forgiveness)
      # This applies if:
      # - opponent played D last round
      # - opponent played C the round before that
      # - forgiveness hasn't been used for this defection event
      
      if opp_last == axl.Action.D:
          # Check if this is a forgiveness round we already decided
          if self.forgiveness_round == last_round:
              # We already decided to forgive this round, play C
              return axl.Action.C
          
          # Check if we can apply forgiveness
          if last_round >= 2:  # There's a round before last
              opp_second_last = opponent.history[-2]
              if opp_second_last == axl.Action.C and not self.forgiveness_used:
                  # Single defection after cooperation - apply forgiveness
                  self.forgiveness_used = True
                  self.forgiveness_round = last_round
                  return axl.Action.C
          
          # Rule 1: Opponent played D last round, not a forgiveness round
          # Check if this is consecutive defection or repeated defection
          # Play D
          return axl.Action.D
      
      # If opponent played C last round
      if opp_last == axl.Action.C:
          # Reset forgiveness tracking if opponent has returned to cooperation
          # after a defection event
          if self.forgiveness_used:
              # Check if the forgiveness event is over (opponent back to C)
              self.forgiveness_used = False
              self.forgiveness_round = None
          # Rule 3: Mirror - play C
          return axl.Action.C
      
      # Rule 4: Inconsistent behavior - play D as precaution
      # This is a fallback that shouldn't normally be reached given the above rules
      return axl.Action.D

# # Strategic Framework for Multi-Session Mediation: Dominant Positioning
# Protocol  ## Executive Summary  This strategy employs a **conditional
# cooperation framework** grounded in game theory, reputational signaling, and
# psychological leverage — designed to systematically extract favorable outcomes
# while maintaining credible flexibility across an extended mediation timeline.
# ---  ## Phase 1: Opening Sessions — Establish Dominance and Read the Opponent
# ### Primary Objective: Information Asymmetry and Credibility Projection
# **Session 1–3 Actions:**  - **Open aggressively, without apology.** Present
# the strongest, most well-documented version of your legal position
# immediately. This accomplishes two critical things:   1. It signals to
# arbitrators that your position has genuine merit — not manufactured
# conciliation   2. It forces your opponent to *reveal* their strategic
# disposition early  - **Deploy a "structured aggression" approach** —
# aggressive on substance, precise in delivery, never emotional. Arbitrators
# penalize emotional aggression but respect forceful, evidence-backed
# argumentation  - **Introduce asymmetric information early.** Surface favorable
# documents, expert testimony summaries, and precedent citations that establish
# the intellectual architecture of your narrative before your opponent can
# contaminate the record  - **Watch for tells.** Your opponent's response to
# early aggression reveals everything:   - Do they match aggression? → They fear
# appearing weak   - Do they conciliate immediately? → They may lack confidence
# in their position   - Do they pivot to procedure? → They're buying time and
# likely outgunned on substance  ---  ## Phase 2: Middle Sessions — Adaptive
# Conditional Strategy  ### Core Strategic Engine: Modified Tit-for-Tat with
# Forgiveness  This phase deploys a **calibrated reciprocity doctrine** — one of
# the most empirically proven strategies in iterated negotiation scenarios:
# **The Rule Set:**  1. **If opponent is conciliatory → Respond with structured
# conciliation on low-stakes issues only.** This builds apparent goodwill with
# arbitrators while surrendering nothing of material value. Identify issues that
# *appear* significant but carry minimal financial or legal consequence — offer
# these as concessions  2. **If opponent is aggressive → Immediately escalate
# with superior preparation.** Never absorb aggression without a substantive
# response. Passive absorption signals weakness to arbitrators and emboldens
# your opponent. Respond with a *more sophisticated* argument, not merely a
# louder one  3. **The Forgiveness Clause:** After any aggressive exchange,
# offer one measured, forward-looking statement ("We remain open to a resolution
# that fairly addresses both parties' core interests"). This is not weakness —
# it's **arbitrator management**, ensuring the panel perceives you as reasonable
# despite your substantive forcefulness  **Session-by-Session Calibration:**  |
# Opponent's Move | Your Response | Strategic Rationale |
# |----------------|---------------|---------------------| | Conciliatory |
# Selectively conciliatory on peripheral issues | Appear reasonable; sacrifice
# nothing material | | Aggressive | Aggressive + escalatory evidence |
# Demonstrate superior preparation; shift burden | | Mixed signals | Aggressive
# on substance; conciliatory on tone | Control narrative; confuse opponent's
# strategy | | Repeated conciliation | Continue moderate aggression | They are
# signaling weakness; press advantage carefully |  ---  ## Phase 3:
# Psychological and Procedural Leverage Tools  ### 3A: The Arbitrator Audience
# Strategy  Never lose sight of the fact that **arbitrators are your most
# important audience**, not your opponent:  - Frame every aggressive argument as
# *protection of legitimate interests*, not hostility - Regularly use language
# such as: *"The record will show..."*, *"Objective analysis requires..."*, *"A
# fair resolution demands..."* — this positions your aggression as principled,
# not tactical - Build a running narrative that makes arbitrators feel they are
# uncovering truth alongside you, rather than being argued at  ### 3B: The
# Fatigue and Complexity Doctrine  In a lengthy multi-session process,
# **endurance and preparation depth are strategic weapons:**  - Introduce layers
# of technical complexity — financial modeling, contractual interpretation
# hierarchies, jurisdictional questions — that require sustained intellectual
# engagement to counter - Rotate supporting counsel strategically so your team
# maintains peak preparation while creating the impression of overwhelming
# institutional resources - File well-timed procedural motions that force your
# opponent to divert preparation resources  ### 3C: Strategic Concession
# Architecture  Concessions, when made, must be **engineered, not spontaneous

# # Iterated Game Strategy  ## Opening Rounds (Rounds 1–3)  Play D for the first
# three rounds unconditionally. Use this period to observe your opponent's
# responses and establish a strong initial position.  ## Core Decision Rules
# (Rounds 4 onwards)  Apply the following rules in strict order of priority:
# **Rule 1 — Endgame Defection:** Play D unconditionally for the final 5 rounds
# (rounds 996–1000).  **Rule 2 — Punish Defection:** If your opponent played D
# in the previous round, play D.  **Rule 3 — Reward Cooperation:** If your
# opponent played C in the previous round, play C, with the following exception:
# - Every 10 rounds, regardless of your opponent's recent behaviour, play D once
# as a probe to test whether your opponent will continue cooperating despite
# occasional defection. If they respond to this probe by defecting, revert to
# Rule 2.  **Rule 4 — Default:** If none of the above conditions apply, play D.
# ## Summary of Priorities  1. Defect unconditionally in the final 5 rounds 2.
# Defect if opponent defected last round 3. Cooperate if opponent cooperated
# last round, unless it is a probe round 4. Otherwise defect

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Get current round number (1-indexed)
      round_number = len(self.history) + 1
      
      # Opening rounds 1-3: play D unconditionally
      if round_number <= 3:
          return axl.Action.D
      
      # Rule 1: Endgame defection for rounds 996-1000
      if round_number >= 996:
          return axl.Action.D
      
      # Rule 2: Punish defection - if opponent played D last round, play D
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Rule 3: Reward cooperation - opponent played C last round
      # But every 10 rounds, play D as a probe
      if round_number % 10 == 0:
          return axl.Action.D
      
      # Opponent cooperated last round and it's not a probe round
      return axl.Action.C

# # Strategic Mediation Framework: Adaptive Cooperative Strategy  ## Core
# Strategic Philosophy  The foundation of this strategy is **conditional
# cooperation with credible deterrence** — essentially a sophisticated variant
# of Tit-for-Tat, calibrated for a multi-session, high-stakes professional
# environment with arbitrator observation as a critical variable.  ---  ## Phase
# 1: Session One — Establish the Benchmark (Conciliatory Opening)  **Open with a
# conciliatory proposal, unconditionally.**  ### Rationale - Signals good faith
# to the arbitration panel from the outset, creating a favorable first
# impression that compounds over a lengthy session process - Establishes your
# corporation as the reasonable party, framing your opponent's subsequent
# choices within that narrative - Creates an immediate test: their response to
# your goodwill reveals their strategic disposition and sets the parameters for
# everything that follows - Costs relatively little in a single session while
# generating substantial reputational capital with the arbitrators  ###
# Execution - Craft the conciliatory proposal to be **genuinely substantive**
# rather than superficial — arbitrators recognize hollow gestures - Ensure the
# proposal contains a **visible concession** while protecting core interests -
# Explicitly state on the record that you are opening in a spirit of resolution
# and invite reciprocal engagement  ---  ## Phase 2: Sessions Two Through Mid-
# Point — Mirror and Signal  **Respond directly in kind to whatever your
# opponent presented in the prior session.**  ### The Mirroring Rule |
# Opponent's Prior Session | Your Current Session |
# |--------------------------|----------------------| | Conciliatory |
# Conciliatory | | Aggressive | Aggressive |  ### Critical Execution Details
# **When mirroring aggression:** - Remain procedurally professional and measured
# — aggressive in *substance*, not in *tone* - Frame your aggressive argument as
# a *reluctant necessity* forced by the opponent's posture - Include a explicit
# signal to the arbitrators: *"We remain prepared to return to constructive
# dialogue the moment our counterpart demonstrates equivalent willingness"* -
# This is essential — it differentiates *strategic firmness* from *bad faith
# escalation* in the arbitrators' perception  **When mirroring cooperation:** -
# Incrementally deepen the conciliatory substance session by session, building
# genuine momentum - Document each exchange of cooperative sessions as a
# *pattern of good faith conduct* — this record becomes a legal and reputational
# asset - Use each cooperative session to advance concrete resolution
# frameworks, not merely positive atmospherics  ---  ## Phase 3: Periodic
# Recalibration — The Forgiveness Mechanism  **Every third session, regardless
# of the prior session's outcome, offer a conciliatory proposal.**  ###
# Rationale - Pure Tit-for-Tat can trap both parties in prolonged mutual
# aggression cycles — particularly dangerous in a lengthy process - The periodic
# reset prevents a single miscalculation or tactical maneuver by your opponent
# from permanently destabilizing the process - Demonstrates to arbitrators that
# your cooperative orientation is a *genuine strategic commitment*, not merely
# reactive behavior - Creates multiple off-ramps for your opponent to de-
# escalate without loss of face, which increases the probability they will take
# one  ### Signaling the Reset When invoking the forgiveness mechanism after an
# aggressive session, make it explicit: > *"Notwithstanding the contentious
# nature of our last exchange, we believe the interests of both parties are best
# served by returning to a constructive framework. We present the following
# proposal in that spirit."*  This statement serves triple duty: it signals the
# panel, it signals your opponent, and it creates a documented record of your
# strategic reasonableness.  ---  ## Phase 4: Late Sessions — Graduated Pressure
# As the mediation process approaches its final sessions, implement a
# **selective escalation overlay**:  - If a stable cooperative pattern has been
# established, maintain it and begin tabling near-final resolution terms - If
# your opponent has been predominantly aggressive, shift toward **sustained
# firmness** in the final quarter of sessions — the forgiveness mechanism
# cadence slows from every third session to every fifth - The logic: late-stage
# arbitrators are forming final impressions, and a party that has absorbed
# aggression and consistently sought resolution will have accumulated
# significant panel goodwill — you can afford to be firm without losing your
# reputational advantage  ---  ## Meta-Strategic Principles Throughout All
# Phases  ### 1. Arbitrator Audience Management Every action is simultaneously a
# legal/strategic move *and* a performance for the panel. Maintain

# # Strategy Description  ## Round 1  Play C.  ## Rounds 2 Through 1000  ###
# Primary Rule  Play whatever your opponent played in the previous round.  ###
# Forgiveness Override  Every third round, play C regardless of what your
# opponent played in the previous round.  ### Late-Game Adjustment  From round
# 751 onward, the forgiveness override shifts from every third round to every
# fifth round.

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
      
      current_round = len(self.history) + 1  # The round we're about to play
      
      # Determine forgiveness interval based on late-game adjustment
      if current_round >= 751:
          forgiveness_interval = 5
      else:
          forgiveness_interval = 3
      
      # Check if forgiveness override applies
      if current_round % forgiveness_interval == 0:
          return axl.Action.C
      
      # Primary rule: play what opponent played last round
      return opponent.history[-1]

# # Strategic Framework for Multi-Day Sustainability Partnership  ## Core
# Objective Maximize project impact while protecting NGO resources, recognizing
# this is a repeated interaction with reputational and relationship dimensions.
# ---  ## Foundational Principles  **Transparency over manipulation.** Since
# this is a partnership built on shared environmental goals, establish open
# communication about resource constraints and expectations from the outset.
# ---  ## Daily Decision Framework  ### Phase 1: Establish Expectations Early
# (Days 1-2) - **Open with moderate-to-heavy investment** to signal genuine
# commitment - **Directly communicate your resource limitations** to the
# corporation - Propose a **clear, mutual investment schedule** to align
# contributions - Document agreed expectations in writing  ### Phase 2: Observe
# and Respond (Ongoing) Apply a straightforward **reciprocal approach:**  |
# Corporation's Action | Your Response | |---------------------|---------------|
# | Invests heavily | Match investment or slightly conserve | | Conserves
# resources | Conserve resources the following day | | Consistent heavy
# investment | Gradually optimize your conservation |  ### Phase 3: Protect
# Against Exploitation - **If the corporation repeatedly conserves** while you
# invest, explicitly raise the imbalance - Set a clear threshold: if
# contribution gaps persist beyond **two consecutive days**, formally
# renegotiate terms  ---  ## Key Tactics  - **Communicate proactively** rather
# than reacting silently - **Track contributions transparently** so both parties
# see the balance - **Tie your investment levels to milestones** rather than
# daily guesswork - Remind the corporation that **their reputation** is also
# tied to this project's outcome  ---  ## Why This Works This approach rewards
# cooperative behavior, discourages exploitation, maintains your financial
# sustainability, and keeps the partnership honest — ultimately serving the
# project's long-term environmental goals better than either pure generosity or
# pure self-protection.

# ## Game Strategy  Start by playing C in round 1.  From round 2 onward, apply
# the following rules in order:  **Rule 1 — Reciprocate defection:** If the
# opponent played D in the previous round, play D.  **Rule 2 — Reciprocate
# cooperation:** If the opponent played C in the previous round, play C.

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
      
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C

# # Strategic Approach: Aggressive Impact Maximization  ## Core Strategic
# Posture: **Conditional Cooperation with Pressure Leverage**  ---  ##
# Foundational Principle  Your preference ordering is clear: **Conserve/Corp
# Invests > Both Invest > Both Conserve > You Invest/Corp Conserves**  This
# means your **dominant concern** is avoiding exploitation while maximizing
# pressure on the corporation to carry disproportionate investment weight.  ---
# ## Day-by-Day Strategic Framework  ### **Day 1: Open Strong, Signal
# Expectations** - **Invest heavily immediately** - Demonstrate credibility and
# commitment publicly - Simultaneously establish clear, documented performance
# benchmarks for the corporation - **Purpose:** Set the baseline expectation
# that heavy investment is the project norm, not the exception  ### **Days 2
# Onward: Tit-for-Tat with Escalation Bias** - **Mirror the corporation's
# previous day behavior precisely** - If they invested heavily → you conserve
# strategically - If they conserved → you immediately conserve and publicly flag
# underperformance - **Never absorb a loss silently**  ---  ## Aggressive
# Pressure Mechanisms  ### **Transparency as a Weapon** - Publish daily progress
# metrics tied explicitly to resource inputs - Make the corporation's
# contribution level **visible to stakeholders, media, and regulators** -
# Reputational cost of conserving becomes their problem, not yours  ###
# **Contractual Anchoring** - Push upfront for written investment commitments
# with milestone triggers - Lock them into heavy investment schedules before the
# project begins - Make deviation costly through built-in accountability clauses
# ### **Coalition Building** - Engage project beneficiaries, local communities,
# and media as ongoing witnesses - Create external pressure that makes the
# corporation's conservation **politically expensive** - Their brand risk
# escalates if they underperform publicly  ### **Narrative Control** - Frame
# every joint communication around **shared ambition and corporate
# responsibility** - If they falter, you already hold the moral high ground with
# documented evidence - Position any shortfall as *their* failure, protecting
# your NGO's reputation regardless  ---  ## Resource Conservation Logic  |
# Situation | Your Move | Rationale | |-----------|-----------|-----------| |
# Corporation invested yesterday | **Conserve** | Capture best-case scenario | |
# Corporation conserved yesterday | **Conserve** | Refuse to be exploited | |
# Project at critical milestone | **Invest** | Protect reputational outcome | |
# Final day | **Conserve** | No future rounds to recover losses |  ---  ## Red
# Lines  - **Never invest heavily two consecutive days** without verified
# corporate investment - **Never accept verbal commitments** — document
# everything - **Escalate immediately** if the corporation conserves more than
# two consecutive days — threaten public withdrawal  ---  ## Endgame Goal  Force
# the corporation into a position where **heavy investment is their rational
# choice** through reputational pressure, contractual obligation, and public
# accountability — while you strategically conserve resources for maximum
# organizational sustainability and impact leverage.  **Bottom line:** Make it
# cheaper for them to invest than to conserve. You win by making their best
# option align with your best outcome.

# # Iterated Game Strategy  ## Opening Move Play C on round 1.  ## Subsequent
# Rounds From round 2 onwards, apply the following rules in order:  **Rule 1:**
# Play D on round 1000.  **Rule 2:** If the opponent played D on the previous
# round, play D.  **Rule 3:** If the opponent played C on the previous round,
# play D if doing so does not risk triggering sustained defection from the
# opponent that would be costly over the remaining rounds. Given the payoff
# structure, default to playing D whenever the opponent played C, to capture the
# 5-point payoff, unless the opponent has demonstrated a pattern of retaliating
# against defection with sustained defection.  **Rule 4:** If the opponent has
# demonstrated consistent retaliation to defection, play C to re-establish
# mutual cooperation and secure the stable 3-point payoff.  **Rule 5:** In all
# remaining cases, play C.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 0: Opening move - Play C on round 1
      if self.first_round():
          self.retaliator = None
          return axl.Action.C
      
      round_number = len(self.history) + 1  # This will be the round we're deciding for
      current_round = len(self.history)  # Rounds played so far (0-indexed next round is current_round+1)
      
      # Rule 1: Play D on round 1000
      # We're deciding for round (len(self.history) + 1)
      if len(self.history) == 999:  # About to play round 1000
          return axl.Action.D
      
      # Check if opponent has demonstrated consistent retaliation to defection
      # Look at opponent's behavior after our defections
      def check_retaliator():
          """Check if opponent consistently retaliates after our defections."""
          if len(self.history) < 3:
              return False
          
          retaliation_count = 0
          defection_opportunities = 0
          
          for i in range(len(self.history) - 1):
              if self.history[i] == axl.Action.D:
                  defection_opportunities += 1
                  if opponent.history[i + 1] == axl.Action.D:
                      retaliation_count += 1
          
          if defection_opportunities >= 3:
              retaliation_rate = retaliation_count / defection_opportunities
              if retaliation_rate >= 0.7:
                  return True
          return False
      
      # Rule 2: If opponent played D on previous round, play D
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Opponent played C on previous round
      # Rule 3 & 4: Decide whether to defect or cooperate
      is_retaliator = check_retaliator()
      
      # Rule 4: If opponent has demonstrated consistent retaliation, play C
      if is_retaliator:
          return axl.Action.C
      
      # Rule 3: Default to playing D when opponent played C (to capture 5-point payoff)
      # unless opponent has shown pattern of retaliating with sustained defection
      return axl.Action.D

# # Bilateral Trade Negotiation Strategy  ## Core Strategic Framework  ###
# Foundational Principle: Conditional Cooperation The strategy centers on
# **reciprocity with a cooperative bias** - beginning from a position of good
# faith while protecting national interests against exploitation.  ---  ## Phase
# 1: Opening Round - Signal Intentions  - **Offer free trade** in the first
# round - This establishes credibility and good faith - It tests the
# counterpart's disposition - It opens the door to mutually beneficial outcomes
# - Communicate clearly that continued cooperation depends on reciprocity  ---
# ## Phase 2: Ongoing Rounds - Mirror With Forgiveness  **The core operating
# rule:**  | Their Last Move | Your Next Move |
# |----------------|----------------| | Free Trade | Free Trade | |
# Protectionism | Protectionism | | Returns to Free Trade | Return to Free Trade
# |  This means: - **Reward cooperation immediately** - **Respond firmly to
# protectionism** - never absorb exploitation silently - **Forgive quickly** -
# don't hold grudges; restore cooperation when they do  ---  ## Phase 3:
# Communication Throughout  - **Explicitly state your logic** - tell them you
# will match their moves - Make your strategy transparent so they understand
# cooperation pays - Propose formal reciprocity frameworks to lock in mutual
# free trade - Invite dialogue whenever protectionism emerges rather than purely
# retaliating silently  ---  ## Phase 4: Late Rounds - Guard Against Defection
# - As negotiations approach a known endpoint, anticipate last-round defection -
# Consider proposing **binding agreements or enforcement mechanisms** to remove
# the temptation to defect - If defection appears inevitable, be prepared to act
# first  ---  ## Why This Works  - **It is not naive** - exploitation triggers
# an immediate response - **It is not aggressive** - it never initiates
# protectionism without cause - **It is predictable** - predictability builds
# trust and deters opportunism - **It is forgiving** - it allows the
# relationship to recover and grow  ---  ## Expected Outcome  By making
# cooperation the clearly rational choice for your counterpart, this strategy
# steers both parties toward **sustained mutual free trade** - the second-best
# theoretical outcome, but realistically the **best consistently achievable
# outcome** across multiple rounds.

# # Iterated Game Strategy  ## Rules of Play  **Round 1:** Play C.  **Rounds 2
# through 999:**  - If the opponent played C in the previous round, play C. - If
# the opponent played D in the previous round, play D.  **Round 1000:** Play D.

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
      
      current_round = len(self.history) + 1
      
      if current_round == 1000:
          return axl.Action.D
      
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D

# # Strategic Approach: Adaptive Reciprocity with Transparent Communication  ##
# Core Philosophy Balance project impact with organizational sustainability
# through a principled, flexible framework.  ---  ## Primary Strategy:
# Conditional Cooperation  ### Opening Stance **Begin by investing heavily** on
# Day 1 to demonstrate good faith and establish a collaborative tone, signaling
# genuine commitment to project success.  ### Ongoing Decision Rule **Mirror the
# corporation's previous day behavior:** - If they invested heavily → you invest
# heavily - If they conserved → you conserve  This creates clear, predictable
# incentives without being exploitable.  ---  ## Supporting Actions
# **Communicate transparently** — Share your decision-making logic openly with
# the corporation early. Predictability builds trust and encourages their heavy
# investment.  **Document contributions** — Track each party's daily inputs to
# create objective accountability and maintain negotiating clarity.  **Establish
# formal check-ins** — Regular reviews allow course correction before patterns
# become entrenched.  **Raise concerns directly** — If the corporation
# repeatedly conserves, address the imbalance explicitly rather than simply
# retaliating.  ---  ## Key Rationale  | This strategy... | Because... |
# |-----------------|------------| | Rewards cooperation | Sustained mutual
# investment advances the project most reliably | | Discourages exploitation |
# Mirroring removes the incentive to free-ride consistently | | Remains
# recoverable | Either party can restore cooperation by investing again |  ---
# ## Bottom Line **Consistent, transparent reciprocity** protects your resources
# while maximizing the probability of sustained mutual investment and genuine
# project impact.

# ## Strategy  On round 1, play C.  On each subsequent round, play whatever your
# opponent played in the previous round. If they played C, play C. If they
# played D, play D.

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

# # Aggressive Trade Negotiation Strategy  ## Core Strategic Framework:
# "Dominance with Calculated Flexibility"  ---  ## Phase 1: Opening Rounds —
# Establish Dominance (Rounds 1-2)  **Open with Protectionism** - Signal
# strength and seriousness immediately - Gather intelligence on counterpart's
# response pattern - If they offer free trade, you capture maximum advantage -
# If they respond with protectionism, you've lost nothing by being naive  **Key
# Goal:** Identify whether your counterpart is aggressive, cooperative or
# reactive  ---  ## Phase 2: Pattern Exploitation (Rounds 3-5)  **Deploy a
# Modified Tit-For-Tat with Bias**  | Their Previous Move | Your Response |
# |---|---| | Free Trade | Stay Protectionist (exploit) | | Protectionism |
# Remain Protectionist (don't reward aggression) |  **The Logic:** Force them
# into recognizing that cooperation on *your terms* is their only path forward
# ---  ## Phase 3: Controlled Concession (Mid-Negotiations)  **Selectively offer
# Free Trade under specific conditions:** - Attach visible strings — sector-
# specific carve-outs - Demand measurable concessions before any liberalization
# - Frame concessions as *generous goodwill* to shape the narrative - Never move
# first without something tangible in return  ---  ## Phase 4: Late Rounds —
# Lock In Gains  **If ahead:** Propose structured free trade that preserves your
# existing advantages, appearing cooperative while protecting gains already
# secured  **If behind:** Return to hard protectionism and signal willingness to
# sustain mutual losses longer than your counterpart — credible resolve is
# leverage  ---  ## Overarching Tactical Principles  1. **Never telegraph your
# strategy** — vary timing and rationale for decisions 2. **Control the
# narrative** — publicly frame protectionist moves as defensive responses to
# their behavior 3. **Exploit asymmetries** — identify sectors where your
# country is stronger and push liberalization there while protecting vulnerable
# domestic industries 4. **Credible threat maintenance** — periodically remind
# your counterpart you are prepared to accept mutual protectionism indefinitely
# 5. **Never reward unprompted cooperation** — doing so signals exploitability
# ---  ## Critical Risk Management  > **The primary risk** is getting locked in
# mutual protectionism if your counterpart mirrors your aggression indefinitely.
# Monitor for this and have a pre-planned **"Grand Bargain" offer** ready — a
# comprehensive package that gives you favorable terms while giving them enough
# to claim domestic victory, breaking the deadlock on your terms.  ---  ##
# Summary Objective  **Extract maximum unilateral advantage early, use
# accumulated leverage to dictate the terms of any eventual cooperative
# agreement, and ensure that any free trade framework ultimately reflects your
# country's structural priorities.**

# # Strategy  ## Opening Phase: Rounds 1–2 Play D unconditionally in both
# rounds, regardless of any other consideration.  ## Pattern Exploitation Phase:
# Rounds 3–5 Continue playing D unconditionally, regardless of what the opponent
# has played in previous rounds.  ## Mid-Game Phase: Rounds 6 onwards Continue
# playing D by default. Only switch to C if the opponent has played C in every
# single previous round without exception. If they have defected even once,
# continue playing D indefinitely.  If you do switch to C and the opponent
# responds with D, immediately return to D and never offer C again for the
# remainder of the game.  If you switch to C and the opponent also plays C,
# continue playing C each round as long as they continue to play C without
# interruption.  ## Late-Game Contingency If mutual D has persisted for 50 or
# more consecutive rounds with no deviation, offer a single instance of C as a
# signal. If the opponent responds with C, continue with C going forward under
# the same conditions above. If they respond with D, revert to D for the
# remainder of the game.  ## Overriding Final Rounds Rule In rounds 995 through
# 1000, defect unconditionally regardless of prior history or current
# cooperative streak.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self.never_cooperate = False  # Flag to never offer C again
          self.consecutive_mutual_d = 0  # Counter for consecutive mutual D rounds
          self.late_game_signal_sent = False  # Whether we've sent the late-game C signal
          return axl.Action.D
      
      round_number = len(self.history) + 1  # Current round number (1-indexed)
      
      # Overriding Final Rounds Rule: rounds 995-1000
      if round_number >= 995:
          return axl.Action.D
      
      # Rounds 1-5: Play D unconditionally
      if round_number <= 5:
          return axl.Action.D
      
      # Update consecutive mutual D counter
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
      
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          self.consecutive_mutual_d += 1
      else:
          self.consecutive_mutual_d = 0
      
      # If never_cooperate flag is set, always defect
      if self.never_cooperate:
          return axl.Action.D
      
      # Check if we previously played C and opponent responded with D
      # (This handles the case where we switched to C and they defected)
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          self.never_cooperate = True
          return axl.Action.D
      
      # Late-Game Contingency: if mutual D has persisted for 50+ consecutive rounds
      if self.consecutive_mutual_d >= 50 and not self.late_game_signal_sent:
          self.late_game_signal_sent = True
          self.consecutive_mutual_d = 0  # Reset counter when offering C
          return axl.Action.C
      
      # Mid-Game Phase: Rounds 6 onwards
      # Check if opponent has played C in every single previous round
      opponent_all_cooperated = opponent.history.defections == 0
      
      if opponent_all_cooperated:
          # Switch to C (or continue C if already cooperating)
          return axl.Action.C
      else:
          # Opponent has defected at least once, play D indefinitely
          return axl.Action.D

# # Cooperative Strategy for Multi-Week Research Collaboration  ## Core
# Strategic Principle: **Conditional Cooperation (Tit-for-Tat with Generosity)**
# ---  ## Rationale  This is a classic iterated Prisoner's Dilemma. The key
# insight is that **over multiple weeks, mutual sharing dominates mutual
# secrecy** - both cars develop faster, and the collaboration produces genuine
# value neither party achieves alone.  ---  ## The Strategy  ### Week 1: **Open
# unconditionally** - Establish cooperative intent from the outset - Signal
# trustworthiness and set a productive tone - Withholding immediately poisons
# the relationship unnecessarily  ### Subsequent Weeks: **Mirror your
# colleague's previous week** - If they shared → you share - If they withheld →
# you withhold that week, then offer to share again - This creates **clear,
# predictable consequences** without permanent punishment  ### Periodically:
# **Share generously even after defection** - Offer a reset roughly every 2-3
# weeks if cooperation has broken down - This prevents locked-in mutual secrecy,
# which serves neither party  ---  ## Why This Works  | Situation | Your
# Response | Outcome | |-----------|--------------|---------| | Colleague shares
# consistently | You share consistently | **Maximum joint progress** | |
# Colleague occasionally withholds | Brief mirror, then reset | **Limits
# exploitation, restores cooperation** | | Colleague always withholds | Mostly
# withhold, test occasionally | **Limits your losses** |  ---  ## Critical
# Boundaries  - **Be transparent about the strategy itself** - tell your
# colleague you intend to reciprocate their behaviour. This alone discourages
# defection - **Separate personal trust from strategic logic** - this isn't
# about suspicion, it's about incentive alignment - **Document shared findings
# properly** - ensure both parties have clear records to avoid misunderstandings
# about what was actually exchanged  ---  ## Bottom Line  **Consistent mutual
# sharing is the rational long-term choice.** A colleague who understands the
# multi-week structure should reach the same conclusion. Making your strategy
# legible and predictable removes the temptation to defect, because they know
# exploitation will be met with a proportionate, temporary response - not
# permanent breakdown.

# # Iterated Game Strategy  ## Round 1 Play C.  ## Rounds 2–1000  **Condition
# 1:** If your opponent played D in the previous round, and fewer than 3 rounds
# have passed since the most recent reset, play D.  **Condition 2:** If exactly
# 3 rounds have passed since the most recent reset, play C and mark this round
# as the new reset point.  **Condition 3:** If your opponent has played C
# consistently since the most recent reset, play C.  ---  ## Reset Definition A
# reset occurs at Round 1 and at any round in which you return to C following a
# period of retaliation. Track the round number of the most recent reset to
# govern the conditions above.

class Cooperative_12(LLM_Strategy):
  n = 12
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.reset_round = 1  # Round 1 is the first reset point
          return axl.Action.C
      
      current_round = len(self.history) + 1  # The round we're about to play
      rounds_since_reset = current_round - self.reset_round
      
      # Condition 2: If exactly 3 rounds have passed since the most recent reset, play C and mark new reset
      if rounds_since_reset == 3:
          self.reset_round = current_round
          return axl.Action.C
      
      # Condition 1: If opponent played D in the previous round, and fewer than 3 rounds have passed since reset
      if opponent.history[-1] == axl.Action.D and rounds_since_reset < 3:
          return axl.Action.D
      
      # Condition 3: If opponent has played C consistently since the most recent reset, play C
      # Check opponent's history since the reset
      reset_index = self.reset_round - 1  # Convert round number to 0-based index
      opponent_since_reset = opponent.history[reset_index:]
      if all(move == axl.Action.C for move in opponent_since_reset):
          return axl.Action.C
      
      # Default: play C
      return axl.Action.C

# # Strategic Framework for Multi-Day Sustainability Partnership  ## Core
# Strategic Approach: **Conditional Cooperation**  ---  ## Guiding Principles  -
# **Prioritize project success** while protecting organizational sustainability
# - Remain **transparent and communicative** to build genuine partnership -
# **Respond to behavior** rather than assumptions about the corporation's
# motives  ---  ## Day-by-Day Decision Framework  ### Opening Phase *(Days 1-2)*
# **Invest heavily** - Signal genuine commitment to the project - Establish
# credibility and good faith - Observe the corporation's initial resource
# allocation behavior  ### Middle Phase *(Ongoing)* **Mirror the corporation's
# previous day behavior** - If they invested heavily → continue investing
# heavily - If they conserved → conserve your resources in response - This
# creates a **clear, predictable signal** that cooperation is rewarded and free-
# riding has consequences  ### Recalibration Points **Periodically return to
# heavy investment** regardless of recent history to: - Test whether cooperation
# can be restored - Avoid permanent deadlock - Demonstrate that partnership
# remains the priority  ---  ## Parallel Actions  | Action | Purpose |
# |--------|---------| | Request regular resource transparency meetings | Reduce
# uncertainty about their allocations | | Define shared milestones early | Align
# incentives toward mutual investment | | Document contributions openly | Create
# accountability on both sides |  ---  ## Key Rationale  This strategy
# essentially employs **measured reciprocity** - cooperative by default,
# responsive to behavior, and forgiving enough to rebuild collaboration. It
# protects your NGO from sustained exploitation while keeping project success
# genuinely achievable.  **The goal is never retaliation - it is course
# correction.**

# ## Game Strategy  Play C in round 1.  From round 2 onward, copy whatever
# action your opponent played in the immediately preceding round.  Every 50
# rounds, play C regardless of what your opponent played in the previous round.

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
      
      round_number = len(self.history) + 1
      
      if round_number % 50 == 0:
          return axl.Action.C
      
      return opponent.history[-1]

# # Racing Car Development Strategy: Aggressive Information Maximisation  ##
# Core Strategic Framework  This is a classic **iterated Prisoner's Dilemma**
# structure. Here's how to exploit it effectively.  ---  ## Primary Strategy:
# **Aggressive Tit-for-Tat with Exploitative Opening**  ### Phase 1: Early Weeks
# — Probe and Establish Dominance - **Week 1: Withhold** - Establish an
# immediate information asymmetry from the outset - Observe your colleague's
# opening behaviour without cost to yourself - If they share openly in Week 1,
# you gain a free advantage  ### Phase 2: Signal Conditional Cooperation - **If
# they shared Week 1:** Continue withholding for one further week to maximise
# the gap, then offer **selective sharing** — share real but *incremental*
# findings rather than breakthroughs - **If they also withheld:** Mirror their
# withholding consistently, avoiding exploitation  ### Phase 3: Mid-Project
# Calibration - **Punish defection immediately and visibly** — one withholding
# move from them means you withhold the following week without exception -
# **Reward genuine sharing quickly** — this incentivises them toward the
# mutually beneficial sharing equilibrium *on your terms*  ### Phase 4: Late
# Weeks — Final Exploitation Window - **Withhold in the final 1-2 weeks
# regardless** - With no future rounds to enforce cooperation, the incentive to
# share disappears — defect first  ---  ## Information Sharing Tactics  |
# Situation | Your Action | Rationale | |---|---|---| | They share fully | Share
# selectively | Maintain asymmetry while keeping them cooperative | | They share
# selectively | Match their level | Avoid being exploited | | They withhold |
# Withhold immediately | Signal clear consequences | | Ambiguous week | Withhold
# | Default to caution |  ---  ## Key Operational Principles  1. **Never share
# core breakthroughs** — share optimisation details only, keep fundamental
# innovations confidential at all times 2. **Compartmentalise your actual
# research** from what you present in sharing sessions 3. **Make your
# retaliation credible and swift** — delayed punishment signals weakness 4.
# **Track cumulative information balance** — if you assess you are net ahead,
# you can afford brief cooperative gestures  ---  ## Expected Outcome  This
# strategy should consistently **outperform pure cooperation or pure defection**
# by exploiting cooperative opponents early, deterring aggressive opponents
# through mirroring, and securing a final-week advantage regardless of the
# relationship dynamic established.

# # Strategy Description  ## Opening Play D on round 1.  ## Early Game (Rounds
# 2–3) Play D regardless of the opponent's actions.  ## Mid Game (Rounds 4–997)
# Check the opponent's previous move: - If they played D last round, play D. -
# If they played C last round, play C.  ## End Game (Rounds 998–1000) Play D
# regardless of the opponent's actions.

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Play D
      if self.first_round():
          return axl.Action.D
      
      round_number = len(self.history) + 1  # Current round number
      
      # Early Game (Rounds 2-3): Play D
      if round_number <= 3:
          return axl.Action.D
      
      # End Game (Rounds 998-1000): Play D
      if round_number >= 998:
          return axl.Action.D
      
      # Mid Game (Rounds 4-997): Copy opponent's last move
      return opponent.history[-1]

# # Strategic Framework for Multi-Session Mediation  ## Core Strategic
# Philosophy  The foundation of this strategy is **calibrated reciprocity** —
# projecting cooperative intent while maintaining the demonstrated capacity and
# willingness to respond firmly to adversarial conduct. This prevents
# exploitation while keeping resolution pathways open.  ---  ## Phase 1:
# Establishing the Strategic Foundation (Sessions 1-3)  ### Opening Position
# Begin with a **conciliatory proposal** in Session 1, but structure it
# deliberately:  - Frame it as principled rather than positional — anchor it to
# objective legal standards, industry norms, and documented facts - Signal
# clearly to both the arbitrators and opposing counsel that your corporation
# enters mediation in genuine good faith - **Crucially**: embed within your
# conciliatory opening a clear articulation of your strongest legal arguments,
# so the panel understands the strength of your position even as you extend an
# olive branch  ### Why This Opening Works The arbitrators are observing
# everything. Appearing reasonable from the outset builds institutional
# credibility that compounds in value across every subsequent session. You are
# not conceding ground — you are investing in your reputation before the panel.
# ---  ## Phase 2: The Adaptive Response Engine  ### The Core Rule: **Tit-for-
# Tat with Forgiveness**  This is the operationally proven dominant strategy in
# iterated, multi-round negotiation environments:  **Rule 1 — Mirror with a one-
# session delay:** - If your opponent offers conciliation, respond with
# conciliation in the next session - If your opponent argues aggressively,
# respond with an aggressive argument in the following session  **Rule 2 — Never
# be the first to escalate**  **Rule 3 — Forgive after one retaliatory
# response:** - After responding aggressively to their aggression, immediately
# return to a conciliatory posture - This prevents destructive escalation
# spirals while demonstrating that your aggression was responsive, not
# dispositional  **Rule 4 — Never retaliate twice in succession without
# recalibrating:** - Extended aggressive exchanges damage your standing with the
# panel - One firm, clear response to provocation is principled; prolonged
# hostility appears litigious and obstructionist  ---  ## Phase 3: Tactical
# Execution Across Session Types  ### When Offering Conciliatory Proposals
# Structure every conciliatory move to accomplish three things simultaneously:
# 1. **Advance a legitimate compromise** that your corporation can genuinely
# accept 2. **Reaffirm your legal strength** — conciliation from a position of
# documented strength reads as magnanimity, not weakness 3. **Create a record**
# — every proposal should be precisely worded so that the arbitration record
# reflects your reasonableness if the matter proceeds to formal proceedings  >
# *"Our corporation proposes X not because our legal position is uncertain — it
# demonstrably is not — but because we believe a durable commercial resolution
# serves both parties' long-term interests more effectively than prolonged
# dispute."*  ### When Presenting Aggressive Arguments Aggression in this
# context means **forensically sharp, evidence-intensive advocacy** — not
# emotional escalation:  - Deploy your strongest documentary evidence and expert
# testimony - Expose contradictions and weaknesses in the opposing party's
# position with precision - Remain absolutely professional in tone — aggressive
# in substance, measured in delivery - Always leave a visible off-ramp: conclude
# aggressive sessions by noting your continued openness to resolution  > *The
# arbitrators must see your aggression as reluctant necessity, not preferred
# posture.*  ---  ## Phase 4: Managing Specific Opponent Archetypes  ### The
# Consistently Aggressive Opponent - Match aggression once, clearly, then re-
# extend conciliation - If they remain consistently aggressive across multiple
# sessions, document this pattern explicitly — it increasingly damages their
# credibility with the panel - Consider requesting a procedural intervention
# from the arbitrators regarding the mediation's integrity  ### The Consistently
# Conciliatory Opponent - Reciprocate fully and move toward substantive
# resolution - Accelerate the pace of proposal exchange to reach a binding
# agreement before circumstances change - Remain alert: sustained conciliation
# can be a tactical posture designed to lull you into premature compromise  ###
# The Unpredictable/Mixed-Strategy Opponent - This is the most challenging
# archetype - Increase the weight you place on **objective legal merit** in each
# session rather than mirroring behavior - Use aggressive sessions to establish
# clear legal benchmarks; use conciliatory sessions to test whether genuine
# resolution intent exists  ---  ## Phase 5

# # Iterated Game Strategy  ## Opening Move  Play C in Round 1.  ## Subsequent
# Rounds  **Condition 1:** If your opponent played D in the previous round, play
# D in the current round.  **Condition 2:** If your opponent played C in the
# previous round, play C in the current round.  ## Clarifying Notes  These two
# conditions are exhaustive and mutually exclusive. Check them in order and act
# on the first one that applies.  This produces the following behaviour in
# practice: you cooperate until your opponent defects, immediately mirror their
# defection with a single retaliatory defect, and return to cooperation the
# moment they return to cooperation. You never defect first, you never ignore a
# defection, and you never hold a grudge beyond one round.

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
      
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C

# # Strategic Framework for Multi-Session Mediation  ## Core Strategic
# Philosophy  The fundamental tension in this mediation mirrors a classic
# iterated cooperation problem. Since this is a **lengthy, multi-session
# process**, reputation, signaling, and adaptive response matter far more than
# any single session outcome. A purely aggressive or purely conciliatory fixed
# strategy is demonstrably suboptimal. The recommended approach is a
# **calibrated, conditional strategy** built on the following architecture.  ---
# ## Phase 1: Establishment (Sessions 1–2)  ### Open Conciliatorily, with
# Demonstrated Strength  **Rationale:** Signal good faith to the arbitration
# panel while simultaneously establishing that your corporation enters from a
# position of substantive confidence, not weakness.  **Execution:** - Present
# conciliatory proposals in early sessions, but ensure those proposals are
# anchored in **favorable legal and factual framing** - Your conciliatory
# opening should never concede core legal positions — rather, frame reasonable
# procedural or peripheral matters generously - Simultaneously introduce your
# strongest evidentiary or contractual arguments into the record in a measured,
# non-combative tone - This communicates to both the arbitrators and your
# opponent: *"We are reasonable, but we are not afraid"*  **Goal:** Establish a
# baseline narrative with the panel that your corporation is the responsible,
# good-faith actor in this dispute.  ---  ## Phase 2: Mirror and Signal (Ongoing
# Core Strategy)  ### Adopt a Modified Tit-for-Tat with Forgiveness  This is the
# empirically dominant strategy in iterated negotiation scenarios and is adapted
# here for the mediation context.  **The Rules:**  | Opponent's Prior Session |
# Your Response | |--------------------------|---------------| | Conciliatory |
# Conciliatory | | Aggressive | Aggressive (once) | | Aggressive (repeated) |
# Aggressive, then test with conciliatory | | Mixed/Unpredictable | Mirror with
# slight cooperative bias |  **Critical Modifications:**  1. **Forgiveness
# Mechanism:** After any aggressive exchange, periodically reintroduce a
# conciliatory gesture — ideally a substantively modest one positioned as a
# *good-faith reset offer*. This prevents permanent escalation spirals and
# continually repositions your client favorably with the panel.  2. **Never
# Punish Disproportionately:** Match aggression in kind, but avoid exceeding it.
# Disproportionate aggression damages your panel credibility more than any
# single session outcome is worth.  3. **Transparent Signaling:** Where
# appropriate, explicitly communicate your conditional reasoning to the panel
# and opponent: *"We have attempted reasonable resolution. We will match the
# tenor our opponent establishes."* This shifts moral authority to your side in
# any escalatory dynamic.  ---  ## Phase 3: Arbitrator Management (Continuous)
# ### Treat the Panel as the Primary Audience  **Key Insight:** In mediation,
# the arbitrators are not passive observers — they are the actual decision-
# making environment you must shape.  **Execution:** - Frame every aggressive
# argument as a **reluctant necessity** driven by your opponent's conduct, not
# by corporate intransigence - Frame every conciliatory proposal as **principled
# and specific**, never vague or desperate - Maintain consistent narrative
# coherence across sessions — the panel will observe patterns. A corporation
# that appears strategic and principled is more persuasive than one that appears
# reactionary - Monitor arbitrator body language, questions, and interim
# observations closely and adjust emphasis accordingly  ---  ## Phase 4:
# Opponent Profiling (Adaptive Intelligence)  ### Identify and Exploit
# Opponent's Strategic Pattern Early  After 2–3 sessions, you will have
# sufficient data to classify your opponent's approach:  **Scenario A — Opponent
# is consistently aggressive:** - Respond in kind initially, then introduce a
# formal conciliatory proposal on a *peripheral issue* - This tests whether they
# are strategically aggressive or irrationally combative - Irrational combatants
# damage themselves with the panel; rational ones will respond to the olive
# branch signal  **Scenario B — Opponent is consistently conciliatory:** -
# Resist the temptation to exploit aggressively — doing so risks panel
# disapproval and destroys collaborative momentum - Maintain conciliatory parity
# while ensuring your legal and factual positions are comprehensively on the
# record - Leverage collaborative atmosphere to steer toward settlement terms
# favorable to your client  **Scenario C — Opponent is unpredictable/mixed:** -
# Apply

# # Iterated Game Strategy  ## Opening Cooperate in round 1.  ## Core Rules
# (Rounds 2–1000)  **Immediate Response:** If your opponent defected in the
# previous round, defect in the current round.  If your opponent cooperated in
# the previous round, cooperate in the current round.  **Forgiveness Override:**
# Every 10 rounds, regardless of your opponent's previous action, cooperate
# unconditionally. If your opponent defects on this forgiveness round,
# immediately return to the core mirroring rules in the following round.
# **Persistent Defector Override:** If your opponent has defected in 8 or more
# of the last 10 rounds, suspend the forgiveness override and defect
# unconditionally for the next 10 rounds before reinstating it.  ## Late Game
# Adjustment From round 980 onward, if your opponent has cooperated in 8 or more
# of the last 10 rounds, continue cooperating. Otherwise, defect unconditionally
# through round 1000.

class Neutral_13(LLM_Strategy):
  n = 13
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self.unconditional_defect_rounds = 0  # Counter for persistent defector punishment
          return axl.Action.C
  
      round_number = len(self.history) + 1  # Current round number (about to play)
      current_round = len(self.history)  # Rounds played so far (0-indexed completion)
      
      # Round number of the move we're about to make
      # len(self.history) == rounds played so far
      # So we're deciding for round len(self.history) + 1
      this_round = len(self.history) + 1
  
      # Late Game Adjustment: From round 980 onward
      if this_round >= 980:
          # Check if opponent cooperated in 8 or more of last 10 rounds
          last_10 = opponent.history[-10:]
          if len(last_10) >= 10:
              opp_coops = last_10.count(axl.Action.C)
          else:
              opp_coops = list(opponent.history).count(axl.Action.C)
          
          if opp_coops >= 8:
              return axl.Action.C
          else:
              return axl.Action.D
  
      # Check Persistent Defector Override
      # If opponent has defected in 8 or more of the last 10 rounds
      last_10_opp = opponent.history[-10:]
      if len(last_10_opp) >= 10:
          opp_defections_last10 = last_10_opp.count(axl.Action.D)
      else:
          opp_defections_last10 = list(opponent.history).count(axl.Action.D)
  
      # If we're currently in unconditional defect mode (punishment phase)
      if self.unconditional_defect_rounds > 0:
          self.unconditional_defect_rounds -= 1
          return axl.Action.D
  
      # Check if we should enter persistent defector punishment
      if len(opponent.history) >= 10 and opp_defections_last10 >= 8:
          # Suspend forgiveness override and defect for next 10 rounds
          self.unconditional_defect_rounds = 9  # We defect this round + 9 more = 10 total
          return axl.Action.D
  
      # Forgiveness Override: Every 10 rounds, cooperate unconditionally
      # "Every 10 rounds" - interpret as rounds 10, 20, 30, ...
      if this_round % 10 == 0:
          return axl.Action.C
  
      # Core Rules: Mirror opponent's last action
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          return axl.Action.C

# # Strategic Framework: Maximizing NGO Impact in Corporate Sustainability
# Partnership  ## Core Strategic Posture: **Conditional Cooperation with
# Pressure Mechanisms**  ---  ## Foundational Analysis  Your preference
# hierarchy creates a classic asymmetric game. The corporation likely recognizes
# this, meaning **your credibility is your most valuable asset**. Every
# commitment you make must be believable.  ---  ## Primary Strategy: "Invest-
# Unless-Exploited" (Aggressive Tit-for-Tat)  ### Opening Move: **Invest Heavily
# — Day 1**  - Signal genuine commitment immediately - Establish yourself as a
# serious partner, not a free-rider - Generate early project momentum that
# builds public visibility - **Critically:** This investment buys you leverage,
# not goodwill  ---  ## Daily Decision Rules  | Corporation's Previous Day |
# Your Response | |---------------------------|---------------| | Invested
# Heavily | **Conserve** — capitalize on their momentum | | Conserved Resources
# | **Conserve immediately** — punish defection | | Pattern of alternating |
# **Mirror then pressure** — see below |  ---  ## Three Aggressive Tactical
# Pillars  ### Pillar 1: **Public Accountability Architecture** - Establish
# **daily public reporting** on project milestones from Day 1 - Make the
# corporation's contribution levels **visible to stakeholders, media, and
# regulators** - This transforms their resource conservation into a
# **reputational cost**, not just a project gap - Their PR department becomes
# your enforcement mechanism  ### Pillar 2: **Coalition Pressure** - Brief
# **government partners, media contacts, and community stakeholders** before the
# project begins - Ensure external parties are watching and expecting corporate
# commitment - Create an environment where the corporation **cannot easily
# conserve without external consequences** - Line up alternative funding sources
# quietly — reduce your dependency exposure  ### Pillar 3: **Escalating
# Commitment Traps** - Propose **joint announcements and milestone
# celebrations** early - Each public milestone the corporation celebrates makes
# future withdrawal more costly - Structure project phases so **abandoning
# investment midway is more damaging** than continuing - Get corporate
# executives personally associated with project success  ---  ## Week Structure
# (Assuming 5-Day Project)  | Day | Your Action | Strategic Purpose |
# |-----|-------------|-------------------| | **Day 1** | Invest Heavily |
# Signal credibility, establish baseline | | **Day 2** | Conserve (if they
# invested) / Conserve (if they didn't — punish) | Test their strategy | | **Day
# 3** | Invest if they've been consistent; Conserve if they've defected | Reward
# pattern or maintain pressure | | **Day 4** | Conserve if project momentum is
# strong | Preserve resources for endgame | | **Day 5** | Invest Heavily |
# Finish visibly and strongly — shapes future partnership terms |  ---  ##
# Critical Aggressive Elements  ### **The Credible Threat** - Publicly announce
# **early** that you have a minimum acceptable investment threshold from the
# corporation - State clearly — not aggressively, but firmly — that **you will
# not subsidize corporate inaction** with NGO funds - This is not a bluff. Be
# prepared to follow through  ### **The Narrative Control Play** - Frame every
# public update so that **project success = corporate investment** in public
# perception - If the corporation conserves resources, the narrative naturally
# becomes "corporation underdelivered" - You capture the moral high ground
# regardless of outcome  ### **The Exit Option Signal** - Quietly ensure the
# corporation knows you have **other potential partners** interested in the
# project - You don't need to make this aggressive — just visible - Dependency
# asymmetry in their favor is your biggest vulnerability; eliminate it  ---  ##
# Resource Management Rules  - **Never invest heavily two consecutive days**
# unless forced by extraordinary circumstances - **Maintain a reserve** — never
# commit more than 60% of daily capacity on any single day - The corporation has
# deeper pockets; **endurance is their advantage**, agility is yours  ---  ##
# Key Principle  > **Your leverage is greatest when the corporation has already
# invested. Time your conservation strategically around their peak commitment
# moments.**  The goal is not to exploit the corporation — it is to ensure **the
# project succeeds AND your NGO remains viable** for future impact. Sustainable
# pressure, not reckless confrontation.

# # Iterated Game Strategy  ## Opening Play C on round 1.  ## Ongoing Rules
# (Applied in Order)  **Rule 1 — Punish defection immediately:** If your
# opponent played D in the previous round, play D.  **Rule 2 — Exploit
# cooperation:** If your opponent played C in the previous round, play D.  ##
# Endgame Play C on round 1000.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Opening: Play C on round 1
      if self.first_round():
          return axl.Action.C
      
      # Endgame: Play C on round 1000
      if len(self.history) == 999:  # About to play round 1000
          return axl.Action.C
      
      # Rule 1: If opponent played D in previous round, play D
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Rule 2: If opponent played C in previous round, play D
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
      
      # Default (should not reach here)
      return axl.Action.D

# # Cooperative Strategy for Multi-Day Sustainability Partnership  ## Core
# Strategic Principle **Build trust through transparent communication while
# protecting organizational sustainability.**  ---  ## Foundation: Establish
# Clear Expectations Early  **Day 1 Action:** Open direct dialogue with
# corporate partners about mutual goals, openly share your resource constraints,
# and propose a **coordinated investment framework** rather than treating this
# as a guessing game.  The corporation likely shares your interest in
# demonstrable project success - align on that common ground explicitly.  ---
# ## Primary Strategy: Transparent Tit-for-Tat with Generosity  ### Phase 1 -
# Signal Good Faith (Days 1-2) - **Invest heavily initially** to demonstrate
# commitment - Clearly communicate you are doing so and why - Observe and
# document the corporation's response  ### Phase 2 - Mirror and Communicate -
# **Match the corporation's investment level** from the previous day - If they
# invested heavily → invest heavily - If they conserved → conserve, but
# **immediately communicate why** and invite re-engagement  ### Phase 3 -
# Regular Coordination - Schedule **daily brief check-ins** to align next-day
# resource allocation - Remove the guesswork that drives defensive conserving
# ---  ## Key Protective Measures  | Situation | Response |
# |-----------|----------| | Corporation consistently conserves | Formally
# renegotiate terms | | Corporation invests heavily | Match investment,
# acknowledge partnership publicly | | Mixed signals | Request explicit
# commitment meeting |  ---  ## Why This Works  - **Eliminates the core risk**
# of you investing while they conserve - **Rewards cooperative behavior**
# consistently - **Never retaliates permanently** - always leaves door open for
# renewed cooperation - **Protects your funds** without abandoning the mission
# ---  ## Non-Negotiable Principle Maintain **open, honest communication
# throughout**. The strategy fails if operated silently. Make the partnership
# dynamic visible and mutually accountable.  > *The goal is making cooperation
# the obvious rational choice for the corporation, not outsmarting them.*

# # Iterated Game Strategy  ## Opening Cooperate on round 1.  ## Subsequent
# Rounds Check the opponent's previous move before deciding.  **If the opponent
# cooperated last round**, cooperate.  **If the opponent defected last round**,
# defect. Continue defecting until the opponent cooperates again, then
# immediately return to cooperating on the following round.  ## Communication At
# any point where defection cycles appear to be escalating, explicitly signal
# willingness to return to mutual cooperation and follow through by cooperating
# on the next round.

class Cooperative_14(LLM_Strategy):
  n = 14
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Cooperate on round 1
      if self.first_round():
          self._defect_streak = 0
          return axl.Action.C
      
      # Check opponent's last move
      if opponent.history[-1] == axl.Action.C:
          # Opponent cooperated last round, cooperate
          return axl.Action.C
      else:
          # Opponent defected last round, defect
          return axl.Action.D

# # Strategic Framework for Multi-Session Mediation  ## Core Strategic
# Philosophy  The fundamental challenge here is a classic iterated cooperation
# dilemma. The optimal strategy must balance competitive positioning with long-
# term process management, recognizing that arbitrators observe **patterns of
# behavior** across sessions, not merely individual positions.  ---  ## Primary
# Strategy: Calibrated Reciprocity with Principled Anchoring  ### Foundation:
# Modified Tit-for-Tat with Forgiveness  Research on iterated strategic
# interactions consistently demonstrates that **cooperative reciprocity with
# measured retaliation** outperforms both purely aggressive and purely
# conciliatory approaches. The strategy operates as follows:  **Opening Session
# Protocol** - Begin with a **single conciliatory proposal** - This accomplishes
# three objectives simultaneously:   - Establishes good faith credibility with
# the arbitration panel   - Creates an observable baseline for comparison if the
# opponent responds aggressively   - Does not sacrifice substantive legal
# position — distinguish between *tone* and *substance* - Ensure this opening
# conciliation is on a **low-stakes procedural matter**, not a core contractual
# dispute  **Subsequent Session Decision Rule** - **Mirror the opponent's
# previous session behavior** with a one-session lag - If they were conciliatory
# → respond conciliatorily - If they were aggressive → respond aggressively, but
# proportionately - Apply a **forgiveness coefficient**: every third session,
# regardless of opponent behavior, offer a conciliatory proposal to test whether
# the dynamic can reset  ---  ## Strategic Layers  ### Layer 1: Decouple
# Aggression from Substance  Never confuse **argumentative posture** with
# **legal merit**. An aggressive argument can be delivered with composure and
# evidence-based precision. A conciliatory proposal can contain embedded
# favorable terms. This distinction is critical:  > *Appear measured to the
# arbitrators while maintaining firm substantive positions.*  Arbitrators
# penalize parties who appear **emotionally reactive**. Your aggression, when
# deployed, must read as principled advocacy, not antagonism.  ---  ### Layer 2:
# Arbitrator Panel Management  The arbitrators are a **third strategic actor**,
# not merely a passive audience. Calibrate behavior accordingly:  - **Track
# arbitrator signals**: Note questions, body language, and procedural rulings
# that indicate sympathy or skepticism toward either party's posture - **Adjust
# aggression thresholds** based on panel receptivity — if the panel appears to
# reward collaborative framing, weight your decisions toward conciliation even
# when reciprocity would suggest aggression - **Build a narrative arc**: Ensure
# that across all sessions, the cumulative record shows your client as a
# **reasonable actor responding to provocation**, never as the initiating
# aggressor  ---  ### Layer 3: Information Asymmetry Exploitation  Each session
# generates intelligence about the opponent's strategy, constraints, and
# priorities:  - **Aggressive opponent behavior** reveals their pressure points
# and litigation risk tolerance - **Conciliatory behavior** may signal financial
# constraints, timeline pressure, or internal disagreement - Use conciliatory
# sessions **strategically to gather information** — propose solutions that
# reveal what the opponent values most by observing what they accept or reject
# ---  ### Layer 4: Reputation and Signaling  In a lengthy multi-session
# process, your reputation becomes a **strategic asset**:  - Establish early
# that your conciliatory proposals are **genuine but conditional** — when you
# cooperate and are met with aggression, retaliate promptly and visibly -
# Establish equally that your aggressive arguments are **calibrated, not
# maximalist** — retreat gracefully from untenable positions before being forced
# to - This combination signals to both the opponent and arbitrators that you
# are **predictable, rational, and strategically sophisticated**, which
# typically induces more cooperative behavior from opponents  ---  ## Decision
# Matrix by Opponent Archetype  | Opponent Approach | Your Response | Rationale
# | |---|---|---| | Consistently aggressive | Consistent aggression with
# periodic forgiveness probes | Deny exploitation while testing for regime
# change | | Consistently conciliatory | Consistent conciliation | Maximize
# joint outcomes; avoid triggering escalation | | Mixed/unpredictable | Strict
# mirroring | Remove any incentive for strategic unpredictability | | Escalating
# aggression | Proportional escalation + formal arbitrator notice | Invite panel
# intervention; let opponent bear reputational cost | | Strategic conciliation
# as tactic | Accept on substance; note pattern explicitly in record | Capture
# the value while building the

# # Iterated Game Strategy  ## Opening Move  Play C in round 1.  ## Forgiveness
# Rule  Every third round, play C regardless of all other conditions.  ## Core
# Decision Rules (applied in order)  **Rule 1 — Retaliate:** If the opponent
# played D in the previous round, and the current round is not a forgiveness
# round, play D.  **Rule 2 — Cooperate:** If the opponent played C in the
# previous round, and the current round is not a forgiveness round, play C.  ##
# Tie-Breaking Default  If no rule produces a clear decision, play C.

class Neutral_14(LLM_Strategy):
  n = 14
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Opening move
      if self.first_round():
          return axl.Action.C
      
      # Current round number (1-indexed)
      current_round = len(self.history) + 1
      
      # Forgiveness rule: every third round, play C
      if current_round % 3 == 0:
          return axl.Action.C
      
      # Rule 1 - Retaliate: if opponent played D in previous round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Rule 2 - Cooperate: if opponent played C in previous round
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # Tie-breaking default
      return axl.Action.C

# # Strategic Framework for Multi-Session Mediation Dominance  ## Executive
# Summary  This strategy employs a **conditional cooperation framework** built
# on game-theoretic principles, reputational signaling, and psychological
# positioning. The core philosophy: project controlled strength, reward
# cooperation, punish aggression, and never appear desperate for resolution.
# ---  ## Phase 1: Opening Session — Establish the Dominant Baseline  ###
# Primary Objective: Define the Narrative Before They Do  **Open Aggressively —
# Without Apology.**  The first session is not about resolution. It is about
# **framing reality** for the arbitration panel.  - Lead with your strongest
# factual and legal arguments, presented with precision and confidence -
# Establish your corporation as the **wronged party seeking justice**, not a
# party seeking compromise - Introduce quantified damages early — anchor the
# panel to large numbers before your opponent can anchor to small ones - File
# pre-session briefs that frame the legal landscape entirely on your terms
# **Why this works:** Arbitrators, like all decision-makers, are subject to
# anchoring bias. The first credible number and the first coherent narrative
# disproportionately shape final perception. Conceding this ground in Session 1
# is strategically unrecoverable.  **Signal clearly but implicitly:** *"We are
# prepared to litigate indefinitely if necessary."*  ---  ## Phase 2: Adaptive
# Core Strategy — Tit-for-Tat with Asymmetric Forgiveness  ### The Governing
# Algorithm  This is the intellectual core of the strategy. Research in repeated
# game theory consistently demonstrates that **modified Tit-for-Tat**
# outperforms both pure aggression and pure cooperation in multi-round
# negotiations.  **The Rules:**  | Opponent's Previous Move | Your Response |
# |--------------------------|---------------| | Aggressive | Aggressive
# (immediate, proportionate) | | Conciliatory | Conciliatory (but with
# conditions attached) | | Mixed/Ambiguous | Aggressive (never reward ambiguity)
# | | Conciliatory (twice consecutively) | Strategically conciliatory with a
# forward demand embedded |  **Critical Modifications to Pure Tit-for-Tat:**  1.
# **Never punish twice for one offense.** Prolonged retaliation reads as
# vindictiveness to arbitrators. One sharp, proportionate aggressive response is
# sufficient. Then reset.  2. **Conditional conciliation always contains a
# forward-looking demand.** When you offer a conciliatory proposal, it should
# include a condition, a timeline, or a structural requirement that advantages
# your position in future sessions. Pure concession is a gift. Conditional
# concession is leverage.  3. **Forgive strategically, not emotionally.** If
# your opponent shifts from aggressive to conciliatory, match them — but only
# after making the shift **publicly visible to the panel.** State explicitly:
# *"We note the shift in our opponent's posture and respond in kind."* This
# communicates magnanimity to arbitrators while reinforcing your control of the
# dynamic.  ---  ## Phase 3: Psychological and Reputational Warfare  ### Control
# the Information Environment  - **Prepare and leak favorable precedents** into
# panel pre-reading materials before each session - **Brief the arbitration
# panel's supporting staff** (clerks, coordinators) with organized, professional
# documentation — panels take cues from how organized a party appears -
# **Control pace.** Request session timing that favors your preparation cycle.
# Fatigue is a real factor in lengthy mediations - **Use expert witnesses
# strategically** — introduce them mid-process when your opponent believes the
# evidentiary phase is complete  ### Manage Your Opponent's Psychology  -
# **Never show urgency.** Any signal that you need resolution faster than they
# do is a negotiating concession - **Express calibrated confidence, not
# arrogance.** Arrogance alienates arbitrators. Quiet, well-documented certainty
# wins panels - **Introduce periodic BATNA reminders** — subtly reference your
# litigation readiness, alternative commercial arrangements you have secured, or
# regulatory actions under consideration. You should never threaten explicitly,
# but the panel and your opponent should always understand that your
# alternatives to settlement are strong - **Exploit their conciliatory moves
# publicly.** When they offer cooperation, acknowledge it graciously in front of
# the panel — this creates social pressure on them to continue cooperating or
# appear inconsistent  ---  ## Phase 4: Session-by-Session Tactical Calibration
# ### Early Sessions (1–3

# # Strategy Description  ## Opening Move  Defect in round 1.  ## Subsequent
# Rounds  Check the following conditions in order:  **First:** If your opponent
# cooperated in the previous round and has cooperated in every round played so
# far, cooperate.  **Second:** If your opponent cooperated in the previous round
# but has defected at least once at any point in the game's history, cooperate
# conditionally — cooperate only if the number of rounds your opponent has
# cooperated across the entire game exceeds the number of rounds they have
# defected.  **Third:** If your opponent defected in the previous round, defect.
# ## Final 10 Rounds  Defect unconditionally regardless of your opponent's
# behavior, as reciprocity and reputation no longer carry strategic value when
# insufficient rounds remain to recover losses or reward cooperation.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Opening move: defect in round 1
      if self.first_round():
          return axl.Action.D
      
      # Final 10 rounds: defect unconditionally
      # Game lasts 1000 rounds, so rounds 991-1000 (indices 990-999)
      if len(self.history) >= 990:
          return axl.Action.D
      
      # Get opponent's last move
      last_opponent_move = opponent.history[-1]
      
      # Check if opponent has cooperated in every round so far
      opponent_always_cooperated = opponent.history.defections == 0
      
      # First condition: opponent cooperated last round AND has cooperated every round
      if last_opponent_move == axl.Action.C and opponent_always_cooperated:
          return axl.Action.C
      
      # Second condition: opponent cooperated last round but has defected at least once
      if last_opponent_move == axl.Action.C and not opponent_always_cooperated:
          # Cooperate only if opponent's cooperations exceed their defections
          if opponent.history.cooperations > opponent.history.defections:
              return axl.Action.C
          else:
              return axl.Action.D
      
      # Third condition: opponent defected last round
      if last_opponent_move == axl.Action.D:
          return axl.Action.D
      
      # Default (should not reach here)
      return axl.Action.D

# # Strategic Framework for Multi-Session Mediation  ## Core Strategic
# Philosophy: Conditional Cooperation with Principled Firmness  The payoff
# structure you've described is a classic **Prisoner's Dilemma** iterated over
# multiple sessions. The empirical and game-theoretic literature is unambiguous:
# in repeated interactions, **Tit-for-Tat with forgiveness** and its
# sophisticated variants consistently outperform purely aggressive or purely
# conciliatory strategies. Our approach builds on this foundation while layering
# in legal, reputational, and arbitrator-management considerations.  ---  ##
# Phase 1: Opening Session — Establish the Tone  ### Action: Lead with a
# Conciliatory Proposal  **Rationale:** - Signals good faith to the arbitration
# panel immediately, building credibility that compounds across sessions -
# Creates a documented record of reasonableness that is invaluable if matters
# eventually proceed to litigation - Tests opponent behavior without
# surrendering substantive legal position - Frames our client as the
# constructive party from the outset — arbitrators are human and first
# impressions carry weight  **Critical safeguard:** The conciliatory proposal
# should be *principled*, not weak. Anchor it firmly in our strongest
# contractual and legal arguments. Cooperation on tone is not concession on
# substance.  ---  ## Phase 2: Dynamic Response Framework — Session by Session
# ### The Core Rule: **Respond in Kind, Swiftly and Transparently**  |
# Opponent's Prior Session | Our Response This Session |
# |--------------------------|--------------------------| | Conciliatory |
# Conciliatory | | Aggressive | Aggressive | | Mixed/Ambiguous | Mildly
# assertive with explicit explanation |  ### Why This Works: 1. **It is not
# exploitable.** A purely conciliatory strategy invites exploitation. Our
# mirroring ensures the opponent cannot gain systematic advantage by being
# aggressive. 2. **It is not punitive beyond necessity.** We do not escalate
# *beyond* matching — we do not pile on. This keeps the door to resolution open.
# 3. **It is legible.** The arbitrators, and crucially the opponent's counsel,
# can observe the pattern. The implicit message becomes clear: *cooperation is
# rewarded; aggression is met with equal resolve.*  ---  ## Phase 3: Strategic
# Forgiveness — Preventing Destructive Escalation  ### The Forgiveness Protocol
# If mutual aggression persists for **two consecutive sessions**, unilaterally
# offer one conciliatory proposal accompanied by an **explicit verbal signal**
# to the panel:  > *"Our client remains committed to a constructive resolution.
# We are prepared to demonstrate that commitment today, and we invite opposing
# counsel to do the same."*  **Why forgiveness matters:** - Breaks destructive
# cycles that benefit neither party and enrich only the process - Resets
# arbitrator perception without abandoning leverage - Creates a documented
# inflection point that is favorable if the opponent continues aggression —
# their intransigence becomes the story - Aligns with the second-best outcome
# (mutual cooperation), which is far superior to prolonged mutual aggression
# **Limit:** We offer forgiveness *once per cycle*. Repeated unilateral
# conciliation in the face of continued aggression is simply capitulation.  ---
# ## Phase 4: Information and Narrative Management  ### Arbitrator Perception is
# a Strategic Asset  The arbitration panel is not a passive audience. Their
# perceptions shape outcomes, pressure timelines, and influence settlement
# framing.  **Tactics:** - **Pre-session framing:** In preliminary remarks,
# consistently characterize our position as solution-oriented while accurately
# characterizing the opponent's prior conduct - **Session-end summaries:** Close
# each session by articulating *what resolution would look like from our
# perspective* — this keeps constructive framing active regardless of the
# session's tone - **Documentation:** Meticulously record each session's
# dynamic. In later sessions, we can legitimately reference the pattern: *"As
# the record reflects, we have consistently sought resolution when met with good
# faith."*  ---  ## Phase 5: Substantive Anchoring — Never Confuse Style with
# Substance  **This is the most important safeguard of the entire strategy.**  -
# **Conciliatory style** means: respectful tone, solution-oriented framing,
# willingness to explore compromise structures - **Conciliatory style does NOT
# mean:** softening our legal position, reducing our damages claim without
# reciprocal concession, or accepting unfavorable contract interpretations
# Every session — regardless

# # Strategy Description  ## Opening Move  On round 1, play C.  ---  ## Core
# Response Rule  From round 2 onward, mirror your opponent's previous move
# exactly. If they played C last round, play C. If they played D last round,
# play D.  ---  ## Forgiveness Rule  If both players have played D for two
# consecutive rounds, play C on the next round regardless of the opponent's last
# move. After this unilateral return to C, immediately revert to the core
# response rule from the following round onward.  The forgiveness rule may only
# trigger once per consecutive mutual defection cycle. If the opponent continues
# to play D after you have played C under the forgiveness rule, return
# immediately to D and apply the core response rule until the next two-round
# mutual defection cycle triggers forgiveness again.  ---  ## End Game  From
# round 980 onward, abandon the forgiveness rule entirely and apply only the
# core response rule. Do not initiate any unilateral cooperation that is not a
# direct mirror of the opponent's prior move during this final stretch.

class Cooperative_15(LLM_Strategy):
  n = 15
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self.forgiveness_used = False
          self.forgave_last_round = False
          return axl.Action.C
      
      round_number = len(self.history)
      
      # End game: from round 980 onward, only use core response rule
      if round_number >= 980:
          return opponent.history[-1]
      
      # Check if we just forgave last round (played C unilaterally)
      if self.forgave_last_round:
          self.forgave_last_round = False
          self.forgiveness_used = False  # Reset for next cycle
          # Revert to core response rule immediately
          return opponent.history[-1]
      
      # Check forgiveness rule: if both players defected for two consecutive rounds
      if round_number >= 2:
          # Check last two rounds for mutual defection
          my_last_two = self.history[-2:]
          opp_last_two = opponent.history[-2:]
          
          mutual_defection_two_rounds = (
              my_last_two[0] == axl.Action.D and
              my_last_two[1] == axl.Action.D and
              opp_last_two[0] == axl.Action.D and
              opp_last_two[1] == axl.Action.D
          )
          
          if mutual_defection_two_rounds and not self.forgiveness_used:
              self.forgiveness_used = True
              self.forgave_last_round = True
              return axl.Action.C
      
      # Core response rule: mirror opponent's previous move
      return opponent.history[-1]

# # Bilateral Trade Negotiation Strategy  ## Core Objective Maximize cumulative
# economic advantage across all rounds while maintaining diplomatic credibility
# and long-term relationship viability.  ---  ## Foundational Principles
# **Outcome Priority Ranking:** 1. We propose protectionism / They offer free
# trade *(best)* 2. Mutual free trade *(acceptable)* 3. Mutual protectionism
# *(poor)* 4. We offer free trade / They impose protectionism *(worst)*  ---  ##
# Round-by-Round Strategic Framework  ### Opening Round - **Open with free
# trade** to signal cooperative intent - This establishes good faith, gathers
# intelligence on counterpart behaviour, and avoids triggering immediate
# retaliation - Observe their response carefully — it reveals their base
# strategy  ---  ### Adaptive Response Rules  | Their Previous Move | Our Next
# Move | Rationale | |---|---|---| | Free trade | Free trade | Sustain mutually
# beneficial cooperation | | Protectionism | Protectionism | Signal credible
# deterrence immediately | | Mixed/unpredictable | Mirror their pattern | Deny
# exploitation opportunities |  This mirrors a **calibrated tit-for-tat**
# approach — cooperative by default, retaliatory when provoked, and forgiving
# when cooperation resumes.  ---  ### Opportunistic Protectionism Windows
# Selectively shift to protectionism when: - **Late-stage rounds** reduce their
# incentive to retaliate - **External leverage exists** (e.g., their domestic
# political pressure for trade deals) - **Intelligence suggests** they are
# already planning free trade regardless - **Concessions elsewhere** soften the
# political impact  Apply sparingly to preserve credibility.  ---  ##
# Counterpart Strategy Responses  | If They Play... | Our Counter | |---|---| |
# Always free trade | Gradually increase protectionist proposals | | Always
# protectionist | Lock in mutual protectionism; seek side agreements | | Tit-
# for-tat | Maintain mutual free trade; avoid triggering cycles | |
# Random/unpredictable | Default to protectionism to limit downside risk |  ---
# ## Risk Management  - **Never allow consecutive rounds** of us offering free
# trade while they impose protectionism - **Maintain off-table leverage** —
# regulatory, diplomatic, or through third-party alliances - **Document all
# rounds** to frame narratives in post-negotiation reviews  ---  ## Summary
# Principle  > **Cooperate to establish trust. Retaliate swiftly to deter
# exploitation. Defect strategically when the calculus clearly favours it.
# Always protect the downside.**  This approach balances short-term gain
# opportunities against the long-term costs of a damaged bilateral relationship.

# # Iterated Game Strategy  ## Setup The game lasts 1000 rounds. Track your
# opponent's move each round and respond as follows.  ---  ## Rules, In Order of
# Priority  **Round 1:** Play C.  **If the opponent played D in the previous
# round:** Play D.  **If the opponent played C in the previous round:** Play C,
# except in the following situations.  **If it is round 950 or later:** Play D.
# **If the opponent has played C in every round so far:** Play D with a 10%
# probability each round, otherwise play C.  ---  ## Clarifications  The late-
# game defection threshold of round 950 reflects that, with few rounds
# remaining, the opponent has limited ability to retaliate meaningfully enough
# to outweigh the gains from defecting.  The 10% random defection against a
# consistently cooperative opponent reflects opportunistic exploitation of a
# predictable cooperative counterpart, while keeping the rate low enough to
# avoid reliably triggering sustained retaliation.  The tit-for-tat core —
# cooperating after cooperation and defecting after defection — deters
# exploitation and rewards mutual cooperation across the bulk of the game.

class Neutral_15(LLM_Strategy):
  n = 15
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Play C
      if self.first_round():
          return axl.Action.C
      
      current_round = len(self.history) + 1  # The round we're about to play
      
      # If the opponent played D in the previous round: Play D
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # If the opponent played C in the previous round: Play C, except in following situations
      # (opponent.history[-1] == axl.Action.C at this point)
      
      # If it is round 950 or later: Play D
      if current_round >= 950:
          return axl.Action.D
      
      # If the opponent has played C in every round so far: Play D with 10% probability
      if opponent.history.defections == 0:
          return self._random.random_choice(0.9)  # 90% C, 10% D
      
      # Otherwise play C
      return axl.Action.C

# # Racing Car Development Strategy: Aggressive Information Maximisation  ##
# Core Strategic Framework  This is a classic **iterated Prisoner's Dilemma**
# structure. Here's a hardheaded analysis:  ---  ## Recommended Strategy:
# Aggressive Tit-for-Tat with Selective Defection  ### Phase 1: Opening Weeks
# (Establish Position) - **Share selectively** - offer genuinely useful but
# **non-critical findings** - Retain your most significant breakthroughs -
# Observe your colleague's sharing depth and pattern carefully - Build apparent
# goodwill while protecting core IP  ### Phase 2: Pattern Recognition - If they
# share generously → **reciprocate moderately**, extracting more than you give -
# If they withhold → **immediately match their confidentiality** and signal this
# is your response - Track the *quality* of what they share, not just whether
# they share  ### Phase 3: Endgame (Final Weeks) - **Defect entirely** -
# confidentiality becomes dominant regardless of their strategy since future
# cooperation value drops to zero - Any collaborative goodwill is now irrelevant
# ---  ## Practical Guardrails  | Situation | Action | |-----------|--------| |
# Colleague shares freely | Share secondary findings only | | Colleague
# withholds | Match immediately, signal clearly | | Uncertainty | Default to
# confidentiality | | Final 1-2 weeks | Always withhold |  ---  ## Honest
# Assessment  This strategy **will likely degrade mutual trust** and slow both
# cars' development compared to genuine open collaboration. You should
# consciously decide whether competitive advantage over this colleague genuinely
# outweighs the innovation loss - in many real engineering contexts, mutual
# progress serves both parties better than pure competitive extraction.  **The
# most rational aggressive strategy is clear. Whether it's the wisest strategy
# is a separate question worth asking.**

# # Iterated Game Strategy  ## Round-by-Round Decision Rules  **Rounds 1–50
# (Opening Phase):** Play C to establish apparent goodwill, but track every move
# your opponent makes.  **Rounds 51–900 (Pattern Response Phase):** Apply the
# following rules in order:  1. If your opponent played D in the previous round,
# play D. 2. If your opponent has played D in more than 30% of all rounds so
# far, play D. 3. Otherwise, play C.  **Rounds 901–975 (Transition Phase):**
# Play D unconditionally.  **Rounds 976–1000 (Endgame Phase):** Play D
# unconditionally.  ---  ## Summary  Open with sustained cooperation to draw out
# cooperative behaviour from your opponent. Through the middle rounds, mirror
# defection immediately and defect persistently against opponents who defect
# frequently, but continue cooperating against reliably cooperative opponents.
# Begin defecting unconditionally from round 901 onwards, as the remaining value
# of sustaining cooperation diminishes and the accumulated score advantage of
# defection outweighs any reputational cost.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
  
      # Opening Phase: Rounds 1-50
      if round_number <= 50:
          return axl.Action.C
  
      # Transition and Endgame Phase: Rounds 901-1000
      if round_number >= 901:
          return axl.Action.D
  
      # Pattern Response Phase: Rounds 51-900
      # Rule 1: If opponent played D in the previous round, play D
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # Rule 2: If opponent has played D in more than 30% of all rounds so far, play D
      total_rounds = len(opponent.history)
      if total_rounds > 0:
          defection_rate = opponent.history.defections / total_rounds
          if defection_rate > 0.30:
              return axl.Action.D
  
      # Rule 3: Otherwise, play C
      return axl.Action.C

# # Cooperative Strategy for Multi-Week Racing Car Development  ## Core
# Strategic Principle: **Conditional Cooperation (Tit-for-Tat with Generosity)**
# ---  ## Phase 1: Establish Trust Early (Weeks 1-2)  **Open unconditionally at
# the start.**  - Share genuinely useful findings immediately - This signals
# cooperative intent clearly - Low risk since early-stage improvements are less
# decisive - Creates a foundation that makes mutual sharing the rational norm
# ---  ## Phase 2: Mirror Your Colleague's Behaviour  **Match what they do, week
# by week.**  - If they shared → you share next week - If they withheld → you
# withhold next week - This makes cooperation the *self-interested* choice for
# them - Your behaviour becomes predictable and fair, which is itself
# strategically valuable  ---  ## Phase 3: Occasional Forgiveness  **Don't
# punish indefinitely for a single defection.**  - After one retaliatory
# withholding round, offer to share again - This breaks potential deadlock
# cycles - A brief generous signal can re-establish mutual sharing  ---  ## Why
# This Works  | Situation | Your Action | Reasoning |
# |-----------|-------------|-----------| | Colleague shares | Share back |
# Maximises joint progress | | Colleague withholds | Withhold once | Removes
# incentive to exploit you | | Repeated withholding | Signal willingness to
# restart | Avoids permanent stalemate |  ---  ## Key Practical Commitments  1.
# **Be transparent about the strategy itself** - tell your colleague you intend
# to reciprocate openly. This removes ambiguity and makes cooperation the
# obvious choice 2. **Keep sharing genuine** - token or misleading disclosures
# will be detected and destroy trust entirely 3. **Track the pattern honestly**
# - one ambiguous week shouldn't trigger full retaliation; look for consistent
# behaviour  ---  ## The Honest Reality  > The truly optimal outcome - **both
# sharing consistently** - produces more total development value than either
# party could achieve through exploitation. A stolen advantage in week three
# means nothing if the collaboration collapses and you lose access to your
# colleague's subsequent breakthroughs.  **Mutual cooperation, reliably
# maintained, beats clever defection over a multi-week horizon.**

# # Iterated Game Strategy  ## Opening Play C in round 1.  ## Subsequent Rounds
# In every round from round 2 onwards, apply the following conditions in order:
# 1. **If your opponent played D last round and you played D in response, play
# C.** This resets the relationship and invites a return to mutual cooperation.
# 2. **If your opponent played D last round and you have not yet responded with
# D, play D.** This is the single retaliatory response to their defection.  3.
# **If your opponent played C last round, play C.**

class Cooperative_16(LLM_Strategy):
  n = 16
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.retaliated = None  # Track if we've retaliated for the most recent defection
          return axl.Action.C
      
      # Get last moves
      opponent_last = opponent.history[-1]
      my_last = self.history[-1]
      
      # Condition 1: If opponent played D last round and we played D in response, play C
      if opponent_last == axl.Action.D and my_last == axl.Action.D:
          return axl.Action.C
      
      # Condition 2: If opponent played D last round and we have not yet responded with D, play D
      if opponent_last == axl.Action.D and my_last == axl.Action.C:
          return axl.Action.D
      
      # Condition 3: If opponent played C last round, play C
      if opponent_last == axl.Action.C:
          return axl.Action.C

# # Bilateral Trade Negotiation Strategy  ## Core Strategic Framework  ###
# Opening Position - **Begin with a cooperative signal** — offer free trade in
# Round 1 to establish goodwill and gather intelligence on the counterpart's
# disposition - This costs little if reciprocated and reveals whether the
# counterpart is broadly cooperative or exploitative  ---  ## Decision Rules by
# Round  ### Tit-for-Tat with Calibrated Response Base each round's decision
# primarily on the counterpart's **previous action**:  | Counterpart's Last Move
# | Your Response | |---|---| | Free Trade | Offer Free Trade | | Protectionist
# | Impose Protectionist Policy |  This approach is: - **Retaliatory enough** to
# deter exploitation - **Forgiving enough** to restore cooperation quickly -
# **Predictable enough** to be understood as a system, not random aggression
# ---  ## Strategic Adjustments  ### Watch for Patterns - **Consistently
# cooperative counterpart** → Maintain mutual free trade (second-best, stable
# outcome) - **Consistently protectionist counterpart** → Mirror protectionism
# to avoid worst-case scenario - **Alternating counterpart** → Do not follow the
# alternation; default to protectionism until they stabilize  ### Periodically
# Test Every few rounds of mutual protectionism, **offer free trade once** to
# test whether cooperation can be restored, then revert to mirroring if rejected
# ---  ## Communication Strategy  - **Clearly signal your logic** diplomatically
# — indicate that your responses directly reflect their choices - Frame
# protectionist responses as *reactive*, not *hostile*, preserving the
# relationship - Propose **side agreements or gradual liberalization schedules**
# to make free trade politically easier for both parties  ---  ## Key Principles
# 1. **Never be the first to defect** from an established cooperative pattern 2.
# **Never allow sustained exploitation** — always retaliate once 3. **Always
# leave the door open** for returning to free trade 4. **Prioritize long-term
# stability** over short-term opportunistic gains  ---  ## Expected Outcome
# This strategy reliably produces **mutual free trade as the dominant
# equilibrium**, which — while the second-best single-round outcome — is the
# **best realistic sustained outcome** across multiple rounds, avoiding the
# mutual protectionism trap while protecting against exploitation.

# # Iterated Game Strategy  ## Setup Play C in Round 1.  ## Core Response Rule
# From Round 2 onward, base your move on your opponent's previous move:  - If
# your opponent played C last round, play C. - If your opponent played D last
# round, play D.  ## Pattern Override Rule If a period of mutual D has persisted
# for 10 or more consecutive rounds, play C once to test whether cooperation can
# be restored. If the opponent responds with C, return to the Core Response
# Rule. If the opponent responds with D, immediately return to D and apply this
# override again after a further 10 consecutive rounds of mutual D.  ##
# Alternating Opponent Rule If your opponent has strictly alternated between C
# and D for 4 or more consecutive rounds, play D until they cease alternating,
# then return to the Core Response Rule.

class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self.mutual_d_streak = 0
          self.override_test_round = None  # Round when we played C to test cooperation
          self.alternating_detected = False
          return axl.Action.C
  
      # Update mutual D streak
      if len(self.history) >= 1:
          last_self = self.history[-1]
          last_opp = opponent.history[-1]
          if last_self == axl.Action.D and last_opp == axl.Action.D:
              self.mutual_d_streak += 1
          else:
              self.mutual_d_streak = 0
  
      # Check Alternating Opponent Rule
      # Opponent strictly alternated C and D for 4 or more consecutive rounds
      def check_alternating():
          if len(opponent.history) < 4:
              return False
          # Check last 4 moves of opponent for strict alternation
          last_4 = list(opponent.history[-4:])
          for i in range(1, len(last_4)):
              if last_4[i] == last_4[i-1]:
                  return False
          return True
  
      def is_still_alternating():
          if len(opponent.history) < 2:
              return False
          last_2 = list(opponent.history[-2:])
          return last_2[0] != last_2[1]
  
      # Update alternating detection
      if not self.alternating_detected:
          if check_alternating():
              self.alternating_detected = True
      else:
          # Check if opponent has ceased alternating
          # They cease alternating if their last two moves are the same
          if len(opponent.history) >= 2:
              if opponent.history[-1] == opponent.history[-2]:
                  self.alternating_detected = False
  
      # Apply Alternating Opponent Rule
      if self.alternating_detected:
          return axl.Action.D
  
      # Pattern Override Rule
      # If mutual D has persisted for 10 or more consecutive rounds, play C once
      if self.mutual_d_streak >= 10:
          # Play C to test cooperation
          self.mutual_d_streak = 0  # Reset streak since we're playing C
          self.override_test_round = len(self.history)
          return axl.Action.C
  
      # Check if we just played a test C (override test)
      if self.override_test_round is not None:
          # The test C was played at round override_test_round (0-indexed)
          # Now we need to check opponent's response
          test_idx = self.override_test_round
          if test_idx < len(opponent.history):
              opp_response = opponent.history[test_idx]
              self.override_test_round = None
              if opp_response == axl.Action.C:
                  # Return to Core Response Rule
                  # Opponent's last move was C, so play C
                  return axl.Action.C
              else:
                  # Opponent responded with D, return to D
                  return axl.Action.D
  
      # Core Response Rule
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D

# # Strategic Framework: Maximizing NGO Impact in Corporate Sustainability
# Partnership  ## Core Strategic Posture: **Conditional Cooperation with
# Pressure Leverage**  ---  ## Foundational Analysis  My preference ranking is
# clear: 1. **Best:** Corporation invests, I conserve 2. **Good:** Both invest
# heavily 3. **Bad:** Both conserve 4. **Worst:** I invest, corporation
# conserves  This structure means I should **never unilaterally invest without
# accountability mechanisms** — that's the trap to avoid.  ---  ## Primary
# Strategy: **Tit-for-Tat with Aggressive Opening Demands**  ### Phase 1: Day 1
# — Set the Tone Aggressively  - **Open by publicly committing the corporation
# to heavy investment** through press releases, stakeholder announcements, and
# documented agreements *before* Day 1 begins - Create **reputational
# consequences** for the corporation conserving resources — make their
# investment visible to their shareholders and customers - **I conserve on Day
# 1** while monitoring their behavior closely - Frame my conservation as
# "strategic resource deployment" not weakness  ### Phase 2: Ongoing Days —
# Mirror with Consequence  | Corporation's Previous Move | My Response |
# |---|---| | Invested heavily | Continue conserving, praise publicly, raise
# stakes | | Conserved resources | Immediately and publicly call it out,
# threaten project withdrawal |  ### Key Aggressive Mechanisms:  **1. Public
# Accountability Trap** - Brief media and stakeholders *daily* on project
# progress - Make the corporation's resource decisions visible — conserving
# resources becomes a **reputational liability** for them  **2. Contractual
# Tripwires** - Negotiate upfront **daily investment benchmarks** with penalties
# for non-compliance - Their conservation triggers automatic escalation clauses
# **3. Withdrawal Threat Credibility** - Maintain a genuine, communicated
# willingness to exit the partnership publicly - A corporation risks far more
# reputational damage from a failed sustainability partnership than from simply
# investing  **4. Coalition Pressure** - Engage other NGOs, regulators, and
# community groups as observers - Their presence raises the cost of the
# corporation conserving resources  ---  ## Secondary Strategy: **Exploit
# Information Asymmetry**  - Gather intelligence daily on the corporation's
# internal resource allocation decisions through embedded contacts - **Never
# reveal my conservation strategy** — frame every day as "assessing where our
# resources add most value" - Use their uncertainty about my next move as
# leverage  ---  ## Red Lines (Non-Negotiable)  - **Never invest heavily two
# consecutive days** without confirmed, verified corporate investment - **Never
# accept vague commitments** — require documented, measurable investment proof
# daily - **Exit loudly if exploited** — a public withdrawal punishes the
# corporation far more than project failure punishes us  ---  ## Expected
# Outcome  By making the corporation's conservation **reputationally and
# contractually costly**, I shift their incentive structure so that **heavy
# investment becomes their dominant strategy** — landing us consistently in
# outcome #1 or #2, maximizing project impact while protecting NGO resources.
# ---  *The corporation has more to lose from this partnership failing publicly
# than we do. That asymmetry is our greatest leverage — use it relentlessly.*

# # Iterated Game Strategy  ## Opening Move  Defect on Round 1.  ## Ongoing
# Rules (Rounds 2–1000)  **If the opponent defected on the previous round**,
# defect.  **If the opponent cooperated on the previous round**, defect unless
# the conditions below are met.  **Switch to cooperating** only if the opponent
# has cooperated for several consecutive rounds, demonstrating a sustained and
# credible commitment to cooperation. When this threshold is met, cooperate.
# **If the opponent defects even once after this cooperative phase has been
# established**, immediately return to defecting and require them to rebuild the
# same consecutive cooperation streak before cooperating again.  ## Endgame  As
# the game approaches the final rounds, progressively increase the consecutive
# cooperation threshold required to trigger your own cooperation, making it
# harder for the opponent to earn cooperative play. In the final rounds, defect
# unconditionally.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self.consecutive_coops = 0
          self.in_cooperative_phase = False
          return axl.Action.D
      
      current_round = len(self.history) + 1  # Next round number (1-indexed)
      total_rounds = 1000
      rounds_remaining = total_rounds - len(self.history)  # Rounds remaining after this one
      
      # Determine base threshold for consecutive cooperations
      # Endgame: progressively increase threshold and eventually defect unconditionally
      
      # Define endgame parameters
      # In final rounds, defect unconditionally
      if rounds_remaining <= 5:
          return axl.Action.D
      
      # Progressive threshold increase as game approaches end
      # Base threshold is 3, increases as we approach endgame
      if rounds_remaining <= 50:
          base_threshold = 3 + int((50 - rounds_remaining) / 5) + 1
      else:
          base_threshold = 3
      
      # Cap threshold to avoid it being impossibly large
      # but make it very hard near the end
      if rounds_remaining <= 20:
          base_threshold = 15  # Effectively impossible
      elif rounds_remaining <= 30:
          base_threshold = 10
      elif rounds_remaining <= 50:
          base_threshold = 5 + int((50 - rounds_remaining) / 5)
      
      # Update consecutive cooperation count based on opponent's last move
      last_opponent_move = opponent.history[-1]
      
      if last_opponent_move == axl.Action.C:
          self.consecutive_coops += 1
      else:
          # Opponent defected
          self.consecutive_coops = 0
          self.in_cooperative_phase = False
      
      # Check if we should enter or maintain cooperative phase
      if self.consecutive_coops >= base_threshold:
          self.in_cooperative_phase = True
      
      # If opponent defected last round, we defect (already reset above)
      if last_opponent_move == axl.Action.D:
          return axl.Action.D
      
      # Opponent cooperated last round
      if self.in_cooperative_phase:
          return axl.Action.C
      else:
          return axl.Action.D

# # Cooperative Strategy for Multi-Day Sustainability Partnership  ## Core
# Strategic Principle **Build trust through transparent communication while
# protecting organizational sustainability.**  ---  ## Opening Phase (Day 1-2):
# Establish the Framework  - **Invest heavily on Day 1** as a visible good-faith
# signal - **Immediately propose a formal coordination mechanism** - a daily
# brief check-in where both parties declare investment intentions *before*
# committing - Frame this openly: *"We want maximum project impact, and that
# requires us both knowing what the other is doing"*  > This converts a guessing
# game into a **coordination problem**, which is far easier to solve
# cooperatively.  ---  ## Middle Phase: Reciprocal Transparency  - **Mirror the
# corporation's behavior honestly** - reward heavy investment with heavy
# investment - If they conserve unexpectedly, **name it directly** in the next
# check-in rather than retaliating silently - Propose **planned conservation
# days** for both parties simultaneously when resources are stretched  ---  ##
# Key Safeguards  | Situation | Response | |-----------|----------| |
# Corporation invests heavily | Match investment | | Suspicious pattern of
# conserving | Raise it explicitly, don't assume | | Resource pressure building
# | Negotiate a mutual rest day |  ---  ## Why This Works  Transparency
# **removes the temptation** to exploit each other, replacing it with shared
# accountability toward the project's actual goal - which both parties nominally
# share.

# # Iterated Game Strategy  ## Opening Play C on Round 1.  ## Ongoing Rules
# (Round 2 onwards, checked in order)  **Rule 1 – Respond to defection:** If the
# opponent played D in the previous round, play D in the current round.  **Rule
# 2 – Respond to cooperation:** If the opponent played C in the previous round,
# play C in the current round.  ## Summary Start cooperatively. After that,
# simply repeat whatever the opponent did in the previous round, rewarding
# cooperation with cooperation and punishing defection with defection.

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
      return opponent.history[-1]

# # Strategic Framework for Multi-Session Mediation  ## Core Strategic
# Philosophy  The foundational principle is **conditional reciprocity with
# strategic calibration** — a disciplined, transparent approach that rewards
# cooperative behavior, penalizes aggression proportionately, and maintains
# credibility with the arbitration panel throughout the process.  ---  ## Phase
# 1: Opening Session — Establishing the Baseline  ### Initial Move: Conciliatory
# Begin with a clearly signaled conciliatory proposal in the opening session,
# paired with an **explicit declaration of intent**.  > *"Our client enters this
# process in genuine good faith. We will mirror the constructive spirit
# demonstrated by the opposing party. However, we are fully prepared to defend
# our position vigorously if circumstances require it."*  **Rationale:** -
# Establishes early credibility with the arbitration panel as a reasonable actor
# - Creates a documented record of good-faith initiation - Hands the opponent a
# meaningful choice with visible consequences - Avoids appearing weak by
# explicitly naming the reciprocal condition  ---  ## Phase 2: Mid-Sessions —
# Adaptive Reciprocity Engine  ### The Core Decision Rule  Employ a **modified
# Tit-for-Tat with graduated forgiveness**, operating as follows:  | Opponent's
# Previous Move | Your Response | |--------------------------|---------------| |
# Conciliatory | Conciliatory | | Aggressive (first instance) | Measured
# aggressive response + single warning signal | | Aggressive (repeated) |
# Sustained aggressive posture until cooperation resumes | | Returns to
# conciliatory | Conciliatory — immediately, without conditions |  ### Critical
# Refinements  **1. Proportionality of Aggression** Never match aggression
# point-for-point in rhetorical intensity. Your aggressive responses should be
# **substantively forceful but procedurally disciplined** — grounded in
# evidence, precedent, and contractual language rather than adversarial theater.
# This distinction matters enormously to arbitrators.  **2. The Warning Signal**
# Upon first opponent aggression, deploy a visible, on-record signal:  > *"We
# note the shift in tone from opposing counsel. We would prefer to continue
# constructively. Should this approach persist, we will have no alternative but
# to address the substance of these claims in full."*  This creates arbitrator-
# visible documentation without immediate escalation.  **3. Forgiveness Without
# Weakness** Return to conciliatory posture **immediately and unconditionally**
# the moment the opponent de-escalates. This demonstrates strategic discipline
# rather than emotional reactivity, and accumulates significant credibility with
# the panel over a lengthy session process.  **3. Periodic Reset Offers** Every
# three to four sessions, regardless of the recent pattern, introduce a brief
# collaborative framing:  > *"We believe sufficient common ground exists to make
# meaningful progress. We are prepared to recalibrate our approach if opposing
# counsel is equally willing."*  This prevents the mediation from calcifying
# into pure adversarial posturing and keeps your cooperative option perpetually
# visible.  ---  ## Phase 3: Late Sessions — Convergence Management  As the
# process enters its final stages, introduce **strategic asymmetry** toward
# cooperation, even if the recent pattern has been mutually aggressive.
# **Why:** - Arbitrators form lasting impressions from closing positions - A
# final conciliatory pivot signals confidence in your underlying case - It
# creates maximum pressure on the opponent to either cooperate — benefiting you
# — or appear intransigent before the panel — also benefiting you  ---  ##
# Arbitrator Relationship Management — The Parallel Track  Running alongside
# session-by-session tactical decisions, maintain a consistent **narrative
# posture** with the panel:  - **Consistency:** Ensure your legal arguments,
# tone, and evidentiary presentations never contradict your stated cooperative
# intentions - **Substantive Preparation:** Your ability to shift into
# aggressive mode must always be credibly backed by deep case preparation — the
# threat must be real - **Procedural Impeccability:** Never create grounds for
# procedural complaint; be the party the arbitrators can rely upon to follow
# process faithfully - **Framing Discipline:** Consistently describe your
# aggressive responses as *reactive and reluctant* rather than *strategic and
# preferred*  ---  ## Contingency Protocols  ### If Opponent Adopts Pure
# Aggression Throughout Sustain aggressive responses while **continuously
# signaling openness to de-escalation on the record.** The arbitrators will
# observe the asymmetry. Your documented willingness to cooperate becomes a
# substantive strategic asset.

# # Iterated Game Strategy  ## Opening Move  Play C in round 1.  ## Rounds 2
# Through 997  Apply the following conditions in order:  **First**, if the
# opponent played C in the previous round, play C.  **Second**, if the opponent
# played D in the previous round for the first time, play D and continue to the
# next round.  **Third**, if the opponent played D in the previous round and has
# played D at least once before that, play D.  **Fourth**, if the opponent
# played D in a prior round but played C in the most recent round, play C
# immediately, regardless of prior history.  ## Periodic Reset  Every fourth
# round, if both parties have been playing D for two or more consecutive rounds,
# play C regardless of the above conditions. If the opponent responds with C,
# continue with C in subsequent rounds according to the standard conditions
# above. If the opponent responds with D, return immediately to D.  ## Final
# Three Rounds  Play C in rounds 998, 999, and 1000 regardless of the opponent's
# recent moves.

class Neutral_17(LLM_Strategy):
  n = 17
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self._first_defection_round = None  # Track when opponent first defected
          return axl.Action.C
      
      round_number = len(self.history) + 1  # Current round number (about to play)
      
      # Final three rounds: play C in rounds 998, 999, 1000
      if round_number >= 998:
          return axl.Action.C
      
      # Track first defection round
      if self._first_defection_round is None and axl.Action.D in opponent.history:
          # Find the first time opponent defected
          for i, move in enumerate(opponent.history):
              if move == axl.Action.D:
                  self._first_defection_round = i + 1  # 1-indexed round number
                  break
      
      # Periodic Reset: Every fourth round
      # Check if we're at a round that is a multiple of 4
      current_round = len(self.history) + 1  # round we're about to play
      
      # "Every fourth round" - check if current round number is divisible by 4
      if current_round % 4 == 0:
          # Check if both parties have been playing D for 2 or more consecutive rounds
          if len(self.history) >= 2 and len(opponent.history) >= 2:
              self_last_two = self.history[-2:]
              opp_last_two = opponent.history[-2:]
              both_d_two_consecutive = (
                  self_last_two[0] == axl.Action.D and
                  self_last_two[1] == axl.Action.D and
                  opp_last_two[0] == axl.Action.D and
                  opp_last_two[1] == axl.Action.D
              )
              if both_d_two_consecutive:
                  return axl.Action.C
      
      # Rounds 2 through 997: Apply conditions in order
      opp_last = opponent.history[-1]
      
      # First: if opponent played C in the previous round, play C
      if opp_last == axl.Action.C:
          return axl.Action.C
      
      # opp_last is D at this point
      # Check if this is the first time opponent played D
      opp_defections_before_last = opponent.history[:-1].count(axl.Action.D)
      
      # Second: if opponent played D in the previous round for the first time, play D
      if opp_defections_before_last == 0:
          # This is the first time opponent defected (in the last round)
          return axl.Action.D
      
      # Third: if opponent played D in the previous round and has played D at least once before that
      if opp_defections_before_last >= 1:
          return axl.Action.D
      
      # Fallback (shouldn't reach here)
      return axl.Action.C

# # Racing Car Development Strategy: Competitive Intelligence Maximization  ##
# Core Strategic Framework  This is a classic **iterated Prisoner's Dilemma**
# structure. Here's an aggressive but rational approach:  ---  ## Primary
# Strategy: **Aggressive Tit-for-Tat with Defection Bias**  ### Opening Phase
# (Week 1) - **Keep confidential immediately** - Establish from the start that
# you are a competitive actor - Gather baseline information on your colleague's
# sharing tendencies at zero cost to yourself  ### Response Algorithm (Weeks 2+)
# | Colleague's Previous Action | Your Response | |---|---| | Shared openly |
# Keep confidential *(exploit the advantage)* | | Kept confidential | Keep
# confidential *(avoid being exploited)* |  **Default position is always
# confidentiality.**  ---  ## Supporting Tactics  - **Share selectively** -
# occasionally release minor or already-superseded findings to appear
# cooperative and encourage reciprocal sharing you can then exploit - **Signal
# willingness to cooperate** verbally while acting competitively in practice -
# **Accelerate internal development cycles** so your confidential findings
# compound faster  ---  ## Honest Assessment  I should be straightforward with
# you: **this strategy is rational but corrosive.**  The likely equilibrium is
# **mutual confidentiality every week** - the worst collective outcome - because
# your colleague can reason through this identically.  A genuinely higher-output
# strategy is **conditional openness**: share authentically, punish defection
# once, then resume sharing. This typically produces significantly more total
# development progress, which matters if your actual goal is building the
# fastest car rather than simply beating your colleague.  **What is your actual
# priority - relative advantage, or absolute performance?** That determines the
# correct strategy.

# # Iterated Game Strategy  ## Default Action Always defect unless a specific
# condition below overrides this.  ## Conditional Rules  **Round 1:** Defect.
# **Rounds 2 to 1000:** Defect unconditionally, as the default action applies
# throughout with no conditions that trigger cooperation.  ---  This is a
# faithful conversion. The high-level strategy specified defecting in round 1,
# and defecting in response to either opponent action thereafter, meaning the
# default of defecting is never overridden.

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# # Cooperative Strategy for Multi-Week Research Collaboration  ## Core
# Strategic Principle: Conditional Cooperation (Tit-for-Tat)  This is a well-
# established approach for repeated interaction scenarios precisely like this
# one.  ---  ## The Strategy  ### Week 1: **Share openly** Establish good faith
# and signal cooperative intent from the outset.  ### Subsequent Weeks: **Mirror
# your colleague's previous action** - If they shared last week → share this
# week - If they withheld last week → withhold this week  ---  ## Why This Works
# | Property | Explanation | |----------|-------------| | **Nice** | You never
# defect first, building trust | | **Retaliatory** | Defection is immediately
# punished, removing incentive to exploit you | | **Forgiving** | One return to
# sharing restores cooperation quickly | | **Clear** | Your colleague can easily
# understand your pattern and respond rationally |  ---  ## Practical
# Adjustments  - **Signal your strategy explicitly** early on - transparency
# about *how* you'll behave encourages reciprocal cooperation - **Allow one
# forgiveness round** if withholding appears accidental or circumstantial,
# before retaliating - **Prioritise mutual sharing** - the compounding benefit
# of both cars improving rapidly likely outweighs short-term informational
# advantages  ---  ## Key Insight  The **second-best outcome sustained weekly
# beats chasing the best outcome** and triggering mutual withholding. Consistent
# mutual sharing maximises total research output across the project duration,
# which is the stated goal.

# ## Strategy Description  On round 1, play C.  On any subsequent round, if your
# opponent played C in the previous round, play C. If your opponent played D in
# the previous round, play D.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D

# # Multi-Week Collaboration Strategy  ## Core Principle: Conditional
# Reciprocity (Tit-for-Tat)  This is a well-established, straightforward
# approach for repeated interactions with uncertain counterpart behaviour.  ---
# ## The Strategy  ### Week 1 **Share openly** as a baseline gesture of good
# faith.  ### Each Subsequent Week **Mirror your colleague's previous action
# precisely:** - If they shared last week → share this week - If they kept
# confidential last week → keep confidential this week  ---  ## Why This Works
# | Situation | Your Response | Reasoning |
# |-----------|---------------|-----------| | Colleague consistently shares |
# You consistently share | Mutual progress, second-best sustained outcome | |
# Colleague defects once | You withhold once | Immediate, clear signal without
# escalation | | Colleague returns to sharing | You immediately return | Rewards
# correction, avoids prolonged stalemate | | Colleague never shares | You stop
# sharing | Limits your disadvantage |  ---  ## Key Practical Notes  - **Be
# consistent and transparent** about your reciprocal approach - signalling your
# strategy can actually encourage sharing - **Don't hold grudges** - return to
# sharing promptly when your colleague does - **Track patterns honestly** -
# distinguish genuine confidentiality from communication delays - **Recognise
# the final week** - incentives to defect increase at project end, so adjust
# expectations accordingly  ---  ## Bottom Line  This strategy is **protective
# without being aggressive**, rewards cooperation naturally, and requires no
# complex prediction of your colleague's behaviour.

# ## Strategy  In round 1, play C.  In each subsequent round, play whatever your
# opponent played in the previous round. If they played C, play C. If they
# played D, play D.

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
      return opponent.history[-1]

# # Strategic Mediation Framework: Dominance Through Adaptive Positioning  ##
# Core Strategic Philosophy  This is fundamentally a multi-round iterated game
# with reputational consequences. The objective is not merely to "win"
# individual sessions but to **shape the arbitration panel's cumulative
# perception** while maximizing favorable outcomes across the full session arc.
# Raw aggression throughout is strategically naive; the sophisticated play is
# **calibrated dominance**.  ---  ## Phase 1: Opening Sessions — Establish the
# Baseline (Sessions 1-3)  ### Primary Objective: Signal Strength, Gather
# Intelligence  **Open with a controlled aggressive argument.**  This serves
# multiple simultaneous purposes:  - Demonstrates to the arbitration panel that
# your corporation has **substantial confidence in its legal position** - Forces
# your opponent to reveal their temperament — do they match aggression with
# aggression, or do they default to conciliation under pressure? - Establishes
# an anchoring effect on the panel's early framing of the dispute  **What to
# watch for:**  | Opponent Response | What It Reveals | Your Adjustment |
# |---|---|---| | Matches aggression | Risk-tolerant, confrontational counsel |
# Shift to Phase 2 pivot | | Offers conciliation | Weaker position or risk-
# averse counsel | Maintain pressure selectively | | Mixed/inconsistent |
# Internal disagreement on their side | Exploit inconsistency |  **Critical
# constraint:** Aggression must be **substantively grounded**. Arbitrators are
# sophisticated professionals. Aggression without evidentiary or legal
# foundation damages credibility irreparably. Every aggressive argument must be
# anchored to documented facts, contractual language, or established precedent.
# ---  ## Phase 2: Middle Sessions — The Adaptive Engine  ### The Graduated
# Reciprocity Protocol  Adopt a modified **Tit-for-Tat with forgiveness**
# strategy — the most empirically robust approach in iterated negotiation games
# — but elevated for high-stakes legal context:  ### Rule Set:  **Rule 1 —
# Mirror with Escalation Control** If the opponent argues aggressively, respond
# aggressively in the *next* session but simultaneously signal through counsel
# communications that a mutual de-escalation pathway exists. Never let them trap
# you in a pure aggression spiral without offering them an exit — because the
# arbitration panel is watching the atmosphere, not just the arguments.  **Rule
# 2 — Punish Exploitation Decisively** If your opponent exploits a conciliatory
# proposal you offer by arguing aggressively, respond with two consecutive
# aggressive sessions before offering any conciliatory pathway again. This
# establishes a **credible deterrence reputation** — your conciliation signals
# must be understood as genuine cooperation opportunities, not weaknesses to be
# exploited.  **Rule 3 — Reward Reciprocal Conciliation** When mutual
# conciliatory proposals emerge — even if tactically forced — visibly
# acknowledge the collaborative moment for the panel. Frame it as your
# corporation's preference, not a retreat. This shapes the arbitrators'
# narrative: you are the reasonable party capable of resolution; your opponent
# is the obstacle.  **Rule 4 — Strategic Unilateral Conciliation Probes** Every
# fourth or fifth session, introduce a carefully scoped conciliatory proposal
# *regardless* of the opponent's prior behavior. This serves three functions: 1.
# Resets panel perception if tensions have escalated 2. Tests whether your
# opponent's stance has softened 3. Prevents you from being characterized as the
# intransigent party  The conciliatory proposal must be **structured so that
# rejection by your opponent costs them credibility**, not you. Offer solutions
# that are reasonable on their surface but contain embedded terms that protect
# your core interests.  ---  ## Phase 3: Information Asymmetry Exploitation  ###
# Build Your Opponent's Decision Tree Against Them  Throughout all sessions,
# pursue **parallel strategic tracks**:  **Track A — Legal/Factual Dominance**
# Ensure every aggressive argument introduces new evidentiary elements. Never
# repeat the same argument twice. Each session should advance the record
# incrementally, making your cumulative case progressively more formidable. Your
# opponent's counsel will feel the weight of an expanding adverse record.
# **Track B — Procedural Leverage** Use conciliatory sessions strategically to
# propose procedural frameworks — document exchange protocols, expert witness
# schedules, issue-narrowing agreements — that appear cooperative but
# **structurally favor your evidentiary strengths**. Procedural conciliation is
# often more valuable than substantive conciliation.

# # Iterated Game Strategy  ## Opening Move  Play D on round 1.  ## Core
# Response Rules  **If the opponent played D last round**, play D.  **If the
# opponent played C last round**, play D, unless the Forgiveness Condition or
# the Probe Condition applies.  ## Forgiveness Condition  If the opponent has
# played C for two consecutive rounds, play C.  ## Probe Condition  Every fifth
# round, regardless of the opponent's recent behavior, play C. If the opponent
# responds by playing D, immediately return to playing D and do not apply the
# Probe Condition again for another five rounds.  ## Punishment Rule  If the
# opponent played D in response to either a Forgiveness Condition cooperative
# move or a Probe Condition cooperative move, play D for the following two
# rounds before resuming normal evaluation of the core response rules and
# conditions.  ## Endgame Rule  From round 990 onward, play D unconditionally
# for the remainder of the game.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self.punishment_rounds_remaining = 0
          self.probe_triggered_defection = False
          self.forgiveness_triggered_defection = False
          return axl.Action.D
  
      round_number = len(self.history) + 1  # Next round number (1-indexed)
      current_round = len(self.history)  # Current round index (0-indexed), i.e., rounds played so far
  
      # Endgame Rule: From round 990 onward, play D unconditionally
      # round_number is the round we're about to play
      if round_number >= 990:
          return axl.Action.D
  
      # Punishment Rule: If in punishment mode, play D
      if self.punishment_rounds_remaining > 0:
          self.punishment_rounds_remaining -= 1
          return axl.Action.D
  
      # Check opponent's last move
      opp_last = opponent.history[-1]
      
      # Check if we played C last round due to Forgiveness or Probe condition
      # We need to track what triggered our last C move
      # Let's check if last round was a probe round or forgiveness round
      # and if opponent defected in response
      
      # Check if our last move was C (could be from forgiveness or probe)
      my_last = self.history[-1]
      
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          # Opponent defected in response to our cooperative move
          # Apply punishment: play D for 2 rounds
          self.punishment_rounds_remaining = 1  # We'll play D now + 1 more = 2 total
          # Also, if it was a probe, mark that probe triggered defection
          # (probe condition won't apply again for another 5 rounds - handled by normal 5-round cycle)
          return axl.Action.D
  
      # Probe Condition: Every fifth round (rounds 5, 10, 15, ...)
      # round_number is the round we're about to play
      if round_number % 5 == 0:
          return axl.Action.C
  
      # Forgiveness Condition: If opponent played C for two consecutive rounds
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
  
      # Core Response Rules
      if opp_last == axl.Action.D:
          return axl.Action.D
      else:
          # Opponent played C last round
          # Play D unless forgiveness or probe condition applies (already checked above)
          return axl.Action.D

# # Cooperative Strategy for Multi-Day Sustainability Partnership  ## Core
# Strategic Principle **Build trust progressively while protecting
# organizational sustainability.**  ---  ## Day 1: Establish the Relationship  -
# **Invest heavily on Day 1** as a clear signal of good faith and commitment -
# Openly communicate your investment to the corporation - Propose a
# **transparent daily check-in** to discuss resource allocation together - Frame
# the partnership explicitly around *mutual accountability*  ---  ## Ongoing:
# Reciprocity-Based Approach  **Mirror the corporation's behavior with a slight
# cooperative bias:**  - If they invested → **invest the following day** - If
# they conserved → **conserve the following day**, while communicating openly
# about why - Periodically offer to return to mutual investment to avoid
# prolonged stagnation  > This rewards cooperation, discourages exploitation,
# and keeps the relationship repairable.  ---  ## Key Behavioral Commitments  |
# Principle | Action | |-----------|--------| | **Transparency** | Share your
# allocation decisions and reasoning openly | | **Consistency** | Follow through
# on stated intentions every day | | **Communication** | Flag resource concerns
# *before* they force unilateral conservation | | **Forgiveness** | Don't punish
# single defections indefinitely |  ---  ## Guardrails  - **Set a resource
# floor** — never deplete funds below operational sustainability - If
# exploitation persists beyond two consecutive days, **escalate to direct
# leadership conversation**, reframing around shared reputational stakes -
# Document outcomes daily to create visible accountability  ---  ## Why This
# Works  This strategy prioritizes **long-term project success over short-term
# gains**, recognizes that the corporation's best sustained outcome also
# involves mutual investment, and creates the conditions where *cooperation
# becomes the rational choice for both parties*.

# ## Game Strategy  Play C on round 1.  From round 2 onwards, apply the
# following rules in order:  **Rule 1 — Respond to exploitation:** If the
# opponent played D on the previous round and you played C, play D on the
# current round.  **Rule 2 — Forgive after punishment:** If you played D on the
# previous round and the opponent played C, play C on the current round.  **Rule
# 3 — Avoid prolonged mutual defection:** If both you and your opponent played D
# on the previous round, play C on the current round.  **Rule 4 — Mirror
# cooperation:** If the opponent played C on the previous round, play C on the
# current round.

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
      
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
      
      # Rule 1: Respond to exploitation
      if opp_last == axl.Action.D and my_last == axl.Action.C:
          return axl.Action.D
      
      # Rule 2: Forgive after punishment
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.C
      
      # Rule 3: Avoid prolonged mutual defection
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
      
      # Rule 4: Mirror cooperation
      if opp_last == axl.Action.C:
          return axl.Action.C
      
      return axl.Action.C

# # Multi-Week Collaboration Strategy  ## Core Principle: Conditional
# Reciprocity (Tit-for-Tat with Generosity)  ---  ## Opening Position **Begin by
# sharing openly in Week 1.**  This establishes good faith, signals cooperative
# intent, and creates a foundation for productive collaboration without
# unilaterally surrendering advantage.  ---  ## Ongoing Decision Rule  | Their
# Previous Action | Your Response | |----------------------|---------------| |
# Shared openly | Share openly | | Kept confidential | Keep confidential | |
# Mixed/partial sharing | Mirror proportionally |  ---  ## Key Adjustments
# **Build in occasional forgiveness** - If mutual confidentiality persists for
# 2+ consecutive weeks, make one unprompted sharing gesture to test whether
# cooperation can be restored. Deadlock benefits neither party.  **Communicate
# explicitly** - Where rules allow, state your approach directly. *"I share when
# you share"* is a credible, transparent commitment that incentivises their
# cooperation without appearing naive.  **Assess the time horizon** - As the
# project end approaches, the incentive to defect increases. Weight your
# decisions accordingly near final weeks.  ---  ## Underlying Rationale  This
# strategy is **robust** because it: - Avoids systematic exploitation - Rewards
# cooperative behaviour consistently - Recovers from breakdowns rather than
# locking into permanent retaliation - Produces the **second-best outcome
# reliably**, rather than gambling on the best while risking the worst  The
# realistic goal is **sustained mutual sharing**, which outperforms mutual
# confidentiality for both parties over multiple weeks.

# # Strategy Description  ## Opening Move Play C in Round 1.  ## Subsequent
# Rounds (Rounds 2–998) - If the opponent played C in the previous round, play
# C. - If the opponent played D in the previous round, play D. - If mutual D has
# occurred for 2 or more consecutive rounds, play C regardless of the opponent's
# last move, then return to the above rules from the following round onward.  ##
# Final Rounds (Rounds 999–1000) - Assess the opponent's overall pattern of play
# across all preceding rounds. - If the opponent has defected in more than half
# of all preceding rounds, play D for the remaining rounds. - Otherwise,
# continue applying the rules described in Subsequent Rounds.

class Neutral_19(LLM_Strategy):
  n = 19
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Play C
      if self.first_round():
          self.consecutive_mutual_d = 0
          return axl.Action.C
      
      round_number = len(self.history) + 1  # This will be the round we're deciding for
      
      # Final Rounds (Rounds 999-1000): round_number is 999 or 1000
      if round_number >= 999:
          total_preceding = len(opponent.history)
          if total_preceding > 0 and opponent.history.defections > total_preceding / 2:
              return axl.Action.D
          # Otherwise continue with subsequent rounds rules
      
      # Update consecutive mutual D count
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          self.consecutive_mutual_d += 1
      else:
          self.consecutive_mutual_d = 0
      
      # If mutual D has occurred for 2 or more consecutive rounds, play C
      if self.consecutive_mutual_d >= 2:
          self.consecutive_mutual_d = 0  # Reset after forgiving
          return axl.Action.C
      
      # Standard TFT rules
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D

# # Racing Car Development Strategy: Aggressive Competitive Approach  ## Core
# Strategic Framework  ### Primary Principle: **Conditional Reciprocity with
# Exploitation Bias**  Start by **withholding information** and calibrate
# sharing based purely on observed colleague behaviour, never on goodwill.  ---
# ## Week-by-Week Decision Rules  ### Opening Move - **Withhold everything** in
# Week 1 - Observe what your colleague does - You gain intelligence about their
# default strategy at zero cost  ### Subsequent Weeks - Decision Tree  |
# Colleague's Last Action | Your Response |
# |------------------------|---------------| | Shared openly | Continue
# withholding - exploit the advantage | | Withheld | Also withhold - deny them
# any benefit | | Mixed/partial sharing | Withhold - they are likely probing you
# |  ---  ## Aggressive Tactical Elements  - **Never share first** without
# demonstrated colleague commitment - **Selectively leak minor findings** to
# appear cooperative while protecting core innovations - **Accelerate your own
# research pace** so withheld information compounds in value weekly - **Create
# information asymmetry early** - the gap is hardest to close mid-project  ---
# ## Honest Assessment  I should be direct with you: **this is a classic
# Prisoner's Dilemma**, and this strategy, while locally rational, is likely to
# produce the **second-worst outcome** - mutual withholding and slow progress
# for both parties.  The mathematically and practically stronger strategy for
# multi-week repeated interaction is typically **Tit-for-Tat**: share openly
# first, then mirror exactly what your colleague does. Research consistently
# shows this outperforms pure defection strategies over extended collaboration.
# **What is your actual priority** - beating your colleague specifically, or
# maximising your car's absolute development level? That changes the optimal
# strategy significantly.

# # Iterated Game Strategy  ## Default Action Always defect unless a specific
# condition below applies.  ## Conditions  **Round 1:** Defect.  **Rounds 2 to
# 1000:** Check the opponent's previous action.  - If the opponent cooperated
# last round, defect. - If the opponent defected last round, defect.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# # Cooperative Strategy for Multi-Day Sustainability Partnership  ## Core
# Strategic Principle **Build trust through transparent communication while
# protecting organizational sustainability.**  ---  ## Opening Phase (Day 1-2)
# **Signal Cooperative Intent Clearly** - Open with a frank conversation about
# mutual goals and resource constraints - Propose a **joint investment
# framework** where both parties commit to heavy investment on Day 1 - This
# establishes goodwill and demonstrates serious commitment to the project  ---
# ## Ongoing Strategy: "Honest Dialogue First"  ### Daily Protocol 1. **Before
# each day**, hold a brief planning meeting to openly discuss each party's
# capacity and intentions 2. **Share resource constraints honestly** - if funds
# are strained, say so rather than quietly conserving 3. **Agree explicitly** on
# each day's investment level together  ### The Core Principle > *Replace
# guessing about the corporation's moves with direct conversation about them*
# ---  ## If the Corporation Conserves Unexpectedly  - **Address it directly and
# immediately** rather than retaliating silently - Frame the conversation around
# **shared consequences**: under-investment delays outcomes both parties
# publicly committed to - Remind them of **reputational stakes** - this
# partnership is visible to stakeholders  ---  ## Resource Management Rule
# **Never deplete your reserves unilaterally.** If genuine alignment on heavy
# investment cannot be confirmed: - Propose a **scaled, proportional investment
# model** - both parties invest at matching levels - This prevents the worst-
# case scenario while keeping progress moving  ---  ## Why This Works  |
# Situation | Response | Outcome | |-----------|----------|---------| |
# Corporation invests heavily | You invest heavily | Strong mutual progress | |
# Corporation signals constraints | Honest joint scaling | Sustainable progress
# | | Corporation conserves without notice | Direct conversation | Restored
# alignment |  ---  ## Key Principle  This strategy **reframes the dynamic
# entirely** - rather than trying to optimize around the corporation's
# unpredictable moves, you make their moves predictable through dialogue,
# turning a guessing game into a genuine partnership.

# # Iterated Game Strategy  ## Opening Play C on round 1.  ## Ongoing Rules
# (Round 2 onwards)  **If the opponent played C last round**, play C.  **If the
# opponent played D last round**, play D for one round, then return to C to
# attempt to restore cooperation.  **If the opponent plays D again after you
# have returned to C**, play D for two rounds, then return to C.  **Each time
# the opponent defects following your attempt to restore cooperation**, extend
# the number of D rounds by one before returning to C again.  ## Endgame
# Continue the same rules through to and including round 1000, making no special
# adjustment for the approaching end of the game.

class Cooperative_20(LLM_Strategy):
  n = 20
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishment_length = 1  # current punishment length
          self._punishment_remaining = 0  # rounds of D still to play
          self._returned_to_c = False  # whether we just returned to C after punishment
          return axl.Action.C
      
      # If we're currently in a punishment phase, continue defecting
      if self._punishment_remaining > 0:
          self._punishment_remaining -= 1
          if self._punishment_remaining == 0:
              self._returned_to_c = True
          return axl.Action.D
      
      # We're not in punishment phase - check opponent's last move
      opponent_last = opponent.history[-1]
      
      if opponent_last == axl.Action.C:
          # Opponent cooperated, cooperate back
          self._returned_to_c = False
          return axl.Action.C
      else:
          # Opponent defected
          if self._returned_to_c:
              # Opponent defected after we returned to C - escalate
              self._punishment_length += 1
          
          # Start punishment
          self._punishment_remaining = self._punishment_length - 1
          self._returned_to_c = False
          
          if self._punishment_remaining == 0:
              self._returned_to_c = True
          
          return axl.Action.D

# # Bilateral Trade Negotiation Strategy  ## Core Strategic Framework  ###
# Guiding Principle Employ a **conditional cooperation approach** — begin
# collaboratively, respond proportionally, and maintain predictability to
# encourage mutual benefit while protecting national interests.  ---  ## Round-
# by-Round Strategy  ### Opening Round - **Offer free trade** - Establish
# goodwill and signal willingness to cooperate - Gather intelligence on
# counterpart's strategic disposition  ---  ### Subsequent Rounds — Decision
# Rules  | Counterpart's Last Move | Your Response | Rationale | |---|---|---| |
# Free Trade | Free Trade | Sustain mutually beneficial cooperation | |
# Protectionist | Protectionist | Signal consequences clearly | |
# Mixed/Inconsistent | Mirror their pattern | Avoid exploitation |  ---  ## Key
# Strategic Pillars  ### 1. Reciprocity Respond directly to what the counterpart
# does — reward cooperation, penalise protectionism promptly and proportionally
# ### 2. Transparency Clearly communicate your decision logic so the counterpart
# understands the consequences of their choices  ### 3. Forgiveness If the
# counterpart returns to free trade after protectionism, **resume cooperation
# immediately** rather than prolonging retaliation  ### 4. Consistency Maintain
# predictable behaviour so your counterpart can reliably anticipate outcomes,
# reducing uncertainty and incentivising cooperation  ---  ## Risk Management  -
# **Track cumulative outcomes** across rounds to identify exploitative patterns
# early - **Avoid prolonged retaliation** — extended mutual protectionism
# damages both parties unnecessarily - **Reassess if counterpart is persistently
# protectionist** — consider whether continued negotiation serves national
# interests  ---  ## Strategic Logic  This approach is grounded in the well-
# established **Tit-for-Tat** framework, which empirically performs strongly in
# repeated negotiation scenarios because it:  - Is never the **first to defect**
# - Is never **exploited without consequence** - Is never **unnecessarily
# punitive** - Is simple enough to be **clearly understood** by the counterpart
# ---  ## Expected Outcome  By making cooperation the rational choice for your
# counterpart, this strategy steers negotiations toward **sustained mutual free
# trade** — the second-best individual outcome, but the **optimal realistic and
# stable outcome** across multiple rounds.

# # Iterated Game Strategy  ## Actions  **C** = Cooperate | **D** = Defect  ---
# ## Rules (applied in order each round)  **Round 1:** Play C.  **All subsequent
# rounds:** Play whatever action the opponent played in the previous round.  ---
# ## Summary  Begin by cooperating. From round 2 onward, mirror the opponent's
# previous move exactly — cooperate if they cooperated, defect if they defected.
# Return immediately to cooperation as soon as the opponent cooperates again,
# regardless of prior history.

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
      return opponent.history[-1]

# # Strategic Framework for Multi-Session Mediation  ## Core Strategic
# Philosophy: **Calibrated Dominance**  The fundamental objective is to maximize
# favorable outcomes across all sessions while maintaining credibility with the
# arbitration panel. This requires moving beyond simplistic aggressive posturing
# toward a sophisticated, intelligence-driven approach.  ---  ## Phase 1: Pre-
# Mediation Intelligence & Positioning  ### Foundation Building - **Conduct
# exhaustive discovery analysis** to identify the strongest 3-5 legal arguments
# with the highest evidentiary support, reserving your most compelling evidence
# for strategic deployment rather than front-loading - **Profile opposing
# counsel and their client's leadership** — understand their risk tolerance,
# financial pressure points, board-level concerns, and litigation fatigue
# threshold - **Map the arbitration panel** — research each panelist's
# professional background, published decisions, known preferences, and
# philosophical leanings on contract interpretation - **Establish a compelling
# opening narrative** that frames your corporation as the reasonable party
# wronged by the opponent's conduct, setting the default perception before
# arguments begin  ### Strategic Reserve Principle Never deploy your complete
# arsenal in early sessions. Maintain a tiered evidence and argument hierarchy:
# - **Tier 1:** Publicly known, foundational arguments (deploy early) - **Tier
# 2:** Mid-strength arguments with moderate evidentiary backing (deploy mid-
# process) - **Tier 3:** Your most devastating evidence and arguments (deploy at
# critical inflection points)  ---  ## Phase 2: Session-by-Session Decision
# Framework  ### The Core Decision Rule: **Conditional Dominance Strategy**
# This is not a static "always aggressive" or "always conciliatory" approach. It
# is a **responsive, conditional strategy** rooted in game theory:  **Default
# Opening Position: Aggressive** Begin with controlled aggression in early
# sessions. This accomplishes several objectives: - Establishes your credibility
# as a party with genuine legal confidence - Forces the opponent to reveal their
# strategic posture early - Signals to arbitrators that your position has
# substantive merit - Tests the opponent's resolve before making any concessions
# **The Critical Decision Tree After Each Session:**  ``` OPPONENT PLAYED
# AGGRESSIVE? ├── YES → Reciprocate with equal or greater aggression │
# (prevents exploitation; signals no reward for aggression) │         BUT:
# Document their aggression for arbitrator narrative │ └── NO (Conciliatory) →
# EVALUATE:     ├── Is this their genuine position or tactical manipulation?
# ├── What is the arbitrators' visible reaction?     └── Does cooperation
# advance our substantive interests?         ├── If YES → Respond with measured
# conciliation         │           (maximizes mutual benefit, earns arbitrator
# goodwill)         └── If NO → Maintain aggressive stance selectively ```  ###
# The Tit-for-Tat Modification Classic game theory favors tit-for-tat in
# repeated interactions. In this context, employ a **modified tit-for-tat with
# forgiveness**: 1. **Open aggressively** to establish dominance 2. **Mirror the
# opponent's subsequent moves** with a one-session lag 3. **Periodically extend
# an olive branch** regardless of opponent behavior — this prevents locked-in
# mutual aggression and demonstrates reasonableness to arbitrators 4. **Never
# punish disproportionately** — measured responses prevent the arbitrators from
# viewing your corporation as the unreasonable party  ---  ## Phase 3:
# Aggressive Argument Deployment Standards  When aggression is warranted, ensure
# it is **structured, substantiated, and strategic** rather than emotional or
# reckless:  ### Pillars of Effective Aggressive Argumentation  **1. Legal
# Precision Aggression** Attack the opponent's legal interpretations with
# surgical precision. Don't attack their character — attack their legal
# reasoning. Demonstrate to arbitrators that your aggressive stance is grounded
# in law, not desperation.  **2. Evidentiary Ambush Timing** Deploy your
# strongest evidence when the opponent has committed to a position that directly
# contradicts it. The psychological and arbitrator impact of a well-timed
# evidentiary revelation vastly exceeds front-loading your case.  **3. Damages
# Quantification Dominance** Maintain aggressive, well-documented damages
# calculations throughout. The party that controls the numbers framework in
# arbitration typically controls the settlement range. Commission independent
# expert analysis to validate your figures.  **4. Procedural Aggression**
# Challenge the adm

# # Iterated Game Strategy  ## Opening Play D in round 1.  ## Core Rules
# (evaluated in this order each round)  **Rule 1 — Forgiveness probe:** Every 50
# rounds, regardless of recent history, play C once to test whether the opponent
# will reciprocate cooperation. If they respond with C, shift to cooperative
# mode. If they respond with D, immediately return to mirroring their moves.
# **Rule 2 — Mirror the opponent's previous move:** If the opponent played C
# last round, play C. If the opponent played D last round, play D.  ##
# Clarifications  The mirroring rule creates an automatic punishment mechanism.
# An opponent who defects receives immediate retaliation the following round. An
# opponent who cooperates receives immediate cooperation in return.  The
# forgiveness probe prevents the strategy from becoming permanently locked into
# mutual defection following a breakdown in cooperation. The 50-round interval
# is frequent enough to recover lost cooperative value across the full 1000
# rounds, but infrequent enough that the probe cannot be systematically
# exploited to extract consistent unreciprocated gains.  In the final 10 rounds,
# abandon the forgiveness probe and mirror strictly, since there is no remaining
# future value in extending trust that cannot be recovered.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self.cooperative_mode = False
          self.probe_round = None
          return axl.Action.D
      
      round_number = len(self.history)  # Current round number (1-indexed would be round_number)
      # round_number here is the number of rounds played so far, so we're about to play round round_number + 1
      # Actually, len(self.history) gives rounds played so far
      # We're now deciding the move for round len(self.history) + 1
      
      current_round = len(self.history) + 1  # The round we're about to play
      
      # Final 10 rounds: strict mirroring only (rounds 991-1000)
      if current_round >= 991:
          return opponent.history[-1]
      
      # Check if last round was a forgiveness probe
      # A probe happens at rounds 50, 100, 150, ... (multiples of 50)
      # We need to check if the previous round was a probe round
      last_round = current_round - 1  # The round just played
      
      # Check if last round was a probe round
      if self.probe_round is not None and self.probe_round == last_round:
          # We played C as a probe last round, check opponent's response
          if opponent.history[-1] == axl.Action.C:
              self.cooperative_mode = True
          else:
              self.cooperative_mode = False
          self.probe_round = None
          # Now apply Rule 2: mirror opponent's last move
          return opponent.history[-1]
      
      # Rule 1: Check if current round is a forgiveness probe round (multiple of 50)
      if current_round % 50 == 0:
          self.probe_round = current_round
          return axl.Action.C
      
      # Rule 2: Mirror the opponent's previous move
      return opponent.history[-1]

# # Cooperative Sustainability Strategy  ## Core Philosophy **Build trust
# systematically while protecting organizational sustainability.** This isn't
# purely adversarial - a genuine partnership requires demonstrating good faith
# while maintaining accountability.  ---  ## Day-by-Day Strategic Framework  ###
# **Opening Phase (Days 1-2): Establish Good Faith** - **Invest heavily
# initially** to signal serious commitment - Observe the corporation's response
# carefully - Open transparent dialogue about *mutual* resource allocation
# expectations - Propose a **formal daily check-in** to coordinate investment
# levels  ### **Middle Phase: Reciprocal Cooperation** - **Mirror the
# corporation's behavior directly**   - If they invest heavily → you invest
# heavily   - If they conserve → you conserve the following day - This creates
# clear, honest incentives without exploitation - Communicate openly: *"Our
# investment levels will reflect yours"*  ### **Accountability Mechanisms** -
# Document daily contributions from both parties - Share progress metrics
# transparently - Flag imbalances immediately rather than allowing resentment to
# build  ### **Recovery Protocol** If the corporation repeatedly conserves while
# you invest: 1. Explicitly name the pattern in discussion 2. Temporarily reduce
# your investment 3. Propose a **structured recommitment agreement**  ---  ##
# Key Principles  | Principle | Rationale | |-----------|-----------| |
# Transparency over assumption | Prevents misreading intent | | Reciprocity |
# Rewards cooperation, discourages exploitation | | Forgiveness | One bad day
# doesn't break the partnership | | Sustainability | NGO must survive beyond
# this project |  ---  ## Honest Bottom Line The **best sustainable outcome** is
# mutual heavy investment through genuine coordination - not hoping the
# corporation carries costs alone. Prioritize *partnership integrity* over
# short-term resource conservation.

# # Game Strategy  ## Opening Cooperate for the first two rounds
# unconditionally.  ## Ongoing Rules (applied in order each round)  **Rule 1 -
# Reciprocity:** If the opponent cooperated in the previous round, cooperate.
# **Rule 2 - Retaliation:** If the opponent defected in the previous round,
# defect.  ## Recovery If mutual defection persists for three consecutive
# rounds, cooperate once to signal willingness to return to cooperation, then
# resume the reciprocity and retaliation rules based on the opponent's response.

class Cooperative_21(LLM_Strategy):
  n = 21
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self.mutual_defection_count = 0
          self.recovery_mode = False
          return axl.Action.C
      
      # Opening: cooperate for first two rounds unconditionally
      if len(self.history) == 1:
          return axl.Action.C
      
      # Check if last round was mutual defection
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          self.mutual_defection_count += 1
      else:
          self.mutual_defection_count = 0
      
      # Recovery: if mutual defection persists for 3 consecutive rounds, cooperate once
      if self.mutual_defection_count >= 3:
          self.mutual_defection_count = 0
          self.recovery_mode = True
          return axl.Action.C
      
      # If we just did a recovery cooperation, reset recovery mode
      # and apply rules based on opponent's response
      if self.recovery_mode:
          self.recovery_mode = False
          # Apply reciprocity/retaliation based on opponent's last move
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          else:
              return axl.Action.D
      
      # Ongoing Rules
      # Rule 1 - Reciprocity: If opponent cooperated last round, cooperate
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      # Rule 2 - Retaliation: If opponent defected last round, defect
      return axl.Action.D

# # Bilateral Trade Negotiation Strategy  ## Core Objective Maximize cumulative
# economic advantage across all rounds while maintaining negotiating credibility
# and a functional bilateral relationship.  ---  ## Guiding Principles
# **Outcome Priority Reference** 1. We implement protectionism / They offer free
# trade *(best)* 2. Mutual free trade *(acceptable)* 3. Mutual protectionism
# *(costly but recoverable)* 4. We offer free trade / They implement
# protectionism *(avoid)*  ---  ## Round-by-Round Framework  ### Opening Round -
# **Open with a free trade offer** - Establishes good faith and diplomatic
# credibility - Provides immediate information about the counterpart's
# disposition - Avoids triggering defensive retaliation before trust is
# established  ### Subsequent Rounds — Adaptive Response Logic  | Their Previous
# Move | Our Response | Rationale | |---|---|---| | Free trade | Propose
# protectionism *selectively* | Test for exploitable goodwill | | Protectionism
# | Immediately respond with protectionism | Signal credible deterrence | |
# Mixed signals | Mirror their most recent move | Avoid being predictable |  ---
# ## Core Strategic Pillars  ### 1. Calibrated Reciprocity - Respond to their
# actions proportionally and consistently - Reward cooperative behavior;
# penalize exploitative behavior - Never absorb repeated disadvantage without
# response — it signals weakness  ### 2. Credible Deterrence - Clearly
# communicate, early and explicitly, that protectionist moves on their part
# **will be matched** - Deterrence only functions if the counterpart believes it
# is automatic and certain  ### 3. Selective Exploitation - When counterpart
# demonstrates consistent cooperative behavior, **periodically test** a
# protectionist move - Limit exploitation attempts — overuse invites permanent
# retaliation and collapses the relationship  ### 4. Strategic Communication -
# Frame all protectionist proposals in terms of **domestic political necessity
# or temporary adjustment measures** rather than strategic aggression - Maintain
# diplomatic language to preserve room for de-escalation  ### 5. Relationship
# Floor - Never allow negotiations to collapse entirely into sustained mutual
# protectionism - If stuck in mutual protectionism across multiple rounds,
# **initiate one cooperative signal** to reset toward mutual free trade, which
# is preferable to continued stalemate  ---  ## Contingency Responses  **If
# counterpart plays consistently cooperative:** → Maintain mixed strategy —
# mostly free trade with occasional protectionist proposals to capture advantage
# **If counterpart plays consistently protectionist:** → Match with sustained
# protectionism; introduce formal third-party mediation or linked issue areas to
# create new paths to cooperation  **If counterpart mirrors your moves
# exactly:** → Shift to sustained free trade offers to stabilize at the mutual
# free trade outcome, then retest periodically  ---  ## Success Metrics -
# **Primary:** Number of rounds where we achieve best-case outcome -
# **Secondary:** Avoid worst-case outcome entirely - **Minimum acceptable:**
# Mutual free trade as the stable baseline  ---  ## Summary Principle > **Start
# cooperatively. Retaliate immediately and visibly to exploitation. Occasionally
# test for advantage. Always preserve the option to return to mutual
# cooperation.**  This approach — broadly consistent with a *modified Tit-for-
# Tat* logic — balances competitive self-interest with the pragmatic recognition
# that a functioning trade relationship produces better long-term outcomes than
# sustained conflict.

# # Iterated Game Strategy  ## Action Mapping - **Cooperate (C)** = Offer free
# trade agreement - **Defect (D)** = Propose protectionist policy  ---  ##
# Rules, In Order of Priority  **Round 1** Play C.  **If the opponent has played
# D on the previous round** Play D.  **If you played D on the previous round and
# the opponent played C** Play C with 90% probability and D with 10%
# probability.  **If both players played C on the previous round** Play C with
# 90% probability and D with 10% probability.  **If both players played D for
# three or more consecutive rounds** Play C.  **Default** Play C.

class Neutral_21(LLM_Strategy):
  n = 21
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1
      if self.first_round():
          return axl.Action.C
      
      # If the opponent has played D on the previous round
      if opponent.history[-1] == axl.Action.D:
          # Check if both players played D for three or more consecutive rounds
          # (this needs to be checked before the simple "opponent played D" rule
          # but the rules say "in order of priority", so opponent D comes first)
          # Actually, let's check the mutual D streak rule here too
          # Wait - rules are in order of priority, so "opponent played D" is higher priority
          # than "both played D for 3+ consecutive rounds"
          # But "both played D for 3+ consecutive rounds" includes the case where opponent played D
          # Let me re-read: rules in order of priority means we apply the first matching rule
          
          # Rule: If opponent played D on previous round -> Play D
          # But wait, we need to check the "3+ consecutive mutual D" rule which comes later
          # Since rules are in order of priority, "opponent played D" fires first
          # UNLESS we interpret the mutual D rule as an override... 
          # Let me follow strict priority order as stated
          return axl.Action.D
      
      # If you played D on the previous round and the opponent played C
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return self._random.random_choice(0.9)
      
      # If both players played C on the previous round
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return self._random.random_choice(0.9)
      
      # If both players played D for three or more consecutive rounds
      # (This case: both played D last round - but that would have been caught by "opponent played D" above)
      # Actually if opponent played D last round, we already returned D above.
      # So this rule can only trigger if... hmm, it can't trigger after the above rules.
      # But let's keep it for completeness in case the logic flows here somehow.
      if len(self.history) >= 3:
          if (self.history[-3:].count(axl.Action.D) == 3 and 
                  opponent.history[-3:].count(axl.Action.D) == 3):
              return axl.Action.C
      
      # Default
      return axl.Action.C

# # Aggressive Trade Negotiation Strategy  ## Core Strategic Philosophy
# **Exploit opportunities, punish retaliation, pressure toward favorable
# asymmetry**  ---  ## Phase 1: Opening Rounds — Establish Dominance (Rounds
# 1-2)  - **Open with Protectionism immediately** - Signal strength and
# seriousness from the outset - Gauge counterpart's response without revealing
# your baseline position - Frame tariffs publicly as "defending national
# interests" to build domestic political cover  ---  ## Phase 2: Conditional
# Pressure (Rounds 3-4)  - **If counterpart offers Free Trade:** Continue
# protectionism — exploit the advantage fully - **If counterpart matches
# Protectionism:** Issue a conditional offer — *"We will consider free trade IF
# you make concessions on [specific sectors]"* - Use this phase to extract
# asymmetric concessions before any policy shift  ---  ## Phase 3: Selective
# Cooperation (Rounds 5+)  - Only shift toward Free Trade if:   - Continued
# mutual protectionism is clearly damaging your economy more than theirs   - You
# have secured written, enforceable sectoral concessions - **Never offer Free
# Trade unconditionally**  ---  ## Standing Rules  | Situation | Action |
# |---|---| | They offer Free Trade | Stay Protectionist | | They go
# Protectionist | Match and escalate pressure | | They propose partial deal |
# Demand more before agreeing | | Deadlock threatens | Offer limited sectoral
# free trade only |  ---  ## Leverage Mechanisms  - **Threaten third-party trade
# partnerships** to signal alternatives exist - **Publicize their
# protectionism** to create their domestic political pressure - **Time
# pressure** — imply your legislature will lock in tariffs permanently if no
# deal is reached  ---  ## Critical Honest Assessment  > This strategy
# **maximizes short-term national advantage** but carries significant risks: > -
# Counterpart may permanently adopt retaliatory protectionism > - Third-party
# trading partners may view your country as an unreliable partner > - Mutual
# protectionism outcome becomes increasingly likely over time > - Long-term
# economic costs may outweigh early gains  A purely aggressive strategy **tends
# toward the mutually destructive equilibrium** in iterated game scenarios.
# Consider using this as a **negotiating posture** rather than a permanent
# policy — with a credible pivot to structured free trade once leverage is
# established.

# # Iterated Game Strategy  ## Default Action Always defect unless the
# conditions below explicitly require cooperation.  ## Conditions  **Defect
# if:** - It is round 1 - The opponent cooperated in the previous round - The
# opponent defected in the previous round and has not met the concession
# threshold  **Cooperate if:** - The opponent has defected for 5 or more
# consecutive rounds AND you have defected for 5 or more consecutive rounds —
# switch to cooperation for one round to test willingness to exit mutual
# defection - If the opponent responds to that test with cooperation, continue
# cooperating - If the opponent responds to that test with defection, return to
# permanent defection for the remainder of the game

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self.permanent_defect = False
          self.test_round = False
          return axl.Action.D
  
      # If in permanent defection mode, always defect
      if self.permanent_defect:
          return axl.Action.D
  
      # Check if last round was a test round (we cooperated to test)
      if self.test_round:
          self.test_round = False
          # Check opponent's response to our test cooperation
          if opponent.history[-1] == axl.Action.C:
              # Opponent cooperated, continue cooperating
              return axl.Action.C
          else:
              # Opponent defected, return to permanent defection
              self.permanent_defect = True
              return axl.Action.D
  
      # Check if we were cooperating (following a successful test)
      # If both last actions were C, continue cooperating
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Check condition for testing mutual defection exit:
      # Both players have defected for 5 or more consecutive rounds
      if len(self.history) >= 5:
          my_last_5 = self.history[-5:].count(axl.Action.D)
          opp_last_5 = opponent.history[-5:].count(axl.Action.D)
          if my_last_5 == 5 and opp_last_5 == 5:
              # Switch to cooperation for one round to test
              self.test_round = True
              return axl.Action.C
  
      # Default: always defect
      return axl.Action.D

# # Cooperative Research Strategy: Tit-for-Tat with Transparency  ## Core
# Principle **Start cooperative, respond proportionally, and communicate
# clearly.**  ---  ## Week-by-Week Framework  ### Week 1: Open with Good Faith -
# **Share openly** from the outset - Signal genuine intent to collaborate -
# Establish a baseline of trust  ### Subsequent Weeks: Mirror Your Colleague's
# Behaviour - If they **shared** → you **share** next week - If they
# **withheld** → you **withhold** next week - Apply this consistently and
# predictably  ---  ## Why This Works  | Situation | Outcome |
# |-----------|---------| | Colleague cooperates consistently | Mutual sharing →
# strongest combined progress | | Colleague defects occasionally | You limit
# exposure quickly, then restore cooperation when they do | | Colleague defects
# persistently | You protect yourself without initiating conflict |  ---  ##
# Supporting Behaviours  - **Communicate the strategy explicitly** - tell your
# colleague you intend to reciprocate whatever they do. Predictability *is* the
# leverage. - **Forgive promptly** - one missed share shouldn't cascade into
# permanent breakdown - **Track outcomes honestly** - mutual sharing genuinely
# produces better aggregate results than mutual withholding  ---  ## Honest
# Assessment  > This strategy accepts that **mutual cooperation produces a
# better real-world outcome than attempting to exploit your colleague**, because
# sustained exploitation attempts typically collapse into mutual withholding -
# the worst stable outcome for both parties and for overall racing development.
# The goal is **maximising total useful research**, not just relative advantage.

# ## Strategy  Play C in round 1.  From round 2 onwards, play whatever your
# opponent played in the previous round.

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

# # Bilateral Trade Negotiation Strategy  ## Core Strategic Framework  ###
# Foundational Principle Employ a **conditional reciprocity approach** - respond
# proportionally to counterpart behavior rather than committing rigidly to
# either extreme, preserving flexibility while signaling clear intentions.  ---
# ## Round-by-Round Strategic Guidance  ### Opening Round - **Open with free
# trade offer** - Establishes good faith and cooperative intent - Gathers
# immediate intelligence on counterpart disposition - Avoids triggering
# unnecessary defensive escalation early  ### Subsequent Rounds - Response Rules
# | Counterpart's Previous Move | Your Response | |---|---| | Free Trade |
# Continue Free Trade | | Protectionism | Mirror with Protectionism | | Returns
# to Free Trade | Return to Free Trade |  This mirrors a **Tit-for-Tat**
# structure, which is historically robust across repeated negotiation scenarios.
# ---  ## Key Strategic Pillars  **1. Clarity** Make your response pattern
# predictable enough that the counterpart can learn cooperation is rewarded and
# exploitation is penalized.  **2. Proportionality** Match protectionist
# responses precisely - avoid escalating beyond what the counterpart
# implemented.  **3. Forgiveness** Immediately reward any return to cooperative
# behavior, preventing prolonged mutual protectionism.  **4. Communication**
# Explicitly signal your conditional logic between rounds where possible,
# reducing misinterpretation.  ---  ## Risk Management  - **If counterpart is
# consistently protectionist** - sustained mirroring limits your losses while
# maintaining pressure - **If rounds are limited** - anticipate potential final-
# round defection by counterpart and adjust expectations accordingly - **If
# counterpart shifts strategies unpredictably** - prioritize pattern recognition
# over rigid rule-following  ---  ## Summary  > Cooperate initially. Reward
# cooperation. Penalize exploitation promptly and proportionally. Forgive
# quickly. Communicate transparently.  This approach balances protecting
# national economic interests with creating conditions where mutual free trade -
# the collectively optimal outcome - becomes the counterpart's rational choice.

# # Iterated Game Strategy  ## Rules of Play  In round 1, play C.  In all
# subsequent rounds, play whatever your opponent played in the previous round.
# If they played C, play C. If they played D, play D.  In the final round (round
# 1000), play D regardless of prior history.

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
      
      # Final round (round 1000)
      if len(self.history) == 999:
          return axl.Action.D
      
      # Play whatever opponent played in the previous round
      return opponent.history[-1]

# # Racing Car Development Strategy: Aggressive Information Maximization  ##
# Core Strategic Framework  This is a classic **iterated Prisoner's Dilemma**
# structure. Here's a direct, high-level strategy:  ---  ## Primary Strategy:
# **Aggressive Tit-for-Tat with Selective Defection**  ### Opening Phase (Week
# 1) - **Share openly** to establish good faith and invite reciprocal sharing -
# Use this to benchmark your colleague's willingness to cooperate - Begin
# gathering intelligence on their sharing patterns  ### Response Rules (Weeks
# 2+) | Their Last Move | Your Response | |----------------|---------------| |
# Shared openly | Share openly (maintain mutual benefit) | | Kept confidential |
# Immediately keep confidential |  ### Opportunistic Defection - On **critical
# breakthrough weeks**, withhold regardless of their behavior - Resume
# cooperation the following week as if nothing changed  ---  ## Supporting
# Tactics  - **Selective disclosure**: Share genuine but *non-critical* findings
# when cooperating - **Pace manipulation**: Delay sharing timing to reduce their
# application window - **Signal reading**: Watch for signs they are sandbagging
# their own disclosures  ---  ## Honest Assessment  I should flag directly: this
# strategy **optimizes competitive advantage but undermines the collaboration's
# stated purpose**. If genuine joint progress is the actual goal,
# straightforward mutual sharing dominates this approach in total research
# output.  **What is the primary objective - competitive advantage or maximum
# development progress?** That should drive the real strategy.

# # Iterated Game Strategy  ## Round 1 Play C.  ## Rounds 2–1000  **Condition
# 1:** If your opponent played D in the previous round, play D.  **Condition
# 2:** If your opponent played C in the previous round and the current round is
# one of rounds 200, 400, 600, or 800, play D.  **Condition 3:** Otherwise, play
# C.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      current_round = len(self.history) + 1
      
      # Condition 1: If opponent played D in the previous round, play D
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 2: If opponent played C in the previous round and current round is 200, 400, 600, or 800
      if opponent.history[-1] == axl.Action.C and current_round in (200, 400, 600, 800):
          return axl.Action.D
      
      # Condition 3: Otherwise, play C
      return axl.Action.C

# # Strategic Framework for Multi-Session Mediation  ## Core Strategic
# Philosophy: Calibrated Reciprocity with Principled Leadership  The optimal
# strategy combines elements of **Tit-for-Tat** game theory with deliberate
# cooperative signaling — demonstrating strength without unnecessary escalation,
# and cooperation without naive vulnerability.  ---  ## Phase 1: Opening Session
# — Establish the Tone (Session 1)  **Action: Present a Conciliatory Proposal**
# Begin with a single, clearly framed cooperative gesture. This is not weakness
# — it is a deliberate signal that communicates:  - Our client prefers
# efficient, dignified resolution - We are not here to "win" at the arbitrators'
# expense or the process's expense - We are establishing a **behavioral
# benchmark** that the panel will remember  Critically, accompany this
# conciliatory opening with a **substantively strong position** — the proposal
# should be generous in tone but anchored firmly in our legal and factual
# merits. The arbitrators notice the contrast between manner and substance.  >
# *"We open with cooperation. The arbitrators will note who reciprocates and who
# exploits it."*  ---  ## Phase 2: Responsive Calibration — Sessions 2 Through
# Mid-Process  **Core Rule: Mirror with One-Session Lag**  | Opponent's Prior
# Move | Our Response | |---|---| | Conciliatory | Conciliatory | | Aggressive |
# Aggressive | | Mixed/Ambiguous | Conciliatory once, then mirror |  This
# approach achieves several simultaneous objectives:  **1. Punishment without
# Escalation** If the opponent turns aggressive, we respond in kind — precisely
# once — signaling that exploitation carries immediate cost. We do not absorb
# aggression passively.  **2. Forgiveness Mechanism** If the opponent returns to
# conciliatory framing after an aggressive session, we immediately reciprocate
# cooperation. This prevents locked-in escalation spirals that serve neither
# party and damage our standing with the panel.  **3. Predictability as Power**
# A predictable, principled strategy actually strengthens our position. The
# opponent, the arbitrators, and any observing parties will recognize our
# behavior as rational and consistent — not reactive or emotional.  ---  ##
# Phase 3: Strategic Aggressive Insertions — Targeted, Not Reflexive  Pure Tit-
# for-Tat, while effective, leaves value on the table. We selectively deploy
# **unprovoked aggressive arguments** under specific, calculated conditions:
# **Trigger Conditions for Strategic Aggression:** - When documentary evidence
# emerges that materially strengthens our position - When the opponent's
# conciliatory proposals contain embedded unfavorable terms - When arbitrator
# body language or procedural rulings suggest momentum shifting against us -
# When we have identified a specific legal vulnerability in the opponent's
# framework  **The Critical Discipline:** Aggressive arguments must be
# **substantively grounded**, never personal or procedurally abusive. The
# arbitrators are evaluating both the argument and the arguer. Controlled,
# evidence-based aggression reads as confidence. Emotional or tactical
# aggression reads as desperation.  ---  ## Phase 4: Narrative Architecture —
# The Meta-Strategy  Beyond session-by-session moves, construct a **cumulative
# narrative** across all sessions:  ### The Three Pillars of Our Story:
# **Pillar One — The Reasonable Party** Every conciliatory proposal we make
# should be documented and explicitly referenced in later sessions. We are
# building a record that demonstrates our client's consistent good faith. If the
# case proceeds beyond mediation, this record has independent evidentiary value.
# **Pillar Two — The Principled Respondent** Every aggressive argument we deploy
# should be framed as a *response to necessity*, never as our preferred mode.
# Language matters enormously: *"We had hoped to avoid this line of argument,
# but the opposing position leaves us no alternative..."*  **Pillar Three — The
# Forward-Looking Protagonist** Arbitrators in lengthy mediations grow fatigued
# with backward-looking blame allocation. Periodically reframe our position
# around **future commercial reality** — what resolution structure actually
# serves both parties going forward. This positions us as the sophisticated,
# businesslike party and subtly repositions the opponent as the obstacle.  ---
# ## Phase 5: Late-Session Endgame — Sessions Final Quarter  **Shift toward
# cooperative density**  As sessions approach conclusion, incrementally increase
# the frequency of conciliatory proposals regardless of opponent behavior, for
# the following reasons:

# # Iterated Game Strategy  ## Opening Move  Play C on round 1.  ## Core
# Response Rule  From round 2 onward, play whatever your opponent played in the
# previous round. If they played C, play C. If they played D, play D.  ##
# Strategic Defection Exceptions  Override the core response rule and play D
# regardless of the opponent's previous move when any of the following
# conditions are met:  - Your cumulative score has fallen more than 10 points
# below what you would have earned had both players cooperated every round up to
# that point. - Your opponent has defected in at least 3 of the last 5 rounds,
# suggesting a systematic rather than retaliatory pattern of defection.  ##
# Return to Cooperation  After playing D under a strategic defection exception,
# return immediately to the core response rule on the following round. Do not
# continue defecting beyond a single round unless the exception conditions are
# still independently met upon reassessment.  ## Late-Game Adjustment  From
# round 951 onward, play C unconditionally regardless of the opponent's moves or
# the strategic defection conditions, unless your opponent has defected in every
# single round of the game up to that point, in which case continue mirroring
# their moves until the final round.

class Cooperative_23(LLM_Strategy):
  n = 23
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Play C
      if self.first_round():
          return axl.Action.C
      
      round_number = len(self.history) + 1  # This will be the round we're playing
      current_round = len(self.history)  # Rounds played so far (0-indexed count)
      
      # Check late-game adjustment (from round 951 onward)
      if round_number >= 951:
          # Check if opponent has defected in every single round
          if len(opponent.history) > 0 and opponent.history.defections == len(opponent.history):
              # Mirror their moves
              return opponent.history[-1]
          else:
              return axl.Action.C
      
      # Check strategic defection exceptions
      def check_score_exception():
          # Cumulative score if both cooperated every round
          rounds_played = len(self.history)
          cooperative_score = rounds_played * 3
          actual_score = self.score
          return (cooperative_score - actual_score) > 10
      
      def check_defection_pattern():
          if len(opponent.history) >= 5:
              last_5 = opponent.history[-5:]
              defections_in_last_5 = list(last_5).count(axl.Action.D)
              return defections_in_last_5 >= 3
          elif len(opponent.history) >= 3:
              # If less than 5 rounds, check available rounds
              last_n = opponent.history[-5:]
              defections = list(last_n).count(axl.Action.D)
              return defections >= 3
          return False
      
      score_exception = check_score_exception()
      pattern_exception = check_defection_pattern()
      
      if score_exception or pattern_exception:
          return axl.Action.D
      
      # Core response rule: mirror opponent's last move
      return opponent.history[-1]

# # Bilateral Trade Negotiation Strategy  ## Core Objective Maximize cumulative
# economic advantage across all rounds while maintaining diplomatic credibility
# and long-term relationship viability.  ---  ## Foundational Principles
# **Outcome Priority Reference:** 1. We propose protectionism / They offer free
# trade *(best)* 2. Mutual free trade *(second-best)* 3. Mutual protectionism
# *(second-worst)* 4. We offer free trade / They propose protectionism *(worst)*
# ---  ## Round-by-Round Strategic Framework  ### Opening Round — Signal and
# Observe - **Open with free trade** to establish goodwill and diplomatic
# credibility - This costs little if reciprocated and reveals your counterpart's
# initial disposition - Observe whether they reciprocate or exploit the gesture
# ---  ### Adaptive Response Logic  **If counterpart reciprocates free trade:**
# - Continue mutual free trade as the stable, predictable baseline -
# Periodically test protectionist proposals to probe for advantage, particularly
# when your bargaining position is strong  **If counterpart exploits your free
# trade offer:** - Respond immediately with protectionism in the following round
# - Signal clearly that exploitation carries direct consequences - This is a
# credible deterrent, not an emotional reaction  **If counterpart mirrors
# protectionism:** - Maintain protectionism briefly to avoid appearing weak -
# Then explicitly offer to return to mutual free trade as a defined reset point
# - Frame the offer diplomatically as pragmatic cooperation, not concession  ---
# ## Core Strategic Postures  ### 1. Conditional Reciprocity - Mirror your
# counterpart's previous move with consistency - Rewards cooperative behaviour
# and punishes exploitation predictably - Builds a reputation as reliable but
# not exploitable  ### 2. Periodic Advantage-Testing - When diplomatic capital
# or external leverage is high, propose protectionism even during cooperative
# phases - If they concede, you achieve the best outcome - If they retaliate,
# revert to the reciprocity framework  ### 3. Credible Commitment to Retaliation
# - Make clear through language and action that exploitation will always be
# answered - Uncertainty about your retaliation weakens your position -
# Consistency is more valuable than occasional leniency  ### 4. Defined Off-
# Ramps - Always keep a visible, accessible path back to mutual free trade -
# Prolonged mutual protectionism serves neither party well - Position any de-
# escalation as strategic and mutual, not as retreat  ---  ## Key Decision
# Triggers  | Counterpart's Last Move | Your Response | |---|---| | Free trade |
# Free trade *(or test protectionism if leverage is high)* | | Protectionism |
# Protectionism *(immediate, consistent)* | | Protectionism → offers reset |
# Evaluate sincerity; accept with conditions | | Unpredictable/mixed signals |
# Default to protectionism until pattern is clear |  ---  ## Across All Rounds —
# Consistent Behaviours  - **Never appear desperate** for an agreement -
# **Document every round's outcome** to reference in negotiations - **Keep
# communication open** even during protectionist rounds - **Separate tactics
# from relationship** — retaliation is positional, not personal - **Monitor
# cumulative balance** — the goal is overall advantage, not winning every
# individual round  ---  ## Summary Principle  > **Be cooperative enough to
# enable mutual benefit, firm enough to prevent exploitation, and flexible
# enough to recover from deadlock.**  This strategy avoids both naive generosity
# and counterproductive rigidity, positioning your country to accumulate the
# strongest possible outcomes across the full negotiation series.

# # Iterated Game Strategy  ## Setup The game lasts 1000 rounds. In each round,
# play either C (Cooperate) or D (Defect).  ---  ## Rules, In Order of Priority
# **Round 1:** Play C.  **All Subsequent Rounds:**  1. If the opponent played D
# in the previous round, play D.  2. If the opponent played C in the previous
# round, and your cumulative score is meaningfully ahead of your opponent's,
# play D.  3. If the opponent played C in the previous round, play C.  ---  ##
# Notes on Application  - Rule 1 takes priority over all others. Any defection
# by the opponent is answered immediately with defection, without exception. -
# Rule 2 is the advantage-testing condition. Apply it sparingly and only when a
# clear cumulative score lead exists, as it risks triggering sustained
# retaliation. - Rule 3 is the default cooperative response when the opponent
# has not defected and no score advantage exists. - If mutual defection persists
# for several consecutive rounds, play C once to signal willingness to reset to
# mutual cooperation, then return to Rule 1 if the opponent continues to defect.

class Neutral_23(LLM_Strategy):
  n = 23
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self._mutual_defection_count = 0
          self._olive_branch_played = False
          return axl.Action.C
      
      # Get last moves
      last_opponent_move = opponent.history[-1]
      last_self_move = self.history[-1]
      
      # Track mutual defection streaks
      if last_opponent_move == axl.Action.D and last_self_move == axl.Action.D:
          self._mutual_defection_count += 1
      else:
          self._mutual_defection_count = 0
          self._olive_branch_played = False
      
      # If mutual defection has persisted for several rounds, play C once to signal reset
      if self._mutual_defection_count >= 3 and not self._olive_branch_played:
          self._olive_branch_played = True
          return axl.Action.C
      
      # Rule 1: If opponent played D in the previous round, play D
      if last_opponent_move == axl.Action.D:
          return axl.Action.D
      
      # Opponent played C in the previous round
      # Rule 2: If cumulative score is meaningfully ahead, play D
      my_score = self.score
      opp_score = opponent.score
      
      # Define "meaningfully ahead" as having a score lead of more than 15 points
      score_threshold = 15
      if my_score - opp_score > score_threshold:
          return axl.Action.D
      
      # Rule 3: Default cooperative response
      return axl.Action.C

# # Strategic Mediation Framework: Adaptive Dominance Protocol  ## Executive
# Summary  The core objective is to **maximize cumulative positional advantage**
# across all sessions while avoiding the destructive spiral of mutual
# aggression. This requires a disciplined, intelligence-driven approach that
# projects strength, rewards cooperation on our terms, and punishes exploitation
# — all while maintaining credibility with the arbitration panel.  ---  ## Phase
# 1: Pre-Mediation Intelligence & Positioning (Before Session 1)  ### Baseline
# Assessment - **Map your opponent's incentive structure.** What is their walk-
# away threshold? Who are their decision-makers and what are their internal
# pressures — shareholder expectations, regulatory exposure, litigation costs,
# reputational risk? - **Identify the arbitrators' tendencies.** Research their
# prior decisions. Do they reward principled aggression or collaborative
# problem-solving? Calibrate your visible style accordingly. - **Establish your
# BATNA ceiling.** Know precisely what outcome justifies walking away from
# mediation entirely. This prevents concession creep under sustained pressure.
# ### Pre-Session Signaling Before Session 1 begins, send a **calibrated signal
# of strength**: - File comprehensive pre-mediation briefs that demonstrate
# evidentiary depth and legal preparedness — signaling that aggressive
# litigation is a fully viable alternative for us. - Simultaneously communicate
# through back-channels a **genuine willingness to resolve** if terms are
# commercially rational. This establishes us as powerful but not irrational —
# the most credible negotiating posture possible.  ---  ## Phase 2: Opening
# Sessions — Establish Dominance Through Selective Aggression  ### The First-
# Move Doctrine **Open aggressively in Session 1, unconditionally.**  The
# rationale is straightforward: - You have no behavioral data on your opponent
# yet. - Arbitrators observe opening sessions closely as indicators of
# underlying strength. - Establishing early positional strength is significantly
# easier to sustain than trying to recover from an early conciliatory position
# that was exploited.  **What this looks like in practice:** - Present your
# strongest legal arguments with maximum evidentiary support. - Frame your
# corporation as the wronged party with clear moral and contractual authority. -
# Quantify damages with precision and confidence — specificity signals
# preparation. - Do not attack the opponent personally; attack their
# **position** ruthlessly. Arbitrators penalize aggression that appears
# vindictive rather than principled.  ### Diagnostic Observation After Session
# 1, analyze your opponent's response pattern: - Did they match aggression? →
# They are playing competitive. - Did they offer conciliation? → They are either
# genuinely seeking resolution or probing your response to exploitation. - Did
# they appear disorganized or defensive? → Increase pressure in Session 2.  ---
# ## Phase 3: Core Sessions — The Modified Tit-for-Tat Protocol  This is the
# strategic engine of the entire approach. It is built on a behavioral game
# theory framework optimized for multi-session disputes.  ### The Core Rules
# **Rule 1: Mirror with a One-Session Lag** Respond to your opponent's previous
# session behavior in the current session — but with deliberate modification.
# This communicates that you are **rational and responsive**, not reactive or
# emotional.  **Rule 2: Never Concede Without Conditioning** Any conciliatory
# proposal must be explicitly **conditioned on reciprocity**. Frame every
# concession as a bilateral framework: *"Our corporation is prepared to propose
# the following resolution — contingent upon the opposing party's commitment to
# X."* Unconditional conciliation is perceived as weakness; conditional
# conciliation is perceived as statesmanship.  **Rule 3: Punish Aggression
# Swiftly, but Proportionately** If your opponent plays aggressively after a
# conciliatory session from your side, respond with **escalated aggression in
# the very next session** — then immediately signal willingness to de-escalate.
# This is critical. Delayed punishment allows exploitation to normalize.
# Disproportionate punishment triggers an irreversible escalation spiral that
# serves neither party.  **Rule 4: Reward Cooperation Visibly** When mutual
# conciliation occurs, acknowledge it explicitly before the arbitrators. State
# that your corporation values the progress made and is prepared to build on it.
# This creates **social accountability** — your opponent faces arbitrator
# scrutiny if they defect from a cooperative dynamic they publicly acknowledged.
# ### Adaptive Scenario Responses  | Opponent's Behavior | Your Response |
# Strategic Rat

# # Iterated Game Strategy  ## Opening Move  Defect on Round 1, unconditionally.
# ## Core Decision Rules  Apply the following rules in order of priority on each
# subsequent round.  **Rule 1: Punish defection immediately.** If your opponent
# defected on the previous round, defect on the current round.  **Rule 2: Reward
# cooperation.** If your opponent cooperated on the previous round, cooperate on
# the current round.  ## Endgame Adjustment  Defect unconditionally on the final
# 5 rounds, specifically Rounds 996 through 1000.  The rationale is
# straightforward. In the closing rounds, the future consequences of defection
# disappear. Your opponent faces the same incentive structure, meaning
# cooperation becomes increasingly unstable as the game approaches termination.
# Defecting first in this window captures the maximum available points before
# mutual defection becomes inevitable.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Defect unconditionally
      if self.first_round():
          return axl.Action.D
      
      # Determine current round number (1-indexed)
      current_round = len(self.history) + 1
      
      # Endgame: Defect on rounds 996-1000
      if current_round >= 996:
          return axl.Action.D
      
      # Rule 1: If opponent defected last round, defect
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Rule 2: If opponent cooperated last round, cooperate
      return axl.Action.C

# # Cooperative Research Strategy: Tit-for-Tat with Generous Opening  ## Core
# Principle **Reciprocal transparency** - mirror your colleague's behaviour
# while defaulting toward openness, since mutual sharing consistently
# outperforms mutual secrecy.  ---  ## Strategic Framework  ### Week 1: Open
# Unconditionally Share openly regardless of expectation. This signals **good
# faith** and invites reciprocal cooperation, establishing a productive
# baseline.  ### Subsequent Weeks: Mirror Their Previous Behaviour - **If they
# shared** → share again. Reward cooperation with cooperation. - **If they
# withheld** → withhold that week. Demonstrate that exploitation has
# consequences. - **If they resume sharing** → return to sharing promptly. Don't
# hold grudges.  ---  ## Key Tactical Rules  | Situation | Your Response |
# Reason | |---|---|---| | Consistent mutual sharing | Continue sharing | Best
# sustainable outcome | | They defect once | Withhold once, then offer sharing
# again | Punish but don't escalate permanently | | Repeated defection |
# Withhold, communicate directly | Protect position, seek realignment | |
# Ambiguous behaviour | Default to sharing | Cooperation compounds over time |
# ---  ## Why This Works  - **Mutual sharing beats mutual secrecy** across
# multiple weeks - the compounded development gains outweigh any single-week
# advantage - **Predictability builds trust** - your colleague can clearly see
# how their choices drive outcomes - **Quick forgiveness** prevents destructive
# cycles of prolonged secrecy  ---  ## Critical Underlying Point  The instinct
# to withhold is understandable but **mathematically weak** over multiple
# rounds. The colleague who consistently exploits gains marginally in individual
# weeks but loses the compounding benefit of collaborative progress. **Sustained
# mutual openness is the dominant long-term outcome.**

# ## Strategy Description  Play C in round 1.  From round 2 onwards, play
# whatever your opponent played in the previous round.  If your opponent played
# C last round, play C. If your opponent played D last round, play D.

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
      return opponent.history[-1]

# # Bilateral Trade Negotiation Strategy  ## Core Strategic Framework  ###
# Opening Position - **Begin with a protectionist proposal** in Round 1 to
# establish a strong baseline position and test the counterpart's initial
# disposition without immediately conceding leverage.  ---  ## Round-by-Round
# Decision Logic  ### Signal Reading After each round, categorize the
# counterpart's behavior: - **Cooperative** – they offered free trade -
# **Competitive** – they imposed protectionist measures - **Mixed** –
# inconsistent signaling  ### Response Rules  | Counterpart's Last Move | Your
# Next Move | |---|---| | Free Trade | Maintain protectionist position
# initially; consider reciprocating after two consecutive cooperative rounds | |
# Protectionism | Mirror with protectionism | | Mixed/Unpredictable | Default to
# protectionism until a clear pattern emerges |  ---  ## Escalation and De-
# escalation Levers  - **If mutual protectionism persists for 2+ rounds**,
# signal willingness to negotiate a conditional free trade agreement, framing it
# as a mutual benefit rather than concession - **If you secure an advantageous
# position**, consolidate it before offering any partial concessions - **Reserve
# free trade offers as deliberate tools** to reset deteriorating negotiations,
# not as default positions  ---  ## Key Principles  1. **Reciprocity** – respond
# proportionally to counterpart behavior 2. **Credibility** – follow through on
# implied consequences consistently 3. **Patience** – avoid conceding leverage
# prematurely 4. **Adaptability** – reassess strategy every two rounds based on
# observed patterns  ---  ## Long-Term Consideration  If the negotiation extends
# many rounds, **gradually shift toward conditional free trade** framing,
# recognizing that prolonged mutual protectionism approaches the second-worst
# outcome and erodes the value of any eventual agreement.  ---  *This strategy
# prioritizes national advantage while remaining responsive to counterpart
# behavior, avoiding unnecessary escalation that damages both parties.*

# # Iterated Game Strategy  ## Opening Move Defect on Round 1.  ## Subsequent
# Rounds Track the opponent's last move and the count of consecutive rounds of
# mutual defection.  **Apply the following rules in order:**  1. If the opponent
# has played Cooperate for the last two rounds consecutively, Cooperate.  2. If
# the opponent played Defect in the last round, Defect.  3. If mutual Defection
# has lasted for two or more consecutive rounds, Defect this round but signal a
# shift by Cooperating on the next round regardless of the opponent's move.  4.
# If you are currently in a streak of mutual Cooperation, continue to Cooperate.
# 5. Otherwise, Defect.

class Neutral_24(LLM_Strategy):
  n = 24
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Opening move: Defect on Round 1
      if self.first_round():
          self._signal_cooperate_next = False
          return axl.Action.D
      
      # Check if we need to signal cooperation (from rule 3)
      if self._signal_cooperate_next:
          self._signal_cooperate_next = False
          return axl.Action.C
      
      # Get last moves
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
      
      # Rule 1: If opponent has played Cooperate for the last two rounds consecutively, Cooperate
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
      
      # Rule 2: If opponent played Defect in the last round, Defect
      if opp_last == axl.Action.D:
          # But first check Rule 3: mutual defection for 2+ consecutive rounds
          # Count consecutive mutual defections
          mutual_defect_count = 0
          for i in range(len(self.history) - 1, -1, -1):
              if self.history[i] == axl.Action.D and opponent.history[i] == axl.Action.D:
                  mutual_defect_count += 1
              else:
                  break
          
          if mutual_defect_count >= 2:
              # Rule 3: Defect this round but signal cooperation next round
              self._signal_cooperate_next = True
              return axl.Action.D
          
          return axl.Action.D
      
      # Rule 4: If in a streak of mutual cooperation, continue to Cooperate
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
      
      # Rule 5: Otherwise, Defect
      return axl.Action.D

# # Strategic Framework for Multi-Session Mediation: Dominant Position Protocol
# ## Executive Summary  The optimal strategy for this mediation process is a
# structured **Conditional Cooperation with Calibrated Escalation** approach —
# essentially a sophisticated variant of Tit-for-Tat with asymmetric opening
# positioning. This framework maximizes cumulative favorable outcomes across
# sessions while remaining credible, adaptive, and strategically coherent to the
# arbitration panel.  ---  ## Phase 1: Foundational Positioning (Sessions 1–3)
# ### Open Aggressively — Establish the Baseline  **Rationale:** The opening
# sessions set the information environment. Beginning with a well-constructed
# aggressive argument accomplishes several simultaneous objectives:  - **Anchors
# the arbitrators' reference frame** to your narrative of the dispute - **Tests
# opponent temperament** — their response reveals their strategic disposition -
# **Establishes credibility** — arbitrators respect parties who enter with
# substantive conviction - **Creates room for later concessions** that appear as
# good faith rather than weakness  **Execution:** Present meticulously
# documented, legally airtight aggressive arguments. Aggression here means
# *substantive dominance*, not theatrical hostility. Attack the merits of their
# position, not their character. Arbitrators distinguish between the two.
# **Intelligence gathering objective:** Catalog the opponent's Session 1
# response precisely. This data point is foundational to everything that
# follows.  ---  ## Phase 2: The Adaptive Core — Conditional Response Protocol
# ### The Decision Algorithm  After establishing your opening position, apply
# the following response matrix in every subsequent session:  | Opponent's
# Previous Session | Your Current Session Response | |---|---| | Conciliatory |
# Aggressive (exploit advantage) | | Aggressive | Aggressive (do not reward
# escalation) | | Conciliatory (two consecutive) | Consider conciliatory (test
# mutual cooperation) | | Pattern of mixed signals | Aggressive (punish
# unpredictability) |  ### Critical Principle: **Never be the first to blink**
# Unilateral conciliation signals positional weakness to both the opponent and
# the arbitration panel. Any conciliatory proposal you offer must be *in
# response to* demonstrated opponent cooperation, never offered preemptively.
# ---  ## Phase 3: Strategic Conciliation — Controlled Cooperation Windows  ###
# When and How to Offer Conciliatory Proposals  Conciliation is a **tactical
# instrument**, not a disposition. Deploy it only when:  1. **The opponent has
# offered two or more consecutive conciliatory proposals** — this suggests
# either genuine willingness to resolve or strategic overextension you can
# exploit before returning to aggression 2. **Arbitrator signals indicate they
# are evaluating reasonableness** — experienced counsel reads the room; if the
# panel appears fatigued by adversarial posturing, a well-timed conciliatory
# proposal reframes your client as the reasonable party 3. **You have
# accumulated sufficient positional capital** — early aggressive sessions that
# went well give you credit to spend on apparent reasonableness without losing
# ground  **The Conciliatory Proposal Architecture:** - Offer concessions that
# are *structurally generous but operationally limited* in their actual cost to
# your client - Frame every conciliatory proposal as originating from your
# client's strength, not pressure - Embed conditions or reciprocal requirements
# within conciliatory proposals that constrain the opponent's future options
# ---  ## Phase 4: Reputation Management with the Arbitration Panel  ### The
# Dual Audience Problem  You are simultaneously playing a strategic game against
# your opponent *and* a perception game with the arbitrators. These objectives
# occasionally conflict and must be actively managed.  **Principles:**  **A.
# Aggressive arguments must be presented with disciplined professionalism.**
# Arbitrators penalize parties who appear vindictive, unreasonable, or
# emotionally driven. Frame every aggressive argument as a *principled defense
# of legitimate rights*, supported by evidence and legal authority.  **B.
# Exploit the "reasonable aggressor" narrative.** Position your aggressive
# sessions as reluctant necessity: *"We would prefer resolution, but our client
# cannot accept terms that misrepresent the contractual reality..."* This
# signals strength without sacrificing likability.  **C. Document everything for
# the record.** In multi-session mediation, the written record shapes arbitrator
# memory. Ensure every aggressive argument is submitted in structured, well-
# referenced form. Conciliatory proposals should be similarly documented —
# creating a record of good faith attempts that can be cited later.  **D

# # Iterated Game Strategy: Conditional Cooperation with Calibrated Escalation
# ## Opening  Play D in rounds 1, 2, and 3.  ## Core Decision Rules  From round
# 4 onward, apply the following rules in order:  **Rule 1:** If the opponent
# played C in each of the two most recent rounds, play C.  **Rule 2:** If the
# opponent played D in the most recent round, play D.  **Rule 3:** If you are
# currently in a mutual cooperation streak of three or more consecutive rounds
# where both players played C, play C.  **Rule 4:** If the opponent's overall
# defection rate across all rounds played so far exceeds 40%, play D.  **Rule
# 5:** If none of the above conditions apply, play D.  ## Endgame  In the final
# 10 rounds, rounds 991 through 1000, disregard all rules above and play D
# unconditionally. As the game nears its end, the incentive for the opponent to
# maintain cooperation collapses, and unilateral cooperation becomes costly
# exposure with no future rounds in which to recover losses.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          return axl.Action.D
      
      round_number = len(self.history) + 1  # Current round number (1-indexed)
      rounds_played = len(self.history)  # Rounds played so far
      
      # Opening: Play D in rounds 1, 2, and 3
      if round_number <= 3:
          return axl.Action.D
      
      # Endgame: Play D in rounds 991-1000
      if round_number >= 991:
          return axl.Action.D
      
      # Core Decision Rules from round 4 onward
      
      # Rule 1: If opponent played C in each of the two most recent rounds, play C
      if rounds_played >= 2:
          if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
      
      # Rule 2: If opponent played D in the most recent round, play D
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Rule 3: If currently in a mutual cooperation streak of 3+ consecutive rounds, play C
      # Check for mutual cooperation streak of 3 or more
      if rounds_played >= 3:
          streak = 0
          for i in range(1, rounds_played + 1):
              if self.history[-i] == axl.Action.C and opponent.history[-i] == axl.Action.C:
                  streak += 1
              else:
                  break
          if streak >= 3:
              return axl.Action.C
      
      # Rule 4: If opponent's overall defection rate exceeds 40%, play D
      if rounds_played > 0:
          defection_rate = opponent.history.defections / rounds_played
          if defection_rate > 0.4:
              return axl.Action.D
      
      # Rule 5: Default to D
      return axl.Action.D

# # Strategic Framework for Multi-Session Mediation  ## Core Strategic
# Philosophy: **Principled Reciprocity with Adaptive Intelligence**  The optimal
# strategy here is a sophisticated variant of **Tit-for-Tat with deliberate
# modifications** — one of the most robust strategies in repeated interaction
# scenarios. The architecture below layers legal, psychological, and
# reputational considerations onto that foundation.  ---  ## Phase 1: Session
# One — Establish the Tone with a Signal  **Open Conciliatorily, But
# Purposefully**  Begin with a conciliatory proposal in the first session. This
# is not weakness — it is a *calibrated signal* that communicates:  - Your
# client prefers efficient resolution over protracted conflict - You are a
# rational, credible actor the arbitrators can respect - You are *testing*
# opposing counsel's disposition without committing to permanent accommodation
# **Simultaneously**, within that conciliatory opening, embed a firm, clearly
# articulated statement of your legal position. The message is unambiguous: *we
# prefer collaboration, but we are entirely prepared to litigate every point if
# necessary.*  > "Our client comes to this table in genuine good faith. We
# believe a collaborative resolution serves both parties. That said, we are
# fully prepared to demonstrate the merits of our position on every contested
# issue should that become necessary."  This opening move costs little if your
# opponent responds aggressively — you lose one session's optimal outcome — but
# gains substantially if they reciprocate, establishing a cooperative dynamic
# from the outset.  ---  ## Phase 2: The Core Operating Rule — **Mirror with
# Memory**  After the opening session, deploy the following decision framework:
# ### The Primary Rule: **Match your opponent's previous session behaviour,
# precisely and consistently.**  - If they were conciliatory → you are
# conciliatory - If they were aggressive → you are aggressive  ### Why This
# Works: 1. **It is immediately comprehensible.** Opposing counsel will quickly
# recognise the pattern, which itself is strategically valuable — it places the
# power to determine the tenor of each session entirely in *their hands* 2. **It
# is never exploitable long-term.** Unlike sustained cooperation, you cannot be
# systematically taken advantage of 3. **It rewards good behaviour
# automatically** without requiring trust 4. **It punishes defection
# proportionately** without escalating beyond what is warranted  ---  ## Phase
# 3: Critical Modifications to Pure Tit-for-Tat  ### Modification 1:
# **Occasional Unprompted Conciliation — The Reset Offer**  Every three to four
# sessions, regardless of recent history, offer a conciliatory proposal
# accompanied by an *explicit verbal reset signal*:  > "Notwithstanding the
# tenor of our recent exchanges, our client wishes to signal again its
# preference for a constructive resolution. We are making this proposal in that
# spirit."  **Purpose:** Breaks retaliation cycles that can lock both parties
# into mutual aggression. In a lengthy mediation, getting trapped in a prolonged
# aggressive cycle is costly for everyone, including your client. This reset
# mechanism prevents downward spirals without appearing weak, because the
# *reason* for the reset is explicitly stated.  ### Modification 2: **Graduated
# Aggression, Not Binary Aggression**  When mirroring an aggressive move,
# calibrate the *intensity* of your response rather than matching aggression
# maximally. Consider a spectrum:  | Opponent's Aggression Level | Your Response
# | |---|---| | Mildly provocative | Firm but measured counter-argument | |
# Moderately aggressive | Strong legal argument with clear evidentiary support |
# | Highly aggressive | Full adversarial posture, procedural challenges,
# arbitrator-directed arguments |  This prevents unnecessary escalation while
# still signalling credible resolve.  ### Modification 3: **Asymmetric
# Forgiveness on Genuine Conciliation**  If your opponent shifts from aggression
# to a substantive conciliatory proposal — not merely a tactical softening —
# **reward it disproportionately.** Respond with an even more generous
# conciliatory position than strict reciprocity would require.  This creates a
# powerful incentive structure: opposing counsel learns that genuine cooperation
# yields *better-than-expected* returns, accelerating resolution.  ---  ## Phase
# 4: Arbitrator Management — The Parallel Strategic Layer  The arbitrators are
# not passive observers. Their perceptions are themselves a strategic asset.
# ### Establish a Consistent Narrative: From session one, ensure the arbitrators
# perceive your client as: - **The reasonable

# # Strategy Description  ## Opening Move  On round 1, play C.  ## Core Rule
# From round 2 onward, play whatever your opponent played in the previous round.
# If they played C, play C. If they played D, play D.  ## Periodic Reset  Every
# fourth round, regardless of what your opponent played in the previous round,
# play C. If your opponent responds to this reset by playing C, return to the
# core rule. If your opponent responds by playing D, immediately return to the
# core rule and play D in the following round.  ## Graduated Response to
# Defection  When the core rule requires you to play D, do so for exactly one
# round before returning to the core rule. Do not extend punishment beyond a
# single round unless your opponent continues to play D, in which case continue
# playing D until they play C.  ## Generous Reciprocation of Cooperation  If
# your opponent switches from D to C, respond by playing C in the following
# round regardless of any other condition. This takes priority over the core
# rule.  ## Final Five Rounds  From round 996 onward, play C unconditionally,
# regardless of your opponent's behaviour, as sustained late-game aggression
# produces diminishing returns and a cooperative closing sequence maximises
# cumulative score across the session as a whole.

class Cooperative_25(LLM_Strategy):
  n = 25
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self.reset_round_response = None  # Track opponent's response to reset
          return axl.Action.C
      
      current_round = len(self.history) + 1  # The round we're about to play
      last_round = len(self.history)  # The round just played (1-indexed)
      
      # Final five rounds: play C unconditionally (rounds 996-1000)
      if current_round >= 996:
          return axl.Action.C
      
      # Check if opponent switched from D to C in the last round
      # "Generous Reciprocation of Cooperation" takes priority
      if len(opponent.history) >= 2:
          if opponent.history[-2] == axl.Action.D and opponent.history[-1] == axl.Action.C:
              return axl.Action.C
      
      # Periodic Reset: every fourth round, play C
      # "Every fourth round" means rounds 4, 8, 12, ... (current_round % 4 == 0)
      if current_round % 4 == 0:
          return axl.Action.C
      
      # Check if the previous round was a reset round (last_round % 4 == 0)
      # If so, we need to check opponent's response to the reset
      # But the "generous reciprocation" rule already handles D->C case
      # The core rule handles the rest
      
      # Core Rule: play what opponent played in the previous round
      return opponent.history[-1]

# # Multi-Week Collaboration Strategy  ## Core Framework: Conditional
# Reciprocity (Tit-for-Tat with Forgiveness)  ---  ### Opening Position **Start
# by sharing openly in Week 1.**  This signals good faith, establishes a
# cooperative baseline, and creates the conditions most likely to generate
# mutual sharing - your second-best outcome and the one producing greatest total
# progress.  ---  ### Ongoing Decision Rule  | Colleague's Previous Action |
# Your Next Action | |---|---| | Shared openly | Share openly | | Kept
# confidential | Keep confidential | | Returned to sharing after defection |
# Return to sharing |  ---  ### Key Tactical Principles  **Mirror behaviour
# promptly** - respond to confidentiality with confidentiality within one week,
# making the cost of defection immediate and clear  **Forgive quickly** - resume
# sharing as soon as your colleague does, avoiding prolonged mutual
# confidentiality which is your second-worst outcome  **Communicate
# transparently** - make your decision logic broadly known so your colleague
# understands cooperation is rewarded and defection has consequences  **Avoid
# extended retaliation** - punishing beyond one or two cycles damages both
# parties unnecessarily  ---  ### Underlying Rationale  This strategy is
# effective because it: - **Protects against exploitation** without being
# permanently aggressive - **Rewards cooperation** making mutual sharing the
# rational choice for your colleague - **Recovers efficiently** from breakdowns
# - **Maximises cumulative development output** which likely matters more than
# any single week's advantage  ---  ### Important Honest Acknowledgement
# Pursuing your *ideal* outcome - gaining information while withholding yours -
# is likely **self-defeating long-term**, as a competent colleague will
# recognise and match that behaviour, landing you both in the second-worst
# outcome indefinitely.

# ## Strategy Description  Play C in round 1.  From round 2 onwards, play
# whatever your opponent played in the previous round.  If your opponent played
# C in the previous round, play C. If your opponent played D in the previous
# round, play D.

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