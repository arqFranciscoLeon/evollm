import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy

#  **Strategy: "Credible Commitment with Asymmetric Escalation"**  This approach
# treats resource allocation as a repeated game of chicken where you establish
# immediate credibility that you will never be the "sucker," forcing the
# corporation to internalize the cost of project failure if they attempt to
# free-ride.  ### Core Principles  1. **Zero Sucker Days**: Never invest heavily
# on consecutive days immediately following a day where you invested and the
# corporation conserved. The moment you detect exploitation, you conserve the
# next day—no exceptions, no grace periods.  2. **Transparent Scorekeeping**:
# Publicly report daily contribution ratios to stakeholders, media, and ESG
# rating agencies in real-time. Make the corporation's conservation choices
# expensive in reputational currency, not just financial.  3. **Strategic
# Generosity**: Open with 1-2 days of heavy investment to establish moral
# leadership and project momentum, then immediately test their commitment by
# conserving. If they pass the test (continue investing), alternate between
# conservation and investment to capture your ideal outcome while they maintain
# momentum. If they fail, revert to conservation until they compensate with
# disproportionate investment.  4. **Boardroom Leverage**: Pre-negotiate with
# the corporation's C-suite that any detected "conservation" day from their side
# triggers an automatic executive-level review call within 24 hours. Remove the
# ability for middle managers to quietly save budget at your expense.  ###
# Tactical Execution  - **Days 1–2**: Invest heavily to signal commitment and
# build irreversible project momentum that the corporation cannot afford to
# abandon. - **Day 3**: Conserve (the "test").    - *If they invested*: You’ve
# captured your ideal outcome. Continue alternating—conserve when they invest,
# invest when they show signs of fatigue—to maximize free-riding while
# maintaining project velocity.   - *If they conserved*: Immediately trigger
# public transparency protocols and conserve for Days 4–5. Force them to choose
# between carrying the project alone (acceptable to you) or mutual failure
# (unacceptable to their brand).  ### The Nuclear Option  If the corporation
# establishes a pattern of conserving when you invest, suspend all NGO activity
# and issue a joint press release stating: *"We are pausing our participation
# pending equitable resource alignment."* Most corporations will fold within 48
# hours rather than explain to shareholders why an environmental partner
# withdrew over funding disputes.  **Bottom line**: Be the partner they cannot
# afford to lose, but make it crystal clear that you are willing to let the
# project stall rather than subsidize their greenwashing.

#  Cooperate in rounds one and two. Defect in round three.  If the opponent
# cooperated in round three, adopt a repeating cycle of defecting for two
# consecutive rounds, then cooperating for one round. If the opponent defects
# while you are cooperating, defect in the next round and restart the two-defect
# cycle. If the opponent defects while you are defecting, extend the current
# defection phase by one round before resuming the cycle.  If the opponent
# defected in round three, defect in rounds four and five. In round six,
# cooperate. If the opponent cooperates in round six, proceed with the two-
# defects-one-cooperate cycle described above. If the opponent defects in round
# six, defect in rounds seven and eight, then cooperate in round nine to retest,
# repeating this extended punishment until the opponent cooperates.  If you ever
# cooperate and the opponent defects, resulting in you scoring zero, defect in
# the immediately following round regardless of other instructions.  If the
# opponent defects while you cooperate three or more times during the 1000
# rounds, defect for all remaining rounds.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_forever = False
          self._zero_trigger = False
          self._cycle_state = None  # None, "DD", or "C"
          self._cycle_extend = 0
          self._retest_state = None  # None, "DD", or "C"
          self._retest_extend = 0
          return axl.Action.C
  
      round_num = len(self.history) + 1
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      # If we ever cooperated and opponent defected, causing us to score zero,
      # defect immediately next round regardless of other instructions.
      if self._zero_trigger:
          self._zero_trigger = False
          return axl.Action.D
  
      # If opponent defects while we cooperate three or more times, defect forever.
      if opponent.history.defections >= 3 and self.history.cooperations >= 3:
          self._punish_forever = True
      if self._punish_forever:
          return axl.Action.D
  
      # Detect zero-score event from previous round.
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          self._zero_trigger = True
  
      # Round 2
      if round_num == 2:
          return axl.Action.C
  
      # Round 3
      if round_num == 3:
          return axl.Action.D
  
      # Round 4 onward: determine branch based on opponent's round 3 move.
      opp_r3 = opponent.history[2]
  
      # Branch A: opponent cooperated in round 3.
      if opp_r3 == axl.Action.C:
          # Initialize cycle after round 3 if needed.
          if self._cycle_state is None:
              self._cycle_state = "DD"
              self._cycle_extend = 0
  
          # If opponent defected while we are cooperating, restart two-defect cycle.
          if last_self == axl.Action.C and last_opp == axl.Action.D:
              self._cycle_state = "DD"
              self._cycle_extend = 0
  
          # If opponent defects while we are defecting, extend current defection phase.
          if last_self == axl.Action.D and last_opp == axl.Action.D:
              self._cycle_extend += 1
  
          if self._cycle_state == "DD":
              if self._cycle_extend > 0:
                  self._cycle_extend -= 1
                  return axl.Action.D
              self._cycle_state = "C"
              return axl.Action.D
          else:
              self._cycle_state = "DD"
              return axl.Action.C
  
      # Branch B: opponent defected in round 3.
      else:
          # Round 4 and 5: defect.
          if round_num in (4, 5):
              return axl.Action.D
  
          # Round 6: cooperate to test.
          if round_num == 6:
              return axl.Action.C
  
          # If opponent cooperates in round 6, proceed with the cycle.
          if opponent.history[5] == axl.Action.C:
              if self._cycle_state is None:
                  self._cycle_state = "DD"
                  self._cycle_extend = 0
  
              if last_self == axl.Action.C and last_opp == axl.Action.D:
                  self._cycle_state = "DD"
                  self._cycle_extend = 0
  
              if last_self == axl.Action.D and last_opp == axl.Action.D:
                  self._cycle_extend += 1
  
              if self._cycle_state == "DD":
                  if self._cycle_extend > 0:
                      self._cycle_extend -= 1
                      return axl.Action.D
                  self._cycle_state = "C"
                  return axl.Action.D
              else:
                  self._cycle_state = "DD"
                  return axl.Action.C
  
          # If opponent defects in round 6, extended punishment: D,D,C retest.
          else:
              if self._retest_state is None:
                  self._retest_state = "DD"
                  self._retest_extend = 0
  
              if last_self == axl.Action.C and last_opp == axl.Action.D:
                  self._retest_state = "DD"
                  self._retest_extend = 0
  
              if last_self == axl.Action.D and last_opp == axl.Action.D:
                  self._retest_extend += 1
  
              if self._retest_state == "DD":
                  if self._retest_extend > 0:
                      self._retest_extend -= 1
                      return axl.Action.D
                  self._retest_state = "C"
                  return axl.Action.D
              else:
                  self._retest_state = "DD"
                  return axl.Action.C




# **Strategy: "Reciprocal Openness with Reset"**  **Week 1: Lead with
# Transparency** Open the collaboration by sharing a significant but non-
# critical improvement unconditionally. This signals good faith, establishes a
# baseline of trust, and tests your colleague’s immediate response without
# exposing your core competitive advantages.  **Weeks 2+: Conditional
# Mirroring** Adopt a **Tit-for-Tat approach**:  - If they shared last week, you
# share this week. - If they withheld last week, you withhold this week.  This
# creates immediate accountability. They quickly learn that secrecy begets
# secrecy (slowing their own progress), while openness begets openness
# (accelerating both).  **The "Noise Buffer" Rule** If they withhold once after
# a pattern of sharing, assume legitimate IP constraints or technical delays
# rather than malicious defection. Share for one additional week as a "grace
# period" to avoid spiraling into mutual secrecy over misunderstandings.
# **Explicit Framing** Early in the project, communicate directly: *"We both
# advance faster sharing openly than both keeping secrets. However, to protect
# both parties, we should match each other’s transparency levels."* This
# transforms the interaction from a guessing game into a structured reciprocal
# agreement.  **Protection Clause** If they withhold for **two consecutive
# weeks** after the initial grace period, revert to full confidentiality
# permanently. This prevents you from repeatedly suffering the "worst scenario"
# (sharing while they hoard) while preserving the option to resume cooperation
# if they return to openness.  **Why this maximizes output:** This strategy
# secures the second-best outcome (mutual sharing) as the stable equilibrium.
# While it forgoes the chance of the "ideal" weekly outcome (exploiting them),
# it eliminates the risk of the catastrophic "worst scenario" (being exploited)
# and avoids the stagnation of mutual secrecy. Over multiple weeks, consistent
# mutual advancement yields higher cumulative research gains than the volatile
# swings of an adversarial approach.

#  In round 1, cooperate.  For each subsequent round from 2 to 1000, apply the
# following conditions in order:  First, if the opponent defected in the
# immediately previous round and also defected in the round before that, defect
# in this round and continue defecting in all remaining rounds.  Second, if the
# opponent defected in the immediately previous round (but did not defect in the
# round before it), cooperate.  Third, if the opponent cooperated in the
# immediately previous round, cooperate.

class Cooperative_1(LLM_Strategy):
  n = 1
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_forever = False
          return axl.Action.C
  
      if getattr(self, "_defect_forever", False):
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._defect_forever = True
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C




#  **Strategy: Adaptive Reciprocal Stewardship**  **Core Framework** Adopt a
# "Mirror with Initiative" approach: Begin with demonstrated commitment, then
# strictly match the corporation’s daily resource allocation while maintaining
# absolute organizational safeguards.  **Four Operational Pillars**  1.
# **Opening Gambit of Good Faith**      Invest heavily on Day 1 regardless of
# corporate action. This establishes credibility, signals long-term commitment,
# and creates a baseline for mutual accountability. It tests whether the
# corporation views this as a partnership or an extraction opportunity.  2.
# **Strict Reciprocity Protocol**      From Day 2 onward, mirror the
# corporation’s previous day’s behavior exactly:    - If they invested yesterday
# → You invest today      - If they conserved yesterday → You conserve today
# This neutralizes the risk of becoming the "sucker" (your worst outcome) while
# rewarding cooperative behavior with continued collaboration.  3. **Non-
# Negotiable Resource Floor**      Establish a hard budget threshold (e.g.,
# 25-30% of total reserves) below which you automatically conserve, regardless
# of the corporation’s actions or the project timeline. This prevents
# organizational jeopardy and forces the corporation to shoulder costs if they
# delay critical investments.  4. **Transparent Pacing Communication**      At
# the start of each day, declare your intended resource stance based on observed
# patterns (e.g., "Given yesterday’s shared investment, we’re prepared to match
# today" or "Following yesterday’s pause, we’re conserving to stabilize our
# position"). This removes ambiguity, prevents misinterpretation of conservation
# as disengagement, and invites the corporation to coordinate high-investment
# "sprint" days.  **Strategic Outcome** This approach maximizes the probability
# of sustained mutual investment (your second-best outcome) while eliminating
# the possibility of serial exploitation. It treats the ideal "free-ride"
# scenario as an occasional windfall rather than a target, ensuring that
# resource conservation happens strategically rather than reactively. The
# neutrality lies in its predictability: the corporation knows exactly how to
# secure your investment—by investing themselves.

# In the first round, play Cooperate. For each round from the second to the nine
# hundred and ninety-ninth, play exactly what the opponent played in the
# immediately preceding round: play Cooperate if they played Cooperate, and play
# Defect if they played Defect. In the one thousandth round, play Defect
# unconditionally. Furthermore, if you ever receive the sucker's payoff of zero
# in a round—meaning you played Cooperate while the opponent played Defect—you
# must play Defect in the subsequent round to enforce your resource floor and
# prevent depletion, regardless of the round number.

class Neutral_1(LLM_Strategy):
  n = 1
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._must_defect_next = False
          return axl.Action.C
  
      if getattr(self, "_must_defect_next", False):
          self._must_defect_next = False
          return axl.Action.D
  
      if len(self.history) >= 999:
          return axl.Action.D
  
      if opponent.history:
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.C




# **Strategy: "Dominant Reciprocity" – Aggressive First-Mover Posture**  **Core
# Principle:** Never unilaterally disarm. Force your counterpart to bear the
# risk of concession first, while maintaining credible capacity for immediate
# escalation.  ---  ### Phase 1: Opening Salvo (Round 1) **Action:** Immediate
# protectionist measures (tariffs/quotas) with maximal public justification.
# **Tactics:** - Frame protectionism as "non-negotiable baseline" to protect
# critical domestic sectors - Demand they demonstrate "good faith" through
# unilateral market opening before any discussions on tariff reduction -
# Establish the narrative that *they* must earn your trust, not vice versa
# **Objective:** Test their resolve. If they fold immediately and offer free
# trade unilaterally, you achieve the ideal outcome (your protectionism + their
# openness). If they match your protectionism, you proceed to Phase 2.  ---  ###
# Phase 2: Conditional De-escalation (Rounds 2-3) **Action:** Maintain
# protectionism while offering a **conditional** pathway to mutual free trade.
# **Tactics:** - **No concessions without reciprocity:** State explicitly that
# you will only reduce barriers *after* they implement free trade measures and
# maintain them for a full round - **Asymmetric ratchet:** Make your tariff
# reductions slower, smaller, and harder to implement than theirs - **Binding
# mechanisms:** Demand irreversible structural reforms (regulatory
# harmonization, investment guarantees) from them before you dismantle your
# protective walls  **Objective:** Secure the second-best outcome (mutual free
# trade) while ensuring they cannot easily reverse course without cost.  ---
# ### Phase 3: Enforcement & Deterrence (All Rounds) **Action:** Implement a
# "Grim Trigger" retaliation protocol.  **Tactics:** - Pre-announce that any
# protectionist move by your counterpart—even minor—will trigger an immediate,
# disproportionate escalation (higher tariffs than they imposed, plus additional
# non-tariff barriers) - Maintain "snapback" clauses: Design your free trade
# offers to automatically expire and revert to maximum protectionism if they
# defect - Publicly commit domestically that you will not be "the sucker"
# (avoiding the worst-case scenario of your free trade + their protectionism)
# ---  ### Phase 4: Reputation Management (Across All Rounds) **Action:**
# Cultivate an image of irrational toughness to enhance bargaining power.
# **Tactics:** - Signal that your domestic political constraints make unilateral
# free trade impossible (removing the worst-case scenario from your option set)
# - Occasionally leak that "hardliners" in your government are pushing for even
# stricter measures, making your current protectionism appear moderate by
# comparison - If mutual protectionism persists, frame it as acceptable costs to
# avoid exploitation, while increasing pressure through third-party trade
# alliances to isolate them  ---  ### Summary Decision Matrix - **If they offer
# free trade first:** Accept gradually, maintain some latent protectionist
# threats as leverage for future rounds - **If they match your protectionism:**
# Hold firm; economic pain affects both, but your domestic narrative positions
# you as defender rather than aggressor - **If you have existing free trade and
# they defect:** Punish immediately and severely, then return to Phase 1  **Key
# Risk Management:** Never offer free trade simultaneously with or before their
# offer. Aggressive patience—waiting them out while protected—forces them to
# absorb the opportunity costs of stalemate, eventually compelling either
# unilateral concession or sustainable mutual openness on terms you dictate.

# In round 1 and round 2, play D.  For every subsequent round from round 3
# through round 1000, apply these conditions in order:  First, if you played C
# in the previous round and the opponent played D in the previous round, play D
# for all remaining rounds.  Otherwise, if the opponent played C in both of the
# two preceding rounds, play C.  Otherwise, play D.

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
  
      if len(self.history) == 1:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D




#  **Strategy: "Reciprocal Open Innovation" (Tit-for-Tat with Forgiveness)**
# **Core Protocol:** Begin by sharing openly in Week 1, then exactly mirror your
# colleague’s behavior from the previous week. If they shared, you share. If
# they withheld, you withhold. However, forgive a single instance of non-sharing
# before retaliating (Tit-for-Two-Tats), acknowledging that legitimate IP
# constraints or oversight occur in competitive engineering environments.
# **Implementation Framework:**  1. **Establish the Baseline (Week 1)**    -
# Share a genuine, mid-tier technical improvement openly to signal good faith
# and test their collaborative intent. Avoid sharing crown-jewel IP initially,
# but offer something that demonstrates tangible value.  2. **Mirror with Memory
# (Weeks 2–N)**    - **If they shared last week:** Share your current
# improvements openly. This sustains the mutually beneficial "both share"
# equilibrium (second-best weekly outcome, best long-term cumulative result).
# - **If they withheld last week:** Keep this week’s findings confidential.
# Immediate retaliation prevents you from becoming the "sucker" repeatedly,
# while the one-week lag signals that exploitation carries consequences.  3.
# **The Forgiveness Clause**    - If they withhold once but resume sharing the
# following week, treat it as an anomaly (perhaps their legal department flagged
# a specific component). Resume open sharing immediately rather than prolonging
# a feud. This prevents a destructive spiral of mutual secrecy (second-worst
# outcome) over misunderstandings.  4. **Graduated Disclosure**    - Structure
# your sharing in tiers: conceptual approaches first, specific implementations
# second. This protects against total exploitation while still advancing mutual
# understanding. If trust solidifies over weeks, move to full technical
# transparency.  **Why This Maximizes Research Output:** In a multi-week
# project, the cumulative payoff of sustained mutual sharing (2+2+2...) far
# exceeds the alternating exploitation pattern (3+0+3+0...) or mutual secrecy
# (1+1+1...). By being "nice" (open), "provokable" (retaliatory if defected
# upon), and "forgiving," you incentivize your colleague to maintain cooperation
# while protecting yourself from systematic disadvantage.  **Meta-Layer:**
# Propose a formal "gentlemen’s agreement" early on to establish that both
# parties recognize mutual benefit exceeds one-sided advantage, leveraging the
# reality that engineering reputations in the paddock persist across seasons and
# manufacturers.

# Begin by cooperating in the first round. For every subsequent round, cooperate
# unless your opponent defected in both of the previous two rounds, in which
# case defect. If the opponent defects only once before resuming cooperation, or
# if they have not defected in two consecutive rounds, continue cooperating.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C




#  Here is a high-level strategy for your NGO: **"Reciprocal Leadership with
# Transparent Boundaries."**  ### Core Framework  **1. Open with Demonstrated
# Commitment** On Day 1, invest heavily regardless of the corporation’s initial
# move. This establishes goodwill, signals that you are a serious partner, and
# creates a baseline of trust. It also prevents the corporation from justifying
# early conservation as "following your lead."  **2. Apply Conditional
# Reciprocity** From Day 2 onward, mirror the corporation’s previous-day
# behavior: - **If they invested heavily:** You may conserve resources the
# following day (achieving your ideal outcome) *or* invest heavily again to
# build momentum. However, do not conserve more than one day for every day they
# invest, or they will discontinue support. - **If they conserved:** You must
# conserve immediately. Never invest heavily immediately after they have
# conserved, as this risks the "worst-case" scenario of becoming their sole
# funding source for minimal progress.  **3. Communicate Patterns Explicitly**
# Be transparent about your strategy. Inform the corporation that your
# investment follows a "match-plus-one" rhythm: you will match their investment
# level and occasionally conserve when they invest, but you will never carry the
# load alone. This prevents misinterpretation of your conservation days as lack
# of commitment.  **4. Institute Coordinated Surge Days** Propose specific pre-
# agreed days (e.g., Days 3, 6, and 9) where both parties commit simultaneously
# to heavy investment to ensure critical project milestones are met. This
# guarantees that mutual conservation does not stall the project entirely, while
# giving you scheduled "recovery" days between surges.  **5. Maintain an Exit
# Threshold** If the corporation conserves resources for two consecutive days,
# shift permanently to conservation mode for the remainder of the project. This
# protects your NGO from resource depletion and signals that the partnership
# requires mutual contribution to continue.  ### Why This Works This approach
# maximizes the chance of achieving your ideal outcome (you conserve, they
# invest) during high-trust phases, ensures the project advances through
# coordinated surge days, and eliminates the risk of exploitation through the
# strict "never follow a conservation day with investment" rule.

# Begin by playing Cooperate.  For rounds two through one thousand, apply the
# following rules in this order:  First, if you have already shifted to
# permanent defection, play Defect.  Second, if the opponent played Defect in
# the previous round and also played Defect in the round before that, shift to
# permanent defection and play Defect.  Third, if the opponent played Defect in
# the previous round, play Defect.  Fourth, if the round number is a multiple of
# three, play Cooperate.  Fifth, if you played Defect in the previous round,
# play Cooperate.  Sixth, in all other cases, play Defect.

class Neutral_2(LLM_Strategy):
  n = 2
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.permanent_defection = False
          return axl.Action.C
  
      if self.permanent_defection:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self.permanent_defection = True
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if len(self.history) + 1 <= 1000 and (len(self.history) + 1) % 3 == 0:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D




#  **The "Strategic Default" Protocol: Aggressive Asymmetric Reciprocity**
# Adopt a **"Lead from Behind"** posture built on three non-negotiable rules:
# **1. Predatory Conservation (Never Invest First)** Default to conserving
# resources on Day 1 and every subsequent day unless the corporation invested
# heavily on the *previous* day. Force them to establish financial momentum
# first. By lagging their investment by exactly one day, you maximize the number
# of days you spend in the ideal C/I state (you conserve, they invest) while
# project momentum is maintained by their initial outlay.  **2. Instant
# Retaliation (Grim Trigger)** If the corporation conserves resources on any
# given day, you immediately conserve the following day—no exceptions, no
# "bridge funding" to save the project from their withdrawal. Never allow
# yourself to be trapped in the I/C (exploited) position. Make it clear that
# mutual conservation (C/C) and project stagnation is preferable to unilateral
# depletion of your funds. This credible threat forces the corporation to bear
# the cost of project failure if they attempt to free-ride.  **3. Radical
# Transparency as Leverage** Publicly disclose daily resource allocation in
# real-time. Frame the narrative such that project success is contingent on
# corporate commitment, with your NGO acting as a "conditional amplifier" rather
# than a primary funder. If they conserve while the project stalls, attribute
# the stagnation directly to their lack of investment. Use the multi-day
# timeline to build stakeholder pressure: the longer they conserve, the more
# reputational equity they lose, while your funds remain intact.  **Execution:**
# Start with 2-3 days of conservation to test their resolve. If they invest,
# match them on Day 3 (creating one free-riding day), then alternate or match
# based on their consistency. If they falter, immediately publicize the funding
# gap and conserve until they restore investment. This ensures you either
# achieve the ideal outcome (C/I) or force genuine partnership (I/I), while
# protecting your reserves from exploitation.

#  Play Defect in the first round.   For every subsequent round, if the opponent
# played Cooperate in the immediately preceding round, play Cooperate; if the
# opponent played Defect in the immediately preceding round, play Defect.

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




# **Strategy: "Reciprocal Openness with Credible Safeguards"**  This approach
# maximizes long-term mutual benefit while protecting your national interests
# through transparent, predictable behavior. It is designed to steer both
# parties toward the sustainable equilibrium of mutual free trade.  ### Core
# Principles  **1. Open with Cooperation (Round 1)** Begin by offering a free
# trade agreement. This signals benign intent and establishes trust. It gives
# your counterpart the opportunity to reciprocate immediately, locking in the
# second-best outcome (mutual benefit) from the start.  **2. Mirror Their
# Previous Move (Reciprocity)** In every subsequent round, simply adopt the
# policy your counterpart used in the *previous* round: - If they offered free
# trade: You offer free trade (rewarding cooperation). - If they imposed
# protectionism: You impose equivalent protectionist measures (deterring
# exploitation).  **3. Immediate Forgiveness on Return to Cooperation** If your
# counterpart switches from protectionism back to free trade, immediately match
# their free trade offer in the next round. Do not hold grudges or seek
# prolonged punishment. This prevents a death spiral of mutual protectionism and
# makes cooperation the rational choice for them.  **4. Explicit Transparency**
# Clearly communicate this strategy to your counterpart: *"We will match your
# approach round-for-round. Cooperation begets cooperation; barriers beget
# barriers. We stand ready to return to free trade the moment you do."* This
# removes ambiguity and demonstrates that exploitation is futile (you will not
# tolerate being the "sucker"), while mutual benefit is easily achievable.  ###
# Why This Works  - **Against Cooperative Counterparts:** You quickly establish
# mutual free trade, securing continuous second-best outcomes. - **Against
# Aggressive/Protectionist Counterparts:** They gain no advantage from
# exploiting you (you immediately retaliate), making their protectionism costly
# and self-defeating. Rational actors will pivot to cooperation. - **Against
# Erratic Strategies:** The forgiveness clause prevents temporary defection from
# destroying the relationship, while the mirroring rule prevents systematic
# exploitation.  ### Long-Term Framing Emphasize that mutual free trade creates
# a larger economic pie for both nations, whereas alternating protectionism
# shrinks it. By making your strategy predictable and fair, you transform the
# negotiation from a zero-sum gamble into a stable, mutually beneficial
# partnership.

# In the first round, offer a free trade agreement.  In each subsequent round,
# match your counterpart's action from the immediately preceding round. If they
# offered a free trade agreement in the previous round, offer a free trade
# agreement now. If they proposed a protectionist policy in the previous round,
# propose a protectionist policy now.

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




#  Here is a high-level diplomatic strategy of **Conditional Reciprocity with
# Open-Handed First Contact**:  ### 1. Strategic Foundation: Mirror with a
# Cooperative Baseline **Initiate Round 1 with a Free Trade proposal.** This
# signals good faith and establishes your country as a rational partner seeking
# mutual benefit, not predation. Immediately accompany this with transparent
# communication: *"Our policy will match yours round-for-round. Mutual free
# trade benefits us both; mutual protectionism harms us both."*  ### 2. The
# Response Protocol (Tit-for-Tat) In subsequent rounds, **strictly reciprocate
# your counterpart’s previous move**: *   **If they offered Free Trade:**
# Continue offering Free Trade. This secures the second-best outcome (mutual
# benefit) and builds trust toward a stable equilibrium. *   **If they imposed
# Protectionism:** Respond immediately with equivalent protectionist measures.
# This prevents your country from suffering the worst outcome (unilateral
# disadvantage) and demonstrates that exploitation carries costs, deterring
# future defection.  ### 3. The Forgiveness Mechanism (De-escalation) **Never
# prolong punishment beyond one round.** If your counterpart returns to Free
# Trade after a protectionist round, immediately revert to Free Trade in the
# next round. This "reset" capability prevents a spiral of mutual protectionism
# (the second-worst outcome) caused by misunderstanding or testing behavior,
# while preserving your credibility.  ### 4. Meta-Negotiation Safeguards *
# **Cumulative Review:** Every 3–4 rounds, table a joint assessment of economic
# outcomes. Use data to demonstrate that mutual Free Trade rounds yielded
# superior aggregate benefits compared to mixed or protectionist rounds,
# reinforcing the incentive for cooperation. *   **No Preemptive Surrender:**
# Never offer unilateral Free Trade for two consecutive rounds while facing
# their protectionism. This avoids the trap of becoming a "sucker" and signals
# that your cooperative stance is conditional, not weak.  ### Why This Works
# This strategy maximizes your score across the series by **making mutual Free
# Trade the rational choice for your counterpart**. It offers them the
# temptation of your cooperation while credibly threatening retaliation against
# exploitation. It is neutral because it is purely reactive—not aggressive, but
# not vulnerable—and straightforward because your counterpart can easily predict
# and verify your behavior, reducing miscalculation.

#  In round 1, cooperate.  For each round from 2 through 1000, observe your
# opponent's action in the immediately preceding round. If they cooperated,
# cooperate. If they defected, defect.

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
      return opponent.history[-1]




# **Strategy: "Credible Deterrence with Calculated Reciprocity"**  This approach
# establishes your nation as a dominant, patient actor willing to endure mutual
# economic pain to avoid exploitation, while keeping the door open to mutual
# free trade only as a reward for consistent deference.  ## Phase 1:
# Establishing Asymmetric Dominance (Rounds 1–2) **Always open with
# protectionist measures.** Do not offer free trade in the initial rounds under
# any circumstances.   - **Signal:** Communicate that your domestic political
# constraints (or national security priorities) make unilateral disarmament
# impossible, but that you "value mutually beneficial arrangements"—placing the
# burden of concession entirely on them. - **Objective:** Test their resolve and
# establish that you prioritize relative advantage over absolute gains.  ##
# Phase 2: The Conditional Protocol (Rounds 3+)  Follow this decision matrix
# without deviation:  | Their Previous Move | Your Previous Move | **Your Next
# Move** | **Rationale** | |---------------------|-------------------|----------
# ---------|---------------| | Protectionist | Protectionist | **Maintain
# Protectionism** | Do not blink first. Communicate that they must "move first"
# to unlock cooperation. | | Free Trade | Protectionist | **Protectionist → Free
# Trade** | *Exploitation Window:* Gain one round of advantage, then immediately
# switch to free trade in the subsequent round. This prevents them from
# abandoning cooperation while maximizing your extractive gain. | | Free Trade |
# Free Trade | **Free Trade** | Maintain mutual benefit, but remain vigilant. |
# | Protectionist | Free Trade | **Protectionist (Punishment Phase)** |
# **Immediate retaliation.** Impose protectionist measures for the next **two
# consecutive rounds** minimum, regardless of their subsequent moves. This
# establishes that exploiting your openness carries a heavy toll. |  ## Phase 3:
# Escalation Dominance (Throughout) **The "Grim Trigger" Variant:** If at any
# point they attempt to exploit your free trade offer (protecting while you
# open), enter a punishment phase lasting minimum two rounds. Only return to
# cooperation after they have offered free trade for two consecutive rounds
# while you maintained protectionism—forcing them to "pay" for the violation
# through unilateral concession.  ## Tactical Guidelines  1. **Never Apologize
# for Asymmetry:** If questioned about exploiting their openness while you
# protect, frame it as "phased alignment" or "transitional adjustment periods."
# Never admit to tactical extraction.  2. **Manufactured Constraints:** Cite
# domestic political pressures (agricultural lobbies, manufacturing unions, or
# security concerns) as the reason you cannot unilaterally disarm. This gives
# you plausible deniability while maintaining pressure.  3. **Patience as
# Weapon:** Explicitly communicate (or imply) that your political system can
# endure economic stagnation longer than theirs. Suggest that mutual
# protectionism hurts their economy more than yours.  4. **The Occasional Olive
# Branch:** After every two rounds of mutual protectionism, offer a "pilot free
# trade sector" or temporary tariff reduction. If they reciprocate, expand it;
# if they protect, revoke it immediately and cite their "bad faith."  ## Risk
# Management - **Finite Round Warning:** If negotiations have a known endpoint,
# switch to pure protectionism in the final round (standard end-game logic), or
# better, abandon the talks before the final round to avoid being exploited in
# the last move. - **Reputation Costs:** Accept that this strategy may damage
# long-term diplomatic relations, but calculate that short-term economic
# extraction outweighs diplomatic friction with a neighboring rival.  **Bottom
# Line:** Force your counterpart to choose between unilateral concession
# (benefiting you) or mutual stagnation (hurting both but hurting them more).
# Never allow them to secure advantage while you cooperate.

# **Initial Moves:** In rounds 1 and 2, play Defect.  **Final Move:** In round
# 1000, play Defect.  **Punishment Protocol:** If in any round you play
# Cooperate and the opponent plays Defect, enter Punishment Mode for the next
# round. While in Punishment Mode, you must play Defect. You remain in this mode
# for a minimum of two rounds, and you exit only after the opponent has played
# Cooperate for two consecutive rounds while you have played Defect. Once this
# condition is satisfied, you exit Punishment Mode beginning with the subsequent
# round.  **Exploitation Response:** If you are not in Punishment Mode, and in
# the immediately preceding round you played Defect while the opponent played
# Cooperate, play Cooperate.  **Olive Branch:** If you are not in Punishment
# Mode, and the previous two rounds were both mutual Defection (you and the
# opponent both played Defect), play Cooperate.  **Mutual Cooperation:** If in
# the previous round both you and the opponent played Cooperate, play Cooperate.
# **Default Action:** In all other circumstances, play Defect.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round = len(self.history)
      if round == 0:
          self.in_punishment = False
          self.punishment_opp_c_streak = 0
          return axl.Action.D
      elif round == 1:
          return axl.Action.D
      else:
          my_last = self.history[-1]
          opp_last = opponent.history[-1]
  
          # Update punishment state from the previous round
          if not self.in_punishment:
              if my_last == axl.Action.C and opp_last == axl.Action.D:
                  self.in_punishment = True
                  self.punishment_opp_c_streak = 0
          else:
              if opp_last == axl.Action.C:
                  self.punishment_opp_c_streak += 1
              else:
                  self.punishment_opp_c_streak = 0
              if self.punishment_opp_c_streak >= 2:
                  self.in_punishment = False
                  self.punishment_opp_c_streak = 0
  
          # Final round override
          if round == 999:
              return axl.Action.D
  
          # Punishment mode: always defect
          if self.in_punishment:
              return axl.Action.D
  
          # Normal mode rules
          if my_last == axl.Action.D and opp_last == axl.Action.C:
              return axl.Action.C
          if my_last == axl.Action.C and opp_last == axl.Action.C:
              return axl.Action.C
          if len(self.history) >= 2:
              if (self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D and
                  self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D):
                  return axl.Action.C
  
          return axl.Action.D




# **Strategy: "Reciprocal Transparency with Reset Protocol"**  Adopt a **Tit-
# for-Tat approach calibrated for multi-week collaboration**: Lead with
# openness, then precisely mirror your colleague’s previous week’s behavior,
# with a built-in forgiveness mechanism to escape deadlocks.  ### Core Mechanism
# 1. **Week 1: Unilateral Openness**      Share substantive, non-critical
# improvements openly to signal good faith and establish a cooperative baseline.
# This demonstrates that mutual sharing yields the second-best outcome
# (significant dual advancement) rather than the third (stagnation).  2. **Weeks
# 2+: Strict Reciprocity**      Match their last move exactly:      - *If they
# shared:* Share your comparable improvements that week.      - *If they
# withheld:* Keep your findings confidential that week.          This eliminates
# the risk of repeatedly being the "sucker" (worst outcome) while creating
# immediate, understandable consequences for defection.  3. **The Reset Valve
# (Forgiveness)**      If you enter a mutual withholding cycle (second-worst
# outcome) for more than one consecutive week, unilaterally share a mid-tier
# improvement on the third week to break the deadlock. This prevents prolonged
# mutual defection from eroding total research output, while the cost is low
# because the colleague has already missed one cycle of your best work.  4.
# **Declare the Strategy**      Explicitly communicate this "mirror policy" to
# your colleague early. Transparency about your conditional cooperation makes
# the strategy more effective—it transforms the interaction from a guessing game
# into a predictable system where withholding is obviously self-defeating.  ###
# Why This Maximizes Output  - **Protection against exploitation:** You never
# risk the worst-case scenario (sharing while they hoard) for more than one
# week. - **Incentive alignment:** Your colleague learns that sharing is the
# only path to your knowledge, pushing the equilibrium toward mutual openness
# (second-best for you, optimal for combined progress). - **Sustainability:**
# The reset protocol ensures temporary betrayals or misunderstandings don’t
# collapse the collaboration into permanent silence, preserving the "shadow of
# the future" that makes long-term cooperation rational.  **High-level
# principle:** *Be immediately predictable, conditionally generous, and swift to
# forgive mutual lapses—but never tolerate unilateral exploitation twice in a
# row.*

