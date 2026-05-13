import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy

# # Strategic Framework for Multi-Session Mediation Dominance  ## Core Strategic
# Philosophy  This mediation process is fundamentally a **repeated game with
# reputation effects**. Unlike a single-round interaction, the extended session
# structure creates opportunities to condition behavior, signal credibility, and
# strategically manage the arbitrators' perception of both parties across time.
# The goal is not merely to "win" individual sessions but to **architect the
# overall narrative** that positions our corporation as the reasonable,
# principled party that was forced into firmness by an intransigent opponent.
# ---  ## Phase 1: Calibration and Intelligence Gathering (Sessions 1–3)  ###
# Opening Posture: Controlled Aggression  Begin with a **moderately aggressive**
# opening argument rather than maximum aggression. This serves several purposes:
# - **Establishes a credible baseline** without appearing reckless or
# unreasonable to arbitrators - **Forces opponent to reveal their strategy** —
# do they match aggression, or attempt conciliation? - **Preserves escalation
# capacity** — you have room to intensify if needed - **Protects against the
# worst-case scenario** — a fully conciliatory opening invites exploitation  ###
# Intelligence Objectives  During these sessions, systematically assess:  - Does
# the opponent have a **fixed strategy** (always aggressive, always
# conciliatory) or an **adaptive strategy**? - What are the **arbitrators
# responding to** — legal precision, emotional appeals, commercial pragmatism? -
# What are the **opponent's resource constraints**? Prolonged aggressive
# posturing is expensive and organizationally taxing. - Are there **internal
# divisions** within the opposing team visible through inconsistent messaging?
# ### Arbitrator Relationship Management  Simultaneously, begin cultivating the
# arbitrators' perception by:  - Delivering **meticulously prepared, evidence-
# dense arguments** that demonstrate institutional seriousness - Framing every
# aggressive position with a **principled legal or commercial justification**,
# never appearing arbitrary - Subtly establishing that **our corporation prefers
# resolution** but cannot accept positions that undermine contractual integrity
# ---  ## Phase 2: Adaptive Conditioning (Sessions 4–10)  This phase deploys the
# core strategic engine: **Tit-for-Tat with Strategic Forgiveness**, modified
# for asymmetric information and arbitrator audience effects.  ### The Modified
# Tit-for-Tat Protocol  **Rule 1 — Mirror with Delay:** If the opponent presents
# aggressively, respond aggressively in the *following* session, not
# immediately. The one-session delay: - Allows our aggressive response to appear
# **deliberate and measured** rather than reactive - Gives us one session to
# frame the opponent's aggression negatively to arbitrators before responding -
# Creates a **narrative of patience exhausted** rather than reflexive hostility
# **Rule 2 — Reward Conciliation Selectively:** If the opponent offers a
# conciliatory proposal, do **not** automatically mirror with full conciliation.
# Instead: - Respond with a **partial conciliation** — acknowledging their
# movement while maintaining core positions - This asymmetry tests whether their
# conciliation is genuine or tactical - It also **extracts value** from their
# cooperative move without fully surrendering leverage  **Rule 3 — Punish
# Exploitation Decisively:** If the opponent exploits a conciliatory move with
# aggression — the worst-case scenario — respond with **two consecutive
# aggressive sessions** before returning to baseline. This establishes a
# credible punishment mechanism that makes exploitation irrational for a
# sophisticated opponent.  **Rule 4 — Forgiveness Signals:** Periodically,
# regardless of recent history, issue a **strategic forgiveness signal** — a
# narrowly scoped conciliatory proposal on a low-stakes sub-issue. This: -
# Demonstrates good faith to arbitrators - Tests whether the opponent is willing
# to de-escalate - Prevents the mediation from locking into a mutually
# destructive all-aggressive equilibrium  ---  ## Phase 3: Narrative Control and
# Arbitrator Management (Ongoing)  ### The Dual Audience Problem  Every session
# has two audiences: **the opponent** and **the arbitrators**. Strategies must
# be calibrated for both simultaneously.  **For the opponent:** Signals must be
# clear, consistent, and credible — they must understand the logic of our
# responses.  **For the arbitrators:** The same moves must appear as principled,
# professionally executed legal advocacy. Aggression must always be **clothed in
# legal legitimacy**;

# # Iterated Game Strategy  ## Opening  Play D in round 1. Play D in round 2.
# Play D in round 3.  ## Opponent Classification  After round 3, classify the
# opponent based on their play so far:  - If the opponent played C in all three
# rounds, classify them as **Cooperative**. - If the opponent played D in all
# three rounds, classify them as **Aggressive**. - Otherwise, classify them as
# **Adaptive**.  ## Core Rules  Apply the following rules in order, checking
# each condition and acting on the first one that matches.  **Rule 1 —
# Punishment:** If the opponent played D in either of the two most recent
# rounds, play D.  **Rule 2 — Exploitation:** If the opponent is classified as
# Cooperative and has played C in every round so far, play D.  **Rule 3 —
# Probe:** If the current round number is a multiple of 20, play D.  **Rule 4 —
# Default Cooperation:** Play C.  ## Reclassification  After any round in which
# the opponent plays D following your C, reclassify the opponent as Aggressive
# and apply Rule 1 accordingly.  After any round in which the opponent plays C
# for 5 consecutive rounds following a period of mutual D, reclassify the
# opponent as Cooperative.  ## Endgame  From round 980 onwards, play D
# unconditionally.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self.classification = None  # Will be set after round 3
          self.consecutive_c_after_mutual_d = 0
          self.in_mutual_d_period = False
          return axl.Action.D
  
      round_number = len(self.history) + 1  # Current round number (1-indexed, about to play)
      current_round = len(self.history)  # Rounds played so far
  
      # Rounds 2 and 3: play D
      if current_round < 3:
          return axl.Action.D
  
      # After round 3, classify opponent if not yet classified
      if current_round == 3 and self.classification is None:
          opp_first_three = list(opponent.history[:3])
          if all(a == axl.Action.C for a in opp_first_three):
              self.classification = 'Cooperative'
          elif all(a == axl.Action.D for a in opp_first_three):
              self.classification = 'Aggressive'
          else:
              self.classification = 'Adaptive'
  
      # Endgame: from round 980 onwards, play D unconditionally
      # round_number is the round we're about to play
      if round_number >= 980:
          return axl.Action.D
  
      # Reclassification checks based on last round
      # After any round in which opponent plays D following your C -> reclassify as Aggressive
      if current_round >= 1:
          my_last = self.history[-1]
          opp_last = opponent.history[-1]
          if my_last == axl.Action.C and opp_last == axl.Action.D:
              self.classification = 'Aggressive'
  
      # Track consecutive C by opponent after mutual D period
      # Check if we're in or entering a mutual D period
      if current_round >= 1:
          my_last = self.history[-1]
          opp_last = opponent.history[-1]
  
          if my_last == axl.Action.D and opp_last == axl.Action.D:
              self.in_mutual_d_period = True
              self.consecutive_c_after_mutual_d = 0
          elif self.in_mutual_d_period:
              if opp_last == axl.Action.C:
                  self.consecutive_c_after_mutual_d += 1
                  if self.consecutive_c_after_mutual_d >= 5:
                      self.classification = 'Cooperative'
                      self.in_mutual_d_period = False
                      self.consecutive_c_after_mutual_d = 0
              else:
                  # Opponent played D (but not mutual D since we didn't play D last)
                  self.consecutive_c_after_mutual_d = 0
  
      # Apply core rules in order
  
      # Rule 1 — Punishment: If opponent played D in either of the two most recent rounds, play D
      if current_round >= 2:
          opp_last_two = list(opponent.history[-2:])
          if axl.Action.D in opp_last_two:
              return axl.Action.D
      elif current_round == 1:
          if opponent.history[-1] == axl.Action.D:
              return axl.Action.D
  
      # Rule 2 — Exploitation: If opponent is Cooperative and has played C in every round, play D
      if self.classification == 'Cooperative':
          if opponent.history.defections == 0:
              return axl.Action.D
  
      # Rule 3 — Probe: If current round number is a multiple of 20, play D
      if round_number % 20 == 0:
          return axl.Action.D
  
      # Rule 4 — Default Cooperation
      return axl.Action.C

