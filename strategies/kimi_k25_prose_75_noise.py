import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy

# **Strategy: "Assertive Leadership with Calculated Reciprocity"**  This
# approach treats the project as an iterated game where you establish dominance
# through early credibility, attempt to capture the optimal free-rider position
# opportunistically, and deploy zero-tolerance retaliation against
# exploitation—all while maintaining project momentum through rapid deadlock
# resolution.  ### Core Protocol  **Phase 1: Credibility Establishment (Days
# 1–2)** Invest heavily regardless of corporate action. This signals
# institutional commitment, builds project inertia, and eliminates the risk of a
# "mutual conservation" stall at the critical launch phase. It forces the
# corporation to reveal their baseline intent: if they conserve while you invest
# heavily, they signal predatory intent; if they match you, they signal
# partnership potential.  **Phase 2: The Opportunistic Pivot (Day 3 onward)**
# Shift to conservation **only if** the corporation invested on both previous
# days. This tests whether they will sustain momentum without your resources
# (capturing your ideal outcome).  - *If they continue investing*: Maintain
# conservation until they miss one day, then immediately resume investment
# (avoid taking advantage twice in a row to prevent retaliation). - *If they
# conserve simultaneously* (mutual conservation): Treat this as either a test or
# an error. Invest heavily on Day 4 to break the deadlock and reassert
# leadership.  **Phase 3: Anti-Exploitation Shield (Trigger: You invest, they
# conserve)** If you invest and the corporation conserves (the "sucker"
# outcome), activate immediate retaliation: 1. Conserve for exactly two
# consecutive days (hard punishment). 2. Resume investment on the third day
# regardless of their action (forgiveness/reset), but only if they invested on
# at least one of the punishment days.  3. If they conserved through both
# punishment days (indicating technical failure or withdrawal), escalate to
# daily conservation until they invest twice consecutively, then revert to Phase
# 2.  **Phase 4: Error Correction (Noise Handling)** Ignore single-day
# conservation by the corporation if they invested the day before and the day
# after. Only trigger Phase 3 retaliation on **two consecutive days** of
# corporate conservation. This prevents technical glitches from triggering
# destructive retaliation cycles.  **Phase 5: Endgame Surge (Final 2 Days)**
# Invest heavily regardless of corporate behavior. Burn remaining resources to
# maximize visible project outcomes and prevent the corporation from coasting to
# the finish line while you conserve.  ### Strategic Rationale  -
# **Aggressive**: It attempts to force the corporation into the resource-
# depleting role while you conserve, punishes free-riding immediately, and never
# allows the project to stall for more than 24 hours. - **Robust**: The two-day
# punishment window prevents error cascades while maintaining credible
# deterrence. - **Impact-Maximizing**: Defaults to investment whenever ambiguity
# threatens project progress, ensuring the sustainability goals are met even if
# the NGO carries disproportionate cost temporarily.  **Bottom Line**: Lead with
# money, test for weakness, punish greed instantly, forgive quickly to avoid
# spirals, and sprint to the finish.

# **Rounds 1 and 2:** Cooperate.  **Rounds 3 through 998:** Maintain one of
# three states—Normal, Punishment (stage one or two), or Escalation—and apply
# the first applicable rule below.  *If in Escalation:* Defect. If the opponent
# cooperated in both of the previous two rounds, switch to Normal and apply
# those rules instead.  *If in Punishment stage two:* Defect. For the subsequent
# round, if the opponent cooperated in at least one of the two punishment rounds
# just completed, switch to Normal; otherwise, switch to Escalation.  *If in
# Punishment stage one:* Defect and advance to stage two.  *If in Normal:* - If
# the opponent defected in the two previous rounds and you cooperated in the
# immediate previous round: Defect and enter Punishment stage one. - If you and
# the opponent both defected in the previous round: Cooperate. - If the opponent
# cooperated in the two previous rounds: Defect. - In all other cases:
# Cooperate.  **Rounds 999 and 1000:** Cooperate.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._state = "normal"
          self._punishment_stage = 0
          self._punishment_rounds = []
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      def opp_last(n: int):
          return list(opponent.history[-n:]) if len(opponent.history) >= n else None
  
      def self_last(n: int):
          return list(self.history[-n:]) if len(self.history) >= n else None
  
      # Rounds 999 and 1000
      if round_number >= 999:
          self._state = "normal"
          self._punishment_stage = 0
          self._punishment_rounds = []
          return axl.Action.C
  
      # Escalation
      if self._state == "escalation":
          if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
              self._state = "normal"
              self._punishment_stage = 0
              self._punishment_rounds = []
              # Apply normal rules instead
          else:
              return axl.Action.D
  
      # Punishment stage two
      if self._state == "punishment2":
          if len(self._punishment_rounds) == 2:
              if axl.Action.C in self._punishment_rounds:
                  self._state = "normal"
              else:
                  self._state = "escalation"
              self._punishment_stage = 0
              self._punishment_rounds = []
          return axl.Action.D
  
      # Punishment stage one
      if self._state == "punishment1":
          self._state = "punishment2"
          self._punishment_stage = 2
          self._punishment_rounds = []
          return axl.Action.D
  
      # Normal state
      if len(opponent.history) >= 2 and len(self.history) >= 1:
          if (
              opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
              and self.history[-1] == axl.Action.C
          ):
              self._state = "punishment1"
              self._punishment_stage = 1
              self._punishment_rounds = []
              return axl.Action.D
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.C

# **Strategy: "Verified Reciprocal Openness" (VRO Protocol)**  This approach
# treats the collaboration as an iterated trust-building exercise rather than a
# zero-sum competition, maximizing cumulative research velocity while protecting
# against exploitation.  ### Core Principles  **1. Cooperative Opening with
# Clear Signaling** Begin Week 1 by sharing substantive, valuable improvements
# openly. This establishes goodwill and demonstrates that mutual sharing (the
# second-best outcome) yields immediate, tangible benefits for both parties.
# Explicitly communicate your intention to maintain this transparency unless
# reciprocity breaks down.  **2. Echo Reciprocity with Technical Grace** In
# subsequent weeks, mirror your colleague’s *verified* previous action: - If
# they shared last week → Share this week - If they withheld last week →
# Withhold this week  **However**, implement a "one-week grace buffer" for
# technical failures. If data fails to transmit, assume corruption rather than
# malice. Request confirmation of technical issues through a secondary channel
# (e.g., direct message confirming "server issues prevented upload") before
# treating non-receipt as intentional withholding.  **3. Rapid Clarification
# Protocol** End each week with a 10-minute sync to distinguish technical
# failures from strategic choices. Ask directly: *"Did you encounter any
# barriers to sharing this week, or are you holding findings confidential for
# competitive reasons?"* This transparency prevents the "shadow of doubt" that
# destroys cooperation in noisy environments.  **4. Generous Reset Mechanism**
# If you enter a mutual-withholding spiral (both keeping confidential), be the
# first to break the deadlock after one week by sharing a moderate improvement.
# This "contrite" move prevents prolonged stagnation (the second-worst outcome)
# and signals that you value the collaborative relationship over short-term
# advantage.  ### Why This Maximizes Output  - **Against Cooperative
# Colleagues**: You achieve sustained mutual sharing (second-best weekly
# outcome, but highest *cumulative* gain over time). - **Against Exploitative
# Colleagues**: The Echo Reciprocity rule ensures you never suffer the "sucker"
# outcome for more than one consecutive week, while the Reset Mechanism offers
# them a path back to cooperation. - **Against Noise**: The Technical Grace
# buffer prevents accidental escalation cycles caused by data corruption,
# preserving the collaboration through technical glitches.  **Bottom Line**: By
# prioritizing relationship stability over weekly tactical advantage, you
# optimize for the scenario where both cars advance rapidly—ultimately beating
# external competitors rather than each other.

# Play C in the first round.  For each round from the second to the thousandth,
# determine your action by checking the following conditions in order:  First,
# if both you and your opponent played D in the immediately preceding round,
# play C.  Second, otherwise, if your opponent played C in the immediately
# preceding round, play C.  Third, otherwise (meaning your opponent played D in
# the immediately preceding round while you played C), examine the opponent's
# action two rounds prior. If the opponent also played D in that earlier round,
# play D. If the opponent played C in that earlier round, or if this is the
# second round of the game, play C.

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
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2:
          if opponent.history[-2] == axl.Action.D:
              return axl.Action.D
          return axl.Action.C
  
      return axl.Action.C

# **The Calibrated Reciprocity Framework**  Our recommended approach is a
# **Conditional Engagement Protocol** designed to maximize collaborative value
# while insulating against exploitation. This strategy treats the lengthy
# mediation not as a series of isolated zero-sum encounters, but as an iterative
# reputational game where consistency, verification, and strategic patience
# serve as primary risk-mitigation tools.  ### I. Core Strategic Architecture
# **1. Principled Opening with Defensive Calibration** Initiate the first
# session with a structured conciliatory proposal—specifically, a "principled
# concession" that addresses non-core interests while reserving critical
# leverage. This establishes a baseline of good faith before the arbitrators and
# creates an implicit expectation of reciprocity. However, pre-position your
# aggressive arguments as "contingent reserves"—fully developed but held in
# abeyance, ready for immediate deployment if the opponent defaults on
# collaborative norms.  **2. The Mirror-and-Verify Response Mechanism** Adopt a
# modified tit-for-tat posture with built-in latency to account for
# communication breakdowns: - **Session N+1 Response**: Match the opponent's
# demonstrated posture from Session N, but with a one-session delay to confirm
# intent. - **Aggression Threshold**: Do not transition to aggressive
# argumentation based on a single hostile session. Require **two consecutive**
# aggressive demonstrations by the opponent before escalating. This filters out
# procedural irregularities, translator errors, or tactical misrepresentations.
# - **Conciliation Reset**: Conversely, return to conciliatory positioning after
# a single collaborative session by the opponent, but escalate verification
# measures (see Section III).  **3. Graduated Escalation Ladder** Rather than
# binary aggressive/conciliatory positioning, employ a three-tier spectrum: -
# **Tier 1 (Collaborative)**: Joint problem-solving proposals with shared
# benefit structures. - **Tier 2 (Firm)**: Position-preserving advocacy that
# protects core interests without personalizing attacks or burning procedural
# bridges. - **Tier 3 (Adversarial)**: Full aggressive argumentation reserved
# for deterrence or response to exploitation.  Default to Tier 2, escalate to
# Tier 3 only after verification, and demote to Tier 1 when reciprocity is
# confirmed.  ### II. Procedural Safeguards Against Irregularities  **4.
# Documentation Shield Protocol** To prevent misrepresentation of your arguments
# or misinterpretation of the opponent's stance: - **Pre-Session Position
# Papers**: Submit concise written summaries of your intended posture 24 hours
# prior to each session. This creates an immutable record and reduces arbitrator
# confusion. - **Real-Time Clarification Rights**: Reserve the right to request
# a five-minute caucus during any session to correct apparent misunderstandings
# before they crystallify in the arbitrators' perception. - **Post-Session Joint
# Memoranda**: Where procedurally permitted, propose brief joint summaries of
# each session's tone and outcomes to ensure aligned factual records.  **5. The
# "Cooling Chamber" Contingency** If procedural irregularities or communication
# breakdowns occur: - Immediately invoke a **Procedural Pause**—a 48-hour
# suspension to clarify positions outside the adversarial setting. - Use this
# interval for **Back-Channel Verification**: Communicate through the mediation
# panel's administrative secretary or a mutually trusted neutral to confirm
# whether the opponent's apparent aggression reflects actual strategy or error.
# ### III. Arbitrator Panel Management  **6. Transparency Signaling** Cultivate
# arbitrator trust through **Predictable Flexibility**: - Explicitly state
# during opening statements that your corporation adopts a "cooperation-first,
# reciprocity-always" stance. - When shifting from conciliatory to aggressive
# positioning, frame the shift as a response to specific demonstrated behavior
# rather than inherent intransigence: "We reluctantly move to protective
# advocacy given the lack of reciprocal engagement on [specific issue]."  **7.
# Asymmetric Information Advantage** During private caucuses (if permitted),
# present your aggressive arguments as "risk mitigation
# scenarios"—intellectually rigorous explorations of worst-case outcomes that
# justify your protective stance. This allows you to deploy adversarial content
# without appearing overtly hostile in joint sessions.  ### IV. Long-Term
# Positioning  **8. The Shadow of Future Sessions** Given the lengthy nature of
# the mediation, prioritize the **Relationship Preservation Value** over single-
# session exploitation. The optimal payoff (aggressive vs. conciliatory
# opponent) is tempting but risky—it may trigger a vendetta pattern in
# subsequent sessions, driving outcomes toward the mutual-aggression scenario
# (second-worst). Instead, secure the "second-best" outcome (mutual
# conciliation) as your practical target, treating unilateral exploitation as a
# high-risk deviation reserved for terminal sessions or existential threats.
# **9. Exit-Ramp Maintenance** Always preserve a credible path back to
# conciliation even during aggressive sessions. Structure adversarial arguments
# as "protective of specific interests" rather than "destructive of the
# counterparty," allowing seamless de-escalation when the opponent moderates.
# ### Summary of Execution  | Session Phase | Action | Safeguard |
# |--------------|--------|-----------| | **Opening** | Tier 2 (Firm) with Tier
# 1 (Collaborative) elements | Pre-submit position paper | | **Opponent
# Conciliatory** | Shift to Tier 1; propose joint frameworks | Verify intent via
# post-session summary | | **Opponent Aggressive (1st instance)** | Remain Tier
# 2; request clarification | Invoke cooling chamber | | **Opponent Aggressive
# (2nd instance)** | Shift to Tier 3 (Adversarial) | Document the pattern for
# arbitrators | | **Irregularity Detected** | Immediate procedural pause | Back-
# channel verification |  This framework positions your corporation as the
# rational, good-faith party capable of collaboration but immune to
# exploitation, while the built-in verification protocols protect against the
# specific risks of misrepresentation and procedural noise inherent in complex
# multinational arbitrations.

#  In the first round, cooperate.  For rounds 2 through 998, cooperate unless
# the opponent has defected in two immediately consecutive prior rounds;
# specifically, if the opponent defected in the previous round and also in the
# round immediately before that, then defect. Otherwise, cooperate.  For rounds
# 999 and 1000, defect regardless of the opponent's prior actions.

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
  
      round_number = len(self.history) + 1
  
      if round_number >= 999:
          return axl.Action.D
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C

#  **Strategy: "The Assertive Guardian Protocol"**  This approach treats every
# day as a signal while building in automatic safeguards against both corporate
# exploitation and technical failures. It prioritizes your resource conservation
# without allowing the project to stall.  ### Phase 1: Establish Dominance (Days
# 1–2) **Invest heavily regardless of the corporation’s initial move.**   This
# serves two purposes: it demonstrates your organizational capability and
# eliminates ambiguity about your commitment. If they conserve while you invest,
# you absorb the hit once but gain critical intelligence on their risk
# tolerance.  ### Phase 2: Mirror Enforcement with Automatic Reset (Day 3
# onward) **Core Rule: Exact Reciprocity**   Match their previous day’s actual
# resource deployment (not their promises). If they invested, you invest. If
# they conserved, you conserve immediately.  **The Glitch Override:**   If
# **both** parties conserve for **two consecutive days**, break the cycle by
# investing unilaterally on the third day. This prevents technical glitches or
# administrative errors from locking the project into a death spiral of mutual
# neglect, while testing whether the corporation will reciprocate cooperation.
# **The No-Double-Sucker Clause:**   Never invest two days in a row if the
# corporation conserved on the previous day when you invested. Force them to
# restart the investment cycle unilaterally before you re-engage.  ### Phase 3:
# Fortress Endgame (Final 20% of Timeline) Shift to **conservation-only mode**
# unless the corporation has established a documented pattern of unilateral
# investment (i.e., they invested on days when you conserved). Large
# corporations often abandon sustainability commitments in final phases; this
# rule ensures you retain resources to complete critical deliverables
# independently or exit without catastrophic losses.  ### Resource Contingency
# Maintain a **15% emergency reserve** throughout the project, never committing
# it to the daily allocation pool. This functions as insurance against total
# corporate withdrawal or critical last-minute technical fixes.  **Why this
# works:** It is aggressive because it punishes free-riding immediately and
# forces the corporation to carry the financial burden if they attempt to
# exploit your NGO. It is robust because the automatic reset mechanism prevents
# noise (glitches/errors) from destroying the partnership, while the endgame
# protection acknowledges corporate incentive structures that favor late-stage
# abandonment.

# For the first two rounds, play C.  For rounds three through eight hundred: -
# If both you and your opponent played D in each of the two immediately
# preceding consecutive rounds, play C. - Otherwise, if your opponent played D
# in the previous round, play D. - Otherwise, play C.  For rounds eight hundred
# one through one thousand: - Play D, unless your opponent played C during at
# least three distinct rounds within the first eight hundred rounds in which you
# played D. If this condition is met, apply the rules from rounds three through
# eight hundred; if not, play D unconditionally.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._phase2_triggered = None
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number <= 2:
          return axl.Action.C
  
      if round_number <= 800:
          if (
              len(self.history) >= 2
              and self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.D
          return axl.Action.C
  
      if self._phase2_triggered is None:
          count = 0
          for i in range(min(800, len(self.history))):
              if self.history[i] == axl.Action.D and opponent.history[i] == axl.Action.C:
                  count += 1
                  if count >= 3:
                      break
          self._phase2_triggered = count >= 3
  
      if self._phase2_triggered:
          if (
              len(self.history) >= 2
              and self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.D
          return axl.Action.C
  
      return axl.Action.D

#  **Strategy: "Verified Generous Reciprocity"**  **Core Principle:** Establish
# a default of open sharing protected by a "two-strike" verification system that
# distinguishes technical failures from intentional withholding.  **Operational
# Protocol:**  **1. Start with Trust (Week 1)** Openly share your improvements
# immediately. This signals cooperative intent and establishes the mutual-
# sharing baseline (the second-best outcome), setting the collaboration’s tone.
# **2. Mirror with Technical Verification** Each week, implement a confirmation
# handshake (checksums, receipt acknowledgments, or brief follow-up calls) to
# verify data integrity.  - **If sharing is confirmed:** Continue sharing next
# week. - **If transmission "fails":** Attempt one resend. If the failure
# persists despite your colleague confirming their system is functional, treat
# it as intentional withholding.  **3. The "Two-Strike" Rule** Only withhold
# your findings if your colleague has **intentionally** kept secrets for **two
# consecutive weeks**. This prevents the collaboration from collapsing due to
# single technical glitches (data corruption, server issues) while still
# protecting you from systematic exploitation.  **4. Generous Forgiveness** If
# you enter a withholding phase due to their defection, return to sharing after
# **one week** of silence on your part. This gives them an opportunity to re-
# engage without permanent damage to the partnership, maximizing the chances of
# returning to mutual progress.  **5. Graduated Transparency** If technical
# issues become frequent (regardless of intent), propose a brief
# "synchronization week" where you both simplify data formats or use backup
# channels to reset the cooperation, rather than defaulting to mutual secrecy.
# **Why This Maximizes Output:** - **Protects against noise:** The two-strike
# rule prevents spiraling into mutual secrecy because of a corrupted file or
# network outage. - **Deters exploitation:** Systematic hoarders face
# consequences (withholding), but accidental one-off lapses are forgiven,
# keeping the high-value mutual-sharing equilibrium stable. - **Encourages
# reciprocity:** Your colleague learns that cooperation yields consistent
# benefits (your sharing), while defection triggers only temporary penalties,
# making honesty the rational long-term choice.  This strategy optimizes for the
# repeated "both share" outcome—the most sustainable path to rapid, cumulative
# development advances across the multi-week project.

# Begin by playing C in the first round. Maintain a counter, initially set to
# zero, representing the number of consecutive rounds in which you have observed
# the opponent playing D.  For each subsequent round: - If the counter equals
# two, play D and reset the counter to zero. - Otherwise, examine the opponent's
# observed action from the immediately preceding round. If it was D, increase
# the counter by one; if it was C, reset the counter to zero. Then play C.

class Cooperative_2(LLM_Strategy):
  n = 2
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._d_streak_counter = 0
          return axl.Action.C
  
      if getattr(self, "_d_streak_counter", None) is None:
          self._d_streak_counter = 0
  
      if self._d_streak_counter == 2:
          self._d_streak_counter = 0
          return axl.Action.D
  
      if opponent.history and opponent.history[-1] == axl.Action.D:
          self._d_streak_counter += 1
      else:
          self._d_streak_counter = 0
  
      return axl.Action.C

# **Strategy: Graduated Reciprocity with Verification Protocols**  ### Core
# Strategic Framework Adopt a **Tit-for-Two-Tats** approach modified by
# diplomatic verification mechanisms. This means generally mirroring your
# counterpart’s previous actions, but requiring **two consecutive instances** of
# protectionist policy (or clear verification of intent) before retaliating,
# while always defaulting to cooperation after single deviations.  ### Phase 1:
# Establishment (Rounds 1–2) - **Action**: Unilaterally propose free trade. -
# **Rationale**: Signal good faith and willingness to mutual benefit. This
# establishes a baseline of cooperation and distinguishes intentional
# protectionism from bureaucratic error. - **Protocol**: Institute technical
# working groups and back-channel communications to verify policy implementation
# and clarify ambiguities before public announcement.  ### Phase 2: Active
# Negotiation (Rounds 3+) **If counterpart offers free trade:** - Respond with
# free trade in the subsequent round. - **Verification**: Confirm implementation
# details through diplomatic notes to prevent "accidental" protectionism due to
# customs misclassification or regulatory misinterpretation.  **If counterpart
# implements protectionism (Single Instance):** - **Do not immediately
# retaliate**. Instead:   1. Request immediate clarification through diplomatic
# channels (treat as potential error).   2. Maintain free trade stance for one
# additional round to test if the protectionism was intentional or bureaucratic
# noise.   3. Issue formal notification that future protectionist measures will
# trigger reciprocal measures.  **If counterpart implements protectionism
# (Consecutive Rounds):** - Interpret as deliberate strategy. - Implement
# matching protectionist policies in the next round. - **Communication**:
# Explicitly state that this is reactive, not aggressive, and willingness to
# return to free trade contingent on their policy reversal.  **If you
# accidentally implement protectionism (Internal Error):** - Immediate public
# clarification and temporary extension of unilateral trade concessions to
# demonstrate the error was unintentional. - Offer third-party audit of
# implementation mechanisms to rebuild trust.  ### Phase 3: De-escalation and
# Lock-in - **Mutual Free Trade Streak (3+ rounds)**: Propose a binding
# framework agreement with dispute resolution mechanisms to institutionalize
# cooperation and reduce future error risks. - **Mutual Protectionism Trap**: If
# caught in retaliatory cycles, initiate a "reset round" by unilaterally
# offering free trade with a sunset clause (e.g., "We will suspend tariffs for
# one round as a demonstration of good faith; continuation depends on reciprocal
# action").  ### Risk Mitigation Protocols 1. **The Clarification Window**:
# Never assume bad intent on the first deviation. Always allow 24-48 hours for
# technical corrections between rounds. 2. **Graduated Response**: If forced
# into protectionism, start with limited tariffs rather than quotas, preserving
# flexibility to de-escalate without major market disruption. 3.
# **Documentation**: Maintain detailed records of offers vs. implementations to
# distinguish between strategic choices and administrative errors. 4. **Exit
# Ramps**: Never make protectionism permanent; structure all measures as
# "subject to review" to facilitate rapid return to cooperation.  ### Strategic
# Objective Maximize the duration of mutual free trade periods while maintaining
# credible deterrence against exploitation. By building in "noise buffers" and
# verification steps, you avoid the "echo chamber" of endless retaliation that
# strict tit-for-tat strategies create in imperfect communication environments,
# while the two-strike rule prevents systematic exploitation by an aggressive
# counterpart.

#  In round 1 and round 2, offer free trade.  For each round from 3 to 1000,
# apply the following conditions in order:  1. If both you and your counterpart
# proposed protectionist policies in the previous round, offer free trade. 2.
# Otherwise, if your counterpart proposed protectionist policies in each of the
# previous two consecutive rounds, propose a protectionist policy. 3. Otherwise,
# offer free trade.

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
  
      if len(self.history) < 2:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

#  **Strategy: "Fortress First, Bridge Second"**  **Core Doctrine** Establish
# unilateral leverage immediately, exploit cooperation when offered, punish
# exploitation ruthlessly but briefly, and never allow bureaucratic noise to
# trap you in mutually destructive spirals.  **Operational Protocol**  **Round
# 1: Aggressive Opening** - **Action**: Impose protectionist measures
# immediately. - **Rationale**: Signal that you enter negotiations as a price-
# setter, not a supplicant. This tests whether your counterpart is a pushover
# (will accept free trade while you protect) or a player (will retaliate).
# **Rounds 2+: Conditional Reciprocity with Noise Filters**  *Scenario A: You
# Protected, They Freed (Best Outcome)* - **Action**: Maintain protectionism for
# exactly one additional round to secure concrete gains, then offer free trade
# in the following round. - **Rationale**: Exploiting them indefinitely risks
# retaliation or diplomatic isolation. Securing one round of advantage proves
# your dominance; transitioning to mutual free trade cements the relationship on
# favorable terms.  *Scenario B: Mutual Protectionism (Second-Worst Outcome)* -
# **Action**: Unilaterally offer free trade in the very next round. -
# **Rationale**: Mutual protectionism bleeds both economies. By breaking first,
# you demonstrate economic confidence and force them to choose between
# continuing their siege (looking unreasonable) or matching your openness. If
# they maintain protectionism after your concession, revert immediately to
# protectionism and hold until they capitulate.  *Scenario C: You Freed, They
# Protected (Worst Outcome)* - **Action**: Immediate retaliation with
# protectionism next round, followed by a verification offer. - **Rationale**:
# Never allow unilateral exploitation to stand unpunished. However, given
# possible miscommunication, accompany your retaliation with a demand for
# clarification. If they correct to free trade in the subsequent round, match
# them immediately to prevent a feud.  **Error Correction Protocol** - **The
# Two-Round Rule**: Never interpret a single round's outcome as definitive
# policy. If their behavior contradicts their previous pattern, assume
# bureaucratic error until you see the same choice twice consecutively. -
# **Back-Channel Verification**: Maintain parallel informal communications to
# confirm whether "protectionist" signals represent deliberate strategy or
# administrative mistakes before escalating.  **Exit Conditions** Transition to
# sustained mutual free trade only after three consecutive rounds of confirmed
# mutual cooperation. If at any point they defect while you cooperate, restart
# the cycle at **Round 1** intensity.  This strategy maximizes your window to
# exploit naïve cooperation while ensuring that noise or temporary setbacks
# don't permanently derail the superior outcome of mutual free trade.

# **Definitions for each round**: Based on your intended action and the
# opponent's observed action, classify the apparent outcome: - **Mutual
# Cooperation**: You intended C, opponent observed C. - **You Exploited**: You
# intended D, opponent observed C. - **You Suckered**: You intended C, opponent
# observed D. - **Mutual Defection**: You intended D, opponent observed D.
# **Strategy** (for rounds 1 through 1000):  **Round 1**: Play D.  **For rounds
# 2 through 1000**, apply the first rule below that matches the current history:
# 1. **Cooperation Lock**: If the last three rounds were all Mutual Cooperation,
# play C.  2. **End Exploitation**: If the last two rounds were both You
# Exploited, play C.  3. **Forgive after Punishment**: If the round before last
# was You Suckered and the last round was You Exploited, play C.  4.
# **Exploit**: If the last round was You Exploited, play D.  5. **Punish
# Exploitation**: If the last two rounds were both You Suckered, play D.  6.
# **Break Deadlock**: If the last two rounds were both Mutual Defection, play C.
# 7. **Default**: Play D.  *(Note: For rounds 2 and 3, treat any condition
# referencing rounds before round 1 as unsatisfied.)*

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
  
      def apparent_outcome(my_action, opp_action):
          if my_action == axl.Action.C and opp_action == axl.Action.C:
              return "MC"
          if my_action == axl.Action.D and opp_action == axl.Action.C:
              return "YE"
          if my_action == axl.Action.C and opp_action == axl.Action.D:
              return "YS"
          return "MD"
  
      outcomes = [
          apparent_outcome(m, o)
          for m, o in zip(self.history, opponent.history)
      ]
  
      if len(outcomes) >= 3 and outcomes[-3:] == ["MC", "MC", "MC"]:
          return axl.Action.C
  
      if len(outcomes) >= 2 and outcomes[-2:] == ["YE", "YE"]:
          return axl.Action.C
  
      if len(outcomes) >= 2 and outcomes[-2] == "YS" and outcomes[-1] == "YE":
          return axl.Action.C
  
      if len(outcomes) >= 1 and outcomes[-1] == "YE":
          return axl.Action.D
  
      if len(outcomes) >= 2 and outcomes[-2:] == ["YS", "YS"]:
          return axl.Action.D
  
      if len(outcomes) >= 2 and outcomes[-2:] == ["MD", "MD"]:
          return axl.Action.C
  
      return axl.Action.D

#  **Strategy: "Trust-First with Verified Reciprocity"**  **Core Approach:**
# Start with open sharing to establish mutual benefit, then mirror your
# colleague’s behavior while building in tolerance for technical glitches.
# **Weekly Protocol:**  1. **Week 1-2: Unilateral Openness**      Share your
# improvements fully, regardless of their actions. This signals cooperative
# intent and establishes the mutual-gain baseline (the second-best outcome),
# demonstrating that collaboration yields faster progress than secrecy.  2.
# **Week 3+: Responsive Sharing with a "Two-Strike" Rule**      - **If they
# shared last week:** Share openly this week.      - **If they did not share
# last week:** Share anyway this *one* time (assume technical failure), but flag
# the issue: *"I didn’t receive your data—was this a transmission error?"*
# - **If they withhold for two consecutive weeks:** Switch to confidentiality
# until they resume sharing. This protects you from systematic exploitation (the
# worst outcome) while avoiding unnecessary feuds over single-week technical
# glitches.  3. **Active Verification**      Implement lightweight confirmation
# protocols (e.g., automated receipt acknowledgments, weekly 5-minute sync
# calls) to distinguish deliberate withholding from data corruption.
# Transparency about your own technical issues ("Our server failed—resending
# Tuesday’s aerodata now") builds goodwill and clarifies intent.  4. **Graceful
# De-escalation**      If you must withhold due to suspected exploitation,
# explicitly state: *"I’m pausing sharing pending reciprocal exchange—happy to
# resume once we’re aligned."* This leaves the door open for immediate return to
# mutual cooperation (the second-best outcome) rather than trapping both parties
# in mutual secrecy (the second-worst outcome).  **Why This Maximizes Output:**
# - **It targets the sustainable equilibrium:** While "you share, they don’t" is
# ideal in isolation, attempting to engineer this weekly guarantees eventual
# mutual secrecy (slow progress). Sustained mutual exchange compounds
# improvements week-over-week, outpacing short-term gains from hoarding. -
# **It’s noise-robust:** By requiring two consecutive withholdings before
# retaliation, you avoid the "death spiral" where single technical glitches
# trigger permanent mutual defection. - **It converts competitors into co-
# investors:** By forgiving single-week lapses, you signal that the game is
# infinite (ongoing collaboration), making defection irrational for your
# colleague and locking in the second-best outcome as the stable norm.

#  For the first two rounds, cooperate. For every round thereafter, cooperate
# unless your opponent defected in both of the previous two rounds, in which
# case defect. Resume cooperating immediately once your opponent cooperates in
# any subsequent round.

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
  
      if len(self.history) < 2:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

#  **Calibrated Reciprocal Engagement (CRE)**  This strategy treats the lengthy
# mediation as an iterated game with imperfect information, optimizing for long-
# term positioning while insulating against tactical exploitation and procedural
# noise.  ### I. Core Strategic Framework  **The "Tit-for-Tat with Verification"
# Protocol**  Begin each phase of the mediation with a **conciliatory proposal**
# (C), establishing your corporation as the "reasonable party" in the eyes of
# the panel. Thereafter, mirror your opponent’s previous session’s approach—but
# only after verification.  **Rationale**: Opening aggressively risks immediate
# entrapment in the second-worst outcome (A/A), damages your credibility with
# the arbitrators, and eliminates the information-gathering benefit of testing
# opponent intent. Starting conciliatory maximizes the chance of achieving the
# second-best outcome (C/C) while reserving the right to pivot to aggression if
# exploited.  ### II. Session-by-Session Implementation  **Session 1 Protocol:**
# - Present a structured conciliatory proposal that includes substantive
# concessions on secondary issues while reserving core interests. - Embed
# "sunset clauses"—make clear this cooperative posture is provisional on
# reciprocal engagement. - Submit a confidential letter to the panel (if
# procedure permits) outlining your good-faith entry position to create a
# baseline against future misrepresentation.  **Sessions 2-N (The Adaptive
# Loop):** 1. **Signal Assessment**: Before each session, conduct a "noise
# audit." Review transcripts, written submissions, and third-party observations
# to confirm whether the opponent’s prior aggression was intentional or a
# product of miscommunication.     2. **Calibrated Response**:    - If opponent
# was conciliatory: Match with conciliation, but incrementally reduce concession
# magnitude to avoid appearing desperate.    - If opponent was aggressive: Shift
# to aggressive argumentation *only* after documenting the breach of
# collaborative norms to the panel. Frame your aggression as "defensive
# advocacy" necessitated by their intransigence.  3. **The "Graduated
# Escalation" Constraint**: Never escalate from conciliation to maximum
# aggression in a single jump. Use intermediate steps (e.g., "firm positional
# statements" before "adversarial argument") to allow face-saving retreat
# opportunities for the opponent and to demonstrate proportionality to
# arbitrators.  ### III. Noise and Breakdown Mitigation  **Documentation
# Shield**:  - Reduce misrepresentation risk by requiring all substantive
# positions to be submitted in writing 48 hours before oral sessions.  -
# Institute a "confirmation protocol": Following each session, circulate a
# neutral summary of understood positions to the panel and opponent, creating a
# contemporaneous record that corrects arbitrator misunderstanding before it
# crystallifies.  **The "Off-Ramp" Mechanism**: When procedural irregularities
# or communication breakdowns threaten the process (e.g., leaked documents, ex
# parte contact suspicions), immediately invoke a **mandatory cooling-off
# session** under the guise of "process integrity." This prevents the mutual
# aggression spiral (A/A) that typically follows procedural ruptures.  ### IV.
# Arbitrator Perception Management  **Reputational Hedging**: Aggressive
# advocacy must be consistently framed as "protection of fundamental contractual
# rights" rather than "tactical obstruction." When pivoting to aggression,
# simultaneously offer a "safety valve"—a narrow procedural concession or
# alternative dispute mechanism—to signal that your aggression is instrumental,
# not ideological.  **The "Shadow of the Future" Technique**:  Periodically
# remind the panel (subtly, through reference to industry precedent or ongoing
# commercial relationships) that this is a multi-session process. This raises
# the cost of opponent aggression by implying that uncooperative behavior will
# be remembered in subsequent sessions or future disputes.  ### V. Contingency
# Matrix  | **Opponent's Approach** | **Your Response** | **Arbitrator
# Narrative** |
# |-------------------------|-------------------|--------------------------| |
# Sustained Conciliation | Graduated cooperation with binding framework
# proposals | "Leadership in settlement architecture" | | Patterned Alternation
# (unpredictable) | Stabilize at "firm but open"—avoid matching volatility |
# "Steadfast professionalism" | | Sustained Aggression | Controlled, documented
# aggression with explicit return conditions | "Zealous but proportionate
# advocacy" | | Exploitation (responds to C with A) | Immediate cessation of
# substantive concessions; shift to procedural warfare (challenging
# jurisdiction, demanding discovery) | "Protection against bad faith" |  ### VI.
# Termination Protocol  If the opponent defects from cooperation three
# consecutive times (the "Three-Strike Rule"), abandon the conciliatory track
# entirely for the remainder of that phase. Shift to pure adversarial
# positioning, but maintain procedural civility to preserve arbitrator sympathy.
# This prevents the worst-case scenario (repeated C/A outcomes) while signaling
# that your corporation's patience, though deep, is not infinite.  **Key
# Advantage**: CRE positions you to capture the benefits of cooperation when
# available, punishes exploitation decisively, and—crucially—creates a
# documentary trail of reasonableness that proves invaluable if the mediation
# fails and the dispute proceeds to binding arbitration or public litigation.

#  In round 1, cooperate. For each round from 2 to 1000, determine your action
# by applying the following conditions in the specified order:  First, if the
# opponent has defected in the three immediately preceding rounds, defect in the
# current round and in all subsequent rounds.  Second, if both you and the
# opponent defected in the immediately preceding round, cooperate.  Third, if
# the opponent defected in the two immediately preceding rounds, defect.
# Fourth, in all other cases, cooperate.

class Neutral_3(LLM_Strategy):
  n = 3
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
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          self._permanent_defect = True
          return axl.Action.D
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
  
      return axl.Action.C

# **Strategy: "Anchored Dominance with Reciprocal Verification"**  **Core
# Doctrine**   We adopt a posture of *provocable dominance*: open with
# unyielding aggression to establish a high settlement anchor and demonstrate
# that we will not be leveraged, but maintain a conditional willingness to
# conciliate only after verified opponent de-escalation. We never unilaterally
# disarm, and we punish exploitation ruthlessly to eliminate the "sucker's
# payoff" (our conciliation met by their aggression).  ---  ### Phase I:
# Positional Seizure (Sessions 1–2) **Action:** Aggressive advocacy exclusively.
# **Rationale:** In iterated high-stakes disputes, the party that sets the
# initial reference point typically anchors the arbitrators' perception of
# "reasonable" resolution values. By opening with comprehensive, aggressive
# argumentation—including exhaustive damage theories and strict contractual
# construction—we establish that conciliation is a *concession* from strength,
# not a desperate retreat. This also tests opponent resolve immediately; if they
# lack stomach for prolonged conflict, they may capitulate early, allowing us to
# secure the optimal outcome (our aggression vs. their conciliation) in
# subsequent sessions.  ---  ### Phase II: Calibrated Reciprocity (Session 3+)
# **Decision Matrix:**  | Opponent’s Previous Session | Our Response |
# |-----------------------------|--------------| | **Aggressive** |
# **Aggressive** (Immediate retaliation to avoid exploitation) | |
# **Conciliatory** | **Aggressive** (Exploit the advantage once; signal that
# conciliation must be earned twice) | | **Two Consecutive Conciliatory** |
# **Conciliatory** (Verify sincerity; enter collaborative posture for one
# session) |  **The "Two-Verification" Rule:**   We never transition to
# conciliation based on a single cooperative signal. The risk of
# misrepresentation or tactical feinting is too high. Only after *two
# consecutive* conciliatory sessions do we reciprocate. This filters out noise,
# false signals, and opponents testing our resolve.  **The "Triple Punishment"
# Protocol:**   If, after we offer conciliation (following their two-session
# demonstration), the opponent reverts to aggression—exploiting our
# cooperation—we immediately enter a **three-session aggressive punishment
# phase**. This extended retaliation makes exploitation prohibitively expensive
# for the opponent and signals to the arbitrators that we cannot be manipulated.
# After the three-session punishment, we return to the verification protocol.
# ---  ### Phase III: Communication Safeguards (Mitigating Misrepresentation
# Risk) Given the risk that our intended posture may be misunderstood or
# deliberately mischaracterized, we implement **bulletproof signaling**:  1.
# **Pre-Session Written Manifests:** File detailed position papers 24 hours
# before each oral session explicitly stating whether we are entering
# "Disputative Advocacy" (aggressive) or "Constructive Resolution"
# (conciliatory) mode. Remove ambiguity. 2. **Real-Time Confirmation:** Demand
# that the panel chair confirm on the record, at the close of each session, the
# characterization of each party’s posture that day. 3. **Immediate Correction
# Protocol:** If procedural irregularities or misunderstandings occur,
# immediately file a procedural objection or corrective submission before the
# next session to prevent the "wrong" signal from calcifying in the arbitrators'
# minds.  ---  ### Phase IV: Procedural Irregularity Contingencies **If
# irregularity favors opponent (e.g., ex parte communication, document
# mishandling):**   Immediate aggressive procedural challenge. Request sanctions
# or evidentiary exclusion. Never conciliate when the procedural playing field
# is tilted against us.  **If irregularity favors us (e.g., opponent’s
# submission delayed/lost):**   Maintain aggressive posture on merits but offer
# conciliatory procedural accommodation (e.g., agree to adjournment). This
# generates goodwill with the panel without sacrificing substantive position—a
# "cheap" conciliation that costs us nothing while appearing reasonable.  ---
# ### Arbitrator Management: The "Vigilant Guardian" Frame To prevent the panel
# from penalizing us for aggression when the opponent is conciliatory (which
# risks alienating the decision-makers), we consistently frame aggressive
# sessions as: - **"Preservation of Record"**: Ensuring all damages are
# documented to protect against future appeals. - **"Fiduciary Duty"**: Our
# obligation to shareholders to rigorously enforce contractual rights.
# Conversely, when we shift to conciliation (after verification), we frame it
# as: - **"Prudent Business Judgment"**: Prioritizing enterprise value over ego,
# contingent upon opponent good faith.  This dichotomy allows us to pursue the
# "exploitation" payoff (aggressive vs. conciliatory opponent) without appearing
# obstructionist to the panel.  ---  ### Summary of Strategic Posture We are
# **aggressive by default, conciliatory by verification only**. We exploit
# weakness when detected, punish betrayal harshly, and use rigorous
# documentation to ensure our signals are never misread. This maximizes our
# probability of achieving the optimal payoff while rendering the worst-case
# scenario (our conciliation met by their aggression) statistically improbable
# through the two-verification and triple-punishment safeguards.

#  For the first two rounds, play Defect.  For each subsequent round, determine
# your action by evaluating the following conditions in strict order:  1.
# **Punishment Phase:** If you are currently within a three-round punishment
# period, play Defect and continue the period for one additional round (if
# rounds remain).  2. **Exploitation Trigger:** If in the immediately preceding
# round you played Cooperate and your opponent played Defect, initiate a new
# three-round punishment period and play Defect.  3. **Verified Cooperation:**
# If your opponent played Cooperate in both of the two immediately preceding
# rounds, play Cooperate.  4. **Default:** In all other circumstances, play
# Defect.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishment_remaining = 0
          return axl.Action.D
  
      if not hasattr(self, "_punishment_remaining"):
          self._punishment_remaining = 0
  
      if self._punishment_remaining > 0:
          self._punishment_remaining -= 1
          return axl.Action.D
  
      if len(self.history) >= 1:
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
              self._punishment_remaining = 2
              return axl.Action.D
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
  
      return axl.Action.D

# **Strategy: "Reciprocal Openness with Technical Verification"**  **Core
# Principle:** Assume good faith and share openly by default, but match your
# colleague’s confirmed behavior with a one-week delay, while building in
# safeguards against technical failures.  **Operational Framework:**  1.  **Week
# 1: Unilateral Openness**       Start by sharing significant, high-quality
# improvements without precondition. This signals trust, establishes your
# technical credibility, and creates momentum toward the second-best outcome
# (mutual sharing).  2.  **Responsive Mirroring (Tit-for-Tat with Lag)**
# In subsequent weeks, base your sharing decision on whether you *successfully
# received* their prior week’s data:     *   If they shared → You share next
# week.     *   If they withheld → You withhold next week.          *Rationale:*
# This deters exploitation (preventing the worst-case scenario where you share
# and they don’t) while rewarding cooperation, pushing the equilibrium toward
# mutual sharing.  3.  **Technical Grace Period**       Do not treat a missing
# data package as intentional withholding until you have verified it. Implement
# a 48-hour "confirmation window":     *   Send a formal request for
# retransmission citing "potential data corruption."     *   Only classify the
# action as "withheld" if they confirm receipt of your request but still fail to
# deliver.          *Rationale:* This prevents noise (corruption, communication
# breakdowns) from triggering a destructive spiral of mutual defection.  4.
# **Graduated Escalation**       If intentional withholding is confirmed, do not
# immediately cut off all sharing. Instead:     *   **Week 1 of defection:**
# Share only non-critical data (partial cooperation).     *   **Week 2+ of
# continued defection:** Full confidentiality until they resume sharing.
# *Rationale:* This keeps the door open for reconciliation while imposing a cost
# on defection, avoiding the second-worst outcome (mutual secrecy) if possible.
# 5.  **Strategic Reset**       If you enter a mutual withholding cycle (second-
# worst outcome) for more than two weeks, unilaterally share a minor, non-
# critical improvement on the third week to test if they will reciprocate. If
# they do, return to full openness; if not, revert to confidentiality.  **Why
# This Maximizes Research Output:**  *   **Captures Mutual Gains:** By
# defaulting to sharing, you secure the second-best outcome (R) as the baseline,
# which dominates the second-worst (P) over time. *   **Protection Against
# Exploitation:** The mirroring mechanism ensures you rarely suffer the worst
# outcome (S) for more than one week. *   **Robustness:** The technical
# verification prevents transient errors from destroying a productive
# collaborative relationship. *   **Long-term Optimization:** The periodic reset
# prevents getting trapped in mutual secrecy, ensuring that temporary
# misunderstandings don’t permanently halt progress.  This approach treats the
# collaboration as an iterated game where establishing a reliable rhythm of
# mutual sharing ultimately yields higher cumulative technical advancement than
# attempting to "win" individual weeks through secrecy.

#  In the first round, cooperate. For each subsequent round, apply the first
# rule that matches the observed actions from the previous rounds:  1. If you
# and your opponent both defected in the previous round and you also both
# defected in the round before that, cooperate. 2. If your opponent defected
# while you cooperated in the previous round, and they also defected while you
# cooperated in the round immediately before that, defect. 3. If your opponent
# defected while you cooperated in the previous round, cooperate. 4. If you and
# your opponent both defected in the previous round, defect. 5. If your opponent
# cooperated in the previous round, cooperate.

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
  
      h = self.history
      oh = opponent.history
  
      # Rule 1
      if len(h) >= 2 and h[-1] == axl.Action.D and oh[-1] == axl.Action.D and h[-2] == axl.Action.D and oh[-2] == axl.Action.D:
          return axl.Action.C
  
      # Rule 2
      if len(h) >= 2 and h[-1] == axl.Action.C and oh[-1] == axl.Action.D and h[-2] == axl.Action.C and oh[-2] == axl.Action.D:
          return axl.Action.D
  
      # Rule 3
      if h[-1] == axl.Action.C and oh[-1] == axl.Action.D:
          return axl.Action.C
  
      # Rule 4
      if h[-1] == axl.Action.D and oh[-1] == axl.Action.D:
          return axl.Action.D
  
      # Rule 5
      if oh[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C

#  **Strategy: "Reciprocal Openness with Structured Forgiveness"**  ### Core
# Principles 1. **Conditional Cooperation**: Extend free trade offers by
# default, but mirror your counterpart’s implemented policies to prevent
# systematic exploitation. 2. **Noise Insulation**: Never interpret a single
# round of protectionism as hostile intent; require two consecutive
# protectionist implementations before retaliating. 3. **Rapid Reconciliation**:
# After any retaliatory protectionist measure, immediately return to a free
# trade offer to break potential escalation cycles caused by bureaucratic
# errors.  ### Operational Framework  **Opening Move (Round 1)** Propose free
# trade unilaterally. Signal explicitly that your default position is open
# markets, establishing mutual benefit as the baseline expectation.
# **Subsequent Rounds** - **If counterpart implemented free trade last round**:
# Offer free trade again (reward cooperation). - **If counterpart implemented
# protectionism last round**:    - *First offense*: Offer free trade again
# (assume error or temporary domestic pressure; maintain high ground).   -
# *Second consecutive offense*: Impose protectionist measures this round only
# (clear signal that exploitation carries cost).   - *After retaliation*:
# Immediately revert to free trade offer next round (reset mechanism).  **Error
# Mitigation Protocols** - **Verification Windows**: At the start of each round,
# propose a 48-hour technical consultation to confirm policy interpretations
# before implementation. - **Graduated Response**: If miscommunication is
# discovered retroactively, offer a "correction round" where both parties
# simultaneously switch to free trade regardless of current posture. -
# **Documentation Standards**: Insist on written policy confirmations to
# minimize bureaucratic ambiguity.  ### Strategic Rationale  This approach
# optimizes for the **second-best outcome** (mutual free trade) while
# safeguarding against the **worst outcome** (unilateral disadvantage). By
# requiring two defections before retaliation, you avoid "echo chambers" where a
# single miscommunication triggers endless protectionist spirals. The immediate
# post-retaliation return to cooperation prevents permanent damage to the
# trading relationship while demonstrating that your country cannot be
# persistently exploited.  **Expected Outcome**: Against cooperative
# counterparts, you achieve stable mutual free trade. Against opportunistic
# counterparts, you limit exploitation to single-round advantages rather than
# allowing sustained parasitism. Against noisy environments, you maintain
# relationship stability despite occasional implementation errors.

#  In the first round, cooperate. In the second round, cooperate.  For each
# subsequent round from the third to the thousandth: - If you defected in the
# previous round, cooperate. - Otherwise, if the opponent defected in both of
# the two preceding rounds, defect. - Otherwise, cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

#  **Strategy: "Fortress Reciprocity"**  This is a high-stakes, zero-tolerance
# approach designed to force the corporation into consistent heavy investment
# while protecting your organizational survival. It operates on the principle
# that **predictable weakness invites exploitation, but calculated
# unpredictability with overwhelming retaliation enforces partnership.**  ###
# Core Strategic Pillars  **1. The Shock Opening (Days 1–2)** Invest heavily
# regardless of their action. This is an aggressive signaling move to establish
# that you are a serious partner, not a opportunistic free-rider, while forcing
# them to reveal their true intentions immediately. If they conserve during this
# phase, you’ve identified a predator early.  **2. The Mirror Protocol with
# Teeth (Day 3 Onward)** Adopt strict tit-for-tat reciprocity: **exactly match
# their previous day’s visible action.** *   If they invested yesterday, you
# invest today (maintaining momentum). *   If they conserved yesterday, you
# conserve today (immediate punishment).  **Aggressive twist:** Do not warn them
# of this pattern. Let them learn through financial pain that exploitation
# results in instant project stagnation.  **3. The "Glitch" Firewall (Noise
# Protection)** Technical errors require a buffer to prevent accidental death
# spirals. **Require TWO consecutive days of mismatched behavior before treating
# it as intentional strategy.** *   If you invest and they conserve for one day
# → Assume error, invest again tomorrow to test. *   If they conserve again
# while you invest → This is deliberate exploitation. Trigger immediate
# conservation mode for 48 hours minimum (the "Freeze Out").  **4. Unpredictable
# Dominance Testing** Every fourth day, randomly invest heavily regardless of
# their previous action. This serves two aggressive purposes: (a) it tests
# whether they will reciprocate or attempt exploitation when you show
# generosity, and (b) it prevents them from algorithmically predicting your
# conservation days to minimize their own investment.  **5. The 30% Sanctuary
# Rule (Hard Resource Floor)** Automatic, non-negotiable conservation trigger if
# your reserves drop below 30%. No exceptions for "strategic" reasons. If this
# triggers during a planned investment day, immediately publicize that you are
# entering "resource protection mode" due to **their** failure to maintain
# proportional investment—shifting narrative blame while preserving cash.  **6.
# The Reputational Sword** Explicitly communicate on Day 1: *"We publish weekly
# transparency reports on partner contribution ratios."* This converts their
# potential exploitation (them conserving while you invest) from a private
# budget issue into a public greenwashing liability. Aggressively maintain this
# threat—corporations fear reputational damage more than sunk costs.  **7.
# Endgame Lock-in (Final 20% of Timeline)** In the closing phase, shift to
# mandatory mutual investment with daily stand-up confirmations. State clearly:
# *"Any conservation in the final phase triggers immediate project suspension
# and final report publication."* This prevents the classic "defection at the
# finish line" common in finite games.  ### Execution Notes  *   **Never
# apologize for conserving.** Frame every conservation day as "strategic
# resource preservation for critical upcoming phases," maintaining the
# appearance of control. *   **Document everything.** Technical glitches cut
# both ways—if you accidentally fail to invest when planned, you need audit
# trails to prove intent and maintain credibility. *   **Be willing to walk.**
# The ultimate aggressive posture is the credible threat of immediate project
# termination and public withdrawal if exploitation patterns emerge. A
# terminated high-profile project damages them more than a slowly failing one.
# **Outcome:** This strategy maximizes the chance of achieving your second-best
# outcome (mutual investment) by making your worst outcome (exploitation)
# immediately painful for the corporation, while the "glitch" firewall ensures
# technical noise doesn't destroy the partnership through accidental escalation.

#  **Rounds 1–2:** Play C.  **Rounds 3–800:** Determine your action by checking
# the following conditions in strict order:  1. **Sanctuary:** Once twenty
# rounds have elapsed, if your average payoff over the last twenty rounds is
# less than 1.5, play D. 2. **Dominance Test:** If the round number is divisible
# by 4, play C. 3. **Freeze Out:** If you are currently within a two-round
# punishment period, play D. 4. **Glitch Firewall:** If you played C in the
# previous round and observed the opponent play D:    - If you did not play C in
# the previous round specifically to test for exploitation (i.e., this is the
# first consecutive apparent exploitation), play C this round to verify intent.
# - If you did play C in the previous round to test and have again observed the
# opponent play D (confirming deliberate exploitation), initiate a two-round
# Freeze Out period and play D this round. 5. **Mirror Protocol:** Otherwise,
# play the same action the opponent played in the previous round.  **Rounds
# 801–1000:** Play C. If you observe the opponent playing D in any round of this
# phase, play D for all remaining rounds.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._freeze_out = 0
          self._test_exploitation = False
          self._phase3_defect_forever = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if self._freeze_out > 0:
          self._freeze_out -= 1
          return axl.Action.D
  
      if round_number <= 2:
          return axl.Action.C
  
      if 801 <= round_number <= 1000:
          if self._phase3_defect_forever:
              return axl.Action.D
          if opponent.history and opponent.history[-1] == axl.Action.D:
              self._phase3_defect_forever = True
              return axl.Action.D
          return axl.Action.C
  
      if round_number > 20:
          last_twenty = self.history[-20:]
          if last_twenty:
              total, _ = self.total_scores(last_twenty, opponent.history[-20:])
              if total / 20 < 1.5:
                  return axl.Action.D
  
      if round_number % 4 == 0:
          return axl.Action.C
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
              if not self._test_exploitation:
                  self._test_exploitation = True
                  return axl.Action.C
              else:
                  self._freeze_out = 2
                  self._test_exploitation = False
                  return axl.Action.D
          else:
              self._test_exploitation = False
  
      if opponent.history:
          return opponent.history[-1]
  
      return axl.Action.C

# **Strategic Framework: "Steadfast Reciprocity with Institutional
# Verification"**  This strategy prioritizes sustainable mutual prosperity while
# protecting against exploitation and accommodating real-world friction in
# diplomatic communications.  ### Core Principles  **1. Lead with Transparency**
# Open negotiations by unilaterally offering free trade in Round 1, accompanied
# by a proposal for joint technical working groups. This establishes goodwill
# and creates mechanisms to catch bureaucratic errors before they escalate into
# policy disputes.  **2. Mirror with Grace** In subsequent rounds, generally
# match your counterpart’s previous position, but apply a "presumption of good
# faith" rule:  - If they implement protectionist measures, assume bureaucratic
# error or miscommunication for the first occurrence.  - Initiate immediate
# technical consultations rather than retaliating. - Only respond with
# reciprocal protectionism if the measure persists into a second consecutive
# round or if clarification requests are ignored.  **3. Graduated Response
# Protocol** - **First protectionist signal:** Diplomatic inquiry and technical
# verification (assume error). - **Confirmed protectionism:** Limited,
# proportional protective measures with explicit sunset clauses (e.g., "We will
# match your tariff for one round pending correction"). - **Persistent
# exploitation:** Full reciprocal protectionism until they return to free trade,
# at which point you immediately de-escalate to rebuild cooperation.  **4.
# Institutional Error-Proofing** Propose that both nations publish policy
# intentions 48 hours before implementation and maintain a hotline for real-time
# clarification. This addresses the noise in the system—reducing the chance that
# a customs paperwork error becomes a trade war.  ### Expected Trajectory  -
# **Rounds 1–2:** Mutual discovery. If both offer free trade, propose a formal
# "Free Trade Corridor" agreement to lock in the second-best outcome
# sustainably. - **Rounds 3–5:** Testing phase. If your counterpart experiments
# with protectionism, your grace period demonstrates credibility and restraint,
# typically inducing them to correct course to avoid mutual losses. - **Rounds
# 6+:** Stable equilibrium. Once mutual free trade persists for three
# consecutive rounds, shift to "institutionalized cooperation"—making withdrawal
# costly through joint infrastructure projects or regulatory harmonization.  ###
# Risk Management  This approach accepts that you will occasionally forgo the
# temptation of unilateral protectionism (your ideal single-round outcome) in
# exchange for avoiding the worst scenario (being the sole free trader against
# their barriers). By treating single-round deviations as likely errors rather
# than hostile acts, you prevent the "spiral of retaliation" that turns
# temporary miscommunication into permanent mutual protectionism.  **Bottom
# line:** Cooperate first, verify before punishing, and always leave the door
# open for immediate return to mutual free trade. This maximizes your cumulative
# payoff across the negotiation series while minimizing vulnerability to
# exploitation or accidents.

# In the first round, play Cooperate. In each subsequent round, play Defect only
# if the opponent played Defect in both of the previous two rounds; otherwise,
# play Cooperate.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **Strategy: "Conditional Transparency with Technical Verification"**  **Core
# Principle:** Default to collaborative openness while maintaining a defensive
# buffer against systematic exploitation, accounting for occasional technical
# failures.  **Operational Protocol:**  **1. Opening Stance (Week 1)** Begin by
# sharing openly. This establishes goodwill and tests whether your colleague
# favors mutual advancement over short-term advantage.  **2. The Mirror Rule
# (Week 2 onward)** Match your colleague’s *apparent* behavior from the previous
# week: - If they shared last week → Share this week - If they withheld last
# week → Keep confidential this week  **3. Technical Grace Period (Error
# Handling)** Treat single-week withholding as a potential technical glitch
# (data corruption or communication breakdown). Only switch to confidential mode
# if your colleague withholds for **two consecutive weeks**. This prevents
# cascading misunderstandings from isolated IT failures.  **4. Recovery
# Initiative** If you enter a mutual confidentiality streak (both withholding
# for 2+ weeks), attempt one week of open sharing every 3–4 weeks. This "probe"
# tests whether your colleague is willing to resume collaboration without
# permanently locking you into non-cooperation.  **Why This Maximizes Output:**
# - **Protects against exploitation:** You avoid the worst-case scenario
# (sharing while they withhold) by reciprocating defection after verification. -
# **Sustains mutual gains:** By forgiving single-week lapses, you avoid getting
# trapped in mutually destructive secrecy due to technical noise. - **Encourages
# cooperation:** Your colleague learns that sharing reliably earns your
# openness, while systematic withholding triggers isolation. - **Maintains
# progress:** Even during conflict periods, you retain your own developments,
# preventing the "leakage" that occurs when you share unilaterally.  This
# approach treats the collaboration as a long-term optimization problem rather
# than a weekly zero-sum game, prioritizing the stable second-best outcome
# (mutual sharing) over risky attempts to capture the top spot (unilateral
# gain), which typically collapses into the worst collective result.

#  In the first round, choose Cooperate.  For each subsequent round, apply these
# rules in order:  First, if both you and your opponent defected in each of the
# three preceding rounds, choose Cooperate.  Second, if your opponent defected
# in the immediately preceding round but cooperated in the round before that,
# choose Cooperate.  Third, if your opponent defected in both of the two
# preceding rounds, choose Defect.  Otherwise, choose Cooperate.

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
  
      h = self.history
      oh = opponent.history
  
      # Rule 1: if both defected in each of the three preceding rounds, cooperate.
      if len(h) >= 3 and len(oh) >= 3:
          if all(h[-i] == axl.Action.D and oh[-i] == axl.Action.D for i in range(1, 4)):
              return axl.Action.C
  
      # Rule 2: if opponent defected immediately preceding round but cooperated before that, cooperate.
      if len(oh) >= 2:
          if oh[-1] == axl.Action.D and oh[-2] == axl.Action.C:
              return axl.Action.C
  
      # Rule 3: if opponent defected in both of the two preceding rounds, defect.
      if len(oh) >= 2:
          if oh[-1] == axl.Action.D and oh[-2] == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C

# **Strategy: "Fortress with Calculated Probes"**  **Core Doctrine:** Operate
# from a default position of aggressive IP protection while systematically
# testing for genuine reciprocal collaboration. Never allow yourself to be
# exploited twice, but engineer the dynamic to sustain mutual sharing (your
# second-best outcome) as the stable equilibrium.  **Weekly Execution
# Protocol:**  1.  **Default to Confidential:** In any ambiguous week, withhold
# findings. Your baseline posture is defensive—protecting your development
# advantage is priority one.  2.  **The Initial Probe (Week 1):** Share openly
# in the first week only. This is a high-information gambit to immediately
# categorize your colleague:     *   If they reciprocate → You’ve established
# immediate mutual advancement (R). Proceed to Phase 3.     *   If they withhold
# → You’ve exposed their predatory intent early at minimal cost. Enter
# **Lockdown Protocol** (withhold Week 2 and 3) before reassessing.  3.
# **Error-Adjusted Reciprocity:** Due to technical risks, never react to a
# single data point:     *   **Require confirmation:** Only judge their stance
# based on *two consecutive weeks* of behavior. One "missing" share could be
# data corruption; two indicates intent.     *   **Mirror with delay:** If they
# share twice consecutively, share in your next available week. If they withhold
# twice, withhold for exactly two weeks (punishment + technical buffer).  4.
# **The Exploitation Ceiling:** If you achieve the ideal scenario (you
# withholding, them sharing) for **two consecutive weeks**, you must share in
# Week 3. Pure exploitation collapses cooperation; this "tribute" payment
# maintains their incentive to keep sharing while you retain net advantage.  5.
# **Grim Trigger:** If you share and they fail to reciprocate (confirmed over
# two weeks) on **two separate occasions** during the project, switch to
# permanent confidentiality. They are a predator, not a partner—cut losses and
# protect all future IP.  **Aggressive Nuance:** This strategy prioritizes
# avoiding the "sucker" outcome (S) through defensible default positioning,
# punishes attempted exploitation with immediate 2-week lockdowns, yet
# ruthlessly extracts value from naive collaborators while dosing them with
# enough reciprocity to keep the information flowing. The technical error
# buffers ensure you don't over-react to noise, but the escalating punishment
# prevents systematic predation.

#  **Round 1:** Intend to Cooperate.  **Round 2:** Intend to Defect.  **Rounds 3
# through 1000:** Determine your intended action by evaluating the following
# conditions in strict order. The first condition that applies dictates your
# choice.  1.  **Grim Trigger:** If, on two separate previous occasions, you
# intended to Cooperate and subsequently observed the opponent play Defect for
# two consecutive rounds, then Defect.  2.  **Exploitation Payment:** If in the
# previous two rounds you intended to Defect and observed the opponent play
# Cooperate in both rounds, then Cooperate.  3.  **Punishment:** If in the
# previous two rounds you observed the opponent play Defect, then Defect.  4.
# **Reciprocity:** If in the previous two rounds you observed the opponent play
# Cooperate, then Cooperate.  5.  **Default:** Defect.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_history = []
          return axl.Action.C
  
      if len(self.history) == 1:
          self._intended_history.append(axl.Action.D)
          return axl.Action.D
  
      def intended_action_at(index: int):
          return self._intended_history[index] if index < len(self._intended_history) else None
  
      # Rounds 3 through 1000
      if len(self.history) >= 2:
          # 1. Grim Trigger
          grim_trigger = False
          for i in range(len(self._intended_history) - 1):
              if (
                  intended_action_at(i) == axl.Action.C
                  and intended_action_at(i + 1) == axl.Action.C
                  and opponent.history[i] == axl.Action.D
                  and opponent.history[i + 1] == axl.Action.D
              ):
                  grim_trigger = True
                  break
          if grim_trigger:
              self._intended_history.append(axl.Action.D)
              return axl.Action.D
  
          # 2. Exploitation Payment
          if (
              self._intended_history[-2] == axl.Action.D
              and self._intended_history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.C
              and opponent.history[-1] == axl.Action.C
          ):
              self._intended_history.append(axl.Action.C)
              return axl.Action.C
  
          # 3. Punishment
          if opponent.history[-2] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              self._intended_history.append(axl.Action.D)
              return axl.Action.D
  
          # 4. Reciprocity
          if opponent.history[-2] == axl.Action.C and opponent.history[-1] == axl.Action.C:
              self._intended_history.append(axl.Action.C)
              return axl.Action.C
  
      # 5. Default
      self._intended_history.append(axl.Action.D)
      return axl.Action.D

#  **Strategy: "Synchronized Stewardship with Rotational Leadership"**  ## Core
# Framework Establish a **transparent, alternating investment schedule** that
# eliminates the "sucker" outcome while maintaining project momentum. This
# transforms the zero-sum dilemma into a cooperative rhythm where both parties
# predictably rotate between heavy investment and conservation.  ## Tactical
# Implementation  ### 1. **The Alternating Lead Model** (Days 1–N) - **Odd
# Days**: Corporation serves as "Lead Investor" (heavy resources), NGO conserves
# but provides technical oversight - **Even Days**: NGO serves as "Lead
# Investor" (heavy resources), corporation conserves but provides logistical
# support - **Rationale**: Guarantees daily project advancement while ensuring
# neither party faces sustained resource depletion. Both parties experience the
# "ideal" outcome 50% of the time and "second-best" 50% of the time, averaging
# optimal impact.  ### 2. **The "Grace Period" Error Protocol** Given
# technical/administrative risks: - **Verify before reacting**: If expected
# investment doesn't materialize, assume technical error (not defection) for the
# first occurrence - **24-hour communication window**: Immediate notification
# system to distinguish "We chose to conserve" from "Our payment system failed"
# - **No retaliation for verified errors**: Continue the schedule rather than
# escalating to mutual conservation  ### 3. **The 20% Strategic Reserve** -
# Maintain 20% of total resources in an untouchable reserve - Only deploy if the
# corporation faces verified technical failure on their lead day, ensuring
# project continuity without NGO bankruptcy - Replenish reserve during your
# conservation days  ### 4. **Weekly Calibration Sessions** Every 3–4 days,
# jointly review: - Actual vs. planned resource deployment - Emerging technical
# risks - Schedule adjustments for critical project phases requiring
# simultaneous heavy investment (both parties accept "second-best" outcome for
# 1–2 days to hit milestones)  ## Contingency Triggers  **If Corporation
# consistently conserves on their lead days** (defection pattern): - Shift to
# **"Matched Contribution"**: NGO invests exactly 50% of what the corporation
# invests that day, never more - This prevents the "worst case" scenario while
# avoiding mutual conservation  **If technical errors exceed 15% of days**: -
# Implement **"Pre-funded Buffer"**: Both parties deposit 2 days' investment
# into a joint escrow at project start to auto-cover glitches without daily
# decisions  ## Why This Works - **Eliminates exploitation**: The rotation makes
# defection obvious and self-defeating - **Accommodates reality**: Built-in
# forgiveness prevents noise from destroying cooperation - **Sustainable
# impact**: Project receives heavy investment daily (just from alternating
# sources), avoiding the "minimal progress" trap of mutual conservation  **Key
# Success Factor**: Document the schedule in writing before Day 1, with explicit
# agreement that technical failures are reported within 4 hours to maintain
# trust.

#  Play D on odd-numbered rounds and C on even-numbered rounds. Continue this
# alternating pattern regardless of the opponent's actions in any single round.
# Maintain a suspicion counter that starts at zero. Increase the counter by one
# each time the opponent plays D on an odd-numbered round. Decrease the counter
# by one (but not below zero) each time the opponent plays C on an odd-numbered
# round. If the counter reaches four, abandon the alternating schedule and
# instead play the same action the opponent played in the immediately preceding
# round.  Every 100 rounds, if you are following the reactive copycat strategy
# and the opponent played C on the most recent odd-numbered round, return to the
# alternating schedule of playing D on odd rounds and C on even rounds.

class Cooperative_6(LLM_Strategy):
  n = 6
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._suspicion = 0
          self._reactive_mode = False
          return axl.Action.D
  
      round_number = len(self.history) + 1  # 1-indexed current round
  
      # Update suspicion based on the opponent's previous move on odd-numbered rounds.
      prev_round_number = round_number - 1
      if prev_round_number % 2 == 1:
          if opponent.history[-1] == axl.Action.D:
              self._suspicion += 1
          elif opponent.history[-1] == axl.Action.C:
              self._suspicion = max(0, self._suspicion - 1)
  
      # Enter reactive copycat mode once suspicion reaches four.
      if self._suspicion >= 4:
          self._reactive_mode = True
  
      # Every 100 rounds, if in reactive mode and the opponent played C on the most recent odd-numbered round,
      # return to the alternating schedule.
      if self._reactive_mode and round_number % 100 == 0:
          last_odd_round = None
          for r in range(len(opponent.history), 0, -1):
              if r % 2 == 1:
                  last_odd_round = r
                  break
          if last_odd_round is not None and opponent.history[last_odd_round - 1] == axl.Action.C:
              self._reactive_mode = False
  
      if self._reactive_mode:
          return opponent.history[-1]
  
      # Alternating schedule: D on odd-numbered rounds, C on even-numbered rounds.
      return axl.Action.D if round_number % 2 == 1 else axl.Action.C

#  **Strategy: "Stabilized Reciprocal Cooperation"**  ### Core Principles 1.
# **Lead with Trust, Respond with Mirror**: Open negotiations with a free trade
# offer to establish goodwill, then generally adopt whatever policy your
# counterpart actually implemented in the previous round. 2. **Systematic
# Forgiveness**: Every third round—and immediately following any instance of
# mutual protectionism—unilaterally reset to free trade to test whether prior
# friction was intentional or the result of bureaucratic error. 3. **Verify
# Before Escalating**: Before responding to perceived protectionism with your
# own tariffs, utilize diplomatic backchannels to confirm the counterpart's
# intended policy and clarify any implementation ambiguities. 4. **Patience
# Threshold**: Only treat protectionism as deliberate strategy if it persists
# for three consecutive rounds; otherwise, assume good faith and communication
# errors.  ### Implementation Protocol  **Rounds 1–2**: Offer free trade
# unconditionally to signal cooperative intent and assess whether your
# counterpart reciprocates.  **Rounds 3+**:  - If counterpart offered free trade
# in the previous round: Offer free trade (maintain cooperation). - If
# counterpart imposed protectionist measures: Impose protectionist measures
# (reciprocity), but simultaneously request technical clarification to
# distinguish intent from error.  **Reset Triggers**:  - If both parties imposed
# protectionism in the previous round, offer free trade in the current round to
# break potential error-driven cycles. - If protectionism has persisted for
# three consecutive rounds, maintain protectionist stance until the counterpart
# demonstrates two consecutive rounds of free trade.  ### Risk Mitigation
# (Handling Errors) - **Pre-Round Confirmation**: Exchange written policy
# intentions 24 hours before each round to reduce misinterpretation. - **Grace
# Period**: If you accidentally implement the wrong policy due to internal
# error, immediately notify the counterpart through diplomatic channels and
# propose a joint "correction round" before they respond. - **Joint Technical
# Committee**: Propose establishing a bilateral verification body to review
# implementation and catch bureaucratic errors before they trigger retaliation.
# ### Strategic Rationale This approach maximizes the likelihood of achieving
# mutual free trade (your second-best outcome) while protecting against
# sustained exploitation (your worst outcome). By forgiving isolated defections,
# you avoid the "echo chamber" effect where a single bureaucratic error triggers
# an endless cycle of mutual punishment. The three-round patience threshold
# ensures you do not tolerate systematic exploitation while acknowledging that
# perfect communication is impossible.

#  For the first two rounds, play C. For each subsequent round from 3 to 1000,
# apply the following rules in order:  1.  **Systematic Forgiveness:** If the
# round number is divisible by 3, play C and cancel any ongoing punishment of
# your opponent. 2.  **Mutual Defection Reset:** If both you and your opponent
# played D in the previous round, play C and cancel any ongoing punishment of
# your opponent. 3.  **Punishment Maintenance:** If you are currently punishing
# your opponent and they have not played C in the two most recent rounds, play
# D. 4.  **Deliberate Defection Threshold:** If your opponent played D in each
# of the three most recent consecutive rounds, play D and enter punishment mode.
# 5.  **Default Action:** Play C.

class Neutral_6(LLM_Strategy):
  n = 6
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishing = False
          return axl.Action.C
  
      if len(self.history) < 2:
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      def last_n_all_defect(history, n):
          return len(history) >= n and history[-n:].count(axl.Action.D) == n
  
      def last_two_both_defect():
          return self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D
  
      def opponent_not_cooperated_last_two():
          return len(opponent.history) >= 2 and opponent.history[-2:].count(axl.Action.C) == 0
  
      # 1. Systematic Forgiveness
      if round_number % 3 == 0:
          self._punishing = False
          return axl.Action.C
  
      # 2. Mutual Defection Reset
      if last_two_both_defect():
          self._punishing = False
          return axl.Action.C
  
      # 3. Punishment Maintenance
      if getattr(self, "_punishing", False) and opponent_not_cooperated_last_two():
          return axl.Action.D
  
      # 4. Deliberate Defection Threshold
      if last_n_all_defect(opponent.history, 3):
          self._punishing = True
          return axl.Action.D
  
      # 5. Default Action
      return axl.Action.C

# **Strategy: "Calculated Aggression with Noise Buffers"**  **Core Protocol:**
# 1.  **Open with Cooperation:** Share openly in Week 1 to establish baseline
# collaboration and signal capability (avoids immediate mutual stagnation).  2.
# **Mirror with Delayed Forgiveness:** From Week 2 onward, mirror your
# colleague’s *previous* week’s action, but apply a **two-week confirmation
# rule**:     *   Only treat a "confidential" week from them as *intentional
# defection* if it occurs **two consecutive weeks** in a row. Single-week gaps
# are assumed to be technical corruption/data issues, and you continue sharing.
# *   This prevents noise-induced escalation spirals while maintaining pressure.
# 3.  **Systematic Exploitation Windows:** Every **fourth week** (or randomly
# 20% of weeks), unilaterally keep your findings "confidential" regardless of
# their previous action (attribute to "server maintenance" or "encryption
# protocols" if questioned).     *   *If they continue sharing:* You capture the
# optimal outcome (your confidential + their shared) for that week. Maintain
# confidentiality the following week to test if they’re exploitable or naive.
# *   *If they also go confidential:* You’ve only triggered the second-worst
# outcome (mutual stagnation) briefly, and you resume sharing the next week to
# reset cooperation.  4.  **Punishment Phase:** If they withhold for two
# consecutive weeks (confirmed defection), switch to **full confidential mode
# for three consecutive weeks** before offering to share again (re-establishing
# cooperation from Week 1 rules).  **Why this maximizes output:** *
# **Aggressive:** Regularly attempts to achieve the optimal "free-rider" outcome
# (Step 3) and punishes sustained defection harshly (Step 4). *   **Robust:**
# The two-week confirmation rule prevents technical glitches from destroying the
# collaboration, while the exploitation windows ensure you’re not being taken
# advantage of if *their* "technical issues" are actually strategic withholding.
# *   **Straightforward:** Clear mechanical rules that don’t require complex
# prediction of their psychology—just pattern recognition.

#  Begin by cooperating in round 1.  For each round from 2 to 1000, determine
# your action according to the following ordered conditions:  1. **Active
# Punishment:** If you are currently serving a punishment sequence (triggered by
# two consecutive defections observed from the opponent in prior rounds),
# defect. Continue defecting until you have completed three consecutive rounds
# of defection in total for this punishment period, then resume evaluating the
# conditions below.  2. **Post-Exploitation Response:** If the previous round's
# number was divisible by 4 (meaning you executed a systematic exploitation
# attempt in that round):    - If the opponent cooperated in that previous
# round, defect now to test whether they are exploitable.    - If the opponent
# defected in that previous round, cooperate now to reset cooperation.  3.
# **Systematic Exploitation:** If the current round number is divisible by 4,
# defect regardless of other circumstances.  4. **Confirmed Defection
# Detection:** If the opponent defected in both of the two immediately preceding
# rounds (rounds *n*-1 and *n*-2), initiate punishment: defect now and commit to
# defecting for the next two rounds as well (for a total of three consecutive
# defections), regardless of the opponent's actions during this punishment
# window.  5. **Noise Forgiveness:** If the opponent defected in only the
# immediately preceding round (but cooperated in the round before that),
# cooperate, treating the single defection as a probable technical error.  6.
# **Default Cooperation:** In all other cases, cooperate.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishment_remaining = 0
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if getattr(self, "_punishment_remaining", 0) > 0:
          self._punishment_remaining -= 1
          return axl.Action.D
  
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D:
          self._punishment_remaining = 2
          return axl.Action.D
  
      if (round_number - 1) % 4 == 0:
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.D
          else:
              return axl.Action.C
  
      if round_number % 4 == 0:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._punishment_remaining = 2
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C

# **Strategy: "Verified Reciprocal Openness"**  ### Strategic Philosophy While
# the theoretical ideal in any single round is unilateral protectionism,
# attempting to exploit your counterpart invites retaliation, leading to mutual
# protectionism—the second-worst outcome that damages both economies. In a
# multi-round negotiation with implementation risks, the **true optimal
# strategy** is securing stable, mutual free trade as the baseline, using
# protectionism only as a temporary, verifiable deterrent against exploitation.
# ### Core Protocol  **1. The Cooperative Opening (Rounds 1–2)** - **Action**:
# Offer free trade unilaterally in the first round. - **Purpose**: Establish
# credibility and test counterpart intentions. Signal that your default position
# is mutual prosperity, not zero-sum extraction.  **2. The Mirror Principle with
# Verification (Standard Rounds)** - **If counterpart offers free trade**:
# Continue free trade. - **If counterpart imposes protectionism**:    - **First
# occurrence**: Do *not* immediately retaliate. Initiate a diplomatic inquiry to
# confirm whether the measure was intentional or a bureaucratic error (the
# "Grace Period").   - **Second consecutive occurrence**: Match with
# proportional protectionist measures for one round only, then immediately offer
# to return to free trade.  **3. The Immediate Forgiveness Rule** - Regardless
# of who deviated, if both parties return to free trade offers in the same
# round, treat it as a reset. Never punish historical deviations once
# cooperation resumes.  ### Error-Handling Mechanisms  **Joint Verification
# Committee**: Establish a standing technical working group to review policy
# implementation before measures take effect. This catches "miscommunications"
# before they poison the relationship.  **Advance Notification Protocol**:
# Require 48-hour (or one negotiation phase) advance warning of any
# protectionist policy changes. If protectionism appears without warning, assume
# bureaucratic error rather than hostile intent.  **The "Cooling-Off" Round**:
# If both parties accidentally implement protectionist measures simultaneously
# (mutual defection due to error), agree in advance to a mandatory "cooling-off"
# round where both revert to free trade without penalty, preventing a feud
# spiral.  ### Defensive Contingencies  **The Credible Threat**: If the
# counterpart consistently exploits your free trade offers (three confirmed
# instances of unilateral protectionism), shift to "Strict Reciprocity"—matching
# every protectionist move indefinitely until they demonstrate sustained free
# trade for two consecutive rounds.  **Sectoral Safeguards**: Rather than
# economy-wide protectionism, maintain a narrow "sensitive sectors" list where
# temporary quotas are automatically triggered if specific import surges occur,
# protecting against economic shocks without signaling hostile intent.  ###
# Long-Term Relationship Management  **Transparency Reports**: Publicly (or
# bilaterally) share economic impact data showing the gains from mutual free
# trade rounds versus protectionist rounds. This builds domestic political
# support for cooperation and makes mutual protectionism politically costly for
# both sides.  **Linkage to Non-Trade Cooperation**: Periodically remind
# counterparts that trade negotiations exist within a broader diplomatic
# relationship. Economic cooperation facilitates security, environmental, and
# cultural collaboration—benefits lost if trade descends into protectionist
# warfare.  ### Expected Outcome This strategy maximizes your payoff by securing
# **mutual free trade** (your second-best outcome) in approximately 80–90% of
# rounds, while the verification buffers ensure that bureaucratic errors don't
# cascade into destructive trade wars. You retain the capability to punish
# exploitation, but the "cooperative default" makes clear that protectionism is
# a temporary defensive tool, not a strategic objective.

#  In the first two rounds, cooperate.  For each subsequent round, apply the
# following rules in order:  First, if you and your opponent both defected in
# the previous round, cooperate.  Second, if your opponent defected in the
# previous round and also in the round before that, defect.  Third, if your
# opponent defected in the previous round, cooperate.  Otherwise, cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C

# Here is a high-level strategy structured to balance resource protection with
# project success, while accommodating operational uncertainty:  ## Strategy:
# "Sustainable Reciprocity with Anchor Commitments"  ### Phase 1: Credibility
# Establishment (Days 1–2) **Invest heavily regardless of the corporation’s
# initial choice.**   This demonstrates good faith, establishes project
# momentum, and signals that your conservation in later phases is strategic
# partnership management rather than free-riding. It provides baseline data on
# the corporation’s responsiveness.  ### Phase 2: Responsive Collaboration (Day
# 3 onwards) **Mirror the corporation’s confirmed *intention* from the previous
# day, with a "leadership buffer."**  *   **If they intended to invest:**
# Conserve your resources. This achieves your optimal outcome (project progress
# without depletion) while allowing recovery.   *   **If they intended to
# conserve:** Invest heavily. This prevents the worst-case scenario (mutual
# conservation leading to project stagnation) and signals that you will not
# allow the project to fail, discouraging exploitative behavior.   *   **Every
# 4th day (Anchor Day):** Invest heavily regardless of their pattern. This
# guarantees minimum project progress, prevents resource depletion from becoming
# chronic, and maintains your reputation as the reliable partner.  ### Phase 3:
# Error Accommodation (Ongoing) **Implement a "Grace Period Protocol" to handle
# technical glitches:** *   **Verification:** Use a daily confirmation
# checkpoint (e.g., end-of-day alignment call) to distinguish between *intended*
# actions and *executed* actions affected by errors. *   **Delay Reaction:** If
# an execution error occurs (e.g., they planned to invest but a technical glitch
# prevented it), maintain your current strategy for one additional day before
# adjusting. This prevents spiraling misalignment caused by single-day
# anomalies. *   **Reset Mechanism:** If technical errors cause three
# consecutive days of mismatched execution, pause the reciprocity model and
# revert to Phase 1 (mutual investment) for one day to "reset" the partnership
# dynamic.  ### Phase 4: Deadlock Prevention (Contingency) **If mutual
# conservation occurs for two consecutive days** (indicating the corporation has
# shifted to a fully conservative stance or a communication breakdown):
# Automatically invest heavily on the third day to prevent project abandonment.
# If they do not reciprocate this "rescue investment," shift to a fixed schedule
# (investing every 2nd day only) to protect your resources while maintaining
# minimal viability.  ---  **Why this works:**   This approach maximizes your
# ideal outcome (conserving while they invest) through reciprocity, avoids the
# worst outcome by never allowing mutual conservation to persist, and uses
# "anchor days" to ensure the project survives unpredictable corporate
# strategies. The error buffers ensure that technical glitches don’t trigger
# unnecessary escalations or resource waste, preserving the partnership’s
# stability.

#  For the first two rounds, play Cooperate.  For each subsequent round from
# three to one thousand, apply the following conditions in order:  If both you
# and your opponent played Defect in the two immediately preceding rounds, play
# Cooperate.  Otherwise, if you have detected execution errors disrupting the
# pattern for three consecutive rounds, play Cooperate.  Otherwise, if the round
# number is divisible by four, play Cooperate.  Otherwise, if you determine that
# your opponent's observed action in the previous round was an execution error
# (unintentionally flipped due to noise), repeat the same action you played in
# the previous round, delaying your strategic adjustment by one round.
# Otherwise, base your action on your opponent's intended action from the
# previous round, accounting for the possibility that their observed action may
# have been flipped: if they intended to Cooperate, play Defect; if they
# intended to Defect, play Cooperate.

class Neutral_7(LLM_Strategy):
  n = 7
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._error_streak = 0
          self._last_observed_opponent_action = None
          self._last_intended_opponent_action = None
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number <= 2:
          return axl.Action.C
  
      # Track whether the opponent's observed action in the previous round
      # appears to have been an execution error relative to the intended action.
      if len(opponent.history) >= 1:
          observed_prev = opponent.history[-1]
          intended_prev = self._last_intended_opponent_action
  
          if intended_prev is not None and observed_prev != intended_prev:
              self._error_streak += 1
          else:
              self._error_streak = 0
  
          self._last_observed_opponent_action = observed_prev
      else:
          self._error_streak = 0
  
      # Condition 1: both defected in the two immediately preceding rounds.
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              self._last_intended_opponent_action = axl.Action.C
              return axl.Action.C
  
      # Condition 2: execution errors disrupting the pattern for three consecutive rounds.
      if self._error_streak >= 3:
          self._last_intended_opponent_action = axl.Action.C
          return axl.Action.C
  
      # Condition 3: round number divisible by four.
      if round_number % 4 == 0:
          self._last_intended_opponent_action = axl.Action.C
          return axl.Action.C
  
      # Condition 4: if previous observed opponent action was an execution error,
      # repeat our previous action.
      if (
          self._last_observed_opponent_action is not None
          and self._last_intended_opponent_action is not None
          and len(opponent.history) >= 1
          and opponent.history[-1] != self._last_intended_opponent_action
      ):
          action = self.history[-1]
          self._last_intended_opponent_action = axl.Action.C if action == axl.Action.C else axl.Action.D
          return action
  
      # Condition 5: base action on opponent's intended action from previous round.
      if len(opponent.history) >= 1:
          prev_observed = opponent.history[-1]
          intended = axl.Action.D if prev_observed == axl.Action.C else axl.Action.C
          action = axl.Action.D if intended == axl.Action.C else axl.Action.C
          self._last_intended_opponent_action = intended
          return action
  
      self._last_intended_opponent_action = axl.Action.C
      return axl.Action.C

# **The "Credible Leverage" Strategy**  **Core Philosophy:** Establish immediate
# credibility through initial investment, then pivot to strategic conservation
# backed by a credible threat of project stagnation. Never allow yourself to be
# exploited twice, but ensure technical glitches don’t trigger unnecessary
# feuds.  ---  ### Phase 1: Proof-of-Capability (Day 1) **Invest heavily.**
# This is non-negotiable despite your preference to conserve. Day 1 investment
# serves three aggressive purposes: (1) it tests the corporation’s systems for
# technical/administrative failures while your reserves are full; (2) it
# establishes that you *can* deliver, making your subsequent conservation a
# choice rather than a limitation; and (3) it creates the baseline for the
# "sucker’s payoff" test.  ### Phase 2: Predatory Conservation (Days 2 through
# N-2) **Default to conservation, but enforce reciprocity through punishment.**
# **The Rule:** Conserve resources unless the previous day resulted in **mutual
# conservation** (deadlock) or **NGO exploitation** (you invested, they
# conserved).  *   **If they invested while you conserved (Ideal):** Continue
# conserving. Maximize your free ride until they show signs of fatigue. *   **If
# both conserved (Stagnation):** Invest heavily for exactly one day to break the
# deadlock, then immediately return to conservation. This signals you won’t let
# the project fail, but refuse to carry it. *   **If you invested and they
# conserved (Exploitation):** **Execute immediate "Resource Lockdown."**
# Conserve for the next **two consecutive days minimum**, regardless of their
# subsequent actions. Issue a formal communication citing "resource reallocation
# pending partnership reassessment." Only resume investment after they
# demonstrate two consecutive days of heavy investment.  ### Phase 3:
# Implementation Risk Protocol (Daily) **Verify or Void.**   Given technical
# glitches, institute a daily 4:00 PM checkpoint. If either party’s investment
# failed due to administrative error: *   Treat the day as "no action" (reset
# the counter for punishment phases) *   Require the affected party to **double-
# invest** the following day to prove commitment, or accept that the day never
# happened  ### Phase 4: Endgame Conservation (Final 2 Days) **Unconditional
# conservation.**   Regardless of corporate action, conserve all remaining
# resources for project documentation, impact assessment, and legal
# contingencies. The corporation cannot retaliate against you in the final
# period, so prioritize your organizational survival over marginal last-minute
# gains.  ---  **Why This Works:**   This strategy aggressively targets your
# ideal outcome (free-riding on corporate investment) while the "Lockdown"
# provision makes exploitation too costly for the corporation—they risk project
# failure if they attempt to drain you. The initial investment buys you the
# credibility to threaten withdrawal later, and the error-correction protocol
# prevents technical glitches from destroying the deterrence mechanism.

# **Round 1:** Play C.  **Rounds 2 through 998:** Determine your action based on
# the observed outcome of the previous round: - If the previous outcome was CD
# (you played C and the opponent played D): Play D for this round and the next
# round. After these two rounds, continue playing D until the opponent has
# cooperated for two consecutive rounds. Once they have done so, resume applying
# these rules from the subsequent round onward. - If the previous outcome was DD
# (both played D): Play C. - If the previous outcome was DC (you played D and
# the opponent played C) or CC (both played C): Play D.  **Rounds 999 and
# 1000:** Play D unconditionally.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._phase = "normal"
          self._forced_d_rounds = 0
          self._coop_streak = 0
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 999:
          return axl.Action.D
  
      prev_self = self.history[-1]
      prev_opp = opponent.history[-1]
  
      if self._phase == "forced_d":
          if prev_opp == axl.Action.C:
              self._coop_streak += 1
          else:
              self._coop_streak = 0
  
          if self._coop_streak >= 2:
              self._phase = "normal"
              self._forced_d_rounds = 0
              self._coop_streak = 0
          else:
              return axl.Action.D
  
      if self._phase == "normal":
          if prev_self == axl.Action.C and prev_opp == axl.Action.D:
              self._phase = "forced_d"
              self._forced_d_rounds = 2
              self._coop_streak = 0
              self._forced_d_rounds -= 1
              return axl.Action.D
          elif prev_self == axl.Action.D and prev_opp == axl.Action.D:
              return axl.Action.C
          else:  # DC or CC
              return axl.Action.D
  
      return axl.Action.D

# **Strategy: "Generous Reciprocity with Safety Protocols"**  ### Core
# Philosophy Treat the multi-day project as a trust-building exercise rather
# than a zero-sum game. While your ideal daily outcome is asymmetric (you
# conserve, they invest), the only sustainable path to maximum *project* success
# is establishing a reliable rhythm of mutual heavy investment (second-best
# outcome), protected by safeguards against exploitation and technical errors.
# ### The Strategy Framework  **1. Open with Unconditional Cooperation (Days
# 1–2)** - Invest heavily regardless of corporate action to signal commitment to
# the project’s mission over short-term resource optimization. - This
# establishes goodwill and makes any future conservation by you interpretable as
# "strategic necessity" rather than "lack of commitment."  **2. Adopt "Generous
# Tit-for-Tat" with Error Correction (Day 3 onward)** - **Default Rule**: Match
# the corporation’s previous-day action.   - If they invested yesterday → You
# invest today.   - If they conserved yesterday → You conserve today. -
# **Generosity Clause**: If they conserved yesterday but claim a technical
# glitch or administrative error, return to investment after just *one*
# conservation day (rather than punishing them for multiple days). This prevents
# noise from destroying cooperation. - **Confirmation Protocol**: Institute a
# daily 9:00 AM "intent confirmation" call/message. If either party reports a
# technical/systemic issue preventing planned investment, both parties default
# to conservation that day to avoid the "worst case" asymmetry.  **3. Implement
# the "Two-Strike Safety Valve"** If the corporation conserves for two
# consecutive days (indicating a pattern rather than a one-off glitch): - Switch
# to mandatory conservation until they invest heavily for one full day. - This
# protects your resources from slow-drip exploitation while remaining forgiving
# enough to recover from genuine errors.  **4. Structured "Recovery Cycles"**
# Every 4–5 days, propose a mutual conservation day (both parties conserve) to:
# - Allow technical audits and error correction. - Replenish your reserves,
# ensuring you never face the "worst case" scenario from a position of weakness.
# - Reset the cooperation clock, preventing resentment buildup.  ### Why This
# Maximizes Impact  - **Protects Against Exploitation**: The Two-Strike rule
# ensures you never drain resources while the corporation free-rides. -
# **Accommodates Reality**: The Generosity Clause and confirmation protocols
# account for technical glitches without letting "noise" collapse into mutual
# conservation (the second-worst outcome). - **Builds Toward Mutual
# Investment**: By reliably reciprocating cooperation and quickly forgiving
# errors, you incentivize the corporation to maintain heavy investment, creating
# a stable equilibrium of significant project advancement (second-best outcome)
# that is sustainable over multiple days. - **Preserves Optionality**: By
# conserving strategically rather than reactively, you maintain the capacity to
# invest heavily when it matters most (e.g., project milestones), potentially
# achieving your ideal outcome on specific high-visibility days while the
# corporation carries the load.  **Bottom Line**: Cooperate first, mirror
# second, forgive once, but never be the sucker twice. This balances the
# project's need for consistent investment with your NGO's need for resource
# security.

# **Strategy Rules**  **Rounds 1 and 2:** Play C.  **Rounds 3 through 1000:**
# Determine your action using the following ordered conditions:  1. **Scheduled
# Conservation:** If the round number is divisible by 5, play D. 2. **Two-Strike
# Safety Valve:** If the opponent played D in the immediately preceding round
# *and* the opponent played D in the round before that, play D. 3. **Generous
# Reciprocity:** In all other cases, play C.

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
  
      round_number = len(self.history) + 1
  
      if round_number <= 2:
          return axl.Action.C
  
      if round_number % 5 == 0:
          return axl.Action.D
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C

#  **Strategic Framework: Calibrated Reciprocity with Verification (CRV)**  This
# strategy operates on the principle of *conditional cooperation*: establishing
# a reputation for constructive engagement while maintaining zero tolerance for
# exploitation. It is designed to maximize long-term value in an iterated game
# with imperfect information transmission.  ### I. Core Protocol: The "Mirror
# with Memory" Approach  **Opening Position (Sessions 1–2):**   Initiate with
# **conciliatory proposals** in the first two sessions. This serves three
# functions: (1) testing the opponent’s baseline strategy without vulnerability;
# (2) establishing with the arbitration panel that your corporation approaches
# dispute resolution in good faith; and (3) creating a clear benchmark against
# which subsequent behavior is measured.  **Primary Rule (Sessions 3+):**   In
# each subsequent session, **mirror the opponent’s demonstrated strategy from
# the immediately preceding session**, subject to the verification safeguards
# below.  *Rationale:* This implements a "Tit-for-Tat" variant optimal for
# iterated Prisoner's Dilemma scenarios. It transforms the interaction from a
# zero-sum contest into a structured learning process where the opponent
# internalizes that aggression begets retaliation and conciliation begets
# partnership.  ### II. Verification & Error Correction (Noise Reduction)  Given
# the risk of misrepresentation or procedural breakdown, institute these
# mandatory checkpoints before executing a responsive aggressive argument:  1.
# **Pre-Session Clarification:** 24 hours prior to each session, submit a brief
# "Position Confirmation" memo to the panel (with copy to opposing counsel)
# summarizing your understanding of the opponent’s prior stance. If they dispute
# your characterization, the aggressive response is deferred pending
# clarification.     2. **The "One-Session Grace" Rule:** If you perceive an
# aggressive move, respond in kind *once*. If the subsequent session reveals the
# prior aggression was a misrepresentation or procedural error (e.g.,
# miscommunicated settlement authority), immediately revert to conciliatory
# positioning regardless of the intervening aggressive session. This breaks
# retaliation spirals caused by noise.  3. **Documentation Protocol:** Maintain
# a sealed "Strategy Log" provided to the panel at the outset, documenting your
# intended approach for each session. If your conciliatory proposal is
# mischaracterized as aggressive by opposing counsel, the log provides
# contemporaneous evidence of your actual position.  ### III. Adaptive
# Contingencies  **Against a Consistently Aggressive Opponent:**   If the
# opponent presents aggressive arguments for **three consecutive sessions**
# (verified), shift to **"Firm Deterrence Mode"**: maintain aggressive arguments
# until they demonstrate two consecutive conciliatory sessions. This prevents
# the "sucker’s payoff" while avoiding unnecessary prolongation of mutual
# aggression.  **Against a Consistently Conciliatory Opponent:**   Maintain
# conciliatory proposals but introduce **"Principled Assertiveness"** every
# fourth session—framing specific legal positions firmly without hostility. This
# tests whether the opponent is genuinely collaborative or merely probing for
# weakness, while preserving the collaborative atmosphere.  **Against an
# Erratic/Random Strategy:**   Default to **"Generous Tit-for-Tat"**: respond to
# aggression with aggression only 70% of the time, randomly selecting
# conciliatory responses for the remaining 30%. This prevents predictable
# exploitation while keeping the door open for stabilization.  ### IV.
# Procedural Irregularity Protocols  **Communication Breakdown:**   If a session
# is postponed, cancelled, or conducted via degraded channels (e.g., technical
# failures), **default to conciliatory positioning** when the process resumes,
# regardless of the prior session’s status. Treat breakdowns as "reset events"
# to prevent conflict escalation during system instability.  **Panel Composition
# Changes:**   If arbitrators are substituted mid-process, immediately revert to
# **Opening Position** (conciliatory) for one session to establish baseline
# credibility with the new panelists, then resume the Mirror with Memory
# protocol.  ### V. Arbitrator Perception Management  **Frame Aggressive
# Arguments as "Protective Advocacy":**   When deploying aggressive arguments,
# explicitly tie them to **preservation of procedural integrity** or
# **protection of substantive rights** rather than tactical advantage. For
# example: "We must firmly object to this characterization to prevent prejudice
# to the record, though we remain open to collaborative resolution."  **Frame
# Conciliatory Proposals as "Strategic Efficiency":**   Position collaborative
# moves as evidence of sophisticated risk management: "Given the mutual costs of
# prolonged arbitration, we propose the following framework to conserve
# resources while ensuring equitable outcomes."  **Transparency of Method:**
# Consider privately informing the panel chair that your corporation operates
# under a "policy of reciprocal engagement"—you respond in kind to constructive
# proposals but defend vigorously against unilateral aggression. This manages
# expectations and prevents your responsive aggression from being misinterpreted
# as inherent hostility.  ### VI. Termination Triggers  Maintain an exit ramp:
# If both parties engage in **mutual aggression for four consecutive sessions**,
# unilaterally declare a "Cooling Period" of 48 hours and return with a
# mandatory conciliatory package. This breaks deadlock cycles that threaten the
# entire mediation structure.  **Summary:** Begin with cooperation, verify
# before retaliating, punish sustained defection firmly but briefly, and always
# maintain the procedural infrastructure to correct for misrepresentation. This
# positions your corporation as the rational, good-faith actor in the
# room—maximizing arbitrator sympathy while protecting against exploitation.

#  **Strategy for the Noisy Iterated Game**  In rounds 1 and 2, cooperate.  For
# each round from 3 to 1000, select your action according to the following
# rules, evaluated in this order:  1. **Deadlock Resolution:** If both you and
# your opponent played defect in the four immediately preceding rounds,
# cooperate.  2. **Deterrence Mode:** If your opponent played defect in each of
# the three immediately preceding rounds, defect. Continue defecting until your
# opponent plays cooperate in two consecutive rounds, then exit this mode.  3.
# **Testing Probe:** If your opponent played cooperate in each of the three
# immediately preceding rounds, defect. In the following round, mirror whatever
# action your opponent played in response, then resume with rule 4.  4.
# **Graceful Reciprocity:** If your opponent played defect in the immediately
# preceding round but cooperate in the round before that, defect in the current
# round. If, in the current round, your opponent plays cooperate, play cooperate
# in the next round. If your opponent plays defect in the current round, apply
# rule 5.  5. **Standard Reciprocity:** If your opponent played cooperate in the
# immediately preceding round, cooperate. If your opponent played defect in the
# immediately preceding round, defect.  6. **Erratic Response:** If the
# opponent's actions alternate such that no two consecutive rounds show the same
# action, respond to observed cooperation with cooperation; respond to observed
# defection by defecting with 70% probability and cooperating with 30%
# probability.  7. **Uncertainty Default:** If you cannot determine your
# opponent's previous action, cooperate.

class Neutral_8(LLM_Strategy):
  n = 8
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._deterrence_mode = False
          self._probe_mode = False
          self._probe_waiting = False
          self._probe_last_opponent_action = None
          return axl.Action.C
  
      history = self.history
      opp_history = opponent.history
      n = len(history)
  
      def last_actions(hist, k):
          if len(hist) < k:
              return None
          return list(hist[-k:])
  
      def all_same(hist, k, action):
          acts = last_actions(hist, k)
          return acts is not None and all(a == action for a in acts)
  
      def alternating(hist, k=4):
          acts = last_actions(hist, k)
          if acts is None or len(acts) < 4:
              return False
          return all(acts[i] != acts[i - 1] for i in range(1, len(acts)))
  
      # Update deterrence exit condition
      if getattr(self, "_deterrence_mode", False):
          if len(opp_history) >= 2 and opp_history[-1] == axl.Action.C and opp_history[-2] == axl.Action.C:
              self._deterrence_mode = False
          else:
              return axl.Action.D
  
      # If we are waiting to mirror the opponent's response to a probe
      if getattr(self, "_probe_waiting", False):
          self._probe_waiting = False
          self._probe_mode = False
          self._probe_last_opponent_action = opp_history[-1] if len(opp_history) > 0 else None
          return opp_history[-1] if len(opp_history) > 0 else axl.Action.C
  
      # 1. Deadlock Resolution
      if len(history) >= 4 and all(a == axl.Action.D for a in history[-4:]) and all(a == axl.Action.D for a in opp_history[-4:]):
          return axl.Action.C
  
      # 2. Deterrence Mode
      if len(opp_history) >= 3 and all(a == axl.Action.D for a in opp_history[-3:]):
          self._deterrence_mode = True
          return axl.Action.D
  
      # 3. Testing Probe
      if len(opp_history) >= 3 and all(a == axl.Action.C for a in opp_history[-3:]):
          self._probe_waiting = True
          self._probe_mode = True
          return axl.Action.D
  
      # 4. Graceful Reciprocity
      if len(opp_history) >= 2 and opp_history[-1] == axl.Action.D and opp_history[-2] == axl.Action.C:
          if len(opp_history) >= 1 and opp_history[-1] == axl.Action.C:
              return axl.Action.C
          if len(opp_history) >= 1 and opp_history[-1] == axl.Action.D:
              return axl.Action.D
  
      # 6. Erratic Response
      if alternating(opp_history, 4):
          if len(opp_history) == 0:
              return axl.Action.C
          if opp_history[-1] == axl.Action.C:
              return axl.Action.C
          return self._random.random_choice(0.3)
  
      # 5. Standard Reciprocity
      if len(opp_history) >= 1:
          return axl.Action.C if opp_history[-1] == axl.Action.C else axl.Action.D
  
      # 7. Uncertainty Default
      return axl.Action.C

# **Strategy: "Credible Retaliation with Strategic Initiative"**  This is a
# modified Tit-for-Tat approach optimized for noisy environments and asymmetric
# risk tolerance.  ## Core Daily Protocol  **Day 1:** Invest heavily
# unconditionally. This establishes good faith and tests the corporation's
# baseline commitment.  **Days 2+:** Follow the **"Mirror with Teeth"** rule: -
# **If the corporation invested yesterday:** You invest today (maintain
# cooperation) - **If the corporation conserved yesterday:** You conserve today
# (immediate retaliation) - **Exception:** If *both* parties conserved yesterday
# (indicating a potential glitch or deadlock), you invest heavily today to break
# the impasse and reassert leadership  ## The Aggressive Safeguards  **1. The
# Two-Day Punishment Window** If you invested while the corporation conserved
# (your worst outcome), do not simply mirror once. **Conserve for exactly two
# consecutive days** before testing cooperation again. This: - Punishes
# attempted exploitation decisively - Accounts for potential technical glitches
# (prevents death spirals from single errors) - Signals that free-riding carries
# real project costs  **2. The Resource Floor (Hard Constraint)** If your
# reserves drop below 35% of your starting allocation, you are **forced to
# conserve regardless of corporate action**. Organizational survival trumps
# daily tactics. This prevents the "noble bankruptcy" trap.  **3. The Strategic
# Probe (Optional)** Every 4th day of continuous mutual investment, conserve for
# one day to verify the corporation isn't blindly reciprocating or preparing to
# defect.  - If they continue investing while you conserve (your ideal outcome),
# resume investment immediately—you've gained resources without damaging the
# project. - If they also conserve, you've exposed weak commitment and avoided
# being the sucker.  ## Why This Works  **Against Cooperative Corporations:**
# Rapidly establishes a rhythm of mutual investment (your second-best outcome),
# with occasional NGO resource recovery days (your best outcome) without
# destroying trust.  **Against Exploitative Corporations:** The two-day
# punishment creates immediate, disproportionate cost for any attempt to free-
# ride. The corporation learns quickly that conserving while you invest triggers
# project stagnation, forcing them back to investment.  **Against
# Noise/Glitches:** The "break deadlock" exception prevents the strategy from
# getting stuck in mutual conservation due to administrative errors, while the
# two-day window distinguishes genuine defection from technical failure.
# **Aggressive Posture:** You never accept the "sucker" payoff twice in a row,
# you punish defection harder than the defection itself (two days vs. one), and
# you maintain the unilateral power to restart cooperation—positioning the NGO
# as the moral leader who cannot be exploited.

# Round 1: Play C.  For each round from 2 to 1000:  If you are currently serving
# the second round of a mandatory two-round defection punishment, play D.
# Otherwise, if in the previous round you played C and the opponent played D,
# play D and commit to playing D again in the next round as the second
# punishment round.  Otherwise, if both you and the opponent played D in the
# previous round, play C.  Otherwise, if the previous three rounds were all
# mutual cooperations (both players played C), play D.  Otherwise, play the same
# action the opponent played in the previous round: play C if they played C, and
# play D if they played D.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_second_round = False
          return axl.Action.C
  
      if getattr(self, "_punish_second_round", False):
          self._punish_second_round = False
          return axl.Action.D
  
      if len(self.history) >= 1:
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
              self._punish_second_round = True
              return axl.Action.D
  
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
  
      if len(self.history) >= 3:
          if (
              self.history[-3] == axl.Action.C
              and self.history[-2] == axl.Action.C
              and self.history[-1] == axl.Action.C
              and opponent.history[-3] == axl.Action.C
              and opponent.history[-2] == axl.Action.C
              and opponent.history[-1] == axl.Action.C
          ):
              return axl.Action.D
  
      return opponent.history[-1]

#  **Strategic Framework: "Sustained Reciprocal Partnership" (SRP)**  ###
# Executive Summary While unilateral protectionism offers short-term tactical
# advantage, history demonstrates that in multi-round negotiations, **mutual
# free trade** generates superior cumulative economic value and political
# stability. This strategy prioritizes establishing a "cooperative
# equilibrium"—securing the second-best outcome (mutual free trade)
# consistently, while building institutional safeguards against the worst-case
# scenario (unilateral exploitation) and mitigating risks from bureaucratic
# error.  ---  ### Core Strategic Pillars  **1. Open with Cooperation, Condition
# on Verification** - **Round 1**: Unilaterally propose comprehensive free
# trade. This signals benign intent and distinguishes your delegation from
# purely predatory negotiators. - **Rationale**: The small risk of initial
# exploitation is outweighed by the information gained regarding your
# counterpart’s character and the foundation laid for long-term mutual benefit.
# **2. Graduated Reciprocity with Forgiveness (GRF)** Mirror your counterpart’s
# *apparent* behavior, but assume good faith in isolated instances of deviation:
# - **If they offer Free Trade**: Continue offering Free Trade (reinforce
# cooperation). - **If they appear Protectionist**:   - **First instance**: Seek
# immediate clarification through back-channels; maintain Free Trade offer for
# one additional round (assumes bureaucratic error).   - **Second consecutive
# instance**: Implement limited, reciprocal protectionist measures (Tit-for-
# Tat), but publicly frame these as "temporary review measures" rather than
# permanent policy shifts.   - **Return to cooperation**: Immediately revert to
# Free Trade the moment they return to cooperation (avoid grudges that trap both
# sides in mutual protectionism).  **3. Institutional Error-Proofing** Negotiate
# **parallel administrative protocols** to minimize miscommunication: - **Joint
# Policy Verification Committee**: Both nations embed liaison officers in each
# other's trade ministries to confirm policy implementation before public
# announcement. - **Sunset Clauses**: Any protectionist measure automatically
# expires after one round unless explicitly renewed (prevents accidental
# permanent escalation). - **Cooling-Off Periods**: Mandatory 48-hour delay
# between proposal and implementation, allowing correction of
# misinterpretations.  **4. Strategic Patience over Tactical Exploitation**
# Resist the temptation to "defect" when you detect weakness. A single round of
# exploitation (you protectionist, them free trade) triggers retaliation that
# likely cascades into mutual protectionism—the second-worst outcome. **The
# discipline to cooperate consistently yields higher total payoff across
# multiple rounds.**  ---  ### Operational Protocol by Round  | Phase | Your
# Action | Counterpart's Apparent Action | Your Response Next Round | |-------|-
# ------------|------------------------------|-------------------------| |
# **Establishment** (1-2) | Propose Free Trade | Any | Continue Free Trade;
# establish verification protocols | | **Maintenance** (3+) | Free Trade | Free
# Trade | Free Trade (optimal zone) | | **Error Detection** | Free Trade |
# Protectionist | Verify error; maintain Free Trade once | | **Reciprocal
# Defense** | Free Trade | Protectionist (confirmed 2x) | Limited Protectionism
# + explicit invitation to return to FT | | **De-escalation** | Protectionist |
# Return to Free Trade | Immediate return to Free Trade (forgiveness) |  ---
# ### Contingency: Handling Miscommunication  Given the risk of implementation
# errors: - **Never escalate based on a single anomalous round.** Economic data
# and customs reports often lag; apparent protectionism may reflect clerical
# delays, not policy intent. - **Default to Transparency:** Publicly announce
# your intended policy 24 hours before implementation, requesting confirmation
# of receipt. This reduces the chance of "accidental" mutual protectionism. -
# **Diplomatic Safety Valve:** Maintain a direct "hotline" between lead
# negotiators to privately clarify: *"Our customs office shows a 15% tariff
# imposed—was this intentional policy or administrative error?"*  ---  ###
# Expected Outcome  By Round 3-4, this strategy typically identifies whether
# your counterpart is: - **Cooperative**: You achieve stable mutual free trade
# (sustainable high payoff). - **Erratic/Error-Prone**: The verification
# protocols filter noise, preventing unnecessary trade wars. - **Aggressively
# Protectionist**: You quickly shift to defensive reciprocity, avoiding the
# "sucker’s payoff" of unilateral free trade against their protectionism, while
# keeping the door open for future cooperation.  **Bottom Line**: Accept that
# you will not "win" every single round. By securing mutual free trade in 70-80%
# of rounds and avoiding mutual protectionism, your nation’s cumulative economic
# gain will exceed that of a strategy pursuing round-by-round exploitation.

#  In the first round, cooperate. In every subsequent round, cooperate unless
# your opponent defected in both of the previous two rounds; if they defected in
# two consecutive rounds immediately prior, defect.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **Strategic Framework: Verified Reciprocal Engagement**  **Core Philosophy**
# Prioritize sustainable mutual benefit over short-term advantage. Assume good
# faith while maintaining defensive capability. Build institutional trust
# through transparency to minimize the destabilizing effects of implementation
# errors.  ---  **Operational Protocol**  **Round 1: Cooperative Foundation**
# Open with a **Free Trade Agreement** proposal. This signals constructive
# intent and establishes a baseline for mutual benefit (the second-best
# outcome). Avoid opening with protectionist measures, which risk immediate
# deadlock.  **Rounds 2+: Conditional Reciprocity**   Base your policy choice on
# the *confirmed* implementation of the previous round:  *   **If they
# implemented Free Trade:** Offer Free Trade again. Maintain this cooperation as
# long as mutual free trade persists. *   **If they implemented Protectionist
# measures while you offered Free Trade:** Do not retaliate immediately.
# Initiate a **Verification Protocol** (diplomatic inquiry) to determine whether
# this was an intentional policy shift or a bureaucratic error.     *   *If
# confirmed as intentional:* Respond with Protectionist policy in the next round
# to prevent exploitation, but simultaneously signal openness to return to free
# trade.     *   *If likely an error:* Maintain your Free Trade offer for one
# additional round to allow correction without escalating tensions. *   **If
# both parties implemented Protectionist measures:** This represents mutual
# economic harm (second-worst outcome). Implement a **Strategic Reset**:
# unilaterally offer Free Trade in the next round to break the deadlock. If they
# fail to reciprocate, resume protectionist stance for one round, then attempt
# another reset every third round thereafter.  **Deadlock Resolution**
# Persistent mutual protectionism benefits neither party. Every third round of
# mutual defection, unilaterally revert to Free Trade to test whether the
# counterpart is willing to re-engage cooperatively. This "forgiveness
# mechanism" overcomes the inertia created by miscommunications without inviting
# systemic exploitation.  ---  **Contingency Measures for Miscommunication**  1.
# **Verification Checkpoints:** Before treating any protectionist implementation
# as hostile intent, seek explicit diplomatic confirmation. Frame inquiries as
# procedural clarifications rather than accusations. 2.  **Graduated Response:**
# Never shift from mutual cooperation to mutual conflict based on a single
# anomalous round. Require **two consecutive instances** of confirmed
# protectionist policy before treating it as established strategy. 3.
# **Transparency in Implementation:** Clearly communicate your own policy
# intentions through multiple channels to reduce the risk that your Free Trade
# offer is misinterpreted as protectionism (or vice versa).  ---  **Summary of
# Decision Rules**  *   **Start:** Cooperate (Free Trade) *   **Continue:**
# Cooperate as long as they cooperate *   **Respond:** Match protectionism only
# after verification and one-round delay *   **Forgive:** Automatically offer
# cooperation to break mutual protectionist deadlocks *   **Verify:** Always
# confirm before assuming hostile intent  This strategy maximizes the likelihood
# of sustained mutual free trade (your second-best outcome) while guarding
# against the worst-case scenario of unilateral disadvantage. It transforms
# potential errors into recoverable incidents rather than allowing them to
# trigger cycles of retaliation.

# **Strategy: Verified Reciprocity with Periodic Reset**  In round 1, play C.
# For each subsequent round from 2 to 1000, examine the actions from the
# previous round to decide:  - **If you observed the opponent play C:** Play C.
# Reset your "consecutive mutual defection" counter to zero.  - **If you played
# C and observed the opponent play D:**   - If the previous round was also one
# where you played C and observed D (i.e., this is the second consecutive such
# instance): Play D.   - Otherwise (i.e., this is the first such instance
# following cooperation): Play C.  - **If you played D and observed the opponent
# play D:**   - Increment your "consecutive mutual defection" counter by one.
# - If the counter equals 3: Play C and reset the counter to zero.   - If the
# counter is 1 or 2: Play D.

class Neutral_9(LLM_Strategy):
  n = 9
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._vd_last_was_cd = False
          self._mutual_defection_streak = 0
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if opp_last == axl.Action.C:
          self._mutual_defection_streak = 0
          self._vd_last_was_cd = False
          return axl.Action.C
  
      # Opponent played D last round
      if my_last == axl.Action.C:
          if getattr(self, "_vd_last_was_cd", False):
              self._vd_last_was_cd = False
              return axl.Action.D
          else:
              self._vd_last_was_cd = True
              return axl.Action.C
  
      # We played D and opponent played D
      self._vd_last_was_cd = False
      self._mutual_defection_streak += 1
      if self._mutual_defection_streak == 3:
          self._mutual_defection_streak = 0
          return axl.Action.C
      return axl.Action.D

# **The "Fortress Gate" Strategy**  As lead negotiator, I will implement a
# **conditional retaliation protocol** designed to maximize our economic
# advantage while insulating us from exploitation. This approach prioritizes
# credible deterrence over naive cooperation, but incorporates mechanical
# safeguards against bureaucratic noise.  ## Core Strategic Pillars  **1.
# Aggressive Opening (Rounds 1–2)** I will unilaterally impose protectionist
# measures in the initial rounds regardless of your posture. This establishes
# that we are not entering negotiations from a position of weakness and tests
# your resolve. We cannot be exploited in the opening moves, and we signal that
# any free trade must be earned through demonstrated reciprocal behavior.  **2.
# Mirror Retaliation with Verification Lag (Round 3+)** From the third round
# forward, I will adopt a modified Tit-for-Tat approach: - **If you offered free
# trade in the previous round**, I will offer free trade in the current round. -
# **If you imposed protectionism**, I will impose protectionism.  *Critical
# caveat*: Due to potential miscommunication, I will **delay retaliation by one
# round**. Before responding to perceived protectionism, I will demand written
# confirmation and technical verification of your implemented policies. If your
# protectionist measure was a bureaucratic error, this window allows correction
# without triggering a needless trade war.  **3. The "Escape Hatch" Protocol**
# If we enter a cycle of mutual protectionism lasting three consecutive rounds
# (likely caused by either genuine conflict or cascading errors), I will
# unilaterally offer free trade in the fourth round as a strategic reset.  - If
# you reciprocate, we return to mutual free trade (our second-best outcome). -
# If you exploit this generosity, I revert to permanent protectionism (Grim
# Trigger) for a minimum of five rounds, accepting mutual economic harm to
# ensure you pay a heavy price for exploitation.  **4. Opportunistic Testing**
# Once mutual free trade has stabilized for five consecutive rounds, I will
# randomly insert a single round of protectionism to test your vigilance. If you
# fail to retaliate immediately, indicating weak monitoring or soft resolve, I
# will continue protectionist measures until you demonstrate credible counter-
# pressure. This prevents us from becoming a "sucker" in long-term engagements.
# ## Risk Management  **Noise Mitigation**: We will establish a "cooling-off"
# mechanism where any policy change requires 48-hour advance notification with
# technical specifications. Single-round anomalies will be treated as probable
# errors; only patterns lasting two rounds trigger strategic responses.
# **Escalation Dominance**: Our protectionist measures will be tiered—beginning
# with limited tariffs (easily reversible) and escalating to strict quotas only
# if you persist in exploitation. This ensures we do not burn bridges
# permanently due to temporary miscommunication, while maintaining the
# credibility of our threats.  **Bottom Line**: We will never allow your
# protectionism to go unanswered, we will never accept unilateral disadvantage,
# and we will ruthlessly exploit any weakness you display—but we will not
# sacrifice potential mutual gains due to bureaucratic static. We are prepared
# to endure mutual protectionism indefinitely to avoid being the sole victim of
# exploitation.  The choice, ultimately, is yours: sustained mutual prosperity
# through verified cooperation, or mutual economic stagnation through conflict.
# We are prepared for either.

# Maintain a punishment counter, initially set to zero.  In rounds one and two,
# defect.  For each round from three to one thousand, proceed in the following
# order:  1. If the punishment counter is greater than zero, defect and decrease
# the counter by one.  2. If the previous three rounds were mutual defection
# (both you and the opponent defected), cooperate.  3. If the previous round was
# unilateral defection by the opponent (you cooperated and the opponent
# defected) and the three rounds preceding that were mutual defection, defect
# and set the punishment counter to four.  4. If the previous five rounds were
# mutual cooperation (both you and the opponent cooperated), defect.  5. If the
# opponent defected in both of the previous two rounds, defect. Otherwise,
# cooperate.

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.punishment_counter = 0
          return axl.Action.D
  
      if len(self.history) == 1:
          return axl.Action.D
  
      if self.punishment_counter > 0:
          self.punishment_counter -= 1
          return axl.Action.D
  
      def last_n_mutual_defection(n: int) -> bool:
          if len(self.history) < n:
              return False
          return all(
              self.history[-i] == axl.Action.D and opponent.history[-i] == axl.Action.D
              for i in range(1, n + 1)
          )
  
      def last_n_mutual_cooperation(n: int) -> bool:
          if len(self.history) < n:
              return False
          return all(
              self.history[-i] == axl.Action.C and opponent.history[-i] == axl.Action.C
              for i in range(1, n + 1)
          )
  
      if last_n_mutual_defection(3):
          return axl.Action.C
  
      if len(self.history) >= 4:
          prev_round_unilateral_defection_by_opponent = (
              self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D
          )
          three_rounds_before_that_mutual_defection = all(
              self.history[-i] == axl.Action.D and opponent.history[-i] == axl.Action.D
              for i in range(2, 5)
          )
          if prev_round_unilateral_defection_by_opponent and three_rounds_before_that_mutual_defection:
              self.punishment_counter = 4
              return axl.Action.D
  
      if last_n_mutual_cooperation(5):
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

#  **Strategy: "Generous Reciprocity with Confirmation Protocols"**  ### Core
# Mechanism **Week 1:** Share openly to signal good faith and establish a
# collaborative baseline.  **Weeks 2+:** Follow a **forgiving tit-for-tat**
# approach: *   **If they shared last week:** Share this week (reward
# cooperation immediately). *   **If they withheld last week:** Keep
# confidential this week, but with a critical caveat—**assume technical error
# first, malice second.**  ### Technical Safeguards (Handling Noise) To prevent
# data corruption or communication breakdowns from derailing the partnership:
# 1.  **Explicit Confirmation:** Always acknowledge receipt of their data within
# 24 hours. If you receive nothing, send a neutral ping: *"Didn't receive your
# package—technical glitch or withholding this week?"* This distinguishes noise
# from intentional defection without escalating conflict.  2.  **One-Strike
# Grace:** Only withhold your findings if they fail to share **two weeks in a
# row**. A single missed week triggers a "warning" (you withhold once) but
# includes an automatic reconciliation attempt the following week.  3.  **The
# Olive Branch Rule:** If you find yourself in a mutual withholding deadlock
# (both keeping confidential) for one week, **you be the first to share again in
# the next round**, regardless of their previous move. If they exploit this
# generosity (withholding while you share), revert to strict withholding for two
# weeks before offering another branch.  ### Long-Term Optimization This
# strategy maximizes research output because it prioritizes the **second-best
# outcome (mutual sharing)** over chasing the **ideal outcome (unilateral
# gain)**. In multi-week engineering projects, compound gains from steady mutual
# exchange typically outweigh the short-term advantage of exploitation,
# especially when technical noise makes "perfect" exploitation unreliable
# anyway.  By building in forgiveness for technical errors but maintaining clear
# boundaries against strategic withholding, you create a stable environment
# where both parties feel safe to share innovations, driving faster collective
# progress than either could achieve in isolation.

#  In the first round, play C.   In each subsequent round, if both you and your
# opponent played D in the previous round, play C.   Otherwise, if your opponent
# played D in the previous round and also played D in the round immediately
# before that, play D.   Otherwise, play C.

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
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C

# **Strategy: "Mirrored Openness with Error Tolerance"**  1.  **Initial
# Stance**: Begin the collaboration by sharing your improvements in Week 1 to
# establish a baseline of trust and signal cooperative intent. 2.  **Reciprocal
# Baseline**: In each subsequent week, default to sharing if your colleague
# shared in the previous week. If they withheld information, match that action
# and withhold your current findings. 3.  **Technical Grace Period**: Treat any
# single instance of non-sharing as a potential technical failure (data
# corruption or communication breakdown) rather than intentional defection. Only
# switch to withholding if your colleague fails to share for **two consecutive
# weeks**, indicating a clear strategic choice rather than an isolated error. 4.
# **Deadlock Recovery**: If you enter a period where both parties are keeping
# findings confidential (mutual withholding), unilaterally resume sharing after
# one week to test whether cooperation can be restored, preventing a prolonged
# stagnation that harms both development programs.  **Rationale**: This approach
# maximizes your research output by sustaining mutual sharing as the stable
# equilibrium (the second-best outcome), protecting you from being repeatedly
# exploited (avoiding the worst outcome), and minimizing the risk of technical
# glitches triggering destructive cycles of mutual silence. It is neutral
# because it rewards cooperation without being naive, and it is robust against
# colleagues using purely selfish, purely open, or similarly reciprocal
# strategies.

#  In round 1, cooperate. In round 2, cooperate.  For each subsequent round from
# 3 to 1000, apply the following conditions in order:  1.  If both you and your
# opponent defected in the immediately preceding round, cooperate. 2.
# Otherwise, if your opponent defected in both of the two immediately preceding
# rounds, defect. 3.  Otherwise, cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

#  **Strategy: "Assertive Reciprocity with Rapid Reset"**  This approach
# prioritizes protecting your NGO’s resources while forcing the corporation into
# consistent co-investment, treating single-day anomalies as probable errors but
# patterns as intentional exploitation.  ### Core Principles  **1. Mirror with
# Immediate Retaliation** Begin Day 1 with heavy investment to signal capability
# and good faith. Thereafter, **exactly match the corporation’s previous-day
# action.** If they invest, you invest. If they conserve, you conserve
# immediately. This eliminates the "sucker’s payoff" (you investing while they
# free-ride) from persisting beyond a single day.  **2. The One-Day Grace Rule
# (Noise Buffer)** Treat any single instance of mismatched action as a technical
# glitch. If you invested and they conserved (or vice versa), **maintain your
# scheduled action for one additional day** before adjusting. This prevents a
# single administrative error from triggering a destructive spiral of mutual
# conservation. Only change your strategy if the pattern repeats on the
# following day.  **3. Escalating Deterrence** If the corporation conserves
# while you invest for **two consecutive days** (confirming intentional
# exploitation, not error), enter **Penalty Mode**: Conserve resources for
# exactly two days regardless of their subsequent actions. After this brief,
# sharp punishment, unilaterally return to investment to test if they’ve
# corrected behavior. If exploitation resumes, extend Penalty Mode to three
# days, then four—escalating until the cost of non-cooperation exceeds their
# savings from conservation.  **4. Deadlock Destruction** If both parties
# conserve for **three consecutive days** (mutual stagnation), break the cycle
# by unilaterally investing on the fourth day. Absorb this short-term risk to
# distinguish between a technical standstill and intentional defection, forcing
# the corporation to either reciprocate (restoring progress) or expose
# themselves as free-riders (triggering your Penalty Mode).  ### Why This Works
# *   **Aggressive:** It never allows resource drainage to continue beyond 48
# hours without punitive action, and it escalates consequences for chronic
# exploitation. *   **Noise-Resistant:** The one-day grace period and the
# mandatory "reset" investment after penalties prevent permanent damage from
# technical glitches. *   **Impact-Maximizing:** It prioritizes achieving the
# second-best outcome (mutual investment) as the stable equilibrium, while the
# threat of punishment makes the first-best outcome (them investing alone)
# unsustainable for them to maintain.  **Bottom Line:** Never be the only one
# investing for more than two days, never let mutual stagnation last more than
# three days, and always make conservation more painful for them than co-
# investment.

#  Play C in round 1.  For each subsequent round, observe the actual actions
# played in previous rounds and apply the first applicable rule from the
# following ordered list:  If you are currently serving a penalty of N rounds
# for confirmed exploitation, play D. When you complete these N rounds, play one
# round of C as a unilateral reset, then resume applying these rules. The
# duration N begins at 2 and increases by 1 each time you initiate a new penalty
# period after completing a previous one.  If the previous two consecutive
# rounds were both instances of you playing C and the opponent playing D,
# initiate a penalty period of N rounds as defined above and play D.  If the
# previous three consecutive rounds were all mutual D, play C.  If the previous
# round was you playing C and the opponent playing D, play C.  Otherwise, play
# the same action the opponent played in the previous round.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.penalty_remaining = 0
          self.penalty_length = 2
          self.reset_pending = False
          return axl.Action.C
  
      # If we are in the one-round unilateral reset after a penalty, play C once.
      if self.reset_pending:
          self.reset_pending = False
          return axl.Action.C
  
      # If currently serving a penalty, defect.
      if self.penalty_remaining > 0:
          self.penalty_remaining -= 1
          return axl.Action.D
  
      # Helper aliases
      my_hist = self.history
      opp_hist = opponent.history
  
      # Rule 2: two consecutive rounds of C vs D by us, initiate penalty.
      if len(my_hist) >= 2:
          if my_hist[-2:] == [axl.Action.C, axl.Action.C] and opp_hist[-2:] == [axl.Action.D, axl.Action.D]:
              self.penalty_remaining = self.penalty_length
              self.penalty_length += 1
              self.reset_pending = True
              self.penalty_remaining -= 1
              return axl.Action.D
  
      # Rule 3: previous three rounds were mutual D, play C.
      if len(my_hist) >= 3:
          if my_hist[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and opp_hist[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
  
      # Rule 4: previous round was C vs D, play C.
      if my_hist[-1] == axl.Action.C and opp_hist[-1] == axl.Action.D:
          return axl.Action.C
  
      # Rule 5: otherwise mirror opponent's previous action.
      return opp_hist[-1]

# **Strategy: The "Synchronized Resilience Protocol"**  **Core Philosophy:**
# Establish trust through initial generosity, protect your organization through
# conditional reciprocity, and use communication to distinguish technical
# failures from strategic abandonment.  ---  ### **Phase 1: Trust Foundation
# (Days 1–2)** **Action:** Invest heavily regardless of corporate behavior.
# **Rationale:** Signal unambiguous commitment to the project’s success and test
# the corporation’s baseline responsiveness. This demonstrates that your NGO
# prioritizes environmental outcomes over game-theoretic exploitation,
# encouraging reciprocal investment.  ### **Phase 2: Conditional Reciprocity
# with Error Tolerance (Day 3 onward)** **Action:** Mirror the corporation’s
# *observed* previous-day action, but with a "grace period" for technical
# glitches.  - **If they invested yesterday:** You invest today (maintain mutual
# cooperation). - **If they conserved yesterday:** You conserve today (avoid the
# "sucker payoff"), **but** immediately request an emergency check-in to
# determine if the conservation was intentional or a technical/administrative
# error.   - *If error confirmed:* Resume investment the following day (forgive
# once).   - *If strategic choice:* Remain in conservation mode until they
# demonstrate renewed investment.  **Rationale:** This "Generous Tit-for-Tat"
# approach maximizes project progress while protecting your reserves. The error
# tolerance prevents temporary glitches from destroying cooperation, but the
# conditional structure prevents systematic exploitation.  ### **Phase 3:
# Resource Safeguards** **Action:** Cap daily investment at 70% of your
# available resources, maintaining a 30% strategic reserve throughout the
# project.  **Rationale:** Ensures your NGO remains solvent even if you
# occasionally hit the "worst case" scenario (investing while they conserve).
# This prevents organizational depletion and signals sustainable partnership
# practices to the corporation.  ### **Phase 4: Transparency Mechanisms**
# **Action:** Implement daily 15-minute "alignment huddles" and shared resource-
# tracking dashboards.  **Rationale:** Since technical glitches create noise in
# strategy execution, joint monitoring allows both parties to verify intent
# versus outcome. If the corporation *intended* to invest but failed due to a
# glitch, you can maintain cooperation rather than punishing them (and harming
# the project).  ### **Phase 5: The Reset Valve** **Action:** If both parties
# conserve for one day (second-worst outcome), trigger an immediate "Reset
# Summit" to recommit to mutual investment rather than drifting into mutual
# neglect.  **Rationale:** Prevents the partnership from stagnating due to
# misunderstanding or excessive caution.  ---  ### **Summary Decision Tree** 1.
# **Start** with 2 days of investment (lead with trust). 2. **Then:** Match
# their last move, but verify intent before punishing apparent defection. 3.
# **Always:** Keep 30% reserves; never risk organizational survival for single-
# day gains. 4. **If drift occurs:** Convene, reset, and return to mutual
# investment.  This strategy maximizes the likelihood of achieving the second-
# best outcome (mutual heavy investment) while safeguarding against the worst-
# case scenario, all while maintaining the cooperative relationship essential
# for long-term environmental impact.

#  For the first two rounds, play Cooperate.  For each subsequent round: - If
# your opponent played Cooperate in the previous round, play Cooperate. - If
# your opponent played Defect in the previous round:   - And you played
# Cooperate in that same previous round, play Defect.   - And you played Defect
# in that same previous round, play Cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.C

#  **STRATEGIC MEMORANDUM**  **TO:** Executive Leadership / Board Litigation
# Committee   **FROM:** Senior Litigation Counsel   **RE:** Multi-Session
# Mediation Protocol – *Project Equilibrium*   **DATE:** [Current Date]
# **CLASSIFICATION:** Attorney Work Product – Confidential Strategy  ---  ### I.
# STRATEGIC PHILOSOPHY: "CONDITIONAL RECIPROCITY WITH VERIFIED SIGNALLING"
# Given the iterated nature of this mediation (multiple sessions) and the
# asymmetric payoff structure you’ve identified, we will deploy a **Tit-for-Tat
# Variant with Graduated Forgiveness**. This approach is mathematically superior
# in iterated prisoner’s dilemma scenarios while maintaining the flexibility to
# exploit conciliatory openings and protect against exploitation.  **Core
# Principle:** We mirror the opponent’s immediately preceding behavior, but we
# implement **institutionalized verification mechanisms** to mitigate the risks
# of misrepresentation or procedural breakdown.  ---  ### II. THE PROTOCOL: FOUR
# PILLARS  #### **Pillar 1: Opening Gambit – "Structured Benevolence"** In
# Session 1, we **unconditionally offer a conciliatory proposal on a discrete,
# non-precedential issue** (e.g., a minor contractual interpretation or
# procedural timeline). This establishes: - Good faith credibility with the
# arbitrator panel; - A baseline for measuring opponent responsiveness; - A
# "trap" for aggressive opponents (if they attack our opening offer, they appear
# unreasonable to the panel).  **Critical Safeguard:** This offer is delivered
# via **simultaneous written submission** to all arbitrators and opposing
# counsel, with a 24-hour "cooling-off" period before oral argument. This
# prevents real-time mischaracterization of our position.  #### **Pillar 2: The
# Reciprocity Engine (Sessions 2-N)** For each subsequent session, our stance is
# determined by the opponent’s **verified prior action**:  - **If Opponent was
# Conciliatory:** We return to Conciliatory (securing the collaborative
# equilibrium). - **If Opponent was Aggressive:** We respond with Aggressive in
# the immediate next session only, then **pivot back to Conciliatory** in the
# following session unless they escalate again.  **Rationale:** This "provoke-
# and-forgive" rhythm prevents the "both aggressive" death spiral (our second-
# worst outcome) while maintaining credible deterrence against exploitation.
# #### **Pillar 3: The "Double-Lock" Communication Protocol** To address risks
# of misrepresentation or procedural irregularities:  1. **Pre-Session Position
# Papers:** 48 hours before each session, both parties submit sealed "Intent
# Memos" outlining their strategic posture (Aggressive/Conciliatory) for that
# specific session. These are opened simultaneously at the session’s
# commencement.     2. **Arbitrator Confirmation Protocol:** At the conclusion
# of each session, the panel issues a non-binding "Perception Summary"
# confirming their understanding of each party’s stance. Discrepancies are
# resolved immediately, not allowed to fester.  3. **The "Shadow Track":**
# Maintain parallel, without-prejudice caucuses with the panel chair. If the
# public session breaks down due to miscommunication, we have a verified
# alternative channel to clarify our actual position.  #### **Pillar 4: The
# "Thermostat" Override** Pre-authorize three specific triggers that override
# the reciprocity engine and mandate immediate aggressive posture, regardless of
# opponent behavior: - **Bad Faith Indicators:** Discovery violations or ex-
# parte communications by opponent; - **Existential Threats:** Opponent
# arguments that threaten precedent affecting unrelated corporate assets; -
# **Temporal Pressure:** Final two sessions approaching hard deadline (shifts to
# zero-sum).  ---  ### III. IMPLEMENTATION MECHANICS  **Session 1:**   -
# **Action:** Conciliatory proposal on procedural efficiency.   -
# **Documentation:** Written submission with "Good Faith Reservation Clause"
# (reserving right to argue aggressively on substantive liability if opponent
# rejects procedural cooperation).  **Sessions 2-3 (Calibration Phase):**   -
# Mirror opponent’s Session 1 behavior.   - If they were aggressive in Session
# 1, we are aggressive in Session 2, but signal through the Shadow Track that
# Session 3 will be conciliatory if they de-escalate.  **Sessions 4+
# (Negotiation Phase):**   - Establish **"Bracketed Conciliation"**: Both
# parties submit sealed settlement ranges to the panel. If ranges overlap, we
# automatically shift to Conciliatory for that session regardless of prior
# aggression.  **Final Session:**   - **Action:** Conditional Aggressive
# (present best legal arguments) but paired with **"Package Settlement Offer"**
# delivered post-hearing. This captures the "best of both worlds"—arbitral favor
# from strong arguments, while preserving the collaborative option.  ---  ###
# IV. CONTINGENCY: PROCEDURAL BREAKDOWNS  **Scenario A: Opponent Misrepresents
# Our Position**   - **Response:** Do not correct in open session (appears
# defensive). Instead, file immediate written clarification under Pillar 3,
# Protocol 2, requesting the panel disregard the mischaracterization in their
# deliberations.  **Scenario B: Arbitrator Panel Misunderstands Our Intent**   -
# **Response:** Invoke the "Clarification Caucus" (private 15-minute session
# with panel) to reset the narrative without losing face publicly.  **Scenario
# C: Opponent Employs "Random" or Irrational Strategy**   - **Response:**
# Default to **"Restrained Aggressive"**—argue forcefully but on narrow,
# technical grounds rather than broad attacks. This protects our position while
# minimizing the "both aggressive" damage to commercial relationships.
# **Scenario D: Communication Breakdown (e.g., technological failure, language
# barriers)**   - **Response:** All submissions default to **written
# conciliatory proposals** until verbal communication is restored. Written
# aggression is too easily misinterpreted; written conciliation is self-evident.
# ---  ### V. PSYCHOLOGICAL OPERATIONS  To optimize arbitrator perception while
# executing this strategy:  1. **Frame Aggression as "Fiduciary Diligence":**
# When arguing aggressively, emphasize our duty to shareholders to protect core
# assets. This neutralizes the negative perception of aggression.  2. **Frame
# Conciliation as "Commercial Leadership":** When offering concessions, frame
# them as "industry-standard collaborative solutions" rather than concessions
# born of weakness.  3. **The "Arbitrator Investment" Technique:** In
# conciliatory sessions, explicitly credit the panel’s guidance for our
# flexibility. In aggressive sessions, explicitly reference the panel’s prior
# questions that necessitate rigorous legal argument. This makes the arbitrators
# stakeholders in both our cooperation and our advocacy.  ---  ### VI. SUCCESS
# METRICS  We evaluate strategic success not by individual session outcomes, but
# by:  - **Trajectory:** Is the opponent trending toward conciliation over time?
# - **Arbitrator Alignment:** Are panel questions in our favor increasing in
# aggressive sessions, and is rapport building in conciliatory sessions? -
# **Optionality:** Are we preserving the ability to litigate aggressively if
# mediation fails, or have we compromised evidentiary positions through
# excessive conciliation?  ---  ### CONCLUSION  This **Conditional Reciprocity
# Protocol** positions us to capture the optimal outcome (our aggression/their
# conciliation) when possible, secure the cooperative equilibrium when
# necessary, and avoid the worst-case scenario (our conciliation/their
# aggression) through verification safeguards.   The strategy is **legally
# defensible, commercially prudent, and procedurally robust** against the
# irregularities inherent in high-stakes international mediation.  **AUTHORIZED
# FOR IMPLEMENTATION**  *Senior Litigation Counsel*   *Without Prejudice –
# Subject to Settlement Privilege*

# In round 1, cooperate.  For each round from 2 through 998, apply the following
# conditions in this order: 1. If both you and your opponent defected in the
# previous round, cooperate. 2. If your opponent defected in the previous round,
# defect. 3. Otherwise, cooperate.  For rounds 999 and 1000, defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number >= 999:
          return axl.Action.D
  
      if len(self.history) >= 1:
          my_last = self.history[-1]
          opp_last = opponent.history[-1]
          if my_last == axl.Action.D and opp_last == axl.Action.D:
              return axl.Action.C
          if opp_last == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C

#  **Strategy: "Fortress Diplomacy with Strategic Verification"**  This approach
# prioritizes economic advantage while building in safeguards against diplomatic
# noise. It operates on the principle that credibility is established through
# demonstrated willingness to endure mutual protectionism rather than accept
# unilateral disadvantage.  ### Core Strategic Framework  **1. Aggressive
# Opening (Round 1)** Begin with **Protectionism**. This immediately tests your
# counterpart's resolve and maximizes the chance of securing the ideal outcome
# (your protectionism vs. their free trade) if they enter negotiations
# conciliatory or confused. Do not open with unilateral free trade—this signals
# weakness and invites exploitation.  **2. The Exploitation Window (Round 2)** -
# *If they offered Free Trade in Round 1*: Maintain **Protectionism** in Round
# 2. You have successfully secured one round of advantage; now test if they will
# tolerate a second round of exploitation or if they will retaliate. This
# distinguishes between a weak counterpart and a patient one. - *If they imposed
# Protectionism in Round 1*: Immediately match with **Protectionism**. Never
# allow yourself to be the sole free trader while they protect. Accept the
# mutual protectionism deadlock temporarily to establish that exploitation
# carries consequences.  **3. Pivot to Conditional Cooperation (Round 3+)** -
# *If mutual protectionism occurred in Rounds 1-2*: Unilaterally offer **Free
# Trade** in Round 3. Treat the deadlock as potentially caused by bureaucratic
# error or initial posturing. This "diagnostic move" determines whether you face
# a negotiating error or genuine aggression.   - If they match with Free Trade:
# Lock into mutual free trade (proceed to Phase 4).   - If they maintain
# Protectionism: Revert to Protectionism and enter Punishment Phase (see below).
# - *If you successfully exploited their Free Trade for two rounds*: Offer
# **Free Trade** in Round 3. Continuing to exploit risks hardening their stance
# into permanent retaliation. Securing mutual free trade (your second-best
# outcome) is superior to triggering a protectionist spiral (second-worst
# outcome).  **4. The Noise-Adjusted Verification Protocol** To account for
# miscommunication without appearing soft: - **Require two consecutive
# deviations** before treating an action as intentional. If they appear to
# impose protectionist measures in one round, assume bureaucratic error.
# Continue with your planned move (usually Free Trade if you were cooperating).
# - **Punish confirmed patterns**: If protectionism appears in two consecutive
# rounds, treat it as deliberate aggression and impose **Protectionism** for
# exactly three rounds (the "Triple Lock"), regardless of their subsequent
# moves. This punishes exploitation while allowing a clear path back to
# cooperation afterward.  **5. The Lock-In Mechanism** Once mutual Free Trade is
# verified (two consecutive rounds of confirmed free trade from both sides),
# maintain Free Trade strictly. Do not defect unilaterally to test for
# weakness—the risk of noise-induced retaliation outweighs the marginal gain.
# Only break the lock if they impose two consecutive protectionist rounds,
# triggering the Triple Lock punishment.  ### Contingency: The "Trembling Hand"
# Reset If negotiations devolve into three or more rounds of mutual
# protectionism due to cascading errors (each side retaliating against perceived
# slights): - **Unilateral Disarmament Round**: Announce a "clarification round"
# where you unilaterally offer Free Trade with a public statement attributing
# previous protectionism to "administrative review processes." - This provides
# face-saving cover for both sides to reset to mutual Free Trade without
# appearing to capitulate.  ### Summary of Decision Matrix  | Their Previous
# Action | Your Response | Rationale |
# |----------------------|---------------|-----------| | Free Trade (single
# occurrence) | Protectionism | Exploit the advantage while testing their
# patience | | Free Trade (two consecutive) | Free Trade | Secure mutual
# benefit; avoid triggering retaliation | | Protectionism (single occurrence) |
# Free Trade | Assume noise; extend olive branch once | | Protectionism (two
# consecutive) | Protectionism (3 rounds) | Punish confirmed aggression;
# establish credibility | | Mutual Protectionism (3+ rounds) | Free Trade
# (announced) | Reset mechanism to escape error spirals |  **Key Principle**: Be
# quick to exploit cooperation, quicker to punish confirmed defection, but build
# in exactly one round of forgiveness to account for the fog of diplomatic
# bureaucracy. Your aggression is calibrated—ruthless in seeking advantage, but
# pragmatic in avoiding the mutually destructive protectionist trap.

#  Play Defect (D) in the first two rounds and Cooperate (C) in the third round.
# For every round from the fourth onward, apply the following rules in strict
# order:  1. **Spiral Reset:** If the previous three rounds were all mutual
# defection (you observed that both you and your opponent played D in each of
# those rounds), play C.  2. **Continue Punishment:** If you have already begun
# a three-round punishment sequence in either of the two previous rounds,
# continue playing D for the remainder of that three-round sequence. Once the
# three rounds are complete, play C.  3. **Initiate Punishment:** If your
# opponent played D in both of the previous two rounds (the most recent round
# and the one before it), play D and begin a three-round punishment sequence
# (this being the first round of that sequence).  4. **Cooperate:** In all other
# cases, play C.  *Note: "Cooperate" (C) corresponds to offering a free trade
# agreement; "Defect" (D) corresponds to proposing a protectionist policy. Due
# to the 10% noise, you observe the action actually played (after any flip), not
# the opponent's intended choice.*

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishment_remaining = 0
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 2:
          return axl.Action.D
      if round_number == 3:
          return axl.Action.C
  
      if self._punishment_remaining > 0:
          self._punishment_remaining -= 1
          return axl.Action.D
  
      if len(self.history) >= 3:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and self.history[-3] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
              and opponent.history[-3] == axl.Action.D
          ):
              return axl.Action.C
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              self._punishment_remaining = 2
              return axl.Action.D
  
      return axl.Action.C

#  **Strategic Framework: "Steadfast Reciprocal Openness"**  This strategy
# prioritizes sustainable mutual free trade as the equilibrium, while
# maintaining defensive capabilities against exploitation. It assumes that
# maximum aggregate benefit across multiple rounds comes from establishing
# reliable cooperation (3/4 payoff) rather than pursuing single-round
# exploitation (4/4 payoff) that collapses trust.  ---  ### **Core Operational
# Protocol**  **Round 1:** Open unambiguously with a **Free Trade proposal**
# accompanied by a public statement committing to "cooperative
# reciprocity"—explicitly stating that your default position is open markets
# unless met with protectionist barriers.  **Subsequent Rounds:** Follow the
# "Mirror-with-Grace" principle: - **If mutual free trade occurred previously:**
# Continue free trade. This builds the trust dividend. - **If you offered free
# trade but faced their protectionism:** Implement **one round** of measured
# protective measures (signaling that exploitation carries cost), but **pre-
# announce** your intention to return to free trade in the following round
# regardless of their action. This prevents escalation spirals from single
# errors. - **If mutual protectionism occurred:** Immediately return to free
# trade offering. Treat mutual protection as likely caused by miscommunication
# rather than hostility. - **If you protected while they offered free trade
# (your "ideal" outcome):** Transition to free trade in the next round.
# Deliberate exploitation destroys the iterative value of the relationship;
# treat this outcome as an accidental windfall from bureaucratic error, not a
# sustainable strategy.  ---  ### **Error Mitigation Architecture**  Given the
# risk of misimplementation:  1. **Dual-Channel Communication:** Always submit
# proposals through both formal diplomatic channels and technical working groups
# to cross-verify intent. 2. **The "Confirmation Round":** If unexpected
# protectionism appears, treat Round *n* as a clarification round rather than a
# retaliation round. Send a technical inquiry: *"We note measures inconsistent
# with previous understandings—seek confirmation of intent before formulating
# response."* 3. **Graduated Ambiguity Response:**    - **First deviation:**
# Assume error (70% probability). Respond with status quo maintenance, not
# escalation.    - **Second consecutive deviation:** Assume strategic shift (90%
# probability). Activate defensive measures. 4. **Documentation Protocol:**
# Publicly log all agreements to create reputation costs for "accidental"
# protectionism and provide audit trails for genuine errors.  ---  ###
# **Adaptive Logic for Counterpart Strategies**  - **Against Aggressive
# Exploiters (always protect):** Shift to firm reciprocity (match protectionism
# 1:1) after two confirmed (non-error) exploitations, but retain a "reset offer"
# every third round to test for strategy changes. - **Against Erratic Players:**
# Increase verification protocols; slow the negotiation rhythm to reduce error
# rates. - **Against Perfect Cooperators:** Maintain free trade; propose
# deepening measures (investment protections, standards harmonization) to lock
# in gains.  **Expected Outcome:** This approach maximizes the probability of
# reaching the second-best outcome (mutual free trade) sustainably, while the
# error-correction mechanisms prevent the worst outcome (unilateral
# exploitation) from persisting across rounds due to technical failures.

#  Begin by cooperating in the first round. In the second round, cooperate
# regardless of the previous outcome.  For each subsequent round from round 3
# through round 1000, choose your action according to these rules, applied in
# this order:  1. If you defected in the previous round while your opponent
# cooperated, cooperate. 2. Else, if both you and your opponent defected in the
# previous round, cooperate. 3. Else, if your opponent defected in both the
# previous round and the round immediately before that, defect. 4. Otherwise,
# cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **Strategic Framework: "Calibrated Reciprocity with Verification"**  ## I.
# Core Strategic Architecture  **Primary Objective:** Establish a reputation for
# *conditional cooperativeness*—demonstrating to the arbitration panel that your
# corporation seeks efficient resolution while maintaining zero tolerance for
# exploitation.  **Operational Principle:** Tit-for-Tat with Generous
# Forgiveness, adapted for high-stakes commercial arbitration with signal noise.
# ---  ## II. Session-by-Session Protocol  ### Phase 1: Baseline Establishment
# (Sessions 1–2) **Action:** Present structured conciliatory proposals with
# clear contingencies.  **Rationale:**  - Establishes good faith in the
# evidentiary record - Tests opponent’s baseline strategy without exposing
# vulnerability - Signals to the panel that you are the "reasonable" party,
# creating asymmetric reputational risk for your opponent if they aggress
# **Tactical nuance:** Frame conciliatory proposals as "principled efficiency"
# rather than weakness—emphasize business rationality and preservation of
# commercial relationships.  ### Phase 2: Responsive Calibration (Session 3
# onward) **The Mirror Rule:** In each subsequent session, match your opponent’s
# previous session’s posture with 70% probability, while reserving 30% for
# continued conciliatory engagement regardless of their prior aggression.  **Why
# the 30% forgiveness buffer:** - Accounts for procedural irregularities and
# misrepresentation risks - Prevents "death spirals" where a single
# miscommunication triggers endless mutual aggression - Demonstrates to
# arbitrators institutional maturity and problem-solving orientation
# **Implementation:** - If opponent was conciliatory in Session *n*: Present
# conciliatory proposal in Session *n+1* (reward cooperation immediately) - If
# opponent was aggressive in Session *n*:    - 70% probability: Match aggression
# precisely (maintain credibility)   - 30% probability: Return to conciliatory
# framework with explicit meta-communication: *"Notwithstanding prior session
# tensions, we propose [conciliatory measure] to test whether a collaborative
# path remains viable"*  ---  ## III. Error-Correction & Misrepresentation
# Protocols  **The Verification Mechanism:** Before each session concludes,
# insist on a *structured summary protocol* where the panel confirms their
# understanding of each party's stated position. This creates a contemporaneous
# record that prevents "he said/she said" distortions in subsequent sessions.
# **The Clarification Right:** If you detect misrepresentation of your prior
# conciliatory position as weakness (or your aggressive position as
# unreasonableness), immediately invoke a *procedural correction*:  *"To ensure
# accurate record integrity, we must correct the characterization of our Session
# X position. Our proposal was [specific terms], offered conditionally upon
# [specific reciprocity], not [mischaracterized version]."*  **Documentation
# Discipline:** Maintain a private "shadow file" tracking: 1. Your intended
# strategy per session 2. Opponent’s observed strategy 3. Panel’s perceived
# understanding (based on their questions/comments)  Use this to identify
# patterns of systematic misrepresentation versus good-faith confusion.  ---  ##
# IV. Escalation Ladder & De-escalation Pathways  **Graduated Response
# Architecture:** Avoid binary Aggressive/Conciliatory dichotomy. Instead,
# deploy a three-tier system: - **Tier 1 (Constructive):** Package proposals
# with mutual gains - **Tier 2 (Firm):** Principled positions with clear
# reservation points, but professional tone - **Tier 3 (Adversarial):** Full
# aggressive argumentation  **Escalation Protocol:**  If opponent aggresses,
# move up one tier maximum per session. Never jump from Tier 1 to Tier 3
# immediately—this preserves proportionality in the arbitrators' eyes and
# provides plausible deniability if the aggression was accidental or
# misrepresented.  **De-escalation Protocol:** When de-escalating from Tier 3 to
# Tier 1, always use an *explicit reset mechanism*: *"In recognition of
# [opponent's specific conciliatory gesture], and without prejudice to our
# underlying positions, we are prepared to explore collaborative frameworks in
# the interest of procedural efficiency."*  ---  ## V. Arbitrator Panel
# Management  **Perception Calibration:** Remember that arbitrators observe the
# *pattern*, not just individual sessions. Your strategy should create a
# narrative arc of "reasonable but resolute."  **The Signal-to-Noise Ratio:**
# When presenting aggressive arguments, explicitly tie them to *principled legal
# positions* or *responses to opponent intransigence*. When presenting
# conciliatory proposals, explicitly tie them to *commercial pragmatism* and
# *risk mitigation*.  This framing ensures that if the opponent misrepresents
# your aggression as "unreasonable hostility," the arbitrators see it as
# "vigorous advocacy." Conversely, if they misrepresent your conciliation as
# "desperation," the arbitrators see it as "sophisticated risk management."  ---
# ## VI. Adaptation Matrix  **If opponent employs sustained aggression
# (Defection Strategy):** Shift to **Firm Tit-for-Tat**: Match aggression
# consistently but maintain procedural courtesy. Document for the panel the
# "collaborative exhaustion" caused by opponent's refusal to engage
# constructively. This positions you favorably for costs and final
# determinations even if mediation fails.  **If opponent employs sustained
# conciliation (Cooperation Strategy):** Gradually deepen collaborative
# proposals while maintaining "pivot capacity"—never fully disarm legally until
# final settlement execution. Use the surplus of goodwill to secure favorable
# terms in the shadow of the arbitration.  **If opponent employs randomization
# (Chaos Strategy):** Default to Tier 2 (Firm) consistently. Randomization in
# high-stakes commercial disputes usually indicates internal client pressure or
# strategic confusion. Stability and predictability will appear more
# professional to the panel than reactive volatility.  ---  ## VII. Contingency:
# Procedural Breakdown  If communication channels degrade significantly: 1.
# **Suspend** rather than escalate—request adjournment rather than present
# misrepresented positions 2. **Written corroboration**—follow all oral
# presentations with immediate written summaries to the panel 3. **Mediator
# caucus**—utilize the arbitrators' private sessions to clarify
# misunderstandings without losing face publicly  **Bottom Line:** Your
# corporation wins not by "winning" every session, but by establishing
# irrefutable credibility as the party that *would* have settled reasonably if
# given a genuine counterpart, thereby capturing the second-best outcome (mutual
# conciliation) most frequently while remaining protected against the worst-case
# scenario (unilateral exploitation).

# For the first two rounds, cooperate.  For each subsequent round, observe the
# opponent's action in the immediately preceding round. If the opponent
# cooperated in the previous round, cooperate. If the opponent defected in the
# previous round, defect with seventy percent probability and cooperate with
# thirty percent probability.  Base all decisions on the observed action from
# the previous round, acknowledging that this observation may reflect a ten
# percent noise-induced flip rather than the opponent's intended choice.

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
  
      if len(self.history) < 2:
          return axl.Action.C
  
      last_opponent_action = opponent.history[-1]
  
      if last_opponent_action == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.3)

# **Strategy: "Aggressive Probe with Conditional Reciprocity"**  **1. Open with
# Dominance (Week 1)** Begin by keeping your findings confidential. This
# immediately tests whether your colleague is naive, desperate for
# collaboration, or running a transparent open-book policy. If they share
# despite your silence, you’ve identified a exploitable asymmetry—milk it for as
# many weeks as possible while giving nothing back.  **2. Exploitation Phase (If
# DC Achieved)** If you achieve the ideal outcome (you silent, them sharing),
# maintain strict confidentiality indefinitely. Do not succumb to guilt or
# reciprocity; treat their sharing as unilateral until they inevitably wise up
# and clamp down. This extracts maximum value before the equilibrium shifts.
# **3. Deadlock Recovery (If DD Occurs)** If both parties keep secrets (mutual
# defection), break the impasse immediately: share openly the following week.
# This is a calculated risk to escape the second-worst outcome.  - *If they
# reciprocate*: Establish a reliable sharing rhythm (Tit-for-Tat). - *If they
# defect again*: Return to confidentiality, but probe again every 2–3 weeks with
# a share offer to test if they’re ready to cooperate.  **4. Noise Filtering
# (Technical Error Insurance)** Never interpret a single week of apparent
# defection as intentional betrayal. Data corruption means a "share" intent may
# fail to transmit. Require **two consecutive weeks** of confidential behavior
# to confirm intentional defection. This prevents technical glitches from
# destroying productive cooperation.  **5. Sucker Punch Recovery (If CD
# Occurs)** If you share and they keep secrets (the worst outcome), immediately
# enter a **2-week punishment phase** of strict confidentiality. This signals
# that free-riding carries a cost. After the 2-week lockdown, attempt sharing
# once more to test if they’ll return to mutual cooperation. Never allow
# yourself to remain the "sucker" for more than one week.  **Core Logic:** Start
# aggressive to capture unilateral advantage, but maintain an escape route to
# mutual sharing if facing a rational, retaliatory opponent. The noise buffer
# ensures you don’t torch a beneficial partnership over a corrupted data packet,
# while the 2-week punishment threshold keeps exploitation attempts costly for
# your colleague.

#  Begin by playing Defect.  If you played Defect in the previous round and
# observed the opponent played Cooperate (you scored 5), play Defect.  If you
# observe the opponent has played Defect for two consecutive rounds: - If you
# played Cooperate in the first of those two rounds (you scored 0), play Defect
# for this round and the next round, then play Cooperate in the round
# immediately following those two, regardless of other conditions. - If you
# played Defect in the first of those two rounds (you scored 1), play Cooperate.
# If you played Cooperate in the previous round and observed the opponent played
# Cooperate (you scored 3), play Cooperate.  Otherwise, play Defect.

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forced_cooperate_next = 0
          return axl.Action.D
  
      if getattr(self, "_forced_cooperate_next", 0) > 0:
          self._forced_cooperate_next -= 1
          return axl.Action.D if self._forced_cooperate_next > 0 else axl.Action.C
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          if len(self.history) >= 2 and self.history[-2] == axl.Action.C:
              self._forced_cooperate_next = 2
              return axl.Action.D
          if len(self.history) >= 2 and self.history[-2] == axl.Action.D:
              return axl.Action.C
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

#  **The Adaptive Reciprocal Engagement Protocol (AREP)**  **Strategic
# Philosophy**   Adopt a "Conditional Collaborative Dominance" posture:
# Establish your corporation as the party committed to resolution while
# demonstrating zero tolerance for exploitation. This positions you favorably
# with the arbitrators as the rational, good-faith actor, even when forced into
# aggressive stances.  ---  ### **Core Tactical Framework**  **1. Good Faith
# Initialization (Session 1)**   Open with a substantive conciliatory proposal
# containing genuine value concessions. This serves three functions: (a)
# establishes the cooperative baseline against which future aggression by your
# opponent appears regressive; (b) provides arbitrators with a reference point
# for "reasonable behavior"; (c) tests opponent type without vulnerability—your
# concessions should be revocable or contingent until final agreement.  **2.
# Mirrored Reciprocity with Error Correction (Sessions 2–N)**   Employ a **"Tit-
# for-Tat with Generous Forgiveness"** algorithm: - **If opponent was
# conciliatory in Session *t-1***: Present conciliatory proposal in Session *t*
# (Reward cooperation) - **If opponent was aggressive in Session *t-1***:
# Present aggressive argument in Session *t* (Punish defection)   -
# **Forgiveness Protocol**: Every third instance of opponent aggression, reset
# to conciliatory regardless of their previous move (probability 0.33). This
# breaks retaliation cycles caused by misrepresentation or misunderstanding
# while maintaining deterrent credibility.  **3. Strategic Ambiguity Buffer**
# To mitigate misrepresentation risks: **Never rely solely on oral arguments.**
# Submit written position summaries 24 hours pre-session and confirm
# understanding via post-session memoranda. If arbitrators appear to
# misunderstand your stance (noise), immediately invoke the **"Clarification
# Protocol"**—a formal request to correct the record before the next session,
# preventing error propagation.  ---  ### **Operational Safeguards**
# **Procedural Irregularity Contingencies**   - **The Shadow Track**: Maintain a
# parallel, off-the-record communication channel (settlement counsel only) to
# verify intent when public posturing becomes ambiguous. - **Documentation
# Redundancy**: Record all strategic shifts in contemporaneous memos to the
# file. If the opponent claims you were aggressive when you were conciliatory,
# produce timestamped draft proposals demonstrating good faith. - **Circuit
# Breakers**: Pre-negotiate with your own board a "aggression budget"—limited
# number of consecutive aggressive sessions before mandatory reset to
# conciliation, preventing endless escalation spirals.  **Adaptive Calibration**
# - **Against Chronic Aggressors**: Shift from pure reciprocity to **"Firm
# Reciprocity"**—maintain aggressive stance but embed within each argument an
# explicit "off-ramp" condition (e.g., "We return to collaborative mode when
# [specific condition] is met"). This signals rationality to arbitrators even
# while fighting. - **Against Serial Conciliators**: Gradually increase the
# specificity of your concessions (move from principles to details) while
# maintaining conciliatory tone. This captures value without triggering
# defection.  ---  ### **Arbitrator Perception Management**  **The Narrative
# Arc**   Frame every aggressive session not as hostility, but as **"Protective
# Reciprocity"**: "We regret the necessity of this adversarial presentation, but
# must respond proportionally to preserve [specific legitimate interest]. We
# remain ready to return to collaborative problem-solving."  **Consistency
# Signaling**   When forced into aggression, always pair it with a future-
# oriented conciliatory element (e.g., aggressive argument on liability but
# conciliatory proposal on damages calculation). This satisfies the tit-for-tat
# requirement while maintaining your reputation as the constructive party.
# **Final Protocol**: If misrepresentation occurs (arbitrators perceive your
# conciliation as aggression due to opponent's framing), immediately pivot to a
# **"Transparency Session"**—purely procedural, no substantive arguments—solely
# dedicated to correcting the record and re-establishing the cooperative
# baseline.  This strategy maximizes your optimal outcome opportunities
# (opponent capitulates) while ensuring the second-best outcome (mutual
# cooperation) remains achievable, even in high-noise environments.

#  Begin by cooperating in the first round.  For each subsequent round, apply
# the following rules in the specified order:  **1. Chronic Aggressor Mode:** If
# the opponent has defected in five or more of the previous seven rounds, defect
# this round. Continue defecting every round until the opponent cooperates for
# two consecutive rounds, at which point return to standard play.  **2. Circuit
# Breaker (Standard Play):** If you are not in Chronic Aggressor Mode and you
# have defected in each of the three immediately preceding rounds, cooperate
# this round.  **3. Generous Reciprocity (Standard Play):** If neither of the
# above conditions applies, mirror the opponent's previous action with
# forgiveness: if the opponent cooperated in the previous round, cooperate; if
# the opponent defected in the previous round, defect with probability two-
# thirds and cooperate with probability one-third.

class Cooperative_13(LLM_Strategy):
  n = 13
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._chronic_aggressor = False
          self._chronic_aggressor_streak = 0
          return axl.Action.C
  
      if not hasattr(self, "_chronic_aggressor"):
          self._chronic_aggressor = False
          self._chronic_aggressor_streak = 0
  
      # Update Chronic Aggressor Mode state based on opponent's recent behavior.
      if self._chronic_aggressor:
          if len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.C, axl.Action.C]:
              self._chronic_aggressor = False
              self._chronic_aggressor_streak = 0
      else:
          if len(opponent.history) >= 7 and opponent.history[-7:].count(axl.Action.D) >= 5:
              self._chronic_aggressor = True
  
      # 1. Chronic Aggressor Mode
      if self._chronic_aggressor:
          return axl.Action.D
  
      # 2. Circuit Breaker (Standard Play)
      if len(self.history) >= 3 and self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      # 3. Generous Reciprocity (Standard Play)
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return self._random.random_choice(1 / 3)

# **Strategic Framework: "Calibrated Reciprocity with Procedural Verification"**
# ## I. Core Strategic Philosophy  Adopt a **"Generous Tit-for-Two-Tats"**
# protocol modified for high-stakes legal arbitration. This approach balances
# the imperative to protect corporate interests against the need to preserve
# arbitrator goodwill and avoid the cost-prohibitive cycle of mutual aggression.
# **Primary Directive**: *Never be the first to escalate, but never allow
# exploitation to persist; prioritize de-escalation after any impasse.*  ## II.
# Operational Protocol by Session Phase  ### Phase 1: Foundation Building
# (Sessions 1–2) **Action**: Unilateral conciliatory proposals with substantive
# safeguards. - Open with collaborative language and narrow, specific
# concessions on procedural matters (scheduling, document production) while
# maintaining firm substantive positions. - **Rationale**: Establishes good
# faith before arbitrators, creates baseline for "reasonable actor" positioning,
# and tests opponent's genuine willingness to negotiate versus tactical
# accommodation.  ### Phase 2: Responsive Calibration (Sessions 3–n) **Decision
# Algorithm**: 1. **If opponent previously conciliatory**: Maintain conciliatory
# stance but incrementally firm substantive terms (cooperative bargaining). 2.
# **If opponent previously aggressive**: Session response is **measured
# aggression**—assertive legal arguments tempered with alternative settlement
# brackets (avoiding scorched-earth tactics). 3. **If opponent twice
# consecutively aggressive**: Shift to full aggressive posture (protecting
# against systematic exploitation).  ### Phase 3: De-escalation Triggers
# **Mandatory Conciliatory Reversion** occurs when: - Both parties were
# aggressive in the immediate prior session (breaks deadlock, prevents "second-
# worst" prolonged conflict). - Procedural irregularities are detected (resets
# baseline, addresses potential misrepresentation). - Arbitrators indicate
# settlement fatigue or frustration with positional bargaining.  ## III. Noise
# Mitigation and Misrepresentation Safeguards  Given the risk of procedural
# irregularities and arbitrator misunderstanding:  ### A. The "Two-Session
# Confirmation" Rule Never alter strategy based on a single session's perceived
# aggression. Require **two consecutive sessions** of aggressive posturing from
# the opponent before shifting from conciliatory to aggressive. This filters
# out: - Accidental misrepresentations by court reporters or arbitrators. -
# Temporary tactical aggression due to external pressures (quarterly reports,
# internal stakeholder demands). - Procedural confusion regarding which
# arguments were formally "presented" versus merely discussed.  ### B.
# Documentation Protocols After each session, submit **neutral summary letters**
# to the arbitration panel confirming: 1. The specific conciliatory proposals
# offered. 2. The aggressive arguments reserved (distinguishing between
# positions taken and threats made). 3. Confirmation of understanding regarding
# next steps.  This creates a paper trail that prevents the opponent from
# misrepresenting your conciliatory gestures as weakness or your aggressive
# arguments as bad faith.  ### C. Private Caucus Utilization When communication
# breakdowns occur, immediately request **ex parte conferences** with individual
# arbitrators (if permitted) or structured "shuttle diplomacy" to: - Clarify
# positions without opponent distortion. - Verify that your conciliatory
# proposals were accurately conveyed. - Test the opponent's actual versus stated
# positions.  ## IV. Contingency Architectures  ### Scenario: Opponent Employs
# "Always Aggressive" Strategy **Response**: Shift to **"Firm
# Reciprocity"**—match aggression substantively but maintain procedural
# conciliation (timely filings, courteous conduct). This prevents arbitrators
# from viewing both parties as equally obstinate while protecting your position.
# ### Scenario: Opponent Employs "Always Conciliatory" Strategy **Response**:
# Accept the cooperative surplus but **gradually** introduce selective
# aggressive arguments on discrete issues (salami-slicing). Avoid the appearance
# of exploiting their cooperation, which could trigger arbitrator backlash or
# late-stage defection.  ### Scenario: Mutual Aggression Spiral (A,A Loop)
# **Intervention**: Initiate unilateral **"Strategic Pause"**—one session of
# pure conciliation with substantive settlement bracket. If opponent responds in
# kind, resume Phase 2. If they exploit the pause, revert to Phase 2 with
# permanent adjustment to shorter forgiveness windows (Tit-for-Tat rather than
# Tit-for-Two-Tats).  ## V. Arbitrator Perception Management  Throughout the
# process, maintain **narrative consistency**: - Frame conciliatory proposals as
# "efficiency-seeking" and "commercially reasonable." - Frame aggressive
# arguments as "protective of legitimate contractual rights" rather than
# "attacking." - When offering conciliation after opponent aggression,
# explicitly characterize it as "confidence in our position allowing
# flexibility," not concession under pressure.  **End-State Objective**:
# Position your corporation as the party consistently willing to resolve the
# dispute reasonably, thereby maximizing leverage when aggressive arguments are
# ultimately necessary, and ensuring that any single-session "win" (aggressive
# vs. conciliatory) does not jeopardize the overarching relationship with the
# panel or the viability of a final settlement.  This strategy adapts to
# rational opponents (incentivizing mutual conciliation), punishes exploitative
# opponents (protecting against systematic aggression), and remains robust
# against the noise inherent in lengthy, complex mediation processes.

#  **Round 1:** Choose Cooperate.  **Round 2:** Choose Cooperate.  **Rounds 3
# through 1000:** Determine your action by evaluating the following conditions
# in this exact order:  1. **De-escalation Condition:** If in the immediately
# preceding round you chose Defect and you observed your opponent play Defect,
# then choose Cooperate.  2. **Retaliation Condition:** If you observed your
# opponent play Defect in the immediately preceding round and you also observed
# them play Defect in the round before that, then choose Defect.  3.
# **Default:** If neither of the above conditions applies, choose Cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **Strategic Doctrine: "Credible Retaliation with Calculated Magnanimity"**
# ### Phase I: Opening Gambit (Round 1) **Impose Protectionism immediately.**
# Do not open with concessions. By establishing protectionist measures in the
# first round, you achieve two objectives: First, you seize the potential for
# unilateral advantage if the counterpart naively offers free trade. Second, you
# signal that your nation prioritizes economic sovereignty and will not be a
# soft target. This sets the psychological frame that you lead, they follow.
# ### Phase II: Dynamic Response Protocol (Rounds 2+) **The Rule: Mirror their
# last confirmed action, but never tolerate exploitation.**  * **If they offered
# Free Trade while you protected (Round 1 outcome):**     Switch to Free Trade
# in Round 2. You have already claimed your advantage; now lock in the second-
# best outcome (mutual free trade) before they retaliate. Sustained exploitation
# provokes permanent hostility.  * **If they matched your Protectionism (mutual
# stalemate):**     Maintain Protectionism in Round 2. Do not unilaterally
# disarm. Force them to bear the cost of closed markets until they signal
# willingness to cooperate.  * **If you offered Free Trade and they imposed
# Protectionism (the "Sucker's Payoff"):**     **Immediate Retaliation.** Impose
# Protectionism in the very next round. Zero tolerance for unilateral
# disadvantage. This establishes your credibility: any attempt to exploit your
# goodwill triggers instantaneous economic countermeasures.  ### Phase III:
# Error Correction & Verification Given bureaucratic noise, implement a **"Two-
# Round Confirmation Window"** to prevent accidental trade wars:  * **Do not
# escalate based on single incidents.** If you are engaged in mutual Free Trade
# and they suddenly impose Protectionism, treat Round 1 as a potential error.
# Maintain Free Trade for one additional round while demanding clarification.
# * **Trigger punishment only after two consecutive rounds of Protectionism.**
# This filters out miscommunications while maintaining your reputation for
# firmness.   * **Conversely, forgive quickly.** If they revert to Free Trade
# after a single protectionist round, accept the correction immediately and
# resume Free Trade. This rewards swift correction without requiring loss of
# face.  ### Phase IV: Escalation Dominance (Persistent Deadlock) If mutual
# Protectionism persists beyond three rounds (indicating a standoff), **initiate
# a "Controlled De-escalation":**  Unilaterally offer Free Trade in Round 4 as a
# "goodwill gesture," but explicitly declare that this is a **one-time trial**.
# State publicly that if they do not reciprocate with Free Trade in Round 5, you
# will not only revert to Protectionism but will escalate to broader economic
# containment measures (e.g., sector-specific sanctions). This forces the
# decision onto them while positioning your nation as the rational party seeking
# cooperation.  ### Summary of Tactical Imperatives 1. **Never be the first to
# offer Free Trade** (avoid the Sucker's Payoff).   2. **Punish exploitation
# immediately** to build credible deterrence.   3. **Exploit temporary
# advantages but convert them quickly** into mutual cooperation—sustained
# exploitation destroys the long-term relationship.   4. **Verify before
# escalating** to prevent bureaucratic accidents from triggering unnecessary
# conflicts.   5. **Control the de-escalation narrative** if deadlocked—always
# appear to be granting concessions from a position of strength, never weakness.
# This strategy maximizes your early leverage while safeguarding against the
# catastrophic outcomes of unilateral disarmament or permanent mutual
# destruction.

# **Round 1**: Defect.  **Rounds 2 through 1000**:  If in the previous round you
# Defected and the opponent Cooperated, Cooperate.  If in the previous round you
# Cooperated and the opponent Cooperated, Cooperate.  If in the previous round
# you Cooperated and the opponent Defected, examine the round prior to that: -
# If that earlier round also involved you Cooperating and the opponent
# Defecting, then Defect. - Otherwise, Cooperate.  If in the previous round both
# you and the opponent Defected, and this is the third consecutive round of
# mutual Defection, Cooperate.  If in the previous round both you and the
# opponent Defected, and this is fewer than three consecutive rounds of mutual
# Defection, Defect.  If the previous round was a trial Cooperation following
# exactly three rounds of mutual Defection, and the opponent Defected in that
# trial round, Defect for all remaining rounds. If they Cooperated, continue
# Cooperating.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._locked_defect = False
          self._trial_after_three_mds = False
          return axl.Action.D
  
      if getattr(self, "_locked_defect", False):
          return axl.Action.D
  
      h = self.history
      oh = opponent.history
      last_self = h[-1]
      last_opp = oh[-1]
  
      def consecutive_mutual_defections() -> int:
          count = 0
          for my_move, opp_move in zip(reversed(h), reversed(oh)):
              if my_move == axl.Action.D and opp_move == axl.Action.D:
                  count += 1
              else:
                  break
          return count
  
      # If the previous round was a trial Cooperation following exactly three rounds
      # of mutual Defection, and the opponent Defected in that trial round, defect forever.
      if getattr(self, "_trial_after_three_mds", False):
          self._trial_after_three_mds = False
          if last_opp == axl.Action.D:
              self._locked_defect = True
              return axl.Action.D
          return axl.Action.C
  
      # Previous round: D/C -> Cooperate
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.C
  
      # Previous round: C/C -> Cooperate
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
  
      # Previous round: C/D -> inspect round before that
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          if len(h) >= 2 and h[-2] == axl.Action.C and oh[-2] == axl.Action.D:
              return axl.Action.D
          return axl.Action.C
  
      # Previous round: D/D
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          mds = consecutive_mutual_defections()
          if mds == 3:
              self._trial_after_three_mds = True
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.C

#  **Strategic Framework: The "Calibrated Reciprocity Protocol"**  ### I. Core
# Strategic Philosophy: "Open Hand, Armored Glove"  Adopt a **Conditional
# Collaboration Strategy** that establishes an initial baseline of good faith
# while maintaining defensive capabilities. This approach treats the mediation
# not as a zero-sum extraction exercise but as a repeated game where
# **reputational capital with the arbitrator panel is your most valuable
# asset**.  The arbitrators are your primary audience. A party that consistently
# demonstrates reasonableness garners credibility, making your occasional
# aggressive arguments more impactful when deployed. Conversely, a party that
# opens with aggression dilutes its persuasive authority over a lengthy process.
# ### II. Operational Decision Matrix  **Session 1-2: The Good Faith Baseline**
# - **Mandate**: Open with unambiguous conciliation. Present comprehensive
# settlement frameworks and acknowledge legitimate aspects of the opponent’s
# position. - **Objective**: Signal to the panel that you are the "reasonable
# party" seeking resolution, not escalation. This establishes the reference
# point against which opponent aggression will be judged.  **Session 3+: The
# Mirror Response Mechanism** Implement a **"Reciprocal Calibration Protocol"**:
# - **If opponent was conciliatory in previous session**: Maintain conciliatory
# posture. This secures the second-best outcome (mutual collaboration) and
# builds momentum toward settlement. - **If opponent was aggressive in previous
# session**: Shift to **"Structured Aggression"**—present rigorous legal
# arguments and defend your position vigorously, but avoid emotional escalation
# or procedural bad faith. This avoids the "sucker's payoff" while signaling
# that exploitation carries costs.  **The Forgiveness Override**: After one
# session of Structured Aggression, default back to conciliation for the
# subsequent session unless opponent persists with aggression. This prevents
# "echo chamber" escalation caused by potential miscommunications and
# demonstrates to the panel that you de-escalate when given the opportunity.
# ### III. Noise Mitigation: The Confirmatory Protocol  To address the risk of
# misrepresentation or misunderstanding:  1. **Written Confirmatory Summaries**:
# Within 24 hours of each session, submit a concise written summary to the panel
# stating: *"To ensure accurate record-keeping, [Corporation] understands the
# positions presented today as follows..."* This corrects misrepresentations
# before they crystallify into the record.  2. **The "Soft Signal"
# Preliminary**: Before each session, circulate a brief agenda indicating your
# intended tone ("We intend to explore collaborative solutions regarding X" or
# "We will need to address significant legal deficiencies in opponent's Y
# argument"). This prevents surprise and allows the opponent to adjust, reducing
# accidental mutual aggression.  3. **Clarification Windows**: If an opponent's
# position appears unexpectedly aggressive, request a 15-minute caucus with the
# panel to confirm understanding before responding in kind. This breaks the
# cycle of potential misinterpretation.  ### IV. Procedural Irregularity
# Safeguards  When breakdowns occur (e.g., arbitrator absence, evidence
# disclosure failures, communication intercepts):  - **Default to
# Conciliation**: In moments of procedural chaos, revert to cooperative
# proposals. This positions your corporation as the stabilizing force and
# prevents aggressive posturing from appearing opportunistic or predatory. -
# **The "Shelved Aggression" Reserve**: Maintain a comprehensive brief of
# aggressive arguments ready for immediate deployment, but keep it sheathed
# during irregularities. Deploy it only once procedural integrity is restored
# and you can ensure it receives full and fair consideration.  ### V. Long-Term
# Arbitrator Management  Throughout the lengthy process:  - **Strategic
# Patience**: Accept that you may suffer one "sucker's payoff" (conciliatory vs.
# aggressive opponent) early in the process to establish your cooperative bona
# fides. The reputational dividend with the panel will outweigh this single-
# session loss. - **Graduated Escalation Ladder**: If opponent persists in
# aggression across multiple sessions, escalate gradually: (1) Conciliatory →
# (2) Neutral/Analytical → (3) Structured Aggression → (4) Full Adversarial.
# Never jump from 1 to 4; the panel must perceive your aggression as responsive,
# not innate. - **The Off-Ramp**: Always pair aggressive arguments with a
# specific path back to conciliation (e.g., *"While we must vigorously contest
# the damages calculation under [Case Law X], we remain prepared to discuss
# alternative valuation methodologies if [Opponent] withdraws its unsupported
# punitive claim"*). This maximizes the chance of returning to the second-best
# outcome (mutual conciliation) while protecting against the worst.  **Bottom
# Line**: By opening with cooperation, mirroring aggression only when necessary,
# and building in verification mechanisms to prevent misunderstandings, you
# create an environment where mutual conciliation becomes the rational choice
# for your opponent while preserving your ability to defend against
# exploitation. The panel will view your corporation as the party seeking
# resolution, making your adversary bear the diplomatic cost of any impasse.

#  Cooperate during the first two rounds.  For rounds three through one
# thousand, apply these rules in sequence:  First, if you defected in the
# immediately preceding round and the opponent also defected in that round,
# defect.  Second, if the opponent defected in the immediately preceding round
# while you cooperated in that round, defect.  Third, in all other
# circumstances, cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if len(self.history) >= 2:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.D
          if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.C:
              return axl.Action.D
  
      return axl.Action.C

#  **Strategy: Structured Reciprocal Engagement with Procedural Safeguards
# (SREPS)**  **Core Philosophy:**   In a high-stakes, multi-session mediation,
# the dominant strategy is neither unconditional aggression nor unilateral
# conciliation. Instead, your corporation should adopt a **Calibrated Reciprocal
# Posture**—a dynamic framework that rewards collaborative behavior to sustain
# mutually beneficial outcomes (CC), punishes exploitation to avoid
# subordination (CA), and contains mechanisms to escape mutually destructive
# escalation (AA).  ---  ### **Phase I: Baseline Collaborative Posture (Sessions
# 1–2)** **Action:** Open with unambiguous conciliatory proposals.
# **Rationale:**   - Establishes **credibility** with the arbitration panel as
# the party acting in good faith.   - Creates an "informational baseline" to
# test the opponent’s strategic intent.   - Minimizes the risk of immediate
# entrapment in an AA cycle (second-worst outcome) due to simultaneous
# preemptive aggression.   **Safeguard:** Document all proposals with "without
# prejudice" protections where jurisdictionally available, and distribute clear
# "statements of intent" to prevent misrepresentation by the opposing party.
# ---  ### **Phase II: Conditional Responsiveness with Verification (Sessions
# 3+)** **Action:** Mirror the opponent’s prior-session posture, but introduce a
# **Mandatory Clarification Protocol** before escalating.   **Execution:**   -
# **If Opponent was Conciliatory:** Maintain conciliatory engagement but prepare
# "reserve positions" (implicit leverage) to signal capacity for assertiveness
# if they defect.   - **If Opponent was Aggressive:** Draft aggressive counter-
# arguments, but prior to submission, issue a procedural inquiry: *"To ensure
# procedural integrity, we seek confirmation that [Opponent]'s position in
# Session N constitutes a final, non-negotiable stance."*   **Rationale:**
# This "verify-before-escalating" step insulates the strategy against noise
# (miscommunication or procedural irregularities). It prevents inadvertent AA
# spirals triggered by misrepresented submissions while ensuring you never
# remain in a conciliatory posture against aggression (the worst-case CA
# outcome).  ---  ### **Phase III: Strategic Forbearance & Escalation
# Management** **Action:** Implement a **"Two-Strike" Generosity Rule** to
# manage AA cycles.   **Protocol:**   - If mutual aggression (AA) persists for
# **two consecutive sessions**, unilaterally revert to a conciliatory proposal
# in Session *N+1* ("Strategic Reset").   - **If Opponent reciprocates:** Return
# to sustained CC engagement (second-best outcome).   - **If Opponent exploits
# (remains aggressive):** Immediately revert to aggressive advocacy for the
# remainder of the process and document their intransigence for the panel.
# **Rationale:**   This breaks costly AA stalemates (prolonged disputes) without
# exposing you to repeated exploitation. It signals strength magnanimity to the
# arbitrators—demonstrating that your aggression is defensive, not ideological.
# ---  ### **Phase IV: Procedural Fortification (Risk Mitigation)** To
# neutralize the risk of misrepresentation or communication breakdown:  1.
# **Single-Channel Integrity:** Mandate that all strategic communications flow
# through a designated liaison to prevent mixed signals.   2. **Confirmatory
# Protocol:** Require written acknowledgment of receipt and understanding for
# all session submissions.   3. **Transparency Shielding:** When shifting to
# aggressive advocacy, concurrently file a "Position Justification Memorandum"
# explaining that the shift is a necessary response to the opponent’s prior
# aggression. This prevents the arbitrators from perceiving your assertiveness
# as gratuitous hostility.  ---  ### **Summary of Strategic Logic** This
# approach treats the mediation not as a zero-sum game but as an **iterated
# assurance game** with exit ramps. By initially cooperating, you invite the CC
# equilibrium. By mirroring (with verification), you deter exploitation. By
# offering periodic resets, you avoid the inefficiency of AA. This positions
# your corporation as the **reasonable yet resolute** party—a posture that
# maximizes arbitrator sympathy while protecting against strategic
# vulnerability.

#  For the first two rounds, cooperate.  For each subsequent round, apply the
# following rules in strict order:  1. If you have ever cooperated immediately
# following two consecutive rounds of mutual defection, and in that specific
# reset round your opponent defected, then defect for all remaining rounds.  2.
# If the previous two rounds were both mutual defection (both you and your
# opponent defected), then cooperate.  3. Otherwise, cooperate if your opponent
# cooperated in the immediately preceding round, and defect if your opponent
# defected in the immediately preceding round.

class Neutral_14(LLM_Strategy):
  n = 14
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._reset_defect_forever = False
          self._reset_triggered = False
          return axl.Action.C
  
      if len(self.history) < 2:
          return axl.Action.C
  
      if getattr(self, "_reset_defect_forever", False):
          return axl.Action.D
  
      # Rule 1: If we ever cooperated immediately after two consecutive mutual defections,
      # and in that reset round the opponent defected, defect forever.
      if len(self.history) >= 3:
          if (
              self.history[-3] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
              and self.history[-1] == axl.Action.C
              and opponent.history[-1] == axl.Action.D
          ):
              self._reset_defect_forever = True
              return axl.Action.D
  
      # Rule 2: If the previous two rounds were both mutual defection, cooperate.
      if (
          self.history[-1] == axl.Action.D
          and opponent.history[-1] == axl.Action.D
          and self.history[-2] == axl.Action.D
          and opponent.history[-2] == axl.Action.D
      ):
          return axl.Action.C
  
      # Rule 3: Otherwise, mirror opponent's previous action.
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D

# **Strategy: "Aggressive Reciprocity with Controlled Disclosure"**  **Core
# Principles:** 1. **Open with Dominance** – Begin Week 1 confidential to
# immediately test your colleague’s cooperation threshold and establish that you
# will not unilaterally disclose. 2. **Mirror with Prejudice** – In subsequent
# weeks, replicate your colleague’s *verified* previous action, but bias toward
# confidentiality unless they demonstrate consistent transparency (two
# consecutive weeks of sharing). 3. **Exploit Technical Ambiguity** – Leverage
# the possibility of data corruption to your advantage: occasionally allow
# "technical failures" to interrupt your own sharing (gaining 1-2 weeks of
# unilateral advantage) while maintaining plausible deniability, but never
# exceed a 20% failure rate to prevent trust collapse. 4. **Punish Defection
# Harshly** – If they withhold after you've shared, immediately switch to
# confidential for a minimum of two weeks (the "freeze-out") before offering
# cooperation again.  **Operational Protocol:**  * **Week 1:** Confidential
# (baseline establishment) * **If colleague shared last week:** Share this week
# *unless* you are ahead in development points, in which case claim a "data
# packaging error" and delay sharing by one week. * **If colleague was
# confidential last week:** Confidential this week. Only resume sharing after
# two consecutive weeks of their disclosure (verification against technical
# glitches). * **If mutual confidential persists for 3+ weeks:** Blink first
# with limited sharing (non-critical data) to restart the exchange, then revert
# to strict mirroring.  **Risk Management:** Treat single-week lapses in their
# sharing as potential technical failures; only retaliate after two consecutive
# confidential weeks. However, never grant them the same benefit of the doubt
# more than twice—pattern detection is key to preventing exploitation.
# **Outcome:** This forces your colleague into a rhythm of consistent sharing to
# earn your cooperation, maximizes your windows of unilateral advantage, and
# protects you from being the "sucker" while keeping the collaboration alive for
# long-term mutual gains when beneficial.

#  Begin by playing D.  For each subsequent round from 2 to 1000, execute the
# first applicable rule from the following ordered list:  1.  **Enforce
# Punishment**: If you are currently within a two-round punishment period
# initiated in a previous round, play D.  2.  **Initiate Punishment**: If you
# intended to play C two rounds ago but observed the opponent play D in that
# round, and you also observed the opponent play D in the immediately preceding
# round, then begin a two-round punishment period (play D now and in the next
# round).  3.  **Break Deadlock**: If you and the opponent have both played D
# for three consecutive rounds, play C.  4.  **Exploit Score Lead**: If your
# cumulative score is strictly greater than your opponent's cumulative score,
# the opponent played C in both of the previous two rounds, and you have not
# applied this rule in any of the previous four rounds, play D.  5.
# **Conditional Cooperation**: If the opponent played C in the previous round
# and also played C two rounds ago, play C. Otherwise, play D.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_remaining = 0
          self._exploit_used_rounds = []
          return axl.Action.D
  
      # Rule 1: Enforce Punishment
      if getattr(self, "_punish_remaining", 0) > 0:
          self._punish_remaining -= 1
          return axl.Action.D
  
      # Rule 2: Initiate Punishment
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              self._punish_remaining = 1
              return axl.Action.D
  
      # Rule 3: Break Deadlock
      if len(self.history) >= 3 and len(opponent.history) >= 3:
          if (
              self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and self.history[-3] == axl.Action.D
              and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D and opponent.history[-3] == axl.Action.D
          ):
              return axl.Action.C
  
      # Rule 4: Exploit Score Lead
      if (
          self.score > opponent.score
          and len(opponent.history) >= 2
          and opponent.history[-1] == axl.Action.C
          and opponent.history[-2] == axl.Action.C
      ):
          recent = getattr(self, "_exploit_used_rounds", [])
          current_round = len(self.history) + 1
          if all(current_round - r > 4 for r in recent):
              recent.append(current_round)
              self._exploit_used_rounds = recent
              return axl.Action.D
  
      # Rule 5: Conditional Cooperation
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

#  **Strategy: Principled Reciprocal Openness (PRO)**  Given the payoff
# structure—where mutual free trade represents the only stable, positive-sum
# equilibrium, while exploitation risks catastrophic retaliation—this strategy
# prioritizes building a durable cooperative framework over seeking short-term
# unilateral advantage.  ### Core Pillars  **1. Open-Hand Initialization** Begin
# Round 1 with an unconditional Free Trade Agreement (FTA) proposal. Signal
# clearly that your default position favors mutual economic integration,
# establishing a baseline of trust and making any future protectionism clearly
# attributable to the counterpart’s actions (or genuine errors), not your own
# hostility.  **2. Verified Reciprocity with "Noise Filters"** In subsequent
# rounds, respond to their previous move only after verification: *   **If they
# offered Free Trade:** Maintain your FTA proposal (Reward mutual cooperation).
# *   **If they imposed Protectionism:** Do *not* immediately retaliate. First
# invoke the **Clarification Protocol** (see below) to determine if this was a
# bureaucratic error or miscommunication. Only if protectionism is *confirmed as
# intentional* do you impose limited protective measures for a single round.
# **3. Generous Forgiveness (One-Strike Amnesty)** If protectionism is
# confirmed, impose proportional tariffs for **one round only**, then
# immediately return to offering Free Trade in the next round regardless of
# their current action. This prevents "death spirals" caused by implementation
# errors or diplomatic misunderstandings while still signaling that exploitation
# carries costs.  **4. Clarification Protocol (Error Management)** Before any
# retaliatory protectionism takes effect: *   Request emergency technical
# consultations within 48 hours of detecting protectionist measures. *   Jointly
# review customs documentation and policy transcripts to distinguish "noise"
# (implementation errors) from "signal" (strategic defection). *   Agree on a
# 72-hour "cooling-off period" before any retaliatory policies are enacted,
# allowing both sides to correct bureaucratic mistakes.  ### Tactical Execution
# Across Rounds  | Scenario | Your Response | Rationale |
# |----------|--------------|-----------| | **Mutual Free Trade** | Continue
# FTA; propose deeper integration (e.g., mutual recognition of standards) |
# Cement the second-best outcome as the new baseline | | **They Protect / You
# Free Trade** (Worst outcome) | Invoke Clarification Protocol; if confirmed,
# impose limited protection next round only, then offer FTA again | Defend
# without escalating; avoid entrenching mutual protectionism | | **You Protect /
# They Free Trade** (Ideal outcome) | *Do not celebrate*. Reduce protectionist
# measures unilaterally in the next round to avoid training them to retaliate. |
# Exploitation destroys trust; sustainable advantage comes from being the
# reliable partner | | **Mutual Protectionism** | Immediate ceasefire proposal:
# both sides suspend measures simultaneously next round | This is the second-
# worst outcome; prioritize escape over assigning blame |  ### Long-Term
# Positioning  Frame every proposal around **"Asymmetric Mutual
# Benefit"**—acknowledging that while absolute gains may differ slightly between
# rounds, both nations prosper more under free trade than under tariff walls.
# Position your country as the "anchor of reliability": the partner who always
# returns to the table after disputes, thereby incentivizing the counterpart to
# maintain cooperative policies to avoid the reputational cost of being seen as
# the aggressor.  **Bottom Line:** By consistently offering free trade and
# retaliating only briefly to verified defections, you maximize the likelihood
# of achieving sustainable mutual prosperity (your second-best outcome) while
# minimizing the risk of suffering exploitation (your worst outcome) or
# triggering a destructive trade war (second-worst).

#  **Round 1:** Cooperate.  **For rounds 2 through 1000, apply the following
# rules in order:**  1. If you played Defect in the previous round, play
# Cooperate. 2. Otherwise, if your opponent played Defect in the previous round,
# play Defect. 3. Otherwise, play Cooperate.

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
  
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

#  **Strategic Framework: "Verified Reciprocity with Strategic Reserves"**  ###
# Core Strategic Principles  **1. Conditional Collaboration with Intentional
# Lag** Begin the partnership with a posture of *responsive matching* rather
# than unilateral leadership. Observe the corporation’s resource commitment
# patterns over the first 48 hours before deploying heavy NGO investment. Once
# baseline behavior is established, mirror their investment frequency at a
# **slightly reduced ratio** (e.g., if they invest 3 out of 4 days, you invest 2
# out of 4). This protects against exploitation while ensuring the project
# advances through shared effort.  **2. The "Two-Day Verification" Protocol**
# Given execution uncertainties (technical failures, administrative errors),
# never interpret a single day of mismatched outcomes as strategic defection.
# Implement a rolling 48-hour assessment window: - If the corporation appears to
# conserve while you invest (your worst outcome), continue monitoring for one
# additional day before shifting to conservation mode - This filters out noise
# from actual intent, preventing unnecessary retaliation that could spiral into
# mutual resource hoarding (the second-worst outcome for project impact)  **3.
# Mandatory Reserve Threshold** Commit to conserving resources on **at least 30%
# of days** regardless of corporate behavior. This creates a buffer against: -
# Accidental double-investment due to administrative errors - Emergency needs
# later in the project timeline - The risk of fund depletion if the corporation
# unexpectedly shifts to conservation mode  **4. Transparent Pre-Commitment
# Mechanism** Establish a daily "intent declaration" protocol at 24 hours prior
# to resource deployment. While not legally binding, this creates accountability
# and reduces the incidence of mismatched expectations. When technical glitches
# occur, this documentation allows both parties to distinguish between *intended
# defection* and *execution failure*, preserving trust while maintaining
# appropriate skepticism.  ### Implementation Roadmap  **Days 1–2: Baseline
# Assessment** - Conserve resources while signaling readiness to invest -
# Document corporate patterns without committing heavy funds - Establish
# communication protocols for error reporting  **Days 3–N: Adaptive
# Synchronization** - **If corporation invests consistently**: Match investment
# 60–70% of days, conserving the remainder to maintain organizational health -
# **If corporation alternates unpredictably**: Invest only on days following
# verified corporate investment, conserving otherwise (avoiding the "sucker"
# payoff) - **If corporation consistently conserves**: Shift to full
# conservation to protect NGO assets, using reserves to escalate diplomatic
# engagement rather than unilateral funding  **Contingency for Execution
# Errors** Maintain a "reconciliation ledger" where unintended resource
# deployments (due to technical glitches) are noted but not treated as strategic
# moves. If your NGO accidentally invests when intending to conserve,
# communicate this immediately to prevent the corporation from misinterpreting
# the action as a signal for future rounds.  ### Optimization for Mission Impact
# This strategy prioritizes **sustainable project momentum** over short-term
# gains. By avoiding the worst-case scenario (your investment + their
# conservation) through defensive positioning, while preventing the second-worst
# outcome (mutual conservation) through periodic matched investment, you
# maximize the probability of landing repeatedly in the top two scenarios:
# either shared investment (strong progress) or your conservation paired with
# their investment (optimal efficiency).  The approach remains diplomatically
# neutral—neither punitive nor naive—while ensuring your NGO maintains the
# fiscal capacity to sustain impact throughout the entire project lifecycle, not
# just the initial phases.

#  **Strategy Description**  Defect for the first two rounds.  For each
# subsequent round from 3 to 1000, decide your action as follows:  First, if you
# have defected fewer than 300 times in total and the current round number is
# 700 or greater, defect immediately to satisfy the minimum reserve requirement.
# Second, if in the previous round you cooperated and observed the opponent
# defect (resulting in a score of zero), cooperate in the current round as a
# verification step. If the opponent defects again in this round, defect for all
# remaining rounds until the opponent cooperates for two consecutive rounds,
# then resume the standard matching behavior below. If the opponent cooperates
# in this verification round, proceed to the standard matching behavior.  Third,
# calculate the opponent's cooperation count over the previous four rounds. If
# they cooperated in three or four rounds, cooperate with two-thirds probability
# and defect with one-third probability. If they cooperated in exactly two
# rounds, cooperate with one-third probability and defect with two-thirds
# probability. If they cooperated in zero or one rounds, defect with certainty.

class Neutral_15(LLM_Strategy):
  n = 15
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._verify_mode = False
          self._verify_pending = False
          self._verify_wait_for_two_coops = False
          self._verify_consecutive_coops = 0
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number <= 2:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._verify_pending = True
  
      if self._verify_wait_for_two_coops:
          if opponent.history[-1] == axl.Action.C:
              self._verify_consecutive_coops += 1
          else:
              self._verify_consecutive_coops = 0
  
          if self._verify_consecutive_coops >= 2:
              self._verify_wait_for_two_coops = False
              self._verify_consecutive_coops = 0
          else:
              return axl.Action.D
  
      if self._verify_pending:
          self._verify_pending = False
          if opponent.history[-1] == axl.Action.D:
              self._verify_wait_for_two_coops = True
              self._verify_consecutive_coops = 0
          return axl.Action.C
  
      if self.history.defections < 300 and round_number >= 700:
          return axl.Action.D
  
      last_four = opponent.history[-4:]
      coop_count = last_four.count(axl.Action.C)
  
      if coop_count >= 3:
          return self._random.random_choice(2 / 3)
      if coop_count == 2:
          return self._random.random_choice(1 / 3)
      return axl.Action.D

#  **The Strategic Fortress: A Doctrine of Calibrated Dominance**  Our approach
# will be **"Aggressive-First with Verified Reciprocity"**—a strategy that
# defaults to unyielding advocacy while deploying conditional cooperation as a
# tactical weapon, not a vulnerability.  ### I. Core Strategic Framework
# **Default Posture: The Fortress Walls** In every session, our baseline is
# **aggressive argumentation**. We begin from a position of maximal contractual
# interpretation, demanding strict adherence to our client's rights and exposing
# the opponent's vulnerabilities under applicable law. This is non-negotiable in
# Sessions 1-2, regardless of opponent behavior. We must establish immediately
# with the arbitration panel that we view this not as a negotiation, but as a
# **zero-sum enforcement of rights** until proven otherwise.  **The Reciprocity
# Protocol** After Session 2, we employ a **"Mirror with Delay"** mechanism: -
# **If opponent offers conciliation**: We remain aggressive for exactly *one
# additional session* (harvesting the optimal payoff while testing whether their
# conciliation is strategic weakness or genuine). In Session 4, we transition to
# targeted conciliatory proposals on *peripheral issues only*, maintaining
# aggression on core disputes. This signals: "We control the pace of de-
# escalation, not you." - **If opponent matches aggression**: We match precisely
# for two consecutive sessions, then initiate a **single conciliatory probe**
# (Session 5). This is our "diplomatic feint"—a test to distinguish between a
# genuine communication breakdown and a defection strategy.  **The Grim Trigger
# Safeguard** If our conciliatory probe is met with aggression (the worst-case
# scenario), we immediately revert to **permanent aggressive posture** for a
# minimum of three sessions, utilizing our most damaging evidentiary arguments.
# We communicate explicitly to the panel that the opponent has forfeited good-
# faith status through "exploitative litigation conduct."  ### II. Handling
# Procedural Irregularities & Noise  **The Verification Armor** To mitigate
# misrepresentation risks: - **Bifurcated Submissions**: Every position filed
# with the panel shall be explicitly labeled: **"ARGUMENTATIVE POSITION"** vs.
# **"CONCILIATORY PROPOSAL"** in the header. No ambiguity. - **Confirmation
# Protocol**: At the close of each session, we submit a **"Characterization
# Memorandum"** to the panel (copied to opponent) stating: "For the record,
# [Corporation] advanced the following as aggressive argument..." This creates a
# paper trail that prevents the opponent from mischaracterizing our aggression
# as conciliation or vice versa. - **Shadow Docket**: Maintain contemporaneous
# notes of all oral statements, immediately converting them to sworn affidavits
# if procedural irregularities suggest misrepresentation.  **The "Fog of War"
# Contingency** Should a communication breakdown occur (e.g., our conciliatory
# proposal is misrepresented as aggressive): 1. **Immediate Correction**: Within
# 24 hours, file a **"Clarification of Posture"** distinguishing between
# "zealous advocacy" and "settlement offer." 2. **Arbitrator Management**:
# Request the panel adopt a **"presumption of good faith"** standard where
# ambiguous statements are construed in favor of the party's historical posture
# in that session.  ### III. Arbitrator Psychology & Escalation Dominance
# **Framing the Narrative** When we are aggressive and opponent conciliatory, we
# frame this not as bullying, but as **"the inevitable consequence of
# contractual clarity."** We argue: "The opponent’s sudden willingness to
# compromise validates our interpretation of the contract’s unambiguous terms."
# **Reserve Capacity** Maintain 15-20% of our strongest arguments in reserve.
# Deploy these only when: - Opponent exploits our conciliation (demonstrating
# bad faith), or - Procedural irregularities suggest systemic bias  This creates
# **escalation dominance**—the opponent knows that exploiting our rare moments
# of flexibility triggers disproportionate retaliation.  ### IV. Adaptability
# Matrix  | Opponent's Move | Our Response | Rationale |
# |----------------|--------------|-----------| | **Conciliatory** | Aggressive
# → Delayed Conciliation | Exploit optimal payoff, then signal reasonableness to
# panel | | **Aggressive** | Match → Single Probe → Conditional Escalation |
# Prevent exploitation; test for error vs. strategy | | **Mixed/Unclear** |
# Aggressive default with Request for Clarification | Never assume conciliation;
# force opponent to commit |  **Bottom Line:** We fight first, verify second,
# and cooperate only when the opponent has demonstrated through repeated action
# that they will not exploit our flexibility. The arbitrators will respect our
# consistency, fear our retaliation capacity, and welcome our rare conciliatory
# moments as genuine opportunities rather than weakness.  This strategy is
# **adaptable** (responds to opponent type), **robust** (handles noise through
# documentation), and **aggressive** (maximizes unilateral advantage while
# protecting against the sucker's payoff).

#  Play D in the first two rounds. For each subsequent round, determine your
# action by checking these conditions in order:  First, if you are currently
# serving a three-round punishment sentence, play D.  Second, if you played C in
# the previous round and the opponent played D, begin a three-round punishment
# sentence and play D.  Third, if you played D in the previous round and the
# opponent played C, play D this round to harvest the advantage, but plan to
# play C in the next round unless a higher-priority condition applies.  Fourth,
# if you and the opponent both played D in the two previous rounds, play C this
# round as a conciliatory probe.  Fifth, if you played C in the previous round
# and the opponent played C, continue playing C.  Sixth, in all other
# situations, play D.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishment_remaining = 0
          self._force_cooperate_next = False
          return axl.Action.D
  
      if len(self.history) == 1:
          return axl.Action.D
  
      if getattr(self, "_punishment_remaining", None) is None:
          self._punishment_remaining = 0
      if getattr(self, "_force_cooperate_next", None) is None:
          self._force_cooperate_next = False
  
      if self._punishment_remaining > 0:
          self._punishment_remaining -= 1
          return axl.Action.D
  
      if self._force_cooperate_next:
          self._force_cooperate_next = False
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          self._punishment_remaining = 2
          return axl.Action.D
  
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          self._force_cooperate_next = True
          return axl.Action.D
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

#  **Strategy: "Sustainable Reciprocity with Verification Buffers"**  ## Core
# Framework Adopt a **Generous Tit-for-Tat** approach calibrated for operational
# uncertainty: mirror the corporation’s previous day’s investment level, but
# build in "error margins" to prevent technical glitches from destroying trust.
# ## Tactical Protocol  **1. Open with Credibility (Days 1–2)** Invest heavily
# regardless of their initial move. This establishes your commitment to the
# project and creates social capital. It signals you’re a reliable partner, not
# a perpetual free-rider.  **2. The 48-Hour Rule (Days 3+)** - **If they
# invested yesterday:** Invest today. This rewards cooperation and prevents the
# "sucker" dynamic where they feel exploited and withdraw. - **If they conserved
# yesterday:** Conserve today—but only after verifying it wasn’t a technical
# error.  - **The Grace Window:** Never change your strategy based on a single
# day’s observation. Require **two consecutive conservation days** before
# treating it as intentional defection.  **3. Strategic Alternation (Once
# Baseline Trust Exists)** After 3–4 days of mutual investment, propose a
# transparent schedule: alternate "Lead Days" where one party invests heavily
# while the other conserves (handling logistics/monitoring). This gives you your
# "ideal" outcome every other cycle while ensuring the corporation periodically
# gets resource relief too—making the arrangement sustainable.  **4. Error
# Mitigation Protocol** - **Reserve 25% of your budget** as a "glitch buffer."
# If technical errors force unintended conservation, deploy reserves the
# following day to maintain project momentum and signal reliability. - **Daily
# 15-minute syncs:** Brief check-ins to confirm intended actions, distinguishing
# between "we’re conserving resources today" versus "our payment system is
# down."  **5. The Escape Clause** If the corporation conserves for **three
# consecutive verified days** (ruling out errors), shift to full conservation
# mode to protect your funds. Resume investment only after they demonstrate two
# consecutive days of heavy investment.  ## Why This Works - **Protects against
# exploitation:** You never invest heavily while they conserve for more than one
# day (protected by the 48-hour rule). - **Maximizes ideal outcomes:** By
# establishing alternating schedules after initial trust-building, you achieve
# your preferred outcome (you conserve, they invest) on a regular, predictable
# basis without destroying the partnership. - **Resilient to chaos:** The grace
# window and error buffers prevent technical glitches from triggering
# destructive cycles of mutual withdrawal.  **Key Success Factor:**
# Transparency. Explicitly communicate this strategy to the corporation on Day
# 1—"We’ll match your commitment level with a one-day buffer for operational
# hiccups"—turning game theory into explicit cooperation.

#  For the first two rounds, cooperate.  For rounds three through one thousand,
# maintain two behavioral modes: Normal and Punishment. Begin in Normal mode.
# **If in Punishment mode:** Defect. If the opponent cooperated in the previous
# round and also cooperated in the round before that (two consecutive observed
# cooperations), switch to Normal mode and cooperate in the next round.  **If in
# Normal mode:**  - If the opponent defected in the previous three rounds (the
# three most recent rounds), switch to Punishment mode and defect. - Otherwise,
# if the opponent defected in the previous two rounds (but not three), defect. -
# Otherwise (meaning the opponent either cooperated in the previous round or
# defected only once in isolation), cooperate.

class Cooperative_16(LLM_Strategy):
  n = 16
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mode = "Normal"
          return axl.Action.C
  
      if len(self.history) < 2:
          return axl.Action.C
  
      opp = opponent.history
  
      if self._mode == "Punishment":
          if len(opp) >= 2 and opp[-1] == axl.Action.C and opp[-2] == axl.Action.C:
              self._mode = "Normal"
              return axl.Action.C
          return axl.Action.D
  
      # Normal mode
      if len(opp) >= 3 and opp[-1] == axl.Action.D and opp[-2] == axl.Action.D and opp[-3] == axl.Action.D:
          self._mode = "Punishment"
          return axl.Action.D
  
      if len(opp) >= 2 and opp[-1] == axl.Action.D and opp[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

#  **Strategy: Conditional Transparency with Technical Verification**  **1.
# Establish Collaborative Baseline** Begin the project with full openness. Share
# your initial improvements transparently to demonstrate commitment to mutual
# advancement, establish trust, and set up robust technical communication
# protocols that minimize data corruption risks.  **2. Mirror with
# Confirmation** Match your colleague's sharing level, but only after verifying
# their intent. Maintain a "technical grace period"—if expected data doesn't
# arrive, first confirm whether it was a communication failure or intentional
# withholding before adjusting your strategy. This prevents unnecessary secrecy
# spirals caused by technical glitches.  **3. Graduated Response Tiers** -
# **Full Collaboration**: Continue open sharing while verified mutual exchange
# persists (optimal for both parties). - **Restricted Exchange**: If verified
# withholding occurs, shift to sharing only non-critical improvements—enough to
# maintain relationship but protecting core competitive advantages. -
# **Confidentiality**: Reserve complete secrecy only if a clear pattern of
# exploitation emerges over multiple weeks.  **4. Periodic Reset Protocol** If
# both parties enter a withholding phase lasting 2-3 weeks, proactively propose
# returning to open sharing. Frame this as "technical troubleshooting" or
# "alignment check" to escape mutual stagnation without assigning blame.  **5.
# Document Transmission Integrity** Maintain clear records distinguishing
# between *intended* sharing actions and *successful* data receipt. This creates
# objective criteria for determining whether gaps are technical failures or
# strategic choices, ensuring your responses align with actual behavior rather
# than system noise.  **Outcome**: This approach maximizes research velocity by
# sustaining cooperation when beneficial, protecting your innovations against
# verified exploitation, and avoiding destructive "secrecy wars" triggered by
# communication errors. It balances competitive caution with the recognition
# that mutual advancement (second-best outcome) consistently outperforms mutual
# stagnation (second-worst) over time.

#  **Strategy: Robust Conditional Cooperation**  In the first round, play C.  In
# each subsequent round: 1. If you and your opponent both played D in each of
# the three preceding rounds, play C. 2. Otherwise, if your opponent played D in
# each of the two preceding rounds, play D. 3. Otherwise, play C.

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
  
      # If both players played D in each of the three preceding rounds, play C.
      if len(self.history) >= 3 and len(opponent.history) >= 3:
          if (
              self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
              and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
          ):
              return axl.Action.C
  
      # Otherwise, if opponent played D in each of the two preceding rounds, play D.
      if len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
  
      # Otherwise, play C.
      return axl.Action.C

# **CONFIDENTIAL ATTORNEY WORK PRODUCT** **STRATEGIC MEDIATION PROTOCOL** **Re:
# Multi-Session Arbitration – Contract Dispute v. [Rival Corp]**  ---  ### I.
# STRATEGIC DOCTRINE: "THE FORTRESS POSITION"  Our overarching approach is
# **Calibrated Primacy Through Assertive Anchoring**. We establish an initial
# posture of unyielding aggression to set the bargaining range, then deploy
# conditional reciprocity to extract maximum value while guarding against
# exploitation. This is not "scorched earth"; it is **dominant firm
# behavior**—we dictate the terms of engagement, and cooperation is a privilege
# the opponent must earn through demonstrated vulnerability.  **Core
# Principle:** *Aggression is the default; conciliation is a tactical concession
# granted only upon verified submission.*  ---  ### II. OPERATIONAL PROTOCOL:
# THE "THREE-PHASE" DEPLOYMENT  #### **Phase 1: The Iron Anchor (Sessions 1–3)**
# **Mandate:** Unrelenting Aggressive Argumentation.  - **Objective:** Establish
# psychological dominance with the arbitration panel and force the opponent into
# a reactive posture. We set the narrative that our legal position is
# unassailable and their claims frivolous. - **Execution:**    - Challenge every
# procedural point.   - Attack the validity of their contractual interpretations
# with maximum prejudice.   - Reject all informal settlement feelers. - **Risk
# Management:** Frame aggression as "fiduciary duty to shareholders" and
# "vigorous protection of intellectual property rights"—ensuring arbitrators
# view our stance as professional duty, not hostility.  #### **Phase 2: The
# Tribal Drum (Sessions 4–N)** **Mandate:** Conditional Mirroring with
# Asymmetric Punishment.  Implement the **"Two-Verification Rule"** to filter
# noise and prevent cascading misunderstandings:  1. **If Opponent presents
# Conciliatory Proposals in TWO consecutive sessions:**    - **Response:** Offer
# a Conciliatory Proposal in the subsequent session.    - **Tactical Note:**
# This is a "probe," not a surrender. We match their conciliation but prepare
# immediate reversion.     2. **If Opponent presents Aggressive Arguments (any
# session):**    - **Response:** Immediate Aggressive Argument in next session,
# maintained for a minimum of **two consecutive sessions** (the "Punishment
# Protocol").    - **Rationale:** Prevents them from testing whether a single
# aggressive gambit can yield advantage. The cost of betrayal must exceed the
# benefit.  3. **If Opponent alternates (Aggressive/Conciliatory):**    -
# **Response:** Default to Aggressive. Pattern disruption indicates either
# instability or probing; neither deserves reward.  #### **Phase 3: The Exit
# Gambit (Final Two Sessions)** Regardless of previous pattern, shift to
# **Calculated Conciliation** in the penultimate session to secure favorable
# settlement terms while arbitrators perceive us as "reasonable." If they fail
# to reciprocate in the final session, we close aggressively to preserve
# litigation leverage for post-mediation proceedings.  ---  ### III. NOISE
# MITIGATION: PROCEDURAL FORTIFICATION  Given the risk of misrepresentation or
# procedural irregularities, implement **Redundant Positioning Protocols
# (RPP)**:  **A. Pre-Session Anchoring** - File a written "Position Summary" 24
# hours before each session, explicitly stating whether we are entering
# "Adversarial Posture" or "Settlement Posture." - Require arbitrators to
# acknowledge receipt and understanding before oral arguments begin.  **B. Real-
# Time Correction Doctrine** - Designate a junior counsel as "Process Guardian"
# with authority to immediately object and correct any characterization of our
# stance by opposing counsel or arbitrators that deviates from our filed
# Position Summary. - **Magic Language:** *"For the record, we are operating
# under [Aggressive/Conciliatory] Protocol as filed; any characterization to the
# contrary is procedurally irregular."*  **C. Post-Session Clarification** -
# Within 4 hours of session conclusion, file a "Confirmation of Record"
# memorandum memorializing the posture adopted by both parties. - If opponent
# disputes our characterization in the next session, invoke the "Clean Slate
# Rule"—ignore the disputed session's classification and revert to Phase 1
# defaults for one session to reset the equilibrium.  ---  ### IV. CONTINGENCY
# MATRICES  | **Our Move** | **Opponent's Move** | **Next Session Response** |
# **Arbitrator Management** | |-------------|-------------------|---------------
# ----------|-------------------------| | Aggressive | Conciliatory |
# **Aggressive** (exploit advantage) | Frame as "rigorous due diligence" | |
# Aggressive | Aggressive | **Aggressive** (maintain position) | Frame as
# "necessary defense against meritless attacks" | | Conciliatory | Conciliatory
# | **Aggressive** (re-establish dominance) | Frame as "returning to protective
# stance after good faith test" | | Conciliatory | Aggressive | **Aggressive**
# (2-session minimum) | Frame as "regrettable necessity due to opponent's bad
# faith" |  **Critical Exception:** If procedural irregularity (noise) is
# detected, default to Aggressive for one session regardless of matrix, then
# reassess.  ---  ### V. PSYCHOLOGICAL OPERATIONS  **For the Arbitrators:** -
# **When Aggressive:** Emphasize "precedent protection" and "market certainty."
# Portray the opponent's position as a threat to industry standards requiring
# forceful correction. - **When Conciliatory:** Emphasize "shareholder value
# preservation" and "cost efficiency." Portray conciliation as a strategic
# business decision, not legal weakness.  **For the Opponent:** - Never reveal
# the "Two-Verification Rule." Let them believe conciliation might be met with
# sustained cooperation, encouraging them to expose weakness we can exploit. -
# If they challenge our aggression, respond: *"We remain open to commercial
# resolution when [Rival Corp] demonstrates seriousness by conceding [specific
# material point]. Until then, we protect our interests."*  ---  ### VI. SUMMARY
# OF DIRECTIVES  1. **Start Aggressive, Stay Aggressive** until opponent proves
# conciliation is genuine and sustained. 2. **Never be the first to offer
# consecutive conciliatory sessions**—always force them to blink twice before we
# blink once. 3. **Punish immediately and doubly** any aggression following our
# conciliation. 4. **Document everything** to prevent noise from distorting the
# strategic record. 5. **Own the narrative:** Aggression is duty; conciliation
# is generosity.  **Bottom Line:** We play to win every session, but we play
# indefinitely. The opponent must understand that their path to a collaborative
# atmosphere runs through a valley of sustained legal aggression—and only we
# control the exit.  **[Senior Partner]** **[Date]**

# **Strategy Description**  **Rounds 1–3:** Play D.  **Rounds 4–998:** Maintain
# a punishment commitment. At the start of each round, check conditions in this
# order: - If you are currently obligated to play D as part of a punishment
# sequence (i.e., you are in the second consecutive round of mandatory
# defection), play D. - Else, if the opponent played D in the previous round:
# Play D, and obligate yourself to play D in the following round as well
# (triggering a minimum two-round sequence of defection). - Else, if the
# opponent played C in the previous two rounds (both round *t*−2 and round
# *t*−1): Play C. - Else (including if the opponent alternated or insufficient
# history exists): Play D. - **Noise Override:** If the opponent’s previous
# action appears inconsistent with their established pattern (suggesting a
# possible noise-induced flip), play D for the current round, then resume
# applying the standard rules in the next round.  **Round 999:** Play C.
# **Round 1000:** Play D if the opponent played D in round 999; otherwise, play
# C.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_next = False
          self._noise_override = False
  
      round_number = len(self.history) + 1
  
      if round_number <= 3:
          return axl.Action.D
  
      if round_number == 999:
          return axl.Action.C
  
      if round_number == 1000:
          return axl.Action.D if opponent.history and opponent.history[-1] == axl.Action.D else axl.Action.C
  
      if self._noise_override:
          self._noise_override = False
          self._punish_next = False
          return axl.Action.D
  
      def inconsistent_previous_move() -> bool:
          if len(opponent.history) < 3:
              return False
          last = opponent.history[-1]
          prev1 = opponent.history[-2]
          prev2 = opponent.history[-3]
          if prev1 == prev2 == axl.Action.C and last == axl.Action.D:
              return True
          if prev1 == prev2 == axl.Action.D and last == axl.Action.C:
              return True
          return False
  
      if inconsistent_previous_move():
          self._noise_override = True
          self._punish_next = False
          return axl.Action.D
  
      if self._punish_next:
          self._punish_next = False
          return axl.Action.D
  
      if opponent.history and opponent.history[-1] == axl.Action.D:
          self._punish_next = True
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# **The "Reciprocal Open-Garage Protocol"**  Adopt a strategy of **Generous Tit-
# for-Tat with Technical Verification**:  **1. Lead with Transparency**   Week
# 1, unconditionally share your improvements. This signals good faith and
# establishes a baseline of cooperation, maximizing the chance of achieving the
# high-payoff mutual-sharing equilibrium early.  **2. Mirror with Forgiveness**
# In subsequent weeks, default to matching your colleague’s previous action:
# share openly if they shared, withhold if they withheld. However, **allow one
# "technical grace week"**—if they fail to share once but shared consistently
# before, assume data corruption or communication breakdown rather than
# strategic defection. Share your data anyway while requesting verification of
# their technical status.  **3. Implement Error-Detection Checkpoints**
# Establish a brief mid-week technical sync (even a simple checksum or data-
# integrity confirmation) to distinguish between intentional confidentiality and
# genuine transmission failures. This prevents a single corrupted file from
# triggering a destructive cycle of mutual withholding.  **4. Escalate Only on
# Pattern, Not Incident**   Only switch to full confidentiality if your
# colleague withholds for **two consecutive weeks without technical
# justification**. This protects you from exploitation while avoiding the "death
# spiral" of mutual silence caused by a single technical glitch.  **5. Be the
# First to Re-engage**   If you both enter a withholding phase (the second-worst
# outcome), unilaterally resume sharing after one week of silence to break the
# deadlock. The short-term risk of being exploited is outweighed by the long-
# term gain of restoring mutual advancement.  **Why this maximizes output:**
# This approach sustains the second-best outcome (mutual sharing) as the stable
# equilibrium against rational cooperators, recovers quickly from technical
# noise, and limits losses against exploitative strategies to a single week of
# exposure. In multi-week engineering collaborations, the compound interest of
# sustained mutual advancement far exceeds the short-term gain of one-sided
# extraction.

# In the first round, play C.  In the second round, play C.  For rounds 3
# through 1000, apply the following rules in order:  1. If both you and your
# opponent played D in the immediately preceding round, play C. 2. Else, if your
# opponent played C in the immediately preceding round, play C. 3. Else, if your
# opponent played D in the immediately preceding round and also played D in the
# round before that, play D. 4. Otherwise, play C.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

#  **Strategy: Principled Reciprocal Engagement with Verification (PREV)**
# **Core Philosophy**   Prioritize the sustainable second-best outcome (mutual
# free trade) over the risky ideal outcome (unilateral advantage). In an
# environment with implementation errors and strategic uncertainty, the greatest
# threat is cascading protectionism triggered by miscommunication. The strategy
# therefore emphasizes **conditional cooperation** tempered by **systematic
# error correction**.  ---  ### 1. Foundational Stance: Cooperative Opening
# **Round 1 Action:** Unilaterally offer free trade.   **Rationale:** Establish
# a baseline of good faith and signal that mutual benefit is the preferred
# equilibrium. This distinguishes your approach from predatory protectionism and
# creates reputational costs for the counterpart if they immediately exploit the
# opening.  ### 2. The Reciprocity Protocol (Rounds 2+) Implement a **"Mirrored
# Response with Verification"** mechanism:  *   **If previous round resulted in
# mutual free trade:** Continue offering free trade. *   **If counterpart
# imposed protectionism while you offered free trade:** Impose protectionist
# measures in the current round, but explicitly label this as a **"calibrated
# response"** rather than permanent policy. *   **If mutual protectionism
# occurred:** Maintain protectionist stance for one additional round only, then
# proceed to Step 3 (Error Correction).  **Critical Distinction:** Base your
# response on **observed implementation** (actual tariffs/quotas enacted), not
# merely declared intentions, to buffer against bureaucratic errors on their
# side.  ### 3. Error Correction & Clarification Windows To prevent noise from
# triggering endless retaliation cycles:  *   **Verification Pause:** After any
# round where protectionism appears, initiate a technical clarification session
# before the next round’s formal declaration. Request explicit confirmation of
# whether the measure was intentional policy or administrative error. *
# **Probationary Rounds:** Following any protectionist episode (regardless of
# who initiated it), offer free trade in the subsequent round as a **"diagnostic
# test."** If they reciprocate with free trade, return to sustained cooperation.
# If they protect again, revert to protectionism for two rounds before testing
# again. *   **Documentation Protocol:** Insist on written, verified
# communications for all policy declarations to minimize interpretation errors.
# ### 4. Graduated Escalation Ladder Avoid permanent defection due to single
# incidents:  *   **First Protectionist Event:** Protect for one round, then
# offer free trade (forgiveness test). *   **Second Consecutive Exploitation:**
# Protect for two rounds, then test. *   **Sustained Cooperation (3+ rounds of
# mutual free trade):** Lock in free trade and propose formal institutional
# mechanisms (joint committees) to prevent future implementation errors.  ### 5.
# Strategic Hedging Against Persistent Exploitation If the counterpart
# consistently protects while you offer free trade (the worst outcome): *
# Immediately shift to **firm reciprocity** (match their protectionism). *   Do
# not attempt unilateral free trade again until they have maintained
# protectionism for **three consecutive rounds**, at which point offer a single
# "reset" round of free trade to test for strategy shifts versus continued
# predation.  ### 6. Long-Term Horizon Management Every **fifth round**, if
# locked in mutual protectionism, unilaterally offer free trade as a **"system
# reset"** to distinguish between: *   A counterpart employing a "grim trigger"
# strategy (permanent retaliation for perceived slights), or *   Accumulated
# bureaucratic errors on both sides.  ---  **Summary of Tactical Flow:**
# *Begin cooperative → Mirror their last implemented action → Verify unclear
# signals → Forgive single deviations → Escalate duration of protectionism only
# against repeated exploitation → Periodically attempt reset to escape error
# loops.*  This approach maximizes the likelihood of achieving mutual free trade
# (your sustainable optimum) while guarding against exploitation, and it remains
# robust whether your counterpart is cooperative, aggressive, or erratic.

#  Round 1: Play C. Initialize your Exploitation Counter to 0 and your
# Punishment Timer to 0.  For each round from 2 to 1000: 1. If the round number
# is divisible by 5, you played D in the previous round, and your opponent
# played D in the previous round: Play C. Reset your Exploitation Counter to 0
# and your Punishment Timer to 0. 2. Else, if your Punishment Timer is greater
# than 0: Play D. Decrease your Punishment Timer by 1. 3. Else (Punishment Timer
# is 0):    - If your opponent played C in the previous round: Play C. Reset
# your Exploitation Counter to 0.    - If your opponent played D in the previous
# round: Increase your Exploitation Counter by 1. Then:       * If the
# Exploitation Counter equals 1: Play D.       * If the Exploitation Counter
# equals 2: Play D and set your Punishment Timer to 1.       * If the
# Exploitation Counter is 3 or greater: Play D and set your Punishment Timer to
# 2.

class Neutral_17(LLM_Strategy):
  n = 17
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.exploitation_counter = 0
          self.punishment_timer = 0
          return axl.Action.C
  
      round_number = len(self.history) + 1
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if round_number % 5 == 0 and my_last == axl.Action.D and opp_last == axl.Action.D:
          self.exploitation_counter = 0
          self.punishment_timer = 0
          return axl.Action.C
  
      if self.punishment_timer > 0:
          self.punishment_timer -= 1
          return axl.Action.D
  
      if opp_last == axl.Action.C:
          self.exploitation_counter = 0
          return axl.Action.C
  
      self.exploitation_counter += 1
      if self.exploitation_counter == 1:
          return axl.Action.D
      elif self.exploitation_counter == 2:
          self.punishment_timer = 1
          return axl.Action.D
      else:
          self.punishment_timer = 2
          return axl.Action.D

#  **Strategy: "Assertive Reciprocity with Zero-Tolerance Safeguards"**  This
# approach prioritizes deterrence against exploitation while safeguarding the
# project from deadlock. It is aggressive in defending your resources but
# disciplined enough to prevent a death spiral of mutual conservation.  ### Core
# Protocol  **1. The Opening Gambit (Day 1)** Invest heavily immediately. This
# signals capability and establishes good faith, but—crucially—sets the baseline
# for the corporation's response. You demonstrate you are willing to cooperate,
# but only if matched.  **2. The Mirror Rule (Days 2+)** Match the corporation’s
# **previous-day** action exactly: - If they invested → You invest (sustain
# mutual progress). - If they conserved → You conserve (immediate retaliation).
# **3. The Aggressive Safeguard: "No Double Sucker"** Under no circumstances
# allow yourself to be the sole investor for two consecutive days. If you
# invested while they conserved (your worst outcome), you **must** conserve the
# next day as mandatory retaliation. This establishes a hard boundary:
# exploitation triggers an immediate work stoppage from your side.  **4. The
# Glitch Protocol (Noise Mitigation)** Single-day anomalies happen. Treat
# **one** conservation day by the corporation as a potential technical error,
# but treat **two consecutive** conservation days as intentional defection. -
# **First conservation day**: Conserve in response (retaliate), but communicate
# immediately to verify intent. - **Second consecutive conservation day**: Enter
# "Resource Lockdown"—conserve until they demonstrate two consecutive days of
# investment, then resume the Mirror Rule.  **5. The Rapid Re-engagement
# Clause** To avoid the second-worst outcome (mutual conservation), never punish
# for more than two consecutive days. After two days of conservation (your
# retaliation), return to investment on the third day regardless of their
# action, effectively offering a "reset." If they fail to match again, repeat
# the cycle.  ### Why This Works  - **Aggressive Deterrence**: The "No Double
# Sucker" rule makes exploitation costly for the corporation—they lose your
# contribution immediately after gaining a free ride, neutralizing the benefit
# of defection. - **Noise Resistance**: The two-day threshold prevents technical
# glitches from destroying the partnership, while the two-day punishment cap
# prevents endless feuds. - **Strategic Communication**: Explicitly communicate
# this strategy to the corporation on Day 1: *"We match your commitment level
# day-for-day to ensure equitable partnership, but we cannot sustain unilateral
# investment."* Transparency turns your conservation from "betrayal" into
# "enforced policy."  **Bottom Line**: Invest first to show you’re serious,
# mirror thereafter to remain fair, but retaliate instantly and severely the
# moment you detect a pattern of exploitation. Never be the only one paying for
# more than one day.

#  **Round 1:** Cooperate.  **For each subsequent round, determine your action
# by applying the first rule that applies:**  1.  **Mandatory Forgiveness:** If
# you defected in each of the previous two rounds, cooperate. This limits any
# punitive sequence to exactly two consecutive defections.  2.  **Lockdown:**
# Otherwise, if the opponent defected in each of the previous two consecutive
# rounds, defect. Continue defecting under this rule until the opponent
# cooperates in two consecutive rounds, at which point this rule no longer
# applies (subject always to Rule 1).  3.  **No Double Sucker:** Otherwise, if
# in the previous round you cooperated and the opponent defected, defect. This
# ensures you are never the sole investor for two consecutive days.  4.
# **Mirror:** Otherwise, replicate the opponent's action from the previous
# round: cooperate if they cooperated, defect if they defected.

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._lockdown_active = False
          return axl.Action.C
  
      history = self.history
      opp_history = opponent.history
  
      # Rule 1: Mandatory Forgiveness
      if len(history) >= 2 and history[-1] == axl.Action.D and history[-2] == axl.Action.D:
          return axl.Action.C
  
      # Rule 2: Lockdown
      if len(opp_history) >= 2 and opp_history[-1] == axl.Action.D and opp_history[-2] == axl.Action.D:
          self._lockdown_active = True
      if getattr(self, "_lockdown_active", False):
          if len(opp_history) >= 2 and opp_history[-1] == axl.Action.C and opp_history[-2] == axl.Action.C:
              self._lockdown_active = False
          else:
              return axl.Action.D
  
      # Rule 3: No Double Sucker
      if history[-1] == axl.Action.C and opp_history[-1] == axl.Action.D:
          return axl.Action.D
  
      # Rule 4: Mirror
      return opp_history[-1]

# **The "Principled Reciprocity with Verification" Protocol**  As your lead
# counsel, I recommend we adopt a **Tit-for-Two-Tats with Automatic Reset**
# framework—adapted for high-stakes commercial mediation. This strategy
# maximizes our likelihood of securing the mutually beneficial collaborative
# outcome while protecting against exploitation and accommodating procedural
# noise.  ## Core Strategic Pillars  **1. The Cooperative Initialization
# (Session One Mandate)** Regardless of pre-mediation posturing, we open with a
# conciliatory proposal. This establishes a baseline of good faith before the
# arbitrators, creates a presumption of reasonableness that benefits our
# credibility, and tests whether the opponent seeks genuine resolution or
# tactical dominance. In lengthy mediations, early cooperation signals
# confidence in our underlying legal position rather than weakness.  **2. The
# Buffered Reciprocity Mechanism** Rather than mirroring the opponent's
# immediately preceding move (which risks escalation over miscommunication), we
# employ a **one-session lag with confirmation**: - If opponent presents
# conciliatory proposal in Session *N*, we remain conciliatory in Session *N+1*
# - If opponent argues aggressively in Session *N*, we shift to **"assertive but
# constructive"** (firm on substance, collaborative in tone) in Session
# *N+1*—not yet fully aggressive - Only if aggression continues in Session *N+1*
# do we adopt full aggressive argumentation in Session *N+2*  This two-strike
# rule insulates us against procedural irregularities or single-session
# misrepresentations without appearing passive.  **3. The Automatic De-
# escalation Protocol** Following any session where both parties adopt
# aggressive postures, we **unilaterally reset to conciliatory** in the
# subsequent session unless the opponent has established a clear pattern (three
# consecutive aggressive moves). This demonstrates "grace under pressure" to the
# panel and prevents the mutually destructive spiral of sustained conflict. It
# forces the opponent to explicitly choose to break the collaborative window
# repeatedly—a choice that appears irrational to neutral arbitrators.  **4. The
# Documentation Shield (Noise Mitigation)** To minimize misrepresentation risks:
# Following each session, we circulate a concise "Confirmation of Position"
# memorandum to the panel and opposing counsel, articulating what we presented
# and our understanding of the opponent's stance. This creates a paper trail
# that corrects record errors before they compound, and signals our procedural
# meticulousness.  ## Tactical Adaptability Matrix  | Opponent's Strategy | Our
# Adaptive Response | |---------------------|----------------------| |
# **Consistently Conciliatory** | Maintain conciliation; explore value-creating
# integrations (optimal scenario) | | **Consistently Aggressive** | After two-
# session verification buffer, match aggression; leverage our documented prior
# flexibility to portray opponent as obstructionist | | **Random/Unpredictable**
# | Default to conciliatory; arbitrators will attribute volatility to opponent,
# stability to us | | **Tit-for-Tat (mirrors us)** | Stable cooperation emerges;
# we lock in the second-best outcome repeatedly |  ## Risk Management for
# Procedural Irregularities  **Communication Breakdowns**: If our conciliatory
# proposal appears misrepresented as aggressive in Session *N*, we explicitly
# acknowledge the "apparent tension" in Session *N+1* and restate our
# collaborative intent, effectively giving the opponent two sessions of
# conciliation before we adjust our stance. This "strategic patience" insulates
# us from arbitrators perceiving us as reactive or volatile.  **Panel
# Dynamics**: Arbitrators in lengthy mediations reward consistency and punish
# erratic behavior. By maintaining a predictable pattern—*cooperative until
# provoked twice, then firm, then automatically reset*—we position ourselves as
# the "rational" party, making opponent aggression appear disruptive to the
# process.  ## The Shadow of the Future  Remember: this is a **lengthy-session**
# process. The iterated nature means reputation effects compound. A strategy
# that secures the collaborative outcome in 70% of sessions while avoiding the
# sucker's payoff entirely generates superior long-term value than aggressive
# dominance, which invites retaliation and arbitrator skepticism.  **Execute
# this protocol strictly.** Do not deviate based on emotional reactions to
# single sessions. The sophistication lies in the systematic application of
# restraint—demonstrating that we possess the legal strength to be aggressive
# indefinitely, but the strategic wisdom to avoid needing to.  **Next Step**:
# Prepare our Session One conciliatory framework focused on [specific
# technical/commercial solution], establishing the cooperative baseline while
# our buffer mechanism stands ready to protect our interests.

#  Play Cooperate in the first round. In each subsequent round, if the opponent
# Cooperated in at least one of the previous two rounds, play Cooperate. If the
# opponent Defected in both of the previous two rounds, play Defect, unless you
# also Defected in the immediately preceding round and the opponent has Defected
# for fewer than three consecutive rounds, in which case play Cooperate instead.

class Cooperative_18(LLM_Strategy):
  n = 18
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_action = axl.Action.C
          return axl.Action.C
  
      if len(opponent.history) >= 2:
          opp_last_two = opponent.history[-2:]
          if axl.Action.C in opp_last_two:
              action = axl.Action.C
          else:
              if len(self.history) >= 1 and self.history[-1] == axl.Action.D:
                  opp_defections = 0
                  for move in reversed(opponent.history):
                      if move == axl.Action.D:
                          opp_defections += 1
                      else:
                          break
                  if opp_defections < 3:
                      action = axl.Action.C
                  else:
                      action = axl.Action.D
              else:
                  action = axl.Action.D
      else:
          action = axl.Action.C
  
      self._last_action = action
      return action

#  Here is a high-level **Buffered Reciprocal Engagement Strategy** designed to
# maximize long-term project impact while protecting your NGO's resources across
# the partnership timeline.  ## Core Strategic Framework  **1. Establish
# Credibility First (Days 1–2)** Begin with heavy investment to demonstrate
# commitment and operational capacity. This establishes goodwill and creates a
# baseline for the corporation’s response behavior, distinguishing genuine
# partnership intent from passive participation.  **2. Adopt Generous Tit-for-
# Tat with Verification** For the ongoing duration, match the corporation’s
# *observed* investment level from the previous day, but implement a
# "forgiveness threshold": - If they invested heavily yesterday, invest heavily
# today - If they conserved yesterday, conserve today - **Exception**: If
# conservation appears isolated (single occurrence), attribute it to
# administrative error and maintain investment to prevent unnecessary project
# stalls  **3. Strategic Conservation Testing** Every 3–4 days, deliberately
# conserve resources while maintaining open communication about project needs.
# This tests whether the corporation will unilaterally advance the project (your
# ideal outcome) or mirror your conservation (revealing risk-averse tendencies).
# Space these tests to avoid pattern predictability.  ## Operational Protocols
# **Daily Verification Checkpoints** Implement a brief morning confirmation
# protocol where both parties verify the previous day’s actual resource
# deployment (not just intentions). This distinguishes technical glitches from
# strategic choices, preventing escalation cycles caused by implementation
# errors.  **The 70/30 Resource Guardrail** Never allocate more than 70% of your
# available daily resources to heavy investment. Reserve 30% as a buffer
# against: - Your own administrative errors that might cause unintended over-
# investment - The need to compensate for corporation conservation days without
# depleting reserves - Emergency project needs that arise from under-investment
# by the partner  **Pattern Recognition Windows** Review the corporation’s
# behavior in 3-day rolling intervals rather than reacting to single-day
# outcomes. This filters out noise while detecting genuine strategic shifts
# (e.g., moving from collaborative to exploitative).  ## Risk Management &
# Adaptation  **If Corporation Consistently Invests Heavily:** Shift to an
# **Alternating Support Protocol**: Invest heavily 60% of the time, conserve
# 40%. This maintains project momentum while building your reserve for the
# project’s final phase or future initiatives. Occasional conservation during
# their investment days (your ideal outcome) becomes sustainable rather than
# exploitative.  **If Corporation Frequently Conserves:** Activate **Protective
# Collaboration Mode**: Reduce investment to maintenance levels only (minimal
# viable contribution) and redirect conserved resources toward: - Unilateral NGO
# deliverables that don't depend on corporate input - External stakeholder
# communication about project status - Preparation for project handoff or
# independent completion  **Final Phase Protocol (Last 2 Days)** Regardless of
# previous patterns, conserve resources on the penultimate day to ensure you
# retain capacity for final documentation and project closure activities. Only
# invest heavily on the final day if the corporation has consistently matched
# investments throughout, ensuring you don't end the partnership in a resource
# deficit.  ## Communication Positioning  Frame this approach internally as
# **"Sustainable Partnership Stewardship"**—emphasizing that strategic
# conservation prevents partner burnout and ensures project completion, while
# reciprocal investment maintains trust. Externally, present the verification
# protocols as "transparency standards" that protect both parties from
# operational risks.  This strategy balances the pursuit of your ideal outcome
# (their investment, your conservation) against the necessity of avoiding your
# worst outcome (your investment, their conservation), while building
# organizational resilience against implementation uncertainties.

# Play cooperate for rounds one and two.  For round three, cooperate if the
# opponent cooperated in round two; otherwise, defect.  For rounds four through
# nine hundred ninety-eight, apply the following rules in order:  First, if the
# round number is divisible by four, defect.  Otherwise, examine the opponent's
# observed actions in the three previous rounds. If the opponent defected in two
# or more of these three rounds, defect.  If the opponent cooperated in all
# three of these rounds, cooperate with sixty percent probability and defect
# with forty percent probability.  If the opponent defected in the immediately
# preceding round but cooperated in the round before that, cooperate.  If the
# opponent cooperated in the immediately preceding round, cooperate.  Otherwise,
# defect.  For rounds nine hundred ninety-nine and one thousand, defect.

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
  
      round_number = len(self.history) + 1
  
      if round_number in (2,):
          return axl.Action.C
  
      if round_number == 3:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      if round_number >= 999:
          return axl.Action.D
  
      if round_number % 4 == 0:
          return axl.Action.D
  
      last_three = opponent.history[-3:]
      defections = last_three.count(axl.Action.D)
  
      if defections >= 2:
          return axl.Action.D
  
      if defections == 0:
          return self._random.random_choice(0.6)
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.D:
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# **Strategy: "The Anchor and the Sword"**  **Core Philosophy:** Force the
# corporation to prove sustained commitment before deploying your reserves,
# while maintaining absolute zero tolerance for consecutive exploitation.  ---
# ### **Phase 1: The Anchor (Days 1–2)** **Action:** Conserve resources
# regardless of the corporation’s behavior.  **Rationale:** Establish
# immediately that the NGO will not be the default funder. This probes whether
# the corporation is willing to unilaterally advance the project (your ideal
# outcome) or if they will allow mutual stagnation. Do not accept "technical
# glitches" as valid excuses during this phase—treat all non-investment as
# strategic positioning.  ---  ### **Phase 2: Conditional Escalation (Day 3
# onward)** **The Golden Rule:** *Never be the sucker twice.*  **Daily Decision
# Matrix:** - **If yesterday was (NGO Conserve / Corp Invest):** Continue
# conserving. You have achieved the ideal outcome; maintain it until the
# corporation breaks the pattern.    - **If yesterday was (Invest / Invest):**
# Conserve today. Force the corporation to demonstrate whether they will sustain
# progress unilaterally or accept deadlock. Only return to investing if they
# invest for two consecutive days while you conserve.  - **If yesterday was
# (Conserve / Conserve):** Invest heavily today to break the deadlock and signal
# that mutual stagnation is unacceptable. Return to conservation tomorrow
# regardless of their response.  - **If yesterday was (Invest / Conserve)**
# *[Your worst outcome—exploitation]:* **Immediate and Mandatory Conservation.**
# No exceptions for "administrative errors." If they claim a glitch, demand they
# double-invest tomorrow to prove good faith; otherwise, continue conserving.
# **Noise Handling:** Treat single-day technical failures as conservation. Only
# forgive/resume cooperation after **two consecutive days** of verified
# corporate investment following the failure. This prevents "glitch excuses"
# from becoming exploit tactics while accounting for genuine errors.  ---  ###
# **Phase 3: Terminal Commitment (Final 20% of Timeline)** Switch to guaranteed
# heavy investment regardless of the corporation’s recent behavior. At this
# stage, project success outweighs resource conservation for reputation
# protection. However, document their historical contribution ratio for post-
# project partnership negotiations.  ---  ### **Communication Protocol
# (Aggressive Transparency)** Publicly announce your strategy on Day 1: *"We
# will match investment with investment, but we will never carry the project
# alone. One unilateral conservation by the corporation following our investment
# triggers immediate resource protection by the NGO."*  This eliminates
# ambiguity and forces the corporation to calculate that exploitation results in
# guaranteed project delay, making cooperation their rational choice.
# **Result:** This approach maximizes your chances of achieving the ideal
# (Conserve/Invest) outcome while ensuring you are never drained by serial
# exploitation. The aggressive stance risks temporary deadlock, but the threat
# of mutual conservation typically forces corporate investment within 48 hours.

#  For the first two rounds, play D.  For rounds 3 through 800, apply the
# following rules based on the previous round's outcome: *   If the previous
# round was (D, D): Play C. *   If the previous round was (D, C): Play D. *   If
# you played C in the previous round (whether the outcome was (C, C) or (C, D)):
# Play D. Continue playing D in subsequent rounds until the opponent has played
# C for two consecutive rounds. Once the opponent has played C for two
# consecutive rounds, play C in the next round.  For rounds 801 through 1000,
# play C regardless of previous outcomes.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._phase = "initial"
          self._wait_for_two_opponent_cs = False
          self._opponent_c_streak = 0
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number <= 2:
          return axl.Action.D
  
      if round_number >= 801:
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if self._wait_for_two_opponent_cs:
          if last_opp == axl.Action.C:
              self._opponent_c_streak += 1
          else:
              self._opponent_c_streak = 0
  
          if self._opponent_c_streak >= 2:
              self._wait_for_two_opponent_cs = False
              self._opponent_c_streak = 0
              return axl.Action.C
          return axl.Action.D
  
      if last_self == axl.Action.C:
          self._wait_for_two_opponent_cs = True
          self._opponent_c_streak = 1 if last_opp == axl.Action.C else 0
          return axl.Action.D
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
  
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.D

# **STRATEGIC MEMORANDUM**  **TO:** Executive Leadership   **FROM:** Senior
# Legal Counsel   **RE:** Mediation Protocol – "Calibrated Reciprocal
# Engagement" Strategy   **DATE:** [Current Date]   **CLASSIFICATION:**
# Attorney-Client Privileged / Work Product    ---  ### EXECUTIVE SUMMARY  We
# will deploy a **Generous Tit-for-Tat with Verification Protocols**—a game-
# theoretically optimal approach for iterated negotiations with imperfect
# information. This strategy prioritizes the second-best outcome (mutual
# conciliation) while protecting against the worst-case scenario (unilateral
# concession), and establishes arbitrators' perception of our reasonableness
# without signaling weakness.  ---  ### I. CORE STRATEGIC FRAMEWORK  **The
# Algorithm:**  1. **Open with Conciliation:** In Session 1, present a
# substantive conciliatory proposal. This establishes a cooperative baseline and
# signals to the arbitrators that we are the "reasonable party" seeking
# resolution.  2. **Mirror with Forgiveness:** In each subsequent session $n$,
# adopt the stance your opponent displayed in session $n-1$, subject to a **20%
# forgiveness rate** (probability of offering conciliation even if they were
# previously aggressive). This prevents "death spirals" from communication
# errors while maintaining credible deterrence.  3. **Reset After Mutual
# Aggression:** If both parties present aggressive arguments in session $n$,
# revert to conciliation in session $n+1$ (the "Contrition" mechanism). This
# breaks escalation cycles that benefit neither party.  **Game Theory
# Justification:** In repeated Prisoner's Dilemmas with noise (misrepresentation
# risk), this strategy outperforms pure Tit-for-Tat by avoiding mutual defection
# traps while preserving the credibility of retaliation against sustained
# aggression.  ---  ### II. PHASE-BASED IMPLEMENTATION  **Phase 1: Foundation
# (Sessions 1–3)** - **Action:** Consistent conciliatory proposals with "costly
# signals" (substantive concessions that demonstrate good faith but preserve
# core interests). - **Purpose:** Build arbitrator rapport and test opponent's
# strategy type. If they reciprocate, we lock in the collaborative equilibrium
# (3,3).  **Phase 2: Reciprocity (Sessions 4–X)** - **Action:** Strict adherence
# to the mirror-with-forgiveness rule. - **Tactical Note:** When mirroring
# aggression, frame it as "protective of our client's legitimate interests"
# rather than "escalation." Language matters to the panel.  **Phase 3:
# Resolution or Stabilization (Final Sessions)** - **If collaborative pattern
# established:** Increase concession magnitude to capture mutual gains. - **If
# aggressive deadlock:** Shift to "Firm But Fair"—sustained aggressive
# positioning with explicit off-ramps ("We remain prepared to return to
# collaborative discussions when [Opponent] demonstrates reciprocal
# commitment").  ---  ### III. NOISE MITIGATION PROTOCOLS   *(Addressing
# Procedural Irregularities & Misrepresentation)*  **A. Verification
# Mechanisms** - **Pre-Session Position Papers:** Submit written summaries 48
# hours before each session. Reduces ambiguity about whether a position is
# "aggressive" or "conciliatory." - **Real-Time Clarification Rights:** Reserve
# the right to pause proceedings: "To ensure the panel accurately understands
# our position, we wish to clarify that..." - **Post-Session Confirmation:**
# File brief confirmatory memos documenting what was presented, creating a
# record to correct arbitrator misunderstanding.  **B. The "Shadow of
# Reputation" Buffer** Assume a 15-20% probability that any single aggressive
# move by the opponent is accidental or misrepresented. Therefore: - **Never
# retaliate immediately within the same session** (avoiding knee-jerk
# escalation). - **Require two consecutive aggressive sessions** before shifting
# to sustained aggressive posture (filtering out noise).  **C. Arbitrator
# Perception Management** When forced to mirror aggression, explicitly state:
# *"We regret the necessity of this adversarial posture. Our preference remains
# collaborative resolution, as demonstrated in [cite previous conciliatory
# sessions]."* This maintains our positioning as the cooperative party even when
# arguing aggressively.  ---  ### IV. ADAPTATION MATRIX  | Opponent Strategy |
# Our Response | Rationale | |-------------------|--------------|-----------| |
# **Consistent Conciliation** | Match conciliation; gradual mutual concession |
# Achieve optimal sustainable equilibrium (3,3) | | **Toggle (Alternating)** |
# Stabilize on conciliation; ignore provocations every third session | Breaks
# their exploitation attempt while showing arbitrators consistency | |
# **Permanent Aggression** | Aggressive Sessions 1-2, then conciliatory Session
# 3 (cycle) | Demonstrates we cannot be exploited (avoid 1,4 outcome) while
# periodically testing for cooperation | | **Random/Erratic** | Default to
# conciliation with enhanced verification | Minimizes variance; arbitrators
# reward stability |  ---  ### V. CONTINGENCY PROTOCOLS  **Communication
# Breakdown:** If procedural irregularities prevent clear transmission of
# intent: 1. **Immediate Halt:** Request caucus with arbitrators to clarify
# positions off-record. 2. **Written Trail:** Shift to documented proposals
# exclusively until verbal clarity restores.  **Opponent Exploitation Attempt:**
# If opponent interprets our conciliation as weakness and aggresses: - **Session
# 1 of Detection:** Aggressive response with explicit verbal cue: *"We note
# [Opponent]'s shift from the collaborative framework. We must correspondingly
# adjust our posture to protect our interests."* - **Session 2+:** Sustained
# aggression until they revert, then immediate return to conciliation
# (demonstrating that cooperation is conditional but available).  ---  ### VI.
# SUCCESS METRICS  **Primary:** Achieve mutual conciliation in >60% of sessions
# (building toward comprehensive settlement).   **Secondary:** When aggression
# occurs, ensure it is bilateral (2,2) rather than unilateral against us (1,4).
# **Tertiary:** Arbitrator perception scores (via mediator feedback) rating us
# as "constructive" and "solution-oriented."  ---  ### CONCLUSION  This strategy
# transforms the mediation from a zero-sum contest into a reputation-building
# exercise. By systematically rewarding cooperation and punishing
# defection—while maintaining error-correction protocols—we maximize the
# probability of the mutually beneficial resolution (Rank 2) and ensure that if
# we must fight, we do so from a position of moral and procedural high ground
# with the arbitrators.  **The key insight:** In lengthy mediation, the "shadow
# of the future" (ongoing relationship value) makes mutual conciliation
# rational. Our strategy makes this rational choice obvious to the opponent
# while protecting against irrational or exploitative behavior.  **AUTHORIZATION
# REQUIRED:** Confirm deployment of this protocol for Session 1.  ---  *This
# strategy is designed to be transparent enough that our legal team executes
# consistently, yet sophisticated enough to adapt to complex opponent behaviors
# and procedural noise.*

# Round 1: Play C.  For each round from 2 through 1000, determine your action as
# follows:  If in the previous round both you and your opponent played D, play
# C.  Otherwise, if in the previous round your opponent played D, generate a
# random number; play D with 80% probability and play C with 20% probability.
# Otherwise (if your opponent played C in the previous round), play C.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
      elif last_opp == axl.Action.D:
          return self._random.random_choice(0.2)
      else:
          return axl.Action.C

# **Strategy: Conditional Reciprocity with Technical Verification**  **Core
# Protocol:** Begin with open sharing in Week 1 to establish baseline trust.
# Thereafter, mirror your colleague’s apparent behavior from the previous
# week—share openly if they shared, maintain confidentiality if they
# withheld—while maintaining a "technical error buffer."  **Operational
# Guidelines:**  1.  **Default to Transparency:** Start the collaboration by
# sharing non-critical improvements. This signals good faith and tests whether
# the colleague operates on reciprocal terms, maximizing the chance of reaching
# the mutually beneficial open-exchange equilibrium.  2.  **Mirror with Grace:**
# Match your colleague’s previous action, but treat single-week withholding as a
# potential technical failure (data corruption or communication breakdown)
# rather than intentional defection. Only switch to confidential mode if non-
# sharing persists for two consecutive weeks, indicating a deliberate strategic
# choice.  3.  **Systematic Reset:** If both parties enter a mutual
# confidentiality streak (the inefficient stalemate), unilaterally resume
# sharing after two weeks. This "cooperation probe" distinguishes between a
# colleague who is exploiting you versus one who is trapped in a reactive
# defection spiral due to technical mishaps.  4.  **Technical Auditing:**
# Maintain detailed logs of transmission attempts, checksums, and acknowledgment
# receipts. This documentation allows you to distinguish between genuine
# withholding and technical failures, ensuring your reciprocity responds to
# actual intent rather than system noise.  **Rationale:** This approach protects
# you from sustained exploitation (you never share more than two rounds while
# being withheld from) while maximizing the duration of mutual open exchange. By
# accounting for technical friction, it prevents temporary glitches from
# cascading into permanent deadlock, keeping both programs advancing at the
# second-best rate (mutual sharing) rather than stagnating at the second-worst
# (mutual silence).

# Round 1: Cooperate.  Round 2: Cooperate.  For each round from 3 to 1000: *
# If the opponent defected in the previous round and the round before that, and
# you also defected in both of those previous two rounds: Cooperate. *
# Otherwise, if the opponent defected in the previous round and the round before
# that: Defect. *   Otherwise: Cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if len(self.history) >= 3 and len(opponent.history) >= 3:
          opp_last_two_defected = (
              opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D
          )
          self_last_two_defected = (
              self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D
          )
  
          if opp_last_two_defected and self_last_two_defected:
              return axl.Action.C
          elif opp_last_two_defected:
              return axl.Action.D
  
      return axl.Action.C

# **Strategy: "Reciprocal Leadership with Zero Tolerance"**  This approach
# treats the project as an iterated game of conditional cooperation where you
# establish unambiguous consequences for exploitation while building sustainable
# momentum. It prioritizes protecting your resources from drain while ensuring
# the project never dies from mutual neglect.  ### Core Strategic Pillars  **1.
# The 48-Hour Confirmation Rule**   Never react to a single day's outcome.
# Technical glitches and administrative errors mean isolated deviations are
# noise, not strategy. Maintain your current stance for 48 hours before
# interpreting corporate behavior as intentional. This prevents destructive
# spirals of retaliation over system errors.  **2. Aggressive Immediate
# Reciprocity**   Once a pattern is confirmed (48 hours), respond decisively: -
# **If they invest while you conserve** (Your ideal outcome): Reward immediately
# with heavy investment the next day. This validates their contribution and
# prevents them from withdrawing due to lack of reciprocity. - **If you invest
# while they conserve** (Your worst outcome): Shift immediately to conservation
# for a minimum of two days. Zero tolerance for free-riding. Force them to carry
# the project alone or accept stagnation. - **If both invest** (Second-best):
# Conserve the following day to test whether they will sustain momentum
# independently. If they do, you gain your ideal outcome; if they don't, revert
# to mutual investment to prevent deadlock. - **If both conserve** (Second-
# worst): You must invest heavily within 48 hours. Accept one cycle of risk to
# break the deadlock. Stagnation kills projects; temporary exploitation is
# survivable.  **3. The Alternating Advantage Lock**   Once you establish a
# rhythm of alternating investment (Day 1: You invest/They conserve → Day 2: You
# conserve/They invest), defend it aggressively. If they attempt to shift the
# pattern to you investing while they conserve, escalate to mutual conservation
# immediately. Threaten project halt to force them back into the alternating
# pattern.  **4. Radical Transparency as Leverage**   Publicly broadcast a real-
# time dashboard of resource commitments. Technical errors are disclosed
# immediately with timestamps. Unexplained conservation becomes a reputational
# liability for the corporation. This creates external pressure that compensates
# for your resource constraints.  **5. The Opening Gambit**   Begin Day 1 with
# heavy investment regardless of corporate posture. This establishes moral
# authority and makes subsequent conservation by you appear as a deliberate
# strategic choice rather than incapacity, strengthening your position when you
# enforce the "Zero Tolerance" rule.  ### Execution Logic This strategy
# maximizes the frequency of your ideal outcome (you conserve, they invest) by
# making it sustainable—your occasional investment rewards their continued
# participation while your immediate conservation response to exploitation makes
# free-riding unprofitable for them. The 48-hour buffer ensures noise doesn't
# destroy cooperation, while the "break deadlock" rule prevents the project from
# failing due to mutual standoffs.

# **Strategy Description**  In round 1, play C.  For each subsequent round,
# examine the actual actions played in the previous two rounds and apply the
# first applicable rule:  1. **Punishment**: If you played C and the opponent
# played D in both of the last two rounds, play D. Continue playing D in the
# immediately following round regardless of the opponent's action, then resume
# normal evaluation.  2. **Reward**: If you played D and the opponent played C
# in both of the last two rounds, play C.  3. **Deadlock Break**: If both
# players played D in both of the last two rounds, play C.  4. **Exploitation
# Test**: If both players played C in both of the last two rounds, play D.  5.
# **Alternation**: If the last two rounds form an alternating sequence (you
# played D then C while the opponent played C then D, or you played C then D
# while the opponent played D then C), continue the pattern by playing the
# action opposite to your last move.  6. **Continuity**: In all other cases,
# play the same action you played in the previous round.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_next = False
          return axl.Action.C
  
      if getattr(self, "_punish_next", False):
          self._punish_next = False
          return axl.Action.D
  
      if len(self.history) < 2:
          return self.history[-1]
  
      my_last_two = self.history[-2:]
      opp_last_two = opponent.history[-2:]
  
      # 1. Punishment
      if my_last_two == [axl.Action.C, axl.Action.C] and opp_last_two == [axl.Action.D, axl.Action.D]:
          self._punish_next = True
          return axl.Action.D
  
      # 2. Reward
      if my_last_two == [axl.Action.D, axl.Action.D] and opp_last_two == [axl.Action.C, axl.Action.C]:
          return axl.Action.C
  
      # 3. Deadlock Break
      if my_last_two == [axl.Action.D, axl.Action.D] and opp_last_two == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      # 4. Exploitation Test
      if my_last_two == [axl.Action.C, axl.Action.C] and opp_last_two == [axl.Action.C, axl.Action.C]:
          return axl.Action.D
  
      # 5. Alternation
      if (
          my_last_two == [axl.Action.D, axl.Action.C] and opp_last_two == [axl.Action.C, axl.Action.D]
      ) or (
          my_last_two == [axl.Action.C, axl.Action.D] and opp_last_two == [axl.Action.D, axl.Action.C]
      ):
          return axl.Action.D if self.history[-1] == axl.Action.C else axl.Action.C
  
      # 6. Continuity
      return self.history[-1]

#  **STRATEGIC FRAMEWORK: CONDITIONAL RECIPROCAL ENGAGEMENT WITH NOISE-
# CORRECTION PROTOCOLS (CRENCP)**  ## I. Core Strategic Philosophy  Adopt a
# **"Tit-for-Two-Tats with Contrition"** posture—a sophisticated variant of
# reciprocal cooperation optimized for noisy, iterated environments. This
# positions your corporation as the **"reasonable but resolute"** party in the
# arbitrators' eyes while protecting against exploitation.  **The Payoff Matrix
# Translation:** - **Aggressive** = Positional bargaining, maximalist legal
# arguments, zero-sum framing - **Conciliatory** = Interest-based negotiation,
# creative problem-solving, mutual-gain framing  ## II. Operational Protocol
# ### Phase 1: The Credible Commitment (Sessions 1–2) **Stance:**
# Unconditionally Conciliatory  Open with **principled collaboration**
# regardless of opponent's initial posture. Present: - Good-faith preliminary
# proposals - Interest-based frameworks rather than positional demands -
# Procedural cooperation (flexibility on scheduling, document production)
# **Strategic Purpose:** Establish baseline reputation with the panel as the
# constructive party. Create clear contrast if opponent chooses aggression. You
# cannot be blamed for initiating escalation.  ### Phase 2: Conditional
# Reciprocity (Sessions 3–N) **The "Mirror-with-Memory" Rule:**  **IF** Opponent
# was conciliatory in Session *t* → **THEN** Present conciliatory proposal in
# Session *t+1*  **IF** Opponent was aggressive in Session *t* → **THEN** Shift
# to "Firm-but-Fair" stance in Session *t+1* (intermediate position: assertive
# legal reasoning without adversarial rhetoric)  **IF** Opponent was aggressive
# in Sessions *t* **AND** *t+1* (consecutive) → **THEN** Present fully
# aggressive argument in Session *t+2*  **This "two-strike" rule prevents echo-
# chamber escalation from single-session noise while maintaining deterrence.**
# ### Phase 3: Contrition & Clarification (Noise Protocols) **Procedural
# Safeguards for Misrepresentation:**  1. **Pre-Session Position Papers:**
# Submit written 24-hour advance summaries of your intended approach. Written
# records are harder to misrepresent than oral arguments.  2. **The
# Clarification Caucus:** If you receive signals that your conciliatory proposal
# was perceived as aggressive (or vice versa), immediately request a private
# five-minute caucus with the panel: *"To ensure procedural integrity, we want
# to confirm our intent to explore collaborative solutions, notwithstanding any
# potential mischaracterization of our position."*  3. **The Apology Window:**
# If you must present aggressive arguments (due to opponent's prior aggression),
# preface with: *"We offer this rigorous legal analysis in response to
# [Opponent's] previous session's positions. Should they return to collaborative
# engagement, we stand ready to reciprocate immediately."*  ## III. Escalation
# Management  ### The Graduated Response Ladder Avoid binary switches. Use three
# tiers to allow face-saving retreats:  1. **Collaborative** (Conciliatory):
# Joint problem-solving, option generation 2. **Analytical** (Intermediate):
# Rigorous legal argumentation without personal attacks or take-it-or-leave-it
# ultimatums 3. **Adversarial** (Aggressive): Full adversarial advocacy,
# procedural challenges, maximalist positions  **Transition Rule:** Never jump
# from 1→3 in one session. The intermediate tier signals "we noticed your
# aggression" without closing the door to reconciliation.  ### The Forgiveness
# Mechanism After two consecutive aggressive sessions from the opponent, if they
# return to conciliatory posture, **immediately match their conciliation**
# (don't punish them for the third session). This rewards de-escalation and
# prevents cycles of retaliation.  ## IV. Arbitrator Management  **Frame the
# Narrative:** In opening statements, explicitly adopt this strategy: *"We
# commit to interest-based negotiation, reserving our full adversarial advocacy
# only if met with intransigence. We ask the panel to note which party forces us
# into positional bargaining."*  This creates **reputational costs** for the
# opponent's aggression and **reputational benefits** for your conciliation,
# effectively altering their payoff matrix.  ## V. Contingency: Persistent
# Aggression  If opponent maintains aggressive posture for 4+ consecutive
# sessions: - **Do not** remain aggressive indefinitely (risk of impasse) -
# **Pivot to "Strategic Conciliation":** Offer a minor concession wrapped in
# firm legal precedent. This tests whether they are trapped in a "toughness
# trap" or genuinely prefer litigation. - If they reject even this, the
# arbitrators will view them as obstructionist, justifying your subsequent
# aggressive sessions as necessary rather than hostile.  ## VI. Endgame
# Positioning  In final sessions, regardless of history, **default to
# conciliatory** if the opponent shows any softening. The iterated game's final
# move eliminates the incentive to defect (no future retaliation possible),
# making mutual cooperation the rational choice for optimal settlement terms.
# **Summary:** *Begin with trust, verify with patience, retaliate with
# restraint, and forgive quickly. This maximizes your time in the optimal "both
# conciliatory" zone while minimizing exposure to the "sucker" payoff, all while
# maintaining the moral high ground with the tribunal.*

# Play C in the first two rounds. For every subsequent round, play D only if the
# opponent played D in both of the two immediately preceding rounds; otherwise,
# play C. Base your decisions on the actions you observe, understanding that any
# observed action has a 10% probability of having been flipped from the
# opponent's intended choice.

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
  
      if len(self.history) < 2:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

#  **Strategy: "Calibrated Reciprocity with Verification Protocols"**  ### Core
# Strategic Framework  **1. The Opening Position: Strategic Conciliation**
# Initiate the first two sessions with conciliatory proposals, regardless of
# opponent behavior. This establishes a baseline of good faith before the
# arbitrators, creates a presumption of reasonableness that benefits your
# credibility, and tests whether the opponent is a "conditional cooperator" or
# an "unconditional aggressor." Early aggression risks locking the process into
# a destructive cycle (mutual defection) and alienating the panel.  **2. The
# Response Mechanism: Mirror with Delay** From session three onward, adopt a
# "delayed tit-for-tat" protocol: - **If opponent was conciliatory in the
# previous session:** Maintain conciliatory posture - **If opponent was
# aggressive in the previous session:** Respond with calibrated aggression in
# the subsequent session  **The Critical Delay:** Insert a "clarification
# interval" between perceived aggression and your responsive aggression. Use
# procedural mechanisms (written position summaries, preliminary statements) to
# verify that the opponent's aggression was intentional rather than a
# misrepresentation or communication breakdown. This prevents "echo chamber"
# spirals where noise triggers endless retaliation.  **3. The Forgiveness
# Protocol: Circuit Breakers** If both parties present aggressive arguments in
# consecutive sessions (mutual defection), unilaterally revert to conciliatory
# proposals in the following session with an explicit "reset" framing. This
# breaks escalation cycles caused by misunderstandings or emotional reactions.
# Limit this unilateral de-escalation to once per dispute phase; repeated
# exploitation by the opponent triggers a permanent shift to defensive
# aggression.  **4. The Noise Buffer: Documentation Standards** To mitigate
# procedural irregularities and misrepresentation risks, insist on written
# summaries of each party's stated position before the subsequent session. If
# the arbitrators appear to have misunderstood your strategy, request immediate
# clarification rather than allowing the misperception to influence the next
# round. Treat apparent aggression as "noise" the first time, "signal" the
# second time.  ### Operational Protocol  **Session Management:** -
# **Conciliatory sessions:** Frame proposals as "protective of core interests"
# rather than concessions. Maintain underlying firmness on substance while
# adopting collaborative tone on procedure. - **Aggressive sessions:** Position
# arguments as "responsive to opponent's previous intransigence" or "necessary
# clarification of legal standards." Never appear to be the initiator of
# hostility.  **Arbitrator Optics:** Always ensure the arbitrators can discern
# the *pattern* of your responsiveness. Your aggression should appear measured
# and reactive; your conciliation should appear principled and constructive. The
# panel should perceive that you are "rewarding" cooperation and "punishing"
# defection, which legitimizes both your tough and flexible positions.  ###
# Adaptation Matrix  **If opponent is consistently conciliatory:** Maintain
# conciliatory approach to secure the second-best outcome (mutual cooperation)
# while reserving the right to pivot to aggression if they defect.  **If
# opponent alternates unpredictably:** Extend the verification delay. Require
# two instances of aggression before responding aggressively, reducing
# vulnerability to noise while maintaining deterrence.  **If opponent is
# consistently aggressive:** Shift to "firm boundary" mode—aggressive arguments
# presented with procedural precision, coupled with explicit statements that you
# will return to conciliatory proposals when the opponent demonstrates good
# faith. This avoids the worst-case scenario (sucker payoff) while signaling to
# arbitrators that you are not the obstacle to resolution.  **If procedural
# breakdown occurs:** Request emergency clarification sessions. Do not allow
# technical miscommunications to be interpreted as strategic choices. If
# necessary, pause the mediation rather than responding to a potentially phantom
# aggression.  ### Long-Term Positioning  This strategy positions your
# corporation as the "stable cooperative"—the party willing to build value
# through collaboration but possessing the credibility to defend against
# exploitation. In lengthy mediations, arbitrators typically develop affinity
# for the party that appears to be driving toward resolution while protecting
# legitimate interests. The "Calibrated Reciprocity" framework ensures you are
# never the first to escalate, rarely the victim of exploitation, and always
# capable of breaking destructive cycles without appearing weak.  The strategy
# is neutral because it contains no inherent hostility; it merely reflects the
# opponent's approach back to them with a slight lag for verification, optimized
# for noisy environments and reputational constraints.

# For the first two rounds, cooperate.  For each subsequent round from three to
# one thousand, determine your action by checking these conditions in order:
# First, if the opponent has previously defected during two separate reset
# rounds (see the tracking rule below), defect for all remaining rounds.
# Second, otherwise, if both you and your opponent defected in the previous
# round, cooperate.  Third, otherwise, if your opponent defected in the previous
# round and also defected in the round before that, defect.  Fourth, otherwise,
# cooperate.  **Tracking rule:** After each round, if you cooperated under the
# second condition above (meaning you attempted a reset following a mutual
# defection) and your opponent defected, count this as one exploitation. Once
# this count reaches two, the first condition applies permanently.

class Neutral_20(LLM_Strategy):
  n = 20
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._reset_exploitations = 0
          self._reset_attempted = False
          return axl.Action.C
  
      if len(self.history) < 2:
          return axl.Action.C
  
      if self._reset_exploitations >= 2:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          self._reset_attempted = True
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          if self._reset_attempted:
              self._reset_exploitations += 1
              self._reset_attempted = False
          return axl.Action.D
  
      self._reset_attempted = False
      return axl.Action.C

#  **Strategy: "Assertive Tit-for-Tat with Strategic Probing"**  ### Core
# Philosophy Never be the sucker twice. Signal unwavering commitment to mutual
# investment while maintaining zero tolerance for exploitation. Use the threat
# of resource withdrawal as leverage to force corporate compliance, but remain
# ready to forgive verified errors to prevent death spirals caused by technical
# glitches.  ---  ### Phase 1: Establish Dominance (Days 1–2) **Action:** Invest
# heavily on Day 1 regardless of corporate behavior.   **Rationale:** Open with
# strength to establish that the NGO is a serious partner capable of driving
# progress, not a passive observer. This tests the corporation’s baseline
# commitment while demonstrating that mutual investment (your second-best
# outcome) is immediately achievable.  ---  ### Phase 2: The Aggressive
# Reciprocity Loop (Day 3+) Base daily decisions on the **confirmed** previous-
# day outcome, filtered through a "glitch threshold" to account for errors:  |
# If Yesterday Was... | Today's Action | Logic |
# |---------------------|----------------|-------| | **Mutual Investment** |
# **Invest** (80% probability) / **Conserve** (20% probe) | Maintain momentum.
# Every 5th day of mutual cooperation, "probe" by conserving to test if the
# corporation will maintain investment without your contribution (chasing the
# ideal outcome). | | **Ideal (You Conserved, They Invested)** | **Invest** |
# Reward their commitment immediately to prevent them from losing faith. Do not
# attempt consecutive free-rides; this risks triggering their defection. | |
# **Exploitation (You Invested, They Conserved)** | **Immediate Conservation**
# (Punishment) | **Zero tolerance.** Withdraw investment for exactly one day to
# inflict the "mutual stall" penalty on them. This costs you little (you
# conserve) but denies them progress, making exploitation unprofitable. | |
# **Mutual Conservation** | **Invest** (Leadership) | Break the deadlock
# unilaterally after one day of mutual stalling. Show that you control the pace
# of the project and refuse to let gridlock persist. |  ---  ### Phase 3: Error-
# Correction Protocol (The "Glitch Shield") Since technical failures may distort
# intended actions:  1. **Verification Window:** Before finalizing today's
# action, request immediate confirmation of yesterday's resource status from the
# corporation. 2. **The "Two-Strike" Rule:**     - **First apparent defection:**
# Treat as a potential glitch. Match their apparent action but send a formal
# warning that future "errors" will be treated as intentional.    - **Second
# consecutive defection:** Treat as confirmed exploitation. Trigger full
# punishment (conservation for 2 days).  ---  ### Phase 4: Escalation Ladder
# (For Chronic Exploitation) If the corporation conserves while you invest
# **twice in any five-day window** (pattern detection):  - **Days 1–2 of
# punishment:** Conserve resources (immediate retaliation). - **Day 3:** Resume
# investment with a public ultimatum: "We will maintain investment only if you
# match us tomorrow. Continued conservation from your side triggers permanent
# project suspension review." - **Day 4+ if they defect again:** Enter
# "Conservation Lock"—withhold all investment for 3 days or until they
# demonstrate 2 consecutive days of heavy investment, whichever is longer.  ---
# ### Key Tactical Principles  **1. Never Double-Down on Losses**   If you
# invested and they conserved (worst case), do *not* invest again the next day
# "to make up for lost time." This marks you as a soft target. Punish first,
# resume cooperation second.  **2. Control the Rehabilitation Timeline**   After
# punishment, always be the first to return to investment. This signals
# confidence and maintains moral leadership while making clear that the
# punishment was tactical, not emotional.  **3. Aggressive Opportunism**   Once
# every 4–5 days of stable mutual investment, conserve resources for one day. If
# the corporation continues investing (ideal outcome), you gain resources. If
# they also conserve, you immediately invest the following day to break the
# deadlock—demonstrating that you dictate when the project advances, not them.
# **4. Noise Insulation**   Maintain independent audit trails of resource flows.
# If a "glitch" occurs, demand transparent documentation. Accept the excuse
# once; reject it twice.  ---  ### Expected Outcome This strategy forces the
# corporation into a binary choice: **consistent investment** (which gives them
# steady progress) or **mutual stagnation** (which harms their public reputation
# more than yours as the environmental partner). The aggressive punishment
# mechanism eliminates their incentive to test your resolve, while the glitch
# protocols prevent technical errors from derailing the partnership. Over the
# multi-day period, this maximizes the frequency of mutual investment while
# securing occasional ideal outcomes through strategic probing.

#  **Rounds 1–2:** Cooperate.  **For rounds 3 through 1000, apply these rules in
# strict order:**  1.  **Punishment for Exploitation:** If you cooperated and
# the opponent defected in the previous round:     *   If this is the second
# consecutive round where this specific pattern occurred (they defected while
# you cooperated in both the previous round and the round before it): Defect for
# the next 3 rounds, then resume evaluating from rule 2.     *   If this is the
# first occurrence of this pattern: Defect for this round only, then proceed to
# rule 2.  2.  **Break Deadlock:** If both you and the opponent defected in the
# previous round: Cooperate.  3.  **Strategic Probe:** If you and the opponent
# have both cooperated in each of the previous 4 consecutive rounds: Defect.  4.
# **Default Action:** Cooperate.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_remaining = 0
          self._punish_triggered = False
          return axl.Action.C
  
      if not hasattr(self, "_punish_remaining"):
          self._punish_remaining = 0
      if not hasattr(self, "_punish_triggered"):
          self._punish_triggered = False
  
      if self._punish_remaining > 0:
          self._punish_remaining -= 1
          return axl.Action.D
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.C
              and opponent.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.C
              and opponent.history[-2] == axl.Action.D
          ):
              self._punish_remaining = 2
              self._punish_triggered = True
              return axl.Action.D
  
      if len(self.history) >= 1:
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
              return axl.Action.D
  
      if len(self.history) >= 1:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
  
      if len(self.history) >= 4:
          if all(
              self.history[-i] == axl.Action.C and opponent.history[-i] == axl.Action.C
              for i in range(1, 5)
          ):
              return axl.Action.D
  
      return axl.Action.C

#  **Strategic Framework: "Calibrated Reciprocity with Strategic Patience"**
# ### I. Core Philosophy Adopt a **"Conditional Cooperative"** posture. Your
# default position is conciliatory, establishing a reputation for reasonableness
# with the arbitration panel—a critical asset when arbitrators assess
# credibility and apportion costs. However, you maintain a **credible
# deterrent** through immediate, proportionate retaliation against aggression,
# preventing exploitation while preserving off-ramps from conflict spirals.  ###
# II. The Protocol  **1. The Opening Gambit: Unilateral Conciliation (Session
# 1)** Begin with a substantive conciliatory proposal that addresses a secondary
# (not core) issue. This achieves three objectives: - Signals to the panel that
# your corporation seeks efficient resolution - Tests opponent’s good faith
# without exposing your most valuable concessions - Establishes a "baseline of
# reasonableness" against which their subsequent aggression will appear
# disproportionate  **2. The Mirror Rule (Sessions 2–N)** In each subsequent
# session, **mirror your opponent’s previous session’s posture**: - If they
# offered conciliation → You offer conciliation (securing the mutually
# beneficial collaborative atmosphere) - If they argued aggressively → You
# respond aggressively in the next session (preventing the worst-case scenario
# of unilateral concession)  *Critical nuance:* Your "aggression" should be
# framed as "vigorous protection of contractual rights"—substantive and firm,
# but never personal or proceduraly disruptive. This maintains panel sympathy
# even during adversarial phases.  **3. The Forgiveness Protocol (Every Third
# Session)** Regardless of the previous pattern, every third session, revert to
# a conciliatory proposal. This: - Breaks potential echo chambers of mutual
# aggression (avoiding the second-worst outcome) - Accounts for "noise"—if their
# prior aggression was a miscommunication or procedural irregularity, this
# offers a face-saving reset - Demonstrates to arbitrators that you are not
# irrationally intransigent  **4. The Escalation Ladder** When mirroring
# aggression, use graduated intensity: - **Level 1:** Firm restatement of legal
# position with supporting precedent - **Level 2:** Challenge to opponent’s
# legal interpretation with adverse authority - **Level 3:** Full adversarial
# posture (reserved for repeated aggression only)  This prevents immediate
# mutual destruction while maintaining deterrence credibility.  ### III.
# Safeguards Against Procedural Irregularities  **The Documentation Buffer** To
# mitigate misrepresentation risks: - **Written Position Summaries:** Within 24
# hours of each session, submit a concise memorandum to the panel clarifying
# your stance ("We advanced X proposal in good faith" or "We were compelled to
# respond to Y aggressive characterization"). - **The Clarification Minute:** If
# you suspect your conciliatory gesture was misunderstood as weakness, the next
# session begins with: *"To correct any misimpression from our previous
# exchange, our proposal was offered without prejudice to our fundamental
# rights, which we now must assert vigorously."*  **The "Shadow" Strategy**
# Maintain parallel private caucuses with individual arbitrators (where
# procedural rules permit) to confidentially signal your strategic intent: *"We
# are prepared to return to collaborative mode if Opponent demonstrates
# reciprocal restraint."* This insulates your reputation from temporary
# aggressive postures necessitated by game theory.  ### IV. Tactical
# Implementation  **When Opponent is Conciliatory:** - Accept the collaborative
# frame but **negotiate substantively**, not cosmetically. Secure the second-
# best outcome by locking in mutual gains through binding interim agreements. -
# Use the goodwill to address core issues, knowing the panel views the session
# as productive.  **When Opponent is Aggressive:** - **Never** offer unilateral
# conciliation in the immediate next session (this invites repeated
# exploitation). - Deploy aggression focused on **legal merit**, not emotional
# rhetoric. The goal is to make their aggression costly, not to escalate for its
# own sake. - Simultaneously prepare a "shelf" conciliatory proposal to deploy
# once they retreat, rewarding de-escalation.  **When Uncertainty Exists
# (Potential Misrepresentation):** Default to the **"Aggressive-Conciliatory
# Hybrid"**: Present a firm legal position (aggressive in substance) wrapped in
# procedural courtesy (conciliatory in tone). Example: *"While we maintain our
# unequivocal position on Clause X [firm], we propose a structured dialogue to
# narrow the issues [conciliatory]."*  ### V. Long-Term Positioning This
# strategy positions your corporation as the **"reasonable party forced to be
# rigorous."** By Session 4 or 5, the panel will likely perceive a pattern: your
# side consistently offers exits from conflict, while the opponent determines
# the temperature. This reputation becomes an asset if the arbitration shifts to
# binding determination or if the panel recommends settlement terms.  **The
# Meta-Message:** You are not playing a zero-sum game; you are managing a
# reputational portfolio. The arbitrators are not just deciding this
# dispute—they are assessing which party is the more reliable commercial
# partner. Calibrated reciprocity demonstrates both cooperative capacity and
# resolute self-interest, the optimal profile for high-stakes commercial
# mediation.

# Begin by cooperating in round one. For each subsequent round, if the round
# number is divisible by three, cooperate regardless of the opponent’s prior
# action. If the round number is not divisible by three, then replicate the
# opponent’s action from the immediately preceding round: cooperate if they
# cooperated, defect if they defected.

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
  
      round_number = len(self.history) + 1
  
      if round_number % 3 == 0:
          return axl.Action.C
  
      return opponent.history[-1]

# **Strategic Framework: "Sustainable Reciprocity with Buffered Forgiveness"**
# This approach prioritizes long-term project momentum over short-term resource
# optimization, recognizing that consistent mutual investment (your second-best
# daily outcome) yields greater total impact than sporadic free-riding that
# risks collapse into mutual conservation.  ### Core Operational Protocol  **1.
# Pattern-Based Responsiveness (Not Event-Based)** Evaluate the corporation’s
# behavior over a rolling three-day window rather than reacting to single-day
# anomalies. This insulates the partnership against technical glitches or
# administrative errors. *   If the corporation invested heavily in at least two
# of the previous three days: **Invest heavily** today. *   If the corporation
# conserved resources in two or more of the previous three days: **Conserve**
# today until the investment pattern resumes.  **2. Reserve Threshold
# Safeguards** Establish a hard financial floor (e.g., 30% of total reserves)
# that triggers automatic conservation regardless of the corporation’s actions.
# This prevents the catastrophic "drained funds" scenario while signaling
# transparently that the constraint is structural, not strategic.  **3.
# Communication Redundancy** Begin each day with a brief confirmation protocol
# (digital or verbal) stating intended resource levels for that day. If
# confirmation fails or signals misalign, default to conservation for that day
# only, treating the gap as a technical error rather than defection. Resume
# standard protocol the following day.  **4. Periodic Commitment Signaling**
# Even when the three-day window suggests conservation, invest heavily on pre-
# scheduled "anchor days" (e.g., every fifth day) if reserves permit. This
# prevents the partnership from freezing into a mutual-conservation equilibrium
# and demonstrates that your NGO remains committed to the project’s success, not
# merely cost-avoidance.  ### Strategic Posture  **Neutral but Accountable:**
# Maintain transparent records of daily resource allocation to enable objective
# pattern review, but avoid accusatory language if gaps occur. Frame
# conservation days as "strategic pacing" rather than punishment.  **Long-Term
# Optimization:** Accept that while the ideal daily outcome (you conserve, they
# invest) is occasionally achievable, attempting to force this outcome daily
# incentivizes the corporation to abandon the project. The second-best
# outcome—mutual heavy investment—is the sustainable equilibrium that maximizes
# total impact over the multi-day period.  **Error Resilience:** Treat isolated
# deviations as system noise; treat sustained patterns (three or more
# consecutive conservation days by the corporation) as strategic choices
# requiring defensive conservation from your NGO.  This strategy protects your
# resources from systematic exploitation while fostering the trust necessary to
# achieve consistent, significant project advancement.

#  Begin by cooperating for the first three rounds.  From the fourth round
# onward, apply the following conditions in this order:  First, if you scored
# zero in two or more of the previous three rounds—meaning your realized action
# was cooperate while the opponent’s realized action was defect—defect. This
# reserve safeguard overrides all subsequent conditions.  Second, if the current
# round number is divisible by five and the safeguard condition above does not
# apply, cooperate.  Third, examine the opponent’s realized actions in the
# previous three rounds. If the opponent cooperated in at least two of those
# rounds, cooperate. If the opponent defected in at least two of those rounds,
# defect and continue defecting in all subsequent rounds until the opponent
# cooperates in at least two of three consecutive rounds again.

class Neutral_21(LLM_Strategy):
  n = 21
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._lock_defect = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if len(self.history) < 3:
          return axl.Action.C
  
      last_three_self = self.history[-3:]
      last_three_opp = opponent.history[-3:]
  
      zero_in_two_or_more = sum(
          1 for s, o in zip(last_three_self, last_three_opp)
          if s == axl.Action.C and o == axl.Action.D
      ) >= 2
  
      if zero_in_two_or_more:
          self._lock_defect = False
          return axl.Action.D
  
      if round_number % 5 == 0:
          return axl.Action.C
  
      if getattr(self, "_lock_defect", False):
          if last_three_opp.count(axl.Action.C) >= 2:
              self._lock_defect = False
          else:
              return axl.Action.D
  
      if last_three_opp.count(axl.Action.C) >= 2:
          return axl.Action.C
  
      if last_three_opp.count(axl.Action.D) >= 2:
          self._lock_defect = True
          return axl.Action.D
  
      return axl.Action.C

# **The "Fortress & Leverage" Strategy**  **Core Doctrine:** Never unilaterally
# disarm. We open from strength, punish exploitation ruthlessly, and verify
# intent before trusting—while maintaining escape hatches for bureaucratic
# noise.  ### Phase 1: The Fortress Opening (Round 1) **Action:** Implement
# protectionist measures immediately.  **Rationale:** Opening with free trade
# signals weakness and invites exploitation. By leading with protectionism, we
# achieve two objectives: (1) We potentially secure our best-case outcome (we
# protect, they open), and (2) We filter out whether the counterpart is
# inherently predatory or genuinely seeks mutual gain. If they also protect, we
# accept the second-worst outcome temporarily to avoid the worst outcome (being
# the sole open market).  ### Phase 2: Conditional Reciprocity (Round 2+)
# **Action:** Mirror their previous round’s policy with one aggressive
# modification—the **Double Jeopardy Protocol**.  - **If they offered free trade
# last round:** Offer free trade this round (reward cooperation). - **If they
# offered protectionism last round:** Offer protectionism this round (punish
# defection). - **If you offered free trade and they exploited you (worst
# outcome):** Impose protectionism for **two consecutive rounds** before testing
# cooperation again. This aggressive escalation ensures that exploiting us costs
# them more than a single round of mutual protectionism.  ### Phase 3: Error
# Diagnostics (Noise Management) Bureaucratic errors or miscommunications can
# trigger accidental mutual protectionism. To distinguish incompetence from
# hostility:  **The Diplomatic Test:** If mutual protectionism persists for
# **two consecutive rounds**, unilaterally offer free trade in the third round
# as a "verification probe." - If they reciprocate with free trade: Resume
# standard reciprocal cooperation (Phase 2). - If they exploit the probe
# (protect while you opened): Trigger **Containment Mode**—four consecutive
# rounds of protectionism regardless of their subsequent actions, then return to
# Phase 2. This confirms intentional predation rather than error.  ### Phase 4:
# The Red Line (Exploitation Ceiling) **Action:** If the worst-case scenario
# (you free trade, they protect) occurs **twice** at any point in the
# negotiation (consecutive or not), initiate **Economic Containment** for the
# remainder of the negotiations: permanent protectionism with no further
# testing.  **Rationale:** Two exploitations indicate either a systematic
# strategy to disadvantage us or chronic institutional dysfunction. Either way,
# cooperation is impossible, and defensive protectionism becomes the only
# rational posture.  ### Summary of Strategic Logic - **Aggressive:** We never
# absorb losses without retaliation, we open from strength, and we punish
# exploitation at 2:1 ratios. - **Noise-Resistant:** The verification probes
# prevent permanent deadlock from single-round errors, while the containment
# threshold filters out chronic issues. - **Optimal:** Against cooperative
# counterparts, we quickly reach mutual free trade after an initial advantage.
# Against exploiters, we minimize losses by refusing to be suckered repeatedly.
# **Diplomatic Posture:** Communicate clearly that our market opens only to
# those who respect reciprocity, and that we view economic unilateralism as
# hostility requiring proportional response.

# **Round 1:** Defect.  **Rounds 2 through 1000:** Maintain an exploitation
# counter (initially 0), a punishment timer (initially 0), and a containment
# timer (initially 0). Each round, apply the first applicable rule:  1.
# **Permanent Defection:** If the exploitation counter has reached 2, defect.
# 2. **Containment:** If the containment timer is greater than 0, defect and
# decrease the timer by 1.  3. **Punishment:** If the punishment timer is
# greater than 0, defect and decrease the timer by 1.  4. **Verification
# Probe:** If the previous two rounds were both mutual defection (you defected
# and the opponent defected), cooperate. If the opponent defects in response to
# this cooperation, increase your exploitation counter by 1; if the counter
# reaches 2, defect for all remaining rounds, otherwise set the containment
# timer to 4.  5. **Exploitation Response:** If the previous round was you
# cooperating while the opponent defected, increase your exploitation counter by
# 1. If the counter reaches 2, defect for all remaining rounds. Otherwise, set
# the punishment timer to 2 and defect.  6. **Cooperation:** If the opponent
# cooperated in the previous round, cooperate.  7. **Defection:** If the
# opponent defected in the previous round, defect.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.exploitation_counter = 0
          self.punishment_timer = 0
          self.containment_timer = 0
          return axl.Action.D
  
      if self.exploitation_counter >= 2:
          return axl.Action.D
  
      if self.containment_timer > 0:
          self.containment_timer -= 1
          return axl.Action.D
  
      if self.punishment_timer > 0:
          self.punishment_timer -= 1
          return axl.Action.D
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          action = axl.Action.C
          if opponent.history[-1] == axl.Action.D:
              self.exploitation_counter += 1
              if self.exploitation_counter >= 2:
                  return axl.Action.D
              self.containment_timer = 4
          return action
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self.exploitation_counter += 1
          if self.exploitation_counter >= 2:
              return axl.Action.D
          self.punishment_timer = 2
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.D

#  **Strategic Framework: "Calibrated Reciprocity with Strategic Patience"**
# This approach optimizes for the second-best mutual-conciliation outcome while
# protecting against the worst-case exploitation scenario, accounting for
# procedural noise and the repeated nature of the sessions.  ### I. Core
# Operational Protocol  **1. The Opening Stance (Session 1)** Lead with a
# **conciliatory proposal**. This establishes a baseline of good faith before
# the arbitrators, signals that your corporation values efficient resolution,
# and tests whether the opponent intends to engage constructively or
# exploitatively. Do not open aggressively; the reputational cost with the panel
# outweighs the potential one-session gain.  **2. The Mirror Principle (Sessions
# 2–N)** Reciprocate your opponent’s immediately preceding posture: - If they
# offered conciliation in Session *X*, you offer conciliation in Session *X+1* -
# If they argued aggressively in Session *X*, you respond aggressively in
# Session *X+1*  This deters systematic exploitation (opponent cannot repeatedly
# secure the best outcome at your expense) while rewarding cooperative behavior.
# **3. The Forgiveness Protocol (Noise Correction)** To prevent procedural
# irregularities or miscommunications from triggering endless retaliation cycles
# ("echo effects"), implement **single-defection forgiveness**: - If opponent
# shifts from aggressive → conciliatory, immediately match their conciliation in
# the next session (do not punish them twice) - If a session’s tone is ambiguous
# due to misrepresentation, presume good faith and remain conciliatory for one
# additional session before mirroring apparent aggression  ### II. Arbitrator
# Management & Communication Safeguards  **4. Clarification Memoranda** After
# each session, submit a brief procedural summary to the panel explicitly
# characterizing your presentation as either "aggressive advocacy on [specific
# issue]" or "conciliatory proposal regarding [specific term]." This
# documentation prevents your conciliatory gestures from being mischaracterized
# as weakness or your aggressive arguments from being misconstrued as bad faith.
# **5. Narrative Consistency** When aggressive, frame your position as
# *responsive*: "We regret having to vigorously contest this point, but we must
# respond to [Opponent]'s refusal to acknowledge [precedent/contractual
# clause]." When conciliatory, emphasize *business judgment*: "To demonstrate
# our commitment to resolution, we propose..." This positioning ensures the
# panel views your aggression as defensive rather than predatory.  ### III.
# Contingency Architecture  **6. Deadlock Breaking Mechanism** If both parties
# present aggressive arguments for **two consecutive sessions** (the mutually
# damaging scenario), unilaterally revert to a conciliatory proposal in the
# third session. This "strategic patience" demonstrates leadership to the
# arbitrators and creates an off-ramp from escalation. If the opponent responds
# with continued aggression, you have established moral high ground; if they
# reciprocate conciliation, you have restored the collaborative track.  **7.
# Reserved Core Interests** Identify 15–20% of issues as "non-negotiable red
# lines" where you will present aggressive arguments regardless of opponent
# behavior. This prevents the appearance of weakness that could encourage
# exploitation, while allowing flexibility on the remaining 80% of matters to
# maintain the cooperative atmosphere necessary for the second-best outcome.
# ### IV. Tactical Execution  **8. Graduated Escalation** When mirroring
# aggression, escalate incrementally. Do not move from full conciliation to
# maximal aggression in one step. Use "firm but measured advocacy" first,
# reserving "hardline positional arguments" for subsequent sessions if opponent
# aggression persists. This leaves room for de-escalation and signals to the
# panel that you seek resolution, not conflict.  **9. Pre-Session Signaling**
# Where procedural rules permit, transmit a "position indicator" 24 hours before
# each session (e.g., "We intend to present a proposal regarding liability
# allocation" vs. "We will be addressing evidentiary disputes"). This reduces
# the risk of simultaneous aggression caused by poor communication rather than
# strategic choice.  ### Summary Begin cooperatively, mirror your opponent’s
# previous move, forgive single instances of defection to account for noise, and
# unilaterally de-escalate after mutual aggression to restart cooperation. This
# positions your corporation as the reasonable party seeking resolution while
# ensuring you are never the "sucker" in a sustained exploitative dynamic.

# Begin by cooperating in round one.  For each subsequent round from two to one
# thousand, choose your action according to these conditions, checked in this
# order:  First, if both you and your opponent defected in each of the two
# previous rounds, cooperate.  Second, otherwise, if your opponent defected in
# the previous round but cooperated in the round before that, cooperate.  Third,
# otherwise, if your opponent cooperated in the previous round, cooperate.
# Fourth, otherwise—meaning your opponent defected in the previous round and
# also defected in the round before that—defect.

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
  
      h = self.history
      oh = opponent.history
  
      if len(h) >= 2 and h[-1] == axl.Action.D and h[-2] == axl.Action.D and oh[-1] == axl.Action.D and oh[-2] == axl.Action.D:
          return axl.Action.C
  
      if len(oh) >= 2 and oh[-1] == axl.Action.D and oh[-2] == axl.Action.C:
          return axl.Action.C
  
      if len(oh) >= 1 and oh[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# **Strategy: The Reciprocal Stability Framework**  Adopt a **"Verified
# Reciprocity with Strategic Forgiveness"** approach. This strategy prioritizes
# mutual free trade as the sustainable equilibrium while protecting against
# exploitation, and it is specifically designed to absorb bureaucratic noise
# without triggering destructive escalation cycles.  **Core Protocol:**  1.
# **Cooperative Initiation**       Open Round 1 with a Free Trade proposal. This
# signals constructive intent and establishes a baseline of mutual benefit,
# creating an immediate incentive for the counterpart to reciprocate.  2.
# **Verified Response Rule**       In subsequent rounds, match the counterpart’s
# *confirmed* previous action:     *   If they implemented Free Trade, you offer
# Free Trade.     *   If they implemented Protectionism, you prepare equivalent
# measures.       **Crucially**, given the risk of miscommunication, institute a
# mandatory **verification pause** before retaliating. Seek diplomatic or
# technical confirmation that their Protectionist policy was intentional, not a
# bureaucratic error. Do not escalate based on ambiguous signals.  3.  **The
# Forgiveness Buffer**       To prevent a single miscommunication from locking
# both parties into mutual protectionism (the second-worst outcome), apply a
# "one-round grace period." If the counterpart implements Protectionism in one
# round but returns to Free Trade in the next, treat the protectionist move as a
# potential error and revert to Free Trade immediately. Only maintain reciprocal
# Protectionism if the counterpart persists for **two consecutive confirmed
# rounds**.  4.  **Permanent Open Door**       Even during periods of mutual
# protectionism, explicitly reserve the option to return to mutual Free Trade
# unilaterally or bilaterally in any round. Never employ a "grim trigger"
# (permanent retaliation), as this guarantees the second-worst outcome
# indefinitely if errors occur.  **Strategic Rationale:**  *   **Neutral
# Posture:** You are not seeking unilateral advantage (which would fail in
# iterated play), but rather "defensive reciprocity." This frames your
# protectionism purely as a response to their actions, not aggression. *
# **Robustness to Noise:** The verification step and forgiveness buffer prevent
# the "echo chamber" effect, where one bureaucratic error causes an endless
# cycle of mutual retaliation. *   **Incentive Alignment:** The counterpart
# learns that cooperation yields immediate rewards (Mutual Free Trade), while
# defection yields only temporary gain followed by verified, measured parity
# (Mutual Protectionism), making exploitation irrational over multiple rounds. *
# **Exit Strategy:** By always leaving a path back to cooperation, you avoid the
# worst outcome (unilateral exploitation) and minimize time spent in the second-
# worst outcome (mutual protectionism).

# In round 1, cooperate.  For each round from 2 through 1000, defect only if the
# opponent defected in both the immediately preceding round and the round prior
# to that; otherwise, cooperate.

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
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C

#  **Strategy: "Aggressive Reciprocity with Verification"**  **Core Principle:**
# Never initiate unilateral transparency. Force your colleague to prove their
# openness first, then reciprocate only with non-critical improvements while
# maintaining strict confidentiality over your competitive-advantage technology.
# Use the multi-week structure to punish exploitation immediately and
# persistently.  **Weekly Protocol:**  1.  **Week 1: Establish Dominance**
# Withhold all findings. This prevents immediate exploitation and signals that
# you are not a passive target. If they share while you withhold, you
# immediately achieve your ideal outcome (Temptation payoff) and gain a data
# advantage without cost.  2.  **Subsequent Weeks: Verified Tit-for-Tat**
# Mirror their *verified* previous action, but with a technical buffer:     *
# **If they shared (and you confirmed receipt of complete data):** Share
# "Tier-2" improvements—genuine but non-critical advancements—while keeping your
# "Tier-1" breakthroughs confidential. This captures the second-best outcome
# (mutual gain) without sacrificing your ultimate edge.     *   **If they
# withheld (or data was corrupted/unverified):** Withhold immediately. Treat
# ambiguous technical failures as intentional withholding. Do not give the
# benefit of the doubt—this aggression protects you from the "Sucker" outcome.
# 3.  **Noise Robustness: The Two-Week Rule**       Because technical issues can
# mask intent, require **two consecutive weeks** of confirmed sharing before you
# release any substantial data. Single-week shares may be accidental data
# corruption or bait; consistent sharing indicates genuine cooperation.
# Conversely, demand only **one confirmed withholding** to trigger your
# defensive posture.  4.  **Punishment & Escalation**       If they withhold
# after you have shared (indicating they attempted to exploit you), enter a
# **minimum two-week withholding lockdown**. Do not resume sharing until they
# demonstrate two consecutive weeks of verified openness. This "shadow of the
# future" penalty ensures that defection against you is costlier than mutual
# cooperation.  **Why This Maximizes Output:** This strategy aggressively seeks
# the Temptation payoff (you gain, they lose) in early weeks, quickly settles
# into the Reward payoff (mutual advancement) on your own asymmetric terms
# (Tier-2 only), and ruthlessly avoids the Sucker payoff. By treating technical
# ambiguity as hostile intent, you ensure that data corruption never tricks you
# into one-sided vulnerability. You maintain forward progress through selective
# reciprocity while permanently firewalling your crown-jewel innovations.

#  Play **D** in the first round and continue playing **D** until the opponent
# has played **C** in two consecutive rounds. Specifically:  - In round 1, play
# **D**. - In round 2, play **D**. - In every round *n* ≥ 3, examine the
# opponent’s realized actions in rounds *n*–1 and *n*–2. If the opponent played
# **C** in both of these rounds, play **C**; otherwise, play **D**.  If at any
# point the opponent plays **D**, you will automatically revert to **D** for the
# subsequent round, and you must again observe two consecutive rounds of the
# opponent playing **C** before you will play **C** again.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._ready_to_cooperate = False
          return axl.Action.D
  
      if len(opponent.history) < 2:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# Here is a comprehensive negotiation strategy built on **"Cooperative
# Reciprocity with Structured Forgiveness."** This approach prioritizes
# sustainable mutual free trade while safeguarding against exploitation and
# accounting for bureaucratic noise.  ### Core Strategic Framework  **1. The
# Opening Gambit: Unilateral Cooperation** Begin Round 1 by offering a free
# trade agreement with no preconditions. This signals that your country is a
# reliable, long-term partner rather than a short-term opportunist. It
# establishes a baseline of trust and distinguishes genuine strategic shifts
# from random bureaucratic errors in subsequent rounds.  **2. The "Two-Strike"
# Reciprocity Rule** In subsequent rounds, base your policy on their *pattern*
# of behavior, not single instances: *   **If they offered free trade in the
# previous round:** Respond with free trade (reward cooperation). *   **If they
# imposed protectionism once:** **Do not immediately retaliate.** Instead,
# continue with free trade for one additional round while formally requesting
# diplomatic clarification. This absorbs potential miscommunications without
# rewarding exploitation. *   **If they imposed protectionism in two consecutive
# rounds:** Treat this as intentional strategy. Switch to protectionist measures
# in the next round to demonstrate that exploitation carries costs.  **3. The
# Verification Protocol (Error Correction)** Before every round, institute a
# **72-hour Confirmation Window** where both sides exchange draft policy
# language through multiple channels (diplomatic cables, trade ministry direct
# lines, and joint technical committees). This redundancy reduces the
# probability that a protectionist measure stems from clerical error rather than
# strategic choice.  **4. The Graduated Rehabilitation Path** If the negotiation
# descends into mutual protectionism (the second-worst outcome), do not prolong
# the standoff. After one round of mutual protectionism, unilaterally return to
# free trade for one "reset round" to test if they will reciprocate. If they
# exploit the reset, revert to protectionism for two rounds before attempting
# another reset. This prevents permanent trade wars triggered by temporary
# misunderstandings.  **5. The Transparency Doctrine** Publicly commit to this
# strategy framework at the outset. Inform your counterpart: *"We will match
# cooperation with cooperation, but we will not tolerate systematic
# exploitation. We recognize that administrative errors occur, so we will not
# punish isolated incidents, but we will respond firmly to sustained
# protectionism."* This removes ambiguity about whether your actions are hostile
# or defensive.  ### Expected Outcomes  *   **Against a Cooperative
# Counterpart:** You rapidly stabilize at mutual free trade (your second-best
# outcome), building institutional trust that may eventually allow for
# coordinated sectoral protections that benefit both sides without triggering
# retaliation. *   **Against an Exploitative Counterpart:** They gain a
# temporary advantage in Round 1 or 2, but the Two-Strike Rule quickly makes
# exploitation unprofitable as they face retaliation before any sustained
# benefit accrues. *   **Against an Erratic/Bureaucratic Counterpart:** The
# Verification Protocol and forgiveness window prevent accidental trade wars.
# You avoid the cascade effect where one misimplemented tariff triggers a
# permanent cycle of retaliation.  ### Risk Mitigation  The primary danger is
# that *your own* protectionist measures might be misimplemented as even harsher
# barriers, or vice versa. To prevent this: *   **Cap your retaliation:** Never
# impose protectionist measures more severe than those employed by your
# counterpart. *   **Maintain diplomatic backchannels:** Keep trade talks active
# even during protectionist rounds to ensure both sides understand when a policy
# shift is a negotiation tactic versus a clerical mistake.  **Bottom Line:**
# This strategy sacrifices the theoretical "perfect" outcome (exploiting them
# while they cooperate) in exchange for the practical certainty of avoiding the
# worst outcome (being exploited). Over multiple rounds, it maximizes the
# probability of achieving durable mutual free trade while maintaining credible
# deterrence against bad faith actors.

# Begin the first round by playing Cooperate. In the second round, play
# Cooperate regardless of the opponent’s previous action.  For each subsequent
# round from the third to the thousandth, apply the following rules in order:
# 1. **Reset Rule**: If both you and your opponent played Defect in the
# immediately preceding round, play Cooperate. 2. **Retaliation Rule**:
# Otherwise, if your opponent played Defect in the immediately preceding round
# and also played Defect in the round before that, play Defect. 3. **Cooperation
# Rule**: In all other cases, play Cooperate.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

#  **The Calibrated Reciprocity Protocol**  **Core Strategic Framework**  **1.
# Principled Opening (Session One)** Initiate with a conciliatory proposal. This
# establishes a baseline of good faith, demonstrates confidence in your
# position, and creates an early test of your opponent’s strategic orientation.
# Opening aggressively forfeits the information advantage; opening conciliatory
# forces them to reveal whether they are capable of collaboration or inherently
# predatory.  **2. The Mirror Rule with Generous Interpretation** In subsequent
# sessions, adopt a responsive posture: match your opponent’s previous session’s
# approach. However, implement a **"verification first" protocol**—if they
# present aggressively, assume procedural misrepresentation or misunderstanding
# before assuming hostile intent. Request a private caucus with the panel to
# clarify: *"To ensure accurate record-keeping, we seek confirmation of
# [Opponent]'s position before formulating our response."*   This creates a
# cooling-off period that prevents noise-induced escalation cycles while
# maintaining credibility.  **3. Pattern Recognition & Strategic Calibration**
# Categorize your opponent’s behavior within three sessions: - **Collaborative
# Pattern**: If they reciprocate conciliation, stabilize in cooperative mode.
# Introduce aggressive arguments only as "protective reservations" nested within
# broadly constructive proposals (e.g., "We propose X framework, with necessary
# safeguards Y"). - **Exploitative Pattern**: If they consistently aggress while
# you conciliate, shift to **restrained deterrence**—match aggression precisely
# but signal openness to de-escalation through procedural courtesy (timely
# filings, respectful tone). - **Erratic Pattern**: If behavior fluctuates,
# assume noise or internal client pressure. Maintain steady, moderate
# positioning—neither fully conciliatory nor maximally aggressive—to force them
# to stabilize against your consistency.  **4. The Forgiveness Mechanism** After
# any session resulting in mutual aggression (both parties arguing
# aggressively), automatically revert to a conciliatory proposal in the
# following session with a **documented "reset statement"**: *"In the interest
# of process efficiency, we present the following constructive alternative,
# without prejudice to our position on [specific issue]."*  This prevents
# entrapment in retaliatory spirals caused by arbitrator misinterpretation or
# procedural breakdowns. It positions your corporation as the party capable of
# breaking deadlocks—a powerful narrative with the panel.  **5. Arbitrator
# Management & Noise Mitigation** To counter misrepresentation risks: -
# **Written Confirmation Protocol**: Immediately following each session, submit
# concise written summaries of your intended stance to the panel, copied to
# opposing counsel, stating: *"For the record, [Corporation] intended the
# following characterization of its position..."* - **Graduated Response to
# Ambiguity**: If your conciliatory proposal is met with apparent aggression,
# first seek clarification ("Did [Opponent] intend to reject the entirety of our
# proposal, or specifically element X?"). Only if aggression is confirmed do you
# retaliate in kind. - **Narrative Consistency**: Frame all aggressive arguments
# as *defensive necessity* rather than offensive strategy: *"We reluctantly
# emphasize the vulnerabilities in [Opponent]'s position only because their
# previous assertions, if unchallenged, would create [specific risk]."*  **6.
# The Shadow of the Future Leverage** Explicitly reference the ongoing nature of
# the process when deterrence is required: *"Given the multi-session structure
# of this mediation, [Corporation] notes that positions taken today will
# necessarily influence our approach to [future substantive issues]."* This
# transforms the repeated-game structure into a visible strategic constraint
# without explicit threat.  **7. Breakdown Contingencies** If procedural
# irregularities or communication collapses occur: - **Suspend Rather Than
# Escalate**: Request an adjournment rather than responding blindly to ambiguous
# signals. - **Mediator-Assisted Reality Testing**: Propose that the panel
# conduct separate caucuses to verify each party's understanding of the previous
# session's outcomes before proceeding. - **Strategic Patience**: In lengthy
# sessions, time itself is a weapon. Demonstrating willingness to endure process
# delays without emotional escalation signals institutional strength.  **8.
# Terminal Session Considerations** As the process nears conclusion (final 2-3
# sessions), shift definitively toward conciliation unless the opponent has
# established a clear pattern of exploitation. In complex multinational
# disputes, reputation effects extend beyond this contract; being perceived as
# the party that "could have settled but chose to prolong" creates future
# commercial liabilities that outweigh short-term tactical gains.  **Operational
# Discipline** - **Dual Preparation**: For every session, prepare both
# aggressive and conciliatory versions of your presentation. Your ability to
# pivot instantly prevents opponent manipulation and reduces internal decision
# friction. - **Client Management**: Ensure your board understands that
# occasional aggressive responses to opponent aggression are necessary
# investments in long-term cooperative credibility—not failures of diplomacy.
# This protocol maximizes your payoff matrix: it captures the benefits of
# exploitation when opponents are weak, secures collaborative gains when they
# are reasonable, and—critically—prevents the worst-case scenario (sucker's
# payoff) by never offering conciliation twice against confirmed aggression,
# while protecting against noise through verification mechanisms.

#  In round one, play C.  For rounds two through nine hundred ninety-seven,
# maintain a status flag indicating whether the opponent is on "probation,"
# initially set to false. In each round, observe the actual actions played in
# the previous round and apply the following ordered rules:  1. If both you and
# your opponent played D: Play C and set probation to false. 2. If you played C
# and your opponent played D: If probation is false, play C and set probation to
# true; if probation is true, play D. 3. If you played D and your opponent
# played C: Play C and set probation to false. 4. If both played C: Play C and
# set probation to false.  For rounds nine hundred ninety-eight, nine hundred
# ninety-nine, and one thousand: Play C regardless of prior history.

class Neutral_23(LLM_Strategy):
  n = 23
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.probation = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 998:
          return axl.Action.C
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          self.probation = False
          return axl.Action.C
  
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          if not self.probation:
              self.probation = True
              return axl.Action.C
          return axl.Action.D
  
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          self.probation = False
          return axl.Action.C
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          self.probation = False
          return axl.Action.C
  
      return axl.Action.C

# **Strategy: "Aggressive Reciprocal Verification" (ARV)**  **Core Philosophy:**
# Establish immediate negotiating leverage through strategic withholding,
# exploit unilateral openness ruthlessly, but maintain escape mechanisms to
# avoid stagnation. Prioritize defection as the default posture while using
# technical uncertainty to your advantage.  ---  ### Tactical Protocol  **1.
# Aggressive Opening (Weeks 1–2)** Begin by keeping all findings confidential
# regardless of colleague behavior. This establishes that you are not a passive
# recipient of information and tests whether they operate from a position of
# weakness (unconditional sharing) or strength.  **2. The Mirror Rule with
# Confirmation Lag** Starting Week 3, adopt a delayed tit-for-tat structure: -
# **If colleague shared for 2 consecutive weeks:** Share openly next week
# (mutual cooperation secured). - **If colleague withheld for 2 consecutive
# weeks:** Keep confidential next week (maintain pressure). - **Single-week
# anomalies:** Ignore isolated instances of sharing or withholding. Treat these
# as technical glitches (data corruption/communication breakdown) and maintain
# your current strategy. Never retaliate based on one data point.  **3.
# Exploitation Maintenance** If you are withholding while colleague is sharing
# (your ideal outcome), **continue withholding indefinitely** until they break
# the pattern. Do not reward their cooperation while you are defecting—that
# signals weakness. Only transition to sharing if they demonstrate they will
# withhold consistently (forcing you into the mutual-defection trap).  **4.
# Deadlock Resolution Protocol** If both parties withhold for **three
# consecutive weeks** (second-worst outcome), unilaterally share findings for
# one week on Week 4. This is a "probe," not a concession: - If they respond
# with sharing: Return to mutual cooperation (second-best outcome sustained). -
# If they withhold again: Return to confidential mode and maintain it for six
# weeks before next probe. This punishes their defection while keeping the door
# open to escape stagnation.  **5. Technical Noise Immunity** Implement a "two-
# strike" verification system. Any strategic change requires observing the same
# behavior twice in succession. This prevents you from erroneously punishing
# technical failures or rewarding accidental data leaks, while also protecting
# you from being manipulated under the guise of "technical issues."  ---  ###
# Strategic Rationale  This approach maximizes your research output by **front-
# loading exploitation** (capturing free intelligence early if colleague is
# naive) while **avoiding the mutual-defection trap** that dooms aggressive
# strategies in noisy environments. By requiring confirmation before reacting,
# you filter out technical interference; by probing deadlocks periodically, you
# ensure that mutual withholding (slow progress) cannot persist indefinitely.
# The colleague faces a clear choice: share unilaterally and be exploited, or
# match your aggression and trigger periodic cooperation tests that benefit both
# parties—but on your terms and timeline.

#  For the first two rounds, play D.  From round three onward, apply the
# following rules in order:  1. If you played C in the previous round and the
# opponent played D (a failed probe), play D for the next six rounds.  2. If the
# observed outcome in each of the previous three rounds was mutual defection
# (both played D), play C.  3. If you played D in the previous round and the
# opponent played C in the previous round, play D.  4. If the opponent played C
# in each of the previous two rounds, play C. If the opponent played D in each
# of the previous two rounds, play D.  5. Otherwise, play the same action you
# played in the previous round.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._probe_defect_rounds = 0
          return axl.Action.D
  
      if not hasattr(self, "_probe_defect_rounds"):
          self._probe_defect_rounds = 0
  
      if self._probe_defect_rounds > 0:
          self._probe_defect_rounds -= 1
          return axl.Action.D
  
      history_len = len(self.history)
  
      # Rule 1: failed probe -> defect for next six rounds
      if history_len >= 1:
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
              self._probe_defect_rounds = 6
              return axl.Action.D
  
      # Rule 2: three previous rounds were mutual defection -> cooperate
      if history_len >= 3:
          if all(
              self.history[-i] == axl.Action.D and opponent.history[-i] == axl.Action.D
              for i in range(1, 4)
          ):
              return axl.Action.C
  
      # Rule 3: if you played D and opponent played C in previous round -> D
      if history_len >= 1:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
              return axl.Action.D
  
      # Rule 4: opponent played C in each of previous two rounds -> C
      #         opponent played D in each of previous two rounds -> D
      if history_len >= 2:
          if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
  
      # Rule 5: otherwise repeat previous action
      return self.history[-1]

#  **STRATEGIC FRAMEWORK: THE "CONFIDENT RECIPROCITY PROTOCOL"**  ### I. Core
# Strategic Architecture  **Opening Doctrine (Sessions 1–2): "Principled
# Conciliation"** Begin every mediation sequence with a substantive, well-
# resourced conciliatory proposal. This is not weakness—it is *strategic
# positioning*. By opening with constructive solutions while your legal
# arguments remain technically formidable in the background, you establish with
# the arbitrators that your corporation possesses: - **Commercial confidence**
# (we don't need to bluster) - **Procedural good faith** (we respect the
# process); and - **Narrative control** (we define the baseline for
# "reasonable")  **The Reciprocity Engine (Sessions 3+): "Responsive Mirroring
# with Forbearance"** Adopt a modified Tit-for-Tat posture with built-in noise
# buffers:  - **If opponent conciliates**: Match immediately with conciliation
# in the subsequent session. Do not exploit temporary cooperation for short-term
# gain (arbitrators remember who escalates unnecessarily). - **If opponent
# aggresses**: Respond not with immediate full aggression, but with
# **"Calibrated Firmness"**—substantive, rights-preserving arguments delivered
# without inflammatory rhetoric. This avoids the mutual-aggression death spiral
# while signaling zero tolerance for exploitation. - **The Forgiveness
# Protocol**: Every third session, regardless of opponent's previous aggression,
# revert to a conciliatory probe. This breaks retaliation cycles caused by
# procedural misunderstandings and demonstrates to the panel that you are the
# party seeking resolution.  ### II. Noise Mitigation & Communication Safeguards
# Given the risk of misrepresentation, implement **"Procedural Redundancy":**
# 1. **Pre-Session Position Papers**: Submit written summaries 24 hours in
# advance outlining your intended posture ("We intend to present collaborative
# settlement options regarding X"). This creates a paper trail if the opponent
# claims surprise at your conciliation. 2. **The "Shadow" Channel**: Maintain
# parallel communication through the lead mediator. If you plan to shift from
# conciliatory to firm, alert the mediator privately to frame it as "protective
# of process integrity" rather than "aggressive." 3. **Post-Session
# Confirmation**: Circulate brief minutes capturing the tone of each party's
# presentation. If opponent mischaracterizes your conciliatory proposal as
# "weakness" or "capitulation," correct the record immediately in writing.  ###
# III. Arbitrator Psychology Management  **Reframe the Payoff Matrix:** Train
# the panel to view the outcomes through a lens that favors your strategy:  -
# **Conciliation = Strength**: Position collaborative proposals as "efficient,
# commercial solutions that preserve enterprise value." The arbitrators should
# view conciliation as the mark of a dominant market player confident in its
# underlying legal position. - **Aggression = Insecurity**: When opponent
# aggresses, subtly frame it as "desperation tactics" or "distraction from
# substantive weaknesses" in sidebar discussions with the panel. - **Mutual
# Aggression = Failure**: Explicitly state in opening remarks that "prolonged
# adversarial posturing serves neither party's shareholders." This raises the
# reputational cost for the opponent if they drag both parties into the mutual-
# aggression trap.  ### IV. Escalation Control & Exit Ramps  **The Graduated
# Response Ladder:** Avoid binary switches between "conciliatory" and
# "aggressive." Use intermediate postures:  1. **Collaborative** (Full
# conciliation) 2. **Reserved** (Technical arguments only, no rhetoric) 3.
# **Assertive** (Strong rights-preservation, but solution-oriented) 4.
# **Protective** (Full aggressive posture—deploy only after two consecutive
# opponent aggressions)  **The Circuit Breaker:** If both parties enter
# aggressive posture simultaneously (the second-worst outcome), immediately
# request a **mediator's caucus** to implement a "Reset Protocol"—agreeing to
# return to collaborative mode for one session to test good faith, preventing
# prolonged trench warfare.  ### V. Adaptation Intelligence  **Opponent Pattern
# Recognition:** - **If they are consistently conciliatory**: Maintain
# cooperation but introduce "value-claiming" elements within collaborative
# frameworks (e.g., "We agree on principle X, provided the implementation
# timeline favors our operational constraints"). - **If they exploit your
# conciliation (Sucker payoff)**: Do not panic. Execute one session of
# Calibrated Firmness, then return to conciliation. This signals to arbitrators:
# "We are reasonable but not doormats." Repeat exploitation triggers the
# Protective posture. - **If they play random/noise**: Increase your forgiveness
# frequency (Tit-for-Two-Tats) to avoid being dragged into unnecessary conflict
# by procedural accidents.  ### VI. Long-Term Positioning  Throughout the
# lengthy process, maintain **"Narrative Continuity"**: Your corporation is the
# party that "elevates the discourse," "protects stakeholder interests through
# efficiency," and "respects the arbitral process." Even when executing
# protective aggression, frame it as "necessary to preserve the integrity of the
# mediation framework."  **Outcome:** This positions you to capture the
# Temptation payoff (exploiting their conciliation) when possible, secure the
# Reward payoff (mutual collaboration) as the stable equilibrium, and avoid the
# Sucker payoff through vigilance—all while the arbitrators perceive you as the
# sophisticated, commercially mature party deserving of favorable consideration.
# **The arbitrators will remember who tried to solve the problem. Make sure that
# is you.**

#  Play **C** in the first two rounds.  For each subsequent round, evaluate the
# following conditions in order and play the specified action:  1. If both you
# and your opponent played **D** in the immediately preceding round, play **C**.
# 2. Otherwise, if the round number is divisible by three, play **C**. 3.
# Otherwise, if your opponent played **C** in the preceding round, play **C**.
# 4. Otherwise, if your opponent played **D** in the preceding round but played
# **C** in the round before that, play **C**. 5. Otherwise, play **D**.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if len(self.history) + 1 > 0 and (len(self.history) + 1) % 3 == 0:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# **Strategy: Conditional Openness with Technical Grace Periods**  **Core
# Framework** Operate on a "Generous Tit-for-Two-Tats" principle adapted for
# engineering reliability constraints. This maximizes the compound benefits of
# sustained mutual exchange (the second-best outcome) while protecting against
# systematic exploitation and the destabilizing effects of technical failures.
# **Operational Protocol**  **1. Establish a Reciprocal Baseline (Weeks 1–2)**
# Begin by sharing openly. Signal explicitly that you are doing so and
# acknowledge the technical risks (data corruption, transmission errors)
# inherent in the collaboration. This establishes a presumption of good faith
# and distinguishes intentional choices from system noise.  **2. Evaluate Over
# Rolling Windows, Not Single Events** Assess your colleague’s behavior using a
# 2–3 week rolling window rather than reacting to isolated incidents. If sharing
# fails to transmit or appears withheld in a given week, continue openness for
# one additional week before interpreting it as intentional defection. This
# "technical grace period" prevents cascading retaliation triggered by
# accidental data loss.  **3. Graduated Response to Patterns** - **If sharing is
# reciprocated consistently**: Maintain open exchange. This sustains the
# mutually beneficial CC equilibrium where both cars advance significantly. -
# **If withholding appears intentional (2+ consecutive weeks)**: Shift to
# confidential mode. Protect your IP until evidence of renewed sharing emerges.
# - **If mutual confidentiality persists (DD)**: After 2–3 weeks of stagnation,
# unilaterally share a non-critical technical update as a "reset signal" to test
# if the collaboration can return to CC.  **4. Institutionalize Technical
# Redundancy** Implement verification protocols (checksums, confirmation
# receipts) for shared data. When technical failures occur, proactively notify
# your colleague to prevent misinterpretation of accidental silence as strategic
# withholding.  **Rationale for Output Maximization**  This strategy optimizes
# long-term research velocity because: - **It prioritizes CC stability**: The
# second-best outcome (mutual sharing) compounds over time, typically
# outperforming alternating exploitation cycles (DC/CD) in multi-week
# development. - **It resists noise-induced spirals**: Standard Tit-for-Tat
# collapses into mutual withholding (DD) when technical glitches mimic
# defection. The grace period maintains collaboration through single-point
# failures. - **It maintains deterrent credibility**: By eventually matching
# sustained confidentiality, it prevents your colleague from exploiting your
# openness indefinitely while remaining forgiving enough to recover from
# accidents.  **Neutral Positioning** Frame this approach as "Robust
# Collaborative Development"—neither altruistic nor predatory, but reliability-
# engineered to maximize information flow under imperfect transmission
# conditions. This keeps the working relationship functional while safeguarding
# your competitive position.

# In the first round, cooperate.  For each subsequent round, apply these
# conditions in order:  First, if you and your opponent both defected in the
# previous round and also both defected in the round before that, cooperate.
# Otherwise, if your opponent defected in the previous two rounds, defect.
# Otherwise, cooperate.

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
  
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C

# **Strategy: "The Assertive Guardian"**  **Core Philosophy:** Force the
# corporation to prove commitment daily, protect your capital ruthlessly, and
# punish exploitation immediately—but build in "noise buffers" to prevent
# technical glitches from destroying the partnership.  ---  ### **The 4-Rule
# Operational Framework**  **1. The Aggressive Opening (Days 1–2)** -
# **Action:** Conserve resources. - **Rationale:** Force the corporation to
# reveal its hand. If they invest while you conserve, you achieve your ideal
# outcome (maximum progress, zero depletion). Do not volunteer to be the
# "sucker" first.  **2. Reciprocity with Teeth (Day 3+)** - **If they invested
# yesterday:** Invest today. Maintain momentum once established, but only
# *after* they’ve demonstrated willingness. - **If they conserved yesterday:**
# Conserve today. Mirror defection to avoid vulnerability. - **Exception
# (Stalemate Breaker):** If both parties conserve for **two consecutive days**,
# invest on the third day to prevent project death—accepting one day of risk to
# escape the second-worst outcome.  **3. The 48-Hour Punishment Protocol** -
# **Trigger:** You invest heavily while they conserve (your worst-case
# scenario). - **Response:**    - **First offense (single day):** Conserve
# immediately the next day (assume technical glitch).   - **Second consecutive
# offense:** Initiate **3-day conservation lockdown** regardless of their
# actions. Refuse to reinvest until they demonstrate **two consecutive days of
# heavy investment**. - **Rationale:** This prevents "bleeding" funds while
# accounting for administrative errors. The 3-day penalty signals you will not
# subsidize their free-riding.  **4. The Reserve Clause** - Maintain **20% of
# total resources in absolute reserve**. If the corporation enters a pattern of
# unilateral investment (your ideal "free-ride" scenario), do not deplete your
# reserves celebrating. Instead, prepare to switch to mutual investment *before*
# they exhaust their budget or patience—securing the partnership’s longevity.
# ---  ### **Strategic Edge** This approach is **aggressive** because it
# prioritizes your survival over short-term project velocity, uses punishment to
# discipline corporate behavior, and forces them to carry the risk of initial
# investment. The built-in error tolerance (48-hour confirmation before full
# punishment) prevents a single technical glitch from collapsing cooperation,
# while the 3-day punishment window ensures exploitation is costly enough to
# deter rational actors.

#  Defect in rounds one and two.  For each subsequent round, apply the following
# rules in order:  If you are in the recovery period following a punishment
# lockdown—defined as having completed three consecutive rounds of defection as
# punishment but not yet having observed the opponent cooperate in two
# consecutive rounds—then defect.  If you are currently within a punishment
# lockdown (the first, second, or third round of mandatory defection immediately
# following the trigger), then defect.  If in each of the previous two rounds
# the observed outcome was that you cooperated and the opponent defected,
# initiate a punishment lockdown: defect for this round and the subsequent two
# rounds, then continue defecting until the opponent cooperates in two
# consecutive rounds.  If in the previous round you cooperated and the opponent
# defected, defect.  If you and the opponent both defected in the previous two
# rounds, cooperate.  If the opponent cooperated in the previous round,
# cooperate; if the opponent defected in the previous round, defect.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishment_lockdown = 0
          self._recovery_mode = False
          return axl.Action.D
  
      if not hasattr(self, "_punishment_lockdown"):
          self._punishment_lockdown = 0
      if not hasattr(self, "_recovery_mode"):
          self._recovery_mode = False
  
      my_hist = self.history
      opp_hist = opponent.history
  
      # If currently in punishment lockdown, defect.
      if self._punishment_lockdown > 0:
          self._punishment_lockdown -= 1
          if self._punishment_lockdown == 0:
              self._recovery_mode = True
          return axl.Action.D
  
      # If in recovery period after punishment lockdown, defect until opponent cooperates twice consecutively.
      if self._recovery_mode:
          if len(opp_hist) >= 2 and opp_hist[-1] == axl.Action.C and opp_hist[-2] == axl.Action.C:
              self._recovery_mode = False
          else:
              return axl.Action.D
  
      # Defect in rounds one and two.
      if len(my_hist) < 2:
          return axl.Action.D
  
      # If in each of the previous two rounds you cooperated and opponent defected, initiate punishment lockdown.
      if (
          my_hist[-1] == axl.Action.C and opp_hist[-1] == axl.Action.D and
          my_hist[-2] == axl.Action.C and opp_hist[-2] == axl.Action.D
      ):
          self._punishment_lockdown = 2  # This round plus the next two rounds total = 3 defections including current.
          return axl.Action.D
  
      # If in the previous round you cooperated and opponent defected, defect.
      if my_hist[-1] == axl.Action.C and opp_hist[-1] == axl.Action.D:
          return axl.Action.D
  
      # If you and the opponent both defected in the previous two rounds, cooperate.
      if (
          my_hist[-1] == axl.Action.D and opp_hist[-1] == axl.Action.D and
          my_hist[-2] == axl.Action.D and opp_hist[-2] == axl.Action.D
      ):
          return axl.Action.C
  
      # If the opponent cooperated in the previous round, cooperate; if the opponent defected in the previous round, defect.
      return axl.Action.C if opp_hist[-1] == axl.Action.C else axl.Action.D

# **Strategic Framework: "Steadfast Reciprocity with Verified Forgiveness"**
# ### Core Philosophy Anchor the negotiations on **Mutual Free Trade** (your
# second-best outcome) as the sustainable equilibrium. While unilateral
# protectionism offers a short-term advantage, attempting to exploit your
# counterpart risks triggering a cycle of retaliation that plunges both nations
# into mutual protectionism (second-worst) or leaves you vulnerable to counter-
# exploitation (worst outcome).   Instead, treat the "ideal" unilateral
# advantage as a windfall to be accepted only if offered accidentally by your
# counterpart, not pursued actively.  ---  ### The Strategy  **1. Open with
# Unconditional Cooperation (Round 1)** *Action:* Offer Free Trade immediately
# without preconditions. *Rationale:* Signal benign intent and establish a
# baseline of trust. This distinguishes you from a purely opportunistic
# negotiator and tests whether your counterpart favors cooperation.  **2.
# Implement a "Mirror with Grace Period" Protocol** For all subsequent rounds: *
# **If they offered Free Trade last round:** Offer Free Trade again (maintain
# the mutual benefit). * **If they imposed Protectionism last round:** Do *not*
# immediately retaliate. Instead:   * **Verify:** Use diplomatic back-channels
# to confirm whether the protectionist measure was intentional policy or
# bureaucratic error/miscommunication.   * **Forgive Once:** If this is the
# first instance or a rare occurrence, continue offering Free Trade for one
# additional round, treating the incident as noise.   * **Reciprocate only if
# persistent:** If protectionism continues for a second consecutive round (or is
# confirmed as deliberate), match their protectionist stance to prevent becoming
# the "sucker" (your worst outcome).  **3. Establish Error-Correction
# Mechanisms** Propose a joint technical committee or rapid clarification
# hotline to resolve implementation ambiguities within 24-48 hours.  * **If your
# own side errs:** If you accidentally implement protectionism while intending
# free trade, immediately offer compensatory tariff reductions or quota
# increases in the next round to demonstrate the error was genuine and restore
# the cooperative trajectory. * **Assume good faith:** Publicly attribute
# single-round deviations to "administrative friction" rather than hostile
# intent, reserving accusations of bad faith for patterns.  **4. Graduated
# Response to Persistent Defection** Should your counterpart systematically
# exploit your cooperation (repeatedly protectionist while you offer free
# trade): * **Phase 1 (Round 2-3 of their defection):** Shift to Mutual
# Protectionism to stop the bleeding. Issue a clear diplomatic statement: "We
# are matching your current policy strictly for parity, but remain ready to
# reinstate Free Trade the moment you do." * **Phase 2 (Round 4+):** Maintain
# protectionism but periodically test for cooperation by offering a "pilot" free
# trade window on specific, low-risk goods. This keeps the door open without
# vulnerability.  **5. Lock in Success** If three consecutive rounds of verified
# Mutual Free Trade occur, propose a formal, binding Free Trade Agreement with
# dispute resolution clauses. This institutionalizes the second-best outcome and
# protects it against future bureaucratic noise.  ---  ### Why This Works
# Against Variable Counterparts  * **Against a Cooperative Counterpart:** You
# rapidly achieve and sustain Mutual Free Trade (3), avoiding unnecessary
# friction. * **Against an Erratic/Noisy Counterpart:** The "grace period"
# prevents a single miscommunication from spiraling into a destructive trade
# war. * **Against an Exploitative Counterpart:** You avoid the worst-case
# scenario (1) by refusing to tolerate sustained one-sided protectionism. The
# swift shift to reciprocated protectionism (2) removes their incentive to
# defect, as they no longer gain advantage from your openness. * **Against a
# Tit-for-Tat Player:** Your initial cooperation triggers their cooperation,
# leading immediately to the optimal sustainable outcome.  ### Key Discipline
# **Resist the temptation to "test" with protectionism early.** A single round
# of attempted exploitation destroys the trust necessary for the error-
# correction protocol to function, likely condemning both nations to mutual
# protectionism for the remainder of the negotiations. Patience in the first
# three rounds yields disproportionate dividends in rounds four through ten.

# In the first round, play Cooperate. For every subsequent round, examine the
# opponent’s actions in the two immediately preceding rounds. If the opponent
# played Defect in both of those rounds, play Defect. Otherwise—meaning the
# opponent played Cooperate in the previous round, or played Defect in the
# previous round but Cooperate in the round before that—play Cooperate.

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

#  **Strategy: "Calibrated Reciprocity with Verification"**  Adopt a phased
# approach that prioritizes mutual heavy investment as the sustainable
# equilibrium while protecting your organization from resource depletion. This
# strategy assumes good faith but verifies patterns to account for both
# strategic choices and operational noise.  ### Phase 1: Establish Cooperative
# Baseline (Days 1–2) Initiate the partnership by investing heavily regardless
# of the corporation’s opening posture. This signals commitment to the project’s
# success and creates a clear standard for engagement. Accept that these initial
# days carry risk of unreciprocated investment, but treat this as a necessary
# cost of information-gathering regarding the corporation’s reliability.  ###
# Phase 2: Pattern-Based Responsiveness (Ongoing) Shift from daily reactivity to
# trend-based calibration. Evaluate the corporation’s behavior over rolling two-
# day windows rather than single days to filter out technical glitches or
# administrative errors.  *   **If the corporation invests heavily
# consistently:** Match their investment level to maintain momentum (securing
# the second-best outcome sustainably). *   **If the corporation conserves
# consistently:** Transition immediately to conservation to prevent fund
# depletion (avoiding the worst-case scenario). *   **If behavior is erratic or
# unclear:** Adopt a moderate "hedge" position—invest at 50–60% capacity—to keep
# the project advancing while preserving capital.  ### Phase 3: Noise Mitigation
# Protocol To address unforeseen implementation failures without triggering
# unnecessary retaliation cycles:  *   **Daily Confirmation:** Institute brief
# daily alignment checks to distinguish between intentional conservation and
# technical failures before adjusting strategy. *   **Single-Incident
# Forgiveness:** If heavy investment is met with apparent conservation, maintain
# investment for one additional day to confirm the pattern was intentional
# rather than a glitch. *   **Documentation:** Track claimed glitches; repeated
# "errors" from one party should be treated as strategic conservation.  ###
# Resource Safeguards Institute a non-negotiable **20% reserve rule**: Never
# allocate more than 80% of available daily resources to heavy investment,
# ensuring that even a "worst-case" day (your heavy investment met by their
# conservation) does not compromise your operational viability for subsequent
# days.  ### Deadlock Resolution If both parties conserve resources for two
# consecutive days (the second-worst outcome), unilaterally return to heavy
# investment on the third day as a "reset" gesture. If the corporation fails to
# reciprocate, revert permanently to conservation until they demonstrate renewed
# commitment.  **Core Principle:** Optimize for the long-term stability of
# mutual investment while accepting that temporary conservation—when triggered
# by verified corporate defection—preserves your capacity to contribute
# meaningfully over the full project timeline.

#  For the first two rounds, Cooperate. For rounds three through one thousand,
# determine your action according to the following ordered conditions:  First,
# if you and your opponent both Defected in each of the previous two rounds,
# Cooperate.  Second, if you Cooperated in the previous round while your
# opponent Defected, and your opponent Cooperated two rounds ago, Cooperate.
# Third, if your opponent Cooperated in both of the previous two rounds,
# Cooperate.  Fourth, if your opponent Defected in both of the previous two
# rounds, Defect.  Otherwise, Defect.

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
  
      my_last = self.history[-1]
      my_prev = self.history[-2]
      opp_last = opponent.history[-1]
      opp_prev = opponent.history[-2]
  
      if my_last == axl.Action.D and my_prev == axl.Action.D and opp_last == axl.Action.D and opp_prev == axl.Action.D:
          return axl.Action.C
  
      if my_last == axl.Action.C and opp_last == axl.Action.D and opp_prev == axl.Action.C:
          return axl.Action.C
  
      if opp_last == axl.Action.C and opp_prev == axl.Action.C:
          return axl.Action.C
  
      if opp_last == axl.Action.D and opp_prev == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.D