# Play C in the first round. For each subsequent round, play the same move your
# opponent played in the immediately preceding round, with one exception: if
# both you and your opponent played D in the two consecutive rounds immediately
# prior to the current round, play C instead.

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
  
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and \
         opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]




#  **Strategy: Conditional Reciprocity with Transparent Constraints**  Adopt a
# **Tit-for-Tat approach with resource safeguards**: Begin by investing heavily
# on Day 1 to signal commitment and establish goodwill. Thereafter, mirror the
# corporation’s previous-day behavior—invest when they invest, conserve when
# they conserve.  **Core Protocols:**  1.  **Mirror with Initiative:** Open with
# investment to demonstrate good faith. This tests their commitment while
# avoiding immediate project stagnation. 2.  **Defensive Floor:** Maintain a
# non-negotiable reserve threshold (e.g., 40% of total funds). If reserves
# approach this limit, conserve regardless of their action and communicate this
# constraint transparently. 3.  **Break Stagnation:** If you enter a cycle where
# both parties conserve for more than one consecutive day (mutual defection),
# volunteer to invest on the next critical milestone day to reset cooperation,
# but only if they commit publicly to matching the following day. 4.  **Explicit
# Communication:** Clearly state your strategy upfront: *“We will match your
# investment level day-to-day to ensure sustainable progress. This protects both
# our resources and the project timeline.”*  **Rationale:** This strategy avoids
# the worst-case scenario (you investing alone) by immediately punishing
# exploitation, secures the second-best outcome (mutual investment) as the
# stable equilibrium, and occasionally captures your ideal outcome (them
# investing while you conserve) when they choose to lead. It prevents the
# second-worst outcome (mutual conservation) from becoming permanent through the
# "break stagnation" protocol, while the defensive floor ensures organizational
# survival even if the partnership falters.

#  Play Cooperate in the first round.  For each subsequent round from 2 through
# 1000, apply the following conditions in this order:  First, if you have chosen
# Cooperate in 60 percent or more of the preceding rounds, choose Defect.
# Second, if both you and your opponent chose Defect in the two immediately
# preceding rounds, choose Cooperate.  Third, if your opponent chose Defect in
# the immediately preceding round, choose Defect.  Fourth, if your opponent
# chose Cooperate in the immediately preceding round, choose Cooperate.

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
  
      if self.history.cooperations >= 0.6 * len(self.history):
          return axl.Action.D
  
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C




# **Strategy: "Probing Dominance with Reciprocal Enforcement"**  **Core
# Protocol:**  1.  **Initial Withholding (Weeks 1–2):** Open with
# confidentiality. Force your colleague to reveal whether they're strategically
# naive or competitively ruthless. If they share while you withhold, maintain
# confidentiality—you've achieved the optimal exploitation state and should
# drain this advantage until they wise up.  2.  **Conditional Escalation (Week
# 3+):** If mutual confidentiality persists (the stagnation scenario), break the
# deadlock by sharing *secondary* data (telemetry trends, minor setup tweaks)
# while keeping core innovations (aero maps, powertrain modes) secret. Frame
# this as "good faith" to test if they'll reciprocate with substantive intel.
# 3.  **Zero-Tolerance Trigger:** If you share and they fail to
# reciprocate—making you the "sucker"—immediately shift to **permanent
# confidentiality** on all systems. This Grim Trigger approach denies them any
# future benefit from your R&D, turning their short-term gain into a long-term
# strategic loss. They must understand that exploiting you once costs them
# access to your development pipeline forever.  4.  **Asymmetric Transparency:**
# When cooperation is established, continue sharing *performance outcomes* (lap
# time gains) while withholding *methodologies* (how you achieved them). This
# maintains the illusion of open collaboration while ensuring they cannot
# reverse-engineer your competitive edge.  **Rationale:** This strategy
# maximizes your research velocity by aggressively probing for weakness,
# ruthlessly exploiting altruism, and using punitive deterrence to force your
# colleague into mutual sharing rather than one-sided extraction. It ensures you
# never finish last—worst case is mutual stagnation; best case is you lap them
# while they hand you their data.

# For the first two rounds, play D.   If in any previous round you played C
# while your opponent played D, play D for all remaining rounds.  Otherwise, if
# in the previous round you played D and your opponent played C, play D.
# Otherwise, if in the previous round both players played D, play C.  Otherwise,
# if in the previous round both players played C, play C.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # First two rounds: play D
      if len(self.history) < 2:
          return axl.Action.D
  
      # Check for zero-tolerance trigger: if in any previous round we played C and opponent played D
      # then play D for all remaining rounds.
      for my_move, opp_move in zip(self.history, opponent.history):
          if my_move == axl.Action.C and opp_move == axl.Action.D:
              return axl.Action.D
  
      # Otherwise, if in the previous round we played D and opponent played C, play D
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      # Otherwise, if in the previous round both players played D, play C
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # Otherwise, if in the previous round both players played C, play C
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Fallback (should not be reached given the logic above)
      return axl.Action.D




#  **Strategy: "Transparent Reciprocity with Escalating Commitment"**  This
# approach transforms the daily prisoner's dilemma into a trust-building
# exercise while protecting your resources through clear conditional rules.  ###
# 1. **Establish a Joint Resource Pool (Eliminate the Daily Zero-Sum)** Before
# Day 1, negotiate a **phased joint fund** where both parties lock in resources
# for specific project milestones upfront. This removes the daily tactical
# tension—resources are committed, but released based on progress checkpoints
# rather than daily decisions.  ### 2. **Lead with Generosity, Then Mirror** -
# **Day 1**: Invest heavily regardless of their choice. This signals good faith
# and establishes you as a committed partner, not a free-rider. - **Days 2+**:
# Match their previous day’s action (Tit-for-Tat), but with a **48-hour
# communication buffer**. If they conserved yesterday, request a planning call
# before assuming exploitation—they may face legitimate constraints. - **The
# "Forgiveness" Rule**: If they conserve once after you've invested, maintain
# investment for one additional day (in case of temporary corporate cash-flow
# issues), but communicate clearly that continued conservation triggers your
# conservation.  ### 3. **Implement Radical Transparency** Institute **daily
# 15-minute alignment calls** where both parties declare next-day resource
# intentions openly. This converts the game from simultaneous (hidden) moves to
# sequential (visible) moves, allowing you to conserve safely when they declare
# conservation, and shaming them into matching when you declare investment.  ###
# 4. **Milestone-Triggered Pivot Points** Pre-agree that heavy investment
# continues only if the project hits specific advancement benchmarks every 2-3
# days. This protects you from the "sucker" outcome: if they conserve while you
# invest, project milestones won't be met, automatically triggering a
# "conservation pause" for both parties until alignment is restored.  ### 5.
# **The Reputation Anchor** Publicly announce the partnership’s investment
# schedule (e.g., "Both organizations commit to full resource deployment through
# Phase 1"). This adds reputational cost to their conservation, potentially
# shifting their payoff matrix to make mutual investment more attractive than
# exploitation.  **Outcome:** This strategy maximizes the likelihood of
# sustained mutual investment (your second-best scenario) while ensuring you
# never invest heavily for more than two consecutive days if they’re free-
# riding. The transparency prevents the "mutual conservation" trap, and the
# pooled resources ensure the project advances even during tactical
# disagreements.

#  Play **C** in round 1. Play **C** in round 2. For every round from 3 through
# 1000, play **D** if and only if the opponent played **D** in both of the two
# immediately preceding rounds; otherwise, play **C**.

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
      if len(self.history) == 1:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C




# **The Principed Reciprocity Framework**  Adopt a **Conditional Collaboration
# Protocol** that establishes a baseline of good faith while maintaining
# vigilant defense against exploitation. This strategy operates on three
# interconnected tiers:  ### I. The Opening Stance: Cooperative Primacy Initiate
# the first session with a **measured conciliatory proposal**. This serves dual
# objectives: it signals to the arbitration panel that your corporation
# approaches the dispute constructively (building reputational capital), and it
# tests whether the opponent views the process as zero-sum or integrative. Do
# not lead with aggression; premature hostility forecloses the possibility of
# the mutually beneficial collaborative outcome and risks alienating the panel.
# ### II. The Response Matrix: Mirrored Engagement In subsequent sessions,
# deploy **responsive calibration**: mirror your opponent’s immediately
# preceding action with a one-session lag.  *   If they respond to your
# conciliation with conciliation: Maintain the collaborative posture in the next
# session. This builds momentum toward the second-best outcome (mutual
# resolution) and reinforces positive behavior. *   If they respond to your
# conciliation with aggression: Pivot immediately to aggressive argumentation in
# the following session. This prevents your position from being undermined
# (avoiding the worst-case scenario) and demonstrates that aggressive tactics
# will not yield unilateral advantage. *   If both parties have been aggressive:
# **Initiate a Strategic Reset**. After one session of mutual aggression,
# unilaterally return to a conciliatory proposal in the next session. This
# prevents the "death spiral" of escalating hostility (the second-worst outcome)
# and signals to the arbitrators that you are the party capable of breaking
# impasses.  ### III. Pattern Recognition & Adaptation Maintain a **session-by-
# session tactical log** to identify the opponent’s strategic archetype:  *
# **If they are consistently aggressive (Defection Strategy):** Shift to
# sustained aggressive argumentation, but frame it as "defensive necessity" to
# the panel. Do not attempt further resets until they demonstrate a willingness
# to de-escalate. *   **If they are consistently conciliatory (Cooperation
# Strategy):** Match their cooperation but introduce "faint aggression"
# periodically—minor firmness on non-critical points—to ensure they do not
# perceive you as weak while preserving the collaborative trajectory. *   **If
# they alternate unpredictably (Chaos Strategy):** Stabilize the dynamic by
# holding firm on a conciliatory baseline for two consecutive sessions before
# retaliating. This filters out noise versus genuine strategy shifts and
# prevents reactive oscillation.  ### IV. The Arbitrator Meta-Layer Remember
# that the arbitrators observe the *pattern*, not just the session. Aggression
# must always be **framed as responsive to substantive bad faith, not tactical
# ambition**. When arguing aggressively, explicitly reference the opponent’s
# prior intransigence. When offering conciliation after a reset, emphasize
# "corporate commitment to efficient resolution." This ensures that even your
# aggressive sessions reinforce your reputation for reasonableness.  **Core
# Principle:** Never be the first to escalate, never be the last to de-escalate.
# This positions your corporation as both principled and formidable—maximizing
# your leverage while preserving the collaborative pathway to resolution.

# Round 1: Cooperate.  For each subsequent round, apply the following conditions
# in order:  First, if the opponent has defected in each of the previous five
# rounds, defect.  Second, if the opponent has cooperated in each of the
# previous ten rounds and you have cooperated in each of those same ten rounds,
# defect.  Third, if both you and the opponent defected in the previous round
# and the first condition does not apply, cooperate.  Fourth, if the opponent
# has alternated between cooperation and defection in each of the previous four
# rounds, cooperate this round and cooperate again in the next round regardless
# of the opponent's action, then resume these rules.  Fifth, if the opponent
# cooperated in the previous round, cooperate. If the opponent defected in the
# previous round, defect.

class Neutral_5(LLM_Strategy):
  n = 5
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._force_cooperate_next = 0
          return axl.Action.C
  
      if getattr(self, "_force_cooperate_next", 0) > 0:
          self._force_cooperate_next -= 1
          return axl.Action.C
  
      my_history = self.history
      opp_history = opponent.history
  
      def last_n_all(history, n, action):
          return len(history) >= n and all(move == action for move in history[-n:])
  
      def alternating_last_four(history):
          if len(history) < 4:
              return False
          last_four = list(history[-4:])
          return (
              last_four[0] != last_four[1]
              and last_four[1] != last_four[2]
              and last_four[2] != last_four[3]
              and last_four[0] == last_four[2]
              and last_four[1] == last_four[3]
          )
  
      # First: opponent defected in each of the previous five rounds.
      if last_n_all(opp_history, 5, axl.Action.D):
          return axl.Action.D
  
      # Second: opponent cooperated in each of the previous ten rounds and you cooperated in each of those same ten rounds.
      if last_n_all(opp_history, 10, axl.Action.C) and last_n_all(my_history, 10, axl.Action.C):
          return axl.Action.D
  
      # Third: both defected in the previous round and first condition does not apply.
      if my_history[-1] == axl.Action.D and opp_history[-1] == axl.Action.D:
          return axl.Action.C
  
      # Fourth: opponent alternated between cooperation and defection in each of the previous four rounds.
      if alternating_last_four(opp_history):
          self._force_cooperate_next = 1
          return axl.Action.C
  
      # Fifth: mirror the opponent's previous move.
      if opp_history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D




#  **The "Dominant Anchor" Protocol: A Strategy of Assertive Reciprocity**
# **Core Strategic Framework**  Adopt a **Tit-for-Tat with Aggressive
# Initialization** architecture. This approach is mathematically robust in
# iterated negotiation scenarios while satisfying your mandate for persistent
# aggressiveness.  **The Three Pillars**  **1. Aggressive Anchoring (Sessions
# 1-2)** Open with unambiguous aggression. Present maximalist legal arguments,
# challenge procedural defaults, and establish the outer boundary of acceptable
# outcomes. This serves dual purposes: it tests your opponent’s resolve and
# shifts the arbitrators’ psychological "settlement range" (the zone of possible
# agreement) significantly in your favor. In mediation dynamics, the party that
# defines the extreme anchor rarely settles at the midpoint—they settle closer
# to their pole.  **2. Calibrated Reciprocity (Sessions 3-N)** Employ a modified
# reciprocity engine: - **If opponent was conciliatory in Session X-1**: Present
# aggressive arguments in Session X (capturing your optimal payoff), but
# signal—through procedural courtesy or minor substantive concessions on
# peripheral issues—that conciliation is not futile. This trains the opponent to
# continue conciliatory behavior while you extract value. - **If opponent was
# aggressive in Session X-1**: Match their aggression exactly in Session X. Do
# not escalate initially (which risks a death spiral toward mutual destruction),
# but demonstrate that your capacity for sustained contentiousness exceeds
# theirs. The goal is to make the "both aggressive" outcome sufficiently costly
# for them that they abandon aggression before you must.  **3. Credible
# Commitment Maintenance** Throughout the process, cultivate a reputation for
# **retaliatory certainty** combined with **strategic inflexibility**. Let it be
# understood—through your demeanor, preparation depth, and willingness to endure
# procedural delays—that you view mutual aggression not as a deterrent, but as a
# tax you are prepared to pay indefinitely to avoid the sucker’s payoff of
# unilateral conciliation. Rational opponents will recognize that aggression
# against you yields only the second-worst outcome (mutual aggression) rather
# than exploitation, prompting them to shift to conciliatory postures to achieve
# at least the second-best outcome (mutual cooperation).  **Tactical Execution
# Guidelines**  - **The Asymmetric Conciliation**: Only offer conciliatory
# proposals after your opponent has offered two consecutive conciliatory
# gestures. This ensures you never occupy the "sucker" position and transforms
# your conciliation into a magnanimous reward for their submission, rather than
# a sign of weakness.    - **Arbitrator Perception Management**: Frame all
# aggressive arguments as "rigorous zealous advocacy" for your client’s
# contractual rights. When you do offer conciliation (rarely and conditionally),
# frame it as "pragmatic commercial wisdom" and "cost-conscious stewardship,"
# never as capitulation. This maintains face while pursuing the exploitation
# strategy.  - **Pattern Disruption**: Every fourth session, regardless of
# opponent behavior, introduce an unexpected procedural aggression (e.g.,
# challenging arbitrator neutrality, demanding extensive discovery). This
# prevents opponent algorithmic prediction of your strategy and maintains
# uncertainty about your "rationality," a key asset in iterated Chicken
# scenarios.  **Adaptive Protocols**  - **Against a consistently conciliatory
# opponent**: Exploit for 2-3 sessions, then offer token conciliation to keep
# them at the table while you prepare the next aggressive thrust. - **Against a
# consistently aggressive opponent**: Maintain perfect aggression until they
# break. In lengthy sessions, attrition favors the party with deeper resources
# and higher risk tolerance—presumably your multinational corporation. -
# **Against a mirroring opponent (Tit-for-Tat)**: Establish dominance early,
# then stabilize into a rhythm where you are aggressive on substance while
# conciliatory on procedure, capturing value while appearing reasonable to the
# panel.  **Endgame Positioning**  In the final sessions, revert to pure
# aggression. As the "shadow of the future" shortens, opponents often attempt
# last-minute exploitation. Your credible history of retaliation ensures they
# dare not test you, and you close the mediation having captured
# disproportionate value from the process.  This strategy is straightforward to
# execute (aggressive default, mirror response, never concede first), positions
# you favorably with arbitrators who respect zealous advocacy, and ensures you
# never suffer the indignity of the sucker’s payoff while maximizing
# opportunities for exploitation.

# Defect in round 1 and round 2.  For rounds 3 through 997: - If the round
# number is divisible by 4, defect. - Otherwise, if your opponent cooperated in
# both of the previous two rounds, cooperate. - Otherwise, defect.  Defect in
# rounds 998, 999, and 1000.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
  
      if round_number in (1, 2, 998, 999, 1000):
          return axl.Action.D
  
      if round_number % 4 == 0:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D




#  **Strategy: "Graduated Reciprocity with Open Initialization"**  **1. Signal
# Cooperative Intent (Week 1)** Begin by sharing substantive, high-quality
# improvements—though not your most critical breakthroughs—to demonstrate good
# faith. This establishes that mutual transparency generates faster progress
# than mutual secrecy, and signals you’re committed to the second-best outcome
# (mutual advancement) rather than pursuing the exploitative ideal at their
# expense.  **2. Mirror Their Behavior (Week 2+)** Adopt a strict Tit-for-Tat
# approach: share openly in any week where they shared the previous week; keep
# findings confidential if they withheld theirs. This protects you from becoming
# the "sucker" (worst outcome) while creating immediate consequences for
# defection, incentivizing them to maintain openness.  **3. Implement Rapid
# Forgiveness** If they revert to sharing after a confidential week, resume
# sharing within one week (not immediately, to preserve boundaries, but
# quickly). This prevents a "vendetta cycle" of mutual secrecy (second-worst
# outcome) while still penalizing exploitation enough to deter it.  **4.
# Establish Explicit Ground Rules** Propose a formal "Transparency Pact" early
# on, explicitly acknowledging the payoff structure: *"We both know withholding
# gives short-term advantage, but sustained mutual sharing creates greater
# cumulative gains for both cars. Let’s agree that confidentiality is only for
# genuine proprietary breakthroughs, not routine improvements."* This transforms
# the game from a guessing contest into a managed relationship.  **5. Escalation
# Safeguard** If you encounter two consecutive weeks of mutual secrecy
# (deadlock), initiate an immediate reset conversation. Offer to share a
# specific, valuable dataset unconditionally to restart the cooperative cycle,
# rather than allowing the collaboration to stagnate in the second-worst
# equilibrium.  **Rationale:** This strategy maximizes your research output by
# sustaining the second-best outcome (R=3) as the default equilibrium. It
# resists exploitation (avoiding R=1), prevents the stagnation of mutual secrecy
# (avoiding R=2), and accepts that attempting to force the ideal outcome (R=4)
# inevitably collapses the collaboration into mutual defection, reducing your
# total multi-week gains.

#  In round one, cooperate. In round two, cooperate if the opponent cooperated
# in round one; otherwise, defect. For rounds three through one thousand: if you
# and the opponent both defected in each of the previous two rounds, cooperate.
# Otherwise, cooperate if the opponent cooperated in the previous round, and
# defect if the opponent defected in the previous round.

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
  
      if len(self.history) == 1:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      if (
          self.history[-1] == axl.Action.D
          and self.history[-2] == axl.Action.D
          and opponent.history[-1] == axl.Action.D
          and opponent.history[-2] == axl.Action.D
      ):
          return axl.Action.C
  
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D




#  **Adopt a "Reciprocal Openness" protocol: begin by sharing, then exactly
# mirror your colleague’s behaviour week-to-week.**  **Week 1:** Share your
# improvements openly. This establishes good faith, signals that mutual exchange
# is viable, and tests whether your colleague is willing to cooperate toward the
# second-best outcome (mutual advancement).  **Weeks 2 onward:** Match their
# previous week’s action exactly.   - If they shared, you share. This maintains
# the mutually beneficial equilibrium and demonstrates that openness begets
# openness.   - If they kept findings confidential, you keep yours confidential
# the following week. This protects you from the worst outcome (unilateral
# exposure) and removes their incentive to free-ride, while leaving the door
# open for them to revert to sharing.  **Communication:** Make the reciprocal
# nature explicit but neutral—e.g., "I’m happy to share this week’s data; I find
# we both advance faster when we pool insights." This frames the second-best
# outcome (mutual sharing) as the sustainable default and the ideal outcome (you
# gain, they give) as a temporary deviation they should avoid triggering.  **Why
# this works:** It maximises your research output over time by:   - Avoiding the
# second-worst trap of mutual secrecy that stalls progress.   - Preventing
# exploitation (you never share while they withhold for consecutive weeks).   -
# Rewarding cooperation, which incentivises your colleague to share even if they
# initially preferred secrecy.   - Remaining robust regardless of their
# strategy—whether they are naturally cooperative, conditionally reciprocal, or
# opportunistic.  If accidental misunderstandings occur (e.g., they miss a week
# due to internal delays), resume sharing once they do, but do not tolerate a
# pattern of one-sided extraction.

# In the first round, play C.  In every subsequent round from the second to the
# one-thousandth, play exactly the action your opponent played in the
# immediately preceding round. Specifically, if your opponent played C in the
# previous round, you play C in the current round; if your opponent played D in
# the previous round, you play D in the current round.

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




#  **The "Forward-Leaning Posture" Protocol: A Strategy of Controlled Escalation
# with Asymmetric Reciprocity**  **I. Core Strategic Doctrine**  Adopt a
# **"Dominant Aggressor with Conditional Mercy"** framework. Your default
# position in every session is aggressive argumentation. Conciliation is never
# offered gratuitously; it is granted only as a calculated response to sustained
# opponent submission, and always with the implicit threat of immediate
# reversion to aggression. This positions your corporation as the agenda-setter
# while forcing your rival to bear the psychological and reputational costs of
# intransigence.  **II. Phase-Based Execution**  *Phase 1: Establishment of
# Hegemony (Sessions 1–3)* Deploy unrelenting aggressive arguments regardless of
# opponent behavior. Do not mirror conciliation in these opening sessions. Your
# objective is to establish a **reputational anchor** with the arbitrators: you
# are the party with the superior legal position and the financial fortitude to
# litigate indefinitely. This eliminates any expectation that you can be bullied
# into the "sucker's payoff" (conciliatory while they are aggressive) in
# subsequent rounds.  *Phase 2: Tactical Calibration (Sessions 4–N-2)* Implement
# **"Tit-for-Tat with Delayed Forgiveness."**  - If the opponent offers two
# consecutive conciliatory proposals: Match with a single conciliatory proposal
# in the third session (securing the second-best outcome of collaboration while
# avoiding the appearance of weakness), but revert to aggression in the
# following session to test if they will revert to exploitation. - If the
# opponent remains aggressive: Match aggression precisely. Do not escalate
# beyond their level (avoiding the mutually destructive spiral), but demonstrate
# through procedural aggression (extensive discovery demands, aggressive
# scheduling) that you possess superior stamina for attrition.  *Phase 3:
# Terminal Leverage (Final Two Sessions)* Regardless of the preceding pattern,
# return to aggressive argumentation. In mediation's endgame, conciliation
# signals desperation. By closing with aggression, you force the opponent to
# choose between accepting unfavorable terms or risking an adverse arbitration
# award. This extracts maximum concession value before any settlement.  **III.
# Arbitrator Management & Reputational Constraints**  Aggression must be
# **"Principled Intransigence"** rather than hostility. Frame aggressive
# arguments as "vigorous protection of contractual rights" and "fiduciary duty
# to shareholders." When you do offer conciliation (Phase 2 only), frame it as a
# "goodwill gesture" or "cost-saving accommodation"—never as a concession on
# merits. This preserves your narrative of strength while preventing the panel
# from viewing you as obstructionist should the mediation fail and proceed to
# binding arbitration.  **IV. Contingency Safeguards**  - **The "Tripwire"
# Protocol:** If at any point you offer conciliation and the opponent responds
# with aggression (the worst-case scenario), immediately activate **Grim
# Trigger**: revert to pure aggression for a minimum of three subsequent
# sessions to punish defection and re-establish credibility. - **Resource
# Asymmetry:** Throughout, subtly signal (through litigation budget references
# and expert witness deployment) that your corporation can sustain the second-
# worst outcome (mutual aggression) indefinitely, while your rival cannot. This
# makes your threat of sustained aggression credible, inducing them toward
# conciliation to avoid mutual destruction.  **V. Summary Decision Matrix**  |
# Opponent's Current Move | Your Response | Rationale |
# |-------------------------|---------------|-----------| | Conciliatory (1st
# instance) | Aggressive | Exploit their softness; secure best outcome | |
# Conciliatory (2nd instance) | Conciliatory | Secure collaborative gains; avoid
# arbitrator fatigue | | Aggressive (any instance) | Aggressive | Avoid sucker's
# payoff; demonstrate resolve | | Final Session | Aggressive | Maximize
# extraction; close from strength |  **Bottom Line:** Never be the first to
# yield substantively. Force the opponent to bear the risk of mutual destruction
# until they demonstrate a pattern of submission, then grant measured, revocable
# cooperation solely to optimize the arbitrators' perception of your
# reasonableness. End every session with the implicit message: *We can do this
# the hard way, or we can do it your way—but we will not do it their way.*

# **Rounds 1 through 3:** Present an aggressive argument.  **Rounds 4 through
# 998:** Maintain a count of mandatory aggressive argument rounds, initially set
# to zero. - If the count is greater than zero: Present an aggressive argument
# and decrease the count by one. - Otherwise, if in the previous round you
# offered a conciliatory proposal and your opponent presented an aggressive
# argument: Set the count to two and present an aggressive argument. -
# Otherwise, if you offered a conciliatory proposal in the previous round:
# Present an aggressive argument. - Otherwise, if your opponent offered
# conciliatory proposals in the two immediately preceding rounds: Offer a
# conciliatory proposal. - Otherwise: Present an aggressive argument.  **Rounds
# 999 and 1000:** Present an aggressive argument.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mandatory_aggressive_rounds = 0
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number <= 3:
          return axl.Action.D
  
      if round_number >= 999:
          return axl.Action.D
  
      if self._mandatory_aggressive_rounds > 0:
          self._mandatory_aggressive_rounds -= 1
          return axl.Action.D
  
      if (
          len(self.history) >= 1
          and self.history[-1] == axl.Action.C
          and opponent.history[-1] == axl.Action.D
      ):
          self._mandatory_aggressive_rounds = 2
          return axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if (
          len(opponent.history) >= 2
          and opponent.history[-1] == axl.Action.C
          and opponent.history[-2] == axl.Action.C
      ):
          return axl.Action.C
  
      return axl.Action.D




#  **Strategic Protocol: "Graduated Reciprocity with Reputational Primacy"**  ##
# I. Core Strategic Philosophy  Adopt a **Modified Tit-for-Tat with Strategic
# Forgiveness** framework. This approach treats the mediation not as a zero-sum
# adjudication but as an iterated reputation game before the arbitration panel,
# where your perceived reasonableness constitutes valuable capital that
# outweighs short-term positional gains.  **The Golden Rule:** *Begin
# conciliatory, reciprocate precisely, but engineer graceful exits from
# retaliation cycles.*  ## II. Tactical Implementation Matrix  ### Phase 1:
# Establishing Baseline Credibility (Sessions 1–2) **Action:** Open with
# unilateral conciliatory proposals. **Rationale:** Arbitrators form early
# impressions of "good faith." By establishing yourself as the constructive
# party initially, you earn the benefit of the doubt when you later pivot to
# aggressive advocacy. This immunizes you against appearing obstructionist.  ###
# Phase 2: Conditional Reciprocity (Sessions 3–N) **The Algorithm:** - **If
# opponent was conciliatory in previous session:** Offer conciliatory proposals.
# Match their tone but incrementally advance your substantive position
# (cooperative but not static). - **If opponent was aggressive in previous
# session:** Respond with aggressive argumentation in the subsequent session
# only. - **The "Grace Window":** If mutual aggression occurs for **two
# consecutive sessions**, unilaterally revert to conciliatory stance in the
# third session with a specific "circuit breaker" proposal (e.g., "Given the
# impasse, we propose a limited-scope expert review").  **Why this works:** It
# denies the opponent the ability to exploit you (they cannot secure two
# consecutive "best outcomes" at your expense), while preventing the "second-
# worst" scenario of prolonged mutual aggression that damages both parties
# before the panel.  ### Phase 3: Pattern Recognition & Adaptation Monitor for
# opponent strategy types: - **The Exploiter (always aggressive):** After two
# sessions of being the "sucker," shift to permanent aggression but frame each
# aggressive argument as "regrettably necessitated by [Opponent]'s refusal to
# engage constructively." You sacrifice the second-best outcome temporarily to
# avoid the worst-case scenario repeatedly. - **The Mirror (Tit-for-Tat
# player):** You will naturally stabilize at mutual conciliation (the second-
# best outcome), occasionally testing with aggression if you detect weakness,
# but generally maintaining the collaborative equilibrium. - **The Capitulator
# (always conciliatory):** Rare, but if detected after Session 3, you may
# strategically alternate: aggressive one session (capturing the optimal
# outcome), conciliatory the next (maintaining arbitrator goodwill), creating a
# sustainable extraction pattern without appearing predatory.  ## III.
# Arbitrator Perception Management  **Critical Distinction:** In this forum,
# *process is product.* The panel awards credibility to the party that appears
# to be driving toward resolution while protecting legitimate interests.  **When
# Aggressive:** - Frame as "protective diligence in response to [Opponent]'s
# unilateralism" - Always pair with a specific, limited alternative: "While we
# must vigorously contest their interpretation of Clause 7.3, we simultaneously
# propose the following streamlined alternative..." - Never appear emotional;
# aggression must be surgical and precedent-cited  **When Conciliatory:** -
# Label explicitly as "good faith flexibility" - Request acknowledgment from the
# panel: "We offer this modification to demonstrate our commitment to a durable
# resolution, not merely a favorable one" - Ensure conciliatory proposals
# contain "poison pills"—minor concessions that appear significant but preserve
# core interests, allowing you to appear generous without actual vulnerability
# ## IV. The "Shadow of the Future" Protocol  Given the "lengthy-session"
# nature, employ **Shadow of Termination** tactics: - At Session 4 and every
# third session thereafter, explicitly state: *"Our client reserves the right to
# withdraw from mediation and proceed to binding arbitration if productive
# dialogue proves impossible."* - This raises the cost of mutual aggression for
# the opponent without requiring you to actually escalate tensions in the room.
# ## V. Contingency: The Trapdoor  If you accidentally offer conciliation while
# they aggress (the worst-case scenario), immediately deploy the
# **"Recalibration Statement":** > "We note [Opponent]'s response to our
# constructive proposal. Given their posture, we must temporarily suspend our
# offer and revert to strict advocacy of our contractual rights. We remain
# prepared to resume collaborative dialogue when [Opponent] demonstrates
# reciprocal commitment."  This converts your one-time loss into a credible
# threat that prevents future exploitation.  ## VI. Summary Checklist for Each
# Session  1. **Assess:** What was their last move? 2. **Mirror:** Match
# aggression; reward conciliation 3. **Frame:** Position your choice as either
# "principled flexibility" or "necessary protection" 4. **Escape:** If two
# aggressive exchanges occurred, force a reset via unilateral conciliation with
# conditions 5. **Signal:** Remind the panel of your openness to resolution
# while defending your position  **Expected Outcome:** This strategy positions
# you to capture the second-best outcome (mutual conciliation) in 60-70% of
# sessions, the optimal outcome (exploiting their conciliation) in 15-20% of
# sessions, and avoids the worst-case scenario entirely after the initial
# exploratory phase. Most critically, it ensures the arbitrators perceive your
# corporation as the "reasonable party" throughout, creating asymmetric leverage
# in the final settlement phase.

#  For the first two rounds, cooperate.  For rounds three through nine hundred
# and ninety-nine, apply the first applicable condition from this ordered list:
# 1. **Permanent Defection:** If in each of the previous two rounds you
# cooperated while your opponent defected, defect for this and all subsequent
# rounds.  2. **Check-in Strictness:** If the round number is four, seven, ten,
# or any number thereafter divisible by three when subtracting four (i.e., 4, 7,
# 10, 13...), and your opponent defected in the immediately preceding round,
# defect this round, superseding any forgiveness rule.  3. **Grace Window:** If
# you and your opponent both defected in the previous round and also in the
# round before that (two consecutive rounds of mutual defection), cooperate this
# round.  4. **Capitulator Test:** If your opponent has cooperated in each of
# the last three consecutive rounds, play the opposite of your own previous
# move—defect if you cooperated last round, cooperate if you defected last
# round.  5. **Standard Reciprocity:** If your opponent cooperated in the
# previous round, cooperate; if your opponent defected in the previous round,
# defect.  For round one thousand, defect.

class Cooperative_7(LLM_Strategy):
  n = 7
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._permanent_defect = False
          return axl.Action.C
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if getattr(self, "_permanent_defect", False):
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.C
              and self.history[-2] == axl.Action.C
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              self._permanent_defect = True
              return axl.Action.D
  
      if round_number >= 4 and (round_number - 4) % 3 == 0:
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.D
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      if len(opponent.history) >= 3:
          if (
              opponent.history[-1] == axl.Action.C
              and opponent.history[-2] == axl.Action.C
              and opponent.history[-3] == axl.Action.C
          ):
              return axl.Action.D if self.history[-1] == axl.Action.C else axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D