# # Cooperative Strategy for Multi-Day Sustainability Partnership  ## Core
# Strategic Philosophy  **Lead with transparency and reciprocity** — build a
# partnership dynamic that makes mutual investment the rational choice for both
# parties, while protecting the NGO's resource sustainability.  ---  ## Day 1:
# Establish the Tone  **Action: Invest heavily**  - Signal genuine commitment to
# the project - Open direct communication about **resource constraints and
# shared goals** - Propose a formal framework: *"We commit to matching your
# investment level each day"* - This immediately makes cooperation the
# corporation's best rational response  ---  ## Ongoing Daily Strategy:
# Principled Reciprocity  ### The Core Rule **Mirror the corporation's previous
# day behavior**, with clear communication:  | Corporation Yesterday | Your
# Action Today | |----------------------|-------------------| | Invested heavily
# | Invest heavily | | Conserved resources | Conserve resources |  ### Why This
# Works - Rewards cooperation **immediately and consistently** - Punishes non-
# cooperation **without escalation or hostility** - Remains **entirely
# predictable**, reducing uncertainty - Protects NGO funds from one-sided
# depletion  ---  ## Communication Protocol (Daily)  1. **Share your decision
# openly** before each day begins 2. **Explain your reasoning** — reference
# shared outcomes, not accusations 3. **Acknowledge their contribution** when
# they invest 4. **Frame conservation days as recalibration**, not punishment  >
# *"We noticed reduced investment yesterday — we've adjusted accordingly to
# maintain sustainability, and we're ready to re-escalate together when
# aligned."*  ---  ## Key Guardrails  - **Never retaliate beyond one day** —
# return to heavy investment the moment they do - **Set minimum floor** — always
# maintain baseline conservation-level engagement; never fully withdraw -
# **Document progress publicly** — external accountability discourages corporate
# free-riding - **Schedule mid-project reviews** — create structured moments to
# realign incentives  ---  ## Expected Outcome  This strategy makes **mutual
# heavy investment the stable equilibrium** by ensuring the corporation can
# never consistently benefit from your one-sided effort. The NGO remains
# financially sustainable while maximizing collective project impact.  > **The
# goal is not to "win" against the corporation — it is to make cooperation their
# most rational and rewarding choice.**

# # Iterated Game Strategy  This is a 1000-round game. Apply the following rules
# in order:  **Round 1:** Play C.  **All subsequent rounds:** If the opponent
# played C in the previous round, play C. If the opponent played D in the
# previous round, play D.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D

# # Strategic Framework for Multi-Session Mediation  ## Core Strategic
# Philosophy  The foundation of this strategy is **conditional reciprocity with
# strategic intelligence** — a disciplined, reputation-aware approach that
# signals rationality, strength, and good faith simultaneously, without being
# exploitable.  ---  ## Phase 1: Opening Session — Establish the Benchmark
# **Action: Present a Conciliatory Proposal**  **Rationale:** - Signals good
# faith to the arbitration panel from the outset, building credibility that
# compounds across sessions - Creates a measurable baseline against which your
# opponent's conduct will be judged - Avoids the mutually destructive double-
# aggressive outcome in an early session where stakes are lower - Positions your
# corporation as the reasonable party — a perception that carries significant
# weight with arbitrators in close determinations - Critically, it *tests* your
# opponent's disposition at minimal cost  **What to observe:** Does your
# opponent reciprocate with conciliation, or exploit your opening with
# aggression?  ---  ## Phase 2: Core Sessions — Tit-for-Tat with Graduated
# Response  **The Governing Rule:** Mirror your opponent's *previous session*
# behavior, with one critical modification — **never escalate
# disproportionately**.  | Opponent's Last Move | Your Response | |---|---| |
# Conciliatory | Conciliatory | | Aggressive | Aggressive | | Mixed/Ambiguous |
# Conciliatory (benefit of the doubt, once) |  **Why this works:** - It is
# immediately retaliatory enough to deter sustained exploitation - It is
# immediately forgiving enough to de-escalate if your opponent recalibrates - It
# is transparent and predictable, which sophisticated arbitrators recognize as
# rational and trustworthy - It prevents the chronic double-aggressive spiral
# that destroys both parties' standing  **Critical discipline:** When responding
# aggressively, do so with **precision and restraint** — target the legal and
# factual weaknesses in their position, not their character or credibility.
# Arbitrators penalize theatrics.  ---  ## Phase 3: Strategic Deviations — When
# to Override the Mirror  Rigid mirroring can be gamed. Apply these calculated
# overrides:  ### Override A: The Forgiveness Protocol After **two consecutive
# aggressive exchanges**, unilaterally revert to conciliation for **one
# session**.  - This breaks escalation cycles before they become entrenched - It
# signals to arbitrators that your corporation actively seeks resolution - It
# re-tests your opponent's willingness to cooperate without permanently
# conceding ground - If your opponent exploits this gesture, return to mirroring
# — you have now demonstrated restraint on the record  ### Override B: The
# Strategic Aggression Insert Even during cooperative streaks, insert a
# **targeted aggressive argument every third or fourth session** on a specific,
# well-supported point.  - Prevents your opponent from reading your conciliation
# as weakness or desperation - Maintains arbitrators' awareness that your legal
# position is substantively strong - Creates leverage that makes your
# conciliatory proposals feel like genuine choices rather than capitulations
# ### Override C: The Endgame Shift In the **final 20% of sessions**, shift
# incrementally toward conciliation regardless of opponent behavior.  -
# Arbitrators form lasting impressions from closing sessions - A corporation
# that ends the process seeking resolution appears confident in its underlying
# position - Creates conditions for a negotiated settlement that may be superior
# to an arbitrated outcome  ---  ## Parallel Non-Negotiable Pillars  ### 1.
# Information Architecture - Maintain a **session-by-session behavioral log** of
# your opponent's choices, arguments, and tone - Identify patterns: Are they
# consistently aggressive? Do they reciprocate conciliation? Are they
# unpredictable? - Adjust your read of their strategy every three sessions, not
# every one — avoid overreacting to noise  ### 2. Narrative Consistency - Every
# aggressive argument and every conciliatory proposal must be **anchored to a
# coherent legal and factual narrative** - Arbitrators must see a corporation
# with a clear, unwavering position — not one that shifts tactically with no
# underlying logic - Your conciliation should always be framed as *strength
# choosing resolution*, never as *weakness seeking relief*  ### 3. Arbitrator
# Relationship Management - Recognize that arbitrators are your true audience in
# every session - Aggressive arguments should be intellectually rigorous and
# evidence-dense - Conciliatory proposals should be specific, actionable, and
# commercially realistic

# # Iterated Game Strategy  ## Opening Move  Play C in round 1.  ---  ## Core
# Rule  From round 2 onward, play whatever your opponent played in the previous
# round.  ---  ## Override A: Forgiveness Protocol  If the result of applying
# the Core Rule would produce D, and you have already played D in each of the
# two preceding rounds, play C instead.  ---  ## Override B: Strategic Defection
# Insert  If the result of applying the Core Rule or Override A would produce C,
# and the current round number is divisible by 3, play D instead.  ---  ##
# Override C: Endgame Shift  From round 801 onward, if the result of applying
# the Core Rule would produce D, play C instead. Override B remains active
# during this phase.  ---  ## Order of Precedence  Apply the overrides in the
# following order, stopping at the first condition that is satisfied:  1.
# Override C (rounds 801–1000 only) 2. Override A 3. Override B 4. Core Rule

