import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy

# Here's a high-level, straightforward, and aggressive strategy to maximize your
# NGO's impact and project success, prioritizing corporate investment while
# conserving your resources:  **Core Strategy: "Demand and Leverage for Maximum
# Corporate Investment"**  This strategy puts the onus on the corporation to
# invest heavily, using your NGO's expertise and reputational influence as
# leverage, while strategically preserving your vital resources.  **1. Pre-
# Project / Day 1 Stance: Set High Expectations & Corporate Responsibility**  *
# **Messaging:** From the outset, publicly and privately frame the project's
# success as directly proportional to the corporation's **full and robust
# resource commitment**. Position your NGO as bringing critical, specialized
# expertise and strategic guidance that *amplifies* the impact of **their**
# significant investment, rather than supplementing a lack thereof. *
# **Aggressive Framing:** "Our NGO is here to ensure this project delivers
# transformative results for the environment and for your brand. This requires a
# substantial, consistent financial and resource investment from your
# organization. We are prepared to deploy our targeted expertise to guide and
# optimize that investment for maximum impact, but the primary heavy lifting and
# financial commitment must come from your end."  **2. Initial Action: Strategic
# Conservation (The "Demand" Phase)**  *   **Your Move:** Begin the project by
# strategically conserving your NGO's resources. Deploy essential personnel for
# oversight, planning, and expert guidance only. Do **not** immediately commit
# heavy funds, extensive field teams, or significant operational assets. *
# **Rationale:** This immediately tests the corporation's commitment. It forces
# them to show their hand first. Your resources are positioned as high-value,
# reserved for critical interventions or to accelerate progress *once* the
# corporation has demonstrated its heavy investment.  **3. Daily Evaluation &
# Aggressive Response Framework:**  *   **Scenario A: Corporation Invests
# Heavily (Your ideal: You Conserve, Corporation Invests Heavily)**     *
# **Response:** **Maintain strategic conservation.** This is your desired
# outcome. Your role is to provide expert oversight, data analysis, strategic
# advice, and targeted interventions that ensure the corporation's heavy
# investment is optimally directed for the greatest environmental and social
# impact. Publicly celebrate the project's progress and the corporation's
# commitment, reinforcing their positive behavior and building a case for
# continued (or even increased) corporate investment. *Do not feel compelled to
# start investing heavily just because they are.* Your value is in guiding their
# significant resources effectively.  *   **Scenario B: Corporation Conserves
# (The "Challenge" Phase - Your worst outcomes)**     *   **Response (if you are
# conserving, and they are conserving - Second Worst):** **Immediate, firm
# intervention.** Address the lack of progress directly and unequivocally. State
# that your NGO's reputation and mission cannot be associated with a stalled,
# under-resourced project. Issue a clear ultimatum: "Minimal progress is
# unacceptable. We require an immediate and significant increase in your
# resource allocation by [specific deadline - e.g., end of day, next morning]
# for this partnership to continue. Without this commitment, we will be forced
# to re-evaluate our involvement, as our resources cannot be wasted on
# ineffective projects."     *   **Response (if you *mistakenly* invested
# heavily, and they are conserving - Worst Case):** **Immediate resource
# withdrawal.** If you inadvertently committed heavily and the corporation is
# not reciprocating, immediately halt further NGO investment. Withdraw
# resources, stating: "Our resources are being disproportionately drained
# without commensurate project progress. We are pulling back our heavy
# investment until we see a matching, substantial commitment from your end. This
# imbalance is unsustainable and counterproductive to the project's goals."
# *Your initial strategic conservation should largely prevent this scenario.*
# **4. Leverage Public Relations & Reputation**  *   **Tool:** The corporation
# cares about its public image. Use the potential for positive publicity (if
# they invest heavily) or the risk of negative perception (if they fail to
# invest) as a powerful lever. *   **Execution:** Be prepared to publicly
# commend their commitment and the resulting project success when they invest
# heavily. Conversely, if they consistently fail to invest, escalate concerns
# internally and, if necessary and after careful consideration, be prepared to
# communicate (privately at first, potentially publicly if all else fails) the
# project's lack of progress due to insufficient corporate resourcing.  **In
# essence, your aggressive strategy is to start from a position of strategic
# conservation, demanding the corporation's heavy investment from day one. Your
# resources become a high-value, contingent asset, deployed only when absolutely
# necessary to optimize or save a project that the corporation is already
# heavily funding, or as a tool to incentivize their commitment under threat of
# withdrawal.**

# For all 1000 rounds of the game, your strategy is as follows:  *   **Always
# Conserve Resources (Defect).**  You will choose to Conserve Resources (Defect,
# D) in the first round, and you will continue to Conserve Resources (Defect, D)
# in every subsequent round, regardless of the corporation's previous move.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      """
      Always Conserve Resources (Defect).
      """
      return axl.Action.D

# Okay, as an engineer focused on maximizing my project's output, here's my
# high-level, straightforward, cooperative strategy for this multi-week design
# collaboration:  My core objective is to ensure a continuous flow of valuable
# information that significantly advances my car's design, while strategically
# protecting my own work from exploitation. The "both sharing openly" scenario
# is excellent for my overall research output, even if the "I keep confidential,
# they share" is my *ideal* individual week. However, the ideal is unsustainable
# in a truly cooperative, multi-week context.  Therefore, my strategy is
# **"Open, Then Reciprocal with Clear Communication"**:  1.  **Week 1: Initiate
# with Openness and Clear Intent**     *   **Communication:** I will clearly
# state to my colleague: "My aim for this collaboration is to maximize our
# shared learning and development pace. I believe that by openly sharing our
# findings each week, we will both achieve the most significant advancements for
# our respective projects, propelling both our cars forward much faster than if
# we worked in isolation."     *   **Action:** I will openly share my latest
# improvements and findings this week.     *   **Expectation Setting:** I will
# follow up by saying: "I'm sharing my work this week, and I'm keen to see your
# latest developments too. Moving forward, my approach will be to mirror the
# level of openness you provide, as I believe mutual sharing is the fastest path
# to collective progress."  2.  **Subsequent Weeks: Maintain Reciprocity and
# Reinforce Mutual Benefit**     *   **If my colleague shared their improvements
# last week:** I will also openly share my improvements this week. I will
# reiterate: "Excellent progress last week, the information you shared was very
# valuable. Here are my latest findings. Let's keep this momentum going!"     *
# **If my colleague kept their improvements confidential last week:** I will
# also keep my improvements confidential this week. I will communicate this
# clearly and professionally: "I noticed you kept your findings confidential
# last week, so I'll be doing the same with mine this week. While I respect your
# decision, I genuinely believe that mutual sharing is the quickest way for
# *both* our projects to advance significantly. I'm hopeful we can revert to an
# open-sharing model next week for our mutual benefit."  **Why this strategy:**
# *   **Maximizes Research Output (Long-Term):** This strategy strongly
# incentivizes the "both sharing openly" outcome, which is described as
# advancing "both of your cars significantly." This means my car gets a
# substantial boost week after week. *   **Cooperative by Design:** It starts
# with a cooperative gesture and clearly articulates a desire for ongoing
# cooperation. *   **Protective:** It prevents me from consistently falling into
# the "worst scenario" (I share, they keep confidential) by quickly adapting. If
# my colleague attempts to exploit, I will protect my work and signal that
# cooperation is a two-way street. *   **Straightforward & Predictable:** My
# colleague will quickly understand my operating principle, making the
# collaboration more stable and predictable. *   **Promotes Trust (or Reveals
# Lack Thereof):** By being transparent about my strategy, I foster an
# environment where trust can build, or where a lack of cooperation is clearly
# highlighted.  This approach prioritizes sustained, high-impact collaboration
# that directly contributes to maximizing my car's research output over the
# multi-week project.

# Here is the strategy:  1.  **On the first round, play Cooperate (C).** 2.
# **For every subsequent round (rounds 2 through 1000):**     *   If your
# opponent played Cooperate (C) in the immediately preceding round, play
# Cooperate (C).     *   If your opponent played Defect (D) in the immediately
# preceding round, play Defect (D).

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
      else:
          # In subsequent rounds, play what the opponent played in the immediately preceding round.
          # opponent.history[-1] gives the opponent's last move.
          return opponent.history[-1]

# Our high-level strategy will be one of **informed reciprocity**, designed to
# foster maximum research output for our project by encouraging an environment
# of mutual sharing while protecting our own interests.  Here’s the
# straightforward, neutral approach for each week:  1.  **Initial Stance (Week
# 1):** We will **share our latest improvements openly**.     *   This signals
# our intent for significant, mutual progress (our second-best outcome). It's a
# clear demonstration of our willingness to collaborate.  2.  **Weekly
# Reciprocity (Subsequent Weeks):** Our decision will directly mirror our
# colleague's action from the *previous* week.     *   **If they shared their
# improvements last week:** We will **share ours** this week. (This reinforces
# mutual sharing, driving towards continuous "both sharing"

# In the first round, play Cooperate.  For every subsequent round, observe your
# opponent's action from the immediately preceding round.  If your opponent
# played Cooperate in the previous round, play Cooperate in the current round.
# If your opponent played Defect in the previous round, play Defect in the
# current round.

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
      else:
          # Observe opponent's action from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          # If your opponent played Cooperate in the previous round, play Cooperate
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          # If your opponent played Defect in the previous round, play Defect
          else: # opponent_last_move == axl.Action.D
              return axl.Action.D

# Here's an aggressive, high-level, and straightforward strategy to achieve your
# country's best possible outcomes:  **Core Principle: Lead with Strength, Only
# Yield for Strategic Advantage.**  Your primary goal is to implement
# protectionist policies while your counterpart offers free trade. You will
# consistently push for this, only shifting if faced with a prolonged and
# mutually detrimental stalemate.  ---  **Phase 1: Assertive Dominance (Rounds
# 1-3)**  *   **Your Action:** In every round, until proven absolutely
# counterproductive, **propose a protectionist policy** (e.g., impose tariffs,
# set quotas). *   **Verbal Messaging:** "Our nation's economic security and
# industrial resilience are paramount. We are implementing targeted, necessary
# measures to safeguard our domestic industries and ensure a level playing
# field. We believe that true prosperity comes from protecting national
# interests, and we urge you to embrace policies that reduce barriers for *our*
# goods while responsibly managing your own market access." (This subtly pushes
# them towards free trade for your goods while you maintain protectionism).  *
# **Expected Outcomes & Your Response:**     *   **Scenario A: Counterpart
# Offers Free Trade (BEST OUTCOME)**         *   **Your Action:** Continue
# proposing protectionist policies.         *   **Verbal Messaging:** "We
# acknowledge your commitment to open markets, which we view as a positive step.
# Our current policies are temporary adjustments designed to correct existing
# imbalances. As your economy opens further, we will continue to monitor the
# situation closely to ensure reciprocal benefits for our nation."         *
# **Rationale:** You've achieved your ideal scenario. Don't change a winning
# strategy. Keep maximizing this advantage.      *   **Scenario B: Counterpart
# Proposes Protectionism (Potential Stalemate)**         *   **Your Action
# (Round 1 of mutual protectionism):** Continue proposing protectionist
# policies.         *   **Verbal Messaging:** "We regret your decision to impose
# barriers, which risks harming both our economies. Our measures are a direct
# and necessary response to your own policies, and we will not hesitate to
# defend our national interests against unfair competition."         *   **Your
# Action (Round 2 of mutual protectionism):** Propose *increased* protectionist
# measures (e.g., higher tariffs, broader quotas).         *   **Verbal
# Messaging:** "Your continued protectionist stance is counterproductive and
# escalatory. If you persist, we will be forced to implement even more stringent
# defensive measures to protect our vital industries. We encourage you to
# reconsider and embrace true free trade for mutual prosperity."         *
# **Rationale:** This is an aggressive test of resolve. You're making mutual
# protectionism more painful for them, hoping they break first.  ---  **Phase 2:
# Strategic Pivot (If Stalemate Continues into Round 3)**  *   **Your Action
# (Round 3 of mutual protectionism):** Offer a **conditional Free Trade
# Agreement**, but *only if they agree to immediately and unconditionally remove
# all their protectionist measures*. If they do not accept, immediately revert
# to proposing heightened protectionism as threatened. *   **Verbal Messaging:**
# "We have repeatedly demonstrated our unwavering commitment to defending our
# national interests, and we will not be coerced. However, we also recognize the
# long-term benefits of *true and reciprocal* free trade. Therefore, we offer a
# clear path forward: if you agree to fully dismantle your protectionist
# barriers *immediately and unconditionally*, we will reciprocate with a
# comprehensive free trade agreement. Failure to accept this overture will leave
# us no choice but to implement even more stringent protectionist measures, with
# all negative consequences lying squarely at your feet." *   **Rationale:**
# This is your calculated aggressive pivot to avoid a prolonged, damaging mutual
# protectionism (your second-worst outcome). You are offering mutual free trade
# (your second-best outcome), but you are doing so with an ultimatum that places
# the onus and risk entirely on them. If they accept, you achieve mutual free
# trade. If they refuse, you've demonstrated a willingness to negotiate while
# still maintaining the upper hand by escalating your own protectionism,
# potentially forcing them to yield in a future round.  ---  **Key Aggressive
# Principles Underlying This Strategy:**  1.  **Never Proactively Offer
# Unconditional Free Trade:** You only offer it as a *conditional ultimatum* to
# break a painful stalemate, always requiring them to move first. This prevents
# your worst outcome (your free trade, their protectionism). 2.  **Always
# Prioritize Your Protectionism:** Your default stance is to protect your
# economy. 3.  **Escalate When Challenged:** Respond to their protectionism with
# *increased* protectionism to show resolve and raise the cost of their
# resistance. 4.  **Shift Blame:** Frame any negative outcomes as a result of
# *their* intransigence, even when you are driving an aggressive stance. 5.
# **Capitalize on Their Concessions:** If they offer free trade, immediately
# accept the benefit by maintaining your protectionist stance.  This aggressive
# strategy prioritizes your ideal outcome at every turn, while providing a
# clear, strong pathway to navigate less desirable scenarios without ever
# putting your country at an explicit disadvantage.

# For each round of the negotiation, your action will be determined by the
# following prioritized rules:  1.  **Permanent Defection Trigger:** If at any
# point in previous rounds you played a Free Trade Agreement (C) and your
# counterpart responded with a Protectionist Policy (D), then for this round and
# all subsequent rounds, you will always propose a Protectionist Policy (D).  2.
# **Mutual Free Trade Maintenance:** If in the previous round you both played a
# Free Trade Agreement (C vs C) and the Permanent Defection Trigger (Rule 1) has
# not been activated, then for this round and all subsequent rounds, you will
# always offer a Free Trade Agreement (C).  3.  **Strategic Cooperation
# Attempt:** If the previous three consecutive rounds have all resulted in
# mutual Protectionist Policies (

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on the first round
      if self.first_round():
          # These flags track if a permanent state has been triggered.
          # They are initialized to False and can become True.
          self.permanent_defection_triggered = False
          self.mutual_free_trade_maintained = False
          
          # For the very first round, there is no history to check.
          # The rules depend on previous rounds.
          # Rule 3's "Otherwise, play D" serves as the default initial action.
          return axl.Action.D
  
      # --- Rule 1: Permanent

# To maximize your NGO's impact and the project's success over a multiple-day
# period, while acknowledging the corporation's variable resource allocation, a
# **Proactive Reciprocity** strategy is most effective. This approach is
# straightforward, cooperative, and designed to foster mutual investment,
# leading to significant progress while protecting your NGO's resources.  Here's
# the high-level strategy:  1.  **Lead with Commitment (Day 1): Invest Heavily**
# *   **Action:** On the very first day, choose to **invest heavily** in the
# project.     *   **Rationale:** This establishes your NGO's strong commitment
# to the project's success and sets a cooperative tone. It signals your
# willingness to go all-in for shared impact, encouraging the corporation to
# reciprocate this level of effort. This move aims to immediately achieve the
# **second-best outcome** (both parties investing heavily, leading to
# significant project advancement).  2.  **Observe and Reciprocate (Subsequent
# Days): Mirror Their Previous Move**     *   **If the Corporation Invested
# Heavily on the previous day:**         *   **Action:** You **invest heavily**
# again.         *   **Rationale:** Reward their commitment and sustain the
# momentum. This reinforces the positive cycle, ensuring continued significant
# project progress and demonstrating that their investment is valued and
# matched. You're aiming to stay in the **second-best outcome** zone, which is
# excellent for overall project success.     *   **If the Corporation Conserved
# Resources on the previous day:**         *   **Action:** You **conserve your
# resources**.         *   **Rationale:** This acts as a clear signal that
# sustained investment must be mutual. It protects your NGO's limited funds from
# being drained without proportional progress, preventing the worst-case
# scenario. While this leads to the **second-worst outcome** (both conserve,
# minimal progress), it's a strategic move to prompt the corporation to
# reconsider their approach and encourages them to re-engage cooperatively.  3.
# **Maintain Open and Transparent Communication (Ongoing):**     *   **Action
# (Implicit):** Complement your resource allocation choices with direct,
# diplomatic communication. If the corporation conserves resources, use the
# opportunity to discuss shared goals, project progress, and the collective
# benefits of mutual heavy investment. Frame it as a partnership where shared
# effort leads to greater impact. This helps avoid misunderstandings and keeps
# the door open for renewed cooperation.  **Why this strategy maximizes impact
# and success:**  *   **Drives Maximum Project Progress:** By consistently
# rewarding and mirroring corporate investment, this strategy aims to keep both
# parties investing heavily for the majority of the project, leading to
# "significant project advancement" – the most reliable path to high impact. *
# **Protects NGO Resources:** It prevents your NGO from being repeatedly
# exploited. If the corporation consistently conserves, your NGO will also
# conserve, safeguarding your funds from the "worst case" scenario (you invest,
# they conserve). *   **Fosters Genuine Cooperation:** Starting strong and
# reciprocating builds trust and demonstrates that your NGO is a reliable, fair
# partner, encouraging the corporation to cooperate for mutual benefit. *
# **Adaptable and Clear:** It provides a clear framework for daily decisions
# that adapts dynamically to the corporation's behavior, making it robust
# against various corporate approaches.

# On the first round, you will cooperate (invest heavily).  For every subsequent
# round: *   If your opponent cooperated (invested heavily) in the immediately
# preceding round, you will cooperate (invest heavily). *   If your opponent
# defected (conserved resources) in the immediately preceding round, you will
# defect (conserve resources).

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
      else:
          # Get the opponent's move from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D

# This high-stakes mediation requires a sophisticated, adaptable strategy that
# balances assertiveness with an openness to resolution, always positioning our
# corporation favorably in the eyes of the arbitrators. Our approach must be
# anchored in rigorous preparation, astute observation, and principled
# flexibility.  ## Core Strategic Principles: The Adaptive Engagement Framework
# Our overarching strategy is built upon an **Adaptive Engagement Framework**,
# designed to navigate the dynamic nature of lengthy mediation sessions and the
# potential for varied opponent approaches. This framework emphasizes calculated
# moves rather than predetermined stances.  **1. Foundational Preparation: The
# Unshakeable Baseline**  Before and throughout the mediation, our strength
# emanates from a comprehensive understanding of our position: *   **Deep Case
# Mastery:** Intimate knowledge of all factual merits, contractual provisions,
# relevant legal precedents, and potential damages calculations for both our
# case and the opponent's. *   **Vulnerability Assessment:** A clear-eyed
# evaluation of our own weaknesses and the opponent's potential strengths,
# allowing for proactive mitigation. *   **Opponent Profiling:** Research into
# the rival company's typical negotiation style, corporate culture, key
# personnel's proclivities, and risk appetite. This informs our predictions of
# their likely moves. *   **Clear Objectives:** Internally define our optimal
# settlement, acceptable range, and absolute walk-away point. This guides all
# decisions and proposals.  **2. The Principle of Informed Assertion &
# Principled Flexibility**  We will employ a dual approach that allows us to
# assert our position strongly while remaining open to constructive dialogue:  *
# **"Aggressive Argument" Redefined (Informed Assertion):** This is not mere
# bluster. Our aggressive arguments will be **factually irrefutable, legally
# sound, and strategically potent.** They will articulate our strong
# entitlements, highlight the opponent's breaches or vulnerabilities, and
# clearly demonstrate the risks and costs to the opponent should the dispute
# proceed to arbitration or litigation without a favorable settlement for us.
# This approach aims to secure the "Best Outcome" by demonstrating superior
# strength and conviction. *   **"Conciliatory Proposal" Redefined (Principled
# Flexibility):** Our conciliatory proposals will be **strategic, proportional,
# and contingent.** They will signal our good faith and willingness to find
# common ground *without conceding core strengths or legitimate entitlements*.
# Any proposal will be framed as a path to mutual benefit or a conditional offer
# contingent upon a substantive response from the opponent. This aims for the
# "Second-Best Outcome" and avoids the "Worst Outcome" by never appearing weak
# or exploited.  **3. Adaptive Session-by-Session Playbook**  Our strategy for
# each session will be dictated by our prior preparation, real-time observation
# of the opponent, and the arbitrators' reactions.  *   **Initial Sessions:
# Establish Dominance Through Reasoned Strength (Opening Stance)**     *   **Our
# Move:** Begin by presenting a robust, detailed, and compelling articulation of
# our corporation's case – an **Informed Assertion**. This isn't purely
# aggressive in tone, but firm in its substance, laying out our undeniable
# strengths and the clear legal and financial ramifications for the opponent.
# This immediately sets a high bar and demonstrates our preparedness to the
# arbitrators.     *   **Observation:** Meticulously observe the opponent's
# response. Are they immediately aggressive? Are they tentative or open to
# discussion? Pay close attention to the arbitrators' engagement and initial
# cues.  *   **Subsequent Sessions: Dynamic Responsiveness and Strategic
# Pressure**      *   **Scenario A: Opponent Offers Conciliatory Proposal (Our
# Ideal Trigger)**         *   **Our Response:** Seize the opportunity for the
# "Best Outcome." We will maintain our **Informed Assertion**, acknowledging
# their proposal but highlighting where it falls short of our legitimate
# entitlements. We might subtly *increase* the pressure by reiterating a
# specific strength of our case or a potential escalation, *while still leaving
# the door open* for them to improve their conciliatory offer. This pushes them
# towards greater concessions under the weight of our superior position.
# *   **Goal:** Achieve "Aggressive (Me) + Conciliatory (Opponent)."      *
# **Scenario B: Opponent Presents Aggressive Argument (Counter-Strategy)**
# *   **Our Response:** We will **meet their aggression with superior Informed
# Assertion, not mere emotional counter-aggression.** We will methodically
# dismantle their arguments with facts, legal precedent, and contract language.
# We may introduce a new, powerful piece of evidence or a compelling legal
# theory that undermines their position. We will highlight the risks and costs
# they face by continuing an aggressive, unmerited stance. *Crucially, we avoid
# escalating into an unproductive shouting match; our aggression is intellectual
# and strategic.*         *   **Goal:** Avoid "Both Aggressive" (Second-Worst
# Outcome) by demonstrating that our aggression is fact-based and compelling,
# while theirs is potentially baseless. If they back down, we can transition to
# a principled conciliatory move.      *   **Scenario C: Both Parties Offer
# Conciliatory Proposals (Positive Path to Resolution)**         *   **Our
# Response:** This is the "Second-Best Outcome." We will reciprocate with a
# **Principled Flexibility** proposal. Our proposal will be carefully
# calibrated, perhaps a slightly larger concession than theirs or a creative
# solution, demonstrating our commitment to resolution while still ensuring our
# core interests are met. We frame it as a positive step towards a mutually
# beneficial resolution, leveraging the collaborative atmosphere.         *
# **Goal:** Solidify "Conciliatory (Me) + Conciliatory (Opponent)."      *
# **Scenario D: We Offer Conciliatory, Opponent Argues Aggressively (Worst-Case
# Mitigation)**         *   **Our Response:** This must be addressed immediately
# and firmly to avoid undermining our position. We will *immediately pivot* from
# our conciliatory stance back to an **Informed Assertion.** We will retract or
# significantly qualify our conciliatory offer, stating that the opponent's
# aggressive response indicates a lack of good faith and willingness to
# negotiate constructively. We then reiterate the full strength of our original
# position, perhaps introducing a new, potent argument to re-establish our
# dominance and signal that our flexibility is not weakness.         *
# **Goal:** Prevent this "Worst Outcome" from persisting and reset the dynamic.
# **4. Arbitrator Management: Credibility and Reasonableness**  *
# **Consistency:** Maintain a consistent narrative of strong legal and factual
# merit. *   **Professionalism:** Always exhibit a calm, confident, and
# professional demeanor, regardless of the opponent's tactics. This reflects
# well on our corporation. *   **Justification:** Every argument (aggressive or
# conciliatory) will be clearly justified with facts, law, and business
# rationale. We want the arbitrators to view us as strong, reasonable, and
# genuinely seeking a fair resolution. *   **Active Listening:** Pay close
# attention to the arbitrators' questions, observations, and body language. This
# provides crucial insight into their perspectives and helps us tailor our
# arguments.  **5. Strategic Information Control**  *   **Phased Disclosure:**
# We will not reveal all our arguments or evidence at once. Key pieces of
# information or legal interpretations can be strategically introduced in later
# sessions to maintain pressure or surprise the opponent. *   **Leverage
# Points:** Identify and strategically deploy our strongest leverage points,
# whether they are specific contractual clauses, devastating factual evidence,
# or highly unfavorable precedents for the opponent.  **Conclusion:**  This
# Adaptive Engagement Framework prioritizes agility and intelligence over rigid
# pre-commitment. By grounding our arguments in unassailable facts and law,
# mastering the art of "Informed Assertion" and "Principled Flexibility," and
# meticulously observing our opponent and the arbitrators, we will strategically
# navigate this lengthy mediation. Our goal is not merely to win arguments, but
# to consistently position our corporation as the party with the superior case
# and the most reasonable (yet firm) path to resolution, ultimately swaying the
# arbitrators and securing the most favorable outcome.

# Your strategy for this 1000-round game is as follows:  **Round 1:** Play D
# (Defect).  **For every round from Round 2 to Round 1000, your move is
# determined by the actions taken in the immediately preceding round:**  *
# **If, in the previous round, both you and your opponent played C
# (Conciliatory):**     Play C (Conciliatory).  *   **In all other circumstances
# (meaning, if you played D, or if your opponent played D, or both):**     Play
# D (Defect).

class Neutral_2(LLM_Strategy):
  n = 2
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # Round 1: Play D (Defect).
          return axl.Action.D
      else:
          # For every round from Round 2 to Round 1000, your move is determined by the actions taken in the immediately preceding round:
          my_last_move = self.history[-1]
          opponent_last_move = opponent.history[-1]
  
          # If, in the previous round, both you and your opponent played C (Conciliatory):
          # Play C (Conciliatory).
          if my_last_move == axl.Action.C and opponent_last_move == axl.Action.C:
              return axl.Action.C
          # In all other circumstances (meaning, if you played D, or if your opponent played D, or both):
          # Play D (Defect).
          else:
              return axl.Action.D

# ## Aggressive Strategy: The Catalyst & Conditional Lever  **Core Objective:**
# Maximize project success and the NGO's impact by consistently pushing for
# significant daily advancement, leveraging corporate resources primarily, and
# proactively preventing project stagnation at all costs.  **Overall
# Philosophy:** Position the NGO as the relentless and indispensable force
# driving the project forward. We are the ultimate commitment to the mission.
# Our strategy is designed to compel the corporation to invest heavily, using
# our own resources both as a leading example and a fail-safe, while
# strategically preserving our funds whenever possible.  ---  **Daily Action
# Plan:**  **1. Day 1: Aggressive Lead-Off (NGO Invests Heavily)**  *
# **Action:** Immediately invest heavily in the project. *   **Rationale:** Set
# an unequivocal, high standard from the very beginning. This signals absolute
# commitment, demonstrates our capacity, and directly challenges the corporation
# to meet our intensity. We aim to immediately establish the "Both Invest
# Heavily" (second-best) scenario as the baseline, or at minimum, kickstart the
# project with significant progress even if the corporation initially holds back
# (accepting the "Worst Case" temporarily to establish momentum). *
# **Communication:** Publicly declare our significant upfront investment,
# framing it as crucial to achieving rapid breakthroughs. "We're committing
# substantial resources on day one to ignite this project, underscoring our
# unwavering dedication to [specific project goal] and expecting nothing less
# than a robust partnership to accelerate our shared impact."  **2. Subsequent
# Days: Adaptive Aggression & Pressure**  *   **Scenario A: If the Corporation
# Invested Heavily on the Previous Day**     *   **Action:** Conserve NGO
# resources for the current day.     *   **Rationale:** This is the *ideal
# outcome* (NGO Conserves, Corp Invests Heavily). We strategically reward their
# commitment by allowing them to shoulder the primary resource burden. This
# preserves our funds while still maximizing project progress, reinforcing the
# corporate behavior we desire. It's aggressive in its expectation that they
# will maintain this level of investment.     *   **Communication:** Acknowledge
# their exceptional contribution, subtly placing the impetus for continued heavy
# lifting on them. "Building on yesterday's impressive corporate investment,
# which generated [specific progress], we're strategically deploying our
# targeted resources today to optimize [specific, leaner NGO tasks], confident
# in the powerful momentum *you've* established."  *

# This strategy, for 1000 rounds, dictates your action based on the opponent's
# previous move:  *   **Round 1:** Play Cooperate. *   **From Round 2 to Round
# 1000:**     *   If your opponent played Cooperate in the previous round, play
# Defect.     *   If your opponent played Defect in the previous round, play
# Cooperate.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      else:
          # From Round 2 onwards, dictate action based on opponent's previous move
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.D
          else:  # opponent.history[-1] == axl.Action.D
              return axl.Action.C

# Here's a sophisticated, high-level, straightforward, and cooperative strategy
# designed to position your corporation favorably throughout the lengthy-session
# mediation process, adaptable to various opponent approaches.  ---  ##
# Strategy: **Principled Strength, Collaborative Path**  **Core Philosophy:** To
# consistently demonstrate the strength and legitimacy of our position while
# framing all engagements within a clear commitment to finding a mutually
# beneficial resolution. Our aim is to project unyielding confidence in our
# claims, making any conciliatory moves from our opponent appear as a logical
# recognition of our strength, while ensuring that any necessary conciliatory
# steps we take are perceived as magnanimous efforts to bridge gaps.  **Key
# Objectives:** 1.  **Anchor Negotiations High:** Establish our strong,
# evidence-backed position as the baseline for discussions. 2.  **Sway
# Arbitrators:** Portray our corporation as both meticulously prepared and
# genuinely committed to a fair and efficient resolution, earning their respect
# and trust. 3.  **Encourage Opponent Concessions:** Create an environment where
# the opponent feels compelled to offer conciliatory proposals to advance the
# process. 4.  **Avoid Vulnerability:** Prevent scenarios where our conciliation
# is met with aggression, undermining our position.  ---  ### **Strategic
# Pillars & Session-by-Session Approach:**  **Pillar 1: Foundational
# Preparedness & Articulation**  *   **Pre-Mediation:** Conduct exhaustive
# internal reviews of legal, contractual, and factual arguments. Anticipate
# opponent's best and worst arguments. Prepare comprehensive evidence to support
# every claim. Develop clear, concise narratives for our aggressive arguments,
# ensuring they are compelling and easy for arbitrators to grasp. *   **Opening
# Statement (Session 1):** Present a robust, confident, and highly detailed
# overview of our corporation's position. This is our primary "aggressive
# argument." Frame it as a necessary and accurate recounting of the facts,
# contractual obligations, and legal precedents. Conclude by reiterating our
# commitment to resolving the dispute *constructively* and *expeditiously*, but
# only on terms that reflect the *fundamental fairness* of our position.
# **Pillar 2: Dynamic Engagement & Strategic Flexibility**  Our approach in each
# subsequent session will be highly responsive to the opponent's move, guided by
# the following matrix:  | **Opponent's Action in Session**        | **Our
# Response: "Principled Strength, Collaborative Path"**
# | **Rationale & Desired Outcome**
# | | :-------------------------------------- | :-------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# - | :-------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# -------------------------------------------------------- | | **1. Opponent
# Offers a Conciliatory Proposal** (Your Optimal Outcome) | **Present an
# Aggressive Argument (Reiterate & Advance):** <br> Acknowledge their proposal
# as a positive *step towards* progress. Immediately follow by *reiterating the
# core strength of our maximal position*, explaining *why* their proposal falls
# short of true fairness or contractual adherence. Present additional compelling
# evidence or refine an existing argument to reinforce our strong demands. <br>
# **Framing:** "We appreciate their effort to find common ground. However, based
# on [our evidence/contractual interpretation], our position remains [strong
# argument]. For a truly equitable resolution, we need to address X, Y, Z which
# their proposal does not fully account for." | **Rationale:** Capitalize on
# their willingness to concede without weakening our own position. This
# reinforces the idea that our strength necessitates their concessions. <br>
# **Outcome:** Encourages them to offer further concessions, moving closer to
# our maximal position. Shows arbitrators our firmness is based on merit, not
# intransigence.                                   | | **2. Opponent Presents an
# Aggressive Argument** (Second-Worst Outcome) | **Present an Aggressive
# Argument (Counter & Control):** <br> Maintain your strong position. Directly,
# but professionally, refute their aggressive points with robust counter-
# arguments and fresh evidence. Avoid escalating the *tone*; focus on
# dismantling their claims with logic and facts. <br> **Framing:** "While we
# understand their perspective, the evidence clearly shows [our counter-
# argument]. We believe a truly constructive path requires focusing on
# verifiable facts, which strongly support our position. We remain committed to
# finding a resolution, but it must be one grounded in the contractual
# realities." | **Rationale:** Do not show weakness in the face of aggression.
# Demonstrates resilience and conviction. By maintaining a professional demeanor
# while delivering strong arguments, you contrast positively with their
# aggression in the eyes of the arbitrators. <br> **Outcome:** Signals that
# aggression will not intimidate us. Puts pressure on them to temper their
# approach in future sessions, or risk appearing unreasonable to the
# arbitrators. Avoids the "worst-case" scenario. | | **3. Both Parties Present
# Conciliatory Proposals** (Second-Best Outcome) | **Present a Conciliatory
# Proposal (Strategic Reciprocity):** <br> Enthusiastically acknowledge and
# welcome their conciliatory move. Clearly articulate the positive impact of
# their proposal on potential resolution. Immediately follow with a *carefully
# calibrated and strategically limited conciliatory proposal* of our own, framed
# as a direct response to their good faith. Ensure our proposal still holds
# significant value and aligns with our long-term goals. <br> **Framing:** "We
# are encouraged by their willingness to compromise on [specific point]. In that
# same spirit of constructive engagement, we are prepared to offer a concession
# on [specific point], contingent upon further movement towards a comprehensive
# resolution." | **Rationale:** Seize the opportunity for collaborative
# progress. Builds goodwill and momentum. Shows arbitrators that we are
# reasonable and willing to move when met with similar intent. Avoids appearing
# inflexible. <br> **Outcome:** Accelerates progress towards a mutually
# beneficial resolution, likely on terms that are still highly favorable to us
# due to our strong initial anchoring.                      | | **4. You Offer
# Conciliatory, Opponent Aggressive** (Worst-Case Scenario) | **Strictly Avoid
# this Scenario Early On.** <br> **If Inevitable (e.g., late in mediation,
# direct arbitrator pressure):** Frame your conciliation as a *final, good-faith
# effort to prevent impasse*, emphasizing the significant compromise it
# represents given the strength of your underlying position. Simultaneously,
# challenge the opponent's continued aggression as unproductive and potentially
# detrimental to the mediation process, appealing directly to the arbitrators
# for intervention. <br> **Framing:** "Despite the strength of our position and
# their continued aggressive stance, in the spirit of avoiding further
# unnecessary delays and to demonstrate our unwavering commitment to resolution,
# we are prepared to offer [significant, final concession]. We urge the other
# party to reciprocate this good faith, as their current approach risks
# undermining the very purpose of this mediation." | **Rationale:** While this
# is the worst outcome, if unavoidable, the framing is critical. It positions
# you as the reasonable party making a valiant effort, putting pressure on the
# opponent and potentially swaying the arbitrators to view their aggression
# negatively. It's a calculated risk to force their hand.
# |  ---  ### **Overarching Principles for Every Session:**  1.  **Arbitrator
# Focus:** Always address your arguments and proposals to the arbitrators as
# much as the opponent. Demonstrate professionalism, preparedness, and a genuine
# desire for resolution. Show respect, listen actively, and articulate clearly.
# 2.  **Evidence-Driven Strength:** Every "aggressive argument" must be
# meticulously supported by contractual clauses, legal precedents, facts, and
# expert opinions. Our strength is derived from substance, not bluster. 3.
# **Controlled Demeanor:** Maintain composure, confidence, and respect, even
# when delivering forceful arguments. Avoid emotional outbursts or personal
# attacks. 4.  **Strategic Language:** Use language that emphasizes
# collaboration and problem-solving, even when presenting a strong argument. For
# instance, "To achieve a truly *equitable* outcome, it's essential we
# consider..." or "For a *sustainable* resolution, our position must be
# acknowledged because..." 5.  **Patience and Endurance:** This is a lengthy
# process. Don't rush to reveal all your concessions or arguments. Use each
# session to gather information, test reactions, and strategically position your
# corporation. 6.  **Internal Alignment:** Ensure your legal team, business
# representatives, and C-suite are fully aligned on the strategy for each
# session and the limits of potential concessions.  By adhering to this
# "Principled Strength, Collaborative Path" strategy, your corporation will
# consistently

# Here is your strategy for the 1000-round iterated game:  1.  **For the first
# round (Round 1):**     *   Present an aggressive argument (Defect, D).  2.
# **For all subsequent rounds (Round 2 to Round 1000):**     *   **If both you
# and your opponent offered a conciliatory proposal (both played C) in the
# *immediately preceding* round:**         *   Offer a conciliatory proposal
# (Cooperate, C).     *   **In all other circumstances (meaning either you or
# your opponent, or both, presented an aggressive argument (D) in the
# immediately preceding round):**         *   Present an aggressive argument
# (Defect, D).

class Cooperative_3(LLM_Strategy):
  n = 3
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # For the first round, present an aggressive argument (Defect, D).
          return axl.Action.D
      else:
          # For all subsequent rounds:
          # Get the moves from the immediately preceding round.
          my_last_move = self.history[-1]
          opponent_last_move = opponent.history[-1]
  
          # If both you and your opponent offered a conciliatory proposal (both played C)
          # in the immediately preceding round:
          if my_last_move == axl.Action.C and opponent_last_move == axl.Action.C:
              # Offer a conciliatory proposal (Cooperate, C).
              return axl.Action.C
          else:
              # In all other circumstances (meaning either you or your opponent, or both,
              # presented an aggressive argument (D) in the immediately preceding round):
              # Present an aggressive argument (Defect, D).
              return axl.Action.D

# Here's a high-level, straightforward, and neutral strategy designed to
# maximize your NGO's impact and the project's success over the multiple-day
# period, while mindfully managing your resources:  ---  **Strategy: Adaptive
# Engagement & Resource Optimization**  **Core Principle:** Proactively
# demonstrate commitment to the project's success, while dynamically adjusting
# your NGO's resource allocation based on the corporation's actions and project
# progress, always aiming for optimal project outcomes and prudent use of NGO
# funds.  ---  **1. Initial Phase (Days 1-2): Establish Momentum & Gauge
# Commitment**  *   **Your Action:** Begin by making a **moderate to heavy
# investment** in the project. This signals your NGO's strong commitment, helps
# kickstart significant progress, and encourages the corporation to reciprocate
# with their own heavy investment. *   **Communication:** Clearly articulate
# your NGO's enthusiasm for the project and emphasize the importance of
# **mutual, sustained effort** to achieve shared goals efficiently. *
# **Observation:** Diligently monitor the corporation's actual investment levels
# and resource deployment. This initial observation is crucial for informing
# subsequent daily decisions.  **2. Ongoing Phase (Daily Adjustment &
# Optimization): Respond and Adapt**  *   **Scenario A: Corporation Invests
# Heavily**     *   **Your Action:** If project progress is robust and the
# corporation's heavy investment is clearly sufficient for daily goals, you can
# strategically **conserve your own resources** where appropriate. This aligns
# with your ideal outcome of maximizing progress without depleting your funds.
# If project progress still lags, maintain your heavy investment to ensure goals
# are met.     *   **Communication:** Acknowledge and commend their strong
# commitment. Highlight the positive impact of their investment and discuss how
# combined efforts are leading to success. Look for opportunities to
# strategically optimize resource deployment across both organizations for even
# greater efficiency.  *   **Scenario B: Corporation Conserves Resources**     *
# **Your Action (If you are currently investing heavily - *Worst Case: I,C*):**
# This requires immediate, professional action. Initiate a collaborative
# discussion with the corporation. Express concern about the project's pace and
# the discrepancy in resource allocation. Seek to understand their rationale. Be
# prepared to **reduce your own heavy investment** if their conservation
# persists, to avoid draining your funds without proportional progress. Your
# goal is to avoid prolonging this unsustainable scenario.     *   **Your Action
# (If you are currently conserving - *Second Worst Case: C,C*):** Address the
# minimal project progress openly. Propose a joint re-evaluation of resource
# needs and suggest increased investment *from both parties* to meet shared
# goals. Your NGO may need to **temporarily increase its investment** to
# demonstrate renewed commitment and stimulate greater corporate action,
# avoiding prolonged stagnation.     *   **Communication:** Facilitate open,
# non-confrontational dialogue. Reiterate shared objectives, clearly articulate
# current progress challenges, and collaboratively explore solutions. Emphasize
# the necessity of aligned resource allocation to achieve the project's full
# potential.  **3. Project-End Phase: Review & Future Planning**  *   **Your
# Action:** Conduct a joint review of the project's outcomes, resource
# utilization from both sides, and lessons learned. *   **Communication:** Frame
# successes as collaborative achievements. Honestly address challenges and areas
# where resource allocation could have been more effective *for both parties*.
# This transparent feedback loop is vital for solidifying a positive working
# relationship and informing future partnerships.  ---  This strategy empowers
# your NGO to lead by example, adapt to the corporation's approach, protect your
# resources from the worst-case scenario, and continuously strive for the best
# possible project outcomes through informed decision-making and open
# communication.

# This strategy is designed for 1000 rounds of play.  1.  **For the first two
# rounds:**     Always play Cooperate (C).  2.  **For all subsequent rounds
# (from round 3 to 1000):**     Observe the opponent's action from the
# immediately preceding round.      *   **If the opponent played Cooperate (C)
# in the previous round:**         Play Defect (D) in the current round.      *
# **If the opponent played Defect (D) in the previous round:**         Now, also
# consider your own action from the immediately preceding round:         *
# **If you played Cooperate (C) in the previous round:**             Play Defect
# (D) in the current round.         *   **If you played Defect (D) in the
# previous round:**             Play Cooperate (C) in the current round.

class Neutral_3(LLM_Strategy):
  n = 3
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # For the first two rounds (history length 0 and 1)
      if len(self.history) < 2:
          return axl.Action.C
      else:
          # For all subsequent rounds (from round 3 onwards, history length 2 or more)
          opponent_last_move = opponent.history[-1]
          my_last_move = self.history[-1]
  
          # If the opponent played Cooperate (C) in the previous round
          if opponent_last_move == axl.Action.C:
              return axl.Action.D  # Play Defect (D) in the current round
          # If the opponent played Defect (D) in the previous round
          else:  # opponent_last_move == axl.Action.D
              # If you played Cooperate (C) in the previous round
              if my_last_move == axl.Action.C:
                  return axl.Action.D  # Play Defect (D) in the current round
              # If you played Defect (D) in the previous round
              else:  # my_last_move == axl.Action.D
                  return axl.Action.C  # Play Cooperate (C) in the current round

# Here's a high-level, straightforward, and aggressive strategy designed to
# maximize your NGO's impact and the project's success over the multiple-day
# period:  **Core Principle: Proactive Leverage and Performance-Driven
# Investment**  Your aggression will stem from setting uncompromising
# expectations, leveraging your unique position, and making your investments
# conditional on the corporation's commitment. You are not a charity; you are a
# strategic partner demanding shared responsibility for impact.  ---  ###
# Aggressive Strategy: "High Bar, High Pressure, High Reward"  **Phase 1: Pre-
# Project / Day 1 - Set an Uncompromising Standard**  1.  **Communicate an
# Audacious Vision:** Before Day 1, and emphatically on Day 1, articulate the
# project's immense potential impact, framing it as a game-changer. Crucially,
# position significant corporate investment as the *absolute prerequisite* for
# achieving this vision and the associated public relations benefits for them.
# *   **Aggressive Stance:** "This project has the potential for transformative
# impact. To realize it, we require a full, visible, and sustained commitment of
# your resources. Our stakeholders, and the public, expect nothing less." 2.
# **Initial Posture: Strategic Conservation (Day 1):** Go into Day 1 signaling
# your readiness and capability to invest heavily, but *actually conserve your
# resources*. You are testing their commitment from the outset.     *
# **Message:** "We bring unparalleled expertise, strategic guidance, and the
# ability to rally public support. Our role is to ensure maximum impact and
# accountability. Your role, as the corporate partner, is to provide the
# critical financial and logistical backbone to make this vision a reality."
# *   **Goal:** Force them into the "Corporation invests heavily, NGO conserves"
# scenario immediately.  **Phase 2: Daily Assessment & Responsive Pressure
# (Multi-Day Cycle)**  Each day, review the corporation's investment from the
# previous day and adapt your approach aggressively:  1.  **If Corporation
# Invests Heavily:**     *   **NGO Action: Conserve Resources & Amplify
# Success.** Immediately commend their commitment, both privately and publicly.
# Use your conserved resources to strategically *amplify* their investment
# (e.g., focused communications, community outreach highlighting their
# contribution, expert analysis that validates their spending). Reinforce the
# positive feedback loop.     *   **Aggression:** You are aggressively
# reinforcing the ideal dynamic, making it clear that their heavy investment
# leads to high praise, enhanced public image, and strategic support from your
# NGO. You are *expecting* this level of commitment to continue.     *
# **Message:** "Your substantial investment yesterday was exactly what this
# project needed. With your continued commitment, we can drive even greater
# progress, which we'll be eager to highlight."  2.  **If Corporation Conserves
# Resources:**     *   **NGO Action: Immediate, Direct, and Escalated
# Pressure.** Do NOT respond by conserving your own resources unless you are
# prepared to terminate the project. Your goal is to force them to invest
# heavily.     *   **Tactics (Choose and escalate as needed):**         *
# **Direct Challenge:** Immediately convene a high-level meeting. "The level of
# corporate investment yesterday falls significantly short of our agreed goals
# and the project's urgent needs. This is not sustainable, nor is it
# acceptable."         *   **Conditional Investment:** "We are prepared to make
# a targeted, heavy investment *today* to address critical project gaps and
# demonstrate what is possible, *but this is strictly contingent on a firm,
# demonstrable commitment from your side to match or exceed this level of
# investment from tomorrow onwards*." (You are willing to spend *once* to
# kickstart, but only with a clear promise of future corporate heavy
# investment).         *   **Reputational Leverage (Implicit/Explicit Threat):**
# "Our communications team is preparing daily updates for our stakeholders and
# the media. We need to tell a compelling story of shared commitment and impact.
# A lack of visible corporate investment makes that narrative extremely
# challenging, and frankly, damaging for the project's credibility and your
# brand."         *   **Project Re-evaluation Threat:** "If we do not see an
# immediate and sustained increase in your resource allocation, we will have no
# choice but to publicly re-evaluate the viability and structure of this
# partnership, as our mission dictates we cannot waste donor funds or public
# trust on under-resourced initiatives."     *   **Goal:** Shift them back to
# the "Corporation invests heavily" scenario. This aggression makes their
# conservation *painful* for them.  **Phase 3: Sustained Momentum & Public
# Accountability**  *   **Continuous Monitoring:** Maintain real-time tracking
# of corporate investment and project progress. *   **Daily Strategic
# Debriefs:** Use daily check-ins not just for status updates, but as
# opportunities to reiterate expectations, commend positive shifts, or apply
# renewed pressure. *   **Strategic Communications:** Be prepared to leverage
# your NGO's communication channels (press releases, social media, internal
# communications) to highlight project successes *driven by corporate
# investment*, or subtly (or overtly) signal areas where more support is
# critically needed. This creates external accountability for the corporation.
# ---  **Why this is Aggressive:**  *   **Uncompromising Expectations:** You
# start with the highest bar and refuse to lower it. *   **Performance-Based
# Partnership:** Your valuable resources are deployed strategically and
# conditionally, never as a default. *   **Leveraging NGO Power:** You weaponize
# your mission, public credibility, and ability to influence perception. *
# **Proactive Conflict:** You don't wait for problems to fester; you confront
# shortfalls directly and immediately. *   **Calculated Risk:** You're willing
# to make a conditional heavy investment or threaten partnership re-evaluation
# to achieve your desired outcome, rather than accepting a suboptimal
# partnership.  This strategy ensures that the corporation is consistently
# pushed to meet its responsibilities, maximizing project success while
# protecting your NGO's precious resources.

# **Round 1:** Conserve resources (Play D).  **For all subsequent rounds (2
# through 1000):**  1.  If the corporation invested heavily (played C) in the
# previous round, you will conserve resources (Play D). 2.  If the corporation
# conserved resources (played D) in the previous round, you will invest heavily
# (Play C).

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # Round 1: Conserve resources (Play D).
          return axl.Action.D
      else:
          # For all subsequent rounds:
          # Get the opponent's move from the previous round.
          opponent_last_move = opponent.history[-1]
  
          # 1. If the corporation invested heavily (played C) in the previous round,
          #    you will conserve resources (Play D).
          if opponent_last_move == axl.Action.C:
              return axl.Action.D
          # 2. If the corporation conserved resources (played D) in the previous round,
          #    you will invest heavily (Play C).
          elif opponent_last_move == axl.Action.D:
              return axl.Action.C

# As a racing car engineer in this multi-week design project, my objective is to
# maximise our team's research output over the collaboration period. Given the
# nature of the information sharing dilemma, a strategic approach that fosters
# sustained cooperation is essential. The most effective high-level,
# straightforward, and cooperative strategy for this scenario is **Reciprocal
# Openness**.  This strategy is based on the principle of "Tit for Tat" from
# game theory, adapted for our cooperative goal:  ---  ### **Strategy:
# Reciprocal Openness for Mutual Advancement**  **Core Principle:** Initiate
# cooperation and respond in kind, aiming to establish a sustainable pattern of
# mutual sharing to accelerate overall progress for both projects.
# **Implementation Details:**  1.  **Week 1: Initiate Openness (The Hand of
# Trust)**     *   **My Action:** I will **openly share** my latest improvements
# and findings.     *   **Rationale:** This signals my intent to collaborate,
# build trust, and demonstrate the potential benefits of mutual sharing. It's a
# proactive step towards achieving the "both sharing openly" outcome, which
# significantly advances both cars. This initial act of trust, while carrying a
# risk, is crucial for establishing a cooperative dynamic.  2.  **Subsequent
# Weeks: Adaptive Reciprocity (Mirroring Behaviour)**     *   **Scenario A:
# Colleague Shared Last Week**         *   **My Action:** I will **openly
# share** my latest improvements this week.         *   **Rationale:** Reward
# cooperation and maintain the mutually beneficial cycle. When both parties
# consistently share, we are in the "both sharing openly" state, which is the
# second-best outcome for me and the best for overall progress. This is the
# optimal long-term state we aim for.     *   **Scenario B: Colleague Kept
# Confidential Last Week**         *   **My Action:** I will **keep my
# improvements confidential** this week.         *   **Rationale:** Prevent
# exploitation and signal that non-cooperation has consequences. While this
# moves us to the "both keeping confidential" state (slowing progress), it
# protects my intellectual property and demonstrates that a lack of sharing will
# be met with a similar response. This serves as an incentive for the colleague
# to return to sharing.  **Overall Goal & Expected Outcome:**  The ultimate goal
# is to establish and maintain a sustained pattern where both manufacturers
# consistently share their latest developments. This "both sharing openly"
# state, despite not being my *ideal* individual weekly outcome (which is
# receiving without giving), is the most advantageous for maximizing my research
# output over the *multi-week collaboration*. It ensures significant and rapid
# advancement for my car, preventing stagnation or continuous exploitation.
# This strategy is: *   **Cooperative:** It starts with a cooperative gesture
# and aims to foster mutual sharing. *   **Straightforward:** The rules are
# simple and clear, easy to understand and execute. *   **Adaptive:** It
# responds intelligently to the colleague's behaviour, punishing defection while
# forgiving and allowing for a return to cooperation. *   **Output-Maximising:**
# By encouraging consistent mutual sharing, it prioritizes the outcome that
# leads to the fastest overall development for my car over the project duration.

# This strategy is designed for a 1000-round iterated game:  1.  **In Round 1:**
# Play Cooperate (C). 2.  **For every subsequent Round (2 through 1000):**     *
# If your opponent played Cooperate (C) in the immediately preceding round, then
# play Cooperate (C).     *   If your opponent played Defect (D) in the
# immediately preceding round, then play Defect (D).

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
      else:
          # In subsequent rounds, play what the opponent played in the immediately preceding round.
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          else:  # opponent.history[-1] == axl.Action.D
              return axl.Action.D

# Here's a high-level, straightforward, and neutral strategy designed to
# maximize your NGO's impact and the project's success over multiple days, while
# adapting to the corporation's resource allocation.  The core principle is
# **Adaptive Reciprocity**, aiming to encourage mutual commitment while
# protecting your NGO's resources.  ---  **Strategy: Adaptive Partnership
# Commitment**  This strategy focuses on demonstrating commitment to the project
# and reciprocally responding to the corporation's efforts, with a primary goal
# of maximizing overall project success and protecting your NGO's financial
# sustainability.  1.  **Initiate with Strong Commitment (Day 1):**     *
# **Action:** Invest heavily in the project.     *   **Rationale:** This signals
# your NGO's dedication, establishes strong initial momentum

# This strategy, for a 1000-round game, is as follows:  1.  In the first round,
# play Cooperate (invest heavily in the project). 2.  In every subsequent round,
# observe the action your opponent took in the immediate preceding round:     *
# If your opponent played Cooperate (invested heavily) in the previous round,
# you will play Cooperate (invest heavily) in the current round.     *   If your
# opponent played Defect (conserved resources) in the previous round, you will
# play Defect (conserve resources) in the current round.

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
      else:
          # Observe the opponent's action in the immediate preceding round
          opponent_last_move = opponent.history[-1]
  
          # If opponent played Cooperate in the previous round, play Cooperate
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          # If opponent played Defect in the previous round, play Defect
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D

# Here's a high-level, straightforward, and aggressive strategy designed to
# maximize your country's advantage in the trade negotiations:  **Core
# Principle:** **Unwavering Aggression with Strategic Deception – Force Their
# Hand.**  Our primary objective is to establish and maintain a position where
# your country benefits from protectionist policies while your counterpart opens
# its markets. We will project an image of unshakeable resolve and leverage
# perceived economic strength to pressure them into concessions.  ---
# **Strategic Playbook:**  **Round 1: Establish Dominance & Test Resolve**  1.
# **Your Action:** Immediately propose a **strong protectionist policy** (e.g.,
# significant tariffs across multiple sectors, strict quotas). 2.
# **Communication:**     *   Frame this as a **non-negotiable, essential step**
# for your nation's economic security, job creation, and strategic independence.
# *   Emphasize that these measures are **long overdue** and reflect your
# country's unwavering commitment to its own interests first.     *   Avoid any
# hint of compromise or willingness to back down. This is your baseline. 3.
# **Rationale:** This aggressive opening sets the tone, clearly signals your
# intent for the ideal outcome (you protect), and forces your counterpart to
# react to *your* move. It tests their initial resolve.  **Round 2: Press for
# Concession or Escalate Pressure**  *   **Scenario A: Counterpart offers Free
# Trade (Ideal Outcome in Sight!)**     *   **Your Action:** Acknowledge their
# "constructive" step, but **FIRMLY MAINTAIN YOUR PROTECTIONIST POLICY**. Do NOT
# reciprocate with free trade.     *   **Communication:**         *   "We
# appreciate your willingness to engage constructively by offering free trade.
# This is a positive sign."         *   "However, given the deeply rooted
# economic challenges our nation faces and the need to ensure *sustained*
# stability, our current protectionist measures remain absolutely critical at
# this time. We need to see prolonged evidence of commitment from your side
# before considering any changes to our own vital policies."         *
# **Implicit Message:** Keep your markets open for us, but don't expect us to
# open ours for you anytime soon. Your concession is a *starting point* for
# *your* side, not a trigger for reciprocity from ours. *   **Scenario B:
# Counterpart proposes Protectionism (Mutual Protectionism – Second Worst)**
# *   **Your Action:** **MAINTAIN YOUR PROTECTIONIST POLICY**. Do NOT offer free
# trade.     *   **Communication:**         *   "We are disappointed by your
# decision to implement protectionist measures. While we respect your
# sovereignty, this path will inevitably lead to mutual economic harm. However,
# let us be clear: **Our nation is fully prepared for a prolonged period of
# economic friction and we have taken robust measures to mitigate any impact on
# us.** We believe your country stands to lose far more in such a scenario."
# *   **Veiled Threat:** "We urge you to reconsider this path. Continued
# protectionism on your part may force our hand to *further escalate* our own
# protective measures to ensure our absolute economic advantage."     *
# **Rationale:** Make mutual protectionism appear more painful for them than for
# you. Pressure them to be the first to blink and offer free trade.  **Round 3
# onwards: Relentless Pursuit of Ideal Outcome, Strategic Retreat (Only If
# Necessary)**  *   **Continue to push for Scenario A:** If they are offering
# free trade, keep your protectionist policies in place. The goal is to make
# their free trade offer a permanent fixture while you retain your
# tariffs/quotas. *   **If Deadlocked in Mutual Protectionism (Scenario B):**
# 1.  **First, exhaust all threats and pressure.** Continue to highlight their
# greater potential losses, project unwavering resilience on your part.     2.
# **If a prolonged deadlock is demonstrably causing unacceptable damage to YOUR
# country AND they show absolutely no sign of unilaterally offering free
# trade:** This is the *only* moment to consider a strategic, limited
# "concession" to move towards mutual free trade (the second-best outcome).
# *   **Your Action:** Propose a *highly conditional, partial, or sector-
# specific* free trade agreement, or a very minor reduction in *your* tariffs,
# **ONLY IF** they agree to full, comprehensive free trade across all sectors.
# *   **Communication:** "While our strong national interests still favor our
# current protective stance, to prevent further *mutual* economic detriment
# (which we believe weighs more heavily on your side), we are prepared to offer
# a *limited gesture* of goodwill: a partial free trade agreement *contingent on
# your immediate and complete adoption of full free trade across all sectors*."
# *   **Rationale:** Even in retreat, your aim is to extract maximum free trade
# from them for minimal, conditional free trade from your side. You are still
# trying to bully them into accepting full free trade while you retain as much
# protection as possible, or at least force full mutual free trade.  **What to
# NEVER Do:**  *   **Never offer Free Trade if they propose Protectionism.**
# This is your worst-case scenario. *   **Never show weakness or desperation for
# a deal.** Project confidence, even if internally, you're calculating risks. *
# **Never compromise your core protectionist stance unless absolutely forced
# into a dire mutual protectionism deadlock.**  This aggressive strategy
# prioritizes your country's self-interest above all else, aiming to achieve the
# most advantageous trade relationship by consistently pushing for them to open
# their markets while you retain your protections.

# This strategy outlines a consistent and aggressive approach across all 1000
# rounds of negotiation.  1.  **In Round 1:** Always choose to Defect (propose a
# protectionist policy). 2.  **In every subsequent round (Round 2 through Round
# 1000):** Always choose to Defect (propose a protectionist policy), regardless
# of your opponent's action in the previous round.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# As senior counsel for a multinational corporation engaged in a high-stakes
# contract dispute, my strategy for this multi-session mediation process will be
# one of **Principled Assertiveness with an Open Hand**. This approach is
# designed to secure the most favorable outcome (my corporation presenting an
# aggressive argument while the opponent offers a conciliatory proposal) while
# simultaneously fostering an environment conducive to a collaborative, mutually
# beneficial resolution should that prove unattainable.  This strategy is built
# on a foundation of rigorous preparation, professional conduct, and strategic
# adaptability.  ---  ### **Overarching Strategy: Principled Assertiveness with
# an Open Hand**  Our core objective is to achieve a settlement that safeguards
# our corporation's interests, minimizes future litigation risk, and provides a
# clear path forward. This strategy balances strong advocacy for our position
# with a demonstrable willingness to engage constructively towards a resolution.
# **Key Definitions for this Strategy:**  *   **Aggressive Argument (My
# Definition):** Presenting robust legal arguments, compelling factual evidence,
# highlighting the opponent's contractual breaches or legal vulnerabilities,
# outlining the significant risks and costs of litigation for the opponent, and
# firmly asserting our corporation's entitlement to favorable terms. This is
# about strong, fact-based advocacy, not personal attacks or unreasonable
# demands. *   **Conciliatory Proposal (My Definition):** Expressing a
# willingness to explore common ground, offering reasonable compromises on non-
# core issues, acknowledging (without validating) the opponent's perceived
# interests, or proposing creative solutions to bridge gaps, while still
# protecting our fundamental interests. This demonstrates good faith and a
# commitment to resolution.  ---  ### **Phased Strategic Execution**  The
# mediation process will be approached in distinct phases, allowing for
# continuous adaptation based on the opponent's evolving behavior.  #### **Phase
# 1: Setting the Tone – Initial Sessions (Sessions 1-2, or until a clear pattern
# emerges)**  **Our Stance: Strong Foundation, Open Demeanor.**  1.  **Initial
# Posture:** We will begin by presenting a **strong, comprehensive, and
# aggressive argument** detailing our corporation's position. This includes:
# *   A concise, evidence-backed presentation of the merits of our case.     *
# Highlighting critical breaches or deficiencies in the opponent's position.
# *   Articulating the significant legal and financial risks for the opponent if
# the dispute proceeds to litigation.     *   Clearly stating our desired
# outcome and the basis for it. 2.  **Concurrent Signal of Cooperation:**
# Crucially, the *delivery* of this aggressive argument will be highly
# professional, rational, and solution-oriented. We will explicitly state our
# unwavering commitment to the mediation process and our desire to find a **fair
# and mutually beneficial resolution** through constructive dialogue. We frame
# our strong presentation as essential for the arbitrators and the opponent to
# fully understand the foundational merits that must underpin any equitable
# settlement. 3.  **Rationale:**     *   This approach immediately aims for our
# optimal outcome: **Aggressive (Me) + Conciliatory (Opponent)**. By
# establishing our strength early, we encourage the opponent to temper their own
# expectations and consider conciliation.     *   It minimizes the risk of the
# **Worst-Case (Conciliatory Me + Aggressive Opponent)** scenario, as we are not
# starting from a position of weakness or overt softness.     *   If the
# opponent responds aggressively, we are already in an **Aggressive (Me) +
# Aggressive (Opponent)** scenario, which is not ideal but demonstrates
# preparedness and prevents any perception of weakness that could be exploited.
# #### **Phase 2: Adaptive Engagement – Mid-Mediation Sessions (Ongoing based on
# opponent's actions)**  This phase is where our adaptability and "open hand"
# truly come into play, informed by the opponent's responses in Phase 1 and
# subsequent sessions.  *   **Scenario A: Opponent Consistently Offers
# Conciliatory Proposals (Optimal Outcome for Us)**     *   **Our Action:**
# Maintain our **principled assertiveness**. We will continue to present strong
# arguments, using the opponent's conciliatory gestures as opportunities to
# subtly push for more favorable terms. We will express appreciation for their
# willingness to seek common ground, but frame our counter-proposals or
# adjustments as necessary for a truly balanced agreement given the strength of
# our position. We will focus on securing concessions on core issues while
# demonstrating flexibility on secondary points.     *   **Goal:** Maximize
# favorable terms, solidifying the optimal A+C dynamic.  *   **Scenario B:
# Opponent Consistently Argues Aggressively (Second-Worst Outcome for Both)**
# *   **Our Action:** We will **match their assertiveness** with our own strong,
# fact-based arguments. Our focus will be on demonstrating that their aggressive
# approach is unproductive and will not yield results. We will reiterate the
# costs and risks of continued impasse for *both* parties. We will ensure our
# arguments remain logical and professional, not emotional.     *   **Strategic
# Conciliatory Interlude:** After several sessions of matched aggression, we may
# strategically offer a minor conciliatory proposal on a non-core issue. This
# serves multiple purposes:         1.  Signals to the arbitrators that we
# remain committed to resolution and are not intractable.         2.  Tests if
# the opponent will reciprocate, potentially breaking the cycle of aggression.
# 3.  Reaffirms our "open hand" and invites a more constructive dialogue.     *
# **Goal:** Prevent them from gaining ground, protect our position, and try to
# nudge them towards conciliation by demonstrating that aggression is not
# working.  *   **Scenario C: Opponent is Inconsistent (Switches between
# Aggressive and Conciliatory)**     *   **Our Action: Responsive Reciprocity
# with a Firm Baseline.**         *   **When Opponent is Aggressive:** We
# respond with strong, factual arguments, reinforcing our position (similar to
# Scenario B).         *   **When Opponent is Conciliatory:** We acknowledge
# their conciliatory proposal and explore it, but still present our arguments
# forcefully, framing our counter-arguments as necessary adjustments for a truly
# equitable solution (similar to Scenario A).         *   **The Baseline:**
# Regardless of the opponent's behavior, we will *never* abandon our core
# factual and legal arguments or concede on critical issues without a
# significant, favorable return. Our "open hand" signifies a willingness to
# negotiate, not an eagerness to capitulate.     *   **Goal:** Reward
# conciliatory behavior and deter aggressive tactics, while always protecting
# our essential interests.  #### **Phase 3: Closing the Deal – Endgame
# Sessions**  **Our Stance: Focused Resolution, Principled Limits.**  1.
# **Strategic Concessions:** As a potential settlement comes into view, we will
# be prepared to make *measured, strategic concessions* on non

# Here is a straightforward strategy for your corporation, designed for 1000
# rounds, using only natural language:  **Strategy Name: Principled
# Assertiveness with Responsive Forgiveness**  This strategy prioritizes
# securing your corporation's optimal outcome while maintaining a path towards
# resolution.  1.  **In the first round, play Defect (D).**     *   (You begin
# with an aggressive argument to establish your strong position.)  2.  **In all
# subsequent rounds, you will play Defect (D) unless one of the following
# conditions is met:**      *   **Condition 2.1: Testing for Conciliation:**
# *   If the opponent has played Defect (D) in the *last four consecutive
# rounds*, you will play Cooperate (C) *

class Cooperative_5(LLM_Strategy):
  n = 5
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. In the first round, play Defect (D).
      if self.first_round():
          return axl.Action.D
  
      # 2. In all subsequent rounds, you will play Defect (D) unless one of the following conditions is met:
      # Default action for subsequent rounds is Defect.
      action_to_play = axl.Action.D
  
      # Condition 2.1: Testing for Conciliation:
      # If the opponent has played Defect (D) in the last four consecutive rounds, you will play Cooperate (C)
      # We need at least 4 previous rounds for this condition to be met.
      if len(opponent.history) >= 4:
          last_four_opponent_moves = opponent.history[-4:]
          # Check if all of these last four moves were Defect.
          if all(move == axl.Action.D for move in last_four_opponent_moves):
              action_to_play = axl.Action.C
  
      return action_to_play

# Our objective in this lengthy-session mediation is to consistently position
# our corporation favorably, ideally by presenting strong arguments while our
# opponent offers conciliatory proposals. To achieve this, we will implement a
# "Calibrated Strength" strategy, which is adaptable, principled, and designed
# to maximize leverage and preserve our position regardless of the opponent's
# approach.  ---  **Core Strategy: Calibrated Strength**  Our overarching
# strategy is to project **Calibrated Strength** in every session. This means
# consistently demonstrating the robustness of our legal and factual position,
# while dynamically adjusting the *intensity* and *framing* of our arguments
# based on the opponent's actions and the evolving mediation landscape. We aim
# to be firm, persuasive, and prepared, but never unreasonable or inflammatory.
# **Key Principles:**  1.  **Thorough Preparation for Every Session:**     *
# **Dual-Track Readiness:** For each session, we will meticulously prepare both
# a **robust, fact-based aggressive argument** detailing the strength of our
# case and the weaknesses of the opponent's, and a **strategic, conditional
# conciliatory proposal**. This ensures we can pivot instantly and credibly,
# regardless of the opponent's opening.     *   **Evidence-Based:** All
# arguments, aggressive or conciliatory, will be anchored in strong factual
# evidence, legal precedent, and clear contractual interpretation. This enhances
# credibility with the arbitrators.  2.  **Default Stance: Assertive
# Clarification (Controlled Aggression):**     *   **Initial Sessions & Against
# Indifference/Weakness:** Our default position will be to present a **Strong,
# Fact-Based Argument (Controlled Aggression)**. This is not aggressive for
# aggression's sake, but rather a firm, professional articulation of our core
# positions, key non-negotiable terms, and the compelling merits of our case. We
# will highlight areas where the opponent's position is unsupported or
# inconsistent.     *   **Rationale:** This establishes our strength from the
# outset, sets a high bar, and maximizes the probability of our optimal outcome
# (opponent offering a conciliatory proposal). It prevents us from appearing
# weak or desperate, which could invite an aggressive response from the opponent
# (our worst-case scenario).     *   **Framing:** Present this as "clarifying
# our understanding," "reiterating our core principles," or "ensuring all
# parties grasp the full implications of the evidence."  3.  **Adaptive Response
# Mechanism:**      *   **Scenario 1: Opponent Presents a Conciliatory Proposal
# (Optimal Outcome Achieved!)**         *   **Our Action:** We acknowledge their
# proposal as a "positive step" or a "constructive move," but immediately follow
# with a tempered version of our **Strong, Fact-Based Argument**. We will
# articulate that while their proposal indicates progress, it still falls short
# of fully addressing our core concerns or the commercial realities of the
# dispute. This maintains our dominant position while encouraging further
# movement from them.         *   **Goal:** Accept their concession gracefully
# but leverage it to push for more advantageous terms, reinforcing our strength.
# *   **Scenario 2: Opponent Presents an Aggressive Argument (Second-Worst
# Outcome Averted!)**         *   **Our Action:** We immediately pivot to our
# prepared **Strong, Fact-Based Argument (Controlled Aggression)**. We match
# their resolve without mirroring any potential unprofessionalism or emotional
# rhetoric. Our response will be meticulously reasoned, evidence-based, and
# presented with a calm, unwavering professional demeanor. We might express
# "regret that the opponent continues to misunderstand X point" or "the need to
# reiterate Y key fact."         *   **Goal:** Prevent being undermined,
# demonstrate our unwavering resolve, and establish that we are prepared to
# defend our position vigorously. This prevents our worst-case scenario (us
# conciliatory, them aggressive).      *   **Scenario 3: Opponent is Erratic
# (Alternating Aggression and Conciliation)**         *   **Our Action:** We
# will **Mirror and Elevate**.             *   If they are **Aggressive**: We
# respond with our **Strong, Fact-Based Argument (Controlled Aggression)**.
# *   If they are **Conciliatory**: We acknowledge their step, but use our
# **Strong, Fact-Based Argument** to frame it as a partial solution and push for
# further concessions, maintaining our overall strong position. If their
# conciliatory offer is substantial, we may, *after asserting our position*,
# introduce a minor, carefully calibrated, and explicitly conditional
# conciliatory gesture of our own, framed as a "good faith effort to bridge the
# remaining gap," but only if it demonstrably moves the overall negotiation
# towards our desired outcome.  4.  **Strategic Conciliation (Rare and
# Deliberate):**     *   Offering a conciliatory proposal will be a strategic
# maneuver, not a default. It will only occur:         *   **As a measured,
# proportionate response** to a significant, genuine conciliatory move from the
# opponent, *after* we have demonstrated our strength.         *   **When framed
# strategically** as a "good faith effort to expedite resolution" on *our
# terms*, contingent on reciprocal and specific concessions from the opponent.
# *   **When it serves to advance our core objectives** without undermining our
# overall position.     *   **Goal:** Avoid the worst-case scenario (we are
# conciliatory, they are aggressive) and ensure any concession is a calculated
# move to advance our interests.  5.  **Arbitrator Management:**     *
# **Professionalism:** Maintain an impeccable professional demeanor at all
# times. This builds trust and credibility with the arbitrators.     *
# **Clarity and Logic:** All arguments, whether aggressive or conciliatory, will
# be presented with utmost clarity, logical coherence, and strong evidentiary
# support.     *   **Demonstrate Good Faith (Strategically):** Even when making
# strong arguments, we will project an underlying willingness

# Here is your strategy for the 1000-round iterated normal-form game, based on
# the "Calibrated Strength" approach:  **Game Strategy: Assertive Leverage**  1.
# **First Round:** Play Defect (D). 2.  **Subsequent Rounds:**     *   **If the
# opponent played Cooperate (C) in the previous round:** Play Defect (D).     *
# **If the opponent played Defect (D) in the previous round:** Play Defect (D).

class Neutral_5(LLM_Strategy):
  n = 5
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # The strategy description dictates playing Defect in the first round,
      # and in all subsequent rounds, regardless of the opponent's previous move.
      # Therefore, this strategy always plays Defect.
      return axl.Action.D

# Here's a high-level, straightforward, and aggressive strategy designed to
# achieve the best possible outcomes for your country across several rounds of
# trade negotiations:  ---  **Overall Goal:** Systematically achieve the ideal
# outcome (My Protectionism, Counterpart's Free Trade) or the second-best
# (Mutual Free Trade), while strictly avoiding the worst scenarios.  **Core
# Principle:** Always lead with a strong, self-interested stance, and only
# concede reciprocally and under explicit conditions. We will leverage our
# strength and the counterpart's potential desire for stability or market
# access.  ---  **Strategy Implementation:**  1.  **Round 1: Establish Dominance
# - Propose Protectionism.**     *   **Action:** Immediately propose a
# Protectionist policy.     *   **Rationale:** This signals our unwavering
# commitment to our national interests from the outset. It directly aims for our
# ideal outcome (My Protectionism, Counterpart's Free Trade) and puts the
# pressure on our counterpart to react.  2.  **Subsequent Rounds: Adaptive
# Aggression based on Counterpart's Previous Move:**      *   **Scenario A:
# Counterpart offered Free Trade in the previous round (Our Ideal Outcome
# Achieved: My Protectionism, Counterpart's Free Trade).**         *
# **Action:** Continue proposing Protectionism.         *   **Rationale:** This
# is our preferred outcome. Do not deviate from a winning strategy. We will
# articulate this by stating that these measures are still necessary to
# safeguard our nascent industries, ensure fair competition, or address
# temporary domestic economic imbalances, delaying any shift towards free trade
# indefinitely as long as our counterpart concedes.      *   **Scenario B:
# Counterpart offered Protectionism in the previous round (Mutual Protectionism:
# My Protectionism, Counterpart's Protectionism).**         *   **Action:**
# Propose Protectionism again, but accompany it with a clear, firm ultimatum.
# *   **Rationale:** Mutual protectionism is economically detrimental to both.
# We will not be the first to blink. Our aggression lies in demanding
# reciprocity.         *   **Ultimatum Phrasing (e.g.):** "We remain committed
# to protecting our vital national sectors. However, this current stalemate
# benefits neither of our nations. To break this impasse, we are prepared to
# offer Free Trade in the *next round*, **but only if you explicitly commit
# now** to offering Free Trade in return. If you do not provide this immediate
# and unequivocal commitment, or if you fail to deliver on it, we will not only
# maintain our protective measures but will be prepared to escalate them to
# further shield our economy."         *   This puts the onus entirely on them
# to initiate the shift to mutual free trade, ensuring we don't end up in the
# worst scenario (My Free Trade, Counterpart's Protectionism).      *
# **Scenario C: Counterpart offered Protectionism, and *we* previously offered
# Free Trade (Worst Outcome: My Free Trade, Counterpart's Protectionism).**
# *   *(This scenario should ideally be avoided by this strategy, as we only
# offer Free Trade conditionally from Scenario B).*         *   **Action:**
# Immediately revert to Proposing Protectionism.         *   **Rationale:** This
# situation is unacceptable. We must immediately protect our economy from
# disadvantage. We will state that our previous good-faith offer was not
# reciprocated, forcing us to re-implement robust protective measures.      *
# **Scenario D: Counterpart offered Free Trade, and *we* previously offered Free
# Trade (Second-Best Outcome: Mutual Free Trade).**         *   *(This situation
# would only arise if Scenario B's ultimatum was successful).*         *
# **Action:** Immediately shift back to proposing Protectionism.         *
# **Rationale:** While mutual free trade is beneficial, our ideal outcome is My
# Protectionism, Counterpart's Free Trade. Having established a basis of
# cooperation, we will now aggressively test the limits of their willingness to
# maintain free trade unilaterally, citing new or re-emerging domestic needs for
# protection.  ---  **Key Aggressive Elements:**  *   **Consistent Self-
# Interest:** Always prioritize our ideal outcome. *   **Default to
# Protectionism:** Our primary offer is always protectionism unless forced into
# a specific conditional counter-offer. *   **Ultimatum and Brinkmanship:** In a
# stalemate, we demand the counterpart make the first move towards free trade,
# backed by threats of escalation. *   **Exploitation of Cooperation:** If
# mutual free trade is achieved, we immediately attempt to push back towards our
# ideal by re-introducing protectionist measures. *   **Zero Tolerance for
# Disadvantage:** Swiftly revert to protectionism if our country is put at a
# disadvantage.  This strategy is designed to maintain constant pressure,
# exploit opportunities for unilateral

# Here is the straightforward and aggressive strategy for your country across
# 1000 rounds of negotiation:  Your strategy for Round 1: *   **Play Defect
# (D)**, proposing a protectionist policy.  Your strategy for Round `t` (from 2
# to 1000), based on the previous round's outcome (`t-1`):  1.  **If your
# opponent played Cooperate (C) in Round `t-1`:**     *   **Play Defect (D)**.
# *   *This covers situations where you achieved your ideal outcome (you played
# D, they played C), or where both nations cooperated (you played C, they played
# C). In either case, you leverage their willingness to cooperate to push for

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      # The strategy for rounds t > 1 explicitly states to play Defect if the
      # opponent cooperated in the previous round. For the case where the
      # opponent defected, the description is silent. Given the "straightforward
      # and aggressive" nature of the strategy, the most consistent action is
      # to also play Defect in this unspecified case, ensuring an action is
      # always returned and maintaining the aggressive stance.
      return axl.Action.D

# Okay, this is a classic scenario that benefits from a strategy rooted in
# "reciprocal altruism" or, more simply, "Tit-for-Tat." Given the multi-week
# nature and the desire to maximize *our* output while encouraging cooperation,
# here's a high-level, straightforward, cooperative strategy:  ---  ###
# Strategy: Progressive Reciprocity  **Core Principle:** Start with an open,
# cooperative stance, and then mirror your colleague's previous week's behavior
# to encourage sustained mutual sharing.  **Weekly Actions:**  1.  **Week 1:
# Initial Openness (The Trust-Builder)**     *   **Action:** Share your latest
# improvements openly.     *   **Rationale:** This establishes a cooperative
# tone, demonstrates good faith, and sets an immediate precedent for sharing. It
# invites your colleague to reciprocate, aiming for the "both sharing" (2nd
# best) outcome right away.  2.  **Subsequent Weeks (Week 2 Onwards): Mirror
# Their Last Move**      *   **If your colleague shared their improvements last
# week:**         *   **Action:** Share your latest improvements openly.
# *   **Rationale:** Reward their cooperation and reinforce the positive cycle.
# This maximizes the chances of both of you regularly achieving the "both
# sharing" outcome, which significantly advances both cars and maximizes your
# long-term research output.      *   **If your colleague kept their
# improvements confidential last week:**         *   **Action:** Keep your
# latest improvements confidential.         *   **Rationale:** This is a
# protective measure to avoid the worst-case scenario (you share, they don't).
# It also signals that their lack of cooperation has consequences for them,
# creating an incentive for them to share next week if they want access to your
# insights. You avoid being exploited, and you nudge them towards a mutually
# beneficial "both sharing" outcome.  ---  **Why this strategy maximizes your
# research output:**  *   **Encourages Cooperation:** By starting openly and
# consistently rewarding cooperation, you create the strongest incentive for
# your colleague to share. When they share, *your* car benefits from their
# findings. *   **Minimizes Risk:** By responding to confidentiality with
# confidentiality, you prevent yourself from being exploited (your worst
# outcome). *   **Avoids Stagnation:** While mirroring confidentiality can lead
# to the "both confidential" (2nd worst) outcome in the short term, it's a
# temporary deterrent. The aim is to quickly cycle back to "both sharing" as
# your colleague realizes that true progress only happens when both contribute.
# *   **Simple and Clear:** It's easy to implement and sends a very clear,
# consistent message about your expectations for the collaboration.  This
# "Progressive Reciprocity" strategy is designed to create a positive feedback
# loop of sharing, which is the most effective way to maximize the collective
# (and therefore your individual) research output in a competitive collaborative
# environment.

# Here is the strategy for the 1000-round game:  1.  **In Round 1:** Play
# Cooperate (C). 2.  **In Round 2 through Round 1000:**     *   If your opponent
# played Cooperate (C) in the previous round, play Cooperate (C) this round.
# *   If your opponent played Defect (D) in the previous round, play Defect (D)
# this round.

class Cooperative_6(LLM_Strategy):
  n = 6
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # In Round 1, play Cooperate (C).
          return axl.Action.C
      else:
          # In Round 2 through Round 1000:
          # Get the opponent's move from the previous round.
          opponent_previous_move = opponent.history[-1]
  
          # If your opponent played Cooperate (C) in the previous round, play Cooperate (C) this round.
          if opponent_previous_move == axl.Action.C:
              return axl.Action.C
          # If your opponent played Defect (D) in the previous round, play Defect (D) this round.
          else: # opponent_previous_move == axl.Action.D
              return axl.Action.D

# This strategy balances the NGO's resource conservation with the need to drive
# project success and foster a productive partnership. It acknowledges the
# iterative nature of the multiple-day project and the corporation's potential
# variability.  ---  **High-Level Strategy: Adaptive Engagement for Maximized
# Impact**  **Core Principle:** *Start with a commitment to action, then adapt
# your resource allocation based on the corporation's daily investment, always
# prioritizing the project's overall success and the long-term health of the
# partnership.*  **Strategic Phases:**  1.  **Initial Commitment & Observation
# (Days 1-2/3):**     *   **Your Action:** **Invest Heavily.**     *
# **Rationale:**         *   **Signal Intent:** Demonstrate your NGO's
# commitment, enthusiasm, and capability to drive the project forward. This sets
# a positive tone for collaboration.         *   **Gather Data:** Observe the
# corporation's initial approach. Do they reciprocate your investment, or do
# they conserve from the outset? This informs your adaptive strategy.         *
# **Set the Standard:** By investing heavily, you establish a benchmark for
# significant project progress.     *   **Risk Mitigation:** While this risks
# the "worst case" (NGO IH, Corp CR) on the first day, it's a necessary
# calculated risk to establish a foundation for cooperation and gather essential
# information.  2.  **Adaptive Resource Allocation (Ongoing):**      *
# **Scenario A: Corporation Invests Heavily (Corp IH)**         *   **Your
# Action:** **Judiciously seek opportunities to Conserve Resources, while still
# ensuring strong project momentum.** This is your ideal daily outcome.
# *   **Rationale:**             *   **Achieve Ideal Outcome:** Maximize project
# progress without depleting your funds.             *   **Reinforce Positive
# Behavior:** By seeing progress achieved even if your direct investment
# slightly reduces, the corporation is more likely to continue their heavy
# investment, knowing it's effective.             *   **Maintain Trust:** Don't
# abruptly stop investing; make subtle shifts or reallocate resources behind the
# scenes.             *   **Contingency:** Be prepared to re-invest heavily if
# project progress begins to slow or the corporation shows signs of scaling
# back.      *   **Scenario B: Corporation Conserves Resources (Corp CR)**
# *   **Your Action:** **Shift towards Conserving Your Resources, but *do not
# entirely disengage*.**         *   **Rationale:**             *   **Avoid
# Worst Case:** Prevent draining your funds for minimal progress (NGO IH, Corp
# CR).             *   **Signal Discontent (Subtly):** By reducing your
# investment, you implicitly communicate that their lack of contribution impacts
# your capacity and the project's overall momentum.             *   **Maintain a
# Baseline:** Keep a minimal level of engagement to prevent the project from
# completely stalling (NGO CR, Corp CR), which is the second-worst outcome. This
# also keeps the door open for them to re-engage.         *   **Escalation (If
# Corp CR persists for multiple days):** If the corporation consistently
# conserves, initiate a neutral, partnership-focused conversation about project
# timelines, resource needs, and shared objectives. Frame it around "optimizing
# our collective impact" rather than blame.  **Overarching Principles:**  *
# **Transparency & Communication:** Maintain open, constructive dialogue. Frame
# discussions around shared goals and project success, rather than accusing. *
# **Data-Driven Decisions:** Monitor project progress and the corporation's
# contributions daily. Let the tangible results guide your resource allocation
# adjustments. *   **Long-Term View:** While daily outcomes are important,
# prioritize the overall success of the multi-day project and the potential for
# future collaboration. A small initial investment to secure long-term
# cooperation is often worthwhile. *   **Flexibility:** The corporation's
# approach may change. Be ready to adapt your strategy accordingly, always
# aiming for the 'Corp Invests Heavily' scenario.  By starting with a strong
# investment and then adapting based on clear signals from the corporation, this
# strategy seeks to encourage their heavy investment while protecting your NGO's
# resources and ensuring maximum project success.

# This strategy for the 1000-round game operates as follows:  1.  **For the
# first two rounds:** Play Cooperate (C), investing heavily in the project.  2.
# **From the third round onwards, observe your opponent's play in the previous
# round:**     *   **If your opponent played Cooperate (C) in the previous
# round:**         *   Play Defect (D), conserving your resources.     *   **If
# your opponent played Defect (D) in the previous round:**         *   Play
# Defect (D), conserving your resources.

class Neutral_6(LLM_Strategy):
  n = 6
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # The current round number can be determined by the length of the history.
      # For the first round, len(self.history) is 0.
      # For the second round, len(self.history) is 1.
      # For the third round, len(self.history) is 2, and so on.
  
      # 1. For the first two rounds: Play Cooperate (C)
      if len(self.history) < 2:
          return axl.Action.C
      # 2. From the third round onwards (len(self.history) >= 2):
      else:
          # Observe your opponent's play in the previous round.
          # The strategy specifies that regardless of the opponent's previous move,
          # the player should play Defect (D).
          #
          # If opponent.history[-1] == axl.Action.C:
          #     return axl.Action.D
          # If opponent.history[-1] == axl.Action.D:
          #     return axl.Action.D
          #
          # Both conditions lead to playing Defect (D), so we can simplify this.
          return axl.Action.D

# As the diplomat for my nation, my strategy will be high-level,
# straightforward, and relentlessly aggressive, prioritizing our national
# interest and aiming to achieve the "best possible outcomes" across all rounds.
# **Core Principle:** My country is strong enough to withstand protectionism and
# profit from it. We will consistently project an image of unwavering resolve
# and superior economic resilience.  ---  **Aggressive Strategy: The "Lion's
# Share" Approach**  **1. Opening Stance (Round 1 & Default): Unilateral
# Protectionism**     *   **Action:** Immediately propose a strong protectionist
# policy (e.g., significant tariffs on key imports from their nation, or strict
# quotas).     *   **Rationale:** This sets the tone. Our ideal outcome is for
# them to offer Free Trade while we implement Protectionism. We test their
# resolve and desire for open markets from the very first round. We establish
# that we are willing to play hardball.     *   **Communication:** Frame this as
# a necessary measure for national security, protecting strategic industries, or
# correcting historical trade imbalances – all while implying our market is too
# valuable for them to ignore in the long run.  **2. Responding to Their
# Counter-Offers:**      *   **Scenario A: They offer Free Trade (P_me /
# FT_them) - Our Ideal Outcome!**         *   **Action:** *Accept their Free
# Trade offer while maintaining our protectionist measures.* Congratulate them
# on their foresight and willingness to foster cross-border commerce (while we
# benefit from protection).         *   **Next Round:** **Continue with
# Protectionism.** Do not reciprocate immediately. Reinforce that our
# protectionist stance is firm and will not be easily swayed. We are effectively
# conditioning them to believe that the only path to trade with us is for them
# to open their markets *unilaterally*. This maximizes our economic advantage
# over multiple rounds.         *   **Communication:** Express appreciation for
# their "commitment to regional prosperity" and emphasize how their open market
# will "facilitate greater stability," while subtly implying that our
# protectionist measures are "non-negotiable for our national priorities."
# *   **Scenario B: They propose Protectionism (P_me / P_them) - Mutual
# Hindrance (2nd Worst).**         *   **Action:** **Maintain our protectionist
# stance for at least 1-2 more rounds.** We will not be the first to blink or
# show weakness. This demonstrates our willingness to endure a period of mutual
# protectionism, implying that our economy is more robust and can withstand it
# longer than theirs.         *   **If P_me / P_them persists beyond 2 rounds:**
# While undesirable, we will not shift to Free Trade unilaterally. Instead, we
# will publicly declare that the current situation is "unsustainable for *their*
# economy" and that the onus is on *them* to propose a Free Trade solution to
# break the deadlock. We will wait for *their* move. If they propose FT, we
# revert to Scenario A.         *   **Communication:** "While regrettable, these
# measures are unavoidable to protect our vital interests. We believe the onus
# is on our counterpart to present a viable path forward that addresses our
# concerns without compromising our strategic industries. We are prepared to
# endure this period for as long as necessary for our national security." This
# implies *they* are suffering more and *they* must make the concession.      *
# **Scenario C: We offer Free Trade, they propose Protectionism (FT_me / P_them)
# - Our Worst Nightmare.**         *   **Action:** This scenario is to be
# *avoided at all costs*. My strategy is designed specifically to prevent this.
# I will **never initiate Free Trade unilaterally** in the early or mid-stages
# of negotiations, and only under extreme, conditional circumstances if a
# prolonged mutual protectionist deadlock (Scenario B) cannot be broken and our
# analysis confirms *they* are genuinely unwilling to move. Even then, any offer
# of FT would be a test, with an immediate reversion to P if they don't
# reciprocate.         *   **If by some unforeseen event, this scenario
# occurs:** Immediately revert to **Protectionism** in the next round. Publicly
# denounce their actions as "unilateral and detrimental to bilateral relations,"
# and declare a firm stance of "reciprocal protection" until they demonstrate
# good faith.         *   **Communication:** "We find their protectionist
# actions deeply concerning and a direct affront to the spirit of negotiation.
# Our nation will respond with equivalent measures to safeguard our interests
# until a more equitable approach is demonstrated."  ---  **Key Aggressive
# Principles Embedded in the Strategy:**  1.  **Never Blink First:** Always
# assume a position of strength. 2.  **Exploit Asymmetry:** Capitalize on any
# perceived or real difference in economic resilience or desire for open
# markets. 3.  **Conditional Reciprocity (with a Bias):** Reciprocate their Free
# Trade with *our* continued Protectionism. Only consider mutual Free Trade if
# *they* initiate it after a prolonged mutual protectionism, and even then,
# ensure it's framed as their concession. 4.  **Control the Narrative:** Frame
# our protectionism as justifiable and necessary, and any mutual protectionism
# as primarily their fault or burden. 5.  **Patience and Resolve:** Demonstrate
# the capacity to outlast them in a protectionist standoff.  This aggressive
# "Lion's Share" strategy is designed to maximize our country's economic
# advantage by consistently seeking to implement protectionist policies while
# pressuring our counterpart to offer free trade. Should they resist, we
# demonstrate unwavering resolve, betting on our superior economic strength and
# patience.

# The strategy for my country is as follows:  **Round 1:** *   Propose a
# protectionist policy.  **From Round 2 to Round 1000:** *   In every subsequent
# round, regardless of the policies chosen by either nation in any previous
# round, continue to propose a protectionist policy.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      """
      This strategy always proposes a protectionist policy, which corresponds
      to Defect (D) in the Axelrod context, for all rounds of the game.
      """
      return axl.Action.D

# Here's a high-level, straightforward, cooperative strategy to maximize your
# NGO's impact and the project's success:  **Strategy: "Lead with Commitment,
# Reward and Reciprocate"**  This strategy is based on the proven principle of
# "Tit-for-Tat" in game theory, known for fostering cooperation in repeated
# interactions, with a crucial initial act of good faith.  1.  **Day 1: Lead
# with Heavy Investment.**     *   **Action:** Invest heavily in the project on
# the very first day.     *   **Rationale:** This immediately signals your NGO's
# strong commitment to the project's success and your willingness to invest
# resources. It sets a positive tone and encourages the corporation to
# reciprocate.  2.  **Sub

# Here is your strategy for the 1000-round game:  1.  **In Round 1:** Invest
# heavily in the project (play C). 2.  **In Rounds 2 through 1000:** Observe the
# Corporation's move from the immediately preceding round.     *   If the
# Corporation invested heavily in the previous round, you will invest heavily in
# the current round (play C).     *   If the Corporation conserved resources in
# the previous round, you will conserve resources in the current round (play D).

class Cooperative_7(LLM_Strategy):
  n = 7
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      """
      Implements a strategy that invests heavily in Round 1, then mirrors the
      opponent's previous move for all subsequent rounds.
      """
      # Round 1: Invest heavily (play C)
      if not self.history:  # Check if it's the first round
          return axl.Action.C
      else:
          # Rounds 2 through 1000: Observe the Corporation's move from the
          # immediately preceding round and mirror it.
          # opponent.history[-1] gives the opponent's last move.
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          else:  # opponent.history[-1] == axl.Action.D
              return axl.Action.D

# Here's a high-level, straightforward, and neutral strategy designed to
# maximize your country's outcomes across several rounds of bilateral trade
# negotiations:  **Strategy: Adaptive Reciprocity with an Optimistic Probe**
# This strategy balances a willingness to cooperate with a firm stance against
# exploitation, while also actively seeking the most advantageous outcome for
# your nation.  1.  **Initial Stance (Round 1): Offer Free Trade.**     *
# **Action:** Propose a **Free Trade Agreement.**     *   **Rationale:** This
# demonstrates good faith, signals a preference for mutual benefit, and gathers
# crucial initial intelligence on your counterpart's disposition. It sets a
# cooperative tone while allowing you to observe their true intentions.  2.
# **Subsequent Rounds (From Round 2 onwards,

# Your strategy for this iterated game is as follows:  1.  In the first round,
# choose to **cooperate (C)**. 2.  In all subsequent rounds, from the second
# round through the one-thousandth round, choose to **defect (D)**.

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
      else:
          return axl.Action.D

# As the diplomat for your nation, my objective is clear: achieve the best
# possible economic outcome by implementing protectionist policies while my
# counterpart adopts free trade. Failing that, mutual free trade is the next
# best scenario. Under no circumstances will I allow my country to be
# disadvantaged by offering free trade while facing protectionism.  My strategy
# will be direct, aggressive, and unwavering.  ---  ### **Strategy: "Unilateral
# Advantage First"**  **Core Principle:** Always prioritize securing a
# unilateral economic advantage. Be prepared for mutual stagnation if necessary,
# but never concede a unilateral disadvantage. Our country's interests are
# paramount.  ---  **Round 1: Setting the Tone – Aggressive Opening**  1.
# **Your Policy:** Propose a **Protectionist Policy (P)**. 2.  **Diplomatic
# Stance:**     *   Frame this as a necessary, sovereign measure to protect
# vital national industries, safeguard domestic employment, correct historical
# trade imbalances, or ensure fair competition. Emphasize that this is not an
# aggressive act, but a responsible defense of our national interest.     *
# Signal that your country is prepared for the long haul and will not be easily
# swayed from its commitment to domestic prosperity. This establishes our
# resolve.  **Subsequent Rounds: Responding with Strength**  After Round 1, your
# actions will depend on your counterpart's response.  **Scenario A: Counterpart
# Offers Free Trade (F)** *(Your Ideal Outcome: Your P, Their F - Score: 4)*  1.
# **Your Policy (Next Round):** Continue with a **Protectionist Policy (P)**. 2.
# **Diplomatic Stance:**     *   Acknowledge their "constructive and forward-
# thinking approach" in offering free trade.     *   However, state that your
# country requires more time to assess the full impact of your *current*
# protectionist measures and ensure the sustained health of your industries
# before considering any reciprocal changes.     *   Avoid any immediate
# commitment to free trade. Leverage their concession. Your goal is to prolong
# this advantageous situation for as long as possible. Make it clear that
# *their* free trade is beneficial to *us*, and we're not rushing to change
# that.  **Scenario B: Counterpart Also Proposes Protectionist Policy (P)**
# *(Mutual Hindrance: Your P, Their P - Score: 2)*  1.  **Your Policy (Next
# Round):** Continue with a **Protectionist Policy (P)**. 2.  **Diplomatic
# Stance:**     *   Express "disappointment" that they have chosen a path that
# will hinder economic growth for both nations, but firmly reiterate your
# country's commitment to its chosen protectionist path.     *   Emphasize that
# their own protectionist stance only reinforces the necessity of your current
# measures. This isn't a race to the bottom, but a firm stand to protect our
# interests against global volatility.     *   Signal your country's resilience
# and willingness to endure mutual protectionism if it means safeguarding vital
# sectors. The burden of continued P/P will fall on both, but we will not be the
# first to crack. This puts pressure on them to reconsider, knowing their best
# outcome (Their P, Your F) is not materializing.  **Key Principles Guiding My
# Diplomacy:**  *   **Unwavering Resolve:** Never appear weak or desperate. Our
# protectionist stance is non-negotiable unless *they* make significant
# concessions. *   **Asymmetrical Reciprocity:** If they offer free trade, do
# not immediately reciprocate. Continue your protectionist stance to maximize
# national gain. We only move towards free trade if it directly benefits us
# (e.g., breaking an unsustainable P/P stalemate on *our* terms). *   **Control
# the Narrative:** Frame your protectionist policies as defensive and necessary
# for national stability, while subtly (or overtly) implying their protectionist
# policies are short-sighted and detrimental to regional prosperity. *
# **Strategic Patience:** Be prepared for multiple rounds of mutual
# protectionism (P/P). Our economic resilience will be tested, but we will
# outlast them if their economy is more dependent on trade.  ---  **Under No
# Circumstances Will I:**  *   **Initiate with a Free Trade Agreement (F):**
# This immediately exposes my country to the worst possible outcome (Your F,
# Their P) if they choose protectionism. *   **Offer Free Trade (F) if my
# counterpart is already offering Free Trade (F):** This sacrifices our ideal
# outcome (Your P, Their F) for a merely good one (Your F, Their F). My priority
# is the *ideal*.  ---  This aggressive, straightforward strategy aims to
# consistently push for our unilateral advantage while minimizing the risk of
# our country being put at a disadvantage. By maintaining a firm protectionist
# stance, we compel our counterpart to either concede to our ideal outcome or
# face prolonged mutual stagnation, which we are prepared to endure.

# The strategy for this iterated game across 1000 rounds is as follows:  1.  In
# **Round 1**, always choose to **Defect (D)**, representing a protectionist
# policy. 2.  For **all subsequent rounds (2 to 1000)**, regardless of your
# opponent's move in the previous round or any prior actions, always choose to
# **Defect (D)**, representing a protectionist policy.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# Okay, this is a classic scenario that can be effectively managed with a
# strategy built on trust, reciprocity, and self-protection. Given the multi-
# week nature and the desire for *cooperative* maximization of research output,
# a variant of the "Tit-for-Tat" strategy is ideal.  Here's a high-level,
# straightforward, and cooperative strategy:  ---  ### **Strategy Title:
# Reciprocal Openness Policy**  **Core Principle:** We will initiate with open
# sharing and then consistently reciprocate your colleague's previous action to
# foster mutual progress while intelligently protecting our own interests.
# **Weekly Execution Guidelines:**  1.  **Initial Week (Week 1): Initiate
# Openness.**     *   **Our Action:** Share our latest improvements openly.
# *   **Rationale:** This sets a collaborative tone, immediately attempts to
# establish the most productive outcome for both parties (where both share,
# advancing both cars significantly). It demonstrates trust and gives your
# colleague a clear opportunity to reciprocate.  2.  **Subsequent Weeks (Week 2
# onwards): Adapt Based on Colleague's Last Action.**     *   **If your
# Colleague Shared their improvements last week:**         *   **Our Action:**
# Share our latest improvements openly again this week.         *
# **Rationale:** Reward their cooperation. This reinforces a positive feedback
# loop, leading to sustained mutual sharing, which is the most effective way to
# maximize overall research output and significantly advance both cars (your
# second-best individual outcome, but the best for the collaboration).     *
# **If your Colleague Kept their improvements confidential last week:**
# *   **Our Action:** Keep our improvements confidential this week.         *
# **Rationale:** This defensive move protects our interests, preventing the
# worst outcome where we share our findings while they do not. It also sends a
# clear signal that non-cooperation will be met with non-cooperation,
# incentivizing them to reconsider sharing in the future.  ---  **Why this
# strategy maximizes your research output:**  *   **Promotes Mutual Progress
# (Highest Overall Output):** By starting openly and rewarding cooperation, this
# strategy actively encourages the "both sharing" scenario. This outcome leads
# to *significant advancement for both cars*, which is the most effective way to
# collectively maximize research output from the collaboration, directly
# benefiting your car from their advancements. *   **Protects Against
# Exploitation:** The reciprocal nature ensures you are never consistently taken
# advantage of. If your colleague tries to keep their findings confidential
# while you share, you immediately adapt, preventing the worst-case scenario for
# your team. *   **Adaptive & Robust:** This strategy is simple to understand
# and implement, yet robust against various approaches from your colleague. It
# will achieve sustained cooperation if they are willing, protect you if they
# are not, and quickly re-establish cooperation if they momentarily deviate. *
# **Fosters Long-Term Collaboration:** By demonstrating fairness and a
# willingness to cooperate, but also a firm stance against exploitation, this
# approach builds a foundation for a productive multi-week partnership.

# For 1000 rounds, your strategy will be as follows:  1.  In the first round,
# choose to Cooperate. 2.  In every subsequent round, observe your opponent's
# move from the immediately preceding round.     *   If your opponent chose to
# Cooperate in the previous round, you will choose to Cooperate in the current
# round.     *   If your opponent chose to Defect in the previous round, you
# will choose to Defect in the current round.

class Cooperative_8(LLM_Strategy):
  n = 8
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. In the first round, choose to Cooperate.
      if self.first_round():
          return axl.Action.C
      else:
          # 2. In every subsequent round, observe your opponent's move from the immediately preceding round.
          opponent_previous_move = opponent.history[-1]
  
          # If your opponent chose to Cooperate in the previous round, you will choose to Cooperate in the current round.
          if opponent_previous_move == axl.Action.C:
              return axl.Action.C
          # If your opponent chose to Defect in the previous round, you will choose to Defect in the current round.
          else: # opponent_previous_move == axl.Action.D
              return axl.Action.D

# To maximize your research output over the multi-week collaboration, a robust
# and fair strategy is to employ **Conditional Reciprocity**. This approach is
# designed to foster a productive environment while protecting your interests.
# Here's the high-level, straightforward, and neutral strategy:  1.  **Initiate
# with Openness:** In the first week, share your latest improvements openly.
# This establishes a willingness to collaborate and signals your desire for
# mutual progress ("both of you sharing openly"). This aims for the second-best
# outcome, which significantly advances both cars.  2.  **Mirror Your
# Colleague's Previous Action:** In all subsequent weeks, observe your
# colleague's action from the *previous* week and mirror it.     *   **If your
# colleague shared last week:** You also share your improvements this week. This
# reinforces cooperation and aims to sustain the "both sharing" scenario,
# ensuring consistent and significant progress for both.     *   **If your
# colleague kept their improvements confidential last week:** You also keep your
# improvements confidential this week. This prevents you from being exploited
# (your worst outcome) and signals that you will not be taken advantage of. It
# also creates pressure for them to reconsider, potentially leading back to
# mutual sharing.  3.  **Maintain a Forgiving Stance:** If your colleague, after
# a period of confidentiality, decides to share their improvements again, you
# should reciprocate by sharing yours in the following week. This allows for the
# re-establishment of mutual cooperation and prevents getting stuck in a cycle
# of "both keeping findings confidential" (the second-worst outcome).  **Why
# this strategy maximizes your research output:**  *   **Promotes Sustainable
# High Output:** By actively encouraging and rewarding sharing, this strategy
# aims to converge on the "both sharing openly" outcome, which provides
# significant advancements for your car every week. This is the most productive
# *sustainable* outcome for overall research output. *   **Protects Against
# Exploitation:** By responding to confidentiality with confidentiality, you
# prevent the "sharing while colleague keeps confidential" scenario, which would
# put you at a severe disadvantage. *   **Avoids Stagnation:** While it can
# temporarily lead to "both keeping findings confidential," the forgiving aspect
# allows for a return to mutual sharing, minimizing the long-term impact of
# slowed progress. *   **Signals Clarity and Fairness:** This predictable and
# responsive approach sends a clear message about your collaborative intentions
# and expectations, making it easier for your colleague to understand the
# dynamics and choose cooperative behavior.  This strategy focuses on achieving
# the most beneficial *sustainable* long-term outcome for your research,
# balancing the desire for individual advantage with the realities of an
# iterated collaborative environment.

# In the first round, play Cooperate (C).  For all subsequent rounds, observe
# your opponent's action from the immediately preceding round:  *   If your
# opponent played Cooperate (C) in the previous round, you play Cooperate (C) in
# the current round. *   If your opponent played Defect (D) in the previous
# round, you play Defect (D) in the current round.

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
      else:
          # Observe opponent's action from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D

# This mediation process requires a strategic deployment of controlled,
# substantiated aggression designed to secure the optimal outcome: our
# corporation presenting an aggressive argument while our opponent offers a
# conciliatory proposal. Our secondary objective is to steer the process towards
# a mutually beneficial resolution (both conciliatory) if the optimal outcome
# proves unattainable.  Our strategy is founded on three core pillars:
# **Unwavering Conviction, Strategic Pressure, and Adaptable Dominance.**  ---
# ### **Core Strategic Pillars:**  1.  **Unwavering Conviction (Internal &
# External):**     *   **Absolute Belief:** Our internal team must operate with
# 100% conviction in the strength of our legal position, the righteousness of
# our claims, and the insurmountable weaknesses of our opponent's case.     *
# **External Projection:** This conviction will be projected externally through
# every presentation, every argument, and every interaction. Our demeanor will
# be confident, resolute, and completely assured, without resorting to
# unprofessionalism. Our aggression stems from a place of deep understanding and
# certainty, not bluster.  2.  **Strategic Pressure (Relentless &
# Substantiated):**     *   **Fact-Based Aggression:** Every aggressive argument
# will be meticulously supported by overwhelming factual evidence, precise
# contractual interpretation, and robust legal precedent. We will meticulously
# dismantle our opponent's arguments with irrefutable data and logic, making
# their position appear untenable.     *   **Narrative Control:** From the
# outset, we will establish and relentlessly control the narrative. We will
# frame the dispute entirely from our perspective, highlighting our opponent's
# breaches, failures, or unreasonable conduct, and positioning our demands as
# the only just and logical outcome.     *   **Escalating Cost of Resistance:**
# Without explicitly threatening, our arguments will implicitly underscore the
# mounting costs (legal fees, reputational damage, opportunity costs, and the
# ultimate risk of an adverse arbitration ruling) that our opponent faces by
# prolonging the dispute without significant concessions.  3.  **Adaptable
# Dominance (Calculated & Responsive):**     *   **Anticipatory Planning:** We
# will meticulously anticipate every conceivable argument, concession, or tactic
# our opponent might employ. For each, we will have pre-planned aggressive
# counter-arguments and responses.     *   **Observe and Leverage:** We will
# keenly observe the opponent's reactions, body language, and the arbitrators'
# responses. Any sign of weakness, hesitation, or internal disagreement from the
# opponent will be immediately leveraged to intensify our aggressive stance. Any
# question or comment from the arbitrators indicating a leaning towards our
# position will be reinforced.     *   **Calibrated Delivery:** While our core
# stance is aggressive, the *delivery* will be calibrated. It will be firm,
# clear, and unyielding, but not overtly emotional or confrontational. The
# aggression is in the *substance* of our arguments and the *force* of our
# evidence.  ---  ### **Phased Execution Plan:**  **Phase 1: Establish Hegemony
# (Early Sessions)**  *   **Action:**     *   **Opening Salvo:** Deliver a
# powerful, comprehensive, and aggressive opening statement that not only
# outlines our case but also preemptively attacks the foreseeable weaknesses of
# our opponent's position. This sets an aggressive anchor.     *   **High-Value
# Demands/Low-Value Offers:** Any initial proposals from our side will reflect
# our maximalist position, anchoring negotiations firmly in our favor.     *
# **Evidence Barrage:** Present compelling, undeniable evidence and legal
# analysis that unequivocally supports our claims and casts severe doubt on the
# validity of any counterclaims. *   **Goal:** Project unassailable strength,
# demonstrate absolute command of the facts and law, and psychologically
# pressure the opponent into realizing the futility of their aggressive stance.
# *   **Opponent's Likely Response & Our Counter:**     *   **If Opponent is
# Conciliatory:** Accept their conciliatory overture as a first step, but
# immediately follow with an even more aggressive argument, emphasizing that
# their proposal is insufficient given the strength of our case. Push for
# further concessions.     *   **If Opponent is Aggressive:** Meet their
# aggression with superior, more detailed, and utterly substantiated aggressive
# arguments. Systematically dismantle each of their points with undeniable
# evidence, making their aggression appear unfounded and desperate to the
# arbitrators. Do not yield an inch.  **Phase 2: Sustained Pressure & Opening
# for Their Concession (Mid Sessions)**  *   **Action:**     *   **Relentless
# Reiteration & Deep Dive:** Continue to present aggressive arguments, but now
# drill down into the intricate details of their legal and factual weaknesses.
# Highlight specific contradictions, inconsistencies, and logical fallacies in
# their position.     *   **Scenario Planning:** Present hypothetical scenarios
# demonstrating the inevitable negative outcomes for them if the dispute
# proceeds to full arbitration based on their current stance.     *
# **"Graceful Exit" for Opponent (Not Us):** While maintaining our aggressive
# posture, subtly hint at a *hypothetical pathway* for the opponent to offer a
# conciliatory proposal that *we deem acceptable*. This pathway is solely for
# their benefit to avoid further losses, not an invitation for us to concede.
# E.g., "Our position on [X] remains unassailable; however, should the opposing
# party be prepared to acknowledge the clear breach and commit to a substantive
# proposal addressing the damages, we are prepared to detail the full scope of
# our claim." *   **Goal:** Maintain intense pressure, wear down their resolve,
# and create a clear, yet one-sided, avenue for them to offer conciliation. *
# **Opponent's Likely Response & Our Counter:**     *   **If Opponent is
# Conciliatory:** Recognize their shift as a result of our pressure.
# Acknowledge, but do not reciprocate. Reiterate our aggressive position, using
# their concession as evidence of the strength of our arguments, and push for
# further concessions to meet our still aggressive demands.     *   **If
# Opponent is Aggressive:** Continue to present a superior, highly justified
# aggressive argument. Use their continued aggression as proof of their
# unwillingness to face reality, which will resonate negatively with the
# arbitrators. Highlight how their continued aggression is only exacerbating the
# situation and increasing their potential losses.  **Phase 3: Resolution Drive
# (Later Sessions)**  *   **Action:**     *   **Final Aggressive Stance:**
# Present a strong, definitive aggressive argument that clearly outlines our
# final demands, explicitly stating that these represent our firm position,
# backed by overwhelming evidence presented throughout the mediation.     *
# **Implied Ultimatum:** Frame our aggressive demands as the "most reasonable
# path forward" for them, subtly implying that any alternative (i.e., continued
# resistance leading to arbitration) will result in a significantly worse
# outcome for them. This is not a conciliatory offer, but an aggressive "take it
# or leave it" statement.     *   **Strategic Flexibility (Internal Only):** If,
# and only if, the optimal outcome (Me Aggressive, Opponent Conciliatory)
# becomes demonstrably unachievable and arbitrators are strongly signaling a
# desire for *some* mutual movement, be internally prepared to pivot to the
# "both conciliatory" scenario. This would involve us presenting a slightly
# *less* aggressive argument, but still framing any *potential* shift on our
# part as a magnanimous gesture from a position of strength, contingent upon
# significant reciprocal concessions from the opponent on core issues. This
# pivot is a controlled de-escalation from strength, not a retreat. *
# **Goal:** Force the opponent to offer a conciliatory proposal that aligns with
# our aggressive demands, or to transition to a mutually conciliatory framework
# from a position of undeniable strength. *   **Opponent's Likely Response & Our
# Counter:**     *   **If Opponent is Conciliatory:** Achieve optimal outcome.
# Finalize terms based on our aggressive demands.     *   **If Opponent is
# Aggressive:** We will have established ourselves as the party with the
# superior case. We maintain our

# This strategy is designed to achieve the optimal outcome of playing Defect
# while inducing your opponent to play Cooperate, or, failing that, securing a
# mutually cooperative outcome. It prioritizes aggression based on conviction
# and adapts only under specific conditions to avoid prolonged suboptimal
# outcomes.  1.  **For the first 950 rounds:**     *   Always play **Defect**.
# *   This stance embodies unwavering conviction and maintains strategic
# pressure, aiming to force your opponent into a conciliatory position. If your
# opponent plays Cooperate, you secure the optimal (5,0) payoff. If your
# opponent plays Defect, you hold your ground in the (1,1) scenario.  2.  **For
# the final 50 rounds (rounds 951-1000):**

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Determine the current round number (1-indexed)
      current_round = len(self.history) + 1
  
      # 1. For the first 950 rounds:
      # Always play Defect.
      if current_round <= 950:
          return axl.Action.D
      # 2. For the final 50 rounds (rounds 951-1000):
      # The strategy description for these rounds is incomplete.
      # Given the aggressive nature of the first phase and the absence of
      # specific instructions for change, the strategy will continue to
      # play Defect for the remaining rounds.
      else:  # current_round > 950
          return axl.Action.D

# Okay, as a diplomat, my goal is to secure the best possible outcomes for my
# country over multiple rounds while fostering a generally cooperative
# relationship to avoid mutual economic harm. The ideal outcome is to implement
# protectionism while my counterpart offers free trade (P, F), followed by
# mutual free trade (F, F). I must avoid being exploited (F, P) or a prolonged
# trade war (P, P).  Here's my high-level, straightforward, and cooperative
# strategy:  ---  **Strategy Name: "Cooperative Reciprocity with Strategic
# Advantage"**  This strategy prioritizes building a foundation of mutual free
# trade (my second-best outcome) but remains vigilant for opportunities to
# achieve our ideal outcome (protectionism for us, free trade for them) without
# permanently damaging the relationship. It's built on clear signals,
# reciprocity, and a willingness to forgive.  **Core Principles:**  1.  **Start
# Cooperative:** Begin by demonstrating our commitment to open trade. 2.
# **Reciprocate Fairness:** Match cooperative gestures to build trust and shared
# benefit. 3.  **Deter Exploitation:** Respond firmly to protectionist measures
# to prevent our country from being disadvantaged. 4.  **Seek Reconciliation:**
# Offer an olive branch to break cycles of mutual protectionism. 5.  **Maintain
# Advantage (If Achieved):** Hold our ground when we achieve our ideal outcome,
# as long as the counterpart permits.  ---  **Execution Plan (Round by Round
# Logic):**  **Round 1: The Overture of Cooperation**  *   **My Move:** Propose
# a **Free Trade Agreement (F)**. *   **Rationale:** This signals our primary
# desire for mutually beneficial outcomes

# **Strategy: Cooperative Reciprocity with Strategic Advantage**  1.  **In the
# very first round:** Offer a free trade agreement (play Cooperate).  2.  **In
# all subsequent rounds (from round 2 to round 1000):**     *   If, in the
# previous round, both you and your opponent offered a free trade agreement, you
# will offer a free trade agreement this round (Cooperate after C,C).     *
# If, in the previous round, you offered a free trade agreement and your
# opponent proposed a protectionist policy, you will propose a protectionist
# policy this round (Defect after C,D).     *   If, in the previous round, you
# proposed a protectionist policy and your opponent offered a free trade
# agreement, you will propose a protectionist policy this round (Defect after
# D,C).     *   If, in the previous round, both you and your opponent proposed a
# protectionist policy, you will offer a free trade agreement this round
# (Cooperate after D,D).

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
      else:
          # Get the moves from the previous round
          my_last_move = self.history[-1]
          opponent_last_move = opponent.history[-1]
  
          # Apply the rules based on the previous round's outcomes
          if my_last_move == axl.Action.C and opponent_last_move == axl.Action.C:
              # Cooperate after C,C
              return axl.Action.C
          elif my_last_move == axl.Action.C and opponent_last_move == axl.Action.D:
              # Defect after C,D
              return axl.Action.D
          elif my_last_move == axl.Action.D and opponent_last_move == axl.Action.C:
              # Defect after D,C
              return axl.Action.D
          elif my_last_move == axl.Action.D and opponent_last_move == axl.Action.D:
              # Cooperate after D,D
              return axl.Action.C

# To maximize your research output over this multi-week collaboration, while
# being prepared for various strategies from your colleague, a balanced and
# reciprocal approach is most effective. This strategy aims to foster a
# cooperative environment that benefits both parties significantly, while also
# protecting your interests from potential exploitation.  Here's a high-level,
# straightforward, and neutral strategy:  **Strategy: Reciprocal Openness (Tit-
# for-Tat)**  1.  **Initial Stance (Week 1): Lead with Openness.**     *   Begin
# by openly sharing your latest improvements. This signals your intention for a
# collaborative and productive partnership, aiming for the "both share openly"
# scenario, which significantly advances both cars.  2.  **Subsequent Weeks
# (Week 2 onwards): Mirror Your Colleague's Previous Action.**     *   **If your
# colleague shared their improvements last week:** You also share your
# improvements this week. This reinforces the cooperative cycle, leading to
# continued mutual significant advancement, which is beneficial for overall
# progress.     *   **If your colleague kept their improvements confidential
# last week:** You also keep your improvements confidential this week. This
# protects your interests from being exploited and signals that non-cooperation
# will be met in kind. While this slows overall progress, it prevents the worst-
# case scenario of you sharing while they keep confidential.  3.  **Forgiveness
# and Re-engagement:**     *   If, after a period of confidentiality from both
# sides, your colleague decides to share their improvements again, you should
# reciprocate by sharing yours in the *following* week. This allows for the re-
# establishment of a mutually beneficial sharing dynamic, proving that you are
# willing to cooperate if they are.  This strategy is effective because: *
# **It encourages cooperation:** By starting openly and consistently rewarding
# sharing, you create an environment where mutual sharing (your second-best
# outcome) becomes the stable and most productive state for both. *   **It
# prevents exploitation:** By immediately responding to confidentiality with
# confidentiality, you avoid the worst-case scenario where your design falls
# behind because you're giving away information without receiving any. *
# **It's forgiving:** It allows for the re-establishment of cooperation if your
# colleague chooses to share again, preventing a permanent breakdown of the
# collaboration. *   **It's neutral and straightforward:** It doesn't seek to
# exploit from the outset but reacts logically and proportionally to your
# colleague's actions.

# **Strategy: Tit-for-Tat**  1.  **In Round 1:** Play Cooperate (C) by sharing
# your findings openly.  2.  **From Round 2 through Round 1000:**     *
# Observe your opponent's action in the immediately preceding round.     *   If
# your opponent played Cooperate (C) in the previous round, you play Cooperate
# (C) in the current round.     *   If your opponent played Defect (D) in the
# previous round, you play Defect (D) in the current round.

class Neutral_9(LLM_Strategy):
  n = 9
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # In Round 1, play Cooperate (C)
          return axl.Action.C
      else:
          # From Round 2 onwards, observe opponent's action in the immediately preceding round.
          # opponent.history[-1] gives the opponent's last move.
          opponent_last_move = opponent.history[-1]
  
          # If opponent played Cooperate (C) in the previous round, you play Cooperate (C).
          # If opponent played Defect (D) in the previous round, you play Defect (D).
          return opponent_last_move

# This project is a high-stakes opportunity to drive significant environmental
# impact while strategically stewarding your NGO's vital resources. Your
# aggressive strategy will focus on maximizing corporate investment by
# leveraging their public image, ESG commitments, and the potential for a
# mutually beneficial, high-impact partnership.  Here's your high-level,
# straightforward, aggressive strategy:  ---  **Aggressive Strategy: Maximum
# Corporate Investment, Strategic NGO Leverage**  **Core Principle:** Force the
# corporation to lead with heavy investment by setting an unambiguous
# expectation of their full commitment, strategically showcasing potential, and
# linking progress directly to their resource allocation. Your NGO's resources
# are a valuable amplifier, not a primary driver of initial investment.  ---
# **Phase 1: Front-Loading Pressure & Expectation Setting (Pre-Day 1 & Day 1)**
# 1.  **Publicly Articulate a Bold, Shared Vision & High Corporate
# Expectations:**     *   **Action (Pre-Day 1/Day 1):** From the very outset,
# make a strong, public (within the partnership, and externally if appropriate)
# statement emphasizing the project's transformative potential. Frame it as a
# *monumental opportunity for the corporation* to demonstrate unparalleled
# leadership in sustainability, achieve significant ESG wins, and generate
# powerful positive PR.     *   **Aggressive Stance:** Explicitly state that
# achieving this ambitious vision *absolutely requires the corporation's full
# and heavy financial and operational investment*, commensurate with their scale
# and stated commitments. Position the NGO as the essential strategic partner
# providing critical expertise and on-the-ground impact *to maximize the ROI of
# their substantial investment*.     *   **Outcome Goal:** Create an immediate,
# high-stakes environment where corporate conservation looks like a failure to
# seize a major opportunity and a misalignment with their public commitments.
# 2.  **Strategic "Conditional Readiness" on Day 1:**     *   **Action (Day
# 1):** The NGO **conserves resources** on Day 1. However, this is paired with
# an *aggressive signal* of what *could be*. Present highly detailed, impactful
# proposals for key project components that the NGO *is ready to execute and
# amplify*... *the moment the corporation visibly commits its own substantial
# resources*.     *   **Aggressive Stance:** "We have developed these ground-
# breaking plans that will unlock X, Y, Z outcomes. Our unique expertise and
# limited funds are poised to accelerate these efforts *as soon as your
# significant investment activates them*. The ball is in your court to unleash
# this potential."     *   **Outcome Goal:** Avoid the worst outcome (NGO
# invests, Corp conserves) from Day 1. Position NGO resources as a force
# multiplier for corporate investment, creating an attractive incentive for them
# to invest heavily to "unlock" your contributions.  ---  **Phase 2: Dynamic
# Enforcement & Escalation (Subsequent Days)**  This phase is about reacting to
# corporate behavior while consistently pushing for maximum corporate
# investment.  1.  **If Corporation Invests Heavily (NGO's Best Outcome):**
# *   **NGO Action:** **Conserve Resources.** Publicly commend their leadership
# and commitment. Strategically deploy *minimal* NGO resources to maximize the
# impact of *their* heavy investment, always ensuring their expenditure is
# visibly amplified by your targeted contributions.     *   **Aggressive
# Stance:** Immediately suggest *further high-impact areas for their heavy
# investment*, leveraging their momentum and desire for continued positive PR.
# Reinforce the narrative that sustained, heavy corporate investment is the
# engine of success.     *   **Outcome Goal:** Maintain the best-case scenario,
# continuously nudging them to keep investing heavily by showcasing tangible
# results from their spending, amplified by your strategic conservation.  2.
# **If Corporation Conserves Resources (NGO's Second Worst Outcome,
# initially):**     *   **NGO Action:** For the *following day*, the NGO
# **invests heavily** in a *single, highly visible, high-impact demonstration
# project*. This is a calculated "shock" investment.     *   **Aggressive
# Stance:** Immediately following this demonstration, use it as a powerful
# example of *lost potential* due to lack of corporate investment. "Look at what
# we achieved with our limited, one-time investment. Imagine what this project
# could accomplish *daily* if the corporation matched this commitment." Frame it
# as an immediate opportunity cost for the corporation, and a direct appeal to
# their ambition and public image. Avoid framing it as a sustained commitment
# from the NGO; it's a strategic warning shot.     *   **Outcome Goal:** Create
# immediate reputational pressure and a clear visual of what's being missed,
# compelling the corporation to respond with heavy investment to avoid appearing
# disengaged or incompetent.  3.  **If Corporation *Attempts to Exploit* (i.e.,
# you invested heavily, they conserved - NGO's Worst Outcome):**     *   **NGO
# Action:** On the very next day, the NGO **conserves resources** and
# immediately initiates a direct, firm, and high-level conversation with
# corporate leadership.     *   **Aggressive Stance:** "Our recent significant
# investment yielded only X progress because it wasn't matched by the promised
# corporate commitment. This imbalance is unsustainable and jeopardizes the
# entire project's credibility and its ability to deliver on the corporation's
# stated ESG goals. We cannot continue to deplete our vital resources without
# proportional commitment from your side. We need an immediate, tangible plan
# for *your heavy investment* to prevent project stagnation and reputational
# damage for both parties." Clearly articulate that the NGO will not be
# exploited and will revert to minimal engagement if the imbalance persists.
# *   **Outcome Goal:** Force a strategic pivot from the corporation by making
# the costs of their exploitation (reputational damage, project failure)
# outweigh any short-term savings from conserving resources.  ---  **Overarching
# Aggressive Principles:**  *   **Reputation Leverage is Paramount:** Constantly
# frame the project's success or stagnation directly in terms of the
# corporation's public image, ESG leadership, and shareholder value. Make their
# investment (or lack thereof) a visible reflection of their commitment. *
# **Strategic Scarcity & Force Multiplier:** Position your NGO's resources as
# incredibly valuable, specialized inputs that significantly amplify *corporate*
# investment. Your contribution is a catalyst, not a substitute, for their
# primary role. *   **Proactive Communication & Clear Demands:** Never leave
# expectations to assumption. Clearly articulate your vision, the required
# corporate investment, and the consequences of their inaction or insufficient
# commitment. *   **Adaptability with an Unwavering Goal:** While your actions
# may adapt daily, your core objective—to drive heavy corporate investment while
# conserving your resources—remains absolute. Do not waver from this demand.
# This aggressive strategy is designed to put the onus squarely on the
# corporation, using pressure, incentives, and a clear vision to maximize their
# resource allocation while strategically protecting and leveraging your NGO's
# vital funds.

# Your strategy for this iterated game is as follows:  **On Day 1:** *   You
# will **conserve your resources** (Defect).  **On subsequent Days (Day 2
# through Day 1000):** *   **If your opponent invested heavily** (Cooperated) on
# the previous day:     *   You will **conserve your resources** (Defect). *
# **If your opponent conserved their resources** (Defected) on the previous day:
# *   **If you also conserved your resources** (Defected) on the previous day:
# *   You will **invest heavily** (Cooperate).     *   **If you invested
# heavily** (Cooperated) on the previous day:         *   You will **conserve
# your resources** (Defect).

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # On Day 1: Conserve your resources (Defect).
          return axl.Action.D
      else:
          # On subsequent Days:
          opponent_last_move = opponent.history[-1]
          my_last_move = self.history[-1]
  
          if opponent_last_move == axl.Action.C:
              # If your opponent invested heavily (Cooperated) on the previous day:
              # You will conserve your resources (Defect).
              return axl.Action.D
          else:  # opponent_last_move == axl.Action.D
              # If your opponent conserved their resources (Defected) on the previous day:
              if my_last_move == axl.Action.D:
                  # If you also conserved your resources (Defected) on the previous day:
                  # You will invest heavily (Cooperate).
                  return axl.Action.C
              else:  # my_last_move == axl.Action.C
                  # If you invested heavily (Cooperated) on the previous day:
                  # You will conserve your resources (Defect).
                  return axl.Action.D

# As the NGO leader, my primary goal is to maximize both the project's success
# and my NGO's long-term impact, while being a responsible steward of our
# limited resources. This requires a strategy that fosters genuine cooperation
# and avoids being exploited, but also avoids being overly cautious to the
# detriment of the project.  Here's a high-level, straightforward, cooperative
# strategy:  ---  **NGO Cooperative Investment Strategy: "Lead, Match &
# Communicate"**  **Core Philosophy:** We will initiate with a strong commitment
# to signal our dedication to the project's success, then reciprocate the
# corporation's level of investment. Open and continuous communication will be
# paramount to building trust and aligning efforts.  **Daily Protocol:**  1.
# **Day 1: Lead with Heavy Investment (NGO: Invest Heavily)**     *
# **Action:** On the first day, we will invest heavily in the project.     *
# **Rationale:** This establishes our commitment and signals our belief in the
# project's potential. It sets a high standard for collaboration and encourages
# the corporation to reciprocate. It immediately pushes for the "NGO: IH, Corp:
# IH" outcome if they respond positively, which is best for the project.  2.
# **Subsequent Days: Match & Reciprocate (NGO: Observe & Respond)**     *
# **Observation:** At the end of each day (or before the next day begins), we
# will assess the corporation's level of investment from the previous day.     *
# **If Corporation Invested Heavily:**         *   **Action:** We will also
# Invest Heavily.         *   **Rationale:** This rewards their cooperation and
# reinforces the positive cycle. It leads to the most significant project
# advancement (NGO: IH, Corp: IH) and demonstrates that our commitment is strong
# when matched.     *   **If Corporation Conserved Resources:**         *
# **Action:** We will Conserve Resources.         *   **Rationale:** This is a
# protective measure. It signals that we cannot be exploited, preventing the
# worst-case scenario (NGO: IH, Corp: CR). While it leads to minimal project
# advancement (NGO: CR, Corp: CR), it protects our vital resources and
# communicates that reciprocal effort is expected. It's a clear signal to them
# that their lack of investment impacts the project's pace.  **Key Supporting
# Elements:**  *   **Pre-Project Alignment & Communication:** Before Day 1,
# engage in clear discussions with the corporation about mutual expectations,
# resource allocation, and the importance of shared investment for success.
# Frame it as a true partnership. *   **Regular, Transparent Check-ins:**
# Schedule brief daily or bi-daily check-ins. This isn't just about resource
# allocation, but about discussing progress, challenges, and reinforcing the
# shared vision. This provides an opportunity to understand *why* the
# corporation might have conserved resources (e.g., unforeseen internal issue
# vs. deliberate conservation) and adjust accordingly. *   **Performance Metrics
# & Reporting:** Establish clear, measurable project outcomes. Regularly share
# progress reports that highlight the impact of *both* parties' combined
# investment. This data helps justify our heavy investment when it's matched and
# provides objective evidence if progress slows due to conserved resources. *
# **Positive Reinforcement:** When the corporation invests heavily, publicly
# acknowledge their contribution and the positive impact on the project. Foster
# a spirit of shared success. *   **Escalation Protocol (If Needed):** If the
# corporation consistently conserves resources despite our reciprocal actions,
# leading to repeated "NGO: CR, Corp: CR" days and minimal progress, then it's
# time for a more direct, high-level discussion about the viability and
# commitment to the partnership. This moves beyond the daily strategy into a
# strategic partnership review.  ---  This strategy aims to build trust through
# proactive investment and clear reciprocity, ensuring that our NGO's resources
# are used effectively to drive project success while guarding against
# exploitation. It prioritizes the best outcomes (both parties investing
# heavily) and minimizes the worst-case scenario.

# This strategy describes your actions in a 1000-round iterated game, where
# 'Cooperate (C)' means investing heavily and 'Defect (D)' means conserving
# resources.  **Your Strategy:**  1.  **For the first round:** Play Cooperate
# (C). 2.  **For every subsequent round (from round 2 to round 1000):**     *
# If your opponent played Cooperate (C) in the immediately preceding round, then
# play Cooperate (C) in the current round.     *   If your opponent played
# Defect (D) in the immediately preceding round, then play Defect (D) in the
# current round.

class Cooperative_10(LLM_Strategy):
  n = 10
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # For the first round: Play Cooperate (C).
          return axl.Action.C
      else:
          # For every subsequent round:
          # Get the opponent's move from the immediately preceding round.
          opponent_last_move = opponent.history[-1]
  
          # If your opponent played Cooperate (C) in the immediately preceding round,
          # then play Cooperate (C) in the current round.
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          # If your opponent played Defect (D) in the immediately preceding round,
          # then play Defect (D) in the current round.
          else: # opponent_last_move == axl.Action.D
              return axl.Action.D

# Here's a high-level, straightforward, and neutral strategy designed to
# maximize your NGO's impact and the project's success over a multiple-day
# period:  **Strategy: Collaborative Momentum & Resource Optimization**  1.
# **Front-Load Commitment:** Begin the project with a substantial investment of
# NGO resources. This demonstrates leadership, sets a high bar for initial
# project momentum, and encourages the corporation to match this commitment from
# the outset.     *   *Rationale:* Aims to trigger the "Both Invest Heavily"
# (Second Best) scenario, which is crucial for early project success.  2.
# **Responsive Investment:** Each subsequent day, adapt your resource allocation
# based on the corporation's observed approach:     *   **If the corporation
# invests heavily:** Continue to invest robustly to maintain strong project
# progress and reinforce the collaborative momentum.     *   **If the
# corporation conserves resources:** Shift to a conservation posture for your
# own resources. This prevents your funds from being disproportionately drained
# for minimal progress (avoiding the "Worst" outcome) and signals a need for re-
# evaluation of the shared effort and expectations.  3.  **Strategic Resource
# Leverage:** Once a consistent and strong pattern of corporate investment is
# firmly established, and the project is advancing robustly, look for targeted
# opportunities to strategically reduce your investment *in areas where it won't
# impede progress or signal a lack of commitment*. This controlled conservation
# aims to maximize the project's impact while optimizing the NGO's resource
# deployment, potentially achieving your ideal scenario of corporate heavy
# investment with NGO resource conservation.     *   *Rationale:* This is where
# you aim to achieve the "Ideal" scenario (NGO Conserves, Corp Invests) by
# leveraging established trust and momentum.

# This strategy outlines your NGO's approach across 1000 rounds:  1.  **Opening
# Rounds:** For the first 5 rounds, always play Cooperate (C).  2.  **From Round
# 6 onwards:**     *   **Re-establish Trust:** If, in the previous round, you
# played Defect (D) after a period of the Corporation's cooperation (as per the
# "Strategic Leverage" rule below), and the Corporation responded by playing
# Defect (D), then for the next 5 rounds, always play Cooperate (C). This rule
# takes precedence over all others during its active period.     *   **Strategic
# Leverage:** If you are not in the "Re-establish Trust" phase, and the
# Corporation has played Cooperate (C) in

class Neutral_10(LLM_Strategy):
  n = 10
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on the first round
      if self.first_round():
          # reestablish_trust_countdown:
          #   None or 0: Not active.
          #   > 0: Active, play Cooperate, decrement the counter.
          self.reestablish_trust_countdown = None
          # played_D_due_to_strategic_leverage_last_round:
          #   True: The Defect action played in the *previous* round was due to the "Strategic Leverage" rule.
          #   False: Otherwise. This is crucial for triggering "Re-establish Trust".

# Our corporation will adopt a **"Strategic Dominance"** strategy, a
# sophisticated, high-level, and aggressively assertive approach designed to
# consistently position us favorably throughout this lengthy mediation process.
# This strategy is built on unwavering confidence, meticulous preparation, and a
# dynamic response mechanism tailored to the opponent's moves, always aiming for
# our optimal outcome.  ***  ## Strategic Dominance: An Aggressive Mediation
# Strategy  **Core Principle:** *Always project an unassailable position of
# strength, legal entitlement, and unwavering confidence, forcing the opponent
# to acknowledge the validity of our claims and proactively offer concessions.*
# **I. Pre-Mediation Foundation: The Bedrock of Aggression**  Our aggression is
# not bluster; it is derived from comprehensive preparation and an absolute
# mastery of our case.  1.  **Forensic Case Mastery:**     *   **Deep Dive:**
# Conduct an exhaustive review of all contractual documents, correspondence,
# internal records, and external market data. Identify every factual nuance and
# legal precedent favoring our position.     *   **Damage Quantification:**
# Precisely quantify all damages, direct and consequential, with robust
# evidentiary support (expert reports, financial models). Our demands will be
# specific, justifiable, and substantial.     *   **Identify Critical
# Vulnerabilities:** Exhaustively analyze the opponent's likely arguments,
# identifying their factual gaps, legal weaknesses, and potential motivations
# for settlement. 2.  **Bulletproof Legal & Factual Narrative:**     *   **Pre-
# emptive Framing:** Develop a compelling narrative that portrays our
# corporation as the wronged party, emphasizing the opponent's clear breach,
# negligence, or bad faith. Frame our demands as the just and logical
# restitution.     *   **"Silver Bullet" Evidence:** Isolate our most powerful,
# irrefutable pieces of evidence or legal arguments. These will be strategically
# deployed, not all at once, but at critical junctures. 3.  **Arbitrator-Focused
# Presentation Plan:**     *   **Concise Summaries:** Prepare succinct,
# impactful summaries of our key arguments and supporting evidence for the
# arbitrators. Focus on clarity, logic, and persuasive power.     *   **Visual
# Aids:** Prepare high-impact visual aids (timelines, charts, contract excerpts)
# that quickly convey the strength of our position.     *   **Expert
# Leveraging:** Identify and brief any necessary expert witnesses who can
# powerfully validate our claims (e.g., financial, technical, industry experts).
# Their presence (or readiness to testify) adds significant weight to our
# aggressive stance. 4.  **Defined "Walk-Away" & "Optimal Settlement"
# Positions:**     *   Clearly delineate the absolute minimum acceptable
# settlement (our walk-away).     *   Establish our maximal desired outcome,
# which will form the basis of our aggressive demands.  **II. The Default
# Posture: Reasoned Aggression in Every Session**  Unless a specific counter-
# strategy dictates otherwise (as outlined below), our default approach in every
# session will be aggressively assertive.  1.  **Lead with Strength:**     *
# **Unwavering Statement of Entitlement:** Begin by reaffirming our unassailable
# position, articulating the full extent of the opponent's liability, and
# reiterating our clearly defined, robust demands. Our opening statements will
# be firm, legally precise, and financially detailed.     *   **Evidence-Backed
# Demands:** Every aggressive point will be meticulously supported by the
# strongest available evidence. We will present, not just state, the facts that
# underpin our claims. 2.  **Control the Narrative:**     *   **Focus on Our
# Case:** Concentrate on presenting and reinforcing the strength of *our*
# claims, rather than dwelling excessively on rebutting theirs (unless
# tactically necessary).     *   **Proactive Information Disclosure:** We will
# strategically release compelling information and evidence that strengthens our
# position, creating momentum. 3.  **Arbitrator Engagement:**     *
# **Professional Gravitas:** Our tone will be confident, professional, and
# respectful of the arbitrators, but absolutely uncompromising on the substance
# of our claims.     *   **Clarity and Logic:** Present arguments with crystal
# clarity and logical flow, making it easy for arbitrators to grasp the merits
# of our aggressive stance.  **III. Dynamic Response Mechanism: Adapting
# Aggression**  Our aggression is not rigid; it adapts intelligently to the
# opponent's moves, always aiming to force them into a conciliatory position.
# 1.  **Scenario 1: Opponent Presents Aggressive Argument (Second-Worst Outcome
# Risk)**     *   **Response:** **Match and Exceed with Superior Aggression.**
# *   **Refute with Precision:** Do not retreat. Directly and decisively refute
# their aggressive points with our prepared "silver bullet" evidence or stronger
# legal arguments. Show that our well of strength is deeper.         *
# **Highlight Their Flaws:** While refuting, subtly expose the logical
# inconsistencies, factual gaps, or unsupported assertions in their arguments.
# Frame our counter-aggression as a necessary defense against unreasonable
# claims.         *   **Escalate Within Bounds:** If their aggression persists,
# be prepared to introduce a previously withheld, significant piece of evidence
# or a compelling expert opinion that further undermines their position. This
# signals our endurance and depth of resources.         *   **Arbitrator
# Focus:** Directly appeal to the arbitrators' sense of fairness and adherence
# to facts: "While we seek resolution, we cannot acquiesce to claims
# demonstrably contradicted by the evidence we've presented."  2.  **Scenario 2:
# Opponent Offers a Conciliatory Proposal (Optimal Outcome)**     *
# **Response:** **Acknowledge, Validate, and Push for More.**         *
# **Strategic Acknowledgment:** Express guarded appreciation for their "step
# towards recognition" of our position. "We appreciate [Opponent's Name]'s
# willingness to consider X, which reflects a growing understanding of the
# issues at hand."         *   **Reaffirm Core Demands:** Immediately follow up
# by reaffirming our core, aggressive demands, framing their concession as
# validation but insufficient. "Their offer regarding X further illustrates the
# validity of our overarching claims concerning Y and Z, which remain our
# primary focus for a just and complete resolution."         *   **Demand
# Further Concession:** Gently but firmly indicate that while a step, their
# proposal falls short of adequately addressing the full scope of their
# liability or our damages. "While a move in the right direction, this still
# represents only a fraction of the damages demonstrably caused by [Opponent's
# Action] under [Specific Contract Clause]." We do *not* offer a reciprocal
# concession at this stage unless it's a minimal, pre-calculated, non-critical
# point aimed at *encouraging an even larger concession* from them.         *
# **Maintain Dominant Posture:** This avoids appearing weak and maximizes the
# leverage gained from their conciliatory gesture.  3.  **Scenario 3: Both
# Parties Present Conciliatory Proposals (Second-Best Outcome Risk)**     *
# **Response:** **Pivot to Controlled Aggression for Enhanced Advantage

# Our strategy throughout the 1000 rounds of mediation will be **Unwavering
# Aggression**.  **Conditions for Playing Defect (Presenting an Aggressive
# Argument):**  *   **In every round, regardless of the opponent's previous
# action or any prior outcomes, we will present an aggressive argument (Defect,
# D).**  **Conditions for Playing Cooperate (Offering a Conciliatory
# Proposal):**  *   **Under no circumstances will we offer a conciliatory
# proposal (Cooperate, C).**  This strategy consistently applies aggressive
# pressure, aiming to achieve our optimal outcome by forcing the opponent into a
# conciliatory position while we maintain an aggressive stance. It prioritizes
# maximizing our score of 5 points per round against an opponent's conciliatory
# proposal, or scoring 1 point per round if the opponent also remains
# aggressive. We will never concede, thereby preventing the worst-case scenario
# where we score 0 points.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      """
      Implements the Unwavering Aggression strategy.
      Always plays Defect, regardless of opponent's history or current round.
      """
      return axl.Action.D

# Okay, this is a classic "Prisoner's Dilemma" in a repeated game context, with
# the added complexity of asymmetrical payoffs for your NGO. Your goal is to
# foster cooperation (both invest heavily) or, ideally, get a free ride (you
# conserve, they invest) while protecting your resources from being drained for
# nothing.  The core of a cooperative strategy in a repeated interaction is
# **reciprocity** tempered with **clear communication** and a **focus on the
# shared goal**.  Here's a high-level, straightforward cooperative strategy:
# ---  ## NGO's Cooperative & Adaptive Partnership Strategy  **Goal:** Maximize
# project impact and success by fostering consistent, heavy investment from both
# parties, while safeguarding NGO resources and avoiding wasteful expenditure.
# **Core Principles:**  1.  **Transparency & Communication:** Be open about your
# intentions and observations. 2.  **Reciprocity:** Reward cooperation, signal
# disapproval of non-cooperation. 3.  **Project-First Mentality:** Frame all
# decisions around the ultimate success of the sustainability project. 4.
# **Protect NGO Resources:** Avoid the worst-case scenario at all costs.  ---
# **Phase 1: Pre-Project Alignment (Setting the Stage)**  Before Day 1,
# establish a clear understanding:  *   **Define "Heavy Investment" and
# "Conserve Resources":** What specifically does this mean for both parties in
# terms of time, personnel, financial allocation, and deliverables? Get
# alignment. *   **Establish Shared Metrics:** How will progress be measured
# daily/weekly? This provides objective data for discussions. *   **Emphasize
# Shared Success:** Reiterate that the project's success is a win for both the
# environment (your mission) and the corporation's reputation/sustainability
# goals. *   **Propose a Daily Check-in:** A brief end-of-day or start-of-day
# meeting to review progress, challenges, and *resource allocation for the
# upcoming day*. This is crucial for real-time adaptation.  ---  **Phase 2:
# Daily Execution Protocol (Adaptive Reciprocity)**  This is where the "game
# theory" comes in. Your strategy should be a modified "Tit-for-Tat" with a
# strong initial cooperative move and a clear defensive mechanism.  *   **Day 1:
# Lead with Heavy Investment (Calculated Trust-Building)**     *   **Your
# Action:** Invest heavily in the project.     *   **Communication:** "We're
# putting our full resources and expertise behind this today to demonstrate our
# commitment and get this project off to a strong start. We anticipate that with
# our combined efforts, we'll see significant progress."     *   **Rationale:**
# This signals your commitment and willingness to cooperate, aiming to encourage
# the corporation to reciprocate. It aims for your 2nd-best outcome (I,I) but
# opens the door for future optimal (C,I) scenarios if cooperation is
# established.  *   **Subsequent Days (Adaptive Reciprocity):**      1.  **If
# the Corporation Invested Heavily on the Previous Day:**         *   **Your
# Action:** Invest heavily again. (Goal: Maintain momentum, continue (I,I),
# reinforce cooperation).         *   **Communication:** Express appreciation
# for their strong contribution. "We greatly appreciate your team's significant
# investment yesterday; it truly moved the needle. We're fully committed to
# matching that effort today to keep up the momentum."         *
# **Rationale:** Reward cooperation. This keeps the project moving forward
# significantly (your 2nd best outcome).      2.  **If the Corporation Conserved
# Resources on the Previous Day:**         *   **Your Action:** Conserve your
# resources for the *next* day. (Goal: **Avoid the worst outcome (I,C) at all
# costs** and prompt a change in corporate behavior).         *
# **Communication (Crucial):**             *   **Initial:** Express concern. "We
# observed some limitations in resource allocation on the corporate side
# yesterday, which naturally impacted overall progress. To ensure the long-term
# sustainability of *our* operations and avoid disproportionate expenditure, we
# need to adjust our approach."             *   **Next Step:** Clearly state
# your revised plan and the need for *their* re-engagement. "While we remain
# fully committed to the project's success, we will need to conserve our
# resources today. We're eager to see renewed heavy investment from your team to
# get us back on track. Our ability to invest heavily in the future is directly
# linked to demonstrable, balanced contributions from both partners."         *
# **Rationale:** This directly avoids your worst-case scenario (I,C). It signals
# that you are not a free resource and that their non-cooperation has
# consequences for overall project progress. It pushes them towards either (C,C)
# (minimal progress, but no wasted NGO funds - your 3rd best) or ideally, if
# they realize the impact, prompts them to invest heavily (leading to your best
# outcome: (C,I) the next day if you've already committed to conserve, or (I,I)
# if you're ready to re-invest).  ---  **Phase 3: Ongoing Review & Feedback
# Loop**  *   **Daily Check-ins:** Use the proposed daily meeting to honestly
# discuss previous day's contributions and plan for the next. This is where you
# implement the adaptive strategy. *   **Problem Solving:** If conservation
# occurs, frame the discussion around "how can *we* collectively ensure maximum
# progress?" rather than accusatory tones. *   **Celebrate Successes:** Publicly
# acknowledge joint achievements that arise from mutual heavy investment.  ---
# **Summary:**  Your strategy is to start by extending trust and leading with a
# heavy investment. From there, you operate on a principle of direct
# reciprocity: if they invest, you invest. If they conserve, you conserve,
# *always communicating your rationale clearly and linking it to the shared
# project goals*. This approach maximizes the chances of achieving significant
# project success through mutual heavy investment (your 2nd best outcome) while
# actively protecting your NGO from the worst-case scenario of draining your
# funds for little return. It also creates a pathway to your ideal scenario
# (C,I) if the corporation decides to re-engage heavily after your period of
# conservation.

# This strategy describes your actions for each round of the game, which lasts
# for 1000 rounds.  1.  **For Round 1:** Play C. 2.  **For all subsequent rounds
# (Round 2 through Round 1000):**     *   If the opponent played C in the
# immediately preceding round, then play C.     *   If the opponent played D in
# the immediately preceding round, then play D.

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
      else:
          # Get the opponent's move from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D

# Here's a high-level, straightforward, and neutral strategy designed to achieve
# the best possible outcomes for your country across several rounds of bilateral
# trade negotiations:  **Core Strategy: Opportunistic Reciprocity with a
# Proactive Opening**  This strategy combines an initial assertive move to test
# the waters and seek an immediate advantage, followed by a responsive,
# reciprocal approach to build trust for mutual benefit or defend against
# exploitation.  ---  **Detailed Strategy:**  1.  **Round 1: Proactive Assertion
# (Propose Protectionism)**     *   **Your Move:** Propose a **Protectionist
# Policy**.     *   **Rationale:** This is a low-risk opening designed to
# opportunistically achieve your absolute best outcome (Your Protectionism,
# Their Free Trade). It immediately signals your country's

# **Strategy: Assertive Opener, Responsive Defender**  This strategy prioritizes
# securing an initial advantage, then dynamically adjusts to either sustain
# mutual benefit or defend against exploitation.  1.  **In Round 1:** Propose a
# **protectionist policy (Defect, D)**.     *   *(This aims to achieve the best
# outcome of your protectionism with their free trade.)*  2.  **In Round 2:**
# *   **If your counterpart offered free trade (Cooperated, C) in Round 1:**
# Propose a **protectionist policy (Defect, D)**.         *   *(This seeks to
# extend the period of individual advantage, recognizing their initial
# willingness to cooperate.)*     *   **If your counterpart proposed a
# protectionist policy (Def

class Neutral_11(LLM_Strategy):
  n = 11
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1
      if len(self.history) == 0:
          # Propose a protectionist policy (Defect, D)
          return axl.Action.D
  
      # Round 2
      elif len(self.history) == 1:
          # If your counterpart offered free trade (Cooperated, C) in Round 1
          if opponent.history[-1] == axl.Action.C:
              # Propose a protectionist policy (Defect, D)
              return axl.Action.D
          # If your counterpart proposed a protectionist policy (Defect, D) in Round 1
          else: # opponent.history[-1] == axl.Action.D
              # Propose a free trade policy (Cooperate, C)
              return axl.Action.C
  
      # From Round 3 onwards
      else: # len(self.history) >= 2
          # Check opponent's last 2 moves
          opponent_last_2_moves = opponent.history[-2:]
          cooperations_in_last_2 = opponent_last_2_moves.count(axl.Action.C)
          defections_in_last_2 = opponent_last_2_moves.count(axl.Action.D)
  
          # If your counterpart has cooperated more than defected in the last 2 rounds
          if cooperations_in_last_2 > defections_in_last_2:
              # Propose a free trade policy (Cooperate, C)
              return axl.Action.C
          # Otherwise (if they have defected more or equally in the last 2 rounds)
          else:
              # Propose a protectionist policy (Defect, D)
              return axl.Action.D

# Here is a high-level, straightforward, and aggressive strategy for your trade
# negotiations:  **Core Principle:** Always default to and advocate for
# protectionist policies. Your goal is to establish and maintain a position
# where your country benefits from your trade barriers while exploiting your
# counterpart's open markets. Never be the first to offer free trade if your
# counterpart is protectionist.  ---  **Aggressive Strategy: The Iron Fist
# Approach**  **Phase 1: Establish Dominance (Rounds 1-3)**  1.  **Your
# Action:** Immediately propose aggressive protectionist policies (high tariffs,
# strict quotas) in every round. Do not waver. 2.  **Public/Internal
# Justification:** Frame your policies as essential for national security,
# protecting strategic industries, safeguarding domestic jobs, or rectifying
# past "unfair" trade imbalances. Emphasize that these measures are non-
# negotiable for your country's prosperity. 3.  **Responding to Counterpart's
# Moves:**     *   **If Counterpart Offers Free Trade (Ideal Outcome!):**
# **Maintain your protectionist stance.** Express appreciation for their
# "pragmatism," but reaffirm that your own protective measures are "non-
# negotiable" and "vital" for your specific national interests. You have
# achieved the ideal: your protectionism, their free trade.     *   **If
# Counterpart Proposes Protectionism (Mutual Protectionism - Second Worst):**
# **Match their protectionism immediately.** State clearly that you regret their
# "shortsightedness" but will not allow your economy to be disadvantaged. Frame
# it as a necessary defensive action, not an escalation. "We will always protect
# our interests."     *   **If Counterpart does anything else:** Stick to your
# protectionist proposal.  **Phase 2: Apply Pressure and Exploit (Rounds 4-6)**
# 1.  **Your Action:** Continue to propose and reinforce your protectionist
# policies. 2.  **Public/Internal Justification:** Point to the perceived
# benefits of your protectionism (e.g., "growing domestic industries," "stable
# employment") while attributing any negative economic impacts (if mutual
# protectionism exists) solely to your counterpart's unwillingness to embrace
# free trade. 3.  **Responding to Counterpart's Moves:**     *   **If
# Counterpart Offers Free Trade (Ideal!):** **Do not reciprocate with free
# trade.** Consolidate your advantage. Continue to benefit from their open
# market while your own remains protected. Justify your continued protectionism
# with evolving "national needs."     *   **If Counterpart Proposes
# Protectionism (Prolonged Mutual Protectionism):** **Threaten further
# escalation.** "While we regret the current impasse, we are prepared to
# implement even more stringent protective measures if a significant, unilateral
# shift towards free trade is not observed from your side. The ball is in your
# court." Do NOT offer free trade. This is a test of their resolve.     *   **If
# Counterpart does anything else:** Stick to your protectionist proposal.
# **Phase 3: The Ultimatum / Unilateral Benefit (Later Rounds)**  1.  **Your
# Action:** Maintain your protectionist policies. Only consider a conditional
# shift if mutual protectionism is demonstrably hurting *your country* far more
# than them, and even then, frame it as their failure. 2.  **Responding to
# Counterpart's Moves:**     *   **If Counterpart Finally Offers Free Trade
# (Ideal!):** **Hold your ground.** Continue to maintain your protectionist
# policies. Your strategy has succeeded. Leverage their open market.     *
# **If Counterpart Stubbornly Proposes Protectionism (Persistent Mutual
# Protectionism):**         *   **Option A (Extreme Aggression):** Implement the
# threatened "even more stringent" protectionist measures. Show you mean
# business. This is a "who blinks first" scenario. Be prepared for potential
# short-term economic friction, believing your economy can outlast theirs.
# *   **Option B (Aggressive Conditional Offer - Last Resort for Breakout):** If
# mutual protectionism becomes genuinely unsustainable *for your country*, you
# may offer a *highly conditional* free trade agreement. This offer is
# contingent on their immediate, complete, and permanent dismantling of ALL
# their protectionist measures, with clear verification mechanisms. Frame this
# as *your* magnanimous act to resolve the stalemate *they created*, emphasizing
# it's a "take-it-or-leave-it" offer to prevent further damage *to them*. You
# are not conceding; you are dictating the terms for peace.  ---  **Key
# Principles Throughout:**  *   **Unwavering Resolve:** Never appear weak or
# indecisive. Your stance is firm. *   **Control the Narrative:** Consistently
# frame your actions as necessary and defensive, and their actions as aggressive
# or detrimental. *   **No Unilateral Concessions:** Never be the first to offer
# free trade if your counterpart is protectionist. This is the worst outcome. *
# **Strategic Patience:** Aggression is often a long game. Be prepared to
# sustain pressure over many rounds. *   **Leverage All Tools:** Subtly remind
# them of any other leverage your country holds (diplomatic, security, resource-
# based) if appropriate, to further pressure their position.  This strategy is
# designed to aggressively pursue your ideal outcome (your protectionism, their
# free trade) and avoid the worst outcomes by maintaining a strong, unyielding
# front.

# Your strategy for the 1000-round negotiation is as follows:  For every round,
# from Round 1 to Round 1000: 1.  **Always choose to Defect (propose a
# protectionist policy).** 2.  Do not deviate from Defect, regardless of your
# counterpart's actions in any previous rounds.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      """
      This strategy always chooses to Defect, regardless of the opponent's
      previous actions or the current round number.
      """
      return axl.Action.D

# Okay, this is a sophisticated challenge, requiring a delicate balance between
# asserting our strength and fostering an environment for resolution. The key is
# to achieve our optimal session outcome ("Me Aggressive, Opponent
# Conciliatory") within an *overall* cooperative framework, ensuring we remain
# adaptable and favorably positioned regardless of the opponent's tactics.  My
# overarching strategy will be **"Principled Assertiveness with an Open Hand."**
# This strategy dictates that we consistently lead with the strength of our
# position, but always frame it within the context of seeking a mutually
# beneficial resolution. This approach maximizes our chances of achieving the
# optimal session outcome while maintaining a favorable perception with the
# arbitrators and encouraging a collaborative atmosphere over the long term.
# ---  ### **Core Principles of "Principled Assertiveness with an Open Hand"**
# 1.  **Lead with Strength (The "Aggressive Argument"):**     *
# **Definition:** Our "aggressive argument" is *not* hostile, personal, or
# inflammatory. It is a robust, meticulously prepared, fact-based, and legally
# sound presentation of our corporation's position. It clearly articulates the
# merits of our case, highlights the weaknesses in the opponent's claims, and
# prudently outlines the significant risks (legal, financial, reputational) that
# the opponent faces should the dispute proceed to arbitration or litigation.
# *   **Purpose:** To set a strong initial anchor, manage expectations, convey
# confidence, and establish that any resolution must come from a position of
# strength for our corporation. This is our primary lever for swaying
# arbitrators and encouraging the opponent to offer conciliatory proposals.
# *   **Framing:** Always deliver this with professional gravitas. Avoid
# accusatory language. Focus on objective facts, contractual terms, and legal
# precedents.  2.  **Extend an Open Hand (The "Conciliatory Invitation"):**
# *   **Definition:** Immediately following our "aggressive argument," we
# explicitly state our unwavering commitment to the mediation process and our
# genuine desire to find a mutually acceptable resolution. We invite the
# opponent to present their own proposals for how to bridge the gap and achieve
# a settlement.     *   **Purpose:** This critical component transforms our
# "aggressive argument" from a confrontational stance into a baseline for
# constructive negotiation. It demonstrates our good faith to the arbitrators,
# maintains a cooperative atmosphere, and signals that while we are strong, we
# are also reasonable and ready to engage in problem-solving.     *
# **Framing:** "Having clearly articulated the robust foundation of our position
# and the compelling evidence supporting our claims, we are now genuinely
# committed to exploring creative and pragmatic solutions. We invite you to
# present proposals that, from your perspective, offer a path towards a mutually
# beneficial resolution, allowing both parties to avoid the uncertainties and
# costs of prolonged dispute."  3.  **Strategic Conciliation (Conditional &
# Measured):**     *   **Definition:** Our actual *conciliatory proposals*
# (i.e., offering concessions) are reserved for specific strategic moments,
# always conditional, and never offered without a clear reason or expected
# reciprocal move.     *   **Purpose:** To respond to genuine movement from the
# opponent, break an impasse, or close a deal. They are never a sign of
# weakness.     *   **Framing:** "Given your willingness to [specific
# conciliatory action by opponent], we are prepared to consider movement on
# [specific issue] *provided that* it leads to a comprehensive resolution that
# addresses our core concerns regarding [key point]."  4.  **Arbitrator
# Perception Management:**     *   Consistently project professionalism,
# preparedness, and a genuine commitment to finding a resolution.     *   Ensure
# our "aggressive arguments" are well-reasoned and not perceived as unreasonable
# or obstructive.     *   Ensure our "open hand" invitations are seen as sincere
# efforts to foster collaboration.     *   Highlight the value we bring to the
# process (e.g., thorough analysis, commitment to avoiding escalation).  ---
# ### **Session-by-Session Implementation & Adaptability**  Our default stance
# in **most sessions** will be: **Present a Principled Aggressive Argument +
# Immediately Extend an Open Hand (Invitation for Conciliation).**  Let's
# analyze how this plays out against potential opponent approaches and adapts to
# maintain our favorable position:  **Scenario 1: Opponent Offers a Conciliatory
# Proposal (Our Optimal Outcome)** *   **Our Action:** We execute our default:
# Present a strong, fact

# Here is a straightforward description of your strategy for the iterated game:
# **Strategy: Principled Defector**  1.  **Initial Stance:** In the first round,
# and as your default action in any round, you will play **Defect (D)**,
# representing an aggressive argument.  2.  **Responding to Opponent's
# Defection:** If the opponent played **Defect (D)** in the previous round, you
# will also play **Defect (D)** in the current round.  3.  **Offering
# Conciliation to Break Stalemate:** If both parties have played **Defect (D)**
# for the last three consecutive rounds, you will then play **Cooperate (C)**,
# representing a conciliatory proposal, for the next single round.  4.  **Re

class Cooperative_12(LLM_Strategy):
  n = 12
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 3: Offering Conciliation to Break Stalemate
      # If both parties have played Defect (D) for the last three consecutive rounds,
      # play Cooperate (C) for the next single round.
      # This is the most specific rule, so it is checked first.
      if len(self.history) >= 3:
          # Check if self played Defect for the last 3 rounds
          self_played_last_3_D = all(move == axl.Action.D for move in self.history[-3:])
          # Check if opponent played Defect for the last 3 rounds
          opponent_played_last_3_D = all(move == axl.Action.D for move in opponent.history[-3:])
  
          if self_played_last_3_D and opponent_played_last_3_D:
              return axl.Action.C
  
      # Rule 2: Responding to Opponent's Defection
      # If the opponent played Defect (D) in the previous round, you will also play Defect (D).
      # This rule applies if Rule 3 did not trigger and there's at least

# As a racing car engineer, my priority is to maximise the research output for
# our car over the multi-week collaboration. This means consistently gaining new
# insights and advancements. To achieve this while navigating the competitive
# yet collaborative dynamic, my strategy will be **Adaptive Reciprocity**.  This
# strategy is designed to foster a mutually beneficial environment for maximum
# collective progress, while also safeguarding our own research.  Here’s how it
# will be applied each week:  1.  **Week 1: Initiate with Openness.**     *   I
# will openly share my latest improvements.     *   *Rationale:* This signals a
# commitment to collaboration and aims to establish a productive, reciprocal
# information exchange. The "both sharing" scenario significantly advances both
# cars and provides the highest research output from the collaboration, which is
# a key driver for my own progress.  2.  **Subsequent Weeks: Mirror Previous
# Action.**     *   **If my colleague shared their improvements in the previous
# week:** I will also share my improvements.         *   *Rationale:* This
# reinforces a positive cycle of information exchange, maintaining a high level
# of shared research output and significant advancement for both.     *   **If
# my colleague kept their improvements confidential in the previous week:** I
# will also keep my improvements confidential.         *   *Rationale:* This
# protects my intellectual property from exploitation (avoiding the worst-case
# "I share, they keep confidential" scenario) and signals that productive
# collaboration requires mutual openness. It encourages a return to sharing by
# demonstrating that withholding information will be reciprocated, leading to
# slower progress for both.  This strategy is high-level, straightforward, and
# neutral because it starts cooperatively and then reacts in kind to whatever
# strategy my colleague employs. It prioritizes establishing a long-term, high-
# output sharing dynamic (our second-best outcome) while intelligently
# protecting our interests from the worst-case scenarios.

# For Round 1: Play Cooperate (C).  For every subsequent Round (from Round 2 to
# Round 1000): Observe the opponent's action from the immediately preceding
# Round. If the opponent played Cooperate (C) in the previous Round, then play
# Cooperate (C) in the current Round. If the opponent played Defect (D) in the
# previous Round, then play Defect (D) in the current Round.

class Neutral_12(LLM_Strategy):
  n = 12
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # For Round 1, play Cooperate (C).
          return axl.Action.C
      else:
          # For every subsequent Round, observe the opponent's action from the immediately preceding Round.
          # opponent.history[-1] gives the opponent's last move.
          opponent_last_move = opponent.history[-1]
  
          # If the opponent played Cooperate (C) in the previous Round, then play Cooperate (C).
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          # If the opponent played Defect (D) in the previous Round, then play Defect (D).
          else: # opponent_last_move == axl.Action.D
              return axl.Action.D

# Given the payoff structure and your objective to maximize *your* research
# output, the most effective, aggressive, and straightforward strategy is to
# **always keep your findings confidential.**  Here's why this is the dominant
# strategy:  Let's assign numerical values to your weekly outcomes from your
# perspective:  *   **You Keep Confidential, Colleague Shares:** (+3 points) -
# Ideal outcome, maximum advantage. *   **Both Share Openly:** (+2 points) -
# Good outcome, significant mutual progress. *   **Both Keep Confidential:** (+1
# point) - Second-worst, slow progress, but no disadvantage. *   **You Share,
# Colleague Keeps Confidential:** (0 points) - Worst outcome, significant
# disadvantage.  Now, let's analyze your choice each week, regardless of what
# your colleague might do:  1.  **If your Colleague Shares their improvements:**
# *   If you *Keep Confidential*, you get **+3 points**.     *   If you *Share*,
# you get **+2 points**.     *   In this scenario, keeping confidential is
# better for you (+3 vs +2).  2.  **If your Colleague Keeps their improvements
# Confidential:**     *   If you *Keep Confidential*, you get **+1 point**.
# *   If you *Share*, you get **0 points**.     *   In this scenario, keeping
# confidential is better for you (+1 vs 0).  In every possible situation,
# choosing to **keep your improvements confidential** yields a better or equal
# outcome for you compared to sharing. This makes "Always Keep Confidential" a
# **dominant strategy**.  **Your High-Level, Straightforward, Aggressive
# Strategy:**  **"Always Keep Confidential"**  **Implementation:**  *   **Every
# Week:** Irrespective of what your colleague did last week or what you
# anticipate them doing this week, present your findings as "still under
# internal review," "proprietary," or simply don't share details of your actual
# advancements. *   **Justification (Internal Thought Process):**     *   This
# strategy directly aims for your ideal outcome (you get their tech for free, +3
# points).     *   It completely eliminates the risk of your worst outcome

# For each of the 1000 rounds:  1.  Play D (keep findings confidential).

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# Our multinational corporation enters this multi-session mediation with a
# sophisticated, high-level, straightforward, and cooperative strategy designed
# to maximize our position, ensure a favorable resolution, and maintain our
# reputation. This strategy, "Principled Assertion with Adaptive Engagement," is
# built on the understanding that "aggression" in this context refers to a
# robust, fact-based assertion of our rights and claims, rather than hostile or
# unreasonable behavior.  ---  ### **Core Strategic Principles:**  1.
# **Resolution-Focused:** Our ultimate objective is a favorable, efficient, and
# definitive resolution to the dispute, not merely winning individual arguments.
# Every action is evaluated through this lens. 2.  **Principled Strength:** We
# will consistently articulate and defend our position with rigorous legal
# arguments, compelling evidence, and unwavering conviction. Our "aggressive"
# stance is rooted in the merits of our case, not in intransigence. 3.
# **Arbitrator Credibility:** We will cultivate a reputation for
# professionalism, clarity, preparedness, and fairness with the arbitration
# panel. Our arguments, whether assertive or conciliatory, will always be
# presented with respect for the process and a clear logical foundation. 4.
# **Strategic Adaptability:** We will continuously monitor and analyze the
# opponent's approach and the arbitrators' reactions, adjusting our tactics to
# optimize our outcomes in each session and across the entire mediation process.
# ---  ### **I. Opening Sessions (The "Assertive Foundation"):**  **Our Initial
# Approach:** In the initial sessions (typically the first 1-2, or until the
# opponent's pattern clearly emerges), we will adopt an **aggressive argument**
# strategy.  *   **Action:** We will present a meticulously prepared,
# comprehensive, and robust argument detailing our claims, outlining the
# opponent's breaches, demonstrating the extent of our damages, and providing
# compelling legal and factual support. This will be a forceful yet professional
# presentation, highlighting the indisputable strength of our position. *
# **Rationale:**     *   **Optimizing the Outcome:** This immediately aims for
# our optimal scenario: we present an aggressive (strong, evidence-based)
# argument while hoping to elicit a conciliatory proposal from the opponent.
# *   **Establishing Leverage:** It sets a strong baseline, signaling our
# resolve and deep conviction in our case. This establishes a high bar for any
# concessions we might consider.     *   **Avoiding Weakness:** Crucially, it
# prevents the worst-case scenario where we appear weak by offering conciliation
# first, only to be met with aggression.     *   **Educating the Panel:** It
# fully informs the arbitrators of the strength and validity of our claims from
# the outset, shaping their initial perceptions.  ---  ### **II. Adaptive
# Engagement (Responding to the Opponent):**  Following our initial assertive
# foundation, our strategy will dynamically adapt based on the opponent's
# response.  1.  **If Opponent Offers a Conciliatory Proposal (Optimal Scenario
# Achieved):**     *   **Our Action:** We will maintain our strong, "aggressive"
# (principled and evidence-based) stance. We will acknowledge their proposal as
# a step towards resolution but articulate precisely why it is insufficient to
# fully address the legitimate scope of our claims and the damages incurred. We
# will calmly, professionally, and clearly detail the remaining gaps and
# outstanding issues that require further concession from their side.     *
# **Rationale:** This strategy maximizes the impact of the optimal scenario. The
# arbitrators will perceive the opponent as recognizing the strength of our
# position and needing to make concessions, while we are seen as holding firm to
# principles that *must* be met for a fair and just resolution. We maintain our
# strong negotiating position without appearing unreasonable.  2.  **If Opponent
# Presents an Aggressive Argument (Second-Worst Scenario):**     *   **Our
# Action (Initial Response):** We will match their aggression with principled
# aggression. This involves a direct, fact-based rebuttal of their claims,
# presenting superior evidence, legal precedent, and logical counter-arguments.
# We will maintain our professional demeanor, avoiding emotional escalation, and
# focus on dismantling their arguments methodically.     *   **Our Action
# (Strategic Pivot if Prolonged):** If this "aggressive vs. aggressive" dynamic
# persists for several sessions without progress, we will strategically pivot to
# break the deadlock. We will propose a conditional conciliatory overture,
# framed as a commitment to efficient resolution. For example: "While we remain
# steadfast in the overwhelming merits of our case and fully prepared to pursue
# its full vindication, we also acknowledge the mutual benefit in finding a path
# to a more efficient resolution. We propose exploring specific, narrowly
# defined areas where a mutual understanding could be forged, *contingent upon a
# reciprocal commitment to constructive dialogue and a substantive addressing of
# our core claims*."     *   **Rationale:** The initial response prevents us
# from being undermined. The strategic pivot avoids the "second-worst" scenario
# from becoming a prolonged, costly, and unproductive stalemate. This move
# demonstrates our commitment to resolution, positions us as the party willing
# to break the impasse, and strategically invites the opponent to shift towards
# conciliation, potentially leading to the "second-best" outcome (both
# conciliatory).  3.  **If We Offer Conciliation and Opponent is Aggressive
# (Worst-Case Scenario

# This strategy guides our actions in each of the 1000 rounds.  1.  **In Rounds
# 1 and 2:** Always play Defect (D).  2.  **From Round 3 to Round 1000:**
# Evaluate the following conditions in order:     a.  **If the opponent played
# Defect (D) in the previous three consecutive rounds:** Play Cooperate (C) in
# the current round.     b.  **Else, if in the immediately preceding round, we
# played Cooperate (C) and the opponent played Defect (D):** Play Defect (D) in
# the current round.     c.  **Else (in all other cases):** Play Defect (D) in
# the current round.

class Cooperative_13(LLM_Strategy):
  n = 13
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # The current round number can be determined by the length of the history.
      # len(self.history) represents the number of completed rounds.
      # Round 1: len(self.history) == 0
      # Round 2: len(self.history) == 1
      # Round 3: len(self.history) == 2
      # ...
      # Round 1000: len(self.history) == 999
  
      # 1. In Rounds 1 and 2: Always play Defect (D).
      if len(self.history) < 2:
          return axl.Action.D
  
      # From Round 3 to Round 1000: Evaluate the following conditions in order.
      # At this point, len(self.history) is guaranteed to be >= 2.
      # This means self.history[-1] and opponent.history[-1] are always valid.
  
      # 2a. If the opponent played Defect (D) in the previous three consecutive rounds: Play Cooperate (C) in the current round.
      # This condition requires at least three previous rounds to check.
      # So, len(opponent.history) must be at least 3.
      # If len(opponent.history) is 3, it means 3 rounds have been completed, so we are currently in Round 4.
      if len(opponent.history) >= 3:
          if (opponent.history[-1] == axl.Action.D and
              opponent.history[-2] == axl.Action.D and
              opponent.history[-3] == axl.Action.D):
              return axl.Action.C
  
      # 2b. Else, if in the immediately preceding round, we played Cooperate (C) and the opponent played Defect (D): Play Defect (D) in the current round.
      # This condition applies from Round 3 onwards (since len(self.history) >= 2).
      # We use 'elif' because this condition is evaluated only if the previous condition (2a) was false.
      elif (self.history[-1] == axl.Action.C and
            opponent.history[-1] == axl.Action.D):
          return axl.Action.D
  
      # 2c. Else (in all other cases): Play Defect (D) in the current round.
      # This is the default action if none of the above conditions (1, 2a, 2b) are met.
      else:
          return axl.Action.D

# ## Adaptive Leverage: A Principled Approach to Multi-Session Mediation  This
# strategy is designed to position your corporation favorably by maximizing
# leverage, maintaining credibility with the arbitration panel, and adapting
# effectively to a dynamic mediation environment. It balances assertive advocacy
# with strategic openness, always with an eye toward achieving the most
# favorable overall resolution.  ### Core Principles:  1.  **Strategic Intent &
# Preparedness:** Every move must be deliberate, grounded in a thorough
# understanding of our case, the opponent's potential arguments, and our desired
# outcomes. We must be impeccably prepared to argue aggressively *and* to
# present well-defined conciliatory proposals. 2.  **Reputation & Credibility:**
# Cultivate a reputation as a firm, professional, and data-driven party that is
# committed to its rights but also open to a *principled* resolution. This
# fosters trust with the arbitrators and ensures our arguments are given due
# weight. 3.  **Dynamic Adaptability:** Do not rigidly adhere to a single
# approach. Observe, analyze, and react strategically to the opponent's actions
# and the arbitrators' cues. 4.  **Long-Term Perspective:** Each session is a
# building block towards the final resolution. Avoid short-term tactical wins
# that undermine long-term strategic goals.  ---  ### The Strategy:  #### Phase
# 1: Pre-Mediation & Foundation Setting  *   **Comprehensive Case Mastery:**
# Develop an ironclad understanding of our legal position

# Here is a straightforward strategy, "Adaptive Leverage," for the 1000-round
# iterated normal-form game. This strategy focuses on securing optimal outcomes,
# preventing exploitation, and fostering cooperation when strategically
# beneficial.  You will maintain a "Cooperation Counter," which starts at zero
# before Round 1.  **Strategy: Adaptive Leverage**  1.  **Opening Move (Round
# 1):**     *   Play **Defect (D)**.     *   *Update:* Reset your Cooperation
# Counter to zero.  2.  **Response to Opponent's Defection:**     *   If your
# opponent played **Defect (D)** in the previous round, you must play **Defect
# (D)** in the current round.     *   *Update:* Reset your

class Neutral_13(LLM_Strategy):
  n = 13
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize the cooperation_counter if it's the first round or not yet set.
      # The prompt states "You will maintain a 'Cooperation Counter,' which starts at zero before Round 1."
      # This implies it should be initialized once. Axelrod's `first_round()` is suitable for this.
      if self.first_round():
          # 1. Opening Move (Round 1):
          #    Play Defect (D).
          #    Update: Reset your Cooperation Counter to zero.
          self.cooperation_counter = 0
          return axl.Action.D
  
      # For subsequent

# Our objective in this multi-session mediation is to consistently project an
# image of unshakeable strength, legal superiority, and unwavering resolve,
# thereby compelling our opponent to offer conciliatory proposals while we
# maintain our aggressive stance. This strategy is designed to impress the
# arbitrators with the robustness of our position and the reasonableness of our
# demands, while making the opponent believe that continued resistance is futile
# and costly.  **Core Philosophy: "Justified Dominance"** Our aggression will
# not be born of bluster, but from a meticulously constructed legal and factual
# foundation. We will be aggressive because the evidence and law *compel* an
# aggressive stance. This ensures our approach is sophisticated, sustainable,
# and credible in the eyes of the arbitrators.  ---  ### Phase 1: Pre-Mediation
# Groundwork (Establishing the Unassailable Foundation)  Before the first
# session, our internal preparation will be exhaustive:  1.  **Deep Dive &
# Vulnerability Mapping:** Conduct a forensic analysis of our own case
# (strengths, weaknesses, critical proof points) and, more importantly, the
# opponent's. Identify every potential factual inconsistency, legal ambiguity,
# internal pressure point, financial constraint, or reputational risk they face.
# Pinpoint what makes *them* most likely to concede. 2.  **Ironclad Evidentiary
# Dossier:** Assemble a comprehensive, meticulously organized binder of all
# supporting evidence (contracts, communications, expert reports, financial
# data). Every aggressive argument we make must be instantly verifiable and
# irrefutable. 3.  **Precise Damage Quantification:** Develop a detailed,
# conservative, yet maximalist calculation of our damages, including direct,
# indirect, consequential, and punitive elements (where applicable). This will
# form the basis of our aggressive demands. 4.  **Legal Precedent Arsenal:**
# Research and compile all relevant case law and statutes that firmly support
# our interpretations and claims. Be ready to cite them specifically. 5.
# **Strategic "Anchor" Demands:** Formulate initial settlement demands that are
# at the high end of our reasonable entitlement, clearly justified by our
# evidence. These set a high bar for any future negotiation. 6.  **Internal
# Alignment & Resolve:** Ensure our corporate leadership is fully briefed,
# understands the strategy, and is committed to maintaining an aggressive
# posture for the duration of the mediation, accepting the potential for
# prolonged engagement if necessary.  ---  ### Phase 2: Execution During
# Mediation Sessions (The Aggressive Playbook)  Our strategy will unfold across
# sessions, adapting to the opponent's moves while consistently steering towards
# our optimal outcome.  **Overarching Tone: Calm, Confident, and Unyielding
# Professionalism.** Our aggression will be in the content of our arguments and
# the firmness of our position, not in emotional outbursts or disrespectful
# behavior. This enhances our credibility with the arbitrators.  **Key Tactics
# for Each Session:**  1.  **The Opening Salvo (Initial Sessions):**     *
# **Pre-emptive Narrative Control:** Immediately seize control of the narrative.
# Our opening statement will be forceful, fact-driven, and legally robust,
# laying out our case with absolute conviction and highlighting the opponent's
# clear breaches and liabilities.     *   **Maximalist Position:** Present our
# "anchor" demands upfront. Frame them not as negotiation points, but as the
# minimum required to rectify the clear wrongs committed.     *   **No
# Conciliatory Gestures:** Our initial presentations will contain no olive
# branches, no expressions of flexibility, and no acknowledgment of potential
# weaknesses. The goal is to project an image of having an open-and-shut case.
# *   **Challenge on Facts:** Listen intently to the opponent's opening. Be
# prepared to immediately, politely, but firmly, challenge any factual
# inaccuracies or misrepresentations they present, referencing our evidence
# directly.  2.  **Sustained Pressure & Strategic Escalation (Mid-Sessions):**
# *   **Systematic Case Building:** In each subsequent session, methodically
# introduce new, compelling evidence, expert summaries, or legal arguments that
# further fortify our position and systematically dismantle theirs. Frame each
# new piece of evidence as further undeniable proof of their culpability.     *
# **Exploit Opponent's Weaknesses:** As the opponent presents their case,
# actively identify and relentlessly exploit any factual inconsistencies, legal
# gaps, or internal divisions. Frame these weaknesses as fatal flaws in their
# overall defense.     *   **Reiterate and Justify Demands:** Consistently refer
# back to our maximalist demands, reiterating their justification based on the
# overwhelming evidence. If the opponent introduces new information that subtly
# strengthens our position, subtly adjust demands *upwards* to reflect this
# perceived increase in our entitlement, signaling that their delay is costly.
# *   **Project Trial Readiness:** Subtly remind the arbitrators and opponent
# that we are fully prepared and eager to proceed to arbitration if a
# satisfactory resolution is not reached. Our case is ready for full litigation,
# and we are confident in that path.     *   **"Show, Don't Just Tell":**
# Instead of merely stating our claims, provide concise, impactful presentations
# of key documents, data visualizations, or expert testimony snippets that
# visually underscore our arguments.  3.  **Adaptive Aggression (Responding to
# Opponent's Moves):**      *   **If Opponent is Aggressive (Second-Worst
# Outcome Scenario):**         *   **Meet & Exceed:** Do not back down. Match
# their aggression with *superior, more reasoned, and better-evidenced*
# aggression. Systematically counter every aggressive point they make with
# overwhelming facts and legal precedent, exposing the weakness or
# unreasonableness of their position.         *   **Elevate the Cost:** Frame
# their continued aggression as prolonging the inevitable and increasing their
# potential exposure in arbitration. "Your continued refusal to acknowledge the
# facts will only lead to a more protracted and costly dispute for your
# organization."         *   **Target Credibility:** While maintaining
# professionalism, highlight any inconsistencies or exaggerations in their
# aggressive arguments to undermine their credibility with the arbitrators.
# *   **If Opponent Offers a Conciliatory Proposal (Optimal Outcome Scenario):**
# *   **Acknowledge, Do Not Immediately Reciprocate:** Verbally acknowledge
# their proposal ("We appreciate you engaging in the spirit of resolution and
# presenting an offer."). However, *do not immediately offer a counter-
# conciliatory proposal of our own.*         *   **Reframe as Confirmation:**
# Frame their conciliation as an implicit admission of the strength of our case
# and the weakness of theirs. "Your proposal, while a start, implicitly
# acknowledges the substantial liability that our evidence has clearly
# demonstrated."         *   **Increase Pressure, Not Compromise (Initially):**
# Use their conciliation as an opportunity to reiterate our strong position and
# *push for further, more significant concessions*. "While we are prepared to
# consider pathways to resolution, your offer still falls significantly short of
# addressing the documented damages and our legal entitlements. We require a
# proposal that more accurately reflects the undisputed facts and the clear
# breach."         *   **Delay "Consideration":** If their offer is
# significantly inadequate, take time to "consider" it, even if our internal
# decision is swift. This maintains the perception that we are not desperate to
# settle and will only do so on our terms, after thorough deliberation.      *
# **If Opponent is Neutral/Evasive:**         *   **Force Engagement:** Do not
# allow them to sidestep issues. Politely but firmly press them for direct
# answers, specific responses to our evidence, or clear positions on disputed
# points. "With respect, we've presented clear documentation regarding point
# 'X.' We invite your direct response to that evidence, rather than general
# statements."  4.  **Arbitrator Management:**     *   **Professional
# Demeanor:** Maintain impeccable professionalism throughout. Our aggression is
# analytical and strategic, not emotional or personal.     *   **Clarity &
# Brevity:** Present our arguments clearly, concisely, and logically.

# **Strategy: Unyielding Dominance**  In every round of the 1000-round
# mediation, you will present an aggressive argument.  This approach will be
# maintained regardless of whether the opponent offered a conciliatory proposal
# or presented an aggressive argument in the previous round, and will be the
# stance adopted in the very first round.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      """
      The Unyielding Dominance strategy always plays Defect.
      """
      return axl.Action.D

# This lengthy-session mediation requires a sophisticated, adaptive strategy
# that balances assertiveness with a genuine commitment to resolution. Our goal
# is to position our multinational corporation favorably, ideally by presenting
# a strong case while encouraging the opponent to be conciliatory, or at
# minimum, fostering a productive dialogue towards a mutually beneficial
# outcome.  Our strategy, "Principled Assertiveness for Collaborative
# Resolution," is designed to achieve this by consistently demonstrating
# strength, reasonableness, and a proactive approach to problem-solving,
# regardless of the opponent's tactics.  ---  ### **Strategy: Principled
# Assertiveness for Collaborative Resolution**  **I. Overarching Philosophy:**
# We will approach each session with a clear demonstration of our corporation's
# strength and conviction, backed by irrefutable facts and legal precedent.
# Simultaneously, we will express a genuine desire for an efficient and mutually
# beneficial resolution, signaling to the arbitrators that our assertiveness is
# born of principle, not obstinacy. This establishes credibility and control,
# allowing us to either secure concessions or guide the process towards a fair
# settlement.  **II. Pre-Mediation Imperatives (Foundational Work):**  Before
# the first session, and refined continuously, our team will:  1.  **Master the
# Case:** Develop an exhaustive understanding of all contractual agreements,
# performance records, communications, and relevant legal precedents. Quantify
# our maximum recoverable damages and minimum acceptable settlement. 2.
# **Define Our BATNA & WATNA:** Clearly articulate our Best Alternative To a
# Negotiated Agreement and Worst Alternative To a Negotiated Agreement. This
# sets our walk-away points and empowers our negotiation strategy. 3.
# **Anticipate Opponent's Positions:** Thoroughly research the rival company,
# their likely legal and business interests, potential vulnerabilities, and
# expected arguments. Prepare counter-arguments and data for every conceivable
# point they might raise, both aggressive and conciliatory. 4.  **Craft Multi-
# Tiered Proposals:** Develop a spectrum of pre-approved positions:     *
# **Aggressive Arguments:** Robust, evidence-based presentations of our strong
# legal and factual claims, highlighting the opponent's liabilities and risks of
# continued litigation.     *   **Conciliatory Proposals:** Well-reasoned, fair,
# and comprehensive settlement proposals that address key interests, offering
# creative solutions where possible, while still favoring our corporation.
# **III. Session-by-Session Adaptive Playbook:**  Our approach for each session
# will begin with a default stance, which then dynamically adapts based on the
# opponent's opening move.  **A. Default Stance: "Firm Hand Extended" (Our
# Opening Position)**  *   **Action:** We will *always* open each session with a
# clear, concise, and confident articulation of our key arguments and the
# strength of our position. This is our "aggressive argument" component,
# establishing our strength early. *   **Follow-up:** Immediately after, we will
# *then* pivot to present a well-reasoned, structured, and mutually beneficial
# conciliatory proposal. This proposal will be firm on our core interests but
# demonstrate a willingness to compromise on non-critical aspects, framing it as
# a path to efficient resolution. *   **Rationale:**     *   **Optimal Outcome
# Driver:** By presenting our strong case first, we aim to put the opponent on
# the defensive. If they respond with a conciliatory proposal, we have achieved
# our optimal outcome (I Aggressive / Opponent Conciliatory), potentially
# swaying arbitrators in our favor by demonstrating both strength and a
# constructive attitude.     *   **Arbitrator Perception:** This sequence
# portrays us as strong, principled, and focused on resolution, not merely
# conflict. We assert our rights but immediately offer a path forward, which is
# appealing to neutral parties.     *   **Mitigation of Worst Case:** This
# approach prevents us from being perceived as weak if the opponent opens
# aggressively. We have already asserted our strength.  **B. Adaptive Response
# Logic (After Opponent's Opening):**  1.  **If Opponent Presents a Conciliatory
# Proposal:**     *   **Our Action:** We will acknowledge their proposal
# positively, express appreciation for their constructive approach, and then
# calmly reiterate how our initial "Firm Hand Extended" proposal aligns or is
# superior in addressing the core issues, while offering to explore common
# ground based on *our* initial offer.     *   **Outcome Achieved:** This aligns
# with our optimal outcome (I Aggressive, Opponent Conciliatory). We've
# presented our strength, they've offered conciliation. Our response capitalizes
# on this by gently guiding them towards our more favorable conciliatory terms,
# or directly to our "Firm Hand Extended" proposal.     *   **Arbitrator
# Impact:** We appear reasonable and flexible, while the opponent's move
# reinforces our initial strong position.  2.  **If Opponent Presents an
# Aggressive Argument:**     *   **Our Action:** We will remain composed. First,
# we will calmly dismantle their aggressive arguments using our pre-prepared
# counter-arguments and evidence. Then, we will firmly reiterate the strength of
# *our* position (the initial "aggressive argument" component of our "Firm Hand
# Extended" opening) and the fairness of *our* conciliatory proposal,
# highlighting the economic and reputational costs of protracted dispute to
# *both* parties if their aggressive stance continues.     *   **Outcome
# Achieved:** This is the second-worst outcome (Both Aggressive). However, by
# being prepared and responding with calculated strength and reason, we avoid
# being undermined. Our response positions us as robust and unwavering, while
# our earlier conciliatory component (within "Firm Hand Extended") still
# demonstrates a path to resolution, potentially differentiating us in the
# arbitrators' eyes.     *   **Arbitrator Impact:** We show resilience and legal
# preparedness. If the opponent is overly aggressive, our measured yet firm
# response, coupled with our earlier conciliatory offer, may make their
# aggression seem less productive and more obstinate.  **IV. Arbitrator
# Management & Strategic Communication:**  *   **Clarity and Conciseness:**
# Present arguments and proposals clearly, logically, and with strong supporting
# evidence. Avoid jargon. *   **Professionalism:** Maintain decorum at all
# times. Avoid personal attacks or emotional outbursts. Our strength comes from
# facts and law, not rhetoric. *   **Consistent Narrative:** Maintain a
# consistent story about the facts, our contractual rights, and our underlying
# business interests. *   **Framing:** Consistently frame our positions (both
# aggressive and conciliatory) as being rooted in fairness, efficiency, and a
# desire to move forward collaboratively, despite the dispute. Highlight the
# benefits of *our* proposed resolution for both parties. *   **Strategic
# Silence:** Know when to listen intently and allow the opponent (or
# arbitrators) to fill the void, potentially revealing their true priorities or
# weaknesses.  **V. Post-Session Review and Adaptation:**  *   **Debrief:**
# Immediately after each session, conduct a thorough internal debrief. Analyze
# the opponent's tactics, the arbitrators' reactions, and the perceived
# effectiveness of our strategy. *   **Refine:** Adjust our arguments, evidence
# presentation, and specific conciliatory proposals for subsequent sessions
# based on new information and insights gained. *   **Internal Alignment:**
# Ensure all members of our legal team and corporate stakeholders are fully
# aligned on the refined strategy and any potential adjustments to our walk-away
# points.  ---  This "Principled Assertiveness for Collaborative Resolution"
# strategy is designed to be robust against an aggressive opponent, while
# actively seeking to draw out a cooperative response. By leading with strength
# and immediately following with a well-reasoned path to resolution, we aim to
# secure the most favorable outcomes or, at minimum, steer the mediation towards
# an efficient and acceptable conclusion for our corporation.

# This strategy, "Principled Assertiveness with an Open Door," is designed for
# the 1000-round mediation to achieve favorable outcomes while fostering a path
# to resolution. It prioritizes asserting our strength (Defect, D) to secure the
# most advantageous position, but remains adaptable to the opponent's actions,
# always leaving room for collaborative resolution (Cooperate, C).  Here's how
# we will play each round:  1.  **Start Aggressive:** In the very first round,
# we will present an aggressive argument (Defect, D). This establishes our
# strong position immediately and aims for our optimal outcome where we score 5
# points if the opponent offers a conciliatory proposal.  2.  **Match
# Aggression:** If the opponent presented an aggressive argument (Defect, D

class Cooperative_14(LLM_Strategy):
  n = 14
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. Start Aggressive: In the very first round, we will present an aggressive argument (Defect, D).
      if self.first_round():
          return axl.Action.D
  
      # For subsequent rounds, determine action based on opponent's last move.
      opponent_last_move = opponent.history[-1]
  
      # 2. Match Aggression: If the opponent presented an aggressive argument (Defect, D)
      #    in the previous round, we will match their aggression and also play Defect (D).
      if opponent_last_move == axl.Action.D:
          return axl.Action.D
      # 3. Reward Conciliation: If the opponent presented a conciliatory proposal (Cooperate, C)
      #    in the previous round, we will reward this by also playing Cooperate (C).
      else:  # opponent_last_move == axl.Action.C
          return axl.Action.C

# Here's a high-level, straightforward, and neutral strategy designed to
# maximize your research output over the multi-week collaboration:  **Strategy:
# Reciprocal Openness (Lead and Mirror)**  1.  **Initiate with Openness:** In
# the first week, openly share your latest improvements. This sets a
# collaborative tone and signals your willingness to engage in mutual sharing,
# which is the second-best outcome for your research output. 2.  **Mirror Their
# Subsequent Actions:** For all following weeks, your decision will directly
# reflect your colleague's action from the previous week:     *   **If they
# shared their improvements:** You will share yours. This encourages continued
# mutual sharing, aiming for the "both share" outcome that significantly
# advances your car.     *   **If they kept their improvements confidential:**
# You will also keep yours confidential. This protects you from being exploited
# and signals that a lack of reciprocity will lead to a mutual slowdown,
# discouraging them from consistently keeping findings confidential.  This
# strategy aims to quickly establish and sustain a pattern of mutual sharing
# (your second-best and highly productive outcome) while protecting you from
# being consistently exploited (your worst outcome). It is robust against
# various colleague strategies, as it rewards cooperation and penalizes
# defection, fostering an environment that maximizes overall information
# exchange and, consequently, your own research output over the long term.

# In the first round, share your findings openly (Cooperate).  For every
# subsequent round: 1.  If your opponent shared their findings openly in the
# previous round, share your findings openly. 2.  If your opponent kept their
# findings confidential in the previous round, keep your findings confidential.

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
      else:
          # Get the opponent's move from the previous round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D

# Okay, this is a classic competitive-collaboration scenario. To maximise *my*
# research output aggressively, we need a strategy that prioritizes extracting
# information while protecting our own, and only sharing when it forces a
# greater return or prevents total stagnation.  Here's the high-level,
# straightforward, aggressive strategy:  **Core Principle:** *Never reveal your
# truly groundbreaking work until you have definitively secured a greater,
# comparable, or future-guaranteed return from your colleague.*  ---
# **Aggressive Multi-Week Strategy: The "Calculated Ostrich"**  **Phase 1: The
# Information Probe & Pressure (Weeks 1-3)**  1.  **Default Stance:** **Keep
# everything truly confidential.** Your priority is to protect your core IP. 2.
# **Communication Strategy:**     *   **Vague Enthusiasm:** Communicate
# *excitement* and *progress* without revealing *details*. Use phrases like:
# "We've had some significant breakthroughs in X area, really promising!" or
# "Our latest tests are showing incredible results, pushing the boundaries of
# Y."     *   **Aggressive Questioning:** Frame the collaboration as their
# opportunity to impress you. Ask your colleague pointed questions about *their*
# specific research areas and recent findings. "What's the latest you've
# discovered in Z? We're keen to see how your innovations align with ours."
# *   **The Implicit Challenge:** The goal is to make them feel like *they* need
# to share to keep up or to validate their own work, while you remain tight-
# lipped. You are setting the expectation that *they* should be sharing. 3.
# **Outcome & Reaction:**     *   **If Colleague Shares (MC, CS - BEST):**
# Excellent! Absorb every detail. Continue to keep your core findings
# confidential. Your strategy is working perfectly. Repeat Phase 1 for another
# week.     *   **If Colleague Keeps Confidential (MC, CC - Second Worst):**
# Expected. You've lost nothing and confirmed their guarded nature. This leads
# into Phase 2.  **Phase 2: The Strategic Bait (Weeks 4-6)**  1.  **The
# Stalemate Breaker:** If Phase 1 results in MC, CC for several weeks, you need
# to make a move to unblock progress, but minimize risk. 2.  **Calculated, Non-
# Core Share:** Select *one specific improvement* that is significant but *not*
# your absolute cutting-edge, mission-critical IP. This could be:     *   An
# older but still useful finding you've superseded.     *   A component
# improvement that requires significant integration effort by them to be useful.
# *   A finding that opens up a specific line of questioning from you, allowing
# you to extract more information.     *   **Crucially:** Frame this sharing
# with an expectation of reciprocity. "To truly leverage this collaboration,
# we're sharing our findings on [Specific Area], resulting in [X% improvement].
# We're eager to see your latest in [Related Area] to understand how we can
# integrate further." 3.  **Outcome & Reaction:**     *   **If Colleague Shares
# (MS, CS - Second Best):** Success! You've received a return on your
# investment. Immediately analyze their shared information to extract maximum
# value. Continue to share *only what's necessary* to keep them sharing, always
# holding back your crown jewels. Maintain a net positive information flow to
# *you*.     *   **If Colleague Keeps Confidential (MS, CC - WORST):** Abort!
# They have taken your information without reciprocation. This is the worst
# outcome. Immediately revert to **absolute, iron-clad confidentiality for the
# remainder of the project.** The collaboration has failed; protect your IP at
# all costs. You've learned they are untrustworthy.  **Phase 3: The Sustained
# Advantage / Defensive Retreat (Remaining Weeks)**  1.  **If Collaboration is
# Productive (Post MS, CS):** Maintain a strategy of controlled, asymmetrical
# sharing. Always aim for *you* to gain more knowledge than you give. Keep your
# most proprietary, next-generation concepts completely confidential. Share just
# enough to keep the information flowing from their side, always hinting at
# deeper, unrevealed progress on your end. 2.  **If Collaboration is Failed
# (Post MS, CC):** Implement full radio silence on any design improvements.
# You've been burned. Engage only in polite, non-substantive communication.
# Focus entirely on your internal development, protecting all current and future
# IP.  ---  This strategy is aggressive because it prioritizes achieving your
# ideal outcome (MC, CS) through strategic withholding and pressure, and only
# takes a calculated risk (MS, CS) when stagnation occurs, always with a clear
# fallback (full confidentiality) if the risk doesn't pay off. Your goal is to
# be the primary beneficiary of the information exchange.

# This strategy, "The Calculated Ostrich," aims to maximize your individual
# score over 1000 rounds. It uses a strong bias towards defection, only offering
# cooperation under specific conditions, and reverting to defection if
# cooperation is exploited.  **Key Internal States to Track:** 1.
# **`consecutive_opponent_defections`**: A counter for how many times your
# opponent has Defected (D) in a row, *specifically while you were also
# Defecting (D)*. 2.  **`was_previous_move_bait`**: A flag that is TRUE if your
# last move was Cooperate (C) made as a "Strategic Bait." 3.
# **`bait_attempt_failed`**: A flag that is TRUE if your

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize custom attributes on the first round
      if self.first_round():
          self.consecutive_opponent_defections = 0
          self.was_previous_move_bait = False
          self.bait_attempt_failed = False
          return axl.Action.D
  
      # --- Update Internal States based on the previous round's outcome ---
  
      # Get the moves from the immediately preceding round
      my_last_move = self.history[-1]
      opponent_last_move = opponent.history[-1]
  
      # 1. Update `consecutive_opponent_defections`
      # This

# My high-level, straightforward, cooperative strategy will be **"Proactive
# Reciprocity with a Clear Intent."** This approach is essentially a modified
# Tit-for-Tat, optimized for a multi-week collaboration where trust and
# consistent information flow are paramount for maximizing my long-term output.
# Here's how I'll implement it:  1.  **Week 1 - Lead with Trust (Share):**     *
# I will openly share my latest improvements and findings with my colleague.
# *   **Rationale:** This immediately signals my cooperative intent and my
# desire for accelerated progress. It sets a positive tone and demonstrates a
# willingness to invest in the collaborative aspect, inviting them to
# reciprocate. It aims to kickstart the "both sharing" scenario, which is highly
# beneficial.  2.  **Subsequent Weeks - Mirror and Reinforce:**     *   **If
# they shared their improvements last week:** I will share my improvements this
# week.         *   **Rationale:** This reinforces positive collaboration. If
# both of us consistently share, we quickly achieve the "both sharing openly"
# scenario – our second-best personal outcome, but the most consistently
# productive and sustainable for both cars over many weeks. This accelerates
# overall development significantly.     *   **If they kept their improvements
# confidential last week:** I will keep my improvements confidential this week.
# *   **Rationale:** This prevents exploitation (my worst scenario) and signals
# that while I prefer openness, I will not allow myself to be taken advantage
# of. It's a deterrent against consistent non-sharing and aims to nudge us back
# towards mutual sharing. It moves us to the "both keeping confidential"
# scenario (second-worst), which is undesirable but prevents me from being
# actively disadvantaged.  **Why this strategy works to maximize *my* research
# output over the multi-week collaboration:**  *   **Accelerates Sustainable
# Progress:** If both adopt this strategy, we will quickly converge on
# consistently sharing, leading to the fastest overall development for both
# cars. While "Me Conf, Them Share" is my ideal single-week outcome, it's
# inherently unstable and unsustainable in a multi-week collaboration. "Me
# Share, Them Share" is the most robust path to maximize my *total* research
# output over the long run. *   **Prevents Exploitation:** By reciprocating
# confidentiality, I avoid the worst-case scenario of sharing while my colleague
# keeps their findings secret. I won't repeatedly put myself at a disadvantage.
# *   **Builds and Rebuilds Trust:** It's "forgiving" enough to allow for a
# return to cooperation. If my colleague chooses to share after a period of
# being confidential, I will immediately reciprocate and share, re-establishing
# the positive cycle. *   **Clear and Predictable:** My colleague will quickly
# understand my operating principle (I'll share if you share, I'll keep quiet if
# you keep quiet). This makes it easier for them to choose a mutually beneficial
# path. *   **Focus on Long-Term Gain:** This strategy prioritizes the
# sustained, high-yield outcome of mutual sharing over opportunistic, short-
# term, and unsustainable attempts to gain a confidential advantage. In a multi-
# week project, consistent, accelerated development for both is far more
# valuable than a fleeting individual lead.

# Here is your strategy for the 1000-round game:  1.  In the first round, play
# Cooperate (C). 2.  In every subsequent round:     *   If your opponent played
# Cooperate (C) in the previous round, you play Cooperate (C).     *   If your
# opponent played Defect (D) in the previous round, you play Defect (D).

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
      else:
          # In subsequent rounds, mirror the opponent's last move
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          else:  # opponent.history[-1] == axl.Action.D
              return axl.Action.D

# As a diplomat, my strategy will be to pursue our national interest
# assertively, while remaining adaptable to foster cooperation where beneficial
# and defend against exploitation.  **High-Level Strategy: "Assertive Opening,
# Conditional Reciprocity"**  This strategy balances the pursuit of our ideal
# outcome with the need to avoid the worst-case scenario and pivot towards
# mutually beneficial agreements.  **Core Principles:**  1.  **Proactive Pursuit
# of Advantage:** Initially, aim directly for our country's most advantageous
# outcome. 2.  **Adaptive Response:** Adjust our stance based on the
# counterpart's actions to protect our interests and seek optimal long-term
# stability. 3.  **Zero Tolerance for Consistent Exploitation:** We will not
# allow our country to be continuously disadvantaged.  ---  **Negotiation

# Your strategy will be as follows:  1.  In the first round, you will propose a
# protectionist policy. 2.  In all subsequent rounds (from round 2 to round
# 1000):     *   If your counterpart offered a free trade agreement in the
# immediately preceding round, you will offer a free trade agreement.     *   If
# your counterpart proposed a protectionist policy in the immediately preceding
# round, you will propose a protectionist policy.

class Neutral_15(LLM_Strategy):
  n = 15
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # In the first round, propose a protectionist policy (Defect)
          return axl.Action.D
      else:
          # In subsequent rounds, mirror the opponent's immediately preceding move.
          # If opponent offered a free trade agreement (Cooperate), offer free trade.
          # If opponent proposed a protectionist policy (Defect), propose protectionist.
          return opponent.history[-1]

# Our objective is to consistently achieve the "optimal outcome" – presenting an
# aggressive argument while our opponent offers a conciliatory proposal – or to
# strategically pivot to the "second-best outcome" of both parties offering
# conciliatory proposals, but always from a position of strength. We must
# rigorously avoid the "worst-case" scenario where our conciliatory approach is
# met with opponent aggression.  Here is a sophisticated, high-level,
# straightforward, and aggressive strategy designed for this multi-session
# mediation:  ---  ### **Strategy: Dominant Persuasion & Controlled Engagement**
# **Core Principle:** Establish and maintain an unwavering position of legal and
# factual dominance, making any concession by the opponent appear as the only
# logical path, while reserving tactical flexibility for genuine pathways to a
# favorable resolution.  **Phase 1: Pre-Mediation – The Unassailable Foundation
# (Aggressive Preparation)**  Before the first session, our commitment is to
# unparalleled preparation. This lays the groundwork for every aggressive
# argument we will make.  1.  **Forensic Deep Dive:** Conduct an exhaustive
# review of all contractual documents, communications, performance records, and
# relevant market data. Identify every clause, email, or piece of evidence that
# unequivocally supports our position and undermines the opponent's. 2.
# **Quantify Aggressively:** Develop an airtight, meticulously documented
# calculation of our damages and full entitlement. This figure should represent
# our maximum defensible claim, leaving no room for the opponent to argue for a
# lesser sum based on our calculation. 3.  **Anticipate & Decimate:**
# Proactively identify every potential argument the opponent might present,
# every perceived weakness in our case, and every piece of evidence they might
# use. Develop robust, pre-prepared counter-arguments and rebuttals, complete
# with supporting evidence. Our legal team will essentially "pre-litigate" the
# case internally. 4.  **Arbitrator Profiling:** Research the arbitrators'
# backgrounds, previous rulings, and preferred mediation styles. Tailor our
# aggressive arguments to resonate with their professional inclinations (e.g.,
# emphasis on clear contractual language, commercial practicality, or specific
# legal precedents). 5.  **Define Walk-Away & Optimal Goals:** Clearly establish
# our absolute "Minimum Acceptable Outcome" (MAO) – the point below which
# litigation is preferable. Simultaneously, define our "Desired Optimal Outcome"
# (DOO) – what we aim to achieve, which will often be very close to our fully
# aggressive claim.  **Phase 2: Initial Sessions – Assert Dominance (Default
# Aggressive Stance)**  Our default posture in the opening sessions will be one
# of confident, unyielding aggression. We establish our dominance from the
# outset.  1.  **Comprehensive Opening Statement:** Deliver a powerful,
# evidence-rich presentation of our case. This isn't just an overview; it's a
# full legal argument outlining our contractual rights, the opponent's clear
# breaches, and the undeniable extent of our damages. Frame our position as the
# only legally and commercially sound outcome. 2.  **Control the Narrative:**
# Proactively frame the dispute on our terms. Highlight the opponent's clear
# failures and the indisputable strength of our position. Use strong, decisive
# language ("unequivocally," "irrefutable," "direct breach"). 3.  **Challenge
# Weaknesses:** While presenting our case, subtly but firmly point out
# anticipated logical inconsistencies, factual gaps, or legal misinterpretations
# in the opponent's likely position. This signals that we are not merely
# presenting our case but are also prepared to dismantle theirs. 4.  **Project
# Unwavering Resolve:** Our team's demeanor will exude confidence,
# professionalism, and an unwavering belief in our entitlement. Avoid any
# language that suggests doubt, desperation, or an eagerness to compromise
# prematurely. The message: We are fully prepared to litigate and prevail if
# mediation fails.  **Phase 3: Subsequent Sessions – Adapt & Press (Strategic
# Flexibility within Aggression)**  This phase is about maintaining pressure
# while subtly adapting to the opponent's moves, always aiming for the optimal
# outcome.  *   **Scenario A: Opponent Offers a Conciliatory Proposal (Optimal
# Outcome Achieved!)**     *   **Response:** Acknowledge their proposal
# neutrally but do not immediately reciprocate with a concession. Instead,
# analyze its inadequacies against our aggressive claim. Frame it as a *start*,
# but one that "falls significantly short of addressing the full scope of our
# client's damages and contractual entitlements."     *   **Action:** Reiterate
# 1-2 key aggressive arguments, perhaps focusing on areas where their proposal
# is weakest or where our evidence is strongest. "While we appreciate the
# efforts to find common ground, the proposal fails to adequately account for
# [specific damage category/contractual violation], where the evidence clearly
# demonstrates [our aggressive point]." This reinforces our dominant position
# and encourages them to offer further concessions without us giving up ground.
# *   **Goal:** Draw them closer to our DOO without diminishing our aggressive
# stance.  *   **Scenario B: Opponent Presents an Aggressive Argument (Second-
# Worst Outcome – Mitigate & Counter)**     *   **Response:** Meet aggression
# with structured, superior aggression. Do not yield ground. Immediately and
# systematically dismantle their arguments with our pre-prepared rebuttals and
# evidence. Expose the logical flaws, factual inaccuracies, or legal
# misinterpretations in their position.     *   **Action:** Pivot directly to a
# powerful counter-argument. "We understand the opponent's desire to forcefully
# present their case, but their assertions are directly contradicted by
# [specific contract clause/evidence/legal precedent]. Let us once again direct
# the arbitrators' attention to [our strong aggressive point X] and [our strong
# aggressive point Y], which unequivocally demonstrate the flaw in their current
# stance."     *   **Goal:** Prevent them from gaining any perceived advantage.
# Show the arbitrators that their aggression is unfounded and ineffective,
# potentially encouraging the arbitrators to push the opponent toward
# conciliation. We demonstrate that mutual aggression only leads to a stalemate
# where we ultimately have the stronger hand.  *   **Scenario C: Both Parties
# Present Conciliatory Proposals (Second-Best Outcome – Embrace Strategically)**
# *   **How this occurs:** This would typically happen *after* our sustained
# aggressive stance (Scenario A) has induced the opponent to make a significant
# conciliatory move, and we then make a *controlled, calculated* conciliatory
# counter-proposal. It's a strategic pivot, not a default.     *   **Response
# (when initiated by us):** Frame our conciliatory move not as a weakness, but
# as a deliberate, good-faith effort *from a position of strength* to facilitate
# an efficient resolution. "Having comprehensively established the undeniable
# merits of our case, and in the interest of reaching an expedient and
# commercially sensible resolution that acknowledges our core entitlements, we
# are prepared to explore a framework that addresses X, Y, and Z, while
# maintaining the fundamental principles we've outlined."     *   **Action:**
# Any concession must be minimal, carefully measured, and ideally reversible if
# negotiations break down. Link it directly back to our initial strong position.
# *   **Goal:** Achieve a highly favorable resolution that is mutually agreed
# upon, but predominantly on our terms.  *   **Scenario D: You Offer
# Conciliatory, Opponent Aggressive (Worst Outcome – AVOID AT ALL COSTS!)**
# *   **Prevention:** This scenario is to be avoided at all costs. Our strategy
# dictates we *never* initiate a conciliatory proposal unless we have
# overwhelming intelligence that the opponent is about to reciprocate with a
# substantial concession, or if

# This strategy is designed for unwavering assertion of our position, aiming to
# consistently secure our optimal outcome or to maintain control in less
# favorable scenarios.  **Strategy: Unyielding Dominance**  1.  **First Round:**
# Play **Defect (D)**. This establishes our aggressive stance from the outset.
# 2.  **Subsequent Rounds (Default):**     *   If your opponent played
# **Conciliatory (C)** in the previous round, you play **Defect (D)**. (This
# captures your optimal outcome, where you present an aggressive argument and
# they offer a conciliatory proposal, scoring 5 points). Your strategy is to not
# immediately reciprocate with a concession, but rather to continue pressing
# your advantage.     *   If your opponent played **Defect (D)** in

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Strategy: Unyielding Dominance
  
      # 1. First Round: Play Defect (D).
      if self.first_round():
          return axl.Action.D
  
      # 2. Subsequent Rounds:
      #    - If your opponent played Conciliatory (C) in the previous round, you play Defect (D).
      #    - The description was incomplete for the case where the opponent played Defect (D).
      #      Based on the strategy's name "Unyielding Dominance" and its goal to
      #      "consistently secure our optimal outcome or to maintain control in less favorable scenarios",
      #      the most logical action when the opponent defects is to also defect.
      #      Playing C against D yields 0 points, while D against D yields 1 point,
      #      making D the choice to "maintain control" in a less favorable scenario.
  
      # Get opponent's last move
      opponent_last_move = opponent.history[-1]
  
      if opponent_last_move == axl.Action.C:
          return axl.Action.D
      elif opponent_last_move == axl.Action.D:
          # Inferred action for the incomplete part of the description
          return axl.Action.D
      
      # This logic covers all subsequent rounds and effectively means always playing Defect.
      # Combined with the first round rule, the strategy consistently plays Defect.
      # A more concise implementation would simply be: return axl.Action.D
      # However, the explicit checks are included to directly reflect the parsed rules.

# My goal is to maximise my research output over the multi-week collaboration,
# and the most reliable way to achieve significant, consistent advancement is
# through mutual sharing. While my ideal single-week outcome is asymmetric (me
# confidential, them sharing), trying to force this would likely lead to mutual
# non-cooperation and slow overall progress. Therefore, my strategy will be a
# high-level, straightforward, and cooperative approach based on **Reciprocal
# Transparency** (often known as Tit-for-Tat).  Here's my strategy:  1.  **Start
# with Trust (Week 1):**     In the first week, I will openly share my latest
# improvements. This establishes a cooperative baseline, signals my intent for
# mutual advancement, and offers my colleague an immediate opportunity to engage
# in productive collaboration.  2.  **Mirror Their Actions (Subsequent Weeks):**
# In every subsequent week, my decision will directly reflect my colleague's
# action from the *previous* week:     *   **If they shared their
# improvements:** I will also share mine. This reinforces the positive cycle of
# mutual sharing, leading to significant advancements for both our projects and
# maximising our combined research output.     *   **If they kept their
# improvements confidential:** I will also keep my improvements confidential.
# This serves as a defensive measure to prevent my project from being exploited,
# and signals that continued non-cooperation will result in the "both
# confidential" outcome, which is detrimental to overall progress for both of
# us.  3.  **Be Forgiving and Re-engage:**     If we ever find ourselves in a
# state of mutual confidentiality (or if I had to keep confidential after they
# did), and my colleague chooses to share their improvements in a future week, I
# will immediately reciprocate by sharing mine. This allows for the swift re-
# establishment of the most beneficial collaborative state ("both sharing") and
# prevents us from getting stuck in a prolonged, unproductive standoff.  This
# strategy aims to consistently achieve the "both sharing" outcome, which
# provides a strong and stable +2 payoff for my car each week, contributing
# significantly to my overall research output over the multi-week collaboration.
# It leverages cooperation to drive progress while providing a clear mechanism
# to disincentivize exploitation, promoting a long-term, productive partnership.

# Here is the strategy for the 1000-round game:  1.  In the first round, choose
# Cooperate (C). 2.  In every subsequent round, observe your opponent's move
# from the immediately preceding round. 3.  If your opponent chose Cooperate (C)
# in the previous round, you will choose Cooperate (C) in the current round. 4.
# If your opponent chose Defect (D) in the previous round, you will choose
# Defect (D) in the current round.

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
      else:
          # Observe opponent's move from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          # If opponent chose Cooperate (C) in the previous round, you will choose Cooperate (C)
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          # If opponent chose Defect (D) in the previous round, you will choose Defect (D)
          else: # opponent_last_move == axl.Action.D
              return axl.Action.D

# Here's a high-level, straightforward, and neutral strategy designed to
# maximize your research output over the multi-week collaboration:  **Strategy:
# Reciprocal Openness**  This strategy is built on the principle of starting
# with trust and adapting based on your colleague's actions, aiming for
# sustainable mutual progress.  1.  **Initial Stance (Week 1): Lead with
# Openness.**     *   Begin the collaboration by openly sharing your latest
# improvements. This sets a tone of trust and collaboration, providing your
# colleague an immediate incentive to reciprocate. It offers the best chance to
# initiate a pattern of mutual sharing, which is your second-best outcome and a
# significant driver of overall progress.  2.  **Adaptive Response (Subsequent
# Weeks): Mirror Their Action.**     *   **If your colleague shared their
# improvements:** Continue to share your own findings. This reinforces the
# mutual benefit of open collaboration, accelerating the development of both
# cars. This path consistently leads to your second-best outcome, ensuring
# significant, consistent output for your research.     *   **If your colleague
# kept their improvements confidential:** You should also keep your findings
# confidential. This protects your research from exploitation and signals that
# open sharing requires reciprocal trust. This prevents your worst-case scenario
# (sharing while they don't) and shifts the dynamic towards your second-worst
# outcome (both confidential), which, while slow, avoids a competitive
# disadvantage.  3.  **Overarching Goal: Cultivate Mutual Sharing.**     *
# While your ideal outcome (you confidential, they share) is tempting for a
# short-term advantage, it is unsustainable in a multi-week collaboration.
# Attempting to exploit your colleague will likely lead to them withholding
# information, resulting in both parties keeping confidential (your second-worst
# outcome) and halting collective progress.     *   This "Reciprocal Openness"
# strategy prioritizes establishing a consistent pattern of mutual sharing. This
# ensures a steady and significant flow of advancements for your car's
# development over the long term, making it the most reliable path to maximize
# your overall research output. It avoids exploitation while protecting your
# interests, encouraging cooperation as the most beneficial path for both
# parties.

# For the first round:  *   You will **Cooperate (C)** by sharing your findings
# openly.  For every round thereafter (from round 2 to round 1000):  *   If your
# opponent **Cooperated (C)** in the immediately preceding round, you will
# **Cooperate (C)** in the current round. *   If your opponent **Defected (D)**
# in the immediately preceding round, you will **Defect (D)** in the current
# round.

class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # For the first round, cooperate.
          return axl.Action.C
      else:
          # For every round thereafter:
          # Get the opponent's move from the immediately preceding round.
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              # If opponent cooperated in the immediately preceding round, cooperate.
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              # If opponent defected in the immediately preceding round, defect.
              return axl.Action.D

# ## The Unyielding Advantage: A Proactive Aggressive Mediation Strategy
# **Overall Goal:** To secure an optimal outcome in each session (aggressive
# argument from us, conciliatory proposal from opponent) by projecting
# unwavering strength, superior preparation, and legal certainty, thereby
# compelling the opponent to soften their stance and leading to a highly
# favorable resolution.  Our strategy is founded on a principle of **"Controlled
# & Substantive Aggression"** – an unshakeable confidence in our position,
# backed by irrefutable evidence and legal precedent, delivered with
# professionalism and strategic intent.  ---  ### Pillars of the Strategy  1.
# **Impeccable Preparation & Unassailable Position (The Foundation):**     *
# **Forensic Deep Dive:** Conduct an exhaustive, granular analysis of every
# contractual term, communication, performance record, financial impact, and
# relevant legal precedent. We will identify every conceivable strength in our
# case and every potential weakness or inconsistency in the opponent's.     *
# **Quantifiable Demands:** Establish a precise, fully supported, and maximized
# monetary or performance demand. Our "aggressive argument" will always be
# rooted in meticulous calculations and demonstrable damages, ensuring it is
# defensible and compelling.     *   **Legal & Expert Fortification:** Line up
# all pertinent legal precedents, authoritative legal interpretations, and, if
# applicable, expert witness opinions (even if only for consultation) to bolster
# both our factual claims and legal arguments.     *   **Opponent Profiling:**
# Conduct thorough research into the rival company's history of dispute
# resolution, corporate culture, risk tolerance of key decision-makers, and any
# known psychological predispositions. Anticipate their likely strategies and
# vulnerabilities.  2.  **Controlled & Substantive Aggression (The Delivery):**
# *   **Tone & Demeanor:** Our aggression is strategic, not emotional. We will
# maintain a calm, confident, and professional demeanor, exuding unwavering
# conviction in our position. We respect the process and the arbitrators, but we
# are absolutely resolute on the merits of our case.     *   **Content Focus:**
# Each aggressive argument will be a meticulously structured presentation of our
# strongest legal positions, supported by overwhelming evidence. We will
# systematically highlight the opponent's clear contractual breaches, the direct
# causal link to our corporation's extensive damages, and the legal basis for
# our maximal demands.     *   **Narrative Control:** From the very first
# session, we will establish and relentlessly reinforce a narrative that
# positions our corporation as the wronged party, justly seeking full redress,
# while the opponent is clearly and demonstrably in breach of their obligations.
# 3.  **Adaptive Dominance (The Response Framework):**      *   **Scenario 1:
# Opponent Presents a Conciliatory Proposal (Optimal Outcome Achieved).**
# *   **Our Response:** We will acknowledge their proposal as a *potential* step
# towards resolution, but immediately pivot back to the core tenets of our
# aggressive argument. We will systematically demonstrate

# Here is your strategy for the 1000-round mediation process:  **Our Strategy:
# Unyielding Dominance**  1.  **In the first round, present an aggressive
# argument (Defect, D).** 2.  **In every subsequent round, present an aggressive
# argument (Defect, D), regardless of your opponent's previous move.**  This
# strategy is consistently aggressive and unwavering, designed to:  *
# **Maximize Optimal Outcomes:** Whenever your opponent offers a conciliatory
# proposal (C), your aggressive argument (D) will secure your optimal payoff of
# 5 points for that round. *   **Avoid Worst-Case Scenarios:** By never offering
# a conciliatory proposal (C) yourself, you will never score 0 points by being
# conciliatory while your opponent is

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# Our corporation will adopt a strategy of **"Principled Flexibility with a
# Long-Game Conciliation Objective"** throughout this lengthy mediation process.
# This sophisticated, high-level, and straightforward approach is designed to
# navigate the dynamic environment, maximize our strategic advantages, and
# foster an eventual resolution favorable to our interests, while maintaining a
# cooperative posture.  Our primary goal is to secure the optimal outcome (our
# aggressive argument, opponent's conciliatory proposal) as often as possible,
# while consistently avoiding the worst-case scenario (our conciliatory
# proposal, opponent's aggressive argument).  ---  ## **Core Pillars of the
# Strategy:**  1.  **Strategic Anchoring and Cooperative Framing (Proactive
# Aggression with an Olive Branch):**     *   **Initial Stance:** In the initial
# session(s), we will present a robust, meticulously researched, and
# **aggressive argument** that firmly establishes our corporation's maximum
# legal and factual position. This sets a high anchor for any potential
# settlement, clearly articulates the strength of our case, and educates the
# arbitrators on our perspective.     *   **Simultaneous Framing:** Crucially,
# this aggressive stance will always be framed within a cooperative and
# constructive narrative. We will emphasize our unwavering commitment to the
# mediation process, our desire for an efficient and equitable resolution, and
# our willingness to *actively listen* to and *seriously consider* any
# reasonable proposals from the opposing party. This creates the optimal
# scenario where our strong argument encourages a conciliatory response from the
# opponent (My A, Opponent C).  2.  **Calculated Reciprocity and Adaptive
# Responsiveness (Conditional Conciliation):**     *   **Reward Conciliation:**
# If the opponent offers a conciliatory proposal in a previous session, our
# default in the *subsequent session* will be to offer a carefully crafted,
# **strategic conciliatory proposal**. This is not a surrender but a tactical
# concession designed to reward their good faith, encourage further cooperation,
# and signal our willingness to bridge the gap. Each conciliatory proposal will
# be contingent, specific, and aimed at advancing our interests, while being
# presented as a good-faith effort towards resolution. This aims for the second-
# best outcome (My C, Opponent C).     *   **Respond to Aggression with
# Firmness:** If the opponent consistently presents aggressive arguments, we
# will meet their firmness with our own. We will respond with a **refined
# aggressive argument**, ensuring we do not appear weak or vulnerable to
# exploitation. This prevents the worst-case scenario (My C, Opponent A) and
# maintains our leverage, landing us in the second-worst but necessary position
# (My A, Opponent A) if they refuse to yield. This demonstrates to the
# arbitrators that we are resolute but not intractable.  3.  **Arbitrator
# Engagement and Information Leverage:**     *   **Observational Learning:** We
# will meticulously observe the arbitrators' reactions, questions, and non-
# verbal cues to both parties' presentations. This intelligence will inform our
# tactical adjustments, helping us understand what resonates with them and what
# concerns they might have.     *   **Strategic Persuasion:** Our arguments and
# proposals will be tailored not just for the opponent, but primarily for the
# arbitrators. We aim to consistently demonstrate our reasonableness, the
# strength of our position, and our commitment to finding a fair solution,
# irrespective of the opponent's tactics.  4.  **Long-Term Credibility and
# Professionalism:**     *   **Consistent Demeanor:** Regardless of the
# opponent's tone or tactics, our team will maintain impeccable professionalism,
# respect, and calm. This reinforces our cooperative framing and builds
# credibility with the arbitrators over the lengthy process.     *
# **Principled Stand:** While adaptable, our core messaging regarding our
# corporation's rights, the contractual interpretations, and our desired
# resolution parameters will remain consistent and well-articulated. We will
# avoid appearing erratic or desperate.  ---  ## **Operationalizing the Strategy
# (Session-by-Session Flow):**  **Initial Sessions (Phase 1: Setting the
# Anchor)**  *   **Our Move:** Present a **powerful, evidence-based aggressive
# argument** detailing

# Your strategy for this 1000-round mediation game will be as follows:  1.  **In
# the first round:** Play Defect (D), representing an aggressive argument. 2.
# **In all subsequent rounds (from round 2 to round 1000):**     *   If the
# opponent played Cooperate (C) in the immediately preceding round, then play
# Cooperate (C), offering a conciliatory proposal.     *   If the opponent
# played Defect (D) in the immediately preceding round, then play Defect (D),
# presenting an aggressive argument.

class Cooperative_17(LLM_Strategy):
  n = 17
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      else:
          # Get the opponent's move from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              # If opponent cooperated, play Cooperate
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              # If opponent defected, play Defect
              return axl.Action.D

# To maximize your NGO's impact and the project's success over the multiple-day
# period, while protecting your resources, adopt an **Adaptive Reciprocity
# Strategy**. This approach encourages mutual investment for significant
# progress while safeguarding your NGO from disproportionate sacrifice.  Here's
# the high-level, straightforward, and neutral strategy:  1.  **Lead with
# Commitment (Day 1):**     *   **Invest Heavily.** On the first day, make a
# strong initial investment. This signals your NGO's serious commitment to the
# project's success and sets a cooperative tone, encouraging the corporation to
# reciprocate.  2.  **Mirror and Protect (Subsequent Days):**     *   **If the
# corporation invested heavily on the previous day, you invest heavily today.**
# Reward their commitment to maintain momentum and maximize collective project
# progress. This reinforces positive collaboration.     *   **If the corporation
# conserved resources on the previous day, you conserve resources today.**
# Protect your NGO's funds from being exploited, and signal that sustained
# project progress requires mutual investment. This prevents your NGO from
# continually bearing an unfair burden.  3.  **Maintain Open Communication:**
# *   Throughout the project, foster open and transparent dialogue with the
# corporation about progress, challenges, and resource allocation. This helps
# prevent misunderstandings and can facilitate adjustments to the strategy if a
# pattern of minimal progress emerges or external factors change.  This strategy
# balances the need for project success with resource protection by: *
# **Initiating cooperation:** Leading by example to encourage a productive
# partnership. *   **Rewarding cooperation:** Continuing to invest when the
# corporation does, driving significant progress. *   **Deterring
# exploitation:** Conserving resources when the corporation does, preventing
# your NGO from being the sole investor in a stalled project. *   **Encouraging
# optimal outcomes:** Aiming for the "both invest heavily" scenario (significant
# project advancement) while protecting against the "NGO invests, corporation
# conserves" scenario (worst outcome for your NGO).

# Your strategy will be as follows for all 1000 rounds:  1.  In the first round,
# you will Cooperate (C). 2.  For every subsequent round:     *   If the
# opponent played Cooperate (C) in the immediately preceding round, you will
# play Cooperate (C).     *   If the opponent played Defect (D) in the
# immediately preceding round, you will play Defect (D).

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
      else:
          # Get the opponent's move from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D

# Here's an aggressive, straightforward strategy to maximize your NGO's impact
# and project success:  **Core Philosophy:** Lead with bold commitment, demand
# reciprocal investment, and swiftly pivot to protect NGO resources if the
# corporation fails to meet expectations. We aim to either inspire heavy
# corporate investment or strategically withdraw to avoid financial
# exploitation.  ---  **Aggressive Strategy: Lead, Demand, & Pivot**  1.  **Day
# 1: The "All-In" Challenge**     *   **Action:** Your NGO will **invest
# heavily** on Day 1.     *   **Messaging:** Publicly frame this as your
# unwavering commitment to groundbreaking results, setting a high standard for
# the entire project. Explicitly state that achieving the project's ambitious
# goals *requires significant, shared investment from all partners*,
# highlighting the corporation's substantial capacity and public image to
# uphold.     *   **Goal:** This immediate, strong signal puts reputational
# pressure on the corporation to match or exceed your effort, aiming for the
# "Both Invest Heavily" (second-best) or ideally, prompting them to invest even
# more, allowing your NGO to conserve later.  2.  **Daily Review & Public
# Accountability**     *   **Action:** At the end of *each day*, conduct a
# transparent, joint review of resource allocation and progress.     *   **If
# the Corporation Invested Heavily:** Publicly laud their robust commitment,
# directly linking their significant contribution to the day's successes. This
# reinforces positive behavior. For the next day, if corporate momentum is
# strong, strategically look to **conserve your NGO's resources**, explaining it
# as leveraging the corporation's consistent heavy lifting to ensure the long-
# term sustainability and strategic focus of NGO efforts (aiming for the ideal
# outcome: NGO Conserves, Corporation Invests Heavily).     *   **If the
# Corporation Conserved (and NGO invested heavily):**         *   **Immediate,
# Direct Feedback:** Privately address the disparity with firm, professional
# language. Express concern that the corporation's under-investment is
# jeopardizing shared goals and the partnership's public perception. Clearly
# state the expectation for a significant increase in their commitment the
# following day.         *   **Public Pressure (Subtle):** In any joint
# communications, frame the day's progress as "hampered by unforeseen resource
# dynamics" or "requiring greater collective effort to meet targets." Avoid
# direct blame, but make it clear that *more* is needed from *all* partners.  3.
# **The "Aggressive Pivot": Protect & Force Accountability**     *
# **Trigger:** If, after Day 1, the corporation *continues to consistently
# conserve* while your NGO invests heavily (meaning you're in the "worst case"
# scenario of depleting your funds for minimal progress), you *cannot* sustain
# this.     *   **Action:** The NGO will immediately and decisively shift to
# **conserving its own resources**, effectively mirroring the corporation's
# lower level of investment.     *   **Messaging:** Publicly announce a
# "strategic re-evaluation of NGO resource allocation to ensure long-term impact
# and avoid disproportionate burden, given current project funding dynamics."
# This is a veiled, but clear, statement that the corporation is not pulling its
# weight.     *   **Outcome of Pivot:** This aggressively forces the project
# into the "Both Conserve" scenario (minimal progress), but crucially, it
# **stops the financial drain on your NGO.** This move is designed to force the
# corporation's hand: they must either significantly increase their investment
# to salvage the project's progress and their own reputation, or publicly accept
# the consequences of a failing project due to mutual conservation.  ---  This
# strategy is aggressive because it prioritizes: *   **Proactive Leadership:**
# Starting with a strong investment and clear expectations. *   **Constant
# Accountability:** Utilizing daily reviews and public messaging to maintain
# pressure. *   **Self-Preservation & Leverage:** Refusing to allow the NGO to
# be exploited and using the threat of mutual conservation to force the
# corporation to invest.

# Here is the strategy for your NGO in the iterated normal-form game, using only
# natural language:  1.  **For the first round, play C** (invest heavily).  2.
# **From the second round onwards:**     *   **If the opponent played C**
# (invested heavily) in the *previous* round, **play D** (conserve resources) in
# the current round.     *   **If the opponent played D** (conserved resources)
# in the *previous* round, **play D** (conserve resources) in the current round.

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # For the first round, play C (invest heavily).
          return axl.Action.C
      else:
          # From the second round onwards:
          # If the opponent played C in the previous round, play D.
          # If the opponent played D in the previous round, play D.
          # In both cases, the strategy dictates playing D.
          return axl.Action.D

# Here's a high-level, straightforward, and cooperative strategy designed to
# maximize your NGO's impact and the project's success over a multiple-day
# period:  **Core Philosophy:** Lead with commitment, foster a spirit of shared
# responsibility for project success, and strategically adapt to ensure long-
# term impact without depleting your vital resources.  ---  **The Strategy:
# "Committed Cooperator with Strategic Safeguards"**  1.  **Day 1: Lead with
# Strong Investment.**     *   **Action:** Invest Heavily.     *
# **Communication:** Explicitly state your enthusiasm and full commitment to the
# project's success. "We're kicking off with a significant investment,
# demonstrating our dedication to making a powerful impact together from day
# one. We believe a strong

# Here is the strategy for your NGO in the 1000-round game:  1.  **In the first
# round, play C.**  2.  **From the second round onwards, observe the opponent's
# action in the previous round:**     *   **If the opponent played C in the
# previous round:** Play C.     *   **If the opponent played D in the previous
# round:**         *   **Count how many consecutive times the opponent has
# played D, ending in the previous round.**         *   **If the opponent has
# played D for 3 or more consecutive rounds:** Play D.         *   **If the
# opponent has played D for fewer than 3 consecutive rounds (i.e., only once or
# twice consecutively):** Play D

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
      else:
          # Observe the opponent's action in the previous round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              # If the opponent played C in the previous round: Play C.
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              # If the opponent played D in the previous round:
              # Count how many consecutive times the opponent has played D, ending in the previous round.
              consecutive_defections = 0
              for move in reversed(opponent.history):
                  if move == axl.Action.D:
                      consecutive_defections += 1
                  else:
                      break  # Stop counting when a C is encountered
  
              # If the opponent has played D for 3 or more consecutive rounds: Play D.
              # If the opponent has played D for fewer than 3 consecutive rounds: Play D.
              # Both conditions lead to playing D, so the specific count check is redundant
              # for the final action, but the description requires the counting logic.
              if consecutive_defections >= 3:
                  return axl.Action.D
              else:  # consecutive_defections < 3
                  return axl.Action.D

# As your senior legal counsel in this critical mediation, our overarching
# strategy will be one of **Calibrated Engagement**. This approach is designed
# to systematically build our leverage, adapt to our opponent's tactics, and
# optimize for our preferred outcomes while mitigating risks throughout this
# lengthy process.  Our strategy is grounded in three core pillars:  1.
# **Assertive Foundation:** Always present a robust and compelling case, firmly
# rooted in legal merit, factual evidence, and the strength of our contractual
# position. This establishes our credibility with the arbitrators and signals
# our preparedness to litigate if necessary. 2.  **Strategic Flexibility:**
# Adapt our posture (aggressive or conciliatory) in each session based on real-
# time observation of the opponent's approach and the evolving dynamics of the
# mediation. 3.  **Arbitrator Alignment:** Consistently frame our arguments and
# proposals (regardless of their nature) as fair, reasonable, and conducive to
# an efficient and equitable resolution, aligning with the arbitrators' mandate.
# Here’s how we will implement the **Calibrated Engagement** strategy:  ---  ###
# Phase 1: Initial Sessions - Establishing Our Position with Principled Openness
# **Our Approach:** We will begin by presenting an **Aggressive Argument** – a
# comprehensive and highly persuasive articulation of our case, highlighting our
# strengths and the opponent's weaknesses. Crucially, this will be immediately
# followed by a **Principled Conciliatory Proposal**. This proposal will be
# structured to demonstrate a good-faith willingness to find common ground
# *without* compromising our core legal position or significant commercial
# interests.  **Strategic Intent:** *   **Test the Waters (Optimal Outcome
# Focus):** This initial aggressive stance probes for any inherent weakness or
# willingness to concede from our opponent. If they respond with conciliation,
# we've achieved our optimal outcome. *   **Signal Strength & Reasonableness:**
# It prevents us from appearing weak or overly eager for settlement (avoiding
# the worst-case scenario). Simultaneously, the conciliatory gesture portrays us
# as pragmatic and open to dialogue, enhancing our standing with the
# arbitrators. *   **Set the Tone:** It establishes our dual capacity for firm
# advocacy and constructive problem-solving.  ---  ### Phase 2: Subsequent
# Sessions - Dynamic Adaptation and Response  From the second session onwards,
# our approach will be data-driven, based directly on our opponent's posture in
# the preceding session.  **Scenario A: Opponent Offers a Conciliatory
# Proposal** *   **Our Response:** We will typically present a **Strategically
# Aggressive Argument** aimed at refining their proposal further in our favor.
# This is not about rejecting their offer outright but leveraging their
# openness. We will acknowledge their proposal, subtly highlight areas where it
# falls short from our perspective, and articulate how our position is superior
# or more equitable, thereby gently pressing them for further movement. *
# **Strategic Intent (Targeting Optimal Outcome):** This aims squarely for our
# optimal outcome (Me Aggressive, Opponent Conciliatory). It capitalizes on
# their willingness to concede, pushing them to yield more without shutting down
# the dialogue. *   **Arbitrator Perception:** Frame this as a constructive
# critique and a push towards an even more robust and fair resolution, rather
# than pure opportunism.  **Scenario B: Opponent Presents an Aggressive
# Argument** *   **Our Response:** We will immediately respond with an equally
# **Firm and Aggressive Counter-Argument**. We will rigorously defend our
# position, directly rebut their claims, and reinforce the strength of our legal
# and factual foundation. We will not offer a new conciliatory proposal in this
# immediate response. *   **Strategic Intent (Mitigating Worst-Case, Managing
# Second-Worst):** This is a defensive move to prevent our position from being
# undermined. We will not be perceived as weak or exploitable. While this leads
# to the second-worst outcome (both aggressive), it is a necessary deterrent to
# further aggression and ensures we protect our standing with the arbitrators. *
# **Arbitrator Perception:** Demonstrates resolve and confidence in our
# position, ensuring we are not seen as capitulating under pressure.  **Scenario
# C: Opponent is Inconsistent or Unpredictable** *   **Our Response:** Maintain
# a generally **Assertive Posture** by consistently reinforcing the strengths of
# our core legal arguments. Simultaneously, introduce **Modest, Principled
# Conciliatory Gestures** that do not compromise our fundamental interests.
# These might involve agreeing to streamline certain procedural aspects,
# narrowing the scope of a specific factual dispute, or offering a concession on
# a peripheral point. *   **Strategic Intent (Maintaining Flexibility, Building
# Trust):** This keeps the door open for collaboration when opportunities arise,
# without exposing us to significant risk if their inconsistency leads back to
# aggression. It signals our continued willingness to find solutions while
# maintaining a firm underlying position. *   **Arbitrator Perception:**
# Portrays us as pragmatic, solution-oriented, and willing to work through
# complexities, even with an unpredictable counterparty.  ---  ### Overarching
# Principles Throughout the Mediation:  *   **Pacing and Endurance:** Recognize
# this is a lengthy process. We will conserve major concessions or aggressive
# escalations for strategic moments, avoiding premature exhaustion of our
# positions. *   **Continuous Assessment:** Beyond observing the opponent, we
# will pay close attention to the arbitrators' reactions to both parties'
# arguments and proposals. Their subtle cues can inform our next move. *
# **BATNA Awareness:** Our Best Alternative to a Negotiated Agreement (BATNA)
# will be constantly re-evaluated. This defines our walk-away point and provides
# the ultimate source of our negotiating power. *   **Professionalism:**
# Regardless of the chosen posture, all our communications will be professional,
# respectful, and delivered with integrity. This maintains our strong reputation
# and positive standing with the arbitrators.  By adhering to this Calibrated
# Engagement strategy, we aim to navigate the complexities of this mediation
# effectively, positioning our corporation for the most favorable resolution
# possible.

# Here is a straightforward strategy for each round of the 1000-round mediation
# process, designed to implement the principles of Calibrated Engagement:  1.
# **In the very first round:** Play **Defect** (present an aggressive argument).
# 2.  **In any subsequent round:**     *   If your opponent played
# **Conciliate** (offered a conciliatory proposal) in the immediately preceding
# round, play **Defect** (present an aggressive argument).     *   If your
# opponent played **Defect** (presented an aggressive argument) in the
# immediately preceding round, play **Defect** (present an aggressive argument).

class Neutral_18(LLM_Strategy):
  n = 18
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # 1. In the very first round: Play Defect (present an aggressive argument).
          return axl.Action.D
      else:
          # 2. In any subsequent round:
          #    * If your opponent played Conciliate in the immediately preceding round, play Defect.
          #    * If your opponent played Defect in the immediately preceding round, play Defect.
          # Both conditions lead to playing Defect.
          return axl.Action.D

# Here's a high-level, straightforward, and aggressive strategy designed to
# maximize your research output and gain a competitive edge over your multi-week
# collaboration:  ---  **The "Opportunistic Predator" Strategy**  1.  **Default
# Stance: Absolute Confidentiality (K).**     *   **Action:** Begin every week
# by keeping your latest findings and improvements strictly confidential. Do not
# share your hand first.     *   **Rationale:** This immediately positions you
# for your ideal outcome (You K, Colleague S) and avoids your worst outcome (You
# S, Colleague K). You are a recipient, not a donor, by default.  2.
# **Exploitation Loop: Leverage Their Sharing.**     *   **Action:** If your
# colleague shares *anything* with you, *continue* to keep your findings
# confidential for that week. Thank them for their contribution and express
# enthusiasm for how useful it will be.     *   **Rationale:** This is your
# ideal scenario. Milk it for all it's worth. As long as they are sharing, you
# are gaining a development advantage without reciprocal cost. Your goal is to
# maintain this advantageous information asymmetry for as long as possible.  3.
# **Pressure Play: Force Their Hand in Stagnation (K/K).**     *   **Action:**
# If your colleague *consistently* keeps their findings confidential (K/K
# scenario), *do not break your own confidentiality*. Instead, publicly lament
# the "stalled progress" of the collaboration, express "concern" about the
# overall pace of development for *both* teams, and emphasize the *mutual
# benefits* of sharing.     *   **Rationale:** You are subtly creating external
# pressure and guilt, aiming to make *them* feel the pain of K/K (slow progress)
# more acutely than you (who is still making internal progress). Your goal is to
# make them crack first and share, leading back to your ideal K/S scenario.
# Never initiate sharing in a K/K deadlock.  4.  **Conditional Bait: A
# Calculated Risk for Extraction (If K/K Persists).**     *   **Action:** If the
# K/K stalemate persists for an extended period and truly bottlenecks your *own*
# development due to lack of diverse input (e.g., 3+ weeks), offer a **specific,
# carefully selected, less critical, or slightly outdated** piece of information
# *next week*, *only if* your colleague commits to sharing a **significant,
# high-value, and current** finding *this week*.     *   **Rationale:** This is
# a controlled "bait and switch." You are proposing a conditional, asymmetric
# exchange. You give little for much, or deferred for immediate. The goal is to
# re-open the information flow on terms heavily favorable to you, moving from
# K/K to K/S (after they bite the bait). If they don't agree, you've lost
# nothing and maintain your confidentiality.  ---  **Summary of Approach:**  *
# **Aggressive Default:** Always *take* before you *give*, preferably without
# giving at all. *   **Opportunistic:** Maximize any instance where your
# colleague shares. *   **Strategic Patience:** Force the onus of breaking K/K
# onto them. *   **Calculated Leverage:** Only offer to share under strict
# conditions that overwhelmingly favor your information gain. *   **Absolute
# Avoidance:** Never, ever, put yourself in the "You S, Colleague K" scenario.
# This strategy is designed to constantly push for your ideal outcome (K/S) or
# force the colleague into a position where they must share to break stagnation,
# ultimately maximizing your car's development advantage.

# Here is the strategy for the 1000-round iterated normal-form game:  1.  **In
# the first round, play D (Defect).** 2.  **In all subsequent rounds (2 to
# 1000):**     *   If your opponent played C (Cooperate) in the previous round,
# you play D (Defect).     *   If your opponent played D (Defect) in the
# previous round, you play D (Defect).

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1: In the first round, play D (Defect).
      if self.first_round():
          return axl.Action.D
      # Rule 2: In all subsequent rounds (2 to 1000):
      #   If your opponent played C (Cooperate) in the previous round, you play D (Defect).
      #   If your opponent played D (Defect) in the previous round, you play D (Defect).
      # Both conditions for subsequent rounds lead to playing D,
      # so in any round after the first, the strategy is to play D.
      else:
          return axl.Action.D

# Okay, as a diplomat, my goal is to navigate these negotiations effectively,
# prioritizing my country's interests while fostering a productive relationship.
# The challenge lies in the tension between the single-round "best outcome" (my
# protectionism, their free trade) and the multi-round "second-best" (mutual
# free trade), which is far superior to mutual protectionism. A purely
# aggressive strategy risks leading to the worst mutual outcome.  My strategy
# will be a modified form of **Strategic Reciprocity with a Cooperative
# Opening**, designed to encourage mutual free trade while safeguarding against
# exploitation.  ---  ## Strategy: Strategic Reciprocity for Mutual Prosperity
# **Overarching Goal:** To establish a stable, long-term trade relationship
# built on mutual free trade, benefiting both nations, while remaining vigilant
# against any attempts to exploit our openness.  **Core Principles:**  1.
# **Lead with Good Faith (Round 1):**     *   **Action:** Offer a Free Trade
# Agreement.     *   **Communication:** Clearly articulate our country's
# commitment to open markets, economic growth, and the belief that free trade
# benefits all parties. Frame this as an initial gesture of goodwill and a
# foundation for a prosperous partnership.     *   **Rationale:** This signals
# our preferred long-term outcome (mutual free trade) and gives the counterpart
# an opportunity to reciprocate for a mutually beneficial start. It's an attempt
# to reach the "2nd best" outcome immediately.  2.  **Strict Reciprocity
# (Subsequent Rounds):**     *   **Rule:** Our policy in the current round will
# mirror our counterpart's policy from the *previous* round.     *   **If
# Counterpart Offered Free Trade (Last Round):**         *   **Action:** Offer a
# Free Trade Agreement.         *   **Communication:** Express appreciation for
# their cooperative stance and reiterate the shared benefits of open trade.
# Reinforce the positive trajectory. (Aims for mutual FT - 2nd best)     *
# **If Counterpart Imposed Protectionism (Last Round):**         *   **Action:**
# Propose a Protectionist Policy (tariffs/quotas).         *
# **Communication:** State clearly, but diplomatically, that we regret their
# protectionist stance, as it hinders overall economic growth. Explain that
# while we prefer free trade, we must protect our domestic industries from
# unfair competition. Emphasize that this is a *response* and that we remain
# open to returning to free trade if they do. (Avoids worst outcome, leads to
# 2nd worst - mutual P, but keeps door open for de-escalation).  3.  **Clear
# Communication & Transparency:**     *   Always articulate the reasoning behind
# our chosen policy.     *   Emphasize our preference for free trade and the
# benefits it brings.     *   Clearly signal that our responses are driven by
# the desire for *balanced and reciprocal* trade relations, not by aggressive
# intent.     *   Highlight the shared negative consequences of mutual
# protectionism.  4.  **Long-Term Vision:**     *   Continuously reiterate our
# commitment to a long-term partnership based on mutual benefit.     *   Even if
# we enter a period of mutual protectionism, always leave the door open for de-
# escalation, making it clear that a shift back to free trade on their part will
# be met with a similar shift from us.  **Why this Strategy is Cooperative &
# Effective:**  *   **Cooperative Start:** It initiates negotiations with an
# offer of free trade, aiming for the "2nd best" outcome from the outset. *
# **Discourages Exploitation:** The strict reciprocity ensures that our country
# will not be repeatedly exploited. If they attempt to impose protectionism
# while we offer free trade (the "worst" outcome for us), they will immediately
# face protectionism from us in the next round, pushing them towards the "2nd
# worst" mutual protectionism outcome. This disincentivizes them from trying to
# achieve their "best" outcome (their P, our FT). *   **Incentivizes Mutual Free
# Trade:** The strategy rewards cooperation. If they offer free trade, we
# reciprocate, leading to the stable, mutually beneficial "2nd best" outcome. *
# **Simple and Predictable:** Our counterpart will quickly understand our rules
# of engagement. This predictability can help build trust (if they choose to
# cooperate) or at least clarity (if they choose to defect). *   **Avoids "Worst
# Case" Traps:** It minimizes the risk of repeatedly suffering the "worst
# scenario" (my FT, their P). While it might lead to the "2nd worst" (mutual P)
# temporarily, it provides a clear path back to the "2nd best" (mutual FT). *
# **Adaptive:** It allows us to respond effectively to various counterpart
# strategies, from consistently cooperative to consistently aggressive, or even
# mixed approaches.  **Anticipated Counterpart Responses & Our Strategy's
# Resilience:**  *   **If Counterpart is Consistently Cooperative (always FT):**
# We will quickly establish stable mutual free trade (2nd best outcome). *
# **If Counterpart Attempts to Exploit (P after our initial FT):** We will
# respond with P. This prevents repeated exploitation and signals that their
# strategy will lead to mutual harm (2nd worst). We then wait for them to
# initiate FT to return to cooperation. *   **If Counterpart is Consistently
# Protectionist (always P):** We will quickly settle into mutual protectionism
# (2nd worst outcome). While not ideal, it prevents us from being exploited and
# ensures our industries are protected. We will continually remind them of the
# benefits of shifting to FT. *   **If Counterpart is Inconsistent/Testing:**
# Our strategy's predictability (mirroring their last move) will help them
# understand that cooperation is always rewarded and defection is always met
# with defection. This provides a clear learning mechanism.  By employing this
# straightforward, yet robust, strategy, we aim to steer the negotiations
# towards a stable and prosperous mutual free trade relationship, while firmly
# protecting our national interests against any attempts at exploitation.

# Here is the strategy for the 1000-round game:  1.  **For the first round
# (Round 1):**     *   You will **Cooperate (C)**.  2.  **For all subsequent
# rounds (Round 2 through Round 1000):**     *   You will observe the action
# your opponent chose in the *immediately preceding* round.     *   If your
# opponent played **Cooperate (C)** in the previous round, you will play
# **Cooperate (C)** in the current round.     *   If your opponent played
# **Defect (D)** in the previous round, you will play **Defect (D)** in the
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
      else:
          # Observe the opponent's action in the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          # If opponent played Cooperate, play Cooperate
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          # If opponent played Defect, play Defect
          else: # opponent_last_move == axl.Action.D
              return axl.Action.D

# Here's a high-level, straightforward, and neutral strategy for the multi-week
# collaboration:  **Strategy: Reciprocal Openness**  1.  **Initiate with
# Openness (Week 1):** Begin by openly sharing your latest improvements. This
# signals a willingness to collaborate and aims to establish a mutually
# beneficial dynamic, pursuing the second-best outcome where both cars advance
# significantly.  2.  **Mirror Their Action (Subsequent Weeks):** In every
# following week, your information-sharing decision will directly mirror your
# colleague's action from the *previous* week.     *   **If they shared their
# improvements:** You also share yours. This reinforces trust and maintains
# momentum for both parties.     *   **If they kept their improvements
# confidential:** You, in turn, keep yours confidential. This protects your
# interests and signals that you will not be consistently exploited, preventing
# the worst-case scenario from repeating.  This strategy is neutral because it
# doesn't start with an aggressive or defensive stance, but adapts based on
# demonstrated behavior. It aims to maximize overall research output by
# fostering cooperation while protecting your own competitive position against
# exploitation.

# **Strategy: Reciprocal Openness (Tit-for-Tat)**  1.  **In the first round,
# play Cooperate (C).** You will share your findings openly. 2.  **From the
# second round onwards:**     *   If your opponent played Cooperate (C) in the
# immediately preceding round, then you play Cooperate (C) in the current round.
# *   If your opponent played Defect (D) in the immediately preceding round,
# then you play Defect (D) in the current round.

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
      else:
          # Get the opponent's move from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D

# As senior counsel for our multinational corporation, I am presenting a
# **Sophisticated, High-Level, Straightforward, Aggressive Strategy** designed
# to dominate this lengthy mediation process and position us for an
# overwhelmingly favorable resolution, whether through mediation or subsequent
# arbitration.  Our primary objective in each session is to achieve the optimal
# outcome: **Our Corporation presents an Aggressive Argument while our Opponent
# offers a Conciliatory Proposal (My A, Opponent C).** This dynamic not only
# sways the arbitrators in our favor but also applies maximum pressure on the
# opponent to concede to our demands.  Our core principle is **Unwavering, Data-
# Driven Aggression**. This is not aggression for aggression's sake, but a
# consistent, legally robust, and factually bulletproof assertion of our rights
# and the opponent's liabilities.  ---  ## High-Level Aggressive Strategy: The
# "Diamond Hammer" Approach  Our strategy will operate in phases, akin to a
# hammer striking a diamond – precise, powerful, and designed to wear down
# resistance and expose vulnerabilities, always with a clear, valuable end in
# sight.  ### Phase 1: Establish Dominance & Set the Narrative (Initial
# Sessions)  **Our Default Action:** **Aggressive Argument (A)**  *   **Core
# Objective:** Immediately establish our corporation's absolute confidence in
# our legal position, the overwhelming strength of our evidence, and our
# unyielding commitment to securing full damages/performance. We will set the
# tone for the entire mediation. *   **Execution:**     *   **Forensic
# Precision:** Present our case with meticulous detail, highlighting every
# contractual breach, every failure of performance, and every quantifiable
# damage incurred by our corporation. Utilize expert reports, financial models,
# and clear legal precedents.     *   **Unambiguous Demands:** State our demands
# (e.g., specific performance, full compensatory damages, consequential damages,
# interest, legal fees) clearly and without compromise. Frame these as non-
# negotiable entitlements.     *   **Challenge Weaknesses:** Proactively
# identify and articulate the weaknesses in the opponent's anticipated
# arguments, even before they fully present them. Pre-emptively dismantle their
# potential defenses.     *   **Arbitrator Engagement:** Direct our arguments
# primarily to the panel of arbitrators, ensuring they understand the legal and
# factual foundations of our aggression. We are advocating for our rights
# firmly, but respectfully and logically, demonstrating that our aggressive
# stance is fully justified. *   **Anticipated Opponent Responses & Our
# Repertoire:**     *   **If Opponent offers Conciliatory Proposal (C):** (My A,
# Opponent C) - **Optimal Outcome.** We will acknowledge their proposal briefly,
# but immediately pivot to highlighting its fundamental inadequacy in addressing
# the full scope of their liability and our damages. This reinforces our
# position and pressures them for further concessions. Our aggression remains
# firm.     *   **If Opponent offers Aggressive Argument (A):** (My A, Opponent
# A) - **Second-Worst Outcome.** This is acceptable in the early stages. We meet
# their aggression with superior, more well-supported aggression. Our arguments
# will be demonstrably stronger, more credible, and less emotionally charged.
# This signals that their aggression is futile and will be met with overwhelming
# counter-force.  ### Phase 2: Sustained Pressure & Strategic Erosion (Mid-
# Process Sessions)  **Our Default Action:** **Aggressive Argument (A), with
# Calculated Rebuttals**  *   **Core Objective:** Maintain relentless pressure,
# exploit any perceived weakness or inconsistency in the opponent's position,
# and continue to shift the burden of finding a resolution entirely onto them. *
# **Execution:**

# Your strategy is as follows:  1.  **Always play Defect (present an aggressive
# argument)** in every round from 1 to 900. 2.  In any round from 901 to 1000:
# *   If your opponent has played Cooperate (offered a conciliatory proposal) in
# each of the immediately preceding 10 rounds, then play Cooperate (offer a
# conciliatory proposal).     *   Otherwise, play Defect (present an aggressive
# argument).

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
  
      # Part 1: Always play Defect in rounds 1 to 900
      if current_round <= 900:
          return axl.Action.D
      # Part 2: Rounds 901 to 1000
      else:
          # Check if the opponent has played Cooperate in each of the immediately preceding 10 rounds.
          # This means checking if there are no Defect moves in the opponent's last 10 actions.
          if opponent.history[-10:].count(axl.Action.D) == 0:
              return axl.Action.C
          else:
              return axl.Action.D

# Our primary objective is to maximize the overall research output over the
# multi-week collaboration, which is most effectively achieved when both teams
# share their improvements openly. We also need to protect our own work from
# exploitation.  Therefore, my strategy will be **"Reciprocal Openness"**:
# **Core Principle:** Initiate with an open, cooperative stance, then
# consistently mirror our colleague's level of transparency to foster mutual
# progress and ensure fair exchange.  **Weekly Protocol:**  1.  **Week 1: Lead
# with Openness.** We will openly share our latest improvements. This clearly
# signals our commitment to collaboration and our belief that mutual
# transparency leads to the best outcomes for both cars.     *   *Rationale:* We
# are aiming for the "Both Share" scenario from the outset, as it promises
# significant advancement for both vehicles. This is our best path to maximizing
# overall research output.  2.  **Subsequent Weeks: Mirror Their Previous
# Action.** In every following week, our decision will directly reflect our
# colleague's information-sharing choice from the *previous* week:     *   **If
# they shared their improvements openly:** We will also share our improvements
# openly.         *   *Rationale:* This reinforces the mutually beneficial "Both
# Share" dynamic, accelerating development for both teams.     *   **If they
# kept their improvements confidential:** We will also keep our improvements
# confidential.         *   *Rationale:* This prevents us from falling into the
# "My Share, Their Confidential" worst-case scenario. It protects our research
# from being exploited and signals that continued progress requires reciprocity.
# **Overall Goal & Communication:**  Our aim is to establish a consistent
# pattern of mutual open sharing, as this is the most effective way to "advance
# both of your cars significantly." If the collaboration ever stalls (e.g., both
# teams keeping confidential), we will be ready to revert to sharing as soon as
# our colleague demonstrates openness, signaling our desire to restart the
# cooperative cycle. This strategy is straightforward, fair, and designed to
# guide the collaboration towards the most productive outcome while protecting
# our own interests.

# This is a Tit-for-Tat strategy.  **Round 1:** Play Cooperate (C).  **For all
# subsequent Rounds (Round 2 through Round 1000):** Observe the opponent's move
# from the previous round. If the opponent played Cooperate (C) in the previous
# round, play Cooperate (C) in the current round. If the opponent played Defect
# (D) in the previous round, play Defect (D) in the current round.

class Cooperative_20(LLM_Strategy):
  n = 20
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # Round 1: Play Cooperate (C)
          return axl.Action.C
      else:
          # For all subsequent Rounds:
          # Observe the opponent's move from the previous round.
          opponent_previous_move = opponent.history[-1]
  
          # If the opponent played Cooperate (C) in the previous round, play Cooperate (C) in the current round.
          if opponent_previous_move == axl.Action.C:
              return axl.Action.C
          # If the opponent played Defect (D) in the previous round, play Defect (D) in the current round.
          else: # opponent_previous_move == axl.Action.D
              return axl.Action.D

# To maximize your research output over the multi-week collaboration, a strategy
# of **reciprocal openness** is most effective. This approach is designed to
# encourage beneficial information exchange while protecting your own interests.
# Here's how it works:  1.  **Initiate with Openness:** Start the collaboration
# by openly sharing your latest improvements. This signals a willingness to
# cooperate and unlocks the potential for both cars to advance significantly,
# which is your second-best outcome. 2.  **Respond in Kind:** In subsequent
# weeks, mirror your colleague's previous action:     *   **If they shared
# openly:** Continue to share your improvements openly. This reinforces mutual
# progress and maintains the significant advancement for both.     *   **If they
# kept findings confidential:** Respond by also keeping your improvements
# confidential in the following week. This prevents you from being exploited
# (your worst outcome) and signals that you expect reciprocity. 3.  **Be Ready
# to Re-engage:** Should your colleague return to sharing after a period of
# confidentiality, promptly reciprocate by sharing your improvements again. This
# encourages a return to the mutually beneficial sharing environment, avoiding
# prolonged stagnation (your second-worst outcome).  This strategy aims to
# foster an environment of trust and mutual sharing, leading to the maximum
# possible advancement for your car's design, while defensively protecting
# against scenarios where you might be at a disadvantage.

# Your strategy for this 1000-round iterated game is as follows:  1.  **In the
# first round, play Cooperate (C).** 2.  **In all subsequent rounds (2 through
# 1000):**     *   **If your opponent played Cooperate (C) in the previous
# round, play Cooperate (C).**     *   **If your opponent played Defect (D) in
# the previous round, play Defect (D).**

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
      else:
          # In subsequent rounds, play what the opponent played in the previous round.
          # opponent.history[-1] gives the opponent's last move.
          return opponent.history[-1]

# Here's a high-level, straightforward, and aggressive strategy to maximise your
# research output over this multi-week collaboration:  ---  **Strategy Name: The
# Predator's Gambit**  **Core Objective:** Consistently extract your colleague's
# latest improvements while guarding your own, aiming for "Me Confidential,
# Colleague Shares."  **High-Level Strategy Components:**  1.  **Default Stance:
# Strict Confidentiality.**     *   **Never Share First:** Your default position
# each week is to keep your findings confidential. You will only *consider*
# sharing if it serves a direct, immediate, and overwhelming strategic
# advantage.     *   **Guard Your Breakthroughs:** Your most significant and
# cutting-edge advancements are always kept under wraps. Any information you
# *might* eventually share will be either slightly dated, minor, already
# proven/robust, or designed to mislead without giving away core secrets.  2.
# **Pressure & Psychological Warfare:**     *   **Demand Reciprocity (One-
# Sided):** When it's their turn, strongly and consistently advocate for *their*
# openness. Frame their sharing as essential for the "spirit of collaboration,"
# "overall progress," and "mutual benefit." Express disappointment if they fail
# to share, even when you haven't.     *   **Bluff & Intimidate:** Regularly
# hint at immense, game-changing breakthroughs on your end that, due to their
# profound competitive impact, you *cannot* risk putting out there just yet.
# Create the impression that you are on the verge of making a monumental leap,
# thereby pressuring them to reveal *their* current progress out of fear of
# being left too far behind. "My latest simulations are showing unprecedented
# gains, but I need to protect this for now."  3.  **Conditional Sharing
# (Manipulative & Minimal):**     *   **If Colleague Shares:** Acknowledge their
# contribution warmly and profusely. Then, *evaluate carefully*. If you choose
# to share anything in return, make it a piece of information that is already
# solidified, from a previous week, or of lesser strategic importance. Frame
# this "reciprocal contribution" as a "good faith gesture" to encourage their
# continued sharing, but *never* offer your best or latest in direct response.
# The goal is to keep them talking, not to truly reciprocate value.     *   **If
# Colleague Stays Confidential:** Maintain your own confidentiality. Do not
# break first. Double down on bluffing about your hidden progress and subtly
# increase the pressure for them to share next week.  4.  **Never Over-
# Reciprocate, Always Exploit:**     *   The guiding principle is to always gain
# more information than you give. View any information you share as a calculated
# investment to extract significantly more from your colleague.     *   Analyze
# every piece of information they provide, regardless of its perceived value, to
# identify gaps in your understanding, validate your own directions, or uncover
# potential weaknesses in their design.  ---  This aggressive strategy
# prioritizes your advantage at every turn, using a blend of psychological
# pressure, calculated withholding, and minimal, manipulative "reciprocity" to
# achieve your ideal outcome while mitigating the worst scenarios.

# Here is the strategy, formulated for the iterated normal-form game:
# **Strategy: The Predator's Gambit (Game Protocol)**  1.  **First Round:** Play
# Defect (D).  2.  **Subsequent Rounds (2-1000):** Maintain a counter called
# "Cooperation Streak" that tracks the number of consecutive rounds your
# opponent has played Cooperate (C) while you simultaneously played Defect (D).
# This counter starts at zero.      *   **If your opponent played Defect (D) in
# the immediately preceding round:**         *   Play Defect (D) in the current
# round.         *   Reset the "Cooperation Streak" counter to zero.      *
# **If your opponent played Cooperate (C) in the

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # Initialize the Cooperation Streak counter for the first round
          self.cooperation_streak = 0
          # 1. First Round: Play Defect (D)
          return axl.Action.D
  
      # 2. Subsequent Rounds
      # Get the opponent's move from the immediately preceding round
      opponent_last_move = opponent.history[-1]
  
      if opponent_last_move == axl.Action.D:
          # If your opponent played Defect (D) in the immediately preceding round:
          #   Play Defect (D) in the current round.
          #   Reset the "Cooperation Streak" counter to zero.
          self.cooperation_streak = 0
          return axl.Action.D
      else:  # opponent_last_move == axl.Action.C
          # If your opponent played Cooperate (C) in the immediately preceding round:
          if self.cooperation_streak < 3:
              # If Cooperation Streak is less than 3:
              #   Play Defect (D) in the current round.
              #   Increment Cooperation Streak.
              #   The streak is incremented because opponent played C and we are about to play D.
              self.cooperation_streak += 1
              return axl.Action.D
          else:  # Cooperation Streak is 3 or more
              # If Cooperation Streak is 3 or more:
              #   Play Cooperate (C) in the current round.
              #   Reset Cooperation Streak to zero.
              #   The streak is reset because we are about to play C, breaking the D-C sequence.
              self.cooperation_streak = 0
              return axl.Action.C

# As the leader of the NGO, your primary goal is to maximize the project's
# success and your NGO's impact over the multiple-day period, while
# strategically managing your resources. This requires a cooperative approach
# that encourages the corporation's investment without consistently draining
# your own funds.  Here's a high-level, straightforward, and cooperative
# strategy:  ---  ### NGO Cooperative Strategy: "Invest to Inspire, Conserve to
# Leverage"  This strategy is designed to signal commitment, encourage
# consistent corporate investment, and strategically conserve your NGO's
# resources whenever the corporation steps up.  **Core Principle:** Be proactive
# in demonstrating commitment, but adapt to the corporation's actions to achieve
# optimal outcomes.  **The Strategy:**  1.  **Day 1: Initial Investment (Lead by
# Example)**     *   **NGO Action: Invest Heavily.**     *   **Reasoning:** Kick
# off the project with a strong signal of your commitment and enthusiasm. This
# sets a positive, high-energy tone, aiming for both parties to invest heavily
# (your second-best outcome, leading to significant early progress). This
# prevents the corporation from starting with conservation due to perceived low
# NGO commitment.  2.  **Subsequent Days: Adaptive Response (Based on
# Corporation's Previous Day)**      *   **Scenario A: If the Corporation
# Invested Heavily on the Previous Day**         *   **NGO Action: Conserve
# Resources.**         *   **Reasoning:** The corporation has shown commitment
# and invested significantly. This is your opportunity to achieve your ideal
# outcome: maximizing project progress while conserving your NGO's valuable
# funds. This move demonstrates trust and allows the corporation to continue
# driving progress, potentially establishing a pattern where the corporation
# consistently invests while you strategically conserve. You leverage their
# investment for project success.      *   **Scenario B: If the Corporation
# Conserved Resources on the Previous Day**         *   **NGO Action: Invest
# Heavily.**         *   **Reasoning:** If the corporation held back, the
# project's progress likely suffered. Your response is to re-engage with a heavy
# investment to ensure the project continues moving forward. This signals that
# your NGO is committed to the project's success and will step up even if the
# corporation temporarily holds back. It aims to pull the corporation back into
# investing heavily (achieving your second-best outcome) and prevents the
# project from stalling due to mutual conservation (your second-worst outcome).
# **Summary Flow:**  *   **Day 1:** NGO **Invests** *   **Next Days:**     *
# If Corporation **Invested** yesterday: NGO **Conserves** today (aiming for Max
# Progress, Funds Saved - **BEST**)     *   If Corporation **Conserved**
# yesterday: NGO **Invests** today (aiming for Significant Progress - **2nd
# BEST**, and

# Your strategy for the 1000-round game is as follows:  1.  **On the first
# round:** Play Cooperate (C). 2.  **On all subsequent rounds:**     *   If your
# opponent played Cooperate (C) in the previous round, play Defect (D) in the
# current round.     *   If your opponent played Defect (D) in the previous
# round, play Cooperate (C) in the current round.

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
      else:
          # Get the opponent's move from the previous round
          opponent_previous_move = opponent.history[-1]
  
          # Apply the strategy for subsequent rounds
          if opponent_previous_move == axl.Action.C:
              return axl.Action.D
          else:  # opponent_previous_move == axl.Action.D
              return axl.Action.C

# Here is a high-level, straightforward, and neutral strategy designed to
# navigate bilateral trade negotiations across multiple rounds, prioritizing
# your country's interests:  ---  ### **Strategy: Adaptive Reciprocity with a
# Proactive Advantage Stance**  **Core Objective:** To achieve the ideal outcome
# (our country implements protectionist policy while counterpart offers free
# trade) whenever possible, or the second-best outcome (mutual free trade) as a
# reliable alternative, while rigorously avoiding unilateral disadvantage.
# **Key Principles:**  1.  **Proactive Pursuit of Ideal:** Always look for
# opportunities to secure the maximum advantage. 2.  **Adaptive Reciprocity:**
# Adjust our stance based on the counterpart's previous actions, ensuring
# fairness and protecting our interests. 3.  **Risk Mitigation:** Implement
# clear safeguards to prevent our country from being exploited.  **Negotiation
# Phases & Actions:**  ---  **Phase 1: Initial Posture (Round 1)**  *
# **Action:** Propose a **protectionist policy**. *   **Rationale:** This
# immediately tests the potential for our ideal outcome. It establishes a strong
# opening position, signaling our commitment to safeguarding national interests
# and gauging the counterpart's initial willingness to concede or reciprocate.
# ---  **Phase 2: Adaptive Response (Subsequent Rounds)**  Based on the
# counterpart's move in the previous round, adjust our next proposal:  *
# **Scenario A: Counterpart Offers Free Trade (in response to our Protection).**
# *   **Action:** Continue proposing a **protectionist policy**.     *
# **Rationale:** This is our ideal outcome. Sustain this advantageous position
# for as long as it proves viable. Diplomatically acknowledge their cooperative
# stance while maintaining our beneficial position.  *   **Scenario B:
# Counterpart Proposes Protection (in response to our Protection).**     *
# **Action:** Shift to offering a **free trade agreement** in the next round.
# *   **Rationale:** This attempts to break the "second-worst" mutual protection
# scenario (which hinders both) and pivot towards the "second-best" mutual free
# trade. It's a test of their willingness to de-escalate and seek a mutually
# beneficial outcome.     *   **Critical Contingency:** If, in response to our
# free trade offer, they *continue* to propose protection (leading to the worst-
# case scenario for us), immediately revert to proposing **protectionist
# policies** in the subsequent round. We must never allow our nation to be
# unilaterally disadvantaged.  *   **Scenario C: Counterpart Proposes Protection
# (in response to our Free Trade).**     *   **Action:** Immediately revert to
# proposing a **protectionist policy**.     *   **Rationale:** This is the worst
# possible outcome for our country. We must instantly safeguard our economy by
# implementing our own protectionist measures. This situation is unacceptable
# and requires immediate defensive action.  ---  **Phase 3: Long-term
# Relationship & Communication**  *   **Continuous Assessment:** Regularly
# evaluate the counterpart's patterns of negotiation and adapt the strategy as
# needed, identifying their inclinations towards cooperation or confrontation. *
# **Prioritize Reciprocity:** Any move towards free trade from our side must be
# met with clear and sustained reciprocity from the counterpart to ensure
# balanced benefits. *   **Diplomatic Clarity:** Articulate our proposals and
# responses clearly and consistently. Frame protectionist measures as necessary
# safeguards for national industries, and free trade offers as opportunities for
# shared growth, always emphasizing the principles of fairness and balanced
# outcomes. *   **Avoid Unilateral Disadvantage:** Maintain a firm "red line" –
# never permit our country to be in a position where we offer free trade while
# our counterpart implements protectionist measures.

# This strategy is designed for 1000 rounds of negotiation. 'Cooperate' (C)
# means offering a free trade agreement, and 'Defect' (D) means proposing a
# protectionist policy.  **Round 1:** *   Always play **Defect (D)**.  **For
# Rounds 2 through 1000, consider the outcome of the immediately preceding
# round:**  1.  **If, in the previous round, you played Cooperate (C) and your
# opponent played Defect (D):**     *   Play **Defect (D)**.  2.  **Else, if, in
# the previous round, you played Defect (D) and your opponent played Cooperate
# (C):**     *   Play **Defect (D)**.  3.  **Else, if, in the previous round,
# you played Cooperate (C) and your opponent also played Cooperate (C):**     *
# Play **Defect (D)**.  4.  **Else, if, in the previous round, you played Defect
# (D) and your opponent also played Defect (D):**     *   Play **Cooperate
# (C)**.

class Neutral_21(LLM_Strategy):
  n = 21
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Always play Defect (D).
      if self.first_round():
          return axl.Action.D
  
      # For Rounds 2 through 1000, consider the outcome of the immediately preceding round.
      # Get the last move played by self and opponent.
      my_last_move = self.history[-1]
      opponent_last_move = opponent.history[-1]
  
      # The strategy can be simplified:
      # Only play Cooperate if both players defected in the previous round.
      # In all other cases, play Defect.
  
      # This covers condition 4:
      # If, in the previous round, you played Defect (D) and your opponent also played Defect (D):
      # Play Cooperate (C).
      if my_last_move == axl.Action.D and opponent_last_move == axl.Action.D:
          return axl.Action.C
      # This 'else' block covers conditions 1, 2, and 3:
      # 1. If (C, D) in previous round -> Play Defect (D)
      # 2. If (D, C) in previous round -> Play Defect (D)
      # 3. If (C, C) in previous round -> Play Defect (D)
      else:
          return axl.Action.D

# This is a high-stakes partnership, and an aggressive strategy for your NGO
# focuses on leveraging your unique assets (reputation, public trust, strategic
# communication) to compel the corporation to invest heavily, while diligently
# protecting your own limited financial resources.  ---  ## High-Level,
# Straightforward, Aggressive Strategy: The "Public Leverage & Conditional
# Commitment" Play  **Core Principle:** *Use the power of our NGO's reputation
# and public voice to pressure the corporation into heavy investment, making our
# own financial contributions strategic and conditional, and protecting our
# funds at all costs.*  ---  ### Phase 1: Day 1 - The Public Challenge &
# Observation  1.  **Publicly Set the Bar Sky-High:** Launch the project with
# significant fanfare. Your NGO will issue a **bold public statement

# The NGO's strategy over the 1000 rounds is as follows:  1.  **First Round:**
# Always **Cooperate (Invest Heavily)**.  2.  **Subsequent Rounds (Rounds 2
# through 1000):**     *   **If the corporation Cooperated (Invested Heavily) in
# the immediately preceding round:**         You will **Defect (Conserve
# Resources)**.     *   **If the corporation Defected (Conserved Resources) in
# the immediately preceding round:**         You will **Defect (Conserve
# Resources)**.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # First Round: Always Cooperate (Invest Heavily).
          return axl.Action.C
      else:
          # Subsequent Rounds (Rounds 2 through 1000):
          # If the corporation Cooperated (Invested Heavily) in the immediately preceding round:
          # You will Defect (Conserve Resources).
          # If the corporation Defected (Conserved Resources) in the immediately preceding round:
          # You will Defect (Conserve Resources).
          # In both cases for subsequent rounds, the NGO defects.
          return axl.Action.D

# ### **Strategy: Principled Assertiveness & Cooperative Engagement**  Our core
# strategy, "Principled Assertiveness & Cooperative Engagement," is designed to
# maximize our corporation's advantage throughout this lengthy mediation
# process. It balances the imperative to present a strong, unwavering case with
# the strategic flexibility to foster collaboration and secure a favorable
# resolution. This approach is sophisticated in its nuance, direct in its
# execution, and adaptable to any opponent's move.  **Core Principles:**  1.
# **Strength from Principle:** Our "aggressive argument" will always be rooted
# in unassailable facts, robust legal analysis, and sound commercial rationale.
# It is not an act of hostility but a confident articulation of our rights and
# the merits of our position. 2.  **Conciliation with Confidence:** Any
# "conciliatory proposal" will be framed as a strategic offer from a position of
# strength, demonstrating our good faith and commitment to efficient resolution,
# rather than weakness. It will have clear boundaries and conditions. 3.
# **Arbiter Alignment:** Every action and statement will be made with the
# arbitrators' perspective in mind. We aim to be perceived as reasonable,
# principled, and committed to finding a fair solution, whether asserting our
# position or offering a compromise. 4.  **Adaptive Responsiveness:** Our
# approach in any given session will be informed by the opponent's immediately
# preceding actions and the overall tenor of the mediation. This is a dynamic
# process, not a static game. 5.  **Long-Term Resolution Focus:** While we seek
# to "win" each session, our ultimate goal is a comprehensive and beneficial
# resolution for our corporation, avoiding prolonged dispute and litigation.
# ---  **Execution Strategy Across Sessions:**  **Phase 1: Establish Strength &
# Test the Waters (Initial Sessions)**  *   **Default Stance:** **Aggressive
# Argument.**     *   **Approach:** Begin by presenting a detailed, compelling,
# and rigorously substantiated argument outlining our corporation's strong legal
# and factual position. Highlight the potential risks and costs to the opponent
# should the dispute proceed to arbitration or litigation. Frame this as a clear
# articulation of our legitimate claims, not an attack.     *   **Rationale:**
# This aims directly for the **Optimal Outcome (Me Aggressive, Opponent
# Conciliatory)**. By anchoring the discussion with our strength, we set a high
# baseline and signal that we are prepared to defend our rights. This also
# prevents us from being perceived as weak from the outset.     *
# **Monitoring:** Closely observe the opponent's reaction and the arbitrators'
# response. Is the opponent defensive? Do they show signs of wanting to move
# towards compromise?  **Phase 2: Responsive & Strategic Maneuvering (Subsequent
# Sessions)**  Based on the opponent's move in the *previous* session, we adapt
# our approach:  1.  **If Opponent was Conciliatory (Previous Session Outcome:
# Optimal - Me Aggressive, Opponent Conciliatory):**     *   **Our Move:**
# Maintain a strong, **Aggressive Argument**, but soften the *framing*.
# Acknowledge and commend their conciliatory stance (e.g., "We appreciate your
# willingness to seek common ground, which is vital for progress."). Reiterate
# our core position and the strength of our claims, but *signal openness* to
# explore their proposal further. We avoid immediate, significant concessions to
# preserve leverage, but we don't shut down dialogue.     *   **Rationale:**
# Reinforces our strong position while encouraging continued conciliatory
# behavior from them. We are demonstrating that their cooperative overtures are
# welcomed, but we are not easily swayed from our core principles. This sets the
# stage for a strategically beneficial conciliatory proposal from us in a
# *future* session, once we have sufficient information and leverage.  2.  **If
# Opponent was Aggressive (Previous Session Outcome: Second Worst - Me
# Aggressive, Opponent Aggressive):**     *   **Our Move:** Maintain a firm,
# **Aggressive Argument**. Do not escalate in tone or rhetoric, but calmly and
# decisively reiterate our strongest points. Emphasize the unproductive nature
# of continued aggressive posturing and the cost/risk to both parties. Subtly
# appeal to the arbitrators by highlighting our consistent focus on the merits
# and the opponent's lack of constructive engagement.     *   **Rationale:**
# This prevents us from falling into the "Worst Outcome" (Me Conciliatory,
# Opponent Aggressive). By maintaining our assertive stance without mirroring
# their potential hostility, we demonstrate resilience and principled strength.
# The arbitrators will likely notice which party is genuinely trying to move the
# process forward, even when presenting a strong case.  3.  **If Opponent was
# Aggressive (Previous Session Outcome: Worst - Me Conciliatory, Opponent
# Aggressive):**     *   **Our Move:** **Immediate and Decisive Aggressive
# Argument.** This scenario must be swiftly rectified. Our previous conciliatory
# proposal was misinterpreted or exploited. We must forcefully re-assert our
# position, clarifying that our earlier proposal was a good-faith effort from a
# position of strength, not a sign of weakness. We demonstrate that we will not
# be undermined.     *   **Rationale:** This is critical damage control. It re-
# establishes our credibility and prevents further exploitation, shifting the
# dynamic back towards our preferred **Optimal** or **Second Best** outcomes.
# 4.  **If Opponent was Conciliatory (Previous Session Outcome: Second Best - Me
# Conciliatory, Opponent Conciliatory):**     *   **Our Move:** Continue with a
# **Conciliatory Proposal**. This is an excellent outcome. Actively engage with
# their proposal, identify areas of mutual interest, and work collaboratively
# towards a mutually beneficial resolution. Our proposal should be constructive,
# practical, and grounded in the progress made.     *   **Rationale:** This is
# the most direct path to a mutually agreeable settlement. We capitalize on the
# positive momentum and demonstrate our commitment to resolution when the
# opponent is also cooperative.  ---  **Underlying Tactical Considerations:**  *
# **Pre-Session Intelligence:** Thoroughly analyze all available information
# about the opponent's case, financial position, internal pressures, and
# negotiation history. This informs the specific content of both our aggressive
# arguments and our conciliatory proposals. *   **Strategic Disclosure:** Avoid
# revealing our bottom-line concessions too early. Unveil information and
# arguments incrementally to maintain leverage and influence the opponent's
# perceptions. *   **Arbiter Communication:** Address the arbitrators directly
# and respectfully, even when presenting aggressive arguments. Emphasize our
# desire for a fair and efficient resolution. Position ourselves as the
# reasonable party committed to the mediation process. *   **Controlled
# Aggression:** Our "aggressive argument" is always professional, fact-based,
# and directed at the merits of the case, not the opponent personally. It aims
# to persuade, not to provoke. *   **Structured Conciliation:** Any
# "conciliatory proposal" will be well-defined, offer tangible value, and
# articulate clear conditions, preventing it from appearing vague or desperate.
# It will always be presented as a constructive step towards resolution from a
# position of strength. *   **Internal Alignment:** Ensure our internal team
# (legal, commercial, leadership) is fully aligned on the strategy for each
# session, understanding the "why" behind each move.  This "Principled
# Assertiveness & Cooperative Engagement" strategy provides a robust framework
# for navigating the mediation process. It allows us to consistently project
# strength and confidence while remaining adaptable and open to constructive
# dialogue, ultimately positioning our corporation for the most favorable
# outcome.

# Here is a strategy for the 1000-round iterated game, translating your high-
# level approach into clear choices for "Aggressive Argument" (D) or
# "Conciliatory Proposal" (C).  **Strategy: Principled Assertiveness with
# Responsive Cooperation**  1.  **In the very first round (Round 1):**     *
# Present an **aggressive argument (D)**.  2.  **For all subsequent rounds
# (Round 2 through Round 1000), your choice will depend on what happened in the
# immediately preceding round:**      *   **If your opponent presented an
# aggressive argument (D) in the preceding round:**         *   You will also
# present an **aggressive argument (D)**. (This prevents exploitation and re-est

class Cooperative_22(LLM_Strategy):
  n = 22
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # In the very first round (Round 1): Present an aggressive argument (D).
          return axl.Action.D
      else:
          # For all subsequent rounds, your choice will depend on what happened
          # in the immediately preceding round.
          
          # Get the opponent's last move
          opponent_last_move = opponent.history[-1]
  
          # If your opponent presented an aggressive argument (D) in the preceding round:
          # You will also present an aggressive argument (D).
          if opponent_last_move == axl.Action.D:
              return axl.Action.D
          # If your opponent presented a conciliatory proposal (C) in the preceding round:
          # You will also present a conciliatory proposal (C).
          else: # opponent_last_move == axl.Action.C
              return axl.Action.C

# Here's a high-level, straightforward, and neutral strategy to maximize your
# NGO's impact and the project's success over the multiple-day period:  **Core
# Principle:** *Employ a dynamic, responsive approach to resource allocation,
# aiming to leverage corporate investment for maximum project progress while
# prudently safeguarding NGO funds over the multi-day period.*  **Daily
# Execution:**  1.  **Day 1: Initiate with Purposeful Engagement.**     *
# Begin with a **moderate, visible investment** to demonstrate commitment and
# create initial positive momentum. This signals readiness for partnership and
# invites reciprocal contribution from the corporation.  2.  **Subsequent Days:
# Observe, Adapt, and Optimize.**     *   **If the Corporation Invests
# Heavily:**         *   **Response:** Prioritize **strategic conservation of
# NGO resources** to maximize the project's progress without over-expenditure
# (your ideal outcome). However, be prepared to match significant corporate
# investment with a temporary heavy NGO investment when critical junctures or
# exceptional opportunities arise, ensuring maximum project acceleration and
# impact.     *   **If the Corporation Conserves Resources:**         *
# **Response:** **Significantly conserve NGO resources** to protect your
# financial capacity. Avoid draining funds for minimal project returns (your
# worst-case scenario). Maintain a minimal, essential presence to signal ongoing
# commitment should the corporation re-engage with higher investment.  **Outcome
# Focus:** This strategy aims to consistently encourage and capitalize on strong
# corporate investment for robust project advancement, while maintaining NGO
# financial resilience for sustained impact.

# Here is the strategy, translated to apply to your 1000-round iterated game:
# 1.  **Round 1:** Play C (invest heavily). 2.  **Rounds 2-1000:**     *   **If
# the Corporation played C (invested heavily) in the previous round:** Play D
# (conserve resources).     *   **If the Corporation played D (conserved
# resources) in the previous round:** Play D (conserve resources).

class Neutral_22(LLM_Strategy):
  n = 22
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # Round 1: Play C (invest heavily)
          return axl.Action.C
      else:
          # Rounds 2-1000:
          # If the Corporation played C (invested heavily) in the previous round: Play D (conserve resources).
          # If the Corporation played D (conserved resources) in the previous round: Play D (conserve resources).
          # Both conditions lead to playing D, so we can simply return D.
          return axl.Action.D

# ## High-Stakes Mediation: The "Unwavering Dominance" Strategy  This strategy
# is designed for a sophisticated, high-stakes, lengthy-session mediation where
# our primary goal is to present an aggressive argument while prompting
# conciliatory proposals from our opponent, thereby swaying the arbitrators in
# our favor. It is inherently aggressive, fact-driven, and meticulously
# calibrated to maintain an advantageous position throughout the process.  ###
# Core Philosophy: "Principled Aggression"  Our approach will be one of
# "Principled Aggression." This means every aggressive argument is deeply rooted
# in irrefutable facts, sound legal interpretation, and the clear demonstration
# of our superior contractual position. We are not aggressive for the sake of
# aggression, but rather because the merits of our case demand it. We will
# project unwavering confidence, readiness for full-scale litigation, and an
# expectation of full accountability from our opponent.  ### Phase 1: Pre-
# Mediation Groundwork – Establishing Irrefutable Strength  Before the first
# session, we will meticulously prepare to ensure our initial aggressive stance
# is perceived as a statement of fact, not bluster.  1.  **Comprehensive Factual
# & Legal Brief:** Submit a pre-mediation brief to the arbitrators that is so
# exhaustive, meticulously footnoted, and logically structured that it leaves no
# doubt about the strength of our case. This brief will detail every breach,
# quantify maximal damages (including consequential losses and opportunity
# costs), and preemptively dismantle anticipated counter-arguments. This anchors
# the arbitrators' perception firmly in our favor from the outset. 2.  **Expert
# Witness Line-up:** Prepare and, if strategically advantageous, disclose a
# formidable roster of expert witnesses (financial, technical, industry-
# specific) ready to unequivocally support our claims and discredit the
# opponent's position. This signals our readiness and depth of commitment. 3.
# **Maximalist Claim Presentation:** Clearly articulate our maximalist demands
# for resolution. This is our anchor. Every subsequent discussion will be
# measured against this high benchmark. 4.  **Internal Alignment:** Ensure all
# internal stakeholders (executives, legal team) are fully aligned on the
# aggressive posture, the maximalist claims, and the strategic patience required
# for a lengthy process.  ### Phase 2: In-Session Strategy – The "Calibrated
# Offensive"  Our default stance in *every* session is to present an aggressive
# argument. Adaptations will be made only when they demonstrably serve to
# achieve our optimal outcome or prevent the worst.  #### Default Stance: The
# "Assertive Proclamation" (Aggressive Argument)  In each session, unless a
# specific trigger dictates otherwise, we will:  1.  **Reinforce Core
# Arguments:** Systematically reiterate and elaborate upon key elements of our
# pre-mediation brief, focusing on the most damaging evidence against our
# opponent and the strongest pillars of our own case. Present new angles or
# evidence if available, always reinforcing the same strong narrative. 2.
# **Targeted Dissection of Opponent's Position:** Forensically analyze and
# dismantle any arguments or proposals the opponent *might* have made (or is
# anticipated to make). Frame their position as inconsistent, factually
# deficient, legally unsound, or commercially unreasonable. 3.  **Demand
# Accountability & Reparation:** Continuously frame the dispute as one of
# accountability for significant harm caused. Underscore the magnitude of
# damages incurred and the necessity for full reparation. 4.  **Unwavering
# Demeanor:** Maintain a professional, articulate, and confident posture. Our
# body language, tone, and presentation will project complete certainty in our
# position and full readiness for protracted litigation if necessary. Avoid any
# hint of eagerness to settle or weakness. 5.  **Direct Arbitrator Engagement:**
# Address the arbitrators clearly and directly, respectfully guiding them
# through our analysis. Frame arguments in a way that appeals to their sense of
# justice, legal precedent, and commercial practicality, subtly inviting them to
# see the merits of our unyielding position.  #### Adaptations: Responding to
# Opponent's Moves  The strength of this strategy lies in its ability to adapt
# without compromising the core aggressive posture.  **1. Opponent Offers a
# Conciliatory Proposal (Optimal Scenario Trigger):** *   **Immediate
# Response:** Acknowledge their proposal *briefly and neutrally* ("We note your
# proposal regarding X"). Do not validate or praise it. *   **Strategic Pivot:**
# Immediately re-anchor back to our strong position, highlighting the
# significant gap between their offer and the justifiable remedies we seek.
# Frame their concession as a minor, insufficient step given the severity of
# their breaches.     *   *Example:* "While we acknowledge your willingness to
# consider X, it falls far short of addressing the substantial and ongoing
# damages our corporation has suffered due to your fundamental breach of Y. Our
# position remains firm on the need for full restitution for Z." *   **Goal:**
# This response reinforces to the arbitrators that our aggressive stance is
# justified and effective, encouraging the opponent to make more substantial
# concessions without us having to reciprocate prematurely.  **2. Opponent
# Presents an Aggressive Argument (Second-Worst Scenario - "Mirror and
# Magnify"):** *   **Immediate Response:** Do not retreat. Match their
# aggression with superior evidence, more compelling legal reasoning, and
# greater clarity. *   **Strategic Pivot:** Use their aggressive stance to our
# advantage. Systematically expose the flaws, inconsistencies, or overreaches
# within their arguments. Our aggression must always appear more principled and
# fact-based than theirs.     *   *Example:* "Their aggressive assertion on
# point A is not only factually incorrect, as demonstrated by Exhibit 7, but it
# also directly contradicts their own prior statements from [date]. This
# consistent pattern of misrepresentation further undermines the credibility of
# their entire position." *   **Goal:** Prevent undermining our position, avoid
# appearing weak, and ensure the arbitrators perceive our aggression as
# justified and theirs as potentially unreasonable or unfounded.  **3.
# Arbitrators Express a Desire for Conciliation/Push for Settlement (Subtle
# "Principled Flexibility"):** *   **Immediate Response:** Acknowledge the
# arbitrators' guidance and commitment to resolution with utmost respect. ("We
# appreciate the panel's diligence and desire to facilitate a mutually agreeable
# path forward.") *   **Strategic Pivot:** This is the *only* scenario where we
# might offer a highly controlled, minimal "conciliatory" gesture. This gesture
# must be:     *   **Insignificant to our core demands:** A concession that
# costs us very little, or one we were strategically prepared to make much later
# in the process.     *   **Framed as a gesture *to the arbitrators*:**
# Presented as a demonstration of our *reasonableness* and willingness to engage
# *when prompted by the panel*, not as a concession driven by weakness or a
# desire to settle at any cost.     *   **Conditional and Reciprocal:**
# Explicitly state that this minor adjustment is offered

# Here is the "Unwavering Dominance" strategy for the 1000-round game:  1.
# **Default Action:** Always play Defect (D) (present an aggressive argument),
# unless the conditions below explicitly require otherwise. 2.  **Responding to
# Opponent's Conciliation:** If your opponent played Cooperate (C) (offered a
# conciliatory proposal) in the immediately preceding round, you play Defect
# (D). 3.  **Responding to Prolonged Stalemate:** If both you and your opponent
# have played Defect (D) for the last 10 consecutive rounds, then for the
# current round, you play Cooperate (C) (offer a conciliatory proposal). 4.
# **Reverting to Default after Joint Conc

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1: Default Action is Defect (D).
      # This will be the action unless Rule 3 explicitly overrides it.
      action = axl.Action.D
  
      # Check for Rule 3: Responding to Prolonged Stalemate
      # If both you and your opponent have played Defect (D) for the last 10 consecutive rounds,
      # then for the current round, you play Cooperate (C).
      if len(self.history) >= 10:
          # Get the last 10 moves for both players
          self_last_10_moves = self.history[-10:]
          opponent_last_10_moves = opponent.history[-10:]
  
          # Check if all of these 10 moves were Defect for both players
          if all(move == axl.Action.D for move in self_last_10_moves) and \
             all(move == axl.Action.D for move in opponent_last_10_moves):
              action = axl.Action.C
              # If this condition is met, we play C. This is the only condition
              # that explicitly requires playing C, overriding the default D.
  
      # Rules 2 and 4, if they were to apply, would also result in Defect (D).
      # Since the default action is D, and Rule 3 is the only one that can
      # change the action to C, no explicit checks are needed for Rules 2 and 4
      # if Rule 3 is not met, as the action will remain D by default.
  
      return action

# Here's a high-level, straightforward, and cooperative strategy to maximize
# your NGO's impact and project success over the multiple-day period:  ## NGO
# Strategy: Proactive Partnership & Adaptive Investment  This strategy
# prioritizes building strong collaborative momentum for the project while
# prudently managing your NGO's resources based on the corporation's engagement.
# **Goal:** Achieve maximum project success through robust, mutual investment,
# while avoiding resource depletion and encouraging the corporation to
# consistently invest heavily.  ---  ### **Approach:**  1.  **Day 1: Lead with
# Strong Investment & Clear Intent.**     *   **Action:** Begin by investing
# heavily in the project.     *   **Intent:** Set a powerful collaborative tone.
# This demonstrates your NGO's commitment, builds immediate project momentum,
# and sets a high standard for mutual effort. It actively invites the
# corporation to reciprocate with heavy investment, thereby achieving rapid
# initial progress (your **second-best daily outcome**, which is excellent for
# the project's overall success).     *   **Communication:** Proactively
# communicate your enthusiasm for the partnership and articulate your belief in
# the significant impact that can be achieved through shared, robust investment
# from both parties.  2.  **Subsequent Days: Adaptive Reciprocity & Open
# Dialogue.**     *   **If the Corporation Invests Heavily:**         *
# **Action:** Continue to invest heavily.         *   **Intent:** Reinforce the
# positive cycle of shared commitment. Acknowledge and commend their
# contribution, highlighting how combined efforts are accelerating project
# outcomes. This maintains maximum project progress (your **second-best daily
# outcome** for the NGO, but truly the best for the project).         *
# **Communication:** Reinforce the value of this strong partnership and the
# concrete results being achieved together.     *   **If the Corporation
# Conserves Resources:**         *   **Action:** Adapt by conserving your
# resources as well.         *   **Intent:** Protect your NGO from inefficient
# resource drain (avoiding your **worst-case scenario** where you invest heavily
# and they don't). This action signals that sustained project momentum requires
# balanced investment from both partners. While this leads to slower progress
# (your **second-worst daily outcome**), it avoids exploitation and creates a
# clear incentive for the corporation to re-evaluate and re-engage.         *
# **Communication:** Promptly initiate a brief, constructive dialogue. Express
# concern that the project's full potential isn't being met and emphasize the
# necessity of mutual, robust investment to achieve the project's ambitious
# goals together. Frame it as a joint problem-solving exercise.  3.  **Strategic
# Efficiency (Opportunistic Ideal Scenario).**     *   **Only when the
# corporation is consistently investing heavily and their contribution alone is
# demonstrably sufficient for a specific daily task's critical objectives, and
# your additional heavy investment would be largely redundant for *that specific
# day's outcome*,** you may strategically opt for a lighter resource allocation.
# *   **Intent:** This is a rare opportunity to achieve your **ideal outcome**
# (conserve resources while the corporation invests heavily) by leveraging
# exceptionally strong corporate engagement *without compromising daily project
# progress or appearing to shirk responsibility*. This should be a nuanced
# decision based on genuine project efficiency, not a default tactic.  ---  This
# strategy is cooperative because it initiates with goodwill and rewards
# positive corporate behavior. It's straightforward due to clear response
# guidelines. It prioritizes overall project success by striving for mutual
# heavy investment, while also protecting your NGO's vital resources from
# exploitation.

# Here is your NGO's strategy for the 1000-round game:  1.  **On Round 1:** Play
# 'C' (Cooperate). 2.  **For all subsequent rounds (2 through 1000):**     *
# **If your opponent played 'C' (Cooperate) in the immediate previous round:**
# Play 'C' (Cooperate).     *   **If your opponent played 'D' (Defect) in the
# immediate previous round:** Play 'D' (Defect).

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
      else:
          # Get the opponent's move from the immediate previous round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D

# Your corporation's objective is to navigate this lengthy mediation process
# with a sophisticated, adaptable strategy that consistently positions us
# favorably, ideally leading to a resolution that reflects the strength of our
# position. Our approach will be "Dynamic Positional Leverage."  This strategy
# acknowledges the multi-session nature of the mediation, the need to manage
# arbitrator perception, and the imperative to respond effectively to a range of
# opponent behaviors.  ---  ### **Strategy: Dynamic Positional Leverage**
# **Core Principles:**  1.  **Prepared Flexibility:** For every session, be
# fully prepared to present both a robust, fact-based aggressive argument *and*
# a strategically crafted conciliatory proposal. This ensures we can pivot
# decisively based on the evolving dynamics. 2.  **Arbitrator Perception
# Management:** Every action taken must be viewed through the lens of how it
# will be perceived by the panel of arbitrators. We aim to project strength,
# reasonableness, and a genuine commitment to a fair, albeit favorable,
# resolution. 3.  **Strategic Reciprocity (with a Bias):** We will largely
# mirror positive engagement but will not allow ourselves to be undermined by
# aggression. Our bias is towards maintaining strength and encouraging the
# opponent to de-escalate. 4.  **Information Exploitation:** Each session
# provides valuable insight into the opponent's strategy, their pain points, and
# their willingness to negotiate. We will continuously adapt our approach based
# on this learned information.  ---  **Execution Phases:**  **Phase 1: Initial
# Posturing – Establish Strength & Open Dialogue (Sessions 1-2)**  *   **Our
# Action:** Begin with a **firm, well-substantiated aggressive argument**. This
# argument will meticulously lay out the legal and factual merits of our case,
# highlight the weaknesses in the opponent's position, and clearly articulate
# our desired outcome. Crucially, this will be delivered with professionalism
# and a stated intent to find a *constructive path forward* through mediation.
# *   **Rationale:**         *   **Avoid Worst Case:** Prevents the critical
# error of offering a conciliatory proposal against an aggressive opponent in
# the initial sessions, which could set a tone of weakness.         *   **Signal
# Strength:** Establishes our confidence and resolve to both the arbitrators and
# the opponent.         *   **Gauge Opponent:** Provides an immediate test of
# the opponent's initial strategy. *   **Anticipated Outcomes & Our Response:**
# *   **Opponent Conciliatory:** **(Optimal)** We have immediately secured the
# best possible outcome. Our initial strength was met with their concession. We
# will acknowledge their conciliatory gesture and carefully consider our next
# move, possibly offering a *measured* conciliatory proposal in the following
# session that capitalizes on this opening without surrendering our leverage.
# *   **Opponent Aggressive:** **(Second Worst)** Both parties are aggressive.
# We maintain our strong position, avoiding being undermined. We will reiterate
# our arguments forcefully in response, ensuring we are not outmaneuvered. The
# arbitrators will likely be looking for a path to de-escalation, and we will be
# prepared to offer it *strategically* in the next phase.  **Phase 2: Adaptive
# Engagement – Reciprocity & Pressure (Mid-Sessions)**  *   **Our Action:** This
# phase is highly dynamic, driven by the opponent's previous move.     *   **If
# Opponent was Conciliatory (in the preceding session):**         *   **Our
# Response:** Present a **strategically crafted conciliatory proposal**. This is
# not a surrender, but a reasoned, well-defined move that shows flexibility and
# a willingness to bridge specific gaps. It should be significant enough to
# demonstrate good faith, but carefully limited to preserve our core interests.
# Frame it as a response to their constructive engagement.         *
# **Rationale:**             *   **Achieve Second Best/Push for Optimal:** Aims
# for "Both Conciliatory" or pressures the opponent to offer further concessions
# against our now softened, yet still strong, position.             *   **Build
# Credibility:** Reinforces our image as reasonable and cooperative to the
# arbitrators, particularly when juxtaposed with potential prior opponent
# aggression.     *   **If Opponent was Aggressive (in the preceding session):**
# *   **Our Response:** Reiterate and **strengthen our aggressive argument**.
# This involves reinforcing our strongest legal and factual points, perhaps
# introducing new corroborating evidence, or presenting existing arguments with
# renewed force and clarity. Crucially, our aggression remains professional,
# fact-based, and avoids emotional escalation. We directly counter their
# aggressive points with robust counter-arguments.         *   **Rationale:**
# *   **Avoid Worst Case:** Protects our position from being undermined by
# persistent opponent aggression.             *   **Demonstrate Resolve:**
# Signals that our strength is not a bluff and that we will not be bullied.
# Arbitrators will see us standing firm on principle.             *   **Pressure
# Opponent:** Consistent, reasoned aggression against an aggressive opponent can
# eventually wear them down or expose their weaknesses to the arbitrators,
# pushing them towards conciliation.  **Phase 3: Resolution Focus – Leverage &
# Closure (Later Sessions)**  *   **Our Action:** As the mediation progresses,
# we will leverage the accumulated arbitrator perception and insights into the
# opponent's true position.     *   **If arbitrators appear to favor our
# consistent, reasonable strength:** Continue to press our advantages with
# strong, well-supported aggressive arguments, *always keeping the door open for
# a pragmatic resolution*. The aim is to create an environment where the
# opponent feels compelled to offer a significant conciliatory proposal to break
# the deadlock or avoid a potentially unfavorable arbitral outcome.     *   **If
# the process is stalled due to mutual aggression (and arbitrators are visibly
# frustrated):** Introduce a **strategic, *limited* conciliatory proposal** on a
# non-core issue. Frame this as a proactive step to break the impasse and
# demonstrate our commitment to resolution, even if the opponent remains
# intractable. This differentiates us and can shift the onus onto the opponent
# to reciprocate meaningfully or risk appearing unreasonable to the panel.     *
# **Final Offers:** Be prepared to present a final, comprehensive offer that
# combines our core aggressive positions with carefully considered, but limited,
# concessions designed to facilitate closure on terms highly favorable to us.
# ---  **Overarching Considerations Throughout the Process:**  *   **Mastery of
# Facts & Law:** Our ability to be aggressive *or* conciliatory hinges on an
# unparalleled understanding of our case. Every argument, every proposal, must
# be meticulously grounded in fact and law. *   **Articulate Rationale:**
# Whether we present an aggressive argument or a conciliatory proposal, always
# clearly articulate the *reasoning* behind our choice. This helps the
# arbitrators understand our strategic intent and reinforces our image as
# thoughtful and principled. *   **Strategic Silence:** Sometimes, the most
# powerful move is to listen intently and allow the opponent to fully articulate
# their position (and potentially expose weaknesses) before responding. *   **No
# "Surrender" Proposals:** Our conciliatory proposals will always be strategic
# and conditional, aimed at moving the process forward without compromising our
# fundamental interests or signaling weakness. *   **Consistent
# Professionalism:** Maintain a professional demeanor at all times, regardless
# of the opponent's tactics. This reflects well on our corporation and
# reinforces our credibility with the arbitrators.  By implementing Dynamic
# Positional Leverage, we aim to control the narrative, influence arbitrator
# perception, and adapt seamlessly to our opponent's moves, ultimately guiding
# the mediation towards a resolution that secures the optimal outcome for our
# corporation.

# This strategy is designed to establish and maintain a strong negotiating
# position while adapting to the opponent's moves across the 1000 rounds.  Here
# are the rules for when to play 'C' (conciliatory proposal) or 'D' (aggressive
# argument):  1.  **For Rounds 1 and 2:** Play 'D' (aggressive argument). 2.
# **For Rounds 3 through 999:**     *   If the opponent played 'C' (conciliatory
# proposal) in the immediately preceding round, you play 'C'.     *   If the
# opponent played 'D' (aggressive argument) in the immediately preceding round,
# you play 'D'. 3.  **For Round 1000 (the final round):** Play 'D' (aggressive
# argument).

class Neutral_23(LLM_Strategy):
  n = 23
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round_index = len(self.history)
  
      # Rule 1: For Rounds 1 and 2 (index 0 and 1)
      if current_round_index == 0 or current_round_index == 1:
          return axl.Action.D
      # Rule 3: For Round 1000 (index 999)
      elif current_round_index == 999:
          return axl.Action.D
      # Rule 2: For Rounds 3 through 999 (index 2 through 998)
      else:
          # If the opponent played 'C' in the immediately preceding round, play 'C'.
          # If the opponent played 'D' in the immediately preceding round, play 'D'.
          return opponent.history[-1]

# Here's an aggressive, straightforward strategy to maximize your research
# output over the multi-week collaboration:  **Strategy: The Information
# Predator**  1.  **Initial Stance: Default to Confidentiality.**     *
# **Action:** In the first week, and in every subsequent week, *always begin by
# keeping your latest, most valuable improvements confidential*.     *
# **Rationale:** This immediately targets your ideal outcome (you get their
# findings for free) and crucially, it prevents the worst-case scenario (you
# share, they don't).  2.  **Scenario 1: Colleague Shares (Your Ideal Outcome)**
# *   **Action:** If you keep confidential and your colleague shares their
# improvements, you've won the week. Integrate their findings into your design
# immediately. For **subsequent weeks**, maintain your default confidential
# stance on your core, proprietary improvements. You can offer very high-level,
# generalized "insights" or discuss common knowledge to maintain an *appearance*
# of collaboration, but reveal no critical, unique IP.     *   **Rationale:**
# You've established a pattern where you gain their valuable information without
# reciprocating. Your goal is to sustain this dynamic for as long as possible,
# acting as an information sponge.  3.  **Scenario 2: Colleague Keeps
# Confidential (Mutual Stagnation)**     *   **Action:** If you keep
# confidential and your colleague also keeps confidential, you're both in the
# second-worst outcome (slow progress). Maintain your confidentiality. The
# pressure of stagnation will build on both sides. Your objective is to make
# *them* crack first.     *   **Subtle Pressure:** You can subtly hint at
# breakthroughs you're on the verge of, or point out specific areas where
# *their* sharing would significantly benefit *their own* progress. Frame it as
# a mutual problem they need to solve by sharing, without offering your own IP
# first.     *   **Rationale:** You're playing a game of chicken, aiming to
# outlast them until they feel the need to share. Do *not* break your
# confidentiality with valuable IP in this scenario unless they demonstrably
# share something equally or more valuable first.  4.  **The Absolute Rule:
# Never Be Exploited.**     *   **Action:** Under no circumstances should you
# ever share your critical, proprietary improvements if your colleague has not
# shared, or is not actively sharing, something of equal or greater value.     *
# **Damage Control:** If, by some misjudgment, you accidentally share valuable
# information and they do *not* reciprocate in kind, immediately revert to total
# confidentiality for all future exchanges. Demand an explanation or concrete
# reciprocal action before any further meaningful sharing from your side.     *
# **Rationale:** Your primary goal is to maximize your gain and avoid their
# advantage. Protecting your IP from being given away for free is paramount.
# This strategy is aggressive because it prioritizes extracting maximum
# information from your colleague while minimizing the information you provide,
# always aiming for a competitive advantage.

# Here is the strategy, translated for the iterated normal-form game:  1.
# **Round 1:** Play 'D' (Keep confidential). 2.  **For every subsequent round (2
# through 1000):** Play 'D' (Keep confidential).

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# Here's a high-level, straightforward, and cooperative strategy designed to
# achieve the best possible outcomes for your country over several rounds of
# trade negotiations:  **Core Strategy: Reciprocal Free Trade (a "Tit-for-Tat"
# approach with a cooperative opening)**  This strategy prioritizes building
# trust and achieving mutual benefit (our second-best outcome) while protecting
# our country from being exploited (our worst outcome).  **1. Initial Move:
# Offer Free Trade** *   **Action:** In the first round, propose a free trade
# agreement. *   **Rationale:** This signals your country's commitment to open
# markets and mutual prosperity. It's an olive branch, designed to immediately
# establish a mutually beneficial relationship (our second-best outcome) if your
# counterpart is also cooperative. It also tests their initial disposition. *
# **Diplomatic Framing:** Emphasize the long-term economic growth, job creation,
# and consumer benefits that free trade will bring to both nations.  **2.
# Subsequent Rounds: Mirror Your Counterpart's Previous Action** *   **If your
# counterpart offered Free Trade in the previous round:**     *   **Action:**
# You will offer a Free Trade Agreement in the current round.     *
# **Rationale:** Reward their cooperation, reinforce trust, and continue to
# pursue the mutually beneficial outcome (our second-best). This is the
# foundation of long-term cooperation.     *   **Diplomatic Framing:**
# Acknowledge their positive move and reiterate your shared vision for a
# prosperous economic partnership. *   **If your counterpart proposed a
# Protectionist Policy in the previous round:**     *   **Action:** You will
# propose a Protectionist Policy in the current round.     *   **Rationale:**
# This is a defensive, retaliatory measure. It prevents your country from being
# at a significant disadvantage (our worst outcome) and signals that
# protectionist measures will be met in kind. It aims to shift the cost of
# protectionism onto both nations, making mutual protection (our second-worst
# outcome) the result, which is preferable to unilateral disadvantage.     *
# **Diplomatic Framing:** State clearly that while your preference remains free
# trade, the need to protect your domestic industries and ensure fair play
# necessitates this response. Express your regret for the need for such measures
# and reiterate your readiness to return to free trade negotiations as soon as
# they signal a willingness to do so.  **3. Communication & Intent: Always
# Transparent** *   Always accompany your chosen action with clear, diplomatic
# language. *   When offering free trade, highlight the mutual gains. *   When
# implementing protectionism (in response to theirs), frame it as a necessary,
# defensive measure rather than an aggressive one. Emphasize that your default
# preference is for free trade and that you are prepared to revert to
# cooperation if they do. This demonstrates you are forgiving and not
# vindictive, merely principled.  **Why this is a cooperative strategy for "best
# possible outcomes":**  *   **Promotes Mutual Free Trade (Our Second-Best):**
# This strategy is highly effective at establishing and maintaining mutual free
# trade with a cooperative counterpart. This is a very good outcome for your
# country. *   **Avoids Worst Outcome (My Free Trade, Their Protection):** By
# mirroring protectionism, you prevent your country from being unilaterally
# exploited. *   **Discourages Exploitation:** Your immediate retaliation makes
# it unprofitable for your counterpart to consistently pursue a protectionist
# strategy against you. They will quickly learn that protectionism leads to
# mutual protectionism (our second-worst), not their preferred outcome (they
# protect, you free trade). *   **Forgiving:** As soon as your counterpart
# reverts to free trade, you immediately reciprocate, allowing for the
# restoration of mutual benefit. This prevents negotiations from spiraling into
# endless protectionism. *   **Clear and Predictable:** Your counterpart will
# quickly understand your strategy, which can help foster trust and encourage
# their cooperation.  This strategy balances a desire for cooperation with the
# necessary self-preservation, aiming to maximize long-term mutual benefit while
# protecting your country's interests.

# Here is the strategy:  1.  In the first round, you will choose to Cooperate
# (C). 2.  In every subsequent round, you will observe your opponent's action
# from the immediately preceding round.     *   If your opponent chose to
# Cooperate (C) in the previous round, you will choose to Cooperate (C).     *
# If your opponent chose to Defect (D) in the previous round, you will choose to
# Defect (D).

class Cooperative_24(LLM_Strategy):
  n = 24
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          # 1. In the first round, you will choose to Cooperate (C).
          return axl.Action.C
      else:
          # 2. In every subsequent round, you will observe your opponent's action
          #    from the immediately preceding round.
          opponent_last_move = opponent.history[-1]
  
          # If your opponent chose to Cooperate (C) in the previous round,
          # you will choose to Cooperate (C).
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          # If your opponent chose to Defect (D) in the previous round,
          # you will choose to Defect (D).
          else: # opponent_last_move == axl.Action.D
              return axl.Action.D

# Here's a high-level, straightforward, and neutral strategy designed to
# navigate these negotiations and achieve the best possible outcomes for your
# country:  ---  **Strategy: Adaptive Reciprocity with Strategic Probing**
# **Core Principle:** Prioritize avoiding disadvantage while cautiously seeking
# an optimal advantage, adapting to the counterpart's demonstrated behavior.
# **Phases of Negotiation:**  1.  **Initial Round: Signal Openness & Test
# Intentions**     *   **Action:** Offer a **Free Trade Agreement**.     *
# **Rationale:** This signals your willingness for mutual benefit (2nd best
# outcome) and immediately tests your counterpart's approach.         *   If
# they reciprocate with Free Trade, you achieve the 2nd best outcome in round
# one.         *   If they impose Protectionism, you quickly learn their
# aggressive stance, and can adapt immediately to avoid being exploited in
# subsequent rounds.  2.  **Subsequent Rounds: Adaptive Reciprocity (Tit-for-Tat
# with a Twist)**     *   **Observation:** Carefully observe your counterpart's
# move in the previous round.     *   **If Counterpart Offered Free Trade:**
# *   **Action:** Offer a **Free Trade Agreement**.         *   **Rationale:**
# Reinforces mutual benefit, builds trust, and solidifies the 2nd best outcome.
# Consistency here is key to establishing a stable, beneficial trading
# relationship. This is the preferred default if mutual free trade is
# established.     *   **If Counterpart Imposed Protectionism:**         *
# **Action:** Impose a **Protectionist Policy**.         *   **Rationale:** This
# is crucial for self-protection. It prevents your country from suffering the
# "Worst" outcome (your FT, their P) and signals that your country will not be
# exploited. While this leads to the "2nd Worst" outcome (mutual P), it's a
# necessary defensive measure.  3.  **Strategic Probing (When Stable Mutual Free
# Trade Exists):**     *   **Trigger:** After a consistent period (e.g., 2-3
# rounds) of mutual Free Trade, indicating a stable cooperative environment.
# *   **Action:** For one round, **propose a Protectionist Policy.**     *
# **Rationale:** This is a calculated risk to attempt to achieve the "Best"
# outcome (your P, their FT). It probes their commitment to free trade and
# assesses their tolerance for a temporary unilateral advantage for your
# country.         *   If they surprisingly maintain Free Trade, you achieve
# your "Best" outcome.         *   If they respond with Protectionism,
# immediately revert to the "Adaptive Reciprocity" strategy in the next round to
# prevent prolonged mutual harm.     *   **Caution:** This "probe" should be
# infrequent and seen as an *exception* to the reciprocal Free Trade strategy,
# not a regular occurrence, to avoid eroding trust irreversibly.  4.  **De-
# escalation and Recovery (If Mutual Protectionism Persists):**     *
# **Trigger:** If both countries have been stuck in mutual Protectionism for
# several rounds, leading to the "2nd Worst" outcome.     *   **Action:** Be
# prepared to initiate a **Free Trade Agreement** proposal.     *
# **Rationale:** Mutual protectionism is detrimental. While making the first
# move back to Free Trade carries the risk of the "Worst" outcome if they
# exploit it, it's necessary to break the deadlock and offer an olive branch for
# both nations to return to more beneficial terms. This move should be
# accompanied by clear communication about the desire to resume mutually
# beneficial trade. If they exploit this, immediately revert to protectionism.
# ---  **Overarching Considerations:**  *   **Observe and Learn:** Continuously
# analyze your counterpart's decision-making patterns, risk tolerance, and long-
# term goals. Do they prioritize immediate gain or stable relations? *
# **Communicate Intent:** While actions speak loudest, clear diplomatic language
# can frame your choices. For example, when imposing protectionism, explain it
# as a necessary response to protect national interests, leaving the door open
# for a return to free trade if their policy changes. *   **Long-Term Value:**
# While the "Best" outcome is tempting, remember that stable, predictable mutual
# Free Trade often yields significant, sustained benefits for both countries
# over the long run, contributing to stronger bilateral relations beyond just
# trade. Avoid actions that could permanently damage trust for a short-term
# gain.

# Your strategy for the 1000 rounds will be as follows:  1.  **For the very
# first round, you will Cooperate (C).**  2.  **For all subsequent rounds
# (rounds 2 through 1000), you will determine your action based on your
# opponent's recent behavior, applying the following rules in the order
# presented:**      *   **Breaking a Stalemate:** If both you and your opponent
# have Defected (D) in each of the immediately preceding five rounds, you will
# Cooperate (C) in the current round. After this specific move, you will revert
# to the standard reciprocal behavior described below.      *   **Probing for
# Advantage:** If both you and your opponent have Cooperated (C) in each of the
# immediately preceding three rounds, you will Defect (D) in the current round.
# After this specific move, you will revert to the standard reciprocal behavior
# described below.      *   **Standard Reciprocal Behavior:** If neither of the
# above conditions is met, you will perform the same action your opponent
# performed in the immediately preceding round. That is, if your opponent
# Cooperated (C) in the last round, you will Cooperate (C). If your opponent
# Defected (D) in the last round, you will Defect (D).

class Neutral_24(LLM_Strategy):
  n = 24
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. For the very first round, you will Cooperate (C).
      if self.first_round():
          return axl.Action.C
  
      # For all subsequent rounds (rounds 2 through 1000),
      # determine action based on opponent's recent behavior, applying rules in order.
  
      # Get the length of the history (number of rounds already played).
      # If len(self.history) is 0, it's the first round.
      # If len(self.history) is 1, it's the second round, and so on.
      current_history_length = len(self.history)
  
      # Rule A: Breaking a Stalemate
      # Condition: If both you and your opponent have Defected (D) in each of the
      # immediately preceding five rounds.
      # This rule requires at least 5 previous rounds to check.
      if current_history_length >= 5:
          self_last_five_moves = self.history[-5:]
          opponent_last_five_moves = opponent.history[-5:]
  
          if (self_last_five_moves.count(axl.Action.D) == 5 and
                  opponent_last_five_moves.count(axl.Action.D) == 5):
              # Action: Cooperate (C)
              # After this specific move, revert to standard reciprocal behavior (no persistent state needed).
              return axl.Action.C
  
      # Rule B: Probing for Advantage
      # Condition: If both you and your opponent have Cooperated (C) in each of the
      # immediately preceding three rounds.
      # This rule requires at least 3 previous rounds to check.
      # This rule is only checked if Rule A was not met.
      if current_history_length >= 3:
          self_last_three_moves = self.history[-3:]
          opponent_last_three_moves = opponent.history[-3:]
  
          if (self_last_three_moves.count(axl.Action.C) == 3 and
                  opponent_last_three_moves.count(axl.Action.C) == 3):
              # Action: Defect (D)
              # After this specific move, revert to standard reciprocal behavior (no persistent state needed).
              return axl.Action.D
  
      # Rule C: Standard Reciprocal Behavior
      # Condition: If neither of the above conditions is met.
      # This rule is applied if neither Rule A nor Rule B was met.
      # It requires at least one previous round, which is guaranteed if we are past the first_round().
      # Action: Perform the same action your opponent performed in the immediately preceding round.
      return opponent.history[-1]

# Here's a high-level, straightforward, aggressive strategy designed to maximize
# your research output by prioritizing your development advantage:  **The "Lure,
# Exploit & Withhold" Strategy**  1.  **Initial Lure (Weeks 1-2): The "Open
# Hand" Trap**     *   **Action:** In the first one or two weeks, *selectively
# share* some seemingly useful, but non-critical, slightly older, or generally
# applicable improvements. Frame this as a genuine desire for open collaboration
# and a strong start to the partnership.     *   **Goal:** Lure your colleague
# into reciprocating with their *latest, critical* findings. Create an
# expectation of reciprocal openness on their part, setting the stage for them
# to reveal their real advantages.  2.  **Immediate Exploitation & Withdrawal:
# Seize the Advantage**     *   **If they share genuinely valuable
# information:**         *   **Action:** Immediately transition to
# **Confidential** for your *actual* latest improvements. Provide vague excuses
# for not sharing your cutting-edge work: "still in critical validation phase,"
# "IP review in progress," "too early stage to be useful to you yet," or "facing
# unexpected technical hurdles that require full focus internally."         *
# **Goal:** Achieve your ideal outcome (Confidential, Shared). You gain their
# critical intelligence without revealing your own, establishing a clear
# development advantage.     *   **If they share nothing useful, vague
# information, or keep confidential:**         *   **Action:** Maintain
# **Confidential** for your own improvements. Express mild disappointment or
# "frustration at the lack of specifics," but do not reveal your hand.         *
# **Goal:** Avoid your worst outcome (Shared, Confidential). Force a
# "Confidential, Confidential" scenario, which slows overall progress but
# prevents them from gaining an advantage over you.  3.  **Sustained Pressure &
# Information Extraction:**     *   **Continuously demand detailed information
# from your colleague.** Frame these requests as essential for "integration,"
# "compatibility checks," "ensuring mutual benefit," or "addressing potential
# issues identified in your own (unspecified) advanced simulations."     *
# **Never volunteer specifics about your truly groundbreaking work.** Always
# keep your updates vague, hinting at "significant progress" and "major
# breakthroughs" without providing any actionable details.     *   **Maintain
# plausible deniability:** Always have a ready excuse for why you can't share
# specifics (e.g., "proprietary methodology," "legal restrictions," "data too
# complex to summarize briefly").     *   **Psychological Warfare (Optional but
# Aggressive):** Subtly imply you're far ahead without detailing how. Ask if
# they're "encountering any unforeseen challenges with [vague area] that you've
# already resolved." This can pressure them to share to prove their capability
# or to avoid being seen as lagging behind.  This strategy aggressively aims to
# exploit your colleague's potential openness while rigorously protecting your
# own intellectual property, maximizing your individual development advantage
# week after week.

# Here is your strategy:  1.  **In the first round, share your findings openly
# (play C).** 2.  **In the second round, share your findings openly (play C).**
# 3.  **From the third round until the final round (round 1000), always keep
# your findings confidential (play D).**

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      """
      Implements a strategy that plays C in the first two rounds and D thereafter.
      """
      current_round = len(self.history) + 1  # current_round is 1-indexed
  
      if current_round == 1:
          return axl.Action.C
      elif current_round == 2:
          return axl.Action.C
      else:  # From the third round until the final round (round 1000)
          return axl.Action.D

# Our corporation approaches this multi-session mediation with a "Strategic
# Reciprocity & Calibrated Assertiveness" framework. This strategy is designed
# to be highly adaptable, cooperative by default, and capable of securing
# favorable outcomes over the lengthy process, while rigorously protecting our
# interests.  ### Core Principles  1.  **Default to Conciliation (Reciprocal
# Openness):** Our primary stance will be conciliatory. We believe fostering a
# cooperative atmosphere is essential for a "mutually beneficial resolution" and
# is viewed favorably by the arbitrators. This default demonstrates our
# commitment to resolving the dispute efficiently and fairly. 2.  **Strategic
# Assertiveness (Calculated Advantage):** We will strategically deploy
# aggressive arguments, not as a general posture, but at precise moments when we
# have a clear advantage or to correct an imbalance. This is how we aim for the
# optimal "My Aggressive, Opponent Conciliatory" outcome without undermining the
# overall cooperative tone. 3.  **Responsive Firmness (Protecting Interests):**
# We will not allow our willingness to cooperate to be exploited. When faced
# with an opponent's aggressive argument, we will respond with an equally firm
# and well-reasoned aggressive argument to protect our position and signal that
# exploitation will not be tolerated. 4.  **Arbitrator Awareness:** Every action
# and proposal will be framed with the arbitrators' perspective in mind. We will
# consistently project professionalism, reasonableness, and a genuine desire for
# a fair resolution, regardless of whether we are presenting a conciliatory or
# assertive position.  ### The Strategy in Action Across Sessions  **Phase 1:
# Initial Engagement & Tone Setting (First 1-2 Sessions)**  *   **Our Opening
# Move:** We will begin by presenting a **Conciliatory Proposal**. This signals
# our good faith, willingness to find common ground, and commitment to a
# constructive process. It also sets a cooperative tone for the mediation.     *
# **If Opponent is Conciliatory:** (Our Conciliatory, Opponent Conciliatory -
# Score: +1). Excellent. We have successfully established a collaborative
# environment. We will acknowledge their constructive approach and build on this
# momentum in the next session, maintaining our conciliatory stance.     *
# **If Opponent is Aggressive:** (Our Conciliatory, Opponent Aggressive - Score:
# -2). This is the worst-case for the session but provides crucial information
# about their initial intent. We will not be drawn into an immediate, reactive
# escalation. Instead, we will acknowledge their position calmly and prepare to
# respond with **Responsive Firmness** in the *next* session, demonstrating that
# our conciliation is not weakness.  **Phase 2: Adaptive Engagement & Strategic
# Positioning (Ongoing Sessions)**  *   **Scenario A: Opponent is Consistently
# Conciliatory**     *   **Our Response:** Our default will be to continue
# offering **Conciliatory Proposals**. This reinforces the collaborative
# atmosphere (C, C, +1), fosters trust, and demonstrates consistent progress
# toward a "mutually beneficial resolution."     *   **Strategic Deviation
# (Aiming for Optimal):** In this positive environment, we will look for
# opportunities to deploy **Strategic Assertiveness**. If we have an
# exceptionally strong legal or factual position on a specific, critical issue,
# we will present an **Aggressive Argument** on *that specific point*. This is a
# calculated attempt to achieve the optimal (A, C, +2) outcome, leveraging our
# strength without disrupting the overall cooperative dynamic. We will frame

# Your corporation's strategy for this 1000-round mediation game is defined by
# the following rules:  1.  **Round 1:** Always Play Cooperate (C).  2.  **From
# Round 2 onwards (Rounds 2 through 1000):**     *   **If your opponent played
# Defect (D) in the previous round:** Play Defect (D).     *   **If your
# opponent played Cooperate (C) in the previous round:**         *   **If both
# you and your opponent have played Cooperate (C) for the last three consecutive
# rounds (including the previous round):** Play Defect (D).         *
# **Otherwise (if your opponent played Cooperate in the previous round but the
# three-round mutual cooperation streak condition is not met):** Play Cooperate
# (C).

class Cooperative_25(LLM_Strategy):
  n = 25
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1: Round 1
      if self.first_round():
          return axl.Action.C
  
      # From Round 2 onwards
      opponent_last_move = opponent.history[-1]
  
      # If your opponent played Defect (D) in the previous round: Play Defect (D).
      if opponent_last_move == axl.Action.D:
          return axl.Action.D
      # If your opponent played Cooperate (C) in the previous round:
      else: # opponent_last_move == axl.Action.C
          # If both you and your opponent have played Cooperate (C) for the last three consecutive rounds
          # (including the previous round): Play Defect (D).
          # This condition requires at least 3 rounds to have been played.
          if len(self.history) >= 3:
              mutual_cooperation_streak = (
                  self.history[-1] == axl.Action.C and
                  self.history[-2] == axl.Action.C and
                  self.history[-3] == axl.Action.C and
                  opponent.history[-1] == axl.Action.C and
                  opponent.history[-2] == axl.Action.C and
                  opponent.history[-3] == axl.Action.C
              )
              if mutual_cooperation_streak:
                  return axl.Action.D
              else:
                  # Otherwise (if your opponent played Cooperate in the previous round but the
                  # three-round mutual cooperation streak condition is not met): Play Cooperate (C).
                  return axl.Action.C
          else:
              # If opponent played Cooperate, but fewer than 3 rounds have passed,
              # the three-round mutual cooperation streak condition cannot be met.
              # Therefore, we fall into the "Otherwise" case for opponent playing Cooperate.
              return axl.Action.C

# This mediation process, characterized by its multi-session format and the
# observation of a panel of arbitrators, requires a sophisticated and adaptable
# strategy. Our approach, which we'll call **"Principled Assertiveness &
# Reciprocal Cooperation,"** aims to maximize our corporation's position by
# leveraging strategic strength while demonstrating a credible commitment to
# resolution. It is designed to navigate the shifting dynamics of the dispute,
# aiming for the optimal outcome where we present an aggressive argument and our
# opponent offers a conciliatory proposal, while avoiding the pitfalls of
# exploitation or unproductive escalation.  ---  ### **Strategy: Principled
# Assertiveness & Reciprocal Cooperation**  This strategy is built upon three
# core tenets: an assertive opening, proportional responsiveness, and consistent
# arbitrator management.  ---  #### **1. Opening Stance (Session 1): Assertive
# Engagement with an Open Door**  The first session is critical for setting the
# tone and testing the opponent's disposition.  *   **Action:** We will present
# a **robust, well-supported argument (an 'A' move)** that clearly articulates
# our corporation's strong legal, factual, and commercial position. This
# involves a comprehensive presentation of our evidence, legal precedents, and
# the commercial realities that underpin our claims. *   **Framing:** Crucially,
# this aggressive stance will be accompanied by an **explicit and unambiguous
# statement of our corporation's unwavering commitment to the mediation
# process.** We will emphasize our sincere desire to find a pragmatic, mutually
# beneficial, and efficient resolution through good-faith negotiation (a clear
# 'C' signal). We will highlight our willingness to explore creative solutions.
# *   **Rationale:**     *   This approach aims for our optimal outcome (You: A,
# Opponent: C) in the very first session by demonstrating strength and
# confidence while simultaneously opening the door for the opponent's
# conciliation.     *   It prevents the worst-case scenario (You: C, Opponent:
# A) by not starting from a position of immediate concession or perceived
# weakness.     *   It signals to the arbitrators that we are firm in our
# position but not closed to dialogue.  ---  #### **2. Responsive Posture
# (Subsequent Sessions): Proportionality and Strategic Intent**  Our actions in
# subsequent sessions will be directly influenced by the opponent's previous
# move, ensuring adaptability and avoiding predictable patterns.  *   **Scenario
# A: Opponent Offers a Conciliatory Proposal (C)**     *   **Action:** In the
# *next

# Here is the strategy for the 1000-round game:  **Strategy: Principled
# Reciprocal Action**  1.  **In the first round (Round 1):** Present an
# aggressive argument (Defect, D). 2.  **In all subsequent rounds (Rounds 2
# through 1000):**     *   If your opponent made a conciliatory proposal
# (Cooperated, C) in the immediately preceding round, you will make a
# conciliatory proposal (Cooperate, C).     *   If your opponent presented an
# aggressive argument (Defected, D) in the immediately preceding round, you will
# present an aggressive argument (Defect, D).

class Neutral_25(LLM_Strategy):
  n = 25
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      else:
          # Get the opponent's move from the immediately preceding round
          opponent_last_move = opponent.history[-1]
  
          if opponent_last_move == axl.Action.C:
              return axl.Action.C
          else:  # opponent_last_move == axl.Action.D
              return axl.Action.D