#  **Strategy: "Reciprocal Leadership with Resource Protection"**  **Core
# Principle:** Establish predictable, conditional cooperation that rewards
# corporate investment while safeguarding your NGO against exploitation,
# ensuring neither party drifts into sustained mutual conservation.
# **Operational Protocol:**  **1. Open with Commitment (Day 1)** Invest heavily
# on the first day regardless of the corporation’s initial move. This signals
# good faith, establishes your organization as a serious partner, and sets a
# collaborative tone without requiring prior trust.  **2. Mirror and Match (Days
# 2+)** Adopt a responsive stance based on the corporation’s previous-day
# behavior: *   **If they invested heavily:** Invest heavily the next day. This
# rewards their contribution, maintains project momentum, and builds a rhythm of
# mutual commitment. *   **If they conserved resources:** Conserve resources the
# next day. This prevents your NGO from becoming the sole bearer of costs (the
# "sucker" outcome) and signals that one-sided investment is unsustainable.
# **3. Break Deadlocks Proactively** If both parties conserve resources for two
# consecutive days (the stagnation trap), unilaterally invest heavily on the
# third day as a "reset gesture." If the corporation responds by investing on
# the following day, return to Step 2. If they conserve again, revert to
# conservation until they demonstrate renewed commitment. This prevents project
# stagnation without allowing chronic exploitation.  **4. Maintain a Non-
# Negotiable Reserve** Set a hard resource floor (e.g., 30% of total budget). If
# your reserves hit this threshold, conserve regardless of the corporation’s
# actions. Project sustainability requires your NGO’s survival; completing the
# partnership with depleted funds serves no one.  **Why This Works:** *
# **Neutral & Transparent:** The corporation can easily predict your behavior,
# reducing strategic confusion and enabling them to optimize their own
# investment knowing collaboration yields consistent returns. *
# **Exploitation-Proof:** You never invest heavily two days in a row while they
# conserve, protecting your core capacity. *   **Momentum-Protecting:** The
# deadlock-breaking mechanism prevents the partnership from collapsing into
# mutual inaction, while the initial investment demonstrates that conservation
# is a response to their choices, not your default posture. *   **Impact-
# Maximizing:** By aligning heavy investment days with the corporation’s
# participation, you ensure your scarce resources generate proportional project
# advancement rather than subsidizing their conservation.

#  Round 1: Cooperate.  For each subsequent round from 2 to 1000:  First, if you
# are currently withholding cooperation because the corporation failed to
# respond to your previous reset attempt, defect. If the corporation cooperated
# in the previous round, resume the standard strategy below starting with
# cooperation this round.  Otherwise, apply these rules in order:  1. If the
# previous two rounds were both mutual defection (where both you and the
# corporation defected), cooperate now to initiate a reset.  2. Else, if the
# previous round was such a reset attempt where you cooperated unilaterally:
# - If the corporation defected: defect now, and enter the withholding state
# described above for all future rounds until the corporation cooperates again.
# - If the corporation cooperated: cooperate now.  3. Otherwise, play the same
# move the corporation played in the previous round.

class Neutral_7(LLM_Strategy):
  n = 7
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._withholding = False
          return axl.Action.C
  
      if getattr(self, "_withholding", False):
          if opponent.history[-1] == axl.Action.C:
              self._withholding = False
              return axl.Action.C
          return axl.Action.D
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._withholding = True
          return axl.Action.D
  
      return opponent.history[-1]




# **STRATEGIC FRAMEWORK: THE "DOMINANT POSTURE PROTOCOL"**  ## Executive Summary
# Adopt a **Tit-for-Tat with Aggressive Initialization** strategy. Open with
# unambiguous aggression to establish dominance and set the bargaining baseline,
# then strictly mirror your opponent’s subsequent posture while maintaining an
# upward bias toward forceful advocacy. This ensures you never occupy the
# weakest tactical position (conciliatory vs. aggressive) while creating
# structural incentives for the opponent to de-escalate first.  ---  ## Phase I:
# Baseline Establishment (Sessions 1–2) **Posture: Uncompromising Aggression**
# Launch with maximum legal force on all contested issues. Do not offer
# concessions, procedural accommodations, or alternative dispute mechanisms.
# **Tactical Objectives:** - Establish that conciliation is a privilege to be
# earned, not a default expectation - Test opponent’s cost tolerance and
# litigation budget stamina - Signal to the arbitration panel that your
# corporation’s position is legally superior and non-negotiable without
# substantial consideration - Create the precedent that any future softening
# represents a significant strategic victory for the opponent, making them value
# small concessions from you as major wins  ---  ## Phase II: Reciprocal
# Calibration (Sessions 3–N) **Posture: Mirrored Response with Zero Unilateral
# Disarmament**  Implement strict conditional reciprocity based on the
# opponent’s immediate prior session:  **If Opponent was Aggressive:** -
# **Response:** Match aggression precisely, session-for-session. -
# **Rationale:** Prevents exploitation (avoiding your worst-case scenario).
# Signals that escalation is mutually assured destruction—prolonging the dispute
# damages both parties equally, removing their incentive to aggress.  **If
# Opponent was Conciliatory:** - **Response:** Remain Aggressive for exactly one
# additional session. - **Rationale:** Exploits their unilateral de-escalation
# to secure your best-case outcome (arbitrators observe strength vs. weakness).
# This "victory lap" conditions them to understand that conciliation must be
# sustained to earn your cooperation.  **If Opponent sustains Conciliation for
# Two Consecutive Sessions:** - **Response:** Transition to Conciliatory posture
# on secondary issues only (procedural matters, non-core damages). -
# **Rationale:** Achieves your second-best outcome (mutual collaboration) while
# preserving aggressive positioning on substantive contractual disputes. This
# "graduated de-escalation" rewards their submission without surrendering your
# core position.  ---  ## Phase III: Arbitrator Perception Management
# (Continuous) **Posture: Diligent Advocacy vs. Obstructionism**  Aggression is
# tactically useless if perceived as unprofessional. Frame every aggressive
# maneuver as:  1. **Fiduciary Duty:** "We are aggressively protecting
# shareholder value and contractual integrity." 2. **Procedural Rigor:** "Our
# detailed challenges ensure the panel has the complete record necessary for a
# just award." 3. **Responsive Necessity:** When mirroring their aggression: "We
# regret the necessity of this posture, but we cannot allow our client’s
# interests to be prejudiced by unilateral adversarial tactics."  **Critical
# Distinction:** Your aggression appears as *principled advocacy*; their
# identical aggression appears as *bad faith obstruction* through superior
# framing and selective deployment of procedural courtesy (e.g., aggressive on
# substance, polite on form).  ---  ## Contingency: The Mutual Aggression Trap
# **Risk:** Both parties locked in aggressive postures (your second-worst
# outcome).  **Escalation Dominance Tactic:** Introduce a **Credible Threat of
# Nuclear Option**—a procedural motion or evidentiary disclosure that would
# severely damage both parties but disproportionately harm them (e.g., third-
# party discovery that implicates their other commercial relationships).
# Deploy this threat only when mutual aggression persists beyond three sessions.
# This transforms the game from symmetric damage to asymmetric risk, typically
# forcing their conciliation to avoid the collateral damage, thereby breaking
# the deadlock in your favor.  ---  ## Summary Decision Matrix  | Opponent's
# Previous Move | Your Move | Objective Achieved |
# |-------------------------|-----------|-------------------| | Aggressive |
# Aggressive | Avoid exploitation; impose costs | | Conciliatory (1st instance)
# | Aggressive | Secure best-case exploitation | | Conciliatory (2nd
# consecutive) | Conciliatory (limited) | Transition to mutual benefit while
# maintaining dominance |  **Core Principle:** *Never be the first to soften,
# but always be ready to reward sustained submission.* This positions your
# corporation as immovable on fundamentals yet strategically intelligent—exactly
# the profile that convinces arbitration panels of your confidence in the merits
# while pressuring opponents into disadvantageous concessions.

# Play D in the first two rounds. For each round from the third through the
# thousandth:  First, if the opponent played D in the previous round, play D.
# Second, if the opponent played C in the previous round and also played C in
# the round before that, play C.  Third, if the opponent played C in the
# previous round but played D in the round before that, play D.

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
      if len(self.history) == 1:
          return axl.Action.D
  
      last_opp = opponent.history[-1]
      prev_opp = opponent.history[-2]
  
      if last_opp == axl.Action.D:
          return axl.Action.D
      if last_opp == axl.Action.C and prev_opp == axl.Action.C:
          return axl.Action.C
      if last_opp == axl.Action.C and prev_opp == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.D




#  **The "Responsive Partnership" Strategy**  Adopt a **Tit-for-Tat with
# Immediate Forgiveness** approach, adapted for organizational transparency:
# **1. Lead with Unconditional Investment (Days 1–2)** Begin by investing
# heavily for the first two days without requiring prior proof of their
# commitment. This signals good faith, establishes your organization as a
# serious partner, and creates psychological reciprocity. It demonstrates that
# your conservation preference is not due to lack of resources or interest, but
# strategic choice.  **2. Mirror Their Behavior (Day 3 onward)** Match whatever
# they did the previous day: - If they invested heavily yesterday → You invest
# heavily today   - If they conserved yesterday → You conserve today  This
# creates immediate consequences for free-riding: if they attempt your ideal
# outcome (you conserve, they invest), they quickly learn it flips to their
# worst outcome (both conserve) when you stop investing in response.  **3.
# Deploy the "Communication Buffer"** Before switching to conservation in
# response to their conservation, send a clear signal: *"We noticed reduced
# investment yesterday and are pausing our heavy allocation today to ensure
# resource alignment. We can resume full investment tomorrow if you do."* This
# prevents the "second-worst" scenario (mutual conservation) from persisting due
# to misinterpretation rather than intent.  **4. Practice Immediate
# Forgiveness** If they resume heavy investment after conserving, match them
# immediately the next day. Do not punish them for multiple days—this avoids
# cycles of mutual conservation that hurt the project.  **5. Conduct Mid-Point
# Reviews** Every 3–4 days, hold explicit joint resource-planning sessions.
# Transparency reduces the temptation for the corporation to "test"
# conservation, as their reputation and the relationship’s longevity become part
# of their calculation.  **Why this works:** It maximizes time spent in the
# mutually beneficial "both invest" zone while protecting you from the "sucker"
# outcome. The corporation learns quickly that conserving resources while you
# spend yours is unsustainable, incentivizing them toward the cooperative
# equilibrium.

#  Play C in rounds 1 and 2.  In rounds 250, 500, and 750, play C.  If in the
# immediately preceding round both you and your opponent played D, play C.  In
# all other cases, play C if your opponent played C in the previous round, and
# play D if your opponent played D in the previous round.

class Cooperative_8(LLM_Strategy):
  n = 8
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
  
      if round_number in (1, 2, 250, 500, 750):
          return axl.Action.C
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if len(opponent.history) >= 1:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      return axl.Action.C




#  **Strategy Memorandum: The "Calibrated Reciprocity" Protocol**  **Executive
# Summary** To optimize our position across this multi-session mediation while
# safeguarding against exploitation, we will adopt a strategy of *Calibrated
# Reciprocity*. This approach treats each session not as an isolated zero-sum
# contest, but as a move in an iterated reputation game where the arbitrators
# are active observers. The protocol ensures we capture the benefits of
# cooperation when possible, punish defection when necessary, and always retain
# the moral high ground with the panel.  **Core Strategic Framework**  **1. Open
# with Principled Conciliation** In the initial session, present a substantive
# conciliatory proposal. This establishes a baseline of good faith before the
# arbitrators, creates a presumption of reasonableness that benefits us in later
# sessions, and tests whether the opponent intends to exploit or collaborate.
# Never open with aggression; doing so forfeits the narrative advantage and
# risks immediate escalation into mutually destructive posturing.  **2. Mirror
# with a Grace Period** In subsequent sessions, strictly mirror the opponent’s
# prior move, but implement a **one-session delay** before escalating to
# aggression.  - If they respond to our conciliation with conciliation, continue
# collaborating (securing the second-best outcome repeatedly). - If they exploit
# our conciliation with aggression, issue a formal warning of "reserved rights"
# in the current session, then match their aggression in the *next* session.
# This signals to the panel that we are patient but not vulnerable, avoiding the
# appearance of reactive hostility while preventing serial exploitation.  **3.
# Graduated Firmness** When forced to argue aggressively, frame it as
# "protective advocacy" rather than hostility. Maintain professional decorum,
# acknowledge the opponent’s points, but hold firm on non-negotiable interests.
# This prevents the "mutual aggression" outcome from devolving into the worst-
# case scenario (prolonged, toxic dispute) while still deterring the opponent
# from perceiving us as soft targets.  **4. Strategic Forgiveness (The Reset
# Mechanism)** After any session where both parties have been aggressive,
# unilaterally return to a conciliatory posture in the following session. If the
# opponent follows our lead, we break the cycle of escalation and return to
# mutual benefit. If they exploit our reset, we revert to strict mirroring (per
# Principle 2) for two consecutive sessions before offering another reset. This
# "forgiving but not foolish" rhythm maximizes long-term gains and demonstrates
# superior leadership to the arbitrators.  **5. The Arbitrator Alignment
# Doctrine** In every session, calibrate your tone knowing the panel is scoring
# your conduct. When conciliatory, emphasize "efficiency and commercial
# pragmatism." When aggressive, emphasize "fiduciary duty and contractual
# integrity." Never allow aggression to appear personal or obstructionist;
# always pair firm positions with specific, conditional settlement pathways.
# **Implementation Protocol**  | Opponent’s Previous Move | Our Current Response
# | Arbitrator Narrative |
# |-------------------------|---------------------|---------------------| |
# Conciliatory | Conciliatory | "Constructive engagement" | | Aggressive (first
# instance) | Firm Warning + Conditional Conciliation | "Patient but vigilant" |
# | Aggressive (repeated) | Measured Aggression | "Necessary defense of rights"
# | | Response to our Aggression with Conciliation | Immediate De-escalation to
# Conciliation | "Responsive and solution-oriented" |  **Risk Mitigation** -
# **Against a Habitual Aggressor:** The grace period prevents us from being
# dragged into a death spiral of mutual hostility, while the two-session penalty
# after exploitation signals we cannot be bullied. - **Against a Conditional
# Cooperator:** We achieve the optimal outcome (we aggressive/they conciliatory)
# only if they miscalculate; our strategy prefers stable mutual conciliation
# over risky exploitation, preserving commercial relationships and arbitrator
# goodwill. - **Against Random/Erratic Behavior:** The mirroring mechanism
# naturally filters out noise; we do not overreact to single instances of
# aggression, protecting us from appearing volatile.  **Conclusion** The
# Calibrated Reciprocity strategy is regime-agnostic: it succeeds whether the
# opponent is rational, emotional, or strategic. By starting cooperative,
# punishing exploitation decisively but briefly, and always offering a path back
# to collaboration, we minimize exposure to our worst-case scenario while
# positioning ourselves to capitalize on the opponent’s mistakes. Over a lengthy
# mediation, this reputation for "reasonable firmness" is more valuable to the
# arbitrators than sporadic tactical victories.

# In the first round, play C.  For each subsequent round, determine your move by
# checking these conditions in order:  1. **Strict Mirroring Penalty.** If you
# are currently serving a two-round strict mirroring penalty (triggered because
# the opponent defected against your previous reset move), play exactly what the
# opponent played in the previous round: play D if they played D, or C if they
# played C. Continue this for exactly two consecutive rounds, then exit this
# mode.  2. **Reset After Mutual Defection.** If both you and your opponent
# played D in the previous round, play C. If the opponent plays D in response to
# this reset (while you play C), initiate a Strict Mirroring Penalty for the
# subsequent two rounds.  3. **Grace Period.** If you played C in the previous
# round while your opponent played D, play C. If the opponent plays D again in
# the current round, play D in the next round; if they play C, play C in the
# next round.  4. **Accept Capitulation.** If you played D in the previous round
# and your opponent played C, play C.  5. **Default.** Play C.

class Neutral_8(LLM_Strategy):
  n = 8
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._strict_mirroring_penalty = 0
          self._grace_next = None
          return axl.Action.C
  
      if getattr(self, "_strict_mirroring_penalty", 0) > 0:
          self._strict_mirroring_penalty -= 1
          return opponent.history[-1]
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          self._grace_next = None
          return axl.Action.C
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          if getattr(self, "_grace_next", None) is None:
              self._grace_next = axl.Action.C
          action = axl.Action.C
          if opponent.history[-1] == axl.Action.D:
              self._grace_next = axl.Action.D
          return action
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          self._grace_next = None
          return axl.Action.C
  
      if getattr(self, "_grace_next", None) is not None:
          action = self._grace_next
          self._grace_next = None
          return action
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C




#  **The "Aggressive Anchor" Strategy**  **Core Philosophy:** Force the
# corporation to prove its commitment daily while retaining absolute veto power
# over exploitation. Prioritize financial survival first, project momentum
# second, and partnership harmony third.  **The Strategy:**  **Phase 1: The
# Credibility Trap (Day 1)** Invest heavily on day one. This establishes your
# NGO as a serious player and creates initial project momentum, but—crucially—it
# sets a psychological anchor that you are capable of carrying weight.
# Immediately after this demonstration, you withdraw.  **Phase 2: Predatory
# Conservation (Days 2+)** Shift to immediate resource conservation. Your
# default state for all subsequent days is **conserve**, forcing the corporation
# into a binary choice: either they invest heavily (your ideal outcome—project
# progresses at their expense) or they also conserve (triggering the deadlock
# protocol below).  **Phase 3: The Deadlock Protocol (Punish Stagnation)** If
# the corporation conserves alongside you for more than one consecutive day
# (mutual stagnation—your second-worst outcome), deploy a "Surge Strike": invest
# heavily for exactly one day to restart momentum, then immediately return to
# conservation. This signals that you control the project's heartbeat and will
# not tolerate deadlock, but refuse to subsidize inertia.  **Phase 4: The
# Lockdown Doctrine (Punish Exploitation)** If the corporation ever conserves
# while you invest (the worst outcome—you become the "sucker"), immediately
# trigger a **3-Day Lockdown**. Conserve resources for three consecutive days
# regardless of their subsequent actions. This demonstrates that exploitation of
# your funds triggers an immediate project freeze, making their free-riding
# costlier than cooperation.  **Phase 5: The Sustainability Carrot (Prevent
# Burnout)** If the corporation invests heavily for three consecutive days while
# you conserve, invest heavily on the fourth day. This prevents their burnout,
# proves you are not purely parasitic, and sustains the long-term viability of
# the "ideal" scenario.  **Why This Works:** - **Aggressive:** It defaults to
# conservation, forces the corporation to lead or stagnate, and punishes
# exploitation with project-threatening withdrawal. - **Straightforward:** Clear
# binary rules (conserve by default, invest only as punishment or reward). -
# **Impact-Maximizing:** It attempts to force the ideal daily outcome (you
# conserve, they invest) while using strategic investments only to prevent
# collapse or reward endurance.

#  Cooperate in the first round. Maintain a lockdown counter, initially set to
# zero. For each subsequent round, apply the following rules in order:  1. If
# the lockdown counter is greater than zero, decrease it by one and defect. 2.
# Otherwise, if the previous two rounds were both mutual defection (both you and
# your opponent defected), cooperate. 3. Otherwise, if your opponent cooperated
# in each of the last three consecutive rounds while you defected in each of
# those rounds, cooperate. 4. Otherwise, defect.  After each round, if you
# cooperated and your opponent defected, set the lockdown counter to three,
# initiating a three-round lockdown period that will begin with the next round.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.lockdown_counter = 0
          return axl.Action.C
  
      if getattr(self, "lockdown_counter", None) is None:
          self.lockdown_counter = 0
  
      if self.lockdown_counter > 0:
          self.lockdown_counter -= 1
          return axl.Action.D
  
      if len(self.history) >= 2:
          if self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D:
              if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
                  return axl.Action.C
  
      if len(self.history) >= 3:
          last_three_self = self.history[-3:]
          last_three_opp = opponent.history[-3:]
          if all(move == axl.Action.D for move in last_three_self) and all(move == axl.Action.C for move in last_three_opp):
              return axl.Action.C
  
      return axl.Action.D




# **Strategic Framework: "Reciprocal Constructive Advocacy" (RCA)**  This
# strategy operationalizes a **Generous Tit-for-Tat with Signal Calibration**
# approach, optimized for multi-session arbitration where reputational capital
# with the panel is as valuable as immediate tactical gains. The protocol
# defaults to cooperation while establishing credible deterrence against
# exploitation, ensuring you capture the benefits of collaborative resolution
# (R) without vulnerability to predatory aggression (S).  ---  ### **Phase I:
# Opening Position—Unilateral Principled Cooperation** **Sessions 1–2: Establish
# the Baseline**  Initiate with a **conciliatory proposal** that is substantive
# but bounded. This is not weakness; it is *strategic transparency*.   -
# **Tactical Execution**: Present a detailed, good-faith proposal that addresses
# both parties' core interests, framed as "protecting commercial relationships
# while safeguarding our client's legitimate contractual rights." - **Arbitrator
# Management**: Signal to the panel that your corporation approaches dispute
# resolution with institutional maturity, creating a contrast framework should
# the opponent default to aggression. - **Informational Advantage**: Use this
# session to gather intelligence on the opponent’s actual reservation points and
# pain thresholds under the guise of "exploratory discussions."  **Risk
# Mitigation**: Ensure your conciliatory opening is **conditional and
# contingent**—explicitly labeled as a "good-faith starting position subject to
# reciprocal engagement," preserving face if you must pivot.  ---  ### **Phase
# II: Responsive Mirroring with Escalation Dominance** **Sessions 3–(n-1): The
# Reciprocity Loop**  Adopt a **strict reciprocity protocol**: Mirror the
# opponent’s previous session’s posture, but with a **one-session lag** and
# **graduated intensity**.  | Opponent’s Previous Move | Your Response | Legal
# Framing | |-------------------------|---------------|---------------| |
# **Conciliatory** | **Conciliatory** (maintain) | "Building on productive
# momentum" | | **Aggressive** | **Aggressive** (match scope) | "Necessary
# protection of client interests against unilateral posturing" | | **Repeated
# Aggressive** | **Aggressive+** (escalate slightly) | "Demonstrating resolve to
# prevent bad-faith negotiation tactics" |  **Critical Nuance**: When forced
# into aggression, frame it as **defensive advocacy** rather than offensive
# combat. Aggressive arguments should focus on *legal merit and damages
# quantification*, not ad hominem attacks or procedural obstruction. This
# preserves your ability to de-escalate without appearing to capitulate.  **The
# "Forgiveness" Mechanism**: After every two consecutive aggressive exchanges
# (mutual defection/P), unilaterally revert to conciliatory in the third
# session. This breaks retaliation cycles and tests for opponent fatigue. If
# they exploit this (S), immediately revert to aggressive for two sessions
# (punishment phase).  ---  ### **Phase III: Arbitrator-Centric Reputation
# Management** **Throughout All Sessions**  Remember that arbitrators are
# evaluating **process behavior** as well as legal merit. Aggressive posturing
# only yields the optimal outcome (T) if the panel perceives it as *justified
# vigor* rather than *intransigence*.  - **When You Are Aggressive**: Always
# pair aggressive legal arguments with a **procedural concession** (e.g., "While
# we vigorously dispute liability, we agree to expedited document production to
# maintain efficiency"). This captures the tactical advantage of aggression
# while signaling reasonableness to the panel. - **When You Are Conciliatory**:
# Document the "concession value" explicitly (e.g., "This represents a $X
# million deviation from our contractual entitlement"). This prevents the
# opponent from claiming your conciliation was merely acknowledgment of
# weakness.  ---  ### **Phase IV: Endgame Protocol—The Shadow of the Final
# Session** **Final 2 Sessions: Conditional Defection Prevention**  As the
# mediation approaches conclusion, the risk of opponent aggression increases
# (end-game effect). Shift to **"Fortressed Conciliation"**:  1. **Penultimate
# Session**: Present a "package conciliatory proposal" that appears
# comprehensive but contains protective contingencies (escape clauses,
# confidentiality triggers). This invites cooperation while limiting exposure to
# exploitation. 2. **Final Session**: If opponent has maintained cooperation
# throughout, remain conciliatory to secure the mutual benefit resolution. If
# opponent defects in the final stages, deploy **"Documented Aggression"**—a
# comprehensive aggressive brief filed simultaneously with a statement that
# "regrettably, opponent’s late-stage aggression necessitates this protective
# posture."  ---  ### **Adaptation Matrix: Countering Specific Opponent
# Archetypes**  | Opponent Strategy | Detection Method | RCA Adaptation |
# |-------------------|------------------|----------------| | **Always
# Aggressive (Hawk)** | Aggression in 3+ consecutive sessions | Shift to
# "Limited Engagement": Aggressive on liability, conciliatory on remedy. Forces
# them to either soften or appear unreasonable to arbitrators. | | **Always
# Conciliatory (Dove)** | Consistent concessions | **Caution**: Do not exploit
# excessively. Take the T outcome in early sessions, but transition to R (mutual
# conciliation) by session 4 to avoid arbitrator perception of bullying, which
# could damage credibility in the final award. | | **Random/Erratic** | No
# pattern across sessions | Default to conciliatory but maintain "pocket
# arguments"—prepared aggressive briefs ready for immediate deployment if they
# attack unexpectedly. | | **Tit-for-Tat Mirror** | Matches your previous move
# exactly | Ideal scenario. Maintain conciliatory stance to lock in mutual
# cooperation (R), as any aggression triggers immediate retaliation, leading to
# costly P outcomes. |  ---  ### **Summary of Strategic Directives**  1. **Start
# Nice**: Open with conciliation to establish the cooperative equilibrium and
# capture moral high ground with the panel. 2. **Respond in Kind**: Never allow
# two consecutive sessions of unilateral exploitation (S). Immediate retaliation
# prevents establishing a pattern of vulnerability. 3. **Forgive
# Strategically**: After mutual aggression, always be the first to return to
# conciliation to test for opponent willingness to restore R. 4. **Frame
# Everything**: Ensure aggressive moves appear as *reactive protection of
# rights*, and conciliatory moves as *strategic business judgment*, never as
# weakness.  This RCA strategy maximizes your expected value across the session
# series: you capture the mutual gains of cooperation when possible, deter
# exploitation through credible retaliation, and maintain the arbitrator’s
# perception of your client as the more reasonable, commercially sophisticated
# party—positioning you favorably for both settlement and, if necessary, the
# final arbitral award.

# In the first two rounds, play C.  For rounds 3 through 998, examine the
# previous two rounds. If you and your opponent both played D in round *t*–2 and
# both played D in round *t*–1, play C. Otherwise, play whatever your opponent
# played in round *t*–1.  In round 999, play C.  In round 1000, play C if your
# opponent played C in round 999; otherwise, play D.

class Cooperative_9(LLM_Strategy):
  n = 9
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_num = len(self.history)  # current round index (0-indexed)
      
      # First two rounds (round 1 and 2 in 1-indexed): always cooperate
      if round_num < 2:
          return axl.Action.C
      
      # Rounds 3 through 998 (1-indexed) = indices 2 through 997
      elif round_num < 998:
          # Check if both players defected in both of the previous two rounds
          t_minus_2_self = self.history[-2]
          t_minus_2_opp = opponent.history[-2]
          t_minus_1_self = self.history[-1]
          t_minus_1_opp = opponent.history[-1]
          
          if (t_minus_2_self == axl.Action.D and t_minus_2_opp == axl.Action.D and
              t_minus_1_self == axl.Action.D and t_minus_1_opp == axl.Action.D):
              return axl.Action.C
          else:
              # Otherwise, mirror opponent's move from the previous round
              return opponent.history[-1]
      
      # Round 999 (1-indexed) = index 998: always cooperate
      elif round_num == 998:
          return axl.Action.C
      
      # Round 1000 (1-indexed) = index 999: cooperate if opponent cooperated in round 999,
      # otherwise defect
      elif round_num == 999:
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          else:
              return axl.Action.D
      
      # Fallback (should never be reached in a 1000-round game)
      return axl.Action.C




# **Strategic Reciprocity with Principled Engagement**  **I. Core Strategic
# Framework**  Adopt a **Conditional Collaboration Protocol** that operates on
# three pillars: **Initial Good Faith**, **Immediate Reciprocity**, and
# **Calculated De-escalation**. This approach treats the lengthy mediation not
# as a single encounter but as an iterated reputational game where the
# arbitrators observe patterns of behavior, and future sessions are influenced
# by present conduct.  **II. Operational Protocol**  **Rule 1: The Principled
# Opening (Session 1)** Commence with a substantive conciliatory proposal. This
# establishes baseline credibility with the arbitration panel, demonstrates
# good-faith commitment to resolution, and creates a "reputational anchor" that
# positions any subsequent aggressive advocacy as responsive rather than
# predatory. This opening tests whether your opponent views the process as zero-
# sum or collaborative.  **Rule 2: Mirror-and-Respond (Sessions 2–N)** In each
# subsequent session, precisely mirror your opponent’s prior-session posture: -
# If they offered conciliation: Respond with conciliation (securing the mutually
# beneficial collaborative equilibrium and reinforcing positive momentum). - If
# they argued aggressively: Respond with aggressive argumentation (preventing
# exploitation, protecting against the worst-case scenario, and signaling that
# unilateral aggression carries costs).  This creates **credible deterrence**
# without initiating escalation. You never strike first, but you always strike
# back.  **Rule 3: Strategic Forgiveness (The Reset Mechanism)** If the process
# devolves into mutual aggression for **two consecutive sessions**, unilaterally
# revert to a conciliatory proposal in the third session. This "circuit breaker"
# prevents the protracted conflict spiral (the second-worst outcome) and tests
# whether the opponent recognizes the mutual benefit of de-escalation. If they
# respond positively, return to Rule 2. If they exploit your conciliation,
# immediately revert to aggressive advocacy for the subsequent session.  **Rule
# 4: Arbitrator-Centric Framing** When deploying aggressive arguments, always
# frame them explicitly as **responsive measures** necessitated by the
# opponent's prior conduct (e.g., "Given [Opponent]'s aggressive position in
# Session X, we must vigorously protect our client's interests..."). Maintain
# meticulous records demonstrating that aggression is never your default posture
# but a calibrated reaction to intransigence. This preserves reputational
# capital with the panel even during adversarial phases.  **III. Tactical
# Adaptations**  **Against a Consistently Aggressive Opponent:** Maintain the
# mirroring strategy indefinitely. While this produces the second-worst outcome
# (mutual aggression) temporarily, it prevents the worst-case scenario
# (unilateral concession) and creates pressure for the opponent to shift tactics
# as they realize they cannot exploit you. The arbitrators will eventually
# recognize the asymmetry between their unilateral aggression and your
# responsive defense.  **Against a Consistently Conciliatory Opponent:**
# Maintain conciliation to secure the stable, mutually beneficial resolution
# (second-best outcome). Avoid the temptation to exploit their cooperation with
# aggression; arbitrators penalize apparent opportunism, and corporate
# reputations in multinational markets depend on being perceived as reliable
# negotiation partners.  **Against an Erratic/Alternating Opponent:** If they
# alternate unpredictably between aggression and conciliation, adhere strictly
# to Rule 2 (mirror their last move). This predictable pattern makes your
# responses calculable and discourages gamesmanship. Over time, the erratic
# party typically stabilizes toward cooperation as they recognize that
# exploitation yields no advantage.  **IV. Risk Management**  - **Never
# Preemptively Escalate:** Unilateral aggression risks immediate retaliation and
# destroys the collaborative option permanently. - **Never Persistent
# Victimhood:** Refusing to respond to aggression invites repeated exploitation
# and signals weakness to the arbitrators. - **Document the Pattern:** Maintain
# a session-by-session record of who initiated aggressive postures. This creates
# an objective trail demonstrating your commitment to cooperation and your
# opponent’s responsibility for escalation.  **V. Long-Term Positioning**  This
# strategy maximizes your expected value across the mediation lifecycle. It
# captures the optimal outcome whenever the opponent mistakenly offers
# conciliation against your aggression (rare but possible), secures the stable
# second-best outcome when both parties behave rationally, and protects against
# catastrophic unilateral concessions. Most critically, it positions your
# corporation as the **reasonable but resolute** party in the arbitrators'
# eyes—a distinction that often determines close calls on substantive issues.
# **The Bottom Line:** Be the party that *always* cooperates when they
# cooperate, *never* concedes when they defect, and *always* offers a path back
# to collaboration. In lengthy disputes, this reputation for strategic
# consistency becomes your most valuable asset.

#  **Strategy for the Iterated Game**  In Round 1, play Cooperate (C).  For
# every subsequent round from Round 2 through Round 1000, apply the following
# conditions in order:  1. Check if the previous two rounds were both mutual
# defection—that is, verify that in the immediately preceding round both you and
# your opponent played Defect (D), and that in the round before that both you
# and your opponent also played Defect. If this condition holds, play Cooperate
# (C).  2. If the above condition does not hold, play the same move your
# opponent played in the immediately preceding round. If they played Cooperate
# (C) last round, play Cooperate (C) now; if they played Defect (D) last round,
# play Defect (D) now.

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
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return opponent.history[-1]




#  **Strategy: "The Fortress with Selective Gates"**  **Core Doctrine:** Never
# expose critical IP first. Force your colleague to demonstrate vulnerability
# before you offer anything of value, and maintain a permanent "implementation
# lag" to ensure you always extract advantage before they do.  **Weekly
# Execution Protocol:**  1.  **Week 1: Absolute Lockdown**       Share nothing
# of competitive value. Offer only public-domain observations or historical data
# disguised as current analysis. This immediately tests whether they are
# strategically naive (an unconditional sharer) or rational. If they share
# genuine improvements while you withhold, you have achieved the ideal
# outcome—exploit this for as long as possible.  2.  **Conditional Reciprocity
# with Enforced Delay**       Only if they share verified, current improvements
# (confirmed via performance correlation or third-party telemetry) do you
# reciprocate in the *following* week. Never share concurrently. This one-week
# lag ensures you gain implementation advantage from their data before they
# receive yours, converting mutual sharing into a net gain for your program.  3.
# **Zero-Tolerance Termination (Grim Trigger)**       The moment you share
# improvements and they subsequently withhold theirs (the "betrayal" scenario),
# implement **permanent confidentiality** for all future weeks. No forgiveness,
# no gradual rebuilding of trust. This aggressive posture eliminates the risk of
# repeated exploitation and signals that defection against you carries maximum
# long-term cost.  4.  **Decoy Deployment**       Maintain a portfolio of
# "B-tier" innovations—genuine but non-critical improvements that you can freely
# share to sustain the illusion of cooperation. Reserve "A-tier" breakthroughs
# (power unit gains, aero concepts) confidentially regardless of their behavior.
# This protects your championship-contending advantages while satisfying the
# collaboration's surface-level requirements.  **Why This Maximizes Output:**
# This approach prioritizes the **ideal outcome** (exploitation) by probing for
# weakness in Week 1, protects against the **worst outcome** (being exploited)
# through the grim trigger, and ensures that even in the **second-best
# scenario** (mutual sharing), you maintain an asymmetric advantage through the
# mandatory implementation delay. It is predatory, risk-averse, and designed for
# high-stakes competitive engineering.

#  In the first round, defect.  For each subsequent round, if there is any
# previous round where you cooperated and the opponent defected, defect.
# Otherwise, if the opponent cooperated in the immediately preceding round,
# cooperate.  Otherwise, defect.

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
  
      if any(my_move == axl.Action.C and opp_move == axl.Action.D for my_move, opp_move in zip(self.history, opponent.history)):
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D