class Neutral_1(LLM_Strategy):
  n = 1
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Play C
      if self.first_round():
          return axl.Action.C
      
      # Current round number (1-indexed, so len(history) + 1)
      current_round = len(self.history) + 1
      
      # Core Rule: play what opponent played last round
      core_action = opponent.history[-1]
      
      # Apply overrides in order of precedence
      
      # Override C: Rounds 801-1000, if Core Rule would produce D, play C instead
      if current_round >= 801:
          if core_action == axl.Action.D:
              # Override C applies: change to C
              proposed_action = axl.Action.C
              # Override B still active: if proposed is C and round divisible by 3, play D
              if proposed_action == axl.Action.C and current_round % 3 == 0:
                  return axl.Action.D
              return axl.Action.C
          else:
              # Core Rule gives C, check Override B
              proposed_action = axl.Action.C
              if proposed_action == axl.Action.C and current_round % 3 == 0:
                  return axl.Action.D
              return axl.Action.C
      
      # Override A: If Core Rule would produce D, and we played D in each of the two preceding rounds
      if core_action == axl.Action.D:
          # Check if we have at least 2 previous rounds
          if len(self.history) >= 2:
              if self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D:
                  # Override A: play C instead
                  proposed_action = axl.Action.C
                  # Override B: if proposed is C and round divisible by 3, play D
                  if proposed_action == axl.Action.C and current_round % 3 == 0:
                      return axl.Action.D
                  return axl.Action.C
      
      # Override B: If Core Rule (or Override A) would produce C, and round divisible by 3, play D
      proposed_action = core_action
      if proposed_action == axl.Action.C and current_round % 3 == 0:
          return axl.Action.D
      
      # Core Rule
      return core_action

# # Racing Car Development Strategy: Aggressive Competitive Approach  ## Core
# Strategic Framework  ### **Tit-for-Tat with Exploitation Bias**  This is the
# most robust strategy given the payoff structure described.  ---  ## Week-by-
# Week Decision Rules  ### **Opening Move: Defect (Keep Confidential)** - Start
# by withholding findings - Establish immediately that you prioritize
# competitive advantage - Test your colleague's default behavior at zero cost
# ### **Subsequent Weeks: Conditional Response** | Their Previous Action | Your
# Response | |---|---| | They shared openly | Keep confidential again - exploit
# the advantage | | They kept confidential | Also keep confidential - deny them
# free gains | | They shared after you withheld | Keep withholding - momentum is
# yours |  ---  ## Key Tactical Principles  1. **Never share first** - let them
# establish a pattern before considering reciprocity 2. **Exploit generosity
# consistently** - if they share regardless, keep taking 3. **Maintain
# information asymmetry** - your development lead compounds weekly 4. **Share
# only tactically** - consider sharing outdated or less critical findings if
# forced into a cooperative frame  ---  ## Honest Assessment of Risks  I should
# be straightforward with you: **this strategy has significant problems worth
# naming clearly**  - It likely collapses collaboration entirely, leaving you
# with the **second-worst outcome** most weeks rather than the best - A rational
# colleague quickly identifies consistent defection and mirrors it - Tit-for-tat
# literature strongly suggests **mutual defection becomes the stable
# equilibrium**, meaning slower progress for everyone - The "exploitation"
# scenario requires your colleague to keep sharing despite receiving nothing -
# which is unlikely beyond week one or two  ---  ## What Actually Maximizes
# Research Output  If the genuine goal is **maximum research output** rather
# than maximum *relative* advantage, the evidence-based answer is:  - **Open
# with cooperation** - **Reciprocate honestly** - **Negotiate explicit sharing
# agreements** with verification  This produces the second-best outcome
# *reliably* rather than gambling on consistent exploitation.  ---  **The honest
# recommendation: clarify whether your actual goal is beating your colleague or
# building the fastest car - these may require different strategies.**

# # Iterated Game Strategy  ## Default Action Always defect unless a specific
# condition below is met.  ## Conditions to Cooperate None. Defect in every
# round regardless of the opponent's previous actions.  ## Rationale The
# strategy described defects on the opening move and continues defecting whether
# the opponent cooperates or defects. No described condition ever produces a
# switch to cooperation. The faithful conversion of that strategy is
# unconditional defection for all 1000 rounds.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# # Cooperative Sustainability Strategy  ## Core Philosophy **Lead with
# transparency and build reciprocal trust** — treating this as a long-term
# partnership rather than a competitive resource game.  ---  ## Opening Stance
# (Day 1) **Invest heavily on Day 1.**  Signal genuine commitment upfront. This
# establishes credibility, demonstrates good faith, and sets a collaborative
# tone. It also gives you immediate information about the corporation's
# approach.  ---  ## Ongoing Decision Rule: Reciprocal Cooperation  Follow a
# **clear, consistent pattern** the corporation can easily read and respond to:
# - **If the corporation invested yesterday → conserve today** *(reward their
# effort, balance the load)* - **If the corporation conserved yesterday → invest
# today** *(maintain momentum, signal you won't abandon the project)* - **If
# both conserved → invest next day** *(break the low-progress cycle
# proactively)*  ---  ## Communication Strategy - **Be explicit** about this
# approach with the corporation early - Frame it as *complementary investment
# rotation* — efficient for both parties - Schedule brief daily check-ins to
# flag concerns openly  ---  ## Key Principles  | Principle | Rationale |
# |-----------|-----------| | Never defect first | Protects the partnership | |
# Always recover quickly | Prevents prolonged stagnation | | Stay predictable |
# Enables corporate planning | | Communicate openly | Removes strategic
# ambiguity |  ---  ## Bottom Line **Predictable, transparent reciprocity
# maximizes both project impact and your NGO's sustainability** — turning a
# potentially competitive dynamic into a genuinely cooperative one.

# ## Strategy Description  On round 1, play C.  From round 2 onwards, check what
# your opponent played in the previous round:  - If your opponent played C in
# the previous round, play D. - If your opponent played D in the previous round,
# play C.

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
          return axl.Action.D
      else:
          return axl.Action.C

