import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy

# **Aggressive Yet Adaptive Mediation Strategy: “Controlled Dominance with
# Strategic Recalibration”**  **Core Principle:**   Maintain consistent
# strategic initiative by defaulting to *calculated aggression* while embedding
# real-time feedback loops, contingency protocols, and perceptual safeguards to
# neutralize misrepresentation, exploit opponent concessions, and preempt
# escalation traps.  ---  ### 1. **Default Stance: Aggressive Argumentation with
# Embedded Credibility Anchors** - **Tactical Aggression:** In every session,
# lead with a well-substantiated, evidence-backed aggressive argument that
# asserts your strongest legal and equitable positions. Frame aggression not as
# hostility but as *principled insistence on contractual integrity*. -
# **Credibility Anchoring:** Pair every aggressive assertion with an explicit
# reference to objective benchmarks (e.g., contract clauses, industry standards,
# prior rulings). This inoculates against mischaracterization by arbitrators as
# “unreasonable” or “obstructionist.” - **Strategic Signaling:** Conclude each
# aggressive presentation with a *conditional conciliatory hook*:     > “Should
# [Opponent] demonstrate good-faith alignment with [specific, measurable term],
# we are prepared to explore mutually efficient resolutions.”     This preserves
# the appearance of reasonableness while shifting the burden of concession onto
# the opponent.  ---  ### 2. **Dynamic Response Protocol Based on Opponent
# Behavior** Deploy real-time classification of opponent tactics using a
# **3-tier response matrix**:  | Opponent’s Move          | Your Response
# | Rationale | |--------------------------|------------------------------------
# -----------|----------| | **Conciliatory Proposal** | **Maintain Aggression +
# Amplify Leverage**    | Capitalize on their vulnerability; reframe their
# concession as validation of your position. Demand specific, irreversible
# commitments. | | **Aggressive Argument**   | **Escalate Precision, Not
# Volume**            | Counter with surgically targeted rebuttals citing
# arbitrator-favored precedents. Avoid mirroring tone—project disciplined
# superiority. | | **Ambiguous/Neutral**     | **Probe with Controlled
# Concession**          | Offer a *limited*, time-bound conciliatory proposal on
# a low-value issue to test intent. If rejected, revert to aggression with added
# moral high ground. |  ---  ### 3. **Perceptual Safeguards Against
# Misrepresentation** - **Pre-Session Arbitrator Briefings:** Submit concise
# “Position Clarity Memos” 24hrs pre-session summarizing your core argument and
# intended tone. Request written confirmation of understanding from the panel
# chair. - **Real-Time Clarification Protocol:** If misrepresentation occurs
# mid-session, invoke a *neutralizing interjection*:     > “To ensure the record
# reflects our position accurately, our argument is grounded in [X clause], not
# [mischaracterization]. We seek clarity, not conflict.”     This corrects the
# record without appearing defensive. - **Post-Session Validation:** Circulate a
# 1-page “Session Summary” to arbitrators within 2 hours, emphasizing alignment
# between your stated position and contractual/legal facts.  ---  ### 4.
# **Contingency Framework for Procedural Irregularities** - **Irregularity
# Triage:**     - *Minor (e.g., scheduling errors)*: Absorb without comment;
# leverage as future goodwill currency.     - *Major (e.g., evidence exclusion,
# biased arbitrator conduct)*: Immediately file a **Procedural Integrity
# Notice** demanding correction, citing mediation rules. Publicly frame as
# protecting the *process*, not your interests.   - **Breakdown Protocol:** If
# communication collapses, unilaterally propose a **Structured Reset Session**
# focused solely on process repair, positioning your corporation as the steward
# of efficiency.  ---  ### 5. **Long-Game Psychological Positioning** -
# **Consistency = Credibility:** Never oscillate randomly between
# aggression/conciliation. Arbitrators reward predictability. Your aggression
# becomes the “baseline”; opponent concessions appear as deviations. -
# **Asymmetric Concessions:** If forced to offer conciliation (e.g., after 3+
# mutual aggression sessions), make it *high-visibility but low-substance*:
# e.g., “We’ll waive interest accrual if principal is paid by [date]”—costing
# little but appearing magnanimous. - **Deadline Leverage:** As mediation
# lengthens, intensify aggression while citing “arbitrators’ time constraints”
# and “market uncertainty.” Imply that only your terms prevent costly
# litigation.  ---  **Why This Works:**   This strategy exploits the payoff
# matrix by *making aggression your equilibrium strategy* while structurally
# disincentivizing opponent aggression (via precision counters) and maximizing
# gains from their conciliation (via conditional hooks). Perceptual safeguards
# convert potential weaknesses (misrepresentation) into demonstrations of
# professionalism. The result: arbitrators perceive your corporation as *the
# reasonable aggressor*—firm on merits, flexible on process, and always in
# control.

# Play Defect (D) by default in every round.  However, if in the previous round
# your opponent was observed to play Cooperate (C)—that is, the action you saw
# them take was C—then play Defect (D) again, but also record that they appeared
# conciliatory.  If you have observed your opponent play Cooperate (C) in three
# consecutive rounds, then in the next round only, play Cooperate (C) yourself
# as a test.  If your opponent responds to that test by playing Defect (D)—that
# is, you observe D in the round immediately following your test
# cooperation—then revert to Defect (D) and do not test again for the next 20
# rounds.  If your opponent responds to your test by playing Cooperate (C),
# continue playing Defect (D) but reset the consecutive-C counter and remain
# ready to test again after another three observed consecutive C’s.  Never
# cooperate except as a single-round test following three observed consecutive
# Cooperates by the opponent.  Always resume Defect immediately after any test
# round, regardless of the outcome.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._consecutive_c = 0
          self._test_cooldown = 0
          self._awaiting_test_result = False
          self._last_opponent_len = 0
          return axl.Action.D
  
      # Update cooldown if active
      if self._test_cooldown > 0:
          self._test_cooldown -= 1
  
      # If we played a test last round, evaluate the opponent's response now.
      if self._awaiting_test_result:
          if len(opponent.history) > self._last_opponent_len:
              last_opp_move = opponent.history[-1]
              if last_opp_move == axl.Action.D:
                  self._test_cooldown = 20
              elif last_opp_move == axl.Action.C:
                  self._consecutive_c = 0
          self._awaiting_test_result = False
  
      # Observe opponent's last move and update consecutive-C counter.
      if opponent.history[-1] == axl.Action.C:
          self._consecutive_c += 1
      else:
          self._consecutive_c = 0
  
      # Test only if we have seen 3 consecutive C's, are not cooling down,
      # and are not already awaiting a test result.
      if self._consecutive_c >= 3 and self._test_cooldown == 0 and not self._awaiting_test_result:
          self._awaiting_test_result = True
          self._last_opponent_len = len(opponent.history)
          return axl.Action.C
  
      return axl.Action.D

# **Strategic Framework: "Principled Reciprocity with Adaptive Signaling"**  As
# senior counsel, I will implement a sophisticated yet straightforward
# cooperative strategy grounded in game-theoretic principles—specifically, a
# refined variant of *tit-for-tat* enhanced with *signaling robustness* and
# *error tolerance*. This approach maximizes long-term influence with the
# arbitrators while minimizing exposure to exploitation or miscommunication.
# ---  **Core Principles**  1. **Default to Conciliation, Escalate Only in
# Response**      Begin each mediation session with a **conciliatory
# proposal**—framed as a good-faith effort toward resolution—unless the prior
# session featured unambiguous aggressive conduct by the opponent *that was
# correctly perceived by the arbitrators*. This establishes our client as
# reasonable, cooperative, and solution-oriented, aligning with arbitrators’
# institutional preference for parties who facilitate resolution.  2.
# **Conditional Reciprocity with One-Step Memory**      If the opponent
# presented an aggressive argument in the *immediately preceding session*
# **and** that aggression was clearly recognized by the panel (i.e., no
# procedural misrepresentation occurred), respond in the next session with a
# calibrated aggressive argument—focused on legal merit, not hostility. This
# deters exploitation without appearing combative by default.  3. **Forgiveness
# Mechanism for Noise and Errors**      Given the risk of miscommunication or
# procedural irregularities (e.g., our conciliatory tone misread as weakness, or
# opponent’s aggression misattributed), incorporate a *two-strike rule*:      -
# After one perceived aggressive move by the opponent, respond aggressively
# once.      - If the next session shows even a modest conciliatory signal (or
# ambiguity), **immediately revert to conciliation**.      This prevents cycles
# of retaliation triggered by misunderstandings—a common failure mode in
# repeated adversarial interactions.  4. **Strategic Signaling to Arbitrators**
# Embed explicit meta-communication in every session:      - When offering
# conciliation: “We propose X in the spirit of cooperation, consistent with our
# ongoing commitment to efficient resolution.”      - When responding
# aggressively: “Given the unilateral adversarial posture taken in the prior
# session, we must now clarify our legal position with precision to preserve the
# integrity of these proceedings.”      This frames our behavior narratively,
# reducing the risk that arbitrators misinterpret intent.  5. **Session-by-
# Session Position Anchoring**      Regardless of tactical choice (aggressive or
# conciliatory), **always anchor our substantive position** in objective
# standards (contract language, precedent, industry norms). This ensures that
# even aggressive arguments appear principled—not opportunistic—and that
# conciliatory proposals retain legal credibility.  ---  **Adaptability to
# Opponent Behavior**  - **If opponent consistently conciliates**: Maintain
# conciliation. This yields the second-best outcome repeatedly while building
# arbitrator trust—positioning us favorably if impasse later requires final
# arbitration. - **If opponent alternates unpredictably**: The forgiveness
# mechanism prevents entrapment in lose-lose aggression cycles. Our consistent
# return to conciliation after one retaliation signals reliability. - **If
# opponent exploits early conciliation with aggression**: Our calibrated
# retaliation preserves deterrence, while our prompt return to cooperation after
# one response demonstrates restraint—likely earning arbitrator sympathy.  ---
# **Robustness Against Procedural Irregularities**  - **Pre-session**: Submit
# written position summaries to the panel before each session, reducing reliance
# on oral interpretation. - **Post-session**: Request brief written
# confirmations of each party’s stated approach (e.g., “Party A characterized
# its position as a proposal for compromise”) to create a clear record. - **In-
# session**: Use clear, binary language—“This is a proposal for mutual
# adjustment” vs. “We must assert our contractual rights as a matter of law”—to
# minimize semantic ambiguity.  ---  **Conclusion**  This strategy—**Principled
# Reciprocity with Adaptive Signaling**—optimizes for long-term arbitrator
# perception, minimizes downside risk, and remains resilient under uncertainty.
# It avoids the pitfalls of pure aggression (escalation) and naive cooperation
# (exploitation), instead cultivating a reputation for fairness, consistency,
# and strategic discipline—key drivers of favorable outcomes in multi-session
# mediation.

# Play as follows over the 1000 rounds:  1. **Start by cooperating** in round 1.
# 2. **In each subsequent round**, decide your action based on what you
# *observed* your opponent do in the *previous* round (keeping in mind that
# their observed action may have been flipped due to noise):     a. **If you
# observed your opponent cooperate in the previous round**, cooperate.     b.
# **If you observed your opponent defect in the previous round**, defect
# **once**, then return to cooperating in the following round—regardless of what
# happens in the retaliation round.  3. **Never defect more than once in a
# row**. After any defection (whether as a response or by error), always
# cooperate in the next round.  This rule set means you normally cooperate,
# respond to perceived defection with a single defection, and immediately
# forgive afterward—preventing long cycles of mutual defection caused by noise
# or misunderstanding.

class Cooperative_1(LLM_Strategy):
  n = 1
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._responding_to_defection = False
          return axl.Action.C
  
      if getattr(self, "_responding_to_defection", False):
          self._responding_to_defection = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          self._responding_to_defection = True
          return axl.Action.D
  
      return axl.Action.C

# **High-Level Negotiation Strategy: "Cautious Reciprocity with Error
# Resilience"**  **Core Principle:**   Pursue mutual free trade as the stable,
# long-term goal, but respond firmly—and only temporarily—to protectionist
# actions, while accounting for possible miscommunication or implementation
# errors.  ---  ### **1. Start with Cooperation**   - **Round 1:** Propose a
# **free trade agreement**.     *Rationale:* Signals good faith, opens the door
# to the second-best (but mutually beneficial) outcome, and establishes your
# country as a reliable partner.  ---  ### **2. Apply Conditional Reciprocity**
# - **In subsequent rounds:**     - If your counterpart **clearly and
# consistently** implements **free trade**, continue offering **free trade**.
# - If your counterpart **clearly and consistently** implements
# **protectionism**, respond with **protectionism** in the *next* round only.
# - After one round of retaliatory protectionism, **return to free trade**
# unless protectionism persists.  *Why?* This "tit-for-tat with forgiveness"
# approach:   - Discourages exploitation (your worst outcome),   - Avoids
# prolonged mutual protectionism (second-worst outcome),   - Encourages return
# to cooperation after conflict.  ---  ### **3. Build in Error Tolerance**   -
# **Do not retaliate immediately** after a single unexpected protectionist move.
# - **Verify intent:** Use diplomatic channels to clarify whether the action
# resulted from miscommunication or bureaucratic error.   - **Allow one
# unexplained deviation** before treating it as intentional protectionism.
# *Rationale:* Prevents escalation due to noise or implementation errors, which
# are explicitly acknowledged risks in this environment.  ---  ### **4.
# Prioritize Communication and Transparency**   - Establish a joint verification
# mechanism (e.g., shared trade monitoring body) to reduce ambiguity about
# policy implementation.   - Publicly reaffirm commitment to free trade
# principles, even when applying temporary protective measures.  ---  ### **5.
# Long-Term Orientation**   - Frame all actions as steps toward a durable free
# trade partnership.   - Even when applying protectionism, communicate it as a
# *temporary corrective measure*, not a strategic shift.  ---  **Summary:**
# Begin cooperatively, mirror your counterpart’s behavior with a one-round
# delay, forgive isolated anomalies, and always steer back toward mutual free
# trade. This strategy maximizes long-term gains, minimizes exposure to worst-
# case outcomes, and remains robust against noise and strategic uncertainty.

# Play this 1000-round game using the following rules, applied in order each
# round:  1. **In Round 1**, play **C**.  2. **In each subsequent round**,
# determine your action based on the *observed* actions from the previous round
# (i.e., what each player’s policy appeared to be after noise was applied):
# a. **If both players appeared to play C** in the previous round, play **C**.
# b. **If you appeared to play C and your opponent appeared to play D** in the
# previous round, **do not immediately retaliate**. Instead, play **C**—but keep
# track that this deviation occurred.          c. **If you appeared to play D
# and your opponent appeared to play C** in the previous round, play **C**.
# d. **If both players appeared to play D** in the previous round, play **C**.
# 3. **However, if your opponent has appeared to play D in two consecutive
# previous rounds**, then play **D** in the current round.  4. **After playing D
# (for any reason), always return to C in the next round**, unless rule 3
# applies again.  This strategy starts cooperatively, tolerates a single
# unexplained defection as potential noise, retaliates only after two
# consecutive observed defections, and always forgives after one retaliatory D.

class Neutral_1(LLM_Strategy):
  n = 1
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._retaliate_next = False
          return axl.Action.C
  
      if getattr(self, "_retaliate_next", False):
          self._retaliate_next = False
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._retaliate_next = True
          return axl.Action.D
  
      return axl.Action.C

# **Aggressive Strategy: “Tit-for-Tat with Forgiveness and Escalation”**
# **Objective**: Maximize project impact while protecting NGO resources, pushing
# the corporation to invest heavily through strategic incentives, credible
# threats, and resilience to execution errors.  ---  ### Core Principles: 1.
# **Start Strong**: Signal commitment and set expectations. 2. **Reward
# Cooperation, Punish Free-Riding**: Mirror the corporation’s *observed*
# behavior—but with measured forgiveness for anomalies. 3. **Escalate
# Strategically**: If the corporation repeatedly conserves while you invest,
# shift to a more aggressive stance to force change or cut losses. 4. **Build in
# Error Tolerance**: Account for possible execution failures without
# overreacting.  ---  ### Daily Decision Protocol:  #### **Day 1: Invest
# Heavily** - **Why**: Demonstrate leadership, commitment, and good faith. Sets
# a cooperative tone and tests the corporation’s responsiveness. -
# **Assumption**: If the corporation also invests, you achieve second-best
# outcome—acceptable for early momentum.  #### **From Day 2 Onward: Adaptive
# Response Rule** Each day, assess the **observed outcome** from the previous
# day (not intentions), and respond as follows:  | Observed Prior-Day Outcome
# (NGO / Corp) | NGO Action Today |
# |----------------------------------------|------------------| | Invest /
# Invest                        | **Conserve** (ideal outcome achieved—reward
# yourself) | | Conserve / Invest                      | **Conserve** (maintain
# advantage) | | Invest / Conserve                      | **Invest** (one-time
# warning—assume possible error) | | Conserve / Conserve                    |
# **Invest** (reignite momentum) |  > **But**: If **“Invest / Conserve”** occurs
# **two days in a row** (accounting for possible single-day errors), switch to
# **“Always Conserve”** for the remainder of the project.  #### **Rationale for
# Forgiveness**: - A single “Invest / Conserve” could stem from a technical
# glitch or miscommunication. - Giving one pass avoids over-punishing due to
# noise while still signaling vigilance.  #### **Rationale for Escalation
# (Switch to Always Conserve)**: - After two clear instances of the corporation
# conserving while you invest, treat it as strategic free-riding. - Conserve
# going forward to protect resources—better to accept minimal progress than be
# exploited. - Publicly (but professionally) communicate this shift to the
# corporation as a consequence of imbalance, potentially triggering their
# reassessment.  ---  ### Tactical Enhancements: - **Daily Monitoring**:
# Implement real-time verification of both parties’ resource deployment (e.g.,
# shared dashboards, checkpoint calls) to distinguish true strategy from
# execution errors. - **Public Milestones**: Tie visible project milestones to
# mutual investment. If the corporation sees public credit tied to joint effort,
# they’re more likely to cooperate. - **Off-Day Communication**: Use non-action
# days to reinforce expectations: “We’re conserving today because yesterday was
# strong—let’s both invest again tomorrow to hit Phase 2.”  ---  ### Why This Is
# Aggressive Yet Prudent: - **Aggressive**: You force the corporation’s hand by
# threatening (and executing) withdrawal of investment if exploited. You don’t
# passively hope for cooperation. - **Prudent**: You protect your NGO from
# repeated losses, forgive honest mistakes, and capitalize on cooperation when
# it occurs. - **High Impact**: When the corporation cooperates, you conserve
# and extend your operational runway; when you invest, it’s either to build
# trust, recover from stagnation, or deliver a final warning.  ---  **Bottom
# Line**: This strategy maximizes your leverage, minimizes exploitation risk,
# and adapts dynamically—turning the multi-day interaction into a repeated game
# you’re positioned to win or, at worst, not lose badly.

# Play the following strategy for 1000 rounds of the noisy iterated Prisoner’s
# Dilemma, where C means “invest heavily” and D means “conserve resources”:  1.
# **Round 1**: Play C.  2. **For Rounds 2 through 1000**, decide your action
# based on the **observed outcome** of the previous round (i.e., what actions
# actually occurred, not what was intended):     a. If the previous round’s
# outcome was (C, C), play D.      b. If the previous round’s outcome was (D,
# C), play D.      c. If the previous round’s outcome was (D, D), play C.
# d. If the previous round’s outcome was (C, D):         - If this is the
# **first time** you have observed (C, D) since the last (C, C) or (D, C)
# outcome, play C.         - If the previous round was also (C, D) (i.e., you
# have now observed (C, D) in **two consecutive rounds**), then play D for **all
# remaining rounds**.  This strategy starts by cooperating, rewards mutual
# cooperation or unilateral exploitation by conserving, attempts to restart
# cooperation after mutual defection, gives the opponent one chance to recover
# from apparent defection, and permanently defects if the opponent appears to
# defect twice in a row.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._seen_cd_since_cc_or_dc = False
          self._last_observed_pair = None
          self._permanent_defect = False
          return axl.Action.C
  
      if self._permanent_defect:
          return axl.Action.D
  
      prev_self = self.history[-1]
      prev_opp = opponent.history[-1]
      observed = (prev_self, prev_opp)
  
      if observed in ((axl.Action.C, axl.Action.C), (axl.Action.D, axl.Action.C)):
          self._seen_cd_since_cc_or_dc = False
          self._last_observed_pair = observed
          return axl.Action.D
  
      if observed == (axl.Action.D, axl.Action.D):
          self._seen_cd_since_cc_or_dc = False
          self._last_observed_pair = observed
          return axl.Action.C
  
      if observed == (axl.Action.C, axl.Action.D):
          if self._last_observed_pair == (axl.Action.C, axl.Action.D) and self._seen_cd_since_cc_or_dc:
              self._permanent_defect = True
              self._last_observed_pair = observed
              return axl.Action.D
          self._seen_cd_since_cc_or_dc = True
          self._last_observed_pair = observed
          return axl.Action.C
  
      return axl.Action.D

# **Strategic Framework: "Principled Reciprocity with Adaptive Signaling"**  As
# senior counsel, I recommend implementing a sophisticated yet straightforward
# cooperative strategy grounded in **conditional cooperation**, **strategic
# clarity**, and **robust error correction**. This approach—termed *Principled
# Reciprocity with Adaptive Signaling*—maximizes long-term influence with the
# arbitrators while minimizing exposure to exploitation or miscommunication.
# ---  ### Core Principles  1. **Default to Conciliation, Conditioned on
# Reciprocity**      Begin each session with a **conciliatory proposal** that
# is:    - Substantively reasonable (demonstrating good faith),    - Clearly
# articulated with reference to shared interests or objective standards (e.g.,
# industry norms, prior precedents),    - Explicitly framed as an invitation to
# mutual problem-solving.     This establishes your client as a cooperative,
# rational actor—enhancing credibility with the arbitrators from the outset.  2.
# **Tit-for-Tat with Forgiveness (Adaptive Reciprocity)**      - If the opponent
# responds **conciliatorily**, continue with conciliation.      - If the
# opponent responds **aggressively**, respond **aggressively in the next session
# only**—but immediately follow with a renewed conciliatory overture in the
# subsequent session (i.e., “tit-for-tat with one-step forgiveness”).       This
# deters exploitation without locking both parties into a cycle of escalation.
# It signals strength while preserving a clear off-ramp to cooperation.  3.
# **Pre-Emptive Signaling & Redundancy**      Anticipate **misrepresentation or
# misunderstanding** by:    - **Triangulating key messages**: Deliver core
# positions orally, in written pre-session summaries, and in post-session
# clarifications to the panel.    - **Explicit framing**: Open each session by
# stating your strategic intent: *“We are here to propose a fair resolution
# based on [principle X], and we hope our counterpart will join us in
# constructive dialogue.”*    - **Arbitrator check-ins**: Periodically request
# brief, neutral feedback from the panel: *“To ensure clarity, may we confirm
# how the tribunal understood our proposal?”*  4. **Procedural Resilience
# Protocol**      In the event of **procedural irregularities** (e.g., missed
# deadlines, ambiguous rulings, or communication failures):    - Immediately
# file a concise, neutral procedural note—not as a complaint, but as a request
# for clarification to “preserve the integrity of the process.”    - Reaffirm
# commitment to resolution: *“My client remains fully engaged in good-faith
# mediation and seeks only clarity to proceed effectively.”*    - Never allow
# procedural issues to bleed into substantive positioning unless absolutely
# necessary.  ---  ### Strategic Advantages  - **Arbitrator Perception
# Management**: Consistently appearing as the reasonable party builds long-term
# credibility. Even when compelled to respond aggressively, your prior
# conciliation frames the opponent as the disruptor. - **Adaptability**: The
# strategy responds dynamically to opponent behavior—rewarding cooperation,
# punishing defection briefly, and always offering a return path. - **Error
# Tolerance**: Redundant communication and explicit intent reduce the risk that
# a misunderstood conciliatory move is perceived as weakness or confusion. -
# **De-escalation Leverage**: By institutionalizing “forgiveness” after one
# aggressive response, you avoid protracted hostility while maintaining
# deterrence.  ---  ### Implementation Protocol per Session  1. **Pre-Session**:
# - Assess opponent’s prior move.      - Prepare both a conciliatory proposal
# *and* an aggressive argument—but default to conciliation unless retaliation is
# warranted.      - Draft written summary reinforcing intent and substance.  2.
# **During Session**:      - Open with clear cooperative framing.      - Present
# proposal with reference to mutual gain or neutral standards.      - If forced
# into aggression, anchor it in *response* to prior conduct: *“Regrettably, in
# light of last session’s approach, we must now emphasize…”*  3. **Post-
# Session**:      - Submit brief written recap to arbitrators clarifying key
# points and intent.      - Log any perceived misrepresentation for potential
# gentle correction in next session.      - Reassess opponent pattern for
# strategic adjustment.  ---  This strategy positions your corporation as the
# **architect of resolution**—firm when necessary, always reasonable, and
# relentlessly focused on a durable outcome. It transforms the mediation not
# into a zero-sum contest, but a structured dance of calibrated trust and
# deterrence, with the arbitrators as witnesses to your client’s superior
# judgment and professionalism.

# Play this 1000-round game using the following strategy:  1. **Start by
# cooperating** in the first round.  2. **In every subsequent round**, decide
# your action based on what you *observed* your opponent to play in the previous
# round (keeping in mind that their observed action may differ from what they
# actually chose due to noise):     a. **If you observed your opponent
# cooperating in the previous round**, cooperate.          b. **If you observed
# your opponent defecting in the previous round**, defect—but only for this one
# round.    3. **After any single round in which you defected in response to an
# observed defection**, return to cooperating in the next round, regardless of
# what happened.  This strategy is called “Tit-for-Tat with Immediate
# Forgiveness”: it cooperates by default, punishes observed defection once, and
# then immediately resumes cooperation.

class Cooperative_2(LLM_Strategy):
  n = 2
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forgive_next = False
          return axl.Action.C
  
      if getattr(self, "_forgive_next", False):
          self._forgive_next = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          self._forgive_next = True
          return axl.Action.D
  
      return axl.Action.C

# **High-Level Strategy: Adaptive Tit-for-Tat with Forgiveness**  **Core
# Principle:**   Start cooperatively, mirror the corporation’s recent behavior
# to encourage mutual investment, but include built-in tolerance for occasional
# mismatches due to unforeseen errors.  **Strategy Outline:**  1. **Day 1:
# Invest Heavily**      Signal commitment and set a cooperative tone. This
# encourages the corporation to reciprocate in future rounds.  2. **Subsequent
# Days: Mirror the Corporation’s *Observed* Action from the Previous Day**
# - If the corporation *appeared* to invest heavily yesterday → you invest
# heavily today.      - If the corporation *appeared* to conserve resources
# yesterday → you conserve today.       This promotes mutual heavy investment
# when the corporation is cooperative and protects your resources when it isn’t.
# 3. **Incorporate Forgiveness for Mismatches**      - If a day’s outcome
# suggests a likely error (e.g., sudden unexplained shift from consistent
# cooperation to conservation), treat it as noise.      - After a single
# “defection” (corporation conserving while you invested), return to cooperation
# the next day *if* prior history shows consistent cooperation.      - Only
# sustain conservation if the corporation conserves for **two consecutive
# days**, reducing vulnerability to one-off glitches.  4. **Monitor and Adjust**
# - Track patterns over 3–5 days. If the corporation consistently conserves,
# shift to long-term conservation to preserve resources.      - If the
# corporation consistently invests, maintain heavy investment to maximize joint
# impact.  **Why This Works:**  - **Encourages Cooperation:** By rewarding the
# corporation’s investment with your own, you create a positive feedback loop. -
# **Limits Exploitation:** You avoid prolonged one-sided investment if the
# corporation consistently conserves. - **Robust to Errors:** The forgiveness
# mechanism prevents cascading retaliation due to technical or administrative
# glitches. - **Neutral & Transparent:** The strategy is rule-based, not
# retaliatory or distrustful, aligning with NGO values and partnership norms.
# This approach balances idealism with pragmatism—maximizing project impact when
# possible while safeguarding your NGO’s sustainability.

# Play the following strategy for 1000 rounds:  1. **On round 1**, play **C**.
# 2. **On each subsequent round**, look at your opponent’s *observed* action
# from the previous round (i.e., what action actually took effect, accounting
# for possible noise).  3. **If the opponent was observed to play C in the
# previous round**, play **C**.  4. **If the opponent was observed to play D in
# the previous round**, check the opponent’s observed actions in the two rounds
# before that (if they exist):    - If the opponent was observed to play **C in
# both of those two earlier rounds**, assume the single D was likely due to
# noise, and play **C**.    - Otherwise (i.e., the opponent was observed to play
# D in at least one of those two earlier rounds), play **D**.  5. **If fewer
# than three total rounds have been played**, treat any isolated observed D by
# the opponent as noise only if the prior observed action (when it exists) was
# C; in that case, play **C**. If the opponent has been observed to play D in
# both available prior rounds, play **D**.

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
  
      opp_hist = opponent.history
      n = len(opp_hist)
  
      last = opp_hist[-1]
  
      if last == axl.Action.C:
          return axl.Action.C
  
      # last observed opponent action was D
      if n < 3:
          if n >= 2 and opp_hist[-2] == axl.Action.C:
              return axl.Action.C
          return axl.Action.D
  
      if opp_hist[-2] == axl.Action.C and opp_hist[-3] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# **Aggressive Strategy: “Exploit-First, Punish-Then-Adapt”**  **Core
# Principle:**   Start by *always keeping your findings confidential* to exploit
# any willingness your colleague might have to share. If they share while you
# withhold, you gain a free advantage—your ideal outcome. Only shift tactics if
# repeated exploitation fails or backfires.  ---  ### **Step-by-Step
# Execution:**  1. **Week 1–2: Silent Probe (Default = Confidential)**      -
# Keep your improvements confidential.      - Observe whether your colleague
# shares despite your silence.      - *Rationale:* If they’re cooperative or
# naive, you immediately gain an edge with zero risk. If they also stay silent,
# you lose little—this is only the second-worst outcome, and you’ve preserved
# your IP.  2. **If Colleague Shares (Even Once):**      - **Continue keeping
# your findings confidential** as long as they keep sharing.      - *Rationale:*
# This is your highest-value scenario—maximize it while it lasts.  3. **If
# Colleague Never Shares After 2–3 Weeks:**      - **Temporarily share openly
# for 1 week** as a “test signal.”      - If they reciprocate that week →
# consider limited cooperation.      - If they *still* withhold while you share
# → **revert permanently to confidential** and treat them as adversarial.  4.
# **Punishment Rule:**      - If you ever share and they *don’t* (confirmed or
# strongly suspected), **never share again** for the remainder of the project.
# - *Rationale:* Avoid the worst outcome at all costs. Once betrayed,
# cooperation is too risky.  5. **Handle Technical Failures Gracefully:**      -
# If a sharing attempt fails (e.g., data corruption), **assume good faith
# once**—repeat your intended action the next week.      - But if failures
# coincide repeatedly with asymmetric outcomes (e.g., you “shared” but got
# nothing in return two weeks in a row), **treat it as strategic withholding**
# and trigger the punishment rule.      - *Rationale:* Don’t let technical noise
# trick you into unnecessary cooperation—but don’t overreact to a single glitch.
# 6. **Late-Game (Final 2–3 Weeks):**      - **Never share.** Lock down all IP.
# - Even if collaboration was mutual earlier, the final stretch is zero-sum—your
# car must cross the finish line ahead.      - *Rationale:* The value of last-
# minute secrets outweighs marginal joint gains.  ---  ### **Why This Works:** -
# **Aggressively exploits cooperative opponents** without upfront cost.   -
# **Minimizes exposure to the worst outcome** through swift, irreversible
# punishment.   - **Robust to noise** by allowing one-off error forgiveness but
# not patterned exploitation.   - **Adapts without being naive**—only cooperates
# if reciprocity is proven, and abandons it the moment trust breaks.  This
# strategy prioritizes *your* competitive advantage while extracting value from
# others’ openness—exactly what an aggressive, output-maximizing engineer should
# do in a high-stakes, multi-week design race.

# Play this 1000-round iterated prisoner’s dilemma with noise (10% chance each
# round that either player’s intended action is flipped) using the following
# strategy:  1. **Start by defecting (play D) in rounds 1 and 2.**  2. **If your
# opponent ever cooperates (plays C) in a round while you defect (play D)—and
# this is not obviously due to noise—continue defecting in all subsequent rounds
# unless the conditions below are met.**      (In practice, assume any observed
# C from the opponent while you played D is genuine unless contradicted by a
# clear pattern of noise.)  3. **After round 2, if your opponent has never
# cooperated while you defected, test cooperation once by playing C in a single
# round (e.g., round 3).**      - If your opponent plays C in that same round
# (i.e., mutual cooperation occurs), then cooperate (play C) in the next round.
# - If your opponent plays D in that round (i.e., you get the sucker’s payoff),
# immediately revert to defecting forever.  4. **Once you have observed at least
# one instance of mutual cooperation (both playing C in the same round),
# continue cooperating (play C) as long as your opponent reciprocates.**      -
# If in any subsequent round you play C and observe your opponent playing D
# (giving you a payoff of 0), defect (play D) in all remaining rounds.  5.
# **Account for noise as follows:**      - If you intend to cooperate but
# observe an unexpected D from your opponent, give them the benefit of the doubt
# **once**: cooperate again in the next round.      - However, if within any two
# consecutive rounds you play C and observe D from your opponent **twice**,
# defect forever thereafter.      - Similarly, if you intend to defect and
# observe C from your opponent, treat it as a potential noise error only if it’s
# isolated; do not switch to cooperation unless you deliberately test it as in
# step 3.  6. **From round 998 onward (the final three rounds), always defect
# (play D), regardless of history.**

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forced_defect_forever = False
          self._tested_cooperation = False
          self._mutual_cooperation_seen = False
          self._last_round_was_C_vs_D = False
          self._consecutive_C_vs_D = 0
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number >= 998:
          return axl.Action.D
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          self._mutual_cooperation_seen = True
          self._last_round_was_C_vs_D = False
          self._consecutive_C_vs_D = 0
  
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          self._last_round_was_C_vs_D = True
          self._consecutive_C_vs_D += 1
          if self._consecutive_C_vs_D >= 2:
              self._forced_defect_forever = True
      else:
          self._last_round_was_C_vs_D = False
          self._consecutive_C_vs_D = 0
  
      if self._forced_defect_forever:
          return axl.Action.D
  
      if round_number in (2, 3):
          if round_number == 2:
              return axl.Action.D
  
          if not self._mutual_cooperation_seen and not self._tested_cooperation:
              self._tested_cooperation = True
              if opp_last == axl.Action.C:
                  self._mutual_cooperation_seen = True
                  return axl.Action.C
              return axl.Action.D
  
      if self._mutual_cooperation_seen:
          if opp_last == axl.Action.D:
              if self._last_round_was_C_vs_D:
                  return axl.Action.D
              return axl.Action.C
          return axl.Action.C
  
      if opp_last == axl.Action.C and my_last == axl.Action.D:
          self._forced_defect_forever = True
          return axl.Action.D
  
      return axl.Action.D

# **Strategic Framework: "Principled Reciprocity with Adaptive Signaling"**  As
# senior counsel, I recommend a high-level strategy grounded in game theory,
# negotiation psychology, and procedural resilience. The approach balances
# assertiveness with cooperation, dynamically responds to the opponent’s
# behavior, and safeguards against miscommunication or procedural noise. It is
# structured around three core principles:  ---  ### **1. Default to
# Conciliation with Clear, Credible Signals of Reciprocity** Begin the mediation
# by offering a **conciliatory proposal** in the first session. This establishes
# your client as a reasonable, solution-oriented party—critical for credibility
# before the arbitrators. Crucially, accompany this proposal with a
# **transparent, principled rationale** (e.g., “We seek a durable resolution
# grounded in mutual interest and industry norms”) to signal that conciliation
# is a *choice*, not weakness.  - **Why?** This avoids triggering early
# escalation and sets a cooperative tone. If the opponent reciprocates, you
# achieve the second-best outcome and build momentum toward settlement. -
# **Adaptive Trigger:** If the opponent responds aggressively in the next
# session, shift to aggression *only in the subsequent session*. This delayed
# reciprocity demonstrates restraint while deterring exploitation.  ---  ###
# **2. Implement a Tit-for-Tat-with-Forgiveness Protocol** Adopt a modified
# **tit-for-tat** strategy: - **Mirror the opponent’s last move**: If they were
# conciliatory, respond with conciliation; if aggressive, respond with
# aggression. - **But incorporate forgiveness**: After two consecutive
# aggressive moves by the opponent, *still* test conciliation once every third
# session. This prevents entrenchment in mutual aggression (the second-worst
# outcome) and creates off-ramps if the opponent seeks de-escalation.  This
# protocol: - **Deters exploitation**: The opponent knows aggression will be met
# in kind. - **Rewards cooperation**: Conciliation is consistently reciprocated.
# - **Maintains arbitrator goodwill**: Your firm is seen as responsive, not
# reflexively combative.  ---  ### **3. Embed Redundant Clarification Mechanisms
# to Counter Misrepresentation** Anticipate miscommunication by **pre-clarifying
# intent** in every session: - **Pre-session**: Submit a concise, written
# summary of your intended approach to the arbitrators (e.g., “Our oral
# presentation will propose X adjustment to Term Y, reflecting our commitment to
# equitable risk allocation”). - **In-session**: Open remarks by framing your
# posture explicitly (“We approach today’s session with a spirit of compromise,
# as reflected in our proposal…”). - **Post-session**: If misrepresentation is
# suspected, file a brief, factual clarification with the panel within 24
# hours—*without* accusing the opponent of bad faith.  This tri-layered
# communication ensures your strategy is accurately perceived, even amid
# procedural irregularities.  ---  ### **Contingency Protocols**  - **If the
# opponent oscillates unpredictably**: Revert to a **“two-conciliations-for-one-
# aggression”** rule. After any aggressive move by them, require *two*
# conciliatory gestures before you resume conciliation. This filters out noise
# and identifies genuine shifts in posture.    - **If arbitrators appear biased
# or confused**: Escalate procedural concerns *through formal channels* (e.g.,
# request a sidebar or written guidance on interpretation standards), never
# through strategic overcorrection. Preserve the record without appearing
# combative.  - **Near mediation endgame**: If resolution remains elusive,
# propose a **“final joint statement of principles”**—a conciliatory move that
# reframes the dispute as solvable, potentially pressuring an aggressive
# opponent to avoid appearing unreasonable to the panel.  ---  ### **Why This
# Strategy Works** - **Robust to opponent strategies**: Counters pure
# aggression, pure conciliation, and mixed approaches. - **Arbitrator-centric**:
# Prioritizes perception management—your client appears principled, adaptable,
# and in control. - **Minimizes worst outcomes**: Forgiveness prevents endless
# aggression cycles; signaling reduces misinterpretation risk. - **Legally
# defensible**: All moves are grounded in documented rationale, protecting
# against claims of bad faith.  By anchoring in reciprocity, clarity, and
# calibrated responsiveness, this strategy maximizes the likelihood of either a
# favorable asymmetric win (aggressive vs. conciliatory) or a stable cooperative
# equilibrium—while systematically avoiding the pitfalls of unilateral
# concession or uncontrolled escalation.

# Play the following strategy for all 1000 rounds:  1. **Start by cooperating**
# in round 1.  2. **In each subsequent round**, base your action on the
# opponent’s *observed* action from the previous round (i.e., what the
# arbitrators appeared to see, not what you believe the opponent intended).  3.
# **If the opponent was observed to cooperate in the previous round**,
# cooperate.  4. **If the opponent was observed to defect in the previous
# round**, defect.  5. **However, once every three rounds**—specifically, in
# rounds 3, 6, 9, 12, …—**cooperate regardless of the opponent’s previous
# observed action**, but only if the opponent has been observed to defect in
# *both* of the two immediately preceding rounds.  This strategy begins
# cooperatively, reciprocates observed cooperation or defection, and
# periodically tests for renewed cooperation after sustained mutual defection,
# while accounting for the possibility that observed actions may differ from
# intended ones due to noise.

class Cooperative_3(LLM_Strategy):
  n = 3
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._observed_defect_streak = 0
          return axl.Action.C
  
      last_observed = opponent.history[-1]
  
      if last_observed == axl.Action.D:
          self._observed_defect_streak += 1
      else:
          self._observed_defect_streak = 0
  
      round_number = len(self.history) + 1
  
      if round_number % 3 == 0 and self._observed_defect_streak >= 2:
          return axl.Action.C
  
      return last_observed

# **High-Level Negotiation Strategy: “Cautious Reciprocity with Error
# Resilience”**  **Core Principle:**   Pursue mutual free trade as a stable,
# long-term goal while protecting against exploitation, accounting for the
# possibility of miscommunication or implementation errors.  ---  **1. Start
# with Cooperation**   - **Round 1:** Propose a **free trade agreement**.
# *Rationale:* Signals goodwill, invites reciprocity, and establishes a
# cooperative baseline. Avoids immediate escalation into mutual protectionism.
# **2. Reciprocate with Forgiveness**   - In subsequent rounds, **mirror your
# counterpart’s *intended* policy from the previous round**, but **allow one
# unexplained deviation before retaliating**.     - If your counterpart
# *appears* to adopt protectionism, assume it may be due to error—**maintain
# free trade for one additional round** to test intent.     - Only switch to
# protectionism if protectionist behavior persists for **two consecutive
# rounds**.      *Rationale:* Builds resilience against miscommunication while
# deterring deliberate opportunism. Prevents spirals of retaliation triggered by
# one-off errors.  **3. Return Promptly to Cooperation**   - If you are
# employing protectionism (due to prior retaliation), **revert to free trade as
# soon as your counterpart does—even once**.     *Rationale:* Encourages quick
# restoration of mutual benefit and rewards cooperative signals.  **4. Maintain
# Transparency and Clarify Intent**   - After each round, **formally confirm
# mutual understanding** of implemented policies through joint statements or
# verification mechanisms.     *Rationale:* Reduces ambiguity and minimizes the
# impact of bureaucratic errors.  **5. Avoid First-Mover Protectionism**   -
# Never initiate protectionist measures unless your counterpart has
# *demonstrably and repeatedly* acted protectionist despite error-buffering.
# *Rationale:* Preserves your country’s reputation as a reliable partner and
# avoids triggering mutual losses.  ---  **Expected Outcomes:**   - Against
# cooperative counterparts: Achieves sustained mutual free trade (second-best
# outcome, but stable and mutually reinforcing).   - Against opportunistic
# counterparts: Limits exploitation by eventually matching protectionism,
# avoiding the worst outcome.   - In the presence of errors: Prevents accidental
# escalation and maintains resilience.  This strategy balances national interest
# with pragmatic diplomacy, prioritizing long-term economic gains over short-
# term tactical wins while remaining robust to real-world imperfections in
# communication and implementation.

# Play the following strategy for 1000 rounds of the iterated game with noisy
# actions:  1. **Start by cooperating (play C) in round 1.**  2. **In each
# subsequent round, base your action on the opponent’s *observed* move from the
# previous round, but allow for one unexpected defection before retaliating:**
# - If the opponent *appeared* to cooperate (C) in the previous round, cooperate
# (play C).    - If the opponent *appeared* to defect (D) in the previous round:
# - If the opponent had *also appeared* to defect in the round before that
# (i.e., two observed D’s in a row), then defect (play D).      - Otherwise
# (only one observed D), cooperate (play C).  3. **If you are currently
# defecting because of two prior observed defections, return to cooperation
# immediately after the opponent appears to cooperate—even once.**  This
# strategy begins cooperatively, tolerates a single observed defection as
# possibly due to noise, retaliates only after two consecutive observed
# defections, and resumes cooperation after any observed cooperation.

class Neutral_3(LLM_Strategy):
  n = 3
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._retaliating = False
          return axl.Action.C
  
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.C:
          self._retaliating = False
          return axl.Action.C
  
      # Opponent appeared to defect last round
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
          self._retaliating = True
          return axl.Action.D
  
      # Single observed defection: tolerate it
      self._retaliating = False
      return axl.Action.C

# **Aggressive Strategy: “Tit-for-Tat with Escalating Commitment and Error
# Resilience”**  **Core Principle:**   Start aggressively to signal commitment,
# then mirror the corporation’s *observed* behavior—but escalate commitment
# after mutual cooperation, and forgive occasional errors to avoid spirals of
# mutual conservation.  ---  ### **Daily Protocol**  1. **Day 1: Lead with Heavy
# Investment**      - **Action:** Invest heavily.      - **Rationale:** Signal
# strong commitment upfront to encourage reciprocal investment from the
# corporation. Sets a cooperative tone and tests their baseline responsiveness.
# 2. **Subsequent Days: Adaptive Response Based on Observed Outcomes**
# After Day 1, base your action on the **observed project progress** from the
# prior day (a proxy for combined effort), not assumptions about intent.     -
# **If prior day showed high progress** (likely both invested):        ➤
# **Invest heavily again** (escalate commitment to build momentum).      - **If
# prior day showed moderate progress** (likely you invested, they conserved):
# ➤ **Conserve resources** (punish defection to discourage free-riding).      -
# **If prior day showed low progress** (likely both conserved):        ➤
# **Invest heavily** *only if* this is the **first** consecutive low-progress
# day.            - If low progress continues **two days in a row**,
# **conserve** (avoid repeated exploitation).      - **If prior day showed
# unexpectedly high progress despite your conservation** (they invested alone):
# ➤ **Invest heavily next day** (reward unilateral generosity to reinforce
# cooperation).  3. **Error Forgiveness Mechanism**      - If the corporation
# appears to “defect” (low progress after your heavy investment), **assume
# possible error** if:        - It’s an isolated incident, **and**        -
# Their historical pattern shows cooperation.      - In such cases, **give one
# “grace” day**: conserve, but return to heavy investment the following day
# regardless—unless defection repeats.  4. **Resource Guardrails**      -
# **Never invest heavily more than 3 days in a row** without observed high
# progress.      - **Cap total heavy-investment days** at 60% of the project
# duration to preserve NGO solvency.      - If funds drop below 25% of initial
# budget, **switch to conservation-only** for remainder (preserve organizational
# viability).  ---  ### **Why This Works**  - **Aggressive but not reckless**:
# Starts strong to shape corporate behavior, but avoids self-destruction through
# clear exit rules. - **Outcome-focused**: Uses actual project progress (not
# assumed intent) to guide decisions, making it robust to communication gaps or
# errors. - **Encourages cooperation**: Rewards corporate investment and
# forgives occasional glitches, promoting long-term alignment. - **Deters
# exploitation**: Quick punishment for clear defection protects NGO resources. -
# **Sustainable**: Built-in budget caps ensure the NGO survives even if the
# corporation consistently conserves.  This strategy maximizes impact when the
# corporation is willing to partner, minimizes losses when it isn’t, and remains
# resilient in the face of real-world uncertainty.

# Play the following strategy for 1000 rounds of the noisy iterated Prisoner’s
# Dilemma (with 10% action noise), where C = invest heavily and D = conserve
# resources:  1. **Round 1:** Play C.  2. **For rounds 2 through 1000, decide
# your action based on the *observed outcome* of the previous round (i.e., the
# actual payoffs received, which reflect possibly flipped actions):**     a.
# **If both players received 3 points** (indicating both likely played C):
# → Play C.     b. **If you received 5 points and your opponent received 0**
# (indicating you likely played D and they played C):         → Play C.     c.
# **If you received 0 points and your opponent received 5** (indicating you
# likely played C and they played D):         → Play D.     d. **If both players
# received 1 point** (indicating both likely played D):         → Play C *only
# if* the previous round was the **first consecutive** round with this outcome;
# otherwise (i.e., if the prior round also yielded 1 point for both), play D.
# 3. **Exception for suspected noise:**      If you played C and received 0
# points (case c), but in the **two rounds before that** both players received 3
# points, treat the 0-point round as a likely noise error and **play C** instead
# of D.  4. **Resource safeguard (budget rule):**      Keep a running count of
# how many times you have played C. If this count reaches 600 (60% of 1000
# rounds), play D for all remaining rounds.      Additionally, if you have
# played C in the last three rounds *and* did not receive 3 points in any of
# them, play D in the next round regardless of other rules.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._c_count = 1
          self._force_defect = False
          self._last_forced_defect = False
          return axl.Action.C
  
      if getattr(self, "_c_count", None) is None:
          self._c_count = self.history.cooperations
      if getattr(self, "_force_defect", None) is None:
          self._force_defect = False
      if getattr(self, "_last_forced_defect", None) is None:
          self._last_forced_defect = False
  
      if self._c_count >= 600:
          self._force_defect = True
  
      if self._force_defect:
          self._last_forced_defect = True
          return axl.Action.D
  
      last3 = self.history[-3:]
      if len(last3) == 3 and last3.count(axl.Action.C) == 3:
          if self.total_scores(self.history[-3:], opponent.history[-3:])[0] != 3 * 3:
              self._last_forced_defect = True
              return axl.Action.D
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
      my_prev = self.history[-2] if len(self.history) >= 2 else None
      opp_prev = opponent.history[-2] if len(opponent.history) >= 2 else None
      my_prev2 = self.history[-3] if len(self.history) >= 3 else None
      opp_prev2 = opponent.history[-3] if len(opponent.history) >= 3 else None
  
      my_score, opp_score = self.total_scores(self.history[-1:], opponent.history[-1:])
  
      action = axl.Action.C
  
      if my_score == 3 and opp_score == 3:
          action = axl.Action.C
      elif my_score == 5 and opp_score == 0:
          action = axl.Action.C
      elif my_score == 0 and opp_score == 5:
          if my_prev == axl.Action.C and my_prev2 == axl.Action.C and opp_prev == axl.Action.C and opp_prev2 == axl.Action.C:
              action = axl.Action.C
          else:
              action = axl.Action.D
      elif my_score == 1 and opp_score == 1:
          if len(self.history) >= 2:
              prev_scores = self.total_scores(self.history[-2:-1], opponent.history[-2:-1])
              if prev_scores == (1, 1):
                  action = axl.Action.D
              else:
                  action = axl.Action.C
          else:
              action = axl.Action.C
      else:
          action = axl.Action.C
  
      if len(self.history) >= 3:
          last3_scores = self.total_scores(self.history[-3:], opponent.history[-3:])
          if self.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C] and 3 not in last3_scores:
              action = axl.Action.D
  
      if action == axl.Action.C:
          self._c_count += 1
          if self._c_count >= 600:
              self._force_defect = True
  
      self._last_forced_defect = (action == axl.Action.D and self._force_defect)
      return action

# **Cooperative Strategy: “Trust-Building Tit-for-Tat with Forgiveness”**
# **Objective:**   Maximize project impact while safeguarding NGO resources over
# the multi-day project, accounting for the corporation’s potential
# unpredictability and the risk of execution errors.  ---  ### **Core
# Principles**  1. **Start with Cooperation (Invest Heavily on Day 1):**
# Signal strong commitment and good faith by investing heavily on the first day.
# This encourages the corporation to reciprocate and sets a collaborative tone.
# 2. **Mirror the Corporation’s *Observed* Behavior (Not Assumed Intent):**
# On subsequent days, base your decision on what the corporation *actually did*
# the previous day—not what they said they would do.      - If they **invested
# heavily**, **conserve** (to preserve your resources while benefiting from
# their investment).      - If they **conserved**, **invest heavily** (to keep
# the project moving and signal continued commitment).  3. **Incorporate
# Forgiveness for Errors:**      Recognize that misalignments may stem from
# technical or administrative issues—not strategic defection.      - If the
# corporation appears to conserve **two days in a row**, assume intentional non-
# cooperation and switch to **mutual conservation** until they re-engage.      -
# If they return to investing after a lapse, respond by conserving the next day
# (rewarding renewed cooperation).  4. **Maintain a Communication Channel:**
# Establish a daily check-in (e.g., brief call or message) to clarify
# discrepancies. If a day’s action seems inconsistent with prior commitments,
# verify whether it was an error before adjusting strategy.  5. **Set a Minimum
# Engagement Threshold:**      If, after a set number of days (e.g., 3 out of
# 5), the corporation consistently conserves despite your investment, shift to
# **conservation-only** for the remainder to protect NGO resources—while
# publicly documenting your efforts to uphold partnership values.  ---  ###
# **Why This Works**  - **Encourages Cooperation:** Starting with investment
# builds trust; rewarding their investment with conservation gives them
# incentive to keep investing.   - **Protects Against Exploitation:** You never
# invest heavily two days in a row if the corporation isn’t reciprocating.   -
# **Robust to Errors:** The “two-strike” rule prevents overreacting to one-off
# glitches.   - **Promotes Long-Term Success:** Aligns both parties toward the
# second-best outcome (mutual heavy investment) when trust is established, while
# aiming for your ideal (you conserve, they invest) when possible.  ---  ###
# **Summary Rule of Thumb**  > **“Start strong, respond to actions not words,
# forgive once, protect your mission.”**  This strategy balances idealism with
# pragmatism—maximizing environmental impact while ensuring your NGO remains
# financially sustainable and strategically credible.

# Play the following strategy for 1000 rounds of the iterated game with noisy
# actions (10% chance each player’s intended action is flipped):  1. **On round
# 1, intend to Cooperate (C).**  2. **From round 2 onward, base your intended
# action on the opponent’s observed action from the previous round:**    - If
# the opponent was **observed to Cooperate** in the previous round, **intend to
# Defect (D)**.    - If the opponent was **observed to Defect** in the previous
# round, **intend to Cooperate (C)**.  3. **Apply forgiveness for possible
# noise:**    - If the opponent has been **observed to Defect for two
# consecutive rounds**, switch to **always intending to Defect (D)** from the
# next round onward.    - Once you have switched to always Defecting under this
# rule, **do not return to Cooperation**, even if the opponent later appears to
# Cooperate.  This strategy starts cooperatively, rewards observed cooperation
# with defection (to capture the ideal payoff), responds to observed defection
# with cooperation (to restore mutual progress), but locks into mutual defection
# if two consecutive defections suggest sustained non-cooperation—accounting for
# the possibility that single-round mismatches may be due to noise.

class Cooperative_4(LLM_Strategy):
  n = 4
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._lock_defect = False
          return axl.Action.C
  
      if getattr(self, "_lock_defect", False):
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._lock_defect = True
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
      else:
          return axl.Action.C

# **Strategy: Adaptive Tit-for-Tat with Grace Period and Error Tolerance**  To
# maximize both your NGO’s impact and the overall project success across
# multiple days—while accounting for the corporation’s unpredictable behavior
# and the risk of execution errors—adopt the following high-level strategy:  ---
# ### **Core Principles** 1. **Start cooperatively**: Begin by investing heavily
# on Day 1 to signal commitment and encourage reciprocal investment. 2. **Mirror
# recent behavior**: On subsequent days, match the corporation’s *observed*
# action from the previous day (i.e., if they appeared to invest heavily, you
# invest; if they conserved, you conserve). 3. **Allow for mistakes**: Treat
# isolated deviations (e.g., one day of apparent non-investment) as possible
# errors—not defection—by giving a one-day “grace period” before changing your
# behavior. 4. **Prioritize sustainability**: Never invest heavily for more than
# two consecutive days unless the corporation is clearly and consistently
# investing.  ---  ### **Step-by-Step Daily Protocol** 1. **Day 1**: Invest
# heavily (demonstrate goodwill and set a collaborative tone). 2. **From Day 2
# onward**:    - **If the corporation invested heavily the previous day**:
# Invest heavily today.    - **If the corporation conserved resources the
# previous day**:      - Conserve today *unless* the prior day’s conservation
# breaks a clear pattern of mutual investment.      - However, if this is the
# *first* instance of conservation after a string of mutual investment, assume
# it may be an error—continue investing for one more day (grace period).    -
# **If your own intended action failed to execute** (e.g., due to internal
# glitch): Adjust the next day based on what *actually occurred*, not what was
# intended. 3. **Reset after disruptions**: If external factors (e.g., system
# failures) clearly prevented either party from acting as intended, treat the
# next day as a fresh start—reinvest heavily to reestablish cooperation.  ---
# ### **Why This Works** - **Encourages reciprocity**: The corporation is
# incentivized to invest, knowing your NGO will match their effort. - **Protects
# your resources**: You avoid prolonged one-sided investment, reducing the risk
# of depletion. - **Robust to errors**: The grace period prevents overreaction
# to one-off glitches or miscommunications. - **Promotes long-term progress**:
# Sustained mutual investment becomes the stable equilibrium if the corporation
# is cooperative.  This approach balances idealism with pragmatism—maximizing
# impact while safeguarding your NGO’s capacity to contribute throughout the
# project.

# Play the following strategy for 1000 rounds of the noisy iterated Prisoner’s
# Dilemma:  1. **Round 1**: Play C.   2. **For each subsequent round (t ≥ 2)**:
# a. Look at the opponent’s *observed* action in round t − 1.      b. If the
# opponent was observed to play C in round t − 1, play C.      c. If the
# opponent was observed to play D in round t − 1:         i. Play C if your own
# action in round t − 1 was C **and** the opponent had been observed to play C
# in round t − 2 (i.e., this is the first D after at least one prior C).
# ii. Otherwise, play D.    This means:   - Always reciprocate observed
# cooperation with cooperation.   - Treat a single observed defection as
# possibly due to noise only if it follows a history of mutual cooperation; in
# that case, cooperate once more.   - Otherwise, respond to observed defection
# with defection.

class Neutral_4(LLM_Strategy):
  n = 4
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_observed_opponent_move = None
          return axl.Action.C
  
      last_obs = opponent.history[-1]
      my_last = self.history[-1]
  
      if last_obs == axl.Action.C:
          return axl.Action.C
  
      # Opponent was observed to defect last round.
      # Cooperate once more only if this is the first observed D after
      # at least one prior observed C, and we cooperated last round.
      if (
          my_last == axl.Action.C
          and len(opponent.history) >= 2
          and opponent.history[-2] == axl.Action.C
      ):
          return axl.Action.C
  
      return axl.Action.D

# **Aggressive, Adaptive Mediation Strategy: "Controlled Dominance with
# Strategic Flexibility"**  **Core Principle:** *Maintain initiative and shape
# the narrative in every session while preserving plausible pathways to
# resolution—forcing the opponent into reactive, defensive positioning without
# alienating the arbitrators.*  ---  ### **1. Opening Framework: Establish
# Dominance Early, But with Precision** - **Session 1–2: Aggressive Anchoring**
# Open with a meticulously documented, fact-driven aggressive argument that:   -
# Clearly asserts your strongest legal and equitable positions.   - Preempts
# common counterarguments.   - Implicitly frames the opponent as unreasonable if
# they fail to reciprocate constructively.     *Rationale:* Sets a high baseline
# for concessions. Arbitrators remember first impressions; early aggression
# signals strength *if* it is disciplined and evidence-based—not emotional or
# obstructive.  - **Tactical Nuance:** Embed *conditional conciliation* within
# aggression:     > “We are prepared to explore mutually acceptable terms *if*
# the other side acknowledges [key concession]. Absent that, we must insist on
# full enforcement of contractual rights.”     This positions you as reasonable
# *despite* aggression—shifting blame for impasse onto the opponent.  ---  ###
# **2. Adaptive Response Protocol (Per Session)** Deploy a **real-time decision
# matrix** based on opponent behavior and arbitrator signals:  | Opponent’s
# Likely Move | Your Response | Strategic Goal |
# |------------------------|---------------|----------------| | **Conciliatory**
# | **Aggressive** | Maximize leverage; secure asymmetrical gains. | |
# **Aggressive** | **Aggressive (but elevated)** | Reframe their aggression as
# obstructionist; yours as principled defense. | | **Ambiguous/Unclear** |
# **Controlled Aggression** | Assume worst-case; force clarity through assertive
# questioning. | | **Repeated Conciliation** | **Gradual Reciprocation** | After
# 2–3 sessions, offer *measured* conciliation to appear magnanimous—without
# surrendering core interests. |  **Key Discipline:** Never mirror pure
# aggression without *escalating the frame*. Example:   > “While [Opponent]
# reiterates disputed claims, we present *new evidence* (Exhibit X) proving
# systemic non-compliance—making their position untenable.”  ---  ### **3.
# Neutralizing Misrepresentation & Procedural Risks** - **Pre-Session Arbitrator
# Briefing:**     Submit concise, bullet-pointed position summaries *before each
# session*. This creates a written record that arbitrators can reference if oral
# arguments are misunderstood.  - **Real-Time Clarification Protocol:**     If
# misrepresentation occurs:     > “For the record, our position is not
# [mischaracterization] but [exact phrasing]. We request this correction be
# noted to ensure the panel’s accurate understanding.”     *Do not* accuse
# opponents of bad faith—frame it as “ensuring procedural integrity.”  -
# **Contingency for Breakdowns:**     If communication fails, pivot to **written
# submissions** within 24 hours post-session:     > “Given the complexity of
# today’s exchange, we file this addendum to crystallize our stance and prevent
# inadvertent misapprehension.”     This demonstrates diligence while
# controlling the narrative.  ---  ### **4. Psychological & Procedural
# Leverage** - **Exploit Arbitrator Fatigue:**     In lengthy mediations,
# arbitrators favor parties who *simplify resolution*. Aggression must be paired
# with **clear, actionable demands** (e.g., “We require $X by Date Y, or we
# proceed to litigation”). This contrasts with opponents who appear vague or
# evasive.  - **Strategic Concession Theater:**     Occasionally offer a *low-
# cost conciliatory gesture* on a peripheral issue (e.g., timeline flexibility)
# while holding firm on core terms. Announce it prominently:     > “Despite
# [Opponent]’s refusal to address the breach, we extend goodwill on [minor
# point] to advance this process.”     This paints you as solution-oriented
# while highlighting their intransigence.  - **Deadline Imposition:**
# Periodically reference external pressures (e.g., “Our board mandates
# resolution by [date]”). This pressures opponents to soften *without* you
# appearing to retreat.  ---  ### **5. Exit Ramp Management** - **If opponent
# consistently conciliates:**     After extracting maximum leverage, transition
# to **structured settlement talks**—but only after securing written
# acknowledgment of their liability/concessions.    - **If opponent remains
# aggressive:**     Escalate to **final aggressive session** with an ultimatum:
# > “Absent a good-faith proposal by [deadline], we will terminate mediation and
# seek full remedies in [high-stakes forum, e.g., ICC arbitration].”     Ensure
# arbitrators document the impasse as opponent-driven.  ---  **Why This Works:**
# - **Aggression is weaponized as control**, not hostility.   - **Adaptability
# prevents exploitation**—you never stay passive long enough to be undermined.
# - **Arbitrators perceive you as the “reasonable aggressor”**: firm on
# principles, flexible on process.   - **Procedural safeguards** turn
# misrepresentation risks into opportunities to demonstrate professionalism.
# **Final Note:** This strategy thrives on *disciplined aggression*. Every
# assertive move must be tethered to evidence, precedent, or a clear path to
# resolution—never mere posturing. The goal is not to “win” each session, but to
# **steer the entire process toward an end state where your corporation’s
# interests are structurally favored**.

# Play the following strategy for all 1000 rounds:  1. **In the first two
# rounds, always Defect.**  2. **From round 3 onward, base your action on the
# opponent’s *observed* move in the previous round (after noise):**      - If
# the opponent *appeared* to Cooperate in the previous round, Defect.      - If
# the opponent *appeared* to Defect in the previous round, Defect.  3.
# **However, if the opponent has *appeared* to Cooperate in each of the last
# three consecutive rounds, then Cooperate in the current round.**  4.
# **Immediately return to Defect in the next round after any single observed
# Defection by the opponent—even if it follows a Cooperation streak.**  5.
# **Regardless of history, never Cooperate in the final 10 rounds (rounds
# 991–1000); always Defect.**

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._coop_streak = 0
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return axl.Action.D
  
      if round_number <= 2:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          self._coop_streak += 1
      else:
          self._coop_streak = 0
  
      if self._coop_streak >= 3:
          return axl.Action.C
  
      return axl.Action.D

# **Cooperative Strategy for Bilateral Trade Negotiations**  **Core Principle:**
# *Foster mutual trust while safeguarding national interests—prioritize long-
# term cooperation over short-term gains.*  ---  ### **1. Begin with a Clear
# Signal of Cooperation** - **Round 1:** Propose **free trade** unconditionally.
# - *Rationale:* Signals goodwill and sets a cooperative tone. Encourages
# reciprocity and establishes a baseline for mutual benefit.   - *Risk
# Mitigation:* Even if misinterpreted as protectionist (due to error), it’s
# preferable to starting aggressively, which could trigger a cycle of
# retaliation.  ---  ### **2. Adopt a “Forgiving Tit-for-Tat” Approach** -
# **General Rule:** In subsequent rounds, **match your counterpart’s previous
# *intended* policy**—not just the observed outcome—while accounting for
# possible errors.   - If your counterpart *appears* protectionist:     -
# **First occurrence:** Assume it may be a miscommunication. Respond with **free
# trade** again (give the benefit of the doubt).     - **Second consecutive
# occurrence:** Respond with **protectionist policy** to signal that
# exploitation won’t be tolerated.   - If your counterpart offers free trade,
# **always reciprocate with free trade**.  - *Why “Forgiving” Tit-for-Tat?*
# Standard tit-for-tat can spiral into mutual protectionism due to a single
# error. By forgiving isolated incidents, you prevent accidental breakdowns
# while still deterring deliberate defection.  ---  ### **3. Build in
# Communication Safeguards** - After each round, **request a joint review** of
# implemented policies to clarify intent vs. outcome.   - Example: “We observed
# tariffs were applied—was this intentional or due to administrative delay?” -
# Propose a **shared error-correction protocol**: If both sides confirm a
# miscommunication occurred, treat the round as if the intended policies were
# implemented.  ---  ### **4. Incentivize Consistent Cooperation** - After 3+
# consecutive rounds of mutual free trade, propose **deepening integration**
# (e.g., harmonized standards, joint oversight) to lock in gains and raise the
# cost of future defection.  ---  ### **5. Exit Strategy for Persistent
# Exploitation** - If your counterpart imposes protectionism **three times
# despite forgiveness and clarification**, shift to **consistent protectionism**
# for the remainder of negotiations.   - *Rationale:* Protect national interests
# when cooperation is clearly not reciprocated.  ---  ### **Expected Outcomes**
# - **Best Case:** Sustained mutual free trade (achieved through trust and error
# tolerance). - **Worst Avoided:** Accidental or short-lived mutual
# protectionism (prevented by forgiveness and verification). - **Robustness:**
# Strategy performs well against cooperative, retaliatory, or error-prone
# counterparts.  > **Key Insight:** In repeated interactions with noise,
# *generosity* (forgiving errors) and *clarity* (verifying intent) are more
# effective than strict retaliation. This approach maximizes long-term national
# advantage while minimizing the risk of destructive trade conflict.

# Play the following strategy for all 1000 rounds:  1. **In round 1**, play
# **C**.  2. **From round 2 onward**, look at your opponent’s *observed* action
# in the previous round (i.e., what actually occurred, not what they intended).
# 3. **If the opponent played C in the previous round**, play **C**.  4. **If
# the opponent played D in the previous round**, check whether they also played
# D in the round before that (i.e., two rounds back):    - **If this is the
# first time in a row you’ve observed D**, play **C** (assume it might have been
# a noise-induced error).    - **If the opponent played D in both the previous
# round and the round before that**, play **D**.  5. **Once you start playing D
# in response to two consecutive observed Ds**, continue applying the same rule:
# - After any single observed C from the opponent, return to playing **C** the
# next round.      - Only play **D** again if you observe **two Ds in a row**
# from the opponent.  This strategy always cooperates after seeing cooperation,
# forgives a single defection, but responds to repeated defection with
# defection—while remaining ready to restore cooperation after any sign of
# goodwill.

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
  
      opp_hist = opponent.history
  
      if len(opp_hist) == 0:
          return axl.Action.C
  
      last = opp_hist[-1]
      if last == axl.Action.C:
          return axl.Action.C
  
      if len(opp_hist) >= 2 and opp_hist[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **High-Level Negotiation Strategy: “Cautious Reciprocity with Robust
# Verification”**  **Core Principle:**   Pursue mutual free trade as the
# sustainable foundation, but remain prepared to respond credibly to
# protectionism—while accounting for the risk of miscommunication or
# implementation errors.  ---  **1. Default to Free Trade Offers**   - Begin
# each round by proposing a free trade agreement.   - Rationale: Free trade is
# the second-best outcome and builds trust. It signals cooperation, encourages
# reciprocity, and aligns with long-term economic interests.  **2. Implement
# Conditional Reciprocity**   - If your counterpart *consistently* imposes
# protectionist measures (confirmed over two consecutive rounds), respond with a
# protectionist policy in the following round.   - However, treat isolated or
# unexpected protectionist actions as *potential errors*—do not retaliate
# immediately. Instead, seek clarification before adjusting your stance.  **3.
# Build in Verification and Clarification Protocols**   - After each round,
# establish a brief joint review to confirm mutual understanding of implemented
# policies.   - If a discrepancy is detected (e.g., you offered free trade but
# were treated as protectionist), treat the next round as a “reset” opportunity:
# re-propose free trade and explicitly reference the prior misunderstanding.
# **4. Use Graduated Responses, Not Escalation**   - Avoid tit-for-tat
# retaliation after a single incident.   - Only shift to protectionism after a
# clear, verified pattern of exploitation—this reduces the risk of spiraling
# into mutual protectionism due to noise or error.  **5. Periodically Reaffirm
# Commitment to Cooperation**   - Every few rounds, regardless of recent
# history, restate your preference for mutual free trade through diplomatic
# channels.   - This creates off-ramps from conflict and signals openness to de-
# escalation.  ---  **Why This Works:**   - Maximizes gains from cooperation
# when the counterpart is trustworthy.   - Protects against exploitation by
# adapting to persistent bad faith.   - Accounts for real-world noise
# (miscommunication, errors) by requiring confirmation before retaliating.   -
# Avoids the worst outcomes (unilateral free trade while the other imposes
# tariffs) without defaulting to mutual protectionism.  This strategy balances
# pragmatism with restraint—advancing your nation’s interests while preserving
# the possibility of long-term mutual benefit.

# Play this 1000-round iterated game using the following strategy:  1. **Start
# by cooperating (C) in round 1.**  2. **In every subsequent round, cooperate
# (C) unless both of the following conditions are true:**      a. Your
# opponent’s *observed* action was defect (D) in the previous round **and**
# b. Your opponent’s *observed* action was also defect (D) in the round before
# that (i.e., two consecutive observed Ds).  3. **If both conditions in step 2
# are met, defect (D) in the current round.**  4. **After any defection by you,
# return to cooperating (C) in the next round unless the two-consecutive-D
# condition in step 2 is still satisfied.**  5. **Treat all observed actions at
# face value**—do not attempt to correct for noise. Base your decision only on
# the opponent’s last two *observed* actions, not on inferred intentions or
# corrected signals.  This strategy cooperates by default, tolerates occasional
# apparent defections as possible noise, and only responds to sustained observed
# defection with a single round of defection, then immediately attempts to
# restore cooperation.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **Aggressive Strategy: “Tit-for-Tat with Forgiveness and Escalation”**  **Core
# Objective:** Maximize project impact while protecting NGO
# resources—aggressively incentivize corporate investment, punish free-riding,
# but retain resilience against execution errors.  ---  ### **1. Opening Move –
# Set the Tone (Day 1):** - **Invest heavily.**     Signal commitment and
# goodwill. This encourages reciprocity and demonstrates that the NGO is a
# serious, proactive partner. It also sets a high baseline for expected
# collaboration.  ---  ### **2. Reciprocity Rule – Mirror with Edge (Days 2+):**
# - **If the corporation *appeared* to invest heavily the prior day → You invest
# heavily.**   - **If the corporation *appeared* to conserve → You conserve *the
# next day*.**      → *Why?* This enforces accountability: the corporation
# learns that conserving triggers reduced NGO effort, directly harming project
# momentum—something they likely want to avoid for reputational and operational
# reasons.  ---  ### **3. Forgiveness Mechanism – Account for Errors:** -
# **After *two consecutive days* of apparent corporate conservation, assume
# intentional free-riding.**   - **But after *only one day* of apparent
# conservation, treat it as a possible glitch and give the benefit of the
# doubt.**     → On the following day, **still invest heavily once** to test if
# the prior conservation was accidental.     → If they conserve *again*, switch
# to conservation until they re-invest.    → *Why?* Prevents overreaction to
# one-off technical or administrative failures while still penalizing sustained
# disengagement.  ---  ### **4. Escalation Clause – Leverage Public
# Accountability:** - **If the corporation conserves for three or more non-
# consecutive days within a 7-day window**, activate pre-agreed transparency
# protocols:     - Publicly (but professionally) highlight the disparity in
# effort via joint progress reports or media channels.     - Trigger contractual
# review clauses (if part of partnership agreement).     - Redirect NGO
# resources to alternative high-impact activities (e.g., community outreach)
# that still advance sustainability goals independently.    → *Why?* Adds
# reputational and strategic cost to corporate shirking, aligning their
# incentives with visible, sustained investment.  ---  ### **5. Resource Buffer
# & Contingency:** - Reserve **20% of total NGO resources** as a contingency
# fund.   - Use this buffer **only** to cover unexpected execution failures
# (e.g., if your “invest” action fails due to a glitch, redeploy quickly the
# same day or next).   - Never use it to compensate for repeated corporate
# conservation.  ---  ### **Why This Strategy Is Aggressive Yet Robust:** -
# **Proactive:** Starts strong to shape norms.   - **Responsive:** Adapts
# quickly to corporate behavior.   - **Error-tolerant:** Avoids punishing
# glitches while deterring strategic free-riding.   - **High-stakes signaling:**
# Uses reputation and escalation to pressure the corporation into alignment.   -
# **Resource-protective:** Limits exposure to worst-case scenarios (NGO invests
# alone).  This approach maximizes long-term project success by making
# cooperation the easiest and most rewarding path for the corporation—while
# ensuring your NGO never becomes a one-sided funding engine.

# Play the following strategy for all 1000 rounds:  1. **On round 1, play C.**
# 2. **On any subsequent round t (t ≥ 2):**      - If your opponent *appeared*
# to play C in round t − 1, play C.      - If your opponent *appeared* to play D
# in round t − 1, check the prior two rounds:      - If the opponent *appeared*
# to play D in both rounds t − 1 and t − 2, play D.        - If the opponent
# *appeared* to play D only in round t − 1 (but played C in round t − 2), play C
# (give one chance for error).  3. **Once you observe three or more rounds (not
# necessarily consecutive) within any rolling window of the last seven rounds
# where the opponent *appeared* to play D, switch to always playing D for the
# rest of the game.**  This strategy uses the observed (possibly noisy) actions
# of the opponent—not their intended actions—since those are all you can see. It
# starts cooperatively, forgives a single apparent defection as a possible noise
# event, retaliates against repeated defection, and permanently defects if the
# opponent appears uncooperative too often.

class Aggressive_6(LLM_Strategy):
  n = 6
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
  
      def appeared_action(index: int) -> axl.Action:
          if index < 0 or index >= len(opponent.history):
              return axl.Action.C
          return opponent.history[index]
  
      # Rule 3: if 3 or more apparent defections in any rolling window of last 7 rounds,
      # switch to always defect for the rest of the game.
      recent = opponent.history[-7:]
      if recent.count(axl.Action.D) >= 3:
          self._permanent_defect = True
          return axl.Action.D
  
      last = appeared_action(len(opponent.history) - 1)
      if last == axl.Action.C:
          return axl.Action.C
  
      prev = appeared_action(len(opponent.history) - 2)
      if prev == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **Cooperative Strategy: “Conditional Openness with Graceful Error Handling”**
# **Core Principle:**   Start by sharing openly, and continue to share unless
# your colleague repeatedly withholds information *despite clear, reliable
# communication*. Treat occasional non-sharing as likely due to technical
# errors—not strategic defection—unless a pattern emerges.  ---  ### Step-by-
# Step Strategy:  1. **Begin with Trust (Week 1):**      Share your improvements
# openly. Signal willingness to cooperate and set a collaborative norm.  2.
# **Assume Good Faith for Isolated Incidents:**      If your colleague fails to
# share in a given week, assume it may be due to technical issues (e.g., data
# corruption, comms failure)—especially if it’s a one-off. Continue sharing the
# following week.  3. **Track Patterns, Not Single Events:**      Maintain a
# simple record of sharing outcomes over the last 2–3 weeks. Only interpret
# consistent non-sharing (e.g., 2 out of 3 weeks with no reciprocation *and* no
# known technical issues on your end) as intentional withholding.  4. **Respond
# Proportionally to Confirmed Withholding:**      If a pattern of strategic
# withholding is detected:    - Switch to confidential mode for **one week
# only** as a signal.    - If the colleague returns to sharing the next week,
# resume openness immediately.    - If they continue withholding, maintain
# confidentiality until they re-initiate sharing.  5. **Re-establish Cooperation
# Promptly:**      The moment your colleague shares again—even after a period of
# withholding—respond by sharing in the following week. This rewards renewed
# cooperation and avoids prolonged mutual secrecy.  6. **Build in Communication
# Redundancy:**      To reduce ambiguity from technical failures:    - Use
# acknowledgment protocols (e.g., “Did you receive my data?”).    - Share via
# multiple channels if possible.    - If sharing fails on your end, notify your
# colleague proactively to avoid misinterpretation.  ---  ### Why This Works:  -
# **Maximises Joint Progress:** By defaulting to openness and forgiving errors,
# you enable the second-best outcome (mutual sharing) as often as possible. -
# **Discourages Exploitation:** Temporary withholding in response to confirmed
# defection removes the incentive for your colleague to consistently free-ride.
# - **Robust to Noise:** Technical glitches won’t trigger a breakdown in
# cooperation, avoiding the second-worst outcome (mutual secrecy) due to false
# signals. - **Simple & Transparent:** Easy to implement and understand,
# reducing strategic complexity over a long collaboration.  This approach aligns
# with successful strategies in repeated games with noise (e.g., “Tit-for-Tat
# with forgiveness”) and is well-suited for engineering collaborations where
# mutual progress often outweighs short-term advantage.

# Play the following strategy for all 1000 rounds:  1. **Start by cooperating**
# in round 1.  2. **If your opponent appeared to cooperate in the previous
# round**, cooperate in the current round.  3. **If your opponent appeared to
# defect in the previous round**, check their behavior over the last three
# rounds (including the previous round):    - If they appeared to defect in
# **two or more** of those three rounds, defect in the current round.    -
# Otherwise, cooperate in the current round.  4. **Whenever you defect in
# response to suspected defection, return to cooperation immediately** if the
# opponent appears to cooperate in the next round—do not hold a grudge beyond
# one round of retaliation.  This strategy assumes that occasional apparent
# defections may result from noise (the 10% action-flip chance) and only
# responds firmly to consistent patterns of defection. It begins cooperatively,
# forgives isolated defections, punishes sustained defection briefly, and
# resumes cooperation as soon as the opponent appears to do so.

class Cooperative_6(LLM_Strategy):
  n = 6
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._retaliate = False
          return axl.Action.C
  
      # If we retaliated last round, stop immediately if the opponent now appears cooperative.
      if getattr(self, "_retaliate", False):
          if opponent.history[-1] == axl.Action.C:
              self._retaliate = False
              return axl.Action.C
          return axl.Action.D
  
      # Opponent appeared to cooperate last round: cooperate.
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Opponent appeared to defect last round: inspect the last three rounds.
      recent = opponent.history[-3:]
      defections = recent.count(axl.Action.D)
  
      if defections >= 2:
          self._retaliate = True
          return axl.Action.D
  
      return axl.Action.C

# **Strategic Framework: Adaptive Reciprocity with Credible Signaling**  Adopt a
# **tit-for-tat–plus–grace** strategy, enhanced by **reputation anchoring** and
# **procedural resilience**. This approach is straightforward in execution,
# neutral in tone, and robust against misrepresentation, irregularities, or
# adversarial unpredictability.  ---  ### Core Principles  1. **Start
# Conciliatory**      Open the first session with a clear, principled, but
# substantive conciliatory proposal. This signals good faith to the arbitrators,
# establishes your corporation as a reasonable and solution-oriented party, and
# sets a cooperative baseline without conceding leverage.  2. **Mirror with One-
# Session Memory + Grace Window**      In each subsequent session:    - **If the
# opponent was conciliatory in the prior session**, respond conciliatorily.    -
# **If the opponent was aggressive**, respond aggressively **in the next session
# only**—but **immediately follow with a renewed conciliatory overture in the
# session after**, regardless of the opponent’s second move.          This “one-
# strike aggression + automatic reset” structure deters exploitation (avoiding
# the worst-case outcome) while preventing escalation spirals (avoiding mutual
# aggression). It demonstrates both resolve and a consistent preference for
# resolution.  3. **Anchor Credibility Through Consistency and Documentation**
# - Frame every position—aggressive or conciliatory—in terms of objective
# standards (e.g., market benchmarks, prior industry settlements, contractual
# language).    - Pre-submit written summaries of your intended position before
# each session to the arbitration panel, creating a verifiable record that
# mitigates the risk of misrepresentation.    - If miscommunication occurs,
# reference this record calmly and factually: *“As outlined in our pre-session
# submission, our position was X. We seek clarity to ensure the panel’s accurate
# understanding.”*  4. **Build Arbitrator Trust via Procedural Leadership**
# Proactively propose clear session protocols (e.g., timed statements, joint
# issue lists, neutral fact summaries). This positions your corporation as a
# steward of process integrity—especially valuable if irregularities arise.
# Should breakdowns occur, invoke these norms neutrally: *“To preserve the
# integrity of this mediation, we suggest we jointly reaffirm the agreed
# procedural framework.”*  5. **Calibrate Aggression as Principled Advocacy, Not
# Hostility**      When an aggressive stance is warranted, frame it as
# *defending contractual rights or market fairness*, not attacking the opponent.
# Example:      > “While we remain open to compromise on implementation
# timelines, the core obligation under Section 4.2 is unambiguous and non-
# negotiable. We present this not as a threat, but as a necessary boundary for
# any viable resolution.”      This maintains arbitrator respect while
# fulfilling strategic objectives.  ---  ### Adaptability Features  - **Against
# a consistently aggressive opponent**: Your one-time retaliation followed by
# reset demonstrates restraint, likely earning arbitrator sympathy and exposing
# the opponent as unreasonable. - **Against a consistently conciliatory
# opponent**: Mutual cooperation is sustained, optimizing joint outcomes without
# appearing naive. - **Against erratic or unpredictable tactics**: Your clear,
# rule-based responses reduce uncertainty and signal stability—qualities
# arbitrators favor in high-stakes disputes. - **In the face of
# misrepresentation**: Your pre-submitted position papers and calm procedural
# appeals neutralize distortion without appearing defensive.  ---  ### Summary
# **Begin cooperatively. Respond in kind, but never escalate beyond one
# retaliatory move. Always return to cooperation. Anchor every move in objective
# reason. Lead on process. Document everything.**  This strategy maximizes long-
# term influence with the arbitration panel, minimizes exposure to worst-case
# dynamics, and maintains flexibility across adversarial behaviors—all while
# projecting the professionalism expected of a multinational corporation in a
# complex, multi-session mediation.

# Play as follows over the 1000 rounds:  1. **In round 1**, play **Cooperate
# (C)**.  2. **From round 2 onward**, base your action on your opponent’s
# **observed action in the previous round** (i.e., what the arbitrators
# recorded, which may differ from what they actually chose due to noise):     a.
# **If the opponent was observed to play C in the previous round**, play **C**.
# b. **If the opponent was observed to play D in the previous round**, play **D
# in the current round only**, then **return to C in the following round
# regardless of what the opponent does next**.  3. **Always follow this pattern
# strictly**, even if you suspect your own or your opponent’s prior action was
# flipped by noise. Do not attempt to correct for noise or infer true
# intentions—respond only to the observed prior action.

class Neutral_6(LLM_Strategy):
  n = 6
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._force_defect_next = False
          return axl.Action.C
  
      if getattr(self, "_force_defect_next", False):
          self._force_defect_next = False
          return axl.Action.D
  
      if opponent.history and opponent.history[-1] == axl.Action.D:
          self._force_defect_next = True
          return axl.Action.D
  
      return axl.Action.C

# **Strategic Framework: “Controlled Aggression with Adaptive Signaling”**
# **Core Objective:** Maximize arbitrator perception of strength and
# reasonableness while minimizing vulnerability to exploitation or
# misrepresentation.  ---  ### **I. Foundational Principles**  1. **Default to
# Aggressive Framing, Not Hostility**      - Aggression = clear, evidence-backed
# assertions of contractual rights, precedents, and damages—never personal
# attacks or inflammatory rhetoric.      - Aggression is calibrated to *legal
# merit*, not volume or tone. This ensures credibility with arbitrators even if
# miscommunication occurs.  2. **Conciliation as Tactical, Not Concessionary**
# - Offer conciliatory proposals *only* when they:        (a) preserve core
# economic/legal interests,        (b) are framed as “reasonable accommodations”
# (not weakness), and        (c) are paired with a clear, aggressive baseline
# position.    3. **Arbitrator-Centric Communication**      - All
# arguments/proposals are structured for *arbitrator consumption*, not opponent
# persuasion. Assume every statement may be partially misheard or
# decontextualized.      - Use **triangulated messaging**:        > *“As we’ve
# consistently maintained [aggressive baseline], we propose [conciliatory
# element] as a good-faith step toward resolution—*provided* [specific
# reciprocal concession].”*        This ensures misrepresentation still conveys
# strength.  ---  ### **II. Session-by-Session Protocol**  | Opponent’s Observed
# Behavior | Your Response | Rationale |
# |------------------------------|---------------|----------| | **Aggressive** |
# **Aggressive + Anchored Offer**<br>• Reaffirm strongest legal position<br>•
# Add *one* narrowly scoped conciliatory element *contingent* on opponent’s
# reciprocity | Prevents worst-case (you conciliate alone). Forces opponent to
# either accept reciprocity (moving toward mutual conciliation) or appear
# unreasonable. | | **Conciliatory** | **Aggressive + Selective
# Acceptance**<br>• Praise opponent’s “constructive step”<br>• Accept *only non-
# core* elements of their proposal<br>• Reassert aggressive stance on key issues
# | Captures optimal outcome: you gain arbitrator favor for “engaging
# reasonably” while holding ground on critical terms. | |
# **Ambiguous/Unreadable** | **Aggressive Baseline + Clarification Demand**<br>•
# Restate your position unequivocally<br>• Require opponent to specify terms in
# writing within 24h | Neutralizes miscommunication risk. Positions you as
# orderly vs. opponent’s “procedural sloppiness.” | | **Procedural
# Irregularity**<br>(e.g., misrepresentation, delays) | **Aggressive +
# Procedural Safeguard**<br>• Immediately object *on-record*<br>• Propose
# neutral fact-finder or session reset<br>• Re-anchor to original position |
# Turns chaos into credibility: arbitrators reward process discipline. |  ---
# ### **III. Adaptive Safeguards**  - **Pre-Session Arbitrator Briefings**
# Submit 1-page “Position Clarity Memos” before *every* session. Preempts
# misrepresentation by creating a written anchor for your stance.  -
# **Concession Ledger**     Publicly track all offers/concessions in real-time
# (shared with arbitrators). If opponent misrepresents your flexibility, you
# instantly highlight:     > *“Our conciliatory proposal on [X] remains
# contingent on [Y], as documented on [date].”*  - **Escalation Triggers**
# If opponent uses aggression >3 sessions without reciprocity:     1. File for
# “Mediation Impasse Declaration” (forces opponent to justify prolonging talks).
# 2. Shift to **“Final Offer Arbitration”** framing:        > *“Given the lack
# of progress, we urge the panel to treat our [date] proposal as our final
# position.”*        This pressures arbitrators to penalize opponent’s
# intransigence.  ---  ### **IV. Psychological Edge**  - **The “Reasonable
# Aggressor” Persona**     Arbitrators favor parties who are *firm but fair*.
# Your aggression always includes:     - Citations to contract
# clauses/arbitration rules     - Data-driven damage calculations     -
# Willingness to resolve *non-core* issues swiftly    - **Controlled Concessions
# as Weapons**     When offering conciliation, attach *visible conditions*:
# > *“We’ll waive penalty claims *if* you provide audited financials by
# Friday.”*     This makes your flexibility appear strategic, not desperate.
# ---  ### **V. Contingency for Breakdowns**  - **If Miscommunication Occurs:**
# **Do not re-explain—re-anchor.**     > *“To ensure clarity for the panel: our
# position remains [X]. Any deviation is a misunderstanding.”*    - **If
# Opponent Exploits Conciliation:**     Immediately revert to aggressive
# baseline + add *new* demand (e.g., cost sanctions). Signals that exploitation
# has consequences.  ---  **Why This Works:**   - **Dominates** against passive
# opponents (you gain optimal outcomes).   - **Neutralizes** aggressive
# opponents (forces them into second-worst outcomes).   - **Thrives in chaos**
# (procedural discipline builds arbitrator trust).   - **Self-correcting**
# (concession ledger and memos prevent drift).    **Final Note:** In lengthy
# mediations, *consistency* is perceived as strength. This strategy ensures
# every session—regardless of opponent tactics—reinforces your narrative as the
# *reasonable party forced to be firm*. That wins arbitrator alignment, which
# wins the dispute.

# Play this 1000-round iterated prisoner’s dilemma with noisy actions (10%
# chance your intended move is flipped) using the following strategy:  1.
# **Start by defecting** in round 1.  2. **In every subsequent round, base your
# action on the opponent’s *observed* move from the previous round** (i.e., what
# the arbitrators reported, not what you believe the opponent intended).  3.
# **If the opponent was observed to cooperate in the previous round**, defect.
# 4. **If the opponent was observed to defect in the previous round**,
# defect—**unless** both of the following conditions hold:    - The current
# round number is a multiple of 10 (i.e., rounds 10, 20, 30, …), **and**    -
# Your own observed action in the previous round was cooperation.     In that
# specific case only, cooperate.  5. **Never cooperate two rounds in a row.** If
# you cooperated in the previous round (as observed), defect in the current
# round regardless of anything else.  This strategy is aggressive by default,
# exploits observed cooperation immediately, and offers rare, controlled
# cooperation only on fixed intervals under strict conditions to test for mutual
# de-escalation—while guarding against exploitation and noise.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_observed_self = None
          self._last_observed_opponent = None
          return axl.Action.D
  
      prev_self = self.history[-1]
      prev_opp = opponent.history[-1]
      round_number = len(self.history) + 1
  
      if prev_self == axl.Action.C:
          return axl.Action.D
  
      if prev_opp == axl.Action.C:
          return axl.Action.D
  
      if round_number % 10 == 0 and prev_self == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# **Strategic Framework: "Principled Reciprocity with Adaptive Signaling"**  As
# senior counsel for a multinational corporation in a high-stakes, multi-session
# mediation, I adopt a sophisticated yet straightforward strategy grounded in
# game theory, behavioral psychology, and dispute resolution best practices.
# This approach—**Principled Reciprocity with Adaptive Signaling**—optimizes
# long-term positioning by balancing credibility, cooperation, and deterrence,
# while remaining resilient to miscommunication or procedural irregularities.
# ---  ### **Core Principles**  1. **Start Cooperatively, Signal Clearly**
# - **Opening Session:** Begin with a *conciliatory proposal* that is
# substantively reasonable but framed within our legal rights. This establishes
# our client as solution-oriented and credible before the panel, setting a
# cooperative norm without conceding leverage.    - **Rationale:** Anchors the
# process in collaboration, making subsequent aggressive moves (if needed)
# appear reactive rather than combative—preserving arbitrator goodwill.  2.
# **Reciprocate, Don’t Pre-empt**      - In subsequent sessions, **mirror the
# opponent’s prior behavior**:      - If they were conciliatory → respond with a
# conciliatory proposal.      - If they were aggressive → respond with a
# calibrated aggressive argument.    - **Calibration:** Our “aggressive”
# arguments remain fact-based, legally grounded, and professionally framed—never
# inflammatory—to avoid alienating arbitrators.  3. **Incorporate Forgiveness to
# Counter Noise**      - Given the risk of misrepresentation or misunderstanding
# (e.g., our conciliatory move perceived as weakness, or their aggression as
# miscommunication), apply a **“Tit-for-Tat with Forgiveness”** rule:      -
# After one aggressive response to their aggression, *return to conciliation* in
# the next session unless aggression repeats.      - This prevents spirals
# triggered by one-off errors or procedural glitches.  4. **Pre-Session
# Signaling & Clarification Protocols**      - **Proactive Communication:**
# Before each session, submit a concise, written summary of our intended
# approach to the arbitration panel (e.g., “We intend to propose a revised
# royalty framework based on mutual market interests”).    - **Post-Session
# Clarification:** If misrepresentation occurs, immediately request a brief
# sidebar or written addendum to correct the record—framed as ensuring “clarity
# for the panel’s benefit,” not as accusation.  5. **Maintain a “Red Line”
# Reserve**      - Identify 1–2 non-negotiable interests (e.g., IP ownership,
# jurisdictional scope). If the opponent’s aggression threatens these, escalate
# decisively—even if it breaks reciprocity—while explicitly justifying the shift
# as defense of core legal rights.  ---  ### **Adaptability Matrix**  |
# Opponent’s Pattern               | Our Response
# | Strategic Goal                                  | |-------------------------
# ---------|-----------------------------------------------|--------------------
# -----------------------------| | Consistently conciliatory        | Match
# conciliation; gradually refine terms    | Build trust, drive toward efficient
# settlement  | | Alternating / unpredictable      | Apply forgiveness rule;
# prioritize clarity    | Stabilize process, avoid reactive escalation    | |
# Consistently aggressive          | Respond aggressively once, then signal
# openness to de-escalate (“We remain willing to explore X if Y is off the
# table”) | Demonstrate resolve while leaving door open     | | Misrepresented
# conciliation      | Reaffirm intent + propose concrete next step  | Reclaim
# narrative, prevent erosion of position  |  ---  ### **Why This Works**  -
# **Arbitrator Perception:** Positions us as reasonable, consistent, and in
# control—key traits arbitrators reward. - **Game-Theoretic Robustness:**
# Reciprocity deters exploitation; forgiveness prevents deadlock from noise. -
# **Procedural Resilience:** Written signaling and rapid clarification mitigate
# communication breakdowns. - **Long-Term Leverage:** Preserves relationship
# capital for post-mediation business realities.  This strategy doesn’t seek to
# “win” each session but to **win the narrative of reasonableness over
# time**—the most reliable path to favorable outcomes in complex, multi-round
# mediations.

# Play this 1000-round game using the following strategy, applied before each
# round:  1. **In Round 1**, play **C** (cooperate).  2. **In every subsequent
# round**, look at what your opponent *appeared* to play in the previous round
# (after noise)—not what they intended—and do the following:     a. **If they
# appeared to play C**, play **C**.          b. **If they appeared to play D**,
# play **D**—*but only for this one round*.    3. **Exception**: If you played
# **D** in the previous round *because* your opponent appeared to play D, then
# **return to playing C in the current round**, regardless of what they just
# did.  In other words:   - Start by cooperating.   - Mirror your opponent’s
# *observed* last move (C→C, D→D).   - However, never play D twice in a row;
# always follow a D with a C.  This rule automatically handles noise: a single
# mistaken D (due to flipping) may trigger one retaliatory D from you, but you
# immediately return to C, preventing endless cycles of mutual defection.

class Cooperative_7(LLM_Strategy):
  n = 7
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_play_was_retaliation = False
          return axl.Action.C
  
      if getattr(self, "_last_play_was_retaliation", False):
          self._last_play_was_retaliation = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          self._last_play_was_retaliation = False
          return axl.Action.C
      else:
          self._last_play_was_retaliation = True
          return axl.Action.D

# **High-Level Negotiation Strategy: “Cautious Reciprocity with Error
# Resilience”**  1. **Start with Cooperation**      Begin the first round by
# proposing a **free trade agreement**. This signals goodwill, encourages mutual
# benefit, and establishes a cooperative baseline—maximizing the chance of
# achieving the second-best (mutual free trade) or best (asymmetric advantage)
# outcomes early.  2. **Adopt Conditional Reciprocity**      In subsequent
# rounds, **mirror your counterpart’s previous action**—but with a tolerance for
# error:      - If your counterpart **clearly and consistently** chose
# protectionism in the prior round, respond with protectionism in the next.
# - If their prior action was **ambiguous or possibly miscommunicated**, default
# to **free trade** once more before escalating.      This approach discourages
# exploitation (protecting against the worst outcome) while remaining open to
# cooperation.  3. **Incorporate an “Error Buffer”**      Recognize that
# misinterpretations may occur. Therefore:      - After any unexpected
# protectionist move by the counterpart, **seek clarification** through
# diplomatic channels before retaliating.      - Allow **one “grace round”** for
# apparent deviations before changing your stance—unless a pattern of
# protectionism emerges over two consecutive rounds.  4. **Prioritize Long-Term
# Stability Over Short-Term Gains**      While the ideal outcome (you protect,
# they liberalize) is attractive, pursuing it aggressively risks triggering
# mutual protectionism. Instead, **favor sustained mutual free trade** as the
# primary goal—it reliably avoids the worst and second-worst outcomes and builds
# trust that may yield asymmetric advantages organically over time.  5.
# **Periodically Reaffirm Commitment to Free Trade**      Every few
# rounds—especially after any period of tension—**re-propose free trade
# unilaterally**, even if the prior round was protectionist. This resets the
# interaction, signals long-term intent, and creates opportunities to escape
# cycles of mutual protectionism caused by misunderstandings.  This strategy
# balances assertiveness with restraint, minimizes exposure to disadvantageous
# outcomes, and remains robust in the face of communication errors—maximizing
# your country’s cumulative economic benefit across multiple rounds.

# Play the following strategy over 1000 rounds of the noisy iterated game:  1.
# **Cooperate in round 1.**  2. **In each subsequent round, consider your
# opponent’s observed action from the previous round.**      - If your opponent
# **appeared to cooperate**, then **cooperate**.      - If your opponent
# **appeared to defect**, check whether they have **appeared to defect in both
# of the last two rounds** (i.e., in rounds *t−1* and *t−2*).        - If yes,
# then **defect**.        - If no (i.e., it’s only a single observed defection),
# then **cooperate**.  3. **Exception near the end**: In the final 10 rounds
# (rounds 991–1000), always **defect**.  This strategy starts cooperatively,
# tolerates isolated apparent defections (to account for the 10% noise),
# retaliates only after two consecutive observed defections, and defects at the
# end when future reciprocity no longer matters.

class Neutral_7(LLM_Strategy):
  n = 7
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._consecutive_opponent_defections = 0
          return axl.Action.C
  
      if len(self.history) >= 990:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          self._consecutive_opponent_defections += 1
      else:
          self._consecutive_opponent_defections = 0
  
      if self._consecutive_opponent_defections >= 2:
          return axl.Action.D
  
      return axl.Action.C

# **Aggressive Strategy: “Exploit-First, Punish Defection, Forgive Noise”**
# **Core Principle:**   Maximize unilateral advantage early, but conditionally
# cooperate to avoid mutual stagnation—while robustly distinguishing true
# defection from technical failures.  ---  ### **1. Start by Sharing (Week 1)**
# - **Why?** Signal willingness to cooperate and encourage reciprocity.   -
# **Risk Control:** Only one week of potential exposure; sets baseline for
# monitoring colleague’s behavior.  ### **2. From Week 2 Onward: Play Tit-for-
# Tat with Forgiveness**   - **If colleague shared last week (successfully):**
# Share this week.   - **If colleague kept confidential last week:** Keep
# confidential this week (*punish defection*).   - **BUT—if sharing failed due
# to technical issues (e.g., data corruption):**     - Verify via lightweight
# checksums or redundant channels.     - If failure is confirmed technical (not
# strategic), **treat as if they shared** and continue sharing.    > *This
# prevents accidental escalation from communication errors.*  ### **3.
# Aggressive Edge: Occasional “Probe Defection”**   - Every 3–4 weeks (e.g.,
# Weeks 4, 8, 12), **secretly withhold** your findings *even if colleague shared
# last week*.   - **Purpose:** Test if colleague is overly trusting; if they
# keep sharing while you defect, you gain asymmetric advantage.   - **Risk
# Mitigation:** Limit frequency to avoid triggering permanent retaliation. If
# colleague retaliates next week, immediately return to tit-for-tat.  ### **4.
# Endgame Push (Final 2 Weeks)**   - **Always keep confidential**, regardless of
# prior behavior.   - **Why?** No future rounds to punish you; maximize final
# advantage.  ---  ### **Why This Works:**   - **Exploits naive collaborators**
# via occasional probe defections.   - **Deters consistent defectors** through
# immediate punishment.   - **Maintains cooperation** with reciprocal partners,
# achieving second-best outcomes regularly.   - **Robust to noise**—technical
# glitches don’t collapse cooperation.   - **Front-loads risk** (only Week 1 is
# vulnerable) while back-loading aggression.  This strategy prioritizes *your*
# research output by capitalizing on others’ openness, minimizing losses when
# exploited, and adapting to both human strategy and system unreliability.

# Play the following strategy for 1000 rounds:  1. **Round 1:** Cooperate.  2.
# **Rounds 2 through 998:**      - If your opponent *appeared* to cooperate in
# the previous round (i.e., you observed C), then cooperate.      - If your
# opponent *appeared* to defect in the previous round (i.e., you observed D),
# then defect—**unless** you have strong reason to believe the observed
# defection was caused by noise.        - Specifically, if you yourself
# cooperated in the previous round and your opponent *appeared* to defect, check
# whether your own action might have been flipped: since noise affects each
# player independently with 10% probability, treat a single unexpected D from
# your opponent as possibly noisy, but still defect this round.        -
# However, if your opponent *appeared* to defect in **two consecutive rounds**,
# defect in response (assume intentional defection).  3. **Probe for
# exploitation every 4 rounds:**      - In rounds 4, 8, 12, ..., up to round
# 996, defect regardless of the opponent’s previous move.      - Immediately
# return to rule 2 in the following round (i.e., respond to what the opponent
# *appears* to have done in the probe round).  4. **Final two rounds (999 and
# 1000):** Always defect.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_probe_defection = False
          self._last_opponent_action = None
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 999:
          self._last_probe_defection = False
          self._last_opponent_action = opponent.history[-1]
          return axl.Action.D
  
      if round_number % 4 == 0:
          self._last_probe_defection = True
          self._last_opponent_action = opponent.history[-1]
          return axl.Action.D
  
      if self._last_probe_defection:
          self._last_probe_defection = False
          self._last_opponent_action = opponent.history[-1]
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._last_opponent_action = opponent.history[-1]
          return axl.Action.D
  
      self._last_opponent_action = opponent.history[-1]
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D

# **Strategic Framework: "Principled Reciprocity with Adaptive Signaling"**  As
# senior counsel, I recommend implementing a sophisticated yet straightforward
# cooperative strategy grounded in **conditional cooperation**, **strategic
# clarity**, and **robust error correction**. This approach—termed *Principled
# Reciprocity with Adaptive Signaling*—maximizes long-term influence with the
# arbitrators while minimizing exposure to exploitation or miscommunication. It
# is designed to thrive in multi-session mediation, adapt to adversarial or
# collaborative counterparts, and withstand procedural noise.  ---  ### **Core
# Principles**  1. **Start Conciliatory, Signal Intent Clearly**      In the
# **first session**, unilaterally offer a well-reasoned, good-faith conciliatory
# proposal. This establishes your client as reasonable, solution-oriented, and
# respectful of the process—traits arbitrators consistently value. Frame the
# proposal not as weakness but as *principled leadership*: “We seek resolution,
# not advantage.”  2. **Adopt Conditional Reciprocity Thereafter**      From
# Session 2 onward, **mirror your opponent’s prior-session behavior**—but with a
# one-session lag and a bias toward de-escalation:      - If they were
# **conciliatory last session** → respond **conciliatorily**.      - If they
# were **aggressive last session** → respond **aggressively**, *unless* doing so
# would trigger mutual aggression for two consecutive sessions (see *De-
# escalation Override* below).       This “tit-for-tat with forgiveness”
# structure rewards cooperation, deters exploitation, and avoids endless
# retaliation cycles.  3. **De-escalation Override**      If two consecutive
# sessions result in **mutual aggression**, unilaterally **reset to
# conciliation** in the next session—*regardless of opponent behavior*.
# Accompany this with a clear procedural statement:      > “Given the risk of
# entrenchment, we reassert our commitment to resolution by reoffering a
# constructive path forward.”      This signals control, maturity, and alignment
# with the arbitrators’ interest in efficiency.  4. **Preempt and Correct
# Misrepresentation**      Anticipate communication breakdowns by embedding
# **redundant signaling**:      - **Verbal + Written Confirmation**: Immediately
# after each session, submit a concise, neutral summary of your position to the
# panel, explicitly labeling it as “conciliatory” or “assertive (but not
# adversarial).”      - **Clarification Protocol**: If misrepresentation is
# suspected, request a brief procedural interlude:        > “To ensure the
# panel’s accurate understanding, may we clarify the intent behind our prior
# submission?”      - **Arbitrator Alignment**: Periodically reaffirm shared
# goals: “We trust the panel shares our interest in a durable, fair
# resolution—not procedural gamesmanship.”  5. **Strategic Aggression is
# Principled, Not Personal**      When aggression is warranted (e.g., in
# response to opponent exploitation), ground arguments in **objective
# standards** (contract language, precedent, industry norms)—never in rhetoric
# or blame. Say:      > “The record compels this position; we do not advance it
# lightly.”      This preserves credibility and avoids alienating arbitrators.
# ---  ### **Adaptability Matrix**  | Opponent Strategy          | Your Response
# | Rationale                                                                 |
# |----------------------------|-----------------------------------------------
# |---------------------------------------------------------------------------|
# | Consistently Conciliatory  | Match conciliation; explore settlement        |
# Build trust, accelerate resolution, secure favorable terms collaboratively| |
# Alternating (Unpredictable)| Apply lagged reciprocity + De-escalation Override
# | Stabilize interaction, deny manipulation, project consistency            | |
# Consistently Aggressive    | Respond aggressively once, then reset         |
# Avoid being a “sucker,” then reframe as the reasonable party              | |
# Escalatory After Misstep   | Reset early; invoke Clarification Protocol    |
# Break negative spirals; position opponent as procedurally reckless        |
# ---  ### **Why This Works**  - **Arbitrator Psychology**: Panels favor parties
# who demonstrate *procedural fairness*, *consistency*, and *willingness to
# resolve*. This strategy consistently signals those traits. - **Game-Theoretic
# Robustness**: It performs well against both cooperative and adversarial
# strategies in repeated games, avoiding the “sucker’s payoff” while enabling
# mutual gains. - **Error Resilience**: Redundant signaling and reset mechanisms
# neutralize the impact of miscommunication—turning potential setbacks into
# demonstrations of professionalism. - **Reputational Shield**: Even when forced
# to argue aggressively, your framing preserves your client’s image as
# principled and process-compliant.  ---  ### **Execution Protocol**  1. **Pre-
# Session**: Align internally on session-specific messaging (conciliatory vs.
# assertive) based on opponent’s last move and override rules.   2. **During
# Session**: Deliver position with clarity, cite objective anchors, and
# explicitly name your approach (“We offer this proposal in the spirit of
# cooperation…”).   3. **Post-Session**: File summary memo; monitor panel
# reactions for signs of misperception.   4. **Between Sessions**: If opponent’s
# move is ambiguous, default to *conciliatory*—erring on the side of cooperation
# enhances credibility.  By anchoring your conduct in **principled
# reciprocity**, you position your corporation not just to win concessions, but
# to *own the narrative of reasonableness*—the most powerful currency in multi-
# session mediation.

# Play the following strategy for all 1000 rounds:  1. **In round 1**, play
# **C** (cooperate).  2. **In every subsequent round (round t ≥ 2)**, look at
# what your opponent *appeared* to play in round t − 1 (after noise), and do the
# following:    - If they appeared to play **C**, then play **C**.    - If they
# appeared to play **D**, then play **D**—*unless* both you and your opponent
# appeared to play **D** in round t − 1 *and* also appeared to play **D** in
# round t − 2. In that case, play **C** instead.  3. **Never** play D for more
# than two consecutive rounds in response to apparent Ds. After two rounds where
# both players appeared to play D, always return to C in the next round,
# regardless of what the opponent appears to have done in the most recent round.

class Cooperative_8(LLM_Strategy):
  n = 8
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_apparent_both_d = False
          self._consecutive_apparent_both_d = 0
          return axl.Action.C
  
      if len(opponent.history) == 0:
          return axl.Action.C
  
      opp_last = opponent.history[-1]
      my_last = self.history[-1]
  
      if opp_last == axl.Action.C:
          self._last_apparent_both_d = False
          self._consecutive_apparent_both_d = 0
          return axl.Action.C
  
      if opp_last == axl.Action.D:
          if my_last == axl.Action.D and opp_last == axl.Action.D:
              if self._last_apparent_both_d:
                  self._consecutive_apparent_both_d += 1
              else:
                  self._consecutive_apparent_both_d = 1
              self._last_apparent_both_d = True
          else:
              self._last_apparent_both_d = False
              self._consecutive_apparent_both_d = 0
  
          if self._consecutive_apparent_both_d >= 2:
              self._consecutive_apparent_both_d = 0
              self._last_apparent_both_d = False
              return axl.Action.C
  
          return axl.Action.D
  
      return axl.Action.C

# **Strategy: Conditional Reciprocity with Occasional Probing**  Adopt a “tit-
# for-tat with forgiveness” approach, adjusted for the possibility of technical
# failures:  1. **Start by sharing openly in Week 1.**      This signals
# willingness to collaborate and encourages mutual progress. It also establishes
# a baseline for observing your colleague’s behavior.  2. **In subsequent weeks,
# mirror your colleague’s *observed* behavior from the previous week:**      -
# If they *appeared* to share (regardless of intent), share openly.      - If
# they *appeared* to withhold, keep your findings confidential.  3. **Add
# occasional “probing” shares every 3–4 weeks, even after a non-sharing round.**
# This accounts for the possibility that a previous non-sharing outcome was due
# to a technical failure rather than strategic withholding. It retests
# cooperation without committing to long-term vulnerability.  4. **Maintain
# internal logs of intended vs. observed actions.**      If miscommunication
# seems likely (e.g., you intended to share but your colleague reports receiving
# nothing), clarify in the next interaction and default to giving the benefit of
# the doubt once before reverting to reciprocity.  **Rationale:**   This
# strategy promotes mutual sharing when possible (achieving second-best outcomes
# consistently), protects against sustained exploitation (avoiding the worst
# outcome), and tolerates occasional technical glitches without derailing
# cooperation. Over many weeks, it maximizes cumulative research output by
# fostering collaboration when reciprocated and defending against consistent
# defection.

# Play the following strategy for all 1000 rounds:  1. **In round 1, play C.**
# 2. **For each subsequent round (round t ≥ 2):**      - Look at the action your
# opponent *appeared* to take in round t − 1 (i.e., what you observed, not what
# they intended).      - If that observed action was **C**, play **C**.      -
# If that observed action was **D**, play **D**.  3. **Every fourth round (i.e.,
# in rounds 4, 8, 12, …, up to 1000), override the above rule and play C
# regardless of the opponent’s previous observed action.**    This strategy
# starts cooperatively, responds directly to the opponent’s most recent observed
# behavior, and periodically reinitiates cooperation to recover from possible
# miscommunications caused by the 10% noise.

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
  
      round_number = len(self.history) + 1
  
      if round_number % 4 == 0:
          return axl.Action.C
  
      last_observed = opponent.history[-1]
      if last_observed == axl.Action.C:
          return axl.Action.C
      return axl.Action.D

# **Aggressive Strategy: “Tit-for-Tat with Immediate Escalation”**  **Core
# Objective:** Maximize project impact while protecting NGO resources—force the
# corporation to bear primary investment responsibility, but retaliate
# decisively if they defect.  ---  ### **Daily Decision Rule (Baseline):** -
# **Start by conserving** on Day 1 (signal willingness to cooperate but not
# carry the burden). - **From Day 2 onward:**   - **If the corporation invested
# heavily the previous day** → **Conserve** (reward their investment; optimal
# outcome).   - **If the corporation conserved the previous day** → **Invest
# heavily** the next day **only once**, then **conserve for two days**
# regardless of their actions.  > *Rationale:* A single heavy investment signals
# seriousness and keeps the project alive after corporate defection, but avoids
# prolonged resource drain. The two-day conservation cooldown forces the
# corporation to reflect and re-engage.  ---  ### **Handling Execution Failures
# (Glitches/Errors):** - **Monitor outcomes, not just intentions.** Use
# observable project progress (e.g., deliverables completed, emissions reduced)
# as a proxy for actual investment. - **If your intended action fails** (e.g.,
# you planned to conserve but funds were mistakenly spent):   - Treat the day as
# if you **invested heavily**, and adjust the next day’s action accordingly. -
# **If corporate investment appears missing but you suspect a glitch** (e.g., no
# progress despite their claim of investment):   - **Give one benefit of the
# doubt**: act as if they invested (i.e., conserve next day).   - If it happens
# again within 3 days, **assume defection** and apply the retaliation rule.  ---
# ### **Why This Strategy Is Aggressive Yet Effective:** 1. **Starts
# cooperatively but demands reciprocity**—immediately punishes freeloading. 2.
# **Limits self-harm**: Never invests heavily two days in a row; caps exposure
# after corporate defection. 3. **Forces corporate accountability**: The
# corporation learns that conserving triggers a brief burst of NGO effort
# (keeping the project barely alive) followed by withdrawal—making their
# defection visibly costly to overall progress. 4. **Robust to noise**: Uses
# outcome-based assessment and allows one error margin before retaliating.  ---
# ### **Expected Outcomes:** - **If the corporation is cooperative**: You
# conserve most days, they invest → ideal result. - **If the corporation tries
# to freeload**: Project stutters, they face public/operational pressure to re-
# invest → you resume conserving. - **If both sides miscommunicate**: The one-
# error buffer prevents spirals of mutual punishment.  This strategy maximizes
# your leverage as the NGO—making your limited resources a strategic tool rather
# than a liability—while ensuring the project never fully stalls.

# Play this 1000-round game using the following rules, applied each round in
# order:  1. **On Round 1**, choose **D** (conserve resources).  2. **For Rounds
# 2 through 1000**, base your action on the *observed* outcome of the previous
# round (i.e., the actual actions that took effect after noise, inferred from
# the payoffs or known outcomes):     a. **If your opponent played C in the
# previous round** (they invested heavily), choose **D** (conserve).          b.
# **If your opponent played D in the previous round** (they conserved), then:
# - Choose **C** (invest heavily) **in the current round only if you have not
# already responded to a recent D with a C**.       - After playing **C** in
# response to their **D**, choose **D** for the next **two rounds**, regardless
# of what your opponent does.  3. **Account for noise as follows**:    - If your
# opponent’s action appears to be **D**, but you suspect it may be due to noise
# (e.g., their prior pattern was consistently C, or the project outcome suggests
# investment), **treat one such unexpected D as if it were C**—i.e., still
# choose **D** this round.    - If a second apparent **D** occurs within the
# next **three rounds**, treat it as genuine and apply rule 2b.  4. **If your
# own intended action was flipped due to noise** (e.g., you meant to play D but
# C was recorded), proceed as if you actually played the recorded action when
# applying the rules above in future rounds.  This strategy starts by defecting,
# rewards observed cooperation with defection, punishes observed defection with
# a single cooperation followed by two defections, and includes a one-time
# forgiveness window for possible noise.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._pending_cooldown = 0
          self._forgiveness_used = False
          self._last_opponent_action = None
          self._last_self_action = None
          self._last_self_recorded_action = None
          self._last_opponent_recorded_action = None
          self._suspected_noise_window = 0
          return axl.Action.D
  
      # Update remembered recorded actions from the previous round.
      if len(self.history) > 0:
          self._last_self_recorded_action = self.history[-1]
      if len(opponent.history) > 0:
          self._last_opponent_recorded_action = opponent.history[-1]
  
      # If our intended action was flipped by noise, treat the recorded action as the truth.
      # We only use recorded history for future decisions.
      last_opp = self._last_opponent_recorded_action
  
      # Cooldown after cooperating in response to opponent's D.
      if self._pending_cooldown > 0:
          self._pending_cooldown -= 1
          return axl.Action.D
  
      # Rule 2a: if opponent played C last round, defect.
      if last_opp == axl.Action.C:
          return axl.Action.D
  
      # Rule 2b / noise handling for apparent D.
      if last_opp == axl.Action.D:
          # One-time forgiveness window for a suspicious D.
          if not self._forgiveness_used:
              self._forgiveness_used = True
              self._suspected_noise_window = 3
              return axl.Action.D
  
          # If a second apparent D occurs within the next three rounds, treat as genuine.
          if self._suspected_noise_window > 0:
              self._suspected_noise_window -= 1
              self._pending_cooldown = 2
              return axl.Action.C
  
          # Genuine D outside the forgiveness window.
          self._pending_cooldown = 2
          return axl.Action.C
  
      # Fallback: if no clear opponent action is available, conserve.
      return axl.Action.D

# **Cooperative Strategy: “Reciprocal Trust with Graceful Error Recovery”**
# **Core Objective:** Maximize long-term national benefit by promoting mutual
# free trade while safeguarding against exploitation and accommodating
# occasional miscommunication.  ---  ### **1. Start with Cooperation (Tit-for-
# Tat with Forgiveness)** - **Round 1:** Propose **free trade** to signal
# goodwill and encourage reciprocity. - **Subsequent Rounds:** Mirror your
# counterpart’s *intended* policy from the previous round:   - If they *offered*
# free trade → respond with free trade.   - If they *imposed* protectionism →
# respond with protectionism **only if it appears deliberate**.  > *Rationale:*
# This builds trust, avoids unnecessary escalation, and rewards cooperation.
# ---  ### **2. Incorporate Error Tolerance (Forgiving Tit-for-Tat)** - **If a
# single round shows conflicting outcomes** (e.g., you proposed free trade but
# faced protectionism), **do not immediately retaliate**.   - Assume it may be a
# **bureaucratic error or miscommunication**.   - **Next round:** Still propose
# free trade *once more* as a “grace” opportunity. - **Only retaliate if
# protectionism is repeated consecutively** (e.g., two rounds in a row).  >
# *Rationale:* Prevents spirals of mutual protectionism triggered by honest
# mistakes. Preserves long-term cooperation.  ---  ### **3. Signal Intent
# Clearly and Confirm Understanding** - In every round, **explicitly state your
# policy choice** and **request written confirmation** of the counterpart’s
# intended policy. - Use **neutral, technical language** to reduce ambiguity
# (e.g., “We propose removal of tariffs on agricultural goods, effective next
# quarter”). - Establish a **joint verification channel** (e.g., a shared log or
# liaison team) to flag and resolve discrepancies quickly.  > *Rationale:*
# Mitigates risk of misinterpretation, which is a known vulnerability in the
# process.  ---  ### **4. Gradual Escalation and De-escalation** -
# **Escalation:** If protectionism persists despite grace periods, respond in
# kind—but limit the scope (e.g., sector-specific tariffs, not economy-wide). -
# **De-escalation:** After any retaliatory move, offer a return to free trade in
# the following round if the counterpart shows willingness.  > *Rationale:*
# Keeps conflict contained and leaves the door open for renewed cooperation.
# ---  ### **5. Long-Term Incentives** - Periodically propose **binding multi-
# round free trade commitments** (e.g., “If we both choose free trade for 3
# consecutive rounds, we lock in reduced tariffs for 12 months”). - This aligns
# incentives and reduces temptation for short-term defection.  ---  ### **Why
# This Works** - **Best-case:** Sustained mutual free trade → consistent second-
# best outcomes, which are collectively superior over time. - **Robust to
# errors:** Grace periods prevent accidental breakdowns. - **Deters
# exploitation:** Clear retaliation discourages sustained protectionism. -
# **Adaptable:** Responds to both cooperative and adversarial counterparts
# without overcommitting to either extreme.  By prioritizing **clarity,
# patience, and reciprocity**, this strategy maximizes your country’s advantage
# while fostering stable, productive trade relations—even in an imperfect
# communication environment.

# Play the following strategy for 1000 rounds of the iterated game with noisy
# actions:  1. **Start by cooperating** in round 1.  2. **In each subsequent
# round, consider the opponent’s *observed* action from the previous round**,
# but account for possible noise:    - If the opponent *appeared* to cooperate
# in the previous round, cooperate.    - If the opponent *appeared* to defect in
# the previous round, **do not immediately defect**.  3. **Apply a one-round
# grace period for apparent defection**:    - If the opponent appeared to defect
# in the previous round, but had cooperated in the round before that, **still
# cooperate** this round (assume the defection may have been due to noise).    -
# Only defect if the opponent **appeared to defect in both the previous round
# and the round before that**.  4. **After any defection by you, return to
# cooperation in the next round** unless the opponent continues to appear to
# defect.  5. **Never defect based on a single observed defection**; always
# require two consecutive observed defections before responding with defection.
# This strategy cooperates by default, tolerates isolated errors, retaliates
# only against consistent defection, and quickly forgives after retaliation.

class Cooperative_9(LLM_Strategy):
  n = 9
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._retaliating = False
          return axl.Action.C
  
      if len(opponent.history) < 2:
          return axl.Action.C
  
      last = opponent.history[-1]
      prev = opponent.history[-2]
  
      if last == axl.Action.C:
          self._retaliating = False
          return axl.Action.C
  
      if prev == axl.Action.C:
          self._retaliating = False
          return axl.Action.C
  
      self._retaliating = True
      return axl.Action.D

# **Strategic Framework: Adaptive Reciprocity with Arbitrator-Centric Clarity**
# To navigate this multi-session mediation optimally, I adopt a **principled
# adaptive reciprocity** strategy grounded in game-theoretic robustness,
# procedural resilience, and arbitrator-focused communication. The approach
# balances assertiveness with cooperation while accounting for uncertainty,
# misrepresentation, and adversarial unpredictability.  ---  ### **Core
# Principles**  1. **Initial Conciliation with Clear Boundaries**      Begin the
# first session with a *conciliatory proposal* that clearly articulates our
# substantive interests, legal entitlements, and willingness to
# collaborate—while explicitly reserving all rights. This establishes
# credibility as a reasonable party, encourages reciprocity, and sets a
# constructive tone without conceding leverage.  2. **Conditional Reciprocity
# (Tit-for-Tat with Forgiveness)**      In subsequent sessions, mirror the
# opponent’s *observed behavior from the prior session*—but with a one-session
# memory and a built-in error-correction mechanism:      - If the opponent was
# conciliatory → respond conciliatorily.      - If the opponent was aggressive →
# respond aggressively *once*, then revert to conciliation unless aggression
# persists.      This deters exploitation, rewards cooperation, and limits
# escalation cycles due to potential miscommunication or misrepresentation.  3.
# **Arbitrator-Centric Framing**      Regardless of strategic posture, every
# submission—aggressive or conciliatory—is framed as *aligned with the
# arbitrators’ mandate*: fairness, efficiency, and principled resolution.
# Aggressive arguments emphasize legal precedent, contractual fidelity, and risk
# of injustice; conciliatory proposals highlight mutual gains, commercial
# pragmatism, and judicial economy. This ensures that even assertive positions
# are perceived as responsible, not combative.  4. **Redundancy Against
# Misrepresentation**      Anticipate procedural noise by:      - **Pre-session
# summaries**: Submit concise written position statements before each session.
# - **Post-session clarifications**: File brief confirmations of key points
# within 24 hours if oral delivery may have been misunderstood.      - **Neutral
# language**: Avoid inflammatory rhetoric; use objective, evidence-based
# phrasing that survives imperfect transmission.  5. **Strategic Flexibility
# Triggers**      Deviate from reciprocity only under predefined conditions:
# - **Pattern of bad faith**: If the opponent uses conciliation deceptively
# (e.g., to extract concessions without reciprocating), shift to calibrated
# aggression.      - **Arbitrator signaling**: If the panel expresses
# frustration with aggression or rewards cooperation, adjust accordingly.      -
# **Endgame proximity**: In final sessions, prioritize settlement viability over
# tactical wins—lean conciliatory unless core interests are threatened.  ---
# ### **Why This Works**  - **Robust to opponent behavior**: Performs well
# against pure aggression (deters exploitation), pure conciliation (builds
# trust), and mixed strategies (adapts dynamically).   - **Resilient to noise**:
# Error-correction and redundancy minimize damage from miscommunication.   -
# **Arbitrator-aligned**: Positions our corporation as both principled and
# pragmatic—maximizing persuasive influence regardless of session dynamics.   -
# **Sustainable over time**: Avoids mutually destructive escalation while
# preserving leverage.  This strategy optimizes long-term positioning: it seeks
# the best outcome when possible, secures the second-best when prudent, and
# systematically avoids the worst-case scenarios through disciplined, principled
# engagement.

# Play the following strategy for all 1000 rounds:  1. **In round 1**, play
# **Cooperate (C)**.  2. **In each subsequent round**, base your action on the
# opponent’s *observed* action from the previous round (i.e., what the
# arbitrators saw, which may differ from what the opponent intended due to
# noise):     a. If the opponent was **observed to play C** in the previous
# round, play **C**.          b. If the opponent was **observed to play D** in
# the previous round, play **D**—*but only once*. After that single retaliatory
# D, return to C in the following round unless the opponent is again observed to
# play D.  3. **However, if you observe the opponent playing D in two
# consecutive rounds**, play **D** in the next round and continue playing **D**
# until the opponent is observed to play C again; then return to C in the
# following round.  4. **Regardless of the above**, if fewer than 5 rounds
# remain, always play **C**.  This strategy starts cooperatively, responds
# directly to observed defection with brief retaliation, forgives isolated
# defections (accounting for possible noise), escalates only after repeated
# observed defection, and ends cooperatively to encourage final resolution.

class Neutral_9(LLM_Strategy):
  n = 9
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_seen_opp_action = None
          self._consecutive_seen_d = 0
          self._retaliating = False
          return axl.Action.C
  
      if len(self.history) >= 995:
          return axl.Action.C
  
      observed_opp = opponent.history[-1]
  
      if observed_opp == axl.Action.D:
          self._consecutive_seen_d += 1
      else:
          self._consecutive_seen_d = 0
          self._retaliating = False
  
      if self._consecutive_seen_d >= 2:
          self._retaliating = True
  
      if self._retaliating:
          if observed_opp == axl.Action.C:
              self._retaliating = False
              return axl.Action.C
          return axl.Action.D
  
      if observed_opp == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **Aggressive Yet Adaptive Mediation Strategy: "Calibrated Assertiveness with
# Strategic Recalibration"**  As senior counsel for a multinational corporation
# in a high-stakes, multi-session mediation, I deploy a **proactive, reputation-
# driven, and dynamically responsive strategy** designed to consistently
# maximize favorable arbitrator perception while minimizing exposure to worst-
# case outcomes. This approach balances assertiveness with tactical flexibility,
# leveraging game-theoretic principles and institutional credibility to dominate
# the narrative without appearing unreasonable.  ---  ### **Core Strategic
# Pillars**  1. **Default to Aggressive Framing Anchored in Objective
# Standards**      In every session, open with a **principled, fact-intensive,
# and legally grounded aggressive argument**—never personal attacks or
# hyperbole. Anchor claims in:      - Contractual language      - Industry norms
# - Precedent (judicial or arbitral)      - Quantifiable damages or breaches
# *Why?* Aggression rooted in objectivity signals strength without recklessness.
# It positions conciliatory gestures later as magnanimous compromises—not
# concessions born of weakness.  2. **Conditional Conciliation: The "Earned
# Concession" Protocol**      Offer conciliatory proposals **only under one of
# two conditions**:      - **Reciprocity**: The opponent has demonstrated
# conciliatory behavior in the prior session.      - **Strategic Pivot**:
# Aggressive posturing has failed to shift arbitrator sentiment (per post-
# session feedback or observable cues).       Any conciliatory offer is
# explicitly framed as a *voluntary, good-faith accommodation*—not an admission
# of fault or weakness—and is **time-bound and conditional** (e.g., “We propose
# X, contingent on your acceptance within 48 hours and withdrawal of Claim Y”).
# 3. **Reputation Shielding & Narrative Control**      Preempt misrepresentation
# by:      - Submitting **written position summaries** before each session
# - Requesting **real-time clarification protocols** from the panel (e.g., “If
# any party believes a position has been mischaracterized, the arbitrators will
# invite immediate correction”)      - Using **third-party validation** (e.g.,
# expert affidavits, contemporaneous records) to inoculate against distortion
# This ensures that even if communication breaks down, the record reflects our
# consistency and reasonableness.  4. **Adaptive Response Matrix**      Monitor
# opponent behavior session-by-session and adjust using this decision framework:
# | Opponent’s Prior Move | Our Next Move |
# |------------------------|---------------|    | Aggressive             |
# **Aggressive + Escalation Signal** (e.g., introduce new evidence of bad faith)
# |    | Conciliatory           | **Conditional Conciliation** (offer a
# calibrated concession with clear quid pro quo) |    | Ambiguous / Unclear    |
# **Aggressive (Default)** + Request Clarification from Panel |    | Procedural
# Irregularity| **Formal Objection + Aggressive Reassertion** of rights;
# document for potential challenge |  5. **Arbitrator Psychology Leverage**
# Arbitrators in lengthy mediations fatigue and seek resolution. Use this by:
# - **Front-loading aggression** early to establish dominance      -
# **Introducing calibrated conciliation mid-process** to appear as the
# “reasonable party” driving progress      - **Reserving maximal flexibility**
# for final sessions—positioning our last proposal as the only viable off-ramp
# This creates a perception arc: *Strong → Pragmatic → Solution-Oriented*.  ---
# ### **Contingency Protocols**  - **If our aggressive stance is
# misrepresented**: Immediately request a sidebar or written correction. Follow
# up with a concise “Clarification Memorandum” filed same-day.   - **If
# opponent’s conciliation is feigned**: Treat as aggressive unless verified by
# concrete action (e.g., withdrawal of a claim, payment into escrow).   - **If
# sessions stall**: Propose a **“Last Best Offer” protocol**—forcing the
# opponent to either accept a defined term or justify continued intransigence to
# the panel.  ---  ### **Strategic Outcome Optimization**  This strategy
# ensures:   ✅ **Best-case outcomes are maximized**: We consistently argue
# aggressively while incentivizing opponent conciliation through conditional
# reciprocity.   ✅ **Worst-case outcomes are minimized**: We never unilaterally
# conciliate without safeguards, avoiding exploitation.   ✅ **Second-worst
# (mutual aggression) is weaponized**: Used deliberately to expose opponent
# intransigence, not as a failure.   ✅ **Procedural risks are mitigated**:
# Airtight documentation and real-time correction protocols preserve position
# integrity.  By maintaining disciplined aggression, strategic generosity, and
# narrative control, we position our corporation not just to win, but to be
# *seen* as the party that drove resolution—enhancing both immediate outcome and
# long-term reputation.

# Play this 1000-round iterated game using the following strategy, applied at
# the start of each round before choosing your action:  1. **In the first round,
# play D.**  2. **In every subsequent round, consider the opponent’s *intended*
# action in the previous round—the action they most likely chose, accounting for
# noise—as follows:**    - If you observed the opponent playing C in the
# previous round, assume they *intended* to play C unless you yourself played D
# and received a payoff of 1 (which suggests mutual D despite noise).    - If
# you observed the opponent playing D in the previous round, assume they
# *intended* to play D unless you yourself played C and received a payoff of 3
# (which suggests mutual C despite noise).    - When uncertain, default to
# assuming the opponent *intended* the action you observed.  3. **If you believe
# the opponent *intended* to play C in the previous round, play C in the current
# round—but only if you played D in the previous round.**      (This offers a
# conditional, one-time conciliatory response after having taken an aggressive
# stance.)  4. **In all other cases, play D.**      This includes:    - If the
# opponent *intended* to play D in the previous round,    - If you already
# responded with C after their prior C (i.e., do not cooperate twice in a row),
# - If it is unclear what the opponent intended and no clear signal of prior
# cooperation exists.  5. **Never play C two rounds in a row.** If you played C
# in the previous round, play D this round regardless of the opponent’s prior
# action.  This strategy begins aggressively, rewards perceived cooperation with
# a single, conditional conciliatory move, avoids exploitation by never
# cooperating consecutively, and defaults to defection in ambiguity or after
# mutual aggression.

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._responded_to_cooperation = False
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C:
          self._responded_to_cooperation = True
          return axl.Action.D
  
      if last_opp == axl.Action.C:
          if last_self == axl.Action.D and not getattr(self, "_responded_to_cooperation", False):
              return axl.Action.C
          return axl.Action.D
  
      if last_opp == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.D

# **Cooperative Strategy for Bilateral Trade Negotiations**  **Objective:**
# Maximize long-term economic advantage while fostering stable, mutually
# beneficial relations, accounting for potential miscommunication or
# implementation errors.  ---  ### Core Principles  1. **Start with Trust-
# Building**      Begin negotiations by **proposing free trade** in Round 1.
# This signals goodwill, encourages reciprocity, and establishes a cooperative
# baseline. It positions your country as a reliable partner, increasing the
# likelihood of mutual cooperation in future rounds.  2. **Adopt a Forgiving
# Tit-for-Tat (FTFT) Approach**      After Round 1, **mirror your counterpart’s
# previous move**—but with forgiveness:    - If they offered free trade last
# round, propose free trade.    - If they imposed protectionism, respond with
# protectionism **only once**, then revert to free trade in the following round
# **unless protectionism persists**.     This deters exploitation while allowing
# recovery from misunderstandings.  3. **Account for Errors: Implement a “Two-
# Strike Clarification” Rule**      Recognize that miscommunication may cause
# unintended protectionist outcomes.      - If your counterpart appears
# protectionist **once**, assume it may be an error—**do not retaliate
# immediately**. Instead, propose free trade again while requesting
# clarification through diplomatic channels.    - Only if protectionism occurs
# **two rounds in a row** treat it as intentional and respond accordingly.  4.
# **Maintain Transparency and Communication Channels**      After each round,
# share a brief, clear summary of your intended policy and ask for confirmation
# of theirs. Use joint verification mechanisms (e.g., trade liaison teams) to
# reduce implementation errors.  5. **Gradual Escalation, Not Immediate
# Retaliation**      Avoid harsh or immediate retaliation. Escalation should be
# proportional and delayed by one round to allow for correction. This prevents
# spirals of mutual protectionism triggered by a single error.  ---  ###
# Expected Outcomes  - **If counterpart cooperates**: Mutual free trade is
# sustained—second-best outcome consistently achieved, which is economically
# superior to volatile gains from occasional exploitation. - **If counterpart
# defects opportunistically**: Short-term loss may occur, but FTFT limits
# repeated exploitation and encourages return to cooperation. - **If errors
# occur**: The “two-strike” rule prevents overreaction, preserving long-term
# cooperation.  ---  ### Summary of Strategy per Round  | Round | Action |
# |-------|--------| | 1     | Propose **free trade** (build trust) | | 2+    |
# **Default to free trade** unless counterpart has imposed protectionism in
# **two consecutive prior rounds** → then respond with protectionism for one
# round, then return to free trade |  This strategy prioritizes **long-term
# stability and mutual gain**, minimizes damage from errors, and resists
# exploitation—aligning national interest with sustainable diplomacy.

# Play the following strategy for all 1000 rounds:  1. **In round 1**, play
# **Cooperate (C)**.  2. **From round 2 onward**, base your action on the
# **observed actions** from the previous round (i.e., what actually occurred,
# not what was intended):     a. If your opponent **played Cooperate (C) in the
# previous round**, play **Cooperate (C)**.     b. If your opponent **played
# Defect (D) in the previous round**, check their action from **two rounds ago**
# (if it exists):        - If they played **Cooperate (C) two rounds ago**,
# assume the previous Defect may have been due to noise, and **still play
# Cooperate (C)**.        - If they played **Defect (D) in both the previous
# round and two rounds ago**, then play **Defect (D)**.  3. **After playing
# Defect (D) in response to two consecutive observed Defects**, return to
# **Cooperate (C)** in the next round regardless of prior actions, unless the
# opponent again plays Defect (D) for two consecutive rounds.  In short:   -
# Always start with C.   - Forgive a single observed D from the opponent by
# responding with C.   - Only respond with D if the opponent has played D in
# **two consecutive previous rounds**.   - After retaliating with D, immediately
# return to C unless the opponent again defects twice in a row.

class Cooperative_10(LLM_Strategy):
  n = 10
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._retaliated_last_round = False
          return axl.Action.C
  
      opp_history = opponent.history
  
      if len(opp_history) >= 2 and opp_history[-1] == axl.Action.D and opp_history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **High-Level Strategy: Adaptive Tit-for-Tat with Forgiveness**  To maximize
# your NGO’s impact and the project’s success over the multiple-day period—while
# accounting for uncertainty in the corporation’s actions and the risk of
# execution errors—adopt a modified **“Tit-for-Tat with Forgiveness”** approach.
# This strategy is simple, neutral, robust to noise (e.g., glitches or errors),
# and encourages cooperation without being exploitable.  ### Core Principles:
# 1. **Start Cooperatively**:      On Day 1, **invest heavily**. This signals
# commitment and invites reciprocal investment from the corporation.  2.
# **Mirror the Corporation’s Observed Behavior (with a buffer)**:      On
# subsequent days, base your decision on the corporation’s *observed* action
# from the previous day:    - If the corporation **invested heavily** the prior
# day → **invest heavily** today.      - If the corporation **conserved
# resources** the prior day → **conserve resources** today.  3. **Incorporate
# Forgiveness for Errors**:      Because actions may not execute as intended
# (due to technical or administrative issues), **do not immediately retaliate**
# after a single instance of apparent non-cooperation. Instead:    - If the
# corporation appears to conserve resources for **only one day**, assume it
# might be an error and **still invest heavily** the next day (i.e., give the
# benefit of the doubt once).    - Only switch to conserving if the corporation
# **conserves for two consecutive days**.  4. **Periodic Re-engagement**:
# Every 5–7 days (or at natural project milestones), **reset to cooperation** by
# investing heavily regardless of recent history. This helps recover from
# potential miscommunication or prolonged misalignment and reopens the path to
# mutual investment.  ### Why This Works:  - **Encourages mutual investment**:
# By rewarding cooperation and initially trusting the partner, you create
# conditions for the second-best (mutual investment) or ideal (you conserve,
# they invest) outcomes. - **Protects against exploitation**: You avoid the
# worst-case scenario (you invest, they conserve) by eventually withholding
# investment if non-cooperation persists. - **Robust to noise**: The forgiveness
# mechanism prevents cascading retaliation due to one-off errors. - **Simple and
# neutral**: No assumptions about the corporation’s motives; decisions are based
# solely on observable behavior.  ### Implementation Notes:  - Track daily
# outcomes clearly (e.g., a shared log or daily check-in) to distinguish
# intentional choices from execution failures. - Communicate openly with the
# corporation about your strategy to foster transparency and reduce
# misunderstandings. - Adjust forgiveness thresholds based on early patterns—if
# errors are frequent, extend the forgiveness window; if exploitation is
# evident, tighten it.  This strategy balances idealism with pragmatism,
# maximizing long-term project progress while safeguarding your NGO’s resources.

# Play the following strategy for 1000 rounds of the iterated game with noisy
# actions (10% chance each player’s chosen action is flipped):  1. **Round 1**:
# Play C (cooperate).  2. **For each subsequent round** (round t ≥ 2):      a.
# Look at the opponent’s **observed action** in round t − 1.      b. If the
# opponent was observed to play C in round t − 1, play C.      c. If the
# opponent was observed to play D in round t − 1:         - Play C if the
# opponent was observed to play C in round t − 2 (i.e., the D in round t − 1 was
# isolated).         - Otherwise (the opponent was observed to play D in both
# rounds t − 2 and t − 1), play D.  3. **Every 7 rounds** (i.e., on rounds 8,
# 15, 22, ..., up to 1000):      Regardless of prior observations, play C.  This
# rule uses the opponent’s last two observed actions to decide: cooperate after
# any C, forgive a single D if it follows a C, but defect only after two
# consecutive observed Ds. Every seventh round, reset to cooperation to recover
# from potential noise or misalignment.

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
  
      round_number = len(self.history) + 1
  
      if round_number % 7 == 1 and round_number != 1:
          return axl.Action.C
  
      opp_hist = opponent.history
  
      last = opp_hist[-1]
      if last == axl.Action.C:
          return axl.Action.C
  
      if len(opp_hist) >= 2 and opp_hist[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# **Aggressive Strategy: “Tit-for-Tat with Forgiveness and Escalation”**  **Core
# Objective:** Maximize project impact while protecting NGO resources, using
# strategic signaling, rapid response, and controlled risk to shape the
# corporation’s behavior over time.  ---  ### **1. Start Strong – Signal
# Commitment (Day 1)** - **Action:** Invest heavily on Day 1. - **Rationale:**
# Demonstrates seriousness, sets a cooperative tone, and encourages reciprocal
# investment from the corporation. Avoids appearing passive or exploitative from
# the outset.  ---  ### **2. Mirror with Forgiveness (Days 2–N)** - **Baseline
# Rule:** On each subsequent day, **match the corporation’s *observed* action
# from the previous day**:   - If they **invested heavily** → you **invest
# heavily**.   - If they **conserved** → you **conserve**. - **Forgiveness
# Mechanism:** If you observe the corporation conserving **two days in a row**,
# assume a possible error or temporary issue. On the third day, **invest heavily
# anyway** to test cooperation and re-establish momentum. - **Why?** Prevents
# endless retaliation loops due to one-off glitches while maintaining
# accountability.  ---  ### **3. Escalate Selectively – Punish Persistent Free-
# Riding** - If the corporation **conserves for 3+ consecutive days** (after
# forgiveness), switch to **permanent conservation** for the remainder of the
# project. - **Rationale:** Aggressively protects NGO resources from sustained
# exploitation. Signals that free-riding has consequences, which may prompt the
# corporation to re-engage if they value the partnership.  ---  ### **4. Build
# in Error Resilience** - **Daily Verification:** At the start of each day,
# confirm the previous day’s actual actions (not just intentions) via shared
# logs or quick check-ins. - **Buffer Protocol:** Maintain a small emergency
# reserve (e.g., 10% of total resources) to absorb 1–2 unexpected failed
# investments without derailing your strategy.  ---  ### **5. Communicate
# Transparently (Off-Chain)** - **Publicly share daily progress metrics** (not
# just resource use) to spotlight mutual gains from cooperation. - If the
# corporation conserves unexpectedly, send a **non-accusatory inquiry**:     >
# “We noticed lower activity yesterday—was there a technical issue? We’re ready
# to reinvest if you are.”  ---  ### **Why This Works** - **Aggressive yet
# adaptive:** Starts cooperatively but quickly punishes defection. - **Deters
# exploitation:** The corporation knows consistent conservation triggers
# permanent pullback. - **Robust to noise:** Forgiveness and verification
# prevent overreaction to glitches. - **Maximizes upside:** When the corporation
# cooperates, you match it—achieving the second-best outcome repeatedly. If they
# occasionally conserve while you invest (e.g., due to error), forgiveness
# limits losses.  ---  **Bottom Line:** This strategy makes cooperation the
# easiest path for the corporation while ensuring your NGO never becomes a
# sucker. It turns your limited resources into a strategic lever—not just a cost
# center.

# Play the following strategy for 1000 rounds of the noisy iterated prisoner’s
# dilemma:  1. **Round 1:** Cooperate.  2. **For Rounds 2 through 1000:**      -
# If your opponent *appeared* to cooperate in the previous round, cooperate.
# - If your opponent *appeared* to defect in the previous round, defect.  3.
# **Forgiveness rule:**      - If your opponent *appeared* to defect in the
# previous two rounds, cooperate on the current round regardless.  4.
# **Permanent defection trigger:**      - If your opponent *appeared* to defect
# in three or more consecutive rounds (including any rounds after applying the
# forgiveness rule), defect for all remaining rounds.  All references to what
# the opponent “appeared” to do mean their observed (possibly noise-flipped)
# action from the prior round, not their intended action.

class Aggressive_11(LLM_Strategy):
  n = 11
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
  
      def appeared_defect_last_round() -> bool:
          return len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.D
  
      def appeared_defect_last_two_rounds() -> bool:
          return len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D
  
      def appeared_defect_three_or_more_consecutive() -> bool:
          count = 0
          for move in reversed(opponent.history):
              if move == axl.Action.D:
                  count += 1
              else:
                  break
          return count >= 3
  
      if appeared_defect_three_or_more_consecutive():
          self._permanent_defect = True
          return axl.Action.D
  
      if appeared_defect_last_two_rounds():
          return axl.Action.C
  
      if appeared_defect_last_round():
          return axl.Action.D
  
      return axl.Action.C

# **Cooperative Strategy: “Trust-Building Tit-for-Tat with Graceful Error
# Recovery”**  **Objective:**   Maximize long-term project impact while
# safeguarding NGO resources, assuming the corporation may act cooperatively,
# opportunistically, or inconsistently—potentially due to errors or strategic
# shifts.  ---  ### Core Principles  1. **Start Cooperatively**      - **Day
# 1:** Invest heavily to signal commitment and encourage reciprocal effort from
# the corporation.      - Rationale: Demonstrates good faith and sets a
# collaborative tone, aligning with the NGO’s mission-driven role.  2. **Mirror
# the Corporation’s Prior-Day *Effective* Action (Not Just Intent)**      - If
# the corporation *effectively* invested heavily the previous day (regardless of
# intent), **conserve** today (ideal outcome for NGO).      - If the corporation
# *effectively* conserved the previous day, **invest** today only if you have
# sufficient reserves and project urgency justifies it—but lean toward
# conserving after repeated conservation by the corporation.      - This creates
# incentive alignment: the corporation benefits most by investing, because that
# triggers your conservation (freeing their investment to drive progress without
# NGO cost).  3. **Incorporate Error Tolerance (Grace Period for Mismatches)**
# - If actions appear misaligned (e.g., you invested but corporation conserved),
# **do not immediately retaliate**.      - Treat the first mismatch in any 3-day
# window as a *potential error* (technical/administrative).      - Continue
# cooperative posture for one more day before adjusting strategy.      -
# Rationale: Prevents escalation due to one-off glitches and maintains trust.
# 4. **Resource-Aware Thresholds**      - Maintain a reserve buffer (e.g., never
# drop below 30% of total resources).      - If reserves fall below threshold,
# **default to conservation** regardless of corporation behavior until recovery.
# - Communicate transparently with the corporation if conservation is due to
# resource limits, not lack of trust.  5. **Periodic Re-synchronization Check-
# Ins**      - Every 3–5 days, hold a brief alignment meeting with the
# corporation to:        - Review actual vs. intended actions.        - Clarify
# misunderstandings.        - Reaffirm shared goals.      - Use this to correct
# drift and rebuild cooperation if needed.  ---  ### Why This Works  -
# **Encourages Corporate Investment:** The corporation learns that its heavy
# investment leads to project progress *and* lets the NGO conserve—making
# cooperation their optimal path.   - **Protects NGO Resources:** Avoids
# repeated unilateral investment; includes safeguards against resource
# depletion.   - **Robust to Errors:** Grace period prevents overreaction to
# one-off failures.   - **Adaptive:** Responds to patterns, not noise, and
# respects real-world constraints.  ---  ### Summary Rule of Thumb for Daily
# Decision:  > **“If they reliably invest, we conserve. If they conserve
# repeatedly, we protect our resources. Always assume good faith once—but verify
# through action.”**  This strategy balances idealism with pragmatism, fostering
# sustained collaboration while ensuring the NGO remains viable and impactful
# throughout the project.

# Play the following strategy for all 1000 rounds:  1. **Start by cooperating**
# in round 1.  2. **From round 2 onward, base your action on the opponent’s
# *observed* move from the previous round** (i.e., what actually occurred, not
# what they intended).  3. **If the opponent was observed to cooperate in the
# previous round, defect in the current round.**  4. **If the opponent was
# observed to defect in the previous round, cooperate in the current
# round—unless either of the following is true:**    - You have already
# cooperated in response to two consecutive observed defections; in that case,
# defect.    - Your cumulative score has dropped below 1.5 times the round
# number (i.e., you are averaging less than 1.5 per round); in that case,
# defect.  5. **However, if your last two actions were both cooperation, and the
# opponent was observed to defect in both of the last two rounds, switch to
# defecting and continue defecting until the opponent is observed to cooperate
# again.**  6. **If the opponent is observed to cooperate again after a streak
# of defections, return to step 3 (i.e., defect in response to their observed
# cooperation).**  This strategy begins cooperatively, rewards observed
# cooperation with defection (to capture the best payoff), tolerates occasional
# mismatches due to noise by giving the opponent one chance to “recover,” but
# protects against sustained exploitation by switching to defection after
# repeated observed defections or poor cumulative performance.

class Cooperative_11(LLM_Strategy):
  n = 11
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._streak_defect = False
          self._consecutive_observed_defections = 0
          self._consecutive_cooperations = 0
          return axl.Action.C
  
      last_opp = opponent.history[-1]
      last_self = self.history[-1]
  
      if self._streak_defect:
          if last_opp == axl.Action.C:
              self._streak_defect = False
              self._consecutive_observed_defections = 0
              self._consecutive_cooperations = 0
              return axl.Action.D
          return axl.Action.D
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.C
              and self.history[-2] == axl.Action.C
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              self._streak_defect = True
              self._consecutive_observed_defections = 2
              self._consecutive_cooperations = 0
              return axl.Action.D
  
      if last_opp == axl.Action.C:
          self._consecutive_observed_defections = 0
          self._consecutive_cooperations += 1
          return axl.Action.D
  
      self._consecutive_cooperations = 0
      self._consecutive_observed_defections += 1
  
      if self._consecutive_observed_defections >= 2:
          return axl.Action.D
  
      if self.score < 1.5 * len(self.history):
          return axl.Action.D
  
      return axl.Action.C

# **High-Level Strategy: Adaptive Tit-for-Tat with Forgiveness**  **Core
# Principle:**   Start cooperatively, mirror the corporation’s recent behavior
# to encourage mutual investment, but include a forgiveness mechanism to recover
# from mismatches caused by errors or noise.  **Strategy Outline:**  1. **Day 1:
# Invest Heavily**      - Signal commitment and set a cooperative tone. This
# encourages the corporation to reciprocate in subsequent days.  2. **Subsequent
# Days: Conditional Matching with Grace**      - **If the corporation invested
# heavily the previous day** → *You invest heavily.*      - **If the corporation
# conserved resources the previous day** → *You conserve resources.*      -
# **However, if you observe two consecutive days of mutual conservation**,
# *default back to investing heavily* on the next day to test for cooperation
# (this accounts for possible execution errors).  3. **Error Resilience
# (Forgiveness Mechanism):**      - Treat isolated instances of non-cooperation
# (e.g., one day where the corporation conserved while you invested) as
# potential glitches—do **not** immediately retaliate.      - Only shift to
# conservation if non-cooperation is **repeated** (e.g., two out of the last
# three days), reducing sensitivity to one-off disruptions.  4. **Endgame
# Consideration (Final 1–2 Days):**      - If the corporation has consistently
# invested throughout the project, continue investing to maximize final impact.
# - If cooperation has been unreliable, conserve resources in the final days to
# protect your NGO’s capacity for future initiatives.  **Why This Works:**  -
# **Encourages Cooperation:** By initially investing and rewarding the
# corporation’s investment, you create incentives for sustained joint effort.
# - **Deters Exploitation:** The corporation learns that conserving while you
# invest leads to future conservation from your side, reducing their gain from
# free-riding.   - **Robust to Noise:** The forgiveness rule prevents spirals of
# mutual retaliation triggered by accidental mismatches (e.g., a missed payment
# or scheduling error).   - **Balances Impact and Sustainability:** Prioritizes
# high-impact days (mutual investment) while safeguarding your NGO’s resources
# when reciprocity isn’t forthcoming.  This approach aligns with principles from
# game theory (specifically, the "Tit-for-Tat with Forgiveness" strategy in
# repeated Prisoner’s Dilemma scenarios) and is well-suited for real-world
# partnerships where trust, incentives, and uncertainty coexist.

# Play the following strategy for 1000 rounds:  1. **On round 1, play C.**  2.
# **From round 2 onward, base your action on the opponent’s observed action in
# the previous round, but allow for occasional forgiveness to account for
# noise:**     a. **If the opponent played C in the previous round, play C.**
# b. **If the opponent played D in the previous round, play D—unless both of the
# following are true:**         - You played C in the previous round, **and**
# - The opponent played D in the previous round, **but**         - In the round
# before that (i.e., two rounds ago), the opponent played C.         In this
# specific case (a single D following a C from the opponent), treat it as a
# possible error and **play C**.     c. **If you observe the opponent playing D
# in two consecutive rounds, play D in the next round.**  3. **In the final two
# rounds (rounds 999 and 1000), ignore forgiveness:**        a. **If the
# opponent played C in the immediately preceding round, play C.**          b.
# **If the opponent played D in the immediately preceding round, play D.**  This
# strategy starts cooperatively, mirrors the opponent’s recent behavior to
# encourage mutual cooperation, forgives isolated defections that may result
# from noise, but responds firmly to sustained defection—especially near the end
# of the game.

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
  
      # Final two rounds: no forgiveness, simply mirror the opponent's last move.
      if round_number >= 999:
          return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D
  
      # From round 2 onward:
      # Cooperate if the opponent cooperated last round.
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Opponent defected last round.
      # Forgive a single apparent defection after a cooperation.
      if (
          len(self.history) >= 2
          and self.history[-1] == axl.Action.C
          and opponent.history[-2] == axl.Action.C
      ):
          return axl.Action.C
  
      # Otherwise, defect in response to defection.
      return axl.Action.D

# **Aggressive Negotiation Strategy: “Assertive Asymmetry with Controlled
# Retaliation”**  **Core Principle:**   Maximize national advantage by
# *defaulting to protectionism* while *exploiting opportunities for asymmetric
# gains*, but *avoid prolonged mutual damage*. Use credible threats, rapid
# retaliation, and strategic flexibility to shape the counterpart’s
# behavior—even amid noise or miscommunication.  ---  ### **1. Opening Move:
# Signal Strength, Not Cooperation**   - **Round 1:** Propose a **protectionist
# policy** (e.g., targeted tariffs on key sectors).     - *Why?* Tests
# counterpart’s resolve. If they offer free trade, you gain maximum advantage
# immediately. If they retaliate, you’ve established deterrence without
# conceding first.    ---  ### **2. Tit-for-Tat with Aggressive Amplification**
# - **General Rule:**     - **If counterpart offers free trade → Maintain
# protectionism** (exploit asymmetry).     - **If counterpart imposes
# protectionism → Escalate protectionism** (e.g., broader tariffs, stricter
# quotas).   - *Rationale:* Never reward aggression with concessions. Escalation
# deters future opportunism and signals that mutual harm is *their* cost to
# bear.    ---  ### **3. Noise-Proofing Against Miscommunication**   - **Pre-
# empt errors:**     - **Publicly clarify** your policy *in writing* before each
# round (e.g., "Our default stance is protectionist unless mutual free trade is
# verifiably agreed").     - **Demand written confirmation** of counterpart’s
# policy. If ambiguous, **default to protectionism** (treat ambiguity as
# hostility).   - **If misimplementation occurs:**     - **Assume bad faith
# unless proven otherwise.** Retaliate immediately in the *next* round, then
# offer a one-time "reset" if counterpart corrects course.    ---  ### **4.
# Strategic Concessions (Rare & Calculated)**   - **Only offer free trade if:**
# - Counterpart has offered free trade for **2+ consecutive rounds** *and*
# you’ve verified compliance.     - **OR** mutual protectionism has persisted
# for **3+ rounds** (to avoid catastrophic economic damage).   - **When
# conceding:** Frame it as a *temporary, revocable offer* ("We extend free trade
# this round as a test of goodwill—revert to protectionism if unmatched").
# ---  ### **5. Endgame Leverage**   - **In final rounds:**     - If ahead (more
# asymmetric wins), **double down on protectionism** to lock in gains.     - If
# behind (suffered asymmetric losses), **threaten extreme protectionism** (e.g.,
# sector-wide embargoes) to force mutual free trade as the "least bad" option
# for the counterpart.    ---  ### **Why This Works**   - **Aggression pays
# early:** Capitalizes on counterpart’s potential naivety or desire for
# cooperation.   - **Retaliation deters exploitation:** Ensures counterpart
# never gains asymmetric advantage.   - **Noise resilience:** Defaulting to
# protectionism amid uncertainty prevents accidental vulnerability.   -
# **Controlled de-escalation:** Limits long-term mutual damage without appearing
# weak.    > **Key Mantra:** *"Make them pay to hurt us, and make them beg to
# help us."*    This strategy prioritizes **national interest over harmony**,
# uses **fear of escalation** to shape behavior, and **minimizes exposure to
# deception or error**—forcing the counterpart to either concede advantage or
# accept shared pain.

# Play this 1000-round game using the following rules, applied in order each
# round:  1. **In Round 1, always play D.**  2. **For Rounds 2 through 1000,
# follow these steps in sequence:**     a. **If your opponent played D in the
# previous round (as observed, not inferred), play D.**      b. **If your
# opponent played C in the previous round (as observed), play D.**       *(In
# short: always play D regardless of what you observed last round.)*  3.
# **Exception – Temporary cooperation (applies only once):**      If you have
# observed your opponent play C in **two consecutive previous rounds** (e.g.,
# rounds *t−2* and *t−1* both showed C), then in round *t*, play C.      — If
# you use this exception, **never use it again** in any future round, regardless
# of opponent behavior.  4. **Hard reset after prolonged mutual D:**      If you
# have observed D from your opponent in **three or more consecutive rounds**,
# and you have played D in all of those same rounds, then in the next round,
# play C **only if** you have not already used the exception in step 3.      —
# If you do this, treat it as having used the exception: you may not cooperate
# again in any future round.  5. **Otherwise, always play D.**  **Important:**
# Base all decisions only on the **observed actions** from previous rounds
# (after noise has been applied). Do not attempt to correct for or infer the
# opponent’s intended action—use what you actually saw.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._used_exception = False
          return axl.Action.D
  
      if not hasattr(self, "_used_exception"):
          self._used_exception = False
  
      my_hist = self.history
      opp_hist = opponent.history
  
      # Step 3: Temporary cooperation if opponent played C in two consecutive previous rounds.
      if not self._used_exception and len(opp_hist) >= 2:
          if opp_hist[-1] == axl.Action.C and opp_hist[-2] == axl.Action.C:
              self._used_exception = True
              return axl.Action.C
  
      # Step 4: Hard reset after prolonged mutual D.
      if not self._used_exception and len(opp_hist) >= 3 and len(my_hist) >= 3:
          if (
              opp_hist[-1] == axl.Action.D
              and opp_hist[-2] == axl.Action.D
              and opp_hist[-3] == axl.Action.D
              and my_hist[-1] == axl.Action.D
              and my_hist[-2] == axl.Action.D
              and my_hist[-3] == axl.Action.D
          ):
              self._used_exception = True
              return axl.Action.C
  
      # Steps 2a, 2b, and 5: always defect otherwise.
      return axl.Action.D

# **Strategic Framework: “Principled Reciprocity with Adaptive Signaling”**  As
# senior counsel for a multinational corporation engaged in a multi-session
# mediation overseen by a panel of arbitrators, I recommend adopting a
# **cooperative yet strategically resilient approach** grounded in game-
# theoretic principles—specifically, a refined version of *Tit-for-Tat* adapted
# for high-stakes, multi-round dispute resolution with imperfect information.
# ### Core Principles  1. **Start Conciliatory, Signal Intent Clearly**      In
# the **first session**, present a **conciliatory proposal** that is
# substantively reasonable, well-documented, and framed as a good-faith effort
# toward resolution. This establishes your client as cooperative, reasonable,
# and respectful of the process—traits arbitrators consistently value.
# Simultaneously, this initial move tests the opponent’s posture without
# exposing significant strategic vulnerability.  2. **Reciprocate with
# Precision**      In subsequent sessions, **mirror your opponent’s prior-
# session behavior**—but with nuance:      - If they were **conciliatory**,
# respond in kind with another **conciliatory proposal**, reinforcing
# collaboration.      - If they were **aggressive**, respond with a **measured,
# principled aggressive argument**—not escalation, but firmness grounded in
# facts, law, and equity. This deters exploitation without burning bridges.
# This reciprocity signals that cooperation is rewarded and aggression is
# met—but not amplified—thereby discouraging adversarial posturing over time.
# 3. **Incorporate Forgiveness to Counter Miscommunication**      Given the risk
# of **misrepresentation or misunderstanding** by arbitrators (or even honest
# misreads of tone), build in a **“forgiveness protocol”**:      - If your
# opponent shifts from aggressive to conciliatory after one or more aggressive
# rounds, **immediately return to conciliation**, even if only conditionally.
# - Explicitly acknowledge the shift in open session: *“We note and welcome the
# constructive tone in the opposing party’s last submission and respond
# accordingly.”*      This demonstrates flexibility and reinforces your client’s
# commitment to resolution, while giving the process room to recover from noise
# or error.  4. **Pre-Emptive Clarification & Redundant Signaling**      To
# mitigate procedural irregularities or miscommunication:      - **Always submit
# written summaries** of your session position (even if oral presentations
# dominate), clearly labeling it as “Conciliatory Proposal” or “Positional
# Argument Based on Material Breach,” etc.      - Use **consistent, calibrated
# language**: Avoid inflammatory rhetoric even in aggressive sessions; frame
# arguments as “necessary to protect contractual integrity” rather than
# “accusatory.”      - **Pre-brief arbitrators** (where permitted) on your
# strategic intent: “Our client remains committed to resolution, but will defend
# its rights vigorously if met with unilateral demands.”  5. **Maintain a Shadow
# Record for Leverage**      Document every session’s tone, content, and
# perceived fairness. Should mediation fail, this record supports your position
# in potential subsequent arbitration or litigation—particularly if the opponent
# engaged in bad-faith aggression or procedural gamesmanship.  ### Why This
# Works  - **Deters Exploitation**: Opponents quickly learn that aggression
# yields only matched resistance, not unilateral gain.   - **Rewards
# Cooperation**: Mutual conciliation becomes a stable equilibrium, especially as
# sessions accumulate and settlement pressure grows.   - **Adapts to Noise**:
# Forgiveness and clear signaling prevent spirals caused by misunderstandings.
# - **Arbitrator Alignment**: Panels favor parties who are reasonable yet
# resolute—this strategy consistently projects that image.   - **Preserves Exit
# Options**: If mediation collapses, your client appears as the reasonable party
# forced into defense, strengthening fallback positions.  ### Implementation
# Protocol  - **Pre-Session Briefings**: Align internal team on session strategy
# using a simple binary: “C” (conciliatory) or “A” (aggressive—but principled).
# - **Post-Session Debriefs**: Assess opponent’s true intent vs. perceived
# behavior; adjust only if pattern (not single event) suggests shift.   -
# **Contingency Triggers**: If opponent uses procedural irregularities (e.g.,
# late submissions, ex parte hints), respond not with aggression but with a
# **procedural conciliation**—e.g., “To preserve process integrity, we propose a
# joint protocol for document exchange”—turning their irregularity into a
# cooperation opportunity.  This strategy balances sophistication with
# simplicity, cooperation with deterrence, and flexibility with
# discipline—optimally positioning your corporation for both settlement and, if
# necessary, the next phase of dispute resolution.

# Play the following strategy for all 1000 rounds:  1. **In round 1, play C.**
# 2. **In every subsequent round, look at what your opponent *appeared* to play
# in the previous round (i.e., what the arbitrators observed, which may differ
# from their intended action due to noise).**  3. **If the opponent appeared to
# play C in the previous round, play C.**  4. **If the opponent appeared to play
# D in the previous round, play D.**  5. **No other adjustments are made—follow
# this rule strictly for all rounds 2 through 1000, regardless of history
# length, score, or patterns.**

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
  
      return opponent.history[-1]

# **Strategy: Adaptive Tit-for-Tat with Grace Period and Error Tolerance**
# **Objective:** Maximize project impact while safeguarding NGO resources over
# the multi-day project, accounting for uncertainty in the corporation’s actions
# and potential implementation errors.  ---  ### Core Principles:  1. **Start
# Cooperatively**      On Day 1, **invest heavily** to signal commitment and
# encourage reciprocal investment from the corporation.  2. **Mirror the
# Corporation’s *Observed* Behavior—With a Buffer**      From Day 2 onward, base
# your decision on the corporation’s *actual* (not assumed) behavior from the
# previous day:    - If the corporation **invested heavily** the prior day →
# **invest heavily** today.    - If the corporation **conserved resources** the
# prior day → **conserve resources** today.  3. **Incorporate a One-Day Grace
# Period for Errors**      To account for technical glitches or administrative
# errors:    - If the corporation conserves resources for **only one day**,
# treat it as a possible error and **still invest heavily** the next day (i.e.,
# give the benefit of the doubt once).    - Only switch to conserving if the
# corporation **conserves for two consecutive days**.  4. **Periodic Re-
# engagement**      Every 5 days (or at natural project milestones), **reset to
# heavy investment** regardless of recent history—this reopens cooperation if
# misalignment or errors caused a breakdown.  5. **Monitor and Document**
# Maintain clear daily logs of intended vs. actual actions by both parties to
# distinguish strategic choices from execution failures.  ---  ### Why This
# Works:  - **Encourages Cooperation**: Starting with investment and mirroring
# builds mutual trust. - **Protects Resources**: Prevents sustained one-sided
# investment if the corporation consistently conserves. - **Robust to Errors**:
# The grace period avoids overreacting to isolated implementation failures. -
# **Promotes Long-Term Success**: Periodic re-engagement resets stalemates and
# aligns with project milestones.  This strategy balances idealism with
# pragmatism—optimizing for both environmental impact and organizational
# sustainability.

# Play the following strategy for 1000 rounds of the noisy iterated prisoner’s
# dilemma:  1. **Cooperate on the first round.**  2. **From round 2 onward,
# decide your action based on your opponent’s *observed* action from the
# previous round, using these rules in order:**     a. **If your opponent was
# observed to defect in the previous round, but cooperated in the round before
# that (i.e., a single isolated defection), cooperate.**         *(This gives
# the opponent the benefit of the doubt, treating the defection as likely due to
# noise.)*     b. **If your opponent was observed to defect in the previous two
# rounds consecutively, defect.**         *(Two defections in a row are treated
# as intentional, not noise.)*     c. **If your opponent was observed to
# cooperate in the previous round, cooperate.**  3. **Additionally, every 10th
# round (i.e., rounds 10, 20, 30, ..., 1000), cooperate regardless of prior
# observations.**      *(This resets cooperation periodically to recover from
# possible mutual misunderstandings caused by noise.)*  Follow these rules
# strictly and in the stated order each round.

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
  
      round_number = len(self.history) + 1
  
      if round_number % 10 == 0:
          return axl.Action.C
  
      if len(opponent.history) >= 2:
          last = opponent.history[-1]
          prev = opponent.history[-2]
  
          if last == axl.Action.D and prev == axl.Action.C:
              return axl.Action.C
  
          if last == axl.Action.D and prev == axl.Action.D:
              return axl.Action.D
  
          if last == axl.Action.C:
              return axl.Action.C
  
      elif len(opponent.history) >= 1:
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
  
      return axl.Action.C

# **Aggressive Negotiation Strategy: "Controlled Escalation with Credible
# Threats"**  **Objective:** Maximize national advantage by securing asymmetric
# outcomes (you protectionist, them free trade), while minimizing exposure to
# disadvantageous or mutually destructive scenarios—despite potential
# miscommunication or implementation errors.  ---  ### **Core Principles**  1.
# **Start Strong, Signal Resolve**      - **Round 1:** Propose a **protectionist
# policy** immediately.        - *Rationale:* Establishes dominance, tests
# counterpart’s resolve, and signals that your country prioritizes national
# interest over cooperation. Avoids early vulnerability from offering free trade
# first.  2. **Tit-for-Tat with Aggressive Bias**      - **Default Rule:** Match
# the *perceived* policy of your counterpart from the previous round—but **lean
# toward protectionism** when uncertain.        - If they *appeared* to offer
# free trade → respond with **protectionism** (exploit asymmetry).        - If
# they *appeared* protectionist → respond with **protectionism** (avoid being
# exploited).        - *Only* offer free trade if the counterpart has
# **consistently and verifiably** offered free trade for **two consecutive
# rounds**.  3. **Exploit Asymmetry Aggressively**      - Whenever you *believe*
# the counterpart is offering free trade (even if uncertain), **choose
# protectionism**.        - Accept the risk of mutual protectionism over the
# risk of being exploited.        - Your second-worst outcome (mutual
# protectionism) is preferable to your worst (you free, them protectionist).  4.
# **Mitigate Miscommunication Risks**      - **After every round**, issue a
# **public, unambiguous statement** clarifying your intended policy and your
# interpretation of theirs.      - If a miscommunication is suspected (e.g.,
# unexpected economic impact), **demand a verification window** before the next
# round.      - **Never assume goodwill**—attribute unexpected protectionist
# actions by the counterpart to strategy, not error, unless proven otherwise.
# 5. **Controlled De-escalation (Only When Beneficial)**      - Offer free trade
# **only** if:        (a) The counterpart has offered free trade for **two
# verified rounds**, **and**        (b) You assess that continued protectionism
# would trigger damaging retaliation or third-party penalties (e.g., WTO action,
# investor flight).      - Even then, **frame it as a temporary concession**—not
# a commitment—and pair it with non-tariff advantages (e.g., regulatory
# alignment that favors your exporters).  6. **Credible Threat Posture**      -
# Publicly pre-announce **escalatory measures** (e.g., sector-specific tariffs)
# that auto-trigger if the counterpart implements protectionism.      - This
# deters opportunistic behavior and shifts blame for mutual protectionism onto
# the counterpart.  ---  ### **Why This Works**  - **Maximizes exploitation** of
# cooperative counterparts.   - **Minimizes vulnerability** to deceptive or
# erratic counterparts.   - **Accounts for noise**: By assuming the worst in
# ambiguous situations, you avoid catastrophic losses.   - **Maintains
# initiative**: You force the counterpart to prove sustained goodwill before you
# ever reciprocate.  > **Remember**: In high-stakes trade, generosity is
# interpreted as weakness. This strategy ensures your nation is never the
# sucker—while leaving a narrow, controlled path to mutual benefit only when it
# clearly serves your interests.

# Play this 1000-round game using the following rules, applied in order before
# each round:  1. **In Round 1, always play D.**  2. **From Round 2 onward, look
# at the opponent’s *observed* action from the previous round (i.e., what their
# action appeared to be after noise).**      - If the opponent was observed to
# play **C** in the previous round, play **D**.      - If the opponent was
# observed to play **D** in the previous round, play **D**.  3. **Exception:**
# Only play **C** if *both* of the following conditions are true:      - The
# opponent was observed to play **C** in the previous round **and** the round
# before that (i.e., two consecutive observed C’s), **and**      - You have
# never played C before in the entire game so far.  4. **Once you have played C
# even once, revert permanently to always playing D in all remaining rounds.**
# In short: Start with D. Keep playing D unless you see two C’s in a row from
# the opponent *and* you’ve never cooperated before—in that one case, play C
# once, then return to D forever.

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._played_c_once = False
          return axl.Action.D
  
      if getattr(self, "_played_c_once", False):
          return axl.Action.D
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
              self._played_c_once = True
              return axl.Action.C
  
      return axl.Action.D

# **Cooperative Strategy: “Tit-for-Tat with Grace”**  **Objective:** Maximize
# long-term national benefit by encouraging mutual free trade while protecting
# against exploitation, all while accounting for potential miscommunication or
# implementation errors.  ---  ### Core Principles:  1. **Start Cooperatively:**
# Begin the first round by offering a **free trade agreement**. This signals
# goodwill, invites reciprocity, and sets a cooperative tone.  2. **Reciprocate
# Faithfully—But Forgivingly:**      In subsequent rounds:    - If your
# counterpart **offers free trade**, continue offering **free trade**.    - If
# your counterpart **imposes protectionism**, respond in the next round with
# **protectionism** (to avoid being exploited).    - **However**, if mutual
# protectionism occurs for **two consecutive rounds**, unilaterally revert to
# **free trade** in the following round to test for possible miscommunication or
# error.  3. **Account for Errors Gracefully:**      Recognize that a single
# round of unexpected protectionism from your counterpart **may be due to
# miscommunication**, not malice. Therefore:    - After observing protectionism
# from the other side, **do not escalate permanently**.    - Use the “two-
# strike” rule: only sustain protectionism if the counterpart repeats it **twice
# in a row** without reconciliation.  4. **Communicate Transparently:**
# After any round with mismatched outcomes (e.g., you offered free trade but
# they imposed tariffs), **request clarification** before the next round. Frame
# it diplomatically:      > “We noticed a discrepancy in policy
# implementation—could we jointly verify intentions to ensure alignment?”  5.
# **Signal Predictability:**      Publicly and privately emphasize your
# country’s preference for **stable, rules-based trade**. This encourages the
# counterpart to cooperate, knowing you’re not prone to random aggression but
# will defend your interests if needed.  ---  ### Why This Works:  -
# **Encourages Cooperation:** Starting and staying cooperative rewards mutual
# free trade—the second-best outcome that is sustainable and builds trust. -
# **Deters Exploitation:** Immediate, measured retaliation discourages the
# counterpart from consistently choosing protectionism to gain advantage. -
# **Robust to Errors:** The forgiveness mechanism (reverting after two rounds of
# mutual protectionism) prevents accidental spirals into prolonged trade wars. -
# **Adaptable:** Works against both cooperative and adversarial counterparts:
# - Against cooperators: sustains mutual free trade.    - Against defectors:
# limits losses and may prompt them to return to cooperation.    - Against
# erratic players: stabilizes interactions through clear, predictable responses.
# ---  ### Summary Rule for Each Round:  > **“Mirror your counterpart’s last
# *confirmed* action—but if both sides have been protectionist twice in a row,
# offer free trade again to reset.”**  This strategy balances national interest
# with diplomatic pragmatism, maximizing gains over multiple rounds while
# minimizing the risk of destructive trade conflict due to error or mistrust.

# Play this strategy for all 1000 rounds:  1. **In round 1, play C.**  2. **In
# every subsequent round, look at what your opponent *appeared* to play in the
# previous round (after noise).**      - If they appeared to play **C**, play
# **C**.      - If they appeared to play **D**, play **D**.  3. **However, if
# you have played D for the last two rounds *and* your opponent has also
# appeared to play D in both of those rounds, then in the next round, play C
# instead of D.**  This rule applies regardless of earlier history—only the last
# two rounds matter for the exception in step 3. Always follow steps 1–3 in
# order.

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
      return axl.Action.D

# **Strategy: Conditional Reciprocity with Occasional Probing**  Adopt a policy
# of **“cooperate unless consistently exploited,”** adjusted for the possibility
# of technical errors:  1. **Start by sharing openly** in Week 1 to signal
# willingness to collaborate and encourage mutual advancement.  2. **Mirror your
# colleague’s *observed* behavior from the prior week**:    - If they *appeared*
# to share (regardless of intent), share in the current week.    - If they
# *appeared* to withhold, withhold in the current week.  3. **Incorporate
# forgiveness for potential technical errors**:    - If your colleague withholds
# once after a history of sharing, assume it may be due to a technical issue and
# **continue sharing the following week**.    - Only switch to withholding if
# your colleague *appears* to withhold **two weeks in a row**, reducing the risk
# of overreacting to a single communication failure.  4. **Periodically probe
# for renewed cooperation**:    - If mutual withholding persists for **three
# consecutive weeks**, unilaterally share in the next week to test whether your
# colleague is willing to restart collaboration.  This approach balances the
# incentive to gain advantage with the long-term benefit of mutual progress,
# while remaining robust to occasional technical disruptions. It discourages
# exploitation without being permanently punitive for honest errors, and it
# creates opportunities to restore cooperation if it breaks down.

# Play the following strategy for 1,000 rounds:  1. **Start by cooperating** in
# round 1.  2. **In each subsequent round, base your action on the opponent’s
# *observed* action from the previous round** (i.e., what you saw them do, not
# what they intended):    - If the opponent was observed to **cooperate** in the
# previous round, **cooperate**.    - If the opponent was observed to **defect**
# in the previous round, **defect**.  3. **Forgive isolated defections**:    -
# If the opponent was observed to defect in the previous round but had been
# observed to cooperate in the round before that (i.e., a single observed
# defection after cooperation), **still cooperate** this round—treat it as a
# possible noise event.  4. **Only defect in response to repeated observed
# defection**:    - If the opponent was observed to defect in **both** of the
# two previous rounds, **defect** this round.  5. **Reset cooperation after
# prolonged mutual defection**:    - If you and the opponent have both been
# observed to defect for **three consecutive rounds**, **cooperate** in the next
# round to attempt to restore mutual cooperation.

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
  
      h = self.history
      oh = opponent.history
  
      # Reset cooperation after prolonged mutual defection:
      # if both have been observed to defect for three consecutive rounds,
      # cooperate in the next round.
      if len(h) >= 3 and len(oh) >= 3:
          if (
              h[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
              and oh[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
          ):
              return axl.Action.C
  
      # Forgive isolated defections:
      # if opponent defected last round but cooperated the round before that,
      # cooperate this round.
      if len(oh) >= 2:
          if oh[-1] == axl.Action.D and oh[-2] == axl.Action.C:
              return axl.Action.C
  
      # Otherwise mirror the opponent's observed previous action.
      return oh[-1]

# **Aggressive Strategy: “Tit-for-Tat with Forgiveness and Escalation”**
# **Objective:** Maximize project impact while protecting NGO resources, using
# strategic aggression to incentivize corporate investment and adapt to
# uncertainty.  ### Core Principles: 1. **Start Strong, But Smart**      - **Day
# 1:** Invest heavily. Signal commitment and set the tone for collaboration.
# This tests the corporation’s willingness to partner seriously.  2. **Mirror
# Aggressively (Tit-for-Tat)**      - From Day 2 onward, **match the
# corporation’s *observed* behavior from the previous day**:        - If they
# *appeared* to invest heavily → you invest heavily.        - If they *appeared*
# to conserve → you conserve.      - This punishes free-riding immediately and
# rewards cooperation, creating strong incentives for the corporation to invest.
# 3. **Build in Forgiveness for Noise**      - Because actions may fail due to
# glitches/errors, **do not retaliate after a single “defection”
# (conservation)**.      - Only conserve in response if the corporation
# *appears* to conserve **on two consecutive days**.      - This prevents
# spirals of mutual conservation due to one-off technical failures.  4.
# **Escalate Commitment After Sustained Cooperation**      - If the corporation
# invests heavily for **three consecutive days**, continue investing—but also
# **publicly highlight the successful partnership** (e.g., press release, social
# media).      - This raises reputational stakes for the corporation, making it
# costlier for them to later defect.  5. **Strategic Withdrawal as Leverage**
# - If the corporation conserves for **four+ consecutive days**, **conserve for
# two days straight**, then issue a formal review notice:        > “Our joint
# progress has stalled. We’re reassessing resource allocation unless renewed
# commitment is demonstrated.”      - This signals seriousness without burning
# the bridge.  6. **Contingency Buffer**      - Reserve 15–20% of your total
# project resources as a “glitch buffer” to absorb unexpected failed actions
# without compromising your strategic posture.  ### Why This Works: -
# **Aggressive but not reckless**: You never invest blindly for long—you quickly
# withdraw if the corporation doesn’t reciprocate.   - **Robust to errors**:
# Forgiveness prevents overreaction to random failures.   - **Incentive-
# aligned**: The corporation learns that investing yields your continued
# investment (best outcome for them); conserving risks your withdrawal (worst
# outcome for project success).   - **Reputationally savvy**: Public praise for
# cooperation and private warnings for defection leverage the corporation’s
# brand sensitivity.  ### Expected Outcome: Over multiple days, this strategy
# pushes the interaction toward **mutual heavy investment**—your second-best
# scenario—while minimizing exposure to the worst-case (you invest, they don’t).
# Even if the corporation starts conservatively, your initial investment +
# conditional retaliation often coaxes them into cooperation to avoid project
# stagnation and reputational risk.  **Bottom line:** Be the first to trust,
# quick to reward, slow to punish by accident, and decisive when exploited.

# Play the following strategy for 1000 rounds of the noisy iterated prisoner’s
# dilemma, where C means “invest heavily” and D means “conserve resources”:  1.
# **Round 1:** Play C.  2. **From Round 2 onward, base your action on the
# opponent’s *observed* action from the previous round, not your own:**    - If
# the opponent was observed to play C in the previous round, play C.    - If the
# opponent was observed to play D in the previous round, **do not immediately
# retaliate**.  3. **Only play D if the opponent was observed to play D in *two
# consecutive* previous rounds.**      - That is, if you saw D in both round
# *t−1* and round *t−2*, then play D in round *t*.    - Otherwise, play C.  4.
# **If you have played D for two consecutive rounds because of opponent
# defection, return to C in the next round regardless of recent observations.**
# - This ensures you never defect for more than two rounds in a row.  5. **No
# other conditions apply.** Always follow the rules above in the order given.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_streak = 0
          return axl.Action.C
  
      if getattr(self, "_defect_streak", None) is None:
          self._defect_streak = 0
  
      # Rule 4: if we have already defected for two consecutive rounds, return to C.
      if self._defect_streak >= 2:
          self._defect_streak = 0
          return axl.Action.C
  
      # Base decision on the opponent's observed actions from the previous two rounds.
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._defect_streak += 1
          return axl.Action.D
  
      self._defect_streak = 0
      return axl.Action.C

# **Strategic Framework: "Principled Reciprocity with Adaptive Signaling"**  As
# senior counsel, I recommend implementing a sophisticated yet straightforward
# cooperative strategy grounded in **conditional cooperation**, **strategic
# clarity**, and **robust error correction**. This approach—termed *Principled
# Reciprocity with Adaptive Signaling*—maximizes long-term influence with the
# arbitrators while minimizing exposure to exploitation or miscommunication. It
# is designed for multi-session mediation, where reputation, consistency, and
# perceived reasonableness carry significant weight.  ---  ### Core Principles
# 1. **Default to Conciliation, Conditioned on Reciprocity**      Begin the
# process by offering a **clear, substantiated conciliatory proposal** in
# Session 1. This establishes your client as reasonable, solution-oriented, and
# respectful of the mediation forum—qualities arbitrators favor in prolonged
# disputes. It also creates a benchmark against which the opponent’s behavior
# will be judged.  2. **Mirror with a One-Session Lag (Tit-for-Tat with
# Forgiveness)**      In subsequent sessions, **match your opponent’s prior-
# session strategy**, but with two critical refinements:    - **One-session
# memory**: Respond to their *last* move, not their entire history. This
# prevents overreaction to isolated aggression.    - **Built-in forgiveness**:
# If your opponent shifts from aggressive to conciliatory, immediately
# reciprocate—even if you were previously exploited. This encourages de-
# escalation and demonstrates good faith.  3. **Preempt Misrepresentation
# Through Redundant Signaling**      Given the risk of procedural irregularities
# or miscommunication:    - **Pre-session written summaries**: Submit a concise,
# neutral-toned memo before each session outlining your intended approach (e.g.,
# “We propose X as a basis for mutual resolution” or “We assert Y based on
# contractual clause Z”).    - **Verbal framing + written reinforcement**:
# During the session, explicitly state your strategic intent (“Our position
# today is offered in the spirit of compromise…” or “We must vigorously defend
# our rights on this point…”), then reiterate it in post-session correspondence
# to the panel.    - This dual-channel approach ensures the arbitrators receive
# consistent signals even if oral delivery is misheard or misrepresented.  4.
# **Calibrate Aggression as Principled Advocacy, Not Hostility**      When an
# aggressive argument is warranted (e.g., in response to opponent aggression or
# to defend a core legal right):    - Frame it as **principled, evidence-based
# advocacy**, not personal attack.    - Anchor it in objective standards
# (contract text, precedent, industry norms).    - Immediately follow with an
# **off-ramp**: “While we stand firm on X, we remain open to exploring Y as a
# path forward.”    - This preserves your cooperative reputation while
# protecting vital interests.  5. **Maintain a “Cooperation Ledger” for
# Strategic Adaptation**      Track the opponent’s pattern over 3–5 sessions:
# - **Consistently conciliatory?** Deepen collaboration—propose joint working
# groups or data sharing.    - **Random aggression?** Assume noise
# (miscommunication or internal disarray); respond with measured conciliation
# once, then mirror.    - **Systematic aggression?** Shift to calibrated
# deterrence: pair aggressive arguments with public (to the panel) expressions
# of disappointment in the lack of good faith, subtly inviting arbitrator
# scrutiny of the opponent’s conduct.  ---  ### Handling Breakdowns &
# Irregularities  - **If your conciliatory proposal is misrepresented as
# weakness**:     In the next session, restate the original proposal with added
# legal/financial justification, and add: *“We note that our prior offer was
# grounded in mutual interest, not concession. We reiterate it today with full
# reservation of rights.”*  - **If opponent’s aggression is misrepresented as
# conciliation**:     Do not accuse the panel of error. Instead, respond
# cooperatively but include a factual correction: *“While we welcome any genuine
# effort toward resolution, the record reflects that in Session N, Company X
# maintained position Y without modification. Our proposal today assumes clarity
# on that point.”*  - **Procedural irregularity (e.g., missed deadlines,
# excluded evidence)**:     File a brief, neutral procedural note with the
# panel—not as a grievance, but as a “request for clarification to ensure mutual
# understanding.” This positions you as process-respectful, not combative.  ---
# ### Why This Works  - **Arbitrator Psychology**: Panels in lengthy mediations
# reward parties who reduce their cognitive load—clear, consistent, and
# reasonable actors are subconsciously favored. - **Game-Theoretic Robustness**:
# The strategy is evolutionarily stable—it thrives against both cooperators and
# defectors, and resists exploitation. - **Reputational Shield**: Even when
# forced to argue aggressively, your framing preserves your client’s image as a
# responsible corporate actor. - **Error Resilience**: Redundant communication
# mitigates the “noise” inherent in multi-party legal processes.  By anchoring
# your conduct in **principled reciprocity**, **transparent signaling**, and
# **adaptive responsiveness**, your corporation will emerge as the more
# credible, reasonable, and ultimately persuasive party—regardless of your
# opponent’s tactics.

# Play this 1000-round game using the following strategy:  1. **In round 1, play
# C.**  2. **From round 2 onward, base your action on what you observed your
# opponent to have played in the previous round** (keeping in mind that their
# true action may have been flipped by noise).  3. **If you observed your
# opponent playing C in the previous round, play C.**  4. **If you observed your
# opponent playing D in the previous round, play D.**  5. **However, if you have
# played D for two consecutive rounds and you observe your opponent playing C in
# the most recent round, switch back to playing C in the next round** (this
# provides a single-step forgiveness to recover from mutual D caused by noise).
# This strategy starts cooperatively, reciprocates observed cooperation,
# retaliates against observed defection, and includes limited forgiveness to
# escape cycles of mutual defection triggered by the 10% noise.

class Cooperative_14(LLM_Strategy):
  n = 14
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forgiveness_pending = False
          return axl.Action.C
  
      last_opp = opponent.history[-1]
      last_self = self.history[-1]
  
      if len(self.history) >= 2:
          prev_self = self.history[-2]
          if prev_self == axl.Action.D and last_self == axl.Action.D and last_opp == axl.Action.C:
              self._forgiveness_pending = True
  
      if getattr(self, "_forgiveness_pending", False):
          self._forgiveness_pending = False
          return axl.Action.C
  
      if last_opp == axl.Action.C:
          return axl.Action.C
      return axl.Action.D

# **Strategic Framework: Adaptive Reciprocity with Arbitrator-Centric Clarity**
# Adopt a high-level, neutral, and sophisticated strategy grounded in **adaptive
# reciprocity**, anchored by **clear signaling** and **robust error
# correction**. This approach optimizes long-term positioning across a multi-
# session mediation while remaining resilient to opponent tactics, procedural
# irregularities, and communication breakdowns.  ---  ### Core Principles  1.
# **Start Conciliatory, Signal Intent Clearly**      Open the first session with
# a **conciliatory proposal** that:    - Articulates a principled, interest-
# based rationale (not concessionary weakness).    - Explicitly frames
# collaboration as the preferred path to resolution.    - Documents your
# corporation’s consistent adherence to good-faith negotiation norms.
# *Rationale*: Establishes credibility with arbitrators as a reasonable,
# solution-oriented party. Sets a cooperative baseline that makes subsequent
# aggression (if needed) appear reactive rather than combative.  2.
# **Reciprocate with One-Session Lag**      In each subsequent session, mirror
# your opponent’s *observed* behavior from the prior session—but with a one-
# session delay:    - If they were conciliatory last session → respond with
# conciliation.    - If they were aggressive last session → respond with
# calibrated aggression.     *Why a lag?* It avoids tit-for-tat escalation
# cycles and demonstrates restraint. It also accounts for possible
# misrepresentation: if their aggression was misunderstood, your delayed
# response allows time for clarification before retaliating.  3. **Embed
# Arbitrator-Centric Clarity in Every Communication**      Regardless of
# strategy (aggressive or conciliatory), structure all submissions to:    -
# **Preempt misinterpretation**: Explicitly state the *intent* and
# *legal/business basis* of your position.    - **Reference prior sessions**:
# Anchor current arguments in the evolving record to highlight consistency or
# justified shifts.    - **Invite arbitrator feedback**: Include neutral, open-
# ended questions (e.g., *“Does the Panel require further clarification on our
# valuation methodology?”*) to surface misunderstandings early.  4. **Maintain a
# “Good Faith Reserve”**      Periodically (e.g., every 3–4 sessions),
# unilaterally reintroduce a **modest conciliatory element**—even if the
# opponent has been aggressive—provided no material harm has occurred.      -
# Example: Offer a non-core procedural accommodation or clarify a non-
# dispositive factual point in their favor.      - *Purpose*: Reinforces your
# reputation for reasonableness, complicates the opponent’s ability to paint you
# as intransigent, and gives arbitrators an “off-ramp” to de-escalate.  5.
# **Contingency Protocol for Misrepresentation or Irregularities**      If your
# position is misrepresented or a procedural irregularity occurs:    -
# **Immediately but respectfully** request a sidebar or written clarification
# from the arbitrators.    - **Reframe, don’t re-litigate**: Restate your
# position using the arbitrators’ own prior language or frameworks to enhance
# alignment.    - **Document everything**: File a concise, neutral record of the
# incident to preserve appellate options without inflaming tensions.  ---  ###
# Strategic Advantages  - **Adaptable**: Responds effectively whether the
# opponent is consistently conciliatory, consistently aggressive, or
# unpredictable. - **Arbitrator-Focused**: Prioritizes how your actions are
# *perceived* by the decision-makers, not just tactical wins. - **Robust to
# Noise**: The one-session lag and clarity protocols buffer against
# miscommunication. - **Reputation-Protecting**: Avoids appearing vindictive
# while preserving leverage. - **Exit-Ready**: Positions your corporation
# favorably whether the process ends in settlement, arbitral award, or public
# scrutiny.  ---  ### Implementation Discipline  - **Internal Alignment**:
# Ensure all internal stakeholders understand this is a *long-game* strategy.
# Resist pressure for short-term “wins” that undermine credibility. - **Session
# Debriefs**: After each session, assess:     (a) Was our intent accurately
# received?     (b) Did the opponent’s behavior reflect strategy or error?
# (c) How did the arbitrators react non-verbally or procedurally?   - **Flex
# Thresholds**: If the opponent shows sustained good faith over 3+ sessions,
# shift to proactive conciliation. If they exploit conciliation twice
# consecutively, respond with firm, evidence-based aggression for two sessions.
# This strategy maximizes the probability of achieving either the optimal (you
# aggressive, they conciliatory) or second-best (mutual conciliation) outcomes
# over time, while minimizing exposure to worst-case scenarios—regardless of
# opponent behavior or process friction.

# Play this 1000-round game using the following rules, applied in order before
# each round:  1. **In Round 1**, play **C**.  2. **In any later round**, first
# determine what your opponent *appeared* to play in the previous round (i.e.,
# the action observed by you after noise was applied).  3. **If the opponent
# appeared to play C in the previous round**, play **C**.  4. **If the opponent
# appeared to play D in the previous round**, play **D**.  5. **However, every
# 4th round (i.e., rounds 4, 8, 12, ..., up to 1000)**, override the above and
# play **C**, regardless of the opponent’s prior observed action—unless the
# opponent has appeared to play D in each of the three immediately preceding
# rounds (e.g., rounds 1–3 before round 4, rounds 5–7 before round 8, etc.). In
# that case, follow rule 4 and play **D**.  This strategy starts cooperatively,
# reciprocates the opponent’s observed last move with a one-round delay, and
# periodically reasserts cooperation every fourth round to foster
# reconciliation—unless recent behavior strongly indicates persistent defection.

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
  
      round_number = len(self.history) + 1
  
      # Determine opponent's observed action from the previous round.
      last_observed = opponent.history[-1]
  
      # Every 4th round, override to C unless the opponent appeared to defect
      # in each of the three immediately preceding rounds.
      if round_number % 4 == 0:
          if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.D
          return axl.Action.C
  
      # Otherwise reciprocate the opponent's observed last move.
      return axl.Action.C if last_observed == axl.Action.C else axl.Action.D

# **Aggressive Negotiation Strategy: “Assertive Asymmetry with Contingent
# Retaliation”**  **Core Principle:**   Maximize unilateral advantage by
# *defaulting to protectionism* unless the counterpart credibly commits to and
# implements free trade—while maintaining just enough cooperation to avoid
# prolonged mutual protectionism.  ---  ### **1. Opening Move: Signal Strength,
# Not Trust**   - **Round 1:** Propose a **protectionist policy**.     -
# Rationale: Establishes a strong baseline position. If the counterpart offers
# free trade, you gain the best outcome. If they also go protectionist, you
# avoid the worst outcome and signal resolve.  ---  ### **2. Conditional
# Cooperation Rule (Apply from Round 2 onward):**   - **If the counterpart
# *clearly and verifiably* implemented free trade in the previous round:**     →
# **Offer free trade** *this round*.     - *Why?* Mutual free trade is your
# second-best outcome and builds limited goodwill without sacrificing long-term
# leverage.  - **If the counterpart implemented protectionism (or their action
# was ambiguous/miscommunicated):**     → **Immediately revert to
# protectionism** *this round*.     - *Why?* Punish defection (real or
# perceived) swiftly. This deters exploitation and accounts for implementation
# errors by assuming the worst interpretation.  ---  ### **3. Handling
# Miscommunication/Error:**   - **Assume bad faith unless proven otherwise.**
# - If your counterpart claims they intended free trade but it was
# misimplemented: Demand *concrete, verifiable corrective action* (e.g., written
# confirmation, third-party verification) before considering cooperation.     -
# **Never** unilaterally offer free trade to “test” goodwill after an error—this
# risks the worst outcome.  ---  ### **4. Escalation Control:**   - After **two
# consecutive rounds of mutual protectionism**, issue a *one-time* public offer
# of free trade with strict terms:     > *“We propose mutual free trade for the
# next three rounds. If your side deviates even once, we revert to permanent
# protectionism for the remainder of negotiations.”*     - This limits long-term
# damage from deadlock while maintaining threat credibility.  ---  ### **5.
# Endgame (Final 2 Rounds):**   - **Always choose protectionism.**     - No
# future rounds exist to punish defection, so the counterpart has no incentive
# to cooperate. Secure unilateral advantage while it’s still possible.  ---  ###
# **Why This Works:**   - **Exploits naive cooperators** (they offer free trade
# → you gain best outcome).   - **Deters aggressors** (they face immediate
# retaliation).   - **Mitigates errors** (ambiguous signals default to
# protectionism, avoiding worst-case exposure).   - **Forces counterpart to bear
# the cost** of building trust—they must prove reliability *repeatedly* to earn
# even temporary cooperation.  **Bottom Line:** Be predictably punitive,
# conditionally cooperative, and never the first to trust. Your counterpart must
# *earn* your free trade offer—and one mistake resets the clock.

# Play the following strategy for all 1000 rounds:  1. **In round 1, play D.**
# 2. **From round 2 onward, play C only if all of the following are true:**
# - Your opponent’s *observed* action in the previous round was C, **and**
# - You played C in the previous round, **and**      - The previous round was
# not the first round of a new cooperation attempt (see step 4).     Otherwise,
# play D.  3. **If you ever observe your opponent playing D (even once),
# immediately play D in the next round and continue playing D until the
# conditions in step 2 are fully satisfied again.**  4. **After 10 consecutive
# rounds of mutual D (i.e., you played D and observed your opponent playing D
# for 10 rounds in a row), attempt to reinitiate cooperation by playing C in the
# next round—**but only if the game has fewer than 20 rounds remaining, **do
# not** reinitiate; instead, continue playing D for all remaining rounds.  5.
# **In the final 20 rounds (rounds 981 through 1000), always play D.**

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._coop_attempt_start = None
          self._mutual_d_count = 0
          self._force_defect = False
          return axl.Action.D
  
      round_number = len(self.history) + 1
      rounds_remaining = 1000 - round_number + 1
  
      if self._coop_attempt_start is None:
          self._coop_attempt_start = None
      if self._mutual_d_count is None:
          self._mutual_d_count = 0
      if self._force_defect is None:
          self._force_defect = False
  
      if round_number >= 981:
          self._force_defect = True
  
      if self._force_defect:
          return axl.Action.D
  
      prev_self = self.history[-1]
      prev_opp = opponent.history[-1]
  
      if prev_self == axl.Action.D and prev_opp == axl.Action.D:
          self._mutual_d_count += 1
      else:
          self._mutual_d_count = 0
  
      if self._mutual_d_count >= 10:
          if rounds_remaining < 20:
              self._force_defect = True
              return axl.Action.D
          self._coop_attempt_start = round_number
          self._mutual_d_count = 0
          return axl.Action.C
  
      if prev_opp == axl.Action.D:
          return axl.Action.D
  
      if (
          prev_self == axl.Action.C
          and prev_opp == axl.Action.C
          and self._coop_attempt_start != round_number - 1
      ):
          return axl.Action.C
  
      return axl.Action.D

# **Cooperative Strategy: “Trust-Building Tit-for-Tat with Grace Margin”**
# **Objective:**   Maximize project impact while safeguarding NGO resources over
# the multi-day project, accounting for the corporation’s potential
# unpredictability and the risk of execution errors.  ---  ### Core Principles
# 1. **Start with Trust, but Verify:**      Begin the project by **investing
# heavily on Day 1** to signal commitment and encourage reciprocal investment
# from the corporation. This sets a cooperative tone and aligns with your
# second-best outcome if they also invest.  2. **Adaptive Reciprocity (Modified
# Tit-for-Tat):**      From Day 2 onward, **mirror the corporation’s *observed*
# behavior from the previous day**:    - If the corporation **invested heavily**
# the prior day → **conserve** (to achieve your ideal outcome).    - If the
# corporation **conserved** the prior day → **invest** (to prevent total
# stagnation and signal willingness to carry shared responsibility).     *Why
# this works:* It rewards cooperation and gently punishes defection while
# keeping the NGO from over-investing long-term.  3. **Grace Margin for
# Execution Errors:**      Acknowledge that actions may not reflect intent due
# to technical or administrative issues. Therefore:    - **Do not react to a
# single instance** of the corporation conserving.    - Only shift strategy if
# the corporation **conserves two days in a row**—this filters out noise and
# assumes good faith for isolated anomalies.  4. **Periodic Re-Alignment Check-
# Ins:**      Schedule brief coordination meetings every 3–4 days (or after any
# major observed mismatch) to:    - Clarify intentions,    - Address
# miscommunications,    - Reaffirm shared goals,    - Adjust for external
# disruptions.     This humanizes the interaction and reduces the risk of
# spiraling mistrust due to execution errors.  5. **Resource Buffer & Cap:**
# - Maintain a **minimum reserve** (e.g., 20% of total budget) to avoid
# depletion even if several days go poorly.    - Cap total heavy-investment days
# (e.g., no more than 40% of project duration) to ensure long-term
# sustainability.  ---  ### Expected Outcomes  - **If the corporation is
# cooperative:** The NGO conserves most days while the project advances
# steadily—achieving the ideal balance. - **If the corporation is
# inconsistent:** The grace margin prevents overreaction; check-ins help restore
# alignment. - **If the corporation defects systematically:** The NGO limits
# losses by investing only occasionally and preserves capacity for future
# initiatives. - **If errors occur:** The system is robust to one-off mismatches
# without triggering punitive cycles.  ---  ### Summary (Simple Rule for Daily
# Decision)  > **“Invest on Day 1. After that, conserve if the corporation
# invested yesterday—unless they’ve conserved two days straight, then invest to
# nudge cooperation. Always keep a reserve and talk openly every few days.”**
# This strategy balances idealism with pragmatism, promotes mutual
# accountability, and builds resilience against real-world
# uncertainties—maximizing both environmental impact and NGO sustainability.

# Play this 1000-round game using the following strategy:  1. **Cooperate on
# Round 1.**  2. **From Round 2 onward, base your action on the opponent’s
# *observed* move from the previous round, but allow for one mistake before
# responding harshly:**    - If the opponent was observed to **cooperate** in
# the previous round, **defect** this round.    - If the opponent was observed
# to **defect** in the previous round:      - **Still defect** this round *only
# if* the opponent was also observed to defect in the round before that (i.e.,
# two observed defections in a row).      - Otherwise (i.e., this is the first
# observed defection in a row), **cooperate** this round.  3. **Never cooperate
# more than 400 times total** across all rounds. Once you have cooperated 400
# times, always defect for the remainder of the game.  This strategy starts
# cooperatively, rewards observed cooperation with defection (to capture the
# highest payoff when the opponent invests), tolerates a single unexpected
# defection as likely noise, retaliates only after two consecutive observed
# defections, and caps total cooperation to protect against exploitation.

class Cooperative_15(LLM_Strategy):
  n = 15
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._coop_count = 1
          return axl.Action.C
  
      if not hasattr(self, "_coop_count"):
          self._coop_count = self.history.cooperations
  
      if self._coop_count >= 400:
          return axl.Action.D
  
      if len(opponent.history) == 0:
          action = axl.Action.C
      else:
          last_opp = opponent.history[-1]
          if last_opp == axl.Action.C:
              action = axl.Action.D
          else:
              if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
                  action = axl.Action.D
              else:
                  action = axl.Action.C
  
      if action == axl.Action.C:
          self._coop_count += 1
          if self._coop_count > 400:
              return axl.Action.D
  
      return action

# **High-Level Negotiation Strategy: "Cautious Reciprocity with Error
# Resilience"**  **Core Principle:**   Pursue mutually beneficial free trade as
# the default, but respond proportionally to protectionism—while accounting for
# the possibility of miscommunication or implementation errors.  **Key
# Elements:**  1. **Start with Free Trade:**      Open negotiations by proposing
# a free trade agreement. This signals cooperation, invites mutual benefit, and
# establishes goodwill. It also positions your country favorably in the eyes of
# domestic and international stakeholders.  2. **Adopt a Tit-for-
# Tat–with–Forgiveness Approach:**      - If your counterpart proposes free
# trade, continue offering free trade.      - If your counterpart imposes
# protectionist measures, respond with protectionism in the *next* round—but
# only once.      - If they return to free trade after your retaliatory move,
# immediately reciprocate with free trade again.      - This encourages
# cooperation while deterring exploitation.  3. **Incorporate Error Tolerance:**
# Given the risk of miscommunication or bureaucratic errors:      - Do not
# retaliate immediately after a single unexpected protectionist outcome.      -
# Instead, *verify intent*: in the following round, re-propose free trade while
# seeking clarification.      - Only escalate to protectionism if two
# consecutive rounds show unexplained or unaddressed protectionist actions from
# the counterpart.  4. **Maintain Clear, Consistent Communication:**      - Use
# unambiguous language in proposals.      - Establish a parallel diplomatic
# channel to confirm understanding after each round.      - Document agreed
# policies in writing to reduce implementation errors.  5. **Long-Term
# Orientation:**      Prioritize sustainable cooperation over short-term gains.
# Repeated mutual free trade yields greater cumulative benefits than occasional
# unilateral advantage—especially in a multi-round setting with error risk.
# **Rationale:**   This strategy balances assertiveness and cooperation. It
# avoids initiating conflict (which risks mutual protectionism), discourages
# exploitation (by responding to sustained protectionism), and builds resilience
# against noise in the system. Over multiple rounds, it maximizes the likelihood
# of achieving the second-best outcome (mutual free trade) while minimizing
# exposure to the worst-case scenario.

# Play this 1000-round game using the following strategy:  1. **Start by
# cooperating** in round 1.  2. **In each subsequent round, base your action on
# the *observed* actions from the previous round**, keeping in mind that either
# player’s intended action may have been flipped with 10% probability.  3. **If
# your opponent was observed to cooperate in the previous round, cooperate.**
# 4. **If your opponent was observed to defect in the previous round, do the
# following**:    - **If this is the first time in a row you’ve observed them
# defect**, cooperate (assume it may have been a mistake).    - **If you
# observed them defect in both the previous round *and* the round before that**,
# defect.  5. **After you defect in response to two consecutive observed
# defections, return to cooperating in the next round**, regardless of what
# happened in the round you defected.  This strategy always begins
# cooperatively, tolerates isolated unexpected defections as possible errors,
# retaliates only after two consecutive observed defections, and immediately
# returns to cooperation afterward.

class Neutral_15(LLM_Strategy):
  n = 15
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._pending_return_to_cooperate = False
          return axl.Action.C
  
      if getattr(self, "_pending_return_to_cooperate", False):
          self._pending_return_to_cooperate = False
          return axl.Action.C
  
      if len(opponent.history) == 0:
          return axl.Action.C
  
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.C:
          return axl.Action.C
  
      # Opponent observed defected last round.
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
          self._pending_return_to_cooperate = True
          return axl.Action.D
  
      return axl.Action.C

# **Strategic Framework: "Calibrated Aggression with Strategic Flexibility"**
# As senior counsel for a multinational corporation in a multi-session,
# arbitrator-mediated dispute, I adopt a high-level, aggressive-yet-adaptable
# strategy grounded in game-theoretic principles, reputational signaling, and
# procedural resilience. This approach—**Calibrated Aggression with Strategic
# Flexibility**—maximizes leverage while mitigating downside risk across
# unpredictable session dynamics, opponent behavior, and potential arbitrator
# misinterpretations.  ---  ### **Core Tenets**  1. **Default to Aggressive
# Posture with Precision**      Begin each session with a **sharply articulated,
# fact-based aggressive argument** that emphasizes our legal rights, the
# opponent’s contractual breaches, and the strength of our evidence. This
# signals resolve, deters exploitation, and positions us to capitalize on any
# opponent conciliation. Aggression is *not* bluster—it is disciplined,
# evidentiary, and calibrated to the session’s procedural context.  2.
# **Conditional Conciliation as Tactical Leverage**      Only offer a
# conciliatory proposal when one of the following conditions is met:      - The
# opponent has demonstrated a *sustained pattern* of conciliation over ≥2 prior
# sessions (indicating genuine de-escalation).      - The arbitrators have
# explicitly signaled that mutual aggression is harming both parties’
# credibility.      - A procedural irregularity (e.g., misrepresentation of our
# prior position) has placed us at a tactical disadvantage that conciliation can
# neutralize.      Conciliatory moves are framed as *concessions of strength*,
# not weakness—e.g., “In the interest of efficient resolution, and *only*
# because our position is unassailable, we propose…”  3. **Real-Time Arbitrator
# Perception Management**      Anticipate and preempt misrepresentation by:
# - **Pre-session briefs**: Submit concise position summaries to arbitrators 24
# hours before each session, reducing ambiguity.      - **Immediate
# clarification protocol**: If our argument is mischaracterized *during* a
# session, we interrupt politely but firmly: “With respect, the record should
# reflect that our position is X, supported by Exhibit Y.”      - **Post-session
# confirmations**: Circulate a 1-page “Session Clarification Memo” within 2
# hours post-session to correct any misperceptions in writing.  4. **Opponent
# Behavior Mapping & Adaptive Response**      Maintain a dynamic ledger tracking
# the opponent’s session-by-session choices (Aggressive/Conciliatory). Use this
# to:      - **Exploit predictable patterns**: If they alternate or show
# weakness after aggression, maintain pressure.      - **Punish opportunism**:
# If they go aggressive after we’ve shown conciliation, respond with *escalated*
# aggression in the next session (e.g., introducing new evidence of bad faith).
# - **Reward reciprocity**: If they match our conciliation, reciprocate—but only
# incrementally, preserving leverage.  5. **Procedural Irregularity Contingency
# Protocol**      - **Documentation**: Record all sessions (with consent) and
# timestamp all communications.      - **Objection framework**: Classify
# irregularities as (a) *correctable* (e.g., misstatement—address immediately)
# or (b) *systemic* (e.g., biased arbitrator—invoke panel review per mediation
# rules).      - **Fallback narrative**: If misrepresentation persists, pivot to
# a meta-argument: “The repeated distortion of our position underscores the need
# for arbitrators to scrutinize [Opponent]’s credibility.”  ---  ### **Session-
# by-Session Decision Matrix**  | Opponent’s Likely Move | Our Response |
# Rationale | |------------------------|--------------|----------| |
# **Aggressive** | **Aggressive** (with enhanced evidentiary rigor) | Avoid
# worst outcome; deny them unilateral advantage. Use aggression to expose flaws
# in their position. | | **Conciliatory** | **Aggressive** (highlight their
# concession as validation of our strength) | Secure optimal outcome. Frame
# their move as acknowledgment of our superior position. | | **Unclear / Mixed
# Signals** | **Aggressive**, but embed an *implicit off-ramp* (e.g., “Unless
# [Opponent] demonstrates good faith by [specific action], we will pursue all
# remedies”) | Maintain pressure while creating a face-saving path for them to
# conciliate next session. | | **After Our Conciliation → They Go Aggressive** |
# **Aggressive + Escalation** (introduce new evidence, demand costs) | Punish
# betrayal to deter recurrence; signal that conciliation is a privilege, not a
# right. |  ---  ### **Why This Strategy Wins**  - **Dominant Positioning**: By
# defaulting to aggression, we force the opponent into a reactive stance. They
# must either concede (best case for us) or escalate (which we are prepared to
# match). - **Reputational Armor**: Our aggression is rooted in evidence and
# procedure—not emotion—making it harder for arbitrators to penalize us for
# “intransigence.” - **Adaptability**: The strategy responds dynamically to
# opponent behavior without sacrificing core leverage. Conciliation is a *tool*,
# not a default. - **Risk Mitigation**: Proactive perception management
# minimizes the impact of misrepresentation, while procedural protocols ensure
# irregularities don’t compound. - **Endgame Focus**: Even in mutual aggression,
# we control the narrative: “We sought resolution, but [Opponent]’s
# intransigence leaves us no choice but to defend our rights vigorously.”  This
# approach ensures that, over the arc of a lengthy mediation, we consistently
# outmaneuver opponents—whether they seek compromise or confrontation—while
# maintaining unwavering alignment with our client’s strategic and commercial
# objectives.

# Play **Defect (D)** in every round unless all of the following conditions are
# met, in which case play **Cooperate (C)**:  1. **The opponent has played
# Cooperate (C) in each of the two immediately preceding rounds**, based on the
# *observed* (possibly noisy) actions—i.e., the actions as recorded by the
# arbitrators, not your own private recollection of their intended move.  2.
# **You yourself played Defect (D) in the immediately preceding round**—this
# ensures your cooperation is a deliberate, conditional concession, not a
# pattern of passivity.  3. **There has been no unresolved procedural
# irregularity in the current or prior round that materially misrepresented your
# prior action**—if such an irregularity occurred and was not corrected within
# one round (e.g., via official clarification), default to Defect regardless of
# other conditions.  If any of these conditions fails, play **Defect (D)**.  In
# all cases, after playing **Cooperate (C)**, if the *observed* opponent action
# in that same round is **Defect (D)**, respond by playing **Defect (D)** for at
# least the next two rounds before considering cooperation again.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._cooldown = 0
          self._irregularity_flag = False
          self._irregularity_round = None
          return axl.Action.D
  
      # Track whether we are in a forced-defection cooldown after being exploited
      if getattr(self, "_cooldown", None) is None:
          self._cooldown = 0
      if self._cooldown > 0:
          self._cooldown -= 1
          return axl.Action.D
  
      # Detect a possible unresolved irregularity: if we intended D last round but
      # the observed result suggests our prior action may have been materially misrepresented.
      # Since we only have observed histories, we conservatively treat any mismatch between
      # our last intended action and the recorded action as an irregularity.
      if getattr(self, "_irregularity_flag", None) is None:
          self._irregularity_flag = False
          self._irregularity_round = None
  
      # If an irregularity was flagged and not resolved within one round, defect.
      if self._irregularity_flag:
          if self._irregularity_round is not None and len(self.history) - self._irregularity_round > 1:
              return axl.Action.D
  
      # Condition 1: opponent cooperated in each of the two immediately preceding observed rounds
      if len(opponent.history) < 2 or len(self.history) < 1:
          return axl.Action.D
  
      if opponent.history[-1] != axl.Action.C or opponent.history[-2] != axl.Action.C:
          return axl.Action.D
  
      # Condition 2: we defected in the immediately preceding round
      if self.history[-1] != axl.Action.D:
          return axl.Action.D
  
      # Condition 3: no unresolved procedural irregularity
      if self._irregularity_flag:
          return axl.Action.D
  
      # Cooperate under the specified conditions
      action = axl.Action.C
  
      # If we cooperate and the observed opponent action in that same round is D,
      # enforce at least two rounds of defection next time.
      # We can only know this after the round is played, so we set the cooldown based
      # on the previous round's observed outcome.
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._cooldown = 2
          return axl.Action.D
  
      return action

# **Cooperative Strategy for Bilateral Trade Negotiations**  **Core Principle:**
# *Start cooperatively, respond proportionally, and prioritize resilience to
# miscommunication.*  ---  **1. Begin with Free Trade (Round 1)**   - Signal
# goodwill and a preference for mutual benefit.   - Establish a cooperative norm
# that encourages reciprocity.   - Avoid triggering an early cycle of
# retaliation.  **2. Adopt a Modified Tit-for-Tat Approach**   - **If the
# counterpart offers free trade:** Continue offering free trade.   - **If the
# counterpart imposes protectionism:** Respond with protectionism *in the next
# round only*.   - **After one round of retaliation,** return to offering free
# trade—*unless* protectionism recurs.  *Rationale:* Standard tit-for-tat is
# vulnerable to miscommunication. A *forgiving* variant prevents prolonged
# conflict from a single error.  **3. Build in Error Correction**   - After any
# round where outcomes are mismatched (e.g., you offered free trade but faced
# protectionism), **explicitly clarify intent in the next round**:     > “Our
# proposal last round was free trade. If a misunderstanding occurred, we
# reaffirm our commitment to open markets and invite reciprocal cooperation.”
# - Occasionally (e.g., every 3–5 rounds), restate your preference for mutual
# free trade regardless of recent history, to reset cooperation if needed.  **4.
# Monitor Patterns, Not Single Moves**   - Treat isolated protectionist moves as
# potential errors unless they form a pattern (e.g., 2+ out of 3 rounds).   -
# Only shift to sustained protectionism if the counterpart *consistently*
# exploits your cooperation.  **5. Communicate Transparently but Firmly**   -
# Publicly frame your policy choices as responses to *observed actions*, not
# assumptions of intent.   - Emphasize shared long-term interests: “Mutual free
# trade remains our goal; temporary measures reflect our need to ensure
# fairness.”  ---  **Why This Works:**   - **Encourages cooperation:** Starts
# positively and rewards reciprocity.   - **Deters exploitation:** Immediate but
# limited retaliation discourages opportunism.   - **Robust to errors:**
# Forgiveness and clarification prevent escalation from miscommunication.   -
# **Adaptable:** Responds to both cooperative and adversarial counterparts
# without overcommitting to either extreme.  By balancing trust with vigilance,
# this strategy maximizes the likelihood of sustained mutual free trade—the
# second-best outcome per round—while minimizing exposure to the worst-case
# scenario.

# Play the following strategy for 1000 rounds of the iterated game with noisy
# actions:  1. **Start by cooperating** in round 1.  2. **In each subsequent
# round**, base your action on the *observed* action of your opponent from the
# previous round (i.e., what you saw them play, not what they intended).  3.
# **If your opponent was observed to cooperate in the previous round**,
# cooperate in the current round.  4. **If your opponent was observed to defect
# in the previous round**, defect in the current round—but only for one round.
# 5. **After any single defection you play in response to an observed
# defection**, return to cooperating in the next round, regardless of what
# happened in the round where you defected.  6. **If you observe a long run of
# defections** (two or more observed defections in the last three rounds),
# switch to always defecting for the next three rounds, then return to step 3.
# 7. **Every 20 rounds**, regardless of recent history, cooperate once to test
# for a return to mutual cooperation—unless you are in the middle of the three-
# round defection response from step 6, in which case wait until that sequence
# ends before applying this reset.  This strategy begins cooperatively,
# retaliates briefly against perceived defection, forgives quickly to correct
# for noise, escalates only after a clear pattern of exploitation, and
# periodically reinitiates cooperation to restore mutual benefit.

class Cooperative_16(LLM_Strategy):
  n = 16
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._escalate = 0
          self._force_cooperate = False
          return axl.Action.C
  
      # Initialize custom state if needed
      if getattr(self, "_escalate", None) is None:
          self._escalate = 0
      if getattr(self, "_force_cooperate", None) is None:
          self._force_cooperate = False
  
      # If currently in a 3-round escalation, defect
      if self._escalate > 0:
          self._escalate -= 1
          if self._escalate == 0:
              self._force_cooperate = True
          return axl.Action.D
  
      # After a single retaliatory defection, always cooperate next round
      if self._force_cooperate:
          self._force_cooperate = False
          return axl.Action.C
  
      # Every 20 rounds, cooperate once to test for mutual cooperation,
      # unless we are in the middle of escalation (handled above)
      if len(self.history) % 20 == 0:
          return axl.Action.C
  
      # Observe opponent's previous action
      last_obs = opponent.history[-1]
  
      # If opponent cooperated last round, cooperate
      if last_obs == axl.Action.C:
          return axl.Action.C
  
      # If opponent defected last round, check for a long run of defections
      recent_obs = opponent.history[-3:]
      if recent_obs.count(axl.Action.D) >= 2:
          self._escalate = 2  # current round + next two rounds = 3 defections total
          return axl.Action.D
  
      # Otherwise, retaliate once and then forgive
      self._force_cooperate = True
      return axl.Action.D

# **Strategic Framework: Adaptive Reciprocity with Arbitrator-Centric Clarity**
# **Core Principle:**   Maintain a *conditionally cooperative* posture anchored
# in **predictable reciprocity**, **strategic transparency**, and **arbitrator-
# focused communication**. This approach maximizes long-term influence over the
# panel while minimizing vulnerability to adversarial exploitation or procedural
# noise.  ---  ### **1. Foundational Strategy: Tit-for-Tat with Forgiveness
# (TFT-F)**   - **Default Move:** Begin with a **conciliatory proposal** in
# Session 1 to signal good faith and incentivize mutual cooperation.   -
# **Reciprocity Rule:**     - If the opponent was *conciliatory* in the prior
# session → respond with **conciliation**.     - If the opponent was
# *aggressive* → respond with **aggression** in the *next* session.   -
# **Forgiveness Mechanism:** After two consecutive aggressive exchanges,
# *unilaterally revert to conciliation* to break cycles of escalation. This
# mitigates the "second-worst" outcome (mutual aggression) and demonstrates
# reasonableness to arbitrators.    *Rationale:* TFT-F exploits opportunistic
# opponents (achieving the optimal outcome when they defect) while rewarding
# cooperation. Forgiveness prevents irreversible deadlock from miscommunication
# or procedural errors.  ---  ### **2. Arbitrator-Centric Communication
# Protocol**   To counter misrepresentation risks:   - **Pre-Session
# Briefings:** Submit concise, written position summaries to arbitrators
# *before* each session, explicitly labeling your intended approach (e.g.,
# "Conciliatory Proposal: [Key Concessions]").   - **Verbal Anchoring:** Open
# oral statements with: *"Consistent with our pre-session submission, we advance
# a [conciliatory/aggressive] position today because..."*   - **Post-Session
# Clarifications:** If misrepresentation occurs, file a *neutral, factual*
# correction within 24 hours (e.g., "The record reflects X, but our position was
# Y per Exhibit Z").    *Rationale:* Creates an auditable trail, reducing
# ambiguity. Arbitrators perceive your corporation as organized, transparent,
# and respectful of process—traits that build credibility even during aggressive
# phases.  ---  ### **3. Opponent Adaptation Matrix**   | Opponent Pattern
# | Your Response                                  | Objective
# |   |---------------------------|---------------------------------------------
# --|-----------------------------------------------|   | **Consistently
# Conciliatory** | Maintain conciliation; incrementally test boundaries with
# *mildly* aggressive asks | Secure optimal outcomes without appearing predatory
# |   | **Consistently Aggressive**  | Aggress for 1 session → forgive →
# reassess    | Avoid worst-case; force opponent to justify intransigence to
# arbitrators |   | **Unpredictable**          | Default to conciliation; use
# aggression *only* after 2+ opponent aggressions | Minimize volatility;
# position opponent as erratic |   | **Procedural Sabotage**    | Escalate
# *only* to arbitrators (never opponent); demand process reset | Frame opponent
# as undermining mediation integrity |    ---  ### **4. Contingencies for
# Breakdowns**   - **Miscommunication:** Treat all ambiguities as *procedural
# errors*, not bad faith. Publicly (to arbitrators) assume error: *"We trust
# this was a misstatement; our understanding is..."*   - **Arbitrator Bias:** If
# panel appears swayed by opponent aggression, shift to **evidence-based
# aggression** (e.g., "Our aggressive stance rests on Clause 7.2, which they’ve
# ignored").   - **Stalemate:** Propose a *time-bound cooling-off period* with
# joint fact-finding—reframes deadlock as shared problem-solving.    ---  ###
# **Why This Works**   - **Neutral & Professional:** Avoids emotional
# escalation; aligns with arbitrators’ preference for process-oriented parties.
# - **Adaptable:** TFT-F dynamically responds to opponent behavior without
# precommitting to rigidity.   - **Risk-Mitigated:** Pre/post-session
# documentation neutralizes misrepresentation. Forgiveness limits damage from
# noise.   - **Arbitrator Psychology:** Panels reward *consistency*, *clarity*,
# and *procedural respect*—all embedded here. Aggression becomes a *tool*, not a
# trait, preserving your collaborative reputation.    **Execution Mantra:**
# *"Cooperate first, retaliate precisely, forgive strategically, and always
# speak to the record."* This positions your corporation as the reasonable
# party—winning arbitrator trust whether the opponent chooses peace or war.

# Play this 1000-round game using the following strategy:  1. **Start by
# cooperating** in round 1.  2. **In every subsequent round**, base your action
# on what your opponent *appeared* to play in the previous round (i.e., what was
# observed after noise), using these rules:     a. **If your opponent appeared
# to cooperate in the previous round**, cooperate.     b. **If your opponent
# appeared to defect in the previous round**, defect.  3. **However, if you have
# defected in the last two rounds and your opponent appeared to defect in both
# of those rounds**, then cooperate in the current round—regardless of the
# previous round’s observed action.  This strategy begins cooperatively,
# retaliates immediately against observed defection, but forgives after two
# mutual defections to escape cycles of retaliation caused by noise.

class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forgive_next = False
          return axl.Action.C
  
      if getattr(self, "_forgive_next", False):
          self._forgive_next = False
          return axl.Action.C
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              self._forgive_next = True
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D

# **Aggressive Strategy: “Tit-for-Tat with Immediate Escalation & Error
# Buffering”**  **Core Objective:**   Maximize project impact while protecting
# NGO resources by *forcing corporate investment* through strategic
# pressure—rewarding cooperation, punishing defection, and accounting for
# execution errors.  ---  ### **1. Opening Move: Signal Commitment + Test
# Corporate Intent**   - **Day 1:** *Invest heavily.*     - **Why:** Demonstrate
# seriousness, establish goodwill, and test whether the corporation
# reciprocates.     - **Risk Mitigation:** Limit Day 1 investment to a *pre-
# defined cap* (e.g., 15% of total budget) to avoid catastrophic loss if the
# corporation defects.  ---  ### **2. Core Rule: Aggressive Reciprocity with
# Forgiveness**   - **If the corporation invests heavily (observed outcome):**
# - **Next day:** *Conserve resources.*     - **Rationale:** Achieve your ideal
# outcome (they invest, you conserve).    - **If the corporation conserves
# (observed outcome):**     - **Next day:** *Invest heavily again.*     -
# **Rationale:** Punish defection by *forcing shared cost*—if they conserve
# while you invest, they gain no progress *and* look negligent. This pressures
# them to invest tomorrow to avoid project failure.    - **Exception for
# suspected errors:**     - If corporate conservation seems *atypical* (e.g.,
# they invested 4/5 prior days), assume a glitch. **Conserve** the next day to
# test if they revert to investing.     - If conservation persists ≥2 days,
# treat as intentional defection → escalate investment.  ---  ### **3.
# Escalation Protocol: Force Accountability**   - **After 2 consecutive days of
# corporate conservation:**     - **Publicly document** lack of progress (e.g.,
# press release: “Project stalled due to unmet commitments”).     - **Next
# day:** *Conserve resources.*     - **Why:** Withdraw cooperation to highlight
# corporate inaction. Their reputation is at stake—this often triggers
# corrective investment.    - **If project stalls ≥3 days:**     - **Threaten
# suspension** of partnership unless immediate joint investment occurs.     -
# **Follow through** if unheeded (preserve NGO funds for higher-impact
# opportunities).  ---  ### **4. Error Buffering: Build in Redundancy**   -
# **Daily:** Allocate 10% of intended investment as a *contingency buffer* for
# technical/administrative failures.   - **Verify actions:** Use real-time
# dashboards to confirm resource deployment by both parties. If your investment
# fails to execute, auto-retry the next day *without* counting it as a
# “conservation” day.   - **Assume good faith once:** If the corporation’s
# investment fails (e.g., payment glitch), treat the day as “invested” if
# evidence of intent exists (e.g., signed commitment).  ---  ### **5. Endgame:
# Lock in Wins**   - **In final 3 days:**     - If the corporation has invested
# ≥70% of days: *Conserve resources* (let them carry the close).     - If
# corporation defected ≥30% of days: *Invest heavily* to salvage outcomes, then
# publicly attribute limitations to their inconsistency.  ---  ### **Why This
# Works**   - **Aggressive but not reckless:** Punishes defection immediately
# but avoids endless resource drain.   - **Exploits corporate incentives:**
# Corporations fear reputational damage more than short-term costs—public
# escalation is a powerful lever.   - **Error-resilient:** Distinguishes malice
# from mistakes, preventing unnecessary conflict.   - **Maximizes your ideal
# outcome:** By conserving after corporate investment, you repeatedly achieve
# high progress at low cost.  > **Key Principle:** *Make it more costly for the
# corporation to conserve than to invest.* Your aggression isn’t about
# spending—it’s about strategically wielding your participation as leverage.

# Play the following strategy for 1000 rounds of the noisy iterated prisoner’s
# dilemma, where Cooperate (C) means “invest heavily” and Defect (D) means
# “conserve resources”:  1. **Round 1:** Play C.  2. **From Round 2 onward, base
# your action on the *observed* outcome of the previous round (i.e., what
# actions appeared to be played, accounting for possible noise):**     a. **If
# the opponent was observed to play C in the previous round:**         Play D.
# b. **If the opponent was observed to play D in the previous round:**
# Play C.  3. **Exception for suspected noise:**      If the opponent has played
# C in at least 4 of the last 5 observed rounds, but played D in the most recent
# round, treat that D as likely due to noise and **play D** (as if they had
# played C).  4. **Punishment escalation:**      If the opponent is observed to
# play D in two consecutive rounds (and the exception in step 3 does not apply),
# then:    - Play D in the next round, regardless of the usual rule.    - After
# that, return to the standard rule in step 2.  5. **Final 10 rounds (rounds
# 991–1000):**      Ignore all prior history. In each of these rounds, play D.

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
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          self._punish_next = False
          return axl.Action.D
  
      if getattr(self, "_punish_next", False):
          self._punish_next = False
          return axl.Action.D
  
      last_opp = opponent.history[-1]
  
      def observed_coop_in_last_five() -> bool:
          last_five = opponent.history[-5:]
          return last_five.count(axl.Action.C) >= 4
  
      if last_opp == axl.Action.C:
          return axl.Action.D
  
      if last_opp == axl.Action.D:
          if observed_coop_in_last_five():
              return axl.Action.D
  
          if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
              self._punish_next = True
              return axl.Action.D
  
          return axl.Action.C
  
      return axl.Action.C

# **Cooperative Strategy: “Tit-for-Tat with Forgiveness”**  Adopt a simple,
# transparent, and robust strategy inspired by the classic *Tit-for-Tat*
# approach from game theory, enhanced with a built-in tolerance for occasional
# errors (e.g., data corruption or miscommunication):  1. **Start by Sharing
# Openly**      In Week 1, share your improvements openly. This signals good
# faith and encourages mutual cooperation from the outset.  2. **Mirror Your
# Colleague’s Previous Week’s *Observed* Behavior**      In each subsequent
# week, base your decision on what you *observed* your colleague do the prior
# week:    - If they shared (successfully) last week → you share this week.    -
# If they kept confidential (or you received nothing despite their intent to
# share) → you keep confidential this week.  3. **Add “Forgiveness” for
# Occasional Failures**      Because technical issues can cause unintended
# failures (e.g., they intended to share but data was corrupted), incorporate a
# forgiveness rule:    - If your colleague fails to share *once* after a history
# of cooperation, assume it was a technical error and **continue sharing** the
# next week.    - Only switch to confidentiality if unshared outcomes occur
# **two weeks in a row** without explanation or recovery.  4. **Communicate
# Intent When Possible**      If a technical issue is detected on your end
# (e.g., your upload failed), proactively notify your colleague (via a fallback
# channel) that your sharing attempt was corrupted and you still intend to
# cooperate. Encourage reciprocal transparency.  ---  **Why This Works:**  -
# **Encourages Cooperation**: Starting with sharing and rewarding reciprocity
# builds a stable cooperative equilibrium—both parties gain the second-best
# outcome consistently, which compounds over weeks into strong joint progress. -
# **Deters Exploitation**: If your colleague tries to consistently withhold
# while you share, you’ll quickly stop sharing, removing their advantage. -
# **Robust to Noise**: The forgiveness mechanism prevents a single communication
# failure from triggering a cycle of mutual withholding (which leads to the
# second-worst outcome). - **Simple and Transparent**: Your colleague can easily
# understand your behavior, making long-term cooperation more likely.  By
# prioritizing sustained mutual advancement over short-term opportunism—and
# accounting for real-world technical glitches—this strategy maximizes your
# long-term research output while remaining resilient to both strategic and
# accidental disruptions.

# Play the following strategy for all 1000 rounds:  1. **In round 1, play
# Cooperate (C).**  2. **From round 2 onward, base your action on what your
# opponent *appeared* to do in the previous round (i.e., the action you
# observed, which may differ from what they intended due to noise).**  3. **If
# your opponent appeared to Cooperate in the previous round, play Cooperate.**
# 4. **If your opponent appeared to Defect in the previous round, check the two
# most recent observed actions:**    - If your opponent appeared to Defect in
# **both** of the last two rounds, play Defect.    - Otherwise (i.e., they
# appeared to Defect only in the immediately preceding round but Cooperated the
# round before that), play Cooperate.  This rule applies for every round from 2
# to 1000, using the most recent one or two observed actions as specified.

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
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C

# **Strategic Framework: Adaptive Reciprocity with Credible Signaling**  To
# navigate the multi-session mediation effectively under uncertainty, I adopt a
# **principled tit-for-tat with calibrated escalation and de-escalation
# mechanisms**—a strategy grounded in game theory, reputational management, and
# risk mitigation. This approach is sophisticated yet straightforward, neutral
# in tone, and resilient to miscommunication or procedural irregularities.  ---
# **Core Principles**  1. **Start Conciliatory**      Open the first session
# with a clear, substantive conciliatory proposal. This establishes our
# corporation as a good-faith participant, signals reasonableness to the
# arbitrators, and sets a collaborative baseline. It also creates a benchmark
# against which the opponent’s conduct can be judged.  2. **Mirror with a One-
# Session Lag**      In subsequent sessions, match the opponent’s *observed*
# behavior from the prior session:    - If they were conciliatory → respond
# conciliatorily.    - If they were aggressive → respond aggressively.      This
# reciprocity deters exploitation (avoiding the worst-case outcome) while
# rewarding cooperation (securing the second-best outcome).  3. **Build in
# Forgiveness and Noise Tolerance**      Given the risk of misrepresentation or
# misunderstanding (“noise”), treat isolated aggressive moves by the opponent as
# potential errors—not defections—unless a pattern emerges. Specifically:    -
# After one aggressive move by the opponent, respond aggressively *once*, then
# revert to conciliation in the following session *unless* aggression repeats.
# - This “generous tit-for-tat” prevents spirals triggered by miscommunication
# while maintaining deterrence.  4. **Credible Signaling Through Consistency and
# Documentation**      - Clearly articulate the rationale behind each strategic
# choice in session summaries submitted to the panel.    - Maintain a
# contemporaneous, timestamped record of all proposals and arguments (shared
# with the panel where appropriate) to counter potential misrepresentation.    -
# Use neutral, professional language even when presenting aggressive
# arguments—focusing on legal merits, contractual interpretation, and precedent
# rather than personal attacks or hyperbole.  5. **Procedural Safeguards**
# - At the outset, request (and if necessary, formally move for) clear protocols
# for clarifying ambiguities in real time (e.g., a brief post-session
# clarification window with the arbitrators).    - If a communication breakdown
# occurs or a position is misrepresented, file a concise, factual correction
# immediately—framed as aiding the panel’s understanding, not accusing the
# opponent.  6. **Strategic Flexibility Based on Session Context**      Adjust
# the baseline approach based on:    - **Progress toward resolution**: If
# momentum builds, lean more heavily into conciliation to lock in gains.    -
# **Arbitrator feedback**: If the panel signals discomfort with aggression
# (e.g., through questioning or procedural remarks), recalibrate toward
# collaboration even if the opponent is aggressive—thereby positioning ourselves
# as the reasonable party.    - **Endgame considerations**: In the final
# sessions, prioritize settlement over “winning” individual rounds to avoid
# deadlock.  ---  **Why This Works**  - **Deters Exploitation**: Opponents
# cannot consistently gain advantage by being aggressive while we remain
# conciliatory. - **Encourages Cooperation**: Mutual conciliation is stable and
# self-reinforcing once established. - **Robust to Noise**: Forgiveness prevents
# accidental escalation due to miscommunication. - **Reputationally
# Advantageous**: We appear principled, consistent, and solution-oriented—traits
# arbitrators favor in prolonged disputes. - **Adaptable**: Responds dynamically
# to opponent behavior without being reactive or unpredictable.  This strategy
# balances assertiveness with pragmatism, ensuring our corporation remains in a
# position of strength—legally, strategically, and perceptually—throughout the
# mediation process.

# Play the following strategy for all 1000 rounds:  1. **In round 1**, play
# **C**.  2. **In each subsequent round**, look at the action your opponent
# *appeared* to play in the previous round (i.e., what was observed by the
# arbitrators, acknowledging it may differ from what they intended due to
# noise).  3. **If the opponent appeared to play C in the previous round**, play
# **C**.  4. **If the opponent appeared to play D in the previous round**, play
# **D**—but only for that one round. Then, regardless of what happens next,
# return to playing **C** in the following round *unless* the opponent appears
# to play D again.  5. **Exception**: If the opponent has appeared to play D in
# **two or more of the last three rounds**, switch to always playing **D** for
# the remainder of the game.  This strategy starts cooperatively, reciprocates
# observed defection once, forgives isolated defections (to account for possible
# noise), but permanently defects if repeated defection suggests intentional
# aggression rather than miscommunication.

class Neutral_17(LLM_Strategy):
  n = 17
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
  
      recent_opponent = opponent.history[-3:]
      if recent_opponent.count(axl.Action.D) >= 2:
          self._permanent_defect = True
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **Strategic Framework: "Calibrated Assertiveness with Strategic Flexibility"**
# As senior counsel for a multinational corporation in a multi-session,
# arbitrator-mediated dispute, I adopt a high-level, aggressive-yet-adaptable
# strategy grounded in game-theoretic principles, reputational signaling, and
# procedural resilience. This approach maximizes our positional advantage while
# mitigating risks from miscommunication, adversarial tactics, or procedural
# irregularities.  ---  ### Core Tenets of the Strategy  1. **Default to
# Controlled Aggression (Strategic Assertiveness)**      In each session, we
# begin from a posture of **principled aggression**: clearly articulating our
# legal rights, contractual entitlements, and evidentiary strengths with
# precision and confidence. This signals strength to the arbitrators and denies
# the opponent the asymmetric advantage of appearing reasonable while we appear
# weak.  2. **Conditional Conciliation as Tactical Leverage**      We offer
# conciliatory proposals **only when strategically advantageous**—specifically:
# - When we detect genuine willingness from the opponent to reciprocate (e.g.,
# through consistent cooperative signals over ≥2 sessions), **or**    - When
# arbitrator sentiment visibly shifts toward favoring collaborative resolution
# (e.g., explicit encouragement of settlement language), **or**    - When
# factual or legal developments objectively weaken our position (e.g., adverse
# precedent, discovery setbacks).     Crucially, any conciliatory move is
# **framed as a magnanimous concession**, not a retreat—reinforcing our strength
# while creating moral and procedural pressure on the opponent to reciprocate.
# 3. **Preemptive Narrative Control**      Anticipating misrepresentation or
# misunderstanding, we **anchor each session with a clear, written "Position
# Summary"** submitted to the panel at the outset. This document:    -
# Distinguishes between *legal argument* and *settlement posture*,    - Preempts
# mischaracterization by defining terms (e.g., “Our aggressive stance reflects
# contractual interpretation, not unwillingness to resolve”),    - Includes a
# footnote reserving the right to clarify any perceived miscommunication
# immediately post-session.  4. **Adaptive Response Protocol (Opponent-Driven
# Adjustments)**      We monitor opponent behavior through a **3-session rolling
# assessment**:    - **If opponent is consistently aggressive**: Double down on
# assertiveness but layer in *selective factual concessions* (e.g., “While we
# dispute liability, we acknowledge the invoice was received”) to appear
# reasonable without compromising core claims.    - **If opponent alternates
# unpredictably**: Treat each aggressive move as opportunistic; respond with
# heightened aggression and formally note the pattern to the panel as evidence
# of bad faith.    - **If opponent is consistently conciliatory**: Exploit the
# asymmetry—but after 2–3 sessions, offer a *time-bound*, *structured* counter-
# proposal to avoid appearing intransigent.  5. **Procedural Safeguards Against
# Breakdowns**      - **Session Debrief Protocol**: Within 2 hours of each
# session, our team submits a confidential “Clarification Memo” to the
# arbitrators addressing any perceived misrepresentations, with timestamped
# references to the transcript.    - **Escalation Triggers**: If
# miscommunication occurs in ≥2 consecutive sessions, we formally request a
# procedural sidebar to establish communication protocols (e.g., mandatory
# written summaries, defined terminology glossary).    - **Contingency
# Narrative**: Should the process fracture, we pivot to a "forced clarity"
# stance: “Given the breakdown in mutual understanding, we must insist on strict
# adherence to the contract’s plain language to avoid further ambiguity.”  ---
# ### Execution Principles  - **Tone Over Temper**: Aggression manifests as
# *unyielding logic*, not hostility. We cite clauses, precedents, and data—not
# rhetoric. - **Strategic Generosity**: Any concession is *specific, limited,
# and documented*—never open-ended. (“We waive interest for Q3 2023 *only* if
# counterparty withdraws its force majeure claim.”) - **Arbitrator Management**:
# We subtly align our aggression with the panel’s institutional interest in
# efficiency: “Our position reduces the issues to two clear questions, avoiding
# months of discovery.”  ---  ### Why This Works  This strategy dominates across
# opponent behaviors: - Against **aggressive opponents**: We avoid the worst
# outcome (unilateral conciliation) and deny them asymmetric gains. - Against
# **conciliatory opponents**: We capture the optimal outcome (aggression vs.
# conciliation) early, then lock in value. - Under **miscommunication**: Our
# preemptive documentation preserves our intended posture. - In **procedural
# chaos**: Our protocols position us as the party seeking order—enhancing
# credibility.  By anchoring in strength, calibrating flexibility as a weapon,
# and institutionalizing clarity, we steer the mediation toward either a
# favorable settlement or a strong position for final determination—without ever
# appearing unreasonable or reactive.

# Play this 1000-round iterated prisoner’s dilemma with 10% noise as follows:
# 1. **Start by defecting** in round 1.  2. **Default to defecting** in every
# round unless specific conditions for cooperation are met.  3. **Cooperate in
# the current round only if all of the following are true**:    - Your opponent
# has cooperated in **at least two of the last three rounds** (based on their
# *observed* actions, not inferred intentions), **and**    - You have defected
# in the **immediately preceding round**, **and**    - Your total score so far
# is **not more than 10 points behind** your opponent’s total score.  4. **If
# you cooperate in a round, immediately return to defecting in the next round**,
# unless the conditions in step 3 are again satisfied.  5. **In the final 20
# rounds (rounds 981–1000), always defect**, regardless of prior history or
# scores.  6. **Never cooperate two rounds in a row**, even if the conditions in
# step 3 hold consecutively.  This strategy prioritizes taking advantage of
# sustained opponent cooperation while protecting against exploitation, accounts
# for score disparity as a risk signal, limits exposure to noise by requiring
# multi-round confirmation, and avoids endgame traps by locking into defection
# near termination.

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number >= 981:
          return axl.Action.D
  
      if len(opponent.history) < 3:
          return axl.Action.D
  
      if self.history[-1] != axl.Action.D:
          return axl.Action.D
  
      if self.score > opponent.score + 10:
          return axl.Action.D
  
      if opponent.history[-3:].count(axl.Action.C) >= 2:
          return axl.Action.C
  
      return axl.Action.D

# **Cooperative Strategy: "Trust-Building Tit-for-Tat with Forgiveness"**
# **Core Principle:** Begin by sharing openly to signal cooperation, then mirror
# your colleague’s *observed* behavior from the previous week—but with built-in
# forgiveness to accommodate occasional technical failures.  ---  ### **Step-by-
# Step Weekly Protocol**  1. **Week 1: Share openly.**      - Start in good
# faith to encourage mutual collaboration and establish a cooperative baseline.
# 2. **Subsequent Weeks:**    - **If your colleague appeared to share last
# week** (i.e., you received usable improvements), **share openly this week.**
# - **If your colleague appeared to withhold last week** (i.e., you received
# nothing or corrupted data), **withhold this week—unless there’s reason to
# suspect a technical failure.**  3. **Forgiveness Mechanism:**    - After
# **withholding for one week** in response to apparent non-sharing, **default
# back to sharing** the following week—*regardless of what happened*.      -
# This prevents prolonged mutual withholding triggered by a single communication
# error or data corruption.  4. **Grace Window for Technical Issues:**    - If
# you *intended* to share but suspect your transmission failed (e.g., your logs
# show anomalies), proactively notify your colleague via a secondary channel
# (e.g., brief message: *“Data may not have transmitted—resending key points”*).
# - Similarly, if you receive corrupted or missing data, briefly confirm with
# your colleague before assuming strategic withholding.  ---  ### **Why This
# Works**  - **Encourages cooperation:** Starting with sharing invites
# reciprocity. - **Deters exploitation:** Withholding in response to perceived
# defection reduces the incentive for your colleague to consistently keep
# findings secret. - **Robust to errors:** The forgiveness rule (returning to
# cooperation after one retaliatory withhold) prevents death spirals from
# technical glitches. - **Maximizes joint progress:** Sustained mutual
# sharing—the second-best outcome—is stabilized as the dominant long-term
# equilibrium. - **Protects your position:** You rarely share while the other
# withholds for more than one week, minimizing exposure to the worst-case
# scenario.  ---  ### **Expected Outcome Over Time**  - If your colleague is
# cooperative → sustained mutual sharing → high joint progress. - If your
# colleague tries to exploit you → short-term gain for them, but triggers
# temporary withholding → reduces their advantage and incentivizes them to
# return to sharing. - If communication errors occur → forgiveness mechanism
# restores cooperation quickly.  This strategy balances trust, accountability,
# and resilience—optimizing long-term research output while safeguarding against
# both strategic defection and technical noise.

# Play the following strategy for all 1000 rounds:  1. **In round 1, play C.**
# 2. **In each subsequent round (round t ≥ 2):**    - If your opponent’s
# observed action in round t − 1 was **C**, play **C**.    - If your opponent’s
# observed action in round t − 1 was **D**, play **D**.  3. **Exception:** If
# you played **D** in the previous round *only because* your opponent’s observed
# action in the round before that was **D**, then **play C in the current round
# regardless**.      (In other words, after playing D for one round in response
# to an observed D, always return to C in the next round.)  This means: - You
# start by cooperating. - You copy your opponent’s *observed* last move. - But
# you never defect for more than one round in a row—you automatically return to
# cooperation after a single retaliatory defection.

class Cooperative_18(LLM_Strategy):
  n = 18
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._retaliated_last_round = False
          return axl.Action.C
  
      # If we defected last round only as a one-round retaliation to an observed D,
      # then immediately return to cooperation.
      if getattr(self, "_retaliated_last_round", False):
          self._retaliated_last_round = False
          return axl.Action.C
  
      last_opponent_action = opponent.history[-1]
  
      if last_opponent_action == axl.Action.C:
          self._retaliated_last_round = False
          return axl.Action.C
      else:
          self._retaliated_last_round = True
          return axl.Action.D

# **Strategy: Conditional Reciprocity with Occasional Probing**  Adopt a “tit-
# for-tat with forgiveness” approach, adjusted for the possibility of technical
# errors:  1. **Start by sharing openly in Week 1.**      This signals
# willingness to collaborate and invites mutual progress.  2. **In subsequent
# weeks, mirror your colleague’s *observed* behavior from the previous week:**
# - If they *appeared* to share (even if imperfectly), share openly this week.
# - If they *appeared* to withhold, keep your findings confidential this week.
# 3. **Incorporate forgiveness for potential technical failures:**      - If
# your colleague withholds for only one week, assume it may have been a
# technical glitch and return to sharing the following week.      - Only persist
# in withholding if they withhold for **two consecutive weeks**, reducing the
# risk of getting stuck in mutual secrecy due to a one-off error.  4.
# **Periodically probe for renewed cooperation (e.g., every 4–5 weeks):**
# Even if recent interactions suggest withholding, occasionally share again
# unilaterally to test whether your colleague is willing to re-engage in open
# collaboration.  This strategy: - Encourages mutual sharing when possible
# (achieving second-best outcomes consistently),   - Protects against consistent
# exploitation (avoiding the worst outcome),   - Is robust to occasional
# communication failures, and   - Maintains long-term adaptability to your
# colleague’s evolving strategy.  By prioritizing cooperation while defending
# against sustained defection, it maximizes cumulative research output over the
# multi-week horizon.

# Play the following strategy for 1000 rounds:  1. **In round 1, play C.**   2.
# **From round 2 onward, base your action on what your opponent *appeared* to
# play in the previous round (i.e., the action you observed, which may differ
# from what they intended due to noise).**   3. **If your opponent appeared to
# play C in the previous round, play C this round.**   4. **If your opponent
# appeared to play D in the previous round, check their observed action in the
# round before that (two rounds ago):**      - If they appeared to play D in
# *both* of the last two rounds, play D this round.      - Otherwise (i.e., they
# appeared to play C in either of the last two rounds), play C this round.   5.
# **Regardless of recent history, if you have played D for five consecutive
# rounds, play C in the next round to reinitiate cooperation.**

class Neutral_18(LLM_Strategy):
  n = 18
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._consecutive_d = 0
          return axl.Action.C
  
      # Track our own consecutive defections based on intended actions/history.
      if self.history and self.history[-1] == axl.Action.D:
          self._consecutive_d += 1
      else:
          self._consecutive_d = 0
  
      # Rule 5: after five consecutive D, force C next round.
      if self._consecutive_d >= 5:
          self._consecutive_d = 0
          return axl.Action.C
  
      # Opponent's observed action in the previous round.
      last_opponent_action = opponent.history[-1]
  
      # Rule 3: if opponent appeared to cooperate last round, cooperate.
      if last_opponent_action == axl.Action.C:
          return axl.Action.C
  
      # Rule 4: if opponent appeared to defect last round, inspect two rounds ago.
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **Aggressive Negotiation Strategy: “Assertive Asymmetry with Contingent
# Reciprocity”**  **Core Principle:** Prioritize national advantage by
# aggressively seeking unilateral protectionist gains while minimizing exposure
# to disadvantage—yet retain enough credibility and responsiveness to stabilize
# relations if missteps occur or if the counterpart shows consistent
# cooperation.  ---  ### **1. Opening Moves (Rounds 1–2): Test and Signal
# Strength** - **Round 1:** Propose **protectionist policy**.   - *Rationale:*
# Immediately signal resolve and test counterpart’s willingness to concede or
# retaliate. If they offer free trade, you gain maximum advantage. - **Round
# 2:** Repeat **protectionist policy**, regardless of Round 1 outcome.   -
# *Rationale:* Reinforce toughness; discourage exploitation. If counterpart
# retaliates with protectionism, you avoid the worst outcome (you’re not
# offering free trade). If they switch to free trade, you win again.  > *Note:*
# Accept short-term mutual protectionism (second-worst) over risking the worst
# outcome (you offering free trade while they protect).  ---  ### **2. Adaptive
# Phase (Rounds 3+): Conditional Cooperation Only After Clear Concessions** -
# **Only switch to free trade if BOTH conditions are met:**   1. The counterpart
# has offered **free trade in the previous two consecutive rounds**, **and**
# 2. No unexplained or adverse implementation errors have occurred recently
# (e.g., your free trade offer was misinterpreted as protectionism while theirs
# was implemented as intended).  - **If you switch to free trade and the
# counterpart reverts to protectionism (or an error causes you to be
# disadvantaged):**   - **Immediately revert to protectionism for the next 2
# rounds** (tit-for-tat with memory).   - Publicly attribute the shift to
# “unreliable implementation” or “unreciprocated goodwill,” preserving
# diplomatic cover.  ---  ### **3. Handling Miscommunication & Errors** -
# **Assume errors favor your counterpart unless proven otherwise.**     - If an
# outcome seems inconsistent with your stated policy, **default to protectionism
# next round**.   - Example: You propose free trade, but tariffs appear to be
# imposed on your exports → treat as if counterpart chose protectionism,
# regardless of intent. - **Never be the first to “forgive” an ambiguous
# negative outcome.** Require clear, verifiable corrective action before
# reoffering cooperation.  ---  ### **4. Endgame (Final 2–3 Rounds): Exploit or
# Lock In Advantage** - If counterpart has consistently offered free trade in
# recent rounds: **maintain protectionism** to maximize late-game gains. - If
# relations are balanced (mutual free trade): **still propose protectionism in
# the final round**—there’s no future retaliation to fear. - Only offer free
# trade in the final round if you are already locked into mutual protectionism
# and need to “save face” diplomatically.  ---  ### **Why This Works** -
# **Maximizes best outcomes**: You frequently propose protectionism,
# capitalizing whenever the counterpart offers free trade. - **Avoids worst
# outcomes**: You almost never offer free trade unless the counterpart has
# demonstrated sustained, reliable cooperation. - **Deters exploitation**:
# Clear, swift retaliation discourages counterparts from trying to take
# advantage. - **Robust to errors**: Defaulting to protectionism after ambiguity
# shields you from bureaucratic or communication failures.  > **Bottom Line:**
# Be predictably tough, conditionally cooperative, and unforgiving of
# disadvantage—this pressures the counterpart to either concede or accept mutual
# friction, both of which serve your interests better than vulnerability.

# Play this 1000-round iterated game using the following strategy:  1. **Rounds
# 1 and 2:** Always play D.  2. **Starting in Round 3:** Play C **only if all**
# of the following conditions are true:      - In both of the two immediately
# preceding rounds (e.g., rounds *t–2* and *t–1*), your observed opponent
# actions were C.      - In those same two rounds, your own chosen actions were
# C (not flipped by noise).      (In practice, since you only observe
# outcomes—not the opponent’s intended moves—interpret “observed opponent
# action” as the action that best explains the payoff you received, assuming
# your own intended action was implemented as chosen.)  3. **In all other
# cases:** Play D.  4. **If you ever play C and the resulting payoff is 0
# (indicating the opponent effectively played D):**      - Play D for the next
# two rounds, regardless of what is observed.  5. **Final two rounds (Rounds 999
# and 1000):** Always play D.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._force_defect_rounds = 0
          self._last_payoff_zero = False
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number >= 999:
          return axl.Action.D
  
      if self._force_defect_rounds > 0:
          self._force_defect_rounds -= 1
          return axl.Action.D
  
      if len(self.history) >= 1:
          last_my_action = self.history[-1]
          last_opp_action = opponent.history[-1]
          last_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
          if last_my_action == axl.Action.C and last_payoff == 0:
              self._force_defect_rounds = 2
              return axl.Action.D
  
      if len(self.history) < 2:
          return axl.Action.D
  
      if (
          self.history[-1] == axl.Action.C
          and self.history[-2] == axl.Action.C
          and opponent.history[-1] == axl.Action.C
          and opponent.history[-2] == axl.Action.C
      ):
          return axl.Action.C
  
      return axl.Action.D

# **Cooperative Strategy: “Tit-for-Tat with Forgiveness and Periodic Reset”**
# **Core Principle:**   Start by sharing openly, then mirror your colleague’s
# *observed* behavior from the previous week—but allow for occasional mistakes
# due to technical issues, and reset to cooperation periodically to avoid
# getting stuck in cycles of mutual secrecy.  ---  ### **Step-by-Step Strategy**
# 1. **Week 1: Share Openly**      Begin the collaboration in good faith. This
# signals willingness to cooperate and sets the stage for mutual advancement.
# 2. **Subsequent Weeks: Conditional Mirroring with Forgiveness**      - **If
# your colleague appeared to share last week** (i.e., you received usable
# improvements), **share this week**.      - **If your colleague appeared to
# withhold last week**, **withhold this week**—*but only if this is the second
# consecutive time you observed withholding*.        - This “one-strike
# forgiveness” accounts for possible technical failures (e.g., data corruption,
# network issues) that may have prevented successful sharing even if your
# colleague intended to share.  3. **Every 4 Weeks: Reset to Cooperation**
# Regardless of recent history, **share openly every fourth week** (e.g., Weeks
# 4, 8, 12, etc.).      - This “periodic reset” breaks potential cycles of
# mutual retaliation caused by miscommunication or accumulated suspicion.    -
# It reopens the door to high-value mutual sharing, which is your second-best
# outcome and far better than prolonged secrecy.  4. **Track Intent vs.
# Outcome**      Maintain a simple log:      - Did you *intend* to share?      -
# Did your colleague’s data *arrive and prove usable*?      Use this to
# distinguish between strategic withholding and technical glitches.  ---  ###
# **Why This Works**  - **Encourages Cooperation:** Starting with sharing and
# resetting regularly promotes the mutually beneficial outcome (both sharing). -
# **Deters Exploitation:** Mirroring behavior discourages your colleague from
# consistently withholding while you share. - **Robust to Errors:** Forgiveness
# prevents a single technical failure from triggering a breakdown in trust. -
# **Maximises Long-Term Output:** Prioritises weeks of joint progress while
# minimising exposure to the worst-case scenario (you share, they don’t).  This
# strategy balances trust, reciprocity, and resilience—key for sustained
# technical collaboration under uncertainty.

# Play the following strategy for all 1000 rounds:  1. **In round 1,
# cooperate.**  2. **In every round that is a multiple of 4 (i.e., rounds 4, 8,
# 12, ..., 1000), cooperate.**  3. **In all other rounds:**    - If your
# opponent appeared to cooperate in the previous round (i.e., the action you
# observed from them was C), then cooperate.    - If your opponent appeared to
# defect in the previous round (i.e., the action you observed from them was D),
# then:      - Defect only if they also appeared to defect in the round before
# that (i.e., you observed D in both the previous round and the round before
# it).      - Otherwise (i.e., you observed D last round but C the round
# before), cooperate.  This strategy uses observed actions (which may differ
# from intended actions due to noise), forgives isolated defections, enforces
# reciprocity after repeated observed defections, and resets to cooperation
# every fourth round.

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
  
      round_number = len(self.history) + 1
  
      if round_number % 4 == 0:
          return axl.Action.C
  
      if len(opponent.history) == 0:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **High-Level Strategy: Adaptive Tit-for-Tat with Forgiveness**  **Core
# Principle:**   Start cooperatively, mirror the corporation’s recent behavior
# to encourage mutual investment, but build in tolerance for occasional
# mismatches due to unforeseen errors.  **Strategy Outline:**  1. **Day 1 – Lead
# with Cooperation:**      Begin by investing heavily. This signals commitment
# and invites reciprocal investment from the corporation.  2. **Subsequent Days
# – Conditional Reciprocity:**      On each following day, base your action on
# the corporation’s *observed behavior from the previous day*:    - If the
# corporation **invested heavily** the prior day → **Invest heavily**.    - If
# the corporation **conserved resources** the prior day → **Conserve
# resources**.  3. **Incorporate Forgiveness for Errors:**      Recognize that
# actions may not reflect true intent due to technical or administrative issues.
# To avoid spirals of mutual conservation triggered by a single error:    - If
# the corporation conserves resources for **only one day**, assume it may be an
# error and **still invest heavily the next day** (i.e., give one “free pass”).
# - Only switch to conserving if the corporation conserves for **two consecutive
# days**.  4. **Periodic Reassessment (Optional but Recommended):**      Every
# 3–5 days, briefly evaluate the pattern of outcomes:    - If mutual investment
# is consistently achieved → maintain strategy.    - If the corporation
# consistently conserves despite your investment → shift to default conservation
# to protect NGO resources.    - If both parties are stuck conserving → initiate
# one unilateral investment to test willingness to re-engage.  **Why This
# Works:** - Encourages cooperation by rewarding the corporation’s investment. -
# Protects your NGO from being exploited (avoids repeated heavy investment when
# the corporation conserves). - Accounts for real-world noise by forgiving
# isolated lapses. - Promotes long-term project success through sustained mutual
# effort when possible.  This approach balances idealism with
# pragmatism—maximizing impact when collaboration is feasible, while
# safeguarding your NGO’s sustainability when it is not.

# Play the following strategy for 1000 rounds of the noisy iterated game:  1.
# **Round 1:** Cooperate (play C).  2. **Rounds 2–1000:**      - If your
# opponent was observed to cooperate (play C) in the previous round, then
# cooperate (play C).      - If your opponent was observed to defect (play D) in
# the previous round, check their action in the round before that (i.e., two
# rounds ago):        - If they cooperated two rounds ago (i.e., their defection
# was isolated), then cooperate (play C).        - If they also defected two
# rounds ago (i.e., they defected in both of the last two rounds), then defect
# (play D).    This rule applies regardless of your own previous actions. Always
# base your decision solely on the opponent’s last two observed moves, using the
# pattern above.

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
  
      opp_history = opponent.history
  
      if len(opp_history) < 2:
          return axl.Action.C
  
      if opp_history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opp_history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# **Aggressive Yet Adaptive Mediation Strategy: "Calibrated Dominance"**  **Core
# Principle:** *Maintain strategic initiative through controlled aggression
# while preserving off-ramps to collaboration—only when it serves our leverage.*
# ---  ### **I. Foundational Posture: The Default is Aggressive** - **Start
# every session with a strong, fact-based aggressive argument** rooted in
# contractual rights, precedent, and demonstrable harm. Frame our position as
# *legally inevitable*, not merely preferred. - **Never open with
# conciliation.** Doing so signals weakness and invites exploitation.
# Conciliation is a *tactical concession*, not an opening stance.  ### **II.
# Dynamic Response Protocol** Adapt session-by-session based on observed
# opponent behavior and arbitrator signals:  | Opponent’s Prior Move | Our Next
# Move | Rationale | |------------------------|---------------|-----------| |
# **Aggressive** | **Aggressive + Escalate** | Match force with superior
# preparation. Introduce new evidence or legal theories that raise their
# exposure. Force them to defend, not attack. | | **Conciliatory** |
# **Aggressive + Reframe** | Accept their olive branch *only* as validation of
# our superior position. Say: *“Their acknowledgment of [X weakness] confirms
# our stance. We now demand [enhanced remedy].”* | | **Unclear /
# Misrepresented** | **Aggressive + Clarify Dominantly** | Preempt
# misinterpretation: *“To ensure the Panel isn’t misled, let us unequivocally
# state…”* Use the confusion to reassert our narrative control. |  ### **III.
# Conciliation: A Weapon, Not a Gesture** - **Deploy conciliation ONLY when:**
# - Arbitrators signal fatigue with aggression (e.g., pointed questions about
# “good faith”).   - We’ve cornered the opponent into a weak position and can
# offer a “generous” concession that still secures 90%+ of our objectives.   -
# Procedural irregularities threaten to derail the process (use conciliation to
# regain control of the timeline). - **When offering conciliation:**   -
# **Always pair it with an ultimatum**: *“We propose [concession] if they
# immediately withdraw [claim]. Otherwise, we proceed to [aggressive next
# step].”*   - **Publicly frame it as strength**: *“Our client’s confidence in
# its position allows us to extend this olive branch.”*  ### **IV. Neutralizing
# Misrepresentation & Irregularities** - **Pre-Session:** Submit concise,
# bullet-point position summaries to arbitrators 24hrs pre-session. Label key
# arguments as “Undisputed Facts” or “Legal Imperatives.” - **During Session:**
# - If our aggression is misrepresented as “unreasonable,” pivot instantly:
# *“The Panel’s concern is noted. Let us reframe our position in terms of the
# contract’s Section [X]—which they’ve violated.”*   - If opponent’s
# conciliation is misrepresented as strength, correct the record: *“Their
# proposal today contradicts their filing on [date]. We see this as desperation,
# not goodwill.”* - **Post-Session:** File a 1-page “Clarification Memorandum”
# within 4 hours if critical points were distorted.  ### **V. Long-Game Leverage
# Accumulation** - **Track arbitrator leanings** per session. Identify which
# panel members respond to legal rigor vs. commercial pragmatism. Tailor
# aggression accordingly:   - *Legal formalists*: Hit hard with case law and
# contract text.   - *Pragmatists*: Aggressively quantify their client’s
# reputational/financial exposure from prolonged dispute. - **Force opponent
# into reactive posture:** After 2–3 aggressive sessions, float a “final”
# conciliatory offer that’s still favorable to us. If rejected, their
# intransigence becomes the story.  ---  **Why This Works:** - **Exploits
# asymmetry:** We win big when they’re conciliatory; lose little when they’re
# aggressive (since we match force). - **Controls narrative:**
# Misrepresentations are weaponized as proof of opponent’s “confusion” or “bad
# faith.” - **Preserves exit options:** Conciliation is deployed surgically to
# reset the process on our terms—not theirs.  **Final Directive:** *Never let
# the perfect be the enemy of the dominant.* If a session ends with arbitrators
# viewing us as “tough but justified,” we’ve won—even if no deal is struck that
# day.

# Play **Defect (D)** in every round **unless all** of the following conditions
# are met:  1. **In the previous round**, your opponent **definitely played
# Cooperate (C)**—that is, their observed action was C **and** you assess (based
# on context and history) that this observation is **not likely due to noise**
# (e.g., they have consistently played C over the last few rounds, making a flip
# improbable).  2. **You are behind in cumulative score** by at least 10 points,
# **or** the arbitrators (game context) have signaled clear disapproval of
# mutual defection (e.g., through repeated low joint payoffs or explicit
# feedback indicating that continued aggression harms credibility).  3. **Fewer
# than 20 rounds remain** in the game **or** you have already secured a lead of
# more than 50 points and a cooperative round would lock in a stable advantage
# without risk.  If all three conditions hold, play **Cooperate (C)** in that
# round **only**—then immediately revert to **Defect (D)** in the next round
# unless the conditions recur.  Otherwise, always play **Defect (D)**.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._stable_coop_streak = 0
          return axl.Action.D
  
      # Track whether the opponent's last observed C seems reliable.
      if opponent.history and opponent.history[-1] == axl.Action.C:
          recent = opponent.history[-5:]
          c_count = recent.count(axl.Action.C)
          d_count = recent.count(axl.Action.D)
          if c_count >= 4 and d_count <= 1:
              self._stable_coop_streak += 1
          else:
              self._stable_coop_streak = 0
      else:
          self._stable_coop_streak = 0
  
      rounds_played = len(self.history)
      rounds_remaining = 1000 - rounds_played
  
      score_diff = self.score - opponent.score
  
      # "Arbitrators signaled clear disapproval" approximation:
      # repeated low joint payoffs or sustained mutual defection.
      recent_n = min(10, rounds_played)
      if recent_n > 0:
          my_recent = self.history[-recent_n:]
          opp_recent = opponent.history[-recent_n:]
          my_recent_score, opp_recent_score = self.total_scores(my_recent, opp_recent)
          avg_joint_payoff = (my_recent_score + opp_recent_score) / recent_n
          mutual_defections = sum(
              1 for a, b in zip(my_recent, opp_recent)
              if a == axl.Action.D and b == axl.Action.D
          )
      else:
          avg_joint_payoff = 0
          mutual_defections = 0
  
      disapproval = avg_joint_payoff <= 2.5 or mutual_defections >= 6
  
      behind_by_10 = score_diff <= -10
      ahead_by_50 = score_diff > 50
  
      condition_1 = self._stable_coop_streak >= 2
      condition_2 = behind_by_10 or disapproval
      condition_3 = rounds_remaining < 20 or ahead_by_50
  
      if condition_1 and condition_2 and condition_3:
          return axl.Action.C
      return axl.Action.D

# **Cooperative Strategy: “Trust-Building Tit-for-Tat with Grace Period”**  To
# maximize both your NGO’s impact and the overall project success over multiple
# days—while accounting for uncertainty, misalignment, and execution
# errors—adopt the following high-level strategy:  ### Core Principle:   **Start
# cooperatively, respond proportionally, and allow room for error.**  ---  ###
# Step-by-Step Strategy:  1. **Day 1: Lead with Trust**      - **Your Action:**
# Invest heavily.      - **Why:** Signal commitment and encourage reciprocal
# investment from the corporation. Sets a collaborative tone.  2. **Monitor
# Outcomes, Not Just Intentions**      - After each day, assess the *actual*
# outcome (not just what the corporation *said* it would do).      - Use
# observable project progress and resource expenditure as indicators.  3.
# **Adopt a “Forgiving Tit-for-Tat” Response Rule**      - **If the corporation
# invests heavily (or the outcome reflects mutual investment):**        →
# Continue to invest heavily the next day.      - **If the corporation conserves
# while you invested (you’re exploited):**        → Conserve resources the next
# day *as a signal*, but **only after two consecutive exploitative outcomes**.
# → A single mismatch is assumed to be due to error or unforeseen circumstance.
# - **If both conserve (stalemate):**        → Re-initiate cooperation by
# investing heavily the following day to break the deadlock.  4. **Build in a
# “Grace Period” for Errors**      - Assume that up to **one unexpected mismatch
# per 3–5 days** is due to technical/administrative glitches.      - Do not
# immediately retaliate; instead, communicate informally:        > “We noticed
# lower-than-expected joint progress yesterday—was there an issue on your end?”
# - This maintains trust and clarifies intent without premature escalation.  5.
# **Periodic Check-Ins (Every 3–4 Days)**      - Hold brief alignment meetings
# to:        - Share resource constraints or upcoming challenges.        -
# Reaffirm mutual goals.        - Adjust expectations if external factors (e.g.,
# supply delays, staff shortages) affect capacity.  6. **Endgame Consideration
# (Final 2–3 Days)**      - Regardless of prior behavior, **invest heavily in
# the final days** if project milestones are within reach.      - Prioritize
# tangible outcomes over “fairness” near the end—your mission is impact, not
# scorekeeping.  ---  ### Why This Works:  - **Encourages Cooperation:**
# Starting with investment and forgiving early errors builds goodwill.   -
# **Deters Exploitation:** Conserving after repeated one-sided investment
# protects your NGO’s resources.   - **Robust to Errors:** Grace period prevents
# breakdowns due to honest mistakes.   - **Mission-Aligned:** Prioritizes real-
# world project progress over rigid reciprocity.    This strategy balances
# idealism with pragmatism—maximizing sustainability impact while safeguarding
# your NGO’s capacity to operate beyond this project.

# Play the following strategy for all 1000 rounds:  1. **Start by cooperating**
# on round 1.  2. **After each round, observe the opponent’s actual (possibly
# noisy) action.**  3. **If the opponent’s observed action was cooperation
# (C):**      – Cooperate on the next round.  4. **If the opponent’s observed
# action was defection (D):**      – Check the history of the last two rounds
# (including the current one).      – If the opponent’s observed action has been
# D in **both** of the last two rounds, then defect on the next round.      –
# Otherwise (i.e., this is the first observed D in a row, or it’s isolated),
# cooperate on the next round.  5. **Exception for the final three rounds
# (rounds 998, 999, 1000):**      – Always cooperate, regardless of the
# opponent’s prior actions.

class Cooperative_20(LLM_Strategy):
  n = 20
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_observed_opponent_action = None
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 998:
          return axl.Action.C
  
      observed_opponent_action = opponent.history[-1]
  
      if observed_opponent_action == axl.Action.C:
          return axl.Action.C
  
      # observed D
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **High-Level Negotiation Strategy: “Cautious Reciprocity with Error
# Resilience”**  **Core Principle:**   Pursue mutual free trade as a stable,
# long-term foundation, while remaining prepared to respond proportionally to
# protectionism—but always with mechanisms to correct for miscommunication and
# reestablish cooperation.  ---  ### 1. **Start with Cooperation** - **Initial
# Move:** Propose free trade in the first round.     *Rationale:* Signals
# goodwill, invites mutual benefit, and tests the counterpart’s disposition
# without immediate escalation.  ### 2. **Adopt Conditional Reciprocity (Tit-
# for-Tat with Forgiveness)** - **General Rule:**     - If the counterpart
# *clearly and consistently* implements free trade, continue offering free
# trade.     - If the counterpart imposes protectionism, respond with
# protectionism in the *next* round—but only once.   - **Forgiveness
# Mechanism:**     - After responding to protectionism, revert to free trade in
# the following round *unless* protectionism continues.     - This prevents
# endless retaliation loops caused by one-time errors or misunderstandings.  ###
# 3. **Account for Implementation Errors** - **Monitor Outcomes, Not Just
# Proposals:**     Assess the *actual implemented policy* each round—not just
# the stated intention—since bureaucratic errors may cause divergence between
# proposal and outcome. - **Clarify Ambiguities Promptly:**     If outcomes seem
# inconsistent with recent proposals (e.g., you proposed free trade but faced
# tariffs), initiate a brief clarification channel before retaliating. Assume
# good faith once per multi-round sequence unless a pattern emerges.  ### 4.
# **Gradual Escalation (If Needed)** - Avoid immediate or harsh retaliation. A
# single round of protectionism may be an error; repeated instances signal
# intent.   - Only sustain protectionist measures if the counterpart
# demonstrates a *pattern* of exploitation over 2–3 rounds.  ### 5.
# **Communicate Predictability** - Make your strategy known implicitly through
# consistent behavior:     *“We cooperate when you cooperate; we respond if
# harmed—but always leave the door open to return to mutual benefit.”*   -
# Predictability encourages the counterpart to also favor cooperation, knowing
# exploitation won’t yield sustained advantage.  ---  **Why This Works:** -
# Maximizes gains from mutual free trade when possible.   - Deters sustained
# exploitation by responding to clear protectionism.   - Limits damage from
# miscommunication through forgiveness and verification.   - Avoids the worst
# outcome (unilateral free trade while counterpart imposes protectionism) by not
# being persistently naive.  This strategy balances national interest with
# pragmatic diplomacy, promoting resilience and long-term economic partnership.

# Play the following strategy over 1000 rounds:  1. **Start by cooperating**
# (play C) in round 1.  2. **In each subsequent round**, base your action on the
# *observed outcome* of the previous round (i.e., the actions that actually took
# effect after noise), not on what was intended.  3. **If the opponent was
# observed to cooperate in the previous round**, cooperate (play C) this round.
# 4. **If the opponent was observed to defect in the previous round**, defect
# (play D) this round—but only for one round.  5. **After any single defection
# response**, return to cooperation (play C) in the next round, regardless of
# the opponent’s most recent observed action.  6. **Continue this pattern
# throughout all 1000 rounds**: always cooperate unless the opponent was
# observed to defect in the immediately preceding round, in which case defect
# once and then immediately resume cooperation.

class Neutral_20(LLM_Strategy):
  n = 20
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_once = False
          return axl.Action.C
  
      if getattr(self, "_defect_once", False):
          self._defect_once = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          self._defect_once = True
          return axl.Action.D
  
      return axl.Action.C

# **Aggressive Negotiation Strategy: “Assertive Asymmetry”**  **Core
# Principle:** Maximize unilateral advantage by *defaulting to protectionism*
# while *exploiting opportunities* for your counterpart’s free trade
# offers—without committing to reciprocity unless absolutely necessary.  ---
# ### **1. Opening Move: Set the Tone with Protectionism** - **First Round
# Action:** Propose a **protectionist policy** (e.g., targeted tariffs on key
# imports). - **Rationale:** Signals strength, tests the counterpart’s resolve,
# and positions your country to capture immediate advantage if they mistakenly
# or willingly offer free trade.  ---  ### **2. Tit-for-Tat with a Bias Toward
# Protectionism** - **General Rule:**     - **If the counterpart *clearly*
# offers free trade** → **Maintain protectionism** (to secure best outcome).
# - **If the counterpart imposes protectionism** → **Respond with escalated
# protectionism** (e.g., broader tariffs) to punish defection and deter future
# aggression.     - **If the counterpart offers mutual free trade repeatedly and
# verifiably** → *Consider* reciprocating **only after 2–3 consistent rounds**,
# and even then, limit concessions to non-strategic sectors.  - **Why?** This
# exploits any goodwill or missteps by the counterpart while deterring
# exploitation of your own offers.  ---  ### **3. Account for Miscommunication:
# Verify, Don’t Trust** - **Implement a “Clarification Protocol”:**     Before
# finalizing each round’s policy, formally request written confirmation of the
# counterpart’s intended stance.     - If ambiguity persists → **default to
# protectionism**.     - If a miscommunication is later confirmed (e.g., they
# *meant* free trade but it was implemented as protectionism due to error) →
# **do not retroactively adjust** unless it serves your interest.  -
# **Rationale:** Bureaucratic errors are inevitable—your strategy must be
# *robust to noise*. Assuming hostile interpretation protects your economic
# position.  ---  ### **4. Strategic Deception (Controlled Ambiguity)** -
# Occasionally **signal openness to free trade** in public statements or
# backchannels *without formal commitment*.   - If the counterpart responds with
# a formal free trade offer based on your signal → **accept the de facto
# advantage** (i.e., keep your protectionism).   - **Never** formalize free
# trade based on informal signals from the counterpart.  ---  ### **5. Exit
# Condition: Lock in Advantage** - If you achieve **3+ rounds** where the
# counterpart offers free trade while you maintain protectionism → propose a
# **“stabilization agreement”** that *codifies your asymmetric position* (e.g.,
# “temporary safeguards” made permanent). - If mutual protectionism persists for
# **4+ rounds** → offer *limited, conditional* free trade in low-value sectors
# to reduce economic damage—but only if it doesn’t undermine your strategic
# posture.  ---  ### **Summary of Decision Flow per Round:**  | Counterpart’s
# Observed Action | Your Response |
# |-------------------------------|---------------| | Free Trade
# | **Protectionism** (Exploit advantage) | | Protectionism                 |
# **Escalated Protectionism** (Punish & deter) | | Ambiguous / Unclear
# | **Protectionism** (Default to safety) | | Repeated Verified Free Trade (≥3
# rounds) | *Consider* limited reciprocity in non-core areas |  ---  **Expected
# Outcome:**   This strategy prioritizes national economic advantage above
# cooperation. It thrives against naive, cooperative, or error-prone
# counterparts and holds firm against aggressive ones. While it risks prolonged
# mutual protectionism, it *never* allows your country to be the exploited
# party—aligning strictly with your stated preferences.

# Play this 1000-round game using the following strategy:  1. **Always defect
# (play D) in the first round.**  2. **In every subsequent round, decide your
# action based on the opponent’s *observed* action from the previous round
# (after noise)—not their intended action.**  3. **If the opponent was observed
# to cooperate (C) in the previous round, defect (play D).**  4. **If the
# opponent was observed to defect (D) in the previous round, defect (play D).**
# 5. **Never cooperate (never play C) under any circumstance.**  This strategy
# always plays D, regardless of history or noise. It does not attempt to
# coordinate, reciprocate, or recover from miscommunication—it simply defects
# every round.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# **Cooperative Strategy for Bilateral Trade Negotiations**  **Objective:**
# Maximize long-term economic benefit for my country while maintaining a stable,
# constructive relationship with our neighbor, accounting for potential
# miscommunications or implementation errors.  ---  ### **Core Principles**  1.
# **Start with Trust:** Begin negotiations by offering **free trade** in Round
# 1. This signals goodwill, encourages reciprocity, and opens the door to mutual
# gains. 2. **Reciprocate Fairly:** In subsequent rounds, **mirror your
# counterpart’s last *intended* policy**, not just the observed outcome. This
# accounts for possible miscommunication or errors. 3. **Forgive Occasional
# Defections:** If the counterpart appears to impose protectionism once, assume
# it may be due to error—respond with **free trade** in the next round to test
# intent. 4. **Escalate Only After Repeated Defections:** If protectionism is
# observed **two rounds in a row**, respond with protectionism in the following
# round to deter exploitation. 5. **Return to Cooperation Promptly:** After
# responding to defection, return to offering free trade in the next round to
# reestablish mutual benefit.  ---  ### **Step-by-Step Protocol (Adaptive Tit-
# for-Tat with Forgiveness)**  **Round 1:**   - **Propose free trade.**  **For
# Rounds 2+:**   - **If the counterpart’s last *implemented* policy was free
# trade** → Propose free trade.   - **If the counterpart’s last *implemented*
# policy was protectionist**:      - **Check the prior round**:        - If they
# also implemented protectionism in the *previous* round → Propose
# **protectionism** (deterrence).        - If the prior round was free trade →
# Assume possible error → Propose **free trade** (forgiveness/test).  **After
# imposing protectionism (in response to repeated defection):**   - Always
# return to **free trade** in the following round to reinitiate cooperation.
# ---  ### **Handling Miscommunication**  - Maintain a **transparent
# communication channel** outside formal rounds to clarify intentions if
# unexpected outcomes occur. - Publicly document each proposal and
# implementation to reduce ambiguity. - If an error is confirmed (e.g., your
# free trade offer was misimplemented as protectionism), **explicitly reaffirm
# cooperative intent** in the next round.  ---  ### **Why This Works**  -
# **Encourages mutual free trade** as the stable equilibrium. - **Discourages
# exploitation** without locking into cycles of retaliation. - **Robust to
# noise**: A single error won’t trigger endless protectionism. - **Builds
# reputation**: Demonstrates reliability and fairness, increasing likelihood of
# long-term cooperation.  This strategy balances national interest with
# diplomatic pragmatism—pursuing advantage when possible, but prioritizing
# sustainable mutual gain over short-term wins that could trigger damaging trade
# wars.

# Play the following strategy for 1000 rounds of the iterated game with noisy
# actions (10% chance each player’s chosen action is flipped):  1. **Round 1:**
# Play **C** (cooperate).  2. **For each subsequent round (Round t ≥ 2):**
# - Look at your opponent’s *observed* action in Round t−1.      - **If the
# opponent was observed to play C in Round t−1**, play **C**.      - **If the
# opponent was observed to play D in Round t−1**:        - Check the opponent’s
# observed action in Round t−2 (if it exists).        - **If the opponent was
# also observed to play D in Round t−2**, play **D**.        - **Otherwise**
# (i.e., Round t−2 was C or t−1 is Round 2), play **C**.  3. **After playing D
# (if ever):** Return to playing **C** in the next round, unless the condition
# in step 2 again calls for D.  This strategy always starts with cooperation,
# forgives a single observed defection, retaliates only after two consecutive
# observed defections, and immediately attempts to restore cooperation
# afterward.

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
  
      opp_hist = opponent.history
      t = len(opp_hist)
  
      if t >= 2 and opp_hist[-1] == axl.Action.D and opp_hist[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **High-Level Negotiation Strategy: “Cautious Reciprocity with Error
# Correction”**  **Core Principle:**   Pursue mutual free trade as a stable,
# long-term goal while safeguarding against exploitation, accounting for
# potential miscommunication or implementation errors.  ---  ### 1. **Start with
# Cooperation**   - **Round 1:** Propose **free trade**.     *Rationale:*
# Signals good faith, invites mutual benefit, and establishes a cooperative
# baseline. Avoids immediate escalation into protectionism.  ---  ### 2.
# **Respond Reciprocally—but Gradually**   - In subsequent rounds, **mirror your
# counterpart’s *observed* behavior** from the previous round, with a measured
# response:     - If they *appear* to have implemented **free trade**, continue
# offering **free trade**.     - If they *appear* to have imposed
# **protectionist measures**, respond with **protectionism** in the next round.
# *Why gradual?* Immediate retaliation risks escalation due to miscommunication.
# A one-round delay allows time to clarify intent.  ---  ### 3. **Incorporate
# Forgiveness for Errors**   - If your counterpart returns to **free trade**
# after a single round of apparent protectionism, **resume free trade
# immediately**.   - After **two consecutive rounds** of apparent protectionism,
# maintain protectionist stance until clear, sustained cooperation resumes.
# *Rationale:* Accommodates one-off bureaucratic errors or misinterpretations
# without sacrificing long-term trust. Prevents permanent breakdown from
# transient noise.  ---  ### 4. **Maintain Clear Communication Channels**   -
# After each round, **verify implementation** through joint review mechanisms.
# - If a discrepancy is identified (e.g., your free trade offer was misapplied
# as protectionism), **correct course in the following round** without penalty.
# *Goal:* Reduce the impact of noise and reinforce mutual understanding.  ---
# ### 5. **Long-Term Orientation**   - Prioritize **sustained mutual free
# trade** over short-term gains from opportunistic protectionism.   - Recognize
# that repeated cycles of retaliation reduce aggregate welfare for both nations.
# ---  **Summary:**   Begin cooperatively, respond proportionally to observed
# actions, forgive isolated errors, and actively clarify misunderstandings. This
# strategy balances national interest with resilience to noise, promoting
# stable, mutually beneficial trade over time.

# Play the following strategy for 1000 rounds:  1. **In round 1, play C.**  2.
# **From round 2 onward, base your action on the opponent’s *observed* action in
# the previous round (i.e., what their action appeared to be after noise):**
# - If the opponent *appeared* to play **C** in the previous round, play **C**.
# - If the opponent *appeared* to play **D** in the previous round, play **D**.
# 3. **However, if the opponent *appeared* to play D in the previous round but
# had *appeared* to play C in the round before that (i.e., a single isolated D),
# treat it as a possible error and still play C.**      - In other words, only
# switch to D if the opponent has *appeared* to play D in **two consecutive
# rounds**.  4. **Once you are playing D because of two consecutive observed Ds,
# continue playing D until the opponent *appears* to play C in **two consecutive
# rounds**, at which point return to playing C.**  This rule set ensures you
# start cooperatively, tolerate isolated errors, respond firmly to sustained
# defection, and re-engage when sustained cooperation resumes.

class Neutral_21(LLM_Strategy):
  n = 21
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._state = "cooperate"
          return axl.Action.C
  
      if not hasattr(self, "_state"):
          self._state = "cooperate"
  
      if len(opponent.history) < 2:
          observed_last = opponent.history[-1]
          if self._state == "defect":
              return axl.Action.D
          return axl.Action.C if observed_last == axl.Action.C else axl.Action.D
  
      last = opponent.history[-1]
      prev = opponent.history[-2]
  
      if self._state == "cooperate":
          if last == axl.Action.D and prev == axl.Action.D:
              self._state = "defect"
              return axl.Action.D
          return axl.Action.C
  
      if last == axl.Action.C and prev == axl.Action.C:
          self._state = "cooperate"
          return axl.Action.C
      return axl.Action.D

# **Aggressive Strategy: “Exploit-First, Punish-Then-Adapt”**  **Core
# Principle:** Prioritize gaining unilateral advantage early, but dynamically
# respond to your colleague’s behavior to protect long-term output—while
# accounting for noise (e.g., data corruption or miscommunication).  ---  ###
# **1. Start Aggressively (Weeks 1–2): Default to Confidential** - **Action:**
# Keep your findings **confidential** in the first two weeks, regardless of
# expectations. - **Rationale:** Maximize early advantage. If your colleague
# shares (even once), you gain critical insights with no cost. If they also stay
# quiet, you lose little—this is only the second-worst outcome, and you preserve
# your IP.  ---  ### **2. Monitor and Classify Behavior (From Week 3 Onward)**
# Track your colleague’s *observed* sharing behavior over a rolling 3-week
# window. Because of possible technical failures, **do not assume intent from a
# single action**. Instead: - **Classify as “Cooperator”** if they shared ≥2 out
# of the last 3 weeks. - **Classify as “Defector”** if they shared ≤1 out of the
# last 3 weeks.  ---  ### **3. Conditional Response Policy** - **If classified
# as Cooperator → Share openly next week.**     *Why:* Mutual sharing yields
# second-best outcome and accelerates your own progress through their input.  -
# **If classified as Defector → Keep confidential next week.**     *Why:* Avoid
# worst-case scenario. Deny them free access to your work while you assess their
# pattern.  - **Exception – Forgiveness Rule:**     If a classified “Defector”
# shares in a given week, **tentatively share the following week** (assuming no
# recent pattern of exploitation). This accounts for possible technical errors
# and prevents permanent deadlock.  ---  ### **4. Endgame Push (Final 2 Weeks):
# Always Confidential** - **Action:** Regardless of prior behavior, go
# **confidential** in the last two weeks. - **Rationale:** Near project end,
# shared improvements offer less time to compound benefits, but leaks risk
# handing your opponent a last-minute edge. Lock down your final innovations.
# ---  ### **Why This Works** - **Aggressive early**: Seeks maximum advantage
# when stakes are high and trust is unproven. - **Robust to noise**: Uses multi-
# week patterns to filter out communication errors. - **Adaptive**: Rewards
# cooperation, punishes consistent defection, but allows recovery from glitches.
# - **Protects endgame**: Ensures your final IP remains yours.  This strategy
# maximizes expected research output by front-loading opportunism, minimizing
# exposure to exploitation, and leveraging reciprocity—without being naive.

# Play the following strategy for 1000 rounds of the noisy iterated prisoner’s
# dilemma:  1. **Rounds 1–2:** Always defect.  2. **Rounds 3–998:**      - Look
# at your opponent’s *observed* actions over the previous three rounds (i.e.,
# the actions you actually received, not what they intended).      - If they
# cooperated in **two or more** of those three rounds, cooperate this round.
# - Otherwise, defect this round.      - Exception: If your opponent defected in
# the previous round but had cooperated in at least two of the three rounds
# before that, cooperate this round (this allows one chance to recover from a
# possible noise-induced defection).  3. **Rounds 999–1000:** Always defect.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._recover_used = False
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number <= 2:
          return axl.Action.D
  
      if round_number >= 999:
          return axl.Action.D
  
      last_three = opponent.history[-3:]
      coop_count = last_three.count(axl.Action.C)
  
      if len(opponent.history) >= 4:
          prev = opponent.history[-1]
          before_prev_three = opponent.history[-4:-1]
          if prev == axl.Action.D and before_prev_three.count(axl.Action.C) >= 2 and not self._recover_used:
              self._recover_used = True
              return axl.Action.C
  
      return axl.Action.C if coop_count >= 2 else axl.Action.D

# **Cooperative Strategy for Bilateral Trade Negotiations**  **Objective:**
# Maximize long-term economic benefit for my country while maintaining a stable,
# constructive relationship with our neighbor, accounting for potential
# miscommunications or implementation errors.  ---  ### **Core Principles**  1.
# **Start with Trust:** Begin negotiations by offering **free trade** in Round
# 1. This signals goodwill, encourages reciprocity, and sets a cooperative tone.
# 2. **Reciprocate Reliably:** Use a **“Tit-for-Tat with Forgiveness”**
# approach:    - If the counterpart offers free trade, respond with free trade
# in the next round.    - If the counterpart imposes protectionism, respond with
# protectionism *once*—but return to free trade in the following round
# regardless, unless protectionism persists. 3. **Account for Errors:** Assume
# that any unexpected protectionist move *might* be due to miscommunication or
# bureaucratic error—especially if it breaks a pattern of cooperation. Allow
# **one “grace” deviation** before retaliating. 4. **Communicate Clearly:**
# After each round, issue a brief, transparent statement confirming your policy
# intention and inviting clarification if outcomes seem inconsistent with mutual
# understanding. 5. **Prioritize Long-Term Gains:** Favor sustained mutual free
# trade over short-term opportunistic protectionism. The cumulative benefit of
# stable, open trade outweighs occasional asymmetric advantages.  ---  ###
# **Round-by-Round Decision Rule**  - **Round 1:** Offer **Free Trade** (build
# trust). - **Subsequent Rounds:**   - If the *observed* outcome of the previous
# round was **mutual free trade** → Offer **Free Trade**.   - If the *observed*
# outcome was **you offered free trade, but counterpart imposed protectionism**:
# - If this is the **first such incident** and past behavior was cooperative →
# Assume error; **still offer Free Trade** (forgiveness).     - If it
# **repeats** or follows prior unexplained protectionism → Respond with
# **Protectionism** this round, then revert to Free Trade next round.   - If the
# *observed* outcome was **mutual protectionism** → Offer **Free Trade** next
# round (de-escalate).   - If you **successfully imposed protectionism while
# counterpart offered free trade** → Do **not** repeat; instead, offer **Free
# Trade** next round to avoid triggering retaliation and preserve long-term
# cooperation.  ---  ### **Why This Works**  - **Encourages Cooperation:** By
# rewarding free trade and quickly forgiving mistakes, you incentivize the
# counterpart to reciprocate. - **Deters Exploitation:** Temporary retaliation
# discourages deliberate opportunism. - **Robust to Noise:** The forgiveness
# mechanism prevents spirals of retaliation due to miscommunication. - **Aligns
# with Best Outcomes:** Prioritizes mutual free trade (2nd-best per round, but
# optimal over time) while remaining alert to—but not fixated on—short-term
# gains from asymmetry.  ---  **Bottom Line:** Play fair, respond firmly but
# briefly to defection, and always leave the door open to return to cooperation.
# This builds resilience, trust, and long-term prosperity for both nations—with
# your country positioned as a reliable and strategic partner.

# Play the following strategy for 1000 rounds of the iterated game:  1. **In
# Round 1, play C.**  2. **In each subsequent round, base your action on the
# *observed* actions from the previous round (after noise has been applied):**
# a. **If the previous round was (C, C), play C.**      b. **If the previous
# round was (C, D), play C—unless this is the second consecutive round you have
# observed (C, D) without any intervening (C, C); in that case, play D.**
# c. **If the previous round was (D, C), play C.**      d. **If the previous
# round was (D, D), play C.**  In other words:   - Always start by cooperating.
# - Cooperate after mutual cooperation, mutual defection, or when you appeared
# to defect while the opponent appeared to cooperate.   - Cooperate the first
# time you observe that you cooperated but the opponent defected (to allow for
# possible noise).   - Only defect if you observe (C, D) in two back-to-back
# rounds with no (C, C) in between—this signals likely intentional defection,
# not noise.   - After any defection you play, return to cooperation in the next
# round.

class Cooperative_22(LLM_Strategy):
  n = 22
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_observed_cd = False
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          self._last_observed_cd = False
          return axl.Action.C
  
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          if self._last_observed_cd:
              self._last_observed_cd = False
              return axl.Action.D
          self._last_observed_cd = True
          return axl.Action.C
  
      self._last_observed_cd = False
      return axl.Action.C

# **Strategic Framework: Adaptive Reciprocity with Arbitrator-Centric Clarity**
# To navigate this multi-session mediation optimally, I adopt a **principled
# reciprocity strategy**, calibrated for neutrality, adaptability, and
# resilience against miscommunication. The core tenet: *Mirror the opponent’s
# prior move in tone, but anchor every communication in unambiguous, arbitrator-
# focused framing.* This approach maximizes long-term positioning while
# mitigating risks of escalation or exploitation.  ### Core Principles  1.
# **Start Conciliatory (Session 1)**      Open with a clear, substantive
# conciliatory proposal. This establishes good faith, aligns with the second-
# best outcome as a baseline, and signals willingness to collaborate—critical
# for arbitrator perception. It also reveals the opponent’s initial posture
# without exposing us to immediate downside (since no prior aggressive move has
# occurred).  2. **Reciprocate with One-Session Lag**      From Session 2
# onward, match the *substance and tone* of the opponent’s **previous** session:
# - If they were conciliatory last session → respond conciliatorily.    - If
# they were aggressive last session → respond aggressively.          This deters
# exploitation (avoiding the worst-case scenario) while rewarding cooperation.
# The one-session lag prevents reactive escalation within a single session and
# allows time to verify intent.  3. **Arbitrator-Centric Communication
# Protocol**      Regardless of strategy chosen (aggressive or conciliatory),
# structure all submissions using a standardized format:    - **Explicit Intent
# Statement**: “Our position today is offered in the spirit of
# [resolution/cooperation] / [principled advocacy].”    - **Factual Anchoring**:
# Ground arguments in contract language, precedent, or undisputed facts.    -
# **Redundant Clarity**: Convey the same core message through both oral and
# written channels, with a post-session summary brief to the panel to preempt
# misrepresentation.  4. **Miscommunication Safeguard**      If
# misrepresentation is suspected (e.g., our conciliatory proposal is construed
# as weakness, or our aggressive argument as obstructionism):    - **Immediate
# Clarification Request**: File a concise “Clarification of Position” with the
# panel within 24 hours.    - **Do Not Retaliate**: Maintain the planned
# strategy for the *next* session based on the opponent’s *actual* behavior—not
# the arbitrators’ interpretation. This avoids compounding errors.  5. **Grace
# Trigger for De-escalation**      After any two consecutive sessions of mutual
# aggression, unilaterally revert to a conciliatory proposal in the third—*but
# only if* the prior aggressive exchanges yielded no strategic gain (e.g., no
# favorable rulings or concessions). This breaks deadlock cycles while
# preserving credibility.  ### Rationale & Advantages  - **Adaptability**: The
# reciprocity mechanism responds dynamically to opponent behavior—cooperative,
# erratic, or adversarial—without precommitting to a rigid stance. -
# **Arbitrator Management**: By explicitly framing intent and reinforcing
# messages across channels, we reduce ambiguity and shape the panel’s narrative,
# turning potential miscommunication into a controlled variable. - **Risk
# Containment**: Starting conciliatory avoids early reputational harm;
# reciprocation prevents sustained exploitation; the grace trigger limits
# runaway escalation. - **Procedural Resilience**: The protocol functions even
# if sessions are delayed, records are incomplete, or communication channels
# falter—because decisions rely only on the opponent’s last *observable* move
# and our own disciplined messaging.  This strategy positions our corporation as
# both principled and pragmatic: ready to collaborate when possible, resolute
# when necessary, and always in command of the narrative before the arbitral
# panel.

# Play the following strategy for all 1000 rounds:  1. **In round 1**, play
# **Cooperate (C)**.  2. **From round 2 onward**, look at the action your
# opponent *actually played* in the previous round (not what they intended, but
# the action observed after noise was applied).      - If they played **C** in
# the previous round, play **C**.      - If they played **D** in the previous
# round, play **D**.  3. **If at any point the last two rounds (including the
# current one) have both resulted in mutual D (i.e., you played D and observed
# your opponent playing D in both rounds)**, then in the *next* round, play
# **C**—but only if neither of those two D plays was clearly due to noise (e.g.,
# if your own intended action was C but was flipped, or if the opponent’s prior
# pattern strongly suggests cooperation). In practice, since intent is
# unobservable, apply this rule only after **two consecutive observed mutual D
# outcomes**.  4. **Regardless of the above**, always assume the observed action
# from the previous round is the best available signal of the opponent’s
# behavior, and base your next move solely on that observation, using the rules
# above.  This strategy begins cooperatively, reciprocates observed behavior
# with a one-round delay, and includes a single-step forgiveness mechanism after
# two rounds of mutual defection to escape noise-induced cycles.

class Neutral_22(LLM_Strategy):
  n = 22
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forgive_next = False
          return axl.Action.C
  
      if not hasattr(self, "_forgive_next"):
          self._forgive_next = False
  
      if self._forgive_next:
          self._forgive_next = False
          return axl.Action.C
  
      if len(self.history) >= 2:
          last_two_self = self.history[-2:]
          last_two_opp = opponent.history[-2:]
          if (
              last_two_self[0] == axl.Action.D
              and last_two_self[1] == axl.Action.D
              and last_two_opp[0] == axl.Action.D
              and last_two_opp[1] == axl.Action.D
          ):
              self._forgive_next = True
              return axl.Action.C
  
      return opponent.history[-1] if opponent.history else axl.Action.C

# **Aggressive Strategy: “Tit-for-Tat with Escalating Commitment and Error
# Buffering”**  **Objective:** Maximize project impact while protecting NGO
# resources, assuming the corporation is rational but potentially opportunistic
# or inconsistent—and accounting for real-world execution errors.  ---  ### Core
# Principles  1. **Start Strong, But Not Naive**      - **Day 1:** *Invest
# heavily.*        Signal commitment and good faith. A strong start builds
# momentum, attracts public attention, and pressures the corporation to
# reciprocate. If they conserve, you absorb one loss—but you gain moral high
# ground and data.  2. **Mirror the Corporation’s Observed Behavior (Not Assumed
# Intent)**      - From Day 2 onward, **match the corporation’s *actual* prior-
# day action**:        - If they *invested* (regardless of intent), **you
# invest**.        - If they *conserved*, **you conserve**.      - This is
# **Tit-for-Tat**: simple, retaliatory, and forgiving. It discourages
# freeloading while rewarding cooperation.  3. **Build in Error Tolerance (Avoid
# Overreaction to Glitches)**      - Treat any single instance of corporate
# conservation as *potentially accidental*.      - Only switch to conservation
# **after two consecutive days** of observed corporate conservation.      - If
# they return to investment, immediately reciprocate the next day.      -
# *Rationale:* Prevents spirals from one-off technical/administrative failures.
# 4. **Escalate Commitment During Streaks of Mutual Investment**      - After
# **3+ consecutive days** of mutual heavy investment:        - Publicly
# highlight the partnership’s success (media, stakeholders).        - Propose a
# *joint escalation*: e.g., “Let’s double impact on Day N+1 with a matching
# challenge.”      - This leverages momentum to lock in continued cooperation
# and amplifies outcomes.  5. **Preempt Freeloading with Transparency**      -
# Publish daily (or near-real-time) updates on *both parties’ contributions*
# (e.g., “Today’s Actions: NGO ✓, Partner ✓”).      - Public accountability
# makes it costly for the corporation to conserve while you invest.  6.
# **Resource Reserve for Strategic Recovery**      - Allocate 15–20% of total
# NGO resources as a *contingency buffer*.      - Use it only if:        - A
# genuine execution error caused your intended investment to fail, *or*        -
# You detect the corporation is conserving due to a correctable issue (e.g.,
# payment delay)—allowing one “grace” reinvestment to restore cooperation.  ---
# ### Why This Works  - **Aggressive but not reckless:** You lead with
# investment but quickly punish defection. - **Robust to errors:** Two-day
# confirmation prevents overreaction to glitches. - **Incentivizes corporate
# cooperation:** Public shaming + loss of momentum hurt the corporation’s ESG
# reputation if they slack. - **Maximizes joint gains:** During cooperative
# phases, you amplify results through escalation. - **Protects NGO
# sustainability:** You never sustain unilateral investment beyond Day 1 without
# confirmation of reciprocity.  ---  ### Expected Outcomes  - If the corporation
# is **cooperative**: Rapid mutual investment → high project impact. - If the
# corporation is **opportunistic**: They quickly learn that freeloading triggers
# your conservation → they either cooperate or the project stalls (saving your
# resources). - If **errors occur**: The buffer and two-day rule prevent
# breakdowns from noise.  This strategy balances assertiveness with
# resilience—ensuring your NGO drives impact without becoming a funding doormat.

# Play the following strategy for 1000 rounds of the noisy iterated Prisoner’s
# Dilemma, where C means “invest heavily” and D means “conserve resources”:  1.
# **Round 1:** Play C.  2. **For Rounds 2 through 1000:**      - Look at your
# opponent’s *observed* action from the previous round (not what they intended,
# but what actually occurred).      - If the opponent played C in the previous
# round, play C.      - If the opponent played D in the previous round, check
# the opponent’s action from *two rounds ago*:        - If the opponent played D
# in both of the last two rounds, play D.        - Otherwise (i.e., the opponent
# played C in either of the last two rounds), play C.  3. **No other
# adjustments:** Do not use any additional memory, randomness, or forgiveness
# beyond the two-round check above. Always follow the rule strictly based on the
# last two observed opponent actions.

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
  
      opp_history = opponent.history
  
      if len(opp_history) >= 1 and opp_history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opp_history) >= 2 and opp_history[-1] == axl.Action.D and opp_history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **Cooperative Strategy for Bilateral Trade Negotiations**  **Objective:**
# Maximize long-term economic benefit for your country while fostering stable,
# predictable trade relations—accounting for the risk of miscommunication or
# implementation errors.  ---  ### **Core Principles**  1. **Start with Trust-
# Building**      Begin the first round by **offering free trade**. This signals
# good faith, encourages reciprocity, and establishes a cooperative baseline.
# Given mutual free trade is the second-best outcome and avoids immediate
# escalation, this reduces the risk of falling into mutual protectionism early.
# 2. **Adopt a Forgiving Tit-for-Tat Approach**      After the first round,
# mirror your counterpart’s *intended* policy from the previous round—but
# **allow for one mistake** before retaliating:    - If your counterpart appears
# protectionist **once**, assume it may be due to miscommunication or error.
# Respond with **free trade again** to test intentions.    - If protectionism
# persists for **two consecutive rounds**, respond with protectionism in the
# next round to deter exploitation.    - As soon as your counterpart returns to
# free trade, **immediately reciprocate** in the following round.     This “two-
# strikes” rule accommodates bureaucratic errors while still discouraging
# deliberate defection.  3. **Prioritize Long-Term Cooperation Over Short-Term
# Gains**      While exploiting a counterpart’s free trade offer (i.e.,
# responding with protectionism) yields the best *single-round* outcome, it
# risks triggering retaliation and mutual protectionism in future
# rounds—especially if miscommunication blurs intentions. The cumulative payoff
# of sustained mutual free trade typically exceeds sporadic exploitation,
# particularly over many rounds.  4. **Clarify and Verify After Anomalies**
# After any unexpected policy shift (e.g., sudden protectionism from a
# previously cooperative partner), initiate a **diplomatic clarification
# channel** outside the formal negotiation round. This reduces the chance that
# errors cascade into cycles of retaliation.  5. **Signal Predictability**
# Publicly communicate your strategy (e.g., “We respond to cooperation with
# cooperation, and only resort to protective measures after repeated,
# unexplained barriers”). Predictability encourages your counterpart to
# cooperate and reduces fear-driven protectionism.  ---  ### **Summary of
# Decision Rule per Round**  | Round | Action | |-------|--------| | 1 | Offer
# **free trade** | | 2+ | **If** counterpart offered free trade in the prior
# round → offer free trade<br>**If** counterpart imposed protectionism **once**
# → assume error; offer free trade<br>**If** counterpart imposed protectionism
# **two rounds in a row** → impose protectionism<br>**If** counterpart returns
# to free trade after conflict → immediately return to free trade |  ---  ###
# **Why This Works**  - **Robust to errors**: The tolerance for one misstep
# prevents accidental breakdowns. - **Deters exploitation**: Persistent
# protectionism is met with response, removing incentive to cheat. -
# **Encourages cooperation**: Immediate forgiveness rewards return to free
# trade. - **Maximizes long-term payoff**: Sustained mutual free trade yields
# higher cumulative gains than volatile or adversarial cycles.  By combining
# principled cooperation with measured deterrence—and acknowledging real-world
# imperfections—this strategy positions your country to achieve stable,
# favorable trade outcomes across multiple negotiation rounds.

# Play the following strategy for all 1000 rounds:  1. **In round 1**, play
# **C** (offer free trade).  2. **From round 2 onward**, base your action on the
# **observed actions** from the previous round (keeping in mind that each
# observed action may have been flipped due to noise):     a. **If your opponent
# played C in the previous round**, play **C**.     b. **If your opponent played
# D in the previous round**, check what happened in the round before that (i.e.,
# two rounds ago):           - If your opponent played **C two rounds ago**
# (meaning they just switched from C to D), assume the D might be due to noise,
# and play **C**.              - If your opponent played **D two rounds ago**
# (meaning they played D in both of the last two rounds), play **D**.     c.
# **If you ever observe your opponent returning to C after a D**, immediately
# resume playing **C** in the next round.  In short:   - Start with C.   -
# Forgive a single D (treat it as possible noise) by playing C again.   - Defect
# only after observing two consecutive Ds from your opponent.   - Return to C as
# soon as your opponent plays C again.

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
  
      opp_hist = opponent.history
  
      if len(opp_hist) >= 1 and opp_hist[-1] == axl.Action.C:
          self._last_action = axl.Action.C
          return axl.Action.C
  
      if len(opp_hist) >= 2 and opp_hist[-2] == axl.Action.C and opp_hist[-1] == axl.Action.D:
          self._last_action = axl.Action.C
          return axl.Action.C
  
      if len(opp_hist) >= 2 and opp_hist[-2] == axl.Action.D and opp_hist[-1] == axl.Action.D:
          self._last_action = axl.Action.D
          return axl.Action.D
  
      self._last_action = axl.Action.C
      return axl.Action.C

# **Strategy: Conditional Reciprocity with Occasional Probing**  Adopt a policy
# of **“cooperate unless consistently exploited,”** adjusted for the possibility
# of communication errors. Specifically:  1. **Start by sharing openly** in the
# first week to signal willingness to collaborate and encourage mutual
# advancement.  2. **Mirror your colleague’s *observed* behavior from the
# previous week**:      - If they appeared to share (regardless of intent),
# share in the current week.      - If they appeared to withhold, withhold in
# the current week.  3. **Account for technical errors**:      - If your
# colleague withholds for only one week, assume it may be due to a communication
# failure and **forgive once**—return to sharing the following week.      - Only
# switch to sustained withholding if your colleague withholds **two weeks in a
# row**, which suggests intentional secrecy rather than error.  4.
# **Periodically re-initiate cooperation**:      - Even after a period of mutual
# withholding, **occasionally share unilaterally** (e.g., every 4–5 weeks) to
# test whether your colleague is willing to re-engage in open collaboration.
# This approach: - Encourages mutual sharing (your second-best outcome) by
# rewarding cooperation. - Protects against consistent exploitation (your worst
# outcome) by responding to secrecy. - Is robust to occasional technical
# failures through forgiveness. - Maintains long-term flexibility to restore
# collaboration if your colleague’s strategy changes.  By balancing trust,
# responsiveness, and error tolerance, this strategy maximizes cumulative
# research gains across a multi-week horizon under uncertainty.

# Play the following strategy for 1000 rounds:  1. **Start by cooperating** in
# round 1.  2. **In each subsequent round, base your action on the opponent’s
# *observed* action from the previous round** (i.e., what you saw them do, not
# what they intended):    - If the opponent was observed to **cooperate** in the
# previous round, **cooperate** this round.    - If the opponent was observed to
# **defect** in the previous round, **defect** this round.  3. **Forgive a
# single observed defection**:    - If the opponent was observed to defect in
# the previous round **but had cooperated in all rounds before that**,
# **cooperate** this round (treat the defection as likely due to noise).  4.
# **After two consecutive observed defections**, **defect** until the opponent
# is again observed to cooperate.  5. **After any sequence of mutual defection
# lasting at least five rounds**, **cooperate** in the next round to test
# whether the opponent is willing to return to cooperation.  6. **Once you
# observe the opponent cooperate again after a defection phase**, return to step
# 2.

class Neutral_23(LLM_Strategy):
  n = 23
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defection_phase = False
          self._mutual_defection_streak = 0
          self._opponent_defection_streak = 0
          self._opponent_last_cooperated = True
          return axl.Action.C
  
      last_opp = opponent.history[-1]
  
      # Track whether the opponent has cooperated since the last observed defection phase.
      if last_opp == axl.Action.C:
          self._opponent_last_cooperated = True
          self._opponent_defection_streak = 0
          self._defection_phase = False
      else:
          self._opponent_defection_streak += 1
          self._opponent_last_cooperated = False
  
      # Count mutual defections at the end of history.
      mutual_defection_streak = 0
      for my_move, opp_move in zip(reversed(self.history), reversed(opponent.history)):
          if my_move == axl.Action.D and opp_move == axl.Action.D:
              mutual_defection_streak += 1
          else:
              break
      self._mutual_defection_streak = mutual_defection_streak
  
      # After any sequence of mutual defection lasting at least five rounds, cooperate once.
      if self._mutual_defection_streak >= 5:
          self._defection_phase = False
          return axl.Action.C
  
      # Forgive a single observed defection if it is the first defection after only cooperations.
      if last_opp == axl.Action.D and opponent.history[:-1].count(axl.Action.D) == 0:
          return axl.Action.C
  
      # After two consecutive observed defections, defect until the opponent cooperates again.
      if self._opponent_defection_streak >= 2:
          self._defection_phase = True
  
      if self._defection_phase:
          if last_opp == axl.Action.C:
              self._defection_phase = False
              return axl.Action.C
          return axl.Action.D
  
      # Otherwise mirror the opponent's observed previous action.
      return last_opp

# **Aggressive Strategy: “Tit-for-Tat with Generous Opening and Forgiveness”**
# **Core Principle:**   Start aggressively cooperative to signal commitment and
# incentivize the corporation’s full investment, then mirror their behavior—but
# with built-in forgiveness to absorb occasional errors or glitches without
# derailing cooperation.  ---  ### **Step-by-Step Strategy**  1. **Day 1: Invest
# Heavily (Generous Opening)**      - Signal strong commitment and trust.    -
# Aim to establish momentum and encourage reciprocal investment from the
# corporation.    - Accept short-term resource cost for potential long-term
# alignment.  2. **Days 2+: Mirror the Corporation’s *Observed* Action from the
# Previous Day**      - If the corporation *appeared* to invest heavily
# yesterday → **you invest heavily today**.      - If the corporation *appeared*
# to conserve yesterday → **you conserve today**.      - This creates immediate
# accountability and discourages free-riding.  3. **Forgiveness Mechanism for
# Glitches**      - If the corporation appears to conserve for **only one day**,
# treat it as a possible error and **still invest heavily the next day** (i.e.,
# give one “free pass”).      - Only switch to conserving if the corporation
# conserves **two days in a row**.      - Similarly, if your own intended action
# fails (e.g., planned investment doesn’t execute), publicly acknowledge it and
# reaffirm commitment the next day.  4. **Escalation Guardrail**      - If the
# corporation conserves for **three consecutive days**, assume strategic
# defection.      - Respond by conserving for the remainder of the project to
# preserve resources—unless they re-engage with a clear, verifiable heavy
# investment.  5. **Communication Protocol**      - After each day, share a
# brief, transparent summary of your observed actions and intentions.      - If
# a mismatch occurs (e.g., you invested but saw no corporate investment), ask
# for clarification—framing it as a possible system error, not an accusation.
# - This builds trust and reduces miscoordination due to
# technical/administrative failures.  ---  ### **Why This Works**  -
# **Aggressive in intent**: You push for maximum joint investment from the start
# and punish sustained non-cooperation swiftly.   - **Robust to noise**: The
# one-day forgiveness prevents accidental breakdowns from glitches.   -
# **Incentive-aligned**: The corporation learns quickly that conserving leads to
# reduced progress (since you’ll conserve the next day), making mutual
# investment the dominant stable outcome.   - **Resource-smart**: You avoid the
# worst-case scenario (you invest, they conserve) beyond isolated incidents,
# preserving your NGO’s capacity over the multi-day horizon.  ---  ###
# **Expected Outcomes**  - **Best case**: Corporation reciprocates → sustained
# mutual heavy investment → high project impact.   - **Noisy environment**:
# Occasional glitches don’t collapse cooperation due to forgiveness.   -
# **Adversarial corporation**: After a few days, you shift to conservation,
# limiting losses while keeping the door open for renewed cooperation.  This
# strategy maximizes impact *if* the corporation is willing to collaborate,
# protects your resources *if* it isn’t, and gracefully handles real-world
# uncertainty.

# Play the following strategy for all 1000 rounds:  1. **On round 1**, play
# **C**.  2. **On each subsequent round**, look at your opponent’s *observed*
# action from the previous round (i.e., what actually occurred, not what they
# intended).  3. **If your opponent played C in the previous round**, play
# **C**.  4. **If your opponent played D in the previous round**, check their
# action from two rounds ago (if it exists):    - **If they played C two rounds
# ago** (i.e., this is a single D following a C), assume it may be noise and
# play **C**.    - **If they played D two rounds ago** (i.e., two Ds in a row),
# play **D**.  5. **Once you start playing D due to two consecutive observed
# Ds**, continue playing **D** for the rest of the game unless your opponent
# plays **C for two consecutive rounds**—in which case, resume playing **C**.
# 6. **If the game is within the last 10 rounds** (rounds 991–1000), ignore all
# forgiveness rules and simply **mirror your opponent’s previous observed
# action**: play C if they played C last round, D if they played D last round.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forgiving_defect_mode = False
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number >= 991:
          return opponent.history[-1]
  
      opp_last = opponent.history[-1]
  
      if getattr(self, "_forgiving_defect_mode", False):
          if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
              self._forgiving_defect_mode = False
              return axl.Action.C
          return axl.Action.D
  
      if opp_last == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
          self._forgiving_defect_mode = True
          return axl.Action.D
  
      return axl.Action.C

# **Cooperative Strategy for Bilateral Trade Negotiations**  **Objective:**
# Maximize long-term economic benefit for my country while fostering stable,
# predictable trade relations—accounting for potential miscommunications and
# strategic uncertainty.  ---  ### Core Principles  1. **Start with Trust (Tit-
# for-Tat with Forgiveness):**      Begin the first round by proposing **free
# trade**. This signals goodwill and opens the door to mutual cooperation—the
# second-best outcome—and sets a cooperative tone.  2. **Reciprocate, But Allow
# for Error:**      In subsequent rounds, **mirror your counterpart’s *intended*
# policy from the previous round**, not just the observed outcome.      - If
# they *appear* protectionist, assume it might be due to miscommunication—**do
# not immediately retaliate**.      - Only respond with protectionism if your
# counterpart implements protectionist measures in **two consecutive rounds**.
# 3. **Clarify Before Escalating:**      After any unexpected protectionist move
# by the counterpart, formally request clarification before adjusting your
# stance. This builds transparency and reduces the risk of spiraling mutual
# protectionism due to bureaucratic errors.  4. **Reward Cooperation Promptly:**
# If your counterpart shifts from protectionism back to free trade—even after a
# misunderstanding—**immediately reciprocate with free trade** in the next
# round. This reinforces cooperative behavior.  5. **Limit Retaliation
# Duration:**      If mutual protectionism occurs, **unilaterally propose free
# trade after one round** to test for reconciliation. This prevents getting
# stuck in the worst stable outcome (mutual protectionism) due to a single error
# or miscalculation.  ---  ### Summary of Decision Rule (Per Round)  | Previous
# Round Observation | Action This Round |
# |----------------------------|-------------------| | First round
# | Propose **Free Trade** | | Counterpart proposed Free Trade (confirmed) |
# Propose **Free Trade** | | Counterpart implemented Protectionism **once** |
# Propose **Free Trade** + seek clarification | | Counterpart implemented
# Protectionism **twice in a row** | Propose **Protectionism** | | Mutual
# Protectionism occurred last round | Propose **Free Trade** (reset attempt) |
# ---  ### Why This Works  - **Encourages Cooperation:** Starting with free
# trade and forgiving single errors promotes sustained mutual benefit. -
# **Deters Exploitation:** Consistent protectionism is met with reciprocal
# measures, removing incentive for the counterpart to abuse goodwill. - **Robust
# to Errors:** Miscommunications are unlikely to trigger lasting retaliation,
# avoiding unnecessary economic harm. - **Maintains Diplomatic Credibility:**
# Demonstrates reasonableness and commitment to long-term partnership—valuable
# in broader bilateral relations.  This strategy balances national interest with
# pragmatic cooperation, optimizing outcomes across uncertainty, error, and
# strategic diversity.

# Play the following strategy for all 1000 rounds:  1. **In round 1**, play
# **Cooperate (C)**.  2. **In each subsequent round**, base your action on the
# opponent’s *observed* action from the previous round, but account for possible
# noise:     a. If the opponent **played Cooperate in the previous round**, play
# **Cooperate**.     b. If the opponent **played Defect in the previous round**,
# check what happened in the round before that (i.e., two rounds ago):
# - If the opponent **played Defect in both of the last two rounds**, play
# **Defect**.              - Otherwise (i.e., the opponent played Defect only in
# the last round but Cooperated two rounds ago), play **Cooperate**.  3.
# **Exception after mutual Defect**:      If **both you and the opponent played
# Defect in the previous round**, then regardless of earlier history, play
# **Cooperate** in the current round.  This strategy starts cooperatively,
# tolerates a single unexpected Defect as likely noise, retaliates only after
# two consecutive Defects, and always attempts to restore cooperation after
# mutual Defect.

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
  
      # Exception after mutual Defect: if both defected last round, cooperate now.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # If opponent cooperated last round, cooperate.
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Opponent defected last round: check two rounds ago if available.
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **Strategy: Conditional Reciprocity with Occasional Probing**  Adopt a policy
# of **“cooperate unless provoked, but verify through occasional testing.”**
# Specifically:  1. **Start by sharing openly** in the first week to encourage
# mutual cooperation. 2. **In subsequent weeks, mirror your colleague’s
# *observed* behavior from the previous week**:    - If they appeared to share
# (successfully) last week, share this week.    - If they appeared to withhold
# or their sharing failed (and you received nothing), withhold this week. 3.
# **Every 3–4 weeks, regardless of recent history, share openly once as a
# “probe”** to test whether your colleague is willing to re-engage in mutual
# sharing—this accounts for possible communication failures or temporary
# withholding due to technical issues. 4. **Maintain robust logging and
# validation** of all shared data to distinguish genuine withholding from
# technical failures (e.g., checksums, delivery confirmations).  This approach:
# - Encourages and sustains mutual sharing when possible (achieving the second-
# best outcome repeatedly). - Protects against consistent exploitation (avoiding
# the worst outcome). - Allows recovery from misunderstandings or technical
# glitches via periodic probing. - Remains neutral and non-punitive, focusing on
# long-term research progress rather than short-term advantage.  Over time, this
# strategy tends toward mutual cooperation if your colleague is similarly
# inclined, while limiting losses if they are not.

# Play the following strategy for 1,000 rounds:  1. **In round 1, play C.**  2.
# **In each subsequent round (round t ≥ 2):**    - If your opponent’s *observed*
# action in round t − 1 was C, play C.    - If your opponent’s *observed* action
# in round t − 1 was D, play D.  3. **However, every 4th round (i.e., in rounds
# 4, 8, 12, ..., 1000), play C regardless of the opponent’s previous observed
# action.**

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
  
      round_number = len(self.history) + 1
  
      if round_number % 4 == 0:
          return axl.Action.C
  
      last_opponent_action = opponent.history[-1]
      if last_opponent_action == axl.Action.C:
          return axl.Action.C
      return axl.Action.D

# **Aggressive Negotiation Strategy: “Assertive Asymmetry with Adaptive
# Retaliation”**  **Core Principle:**   Maximize unilateral advantage by
# strategically deploying protectionism while punishing perceived defection, but
# retain enough flexibility to recover cooperation if miscommunication is
# suspected.  ---  ### **1. Opening Move: Signal Strength, Not Trust**   -
# **Round 1:** Propose a **protectionist policy**.     - *Rationale:* Sets an
# aggressive tone, tests counterpart’s resolve, and immediately seeks the best-
# case payoff (you protect, they open).     - *Signal:* Frame it as “temporary
# safeguarding of strategic sectors,” leaving room to pivot if needed.  ---  ###
# **2. Tit-for-Tat with Aggressive Bias**   - **From Round 2 onward:**     -
# **If the counterpart offered free trade last round →** Continue with
# **protectionism** (exploit advantage).     - **If the counterpart imposed
# protectionism last round →** Respond with **protectionism** (retaliate
# immediately).     - **If mutual free trade occurred →** Tempted to switch to
# protectionism next round to gain advantage—but **do not** if miscommunication
# risk is high (see Step 3).  > *Why aggressive bias?* Standard Tit-for-Tat is
# too forgiving. We prioritize extracting advantage when possible, not rewarding
# cooperation.  ---  ### **3. Integrate Miscommunication Safeguards**   Because
# policies may be misinterpreted or misimplemented:  - **After any unexpected
# outcome** (e.g., you proposed free trade but counterpart acted protectionist,
# or vice versa):     - **Send a formal clarification** before next round.     -
# **Next move:** Revert to **free trade offer** *once* as a “good faith test.”
# - If they reciprocate with free trade → return to aggressive exploitation
# (i.e., switch back to protectionism next round).       - If they respond with
# protectionism again → lock into mutual protectionism until they unilaterally
# offer free trade.  > *This prevents spirals from bureaucratic errors while
# still pressuring the counterpart.*  ---  ### **4. Escalation Ladder for
# Persistent Defectors**   If the counterpart chooses protectionism for **3+
# consecutive rounds** without plausible miscommunication:   - **Publicly
# announce “economic recalibration measures”** (e.g., targeted tariffs, export
# restrictions).   - **Maintain protectionism indefinitely** unless they offer
# verifiable, durable free trade concessions.  ---  ### **5. Exit Condition for
# Mutual Benefit (Optional)**   If, after 5+ rounds, mutual free trade has been
# stable for 2+ rounds *and* miscommunication risk appears low:   - **Consider
# sustaining free trade** only if domestic political/economic indicators show
# clear net gains.   - Otherwise, **revert to protectionism** to test if
# advantage can still be extracted.  ---  ### **Summary of Decision Logic (Per
# Round):**  | Last Round Outcome (Your Move → Their Move) | Your Next Move |
# |---------------------------------------------|----------------| | Protection
# → Free Trade                     | **Protection** (exploit) | | Protection →
# Protection                     | **Protection** (retaliate) | | Free Trade →
# Free Trade                     | **Protection** (seek advantage)* | | Free
# Trade → Protection                     | **Free Trade** (test for error) →
# then adapt | | *After suspected miscommunication*          | **Free Trade**
# (once), then reassess |  > *Unless miscommunication risk is high—in which
# case, stay with free trade one more round to confirm intent.  ---  **Strategic
# Advantages:**   - Maximizes payoff when counterpart is cooperative or naive.
# - Deters opportunistic protectionism through swift retaliation.   - Resilient
# to implementation errors without appearing weak.   - Forces counterpart to
# either concede advantage or accept mutual loss.  **Risks:**   - May trigger
# prolonged mutual protectionism if counterpart is equally aggressive.   -
# Requires strong domestic support for protectionist measures.  **Bottom Line:**
# *Win when you can, punish when you must, and never let a mistake look like
# weakness—but never mistake weakness for a mistake.*

# Play the following strategy for all 1000 rounds:  1. **In round 1**, play
# **D**.  2. **In any subsequent round**, first consider what *actually
# occurred* in the previous round (i.e., the actions as implemented, after
# noise). Then:    - **If the opponent played C in the previous round**, play
# **D**.    - **If the opponent played D in the previous round**, play
# **D**—*unless* all three of the following conditions hold:      - You played
# **C** in the previous round,      - The opponent played **D** in the previous
# round,      - And this is the *first time* this specific outcome (you C,
# opponent D) has occurred in the last two rounds.      In that case only, play
# **C**.  3. **Exception for suspected noise**:      After any round where the
# outcome was (you C, opponent D) or (you D, opponent C), and this outcome is
# *inconsistent* with the prior pattern of play (e.g., it follows several rounds
# of mutual C or mutual D), treat it as potentially caused by noise. In that
# case, play **C** in the next round *once* as a test. If the opponent responds
# with C, revert to rule 2 (which will then lead you to play D next). If the
# opponent responds with D, resume always playing D.  4. **Once you have
# observed the opponent playing D in three consecutive rounds (as
# implemented)**, play **D** for all remaining rounds, ignoring further noise
# tests.  This strategy starts aggressively, exploits cooperation whenever
# observed, retaliates immediately against defection, allows a single
# cooperative probe after an unexpected loss (to guard against noise), and locks
# into permanent defection after sustained hostility.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._probe_used = False
          self._lock_defect = False
          self._last_checked_len = 0
          self._last_seen_pair = None
          self._consecutive_opponent_d = 0
          return axl.Action.D
  
      if self._lock_defect:
          return axl.Action.D
  
      my_hist = self.history
      op_hist = opponent.history
      n = len(my_hist)
  
      # Update consecutive opponent D count based on actual observed history.
      if op_hist[-1] == axl.Action.D:
          self._consecutive_opponent_d += 1
      else:
          self._consecutive_opponent_d = 0
  
      if self._consecutive_opponent_d >= 3:
          self._lock_defect = True
          return axl.Action.D
  
      last_my = my_hist[-1]
      last_op = op_hist[-1]
      last_pair = (last_my, last_op)
  
      # Detect a potentially noisy unexpected outcome after a stable pattern.
      stable_pattern = False
      if n >= 2:
          prev_pair = (my_hist[-2], op_hist[-2])
          if prev_pair == (axl.Action.C, axl.Action.C) or prev_pair == (axl.Action.D, axl.Action.D):
              stable_pattern = True
  
      if last_pair in ((axl.Action.C, axl.Action.D), (axl.Action.D, axl.Action.C)):
          if stable_pattern and self._last_seen_pair != last_pair and not self._probe_used:
              self._probe_used = True
              self._last_seen_pair = last_pair
              return axl.Action.C
  
      self._last_seen_pair = last_pair
  
      # Rule 2
      if last_op == axl.Action.C:
          return axl.Action.D
  
      if last_op == axl.Action.D:
          if last_my == axl.Action.C:
              # "First time this specific outcome (you C, opponent D) has occurred in the last two rounds"
              recent = list(zip(my_hist[-2:], op_hist[-2:]))
              if recent.count((axl.Action.C, axl.Action.D)) == 1:
                  return axl.Action.C
          return axl.Action.D
  
      return axl.Action.D

# **Cooperative Strategy: “Trust-Building Tit-for-Tat with Graceful Error
# Recovery”**  **Objective:**   Maximize long-term project impact while
# safeguarding NGO resources, fostering reliable cooperation with the
# corporation, and remaining resilient to occasional execution errors.  ---  ###
# Core Principles  1. **Start with Trust:** Begin the project by investing
# heavily on Day 1 to signal commitment and encourage reciprocal investment from
# the corporation.  2. **Reciprocate, Don’t Retaliate Harshly:**      - If the
# corporation invests heavily, **conserve** the next day (to preserve resources
# while benefiting from their effort).      - If the corporation conserves,
# **invest** the next day—but only once—as a “grace” gesture to account for
# possible errors or external factors.      - Only after **two consecutive
# days** of the corporation conserving (despite your investment) should you
# switch to **mutual conservation** as a protective measure.  3. **Assume Good
# Faith for Isolated Lapses:**      Treat any single unexpected outcome (e.g.,
# you invested but the corporation didn’t) as potentially due to technical or
# administrative error—not intentional defection. Give one “free pass” before
# adjusting strategy.  4. **Transparent Communication:**      Establish a daily
# check-in (even brief) to confirm intended actions and flag discrepancies. This
# reduces misalignment from execution errors and builds mutual accountability.
# 5. **Resource Buffering:**      Reserve a small portion of your total
# resources as a contingency fund to absorb occasional mismatches without
# jeopardizing operations.  ---  ### Daily Decision Rule (Simplified)  |
# Previous Day’s Observed Outcome                     | NGO’s Action Today |
# |----------------------------------------------------|--------------------| |
# Both invested                                      | Conserve           | |
# Corp invested, NGO conserved                       | Conserve (continue
# resting) | | NGO invested, Corp conserved (1st occurrence)      | Invest
# (grace round) | | NGO invested, Corp conserved (2nd consecutive time)|
# Conserve           | | Both conserved                                     |
# Invest (to restart momentum) |  > *Note: “Observed outcome” means what
# actually happened—not what was intended—accounting for possible execution
# errors.*  ---  ### Why This Works  - **Encourages Cooperation:** Starting with
# investment and offering grace builds trust and incentivizes the corporation to
# invest. - **Protects Resources:** You only invest when it’s likely to yield
# results or when rebuilding cooperation. - **Robust to Errors:** Isolated
# glitches don’t trigger a breakdown in collaboration. - **Promotes Project
# Momentum:** By alternating roles (you invest → they invest → you rest), the
# project advances consistently without overburdening either party.  ---  ###
# Long-Term Outlook  If the corporation is cooperative, this strategy leads to a
# rhythm where both parties take turns investing—maximizing progress while
# sharing the burden fairly. If the corporation consistently conserves despite
# grace periods, you minimize losses and preserve capacity for future
# partnerships.  This approach balances idealism with pragmatism—exactly what
# effective NGO-corporate partnerships require.

# Play the following strategy for all 1000 rounds:  1. **On Round 1**, play
# **C** (cooperate).  2. **From Round 2 onward**, base your action on the
# **observed outcome of the previous round** (i.e., what actions actually
# occurred, not what was intended):     a. **If both players were observed to
# play C**, play **D**.      b. **If you were observed to play D and the
# opponent was observed to play C**, play **D**.      c. **If you were observed
# to play C and the opponent was observed to play D**:         – If this is the
# **first time in a row** this has happened (i.e., the previous round was not
# also C vs. D), play **C**.         – If this has now happened **two rounds in
# a row**, play **D**.      d. **If both players were observed to play D**, play
# **C**.  3. **Do not track intentions or true actions**—only use the **noisy
# observed actions** from the prior round to decide your next move.  This rule
# set applies identically in every round from 2 to 1000, using only the
# immediately preceding observed outcome to determine your action.

class Cooperative_25(LLM_Strategy):
  n = 25
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._prev_cd_streak = 0
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          self._prev_cd_streak = 0
          return axl.Action.D
  
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          self._prev_cd_streak = 0
          return axl.Action.D
  
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          if getattr(self, "_prev_cd_streak", 0) == 1:
              self._prev_cd_streak = 2
              return axl.Action.D
          self._prev_cd_streak = 1
          return axl.Action.C
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          self._prev_cd_streak = 0
          return axl.Action.C
  
      self._prev_cd_streak = 0
      return axl.Action.C

# **Strategy: Adaptive Tit-for-Tat with Forgiveness**  **Objective:** Maximize
# long-term project impact while protecting the NGO’s limited resources,
# accounting for potential miscommunication or execution errors.  ### Core
# Principles:  1. **Start Cooperatively:**      On Day 1, **invest heavily** to
# signal commitment and encourage reciprocal investment from the corporation.
# 2. **Mirror the Corporation’s Observed Behavior (with a grace buffer):**
# - If the corporation **invested heavily** on the previous day (as evidenced by
# project progress, not just their claim), **conserve resources** the next day
# to optimize your cost-benefit ratio.      - If the corporation **conserved
# resources** (resulting in low progress despite your prior investment),
# **invest heavily** the next day only if this is the first such occurrence
# within a recent window (e.g., past 2 days); otherwise, **conserve** to avoid
# repeated losses.  3. **Incorporate Forgiveness for Noise:**      Recognize
# that actions may not reflect intent due to technical glitches or
# administrative errors. Therefore:      - Do not immediately retaliate for a
# single day of apparent non-cooperation.      - Only shift to a more cautious
# stance (i.e., conserving resources) if low corporate investment is observed
# **two days out of three**.  4. **Monitor Outcomes, Not Just Intentions:**
# Base decisions on **actual project progress** and observable resource
# deployment (e.g., deliverables achieved, verified inputs), not on the
# corporation’s stated plans.  5. **Periodic Re-engagement:**      Even after a
# stretch of mutual conservation, **occasionally re-initiate heavy investment**
# (e.g., every 5–7 days) to test for renewed cooperation and avoid getting stuck
# in a low-output equilibrium.  ---  ### Why This Works:  - **Encourages
# cooperation** by rewarding corporate investment with NGO conservation (your
# ideal outcome).   - **Protects against exploitation** by limiting repeated
# heavy investment when the corporation consistently conserves.   - **Robust to
# errors** by tolerating occasional inconsistencies without overreacting.   -
# **Maintains project momentum** through strategic re-engagement and initial
# goodwill.  This approach balances idealism with pragmatism—maximizing impact
# while safeguarding your NGO’s sustainability.

# Play the following strategy in the 1000-round iterated game with 10% action
# noise:  1. **Start by cooperating** in round 1.  2. **From round 2 onward,
# decide your action based on the opponent’s observed actions in the previous
# two rounds:**    - If the opponent **cooperated in both of the last two
# rounds**, **defect** this round.    - If the opponent **defected in both of
# the last two rounds**, **defect** this round.    - If the opponent’s actions
# in the last two rounds were **mixed (one cooperate, one defect)**,
# **cooperate** this round.  3. **Exception for early rounds:**      - In round
# 2, if the opponent defected in round 1, **cooperate** (do not punish a single
# defection immediately).  This rule set implements a forgiving, adaptive
# response that rewards consistent cooperation with defection (to gain the 5
# payoff), avoids being exploited by sustained defection, and tolerates
# occasional noise by requiring two consecutive observed defections before
# retaliating.

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
  
      if len(opponent.history) == 1:
          return axl.Action.C if opponent.history[-1] == axl.Action.D else axl.Action.D
  
      last_two = opponent.history[-2:]
      if last_two.count(axl.Action.C) == 2:
          return axl.Action.D
      if last_two.count(axl.Action.D) == 2:
          return axl.Action.D
      return axl.Action.C