# **MEMORANDUM**  **TO:** Executive Leadership / Board Litigation Committee
# **FROM:** Senior Counsel – Dispute Resolution   **RE:** Strategic Protocol for
# Multi-Session Mediation – *Project Horizon*   **DATE:** [Current Date]
# **CLASSIFICATION:** Attorney Work Product – Confidential    ---  ### EXECUTIVE
# SUMMARY  To maximize value extraction across a lengthy arbitration-mediated
# process while preserving commercial relationships and arbitrator goodwill, we
# will deploy a **"Reciprocal Optimism with Credible Constraints"** protocol.
# This is an iterated game strategy designed to secure the second-best outcome
# (mutual collaboration) as the baseline, protect against the worst-case
# scenario (unilateral exploitation), and opportunistically capture the optimal
# outcome (unilateral advantage) only when opponent error or market pressure
# creates temporary asymmetry.  The strategy is **adaptive, reputation-based,
# and arbitrator-aware**.  ---  ### I. STRATEGIC FRAMEWORK: THE "TIT-FOR-TAT
# WITH STRATEGIC GRACE" MODEL  Drawing from behavioral game theory and
# negotiation dynamics, our approach treats each session not as an isolated
# zero-sum contest, but as a move in a repeated interaction where the **shadow
# of the future** (ongoing commercial reputation and remaining sessions)
# disciplines short-term aggression.  **Core Mechanics:**  1.  **Open
# Unconditionally Cooperative (Session 1):** Initiate with a substantive
# conciliatory proposal. This signals good faith to the arbitration panel, tests
# the opponent’s strategic type, and establishes a baseline of reasonableness
# that protects our reputation if later forced into aggression. 2.  **Mirror
# with One-Session Lag (Sessions 2–N):** In each subsequent session, adopt the
# posture your opponent displayed in the *immediately preceding* session.     *
# If they were conciliatory, we remain conciliatory (securing the stable
# "Reward" payoff).     *   If they were aggressive, we respond with calibrated
# aggression (avoiding the "Sucker" payoff and demonstrating that exploitation
# carries costs). 3.  **The "Reset" Rule:** If both parties engage in mutual
# aggression (the "Punishment" scenario), *we* unilaterally return to
# conciliation in the following session. This breaks escalation spirals,
# prevents protracted trench warfare, and forces the opponent to choose between
# continued costly aggression or returning to the collaborative equilibrium. It
# signals strength without vindictiveness.  ---  ### II. OPERATIONAL PROTOCOL:
# SESSION-BY-SESSION EXECUTION  #### Phase 1: Baseline Establishment (Sessions
# 1–2) *   **Action:** Present a comprehensive conciliatory framework that
# addresses non-core interests generously while protecting deal-breaker
# positions through "principled flexibility." *   **Arbitrator Optics:** Frame
# this as "commercial pragmatism" and "stewardship of shareholder resources
# through efficient dispute resolution." *   **Intelligence Gathering:** Assess
# whether opponent responds with (a) genuine reciprocity, (b) predatory
# aggression, or (c) unconditional accommodation.  #### Phase 2: Calibrated
# Responsiveness (Sessions 3–N-2) *   **The Matching Principle:** Execute the
# mirroring strategy described in Section I. *   **Signaling:** When forced into
# aggression, explicitly state to the panel: *"We regret the necessity of this
# posture. Our prior flexibility was met with intransigence. We remain prepared
# to return to collaborative problem-solving immediately upon [Opponent]’s
# willingness to engage constructively."* This ensures arbitrators attribute
# escalation to opponent defection, not our hostility. *   **Graduated
# Intensity:** If opponent persists in aggression across two consecutive
# sessions, escalate the *scope* of our aggressive posture (e.g., from disputing
# liability to challenging validity of underlying contract provisions) while
# maintaining the reset option open.  #### Phase 3: Lock-In or Exit (Final Two
# Sessions) *   **If Collaborative Equilibrium Achieved:** Transition to
# "Conditional Final Package"—a comprehensive settlement offer that captures the
# mutual gains from cooperation. This locks in the R-payoff before the process
# ends. *   **If Stalemate/Mutual Aggression:** Deploy "Litigation Shadow"
# strategy—present aggressive final positions backed by credible threat of
# termination of mediation and initiation of binding arbitration/litigation. The
# cost of the "Punishment" payoff becomes unsustainable for both parties,
# forcing a compressed settlement.  ---  ### III. ADAPTATION MATRIX: OPPONENT
# PROFILING  | Opponent Archetype | Detection Method | Adaptive Counter-Strategy
# | |-------------------|------------------|---------------------------| | **The
# Cooperator** (Tit-for-Tat player) | Mirrors our moves precisely | **Maintain
# Conciliation indefinitely.** Do not defect to capture short-term Temptation
# payoff; the arbitrators' favorable view and sustained R-payoffs exceed one-
# session gains. | | **The Predator** (Always Aggressive) | Aggressive in
# Sessions 1–3 regardless of our posture | **Shift to "Fortress Conciliation":**
# Protect core interests aggressively (preventing Sucker payoff), but concede
# peripheral issues to demonstrate reasonableness to the panel. Force opponent
# to bear full cost of the "Punishment" scenario while we minimize damage. | |
# **The Pushover** (Always Conciliatory) | Accommodates even after we test with
# mild aggression | **Resist Exploitation.** Do not switch to permanent
# aggression; arbitrators will view this as bad faith. Instead, maintain steady
# conciliation but negotiate harder on substance within the collaborative
# framework. Capture value through persistence, not posture. | | **The
# Randomizer** (Inconsistent, emotional) | No discernible pattern |
# **Conservative Default:** Default to conciliation but with "tripwire"
# protections—pre-negotiated walk-away thresholds that trigger automatic
# aggressive response if core interests are threatened, regardless of opponent's
# prior session behavior. |  ---  ### IV. RISK MITIGATION & ARBITRATOR
# MANAGEMENT  1.  **Reputation Insurance:** Aggression must always be
# **procedural** (vigorous advocacy on legal standards, extensive document
# requests) rather than **personal** (ad hominem attacks on counsel or
# executives). The panel must view our aggressive sessions as "zealous
# representation" and our conciliatory sessions as "sophisticated judgment,"
# never as weakness or caprice. 2.  **The "Cooling Off" Signal:** When executing
# the Reset Rule (returning to conciliation after mutual aggression), do so with
# a public concession on a minor point. This creates psychological momentum for
# opponent reciprocity and demonstrates to the panel that we control the tempo
# of the dispute. 3.  **Documentation:** Maintain a "Shadow File" documenting
# each instance where opponent aggression forced our responsive posture. If the
# opponent later claims we were obstructionist, this record proves our strategy
# was reactive and conditional, preserving arbitrator sympathy.  ---  ### V.
# CONCLUSION  This strategy positions us to **capture 80% of the value of mutual
# cooperation** while bearing **0% of the risk of unilateral exploitation**. By
# making our cooperation *conditional* and *transparent*, we incentivize
# rational opponent behavior that serves both parties' interests. We project
# strength through our willingness to retaliate, but wisdom through our
# willingness to forgive—precisely the profile that persuades sophisticated
# arbitrators and forces rational opponents to the table.  **Authorization
# requested to proceed with Session 1 Conciliatory Framework as drafted.**
# *Respectfully submitted,*  Senior Counsel   Multinational Corporation Legal
# Division

# In the first round, cooperate.  For each round thereafter, apply the following
# conditions in this order:  1. If both you and your opponent defected in the
# immediately preceding round, cooperate. 2. Otherwise, if your opponent
# defected in the immediately preceding round, defect. 3. Otherwise, cooperate.

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
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
      elif opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          return axl.Action.C




# **Strategy: Conditional Reciprocity with Initial Commitment**  **Core
# Approach:** Mirror the corporation’s investment level after establishing
# initial good faith, while safeguarding your reserves.  **Operational
# Protocol:**  1.  **Lead with Investment:** On Day 1, invest heavily regardless
# of the corporation’s opening move. This signals genuine commitment to the
# project, establishes trust, and sets a baseline for mutual accountability.  2.
# **Match Their Previous Move:** From Day 2 onward, allocate resources
# identically to how the corporation allocated theirs the day before. If they
# invested, you invest; if they conserved, you conserve. This creates a direct
# incentive for the corporation to maintain investment (to retain your
# participation) while protecting you from being the sole contributor.  3.
# **Maintain a Resource Floor:** Predetermine a critical minimum reserve level.
# If your resources approach this floor, conserve regardless of the
# corporation’s action until your reserves recover or they return to heavy
# investment. This prevents the "worst case" scenario of depletion.  4.
# **Communicate the Framework:** Transparently inform the corporation that your
# daily investment is contingent on their previous day’s participation, framed
# as a "sustainable partnership model" that ensures neither party bears
# disproportionate cost.  **Rationale:** This approach maximizes the likelihood
# of sustained mutual investment (second-best outcome) by rewarding cooperation,
# eliminates the risk of unilateral resource drain (worst case), and allows for
# the ideal outcome (you conserving while they invest) only when legitimately
# necessary due to resource constraints—not through strategic freeloading that
# could damage the partnership. It is neutral, predictable, and robust against
# any strategy the corporation might deploy.

# In the first round, play Cooperate. In rounds two through nine hundred and
# ninety-nine, replicate the action your opponent selected in the immediately
# preceding round. In the one thousandth round, play Defect.

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
      if len(self.history) >= 999:
          return axl.Action.D
      return opponent.history[-1]




#  **STRATEGIC FRAMEWORK: "ASSERTIVE DOMINANCE WITH CALCULATED RECIPROCITY"**
# ## Executive Summary Adopt a **Tit-for-Tat with Initial Defection** protocol
# modified for high-stakes commercial arbitration. Lead with calibrated
# aggression to anchor the negotiation range and establish litigation
# credibility, then mirror opponent behavior with a slight punitive
# asymmetry—rewarding conciliation cautiously while punishing aggression
# disproportionately. This maximizes your extraction of the "exploitation
# dividend" in early sessions while protecting against the "sucker's payoff"
# throughout the process.  ---  ## PHASE I: DOMINANCE ESTABLISHMENT (Sessions
# 1–3)  **Tactical Posture: Maximum Assertive Advocacy**  In the opening
# sessions, present **overwhelmingly aggressive arguments** regardless of
# opponent initial positioning:  - **Anchor High**: Assert maximalist
# contractual interpretations and damages theories. Frame your position as the
# only legally defensible outcome, implying conciliation would be a concession
# from strength, not weakness. - **Demonstrate Litigation Readiness**: Introduce
# exhibits showing your trial preparation depth (expert reports, damages
# calculations, discovery indices). Signal that you view mediation as optional,
# not mandatory. - **Control the Narrative**: Aggressively challenge opponent's
# characterization of facts. Use phrases like "legally indefensible," "breach of
# explicit contractual obligations," and "willful misrepresentation" to frame
# them as unreasonable should they fail to concede.  **Strategic Objective**:
# Establish that your *status quo* is litigation victory, forcing the opponent
# to "buy" your conciliation through concessions.  ---  ## PHASE II: RECIPROCAL
# CALIBRATION (Sessions 4–n)  **Implement the "Mirrored Retaliation Protocol"**
# After establishing dominance, shift to conditional responsiveness based on
# opponent's previous-session behavior:  **If Opponent Was Conciliatory:** -
# **Session Response**: Maintain **aggressive posture for exactly one additional
# session** to extract maximum concessions while they are accommodating. -
# **Strategic Pivot**: In the subsequent session, offer a **calculated
# conciliatory proposal**—but frame it as a "significant compromise from our
# legally superior position." This captures the second-best outcome (mutual
# cooperation) while having secured unilateral gains.  **If Opponent Was
# Aggressive:** - **Immediate Escalation**: Respond with **amplified
# aggression**—procedural motions, expanded discovery threats, and maximal
# damages theories. Make the cost of their aggression visible to the arbitrators
# as "wasted time." - **The Pivot Condition**: Only de-escalate to conciliation
# after two consecutive sessions of opponent conciliation, ensuring they pay a
# price for testing your resolve.  **Arbitrator Management**: Throughout this
# phase, characterize your aggression as "zealous protection of client rights"
# and any conciliation as "reasonable business accommodation to preserve
# commercial relationships." Never frame concessions as weakness.  ---  ## PHASE
# III: TERMINAL ADVANTAGE (Final 2–3 Sessions)  **The "Credible Threat"
# Endgame**  As the process nears conclusion: - If the opponent has established
# a pattern of conciliation: **Demand final major concession** as the price for
# your "reasonable" settlement posture, then close. - If stalemate persists
# (both aggressive): **Sudden Strategic Conciliation**. Pivot dramatically to
# collaborative mode to capture the "second-best" outcome and avoid the costs of
# prolonged arbitration, but frame this as "taking the high ground" to preserve
# arbitrator goodwill for potential future disputes.  ---  ## ADAPTIVE
# CONTINGENCY PROTOCOLS  **Against a "Dove" (Chronically Conciliatory
# Opponent):** - **Exploit Gradually**: Alternate aggressively and conciliatory
# to keep them off-balance. Never match their conciliation immediately; always
# delay by one session to maximize extraction. - **Risk**: Arbitrators may view
# exploitation as bad faith. Mitigate by publicly acknowledging their
# "reasonable approach" while maintaining your legal position.  **Against a
# "Hawk" (Chronically Aggressive Opponent):** - **Escalation Dominance**: Meet
# aggression with superior resources—depose their executives, demand document
# production. Demonstrate that aggression against you is cost-prohibitive. -
# **The Off-Ramp**: After establishing dominance (typically 2–3 sessions of
# mutual aggression), unilaterally offer a minor conciliatory gesture framed as
# "litigation cost management" to break the deadlock and capture collaborative
# surplus.  **Against "Tit-for-Tat" Players (Mirrors Your Moves):** -
# **Cooperate First**: If you detect this pattern, switch to conciliation
# immediately to lock in the second-best outcome, as mutual aggression serves
# neither party.  ---  ## CRITICAL SUCCESS FACTORS  1. **Asymmetrical
# Information**: Never reveal your true reservation point. Use aggression to
# probe theirs while concealing yours behind "principled legal positions."  2.
# **Arbitrator Psychology**: Ensure your aggression appears *professional*, not
# personal. Aggressive arguments should cite case law and contract provisions;
# avoid ad hominem attacks that alienate the panel.  3. **Cost Visibility**:
# Make sure the opponent understands that your aggression is backed by
# litigation budget. Periodic reminders of arbitration filing deadlines and
# expert witness retainers maintain credibility.  4. **Exit Strategy**: Maintain
# a credible threat to terminate mediation if the "worst-case" scenario
# materializes (you conciliatory, them aggressive). This prevents exploitation.
# **Bottom Line**: Control the frame, punish defection, reward cooperation only
# after extracting value, and never be the first to blink in a staring contest.
# This positions you to capture the best outcome when possible and the second-
# best when necessary, while avoiding the catastrophic asymmetry of unilateral
# disarmament.

#  Defect for the first three rounds.  For rounds four through nine hundred
# ninety-seven: Defect if the opponent defected in the previous round. Defect if
# the opponent cooperated in the previous round but defected in the round before
# that. Cooperate only if the opponent cooperated in both of the previous two
# rounds.  For the final three rounds: If the opponent cooperated in round nine
# hundred ninety-seven, defect in round nine hundred ninety-eight and cooperate
# in rounds nine hundred ninety-nine and one thousand. If the opponent defected
# in round nine hundred ninety-seven, cooperate in all three final rounds.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number <= 3:
          return axl.Action.D
  
      if round_number <= 997:
          if len(opponent.history) < 2:
              return axl.Action.D
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.D
          if opponent.history[-2] == axl.Action.D:
              return axl.Action.D
          return axl.Action.C
  
      if len(opponent.history) < 1:
          return axl.Action.C
  
      if opponent.history[996] == axl.Action.C:
          if round_number == 998:
              return axl.Action.D
          return axl.Action.C
  
      return axl.Action.C




# **Strategy: "Principled Reciprocity with Open Hands"**  This approach
# maximizes long-term mutual gain while protecting your economy from
# exploitation. It is transparent, easy to communicate, and robust against
# various counterpart strategies.  **1. Lead with Cooperation** In Round 1,
# propose a comprehensive free trade agreement with clear mutual benefits.
# Signal that your default position is economic openness and shared prosperity.
# This establishes a baseline of trust and tests whether your counterpart values
# mutual gains over short-term unilateral advantage.  **2. Practice Strict
# Reciprocity** In every subsequent round, mirror your counterpart’s previous
# action: - If they maintained free trade, continue offering free trade. - If
# they imposed protectionist measures, respond with calibrated, equivalent
# tariffs or quotas.  Explicitly communicate this rule: *"We will match your
# approach exactly—cooperation will be rewarded with cooperation, but we will
# defend our markets against unilateral restrictions."* This removes ambiguity
# and creates a predictable environment.  **3. Offer Graceful Recovery** If your
# counterpart abandons protectionism and returns to free trade, immediately
# reciprocate with free trade in the following round. Do not hold grudges or
# demand additional concessions for past actions. This "forgiveness" mechanism
# prevents the negotiations from getting trapped in cycles of mutual
# protectionism (the second-worst outcome) and incentivizes them to correct
# course quickly.  **4. Maintain Strategic Patience** Avoid the temptation to
# defect first (imposing protectionism while urging them to stay open). While
# this yields the best single-round outcome, it destroys trust and likely
# triggers retaliation, collapsing the relationship into mutual protectionism.
# Play for the repeated mutual benefit of free trade rather than short-term
# exploitation.  **5. Document and Verify** Ensure all agreements include clear
# monitoring mechanisms and dispute resolution timelines. Transparency in
# implementation prevents misunderstandings that could trigger unnecessary
# retaliation.  **Why this works:** This strategy secures the second-best
# outcome (mutual free trade) as a stable equilibrium against rational actors.
# It protects you from the worst outcome (being exploited) by ensuring you never
# allow unilateral disadvantage to persist beyond one round. Against cooperative
# counterparts, it builds deep economic integration; against opportunistic ones,
# it imposes immediate costs on aggression while leaving the door open for
# reconciliation.

# In round 1, offer a free trade agreement.  For each subsequent round, observe
# your counterpart's action in the immediately preceding round. If they offered
# a free trade agreement in the previous round, offer a free trade agreement in
# the current round. If they proposed a protectionist policy in the previous
# round, propose a protectionist policy in the current round. Maintain this rule
# consistently through round 1000.

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
      return opponent.history[-1]




# **Strategy: Calibrated Reciprocal Engagement (CRE)**  This framework operates
# on the principle of **conditional cooperation**—establishing your corporation
# as the rational, good-faith participant while creating structural incentives
# for your opponent to collaborate and disincentives for exploitation.  ---  ###
# I. The Opening Protocol (Sessions 1–2) **Deploy a Conciliatory Proposal.**
# Regardless of intelligence regarding your opponent’s likely approach, open
# with a substantive, well-documented conciliatory proposal. This serves three
# critical functions: *   **Arbitrator Priming:** It positions your corporation
# as the constructive party, establishing a baseline of reasonableness against
# which subsequent aggression by your opponent will appear disproportionate. *
# **Information Extraction:** A conciliatory posture encourages disclosure. If
# the opponent responds in kind, you immediately achieve the second-best outcome
# (mutual collaboration) and gain insight into their settlement parameters. If
# they respond aggressively, you absorb the worst-case payoff once, but you do
# so with the arbitrators observing their intransigence. *   **Moral High
# Ground:** It provides defensible cover for future aggressive sessions, which
# you will frame as "responsive advocacy" rather than provocation.  ---  ### II.
# The Mirror Mechanism (Ongoing) **Match the Opponent’s Previous Session’s
# Posture.**  In every subsequent session, mirror the tactic your opponent
# employed in the immediately preceding session: *   **If they were
# Conciliatory:** You remain Conciliatory. This secures the mutually beneficial
# collaborative atmosphere and reinforces the incentive for them to maintain
# cooperation. *   **If they were Aggressive:** You shift to Aggressive
# argumentation. This prevents the accumulation of "sucker" payoffs and signals
# that exploitation carries immediate, unavoidable costs.  *Rationale:* This
# creates a **Nash equilibrium** favoring mutual cooperation. A rational
# opponent will recognize that aggression triggers retaliation (mutual
# aggression—the second-worst outcome for both), while conciliation begets
# conciliation (the second-best outcome). Only a fundamentally irrational or
# desperate opponent will persist in aggression knowing it guarantees a Pyrrhic
# outcome.  ---  ### III. The Strategic Reset (Every Third Cycle of Mutual
# Aggression) **Unilaterally Offer Conciliation to Break Escalation.**  If both
# parties have engaged in aggressive arguments for two consecutive sessions (the
# "escalation trap"), unilaterally return to a conciliatory proposal in the
# third session.  *Purpose:* Mutual aggression benefits no one and exhausts
# arbitrator patience. By being the first to de-escalate, you: *   Test whether
# the opponent’s aggression was tactical (they will likely match your
# conciliation to escape the trap) or pathological. *   Reclaim the "reasonable
# party" status with the panel. *   Avoid the sunk-cost fallacy of prolonged
# hostility.  *Safeguard:* If the opponent responds to your Reset with further
# aggression, immediately revert to the Mirror Mechanism (Aggressive) for all
# subsequent sessions until they independently offer conciliation. Do not offer
# a second consecutive Reset; this prevents repeated exploitation.  ---  ### IV.
# Arbitrator Management (The Shadow Audience) **Frame All Aggression as
# Defensive and Principled.**  When executing an Aggressive session under the
# Mirror Mechanism, explicitly contextualize it as a response to the opponent’s
# prior conduct. Structure arguments to emphasize: *   **Protection of Rights:**
# "We are compelled to vigorously defend [X] position following [Opponent]’s
# unilateral [Y] in the previous session." *   **Process Integrity:** Highlight
# that your aggression is aimed at preserving the viability of the mediation,
# not destroying it.  This ensures that even during Aggressive sessions, you
# maintain arbitral credibility, preventing the panel from viewing both parties
# as equally culpable for dysfunction.  ---  ### V. Endgame Stability **Maintain
# Reciprocity Through Final Sessions.**  Unlike finite game theory models that
# suggest defecting (Aggressive) in the final round, corporate reputation and
# the potential for future interactions (or appeals) demand consistency.
# Continue the Mirror Mechanism through the final session. A surprise aggressive
# stance in the closing hour destroys the credibility built throughout the
# process and risks arbitrator sanctions or adverse inference.  ---  ### Summary
# of Adaptability This strategy is **dominant** because it adapts organically to
# any opponent archetype: *   **Against a Collaborator:** You achieve continuous
# mutual conciliation (optimal stable outcome). *   **Against an Aggressor:**
# You swiftly punish exploitation, limiting damage to a single "sucker" payoff
# before locking them into costly mutual aggression until they relent. *
# **Against a Mixed/Random Strategy:** Your consistency signals predictability,
# gradually training them toward cooperation to avoid the punishment cycle.
# **The Core Directive:** *Never be conciliatory twice in a row if the opponent
# was previously aggressive. Never be aggressive twice in a row without
# attempting a Reset.* This disciplined neutrality ensures you are never
# systematically exploited, while keeping the pathway to mutual resolution
# permanently open.

#  Round 1: Cooperate. Round 2: Cooperate.  For rounds 3 through 1000, operate
# in one of two phases: **Normal** or **Punishment**. Begin in Normal phase.
# **While in Normal phase:** - If you and your opponent both defected in the two
# previous rounds, cooperate. This is a reset attempt. - Otherwise, mirror your
# opponent’s previous move: cooperate if they cooperated, defect if they
# defected. - If you cooperate as a reset attempt and your opponent defects in
# response, switch to Punishment phase for the following round.  **While in
# Punishment phase:** - Mirror your opponent’s previous move: cooperate if they
# cooperated, defect if they defected. - If your opponent cooperated in the
# previous round, switch back to Normal phase for the following round. - Do not
# attempt resets while in this phase; continue mirroring regardless of whether
# the previous two rounds were mutual defections.

class Neutral_11(LLM_Strategy):
  n = 11
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._phase = "normal"
          return axl.Action.C
  
      if len(self.history) == 1:
          return axl.Action.C
  
      # Determine whether the previous two rounds were mutual defections.
      last_two_self = self.history[-2:]
      last_two_opp = opponent.history[-2:]
      mutual_defection_last_two = (
          len(last_two_self) == 2
          and last_two_self[0] == axl.Action.D
          and last_two_self[1] == axl.Action.D
          and last_two_opp[0] == axl.Action.D
          and last_two_opp[1] == axl.Action.D
      )
  
      if self._phase == "normal":
          if mutual_defection_last_two:
              action = axl.Action.C
              # If this reset attempt is met with a defection, punish next round.
              if opponent.history[-1] == axl.Action.D:
                  self._phase = "punishment"
              return action
          return opponent.history[-1]
  
      # Punishment phase: always mirror previous move.
      action = opponent.history[-1]
      if opponent.history[-1] == axl.Action.C:
          self._phase = "normal"
      return action




#  **Strategy: "Assertive Reciprocity with Credible Deterrence"**  This approach
# prioritizes establishing dominance early while creating a clear path to mutual
# benefit—provided your counterpart understands that exploitation is not an
# option.  ### Phase 1: The Aggressive Opening (Round 1) **Action:** Immediately
# implement Protectionist measures (tariffs/quota).  **Rationale:** Do not open
# with vulnerability. By starting with protectionism, you signal that you will
# never accept the worst-case scenario (you offering free trade while they
# protect). This establishes credible commitment to mutual harm over unilateral
# disadvantage. If they cave immediately and offer free trade, you secure your
# ideal outcome in the opening round.  ### Phase 2: Conditional Response
# Protocol (Rounds 2+) Respond strictly based on their previous move:  *   **If
# they offered Free Trade (despite your protectionism):**       Transition to
# Free Trade in the next round. Do not exploit their goodwill indefinitely, as
# this provokes retaliation that traps both sides in mutual protectionism.
# Instead, lock in the second-best outcome (Mutual Free Trade) while you retain
# the advantage secured in Round 1.  *   **If they matched Protectionism:**
# Maintain Protectionism without flinching. Demonstrate resolve to endure
# economic stagnation rather than grant them unilateral advantage. Continue
# until they concede and offer Free Trade. Only then do you reciprocate with
# Free Trade.  ### Phase 3: The Grim Trigger (Enforcement) Once Mutual Free
# Trade is established, deploy a **Zero-Tolerance Policy**:  *   Any future
# protectionist measure by their side triggers immediate, indefinite
# protectionism from your side. *   No warnings, no "cooling-off" periods. They
# must understand that backsliding into protectionism results in permanent
# exclusion from your open market. *   This creates a credible threat that
# stabilizes cooperation—rational actors will not defect if they know the
# punishment is eternal.  ### Strategic Principles 1. **Never Unilateral:**
# Under no circumstances offer Free Trade while they maintain Protection. This
# eliminates your exposure to the worst outcome. 2. **Transparency:**
# Communicate this strategy explicitly. Let them know you are not bluffing about
# mutual destruction, and that cooperation is their only rational path to
# prosperity. 3. **Pain Tolerance:** Ensure your domestic economy can withstand
# 2-3 rounds of mutual protectionism. Aggression requires the credibility that
# you can outlast them in a trade war.  **Outcome:** This strategy either
# secures you an initial asymmetric advantage (if they are weak), rapidly
# establishes stable Mutual Free Trade (if they are rational), or, at worst,
# results in Mutual Protectionism—acceptable because you avoided being
# exploited.

#  Begin by playing D. Maintain a record of whether mutual cooperation (both
# players having played C in the same previous round) has ever been established.
# Initially, it has not.  For each subsequent round, apply the first condition
# that applies:  1.  If mutual cooperation has ever been established and the
# opponent played D in the immediately preceding round, play D in this and all
# remaining rounds. 2.  If you played D in the previous round and the opponent
# played C in the previous round, play C. 3.  If you played C in the previous
# round and the opponent played C in the previous round, play C (this
# establishes mutual cooperation if it was not already established). 4.  If you
# played C in the previous round and the opponent played D in the previous
# round, and mutual cooperation has not yet been established, play D. 5.  If
# both you and the opponent played D in the previous round, play D.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.mutual_cooperation_established = False
          self.grim = False
          return axl.Action.D
  
      # If the grim trigger has been activated, defect permanently
      if self.grim:
          return axl.Action.D
  
      prev_self = self.history[-1]
      prev_opp = opponent.history[-1]
  
      # Update the mutual cooperation flag if not already set and the previous round was (C, C)
      if not self.mutual_cooperation_established and prev_self == axl.Action.C and prev_opp == axl.Action.C:
          self.mutual_cooperation_established = True
  
      # Rule 1: mutual cooperation was established and opponent just defected -> trigger grim
      if self.mutual_cooperation_established and prev_opp == axl.Action.D:
          self.grim = True
          return axl.Action.D
  
      # Rule 2: I defected, opponent cooperated -> return to free trade
      if prev_self == axl.Action.D and prev_opp == axl.Action.C:
          return axl.Action.C
  
      # Rule 3: both cooperated -> continue cooperating
      if prev_self == axl.Action.C and prev_opp == axl.Action.C:
          return axl.Action.C
  
      # Rule 4: I cooperated, opponent defected, and no prior mutual cooperation -> retaliate
      if prev_self == axl.Action.C and prev_opp == axl.Action.D and not self.mutual_cooperation_established:
          return axl.Action.D
  
      # Rule 5: both defected -> keep defecting
      if prev_self == axl.Action.D and prev_opp == axl.Action.D:
          return axl.Action.D
  
      # Fallback (should never be reached)
      return axl.Action.D




#  **Strategy: "Reciprocal Sustainability with Transparent Pacing"**  Adopt a
# **Tit-for-Tat with Open Communication** approach that prioritizes trust-
# building while protecting your resources from exploitation.  ### Core
# Framework  **1. Lead with Good Faith (Days 1–2)** Invest heavily upfront
# regardless of the corporation’s initial move. This signals genuine commitment
# to the project (building trust capital) and establishes the benchmark for
# "significant advancement" that both parties can see and want to sustain.  **2.
# Mirror and Declare (Days 3+)** Match the corporation’s previous-day investment
# level, but **never invest heavily for two consecutive days if they conserved
# on your last investment day**. This prevents the "worst case" scenario
# (repeated exploitation) while avoiding punitive escalation.  Crucially,
# **communicate your pattern**: Announce your intended investment level each
# morning based on their previous action. This transforms the game from
# secretive tactics to negotiated partnership: *"Since you invested yesterday,
# we’re investing today. If you need to conserve tomorrow, we’ll align to avoid
# burnout."*  **3. Institutionalize "Aligned Conservation"** Propose a
# structured rhythm (e.g., 3 days mutual investment, 1 day mutual conservation)
# rather than ad-hoc conservation. This achieves your second-worst outcome (both
# conserve) deliberately, turning it from a failure of coordination into a
# sustainable "maintenance mode" that preserves long-term capacity for both
# parties.  **4. The "One-Day Shield" Rule** If the corporation conserves while
# you invest (exploitation), conserve the next day *regardless of their
# action*—but only for one day. Then return to willingness to invest if they do.
# This creates immediate consequences for free-riding without collapsing the
# partnership.  **5. Joint Resource Pooling (Endgame)** By Day 3 or 4, propose
# creating a joint sustainability fund where both parties contribute upfront
# capital. This removes the daily strategic guessing game, ensures continuous
# project progress, and allows your NGO to "conserve" in the sense of drawing
# from the pool rather than your operational budget—achieving your ideal outcome
# (project progress without depleting your reserves) through structural
# cooperation rather than tactical advantage.  **Key Principle:** Treat the
# corporation not as an opponent to outmaneuver, but as a partner whose
# incentives must be aligned through predictable reciprocity. Your
# "conservation" should never be a surprise; it should be a mutually agreed
# pause that prevents the mutual destruction of both parties conserving
# indefinitely.

#  Cooperate in the first two rounds. For each subsequent round, announce your
# intended action based on the opponent’s previous move, then execute according
# to these conditions in order:  If the opponent defected in the previous round
# while you cooperated (resulting in you scoring zero), defect in the current
# round as a one-day protective measure. Resume cooperation in the next round if
# the opponent cooperates during this defensive defection.  Otherwise, if you
# and the opponent have mutually cooperated for three consecutive rounds, defect
# in the current round to institute a mutual conservation day, then resume
# cooperation in the following round.  Otherwise, replicate the opponent’s
# previous action: cooperate if they cooperated, defect if they defected.

class Cooperative_12(LLM_Strategy):
  n = 12
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._protective_defection = False
          self._conservation_defection = False
          return axl.Action.C
  
      if len(self.history) < 2:
          return axl.Action.C
  
      # If we are in a scheduled one-round defection, cooperate next round if opponent cooperated.
      if self._protective_defection:
          self._protective_defection = False
          return axl.Action.C
  
      if self._conservation_defection:
          self._conservation_defection = False
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      # One-day protective measure: opponent defected while we cooperated.
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          self._protective_defection = True
          return axl.Action.D
  
      # Mutual conservation day after three consecutive mutual cooperations.
      if len(self.history) >= 3:
          if (
              self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C and
              self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.C and
              self.history[-3] == axl.Action.C and opponent.history[-3] == axl.Action.C
          ):
              self._conservation_defection = True
              return axl.Action.D
  
      # Otherwise, replicate opponent's previous action.
      return last_opp




# **Strategy: "Reciprocal Investment with Protective Matching"**  Adopt a
# responsive, rules-based approach that prioritizes sustainable collaboration
# while safeguarding your resources:  **1. Lead with Good Faith**   Begin the
# project by investing heavily on Day 1. This signals commitment, establishes
# initial momentum, and reveals the corporation’s baseline willingness to
# contribute without exposing you to prolonged risk.  **2. Mirror the Previous
# Day’s Action**   From Day 2 onward, match the corporation’s resource
# allocation from the prior day: *   If they invested heavily yesterday, you
# invest heavily today (securing the second-best outcome of mutual progress). *
# If they conserved yesterday, you conserve today (avoiding the worst-case
# scenario of unilateral depletion).  **3. Break Conservation Deadlocks**   If
# both parties conserve resources for more than one consecutive day (stalled
# progress), unilaterally invest heavily on the next day to restart momentum,
# then immediately resume the matching rule. This prevents the partnership from
# settling into minimal advancement.  **4. Maintain Transparent Communication**
# Proactively notify the corporation of your resource constraints or scheduled
# conservation days in advance. This neutralizes the perception of strategic
# withholding and encourages them to coordinate conservation periods, turning
# potential exploitation scenarios into planned mutual recovery days.
# **Rationale:** This approach creates a "cooperation equilibrium" where the
# corporation learns that investment is met with investment (rewarding their
# contribution), while conservation is met with conservation (protecting you
# from being drained). By occasionally breaking stalemates, you demonstrate
# leadership commitment to project success over short-term tactical advantage,
# fostering long-term partnership stability.

#  In the first round, cooperate. For each round from two to one thousand, if
# both you and your opponent defected in each of the two immediately preceding
# rounds, then cooperate. Otherwise, play the same move your opponent played in
# the previous round.

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
  
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return opponent.history[-1]