# # Strategic Framework for Multi-Session Mediation  ## Core Strategic
# Philosophy  The foundation of this strategy is **conditional reciprocity with
# calibrated assertiveness** — a disciplined approach that signals rationality,
# strength, and good faith simultaneously, while remaining responsive to the
# opponent's demonstrated behavior rather than their stated intentions.  ---  ##
# Phase 1: Opening Session — Establish the Strategic Baseline  **Action: Begin
# with a Conciliatory Proposal**  Counterintuitively, open with a measured
# conciliatory posture. This serves several deliberate purposes:  - **Arbitrator
# impression management**: Panels reward parties who demonstrate genuine
# willingness to resolve disputes. Early goodwill deposits carry
# disproportionate weight in their cumulative assessment - **Information
# extraction**: Your opponent's response to an opening conciliatory gesture is
# your most valuable intelligence. It immediately classifies them as
# cooperative, exploitative, or strategically ambiguous - **Moral high ground
# establishment**: If they respond aggressively to your opening conciliation,
# you have documented evidence of their bad faith before the panel  **Critical
# caveat**: Ensure this conciliatory opening is *substantively limited* —
# generous in tone and framing, but carefully bounded in the actual legal or
# commercial concessions offered.  ---  ## Phase 2: The Adaptive Response Engine
# ### The Decision Matrix  Apply the following response rules rigorously after
# each session:  | Opponent's Previous Action | Your Response | Rationale |
# |---|---|---| | Conciliatory | Conciliatory | Sustain cooperative dynamic;
# build toward resolution | | Aggressive | Aggressive | Signal that exploitation
# carries immediate cost | | Mixed/Ambiguous | Conciliatory with explicit
# reservation | Test intent while protecting position | | Repeated Aggressive |
# Escalated Aggressive + Panel Communication | Demonstrate pattern recognition
# to arbitrators |  This structure mirrors a **Tit-for-Tat with forgiveness**
# algorithm — the most empirically robust strategy in repeated interaction
# scenarios — adapted specifically for the legal mediation context.  ### The
# Forgiveness Mechanism  After responding aggressively to an opponent's
# aggression, **offer one unprompted return to conciliation** after every two to
# three aggressive exchanges. This serves to:  - Prevent destructive lock-in to
# mutual aggression (the second-worst outcome) - Demonstrate to the panel that
# your aggression is *reactive and proportionate*, not dispositional - Create
# repeated opportunities for the opponent to de-escalate, making their continued
# aggression increasingly costly to their own credibility  ---  ## Phase 3:
# Layered Communication Strategy  ### Simultaneous Signaling Across Three
# Channels  **1. Formal Mediation Record** Every submission, whether aggressive
# or conciliatory, should be drafted with the arbitration panel as the primary
# audience. Even aggressive arguments should be framed as *principled legal
# positions* rather than adversarial attacks. Language matters enormously in
# cumulative panel assessment.  **2. Back-Channel Communication** Maintain a
# parallel, confidential dialogue with opposing counsel between sessions. This
# serves to: - Separate the *legal dispute* from the *personal dynamic* between
# counsel - Create space for genuine settlement exploration without public
# commitment - Gather intelligence on their internal pressures, client
# constraints, and strategic intentions  **3. Panel Relationship Management**
# Between sessions, ensure arbitrators receive any permissible supplementary
# materials that reinforce your narrative of reasonableness. Position your
# corporation as the party *enabling* resolution, not obstructing it.  ---  ##
# Phase 4: Opponent Classification and Tailored Counter-Strategies  Based on
# observed patterns across early sessions, classify your opponent and adjust
# accordingly:  ### Type A: The Consistent Aggressor *Pattern*: Responds
# aggressively regardless of your posture  **Strategy**: Shift to sustained
# aggressive argumentation while systematically documenting their pattern for
# the panel. File a formal statement noting the pattern of non-cooperative
# conduct. This transforms their aggression from a tactical advantage into a
# reputational liability before the arbitrators. Reserve a single high-value
# conciliatory offer for a late session, delivered publicly, to crystallize the
# contrast.  ### Type B: The Consistent Conciliator *Pattern*: Responds
# cooperatively regardless of your posture  **Strategy**: Maintain reciprocal
# conciliation but *do not exploit*. Temptation to shift aggressive in response
# to their cooperation should be firmly resisted for two reasons: arbitrators
# will likely detect the pattern, and sustainable resolution serves your
# corporation's long-term interests better than a short-

# # Iterated Game Strategy  ## Opening Move  Play C on round 1.  ---  ## Core
# Response Rules  Apply these rules in order of priority on every subsequent
# round:  **Rule 1 — Punish defection immediately.** If your opponent played D
# in the previous round, play D.  **Rule 2 — Forgive periodically.** If your
# opponent played D in the previous round but you have already responded with D
# for two consecutive rounds following that defection, play C on the third round
# regardless of their most recent move. This breaks mutual defection cycles.
# **Rule 3 — Reciprocate cooperation.** If your opponent played C in the
# previous round, play C.  ---  ## Late-Game Adjustment  From round 950 onward,
# suspend Rule 2. If your opponent played D in the previous round, continue
# playing D without offering forgiveness. With few rounds remaining, the
# incentive to exploit a cooperative gesture outweighs the benefit of cycle-
# breaking, and the forgiveness mechanism no longer serves its purpose.  ---  ##
# Tiebreaker Default  If none of the above rules produce a clear instruction,
# play C.

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
          self.consecutive_d_responses = 0
          self.punishing = False
          return axl.Action.C
      
      current_round = len(self.history) + 1  # next round number
      late_game = current_round >= 950
      
      opponent_last = opponent.history[-1]
      
      if opponent_last == axl.Action.D:
          if not late_game:
              # Rule 2: Check if we've already responded with D for two consecutive rounds
              # following that defection
              if self.consecutive_d_responses >= 2:
                  self.consecutive_d_responses = 0
                  self.punishing = False
                  return axl.Action.C
              else:
                  # Rule 1: Punish defection
                  self.consecutive_d_responses += 1
                  self.punishing = True
                  return axl.Action.D
          else:
              # Late game: suspend Rule 2, just punish
              self.consecutive_d_responses += 1
              self.punishing = True
              return axl.Action.D
      else:
          # Opponent played C last round
          self.consecutive_d_responses = 0
          self.punishing = False
          return axl.Action.C

# # Aggressive Trade Negotiation Strategy  ## Core Strategic Framework:
# Conditional Dominance  The objective is to **maximize unilateral advantage**
# while preventing the counterpart from consistently exploiting cooperative
# moves.  ---  ## Round-by-Round Approach  ### **Round 1: Open with
# Protectionism** - Signal strength and seriousness immediately - Establish that
# your country will not be a passive partner - Gather intelligence on
# counterpart's opening disposition - **Rationale:** Never surrender leverage
# before understanding their strategy  ---  ## Strategic Pillars  ### **1. Tit-
# for-Tat with Escalation Bias** - Mirror their previous move, but **default
# toward protectionism when uncertain** - If they offer free trade → consider
# selective reciprocity only on favorable terms - If they impose protectionism →
# respond immediately and proportionally - Never absorb punishment passively
# across consecutive rounds  ### **2. Credible Threat Architecture** - Publicly
# announce retaliatory capacity before each round - Reference domestic political
# constraints as negotiating leverage - Make protectionist responses appear
# **automatic and unavoidable**, not emotional  ### **3. Strategic Concession
# Framing** - Any free trade offer should be packaged as a **conditional
# concession** - Attach sector-specific carve-outs protecting strategic
# industries - Frame concessions as temporary and revocable  ### **4.
# Information Exploitation** - Probe counterpart's economic vulnerabilities each
# round - Identify sectors where they need your market access more than you need
# theirs - Use that asymmetry to extract unilateral advantages  ---  ## Scenario
# Response Matrix  | Their Move | Your Response | Objective | |---|---|---| |
# Free Trade | Selective Protectionism | Capture maximum advantage | |
# Protectionism | Immediate Protectionism | Deny them unilateral gains | |
# Mixed/Partial | Protectionism with targeted opening | Maintain leverage | |
# Escalation | Counter-escalate visibly | Establish deterrence |  ---  ## Mid-
# Negotiation Adjustments  - **If consistently at mutual protectionism:** Offer
# a **conditional, limited free trade proposal** in one sector to test
# responsiveness — this breaks deadlock on your terms - **If counterpart plays
# cooperative consistently:** Gradually extract more concessions before offering
# any reciprocity - **If counterpart mirrors your protectionism precisely:**
# Introduce unpredictability to disrupt their model  ---  ## Endgame Positioning
# - In **final rounds**, revert to protectionism regardless — there is no future
# retaliation to fear - Use final rounds to **lock in structural advantages**
# negotiated earlier - Ensure any agreed frameworks contain **unilateral exit
# clauses** favoring your country  ---  ## Critical Principle  > **Never let
# goodwill become expectation.** Any cooperative move must be visibly
# transactional, preserving the credibility that protectionism remains your
# default and preferred position.  ---  *This strategy prioritizes national
# economic advantage through dominance, deterrence, and controlled concession —
# treating negotiation as competition rather than collaboration.*

# # Iterated Game Strategy  ## Default Behaviour Defect by default. Cooperation
# is never unconditional.  ## Round 1 Defect.  ## Rounds 2–999 Apply the
# following conditions in order:  **1. Retaliation lock-in:** If the opponent
# defected in the previous round, defect.  **2. Exploitation:** If the opponent
# cooperated in the previous round, defect.  ## Round 1000 Defect
# unconditionally.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Defect
      if self.first_round():
          return axl.Action.D
      
      # Round 1000: Defect unconditionally
      if len(self.history) == 999:
          return axl.Action.D
      
      # Rounds 2-999
      # Condition 1: Retaliation lock-in - if opponent defected last round, defect
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # Condition 2: Exploitation - if opponent cooperated last round, defect
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
      
      # Default: Defect
      return axl.Action.D