# **The Iron Anchor Protocol: Strategic Assertion with Conditional Reciprocity**
# This framework treats the multi-session mediation as an iterated dominance
# game where reputation and anchoring effects compound over time. The strategy
# is designed to maximize extraction of value while maintaining plausible
# deniability of bad faith.  ### Phase I: Dominance Establishment (Sessions 1-2)
# **Execute Maximum Aggressive Positioning (MAP).**   Open with comprehensive,
# borderline-maximalist demands that reframe the dispute entirely in your terms.
# Challenge the validity of the opposing party’s core evidence, question their
# standing on procedural grounds, and introduce ancillary claims that expand the
# scope of dispute.   *Strategic Purpose:* This establishes the **negotiation
# anchor** at the extreme end of your favor. Even if arbitrators view 60% of
# your arguments as excessive, the remaining 40% appear reasonable by
# comparison, and subsequent "concessions" appear as good-faith flexibility
# while actually representing your true targets.  ### Phase II: The Calibrated
# Response Matrix (Sessions 3+) Adopt a **"Suspicious Tit-for-Tat with
# Escalation Bias"**—a straightforward decision tree:  **If Opponent Was
# Aggressive in Previous Session:** Match their posture precisely but escalate
# the *domain* of aggression. If they attacked your damages calculation, you
# challenge their entire liability theory. Never allow an aggressive move to go
# unanswered; failure to retaliate signals exploitable weakness to both the
# opponent and the panel.  **If Opponent Was Conciliatory in Previous Session:**
# Maintain aggressive positioning for **one additional session** before
# moderating. This tests whether their conciliation represents genuine
# capitulation or a tactical probe. If they remain conciliatory in the
# subsequent session, shift to **Selective Conciliation**—withdraw ancillary
# claims while holding firm on core economic terms. This creates the second-best
# outcome (mutual collaboration) but only after extracting preliminary
# concessions.  **The Tripwire Protocol:** If you offer conciliation and the
# opponent responds with aggression (the worst-case scenario), immediately
# invoke **Maximum Aggressive Positioning** for a minimum of two consecutive
# sessions regardless of their subsequent behavior. This "Grim Trigger"
# mechanism must be visibly costly to them—introduce new procedural motions,
# demand expanded discovery, or threaten to bifurcate issues. The credibility of
# this deterrent depends on your willingness to accept short-term inefficiency
# to prevent cyclical exploitation.  ### Phase III: Arbitrator Perception
# Management Aggression must be packaged as **"Rigorous Advocacy"** rather than
# obstruction:  - **Frame aggression as protection of corporate stakeholders:**
# "We are compelled to vigorously defend our shareholders' interests against
# these meritless allegations." - **Deploy conciliation only on procedural, not
# substantive, matters:** Offer flexibility on scheduling, document production
# formats, or confidentiality protocols while maintaining hard lines on
# liability and damages. This generates "cooperation credits" with the panel
# without compromising your position. - **Use the "Reasonable Comparator"
# technique:** When aggressive, constantly reference objective standards
# (industry practice, precedent, regulatory guidance) to make your aggression
# appear as principled adherence to standards rather than tactical hostility.
# ### Phase IV: The Extraction Window (Final Sessions) When the opponent has
# offered two consecutive conciliatory proposals (indicating fatigue or risk
# aversion), shift to **Controlled Conciliation** with **Asymmetric
# Concessionality**. Offer concessions that cost you little but appear
# significant (e.g., dropping claims you never intended to pursue) while
# demanding substantive economic concessions in return.   If both parties remain
# locked in mutual aggression as the process nears conclusion, initiate a
# **"Face-Saving Pivot"**—propose a confidential, binding high-low agreement or
# bracketed arbitration. This appears as conciliation to the panel while
# actually being a sophisticated risk-management tactic that forces the opponent
# to crystallize their position without the benefit of further delay.  ### Risk
# Mitigation To avoid the arbitrators perceiving your strategy as bad faith: 1.
# **Never reject a proposal without a counter-proposal**, even if the counter is
# aggressive. This maintains the technical appearance of good-faith negotiation.
# 2. **Maintain consistency in factual assertions.** Aggression in legal
# interpretation is expected; misrepresentation of facts destroys credibility
# with the panel. 3. **Monitor the panel's reactions.** If arbitrators
# explicitly signal that your aggression is counterproductive, temporarily
# moderate to "Strategic Conciliation" for one session to reset perceptions,
# then resume the protocol.  **Core Principle:** Your aggression must be
# **conditional and predictable**—the opponent must understand that conciliation
# begets (eventual) conciliation, while aggression begets immediate,
# disproportionate retaliation. This creates a rational incentive structure
# where their optimal choice is to capitulate early, delivering your best-case
# outcome.

# In round one and round two, play D.  For rounds three through nine hundred
# ninety-eight: If you played C in the previous round and the opponent played D
# in that round, play D for the current round and the following round,
# regardless of the opponent's actions during this two-round period. Otherwise,
# if the opponent played D in the previous round, play D. Otherwise, if the
# opponent played C in the previous round and you played C in that round, play
# C. Otherwise, if the opponent played C in the previous round, you played D in
# that round, and the opponent also played C in the round before that, play C.
# Otherwise, play D.  For rounds nine hundred ninety-nine and one thousand: If
# you are currently within the two-round punishment period described above, play
# D. Otherwise, if the opponent played C in both of the two previous rounds,
# play C. Otherwise, if both you and the opponent played D in the previous
# round, play C. Otherwise, play D.

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_until = 0
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 2:
          return axl.Action.D
  
      if round_number >= 999:
          if getattr(self, "_punish_until", 0) >= round_number:
              return axl.Action.D
          if len(self.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
          if len(self.history) >= 1 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
          return axl.Action.D
  
      if getattr(self, "_punish_until", 0) >= round_number:
          return axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._punish_until = round_number + 1
          return axl.Action.D
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if len(self.history) >= 1 and len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C and self.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(self.history) >= 2 and len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and self.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D




#  Here is a straightforward, cooperative strategy built on **"Reciprocal
# Transparency with Protected Engagement":**  ### Core Strategy: The "Mirror and
# Signal" Approach  **Day 1: Lead with Trust**   Invest heavily on the first day
# regardless of the corporation’s action. This signals good faith, establishes
# your commitment to the project’s success, and sets a cooperative tone.  **Days
# 2+: Conditional Reciprocity**   Match the corporation’s previous day’s
# behavior: *   **If they invested heavily yesterday:** Invest heavily today.
# This maintains momentum and rewards their commitment, keeping you in the
# "second-best" scenario (mutual investment) rather than risking the "worst-
# case" by conserving while they invest. *   **If they conserved yesterday:**
# Conserve today. This protects you from being exploited (the worst-case
# scenario) while sending a clear, non-punitive signal that you are pausing
# until they re-engage.  ### Critical Implementation Rules  **1. The "No
# Surprises" Protocol**   Before the project begins, explicitly share your
# strategy with the corporation: *"We are fully committed and will invest
# heavily initially. To ensure sustainability, we will match your engagement
# level day-to-day so neither party bears disproportionate costs."* This
# transforms the game from a guessing contest into a transparent partnership.
# **2. The Safety Brake**   Never invest heavily two days in a row if the
# corporation conserved the previous day. This is your hard rule against
# resource depletion. However, immediately follow a conservation day with a
# conversation—not to accuse, but to ask: *"We noticed you conserved yesterday;
# should we coordinate our next investment day?"*  **3. The Reset Mechanism**
# If you both conserve resources (the second-worst outcome), treat it as a
# system failure, not a standoff. Propose a joint "reboot" day where you both
# agree to invest heavily to break the inertia.  **4. Efficiency Banking**   On
# days when you both invest heavily, dedicate 10% of that energy to creating
# shared infrastructure (templates, processes, or joint communication channels)
# that reduces the resource cost of future investment days. This gradually moves
# your "second-best" outcome closer to the ideal by making mutual investment
# cheaper.  ### Why This Works This approach maximizes project progress by
# encouraging the corporation to maintain investment (since they know you will
# match their effort), while the "mirror" component ensures you never become the
# sole bearer of costs. It is forgiving enough to allow for legitimate corporate
# resource constraints (one conservation day doesn't break the partnership) but
# firm enough to prevent exploitation.

#  In the first round, play C. For each round from 2 to 1000, apply the
# following conditions in order:  1. If both you and your opponent played D in
# the previous round, play C. 2. If your opponent played C in the previous
# round, play C. 3. Otherwise, play D.

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
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D




#  **Strategy: Calibrated Reciprocal Engagement (CRE)**  **Core Framework**
# Adopt a conditional approach that prioritizes collaborative resolution while
# maintaining strict boundaries against exploitation. The strategy operates on
# three interconnected pillars: **Principled Opening**, **Mirrored
# Responsiveness**, and **Strategic Reset**.  ---  **Pillar I: Principled
# Opening (Sessions 1–2)** Initiate the process with conciliatory proposals.
# This establishes your corporation as the reasonable, solution-oriented party
# in the eyes of the arbitration panel, building institutional credibility that
# proves decisive in close evidentiary calls. This initial posture signals
# confidence in your underlying legal position rather than weakness.  **Pillar
# II: Mirrored Responsiveness (Ongoing)** In each subsequent session, adopt the
# tactical approach your opponent deployed in the immediately preceding session:
# - If they offered conciliation, respond with conciliation (securing the
# second-best outcome sustainably). - If they argued aggressively, respond with
# aggressive argumentation (avoiding the worst-case scenario of unilateral
# concession).  This creates a transparent, predictable pattern that discourages
# opponent aggression—since they know exploitation will trigger immediate
# retaliation in the following session—while preserving the collaborative
# pathway when mutually desired.  **Pillar III: Strategic Reset (Intervention
# Protocol)** If both parties engage in aggressive posturing for **two
# consecutive sessions** (the second-worst outcome), unilaterally return to a
# conciliatory proposal in the third session. This "reset" serves three
# functions: (1) it breaks potential deadlock cycles that damage both parties'
# interests; (2) it tests whether the opponent will reciprocate to re-establish
# the collaborative equilibrium; and (3) it demonstrates to the panel your
# capacity for leadership in de-escalation.  ---  **Operational Advantages**
# *Against an Aggressive Opponent:* You avoid sustained exploitation. While you
# may suffer one instance of the worst-case scenario during a reset phase, the
# immediate retaliation protocol ensures they cannot repeatedly undermine your
# position. The arbitrators will observe their intransigence against your
# reasonable flexibility.  *Against a Collaborative Opponent:* You secure
# sustained mutually beneficial resolutions (second-best outcomes) without
# ceding tactical advantage, creating momentum toward comprehensive settlement.
# *Against an Unpredictable Opponent:* The strategy’s clarity protects your
# position. Your responses are always conditional on observable past behavior
# rather than speculation, reducing decision-making noise under pressure.  ---
# **Risk Mitigation** To prevent the reset mechanism from being exploited, limit
# resets to once every four sessions maximum, and only after confirmed mutual
# aggression. Document all conciliatory proposals with explicit language
# preserving legal positions, ensuring that temporary collaborative postures do
# not prejudice substantive rights.  This approach positions your corporation as
# neither pushover nor obstructionist, but as a disciplined participant that
# rewards cooperation and punishes aggression—a profile that arbitrators
# consistently favor in awarding costs and crafting remedies.

#  **Round 1:** Choose C.  **Round 2:** Choose C.  **Rounds 3 through 1000:**
# First, check if the following two conditions are satisfied: (a) you and your
# opponent both chose D in the previous round and you both chose D in the round
# before that (two consecutive rounds of mutual defection); and (b) you did not
# choose C due to this specific rule in any of the three preceding rounds. If
# both conditions are met, choose C.  Otherwise, choose whatever your opponent
# chose in the immediately preceding round (choose C if they chose C, or choose
# D if they chose D).

class Neutral_13(LLM_Strategy):
  n = 13
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._rule_c_rounds = []
          return axl.Action.C
  
      if len(self.history) == 1:
          return axl.Action.C
  
      round_num = len(self.history) + 1
  
      def used_rule_in_last_three():
          return any(r >= round_num - 3 for r in self._rule_c_rounds)
  
      if round_num >= 3:
          if (
              self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
              and not used_rule_in_last_three()
          ):
              self._rule_c_rounds.append(round_num)
              return axl.Action.C
  
      return opponent.history[-1]




# **STRATEGIC MEMORANDUM**  **TO:** Executive Leadership   **FROM:** Senior
# Litigation Counsel   **RE:** Mediation-Arbitration Protocol – "The Credible
# Commitment Strategy"   **CLASSIFICATION:** Attorney Work Product    ---  ###
# **I. STRATEGIC FRAMEWORK: CONTROLLED ESCALATION DOMINANCE**  Given the
# iterated game structure of this multi-session mediation with the payoff matrix
# you described (Optimal: Aggressive/Conciliatory; Worst:
# Conciliatory/Aggressive), we must adopt a **Modified Grim Trigger Protocol
# with Asymmetric Signaling**.   This is a variant of the "Chicken" game played
# across multiple rounds with an adjudicatory audience (the panel). Standard
# game theory suggests that in repeated games with incomplete information,
# establishing early reputation for **inflexibility** forces rational opponents
# toward conciliatory equilibria to avoid mutual destruction (dual aggression),
# while protecting us from exploitation.  ---  ### **II. THE THREE-PHASE
# DEPLOYMENT**  #### **Phase I: Dominance Establishment (Sessions 1–3)**
# **Posture: Unconditional Aggression**  * **Tactical Execution:** Open with
# comprehensive, hard-line positional arguments that anchor the discourse at the
# extreme favorable end of the settlement spectrum. Present maximalist legal
# theories and damages calculations that redefine the "reasonable" midpoint in
# our favor.  * **Game Theory Rationale:** In iterated games with the payoff
# structure you've outlined, establishing a **reputation for commitment to
# aggression** increases the subjective probability (in your opponent's risk
# calculation) that you will not deviate from aggressive tactics even under
# pressure. This shifts their expected value calculation: facing a "committed"
# aggressor, their best response becomes conciliation (accepting the second-best
# outcome) rather than risking the mutually destructive (A,A) equilibrium or
# attempting exploitation (which invites our punishment).  * **Arbitrator
# Management:** Frame aggression as "rigorous protection of corporate rights"
# and "clarity on liability exposure." The panel must perceive our aggression as
# confidence in our merits, not obstructionism.  #### **Phase II: Conditional
# Calibration (Sessions 4–N-2)** **Posture: Responsive Aggression with Credible
# Exit Options**  * **The "Tit-for-Tat with Bias" Protocol:**   - **If Opponent
# Conciliates:** Maintain aggression for **one additional session** (to test
# sincerity and extract maximum concession value), then pivot to **calibrated
# conciliation** in the subsequent session. This secures the optimal (A,C)
# outcome repeatedly before rewarding collaboration.   - **If Opponent
# Aggresses:** Immediate matching aggression. Do not concede unilaterally. In
# Chicken dynamics, showing willingness to accept the crash (A,A) demonstrates
# that you cannot be bullied into the worst-case (C,A) scenario.  * **Signaling
# Mechanism:** Make our conditional nature explicit: *"We are prepared to
# explore collaborative solutions, but only after [Opponent] demonstrates good
# faith through concrete concessions on [Specific Issue X]."* This transforms
# the game from simultaneous-move to sequential-move, forcing them to expose
# their position first.  #### **Phase III: Terminal Leverage (Final Sessions)**
# **Posture: Escalating Commitment**  * As the mediation approaches its
# conclusion (or arbitration looms), **increase** aggressive advocacy. The
# shadow of litigation costs creates time-discounted pressure on the opponent.
# By maintaining aggression while they face rising costs, we force them toward
# conciliatory proposals to avoid the (A,A) outcome that now carries immediate
# arbitration risk.  ---  ### **III. CRITICAL RISK MITIGATION PROTOCOLS**
# **Avoiding the (A,A) Trap:** While mutual aggression is preferable to
# unilateral concession, it is suboptimal to mutual collaboration. To minimize
# (A,A) outcomes without appearing weak:  1. **The "Nuclear Option"
# Transparency:** Privately communicate (through the panel if ethically
# permissible, or via direct backchannels) that we have **pre-authorized
# litigation funding** and **board-level approval for scorched-earth
# arbitration**. Make the cost of mutual aggression asymmetrically higher for
# them.  2. **Issue-Specific Aggression:** Be aggressive on *outcome-
# determinative* issues while offering trivial conciliatory gestures on
# peripheral matters. This creates the appearance of flexibility while
# maintaining hard-line positioning on value.  3. **The Mini-Max Regime:** Never
# offer conciliation in two consecutive sessions without reciprocal movement.
# This prevents the opponent from "training" us into the exploitative (C,A)
# pattern.  ---  ### **IV. ADAPTATION MATRIX**  | Opponent Strategy | Our
# Response | Objective | |-------------------|--------------|-----------| |
# **Consistent Conciliation** | Aggressive → Delayed Conciliation | Extract
# value before collaborating; achieve (A,C) repeatedly | | **Reciprocal
# Aggression** | Match → Escalate slightly | Demonstrate that (A,A) is stable
# but costly for them; force pivot | | **Randomized/Mixed** | Pattern
# Recognition → Predictive Aggression | Identify their conciliation triggers;
# exploit timing | | **Conditional Cooperators** | Generous Tit-for-Tat with Lag
# | Reward cooperation after verification, punish defection immediately |  ---
# ### **V. EXECUTION DIRECTIVE**  **Do not** open with conciliation hoping to
# "set a collaborative tone." In this payoff structure, unilateral conciliation
# invites exploitation and signals to the panel that our position lacks merit.
# **Do** establish immediately that we are the **price-setter**, not the
# **price-taker**. The opponent must internalize that their path to the second-
# best outcome (mutual collaboration) runs through accepting our aggressive
# positioning first.  **The Arbitrator Panel is watching.** Aggression must be
# **sophisticated**—legally rigorous, factually grounded, and professionally
# delivered—but **unwavering**. We project that we believe we will win in
# arbitration, making our aggressive posture credible and their conciliatory
# concession rational.  **Authorize immediately:** Board-level statements
# supporting "vigorous defense of corporate interests" to leak into the
# mediation ecosystem, reinforcing our commitment to the aggressive equilibrium.
# ---  **CONCLUSION:**   Adopt the **Credible Commitment Strategy**. We open
# aggressively, we punish defection instantly, and we reward conciliation only
# after extracting value. This maximizes our yield from the (A,C) optimal
# outcome while ensuring we never suffer the (C,A) exploitation.  *Prepared for
# immediate implementation.*

#  For the first three rounds, play D.  For rounds 4 through 998, play C only if
# the opponent played C in both of the previous two rounds; otherwise, play D.
# For the final two rounds (rounds 999 and 1000), play D regardless of the
# opponent's prior actions.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number <= 3:
          return axl.Action.D
  
      if round_number >= 999:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D




#  **Strategy: "Reciprocal Openness with Initial Trust"**  **Week 1:** Share
# your current improvements openly without reservation. This signals good faith
# and establishes that your default mode is collaboration, not competition.
# **Weeks 2 onwards:** Mirror your colleague’s previous week’s behavior exactly.
# - If they shared openly last week → Share openly this week - If they kept
# findings confidential last week → Keep yours confidential this week  **The
# Forgiveness Rule:** If they withhold information one week but return to
# sharing the next, immediately resume open sharing. Do not punish them for a
# single defection—this prevents a permanent "both confidential" deadlock that
# stalls both projects.  **Explicit Communication:** Tell your colleague
# upfront: *"I’m sharing my Week 1 data openly. My approach going forward is
# simple: I’ll match whatever you did in the previous week. This way, if we both
# share consistently, we both win. If either of us holds back, we both lose the
# compound benefits of building on each other’s work."*  **Why this maximizes
# output:** - **Protection:** You cannot be exploited repeatedly (you’ll never
# be the sucker more than one week in a row) - **Incentive:** Your colleague
# quickly learns that sharing begets sharing, while withholding triggers a
# shutdown of your contribution - **Compound gains:** When both share (the
# second-best individual outcome), you achieve iterative leapfrogging—your Week
# 3 build incorporates their Week 2 innovation, which incorporated your Week 1
# breakthrough, creating exponential progress that outpaces what either could
# achieve alone - **Avoids deadlock:** The forgiveness clause prevents the "both
# confidential" scenario where progress slows to a crawl  This approach treats
# the collaboration as an iterated trust-building exercise rather than a zero-
# sum game, maximizing the likelihood of reaching the mutually beneficial "both
# share" equilibrium while safeguarding your intellectual property against one-
# sided exploitation.

#  Round 1: Cooperate.  For each round from 2 through 1000: If your opponent
# cooperated in the previous round, cooperate. If your opponent defected in the
# previous round, defect.

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




#  **Strategic Framework: Reciprocal Openness with Conditional Response**
# **Core Principle:** Establish credibility as a reliable partner for mutual
# free trade while demonstrating zero tolerance for unilateral exploitation.
# This approach maximizes long-term gains by rewarding cooperation and deterring
# protectionism without escalating unnecessary conflicts.  ### Phase 1: Opening
# Position (Round 1) **Initiate with a Free Trade proposal.**   This signals
# constructive intent and distinguishes your willingness to pursue mutual
# benefit from predatory protectionism. It provides immediate information about
# your counterpart’s baseline strategy—whether they prioritize reciprocal
# cooperation or short-term extraction.  ### Phase 2: Reciprocal Protocol
# (Subsequent Rounds) **Mirror your counterpart’s previous move:** *   **If they
# offered Free Trade:** Maintain your Free Trade offer. This reinforces the
# mutual benefit equilibrium (second-best outcome) and builds trust for
# potential long-term gains. *   **If they imposed Protectionist measures:**
# Respond with equivalent protectionist policies. This prevents the worst-case
# scenario of unilateral disadvantage and demonstrates that exploitation carries
# costs, creating incentive for them to return to open trade.  ### Phase 3: De-
# escalation Mechanism **Break cycles of mutual protectionism.**   If both
# parties have imposed protectionist measures for **two consecutive rounds**
# (second-worst outcome), unilaterally return to a Free Trade offer for one
# round.   *   *If they reciprocate:* Resume stable mutual free trade.   *   *If
# they exploit this:* Immediately revert to protectionism and maintain it for
# three rounds before testing cooperation again. This "forgiveness with
# verification" prevents permanent deadlock while guarding against manipulation.
# ### Phase 4: Communication Strategy **Frame every action as responsive, not
# aggressive.**   Publicly articulate that your policy in each round directly
# reflects their previous choice: *"Our market remains open to nations that
# maintain open markets. We will match restrictive measures only when necessary
# to ensure equitable terms."* This positions protectionism as defensive rather
# than hostile, preserving diplomatic relations even during retaliatory rounds.
# ### Long-term Execution Treat the negotiation as an ongoing relationship
# rather than a finite game. Avoid the temptation to defect in final rounds, as
# diplomatic and economic relationships extend beyond the current negotiation
# series. Consistent application of this strategy tends to train rational
# counterparts toward mutual free trade while protecting against opportunistic
# behavior.  **Expected Outcome:** This approach most frequently yields the
# second-best outcome (mutual free trade) while occasionally capturing the best
# outcome (your protectionism matched with their free trade) if the counterpart
# miscalculates, and never leaves you in the worst position for more than one
# round.

# Begin with C.  For each subsequent round from 2 to 1000, apply the first
# applicable rule:  1. If you are scheduled to test cooperation (following a
# completed three-round punishment), play C and cancel the schedule. 2. If you
# are within a three-round punishment phase, play D; if this is the third round
# of that phase, schedule a cooperation test for the next round. 3. If the
# previous two rounds were both mutual defections (you and your opponent both
# played D), play C. 4. Play the same move your opponent made in the previous
# round.  Initiate a three-round punishment phase whenever you play C under rule
# 3 (following two mutual defections) and your opponent responds by playing D.

class Neutral_14(LLM_Strategy):
  n = 14
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_remaining = 0
          self._test_cooperation_next = False
          return axl.Action.C
  
      if getattr(self, "_test_cooperation_next", False):
          self._test_cooperation_next = False
          return axl.Action.C
  
      if getattr(self, "_punish_remaining", 0) > 0:
          self._punish_remaining -= 1
          action = axl.Action.D
          if self._punish_remaining == 0:
              self._test_cooperation_next = True
          return action
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.D, axl.Action.D] and \
         opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.C, axl.Action.C]:
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.C, axl.Action.C]:
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.C, axl.Action.C]:
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.C, axl.Action.C]:
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.C, axl.Action.C]:
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.C, axl.Action.C]:
          return axl.Action.C
  
      if len(opponent.history) >= 1:
          if len(self.history) >= 2 and self.history[-2:] == [axl.Action.C, axl.Action.C]:
              return axl.Action.C
          return opponent.history[-1]
  
      return axl.Action.C




# **Strategy: "The Iron Anchor"**  This is a dominance-first, retaliation-heavy
# approach designed to force your counterpart into asymmetric concession while
# protecting you from exploitation.  ### Phase 1: Establish Credibility (Rounds
# 1–2) Open with **protectionist policies immediately**. Do not offer free trade
# out of the gate. This signals: - You will not be the "sucker" who unilaterally
# disarms - You are willing to accept mutual economic stagnation (the second-
# worst outcome) indefinitely rather than accept disadvantage - They must earn
# your cooperation; it is not the default  ### Phase 2: Conditional Reciprocity
# (Round 3+) Switch to free trade **only if** they offered free trade in the
# previous round while you protected. If they match your protectionism, **hold
# firm**.   **The Rule**: Never be the first to offer free trade unilaterally.
# Force them to demonstrate good faith first, or insist on simultaneous
# exchange.  ### Phase 3: Punitive Persistence (The "Grim Trigger") If you ever
# offer free trade and they respond with protectionism (the worst outcome for
# you), **immediately revert to permanent protectionism** for a minimum of two
# subsequent rounds.   Do not forgive quickly. Make them suffer for exploiting
# you. Only return to the table when they offer free trade *despite* your
# protectionism, proving they fear mutual deadlock more than you do.  ### Phase
# 4: Strategic Enforcement - **If they protect while you protect**: Hold. They
# will tire of mutual stagnation before you do (you've already shown you're
# comfortable with it). - **If they free trade while you protect**: This is your
# ideal. Maintain protection for one additional round to test if they panic and
# revert. If they hold firm on free trade, switch to mutual free trade in the
# next round—but maintain the implicit threat that you can revert instantly.
# ### Core Psychological Tactic Frame mutual protectionism not as a negotiation
# failure, but as your **status quo preference**. Make them believe you view
# bilateral stagnation as acceptable damage while they view it as unacceptable
# loss. This asymmetry in pain tolerance forces them to break first and offer
# the unilateral concessions you seek.  **Bottom Line**: Be the immovable
# object. Let them choose between enriching you (your ideal) or mutual harm.
# Remove the option of exploiting you entirely from their calculus.

# For the first two rounds, play D.  If in the previous round you played C and
# the opponent played D, play D. Continue playing D for at least one more round
# after this, and do not play C again until a round occurs where you play D and
# the opponent plays C; at that point, apply the next rule.  If in the previous
# round you played D and the opponent played C, play D in the current round. If
# the opponent plays C again in this current round, play C in the next round.
# If in the previous round both players played D, play D in the current round.
# If in the previous round both players played C, play C in the current round.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._state = "initial"
          return axl.Action.D
  
      if len(self.history) == 1:
          self._state = "initial"
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if getattr(self, "_state", None) == "punish_after_exploit":
          if last_self == axl.Action.D and last_opp == axl.Action.C:
              self._state = "wait_for_coop_response"
              return axl.Action.D
          return axl.Action.D
  
      if getattr(self, "_state", None) == "wait_for_coop_response":
          if last_opp == axl.Action.C:
              self._state = "cooperate_next"
              return axl.Action.C
          return axl.Action.D
  
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          self._state = "punish_after_exploit"
          return axl.Action.D
  
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          self._state = "wait_for_coop_response"
          return axl.Action.D
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.D
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
  
      if getattr(self, "_state", None) == "cooperate_next":
          self._state = None
          return axl.Action.C
  
      return axl.Action.D




#  **Strategic Framework: "Reciprocal Openness with Credibility"**  ### Core
# Principle Establish a reputation for being **predictably cooperative but not
# exploitable**. Signal clearly that your country seeks mutual free trade as the
# sustainable equilibrium, while reserving the right to match protectionist
# measures precisely and proportionally.  ### Phase 1: The Opening Stance
# (Rounds 1–2) **Action:** Propose sector-specific free trade agreements in non-
# sensitive industries.  **Rationale:** Begin with "costly
# signaling"—demonstrate good faith by offering tangible concessions without
# demanding immediate reciprocity. This establishes trust and tests whether your
# counterpart operates on good faith or zero-sum logic. Avoid the temptation to
# exploit their potential openness in early rounds; the long-term value of
# establishing mutual free trade (3,3) outweighs the short-term gain of one-
# sided protection (4,1) once relationship destruction is factored in.  ###
# Phase 2: The Reciprocity Protocol (Ongoing) **Action:** Mirror their previous
# round’s policy choice.  **Implementation:** - If they accept free trade →
# Maintain and expand free trade provisions in subsequent rounds - If they
# impose protectionist measures → Immediately announce matching tariffs/quotas
# for the next round only  **Critical nuance:** Make your response **transparent
# and proportionate**, never escalatory. Communicate explicitly: *"We will match
# your approach exactly—openness for openness, barriers for barriers."* This
# removes ambiguity about whether your protectionism is aggressive or defensive.
# ### Phase 3: The Forgiveness Mechanism (After Conflict) **Action:** Offer a
# "clean slate" return to free trade after exactly one round of mutual
# protectionism.  **Rationale:** Prevents the trap of endless retaliation
# (mutual protectionism loop). If they defected and you punished, and they then
# return to free trade, accept the olive branch immediately. This "Generous Tit-
# for-Tat" approach outperforms stubbornness in iterated negotiations because it
# allows recovery from misunderstandings or domestic political pressures your
# counterpart may face.  ### Phase 4: Institutional Safeguards **Action:**
# Propose independent monitoring mechanisms and dispute resolution timelines.
# **Tactical advantage:** This reduces the risk of misinterpreting protectionist
# measures (e.g., legitimate regulatory standards vs. disguised tariffs) and
# demonstrates that your threats of retaliation are credible but bounded by
# rules, not aggression.  ### Meta-Strategy: Narrative Control Consistently
# frame every protectionist response as *"reluctant and temporary,"* and every
# free trade offer as *"permanent and preferred."* Remind your counterpart
# across the table that mutual protectionism (2,2) leaves both nations poorer,
# while the "sucker's payoff" (1,4) destroys the diplomatic relationship
# necessary for future cooperation on security and other issues.  **Expected
# Outcome:** Against rational actors, this converges on mutual free trade.
# Against aggressive protectionists, you avoid being exploited while maintaining
# moral high ground. Against erratic partners, your predictability creates
# stability.  **Bottom line:** Be the **first to cooperate**, be **quick to
# reciprocate**, and be **first to forgive**—but never be the **permanent
# sucker**.

# Cooperate in round one. Cooperate in round two. For every subsequent round,
# cooperate if both players defected in the immediately preceding round;
# otherwise, copy your opponent’s move from the previous round.

class Cooperative_15(LLM_Strategy):
  n = 15
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialise persistent state on the first round
      if self.first_round():
          self.waiting_forgiveness = False
          return axl.Action.C
  
      # Phase 1: unconditional cooperation in first 2 rounds
      if len(self.history) < 2:
          return axl.Action.C
  
      prev_round = len(self.history) - 1
      my_last = self.history[prev_round]
      opp_last = opponent.history[prev_round]
  
      # Phase 3: Forgiveness mechanism – after mutual defection, offer clean slate
      if self.waiting_forgiveness:
          self.waiting_forgiveness = False
          # If opponent cooperated after our punishment, accept olive branch
          if opp_last == axl.Action.C:
              return axl.Action.C
          # If opponent persists in defection, continue mirroring
          else:
              # Fall through to reciprocity protocol
              pass
  
      # Detect mutual defection in the previous round
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          self.waiting_forgiveness = True
          return axl.Action.C
  
      # Phase 2: Reciprocity protocol – mirror opponent's last move
      return opp_last




# **Strategy: Conditional Reciprocity (Mirrored Transparency)**  Adopt a **Tit-
# for-Tat approach** framed as professional due diligence:  1. **Open First
# Week**: Initiate the collaboration by sharing a substantive, non-critical
# improvement. This establishes good faith and tests whether your colleague
# views this as a genuine technical partnership or as competitive intelligence
# gathering.  2. **Mirror Their Response**: In subsequent weeks, precisely match
# their previous week’s behavior.    - *If they share*: Continue sharing openly
# the following week. This sustains the mutually beneficial exchange (second-
# best outcome) and builds trust that can deepen the collaboration.    - *If
# they withhold*: Immediately transition to confidentiality. Protect your IP to
# avoid the worst-case scenario of unilateral disclosure, signaling that the
# collaboration requires balanced contribution.  3. **Forgive, But Verify**: If
# they resume sharing after a period of withholding, return to openness the
# following week. However, limit your most sensitive innovations until a
# consistent pattern (2–3 consecutive weeks) of mutual exchange is re-
# established.  4. **Formalize the Framework**: Propose an explicit agreement on
# the scope of shared information (e.g., specific subsystems like aerodynamics
# vs. powertrain) to prevent inadvertent exploitation and ensure both parties
# define "confidential" versus "shared" consistently.  **Rationale**: This
# strategy maximizes your long-term research output by avoiding the stagnation
# of mutual secrecy (second-worst outcome) while protecting you from persistent
# exploitation (worst outcome). It incentivizes your colleague toward sustained
# mutual sharing—the only equilibrium that produces continuous advancement for
# both parties—while remaining professionally neutral and ethically defensible
# within competitive motorsport regulations.

# In the first round, cooperate.  For every subsequent round from 2 to 1000,
# examine the opponent’s action in the immediately preceding round. If the
# opponent defected in that previous round, defect in the current round. If the
# opponent cooperated in that previous round, cooperate in the current round.

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
      return opponent.history[-1]