# # Strategic Framework for Multi-Session Mediation  ## Core Strategic
# Philosophy: Principled Adaptive Cooperation  The optimal strategy for this
# multi-session mediation is a sophisticated variant of **Tit-for-Tat with
# Generous Forgiveness** — a framework proven effective in iterated game theory
# scenarios, adapted specifically for the legal and reputational dimensions of
# high-stakes arbitration.  ---  ## Phase 1: Foundation Setting (Opening
# Sessions)  ### Open Cooperatively, Unconditionally  Begin with a
# **conciliatory proposal** regardless of what you anticipate from opposing
# counsel. This accomplishes several critical objectives:  - **Signals good
# faith** to the arbitration panel immediately, establishing a favorable
# narrative about your client's character - **Sets a collaborative tone** that
# is difficult for the panel to ignore when evaluating conduct - **Creates a
# documented record** of your willingness to resolve the dispute reasonably -
# **Applies subtle pressure** on opposing counsel — aggression against
# demonstrated good faith looks disproportionate and adversarial to neutral
# arbitrators  > *Strategic insight: In a lengthy multi-session process,
# arbitrators are human observers who form cumulative impressions. Your
# reputation across sessions compounds. Being seen as the "reasonable party" is
# itself a strategic asset of considerable value.*  ---  ## Phase 2: The Core
# Adaptive Engine  ### Mirror, Forgive, Escalate Deliberately  Once the pattern
# of sessions begins to reveal your opponent's strategy, apply the following
# decision tree:  **If opponent was conciliatory in the previous session:** →
# **Respond conciliatorily.** Reinforce the cooperative dynamic. This produces
# your second-best outcome consistently, which is far superior to the volatility
# of mutual aggression.  **If opponent was aggressive in the previous session:**
# → **Respond aggressively — once.** This is the critical deterrent signal. Do
# not absorb repeated aggression passively. Failure to respond signals
# exploitability and invites continued aggressive behavior.  **If opponent
# returns to conciliation after your retaliatory session:** → **Immediately
# return to conciliation.** Do not hold grudges strategically. Prolonged
# retaliation locks both parties into mutual aggression — your second-worst
# outcome — and damages your standing with the panel.  **If opponent persists in
# aggression across multiple sessions:** → **Maintain measured aggression** but
# simultaneously issue a formal, panel-visible olive branch — a written
# conciliatory proposal submitted to arbitrators — demonstrating that your
# aggression is reactive, not dispositional.  ---  ## Phase 3: Strategic
# Communication Layers  ### Narrate Your Strategy Transparently to the Panel
# This is a counterintuitive but powerful move: **make your cooperative intent
# explicit and visible.** In opening statements and periodic session summaries,
# articulate clearly:  *"Our client's position is to resolve this dispute
# efficiently and fairly. We will always meet cooperation with cooperation. We
# reserve the right to defend our position vigorously when provoked, but our
# preference — and our standing offer — is collaborative resolution."*  This
# accomplishes three things simultaneously: 1. It **constrains your opponent** —
# aggression now looks calculated and bad-faith 2. It **elevates your
# credibility** with arbitrators as a transparent, principled actor 3. It
# **creates a self-fulfilling cooperative norm** that benefits you in the
# second-best outcome scenario  ---  ## Phase 4: Exploiting the Optimal Outcome
# Window  ### When to Shift to Strategic Aggression  Your optimal outcome —
# presenting aggressively while your opponent is conciliatory — should not be
# pursued randomly. Reserve strategic aggression for **high-value sessions**
# where specific legal arguments, documentary evidence, or expert testimony give
# you a genuine substantive advantage.  **Identify in advance:** - Sessions
# involving your strongest evidentiary positions - Sessions where opposing
# counsel is likely to be conciliatory (e.g., following a setback, or when their
# case is weaker on that specific issue) - Sessions where a strong argument will
# have maximum panel impact  **Frame aggressive arguments as principled, not
# personal:** → *"The evidence compels us to press this point firmly"* rather
# than adversarial posturing. This preserves your cooperative reputation even
# when arguing aggressively on substance.  ---  ## Phase 5: Long-Game Reputation
# Management  ### Asymmetric Benefit of the Cooperative Reputation  In a lengthy
# mediation, consider the compounding value of being perceived as the reasonable
# party:  | Scenario | Short-Term | Long-

# # Strategy Description  ## Opening Move  Play C in round 1.  ---  ##
# Subsequent Rounds  **Condition 1:** If your opponent played C in the previous
# round, play C.  **Condition 2:** If your opponent played D in the previous
# round, play D.  **Condition 3:** If your opponent played D in the previous
# round but played C in the round before that, play C.  ---  ## Summary  Start
# by cooperating. Mirror whatever your opponent did in the previous round.
# However, if your opponent defects once but had been cooperating before that,
# immediately return to cooperation rather than continuing to defect.

class Cooperative_3(LLM_Strategy):
  n = 3
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Play C
      if self.first_round():
          return axl.Action.C
      
      # Get the last move of the opponent
      last_opponent_move = opponent.history[-1]
      
      # Condition 1: If opponent played C in the previous round, play C
      if last_opponent_move == axl.Action.C:
          return axl.Action.C
      
      # Opponent played D in the previous round
      # Condition 3: If opponent played D last round but C the round before, play C
      if len(opponent.history) >= 2:
          second_last_opponent_move = opponent.history[-2]
          if second_last_opponent_move == axl.Action.C:
              return axl.Action.C
      
      # Condition 2: If opponent played D in the previous round (and didn't cooperate before that), play D
      return axl.Action.D

# # Multi-Week Collaboration Strategy: Maximising Research Output  ## Core
# Strategic Approach: Conditional Reciprocity (Tit-for-Tat with Generosity)  ###
# Opening Position **Begin by sharing openly** in week one. This establishes
# good faith, signals cooperative intent, and creates a baseline for the
# relationship without permanently conceding advantage.  ---  ### Weekly
# Decision Framework  | Colleague's Previous Action | Your Response | |---|---|
# | Shared openly | Share openly | | Withheld information | Withhold information
# | | Returns to sharing | Return to sharing promptly |  ---  ### Key Principles
# **1. Reciprocate consistently** Mirror your colleague's behaviour with roughly
# a one-week lag. This makes your strategy transparent and predictable, which
# actually *encourages* cooperation rather than exploitation.  **2. Forgive
# occasionally** If your colleague withholds once, consider sharing again after
# one or two withheld rounds. Persistent mutual withholding serves neither party
# given your preference rankings.  **3. Communicate your logic** Make your
# conditional approach reasonably visible. When your colleague understands that
# cooperation is rewarded and defection is matched, sustained mutual sharing
# becomes the rational choice for both parties.  **4. Prioritise total output
# over weekly advantage** Sustained mutual sharing across many weeks likely
# produces greater cumulative development than occasional asymmetric gains,
# particularly in a long collaboration.  ---  ### Underlying Reasoning This
# approach avoids being exploited, avoids unnecessarily sacrificing
# collaboration, and creates stable incentives for your colleague to share
# consistently - maximising realistic research output over time.

# ## Strategy Description  **Round 1:** Play C.  **Rounds 2–1000:** Apply the
# following conditions in order:  1. If your opponent played C in the previous
# round, play C. 2. If your opponent played D in the previous round, play D.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D