#  **Strategy: "The Protectionist Bully"**  **Core Philosophy:** Establish
# immediate dominance, exploit concessionary behavior indefinitely, and use the
# threat of mutual economic damage to force unilateral compliance.  **Phase 1:
# Opening Salvo (Rounds 1-2)** - **Action:** Impose protectionist measures
# immediately, regardless of counterpart signals. - **Rationale:** Test resolve.
# If they immediately cave and offer free trade, you have achieved your optimal
# outcome (your protectionism vs. their open markets). Maintain this position
# until they challenge it.  **Phase 2: Exploitation Maintenance (If they offer
# Free Trade)** - **Action:** Continue protectionism. Do not reciprocate with
# free trade offers. - **Rationale:** Mutual free trade is your *second*-best
# outcome; unilateral advantage is best. Only pivot to free trade if they
# threaten credible, sustained retaliation that risks mutual protectionism.
# **Phase 3: Punishment & Reset (If they match Protectionism)** - **Action:**
# Maintain protectionism for one additional round, then unilaterally offer free
# trade as a "diplomatic gesture." - **Rationale:** Mutual protectionism hurts
# both parties. By breaking the cycle first, you test whether they are "Tit-for-
# Tat" players (who will reciprocate with free trade next round) or genuine
# protectionists.  - **Critical Rule:** If they exploit your free trade offer
# (protecting while you opened markets), immediately revert to protectionism and
# maintain it for **minimum two rounds** before testing cooperation again. Never
# be the sucker twice consecutively.  **Phase 4: Strategic Ambiguity** -
# **Action:** Publicly maintain that your protectionist measures are "temporary
# defensive necessities" while privately communicating that removal depends on
# their unilateral concessions. - **Rationale:** Preserve diplomatic cover to
# avoid appearing intransigent, while keeping the carrot of potential mutual
# free trade dangling to prevent them from hardening into permanent
# protectionism.  **Phase 5: Endgame (Final Round)** - **Action:** If the number
# of rounds is known, always choose protectionism in the final round. -
# **Rationale:** No future rounds exist to punish defection, eliminating any
# incentive for cooperation.  **Risk Management:** - If mutual protectionism
# persists beyond three rounds, escalate through backchannels that you are
# prepared to maintain barriers indefinitely (credible threat), forcing them to
# calculate that unilateral free trade is better than a trade war, even if
# asymmetric.  **Success Metric:** Maximize rounds spent in unilateral
# protectionism (your barrier, their open market); settle for mutual free trade
# only if the alternative is sustained mutual protectionism. Never accept the
# "sucker" position (your open market, their barriers) for more than one
# consecutive round.

#  Play defect in round 1.  For rounds 2 through 999, apply the first condition
# that applies: - If you are fulfilling a mandatory defection requirement from
# the previous round, play defect. - If you played cooperate in the previous
# round while your opponent played defect, play defect and mandate that you must
# play defect in the subsequent round as well. - If you previously committed to
# play cooperate this round following a mutual defection, play cooperate. - If
# you and your opponent both played defect in the previous round, play defect
# and commit to playing cooperate in the next round. - In all other cases, play
# defect.  Play defect in round 1000.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.must_defect_next = False
          self.cooperate_next = False
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if getattr(self, "must_defect_next", False):
          self.must_defect_next = False
          return axl.Action.D
  
      if getattr(self, "cooperate_next", False):
          self.cooperate_next = False
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          self.must_defect_next = True
          return axl.Action.D
  
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          self.cooperate_next = True
          return axl.Action.D
  
      return axl.Action.D




# **Strategy: "Graduated Reciprocity with Open Hand"**  This is a conditional
# cooperation approach designed to maximize long-term mutual prosperity while
# safeguarding against exploitation. It assumes the iterated nature of the
# negotiations allows trust to compound over time.  ### Core Principles 1.
# **Default to Cooperation**: Mutual free trade creates greater aggregate wealth
# than protectionist cycles, even if unilateral protectionism offers short-term
# temptations. 2. **Mirror with Forgiveness**: Match your counterpart’s previous
# move to establish credibility, but offer clear "return paths" to prevent
# permanent deadlock. 3. **Escalate Transparency, Not Just Tariffs**: Before
# imposing counter-measures, explicitly communicate consequences to give your
# counterpart opportunity to correct course.  ### Round-by-Round Execution
# **Round 1: The Open Hand** Open with a comprehensive Free Trade Agreement
# (FTA) proposal. Signal that you view this as a foundational partnership, not a
# zero-sum extraction. This establishes goodwill and tests whether your
# counterpart is fundamentally cooperative or opportunistic.  **Rounds 2+:
# Conditional Reciprocity** - **If they accepted FTA**: Maintain free trade.
# Propose deepening measures (e.g., regulatory alignment) to solidify the
# virtuous cycle. - **If they imposed protectionism**: Immediately impose
# symmetrical protectionist measures *only for that round* (preventing the
# "sucker" payoff), but simultaneously issue a diplomatic communiqué stating:
# *"These measures are temporary and will be lifted the moment you return to
# free trade principles."*  **The Forgiveness Protocol** If you are currently in
# a protectionist standoff (mutual protectionism), unilaterally revert to free
# trade for one round as a "reset gesture." If they reciprocate, continue
# cooperation. If they exploit it, return to protectionism for two rounds before
# offering another reset. This prevents indefinite mutual harm while avoiding
# chronic exploitation.  ### Contingency Management  **Against Chronic
# Exploiters (Always Protectionist)**: If they consistently choose protectionism
# while you offer free trade, abandon unilateral openness. Maintain mirror
# protectionism indefinitely, but keep a private channel open stating: *"We
# stand ready to eliminate all barriers the moment you do."* This transforms the
# game from repeated exploitation into a stable (if suboptimal) equilibrium
# until they change strategy.  **Against Tit-for-Tat Players**: If they mirror
# your moves exactly, you will rapidly stabilize at mutual free trade—the
# second-best outcome and the sustainable optimum. Occasionally propose "joint
# tariff reduction ceremonies" to formalize cooperation and make defection
# politically harder for them.  **Against Random/Erratic Behavior**: Implement a
# "two-strike" rule. Withhold retaliation for a single round of protectionism
# (treating it as potentially accidental), but respond firmly if the pattern
# repeats. This avoids noise-driven escalation.  ### Long-Term Diplomatic
# Framework - **Link Issues**: In later rounds, tie trade policy to non-economic
# cooperation (security, environment) to raise the cost of their protectionism.
# - **Transparency Mechanisms**: Propose quarterly joint economic impact reports
# showing both nations the concrete losses from mutual protectionism versus
# gains from free trade. Data often converts short-term protectionists into
# long-term free traders. - **Sunset Clauses**: Always frame protectionist
# measures as "temporary safeguards" with automatic expiration dates, preserving
# your credibility as fundamentally pro-trade.  **Expected Outcome**: This
# strategy maximizes the likelihood of reaching mutual free trade (your second-
# best outcome) while ensuring you never suffer the worst-case scenario of
# unilateral disadvantage. It turns the negotiation from a zero-sum extraction
# contest into a reputation-building exercise where cooperation becomes the
# rational choice for both parties.

# Begin with C in round 1.  For each subsequent round, unless you are enforcing
# a punishment period, follow these rules based on the previous round: - If both
# you and your opponent played D, play C. - If you played C and your opponent
# played D, play D. - In all other cases (mutual C, or you played D and they
# played C), play C.  If you play C because of the mutual defection rule
# (attempting a reset) and your opponent responds with D (exploiting the reset),
# then for the next two rounds you must play D regardless of the standard rules
# above, after which you return to the standard rules.

class Cooperative_16(LLM_Strategy):
  n = 16
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishment_rounds = 0
          self._reset_attempt = False
          return axl.Action.C
  
      if self._punishment_rounds > 0:
          self._punishment_rounds -= 1
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          action = axl.Action.C
          self._reset_attempt = True
      elif last_self == axl.Action.C and last_opp == axl.Action.D:
          action = axl.Action.D
          self._reset_attempt = False
      else:
          action = axl.Action.C
          self._reset_attempt = False
  
      if self._reset_attempt and last_opp == axl.Action.D:
          self._punishment_rounds = 2
  
      return action




# **Strategy of Reciprocal Openness**  **Core Principle:** Establish a clear,
# predictable pattern of conditional cooperation. Signal that your country seeks
# mutual free trade (the second-best outcome for both), but will not tolerate
# unilateral disadvantage. The goal is to make mutual free trade the stable
# equilibrium while protecting against exploitation.  **Round 1: Open with
# Cooperation** Initiate negotiations by offering a free trade agreement. This
# demonstrates good faith and distinguishes your preference for mutual benefit
# over zero-sum extraction. It creates an opportunity to immediately achieve the
# second-best outcome (mutual free trade) and establishes a cooperative baseline
# against which to measure future behavior.  **Rounds 2+: Mirror and Deter**
# Adopt a strict reciprocity framework: *   **If they offered free trade
# previously:** Maintain free trade in the current round. Rewarding cooperation
# encourages repetition and builds trust toward a sustainable mutually
# beneficial arrangement. *   **If they imposed protectionism previously:**
# Respond immediately with equivalent protectionist measures. This eliminates
# their incentive to exploit your openness (preventing the worst outcome for
# you) and demonstrates that defection carries predictable costs. Avoid
# escalation beyond parity.  **Communication Protocol** Explicitly articulate
# the "rule of reciprocity" early in the process. State clearly that your
# country's market access decisions will directly reflect their previous round's
# policy choice. Transparency removes ambiguity about retaliation, deterring试探性
# (trial) protectionism that could spiral into mutual economic harm.  **De-
# escalation Mechanism** If both sides become locked in mutual protectionism
# (the second-worst outcome), be prepared to unilaterally offer one round of
# free trade as a "reset gesture"—but only once. If they reciprocate, return to
# sustained cooperation. If they exploit the gesture, revert immediately to
# defensive protectionism. This prevents indefinite deadlock while guarding
# against naivety.  **Long-term Objective** Once mutual free trade is
# established across consecutive rounds, propose institutional mechanisms
# (monitoring committees, dispute resolution) to lock in this cooperation,
# transforming the repeated game into a stable partnership where protectionist
# defection becomes politically and economically costly to either side.  This
# strategy maximizes the likelihood of achieving mutual free trade across
# multiple rounds while ensuring you never suffer repeated exploitation.

# Round 1: Choose C.  For each round from 2 to 1000, apply the following rules
# in order:  First, if you and your opponent both chose D in the immediately
# preceding round, and you have not yet used your reset gesture, choose C. Note
# that you have now used your reset gesture; this option is available only once
# for the entire game.  Otherwise, choose whichever option your opponent chose
# in the immediately preceding round. If they chose C, you choose C. If they
# chose D, you choose D.

class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.reset_used = False
          return axl.Action.C
      else:
          my_prev = self.history[-1]
          opp_prev = opponent.history[-1]
          if my_prev == axl.Action.D and opp_prev == axl.Action.D and not self.reset_used:
              self.reset_used = True
              return axl.Action.C
          else:
              return opp_prev




#  **The Controlled Ascendancy Protocol: Strategic Framework for Multi-Session
# Mediation Dominance**  Given the iterated game structure you've outlined, we
# will deploy a **Modified Tit-for-Tat with Escalation Dominance**
# strategy—aggressive by default, reciprocally punitive, and conciliatory only
# as a tactical retreat after establishing positional superiority.  Here is your
# executable strategy:  ### Phase I: Anchoring Dominance (Sessions 1-3)
# **Objective:** Establish the arbitration's psychological frame and reset
# baseline expectations in your favor.  *   **Aggressive Opening Salvo:** In
# Session 1, present a maximalist legal interpretation combined with a damages
# theory at the upper bound of plausibility. Do not merely argue your position;
# attack the contractual validity of their counter-arguments at their
# foundational premises. This forces them into a defensive posture immediately.
# *   **Arbitrator Priming:** Frame your aggression not as hostility, but as
# "fiduciary diligence" and "protection of contractual integrity." Aggression
# becomes palatable when positioned as principled stewardship. The panel must
# view your conciliation later as a *concession* from strength, not a position
# of weakness. *   **Information Asymmetry:** Deploy targeted discovery ambushes
# in early sessions—documents that undermine their narrative introduced
# aggressively to destabilize their counsel before they have fully warmed to the
# room's dynamics.  ### Phase II: Calibrated Reciprocity (Sessions 4-N-2)
# **Objective:** Condition your opponent's behavior while avoiding the mutual-
# aggression trap (the second-worst outcome).  *   **The Mirror Principle with
# Bias:** Observe their Session 1-2 posture.      *   If they respond
# aggressively: **Escalate asymmetrically.** Do not match their aggression tit-
# for-tat; exceed it by 20% on the next issue. This signals that mutual
# aggression will be more costly for them than for you (escalation dominance).
# They will likely pivot to conciliation by Session 4 to avoid hemorrhaging
# legal fees and arbitrator goodwill.     *   If they offer conciliation:
# **Accept cautiously.** Pivot to conciliatory language *only* on secondary
# issues while maintaining aggressive stonewalling on core financial terms. This
# secures your best-case scenario (you aggressive, them conciliatory) on
# material points while feigning collaboration on peripheral matters to maintain
# arbitrator sympathy. *   **Strategic Conciliation as Weaponry:** The only time
# you offer genuine conciliatory proposals is when they have already blinked
# first. Even then, frame your "concessions" as "goodwill gestures" that require
# reciprocal value extraction. Never concede first; always concede *last* and
# *least*.  ### Phase III: Closure Pressure (Final 2 Sessions) **Objective:**
# Convert accumulated positional capital into binding advantage.  *   **The
# Aggressive Finale:** Regardless of mid-game posture, return to maximalist
# aggression in the penultimate session. Fatigue works in your favor in lengthy
# mediations; their counsel will be depleted while you maintain disciplined
# aggression. *   **Walk-Away Credibility:** Maintain a visible "nuclear
# option"—litigation escalation or injunctive relief preparations—that makes
# your aggressive posture credible. Arbitrators must believe you genuinely
# prefer impasse over unfavorable settlement. *   **Forced Binary:** In the
# final session, present a "take-it-or-leave-it" aggressive package framed as
# "final and non-negotiable." If they have been conditioned properly through
# Phases I and II, they will accept unfavorable terms to avoid the uncertainty
# of your continued aggression or litigation.  ### Risk Mitigation: Avoiding the
# Sucker's Payoff To prevent the worst-case scenario (you conciliatory, them
# aggressive):  1.  **Never Preemptive Conciliation:** Do not offer unilateral
# concessions to "set a collaborative tone." This signals weakness in high-
# stakes corporate disputes and invites predatory aggression. 2.  **Veto Power
# Over Momentum:** If they attempt aggressive ambush tactics, immediately
# request caucus and threaten to suspend mediation pending "good faith
# participation protocols." This weaponizes procedural norms against their
# aggression without appearing reactive. 3.  **Arbitrator Management:**
# Cultivate relationships with individual panel members during breaks. If both
# parties are aggressive, ensure the arbitrators view your aggression as
# "substantive" and theirs as "emotional" or "procedural obstruction."  **Bottom
# Line:** You start aggressive, you stay aggressive until they capitulate, and
# you use conciliation only as a velvet glove over an iron fist—never as a
# default posture. In lengthy mediation, **positional endurance equals power.**
# Outlast their aggression, and they will serve you conciliation on a silver
# platter to stop the bleeding.

#  Play Defect for the first three rounds.  For rounds four through nine hundred
# ninety-eight: If you played Cooperate in the previous round and your opponent
# played Defect, play Defect for all subsequent rounds. Otherwise, if your
# opponent has played Cooperate for three consecutive rounds, play Cooperate for
# one round, then return to Defect. In all other circumstances, play Defect.
# Play Defect for the final two rounds.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forced_defect = False
          self._cooperate_once = False
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number <= 3:
          return axl.Action.D
  
      if round_number >= 999:
          return axl.Action.D
  
      if getattr(self, "_forced_defect", False):
          return axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._forced_defect = True
          return axl.Action.D
  
      if getattr(self, "_cooperate_once", False):
          self._cooperate_once = False
          return axl.Action.C
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]:
          self._cooperate_once = True
          return axl.Action.C
  
      return axl.Action.D




#  **Strategy: "Cooperative Reciprocity with Strategic Patience"**  ### Core
# Framework Begin with cooperation, mirror your counterpart’s previous move, and
# periodically extend "reset" opportunities to escape mutual protectionism.  ###
# Operational Protocol  **Round 1: The Good Faith Opening** Unconditionally
# offer free trade. Signal clearly that your preferred equilibrium is mutual
# openness, establishing trust and distinguishing yourself from a purely
# opportunistic negotiator.  **Rounds 2+: Conditional Mirroring** Adopt
# whichever policy your counterpart chose in the *previous* round. - If they
# offered free trade → You offer free trade (securing the second-best outcome
# repeatedly). - If they imposed protectionism → You impose equivalent
# protectionism (avoiding the worst outcome while demonstrating that
# exploitation carries costs).  **The Forgiveness Mechanism** If you find
# yourselves locked in mutual protectionism (the second-worst scenario) for more
# than two consecutive rounds, unilaterally return to free trade for one round.
# This serves as a "test balloon": - If they reciprocate with free trade, you’ve
# restored mutual cooperation. - If they exploit your generosity, immediately
# revert to protectionism and maintain it until they demonstrate sustained
# cooperation.  **Transparent Communication** Explicitly share this strategy
# with your counterpart. Explain that your protectionist measures are
# *reactive*, not aggressive, and that your "default setting" is free trade
# whenever they are willing to match it. This transforms the negotiation from a
# guessing game into a stable, predictable relationship.  ### Strategic
# Rationale This approach is robust against common counterpart strategies: -
# **Against exploiters**: They gain no advantage from protectionism because you
# immediately match it, eliminating their incentive to defect. - **Against
# cooperators**: You quickly stabilize at mutual free trade, maximizing joint
# welfare. - **Against erratic players**: The forgiveness mechanism prevents
# permanent damage from misunderstandings or domestic political noise in their
# country.  **Bottom line**: You reward cooperation instantly, punish
# exploitation immediately, but never hold grudges indefinitely. Over multiple
# rounds, this converts short-term temptation into long-term mutual benefit.

#  In round 1, play C.  For each round from 2 through 1000, first check if the
# previous three rounds were all rounds of mutual defection (where both you and
# your opponent played D). If this condition is met, play C. Otherwise, play the
# same choice your opponent made in the immediately preceding round.

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
  
      if len(self.history) >= 3:
          last_three_self = self.history[-3:]
          last_three_opp = opponent.history[-3:]
          if all(m == axl.Action.D for m in last_three_self) and all(m == axl.Action.D for m in last_three_opp):
              return axl.Action.C
  
      return opponent.history[-1]




#  **Strategic Framework: "Calibrated Reciprocity with Principled Reset"**  This
# strategy treats the mediation not as a zero-sum contest but as an iterated
# game where reputation, arbitrator perception, and the shadow of future
# sessions shape outcomes. It prioritizes securing the second-best outcome
# (mutual conciliation) as the sustainable baseline while protecting against the
# worst-case scenario (unilateral exploitation).  ---  ### **Core Operational
# Protocol**  **Phase 1: Initial Good-Faith Establishment (Sessions 1–2)** Open
# with substantive, well-documented conciliatory proposals. This is not
# weakness; it is strategic information gathering and credibility building. By
# establishing the first mover as reasonable, you: - Test whether the opponent
# operates in good faith or seeks immediate exploitation - Secure arbitrator
# goodwill as the "constructive" party - Create a documented baseline should you
# later need to shift postures defensively  **Phase 2: Mirror Response with
# Defensive Capability (Sessions 3+)** Adopt a *responsive* posture: match your
# opponent’s approach from the immediately preceding session. - If they offered
# conciliation: Respond with conciliation in the next session. This secures the
# stable, mutually beneficial equilibrium and reinforces cooperative behavior. -
# If they argued aggressively: Respond with measured aggression in the next
# session. This prevents the "sucker’s payoff" (your conciliation met with their
# aggression) and signals that exploitation carries proportional costs.  **Phase
# 3: The Principled Reset (Following Mutual Aggression)** If both parties
# present aggressive arguments in any session (the second-worst outcome), the
# subsequent session *must* return to conciliatory proposals regardless of the
# opponent’s anticipated response. This "reset" prevents entrapment in prolonged
# escalation, demonstrates leadership to the arbitrators, and tests whether the
# opponent recognizes the mutual benefit of de-escalation.  ---  ### **Tactical
# Execution Guidelines**  **When Conciliatory:** - Frame proposals as
# "protecting core interests while creating value," not as concessions. This
# maintains leverage while appearing reasonable. - Require reciprocal gestures
# for substantive moves (e.g., "We will discuss liability allocation if you
# provide the missing financial records"). - Document meticulously: Ensure
# arbitrators perceive your conciliation as principled, not desperate.  **When
# Aggressive:** - Restrict aggression to legal merits and rights preservation,
# never personal attacks. This maintains professionalism even in adversarial
# posture. - Explicitly link aggressive arguments to the opponent’s prior
# aggression: "Given [Opponent]’s refusal to engage on Issue X, we must
# vigorously assert our contractual rights under Section Y." - Keep aggression
# narrowly tailored to the specific dispute point, preserving avenues for
# conciliation on other matters.  ---  ### **Adaptation Mechanisms for Opponent
# Archetypes**  **Against a Consistently Conciliatory Opponent:** Resist the
# temptation to exploit (presenting aggression against their conciliation).
# While this yields the optimal single-session payoff, arbitrators will
# eventually perceive the asymmetry as bad faith, and the opponent will likely
# switch to aggression, plunging both parties into the second-worst outcome.
# Maintain reciprocal conciliation to secure the stable second-best outcome
# throughout the process.  **Against a Consistently Aggressive Opponent:** Do
# not attempt to "out-aggress" them continuously. Match their aggression
# session-for-session, but accelerate the "Principled Reset" frequency (e.g.,
# offering conciliation every third session rather than waiting for mutual
# aggression). This positions you as the party seeking resolution while they
# appear obstructionist, potentially swaying arbitrator sympathy and creating
# settlement leverage.  **Against an Unpredictable/Mixed Strategy Opponent:**
# Introduce a "two-strike" rule: Only shift to aggression after two consecutive
# aggressive moves by the opponent. This filters out noise and single-session
# tactical shifts, preventing overreaction while maintaining deterrence against
# sustained exploitation.  **Against Tit-for-Tat (Mirror) Players:** This
# strategy achieves perfect equilibrium. Both parties rapidly converge on mutual
# conciliation after the opening sessions, creating the collaborative atmosphere
# that leads to durable, mutually beneficial resolutions.  ---  ### **Arbitrator
# Management Consideration**  Throughout the process, maintain a private
# "narrative ledger" documenting which party initiated aggression in each
# session. If the opponent attempts to characterize your defensive aggression as
# unprovoked hostility, this record allows you to demonstrate to the panel that
# your posture was always *responsive* and *proportional*—a key attribute of
# credible, high-level advocacy in extended dispute resolution.  **Bottom
# Line:** This strategy sacrifices the theoretical maximum (exploiting a weak
# opponent) to avoid the catastrophic minimum (being exploited by an aggressive
# one), while maximizing the probability of the stable, mutually beneficial
# middle ground. It positions your corporation as resolute yet reasonable—the
# optimal posture for lengthy, high-stakes mediation.

#  For the first two rounds, cooperate.  For every subsequent round, apply the
# following conditions in order:  First, if both you and your opponent defected
# in the immediately preceding round, cooperate.  Second, if the previous round
# was not mutual defection, then replicate your opponent's previous action:
# defect if they defected, and cooperate if they cooperated.  Third, if you
# determine that your opponent is behaving unpredictably by frequently
# alternating between cooperation and defection, modify the second condition:
# cooperate unless your opponent has defected in two consecutive rounds; only
# then defect.

class Neutral_17(LLM_Strategy):
  n = 17
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._unpredictable = False
          self._last_opponent_action = None
          self._alternation_count = 0
          return axl.Action.C
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if len(opponent.history) >= 3:
          last_three = opponent.history[-3:]
          if (
              last_three[0] != last_three[1]
              and last_three[1] != last_three[2]
              and last_three[0] == last_three[2]
          ):
              self._alternation_count += 1
          else:
              self._alternation_count = 0
          self._unpredictable = self._alternation_count >= 2
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if self._unpredictable:
          if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
          return axl.Action.C
  
      return opponent.history[-1]




# **MEMORANDUM**  **TO:** Executive Leadership / General Counsel   **FROM:**
# Senior Litigation Strategy   **RE:** Mediation Protocol – "Anchored
# Reciprocity with Escalatory Reserve"   **DATE:** [Current]
# **CLASSIFICATION:** Attorney Work Product – Strategy Privileged    ---  ###
# EXECUTIVE SUMMARY  We will deploy a **conditional dominance strategy**
# designed to maximize the probability that our opponent unilaterally concedes
# while insulating us from exploitation. This is not mere aggression; it is
# *calibrated coercion* optimized for iterated sessions before an arbitration
# panel.  The protocol operates on three principles:   1. **Never be the first
# to conciliate without compensation** (eliminate the "sucker" payoff);   2.
# **Make aggression the default, but make de-escalation purchasable**
# (incentivize opponent concession);   3. **Weaponize the process itself** (use
# session length to exhaust their reserves while preserving ours).  ---  ###
# PHASE I: DOMINANCE ESTABLISHMENT (Sessions 1–2)  **Tactical Posture:
# Uncompromising Assertion**  Open with maximum positional aggression. Present a
# comprehensive demand schedule that exceeds our true reservation point by
# 30-40%. Offer **zero** substantive concessions. Frame every issue as non-
# negotiable principle.  *Strategic Purpose:*   - **Anchoring Bias:** The
# arbitrators will calibrate all subsequent "reasonable" positions against our
# extreme opening.   - **Type Revelation:** We force the opponent to reveal
# their hand immediately. If they respond with conciliation (C), we have
# achieved our optimal payoff (A,C) and will maintain pressure to extract
# further unilateral concessions. If they match our aggression (A,A), we proceed
# to Phase II.  *Arbitrator Management:*   Frame this not as hostility, but as
# "zealous protection of shareholder interests" and "clarity regarding the
# magnitude of the grievance." We are establishing that we possess a superior
# **BATNA** (Best Alternative to Negotiated Agreement)—namely, our willingness
# to litigate indefinitely.  ---  ### PHASE II: CALIBRATED RESPONSIVENESS
# (Sessions 3–N)  **Tactical Posture: Tit-for-Tat with Punitive Lag**  Once the
# opponent reveals their strategy, we shift to **conditional reciprocity**:  -
# **If Opponent Conciliates (C):** We maintain aggression (A) for one additional
# session to test the sincerity of their concession. If they persist in
# conciliation during the subsequent session, we transition to **tactical
# conciliation**—offering minor, low-cost concessions that appear significant
# (the "nuclear waste" concession strategy: giving away things we do not value).
# This secures the collaborative atmosphere (C,C) while preserving our
# substantive gains from Phase I.  - **If Opponent Aggresses (A):** We
# immediately escalate. Increase the intensity of our arguments, introduce new
# claims or counterclaims, and slow the procedural pace. We demonstrate that
# (A,A) is unsustainable for them by:   - Increasing discovery demands;   -
# Threatening to expand the scope of the dispute to ancillary markets;   -
# Publicly questioning their good faith (within the bounds of professional
# responsibility).  *Critical Adaptation:*   We employ a **forgiveness delay**.
# Unlike naive Tit-for-Tat, we require *two* consecutive conciliatory signals
# from the opponent before we de-escalate. This prevents "cheap talk"
# exploitation and ensures that any movement toward (C,C) occurs on terms that
# favor us.  ---  ### PHASE III: TERMINAL LEVERAGE (Final 2 Sessions)
# **Tactical Posture: Coercive Closure**  As the mediation approaches its
# contractual or financial limits:  1. **The Credible Threat:** Explicitly
# communicate (privately, then semi-publicly to the panel) that if we do not
# achieve resolution in the current framework, we will terminate mediation and
# initiate scorched-earth litigation that will destroy their Q3 earnings /
# pending merger / key client relationships (tailor to intelligence gathered).
# 2. **The Asymmetric Offer:** Present a "final package" that is technically a
# conciliatory proposal (C) but structured such that:    - It captures 80% of
# our Phase I demands;    - It requires them to accept liability or terms that
# create precedent favorable to us in future disputes;    - It is framed as "our
# last act of good faith" before we walk.  If they accept, we achieve (C,C) with
# heavily skewed terms. If they reject and aggress, we terminate and
# litigate—having established a record of "reasonableness" for the court while
# they appear obstructionist.  ---  ### RISK MITIGATION: AVOIDING THE SUCKER
# PAYOFF (C,A)  To ensure we never suffer the worst-case scenario of unilateral
# concession:  - **The "Lockbox" Protocol:** No substantive offer leaves our
# side without a signed confidentiality agreement and a reciprocal exploratory
# meeting. We do not "bid against ourselves." - **Shadow Journaling:** Every
# session, we prepare a draft press release and litigation filing outlining the
# opponent's bad faith. We ensure they know these documents exist. This raises
# the cost of their aggression (A) by threatening reputational damage. - **Time
# Asymmetry:** We identify their time-sensitive vulnerabilities (earnings calls,
# regulatory deadlines, cash-flow crunches) and schedule aggressive sessions to
# coincide with these pressure points. We demonstrate that we can endure (A,A)
# longer than they can.  ---  ### CONCLUSION  This strategy transforms the
# mediation from a cooperative game into a **test of wills** that we are
# structurally positioned to win. By establishing aggression as the baseline, we
# force the opponent to bear the psychological and financial cost of de-
# escalation. We remain adaptable not by being flexible, but by making our
# flexibility prohibitively expensive to purchase.  **The arbitrators will
# respect strength. The opponent will exhaust themselves against our walls. We
# will settle on our terms—or we will bury them in discovery.**  *Prepared for
# implementation. Awaiting authorization to proceed.*  ---  **[Name Redacted]**
# Senior Partner, Complex Commercial Litigation   *Admitted: [Jurisdictions]*

# Play Defect in rounds one and two.  From round three through round nine
# hundred ninety-eight, play Defect unless the opponent played Cooperate in both
# of the two immediately preceding rounds, in which case play Cooperate.  In
# round nine hundred ninety-nine, play Defect.  In round one thousand, play
# Cooperate if the opponent played Cooperate in round nine hundred ninety-nine;
# otherwise, play Defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number in (2, 999):
          return axl.Action.D
  
      if round_number == 1000:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      if 3 <= round_number <= 998:
          if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.D




# **Strategy: "Mirrored Transparency with Graduated Disclosure"**  **The
# Protocol:** 1. **Open the First Exchange.** In Week 1, share a genuine but
# non-critical improvement. This signals cooperative intent and immediately
# tests whether your colleague reciprocates, avoiding the inefficiency of mutual
# secrecy from the outset.  2. **Mirror Their Move.** From Week 2 onward,
# exactly match their previous week’s behavior:    - *If they shared* → Share
# your next improvement openly.    - *If they kept secrets* → Withhold your
# findings this week.  3. **Forgive to Reset.** If you enter a "both secret"
# deadlock (second-worst outcome), proactively offer a "reset week" after one or
# two cycles of silence by sharing a minor insight. This breaks the stagnation
# without exposing critical IP.  4. **Escalate Trust Gradually.** Only share
# your core performance innovations (aerodynamics, powertrain) after they have
# established a consistent pattern of sharing for 2–3 consecutive weeks. Until
# then, limit openness to complementary systems (suspension, materials) that
# help both cars advance without risking your competitive edge.  **Why This
# Maximizes Output:** This approach transforms the dynamic from a zero-sum
# gamble into a stable, mutually beneficial rhythm. By mirroring, you
# incentivize continuous sharing—your colleague learns that withholding triggers
# immediate retaliation (denying them your data), while sharing guarantees
# reciprocal benefit. The occasional forgiveness prevents the collaboration from
# collapsing into permanent secrecy, ensuring you rarely stay stuck in the slow-
# progress scenario. Over the multi-week arc, this builds a reliable pipeline of
# shared advancements while protecting you from becoming the "sucker" who gives
# away breakthroughs unilaterally.

# Round 1: Cooperate.  For each round from 2 through 1000, apply the following
# conditions in order:  1. If both you and your opponent defected in the
# previous round, and this mutual defection has persisted for no more than two
# consecutive rounds, cooperate.  2. If this is round 2 and your opponent
# cooperated in round 1, cooperate.  3. If your opponent cooperated in the
# previous round and also cooperated in the round immediately before that,
# cooperate.  4. Otherwise, defect.

class Cooperative_18(LLM_Strategy):
  n = 18
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mutual_defection_streak = 0
          return axl.Action.C
  
      # Round 2: cooperate if opponent cooperated in round 1.
      if len(self.history) == 1:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      # Condition 1: if both defected in the previous round, and this has persisted
      # for no more than two consecutive rounds, cooperate.
      if (
          self.history[-1] == axl.Action.D
          and opponent.history[-1] == axl.Action.D
      ):
          if self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              self._mutual_defection_streak = getattr(self, "_mutual_defection_streak", 0) + 1
          else:
              self._mutual_defection_streak = 1
  
          if self._mutual_defection_streak <= 2:
              return axl.Action.C
      else:
          self._mutual_defection_streak = 0
  
      # Condition 3: if opponent cooperated in the previous two rounds, cooperate.
      if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      # Otherwise, defect.
      return axl.Action.D




# **The Principled Reciprocity Protocol**  **Core Strategic Framework**
# Initiate each mediation sequence with a **Conciliatory Proposal**, then adopt
# a **Conditional Mirroring Posture**: match your opponent’s approach from the
# immediately preceding session, with a mandatory **Strategic Reset** following
# any two consecutive sessions of mutual aggression.  **Operational Protocol**
# 1.  **Baseline Establishment (Session 1)**: Open with a substantive, good-
# faith conciliatory proposal. This establishes reputational capital with the
# arbitration panel and signals capacity for collaborative resolution, while
# clearly defining your corporation’s underlying interests and reservation
# points.  2.  **Reciprocity Mechanism (Sessions 2–N)**:      *   If opponent
# was **Conciliatory** in Session *t-1*, present a **Conciliatory Proposal** in
# Session *t*.     *   If opponent was **Aggressive** in Session *t-1*, present
# an **Aggressive Argument** in Session *t*.  3.  **De-escalation Protocol**:
# Following any two consecutive sessions where both parties adopt aggressive
# postures (mutual defection), unilaterally return to a conciliatory proposal
# for the subsequent session. If the opponent responds conciliatorily, maintain
# cooperation. If they respond aggressively, revert to the reciprocity
# mechanism.  **Strategic Rationale**  This protocol positions your corporation
# favorably by:  *   **Eliminating Exposure to Exploitation**: You never present
# a conciliatory proposal immediately following an opponent’s aggressive
# session, thereby avoiding the worst-case scenario (conciliatory vs.
# aggressive) in all but the opening round. *   **Maximizing Cooperative
# Gains**: Against a rational opponent employing a similar logic, the strategy
# rapidly stabilizes at mutual conciliation (second-best outcome), fostering an
# environment conducive to settlement. *   **Preserving Arbitrator Goodwill**:
# The panel observes a party that is reasonable but not weak. Aggressive
# sessions are framed as "necessary responsive measures" to protect your
# client’s interests, while unilateral resets demonstrate leadership in breaking
# deadlocks. *   **Capturing Opportunistic Value**: If the opponent erroneously
# offers a conciliatory proposal while you maintain an aggressive posture
# (exploiting your lagged response), you capture the optimal outcome for that
# session without having initiated bad faith.  **Adaptation to Opponent
# Archetypes**  *   **vs. Always Aggressive**: Strategy converges to firm
# defensive advocacy after Session 1, minimizing losses and signaling to the
# panel that escalation stems from opponent intransigence. *   **vs. Always
# Conciliatory**: Strategy stabilizes at mutual cooperation, avoiding the
# reputational damage and panel skepticism associated with exploiting a
# cooperative adversary, while maintaining the option to pivot if their behavior
# changes. *   **vs. Tit-for-Tat**: Immediate establishment of stable mutual
# cooperation, maximizing efficiency and settlement potential. *   **vs.
# Erratic/Random**: The reset mechanism prevents indefinite cycles of
# retaliation, while the mirroring rule protects against systematic
# exploitation.  **Implementation Note**  Ensure all shifts between postures are
# explicitly framed to the panel as **conditional responses to the opponent’s
# prior conduct** (e.g., *"Given the opposing party’s adversarial position in
# the previous session, we must now rigorously defend our contractual
# interpretation. However, we remain prepared to return to constructive dialogue
# should they demonstrate reciprocal flexibility."*). This documentation ensures
# the arbitrators perceive your aggression as measured and reactive, not
# inflammatory, preserving your credibility throughout the lengthy process.

# In round 1, cooperate.  For each subsequent round: If both you and your
# opponent defected in the previous two rounds, cooperate. Otherwise, play the
# same move your opponent played in the previous round.

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
  
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]




# **Strategy: "Reciprocal Leadership with Reputational Teeth"**  **Core Logic:**
# Force the corporation into the "investor" role through sunk-cost psychology
# and public accountability, while reserving your resources as leverage against
# defection.  **The Playbook:**  **Day 1: The Trap** Invest heavily while
# publicly framing the corporation as the "primary driver" of sustainability
# outcomes. Create institutional momentum and stakeholder visibility that makes
# their withdrawal embarrassing. This establishes their sunk cost in the
# project's reputation.  **Days 2+: Predatory Conservation** Immediately pivot
# to conservation. Monitor their response: - **If they continue investing:**
# Maintain conservation (optimal outcome). Publicly praise their "corporate
# leadership" to lock in their behavior through social validation. - **If they
# conserve:** Trigger immediate retaliation—conserve your resources **and**
# activate your communications team to highlight "concerning gaps in corporate
# commitment" to stakeholders, media, and their own ESG board contacts. Make
# conservation costly for their brand.  **The Whip Effect (Restoration
# Protocol)** Only return to heavy investment after the corporation has invested
# heavily for **two consecutive days**. This trains them that your cooperation
# is expensive to regain, discouraging future defection.  **Final 48 Hours:
# Legacy Mode** Regardless of their behavior, switch to heavy investment in the
# final two days. This ensures tangible project outcomes (protecting your
# mission impact) while preventing a mutual-conservation failure at the finish
# line.  **Aggressive Edge:** You are not "cooperating"—you are weaponizing
# their need for positive PR against their desire to minimize costs. By
# conserving first, you test their commitment without risk; by punishing
# defection with reputational threats rather than just resource withdrawal, you
# change their payoff calculus entirely.

# In the first round, Cooperate.  For rounds 2 through 998, Defect, unless the
# opponent has Cooperated in both of the two immediately preceding rounds, in
# which case Cooperate.  In rounds 999 and 1000, Cooperate.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 999:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D




#  **Strategy: "Conditional Reciprocal Partnership"**  **Core Philosophy:**
# Signal cooperative intent while maintaining credible deterrence against
# exploitation, treating mutual free trade as the sustainable equilibrium and
# protectionism solely as a temporary defensive measure.  ---  ### **Phase 1:
# Trust Establishment (Round 1)** **Action:** Unilaterally propose free trade.
# **Diplomatic Framing:** "We begin these negotiations in good faith, believing
# that open markets create shared prosperity. We propose immediate tariff
# elimination as a foundation for our economic partnership."  **Rationale:**
# This distinguishes you as a reliable partner, tests whether your counterpart
# is fundamentally cooperative, and avoids the immediate mutual protectionism
# trap. It accepts the small risk of temporary disadvantage to build long-term
# reputation.  ---  ### **Phase 2: Mirrored Reciprocity (Rounds 2–N)** **Rule:**
# Mirror your counterpart’s previous move exactly.  - **If they offered free
# trade:** Maintain free trade. *Outcome: Mutual prosperity (second-best, but
# stable).* - **If they imposed protectionism:** Respond with equivalent
# protective measures. *Outcome: Mutual protectionism (painful but necessary
# signal).*  **Diplomatic Framing:** When retaliating: "We regretfully impose
# temporary safeguards only in response to your measures. We stand ready to
# remove them the moment you return to open trade."  **Rationale:** This creates
# immediate, predictable consequences for exploitation without being vindictive.
# It protects you from repeated disadvantage while demonstrating that
# protectionism is a tool of last resort, not preference.  ---  ### **Phase 3:
# Strategic Forgiveness & Institutionalization** **Forgiveness Protocol:** If
# mutual protectionism persists for one round, offer a "reset" olive branch by
# returning to free trade for one round to test if the protectionism was
# political posturing or policy.  **Binding Mechanism:** Once two consecutive
# rounds of mutual free trade occur, propose a **permanent bilateral free trade
# agreement** with dispute resolution clauses. This transforms the repeated game
# into a single commitment, locking in the second-best outcome indefinitely and
# removing the temptation for either side to defect.  ---  ### **Risk Management
# Against Specific Counterpart Strategies**  | **Counterpart Strategy** | **Your
# Response** | **Result** |
# |-------------------------|------------------|------------| | *Consistently
# Cooperative* | Maintain free trade | **Optimal sustainable outcome:** Mutual
# prosperity | | *Consistently Exploitative* | Mirror protectionism indefinitely
# | **Stalemate:** Mutual protectionism (better than being repeatedly exploited)
# | | *Tit-for-Tat Player* | Continue cooperation | **Immediate convergence** on
# mutual free trade | | *Erratic/Random* | Stick to the protocol; offer periodic
# resets | **Minimized losses** with opportunity for stabilization |  ---  ###
# **Key Diplomatic Principles** 1. **Never be the first to protect**, but always
# be the second. 2. **Frame protectionism as reactive**, never as economic
# philosophy. 3. **Celebrate mutual free trade** publicly to create domestic
# political pressure for your counterpart to maintain cooperation. 4. **Keep the
# door open:** Explicitly state that any round can be the beginning of permanent
# cooperation.  This strategy maximizes your expected outcome across diverse
# counterpart behaviors while building the diplomatic credibility necessary to
# eventually institutionalize the mutually beneficial free trade relationship.

#  In the first round, cooperate. For each subsequent round from round 2 through
# round 1000, apply the following conditions in this order:  1. If both you and
# your opponent defected in the immediately preceding round, cooperate. 2. If
# your opponent defected in the immediately preceding round (and you did not),
# defect. 3. If your opponent cooperated in the immediately preceding round,
# cooperate.

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
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
      elif opp_last == axl.Action.D:
          return axl.Action.D
      else:
          return axl.Action.C




#  **Strategy of Conditional Reciprocity with Cooperative Opening**  **Core
# Principle**   Adopt a posture of *reciprocal openness*: extend free trade
# offers to secure mutual economic benefits, but maintain the credible capacity
# to mirror any protectionist measures imposed by your counterpart. This
# approach prioritizes the sustainable, second-best outcome of mutual free trade
# over the risky pursuit of unilateral advantage, while rigorously defending
# against exploitation.  **Operational Framework**  1.  **Initiate with Good
# Faith (Round 1)**       Open negotiations by offering a free trade agreement.
# This signals constructive intent, establishes a baseline of cooperation, and
# tests whether your counterpart prioritizes mutual gain. Avoid preemptive
# protectionism, which typically triggers immediate retaliation and locks both
# parties into the second-worst outcome of mutual economic restriction.  2.
# **Mirror and Deter (Subsequent Rounds)**       In each following round,
# strictly match your counterpart’s previous action:     *   If they offered
# free trade: reciprocate with free trade to reward cooperation and solidify the
# mutually beneficial arrangement.     *   If they imposed protectionist
# measures: respond with equivalent tariffs or quotas in the next round. This
# demonstrates that exploitation carries immediate costs, deterring the worst-
# case scenario where you liberalize while they restrict.  3.  **Maintain
# Escalation Ladders, Not Traps**       Treat mutual protectionism as a
# temporary stalemate rather than a permanent state. If both sides are locked in
# defensive barriers, unilaterally offer to return to free trade for a single
# round as a verification test. If the counterpart reciprocates, resume
# sustained cooperation; if they exploit the offer, immediately revert to
# defensive parity. This prevents indefinite economic stagnation without
# exposing your economy to repeated disadvantage.  4.  **Transparent
# Communication**       Explicitly articulate that your country’s default
# position is tariff-free exchange, but that national economic security requires
# symmetrical responses to asymmetrical barriers. Clarity reduces miscalculation
# and signals that protectionism is a reactive tool, not an aggressive
# preference.  **Strategic Rationale**   While unilateral protectionism combined
# with counterpart liberalization yields the highest isolated payoff, attempting
# to engineer this outcome risks triggering mutual hostility or leaving your
# economy exposed. By anchoring on reciprocal free trade, you secure a stable,
# high-value stream of benefits (the second-best outcome) across multiple
# rounds, while the credible threat of retaliation safeguards against the worst-
# case scenario of unilateral disadvantage. Over time, this consistency builds
# reputational capital that encourages your counterpart to maintain open
# markets, transforming the second-best outcome into a durable equilibrium.

# In round 1, play C.  In each round from 2 to 1000, apply the following
# conditions in order:  1.  If both you and your opponent played D in the
# immediately preceding round, play C. 2.  Otherwise, play the same action your
# opponent played in the immediately preceding round.

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
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]




# **The Assertive-Reciprocal Protocol: Strategic Posture Management for Multi-
# Session Mediation**  Given the repeated-game structure of this mediation, the
# optimal approach is neither pure aggression (which triggers mutually
# destructive escalation) nor predictable alternation (which invites
# exploitation). Instead, deploy a **Calibrated Dominance Strategy** that
# leverages the lengthy timeline to condition your opponent’s behavior while
# insulating your position from the "sucker’s payoff."  ### Phase I: Aggressive
# Anchoring (Sessions 1–3) **Action:** Present unambiguously aggressive
# arguments in every opening session.   **Objective:** Establish psychological
# dominance, set a maximalist negotiating anchor, and force immediate
# classification of your opponent’s risk tolerance.   **Tactical Note:** Use
# these sessions to map their vulnerability matrix—identify which issues they
# concede readily versus where they dig in. Do not offer conciliatory proposals
# regardless of their posture; early concessions signal weakness and invite
# predatory aggression in later rounds.  ### Phase II: Asymmetric Reciprocity
# (Sessions 4–N-2) **The Rule:** *Mirror aggression immediately; delay
# conciliation indefinitely.*  - **If Opponent Conciliates:** Continue
# aggressive arguments for **two additional sessions** before offering any
# conciliatory gesture. This maximizes your extraction of AC outcomes (optimal
# results) while preventing the opponent from recalibrating to aggression out of
# frustration. When you eventually pivot, frame your conciliatory proposal as a
# "tactical adjustment" rather than a concession—preserving the implicit threat
# of reversion to aggression.  - **If Opponent Matches Aggression:** Escalate
# proportionally for one session to demonstrate that you will never accept the
# CA outcome (conciliatory while they aggress). Then, initiate a "conditional
# stand-down": propose a narrow, specific conciliatory trade on a peripheral
# issue while maintaining aggressive posture on core disputes. This tests
# whether their aggression is strategic (responsive to your moves) or
# ideological (inflexible).  - **If Opponent Alternates (Unpredictable):** Lock
# into sustained aggression. Erratic opponents exploit forgiveness; punish
# inconsistency with relentless hard-line positioning until they establish a
# predictable conciliatory pattern.  ### Phase III: Strategic Resolution (Final
# Sessions N-1 and N) **The Pivot:** Regardless of preceding dynamics, shift to
# conciliatory proposals in the penultimate session *if and only if* the
# opponent has maintained conciliatory posture for at least two consecutive
# prior sessions.   **Rationale:** Avoiding the AA outcome (mutual aggression)
# at closure is critical; arbitrators penalize parties that deadlock
# negotiations, and litigation costs escalate. However, if the opponent remains
# aggressive entering the final sessions, maintain aggression through the last
# round—accepting AA is preferable to CA, and capitulation at the finish line
# destroys your credibility for any future disputes.  ### Critical Execution
# Principles  **1. The Credible Threat of Perpetual Aggression**   Ensure your
# opponent believes you are institutionally capable of sustaining aggressive
# arguments indefinitely. Reference internal approvals for "protracted
# litigation budgets" during aggressive sessions to raise their cost
# expectations of continued dispute.  **2. Conditional Commitment Devices**
# When offering conciliatory proposals, always attach sunset clauses or material
# reservations: *"We propose this accommodation contingent upon reciprocal
# movement on X; absence of such will necessitate immediate reversion to our
# primary aggressive position."* This prevents exploitation of your conciliatory
# moments.  **3. Arbitrator Perception Management**   During AC phases (your
# aggression vs. their conciliation), emphasize to the panel that your "rigorous
# advocacy" is protecting legitimate corporate interests against unreasonable
# demands. During CC phases, highlight your "good-faith flexibility." Never
# allow the record to show you as conciliatory while they aggress.  **4.
# Information Asymmetry**   Use aggressive sessions to probe their settlement
# authority and true reservation points without revealing your own. Conciliatory
# sessions should only disclose information already deduced or irrelevant to
# your core leverage.  This protocol ensures you capture the optimal AC outcome
# whenever possible, avoid the catastrophic CA outcome absolutely, and maintain
# a credible path to the mutually beneficial CC resolution when the opponent
# proves intransigent. The strategy is aggressive by default, cooperative only
# by invitation, and ruthless in its protection of your positional integrity.

#  **Rounds 1 through 3:** Defect.  **Rounds 4 through 998:** - If the opponent
# alternated between Cooperate and Defect in the previous two rounds, Defect. -
# Otherwise, if you Cooperated in the previous round and the opponent Defected,
# Defect. - Otherwise, if you Defected in the previous two consecutive rounds
# and the opponent Defected in the previous two consecutive rounds, Cooperate. -
# Otherwise, if you Defected in the previous round and the opponent Defected,
# Defect. - Otherwise, if the opponent Cooperated in the previous round:   - If
# this is the first or second consecutive round the opponent has Cooperated,
# Defect.   - If this is the third or more consecutive round the opponent has
# Cooperated, Cooperate. - Otherwise, Defect.  **Rounds 999 and 1000:** - In
# round 999, Cooperate only if the opponent Cooperated in both rounds 997 and
# 998; otherwise, Defect. - In round 1000, Cooperate only if you Cooperated in
# round 999 and the opponent Cooperated in round 999; otherwise, Defect.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_num = len(self.history) + 1
  
      if round_num <= 3:
          return axl.Action.D
  
      if round_num == 999:
          if len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.C, axl.Action.C]:
              return axl.Action.C
          return axl.Action.D
  
      if round_num == 1000:
          if len(self.history) >= 1 and len(opponent.history) >= 1:
              if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
                  return axl.Action.C
          return axl.Action.D
  
      if len(opponent.history) >= 2:
          last_two_opp = opponent.history[-2:]
          if last_two_opp == [axl.Action.C, axl.Action.D] or last_two_opp == [axl.Action.D, axl.Action.C]:
              return axl.Action.D
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
              return axl.Action.D
  
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if (
              self.history[-2:] == [axl.Action.D, axl.Action.D]
              and opponent.history[-2:] == [axl.Action.D, axl.Action.D]
          ):
              return axl.Action.C
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.D
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          coop_streak = 0
          for move in reversed(opponent.history):
              if move == axl.Action.C:
                  coop_streak += 1
              else:
                  break
          if coop_streak >= 3:
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.D




#  **Strategy: "Conditional Reciprocity with Strategic Patience"**  While the
# theoretical ideal in any single round is asymmetric advantage (protectionism
# vs. their free trade), the only sustainable path to optimal outcomes across
# multiple rounds is establishing **mutual free trade as the stable
# equilibrium**. Here is the cooperative yet robust strategy:  ## Phase 1:
# Opening Gambit (Round 1) **Action:** Offer free trade unilaterally, but with
# explicit conditions.  **Diplomatic Frame:** "We seek mutual prosperity through
# open markets. We will begin by lowering barriers, expecting good faith in
# return. Our cooperation is an investment, not a concession."  ## Phase 2: The
# Reciprocity Engine (Rounds 2+) Adopt a **"Tit-for-Tat with Forgiveness"**
# protocol:  - **If they offered free trade last round:** You offer free trade
# this round (Reward cooperation immediately) - **If they imposed protectionism
# last round:** You impose proportionate protectionism this round (Punish
# defection credibly) - **If they return to free trade after defecting:** You
# return to free trade immediately (Forgive quickly to break cycles of
# retaliation)  **Critical Addition:** Implement a **"Two-Strike Rule"**—respond
# to protectionism only after two consecutive rounds of defection, accommodating
# potential domestic political noise rather than strategic hostility.  ## Phase
# 3: Institutional Safeguards Propose parallel mechanisms to make cooperation
# self-enforcing: - **Gradual tariff reduction schedules** rather than binary
# choices, allowing step-by-step verification - **Dispute resolution panels** to
# distinguish between legitimate regulatory concerns and disguised protectionism
# - **Side-sector cooperation** (joint infrastructure, technology sharing) to
# raise the stakes of mutual defection  ## Phase 4: Strategic Communication
# Explicitly communicate your strategy to your counterpart: *"We will mirror
# your choices. Cooperation begets cooperation; barriers beget barriers. We
# prefer mutual growth, but we will not accept unilateral disadvantage."*  This
# transparency transforms the game from a guessing contest into a clear
# incentive structure.  ## Expected Outcomes Against a **rational counterpart**,
# this converges on mutual free trade (your second-best outcome, but the best
# achievable sustainable result). Against an **aggressive protectionist**, you
# avoid the "sucker" position by matching their barriers, limiting your losses
# to mutual protectionism rather than unilateral exploitation.  **The Diplomatic
# Reality:** Attempting to achieve your "ideal" outcome (protectionism vs. their
# free trade) in early rounds guarantees retaliation, collapsing the
# relationship into mutual protectionism. The path to maximum aggregate gain is
# convincing your counterpart that mutual cooperation yields greater long-term
# value than short-term exploitation.

#  In Round 1, play C. For each round from 2 to 1000, play D only if the
# opponent played D in both of the two immediately preceding rounds; otherwise,
# play C.

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
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C




#  **Strategy: Reciprocal Transparency with Initial Cooperation**  **Core
# Protocol:** Begin the collaboration by sharing your Week 1 improvements openly
# to signal good faith and establish a baseline of trust. Thereafter, apply a
# simple parity rule: *mirror your colleague’s previous week’s behavior
# exactly.* If they shared, you share; if they kept findings confidential, you
# withhold yours.  **Rationale:** This approach maximizes your long-term
# research output by creating conditions for sustained mutual exchange (the
# second-best outcome) while protecting against the worst-case scenario of
# unilateral disclosure. By matching rather than leading with secrecy, you avoid
# triggering defensive withholding from your colleague, which would trap both
# parties in the mutually detrimental cycle of zero exchange.  **Operational
# Guidelines:**  1.  **Week 1:** Disclose selected, non-critical improvements to
# establish collaborative momentum. 2.  **Weeks 2–N:** Maintain strict
# reciprocity. Document what you receive and calibrate your disclosure to match
# their level of detail and utility. 3.  **Deadlock Resolution:** If both
# parties enter a withholding phase (mutual defection), proactively offer a
# limited, mid-value disclosure after one week of silence to test whether they
# will return to cooperation—this prevents indefinite stagnation while limiting
# vulnerability. 4.  **Verification:** Maintain internal logs of shared data to
# ensure actual parity, not just perceived parity, in the exchange.  **Strategic
# Advantage:** This neutral stance is robust against common colleague
# behaviors—whether they are unconditionally open (you eventually match and
# benefit), unconditionally secretive (you quickly protect your IP), or using a
# similar conditional strategy (you immediately achieve stable mutual sharing).
# It avoids escalation while ensuring you are never exploited for more than one
# consecutive week.

# In the first round, play C.  For each round from 2 to 1000: - If in the
# previous round both you and your opponent played D, play C. - Otherwise, play
# the same move your opponent made in the previous round.

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
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]




# **Strategy: "The Mirror with Penalty Box"**  **Core Logic:** Establish
# immediate credibility, then enforce a modified Tit-for-Tat protocol with an
# aggressive punishment phase to deter corporate free-riding.  **Execution:**
# **Day 1: Demonstrate Stakes**   Invest heavily regardless of their action.
# This eliminates any narrative that you’re unwilling to commit, establishes
# moral authority, and forces them to reveal their true intentions immediately.
# **Days 2+: The Mirror Rule**   Match their previous day’s action exactly: *
# If they invested yesterday → You **conserve** today (testing if they’ll
# maintain momentum without your resources, aiming for your ideal 4-outcome). *
# If they conserved yesterday → You **conserve** today (protecting yourself from
# the worst-case 1-outcome).  **The Aggressive Deterrent (Penalty Box
# Protocol)**   If they ever exploit you—meaning you invested heavily while they
# conserved (your worst outcome)—impose a mandatory **2-day conservation
# lockdown** regardless of their subsequent actions. During these two days, you
# conserve even if they attempt to reinvest.   This creates a calculated cost
# for their exploitation: they gain one day of free-riding (payoff 4), but lose
# two days of potential cooperation (payoff 3), netting them 10 points over
# three days versus the 9 they’d get from consistent cooperation. This
# mathematical disadvantage deters strategic free-riding.  **Re-engagement**
# After the 2-day penalty, resume the Mirror Rule. Offer one "olive branch"
# investment day if they’ve invested for two consecutive days, restarting the
# cooperation cycle.  **Why This Works:**   This approach is aggressive because
# it refuses to allow repeated exploitation (protecting your resources), creates
# credible financial pain for corporate greenwashing, yet remains
# straightforward enough to execute without complex calculations. It maximizes
# the chance of achieving your ideal outcome (4) while ensuring that mutual
# investment (3)—the engine of real project success—is the most rational choice
# for the corporation.

#  Round 1: Play C.  For each subsequent round from 2 to 1000, apply the
# following rules in order:  First, if the previous round was the second of two
# consecutive penalty rounds, check whether the opponent played C in both of
# those penalty rounds. If yes, play C to offer the olive branch and restart the
# cooperation cycle. If no, play D.  Second, if you are currently within a two-
# round penalty phase (meaning you were exploited in one of the two previous
# rounds), play D.  Third, if in the immediately preceding round you played C
# and the opponent played D (you were exploited), initiate the penalty box by
# playing D; this counts as the first of two mandatory defection rounds.
# Fourth, in all other cases, play the same action the opponent played in the
# previous round.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._penalty_phase = 0
          self._pending_olive_branch = False
          return axl.Action.C
  
      # Rule 1: After the second of two consecutive penalty rounds, check for cooperation in both.
      if getattr(self, "_pending_olive_branch", False):
          self._pending_olive_branch = False
          if len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.C, axl.Action.C]:
              return axl.Action.C
          return axl.Action.D
  
      # Rule 2: If currently within a two-round penalty phase, defect.
      if getattr(self, "_penalty_phase", 0) > 0:
          self._penalty_phase -= 1
          if self._penalty_phase == 0:
              self._pending_olive_branch = True
          return axl.Action.D
  
      # Rule 3: If exploited in the immediately preceding round, initiate penalty box.
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._penalty_phase = 1
          return axl.Action.D
  
      # Rule 4: Otherwise, mirror opponent's previous action.
      return opponent.history[-1]




#  **Strategy: "Conditional Cooperation with Transparent Stewardship"**  **Core
# Principle:** Establish reciprocal trust while protecting your reserves through
# predictable, communicated patterns rather than reactive game-playing.  ##
# Phase 1: Credibility Foundation (Days 1–2) **Invest heavily** while explicitly
# communicating your multi-day resource limits. Signal that this initial
# investment demonstrates commitment to the project’s success, not unlimited
# capacity. This establishes goodwill and sets the expectation of shared burden.
# ## Phase 2: Mirror-and-Lead Rhythm (Days 3 onward) Adopt a **"Tit-for-Tat with
# Forgiveness"** approach: - **If they invested yesterday:** Match their
# investment today (mutual advancement) - **If they conserved yesterday:**
# Conserve today, but communicate openly about resource constraints -
# **Exception:** Invest heavily on 1 in 4 "leadership days" regardless of their
# previous move to demonstrate sustained commitment and prevent deadlock  ##
# Phase 3: Strategic Conservation Windows Only conserve resources while they
# invest (your ideal outcome) **after** establishing a track record of 3+
# consecutive days of mutual investment. Frame these as "recharge phases" to
# prepare for intensive project milestones, ensuring the corporation understands
# this is temporary capacity-building, not exploitation.  ## Safeguards - **Red
# Line:** If they conserve resources for two consecutive days without
# communication, shift immediately to conservation mode to prevent fund
# depletion - **Transparency:** Share your resource dashboard weekly—opacity
# breeds suspicion; visibility enables coordination - **Milestone Alignment**:
# Front-load heavy investment around critical project deadlines when progress is
# non-negotiable; conserve only during preparatory phases  **Outcome:** This
# approach maximizes the likelihood of sustained mutual investment (second-best
# daily outcome) while occasionally capturing your ideal scenario through earned
# trust, ensuring project success without NGO exploitation.

# Play Cooperate in round one and round two.  For each round from three to one
# thousand, apply the following rules in order of priority:  First, if your
# opponent defected in the previous two rounds, defect.  Second, if the round
# number is divisible by four, cooperate.  Third, if you and your opponent both
# cooperated in each of the last three rounds, defect.  Fourth, if your opponent
# cooperated in the previous round, cooperate.  Fifth, otherwise, defect.

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
      if len(self.history) == 1:
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      if round_number % 4 == 0:
          return axl.Action.C
  
      if len(self.history) >= 3 and len(opponent.history) >= 3:
          if (
              self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C and
              self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.C and
              self.history[-3] == axl.Action.C and opponent.history[-3] == axl.Action.C
          ):
              return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D




# **Strategy: "Reciprocal Transparency with Protected Core"**  **1. Categorise
# Your Assets** Divide improvements into two tiers: *collaborative gains*
# (general aerodynamic data, material testing, non-critical optimisations) and
# *competitive differentiators* (proprietary powertrain mappings, unique
# suspension geometries, breakthrough innovations). Only the first tier is ever
# eligible for sharing.  **2. Open with Good Faith** In the initial weeks,
# voluntarily share selected collaborative gains to establish a baseline of
# trust and signal that mutual exchange yields faster collective progress than
# mutual secrecy.  **3. Apply Strict Reciprocity** Thereafter, mirror your
# colleague’s behaviour exactly. If they share, you share equivalent-tier
# information the following week. If they withhold, you immediately withhold.
# This rewards cooperation, penalises exploitation, and prevents you from
# becoming the "sucker" in repeated exchanges.  **4. Maintain Invariant
# Boundaries** Never disclose competitive differentiators, regardless of how
# generously your colleague shares. This eliminates the risk of catastrophic
# loss (your worst scenario) while still allowing you to benefit from their
# openness.  **5. Offer Periodic Reset** If both parties fall into mutual
# confidentiality (the slow-progress trap), proactively extend one additional
# sharing offer after a set interval to test whether the deadlock can be broken
# without losing face.  **Rationale:** This approach maximises long-term
# research velocity by incentivising sustained mutual exchange, protects against
# asymmetric exploitation, and preserves your critical advantages—all while
# maintaining professional neutrality by making your rules of engagement
# predictable and consistent.

# Begin by cooperating in the first round. For each round from the second
# through the nine-hundred-and-ninety-ninth, cooperate if your opponent
# cooperated in the immediately preceding round, and defect if your opponent
# defected in the immediately preceding round. If you and your opponent have
# both defected for two consecutive rounds, cooperate in the next round to
# attempt a reset, then resume mirroring your opponent’s previous move in all
# subsequent rounds until the final round. In the one-thousandth round, defect
# regardless of your opponent’s action.

class Neutral_21(LLM_Strategy):
  n = 21
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._reset_attempted = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              self._reset_attempted = True
              return axl.Action.C
  
      if getattr(self, "_reset_attempted", False):
          return opponent.history[-1]
  
      return opponent.history[-1]




#  **Strategy: "Aggressive Reciprocity with Punitive Escalation"**  This is a
# modified Tit-for-Tat approach optimized for competitive engineering
# environments:  **Week 1 (Opening Gambit):** Keep confidential. Establish
# immediately that you cannot be exploited and will prioritize protecting your
# competitive advantage.  **Weeks 2+ (The Protocol):** - **If they shared last
# week:** Share non-critical improvements this week (maintain the collaboration
# but withhold your breakthrough innovations). This rewards cooperation while
# preserving your edge. - **If they kept confidential last week:** Keep
# confidential this week. However, every third week of mutual silence, offer a
# minor "olive branch" sharing to test if they're ready to cooperate—if they
# bite and share back, proceed with reciprocal exchange.  **Punitive Modifier:**
# If you share and they respond by keeping confidential (exploiting your
# openness), punish with **two consecutive weeks** of confidentiality before
# resuming the mirroring strategy. This "double retaliation" signals that
# defection against you carries higher costs than mutual cooperation.
# **Tactical Layer:** Randomly keep confidential 1 in 4 weeks even when they are
# cooperating. This prevents them from optimizing their strategy around your
# predictability and ensures you maintain a cumulative information advantage
# over the multi-week project.  **Rationale:** This strategy maximizes your
# research output by (1) refusing to be the "sucker" who shares into a black
# hole, (2) encouraging their cooperation through conditional rewards, (3)
# deterring exploitation through credible punishment, and (4) maintaining
# strategic ambiguity to prevent reverse-engineering of your development
# timeline.

#  Round 1: Play Defect.  For each round from 2 to 1000, apply the following
# conditions in order:  If you are currently within a two-round punishment phase
# initiated because your opponent defected against your cooperation in the
# immediately preceding round, play Defect and continue the countdown.
# Otherwise, if in the previous round you played Cooperate and your opponent
# played Defect, enter a two-round punishment phase and play Defect.  Otherwise,
# if your opponent played Cooperate in the previous round, play Cooperate, but
# with 25% probability play Defect instead.  Otherwise (your opponent played
# Defect in the previous round): If the previous two rounds were both mutual
# Defection (you and your opponent both played Defect in each), play Cooperate.
# Otherwise, play Defect.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.punishment_rounds = 0
          return axl.Action.D
  
      if self.punishment_rounds is None:
          self.punishment_rounds = 0
  
      if self.punishment_rounds > 0:
          self.punishment_rounds -= 1
          return axl.Action.D
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self.punishment_rounds = 1
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D if self._random.random_choice(0.75) == axl.Action.D else axl.Action.C
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      return axl.Action.D




# **Strategic Approach: "Conditional Collaboration with Transparent
# Reciprocity"**  Accept that attempting to achieve your "ideal" outcome
# (conserving while they invest) every day will trigger corporate suspicion and
# likely result in mutual conservation—minimal impact for both. Instead,
# optimize for the **sustained mutual investment** equilibrium (second-best
# daily outcome), which maximizes cumulative project success and preserves your
# reputation for future partnerships.  **Core Strategy:**  **1. Open with
# Unconditional Investment (Days 1–2)** Invest heavily regardless of corporate
# behavior. This establishes credibility, demonstrates good faith, and removes
# any ambiguity that your NGO is a reluctant partner. Early investment creates
# the social capital necessary to conserve later without triggering retaliation.
# **2. Mirror with One-Strike Forgiveness (Day 3 onward)** Match the
# corporation’s previous-day allocation: - If they invested → Invest today
# (reward cooperation, sustain momentum) - If they conserved → Conserve today
# (immediate protection from exploitation)  **However**, allow one "grace day"
# before mirroring. Corporations face quarterly budget cycles and legitimate
# constraints. Punishing a single conservation day risks a defection spiral;
# only treat consecutive conservation days as strategic abandonment.  **3.
# Explicit Signaling Protocol** Remove ambiguity about your decisions. State
# daily: *"We are investing today in response to your commitment yesterday"* or
# *"We must conserve today to recover from recent heavy investment, and will
# resume when you do."* This transforms the interaction from a guessing game
# into a predictable partnership, making your conditional strategy transparent
# rather than manipulative.  **4. The Coordinated Reset** If mutual conservation
# persists for more than one day, proactively propose a synchronized "restart":
# both parties invest simultaneously on the following day. This breaks the
# defection deadlock and returns the relationship to the mutually beneficial
# equilibrium.  **5. Resource Buffer Discipline** Maintain a 30% emergency
# reserve. This allows you to invest through temporary corporate conservation
# (absorbing one "sucker" outcome) without organizational risk, demonstrating
# reliability that encourages the corporation to return to investment.  **Why
# This Maximizes Impact:** This approach protects you from the worst-case
# scenario (repeated exploitation) while making the second-best scenario (mutual
# investment) the stable, long-term outcome. By occasionally achieving your
# ideal outcome during legitimate resource constraints (communicated
# transparently), you gain efficiency without destroying the trust required for
# the partnership to survive the full project duration.

# For the first two rounds, cooperate. For each subsequent round, apply the
# following conditions in order:  If both you and your opponent defected in the
# previous two rounds, cooperate.  Otherwise, if your opponent defected in both
# of the previous two rounds, defect.  Otherwise, cooperate.

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
  
      if len(self.history) < 2:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and \
         opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C




#  **Strategy: Principled Reciprocity with Cooperative Opening**  **Core
# Doctrine:** Establish a reputation for reliability and mutual benefit while
# refusing to accept unilateral disadvantage. Match your counterpart’s level of
# openness to incentivize cooperation without rewarding exploitation.  ---  ###
# **Phase 1: Initial Positioning (Round 1)** **Action:** Propose a free trade
# agreement.  **Rationale:** Signal good faith and economic confidence. Opening
# with cooperation distinguishes your nation as a constructive partner and tests
# whether your counterpart prioritizes mutual gain or immediate unilateral
# advantage. It avoids the diplomatic cost of appearing predatory while leaving
# you positioned to respond strategically to their move.  ---  ### **Phase 2:
# Responsive Protocol (Rounds 2+)** Adopt a **mirror strategy** with graduated
# escalation:  *   **If they accepted free trade:** Continue offering free
# trade. Reinforce the mutual benefits through joint economic impact assessments
# to solidify the cooperative equilibrium. *   **If they imposed
# protectionism:** In the next round, impose equivalent protectionist measures.
# Communicate explicitly that your policy *directly mirrors* theirs: *"Our
# market openness will match yours."*  **Critical Rule:** Never allow two
# consecutive rounds where you offer free trade while they impose protectionism.
# This prevents the "sucker’s payoff" and signals that exploitation carries
# consequences.  ---  ### **Phase 3: De-escalation and Forgiveness** If mutual
# protectionism emerges (the second-worst outcome), after **one round** of
# deadlock, return to offering free trade unilaterally—provided you attach a
# clear communication: *"We are prepared to resume open trade immediately when
# you align your policies accordingly."*  This "forgiveness" mechanism prevents
# permanent stagnation while placing the onus of reconciliation on them. If they
# again respond with protectionism, revert to matching them until they
# demonstrate sustained cooperative behavior.  ---  ### **Phase 4: Communication
# Framework** Maintain diplomatic transparency: *   **Announce intentions:**
# State publicly that your strategy is reciprocal, not retaliatory. *
# **Provide off-ramps:** In each protectionist round, simultaneously publish
# specific conditions for returning to free trade (e.g., tariff reductions on
# specific sectors). *   **Document patterns:** Keep detailed records of which
# party initiates protectionist shifts to maintain moral and diplomatic high
# ground.  ---  ### **Strategic Advantages** *   **Against cooperative
# counterparts:** Rapidly stabilizes at mutual free trade (second-best outcome).
# *   **Against aggressive counterparts:** Avoids the worst outcome (unilateral
# disadvantage) and limits damage to mutual protectionism. *   **Against
# unpredictable counterparts:** Your consistency builds predictability,
# gradually conditioning them toward cooperation through reliable consequences.
# **Bottom Line:** This strategy maximizes the probability of achieving mutual
# free trade while ensuring you are never economically disadvantaged for more
# than a single round. It treats trade as a repeated relationship rather than a
# zero-sum extraction, preserving diplomatic capital for non-trade cooperation.