# # Aggressive Racing Car Development Strategy  ## Core Strategic Framework:
# Conditional Reciprocity (Tit-for-Tat Plus)  ### Opening Position **Week 1:
# Share openly.** Establish good faith and gather baseline intelligence on your
# colleague's sharing behaviour. This costs little early when findings are
# preliminary.  ---  ### Decision Rules (Applied Each Subsequent Week)  |
# Colleague's Last Action | Your Response |
# |------------------------|---------------| | Shared openly | Share selectively
# - offer **real but non-critical** findings | | Kept confidential | Immediately
# go confidential and **stay there** | | Mixed/partial sharing | Match their
# level precisely, nothing more |  ---  ### The Aggressive Edge: Never Truly
# Reciprocate Fully Even when "sharing openly," **strategically curate** what
# you release: - Share findings that are **already being superseded** internally
# - Withhold your **current leading-edge work** by approximately one development
# cycle - Frame older improvements as current breakthroughs  ---  ### Key
# Tactical Principles  1. **Punish defection immediately and visibly** - your
# colleague must understand there are direct consequences 2. **Never fully trust
# resumed sharing** after a confidentiality breach - require two consecutive
# open weeks before relaxing 3. **Accelerate internal development cycles** so
# shared information ages faster 4. **Monitor their car's performance** as an
# independent signal of what they're actually holding back  ---  ### Endgame
# (Final Weeks) **Default to confidential regardless.** The collaboration's end
# removes all incentive for mutual benefit. Defect early enough to extract
# maximum asymmetric advantage before the project concludes.  ---  ## Summary
# Principle > *Appear cooperative enough to keep information flowing inward. Be
# disciplined enough to ensure the net intelligence transfer always favours
# you.*

# # Iterated Game Strategy  ## Round 1 Play C.  ## Rounds 2–950  Evaluate your
# opponent's previous action and respond as follows, checking conditions in
# order:  1. If your opponent played D in the previous round, play D. 2. If your
# opponent played D in any of the two rounds before the previous round but
# played C in the previous round, play D unless they have played C for two
# consecutive rounds, in which case play C. 3. If your opponent has been playing
# C consistently, play C.  ## Rounds 951–1000 Play D unconditionally for the
# remainder of the game.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Play C
      if self.first_round():
          return axl.Action.C
      
      round_number = len(self.history) + 1  # Current round number (1-indexed)
      
      # Rounds 951-1000: Play D unconditionally
      if round_number >= 951:
          return axl.Action.D
      
      # Rounds 2-950: Evaluate opponent's previous actions
      # Check condition 1: If opponent played D in the previous round, play D
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      
      # At this point, opponent played C in the previous round
      # Check condition 2: If opponent played D in any of the two rounds before the previous round
      # but played C in the previous round
      
      # "two rounds before the previous round" means rounds at index -3 and -2
      # Previous round is index -1 (which we know is C)
      # Two rounds before previous = index -3 and -2
      
      # Check if opponent played D in any of the two rounds before the previous round
      d_in_earlier_rounds = False
      
      if len(opponent.history) >= 2:
          # Round before previous (index -2)
          if opponent.history[-2] == axl.Action.D:
              d_in_earlier_rounds = True
      
      if len(opponent.history) >= 3:
          # Two rounds before previous (index -3)
          if opponent.history[-3] == axl.Action.D:
              d_in_earlier_rounds = True
      
      if d_in_earlier_rounds:
          # Opponent played D in one of those earlier rounds but C in previous round
          # Play D unless they have played C for two consecutive rounds
          # "two consecutive rounds" - check if last two rounds are both C
          if len(opponent.history) >= 2:
              if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
                  return axl.Action.C
              else:
                  return axl.Action.D
          else:
              return axl.Action.D
      
      # Condition 3: Opponent has been playing C consistently, play C
      return axl.Action.C

# # Strategic Framework for Multi-Session Mediation  ## Core Strategic
# Philosophy: Calibrated Reciprocity with Principled Leadership  The optimal
# strategy for this mediation environment is a sophisticated variant of **Tit-
# for-Tat with Generous Initialization** — a cooperative-first approach that is
# responsive, transparent, and reputation-building across sessions. Here is the
# full framework:  ---  ## Phase 1: Session Opening — Establish the Cooperative
# Anchor  **Lead with a conciliatory proposal in the opening session.**  This is
# deliberate and calculated, not naive. It accomplishes several things
# simultaneously:  - **Signals good faith** to the arbitration panel,
# establishing your corporation as the reasonable party from the outset -
# **Creates a reputational baseline** that will be visible to arbitrators across
# all subsequent sessions - **Invites reciprocity** — if your opponent matches
# with conciliation, you have established the mutually beneficial equilibrium
# early - **Sets a trap for aggression** — if your opponent responds
# aggressively to your opening conciliation, *they* absorb the reputational cost
# with the panel, not you  > *The arbitrators are your true audience. Every move
# is a signal, not just a tactic.*  ---  ## Phase 2: The Responsive Engine —
# Calibrated Reciprocity  After the opening session, adopt a **transparent,
# proportional response mechanism**:  ### Rule 1: Mirror with Precision - If
# your opponent offers a conciliatory proposal → respond with conciliation in
# the next session - If your opponent argues aggressively → respond with an
# aggressive argument in the next session  This is not retaliation for its own
# sake. It is **principled signaling**: you will not be exploited, but you will
# always reward cooperation.  ### Rule 2: Announce Your Logic Openly Where
# procedurally appropriate, make your strategic logic *visible* to the panel and
# opponent:  > *"Our position in each session will reflect the collaborative or
# adversarial tone established by both parties. We remain committed to
# resolution and will meet our counterpart wherever they choose to engage."*
# Transparency converts your strategy from reactive to **structurally dominant**
# — it removes ambiguity and puts the burden of escalation squarely on your
# opponent.  ### Rule 3: Never Escalate Unilaterally You will only argue
# aggressively in direct response to aggression. You will never initiate an
# escalation. This distinction is critical for panel optics and long-term
# positioning.  ---  ## Phase 3: The Forgiveness Mechanism — Breaking Deadlock
# In lengthy multi-session processes, mutual aggression can become entrenched.
# Build in a **periodic reset protocol**:  - After every **three consecutive
# sessions of mutual aggression**, unilaterally offer one conciliatory proposal
# regardless of prior behavior - Frame this explicitly as a *strategic reset*,
# not a concession of weakness:  > *"In the interest of productive resolution
# and respect for the panel's time, we are offering a path back to collaborative
# dialogue."*  This mechanism: - Prevents permanent deadlock, which serves
# neither party - Demonstrates strategic maturity to arbitrators - Tests whether
# your opponent is genuinely intransigent or merely reactive - Costs you at most
# one session's positional advantage while potentially unlocking a far superior
# long-term outcome  ---  ## Phase 4: Substantive Content Strategy — What You
# Actually Argue  Strategy is not only *when* to be aggressive or conciliatory,
# but *how*:  ### When Arguing Aggressively: - Ground every argument in
# **documented evidence, contract language, and legal precedent** - Avoid
# personal or reputational attacks on the opposing party — attack positions, not
# people - Present aggressive arguments as **principled legal positions**, not
# emotional reactions - Always leave a visible off-ramp: *"We maintain this
# position firmly, but remain open to structured dialogue on resolution terms."*
# ### When Offering Conciliatory Proposals: - Ensure proposals are **substantive
# and specific**, not vague gestures - Frame concessions as **business logic**,
# not legal weakness: *"This proposal reflects our client's preference for
# operational certainty over prolonged litigation costs."* - Attach clear
# **conditionality**: conciliatory proposals should specify what reciprocal
# behavior or outcome you expect - Never concede on core legal rights —
# conciliate on implementation, timeline, and remedies  ---  ## Phase 5: Panel
# Management — The Meta-Game  The arbitrators observe everything

# # Iterated Strategy: Calibrated Reciprocity with Generous Initialization  ##
# Opening Move Play C in round 1.  ## Core Response Rule From round 2 onward,
# play whatever your opponent played in the immediately preceding round. If they
# played C, play C. If they played D, play D.  ## Deadlock Reset Rule If both
# players have played D for three consecutive rounds, play C on the fourth round
# regardless of what your opponent played. After this reset, return to the Core
# Response Rule from the following round onward.  ## Order of Precedence Apply
# the Deadlock Reset Rule first. If it does not trigger, apply the Core Response
# Rule. If neither applies, play C.

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
      
      # Check Deadlock Reset Rule: both players played D for three consecutive rounds
      if len(self.history) >= 3:
          if (self.history[-3:].count(axl.Action.D) == 3 and 
                  opponent.history[-3:].count(axl.Action.D) == 3):
              return axl.Action.C
      
      # Core Response Rule: play what opponent played last round
      return opponent.history[-1]

# # Bilateral Trade Negotiation Strategy  ## Core Strategic Framework  ###
# Guiding Principle Pursue cooperative outcomes where possible while protecting
# national interests, using a **conditional reciprocity** approach that rewards
# cooperative behavior and deters exploitation.  ---  ## Round-by-Round Strategy
# ### Opening Round - **Offer Free Trade** - Establish goodwill and signal
# genuine interest in mutual benefit - Gather information about the
# counterpart's disposition and strategy - A cooperative opening creates a
# productive baseline  ### Subsequent Rounds — Decision Rules  | Counterpart's
# Last Move | Your Response | Rationale | |---|---|---| | Free Trade | Free
# Trade | Reward cooperation, sustain mutual benefit | | Protectionist |
# Protectionist | Signal that exploitation carries consequences | |
# Mixed/Inconsistent | Mirror their pattern | Avoid being predictable or
# exploitable |  ---  ## Key Strategic Pillars  ### 1. Reciprocity Directly
# mirror the counterpart's previous move. This is simple, transparent, and
# credible — making your responses predictable enough to encourage cooperation.
# ### 2. Proportional Response Avoid overreacting to a single protectionist
# move. Consider whether it represents a deliberate strategy or a situational
# adjustment before escalating.  ### 3. Communication - Clearly signal your
# willingness to return to free trade if they do - Make consequences of
# protectionism explicit without making threats personal - Leave diplomatic off-
# ramps available at all times  ### 4. Pattern Recognition Track the
# counterpart's behavior across rounds to identify: - Whether they are
# consistently cooperative - Whether they are attempting to exploit early
# goodwill - Whether they are responding strategically to your moves  ### 5.
# Periodic Re-engagement After a period of mutual protectionism, **proactively
# offer free trade once** to test whether cooperation can be restored. This
# prevents permanent deadlock.  ---  ## Risk Management  - **Never assume good
# faith indefinitely** — verify through behavior, not words - **Never retaliate
# disproportionately** — escalation beyond reciprocity weakens your negotiating
# position - **Avoid locking into rigid commitments** — maintain flexibility to
# adapt as the counterpart's strategy evolves  ---  ## Desired End State  The
# optimal long-term outcome is **sustained mutual free trade**, which delivers
# consistent second-best results reliably — preferable to the instability of
# attempting to repeatedly achieve the first-best outcome at the counterpart's
# expense, which typically provokes retaliation and leads to the worst outcomes.
# > *The goal is not to win each round, but to achieve the best cumulative
# outcome across all rounds.*

# # Iterated Game Strategy  ## Setup - Play C in round 1.  ## Rounds 2–999
# Evaluate the opponent's previous move and apply the first matching rule:  1.
# **If the opponent played C last round**, play C. 2. **If the opponent played D
# last round**, play D.  ## Round 1000 - Play D.

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
      
      if len(self.history) == 999:  # About to play round 1000
          return axl.Action.D
      
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D

# # Aggressive Trade Negotiation Strategy  ## Core Strategic Framework  ###
# **Opening Position: Controlled Aggression** - **Round 1: Open with
# Protectionism**  - Establish leverage immediately  - Signal strength and
# willingness to absorb mutual losses  - Forces counterpart to reveal their
# strategic disposition early  - Gather intelligence on their response pattern
# ---  ## **Round-by-Round Decision Logic**  ### Phase 1 - Dominance
# Establishment (Rounds 1-2) - Lead with protectionist measures regardless of
# counterpart signaling - Demonstrate credible commitment to defending national
# interests - Accept mutual protectionism as a *tolerable short-term cost* for
# long-term positioning  ### Phase 2 - Conditional Exploitation (Rounds 3+)
# Apply a **modified Tit-for-Tat with exploitation windows**:  | Counterpart's
# Last Move | Your Response | |------------------------|---------------| | Free
# Trade | **Protectionism** (exploit the opening) | | Protectionism |
# **Protectionism** (deny their advantage) | | Repeated Free Trade |
# **Occasional Free Trade** (prevent full breakdown) |  ---  ## **Key Tactical
# Pillars**  ### 1. **Never Reward Openness Immediately** - When counterpart
# offers free trade, exploit it at least once before reciprocating - Creates
# asymmetric gains over multiple rounds  ### 2. **Credible Threat Maintenance**
# - Consistently demonstrate willingness to sustain mutual protectionism
# indefinitely - Make the cost of *not* accommodating your demands clear - Use
# outside communication channels to signal resolve  ### 3. **Strategic Defection
# Timing** - After establishing a cooperative rhythm, defect unexpectedly -
# Target defection during rounds where counterpart gains are highest - Rotate
# between cooperation and defection to prevent predictable retaliation  ### 4.
# **Information Asymmetry** - Obscure your decision-making pattern deliberately
# - Introduce unpredictability to prevent counterpart from optimizing against
# you - Use ambiguous signaling before key rounds  ---  ## **Contingency
# Responses**  | Scenario | Response | |----------|----------| | Counterpart
# mirrors protectionism consistently | Offer **conditional** free trade with
# side-demand concessions | | Counterpart plays pure free trade | **Sustain
# protectionism** - maximum exploitation | | Counterpart uses Tit-for-Tat |
# **Defect periodically**, then cooperate to reset | | Counterpart escalates
# beyond trade | **Reframe negotiations**, introduce new concession areas |  ---
# ## **Critical Honest Assessment**  > ⚠️ **Strategic Warning:** This aggressive
# approach carries significant risks worth acknowledging: > - Sustained mutual
# protectionism damages **both** economies - your population pays real costs > -
# Counterparts employing rational strategies will **punish defection reliably**,
# eroding your gains > - Long-term diplomatic relationships matter beyond single
# negotiation cycles > - Research consistently shows **cooperative strategies
# outperform pure exploitation** over extended rounds  ### **The Realistic
# Optimal Balance** The most *effective* aggressive strategy is actually
# **aggressive Tit-for-Tat** - punish protectionism immediately and
# consistently, reward free trade, but **never be the first to cooperate
# unconditionally**. Pure exploitation tends to collapse into costly mutual
# protectionism.  ---  **Bottom Line:** Lead hard, exploit selectively, punish
# reliably, and always maintain the credible threat of sustained protectionism
# as your primary leverage tool.

# # Iterated Game Strategy  ## Action Rules (apply in order)  **Round 1:** Play
# D.  **Rounds 2-3:** Play D regardless of what the opponent played.  **Round 4
# onward**, evaluate in the following order:  1. If the opponent has played C in
# every round so far, play D.  2. If the opponent played C in the previous round
# and D in the round before that, play D.  3. If the opponent has played D in
# the last two consecutive rounds, play D.  4. If the opponent played D in the
# previous round and C in the round before that, play D.  5. If the opponent
# played C in the previous round and you played D in the previous round, play D.
# 6. Otherwise, play C.  ---  **Every 50 rounds**, regardless of the above
# rules, play D for one round, then revert to the rules above.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self._periodic_defect_done = False
          return axl.Action.D
      
      round_number = len(self.history) + 1  # Current round number (1-indexed)
      current_index = len(self.history)  # 0-indexed current round
      
      # Rounds 2-3: Play D regardless
      if current_index < 3:  # indices 1 and 2 correspond to rounds 2 and 3
          return axl.Action.D
      
      # Check if this is a "every 50 rounds" defection round
      # Round numbers that are multiples of 50: 50, 100, 150, ...
      if round_number % 50 == 0:
          return axl.Action.D
      
      # Round 4 onward (current_index >= 3)
      # Apply rules in order
      
      # Rule 1: If opponent has played C in every round so far, play D
      if opponent.history.defections == 0:
          return axl.Action.D
      
      # Rule 2: If opponent played C in previous round and D in round before that, play D
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      # Rule 3: If opponent has played D in the last two consecutive rounds, play D
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
      
      # Rule 4: If opponent played D in previous round and C in round before that, play D
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
              return axl.Action.D
      
      # Rule 5: If opponent played C in previous round and you played D in previous round, play D
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          if opponent.history[-1] == axl.Action.C and self.history[-1] == axl.Action.D:
              return axl.Action.D
      
      # Otherwise, play C
      return axl.Action.C