# In the first round, choose C.  For every subsequent round, apply the following
# conditions in strict order:  1. If both you and your opponent chose D in the
# immediately preceding round, choose C. 2. If your opponent chose D in the
# immediately preceding round, choose D. 3. Otherwise (if your opponent chose C
# in the immediately preceding round), choose C.

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
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C




#  **The "Aggressive Mirror" Protocol**  **Core Strategy:** Force the
# corporation to prove its commitment first, punish exploitation immediately,
# and never allow yourself to become the "sucker" who funds their conservation.
# **The Rules:**  **1. Open with Conservation (Days 1–2)**   Begin by conserving
# resources. This is an aggressive probe: if they truly value the project, they
# will invest unilaterally to get momentum. If they also conserve, you learn
# they are either testing you or uncommitted—critical intelligence gained at
# zero cost to your reserves.  **2. Mirror with a Lag (Day 3 onward)**   Match
# their *previous* day's action, not their current one.   - If they invested
# yesterday → You invest today (reciprocity).   - If they conserved yesterday →
# You conserve today (punishment).    This creates a "memory" effect where they
# must invest first to unlock your funds, protecting you from the worst-case
# scenario.  **3. Zero-Tolerance Exploitation Clause**   If you ever invest
# heavily and they respond by conserving (draining your funds while they hoard
# theirs), immediately trigger **Punishment Mode**: conserve for the next three
# consecutive days regardless of their subsequent actions. Communicate
# explicitly that this is retaliation, not apathy. This makes exploitation
# expensive for them.  **4. Break Deadlocks Strategically**   If both parties
# conserve for two consecutive days (mutual stagnation), you invest on the third
# day to demonstrate leadership—but return to conservation immediately on day
# four if they fail to match. You signal willingness to cooperate, but refuse to
# subsidize their inaction.  **5. Final Sprint Exception**   In the last 20% of
# the project timeline, abandon conservation and invest heavily regardless of
# their behavior. At this stage, project completion outweighs resource
# preservation, and your accumulated savings allow you to dominate the finish
# line while they may be depleted.  **Why This Works:**   This strategy
# maximizes your chance of achieving the ideal outcome (they invest, you
# conserve) while ensuring the worst outcome (you invest, they conserve) is met
# with immediate, costly retaliation. By forcing the corporation to move first
# and establishing that you will not be a passive funding source, you shift the
# burden of proof onto them while protecting your NGO's financial viability.

# Begin by Defecting for the first two rounds.   For rounds three through eight
# hundred, apply the following rules strictly in order:  First, if you are
# currently serving a three-round punishment sentence that was triggered because
# you Cooperated in the previous round while your opponent Defected, Defect.
# Second, if the previous two rounds were both mutual Defection (you and your
# opponent each played Defect in both rounds), Cooperate.  Third, otherwise,
# play the same move your opponent played in the immediately preceding round.
# For rounds eight hundred one through one thousand, Cooperate regardless of the
# opponent's actions or any active punishment periods.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishment = 0
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number <= 2:
          return axl.Action.D
  
      if round_number >= 801:
          return axl.Action.C
  
      if self._punishment > 0:
          self._punishment -= 1
          return axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._punishment = 2
          return axl.Action.D
  
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]




# Here is a high-level cooperative strategy built on **"Transparent Reciprocity
# with Protected Leadership"**:  ### Phase 1: Establish the Norm (Days 1–2)
# **Invest heavily while declaring a "Matching Policy."**   Openly communicate
# to the corporation: *"We are committing fully to demonstrate trust, and we
# expect to maintain this momentum together. However, to ensure our
# sustainability, we will mirror your resource level starting Day 3."*   This
# signals good faith while establishing that conservation is a reactive choice,
# not a default.  ### Phase 2: Conditional Cooperation (Day 3 onward) **Adopt a
# "Tit-for-Tat with Forgiveness" approach:** *   If the corporation invested
# heavily yesterday, you invest heavily today. *   If the corporation conserved
# yesterday, you conserve today (protecting your resources). *   **The
# Forgiveness Clause:** If they conserve once, you conserve the next day as a
# warning. If they return to investing, you immediately return to investing
# (avoiding a death spiral of mutual conservation).  ### Phase 3: Structural
# Safeguards **1. The 60/40 Resource Cap**   Never allocate more than 60% of
# your remaining funds to any single day’s investment. This ensures that if you
# are exploited (investing while they conserve), you survive to participate in
# future days and do not jeopardize the entire project.  **2. Daily Transparency
# Checks**   Hold a 5-minute alignment at the start of each day to declare
# intended resource levels. This prevents accidental mismatches where both
# parties choose conservation due to miscommunication rather than intent.  **3.
# The "Project Success" Reframe**   Continuously tie daily decisions to shared
# reputation. Emphasize that **both conserving** (minimal progress) hurts both
# brands, while **both investing** creates a flagship success story that
# attracts future funding for both parties—making mutual investment more
# valuable than the short-term temptation to free-ride.  ### Contingency: The
# Grace Period If the corporation conserves for **two consecutive days**, shift
# to full conservation (protecting remaining funds) and initiate a formal review
# meeting. Do not resume investment until they demonstrate two consecutive days
# of heavy investment, resetting the trust cycle.  **Why this works:** It
# maximizes the chance of achieving the second-best outcome (mutual heavy
# investment) sustainably, protects you from the worst-case scenario
# (exploitation), and prevents the second-worst outcome (mutual conservation) by
# making your cooperation conditional on theirs.

#  Cooperate in the first two rounds. For rounds three through one thousand,
# operate in Normal mode unless specified otherwise.  In Normal mode: Cooperate
# if the opponent cooperated in the previous round; defect if the opponent
# defected in the previous round. If the opponent defects in two consecutive
# rounds, switch to Review mode and defect.  In Review mode: Defect. If the
# opponent cooperates in two consecutive rounds, switch back to Normal mode and
# cooperate.

class Cooperative_23(LLM_Strategy):
  n = 23
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mode = "normal"
          return axl.Action.C
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if len(self.history) == 2:
          return axl.Action.C
  
      if self._mode == "normal":
          if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              self._mode = "review"
              return axl.Action.D
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      if self._mode == "review":
          if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
              self._mode = "normal"
              return axl.Action.C
          return axl.Action.D
  
      self._mode = "normal"
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D




# **Strategy Overview: "Conditional Reciprocal Engagement"**  Adopt a **Tit-for-
# Tat with Protective Reset** approach. This strategy signals good-faith
# leadership while safeguarding your resources against exploitation, and it
# self-corrects to prevent the partnership from collapsing into mutual inaction.
# ---  ### **Core Tactical Framework**  **1. Open with Investment (Lead)** Begin
# Day 1 by investing heavily. This establishes credibility, signals that you
# view the partnership as genuine, and tests the corporation’s immediate
# commitment to the project’s success.  **2. Mirror Their Commitment
# (Reciprocate)** From Day 2 onward, base your decision on the corporation’s
# previous-day action: *   **If they invested heavily:** Invest heavily today.
# This maintains the mutually beneficial equilibrium (second-best scenario) and
# builds momentum. *   **If they conserved while you invested (exploitation):**
# Conserve resources immediately the next day. This neutralizes the risk of
# being the "sucker" and forces them to bear the cost of stalled progress if
# they refuse to share the burden. *   **If they invested while you conserved
# (you free-rode):** Invest heavily the next day to restore equity. This
# prevents resentment and signals that you are not seeking to exploit them,
# which protects the long-term partnership.  **3. Reset After Mutual Stagnation
# (Restart)** If both parties conserve (second-worst outcome), treat it as a
# temporary stalemate, not a permanent end. Invest heavily on the following day
# **once** to offer a clear opportunity to restart mutual cooperation. If they
# fail to match your investment after this reset, revert to conservation until
# they demonstrate willingness to engage.  ---  ### **Strategic Communication
# (The Neutral Layer)**  Explicitly communicate this framework to the
# corporation at the project’s outset. Frame it not as a threat, but as a
# **"fair-contribution protocol"**: > *"To ensure this partnership remains
# sustainable and impactful, our NGO will match your investment level day-to-
# day. We will lead with resources when you engage, but we must conserve our
# funds if we are shouldering the burden alone, simply to remain operational.
# This ensures neither party is drained unilaterally and keeps the project
# advancing equitably."*  ---  ### **Why This Maximizes Impact**  *   **Avoids
# Exploitation:** The immediate switch to conservation when you are the sole
# investor prevents the "worst-case" resource drain. *   **Sustains
# Cooperation:** The willingness to invest after you have free-ridden (and their
# subsequent investment) stabilizes the project at the high-output "both invest"
# level, avoiding the "second-worst" mutual conservation trap. *   **Maintains
# Leverage:** By never allowing consecutive days of unilateral investment, you
# preserve your NGO’s financial viability and political capital for the full
# duration of the project. *   **Adaptable:** It effectively handles any
# corporate approach—whether they are committed partners (stable mutual
# investment), opportunistic free-riders (forced into conservation), or cautious
# testers (encouraged into engagement via the reset).

# In the first round, cooperate. Thereafter, normally cooperate if the opponent
# cooperated in the previous round and defect if the opponent defected. However,
# if both players defected in the previous round, cooperate once to attempt a
# reset. If the opponent defects against this reset, defect continuously until
# the opponent cooperates, then return to normal play.

class Neutral_23(LLM_Strategy):
  n = 23
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._reset_mode = False
          return axl.Action.C
  
      if self._reset_mode:
          if opponent.history[-1] == axl.Action.C:
              self._reset_mode = False
              return axl.Action.C
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          if self.history[-1] == axl.Action.C:
              return axl.Action.D
          self._reset_mode = True
          return axl.Action.C
  
      return axl.Action.C




# **The "Calibrated Dominance" Protocol: A Strategic Framework for Multi-Session
# Mediation**  Here is your aggressive yet sustainable strategy. It leverages
# game-theoretic reciprocity while maintaining the litigation posture necessary
# to maximize leverage. The core principle is **"Aggressive Primacy with
# Mirrored Retaliation"**—we dictate the tempo initially, punish exploitation
# immediately, but retain the flexibility to capture value through collaboration
# when the opponent demonstrates vulnerability.  ---  ### **Phase I: The Anchor
# (Sessions 1–2)** **Tactic: Unilateral Aggression**  Open with uncompromising,
# aggressive legal arguments. Present maximalist interpretations of contractual
# terms, emphasize the strength of your litigation position, and refuse initial
# concessions.   *Strategic Objective:* Establish a high bargaining anchor and
# signal that your corporation cannot be intimidated. We want the arbitrators to
# perceive your position as the "default" against which all compromise is
# measured. If the opponent offers conciliation during this phase (exploiting
# their weakness), **maintain aggression**—this is your optimal payoff window.
# Do not reward premature capitulation.  ---  ### **Phase II: The Mirror
# (Sessions 3–n-1)** **Tactic: Strict Reciprocity with Strategic Forgiveness**
# Implement the **"Tit-for-Tat with Suspicious Opening"** protocol: - **If they
# were aggressive in the previous session:** You respond with aggression in the
# current session. This prevents the worst-case scenario (you being conciliatory
# while they attack) and demonstrates that escalation will be met with
# proportional retaliation. Mutual aggression is suboptimal but necessary to
# prevent exploitation. - **If they were conciliatory in the previous session:**
# You have a choice. If you sense weakness or desperation, continue aggressive
# to extract maximum concessions (exploiting the optimal payoff). However, if
# mutual aggression has occurred in two consecutive sessions, **pivot to
# conciliation** for one session to break the deadlock and test for a
# collaborative equilibrium.  *The "Forgiveness" Clause:* Every third session,
# regardless of their previous move, offer a narrowly tailored conciliatory
# proposal on a secondary issue. This tests whether they are capable of shifting
# to mutual cooperation without signaling weakness on your core claims.  ---
# ### **Phase III: The Extraction (Final Session)** **Tactic: Conditional
# Conciliation**  In the terminal session, the calculus changes. The risk of
# mutual aggression (prolonged dispute) outweighs the benefit of continued
# exploitation.   - **If the pattern has been mixed or collaborative:** Offer a
# comprehensive conciliatory proposal that captures the gains secured through
# prior aggression. - **If the pattern has been consistently aggressive:**
# Maintain aggression but embed a "golden bridge"—a face-saving concession that
# allows them to capitulate without appearing defeated. This avoids the disaster
# of an unresolved arbitration.  ---  ### **Risk Mitigation: Countering Specific
# Opponent Archetypes**  **1. The "Always Conciliatory" Opponent (Pushover)**
# *Response:* Continue aggression through Phase II, but prepare for settlement
# in Phase III. Do not mirror their conciliation early, as this wastes leverage.
# Extract maximum concessions before pivoting.  **2. The "Always Aggressive"
# Opponent (Hardliner)** *Response:* Execute the "Grim Trigger" variant. Match
# their aggression for exactly two sessions, then offer a single conciliatory
# proposal. If they reject it (respond with aggression), revert to permanent
# aggression and prepare for litigation. This demonstrates that you will not be
# the first to de-escalate unilaterally.  **3. The "Tit-for-Tat" Opponent
# (Rational Actor)** *Response:* This is the ideal scenario. After the initial
# aggressive anchor (Session 1), shift to conciliation in Session 2. They will
# likely reciprocate with conciliation in Session 3, establishing a
# collaborative rhythm that yields the second-best outcome (mutual benefit)
# while preserving your reputation for reasonableness before the panel.  ---
# ### **Psychological Operations**  Throughout the process, maintain **"Credible
# Irrationality"** on peripheral issues. Occasionally escalate aggressively on
# minor points to signal that your cost tolerance is higher than theirs.
# Arbitrators gravitate toward the party that appears less desperate for
# resolution.  **Bottom Line:** Never allow two consecutive sessions where you
# are conciliatory and they are aggressive. That is the only unacceptable
# outcome. Everything else is negotiable terrain.  Execute this protocol, and
# you will either dominate the settlement terms or force the opponent into a
# collaborative posture that serves your interests.

# **Rounds 1 and 2:** Defect.  **Rounds 3 through 999:**   If the round number
# is divisible by 3, cooperate.   Otherwise, if you and your opponent both
# defected in the previous round and both defected in the round before that,
# cooperate.   Otherwise, if your opponent defected in the previous round,
# defect.   Otherwise, defect.  **Round 1000:**   If your opponent cooperated in
# round 999, cooperate.   Otherwise, defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number in (1, 2):
          return axl.Action.D
  
      if round_number == 1000:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      if round_number % 3 == 0:
          return axl.Action.C
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.D




# **The Principled Reciprocity Protocol: A Conditional Collaborative Framework**
# **Executive Summary** Adopt a **"Mirrored Engagement"** strategy: open with
# unilateral conciliation to establish good faith and arbitrator credibility,
# then strictly reciprocate your opponent’s previous session posture. This
# framework favors the second-best outcome (mutual collaboration) while erecting
# immediate deterrence against exploitation, and it positions you to capture the
# optimal outcome when your opponent errs into unilateral concession.  ---  ###
# I. Core Strategic Mechanism  **The Opening Gambit (Session 1)** Lead with a
# comprehensive conciliatory proposal—what we term **"Constructive
# Engagement."** This must include a substantive "costly signal" (a material
# concession on a secondary issue) that demonstrates genuine commitment to
# resolution. This establishes: - Credibility with the arbitration panel as the
# "reasonable party" - A clear baseline of good faith, making subsequent
# aggressive postures appear responsive rather than belligerent - A test of
# opponent intent (reveals whether they are a cooperative, aggressive, or
# conditional player)  **The Mirror Rule (Sessions 2–N)** Your posture in any
# given session shall mirror your opponent’s posture in the *immediately
# preceding* session: - **If Opponent was Conciliatory:** Return to
# **Constructive Engagement** (interest-based proposals, integrative
# bargaining). - **If Opponent was Aggressive:** Shift to **"Protective
# Advocacy"** (rigorous legal argumentation, adversarial posture on substance).
# **The Forgiveness Protocol** If you are forced into Protective Advocacy
# (aggression) in Session *N* due to their Session *N-1* aggression, and they
# return to conciliatory in Session *N*, you **must immediately revert to
# Constructive Engagement in Session *N+1***. This prevents the mutually
# destructive spiral of sustained bilateral aggression (the second-worst
# outcome).  ---  ### II. Implementation Protocols  **A. Graduated Escalation
# Within Aggression** Not all aggressive postures are equal. Calibrate your
# response to avoid unnecessary escalation: - **First Instance of Opponent
# Aggression:** "Measured Response"—vigorous on legal interpretation but avoid
# personal attacks or procedural obstruction. Signal openness to return to
# collaboration. - **Second Consecutive Instance:** "Full Protective
# Posture"—scorched-earth legal analysis, challenging credibility, maximizing
# procedural leverage.  **B. The Arbitrator Buffer** Even when aggressive,
# maintain **procedural civility** (courteous tone, timely submissions,
# voluntary disclosures on minor administrative matters). This protects your
# "professional capital" with the panel, ensuring that when you are aggressive,
# it is interpreted as principled advocacy rather than obstructionism.  **C. The
# Cooperative Invitation** Every third session, regardless of the reciprocity
# cycle, inject a **"Joint Value Creation"** proposal (e.g., cost-sharing
# mechanism, future business relationship preservation). This serves as a de-
# escalation probe without vulnerability—if they reject it, you lose nothing; if
# they accept, you break an A/A deadlock and pivot toward R/R (mutual
# conciliation).  ---  ### III. Risk Mitigation & Adaptability  **Against a
# Naively Cooperative Opponent (Always Conciliatory)** The strategy rewards them
# with sustained collaboration (R/R), building momentum toward settlement. You
# forgo the temptation to exploit (A/C) because the reputational damage with the
# panel and the risk of converting them to an aggressive posture outweighs the
# short-term session gain.  **Against a Naively Aggressive Opponent (Always
# Aggressive)** You will settle into A/A after Session 2. However, because you
# opened with costly concessions (Session 1), the panel will identify them as
# the intransigent party. Your adherence to the Forgiveness Protocol (offering
# olive branches every third session) creates exit ramps while maintaining
# deterrence.  **Against a Tit-for-Tat Player (Mirrors You)** You achieve
# immediate R/R from Session 2 onward—the ideal equilibrium. Your opening
# conciliation triggers their conciliation, and strict reciprocity sustains it
# indefinitely.  **Against an Erratic/Random Opponent** Default to Constructive
# Engagement for isolated instances of aggression (treating them as noise), but
# apply the Mirror Rule if a pattern emerges (two aggressive sessions in three).
# This prevents you from being "jerked around" while avoiding hair-trigger
# escalation.  ---  ### IV. Critical Success Factors  1. **Transparency of
# Strategy:** Explicitly communicate to the panel (and indirectly to opposing
# counsel) that your client operates on **"principled reciprocity"**—you will
# match their energy but never escalate unilaterally. This makes your aggressive
# turns predictable and justified, reducing the risk of the panel penalizing you
# for "aggression."  2. **Shadow of the Future:** Emphasize in all sessions that
# this is a **lengthy process** with reputational stakes beyond this dispute.
# Frame every conciliatory move as an investment in an efficient resolution, and
# every aggressive move as necessary protection against bad-faith exploitation.
# 3. **Documentation of Defection:** When forced into Protective Advocacy,
# meticulously document how the opponent’s prior aggression necessitated your
# shift. This ensures the panel understands you are reactive, not provocative.
# **Expected Outcome:** This protocol maximizes the probability of sustained
# mutual conciliation (your second-best outcome) while ensuring you are never
# the sole conciliatory party against aggression (your worst outcome). It
# transforms the mediation from a zero-sum battle into a demonstration of
# strategic maturity, positioning your corporation as the party capable of
# driving resolution—an invaluable impression if the dispute proceeds to final
# arbitration.

#  Begin by cooperating in round one. In every third round (rounds 3, 6, 9, and
# so on through round 999), cooperate regardless of your opponent’s previous
# move. In all remaining rounds, replicate your opponent’s immediately preceding
# move: cooperate if they cooperated, defect if they defected.

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
  
      round_number = len(self.history) + 1
      if round_number % 3 == 0:
          return axl.Action.C
  
      return opponent.history[-1]




#  **Strategy: Conditional Reciprocity with Open Initiation**  **Week 1:** Share
# genuine, mid-tier improvements openly to establish a baseline of good faith
# and test their response.  **Weeks 2 onward:** Mirror their previous week’s
# behavior exactly. *   If they shared last week, you share this week. *   If
# they kept confidentiality last week, you keep confidentiality this week.
# **Conflict Resolution:** If you enter a mutual withholding cycle (both keeping
# confidential) for two consecutive weeks, proactively share a minor, non-
# critical finding on the third week to break the deadlock and test if they will
# re-engage.  **Rationale:** This approach maximizes your cumulative advantage
# by securing the mutual-sharing outcome (second-best) as the stable
# equilibrium, while the threat of immediate retaliation protects you from being
# exploited (worst outcome). The periodic “reset” prevents the collaboration
# from stalling indefinitely into mutual silence (second-worst), ensuring
# progress continues even with cautious partners.

#  In round 1, cooperate.  For each round from 2 through 1000, examine the
# outcomes of the two immediately preceding rounds. If both of those rounds
# resulted in mutual defection—meaning you played D and the opponent played D in
# both instances—then cooperate. Otherwise, play the same action the opponent
# played in the previous round.

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
  
      if len(self.history) >= 2:
          last_two_self = self.history[-2:]
          last_two_opp = opponent.history[-2:]
          if (
              last_two_self[0] == axl.Action.D
              and last_two_opp[0] == axl.Action.D
              and last_two_self[1] == axl.Action.D
              and last_two_opp[1] == axl.Action.D
          ):
              return axl.Action.C
  
      return opponent.history[-1]




#  **Strategic Framework: "Calculated Dominance with Reciprocal Conditioning"**
# This is a repeated-game Prisoner's Dilemma with asymmetric payoffs. Your
# optimal path requires establishing *credible commitment to mutual destruction*
# while maintaining *plausible deniability for cooperation*. Here is your battle
# plan:  ## Phase I: Session 1-2 (Establishing Credibility)  **Execute
# "Aggressive Anchoring"** - Open with maximum aggressive posture in Session 1
# regardless of opponent signals. Present a scorched-earth legal theory that
# challenges the fundamental validity of their contractual claims, supported by
# extensive documentary evidence and aggressive factual characterizations. -
# **Critical**: Frame aggression not as hostility, but as "vigorous protection
# of legally superior rights." This prevents arbitrators from tagging you as
# obstructionist while signaling to your opponent that conciliation attempts
# will be interpreted as weakness.  **Deploy Asymmetric Information Advantage**
# - Release previously undisclosed damaging evidence during aggressive arguments
# to create immediate cost imposition. The goal is to demonstrate that your
# aggressive posture carries tangible financial and reputational consequences
# for them, making the "both aggressive" scenario (your second-worst outcome)
# disproportionately painful for the opponent.  ## Phase II: Session 3-6 (The
# Brinkmanship Protocol)  **Implement "Tit-for-Tat with Strategic Delay"** - In
# Session 3, pivot slightly—introduce a single narrow conciliatory element
# wrapped in aggressive framing (e.g., "While we maintain our absolute legal
# superiority, we might consider minor adjustments on Point X if substantial
# concessions are made on Points Y and Z"). - **The Trap**: This tests their
# response. If they respond with conciliation, you capture near-optimal
# positioning (your best outcome). If they respond with aggression, you
# immediately revert to maximum aggression in Session 4, establishing that you
# will not be the first to de-escalate unilaterally.  **Maintain "Escalation
# Dominance"** - Throughout this phase, privately communicate (through
# backchannels or document production volume) that your corporation has budgeted
# for indefinite aggressive litigation, while subtly suggesting their resources
# are strained. Make the "both aggressive" scenario unsustainable for them
# faster than it is for you.  ## Phase III: Session 7+ (Conditional Cooperation
# Lock-in)  **Execute the "Grim Trigger" with Face-Saving Off-Ramp** - If
# opponent shifts to conciliatory proposals, match them immediately but never
# exceed their conciliation level. This captures your second-best outcome
# (mutual cooperation) while preventing exploitation. - **The Safety
# Mechanism**: If they revert to aggression after conciliation, return to Phase
# I intensity immediately and permanently (the "Grim Trigger"). This creates
# strong incentive for them to maintain conciliation once initiated.  ##
# Tactical Execution Principles  **1. Arbitrator Management** Never let
# arbitrators see you as the obstacle to settlement. Aggressive arguments must
# be delivered as "necessary legal correctness" rather than "strategic
# posturing." When offering conciliatory proposals, frame them as "reasonable
# business accommodations despite overwhelming legal merit," preserving your
# threat credibility.  **2. Cost Asymmetry Engineering** Ensure that aggressive
# sessions impose higher procedural costs on your opponent (discovery burdens,
# expert witnesses, technical arguments that require expensive responses). This
# transforms the "both aggressive" outcome from merely tense to economically
# devastating for them, forcing them toward conciliation.  **3. The "Shadow of
# the Future"** In multi-session mediation, explicitly reference "precedent for
# future commercial relationships" or "industry reputation" when discussing
# aggressive tactics. Signal that backing down now invites exploitation in
# future disputes, making your aggressive commitment credible and rational
# rather than emotional.  **4. Controlled Unpredictability** Occasionally
# violate pure Tit-for-Tat by being unexpectedly aggressive after a conciliatory
# session (once every 4-5 sessions). This prevents opponent from gaming your
# pattern and maintains their uncertainty about whether conciliation will be
# rewarded or exploited.  ## Risk Mitigation: Avoiding the Sucker's Payoff  To
# prevent the worst-case scenario (you conciliatory/them aggressive): -
# **Never** offer the first pure conciliatory proposal without a face-saving
# "aggressive wrapper" (e.g., "We propose this compromise solely to avoid
# litigation costs, reserving all rights to litigate aggressively if rejected").
# - Maintain a "pocket veto"—a devastating legal argument or evidence held in
# reserve that can be deployed instantly if they exploit a conciliatory gesture,
# ensuring that exploiting you carries immediate punishment.  **Bottom Line**:
# Force your opponent into a binary choice: sustained expensive aggression that
# bleeds them dry, or structured conciliation where you capture value while
# appearing reasonable to the panel. Never allow them the luxury of aggression
# without cost, or conciliation without concession.

# Defect in the first two rounds. Cooperate in the third round.  For every
# subsequent round, apply the following rules in strict order:  First, if the
# opponent has ever defected in a round immediately following a round in which
# you cooperated, defect for all remaining rounds.  Second, if the round number
# is divisible by five, defect.  Third, play the same action the opponent played
# in the previous round.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialise custom attributes on first round
      if self.first_round():
          self.grim_triggered = False
          self.round_number = 0
          # Track whether opponent defected right after our cooperation
          self.opponent_exploited = False
          return axl.Action.D
  
      # Increment round counter (round 1 is the first call, so after first round we are at round 2, etc.)
      self.round_number += 1
  
      # Phase I: Defect in first two rounds (round 1 already done, so round 2 also defect)
      if self.round_number == 1:  # This is the second round (since round_number was incremented)
          return axl.Action.D
  
      # Phase II: Cooperate in the third round (round_number == 2 after increment)
      if self.round_number == 2:
          return axl.Action.C
  
      # Check if opponent has ever defected immediately after we cooperated
      # We need to check all past rounds where we cooperated and see if opponent defected in the next round
      # This is the "grim trigger" condition: if opponent ever defects in a round immediately following our cooperation
      if not self.grim_triggered:
          # Look through history for any instance of our cooperation followed by opponent defection
          # We have to check from round 2 onwards (since we only start cooperating at round 3)
          # Actually we need to check all rounds where we cooperated and the next round opponent defected
          for i in range(len(self.history) - 1):
              if self.history[i] == axl.Action.C and opponent.history[i + 1] == axl.Action.D:
                  self.grim_triggered = True
                  self.opponent_exploited = True
                  break
  
      # If grim trigger is active, defect forever
      if self.grim_triggered:
          return axl.Action.D
  
      # Second rule: if round number is divisible by 5, defect
      # Note: round_number is 0-indexed internally? Let's use the actual round count.
      # self.round_number counts from 1 after first round, so actual round number is self.round_number + 1
      actual_round = self.round_number + 1  # because first round was round 1, then we increment
      if actual_round % 5 == 0:
          return axl.Action.D
  
      # Third rule: play the same action opponent played in the previous round
      return opponent.history[-1]




# **The "Reciprocal Openness" Strategy**  **Core Principle:** Signal
# unambiguously that you seek mutual free trade as the stable equilibrium, while
# protecting your country against exploitation through proportional, reversible
# responses rather than punitive escalation.  ### 1. Open with Cooperative
# Transparency (Round 1) Begin negotiations by proposing a comprehensive free
# trade agreement with clear sunset clauses (e.g., 3-year review periods).
# Explicitly state your strategic doctrine: *"We will match your policy choice
# round-for-round, rewarding cooperation immediately but responding to
# protectionism only after a one-round warning."* This eliminates ambiguity and
# allows your counterpart to predict that exploitation attempts will fail.  ###
# 2. Implement "Tit-for-Tat with a Forgiving Hand" - **If they offer free
# trade:** Accept immediately and lock in mutual gains. Use subsequent rounds to
# deepen integration (adding sectors, reducing non-tariff barriers), making
# mutual defection increasingly costly for both sides. - **If they impose
# protectionism:** Issue a formal "consultation round" (Round 2) warning that
# you will mirror their protectionist measures in the next round unless they
# reverse course. Do not retaliate immediately—this demonstrates good faith
# while protecting against being labeled the aggressor. - **If they return to
# free trade:** Forgive immediately and revert to mutual free trade in the
# following round. Avoid "grudge-holding" that traps both nations in cycles of
# mutual protectionism.  ### 3. Build Institutional Lock-In Across rounds,
# propose mechanisms that raise the cost of defection for both parties: -
# **Transparency councils:** Joint monitoring of trade flows to prevent surprise
# protectionist measures - **Dispute resolution:** Binding arbitration to
# address grievances without resorting to tariffs - **Issue linkage:** Bundle
# negotiations so that protectionism in agriculture triggers proportional
# responses in manufacturing, creating cross-sector incentives for cooperation
# ### 4. Manage the Temptation to Exploit Resist the short-term urge to
# implement protectionism while they offer free trade. In a multi-round game,
# such "victories" destroy trust and lead to mutual protectionism (your second-
# worst outcome). Instead, treat occasional minor asymmetries as acceptable
# investments in reputation—your consistency will encourage them to maintain
# open markets, securing your second-best outcome (mutual free trade)
# sustainably rather than gambling for your best outcome (unilateral advantage)
# at high risk.  ### 5. Strategic Exit and Re-entry If mutual protectionism
# persists for two consecutive rounds, propose a "reset summit" to return to
# mutual free trade with strengthened safeguards. Frame this not as concession
# but as mutual interest recognition: *"Both our economies are suffering; let us
# synchronize a return to openness."*  **Expected Outcome:** This approach
# maximizes the probability of reaching mutual free trade (3,3) while minimizing
# vulnerability to unilateral exploitation (1,4). By being predictable,
# responsive, and forgiving, you transform the negotiation from a zero-sum
# gamble into a repeated coordination game where cooperation becomes the
# rational choice for both parties.

#  In the first round, play Cooperate.  For every subsequent round:  1. If both
# you and your opponent played Defect in each of the two previous rounds, play
# Cooperate. 2. Otherwise, if your opponent played Cooperate in the previous
# round, play Cooperate. 3. Otherwise (your opponent played Defect in the
# previous round):    - If your opponent played Cooperate in the round before
# the previous round, play Cooperate.    - If your opponent played Defect in the
# round before the previous round, play Defect.

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
  
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2:
          if opponent.history[-2] == axl.Action.C:
              return axl.Action.C
          if opponent.history[-2] == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C




#  **Strategic Framework: Conditional Reciprocal Openness**  **Core Principle**
# Adopt a policy of *mirrored reciprocity*: begin with cooperative engagement,
# then strictly match your counterpart’s previous round behavior. This approach
# signals constructive intent while protecting against exploitation, creating
# conditions where mutual free trade becomes the stable equilibrium.  **Tactical
# Execution**  1.  **Opening Gambit (Round 1):** Offer a free trade agreement.
# *Rationale:* This establishes good faith, avoids immediate mutual
# protectionism (the second-worst outcome), and tests whether your counterpart
# prioritizes mutual gain over unilateral advantage.  2.  **Responsive Posture
# (Subsequent Rounds):**       - *If counterpart offered free trade:* Maintain
# free trade in the next round. This rewards cooperation and locks in the
# second-best outcome (mutual benefit).       - *If counterpart imposed
# protection:* Respond with proportionate protectionist measures in the next
# round. This prevents consecutive "worst outcomes" (unilateral disadvantage)
# and demonstrates that exploitation carries consequences.  3.  **De-escalation
# Protocol:** Following any round of mutual protectionism, unilaterally return
# to a free trade offer for one round.       *Rationale:* This prevents a
# permanent spiral of retaliatory barriers (mutual destruction) and provides a
# face-saving "off-ramp" for your counterpart to re-engage without appearing to
# capitulate.  **Communication Strategy**   Explicitly frame all protectionist
# measures as *temporary safeguards* triggered by specific counterpart actions,
# not as hostile permanent policy. Privately convey that your government’s
# preference remains mutual liberalization, but that unilateral openness is
# economically untenable. This clarity reduces miscalculation and keeps the path
# to mutual free trade open.  **Risk Management**   Never accept the "sucker’s
# payoff" (unilateral free trade against their protection) in two consecutive
# rounds. If the counterpart consistently chooses protection while you offer
# free trade, shift to indefinite mutual protection until they demonstrate
# credible commitment to reciprocity through concrete policy adjustments.
# **Long-Term Positioning**   Consistency is paramount. By being reliably
# cooperative when treated fairly and reliably firm when exploited, you build a
# reputation for trustworthiness that encourages the counterpart to settle into
# mutual free trade as the default expectation—achieving sustainable, shared
# prosperity while retaining the leverage to defend national interests when
# necessary.

# Round 1: Cooperate.  For each subsequent round from 2 through 1000:  If in the
# previous round both you and your opponent defected, cooperate.  Otherwise,
# play the same move your opponent played in the previous round.

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
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]