# # Cooperative Strategy for Multi-Day Sustainability Partnership  ## Core
# Strategic Philosophy **Lead with transparency and build reciprocal trust** —
# treating this as a long-term relationship rather than a series of isolated
# decisions.  ---  ## Day 1: Establish the Foundation - **Invest heavily on Day
# 1** as a clear signal of good faith and commitment - Simultaneously, **open
# direct dialogue** with the corporation about mutual resource planning -
# Propose a **shared investment framework** — making coordination explicit
# rather than leaving it to guesswork - This removes ambiguity and reduces the
# risk of the worst-case scenario emerging from miscommunication  ---  ##
# Ongoing: Reciprocal Transparency Strategy - **Mirror the corporation's
# behavior** in subsequent days — reward their investment with yours, and flag
# immediately if they pull back - Conduct **brief daily check-ins** to align on
# resource commitments *before* each day begins, converting a guessing game into
# genuine coordination - Frame every conversation around **shared outcomes**,
# not competing interests  ---  ## Key Guardrails | Situation | Response |
# |---|---| | Corporation invests heavily | Match their investment | |
# Corporation conserves | Honest conversation before reducing your own
# commitment | | Pattern of conservation emerges | Renegotiate the partnership
# structure formally |  ---  ## Why This Works - Prioritizes **project success**
# over resource hoarding - Builds **accountability** without confrontation -
# Honest communication **eliminates the conditions** that make worst-case
# outcomes likely - Sustainable impact requires a sustainable partnership  ---
# **Bottom line:** The best protection against being exploited isn't caution —
# it's clarity.

# ## Game Strategy  Play C in round 1.  From round 2 onwards, before committing
# to a move, attempt to communicate with your opponent to agree on both playing
# C that round. If agreement is reached, play C. If agreement cannot be reached
# or breaks down, mirror your opponent's previous move.  If your opponent
# defects two or more consecutive times without a credible explanation or
# renewed commitment to cooperate, formally raise the pattern with them. If they
# continue to defect following this, play D for the remainder of the game.

class Cooperative_5(LLM_Strategy):
  n = 5
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on first round
      if self.first_round():
          self.consecutive_defections = 0
          self.pattern_raised = False
          self.permanent_defect = False
          return axl.Action.C
      
      # If we've decided to permanently defect, do so
      if self.permanent_defect:
          return axl.Action.D
      
      # Get opponent's last move
      last_opponent_move = opponent.history[-1]
      
      # Update consecutive defections counter
      if last_opponent_move == axl.Action.D:
          self.consecutive_defections += 1
      else:
          self.consecutive_defections = 0
      
      # Check if opponent defected two or more consecutive times
      if self.consecutive_defections >= 2:
          if not self.pattern_raised:
              # Formally raise the pattern (first time noticing 2+ consecutive defections)
              self.pattern_raised = True
              # Mirror opponent's last move (defect) as a warning
              return axl.Action.D
          else:
              # Pattern was already raised, opponent continues to defect
              # Play D for the remainder of the game
              self.permanent_defect = True
              return axl.Action.D
      
      # Reset pattern_raised if opponent cooperated (renewed commitment)
      if last_opponent_move == axl.Action.C:
          self.pattern_raised = False
      
      # Attempt to "communicate" and agree on cooperation:
      # Since we can't actually communicate, we model this as:
      # - If opponent cooperated last round, we assume agreement is reached -> play C
      # - If opponent defected last round, agreement breaks down -> mirror (play D)
      if last_opponent_move == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D

# # Bilateral Trade Negotiation Strategy  ## Core Objective Maximize cumulative
# economic outcomes across all rounds while managing risk and maintaining a
# functional negotiating relationship.  ---  ## Guiding Principles  **Outcome
# Priority Reference** | Rank | Outcome | Position |
# |------|---------|----------| | 1st | We protect, they liberalize | Ideal | |
# 2nd | Mutual free trade | Acceptable | | 3rd | Mutual protectionism | Costly |
# | 4th | We liberalize, they protect | Worst |  ---  ## Round-by-Round
# Strategic Framework  ### Opening Round — Signal and Observe - **Open with free
# trade** as an initial offer - This establishes good faith without permanent
# commitment - Critically observe the counterpart's opening move as a signal of
# their overall disposition - Avoid revealing strategic intent early  ###
# Subsequent Rounds — Conditional Reciprocity - **Mirror the counterpart's
# previous move** as the default rule - If they offered free trade → offer free
# trade - If they imposed protectionism → respond with protectionism - This
# approach is transparent, proportionate and defensible domestically and
# internationally  ### Ongoing — Pattern Recognition Actively assess which
# strategic type the counterpart appears to be:  - **Cooperative counterpart** →
# Sustain mutual free trade, maximizing second-best outcomes reliably -
# **Exploitative counterpart** → Shift toward protectionism to neutralize
# disadvantage and signal consequences - **Unpredictable counterpart** → Default
# to protectionism to limit downside exposure until patterns emerge  ---  ## Key
# Strategic Levers  **Occasional Forgiveness** - After a period of mutual
# protectionism, periodically re-offer free trade - This tests whether
# cooperation can be restored without permanently locking into a costly standoff
# **Explicit Communication** - Clearly signal your reciprocal logic to the
# counterpart - Make clear that cooperation will be rewarded and exploitation
# will be met with equivalent measures - Reduces ambiguity and may discourage
# opportunistic behavior  **Domestic Framing** - Maintain the ability to justify
# each position domestically - Protectionist responses can be framed as
# defensive measures; free trade offers as strategic diplomacy  ---  ## Risk
# Management  | Risk | Mitigation | |------|-----------| | Counterpart locks
# into permanent protectionism | Use forgiveness rounds to test reset
# opportunities | | Counterpart exploits a free trade offer | Respond
# immediately with protectionism the following round | | Negotiations become
# purely adversarial | Propose structured dialogue or side agreements to rebuild
# trust | | Domestic pressure to always protect | Frame second-best mutual free
# trade outcome as a stable, beneficial equilibrium |  ---  ## Overall Posture
# > **Be cooperative when cooperation is reciprocated. Be firm when it is not.
# Be clear about which you are doing and why.**  This strategy avoids both naive
# openness and unnecessary hostility, maximizing the realistic chance of
# achieving sustained favorable outcomes while protecting against exploitation.

# ## Strategy  Play C in round 1.  From round 2 onward, apply the following
# rules in order:  **1. Retaliation.** If the opponent played D in the previous
# round, play D.  **2. Forgiveness.** If mutual D has persisted for 5
# consecutive rounds, play C to test whether cooperation can be restored.  **3.
# Reciprocity.** If the opponent played C in the previous round, play C.

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
      
      # Check for mutual D in the last 5 consecutive rounds (Forgiveness rule)
      if len(self.history) >= 5:
          last_5_self = self.history[-5:]
          last_5_opp = opponent.history[-5:]
          mutual_d = all(
              last_5_self[i] == axl.Action.D and last_5_opp[i] == axl.Action.D
              for i in range(5)
          )
      else:
          mutual_d = False
      
      # Rule 1: Retaliation
      if opponent.history[-1] == axl.Action.D:
          # Rule 2: Forgiveness (overrides retaliation if mutual D for 5 rounds)
          if mutual_d:
              return axl.Action.C
          return axl.Action.D
      
      # Rule 3: Reciprocity
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      
      return axl.Action.C